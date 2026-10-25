"""Candidate fundraising totals from the FEC API, cached on disk.

Set FEC_API_KEY (free, from https://api.data.gov/signup/) for full, fast access.
Without it the shared DEMO_KEY is used, which allows only a few dozen calls an
hour; when it runs out, the last good download is kept and reported as stale.
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
MAX_AGE_HOURS = 20  # FEC reports arrive quarterly and in pre-election batches; daily is plenty
MIN_RECEIPTS = 5000


class RateLimited(Exception):
    pass


def _get(path, params):
    key = os.environ.get("FEC_API_KEY") or "DEMO_KEY"
    url = f"{BASE}{path}?{urllib.parse.urlencode({**params, 'api_key': key})}"
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


def load():
    """(rows, info). Re-downloads when the cache is older than MAX_AGE_HOURS."""
    cached = json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.exists() else None
    if cached:
        age = (datetime.now(timezone.utc) - datetime.fromisoformat(cached["fetched"])).total_seconds() / 3600
        if age < MAX_AGE_HOURS:
            return cached["rows"], {"fetched": cached["fetched"], "fresh": True, "note": "cached"}
    try:
        rows = _download("S") + _download("H")
    except RateLimited:
        note = "FEC API rate limit reached (set FEC_API_KEY for a personal key)"
        if cached:
            return cached["rows"], {"fetched": cached["fetched"], "fresh": False, "note": note}
        return [], {"fetched": None, "fresh": False, "note": note}
    except Exception as e:  # network trouble: keep the last good copy
        note = f"FEC download failed: {e}"
        if cached:
            return cached["rows"], {"fetched": cached["fetched"], "fresh": False, "note": note}
        return [], {"fetched": None, "fresh": False, "note": note}
    fetched = datetime.now(timezone.utc).isoformat(timespec="seconds")
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps({"fetched": fetched, "rows": rows}), encoding="utf-8")
    return rows, {"fetched": fetched, "fresh": True, "note": f"{len(rows)} candidates"}


def finance_from(row):
    """FEC totals row -> the site's finance object. The breakdown is filled in only
    from fields the API actually returned."""
    total = round(row.get("receipts") or 0)
    parts = {}
    fields = {
        "small": row.get("individual_unitemized_contributions"),
        "large": row.get("individual_itemized_contributions"),
        "pac": row.get("other_political_committee_contributions"),
        "party": row.get("political_party_committee_contributions"),
    }
    self_money = None
    if row.get("candidate_contribution") is not None or row.get("loans_made_by_candidate") is not None:
        self_money = (row.get("candidate_contribution") or 0) + (row.get("loans_made_by_candidate") or 0)
    if all(v is not None for v in fields.values()):
        parts = {k: round(v) for k, v in fields.items()}
        parts["self"] = round(self_money or 0)
        parts["public"] = 0
        parts["other"] = max(0, total - sum(parts.values()))
    cid = row.get("candidate_id")
    end = (row.get("coverage_end_date") or "")[:10] or None
    return {
        "total": total, "parts": parts, "cashOnHand": round(row["cash_on_hand_end_period"]) if row.get("cash_on_hand_end_period") is not None else None,
        "asOf": end, "source": "FEC", "fecId": cid,
        "url": f"https://www.fec.gov/data/candidate/{cid}/?cycle=2026&election_full=true" if cid else None,
    }
