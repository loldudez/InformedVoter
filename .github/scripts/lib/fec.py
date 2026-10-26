"""Candidate fundraising from the FEC API, cached on disk.

A personal key (free, from https://api.data.gov/signup/) is needed for the
breakdown by source. Put it in the FEC_API_KEY environment variable, or in
~/.informed-voter/fec_api_key (outside the website folder, so it is never
published). Without one the shared DEMO_KEY is used; it allows about ten calls an
hour, enough at best for the totals, and when it runs out the last good download
is kept and reported as stale.
"""

import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = "https://api.open.fec.gov/v1"
UA = "InformedVoter/1.0 (personal election-information site; data refresh script)"
CACHE = Path(__file__).resolve().parents[2] / "data" / "cache" / "fec_totals.json"
DETAIL_CACHE = Path(__file__).resolve().parents[2] / "data" / "cache" / "fec_breakdowns.json"
KEY_FILE = Path.home() / ".informed-voter" / "fec_api_key"
MAX_AGE_HOURS = 20  # FEC reports arrive quarterly and in pre-election batches; daily is plenty
MIN_RECEIPTS = 5000
DETAIL_FIELDS = ("individual_unitemized_contributions", "individual_itemized_contributions",
                 "other_political_committee_contributions", "political_party_committee_contributions",
                 "candidate_contribution", "loans_made_by_candidate", "transfers_from_other_authorized_committee")


class RateLimited(Exception):
    pass


def api_key():
    key = os.environ.get("FEC_API_KEY", "").strip()
    if not key and KEY_FILE.exists():
        key = KEY_FILE.read_text(encoding="utf-8").strip()
    return key or "DEMO_KEY"


def _get(path, params):
    url = f"{BASE}{path}?{urllib.parse.urlencode({**params, 'api_key': api_key()})}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 429:
                raise RateLimited()
            if e.code >= 500 and attempt < 2:
                time.sleep(5 * (attempt + 1))
                continue
            raise


def _download(office):
    """Every 2026 candidate for one office with meaningful receipts, highest first."""
    out, page = [], 1
    while True:
        d = _get("/candidates/totals/", {"election_year": 2026, "office": office, "per_page": 100,
                                         "page": page, "sort": "-receipts", "sort_null_only": "false"})
        rows = d.get("results", [])
        out.extend(rows)
        pages = d.get("pagination", {}).get("pages", 1)
        if not rows or page >= pages or (rows[-1].get("receipts") or 0) < MIN_RECEIPTS:
            break
        page += 1
    return [r for r in out if (r.get("receipts") or 0) >= MIN_RECEIPTS]


def _add_breakdowns(rows):
    """Fill in where each candidate's money came from, one call per candidate, only
    when the bulk list lacks it and a personal key is set. A candidate is fetched
    again only after a new report changes their coverage date."""
    if api_key() == "DEMO_KEY" or not rows or all(r.get(DETAIL_FIELDS[0]) is not None for r in rows):
        return 0
    cache = json.loads(DETAIL_CACHE.read_text(encoding="utf-8")) if DETAIL_CACHE.exists() else {}
    fetched = 0
    try:
        for r in rows:
            cid, end = r.get("candidate_id"), (r.get("coverage_end_date") or "")[:10]
            hit = cache.get(cid)
            if not hit or hit.get("end") != end:
                d = _get(f"/candidate/{cid}/totals/", {"cycle": 2026, "election_full": "true", "per_page": 1})
                res = (d.get("results") or [{}])[0]
                hit = {"end": end, **{k: res.get(k) for k in DETAIL_FIELDS + ("all_other_loans", "offsets_to_operating_expenditures", "other_receipts", "last_debts_owed_by_committee")}}
                cache[cid] = hit
                fetched += 1
                time.sleep(0.4)
            for k, v in hit.items():
                if k != "end" and v is not None:
                    r.setdefault(k, v)
    except RateLimited:
        pass  # keep what arrived; the rest fills in on the next refresh
    DETAIL_CACHE.parent.mkdir(parents=True, exist_ok=True)
    DETAIL_CACHE.write_text(json.dumps(cache), encoding="utf-8")
    return fetched


def load():
    """(rows, info). Re-downloads when the cache is older than MAX_AGE_HOURS."""
    cached = json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.exists() else None
    if cached:
        age = (datetime.now(timezone.utc) - datetime.fromisoformat(cached["fetched"])).total_seconds() / 3600
        if age < MAX_AGE_HOURS:
            return cached["rows"], {"fetched": cached["fetched"], "fresh": True, "note": "cached"}
    personal = api_key() != "DEMO_KEY"
    try:
        rows = _download("S") + _download("H")
    except RateLimited:
        note = "FEC API rate limit reached" + ("" if personal else " (the shared DEMO_KEY; add a personal key, see scripts/lib/fec.py)")
        if cached:
            return cached["rows"], {"fetched": cached["fetched"], "fresh": False, "note": note}
        return [], {"fetched": None, "fresh": False, "note": note}
    except Exception as e:  # network trouble: keep the last good copy
        note = f"FEC download failed: {e}"
        if cached:
            return cached["rows"], {"fetched": cached["fetched"], "fresh": False, "note": note}
        return [], {"fetched": None, "fresh": False, "note": note}
    detailed = _add_breakdowns(rows)
    fetched = datetime.now(timezone.utc).isoformat(timespec="seconds")
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps({"fetched": fetched, "rows": rows}), encoding="utf-8")
    with_parts = sum(r.get(DETAIL_FIELDS[0]) is not None for r in rows)
    return rows, {"fetched": fetched, "fresh": True,
                  "note": f"{len(rows)} candidates, {with_parts} with a breakdown by source ({detailed} updated)" if personal
                  else f"{len(rows)} candidates; totals only (a personal key adds the breakdown by source)"}


def finance_from(row):
    """FEC totals -> the site's finance object. The breakdown mirrors the filing's
    receipt lines and is filled in only when the API returned them."""
    total = round(row.get("receipts") or 0)
    parts = {}
    if all(row.get(k) is not None for k in DETAIL_FIELDS[:4]):
        parts = {
            "small": round(row["individual_unitemized_contributions"]),
            "large": round(row["individual_itemized_contributions"]),
            "pac": round(row["other_political_committee_contributions"]),
            "party": round(row["political_party_committee_contributions"]),
            "self": round((row.get("candidate_contribution") or 0) + (row.get("loans_made_by_candidate") or 0)),
            "public": 0,
            "transfers": round(row.get("transfers_from_other_authorized_committee") or 0),
        }
        other = ("all_other_loans", "offsets_to_operating_expenditures", "other_receipts")
        if any(row.get(k) is not None for k in other):  # the filing's own lines, never padded to the total
            parts["other"] = round(sum(row.get(k) or 0 for k in other))
        else:
            parts["other"] = max(0, total - sum(parts.values()))
    cid = row.get("candidate_id")
    end = (row.get("coverage_end_date") or "")[:10] or None
    debts = row.get("debts_owed_by_committee", row.get("last_debts_owed_by_committee"))
    return {
        "total": total, "parts": parts,
        "spent": round(row["disbursements"]) if row.get("disbursements") is not None else None,
        "cashOnHand": round(row["cash_on_hand_end_period"]) if row.get("cash_on_hand_end_period") is not None else None,
        "debts": round(debts) if debts else None,
        "from": (row.get("coverage_start_date") or "")[:10] or None,
        "asOf": end, "source": "FEC", "fecId": cid,
        "url": f"https://www.fec.gov/data/candidate/{cid}/?cycle=2026&election_full=true" if cid else None,
    }
