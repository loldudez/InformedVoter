"""Researched positions for Wisconsin's governor race (Crowley vs. Tiffany).
Writes data/research/WI.json.

Positions come from guides.vote's nonpartisan Wisconsin guide, which ties each
stance to a vote, bill or statement (read Oct. 25, 2026). Tiffany's recorded
House votes are added automatically by update_races.py. Researched Oct. 25, 2026.

    py scripts/research/wisconsin_2026.py
"""

from common import P, guide, write

READ = "2026-10-25"
G = guide("2026 Wisconsin governor voters guide", "https://guides.vote/guide/2026-wisconsin-governor-voters-guide/", READ)

governor = {
    "id": "WI-GOV",
    "candidates": [
        {"id": "WI-GOV:crowley", "name": "David Crowley", "party": "D",
         "bio": "Milwaukee County executive since 2020 and a former state Assembly member.",
         "officialSite": "https://www.crowleyforwi.com/",
         "positions": P(
             ("soc-03", 2, G("Crowley would write reproductive rights into the state constitution and supports access to mifepristone"), "protected at all costs"),
             ("soc-04", -2, G("Crowley opposed Wisconsin's 1849 abortion ban (Milwaukee County statement)"), None),
             ("ene-06", 2, G("Crowley backed Milwaukee County's net-zero-by-2050 goal"), "The climate crisis is a real, pressing threat."),
             ("ene-01", 1, G("Crowley supported the 2022 federal clean energy investments"), None),
             ("cri-01", 0, G("Crowley opposes defunding the police but says public safety investment doesn't mean more money for officers"), "We cannot defund the police."),
             ("cri-02", 1, G("Crowley supports police body cameras"), None),
             ("cri-08", 1, G("Crowley supports alternatives to incarceration"), None),
             ("edu-06", -1, G("Crowley would keep Wisconsin's voucher programs without expanding them (Wisconsin Examiner, Aug. 2026)"), None),
             ("edu-01", 2, G("Crowley would prioritize public school investment"), "invest in our public schools to make sure that they're the school of choice"),
             ("sta-02", 2, G("Crowley would prioritize public school investment"), "invest in our public schools to make sure that they're the school of choice"),
             ("ene-04", 2, G("Crowley opposes gutting PFAS protections and wants environmental guardrails on data centers"), "defend Wisconsin's water standards"),
             ("hea-03", 2, G("Crowley would use federal Medicaid matching funds to open BadgerCare to any household that wants it"), None),
             ("hea-01", 1, G("Crowley would open BadgerCare, with medical, dental and vision coverage, to any household that wants it"), None),
             ("hea-07", 1, G("Crowley supports extending the ACA premium tax credits"), None),
             ("sta-09", 1, G("Crowley would invest in mobile care and rural clinics"), None),
             ("imm-07", 1, G("Crowley says an undocumented person convicted of a heinous crime should be deported"), None),
             ("imm-08", -1, G("Crowley opposes requiring local police to partner with ICE"), None),
             ("eco-09", 2, G("Crowley would repeal Act 10 in full and protect the right to organize, bargain and strike"), "Labor unions are the lifeblood of the U.S."),
             ("soc-10", 2, G("Crowley supports repealing Wisconsin's constitutional ban on same-sex marriage"), None),
             ("soc-12", 1, G("Crowley backed a Milwaukee resolution against conversion therapy; on transgender athletes he would defer to the state athletic association"), None),
             ("soc-05", 2, G("Crowley would legalize medical and recreational marijuana"), "I will legalize it."),
             ("sta-03", 2, G("Crowley would raise the state minimum wage to $15 immediately and to $20 by 2030"), None),
             ("eco-01", 1, G("Crowley would raise income taxes on people making over $1 million"), None),
             ("sta-04", 1, G("Crowley says he would have signed the state deal lowering property taxes"), None),
             ("gov-05", -1, G("Crowley opposes requiring proof of citizenship to register to vote"), None),
             ("gov-06", 1, G("Crowley opposes limits on mail-in voting"), None))},
        {"id": "WI-GOV:tiffany", "name": "Tom Tiffany", "party": "R",
         "bio": "U.S. representative for Wisconsin's 7th District since 2020 and a former state senator.",
         "officialSite": "https://tomtiffany.com/",
         "positions": P(
             ("soc-03", -2, G("Tiffany cosponsored federal bills banning abortion once a heartbeat is detectable (H.R. 705, 2021; H.R. 175, 2023)"), None),
             ("soc-04", 2, G("Tiffany voted for Wisconsin's 20-week abortion limit (2015) and would uphold it"), "proud to be pro-life"),
             ("ene-01", -2, G("Tiffany introduced a bill barring federal funding for solar and wind projects on farmland (H.R. 1754)"), "Taxpayer dollars shouldn't be used to sacrifice farmland for green energy boondoggles."),
             ("ene-03", 2, G("Tiffany introduced a bill directing the Interior Department to issue oil and gas drilling permits on public land (H.R. 9024, 2022)"), None),
             ("ene-04", -1, G("Tiffany voted to undo limits on seven hazardous air pollutants (2025), though he would set environmental standards for data centers"), None),
             ("cri-04", 2, G("Tiffany introduced a bill raising penalties for certain violent crimes and opposes commutations for violent criminals"), "Crime is a policy choice."),
             ("cri-01", 1, G("Tiffany would give police more tools and training"), None),
             ("sta-08", 1, G("Tiffany would give police more tools and training"), None),
             ("edu-06", 2, G("Tiffany sponsored federal tax credits for private school scholarships (H.R. 833) and urged Wisconsin to opt in"), "expand access to quality education for every child"),
             ("hea-07", -1, G("Tiffany voted against extending ACA premium subsidies for three years (House roll call 11, 2026)"), None),
             ("hea-04", 1, G("Tiffany backs more choice and competition in health care, upfront prices and direct payments to doctors"), None),
             ("imm-08", 2, G("Tiffany voted for $75 billion more for ICE and $70 billion more for DHS"), "Deporting illegal aliens is how you make America safer."),
             ("imm-06", -2, G("Tiffany introduced a bill letting states block refugee resettlement (H.R. 6414)"), None),
             ("eco-09", -2, G("Tiffany cosponsored a national right-to-work bill (H.R. 1232) and voted for Act 10 (2011)"), None),
             ("soc-02", -1, G("Tiffany voted against the Equality Act (H.R. 5; House roll call 39, 2021)"), None),
             ("soc-11", -1, G("Tiffany opposes gender transition surgery for minors"), None),
             ("sta-03", -1, G("Tiffany says a $20 minimum wage would cost rural jobs; in 2020 he said a $15 minimum would cost jobs"), None),
             ("eco-02", 2, G("Tiffany would cut income taxes 10% for families earning under $150,000 and end state income tax on tips and overtime"), None),
             ("sta-04", 1, G("Tiffany would repeal the partial veto that lets schools raise property taxes for 400 years"), None),
             ("gov-05", 2, G("Tiffany sponsored H.R. 7300, requiring voter ID"), None),
             ("gov-06", -2, G("Tiffany sponsored H.R. 7300, requiring mail ballots to arrive by Election Day, and voted against the John Lewis Voting Rights Act (2021)"), None))},
    ],
}

write("data/research/WI.json", [governor], "Wisconsin governor race, researched Oct. 25, 2026.", updated=READ)
