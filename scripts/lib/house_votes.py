"""Recorded U.S. House votes, from the House Clerk's official roll-call XML, turned
into sourced positions on the site's questions.

Used two ways: by the research scripts for hand-checked members, and by
update_races.py for every current House member on the 2026 ballot (re-election,
or a run for Senate or governor). Votes never change, so each roll call is
downloaded once and cached.
"""

import re
import time
import urllib.request
from pathlib import Path

from elections import first_names_match, norm

ROOT = Path(__file__).resolve().parents[2]
CACHE = ROOT / "data" / "cache" / "votes"
UA = "InformedVoter/1.0 (personal election-information site; data refresh script)"

# A vote counts for the question it squarely answers, at full strength (2) for
# single-issue bills and half strength (1) for broader packages. A "no" on the
# marriage and abortion-rights bills counts at half strength, since members gave
# narrower reasons for opposing those particular texts. Omnibus "no" votes that
# could mean many things (H.R. 2 in 2023, the 2023 energy bill, H.R. 1 in 2025)
# are used only for "yes" votes.
#
# The 2025-26 votes give members first elected in 2024 positions too, and cover
# topics the older set misses. Where a newer vote answers the same question as an
# older one (energy, health subsidies), the newer vote is used.
HOUSE_VOTES = {
    "rfma": (2022, 513, "the Respect for Marriage Act (H.R. 8404)", "2022-12-08"),
    "whpa": (2022, 360, "the Women’s Health Protection Act (H.R. 8296), to protect abortion access in federal law", "2022-07-15"),
    "ira": (2022, 420, "the Inflation Reduction Act (H.R. 5376), which let Medicare negotiate drug prices and extended ACA premium subsidies", "2022-08-12"),
    "iija": (2021, 369, "the Infrastructure Investment and Jobs Act (H.R. 3684)", "2021-11-05"),
    "chips": (2022, 404, "the CHIPS and Science Act (H.R. 4346), funding domestic semiconductor manufacturing", "2022-07-28"),
    "hr1_2025": (2025, 190, "H.R. 1 (2025), the tax and spending law that cut federal Medicaid spending", "2025-07-03"),
    "ukraine": (2024, 151, "H.R. 8035, military aid for Ukraine", "2024-04-20"),
    "israel": (2024, 152, "H.R. 8034, military aid for Israel", "2024-04-20"),
    "border": (2023, 209, "the Secure the Border Act (H.R. 2), funding border wall construction and more Border Patrol agents", "2023-05-11"),
    "energy": (2023, 182, "the Lower Energy Costs Act (H.R. 1, 2023), expanding oil and gas leasing and permitting", "2023-03-30"),
    "icc": (2025, 7, "the Illegitimate Court Counteraction Act (H.R. 23), sanctioning the International Criminal Court over its cases against Israeli officials", "2025-01-09"),
    "sports": (2025, 12, "the Protection of Women and Girls in Sports Act (H.R. 28), barring transgender women and girls from women’s and girls’ school sports", "2025-01-14"),
    "laken_riley": (2025, 23, "the Laken Riley Act (S. 5), requiring immigration detention for people in the country illegally who are charged with theft or violent crimes", "2025-01-22"),
    "fracking": (2025, 35, "the Protecting American Energy Production Act (H.R. 26), barring a president from declaring a moratorium on fracking", "2025-02-07"),
    "methane_fee": (2025, 52, "H.J.Res. 35 (2025), repealing the EPA’s charge on methane emissions from oil and gas operations", "2025-02-26"),
    "ca_cars": (2025, 114, "H.J.Res. 88 (2025), revoking California’s permission to set stricter vehicle emission standards (Advanced Clean Cars II)", "2025-05-01"),
    "rescissions": (2025, 168, "the Rescissions Act of 2025 (H.R. 4), canceling about $9.4 billion in foreign aid and public broadcasting funds", "2025-06-12"),
    "lng": (2025, 304, "the Unlocking our Domestic LNG Potential Act (H.R. 1949), easing approval of natural gas exports", "2025-11-20"),
    "workforce": (2025, 332, "the Protect America’s Workforce Act (H.R. 2550), restoring collective bargaining rights for federal workers", "2025-12-11"),
    "minors_care": (2025, 351, "the Protect Children’s Innocence Act (H.R. 3492), making it a federal crime to provide gender-transition treatment to minors", "2025-12-17"),
    "aca_2026": (2026, 11, "H.R. 1834 (2026), a three-year extension of the enhanced Affordable Care Act premium tax credits", "2026-01-08"),
    "minerals": (2026, 55, "the Critical Mineral Dominance Act (H.R. 4090)", "2026-02-04"),
    "canada_tariffs": (2026, 65, "H.J.Res. 72 (2026), ending the national emergency behind the 25% tariffs on Canadian goods", "2026-02-11"),
    "bba": (2026, 95, "H.J.Res. 139 (2026), a constitutional amendment requiring a balanced federal budget", "2026-03-18"),
    "farm_bill": (2026, 154, "the Farm, Food, and National Security Act of 2026 (H.R. 7567), the farm bill", "2026-04-30"),
    "ukraine_2026": (2026, 207, "the Ukraine Support Act (H.R. 2913), with military aid and loans for Ukraine and new sanctions on Russia", "2026-06-04"),
    "faster_labor": (2026, 216, "the Faster Labor Contracts Act (H.R. 5408), setting deadlines for first union contracts", "2026-06-09"),
    "stock_trading": (2026, 280, "the Stop Insider Trading Act (H.R. 7008), barring members of Congress from buying individual stocks and adding a photo ID requirement for voting", "2026-07-22"),
}

# War powers resolutions directing the president to withdraw U.S. forces from
# hostilities Congress hasn't authorized. A "yes" insists on congressional
# authorization; the Iran ones also answer whether to keep intervening there.
WAR_POWERS = {
    "wp_hemisphere": (2025, 345, "groups in the Western Hemisphere", "2025-12-17"),
    "wp_venezuela": (2025, 346, "Venezuela", "2025-12-17"),
    "wp_venezuela_2": (2026, 48, "Venezuela", "2026-01-22"),
    "wp_lebanon": (2026, 201, "Lebanon", "2026-06-04"),
    "wp_lebanon_2": (2026, 232, "Lebanon", "2026-06-30"),
}
IRAN_WAR_POWERS = {
    "wp_iran_1": (2026, 85, "Iran", "2026-03-05"),
    "wp_iran_2": (2026, 114, "Iran", "2026-04-16"),
    "wp_iran_3": (2026, 170, "Iran", "2026-05-14"),
    "wp_iran_4": (2026, 199, "Iran", "2026-06-03"),
    "wp_iran_5": (2026, 282, "Iran", "2026-07-23"),
    "wp_iran_6": (2026, 307, "Iran", "2026-09-15"),
}
HOUSE_VOTES.update({k: (y, r, f"a war powers resolution on {target}", d) for k, (y, r, target, d) in {**WAR_POWERS, **IRAN_WAR_POWERS}.items()})


def _src(title, url, date):
    return {"title": title, "url": url, "date": date}


def house_vote(key, member, vote):
    year, roll, bill, date = HOUSE_VOTES[key]
    return _src(f"U.S. House roll call {roll} ({year}) on {bill}: {member} voted {vote}",
                f"https://clerk.house.gov/Votes/{year}{roll:03d}", date)


def war_powers_source(keys, member, votes, cast):
    """One source for a run of war powers votes: how many, how the member voted,
    linked to the most recent roll call they voted on."""
    last = max(cast, key=lambda kv: HOUSE_VOTES[kv[0]][3])[0]
    year, roll, _, date = HOUSE_VOTES[last]
    yes = sum(1 for _, v in cast if v == "Yea")
    no = len(cast) - yes
    targets = sorted({(WAR_POWERS.get(k) or IRAN_WAR_POWERS.get(k))[2] for k, _ in cast})
    how = (f"{member} voted for all {len(cast)}" if no == 0 and len(cast) > 1 else
           f"{member} voted against all {len(cast)}" if yes == 0 and len(cast) > 1 else
           f"{member} voted {'for' if yes else 'against'} it" if len(cast) == 1 else
           f"{member} voted for {yes} and against {no}")
    return _src(f"U.S. House war powers resolutions on {', '.join(targets)} ({len(cast)} roll call{'s' if len(cast) > 1 else ''}, 2025-26), "
                f"directing the withdrawal of U.S. forces from hostilities Congress hadn't authorized: {how}; latest, roll call {roll} ({year})",
                f"https://clerk.house.gov/Votes/{year}{roll:03d}", date)


def run_stance(cast, sign=1):
    """A stance from several votes on one question: all one way counts fully once
    there are three or more, a lopsided record (3 in 4) at half strength, and an
    even split as mixed."""
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
    return s * sign


def vote_positions(member, votes):
    """Standard positions from a member's recorded votes: [(question, stance, source, quote)].
    votes: {key: 'Yea'|'Nay'|'Aye'|'No'} (missing = not in office or not voting).
    Each question is answered once; where several votes could answer it, the first
    rule listed for it wins."""
    out = {}
    v = lambda k: {"Aye": "Yea", "No": "Nay"}.get(votes.get(k), votes.get(k))  # noqa: E731
    shown = lambda k: votes.get(k)  # noqa: E731  as the Clerk recorded it

    def put(q, key, yea, nay=None):
        """Answer q from vote `key`: stance `yea` for a yes, `nay` for a no (None: a no says nothing)."""
        if q in out or v(key) not in ("Yea", "Nay"):
            return
        s = yea if v(key) == "Yea" else nay
        if s is not None:
            out[q] = (s, house_vote(key, member, shown(key)))

    put("soc-10", "rfma", 2, -1)
    put("soc-03", "whpa", 2, -1)
    put("hea-02", "ira", 1, -1)
    put("hea-07", "aca_2026", 2, -1)
    put("hea-07", "ira", 1, -1)
    put("eco-06", "iija", 1, -1)
    put("agr-02", "chips", 1, -1)
    put("hea-03", "hr1_2025", -1)
    put("def-13", "ukraine", 2, -2)
    put("def-13", "ukraine_2026", 1, -1)
    put("def-14", "ukraine_2026", 1)
    put("def-12", "israel", 2, -2)
    put("def-11", "icc", 1)
    put("def-10", "rescissions", 1, -1)
    put("imm-01", "border", 1)
    put("imm-07", "laken_riley", 1)
    put("ene-03", "fracking", 1, -1)
    put("ene-03", "lng", 1, -1)
    put("ene-03", "energy", 1)
    put("ene-06", "methane_fee", -1, 1)
    put("ene-04", "ca_cars", -1, 1)
    put("soc-12", "sports", -1, 1)
    put("soc-11", "minors_care", -2, 1)
    put("agr-05", "minerals", 1)
    put("agr-01", "farm_bill", 1)
    put("eco-10", "canada_tariffs", -1, 1)
    put("eco-07", "bba", 1, -1)
    put("gov-02", "stock_trading", 1)
    put("gov-05", "stock_trading", 1)
    # Two votes on union bargaining rights: both yes, or both no, count fully.
    labor = [(k, v(k)) for k in ("workforce", "faster_labor") if v(k) in ("Yea", "Nay")]
    if labor:
        yes = sum(1 for _, x in labor if x == "Yea")
        s = (2 if yes == len(labor) else -2 if yes == 0 and len(labor) == 2 else -1 if yes == 0 else 0)
        key = max(labor, key=lambda kv: HOUSE_VOTES[kv[0]][3])[0]
        out["eco-09"] = (s, house_vote(key, member, shown(key)) if len(labor) == 1 else
                         _src(f"U.S. House votes on {HOUSE_VOTES['workforce'][2]} and {HOUSE_VOTES['faster_labor'][2]}: "
                              f"{member} voted {shown('workforce')} and {shown('faster_labor')}",
                              f"https://clerk.house.gov/Votes/{HOUSE_VOTES[key][0]}{HOUSE_VOTES[key][1]:03d}", HOUSE_VOTES[key][3]))
    # War powers: every resolution answers whether Congress should authorize
    # prolonged hostilities; the Iran ones also whether to keep intervening there.
    all_wp = list(WAR_POWERS) + list(IRAN_WAR_POWERS)
    cast = [(k, v(k)) for k in all_wp if v(k) in ("Yea", "Nay")]
    if cast:
        out["def-04"] = (run_stance(cast), war_powers_source(all_wp, member, votes, cast))
    cast = [(k, v(k)) for k in IRAN_WAR_POWERS if v(k) in ("Yea", "Nay")]
    if cast:
        out["def-15"] = (run_stance(cast, sign=-1), war_powers_source(list(IRAN_WAR_POWERS), member, votes, cast))
    return [(q, s, src, None) for q, (s, src) in out.items()]


_REC = re.compile(r'<legislator name-id="([^"]*)"[^>]*?unaccented-name="([^"]*)"[^>]*?party="([^"]*)"[^>]*?state="([^"]*)"[^>]*>.*?</legislator>\s*<vote>([^<]*)</vote>', re.S)


def _load(year, roll):
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / f"{year}-{roll:03d}.xml"
    if not path.exists():
        url = f"https://clerk.house.gov/evs/{year}/roll{roll:03d}.xml"
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60) as r:
            path.write_bytes(r.read())
        time.sleep(1)
    xml = path.read_text(encoding="utf-8", errors="replace")
    out = []
    for name_id, uname, party, state, vote in _REC.findall(xml):
        last, _, first = uname.partition(",")
        last = re.sub(r"\s*\([A-Z]{2}\)\s*$", "", last).strip()
        out.append({"id": name_id, "last": norm(last), "first": norm(first) or None, "party": party, "state": state, "vote": vote.strip()})
    return out


class HouseRecord:
    """All the roll calls above, searchable by member."""

    def __init__(self):
        self.rolls = {k: _load(y, r) for k, (y, r, _, _) in HOUSE_VOTES.items()}

    def member_votes(self, state, name, party=None):
        """{vote key: vote} for the member from `state` named `name`, or None if
        no single member matches. Matched once by name, then followed by the
        Clerk's member id across every roll call."""
        tokens = norm(name).split()
        if not tokens:
            return None
        last, first = tokens[-1], tokens[0]
        ids = set()
        for members in self.rolls.values():
            for m in members:
                if m["state"] != state or m["last"].split()[-1:] != [last]:
                    continue
                if m["first"] and not first_names_match(first, m["first"].split()[0]):
                    continue
                ids.add(m["id"])
        if len(ids) > 1 and party:
            ids = {i for i in ids if any(m["id"] == i and m["party"] == party for ms in self.rolls.values() for m in ms)}
        if len(ids) > 1:
            # A sitting member and a predecessor with the same surname (Adelita and Raúl
            # Grijalva, whom the Clerk lists by surname alone): only the member is still
            # voting, so keep whoever appears in the latest roll call.
            latest = max(self.rolls, key=lambda k: HOUSE_VOTES[k][:2])
            current = {m["id"] for m in self.rolls[latest]} & ids
            if len(current) == 1:
                ids = current
        if len(ids) != 1:
            return None
        return self.votes_for(ids.pop())

    def votes_for(self, mid):
        """{vote key: vote} for the Clerk's member id `mid` (also used for former
        members, who are named by id because their seats belong to others now)."""
        votes = {}
        for k, members in self.rolls.items():
            for m in members:
                if m["id"] == mid and m["vote"] in ("Yea", "Nay", "Aye", "No"):
                    votes[k] = m["vote"]
        return votes or None
