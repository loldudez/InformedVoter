"""The forecast model in Python, mirroring js/model/forecast.js line for line.

The refresh pipeline uses it to compute every real race and the chamber-control
simulation. The site recomputes each race in the browser with the JavaScript
version and warns in the console if the two ever disagree (see `modelCheck`).
"""

import math
import random
from datetime import date, datetime

ELECTION_DAY = datetime(2026, 11, 3, 20, 0, 0)
POP_WEIGHT = {"LV": 1.0, "RV": 0.9, "A": 0.75}
HALF_LIFE_DAYS = 14.0
DEFAULT_N = 600            # polls that don't report a sample size count as a typical 600
NAT = 3.5                  # shared national polling miss on the margin, points (one per simulated election)

# How published ratings translate into an expected D-minus-R margin. A rating sets
# the band; the district's partisan lean (PVI plus the national environment)
# places the race inside it. Toss-ups stay within two points of even.
RATING_BANDS = {"safe": (15.0, 75.0), "solid": (15.0, 75.0), "likely": (7.0, 15.0), "lean": (3.0, 7.0), "tilt": (0.5, 3.0)}
RATING_SCORE = {"safe": 3.0, "solid": 3.0, "likely": 2.0, "lean": 1.0, "tilt": 0.5}


def parse_rating(text):
    """'Lean D (flip)' -> ('lean', 'D'); 'Tossup' -> ('toss', None); junk -> None."""
    t = (text or "").lower().replace("(flip)", "").replace("-", " ").strip()
    if t.startswith("toss"):
        return ("toss", None)
    parts = t.split()
    if len(parts) >= 2 and parts[0] in RATING_BANDS and parts[1] in ("d", "r"):
        return (parts[0], parts[1].upper())
    return None


def rating_margin(text, base):
    """Expected D-minus-R margin for one outlet's rating, given the partisan baseline
    `base` (None when unknown)."""
    p = parse_rating(text)
    if not p:
        return None
    word, side = p
    if word == "toss":
        return max(-2.0, min(2.0, base if base is not None else 0.0))
    lo, hi = RATING_BANDS[word]
    sign = 1.0 if side == "D" else -1.0
    x = (lo + hi) / 2 if base is None else base * sign
    if base is None and word in ("safe", "solid"):
        x = 25.0
    return sign * min(max(x, lo), hi)


def consensus(ratings, base):
    """Average of every outlet's rating -> {"rating", "margin", "outlets"}."""
    margins, scores = [], []
    for r in ratings:
        p = parse_rating(r["rating"])
        if not p:
            continue
        m = rating_margin(r["rating"], base)
        margins.append(m)
        scores.append(0.0 if p[0] == "toss" else RATING_SCORE[p[0]] * (1 if p[1] == "D" else -1))
    if not margins:
        return None
    s = sum(scores) / len(scores)
    a = abs(s)
    word = "Safe" if a >= 2.5 else "Likely" if a >= 1.5 else "Lean" if a >= 0.75 else "Tilt" if a >= 0.25 else None
    label = f"{word} {'D' if s > 0 else 'R'}" if word else "Toss-up"
    return {"rating": label, "margin": round(sum(margins) / len(margins), 2), "outlets": len(margins)}


def norm_cdf(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def _as_dt(d):
    if isinstance(d, datetime):
        return d
    if isinstance(d, date):
        return datetime(d.year, d.month, d.day)
    y, m, dd = (int(x) for x in str(d)[:10].split("-"))
    return datetime(y, m, dd)


def poll_average(polls, as_of):
    live = [p for p in polls or [] if _as_dt(p["end"]) <= as_of]
    if not live:
        return None
    acc, wts, total = {}, {}, 0.0
    for p in live:
        age = (as_of - _as_dt(p["end"])).total_seconds() / 86400
        n = p.get("n") or DEFAULT_N
        w = 0.5 ** (age / HALF_LIFE_DAYS) * math.sqrt(min(n, 2000) / 600) * POP_WEIGHT.get(p.get("pop"), 0.8)
        total += w
        for cid, v in p["results"].items():
            acc[cid] = acc.get(cid, 0.0) + w * v
            wts[cid] = wts.get(cid, 0.0) + w
    return {"shares": {k: acc[k] / wts[k] for k in acc}, "weight": total, "count": len(live)}


def blind_sigma(race):
    """Typical miss on the margin with no polls: tighter when forecasters have rated the race."""
    if race.get("priorKind") == "ratings":
        return 7.0 if race.get("statewide") else 8.0
    return 9.0 if race.get("statewide") else 11.0


def forecast(race, as_of=None):
    as_of = as_of or datetime.now()
    cands = race["candidates"]
    avg = poll_average(race.get("polls"), as_of)
    days = max(0.0, (ELECTION_DAY - as_of).total_seconds() / 86400)
    prior = race["prior"]
    k = 0.0
    shares = {}
    if avg:
        decided = sum(avg["shares"].get(c["id"], 0) for c in cands) or 1
        k = min(0.85, avg["weight"] / (avg["weight"] + 1.5))
        for c in cands:
            polled = avg["shares"].get(c["id"], 0) / decided * 100
            shares[c["id"]] = k * polled + (1 - k) * prior[c["id"]]
    else:
        for c in cands:
            shares[c["id"]] = prior[c["id"]]
    first = dict(shares) if race.get("rcv") else None
    final_avg = None
    if race.get("rcv"):
        shares.update(rcv_final(cands, shares))
        top2 = sorted(cands, key=lambda c: -shares[c["id"]])[:2]
        ids = {c["id"] for c in top2}
        final_polls = [p for p in race.get("finalPolls") or [] if len(ids) == 2 and set(p["results"]) == ids]
        final_avg = poll_average(final_polls, as_of)
        if final_avg:
            shares.update(final_round(cands, top2, final_avg, race.get("lean") or 0.0))
    if final_avg:
        poll_shares = final_avg["shares"]
    elif avg:
        poll_shares = rcv_final(cands, avg["shares"]) if race.get("rcv") else avg["shares"]
    else:
        poll_shares = None
    ranked = sorted(cands, key=lambda c: -shares[c["id"]])
    lead = ranked[0]
    second = ranked[1] if len(ranked) > 1 else None
    margin = shares[lead["id"]] - (shares[second["id"]] if second else 0)
    polled_sigma = 5.5 if race.get("statewide") else 7.0
    blind = blind_sigma(race)
    poll_sigma = blind - (blind - polled_sigma) * (k / 0.85)
    sigma = math.sqrt(poll_sigma ** 2 + 0.06 * days)
    p_lead = norm_cdf(margin / sigma) if second else 1.0
    # The margin reads as Democrat minus Republican only when they are the top two;
    # against an independent (Nebraska, Montana) it is the leader's margin instead.
    d_vs_r = second is not None and {lead["party"], second["party"]} == {"D", "R"}
    d = next((c for c in ranked if c["party"] == "D"), None)
    r = next((c for c in ranked if c["party"] == "R"), None)
    dr = shares[d["id"]] - shares[r["id"]] if d_vs_r else None
    poll_dr = None
    if d_vs_r and poll_shares and d["id"] in poll_shares and r["id"] in poll_shares:
        poll_dr = poll_shares[d["id"]] - poll_shares[r["id"]]
    return {"shares": shares, "first": first, "lead": lead, "second": second, "margin": margin, "dr": dr, "pollDR": poll_dr,
            "sigma": sigma, "pLead": p_lead, "poll": avg, "k": k}


def rcv_final(cands, shares):
    """Ranked-choice races (Alaska; Maine's federal races): in the final round each
    party's other candidates' votes go to its strongest candidate. Independent and
    third-party votes stay where they are."""
    out = dict(shares)
    for party in ("D", "R"):
        members = sorted((c for c in cands if c["party"] == party), key=lambda c: -(shares.get(c["id"]) or 0))
        if len(members) > 1:
            out[members[0]["id"]] = sum(shares.get(m["id"]) or 0 for m in members)
            for m in members[1:]:
                out[m["id"]] = 0.0
    return out


def final_round(cands, top2, avg_f, lean):
    """The final round of a ranked-choice race, on the two-way basis such polls
    report (finalists sum to 100, everyone else eliminated). Published final-round
    polls between the two finalists set the split, weighted like first-round polls;
    the rest comes from the forecasters' expected margin, so the result never leans
    on an assumption about how eliminated ballots transfer."""
    a, b = top2
    decided = (avg_f["shares"][a["id"]] + avg_f["shares"][b["id"]]) or 1
    kf = min(0.85, avg_f["weight"] / (avg_f["weight"] + 1.5))
    if (a["party"] == "R") != (b["party"] == "R"):
        non_r = b if a["party"] == "R" else a
        p_non_r = min(97.0, max(3.0, 50 + lean / 2)) / 100
        prior = {non_r["id"]: p_non_r, (a if non_r is b else b)["id"]: 1 - p_non_r}
    else:
        prior = {a["id"]: 0.5, b["id"]: 0.5}
    out = {c["id"]: 0.0 for c in cands}
    for c in (a, b):
        out[c["id"]] = 100 * (kf * avg_f["shares"][c["id"]] / decided + (1 - kf) * prior[c["id"]])
    return out


def main_contenders(cands):
    """The two sides the expected margin applies to: the strongest non-Republican
    (usually the Democrat; an independent where one leads the opposition, as in
    Nebraska or Montana) against the strongest Republican. With no Republican, the
    strongest Democrat against the next candidate. `cands` must be ordered
    strongest first (poll share, then incumbency, then money)."""
    r = next((c for c in cands if c["party"] == "R"), None)
    if r:
        a = next((c for c in cands if c["party"] != "R"), None) or next((c for c in cands if c is not r), None)
        return a, r
    d = next((c for c in cands if c["party"] == "D"), None)
    if d:
        return d, next((c for c in cands if c is not d), None)
    return (cands[0], cands[1]) if len(cands) > 1 else (cands[0], None)


def prior_shares(cands, margin_dr):
    """Baseline vote shares from an expected margin between the two main contenders
    (positive favors the Democratic or non-Republican side). Every other candidate
    gets two points, up to eight in all. Two candidates of the same party (a
    top-two runoff) start 56-44 toward the stronger one."""
    if len(cands) == 1:
        return {cands[0]["id"]: 100.0}
    a, b = main_contenders(cands)
    minors = [c for c in cands if c is not a and c is not b]
    rest = min(8.0, 2.0 * len(minors))
    if a["party"] == b["party"]:
        m = 12.0 if cands.index(a) < cands.index(b) else -12.0
    else:
        m = margin_dr
    share_a = min(97.0, max(3.0, 50 + m / 2))
    out = {c["id"]: rest / len(minors) for c in minors}
    out[a["id"]] = share_a * (100 - rest) / 100
    out[b["id"]] = (100 - share_a) * (100 - rest) / 100
    return out


def caucus(c):
    """Which side a winner counts for in chamber control."""
    if c.get("caucus") in ("D", "R"):
        return c["caucus"]
    return c["party"] if c["party"] in ("D", "R") else "O"


def _side(p):
    return 1.0 if p == "D" else -1.0 if p == "R" else 0.0


def sim_entry(race, f):
    """One race as the chamber simulation sees it: the top two contenders, the
    expected margin between them, its uncertainty, and how much a national swing
    toward Democrats moves it (1 for D vs R, 0.5 when one side is an independent)."""
    if race.get("format") == "open-primary":
        return {"id": race["id"], "a": "D", "b": "R", "m": float(race.get("lean") or 0.0), "sigma": blind_sigma(race), "nat": 1.0}
    lead, second = f["lead"], f["second"]
    a = caucus(lead)
    if second is None:
        return {"id": race["id"], "a": a, "b": a, "m": 100.0, "sigma": 1.0, "nat": 0.0}
    b = caucus(second)
    return {"id": race["id"], "a": a, "b": b, "m": f["margin"], "sigma": f["sigma"], "nat": (_side(a) - _side(b)) / 2}


def simulate_control(entries, hold_d, hold_r, d_needs, r_needs, sims=20000, seed=2026):
    """Seat totals over `sims` simulated elections. Every simulation draws one
    national polling miss shared by all races, so races move together the way they
    do on a real election night."""
    rnd = random.Random(seed)
    dist_d, dist_r = {}, {}
    d_ctrl = r_ctrl = 0
    sum_d = sum_r = 0
    for _ in range(sims):
        nat = rnd.gauss(0, NAT)
        d, r = hold_d, hold_r
        for e in entries:
            if e["a"] == e["b"]:
                w = e["a"]
            else:
                local = math.sqrt(max(e["sigma"] ** 2 - (NAT * e["nat"]) ** 2, 4.0))
                w = e["a"] if e["m"] + e["nat"] * nat + rnd.gauss(0, local) > 0 else e["b"]
            if w == "D":
                d += 1
            elif w == "R":
                r += 1
        dist_d[d] = dist_d.get(d, 0) + 1
        dist_r[r] = dist_r.get(r, 0) + 1
        sum_d += d
        sum_r += r
        d_ctrl += d >= d_needs
        r_ctrl += r >= r_needs

    def quantiles(dist):
        acc, q = 0, {}
        for s in sorted(dist):
            acc += dist[s]
            for name, cut in (("lo", 0.1), ("median", 0.5), ("hi", 0.9)):
                if name not in q and acc >= sims * cut:
                    q[name] = s
        return q

    qd, qr = quantiles(dist_d), quantiles(dist_r)
    return {
        "pD": d_ctrl / sims, "pR": r_ctrl / sims, "pNone": max(0.0, 1 - (d_ctrl + r_ctrl) / sims),
        "meanD": sum_d / sims, "meanR": sum_r / sims,
        "medianD": qd["median"], "medianR": qr["median"],
        "range80D": [qd["lo"], qd["hi"]], "range80R": [qr["lo"], qr["hi"]],
        "sims": sims, "distD": {str(k): v for k, v in sorted(dist_d.items())},
    }
