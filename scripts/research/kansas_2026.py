"""Researched positions for Kansas's statewide races: U.S. Senate (Marshall vs.
Hamilton) and governor (Masterson vs. Holscher). Writes data/research/KS.json.

Positions come from guides.vote's nonpartisan Kansas guides, which tie each
stance to a vote, bill or statement (read Oct. 25, 2026). Researched Oct. 25, 2026.

    py scripts/research/kansas_2026.py
"""

from common import P, guide, write

READ = "2026-10-25"
S = guide("2026 Kansas U.S. Senate voters guide", "https://guides.vote/guide/2026-kansas-us-senate-voters-guide/", READ)
G = guide("2026 Kansas governor voters guide", "https://guides.vote/guide/2026-kansas-governor-voters-guide/", READ)

senate = {
    "id": "KS-SEN",
    "candidates": [
        {"id": "KS-SEN:hamilton", "name": "Adam Hamilton", "party": "D",
         "bio": "Founding senior pastor of the United Methodist Church of the Resurrection in Leawood, the largest Methodist church in the country.",
         "officialSite": "https://hamiltonforkansas.com/",
         "positions": P(
             ("soc-03", 2, S("Hamilton calls for legal and safe access to abortion"), "legal and safe access to abortion"),
             ("soc-04", -2, S("Hamilton voted against the 2022 Kansas amendment that would have let the Legislature restrict or ban abortion"), None),
             ("ene-01", 1, S("Hamilton would restore Biden-era energy production tax credits"), None),
             ("cri-09", -2, S("Hamilton opposes the death penalty (Mark Beckwith podcast, 2024)"), None),
             ("eco-04", 1, S("Hamilton would ban junk fees and algorithmic price-fixing at grocery stores"), None),
             ("hou-05", 2, S("Hamilton would create first-time homebuyer tax credits"), None),
             ("hea-03", 2, S("Hamilton would reverse the cuts to Medicaid"), "reverse the cuts to Medicaid"),
             ("hea-07", 2, S("Hamilton would restore ACA subsidies"), None),
             ("hea-02", 2, S("Hamilton would expand Medicare drug price negotiation"), None),
             ("hea-01", 1, S("Hamilton calls for universal access to a basic level of health care, though not Medicare for All"), None),
             ("imm-01", 1, S("Hamilton supports secure borders (Johnson County Post, July 2026)"), None),
             ("imm-09", 1, S("Hamilton would reform the H-2A guest-worker program with year-round visas"), None),
             ("imm-02", 1, S("Hamilton would give H-2A workers a path to legal status"), None),
             ("imm-07", 1, S("Hamilton says ICE should focus on serious criminals"), None),
             ("def-15", -2, S("Hamilton says he will fight to end the war in Iran"), None),
             ("eco-09", 2, S("Hamilton supports strengthening the right to organize and H.R. 5408"), None),
             ("soc-10", 2, S("Hamilton supports same-sex marriage (Resurrection Church, 2024)"), None),
             ("eco-03", 2, S("Hamilton says it is time to raise the outdated minimum wage"), None),
             ("eco-01", 1, S("Hamilton supports raising the Social Security tax cap on high earners"), None),
             ("gov-06", 2, S("Hamilton supports vote by mail (Johnson County Post, July 2026)"), None))},
        {"id": "KS-SEN:marshall", "name": "Roger Marshall", "party": "R",
         "bio": "U.S. senator since 2021, earlier a U.S. representative; an obstetrician.",
         "positions": P(
             ("soc-04", 2, S("Marshall sponsored S. 99 (2021) to establish a right to life at conception"), None),
             ("soc-03", -2, S("Marshall is a member of the Pro-Life Caucus and supported overturning Roe v. Wade"), None),
             ("ene-03", 2, S("Marshall on energy"), "Drill, Baby, Drill!"),
             ("ene-01", -1, S("Marshall voted to end Biden-era clean energy tax credits (Senate roll call 372, 2025)"), None),
             ("ene-06", -1, S("Marshall voted to end the EPA charge on oil and gas facilities exceeding greenhouse gas limits (Senate roll call 97, 2025)"), None),
             ("cri-06", -2, S("Marshall introduced a bill to withhold federal funds from local governments that eliminate cash bail (S. 5152, 2022)"), None),
             ("eco-06", -1, S("Marshall voted against the infrastructure law (Senate roll call 314, 2021)"), None),
             ("edu-06", 2, S("Marshall sponsored federal tax credits for private school scholarship donations (S. 292)"), None),
             ("ene-04", -2, S("Marshall voted to remove hazardous air pollutant rules and against mercury limits for power plants (Senate roll calls 232, 2025, and 135, 2026)"), None),
             ("hea-03", -1, S("Marshall voted for the 2025 law that cut Medicaid (Senate roll call 372)"), None),
             ("hea-07", -1, S("Marshall voted against extending ACA premium subsidies for 3 years (Senate roll call 644, 2025)"), None),
             ("imm-08", 2, S("Marshall voted to increase ICE funding by $75 billion and DHS by $70 billion more"), None),
             ("imm-01", 2, S("Marshall sponsored S. 2824 to build 900 miles of border wall"), None),
             ("imm-10", 2, S("Marshall sponsored S. 2824, requiring E-Verify for new employees"), None),
             ("imm-02", -1, S("Marshall voted in 2019 against a path to permanent residency for Dreamers (H.R. 6)"), None),
             ("imm-09", 1, S("Marshall supports continuing the H-2A guest worker program"), None),
             ("def-15", 2, S("Marshall on Iran"), "I'm standing with the President here"),
             ("def-04", -2, S("Marshall voted five times in 2026 against requiring congressional authorization for military action in Iran"), None),
             ("eco-09", -2, S("Marshall sponsored the National Right-to-Work Act (S. 532)"), None),
             ("soc-10", -1, S("Marshall voted against the Respect for Marriage Act (Senate roll call 362, 2022)"), None),
             ("soc-12", -2, S("Marshall sponsored S. 9 to ban transgender students from girls' school sports"), None),
             ("eco-03", -2, S("Marshall called a $15 minimum wage a job-killing proposal (2021)"), None),
             ("eco-01", -1, S("Marshall voted to extend the 2017 tax cuts (Senate roll call 372, 2025)"), None),
             ("gov-05", 2, S("Marshall voted to require voter ID (Senate roll call 73, 2026) and sponsored proof-of-citizenship rules"), None))},
    ],
}

governor = {
    "id": "KS-GOV",
    "candidates": [
        {"id": "KS-GOV:holscher", "name": "Cindy Holscher", "party": "D",
         "bio": "Kansas state senator from Johnson County.",
         "officialSite": "https://www.cindyforkansas.com/",
         "positions": P(
             ("soc-03", 2, G("Holscher on abortion"), "Every Kansan deserves access to reproductive care."),
             ("soc-04", -2, G("Holscher voted against SB 5 (2023), banning telehealth access to abortion drugs"), None),
             ("ene-01", 2, G("Holscher supports expanding wind power"), None),
             ("ene-06", 1, G("Holscher supports local emission goals and ending fossil fuel subsidies (Johnson County Post, 2020)"), None),
             ("cri-09", -2, G("Holscher sponsored SB 211 (2023) to abolish the death penalty"), None),
             ("cri-04", -1, G("Holscher voted against HB 2444 (2026), which lengthens prison sentences"), None),
             ("edu-06", -2, G("Holscher voted against opting into the federal private school tax credit program (HB 2468, 2026)"), None),
             ("edu-01", 2, G("Holscher supports fully funding public schools"), None),
             ("sta-02", 2, G("Holscher supports fully funding public schools"), None),
             ("ene-04", 1, G("Holscher voted to require groundwater conservation plans (HB 2279)"), None),
             ("hea-03", 2, G("Holscher voted to expand Medicaid (SB 161 amendment, 2025)"), None),
             ("imm-08", -1, G("Holscher voted against more cooperation between local police and ICE (HB 2372, 2026)"), None),
             ("eco-09", 2, G("Holscher sponsored an amendment to repeal Kansas's right-to-work provision (SCR 1609)"), None),
             ("soc-11", 1, G("Holscher voted against banning gender-affirming care for minors (SB 63, 2025)"), None),
             ("soc-12", 2, G("Holscher voted against the 2026 bathroom bill (SB 244) and the 2023 transgender sports ban (HB 2238)"), None),
             ("soc-05", 2, G("Holscher supports legalizing recreational and medicinal cannabis"), None),
             ("sta-03", 2, G("Holscher introduced a bill to raise the minimum wage to $16 (SB 471)"), None),
             ("sta-04", 2, G("Holscher supports cutting property taxes, with exemptions for seniors and disabled veterans"), None),
             ("eco-12", 1, G("Holscher voted against a flat income tax (SB 169, 2023)"), None),
             ("gov-06", 2, G("Holscher voted to keep the mail-ballot grace period and against limiting no-excuse mail voting"), None))},
        {"id": "KS-GOV:masterson", "name": "Ty Masterson", "party": "R",
         "bio": "President of the Kansas Senate.",
         "officialSite": "https://www.mastersonforgovernor.com/",
         "positions": P(
             ("soc-04", 2, G("Masterson sponsored a ban on second-trimester abortions (SB 95, 2015)"), None),
             ("soc-03", -2, G("Masterson on abortion"), "I will always defend the unborn's God-given right to life."),
             ("ene-03", 2, G("Masterson on energy"), "the most…oil and gas…friendly governor Kansas has ever had"),
             ("ene-06", -1, G("Masterson said climate activists would put the economy at risk (2023)"), None),
             ("cri-04", 2, G("Masterson voted for HB 2444 (2026), which lengthens prison sentences"), None),
             ("cri-01", 1, G("Masterson on police"), "I have always backed the blue."),
             ("sta-08", 1, G("Masterson on police"), "giving them the resources they need"),
             ("edu-06", 2, G("Masterson voted to opt into the federal private school tax credit program (HB 2468, 2026)"), "We need to give parents the freedom to choose."),
             ("hea-03", -2, G("Masterson voted against expanding Medicaid (2025) and for stricter eligibility checks (SB 363, 2026)"), None),
             ("imm-01", 2, G("Masterson backed sending $15.7 million to Texas for border security (2024)"), None),
             ("imm-08", 2, G("Masterson voted for more cooperation between local police and ICE (HB 2372, 2026)"), None),
             ("eco-09", -1, G("Masterson voted against advancing a repeal of Kansas's right-to-work provision (2025)"), None),
             ("soc-11", -2, G("Masterson voted to prohibit gender-affirming care for minors (SB 63, 2025)"), None),
             ("soc-12", -2, G("Masterson voted for the 2026 bathroom bill (SB 244) and the 2023 transgender sports ban (HB 2238)"), None),
             ("soc-05", -1, G("Masterson opposes legalizing recreational marijuana but is open to medical use"), None),
             ("sta-03", -2, G("Masterson opposed raising the minimum wage to $15 (2025)"), None),
             ("sta-04", 2, G("Masterson sponsored a resolution capping property tax increases (SCR 1616)"), None),
             ("eco-12", -2, G("Masterson voted for a flat income tax and a lower corporate rate (SB 169, 2023)"), None),
             ("gov-06", -2, G("Masterson voted to end the mail-ballot grace period and to limit no-excuse mail voting"), None),
             ("gov-05", 1, G("Masterson voted for the SAVE Kansas Act, checking voters against federal citizenship databases (HB 2437, 2026)"), None))},
    ],
}

write("data/research/KS.json", [senate, governor], "Kansas U.S. Senate and governor races, researched Oct. 25, 2026.", updated=READ)
