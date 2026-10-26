"""Researched positions for Arizona's governor race (Hobbs vs. Biggs).
Writes data/research/AZ.json.

Positions come from guides.vote's nonpartisan Arizona guide, which ties each
stance to a vote, bill, executive action or statement (read Oct. 25, 2026).
Biggs's recorded House votes are added automatically by update_races.py.
Researched Oct. 25, 2026.

    py scripts/research/arizona_2026.py
"""

from common import P, guide, write

READ = "2026-10-25"
G = guide("2026 Arizona governor voters guide", "https://guides.vote/guide/2026-arizona-governor-voters-guide/", READ)

governor = {
    "id": "AZ-GOV",
    "candidates": [
        {"id": "AZ-GOV:hobbs", "name": "Katie Hobbs", "party": "D",
         "bio": "Governor of Arizona since 2023 and formerly Arizona secretary of state.",
         "positions": P(
             ("soc-03", 2, G("Hobbs signed the repeal of Arizona's 1864 abortion ban (HB 2677, 2024)"), "we should recommit to protecting women's bodily autonomy"),
             ("soc-04", -2, G("Hobbs barred county attorneys from prosecuting abortion providers (Executive Order 2023-11)"), None),
             ("ene-01", 2, G("Hobbs's energy taskforce recommends utility-scale wind and solar, and she seeks a 640-acre solar farm"), "build a 21st-century clean energy economy"),
             ("ene-06", 1, G("Hobbs joined the U.S. Climate Alliance (2023)"), None),
             ("ene-04", 1, G("Hobbs joined a multistate lawsuit over the EPA's repeal of a toxic air pollutant rule (2026), though she sought flexibility on ozone standards (2024)"), None),
             ("edu-06", -2, G("Hobbs seeks an income cap on Arizona's universal ESA vouchers and vetoed opting into the federal private school tax credit (2026)"), None),
             ("sta-08", 1, G("Hobbs directed state troopers to expand patrols with up to 14,000 hours of overtime (2026)"), None),
             ("cri-07", 1, G("Hobbs allocated more than $25 million for crime victims and violent crime prevention"), None),
             ("hea-03", 2, G("Hobbs expanded KidsCare and opposed the 2025 federal Medicaid cuts"), None),
             ("hea-02", 1, G("Hobbs joined a multistate public pharmacy collaborative offering discounted prescriptions (2025)"), None),
             ("imm-01", 1, G("Hobbs created Operation Desert Guardian to expand border security (executive order, 2025)"), None),
             ("imm-08", 0, G("Hobbs funded 50 state troopers for immigration enforcement but vetoed bills requiring local cooperation with ICE (2025)"), None),
             ("eco-09", 2, G("Hobbs opposes the 2026 ballot measure restricting public employee unions"), "I grew up in a working-class family, and I am a proud union member."),
             ("soc-02", 2, G("Hobbs signed executive orders barring workplace discrimination by sexual orientation and gender identity (2023)"), None),
             ("soc-12", 2, G("Hobbs vetoed a bill limiting which restrooms transgender students can use"), "I will always stand up for your freedom to be who you are."),
             ("eco-02", 2, G("Hobbs signed the 2026 budget with a $1.4 billion middle-class tax cut and no state tax on tips and overtime"), None),
             ("sta-10", -1, G("Hobbs opposes business tax breaks and signed a three-year pause on a data center tax credit (2026)"), None),
             ("gov-06", 1, G("Hobbs vetoed SB 1001, which would have set ID requirements for voting by mail"), None))},
        {"id": "AZ-GOV:biggs", "name": "Andy Biggs", "party": "R",
         "bio": "U.S. representative for Arizona's 5th District since 2017 and a former president of the Arizona Senate.",
         "officialSite": "https://biggsforarizona.com/",
         "positions": P(
             ("soc-04", 2, G("Biggs sponsored the Life at Conception Act (H.R. 722), which would ban abortion nationwide"), None),
             ("soc-03", -2, G("Biggs on the overturning of Roe v. Wade"), "a major victory for the unborn"),
             ("ene-01", -2, G("Biggs voted against the 2022 clean energy investments, to repeal them in 2023 and to end the tax credits in 2025"), None),
             ("ene-06", -1, G("Biggs voted to overturn a Labor Department rule letting retirement managers weigh climate risk (H.J.Res. 30, 2023)"), None),
             ("ene-04", -2, G("Biggs voted to undo limits on seven hazardous air pollutants (2025) and to end mining limits near the Boundary Waters (2026), and opposed stricter air pollution limits for Maricopa County"), None),
             ("cri-01", 1, G("Biggs would fully fund public safety departments"), None),
             ("sta-08", 1, G("Biggs would fully fund public safety departments"), None),
             ("cri-04", 1, G("Biggs introduced mandatory minimum sentences for certain crimes in Washington, D.C. (H.R. 5172)"), None),
             ("edu-06", 2, G("Biggs introduced H.R. 83 to let federal funds follow low-income students to private or charter schools and would expand Arizona's universal ESA vouchers"), None),
             ("hea-07", -2, G("Biggs introduced a bill to repeal the ACA (H.R. 114), calling it a complete failure, and voted against extending its subsidies (2026)"), None),
             ("imm-01", 2, G("Biggs would fund and complete the border wall"), None),
             ("imm-08", 2, G("Biggs supports mass deportations and wants federal and local police to partner on border security"), None),
             ("imm-02", -1, G("Biggs voted in 2021 against a path to permanent residency for Dreamers (H.R. 6)"), None),
             ("eco-09", -2, G("Biggs voted against the PRO Act (2021) and against restoring federal workers' bargaining rights (2025)"), None),
             ("soc-02", -1, G("Biggs voted against the Equality Act (House roll call 39, 2021)"), None),
             ("soc-12", -2, G("Biggs sponsored H.R. 28 to bar transgender students from girls' and women's sports"), "denies the biological facts that men and women are the two genders"),
             ("eco-02", 1, G("Biggs would eventually eliminate Arizona's income tax and pledged never to raise taxes"), "I will never raise taxes on Arizonans."),
             ("gov-05", 2, G("Biggs sponsored H.R. 7296, requiring proof of citizenship to register, and wants a Florida-style election law"), None))},
    ],
}

write("data/research/AZ.json", [governor], "Arizona governor race, researched Oct. 25, 2026.", updated=READ)
