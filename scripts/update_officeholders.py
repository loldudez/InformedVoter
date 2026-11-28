"""Build data/officeholders.json: who holds each statewide office and Senate seat now,
which caucus each member of Congress belongs to, and the senators' recorded positions.

The state pages and the Congress page put the 2026 winners together with the people
whose seats weren't on the ballot, so after the election every office shows who holds it
next: the winner where the race is called, otherwise the person in office. This file is
the second half.

Sources, read once a day by scripts/refresh_all.py (Wikipedia through the paced client in
scripts/lib/wikitables.py, cached by revision):
  * English Wikipedia's tables of current officeholders: "List of current United States
    governors", "List of current United States lieutenant governors", "State attorney
    general", "Secretary of state (U.S. state government)", "State treasurer" and "State
    auditor" (its elected officials only).
  * The caucuses' members (owner's request, Nov. 28, 2026: "double check the membership
    ... who is a part of what Caucus"): each caucus's own roster where it publishes one
    (scripts/lib/caucus_rosters.py: the Progressive Caucus, the New Democrat Coalition, the
    Blue Dog Coalition and the Main Street Caucus on their House sites, the Republican
    Governance Group through its PAC's member list), else its Wikipedia page's list (the
    Freedom Caucus and the Republican Study Committee, which publish none, and "List of
    Democratic Socialists of America public officeholders", only rows marked "member",
    never "former member"). Wikipedia's lists also give the members-elect, which no roster
    lists yet, and each member's article link. Every current member is matched to a sitting
    member's id (the House Clerk's, or a senator's Bioguide id) by last name and seat,
    state or first name, so the Congress page matches the sitting Congress exactly.
  * The senators sitting now (data/congress.json) and their recorded votes from Voteview
    (scripts/lib/senate_votes.py), turned into positions with the House votes' rules.
  * The governors' positions (owner's request, Nov. 27, 2026: "getting political positions
    for every governor that is currently in charge"): the recorded votes in Congress since
    2021 of those who served there (House roll calls by the Clerk's member id, Voteview's
    Senate roll calls), the bills they sponsored or cosponsored for questions no vote
    answers, then hand research on top: data/research/president-2028.json (Beshear) and
    data/research/governors-sitting.json (scripts/research/governors_sitting.py), which wins.
  * For each officeholder: the first two sentences of their Wikipedia article, their
    Wikidata photo and official website (scripts/lib/people.py).

A source that can't be read keeps its part of the previous file.

    py scripts/update_officeholders.py
    py scripts/update_officeholders.py --governors   # only the governors' positions, on the last build
    py scripts/update_officeholders.py --caucuses    # only the caucus lists, on the last build
"""

import json
import re
import sys
import traceback
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "lib"))
import wikitables as W  # noqa: E402
import people as P  # noqa: E402
import senate_votes as SV  # noqa: E402
import house_votes  # noqa: E402
import cosponsors  # noqa: E402
import caucus_rosters as CR  # noqa: E402
from elections import STATE_ABBR, party_code  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
OUT = ROOT / "data" / "officeholders.json"
WIKI = "https://en.wikipedia.org/wiki/"
NOW = datetime.now(timezone.utc)

OFFICE_PAGES = {
    "GOV": "List of current United States governors",
    "LG": "List of current United States lieutenant governors",
    "AG": "State attorney general",
    "SOS": "Secretary of state (U.S. state government)",
    "TREAS": "State treasurer",
    "AUD": "State auditor",
}

# The caucuses shown on the Congress page, in the order a member is placed: each member
# goes in the first one they belong to (the owner's choice, Nov. 25, 2026).
CAUCUSES = [
    {"id": "dsa", "party": "D", "name": "Democratic Socialists of America", "short": "DSA",
     "page": "List of Democratic Socialists of America public officeholders"},
    {"id": "cpc", "party": "D", "name": "Congressional Progressive Caucus", "short": "Progressive Caucus",
     "page": "Congressional Progressive Caucus"},
    {"id": "bluedog", "party": "D", "name": "Blue Dog Coalition", "short": "Blue Dogs", "page": "Blue Dog Coalition"},
    {"id": "newdem", "party": "D", "name": "New Democrat Coalition", "short": "New Democrats", "page": "New Democrat Coalition"},
    {"id": "freedom", "party": "R", "name": "Freedom Caucus", "short": "Freedom Caucus", "page": "Freedom Caucus"},
    {"id": "mainstreet", "party": "R", "name": "Main Street Caucus", "short": "Main Street", "page": "Main Street Caucus"},
    {"id": "governance", "party": "R", "name": "Republican Governance Group", "short": "Governance Group",
     "page": "Republican Governance Group"},
    {"id": "rsc", "party": "R", "name": "Republican Study Committee", "short": "Study Committee", "page": "Republican Study Committee"},
]


def log(*a):
    print(*a, flush=True)


def wiki_url(href):
    """A full article link for a table cell's href, or None for red links and files."""
    if not href or not href.startswith("/wiki/") or href.startswith(("/wiki/File:", "/wiki/Help:", "/wiki/Special:")):
        return None
    return WIKI + href[len("/wiki/"):].split("#")[0]


def person_link(cell):
    for l in cell.get("links") or []:
        u = wiki_url(l.get("href"))
        if u and not re.search(r"Party|Independent_politician|_\(list\)|List_of", u.split("/wiki/")[-1]):
            return u
    return None


def iso_day(s):
    """"April 10, 2017" as 2017-04-10, "January 2011" as 2011-01, "2011" as 2011."""
    s = re.sub(r"\s+", " ", re.sub(r"\[\d+\]", "", s or "")).strip()
    for fmt, n in (("%B %d, %Y", 10), ("%B %Y", 7), ("%Y", 4)):
        try:
            return datetime.strptime(s, fmt).date().isoformat()[:n]
        except ValueError:
            continue
    return None


def state_of(cell):
    t = re.sub(r"\s*\(list\)\s*$", "", W.text(cell)).strip()
    return STATE_ABBR.get(t)


def party_of(*cells):
    for c in cells:
        t = W.text(c).strip()
        if t:
            p = party_code(t)
            return {"Nonpartisan": "N", "Unknown": None}.get(t, p if p in ("D", "R", "L", "G", "I") else t)
    return None


_REVS = {}


def page(title):
    if title not in _REVS:  # one request for every page's latest revision
        _REVS.update(W.revisions(list(OFFICE_PAGES.values()) + [c["page"] for c in CAUCUSES] + [title]))
    rev = _REVS.get(title)
    if not rev:
        raise ValueError(f"Wikipedia has no page {title!r}")
    return W.page_at(rev["title"], rev), {"title": f"Wikipedia: {rev['title']}", "url": WIKI + rev["title"].replace(" ", "_"),
                                          "asOf": rev.get("timestamp"), "revid": rev.get("revid")}


def header_index(row):
    heads = []
    for c in row:
        heads.append(re.sub(r"\s+", " ", W.text(c)).strip().lower())
    return heads


def find_table(html_text, *must):
    for t in W.tables(html_text):
        heads = header_index(t["rows"][0])
        if all(any(h.startswith(m) for h in heads) for m in must):
            return t, heads
    return None, None


def cols(heads, name):
    return [i for i, h in enumerate(heads) if h.startswith(name)]


def clean(name):
    name = re.sub(r"\[\d+\]", "", name)
    acting = bool(re.search(r"\bacting\b|\binterim\b", name, re.I))
    name = re.split(r"\s+/\s+|\n", name)[0]
    name = re.sub(r"\s*\((acting|interim)\)\s*", " ", name, flags=re.I)
    return re.sub(r"\s+", " ", name).strip(" *†‡"), acting


# Statewide offices -----------------------------------------------------------------------

def read_office(key, html_text):
    """{state: holder} (or a list for auditors) from one office's table."""
    out = {}
    if key == "GOV":
        t, heads = find_table(html_text, "state", "governor", "party", "term start")
        c_name, c_state = cols(heads, "governor")[0], cols(heads, "state")[0]
    elif key == "LG":
        t, heads = find_table(html_text, "state", "name", "party", "term start")
        c_name, c_state = cols(heads, "name")[0], cols(heads, "state")[0]
    elif key in ("AG", "SOS", "TREAS"):
        t, heads = find_table(html_text, "name", "state", "party", "start")
        c_name, c_state = cols(heads, "name")[0], cols(heads, "state")[0]
    else:  # AUD: the table of auditors elected by the voters
        t, heads = find_table(html_text, "incumbent", "state", "party", "assumed office", "title", "mode of election")
        c_name, c_state = cols(heads, "incumbent")[0], cols(heads, "state")[0]
    if not t:
        raise ValueError(f"{key}: the officeholders' table wasn't found")
    c_party = cols(heads, "party")
    c_start = (cols(heads, "term start") or cols(heads, "start") or cols(heads, "assumed office"))[0]
    c_end = (cols(heads, "term end") or [None])[0]
    c_title = (cols(heads, "title") or [None])[0]
    # How the holder got the office ("Elected", "Ticket", "Appointed"; the lieutenant governors'
    # "Selection"); the auditors' "Type of state auditor" is something else.
    c_type = next((i for i, h in enumerate(heads) if h in ("type", "selection") or h.startswith("mode of election")), None)
    c_prior = (cols(heads, "prior public experience") or [None])[0]
    for row in t["rows"][1:]:
        if len(row) <= max(c_name, c_state):
            continue
        st = state_of(row[c_state])
        if not st:
            continue
        name, acting = clean(W.text(row[c_name]))
        if not name or name.lower() in ("vacant", "none"):
            continue
        h = {"name": name, "party": party_of(*[row[i] for i in c_party if i < len(row)])}
        link = person_link(row[c_name])
        if link:
            h["wiki"] = link
        since = iso_day(W.text(row[c_start])) if c_start < len(row) else None
        if since:
            h["since"] = since
        if acting:
            h["acting"] = True
        if c_end is not None and c_end < len(row):
            end = W.text(row[c_end]).strip()
            if re.search(r"appointed", end, re.I):
                h["appointed"] = True
            elif (m := re.search(r"\b(20\d\d)\b", end)):
                h["termEnd"] = int(m.group(1))
                if re.search(r"term.limit", end, re.I):
                    h["termLimited"] = True
        if c_title is not None and c_title < len(row):
            title = W.text(row[c_title]).strip()
            if title:
                h["title"] = re.sub(r"\[\d+\]", "", title)
        if c_type is not None and c_type < len(row):
            how = re.sub(r"\[\d+\]", "", W.text(row[c_type])).strip()
            if re.search(r"appoint", how, re.I):
                h["appointed"] = True
            if re.search(r"ticket", how, re.I):
                h["ticket"] = True
            if key == "LG" and how:
                h["selection"] = how.split(";")[0].split(" / ")[0].strip()
        if c_prior is not None and c_prior < len(row):
            prior = re.sub(r"\[\d+\]", "", W.text(row[c_prior])).replace("\n", "; ").strip()
            if prior:
                h["prior"] = prior
        if key == "AUD":
            out.setdefault(st, []).append(h)
        else:
            out.setdefault(st, h)
    return out


# Caucuses ----------------------------------------------------------------------------------

SEAT = re.compile(r"\b([A-Z]{2})-(\d{1,2}|AL)\b")


def seat_code(s):
    """"AZ-3", "AZ-03" or "AK-AL" as the site's district code ("AZ-03", "AK-00")."""
    m = SEAT.search(s or "")
    if not m:
        return None
    st, d = m.groups()
    return f"{st}-00" if d == "AL" else f"{st}-{int(d):02d}"


ELECT = re.compile(r"(representative|member|senator)[- ]elect", re.I)


def caucus_rows(cid, html_text):
    """[{"n", "wiki", "seat", "elect"}] for one caucus page's current members and members-elect
    (whose "seat" is the district they were elected in, not one they hold yet)."""
    out = []

    def add(name, cell_link, seat, elect):
        e = {"n": re.sub(r"\s+", " ", re.sub(r"\[\d+\]|[*†‡]", "", name)).strip()}
        if cell_link:
            e["wiki"] = cell_link
        if seat:
            e["seat"] = seat
        if elect:
            e["elect"] = True
        out.append(e)
    if cid == "dsa":
        for s in W.split_sections(html_text):
            if s["level"] != 3 or s["title"] != "United States House of Representatives":
                continue
            for sub in W.split_sections(s["html"]):
                if sub["level"] != 4 or not re.match(r"(Current|Elected, not yet sworn in)", sub["title"]):
                    continue
                elect = sub["title"].startswith("Elected")
                for t in W.tables(sub["html"]):
                    heads = header_index(t["rows"][0])
                    c_name, c_dist, c_note = heads.index("name"), heads.index("district"), heads.index("notes")
                    for row in t["rows"][1:]:
                        note = W.text(row[c_note]).strip().lower()
                        if not note.startswith("member"):
                            continue  # "former member", "expelled former member"
                        # A member who has held several districts lists them oldest first.
                        add(W.text(row[c_name]), person_link(row[c_name]), seat_code(W.text(row[c_dist]).split(",")[-1]), elect)
        return out
    # The member tables: State | District | CPVI | Member | (Also a member of) | Notes.
    for t in W.tables(html_text):
        heads = header_index(t["rows"][0])
        if "member" in heads and "district" in heads and "cpvi" in heads:
            c_mem, c_dist = heads.index("member"), heads.index("district")
            c_note = heads.index("notes") if "notes" in heads else None
            for row in t["rows"][1:]:
                note = W.text(row[c_note]).strip() if c_note is not None and c_note < len(row) else ""
                add(W.text(row[c_mem]), person_link(row[c_mem]), seat_code(W.text(row[c_dist])), bool(ELECT.search(note)))
    if out:
        return out
    # The list pages: "Barry Moore (AL-1)*" under "Current members".
    sec = W.section_by_title(html_text, "Current members", "Members")
    if sec:
        for li in re.findall(r"<li[^>]*>(.*?)</li>", sec, re.S):
            txt = re.sub(r"<[^>]+>", "", li)
            # The member is the first link that isn't a state or territory (a list can open
            # with a heading line, "American Samoa", inside its first item).
            for href, label in re.findall(r'<a[^>]*href="/wiki/([^"#]+)"[^>]*>(.*?)</a>', li, re.S):
                title = unquote(href).replace("_", " ")
                if re.match(r"(File|Help|Special|Template):", href) or title in STATE_ABBR or title in TERRITORIES:
                    continue
                add(re.sub(r"<[^>]+>", "", label), WIKI + href, seat_code(txt), bool(ELECT.search(txt)))
                break
    return out


TERRITORIES = {"American Samoa", "Guam", "Puerto Rico", "Northern Mariana Islands", "United States Virgin Islands",
               "U.S. Virgin Islands", "Washington, D.C.", "District of Columbia"}


def senate_caucus_rows(cid, html_text):
    """Senators a caucus page lists (the Progressive Caucus has a Senate table)."""
    out = []
    for t in W.tables(html_text):
        heads = header_index(t["rows"][0])
        if "member" in heads and "state" in heads and "district" not in heads:
            c_mem, c_st = heads.index("member"), heads.index("state")
            for row in t["rows"][1:]:
                e = {"n": W.text(row[c_mem]).strip()}
                link = person_link(row[c_mem])
                if link:
                    e["wiki"] = link
                st = STATE_ABBR.get(W.text(row[c_st]).strip())
                if st:
                    e["st"] = st
                out.append(e)
    return out


def _fold(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s or "") if not unicodedata.combining(c)).lower()


def last_of(name):
    """lastNameOf in js/data/holders.js: the last word, without a parenthesis or Jr./Sr./II-IV."""
    parts = re.sub(r"\(.*?\)|,? (jr|sr|ii|iii|iv)\.?$", "", _fold(name)).split()
    return parts[-1] if parts else ""


def firsts_of(name):
    """Every word before the last name, nicknames included: the Clerk lists Buddy Carter as
    'Earl L. "Buddy" Carter' (firstNames in js/views/congress.js does the same)."""
    parts = re.sub(r"\(.*?\)|,? (jr|sr|ii|iii|iv)\.?$", " ", _fold(name)).split()[:-1]
    return [w for w in (re.sub(r"[^a-z-]", "", p) for p in parts) if len(w) > 1]


def sitting_members(congress, chamber):
    """Who a caucus list can name now: the House's members with their seats ("AZ-03",
    "AK-00") and its delegates (who have no member id here), or the senators."""
    c = congress["chambers"][chamber]
    out = []
    for m in c["members"] + ((c.get("delegates") or []) if chamber == "house" else []):
        x = {"n": m["n"], "party": m.get("party"), "st": m["st"], "id": m.get("id")}
        if chamber == "house":
            x["seat"] = f"{m['st']}-{int(m.get('d') or 0):02d}"
        out.append(x)
    return out


def member_of(e, members, party):
    """The one sitting member a list's entry names: the same last name, in the caucus's party
    or an independent, then the same seat, else the same state, else (a list without
    districts) the same first name. None when no one, or more than one, fits: Wikipedia's
    lists give some members the districts of the 2026 maps (Utah's), and seats change hands
    (GA-13, NJ-11), so a seat alone never decides."""
    last = last_of(e["n"])
    same = [m for m in members if last_of(m["n"]) == last and (m["party"] == party or m["party"] not in ("D", "R"))]
    if e.get("seat"):
        hit = [m for m in same if m.get("seat") == e["seat"]]
        if len(hit) == 1:
            return hit[0]
    st = e.get("st") or (e.get("seat") or "")[:2]
    if st:
        same = [m for m in same if m["st"] == st]
    if len(same) > 1:
        mine = firsts_of(e["n"])
        same = [m for m in same if any(a[:3] == b[:3] for a in firsts_of(m["n"]) for b in mine)]
    return same[0] if len(same) == 1 else None


def with_ids(entries, members, party, unmatched):
    """Each current entry's member id, so the Congress page matches sitting members exactly
    (and a list without districts gets the member's seat); members-elect have no id yet."""
    for e in entries:
        if e.get("elect"):
            continue
        m = member_of(e, members, party)
        if m and m.get("id"):
            e["id"] = m["id"]
            if not e.get("seat") and m.get("seat"):
                e["seat"] = m["seat"]
        elif not m:
            unmatched.append(e["n"] + (f" ({e['seat']})" if e.get("seat") else ""))


def from_roster(d, roster, house_members, senate_members):
    """A caucus's current members from its own roster, each with the article link Wikipedia's
    list gives the same person, plus Wikipedia's members-elect, which no roster lists yet."""
    party = d["party"]

    def by_member(entries, members):
        out = {}
        for e in entries:
            m = None if e.get("elect") else member_of(e, members, party)
            if m and m.get("id"):
                out.setdefault(m["id"], e)
        return out

    def linked(entries, wiki_entries, members):
        listed = by_member(wiki_entries, members)
        out = []
        for r in entries:
            e = dict(r)
            m = member_of(e, members, party)
            w = listed.get(m["id"]) if m and m.get("id") else None
            if w and w.get("wiki"):
                e["wiki"] = w["wiki"]
            out.append(e)
        return out

    wiki_ids, roster_ids = by_member(d["house"], house_members), by_member(roster["house"], house_members)
    out = d | {"house": linked(roster["house"], d["house"], house_members) + [e for e in d["house"] if e.get("elect")],
               "source": roster["source"], "listSource": d["source"], "fromRoster": True}
    if roster["senate"]:
        out["senate"] = linked(roster["senate"], d.get("senate") or [], senate_members)
    left_out = [e["n"] for i, e in wiki_ids.items() if i not in roster_ids]
    added = [e["n"] for i, e in roster_ids.items() if i not in wiki_ids]
    log(f"caucus {d['short']}: its roster lists {len(roster['house'])} House members"
        + (f"; Wikipedia's list also names {', '.join(left_out)} (left out)" if left_out else "")
        + (f"; only the roster names {', '.join(added)}" if added else ""))
    return out


def build_caucuses(old, congress, problems):
    """Each caucus's members: its own roster where it publishes one, else its Wikipedia list,
    with the members-elect Wikipedia lists and every sitting member's id."""
    house_members, senate_members = sitting_members(congress, "house"), sitting_members(congress, "senate")
    prev_defs = {d["id"]: d for d in (old.get("caucuses") or {}).get("defs", [])}
    defs = []
    for c in CAUCUSES:
        prev = prev_defs.get(c["id"])
        try:
            html_text, src = page(c["page"])
            house = caucus_rows(c["id"], html_text)
            if not house:
                raise ValueError("no members found")
            senate = senate_caucus_rows(c["id"], html_text)
        except Exception as e:  # noqa: BLE001
            problems.append(f"caucus {c['short']}: {e}; kept the last build's")
            log(problems[-1])
            if prev:
                defs.append(prev)
            continue
        d = {k: c[k] for k in ("id", "party", "name", "short")} | {"source": src, "house": house}
        if senate:
            d["senate"] = senate
        if c["id"] in CR.ROSTERS:
            try:
                d = from_roster(d, CR.read(c["id"]), house_members, senate_members)
            except Exception as e:  # noqa: BLE001
                why = f"caucus {c['short']}: its own roster ({CR.ROSTERS[c['id']][0]}): {e}"
                if prev and prev.get("fromRoster"):
                    # The last roster read beats Wikipedia's list; the members-elect are today's.
                    d = prev | {"house": [x for x in prev["house"] if not x.get("elect")] + [x for x in house if x.get("elect")]}
                    problems.append(why + "; kept the last roster read")
                else:
                    problems.append(why + "; used Wikipedia's list")
                log(problems[-1])
        unmatched = []
        with_ids(d["house"], house_members, d["party"], unmatched)
        if d.get("senate"):
            with_ids(d["senate"], senate_members, d["party"], unmatched)
        defs.append(d)
        log(f"caucus {c['short']}: {sum(1 for e in d['house'] if not e.get('elect'))} House members "
            f"({'its roster' if d.get('fromRoster') else 'Wikipedia'}), {sum(1 for e in d['house'] if e.get('elect'))} elected, not sworn in"
            + (f", {len(d['senate'])} senators" if d.get("senate") else "")
            + (f"; matched to no sitting member: {', '.join(unmatched)}" if unmatched else ""))
    return {"order": [c["id"] for c in CAUCUSES], "defs": defs}


def caucuses_only():
    """Only the caucus lists, on the last build (`--caucuses`)."""
    data = json.loads(OUT.read_text(encoding="utf-8"))
    congress = json.loads((ROOT / "data" / "congress.json").read_text(encoding="utf-8"))
    problems = []
    data["caucuses"] = build_caucuses(data, congress, problems)
    data["checks"] = [c for c in data.get("checks", []) if c.get("id") != "caucuses"] + \
        [{"id": "caucuses", "ok": not problems, "detail": "; ".join(problems) or "every caucus list read"}]
    OUT.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    log(f"caucuses: wrote {OUT.relative_to(ROOT)}" + (f"; problems: {'; '.join(problems)}" if problems else ""))


# Senators ------------------------------------------------------------------------------------

def senators(record, congress, bills=None):
    out = []
    for m in congress["chambers"]["senate"]["members"]:
        wiki = WIKI + m["article"].replace(" ", "_") if m.get("article") else None
        s = {"name": m["n"], "party": m["party"], "st": m["st"], "cls": m.get("cls"), "up": m.get("up"), "since": m.get("since")}
        if wiki:
            s["wiki"] = wiki
        icpsr = record.find(m["st"], m["n"]) if record else None
        if icpsr:
            vm = record.members.get(icpsr) or {}
            if vm.get("bioguide_id"):
                s["bioguide"] = vm["bioguide_id"]
            votes = record.votes_of(icpsr)
            s["votesCast"] = len(votes)
            pos = {}
            for q, stance, src, quote in SV.vote_positions(record, m["n"], votes):
                pos[q] = {"stance": stance, "source": src}
            # Questions no vote answers, from the bills they sponsored or cosponsored.
            for q, p in (bills.positions(s["bioguide"], m["n"]) if bills and s.get("bioguide") else {}).items():
                pos.setdefault(q, p)
            if pos:
                s["positions"] = pos
        out.append(s)
    return out


# Governors' positions --------------------------------------------------------------------------

GOV_RESEARCH = [ROOT / "data" / "research" / "president-2028.json",    # Beshear's 2028 research
                ROOT / "data" / "research" / "governors-sitting.json"]  # wins where both answer
SUFFIX = re.compile(r"\s+(Jr\.?|Sr\.?|II|III|IV)$")


def governors(gov_rows, record, bills, problems):
    """Positions for each governor in office (the state pages show them where the seat wasn't
    up in 2026): recorded votes in Congress since 2021, looked up only for those whose prior
    offices include the U.S. House or Senate, then the bills they sponsored or cosponsored
    for questions no vote answers, then hand research on top. Returns how many have any."""
    research = {}
    for path in GOV_RESEARCH:
        try:
            for wiki, p in json.loads(path.read_text(encoding="utf-8")).get("people", {}).items():
                research.setdefault(wiki, {}).update(p.get("positions") or {})
        except (OSError, ValueError) as e:
            problems.append(f"governors' research {path.name}: {e}")
    house = None
    if any("U.S. House" in (h.get("prior") or "") for h in gov_rows.values()):
        try:
            house = house_votes.HouseRecord()
        except Exception as e:  # noqa: BLE001
            problems.append(f"House roll calls unavailable for governors: {e}")
    n = 0
    for st, h in gov_rows.items():
        for k in ("positions", "positionsFrom", "votesCast", "bioguide"):
            h.pop(k, None)
        prior = h.get("prior") or ""
        surname = SUFFIX.sub("", h["name"]).split()[-1]
        pos, cast, bg = {}, 0, None
        if house and "U.S. House" in prior:
            mid = house.member_id(st, h["name"], h.get("party"))
            v = house.votes_for(mid) if mid else None
            if v:
                bg = mid
                for q, stance, src, _ in house_votes.vote_positions(surname, v):
                    pos[q] = {"stance": stance, "source": src}
                cast += len(v)
        if record and "U.S. Senate" in prior:
            icpsr = record.find(st, h["name"])
            v = record.votes_of(icpsr) if icpsr else {}
            if v:
                bg = bg or (record.members.get(icpsr) or {}).get("bioguide_id")
                for q, stance, src, _ in SV.vote_positions(record, h["name"], v):
                    pos[q] = {"stance": stance, "source": src}
                cast += len(v)
        if bg and bills:
            for q, b in bills.positions(bg, surname).items():
                pos.setdefault(q, b)
        mine = research.get(h.get("wiki") or "") or {}
        if pos or mine:
            h["positions"] = {**pos, **mine}
            h["positionsFrom"] = "research+votes" if pos and mine else "research" if mine else "votes"
            n += 1
        if cast:
            h["votesCast"] = cast
        if bg:
            h["bioguide"] = bg
    return n


def governors_only():
    """Lay the governors' positions over the last build, without reading Wikipedia."""
    data = json.loads(OUT.read_text(encoding="utf-8"))
    problems = []
    try:
        record = SV.SenateRecord()
        problems += record.problems
    except Exception as e:  # noqa: BLE001
        record = None
        problems.append(f"Senate votes: {e}")
    try:
        bills = cosponsors.Cosponsors()
    except Exception as e:  # noqa: BLE001
        bills = None
        problems.append(f"Bill cosponsors unavailable: {e}")
    n = governors(data["offices"]["GOV"], record, bills, problems)
    OUT.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    log(f"governors: {n} of {len(data['offices']['GOV'])} with positions; wrote {OUT.relative_to(ROOT)}"
        + (f"; problems: {'; '.join(problems)}" if problems else ""))


# Build ---------------------------------------------------------------------------------------

def main():
    if "--governors" in sys.argv[1:]:
        return governors_only()
    if "--caucuses" in sys.argv[1:]:
        return caucuses_only()
    try:
        old = json.loads(OUT.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        old = {}
    data = {"updated": NOW.strftime("%Y-%m-%dT%H:%M:%SZ"), "sources": {}, "checks": []}
    problems = []

    # Statewide offices.
    offices = {}
    for key, title in OFFICE_PAGES.items():
        try:
            html_text, src = page(title)
            got = read_office(key, html_text)
            if len(got) < 30:
                raise ValueError(f"only {len(got)} states read")
            offices[key] = got
            data["sources"][key] = src
            log(f"{key}: {len(got)} states from {title}")
        except Exception as e:  # noqa: BLE001
            problems.append(f"{key}: {e}; kept the last build's")
            log(problems[-1])
            if old.get("offices", {}).get(key):
                offices[key] = old["offices"][key]
                data["sources"][key] = old.get("sources", {}).get(key)
    data["offices"] = offices

    # Caucuses: each one's own roster where it publishes one, else its Wikipedia list.
    congress = json.loads((ROOT / "data" / "congress.json").read_text(encoding="utf-8"))
    data["caucuses"] = build_caucuses(old, congress, problems)

    # Senators and their votes.
    try:
        record = SV.SenateRecord()
        problems += record.problems
        try:
            bills = cosponsors.Cosponsors()
            problems += [f"Bill cosponsors: {x}" for x in bills.problems]
        except Exception as e:  # noqa: BLE001  the votes still count without them
            bills = None
            problems.append(f"Bill cosponsors unavailable: {e}")
        data["senators"] = senators(record, congress, bills)
        if bills:
            data["sources"]["bills"] = {"title": "Library of Congress bill status files on govinfo.gov: sponsors and cosponsors",
                                        "url": "https://www.govinfo.gov/bulkdata/BILLSTATUS", "asOf": NOW.strftime("%Y-%m-%d")}
        data["sources"]["votes"] = {"title": "Voteview: Congressional Roll-Call Votes Database (Lewis, Poole, Rosenthal, Boche, Rudkin and Sonnet)",
                                    "url": "https://voteview.com/", "asOf": NOW.strftime("%Y-%m-%d")}
        withpos = sum(1 for s in data["senators"] if s.get("positions"))
        log(f"senators: {len(data['senators'])}, {withpos} with positions from votes")
    except Exception as e:  # noqa: BLE001
        traceback.print_exc()
        problems.append(f"Senate votes: {e}; kept the last build's")
        data["senators"] = old.get("senators") or senators(None, congress)
        record = bills = None

    # Governors' positions: votes, bills, then hand research.
    if offices.get("GOV"):
        n = governors(offices["GOV"], record, bills, problems)
        log(f"governors: {n} of {len(offices['GOV'])} with positions")

    # Who they are: bios, photos, websites.
    persons, seen = [], set()
    for key, by_state in offices.items():
        for st, h in by_state.items():
            for p in (h if isinstance(h, list) else [h]):
                if p.get("wiki") and p["wiki"] not in seen:
                    seen.add(p["wiki"]); persons.append({"name": p["name"], "wiki": p["wiki"]})
    for s in data["senators"]:
        if s.get("wiki") and s["wiki"] not in seen:
            seen.add(s["wiki"]); persons.append({"name": s["name"], "wiki": s["wiki"]})
    try:
        people, stats = P.enrich(persons, log=log)
        data["people"] = people
    except Exception as e:  # noqa: BLE001
        traceback.print_exc()
        problems.append(f"bios and photos: {e}; kept the last build's")
        data["people"] = old.get("people") or {}

    data["checks"] = [{"id": "officeholders", "ok": not problems, "detail": "; ".join(problems) or "every source read"}]
    OUT.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    log(f"wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size // 1024} KB)" + (f"; problems: {len(problems)}" if problems else ""))
    for p in problems:
        log("  ", p)


if __name__ == "__main__":
    main()
