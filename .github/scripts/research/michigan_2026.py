"""Researched positions for Michigan's statewide races: U.S. Senate (El-Sayed vs.
Rogers) and governor (Benson vs. James). Writes data/research/MI.json.

Positions come from guides.vote's nonpartisan Michigan guides, which tie each
stance to a vote, bill or statement (read Oct. 25, 2026). James's recorded House
votes are added automatically by update_races.py. Researched Oct. 25, 2026.

    py scripts/research/michigan_2026.py
"""

from common import P, guide, write

READ = "2026-10-25"
S = guide("2026 Michigan U.S. Senate voters guide", "https://guides.vote/guide/2026-michigan-us-senate-voters-guide/", READ)
G = guide("2026 Michigan governor voters guide", "https://guides.vote/guide/2026-michigan-governor-voters-guide/", READ)

senate = {
    "id": "MI-SEN",
    "candidates": [
        {"id": "MI-SEN:el-sayed", "name": "Abdul El-Sayed", "party": "D",
         "bio": "Physician and epidemiologist who ran Detroit's health department and ran for governor in 2018.",
         "officialSite": "https://abdulforsenate.com/",
         "positions": P(
             ("soc-03", 2, S("El-Sayed would write Roe-era abortion rights into federal law and backs the Women's Health Protection Act (S. 2150)"), None),
             ("soc-04", -2, S("El-Sayed would sponsor the Women's Health Protection Act, which limits state abortion restrictions"), None),
             ("ene-01", 2, S("El-Sayed on energy"), "fight for a pathway to 100% renewable energy"),
             ("ene-06", 2, S("El-Sayed backs U.S. engagement in the Paris climate agreement"), "The climate crisis is not a future threat. It's here."),
             ("ene-03", -1, S("El-Sayed opposes U.S. dependence on oil and gas and would shut down the Line 5 pipeline"), None),
             ("ene-04", 2, S("El-Sayed would shut down Line 5 to protect the Great Lakes"), "fight to hold corporate polluters fully accountable"),
             ("cri-01", 0, S("El-Sayed now backs funding for police recruitment, retention and retirement; in 2020 and 2021 he called for reducing police budgets (CNN, July 2026)"), None),
             ("cri-06", 2, S("El-Sayed opposes cash bail"), None),
             ("cri-07", 1, S("El-Sayed supports investing in community violence-prevention programs"), None),
             ("cri-10", 1, S("El-Sayed supports the George Floyd Justice in Policing Act"), None),
             ("eco-04", 2, S("El-Sayed would enforce antitrust law and break up corporate monopolies"), None),
             ("hou-01", 2, S("El-Sayed would invest heavily in new housing construction"), "invest in building new housing"),
             ("hou-04", 1, S("El-Sayed would streamline local housing regulations"), None),
             ("edu-06", -2, S("El-Sayed opposes vouchers and in 2018 proposed outlawing for-profit charter schools"), "public money into private pockets"),
             ("edu-04", 2, S("El-Sayed would raise the minimum teacher salary to at least $60,000 a year"), None),
             ("hea-01", 2, S("El-Sayed would pass Medicare for All and abolish medical debt"), None),
             ("hea-03", 2, S("El-Sayed would pass Medicare for All and immediately repeal the 2025 Medicaid cuts"), None),
             ("hea-04", -2, S("El-Sayed supports Medicare for All and breaking up big health care companies"), None),
             ("hea-07", 2, S("El-Sayed would immediately repeal the 2025 cuts to Medicaid and ACA subsidies"), None),
             ("imm-02", 2, S("El-Sayed supports the DREAM Act (S. 3348)"), "I believe in a safe and secure border and a clear pathway to citizenship."),
             ("imm-06", 1, S("El-Sayed on refugees"), "We must fully fund asylum and refugee programs."),
             ("imm-08", -2, S("El-Sayed would abolish ICE and restructure immigration enforcement"), None),
             ("def-15", -2, S("El-Sayed calls the Iran war illegal and unjustifiable and wants an immediate end to hostilities"), None),
             ("def-07", 2, S("El-Sayed opposes a nuclear-armed Iran but seeks diplomatic means to prevent one"), None),
             ("eco-09", 2, S("El-Sayed would pass the PRO Act (S. 852) and says right-to-work laws should be illegal"), "every worker deserves the right to join a union"),
             ("soc-02", 1, S("El-Sayed would guarantee civil rights in health care for LGBTQ people"), "I stand with the LGBTQ+ community in their struggle for equal rights and dignity."),
             ("soc-12", 1, S("El-Sayed opposed ending the 988 crisis line's service for LGBTQ+ youth (2025)"), None),
             ("eco-03", 1, S("El-Sayed says wages must rise; in 2018 he proposed a $15 state minimum wage"), "We need to stand up to increase wages."),
             ("eco-01", 2, S("El-Sayed would raise the top rate on income over $1 million and tax wealth over $1 billion"), "It is high past time for us to tax billionaires their wealth."),
             ("eco-12", 2, S("El-Sayed would raise the marginal tax rate on income over $1 million"), None),
             ("gov-05", -2, S("El-Sayed opposes voter ID and the SAVE Act's proof-of-citizenship requirement"), None),
             ("gov-06", 2, S("El-Sayed supports no-reason absentee and early in-person voting and an Election Day holiday"), "I believe in making voting easier."))},
        {"id": "MI-SEN:rogers", "name": "Mike Rogers", "party": "R",
         "bio": "U.S. representative from 2001 to 2015, former chair of the House Intelligence Committee and a former FBI agent; the 2024 Republican Senate nominee.",
         "officialSite": "https://rogersforsenate.com/",
         "positions": P(
             ("soc-03", -1, S("Rogers supported overturning Roe v. Wade"), "I'm a pro-life guy, I've voted pro-life."),
             ("soc-04", 0, S("Rogers opposes a national abortion ban and says states should decide"), "I will 100% respect Michiganders' decision on the abortion issue."),
             ("ene-01", -1, S("Rogers says renewable energy mandates are expensive"), "costing us all pretty dearly"),
             ("cri-01", 1, S("Rogers would give law enforcement the resources they need"), "back the blue all the way"),
             ("eco-07", 1, S("Rogers on federal spending"), "We can stop the spending in Washington that drove up prices."),
             ("hou-04", 1, S("Rogers blames excessive regulation for high housing prices and would give home builders tax credits"), None),
             ("edu-06", 2, S("Rogers wants Michigan to opt into the federal private school scholarship tax credit and voted for D.C. vouchers (House roll call 204, 2011)"), "We have to have choice for our kids."),
             ("ene-04", 0, S("Rogers backs a Great Lakes drilling ban and removing Line 5 from under Lake Michigan, but voted in 2014 to limit EPA Clean Water Act enforcement (House roll call 489)"), None),
             ("hea-04", 1, S("Rogers would create a health plan based on the free market"), "embrace the freedom of the free market"),
             ("hea-03", -1, S("Rogers says federally funded insurance plans don't work very well and voted against the Affordable Care Act (2010) and to repeal it (2013), though he opposed cutting health care to pay for defense (2026)"), None),
             ("imm-01", 2, S("Rogers would finish the border wall and reinstate the Remain in Mexico policy"), None),
             ("imm-07", 2, S("Rogers favors tracking down criminals over mass deportations"), None),
             ("def-15", 2, S("Rogers would let the president continue the Iran war"), "Iran is an imminent threat to our country"),
             ("eco-09", 0, S("Rogers backed the 2023 UAW strike but voted to limit prevailing wages (2014) and NLRB action (2013)"), None),
             ("soc-02", 1, S("Rogers says people should not be evicted or fired for being LGBTQ"), None),
             ("soc-12", -1, S("Rogers opposes transgender athletes in women's sports"), None),
             ("eco-03", -1, S("Rogers voted against raising the federal minimum wage to $7.25 (House roll call 18, 2007)"), None),
             ("eco-01", -2, S("Rogers supports the 2025 tax cut law"), "There's no tax cut I don't like."),
             ("gov-05", 2, S("Rogers supports voter ID and the SAVE Act"), "easier to vote and harder to cheat"),
             ("gov-06", -1, S("Rogers worries that more ways to vote, such as mail ballots, make votes harder to verify"), None))},
    ],
}

governor = {
    "id": "MI-GOV",
    "candidates": [
        {"id": "MI-GOV:benson", "name": "Jocelyn Benson", "party": "D",
         "bio": "Michigan secretary of state since 2019.",
         "officialSite": "https://www.jocelynbenson.com/",
         "positions": P(
             ("soc-03", 2, G("Benson supported Proposal 3, which put reproductive freedom in the Michigan Constitution"), "fight to make sure women can make their own decisions"),
             ("soc-04", -2, G("Benson says overturning Roe v. Wade led to draconian bans"), None),
             ("ene-01", 2, G("Benson supported moving Michigan to 100% clean electricity by 2040 and the federal clean energy tax credits"), None),
             ("ene-06", 1, G("Benson on climate solutions"), "both an imperative and an economic opportunity"),
             ("ene-04", 2, G("Benson would raise penalties for corporations that pollute Michigan's water, land and air and set enforceable Great Lakes guardrails"), None),
             ("hea-01", 1, G("Benson on health care"), "should be a right, not a privilege"),
             ("hea-03", 1, G("Benson would push to restore the federal health care cuts"), None),
             ("hea-09", 1, G("Benson would expand low- or no-cost preventive care"), None),
             ("eco-09", 2, G("Benson supports protecting collective bargaining and unemployment benefits during strikes"), "I'll always defend your right to organize."),
             ("soc-02", 2, G("Benson supported adding sexual orientation and gender identity to Michigan's civil rights law"), None),
             ("soc-10", 1, G("Benson opposed the effort to overturn the Supreme Court's same-sex marriage ruling"), None),
             ("soc-12", 1, G("Benson made it easier for transgender people to change the sex marker on state IDs (2019)"), None),
             ("hou-05", 2, G("Benson proposes down-payment tax credits for first-time homebuyers"), None),
             ("gov-06", 1, G("Benson supports a state Voting Rights Act"), "fight for your freedom to vote"),
             ("gov-05", -1, G("Benson opposed state and federal proof-of-citizenship requirements for voter registration"), "would be taking a chainsaw to our election system"))},
        {"id": "MI-GOV:james", "name": "John James", "party": "R",
         "bio": "U.S. representative for Michigan's 10th District since 2023, an Army veteran and businessman.",
         "officialSite": "https://johnjamesmi.com/",
         "positions": P(
             ("soc-03", -1, G("James on abortion (2018); in 2024 he said Michigan voters had already decided the issue with Proposal 3"), "I am 100% pro-life."),
             ("soc-04", 1, G("James voted for H.R. 21 (2025), penalizing providers who don't care for infants surviving an attempted abortion; he has shifted on rape and incest exceptions"), None),
             ("ene-01", -1, G("James called Michigan's 100% clean electricity law insane and voted to end the clean energy tax credits (2025)"), None),
             ("ene-06", -1, G("James supports cutting emissions"), "through innovation rather than mandates"),
             ("ene-04", -1, G("James introduced a resolution to overturn the EPA's stricter vehicle emission rules (H.J.Res. 136) and voted to narrow the Clean Water Act, though he won funding for Lake St. Clair's sewer system"), None),
             ("cri-01", 1, G("James would ensure every officer has training, equipment, legal protections and respect"), None),
             ("sta-08", 1, G("James would ensure every officer has training, equipment, legal protections and respect"), None),
             ("cri-04", 1, G("James would keep violent criminals in prison"), "lock up violent criminals"),
             ("edu-06", 2, G("James would opt Michigan into the federal private school scholarship tax credit on his first day"), None),
             ("hea-04", 1, G("James calls for market-based health care reforms"), "The path to fixing healthcare is not more government, it's less."),
             ("hea-07", -1, G("James voted against extending ACA premium subsidies for three years (House roll call 11, 2026)"), None),
             ("imm-01", 2, G("James voted for the 2023 border wall bill (H.R. 2)"), "we need to lock our borders to protect us from drugs and terrorists"),
             ("imm-08", 2, G("James voted for $75 billion more for ICE and $70 billion more for DHS"), None),
             ("imm-10", 1, G("James voted for H.R. 2 (2023), which requires E-Verify for new hires"), None),
             ("eco-09", -1, G("James supports right-to-work laws and voted against restoring federal workers' bargaining rights, though he has backed UAW workers and joined a nurses' picket line"), None),
             ("soc-11", -2, G("James voted to make providing gender-affirming care to minors a federal crime (H.R. 3492)"), None),
             ("soc-12", -1, G("James voted to bar transgender students from girls' and women's sports (H.R. 28, 2025)"), None),
             ("soc-02", 1, G("James said in 2018 that employers shouldn't be able to fire someone for being gay"), None),
             ("eco-02", 1, G("James would eliminate the state income tax"), None),
             ("gov-05", 2, G("James supports a constitutional amendment requiring voter ID at the polls and proof of citizenship to register"), None))},
    ],
}

write("data/research/MI.json", [senate, governor], "Michigan U.S. Senate and governor races, researched Oct. 25, 2026.", updated=READ)
