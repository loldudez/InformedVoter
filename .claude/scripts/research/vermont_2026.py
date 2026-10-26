"""Researched positions for Vermont's governor race (Scott vs. Janoo).
Writes data/research/VT.json.

Gov. Scott's positions come from bills he signed or vetoed; Janoo, a first-time
candidate, from campaign and debate coverage. Researched Oct. 25, 2026.

    py scripts/research/vermont_2026.py
"""

from common import P, article, write

READ = "2026-10-25"
VTD_2019 = article("VTDigger, June 10, 2019", "https://vtdigger.org/2019/06/10/scott-vetoes-24-hour-handgun-waiting-period-bill/", "2019-06-10")
VPR_2018 = article("Vermont Public, May 22, 2018", "https://www.vermontpublic.org/post/heres-what-gov-phil-scotts-vetoed-so-far", "2018-05-22")
VETO_2026 = article("Office of Gov. Phil Scott, June 17, 2026", "https://governor.vermont.gov/press-release/action-taken-governor-phil-scott-legislation-june-17-2026", "2026-06-17")
VP_MAR = article("Vermont Public, March 10, 2026", "https://www.vermontpublic.org/local-news/2026-03-10/republican-gov-phil-scott-democratic-challenge-2026", "2026-03-10")
VTD_MAR = article("VTDigger, March 10, 2026", "https://vtdigger.org/2026/03/10/first-democratic-challenger-to-phil-scott-enters-governors-race/", "2026-03-10")
WCAX_DEBATE = article("WCAX primary debate report, July 28, 2026", "https://www.wcax.com/2026/07/28/watch-live-democrats-vermont-governor-debate/", "2026-07-28")
WCAX_SCHOOLS = article("WCAX, Oct. 8, 2026", "https://www.wcax.com/2026/10/08/campaign-countdown-scott-janoo-offer-sharply-different-visions-vermont-education-reform/", "2026-10-08")

governor = {
    "id": "VT-GOV",
    "candidates": [
        {"id": "VT-GOV:scott", "name": "Phil Scott", "party": "R",
         "bio": "Governor of Vermont since 2017 and a former lieutenant governor.",
         "positions": P(
             ("soc-03", 2, VTD_2019("Scott signed H.57 (2019), protecting abortion rights at every stage of pregnancy"), "I have consistently supported a woman's right to choose."),
             ("soc-04", -2, VTD_2019("Scott signed H.57 (2019), barring government interference in abortion decisions"), None),
             ("sta-03", -1, VPR_2018("Scott vetoed a $15 minimum wage (S.40, 2018), preferring increases tied to inflation"), "more likely to harm those it intends to help"),
             ("eco-11", 0, VPR_2018("Scott vetoed a mandatory paid family leave program (H.196, 2018), preferring a voluntary state-run one"), None),
             ("ene-01", -1, VETO_2026("Scott vetoed H.710 (2026), saying it would let industrial wind sites expand with less local scrutiny"), None))},
        {"id": "VT-GOV:janoo", "name": "Amanda Janoo", "party": "D",
         "bio": "Economist and founder of the Wellbeing Economy Alliance of Vermont, running for statewide office for the first time.",
         "positions": P(
             ("hea-01", 2, VP_MAR("Janoo's free primary care plan would lay groundwork for a universal health care system"), "ensure free health care for all"),
             ("hea-09", 2, VTD_MAR("Janoo proposes free primary and preventive health care"), None),
             ("hou-01", 1, VP_MAR("Janoo would broaden the availability of affordable housing"), None),
             ("eco-01", 2, WCAX_SCHOOLS("Janoo proposes taxing Vermont's highest earners to cut health care and school costs"), None),
             ("cri-07", 1, WCAX_DEBATE("Janoo would address the roots of repeat offending with a community-first approach"), "the safest communities are the ones where people know their neighbors"),
             ("sta-02", 1, WCAX_SCHOOLS("Janoo would keep small schools open and invest in them, opposing forced mergers"), None))},
    ],
    "notes": [{"text": "Janoo is a first-time candidate with few published positions, and Scott has not released a platform beyond affordability and school consolidation, so many questions are unclear for both.", "source": "WCAX", "url": "https://www.wcax.com/2026/09/17/campaign-countdown-candidates-vermont-governor/"}],
}

write("data/research/VT.json", [governor], "Vermont governor race, researched Oct. 25, 2026.", updated=READ)
