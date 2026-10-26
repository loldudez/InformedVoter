"""Researched positions for Georgia's statewide races: U.S. Senate (Ossoff vs.
Collins) and governor (Bottoms vs. Jackson). Writes data/research/GA.json.

Positions come from guides.vote's nonpartisan Georgia guides, which tie each
stance to a vote, bill or statement (read Oct. 25, 2026). Collins's recorded
House votes are added automatically by update_races.py. Researched Oct. 25, 2026.

    py scripts/research/georgia_2026.py
"""

from common import P, guide, write

READ = "2026-10-25"
S = guide("2026 Georgia U.S. Senate voters guide", "https://guides.vote/guide/2026-georgia-us-senate-voters-guide/", READ)
G = guide("2026 Georgia governor voters guide", "https://guides.vote/guide/2026-georgia-governor-voters-guide/", READ)

senate = {
    "id": "GA-SEN",
    "candidates": [
        {"id": "GA-SEN:ossoff", "name": "Jon Ossoff", "party": "D",
         "bio": "U.S. senator since 2021 and a former investigative documentary producer.",
         "positions": P(
             ("soc-03", 2, S("Ossoff sponsored S. 701 to prohibit government restrictions on abortion"), None),
             ("soc-04", -2, S("Ossoff says Georgia's six-week ban strips women of autonomy"), "strips women of autonomy"),
             ("ene-01", 2, S("Ossoff voted for $369 billion in clean energy investments (Senate roll call 325, 2022) and against ending the tax credits (2025)"), None),
             ("ene-06", 1, S("Ossoff on climate change"), "The U.S. must swiftly combat climate change."),
             ("cri-01", 1, S("Ossoff supports increasing law enforcement funding"), None),
             ("cri-02", 1, S("Ossoff supports funding police body cameras"), None),
             ("cri-09", -2, S("Ossoff sponsored S. 2299 to ban the federal death penalty"), None),
             ("eco-06", 1, S("Ossoff voted for the infrastructure law (Senate roll call 314, 2021)"), None),
             ("edu-01", 1, S("Ossoff sponsored $500 million for public school facility upgrades (S. 694, 2021)"), None),
             ("ene-04", 1, S("Ossoff voted against repealing EPA hazardous air pollutant limits (Senate roll call 229, 2025)"), None),
             ("hea-03", 1, S("Ossoff voted against the 2025 Medicaid cuts (Senate roll call 372)"), None),
             ("hea-07", 2, S("Ossoff sponsored S. 46 to extend ACA tax credits"), None),
             ("hea-01", 1, S("Ossoff on health coverage"), "No one should go without care for lack of money."),
             ("imm-07", 1, S("Ossoff voted for the Laken Riley Act, detaining immigrants charged with theft (Senate roll call 7, 2025)"), None),
             ("imm-08", -1, S("Ossoff voted against the $75 billion ICE increase and the $70 billion DHS increase"), None),
             ("imm-04", 1, S("Ossoff voted for the 2024 bill to speed asylum claims (Senate roll call 182, 2024)"), None),
             ("def-04", 2, S("Ossoff voted five times in 2026 to require congressional authorization for military action in Iran"), None),
             ("def-15", -2, S("Ossoff on Iran"), "I oppose yet another regime change war-of-choice in the Middle East."),
             ("eco-09", 2, S("Ossoff sponsored the PRO Act (S. 852)"), None),
             ("soc-02", 2, S("Ossoff sponsored S. 1503 to ban discrimination based on sexual orientation or gender identity"), None),
             ("soc-10", 2, S("Ossoff voted for the Respect for Marriage Act (Senate roll call 362, 2022)"), None),
             ("soc-12", 1, S("Ossoff voted against banning transgender students from girls' school sports (Senate roll call 100, 2025)"), None),
             ("eco-03", 2, S("Ossoff sponsored S. 53 (2021) to raise the federal minimum wage to $15"), None),
             ("eco-01", 2, S("Ossoff voted in 2021 to raise taxes on corporations and the wealthy (Senate roll call 357)"), None),
             ("gov-05", -1, S("Ossoff opposes the proof-of-citizenship voting bill (H.R. 22)"), None),
             ("gov-06", 1, S("Ossoff sponsored the Right to Vote Act and S. 2523 restoring voting-change preclearance"), None))},
        {"id": "GA-SEN:collins", "name": "Mike Collins", "party": "R",
         "bio": "U.S. representative for Georgia's 10th District since 2023 and a former trucking company owner.",
         "positions": P(
             ("soc-04", 2, S("Collins supports Georgia's six-week ban and sponsored H.R. 431, declaring life begins at conception"), "unapologetically pro-life"),
             ("soc-03", -2, S("Collins supported overturning Roe v. Wade"), None),
             ("ene-01", -1, S("Collins voted to end Biden-era clean energy tax credits (House roll call 190, 2025)"), None),
             ("ene-06", -2, S("Collins voted to repeal greenhouse gas reduction programs and to end the EPA methane charge"), None),
             ("cri-01", 2, S("Collins sponsored resolutions to invest in police hiring, training and equipment (H. Con. Res. 31, 98)"), "Being tough on crime stops crime."),
             ("cri-09", 1, S("Collins supports the death penalty for child sex crimes"), None),
             ("eco-07", 1, S("Collins says he would work to reduce government spending"), None),
             ("edu-06", 2, S("Collins supports expanding school choice"), "ensure that our children aren't trapped in failing public schools"),
             ("ene-04", -2, S("Collins introduced H.R. 8079 to strip EPA vehicle emission enforcement and voted to repeal hazardous air pollutant limits"), None),
             ("hea-07", -1, S("Collins voted against extending ACA premium subsidies for 3 years (House roll call 11, 2026)"), None),
             ("imm-07", 2, S("Collins introduced H.R. 7511 to detain immigrants charged with theft"), None),
             ("imm-08", 2, S("Collins voted for $75 billion more for ICE and $70 billion more for DHS"), "I fully support ICE."),
             ("def-15", 2, S("Collins on Iran"), "I fully support President Trump and what he is doing with Iran."),
             ("def-04", -2, S("Collins voted five times in 2026 against requiring congressional authorization for military action in Iran"), None),
             ("eco-09", -2, S("Collins sponsored H.R. 1232 to let workers at union shops opt out of dues"), None),
             ("soc-11", -2, S("Collins voted to make providing gender-affirming care to minors a crime (H.R. 3492)"), None),
             ("soc-12", -1, S("Collins sponsored H.R. 465 to ban LGBTQ flags at U.S. embassies"), None),
             ("eco-01", -2, S("Collins voted to extend the 2017 tax cuts and sponsored repeal of the estate tax (H.R. 1301)"), None),
             ("gov-05", 2, S("Collins voted to require voter ID (House roll call 69, 2026)"), None),
             ("gov-06", -2, S("Collins sponsored H.R. 7300 to ban universal vote-by-mail"), None),
             ("gov-07", -2, S("Collins sponsored H.R. 7300, which would ban ranked-choice voting"), None))},
    ],
}

governor = {
    "id": "GA-GOV",
    "candidates": [
        {"id": "GA-GOV:bottoms", "name": "Keisha Lance Bottoms", "party": "D",
         "bio": "Mayor of Atlanta from 2018 to 2022 and later a White House senior adviser.",
         "officialSite": "https://www.keishaforgovernor.com/",
         "positions": P(
             ("soc-03", 2, G("Bottoms would repeal Georgia's six-week abortion law"), "Roe standards where a woman could have the right to choose"),
             ("soc-04", -2, G("Bottoms would repeal Georgia's six-week abortion law"), None),
             ("ene-01", 2, G("Bottoms launched Clean Energy Atlanta, aiming for 100% clean energy by 2035"), None),
             ("cri-01", 1, G("Bottoms would increase state support for local law enforcement"), None),
             ("sta-08", 2, G("Bottoms would increase state support for local law enforcement"), None),
             ("edu-01", 2, G("Bottoms on schools"), "fully fund Georgia's schools"),
             ("sta-02", 2, G("Bottoms on schools"), "fully fund Georgia's schools"),
             ("edu-02", 1, G("Bottoms supports a path to free technical and community college"), None),
             ("edu-04", 2, G("Bottoms proposes eliminating state income tax for teachers and a $60,000 minimum teacher salary"), None),
             ("hea-03", 2, G("Bottoms on Medicaid"), "expand Medicaid to cut costs and close the coverage gap"),
             ("hea-02", 1, G("Bottoms would create an independent board to review drug prices (AARP)"), None),
             ("sta-09", 1, G("Bottoms calls reopening rural hospitals a priority"), None),
             ("imm-04", 2, G("Bottoms supports more immigration judges (Capital B News)"), None),
             ("imm-02", 1, G("Bottoms opposed ending DACA as mayor (2018)"), None),
             ("eco-09", 1, G("Bottoms on workers"), "Human rights and workers' rights go hand in hand."),
             ("soc-10", 2, G("Bottoms would protect marriage equality"), None),
             ("soc-12", 1, G("Bottoms opposes the state bill banning transgender students from women's sports"), None),
             ("gov-06", 2, G("Bottoms would create same-day voter registration"), "making it easier for Georgians to vote, not harder"))},
        {"id": "GA-GOV:jackson", "name": "Rick Jackson", "party": "R",
         "bio": "Founder of Jackson Healthcare, a medical staffing company.",
         "officialSite": "https://rickjackson.com/",
         "positions": P(
             ("soc-04", 2, G("Jackson would defend Georgia's heartbeat law"), None),
             ("soc-03", -2, G("Jackson on abortion"), "No one is more pro-life than me."),
             ("ene-03", 1, G("Jackson is the largest outside investor in a new Texas oil refinery"), "We're going to sell our oil."),
             ("cri-04", 1, G("Jackson on crime"), "keep violent criminals behind bars"),
             ("cri-01", 2, G("Jackson on police"), "fully support law enforcement with resources, training, and respect"),
             ("sta-08", 2, G("Jackson on police"), "fully support law enforcement with resources, training, and respect"),
             ("edu-06", 2, G("Jackson would opt Georgia into the federal private school scholarship tax credit"), None),
             ("imm-07", 2, G("Jackson on deportations"), "number one in the nation for deporting criminal illegal immigrants"),
             ("imm-08", 1, G("Jackson would work with ICE"), None),
             ("soc-12", -2, G("Jackson on gender"), "There are two genders, and they are God-given."),
             ("soc-11", -2, G("Jackson would imprison those who change a child's gender"), None),
             ("sta-04", 2, G("Jackson on property taxes"), "freeze property taxes immediately"),
             ("eco-02", 1, G("Jackson would cut the state income tax in half within four years"), None),
             ("gov-05", 2, G("Jackson on voter ID"), "You should have to show [an ID] to vote."))},
    ],
}

write("data/research/GA.json", [senate, governor], "Georgia U.S. Senate and governor races, researched Oct. 25, 2026.", updated=READ)
