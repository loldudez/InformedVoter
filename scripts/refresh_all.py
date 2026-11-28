"""Run every data refresh in order. Windows Task Scheduler runs this every 8 hours
(see README: "Automatic refresh"); it can also be run by hand:

    py scripts/refresh_all.py

1. News headlines (every run).
2. Inflation series (once a day; BLS publishes monthly).
3. The research overlays in scripts/research/ (cheap, so edits there are picked up).
4. Every race, the forecasts and chamber control (update_races.py).
5. The validator. If the new race data fails it, the previous race, control and
   status files are put back, so the site never shows a broken refresh.
   Then who sits in Congress (update_congress.py), the candidates' photos
   (update_photos.py), the elections of the next three years (update_upcoming.py), the
   2028 presidential field (update_president_2028.py),
   the statewide officers, caucuses and senators' votes (update_officeholders.py) and
   the state legislators whose seats weren't up (update_legislators.py), once a day;
   each keeps its previous file when a source can't be read.
6. The France section (scripts/fr/): the presidential candidates and polls, the
   parties, who sits in Parliament and the figures behind "Les grands enjeux" once a
   day, the election calendar and the candidates' researched positions every run. Its
   own files, kept apart from step 5.
7. The elections the mail service may send reminders for (update_reminders.py, no
   network), every run.
8. Publishing: every data file that changed goes to the live site (publish.py, when
   this computer is set up to publish; README, "Publishing from this computer").

"Once a day" means the step's file is over 20 hours old (INFORMED_VOTER_DAILY_HOURS)
by the time written inside it (`written_at`), not by when the file was saved: the cloud
workflow's checkout dates every file at the checkout. In the cloud a time budget
(INFORMED_VOTER_BUDGET_MINUTES) leaves the steps it can't reach for the next run.

Each run is appended to data/cache/refresh.log.
"""

import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
LOG = DATA / "cache" / "refresh.log"
PY = sys.executable.replace("pythonw.exe", "python.exe")  # child scripts print; give them a console interpreter
GUARDED = ["races.json", "offices.json", "control.json", "status.json"]
LOCK = DATA / "cache" / "refresh.lock"  # shared with update_results.py, which writes the same files
STEP_MINUTES = int(os.environ.get("INFORMED_VOTER_STEP_MINUTES") or 30)
# The once-a-day steps run when their file is older than this. The cloud workflow, which
# refreshes about every 16 hours, sets 12 so each of its runs rebuilds them.
DAILY_HOURS = float(os.environ.get("INFORMED_VOTER_DAILY_HOURS") or 20)
# The cloud job's time limit, less the time it needs to save its cache and commit: past
# it, the remaining steps wait for the next run, since a job stopped at its limit commits
# nothing. None on this computer.
BUDGET = float(os.environ.get("INFORMED_VOTER_BUDGET_MINUTES") or 0) * 60 or None
START = time.time()


def log(msg):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    line = f"{datetime.now().isoformat(timespec='seconds')}  {msg}"
    with LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    try:
        print(line, flush=True)
    except Exception:
        pass  # no console when run by the scheduler


def run(args, timeout=None):
    """Run one script; False when it fails or outlasts its time (30 minutes here,
    INFORMED_VOTER_STEP_MINUTES in the cloud workflow, whose cache can be colder), or
    when the cloud run's budget leaves it no time."""
    timeout = timeout or STEP_MINUTES * 60
    if BUDGET:
        left = BUDGET - (time.time() - START)
        if left < 5 * 60:
            log(f"SKIP {' '.join(args)}: {max(left, 0) / 60:.0f} minutes left of this run's "
                f"{BUDGET / 60:.0f}; it runs next time")
            return False
        timeout = min(timeout, int(left))
    t0 = time.time()
    try:
        p = subprocess.run([PY, *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace",
                           timeout=timeout, env={**os.environ, "PYTHONIOENCODING": "utf-8"},
                           creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))  # no console flashes when scheduled
    except subprocess.TimeoutExpired:
        # A timeout is a failed step, not a crash: the guarded race files are put back.
        log(f"FAIL {' '.join(args)} stopped after {timeout // 60} minutes")
        return False
    tail = " | ".join((p.stdout or "").strip().splitlines()[-2:])
    log(f"{'ok  ' if p.returncode == 0 else 'FAIL'} {' '.join(args)} ({time.time() - t0:.0f}s) {tail}")
    if p.returncode != 0 and p.stderr:
        log("     " + " | ".join(p.stderr.strip().splitlines()[-4:]))
    return p.returncode == 0


def take_lock(wait_minutes=15, stale_minutes=45):
    """Wait for a results refresh (update_results.py) to finish writing, then hold the
    lock while the race files are rebuilt. A lock older than `stale_minutes` is left from
    a run that died."""
    LOCK.parent.mkdir(parents=True, exist_ok=True)
    deadline = time.time() + wait_minutes * 60
    while True:
        try:
            fd = os.open(LOCK, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            with os.fdopen(fd, "w") as f:
                f.write(f"refresh_all {os.getpid()} {datetime.now().isoformat(timespec='seconds')}\n")
            return
        except FileExistsError:
            if time.time() - LOCK.stat().st_mtime > stale_minutes * 60 or time.time() > deadline:
                LOCK.unlink(missing_ok=True)
                continue
            time.sleep(15)


def written_at(path):
    """When a data file was last built: the time it records inside ("updated", or
    "meta"/"updated" for France's polls), else its modification time. The cloud
    workflow's checkout gives every file the time of the checkout, so judged by that
    alone the once-a-day files always looked new there and were never rebuilt (Nov. 5 to
    27, 2026). Stamps in data/cache keep their times, since the workflow saves the cache."""
    if path.suffix == ".json":
        try:
            d = json.loads(path.read_text(encoding="utf-8"))
            stamp = (d.get("updated") or (d.get("meta") or {}).get("updated")) if isinstance(d, dict) else None
            if isinstance(stamp, str):
                t = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
                return (t if t.tzinfo else t.replace(tzinfo=timezone.utc)).timestamp()
        except (OSError, ValueError, AttributeError):
            pass
    return path.stat().st_mtime


def older_than(path, hours):
    return not path.exists() or (time.time() - written_at(path)) > hours * 3600


def trim_log(max_lines=4000):
    if LOG.exists():
        lines = LOG.read_text(encoding="utf-8").splitlines()
        if len(lines) > max_lines:
            LOG.write_text("\n".join(lines[-max_lines:]) + "\n", encoding="utf-8")


def guarded_races(backup):
    """Rebuild the race files and validate them; put the last good ones back on failure."""
    for name in GUARDED:
        if (DATA / name).exists():
            shutil.copy2(DATA / name, backup / name)
    ok = run(["scripts/update_races.py"]) and run(["-I", "scripts/validate_races.py"])
    if not ok:
        for name in GUARDED:
            if (backup / name).exists():
                shutil.copy2(backup / name, DATA / name)
        # Say so on the site: the status page shows the last good data and this failure.
        st_path = DATA / "status.json"
        if st_path.exists():
            st = json.loads(st_path.read_text(encoding="utf-8"))
            # One note for the latest failure: the restored file already carries the last
            # run's, and they piled up (23 on the live site by Nov. 27, 2026).
            st["checks"] = [c for c in st.get("checks", []) if c.get("id") != "refresh-failed"]
            st["checks"].insert(0, {
                "id": "refresh-failed", "label": "Latest refresh failed; showing the previous data", "status": "fail",
                "detail": f"The refresh at {datetime.now(timezone.utc).isoformat(timespec='minutes')} did not pass its checks (see data/cache/refresh.log). The last good data is shown.",
            })
            st_path.write_text(json.dumps(st, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        log("race data restored from the last good refresh")
    return ok


def main():
    log("refresh started")
    run(["scripts/update_news.py"])
    if older_than(DATA / "inflation.json", DAILY_HOURS):
        run(["scripts/update_inflation.py"])
    for script in sorted((ROOT / "scripts" / "research").glob("*.py")):
        if script.name != "common.py":
            run([str(script.relative_to(ROOT))])

    backup = DATA / "cache" / "last-good"
    backup.mkdir(parents=True, exist_ok=True)
    take_lock()
    try:
        ok = guarded_races(backup)
    finally:
        LOCK.unlink(missing_ok=True)
    if older_than(DATA / "congress.json", DAILY_HOURS):                      # who sits in Congress: once a day
        ok &= run(["scripts/update_congress.py"])
    if older_than(DATA / "photos.json", DAILY_HOURS):                        # candidates' photos: once a day
        ok &= run(["scripts/update_photos.py"])
    if older_than(DATA / "upcoming.json", DAILY_HOURS):                      # the elections of 2027-2029: once a day
        ok &= run(["scripts/update_upcoming.py"])
    if older_than(DATA / "president-2028.json", DAILY_HOURS):                # the 2028 presidential field: once a day
        ok &= run(["scripts/update_president_2028.py"])
    if older_than(DATA / "officeholders.json", DAILY_HOURS):                 # statewide officers, caucuses, senators' votes: once a day
        ok &= run(["scripts/update_officeholders.py"])
    if older_than(DATA / "cache" / "legislators.stamp", DAILY_HOURS):        # state legislators from Open States: once a day
        ok &= run(["scripts/update_legislators.py"])

    # The France section (data/fr/): separate files, so a failure here never touches the
    # U.S. data; each script keeps its previous file when it can't build a new one.
    fr_ok = True
    if older_than(DATA / "fr" / "presidentielle-2027.json", DAILY_HOURS):    # candidates and polls: once a day
        fr_ok &= run(["scripts/fr/update_presidentielle.py"])
    if older_than(DATA / "fr" / "partis.json", DAILY_HOURS):                 # parties and leaders: once a day
        fr_ok &= run(["scripts/fr/partis.py"])
    if older_than(DATA / "fr" / "parlement.json", DAILY_HOURS):              # who sits in Parliament: once a day
        fr_ok &= run(["scripts/fr/parlement.py"])
    if older_than(DATA / "fr" / "enjeux.json", DAILY_HOURS):                 # "Les grands enjeux" figures: once a day
        fr_ok &= run(["scripts/fr/enjeux.py"])
    fr_ok &= run(["scripts/fr/calendrier.py"])
    fr_ok &= run(["scripts/fr/positions_2027.py"])                  # hand research; no network
    ok &= run(["scripts/update_reminders.py"])                      # what email reminders may cover; no network
    run(["scripts/publish.py"])  # the new data to the live site, when this computer publishes (README)
    trim_log()
    log("refresh finished" + ("" if ok and fr_ok else " with errors"))
    return 0 if ok and fr_ok else 1


if __name__ == "__main__":
    sys.exit(main())
