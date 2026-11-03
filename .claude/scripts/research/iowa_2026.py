"""Researched positions for Iowa's statewide races: U.S. Senate (Hinson vs. Turek)
and governor (Sand vs. Lahn). Writes data/research/IA.json.

Positions come from guides.vote's nonpartisan Iowa guides, which tie each stance
to a vote, bill or statement (read Oct. 25, 2026). Hinson's recorded House votes
are added automatically by update_races.py. Researched Oct. 25, 2026.

    py scripts/research/iowa_2026.py
"""

from common import P, guide, write

READ = "2026-10-25"
S = guide("2026 Iowa U.S. Senate voters guide", "https://guides.vote/guide/2026-iowa-us-senate-voters-guide/", READ)
G = guide("2026 Iowa governor voters guide", "https://guides.vote/guide/2026-iowa-governor-voters-guide/", READ)

senate = {
    "id": "IA-SEN",
    "candidates": [
        {"id": "IA-SEN:turek", "name": "Josh Turek", "party": "D",
         "bio": "Iowa state representative and two-time Paralympic gold medalist in wheelchair basketball.",
         "officialSite": "https://turek4iowa.com/",
         "positions": P(
             ("soc-03", 2, S("Turek introduced a bill to repeal Iowa's six-week abortion ban (HF 2455)"), None),
             ("soc-04", -2, S("Turek introduced a bill to repeal Iowa's six-week abortion ban (HF 2455)"), None),
             ("ene-01", 2, S("Turek supports restoring the expired wind and solar production tax credits"), None),
             ("cri-04", 1, S("Turek voted for Iowa's three-strikes bill, with 20-year sentences for repeat serious offenders (HF 2542)"), None),
             ("cri-05", 1, S("Turek calls for more recidivism programs"), None),
             ("eco-04", 2, S("Turek would crack down on agribusiness and meatpacking monopolies"), None),
             ("hou-04", 1, S("Turek would simplify permitting for affordable housing"), None),
             ("edu-06", -2, S("Turek would end school vouchers"), "end school vouchers that waste taxpayer dollars"),
             ("edu-01", 2, S("Turek would increase public school funding"), None),
             ("ene-04", 2, S("Turek would crack down on chemical companies polluting water"), "cracking down on chemical companies that pollute our water supply"),
             ("hea-03", 2, S("Turek would restore Medicaid funding"), None),
             ("hea-07", 2, S("Turek would restore ACA subsidies"), None),
             ("hea-01", 1, S("Turek calls for a public option"), "Healthcare is a human right."),
             ("hea-06", 1, S("Turek would invest in mental health care"), None),
             ("imm-01", 1, S("Turek would pass a bill that strengthens the border"), None),
             ("imm-02", 2, S("Turek supports an earned pathway to citizenship"), None),
             ("imm-07", 1, S("Turek supports deporting people here illegally who commit crimes"), None),
             ("imm-08", -1, S("Turek would not fund DHS without major ICE reform"), "without significant ICE reform"),
             ("def-04", 2, S("Turek says an Iran attack should need congressional approval"), "should not happen without Congressional approval"),
             ("def-15", -1, S("Turek says the Iran war has no clear objective"), None),
             ("eco-09", 2, S("Turek supports the PRO Act"), None),
             ("soc-10", 2, S("Turek sponsored a bill to put same-sex marriage in Iowa law (HF 671)"), None),
             ("soc-02", 1, S("Turek voted against ending state civil rights protections for transgender people (SF 418)"), None),
             ("eco-03", 2, S("Turek would raise the minimum wage and index it to inflation"), None),
             ("eco-01", 2, S("Turek would close tax loopholes for billionaires and big corporations"), "loopholes for billionaires and big corporations"),
             ("gov-06", 1, S("Turek proposed making Election Day a state holiday (HF 407)"), None))},
        {"id": "IA-SEN:hinson", "name": "Ashley Hinson", "party": "R",
         "bio": "U.S. representative for Iowa's 2nd District since 2021 and a former local TV news anchor.",
         "officialSite": "https://ashleyhinson.com/",
         "positions": P(
             ("soc-04", 2, S("Hinson sponsored the Life at Conception Act (H.R. 722)"), "We must protect the unborn."),
             ("soc-03", -2, S("Hinson supports overturning Roe v. Wade and opposes taxpayer-funded abortion"), None),
             ("ene-01", -1, S("Hinson voted to end Biden-era clean energy tax credits (House roll call 190, 2025)"), None),
             ("eco-07", 1, S("Hinson supports cutting wasteful spending"), None),
             ("edu-06", 2, S("Hinson sponsored federal tax credits for private school scholarships (H.R. 833)"), None),
             ("ene-04", -2, S("Hinson voted to narrow the Clean Water Act and repeal an EPA air pollutant rule (2025)"), None),
             ("ene-08", 1, S("Hinson introduced a flood and drought mitigation bill (H.R. 4134)"), None),
             ("hea-07", -1, S("Hinson voted against extending ACA subsidies for 3 years (House roll call 11, 2026)"), None),
             ("hea-08", 1, S("Hinson says she would protect people with pre-existing conditions"), None),
             ("hea-06", 1, S("Hinson voted to reauthorize substance use and mental health programs (H.R. 2483)"), None),
             ("imm-08", 2, S("Hinson voted for $75 billion more for ICE and $70 billion more for DHS"), None),
             ("imm-07", 2, S("Hinson on immigration"), "deporting…criminal illegal immigrants"),
             ("imm-02", -1, S("Hinson voted in 2021 against a path to permanent residency for Dreamers (H.R. 6)"), None),
             ("def-15", 2, S("Hinson backed the military action against Iran"), "Iran cannot have a nuclear weapon."),
             ("def-04", -2, S("Hinson voted five times in 2026 against requiring congressional authorization for military action in Iran"), None),
             ("eco-09", -2, S("Hinson voted against the PRO Act (2021)"), None),
             ("soc-12", -1, S("Hinson voted to ban transgender students from girls' sports (H.R. 28, 2025)"), None),
             ("soc-02", -1, S("Hinson voted against the Equality Act (H.R. 5, 2021)"), None),
             ("eco-03", -2, S("Hinson opposed a $15 federal minimum wage (2021)"), "This would crush our rural economy"),
             ("eco-01", -2, S("Hinson voted to extend the 2017 tax cuts and against raising taxes on corporations and the wealthy (2021)"), None),
             ("gov-05", 2, S("Hinson sponsored the proof-of-citizenship voting bill (H.R. 22)"), "It should be easy to vote and hard to cheat."),
             ("cri-01", 1, S("Hinson on police"), "I will always back the blue."))},
    ],
}

governor = {
    "id": "IA-GOV",
    # Wikipedia still lists independent Sondra Wilson; she and the Libertarian ticket
    # were kept off the ballot, so the researched list is the ballot.
    "candidatesOnly": True,
    "notes": [
        {"text": "Only Sand and Lahn are on the ballot. A judge ruled on Aug. 27 that the Libertarian Party did not correctly replace its lieutenant governor nominee, which keeps Nicholas Gluba’s ticket off.",
         "source": "KCRG / Iowa Capital Dispatch, Aug. 27, 2026", "url": "https://www.kcrg.com/2026/08/28/judge-rules-iowa-libertarians-did-not-correctly-replace-3rd-district-lieutenant-governor-candidates/"},
        {"text": "Independent Sondra Wilson, still listed by Wikipedia, says on her campaign site that she was kept off the ballot.",
         "source": "Sondra Wilson campaign site", "url": "https://wildwillpower.org/"}],
    "candidates": [
        {"id": "IA-GOV:sand", "name": "Rob Sand", "party": "D",
         "bio": "Iowa state auditor since 2019.",
         "officialSite": "https://robsand.com/",
         "positions": P(
             ("soc-03", 2, G("Sand would protect reproductive rights and opposes Iowa's six-week ban"), "use whatever tools I have to protect Iowans' reproductive rights"),
             ("soc-04", -2, G("Sand would veto bills further restricting abortion (The Gazette)"), None),
             ("edu-06", -2, G("Sand calls the voucher program waste"), "open invitation to waste, fraud, and abuse"),
             ("ene-04", 2, G("Sand would expand water quality monitoring"), "No immunity for chemical companies sickening Iowans."),
             ("hea-06", 1, G("Sand would seek more competitive mental health and Medicaid rates"), None),
             ("imm-03", 1, G("Sand calls himself a big supporter of legal immigration"), None),
             ("imm-01", 1, G("Sand says the Biden administration should have done better on border security"), None),
             ("eco-09", 1, G("Sand has joined workers on picket lines"), None),
             ("soc-02", 1, G("Sand opposed repealing Iowa's civil rights protections for transgender people"), "Legalizing discrimination is wrong."),
             ("soc-12", 0, G("Sand opposes repealing transgender civil rights protections but supports the ban on transgender athletes in women's sports"), None),
             ("soc-05", 2, G("Sand supports legalizing adult-use cannabis"), None),
             ("sta-03", 2, G("Sand supports raising the minimum wage"), None),
             ("sta-10", -1, G("Sand on data centers"), "We should not be giving tax incentives to data centers."))},
        {"id": "IA-GOV:lahn", "name": "Zach Lahn", "party": "R",
         "bio": "Businessman who co-founded a private school in Wichita; won the June Republican primary over a Trump-backed opponent.",
         "officialSite": "https://www.zachlahn.com/",
         "positions": P(
             ("soc-04", 2, G("Lahn calls Iowa's six-week ban good and would likely support further protections"), None),
             ("soc-03", -2, G("Lahn calls himself pro-life at conception and opposes abortion pills by mail"), "Every life is a gift from God."),
             ("edu-06", 2, G("Lahn would expand Iowa's Education Savings Accounts"), "foundational to freedom"),
             ("eco-04", 1, G("Lahn would take on big agricultural cartels and bring antitrust suits in health care"), None),
             ("ene-04", 1, G("Lahn would veto any bill giving agricultural chemical companies lawsuit immunity"), None),
             ("hea-03", -1, G("Lahn opposed Medicaid expansion in Montana (2015)"), None),
             ("imm-03", -1, G("Lahn supports barring H-1B visa holders from state government and university jobs"), None),
             ("eco-09", -2, G("Lahn supports right-to-work laws"), None),
             ("sta-04", 1, G("Lahn would lower Iowans' property taxes by raising rates on Wall Street investors"), None),
             ("eco-02", 1, G("Lahn supports eliminating income taxes"), None))},
    ],
}

write("data/research/IA.json", [senate, governor], "Iowa U.S. Senate and governor races, researched Oct. 25, 2026.", updated=READ)
