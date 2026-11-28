"""Sourced positions for the governors in office whose seats weren't on the 2026 ballot
(Delaware, Indiana, Kentucky, Louisiana, Mississippi, Missouri, Montana, New Jersey, North
Carolina, North Dakota, Utah, Virginia, Washington and West Virginia), the ones the state
pages show from data/officeholders.json. The governors elected in 2026 have their race
research (governors_2026.py and the state files). Writes
data/research/governors-sitting.json ({"people": {wiki link: {"positions": {...}}}}),
which update_officeholders.py lays over the recorded votes and bills of those who served in
Congress since 2021 (Braun, Armstrong, Sherrill, Spanberger) and over Beshear's 2028
research (this file wins where both answer a question). Owner's request, Nov. 27, 2026:
"getting political positions for every governor that is currently in charge".

The rules are the 2028 research's: only the governor's own words (State of the State and
budget addresses, inaugural addresses, campaign platforms, their office's releases, op-eds,
interviews, debate answers) or official acts (bills signed or vetoed with their message,
executive orders, budgets proposed), never what others say they think, never an advocacy
group's rating, and nothing inferred from party. A platform written in the third person by
the governor's own campaign or office counts as their text. Quotes are verbatim, at most 25
words, and were checked against the page's text (`--quotes` lists them by page for that
check); a news report's summary of an act has no quote. https only.

    py scripts/research/governors_sitting.py
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import P, article, page  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "research" / "governors-sitting.json"
READ = "2026-11-27"   # the day the quotes were last checked against the live pages
WIKI = "https://en.wikipedia.org/wiki/"


def site(title, url):
    """A live page read on READ; each call names what it shows."""
    return lambda note: page(f"{title}: {note}", url, READ)


# ---------------------------------------------------------------- Delaware: Matt Meyer (D)

MEYER_SOTS = article("Office of Gov. Matt Meyer, 2026 State of the State address, Jan. 22, 2026",
                     "https://governor.delaware.gov/text-of-the-2025-state-of-the-state-speech/", "2026-01-22")
MEYER_TAX = article("WHYY, Mar. 27, 2025",
                    "https://whyy.org/articles/delaware-new-tax-brackets-gov-meyer-housing-education/", "2025-03-27")
MEYER_MAID = article("Delaware Public Media, May 20, 2025",
                     "https://www.delawarepublic.org/politics-government/2025-05-20/gov-matt-meyer-signs-medical-aid-in-dying-into-law-after-decades-worth-of-effort",
                     "2025-05-20")
MEYER_ROWS = [
    ("eco-01", 2, MEYER_TAX("Meyer’s budget address proposed new income tax brackets that raise what wealthier Delawareans pay"),
     "hardworking Delawareans who come home with dirt under their nails and stains on their shirts have paid the same as the wealthiest among us"),
    ("eco-12", 2, MEYER_TAX("Meyer proposed new top brackets starting at $125,000, $250,000 and $500,000, with no increase under $134,667"), None),
    ("hea-07", 2, MEYER_SOTS("the end of the enhanced ACA premium subsidies"),
     "healthcare premiums are going up by thousands of dollars due to congressional Republicans’ unconscionable cutting of ACA subsidies"),
    ("soc-07", 2, MEYER_SOTS("early childhood education and child care"),
     "we will make a nearly $50 million investment in early childhood education"),
    ("soc-09", 2, MEYER_MAID("Meyer signed House Bill 140, the End-of-Life Options Act, which his predecessor had vetoed"),
     "giving families the comfort of knowing that their loved one was able to pass on their own terms without unnecessary pain"),
    ("ene-01", 2, MEYER_SOTS("the US Wind offshore wind project"),
     "U.S Wind, a 1.7-gigawatt project can and must be part of the solution"),
    ("ene-02", 2, MEYER_SOTS("nuclear energy"), "We also need safe, modern nuclear energy."),
    ("hou-04", 1, MEYER_SOTS("streamlining permits to build housing"),
     "One-third of housing costs today have nothing to do with construction – and everything to do with red tape."),
    ("hou-09", 2, MEYER_SOTS("broadband for every home"),
     "Delaware is closer than ever to being the first state in the country with universal high-speed broadband."),
    ("sta-10", 1, MEYER_SOTS("a film tax credit"),
     "it does not make sense that Delaware is one of the few states without a film tax credit"),
]

# ---------------------------------------------------------------- Indiana: Mike Braun (R)
# His Senate votes (2019-2025) and bills add federal positions in update_officeholders.py.

BRAUN_SOTS = article("Office of Gov. Mike Braun, 2026 State of the State address, Jan. 14, 2026",
                     "https://events.in.gov/event/gov-mike-brauns-2026-state-of-the-state-address", "2026-01-14")
BRAUN_SEX = article("Office of Gov. Mike Braun, Mar. 4, 2025",
                    "https://events.in.gov/event/release-governor-braun-signs-executive-orders-to-protect-womens-sports-and-reinforce-indianas-legal-definition-of-sex",
                    "2025-03-04")
BRAUN_ICE = article("Indiana Capital Chronicle, Jan. 28, 2025",
                    "https://indianacapitalchronicle.com/2025/01/28/gov-mike-braun-promises-indiana-law-enforcements-cooperation-with-federal-immigration-efforts/",
                    "2025-01-28")
BRAUN_EXEC = article("Office of Gov. Mike Braun, May 20, 2025",
                     "https://events.in.gov/event/statement-gov-mike-braun-issues-statement-on-execution-of-benjamin-ritchie", "2025-05-20")
BRAUN_ROWS = [
    ("edu-04", 2, BRAUN_SOTS("a $5,000 raise in starting teacher pay"),
     "We raised starting teacher salaries by $5,000 dollars so we can recruit the best."),
    ("edu-06", 2, BRAUN_SOTS("universal school choice"), "After decades of trying to get it done, Indiana now has UNIVERSAL SCHOOL CHOICE."),
    ("soc-07", 1, BRAUN_SOTS("child care costs"), "we need to make child care more affordable and available"),
    ("sta-04", 2, BRAUN_SOTS("property tax cuts"),
     "Our historic property tax cut will save taxpayers $1.5 billion dollars over the next 3 years."),
    ("hea-03", -1, BRAUN_SOTS("Medicaid work requirements"),
     "For Medicaid recipients who can work, work requirements foster self-sufficiency and build a foundation for a better life."),
    ("soc-12", -2, BRAUN_SEX("Executive Orders 25-35 (college women’s sports) and 25-36 (sex defined as biological sex in state law)"),
     "rejecting extreme gender ideology in favor of the scientific reality of biological sex"),
    ("eco-11", 1, BRAUN_SEX("an executive order expanding paid parental leave for state employees"),
     "landmark executive order expanding paid parental and childbirth recovery leave for women"),
    ("imm-07", 2, BRAUN_ICE("Executive Order 25-29: state law enforcement to cooperate fully with federal immigration enforcement"),
     "help find the most egregious examples of illegal immigrants that have committed egregious crimes"),
    ("imm-08", 1, BRAUN_ICE("Braun ordered state law enforcement to cooperate fully with federal immigration enforcement and kept 50 Indiana National Guard members at the southern border"), None),
    ("cri-09", 1, BRAUN_EXEC("Braun declined clemency and let the execution of Benjamin Ritchie go ahead"),
     "Today, Ritchie's sentence has been carried out as ordered by the court."),
]

# ---------------------------------------------------------------- Kentucky: Andy Beshear (D)
# Eight more positions come from scripts/research/president_2028.py (this file wins).

BESHEAR_SOTC = article("Office of Gov. Andy Beshear, 2026 State of the Commonwealth and budget address, Jan. 7, 2026",
                       "https://governor.ky.gov/attachments/20260107_State-of-the-Commonwealth-Address.pdf", "2026-01-07")
BESHEAR_AMEND2 = article("LEX18, Oct. 15, 2024",
                         "https://www.lex18.com/news/covering-kentucky/gov-beshear-urges-voters-to-say-no-to-amendment-2", "2024-10-15")
BESHEAR_DEBATE = article("LEX18 (governor’s debate), Oct. 16, 2023",
                         "https://www.lex18.com/news/state-of-the-commonwealth/candidates-wrangle-over-abortion-policy-in-kentucky-gubernatorial-debate",
                         "2023-10-16")
BESHEAR_ROWS = [
    ("eco-09", 2, BESHEAR_SOTC("unions"), "In Kentucky, we’ve proven that you can be pro-job, pro-business and pro-union."),
    ("eco-10", -2, BESHEAR_SOTC("tariffs"),
     "despite the damages of President Trump’s tariff policy that both of our U.S. Senators and this governor strongly oppose"),
    ("hea-03", 2, BESHEAR_SOTC("Medicaid coverage of dental, vision and hearing care"),
     "I was proud to expand Medicaid to include dental, vision and hearing."),
    ("hea-07", 2, BESHEAR_SOTC("the federal premium tax credits"),
     "voting “no” to extend tax credits for working Americans to afford health care"),
    ("soc-07", 2, BESHEAR_SOTC("Pre-K for All"),
     "The single-most effective way we succeed with this next budget is by funding Pre-K for All."),
    ("sta-02", 2, BESHEAR_SOTC("more school funding per pupil"), "My budget also increases education funding per pupil"),
    ("sta-08", 2, BESHEAR_SOTC("more and better-paid law enforcement"), "We do it by hiring more law enforcement and paying them better"),
    ("hou-01", 2, BESHEAR_SOTC("the Affordable Housing Trust Fund"),
     "So I am proposing a game-changing $150 million investment in our Affordable Housing Trust Fund."),
    ("sta-10", 1, BESHEAR_SOTC("job-creation incentives and site development"),
     "Last year, our average incentivized wage was just under $30 an hour."),
    ("ene-02", 1, BESHEAR_SOTC("a new nuclear company in Kentucky"), "bring modern nuclear power to our state"),
    ("edu-06", -2, BESHEAR_AMEND2("Beshear campaigned against Amendment 2, which would have allowed public money for private schools"),
     "Amendment 2 would allow Frankfort politicians to take taxpayer money away from public schools and send it to unaccountable private schools."),
    ("soc-04", -1, BESHEAR_DEBATE("Beshear wants rape and incest exceptions added to Kentucky’s abortion ban and supports some limits on late-term abortions"),
     "Those individuals deserve to have options"),
]

# ---------------------------------------------------------------- Louisiana: Jeff Landry (R)

LANDRY_2026 = article("Office of Gov. Jeff Landry, address opening the 2026 regular session, Mar. 9, 2026",
                      "https://gov.louisiana.gov/news/governor-jeff-landry-opens-third-regular-session", "2026-03-09")
LANDRY_2025 = article("Office of Gov. Jeff Landry, address opening the 2025 regular session, Apr. 14, 2025",
                      "https://gov.louisiana.gov/news/prioritizes-insurance-reform-maha-and-dotd-reorganization", "2025-04-14")
LANDRY_CRIME = article("Office of Gov. Jeff Landry, Mar. 5, 2024", "https://gov.louisiana.gov/news/4439", "2024-03-05")
LANDRY_LNG = article("Office of Gov. Jeff Landry, Dec. 18, 2024", "https://gov.louisiana.gov/news/4704", "2024-12-18")
LANDRY_EXEC = article("WBRZ, Mar. 19, 2025",
                      "https://www.wbrz.com/news/governor-says-state-s-execution-was-justice-jessie-hoffman-s-wife-calls-it-revenge-", "2025-03-19")
LANDRY_PILLS = article("CBS News, May 24, 2024", "https://www.cbsnews.com/news/louisiana-abortion-pill-law/", "2024-05-24")
LANDRY_ICE = article("Louisiana Illuminator, Sept. 3, 2025", "https://lailluminator.com/2025/09/03/ice-angola/", "2025-09-03")
LANDRY_ROWS = [
    ("edu-06", 2, LANDRY_2026("the LA GATOR education savings accounts he signed in 2024"),
     "I encourage you to strengthen the LA GATOR program helping families access the school that best suits their child."),
    ("edu-04", 2, LANDRY_2026("a permanent teacher pay raise"),
     "it converts that progress into something teachers feel immediately: a permanent pay raise"),
    ("sta-07", 2, LANDRY_2026("more money for community and technical colleges"),
     "Our proposal increases the Promise Program funding to expand access to community and technical colleges that train students for in-demand, high-paying jobs."),
    ("eco-12", -1, LANDRY_2026("eliminating the state income tax"),
     "We should renew our commitment to further tax reform in our quest for total elimination of the state income tax."),
    ("eco-02", 1, LANDRY_2025("lower income taxes"), "That’s why we worked so hard to lower income taxes and simplify our tax code."),
    ("cri-05", 1, LANDRY_2025("drug courts and re-entry programs"),
     "We have strengthened Drug Courts, focused on logistical improvements and effective re-entry programs."),
    ("cri-04", 2, LANDRY_CRIME("Landry signed the bills of his special session on crime"),
     "Reforms that put the interests of victims before the interests of criminals."),
    ("cri-09", 2, LANDRY_EXEC("Landry resumed executions, by nitrogen gas, after 15 years"),
     "If you commit heinous acts of violence in this State, it will cost you your life."),
    ("soc-04", 2, LANDRY_PILLS("Landry signed a law classifying the abortion pills mifepristone and misoprostol as controlled substances"), None),
    ("ene-03", 2, LANDRY_LNG("liquefied natural gas exports, as chair of the Governors’ Coalition for Energy Security"),
     "The facts clearly show that oil and gas exports strengthen local economies while maintaining affordable energy prices for our residents."),
    ("imm-07", 2, LANDRY_ICE("Landry opened Camp 57 at the Angola penitentiary to hold ICE detainees"),
     "will house the worst of the worst criminal illegal aliens arrested by ICE"),
]

# ---------------------------------------------------------------- Missouri: Mike Kehoe (R)

KEHOE_SOTS = article("Office of Gov. Mike Kehoe, 2026 State of the State address (as prepared), Jan. 13, 2026",
                     "https://content.govdelivery.com/attachments/MOGOV/2026/01/13/file_attachments/3520534/EMBARGOED%202026%20State%20of%20the%20State%20Address.pdf",
                     "2026-01-13")
KEHOE_ROWS = [
    ("eco-12", -2, KEHOE_SOTS("ending the income tax on capital gains, and phasing out the individual income tax"),
     "Just last year, we were proud to support a historic elimination of the income tax on capital gains."),
    ("eco-02", 1, KEHOE_SOTS("phasing out the individual income tax"),
     "we must begin the work now to phase-out and eliminate Missouri’s individual income tax"),
    ("sta-04", 1, KEHOE_SOTS("cutting local property taxes as sales taxes reach digital services"),
     "These increases will need to be offset by reducing local taxes, like property taxes"),
    ("edu-06", 2, KEHOE_SOTS("opting in to the federal scholarship tax credit, and open enrollment"),
     "The next step in school choice is clear: open enrollment."),
    ("sta-02", 2, KEHOE_SOTS("record funding for the K-12 formula"),
     "we provided record funding for the K-12 education formula, an increase equivalent to ten years of funding increases"),
    ("sta-08", 1, KEHOE_SOTS("grants for local law enforcement"),
     "allowing for just over 200 communities to receive grants of 50,000 dollars for law enforcement training and equipment"),
    ("soc-04", 2, KEHOE_SOTS("the 2026 ballot measure to repeal the abortion-rights amendment"),
     "vote to restore our pro-life laws that protect innocent life and prohibit dangerous transgender procedures for minors"),
    ("soc-11", -2, KEHOE_SOTS("the same ballot measure, which bans transition care for minors"),
     "vote to restore our pro-life laws that protect innocent life and prohibit dangerous transgender procedures for minors"),
    ("ene-02", 2, KEHOE_SOTS("nuclear power"),
     "We know nuclear is a safe, reliable, and clean energy source that can and will power Missouri’s economic future"),
    ("ene-01", -1, KEHOE_SOTS("limits on industrial solar developments"),
     "put basic guardrails around industrial solar developments that are dividing our rural communities"),
]

# ---------------------------------------------------------------- Mississippi: Tate Reeves (R)

REEVES_SOTS = article("Office of Gov. Tate Reeves, 2025 State of the State address (as prepared), Jan. 29, 2025",
                      "https://governorreeves.ms.gov/governor-reeves-gives-state-of-the-state-address-4/", "2025-01-29")
REEVES_REAP = article("NBC News, Feb. 28, 2023",
                      "https://www.nbcnews.com/nbc-out/out-politics-and-policy/mississippi-governor-signs-bill-banning-transgender-health-care-minors-rcna72765",
                      "2023-02-28")
REEVES_JORDAN = article("WLOX, June 24, 2025",
                        "https://www.wlox.com/2025/06/24/gov-reeves-court-appeals-reject-last-minute-petitions-richard-gerald-jordan/", "2025-06-24")
REEVES_ROWS = [
    ("eco-02", 1, REEVES_SOTS("eliminating the state income tax"),
     "The single best thing we can do for our state and her people is to eliminate our state’s income tax."),
    ("eco-12", -1, REEVES_SOTS("eliminating the state income tax"), None),
    ("hea-03", -2, REEVES_SOTS("Reeves opposes Medicaid expansion, which he calls a welfare expansion"),
     "now is not the time to expand welfare in our state"),
    ("ene-10", 2, REEVES_SOTS("affordable energy over climate policy"),
     "We don’t need ideology and climate-cult death-wish politics. We need abundant, affordable energy"),
    ("ene-03", 2, REEVES_SOTS("natural gas"), "that beautiful, life-giving technology: natural gas"),
    ("ene-02", 1, REEVES_SOTS("nuclear, solar and wind power among “all forms of energy”"),
     "Electricity derived from nuclear power, our sun, our winds"),
    ("ene-01", 1, REEVES_SOTS("nuclear, solar and wind power among “all forms of energy”"),
     "Electricity derived from nuclear power, our sun, our winds"),
    ("soc-11", -2, REEVES_REAP("Reeves signed House Bill 1125, banning puberty blockers, hormone therapy and surgery for minors"),
     "there is a dangerous movement spreading across America today"),
    ("cri-09", 1, REEVES_JORDAN("Reeves declined clemency for Richard Jordan and let his execution go ahead"), None),
]

# ---------------------------------------------------------------- Montana: Greg Gianforte (R)

GIANFORTE_SOTS = article("Office of Gov. Greg Gianforte, 2025 State of the State address, Jan. 13, 2025",
                         "https://news.mt.gov/Governors-Office/Governor_Gianforte_Outlines_Vision_To_Secure_Montanas_Future", "2025-01-13")
GIANFORTE_MEDICAID = article("Montana Public Radio, Mar. 28, 2025",
                             "https://www.mtpr.org/montana-news/2025-03-28/governor-signs-medicaid-expansion-renewal-into-law", "2025-03-28")
GIANFORTE_SB99 = article("KTVH, Apr. 28, 2023",
                         "https://www.ktvh.com/news/68th-session/gianforte-signs-bill-banning-gender-affirming-care-for-minors-in-montana",
                         "2023-04-28")
GIANFORTE_ROWS = [
    ("eco-02", 2, GIANFORTE_SOTS("a larger earned income tax credit and a lower income tax rate"),
     "we should expand the earned income tax credit for hardworking lower- and middle-income Montanans"),
    ("eco-07", 1, GIANFORTE_SOTS("holding down state spending and paying off the state’s debt"),
     "held the line on new spending, kept spending under inflation, and even paid off all the state’s debt"),
    ("sta-04", 2, GIANFORTE_SOTS("permanent property tax relief"),
     "One of my top priorities is delivering meaningful, permanent property tax relief for Montanans"),
    ("edu-04", 2, GIANFORTE_SOTS("$100 million for teacher pay"),
     "our budget invests a historic $100 million to raise teacher pay, with a focus on educators who are just starting their careers"),
    ("edu-03", 2, GIANFORTE_SOTS("more money for career and technical education"),
     "We’re also expanding educational opportunities through the Digital Academy and increasing funding for STEM and career and technical education."),
    ("edu-08", 2, GIANFORTE_SOTS("more money for STEM education"),
     "We’re also expanding educational opportunities through the Digital Academy and increasing funding for STEM and career and technical education."),
    ("sta-08", 2, GIANFORTE_SOTS("more money for law enforcement in his budget"),
     "That’s why our budget significantly increases support for law enforcement, because in Montana, we back the blue."),
    ("hou-04", 1, GIANFORTE_SOTS("the pro-housing reforms of his Housing Task Force, so more homes get built"),
     "now, Montana leads the nation in pro-housing reforms"),
    ("hea-03", 1, GIANFORTE_MEDICAID("Gianforte funded Medicaid expansion in his budget and signed House Bill 245, which keeps it from expiring in 2025"), None),
    ("soc-11", -2, GIANFORTE_SB99("Gianforte signed Senate Bill 99, banning puberty blockers, hormones and surgery for minors’ gender transition"), None),
    ("soc-12", -2, GIANFORTE_SOTS("the 2023 law defining sex in state law as the sex at birth"),
     "we’ve also defined an individual’s sex into law, because the sex one is born with is an unchangeable, biological fact"),
]

# ---------------------------------------------------------------- North Carolina: Josh Stein (D)

STEIN_SOTS = article("Office of Gov. Josh Stein, 2025 State of the State address (as prepared), Mar. 12, 2025",
                     "https://governor.nc.gov/news/press-releases/2025/03/12/governor-steins-state-state-remarks-prepared", "2025-03-12")
STEIN_JUNE = article("Office of Gov. Josh Stein, veto statements, June 20, 2025",
                     "https://governor.nc.gov/news/press-releases/2025/06/20/governor-stein-takes-action-four-bills", "2025-06-20")
STEIN_SB266 = article("Office of Gov. Josh Stein, veto statements, July 2, 2025",
                      "https://governor.nc.gov/news/press-releases/2025/07/02/governor-stein-takes-action-10-bills", "2025-07-02")
STEIN_JULY3 = article("Office of Gov. Josh Stein, veto statement, July 3, 2025",
                      "https://governor.nc.gov/news/press-releases/2025/07/03/governor-stein-takes-action-12-bills", "2025-07-03")
STEIN_ROWS = [
    ("eco-02", 2, STEIN_SOTS("targeted tax cuts for working families"),
     "we can cut taxes on working families to put more money in their pockets"),
    ("eco-12", 1, STEIN_SOTS("the scheduled income and corporate tax cuts, which he says go mainly to the wealthy"),
     "nearly $10 billion of tax giveaways over the next 4 years, mainly to the wealthy and to corporate shareholders"),
    ("hea-03", 2, STEIN_SOTS("defending North Carolina’s 2023 Medicaid expansion"),
     "Just as we stood arm-in-arm as North Carolinians to make Medicaid expansion a reality, let’s stand arm-in-arm to defend our health care."),
    ("hea-06", 2, STEIN_SOTS("more school support staff for students’ mental health"),
     "Let’s make sure our schools have the support staff they need to improve our kids’ mental health and help them thrive."),
    ("sta-02", 2, STEIN_SOTS("more school funding per pupil"),
     "North Carolina is 48th in the nation in per pupil investment – we can do so much better."),
    ("edu-04", 2, STEIN_SOTS("a teacher pay raise"), "we must give teachers a real pay raise"),
    ("edu-06", -2, STEIN_SOTS("the expansion of Opportunity Scholarships for private schools"),
     "We should not be taking money from our public school kids to pay for wealthy parents sending their kids to unaccountable private schools"),
    ("edu-09", 1, STEIN_SOTS("free school breakfast for every student"), "Let’s provide every North Carolina student a free school breakfast!"),
    ("edu-02", 1, STEIN_SOTS("free community college for certificates in high-demand fields"),
     "for students getting certified in high-demand sectors, like in advanced manufacturing, health care, and IT, we provide them free community college"),
    ("edu-03", 2, STEIN_SOTS("doubling the number of apprentices"), "Doubling the number of apprentices over the next four years"),
    ("sta-07", 2, STEIN_SOTS("Propel NC, which funds community colleges by the credentials students earn"),
     "We’ve also got to support Propel NC, which rewards community colleges when students earn credentials for high wage jobs."),
    ("soc-07", 2, STEIN_SOTS("affordable child care"),
     "Let’s work together to expand access to quality, affordable child care here in North Carolina!"),
    ("hou-04", 1, STEIN_SOTS("more housing of every type"),
     "To keep prices down, we need more housing of all types – single family, duplexes, triplexes, condos, apartments, special needs housing."),
    ("sta-08", 2, STEIN_SOTS("raises for state law enforcement and correctional officers"),
     "I’m proposing salary increases for state law enforcement and correctional officers and signing bonuses for new officers"),
    ("imm-07", 1, STEIN_JUNE("Stein vetoed House Bill 318, which makes sheriffs hold people for ICE up to 48 hours, as unconstitutional, but backs telling ICE about people charged with serious crimes"),
     "those charged with serious offenses ought to receive increased scrutiny from federal immigration officials"),
    ("imm-08", -1, STEIN_JUNE("Stein vetoed Senate Bill 153, which has state officers enforce immigration law"),
     "this bill takes state law enforcement officers away from their existing state duties and forces them to act as federal immigration agents"),
    ("ene-06", 2, STEIN_SB266("Stein vetoed Senate Bill 266, which drops the 2030 goal for cutting the power sector’s carbon emissions"),
     "this bill walks back our state’s commitment to reduce carbon emissions"),
    ("ene-01", 1, STEIN_SB266("the clean energy economy, in his veto of Senate Bill 266"),
     "sending the wrong signal to businesses that want to be a part of our clean energy economy"),
    ("soc-12", 1, STEIN_JULY3("Stein vetoed House Bill 805, which defines sex in state law as only male or female, and three bills banning DEI programs"),
     "These mean-spirited bills would marginalize vulnerable people"),
]

# ---------------------------------------------------------------- North Dakota: Kelly Armstrong (R)
# His House votes (2019-2024) and bills add federal positions in update_officeholders.py.

ARMSTRONG_2025 = article("Office of Gov. Kelly Armstrong, 2025 State of the State address, Jan. 7, 2025",
                         "https://www.governor.nd.gov/sites/www/files/documents/2025%20State%20of%20the%20State%20Address%20-for%20website.pdf",
                         "2025-01-07")
ARMSTRONG_2026 = article("Office of Gov. Kelly Armstrong, 2026 State of the State address, Jan. 21, 2026",
                         "https://www.governor.nd.gov/sites/www/files/documents/2026%20State%20of%20the%20State%20transcript.pdf",
                         "2026-01-21")
ARMSTRONG_VETOES = article("CBS Minnesota, Apr. 25, 2025",
                           "https://www.cbsnews.com/minnesota/news/north-dakota-governor-library-restrictions-veto/", "2025-04-25")
ARMSTRONG_ROWS = [
    ("sta-04", 2, ARMSTRONG_2025("his plan to cut homeowners’ property taxes, starting with a larger primary residence credit"),
     "Our property taxes are too high."),
    ("edu-06", 2, ARMSTRONG_2025("education savings accounts for public, private and home-schooled students, and public charter schools"),
     "Our budget will support Education Savings Accounts – funding set aside for each student to direct toward services or tuition"),
    ("edu-03", 1, ARMSTRONG_2025("career and technical education"), "Our Career and Technical Education programs are an absolute gamechanger."),
    ("cri-05", 1, ARMSTRONG_2025("a new cabinet post for recovery and re-entry"),
     "we are creating a new cabinet position, Commissioner of Recovery and Re-entry"),
    ("cri-08", 2, ARMSTRONG_2025("diversion and deflection programs that steer people toward addiction treatment"),
     "investing in diversion and deflection programs on the front end of the justice system"),
    ("ene-03", 2, ARMSTRONG_2025("more oil production and gas pipelines"),
     "To reduce flaring and increase oil production, we need to move our gas, and we must work with industry to build out pipeline infrastructure."),
    ("sta-09", 1, ARMSTRONG_2026("care closer to rural residents through the Rural Health Transformation Program"),
     "expanding local access to essential health services through telehealth, transportation, virtual medical rooms, and mobile clinics for hard-to-reach populations"),
    ("soc-01", 1, ARMSTRONG_VETOES("Armstrong vetoed a bill extending the limits on sexual material in public libraries to school libraries"),
     "represents a misguided attempt to legislate morality through overreach and censorship"),
]

# ---------------------------------------------------------------- New Jersey: Mikie Sherrill (D)
# Her House votes (2019-2025) and bills add federal positions in update_officeholders.py.

SHERRILL_EO = article("Office of Gov. Mikie Sherrill, Executive Orders 1 and 2, Jan. 20, 2026",
                      "https://www.nj.gov/governor/news/2026/20260120a.shtml", "2026-01-20")
SHERRILL_BUDGET = article("Office of Gov. Mikie Sherrill, Fiscal Year 2027 budget address (as prepared), Mar. 10, 2026",
                          "https://www.nj.gov/governor/news/remarks/20260310a_budget.shtml", "2026-03-10")
SHERRILL_ROWS = [
    ("ene-01", 2, SHERRILL_EO("Executive Order 2: new solar and battery storage, under a state of emergency on utility costs"),
     "massively expand in-state power generation – including solar and battery storage in the short-term, and nuclear power in the long-term"),
    ("ene-02", 2, SHERRILL_EO("Executive Order 2’s Nuclear Power Task Force"),
     "Establishes a Nuclear Power Task Force to position the state to lead on building new nuclear power generation."),
    ("sta-04", 2, SHERRILL_BUDGET("record property tax relief"),
     "it provides the most property tax relief in state history: nearly 4.2 billion dollars next year"),
    ("hea-07", 1, SHERRILL_BUDGET("Congress letting the ACA premium credits lapse"),
     "Because Washington refused to extend Affordable Care Act credits, nearly half-a-million New Jerseyans will see their premiums triple this year."),
    ("hea-03", 1, SHERRILL_BUDGET("help for Medicaid enrollees with the new federal paperwork rules, and a fine on companies with 50 or more workers on Medicaid that don’t insure them"),
     "because his H.R.1 law makes people jump through hoops to stay on Medicaid, 300,000 more New Jerseyans will be kicked off"),
    ("hea-06", 2, SHERRILL_BUDGET("mental health support in schools"), "brings specialized, intensive mental health support back into schools"),
    ("soc-07", 1, SHERRILL_BUDGET("the state child care program"), "It invests in our state childcare program."),
    ("hou-01", 1, SHERRILL_BUDGET("keeping the Affordable Housing Trust Fund for building affordable housing"),
     "protecting the Affordable Housing Trust Fund to the tune of 70 million dollars"),
    ("hou-03", 2, SHERRILL_BUDGET("new NJ Transit rail cars and buses"),
     "fully modernize one of the oldest rail fleets in the nation – starting with 40 new rail cars and 250 new buses"),
    ("hou-07", 2, SHERRILL_BUDGET("the Gateway rail tunnel"), "I’m going to keep fighting for every dollar owed to the Gateway Tunnel project"),
    ("sta-11", 1, SHERRILL_BUDGET("paring back corporate tax breaks"), "we’re also paring back some corporate tax breaks"),
]

# ---------------------------------------------------------------- Utah: Spencer Cox (R)

COX_2026 = article("Office of Gov. Spencer Cox, 2026 State of the State address (as prepared), published by KUER, Jan. 22, 2026",
                   "https://www.kuer.org/politics-government/2026-01-22/video-transcript-gov-spencer-cox-2026-utah-state-of-the-state-address",
                   "2026-01-22")
COX_2025 = article("Office of Gov. Spencer Cox, 2025 State of the State address (as prepared), published by KUER, Jan. 23, 2025",
                   "https://www.kuer.org/politics-government/2025-01-23/video-transcript-gov-spencer-cox-2025-utah-state-of-the-state-address",
                   "2025-01-23")
COX_BUDGET = article("Office of Gov. Spencer Cox, FY 2027 budget proposal, Dec. 3, 2025",
                     "https://governor.utah.gov/press/gov-cox-releases-fy-2027-budget-proposal-focused-on-responsible-fiscal-management-strong-families-and-long-term-prosperity/",
                     "2025-12-03")
COX_2023 = article("KSL, Jan. 28, 2023",
                   "https://www.ksl.com/article/50567331/gov-cox-signs-high-profile-bills-on-transgender-surgeries-school-choice-vouchers",
                   "2023-01-28")
COX_UNIONS = article("KUER, Feb. 14, 2025",
                     "https://www.kuer.org/politics-government/2025-02-14/gov-cox-signs-bill-that-bans-public-sector-unions-from-collective-bargaining",
                     "2025-02-14")
COX_ROWS = [
    ("hou-04", 2, COX_2026("zoning reform so more homes get built"),
     "We must pull every lever to increase the supply of housing — reform zoning, streamline permitting, support infrastructure, and encourage innovation."),
    ("hea-06", 1, COX_2026("help with mental illness for people who are chronically homeless"),
     "We’re starting with chronic homelessness — helping with mental illness and breaking the vicious cycle of addiction and crime."),
    ("ene-02", 2, COX_2025("advanced nuclear reactors under Operation Gigawatt"),
     "We're laying groundwork for advanced nuclear reactors while protecting national security by building capacity to be a net energy exporter through Operation Gigawatt."),
    ("eco-02", 1, COX_BUDGET("a larger state child tax credit"),
     "The budget also recommends expanding the Child Tax Credit to support more than 11,000 families with young children"),
    ("sta-02", 1, COX_BUDGET("a 4.2% increase in per-pupil school funding"),
     "The budget recommends $654.2 million for public education, including a 4.2% increase in the Weighted Pupil Unit"),
    ("sta-07", 1, COX_BUDGET("technical colleges and workforce preparation"),
     "targeted support for higher education and technical colleges to align workforce preparation with Utah’s economic needs"),
    ("eco-07", 1, COX_BUDGET("paying down state debt"), "Since 2021, Utah has paid down 66% of its general obligation (GO) debt"),
    ("soc-11", -2, COX_2023("Cox signed SB 16, which bans gender-transition surgery for minors and puts an indefinite moratorium on puberty blockers and cross-sex hormones for them"), None),
    ("edu-06", 2, COX_2023("Cox signed HB 215, which created an $8,000 private school voucher program alongside a $6,000 teacher raise"), None),
    ("edu-04", 2, COX_2023("Cox signed HB 215, which gave teachers a $6,000 raise alongside a private school voucher program"), None),
    ("eco-09", -1, COX_UNIONS("Cox signed House Bill 267, banning collective bargaining for public employees"), None),
]

# ---------------------------------------------------------------- Virginia: Abigail Spanberger (D)
# Her House votes (2019-2025) and bills add federal positions in update_officeholders.py.

SPANBERGER_JOINT = article("Office of Gov. Abigail Spanberger, address to the General Assembly (as prepared), Jan. 19, 2026",
                           "https://www.governor.virginia.gov/newsroom/news-releases/2026/january-releases/name-1111414-en.html", "2026-01-19")
SPANBERGER_WAGE = article("Office of Gov. Abigail Spanberger, Apr. 9, 2026",
                          "https://www.governor.virginia.gov/newsroom/news-releases/2026/april-releases/name-1116004-en.html", "2026-04-09")
SPANBERGER_LEAVE = article("Office of Gov. Abigail Spanberger, May 11, 2026",
                           "https://www.governor.virginia.gov/newsroom/news-releases/2026/may-releases/name-1117602-en.html", "2026-05-11")
SPANBERGER_ROWS = [
    ("sta-03", 2, SPANBERGER_WAGE("Spanberger signed SB 1 and HB 1, raising Virginia’s minimum wage to $15 an hour by 2028"),
     "Today, we are putting more money in the pockets of Virginia workers"),
    ("eco-11", 2, SPANBERGER_LEAVE("Spanberger signed the law creating paid family and medical leave of up to 12 weeks"),
     "Virginia is now the first state in the South to create a paid family and medical leave program."),
    ("soc-07", 2, SPANBERGER_JOINT("wider access to the state’s child care subsidy"), "increase access to Virginia’s child care subsidy program"),
    ("hea-07", 2, SPANBERGER_JOINT("state premium assistance after the federal ACA credits lapsed"),
     "Our proposal will establish targeted premium assistance."),
    ("hou-06", 2, SPANBERGER_JOINT("more time for tenants to pay overdue rent before an eviction"),
     "Our legislation will extend that window to two weeks — giving families a fair chance to get that paycheck, pay their rent"),
    ("hou-01", 1, SPANBERGER_JOINT("local affordable housing programs"), "we are going to give communities more tools to build affordable housing"),
    ("hou-04", 1, SPANBERGER_JOINT("a commission on unlocking housing production"),
     "We need to get ready to build more housing — and that’s why I am establishing a Commission on Unlocking Housing Production."),
    ("ene-01", 2, SPANBERGER_JOINT("offshore wind"), "And yes, despite what Washington might have you think, it also means offshore wind."),
    ("ene-06", 2, SPANBERGER_JOINT("rejoining the Regional Greenhouse Gas Initiative, which caps power plants’ carbon emissions"),
     "the Commonwealth of Virginia is rejoining the Regional Greenhouse Gas Initiative — RGGI"),
    ("soc-03", 2, SPANBERGER_JOINT("the reproductive-freedom amendment to Virginia’s constitution, sent to the voters"),
     "a woman has the same freedom to make her own healthcare decisions as she did before the fall of Roe v. Wade"),
    ("soc-04", -2, SPANBERGER_JOINT("the reproductive-freedom amendment to Virginia’s constitution, sent to the voters"),
     "a woman has the same freedom to make her own healthcare decisions as she did before the fall of Roe v. Wade"),
    ("soc-10", 2, SPANBERGER_JOINT("the marriage amendment to Virginia’s constitution, sent to the voters"),
     "Every citizen of this Commonwealth should rest assured that they can marry the person they love"),
    ("sta-08", 1, SPANBERGER_JOINT("recruiting and keeping law enforcement officers, firefighters and first responders"),
     "My administration will support these public servants with investments in recruitment, retention, training, and mental health resources."),
    ("edu-03", 2, SPANBERGER_JOINT("more apprenticeships"), "My administration will work to expand apprenticeships."),
]

# ---------------------------------------------------------------- Washington: Bob Ferguson (D)

FERGUSON_SOTS = article("Office of Gov. Bob Ferguson, 2026 State of the State address, Jan. 13, 2026",
                        "https://governor.wa.gov/news/speeches/state-state-2026", "2026-01-13")
FERGUSON_RENT = article("Office of Gov. Bob Ferguson, May 7, 2025",
                        "https://governor.wa.gov/news/2025/governor-ferguson-signs-rent-stabilization-affordable-housing-bills", "2025-05-07")
FERGUSON_ROWS = [
    ("eco-01", 2, FERGUSON_SOTS("a tax on income over $1 million a year"),
     "And that’s why I’m calling for something truly historic — a Millionaires’ Tax."),
    ("eco-12", 2, FERGUSON_SOTS("shifting taxes from working families to the wealthy"),
     "Our system takes too much in taxes from hardworking families and not enough from the wealthy."),
    ("eco-02", 2, FERGUSON_SOTS("a larger Working Families Tax Credit"),
     "Some of those gains must be used to expand eligibility for — and increase the amount of — the Working Families Tax Credit."),
    ("eco-08", 1, FERGUSON_SOTS("no B&O tax for small businesses grossing up to $1 million"),
     "they should not have to pay B&O taxes until they gross more than $1 million in revenue"),
    ("sta-02", 2, FERGUSON_SOTS("more money for K-12 schools"),
     "We should also use the gains from a Millionaires’ Tax to put more money into K-12 schools"),
    ("hou-01", 2, FERGUSON_SOTS("$244 million for housing in the supplemental budget"), "we will build and protect thousands of affordable housing units"),
    ("hou-05", 1, FERGUSON_SOTS("help for first-time home buyers"), "make it easier for first-time home buyers to enter the market"),
    ("hea-09", 1, FERGUSON_SOTS("vaccine recommendations set by the state Department of Health"),
     "shift vaccine recommendations away from science-denying federal committees and place it with our own Washington State Department of Health"),
    ("soc-07", 1, FERGUSON_SOTS("free early learning for military families"),
     "I support your effort to expand eligibility for free early learning programs to military families."),
    ("imm-08", -1, FERGUSON_SOTS("ICE’s tactics, and a ban on masked law enforcement"),
     "As an American, I never thought I would see federal agents in masks jumping out of unmarked cars and grabbing people off our streets."),
    ("hou-06", 2, FERGUSON_RENT("Ferguson signed House Bill 1217, capping yearly rent increases"),
     "House Bill 1217 limits rent increases for existing tenants in Washington state to 7% plus inflation or 10%, whichever is lower."),
    ("hou-04", 1, FERGUSON_RENT("bills encouraging “middle housing” such as condominiums"),
     "encouraging construction of so-called “middle housing” options like condominiums"),
]

# ---------------------------------------------------------------- West Virginia: Patrick Morrisey (R)

MORRISEY_2025 = article("Gov. Patrick Morrisey, 2025 State of the State address (transcript), West Virginia Public Broadcasting, Feb. 12, 2025",
                        "https://wvpublic.org/morrisey-state-of-the-state-transcript/", "2025-02-12")
MORRISEY_2026 = article("Office of Gov. Patrick Morrisey, 2026 State of the State address, Jan. 14, 2026",
                        "https://governor.wv.gov/article/governor-morrisey-highlights-major-victories-looks-ahead-cutting-taxes-improving-healthcare",
                        "2026-01-14")
MORRISEY_ROWS = [
    ("eco-02", 1, MORRISEY_2025("the lowest income tax among West Virginia’s neighbors"),
     "Tonight, I am renewing my call to ensure we have the lowest income tax of the states we touch."),
    ("eco-12", -1, MORRISEY_2025("cutting the income tax to the lowest among the neighboring states"),
     "Tonight, I am renewing my call to ensure we have the lowest income tax of the states we touch."),
    ("eco-07", 2, MORRISEY_2025("cutting spending rather than raising taxes"),
     "the answer to fiscal constraints is not to raise taxes – it’s to cut spending and grow our economy"),
    ("edu-03", 2, MORRISEY_2025("more vocational and technical education"),
     "We’re going to expand vocational tech and the way we prepare students to enter the job market."),
    ("imm-08", 1, MORRISEY_2025("working with the Trump administration on immigration enforcement"),
     "I’m already partnering with President Trump to crack down on illegal immigration and stop the flow of deadly fentanyl into our communities."),
    ("soc-12", -2, MORRISEY_2025("the Riley Gaines Act, defining sex-based terms in state law"),
     "allow for facilities such as locker rooms, bathrooms, and rape crisis centers to be based on biological sex"),
    ("ene-03", 2, MORRISEY_2025("more coal and gas"),
     "That means using even more coal and gas, utilizing our rich water resources, and developing nuclear-powered Small Modular Reactors."),
    ("ene-02", 2, MORRISEY_2025("small modular nuclear reactors"),
     "That means using even more coal and gas, utilizing our rich water resources, and developing nuclear-powered Small Modular Reactors."),
    ("hou-09", 1, MORRISEY_2025("faster broadband with the federal broadband money"),
     "West Virginians don’t want broadband that moves at the speed of slow."),
    ("soc-06", 1, MORRISEY_2025("religious liberty"),
     "We stand for God, life, religious liberty, the 2nd Amendment, our Constitution, and our freedoms."),
    ("edu-06", 2, MORRISEY_2026("fully funding the Hope Scholarship, the state’s education savings accounts"),
     "Our dedication to fiscal responsibility is also allowing us to fully fund the HOPE scholarship."),
    ("sta-07", 2, MORRISEY_2026("more money for higher education and technical training"),
     "By investing in higher education and technical training, we are ensuring that good-paying jobs are available for all West Virginians."),
    ("sta-01", 2, MORRISEY_2026("$100 million more for road and bridge repair"),
     "Apart from the current road fund, we plan to invest $100 million dollars to supplement our road and bridge repair work."),
    ("ene-08", 1, MORRISEY_2026("SENTRY, a flood-warning system"),
     "Finding a solution to our state’s flooding problems remains high on my list of priorities."),
]

PEOPLE = {
    "Matt_Meyer": MEYER_ROWS,
    "Mike_Braun": BRAUN_ROWS,
    "Andy_Beshear": BESHEAR_ROWS,
    "Jeff_Landry": LANDRY_ROWS,
    "Mike_Kehoe": KEHOE_ROWS,
    "Tate_Reeves": REEVES_ROWS,
    "Greg_Gianforte": GIANFORTE_ROWS,
    "Josh_Stein": STEIN_ROWS,
    "Kelly_Armstrong": ARMSTRONG_ROWS,
    "Mikie_Sherrill": SHERRILL_ROWS,
    "Spencer_Cox": COX_ROWS,
    "Abigail_Spanberger": SPANBERGER_ROWS,
    "Bob_Ferguson_(politician)": FERGUSON_ROWS,
    "Patrick_Morrisey": MORRISEY_ROWS,
}


def main():
    people = {WIKI + k: {"positions": P(*rows)} for k, rows in PEOPLE.items()}
    if "--quotes" in sys.argv:   # {url: [quotes]} for checking against the pages
        by_url = {}
        for rows in PEOPLE.values():
            for _, _, src, quote in rows:
                by_url.setdefault(src["url"], [])
                if quote and quote not in by_url[src["url"]]:
                    by_url[src["url"]].append(quote)
        print(json.dumps(by_url, ensure_ascii=False, indent=1))
        return
    out = {"updated": READ, "note": "Hand research for the governors whose seats weren't on the 2026 ballot (scripts/research/governors_sitting.py)",
           "people": people}
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    n = sum(len(p["positions"]) for p in people.values())
    print(f"wrote {OUT.relative_to(ROOT).as_posix()}: {len(people)} people, {n} positions")


if __name__ == "__main__":
    main()
