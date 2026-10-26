"""Early-vote returns from the University of Florida Election Lab's 2026 tracker
(Michael McDonald), which compiles each state's official reports: ballots cast
before Election Day, mail ballots returned, in-person early votes and, where voters
register by party, the registration split of those voters (not how they voted).

https://election.lab.ufl.edu/early-vote/2026-early-voting/ is published under CC
BY-NC-ND 4.0: attribution is required and commercial use isn't allowed. Every Early
vote tab names the Lab and links its tracker and the state's own source.

District totals come from the Lab's county-by-district files. A state's districts are
used only when the file covers every district and at least 98% of the state's ballots;
California, Connecticut, Idaho and Nevada had partial files when this was written.
"""

import csv
import io
import re
import urllib.error
import urllib.request
from collections import defaultdict
from datetime import datetime

BASE = "https://election.lab.ufl.edu/data-downloads/earlyvote/2026/"
PAGE = "https://election.lab.ufl.edu/early-vote/2026-early-voting/"
UA = "InformedVoter/1.0 (personal election-information site; data refresh script)"
SOURCE = {"title": "UF Election Lab 2026 early vote tracker (Michael McDonald)", "url": PAGE}
# Same list as PARTY_REGISTRATION in js/data/states.js.
PARTY_REGISTRATION = set("AK AZ CA CO CT DE DC FL IA ID KS KY LA ME MD MA NE NV NH NJ NM NY NC OK OR PA RI SD UT WV WY".split())
MIN_COVERAGE = 0.98


def _get(url):
    """The CSV's text, or None when the Lab has no such file (it answers with a web page)."""
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60) as r:
            text = r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError:
        return None
    return None if text.lstrip().startswith("<") else text


def _num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0


def _date(mdy):
    try:
        return datetime.strptime(mdy.strip(), "%m/%d/%Y").strftime("%Y-%m-%d")
    except (AttributeError, ValueError):
        return None


# The Lab's notes on each state's data are long and technical; only the points that
# change what the shown figures mean become a short caveat, in our own words.
CAVEATS = [
    (r"St\. Louis County only", "Covers St. Louis County only."),
    (r"In-person early voting is not yet included", "Mail ballots only; in-person early votes aren't included yet."),
    (r"\b(estimated|approximated)\b", "The split between mail and in-person ballots is an estimate."),
]


def _caveat(notes, mail, inperson):
    out = [text for pat, text in CAVEATS if re.search(pat, notes or "")]
    if mail <= 0 and inperson > 0:
        out.append("In-person early votes only; mail ballots aren't reported yet.")
    return " ".join(out) or None


def _by_party(st, ballots, d, r, other):
    """Registration shares in percent, only where the state registers voters by party and
    the three groups account for the ballots."""
    if st not in PARTY_REGISTRATION or ballots <= 0 or d + r <= 0 or abs(d + r + other - ballots) > 0.01 * ballots:
        return None
    return {"D": round(100 * d / ballots, 1), "R": round(100 * r / ballots, 1), "other": round(100 * other / ballots, 1)}


def _totals(row):
    mail, inperson = _num(row.get("accept_all")), _num(row.get("inperson_all"))
    ballots = _num(row.get("voted_all")) or mail + inperson
    return ballots, mail, inperson


def _entry(st, ballots, mail, inperson, d, r, other, as_of, caveat, state_source):
    out = {"ballots": int(round(ballots)), "asOf": as_of, "byParty": _by_party(st, ballots, d, r, other),
           "source": dict(SOURCE), "auto": True}  # refreshed with the races, not researched by hand
    # A zero beside a positive total usually means "not reported", so the split is
    # shown only when the state reports both kinds of ballots.
    if mail > 0 and inperson > 0:
        out["mail"], out["inPerson"] = int(round(mail)), int(round(inperson))
    if caveat:
        out["caveat"] = caveat
    if state_source and state_source.startswith("http"):
        out["stateSource"] = state_source
    return out


def load(n_districts):
    """({state: entry}, {"ST-H-NN": entry}, info). n_districts: {state: number of House seats}."""
    text = _get(BASE + "US.csv")
    if not text:
        return {}, {}, {"ok": False, "reason": "the Election Lab's US.csv could not be read"}
    states, districts, partial = {}, {}, []
    for row in csv.DictReader(io.StringIO(text)):
        st = (row.get("state_abbv") or "").strip()
        ballots, mail, inperson = _totals(row)
        if not st or ballots <= 0:
            continue
        as_of = _date(row.get("last_update"))
        e = _entry(st, ballots, mail, inperson, _num(row.get("voted_dem")), _num(row.get("voted_rep")),
                   _num(row.get("voted_none")), as_of, _caveat(row.get("notes"), mail, inperson), row.get("data_source"))
        if _num(row.get("turn_2022")) > 0:
            e["of2022"] = round(ballots / _num(row.get("turn_2022")), 4)
        states[st] = e
        n = n_districts.get(st, 0)
        if n > 1:
            got = _districts(st, n, ballots, as_of)
            if got is None:
                partial.append(st)
            else:
                districts.update(got)
    return states, districts, {"ok": True, "states": len(states), "districts": len(districts), "partial": partial,
                               "latest": max((e["asOf"] for e in states.values() if e.get("asOf")), default=None)}


def _districts(st, n, state_ballots, as_of):
    text = _get(f"{BASE}{st}_cd.csv")
    if not text:
        return {}
    sums = defaultdict(lambda: defaultdict(float))
    for row in csv.DictReader(io.StringIO(text)):
        m = re.search(r"\d+", str(row.get("cd") or ""))
        if not m:
            continue  # rows the Lab couldn't place in a district
        code = f"{int(m.group(0)):02d}"
        ballots, mail, inperson = _totals(row)
        s = sums[code]
        s["ballots"] += ballots
        s["mail"] += mail
        s["inperson"] += inperson
        for k in ("voted_dem", "voted_rep", "voted_none"):
            s[k] += _num(row.get(k))
    codes = {f"{i:02d}" for i in range(1, n + 1)}
    covered = sum(sums[c]["ballots"] for c in codes if c in sums)
    if not codes <= set(sums) or covered < MIN_COVERAGE * state_ballots:
        return None
    out = {}
    for c, t in sums.items():
        if c in codes:
            out[f"{st}-H-{c}"] = _entry(st, t["ballots"], t["mail"], t["inperson"], t["voted_dem"], t["voted_rep"], t["voted_none"],
                                       as_of, None, None)
            out[f"{st}-H-{c}"]["note"] = "District totals add up the Election Lab's county-by-district figures."
    return out
