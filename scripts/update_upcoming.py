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
the summary tables (Wikipedia keeps potential candidates on the race pages, and parts of a
cell headed "Potential:" or "Declined:" are dropped), "TBD" meaning no one has declared.
Dates are each page's own ("October 9 (Louisiana)" overrides the general date for that
state), falling back to the first Tuesday after the first Monday in November.

No forecasts: nothing is rated this early, and the only polls test people who aren't
running. The 2026 runoffs still ahead come from the race data itself (the page reads
races.json), not from this file.

If none of the pages can be read, the previous file is kept.

    py scripts/update_upcoming.py
"""

import json
import re
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "lib"))
import elections as el  # noqa: E402
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

    def prefetch(self, titles):
        need = [t for t in titles if t not in self.revs]
        if need:
            self.revs.update(wt.revisions(need))

    def html(self, title):
        self.prefetch([title])
        rev = self.revs.get(title)
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


def page_dates(h, y):
    """The page's general date and per-state exceptions: ({state: date}, general date),
    read from the lead and its infobox only ("November 2, 2027 / October 9 (Louisiana)"),
    so primary dates further down never pass for an election day."""
    cut = re.search(r"<h2[\s>]", h)
    txt = page_text(h[:cut.start()] if cut else h)
    general = None
    m = re.search(r"(?:scheduled to be held|will be held|to be held)[^.]{0,80}?" + MONTH_RE + r" (\d{1,2}), " + str(y), txt)
    if m:
        general = date(y, el.MONTHS[m.group(1).lower()], int(m.group(2)))
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


def main():
    pages = Pages()
    titles = [tpl.format(y=y) for y in YEARS for _, _, tpl, _ in STATE_PAGES]
    titles += [SENATE.format(y=y) for y in YEARS if y % 2 == 0] + [PRESIDENT.format(y=y) for y in YEARS if y % 4 == 0]
    titles += [ELECTIONS.format(y=y) for y in YEARS if y % 2 == 1]
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
    rank = {"president": 0, "senate": 1, "house": 2, "governor": 3, "lieutenant-governor": 4, "attorney-general": 5,
            "secretary-of-state": 6, "treasurer": 7, "auditor": 8}
    races.sort(key=lambda r: (r["date"][:4], r["date"], rank.get(r["office"], 9), el.STATE_NAME.get(r["state"] or "", ""), r["special"]))
    ids = [r["id"] for r in races]
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        checks.append(f"duplicate ids: {', '.join(dupes)}")
    out = {
        "updated": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "years": list(YEARS),
        "races": races,
        "sources": [pages.source(t) | {"revid": pages.revs[t]["revid"]} for t in read],
        "checks": checks,
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    by_year = {y: sum(1 for r in races if r["year"] == y) for y in YEARS}
    declared = sum(len(r["candidates"]) for r in races)
    log(f"upcoming: {len(races)} races ({', '.join(f'{y}: {n}' for y, n in by_year.items())}), {declared} declared candidates, "
        f"{len(read)} pages; wrote {OUT.relative_to(ROOT)}")
    for c in checks:
        log("  check:", c)
    return 0


if __name__ == "__main__":
    sys.exit(main())
