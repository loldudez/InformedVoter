"""Researched positions for Minnesota's statewide races: U.S. Senate (Flanagan vs.
Tafoya) and governor (Klobuchar vs. Demuth). Writes data/research/MN.json.

Positions come from KAXE's candidate questionnaires (Tafoya answered for the
primary), the candidates' debates and campaign coverage. Researched
Oct. 25, 2026.

    py scripts/research/minnesota_2026.py
"""

from common import P, article, write

READ = "2026-10-25"
KAXE_GOV = article("KAXE 2026 election guide, candidate questionnaire", "https://www.kaxe.org/2026-09-28/governor-demuth-klobuchar-young-mn-2026-election-guide", "2026-09-28")
GOV_DEBATE = article("KAXE debate report, Oct. 20, 2026", "https://www.kaxe.org/elections/2026-10-20/here-are-4-takeaways-from-the-first-demuth-klobuchar-debate", "2026-10-20")
KAXE = article("KAXE 2026 election guide, candidate questionnaire", "https://www.kaxe.org/2026-09-25/senate-flanagan-tafoya-whiting-simonetti-mn-2026-election-guide", "2026-09-25")
DEBATE = article("KTTC debate report, Oct. 16, 2026", "https://www.kttc.com/2026/10/16/only-scheduled-debate-flanagan-tafoya-spar-over-track-records-policy-positions/", "2026-10-16")
MPR = article("MPR News, Aug. 12, 2026", "https://www.mprnews.org/story/2026/08/12/peggy-flanagan-primary-win-takes-aim-at-trump-outlines-senate-agenda", "2026-08-12")
REFORMER = article("Minnesota Reformer, Oct. 13, 2026", "https://www.newsfromthestates.com/article/michele-tafoya-shrugs-trump-endorsement-close-senate-race-minnesota", "2026-10-13")

senate = {
    "id": "MN-SEN",
    "candidates": [
        {"id": "MN-SEN:flanagan", "name": "Peggy Flanagan", "party": "D",
         "bio": "Lieutenant governor of Minnesota since 2019, a former state representative and a citizen of the White Earth Nation.",
         "positions": P(
             ("hea-01", 2, KAXE("Flanagan would fight for Medicare for All"), None),
             ("hea-04", -2, MPR("Flanagan supports Medicare for All"), "pay for healthcare and not just health insurance"),
             ("hea-03", 2, KAXE("Flanagan would reverse the Medicaid cuts"), None),
             ("hea-02", 1, KAXE("Flanagan would lower prescription drug costs and end prior authorization"), None),
             ("eco-03", 2, KAXE("Flanagan would raise the federal minimum wage"), None),
             ("soc-07", 2, KAXE("Flanagan would create universal child care"), None),
             ("hou-01", 1, KAXE("Flanagan would invest in affordable housing"), None),
             ("hou-02", 2, KAXE("Flanagan would ban Wall Street from buying up homes"), None),
             ("imm-02", 2, KAXE("Flanagan opposes mass deportation and supports a path to citizenship"), "a pathway to legal status and citizenship"),
             ("imm-08", -2, MPR("Flanagan calls for comprehensive reform of ICE and an end to indefinite detention"), "ICE as it currently exists is not it."),
             ("imm-01", 1, KAXE("Flanagan would secure the border while protecting due process"), None),
             ("ene-01", 2, KAXE("Flanagan supports 100% carbon-free electricity by 2040 and investment in wind, solar and green steel"), None),
             ("ene-06", 1, KAXE("Flanagan supports 100% carbon-free electricity by 2040"), None),
             ("ene-04", 1, KAXE("Flanagan would enforce environmental standards and hold polluters accountable"), None),
             ("agr-01", 1, KAXE("Flanagan would pass a comprehensive five-year Farm Bill"), None),
             ("agr-08", 1, KAXE("Flanagan would invest in regenerative agriculture research"), None),
             ("eco-10", -1, KAXE("Flanagan opposes the administration's tariffs and would shield farm markets from them"), None),
             ("gov-11", 2, KAXE("Flanagan would ban corporate PAC money and overturn Citizens United"), None),
             ("gov-13", -2, KAXE("Flanagan would ban corporate PAC money and overturn Citizens United"), None),
             ("gov-03", 2, KAXE("Flanagan would require donor disclosure and restore independent watchdogs"), None),
             ("def-15", -2, MPR("Flanagan on the Iran war"), "Donald Trump's illegal war in Iran"),
             ("def-12", -1, DEBATE("Flanagan would not send more offensive weapons or military aid to Israel's Netanyahu government"), "would not support additional offensive weapons or military aid to Israel"))},
        {"id": "MN-SEN:tafoya", "name": "Michele Tafoya", "party": "R",
         "bio": "Former NBC and ESPN sports broadcaster, running for office for the first time.",
         "positions": P(
             ("soc-03", 1, DEBATE("Tafoya supports abortion rights"), "I am a pro-choice Republican."),
             ("imm-01", 2, KAXE("Tafoya would secure the southern border and end catch-and-release"), None),
             ("imm-02", -1, KAXE("Tafoya on legal status for undocumented immigrants"), "I do not support amnesty."),
             ("imm-07", 1, KAXE("Tafoya backs the Laken Riley Act, which requires detaining immigrants charged with theft"), None),
             ("gov-05", 2, KAXE("Tafoya supports the SAVE America Act"), None),
             ("cri-01", 1, REFORMER("Tafoya's public safety plan calls for more support for local police and better coordination with federal agencies"), None),
             ("ene-03", 2, KAXE("Tafoya would unleash American energy production and cut federal regulations"), None),
             ("ene-01", -1, KAXE("Tafoya opposes the Inflation Reduction Act"), None),
             ("eco-07", 1, KAXE("Tafoya on spending"), "hold the line on spending"),
             ("eco-10", 0, DEBATE("Tafoya would renegotiate trade with Canada and Mexico and says she would have taken a different approach than the president"), "let's renegotiate this with Canada and with Mexico"),
             ("def-11", 1, DEBATE("Tafoya stands with Israel"), "calling it a genocide is an absolute misrepresentation"))},
    ],
}

governor = {
    "id": "MN-GOV",
    "candidates": [
        {"id": "MN-GOV:klobuchar", "name": "Amy Klobuchar", "party": "D",
         "bio": "U.S. senator from Minnesota since 2007 and a former Hennepin County attorney.",
         "positions": P(
             ("hea-02", 2, KAXE_GOV("Klobuchar would use state bulk purchasing and biosimilars to cut drug prices"), "taking on Big Pharma to lower prescription drug prices"),
             ("hea-07", 1, GOV_DEBATE("Klobuchar supports the state's reinsurance program and help for small businesses with premiums"), None),
             ("sta-09", 1, KAXE_GOV("Klobuchar would support rural hospitals"), None),
             ("soc-07", 1, KAXE_GOV("Klobuchar would expand access to affordable child care"), None),
             ("hou-01", 1, GOV_DEBATE("Klobuchar would build more housing, with incentives for 100,000 new units"), None),
             ("hou-09", 1, KAXE_GOV("Klobuchar would finish building high-speed broadband"), None),
             ("edu-03", 2, KAXE_GOV("Klobuchar would create 10,000 more apprenticeships"), None),
             ("sta-07", 2, KAXE_GOV("Klobuchar would create 10,000 more apprenticeships and tie degrees to in-demand careers"), None),
             ("sta-02", 1, KAXE_GOV("Klobuchar on school funding"), "funding our schools will always be a priority for me"),
             ("sta-10", 1, GOV_DEBATE("Klobuchar supports more R&D incentives for small businesses and startups and workforce training incentives"), None),
             ("eco-10", -1, GOV_DEBATE("Klobuchar would negotiate trade agreements with Canadian provinces to blunt the tariffs"), None))},
        {"id": "MN-GOV:demuth", "name": "Lisa Demuth", "party": "R",
         "bio": "Speaker of the Minnesota House since 2025 and a state representative since 2019.",
         "positions": P(
             ("eco-02", 2, KAXE_GOV("Demuth would cut the two lowest income tax brackets and end state taxes on Social Security benefits"), "cut income taxes for families by reducing the lowest two tax brackets"),
             ("eco-01", -1, GOV_DEBATE("Demuth rules out any tax increase"), "Tax hikes are absolutely off the table for me."),
             ("hea-03", -1, GOV_DEBATE("Demuth opposes putting more people on public health plans to cut costs"), "putting more people on a public plan does not help bring those costs down"),
             ("soc-12", -1, KAXE_GOV("Demuth would preserve girls' sports"), "preserve girls' sports"),
             ("gov-05", 2, KAXE_GOV("Demuth would pass voter ID"), "ensure we finally pass voter ID"),
             ("sta-04", 1, GOV_DEBATE("Demuth blames state mandates for rising property taxes and would create a commission to study them"), None))},
    ],
}

write("data/research/MN.json", [senate, governor], "Minnesota U.S. Senate and governor races, researched Oct. 25, 2026.", updated=READ)
