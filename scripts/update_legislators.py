"""Who sits in each state legislature now, from Open States' current-members files
(data.openstates.org/people/current/<st>.csv, CC0), for the seats not decided in 2026:
the staggered seats that weren't up, the chambers that didn't elect this year (Kansas's
Senate, the odd-year states), and any 2026 seat whose winner Wikipedia hasn't marked yet.
2026 winners come from the chamber pages (scripts/lib/legislature.py), never from here.

Each member is placed on the chamber's district map (data/maps/sldu|sldl/ST.json) by the
same district-name matching the chamber pages use; a member the matching can't place is
listed under "unmatched" and left off the map rather than guessed onto a district.

    py scripts/update_legislators.py            (every state)
    py scripts/update_legislators.py TX VT      (only those)

Writes data/legislators/ST.json. A state whose file can't be read keeps its old file.
"""

import csv
import io
import json
import re
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "lib"))
import elections as el  # noqa: E402
import legislature as LG  # noqa: E402

OUT = ROOT / "data" / "legislators"
URL = "https://data.openstates.org/people/current/{st}.csv"
SOURCE = {"title": "Open States (Plural Policy), current legislators", "url": "https://open.pluralpolicy.com/data/", "license": "CC0"}
UA = "InformedVoterResearch/1.0"
CHAMBER = {"upper": ("senate", "sldu"), "lower": ("house", "sldl"), "legislature": ("leg", "sldu")}
PARTY = {"democratic": "D", "republican": "R", "independent": "I", "libertarian": "L", "green": "G", "nonpartisan": "N",
         "democratic-farmer-labor": "D", "progressive": "Progressive", "forward": "Forward"}


def party_code(p):
    low = (p or "").strip().lower()
    if low in PARTY:
        return PARTY[low]
    code = el.party_code(p) if p else None
    return code or (p or None)


def fetch(st):
    req = urllib.request.Request(URL.format(st=st.lower()), headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        if r.status != 200:
            raise RuntimeError(f"HTTP {r.status}")
        return r.read().decode("utf-8")


def wiki_of(row):
    for u in re.split(r";", (row.get("sources") or "") + ";" + (row.get("links") or "")):
        u = u.strip()
        if re.match(r"https?://en\.wikipedia\.org/wiki/", u):
            return "https://en.wikipedia.org/wiki/" + u.split("/wiki/", 1)[1]
    return None


def site_of(row):
    """The member's own page: the legislature's page for them first, else their site."""
    links = [u.strip() for u in (row.get("links") or "").split(";") if u.strip().startswith("https://")]
    official = [u for u in links if re.search(r"\.(gov|us)(/|$)|legis|senate\.|house\.|assembly\.", u, re.I)]
    return (official or links or [None])[0]


def build_state(st, text, log=print):
    rows = list(csv.DictReader(io.StringIO(text)))
    chambers, unmatched = {}, []
    idx_cache = {}
    for row in rows:
        ch = CHAMBER.get((row.get("current_chamber") or "").strip())
        if not ch:
            continue
        key, layer = ch
        if (key, layer) not in idx_cache:
            path = ROOT / "data" / "maps" / layer / f"{st}.json"
            feats = json.loads(path.read_text(encoding="utf-8"))["features"] if path.exists() else []
            idx_cache[(key, layer)] = LG.feature_index(feats) if feats else None
        idx = idx_cache[(key, layer)]
        label = (row.get("current_district") or "").strip()
        fid = LG.match_feature(label, idx) if idx and label else None
        if not fid and idx and re.fullmatch(r"\d+[A-Z]", label):
            fid = LG.match_feature(label[:-1], idx)  # Idaho's seats A and B of one district ("10A")
        person = {"n": (row.get("name") or "").strip(), "p": party_code(row.get("current_party"))}
        if not person["n"]:
            continue
        w = wiki_of(row)
        if w:
            person["wiki"] = w
        site = site_of(row)
        if site:
            person["site"] = site
        if not fid:
            unmatched.append({"chamber": key, "district": label, **person})
            continue
        chambers.setdefault(key, {}).setdefault(fid, []).append(person)
    for ch in chambers.values():
        for fid in ch:
            ch[fid].sort(key=lambda p: p["n"])
    n = sum(len(v) for ch in chambers.values() for v in ch.values())
    log(f"  {st}: {n} members on the map" + (f", {len(unmatched)} unmatched ({', '.join(sorted({u['district'] for u in unmatched})[:6])})" if unmatched else ""))
    return {"state": st, "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "source": SOURCE,
            "chambers": chambers, "unmatched": unmatched}


def unchanged(path, data):
    """The same members as the file already written (its date aside), so the file stays
    as it is and the live site gets no new copy of it."""
    try:
        old = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    return {k: v for k, v in old.items() if k != "updated"} == {k: v for k, v in data.items() if k != "updated"}


STAMP = ROOT / "data" / "cache" / "legislators.stamp"  # when the files were last checked (refresh_all.py)


def main(states=None, log=print):
    OUT.mkdir(parents=True, exist_ok=True)
    states = states or [s for s in el.STATE_ABBR.values() if s != "DC"]
    ok, same, failed = 0, 0, []
    for i, st in enumerate(sorted(set(states))):
        if i:
            time.sleep(1)
        try:
            data = build_state(st, fetch(st), log)
        except Exception as e:  # keep the old file
            failed.append(f"{st} ({e})")
            log(f"  {st}: failed, keeping the old file: {e}")
            continue
        path = OUT / f"{st}.json"
        if unchanged(path, data):
            same += 1
            continue
        path.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        ok += 1
    STAMP.parent.mkdir(parents=True, exist_ok=True)
    STAMP.write_text(datetime.now(timezone.utc).isoformat(timespec="seconds"), encoding="utf-8")
    log(f"  legislators: {ok} states written, {same} unchanged" + (f", {len(failed)} failed: {', '.join(failed)}" if failed else ""))
    return {"ok": ok, "same": same, "failed": failed}


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    res = main([a.upper() for a in sys.argv[1:]] or None)
    sys.exit(1 if res["failed"] and not (res["ok"] or res["same"]) else 0)
