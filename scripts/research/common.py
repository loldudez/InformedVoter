"""Helpers shared by the research scripts: positions with their sources, and
recorded congressional votes as sources.

A position is (question id, stance, source, short quote or None). The stance
scale is the site's: 2 strongly supports ... -2 strongly opposes. A question with
no clear public position is left out, never inferred from party.
"""

import json
import sys
from pathlib import Path

TODAY = "2026-10-24"
ROOT = Path(__file__).resolve().parents[2]


def source(title, url, date, accessed=None):
    """A source. `accessed=True` marks a live page whose date is when it was read
    (the default treats TODAY that way, for the first research scripts)."""
    s = {"title": title, "url": url, "date": date}
    if accessed or (accessed is None and date == TODAY):
        s["accessed"] = True
    return s


def page(title, url, read_on):
    """A live page (campaign site, voter guide) read on `read_on`."""
    return source(title, url, read_on, accessed=True)


def guide(name, url, read_on):
    """Sources from a guides.vote voters guide, which ties each stance to a vote,
    bill or statement. Each call names that evidence: G("Turek voted for ...")."""
    return lambda note: page(f"guides.vote, {name}: {note}", url, read_on)


def article(outlet, url, date):
    """Sources from one news article or candidate questionnaire, dated when it was
    published. Each call names what it reports: A("Andrews would ...")."""
    return lambda note: source(f"{outlet}: {note}", url, date, accessed=False)


def P(*rows):
    out = {}
    for qid, stance, src, quote in rows:
        assert qid not in out, qid
        assert stance in (-2, -1, 0, 1, 2), (qid, stance)
        s = dict(src)
        if quote:
            assert len(quote.split()) <= 25, quote
            s["quote"] = quote
        out[qid] = {"stance": stance, "source": s}
    return out


def combine(auto_rows, *rows):
    """Hand-researched rows plus automatic vote rows, the hand-researched ones
    winning where both answer the same question."""
    taken = {r[0] for r in rows}
    return [*rows, *(r for r in auto_rows if r[0] not in taken)]


# Recorded House votes: the definitions and the vote-to-question rules live with
# the automatic pipeline, so hand-researched and automatic members match exactly.
sys.path.insert(0, str(ROOT / "scripts" / "lib"))
from house_votes import HOUSE_VOTES, house_vote, vote_positions  # noqa: E402,F401

# Senate key votes as Ballotpedia lists them on each senator's page (senate.gov
# refuses scripted reads; Ballotpedia cites its roll calls). The rules follow the
# House votes: full strength for single-issue bills, half for broader packages,
# and "no" votes that could mean many things are not used.
SENATE_VOTES = {
    "rfma": "the Respect for Marriage Act (H.R. 8404, 2022)",
    "whpa": "the Women's Health Protection Act (H.R. 3755, 2022), to protect abortion access in federal law",
    "ira": "the Inflation Reduction Act (H.R. 5376, 2022), which let Medicare negotiate drug prices and extended ACA premium subsidies",
    "iija": "the Infrastructure Investment and Jobs Act (H.R. 3684, 2021)",
    "chips": "the CHIPS and Science Act (H.R. 4346, 2022), funding domestic semiconductor manufacturing",
    "obbba": "H.R. 1 (2025), the tax and spending law that cut federal Medicaid spending",
    "supp2024": "H.R. 815 (2024), military aid for Ukraine, Israel and Taiwan",
    "laken": "the Laken Riley Act (S. 5, 2025), requiring detention of immigrants charged with theft or violent crimes",
    "ftv": "the Freedom to Vote: John R. Lewis Act (2022), expanding voting access",
    "border2024": "the Border Act of 2024 (S. 4361), the bipartisan border security bill",
    "esg": "H.J.Res. 30 (2023), overturning a rule letting retirement plans weigh climate risk",
    "pact": "the PACT Act (2022), expanding health care for veterans exposed to toxic burn pits",
}
SENATE_RULES = {  # key: {vote: [(question, stance)]}
    "rfma": {"Yea": [("soc-10", 2)], "Nay": [("soc-10", -1)]},
    "whpa": {"Yea": [("soc-03", 2)], "Nay": [("soc-03", -1)]},
    "ira": {"Yea": [("hea-02", 1), ("hea-07", 1)], "Nay": [("hea-02", -1), ("hea-07", -1)]},
    "iija": {"Yea": [("eco-06", 1)], "Nay": [("eco-06", -1)]},
    "chips": {"Yea": [("agr-02", 1)], "Nay": [("agr-02", -1)]},
    "obbba": {"Yea": [("hea-03", -1)]},
    "supp2024": {"Yea": [("def-13", 1), ("def-12", 1)]},
    "laken": {"Yea": [("imm-07", 1)], "Nay": [("imm-07", -1)]},
    "ftv": {"Yea": [("gov-06", 1)], "Nay": [("gov-06", -1)]},
    "border2024": {"Yea": [("imm-01", 1)]},
    "esg": {"Yea": [("ene-06", -1)]},
    "pact": {"Yea": [("def-03", 1)], "Nay": [("def-03", -1)]},
}


def senate_vote_positions(member, url, votes, read_on):
    """Positions from a senator's key votes on Ballotpedia: [(question, stance,
    source, quote)]. votes: {key: 'Yea'|'Nay'} as Ballotpedia shows them."""
    rows = []
    for key, vote in votes.items():
        for qid, stance in SENATE_RULES[key].get(vote, []):
            rows.append((qid, stance, page(f"Ballotpedia key votes, U.S. Senate vote on {SENATE_VOTES[key]}: {member} voted {vote}", url, read_on), None))
    return rows


def write(path, races, note, updated=TODAY):
    out = {"updated": updated, "note": note, "races": races}
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    n = sum(len(c.get("positions", {})) for r in races for c in r.get("candidates", []))
    print(f"wrote {path}: {len(races)} races, {sum(len(r.get('candidates', [])) for r in races)} candidates, {n} sourced positions")
