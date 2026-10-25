"""Researched positions for Nebraska's statewide races: U.S. Senate (Ricketts vs.
Osborn) and governor (Pillen vs. Walz). Writes data/research/NE.json.

Senate positions come from guides.vote's nonpartisan Nebraska guide, which ties
each stance to a vote, bill or statement (read Oct. 25, 2026). Governor positions
come from the Flatwater Free Press voter guide, bills Gov. Pillen signed and
campaign coverage. Researched Oct. 25, 2026.

    py scripts/research/nebraska_2026.py
"""

from common import P, article, guide, page, write

READ = "2026-10-25"
S = guide("2026 Nebraska U.S. Senate voters guide", "https://guides.vote/guide/2026-nebraska-us-senate-voters-guide/", READ)
FLATWATER = lambda note: page(f"Flatwater Free Press voter guide: {note}", "https://voterguide.flatwaterfreepress.org/race/governor/", READ)  # noqa: E731
AP_2023 = article("Associated Press via WECT, May 22, 2023", "https://www.wect.com/2023/05/22/nebraska-governor-sign-12-week-abortion-ban-limits-gender-affirming-care-minors/", "2023-05-22")
NEX_ABORTION = article("Nebraska Examiner, June 29, 2023", "https://www.newsfromthestates.com/article/nebraska-gov-jim-pillen-says-he-wont-stop-abortion-seeks-total-ban", "2023-06-29")
NEX_SCHOLARSHIPS = article("Nebraska Examiner, May 30, 2023", "https://nebraskaexaminer.com/2023/05/30/nebraska-gov-pillen-signs-opportunity-scholarships-proposal-into-law/", "2023-05-30")
WOWT_BORDER = article("WOWT, July 31, 2023", "https://www.wowt.com/2023/07/31/gov-pillen-deploying-60-nebraska-national-guard-soldiers-southern-border", "2023-07-31")
WOWT_WALZ = article("WOWT, Oct. 19, 2026", "https://www.wowt.com/2026/10/19/election-2026-lynne-walz-promises-expedite-medical-marijuana-day-one/", "2026-10-19")
NORFOLK = article("Norfolk Daily News, Aug. 4, 2026", "https://norfolkdailynews.com/select/news/walz-pitches-bipartisan-leadership-rural-outreach-during-campaign-stop/article_73853100-9082-4d57-8b0d-af8f4117d1b6.html", "2026-08-04")

senate = {
    "id": "NE-SEN",
    "candidates": [
        {"id": "NE-SEN:osborn", "name": "Dan Osborn", "party": "I",
         "bio": "Navy veteran and union leader who led the 2021 Kellogg's strike in Omaha; ran as an independent for Senate in 2024.",
         "officialSite": "https://www.osbornforsenate.com/",
         "positions": P(
             ("soc-03", 2, S("Osborn would put Roe v. Wade into law and says the decision belongs to a woman and her doctor"), "the government should not be making health decisions for people"),
             ("soc-04", -1, S("Osborn would restore Roe v. Wade's protections in federal law"), None),
             ("ene-01", 1, S("Osborn supports a transition to clean energy and landowners' right to lease land for solar"), None),
             ("eco-04", 2, S("Osborn would break up agricultural monopolies and investigate corporate price gouging"), None),
             ("edu-06", -2, S("Osborn opposes vouchers that fund private school tuition at public schools' expense"), None),
             ("edu-01", 1, S("Osborn on public schools"), "Strong and well-funded public schools are the backbone of the American education system."),
             ("ene-04", 1, S("Osborn would keep air, water and land clean and opposes data center expansion"), "We must protect our water and land, not sell it to the highest bidder."),
             ("hea-02", 2, S("Osborn would let Medicaid negotiate drug prices directly with manufacturers"), None),
             ("imm-01", 1, S("Osborn says the administration's border policy is the right thing to do (Newsweek, April 2026)"), None),
             ("def-15", -1, S("Osborn says the Iran war's fuel and fertilizer costs will bankrupt farmers"), "With this war, I'm not seeing why we are in it."),
             ("eco-09", 2, S("Osborn supports the PRO Act and opposes a national right-to-work law"), None),
             ("soc-10", 1, S("Osborn supports same-sex marriage"), None),
             ("soc-02", 1, S("Osborn on discrimination"), "I oppose discrimination for any reason."),
             ("eco-03", 2, S("Osborn would raise the federal minimum wage to $15, Nebraska's current rate"), None),
             ("eco-01", 2, S("Osborn supports a wealth tax and closing multinational tax loopholes"), "We cannot afford more tax cuts for the ultra-wealthy."))},
        {"id": "NE-SEN:ricketts", "name": "Pete Ricketts", "party": "R",
         "bio": "U.S. senator since 2023 and governor of Nebraska from 2015 to 2023.",
         "officialSite": "https://petericketts.com/",
         "positions": P(
             ("soc-04", 2, S("Ricketts supports a 12-week abortion ban and cosponsored bills to ban mailed abortion pills"), None),
             ("soc-03", -2, S("Ricketts supports the pro-life movement and funded a petition drive for a constitutional abortion ban in Nebraska"), None),
             ("ene-06", -2, S("Ricketts praised the EPA's repeal of the greenhouse gas endangerment finding (2026)"), None),
             ("ene-01", -1, S("Ricketts voted to end the clean energy tax credits (Senate roll call 372, 2025)"), None),
             ("cri-04", 2, S("Ricketts sponsored S. 1569 for harsher penalties on criminals who target police and supports murder charges for fentanyl dealers"), None),
             ("edu-06", 2, S("Ricketts is a vocal supporter of school choice and proposed public-funded private school scholarships as governor"), None),
             ("ene-04", -2, S("Ricketts voted to overturn the Clean Water Act streams and wetlands rule (Senate roll call 79, 2023) and to end mining limits near the Boundary Waters (Senate roll call 84, 2026)"), None),
             ("hea-03", -2, S("Ricketts voted for the 2025 law that cut Medicaid (Senate roll call 372) and opposed Medicaid expansion as governor"), None),
             ("imm-08", 2, S("Ricketts voted against repealing $75 billion in ICE funding (Senate roll call 18, 2026) and introduced a bill against sanctuary cities"), None),
             ("def-04", -2, S("Ricketts voted against requiring congressional authorization for military action in Iran (Senate roll call 46, 2026)"), None),
             ("def-15", 2, S("Ricketts on Iran"), "We have to destroy [Iran's] ability to threaten us."),
             ("def-01", 1, S("Ricketts voted for $150 billion more for national security in the 2025 tax and spending law"), None),
             ("eco-09", -2, S("Ricketts sponsored the National Right to Work Act (S. 532)"), None),
             ("soc-12", -2, S("Ricketts cosponsored S. 9 to ban transgender students from girls' sports and opposed adding gender identity to Title IX"), "classic big government overreach"),
             ("eco-03", -2, S("Ricketts opposed Nebraska's voter-approved minimum wage increase (2022)"), "Employers should pay what the market demands to hire people."),
             ("eco-01", -2, S("Ricketts voted to extend the 2017 tax cuts and sponsored repeal of the estate tax (S. 587)"), None),
             ("eco-12", -1, S("As governor, Ricketts signed cuts to Nebraska's corporate and top individual income tax rates"), None),
             ("gov-05", 2, S("Ricketts led the 2022 campaign for Nebraska's voter ID amendment"), None),
             ("eco-07", 1, S("Ricketts says he helped cut nearly $2 trillion in federal spending (campaign site)"), None),
             ("agr-01", 1, S("Ricketts supports federal assistance for farmers and ranchers"), None))},
    ],
}

governor = {
    "id": "NE-GOV",
    "candidates": [
        {"id": "NE-GOV:pillen", "name": "Jim Pillen", "party": "R",
         "bio": "Governor of Nebraska since 2023, a hog producer and a former University of Nebraska regent.",
         "positions": P(
             ("soc-04", 2, AP_2023("Pillen signed a 12-week abortion ban with exceptions for rape, incest and the mother's life (2023)"), "It's about protecting our kids and saving babies. Pure and simple."),
             ("soc-03", -2, NEX_ABORTION("Pillen says the 12-week limit is unacceptable and he will push to end abortion"), "I pushed hard to get us to 12, but we're going to end abortion."),
             ("soc-11", -2, AP_2023("Pillen signed limits on hormone treatment and puberty blockers for minors (2023)"), None),
             ("edu-06", 2, NEX_SCHOLARSHIPS("Pillen signed tax credits for donations to private school scholarships (LB 753, 2023)"), None),
             ("imm-01", 2, WOWT_BORDER("Pillen sent Nebraska National Guard soldiers to the Texas border (2023)"), None),
             ("sta-04", 2, FLATWATER("Pillen wants lower property taxes and hard caps on local spending"), None),
             ("eco-02", 1, FLATWATER("Pillen wants lasting tax cuts rather than tax shifts"), "durable, lasting tax cuts, not tax shifts"))},
        {"id": "NE-GOV:walz", "name": "Lynne Walz", "party": "D",
         "bio": "Nebraska state senator from 2017 to 2025, where she chaired the Education Committee.",
         "positions": P(
             ("soc-04", -1, FLATWATER("Walz says voters' recent abortion decisions should be respected and wants exceptions for rape, incest and the mother's life"), None),
             ("sta-04", 2, WOWT_WALZ("Walz says she voted for most property tax bills and would back any plan to reduce them"), "I probably have voted for the majority of property tax legislation that came across our desk."),
             ("soc-12", 1, WOWT_WALZ("Walz voted against the Sports and Spaces Act on transgender athletes"), None),
             ("edu-01", 1, NORFOLK("Walz says the state should invest more in public education and support educators"), None),
             ("sta-02", 1, NORFOLK("Walz says the state should invest more in public education and support educators"), None),
             ("hou-09", 1, NORFOLK("Walz says lawmakers should spend more time on housing and rural broadband"), None),
             ("eco-02", 1, FLATWATER("Walz backs temporary tax holidays and targeted tax relief"), None))},
    ],
}

write("data/research/NE.json", [senate, governor], "Nebraska U.S. Senate and governor races, researched Oct. 25, 2026.", updated=READ)
