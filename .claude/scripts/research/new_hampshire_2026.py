"""Researched positions for New Hampshire's statewide races: U.S. Senate (Pappas vs.
Sununu) and governor (Ayotte vs. Warmington). Writes data/research/NH.json.

Senate positions come from guides.vote's nonpartisan New Hampshire guide, which
ties each stance to a vote, bill or statement (read Oct. 25, 2026); Pappas's
recorded House votes are added automatically by update_races.py. Governor
positions come from bills Gov. Ayotte signed or vetoed, campaign coverage and
Warmington's campaign site. Researched Oct. 25, 2026.

    py scripts/research/new_hampshire_2026.py
"""

from common import P, article, guide, page, write

READ = "2026-10-25"
S = guide("2026 New Hampshire U.S. Senate voters guide", "https://guides.vote/guide/2026-new-hampshire-us-senate-voters-guide/", READ)
NHPR_VETOES = article("NHPR and New Hampshire Bulletin, July 3, 2026", "https://www.nhpr.org/politics/2026-07-03/ayotte-vetoes-nine-bills-including-book-ban-push-and-toll-increases-for-out-of-state-visitors", "2026-07-03")
VNEWS_EFA = article("Valley News, June 11, 2025", "https://vnews.com/2025/06/11/governor-kelly-ayotte-signs-universal-education-freedom-accounts-bill-into-law-sb295-61699853/", "2025-06-11")
BULLETIN_ID = article("New Hampshire Bulletin, April 6, 2026", "https://newhampshirebulletin.com/2026/04/06/ayotte-signs-bill-barring-use-of-student-ids-to-vote/", "2026-04-06")
WCAX = article("WCAX, Oct. 7, 2026", "https://www.wcax.com/2026/10/07/campaign-countdown-candidates-nh-governor/", "2026-10-07")
NHPR_ICE = article("NHPR, May 23, 2025", "https://www.nhpr.org/nh-news/2025-05-23/nh-new-law-requiring-local-cooperation-federal-immigration-enforcement", "2025-05-23")
NHPR_YOUTH = article("NHPR via WBUR, Aug. 4, 2025", "https://www.wbur.org/news/2025/08/04/new-hampshire-trans-youth-health-care-puberty-blockers", "2025-08-04")
MONITOR = article("Concord Monitor, June 12, 2026", "https://www.concordmonitor.com/2026/06/12/new-hampshire-democrats-governor-cinde-warmington/", "2026-06-12")
WARMINGTON_SITE = lambda note: page(f"Cinde Warmington campaign site: {note}", "https://www.cindewarmington.com/", READ)  # noqa: E731

senate = {
    "id": "NH-SEN",
    "candidates": [
        {"id": "NH-SEN:pappas", "name": "Chris Pappas", "party": "D",
         "bio": "U.S. representative for New Hampshire's 1st District since 2019.",
         "officialSite": "https://chrispappas.org/",
         "positions": P(
             ("soc-04", -2, S("Pappas cosponsored the Women's Health Protection Act (H.R. 3755, 2021), barring government restrictions on abortion access"), None),
             ("ene-01", 2, S("Pappas voted for the 2022 clean energy investments (House roll call 420)"), "invest in lower-cost, clean energy solutions"),
             ("ene-06", 1, S("Pappas calls for innovative solutions to the climate crisis"), None),
             ("cri-01", 2, S("Pappas cosponsored H.R. 3184 to fund training and recruitment for small and midsize police departments"), None),
             ("cri-02", 1, S("Pappas voted for the 2021 George Floyd Justice in Policing Act, which required body cameras (House roll call 60)"), None),
             ("cri-10", 1, S("Pappas voted for the 2021 George Floyd Justice in Policing Act, which banned racial profiling and limited qualified immunity"), None),
             ("hea-06", 1, S("Pappas introduced a bill funding substance use treatment and prevention (H.R. 9759)"), None),
             ("soc-08", 1, S("Pappas introduced a bill banning companies from using surveillance pricing to raise food prices"), None),
             ("edu-01", 1, S("Pappas on public schools"), "I'll keep fighting for strong public schools."),
             ("edu-06", -1, S("Pappas says he has stood firm against efforts to dismantle public education"), None),
             ("ene-04", 2, S("Pappas introduced a bill to hold polluters accountable for PFAS contamination (H.R. 6668) and voted to keep mining limits near the Boundary Waters (2026)"), "hold polluters accountable"),
             ("hea-03", 1, S("Pappas opposes cuts to Medicaid and Medicare"), None),
             ("hea-07", 2, S("Pappas would make the ACA premium tax credits permanent"), None),
             ("imm-07", 1, S("Pappas supports more enforcement against people who cross the border illegally and commit serious crimes"), None),
             ("imm-02", 2, S("Pappas cosponsored the American Dream and Promise Act (H.R. 6, 2021) for Dreamers"), None),
             ("imm-08", -2, S("Pappas introduced a bill moving ICE's $75 billion slush fund to local police (H.R. 7163)"), None),
             ("def-04", 2, S("Pappas voted five times in 2026 to require congressional authorization for military action in Iran"), None),
             ("def-15", -2, S("Pappas on the Iran war"), "a war of choice, with no plan for how to win it"),
             ("def-07", 1, S("Pappas pressed the administration to prioritize diplomacy with Iran"), None),
             ("eco-09", 2, S("Pappas cosponsored the PRO Act (H.R. 842, 2021) and H.R. 2550 restoring federal workers' bargaining rights"), None),
             ("soc-02", 2, S("Pappas sponsored the Equality Act (H.R. 15)"), None),
             ("soc-12", 2, S("Pappas voted against barring transgender students from girls' sports (House roll call 12, 2025) and cosponsored restoring the LGBTQ+ youth crisis line (H.R. 5434)"), None),
             ("eco-03", 2, S("Pappas voted to raise the federal minimum wage to $15 by 2025 (House roll call 496, 2019)"), None),
             ("eco-01", 1, S("Pappas voted against extending the 2017 tax cuts (2025), saying they favored the wealthiest and the biggest corporations"), "gave tax giveaways to the wealthiest"),
             ("gov-05", -1, S("Pappas voted three times against proof-of-citizenship registration requirements and opposes New Hampshire's ban on student IDs for voting"), None))},
        {"id": "NH-SEN:sununu", "name": "John E. Sununu", "party": "R",
         "bio": "U.S. senator for New Hampshire from 2003 to 2009 and U.S. representative from 1997 to 2003.",
         "officialSite": "https://www.sununusenator.com/",
         "positions": P(
             ("soc-03", -1, S("Sununu says abortion is a state issue and would not undermine New Hampshire's law, which allows abortion up to 24 weeks"), "I'm pro-life."),
             ("soc-04", 0, S("Sununu would not override New Hampshire's abortion law federally; in 2006 he voted to make taking a minor across state lines for an abortion a federal crime"), None),
             ("ene-03", 1, S("Sununu supports increasing domestic oil and gas production"), "We need to protect [U.S.] energy dominance."),
             ("ene-01", -1, S("Sununu called the Inflation Reduction Act's climate and clean energy funding reckless spending"), None),
             ("ene-02", 1, S("Sununu would expand nuclear power in New Hampshire"), None),
             ("ene-04", 1, S("Sununu sponsored national pollutant limits in 2007 (S. 1177) and expanded White Mountain wilderness in 2006, and now backs permitting reform for transmission lines and pipelines"), None),
             ("eco-07", 1, S("Sununu supports the 2025 law's cuts to government programs"), None),
             ("edu-06", 2, S("Sununu supports New Hampshire's universal Education Freedom Accounts"), "It puts money and power in the hands of the parent."),
             ("hea-03", -1, S("Sununu supports the 2025 Medicaid cuts and work requirements"), None),
             ("hea-07", -1, S("Sununu says the ACA premium subsidies were meant to expire"), None),
             ("hea-04", 1, S("Sununu would loosen federal health regulations and expand health savings accounts"), "We need more competition."),
             ("imm-07", 1, S("Sununu says people here illegally who commit crimes should be deported"), None),
             ("imm-03", 1, S("Sununu supports legal immigration programs and would work to fix them"), None),
             ("imm-09", 1, S("Sununu says the U.S. needs seasonal workers"), None),
             ("def-04", -1, S("Sununu says presidents have the right to defend what they see as national security interests"), None),
             ("def-15", 0, S("Sununu says he would not have started the Iran war but defends the president's right to act"), "If you're asking me if I would have done this, no"),
             ("soc-12", -1, S("Sununu praised the Supreme Court ruling upholding bans on transgender athletes in girls' sports (2026)"), None),
             ("eco-03", -1, S("Sununu opposed raising the federal minimum wage (2005)"), "pricing some workers out of the market"),
             ("eco-01", -2, S("Sununu supports extending the 2017 tax cuts"), "voting for the biggest tax increase in American history"),
             ("gov-05", 2, S("Sununu supports a voter ID bill and proof of citizenship to register"), "Attach it to every critical piece of legislation."))},
    ],
}

governor = {
    "id": "NH-GOV",
    "candidates": [
        {"id": "NH-GOV:ayotte", "name": "Kelly Ayotte", "party": "R",
         "bio": "Governor of New Hampshire since 2025, U.S. senator from 2011 to 2017 and earlier state attorney general.",
         "positions": P(
             ("soc-04", -2, NHPR_VETOES("Ayotte pledged to veto any further abortion restrictions and in 2026 vetoed a bill on abortion conscience objections"), "I will veto it."),
             ("edu-06", 2, VNEWS_EFA("Ayotte signed SB 295, making Education Freedom Accounts universal (June 2025)"), None),
             ("cri-06", -1, MONITOR("Ayotte signed a law tightening what she calls a broken bail system"), None),
             ("hou-04", 1, WCAX("Ayotte signed a dozen bills to increase housing, including regulatory changes"), None),
             ("hou-06", 1, NHPR_VETOES("Ayotte vetoed a bill letting landlords demand an extra month's deposit from low-income tenants (2026)"), None),
             ("soc-07", 1, WCAX("Ayotte backed child care tax credits"), None),
             ("sta-08", 1, MONITOR("Ayotte increased benefits for law enforcement"), None),
             ("hea-06", 1, MONITOR("Ayotte directed more money to mental health care"), None),
             ("gov-05", 1, BULLETIN_ID("Ayotte signed a bill barring the use of student IDs to vote (2026)"), None),
             ("soc-11", -2, NHPR_YOUTH("Ayotte signed HB 377, barring puberty blockers and hormone treatment for gender transition before 18 (Aug. 2025)"), "these bills represent a balanced, bipartisan effort to protect children"),
             ("imm-08", 1, NHPR_ICE("Ayotte signed HB 511 and SB 62, requiring local police to cooperate with federal immigration enforcement (May 2025)"), None))},
        {"id": "NH-GOV:warmington", "name": "Cinde Warmington", "party": "D",
         "bio": "Health care lawyer and New Hampshire executive councilor from 2021 to 2025.",
         "officialSite": "https://www.cindewarmington.com/",
         "positions": P(
             ("edu-06", -2, MONITOR("Warmington would repeal Education Freedom Accounts"), "school voucher scam"),
             ("hou-01", 1, MONITOR("Warmington would put more state money into matching federal affordable housing funds"), None),
             ("sta-02", 1, MONITOR("Warmington would give towns more state aid for school construction"), None),
             ("eco-10", -1, WCAX("Warmington would push for consumer refunds on tariffs"), None),
             ("eco-02", 1, WCAX("Warmington would suspend the state gas tax and rules out new taxes on working people"), None),
             ("imm-08", -1, WARMINGTON_SITE("Warmington opposes the planned ICE detention facility in Merrimack"), "say no to ICE's human warehouse in Merrimack or anywhere else"))},
    ],
}

write("data/research/NH.json", [senate, governor], "New Hampshire U.S. Senate and governor races, researched Oct. 25, 2026.", updated=READ)
