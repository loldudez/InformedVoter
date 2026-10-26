"""Researched details for Louisiana's U.S. House districts 1 to 5 (the 6th is in
louisiana_2026.py). Writes data/research/LA-house.json, which update_races.py
merges onto the automatically refreshed races.

Candidates are the qualified lists reported by WWNO (Aug. 12, 2026). Positions
come from the WWNO/WRKF questionnaire (Oct. 19-20, 2026) for challengers who
answered it, and from recorded House votes for the four incumbents, none of whom
answered. Researched Oct. 24, 2026.

    py scripts/research/louisiana_house_2026.py
"""

from common import P, source, vote_positions, write

QUAL = source("WWNO: 39 candidates qualify to run for Louisiana’s 6 congressional districts", "https://www.wwno.org/2026-08-12/39-candidates-qualify-to-run-for-louisianas-6-congressional-districts", "2026-08-12")
G = {d: source(f"WWNO/WRKF election guide: {d} Congressional District candidates’ questionnaire answers",
               f"https://www.wwno.org/2026-10-{19 if d == '1st' else 20}/nov-3-election-guide-meet-the-{d}-congressional-district-candidates",
               "2026-10-19" if d == "1st" else "2026-10-20")
     for d in ("1st", "2nd", "3rd", "4th", "5th")}
HB648 = source("Louisiana Legislature: HB 648 (2023), “Prohibits certain procedures to alter the sex of a minor child”, authored by Rep. Gabe Firment; Act 466, passed over the governor’s veto",
               "https://legis.la.gov/legis/BillInfo.aspx?s=23RS&b=HB648", "2023-07-18")

FORMAT_NOTE = {"text": "Gov. Jeff Landry canceled this year’s closed party primaries for Congress, so every candidate shares the Nov. 3 ballot. A majority wins outright; otherwise the top two meet on Dec. 12.",
               "source": "WWNO", "url": QUAL["url"]}


def cand(rid, slug, name, party, bio, site=None, positions=None, **extra):
    c = {"id": f"{rid}:{slug}", "name": name, "party": party, "bio": bio, "positions": positions or {}}
    if site:
        c["officialSite"] = site
    c.update(extra)
    return c


def race(n, candidates, notes=()):
    rid = f"LA-H-{n:02d}"
    return {"id": rid, "candidatesOnly": True, "notes": [FORMAT_NOTE, *notes],
            "candidates": [c if c["id"].startswith(rid) else c for c in candidates]}


R1, R2, R3, R4, R5 = (f"LA-H-0{i}" for i in range(1, 6))

la1 = race(1, [
    cand(R1, "scalise", "Steve Scalise", "R",
         "U.S. Representative for the 1st District since 2008 and House Majority Leader since 2023; lives in Jefferson.",
         "https://www.stevescalise.com/", P(*vote_positions("Scalise", {
             "rfma": "Nay", "whpa": "Nay", "ira": "Nay", "iija": "Nay", "chips": "Nay", "hr1_2025": "Aye",
             "ukraine": "Yea", "israel": "Yea", "border": "Yea", "energy": "Yea"})), incumbent=True),
    cand(R1, "arrington", "Randall Arrington", "R",
         "Retired U.S. Navy aviator with a Ph.D. in political science from UCLA; lives in Ponchatoula.", None, P(
             ("ene-08", 2, G["1st"], None),
             ("hou-10", 2, G["1st"], None),
             ("imm-02", -2, G["1st"], None),
             ("imm-08", 1, G["1st"], None),
             ("ene-03", 2, G["1st"], None),
             ("gov-02", 2, G["1st"], None),
             ("gov-12", 2, G["1st"], None),
             ("gov-01", 2, G["1st"], None),
             ("def-10", 2, G["1st"], None))),
    cand(R1, "jewett", "Lauren Jewett", "D",
         "Special education teacher for 16 years; serves on the Louisiana Democratic Party’s executive committee; lives in Metairie.",
         "https://laurenjewett.com/", P(
             ("soc-03", 2, G["1st"], None),
             ("soc-04", -2, G["1st"], None),
             ("imm-02", 2, G["1st"], None),
             ("imm-08", -2, G["1st"], None),
             ("gov-02", 2, G["1st"], None),
             ("gov-12", 2, G["1st"], None),
             ("ene-08", 2, G["1st"], None),
             ("hou-10", 1, G["1st"], None),
             ("hea-01", 2, G["1st"], None),
             ("hea-03", 2, G["1st"], None),
             ("hea-10", 2, G["1st"], None),
             ("ene-04", 1, G["1st"], None),
             ("edu-01", 1, G["1st"], None))),
    cand(R1, "glass", "E. Liddy Glass", "I",
         "Independent from Metairie who says she believes in limited government, individual liberty and fiscal responsibility."),
])

la2 = race(2, [
    cand(R2, "carter", "Troy Carter", "D",
         "U.S. Representative for the 2nd District since 2021; former state Senate minority leader and New Orleans City Council member.",
         None, P(*vote_positions("Carter", {
             "rfma": "Yea", "whpa": "Yea", "ira": "Yea", "iija": "Yea", "chips": "Yea", "hr1_2025": "No",
             "ukraine": "Yea", "israel": "Yea", "border": "Nay", "energy": "Nay"})), incumbent=True),
    cand(R2, "ballay", "Lisa Ballay", "L",
         "Director of surgical physician practices at LCMC Health and a Louisiana State Museum board member; lives in New Orleans.", None, P(
             ("imm-07", 1, G["2nd"], None),
             ("ene-03", 1, G["2nd"], None),
             ("gov-02", 1, G["2nd"], None),
             ("gov-12", 1, G["2nd"], None))),
    cand(R2, "beach", "Walter “Rocky” Beach", "I",
         "Paramedic since 1991 and first-time candidate; lives in Gonzales.", None, P(
             ("ene-08", 1, G["2nd"], None),
             ("imm-08", 1, G["2nd"], None),
             ("gov-02", -1, G["2nd"], None))),
    cand(R2, "collins", "Renada “Honey” Collins", "I", "Candidate from New Orleans."),
    cand(R2, "williams", "Peter Williams", "R", "Agriculturist and tree farmer from Lettsworth."),
], notes=[{"text": "Wikipedia lists Renada Collins as a Democrat; the qualifying list reported by WWNO shows her with no party, which is used here.", "source": "WWNO", "url": QUAL["url"]}])

la3 = race(3, [
    cand(R3, "higgins", "Clay Higgins", "R",
         "U.S. Representative for the 3rd District since 2017; lives in Lafayette.",
         "https://captainhiggins.com/", P(*vote_positions("Higgins", {
             "rfma": "Nay", "whpa": "Nay", "ira": "Nay", "iija": "Nay", "chips": "Nay", "hr1_2025": "Aye",
             "ukraine": "Nay", "israel": "Yea", "border": "Yea", "energy": "Yea"})), incumbent=True),
    cand(R3, "day", "John Day", "D", "Has never held elected office; lives in Lake Charles.", "https://johndayforcongress.com/", P(
        ("soc-03", 2, G["3rd"], None),
        ("ene-08", 2, G["3rd"], "Absolutely essential"),
        ("imm-01", 1, G["3rd"], None),
        ("imm-02", 1, G["3rd"], None),
        ("ene-03", 1, G["3rd"], None),
        ("soc-08", 1, G["3rd"], None),
        ("gov-02", 2, G["3rd"], None),
        ("gov-12", 1, G["3rd"], None),
        ("gov-09", 2, G["3rd"], None))),
    cand(R3, "gonzalez", "Priscilla Gonzalez", "D",
         "Advocate for the PACT Act for veterans exposed to burn pits; ran against Higgins in 2024; lives in Lafayette.",
         "https://prisforcongress.com/", P(
             ("soc-03", 1, G["3rd"], None),
             ("ene-08", 2, G["3rd"], None),
             ("soc-08", 1, G["3rd"], None),
             ("imm-01", 1, G["3rd"], None),
             ("imm-07", 1, G["3rd"], None),
             ("imm-02", 1, G["3rd"], "firm, orderly, humane, and enforceable"),
             ("ene-03", 1, G["3rd"], None),
             ("ene-04", 1, G["3rd"], None),
             ("gov-02", 2, G["3rd"], None),
             ("gov-12", 1, G["3rd"], None),
             ("eco-03", 2, G["3rd"], None))),
    cand(R3, "walker", "Caleb Walker", "D",
         "Former U.S. Army sergeant first class who deployed to Afghanistan; served on Louisiana’s Task Force on Career Alignment; lives in Lafayette.",
         "https://calebforcongress.com/", P(
             ("soc-03", 1, G["3rd"], None),
             ("ene-08", 2, G["3rd"], "one of my top priorities"),
             ("imm-07", 1, G["3rd"], None),
             ("imm-09", 1, G["3rd"], None),
             ("soc-08", 1, G["3rd"], None),
             ("ene-03", 1, G["3rd"], None),
             ("gov-02", 2, G["3rd"], "a basic accountability issue"),
             ("gov-12", 2, G["3rd"], "have no place in public service"),
             ("def-03", 1, G["3rd"], None))),
    cand(R3, "cotten", "Kate Cotten", "R", "Candidate from Lake Charles."),
    cand(R3, "lebrun", "Tia LeBrun", "I", "Candidate from Sulphur.", "https://lebrun4la.com/"),
], notes=[{"text": "Wikipedia lists Tia LeBrun as a Democrat; the qualifying list reported by WWNO shows her with no party, which is used here.", "source": "WWNO", "url": QUAL["url"]}])

la4 = race(4, [
    cand(R4, "johnson", "Mike Johnson", "R",
         "U.S. Representative for the 4th District since 2017 and Speaker of the House since 2023; lives in Bossier City.",
         "https://mikejohnsonforlouisiana.com/", P(*vote_positions("Johnson", {
             "rfma": "Nay", "whpa": "Nay", "ira": "Nay", "iija": "Nay", "chips": "Nay", "hr1_2025": "Aye",
             "ukraine": "Yea", "israel": "Yea", "border": "Yea", "energy": "Yea"})), incumbent=True),
    cand(R4, "cable", "Conrad Cable", "D", "First-generation farmer from Farmerville.", "https://conrad4congress2026.com/", P(
        ("soc-03", 2, G["4th"], None),
        ("soc-04", -2, G["4th"], None),
        ("eco-11", 2, G["4th"], None),
        ("imm-08", -2, G["4th"], None),
        ("imm-04", 1, G["4th"], None),
        ("gov-02", 2, G["4th"], None),
        ("gov-09", 1, G["4th"], None),
        ("gov-12", 2, G["4th"], None),
        ("ene-08", 2, G["4th"], None),
        ("def-15", -2, G["4th"], None),
        ("eco-10", -2, G["4th"], "illegal tariffs"),
        ("hea-03", 1, G["4th"], None),
        ("ene-04", 1, G["4th"], None))),
    cand(R4, "heslop", "Gordon Heslop", "R", "Candidate from Natchitoches who also ran for Congress in Missouri this year.", "https://heslopforcongress.com/", P(
        ("soc-03", -1, G["4th"], None),
        ("ene-08", 1, G["4th"], None),
        ("ene-03", 1, G["4th"], None),
        ("gov-02", 2, G["4th"], None),
        ("gov-12", 1, G["4th"], None),
        ("eco-10", -2, G["4th"], None),
        ("eco-07", 1, G["4th"], None))),
    cand(R4, "gromlich", "Matt Gromlich", "D", "Candidate from Greenwood.", "https://mattgromlichforcongress.com/"),
    cand(R4, "nichols", "Mike Nichols", "R", "Retired biologist with more than 35 years in land management and water resources; lives in Pitkin.", "https://mikenicholsforcongress.com/"),
])

la5 = race(5, [
    cand(R5, "cordell", "Misti Cordell", "R", "Chair of the Louisiana Board of Regents; lives in West Monroe.", "https://cordellforcongress.com/", P(
        ("soc-04", 2, G["5th"], "defend the unborn"),
        ("soc-03", -2, G["5th"], "defend the unborn"),
        ("ene-08", 1, G["5th"], None),
        ("ene-03", 2, G["5th"], None),
        ("imm-08", 1, G["5th"], None),
        ("gov-02", 2, G["5th"], None),
        ("gov-01", 2, G["5th"], None),
        ("eco-07", 1, G["5th"], None),
        ("eco-02", 1, G["5th"], None),
        ("def-16", 1, G["5th"], None))),
    cand(R5, "echols", "Michael Echols", "R", "State representative since 2020 and Louisiana House majority leader since 2025; lives in Monroe.", "https://michaelechols.com/", P(
        ("soc-03", -2, G["5th"], "100% pro-life"),
        ("soc-04", 2, G["5th"], "100% pro-life"),
        ("imm-08", 2, G["5th"], "100% with President Trump on immigration enforcement"),
        ("imm-01", 2, G["5th"], None),
        ("imm-02", -2, G["5th"], None),
        ("ene-03", 2, G["5th"], "unleashing American energy dominance"),
        ("gov-02", 2, G["5th"], None),
        ("gov-12", 2, G["5th"], "Transparency and the public interest should always come first"))),
    cand(R5, "firment", "Gabe Firment", "R", "State representative since 2020 and chair of the Louisiana House Insurance Committee; lives in Pollock.", "https://firmentforcongress.com/", P(
        ("soc-04", 2, G["5th"], "unapologetically pro-life"),
        ("soc-03", -2, G["5th"], "unapologetically pro-life"),
        ("ene-03", 2, G["5th"], "all-of-the-above energy strategy"),
        ("imm-01", 2, G["5th"], None),
        ("imm-07", 2, G["5th"], None),
        ("imm-09", 2, G["5th"], None),
        ("gov-02", 2, G["5th"], "prohibiting members of Congress from actively trading individual stocks"),
        ("gov-12", 1, G["5th"], "Transparency should be the rule; confidentiality should be the limited exception"),
        ("eco-07", 1, G["5th"], None),
        ("soc-11", -2, HB648, None))),
    cand(R5, "magee", "Austin Magee", "R", "Owner of Pittman Industrial, a welding and mechanical company; lives in Franklinton.", "https://austinmageeforcongress.com/", P(
        ("soc-03", -1, G["5th"], "the unnecessary taking of unborn life is wrong"),
        ("ene-08", 1, G["5th"], None),
        ("imm-01", 1, G["5th"], None),
        ("imm-08", 1, G["5th"], "effective and safe deportations"),
        ("ene-03", 1, G["5th"], "an energy-independent America"),
        ("gov-02", 2, G["5th"], None),
        ("gov-12", 2, G["5th"], "no business keeping secrets from the public"),
        ("eco-07", 1, G["5th"], None),
        ("gov-09", 1, G["5th"], None))),
    cand(R5, "moore", "Pat Moore", "D", "State representative since 2019 and Ouachita Parish Police Jury member from 2007 to 2019; lives in Monroe.", "https://patmooreforcongress.com/", P(
        ("soc-03", -2, G["5th"], "life in the womb until birth"),
        ("ene-08", 2, G["5th"], "the coast belongs to all of us"),
        ("hou-10", 1, G["5th"], None),
        ("imm-01", 1, G["5th"], None),
        ("ene-03", 1, G["5th"], None),
        ("ene-04", 1, G["5th"], None),
        ("gov-02", 2, G["5th"], "Members of Congress shouldn’t own or trade individual stocks"),
        ("gov-12", 2, G["5th"], None),
        ("hea-03", 1, G["5th"], None),
        ("hou-05", 2, G["5th"], None))),
    cand(R5, "cathey", "Stewart Cathey Jr.", "R", "State senator since 2020; lives in Monroe.", "https://stewartcathey.com/"),
    cand(R5, "dantzler", "Omar Dantzler", "R", "Retired school bus driver from Hammond."),
    cand(R5, "mckay", "Dan McKay", "D", "Vietnam War veteran and attorney from Bunkie.", "https://mckayforcongress.com/"),
    cand(R5, "wilson", "Antonio Wilson", "D", "Candidate from Tallulah.", "https://wilsonforlouisiana.com/"),
])

write("data/research/LA-house.json", [la1, la2, la3, la4, la5],
      "Louisiana U.S. House districts 1-5, researched Oct. 24, 2026.")
