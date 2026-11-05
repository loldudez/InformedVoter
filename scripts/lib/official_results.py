"""Official vote counts read straight from the states that publish them in a form a
script can read, ahead of the Wikipedia results boxes (which copy them by hand, often
hours later).

California: the Secretary of State's results API (api.sos.ca.gov/returns/..., the JSON
behind electionresults.sos.ca.gov) for every U.S. House district, governor and the
statewide offices below governor. Its counts are unofficial until the state certifies
them, and they keep growing for weeks: California counts mail ballots postmarked by
Election Day that arrive within seven days. The API's "precincts reporting" is not the
share of ballots counted (every precinct reports on election night, the mail ballots
come after), so it is not used as one.

    load()            {race_id: {"rows", "total", "asOf", "source"}}, or {} when the
                      API can't be read (the cached copy from the last good read is
                      used when the state hasn't posted an update since)
    apply(race, off)  the official count in place of the race page's; the call stays
                      the one Wikipedia's national table check-marks

The state posts all its contests at once, so one request (the governor's race) tells
whether anything changed since the last read; only then are the rest fetched.
"""

import json
import re
import time
import urllib.request
from datetime import datetime
from pathlib import Path

import results

ROOT = Path(__file__).resolve().parents[2]
CACHE = ROOT / "data" / "cache" / "official"
UA = "InformedVoterResearch/1.0"
CA_API = "https://api.sos.ca.gov/returns/"
CA_PAGE = "https://electionresults.sos.ca.gov/returns/"
CA_HOUSE_SEATS = 52
CA_OFFICES = {  # race id -> the API's path
    "CA-GOV": "governor",
    "CA-LG": "lieutenant-governor",
    "CA-SOS": "secretary-of-state",
    "CA-AUD": "controller",
    "CA-TREAS": "treasurer",
    "CA-AG": "attorney-general",
}
CA_PARTY = {"Dem": "D", "Rep": "R", "Lib": "L", "Grn": "G", "NPP": "I", "PF": "PF", "AI": "AI"}
MONTHS = {m: i for i, m in enumerate(("January", "February", "March", "April", "May", "June", "July", "August",
                                      "September", "October", "November", "December"), 1)}


def _get(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def _num(s):
    s = re.sub(r"[^\d.]", "", str(s or ""))
    return float(s) if s else None


def pacific_iso(text):
    """'November 4, 2026, 5:18 p.m.' (Pacific time) -> '2026-11-04T17:18:00-08:00'.
    Daylight time ended on Nov. 1, 2026, before Election Day, so every count after it
    is posted in standard time (UTC-8)."""
    m = re.match(r"(\w+) (\d+), (\d{4}),? (\d+):(\d\d) ([ap])\.?m\.?", (text or "").strip(), re.I)
    if not m or m.group(1) not in MONTHS:
        return None
    hour = int(m.group(4)) % 12 + (12 if m.group(6).lower() == "p" else 0)
    dt = datetime(int(m.group(3)), MONTHS[m.group(1)], int(m.group(2)), hour, int(m.group(5)))
    return dt.isoformat(timespec="seconds") + "-08:00"


def _ca_race(rid, path, data):
    rows = []
    for c in data.get("candidates") or []:
        votes = _num(c.get("Votes"))
        rows.append({"name": " ".join(str(c.get("Name") or "").split()), "party": CA_PARTY.get(c.get("Party"), "I"),
                     "votes": votes, "pct": _num(c.get("Percent")), "incumbent": bool(c.get("incumbent"))})
    rows = [r for r in rows if r["name"]]
    if not rows or not any(r["votes"] for r in rows):
        return None
    return {"rows": rows, "total": sum(r["votes"] or 0 for r in rows), "asOf": pacific_iso(data.get("ReportingTime")),
            "reportingTime": data.get("ReportingTime"),
            "source": {"title": "California Secretary of State: unofficial election results", "url": CA_PAGE + path}}


def load_california(log=print):
    CACHE.mkdir(parents=True, exist_ok=True)
    cache_path = CACHE / "ca.json"
    cached = json.loads(cache_path.read_text(encoding="utf-8")) if cache_path.exists() else {}
    paths = {f"CA-H-{n:02d}": f"us-rep/district/{n}" for n in range(1, CA_HOUSE_SEATS + 1)}
    paths.update(CA_OFFICES)
    try:
        probe = _get(CA_API + CA_OFFICES["CA-GOV"])
    except Exception as e:  # noqa: BLE001  the state's server is down or refused: keep the last read
        log(f"  California results API unreadable ({e}); {'using the last read' if cached.get('races') else 'no counts'}")
        return cached.get("races") or {}, {"ok": False, "reason": str(e), "asOf": cached.get("asOf")}
    stamp = probe.get("ReportingTime")
    if cached.get("reportingTime") == stamp and cached.get("races"):
        return cached["races"], {"ok": True, "changed": False, "asOf": cached.get("asOf"), "races": len(cached["races"])}
    out, failed = {}, []
    for rid, path in paths.items():
        try:
            data = probe if rid == "CA-GOV" else _get(CA_API + path)
        except Exception:  # noqa: BLE001
            failed.append(rid)
            if rid in (cached.get("races") or {}):
                out[rid] = cached["races"][rid]
            continue
        race = _ca_race(rid, path, data)
        if race:
            out[rid] = race
        time.sleep(0.3)
    as_of = pacific_iso(stamp)
    if out and not failed:
        cache_path.write_text(json.dumps({"reportingTime": stamp, "asOf": as_of, "races": out}, ensure_ascii=False), encoding="utf-8")
    log(f"  California: {len(out)} contests, posted {stamp}" + (f"; {len(failed)} unreadable" if failed else ""))
    return out, {"ok": not failed, "changed": True, "asOf": as_of, "races": len(out), "failed": failed}


def load(log=print):
    """Every state's official counts this module reads, by race id, and what was read."""
    ca, info = load_california(log)
    return dict(ca), {"CA": info}


def apply(race, off):
    """Put the official count in the race's result. Returns True when it did: at least
    the two leading candidates of the count must match the race's candidates by name."""
    cands = race["candidates"]
    rows, matched = [], 0
    for r in sorted(off["rows"], key=lambda r: -(r["votes"] or 0)):
        c = results.match(r["name"], cands, r["party"] if r["party"] in ("D", "R") else None)
        if c and any(x["id"] == c["id"] for x in rows):
            c = None
        if c and len(rows) < 2:
            matched += 1
        rows.append({"id": c["id"] if c else None, "name": c["name"] if c else r["name"],
                     "party": c["party"] if c else r["party"], "votes": r["votes"], "pct": r["pct"]})
    if matched < min(2, len(off["rows"])):
        return False
    total = off["total"] or sum(r["votes"] or 0 for r in rows)
    for r in rows:
        if r["votes"] is not None and total:
            r["pct"] = round(100 * r["votes"] / total, 2)
    res = dict(race.get("result") or {"status": "counting"})
    for k in ("reporting", "precincts", "sharesFromVotes", "via", "totalFromShares"):
        res.pop(k, None)
    res.update(rows=rows, total=total, source=off["source"], countAsOf=off["asOf"], official=True)
    race["result"] = res
    return True


def apply_all(race_map, offs):
    """Apply every official count that matches a race; the ids it applied and those it
    couldn't match."""
    done, unmatched = [], []
    for rid, off in offs.items():
        race = race_map.get(rid)
        if not race or not race.get("candidates"):
            continue
        (done if apply(race, off) else unmatched).append(rid)
    return done, unmatched
