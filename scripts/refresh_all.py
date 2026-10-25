"""Run every data refresh in order. Windows Task Scheduler runs this every 8 hours
(see README: "Automatic refresh"); it can also be run by hand:

    py scripts/refresh_all.py

1. News headlines (every run).
2. Inflation series (once a day; BLS publishes monthly).
3. The research overlays in scripts/research/ (cheap, so edits there are picked up).
4. Every race, the forecasts and chamber control (update_races.py).
5. The validator. If the new race data fails it, the previous race, control and
   status files are put back, so the site never shows a broken refresh.

Each run is appended to data/cache/refresh.log.
"""

import json
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
GUARDED = ["races.json", "control.json", "status.json"]


def log(msg):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    line = f"{datetime.now().isoformat(timespec='seconds')}  {msg}"
    with LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    try:
        print(line, flush=True)
    except Exception:
        pass  # no console when run by the scheduler


def run(args, timeout=1800):
    t0 = time.time()
    p = subprocess.run([PY, *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace",
                       timeout=timeout, env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8"},
                       creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))  # no console flashes when scheduled
    tail = " | ".join((p.stdout or "").strip().splitlines()[-2:])
    log(f"{'ok  ' if p.returncode == 0 else 'FAIL'} {' '.join(args)} ({time.time() - t0:.0f}s) {tail}")
    if p.returncode != 0 and p.stderr:
        log("     " + " | ".join(p.stderr.strip().splitlines()[-4:]))
    return p.returncode == 0


def older_than(path, hours):
    return not path.exists() or (time.time() - path.stat().st_mtime) > hours * 3600


def trim_log(max_lines=4000):
    if LOG.exists():
        lines = LOG.read_text(encoding="utf-8").splitlines()
        if len(lines) > max_lines:
            LOG.write_text("\n".join(lines[-max_lines:]) + "\n", encoding="utf-8")


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
    trim_log()
    log("refresh finished" + ("" if ok else " with errors"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
