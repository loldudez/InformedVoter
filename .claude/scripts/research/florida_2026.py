"""Researched positions for Florida's statewide races: governor (Donalds vs. Jolly)
and U.S. Senate (Moody vs. Nixon). Writes data/research/FL.json.

Governor positions come from guides.vote's nonpartisan Florida guide, which ties
each stance to a vote, bill or statement (read Oct. 25, 2026); Donalds's recorded
House votes are added automatically by update_races.py. Senate positions come
from campaign coverage and OnTheIssues' record of Moody's statements and actions,
each naming the outlet it cites. Researched Oct. 25, 2026.

    py scripts/research/florida_2026.py
"""

from common import P, article, guide, page, write

READ = "2026-10-25"
G = guide("2026 Florida governor voters guide", "https://guides.vote/guide/2026-florida-governor-voters-guide/", READ)
PHOENIX = article("Florida Phoenix, Sept. 9, 2026", "https://floridaphoenix.com/2026/09/09/angie-nixon-says-there-are-10-million-reasons-to-oppose-ashley-moody/", "2026-09-09")
FOX13 = article("FOX 13 interview, July 8, 2026", "https://www.fox13news.com/news/one-on-one-senate-candidate-angie-nixon-outlines-positions-housing-healthcare-foreign-policy", "2026-07-08")
OTI = lambda note: page(f"OnTheIssues, 2026 Florida Senate race: {note}", "https://ontheissues.org/2026_FL_Senate.htm", READ)  # noqa: E731

governor = {
    "id": "FL-GOV",
    "candidates": [
        {"id": "FL-GOV:donalds", "name": "Byron Donalds", "party": "R",
         "bio": "U.S. representative for Florida's 19th District since 2021 and a former state representative.",
         "officialSite": "https://byrondonalds.com/",
         "positions": P(
             ("soc-03", -2, G("Donalds stands with the pro-life movement, opposes writing Roe v. Wade into law and voted against the Women's Health Protection Act (H.R. 3755, 2021)"), None),
             ("soc-04", 1, G("Donalds says states should regulate abortion"), "Regulating abortion is the job of the states."),
             ("ene-01", -2, G("Donalds voted against the 2022 clean energy investments, to repeal them in 2023 and to end the tax credits in 2025"), None),
             ("ene-06", -2, G("Donalds sponsored H.R. 4300 to bar presidents from declaring a climate emergency and said heat waves aren't tied to climate change"), None),
             ("ene-04", -1, G("Donalds voted to ease environmental rules for chip plants (S. 2228) and to end mining limits near the Boundary Waters (2026), though he backs fighting algal blooms"), None),
             ("edu-06", 2, G("Donalds voted for the federal private school scholarship tax credit (2025) and says education dollars should follow students"), "School choice is the civil rights issue of our time."),
             ("hea-07", -1, G("Donalds voted against extending ACA premium subsidies for three years (House roll call 11, 2026) and opposes the ACA"), None),
             ("hou-04", 1, G("Donalds would cut construction permit costs"), "On housing, we are going to slash red tape."),
             ("imm-01", 2, G("Donalds voted for the 2023 border wall bill (H.R. 2) and introduced a bill to study a biometric entry-exit system"), None),
             ("imm-08", 2, G("Donalds voted for $75 billion more for ICE and $70 billion more for DHS and opposes sanctuary policies"), None),
             ("imm-10", 1, G("Donalds voted for H.R. 2 (2023), which requires E-Verify for new hires"), None),
             ("eco-09", -2, G("Donalds voted against the PRO Act (2021) and the 2026 first-contract bill (H.R. 5408) and supports right-to-work laws"), None),
             ("soc-11", -2, G("Donalds voted to make providing gender-affirming care to minors a federal crime (H.R. 3492)"), None),
             ("soc-12", -2, G("Donalds voted to bar transgender students from girls' sports (H.R. 734, 2023)"), "Men SHOULD NOT be competing in women's sports PERIOD."),
             ("soc-05", -2, G("Donalds opposed 2024's Amendment 3 and would oppose future legalization measures"), "I do not support recreational marijuana."),
             ("eco-02", 2, G("Donalds would cut taxes on tips, overtime and Social Security"), None),
             ("eco-01", -2, G("Donalds opposes raising taxes and voted to extend the 2017 tax cuts (2025)"), None),
             ("sta-04", 2, G("Donalds supports 2026's Amendment 3, phasing out property taxes on many owner-occupied homes"), None),
             ("gov-05", 2, G("Donalds supports voter ID and sponsored H.R. 7300, requiring proof of citizenship to register"), None),
             ("gov-06", -2, G("Donalds sponsored H.R. 7300, which bans universal vote-by-mail"), None))},
        {"id": "FL-GOV:jolly", "name": "David Jolly", "party": "D",
         "bio": "Republican U.S. representative for Florida's 13th District from 2014 to 2017, now running as a Democrat.",
         "officialSite": "https://davidjolly.com/",
         "positions": P(
             ("soc-03", 2, G("Jolly would replace Florida's six-week ban with a law allowing abortion until fetal viability"), None),
             ("soc-04", -2, G("Jolly would repeal Florida's six-week abortion ban"), None),
             ("ene-01", 2, G("Jolly would expand clean and renewable energy and build it into public utilities"), None),
             ("ene-06", 1, G("Jolly on climate"), "faces some of the most direct climate impacts in the country"),
             ("ene-04", 2, G("Jolly calls for a data center moratorium until Florida has real protections for water and air"), None),
             ("ene-03", -1, G("Jolly opposes offshore drilling"), None),
             ("sta-05", 1, G("Jolly supports Everglades restoration and septic-to-sewer conversions to protect springs"), None),
             ("cri-05", 1, G("Jolly supports a state version of the federal FIRST STEP Act to reduce recidivism"), None),
             ("edu-06", 0, G("Jolly would keep Florida's voucher program but reform it"), "We should keep choice, but improve the standards of our choice schools."),
             ("hea-03", 2, G("Jolly supports expanding Medicaid"), None),
             ("hea-07", 1, G("Jolly supports extending the ACA premium tax credits"), None),
             ("sta-09", 2, G("Jolly proposes a pilot program to expand community health centers with a 9-to-1 federal match"), "5-year pilot to dramatically expand community health centers"),
             ("hou-05", 1, G("Jolly supports down-payment assistance"), None),
             ("imm-02", 2, G("Jolly supports a path to legal status for long-term residents, parents of U.S. citizens and DACA recipients"), None),
             ("imm-08", -1, G("Jolly would not require state or local police to work with ICE"), None),
             ("imm-10", -1, G("Jolly opposes mandating E-Verify"), None),
             ("eco-09", 1, G("Jolly would stand with public servants on fair wages and benefits"), "proud to have the support of the Florida AFL-CIO."),
             ("soc-10", 1, G("Jolly would protect marriage equality at the state level"), None),
             ("soc-12", 0, G("Jolly calls attacks on LGBTQ+ people shameful but doesn't think biological males should play competitive women's sports"), None),
             ("soc-05", 1, G("Jolly voted against 2024's Amendment 3 but would enact any amendment that won a majority, including recreational marijuana"), None),
             ("gov-10", 2, G("Jolly supports home rule and easier citizen ballot initiatives"), "Direct democracy should be easier, not a gauntlet."))},
    ],
}

senate = {
    "id": "FL-SEN",
    "candidates": [
        {"id": "FL-SEN:moody", "name": "Ashley Moody", "party": "R",
         "bio": "U.S. senator since January 2025, appointed to succeed Marco Rubio, and Florida attorney general from 2019 to 2025.",
         "positions": P(
             ("soc-04", 2, OTI("Moody cosponsored the Born-Alive Abortion Survivors Protection Act and a bill raising penalties for medical professionals who mishandle abortions (Florida Politics, Oct. 2025)"), None),
             ("soc-03", -2, OTI("As attorney general, Moody fought to keep the abortion-rights amendment off Florida's ballot"), None),
             ("edu-06", 2, OTI("Moody has long backed school choice (FOX 13, Aug. 2025)"), None),
             ("eco-01", -1, OTI("Moody hailed the 2025 tax and spending law's tax cuts (Florida Phoenix, July 2025)"), None),
             ("hea-07", -1, PHOENIX("Moody was among the Republicans in Congress who let the enhanced ACA subsidies expire"), None),
             ("soc-05", -1, OTI("As attorney general, Moody opposed the 2024 recreational marijuana ballot measure"), None),
             ("cri-04", 1, OTI("Moody supports enhanced penalties under the Thin Blue Line Act (2025)"), None),
             ("ene-06", -1, OTI("As attorney general, Moody sued the federal government over carbon dioxide limits"), None),
             ("imm-08", 1, OTI("Moody supports the administration's immigration enforcement policies (2025)"), None),
             ("def-11", 1, OTI("Moody says Florida stands with its ally Israel"), None),
             ("eco-07", 1, OTI("Moody says government wastes hundreds of millions a year and backed the Billion Dollar Boondoggle Act (2025)"), None))},
        {"id": "FL-SEN:nixon", "name": "Angie Nixon", "party": "D",
         "bio": "Florida state representative from Jacksonville since 2020.",
         "positions": P(
             ("hea-01", 2, PHOENIX("Nixon supports Medicare for All"), "Universal healthcare would save over a trillion dollars if we were to pass it"),
             ("hea-04", -2, FOX13("Nixon supports a step-by-step path to Medicare for All"), None),
             ("hea-07", 2, FOX13("Nixon would start by extending the ACA subsidies"), None),
             ("hea-03", 2, PHOENIX("Nixon criticized the 2025 Medicaid cuts"), None),
             ("eco-03", 2, PHOENIX("Nixon calls for raising the federal minimum wage from $7.25 an hour"), None),
             ("imm-02", 2, FOX13("Nixon supports a path to citizenship for mixed-status families and many TPS recipients"), None),
             ("imm-08", -1, PHOENIX("Nixon criticizes the administration's mass deportation program"), None),
             ("imm-05", 1, FOX13("Nixon would focus enforcement on companies that hire and exploit undocumented workers"), None),
             ("hou-02", 2, FOX13("Nixon would stop private equity firms from buying single-family homes"), None),
             ("hou-06", 1, FOX13("Nixon supports federal rent stabilization with a 10% cap in some areas"), None),
             ("hou-05", 1, FOX13("Nixon would add funding for down payment assistance"), None),
             ("eco-10", -2, FOX13("Nixon wants the administration's tariffs repealed"), None),
             ("eco-01", 1, FOX13("Nixon wants billionaires and corporations to pay their fair share"), None),
             ("def-01", -1, FOX13("Nixon would reassess Pentagon spending after its failed audits"), None),
             ("def-07", 2, FOX13("Nixon says the U.S. should try every diplomatic option before using force"), "exhaust all diplomatic alternatives and efforts"),
             ("def-15", -1, PHOENIX("Nixon criticized the cost of the Iran war"), None),
             ("gov-11", 1, FOX13("Nixon wants big money out of politics"), None),
             ("eco-09", 1, OTI("Nixon says government must not weaken unions' work (Florida Times-Union, May 2023)"), None))},
    ],
}

write("data/research/FL.json", [governor, senate], "Florida governor and U.S. Senate races, researched Oct. 25, 2026.", updated=READ)
