"""Parsers for Wikipedia's 2026 election tables: candidates, forecaster ratings,
polls, aggregator averages, fundraising and chamber composition."""

import re
import unicodedata
from datetime import date

from wikitables import tables, text

STATE_ABBR = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA", "Colorado": "CO",
    "Connecticut": "CT", "Delaware": "DE", "District of Columbia": "DC", "Florida": "FL", "Georgia": "GA",
    "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
    "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD", "Massachusetts": "MA",
    "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO", "Montana": "MT",
    "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM",
    "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
    "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD",
    "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT", "Virginia": "VA", "Washington": "WA",
    "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY",
}
STATE_NAME = {v: k for k, v in STATE_ABBR.items()}

# Forecaster column headings -> the names shown on the site.
OUTLETS = {
    "cook": "Cook Political Report", "ddhq": "Decision Desk HQ", "econ": "The Economist",
    "fpo": "FiftyPlusOne", "fox": "Fox News", "ie": "Inside Elections", "nbc": "NBC News",
    "rcp": "RealClearPolitics", "sabato": "Sabato’s Crystal Ball", "silver": "Silver Bulletin",
    "st": "Split Ticket", "cnalysis": "CNalysis", "cnn": "CNN", "cbs": "CBS News", "538": "538",
    "race": "Race to the WH", "elections daily": "Elections Daily", "ed": "Elections Daily",
}

MONTHS = {m: i + 1 for i, m in enumerate(
    ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"])}
for _m, _i in list(MONTHS.items()):
    MONTHS[_m[:3]] = _i
MONTHS["sept"] = 9


# Names and parties ---------------------------------------------------------------

def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"\([^)]*\)", " ", s)
    s = re.sub(r"\b(jr|sr|ii|iii|iv)\b\.?", " ", s)
    s = re.sub(r"[^a-z\s-]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def last_name(s):
    parts = norm(s).split()
    return parts[-1] if parts else ""


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", norm(s)).strip("-")


def party_code(name):
    n = (name or "").strip().lower()
    if not n:
        return "I"
    if n.startswith("republican"):
        return "R"
    if n.startswith("democrat") or n in ("dfl", "d-npl", "dem-npl"):  # incl. Minnesota's DFL and North Dakota's Dem-NPL
        return "D"
    if n.startswith("libertarian"):
        return "L"
    if n.startswith("green"):
        return "G"
    if n in ("independent", "unaffiliated", "no party preference", "nonpartisan", "no party", "nonaffiliated"):
        return "I"
    return name.strip()


def candidate_lines(cell_text):
    """'▌Barry Moore (Republican)\n▌Everett Wess (Democratic)' -> [(name, party code)].
    Write-in candidates are left out."""
    out = []
    for line in cell_text.split("\n"):
        line = line.strip().lstrip("▌").strip()
        if not line or "write-in" in line.lower():
            continue
        m = re.match(r"^(.*?)\s*\(([^)]*)\)\s*$", line)
        if m:
            name, parties = m.group(1), m.group(2)
            party = party_code(parties.split(",")[0].split("/")[0])
        else:
            name, party = line, "I"
        name = re.sub(r"\s+", " ", re.sub(r"[†‡*]", "", name)).strip(" ,;")
        if name:
            out.append((name, party))
    return out


def assign_ids(race_id, people):
    """Stable candidate ids: RACE:lastname, or RACE:full-name when two share a last name."""
    lasts = [slug(last_name(p["name"])) for p in people]
    for p, ln in zip(people, lasts):
        p["id"] = f"{race_id}:{ln if lasts.count(ln) == 1 else slug(p['name'])}"
    return people


NICKNAMES = [
    ("robert", "bob", "rob", "bobby"), ("william", "bill", "will", "billy"), ("james", "jim", "jimmy"),
    ("michael", "mike"), ("thomas", "tom", "tommy"), ("christopher", "chris"), ("joseph", "joe"),
    ("edward", "ted", "ed", "eddie"), ("theodore", "ted"), ("richard", "rick", "dick", "rich"),
    ("anthony", "tony"), ("patrick", "pat"), ("patricia", "pat", "patty"), ("katherine", "kate", "kathy", "katie"),
    ("catherine", "cathy", "kate"), ("elizabeth", "liz", "beth", "betsy"), ("charles", "chuck", "charlie"),
    ("john", "jack", "johnny"), ("andrew", "andy", "drew"), ("gregory", "greg"), ("stephen", "steve"),
    ("steven", "steve"), ("samuel", "sam"), ("matthew", "matt"), ("nicholas", "nick"), ("ronald", "ron"),
    ("donald", "don"), ("jeffrey", "jeff"), ("joshua", "josh"), ("kenneth", "ken"), ("lawrence", "larry"),
    ("gerald", "jerry"), ("benjamin", "ben"), ("alexander", "alex"), ("zachary", "zach"), ("timothy", "tim"),
    ("david", "dave"), ("jonathan", "jon"), ("deborah", "debbie", "deb"), ("susan", "sue"),
    ("jennifer", "jen", "jenny"), ("rebecca", "becky"), ("margaret", "maggie", "peggy"), ("frederick", "fred"),
    ("raymond", "ray"), ("douglas", "doug"), ("phillip", "phil"), ("philip", "phil"), ("leonard", "len"),
    ("eugene", "gene"), ("harold", "hal"), ("henry", "hank"), ("albert", "al"), ("alfred", "al"),
]
_NICK = {}
for _group in NICKNAMES:
    for _n in _group:
        _NICK.setdefault(_n, set()).update(_group)


def first_names_match(a, b):
    """'dan'/'daniel', 'j'/'james', 'bob'/'robert', 'zach'/'zack' match; 'lindsey'/'darline' don't."""
    return a == b or a.startswith(b) or b.startswith(a) or b in _NICK.get(a, ()) or (min(len(a), len(b)) >= 3 and a[:3] == b[:3])


def match_candidate(name, cands, party=None):
    """Find the candidate a poll column, FEC filer or table row refers to. A
    surname alone is enough when it is unique, but a different first name or a
    different major party rules a candidate out."""
    n = norm(name)
    if not n:
        return None
    full = [c for c in cands if norm(c["name"]) == n]
    if len(full) == 1:
        return full[0]
    tokens = n.split()
    same_last = [c for c in cands if last_name(c["name"]) == tokens[-1]]
    if party in ("D", "R"):
        same_last = [c for c in same_last if c["party"] == party or c["party"] not in ("D", "R")]
    if len(tokens) > 1:
        same_last = [c for c in same_last if first_names_match(tokens[0], norm(c["name"]).split()[0])]
    if len(same_last) == 1:
        return same_last[0]
    if len(same_last) > 1 and len(tokens) > 2:
        # Middle initials tell apart namesakes (Alaska's Dan S. and Dan J. Sullivan).
        hit = [c for c in same_last if tokens[1][:1] in [t[:1] for t in norm(c["name"]).split()[1:-1]]]
        if len(hit) == 1:
            return hit[0]
    return None


# Dates ---------------------------------------------------------------------------

def _md(token):
    m = re.match(r"([A-Za-z]+)\.?\s+(\d{1,2})$", token.strip())
    if not m or m.group(1).lower() not in MONTHS:
        return None
    return MONTHS[m.group(1).lower()], int(m.group(2))


def parse_range(s):
    """'October 20–21, 2026' / 'September 19 – October 1, 2025' / 'May 9, 2026' /
    'Dec 28, 2025 – Jan 3, 2026' / 'through October 21, 2026' -> (start, end) dates."""
    s = re.sub(r"[–—−]", "-", s.replace("\xa0", " ")).replace("\n", " ")
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"^(through|thru|until|as of)\s+", "", s, flags=re.I)
    years = [int(y) for y in re.findall(r"\b(20\d\d)\b", s)]
    if not years:
        return None, None
    body = re.sub(r",?\s*\b20\d\d\b", "", s).strip(" ,")
    parts = [p.strip(" ,") for p in body.split("-")]
    try:
        if len(parts) == 1:
            md = _md(parts[0])
            if not md:
                return None, None
            d = date(years[-1], *md)
            return d, d
        a, b = parts[0], parts[1]
        ma = _md(a)
        if not ma:
            return None, None
        if re.fullmatch(r"\d{1,2}", b):
            mb = (ma[0], int(b))
        else:
            mb = _md(b)
            if not mb:
                return None, None
        y_end = years[-1]
        y_start = years[0] if len(years) > 1 else (y_end - 1 if ma[0] > mb[0] else y_end)
        return date(y_start, *ma), date(y_end, *mb)
    except ValueError:
        return None, None


def iso(d):
    return d.isoformat() if d else None


# Tables --------------------------------------------------------------------------

def header_row(t, *must):
    """Index of the first row containing every heading in `must` (case-insensitive prefix)."""
    for i, row in enumerate(t["rows"][:4]):
        heads = [text(c).replace("\n", " ").strip().lower() for c in row]
        if all(any(h.startswith(m.lower()) for h in heads) for m in must):
            return i
    return None


def col(heads, *names):
    for name in names:
        for i, h in enumerate(heads):
            if h.startswith(name.lower()):
                return i
    return None


def heads_of(t, i):
    return [re.sub(r"\s+", " ", text(c).replace("\n", " ")).strip().lower() for c in t["rows"][i]]


def ratings_table(html_text, key_head):
    """Forecaster ratings table -> {row key: {"pvi", "ratings": [{outlet, rating, date}]}}.
    `key_head` is the first column's heading ("State" or "District")."""
    for t in tables(html_text):
        hi = header_row(t, key_head)
        if hi is None:
            continue
        heads = heads_of(t, hi)
        raw_heads = [text(c) for c in t["rows"][hi]]
        outlet_cols = []
        for j, h in enumerate(raw_heads):
            bits = [b.strip() for b in h.split("\n") if b.strip()]
            if not bits:
                continue
            key = bits[0].lower().rstrip(".")
            if key in OUTLETS:
                _, end = parse_range(" ".join(bits[1:])) if len(bits) > 1 else (None, None)
                outlet_cols.append((j, OUTLETS[key], iso(end)))
        if len(outlet_cols) < 3:
            continue
        pvi_col = col(heads, "pvi", "cpvi", "2026 pvi", "2025 pvi")
        out = {}
        for row in t["rows"][hi + 1:]:
            key = text(row[0]).replace("\n", " ").strip()
            if not key or key.lower().startswith("overall"):
                continue
            ratings = []
            for j, outlet, when in outlet_cols:
                if j < len(row):
                    r = text(row[j]).strip()
                    if r and r not in ("—", "-", "N/A"):
                        ratings.append({"outlet": outlet, "rating": r, "date": when})
            out[key] = {"pvi": parse_pvi(text(row[pvi_col])) if pvi_col is not None else None, "ratings": ratings,
                        "links": row[0]["links"]}
        return out
    return {}


def parse_pvi(s):
    """'R+15' -> -15, 'D+6' -> 6, 'EVEN' -> 0 (positive = Democratic-leaning)."""
    s = (s or "").strip().upper()
    if s.startswith("EVEN"):
        return 0.0
    m = re.match(r"([DR])\s*\+\s*(\d+(?:\.\d+)?)", s)
    if not m:
        return None
    v = float(m.group(2))
    return v if m.group(1) == "D" else -v


def num(s):
    s = (s or "").strip().replace(",", "")
    if s.startswith("<"):
        try:
            return float(re.sub(r"[^\d.]", "", s)) / 2
        except ValueError:
            return None
    m = re.search(r"-?\d+(?:\.\d+)?", s)
    return float(m.group(0)) if m else None


def money(s):
    s = (s or "").replace(",", "").strip()
    m = re.search(r"\$\s*(-?\d+(?:\.\d+)?)\s*(million|m|thousand|k)?", s, re.I)
    if not m:
        return None
    v = float(m.group(1))
    unit = (m.group(2) or "").lower()
    if unit in ("million", "m"):
        v *= 1e6
    elif unit in ("thousand", "k"):
        v *= 1e3
    return round(v)


PARTY_ABBR = {"R": "R", "D": "D", "L": "L", "G": "G", "I": "I", "IND": "I", "LIB": "L", "GRN": "G", "REP": "R", "DEM": "D"}
SKIP_COLS = ("other", "undecided", "margin", "lead", "someone else", "would not vote", "none", "refused", "don't know", "dont know", "no opinion", "others")


def _poll_columns(t, hi):
    """Candidate columns of a poll table: [(index, name, party)]."""
    heads = heads_of(t, hi)
    start = col(heads, "margin of error", "margin", "sample size", "sample")
    if start is None:
        return []
    if heads[start].startswith("sample") and col(heads, "margin of error") is not None:
        start = col(heads, "margin of error")
    out = []
    seen = set()
    for j in range(start + 1, len(heads)):
        cell = t["rows"][hi][j]
        if id(cell) in seen:
            continue
        seen.add(id(cell))
        raw = text(cell).replace("\n", " ").strip()
        low = raw.lower()
        if not raw or any(low.startswith(s) for s in SKIP_COLS):
            continue
        m = re.match(r"^(.*?)\s*\(([A-Za-z.\-]{1,12})\)\s*$", raw)
        name, party = (m.group(1), PARTY_ABBR.get(m.group(2).upper().rstrip("."), m.group(2))) if m else (raw, None)
        out.append((j, re.sub(r"\s+", " ", name).strip(), party))
    return out


def parse_sample(s):
    s = (s or "").replace(",", "")
    n = re.search(r"\d+", s)
    pop = re.search(r"\(\s*(LV|RV|A|V|RV/LV)\s*\)", s, re.I)
    return (int(n.group(0)) if n else None), (pop.group(1).upper() if pop else None)


def poll_rows(t, hi, colmap, refs):
    """Rows of one poll table, as poll dicts keyed by candidate id."""
    heads = heads_of(t, hi)
    c_src = col(heads, "poll source", "source")
    c_date = col(heads, "date")
    c_n = col(heads, "sample")
    polls = []
    for row in t["rows"][hi + 1:]:
        if len(row) <= max(colmap):
            continue
        src = text(row[c_src]).replace("\n", " ").strip() if c_src is not None else ""
        if not src or (row[c_src].get("th") and src.lower().startswith("poll source")):
            continue
        start, end = parse_range(text(row[c_date])) if c_date is not None else (None, None)
        if not end:
            continue
        results = {}
        for j, cid in colmap.items():
            cell = text(row[j]).strip()
            v = num(cell)
            if v is not None and ("%" in cell or re.fullmatch(r"\d+(\.\d+)?", cell)):
                results[cid] = v
        if len(results) < 2:
            continue
        n, pop = parse_sample(text(row[c_n])) if c_n is not None else (None, None)
        ref = next((refs[r] for r in row[c_src].get("refs", []) if r in refs), None) if c_src is not None else None
        p = {"pollster": re.sub(r"\s+", " ", src).strip(), "start": iso(start), "end": iso(end), "n": n,
             "pop": pop or "V", "results": results}
        if ref:
            p["url"] = ref["url"]
        polls.append(p)
    return polls


POP_RANK = {"LV": 0, "RV": 1, "V": 2, "A": 3, "RV/LV": 1}


def dedupe_polls(polls):
    """One row per poll: when a pollster reports several versions (likely and
    registered voters, with and without leaners), keep the likely-voter one,
    else the first listed."""
    best = {}
    order = []
    for p in polls:
        key = (re.sub(r"\W+", "", p["pollster"].lower()), p["end"], p.get("start"))
        if key not in best:
            best[key] = p
            order.append(key)
        elif POP_RANK.get(p["pop"], 9) < POP_RANK.get(best[key]["pop"], 9):
            best[key] = p
    return [best[k] for k in order]


def find_polls(html_text, refs, cands, need):
    """The first poll table whose candidate columns are all on the ballot and that
    includes at least one candidate from each group in `need` (normally the two
    main contenders). Hypothetical match-ups with candidates who are not running
    are skipped automatically.

    Returns (polls, aggregates)."""
    polls, aggregates = [], []
    found_main = False
    for t in tables(html_text):
        hi = header_row(t, "source of poll aggregation")
        if hi is not None:
            aggregates = aggregates or _aggregates(t, hi, cands)
            continue
        if found_main:
            continue
        hi = header_row(t, "poll source")
        if hi is None:
            continue
        cols = _poll_columns(t, hi)
        if len(cols) < 2:
            continue
        colmap = {}
        ok = True
        for j, name, party in cols:
            c = match_candidate(name, cands, party)
            if not c or c["id"] in colmap.values():
                ok = False
                break
            colmap[j] = c["id"]
        if not ok or not all(any(n["id"] in colmap.values() for n in group) for group in need):
            continue
        rows = dedupe_polls(poll_rows(t, hi, colmap, refs))
        if rows:
            polls = rows
            found_main = True
    return polls, aggregates


def _aggregates(t, hi, cands):
    heads = heads_of(t, hi)
    c_upd = col(heads, "dates updated", "updated")
    out = []
    cols = []
    for j, h in enumerate(heads):
        if j < 3:
            continue
        raw = text(t["rows"][hi][j]).replace("\n", " ").strip()
        if any(raw.lower().startswith(s) for s in SKIP_COLS):
            continue
        m = re.match(r"^(.*?)\s*\(([A-Za-z]{1,3})\)\s*$", raw)
        name = m.group(1) if m else raw
        c = match_candidate(name, cands, {"R": "R", "D": "D"}.get(m.group(2).upper()) if m else None)
        if c:
            cols.append((j, c["id"]))
    if len(cols) < 2:
        return []
    for row in t["rows"][hi + 1:]:
        src = text(row[0]).replace("\n", " ").strip()
        if not src:
            continue
        res = {cid: num(text(row[j])) for j, cid in cols if j < len(row) and num(text(row[j])) is not None}
        if len(res) < 2:
            continue
        _, upd = parse_range(text(row[c_upd])) if c_upd is not None else (None, None)
        out.append({"source": src, "updated": iso(upd), "results": res, "average": src.lower().startswith("average")})
    return out


def find_fundraising(html_text, refs, cands):
    """Latest 'Campaign finance reports as of ...' figures for each candidate."""
    best = {}
    for t in tables(html_text):
        rows = t["rows"]
        if not rows or not text(rows[0][0]).lower().startswith("campaign finance reports as of"):
            continue
        _, asof = parse_range(text(rows[0][0]).split("as of", 1)[1])
        hi = header_row(t, "candidate")
        if hi is None:
            continue
        heads = heads_of(t, hi)
        c_raised, c_spent, c_cash = col(heads, "raised"), col(heads, "spent"), col(heads, "cash")
        url = None
        for row in rows:
            for c in row:
                for r in c.get("refs", []):
                    if r in refs:
                        url = url or refs[r]["url"]
        source = "FEC" if any("federal election commission" in text(c).lower() for row in rows for c in row) else None
        for row in rows[hi + 1:]:
            name = text(row[0]).replace("\n", " ").strip()
            m = re.match(r"^(.*?)\s*\(([A-Za-z]{1,3})\)", name)
            c = match_candidate(m.group(1) if m else name, cands, m.group(2).upper() if m else None)
            if not c or c_raised is None:
                continue
            raised = money(text(row[c_raised]))
            if raised is None:
                continue
            prev = best.get(c["id"])
            if prev and prev["asOf"] and asof and prev["asOf"] >= iso(asof):
                continue
            best[c["id"]] = {"total": raised, "spent": money(text(row[c_spent])) if c_spent is not None else None,
                             "cashOnHand": money(text(row[c_cash])) if c_cash is not None else None,
                             "asOf": iso(asof), "url": url, "source": source}
    return best


def party_summary(html_text):
    """Latest dated row of a '... party summary' table -> {"D","I","R","total","vacant","asOf"}."""
    for t in tables(html_text):
        hi = header_row(t, "", "democratic", "republican")
        if hi is None:
            continue
        heads = heads_of(t, hi)
        cD, cI, cR = col(heads, "democratic"), col(heads, "independent"), col(heads, "republican")
        cT, cV = col(heads, "total"), col(heads, "vacant")
        latest = None
        for row in t["rows"][hi + 1:]:
            label = text(row[0]).replace("\n", " ").strip()
            _, d = parse_range(label)
            if not d:
                continue
            vals = [num(text(row[c])) if c is not None else 0 for c in (cD, cI, cR, cT, cV)]
            if None in vals[:3]:
                continue
            latest = {"D": int(vals[0]), "I": int(vals[1] or 0), "R": int(vals[2]), "total": int(vals[3] or 0),
                      "vacant": int(vals[4] or 0), "asOf": iso(d)}
        if latest:
            return latest
    return None


def generic_ballot(html_text):
    """Average row of the generic-ballot aggregate table -> D-minus-R margin."""
    for t in tables(html_text):
        hi = header_row(t, "source of poll aggregation")
        if hi is None:
            continue
        heads = heads_of(t, hi)
        cD, cR = col(heads, "democrat"), col(heads, "republican")
        c_upd = col(heads, "dates updated")
        rows = []
        for row in t["rows"][hi + 1:]:
            src = text(row[0]).strip()
            d, r = num(text(row[cD])), num(text(row[cR]))
            if d is None or r is None:
                continue
            _, upd = parse_range(text(row[c_upd])) if c_upd is not None else (None, None)
            rows.append({"source": src, "D": d, "R": r, "margin": round(d - r, 1), "updated": iso(upd)})
        avg = next((x for x in rows if x["source"].lower().startswith("average")), None)
        if not avg and rows:
            m = sum(x["margin"] for x in rows) / len(rows)
            avg = {"source": "Average", "margin": round(m, 1), "updated": max((x["updated"] or "") for x in rows) or None}
        if avg:
            return {"margin": avg["margin"], "updated": avg["updated"], "sources": [x for x in rows if not x["source"].lower().startswith("average")]}
    return None
