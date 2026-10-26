"""Refresh data/inflation.json from FRED (Federal Reserve Bank of St. Louis).

FRED republishes the Bureau of Labor Statistics CPI and average-price series
under BLS's own IDs, plus interest-rate series, as plain CSV with no API key.
BLS's own API rejects scripted requests, and neither service allows a browser
to call it directly, so the site reads a snapshot written by this script.

Usage:  python -I scripts/update_inflation.py [output-path]
Run it monthly, after BLS publishes CPI (usually mid-month).
"""

import csv
import io
import json
import sys
import time
import urllib.request
from datetime import date, datetime, timezone

YEARS = 6  # five-year view plus one year of history for year-over-year change

# id (or fallbacks), label, unit, kind, group
# kind: "index" -> shown as year-over-year % change; "price" -> dollars; "rate" -> percent
SERIES = [
    (["CPIAUCNS"], "All items (headline CPI)", "index", "index", "Overall"),
    (["CPILFENS"], "Core CPI (excludes food and energy)", "index", "index", "Overall"),
    (["CUUR0000SAF11"], "Groceries (food at home)", "index", "index", "Food"),
    (["CUUR0000SEFV"], "Restaurants (food away from home)", "index", "index", "Food"),
    (["APU0000708111"], "Eggs, grade A large", "$ per dozen", "price", "Food"),
    (["APU0000709112"], "Milk, whole", "$ per gallon", "price", "Food"),
    (["APU0000702111"], "Bread, white", "$ per lb", "price", "Food"),
    (["APU0000703112"], "Ground beef", "$ per lb", "price", "Food"),
    (["APU0000706111"], "Chicken, whole", "$ per lb", "price", "Food"),
    (["APU0000FF1101"], "Chicken breast, boneless", "$ per lb", "price", "Food"),
    (["APU0000717311"], "Coffee, ground", "$ per lb", "price", "Food"),
    (["APU0000711211"], "Bananas", "$ per lb", "price", "Food"),
    (["APU0000710212"], "Cheddar cheese", "$ per lb", "price", "Food"),
    (["APU0000712311"], "Tomatoes", "$ per lb", "price", "Food"),
    (["APU0000701111"], "Flour, all-purpose", "$ per lb", "price", "Food"),
    (["APU000074714"], "Gasoline, regular", "$ per gallon", "price", "Energy"),
    (["CUUR0000SETB01"], "Gasoline (CPI)", "index", "index", "Energy"),
    (["APU000072610"], "Electricity", "$ per kWh", "price", "Energy"),
    (["CUUR0000SEHF01"], "Electricity (CPI)", "index", "index", "Energy"),
    (["CUUR0000SETA01"], "New vehicles", "index", "index", "Cars"),
    (["CUUR0000SETA02"], "Used cars and trucks", "index", "index", "Cars"),
    (["CUUR0000SEHA"], "Rent", "index", "index", "Housing"),
    (["CUUR0000SAM", "CPIMEDSL", "CUSR0000SAM"], "Medical care", "index", "index", "Health"),
    (["FEDFUNDS"], "Federal funds rate", "%", "rate", "Interest rates"),
    (["MORTGAGE30US"], "30-year fixed mortgage", "%", "rate", "Interest rates"),
    (["GS10"], "10-year Treasury yield", "%", "rate", "Interest rates"),
    (["TERMCBCCALLNS"], "Credit card interest rate", "%", "rate", "Interest rates"),
    (["TERMCBAUTO48NS"], "New car loan rate (48-month)", "%", "rate", "Interest rates"),
]

SOURCES = {
    "CPI": "U.S. Bureau of Labor Statistics, Consumer Price Index and Average Price Data",
    "MORTGAGE30US": "Freddie Mac, Primary Mortgage Market Survey",
    "rates": "Board of Governors of the Federal Reserve System",
    "via": "Retrieved from FRED, Federal Reserve Bank of St. Louis",
}


def fetch(series_id, start):
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}&cosd={start}"
    req = urllib.request.Request(url, headers={"User-Agent": "InformedVoter-data-refresh/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        text = r.read().decode("utf-8")
    if not text.startswith("observation_date"):
        raise ValueError("not a FRED csv")
    rows = list(csv.reader(io.StringIO(text)))[1:]
    out = []
    for d, v in rows:
        if v in (".", ""):
            continue  # FRED marks missing months (e.g. the Oct 2025 shutdown gap) with "."
        out.append((d, float(v)))
    if not out:
        raise ValueError("empty series")
    return out


def monthly(points):
    """Average weekly/daily observations into calendar months."""
    buckets = {}
    for d, v in points:
        buckets.setdefault(d[:7], []).append(v)
    return [[m, round(sum(vs) / len(vs), 3)] for m, vs in sorted(buckets.items())]


def main(out_path):
    start = date(date.today().year - YEARS, 1, 1).isoformat()
    series = []
    for ids, label, unit, kind, group in SERIES:
        last_err = None
        for sid in ids:
            try:
                pts = fetch(sid, start)
                break
            except Exception as e:  # try the next fallback id
                last_err = e
                pts = None
            finally:
                time.sleep(0.4)
        if pts is None:
            print(f"SKIP {label}: {last_err}")
            continue
        data = monthly(pts) if sid in ("MORTGAGE30US",) else [[d[:7], round(v, 3)] for d, v in pts]
        series.append({"id": sid, "label": label, "unit": unit, "kind": kind, "group": group, "data": data})
        print(f"{sid:16} {label:40} {len(data):3} months, latest {data[-1]}")
    out = {
        "updated": datetime.now(timezone.utc).isoformat(timespec="minutes"),
        "sources": SOURCES,
        "series": series,
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, separators=(",", ":"))
    print(f"wrote {out_path} ({len(series)} series)")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "data/inflation.json")
