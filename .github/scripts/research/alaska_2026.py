"""Researched positions for Alaska's statewide races: U.S. Senate (Sullivan vs.
Peltola) and governor (Kreiss-Tomkins, Wilson, Bronson, Taylor). Writes
data/research/AK.json.

Senate positions come from guides.vote's nonpartisan Alaska guide, which ties
each stance to a vote, bill or statement (read Oct. 25, 2026), plus Peltola's
recorded House votes from 2022 to 2024. Governor positions come from Alaska
Beacon, Alaska Public Media, Alaska's News Source and Anchorage Daily News
coverage of the campaign and debates. Researched Oct. 25, 2026.

    py scripts/research/alaska_2026.py
"""

from common import P, article, guide, vote_positions, write

READ = "2026-10-25"
S = guide("2026 Alaska U.S. Senate voters guide", "https://guides.vote/guide/2026-alaska-us-senate-voters-guide/", READ)
BEACON_ABORTION = article("Alaska Beacon, Sept. 22, 2026", "https://alaskabeacon.com/2026/09/22/where-do-alaskas-four-governor-candidates-stand-on-abortion-and-birth-control/", "2026-09-22")
BEACON_WAGE = article("Alaska Beacon, Oct. 9, 2026", "https://alaskabeacon.com/2026/10/09/two-alaska-governor-candidates-advocate-lower-minimum-wage-rollback-of-sick-leave-law/", "2026-10-09")
BEACON_CHILDCARE = article("Alaska Beacon, Oct. 12, 2026", "https://alaskabeacon.com/2026/10/12/alaska-candidates-for-governor-address-growing-gap-in-childcare/", "2026-10-12")
APM_DEBATE = article("Alaska Public Media debate report, Oct. 9, 2026", "https://alaskapublic.org/news/politics/alaska-legislature/2026-10-09/3-takeaways-from-alaskas-gubernatorial-debate-for-the-state", "2026-10-09")
KTUU_DEBATE = article("Alaska's News Source debate report, Oct. 8, 2026", "https://www.alaskasnewssource.com/2026/10/09/live-alaskas-gubernatorial-candidates-clash-debate-state/", "2026-10-08")

senate = {
    "id": "AK-SEN",
    "candidates": [
        {"id": "AK-SEN:peltola", "name": "Mary Peltola", "party": "D",
         "bio": "U.S. representative for Alaska's at-large district from 2022 to 2025 and the first Alaska Native elected to Congress.",
         "officialSite": "https://marypeltola.com/",
         "positions": P(
             *vote_positions("Peltola", {"rfma": "Yea", "ukraine": "Yea", "israel": "Yea", "border": "Nay", "energy": "Nay"}),
             ("soc-03", 2, S("Peltola supports Medicaid coverage of abortion and opposes a national ban (Alaska Beacon, 2024)"), "I will always protect the right to choose."),
             ("soc-04", -2, S("Peltola opposes a national abortion ban (Alaska Beacon, 2024); her campaign said a 2022 remark backing a 16-week limit was a mistake"), None),
             ("ene-01", 2, S("Peltola would fight to restore federal tax credits for solar, wind and hydropower projects"), None),
             ("ene-03", 1, S("Peltola supports oil and gas development alongside renewables (campaign energy plan)"), None),
             ("ene-06", 1, S("Peltola voted against repealing greenhouse gas reduction programs (H.R. 1023; House roll call 104, 2024)"), None),
             ("ene-04", 1, S("Peltola voted against overturning the rule extending Clean Water Act protection to more streams and wetlands (H.J.Res. 27; House roll call 187, 2023)"), None),
             ("cri-01", 1, S("Peltola calls for more funding for local law enforcement"), "more funding for local law enforcement"),
             ("eco-01", 2, S("Peltola would raise taxes on millionaires and billionaires to end federal income tax for people earning under $92,000"), None),
             ("eco-02", 2, S("Peltola would end federal income tax for people earning under $92,000, paid for by taxing millionaires and billionaires"), None),
             ("eco-12", 2, S("Peltola would shift income taxes from people earning under $92,000 to millionaires and billionaires"), None),
             ("hea-03", 2, S("Peltola would restore the Medicaid funding cut by the 2025 budget law"), "We can restore Medicaid and the [ACA] tax credits"),
             ("hea-07", 2, S("Peltola would restore the ACA premium tax credits"), None),
             ("hea-01", 1, S("Peltola on health coverage"), "Every Alaskan should be able to access and afford healthcare."),
             ("imm-02", 2, S("Peltola cosponsored the Dignity Act (H.R. 3599), pairing border security with a path to legal status, including for Dreamers"), None),
             ("imm-01", 1, S("Peltola voted for H.Res. 957 denouncing the Biden administration's border policies (2024) and cosponsored the Dignity Act's border security measures"), None),
             ("def-04", 2, S("Peltola says presidents should not act alone on major decisions (Alaska Beacon, May 2026)"), "There is a need for the War Powers Act."),
             ("def-15", -1, S("Peltola says the war in Iran is driving up gas and diesel prices"), None),
             ("eco-09", 2, S("Peltola cosponsored the PRO Act (H.R. 20, 2023) to protect organizing and collective bargaining"), None),
             ("soc-02", 2, S("Peltola supported the Equality Act's ban on discrimination by sexual orientation and gender identity"), None),
             ("soc-12", 1, S("Peltola voted against banning transgender students from girls' school sports (H.R. 734; House roll call 192, 2023), calling the ban bullying"), None),
             ("eco-03", 1, S("Peltola backs livable wages and tax incentives for companies that pay fair wages"), "The best wage is one that's livable."),
             ("gov-07", 1, S("Peltola supports ranked-choice voting"), None))},
        {"id": "AK-SEN:dan-s-sullivan", "name": "Dan S. Sullivan", "party": "R",
         "bio": "U.S. senator since 2015, a Marine Corps Reserve officer and a former Alaska attorney general.",
         "officialSite": "https://dansullivanforalaska.com/",
         "positions": P(
             ("soc-04", 2, S("Sullivan cosponsored S. 6, the Born-Alive Abortion Survivors Protection Act"), "I'm as pro-life as they come."),
             ("soc-03", -2, S("Sullivan supported overturning Roe v. Wade and returning abortion law to the states"), None),
             ("ene-01", -2, S("Sullivan voted against the 2022 clean energy investments (Senate roll call 325) and to end the clean energy tax credits (Senate roll call 372, 2025)"), None),
             ("ene-03", 2, S("Sullivan on energy"), "unleash Alaska's extraordinary resource potential"),
             ("ene-04", -2, S("Sullivan cosponsored S.J.Res. 31 to undo limits on seven hazardous air pollutants and voted to overturn the Clean Water Act streams and wetlands rule (Senate roll call 79, 2023)"), None),
             ("cri-04", 1, S("Sullivan introduced bills making assault on a public safety officer a federal crime (S. 1766) and ending the statute of limitations for fatal overdose crimes (S. 4209)"), None),
             ("eco-07", 1, S("Sullivan opposes reckless federal spending and voted to cancel public broadcasting funding (Senate roll call 411, 2025)"), None),
             ("hea-03", -1, S("Sullivan voted for the 2025 law that cut Medicaid (Senate roll call 372), after negotiating rural health funding in it"), None),
             ("hea-07", 0, S("Sullivan voted to extend ACA premium tax credits for three years (Senate roll call 644, 2025) but wants the subsidies tapered down rather than ended abruptly"), None),
             ("imm-01", 2, S("Sullivan cosponsored S. 2824 to build 900 miles of border wall and limit asylum"), None),
             ("imm-10", 2, S("Sullivan cosponsored S. 2824, which requires E-Verify for new hires"), None),
             ("imm-08", 2, S("Sullivan voted for $75 billion more for ICE (2025) and $70 billion more for DHS (2026), while saying ICE should revise its tactics"), None),
             ("def-04", -2, S("Sullivan voted five times in 2026 against requiring congressional authorization for military action in Iran"), None),
             ("def-15", 2, S("Sullivan on Iran (2025)"), "I fully support the President and his national security team"),
             ("soc-10", 1, S("Sullivan voted for the Respect for Marriage Act, citing its religious liberty protections (Senate roll call 362, 2022), after opposing the 2015 Supreme Court ruling"), None),
             ("soc-12", -1, S("Sullivan signed a 2022 letter opposing proposed federal protections for transgender athletes"), None),
             ("eco-03", -1, S("Sullivan voted against a $15 federal minimum wage (Senate roll call 74, 2021)"), None),
             ("eco-01", -2, S("Sullivan voted to extend the 2017 tax cuts (2025) and against raising taxes on corporations and the wealthy (Senate roll call 357, 2021)"), None),
             ("gov-05", 1, S("Sullivan supports the SAVE Act's proof-of-citizenship requirement for voter registration (Alaska Current, Feb. 2026)"), None),
             ("gov-06", -1, S("Sullivan voted against the 2021 voting access bill (S. 2093) and the John Lewis Voting Rights Act (S. 4)"), None))},
    ],
}

governor = {
    "id": "AK-GOV",
    "candidates": [
        {"id": "AK-GOV:kreiss-tomkins", "name": "Jonathan Kreiss-Tomkins", "party": "D",
         "bio": "Alaska state representative from Sitka from 2013 to 2023.",
         "positions": P(
             ("soc-03", 2, BEACON_ABORTION("Kreiss-Tomkins voted against abortion limits for 10 years in the Alaska House and would uphold the state Supreme Court's rulings"), "Medical privacy and reproductive freedom should be fundamental personal freedoms"),
             ("soc-04", -2, BEACON_ABORTION("Kreiss-Tomkins voted in 2014 against limiting abortion to cases of rape, incest or medical necessity"), None),
             ("sta-03", 1, BEACON_WAGE("Kreiss-Tomkins opposes lowering the voter-approved minimum wage, which rises to $15 in 2027"), None),
             ("eco-11", 1, BEACON_CHILDCARE("Kreiss-Tomkins would aim to expand paid family leave"), None),
             ("soc-07", 2, BEACON_CHILDCARE("Kreiss-Tomkins supports recurring state child care funding, child care workforce investment and a long-term goal of universal pre-K"), None),
             ("sta-02", 2, KTUU_DEBATE("Kreiss-Tomkins's first bill would fund K-12 schools a year in advance, and he would raise school funding"), None),
             ("edu-01", 1, APM_DEBATE("Kreiss-Tomkins would boost public school funding"), None),
             ("hou-04", 1, KTUU_DEBATE("Kreiss-Tomkins backs streamlined permitting for a statewide housing building boom"), None),
             ("ene-03", 1, KTUU_DEBATE("Kreiss-Tomkins supports an all-of-the-above energy approach, a gas line and royalty relief for Cook Inlet gas producers"), None),
             ("sta-11", 1, KTUU_DEBATE("Kreiss-Tomkins would make the oil company Hilcorp pay state corporate income tax, calling its exemption unfair"), None))},
        {"id": "AK-GOV:wilson", "name": "Bernadette Wilson", "party": "R",
         "bio": "Anchorage business owner and talk radio host.",
         "positions": P(
             ("soc-03", -2, BEACON_ABORTION("Wilson would appoint a pro-life advocate in her administration and have her attorney general narrow medically necessary abortion care"), None),
             ("soc-04", 2, BEACON_ABORTION("Wilson would keep fighting the state Supreme Court over abortion restrictions and run a state campaign on the risks of medication abortion"), None),
             ("sta-03", -2, BEACON_WAGE("Wilson supports repealing the voter-approved minimum wage increases and paid sick leave law"), None),
             ("ene-03", 1, KTUU_DEBATE("Wilson calls a gas line the biggest lever for lower energy costs"), "been a terrible business partner to our oil and gas industries"),
             ("edu-03", 1, KTUU_DEBATE("Wilson backs vocational training aligned with workforce needs"), None),
             ("sta-02", 0, APM_DEBATE("Wilson would not raise school funding without a clear plan to improve student performance"), None))},
        {"id": "AK-GOV:bronson", "name": "Dave Bronson", "party": "R",
         "bio": "Mayor of Anchorage from 2021 to 2024 and a cofounder of the anti-abortion group Alaska Family Action.",
         "positions": P(
             ("soc-03", -2, BEACON_ABORTION("Bronson would veto any state money for abortion"), "He vetoes any bit of money, any funding that goes towards abortion"),
             ("soc-04", 2, BEACON_ABORTION("Bronson would fight the state Supreme Court over abortion and replace merit selection of judges with elections"), None),
             ("sta-03", -2, BEACON_WAGE("Bronson would repeal the voter-approved minimum wage increase and paid sick leave"), "Mandatory sick leave, minimum wage — I would repeal them both"),
             ("soc-07", 1, BEACON_CHILDCARE("Bronson supports recurring state child care funding and calls child care essential infrastructure"), None),
             ("ene-03", 1, KTUU_DEBATE("Bronson blames federal regulation for stalled resource development and wants a second Cook Inlet drilling rig"), None))},
        {"id": "AK-GOV:taylor", "name": "Treg Taylor", "party": "R",
         "bio": "Former Alaska attorney general under Gov. Mike Dunleavy.",
         "positions": P(
             ("soc-03", -2, BEACON_ABORTION("As attorney general, Taylor sought to restrict the abortion pill mifepristone (2023) and defended limits on telehealth prescriptions"), None),
             ("soc-04", 1, BEACON_ABORTION("Taylor openly opposes abortion and worked to restrict it as attorney general"), None),
             ("cri-04", 1, APM_DEBATE("Taylor helped pass the law letting fentanyl dealers be charged with murder in overdose deaths"), None),
             ("sta-02", 1, KTUU_DEBATE("Taylor's first bill would fund K-12 schools a year in advance, with accountability restored to the Alaska Reads Act"), None),
             ("edu-03", 1, KTUU_DEBATE("Taylor backs vocational training aligned with workforce needs"), None),
             ("soc-07", 1, BEACON_CHILDCARE("Taylor would expand child care through federal funds, tax credits and fewer regulations rather than new state money, and opposes statewide pre-K"), None),
             ("ene-03", 1, KTUU_DEBATE("Taylor defended the Willow oil project and cites the jobs a gas line would bring"), None))},
    ],
}

write("data/research/AK.json", [senate, governor], "Alaska U.S. Senate and governor races, researched Oct. 25, 2026.", updated=READ)
