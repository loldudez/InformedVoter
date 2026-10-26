"""Researched details for Oklahoma's statewide races: U.S. Senate (Hern vs. Thomas)
and governor (Mazzei vs. Munson). Writes data/research/OK.json.

Positions come from Kevin Hern's recorded House votes, News 9's side-by-side on
the governor's race (Oct. 6, 2026), and coverage of N'Kiyla Jasmine Thomas's
campaign, which has published little on specific issues. Researched Oct. 24, 2026.

    py scripts/research/oklahoma_2026.py
"""

from common import P, source, vote_positions, write

NEWS9 = source("News 9: Oklahoma governor race: where Mike Mazzei and Cyndi Munson stand on key issues",
               "https://www.news9.com/oklahoma-elections/mike-mazzei-cyndi-munson-oklahoma-governor-key-issues", "2026-10-06")
NEWS6 = source("News On 6: N’Kiyla Jasmine Thomas wins the Democratic runoff for U.S. Senate",
               "https://www.newson6.com/oklahoma-politics/democratic-runoff-oklahoma-us-senate-results", "2026-08-25")
OKWATCH = source("Oklahoma Watch (via Oklahoma Gazette): previewing the Democratic runoff for U.S. Senate",
                 "https://www.okgazette.com/news/democracy-watch-previewing-the-democratic-runoff-for-u-s-senate/", "2026-08-10")

senate = {
    "id": "OK-SEN",
    "candidates": [
        {"id": "OK-SEN:hern", "name": "Kevin Hern", "party": "R",
         "bio": "U.S. Representative for Oklahoma’s 1st District since 2018 and a former McDonald’s franchise owner.",
         "positions": P(*vote_positions("Hern", {
             "rfma": "Nay", "whpa": "Nay", "ira": "Nay", "iija": "Nay", "chips": "Nay", "hr1_2025": "Aye",
             "ukraine": "Nay", "israel": "Yea", "border": "Yea", "energy": "Yea"}))},
        {"id": "OK-SEN:thomas", "name": "N’Kiyla Jasmine Thomas", "party": "D",
         "bio": "Nurse, active-duty military spouse and Chickasaw Nation citizen from Ardmore, running for office for the first time.",
         "positions": P(
             ("hou-08", 1, NEWS6, "fixing Oklahoma’s roads and bridges"),
             ("gov-11", 1, OKWATCH, None))},
    ],
    "notes": [{"text": "This is the seat Markwayne Mullin left. Thomas has published few specific policy positions, so most questions are unclear for her rather than guessed.", "source": "News On 6", "url": NEWS6["url"]}],
}

governor = {
    "id": "OK-GOV",
    "candidates": [
        {"id": "OK-GOV:mazzei", "name": "Mike Mazzei", "party": "R",
         "bio": "Former Oklahoma state senator; won the Aug. 25 Republican runoff over Attorney General Gentner Drummond.",
         "officialSite": "https://www.mikeforok.com/",
         "positions": P(
             ("sta-04", 2, NEWS9, None),
             ("eco-02", 1, NEWS9, None),
             ("edu-04", 1, NEWS9, None),
             ("soc-03", -2, NEWS9, None),
             ("soc-04", 2, NEWS9, None))},
        {"id": "OK-GOV:munson", "name": "Cyndi Munson", "party": "D",
         "bio": "Oklahoma City state representative since 2015.",
         "positions": P(
             ("eco-12", 1, NEWS9, None),
             ("sta-02", 2, NEWS9, "More funding for public education"),
             ("edu-01", 2, NEWS9, "More funding for public education"),
             ("edu-04", 2, NEWS9, None),
             ("edu-06", -2, NEWS9, "Repeal Oklahoma’s parental choice tax voucher"),
             ("soc-03", 2, NEWS9, None),
             ("soc-04", -2, NEWS9, None),
             ("sta-09", 1, NEWS9, None),
             ("sta-10", -1, NEWS9, None),
             ("soc-07", 2, NEWS9, None),
             ("edu-09", 2, NEWS9, None),
             ("edu-02", 1, NEWS9, None))},
    ],
}

write("data/research/OK.json", [senate, governor], "Oklahoma U.S. Senate and governor races, researched Oct. 24, 2026.")
