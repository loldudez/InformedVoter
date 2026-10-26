"""Refresh every 2026 U.S. Senate, governor and U.S. House race and recompute the
forecasts and chamber control; also rebuild the state legislative races.

    py scripts/update_races.py

Writes data/races.json (every race), data/control.json (chamber control, expected
seats and gains, with a history) and data/status.json (the automatic checks).
refresh_all.py runs it every 8 hours.

Sources
- Wikipedia's 2026 election pages, used as an aggregator (CC BY-SA): candidates
  on the ballot, the forecasters' ratings, each race's polls (with the poll's own
  citation), fundraising tables, and the current party composition.
- The FEC API for federal fundraising (see scripts/lib/fec.py).
- The UF Election Lab's early-vote tracker for ballots cast before Election Day
  (see scripts/lib/early_vote.py).
- Wikipedia's 2026 state legislative chamber pages for every legislative seat on the
  ballot, written to data/legislature/ST.json (see scripts/lib/legislature.py).
- Polymarket's chamber-control markets, as a cross-check only. They never feed
  the forecast.
- Hand-researched details (bios, positions, curated polls, early vote) in
  data/research/*.json, merged on top. See DATA.md.
"""

import html
import json
import math
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "lib"))

import early_vote  # noqa: E402
import elections as el  # noqa: E402
import fec  # noqa: E402
import house_votes  # noqa: E402
import legislature  # noqa: E402
import model  # noqa: E402
import wikitables as wt  # noqa: E402

DATA = ROOT / "data"
WIKI = "https://en.wikipedia.org/wiki/"
PAGES = {
    "senate": "2026 United States Senate elections",
    "governor": "2026 United States gubernatorial elections",
    "house": "2026 United States House of Representatives elections",
    "ratings": "2026 United States House of Representatives election ratings",
    "congress": "119th United States Congress",
    "pres24": "2024 United States presidential election",
}
# Election formats the national tables don't spell out.
FORMATS = {("LA", "house"): {"format": "open-primary", "runoff": "2026-12-12"}}
# Ranked-choice general elections: Alaska (all races) and Maine (federal races only;
# its constitution keeps governor races plurality).
RCV = {("AK", "senate"), ("AK", "governor"), ("AK", "house"), ("ME", "senate"), ("ME", "house")}
# Governors not on the 2026 ballot, by party (verified October 2026). The script
# checks that these plus the 36 races on the ballot make 50.
GOV_HOLDOVER = {"D": ["DE", "KY", "NJ", "NC", "VA", "WA"], "R": ["IN", "LA", "MS", "MO", "MT", "ND", "UT", "WV"]}
# Both Senate independents (King, Sanders) caucus with the Democrats.
SENATE_INDEPENDENTS_CAUCUS = "D"
# Midterm turnout relative to the last presidential election: 0.71 in 2022, 0.85 in 2018.
MIDTERM_RATIO = 0.75
POLYMARKET = {
    "senate": "which-party-will-win-the-senate-in-2026",
    "house": "which-party-will-win-the-house-in-2026",
}
UA = "InformedVoter/1.0 (personal election-information site; data refresh script)"
NOW = datetime.now()


def log(*a):
    print(*a, flush=True)


def wiki_url(title):
    return WIKI + title.replace(" ", "_")


class Status:
    def __init__(self):
        self.checks = []
        self.warnings = []

    def check(self, cid, label, ok, detail, level="warn"):
        self.checks.append({"id": cid, "label": label, "status": "pass" if ok else level, "detail": detail})
        log(f"  [{'pass' if ok else level}] {label}: {detail}")

    def warn(self, msg):
        self.warnings.append(msg)
        log("  warning:", msg)


# Pages ---------------------------------------------------------------------------

class Pages:
    """Fetches pages by title through the revision cache."""

    def __init__(self):
        self.revs = {}

    def prefetch(self, titles):
        need = [t for t in titles if t not in self.revs]
        if need:
            self.revs.update(wt.revisions(need))

    def html(self, title):
        self.prefetch([title])
        rev = self.revs.get(title)
        if not rev:
            return None
        return wt.page_at(rev["title"], rev)

    def url(self, title):
        rev = self.revs.get(title)
        return wiki_url(rev["title"] if rev else title)


# States --------------------------------------------------------------------------

def load_states():
    """abbr -> {name, pop, pres24, senate held, governor held} parsed from js/data/states.js,
    so the site and this script share one list."""
    src = (ROOT / "js" / "data" / "states.js").read_text(encoding="utf-8")
    out = {}
    for m in re.finditer(r"S\('([A-Z]{2})', '(\d\d)', '([^']+)', (-?[\d.]+), ([\d.]+), (sen\('([DR])'(?:, '(\w+)')?\)|null), (gov\('([DR])'\)|null)", src):
        out[m.group(1)] = {"name": m.group(3), "pres24": float(m.group(4)), "pop": float(m.group(5)),
                           "senate": m.group(7), "governor": m.group(10)}
    return out


def turnout_2024(pages):
    """Total presidential votes by state in 2024."""
    h = pages.html(PAGES["pres24"])
    chunk = wt.section_by_title(h or "", "Results by state") or ""
    out = {}
    for t in wt.tables(chunk):
        hi = el.header_row(t, "state or district")
        if hi is None:
            continue
        heads = el.heads_of(t, hi + 1) if hi + 1 < len(t["rows"]) else el.heads_of(t, hi)
        c_tot = el.col(heads, "total votes")
        if c_tot is None:
            continue
        for row in t["rows"][hi + 1:]:
            name = re.sub(r"[†‡*]", "", wt.text(row[0])).strip()
            if name in el.STATE_ABBR and c_tot < len(row):
                v = el.num(wt.text(row[c_tot]))
                if v:
                    out[el.STATE_ABBR[name]] = v
        if len(out) >= 50:
            break
    return out


# National tables -----------------------------------------------------------------

def state_key(label):
    """'Florida (special)' / 'Ohio (Class 3)' -> ('FL', True)."""
    base = re.sub(r"\(.*?\)", "", label).strip()
    return el.STATE_ABBR.get(base), "special" in label.lower() or "class 3" in label.lower()


RUNNING = ("renominated", "advanced", "running", "appointee nominated", "seeking re-election")


def new_candidates(race_id, cand_cell, inc_cell=None, status_text=""):
    """Candidates from a '▌Name (Party)' cell. The incumbent is found by the
    Wikipedia article both cells link to (which tells apart, say, Alaska's two
    Dan Sullivans), falling back to the name."""
    people = [{"name": n, "party": p} for n, p in el.candidate_lines(wt.text(cand_cell))]
    el.assign_ids(race_id, people)
    links = {el.norm(l["text"]): l["href"] for l in cand_cell["links"] if l["href"].startswith("/wiki/") and l["text"].strip()}
    for p in people:
        href = links.get(el.norm(p["name"]))
        if href:
            p["wiki"] = "https://en.wikipedia.org" + href
    inc = None
    if inc_cell is not None:
        inc_href = next((l["href"] for l in inc_cell["links"] if l["href"].startswith("/wiki/") and ":" not in l["href"]), None)
        if inc_href:
            inc = next((p for p in people if p.get("wiki") == "https://en.wikipedia.org" + inc_href), None)
        name = wt.text(inc_cell).split("\n")[0].strip()
        if inc is None and name and not name.lower().startswith(("vacant", "new seat", "none")):
            inc = el.match_candidate(name, people)
    for p in people:
        p["incumbent"] = p is inc
    running = inc is not None or any(w in status_text.lower() for w in RUNNING)
    return people, running


def statewide_races(pages, status):
    """Senate and governor races from the national pages."""
    races = {}
    sen_html = pages.html(PAGES["senate"])
    gov_html = pages.html(PAGES["governor"])

    def candidates_table(html_text, sec_title, office, special):
        chunk = wt.section_by_title(html_text, sec_title)
        if not chunk:
            status.warn(f"section '{sec_title}' not found for {office}")
            return
        for t in wt.tables(chunk):
            hi = el.header_row(t, "state", "candidates")
            if hi is None:
                continue
            heads = el.heads_of(t, hi)
            c_inc = el.col(heads, "senator", "governor")
            c_party = el.col(heads, "party")
            c_cand = el.col(heads, "candidates")
            c_status = el.col(heads, "status", "results")
            for row in t["rows"][hi + 1:]:
                label = wt.text(row[0]).replace("\n", " ").strip()
                st, is_special = state_key(label)
                if not st:
                    continue
                is_special = is_special or special
                rid = f"{st}-{'SEN' if office == 'senate' else 'GOV'}"
                inc_name = wt.text(row[c_inc]).split("\n")[0].strip() if c_inc is not None else None
                status_text = wt.text(row[c_status]).replace("\n", " ") if c_status is not None else ""
                people, inc_running = new_candidates(rid, row[c_cand], row[c_inc] if c_inc is not None else None, status_text)
                link = next((l["title"] for l in row[0]["links"] if l["title"].startswith("2026")), None)
                races[rid] = {
                    "rcv": (st, office) in RCV,
                    "id": rid, "state": st, "office": office, "level": "federal" if office == "senate" else "state",
                    "district": None, "statewide": True, "special": is_special,
                    "held": el.party_code(wt.text(row[c_party])) if c_party is not None else None,
                    "incumbentName": inc_name, "open": not inc_running, "statusText": status_text,
                    "candidates": people, "page": link,
                }

    candidates_table(sen_html, "Elections leading to the next Congress", "senate", False)
    candidates_table(sen_html, "Special elections during the preceding Congress", "senate", True)
    candidates_table(gov_html, "States", "governor", False)

    # Forecaster ratings and PVI.
    for html_text, office, sec in ((sen_html, "senate", "Predictions"), (gov_html, "governor", "Predictions")):
        chunk = wt.section_by_title(html_text, sec) or ""
        rated = el.ratings_table(chunk, "State")
        for label, info in rated.items():
            st, _ = state_key(label)
            rid = f"{st}-{'SEN' if office == 'senate' else 'GOV'}"
            if rid in races:
                races[rid]["ratings"] = info["ratings"]
                races[rid]["pvi"] = info["pvi"]
                races[rid]["ratingsSource"] = {"title": f"Wikipedia: {PAGES[office]}, Predictions", "url": pages.url(PAGES[office]) + "#Predictions"}
                if not races[rid].get("page"):
                    races[rid]["page"] = next((l["title"] for l in info["links"] if l["title"].startswith("2026")), None)
            elif st:
                status.warn(f"rated {office} race {label} has no candidate row")
    return races, sen_html, gov_html


def overall_rows(html_text, sec, key_head):
    """Each outlet's seat totals from the 'Overall' row: {outlet: {"D", "R", "T"}}."""
    chunk = wt.section_by_title(html_text, sec) if sec else html_text
    out = {}
    for t in wt.tables(chunk or ""):
        hi = el.header_row(t, key_head)
        if hi is None:
            continue
        raw_heads = [wt.text(c) for c in t["rows"][hi]]
        for row in t["rows"][hi + 1:]:
            if not wt.text(row[0]).lower().startswith("overall"):
                continue
            seen = set()
            for j, cell in enumerate(row):
                if id(cell) in seen or j >= len(raw_heads):
                    continue
                seen.add(id(cell))
                key = raw_heads[j].split("\n")[0].strip().lower().rstrip(".")
                if key not in el.OUTLETS:
                    continue
                s = wt.text(cell).replace("–", "-")
                d = re.search(r"D(?:/I)?\s*-\s*(\d+)", s)
                r = re.search(r"R\s*-\s*(\d+)", s)
                tu = re.search(r"(\d+)\s*toss", s, re.I)
                if d and r:
                    out[el.OUTLETS[key]] = {"D": int(d.group(1)), "R": int(r.group(1)), "T": int(tu.group(1)) if tu else 0}
        if out:
            break
    return out


def house_races(pages, status, map_index):
    races = {}
    h = pages.html(PAGES["house"])
    state_pages = {}
    for sec in wt.split_sections(h):
        if sec["level"] != 2:
            continue
        name = sec["title"]
        st = el.STATE_ABBR.get(name)
        if name == "Non-voting delegates":
            st = "DC"
        if not st:
            continue
        m = re.search(r'Main articles?:.*?<a href="/wiki/([^"#]+)"', sec["html"], re.S)
        if m and st != "DC":
            state_pages[st] = html.unescape(urllib.parse.unquote(m.group(1))).replace("_", " ")
        for t in wt.tables(sec["html"]):
            hi = el.header_row(t, "candidates", "party")
            if hi is None:
                continue
            heads = el.heads_of(t, hi)
            c_pvi = el.col(heads, "2026 pvi", "pvi", "cpvi")
            c_member = el.col(heads, "member", "delegate")
            c_party = el.col(heads, "party")
            c_status = el.col(heads, "status", "results")
            c_cand = el.col(heads, "candidates")
            for row in t["rows"][hi + 1:]:
                label = wt.text(row[0]).replace("\n", " ").strip()
                if st == "DC":
                    if not label.startswith("District of Columbia"):
                        continue
                    code = "98"
                else:
                    dm = re.match(rf"{re.escape(name)}\s+(\d+|at-large)", label, re.I)
                    if not dm:
                        continue
                    code = "00" if dm.group(1).lower() == "at-large" else f"{int(dm.group(1)):02d}"
                rid = f"{st}-H-{code}"
                member = wt.text(row[c_member]).split("\n")[0].strip() if c_member is not None else ""
                vacant = not member or member.lower().startswith(("vacant", "new seat", "none"))
                status_text = wt.text(row[c_status]).replace("\n", " ") if c_status is not None else ""
                people, inc_running = new_candidates(rid, row[c_cand], None if vacant or c_member is None else row[c_member], status_text)
                held = el.party_code(wt.text(row[c_party])) if c_party is not None and not vacant else None
                if held not in ("D", "R", "I"):
                    held = None
                n_cd = map_index.get(st, {}).get("cd", 0)
                race = {
                    "id": rid, "state": st, "office": "house", "level": "federal", "district": code,
                    "districtName": "Delegate (at large)" if st == "DC" else ("At-large district" if code == "00" else f"District {int(code)}"),
                    "statewide": n_cd == 1, "special": False, "held": held, "incumbentName": None if vacant else member,
                    "open": not inc_running, "statusText": status_text,
                    "incumbentWiki": None if vacant or c_member is None else next(("https://en.wikipedia.org" + l["href"] for l in row[c_member]["links"] if l["href"].startswith("/wiki/") and ":" not in l["href"]), None),
                    "pvi": el.parse_pvi(wt.text(row[c_pvi])) if c_pvi is not None else None,
                    "candidates": people,
                }
                race.update(FORMATS.get((st, "house"), {}))
                race["rcv"] = (st, "house") in RCV
                races[rid] = race
    # Ratings for competitive seats.
    rh = pages.html(PAGES["ratings"])
    rated = el.ratings_table(rh, "District")
    for label, info in rated.items():
        m = re.match(r"(.+?)\s+(\d+|at-large)$", label, re.I)
        st = el.STATE_ABBR.get(m.group(1)) if m else None
        if not st:
            status.warn(f"House rating row not understood: {label}")
            continue
        code = "00" if m.group(2).lower() == "at-large" else f"{int(m.group(2)):02d}"
        rid = f"{st}-H-{code}"
        if rid not in races:
            status.warn(f"rated House race {label} not found in the candidate tables")
            continue
        races[rid]["ratings"] = info["ratings"]
        races[rid]["ratingsSource"] = {"title": f"Wikipedia: {PAGES['ratings']}", "url": pages.url(PAGES["ratings"])}
        if info["pvi"] is not None and races[rid].get("pvi") is None:
            races[rid]["pvi"] = info["pvi"]
    return races, state_pages, h, rh


# Race pages: polls, aggregates, fundraising ----------------------------------------

def prominence(race, finance):
    """Order candidates strongest first: latest poll share, then incumbency, then money raised."""
    latest = {}
    for p in sorted(race.get("polls", []), key=lambda p: p["end"]):
        latest.update(p["results"])

    def key(c):
        fin = finance.get(c["id"]) or {}
        major = 0 if c["party"] in ("D", "R") else 1  # with no polls or money to go on, the major parties lead
        return (-(latest.get(c["id"]) or 0), 0 if c.get("incumbent") else 1, -(fin.get("total") or 0), major)
    race["candidates"].sort(key=key)


def main_two(race):
    a, b = model.main_contenders(race["candidates"])
    return [x for x in (a, b) if x]


def attach_page_data(race, html_text, refs, status, scope_title="General election"):
    general = wt.section_by_title(html_text, scope_title, level=2) or wt.section_by_title(html_text, scope_title) or html_text
    fund = el.find_fundraising(general, refs, race["candidates"])
    if not fund and general is not html_text:
        fund = el.find_fundraising(html_text, refs, race["candidates"])
    prominence(race, fund)  # money decides who the main contenders are in a crowded field
    two = main_two(race)
    race["polls"], race["aggregates"] = [], []
    if len(two) < 2:
        return fund
    a, b = two
    cands = race["candidates"]
    # A poll must include both main contenders; failing that, any candidate of each
    # main contender's party, and finally anyone against the second contender's party.
    attempts = [[[a], [b]],
                [[c for c in cands if c["party"] == a["party"]], [c for c in cands if c["party"] == b["party"]]],
                [[c for c in cands if c["party"] != b["party"]], [c for c in cands if c["party"] == b["party"]]]]
    polls, aggs = [], []
    for need in attempts:
        for scope in ([general, html_text] if general is not html_text else [general]):
            polls, aggs2 = el.find_polls(scope, refs, race["candidates"], need)
            aggs = aggs or aggs2
            if polls:
                break
        if polls:
            break
    race["polls"] = [p for p in polls if p["end"] >= "2025-01-01"]
    race["aggregates"] = aggs
    if race.get("rcv"):
        # Ranked-choice polls publish each round; the final one feeds the forecast.
        race["finalPolls"] = el.find_rcv_final(general, refs, race["candidates"]) or \
            (el.find_rcv_final(html_text, refs, race["candidates"]) if general is not html_text else [])
    return fund


def attach_sites(race_list, sites):
    """Official campaign websites from a race page's External links, for candidates
    whose name (and major party, where given) match without doubt. A researched
    officialSite in an overlay still wins. Returns how many were attached."""
    n = 0
    for name, party, url in sites:
        hits = [c for r in race_list for c in [el.match_candidate(name, r["candidates"], party if party in ("D", "R") else None)] if c]
        if len(hits) == 1 and not hits[0].get("officialSite"):
            hits[0]["officialSite"] = url
            n += 1
    return n


def district_chunks(html_text, n_cd):
    """{'01': html, ...} for a state's House page."""
    if n_cd == 1:
        return {"00": html_text}
    out = {}
    for s in wt.split_sections(html_text):
        m = re.fullmatch(r"District (\d+)", s["title"])
        if m and s["level"] == 2:
            out[f"{int(m.group(1)):02d}"] = s["html"]
    return out


# Priors --------------------------------------------------------------------------

def set_prior(race, generic):
    """Expected margin and baseline shares from forecasters' ratings, or from the
    partisan lean when no forecaster rates the race."""
    cands = race["candidates"]
    pvi = race.get("pvi")
    base = None if pvi is None else 2 * pvi + generic
    cons = model.consensus(race.get("ratings") or [], base)
    a, b = model.main_contenders(cands) if cands else (None, None)
    if len(cands) <= 1 or b is None:
        margin = 100.0 if cands and cands[0]["party"] == "D" else -100.0
        race.update(priorKind="uncontested", consensus={"rating": f"Safe {cands[0]['party']}" if cands else "Not rated", "margin": margin, "outlets": 0},
                    priorNote="Only one candidate is on the ballot.")
    elif cons:
        margin = cons["margin"]
        race.update(priorKind="ratings", consensus=cons,
                    priorNote=f"Average of {cons['outlets']} forecasters’ ratings, placed within each rating’s range by the {'state' if race['statewide'] else 'district'}’s partisan lean.")
    else:
        # Not on any forecaster's competitive list: all of them rate it safe for
        # the party that holds it (or the party the lean favors for a new seat).
        side = race.get("held") if race.get("held") in ("D", "R") else ("D" if (base or 0) > 0 else "R")
        sign = 1 if side == "D" else -1
        lean = base if base is not None else sign * 25
        margin = sign * max(15.0, lean * sign)
        race.update(priorKind="pvi", consensus={"rating": f"Safe {side}", "margin": round(margin, 2), "outlets": 0},
                    priorNote="Not on any forecaster’s list of competitive races, so the partisan lean (Cook PVI plus the national generic ballot) sets the baseline.")
    race["lean"] = round(margin, 2)
    race["prior"] = {k: round(v, 3) for k, v in model.prior_shares(cands, margin).items()} if cands else {}


def projected_turnout(race, votes24, states, map_index):
    st = race["state"]
    base = votes24.get(st)
    if base is None:
        base = states[st]["pop"] * 1e6 * 0.47 if st in states else 300000
    base *= MIDTERM_RATIO
    if race["office"] == "house" and not race["statewide"]:
        base /= max(1, map_index.get(st, {}).get("cd", 1))
    return int(round(base, -3))


# Research overlays ---------------------------------------------------------------

OVERLAY_FIELDS = ("turnout", "notes", "earlyVote", "format", "runoff", "open", "districtName", "statusNote")
CAND_FIELDS = ("bio", "officialSite", "donateUrl", "positions", "aliases", "caucus", "photo")


def rename_candidate(race, old, new):
    if old == new:
        return
    for p in race.get("polls", []) + race.get("finalPolls", []):
        if old in p["results"]:
            p["results"][new] = p["results"].pop(old)
    for a in race.get("aggregates", []):
        if old in a["results"]:
            a["results"][new] = a["results"].pop(old)
    if old in race.get("prior", {}):
        race["prior"][new] = race["prior"].pop(old)


def poll_key(p):
    return (re.sub(r"[^a-z]", "", p["pollster"].lower())[:10], p["end"])


def merge_overlay(race, ov, status):
    matched = set()
    for oc in ov.get("candidates", []):
        c = next((x for x in race["candidates"] if x["id"] == oc["id"]), None) or \
            el.match_candidate(oc["name"], race["candidates"], oc.get("party"))
        if c is None:
            race["candidates"].append(dict(oc))
            race.setdefault("prior", {})[oc["id"]] = 0.0
            status.warn(f"{race['id']}: researched candidate {oc['name']} is not in the automatic list; kept from research")
            continue
        rename_candidate(race, c["id"], oc["id"])
        c["id"] = oc["id"]
        matched.add(oc["id"])
        c["name"] = oc.get("name", c["name"])
        for f in CAND_FIELDS:
            if f == "positions" and oc.get("positions") is not None and c.get("positions"):
                # Researched positions add to (and win over) a member's automatic voting record.
                c["positions"] = {**c["positions"], **oc["positions"]}
            elif f in oc:
                c[f] = oc[f]
        if "incumbent" in oc:
            c["incumbent"] = oc["incumbent"]
        if oc.get("finance"):
            auto, of = c.get("finance"), oc["finance"]
            # A filed $0 has its coverage dates; a bare $0 (Wikipedia lists candidates who
            # have filed nothing that way) is no figure at all. Same rule as hasFigures in world.js.
            has_figures = bool(auto and auto.get("total") is not None and (auto["total"] > 0 or auto.get("from")))
            # The same report with its breakdown (Wikipedia dates a whole table, the FEC
            # dates each candidate's last report, so equal totals mean equal reports).
            same_report = bool(auto and auto.get("total") == of.get("total") and of.get("parts") and not auto.get("parts"))
            if of.get("total") is None:
                if not has_figures:  # a researched note stands in only until figures arrive
                    c["finance"] = of
            elif not has_figures or (of.get("asOf") or "") >= (auto.get("asOf") or "") or same_report:
                c["finance"] = of
    if ov.get("candidatesOnly"):
        # The researched list is the qualified list: drop anyone else the automatic
        # source shows (and their poll columns), and say so.
        ids = {oc["id"] for oc in ov.get("candidates", [])}
        for c in [c for c in race["candidates"] if c["id"] not in ids]:
            status.warn(f"{race['id']}: {c['name']} is listed by Wikipedia but not on the researched qualified list; left out")
            race["candidates"].remove(c)
            race.get("prior", {}).pop(c["id"], None)
            for p in race.get("polls", []) + race.get("finalPolls", []):
                p["results"].pop(c["id"], None)
    for f in OVERLAY_FIELDS:
        if f in ov:
            if f == "earlyVote" and ((race.get(f) or {}).get("asOf") or "") > (ov[f].get("asOf") or ""):
                continue  # the automatic early-vote feed is newer than the researched figure
            race[f] = ov[f]
    if not race.get("ratings") and ov.get("ratings"):
        race["ratings"], race["ratingsSource"] = ov["ratings"], ov.get("ratingsSource")
    excl = [e.lower() for e in ov.get("excludePolls", [])]
    polls = [p for p in race.get("polls", []) if not any(e in p["pollster"].lower() for e in excl)]
    keys = {poll_key(p): i for i, p in enumerate(polls)}
    for op in ov.get("polls", []):
        k = poll_key(op)
        if k in keys:
            polls[keys[k]] = op  # the researched version (sponsor, notes) wins
        else:
            polls.append(op)
    race["polls"] = sorted(polls, key=lambda p: p["end"], reverse=True)
    # Money alone doesn't make a race researched (matching needs positions), nor do
    # positions for only some candidates (`partial`, such as one challenger's).
    if not ov.get("financeOnly") and not ov.get("partial"):
        race["research"] = ov.get("researchNote", True)


def combine_overlays(a, b):
    """Two research files covering one race (say, positions in one and FEC money in
    another): b's race fields win, candidates are merged by id, positions and notes
    are pooled."""
    out = {**a, **{k: v for k, v in b.items() if k not in ("candidates", "notes")}}
    cands = {c["id"]: dict(c) for c in a.get("candidates", [])}
    for c in b.get("candidates", []):
        old = cands.get(c["id"])
        if old:
            merged = {**old, **{k: v for k, v in c.items() if v is not None}}
            if old.get("positions") and c.get("positions"):
                merged["positions"] = {**old["positions"], **c["positions"]}
            if old.get("finance") and c.get("finance") and (c["finance"].get("asOf") or "") < (old["finance"].get("asOf") or ""):
                merged["finance"] = old["finance"]  # the later report wins, as in merge_overlay
            cands[c["id"]] = merged
        else:
            cands[c["id"]] = dict(c)
    out["candidates"] = list(cands.values())
    if a.get("notes") or b.get("notes"):
        out["notes"] = (a.get("notes") or []) + (b.get("notes") or [])
    # Money alone doesn't make a race researched, nor do positions for only some of
    # its candidates (`partial`); the pair does if either file does.
    marks = lambda o: not o.get("financeOnly") and not o.get("partial")  # noqa: E731
    out.pop("financeOnly", None)
    out.pop("partial", None)
    if a.get("financeOnly") and b.get("financeOnly"):
        out["financeOnly"] = True
    elif not (marks(a) or marks(b)):
        out["partial"] = True
    return out


def load_overlays(status):
    out = {}
    folder = DATA / "research"
    for f in sorted(folder.glob("*.json"), key=lambda p: p.name.lower()) if folder.exists() else []:
        try:
            for r in json.loads(f.read_text(encoding="utf-8")).get("races", []):
                out[r["id"]] = combine_overlays(out[r["id"]], r) if r["id"] in out else r
        except Exception as e:
            status.warn(f"could not read {f.name}: {e}")
    return out


# Recorded votes ------------------------------------------------------------------

SUFFIX = re.compile(r"\s+(Jr\.?|Sr\.?|II|III|IV)$")


def attach_house_votes(races, status):
    """Every current House member on the ballot (running again, or for Senate or
    governor) gets positions from their recorded votes. Members are identified by
    the Wikipedia article their House seat links to, then matched to the Clerk's
    roll calls by state and name. Returns how many candidates got positions."""
    try:
        record = house_votes.HouseRecord()
    except Exception as e:
        status.warn(f"House roll calls unavailable: {e}")
        return 0
    seats = {r["incumbentWiki"]: r for r in races.values() if r["office"] == "house" and r.get("incumbentWiki")}
    n = 0
    for race in races.values():
        for c in race["candidates"]:
            seat = race if race["office"] == "house" and c.get("incumbent") else seats.get(c.get("wiki"))
            if not seat:
                continue
            votes = record.member_votes(seat["state"], c["name"], c["party"] if c["party"] in ("D", "R") else None)
            if not votes:
                continue
            surname = SUFFIX.sub("", c["name"]).split()[-1]
            rows = house_votes.vote_positions(surname, votes)
            if race["level"] == "state":
                rows = [r for r in rows if not r[0].startswith("def-")]  # state races don't ask foreign policy
            if rows:
                c["positions"] = {q: {"stance": st, "source": src} for q, st, src, _ in rows}
                c["positionsFrom"] = "votes"
                n += 1
    return n


# Markets -------------------------------------------------------------------------

def polymarket(slug):
    url = f"https://gamma-api.polymarket.com/events?slug={slug}"
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=30) as r:
            ev = json.loads(r.read())[0]
        for m in ev.get("markets", []):
            if "democratic party control" in m.get("question", "").lower():
                prices = json.loads(m["outcomePrices"]) if isinstance(m["outcomePrices"], str) else m["outcomePrices"]
                return {"source": "Polymarket", "pD": float(prices[0]), "url": f"https://polymarket.com/event/{slug}",
                        "volume": round(float(ev.get("volume") or 0)), "asOf": datetime.now(timezone.utc).isoformat(timespec="minutes")}
    except Exception as e:
        log("  polymarket unavailable:", e)
    return None


# Main ----------------------------------------------------------------------------

def main():
    t0 = time.time()
    status = Status()
    pages = Pages()
    map_index = json.loads((DATA / "maps" / "index.json").read_text(encoding="utf-8"))
    states = load_states()
    pages.prefetch(list(PAGES.values()))

    log("National tables")
    races, sen_html, gov_html = statewide_races(pages, status)
    house, state_pages, house_html, ratings_html = house_races(pages, status, map_index)
    races.update(house)
    generic = el.generic_ballot(wt.section_by_title(sen_html, "Generic congressional ballot aggregate polls") or "") or \
        el.generic_ballot(wt.section_by_title(house_html, "Generic congressional ballot aggregate polls") or "")
    gmargin = generic["margin"] if generic else 0.0
    if not generic:
        status.warn("generic ballot average not found; using an even national environment")
    votes24 = turnout_2024(pages)

    log("Race pages")
    finance_auto = {}
    sites = 0
    titles = [r["page"] for r in races.values() if r.get("page")]
    titles += list(state_pages.values())
    pages.prefetch(titles)
    for rid, race in sorted(races.items()):
        if race["office"] == "house" or not race.get("page"):
            continue
        h = pages.html(race["page"])
        if not h:
            status.warn(f"{rid}: page {race['page']} missing")
            continue
        refs = wt.references(h)
        fund = attach_page_data(race, h, refs, status)
        finance_auto.update(fund)
        race["sources"] = [{"title": f"Wikipedia: {pages.revs[race['page']]['title']}", "url": pages.url(race["page"])}]
        sites += attach_sites([race], el.campaign_sites(h))
    for st, title in sorted(state_pages.items()):
        h = pages.html(title)
        if not h:
            status.warn(f"House page {title} missing")
            continue
        refs = wt.references(h)
        sites += attach_sites([r for r in races.values() if r["state"] == st and r["office"] == "house"], el.campaign_sites(h))
        chunks = district_chunks(h, map_index.get(st, {}).get("cd", 0))
        for code, chunk in chunks.items():
            race = races.get(f"{st}-H-{code}")
            if not race:
                continue
            fund = attach_page_data(race, chunk, refs, status)
            finance_auto.update(fund)
            race["sources"] = [{"title": f"Wikipedia: {pages.revs[title]['title']}", "url": pages.url(title) + (f"#District_{int(code)}" if code != "00" else "")}]

    status.check("campaign-sites", "Campaign websites found", sites > 0,
                 f"{sites} candidates linked to the official campaign sites their Wikipedia race page lists")

    log("FEC")
    fec_rows, fec_info = fec.load()
    fec_matched = 0
    by_race = {}
    for row in fec_rows:
        office = row.get("office")
        st = row.get("state")
        if office == "S":
            rid = f"{st}-SEN"
        elif office == "H":
            dist = row.get("district") or "00"
            rid = f"{st}-H-{'98' if st == 'DC' else dist}"
        else:
            continue
        by_race.setdefault(rid, []).append(row)
    for rid, rows in by_race.items():
        race = races.get(rid)
        if not race:
            continue
        for row in rows:
            last, _, first = (row.get("name") or "").partition(",")
            name = f"{first.strip()} {last.strip()}".title()
            party = {"DEM": "D", "REP": "R", "LIB": "L", "GRE": "G", "IND": "I"}.get((row.get("party") or "")[:3])
            c = el.match_candidate(name, race["candidates"], party)
            if c and (row.get("receipts") or 0) > (finance_auto.get(c["id"], {}).get("_fec") or 0):
                f = fec.finance_from(row)
                f["_fec"] = row.get("receipts") or 0
                finance_auto[c["id"]] = f
                fec_matched += 1

    log("House votes")
    voted = attach_house_votes(races, status)

    log("Early vote")
    ev_states, ev_districts, ev_info = early_vote.load({st: v.get("cd", 0) for st, v in map_index.items()})
    status.check("early-vote", "Early-vote returns found", bool(ev_info.get("states")),
                 (f"{ev_info['states']} states and {ev_info['districts']} House districts from the UF Election Lab, latest {ev_info['latest']}"
                  + (f"; district files left out as incomplete: {', '.join(ev_info['partial'])}" if ev_info.get("partial") else ""))
                 if ev_info.get("ok") else ev_info.get("reason"))

    log("State legislatures")
    try:
        leg = legislature.build(votes24, log=log)
        status.check("legislatures", "State legislative races found on Wikipedia", leg["districts"] > 0,
                     f"{leg['districts']} districts in {leg['chambers']} chambers, {leg['withCandidates']} with candidates listed"
                     + (f"; no district list for {', '.join(leg['missing'])}, left to the demo set" if leg["missing"] else ""))
    except Exception as e:  # noqa: BLE001  a bad chamber page mustn't stop the federal refresh
        status.check("legislatures", "State legislative races found on Wikipedia", False, f"failed: {e}")

    log("Priors and overlays")
    overlays = load_overlays(status)
    for rid, race in races.items():
        for c in race["candidates"]:
            fin = finance_auto.get(c["id"])
            if fin:
                fin = {k: v for k, v in fin.items() if not k.startswith("_") and v is not None}
                fin.setdefault("parts", {})
                if not fin.get("source"):
                    fin["source"] = "Campaign finance reports via Wikipedia"
                c["finance"] = fin
        prominence(race, {c["id"]: c.get("finance") for c in race["candidates"]})
        set_prior(race, gmargin)
        race["turnout"] = projected_turnout(race, votes24, states, map_index)
        ev = ev_districts.get(rid) or (ev_states.get(race["state"]) if race["statewide"] else None)
        if ev:
            race["earlyVote"] = {**ev, "pctOfTurnout": round(ev["ballots"] / race["turnout"], 3) if race["turnout"] else None}
        race["auto"] = True
        if rid in overlays:
            merge_overlay(race, overlays[rid], status)
            prominence(race, {c["id"]: c.get("finance") for c in race["candidates"]})
            set_prior(race, gmargin)  # ids may have changed
    for rid in overlays:
        if rid not in races:
            status.warn(f"research overlay {rid} matches no race on the ballot")

    log("Forecasts")
    forecasts = {}
    for rid, race in races.items():
        if not race["candidates"]:
            continue
        if race.get("format") == "open-primary":
            forecasts[rid] = None
            continue
        f = model.forecast(race, NOW)
        forecasts[rid] = f
        race["modelCheck"] = {"asOf": NOW.isoformat(timespec="seconds"), "lead": f["lead"]["id"], "pLead": round(f["pLead"], 4),
                              "margin": round(f["margin"], 3), "dr": None if f["dr"] is None else round(f["dr"], 3)}

    control = chamber_control(races, forecasts, pages, status)
    run_checks(races, forecasts, control, status, generic, sen_html, gov_html, ratings_html, fec_info, fec_matched, overlays)

    # Strip build-only fields and write.
    out = []
    for rid in sorted(races, key=race_sort_key):
        r = races[rid]
        r.pop("page", None)
        r.pop("incumbentName", None)
        r.pop("statusText", None)
        r.pop("incumbentWiki", None)
        if not r.get("candidates"):
            status.warn(f"{rid}: no candidates listed; left to the demo set")
            continue
        out.append(r)
    meta = {"updated": datetime.now(timezone.utc).isoformat(timespec="seconds"), "generic": generic,
            "sources": [{"title": f"Wikipedia: {t}", "url": pages.url(t)} for t in PAGES.values() if t != PAGES["pres24"]]}
    write_json(DATA / "races.json", {"meta": meta, "races": out})
    write_json(DATA / "control.json", control)
    st = {
        "updated": meta["updated"], "nextRefreshHours": 8, "seconds": round(time.time() - t0, 1),
        "counts": {"races": len(out), "senate": sum(r["office"] == "senate" for r in out), "governor": sum(r["office"] == "governor" for r in out),
                   "house": sum(r["office"] == "house" for r in out), "withPolls": sum(bool(r.get("polls")) for r in out),
                   "polls": sum(len(r.get("polls", [])) for r in out), "rated": sum(r.get("priorKind") == "ratings" for r in out),
                   "withMoney": sum(any(c.get("finance", {}).get("total") for c in r["candidates"]) for r in out),
                   "researched": sum(bool(r.get("research")) for r in out),
                   "withVotes": voted},
        "fec": fec_info, "wikipedia": dict(wt.stats), "checks": status.checks, "warnings": status.warnings[:200],
    }
    write_json(DATA / "status.json", st)
    log(f"Done in {st['seconds']}s: {st['counts']}")
    return 0 if all(c["status"] != "fail" for c in status.checks) else 1


def race_sort_key(rid):
    order = {"SEN": 0, "GOV": 1}
    parts = rid.split("-")
    return (parts[0], order.get(parts[1], 2), parts[-1])


def write_json(path, obj):
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    tmp.replace(path)


# Chamber control -----------------------------------------------------------------

def chamber_control(races, forecasts, pages, status):
    cong = pages.html(PAGES["congress"]) or ""
    sen_now = el.party_summary(wt.section_by_title(cong, "Senate party summary") or "")
    house_now = el.party_summary(wt.section_by_title(cong, "House party summary") or "")
    if not sen_now or not house_now:
        status.warn("current party composition not found on the 119th Congress page")
    sen = [r for r in races.values() if r["office"] == "senate"]
    gov = [r for r in races.values() if r["office"] == "governor"]
    hou = [r for r in races.values() if r["office"] == "house" and r["state"] != "DC"]

    def entries(rs):
        out = []
        for r in rs:
            if not r["candidates"]:
                continue
            out.append(model.sim_entry(r, forecasts.get(r["id"])))
        return out

    result = {"updated": datetime.now(timezone.utc).isoformat(timespec="seconds"), "nat": model.NAT}
    # Senate: the vice president (a Republican) breaks ties, so Democrats need 51.
    if sen_now:
        cur_d = sen_now["D"] + (sen_now["I"] if SENATE_INDEPENDENTS_CAUCUS == "D" else 0)
        cur_r = sen_now["R"]
        up_d = sum(r["held"] == "D" for r in sen)
        up_r = sum(r["held"] == "R" for r in sen)
        hold_d, hold_r = cur_d - up_d, cur_r - up_r
        s = model.simulate_control(entries(sen), hold_d, hold_r, d_needs=51, r_needs=50)
        s.update(current={"D": cur_d, "R": cur_r, "asOf": sen_now["asOf"], "note": "Democrats include the two independents who caucus with them."},
                 holdover={"D": hold_d, "R": hold_r}, up=len(sen), seats=100, majority="Democrats need 51 seats; Republicans need 50, since the vice president breaks ties.")
        s["gainD"] = s["meanD"] - cur_d
        s["gainR"] = s["meanR"] - cur_r
        s["market"] = polymarket(POLYMARKET["senate"])
        result["senate"] = s
    if house_now:
        s = model.simulate_control(entries(hou), 0, 0, d_needs=218, r_needs=218)
        s.update(current={"D": house_now["D"], "R": house_now["R"], "I": house_now["I"], "vacant": house_now["vacant"], "asOf": house_now["asOf"]},
                 holdover={"D": 0, "R": 0}, up=len(hou), seats=435, majority="218 seats for a majority.")
        s["gainD"] = s["meanD"] - house_now["D"]
        s["gainR"] = s["meanR"] - house_now["R"]
        s["market"] = polymarket(POLYMARKET["house"])
        result["house"] = s
    hold_d, hold_r = len(GOV_HOLDOVER["D"]), len(GOV_HOLDOVER["R"])
    cur_d = hold_d + sum(r["held"] == "D" for r in gov)
    cur_r = hold_r + sum(r["held"] == "R" for r in gov)
    s = model.simulate_control(entries(gov), hold_d, hold_r, d_needs=26, r_needs=26)
    s.update(current={"D": cur_d, "R": cur_r}, holdover={"D": hold_d, "R": hold_r}, up=len(gov), seats=50,
             majority="A majority of governorships is 26.")
    s["gainD"] = s["meanD"] - cur_d
    s["gainR"] = s["meanR"] - cur_r
    s["market"] = None
    result["governor"] = s

    # Keep a history so the site can show how control odds have moved.
    prev = json.loads((DATA / "control.json").read_text(encoding="utf-8")) if (DATA / "control.json").exists() else {}
    hist = prev.get("history", [])
    point = {"t": result["updated"]}
    for k in ("senate", "house", "governor"):
        if k in result:
            point[k] = {"pD": round(result[k]["pD"], 4), "meanD": round(result[k]["meanD"], 2), "meanR": round(result[k]["meanR"], 2)}
    if hist and hist[-1]["t"][:13] == point["t"][:13]:
        hist[-1] = point  # same hour: replace rather than pile up
    else:
        hist.append(point)
    result["history"] = hist[-1000:]
    return result


# Checks --------------------------------------------------------------------------

def run_checks(races, forecasts, control, status, generic, sen_html, gov_html, ratings_html, fec_info, fec_matched, overlays):
    log("Checks")
    sen = [r for r in races.values() if r["office"] == "senate"]
    gov = [r for r in races.values() if r["office"] == "governor"]
    hou = [r for r in races.values() if r["office"] == "house"]
    status.check("counts", "Every race on the ballot was found",
                 len(sen) == 35 and len(gov) == 36 and len(hou) == 436,
                 f"{len(sen)} of 35 Senate, {len(gov)} of 36 governor, {len(hou)} of 436 House (435 + D.C.)", "fail")

    if "senate" in control:
        s = control["senate"]
        total = s["holdover"]["D"] + s["holdover"]["R"] + s["up"]
        status.check("senate-seats", "Senate seats add up to 100", total == 100,
                     f"{s['holdover']['D']} D + {s['holdover']['R']} R not up, plus {s['up']} on the ballot = {total}", "fail")
    g = control["governor"]
    status.check("gov-seats", "Governorships add up to 50", g["holdover"]["D"] + g["holdover"]["R"] + g["up"] == 50,
                 f"{g['holdover']['D'] + g['holdover']['R']} not up + {g['up']} on the ballot", "fail")

    missing = []
    for rid, r in races.items():
        f = forecasts.get(rid)
        m = r.get("lean") if f is None else (f["dr"] if f["dr"] is not None else f["margin"])
        if m is None or not math.isfinite(m):
            missing.append(rid)
    status.check("margins", "Every race has an expected margin", not missing,
                 "all races" if not missing else f"missing for {', '.join(sorted(missing)[:20])}", "fail")

    # The model's favorite against the forecasters' consensus.
    disagree = []
    for rid, r in races.items():
        f = forecasts.get(rid)
        cons = r.get("consensus") or {}
        if not f or r.get("priorKind") != "ratings" or cons.get("rating", "").startswith("Toss"):
            continue
        side = cons["rating"].split()[-1]
        if f["lead"]["party"] in ("D", "R") and f["lead"]["party"] != side and f["pLead"] > 0.6:
            disagree.append(f"{rid} (model {f['lead']['party']} {f['pLead']:.0%}, forecasters {cons['rating']})")
    status.check("consensus", "The model agrees with forecasters on who is favored", len(disagree) <= 3,
                 "no disagreements" if not disagree else
                 f"{len(disagree)} race{'' if len(disagree) == 1 else 's'} where polls point the other way: " + "; ".join(disagree[:10]))

    # Confidence: a race forecasters call close shouldn't come out a near-certainty.
    # (This catches modelling mistakes such as treating a ranked-choice race as plurality.)
    ceiling = {"Toss-up": 0.85, "Tilt": 0.85, "Lean": 0.95, "Likely": 0.995}
    overconfident = []
    for rid, r in races.items():
        f = forecasts.get(rid)
        cons = (r.get("consensus") or {}).get("rating", "")
        word = "Toss-up" if cons.startswith("Toss") else cons.split()[0] if cons else ""
        if f and r.get("priorKind") == "ratings" and word in ceiling and f["pLead"] > ceiling[word]:
            overconfident.append(f"{rid} (model {f['pLead']:.1%}, forecasters {cons})")
    status.check("confidence", "No race is far more certain in the model than forecasters rate it", not overconfident,
                 "none" if not overconfident else "; ".join(overconfident[:12]))

    # Our polling average against the aggregators' published averages.
    gaps = []
    compared = 0
    for rid, r in races.items():
        f = forecasts.get(rid)
        aggs = [a for a in r.get("aggregates", []) if not a.get("average")]
        if not f or not f["poll"] or not aggs:
            continue
        a, b = model.main_contenders(r["candidates"])
        if not b:
            continue
        theirs = [x["results"].get(a["id"], 0) - x["results"].get(b["id"], 0) for x in aggs if a["id"] in x["results"] and b["id"] in x["results"]]
        if not theirs:
            continue
        compared += 1
        ours = f["poll"]["shares"].get(a["id"], 0) - f["poll"]["shares"].get(b["id"], 0)
        avg = sum(theirs) / len(theirs)
        if abs(ours - avg) > 4:
            gaps.append(f"{rid}: ours {ours:+.1f}, aggregators {avg:+.1f}")
    status.check("pollavg", "Polling averages match the published aggregators (within 4 pts)", not gaps,
                 f"{compared} races compared" + ("" if not gaps else "; off in " + "; ".join(gaps[:10])))

    # Expected seats against each forecaster's own seat count.
    for key, html_text, sec, head in (("senate", sen_html, "Predictions", "State"), ("governor", gov_html, "Predictions", "State"), ("house", ratings_html, None, "District")):
        if key not in control:
            continue
        rows = overall_rows(html_text, sec, head)
        if not rows:
            continue
        lo = min(v["D"] for v in rows.values())
        hi = max(v["D"] + v["T"] for v in rows.values())
        mean = control[key]["meanD"]
        control[key]["forecasters"] = rows
        status.check(f"{key}-seats-vs-forecasters", f"Expected {key} seats sit within forecasters' range",
                     lo - 1 <= mean <= hi + 1, f"model {math.floor(mean + 0.5)} D; forecasters {lo} to {hi} D counting their toss-ups")

    for key in ("senate", "house"):
        c = control.get(key)
        if not c or not c.get("market"):
            continue
        diff = c["pD"] - c["market"]["pD"]
        status.check(f"{key}-market", f"{key.title()} control odds near the betting market (within 20 pts)", abs(diff) <= 0.2,
                     f"model {c['pD']:.0%} D, Polymarket {c['market']['pD']:.0%}")

    status.check("generic", "National environment found", bool(generic),
                 f"generic ballot D {generic['margin']:+.1f} (updated {generic['updated']})" if generic else "missing; assumed even")
    hand_fec = sum(1 for ov in overlays.values() for c in ov.get("candidates", [])
                   if (c.get("finance") or {}).get("source") == "FEC" and (c.get("finance") or {}).get("parts"))
    status.check("fec", "Fundraising data is current", fec_info.get("fresh", False),
                 f"{fec_matched} candidates matched to FEC filings by the API; {hand_fec} more with full breakdowns from the FEC summaries in scripts/research/fec_2026.py; {fec_info.get('note')}"
                 + (f"; last download {fec_info['fetched']}" if fec_info.get("fetched") else ""))
    stale = []
    for rid, r in races.items():
        cons = (r.get("consensus") or {}).get("rating", "")
        if r.get("priorKind") == "ratings" and r["office"] != "house" and (cons.startswith(("Toss", "Tilt", "Lean"))):
            last = max((p["end"] for p in r.get("polls", [])), default=None)
            if not last or last < (NOW - timedelta(days=30)).date().isoformat():
                stale.append(f"{rid} (last poll {last or 'none'})")
    status.check("fresh-polls", "Close statewide races have a poll from the last 30 days", not stale,
                 "all close races" if not stale else "; ".join(stale), "info")
    researched = sorted(rid for rid, ov in overlays.items() if not ov.get("financeOnly") and not ov.get("partial"))
    status.check("overlays", "Researched races merged", True,
                 f"{len(researched)} researched: {', '.join(researched) or 'none'}; {len(overlays) - len(researched)} more with FEC money only")


if __name__ == "__main__":
    sys.exit(main())
