"""Statewide races below governor on the 2026 ballot: attorney general, secretary of
state, lieutenant governor (where it is elected on its own ballot line), state
treasurer and state auditor (comptroller in some states), from Wikipedia's national
page for each office, used as an aggregator (CC BY-SA) like the Senate, House and
governor pages.

Each page's "Race summary" table gives the state, the officeholder and party, a
status ("Incumbent re-elected.", "Republican hold.") and the candidates, with a
check mark on each winner once the race is called; the state's name links the race's
own page, where the refresh reads the results box, polls and campaign sites. The
"Predictions" table carries Sabato's Crystal Ball, the one outlet that rates these.

These races carry `format: "office"`: no win probabilities, as for state legislative
races (almost none are polled), the state's 2024 presidential margin for context, the
forecasters' rating where there is one, and the results. They are written to
data/offices.json by update_races.py, which merges research overlays (bios, sourced
positions) into them exactly as it does for federal races; ids are ST-AG, ST-SOS,
ST-LG, ST-TREAS and ST-AUD.

Lieutenant governors elected on a ticket with the governor (most states) are not
separate races; the governor's results box names the running mate.
"""

import re

import elections as el
import wikitables as wt

# (office key, id code, Wikipedia page, default title)
OFFICES = [
    ("attorney-general", "AG", "2026 United States attorney general elections", "Attorney General"),
    ("secretary-of-state", "SOS", "2026 United States secretary of state elections", "Secretary of State"),
    ("lieutenant-governor", "LG", "2026 United States lieutenant gubernatorial elections", "Lieutenant Governor"),
    ("treasurer", "TREAS", "2026 United States state treasurer elections", "State Treasurer"),
    ("auditor", "AUD", "2026 United States state auditor elections", "State Auditor"),
]
PAGES = [o[2] for o in OFFICES]


def office_title(page_title, state_name, default):
    """'2026 Connecticut State Comptroller election' -> 'State Comptroller'."""
    if not page_title:
        return default
    t = re.sub(r"^2026\s+", "", page_title)
    t = re.sub(r"\s+(special\s+)?elections?$", "", t, flags=re.I)
    if t.startswith(state_name + " "):
        t = t[len(state_name) + 1:]
    if not t or "gubernatorial" in t.lower() or len(t) > 60:
        return default
    return t[0].upper() + t[1:]


def summary_tables(html_text):
    """The race summary tables (states first; the territories' table is skipped,
    except the District of Columbia's row)."""
    chunk = wt.section_by_title(html_text, "Race summary") or wt.section_by_title(html_text, "States") or ""
    out = []
    for t in wt.tables(chunk):
        hi = el.header_row(t, "state", "candidates")
        if hi is None:
            hi = el.header_row(t, "territory", "candidates")
        if hi is not None:
            out.append((t, hi))
    return out


def races(pages, status, states):
    """{race id: race} for every down-ballot race the five pages list, plus the pages'
    HTML by office key (for the ratings)."""
    pages.prefetch(PAGES)
    out, htmls = {}, {}
    for key, code, title, default in OFFICES:
        h = pages.html(title)
        if not h:
            status.warn(f"down-ballot page {title} missing")
            continue
        htmls[key] = h
        n = 0
        for t, hi in summary_tables(h):
            heads = el.heads_of(t, hi)
            c_party = el.col(heads, "party")
            c_status = el.col(heads, "status", "results")
            c_cand = el.col(heads, "candidates")
            c_inc = 1 if c_party != 1 else None   # the officeholder's column follows the state's
            for row in t["rows"][hi + 1:]:
                label = wt.text(row[0]).replace("\n", " ").strip()
                st = el.STATE_ABBR.get(re.sub(r"\(.*?\)", "", label).strip())
                if not st or c_cand is None or c_cand >= len(row):
                    continue
                rid = f"{st}-{code}"
                status_text = wt.text(row[c_status]).replace("\n", " ") if c_status is not None else ""
                inc_cell = row[c_inc] if c_inc is not None else None
                people, inc_running, winners, advancing = el.table_candidates(rid, row[c_cand], inc_cell, status_text)
                if not people:
                    continue
                link = next((l["title"] for l in row[0]["links"] if l["title"].startswith("2026")), None)
                held = el.party_code(wt.text(row[c_party])) if c_party is not None else None
                out[rid] = {
                    "id": rid, "state": st, "office": key, "level": "state", "format": "office",
                    "officeName": office_title(link, el.STATE_NAME.get(st, ""), default),
                    "district": None, "statewide": True, "special": "special" in label.lower(),
                    "held": held if held in ("D", "R", "I") else None,
                    "incumbentName": wt.text(inc_cell).split("\n")[0].strip() if inc_cell is not None else None,
                    "open": not inc_running, "statusText": status_text,
                    "candidates": people, "page": link, "_winners": winners, "_advance": advancing,
                    "pres24": states.get(st, {}).get("pres24"),
                    "sources": [{"title": f"Wikipedia: {pages.revs[title]['title']}, Race summary", "url": pages.url(title) + "#Race_summary"}],
                }
                n += 1
        # Ratings (Sabato's Crystal Ball rates attorney general and secretary of state races).
        rated = el.ratings_table(wt.section_by_title(h, "Predictions") or "", "State", min_outlets=1)
        for label, info in rated.items():
            st = el.STATE_ABBR.get(re.sub(r"\(.*?\)", "", label).strip())
            r = out.get(f"{st}-{code}") if st else None
            if r and info["ratings"]:
                r["ratings"] = info["ratings"]
                r["ratingsSource"] = {"title": f"Wikipedia: {pages.revs[title]['title']}, Predictions", "url": pages.url(title) + "#Predictions"}
        status.check(f"offices-{code.lower()}", f"{default} races found", n > 0, f"{n} races on {title}")
    return out, htmls
