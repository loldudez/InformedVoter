"""Researched positions for New Mexico's governor race (Haaland vs. Hull).
Writes data/research/NM.json.

Positions come from the candidates' August forum (Albuquerque Journal) and the
October KOB-TV debate, which Haaland skipped (Source NM). Researched
Oct. 25, 2026.

    py scripts/research/new_mexico_2026.py
"""

from common import P, article, write

READ = "2026-10-25"
FORUM = article("Albuquerque Journal forum report, Aug. 25, 2026", "https://www.abqjournal.com/news/gubernatorial-candidates-stake-out-competing-policy-positions-during-congenial-forum/3109160", "2026-08-25")
SOURCE_NM = article("Source NM, Oct. 9, 2026", "https://sourcenm.com/2026/10/09/new-mexico-gop-gubernatorial-nominee-hull-takes-debate-stage-solo-as-haaland-opts-to-see-farmers/", "2026-10-09")

governor = {
    "id": "NM-GOV",
    "candidates": [
        {"id": "NM-GOV:haaland", "name": "Deb Haaland", "party": "D",
         "bio": "U.S. secretary of the interior from 2021 to 2025 and earlier U.S. representative for New Mexico's 1st District.",
         "positions": P(
             ("sta-03", 2, SOURCE_NM("Haaland's affordability agenda would raise the state minimum wage"), None),
             ("hou-01", 1, FORUM("Haaland would explore building affordable housing on state trust land, possibly paid for from the permanent funds"), None),
             ("ene-01", 1, FORUM("Haaland supports developing geothermal power and expanding other renewable energy"), None),
             ("cri-08", 1, SOURCE_NM("Haaland would invest in sending behavioral health professionals to mental health 911 calls"), None))},
        {"id": "NM-GOV:hull", "name": "Gregg Hull", "party": "R",
         "bio": "Former mayor of Rio Rancho.",
         "positions": P(
             ("eco-02", 2, SOURCE_NM("Hull would phase out the state personal income tax in four steps, starting with lower and middle earners"), None),
             ("cri-06", -1, SOURCE_NM("Hull would seek a constitutional amendment letting judges hold violent defendants in jail before trial"), None))},
    ],
    "notes": [{"text": "Haaland skipped the only scheduled debate and both candidates have published few detailed positions, so most questions are unclear for them.", "source": "Source NM", "url": "https://sourcenm.com/2026/10/09/new-mexico-gop-gubernatorial-nominee-hull-takes-debate-stage-solo-as-haaland-opts-to-see-farmers/"}],
}

write("data/research/NM.json", [governor], "New Mexico governor race, researched Oct. 25, 2026.", updated=READ)
