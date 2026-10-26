"""Researched positions for Oregon's governor race (Kotek vs. Drazan).
Writes data/research/OR.json.

Positions come from guides.vote's nonpartisan Oregon guide, which ties each
stance to a vote, bill or statement (read Oct. 25, 2026). Researched Oct. 25, 2026.

    py scripts/research/oregon_2026.py
"""

from common import P, guide, write

READ = "2026-10-25"
G = guide("2026 Oregon governor voters guide", "https://guides.vote/guide/2026-oregon-governor-voters-guide/", READ)

governor = {
    "id": "OR-GOV",
    "candidates": [
        {"id": "OR-GOV:kotek", "name": "Tina Kotek", "party": "D",
         "bio": "Governor of Oregon since 2023 and a former speaker of the Oregon House.",
         "officialSite": "https://www.tinafororegon.com/",
         "positions": P(
             ("soc-03", 2, G("Kotek signed HB 4088 protecting abortion seekers and providers and HB 4127 funding Planned Parenthood (2026)"), "protect Oregonians from federal attempts to restrict access to abortion"),
             ("soc-04", -2, G("Kotek opposed overturning Roe v. Wade"), None),
             ("ene-06", 2, G("Kotek is fully supportive of Oregon's Climate Protection Program, which caps emissions"), None),
             ("ene-08", 1, G("Kotek signed the Climate Resilience Investment Act"), None),
             ("ene-04", 1, G("Kotek pledges clean air and water and backed restoring salmon protections"), None),
             ("sta-08", 1, G("Kotek directed the state to expand and speed up police training"), None),
             ("cri-08", 1, G("Kotek signed HB 4002 (2024), recriminalizing small-amount drug possession while allowing deflection into treatment"), None),
             ("edu-06", -2, G("Kotek opposes public money for private schools and opted Oregon out of the federal scholarship tax credit (2026)"), None),
             ("hea-01", 2, G("Kotek supported the 2022 measure creating a state constitutional right to affordable health care"), None),
             ("hea-03", 1, G("Kotek signed HB 2010 (2025), extending the taxes that fund Oregon's Medicaid program"), None),
             ("hea-02", 1, G("Kotek would team up with other states to lower prescription drug costs"), None),
             ("imm-08", -2, G("Kotek defended Oregon's sanctuary law and signed eight bills in 2026 protecting immigrants from federal enforcement"), "Oregon is not staying quiet."),
             ("eco-09", 2, G("Kotek signed unemployment benefits for striking workers (SB 916, 2025) and required project labor agreements on state construction"), "I'm proud to stand with working people."),
             ("soc-11", 1, G("Kotek signed HB 4088, protecting providers of gender-affirming care (2026)"), None),
             ("soc-12", 2, G("Kotek opposed the Supreme Court ruling letting states bar transgender athletes from girls' sports"), "our LGBTQ+ community from federal attacks"),
             ("sta-03", 1, G("Kotek voted in 2016 to raise Oregon's minimum wage in steps through 2022 (SB 1532)"), "All workers deserve fair, living wages."),
             ("gov-06", 2, G("Kotek would safeguard vote-by-mail and opposes federal limits on mail voting"), "It's safe, it's secure, and it works."))},
        {"id": "OR-GOV:drazan", "name": "Christine Drazan", "party": "R",
         "bio": "Oregon state representative, a former House Republican leader and the 2022 Republican nominee for governor.",
         "officialSite": "https://christinefororegon.com/",
         "positions": P(
             ("soc-03", -1, G("Drazan calls herself pro-life and said in 2022 she would veto bills expanding abortion rights"), None),
             ("soc-04", 0, G("Drazan calls Oregon's abortion law an outlier but does not support a ban"), "I do not support banning abortion."),
             ("ene-06", -2, G("Drazan would rescind Oregon's Climate Protection Program on her first day"), None),
             ("ene-04", -1, G("Drazan voted against banning the pesticide chlorpyrifos (2020)"), None),
             ("cri-01", 2, G("Drazan on public safety"), "We need fewer needles and more cops to restore safe communities."),
             ("sta-08", 2, G("Drazan on public safety"), "We need fewer needles and more cops to restore safe communities."),
             ("edu-06", 2, G("Drazan supports opting Oregon into the federal private school tax credit and would expand school choice"), "We urgently need more options for students and their families to succeed."),
             ("hea-01", -1, G("Drazan opposed the 2022 measure creating a state constitutional right to affordable health care"), None),
             ("hea-03", -1, G("Drazan voted against HB 2010 (2025), which extended the taxes that fund Oregon's Medicaid program"), None),
             ("hea-02", -1, G("Drazan voted against creating a Prescription Drug Affordability Board (SB 844, 2021)"), None),
             ("imm-07", 2, G("Drazan sponsored HB 3551, letting state police work with federal agencies to locate immigrants convicted of certain crimes"), None),
             ("imm-08", 1, G("Drazan calls Oregon's sanctuary status off the rails and backed the 2025 federal troop deployment to Portland"), None),
             ("eco-09", -2, G("Drazan voted against unemployment benefits for striking workers (SB 916, 2025) and against easing union organizing (HB 2016, 2019)"), None),
             ("soc-12", -2, G("Drazan sponsored HB 3740, barring transgender athletes from girls' school sports"), "No more boys in girls' sports."),
             ("eco-02", 2, G("Drazan supports bold tax cuts for families and businesses and more child care tax credits"), None),
             ("eco-01", -1, G("Drazan would eliminate Oregon's estate tax"), None),
             ("gov-05", 2, G("Drazan introduced HB 3872, requiring photo ID to vote or request a ballot (2025)"), None),
             ("gov-06", -1, G("Drazan introduced HB 3872 to replace vote-by-mail with in-person voting, though she says she has always supported vote by mail"), None))},
    ],
}

write("data/research/OR.json", [governor], "Oregon governor race, researched Oct. 25, 2026.", updated=READ)
