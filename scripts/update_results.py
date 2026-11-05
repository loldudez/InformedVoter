"""The results between full refreshes: every 10 minutes after Election Day until every
race is decided (Windows Task Scheduler, "\\InformedVoter\\Informed Voter results"; see
README, "Results every 10 minutes").

    py scripts/update_results.py

It reads only what changes while votes are counted: Wikipedia's national tables for the
calls (Senate, governor, House and the five statewide-office pages), the race pages that
changed since they were last read for the counts (races not called yet first, then
called races whose count isn't posted, within a time budget; the next run picks up the
rest), and the states' own counts where a script can read them
(scripts/lib/official_results.py, California so far). Then it recomputes each uncalled
race's count-adjusted projection (model.live) and the chambers' projected seats, and
rewrites data/races.json, data/offices.json, data/control.json and data/status.json in
place: everything else in them stays as the last full refresh (update_races.py, every 8
hours) left it. The new files must pass the validator before they replace the old ones.

A lock file (data/cache/refresh.lock) keeps it from running while the full refresh
writes the same files. After a good run, scripts/publish.py sends the four files to the
live site when this computer is set up to publish (README, "Publishing from this
computer"). Once every race is called or sent to a runoff, the script turns its own
scheduled task off. Each run is appended to data/cache/refresh.log.
"""

import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scripts" / "lib"))

import update_races as ur  # noqa: E402
import elections as el  # noqa: E402
import model  # noqa: E402
import official_results  # noqa: E402
import offices  # noqa: E402
import results  # noqa: E402
import wikitables as wt  # noqa: E402

DATA = ROOT / "data"
LOCK = DATA / "cache" / "refresh.lock"
LOG = DATA / "cache" / "refresh.log"
TASK = r"\InformedVoter\Informed Voter results"
EVERY_MINUTES = 10
BUDGET = 7 * 60          # seconds of page downloads per run; the task fires every 10 minutes
STOP_AFTER = datetime(2026, 12, 31, 23, 59)  # the last day the task runs, whatever is left
PY = sys.executable.replace("pythonw.exe", "python.exe")


def log(msg):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(f"{datetime.now().isoformat(timespec='seconds')}  results: {msg}\n")
    try:
        print(msg, flush=True)
    except Exception:  # noqa: BLE001  no console when run by the scheduler
        pass


# The lock ---------------------------------------------------------------------------

def take_lock(stale_minutes=45):
    """True when this run may write the data files. A lock older than `stale_minutes`
    is left from a run that died, and is taken over."""
    LOCK.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(LOCK, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        if time.time() - LOCK.stat().st_mtime < stale_minutes * 60:
            return False
        LOCK.unlink(missing_ok=True)
        return take_lock(stale_minutes)
    with os.fdopen(fd, "w") as f:
        f.write(f"update_results {os.getpid()} {datetime.now().isoformat(timespec='seconds')}\n")
    return True


def drop_lock():
    LOCK.unlink(missing_ok=True)


# Reading ----------------------------------------------------------------------------

def decided(r):
    return (r.get("result") or {}).get("status") in ("won", "runoff")


def has_count(r):
    return bool((r.get("result") or {}).get("rows"))


def fresh_calls(pages, status, map_index, states):
    """Every race as the national tables list it now: id -> {winners, advance, statusText,
    page} (winners as the table's candidate dicts), and the House's state pages."""
    sen_gov, _, _ = ur.statewide_races(pages, status)
    house, state_pages, _, _ = ur.house_races(pages, status, map_index)
    down, _ = offices.races(pages, status, states)
    out = {}
    for rid, r in {**sen_gov, **house, **down}.items():
        out[rid] = {"winners": r.get("_winners") or [], "advance": r.get("_advance") or [],
                    "statusText": r.get("statusText"), "page": r.get("page")}
    return out, state_pages


def ours(people, race):
    """The table's candidates as the race's own (the full refresh may have renamed ids)."""
    out = []
    for p in people:
        c = results.match(p["name"], race["candidates"], p["party"] if p.get("party") in ("D", "R") else None)
        if c and c not in out:
            out.append(c)
    return out


def old_box(race):
    """The count already on file, as results.build reads a box, for a race whose page
    wasn't read this time."""
    res = race.get("result") or {}
    if not res.get("rows"):
        return None
    return {"rows": [{k: r.get(k) for k in ("name", "party", "votes", "pct", "mate", "final")} | {"other": r.get("id") is None and r.get("party") is None}
                     for r in res["rows"]],
            "total": res.get("total"), "reporting": res.get("reporting"), "precincts": res.get("precincts"),
            "outcome": res.get("outcome"), "source": res.get("source"),
            "via": res.get("via"), "totalFromShares": res.get("totalFromShares")}


def read_pages(pages, wanted, budget_end):
    """HTML of each wanted page, by title: from the cache when its current revision is
    there, downloaded otherwise while the time budget lasts. Titles left for later are
    returned apart."""
    pages.prefetch(wanted)
    got, later = {}, []
    for title in wanted:
        rev = pages.revs.get(title)
        if not rev:
            continue
        if not wt.is_cached(rev["title"], rev) and time.time() > budget_end:
            later.append(title)
            continue
        got[title] = pages.html(title)
    return got, later


# Writing ----------------------------------------------------------------------------

def write_checked(outputs):
    """Write each file next to its target, validate the race files, then replace them all.
    False (and nothing replaced) when a race file fails the validator."""
    tmps = {}
    for name, obj in outputs.items():
        tmp = DATA / "cache" / f"results-{name}"
        tmp.write_text(json.dumps(obj, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        tmps[name] = tmp
    for name in ("races.json", "offices.json"):
        if name in tmps:
            p = subprocess.run([PY, "-I", "scripts/validate_races.py", str(tmps[name])], cwd=ROOT, capture_output=True,
                               text=True, encoding="utf-8", errors="replace", creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
            if p.returncode != 0:
                log(f"FAIL validator on {name}: {' | '.join((p.stdout or p.stderr).strip().splitlines()[-3:])}")
                for t in tmps.values():
                    t.unlink(missing_ok=True)
                return False
    for name, tmp in tmps.items():
        tmp.replace(DATA / name)
    return True


def publish():
    """Send the new files to the live site (scripts/publish.py, which does nothing unless
    this computer is set up to publish). It runs while this run still holds the lock, so
    no other run rewrites the files under it."""
    try:
        subprocess.run([PY, "scripts/publish.py", "results"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=1500, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    except subprocess.TimeoutExpired:
        log("publishing took over 25 minutes and was stopped; the next run tries again")


def stop_task(reason):
    p = subprocess.run(["schtasks", "/Change", "/TN", TASK, "/DISABLE"], capture_output=True, text=True,
                       creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    log(f"stopping: {reason}; scheduled task {'disabled' if p.returncode == 0 else 'not changed (' + (p.stderr or p.stdout).strip() + ')'}")


# The run ----------------------------------------------------------------------------

def main():
    t0 = time.time()
    now = datetime.now()
    if now < model.ELECTION_DAY:
        log("before Election Day; nothing to do")
        return 0
    if not take_lock():
        log("another refresh is writing the data files; skipped")
        return 0
    try:
        return run(t0, now)
    finally:
        drop_lock()


def run(t0, now):
    races_doc = json.loads((DATA / "races.json").read_text(encoding="utf-8"))
    offices_doc = json.loads((DATA / "offices.json").read_text(encoding="utf-8"))
    control = json.loads((DATA / "control.json").read_text(encoding="utf-8"))
    st = json.loads((DATA / "status.json").read_text(encoding="utf-8"))
    races = {r["id"]: r for r in races_doc["races"]}
    down = {r["id"]: r for r in offices_doc["races"]}
    every = {**races, **down}
    open_before = sorted(rid for rid, r in every.items() if not decided(r))
    if not open_before:
        stop_task("every race is called or sent to a runoff")
        return 0
    if now > STOP_AFTER:
        stop_task(f"past {STOP_AFTER:%b %d, %Y} with {len(open_before)} races still open")
        return 0

    status = ur.Status()
    pages = ur.Pages()
    map_index = json.loads((DATA / "maps" / "index.json").read_text(encoding="utf-8"))
    states = ur.load_states()
    budget_end = t0 + BUDGET

    # Calls: the national tables (only downloaded when they changed).
    pages.prefetch([ur.PAGES["senate"], ur.PAGES["governor"], ur.PAGES["house"], ur.PAGES["ratings"], *offices.PAGES])
    calls, state_pages = fresh_calls(pages, status, map_index, states)

    # Counts: the pages of races still open first, then of called races with no count, or
    # with only their infobox's count (read again until the page's results box is filled in).
    def page_of(r):
        if r["office"] == "house":
            return state_pages.get(r["state"])
        return (calls.get(r["id"]) or {}).get("page") or (r.get("result") or {}).get("page", {}).get("title", "").removeprefix("Wikipedia: ") or None
    first = [page_of(r) for r in every.values() if not decided(r)]
    then = [page_of(r) for r in every.values() if decided(r) and (not has_count(r) or (r.get("result") or {}).get("via") == "infobox")]
    wanted = list(dict.fromkeys(t for t in first + then if t))
    html_by_title, later = read_pages(pages, wanted, budget_end)

    boxes = {}
    for rid, r in every.items():
        title = page_of(r)
        h = html_by_title.get(title) if title else None
        if not h:
            continue
        refs = wt.references(h)
        rev = pages.revs[title]
        page = {"title": f"Wikipedia: {rev['title']}", "url": pages.url(title), "asOf": rev["timestamp"]}
        if r["office"] == "house":
            chunk = ur.district_chunks(h, map_index.get(r["state"], {}).get("cd", 0)).get(r["district"])
            if chunk is None:
                continue
            if r["district"] != "00":
                page["url"] += f"#District_{int(r['district'])}"
            boxes[rid] = (results.general_box(chunk, refs), page)
        else:
            boxes[rid] = (results.page_box(h, refs), page)

    # Rebuild each race's result: the table's call, the page's count (or the one on file).
    newly = []
    for rid, r in every.items():
        call = calls.get(rid)
        if call is None:
            continue
        box, page = boxes.get(rid, (None, None))
        if box is None:
            box = old_box(r)
            page = (r.get("result") or {}).get("page")
        res = results.build(r, ours(call["winners"], r), call["statusText"], box, page, advance=ours(call["advance"], r) or None)
        was = (r.get("result") or {}).get("status")
        if res:
            r["result"] = res
        if res and res["status"] in ("won", "runoff") and was not in ("won", "runoff"):
            newly.append(rid)

    # The states' own counts, ahead of the pages'.
    offs, off_info = official_results.load(log=lambda m: None)
    applied, unmatched = official_results.apply_all(every, offs)
    for rid in unmatched:
        status.warn(f"{rid}: the state's count names candidates not on our list; the race page's count is kept")

    ur.results_checks(races, down, status)
    forecasts = ur.forecast_all(races)
    ur.after_count(control, races, forecasts)
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    control["resultsUpdated"] = stamp

    open_after = sorted(rid for rid, r in every.items() if not decided(r))
    projected = sum(1 for rid in races if model.live(races[rid], forecasts.get(rid)))
    ca = off_info.get("CA") or {}
    detail = (f"{len(open_after)} races still open ({len(newly)} called since the last run: {', '.join(newly[:12]) or 'none'}); "
              f"{projected} with a count-adjusted projection; {len(html_by_title)} race pages read"
              + (f", {len(later)} left for the next run" if later else "")
              + f"; California's own count for {len(applied)} races"
              + (f" (posted {ca['asOf']})" if ca.get("asOf") else "") + ("" if ca.get("ok", True) else f" (API unreadable: {ca.get('reason')})"))
    status.check("results-refresh", f"Results re-read every {EVERY_MINUTES} minutes until every race is called", True, detail, "info")

    # Status: the full refresh's checks, with this run's results checks in their place.
    st["checks"] = [c for c in st.get("checks", []) if not c["id"].startswith("results") and c["id"] != "refresh-failed"] + status.checks
    st["resultsUpdated"] = stamp
    st["nextResultsMinutes"] = EVERY_MINUTES if open_after else None
    counts = st.setdefault("counts", {})
    counts.update(called=sum((r.get("result") or {}).get("status") == "won" for r in races.values()),
                  withCounts=sum(has_count(r) for r in races.values()),
                  officesCalled=sum((r.get("result") or {}).get("status") == "won" for r in down.values()))
    st["resultsWarnings"] = status.warnings[:50]
    races_doc["meta"]["resultsUpdated"] = stamp
    offices_doc["meta"]["resultsUpdated"] = stamp

    if not write_checked({"races.json": races_doc, "offices.json": offices_doc, "control.json": control, "status.json": st}):
        return 1
    log(f"ok ({time.time() - t0:.0f}s) {detail}")
    publish()
    if not open_after:
        stop_task("every race is called or sent to a runoff")
    return 0


if __name__ == "__main__":
    sys.exit(main())
