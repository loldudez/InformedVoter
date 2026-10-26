"""Researched positions for Maine's statewide races: U.S. Senate (Collins vs.
Jackson) and governor (Pingree, Charles, Bennett). Writes data/research/ME.json.

Senate positions come from guides.vote's nonpartisan Maine guide, which ties
each stance to a vote, bill or statement (read Oct. 25, 2026). Governor
positions come from Maine Public's candidate questionnaires (Charles did not
publish one), debate coverage and Charles's campaign site. Researched
Oct. 25, 2026.

    py scripts/research/maine_2026.py
"""

from common import P, article, guide, page, write

READ = "2026-10-25"
S = guide("2026 Maine U.S. Senate voters guide", "https://guides.vote/guide/2026-maine-us-senate-voters-guide/", READ)
MP_PINGREE = article("Maine Public candidate questionnaire, April 17, 2026", "https://www.mainepublic.org/politics/2026-04-17/your-vote-2026-profile-hannah-pingree-democrat-for-governor", "2026-04-17")
MP_BENNETT = article("Maine Public candidate questionnaire, Sept. 22, 2026", "https://www.mainepublic.org/politics/2026-09-22/your-vote-2026-profile-rick-bennett-independent-for-governor", "2026-09-22")
DEBATE = article("Maine Public debate report, Oct. 9, 2026", "https://www.wgbh.org/news/politics/2026-10-09/maines-2nd-gubernatorial-debate-is-over-heres-some-takeaways", "2026-10-09")
CHARLES_SITE = lambda note: page(f"Bobby Charles campaign site: {note}", "https://www.bobbyformaine.com/", READ)  # noqa: E731

senate = {
    "id": "ME-SEN",
    "candidates": [
        {"id": "ME-SEN:collins", "name": "Susan Collins", "party": "R",
         "bio": "U.S. senator since 1997 and chair of the Senate Appropriations Committee.",
         "positions": P(
             ("soc-03", 1, S("Collins introduced a bill with Sen. Murkowski to write the Roe v. Wade and Casey protections into law, but voted against the Women's Health Protection Act (Senate roll call 170, 2022), citing missing conscience protections"), None),
             ("soc-04", -1, S("Collins called the overturning of Roe v. Wade a radical jolt to the country"), "radical jolt to the country"),
             ("ene-01", 0, S("Collins voted to extend the residential clean energy credit but against keeping the wind and solar tax credits (Senate roll calls 365 and 364, 2025)"), None),
             ("ene-03", -1, S("Collins sponsored a ban on offshore drilling in the Gulf of Maine (S. 1472) and voted against opening the Arctic refuge's coastal plain to drilling (Senate roll call 632, 2025)"), None),
             ("ene-04", 0, S("Collins voted to keep mining limits near the Boundary Waters (Senate roll call 84, 2026) but to undo limits on seven hazardous air pollutants (Senate roll call 229, 2025)"), None),
             ("eco-06", 1, S("Collins voted for the infrastructure law (Senate roll call 314, 2021)"), None),
             ("edu-03", 1, S("Collins calls for expanded access to workforce training"), None),
             ("hea-07", 1, S("Collins voted to extend ACA premium subsidies (Maine Public, Dec. 2025)"), None),
             ("hea-03", 1, S("Collins voted against the 2025 tax and spending law over its Medicaid cuts (Senate roll call 372) and proposed taxing the ultrawealthy to help rural hospitals (S.Amdt. 2812)"), "harmful impact it will have on Medicaid"),
             ("eco-01", 0, S("Collins voted for the 2017 tax cuts and against their 2025 extension, and proposed a tax increase on the ultrawealthy to fund rural hospitals (S.Amdt. 2812)"), None),
             ("imm-08", 1, S("Collins voted for about $70 billion in new ICE and border funding twice in 2026, but also to move some ICE money to Medicaid (Senate roll call 18, 2026)"), None),
             ("def-04", 1, S("Collins voted in April 2026 to end the Iran hostilities at the War Powers Act's 60-day mark, after voting against a March limit (Senate roll call 46)"), "Further military action against Iran must have a clear mission."),
             ("def-15", 0, S("Collins first voted against limiting the Iran war, then voted to end the hostilities at the 60-day mark"), None),
             ("eco-09", 1, S("Collins sponsored the Protect America's Workforce Act (S. 2837) to restore union rights at federal agencies"), None),
             ("soc-10", 2, S("Collins introduced the Respect for Marriage Act (S. 4556, 2022)"), None),
             ("soc-12", -1, S("Collins voted for a federal ban on transgender athletes in girls' and women's sports (S. 9; Senate roll call 100, 2025)"), None),
             ("eco-03", 1, S("Collins introduced a bill to raise the federal minimum wage to $11 by 2028, indexed to inflation (S. 2785, 2023)"), None),
             ("gov-05", 1, S("Collins supports voter ID (Press Herald, Feb. 2026); she voted for proof of citizenship at registration, then later against it"), "an ID at the polls…will improve the security of our federal elections"))},
        {"id": "ME-SEN:jackson", "name": "Troy Jackson", "party": "D",
         "bio": "Former president of the Maine Senate (2018 to 2024) and a logger from Allagash.",
         "officialSite": "https://jacksonformaine.com/",
         "positions": P(
             ("soc-03", 2, S("Jackson would pass a federal right to abortion"), "Abortion is health care."),
             ("soc-04", -2, S("Jackson sponsored LD 1619 (2023), allowing abortion after 24 weeks when a doctor deems it necessary, and voted against a 2017 fetal-protection bill"), None),
             ("ene-06", 1, S("Jackson on climate"), "Climate change is a profound threat to our environment and economy."),
             ("ene-01", 1, S("Jackson voted to boost offshore wind energy in Maine and promoted wood-based energy"), None),
             ("ene-04", 2, S("Jackson sponsored a 2021 bill to ban synthetic herbicide spraying in forestry (SP 58) and pledges to protect air and water from chemicals like PFAS"), None),
             ("cri-08", 2, S("Jackson sponsored a bill creating a drug treatment court in Aroostook County"), None),
             ("hou-02", 1, S("Jackson's housing plan would stop Wall Street from buying up Maine"), None),
             ("hou-05", 2, S("Jackson would offer housing tax credits and down-payment help"), None),
             ("soc-07", 1, S("Jackson would invest in child care"), None),
             ("hea-01", 2, S("Jackson supports Medicare for All"), "Healthcare is a human right."),
             ("hea-03", 2, S("Jackson supports Medicare for All nationally and a public option in Maine (Maine Public, April 2026)"), None),
             ("hea-04", -2, S("Jackson supports Medicare for All"), "Healthcare is not, in my mind, a for-profit industry."),
             ("hea-02", 1, S("Jackson voted to cap prescription drug costs at a reference rate (SP 745)"), None),
             ("imm-08", -2, S("Jackson would abolish ICE and opposes its $70 billion funding increase"), None),
             ("imm-07", 1, S("Jackson says people here illegally or who commit crimes should be deported through a better process (Washington Post opinion, July 2026)"), None),
             ("def-15", -2, S("Jackson calls the Iran war foolish and illegal"), None),
             ("def-07", 2, S("Jackson would put diplomacy ahead of open-ended military action (Bangor Daily News, Aug. 2026)"), None),
             ("def-04", 1, S("Jackson would demand real congressional oversight of the Iran war"), None),
             ("eco-09", 2, S("Jackson voted to expand public-sector collective bargaining (2019) and against a right-to-work bill"), "give every worker the freedom to organize a union"),
             ("soc-02", 2, S("Jackson would pass comprehensive civil rights protections for LGBTQ+ people"), None),
             ("soc-10", 1, S("Jackson calls his 2009 vote against same-sex marriage his worst vote ever"), "my worst vote ever"),
             ("soc-12", 1, S("Jackson opposes banning transgender athletes from women's sports"), None),
             ("eco-03", 1, S("Jackson voted to raise Maine's minimum wage to $15 with cost-of-living increases (2023)"), None),
             ("eco-01", 2, S("Jackson on taxes"), "tax the billionaires and make sure greedy corporations pay their fair share"),
             ("eco-12", 2, S("Jackson voted to add an income tax bracket above $500,000 while expanding the lowest bracket"), "I don't believe in income tax cuts for wealthy people."),
             ("gov-06", 1, S("Jackson opposed 2025's Question 1, which would have cut absentee voting days and limited drop boxes"), None))},
    ],
}

governor = {
    "id": "ME-GOV",
    "candidates": [
        {"id": "ME-GOV:pingree", "name": "Hannah Pingree", "party": "D",
         "bio": "Speaker of the Maine House from 2008 to 2010, later director of Gov. Janet Mills's policy office and co-chair of the Maine Climate Council.",
         "positions": P(
             ("soc-03", 2, MP_PINGREE("Pingree supports the right to an abortion and says she defended reproductive rights as speaker"), None),
             ("soc-10", 2, MP_PINGREE("Pingree says she stood up for marriage equality as speaker in 2009"), None),
             ("soc-12", 1, MP_PINGREE("Pingree opposes banning transgender athletes from girls' and women's sports and weakening the Maine Human Rights Act"), None),
             ("gov-05", -2, MP_PINGREE("Pingree says photo ID should not be required to vote and would veto any bill that undermines voting rights"), None),
             ("edu-02", 1, MP_PINGREE("Pingree would make Maine's free community college permanent"), None),
             ("edu-03", 1, MP_PINGREE("Pingree would expand apprenticeships"), None),
             ("hou-01", 2, MP_PINGREE("Pingree would invest $100 million a year in building and preserving housing"), None),
             ("hou-02", 1, MP_PINGREE("Pingree would crack down on out-of-state corporations and private equity displacing Maine families from homes"), None),
             ("hou-04", 1, MP_PINGREE("Pingree would cut red tape and streamline housing permits"), None),
             ("hou-06", 1, MP_PINGREE("Pingree would work to reduce evictions"), None),
             ("sta-04", 2, MP_PINGREE("Pingree would raise the homestead exemption and widen the Property Tax Fairness Credit"), None),
             ("hea-01", 1, MP_PINGREE("Pingree says health care is a right"), None),
             ("hea-03", 1, MP_PINGREE("Pingree would create a state-backed public insurance option and streamline MaineCare enrollment"), None),
             ("hea-06", 1, MP_PINGREE("Pingree would add mental health to primary care, deploy mobile crisis teams and expand addiction recovery"), None),
             ("sta-09", 1, MP_PINGREE("Pingree would use the federal rural health grant to prevent rural closures and recruit providers"), None),
             ("ene-06", 2, MP_PINGREE("Pingree advanced Maine's first greenhouse gas targets and its entry into the regional carbon market (RGGI)"), None),
             ("ene-01", 1, MP_PINGREE("Pingree would expand affordable clean energy and clean energy jobs"), None),
             ("ene-04", 2, MP_PINGREE("Pingree passed the Kid-Safe Products Act on toxic chemicals and would hold corporate polluters accountable"), None),
             ("imm-03", 1, MP_PINGREE("Pingree agrees an immigrant workforce is essential to Maine's economy"), None),
             ("imm-08", -1, DEBATE("Pingree criticizes Charles for wanting an immigration detention center in Maine"), "open an Alligator Alcatraz to detain people here"),
             ("soc-01", 1, MP_PINGREE("Pingree supports free speech and press, including speech she considers biased"), None))},
        {"id": "ME-GOV:charles", "name": "Bobby Charles", "party": "R",
         "bio": "Former assistant U.S. secretary of state for counter-narcotics and a Navy veteran.",
         "positions": P(
             ("imm-08", 1, DEBATE("Charles blames Maine's new law limiting police cooperation with ICE and wants agencies to cooperate"), "State and local and federal law enforcement should always be talking to each other."),
             ("eco-10", -1, DEBATE("Charles disagrees with the tariffs on Canada"), None),
             ("ene-04", 1, DEBATE("Charles opposes rolling back power plant emission standards"), None),
             ("eco-02", 1, CHARLES_SITE("Charles would cut taxes on businesses and working families and suspend the gas tax"), None))},
        {"id": "ME-GOV:bennett", "name": "Rick Bennett", "party": "I",
         "bio": "Maine state senator from Oxford and Senate president from 2001 to 2002, running as an independent after leaving the Republican Party.",
         "positions": P(
             ("soc-03", 1, MP_BENNETT("Bennett supports the right to an abortion and includes reproductive care in the health care he calls a right"), None),
             ("soc-12", 1, MP_BENNETT("Bennett opposes banning transgender athletes from girls' and women's sports and weakening the Maine Human Rights Act"), None),
             ("gov-05", 1, MP_BENNETT("Bennett says photo ID should be required to vote"), None),
             ("edu-02", 1, MP_BENNETT("Bennett supports tuition-free community college"), None),
             ("edu-03", 1, MP_BENNETT("Bennett would expand workforce training and apprenticeships"), None),
             ("hou-05", 2, MP_BENNETT("Bennett would reduce down payments for first-time homebuyers and offer direct mortgage assistance"), None),
             ("hou-04", 1, MP_BENNETT("Bennett would clear permitting and infrastructure bottlenecks for new housing"), None),
             ("sta-04", 2, MP_BENNETT("Bennett would apply the Property Tax Fairness Credit directly to tax bills and expand relief for older Mainers"), None),
             ("hea-01", 2, MP_BENNETT("Bennett says health care is a right and would move Maine toward universal coverage"), None),
             ("hea-03", 1, DEBATE("Bennett would keep the Medicaid expansion voters approved in 2017"), None),
             ("hea-06", 1, MP_BENNETT("Bennett would strengthen behavioral health care"), None),
             ("ene-01", 1, MP_BENNETT("Bennett would expand heat pumps, storage and grid upgrades and create a Maine Generation Authority for in-state renewable power"), None),
             ("ene-06", 1, MP_BENNETT("Bennett says clean energy policy must cut emissions while lowering costs"), None),
             ("imm-08", -1, DEBATE("Bennett supports Maine's law limiting cooperation with ICE"), "ICE has not earned the benefit of the doubt."),
             ("imm-03", 1, MP_BENNETT("Bennett agrees an immigrant workforce is essential to Maine's economy"), None),
             ("soc-01", 1, MP_BENNETT("Bennett supports free speech and press, including speech he considers biased"), None))},
    ],
    "notes": [{"text": "Bobby Charles did not answer Maine Public's candidate questionnaire, so fewer of his positions are known.", "source": "Maine Public", "url": "https://www.mainepublic.org/politics/2026-09-22/your-vote-2026-profile-rick-bennett-independent-for-governor"}],
}

write("data/research/ME.json", [senate, governor], "Maine U.S. Senate and governor races, researched Oct. 25, 2026.", updated=READ)
