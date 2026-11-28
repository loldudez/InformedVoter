"""Sourced positions for the 2028 presidential field (#/2028), for the people whose
votes in Congress since 2021 give none or few. Writes data/research/president-2028.json
({"people": {wiki link: {"positions": {...}}}}), which update_president_2028.py lays over
the vote positions (research wins where both answer a question).

The rules are the site's: only the person's own words (campaign platforms, speeches,
op-eds, interviews, debate answers, their office's releases) or official acts (bills
signed, vetoed or sponsored, budgets proposed, tie-breaking votes), never what others say
they think, never an advocacy group's rating, and nothing inferred from party. A platform
written in the third person by the person's own campaign or office counts as their text.
Quotes are verbatim, at most 25 words, and were checked against the page's text in the
browser pane before going in (`python scripts/research/president_2028.py --quotes` lists
them by page for that check); a news report's summary has no quote. Older platforms
(Buttigieg's, Yang's and Jorgensen's 2020 campaigns, Vance's 2022 Senate campaign) are
cited from dated Wayback Machine copies, since the sites are gone. https only.

People with no position here have published none that answers a question: Don Lemon,
Soulja Boy (four priorities named in October 2026, no stances) and Randy Toler (his
campaign site has expired).

    py scripts/research/president_2028.py
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import P, article, page, source  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "research" / "president-2028.json"
READ = "2026-11-27"   # the day the quotes were last checked against the live pages
WIKI = "https://en.wikipedia.org/wiki/"


def site(title, url):
    """A live page read on READ; each call names what it shows."""
    return lambda note: page(f"{title}: {note}", url, READ)


def archived(title, url, date):
    """A page as the Wayback Machine kept it on `date` (a campaign site since taken down)."""
    return lambda note: source(f"{title}: {note}", url, date, accessed=False)


# ---------------------------------------------------------------- Democrats

HARRIS = archived("Kamala Harris for President, Issues (campaign site, Wayback Machine copy of Nov. 1, 2024)",
                  "https://web.archive.org/web/20241101234237/https://kamalaharris.com/issues/", "2024-11-01")
HARRIS_DEBATE = article("Presidential debate in Philadelphia, Sept. 10, 2024 (transcript, ABC News)",
                        "https://abcnews.go.com/Politics/harris-trump-presidential-debate-transcript/story?id=113560542", "2024-09-10")
HARRIS_ROWS = [
    ("eco-01", 2, HARRIS("rolling back the 2017 tax cuts for the wealthiest and a billionaire minimum tax"),
     "rolling back Trump’s tax cuts for the wealthiest Americans, enacting a billionaire minimum tax"),
    ("eco-02", 2, HARRIS("tax cuts for working and middle-class Americans"),
     "she will fight to cut taxes for more than 100 million working and middle class Americans"),
    ("eco-03", 2, HARRIS("raising the minimum wage"), "She’ll fight to raise the minimum wage"),
    ("eco-09", 2, HARRIS("signing the PRO Act"),
     "She’ll sign landmark pro-union legislation, including the PRO Act to support workers who choose to organize and bargain"),
    ("eco-11", 2, HARRIS("paid family and medical leave"), "establish paid family and medical leave"),
    ("eco-12", 1, HARRIS("the wealthiest and the largest corporations paying more"),
     "They will ensure the wealthiest Americans and the largest corporations pay their fair share"),
    ("hea-01", 1, HARRIS("health care as a right, by expanding the Affordable Care Act"),
     "make affordable health care a right, not a privilege by expanding and strengthening the Affordable Care Act"),
    ("hea-02", 2, HARRIS("Medicare drug price negotiation"),
     "she’ll accelerate the negotiations to cover more drugs and lower prices for Americans"),
    ("hea-07", 2, HARRIS("permanent premium tax credits"),
     "making permanent the Biden-Harris tax credit enhancements that are lowering health care premiums"),
    ("hou-02", 1, HARRIS("penalizing firms that hoard homes"),
     "penalize firms that hoard available homes to drive up prices for local homebuyers"),
    ("hou-05", 2, HARRIS("down-payment help for first-time buyers"),
     "provide first-time homebuyers with up to $25,000 to help with their down payments"),
    ("imm-01", 2, HARRIS("the bipartisan border security bill"),
     "she will bring back the bipartisan border security bill and sign it into law"),
    ("imm-02", 2, HARRIS("an earned pathway to citizenship"),
     "comprehensive reform that includes strong border security and an earned pathway to citizenship"),
    ("cri-01", 2, HARRIS("funding law enforcement"),
     "She will also continue to invest in funding law enforcement, including the hiring and training of officers"),
    ("soc-02", 2, HARRIS("the Equality Act"),
     "she’ll fight to pass the Equality Act to enshrine anti-discrimination protections for LGBTQI+ Americans"),
    ("soc-03", 2, HARRIS("restoring reproductive freedom"),
     "trust women to make decisions about their own bodies, and not have the government tell them what to do"),
    ("soc-07", 2, HARRIS("affordable child care"),
     "Vice President Harris will fight to ensure parents can afford high-quality child care and preschool for their children."),
    ("soc-12", 1, HARRIS("the Equality Act’s protections for LGBTQI+ Americans"),
     "she’ll fight to pass the Equality Act to enshrine anti-discrimination protections for LGBTQI+ Americans"),
    ("gov-06", 2, HARRIS("the Freedom to Vote Act"), "enshrine voting rights protections, expand vote-by-mail and early voting"),
    ("edu-03", 2, HARRIS("career pathways for non-college graduates"),
     "she will do even more to scale up programs that create good career pathways for non-college graduates"),
    ("edu-05", 1, HARRIS("student debt relief"), "she’ll continue working to end the unreasonable burden of student loan debt"),
    ("ene-01", 1, HARRIS("her tie-breaking vote for the Inflation Reduction Act"),
     "cast the tie-breaking vote to pass the Inflation Reduction Act, the largest investment in climate action in history"),
    ("agr-02", 1, HARRIS("American leadership in semiconductors"),
     "Vice President Harris will continue to support American leadership in semiconductors, clean energy, AI, and other cutting edge industries of the future."),
    ("def-02", 2, HARRIS("NATO and the alliances"), "she has worked with our allies to ensure NATO is stronger than ever"),
    ("def-12", 1, HARRIS("Israel’s ability to defend itself"), "she will always ensure Israel has the ability to defend itself"),
    ("def-13", 1, HARRIS("rallying help for Ukraine"),
     "helped mobilize a global response of more than 50 countries to help Ukraine defend itself"),
    ("def-14", 1, HARRIS("Russia’s aggression"), "help Ukraine defend itself against Vladimir Putin’s brutal aggression"),
    ("ene-03", 1, HARRIS_DEBATE("Harris said she would not ban fracking, citing her tie-breaking vote for the Inflation Reduction Act, which she said opened new leases for fracking"),
     "I will not ban fracking. I have not banned fracking as Vice President of the United States."),
]

NEWSOM = site("Office of Gov. Gavin Newsom, All progress", "https://www.gov.ca.gov/priorities-and-progress/progress/all-progress/")
NEWSOM_DP = article("Office of Gov. Gavin Newsom, Nov. 5, 2026",
                    "https://www.gov.ca.gov/2026/11/05/governor-newsom-releases-letter-to-california-on-the-death-penalty/", "2026-11-05")
NEWSOM_ENERGY = article("Office of Gov. Gavin Newsom, Sept. 19, 2025",
                        "https://www.gov.ca.gov/2025/09/19/governor-newsom-signs-historic-package-of-bipartisan-legislation-saving-billions-on-electric-bills-stabilizing-gas-market-and-cutting-pollution/",
                        "2025-09-19")
NEWSOM_SB107 = article("NBC News, Sept. 30, 2022",
                       "https://www.nbcnews.com/nbc-out/out-politics-and-policy/california-governor-signs-bill-offering-legal-refuge-transgender-youth-rcna50240",
                       "2022-09-30")
NEWSOM_SPORTS = article("NBC News, Mar. 6, 2025",
                        "https://www.nbcnews.com/nbc-out/out-politics-and-policy/california-gov-gavin-newsom-breaks-democrats-trans-sports-participatio-rcna195165",
                        "2025-03-06")
NEWSOM_ROWS = [
    ("hou-01", 2, NEWSOM("$40 billion for affordable housing"),
     "Governor Newsom invested over $40 billion to boost affordable housing across the state"),
    ("hou-04", 1, NEWSOM("CEQA reforms to streamline building"),
     "32 housing-related CEQA reforms since taking office to cut bureaucratic red tape and streamline building"),
    ("eco-06", 2, NEWSOM("$180 billion for infrastructure"),
     "the state is investing $180 billion in infrastructure over the next 10 years"),
    ("ene-01", 2, NEWSOM("100% clean electricity by 2045"),
     "These will help California meet its ambitious clean electricity target of 100% by 2045."),
    ("ene-04", 2, NEWSOM("the climate plan’s air pollution cut"), "cut air pollution by 71%"),
    ("ene-06", 2, NEWSOM_ENERGY("Newsom signed the extension of California’s cap-and-trade program (now cap-and-invest) to 2045"),
     "Extending Cap-and-Invest, formerly known as Cap-and-Trade, to 2045 continues California’s world-leading efforts to cut climate pollution"),
    ("ene-03", 1, NEWSOM_ENERGY("Newsom signed SB 237, allowing more oil drilling permits in Kern County while the state moves off fossil fuels"),
     "a targeted, locally-led, environmentally responsible and safe increase in oil production in Kern County to boost overall fuel supplies in the state"),
    ("hea-03", 2, NEWSOM("Medi-Cal for all income-eligible Californians"),
     "he expanded access to Medi-Cal to all income-eligible Californians, regardless of immigration status"),
    ("hea-06", 2, NEWSOM("mental health care"), "billions in investments to expand mental health care for low-income Californians"),
    ("hea-07", 2, NEWSOM("state premium help on top of federal subsidies"),
     "the state became the first in the nation to offer financial help for individual health insurance on top of federal support"),
    ("soc-03", 2, NEWSOM("abortion access"), "Governor Newsom has expanded and protected access to reproductive care"),
    ("soc-07", 2, NEWSOM("more child care slots"), "Led a significant expansion of childcare slots"),
    ("soc-11", 2, NEWSOM_SB107("Newsom signed SB 107, a legal refuge for transgender minors and their families seeking gender-affirming care"),
     "California will ensure that these kids and their families can seek and obtain the medical and mental health care that they need"),
    ("soc-12", 1, NEWSOM_SPORTS("Newsom, who signed California’s refuge law for transgender minors, called transgender athletes in female sports “deeply unfair”"),
     "It is an issue of fairness — it’s deeply unfair."),
    ("eco-11", 2, NEWSOM("paid family leave"), "expanded paid family leave and its wage replacement"),
    ("eco-02", 1, NEWSOM("the state Earned Income Tax Credit"),
     "Expanded the California Earned Income Tax Credit from $400 million in 2018 to over $1.3 billion"),
    ("edu-02", 1, NEWSOM("two tuition-free years of community college"),
     "Governor Newsom provided up to two years of community college tuition-free."),
    ("cri-01", 1, NEWSOM("funding for local law enforcement"),
     "California has made major investments in local law enforcement and prosecutors to combat violent crime"),
    ("cri-09", -2, NEWSOM_DP("Newsom plans to commute every California death sentence"),
     "Governor Gavin Newsom announced that he plans to change all California death sentences to life imprisonment without the possibility of parole."),
]

WHITMER = site("Office of Gov. Gretchen Whitmer, Signature Accomplishments",
               "https://www.michigan.gov/whitmer/issues/accomplishments/signature-accomplishments")
WHITMER_RHA = article("Office of Gov. Gretchen Whitmer, Nov. 21, 2023",
                      "https://www.michigan.gov/whitmer/news/press-releases/2023/11/21/governor-whitmer-signs-reproductive-health-act", "2023-11-21")
WHITMER_ELCRA = article("Office of Gov. Gretchen Whitmer, Mar. 16, 2023",
                        "https://www.michigan.gov/whitmer/news/press-releases/2023/03/16/whitmer-signs-bipartisan-legislation-expanding-rights-and-freedoms-for-lgbtq", "2023-03-16")
WHITMER_LINE5 = article("Office of Gov. Gretchen Whitmer, Nov. 13, 2020",
                        "https://www.michigan.gov/whitmer/news/press-releases/2020/11/13/governor-whitmer-takes-action-to-shut-down-the-line-5-dual-pipelines-through-the-straits-of-mackina",
                        "2020-11-13")
WHITMER_ROWS = [
    ("eco-02", 2, WHITMER("the Working Families Tax Credit, quintupled"),
     "Signed legislation to deliver a combined $3,800 refund to 650,000 working families in Michigan."),
    ("eco-09", 2, WHITMER("repealing right-to-work"),
     "Restored workers' rights to more effectively bargain together for fair wages, benefits, and safer working conditions."),
    ("eco-06", 2, WHITMER("fixing roads and bridges"),
     "Michigan will have fixed more than 26,500 lane miles of road and 2,000 bridges"),
    ("edu-01", 2, WHITMER("school funding"), "Closed the funding gap between schools in Michigan without raising taxes."),
    ("edu-02", 1, WHITMER("free community college"), "Expanded access to free pre-K and community college to every Michigander"),
    ("edu-03", 1, WHITMER("Michigan Reconnect"),
     "Launched Michigan Reconnect to offer a tuition-free path to higher education or skills training for any Michigander 21 and up."),
    ("edu-09", 2, WHITMER("free school meals for every public school student"),
     "Delivered free breakfast and lunch to all of Michigan’s 1.4 million public school students."),
    ("soc-07", 2, WHITMER("low- or no-cost child care"),
     "Expanded access to low or no-cost child care to 150,000 more kids and their families."),
    ("hea-03", 1, WHITMER("Healthy Michigan (Medicaid expansion)"), "Extended Healthy Michigan to over 700,000 people."),
    ("ene-01", 2, WHITMER("a 100% clean energy standard"), "Established a 100% clean energy standard for Michigan by 2040."),
    ("ene-06", 1, WHITMER("a 100% clean energy standard"), "Established a 100% clean energy standard for Michigan by 2040."),
    ("ene-02", 1, WHITMER("reopening the Palisades nuclear plant"),
     "reopened the Palisades Nuclear Plant, protecting 900 union jobs and clean power for 1.4 million households"),
    ("soc-03", 2, WHITMER_RHA("Whitmer signed the Reproductive Health Act"),
     "protects every Michigander’s constitutional right to make their own decisions about their own body"),
    ("soc-02", 2, WHITMER_ELCRA("Whitmer signed the expansion of Michigan’s civil rights law"),
     "no one can be fired from their job or evicted from their home because of who they are or how they identify"),
    ("soc-12", 2, WHITMER_ELCRA("Whitmer signed protections for gender identity and expression"),
     "Our LGBTQ+ friends, family, and neighbors deserve equal protection under the law so they can live their authentic lives"),
    ("ene-04", 1, WHITMER_LINE5("Whitmer revoked the easement for the Line 5 oil pipelines under the Straits of Mackinac to protect the Great Lakes"),
     "Enbridge has imposed on the people of Michigan an unacceptable risk of a catastrophic oil spill in the Great Lakes"),
]

BESHEAR_VETO = article("Associated Press (PBS News), Mar. 24, 2023",
                       "https://www.pbs.org/newshour/politics/kentucky-governor-vetoes-sweeping-gop-transgender-care-ban", "2023-03-24")
BESHEAR_BUDGET = article("Office of Gov. Andy Beshear, Dec. 18, 2023",
                         "https://www.kentucky.gov/Pages/Activity-stream.aspx?n=GovernorBeshear&prId=2057", "2023-12-18")
BESHEAR_ROWS = [
    ("soc-11", 1, BESHEAR_VETO("Beshear vetoed Senate Bill 150, which banned gender-affirming care for minors (his veto message)"),
     "too much government interference in personal healthcare issues and rips away the freedom of parents to make medical decisions for their children"),
    ("soc-12", 1, BESHEAR_VETO("Beshear’s veto message on Senate Bill 150"),
     "My faith teaches me that all children are children of God and Senate Bill 150 will endanger the children of Kentucky."),
    ("edu-04", 2, BESHEAR_BUDGET("Beshear’s budget proposed an 11% raise for all public school employees"),
     "Just imagine the local economic impact of an 11% raise to every employee of the county’s largest employer."),
    ("edu-01", 2, BESHEAR_BUDGET("Beshear’s budget put public education first"),
     "prioritizes public education and families by funding the largest single pay raise for public school educators and staff in 40 years"),
    ("soc-07", 1, BESHEAR_BUDGET("universal pre-K and support for child care providers"),
     "fully funding universal pre-K and providing support for child care providers"),
    ("edu-03", 1, BESHEAR_BUDGET("new career and technical education centers"),
     "will help build new career and technical education centers"),
    ("edu-05", 1, BESHEAR_BUDGET("student loan forgiveness for teachers"), "provides teachers student loan forgiveness"),
    ("hea-06", 1, BESHEAR_BUDGET("more mental health services in schools"), "boosts mental health services"),
]

BUTTIGIEG = archived("Pete for America, Issues (2020 campaign site, Wayback Machine copy of Jan. 31, 2020)",
                     "https://web.archive.org/web/20200131232747/https://peteforamerica.com/issues/", "2020-01-31")
BUTTIGIEG_RAIL = article("U.S. Department of Transportation, Dec. 8, 2023",
                         "https://www.transportation.gov/briefing-room/president-biden-announces-82-billion-new-grants-high-speed-rail-and-pipeline-projects",
                         "2023-12-08")
BUTTIGIEG_EV = article("U.S. Department of Transportation, Feb. 15, 2023",
                       "https://www.transportation.gov/briefing-room/biden-harris-administration-announces-latest-steps-deliver-national-network",
                       "2023-02-15")
BUTTIGIEG_ROWS = [
    ("hea-01", 2, BUTTIGIEG("universal coverage through “Medicare for All Who Want It”"),
     "Pete's approach will achieve universal coverage and put Americans back in charge of their health"),
    ("hea-03", 1, BUTTIGIEG("a public option open to everyone"), "Medicare for All Who Want It"),
    ("imm-02", 2, BUTTIGIEG("a pathway to citizenship"),
     "Common sense immigration reform must include a pathway to citizenship for immigrants living, working, paying taxes, and contributing to our American story, including DREAMers"),
    ("imm-04", 1, BUTTIGIEG("ending immigration and asylum backlogs"),
     "resources to end the backlogs in our lawful immigration and asylum processes"),
    ("soc-12", 2, BUTTIGIEG("LGBTQ+ rights, gender identity included"),
     "a person’s sexual orientation or gender identity should not limit them from pursuing their dreams and realizing their full potential"),
    ("soc-03", 2, BUTTIGIEG("abortion rights in federal law"), "Codify the right to an abortion into law."),
    ("gov-11", 2, BUTTIGIEG("public financing that matches small donors"),
     "Our democracy should work for the interests of ordinary Americans, not corporations and special interests."),
    ("gov-13", -2, BUTTIGIEG("overturning Citizens United"),
     "Overturn Citizens United and Buckley v. Valeo, if necessary by constitutional amendment"),
    ("gov-08", 2, BUTTIGIEG("a national popular vote"), "The Electoral College has to go."),
    ("gov-04", 2, BUTTIGIEG("independent redistricting"), "Establish independent, statewide redistricting commissions."),
    ("gov-06", 2, BUTTIGIEG("a new Voting Rights Act"),
     "A 21st Century Voting Rights Act to end all types of voter suppression and expand voting access."),
    ("eco-03", 2, BUTTIGIEG("a $15 minimum wage"), "Raise the minimum wage to $15"),
    ("eco-09", 2, BUTTIGIEG("doubling union membership"), "His policies aim to double unionization"),
    ("eco-11", 2, BUTTIGIEG("12 weeks of paid leave"),
     "Ensure all working Americans have access to 12 weeks of comprehensive paid family and medical leave."),
    ("edu-02", 1, BUTTIGIEG("debt-free public college"), "Middle-income families at public colleges will pay zero tuition."),
    ("edu-05", 1, BUTTIGIEG("cancelling debts from for-profit programs"),
     "We will cancel the debts of borrowers in low-quality, overwhelmingly for-profit programs"),
    ("ene-06", 2, BUTTIGIEG("eliminating greenhouse gas pollution"),
     "take bold, decisive action to eliminate greenhouse gas pollution once and for all"),
    ("ene-01", 2, BUTTIGIEG("the transition to clean energy"), "ensure the transition to clean energy is inclusive and fair for all"),
    ("cri-08", 2, BUTTIGIEG("diversion programs and halving incarceration"),
     "we also need to invest in social services and diversion programs, and allow people to rehabilitate"),
    ("def-07", 1, BUTTIGIEG("a higher bar for using military force"),
     "establish a new and higher standard for the deployment of U.S. military force"),
    ("hou-07", 2, BUTTIGIEG_RAIL("Secretary Buttigieg announced $8.2 billion for passenger rail, including the first high-speed line"),
     "$8.2 billion for faster, more reliable, expanded train service across the country"),
    ("ene-07", 2, BUTTIGIEG_RAIL("Secretary Buttigieg on the passenger rail grants"),
     "deliver the passenger rail system that Americans have been calling for"),
    ("ene-05", 2, BUTTIGIEG_EV("Secretary Buttigieg on standards for the national EV charging network the 2021 infrastructure law funds"),
     "This is a major step toward a world where every EV user will be able to find safe, reliable charging stations anywhere in the country"),
]

EMANUEL_WAGE = article("City of Chicago, Mayor’s Press Office, Dec. 2, 2014",
                       "https://www.chicago.gov/city/en/depts/mayor/press_room/press_releases/2014/dec/mayor-emanuel--city-council-approve-ordinance-to-increase-minimu.html",
                       "2014-12-02")
EMANUEL_PREK = article("City of Chicago, Mayor’s Press Office, May 30, 2018",
                       "https://www.chicago.gov/city/en/depts/mayor/press_room/press_releases/2018/may/UniversalPreK.html", "2018-05-30")
EMANUEL_NPR = article("NPR (KPBS), Jan. 22, 2026",
                      "https://www.kpbs.org/news/politics/2026/01/22/rahm-emanuel-critiques-democrats-and-offers-advice-for-the-upcoming-midterms",
                      "2026-01-22")
EMANUEL_ROWS = [
    ("eco-03", 2, EMANUEL_WAGE("Mayor Emanuel’s ordinance raising Chicago’s minimum wage to $13 by 2019 passed the City Council"),
     "A higher minimum wage ensures that nobody who works in the City of Chicago will ever struggle to reach the middle class"),
    ("soc-07", 1, EMANUEL_PREK("Mayor Emanuel’s plan to make full-day pre-kindergarten universal for Chicago’s 4-year-olds"), None),
    ("imm-07", 2, EMANUEL_NPR("Emanuel would have local officials hand people held in prison, who were convicted of crimes, to ICE “one hundred percent”"), None),
    ("def-02", 2, EMANUEL_NPR("Emanuel says the United States is throwing away its global alliances"),
     "We just decided that it's a burden on us, and we're going to see the price for that."),
]

# ---------------------------------------------------------------- Republicans

DESANTIS_LIFE = article("Office of Gov. Ron DeSantis, Apr. 13, 2023",
                        "https://www.flgov.com/eog/news/press/2023/governor-ron-desantis-signs-heartbeat-protection-act", "2023-04-13")
DESANTIS_CHOICE = article("Office of Gov. Ron DeSantis, Mar. 27, 2023",
                          "https://www.flgov.com/eog/news/press/2023/governor-ron-desantis-signs-historic-legislation-expand-school-choice-options-all", "2023-03-27")
DESANTIS_IMM = article("Office of Gov. Ron DeSantis, May 10, 2023",
                       "https://www.flgov.com/eog/news/press/2023/governor-ron-desantis-signs-strongest-anti-illegal-immigration-legislation-country", "2023-05-10")
DESANTIS_PAY = article("Office of Gov. Ron DeSantis, May 9, 2023",
                       "https://www.flgov.com/eog/news/press/2023/governor-ron-desantis-approves-record-increase-teacher-pay-and-signs-nations-most", "2023-05-09")
DESANTIS_CRIME = article("Office of Gov. Ron DeSantis, May 1, 2023",
                         "https://www.flgov.com/eog/news/press/2023/governor-ron-desantis-signs-third-consecutive-anti-crime-pro-public-safety", "2023-05-01")
DESANTIS_KIDS = article("Office of Gov. Ron DeSantis, May 17, 2023",
                        "https://www.flgov.com/eog/news/press/2023/governor-ron-desantis-signs-sweeping-legislation-protect-innocence-floridas", "2023-05-17")
DESANTIS_ENERGY = article("Florida Phoenix, May 15, 2024",
                          "https://floridaphoenix.com/2024/05/15/desantis-signs-bill-erasing-the-term-climate-change-from-state-law/", "2024-05-15")
DESANTIS_FUEL = article("DeSantis for President, Sept. 20, 2023 (The American Presidency Project)",
                        "https://www.presidency.ucsb.edu/documents/desantis-campaign-press-release-ron-desantis-announces-plan-revive-american-energy", "2023-09-20")
DESANTIS_SB2C = article("WUSF, Feb. 13, 2025",
                        "https://www.wusf.org/politics-issues/2025-02-13/desantis-signs-sweeping-bills-to-beef-up-immigration-enforcement-in-florida", "2025-02-13")
DESANTIS_ROWS = [
    ("soc-04", 2, DESANTIS_LIFE("DeSantis signed the Heartbeat Protection Act (SB 300), banning abortion once a heartbeat is detected"),
     "I applaud the Legislature for passing the Heartbeat Protection Act that expands pro-life protections and provides additional resources for young mothers and families."),
    ("edu-06", 2, DESANTIS_CHOICE("DeSantis signed HB 1, opening school choice scholarships to every student"),
     "today’s bill signing represents the largest expansion of education choice in the history of these United States"),
    ("imm-10", 2, DESANTIS_IMM("DeSantis signed SB 1718, which requires E-Verify"),
     "This legislation makes using E-Verify mandatory for any employer with 25 or more employees"),
    ("imm-05", 2, DESANTIS_IMM("SB 1718’s penalties for employers"), "imposes enforceable penalties for those employing illegal aliens"),
    ("edu-04", 2, DESANTIS_PAY("DeSantis approved a record increase in teacher pay"),
     "We have delivered another record boost to teacher pay and we have coupled salary increases with positive reforms."),
    ("cri-09", 2, DESANTIS_CRIME("DeSantis signed HB 1297, making child rape a capital crime"), "subject child rapists to the death penalty"),
    ("cri-04", 2, DESANTIS_CRIME("DeSantis’s anti-crime package"),
     "with a particular emphasis on keeping criminals in jail and throwing the book at pedophiles"),
    ("cri-06", -2, DESANTIS_CRIME("DeSantis signed HB 1627 against “bail reform”"),
     "push back against “bail reform” efforts that have made other states significantly less safe"),
    ("soc-11", -2, DESANTIS_KIDS("DeSantis signed SB 254, banning gender transition treatment for minors"),
     "Prohibits sex reassignment surgeries and experimental puberty blockers for children."),
    ("soc-12", -2, DESANTIS_KIDS("DeSantis signed HB 1521, requiring restrooms and changing rooms separated by sex at birth, with SB 254"),
     "ensures that Florida’s bathrooms, changing rooms, and locker rooms are safe places for women"),
    ("ene-01", -1, DESANTIS_ENERGY("DeSantis signed HB 1645, which bans building or expanding offshore wind facilities and certain wind turbines within a mile of the coast"), None),
    ("ene-06", -2, DESANTIS_ENERGY("DeSantis signed HB 1645, removing climate change and greenhouse gas goals from state energy policy (his statement on X)"),
     "Radical green zealots want to impose their climate agenda on people through restrictions, regulations, and taxes."),
    ("ene-03", 2, DESANTIS_FUEL("DeSantis’s “Freedom to Fuel” energy plan (his campaign’s release)"),
     "Unleash oil and gas exploration and development, pipelines, and infrastructure on Day One to crush inflation and support working families"),
    ("imm-08", 2, DESANTIS_SB2C("DeSantis signed a package of immigration bills that puts $298 million into state immigration enforcement and creates a State Board of Immigration Enforcement"), None),
]

VANCE = archived("JD Vance for Senate, Issues (2022 campaign site, Wayback Machine copy of Oct. 30, 2022)",
                 "https://web.archive.org/web/20221030041014/https://jdvance.com/issues/", "2022-10-30")
VANCE_OBBBA = article("PBS News, July 1, 2025",
                      "https://www.pbs.org/newshour/politics/senate-passes-trumps-reconciliation-bill-with-vance-casting-tie-breaking-vote", "2025-07-01")
VANCE_S2357 = article("WKYC, July 19, 2023",
                      "https://wkyc.com/article/news/politics/us-senator-jd-vance-introduces-bill-federally-ban-gender-reassignment-procedures-minors/95-5a109a15-2430-4635-ac00-bc9b1ca1792a",
                      "2023-07-19")
VANCE_ROWS = [
    ("hea-03", -1, VANCE_OBBBA("As vice president, Vance cast the tie-breaking vote for H.R. 1 (2025), the tax and spending law that cut federal Medicaid spending"), None),
    ("soc-11", -2, VANCE_S2357("As a senator, Vance proposed the Protect Children’s Innocence Act (S. 2357), under which doctors who perform gender transition procedures on minors could be charged with a felony"), None),
    ("ene-03", 2, VANCE("energy independence"),
     "implement policies that properly support the ample natural energy we can harness and produce right here at home"),
    ("imm-02", -2, VANCE("no amnesty"), "I will oppose every attempt by the Democrats to grant amnesty"),
    ("imm-01", 2, VANCE("a border wall"),
     "I’ll also work to finish construction of a border wall, and double the number of border agents in our country."),
    ("imm-08", 2, VANCE("twice as many border agents"), "double the number of border agents in our country"),
    ("imm-06", -1, VANCE("refugees"), "accept millions of refugees into middle and working class neighborhoods. This is a bad deal for Americans"),
    ("eco-10", 2, VANCE("tariffs on goods made in China"),
     "imposing punitive tariffs on companies that manufacture in China and other nations. These were the right policies"),
    ("eco-05", 2, VANCE("lower taxes for companies that invest at home"),
     "let’s cut the taxes of the companies that invest in our country. But we’re going to raise taxes on companies that ship jobs overseas"),
    ("agr-03", 1, VANCE("rebuilding manufacturing"), "the effort to rebuild our industrial base is only beginning"),
    ("eco-07", 1, VANCE("federal spending"), "The Biden administration has spent billions and billions of dollars on things we don’t need."),
    ("eco-04", 2, VANCE("breaking up big tech companies"),
     "we need to break up the big tech companies, to reduce their power in our economy and our politics"),
    ("soc-08", 2, VANCE("personal data"), "We also need to ban the theft of our personal information. If they want our data, it’s time they paid for it."),
    ("soc-04", 2, VANCE("abortion"), "I am 100 percent pro-life"),
    ("gov-05", 2, VANCE("voter ID"), "Voter ID, signature verification on absentee ballots, and an end to mass mail-in voting"),
    ("gov-06", -2, VANCE("ending mass mail-in voting"), "Voter ID, signature verification on absentee ballots, and an end to mass mail-in voting"),
    ("def-07", 1, VANCE("nation-building wars"), "a good deal for the elites who profit from endless war"),
]

PENCE_LIFE = article("Pence 2024 campaign release (The American Presidency Project), June 26, 2023",
                     "https://www.presidency.ucsb.edu/documents/pence-campaign-press-release-icymi-anniversary-dobbs-mike-pence-leads-gop-field-life", "2023-06-26")
PENCE_PLAN = article("Pence 2024 campaign release (The American Presidency Project), July 26, 2023",
                     "https://www.presidency.ucsb.edu/documents/pence-campaign-press-release-pence-releases-the-pence-plan-fight-inflation", "2023-07-26")
PENCE_TARIFF = article("Pence 2024 campaign release (The American Presidency Project), Sept. 21, 2023",
                       "https://www.presidency.ucsb.edu/documents/pence-campaign-press-release-icymi-mike-pence-says-no-trumps-10-tariff-plan-mornings-with", "2023-09-21")
PENCE_WORLD = article("Pence 2024 campaign release (The American Presidency Project), Sept. 19, 2023",
                      "https://www.presidency.ucsb.edu/documents/pence-campaign-press-release-icymi-pence-releases-plan-for-security-home-and-stability", "2023-09-19")
PENCE_ROWS = [
    ("soc-04", 2, PENCE_LIFE("Pence called for a nationwide 15-week abortion ban at minimum"),
     "Every Republican candidate for president should support a ban on abortion before 15 weeks as a minimum nationwide standard."),
    ("soc-03", -2, PENCE_LIFE("Pence on the anniversary of the Dobbs decision"), "We'll continue to stand for the right to life without apology."),
    ("eco-07", 2, PENCE_PLAN("Pence’s plan to fight inflation"),
     "My top economic priority will be to renew American prosperity by cutting wasteful government spending"),
    ("ene-03", 2, PENCE_PLAN("more oil and gas leasing and exploration"),
     "restarting oil and gas leasing on federal lands, opening the Arctic and offshore regions for exploration"),
    ("ene-10", 2, PENCE_PLAN("cheap energy"), "Produce cheap, abundant American made energy to power our economy."),
    ("ene-06", -1, PENCE_PLAN("climate policy"), "rejecting climate change hysteria that is causing U.S. energy production to fall"),
    ("agr-03", 1, PENCE_PLAN("bringing supply chains home"), "Bring manufacturing and production supply chains back home to reduce costs"),
    ("agr-05", 1, PENCE_PLAN("mining rare earth minerals at home"), "mining rare earth minerals"),
    ("eco-10", -2, PENCE_TARIFF("Pence against a 10% tariff on all imports"),
     "Trump's broad-sweeping 10% tariffs on all imported goods will be a tax increase on America's families"),
    ("def-16", 2, PENCE_WORLD("Pence’s plan to counter China"),
     "China is the greatest strategic and economic threat to the United States of America in the 21st century"),
    ("def-13", 2, PENCE_WORLD("Pence argued that holding back U.S. support for Ukraine would embolden China (The Hill’s report, quoted by his campaign)"), None),
]

CHRISTIE = article("Republican debate in Milwaukee, Aug. 23, 2023 (transcript, The American Presidency Project)",
                   "https://www.presidency.ucsb.edu/documents/republican-candidates-debate-milwaukee-wisconsin-0", "2023-08-23")
CHRISTIE_WIND = article("CBS Philadelphia, Aug. 19, 2010",
                        "https://www.cbsnews.com/philadelphia/news/christie-signs-bill-to-boost-wind-turbine-industry-in-nj", "2010-08-19")
CHRISTIE_ROWS = [
    ("eco-07", 2, CHRISTIE("Christie on federal spending"),
     "We cannot sit by any longer and allow the kind of spending that is going on in Washington."),
    ("def-13", 2, CHRISTIE("Christie on standing with Ukraine"),
     "If we don't stand up against this type of autocratic killing in the world, we will be next."),
    ("def-14", 2, CHRISTIE("Christie on Russia’s war, after his visit to Ukraine"),
     "I wanted to see for myself, what Vladimir Putin's army was doing to the free Ukrainian people."),
    ("imm-01", 1, CHRISTIE("Christie on the border"), "the first thing we need to do is to stop any more from coming"),
    ("imm-08", 1, CHRISTIE("Christie on detaining people who crossed illegally"), "We have to have them detained."),
    ("def-16", 2, CHRISTIE("Christie on China and fentanyl"), "The Chinese are engaging in an act of war against us killing our citizens."),
    ("ene-01", 1, CHRISTIE_WIND("As governor, Christie signed the Offshore Wind Economic Development Act, with incentives for wind farms off New Jersey’s coast and a goal of at least 1,100 megawatts"), None),
]

GREANEY = site("Dan Greaney for President 2028, The Issue Is America (platform)", "https://dangreaneyusa.com/issues")
GREANEY_CU = "A multi-tiered approach combining transparency legislation and a constitutional amendment to repeal Citizens United"
GREANEY_GSD = "Massive investment in clean energy, public transit, and resilient infrastructure"
GREANEY_ROWS = [
    ("gov-11", 2, GREANEY("repealing Citizens United"), GREANEY_CU),
    ("gov-13", -2, GREANEY("a constitutional amendment repealing Citizens United"), None),
    ("gov-03", 2, GREANEY("transparency legislation"), GREANEY_CU),
    ("gov-09", 1, GREANEY("accountability for officials"), "No official or citizen at any level will be above the law."),
    ("hea-01", 2, GREANEY("health care for all"), "Guarantee health coverage for every American regardless of income, employment, or geography"),
    ("hea-02", 1, GREANEY("lower drug prices"), "Lower prescription drug costs and bring real price transparency to the system"),
    ("soc-03", 2, GREANEY("reproductive rights"), "Protect and expand reproductive rights as a core component of health care"),
    ("hou-02", 1, GREANEY("cracking down on corporate consolidation in housing"),
     "Crack down on speculation and corporate consolidation in single-family housing"),
    ("hou-06", 1, GREANEY("protecting renters"), "Protect renters and first-time homebuyers from predatory practices"),
    ("eco-06", 2, GREANEY("the Green Square Deal"),
     "An ambitious Green Square Deal to rebuild American infrastructure, create good jobs, and meet the climate crisis."),
    ("ene-01", 2, GREANEY("clean energy investment"), GREANEY_GSD),
    ("hou-03", 2, GREANEY("public transit investment"), GREANEY_GSD),
    ("hou-10", 1, GREANEY("resilient infrastructure"), GREANEY_GSD),
    ("eco-09", 1, GREANEY("union jobs in the energy transition"), "Good union jobs at the center of the energy transition"),
]

WHITE = article("KSTP, Aug. 7, 2026",
                "https://kstp.com/kstp-news/top-news/5-questions-on-5-issues-royce-white-republican-candidate-for-us-senate/", "2026-08-07")
WHITE_ROWS = [
    ("eco-04", 2, WHITE("White, running again for the U.S. Senate in Minnesota, on health care"),
     "My first prescription for health care reform is that we become much more strict with our anti-trust laws."),
    ("cri-02", 1, WHITE("White on body cameras for immigration agents"), "Yeah, body cameras are great."),
]

BOVINO = article("The National News Desk (KUTV), June 9, 2026",
                 "https://kutv.com/news/nation-world/greg-bovino-launches-a-committee-to-explore-a-2028-presidential-run-trump-administration-border-patrol-minneapolis",
                 "2026-06-09")
BOVINO_ROWS = [
    ("imm-02", -2, BOVINO("Bovino on X, launching his exploratory committee"),
     "My one and only priority is deporting the 106 million illegals who are here."),
]

# ---------------------------------------------------------------- Others

AYYADURAI = site("Shiva Ayyadurai’s 2026 U.S. Senate campaign (Massachusetts), Platform", "https://shiva4senate.com/platform/")
AYYADURAI_TERMS = "Term limits, ban insider trading, make every representative legally accountable to the people"
AYYADURAI_ROWS = [
    ("soc-01", 2, AYYADURAI("ending censorship"), "End censorship, protect medical freedom, and return science to the people"),
    ("gov-11", 1, AYYADURAI("lobbyists and billionaires out of government"), "Rip lobbyists and billionaires out of government"),
    ("eco-02", 2, AYYADURAI("tax cuts for families"), "Cut taxes for families and small business"),
    ("eco-08", 1, AYYADURAI("tax cuts for small business"), "Cut taxes for families and small business"),
    ("ene-04", 1, AYYADURAI("clean food, air and water"),
     "Clean Food, Clean Air, Clean Water – Ban poisons in food and agriculture, enforce honest labeling."),
    ("soc-08", 1, AYYADURAI("a Digital Bill of Rights"),
     "Digital Freedom & Privacy – A Digital Bill of Rights to protect your voice and your mind from censorship and manipulation"),
    ("gov-05", 2, AYYADURAI("voter ID"), "Paper ballots, hand-counting, same-day voting, Voter ID."),
    ("def-07", 1, AYYADURAI("no more wars abroad"), "No more trillion-dollar wars abroad."),
    ("def-08", -2, AYYADURAI("bringing troops home"), "Bring troops home and reinvest in communities’ health infrastructure."),
    ("def-12", -2, AYYADURAI("ending aid to Israel"), "Stop taxpayer subsidies to Israel and others."),
    ("def-10", 1, AYYADURAI("ending taxpayer subsidies abroad"), "Stop taxpayer subsidies to Israel and others."),
    ("gov-01", 2, AYYADURAI("term limits"), AYYADURAI_TERMS),
    ("gov-02", 1, AYYADURAI("banning insider trading"), AYYADURAI_TERMS),
]

LAPORTE = article("U.S. Term Limits, May 28, 2025", "https://termlimits.com/chase-laporte-pledges-to-support-term-limits-on-congress/", "2025-05-28")
LAPORTE_ROWS = [
    ("gov-01", 2, LAPORTE("LaPorte signed U.S. Term Limits’ pledge for a constitutional amendment limiting congressional terms (the pledge’s text)"),
     "I will cosponsor and vote for the U.S. Term Limits amendment of three (3) House terms and two (2) Senate terms"),
]

JORGENSEN = site("Jo Jorgensen exploratory campaign, announcement", "https://www.votejo28.com/")


def jo20(slug, title):
    return archived(f"Jo Jorgensen for President, {title} (2020 campaign site, Wayback Machine copy of Nov. 1, 2020)",
                    f"https://web.archive.org/web/20201101000000/https://jo20.com/issues/{slug}/", "2020-11-01")


JO_HEALTH, JO_ENV, JO_TRADE = jo20("healthcare", "Healthcare"), jo20("environment", "Environment"), jo20("trade-immigration", "Trade & Immigration")
JO_JUSTICE, JO_EDU = jo20("criminal-justice-reform", "Criminal Justice Reform"), jo20("education", "Education")
JO_PEACE, JO_TAX = jo20("neutrality-and-peace", "Neutrality and Peace"), jo20("taxes", "Taxes")
JORGENSEN_ROWS = [
    ("eco-07", 2, JORGENSEN("a government that lives within its means"), "We need a government that lives within its means."),
    ("def-07", 2, JORGENSEN("peace over intervention"),
     "We need leaders who understand that peace is wiser than intervention, that markets work better than mandates"),
    ("hea-01", -2, JO_HEALTH("against Medicare for All"),
     "Those who are dealing with serious ailments would be further victimized in a nationalized system such as the proposed “Medicare for All.”"),
    ("hea-04", 2, JO_HEALTH("price competition in health care"), "We can reduce the cost of health care 75% by allowing real price competition"),
    ("ene-02", 2, JO_ENV("nuclear power"),
     "replacing coal burning and oil burning powerplants in the United States with safe, non-polluting, high-tech nuclear powerplants"),
    ("ene-06", -1, JO_ENV("against the Green New Deal"), "This kind of legislation is neither rational nor workable."),
    ("eco-10", -2, JO_TRADE("ending tariffs"), "As President, I will use my Constitutional authority to eliminate trade barriers & tariffs"),
    ("agr-06", 2, JO_TRADE("free trade"), "I am the only free trade candidate for president."),
    ("imm-03", 2, JO_TRADE("repealing immigration quotas"),
     "work to repeal arbitrary quotas on the number of people who can legally enter the United States to work, visit, or reside"),
    ("soc-05", 2, JO_JUSTICE("ending the War on Drugs"),
     "I will also work with Congress to end the failed War on Drugs and other victimless crime laws."),
    ("edu-07", 2, JO_EDU("local control of schools, without the Department of Education"),
     "return control of education to where it belongs – with parents, teachers, and students"),
    ("def-08", -2, JO_PEACE("bringing troops home"), "Bring home our 200,000 plus American military personell stationed in foreign countries"),
    ("def-05", -2, JO_PEACE("no military aid abroad"), "no US military aid to foreign governments"),
    ("eco-02", 1, JO_TAX("lower taxes"), "let you keep what you earn"),
]


def yang(slug, title):
    return archived(f"Yang2020, {title} (2020 campaign site, Wayback Machine copy of Feb. 4, 2020)",
                    f"https://web.archive.org/web/20200204000000/https://www.yang2020.com/policies/{slug}/", "2020-02-04")


Y_HEALTH, Y_TRANS = yang("medicare-for-all", "Medicare for All"), yang("support-for-transgender-individuals", "Support for Transgender Individuals")
Y_FOSSIL, Y_RENEW = yang("fossil-fuels-their-days-are-over", "Fossil Fuels: Their Days Are Over"), yang("renewable-energy", "Renewable Energy")
Y_NUKE, Y_CU = yang("nuclear-energy", "Nuclear Energy"), yang("overturning-citizens-united", "Overturning Citizens United")
Y_RCV, Y_PATH = yang("rankedchoice", "Ranked Choice Voting"), yang("pathway-to-citizenship-2", "Pathway to Citizenship")
Y_BORDER, Y_SKILL = yang("southern-border-security", "Southern Border Security"), yang("enticing-high-skill-individuals", "Enticing High-Skill Individuals")
Y_POT, Y_CAM = yang("legalization-of-marijuana", "Legalization of Marijuana"), yang("every-cop-gets-camera", "Every Cop Gets a Camera")
Y_BAIL, Y_LEAVE = yang("cashbail", "Cash Bail"), yang("paid-family-leave", "Paid Family Leave")
Y_CARE, Y_TEACH = yang("guaranteed-childcare", "Guaranteed Childcare"), yang("teacher-salaries", "Teacher Salaries")
Y_CARBON, Y_ID = yang("carbon-fee-dividend", "Carbon Fee and Dividend"), yang("prohibit-voter-id-laws", "Prohibit Voter ID Laws")
Y_MAIL, Y_UNION = yang("early-voting-and-vote-by-mail", "Early Voting and Vote by Mail"), yang("empowering-unions-in-the-21st-century", "Empowering Unions")
Y_MAPS, Y_DOOR = yang("end-gerrymandering", "End Gerrymandering"), yang("stop-the-d-c-revolving-door", "Stop the D.C. Revolving Door")
Y_PRISON = yang("reduce-mass-incarceration", "Reduce Mass Incarceration")
YANG_ROWS = [
    ("hea-01", 2, Y_HEALTH("health care for everyone"), "Comprehensive healthcare for all Americans"),
    ("hea-02", 2, Y_HEALTH("negotiating drug prices"), "Control the cost of life-saving prescription drugs, through negotiating drug prices"),
    ("soc-12", 2, Y_TRANS("protecting transgender people"), "End the systemic threat and real violence against the trans community"),
    ("ene-03", -2, Y_FOSSIL("ending support for fossil fuel production"), "Stop federal contributions that promote fossil fuel production"),
    ("ene-01", 2, Y_RENEW("100% renewable energy"), "Convert to 100% renewable energy by 2049"),
    ("ene-02", 2, Y_NUKE("new nuclear reactors"),
     "Invest $50 billion in research and development for thorium-based molten salt reactors, and nuclear fusion reactors"),
    ("ene-06", 2, Y_CARBON("a carbon fee"), "Propose a carbon fee and dividend system"),
    ("gov-11", 2, Y_CU("less corporate influence on elections"), "Reduce corporate influence and outsize influence of the wealthy"),
    ("gov-13", -2, Y_CU("ending super PACs"), "Eliminate super PACs and vessels for corporate intervention in campaigns."),
    ("gov-07", 2, Y_RCV("ranked-choice voting"), "Work with Congress to adopt ranked-choice voting for all federal elections."),
    ("gov-05", -2, Y_ID("against voter ID laws"), "Direct the DOJ to prohibit all voter ID laws that disenfranchise underrepresented communities."),
    ("gov-06", 2, Y_MAIL("voting by mail"), "Give every voter the option to vote by mail"),
    ("gov-04", 2, Y_MAPS("independent redistricting"), "Promote the use of independent redistricting commissions"),
    ("gov-09", 2, Y_DOOR("ethics rules for officials"), "Restore the public’s trust in the motives of all government officials"),
    ("imm-02", 2, Y_PATH("permanent residency and an eighteen-year path to citizenship"),
     "Provide a new tier of long-term permanent residency for anyone who has been here for a substantial amount of time"),
    ("imm-01", 2, Y_BORDER("ports of entry"), "Increase funding to secure our landed ports of entry, where most drugs enter the United States."),
    ("imm-08", 1, Y_BORDER("customs enforcement"),
     "Increase funding to our Customs Enforcement teams that are tasked with preventing human trafficking"),
    ("imm-03", 2, Y_SKILL("visas for skilled workers"), "Enhance the H-1B visa program"),
    ("soc-05", 2, Y_POT("legal marijuana"),
     "Support the full legalization of marijuana at the federal level and remove it from the controlled substances list."),
    ("cri-02", 2, Y_CAM("body cameras"),
     "Authorize federal funding to pay for a body camera for every officer in every police department in the country."),
    ("cri-06", 2, Y_BAIL("less cash bail"), "Work with states to decrease their reliance on cash bail"),
    ("cri-08", 2, Y_PRISON("treatment over punishment"), "Shift drug policy away from punishment and towards treatment."),
    ("cri-05", 2, Y_PRISON("programs that reduce recidivism"),
     "Invest money to fund innovative prison programs that decrease recidivism and increase reintegration."),
    ("eco-11", 2, Y_LEAVE("six months of paid leave"), "Guarantee 6 months Paid Family Leave for all parents"),
    ("eco-09", 2, Y_UNION("the PRO Act"),
     "Work with Congress to pass the PRO Act to protect workers’ rights to organize and negotiate on a level playing field."),
    ("soc-07", 2, Y_CARE("affordable child care"), "Make childcare affordable for all families"),
    ("edu-04", 2, Y_TEACH("teacher pay"), "Work with states to fund their educational systems to improve teacher salaries"),
]

PEOPLE = {
    "Kamala_Harris": HARRIS_ROWS,
    "Gavin_Newsom": NEWSOM_ROWS,
    "Gretchen_Whitmer": WHITMER_ROWS,
    "Andy_Beshear": BESHEAR_ROWS,
    "Pete_Buttigieg": BUTTIGIEG_ROWS,
    "Rahm_Emanuel": EMANUEL_ROWS,
    "Ron_DeSantis": DESANTIS_ROWS,
    "JD_Vance": VANCE_ROWS,
    "Mike_Pence": PENCE_ROWS,
    "Chris_Christie": CHRISTIE_ROWS,
    "Dan_Greaney": GREANEY_ROWS,
    "Royce_White": WHITE_ROWS,
    "Gregory_Bovino": BOVINO_ROWS,
    "Shiva_Ayyadurai": AYYADURAI_ROWS,
    "Chase_LaPorte": LAPORTE_ROWS,
    "Jo_Jorgensen": JORGENSEN_ROWS,
    "Andrew_Yang": YANG_ROWS,
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
    out = {"updated": READ, "note": "Hand research for the 2028 presidential field (scripts/research/president_2028.py)",
           "people": people}
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    n = sum(len(p["positions"]) for p in people.values())
    print(f"wrote {OUT.relative_to(ROOT).as_posix()}: {len(people)} people, {n} positions")


if __name__ == "__main__":
    main()
