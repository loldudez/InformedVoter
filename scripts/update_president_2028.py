"""Build data/president-2028.json: who might run for President in 2028, party by party, for
the "2028 presidential field" page (#/2028).

Who is listed (the owner's choice, Nov. 25, 2026: declared, plus people who have said
they're weighing it): everyone who has declared, formed an exploratory committee, or
publicly expressed interest, each with that status. People only "speculated by the media"
and people who declined aren't listed.

Sources: English Wikipedia (CC BY-SA), read through the revision cache at the site's pace
(scripts/lib/wikitables.py):
  * "2028 Democratic Party presidential primaries" and "2028 Republican Party presidential
    primaries": the "Declared" and exploratory-committee tables (announcement date, most
    recent position, home state, campaign website, FEC filing) and the "Expressed
    interest" galleries (office and years), with each person's own subsection: the
    sentences about 2028, kept word for word with the news reports they cite.
  * "2028 United States presidential election": the same layout for the third parties and
    independents (its "Third-party and independent candidates" section), and the
    incumbent from its infobox.
  * Each person's article: a summary from its lead (about 1,000 characters), and the photo
    and website as on the Upcoming page (scripts/lib/people.py: the campaign's site from
    the table, else their official one on Wikidata, each checked to answer and show the
    name); from Wikidata, the birth date and the Congress Bioguide id.
Positions for "Compare with my views" are never inferred: recorded votes since 2021 for
anyone who served in Congress then (House roll calls, house_votes.py; Senate roll calls
from Voteview, senate_votes.py), matched by Bioguide id so a relative or namesake can't
lend their votes, the Senate's record winning over the House's on a question both answer;
and hand research in data/research/president-2028.json where it exists ({"people": {wiki
link: {"positions": {...}}}}, the overlays' format), which wins over votes.

If the pages can't be read, or list fewer than five people, the previous file is kept.

    py scripts/update_president_2028.py
"""

import html as _html
import json
import re
import sys
import time
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "lib"))
import elections as el  # noqa: E402
import cosponsors  # noqa: E402
import house_votes  # noqa: E402
import people as P  # noqa: E402
import senate_votes as SV  # noqa: E402
import wikitables as wt  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
OUT = ROOT / "data" / "president-2028.json"
RESEARCH = ROOT / "data" / "research" / "president-2028.json"
CACHE = ROOT / "data" / "cache" / "wiki" / "president-2028.json"
WIKI = "https://en.wikipedia.org/wiki/"
SPARQL = "https://query.wikidata.org/sparql"
MAIN = "2028 United States presidential election"
PARTY_PAGES = [("D", "2028 Democratic Party presidential primaries"), ("R", "2028 Republican Party presidential primaries")]
THIRD = "Third-party and independent candidates"
LEAD_DAYS = 7
SUMMARY_CHARS = 1000
SAID_CHARS = 520
STATUS_ORDER = {"declared": 0, "exploratory": 1, "interest": 2}
THIRD_PARTY = {"forward party": "Forward", "libertarian party": "L", "green party": "G", "independents": "I", "independent": "I",
               "constitution party": "Constitution", "socialist party usa": "Socialist", "party for socialism and liberation": "PSL"}


def log(*a):
    print(*a, flush=True)


def status_of(title):
    """The status a heading lists people under; None for "Speculated by the media",
    "Potential candidates", "Declined" and the rest, which aren't listed."""
    t = re.sub(r"\s+", " ", title).strip().lower()
    if re.fullmatch(r"(declared|declared candidates|candidates declared|announced|formally declared)", t):
        return "declared"
    if "exploratory" in t:
        return "exploratory"
    if re.fullmatch(r"(publicly )?expressed (an )?interest", t):
        return "interest"
    return None


def clean(h):
    h = re.sub(r"<sup[^>]*>.*?</sup>", "", h or "", flags=re.S)
    h = re.sub(r"<(style|script)[^>]*>.*?</\1>", " ", h, flags=re.S)
    return re.sub(r"\s+", " ", _html.unescape(re.sub(r"<[^>]+>", " ", h))).strip()


def own_part(s):
    """A section's HTML before its first subsection."""
    m = re.search(r'<div class="mw-heading mw-heading\d', s["html"][10:])
    return s["html"][:m.start() + 10] if m else s["html"]


def article(href):
    """The article a /wiki/ link points to, as a full link; None for files, red links and
    other namespaces."""
    if not href or not href.startswith("/wiki/") or "redlink=1" in href:
        return None
    t = href[6:].split("#")[0]
    if ":" in t.split("/")[0] and not re.match(r"^[^:]+:_", t):
        return None
    return WIKI + t


def state_code(text):
    """The state in "Governor of Kentucky" or "Former Secretary of Transportation from
    Michigan": the first "of"/"from" that names one."""
    for m in re.finditer(r"\b(?:of|from)\s+(?:the\s+)?([A-Z][A-Za-z.]+(?:\s+[A-Z][A-Za-z.]+){0,2})", text or ""):
        name = m.group(1).strip(" .")
        while name and name not in el.STATE_ABBR and " " in name:
            name = name.rsplit(" ", 1)[0]
        if name in el.STATE_ABBR:
            return el.STATE_ABBR[name]
    return el.STATE_ABBR.get((text or "").strip())


def born_from(text):
    m = re.search(r"\((\d{4}-\d{2}-\d{2})\)", text or "")
    if m:
        return m.group(1)
    m = re.search(r"\b([A-Z][a-z]+ \d{1,2}, \d{4})\b", text or "")
    if m:
        try:
            return datetime.strptime(m.group(1), "%B %d, %Y").date().isoformat()
        except ValueError:
            return None
    return None


# Statements -----------------------------------------------------------------------------

ABBR = re.compile(r"(?:\b[A-Z]\.){1,3}$|\b(?:Jr|Sr|Dr|Mr|Mrs|Ms|St|Gov|Sen|Rep|Lt|Gen|Col|No|vs|Inc|Co|Corp|Ltd|Mt|Ft)\.$")
SAYS = re.compile(r"\b(said|says|stated|told|announced|announcing|expressed|declared|filed|formed|launched|indicated|hinted|teased|"
                  r"confirmed|acknowledged|rule[ds]? out|ruling out|considering|consider|weighing|open to|plans? to|planning|"
                  r"intends?|would run|will run|not run|decision|decide[ds]?|exploratory)\b", re.I)


def split_sentences(t):
    """[(sentence, [footnote ids])]: cut after ".", "!" or "?" (and a closing quote) and
    the footnote marks that follow, unless the period ends an abbreviation ("U.S.")."""
    out, start = [], 0
    for m in re.finditer(r'([.!?]["”’]?)((?:\s*⟦[^⟧]+⟧)*)(?=\s+[A-Z"“‘0-9]|\s*$)', t):
        head = t[start:m.end(1)]
        if m.group(1).startswith(".") and ABBR.search(head):
            continue
        refs = re.findall(r"⟦([^⟧]+)⟧", t[start:m.end()])
        text = re.sub(r"\s*⟦[^⟧]+⟧", "", head).strip()
        if text:
            out.append((text, refs))
        start = m.end()
    rest = t[start:].strip()
    if rest:
        text = re.sub(r"\s*⟦[^⟧]+⟧", "", rest).strip()
        if text:
            out.append((text, re.findall(r"⟦([^⟧]+)⟧", rest)))
    return out


def statement(part_html, refs):
    """What a person's subsection says about 2028: its sentences that report what they
    said or did, word for word, with the news reports cited after them."""
    sents = []
    for p in re.findall(r"<p>(.*?)</p>", part_html, flags=re.S):
        t = re.sub(r'<sup[^>]*class="reference"[^>]*>\s*<a href="#([^"]+)".*?</sup>', lambda m: f" ⟦{_html.unescape(m.group(1))}⟧", p, flags=re.S)
        t = re.sub(r"<sup.*?</sup>", "", t, flags=re.S)
        t = re.sub(r"\s+", " ", _html.unescape(re.sub(r"<[^>]+>", "", t))).strip()
        sents += split_sentences(t)
    if not sents:
        return None, []

    def score(i, s):
        n = 3 if "2028" in s else 0
        n += 2 if SAYS.search(s) else 0
        n += 1 if re.search(r"\b202[4-8]\b", s) else 0
        if i == 0 and re.search(r"\b(is|was|has served|served|has been)\b", s) and "2028" not in s:
            n -= 2
        return n
    keep = [(i, s, r) for i, (s, r) in enumerate(sents) if score(i, s) >= 2] or [(len(sents) - 1, *sents[-1])]
    text, cites = "", []
    for _, s, r in keep:
        if text and len(text) + len(s) + 1 > SAID_CHARS:
            break
        text = f"{text} {s}".strip()
        for cid in r:
            ref = refs.get(cid)
            if ref and "wikipedia.org" not in ref["url"] and ref["url"] not in [c["url"] for c in cites]:
                cites.append({"title": ref["title"] or ref["url"], "url": ref["url"]})
    return text or None, cites[:3]


# Pages ----------------------------------------------------------------------------------

class Pages:
    def __init__(self, titles):
        self.revs = wt.revisions(titles)

    def html(self, title):
        rev = self.revs.get(title)
        return wt.page_at(rev["title"], rev) if rev else None

    def url(self, title, anchor=None):
        t = self.revs[title]["title"]
        return WIKI + t.replace(" ", "_") + (f"#{anchor}" if anchor else "")

    def source(self, title, anchor=None, label=None):
        rev = self.revs[title]
        return {"title": f"Wikipedia: {rev['title']}{f', {label}' if label else ''}", "url": self.url(title, anchor),
                "asOf": rev.get("timestamp"), "revid": rev.get("revid")}


def table_people(part_html, status):
    """People in a "Declared" or exploratory-committee table."""
    out = []
    for t in wt.tables(part_html):
        hi = el.header_row(t, "candidate")
        if hi is None:
            continue
        heads = el.heads_of(t, hi)
        c_name = el.col(heads, "candidate")
        c_born = el.col(heads, "born")
        c_pos = el.col(heads, "most recent position", "experience", "most recent", "current position")
        c_st = el.col(heads, "home state", "state")
        c_ann = next((i for i, h in enumerate(heads) if "announced" in h or h.startswith("date")), None)
        c_web = next((i for i, h in enumerate(heads) if h in ("campaign", "website", "campaign website", "links")), None)
        for row in t["rows"][hi + 1:]:
            if c_name is None or len(row) <= c_name:
                continue
            cell = row[c_name]
            link = next((l for l in cell["links"] if article(l["href"]) and l["text"].strip()), None)
            name = wt.clean_name((link["text"] if link else wt.text(cell).split("\n")[0]).strip())
            if not name or name.lower() == "candidate" or not re.search(r"[A-Za-z]", name):
                continue
            cellv = lambda i: (wt.text(row[i]) if i is not None and i < len(row) else "")  # noqa: E731
            p = {"name": name, "status": status}
            if link:
                p["wiki"] = article(link["href"])
            if cellv(c_ann):
                start, _ = el.parse_range(cellv(c_ann))
                if start:
                    p["since"] = start.isoformat()
            if cellv(c_pos):
                # One line per position; a line of years belongs to the one before it.
                lines = []
                for x in (y.strip() for y in cellv(c_pos).split("\n")):
                    if x and lines and x.startswith("("):
                        lines[-1] += f" {x}"
                    elif x:
                        lines.append(x)
                p["office"] = "; ".join(lines)
            st = cellv(c_st).strip()
            if st:
                p["st"] = el.STATE_ABBR.get(st) or state_code(st)
            b = born_from(cellv(c_born))
            if b:
                p["born"] = b
            if c_web is not None and c_web < len(row):
                for l in row[c_web]["links"]:
                    href = l["href"]
                    if not href.startswith("http") or "wikipedia.org" in href:
                        continue
                    if "fec.gov" in href:
                        p.setdefault("fec", href)
                    else:
                        p.setdefault("campaignSite", href)
            out.append(p)
    return out


GALLERY = re.compile(r'<li class="gallerybox"[^>]*>.*?<div class="gallerytext">(.*?)</div>\s*</li>', re.S)
YEARS = re.compile(r"^\(\s*(?:\d{4}|c\.)[^)]*\)$")


def gallery_people(part_html, status, names_here):
    """People in an "Expressed interest" gallery: the caption's office, name, state and
    years, one per line."""
    out = []
    for cap in GALLERY.findall(part_html):
        lines = [x for x in re.split(r"<br\s*/?>", cap)]
        texts = [clean(x) for x in lines]
        idx, link = None, None
        for i, x in enumerate(lines):
            a = re.search(r'<a\s[^>]*href="([^"]+)"[^>]*>(.*?)</a>', x, flags=re.S)
            if a and article(_html.unescape(a.group(1))) and clean(a.group(2)) == texts[i] and (texts[i] in names_here or idx is None):
                idx, link = i, article(_html.unescape(a.group(1)))
                if texts[i] in names_here:
                    break
        if idx is None:  # a caption with no link: the line that is a person's subsection title
            idx = next((i for i, x in enumerate(texts) if x in names_here), None)
            if idx is None:
                continue
        name = texts[idx]
        rest = [x for i, x in enumerate(texts) if i != idx and x]
        notes = [x.strip("() ") for x in rest if x.startswith("(") and not YEARS.match(x)]
        office = " ".join(x for x in rest if not (x.startswith("(") and not YEARS.match(x)))
        p = {"name": name, "status": status, "office": re.sub(r"\s+", " ", office).strip() or None}
        if link:
            p["wiki"] = link
        st = state_code(" ".join(rest))
        if st:
            p["st"] = st
        if notes:
            p["note"] = "; ".join(notes)
        out.append(p)
    return out


REF_ITEM = re.compile(r'<li id="(cite(?:_|&#95;)note-[^"]+)"[^>]*>(.*?)</li>', re.S)
EXT_LINK = re.compile(r'<a[^>]*href="(https?://[^"]+)"[^>]*>(.*?)</a>', re.S)


def refs_of(h):
    """{footnote id: {"url", "title"}}: each reference's first link off Wikipedia (some
    start with an "[update]" link to the page's own edit form)."""
    out = {}
    for m in REF_ITEM.finditer(h):
        for u, label in EXT_LINK.findall(m.group(2)):
            u = _html.unescape(u)
            if re.search(r"(wikipedia|wikimedia|wikidata)\.org", u):
                continue
            out[_html.unescape(m.group(1))] = {"url": u, "title": clean(label).strip("\"“”' ") or u}
            break
    return out


def read_page(pages, title, party, third=False):
    """Everyone a page lists as declared, exploring or interested, with their statement."""
    h = pages.html(title)
    if not h:
        return [], []
    refs = refs_of(h)
    secs = wt.split_sections(h)
    found, checks = [], []
    in_third, group = False, None
    for i, s in enumerate(secs):
        if s["level"] == 2:
            in_third = s["title"].strip().lower() == THIRD.lower()
        if third:
            if not in_third:
                continue
            if s["level"] == 4:
                t = s["title"].strip().lower()
                group = THIRD_PARTY.get(t) or re.sub(r"\s+party$", "", s["title"].strip(), flags=re.I)
                continue
        status = status_of(s["title"])
        if not status:
            continue
        # This status's own subsections are its people's paragraphs.
        subs = []
        for s2 in secs[i + 1:]:
            if s2["level"] <= s["level"]:
                break
            if s2["level"] == s["level"] + 1:
                subs.append(s2)
        names_here = {x["title"] for x in subs}
        part = own_part(s)
        people = table_people(part, status) + gallery_people(part, status, names_here)
        for p in people:
            p["party"] = group if third else party
            sub = next((x for x in subs if el.norm(x["title"]) == el.norm(p["name"])), None)
            if sub:
                said, cites = statement(own_part(sub), refs)
                if said:
                    p["said"] = said
                    p["saidSources"] = cites
                p["source"] = pages.source(title, sub["id"], p["name"])
                if not cites:
                    checks.append(f"{p['name']}: the paragraph on {title} cites no news report for what it says")
            else:
                p["source"] = pages.source(title, s["id"], s["title"])
                if status == "interest":
                    checks.append(f"{p['name']}: listed under “{s['title']}” on {title} with no paragraph saying what they said")
            if not p.get("wiki"):
                checks.append(f"{p['name']}: no Wikipedia article linked on {title}")
            found.append(p)
    return found, checks


def incumbent(pages):
    h = pages.html(MAIN)
    if not h:
        return None
    for t in wt.tables(h)[:4]:
        for row in t["rows"]:
            for c in row:
                lines = [x.strip() for x in wt.text(c).split("\n") if x.strip()]
                if lines and lines[0].lower().startswith("incumbent president") and len(lines) >= 3:
                    out = {"name": lines[1], "party": el.party_code(lines[2])}
                    link = next((article(l["href"]) for l in c["links"] if article(l["href"]) and l["text"].strip() == lines[1]), None)
                    if link:
                        out["wiki"] = link
                    txt = clean(h)
                    out["termLimited"] = bool(re.search(re.escape(lines[1]) + r"[^.]{0,80}ineligible to run for a third term", txt))
                    return out
    return None


# Articles and Wikidata ------------------------------------------------------------------

def _load():
    try:
        return json.loads(CACHE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def _save(data):
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    tmp = Path(str(CACHE) + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    tmp.replace(CACHE)


def long_leads(titles):
    """{title: {"text": the article's whole lead as plain text, "qid"}}."""
    cache = _load()
    leads = cache.setdefault("leads", {})
    now = time.time()
    need = [t for t in dict.fromkeys(titles) if now - (leads.get(t) or {}).get("at", 0) > LEAD_DAYS * 86400]
    for i in range(0, len(need), 20):
        batch = need[i:i + 20]
        q = wt.api({"action": "query", "prop": "extracts|pageprops", "exintro": 1, "explaintext": 1, "exlimit": 20,
                    "ppprop": "wikibase_item|disambiguation", "redirects": 1, "titles": "|".join(batch)})["query"]
        fwd = {n["from"]: n["to"] for n in q.get("normalized", []) + q.get("redirects", [])}
        got = {p["title"]: p for p in q.get("pages", [])}
        for t in batch:
            cur, seen = t, set()
            while cur in fwd and cur not in seen:
                seen.add(cur)
                cur = fwd[cur]
            p = got.get(cur) or {}
            pp = p.get("pageprops") or {}
            ok = not p.get("missing") and "disambiguation" not in pp
            leads[t] = {"at": now, "text": p.get("extract") if ok else None, "qid": pp.get("wikibase_item") if ok else None}
    if need:
        _save(cache)
    return {t: leads[t] for t in titles if t in leads}


def summary(text):
    """The lead's first paragraphs, up to about SUMMARY_CHARS characters."""
    paras = [P.tidy_bio(x, 100_000) for x in (text or "").split("\n") if x.strip()]
    paras = [x for x in paras if x and len(x) > 40]
    out = []
    for x in paras:
        if not out:
            out.append(P.tidy_bio(x, SUMMARY_CHARS))
        elif sum(len(y) for y in out) + len(x) <= SUMMARY_CHARS:
            out.append(x)
        else:
            break
    return out


def wikidata(qids):
    """{qid: {"bioguide", "born"}} from Wikidata (P1157, P569)."""
    cache = _load()
    store = cache.setdefault("wikidata", {})
    now = time.time()
    need = [q for q in dict.fromkeys(qids) if q and now - (store.get(q) or {}).get("at", 0) > LEAD_DAYS * 86400]
    for i in range(0, len(need), 100):
        batch = need[i:i + 100]
        sparql = ("SELECT ?item ?bio ?dob WHERE { VALUES ?item { " + " ".join(f"wd:{q}" for q in batch) + " } "
                  "OPTIONAL { ?item wdt:P1157 ?bio } OPTIONAL { ?item wdt:P569 ?dob } }")
        rows = wt.api({"query": sparql}, base=SPARQL)["results"]["bindings"]
        got = {q: {"at": now} for q in batch}
        for b in rows:
            q = b["item"]["value"].rsplit("/", 1)[-1]
            if q not in got:
                continue
            if b.get("bio") and not got[q].get("bioguide"):
                got[q]["bioguide"] = b["bio"]["value"]
            if b.get("dob") and not got[q].get("born"):
                got[q]["born"] = b["dob"]["value"][:10]
        store.update(got)
    if need:
        _save(cache)
    return {q: store[q] for q in qids if q in store}


# Positions ------------------------------------------------------------------------------

SUFFIX = re.compile(r"\s+(Jr\.?|Sr\.?|II|III|IV)$")


def attach_positions(people_list, checks):
    """Recorded votes since 2021 (by Bioguide id), then the bills they sponsored or
    cosponsored for questions no vote answers, then hand research on top."""
    try:
        house = house_votes.HouseRecord()
    except Exception as e:  # noqa: BLE001
        house = None
        checks.append(f"House roll calls unavailable: {e}")
    try:
        senate = SV.SenateRecord()
    except Exception as e:  # noqa: BLE001
        senate = None
        checks.append(f"Voteview's Senate roll calls unavailable: {e}")
    try:
        bills = cosponsors.Cosponsors()
        checks.extend(f"Bill cosponsors: {x}" for x in bills.problems)
    except Exception as e:  # noqa: BLE001
        bills = None
        checks.append(f"Bill cosponsors unavailable: {e}")
    try:
        research = json.loads(RESEARCH.read_text(encoding="utf-8")).get("people", {})
    except (OSError, ValueError):
        research = {}
    for p in people_list:
        pos, votes = {}, {}
        bg = p.get("bioguide")
        if bg and house:
            v = house.votes_for(bg)
            if v:
                surname = SUFFIX.sub("", p["name"]).split()[-1]
                for q, stance, src, _ in house_votes.vote_positions(surname, v):
                    pos[q] = {"stance": stance, "source": src}
                votes["house"] = len(v)
        if bg and senate:
            icpsr = senate.by_bioguide.get(bg)
            v = senate.votes_of(icpsr) if icpsr else {}
            if v:
                for q, stance, src, _ in SV.vote_positions(senate, p["name"], v):
                    pos[q] = {"stance": stance, "source": src}
                votes["senate"] = len(v)
        if bg and bills:
            for q, b in bills.positions(bg, SUFFIX.sub("", p["name"]).split()[-1]).items():
                pos.setdefault(q, b)
        mine = (research.get(p.get("wiki") or "") or {}).get("positions") or {}
        if pos or mine:
            p["positions"] = {**pos, **mine}
            p["positionsFrom"] = "research+votes" if pos and mine else "research" if mine else "votes"
        if votes:
            p["votes"] = votes


# Build ----------------------------------------------------------------------------------

def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", el.norm(name)).strip("-")


def main():
    pages = Pages([MAIN] + [t for _, t in PARTY_PAGES])
    everyone, checks, sources = [], [], []
    for party, title in PARTY_PAGES:
        found, ch = read_page(pages, title, party)
        everyone += found
        checks += ch
        if pages.revs.get(title):
            sources.append(pages.source(title, None, "Candidates"))
    found, ch = read_page(pages, MAIN, None, third=True)
    everyone += found
    checks += ch
    if pages.revs.get(MAIN):
        sources.append(pages.source(MAIN, THIRD.replace(" ", "_"), THIRD))
    # One entry per person (a page can list someone twice: in a table and a gallery).
    seen, people = {}, []
    for p in everyone:
        k = p.get("wiki") or el.norm(p["name"])
        if k in seen:
            old = seen[k]
            if STATUS_ORDER[p["status"]] < STATUS_ORDER[old["status"]]:
                old.update({x: y for x, y in p.items() if y})
            continue
        seen[k] = p
        people.append(p)
    if len(people) < 5:
        log(f"only {len(people)} people found; keeping the previous file")
        return 1

    # Articles: summary, birth date, Congress id; photos and websites as on the Upcoming page.
    titles = {p["wiki"]: P.title_of(p["wiki"]) for p in people if p.get("wiki")}
    leads = long_leads(sorted({t for t in titles.values() if t}))
    facts = wikidata(sorted({(leads.get(t) or {}).get("qid") for t in titles.values() if (leads.get(t) or {}).get("qid")}))
    persons = [{"name": p["name"], "wiki": p.get("wiki"), **({"site": p["campaignSite"]} if p.get("campaignSite") else {})} for p in people]
    known, _ = P.enrich(persons, log=log)
    for p, q in zip(people, persons):
        p["id"] = slug(p["name"])
        p["key"] = f"p2028:{p['id']}"
        t = titles.get(p.get("wiki"))
        lead = leads.get(t) or {}
        if lead.get("text"):
            paras = summary(lead["text"])
            if paras:
                p["summary"] = paras
        f = facts.get(lead.get("qid")) or {}
        if f.get("born") and not p.get("born"):
            p["born"] = f["born"]
        if f.get("bioguide"):
            p["bioguide"] = f["bioguide"]
        k = known.get(p.get("wiki")) or {}
        if k.get("photo"):
            p["photo"] = k["photo"]
        if not p.get("summary") and k.get("bio"):
            p["summary"] = [k["bio"]]
        p.pop("campaignSite", None)
        if q.get("site"):
            p["site"], p["siteKind"] = q["site"], "campaign"
        elif k.get("site"):
            p["site"], p["siteKind"] = k["site"], "official"
    attach_positions(people, checks)

    groups = []
    for gid, name in (("D", "Democratic Party"), ("R", "Republican Party"), ("other", "Third parties and independents")):
        mine = [p for p in people if (p["party"] == gid if gid != "other" else p["party"] not in ("D", "R"))]
        mine.sort(key=lambda p: (STATUS_ORDER[p["status"]], p.get("since") or "9999", P.last_name(p["name"])))
        src = pages.source(dict(PARTY_PAGES)[gid], None, "Candidates") if gid in ("D", "R") and pages.revs.get(dict(PARTY_PAGES)[gid]) \
            else pages.source(MAIN, THIRD.replace(" ", "_"), THIRD) if pages.revs.get(MAIN) else None
        groups.append({"id": gid, "name": name, "source": src, "people": mine})
    out = {
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "date": date(2028, 11, 7).isoformat(),
        "incumbent": incumbent(pages),
        "groups": groups,
        "sources": sources,
        "checks": checks,
        "stats": {s: sum(1 for p in people if p["status"] == s) for s in STATUS_ORDER},
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    withpos = sum(1 for p in people if p.get("positions"))
    log(f"2028 field: {len(people)} people ({', '.join(f'{v} {k}' for k, v in out['stats'].items())}), "
        f"{sum(1 for p in people if p.get('summary'))} summaries, {sum(1 for p in people if p.get('photo'))} photos, "
        f"{sum(1 for p in people if p.get('site'))} websites, {withpos} with positions; {len(checks)} checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
