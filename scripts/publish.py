"""Publish the data to the live site from this computer (README, "Publishing from this
computer"): commit the working folder's data files to the site's GitHub repository and
push them. update_results.py calls it after every results run (every 10 minutes while
votes are counted) and refresh_all.py after every full refresh.

    py scripts/publish.py            # every data file that changed (after a full refresh)
    py scripts/publish.py results    # the four files a results run rewrites
    py scripts/publish.py --dry-run  # what would go out, without committing or pushing

It works in a clone of its own (%LOCALAPPDATA%\\InformedVoter\\publish), never the
owner's GitHub Desktop clone, and publishes only data/ (data/cache excepted): code
reaches the site when the owner pushes it from GitHub Desktop, so a data format must
change in a way the live code still reads. It is off unless
~/.informed-voter/publish.json names the repository:

    {"repo": "https://github.com/loldudez/InformedVoter.git", "branch": "main"}

Pushing uses this computer's git sign-in (Git Credential Manager), made once by hand.
The script never asks for one, so no window opens from the scheduler; a failed push is
logged to data/cache/refresh.log and the next run tries again. A push refused because
the branch moved (the owner pushed in between) is redone on top of it.
"""

import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
LOG = DATA / "cache" / "refresh.log"
LOCK = DATA / "cache" / "publish.lock"
REFRESH_LOCK = DATA / "cache" / "refresh.lock"  # held while the race files are written
CONFIG = Path.home() / ".informed-voter" / "publish.json"
CLONE = Path(os.environ.get("LOCALAPPDATA") or Path.home()) / "InformedVoter" / "publish"
RESULTS = ["data/races.json", "data/offices.json", "data/control.json", "data/status.json"]
AUTHOR = ["-c", "user.name=informed-voter-refresh", "-c", "user.email=actions@users.noreply.github.com"]
# Never prompt: a scheduled run has nobody to answer, and Git Credential Manager would
# otherwise open a sign-in window every 10 minutes.
NO_PROMPT = {"GIT_TERMINAL_PROMPT": "0", "GCM_INTERACTIVE": "never"}
NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)


def log(msg):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(f"{datetime.now().isoformat(timespec='seconds')}  publish: {msg}\n")
    try:
        print(msg, flush=True)
    except Exception:  # noqa: BLE001  no console when run by the scheduler
        pass


class GitError(RuntimeError):
    pass


def git(*args, cwd=CLONE, timeout=180):
    p = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace",
                       timeout=timeout, env={**os.environ, **NO_PROMPT}, creationflags=NO_WINDOW)
    if p.returncode != 0:
        lines = (p.stderr or p.stdout or "").strip().splitlines()
        raise GitError(" | ".join(lines[-3:]) or f"git {args[0]} exited {p.returncode}")
    return p.stdout


# Locks: one publisher at a time, and no copying while a results run writes ---------------

def take(lock, wait_minutes, stale_minutes):
    lock.parent.mkdir(parents=True, exist_ok=True)
    deadline = time.time() + wait_minutes * 60
    while True:
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            with os.fdopen(fd, "w") as f:
                f.write(f"publish {os.getpid()} {datetime.now().isoformat(timespec='seconds')}\n")
            return True
        except FileExistsError:
            try:
                if time.time() - lock.stat().st_mtime > stale_minutes * 60:
                    lock.unlink(missing_ok=True)
                    continue
            except FileNotFoundError:
                continue
            if time.time() > deadline:
                return False
            time.sleep(5)


# What to publish ---------------------------------------------------------------------

def data_files():
    """Every file under data/ except the cache (which .gitignore leaves out too)."""
    out = []
    for p in sorted(DATA.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(ROOT)
        if rel.parts[1] == "cache" or "__pycache__" in rel.parts or p.suffix == ".tmp":
            continue
        out.append(rel.as_posix())
    return out


def ensure_clone(repo, branch):
    if (CLONE / ".git").exists():
        url = git("remote", "get-url", "origin").strip()
        if url != repo:
            git("remote", "set-url", "origin", repo)
        return
    CLONE.parent.mkdir(parents=True, exist_ok=True)
    git("clone", "-q", "--single-branch", "--branch", branch, repo, str(CLONE), cwd=CLONE.parent, timeout=900)


def stage(paths, guard):
    """Copy the files into the clone and stage them; the paths git sees changed."""
    if guard and not take(REFRESH_LOCK, wait_minutes=15, stale_minutes=45):
        raise GitError("the race files stayed locked for 15 minutes")
    try:
        present = []
        for rel in paths:
            src = ROOT / rel
            if not src.exists():
                continue
            dst = CLONE / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)
            present.append(rel)
    finally:
        if guard:
            REFRESH_LOCK.unlink(missing_ok=True)
    for i in range(0, len(present), 200):
        git("add", "--", *present[i:i + 200])
    return [line for line in git("diff", "--cached", "--name-only").splitlines() if line.strip()]


def publish(which, repo, branch, dry_run=False):
    paths = RESULTS if which == "results" else data_files()
    message = (f"Results as of {datetime.now():%b %d, %Y %H:%M}" if which == "results"
               else "Refresh election data")
    for attempt in range(1, 4):
        t0 = time.time()
        git("fetch", "-q", "origin", branch, timeout=600)
        git("reset", "-q", "--hard", f"origin/{branch}")  # this clone holds nothing of its own
        # A results run calls this while it holds the refresh lock itself; a full publish
        # takes it while copying, so it never copies a race file half-written.
        changed = stage(paths, guard=which != "results")
        if not changed:
            if dry_run:
                print(f"{which}: nothing new to publish")
            else:
                log(f"{which}: nothing new to publish")
            return 0
        if dry_run:
            print(f"{which}: would publish {len(changed)} files as \"{message}\":")
            for path in changed[:40]:
                print("  ", path)
            if len(changed) > 40:
                print(f"   ... and {len(changed) - 40} more")
            git("reset", "-q", "--hard", f"origin/{branch}")
            git("push", "--dry-run", "-q", "origin", f"HEAD:{branch}", timeout=120)  # signed in?
            print("The sign-in works: a real run would push.")
            return 0
        git(*AUTHOR, "commit", "-q", "-m", message)
        try:
            git("push", "-q", "origin", f"HEAD:{branch}", timeout=600)
        except GitError as e:
            text = str(e).lower()
            if any(k in text for k in ("rejected", "fetch first", "non-fast-forward")) and attempt < 3:
                log(f"{which}: the branch moved while publishing; trying again on top of it")
                continue
            raise
        head = git("rev-parse", "--short", "HEAD").strip()
        log(f"{which}: pushed {len(changed)} file{'s' if len(changed) != 1 else ''} as {head} ({time.time() - t0:.0f}s)")
        return 0
    return 1


def main():
    which = "results" if "results" in sys.argv[1:] else "all"
    dry_run = "--dry-run" in sys.argv[1:]
    if os.environ.get("GITHUB_ACTIONS"):
        return 0  # the cloud workflow commits its own data
    if not CONFIG.exists():
        print(f"Publishing is off: {CONFIG} doesn't exist (README, \"Publishing from this computer\").")
        return 0
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    repo, branch = cfg["repo"], cfg.get("branch", "main")
    if not take(LOCK, wait_minutes=10, stale_minutes=30):
        log(f"{which}: another publish has been running for 10 minutes; skipped")
        return 0
    try:
        ensure_clone(repo, branch)
        return publish(which, repo, branch, dry_run)
    except GitError as e:
        text = str(e).lower()
        why = ("this computer isn't signed in to GitHub for git (README, \"Publishing from this computer\")"
               if any(k in text for k in ("could not read username", "cannot prompt", "authentication failed", "403"))
               else str(e))
        log(f"FAIL {which}: {why}")
        return 1
    except subprocess.TimeoutExpired as e:
        log(f"FAIL {which}: git {e.cmd[1] if len(e.cmd) > 1 else ''} timed out")
        return 1
    finally:
        LOCK.unlink(missing_ok=True)


if __name__ == "__main__":
    sys.exit(main())
