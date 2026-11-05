"""The 2026 general election's results, read from Wikipedia (CC BY-SA), used as an
aggregator just as it is for candidates and ratings.

Two places carry them:

- The national tables (Senate, governor, House, and the down-ballot office pages)
  mark each winner with a green check mark once the race is called, set the name
  in bold, and say what happened in the status column ("Incumbent re-elected.",
  "Democratic gain."). A race counts as decided only with that mark: vote counts
  alone never call a race here. Two marks in a race for one seat mean the two
  candidates advancing to a runoff (Louisiana's open primaries).
- Each race page's general-election box ("Party | Candidate | Votes | %") has the
  vote counts editors copy from the official returns, cited in its caption and
  sometimes captioned "(98.24% reporting)". They are unofficial until the states
  certify them, and the site says so.
- While that box is still blank on the night of the count, a statewide race page's
  infobox can already carry the count: "Reporting 96% as of 6:32 PM EST", citing the
  AP and the New York Times, and each leading nominee's "Popular vote" and
  "Percentage" (Mississippi's Senate race, Nov. 4, 2026). `page_box` falls back on it
  (`via: "infobox"`). It lists only the leading candidates, so an "Others" line takes
  the share that remains, and the total is worked out from the shares, to the nearest
  hundred votes (`totalFromShares`).

A race's `result`:
    status    "won", "runoff" or "counting" (votes posted, no call yet)
    winners   ids of the check-marked candidates ("won")
    advance   ids of the candidates advancing ("runoff")
    rows      the box as published, in its order: {id (None for a write-in line or
              a name not on our list), name, party, votes, pct}
    total     total votes, reporting (percent of the vote counted, when the caption
              gives it; a share of precincts reporting goes in `precincts` instead)
    via       "infobox" when the count comes from the page's infobox (see above), with
              totalFromShares: the total is worked out from the printed shares
    outcome   "Republican hold", "Democratic gain" ... (the box's footer, else the
              status column), note (the status column's own words)
    flip      True when the winner's party differs from the party holding the seat
    source    the official returns the box cites; page: the Wikipedia page read
"""

import math
import re

import elections as el
import wikitables as wt

BAD_CAPTION = re.compile(r"primar|runoff|run-off|caucus|convention|by county|by district|results by|straw|nominat|special election results", re.I)
REPORTING = re.compile(r"\(\s*([\d.]+)\s*%\s*(?:of (?:the )?(?:expected |estimated )?(votes?|precincts|ballots) )?(?:reporting|counted|in)\b", re.I)
OTHER_ROW = re.compile(r"^(write-?ins?|others?|scattering|scattered|blank|none of (?:these|the) candidates|over ?votes|under ?votes|void)\b", re.I)
SKIP_ROW = re.compile(r"^(total|turnout|majority|plurality|margin|swing|registered|rejected|spoiled|invalid|blank ballots|valid votes|continuing ballots|exhausted ballots|inactive ballots)", re.I)
# Sections that hold primaries, conventions and runoffs, cut out before a page is searched
# for its general-election box (Maine's primary tabulations have no caption at all).
NOT_GENERAL = re.compile(r"primar|convention|caucus|runoff|run-off|nominat|endorsement|polling|fundraising|background", re.I)


def without_sections(html_text, pattern=NOT_GENERAL):
    """The page with every section whose title matches `pattern` cut out."""
    out = html_text
    for s in wt.split_sections(html_text):
        if pattern.search(s["title"]) and s["html"] in out:
            out = out.replace(s["html"], "")
    return out


def _pct(s):
    m = re.search(r"-?\d+(?:\.\d+)?", (s or "").replace(",", ""))
    return float(m.group(0)) if m else None


def _name(s):
    # "(projected)" is an editor's note beside a name, never a call (calls come only from
    # the national tables' check marks).
    s = re.sub(r"\((?:incumbent|write-in|withdrawn|deceased|inc\.?|projected|presumptive)[^)]*\)", "", s, flags=re.I)
    s = re.sub(r"[†‡*§¶]", "", s)
    return re.sub(r"\s+", " ", s).strip(" ,;")


def boxes(chunk):
    """Every general-election results box in an HTML chunk, as (table, header row)."""
    out = []
    for t in wt.tables(chunk or "", li_breaks=True):
        if BAD_CAPTION.search(t.get("caption") or ""):
            continue
        hi = el.header_row(t, "party", "candidate", "votes")
        if hi is not None:
            out.append((t, hi))
    return out


def parse_box(t, hi, refs):
    """One results box -> {rows, total, reporting, outcome, source}."""
    heads = el.heads_of(t, hi)
    party_cols = [i for i, h in enumerate(heads) if h.startswith("party")]
    c_party = party_cols[-1] if party_cols else None
    c_cand = el.col(heads, "candidate")
    c_votes = el.col(heads, "votes", "first round", "round 1")
    c_pct = next((i for i, h in enumerate(heads) if h in ("%", "percent", "share")), None)
    if c_pct is None and c_votes is not None and c_votes + 1 < len(heads) and "%" in heads[c_votes + 1]:
        c_pct = c_votes + 1
    # A ranked-choice tabulation repeats "Votes | %" for each round, with transfers between:
    # the first pair is the first round, the last pair the final round.
    vote_cols = [i for i, h in enumerate(heads) if h == "votes"]
    c_final = vote_cols[-1] if len(vote_cols) > 1 else None
    c_final_pct = c_final + 1 if c_final is not None and c_final + 1 < len(heads) and heads[c_final + 1] == "%" else None
    rows, total, outcome, cited = [], None, None, list(t.get("caprefs") or [])
    seen = set()
    for row in t["rows"][hi + 1:]:
        raw = [wt.text(c) for c in row]
        cells = [" ".join(x.split()) for x in raw]
        if not cells:
            continue
        first = cells[0].lower()
        joined = " ".join(dict.fromkeys(c for c in cells if c))
        votes = el.num(cells[c_votes]) if c_votes is not None and c_votes < len(cells) else None
        if first.startswith("total"):
            total = votes
            cited += [r for c in row for r in c.get("refs", [])]
            continue
        hold = re.search(r"\b([A-Z][\w-]*(?: \(?[A-Z][\w.-]*\)?)*) (hold|gain)(?: from ([A-Z][\w-]*(?: \(?[A-Z][\w.-]*\)?)*))?", joined)
        if hold and (votes is None or "swing" in joined.lower()):
            outcome = hold.group(0)
            continue
        if SKIP_ROW.match(first) or (c_cand is not None and c_cand < len(cells) and SKIP_ROW.match(cells[c_cand].lower())):
            continue
        if c_cand is None or c_cand >= len(cells):
            continue
        # A governor's box lists the running mate on a second line of the same cell.
        lines = [x.strip() for x in raw[c_cand].split("\n") if x.strip()]
        name = _name(lines[0]) if lines else ""
        mate = _name(lines[1]) if len(lines) > 1 else None
        if not name or name.lower() in ("candidate", "party"):
            continue
        party = cells[c_party] if c_party is not None and c_party < len(cells) else ""
        if OTHER_ROW.match(name) or OTHER_ROW.match(party):
            rows.append({"id": None, "name": name if OTHER_ROW.match(name) else party or name, "party": None,
                         "votes": votes, "pct": _pct(cells[c_pct]) if c_pct is not None and c_pct < len(cells) else None, "other": True})
            continue
        key = el.norm(name)
        if key in seen:
            continue
        seen.add(key)
        final = None
        if c_final_pct is not None and c_final_pct < len(cells):
            final = _pct(cells[c_final_pct])
        rows.append({"id": None, "name": name, "party": el.party_code(party) if party else "I", "votes": votes,
                     "pct": _pct(cells[c_pct]) if c_pct is not None and c_pct < len(cells) else None,
                     "bold": bool(row[c_cand].get("bold")), **({"mate": mate} if mate else {}),
                     **({"final": final} if final is not None else {})})
    m = REPORTING.search(t.get("caption") or "")
    src = next((refs[r] for r in cited if r in refs), None)
    precincts = bool(m and (m.group(2) or "").lower() == "precincts")
    return {"rows": rows, "total": total, "reporting": float(m.group(1)) if m and not precincts else None,
            "precincts": float(m.group(1)) if precincts else None, "outcome": outcome,
            "source": {"title": src["title"] or "Official results", "url": src["url"]} if src else None}


def general_box(html_text, refs, scope_titles=("General election",)):
    """The general-election box of a race page or a House district's section: the
    one in the "General election" section (its "Results" subsection first). Only a
    page with no such section is searched as a whole, with its primary, convention and
    runoff sections cut out first."""
    scopes = []
    for title in scope_titles:
        sec = wt.section_by_title(html_text, title)
        if sec:
            res = wt.section_by_title(sec, "Results")
            scopes += [res, sec] if res else [sec]
    if not scopes:
        scopes.append(without_sections(html_text))
    for chunk in scopes:
        found = [parse_box(t, hi, refs) for t, hi in boxes(chunk)]
        found = [b for b in found if len([r for r in b["rows"] if not r.get("other")]) >= 1]
        if found:
            return found[0]
    return None


# The general election's day as an infobox prints it: an infobox for a primary or a
# December runoff is never read as the count.
GENERAL_DAY = re.compile(r"November\s+3,\s*2026")


def _infobox(html_text):
    """The HTML of a page's first election infobox, its nested tables included."""
    m = re.search(r'<table[^>]*class="[^"]*\binfobox\b[^"]*\bib-election\b', html_text or "")
    if not m:
        return None
    depth = 0
    for t in re.finditer(r"<(/?)table\b[^>]*>", html_text[m.start():]):
        depth += -1 if t.group(1) else 1
        if depth == 0:
            return html_text[m.start():m.start() + t.end()]
    return None


def infobox_count(html_text, refs):
    """The count in a statewide race page's election infobox, as parse_box gives a box's,
    or None when the infobox has no votes. Each block of nominees (the infobox puts two
    or three side by side) has rows labelled "Nominee" (or "Candidate"), "Party",
    "Popular vote" and "Percentage"; "Reporting" sits in the infobox itself, citing the
    count's sources. A ranked-choice race's "First round" and "Final round" rows aren't
    read: its box gives the rounds."""
    seg = _infobox(html_text)
    if not seg or not GENERAL_DAY.search(re.sub(r"<[^>]+>|&#160;|&nbsp;|\xa0", " ", seg)):
        return None
    tabs = wt.tables(seg)
    outer = next((t for t in tabs if "infobox" in t["classes"]), None)
    if outer is None or BAD_CAPTION.search(outer.get("caption") or ""):
        return None
    rows, decimals = [], 2
    for t in tabs:
        if t is outer:
            continue
        block = {}
        for row in t["rows"]:
            if row and row[0].get("th"):
                label = " ".join(wt.text(row[0]).split()).lower()
                block.setdefault(label, [" ".join(wt.text(c).split()) for c in row[1:]])
        names = block.get("nominee") or block.get("candidate")
        if not names or "popular vote" not in block:
            continue
        parties, votes, pcts = block.get("party", []), block["popular vote"], block.get("percentage", [])
        for i, raw_name in enumerate(names):
            name = _name(raw_name)
            if not name:
                continue
            v = el.num(votes[i]) if i < len(votes) else None
            p = _pct(pcts[i]) if i < len(pcts) else None
            if p is not None:
                d = re.search(r"\d+(?:\.(\d+))?", pcts[i].replace(",", ""))
                decimals = min(decimals, len(d.group(1) or "") if d else 0)
            party = parties[i] if i < len(parties) else ""
            rows.append({"id": None, "name": name, "party": el.party_code(party) if party else "I",
                         "votes": v, "pct": p, "bold": False})
    counted = [r for r in rows if r["votes"] is not None and r["pct"]]
    if len(counted) < 2 or len(counted) < len(rows):
        return None
    shown = sum(r["pct"] for r in rows)
    if shown > 100.5:
        return None
    listed = sum(r["votes"] for r in rows)
    approx = shown < 99.95
    if approx:
        # The total from the nominees' votes over their shares, rounded to what the printed
        # shares allow (to the hundred with two decimals, the thousand with one), and the
        # others' share as the rest.
        total = listed / (shown / 100)
        err = total * len(rows) * 0.5 * 10 ** -decimals / shown
        unit = 10 ** max(0, math.ceil(math.log10(err))) if err > 0 else 1
        total = int(round(total / unit) * unit)
        rows.append({"id": None, "name": "Others", "party": None, "votes": None, "pct": round(100 - shown, decimals), "other": True})
    else:
        total = int(listed)
    reporting, precincts, cited = None, None, []
    for row in outer["rows"]:
        if row and row[0].get("th") and " ".join(wt.text(row[0]).split()).lower() == "reporting" and len(row) > 1:
            txt = wt.text(row[1])
            share = _pct(txt)
            if share is not None and 0 < share <= 100:
                if "precinct" in txt.lower():
                    precincts = share
                else:
                    reporting = share
            cited = list(row[1].get("refs") or [])
    src = next((refs[r] for r in cited if r in refs and str(refs[r].get("url", "")).startswith("https://")), None)
    return {"rows": rows, "total": total, "reporting": reporting, "precincts": precincts, "outcome": None,
            "source": {"title": src["title"] or "Election results", "url": src["url"]} if src else None,
            "via": "infobox", "totalFromShares": approx}


def _has_count(box):
    return bool(box) and any(r.get("votes") is not None or r.get("pct") is not None for r in box["rows"] if not r.get("other"))


def page_box(html_text, refs):
    """The count on a statewide race page: its general-election box, or, while that box
    is still blank (candidates listed, no figures), the count in the page's infobox."""
    box = general_box(html_text, refs)
    if _has_count(box):
        return box
    return infobox_count(html_text, refs) or box


def match(name, cands, party=None):
    """el.match_candidate, also trying the name without a leading initial ("S. Brett
    Guthrie") and by a quoted nickname ('John "Drew" Williams')."""
    c = el.match_candidate(name, cands, party)
    toks = name.split()
    if c is None and len(toks) > 2 and re.fullmatch(r"[A-Z]\.?", toks[0]):
        c = el.match_candidate(" ".join(toks[1:]), cands, party)
    nick = re.search(r"[\"“']([^\"”']+)[\"”']", name)
    if c is None and nick and toks:
        c = el.match_candidate(f"{nick.group(1)} {toks[-1]}", cands, party)
    return c


def clean_note(status_text):
    s = re.sub(r"\s+", " ", status_text or "").strip()
    return s.replace(" .", ".")


def outcome_of(note):
    m = re.search(r"\b((?:[A-Z][\w-]*\s)*?(?:Democratic|Republican|Independent|Libertarian|Green|DFL|Forward|Nonpartisan)[\w-]*(?:\s[A-Z][\w-]*)*\s(?:hold|gain))\b", note or "")
    return m.group(1) if m else None


def build(race, winners, status_text, box, page=None, single_seat=True, advance=None):
    """The race's result, or None before anything is known. `winners` are the
    candidate dicts the national table check-marks (in a runoff's part of the cell
    when it has one); `advance` those listed for a runoff; `box` is parse_box's
    output for the race page (or None)."""
    to_runoff = bool(advance) and not winners
    if to_runoff:
        winners = advance
    note = clean_note(status_text)
    cands = race["candidates"]
    rows, fixed = [], False
    if box:
        for r in box["rows"]:
            c = None if r.get("other") else match(r["name"], cands, r["party"] if r["party"] in ("D", "R") else None)
            rows.append({"id": c["id"] if c else None, "name": c["name"] if c else r["name"],
                         "party": (c["party"] if c else r["party"]), "votes": r["votes"], "pct": r["pct"],
                         **({"mate": r["mate"]} if r.get("mate") else {}),
                         **({"final": r["final"]} if r.get("final") is not None else {})})
        counted = [r for r in rows if r["votes"] is not None]
        # A total below the candidates' own votes is a total not yet updated.
        base = max(box["total"] or 0, sum(r["votes"] for r in counted))
        fixed = False
        for r in counted:
            # Shares come from the counts the box cites: a blank share is filled in, and a
            # mistyped one (Iowa's governor box once printed 55.5% and 45.5%) is replaced.
            share = round(100 * r["votes"] / base, 2) if base else None
            if share is not None and (r["pct"] is None or abs(r["pct"] - share) > 0.3):
                fixed = fixed or r["pct"] is not None
                r["pct"] = share
        if not counted and not any(r["pct"] is not None for r in rows):
            rows = []  # the box is still blank: candidates listed, no counts yet
    win_ids = [w["id"] for w in winners]
    runoff = to_runoff or ("runoff" in note.lower() and not re.search(r"avoid(?:ed|ing)? (?:a )?runoff|no runoff", note, re.I))
    if win_ids and (len(win_ids) == 1 or not single_seat) and not (runoff and len(win_ids) > 1):
        status = "won"
    elif win_ids or runoff:
        status = "runoff"
    elif rows:
        status = "counting"
    else:
        return None
    out = {"status": status}
    if status == "won":
        out["winners"] = win_ids
    elif win_ids:
        out["advance"] = win_ids
    if rows:
        out["rows"] = rows
        out["total"] = max(box["total"] or 0, sum(r["votes"] for r in rows if r["votes"] is not None)) or None
        if box["reporting"] is not None:
            out["reporting"] = box["reporting"]
        if box.get("precincts") is not None:
            out["precincts"] = box["precincts"]
        if box["source"]:
            out["source"] = box["source"]
        if fixed:
            out["sharesFromVotes"] = True
        if box.get("via"):
            out["via"] = box["via"]
        if box.get("totalFromShares"):
            out["totalFromShares"] = True
    # "Democratic gain" is a call: a box can carry it before the race is called (MN-1's
    # did), so it is kept only once the national table marks the winner.
    outcome = (box or {}).get("outcome") or outcome_of(note)
    if outcome and status == "won":
        out["outcome"] = outcome
    if note:
        out["note"] = note
    if status == "won":
        parties = {c["party"] for c in winners}
        held = race.get("held")
        if held in ("D", "R", "I") and parties and held not in parties:
            out["flip"] = True
    if page:
        out["page"] = page
    return out
