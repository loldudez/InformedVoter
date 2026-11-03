"""Write data/reminders.json: the elections the site offers email reminders for, with
the names and dates the site shows. The mail service (services/mail/Code.gs) reads
this file from the live site, so the emails it sends carry the site's own names and
dates, never text a browser sent it.

Only elections with a fixed day are listed: the U.S. general election and the runoffs
in data/races.json, and the French elections in data/fr/calendrier.json whose dates
are set ("fixed"; a deadline such as the legislative elections' "au plus tard" isn't).
Elections already over are left out. No network; scripts/refresh_all.py runs it every
time.

    py scripts/update_reminders.py
"""

import json
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "lib"))
from elections import STATE_NAME  # noqa: E402

DATA = ROOT / "data"
OUT = DATA / "reminders.json"
# The ids and names the site's reminder buttons use (js/views/elections.js).
US_GENERAL = ("us:general-2026", "Election Day, November 3, 2026", "2026-11-03")


def us_elections():
    gid, name, day = US_GENERAL
    out = {gid: {"section": "us", "page": "#/elections", "rounds": [{"date": day, "name": {"en": name}}]}}
    races = json.loads((DATA / "races.json").read_text(encoding="utf-8"))
    for r in races["races"] if isinstance(races, dict) else races:
        if r.get("runoff"):
            out[f"us:runoff-{r['state']}-{r['runoff']}"] = {
                "section": "us", "page": "#/elections",
                "rounds": [{"date": r["runoff"], "name": {"en": f"{STATE_NAME[r['state']]} runoff"}}]}
    return out


def fr_elections():
    cal = json.loads((DATA / "fr" / "calendrier.json").read_text(encoding="utf-8"))
    out = {}
    for e in cal["elections"]:
        if e.get("status") != "fixed" or not e.get("date"):
            continue
        n = e["name"]
        if e.get("round2"):
            rounds = [{"date": e["date"], "name": {"fr": f"{n['fr']}, 1er tour", "en": f"{n['en']}, round 1"}},
                      {"date": e["round2"], "name": {"fr": f"{n['fr']}, 2nd tour", "en": f"{n['en']}, round 2"}}]
        else:
            rounds = [{"date": e["date"], "name": {"fr": n["fr"], "en": n["en"]}}]
        out[f"fr:{e['id']}"] = {"section": "fr", "page": f"#/fr/calendrier?e={e['id']}", "rounds": rounds}
    return out


def main():
    today = date.today().isoformat()
    elections = {**us_elections(), **fr_elections()}
    for eid, e in list(elections.items()):
        assert re.fullmatch(r"(us|fr):[\w-]+", eid), eid
        assert all(re.fullmatch(r"\d{4}-\d{2}-\d{2}", r["date"]) for r in e["rounds"]), eid
        if e["rounds"][-1]["date"] < today:
            del elections[eid]
    OUT.write_text(json.dumps({"updated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                               "elections": elections}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}: {len(elections)} elections ({', '.join(elections)})")


if __name__ == "__main__":
    main()
