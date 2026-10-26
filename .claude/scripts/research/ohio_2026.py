"""Researched details for Ohio's statewide races: the U.S. Senate special election
(Husted vs. Brown) and governor (Ramaswamy vs. Acton). Writes data/research/OH.json.

Positions come from guides.vote's nonpartisan Ohio voters guides, which tie each
stance to a vote, bill, statement or interview (read Oct. 24, 2026). The Senate's
own roll-call pages refuse automated reads, so each vote is cited through the
guide that links it. Researched Oct. 24, 2026.

    py scripts/research/ohio_2026.py
"""

from common import P, TODAY, source, write

SEN_URL = "https://guides.vote/guide/2026-ohio-senate-voters-guide/"
GOV_URL = "https://guides.vote/guide/2026-ohio-governor-voters-guide/"


def S(note):
    return source(f"guides.vote, 2026 Ohio U.S. Senate voters guide: {note}", SEN_URL, TODAY)


def G(note):
    return source(f"guides.vote, 2026 Ohio governor voters guide: {note}", GOV_URL, TODAY)


senate = {
    "id": "OH-SEN",
    "candidates": [
        {"id": "OH-SEN:brown", "name": "Sherrod Brown", "party": "D",
         "bio": "U.S. senator from Ohio from 2007 to 2025; earlier a U.S. representative and Ohio secretary of state.",
         "officialSite": "https://www.sherrodbrown.com/", "donateUrl": "https://secure.actblue.com/donate/sherrod-website",
         "positions": P(
             ("soc-03", 2, S("Brown supports abortion access and voted against abortion restrictions in 2022"), "abortion access for all women"),
             ("soc-04", -2, S("Brown voted against a 20-week abortion ban (Senate roll call 25, 2018)"), None),
             ("ene-01", 1, S("Brown voted for $369 billion in clean energy tax credits (Inflation Reduction Act, Senate roll call 325, 2022)"), None),
             ("ene-06", 0, S("Brown supports action on climate change but opposed the EPA’s 2024 limits on coal plant emissions"), "an unrealistic, unachievable rule"),
             ("ene-04", 1, S("Brown voted to keep limits on air pollution from new heavy-duty vehicles (Senate roll call 98, 2023)"), None),
             ("eco-06", 1, S("Brown voted for the infrastructure law (Senate roll call 314, 2021)"), None),
             ("edu-06", -1, S("Brown said vouchers moved money out of public education into private schools (Ohio Capital Journal, 2022)"), None),
             ("edu-01", 1, S("Brown on public school funding"), "make sure our public schools have the resources they need"),
             ("imm-01", 1, S("Brown wants to strengthen the border and give border agents more resources"), None),
             ("imm-02", 1, S("Brown supported a path to citizenship for DACA recipients (2017)"), None),
             ("cri-01", 1, S("Brown on police funding"), "the resources, training, and support they need"),
             ("hea-02", 2, S("Brown voted to let Medicare negotiate drug prices (Senate roll call 325, 2022) and sponsored a $35 monthly insulin cap"), None),
             ("hea-07", 1, S("Brown supports the Affordable Care Act (Ohio Capital Journal, 2024)"), None),
             ("eco-09", 2, S("Brown sponsored a bill to expand organizing and collective bargaining rights (S. 420)"), None),
             ("soc-10", 2, S("Brown voted for the Respect for Marriage Act (Senate roll call 362, 2022)"), None),
             ("soc-02", 2, S("Brown sponsored a bill banning discrimination based on sex, sexual orientation and gender identity (S. 393)"), None),
             ("eco-03", 2, S("Brown supports raising the minimum wage to $17 an hour"), None),
             ("eco-01", 2, S("Brown voted to raise taxes on corporations and the wealthy (Senate roll call 357, 2021) and opposes tax cuts for the richest"), None),
             ("gov-06", 2, S("Brown voted to expand voting access (Senate roll call 246, 2021)"), "make it easier to vote, not creating unnecessary barriers"),
             ("gov-05", -1, S("Brown called a push for a federal voter ID requirement unnecessary (Journal-News)"), None),
             ("def-15", -2, S("Brown opposes the war with Iran (Ohio Capital Journal, March 2026)"), "country’s safety and security at risk"))},
        {"id": "OH-SEN:husted", "name": "Jon Husted", "party": "R",
         "bio": "Appointed to the U.S. Senate in January 2025 to fill J.D. Vance’s seat; previously Ohio lieutenant governor and secretary of state.",
         "officialSite": "https://www.jonhustedforsenate.com/",
         "positions": P(
             ("soc-03", -2, S("Husted cosponsored S. 186 to bar federal funding of abortion and opposed Ohio’s 2023 abortion-rights amendment"), None),
             ("soc-04", 2, S("Husted supported overturning Roe v. Wade and cosponsored S. 186"), "defending the rights of women, children, and the unborn"),
             ("ene-01", -1, S("Husted voted to end Biden-era clean energy tax credits (H.R. 1, Senate roll call 372, 2025)"), None),
             ("ene-06", -2, S("Husted supports repealing EPA greenhouse gas standards for coal plants"), None),
             ("ene-04", -2, S("Husted voted to undo rules on emissions of seven hazardous air pollutants (Senate roll call 229, 2025)"), None),
             ("cri-01", 2, S("Husted supports funding law enforcement"), "more tools to convict criminals"),
             ("def-01", 1, S("Husted voted to increase defense spending (H.R. 1, Senate roll call 372, 2025)"), None),
             ("def-10", 1, S("Husted voted to cut existing USAID foreign aid and public broadcasting funds (Senate roll call 411, 2025)"), None),
             ("edu-06", 2, S("Husted helped create Ohio’s EdChoice scholarship"), "empowers parents"),
             ("hea-03", -1, S("Husted voted for the 2025 law that cut Medicaid (H.R. 1, Senate roll call 372)"), None),
             ("imm-01", 2, S("Husted on the border"), "securing the border and adding more agents"),
             ("imm-08", 2, S("Husted voted to increase ICE funding by $75 billion (H.R. 1, Senate roll call 372, 2025)"), None),
             ("soc-11", -2, S("Husted supported Ohio’s HB 68, banning gender-affirming care for minors"), None),
             ("soc-12", -1, S("Husted backed Ohio’s parents’ bill of rights (HB 8) and says men should not compete in women’s sports"), None),
             ("eco-03", -1, S("Husted voted against raising the federal minimum wage to $17 by 2030 (Senate roll call 184, 2025)"), None),
             ("eco-01", -2, S("Husted sponsored a bill to repeal the federal estate tax and voted to extend the 2017 tax cuts"), None),
             ("gov-05", 2, S("Husted proposed a photo ID requirement for federal elections"), "Passing voter ID requirements is common sense"),
             ("def-04", -2, S("Husted voted twice in 2026 against requiring congressional authorization for military action in Iran (S.J.Res. 123)"), None),
             ("def-15", 2, S("Husted backed the president’s military action against Iran, calling it decisive"), None))},
    ],
    "notes": [{"text": "A special election: the winner serves the rest of J.D. Vance’s term, through January 2029.", "source": "guides.vote", "url": SEN_URL}],
}

governor = {
    "id": "OH-GOV",
    "candidates": [
        {"id": "OH-GOV:acton", "name": "Amy Acton", "party": "D",
         "bio": "Physician and former director of the Ohio Department of Health, who led the state’s early COVID-19 response.",
         "officialSite": "https://actonforgovernor.com/",
         "positions": P(
             ("soc-03", 2, G("Acton on reproductive rights (actonforgovernor.com)"), "Every Ohioan deserves the right to make their own reproductive health care decisions"),
             ("eco-02", 1, G("Acton proposes a refundable state earned income credit"), None),
             ("sta-04", 1, G("Acton proposes child tax credits and property tax relief (Statehouse News Bureau, April 2026)"), None),
             ("edu-06", -2, G("Acton opposes the voucher program"), "sending billions…of your tax dollars to fund private schools"),
             ("sta-03", 2, G("Acton would raise the minimum wage"), None),
             ("hea-03", 1, G("Acton calls Medicaid a “life-saving program” that should not be cut"), None),
             ("soc-05", 1, G("Acton on cannabis, which Ohio voters legalized in 2023"), "respect the will of the voters"),
             ("imm-07", 1, G("Acton on immigration enforcement (WLWT)"), "We want violent offenders off the street"),
             ("ene-01", 1, G("Acton’s all-of-the-above energy plan"), "the lowest-cost and cleanest sources of energy"),
             ("cri-01", 2, G("Acton on public safety"), "fully fund the police and public safety"),
             ("sta-08", 2, G("Acton on public safety"), "fully fund the police and public safety"),
             ("gov-05", 1, G("Acton would ensure Ohio’s voter ID law is enforced (Columbus Dispatch, May 2026)"), None),
             ("eco-09", 2, G("Acton on labor"), "steadfast pro-union, pro-worker Governor"),
             ("soc-12", 1, G("Acton on Pride Month"), "the right to live with dignity"))},
        {"id": "OH-GOV:ramaswamy", "name": "Vivek Ramaswamy", "party": "R",
         "bio": "Biotech entrepreneur and 2024 Republican presidential candidate.",
         "officialSite": "https://vivekforohio.com/",
         "positions": P(
             ("soc-03", -2, G("Ramaswamy on abortion (NBC’s Meet the Press, April 2023)"), "I believe that abortion is a form of murder"),
             ("soc-04", 2, G("Ramaswamy on abortion (NBC’s Meet the Press, April 2023)"), "I believe that abortion is a form of murder"),
             ("sta-04", 2, G("Ramaswamy’s plan (vivekforohio.com)"), "slash property taxes immediately"),
             ("eco-01", -2, G("Ramaswamy would phase out the state income tax, starting with capital gains taxes"), None),
             ("edu-06", 2, G("Ramaswamy on school choice"), "to the next level"),
             ("hea-03", -1, G("Ramaswamy says Medicaid without work requirements has harmed the people it was meant to help"), None),
             ("imm-01", 2, G("Ramaswamy on the border"), "Militarize the southern border"),
             ("ene-03", 2, G("Ramaswamy on energy (Canton Repository, June 2026)"), "We’re going to frack"),
             ("ene-06", -2, G("Ramaswamy on climate policy"), "The climate agenda is a hoax"),
             ("cri-01", 1, G("Ramaswamy on policing"), "more cops on the street"),
             ("sta-08", 1, G("Ramaswamy on policing"), "more cops on the street"),
             ("cri-04", 2, G("Ramaswamy’s plan (vivekforohio.com)"), "stricter bail and sentencing for repeat violent offenders"),
             ("gov-05", 2, G("Ramaswamy would put voter ID in Ohio’s constitution"), None),
             ("gov-06", -2, G("Ramaswamy has proposed single-day voting with paper ballots"), None),
             ("soc-12", -2, G("Ramaswamy has called transgender identity a “mental health disorder”"), None),
             ("eco-09", 1, G("Ramaswamy on labor organizing"), None))},
    ],
}

write("data/research/OH.json", [senate, governor], "Ohio U.S. Senate special and governor races, researched Oct. 24, 2026.")
