"""Build data/upcoming.json: the elections of the next three years (2027, 2028 and 2029)
for the "Upcoming elections" page (#/upcoming): president, Senate (regular and special),
House, governors and the statewide offices below governor, each with its date, who holds
the office, whether they can or will run again, and the declared candidates.

Source: English Wikipedia's national pages, the same aggregator (CC BY-SA) as the 2026
races, read through the revision cache at the site's slow pace (scripts/lib/wikitables.py):
  * "<year> United States gubernatorial elections", "... lieutenant gubernatorial
    elections", "... attorney general elections", "... secretary of state elections",
    "... state treasurer elections" and "... state auditor elections" for 2027-2029,
    wherever the page exists: each "Race summary" table gives the state, the officeholder
    and party, their last race, a status ("Term-limited", "Incumbent running") and the
    candidates.
  * "2028 United States Senate elections": the regular seats and the special elections
    (Tennessee's), in the same layout.
  * Special Senate elections in the odd years, from the "U.S. Senate" line of the "<year>
    United States elections" navigation box (Minnesota's in 2027), each read from its own
    page: the date, the seat's party and the "Declared" candidates of each primary.
  * "2028 United States presidential election": the incumbent, and the "Declared" tables
    of each party's primaries (exploratory committees and people who have only expressed
    interest are left out).
The House is up in full every even year (all 435 seats on Nov. 7, 2028); Wikipedia has no
2028 House page yet, so that entry carries the date only.

Only declared candidates are listed, as on the France pages: the "Candidates" column of
the summary tables (parts of a cell headed "Potential:" or "Declined:" are dropped), "TBD"
meaning no one has declared, plus the "Declared" lists of each race's own page (linked
from the table, or from the navigation box where the table only points at its own
section), which the tables lag behind: Kentucky's 2027 governor table lacked three
declared Republicans and an independent. A link that redirects to a page about many
races (most of them do) isn't read. Potential candidates and people who have only
expressed interest, which the race pages also list, are left out.
Dates are each page's own ("October 9 (Louisiana)" overrides the general date for that
state), never a sentence about a primary, a runoff or a deadline ("The primary election
for all offices will be held on May 18, 2027"), falling back to the first Tuesday after
the first Monday in November.

No forecasts: nothing is rated this early, and the only polls test people who aren't
running. The 2026 runoffs still ahead come from the race data itself (the page reads
races.json), not from this file.

Below the national pages, in keys of their own ("more", "local", "legislatures"), so
pages built before them never miscount them:
  * Statewide offices the national pages don't cover (agriculture and insurance
    commissioners, Wisconsin's Supreme Court), from the "<year> <State> elections" pages
    of the navigation box's "States and territories" line, each office's section giving
    its holder and declared candidates; a holder the section doesn't name comes from the
    office's own article (its infobox's "Incumbent").
  * Offices of the navigation box with no national page (2028's attorneys general): the
    states it lists, the holder from the office's article.
  * Mayors: the "Mayoral elections" lists of "<year> United States elections" (each city,
    its mayor and their plans), with the date and declared candidates from the race's
    page where it has one.
  * County offices from the navigation box's "Local" line ("2028 Los Angeles County
    elections": the district attorney, the new county executive). Seats elected by
    district (supervisors, councils, commissions) are left out: without their district
    maps the site can't tell whose ballot they are on.
  * State legislatures (2027: Louisiana, Mississippi, New Jersey, Virginia): every
    district's member, from the election page's results-by-district table or the
    chamber's own article, with the retirements the election page lists; an empty seat
    is kept as vacant. The district numbers match the Census Bureau's, so "My elections"
    finds a visitor's own seats. Louisiana's chambers take its statewide offices' first
    round as their date (the chamber pages give the runoff's).
  * An officeholder declared for another office the same year gets that as their plans.
  * People (scripts/lib/people.py): a two-sentence bio from each linked article's lead,
    a Wikidata photo and a website (campaign sites from race pages, else the person's
    official website on Wikidata), each website checked to answer and show the name.

If none of the pages can be read, the previous file is kept.

    py scripts/update_upcoming.py
"""

import html as _html
import json
import re
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "lib"))
import elections as el  # noqa: E402
import people as P  # noqa: E402
import wikitables as wt  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
OUT = ROOT / "data" / "upcoming.json"
WIKI = "https://en.wikipedia.org/wiki/"
YEARS = (2027, 2028, 2029)

# (office key, id code, page title, default office name), in the order the page lists them.
STATE_PAGES = [
    ("governor", "GOV", "{y} United States gubernatorial elections", "Governor"),
    ("lieutenant-governor", "LG", "{y} United States lieutenant gubernatorial elections", "Lieutenant Governor"),
    ("attorney-general", "AG", "{y} United States attorney general elections", "Attorney General"),
    ("secretary-of-state", "SOS", "{y} United States secretary of state elections", "Secretary of State"),
    ("treasurer", "TREAS", "{y} United States state treasurer elections", "State Treasurer"),
    ("auditor", "AUD", "{y} United States state auditor elections", "State Auditor"),
]
SENATE = "{y} United States Senate elections"
PRESIDENT = "{y} United States presidential election"
ELECTIONS = "{y} United States elections"
# "TBD", "TBD in 2026" (Vermont's two-year offices, before the 2026 winner is filled in),
# "To be appointed" and the like: no one to list.
NOT_A_NAME = re.compile(r"^(tbd|tba|to be (determined|announced|appointed))\b.*$|^(none( yet| declared)?|n/?a|vacant|unopposed)$", re.I)
KEEP_PARTS = ("declared", "candidate", "running", "announced", "filed", "nominee")
MONTH_RE = r"(January|February|March|April|May|June|July|August|September|October|November|December)"


def log(*a):
    print(*a, flush=True)


def general_day(y):
    """The first Tuesday after the first Monday in November."""
    d = date(y, 11, 2)
    while d.weekday() != 1:
        d += timedelta(days=1)
    return d


class Pages:
    def __init__(self):
        self.revs = {}
        self.used = []  # titles whose text was read, in order

    def prefetch(self, titles):
        need = [t for t in dict.fromkeys(titles) if t not in self.revs]
        if need:
            self.revs.update(wt.revisions(need))

    def html(self, title):
        self.prefetch([title])
        rev = self.revs.get(title)
        if rev and title not in self.used:
            self.used.append(title)
        return wt.page_at(rev["title"], rev) if rev else None

    def source(self, title, anchor=None, label=None):
        rev = self.revs[title]
        url = WIKI + rev["title"].replace(" ", "_") + (f"#{anchor.replace(' ', '_')}" if anchor else "")
        return {"title": f"Wikipedia: {rev['title']}{f', {label}' if label else ''}", "url": url, "asOf": rev.get("timestamp")}


def page_text(h):
    h = re.sub(r"<(style|script)[^>]*>.*?</\1>", " ", h, flags=re.S)
    h = re.sub(r"<sup[^>]*>.*?</sup>", "", h, flags=re.S)
    h = re.sub(r"<(br|/p|/li|/tr|/td|/th|/div|/h\d)[^>]*>", "\n", h)
    import html as _html
    return re.sub(r"[ \t\xa0]+", " ", _html.unescape(re.sub(r"<[^>]+>", " ", h)))


HELD = re.compile(r"(?:scheduled to be held|will be held|to be held|will take place|scheduled for|held on)[^.]{0,120}?"
                  + MONTH_RE + r" (\d{1,2}), (\d{4})")


def held_date(txt, y):
    """The first election day a text gives ("will be held in the U.S. state of Kentucky
    on November 2, 2027"), passing over sentences about primaries, runoffs and deadlines
    ("The primary election for all offices will be held on May 18, 2027")."""
    t = (txt or "").replace("U.S.", "US")
    for m in HELD.finditer(t):
        if int(m.group(3)) != y:
            continue
        start = max(t.rfind(". ", 0, m.start()), t.rfind("\n", 0, m.start()), 0)
        if re.search(r"primar|caucus|runoff|filing|deadline|registration", t[start:m.end()], re.I):
            continue
        return date(y, el.MONTHS[m.group(1).lower()], int(m.group(2)))
    return None


def page_dates(h, y):
    """The page's general date and per-state exceptions: ({state: date}, general date),
    read from the lead and its infobox only ("November 2, 2027 / October 9 (Louisiana)"),
    so primary dates further down never pass for an election day."""
    cut = re.search(r"<h2[\s>]", h)
    txt = page_text(h[:cut.start()] if cut else h)
    general = held_date(txt, y)
    exceptions = {}
    # "October 9 (Louisiana)" in the infobox (links leave spaces inside the brackets).
    for m in re.finditer(MONTH_RE + r" (\d{1,2})(?:, (\d{4}))?\s*\(\s*([A-Z][A-Za-z ]+?)\s*\)", txt):
        st = el.STATE_ABBR.get(m.group(4).strip())
        if st and (not m.group(3) or int(m.group(3)) == y):
            exceptions[st] = date(y, el.MONTHS[m.group(1).lower()], int(m.group(2)))
    # "... in Louisiana on October 9" and "... and on October 9, 2027, in Louisiana" in the lead.
    for m in re.finditer(r"in ([A-Z][a-z]+(?: [A-Z][a-z]+)?) on " + MONTH_RE + r" (\d{1,2})(?:, (\d{4}))?", txt):
        st = el.STATE_ABBR.get(m.group(1))
        if st and (not m.group(4) or int(m.group(4)) == y):
            exceptions.setdefault(st, date(y, el.MONTHS[m.group(2).lower()], int(m.group(3))))
    for m in re.finditer(r"on " + MONTH_RE + r" (\d{1,2}), (\d{4}),? in ([A-Z][a-z]+(?: [A-Z][a-z]+)?)", txt):
        st = el.STATE_ABBR.get(m.group(4))
        if st and int(m.group(3)) == y:
            d = date(y, el.MONTHS[m.group(1).lower()], int(m.group(2)))
            if d != general:
                exceptions.setdefault(st, d)
    return exceptions, general or general_day(y)


def wiki_link(cell, name=None):
    for l in cell["links"]:
        href = l["href"]
        if not href.startswith("/wiki/") or ":" in href[6:]:
            continue
        if name is None or el.norm(l["text"]) == el.norm(name):
            return "https://en.wikipedia.org" + href
    return None


def declared_from_cell(cell):
    """'▌Rocky Adkins (Democratic)\n▌Jacqueline Coleman (Democratic)' -> declared people;
    "TBD" and the parts of a cell headed "Potential:" or "Declined:" are left out."""
    out, seen = [], set()
    for name, party, _won, part in el.candidate_lines(wt.text(cell)):
        if part and not any(w in part for w in KEEP_PARTS):
            continue
        if NOT_A_NAME.match(name) or el.norm(name) in seen or len(name) > 60:
            continue
        seen.add(el.norm(name))
        p = {"name": name, "party": party}
        link = wiki_link(cell, name)
        if link:
            p["wiki"] = link
        out.append(p)
    return out


def holder_of(inc_cell, party_cell):
    """The officeholder: name, party and article; None for a seat to be filled."""
    name = wt.text(inc_cell).split("\n")[0].strip() if inc_cell is not None else ""
    party_text = re.sub(r"\s+", " ", wt.text(party_cell)).strip() if party_cell is not None else ""
    party = el.party_code(party_text) if party_text and not NOT_A_NAME.match(party_text) else None
    h = {"party": party if party in ("D", "R", "I", "L", "G") else (party or None)}
    if not name or NOT_A_NAME.match(name) or name.lower().startswith(("to be appointed", "tbd")):
        h["name"] = None
        h["appointment"] = name.lower().startswith("to be appointed")
    else:
        h["name"] = re.sub(r"\s+", " ", re.sub(r"[†‡*]", "", name)).strip()
        link = wiki_link(inc_cell)
        if link:
            h["wiki"] = link
    return h


def plans(status_text, holder, cands):
    """'running' | 'leaving' | 'unknown', from the status and whether the officeholder is
    among the declared candidates."""
    s = status_text.lower()
    if holder.get("name") and any((c.get("wiki") and c.get("wiki") == holder.get("wiki")) or el.norm(c["name"]) == el.norm(holder["name"]) for c in cands):
        return "running"
    if any(w in s for w in ("term-limited", "term limited", "retiring", "to run for", "not running", "not seeking", "resign", "lost")):
        return "leaving"
    if "running" in s or "seeking re-election" in s:
        return "running"
    return "unknown"


def tidy_status(s):
    s = re.sub(r"\s+", " ", s.replace("\n", " ")).strip().replace("'", "’")
    return s[0].upper() + s[1:] if s else s


def summary_rows(h):
    """(section title, table, header row index) for every table in the "Race summary"
    section (or "States"), the header row being the last of the table's heading rows."""
    out = []
    secs = wt.split_sections(h)
    chunks = []
    for i, s in enumerate(secs):
        if s["level"] == 2 and s["title"] in ("Race summary", "States", "Summary"):
            subs = []
            for t in secs[i + 1:]:
                if t["level"] <= 2:
                    break
                subs.append(t)
            if subs and any(wt.tables(t["html"]) for t in subs):
                chunks += [(t["title"], t["html"]) for t in subs if t["level"] == 3]
            else:
                chunks.append((s["title"], s["html"]))
            break
    seen = set()
    for title, chunk in chunks:
        for t in wt.tables(chunk):
            key = id(t)
            heads_rows = [i for i in range(min(3, len(t["rows"]))) if "candidates" in el.heads_of(t, i)]
            if not heads_rows or key in seen:
                continue
            seen.add(key)
            out.append((title, t, heads_rows[-1]))
    return out


def state_races(pages, y, key, code, title, default):
    h = pages.html(title)
    if not h:
        return []
    exceptions, general = page_dates(h, y)
    out = []
    for sec_title, t, hi in summary_rows(h):
        heads = el.heads_of(t, hi)
        c_cand = el.col(heads, "candidates")
        c_status = el.col(heads, "status", "results")
        c_last = el.col(heads, "last race")
        c_first = el.col(heads, "first elected", "electoral history")
        c_party = el.col(heads, "party")
        if c_party is None and len(heads) > 2 and heads[2] == "":
            c_party = 2  # the Senate's colored party column has no heading of its own
        for row in t["rows"][hi + 1:]:
            if c_cand is None or c_cand >= len(row):
                continue
            label = wt.text(row[0]).replace("\n", " ").strip()
            st = el.STATE_ABBR.get(re.sub(r"\(.*?\)", "", label).strip())
            if not st:
                continue  # territories (the site covers the states and D.C.)
            special = "special" in sec_title.lower() or "special" in label.lower()
            rid = f"{y}-{st}-{code}{'-SP' if special else ''}"
            cands = declared_from_cell(row[c_cand])
            holder = holder_of(row[1], row[c_party] if c_party is not None and c_party < len(row) else None)
            status = cell_text(row, c_status) or ""
            status = tidy_status(status) if status else ""
            for c in cands:
                c["incumbent"] = bool(holder.get("name")) and ((c.get("wiki") and c.get("wiki") == holder.get("wiki")) or el.norm(c["name"]) == el.norm(holder["name"]))
            # "Incumbent running" with "TBD" in the candidates column: the status is the
            # officeholder's declaration, so they are listed.
            if holder.get("name") and not any(c["incumbent"] for c in cands) and re.match(r"^incumbent running\b", status, re.I):
                cands.insert(0, {k: v for k, v in (("name", holder["name"]), ("party", holder.get("party") or "I"), ("wiki", holder.get("wiki")), ("incumbent", True)) if v is not None})
            link = next((l for l in row[0]["links"] if l["title"].startswith(str(y)) and "page does not exist" not in l["title"]), None)
            anchor = next((l["href"] for l in row[0]["links"] if l["href"].startswith("#")), None)
            if link:
                page = {"title": link["title"], "url": WIKI + link["title"].replace(" ", "_")}
            elif anchor:  # "State (linked to summaries below)": the national page's own section
                page = {"title": f"{pages.revs[title]['title']}: {el.STATE_NAME.get(st, st)}", "url": WIKI + pages.revs[title]["title"].replace(" ", "_") + anchor}
            else:
                page = None
            d = exceptions.get(st, general)
            race = {
                "id": rid, "year": y, "date": d.isoformat(), "office": key,
                "officeName": office_name(link["title"] if link else None, el.STATE_NAME.get(st, ""), default, y),
                "state": st, "special": special, "holder": holder,
                "firstElected": cell_text(row, c_first), "lastRace": cell_text(row, c_last),
                "statusText": status, "plans": plans(status, holder, cands),
                "candidates": cands, "page": page,
                "source": pages.source(title, "Race summary", "Race summary"),
            }
            if st == "LA" and d != general:
                race["dateNote"] = "Louisiana’s first round: if no one wins a majority, the top two meet in a runoff."
            out.append(race)
    return out


def cell_text(row, i):
    """A cell's text on one line; None for a missing cell or a placeholder ("TBD in 2026")."""
    if i is None or i >= len(row):
        return None
    s = re.sub(r"\s+", " ", wt.text(row[i])).strip()
    return None if not s or NOT_A_NAME.match(s) else s


def office_name(page_title, state_name, default, y):
    """'2027 Kentucky Attorney General election' -> 'Attorney General'."""
    if not page_title:
        return default
    t = re.sub(r"^\d{4}\s+", "", page_title)
    t = re.sub(r"\s+(special\s+)?elections?(\s+in\s+.*)?$", "", t, flags=re.I)
    if t.startswith(state_name + " "):
        t = t[len(state_name) + 1:]
    if not t or "gubernatorial" in t.lower() or "senate" in t.lower() or len(t) > 60:
        return default
    return t[0].upper() + t[1:]


def special_titles(pages, y):
    """Special Senate elections in a year without regular ones, from the navigation box
    of "<year> United States elections" (its "U.S. Senate" line)."""
    h = pages.html(ELECTIONS.format(y=y))
    if not h:
        return []
    out = []
    for t in wt.tables(h):
        for row in t["rows"]:
            if len(row) >= 2 and wt.text(row[0]).strip().lower() in ("u.s. senate", "senate"):
                for l in row[1]["links"]:
                    if "senate" in l["title"].lower() and "special" in l["title"].lower() and l["title"].startswith(str(y)):
                        out.append(l["title"])
    return list(dict.fromkeys(out))


def declared_lists(h):
    """The "Declared" lists of a race page: [(party code, name, article)]. Each list sits
    under a party's primary heading ("Democratic–Farmer–Labor primary")."""
    out, party = [], None
    for s in wt.split_sections(h):
        if s["level"] == 2:
            party = el.party_code(re.sub(r"\s+(primary|primaries|convention|nomination).*$", "", s["title"], flags=re.I))
        if s["title"].strip().lower() not in ("declared", "declared candidates", "candidates declared"):
            continue
        body = s["html"]
        for li in re.findall(r"<li[^>]*>(.*?)</li>", body, flags=re.S):
            a = re.search(r'<a [^>]*href="(/wiki/[^"#:]+)"[^>]*>(.*?)</a>', li, flags=re.S)
            txt = re.sub(r"<[^>]+>", "", li)
            name = re.sub(r"<[^>]+>", "", a.group(2)).strip() if a else re.split(r",|\(", txt)[0].strip()
            import html as _html
            name = _html.unescape(name)
            if name and not NOT_A_NAME.match(name) and len(name) <= 60:
                out.append((party if party in ("D", "R", "L", "G") else "I", name,
                            "https://en.wikipedia.org" + a.group(1) if a and re.sub(r"<[^>]+>", "", a.group(2)).strip() == name else None))
    return out


def special_race(pages, y, title):
    h = pages.html(title)
    if not h:
        return None
    m = re.search(r"special election in (.+)$", title)
    st = el.STATE_ABBR.get(m.group(1).strip()) if m else None
    if not st:
        return None
    exceptions, general = page_dates(h, y)
    # The infobox: "Incumbent U.S. senator / TBD" and, in the same cell or the next row,
    # the seat's party ("Democratic (DFL)").
    holder = {"name": None, "party": None, "appointment": False}
    found = False
    for t in wt.tables(h)[:8]:
        rows = t["rows"]
        for ri, row in enumerate(rows):
            for c in row:
                lines = [l.strip() for l in wt.text(c).split("\n") if l.strip()]
                if not lines or not lines[0].lower().startswith("incumbent") or len(lines) < 2:
                    continue
                name = lines[1]
                party_line = lines[2] if len(lines) >= 3 else (wt.text(rows[ri + 1][0]).strip() if ri + 1 < len(rows) and rows[ri + 1] else "")
                party = el.party_code(re.sub(r"\(.*?\)", "", party_line).strip()) if party_line else None
                holder = {"name": None if NOT_A_NAME.match(name) else name, "party": party if party in ("D", "R", "I", "L", "G") else None,
                          "appointment": bool(NOT_A_NAME.match(name))}
                if holder["name"]:
                    link = wiki_link(c, name)
                    if link:
                        holder["wiki"] = link
                found = True
                break
            if found:
                break
        if found:
            break
    cands, seen = [], set()
    for party, name, link in declared_lists(h):
        if el.norm(name) in seen:
            continue
        seen.add(el.norm(name))
        c = {"name": name, "party": party, "incumbent": False}
        if link:
            c["wiki"] = link
        cands.append(c)
    return {
        "id": f"{y}-{st}-SEN-SP", "year": y, "date": exceptions.get(st, general).isoformat(), "office": "senate",
        "officeName": "U.S. Senate", "state": st, "special": True, "holder": holder,
        "firstElected": None, "lastRace": None,
        "statusText": "To be filled by appointment until the special election" if holder.get("appointment") else "",
        "plans": "unknown" if not holder.get("name") else plans("", holder, cands), "candidates": cands,
        "page": {"title": pages.revs[title]["title"], "url": WIKI + pages.revs[title]["title"].replace(" ", "_")},
        "source": pages.source(title, None, "Candidates"),
    }


def president(pages, y):
    title = PRESIDENT.format(y=y)
    h = pages.html(title)
    if not h:
        return None
    _, general = page_dates(h, y)
    txt = page_text(h)
    holder = {"name": None, "party": None}
    for t in wt.tables(h)[:4]:
        for row in t["rows"]:
            for c in row:
                lines = [l.strip() for l in wt.text(c).split("\n") if l.strip()]
                if lines and lines[0].lower().startswith("incumbent president") and len(lines) >= 3:
                    holder = {"name": lines[1], "party": el.party_code(lines[2])}
                    link = wiki_link(c, lines[1])
                    if link:
                        holder["wiki"] = link
                    break
            if holder["name"]:
                break
        if holder["name"]:
            break
    status = ""
    if holder["name"] and re.search(re.escape(holder["name"]) + r"[^.]{0,80}ineligible to run for a third term", txt):
        status = "Term-limited (22nd Amendment)"
    cands, primaries, seen = [], [], set()
    parent = sub = None
    for s in wt.split_sections(h):
        if s["level"] == 2:
            parent, sub = s["title"], None
            if parent.lower().endswith("primaries"):
                primaries.append({"party": el.party_code(re.sub(r"\s+primaries$", "", parent, flags=re.I)), "title": parent, "declared": 0})
        elif s["level"] == 3:
            sub = s["title"]
        if not parent or s["title"].strip().lower() not in ("declared", "candidates", "declared candidates"):
            continue
        third = "third" in parent.lower() or "independent" in parent.lower()
        if not (parent.lower().endswith("primaries") or third):
            continue
        if parent.lower().endswith("primaries"):
            party = el.party_code(re.sub(r"\s+primaries$", "", parent, flags=re.I))
        else:
            party = el.party_code(re.sub(r"\s+Party$", "", sub)) if sub and sub.endswith("Party") and s["level"] > 3 else None
        for t in wt.tables(s["html"]):
            hi = el.header_row(t, "candidate")
            if hi is None:
                continue
            heads = el.heads_of(t, hi)
            c_ann = el.col(heads, "announcement date", "announced", "date announced")
            if c_ann is None:
                continue
            c_exp, c_st, c_party = el.col(heads, "experience", "most recent position"), el.col(heads, "state", "home state"), el.col(heads, "party")
            for row in t["rows"][hi + 1:]:
                if len(row) <= c_ann:
                    continue
                cell = row[0]
                link = next((l for l in cell["links"] if l["href"].startswith("/wiki/") and ":" not in l["href"][6:] and l["text"].strip()), None)
                name = (link["text"] if link else wt.text(cell).split("\n")[0]).strip()
                if not name or NOT_A_NAME.match(name) or el.norm(name) in seen:
                    continue
                seen.add(el.norm(name))
                start, _ = el.parse_range(wt.text(row[c_ann]))
                p = party or (el.party_code(wt.text(row[c_party])) if c_party is not None and c_party < len(row) else "I")
                c = {"name": name, "party": p, "incumbent": False, "announced": el.iso(start),
                     "experience": re.sub(r"\s+", " ", wt.text(row[c_exp])).strip() if c_exp is not None and c_exp < len(row) else None,
                     "home": re.sub(r"\s+", " ", wt.text(row[c_st])).strip() if c_st is not None and c_st < len(row) else None}
                if link:
                    c["wiki"] = "https://en.wikipedia.org" + link["href"]
                cands.append(c)
                for pr in primaries:
                    if pr["title"] == parent:
                        pr["declared"] += 1
    return {
        "id": f"{y}-US-PRES", "year": y, "date": general.isoformat(), "office": "president", "officeName": "President",
        "state": None, "special": False, "holder": holder, "firstElected": None, "lastRace": None,
        "statusText": status, "plans": "leaving" if status else plans("", holder, cands), "candidates": cands,
        "primaries": [{"party": p["party"], "declared": p["declared"]} for p in primaries],
        "page": {"title": pages.revs[title]["title"], "url": WIKI + pages.revs[title]["title"].replace(" ", "_")},
        "source": pages.source(title, None, "Declared candidates"),
    }


# =====================================================================================
# Below the national pages: other statewide offices, mayors, counties and legislatures.
# =====================================================================================

STATE_RE = "|".join(sorted(map(re.escape, el.STATE_ABBR), key=len, reverse=True))
NUM_WORDS = {w: i + 1 for i, w in enumerate(
    "one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen".split())}
# Sections listing people who have announced (and their sub-lists, like "Minor candidates").
DECLARED_HEAD = re.compile(r"^(declared|declared candidates|candidates declared|announced|minor candidates|other declared candidates)$", re.I)
NOT_PERSON = re.compile(r"\b(Party|Department|Commission|Court|County|Council|Board|Office|election|elections|Senate|House|Assembly|"
                        r"United States|Attorney General|Secretary of State|Governor|Mayor|Treasurer|Auditor|Legislature|District|"
                        r"University|College|School|Company|Corporation|Inc)\b")
NAMEISH = re.compile(r"^[A-Z][\w.'’-]*(?:\s+(?:[A-Z\"“(][\w.'’”)-]*|de|la|van|von|der|del|da|di|le|bin)){1,5}$")
SITE_WORDS = ("website", "campaign website", "official website", "campaign site", "campaign")
NAV_OFFICES = {  # navigation-box line -> (office key, id code, default name, articles naming the holder)
    "governors": ("governor", "GOV", "Governor", ["Governor of {s}"]),
    "lieutenant governors": ("lieutenant-governor", "LG", "Lieutenant Governor", ["Lieutenant Governor of {s}"]),
    "attorneys general": ("attorney-general", "AG", "Attorney General", ["{s} Attorney General", "Attorney General of {s}"]),
    "secretaries of state": ("secretary-of-state", "SOS", "Secretary of State", ["{s} Secretary of State", "Secretary of State of {s}"]),
    "state treasurers": ("treasurer", "TREAS", "State Treasurer", ["{s} State Treasurer", "Treasurer of {s}", "{s} Treasurer"]),
    "state auditors": ("auditor", "AUD", "State Auditor", ["{s} State Auditor", "Auditor of {s}", "{s} Auditor"]),
}
# Offices of a state's own elections page that the national pages don't cover, by section
# title; anything elected by district is left out (see the module docstring).
STATE_OFFICES = [
    (r"agricultur", "agriculture"), (r"insurance", "insurance"), (r"supreme court", "supreme-court"),
    (r"superintendent|public instruction", "superintendent"), (r"\blabor\b", "labor"), (r"public lands|land commissioner", "lands"),
]
# Judges keep only the party their page's list gives them: most states print none on the
# ballot, and the party of a judge's earlier career (Wikidata's) isn't the one running.
JUDICIAL = {"supreme-court"}
COVERED = re.compile(r"governor|attorney general|secretary of state|treasurer|auditor|comptroller|controller", re.I)
BY_DISTRICT = re.compile(r"commission\b|board|court of appeals|circuit|district|legislat|senate|house|assembly|council", re.I)
COUNTY_BY_DISTRICT = re.compile(r"board|council|commission|supervisor|court|judge|judicial|school|college|water|district \d|ward", re.I)


def clean(h):
    """A piece of page HTML as one line of text, without footnote marks."""
    h = re.sub(r"<sup[^>]*>.*?</sup>", "", h or "", flags=re.S)
    h = re.sub(r"<(style|script)[^>]*>.*?</\1>", " ", h, flags=re.S)
    return re.sub(r"\s+", " ", _html.unescape(re.sub(r"<[^>]+>", " ", h))).strip()


def links_in(h):
    """[(href, title, text)] for each link in a piece of page HTML, in order."""
    out = []
    for m in re.finditer(r"<a\s([^>]*)>(.*?)</a>", h or "", flags=re.S):
        href = re.search(r'href="([^"]*)"', m.group(1))
        title = re.search(r'title="([^"]*)"', m.group(1))
        out.append((_html.unescape(href.group(1)) if href else "", _html.unescape(title.group(1)) if title else "", clean(m.group(2))))
    return out


def article(href):
    """'/wiki/Brandon_Johnson' -> its address; None for red links, files and other namespaces."""
    if not href or not href.startswith("/wiki/") or ":" in unquote(href[6:]).split("#")[0]:
        return None
    return "https://en.wikipedia.org" + href.split("#")[0]


def own_html(h):
    """A section's own part, without its subsections."""
    heads = list(wt._HEADING.finditer(h))
    return h[:heads[1].start()] if len(heads) > 1 else h


def party_of(text):
    t = re.sub(r"[^a-z]", "", (text or "").lower())
    if t in ("r", "rep", "republican") or t.startswith("republican"):
        return "R"
    if t in ("d", "dem", "democratic", "democrat", "dfl") or t.startswith("democrat"):
        return "D"
    if t in ("i", "ind", "independent"):
        return "I"
    return el.party_code(text) if t else None


def plain_status(s):
    """(status, plans) in the site's own words, from Wikipedia's phrasing of a holder's
    plans ("is ineligible to run for re-election due to term limits" -> "Term-limited")."""
    t = (s or "").lower()
    if re.search(r"term[- ]limit|ineligible|can(not|'t|’t| not) (seek|run|be re-?elected)", t):
        return "Term-limited", "leaving"
    if re.search(r"\bresign", t):
        return ("Resigned before the end of the term; a special election fills the seat" if "special" in t else "Resigned"), "leaving"
    # Negations first: "is not seeking a full term" is no declaration.
    if re.search(r"not (to )?(run|seek)|will not|won['’]t|retir|declined|isn['’]t running|stepping down|leaving office", t):
        return "Not running again", "leaving"
    if re.search(r"running for (re-?election|a (second|third|fourth|fifth|sixth|full|final)\b[\w ]*term|another term)|"
                 r"seeking (re-?election|another term|a (second|third|full)\b[\w ]*term)|running again", t):
        return "Running for another term", "running"
    if re.search(r"running for|seeking the|candidate for", t):
        return "Running for another office", "leaving"
    if re.search(r"not (yet )?(indicated|announced|said|decided)|undecided|unclear|intent unknown", t):
        return "Hasn’t announced plans yet", "unknown"
    if "eligible" in t:
        return "Can run again; no announcement yet", "unknown"
    return "", "unknown"


def lead_date(h, y):
    """The election day a race page's lead gives, or None."""
    cut = re.search(r"<h2[\s>]", h)
    txt = page_text(h[:cut.start()] if cut else h)
    d = held_date(txt, y)
    if d:
        return d
    # Else the first date of the year that isn't a primary's (the infobox's comes first).
    t = txt.replace("U.S.", "US")
    for m in re.finditer(r"(?<![\w-])" + MONTH_RE + r" (\d{1,2}), " + str(y), t):
        start = max(t.rfind(". ", 0, m.start()), t.rfind("\n", 0, m.start()), 0)
        if not re.search(r"primar|caucus|runoff|filing|deadline|registration", t[start:m.end()], re.I):
            return date(y, el.MONTHS[m.group(1).lower()], int(m.group(2)))
    return None


def incumbent_in(h):
    """(name, article, rest of the sentence) for the officeholder a paragraph of prose
    names: the first link to a person after "Incumbent", within that sentence."""
    m = re.search(r"\bincumbent\b", h or "", flags=re.I)
    if not m:
        return None
    seg = h[m.start():]
    for lm in re.finditer(r"<a\s([^>]*)>(.*?)</a>", seg, flags=re.S):
        before = clean(seg[:lm.start()])
        if re.search(r"[a-z]{2}\.\s+[A-Z]", before) or "</p>" in seg[:lm.start()]:
            return None  # past the sentence
        href = re.search(r'href="([^"]*)"', lm.group(1))
        title = re.search(r'title="([^"]*)"', lm.group(1))
        text = clean(lm.group(2))
        wiki = article(_html.unescape(href.group(1))) if href else None
        if not text or not text[0].isupper() or NOT_PERSON.search(_html.unescape(title.group(1)) if title else text) \
                or not NAMEISH.match(text):
            continue
        rest = clean(seg[lm.end():])
        rest = re.split(r"(?<=[a-z\d)]{2})\.(?:\s|$)", rest)[0]
        return text, wiki, rest.strip(" ,")
    return None


def li_person(li):
    """(name, article, the rest of the line) for a list entry such as
    '[[Mike Harmon]], former auditor of public accounts (2016–2024)'."""
    txt = clean(li)
    if not txt or len(txt) > 700:
        return None
    lk = [l for l in links_in(li) if l[2]]
    head = clean(li.split("<a", 1)[0]) if "<a" in li else txt
    if lk and not head and article(lk[0][0]):
        name, wiki = lk[0][2], article(lk[0][0])
        rest = txt[len(name):] if txt.startswith(name) else txt.split(name, 1)[-1]
    else:
        name, wiki = re.split(r",|\(| – | — | - |;", txt)[0].strip(), None
        rest = txt[len(name):]
    name = re.sub(r"\s+", " ", name).strip(" ,.")
    if not name or NOT_A_NAME.match(name) or len(name) > 60 or re.search(r"\d", name) or not name[0].isupper():
        return None
    exp = re.sub(r"^[\s,;:–—-]+", "", rest).strip()
    return name, wiki, (exp[:197].rsplit(" ", 1)[0] + "…" if len(exp) > 200 else exp) or None


def declared_people(h, base_party=None):
    """[{"name", "party", "wiki", "experience", "site"}] from the "Declared" lists and
    tables of a race page (or of one office's section of a state page). Under a party's
    primary heading the people take its party; in nonpartisan races they take none."""
    out, seen, party = [], set(), base_party

    def add(name, wiki, exp, site, p):
        if el.norm(name) in seen:
            return
        seen.add(el.norm(name))
        c = {"name": name, "party": p, "incumbent": False}
        if wiki:
            c["wiki"] = wiki
        if exp:
            c["experience"] = exp
        if site:
            c["site"] = site
        out.append(c)

    for s in wt.split_sections(h):
        title = s["title"].strip()
        low = title.lower()
        if s["level"] <= 3 and re.search(r"\b(primary|primaries|convention|nomination|caucus)\b", low):
            party = el.party_code(re.sub(r"\s+(primary|primaries|convention|nomination|caucus)\b.*$", "", title, flags=re.I))
            party = party if party in ("D", "R", "L", "G") else "I"
        elif s["level"] <= 3 and re.match(r"^independents?$|^independent candidates?$", low):
            party = "I"
        elif s["level"] == 2:
            party = base_party
        if not DECLARED_HEAD.match(low):
            continue
        body = own_html(s["html"])
        for t in wt.tables(body):
            hi = el.header_row(t, "candidate")
            hi = el.header_row(t, "name") if hi is None else hi
            if hi is None:
                continue
            heads = el.heads_of(t, hi)
            c_name = el.col(heads, "candidate", "name") or 0
            c_exp = el.col(heads, "experience", "most recent position", "current or previous", "occupation", "background", "position")
            for row in t["rows"][hi + 1:]:
                if c_name >= len(row):
                    continue
                cell = row[c_name]
                link = next((l for l in cell["links"] if article(l["href"]) and l["text"].strip()), None)
                name = (link["text"] if link else wt.text(cell).strip().split("\n")[0]).strip()
                if not name or NOT_A_NAME.match(name) or len(name) > 60 or el.norm(name) in ("", "candidate"):
                    continue
                exp = wt.text(row[c_exp]) if c_exp is not None and c_exp < len(row) else ""
                # One line per position, its years kept with it: "Illinois Comptroller
                # (2016–present); Chicago City Clerk (2011–2016)".
                exp = re.sub(r"\s*\n\s*(?=[(\[])", " ", exp)
                exp = re.sub(r"\s+", " ", exp.replace("\n", "; ")).strip(" ;") or None
                site = next((l["href"] for c in row for l in c["links"]
                             if l["href"].startswith("http") and l["text"].strip().lower() in SITE_WORDS), None)
                add(name, article(link["href"]) if link else None, exp[:200] if exp else None, site, party)
        for attrs, li in re.findall(r"<li([^>]*)>(.*?)</li>", re.sub(r"<table.*?</table>", " ", body, flags=re.S), flags=re.S):
            if "gallery" in attrs or "/wiki/File:" in li:
                continue
            got = li_person(li)
            if got:
                add(got[0], got[1], got[2], None, party)
    return out


def attach_sites(cands, sites):
    """Campaign sites from a page's External links, for the candidates they name."""
    for name, party, url in sites:
        c = el.match_candidate(name, cands, party if party in ("D", "R") else None)
        if c and not c.get("site"):
            c["site"] = url


def navbox(pages, y):
    """{line: [(title, exists)]} from the "<year> United States elections" navigation box."""
    h = pages.html(ELECTIONS.format(y=y))
    if not h:
        return {}
    out = {}
    for t in wt.tables(h):
        for row in t["rows"]:
            if len(row) < 2:
                continue
            label = re.sub(r"\s+", " ", wt.text(row[0])).strip().lower()
            if not label or len(label) > 40:
                continue
            for l in row[1]["links"]:
                title = l.get("title") or ""
                if title and not title.startswith(("Template", "Special:", "Help:", "Wikipedia:")):
                    out.setdefault(label, []).append((title.replace(" (page does not exist)", ""), "page does not exist" not in title))
    return out


def state_in(text):
    m = re.search(rf"\b({STATE_RE})\b", text or "")
    return el.STATE_ABBR[m.group(1)] if m else None


def infobox_holder(h):
    """{"name", "wiki", "since"} for the "Incumbent" of an office's infobox (or an agency's
    "Agency executive"), or None."""
    for t in wt.tables(h)[:3]:
        rows = t["rows"]
        for ri, row in enumerate(rows):
            for c in row:
                first = wt.text(c).strip().split("\n")[0].strip().lower()
                if first.startswith("incumbent"):
                    near = [c] + [cell for r in rows[ri + 1:ri + 4] for cell in r]
                elif re.search(r"\bexecutives?$", first) and len(row) > 1 and c is row[0]:
                    # "Agency executive", "Department of Justice executive" (Montana's
                    # attorney general heads its Department of Justice).
                    near = row[1:]
                else:
                    continue
                for cell in near:
                    link = next((l for l in cell["links"] if article(l["href"]) and NAMEISH.match(l["text"].strip())
                                 and not NOT_PERSON.search(l["title"] or l["text"])), None)
                    if link:
                        txt = " ".join(wt.text(x) for x in near)
                        since = re.search(r"since\s+((?:" + MONTH_RE + r"\s+\d{1,2},\s+)?\d{4})", txt)
                        return {"name": link["text"].strip(), "wiki": article(link["href"]), "since": since.group(1) if since else None}
                return None
    return None


def office_holder(pages, guesses):
    """The holder an office's article names, from the first of `guesses` that exists."""
    pages.prefetch(guesses)
    for g in guesses:
        if not pages.revs.get(g):
            continue
        hd = infobox_holder(pages.html(g) or "")
        if hd:
            return hd, pages.source(g, None, "infobox")
    return None, None


def missing_offices(pages, nav, races, checks):
    """Offices the navigation box lists without a national page (2028's attorneys
    general): one race per state, its holder from the office's article."""
    have = {(r["year"], r["state"], r["office"]) for r in races}
    todo = []
    for y, rows in nav.items():
        for label, (key, code, default, guesses) in NAV_OFFICES.items():
            for title, _exists in rows.get(label, []):
                if not title.startswith(str(y)) or "special" in title.lower():
                    continue
                st = state_in(title)
                if not st or (y, st, key) in have:
                    continue
                have.add((y, st, key))
                todo.append((y, st, key, code, default, [g.format(s=el.STATE_NAME[st]) for g in guesses]))
    pages.prefetch([g for *_, gs in todo for g in gs])
    out = []
    for y, st, key, code, default, guesses in todo:
        holder, hsrc = office_holder(pages, guesses)
        h = {"name": holder["name"], "party": None, "wiki": holder["wiki"]} if holder else {"name": None, "party": None}
        if not holder:
            checks.append(f"{y} {el.STATE_NAME[st]} {default}: no article named the officeholder")
        out.append({
            "id": f"{y}-{st}-{code}", "year": y, "date": general_day(y).isoformat(), "office": key, "officeName": default,
            "state": st, "special": False, "holder": h, "since": holder.get("since") if holder else None,
            "firstElected": None, "lastRace": None, "statusText": "", "plans": "unknown", "candidates": [],
            "page": None, "holderSource": hsrc,
            "source": pages.source(ELECTIONS.format(y=y), None, "navigation box") | {"note": "listed in the navigation box; no page of its own yet"},
        })
    return out


def state_page_offices(pages, y, nav, races, checks):
    """Statewide offices of a state's "<year> <State> elections" page that the national
    pages don't cover, each with its holder and declared candidates."""
    have = {(r["state"], r["office"]) for r in races if r["year"] == y}
    titles = [t for t, ok in nav.get("states and territories", []) if ok and not t.startswith("Category:")]
    pages.prefetch(titles)
    out = []
    for title in titles:
        st = state_in(title)
        h = pages.html(title)
        if not st or not h:
            continue
        ex, general = page_dates(h, y)
        secs = wt.split_sections(h)
        for i, s in enumerate(secs):
            name = s["title"].strip()
            hit = next((k for pat, k in STATE_OFFICES if re.search(pat, name, re.I)), None)
            if not hit or COVERED.search(name) or (st, hit) in have:
                continue
            body = s["html"]
            if BY_DISTRICT.search(name) or re.search(r"\bdistricts?\b", clean(own_html(body))[:300], re.I):
                continue
            # Skip a section whose parent is the same office (the page repeats headings).
            have.add((st, hit))
            inc = incumbent_in(own_html(body)) or incumbent_in(body)
            holder, plans_, status = {"name": None, "party": None}, "unknown", ""
            if inc:
                holder = {"name": inc[0], "party": None}
                if inc[1]:
                    holder["wiki"] = inc[1]
                status, plans_ = plain_status(inc[2])
            hsrc = None
            main = next((t for href, t, _ in links_in(own_html(body)) if article(href) and t.startswith(str(y))), None)
            office_name = re.sub(r"^(State|Commissioner of)\s+", lambda m: "" if m.group(1) == "State" else m.group(0), name)
            if not holder["name"]:
                hd, hsrc = office_holder(pages, [f"{el.STATE_NAME[st]} {name}", f"{name} of {el.STATE_NAME[st]}",
                                                 f"{el.STATE_NAME[st]} {re.sub(r'^Commissioner of ', '', name)} Commissioner"])
                if hd:
                    holder = {"name": hd["name"], "party": None, "wiki": hd["wiki"]}
            cands = declared_people(body)
            page, d = None, ex.get(st, general)
            d = held_date(clean(own_html(body)) + "\n" + clean(body)[:600], y) or d
            if main:
                pages.prefetch([main])
                mh = pages.html(main)
                if mh:
                    cands = cands or declared_people(mh)
                    attach_sites(cands, el.campaign_sites(mh))
                    d = lead_date(mh, y) or d
                    page = {"title": pages.revs[main]["title"], "url": WIKI + pages.revs[main]["title"].replace(" ", "_")}
            if holder["name"]:
                for c in cands:
                    c["incumbent"] = (c.get("wiki") and c.get("wiki") == holder.get("wiki")) or el.norm(c["name"]) == el.norm(holder["name"])
                if plans_ == "running" and not any(c["incumbent"] for c in cands):
                    cands.insert(0, {k: v for k, v in holder.items() if v is not None} | {"incumbent": True})
                if any(c["incumbent"] for c in cands):
                    plans_, status = "running", "Running for another term"
            out.append({
                "id": f"{y}-{st}-{hit.upper()}", "year": y, "date": d.isoformat(), "office": hit, "officeName": office_name,
                "level": "state", "state": st, "special": False, "holder": holder, "firstElected": None, "lastRace": None,
                "statusText": status, "plans": plans_, "candidates": cands,
                "page": page or {"title": f"{pages.revs[title]['title']}: {name}", "url": WIKI + pages.revs[title]["title"].replace(" ", "_") + "#" + s["id"]},
                "source": pages.source(title, s["id"], name), **({"holderSource": hsrc} if hsrc else {}),
            })
        if not out:
            checks.append(f"{title}: no other statewide office found")
    return out


def mayor_race(li, y, src):
    txt = clean(li)
    m = re.match(r"^(?P<city>[^:]+?),\s*(?P<state>" + STATE_RE + r")\b(?P<special>\s*\(special(?: election)?\))?\s*:?\s*(?P<rest>.*)$", txt)
    if not m:
        return None
    st = el.STATE_ABBR[m.group("state")]
    city, rest = m.group("city").strip(), m.group("rest").strip()
    lk = links_in(li)
    page = next((t for href, t, _ in lk if article(href) and re.match(rf"^{y}\b.*\bmayoral (special )?election", t)), None)
    nm = re.search(r"\b[Ii]ncumbent(?:\s+mayor)?\s+(?P<name>[A-Z][\w.'’\- ]*?)\s*,?\s+(?P<status>(?:is|was|has|have|had|will|resigned|"
                   r"announced|died|lost|cannot|can't|won't|did|plans|intends|faces|filed|decided)\b.*)$", rest)
    name = nm.group("name").strip() if nm else None
    wiki = next((article(h) for h, _, t in lk if article(h) and name and el.norm(t) == el.norm(name)), None) if name else None
    status, plans_ = plain_status(nm.group("status") if nm else rest)
    terms = re.search(r"\b(" + "|".join(NUM_WORDS) + r")-term\b", rest, re.I)
    holder = {"name": name, "party": None}
    if wiki:
        holder["wiki"] = wiki
    special = bool(m.group("special"))
    slug = re.sub(r"[^a-z0-9]+", "-", el.norm(city)).strip("-")
    return {
        "id": f"{y}-{st}-MAYOR-{slug}{'-SP' if special else ''}", "year": y, "date": None, "office": "mayor", "officeName": "Mayor",
        "level": "local", "state": st, "place": city, "special": special, "holder": holder,
        "terms": NUM_WORDS[terms.group(1).lower()] if terms else None, "statusText": status, "plans": plans_,
        "candidates": [], "page": {"title": page, "url": WIKI + page.replace(" ", "_")} if page else None, "source": src,
    }


def mayors(pages, y):
    """Every city in the "Mayoral elections" lists of "<year> United States elections"."""
    title = ELECTIONS.format(y=y)
    h = pages.html(title)
    if not h:
        return []
    secs = wt.split_sections(h)
    parts, parent = [], None
    for s in secs:
        if s["level"] <= 3:
            parent = s["title"].lower()
        if s["level"] == 4 and parent and "mayor" in parent and "incumbent" in s["title"].lower():
            parts.append(s)
    if not parts:
        parts = [s for s in secs if s["level"] == 3 and "mayor" in s["title"].lower()]
    src = pages.source(title, parts[0]["id"] if parts else None, "Mayoral elections") if parts else None
    out, seen = [], set()
    for s in parts:
        for li in re.findall(r"<li[^>]*>(.*?)</li>", s["html"], flags=re.S):
            r = mayor_race(li, y, src)
            if r and r["id"] not in seen:
                seen.add(r["id"])
                out.append(r)
    return out


def county_races(pages, y, nav):
    """Countywide offices from the county pages on the navigation box's "Local" line."""
    out = []
    titles = [t for t, ok in nav.get("local", []) if ok and re.match(rf"^{y} .+ County(?:, [A-Za-z ]+)? elections$", t)]
    pages.prefetch(titles)
    for title in titles:
        h = pages.html(title)
        if not h:
            continue
        county = re.match(rf"^{y} (.+? County)", title).group(1)
        st = state_in(title.split(",", 1)[1]) if "," in title else None
        if not st:
            # "Los Angeles County, California" in the text, else the page's link to the
            # county's own article (titled that way), to its state's elections sidebar
            # ("Elections in California") or to its state's elections of the year.
            sm = re.search(re.escape(county) + r",?\s+(" + STATE_RE + r")\b", page_text(h))
            st = el.STATE_ABBR[sm.group(1)] if sm else None
            for pat in (rf"^{re.escape(county)}, ({STATE_RE})$", rf"^Elections in ({STATE_RE})$", rf"^{y} ({STATE_RE}) elections$"):
                st = st or next((state_in(t) for href, t, _ in links_in(h) if article(href) and re.match(pat, t)), None)
        if not st:
            continue
        for s in wt.split_sections(h):
            name = s["title"].strip()
            # Boards and courts are elected by district; a district attorney isn't.
            if s["level"] != 2 or name.lower() in SKIP_SECTIONS or COUNTY_BY_DISTRICT.search(name):
                continue
            body = s["html"]
            inc = incumbent_in(body)
            holder, status, plans_ = {"name": None, "party": None}, "", "unknown"
            if inc:
                holder = {"name": inc[0], "party": None, **({"wiki": inc[1]} if inc[1] else {})}
                status, plans_ = plain_status(inc[2])
            elif re.search(r"new office|for the first time|first election", clean(body), re.I):
                status = f"A new office, elected for the first time in {y}"
            main = next((t for href, t, _ in links_in(body) if article(href) and t.startswith(str(y))), None)
            cands, page, d = declared_people(body), None, general_day(y)
            if main:
                pages.prefetch([main])
                mh = pages.html(main)
                if mh:
                    cands = cands or declared_people(mh)
                    attach_sites(cands, el.campaign_sites(mh))
                    d = lead_date(mh, y) or d
                    page = {"title": pages.revs[main]["title"], "url": WIKI + pages.revs[main]["title"].replace(" ", "_")}
            slug = re.sub(r"[^a-z0-9]+", "-", el.norm(f"{county} {name}")).strip("-")
            out.append({
                "id": f"{y}-{st}-{slug}", "year": y, "date": d.isoformat(), "office": "county", "officeName": name,
                "level": "local", "state": st, "county": county, "special": False, "holder": holder, "statusText": status,
                "plans": plans_, "candidates": cands,
                "page": page or {"title": f"{pages.revs[title]['title']}: {name}", "url": WIKI + pages.revs[title]["title"].replace(" ", "_") + "#" + s["id"]},
                "source": pages.source(title, s["id"], name),
            })
    return out


SKIP_SECTIONS = {"see also", "references", "notes", "external links", "footnotes", "further reading", "bibliography", "background"}


def district_of(text):
    m = re.search(r"\d+", text or "")
    return str(int(m.group(0))) if m else None


def member_table_rows(t, hi, summary):
    heads = el.heads_of(t, hi)
    c_d = next((i for i, x in enumerate(heads) if "district" in x), None)
    c_n = el.col(heads, "incumbent") if summary else el.col(heads, "name", "representative", "senator", "delegate", "member",
                                                            "assemblymember", "assembly member", "legislator")
    c_p = el.col(heads, "party")
    if c_d is None or c_n is None:
        return []
    c_pres = next((i for i, x in enumerate(heads) if re.search(r"\bpres", x)), None)
    c_first = el.col(heads, "first elected", "first election", "start", "assumed office", "took office", "in office since", "since")
    c_tl = el.col(heads, "term-limited", "term limited")
    c_elig = el.col(heads, "eligible")
    rows = []
    for row in t["rows"][hi + 1:]:
        if max(c_d, c_n) >= len(row):
            continue
        d = district_of(wt.text(row[c_d]))
        cell = row[c_n]
        link = next((l for l in cell["links"] if article(l["href"]) and l["text"].strip()), None)
        name = (link["text"] if link else wt.text(cell).split("\n")[0]).strip()
        name = re.sub(r"\s*\((?:incumbent|resigned|died)[^)]*\)", "", name).strip()
        if d and re.match(r"^vacan(t|cy)\b", name, re.I):
            # An empty seat still has an election (Louisiana's House 77 and 92 on Nov. 5, 2026).
            rows.append({"district": d, "name": None, "party": None, "vacant": True})
            continue
        if not d or not name or NOT_A_NAME.match(name) or name.lower() in ("district", "name", "incumbent") or len(name) > 60:
            continue
        party = None
        if c_p is not None:
            for j in (c_p, c_p + 1):
                if j < len(row) and wt.text(row[j]).strip():
                    party = party_of(wt.text(row[j]))
                    break
        m = {"district": d, "name": name, "party": party if party in ("D", "R", "I", "L", "G") else party}
        if link:
            m["wiki"] = article(link["href"])
        if c_first is not None and c_first < len(row):
            yr = re.search(r"\b(19|20)\d{2}\b", wt.text(row[c_first]))
            if yr:
                m["firstElected"] = yr.group(0)
        if c_pres is not None and c_pres < len(row):
            pm = re.search(r"\b([DR])\s*\+\s*([\d.]+)", wt.text(row[c_pres]))
            if pm:
                m["dr"] = round(float(pm.group(2)) * (1 if pm.group(1) == "D" else -1), 1)
        limited = None
        if c_tl is not None and c_tl < len(row):
            limited = wt.text(row[c_tl]).strip().lower().startswith("y")
        elif c_elig is not None and c_elig < len(row):
            v = wt.text(row[c_elig]).strip().lower()
            limited = v.startswith("n") if v else None
        if limited:
            m["statusText"], m["plans"] = "Term-limited", "leaving"
        rows.append(m)
    return rows


def member_rows(h, summary):
    """Every district's member: from a "Summary of results by district" table (`summary`,
    "District | 2024 Pres. | Incumbent | Party ...") or a chamber article's members table."""
    best = []
    for t in wt.tables(h):
        for hi in range(min(3, len(t["rows"]))):
            heads = el.heads_of(t, hi)
            if not any("district" in x for x in heads):
                continue
            if summary and "incumbent" not in heads:
                continue
            rows = member_table_rows(t, hi, summary)
            if len(rows) > len(best):
                best = rows
            break
    return best


def retirements(h):
    """[(district, name, status)] from an election page's lists of incumbents who aren't
    running ("Retirements", "Incumbents not running for re-election")."""
    out = []
    for s in wt.split_sections(h):
        if not re.search(r"retir|not (running|seeking)|not standing|open seats", s["title"], re.I):
            continue
        for li in re.findall(r"<li[^>]*>(.*?)</li>", s["html"], flags=re.S):
            txt = clean(li)
            dm = re.search(r"(?:District|SD|HD|LD|AD)[\s-]*(\d+)|(\d+)(?:st|nd|rd|th)?\s+[Dd]istrict", txt)
            if not dm:
                continue
            person = next((t for h_, _, t in links_in(li) if article(h_) and NAMEISH.match(t)), None)
            status, plans_ = plain_status(txt)
            out.append((str(int(dm.group(1) or dm.group(2))), person, status if plans_ == "leaving" else "Not running again"))
    return out


def legislature_races(pages, y, nav, checks):
    """Each chamber of the navigation box's "State legislatures" line, with every
    district's member."""
    out = []
    titles = [t for t, ok in nav.get("state legislatures", []) if ok]
    pages.prefetch(titles)
    for title in titles:
        h = pages.html(title)
        if not h:
            continue
        real = pages.revs[title]["title"]
        m = re.match(rf"^{y} (?P<chamber>.+?) (?:special )?elections?$", real)
        st = state_in(real)
        if not m or not st:
            continue
        chamber = m.group("chamber")
        upper = "senate" in chamber.lower()
        rows, src = member_rows(h, summary=True), pages.source(title, None, "results by district")
        if not rows:
            cut = re.search(r"<h2[\s>]", h)
            lead = h[:cut.start()] if cut else h
            art = next((t for href, t, _ in links_in(lead) if article(href) and not t[:1].isdigit() and state_in(t) == st
                        and re.search(r"Senate|House|Assembly|Delegates", t) and (("Senate" in t) == upper)), None)
            if art:
                pages.prefetch([art])
                ah = pages.html(art)
                rows = member_rows(ah, summary=False) if ah else []
                src = pages.source(art, None, "members")
        if not rows:
            checks.append(f"{real}: no list of members read")
            continue
        districts = {}
        for r in rows:
            districts.setdefault(r.pop("district"), []).append(r)
        for d, name, status in retirements(h):
            for mem in districts.get(d, []):
                if not mem.get("name"):
                    continue  # a vacant seat
                if not name or el.norm(name) == el.norm(mem["name"]) or el.last_name(name) == el.last_name(mem["name"]):
                    mem["statusText"], mem["plans"] = status, "leaving"
        ex, general = page_dates(h, y)
        d = ex.get(st, general)
        race = {
            "id": f"{y}-{st}-{'SD' if upper else 'HD'}", "year": y, "date": d.isoformat(), "office": "legislature",
            "chamber": "senate" if upper else "house", "officeName": chamber, "level": "state", "state": st,
            "layer": "sldu" if upper else "sldl", "seats": sum(len(v) for v in districts.values()), "districts": districts,
            "page": {"title": real, "url": WIKI + real.replace(" ", "_")}, "source": src,
        }
        if st == "LA" and d != general_day(y):
            race["dateNote"] = "Louisiana’s first round: if no one wins a majority, the top two meet in a runoff."
        out.append(race)
    return out


def local_pages(pages, local):
    """Dates, declared candidates and campaign sites from each mayoral race's own page."""
    pages.prefetch([r["page"]["title"] for r in local if r.get("page") and r["office"] == "mayor"])
    for r in local:
        if r["office"] != "mayor":
            continue
        if r.get("page") and pages.revs.get(r["page"]["title"]):
            h = pages.html(r["page"]["title"]) or ""
            real = pages.revs[r["page"]["title"]]["title"]
            url = WIKI + real.replace(" ", "_")
            if not real.startswith(str(r["year"])):
                # "2027 Madison mayoral election" redirects to "Mayoral elections in
                # Madison, Wisconsin": read only that year's section, never past races.
                sec = next((s for s in wt.split_sections(h) if str(r["year"]) in s["title"]), None)
                # Without its own heading, so lead_date reads the section as a lead.
                h = re.sub(r"<h2[\s>].*?</h2>", "", sec["html"], count=1, flags=re.S) if sec else ""
                url += f"#{sec['id']}" if sec else ""
            d = lead_date(h, r["year"]) if h else None
            r["date"] = d.isoformat() if d else None
            r["candidates"] = declared_people(h) if h else []
            attach_sites(r["candidates"], el.campaign_sites(h) if h else [])
            r["page"] = {"title": real, "url": url}
        h_ = r["holder"]
        for c in r["candidates"]:
            c["incumbent"] = bool(h_.get("name")) and ((c.get("wiki") and c.get("wiki") == h_.get("wiki")) or el.norm(c["name"]) == el.norm(h_["name"]))
        if h_.get("name") and r["plans"] == "running" and not any(c["incumbent"] for c in r["candidates"]):
            r["candidates"].insert(0, {k: v for k, v in h_.items() if v is not None} | {"incumbent": True})
        if any(c["incumbent"] for c in r["candidates"]):
            r["plans"], r["statusText"] = "running", "Running for another term"


NAV_RACES = {"governors": "governor", "lieutenant governors": "lieutenant-governor", "attorneys general": "attorney-general",
             "secretaries of state": "secretary-of-state", "state treasurers": "treasurer", "state auditors": "auditor",
             "u.s. senate": "senate"}


def own_article(pages, title):
    """Whether a race's page is an article of its own. Most of the navigation box's race
    links, and some of the tables', redirect to a page about many races: the national
    page, or the state's elections of the year ("2027 Kentucky Attorney General election"
    goes to "2027 Kentucky elections", whose declared lists are every office's)."""
    rev = pages.revs.get(title)
    return bool(rev) and (rev["title"] == title or not rev["title"].endswith(" elections"))


def nav_pages(pages, races, nav):
    """Each race's own article where the navigation box links one and the national table
    only points at its own section (Louisiana's 2027 governor's race)."""
    want = {}
    for r in races:
        if r.get("page") and "#" not in r["page"]["url"]:
            continue
        lines = [line for line, office in NAV_RACES.items() if office == r["office"]]
        t = next((t for line in lines for t, ok in (nav.get(r["year"]) or {}).get(line, [])
                  if ok and state_in(t) == r["state"] and ("special" in t.lower()) == bool(r["special"])), None)
        if t:
            want[r["id"]] = t
    pages.prefetch(list(want.values()))
    n = 0
    for r in races:
        t = want.get(r["id"])
        if t and own_article(pages, t):
            r["page"] = {"title": t, "url": WIKI + t.replace(" ", "_")}
            n += 1
    return n


def race_page_people(pages, races):
    """Declared candidates and campaign sites from the races' own pages. Someone the table
    already lists keeps their entry, gaining the article, experience or site the table
    lacked; someone it doesn't is added, with the party of the primary they are listed
    under. An officeholder the page lists as declared is running for another term. The
    President's page is the national page itself, so it only lends sites and details."""
    own = [r for r in races if r["office"] != "house" and r.get("page") and "#" not in r["page"]["url"]]
    pages.prefetch([r["page"]["title"] for r in own])
    own = [r for r in own if own_article(pages, r["page"]["title"])]
    added = sites = 0
    for r in own:
        h = pages.html(r["page"]["title"])
        if not h:
            continue
        cands, holder = r["candidates"], r.get("holder") or {}
        before = sum(1 for c in cands if c.get("site"))
        for p in declared_people(h):
            c = next((c for c in cands if p.get("wiki") and c.get("wiki") == p["wiki"]), None) \
                or el.match_candidate(p["name"], cands, p["party"] if p.get("party") in ("D", "R") else None)
            if c:
                for k in ("wiki", "experience", "site"):
                    if p.get(k) and not c.get(k):
                        c[k] = p[k]
                continue
            if r["office"] == "president":
                continue
            p["incumbent"] = bool(holder.get("name")) and (
                bool(p.get("wiki") and p["wiki"] == holder.get("wiki")) or el.norm(p["name"]) == el.norm(holder["name"]))
            if p["incumbent"] and not p.get("party"):
                p["party"] = holder.get("party")
            cands.append(p)
            added += 1
        if any(c.get("incumbent") for c in cands) and r.get("plans") in (None, "unknown"):
            r["plans"], r["statusText"] = "running", "Running for another term"
        attach_sites(cands, el.campaign_sites(h))
        sites += sum(1 for c in cands if c.get("site")) - before
    return added, sites


def everyone(*groups, legislatures=()):
    """Every person dict of the file, holders and candidates, for scripts/lib/people.py."""
    out = []
    for group in groups:
        for r in group:
            if r.get("holder") and r["holder"].get("name"):
                out.append(r["holder"])
            out += r.get("candidates") or []
    for ch in legislatures:
        for mems in ch["districts"].values():
            out += [m for m in mems if m.get("name")]
    return out


def other_races(races, more, local, legislatures):
    """Officeholders who have declared for another office the same year (Mississippi's
    agriculture commissioner for governor in 2027) get that as their plans, where the
    page about their own office doesn't say. Matched by article, or by name within the
    state."""
    groups = races + more + local
    where = {}
    for r in groups:
        for c in r.get("candidates") or []:
            if c.get("incumbent"):
                continue
            for k in ([("wiki", c["wiki"])] if c.get("wiki") else []) + [("name", r.get("state"), el.norm(c["name"]))]:
                where.setdefault((r["year"],) + k, []).append(r)

    def label(o):
        if o["office"] == "mayor":
            return f"Mayor of {o['place']}"
        if o["office"] == "county":
            return f"{o['county']} {o['officeName']}"
        return o["officeName"]  # "President", "Governor", "U.S. Senate", "State Treasurer"

    def find(y, st, p, own_id):
        hits = (where.get((y, "wiki", p["wiki"])) if p.get("wiki") else None) or where.get((y, "name", st, el.norm(p["name"]))) or []
        return next((o for o in hits if o["id"] != own_id), None)

    n = 0
    for r in groups:
        h = r.get("holder") or {}
        if not h.get("name") or r.get("plans") not in ("unknown", None) or r["office"] == "house":
            continue
        o = find(r["year"], r.get("state"), h, r["id"])
        if not o:
            continue
        r["statusText"] = f"Running for {label(o)}"
        # On one state's ballot a person runs for one office; a run for president can
        # sit beside a run for another term in some states, so it says nothing more.
        if o["office"] != "president" and o.get("state") == r.get("state"):
            r["plans"] = "leaving"
        n += 1
    for ch in legislatures:
        for mems in ch["districts"].values():
            for m in mems:
                if not m.get("name") or m.get("plans"):
                    continue
                o = find(ch["year"], ch["state"], m, ch["id"])
                if o and o.get("state") in (ch["state"], None):
                    m["statusText"] = f"Running for {label(o)}"
                    m["plans"] = "leaving" if o["office"] != "president" else None
                    if not m["plans"]:
                        m.pop("plans")
                    n += 1
    return n


def main():
    pages = Pages()
    titles = [tpl.format(y=y) for y in YEARS for _, _, tpl, _ in STATE_PAGES]
    titles += [SENATE.format(y=y) for y in YEARS if y % 2 == 0] + [PRESIDENT.format(y=y) for y in YEARS if y % 4 == 0]
    # Every year's "<year> United States elections": odd years' special Senate elections,
    # and every year's navigation box and mayors below.
    titles += [ELECTIONS.format(y=y) for y in YEARS]
    pages.prefetch(titles)
    races, read, checks = [], [], []
    for y in YEARS:
        if y % 4 == 0:
            p = president(pages, y)
            if p:
                races.append(p)
                read.append(PRESIDENT.format(y=y))
        if y % 2 == 0:
            n0 = len(races)
            races += [r | {"office": "senate", "officeName": "U.S. Senate"} for r in state_races(pages, y, "senate", "SEN", SENATE.format(y=y), "U.S. Senate")]
            if len(races) > n0:
                read.append(SENATE.format(y=y))
            races.append({
                "id": f"{y}-US-HOUSE", "year": y, "date": general_day(y).isoformat(), "office": "house",
                "officeName": "U.S. House", "state": None, "special": False, "holder": None,
                "statusText": "", "plans": None, "candidates": [], "seats": 435, "page": None, "source": None,
            })
        else:
            for t in special_titles(pages, y):
                pages.prefetch([t])
                r = special_race(pages, y, t)
                if r:
                    races.append(r)
                    read.append(t)
        for key, code, tpl, default in STATE_PAGES:
            title = tpl.format(y=y)
            got = state_races(pages, y, key, code, title, default)
            if got:
                races += got
                read.append(title)
            elif pages.revs.get(title):
                checks.append(f"{title}: no race summary table read")
    if not read:
        log("upcoming: no page could be read; keeping the previous file")
        return 1
    used_before = set(pages.used)

    def guarded(step, fn, default):
        # One reader failing (a page laid out differently) mustn't sink the rest.
        try:
            return fn()
        except Exception as e:  # noqa: BLE001
            checks.append(f"{step}: {type(e).__name__}: {e}")
            log(f"  {step} failed: {type(e).__name__}: {e}")
            return default

    nav = {y: navbox(pages, y) for y in YEARS if pages.revs.get(ELECTIONS.format(y=y))}
    races += guarded("offices without a national page", lambda: missing_offices(pages, nav, races, checks), [])
    more, local, legislatures = [], [], []
    for y, rows in nav.items():
        more += guarded(f"{y} statewide offices", lambda: state_page_offices(pages, y, rows, races, checks), [])
        local += guarded(f"{y} mayors", lambda: mayors(pages, y), [])
        local += guarded(f"{y} county offices", lambda: county_races(pages, y, rows), [])
        legislatures += guarded(f"{y} legislatures", lambda: legislature_races(pages, y, rows, checks), [])
    # Louisiana elects its legislature in the same open primary as its statewide offices
    # (the chamber pages say so), but their leads give the runoff's day (and, on Nov. 5,
    # 2026, called that Saturday a Tuesday): take the governor's race's first round.
    for ch in legislatures:
        gov = next((r for r in races if r["id"] == f"{ch['year']}-{ch['state']}-GOV" and r.get("dateNote")), None)
        if ch["state"] == "LA" and gov:
            ch["date"], ch["dateNote"] = gov["date"], gov["dateNote"]
    guarded("mayoral race pages", lambda: local_pages(pages, local), None)
    linked = guarded("race pages", lambda: nav_pages(pages, races, nav), 0)
    from_pages, sites = guarded("race pages' candidates", lambda: race_page_people(pages, races), (0, 0))
    moving = guarded("runs for another office", lambda: other_races(races, more, local, legislatures), 0)
    persons = everyone(races, more, local, legislatures=legislatures)
    people = guarded("people", lambda: P.enrich(persons, log)[0], None)
    if people is None:  # no checked website goes out unchecked
        people = {}
        for p in persons:
            p.pop("site", None)
    # Parties the lists leave out (mayors, the officeholders an article names), from
    # each person's Wikidata party where it gives exactly one; never for judges.
    judges = {id(p) for p in everyone([r for r in races + more + local if r["office"] in JUDICIAL])}
    for p in persons:
        if id(p) not in judges and not p.get("party") and (people.get(p.get("wiki")) or {}).get("party"):
            p["party"] = people[p["wiki"]]["party"]
    rank = {"president": 0, "senate": 1, "house": 2, "governor": 3, "lieutenant-governor": 4, "attorney-general": 5,
            "secretary-of-state": 6, "treasurer": 7, "auditor": 8}
    races.sort(key=lambda r: (r["date"][:4], r["date"], rank.get(r["office"], 9), el.STATE_NAME.get(r["state"] or "", ""), r["special"]))
    for group in (more, local):
        group.sort(key=lambda r: (r["year"], r["date"] or f"{r['year']}-99", el.STATE_NAME.get(r["state"], ""), r.get("place") or r.get("county") or "", r["officeName"]))
    legislatures.sort(key=lambda r: (r["year"], r["date"], el.STATE_NAME.get(r["state"], ""), r["chamber"] != "senate"))
    ids = [r["id"] for r in races + more + local + legislatures]
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        checks.append(f"duplicate ids: {', '.join(dupes)}")
    extra = [t for t in pages.used if t not in used_before and t not in read and pages.revs.get(t)]
    out = {
        "updated": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "years": list(YEARS),
        "races": races,
        "sources": [pages.source(t) | {"revid": pages.revs[t]["revid"]} for t in read],
        # Below the national pages (see the docstring); pages built before these keys
        # read only "races".
        "more": more,
        "local": local,
        "legislatures": legislatures,
        "people": people,
        "moreSources": [pages.source(t) | {"revid": pages.revs[t]["revid"]} for t in sorted(set(extra))],
        "checks": checks,
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    by_year = {y: sum(1 for r in races if r["year"] == y) for y in YEARS}
    declared = sum(len(r["candidates"]) for r in races + more + local)
    seats = sum(ch["seats"] for ch in legislatures)
    log(f"upcoming: {len(races)} races ({', '.join(f'{y}: {n}' for y, n in by_year.items())}), {len(more)} other statewide offices, "
        f"{sum(1 for r in local if r['office'] == 'mayor')} mayors, {sum(1 for r in local if r['office'] == 'county')} county offices, "
        f"{len(legislatures)} legislative chambers ({seats} seats), {declared} declared candidates ({from_pages} added from "
        f"race pages; {linked} race pages found through the navigation box), {sites} campaign sites from race pages, "
        f"{moving} officeholders running for another office, {len(people)} people with a bio, photo or website, "
        f"{len(read) + len(extra)} pages; wrote {OUT.relative_to(ROOT)}")
    for c in checks:
        log("  check:", c)
    return 0


if __name__ == "__main__":
    sys.exit(main())
