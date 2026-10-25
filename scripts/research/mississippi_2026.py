"""Researched positions for Mississippi's U.S. Senate race (Hyde-Smith vs. Colom).
Writes data/research/MS.json.

Positions come from guides.vote's nonpartisan Mississippi guide, which ties each
stance to a vote, bill or statement (read Oct. 25, 2026). Researched Oct. 25, 2026.

    py scripts/research/mississippi_2026.py
"""

from common import P, guide, write

READ = "2026-10-25"
S = guide("2026 Mississippi U.S. Senate voters guide", "https://guides.vote/guide/2026-mississippi-us-senate-voters-guide/", READ)

senate = {
    "id": "MS-SEN",
    "candidates": [
        {"id": "MS-SEN:hyde-smith", "name": "Cindy Hyde-Smith", "party": "R",
         "bio": "U.S. senator since 2018 and a former Mississippi agriculture commissioner.",
         "officialSite": "https://cindyhydesmith.com/",
         "positions": P(
             ("soc-04", 2, S("Hyde-Smith chairs the Senate Pro-Life Caucus and opposes taxpayer funding of abortion"), None),
             ("soc-03", -2, S("Hyde-Smith says unborn children have a right to life from their Creator"), None),
             ("ene-01", -1, S("Hyde-Smith voted to end the clean energy tax credits (Senate roll call 372, 2025)"), None),
             ("ene-09", 1, S("Hyde-Smith supported incentives for a new electric vehicle battery plant in Mississippi"), None),
             ("ene-03", 1, S("Hyde-Smith supports the administration's push for more oil drilling"), None),
             ("ene-06", -1, S("Hyde-Smith criticizes Democratic climate policy"), "Democrats' radical Green New Deal climate agenda"),
             ("ene-04", -2, S("Hyde-Smith voted to end mining limits near the Boundary Waters (Senate roll call 84, 2026) and seeks repeal of a gasoline vapor testing rule"), None),
             ("cri-01", 1, S("Hyde-Smith secured federal funding for law enforcement technology and training (2024)"), None),
             ("eco-06", -1, S("Hyde-Smith voted against the infrastructure law (Senate roll call 314, 2021)"), None),
             ("agr-01", 1, S("Hyde-Smith called for farm aid after commodity prices fell"), None),
             ("eco-05", 1, S("Hyde-Smith introduced the Buying American Cotton Act, a tax credit for products made with U.S. cotton (S. 1919)"), None),
             ("edu-07", 1, S("Hyde-Smith says Washington should support states' schools without dictating to them"), "should not dictate how they get the job done"),
             ("edu-06", 1, S("Hyde-Smith supported a $600,000 federal grant for Mississippi charter schools (2023)"), None),
             ("hea-03", -1, S("Hyde-Smith voted for the 2025 law that cut Medicaid (Senate roll call 372)"), None),
             ("hea-07", -1, S("Hyde-Smith voted against extending the ACA tax credits (Senate roll call 644, 2025)"), None),
             ("eco-01", -1, S("Hyde-Smith voted to extend the 2017 tax cuts (2025), though she also voted for a tax increase on the ultrawealthy to help rural hospitals (Senate roll call 355, 2025)"), "helping unleash a wave of prosperity across America"),
             ("imm-01", 2, S("Hyde-Smith supports the border wall"), "secure its borders and control who enters our country"),
             ("imm-10", 2, S("Hyde-Smith introduced a bill requiring all employers to use E-Verify"), None),
             ("imm-08", 1, S("Hyde-Smith says ICE is pursuing law and order (WLOX, Feb. 2026)"), None),
             ("def-04", -2, S("Hyde-Smith voted against requiring congressional authorization for military action in Iran (Senate roll call 46, 2026)"), None),
             ("def-15", 2, S("Hyde-Smith opposed limiting the Iran war"), "embolden our enemies and endanger our brave fighting men and women"),
             ("soc-10", -1, S("Hyde-Smith voted against the Respect for Marriage Act (Senate roll call 362, 2022)"), "believe in the traditional definition of marriage"),
             ("soc-12", -2, S("Hyde-Smith introduced a resolution defining sex as biological sex at birth (S.Res. 53) and opposes transgender girls in girls' sports"), None),
             ("eco-10", 2, S("Hyde-Smith calls tariffs a really good tool against unfair trade"), "I support President Trump's effort."),
             ("gov-05", 2, S("Hyde-Smith supports voter ID and proof of citizenship to register"), "It is lawful, it is fair, and it works."))},
        {"id": "MS-SEN:colom", "name": "Scott Colom", "party": "D",
         "bio": "District attorney for Mississippi's 16th Circuit Court District since 2016.",
         "officialSite": "https://scottcolom.com/",
         "positions": P(
             ("soc-03", 1, S("Colom calls himself pro-life as a Christian but would trust women to make their own choices, and supports IVF access"), None),
             ("cri-08", 2, S("As district attorney, Colom expanded pretrial diversion and started Mississippi's first restorative justice program"), "alternatives to incarceration for young people"),
             ("eco-02", 1, S("Colom would end income tax for teachers and police officers earning under $75,000"), None),
             ("edu-01", 1, S("Colom criticized the 2025 federal funding freeze that cut $137 million from Mississippi schools"), "fewer resources, fewer safeguards, and more young lives at risk"),
             ("hea-03", 2, S("Colom supports expanding Medicaid"), "We have to cancel those healthcare cuts."),
             ("hea-07", 1, S("Colom supports extending the ACA tax credits"), None),
             ("imm-01", 1, S("Colom says President Trump has done a good job securing the border"), None),
             ("imm-03", -1, S("Colom opposes H-1B visas, saying companies replace American workers with foreign ones"), "those jobs need to be in Mississippi"),
             ("def-04", 2, S("Colom says the Constitution requires Congress to declare war"), None),
             ("def-15", -1, S("Colom on Iran"), "I don't know what the objective is right now in the war in Iran."),
             ("soc-12", 0, S("Colom says biological boys shouldn't play girls' sports but in 2021 opposed criminalizing gender-affirming care"), "We should not criminalize people's identity."),
             ("eco-03", 1, S("Colom says the minimum wage hasn't risen in nearly 20 years"), "when you raise the minimum wage, you boost all wages"),
             ("eco-10", -2, S("Colom says tariffs raise prices and hurt farmers, and that Congress should set them"), "Tariffs have been terrible for Mississippi."),
             ("eco-01", 1, S("Colom criticized extending the 2017 tax cuts"), "a permanent tax handout to people making more than $600,000 a year"),
             ("gov-05", -1, S("Colom opposes Mississippi's 2026 law checking new voters' citizenship against a federal database"), None))},
    ],
}

write("data/research/MS.json", [senate], "Mississippi U.S. Senate race, researched Oct. 25, 2026.", updated=READ)
