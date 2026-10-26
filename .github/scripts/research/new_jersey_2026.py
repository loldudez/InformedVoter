"""Researched positions for New Jersey's U.S. Senate race (Booker vs. Murphy).
Writes data/research/NJ.json.

Booker's positions come from his key Senate votes as Ballotpedia lists them;
Murphy's from his campaign website, quoted on Ballotpedia (read Oct. 25, 2026).
Researched Oct. 25, 2026.

    py scripts/research/new_jersey_2026.py
"""

from common import P, page, senate_vote_positions, write

READ = "2026-10-25"
MURPHY = lambda note: page(f"Justin Murphy's campaign website, as quoted by Ballotpedia: {note}", "https://ballotpedia.org/Justin_Murphy", READ)  # noqa: E731

senate = {
    "id": "NJ-SEN",
    "candidates": [
        {"id": "NJ-SEN:booker", "name": "Cory Booker", "party": "D",
         "bio": "U.S. senator from New Jersey since 2013 and a former mayor of Newark.",
         "positions": P(*senate_vote_positions("Booker", "https://ballotpedia.org/Cory_Booker", {
             "rfma": "Yea", "whpa": "Yea", "ira": "Yea", "iija": "Yea", "chips": "Yea", "obbba": "Nay",
             "supp2024": "Yea", "laken": "Nay", "ftv": "Yea", "border2024": "Nay", "esg": "Nay", "pact": "Yea"}, READ))},
        {"id": "NJ-SEN:murphy", "name": "Justin Murphy", "party": "R",
         "positions": P(
             ("soc-03", -2, MURPHY("Murphy is pro-life, with exceptions for the mother's life, rape and incest"), "I believe life begins at conception"),
             ("soc-04", 1, MURPHY("Murphy supports parental notification and opposes tax dollars for abortion"), None),
             ("eco-12", -2, MURPHY("Murphy would replace the income tax code with a 10% to 12% flat tax"), None),
             ("eco-01", -2, MURPHY("Murphy would abolish the capital gains and estate taxes"), None),
             ("eco-07", 2, MURPHY("Murphy would make DOGE permanent and supports a balanced budget amendment"), None),
             ("edu-06", 2, MURPHY("Murphy supports school choice and would split the Education Department's budget among local schools and voucher programs"), None),
             ("edu-07", 1, MURPHY("Murphy says parents control their children's education and would abolish the federal Education Department"), None),
             ("def-01", 1, MURPHY("Murphy wants a military able to fight and win two wars at once"), None),
             ("imm-01", 2, MURPHY("Murphy would finish the southern border wall, secure the northern border and station troops at the border"), None),
             ("imm-08", 1, MURPHY("Murphy would withhold federal aid from sanctuary cities and supports local police enforcing immigration law"), None),
             ("imm-07", 1, MURPHY("Murphy would deport immigrants who commit crimes"), None),
             ("hea-01", 1, MURPHY("Murphy agrees with the goal of universal coverage but through health savings accounts and competition"), None),
             ("hea-04", 2, MURPHY("Murphy wants every American to own a health savings account and to buy insurance across state lines"), "I adamantly oppose government-run healthcare"),
             ("ene-03", 2, MURPHY("Murphy would develop domestic energy, including shale oil, where it can be done responsibly"), None),
             ("ene-02", 2, MURPHY("Murphy on nuclear power"), "I strongly support the expansion of nuclear power"))},
    ],
}

write("data/research/NJ.json", [senate], "New Jersey U.S. Senate race, researched Oct. 25, 2026.", updated=READ)
