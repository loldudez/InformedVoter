"""Researched positions for Virginia's U.S. Senate race (Warner vs. Mizusawa).
Writes data/research/VA.json.

Warner's positions come from his key Senate votes as Ballotpedia lists them;
Mizusawa's from his Ballotpedia candidate survey and campaign website, quoted
there (read Oct. 25, 2026). Researched Oct. 25, 2026.

    py scripts/research/virginia_2026.py
"""

from common import P, page, senate_vote_positions, write

READ = "2026-10-25"
MIZUSAWA = lambda note: page(f"Bert Mizusawa's campaign website, as quoted by Ballotpedia: {note}", "https://ballotpedia.org/Bert_Mizusawa", READ)  # noqa: E731

senate = {
    "id": "VA-SEN",
    "candidates": [
        {"id": "VA-SEN:warner", "name": "Mark Warner", "party": "D",
         "bio": "U.S. senator from Virginia since 2009 and governor of Virginia from 2002 to 2006.",
         "positions": P(*senate_vote_positions("Warner", "https://ballotpedia.org/Mark_Warner", {
             "rfma": "Yea", "whpa": "Yea", "ira": "Yea", "iija": "Yea", "chips": "Yea", "obbba": "Nay",
             "supp2024": "Yea", "laken": "Yea", "ftv": "Yea", "border2024": "Yea", "esg": "Nay", "pact": "Yea"}, READ))},
        {"id": "VA-SEN:mizusawa", "name": "Bert Mizusawa", "party": "R",
         "bio": "Retired Army major general, combat veteran and former senior adviser at the CIA.",
         "positions": P(
             ("eco-07", 1, MIZUSAWA("Mizusawa would rein in federal spending"), "I will focus government on its core functions and bring excessive spending under control."),
             ("eco-02", 1, MIZUSAWA("Mizusawa supports a simpler tax code with fewer brackets and larger standard deductions"), None),
             ("imm-01", 1, MIZUSAWA("Mizusawa would keep the borders secure"), None),
             ("imm-03", 1, MIZUSAWA("Mizusawa would make legal immigration easier"), None),
             ("ene-02", 2, MIZUSAWA("Mizusawa supports bringing new nuclear power online"), "Nuclear power is clean, cheap, reliable and safe."))},
    ],
}

write("data/research/VA.json", [senate], "Virginia U.S. Senate race, researched Oct. 25, 2026.", updated=READ)
