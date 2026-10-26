"""2026 state legislative races from Wikipedia's chamber election pages (used as an
aggregator, CC BY-SA), one page per chamber, such as "2026 Michigan House of
Representatives election".

What a page gives, where its editors have filled it in:
- the district summary table: each seat on the ballot, who holds it and their
  party, and usually the district's 2024 presidential margin;
- the November candidates: a general-election box in the district's section, a
  "Candidates" column, a combined candidate table (Pennsylvania), or each party's
  "Nominee" list;
- for some chambers, forecasters' district ratings (State Navigate, Capitol Inside,
  Marquette).

These races get no win probabilities. Almost none have public polls and few are
rated, so a forecast would invent precision; like Louisiana's open primaries they
show the field, the seat's holder, the 2024 presidential margin and any ratings
(format "field"). A chamber whose page lists no districts stays in the demo set.

    py scripts/lib/legislature.py MI WI      (prints what it finds for those states)
"""

import json
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import elections as el  # noqa: E402
import model  # noqa: E402
import wikitables as W  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
WIKI = "https://en.wikipedia.org/wiki/"
SKIP_WORDS = {"state", "house", "senate", "senatorial", "legislative", "assembly", "delegate", "district", "subdistrict",
              "and", "the", "of", "representatives", "representative"}
# Wikipedia's party colors on the "▌" markers some candidate lists use instead of names.
MARK_COLORS = {"#0044c9": "D", "#3333ff": "D", "#e81b23": "R", "#ff3333": "R", "#fed105": "L", "#fed000": "L",
               "#17aa5c": "G", "#00a95c": "G", "#0bda51": "G", "#a356de": "Constitution", "#dcdcdc": "I"}
NOT_ON_BALLOT = re.compile(r"Eliminated|Withdr[ae]w|Disqualified|Lost |Defeated in|Declined|primary:|Primary results|runoff", re.I)


def chambers():
    """Every chamber that elects in 2026, from js/data/states.js (the site's own list)."""
    names = {"SENATE": "State Senate", "HOUSE": "State House", "ASSEMBLY": "State Assembly", "DELEGATES": "House of Delegates"}
    out = []
    ch_re = re.compile(r"ch\((\w+|'[^']+'), (\d+), (\d), '(\w+)'(?:, '(\w+)')?\)")
    for line in (ROOT / "js" / "data" / "states.js").read_text(encoding="utf-8").splitlines():
        m = re.match(r"\s*S\('([A-Z]{2})', '\d\d', '([^']+)'", line)
        if not m:
            continue
        st, name = m.groups()
        unicameral = "unicameral: true" in line
        for i, cm in enumerate(ch_re.finditer(line)):
            if cm.group(4) == "none":
                continue
            label = names.get(cm.group(1), cm.group(1).strip("'"))
            upper = i == 0
            key = "leg" if unicameral else "senate" if upper else "house"
            out.append({"state": st, "name": name, "key": key, "layer": "sldu" if upper else "sldl", "label": label,
                        "seats": int(cm.group(2)), "up": cm.group(4),
                        "prefix": {"leg": "LEG", "senate": "SS", "house": "SH"}[key],
                        "office": {"leg": "legislature", "senate": "state-senate", "house": "state-house"}[key]})
    return out


def titles_for(ch):
    n = ch["name"]
    if ch["key"] == "leg":
        return [f"2026 {n} Legislature election"]
    if ch["key"] == "senate":
        return [f"2026 {n} Senate election", f"2026 {n} State Senate election"]
    return [f"2026 {n} House of Representatives election", f"2026 {n} State Assembly election", f"2026 {n} Assembly election",
            f"2026 {n} House of Delegates election"]


# District names ------------------------------------------------------------------

def _ascii(s):
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()


ORDINALS = {"first": "1st", "second": "2nd", "third": "3rd", "fourth": "4th", "fifth": "5th", "sixth": "6th",
            "seventh": "7th", "eighth": "8th", "ninth": "9th", "tenth": "10th"}


def clean_label(s):
    """'41st (special)', '3rd (sp)', '6th sp' -> the district alone."""
    return re.sub(r"\s*\((?:special|sp\.?)\)|\s+sp\.?$", "", s.strip(), flags=re.I)


def text_key(s):
    t = _ascii(s).lower()
    t = re.sub(r"\b(" + "|".join(ORDINALS) + r")\b", lambda m: ORDINALS[m.group(1)], t)
    t = re.sub(r"\(house\)", " ", t)
    t = re.sub(r"[^a-z0-9]+", " ", t)
    t = re.sub(r"\b0+(\d)", r"\1", t)
    return "t:" + " ".join(w for w in t.split() if w not in SKIP_WORDS)


def num_key(s):
    """'1st', 'District 1', '001', '01A', '1A', 'A' -> 'n:1', 'n:1A', 'n:A'; None otherwise."""
    t = _ascii(s).strip()
    m = re.fullmatch(r"(?:(?:State\s+)?(?:Senate|House|Assembly)?\s*District\s*)?0*(\d+)(?:st|nd|rd|th)?\s*(?:District)?\s*-?\s*([A-Za-z])?", t, re.I)
    if m:
        return f"n:{int(m.group(1))}{(m.group(2) or '').upper()}"
    m = re.fullmatch(r"(?:District\s*)?0*([A-Za-z])", t, re.I)
    return f"n:{m.group(1).upper()}" if m else None


def feature_index(features):
    idx = {}
    for f in features:
        fid, name = f["id"], f["properties"].get("n", "")
        keys = {text_key(name)}
        k = num_key(fid) if re.fullmatch(r"0*\d+[A-Z]?|0*[A-Z]", fid) else None
        if k:
            keys.add(k)
        k2 = num_key(re.sub(r"(?i)\b(state|house|senate|legislative|delegate|sub)?district\b", "", name).strip())
        if k2:
            keys.add(k2)
        for key in keys:
            idx.setdefault(key, set()).add(fid)
    return idx


def match_feature(label, idx):
    label = clean_label(label)
    for key in (num_key(label), text_key(label)):
        hits = idx.get(key) if key else None
        if hits and len(hits) == 1:
            return next(iter(hits))
    return None


# Tables --------------------------------------------------------------------------

def header(t):
    """(column names in lower case, number of header rows)."""
    rows, hrows = t["rows"], []
    for r in rows[:3]:
        if r and all(c["th"] for c in r):
            hrows.append(r)
        else:
            break
    if not hrows:
        hrows = rows[:1]
    ncol = max(len(r) for r in rows[:6])
    names = []
    for j in range(ncol):
        parts = []
        for r in hrows:
            tx = W.text(r[j]).replace("\n", " ").strip() if j < len(r) else ""
            if tx and tx not in parts:
                parts.append(tx)
        names.append(" ".join(parts).lower())
    return names, len(hrows)


RATING_OUTLETS = re.compile(r"state navigate|capitol inside|marquette|sabato|cnalysis|split ticket|inside elections|cook", re.I)


def is_summary(t):
    names, nh = header(t)
    h = " | ".join(names)
    if len(t["rows"]) - nh < 2 or not re.search(r"district|dist\.", h):
        return False
    if not re.search(r"incumbent|member|senator", h):
        return False
    return not re.search(r"last result|previous result|trump margin|harris margin|reg\. voters|departing member", h) and not RATING_OUTLETS.search(h)


def party_of(text):
    t = (text or "").strip().strip("()").strip()
    if not t:
        return None
    low = t.lower().rstrip(".")
    for a, b in (("dem", "D"), ("democratic", "D"), ("dfl", "D"), ("democratic-npl", "D"), ("rep", "R"), ("republican", "R"),
                 ("ind", "I"), ("independent", "I"), ("lib", "L"), ("libertarian", "L"), ("grn", "G"), ("green", "G"),
                 ("nonpartisan", "N"), ("np", "N")):
        if low == a:
            return b
    code = el.party_code(t) if hasattr(el, "party_code") else None
    return code or t


def clean_person(s):
    s = re.sub(r"\((?:i|incumbent|write-in|withdrawn)\)", "", s, flags=re.I)
    s = re.sub(r"^\s*(?:Sen|Rep|Del|Asm|Senator|Representative|Delegate|Dr|Mr|Mrs|Ms)\.?\s+(?=[A-Z])", "", s)
    s = W.clean_name(s)
    return re.sub(r"\s+", " ", s).strip(" ,;:")


def summary_rows(t):
    """[{label, seat, pres24, incumbent, party, status, candidates}] from a district summary table."""
    names, nh = header(t)
    dist_cols = []
    for j, n in enumerate(names):
        if re.search(r"district|dist\.", n) and not re.search(r"pres|margin|elected", n):
            if not dist_cols or j == dist_cols[-1] + 1:
                dist_cols.append(j)
        elif dist_cols:
            break
    if not dist_cols:
        dist_cols = [0]
    seat_col = next((j for j, n in enumerate(names) if re.fullmatch(r"(seat|posi|position|pos\.?)", n)), None)
    pres_col = next((j for j, n in enumerate(names) if re.search(r"2024 pres", n)), None)
    inc_col = next((j for j, n in enumerate(names) if j not in dist_cols and re.search(r"incumbent|member|senator", n)
                    and not re.search(r"party|elected|status|margin|first", n)), None)
    # The incumbent's party sits right beside the incumbent (a later "Party" column
    # belongs to the candidates in Pennsylvania's combined table).
    party_cols = []
    if inc_col is not None:
        j = inc_col - 1
        while j >= 0 and "party" in names[j]:
            party_cols.insert(0, j)
            j -= 1
        j = inc_col + 1
        while j < len(names) and "party" in names[j]:
            party_cols.append(j)
            j += 1
    status_col = next((j for j, n in enumerate(names) if "status" in n), None)
    cand_col = next((j for j, n in enumerate(names) if re.search(r"(^|\s)candidates$", n) and "primary" not in n), None)
    out = []
    for r in t["rows"][nh:]:
        if len(r) <= max(dist_cols):
            continue
        label = " ".join(W.text(r[j]).strip() for j in dist_cols).strip()
        if not label or re.search(r"total|source", label, re.I):
            continue
        inc_cell = r[inc_col] if inc_col is not None and inc_col < len(r) else None
        party = next((W.text(r[j]).strip() for j in party_cols if j < len(r) and W.text(r[j]).strip()), "")
        if inc_col is not None and not party_cols and inc_cell and re.search(r"\(([RDI])\)", W.text(inc_cell)):
            party = re.search(r"\(([RDI])\)", W.text(inc_cell)).group(1)  # "Scott Sandall (R)"
        inc_raw = W.text(inc_cell) if inc_cell else ""
        status = " ".join(W.text(r[status_col]).split()) if status_col is not None and status_col < len(r) else ""
        if "†" in inc_raw or re.search(r"retir", inc_raw, re.I):
            status = status or "Retiring"
        if "‡" in inc_raw:
            status = status or "Lost renomination"
        out.append({
            "label": label, "seat": W.text(r[seat_col]).strip() if seat_col is not None and seat_col < len(r) else None,
            "pres24": margin(W.text(r[pres_col])) if pres_col is not None and pres_col < len(r) else None,
            "incumbent": None if re.search(r"vacant", inc_raw, re.I) else (clean_person(re.sub(r"\(.*?\)", "", inc_raw.split("\n")[0])) or None),
            "party": party_of(re.sub(r"\(.*?\)", "", party)) if party and not re.search(r"vacant", party, re.I) else None,
            "status": status,
            "candidates": column_candidates(r[cand_col]) if cand_col is not None and cand_col < len(r) else None,
        })
    return out


def margin(text):
    """'D+58.5', 'R +5.1', 'R+0.03' -> signed D-minus-R margin; None otherwise."""
    m = re.search(r"\b([DR])\s*\+\s*(\d+(?:\.\d+)?)", text or "")
    if not m:
        return None
    v = float(m.group(2))
    return v if m.group(1) == "D" else -v


def column_candidates(cell):
    """Candidates from a "Candidates" cell: '▌Name (Republican)' lines, a colored marker
    standing for the party where no name is given. Stops at "Eliminated in primary"."""
    text = W.text(cell)
    cut = NOT_ON_BALLOT.search(text)
    if cut:
        text = text[:cut.start()]
    if "▌" not in text:
        return [] if not text.strip() or re.fullmatch(r"\s*(TBD|TBA|None|—|-)\s*", text, re.I) else None
    marks = list(cell.get("marks") or [])
    out, mark_i = [], 0
    for part in re.split(r"(▌)", text):
        if part == "▌":
            mark_i += 1
            continue
        entry = part.strip()
        entry = re.sub(r"^Y\s+", "", entry)
        if not entry or re.search(r"write-in", entry, re.I):
            continue
        color = marks[mark_i - 1] if 0 < mark_i <= len(marks) else None
        m = re.search(r"\(([^()]+)\)\s*$", entry)
        party = party_of(m.group(1)) if m and m.group(1).lower() not in ("i", "incumbent") else None
        name = clean_person(entry[:m.start()] if m and party else entry)
        party = party or MARK_COLORS.get(color or "")
        if name and not re.search(r"\d|TBD", name):
            out.append({"name": name, "party": party})
    return out


def box_candidates(t):
    """Candidates in an election box (Party | Candidate | Votes | %)."""
    names, nh = header(t)
    cand_col = next((j for j, n in enumerate(names) if n.startswith("candidate")), None)
    if cand_col is None:
        return []
    out = []
    for r in t["rows"][nh:]:
        if cand_col >= len(r):
            continue
        name = W.text(r[cand_col])
        if not name or re.search(r"total|majority|turnout|write-in|blank|over/under|registered", name, re.I):
            continue
        party = next((W.text(r[j]).strip() for j in range(cand_col - 1, -1, -1) if W.text(r[j]).strip()), "")
        if re.search(r"total|write-in", party, re.I):
            continue
        person = clean_person(name)
        if person and not any(c["name"] == person for c in out):  # fusion: one candidate on several party lines
            out.append({"name": person, "party": party_of(party), "incumbent": "incumbent" in name.lower()})
    return out


GENERAL_BAD = re.compile(r"primary|special|caucus|runoff|convention|by county|results by", re.I)


def is_general_box(t):
    cap = t.get("caption") or ""
    names, _ = header(t)
    if not any(n.startswith("candidate") for n in names) or not any("party" in n for n in names):
        return False
    return bool(cap) and not GENERAL_BAD.search(cap) and bool(re.search(r"general|district|election", cap, re.I))


def district_sections(html, idx):
    """[(fid, html)] for sections whose title names a district: 'District 12', '12th
    district', 'House district 106', 'District A', '1st Barnstable'."""
    out = []
    for s in W.split_sections(html):
        title = re.sub(r"^(?:(?:State\s+)?(?:Senate|House|Assembly)\s+)?District\s+", "", s["title"], flags=re.I)
        title = re.sub(r"\s+district$", "", title, flags=re.I).strip()
        fid = match_feature(title, idx) if title else None
        if fid:
            out.append((fid, s["html"]))
    return out


PARTY_HEAD = re.compile(r"Republican|Democratic|Libertarian|Green|Independent|Constitution|Working Families|Forward|Unaffiliated", re.I)
NOMINEE_HEAD = re.compile(r"Nominees?|Presumptive nominees?|Advanced to (?:the )?general(?: election)?", re.I)


def nominee_candidates(sec_html):
    """November candidates listed in a district section: each party's "Nominee" list,
    a top-two "Advanced to general" list, or a district-level "Candidates" list whose
    entries name their party. Lists of declared primary candidates are not used."""
    out, party, seat, mode = [], None, None, None
    tokens = re.finditer(r'<div class="mw-heading mw-heading\d"[^>]*>\s*<h\d[^>]*>(.*?)</h\d>|<ul>(.*?)</ul>', sec_html, re.S)
    for m in tokens:
        if m.group(1) is not None:
            title = re.sub(r"<[^>]+>", "", m.group(1)).strip()
            if re.fullmatch(r"(Position|Seat)\s+\w+", title, re.I):
                seat, party, mode = title, None, None
            elif NOMINEE_HEAD.fullmatch(title):
                mode = "nominee"
            elif PARTY_HEAD.search(title):
                party, mode = party_of(PARTY_HEAD.search(title).group(0)), None
            elif re.fullmatch(r"Candidates", title, re.I) and party is None:
                mode = "listed"  # only entries that name their party count
            else:
                mode = None  # Declared, Eliminated in primary, Withdrawn, Endorsements...
        elif mode:
            for li in re.findall(r"<li>(.*?)</li>", m.group(2), re.S):
                t = re.sub(r"<sup.*?</sup>", "", li, flags=re.S)
                t = re.sub(r"<[^>]+>", "", t)
                pm = re.search(r"\(([A-Za-z][A-Za-z .-]+)\)", t)
                named = pm and (PARTY_HEAD.search(pm.group(1)) or pm.group(1) in ("DFL", "Dem-NPL", "R", "D", "I", "L", "G"))
                p = party_of(pm.group(1)) if named else None
                if mode == "listed" and not p:
                    continue
                name = clean_person(re.split(r",|\(|–|—| - ", t)[0])
                if name and len(name.split()) >= 2:
                    out.append({"name": name, "party": p or party, "seat": seat})
            mode = None
    return out


def infobox_candidates(sec_html):
    """The district's election infobox: a 'Candidate' row of names over a 'Party' row."""
    for t in W.tables(sec_html):
        rows = t["rows"]
        for i, r in enumerate(rows[:-1]):
            if r and W.text(r[0]).strip() in ("Candidate", "Nominee") and rows[i + 1] and W.text(rows[i + 1][0]).strip() == "Party":
                names = [clean_person(W.text(c)) for c in r[1:]]
                parties = [party_of(W.text(c)) for c in rows[i + 1][1:]]
                out = [{"name": n, "party": p} for n, p in zip(names, parties) if n]
                if out:
                    return out
    return []


def primary_winners(sec_html):
    """Who won or advanced from the primaries: the bold names in a district's primary
    boxes (a runoff's winner replaces the first round's leaders for that party)."""
    by_party, runoff = {}, {}
    for t in W.tables(sec_html):
        cap = t.get("caption") or ""
        if not re.search(r"primary", cap, re.I) or re.search(r"special", cap, re.I):
            continue
        names, nh = header(t)
        cand_col = next((j for j, n in enumerate(names) if n.startswith("candidate")), None)
        if cand_col is None:
            continue
        target = runoff if re.search(r"runoff", cap, re.I) else by_party
        for r in t["rows"][nh:]:
            if cand_col >= len(r) or not r[cand_col].get("bold"):
                continue
            name = W.text(r[cand_col])
            if not name or re.search(r"total|majority|turnout|write-in", name, re.I):
                continue
            party = party_of(next((W.text(r[j]).strip() for j in range(cand_col - 1, -1, -1) if W.text(r[j]).strip()), ""))
            target.setdefault(party, []).append({"name": clean_person(name), "party": party})
    by_party.update(runoff)
    return [c for cs in by_party.values() for c in cs if c["name"]]


def table_candidates(t):
    """Pennsylvania's combined table: District | Party | Incumbent | Status | Party | Candidate | Votes."""
    names, nh = header(t)
    cand_col = next((j for j, n in enumerate(names) if n == "candidate"), None)
    if cand_col is None:
        return {}
    out = {}
    for r in t["rows"][nh:]:
        if cand_col >= len(r):
            continue
        label = W.text(r[0]).strip()
        name = W.text(r[cand_col])
        if not label or not name or re.search(r"no candidate|vacant", name, re.I):
            continue
        party = next((W.text(r[j]).strip() for j in range(cand_col - 1, -1, -1) if W.text(r[j]).strip()), "")
        party = party.split("/")[0]  # "Democratic/Republican": cross-filed, listed under the first
        out.setdefault(label, []).append({"name": clean_person(name), "party": party_of(party)})
    return out


def rating_rows(t):
    """{district label: [{"outlet", "rating"}]} from a forecasters' district ratings table."""
    names, nh = header(t)
    cols = [(j, re.sub(r"\s+\w+\.?\s*\d.*$", "", n).strip().title()) for j, n in enumerate(names) if RATING_OUTLETS.search(n)]
    out = {}
    for r in t["rows"][nh:]:
        if not r:
            continue
        label = W.text(r[0]).strip()
        rs = [{"outlet": outlet, "rating": W.text(r[j]).strip()} for j, outlet in cols if j < len(r) and W.text(r[j]).strip()]
        if label and rs:
            out[label] = rs
    return out


# One chamber ---------------------------------------------------------------------

def slug(name):
    return re.sub(r"[^a-z]+", "-", _ascii(name).lower()).strip("-")


def parse_chamber(html, features):
    """{fid: district} plus counts, for one chamber page and its map features."""
    idx = feature_index(features)
    tabs = W.tables(html)
    summaries = [t for t in tabs if is_summary(t)]
    summary = max(summaries, key=lambda t: len(t["rows"]), default=None)
    districts, unmatched = {}, []
    for row in summary_rows(summary) if summary else []:
        fid = match_feature(row["label"], idx)
        if not fid:
            unmatched.append(row["label"])
            continue
        d = districts.setdefault(fid, {"label": row["label"], "pres24": row["pres24"], "incumbents": [], "candidates": None, "ratings": [], "via": None})
        inc = {"name": row["incumbent"], "party": row["party"], "status": row["status"], "seat": row["seat"]}
        if not any(x["name"] == inc["name"] and x["name"] and x["party"] == inc["party"] for x in d["incumbents"]):
            d["incumbents"].append(inc)  # a vacant seat stays as an entry with no name
        if row["candidates"]:
            d["candidates"] = (d["candidates"] or []) + [dict(c, seat=row["seat"]) for c in row["candidates"]]
            d["via"] = "column"
        if d["pres24"] is None:
            d["pres24"] = row["pres24"]
    listed = bool(districts)
    # General-election boxes and nominee lists in each district's section.
    for fid, sec in district_sections(html, idx):
        if fid not in districts:
            if listed:
                continue  # the summary table is the list of seats up; a stray section is an old race
            districts[fid] = {"label": fid, "pres24": None, "incumbents": [], "candidates": None, "ratings": [], "via": None}
        d = districts[fid]
        if d["via"] == "column":
            continue
        boxes = [t for t in W.tables(sec) if is_general_box(t)]
        if boxes:
            cands = box_candidates(boxes[-1])
            if cands:
                d["candidates"], d["via"] = cands, "box"
                continue
        info = infobox_candidates(sec)
        if info:
            d["candidates"], d["via"] = info, "infobox"
            continue
        # Nominee lists, with each remaining party's primary winners (bold in its box).
        noms = nominee_candidates(sec)
        have = {c["party"] for c in noms}
        wins = [c for c in primary_winners(sec) if c["party"] not in have]
        if noms or wins:
            # A list entry without a party takes it from the district's results boxes.
            known = {el.norm(c["name"]): c["party"] for t in W.tables(sec) for c in box_candidates(t) if c["party"]}
            for c in noms:
                c["party"] = c["party"] or known.get(el.norm(c["name"]))
            d["candidates"], d["via"] = noms + wins, "nominee" if noms else "primary"
    # Pennsylvania-style combined table.
    for t in tabs:
        names, _ = header(t)
        if "candidate" in names and any("status" in n for n in names) and len(t["rows"]) > 10:
            for label, cands in table_candidates(t).items():
                fid = match_feature(label, idx)
                if fid and fid in districts and districts[fid]["via"] is None:
                    districts[fid]["candidates"], districts[fid]["via"] = cands, "table"
    # Forecasters' district ratings.
    for t in tabs:
        names, _ = header(t)
        if "district" in " ".join(names) and any(RATING_OUTLETS.search(n) for n in names):
            for label, rs in rating_rows(t).items():
                fid = match_feature(re.sub(r"\s*\(.*\)", "", label), idx)
                if fid and fid in districts:
                    districts[fid]["ratings"] = rs
    return districts, {"summary": bool(summary), "unmatched": unmatched}


# Races ---------------------------------------------------------------------------

MIDTERM_RATIO = 0.75  # same as update_races.py
GENERAL_VIA = {"box", "column", "infobox", "table"}  # lists of the November field itself


def district_name(feature):
    """The map's district name, as the demo set words it ("District 12", "1st Barnstable District")."""
    n = feature["properties"].get("n", feature["id"])
    return re.sub(r"\s+", " ", re.sub(r"\b(State (Senate|House|Legislative)|Assembly|Legislative \((?:House|Senate)\)|Delegate)\s*", "", n)).strip()


def same_person(a, b):
    na, nb = el.norm(a or "").split(), el.norm(b or "").split()
    if not (na and nb) or not el.first_names_match(na[0], nb[0]):
        return False
    # "Nancy De Boer" and "Nancy DeBoer" are one person.
    return na[-1] == nb[-1] or "".join(na[1:]) == "".join(nb[1:])


def race_from(ch, fid, d, name, title, url, turnout):
    rid = f"{ch['state']}-{ch['prefix']}-{fid}"
    incs = [i for i in d["incumbents"] if i["name"]]
    seats = max(1, len(d["incumbents"]))
    cands, used = [], set()
    for x in d["candidates"] or []:
        base = slug(x["name"].split()[-1]) or "candidate"
        cid = f"{rid}:{base}"
        if cid in used:
            cid = f"{rid}:{slug(x['name'])}"
        used.add(cid)
        c = {"id": cid, "name": x["name"], "party": x["party"] or "Party not listed",
             "incumbent": any(same_person(x["name"], i["name"]) for i in incs)}
        if x.get("seat"):
            c["seat"] = x["seat"]
        cands.append(c)
    held = incs[0]["party"] if seats == 1 and incs and incs[0]["party"] in ("D", "R", "I", "N") else None
    race = {"id": rid, "state": ch["state"], "office": ch["office"], "chamber": ch["key"], "level": "state", "statewide": False,
            "district": fid, "districtName": name, "format": "field", "lean": d["pres24"], "pres24": d["pres24"],
            "held": held, "open": bool(seats == 1 and incs and re.search(r"retir|term|lost|running for|defeated|resign", incs[0]["status"], re.I)),
            "incumbents": [{"name": i["name"], "party": i["party"], "status": i["status"]} for i in d["incumbents"]],
            "candidates": cands, "candidatesFrom": None if d["candidates"] is None else "general" if d["via"] in GENERAL_VIA else "nominees",
            "polls": [], "turnout": turnout,
            "sources": [{"title": f"Wikipedia: {title}", "url": url}]}
    if seats > 1:
        race["seats"] = seats
    if d["ratings"]:
        race["ratings"] = d["ratings"]
        cons = model.consensus(d["ratings"], None)
        if cons:
            race["consensus"] = cons
    return race


RESEARCH_DIR = ROOT / "data" / "research" / "legislature"


def load_research():
    """{race id: overlay} from data/research/legislature/*.json, written by
    scripts/research/legislature_2026.py in the same shape as the federal overlays
    (a folder of its own, so update_races.py's federal overlays never see it)."""
    out = {}
    for p in sorted(RESEARCH_DIR.glob("*.json")) if RESEARCH_DIR.exists() else []:
        for r in json.loads(p.read_text(encoding="utf-8")).get("races", []):
            out[r["id"]] = r
    return out


def merge_research(race, ov, log):
    """Researched bios, campaign sites and sourced positions onto a race's candidates.
    A researched candidate Wikipedia doesn't list is kept, with a warning."""
    for oc in ov.get("candidates", []):
        c = next((x for x in race["candidates"] if x["id"] == oc.get("id")), None) or \
            el.match_candidate(oc["name"], race["candidates"], oc.get("party") if oc.get("party") in ("D", "R") else None)
        if c is None:
            c = {"id": oc.get("id") or f"{race['id']}:{slug(oc['name'].split()[-1])}", "name": oc["name"],
                 "party": oc.get("party") or "Party not listed", "incumbent": bool(oc.get("incumbent"))}
            race["candidates"].append(c)
            log(f"  warning: {race['id']}: researched candidate {oc['name']} is not on Wikipedia's list; kept from research")
        for f in ("bio", "officialSite", "positions"):
            if oc.get(f):
                c[f] = oc[f]
        if oc.get("party") and c.get("party") in (None, "Party not listed"):
            c["party"] = oc["party"]  # a party the page left out, from the candidate's own site
    if ov.get("notes"):
        race["notes"] = ov["notes"]
    # Matching needs every candidate's positions; until then the race stays "live data".
    if race["candidates"] and all(c.get("positions") for c in race["candidates"]):
        race["research"] = True


def build(votes24=None, out_dir=None, log=print):
    """Parse every chamber page and write data/legislature/{ST}.json. Returns counts."""
    out_dir = out_dir or ROOT / "data" / "legislature"
    out_dir.mkdir(parents=True, exist_ok=True)
    research = load_research()
    chs = chambers()
    titles = [t for c in chs for t in titles_for(c)]
    revs = W.revisions(titles)
    by_state, counts = {}, {"chambers": 0, "districts": 0, "withCandidates": 0, "missing": [], "unmatched": 0}
    for c in chs:
        title = next((t for t in titles_for(c) if revs.get(t)), None)
        feats = json.loads((ROOT / "data" / "maps" / c["layer"] / f"{c['state']}.json").read_text(encoding="utf-8"))["features"]
        ds, info = parse_chamber(W.page_at(title, revs[title]), feats) if title else ({}, {"summary": False, "unmatched": []})
        if c["up"] == "all" and title:
            # Every seat is on the ballot: a district the page doesn't cover is still a
            # real race, with its candidates not listed yet.
            for f in feats:
                if f["id"] not in ds and not re.search(r"not defined|^Z+$", f["properties"].get("n", "") + " " + f["id"]):
                    ds[f["id"]] = {"label": f["id"], "pres24": None, "incumbents": [], "candidates": None, "ratings": [], "via": None}
        if not ds:
            counts["missing"].append(f"{c['state']} {c['key']}")
            continue
        real_title = revs[title]["title"]
        url = WIKI + real_title.replace(" ", "_")
        # The seats on the ballot are known when every seat is up, when the page has its
        # district table, or when its sections cover about as many seats as the chamber elects.
        complete = c["up"] == "all" or bool(info["summary"]) or len(ds) >= len(feats) * 0.45
        votes = (votes24 or {}).get(c["state"])
        turnout = int(round(votes * MIDTERM_RATIO / len(feats), -2)) if votes else None
        names = {f["id"]: district_name(f) for f in feats}
        state = by_state.setdefault(c["state"], {"chambers": [], "races": []})
        races = [race_from(c, fid, d, names[fid], real_title, url, turnout) for fid, d in sorted(ds.items())]
        for r in races:
            if r["id"] in research:
                merge_research(r, research.pop(r["id"]), log)
                counts["researched"] = counts.get("researched", 0) + 1
        with_c = sum(1 for r in races if r["candidates"])
        state["chambers"].append({"key": c["key"], "title": real_title, "url": url, "complete": complete,
                                  "districts": len(races), "withCandidates": with_c})
        state["races"].extend(races)
        counts["chambers"] += 1
        counts["districts"] += len(races)
        counts["withCandidates"] += with_c
        counts["unmatched"] += len(info["unmatched"])
    for rid in research:
        log(f"  warning: legislative research for {rid} matches no district on the ballot")
    for old in out_dir.glob("*.json"):
        if old.stem not in by_state:
            old.unlink()
    for st, data in sorted(by_state.items()):
        (out_dir / f"{st}.json").write_text(json.dumps({"state": st, **data}, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    log(f"  state legislatures: {counts['districts']} districts in {counts['chambers']} chambers, {counts['withCandidates']} with candidates")
    return counts


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    want = set(sys.argv[1:])
    chs = [c for c in chambers() if not want or c["state"] in want]
    titles = [t for c in chs for t in titles_for(c)]
    revs = W.revisions(titles)
    for c in chs:
        title = next((t for t in titles_for(c) if revs.get(t)), None)
        if not title:
            print(c["state"], c["key"], "no page")
            continue
        feats = json.loads((ROOT / "data" / "maps" / c["layer"] / f"{c['state']}.json").read_text(encoding="utf-8"))["features"]
        ds, info = parse_chamber(W.page_at(title, revs[title]), feats)
        with_c = sum(1 for d in ds.values() if d["candidates"])
        vias = {}
        for d in ds.values():
            vias[d["via"]] = vias.get(d["via"], 0) + 1
        nopty = sum(1 for d in ds.values() for x in (d["candidates"] or []) if not x.get("party"))
        print(f"{c['state']} {c['key']:6} seats {c['seats']:3} up {c['up']:7} -> districts {len(ds):3}, with candidates {with_c:3}, "
              f"pres {sum(1 for d in ds.values() if d['pres24'] is not None):3}, rated {sum(1 for d in ds.values() if d['ratings']):2}, "
              f"via {vias}, no-party {nopty}, unmatched {info['unmatched'][:4]}")
