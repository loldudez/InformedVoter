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
   (update_photos.py) and the elections of the next three years (update_upcoming.py),
   once a day; each keeps its previous file when a source can't be read.
6. The France section (scripts/fr/): the presidential candidates and polls, the
   parties, who sits in Parliament and the figures behind "Les grands enjeux" once a
   day, the election calendar and the candidates' researched positions every run. Its
   own files, kept apart from step 5.
7. The elections the mail service may send reminders for (update_reminders.py, no
   network), every run.
8. Publishing: every data file that changed goes to the live site (publish.py, when
   this computer is set up to publish; README, "Publishing from this computer").

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
    INFORMED_VOTER_STEP_MINUTES in the cloud workflow, whose cache can be colder)."""
    timeout = timeout or STEP_MINUTES * 60
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


def older_than(path, hours):
    return not path.exists() or (time.time() - path.stat().st_mtime) > hours * 3600


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
            st.setdefault("checks", []).insert(0, {
                "id": "refresh-failed", "label": "Latest refresh failed; showing the previous data", "status": "fail",
                "detail": f"The refresh at {datetime.now(timezone.utc).isoformat(timespec='minutes')} did not pass its checks (see data/cache/refresh.log). The last good data is shown.",
            })
            st_path.write_text(json.dumps(st, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        log("race data restored from the last good refresh")
    return ok


def main():
    log("refresh started")
    run(["scripts/update_news.py"])
    if older_than(DATA / "inflation.json", 20):
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
    if older_than(DATA / "congress.json", 20):                     # who sits in Congress: once a day
        ok &= run(["scripts/update_congress.py"])
    if older_than(DATA / "photos.json", 20):                       # candidates' photos: once a day
        ok &= run(["scripts/update_photos.py"])
    if older_than(DATA / "upcoming.json", 20):                     # the elections of 2027-2029: once a day
        ok &= run(["scripts/update_upcoming.py"])

    # The France section (data/fr/): separate files, so a failure here never touches the
    # U.S. data; each script keeps its previous file when it can't build a new one.
    fr_ok = True
    if older_than(DATA / "fr" / "presidentielle-2027.json", 20):   # candidates and polls: once a day
        fr_ok &= run(["scripts/fr/update_presidentielle.py"])
    if older_than(DATA / "fr" / "partis.json", 20):                # parties and leaders: once a day
        fr_ok &= run(["scripts/fr/partis.py"])
    if older_than(DATA / "fr" / "parlement.json", 20):             # who sits in Parliament: once a day
        fr_ok &= run(["scripts/fr/parlement.py"])
    if older_than(DATA / "fr" / "enjeux.json", 20):                # "Les grands enjeux" figures: once a day
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
