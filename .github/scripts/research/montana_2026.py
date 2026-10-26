"""Researched positions for Montana's U.S. Senate race (Alme, Bodnar, Bankhead).
Writes data/research/MT.json.

Positions come from the candidates' Oct. 11, 2026 debate in Bozeman (Daily
Montanan) and NBC Montana's issue-by-issue interviews. Researched Oct. 25, 2026.

    py scripts/research/montana_2026.py
"""

from common import P, article, write

READ = "2026-10-25"
DEBATE = article("Daily Montanan debate report, Oct. 12, 2026", "https://dailymontanan.com/?p=39449", "2026-10-12")
NBC = article("NBC Montana, Oct. 18, 2026", "https://nbcmontana.com/newsletter-daily/alme-bankhead-bodnar-austin-lay-out-policy-positions-in-race-for-senate", "2026-10-18")

senate = {
    "id": "MT-SEN",
    "candidates": [
        {"id": "MT-SEN:alme", "name": "Kurt Alme", "party": "R",
         "bio": "Former U.S. attorney for Montana, twice appointed by President Trump.",
         "positions": P(
             ("imm-01", 1, NBC("Alme wants the border secured"), "Now what we need to do is secure the border"),
             ("def-15", 1, NBC("Alme backs the president and military on Iran but would never support ground troops in endless wars"), "I will never support sending our sons and daughters boots on the ground"),
             ("eco-07", 1, NBC("Alme would cut federal spending to bring down inflation and building costs"), "we've got to rein in Washington spending"),
             ("hea-04", 1, DEBATE("Alme would make health care more transparent and competitive"), "making it more transparent, more competitive, and by putting patients first"),
             ("hea-07", -1, DEBATE("Alme says the ACA failed and mainly subsidized drug and insurance companies"), None),
             ("cri-04", 1, DEBATE("Alme pledges to lock up violent criminals"), None),
             ("agr-01", 1, NBC("Alme wants the farm bill passed"), None))},
        {"id": "MT-SEN:bodnar", "name": "Seth Bodnar", "party": "I",
         "bio": "Former president of the University of Montana and an Army veteran, running as an independent.",
         "positions": P(
             ("def-04", 2, NBC("Bodnar says Congress must decide whether to authorize military action in Iran"), None),
             ("imm-01", 1, NBC("Bodnar supports strong borders and enforcing immigration law, opposes the administration's tactics and backs comprehensive reform"), "We need strong borders and we need to enforce our immigration laws"),
             ("hou-04", 2, NBC("Bodnar backs zoning and building-code reform to unlock housing supply"), "incentivizing the type of zoning and code reform to unlock more supply"),
             ("hou-02", 1, NBC("Bodnar would limit private equity purchases of single-family homes"), None),
             ("eco-04", 2, NBC("Bodnar supports stronger antitrust enforcement against corporate monopolies in agriculture"), "Our farmers, our ranchers are getting squeezed by these big corporate monopolies"),
             ("eco-10", -1, NBC("Bodnar opposes the trade war with Canada"), None),
             ("hea-01", 1, DEBATE("Bodnar supports a universal coverage option that keeps choice and competition"), None),
             ("hea-07", 2, DEBATE("Bodnar would restore the expired ACA subsidies"), None),
             ("hea-03", 1, DEBATE("Bodnar would protect Montana's Medicaid expansion"), None),
             ("eco-01", 1, DEBATE("Bodnar would have higher earners pay more into Social Security"), None))},
        {"id": "MT-SEN:bankhead", "name": "Alani Bankhead", "party": "D",
         "bio": "Retired Air Force lieutenant colonel and counterintelligence agent.",
         "positions": P(
             ("hea-01", 2, DEBATE("Bankhead favors universal health care modeled on TRICARE, paid for by ending the Iran war"), None),
             ("eco-01", 2, DEBATE("Bankhead would remove the Social Security wage cap so all income is taxed"), "tax the wealthy, and it starts by ensuring that they pay"),
             ("def-15", -2, NBC("Bankhead opposes the Iran war"), "I do not support the war in Iran"),
             ("imm-02", 2, NBC("Bankhead supports comprehensive immigration reform and a faster path to citizenship"), None),
             ("hou-01", 1, NBC("Bankhead would give builders tax incentives for affordable homes"), "providing tax incentives to construction companies that create affordable housing"),
             ("eco-10", -1, NBC("Bankhead blames tariffs for the drop in Canadian tourism"), None))},
    ],
}

write("data/research/MT.json", [senate], "Montana U.S. Senate race, researched Oct. 25, 2026.", updated=READ)
