"""Recorded U.S. Senate votes, turned into sourced positions on the site's questions
under the same rules as house_votes.py.

senate.gov refuses scripted reads (and shows a bot check even in a browser), so the
votes come from Voteview (UCLA's roll-call database: Lewis, Poole, Rosenthal, Boche,
Rudkin and Sonnet), which copies the Senate's own records into one file of roll calls,
one of members and one of votes per Congress. Each position cites the roll call's page
on voteview.com, which shows the bill, the question and how every senator voted.

Roll calls of finished Congresses never change and are downloaded once; the current
Congress's files are read again when they are over a day old. Every roll call used is
checked against the bill number written here, so a typo can't attach a senator's vote
to the wrong bill.
"""

import csv
import io
import re
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CACHE = ROOT / "data" / "cache" / "votes" / "voteview"
BASE = "https://voteview.com/static/data/out"
UA = "InformedVoterResearch/1.0"
CONGRESSES = (117, 118, 119)
CURRENT = 119
MAX_AGE = 24 * 3600

# key: (congress, roll number in Voteview's count for that Congress, bill as Voteview
# numbers it, date, what was voted on). Same strengths as house_votes.py: a vote counts
# for the question it squarely answers, at full strength for single-issue bills and half
# for broader packages; "no" votes on packages say nothing.
SENATE_VOTES = {
    "rfma": (117, 890, "HR8404", "2022-11-29", "passage of the Respect for Marriage Act (H.R. 8404)"),
    "whpa": (117, 698, "S4132", "2022-05-11", "cloture on the Women’s Health Protection Act (S. 4132), to protect abortion access in federal law"),
    "rfwa": (118, 563, "S4554", "2024-07-10", "cloture on the Reproductive Freedom for Women Act (S. 4554), supporting the abortion protections of Roe v. Wade"),
    "ira": (117, 853, "HR5376", "2022-08-07", "passage of the Inflation Reduction Act (H.R. 5376), which let Medicare negotiate drug prices, extended ACA premium subsidies and funded clean energy tax credits"),
    "aca_2025": (119, 644, "S3385", "2025-12-11", "cloture on S. 3385, a three-year extension of the enhanced Affordable Care Act premium tax credits"),
    "iija": (117, 314, "HR3684", "2021-08-10", "passage of the Infrastructure Investment and Jobs Act (H.R. 3684)"),
    "chips": (117, 799, "HR4346", "2022-07-27", "final passage of the CHIPS and Science Act (H.R. 4346), funding domestic semiconductor manufacturing"),
    "hr1_2025": (119, 372, "HR1", "2025-07-01", "passage of H.R. 1 (2025), the tax and spending law that cut federal Medicaid spending, phased out clean energy tax credits and funded border and immigration enforcement"),
    "ukraine_2022": (117, 719, "HR7691", "2022-05-19", "passage of H.R. 7691, emergency aid for Ukraine"),
    "supplemental_2024": (118, 506, "HR815", "2024-04-23", "final passage of H.R. 815 (2024), military aid for Ukraine, Israel and Taiwan"),
    "ukraine_2025": (119, 178, "HCONRES14", "2025-04-04", "an amendment to the 2025 budget resolution “to prevent any disruption in security assistance to Ukraine”"),
    "russia_2026": (119, 883, "HR5334", "2026-08-07", "passage of H.R. 5334 (2026), sanctions on the Russian Federation"),
    "icc": (119, 22, "HR23", "2025-01-28", "cloture on the Illegitimate Court Counteraction Act (H.R. 23), sanctioning the International Criminal Court over its cases against Israeli officials"),
    "rescissions": (119, 411, "HR4", "2025-07-17", "passage of the Rescissions Act of 2025 (H.R. 4), canceling about $9 billion in foreign aid and public broadcasting funds"),
    "laken_riley": (119, 7, "S5", "2025-01-20", "passage of the Laken Riley Act (S. 5), requiring immigration detention for people in the country illegally who are charged with theft or violent crimes"),
    "methane_fee": (119, 97, "HJRES35", "2025-02-27", "H.J.Res. 35 (2025), repealing the EPA’s charge on methane emissions from oil and gas operations"),
    "ca_cars": (119, 277, "HJRES88", "2025-05-22", "H.J.Res. 88 (2025), revoking California’s permission to set stricter vehicle emission standards (Advanced Clean Cars II)"),
    "sports": (119, 100, "S9", "2025-03-03", "cloture on the Protection of Women and Girls in Sports Act (S. 9), barring transgender women and girls from women’s and girls’ school sports"),
    "student_loans": (118, 135, "HJRES45", "2023-06-01", "H.J.Res. 45 (2023), overturning the Education Department’s student debt relief program"),
    "min_wage_2021": (117, 74, "HR1319", "2021-03-05", "the motion to waive the budget rules for an amendment raising the federal minimum wage to $15 (H.R. 1319)"),
    "min_wage_2025": (119, 184, "HCONRES14", "2025-04-05", "an amendment to the 2025 budget resolution to let the Senate raise the federal minimum wage to $17 an hour by a simple majority"),
    "disclose": (117, 874, "S4822", "2022-09-22", "cloture on the DISCLOSE Act (S. 4822), requiring groups that spend on elections to disclose donors of $10,000 or more"),
    "stock_trading": (119, 912, "HR7008", "2026-09-30", "cloture on the Stop Insider Trading Act (H.R. 7008), barring members of Congress from buying individual stocks and adding a photo ID requirement for voting"),
    "pact": (117, 808, "S3373", "2022-08-02", "final passage of the PACT Act (S. 3373), expanding health care and benefits for veterans exposed to toxic burn pits"),
    "freedom_to_vote": (117, 537, "HR5746", "2022-01-19", "cloture on the Freedom to Vote: John R. Lewis Act (H.R. 5746), which set national minimums for early voting and voting by mail"),
    "scholarships": (119, 358, "HR1", "2025-07-01", "an amendment to strike H.R. 1’s tax credit for scholarships to private and religious schools"),
    # Added Nov. 27, 2026 (owner's request: positions on oil and gas, renewable energy,
    # money in politics and immigration from the voting record first).
    "clean_credits_2025": (119, 366, "HR1", "2025-07-01", "an amendment to H.R. 1 (2025) to keep the clean energy tax credits the bill was ending"),
    "anwr_2025": (119, 632, "HJRES131", "2025-12-04", "H.J.Res. 131 (2025), overturning the Biden administration’s 2024 decision limiting oil and gas leasing on the coastal plain of the Arctic National Wildlife Refuge"),
    "leasing_2021": (117, 320, "SCONRES14", "2021-08-10", "an amendment to the 2021 budget resolution to cancel the Biden administration’s pause on new oil and gas leasing on federal land"),
    "super_pacs_2026": (119, 807, "S2", "2026-06-04", "a motion during the 2026 budget reconciliation debate (S. 2) to place reasonable limits on contributions to super PACs"),
    "border_2024": (118, 534, "S4361", "2024-05-23", "cloture on S. 4361 (2024), emergency funding for border security and against fentanyl"),
}

# Resolutions ending the national emergencies behind the 2025 tariffs. A "yes" is a vote
# against those tariffs.
TARIFFS = {
    "tariff_canada_1": (119, 160, "SJRES37", "2025-04-02", "Canada"),
    "tariff_global_1": (119, 225, "SJRES49", "2025-04-30", "imports from every country"),
    "tariff_brazil": (119, 594, "SJRES81", "2025-10-28", "Brazil"),
    "tariff_canada_2": (119, 598, "SJRES77", "2025-10-29", "Canada"),
    "tariff_global_2": (119, 600, "SJRES88", "2025-10-30", "imports from every country"),
}

# Resolutions disapproving arms sales to Israel. A "yes" is a vote to block the sale.
ISRAEL_ARMS = {
    "arms_2024_1": (118, 644, "SJRES111", "2024-11-20"),
    "arms_2024_2": (118, 645, "SJRES113", "2024-11-20"),
    "arms_2024_3": (118, 646, "SJRES115", "2024-11-20"),
    "arms_2025_1": (119, 165, "SJRES33", "2025-04-03"),
    "arms_2025_2": (119, 166, "SJRES26", "2025-04-03"),
    "arms_2025_3": (119, 454, "SJRES41", "2025-07-30"),
    "arms_2025_4": (119, 455, "SJRES34", "2025-07-30"),
    "arms_2026_1": (119, 739, "SJRES32", "2026-04-15"),
    "arms_2026_2": (119, 740, "SJRES138", "2026-04-15"),
}

# War powers resolutions directing the president to withdraw U.S. forces from
# hostilities Congress hasn't authorized: motions to discharge or proceed and the votes
# on the resolutions themselves, where "yes" is for the resolution. Points of order,
# where "yes" counts against it, are left out.
WAR_POWERS = {
    "wp_hemisphere": (119, 555, "SJRES83", "2025-10-08", "unauthorized hostilities (the boat strikes)"),
    "wp_venezuela_1": (119, 608, "SJRES90", "2025-11-06", "Venezuela"),
    "wp_venezuela_2": (119, 664, "SJRES98", "2026-01-08", "Venezuela"),
}
IRAN_WAR_POWERS = {
    "wp_iran_1": (119, 328, "SJRES59", "2025-06-27", "Iran"),
    "wp_iran_2": (119, 705, "SJRES104", "2026-03-04", "Iran"),
    "wp_iran_3": (119, 717, "SJRES118", "2026-03-18", "Iran"),
    "wp_iran_4": (119, 728, "SJRES116", "2026-03-24", "Iran"),
    "wp_iran_5": (119, 738, "SJRES123", "2026-04-15", "Iran"),
    "wp_iran_6": (119, 747, "SJRES114", "2026-04-22", "Iran"),
    "wp_iran_7": (119, 772, "SJRES184", "2026-04-30", "Iran"),
    "wp_iran_8": (119, 777, "SJRES163", "2026-05-13", "Iran"),
    "wp_iran_9": (119, 788, "SJRES185", "2026-05-19", "Iran"),
    "wp_iran_10": (119, 833, "SJRES172", "2026-06-16", "Iran"),
    "wp_iran_11": (119, 843, "HCONRES86", "2026-06-23", "Iran"),
    "wp_iran_12": (119, 851, "SJRES185", "2026-06-24", "Iran"),
    "wp_iran_13": (119, 866, "SJRES180", "2026-07-23", "Iran"),
    "wp_iran_14": (119, 875, "SJRES181", "2026-07-30", "Iran"),
    "wp_iran_15": (119, 903, "HCONRES89", "2026-09-24", "Iran"),
    "wp_iran_16": (119, 928, "HCONRES93", "2026-11-19", "Iran"),
}

ALL_ROLLS = {
    **{k: v[:4] for k, v in SENATE_VOTES.items()},
    **{k: v[:4] for k, v in TARIFFS.items()},
    **ISRAEL_ARMS,
    **{k: v[:4] for k, v in WAR_POWERS.items()},
    **{k: v[:4] for k, v in IRAN_WAR_POWERS.items()},
}

YEA, NAY = 1, 6  # Voteview's cast codes for a recorded yea and nay (paired and announced votes don't count)


def _get(kind, congress, chamber="S"):
    """One of Voteview's files for a Congress: the Senate's ("S"), or the House's ("H",
    nominate.py's member files)."""
    name = f"{chamber}{congress}_{kind}.csv"
    path = CACHE / name
    fresh = path.exists() and (congress != CURRENT or time.time() - path.stat().st_mtime < MAX_AGE)
    if not fresh:
        CACHE.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(f"{BASE}/{kind}/{name}", headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                body = r.read()
            if not body.startswith(b"congress,"):
                raise ValueError("not a Voteview CSV")
            path.write_bytes(body)
        except Exception:
            if not path.exists():
                raise
            # An old copy still answers every vote cast before it was saved.
    return list(csv.DictReader(io.StringIO(path.read_text(encoding="utf-8"))))


def vote_url(congress, roll):
    return f"https://voteview.com/rollcall/RS{congress}{roll:04d}"


class SenateRecord:
    """Every senator's recorded votes on the roll calls above, 2021 onward."""

    def __init__(self):
        self.rolls = {}      # (congress, roll) -> roll-call row
        self.members = {}    # icpsr -> member row (latest Congress they served in)
        self.cast = {}       # (congress, roll) -> {icpsr: "Yea"|"Nay"}
        self.problems = []
        want = {(c, r) for c, r, *_ in ALL_ROLLS.values()}
        for cong in CONGRESSES:
            for row in _get("rollcalls", cong):
                key = (int(row["congress"]), int(row["rollnumber"]))
                if key in want:
                    self.rolls[key] = row
            for row in _get("members", cong):
                if row["chamber"] == "Senate":
                    self.members[row["icpsr"]] = row
            for row in _get("votes", cong):
                key = (int(row["congress"]), int(row["rollnumber"]))
                if row["chamber"] != "Senate" or key not in want:
                    continue
                code = int(float(row["cast_code"]))
                if code in (YEA, NAY):
                    self.cast.setdefault(key, {})[row["icpsr"]] = "Yea" if code == YEA else "Nay"
        for k, (c, r, bill, date) in ALL_ROLLS.items():
            row = self.rolls.get((c, r))
            if not row:
                self.problems.append(f"{k}: roll call {r} of the {c}th Congress not in Voteview's file")
            elif row["bill_number"] != bill or row["date"] != date:
                self.problems.append(f"{k}: roll call {r} of the {c}th Congress is {row['bill_number']} on {row['date']}, not {bill} on {date}")
                self.rolls.pop((c, r))
        self.by_bioguide = {m["bioguide_id"]: icpsr for icpsr, m in self.members.items() if m.get("bioguide_id")}

    def senate_roll(self, key):
        """The Senate's own number for a roll call (its clerk's count within the session)."""
        c, r = ALL_ROLLS[key][:2]
        row = self.rolls.get((c, r))
        return row and row.get("clerk_rollnumber") or r

    def find(self, state, name, bioguide=None):
        """The Voteview id of a senator, by Bioguide id or else by state and last name."""
        if bioguide and bioguide in self.by_bioguide:
            return self.by_bioguide[bioguide]
        last = _norm(_last_name(name))
        first = _norm(name.split()[0]) if name.split() else ""
        hits = []
        for icpsr, m in self.members.items():
            if m["state_abbrev"] != state:
                continue
            vlast, vfirst = (m["bioname"].split(",", 1) + [""])[:2]
            if _norm(vlast) == last or _norm(vlast).endswith(last) or last.endswith(_norm(vlast)):
                hits.append((icpsr, _norm(vfirst)))
        if len(hits) > 1 and first:
            hits = [h for h in hits if first[:3] in h[1]] or hits
        return hits[0][0] if len(hits) == 1 else None

    def votes_of(self, icpsr):
        """{key: "Yea"|"Nay"} for one senator."""
        out = {}
        for k, (c, r, *_) in ALL_ROLLS.items():
            if (c, r) in self.rolls:
                v = self.cast.get((c, r), {}).get(icpsr)
                if v:
                    out[k] = v
        return out


def _norm(s):
    import unicodedata
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z]", "", s.lower())


def _last_name(name):
    parts = [p for p in re.sub(r"\(.*?\)|,?\s+(Jr\.?|Sr\.?|II|III|IV)$", "", name).split() if p]
    return parts[-1] if parts else name


def _src(title, url, date):
    return {"title": title, "url": url, "date": date}


def senate_vote(rec, key, member, vote):
    c, r, bill, date = ALL_ROLLS[key][:4]
    what = SENATE_VOTES[key][4]
    year = date[:4]
    return _src(f"U.S. Senate roll call vote {rec.senate_roll(key)} ({year}) on {what}: {member} voted {vote}",
                vote_url(c, r), date)


def run_source(rec, keys, member, cast, about, what_yes):
    """One source for a run of votes on one question: how many, how the member voted,
    linked to the most recent one they cast."""
    last = max(cast, key=lambda kv: ALL_ROLLS[kv[0]][3])[0]
    c, r, _, date = ALL_ROLLS[last][:4]
    yes = sum(1 for _, v in cast if v == "Yea")
    no = len(cast) - yes
    how = (f"{member} voted for all {len(cast)}" if no == 0 and len(cast) > 1 else
           f"{member} voted against all {len(cast)}" if yes == 0 and len(cast) > 1 else
           f"{member} voted {'for' if yes else 'against'} it" if len(cast) == 1 else
           f"{member} voted for {yes} and against {no}")
    years = sorted({ALL_ROLLS[k][3][:4] for k, _ in cast})
    span = years[0] if len(years) == 1 else f"{years[0]}-{years[-1][2:]}"
    return _src(f"U.S. Senate votes on {about} ({len(cast)} roll call{'s' if len(cast) > 1 else ''}, {span}), {what_yes}: {how}; "
                f"latest, roll call vote {rec.senate_roll(last)} ({date[:4]})", vote_url(c, r), date)


def run_stance(cast, sign=1, cap=2):
    """As in house_votes.py: all one way counts fully once there are three or more votes,
    a lopsided record (3 in 4) at half strength, an even split as mixed."""
    yes = sum(1 for _, v in cast if v == "Yea")
    share = yes / len(cast)
    if share == 1:
        s = 2 if len(cast) >= 3 else 1
    elif share == 0:
        s = -2 if len(cast) >= 3 else -1
    elif share >= 0.75:
        s = 1
    elif share <= 0.25:
        s = -1
    else:
        s = 0
    s = max(-cap, min(cap, s))
    return s * sign


def vote_positions(rec, member, votes):
    """Standard positions from a senator's recorded votes: [(question, stance, source, quote)].
    Each question is answered once; the first rule listed for it wins, and a rule that
    `stops` keeps a vote that says nothing from falling through to an older one."""
    out = {}
    closed = set()

    def put(q, key, yea, nay=None, stops=False):
        if q in out or q in closed or votes.get(key) not in ("Yea", "Nay"):
            return
        s = yea if votes[key] == "Yea" else nay
        if s is None:
            if stops:
                closed.add(q)
            return
        out[q] = (s, senate_vote(rec, key, member, votes[key]))

    put("soc-10", "rfma", 2, -1)
    put("soc-03", "whpa", 2, -1)
    put("soc-03", "rfwa", 1, -1)
    put("hea-07", "aca_2025", 2, -1)
    put("hea-07", "ira", 1, -1)
    put("hea-02", "ira", 1, -1)
    put("hea-03", "hr1_2025", -1)
    put("eco-06", "iija", 1, -1)
    put("agr-02", "chips", 1, -1)
    # Ukraine: the 2024 package (a "no" may be about its Israel aid, so it says nothing and
    # ends the search), else the 2022 Ukraine-only bill, else the 2025 budget amendment.
    put("def-13", "supplemental_2024", 1, None, stops=True)
    put("def-13", "ukraine_2022", 2, -2)
    put("def-13", "ukraine_2025", 1)
    put("def-14", "russia_2026", 1)
    put("def-11", "icc", 1)
    put("def-10", "rescissions", 1, -1)
    put("imm-07", "laken_riley", 1)
    put("imm-01", "border_2024", 1)
    put("imm-01", "hr1_2025", 1)
    put("imm-08", "hr1_2025", 1)
    put("ene-06", "methane_fee", -1, 1)
    put("ene-04", "ca_cars", -1, 1)
    put("ene-03", "anwr_2025", 1, -1)
    put("ene-03", "leasing_2021", 1, -1)
    # Renewable energy: the 2025 amendment to keep the clean energy credits, else H.R. 1's
    # "yes" (it phased them out), else the 2022 law that created most of them.
    put("ene-01", "clean_credits_2025", 1, -1)
    put("ene-01", "hr1_2025", -1)
    put("ene-01", "ira", 1, -1)
    put("soc-12", "sports", -1, 1)
    put("edu-05", "student_loans", -1, 1)
    put("edu-06", "scholarships", -1, 1)
    put("eco-03", "min_wage_2021", 1)
    put("eco-03", "min_wage_2025", 1)
    put("gov-03", "disclose", 2, -1)
    # A motion during a reconciliation vote-a-rama: only a "yes" says something.
    put("gov-11", "super_pacs_2026", 1)
    put("gov-02", "stock_trading", 1)
    put("gov-05", "stock_trading", 1)
    put("def-03", "pact", 1)
    put("gov-06", "freedom_to_vote", 1)

    # Arms sales to Israel: a record of votes to block them is against military aid to
    # Israel, a record of votes to let them go ahead is for it, at half strength either
    # way (the resolutions covered particular weapons); the 2024 aid package's "yes" next.
    cast = [(k, votes[k]) for k in ISRAEL_ARMS if votes.get(k) in ("Yea", "Nay")]
    if cast:
        out.setdefault("def-12", (run_stance(cast, sign=-1, cap=1),
                                  run_source(rec, list(ISRAEL_ARMS), member, cast, "resolutions blocking arms sales to Israel",
                                             "where “yes” was a vote to block the sale")))
    put("def-12", "supplemental_2024", 1)
    # Tariffs: votes to end the national emergencies behind them, at half strength (a vote
    # can be about the emergency powers as much as the tariffs).
    cast = [(k, votes[k]) for k in TARIFFS if votes.get(k) in ("Yea", "Nay")]
    if cast:
        out["eco-10"] = (run_stance(cast, sign=-1, cap=1),
                         run_source(rec, list(TARIFFS), member, cast,
                                    "resolutions ending the national emergencies behind the 2025 tariffs on "
                                    + ", ".join(sorted({TARIFFS[k][4] for k, _ in cast})),
                                    "where “yes” was a vote to end the tariffs"))
    # War powers: every resolution answers whether Congress should authorize prolonged
    # hostilities; the Iran ones also whether to keep intervening there.
    all_wp = list(WAR_POWERS) + list(IRAN_WAR_POWERS)
    cast = [(k, votes[k]) for k in all_wp if votes.get(k) in ("Yea", "Nay")]
    if cast:
        targets = sorted({(WAR_POWERS.get(k) or IRAN_WAR_POWERS.get(k))[4] for k, _ in cast})
        out["def-04"] = (run_stance(cast), run_source(rec, all_wp, member, cast, "war powers resolutions on " + ", ".join(targets),
                                                      "directing the withdrawal of U.S. forces from hostilities Congress hadn't authorized"))
    cast = [(k, votes[k]) for k in IRAN_WAR_POWERS if votes.get(k) in ("Yea", "Nay")]
    if cast:
        out["def-15"] = (run_stance(cast, sign=-1), run_source(rec, list(IRAN_WAR_POWERS), member, cast, "war powers resolutions on Iran",
                                                               "directing the withdrawal of U.S. forces from hostilities with Iran"))
    return [(q, s, src, None) for q, (s, src) in out.items()]
