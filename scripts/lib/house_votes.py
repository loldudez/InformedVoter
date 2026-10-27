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
}


def _src(title, url, date):
    return {"title": title, "url": url, "date": date}


def house_vote(key, member, vote):
    year, roll, bill, date = HOUSE_VOTES[key]
    return _src(f"U.S. House roll call {roll} ({year}) on {bill}: {member} voted {vote}",
                f"https://clerk.house.gov/Votes/{year}{roll:03d}", date)


def vote_positions(member, votes):
    """Standard positions from a member's recorded votes: [(question, stance, source, quote)].
    votes: {key: 'Yea'|'Nay'|'Aye'|'No'} (missing = not in office or not voting)."""
    rows = []
    v = lambda k: {"Aye": "Yea", "No": "Nay"}.get(votes.get(k), votes.get(k))  # noqa: E731
    shown = lambda k: votes.get(k)  # noqa: E731  as the Clerk recorded it
    if v("rfma") in ("Yea", "Nay"):
        rows.append(("soc-10", 2 if v("rfma") == "Yea" else -1, house_vote("rfma", member, shown("rfma")), None))
    if v("whpa") in ("Yea", "Nay"):
        rows.append(("soc-03", 2 if v("whpa") == "Yea" else -1, house_vote("whpa", member, shown("whpa")), None))
    if v("ira") in ("Yea", "Nay"):
        s = 1 if v("ira") == "Yea" else -1
        rows.append(("hea-02", s, house_vote("ira", member, shown("ira")), None))
        rows.append(("hea-07", s, house_vote("ira", member, shown("ira")), None))
    if v("iija") in ("Yea", "Nay"):
        rows.append(("eco-06", 1 if v("iija") == "Yea" else -1, house_vote("iija", member, shown("iija")), None))
    if v("chips") in ("Yea", "Nay"):
        rows.append(("agr-02", 1 if v("chips") == "Yea" else -1, house_vote("chips", member, shown("chips")), None))
    if v("hr1_2025") == "Yea":
        rows.append(("hea-03", -1, house_vote("hr1_2025", member, shown("hr1_2025")), None))
    if v("ukraine") in ("Yea", "Nay"):
        rows.append(("def-13", 2 if v("ukraine") == "Yea" else -2, house_vote("ukraine", member, shown("ukraine")), None))
    if v("israel") in ("Yea", "Nay"):
        rows.append(("def-12", 2 if v("israel") == "Yea" else -2, house_vote("israel", member, shown("israel")), None))
    if v("border") == "Yea":
        rows.append(("imm-01", 1, house_vote("border", member, shown("border")), None))
    if v("energy") == "Yea":
        rows.append(("ene-03", 1, house_vote("energy", member, shown("energy")), None))
    return rows


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
        if len(ids) != 1:
            return None
        mid = ids.pop()
        votes = {}
        for k, members in self.rolls.items():
            for m in members:
                if m["id"] == mid and m["vote"] in ("Yea", "Nay", "Aye", "No"):
                    votes[k] = m["vote"]
        return votes or None
