"""Researched positions for North Carolina's U.S. Senate race (Cooper vs. Whatley).
Writes data/research/NC.json.

Positions come from guides.vote's nonpartisan North Carolina guide, which ties
each stance to a vote, veto, bill or statement (read Oct. 25, 2026).
Researched Oct. 25, 2026.

    py scripts/research/north_carolina_2026.py
"""

from common import P, guide, write

READ = "2026-10-25"
S = guide("2026 North Carolina U.S. Senate voters guide", "https://guides.vote/guide/2026-north-carolina-us-senate-voters-guide/", READ)

senate = {
    "id": "NC-SEN",
    "candidates": [
        {"id": "NC-SEN:cooper", "name": "Roy Cooper", "party": "D",
         "bio": "Governor of North Carolina from 2017 to 2025 and state attorney general from 2001 to 2017.",
         "officialSite": "https://roycooper.com/",
         "positions": P(
             ("soc-03", 2, S("Cooper vetoed North Carolina's 12-week abortion ban (S 20, 2023)"), "to keep politicians out of the doctor's exam room"),
             ("soc-04", -2, S("Cooper called the 12-week ban dangerous for women (CNN, 2023)"), None),
             ("ene-06", 2, S("Cooper ordered state greenhouse gas cuts of at least 50% below 2005 levels by 2030 and net zero by 2050"), "The urgency of the climate crisis is real."),
             ("ene-01", 2, S("Cooper set goals of 2.8 gigawatts of offshore wind by 2030 and 8 by 2040 (Executive Order 218)"), None),
             ("ene-04", 2, S("Cooper vetoed a bill limiting wetlands protections (S 582, 2023) and re-established a state environmental justice board"), None),
             ("cri-07", 1, S("Cooper created North Carolina's first Community Violence Prevention Strategic Plan (2024)"), None),
             ("eco-04", 2, S("Cooper supports stronger antitrust rules and banning algorithms that raise grocery prices"), None),
             ("soc-07", 1, S("Cooper supports child care subsidies for employees"), None),
             ("edu-06", -2, S("Cooper vetoed the private school voucher expansion (H 10, 2024) and wants a moratorium on vouchers"), None),
             ("hea-03", 2, S("Cooper expanded Medicaid to more than 600,000 North Carolinians and would reverse the federal Medicaid cuts"), None),
             ("hea-07", 2, S("Cooper would restore the ACA tax credits"), None),
             ("hea-02", 1, S("Cooper would cap prescription drug costs"), None),
             ("imm-08", -1, S("Cooper vetoed bills requiring sheriffs to work with ICE on jail inmates (2019, 2022, 2024) and wants ICE reforms before more funding"), None),
             ("def-04", 2, S("Cooper says Congress should take back its constitutional authority to declare war"), None),
             ("def-15", -1, S("Cooper is deeply concerned about the reasons for the Iran war and its exit strategy"), None),
             ("eco-09", 0, S("Cooper praises unions but signed 2017 limits on farmworker union representation (S 615)"), None),
             ("soc-11", 1, S("Cooper vetoed the ban on gender transition care for minors (H 808, 2023)"), None),
             ("soc-12", 2, S("Cooper vetoed bills limiting transgender sports participation and transition care (2023) and as attorney general refused to defend the 2016 bathroom bill"), None),
             ("eco-03", 1, S("Cooper supported raising North Carolina's minimum wage (2019) and proposed $15 an hour for school support staff"), None),
             ("eco-01", 1, S("Cooper opposed further income tax cuts for corporations and high earners"), None),
             ("gov-05", -1, S("Cooper vetoed a voter ID bill (S 824, 2018)"), None),
             ("gov-06", 1, S("Cooper vetoed added absentee voting restrictions (S 747, 2023)"), None))},
        {"id": "NC-SEN:whatley", "name": "Michael Whatley", "party": "R",
         "bio": "Chair of the Republican National Committee from 2024 to 2025 and a former chair of the North Carolina Republican Party.",
         "positions": P(
             ("soc-03", -2, S("Whatley on abortion (USA Today, 2024)"), "proud to be the most pro-life chair in the history of the Republican Party"),
             ("soc-04", 2, S("Whatley called the veto of North Carolina's 12-week ban the radical abortion-on-demand position"), None),
             ("ene-03", 2, S("Whatley backs an all-of-the-above energy approach and lobbied for offshore drilling off North Carolina"), None),
             ("ene-04", -1, S("As an energy industry lobbyist, Whatley sought to limit air pollution rules and called EPA air provisions an unfunded mandate (2014)"), None),
             ("cri-01", 2, S("Whatley would put more police on the street and pay them better"), "We need to back the blue."),
             ("cri-06", -1, S("Whatley would create a federal version of Iryna's Law, limiting pretrial release for people accused of violent crimes"), None),
             ("eco-07", 1, S("Whatley supports the 2025 law's cuts to Medicaid and SNAP"), "We do not need waste, fraud and abuse in these programs."),
             ("hea-03", -1, S("Whatley defended the 2025 law's Medicaid cuts"), None),
             ("hea-04", 1, S("Whatley wants market-driven replacements for the ACA"), "We need to get the government out of the way"),
             ("edu-06", 2, S("Whatley supports the federal Education Freedom Tax Credit for private school scholarships"), "Dollars should follow students."),
             ("imm-08", 1, S("Whatley welcomed the 2025 Border Patrol operation in Charlotte as strong, decisive action"), None),
             ("imm-07", 1, S("Whatley praised taking violent criminals who are here illegally off the street"), None),
             ("def-15", 2, S("Whatley says he absolutely supports the Iran war"), "very, very important from our national security perspective"),
             ("eco-01", -1, S("Whatley supports the 2025 law extending the 2017 tax cuts"), None),
             ("gov-05", 2, S("Whatley led the push for North Carolina's voter ID requirement and supports the SAVE America Act"), None))},
    ],
}

write("data/research/NC.json", [senate], "North Carolina U.S. Senate race, researched Oct. 25, 2026.", updated=READ)
