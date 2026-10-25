"""Researched positions for Nevada's governor race (Lombardo vs. Ford). Writes
data/research/NV.json.

Positions come from guides.vote's nonpartisan Nevada guide, which ties each
stance to a vote, bill, lawsuit or statement (read Oct. 25, 2026).
Researched Oct. 25, 2026.

    py scripts/research/nevada_2026.py
"""

from common import P, guide, write

READ = "2026-10-25"
G = guide("2026 Nevada governor voters guide", "https://guides.vote/guide/2026-nevada-governor-voters-guide/", READ)

governor = {
    "id": "NV-GOV",
    "candidates": [
        {"id": "NV-GOV:ford", "name": "Aaron Ford", "party": "D",
         "bio": "Nevada attorney general since 2019.",
         "officialSite": "https://www.fordfornevada.com/",
         "positions": P(
             ("soc-03", 2, G("Ford sued the FDA over restrictions on the abortion pill (2023)"), "Throughout my career, I've fought to protect reproductive freedom."),
             ("ene-01", 2, G("Ford supports promoting rooftop solar and sued to recover $155 million in federal solar funding"), None),
             ("ene-06", 1, G("Ford joined the lawsuit against the EPA's repeal of the greenhouse gas endangerment finding (2026)"), None),
             ("cri-02", 2, G("Ford sponsored the 2017 law requiring police to wear body cameras"), None),
             ("cri-03", 1, G("Ford supported 2021 laws letting the attorney general investigate civil rights complaints against police"), None),
             ("edu-06", -2, G("Ford opposes using public funds for private schools and opposed vouchers as a state senator"), None),
             ("ene-04", 2, G("Ford urged the EPA to keep mercury limits and sued over vehicle emission rules"), None),
             ("hea-02", 2, G("Ford would cap many prescription drug prices at the Medicare-negotiated rate"), None),
             ("hea-03", 1, G("Ford sued over the new federal Medicaid work requirements (2026)"), None),
             ("imm-08", -1, G("Ford sued over federal conditions forcing states to help immigration enforcement"), None),
             ("eco-09", 2, G("Ford would repeal Nevada's right-to-work law"), None),
             ("soc-12", 2, G("Ford pledged every legal tool for LGBTQIA+ rights (Human Rights Campaign)"), None),
             ("soc-02", 2, G("Ford filed a 2019 brief to protect LGBTQ employees from discrimination"), None),
             ("gov-05", -2, G("Ford opposes voter ID"), None),
             ("gov-06", 2, G("Ford sued over the executive order restricting mail ballots and voted for automatic voter registration (2017)"), None))},
        {"id": "NV-GOV:lombardo", "name": "Joe Lombardo", "party": "R",
         "bio": "Governor of Nevada since 2023 and former Clark County sheriff.",
         "officialSite": "https://www.joelombardofornv.com/",
         "positions": P(
             ("soc-03", 0, G("Lombardo calls himself pro-life with exceptions but signed protections for out-of-state abortion seekers (SB 98, 2023)"), "pro-life with exceptions"),
             ("soc-04", 1, G("Lombardo supports a 15-week limit, while saying abortion is up to Nevada voters"), None),
             ("ene-06", -1, G("Lombardo withdrew Nevada from the U.S. Climate Alliance"), None),
             ("ene-10", 2, G("Lombardo revised Nevada's climate plan to put energy affordability ahead of emissions goals"), None),
             ("ene-05", 1, G("Lombardo signed incentives for zero-emission trucks (AB 184, 2023)"), None),
             ("cri-06", -1, G("Lombardo supports cash bail"), None),
             ("edu-06", 2, G("Lombardo opted Nevada into the federal private school tax credit program and proposed expanding vouchers"), None),
             ("hea-03", 1, G("Lombardo urged Congress not to cut Medicaid"), None),
             ("eco-11", -1, G("Lombardo vetoed a bill expanding paid family and medical leave (2025)"), None),
             ("sta-09", 1, G("Lombardo sought $60 million for health care in underserved areas (2025)"), None),
             ("imm-08", 2, G("Lombardo called for the $70 billion DHS and ICE bill and pledged state help with deportations"), None),
             ("eco-09", -1, G("Lombardo supports Nevada's right-to-work law"), None),
             ("soc-12", 0, G("Lombardo signed transgender protections in 2023, vetoed others in 2025, and opposes transgender athletes in women's sports"), None),
             ("soc-11", -1, G("Lombardo vetoed a bill protecting doctors who provide gender-affirming care (2025)"), None),
             ("gov-05", 2, G("Lombardo on voter ID"), "essential for ensuring election integrity"),
             ("gov-06", -1, G("Lombardo opposes more ballot drop boxes and wants mail ballots by request"), None))},
    ],
}

write("data/research/NV.json", [governor], "Nevada governor race, researched Oct. 25, 2026.", updated=READ)
