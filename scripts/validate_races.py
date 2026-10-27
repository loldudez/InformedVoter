"""Check data/races.json before publishing it.

Catches the mistakes that would mislead a voter: unknown question ids, stances
off the five-point scale, positions without a source link, poll results for
candidates who aren't in the race or outside 0-100, baselines that don't cover
every candidate, and donation links that aren't on the campaign's own domain or
a recognized processor.

Usage:  python -I scripts/validate_races.py [path]
"""

import json
import math
import re
import sys
from datetime import date
from urllib.parse import urlparse

QUESTION_FILE = "js/data/questions.js"
PROCESSORS = {"secure.actblue.com", "secure.winred.com", "secure.anedot.com"}
OFFICES = {"senate", "governor", "house", "state-senate", "state-house", "legislature"}


def question_ids():
    """Rebuild the question ids from questions.js (category prefix + position)."""
    src = open(QUESTION_FILE, encoding="utf-8").read()
    ids = set()
    for cat, body in re.findall(r"\['(\w{3})', '[^']*', '\w+', \[(.*?)\n  \]\]", src, re.S):
        count = len(re.findall(r"^\s*\['Do you", body, re.M))
        ids.update(f"{cat}-{i:02d}" for i in range(1, count + 1))
    return ids


def finite(x):
    return isinstance(x, (int, float)) and math.isfinite(x)


def is_day(s):
    try:
        date.fromisoformat(s)
        return True
    except (TypeError, ValueError):
        return False


def main(path):
    data = json.load(open(path, encoding="utf-8"))
    qids = question_ids()
    errors, warnings = [], []
    no_url = 0
    for race in data.get("races", []):
        rid = race.get("id", "?")
        if race.get("office") not in OFFICES:
            errors.append(f"{rid}: unknown office {race.get('office')!r}")
        cands = [c["id"] for c in race.get("candidates", [])]
        if not cands:
            errors.append(f"{rid}: no candidates")
        if len(set(cands)) != len(cands):
            errors.append(f"{rid}: duplicate candidate ids")
        prior = race.get("prior")
        if prior is not None:
            missing = [c for c in cands if not finite(prior.get(c))]
            if missing:
                errors.append(f"{rid}: baseline share missing for {', '.join(missing)}")
            elif abs(sum(prior[c] for c in cands) - 100) > 0.5:
                errors.append(f"{rid}: baseline shares add up to {sum(prior[c] for c in cands):.1f}, not 100")
        if "lean" in race and not finite(race["lean"]):
            errors.append(f"{rid}: expected margin (lean) is not a number")
        for c in race.get("candidates", []):
            cid = c["id"]
            if not cid.startswith(rid + ":"):
                errors.append(f"{cid}: candidate id must start with '{rid}:'")
            if not c.get("name") or not c.get("party"):
                errors.append(f"{cid}: candidate needs a name and party")
            for qid, pos in (c.get("positions") or {}).items():
                if qid not in qids:
                    errors.append(f"{cid}: unknown question id {qid}")
                if pos.get("stance") not in (-2, -1, 0, 1, 2):
                    errors.append(f"{cid} {qid}: stance must be -2..2")
                src = pos.get("source") or {}
                if not src.get("url", "").startswith("https://") or not src.get("title"):
                    errors.append(f"{cid} {qid}: every position needs a source title and https url")
                if race.get("level") == "federal" and qid.startswith("sta-"):
                    warnings.append(f"{cid} {qid}: state-and-local question on a federal race is never asked")
                if race.get("level") == "state" and qid.startswith("def-"):
                    warnings.append(f"{cid} {qid}: foreign-policy question on a state race is never asked")
            fin = c.get("finance")
            if fin and not (finite(fin.get("total")) and fin["total"] >= 0):
                errors.append(f"{cid}: fundraising total is not a number")
            if c.get("donateUrl"):
                u, site = urlparse(c["donateUrl"]), urlparse(c.get("officialSite") or "")
                own = site.hostname and (u.hostname == site.hostname.removeprefix("www.") or u.hostname.endswith("." + site.hostname.removeprefix("www.")) or u.hostname == site.hostname)
                if u.scheme != "https" or not (own or u.hostname in PROCESSORS):
                    errors.append(f"{cid}: donation link {c['donateUrl']} is not on the official domain or a known processor (it will be hidden)")
        for p in race.get("polls", []):
            who = f"{rid}: poll by {p.get('pollster')}"
            if not is_day(p.get("end")) or (p.get("start") and not is_day(p["start"])):
                errors.append(f"{who} has a bad date")
            if p.get("n") is not None and not (isinstance(p["n"], int) and p["n"] > 0):
                errors.append(f"{who} has a bad sample size {p.get('n')!r}")
            for k, v in p.get("results", {}).items():
                if k not in cands:
                    errors.append(f"{who} has a result for unknown candidate {k}")
                if not finite(v) or not 0 <= v <= 100:
                    errors.append(f"{who} has a result outside 0-100: {v!r}")
            if sum(v for v in p.get("results", {}).values() if finite(v)) > 102:
                errors.append(f"{who} adds up to more than 100%")
            if not p.get("url"):
                no_url += 1
    for w in warnings:
        print("warning:", w)
    if no_url:
        print(f"note: {no_url} poll(s) have no source link")
    for e in errors:
        print("ERROR:", e)
    n = sum(len(c.get("positions") or {}) for r in data.get("races", []) for c in r.get("candidates", []))
    print(f"{len(data.get('races', []))} races, {n} positions checked against {len(qids)} questions: {'OK' if not errors else f'{len(errors)} error(s)'}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "data/races.json"))
