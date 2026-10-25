"""Researched details for Texas's statewide races: U.S. Senate (Talarico vs.
Paxton) and governor (Abbott vs. Hinojosa). Writes data/research/TX.json, which
update_races.py merges onto the automatically refreshed races.

Positions come from the candidates' own campaign sites (read Oct. 24, 2026),
bills Gov. Abbott signed (Texas Legislature Online), and news coverage that
reports a candidate's stance directly. Researched Oct. 24, 2026.

    py scripts/research/texas_2026.py
"""

from common import P, TODAY, source, write

# Talarico's campaign site, one page per issue.
T = {k: source(f"James Talarico campaign site, “{title}”", f"https://jamestalarico.com/issue/{slug}/", TODAY) for k, title, slug in [
    ("health", "Health Care", "health-care"),
    ("taxes", "Taxes & Cost of Living", "taxes-cost-of-living"),
    ("imm", "Immigration & Border Security", "immigration-border-security"),
    ("energy", "Energy & Environment", "energy-environment"),
    ("freedom", "Freedom, Family & Faith", "freedom-family-faith"),
    ("democracy", "Corruption & Democracy", "corruption-democracy"),
]}
TRIB = source("Texas Tribune: James Talarico is moderating on gender, climate issues in his competitive Senate election",
              "https://www.texastribune.org/2026/09/22/james-talarico-trans-climate-policy-changes-election-2026/", "2026-09-22")
PAX = source("Ken Paxton campaign site, “The Fight at Hand” (issues)", "https://www.kenpaxton.com/issues", TODAY)
PAX_OPINION = source("NBC News: Texas AG says transition care for minors is child abuse under state law (Paxton’s formal opinion KP-0401)",
                     "https://www.nbcnews.com/nbc-out/out-politics-and-policy/texas-ag-says-transition-care-minors-child-abuse-state-law-rcna17176", "2022-02-22")


def bill(session, number, what, signed):
    return source(f"Texas Legislature: {number} ({session}), {what}; signed by Gov. Abbott", f"https://capitol.texas.gov/BillLookup/History.aspx?LegSess={session_code(session)}&Bill={number.replace(' ', '')}", signed)


def session_code(s):
    return {"2021": "87R", "2021, 2nd special": "872", "2023": "88R", "2023, 2nd special": "882", "2023, 4th special": "884", "2025": "89R"}[s]


SB8 = bill("2021", "SB 8", "the Texas Heartbeat Act, banning abortion after about six weeks", "2021-05-19")
SB14 = bill("2023", "SB 14", "prohibiting gender-transition procedures and treatments for minors", "2023-06-02")
SB4 = bill("2023, 4th special", "SB 4", "making illegal entry into Texas a state crime", "2023-12-18")
SB3 = bill("2023, 4th special", "SB 3", "funding border barrier construction and border security operations", "2023-12-18")
SB1_21 = bill("2021, 2nd special", "SB 1", "the election law that banned drive-through and 24-hour early voting and added ID rules for mail ballots", "2021-09-07")
SB2_23 = bill("2023, 2nd special", "SB 2", "property tax relief through the school finance system", "2023-07-22")
SB2_25 = bill("2025", "SB 2", "creating an education savings account (school voucher) program", "2025-05-03")
HB2_25 = bill("2025", "HB 2", "public school finance", "2025-06-20")
KSAT = source("KSAT: Greg Abbott, Gina Hinojosa offer competing visions for Texas in governor’s race",
              "https://www.ksat.com/news/local/2026/10/20/greg-abbott-gina-hinojosa-offer-competing-visions-for-texas-in-governors-race/", "2026-10-19")
GH_SCHOOLS = source("Gina Hinojosa campaign site, “Save Texas Public Schools”", "https://ginafortexas.com/priority/save-texas-public-schools/", TODAY)
GH_MONEY = source("Gina Hinojosa campaign site, “Money in Your Pocket”", "https://ginafortexas.com/priority/an-affordable-texas-that-works-for-everyone/", TODAY)
GH_ROE = source("Gina Hinojosa campaign: on the anniversary of Roe v. Wade, a commitment to restore reproductive freedom",
                "https://ginafortexas.com/2026/01/on-anniversary-of-roe-v-wade-gina-hinojosa-shares-her-story-and-commitment-to-restore-reproductive-freedom/", "2026-01-22")

senate = {
    "id": "TX-SEN",
    "candidates": [
        {"id": "TX-SEN:talarico", "name": "James Talarico", "party": "D",
         "bio": "Texas state representative since 2019 and a former public school teacher.",
         "officialSite": "https://jamestalarico.com/", "donateUrl": "https://secure.actblue.com/donate/jt-tx-web",
         "positions": P(
             ("hea-01", 2, T["health"], "Because health care is a human right"),
             ("hea-03", 2, T["health"], "Allow every American — regardless of their age — to join Medicare"),
             ("hea-02", 2, T["health"], "Increase price transparency and negotiating power to ensure fair pricing"),
             ("hea-07", 2, T["health"], "reverse the Trump Administration’s dangerous cuts to the ACA enhanced tax credits"),
             ("eco-01", 2, T["taxes"], "Make billionaires pay their fair share in taxes"),
             ("eco-12", 1, T["taxes"], None),
             ("eco-02", 2, T["taxes"], "Pass a cost-of-living tax cut for the middle class"),
             ("eco-03", 2, T["taxes"], "Raise the federal minimum wage to $15 an hour"),
             ("eco-10", -2, T["taxes"], "Repeal the Trump tariffs"),
             ("hou-02", 2, T["taxes"], "ban Wall Street from buying up housing stock"),
             ("hou-04", 1, T["taxes"], None),
             ("imm-01", 1, T["imm"], None),
             ("imm-02", 2, T["imm"], "Create a path to citizenship for the immigrants who have been here the longest"),
             ("imm-07", 2, T["imm"], "Prioritize the deportation of criminals, gang members, and human traffickers"),
             ("imm-04", 2, T["imm"], "Hire more immigration judges to clear the asylum backlog"),
             ("imm-03", 1, T["imm"], "make it easier to come here legally"),
             ("ene-01", 2, T["energy"], "accelerate renewable energy development"),
             ("ene-03", 0, T["energy"], "all-of-the-above strategy that protects good-paying oil and gas jobs"),
             ("ene-04", 2, T["energy"], "Prioritize strengthening the Clean Air Act and the Clean Water Act"),
             ("ene-06", 1, TRIB, None),
             ("ene-08", 1, T["energy"], "Prepare for extreme weather events"),
             ("soc-03", 2, T["freedom"], "Restore reproductive freedom with federal legislation to codify Roe v. Wade"),
             ("soc-04", -2, T["freedom"], "codify Roe v. Wade"),
             ("soc-10", 2, T["freedom"], "protect the legality of gay marriage"),
             ("soc-12", 1, T["freedom"], "defend our LGBTQ+ neighbors from government overreach"),
             ("soc-06", 1, T["freedom"], "protect religious liberty and prevent religious discrimination"),
             ("soc-07", 2, T["freedom"], "expand access to affordable child care"),
             ("eco-11", 2, T["freedom"], "pass paid family leave legislation"),
             ("soc-05", 2, T["freedom"], "legalize regulated marijuana for adults"),
             ("gov-02", 2, T["democracy"], "Ban Members of Congress from trading individual stocks"),
             ("gov-01", 2, T["democracy"], None),
             ("gov-11", 2, T["democracy"], "Reverse the impact of the Supreme Court’s Citizens United ruling"),
             ("gov-13", -2, T["democracy"], None),
             ("gov-04", 2, T["democracy"], "Establish independent redistricting commissions"),
             ("gov-09", 1, T["democracy"], None))},
        {"id": "TX-SEN:paxton", "name": "Ken Paxton", "party": "R",
         "bio": "Texas attorney general since 2015; beat Sen. John Cornyn in the May 26 Republican primary runoff.",
         "officialSite": "https://www.kenpaxton.com/", "donateUrl": "https://secure.winred.com/ken-paxton-for-senate/donate-today",
         "positions": P(
             ("imm-01", 2, PAX, "help President Trump finish the border wall"),
             ("imm-07", 2, PAX, "deport the criminal illegal aliens"),
             ("imm-08", 1, PAX, None),
             ("eco-02", 1, PAX, "will fight to cut taxes"),
             ("eco-07", 1, PAX, "stop the wasteful spending"),
             ("ene-04", -1, PAX, "remove harmful regulations designed to hurt our energy companies"),
             ("ene-03", 1, PAX, "remove harmful regulations designed to hurt our energy companies"),
             ("soc-04", 2, PAX, "defend the unborn"),
             ("soc-03", -2, PAX, "defend the unborn"),
             ("soc-12", -2, PAX, "defeat the radical transgender movement"),
             ("soc-11", -2, PAX_OPINION, None))},
    ],
}

governor = {
    "id": "TX-GOV",
    "candidates": [
        {"id": "TX-GOV:abbott", "name": "Greg Abbott", "party": "R",
         "bio": "Governor of Texas since 2015, seeking a fourth term; previously Texas attorney general.",
         "officialSite": "https://www.gregabbott.com/",
         "positions": P(
             ("soc-04", 2, SB8, None),
             ("soc-03", -2, SB8, None),
             ("soc-11", -2, SB14, None),
             ("imm-08", 2, SB4, None),
             ("imm-01", 2, SB3, None),
             ("gov-06", -1, SB1_21, None),
             ("sta-04", 2, SB2_23, None),
             ("edu-06", 2, SB2_25, None),
             ("sta-02", 1, HB2_25, None))},
        {"id": "TX-GOV:hinojosa", "name": "Gina Hinojosa", "party": "D",
         "bio": "State representative from Austin since 2017 and former Austin school board president.",
         "officialSite": "https://ginafortexas.com/", "donateUrl": "https://secure.actblue.com/donate/web_ms_gh",
         "positions": P(
             ("edu-06", -2, GH_SCHOOLS, "end the voucher scam"),
             ("edu-04", 2, GH_SCHOOLS, "pay teachers to be among the highest paid in the nation"),
             ("edu-01", 2, GH_MONEY, "Fully fund schools"),
             ("sta-02", 2, GH_MONEY, "Fully fund schools"),
             ("sta-04", 2, GH_MONEY, "with the end goal of eliminating residential property taxes"),
             ("sta-10", -2, GH_MONEY, None),
             ("hou-02", 2, GH_MONEY, None),
             ("sta-09", 1, GH_MONEY, "Strengthen our rural hospital system"),
             ("gov-12", 1, GH_SCHOOLS, "audit and terminate corrupt vendor contracts"),
             ("soc-03", 2, GH_ROE, None),
             ("soc-04", -2, GH_ROE, None))},
    ],
    "notes": [{"text": "Hinojosa proposes a one-time $1,500 refund check to every Texas household from the rainy day fund, which would need the Legislature’s approval.", "source": "KSAT", "url": KSAT["url"]}],
}

write("data/research/TX.json", [senate, governor], "Texas U.S. Senate and governor races, researched Oct. 24, 2026.")
