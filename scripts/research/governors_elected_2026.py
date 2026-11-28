"""More positions for seven governors elected in 2026 whose race research left them
with fewer than ten: Sanders (Arkansas), Scott (Vermont), Mazzei (Oklahoma), Shapiro
(Pennsylvania), Pritzker (Illinois), Weiser (Colorado) and Foulkes (Rhode Island).
Writes data/research/governors-elected.json, which update_races.py pools with the other
research by question. Researched Nov. 28, 2026.

Sources are their own words and acts: State of the State, inaugural and budget
addresses (the governors' offices' texts, or a newsroom's copy of the text), the
newsroom voter guides' questionnaire answers, Mazzei's plan, and news reports of bills
they signed or acts of their office. Quotes are verbatim, at most 25 words, and were
checked against the page text; a news report or a newsroom's summary of a platform has
no quote, or quotes only the candidate's own words that it prints. Only questions the
other research leaves open are answered here, so nothing already on the site changes.
Each race is `partial` (only its winner is covered here); the other files keep it
researched.

    py scripts/research/governors_elected_2026.py            # write the file
    py scripts/research/governors_elected_2026.py --quotes   # {url: [quotes]}, for checking
"""

import json
import sys

from common import P, article, page, write

READ = "2026-11-28"

# Arkansas: Sarah Huckabee Sanders
AR_SOTS = article("Office of Gov. Sarah Huckabee Sanders, 2025 State of the State Address, Jan. 14, 2025",
                  "https://governor.arkansas.gov/news_post/governor-sanders-delivers-state-of-the-state-address-2/", "2025-01-14")
AR_AP_NITROGEN = article("Associated Press (via UA Little Rock Public Radio), Apr. 21, 2025",
                         "https://www.ualrpublicradio.org/local-regional-news/2025-04-21/arkansas-governor-says-shes-not-rushing-to-resume-executions-after-signing-nitrogen-gas-bill", "2025-04-21")
AR_AP_CARE = article("Associated Press (via PBS News), Mar. 14, 2023",
                     "https://www.pbs.org/newshour/politics/sanders-signs-arkansas-gender-affirming-care-malpractice-bill-into-law", "2023-03-14")

# Vermont: Phil Scott
VT_INAUG = article("Office of Gov. Phil Scott, 2025 inaugural address, Jan. 9, 2025",
                   "https://governor.vermont.gov/press-release/transcript-governor-phil-scott-delivers-2025-inaugural-address", "2025-01-09")
VT_MAIL = article("VTDigger, June 7, 2021", "https://vtdigger.org/2021/06/07/scott-signs-bill-expanding-vote-by-mail-in-general-elections/", "2021-06-07")

# Oklahoma: Mike Mazzei (his campaign site became his transition website after the election)
OK_PLAN = lambda note: page(f"Mike Mazzei transition website (his campaign site until the election), The Plan: {note}",  # noqa: E731
                            "https://mikeforok.com/the-plan/", READ)

# Pennsylvania: Josh Shapiro
PA_BUDGET26 = article("Office of Gov. Josh Shapiro, 2026-27 budget address, Feb. 3, 2026",
                      "https://www.pa.gov/governor/newsroom/2026-press-releases/governor-shapiro-s-2026-27-budget-address-as-prepared-for-delive", "2026-02-03")
PA_BUDGET25 = article("Office of Gov. Josh Shapiro, 2025-26 budget address, Feb. 4, 2025",
                      "https://www.pa.gov/governor/newsroom/2025-press-releases/governor-shapiro-2025-26-budget-address-as-prepared", "2025-02-04")

# Illinois: JB Pritzker (the addresses' text as NPR Illinois published it)
IL_SOTS26 = article("Gov. JB Pritzker’s 2026 State of the State and budget address (text published by NPR Illinois), Feb. 18, 2026",
                    "https://www.nprillinois.org/government-politics/2026-02-18/read-gov-pritzkers-state-of-the-state-and-budget-address", "2026-02-18")
IL_SOTS25 = article("Gov. JB Pritzker’s 2025 State of the State and budget address (text published by NPR Illinois), Feb. 19, 2025",
                    "https://www.nprillinois.org/government-politics/2025-02-19/read-gov-pritzkers-budget-address", "2025-02-19")

# Rhode Island: Helena Foulkes
RI_GUIDE = lambda note: page(f"Rhode Island Current voter guide (candidates’ answers to the newsroom’s questionnaire): {note}",  # noqa: E731
                             "https://rhodeislandcurrent.com/voter-guides/contests/2026-general-governor/", READ)

# Colorado: Phil Weiser (the guide summarizes each platform: it is cited, and only his own
# words that it quotes are quoted)
CO_GUIDE = lambda note: page(f"Colorado Newsline voter guide (the newsroom’s summary of each platform): {note}",  # noqa: E731
                             "https://coloradonewsline.com/voter-guides/contests/2026-general-colorado-governor/", READ)
CO_SUN = article("The Colorado Sun, Nov. 16, 2021", "https://coloradosun.com/2021/11/16/aurora-police-use-force-consent-decree-elijah-mcclain/", "2021-11-16")


def cand(cid, name, *rows):
    return {"id": cid, "name": name, "positions": P(*rows)}


races = [
    {"id": "AR-GOV", "partial": True, "candidates": [cand(
        "AR-GOV:sanders", "Sarah Huckabee Sanders",
        ("eco-12", -1, AR_SOTS("Sanders signed three income tax cuts, lowering the personal income tax rate by a full point"),
         "cut taxes not once, not twice, but three times, lowering our personal income tax rate by a full percentage point"),
        ("eco-01", -1, AR_AP_NITROGEN("Sanders has called for eliminating the state income tax"), None),
        ("eco-07", 1, AR_SOTS("Sanders says her budget holds down spending increases"),
         "The budget I introduced for this year controls spending increases while still making needed investments"),
        ("edu-09", 1, AR_SOTS("Sanders would use medical marijuana revenue to make school breakfast free for every student"),
         "We will also use those funds to make school breakfast in Arkansas completely free."),
        ("edu-03", 1, AR_SOTS("Sanders's Arkansas ACCESS plan would extend scholarships to associate's degrees and non-degree credentials"),
         "expanding scholarships to associate’s degrees and non-degree credentials"),
        ("sta-07", 1, AR_SOTS("Sanders would fund colleges for associate's degrees and non-degree credentials, not only bachelor's degrees"),
         "puts state dollars behind all types of degrees: bachelor’s, associate’s, and non-degree credentials"),
        ("sta-08", 2, AR_SOTS("Sanders points to more state troopers than in a generation and a raise of nearly 20% in their starting pay"),
         "through our new state pay plan, will raise their starting pay by nearly 20%"),
        ("cri-05", 2, AR_SOTS("Sanders would expand and require evidence-based programs in every prison"),
         "We will expand and require evidence-based programming in our prisons"),
        ("imm-07", 2, AR_SOTS("Sanders backed the Defense Against Criminal Illegals Act, with tougher penalties and removal for violent offenders"),
         "pass the Defense Against Criminal Illegals Act to slap enhanced penalties on violent illegal immigrants and remove them from our state"),
        ("cri-09", 1, AR_AP_NITROGEN("Sanders signed a 2025 law allowing executions by nitrogen gas, though she says she is in no hurry to resume them"), None),
        ("soc-11", -2, AR_AP_CARE("Sanders signed a 2023 law letting anyone given gender-affirming care as a minor sue the doctor until 15 years after turning 18, which legal experts said could end that care"), None))]},
    {"id": "VT-GOV", "partial": True, "candidates": [cand(
        "VT-GOV:scott", "Phil Scott",
        ("hou-04", 2, VT_INAUG("Scott calls for regulatory changes to build more housing, including wider Act 250 exemptions"),
         "pushing for regulatory changes to legalize housing"),
        ("eco-07", 1, VT_INAUG("Scott says spending more hasn't fixed the state's problems"),
         "As I’ve said before, just throwing more money at problems hasn’t equaled success."),
        ("sta-02", -1, VT_INAUG("Scott says school spending has grown too fast and wants costs under control"),
         "Since I took office, the Education Fund has gone from $1.6 billion to an astounding $2.3 billion and climbing."),
        ("edu-01", -1, VT_INAUG("Scott says Vermont already spends more than most states on schools and wants costs under control"),
         "We’re one of the top education spenders in the nation."),
        ("edu-04", 1, VT_INAUG("Scott says teachers in many districts are underpaid"),
         "Yet in too many districts, teachers aren’t paid enough"),
        ("sta-04", 1, VT_INAUG("Scott's budget would offset this year's school property tax increase if school boards hold spending to the projected level"),
         "my budget will lower the impact of this year’s increase with a goal to eliminate it"),
        ("imm-06", 1, VT_INAUG("Scott says Vermont will keep resettling refugees"),
         "We’ve welcomed over 1,000 refugees in the last three years, and we’ll continue to do our part."),
        ("hou-07", 1, VT_INAUG("Scott counts restored train service from Burlington to New York City among his administration's results"),
         "We brought train service from Burlington to New York City after two decades of waiting."),
        ("hou-09", 1, VT_INAUG("Scott counts broadband improvements paid for with federal aid among his administration's results"),
         "improved broadband for over 100,000 households and businesses"),
        ("ene-10", 1, VT_INAUG("Scott wants climate policy that is affordable"),
         "support climate policy that’s achievable and affordable"),
        ("ene-08", 1, VT_INAUG("Scott wants infrastructure for housing and flood recovery"),
         "let’s strengthen our foundation with infrastructure for housing and flood recovery"),
        ("gov-06", 2, VT_MAIL("Scott signed S.15 (2021), mailing a ballot to every registered voter for general elections, and wanted it extended to primaries and local votes"),
         "I’m signing this bill because I believe making sure voting is easy and accessible, and increasing voter participation is important"))]},
    {"id": "OK-GOV", "partial": True, "candidates": [cand(
        "OK-GOV:mazzei", "Mike Mazzei",
        ("eco-01", -2, OK_PLAN("More High-Paying Jobs"), "Make Oklahoma a No-Income-Tax State"),
        ("eco-12", -1, OK_PLAN("Eliminating Property Tax for Seniors and Veterans"),
         "Taxing activity instead of ownership or income does much less harm to economic growth."),
        ("eco-07", 1, OK_PLAN("More High-Paying Jobs"), "Cut unnecessary government programs and restrain spending"),
        ("edu-03", 2, OK_PLAN("More High-Paying Jobs"), "Expand apprenticeships, trade pathways, and career tech programs"),
        ("sta-07", 2, OK_PLAN("Education That Works"), "Expand career and technical education pathways"),
        ("edu-07", 1, OK_PLAN("Education That Works"), "Restore parental transparency and involvement in education decisions"),
        ("sta-10", 0, OK_PLAN("More High-Paying Jobs: Mazzei would end poor-return corporate incentives and costly megadeals while revamping incentive programs"),
         "Revamp incentive programs to be cost effective for tax payers"),
        ("ene-01", -1, OK_PLAN("Protecting Oklahoma Land"),
         "Prevent the Commissioners of the Land Office from selling Oklahoma land for green energy projects"))]},
    {"id": "PA-GOV", "partial": True, "candidates": [cand(
        "PA-GOV:shapiro", "Josh Shapiro",
        ("sta-03", 2, PA_BUDGET26("Shapiro calls for raising the minimum wage to $15 an hour"),
         "Because raising the minimum wage to $15/hour will save this Commonwealth $300 million a year on entitlement programs like Medicaid."),
        ("soc-05", 2, PA_BUDGET25("Shapiro asked lawmakers to legalize adult-use cannabis and expunge records for small-amount possession"),
         "I ask you to come together and send to my desk a bill that legalizes adult-use cannabis"),
        ("soc-07", 2, PA_BUDGET26("Shapiro created the state's first recruitment and retention grants for child care workers"),
         "More money in the pockets of our child care workers — and more available child care for Pennsylvania families."),
        ("eco-02", 2, PA_BUDGET26("Shapiro points to the Working Pennsylvanians Tax Credit he signed"),
         "And together, we created the Working Pennsylvanians Tax Credit."),
        ("hea-06", 2, PA_BUDGET26("Shapiro funded mental health services in nearly 800 schools"),
         "We’ve funded mental health services in nearly 800 schools — and helped hire more than 200 new mental health counselors for our students."),
        ("hea-07", 1, PA_BUDGET26("Shapiro faults Congress for letting health insurance premiums double"),
         "Nearly 500,000 Pennsylvanians are seeing their health insurance premiums double this year because Congress failed to act."),
        ("hea-03", 1, PA_BUDGET26("Shapiro opposes Medicaid work requirements, preferring higher wages"),
         "Not by adding arbitrary and cumbersome requirements that push people who still need help off the rolls"),
        ("sta-08", 1, PA_BUDGET26("Shapiro would fund four more classes of state troopers"),
         "let’s continue our work together by funding another four classes of PSP troopers"),
        ("cri-07", 2, PA_BUDGET26("Shapiro would increase funding for community violence prevention"),
         "increasing our commitment to violence prevention rooted in our communities"),
        ("hou-04", 2, PA_BUDGET26("Shapiro proposes reforming zoning laws to build more housing"),
         "I am proposing bold new steps to reform our zoning laws, build more housing, and protect renters and homeowners"),
        ("hou-06", 1, PA_BUDGET26("Shapiro would cap rental application fees at the cost of screening"),
         "I’m calling for a statewide cap on rental application fees, limiting them to the actual cost of screening"),
        ("sta-07", 2, PA_BUDGET26("Shapiro points to his expansion of vo-tech, career and technical education and apprenticeships"),
         "We’ve expanded vo-tech, CTE, and apprenticeships to open new pathways of opportunity."),
        ("ene-01", 1, PA_BUDGET26("Shapiro's Lightning Plan would build more generation and more renewables"),
         "diversify our energy sector to generate more renewables"),
        ("sta-10", 1, PA_BUDGET26("Shapiro would offer data center developers tax credits if they meet his standards, including hiring local workers"),
         "If companies adhere to these principles, they will unlock benefits from the Commonwealth, including speed and certainty in permitting and available tax credits."))]},
    {"id": "IL-GOV", "partial": True, "candidates": [cand(
        "IL-GOV:pritzker", "JB Pritzker",
        ("eco-02", 2, IL_SOTS25("Pritzker enacted a state child tax credit and ended the state grocery tax"),
         "Last year, we lowered taxes on parents when we enacted the Child Tax Credit and permanently eliminated the state grocery tax"),
        ("sta-02", 2, IL_SOTS26("Pritzker has put billions more into public schools"),
         "We’ve prioritized school funding, putting billions more into public education to improve the student-teacher ratio and get better outcomes for our children."),
        ("edu-01", 2, IL_SOTS26("Pritzker's budget keeps increasing Evidence-Based Funding for schools"),
         "my budget proposal for this year prioritizes our state commitment to Evidence Based Funding and advances our effort to hire more teachers"),
        ("edu-02", 1, IL_SOTS25("Pritzker points to free-tuition offers at state universities and to state grants"),
         "our state universities’ free college offers like the Huskie Pledge and Illinois Promise are making university education in Illinois more affordable"),
        ("edu-03", 2, IL_SOTS26("Pritzker proposes a Vocational Training Grant Program"),
         "I propose we create our Vocational Training Grant Program"),
        ("sta-07", 2, IL_SOTS26("Pritzker would help districts and regional vocational centers build workforce programs"),
         "provide school districts and regional vocational centers with support to build and expand specialized workforce programs"),
        ("hou-04", 2, IL_SOTS26("Pritzker's BUILD plan would loosen local rules such as parking mandates to build more homes"),
         "an initiative to lower housing costs by making it easier, faster, and more cost-effective to build homes in Illinois"),
        ("hou-01", 1, IL_SOTS26("Pritzker would close financing gaps for housing developments"),
         "We’ll add to that a robust approach to closing financing gaps for developing housing of all kinds"),
        ("ene-02", 1, IL_SOTS26("Pritzker signed the law lifting Illinois's moratorium on new nuclear power"),
         "I signed the Clean and Reliable Grid Affordability Act which lifted a decades-long moratorium on new nuclear power in Illinois"),
        ("imm-08", -2, IL_SOTS26("Pritzker condemns the 2025 federal immigration enforcement surge in Illinois"),
         "Masked, unaccountable federal agents — with little training — occupied our streets, brutalized our people, tear gassed kids and cops"))]},
    {"id": "CO-GOV", "partial": True, "candidates": [cand(
        "CO-GOV:weiser", "Phil Weiser",
        ("hea-01", 1, CO_GUIDE("Weiser promises universal access to checkups and preventive care"), "primary care for all"),
        ("hea-03", 1, CO_GUIDE("Weiser would add groups to the state employee health plan and strengthen the public Colorado Option plan"), None),
        ("soc-03", 2, CO_GUIDE("Weiser would protect Colorado's constitutional right to abortion"),
         "against any attacks on our laws protecting the right to choose"),
        ("soc-04", -2, CO_GUIDE("Weiser would defend Colorado's laws protecting abortion"), None),
        ("ene-01", 2, CO_GUIDE("Weiser supports wind, solar and battery technology on the way to net-zero emissions by 2050"),
         "Colorado must lean in even more and continue to lead the shift to a clean energy future"),
        ("ene-06", 1, CO_GUIDE("Weiser would keep Colorado's emission reduction targets"),
         "achievement of our statewide emission reduction targets"),
        ("ene-05", 1, CO_GUIDE("Weiser supports the gradual electrification of cars, buildings and industry"), None),
        ("gov-12", 1, CO_GUIDE("Weiser calls for audits, performance reviews and procurement reforms"), None),
        ("cri-03", 2, CO_SUN("As attorney general, Weiser's office investigated the Aurora police and reached a consent decree requiring changes in its use of force (2021)"),
         "The ultimate goal of this consent decree is to elevate policing and to improve public safety here in Aurora"))]},
    {"id": "RI-GOV", "partial": True, "candidates": [cand(
        "RI-GOV:foulkes", "Helena Foulkes",
        ("eco-12", 1, RI_GUIDE("Foulkes would pay for 20,000 homes with a tax on millionaires"), "paid for with a millionaire’s tax"),
        ("hea-03", 1, RI_GUIDE("Foulkes would raise Medicaid payment rates and draw more federal money"),
         "We need to raise Medicaid reimbursement rates and stop leaving federal money on the table."),
        ("edu-03", 2, RI_GUIDE("Foulkes proposed $100 million for classroom-to-career programs"),
         "That’s why I proposed a $100 million investment in classroom-to-career programs across Rhode Island."),
        ("ene-10", -1, RI_GUIDE("Foulkes rejects trading climate goals for lower energy bills, saying renewables are cheaper than fossil fuels"),
         "rolling back the state’s climate goals and setting up a false choice between lower energy bills and policies that address climate change"))]},
]


def quotes():
    out = {}
    for r in races:
        for c in r["candidates"]:
            for p in c["positions"].values():
                q = p["source"].get("quote")
                if q:
                    out.setdefault(p["source"]["url"], []).append(q)
    return out


if __name__ == "__main__":
    if "--quotes" in sys.argv[1:]:
        print(json.dumps(quotes(), ensure_ascii=False))
    else:
        write("data/research/governors-elected.json", races,
              "Seven governors elected in 2026 whose race research had fewer than ten positions; researched Nov. 28, 2026.",
              updated=READ)
