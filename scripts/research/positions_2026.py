"""More sourced positions for candidates who had few or none: what their campaign
sites' issue pages say, and what news coverage reports they would do. Writes
data/research/positions.json, which update_races.py pools with the other research
by question. A position is recorded only where the candidate or the coverage states
it; nothing is inferred from party. Researched Oct. 25, 2026.

    py scripts/research/positions_2026.py
"""

from common import P, article, page, write

READ = "2026-10-25"


def site(title, url):
    """One page of a campaign site, read on READ. Each call names the section."""
    return lambda note: page(f"{title}: {note}", url, READ)


def cand(cid, name, official, *rows):
    c = {"id": cid, "name": name, "positions": P(*rows)}
    if official:
        c["officialSite"] = official
    return c


# West Virginia Senate
WV_ISSUES = site("Rachel Fetty Anderson campaign site, Issues", "https://www.fettyandersonforsenate.com/issues")
WV_PLATFORM = site("Rachel Fetty Anderson campaign site, Platform", "https://www.fettyandersonforsenate.com/platform")
WV_WATCH = article("West Virginia Watch, May 12, 2026", "https://westvirginiawatch.com/2026/05/12/capito-easily-secures-gop-nomination-for-u-s-senate-seat-tuesday-shortly-after-polls-close-in-wv/", "2026-05-12")

# New York governor
NY_BUDGET25 = article("Office of Gov. Kathy Hochul, budget agreement, Apr. 28, 2025", "https://www.governor.ny.gov/news/governor-hochul-announces-agreement-fy-2026-state-budget", "2025-04-28")
NY_AFFORD26 = article("Office of Gov. Kathy Hochul, Jan. 13, 2026", "https://www.governor.ny.gov/news/money-your-pockets-governor-hochul-unveils-new-initiatives-make-new-york-more-affordable", "2026-01-13")
NY_MAID = article("Office of Gov. Kathy Hochul, Feb. 6, 2026", "https://www.governor.ny.gov/news/governor-hochul-signs-medical-aid-dying-act-new-york-state-law", "2026-02-06")
NY_POLITICO = article("Politico (via Yahoo News), Jan. 13, 2026", "https://www.yahoo.com/news/articles/hochul-agenda-blends-trump-fighting-105500029.html", "2026-01-13")
NY_FOX5 = article("FOX 5 New York debate report, Oct. 14, 2026", "https://www.fox5ny.com/news/hochul-blakeman-debate-ny-governor-race", "2026-10-14")

# Idaho Senate
ID_ACH = site("Todd Achilles campaign site, Policies", "https://www.achillesforidaho.com/policies")

# Maryland governor
MD_COX = site("Dan Cox campaign site, Issues", "https://dancoxforgovernor.com/issues/")
MD_MOORE = site("Wes Moore campaign site, Accomplishments", "https://wesmoore.com/accomplishments/")
MD_CBS = article("CBS Baltimore, Jan. 20, 2025", "https://www.cbsnews.com/baltimore/news/maryland-abortion-access-reproductive-rights-amendment-election/", "2025-01-20")
MD_GOV23 = article("Office of Gov. Wes Moore, Sept. 4, 2023", "https://governor.maryland.gov/news/press-releases/governor-moore-proclaims-labor-day-maryland", "2023-09-04")
MD_WYPR = article("WYPR, Jan. 16, 2025", "https://www.wypr.org/wypr-news/2025-01-16/maryland-governor-proposes-tax-on-top-earners-but-also-tax-cuts", "2025-01-16")

# Wyoming: WyoFile's questionnaire, answered in June 2026 and published unedited
WY_BYRD = article("WyoFile 2026 Election Guide, James Byrd’s questionnaire", "https://projects.wyofile.com/election-guide-2026/candidates/byrd-james/", "2026-07-02")
WY_BARLOW = article("WyoFile 2026 Election Guide, Eric Barlow’s questionnaire", "https://projects.wyofile.com/election-guide-2026/candidates/barlow-eric/", "2026-07-02")

# Colorado: the candidates' answers to Colorado Politics' governor questionnaire, and
# Mark Baisley's campaign site
CO_QUEST = article("Colorado Politics voter guide, candidates’ questionnaire answers, Oct. 2, 2026", "https://www.coloradopolitics.com/2026/10/02/colorado-governor-weiser-marx-and-lopez-vie-for-top-state-seat-4/", "2026-10-02")
CO_BAISLEY = site("Mark Baisley campaign site, Issues", "https://baisleyforsenate.com/issues/")
CO_BAISLEY_FARM = article("Mark Baisley campaign, Farm Prosperity proposal, Sept. 14, 2026", "https://baisleyforsenate.com/2026/09/14/farm-prosperity-proposal/", "2026-09-14")
CO_CHEW = site("Bob Chew campaign site, Issues", "https://bobchew2026.com/issues/")

# South Dakota Senate
SD_DNN = article("Dakota News Now, Sept. 22, 2026", "https://www.dakotanewsnow.com/2026/09/22/inside-race-rounds-bengs-talk-senate-priorities-ahead-november-election/", "2026-09-22")
SD_SEARCHLIGHT = article("South Dakota Searchlight, May 2, 2025", "https://southdakotasearchlight.com/2025/05/02/musk-doge-cuts-motivate-former-u-s-senate-candidate-to-run-again/", "2025-05-02")

# Delaware and Illinois Senate
DE_WDEL = article("WDEL, Aug. 17, 2026", "https://www.wdel.com/news/electionwatch-dr-michael-katz-republican-for-u-s-senate/article_e0a61247-0467-423b-85b7-04ec354033a3.html", "2026-08-17")
IL_WTTW = article("WTTW forum report, Oct. 20, 2026", "https://news.wttw.com/2026/10/20/stratton-tracy-face-lone-forum-over-immigration-tariffs-and-minimum-wage", "2026-10-20")
IL_CNI = article("Capitol News Illinois forum report, Oct. 21, 2026", "https://capitolnewsillinois.com/news/stratton-tracy-clash-over-trump-affordability-in-lone-u-s-senate-forum/", "2026-10-21")
IL_BAILEY = site("Darren Bailey campaign site, Issues", "https://baileyforillinois.com/issues/")

# New Mexico governor
NM_AP = article("Associated Press (via Yahoo News), Oct. 17, 2025", "https://www.yahoo.com/news/articles/first-republican-enters-race-governor-222156907.html", "2025-10-17")
NM_HAALAND = site("Deb Haaland campaign site, Deb’s Plan", "https://debhaaland.com/debsplans/")

# Idaho governor
ID_SUN = article("Idaho Capital Sun, Feb. 24, 2026", "https://idahocapitalsun.com/2026/02/24/idaho-gov-brad-little-announces-reelection-campaign/", "2026-02-24")
ID_LITTLE_Q = "We delivered historic tax relief and made record investments in schools, public safety, and infrastructure to protect our exceptional quality of life."

# Rhode Island governor
RI_NBC10 = article("NBC 10 debate report, Oct. 20, 2026", "https://turnto10.com/politics/foulkes-guckian-and-block-debate-housing-health-care-in-final-televised-matchup-october-20-2026", "2026-10-20")

# Oklahoma and Rhode Island Senate
OK_THOMAS = site("N’Kiyla Jasmine Thomas campaign site, Policies", "https://www.jasmineforok.com/policies")
OK_KOSU = article("KOSU interview (via Oklahoma Voice), July 31, 2026", "https://oklahomavoice.com/2026/07/31/democrat-jasmine-thomas-hopes-lived-experience-will-propel-her-to-oklahoma-senate-seat/", "2026-07-31")
OK_NONDOC = article("NonDoc, July 17, 2026", "https://nondoc.com/2026/07/17/u-s-senate-runoff-democrats-nkiyla-jasmine-thomas-jim-priest-clash-over-electability-identity/", "2026-07-17")
RI_MCKAY = site("Ray McKay campaign site, Right Direction", "https://www.mckayforussenate.com/right-direction/")

# Delaware and Alabama Senate; Arkansas and Maine governor
DE_KATZ = site("Mike Katz campaign site, Platform", "https://drmikekatz.com/platform")
DE_KATZ_REC = site("Mike Katz campaign site, Record", "https://drmikekatz.com/record")
AL_REFLECTOR = article("Alabama Reflector, June 16, 2026", "https://alabamareflector.com/2026/06/16/barry-moore-wins-alabama-gop-nomination-for-u-s-senate-seat/", "2026-06-16")
AR_LOVE = site("Fred Love campaign site, Issues", "https://www.fredlove.com/issues")
AR_SANDERS = site("Sarah Huckabee Sanders campaign site, Meet Sarah", "https://www.sarahforgovernor.com/about/")
ME_CHARLES = site("Bobby Charles campaign site, Issues", "https://www.bobbyformaine.com/issues")
NY_BLAKEMAN = site("Bruce Blakeman campaign site", "https://www.blakemanfornewyork.com/")
SD_RHODEN = site("Larry Rhoden campaign site, Accomplishments", "https://governorlarryrhoden.com/accomplishments")
TN_GREEN = site("Jerri Green campaign site, Platform", "https://greenforgovernor.com/policy/")
TN_GREEN_ABOUT = site("Jerri Green campaign site, Meet Jerri", "https://greenforgovernor.com/about/")
RI_GUCKIAN = site("Aaron Guckian campaign site, Five Core Pillars", "https://www.aaronforri.com/")
RI_FOULKES = site("Helena Foulkes campaign site, Plans (plan titles)", "https://helenafoulkes.com/plans/")
CA_HILTON = site("Steve Hilton campaign site, Policies (policy titles)", "https://stevehiltonforgovernor.com/policies")
OK_MAZZEI = site("Mike Mazzei campaign site, The Plan", "https://mikeforok.com/the-plan/")
OK_MAZZEI_ISSUES = site("Mike Mazzei campaign site, The Issues", "https://mikeforok.com/the-issues/")
MA_HEALEY = site("Maura Healey campaign site, Accomplishments", "https://maurahealey.com/accomplishments/")
MA_HEALEY_ABOUT = site("Maura Healey campaign site, Meet Maura", "https://maurahealey.com/meet-maura/")
AK_BRONSON = site("Dave Bronson campaign site", "https://www.davebronson.com/")
AK_BRONSON_ABOUT = site("Dave Bronson campaign site, About Dave", "https://www.davebronson.com/about-dave")
AR_SHOFFNER = site("Hallie Shoffner campaign site, Priorities", "https://www.hallieshoffner.com/platform")
OR_SMITH = site("David Brock Smith campaign site, Issues", "https://www.davidbrocksmithfororegon.com/issues")
VA_MIZUSAWA = site("Bert Mizusawa campaign site, Where I Stand", "https://bertforsenate.com/issues")
HI_CB = article("Honolulu Civil Beat candidate Q&A, July 20, 2026", "https://www.civilbeat.org/2026/07/candidate-qa-governor-josh-green-2/", "2026-07-20")
HI_GREEN_COST = site("Josh Green campaign site, Cost of Living", "https://joshgreenforhawaii.com/issues/cost-of-living/")
HI_GREEN_HOUSING = site("Josh Green campaign site, Affordable Housing", "https://joshgreenforhawaii.com/issues/affordable-housing/")
HI_GREEN_HEALTH = site("Josh Green campaign site, Healthcare", "https://joshgreenforhawaii.com/issues/healthcare/")
HI_GREEN_CLIMATE = site("Josh Green campaign site, Climate Change and Environment", "https://joshgreenforhawaii.com/issues/climate/")
HI_GREEN_ABOUT = site("Josh Green campaign site, Meet Josh", "https://joshgreenforhawaii.com/about/")
RI_BLOCK = site("Ken Block campaign site, Issues & Policies", "https://www.blockforgovernor.com/issues.php")
SC_WILSON = site("Alan Wilson campaign site, Conservative Priorities", "https://wilsonforsc.com/priorities/")
SC_JOHNSON = site("Jermaine Johnson campaign site, Policies", "https://johnsonforsc.com/policies")
SC_WPDE = article("WPDE (via ABC News 4), Sept. 23, 2026", "https://abcnews4.com/news/state/democratic-gubernatorial-candidate-jermaine-johnson-campaigns-in-horry-county-state-politics-south-carolina-department-of-transportation-general-election", "2026-09-23")
CO_MARX = site("Victor Marx campaign site, My Priorities", "https://www.victor2026.com/my-policies")
ID_LITTLE_ACC = site("Brad Little campaign site, Accomplishments", "https://www.bradlittleforidaho.com/accomplishments/")
SD_BENGS = site("Brian Bengs campaign site, Handshake With South Dakotans", "https://bengsforsouthdakota.com/policy-positions/")
SD_BENGS_STAND = site("Brian Bengs campaign site, What I Stand For", "https://bengsforsouthdakota.com/what-i-stand-for/")
WY_BYRD_SITE = site("James Byrd campaign site, Issues", "https://www.byrdforsenate.com/blank")
WY_BARLOW_SITE = site("Eric Barlow campaign site, Positions", "https://www.barlowforwyo.com/positions")
WY_WPM = article("Wyoming Public Media, June 2, 2026", "https://www.wyomingpublicmedia.org/politics-government/2026-06-02/kenneth-casner-is-the-lone-democrat-running-for-governor", "2026-06-02")
WY_YWL = article("Your Wyoming Link, Aug. 17, 2026", "https://www.yourwyominglink.com/news/local/the-people-are-the-party-ken-casners-priorities-in-the-governor-race/article_ab23228c-4665-4052-89f4-f416917fa812.html", "2026-08-17")

# Connecticut governor: Ned Lamont's campaign pages
CT_PRI = site("Ned Lamont campaign site, Priorities", "https://www.nedlamont.com/priorities")
CT_ACC = site("Ned Lamont campaign site, Accomplishments", "https://www.nedlamont.com/accomplishments")
CT_WINS = site("Ned Lamont campaign site, Progressive Wins", "https://www.nedlamont.com/progressive-wins")

# California governor: one page per priority on Xavier Becerra's site
def CA(slug, title):
    return site(f"Xavier Becerra campaign site, {title}", f"https://www.xavierbecerra2026.com/priorities/{slug}/")

# Kentucky Senate: one page per policy on Charles Booker's site
def KY(slug, title):
    return site(f"Charles Booker campaign site, {title}", f"https://charlesbookerky.org/policies/{slug}")

races = [
    {"id": "WV-SEN", "candidates": [cand(
        "WV-SEN:anderson", "Rachel Fetty Anderson", "https://www.fettyandersonforsenate.com/",
        ("hea-01", 2, WV_WATCH("Fetty Anderson said she would support Medicare for All legislation"), None),
        ("hea-03", 2, WV_ISSUES("Healthcare"), "We must invest in Medicare, Medicaid and Tricare to allow all Americans to benefit in real time from the healthcare taxpayers invest in."),
        ("hea-04", -1, WV_ISSUES("Healthcare"), "To eliminate the effect of perverse profit incentives to deny care recommended by treating physicians, the government must divest from obsolete non-provider corporations"),
        ("hea-09", 2, WV_ISSUES("Vaccines"), "I support full vaccination for children before starting school."),
        ("soc-03", 2, WV_WATCH("Fetty Anderson said she would support restoring the right to abortion"), None),
        ("soc-02", 2, WV_ISSUES("Women’s Rights"), "We support full equality, nationwide, for women and support the adoption of the Equal Rights Amendment that bans discrimination based on sex."),
        ("soc-01", 2, WV_ISSUES("Free Speech"), "Free speech is the birthplace of liberty and must be protected."),
        ("soc-05", 2, WV_ISSUES("Marijuana"), "Adults should be permitted to grow marijuana for their own use."),
        ("soc-07", 1, WV_ISSUES("Social Security"), "Support programs for new parents, including paid leave and investments in child care access"),
        ("soc-08", 1, WV_ISSUES("Technology"), "The government must not sacrifice the privacy, welfare, health, safety and art of its constituents and citizens to technocrats or speculative technologies."),
        ("eco-01", 2, WV_ISSUES("Taxation"), "the increase of the marginal tax rate of earners of over $500,000.00 per year"),
        ("eco-12", 1, WV_ISSUES("Taxation"), "The American tax and resource burden must be fairly and equitably distributed among our economy's beneficiaries and participants"),
        ("eco-04", 1, WV_ISSUES("Agriculture"), "The American government must intervene to protect the American farmer from market instability, foreign takeovers of land and resources and monopolization by industries"),
        ("eco-06", 1, WV_ISSUES("Infrastructure"), "Equitable infrastructure development is the investment that West Virginia needs in its economy and workforce."),
        ("eco-09", 2, WV_ISSUES("Economy"), "Free speech and the right to unionize for better pay and working conditions must not be interfered with"),
        ("eco-11", 1, WV_ISSUES("Social Security"), "Support programs for new parents, including paid leave and investments in child care access"),
        ("edu-03", 1, WV_ISSUES("Social Security"), "Increase investments in educational programs for displaced and disabled workers"),
        ("imm-03", 1, WV_ISSUES("Social Security"), "Encourage migration of professional workers into the United States, particularly medical professionals"),
        ("agr-01", 2, WV_ISSUES("Agriculture"), "The American government must intervene to protect the American farmer from market instability"),
        ("ene-01", 1, WV_ISSUES("Energy"), "The government must encourage investment in sustainable energy sources that minimally affect the environment"),
        ("ene-04", 2, WV_ISSUES("Environment"), "We must fight to demand that protections for our precious natural resources be restored and extended."),
        ("hou-09", 1, WV_ISSUES("Infrastructure"), "In the country where the internet was developed, Americans everywhere deserve the best internet resources."),
        ("gov-09", 2, WV_PLATFORM("I will keep your tax dollars safe"), "I will demand disclosure of all gifts, investments, profits, benefits or payments over $50.00 from the same person or entity to the elected person"),
        ("gov-11", 2, WV_ISSUES("Campaign Funding (Citizens United)"), "Candidates should not be allowed to take money from foreign governments or corporations."),
        ("gov-12", 1, WV_PLATFORM("I will keep your tax dollars safe"), "I will demand accountability for American funds and assets to ensure they are spent in a Constitutional manner requiring audits of the Defense department"),
        ("gov-13", -2, WV_ISSUES("Campaign Funding (Citizens United)"), "Candidates should not be allowed to take money from foreign governments or corporations."),
        ("def-02", 1, WV_ISSUES("International Relations"), "It is in the best interest of the American people to encourage and maintain alliances with other countries that share our values"),
        ("def-03", 2, WV_ISSUES("Military"), "To our veterans we owe their prioritization in budgeting, healthcare and services."),
        ("def-04", 2, WV_ISSUES("War"), "No troops should ever be placed in harm's way without the approval of Congress."),
        ("def-07", 2, WV_ISSUES("War"), "US military power should be reserved for self-defense."),
        ("def-12", 0, WV_ISSUES("Israel and Palestine"), "I would not vote to send or sell weapons to any country except for purely self-defense."))]},
    {"id": "NY-GOV", "candidates": [cand(
        "NY-GOV:hochul", "Kathy Hochul", None,
        ("soc-09", 2, NY_MAID("Hochul signed the Medical Aid in Dying Act into law"), "which includes the right for the terminally ill to peacefully and comfortably end their lives with dignity and compassion"),
        ("soc-07", 2, NY_BUDGET25("the budget Hochul negotiated expands child care funding"), "Expanding access to child care by investing $2.2 billion statewide"),
        ("edu-09", 2, NY_BUDGET25("the budget Hochul negotiated makes school meals free for every student"), "Providing $340 million to ensure free breakfast and lunch for every K-12 student in New York"),
        ("edu-03", 1, NY_BUDGET25("free community college for adults in high-demand fields"), "Investing $47 million to make community college free for adult students pursuing associate degrees in certain high-demand industries"),
        ("eco-02", 2, NY_BUDGET25("a middle-class income tax cut"), "A $1 billion tax cut for middle-class and low-income New Yorkers"),
        ("eco-01", -1, NY_POLITICO("Hochul is resisting a push to raise taxes on rich New Yorkers"), None),
        ("cri-01", 1, NY_BUDGET25("state money for police on overnight subway trains"), "investing $77 million for police officers on every overnight subway train"),
        ("hou-02", 1, NY_BUDGET25("a 90-day ban on private equity home purchases"), "Leveling the playing field for homebuyers by banning private equity purchases within the first 90 days a home is on the market"),
        ("hou-06", 1, NY_AFFORD26("tougher penalties for landlords who harass rent-regulated tenants"), "stiffer criminal penalties for landlords who engage in systematic harassment of rent regulated tenants"),
        ("sta-03", 2, NY_AFFORD26("Hochul raised the state minimum wage and tied it to inflation"), "Raised New York’s minimum wage and tied future increases to inflation so a day’s work covers a day’s needs"),
        ("ene-01", 1, NY_POLITICO("Hochul is pressing to expand wind energy"), None),
        ("agr-01", 1, NY_POLITICO("Hochul plans $30 million in direct payments to farmers hurt by tariffs"), None)),
        cand("NY-GOV:blakeman", "Bruce Blakeman", "https://www.blakemanfornewyork.com/",
             ("imm-09", 1, NY_FOX5("Blakeman said he supports a guest worker program"), "I believe in a guest worker program for immigrants."),
             ("sta-08", 2, NY_BLAKEMAN("Blakeman’s Nassau success story"), "As County Executive, Bruce Blakeman hired 600 new Police and Law Enforcement Officers to keep Nassau families safe"),
             ("sta-04", 2, NY_BLAKEMAN("No Property Tax Increases"), "Bruce Blakeman eliminated $150 million in property tax hikes scheduled by his predecessor."))]},
    {"id": "SD-GOV", "candidates": [cand(
        "SD-GOV:rhoden", "Larry Rhoden", "https://governorlarryrhoden.com/",
        ("sta-07", 2, SD_RHODEN("Investing in the Workforce"), "Invested in technical colleges through the Build Dakota Scholarship, tech college expansions, and apprenticeships."),
        ("sta-09", 1, SD_RHODEN("Rural Health Transformation Program"), "Delivered $189 million in federal funds to bring more services to rural and remote areas."),
        ("edu-06", 1, SD_RHODEN("Improving Education Outcomes"), "opted into Trump's school choice opportunity"),
        ("imm-08", 2, SD_RHODEN("Immigration Enforcement"), "Banned sanctuary cities and signed ICE agreements with Highway Patrol and Department of Corrections."),
        ("soc-04", 2, SD_RHODEN("Right to Life"), "Stopped harmful abortion pills from coming into South Dakota, protecting babies and moms."),
        ("soc-06", 1, SD_RHODEN("Freedom to Worship"), "Delivered a bill to guarantee South Dakotans will not come under assault at their place of worship."),
        ("cri-05", 1, SD_RHODEN("Correctional Rehabilitation Task Force"), "Started a task force that has advanced faith-based and tribal-focused rehabilitation efforts."))]},
    {"id": "TN-GOV", "candidates": [cand(
        "TN-GOV:green", "Jerri Green", "https://greenforgovernor.com/",
        ("eco-09", 2, TN_GREEN("An Economy That Works for Working Families"), "Support labor rights and collective bargaining"),
        ("eco-11", 2, TN_GREEN("An Economy That Works for Working Families"), "Expand paid family and medical leave"),
        ("sta-03", 1, TN_GREEN("What I Stand For"), "Paid family leave. Affordable child care. A real living wage."),
        ("hou-01", 2, TN_GREEN("An Economy That Works for Working Families"), "Increase funding for affordable housing"),
        ("sta-07", 1, TN_GREEN("An Economy That Works for Working Families"), "Promote workforce development and vocational training"),
        ("soc-07", 2, TN_GREEN("An Economy That Works for Working Families"), "Make quality childcare more accessible and affordable"),
        ("sta-12", 2, TN_GREEN("An Economy That Works for Working Families"), "Prioritize passenger rail across the state to connect major metropolitan hubs"),
        ("edu-04", 2, TN_GREEN("Public Education That Works for All"), "Raise teacher pay and restore respect to the profession"),
        ("hea-03", 2, TN_GREEN("Health Care as a Right, Not a Luxury"), "Expand Medicaid to cover more working families and keep rural hospitals open"),
        ("hea-06", 1, TN_GREEN("Health Care as a Right, Not a Luxury"), "Invest in mental health services and addiction recovery"),
        ("soc-03", 2, TN_GREEN("Health Care as a Right, Not a Luxury"), "Defend reproductive freedom and the right to choose"),
        ("soc-05", 2, TN_GREEN("Health Care as a Right, Not a Luxury"), "Legalize marijuana medicinally and recreationally to increase treatment options for people with chronic illnesses and decrease reliance on opioids"),
        ("imm-08", -1, TN_GREEN("Our Day One Plan"), "Stop the cooperation between the Tennessee Highway Patrol and ICE to protect our immigrant neighbors from state-sponsored harassment."),
        ("agr-01", 1, TN_GREEN("A Future Farmers Can Count On"), "Provide targeted relief for small and midsized family farms — not corporate agribusiness"),
        ("sta-01", 1, TN_GREEN("A Future Farmers Can Count On"), "Invest in rural infrastructure, including roads, broadband, and water systems so that farmers can grow, sell, and compete"),
        ("hou-09", 1, TN_GREEN("A Future Farmers Can Count On"), "Invest in rural infrastructure, including roads, broadband, and water systems so that farmers can grow, sell, and compete"),
        ("sta-08", 1, TN_GREEN_ABOUT("Proven Leadership That Delivers"), "Increased funding for first responders, including police officers and firefighters"),
        ("cri-05", 1, TN_GREEN_ABOUT("Proven Leadership That Delivers"), "Started programs to make jobs more accessible to ex-offenders to help reduce crime"))]},
    {"id": "ID-SEN", "candidates": [cand(
        "ID-SEN:achilles", "Todd Achilles", "https://www.achillesforidaho.com/",
        ("gov-01", 2, ID_ACH("Stop Corruption in Congress"), "I will fight for a constitutional amendment to limit the terms of members of the Senate, the House of Representatives, and the Supreme Court."),
        ("gov-02", 2, ID_ACH("Stop Corruption in Congress"), "Members of Congress should not be allowed to trade individual stocks. Period."),
        ("gov-04", 1, ID_ACH("Stop Corruption in Congress"), "Politicians cannot be allowed to choose their voters. I will work to end the manipulation of electoral district boundaries (gerrymandering) by long-tenured politicians."),
        ("gov-09", 2, ID_ACH("Stop Corruption in Congress"), "I support a five-year ban on members of Congress becoming registered lobbyists after leaving office."),
        ("gov-11", 2, ID_ACH("Stop Corruption in Congress"), "I support a ban on companies with government contracts from donating to federal candidates."),
        ("gov-13", -2, ID_ACH("Stop Corruption in Congress"), "I support the right of states to prohibit corporate money in elections so billion-dollar corporations can't buy influence in Washington."),
        ("eco-02", 1, ID_ACH("Give Working Families a Fighting Chance"), "I will work to lower taxes for working families, small businesses, and ag producers."),
        ("eco-08", 1, ID_ACH("Give Working Families a Fighting Chance"), "I will work to lower taxes for working families, small businesses, and ag producers."),
        ("eco-12", 1, ID_ACH("Reduce the National Debt"), "I will work to close tax loopholes that American elite and corporations abuse."),
        ("eco-07", 1, ID_ACH("Reduce the National Debt"), "Congress must make responsible spending decisions while ensuring everyone plays by the same rules."),
        ("eco-04", 2, ID_ACH("Make Healthcare & Housing Affordable Again"), "I support strengthening antitrust enforcement to block healthcare mergers that raise costs or reduce patient choice."),
        ("eco-09", 1, ID_ACH("Give Working Families a Fighting Chance"), "I support banning predatory non-compete agreements that prevent workers from advancing their careers"),
        ("hea-06", 1, ID_ACH("Defend the Second Amendment"), "I will work to ensure that crisis mental health support is available 24 hours a day, 7 days a week, 365 days a year"),
        ("hou-02", 1, ID_ACH("Make Healthcare & Housing Affordable Again"), "The bipartisan 21st Century ROAD to Housing Act made meaningful progress toward increasing housing supply and limiting large institutional investors from buying up single-family homes."),
        ("hou-04", 1, ID_ACH("Make Healthcare & Housing Affordable Again"), "I will work to increase housing supply by promoting legislation that rewards cities for building more housing"),
        ("hou-05", 1, ID_ACH("Make Healthcare & Housing Affordable Again"), "creates more financing options for first-time homebuyers"),
        ("soc-03", 1, ID_ACH("Stop Government Intrusion into Our Private Lives"), "I support Idaho’s Reproductive Freedom and Privacy Act ballot initiative."),
        ("soc-06", 1, ID_ACH("Stop Government Intrusion into Our Private Lives"), "I will defend every Idahoan's freedom to practice their faith, build their family, marry the person they love, make private healthcare decisions"),
        ("soc-10", 1, ID_ACH("Stop Government Intrusion into Our Private Lives"), "I will defend every Idahoan's freedom to practice their faith, build their family, marry the person they love, make private healthcare decisions"),
        ("soc-08", 2, ID_ACH("Internet Privacy & AI"), "All Americans should have data freedom — the right to control their personal information and demand its deletion."),
        ("edu-03", 1, ID_ACH("Strengthen Public Schools"), "I support greater investment in career and technical education"),
        ("imm-09", 1, ID_ACH("Support Idaho Agriculture"), "I will support cross-partisan efforts to modernize agricultural workforce programs so Idaho producers have access to a reliable, legal workforce"),
        ("agr-01", 1, ID_ACH("Support Idaho Agriculture"), "I will protect crop insurance and the Farm Bill programs Idaho producers rely on"),
        ("agr-08", 1, ID_ACH("Support Idaho Agriculture"), "I will support agricultural research, innovation, and science-based regulation"),
        ("def-03", 1, ID_ACH("End Endless Wars and Support Our Veterans"), "I will work to ensure the Department of Veterans Affairs is properly funded and accountable"),
        ("def-04", 2, ID_ACH("End Endless Wars and Support Our Veterans"), "I will fight to reassert Congress' constitutional authority over decisions of war and peace"),
        ("def-07", 1, ID_ACH("End Endless Wars and Support Our Veterans"), "I will work to break America's cycle of endless wars that do not advance our national interests."))]},
    {"id": "KY-SEN", "candidates": [cand(
        "KY-SEN:booker", "Charles Booker", "https://charlesbookerky.org/",
        ("eco-02", 2, KY("affordable", "Making Life More Affordable")("tax cuts"), "I will cut taxes for working and middle-class families"),
        ("eco-09", 2, KY("affordable", "Making Life More Affordable")("unions"), "defend workers' freedom to organize for better wages and benefits"),
        ("eco-10", -2, KY("affordable", "Making Life More Affordable")("tariffs"), "Blanket tariffs fueling trade wars are hidden taxes."),
        ("eco-04", 1, KY("small-business", "Growing Kentucky Small Businesses")("corporate consolidation"), "Stand up to corporate consolidation and junk fees that let giant chains undercut local businesses."),
        ("eco-06", 1, KY("infrastructure", "Building Kentucky’s Infrastructure")("water systems"), "Upgrade drinking water and wastewater systems so no Kentucky family has to boil its water."),
        ("hea-01", 1, KY("healthcare", "Making Healthcare Affordable for All Kentuckians")("coverage"), "I believe healthcare is a human right."),
        ("hea-02", 2, KY("seniors", "Supporting Older Kentuckians & Retirees")("drug prices"), "Lowering Medicare prescription costs by making permanent the Medicare Drug Price Negotiation Program."),
        ("hea-03", 2, KY("healthcare", "Making Healthcare Affordable for All Kentuckians")("public option"), "Supporting the State Public Option Act that would build on our successful expansion of Medicaid in Kentucky"),
        ("hea-07", 2, KY("healthcare", "Making Healthcare Affordable for All Kentuckians")("ACA subsidies"), "Restoring the Affordable Care Act subsidies that Andy Barr voted to eliminate"),
        ("hea-10", 2, KY("seniors", "Supporting Older Kentuckians & Retirees")("Medicare benefits"), "Adding oral health, vision, and hearing coverage into traditional Medicare to match popular private Medicare Advantage offerings."),
        ("soc-03", 1, KY("healthcare", "Making Healthcare Affordable for All Kentuckians")("reproductive care"), "Choices about pregnancy, contraception, IVF and miscarriage care belong to women, their families and their doctors, not Washington."),
        ("soc-02", 1, KY("safety", "Keeping Kentucky Communities Safe")("discrimination"), "Protect every Kentuckian from discrimination and harassment, no matter who they are or whom they love."),
        ("cri-01", 1, KY("safety", "Keeping Kentucky Communities Safe")("police funding"), "Support local police, sheriffs and first responders with funding for training, recruitment and mental health crisis response teams."),
        ("cri-05", 1, KY("safety", "Keeping Kentucky Communities Safe")("reentry"), "Help people returning home from incarceration find work and housing so they stay home for good."),
        ("cri-07", 1, KY("safety", "Keeping Kentucky Communities Safe")("violence prevention"), "Invest in proven violence prevention, youth programs and job training that keep young people on the right path."),
        ("edu-03", 2, KY("young", "Supporting Young Kentuckians")("apprenticeships"), "Expanding registered apprenticeships with union and industry partners so young people can earn while they learn a trade."),
        ("edu-04", 2, KY("education", "Supporting Public Education & Teachers")("teacher pay"), "strengthen the educator pipeline by raising teacher pay, improving working conditions, and enhancing professional resources."),
        ("edu-05", 1, KY("young", "Supporting Young Kentuckians")("student debt"), "eliminating student debt for public servants and Kentuckians who go into public service"),
        ("edu-06", -2, KY("education", "Supporting Public Education & Teachers")("vouchers"), "Opposing efforts to divert public funding away from public schools toward private school vouchers."),
        ("hou-05", 1, KY("young", "Supporting Young Kentuckians")("first homes"), "Propose First-Time Buyer Credits for down-payment assistance for young and first-generation homebuyers."),
        ("hou-08", 2, KY("infrastructure", "Building Kentucky’s Infrastructure")("roads and bridges"), "Fight for federal dollars to repair Kentucky’s roads and bridges"),
        ("hou-09", 2, KY("infrastructure", "Building Kentucky’s Infrastructure")("broadband"), "Finish the job on rural broadband so every home, farm and small business can get online."),
        ("hou-10", 1, KY("infrastructure", "Building Kentucky’s Infrastructure")("flood resilience"), "Strengthen flood and disaster resilience in Eastern and Western Kentucky communities hit repeatedly by storms."),
        ("ene-08", 1, KY("infrastructure", "Building Kentucky’s Infrastructure")("flood resilience"), "Strengthen flood and disaster resilience in Eastern and Western Kentucky communities hit repeatedly by storms."),
        ("ene-01", 1, KY("energy", "Lowering Energy Costs & Standing with Energy Workers")("renewable power"), "the Energy Bills Relief Act, which lets cheaper renewable power move between states to lower monthly bills"),
        ("ene-10", 1, KY("energy", "Lowering Energy Costs & Standing with Energy Workers")("all of the above"), "Support an all-of-the-above energy strategy that keeps Kentucky plants running, keeps power affordable and creates new energy jobs here at home."),
        ("agr-01", 1, KY("farmers", "Supporting Kentucky’s Farmers")("farm aid"), "I will support the $12 billion farm aid package currently stalled in the U.S. Senate and a new farm bill that puts our farmers first."),
        ("gov-01", 2, KY("swamp", "Fighting Corruption & Draining the Swamp in Washington")("term limits"), "Supporting a constitutional amendment to establish lifetime term limits on members of Congress."),
        ("gov-02", 2, KY("swamp", "Fighting Corruption & Draining the Swamp in Washington")("stock trading"), "Banning members of Congress from trading stock while they're in office."),
        ("gov-09", 2, KY("swamp", "Fighting Corruption & Draining the Swamp in Washington")("lobbying"), "Banning members of Congress from becoming lobbyists once they leave Congress."),
        ("def-02", 1, KY("military", "Keep America Strong")("alliances"), "I will support a strong military alongside effective diplomacy, intelligence, cybersecurity, key alliances, and secure critical supply chains."),
        ("def-09", 1, KY("military", "Keep America Strong")("cybersecurity"), "I will support a strong military alongside effective diplomacy, intelligence, cybersecurity, key alliances, and secure critical supply chains."),
        ("def-03", 2, KY("military", "Keep America Strong")("veterans"), "I will fully fund veterans' health care, improve rural and mental health access for veterans"),
        ("def-04", 2, KY("military", "Keep America Strong")("war powers"), "Presidents should not enter open-ended conflicts without congressional authorization, clear objectives, legal authority, and an exit strategy."),
        ("def-07", 2, KY("military", "Keep America Strong")("diplomacy"), "Sending troops into danger must be a last resort."),
        ("def-10", 1, KY("military", "Keep America Strong")("foreign aid"), "Bring those dollars back home."),
        ("def-12", -2, KY("military", "Keep America Strong")("aid to Israel"), "On day one, I will introduce a proposal to terminate our annual commitment to Israel that sends nearly $4 billion in foreign aid"))]},
    {"id": "MD-GOV", "candidates": [
        cand("MD-GOV:cox", "Dan Cox", "https://dancoxforgovernor.com/",
             ("eco-02", 2, MD_COX("Cut Taxes, Fees, and Cost of Living"), "He plans to reduce the corporate and income tax rate to 4.9%."),
             ("sta-04", 1, MD_COX("Cut Taxes, Fees, and Cost of Living"), "so that retirees can stay in Maryland without being taxed out of their homes"),
             ("ene-02", 1, MD_COX("Fix the Energy Crisis"), "He will pursue clean energy methods such as SMRs and LNGs, while preserving our farmlands and a clean Bay."),
             ("ene-10", 1, MD_COX("Fix the Energy Crisis"), "Dan Cox will immediately bring power plants back online so that Marylanders are not paying the bill to bring electricity from PA and VA."),
             ("sta-01", 1, MD_COX("Build the Key Bridge Now"), "He will also take swift action to ensure that all of our bridges and roads are functioning safely and efficiently."),
             ("sta-02", 1, MD_COX("Fight for Premier Education in Maryland Schools"), "A Dan Cox administration will prioritize ensuring that our schools are fully funded"),
             ("sta-08", 1, MD_COX("No Flock Surveillance"), "ensure that our law enforcement officers have the accountability and resources they need for ensuring safe communities"),
             ("soc-08", 1, MD_COX("No Flock Surveillance"), "Dan Cox believes firmly in personal privacy for all individuals and will stop the rapid implementation of Flock surveillance.")),
        cand("MD-GOV:moore", "Wes Moore", "https://wesmoore.com/",
             ("soc-03", 2, MD_CBS("Moore signed the proclamation adding abortion rights to the state constitution"), "Since day one of my administration, I have made clear my support for a woman's right to choose"),
             ("sta-03", 2, MD_GOV23("Moore signed the Fair Wage Act of 2023"), "Governor Moore signed the Fair Wage Act of 2023 into law, which raises the minimum wage in Maryland effective January 1, 2024."),
             ("eco-01", 1, MD_WYPR("Moore proposed new income tax brackets for income over $500,000 and over $1 million"), None),
             ("eco-12", 1, MD_WYPR("under Moore's plan households earning over $700,000 would likely pay more while about two-thirds of Marylanders got a cut"), None),
             ("eco-02", 1, MD_MOORE("Cut Taxes and Protected the Middle Class"), "Last year, Governor Moore cut taxes for the middle-class, with 94% getting a tax break or having no changes on their tax bill."),
             ("sta-02", 2, MD_MOORE("Invested Historic Amounts in Public Education"), "For four consecutive years, the Moore-Miller administration has delivered record funding for public schools"),
             ("sta-08", 1, MD_MOORE("Delivered Record Reductions in Violent Crime"), "driven by historic funding for law enforcement and public safety resources"),
             ("ene-01", 1, MD_MOORE("Made Energy More Affordable and Accelerated Clean Energy"), "His administration is advancing clean energy initiatives that lower costs, reduce dependence on fossil fuels, create good-paying jobs"),
             ("hou-01", 1, MD_MOORE("Made Housing More Affordable and Accessible"), "Nearly 4,000 rental units were financed in one year"),
             ("hea-09", 1, MD_MOORE("Expanded Access to Affordable Healthcare"), "requiring insurers to cover recommended vaccines"))]},
    {"id": "WY-SEN", "candidates": [cand(
        "WY-SEN:byrd", "James W. Byrd", None,
        ("ene-02", 1, WY_BYRD("on Wyoming’s challenges"), "to incentivize cutting-edge technology, such as the TerraPower Natrium nuclear project"),
        ("eco-06", 1, WY_BYRD("on tribal interests"), "I will work across the aisle to secure robust federal investments in infrastructure, focusing on high-speed broadband, safe roads, and reliable clean water systems."),
        ("hou-09", 2, WY_BYRD("on health care"), "increasing federal investments in broadband infrastructure and making telehealth reimbursements permanent"),
        ("imm-04", 2, WY_BYRD("on immigration"), "we must fully fund and streamline our immigration courts to clear the years-long backlog"),
        ("imm-09", 2, WY_BYRD("on immigration"), "modernize the legal visa system to provide clear, predictable pathways for vital industries like agriculture, ranching, and hospitality"),
        ("ene-03", 1, WY_BYRD_SITE("Bring Down Gas and Grocery Prices"), "James Byrd will fight to lower energy costs for everyday Wyomingites by supporting responsible domestic production"),
        ("def-07", 1, WY_BYRD_SITE("Bring Down Gas and Grocery Prices"), "ending the wasteful foreign wars that leave us footing the bill overseas instead of investing at home"),
        ("eco-04", 1, WY_BYRD_SITE("Bring Down Gas and Grocery Prices"), "he'll push back against corporate consolidation in food and agriculture that lets a handful of companies set prices"),
        ("hea-01", 1, WY_BYRD_SITE("Make Healthcare Affordable"), "Healthcare should be a right you can count on, not a bill you dread."))]},
    {"id": "WY-GOV", "candidates": [cand(
        "WY-GOV:barlow", "Eric Barlow", None,
        ("sta-07", 2, WY_BARLOW("on economic development"), "That means strong Career and Technical Education programs and apprenticeships, and better coordination among employers, schools, community colleges, and the University of Wyoming."),
        ("sta-09", 1, WY_BARLOW("on health care"), "attract and support more providers; strengthen rural hospitals and clinics; support EMS; expand behavioral health capacity; improve telehealth"),
        ("hea-06", 1, WY_BARLOW("on health care"), "expand behavioral health capacity"),
        ("gov-12", 1, WY_BARLOW("on the state budget"), "Budgets reflect Wyoming’s priorities, and the process should be transparent."),
        ("edu-07", 2, WY_BARLOW_SITE("What is Eric’s vision for Wyoming education?"), "He has consistently backed legislation that keeps education decisions and discussions in the hands of Wyoming families and local school boards, not distant agencies."),
        ("ene-03", 1, WY_BARLOW_SITE("How does Eric support Wyoming’s energy industries?"), "He supported legislation protecting and enhancing coal, oil, gas and uranium production and uses"),
        ("soc-04", 2, WY_BARLOW_SITE("Is Eric pro-life?"), "Yes, Eric is firmly pro-life and has a consistent legislative record supporting protections for the unborn."),
        ("sta-08", 1, WY_BARLOW_SITE("How do we support those who answer the call to protect others?"), "They deserve leadership that backs them with the training, resources, and support they need to do their jobs safely and effectively."),
        ("sta-02", 1, WY_BARLOW_SITE("How does Eric support Wyoming’s rural heritage?"), "He has backed funding for rural infrastructure and fire protection, schools, and first responders")),
        cand("WY-GOV:casner", "Kenneth Casner", None,
             ("sta-02", 1, WY_WPM("Casner backs public school funding"), "He said he supports a state income tax, public school funding and focusing on history education in public schools."),
             ("hea-01", 2, WY_YWL("Casner calls universal health care his top issue"), "I want to give you universal health care. That's number one."))]},
    {"id": "CO-GOV", "candidates": [
        cand("CO-GOV:marx", "Victor Marx", "https://victor2026.com/",
             ("gov-12", 2, CO_QUEST("Marx on his first-year priorities"), "We will audit executive agencies and launch a public dashboard showing spending, contracts, and agency performance."),
             ("hou-04", 1, CO_QUEST("Marx on the cost of living"), "I will accelerate residential permitting, review mandates that unnecessarily increase construction costs"),
             ("sta-04", 1, CO_QUEST("Marx on the cost of living"), "protect homeowners from backdoor tax increases, strengthen relief for seniors"),
             ("sta-08", 1, CO_QUEST("Marx on his first-year priorities"), "We will support law enforcement and focus resources on violent crime, fentanyl, trafficking, and repeat offenders."),
             ("eco-01", -1, CO_QUEST("Marx on the structural deficit"), "I will not balance the budget through new taxes or backdoor fees."),
             ("gov-05", 2, CO_MARX("Election Integrity & Secure Voting"), "As Governor, I will support legislation requiring Voter ID for all forms of voting, including in-person, absentee, and mail-in ballots."),
             ("hea-06", 1, CO_MARX("Law & Order / Public Safety"), "My administration will expand regional mental-health stabilization centers and secure detox facilities"),
             ("cri-08", 1, CO_MARX("Law & Order / Public Safety"), "while expanding treatment diversion for non-violent addiction cases"),
             ("cri-04", 1, CO_MARX("Law & Order / Public Safety"), "My administration will propose legislation prohibiting automatic release or non-custodial sentencing for individuals with multiple violent-offense convictions"),
             ("cri-06", -1, CO_MARX("Law & Order / Public Safety"), "while prohibiting zero-bail programs that ignore individual risk assessments"),
             ("imm-07", 2, CO_MARX("Immigration & Ending Sanctuary Policies"), "I will direct state law enforcement agencies to honor lawful detainer requests for individuals who pose a threat to community safety."),
             ("hou-09", 2, CO_MARX("Agriculture & Rural Colorado"), "I will accelerate rural broadband deployment through the Colorado Broadband Office"),
             ("hou-11", 1, CO_MARX("Agriculture & Rural Colorado"), "incentivize public-private partnerships to deliver high-speed internet to every corner of the state"),
             ("ene-08", 2, CO_MARX("Energy, Water, & Environment"), "My administration will secure stable, long-term funding for fire mitigation to protect lives, homes, and watersheds."),
             ("ene-01", 1, CO_MARX("Energy, Water, & Environment"), "I will support an all-of-the-above energy strategy that expands renewable sources like wind, solar, and geothermal"),
             ("ene-02", 1, CO_MARX("Energy, Water, & Environment"), "maintaining the vital role of oil, gas, hydroelectric power, and emerging technologies such as modular nuclear and advanced storage systems"),
             ("edu-06", 2, CO_MARX("Education & Parental Rights"), "I will support legislation enabling parents to choose the best educational environment—public, charter, magnet, online, homeschool, or private—while ensuring that funding follows the student"),
             ("edu-04", 2, CO_MARX("Education & Parental Rights"), "As Governor, I will prioritize salary increases for teachers—not bureaucrats—by requiring districts to reduce excessive administrative overhead"),
             ("sta-07", 2, CO_MARX("Education & Parental Rights"), "allocate a defined portion of lottery proceeds toward expanding vocational and technical training facilities"),
             ("eco-02", 1, CO_MARX("Housing & Cost of Living"), "I will support legislation expanding earned-income tax credits, preserving the senior homestead exemption"),
             ("sta-10", 2, CO_MARX("Jobs, Taxes, & Economic Growth"), "I will prioritize economic development incentives for advanced manufacturing, clean-tech production, and outdoor-recreation industries"),
             ("sta-06", 1, CO_MARX("Government Accountability & Transparency"), "If elected, I will work to expand Colorado’s whistleblower protections to cover contractors, local government employees administering state funds")),
        cand("CO-GOV:weiser", "Phil Weiser", "https://philforcolorado.com/",
             ("hou-05", 2, CO_QUEST("Weiser on his first-year priorities"), "I’ll lower housing costs by working to build 40,000 affordable starter homes for first-time buyers, expanding down-payment assistance, and protecting renters from predatory corporate landlords."),
             ("hou-01", 1, CO_QUEST("Weiser on his first-year priorities"), "working to build 40,000 affordable starter homes for first-time buyers"),
             ("hou-06", 1, CO_QUEST("Weiser on his first-year priorities"), "protecting renters from predatory corporate landlords"),
             ("sta-02", 1, CO_QUEST("Weiser on his first-year priorities"), "I’ll work hard to support and strengthen Colorado’s K-12 public education system, and ensure our educators have the resources and support they need."),
             ("hea-06", 1, CO_QUEST("Weiser on his first-year priorities"), "I’ll address the youth mental health crisis by launching ColoradoCorps to connect young people to jobs in public service")),
        cand("CO-GOV:lopez", "Greg Lopez", "https://www.greglopez.co/",
             ("hou-04", 1, CO_QUEST("Lopez on the cost of living"), "My Starter Homes initiative will bring local governments, builders and lenders together to increase the supply of affordable, entry-level homes while respecting local control."))]},
    {"id": "CO-SEN", "candidates": [cand(
        "CO-SEN:baisley", "Mark Baisley", "https://baisleyforsenate.com/",
        ("eco-02", 1, CO_BAISLEY("Affordability & Prosperity"), "he will fight to cut federal taxes, roll back job-killing regulations, restore American energy dominance"),
        ("ene-03", 1, CO_BAISLEY("Affordability & Prosperity"), "he will fight to cut federal taxes, roll back job-killing regulations, restore American energy dominance"),
        ("cri-01", 1, CO_BAISLEY("Safe, Prosperous Communities"), "Mark will work with law enforcement to give them the support and funding they need to keep us safe."),
        ("cri-04", 1, CO_BAISLEY("Safe, Prosperous Communities"), "Mark will work to end the dangerous programs that put violent criminals back into our neighborhoods before they’ve rehabilitated."),
        ("agr-01", 0, CO_BAISLEY_FARM("Baisley proposes farm tax relief instead of emergency payments"), "Instead of waiting until agricultural crises occur and then writing an emergency check, we should pursue proactive policies that help producers remain profitable")),
        cand("CO-SEN:chew", "Bob Chew", "https://bobchew2026.com/",
             ("eco-07", 1, CO_CHEW("National Debt"), "My proposal will combine: responsible spending restraint, reforms to entitlement programs that protect today’s retirees while strengthening programs for future generations"),
             ("eco-12", 1, CO_CHEW("Deficit Spending"), "enact fair and responsible tax reform to bring in more revenue from the wealthiest Americans"),
             ("eco-10", -2, CO_CHEW("Free Trade"), "Tariffs are a tax, plain and simple."),
             ("agr-07", -1, CO_CHEW("Free Trade"), "Hardworking families are paying more for basic goods when they are already struggling."),
             ("ene-02", 2, CO_CHEW("Energy"), "I support an all-of-above energy strategy that includes a heavy reliance on nuclear power."),
             ("imm-07", 2, CO_CHEW("Immigration"), "Deporting a drug kingpin makes us safer; deporting a local farm hand makes us poorer."),
             ("imm-08", -1, CO_CHEW("Immigration"), "we should not expend limited government resources pursuing peaceful immigrants who contribute to our economy"),
             ("edu-06", 2, CO_CHEW("Education and Opportunity"), "We should empower families to choose the schools that best meet their children’s needs and provide support so they can afford it."),
             ("edu-07", 1, CO_CHEW("Education and Opportunity"), "More decisions should be made locally, not dictated by bureaucrats in Washington."),
             ("edu-03", 1, CO_CHEW("Jobs and Opportunity"), "I also support workforce training and apprenticeship programs developed in partnership with private industry"),
             ("cri-05", 1, CO_CHEW("Crime and Public Safety"), "We need more private industry entrepreneurs to play a role in giving former criminals a path to productive civic participation and financial independence."),
             ("hou-04", 1, CO_CHEW("Affordable Housing"), "If we want to build more affordable housing, we need to tame our national deficits, reduce tariffs, welcome immigration labor, and repeal costly regulations."),
             ("gov-01", 2, CO_CHEW("Making Government Work for the People"), "Enact congressional term limits: 16 years for members of the U.S. House and 18 years for members of the U.S. Senate."),
             ("gov-04", 1, CO_CHEW("Making Government Work for the People"), "Eliminate gerrymandering and create truly competitive elections with more than two viable political parties."),
             ("gov-07", 1, CO_CHEW("Making Government Work for the People"), "Open primaries, ranked choice voting, or proportional representation can help reduce this threat and restore the independence of the legislative branch."),
             ("def-13", 2, CO_CHEW("International Conflict"), "We must support Ukraine against Russian aggression, counter China’s growing military ambitions"),
             ("def-16", 1, CO_CHEW("International Conflict"), "We must support Ukraine against Russian aggression, counter China’s growing military ambitions"),
             ("def-14", 2, CO_CHEW("International Conflict"), "China, North Korea, Russia, and Iran are controlled by dictators that suppress freedom, threaten their neighbors, and seek to expand their influence at America’s expense."),
             ("def-15", -1, CO_CHEW("Iran"), "But Donald Trump’s war-of-choice with Iran is proving even worse."),
             ("def-04", 1, CO_CHEW("Iran"), "He did not seek congressional authority and did not build both domestic and international support before taking actions with global consequences."))]},
    {"id": "SD-SEN", "candidates": [cand(
        "SD-SEN:bengs", "Brian Bengs", None,
        ("eco-12", 1, SD_SEARCHLIGHT("Bengs supports a tax system that favors work over wealth"), "favors work over wealth"),
        ("def-04", 1, SD_DNN("Bengs calls the war in Iran unconstitutional"), None),
        ("def-15", 0, SD_DNN("Bengs calls the war in Iran unconstitutional but says the U.S. must reopen the Strait of Hormuz rather than pull out prematurely"), None),
        ("agr-07", 1, SD_DNN("Bengs opposes foreign beef imports"), None),
        ("eco-01", 2, SD_BENGS("Unrig The Tax Code"), "It’s long past time for the ultra-rich to pay their fair share once again, like they had to in the 1960s."),
        ("eco-02", 1, SD_BENGS("Unrig The Tax Code"), "we can actually lower taxes for small businesses and people who work for a living"),
        ("gov-02", 2, SD_BENGS("Target & Eliminate Corruption"), "members of Congress and their spouses must be banned from purchasing, selling, or holding individual stocks for the duration of their time in office"),
        ("gov-01", 2, SD_BENGS_STAND("his anti-corruption platform"), "His anti-corruption platform includes: Term Limits"),
        ("gov-13", -2, SD_BENGS_STAND("his anti-corruption platform"), "Eliminating Corporate PACs and Limiting all PAC spending"),
        ("gov-04", 2, SD_BENGS("Take Power Away From Self-Serving Partisans"), "Federal redistricting reform will take map-drawing out of the hands of diehard partisans trying to rig congressional districts for their preferred party."),
        ("soc-03", 1, SD_BENGS("Keep Government Out of Your Business"), "I respect a woman’s right to choose and support abortion restrictions after the point of “viability”"),
        ("soc-04", -1, SD_BENGS("Keep Government Out of Your Business"), "I respect a woman’s right to choose and support abortion restrictions after the point of “viability”"),
        ("soc-10", 1, SD_BENGS("Keep Government Out of Your Business"), "As a person who generally wants others to be happy, I support you loving whomever you want."),
        ("imm-01", 1, SD_BENGS("Overhaul Immigration & Secure Our Border"), "effects-based reform must include a strong border security component and increased legal immigration"),
        ("imm-03", 1, SD_BENGS("Overhaul Immigration & Secure Our Border"), "effects-based reform must include a strong border security component and increased legal immigration"),
        ("def-03", 1, SD_BENGS("Protect And Serve Veterans"), "On my watch, Americans who served their country will not be abandoned at home just so Big Money can make an extra buck."),
        ("eco-04", 2, SD_BENGS("Take On Big Ag"), "we contain it with aggressive enforcement of antitrust laws to break up monopolistic practices"))]},
    {"id": "DE-SEN", "candidates": [cand(
        "DE-SEN:katz", "Michael Katz", "https://drmikekatz.com/",
        ("hea-04", 1, DE_WDEL("Katz wants more competition among private insurers"), "work at the federal level to break down the barriers to competition, focusing on insurance so that people can buy health insurance across state lines"),
        ("hea-06", 1, DE_KATZ("Healthcare"), "Treat the whole person — integrating mental health services into education and community health rather than continuing the artificial wall between physical and mental care."),
        ("hea-09", 1, DE_KATZ("Healthcare"), "Build a system that advocates healthy behaviors and lifestyles starting from prenatal care and early childhood."),
        ("eco-02", 1, DE_KATZ("Protecting Delaware Jobs"), "I will vote to make the pro-growth tax cuts permanent"),
        ("eco-10", 1, DE_KATZ("Protecting Delaware Jobs"), "I support targeted federal incentives and strategic tariffs to protect domestic energy, technology, and pharmaceuticals from foreign exploitation."),
        ("agr-03", 1, DE_KATZ("Protecting Delaware Jobs"), "I support targeted federal incentives and strategic tariffs to protect domestic energy, technology, and pharmaceuticals from foreign exploitation."),
        ("agr-04", 1, DE_KATZ("Protecting Delaware Jobs"), "I support targeted federal incentives and strategic tariffs to protect domestic energy, technology, and pharmaceuticals from foreign exploitation."),
        ("ene-02", 1, DE_KATZ("Economy & Cost of Living"), "including safe nuclear power with the right safeguards — to meet long-term demand and drive down utility bills"),
        ("ene-03", 1, DE_KATZ("Economy & Cost of Living"), "We must unlock American energy dominance to lower prices at the pump"),
        ("hou-04", 1, DE_KATZ("Economy & Cost of Living"), "Augment the supply of affordable homes through zoning reform partnerships, construction incentives, and reduced compliance costs for projects that meet community needs."),
        ("hou-05", 1, DE_KATZ("Economy & Cost of Living"), "Create targeted federal pathways — tax incentives, lending standards, and construction support — that give first-time homebuyers a fair shot at building a future here."),
        ("edu-03", 1, DE_KATZ("Education"), "Invest in workforce and education alignment so Delaware students graduate ready for 21st-century careers, including skilled trades, healthcare, and technical fields."),
        ("def-01", 1, DE_KATZ("Military, Veterans & National Security"), "Fully fund military readiness."),
        ("def-02", 1, DE_KATZ("Military, Veterans & National Security"), "I support policies that strengthen our alliances, deter aggression, protect critical infrastructure, defend our supply chains, and counter emerging threats"),
        ("def-03", 2, DE_KATZ("Military, Veterans & National Security"), "Improve access to timely, high-quality healthcare."),
        ("def-09", 1, DE_KATZ("Military, Veterans & National Security"), "Strengthen cybersecurity and missile defense."),
        ("cri-01", 2, DE_KATZ("Law & Order, Constitution, and Police"), "provide our federal, state, and local law enforcement agencies with the funding, advanced tactical resources, and legal protections they need to do their jobs safely"),
        ("cri-04", 2, DE_KATZ("Law & Order, Constitution, and Police"), "I support heavily increasing federal penalties for violent crimes and expanding support for localized police recruitment."),
        ("soc-01", 2, DE_KATZ("Law & Order, Constitution, and Police"), "Keep the federal bureaucracy entirely out of the business of policing American speech and religious expression."),
        ("soc-06", 1, DE_KATZ("Law & Order, Constitution, and Police"), "Keep the federal bureaucracy entirely out of the business of policing American speech and religious expression."),
        ("imm-01", 2, DE_KATZ("Border Security & National Sovereignty"), "I fully support finishing physical wall construction in high-traffic sectors"),
        ("imm-04", 1, DE_KATZ("Border Security & National Sovereignty"), "We need to deploy expedited judicial assets directly to processing centers to deliver immediate decisions."),
        ("imm-08", 1, DE_KATZ("Border Security & National Sovereignty"), "strictly enforcing interior immigration laws"),
        ("imm-10", 1, DE_KATZ("Border Security & National Sovereignty"), "mandating workplace verification systems to protect American labor and wages"),
        ("gov-05", 2, DE_KATZ("Voter Integrity"), "Establish nationwide photo identification standards for voting"),
        ("gov-06", -2, DE_KATZ("Voter Integrity"), "Mail-in voting should be scaled back strictly to legitimate exceptions"),
        ("gov-04", 1, DE_KATZ_REC("SR 9"), "Dr. Katz introduced a Senate Resolution calling for an open and transparent redistricting process with meaningful public participation"),
        ("gov-09", 2, DE_KATZ_REC("SB 141"), "Dr. Katz introduced sweeping ethics and transparency legislation targeting the revolving door between lobbyists and government."),
        ("gov-12", 1, DE_KATZ("Military, Veterans & National Security"), "Improve Government Accountability — improve transparency, reduce administrative waste, strengthen oversight"))]},
    {"id": "AL-SEN", "candidates": [cand(
        "AL-SEN:wess", "Everett Wess", "https://wessforsenate.com/",
        ("eco-03", 1, AL_REFLECTOR("Wess campaigned on raising the federal minimum wage"), None))]},
    {"id": "AR-GOV", "candidates": [
        cand("AR-GOV:love", "Fredrick Love", "https://www.fredlove.com/",
             ("sta-01", 1, AR_LOVE("Economic Development"), "rebuild critical infrastructure like roads, water, sewer, and broadband"),
             ("hou-09", 1, AR_LOVE("Economic Development"), "rebuild critical infrastructure like roads, water, sewer, and broadband"),
             ("sta-07", 1, AR_LOVE("Economic Development"), "expand career pathways through apprenticeships, entrepreneurship, and workforce training"),
             ("hou-01", 1, AR_LOVE("Economic Development"), "a focused effort to expand affordable housing across the state"),
             ("sta-02", 1, AR_LOVE("Education"), "Fred will ensure every student reads on grade level by investing in literacy, providing the proper resources, and strengthening early education."),
             ("edu-04", 1, AR_LOVE("Education"), "support teachers with fair pay and resources"),
             ("hea-06", 1, AR_LOVE("Healthcare"), "expand access to maternal and mental health services across the state"),
             ("cri-05", 2, AR_LOVE("Public Safety"), "instead focus on rehabilitation, workforce training, and reentry programs that reduce repeat offenses")),
        cand("AR-GOV:sanders", "Sarah Huckabee Sanders", "https://www.sarahforgovernor.com/",
             ("cri-04", 1, AR_SANDERS("Meet Sarah"), "public safety reforms to invest in prison space and get repeat offenders off the streets"))]},
    {"id": "ME-GOV", "candidates": [cand(
        "ME-GOV:charles", "Bobby Charles", "https://www.bobbyformaine.com/",
        ("sta-08", 1, ME_CHARLES("Cut Crime"), "He will strengthen law enforcement, increase support for addiction recovery and mental health services"),
        ("hea-06", 1, ME_CHARLES("Cut Crime"), "He will strengthen law enforcement, increase support for addiction recovery and mental health services"),
        ("sta-06", 1, ME_CHARLES("Cut Crime"), "CRACK DOWN ON GOVERNMENT CORRUPTION AND FRAUD"),
        ("sta-04", 2, ME_CHARLES("Cut Your Taxes"), "Bobby Charles $100K Homestead Exemption Plan"),
        ("eco-01", -2, ME_CHARLES("Cut Your Taxes"), "He pledges to abolish the state income tax"),
        ("ene-10", 1, ME_CHARLES("Cut Your Taxes"), "RESTORE RELIABLE, AFFORDABLE POWER"),
        ("edu-06", 1, ME_CHARLES("No Nonsense"), "He will support teachers, educational freedom, and curriculum transparency to ensure parents have real say in what is taught."),
        ("edu-07", 1, ME_CHARLES("No Nonsense"), "He will support teachers, educational freedom, and curriculum transparency to ensure parents have real say in what is taught."))]},
    {"id": "IL-SEN", "candidates": [
        cand("IL-SEN:tracy", "Don Tracy", None,
             ("def-15", 1, IL_WTTW("Tracy called the Iran war just if it stops Iran getting a nuclear weapon"), "if we’re able to eliminate Iran from starting a World War III, then I say, it is just."),
             ("def-14", 1, IL_CNI("Tracy called Putin a thug and would have opposed waiving sanctions on Russia"), None),
             ("eco-07", 1, IL_CNI("Tracy would lower costs by reducing government spending"), None),
             ("eco-02", 1, IL_CNI("Tracy would address affordability by cutting taxes"), None),
             ("hea-04", 2, IL_CNI("Tracy opposes overhauling the health care system and wants more market competition"), "We cannot ditch a really good system that provides very good healthcare for 92% in a quest for this perfect healthcare system"),
             ("edu-07", 1, IL_CNI("Tracy believes more education functions belong at the state and local level"), None),
             ("agr-01", 1, IL_CNI("Tracy supports a new five-year farm bill, which traditionally includes farm subsidies"), None)),
        cand("IL-SEN:stratton", "Juliana Stratton", None,
             ("def-15", -2, IL_CNI("Stratton vowed not to vote for supplemental funding for the Iran war"), None),
             ("hea-01", 2, IL_CNI("Stratton supports a Medicare for all system"), None),
             ("eco-02", 2, IL_CNI("Stratton backs a middle-class tax break paid for by higher taxes on income over $1 million"), None),
             ("imm-04", 2, IL_CNI("Stratton wants more immigration judges and caseworkers to clear the backlog"), None),
             ("agr-01", 1, IL_CNI("Stratton supports a new five-year farm bill, which traditionally includes farm subsidies"), "I will fight to make sure that we can get back to that bipartisan piece of legislation"))]},
    {"id": "IL-GOV", "candidates": [cand(
        "IL-GOV:bailey", "Darren Bailey", "https://baileyforillinois.com/",
        ("sta-02", 1, IL_BAILEY("Ensuring Quality Education for Every Child"), "he will fight to ensure that our schools are fully funded, empower parents to make the best choices for their children"),
        ("edu-06", 1, IL_BAILEY("Ensuring Quality Education for Every Child"), "empower parents to make the best choices for their children"),
        ("sta-08", 1, IL_BAILEY("Protecting Our Communities"), "providing the tools, training, and support officers need to do their jobs effectively"),
        ("eco-02", 1, IL_BAILEY("Making Illinois Affordable Again"), "he will fight to lower taxes, cut wasteful government spending, and bring real fiscal responsibility back to Springfield"),
        ("sta-04", 2, IL_BAILEY("Property Taxes"), "No family should ever pay more in property taxes than their mortgage"))]},
    {"id": "NM-GOV", "candidates": [
        cand("NM-GOV:hull", "Gregg Hull", None,
             ("sta-07", 1, NM_AP("Hull would use state money to expand vocational education, including construction trades"), None),
             ("sta-01", 1, NM_AP("Hull wants greater state investment in roadways"), None),
             ("edu-06", 1, NM_AP("Hull is committed to school choice but has not said whether it would fund private schools"), "School choice means, really, parental oversight of their child's education")),
        cand("NM-GOV:haaland", "Deb Haaland", "https://debhaaland.com/",
             ("edu-02", 2, NM_HAALAND("Education"), "Expand the Opportunity Scholarship to provide free tuition for New Mexicans, including for graduate education."),
             ("edu-03", 1, NM_HAALAND("Education"), "Expand career pathways starting in middle school through high school and provide hands-on career experience."),
             ("soc-07", 1, NM_HAALAND("Education"), "Teach kids to read earlier by detecting literacy problems sooner, bolstering universal childcare, boosting reading and bilingual instruction"),
             ("eco-02", 1, NM_HAALAND("Affordability"), "Give New Mexicans a raise by increasing the minimum wage and increasing the child tax credit."),
             ("hou-04", 1, NM_HAALAND("Affordability"), "Aggressively build more housing, focusing on reducing unnecessary barriers and expediting permitting processes."),
             ("hou-05", 1, NM_HAALAND("Affordability"), "Expand down payment assistance programs for first time home buyers"),
             ("sta-08", 1, NM_HAALAND("Public Safety"), "Provide law enforcement with the tools and technology to arrest violent offenders, track and detain drug traffickers"),
             ("cri-07", 1, NM_HAALAND("Public Safety"), "Expand violence intervention and prevention programs in local communities and schools."),
             ("sta-09", 1, NM_HAALAND("Healthcare"), "Increase mobile health clinics to reach New Mexicans in rural areas and protect rural hospitals."),
             ("hea-03", 1, NM_HAALAND("Healthcare"), "Use budget surpluses to fill Medicaid gaps"),
             ("hea-06", 2, NM_HAALAND("Healthcare"), "Launch a full throttle operation to deliver mental health and homelessness assistance to New Mexicans in need."),
             ("hea-07", 1, NM_HAALAND("Healthcare"), "Protect access for those who use the state’s health insurance marketplace by expanding New Mexico’s Health Care Affordability Fund."))]},
    {"id": "CA-GOV", "candidates": [cand(
        "CA-GOV:becerra", "Xavier Becerra", "https://www.xavierbecerra2026.com/",
        ("hea-01", 2, CA("health-care", "Health Care")("coverage"), "building toward a system where universal access is not a promise deferred but a guarantee delivered"),
        ("hea-02", 2, CA("health-care", "Health Care")("drug prices"), "As HHS Secretary, I negotiated drug price reductions of up to 79% on some of the most widely used medications in America"),
        ("hea-08", 2, CA("health-care", "Health Care")("pre-existing conditions"), "led the three-year federal court fight that saved the Affordable Care Act for 133 million Americans with pre-existing conditions"),
        ("hea-06", 2, CA("homelessness", "Homelessness")("treatment"), "I will implement every reform it authorizes, build thousands of treatment beds"),
        ("eco-04", 2, CA("health-care", "Health Care")("antitrust"), "I won a $575 million antitrust settlement against one of the largest health systems in the state"),
        ("soc-07", 1, CA("economy-and-affordability", "Economy and Affordability")("childcare"), "expanding help with childcare and essential costs"),
        ("hou-04", 2, CA("housing", "Housing")("zoning"), "Where zoning still locks out affordable housing from entire communities, we will open it up."),
        ("hou-01", 1, CA("housing", "Housing")("public financing"), "we can use the state’s financing tools, its public land, and its capacity to de-risk development"),
        ("hou-06", 1, CA("homelessness", "Homelessness")("eviction defense"), "We will immediately expand rental assistance and eviction defense for those most at risk, including seniors, foster youth, and veterans."),
        ("ene-01", 1, CA("energy-utilities", "Energy and Utilities")("clean energy"), "California’s clean-energy transition is necessary and urgent"),
        ("ene-08", 2, CA("california-disaster-preparedness-resilience", "Disaster Preparedness")("prevention"), "I will fight for major investments in wildfire prevention, flood control, and seismic retrofits, prioritizing the communities most at risk."),
        ("gov-12", 2, CA("homelessness", "Homelessness")("spending dashboards"), "launch public outcomes dashboards so Californians can see exactly where their money is going and what it is producing"))]},
    {"id": "CT-GOV", "candidates": [cand(
        "CT-GOV:lamont", "Ned Lamont", "https://www.nedlamont.com/",
        ("soc-07", 2, CT_ACC("Childcare and Education"), "Launched a $600 million Early Start CT endowment fund to provide universal early childhood education and access to quality, affordable childcare."),
        ("edu-09", 2, CT_PRI("Lowering Costs for Families"), "Continuing to deliver universal free school meals"),
        ("edu-02", 1, CT_WINS("A Proven Leader"), "Created Debt-Free Community College"),
        ("sta-02", 2, CT_ACC("Childcare and Education"), "Increased education funding to towns and public schools by more than $270 million during the 2026 session."),
        ("hea-01", 1, CT_PRI("Affordable and Accessible Healthcare"), "Explore bold solutions that move Connecticut toward universal affordable healthcare"),
        ("hea-03", 2, CT_ACC("Making Connecticut More Affordable"), "Created the Covered Connecticut program to provide no-cost health coverage – including medical, dental, and non-emergency transportation to nearly 40,000 adults"),
        ("hea-06", 1, CT_PRI("Affordable and Accessible Healthcare"), "Strengthen preventative and mental healthcare services"),
        ("hea-09", 1, CT_ACC("Standing Up to Trump"), "Protected access to vaccines for Connecticut residents to ensure continued COVID-19 vaccination coverage under state-regulated insurance plans"),
        ("soc-03", 2, CT_PRI("Affordable and Accessible Healthcare"), "Protect reproductive freedom and abortion access"),
        ("soc-12", 2, CT_WINS("A Proven Leader"), "Ensured access to gender-affirming care and banned discrimination based on gender identity in health insurance"),
        ("sta-03", 2, CT_WINS("A Proven Leader"), "Increased the minimum wage to $15/hour with automatic increases tied to inflation"),
        ("eco-02", 1, CT_WINS("A Proven Leader"), "Strengthened Earned Income Tax Credit to one of the most generous in the nation"),
        ("eco-09", 2, CT_WINS("Standing Strong for Workers"), "Banned “captive audience” anti-union meetings"),
        ("ene-01", 2, CT_PRI("Environment and Climate Change"), "we will continue a balanced, responsive expansion of utility-scale solar, paired with small-scale and residential deployments"),
        ("ene-06", 1, CT_PRI("Environment and Climate Change"), "Achieve a 100% zero-carbon grid by 2040 and net-zero emissions by 2050 targets."),
        ("hou-01", 1, CT_PRI("Tackling Connecticut’s Housing Shortage"), "Supporting workforce and middle-income housing"),
        ("sta-01", 1, CT_ACC("Housing, Transit and Infrastructure"), "Invested more than $17 million in 15 locally-owned bridge projects across Connecticut under the State Local Bridge Program"),
        ("sta-12", 1, CT_ACC("Housing, Transit and Infrastructure"), "Broke ground on new train stations on the Waterbury Branch and Hartford Lines"),
        ("imm-08", -1, CT_ACC("Standing Up to Trump"), "Prohibited federal agents, like ICE, from wearing masks or making warrantless arrests inside Connecticut courthouses."))]},
    {"id": "ID-GOV", "candidates": [cand(
        "ID-GOV:little", "Brad Little", None,
        ("eco-02", 1, ID_SUN("Little cites the tax relief he delivered"), ID_LITTLE_Q),
        ("sta-02", 1, ID_SUN("Little cites record school spending"), ID_LITTLE_Q),
        ("sta-08", 1, ID_SUN("Little cites record public safety spending"), ID_LITTLE_Q),
        ("sta-01", 1, ID_SUN("Little cites record infrastructure spending"), ID_LITTLE_Q),
        ("edu-04", 1, ID_LITTLE_ACC("Supporting parents and education"), "Under his watch, we achieved historic teacher pay increases"),
        ("sta-04", 1, ID_LITTLE_ACC("Supporting parents and education"), "school facility investments that dual as property tax relief"),
        ("imm-07", 2, ID_LITTLE_ACC("Securing the Border and Our Communities"), "our Operation No Return is removing dangerous illegal alien criminals from Idaho communities"),
        ("hou-09", 1, ID_LITTLE_ACC("Making investments where they count"), "Gov. Little championed historic investments in natural resources, transportation, water, broadband, agriculture and a number of other areas"),
        ("sta-07", 1, ID_LITTLE_ACC("Making America Great Again"), "From increasing wages to workforce development, Gov. Brad Little’s LAUNCH Program is a national model"),
        ("soc-04", 1, ID_LITTLE_ACC("Defending Idaho Values"), "From defending women’s sports to promoting pro-life policies"))]},
    {"id": "RI-GOV", "candidates": [
        cand("RI-GOV:block", "Ken Block", "https://www.blockforgovernor.com/",
             ("soc-08", 1, RI_NBC10("Block says license-plate cameras should be heavily regulated"), "I’m very concerned about Flock cameras and the ability of bad actors to get into those databases"),
             ("eco-01", -2, RI_BLOCK("Millionaires Tax"), "If passed by the legislature, Ken will veto a Millionaires Tax."),
             ("eco-02", 1, RI_BLOCK("Cost of Living Relief"), "My plan targets hidden and regressive taxes, fees, and government-imposed costs that are driving the affordability crisis in Rhode Island."),
             ("gov-12", 2, RI_BLOCK("Cost of Living Relief"), "If government wants to spend money on a program, put it in the budget. Debate it publicly."),
             ("hou-03", 1, RI_BLOCK("Eliminate RIPTA fares for one year"), "My administration would implement a one-year fare-free trial, replacing that revenue with savings identified elsewhere in the state budget")),
        cand("RI-GOV:guckian", "Aaron Guckian", "https://www.aaronforri.com/",
             ("sta-02", 1, RI_GUCKIAN("Rebuilding Education and Preparing the Workforce of the Future"), "The campaign will prioritize investments in public schools, teacher support, and career-ready pathways, including vocational training, technical programs, and partnerships with local employers."),
             ("sta-07", 1, RI_GUCKIAN("Rebuilding Education and Preparing the Workforce of the Future"), "The campaign will prioritize investments in public schools, teacher support, and career-ready pathways, including vocational training, technical programs, and partnerships with local employers."),
             ("gov-12", 1, RI_GUCKIAN("Holding State Government Accountable"), "Aaron pledged to restore transparency, eliminate mismanagement, and ensure every tax dollar is spent responsibly.")),
        cand("RI-GOV:foulkes", "Helena Foulkes", "https://helenafoulkes.com/",
             ("sta-07", 2, RI_FOULKES("Believe in Rhode Island Part 1"), "$100 Million Proposal for Career and Technical Education"),
             ("soc-07", 1, RI_FOULKES("Believe in Rhode Island Part 2"), "Childcare and Transportation for Working Families"),
             ("ene-01", 1, RI_FOULKES("No False Choices"), "Affordable Utility Bills and a Clean Energy Future"),
             ("sta-06", 1, RI_FOULKES("Ethics Reform"), "Ensuring the State House Works for All Rhode Islanders, Not Just the Insiders"))]},
    {"id": "CA-GOV", "candidates": [cand(
        "CA-GOV:hilton", "Steve Hilton", "https://stevehiltonforgovernor.com/",
        ("eco-11", 2, CA_HILTON("paid leave"), "12 WEEKS PAID LEAVE FOR CALIFORNIA FAMILIES"),
        ("ene-01", -2, CA_HILTON("electricity"), "CUT CALIFORNIA’S ELECTRICITY BILLS BY ENDING WIND AND SOLAR FARM MANDATES AND SUBSIDIES"),
        ("ene-10", 2, CA_HILTON("electricity"), "CUT CALIFORNIA’S ELECTRICITY BILLS BY ENDING WIND AND SOLAR FARM MANDATES AND SUBSIDIES"),
        ("ene-08", 1, CA_HILTON("wildfires"), "A MODERN WILDFIRE PREVENTION PLAN FOR CALIFORNIA"),
        ("hou-04", 1, CA_HILTON("housing costs"), "STOP THE HIDDEN TAX ON NEW HOMES: CAP GOVERNMENT FEES AND REGULATORY COSTS AT $50,000"),
        ("sta-08", 1, CA_HILTON("policing"), "BUILD A REAL CALIFORNIA STATE POLICE FORCE"))]},
    {"id": "MA-GOV", "candidates": [cand(
        "MA-GOV:healey", "Maura Healey", "https://maurahealey.com/",
        ("hou-01", 1, MA_HEALEY("Promises Kept"), "She eliminated renters’ fees and is building 100,000 new homes to lower the cost of housing"),
        ("hou-06", 1, MA_HEALEY("Promises Kept"), "She eliminated renters’ fees and is building 100,000 new homes to lower the cost of housing"),
        ("sta-02", 2, MA_HEALEY("Promises Kept"), "Doubled funding for our schools, made meals free, and made community college cost-free for everyone"),
        ("edu-09", 2, MA_HEALEY("Promises Kept"), "Doubled funding for our schools, made meals free, and made community college cost-free for everyone"),
        ("edu-02", 1, MA_HEALEY("Promises Kept"), "Doubled funding for our schools, made meals free, and made community college cost-free for everyone"),
        ("hea-09", 1, MA_HEALEY_ABOUT("Making History"), "She stood up to protect vaccine access when Trump and Robert Kennedy Jr. tried to take it away"))]},
    {"id": "AK-GOV", "candidates": [cand(
        "AK-GOV:bronson", "Dave Bronson", "https://www.davebronson.com/",
        ("sta-01", 2, AK_BRONSON("Infrastructure"), "Invest in roads, bridges, and ports so businesses can thrive and families can prosper"),
        ("eco-01", -1, AK_BRONSON("Economy"), "to create jobs, power America, and strengthen our state’s finances, without raising taxes"),
        ("gov-12", 1, AK_BRONSON("Government Reform"), "My approach to government reform is straightforward: transparency, accountability, and results."),
        ("sta-08", 1, AK_BRONSON_ABOUT("Get to know Dave"), "He also invested in public safety by raising police pay and securing the resources officers needed to serve effectively."))]},
    {"id": "AR-SEN", "candidates": [cand(
        "AR-SEN:shoffner", "Hallie Shoffner", "https://www.hallieshoffner.com/",
        ("eco-02", 2, AR_SHOFFNER("Lowering Costs for Working Families"), "That means real economic vision by cutting taxes for working families, lowering the cost of groceries, childcare, housing, and healthcare, and strengthening Arkansas industries."),
        ("eco-03", 2, AR_SHOFFNER("Growing the Economy and Supporting the Workforce"), "That means raising the minimum wage, expanding workforce training, cutting taxes for working families, giving local businesses the resources they need to thrive"),
        ("eco-04", 1, AR_SHOFFNER("Keeping Arkansas Safe"), "standing up to corporate monopolies that delay repairs and drive up costs for emergency vehicles and critical equipment"),
        ("eco-07", 1, AR_SHOFFNER("Taking on the Debt"), "In the Senate, I will fight to rein in waste, make smart investments in working people"),
        ("eco-09", 2, AR_SHOFFNER("Strengthening Unions and Protecting Workers"), "I will stand with workers to protect the right to organize, bargain collectively, and be treated with dignity."),
        ("eco-11", 1, AR_SHOFFNER("Supporting Mothers and Families"), "Supporting mothers means affordable childcare, paid leave, quality healthcare, and safe communities where kids can grow and families can thrive."),
        ("eco-12", 1, AR_SHOFFNER("Protecting Social Security and Medicare"), "lift the contribution cap on the ultra wealthy"),
        ("soc-07", 1, AR_SHOFFNER("Supporting Mothers and Families"), "Supporting mothers means affordable childcare, paid leave, quality healthcare, and safe communities where kids can grow and families can thrive."),
        ("hea-07", 1, AR_SHOFFNER("Making Healthcare Affordable and Accessible"), "I will fight to protect our hospitals, lower prescription drug prices, strengthen the Affordable Care Act, protect Medicare and Medicaid"),
        ("edu-03", 1, AR_SHOFFNER("Supporting Education and Investing in Opportunity"), "investing in workforce and technical education, apprenticeships, and partnerships with community colleges"),
        ("edu-04", 2, AR_SHOFFNER("Supporting Education and Investing in Opportunity"), "I will fight for increased pay, better benefits, and real support for teachers, bus drivers, cafeteria workers, paraprofessionals, and staff"),
        ("cri-01", 1, AR_SHOFFNER("Keeping Arkansas Safe"), "supporting local law enforcement and first responders with the training, staffing, mental health support, and strong unions they need to do their jobs safely"),
        ("cri-05", 1, AR_SHOFFNER("Addressing the Addiction Crisis"), "investing in reentry programs so people leaving incarceration can work, heal, and rebuild their lives"),
        ("cri-07", 1, AR_SHOFFNER("Keeping Arkansas Safe"), "investing in community-based crime prevention"),
        ("cri-08", 2, AR_SHOFFNER("Addressing the Addiction Crisis"), "treating people struggling with addiction as patients, not criminals"))]},
    {"id": "OR-SEN", "candidates": [cand(
        "OR-SEN:smith", "David Brock Smith", "https://www.davidbrocksmithfororegon.com/",
        ("hea-06", 1, OR_SMITH("Ending the Homelessness Crisis"), "We need drug and mental health treatment that works"),
        ("ene-08", 1, OR_SMITH("Wildfire Prevention Policy"), "address the desperate need for active forest management, fuel reduction, and working with landowners to better protect homes and communities"))]},
    {"id": "VA-SEN", "candidates": [cand(
        "VA-SEN:mizusawa", "Bert Mizusawa", "https://bertforsenate.com/",
        ("def-03", 2, VA_MIZUSAWA("Defending Our Military"), "I will protect veterans' benefits, expand access to quality healthcare, and ensure veterans aren't stuck waiting on Washington for the care they earned."),
        ("gov-02", 2, VA_MIZUSAWA("Stop Corruption"), "As Senator, I will ban congressional stock trading, so politicians put their constituents first, not themselves."))]},
    {"id": "HI-GOV", "candidates": [cand(
        "HI-GOV:green", "Josh Green", "https://joshgreenforhawaii.com/",
        ("hou-04", 1, HI_GREEN_HOUSING("Affordable Housing"), "by cutting red tape and removing unnecessary regulations on new housing, while still protecting our environment"),
        ("hea-07", 2, HI_GREEN_HEALTH("Healthcare"), "Governor Josh Green is lowering healthcare costs for everyone in Hawaii by covering Obamacare subsidies for families who count on them"),
        ("sta-09", 1, HI_GREEN_HEALTH("Healthcare"), "bringing nearly $1 billion in federal investments for rural health statewide"),
        ("ene-01", 2, HI_GREEN_CLIMATE("Climate Change and Environment"), "cut our dependence on fossil fuels, and invest in renewable and sustainable energy in our state"),
        ("hea-09", 1, HI_GREEN_ABOUT("Meet Josh"), "helped lead Hawaii’s COVID pandemic response — vaccinating over a million people and saving thousands of lives"),
        ("soc-07", 1, HI_GREEN_COST("Cost of Living"), "doubled the earned income tax credit and the food tax credit, and increased the child and dependent care credit"),
        ("ene-10", 1, HI_CB("Green on liquefied natural gas"), "I have kept every option on the table to bring costs down and improve reliability, including using LNG as a bridge."),
        ("ene-08", 2, HI_CB("Green on disaster preparedness"), "We are investing in emergency management capacity and disaster mitigation, modernizing our alert systems and hardening our grid and critical infrastructure."),
        ("sta-06", 2, HI_CB("Green on government ethics"), "I signed a broad package of good-government bills: strengthening lobbyist disclosure, banning prohibited gifts, tightening campaign-spending rules and making official misconduct a crime."),
        ("gov-03", 1, HI_CB("Green on government ethics"), "I’ll keep backing stronger enforcement and disclosure, protect the independence of our Ethics and Campaign Spending Commissions"),
        ("gov-11", 1, HI_CB("Green on government ethics"), "support reforms that limit the influence of money in politics"),
        ("gov-10", 0, HI_CB("Green on a citizen initiative process"), "I welcome the conversation."),
        ("hea-06", 1, HI_CB("Green on homelessness"), "rapid re-housing, mental health and addiction support, and building more affordable housing"))]},
    {"id": "SC-GOV", "candidates": [
        cand("SC-GOV:wilson", "Alan Wilson", "https://wilsonforsc.com/",
             ("cri-04", 2, SC_WILSON("Securing Our Communities"), "He’ll work closely with law enforcement to dismantle criminal networks and strengthen penalties for fentanyl and violent offenders."),
             ("sta-02", 1, SC_WILSON("Fixing Education and Empowering Parents"), "As Governor, he will fully fund public schools and expand school choice to ensure families have more control over their children’s education."),
             ("edu-06", 2, SC_WILSON("Fixing Education and Empowering Parents"), "As Governor, he will fully fund public schools and expand school choice to ensure families have more control over their children’s education."),
             ("sta-07", 1, SC_WILSON("Fixing Education and Empowering Parents"), "strengthening technical and vocational education"),
             ("sta-08", 1, SC_WILSON("Fixing Education and Empowering Parents"), "will expand the School Resource Officer programs to ensure students are learning in a safe environment"),
             ("sta-01", 2, SC_WILSON("Improving Roads, Bridges, and Infrastructure"), "Our state’s growth demands serious investment in roads, bridges, and infrastructure."),
             ("sta-09", 1, SC_WILSON("Expanding Access to Rural Healthcare"), "Wilson will support rural clinics, expand telemedicine, and incentive medical professionals to serve under-served areas."),
             ("imm-08", 1, SC_WILSON("Protecting Our Border and Enforcing the Law"), "As Governor, Wilson will deny state benefits to illegal residents, enforce immigration law, and back state and local efforts to support federal immigration authorities"),
             ("eco-02", 2, SC_WILSON("Lowering Taxes, Growing the Economy"), "He will fight to eliminate the state income tax to reduce the overall tax burden on South Carolina families."),
             ("soc-06", 2, SC_WILSON("Defending Constitutional Freedoms"), "Wilson is a fierce defender of the Second Amendment, private property rights, and religious liberty."),
             ("soc-01", 1, SC_WILSON("Defending Constitutional Freedoms"), "fight for legislation that ensures every citizen can speak freely and live according to their values"),
             ("gov-12", 2, SC_WILSON("Fighting for Accountability and Conservative Reform"), "He will overhaul state government by conducting rigorous audits, enforcing conservative reforms, and ensuring that every dollar in the state budget delivers value")),
        cand("SC-GOV:johnson", "Jermaine Johnson", "https://johnsonforsc.com/",
             ("eco-02", 2, SC_JOHNSON("Affordability"), "It is time to reduce the tax burden on our working class."),
             ("eco-12", 1, SC_JOHNSON("Affordability"), "Jermaine’s plan is to increase the amount of families who are not paying income tax to 70%."),
             ("sta-04", 1, SC_JOHNSON("Affordability"), "Plain and simple, Jermaine will work with municipalities to reduce property taxes for working families."),
             ("hou-01", 2, SC_JOHNSON("Affordability"), "Jermaine will fund a grant program that allows municipalities to convert existing structures into affordable housing units."),
             ("sta-03", 1, SC_JOHNSON("Affordability"), "They will be responsible for: recommending a state minimum wage"),
             ("eco-09", 1, SC_JOHNSON("Affordability"), "fighting against dishonest corporate wage theft"),
             ("sta-01", 2, SC_JOHNSON("Infrastructure"), "Jermaine wrote a bill that will allow municipalities the ability to fix their own roads and bridges with money from the state’s Department of Transportation."),
             ("sta-08", 2, SC_JOHNSON("Infrastructure"), "Jermaine would raise the salaries for and hire additional state and local law enforcement officers around the state"),
             ("sta-09", 2, SC_JOHNSON("Infrastructure"), "Jermaine will fund the opening of more rural hospitals across South Carolina to provide much needed care for our citizens."),
             ("sta-07", 2, SC_JOHNSON("Infrastructure"), "As governor, Jermaine will increase the focus and funding for trade schools and tech academies."),
             ("sta-02", 1, SC_JOHNSON("Families"), "It is time to invest in South Carolina’s public education."),
             ("hea-06", 2, SC_JOHNSON("Families"), "It is time to invest in South Carolinians’ mental health."),
             ("eco-11", 1, SC_JOHNSON("Families"), "As Governor, Jermaine would incentivize employers to offer paid family leave for fathers"),
             ("gov-12", 1, SC_WPDE("Johnson would order audits and oversight committees"), "I can use my executive order to get a lot of things done and get some audits going"))]},
    {"id": "OK-GOV", "candidates": [cand(
        "OK-GOV:mazzei", "Mike Mazzei", "https://mikeforok.com/",
        ("sta-11", 1, OK_MAZZEI("Eliminating Property Tax for Seniors and Veterans"), "Eliminate special interest property tax breaks for green energy and data centers"),
        ("gov-12", 1, OK_MAZZEI_ISSUES("Government Accountability"), "Taxpayers deserve transparency, discipline, and results."))]},
    {"id": "OK-SEN", "candidates": [cand(
        "OK-SEN:thomas", "N’Kiyla Jasmine Thomas", "https://www.jasmineforok.com/",
        ("hea-01", 2, OK_THOMAS("Healthcare & Public Health"), "Establish Medicare for All to guarantee universal healthcare coverage for every American"),
        ("hea-03", 2, OK_THOMAS("Healthcare & Public Health"), "Establish Medicare for All to guarantee universal healthcare coverage for every American"),
        ("hea-04", -1, OK_NONDOC("Thomas aims for a single-payer Medicare for All system"), None),
        ("hea-05", 2, OK_KOSU("Thomas on her priorities"), "make sure that we start funding and putting in the resources into our hospitals, getting their funding for their research, such as cancer, autism"),
        ("hea-06", 1, OK_THOMAS("Healthcare & Public Health"), "Protect and expand access to healthcare services, including primary care, preventative care, mental healthcare, reproductive healthcare, and prescription medications."),
        ("hea-09", 1, OK_THOMAS("Healthcare & Public Health"), "Protect and expand access to healthcare services, including primary care, preventative care, mental healthcare, reproductive healthcare, and prescription medications."),
        ("soc-03", 2, OK_THOMAS("Reproductive Rights & Women’s Health"), "Restore Roe v. Wade federally"),
        ("soc-04", -2, OK_THOMAS("Reproductive Rights & Women’s Health"), "Decisions about pregnancy belong to patients, not politicians."),
        ("soc-07", 2, OK_THOMAS("Childcare & Family Support"), "Universal, affordable childcare — including 24/7 options"),
        ("soc-02", 2, OK_THOMAS("Civil Rights & LGBTQIA+ Protections"), "Expand anti-discrimination protections"),
        ("soc-10", 2, OK_THOMAS("Civil Rights & LGBTQIA+ Protections"), "Codify marriage equality"),
        ("soc-12", 2, OK_THOMAS("Civil Rights & LGBTQIA+ Protections"), "Protect trans youth and their families"),
        ("eco-03", 2, OK_THOMAS("Economic Justice & Cost of Living"), "A living wage minimum wage"),
        ("eco-09", 1, OK_KOSU("Thomas on her advocacy"), "nurses, nursing unions, making sure that we actually have a lunch, we get paid for the time that we’re on the clock"),
        ("eco-11", 2, OK_THOMAS("Childcare & Family Support"), "Paid family and medical leave"),
        ("eco-13", 1, OK_THOMAS("Workers’ Rights & Labor"), "32-hour, full-pay workweek pilot programs"),
        ("hou-01", 1, OK_THOMAS("Economic Justice & Cost of Living"), "Investment in affordable housing"),
        ("hou-06", 1, OK_THOMAS("Credit, Housing & Consumer Protection"), "Strong protections against exploitative landlords"),
        ("edu-01", 1, OK_THOMAS("Education"), "Fully fund special education"),
        ("edu-04", 1, OK_THOMAS("Education"), "Ensure competitive teacher pay and retention"),
        ("edu-09", 2, OK_THOMAS("Education"), "Guarantee free breakfast and lunch for all students"),
        ("ene-04", 2, OK_THOMAS("Environmental Protection"), "Strengthen the Clean Water Act"),
        ("def-03", 1, OK_THOMAS("Military Veterans & Families"), "Improve staffing and access in veteran healthcare systems"))]},
    {"id": "RI-SEN", "candidates": [cand(
        "RI-SEN:mckay", "Raymond McKay", "https://www.mckayforussenate.com/",
        ("ene-02", 1, RI_MCKAY("Grow Our Economy for the Benefit of All"), "work together for long-term strength and stability of our nuclear and fossil fuel industries"),
        ("ene-03", 1, RI_MCKAY("Grow Our Economy for the Benefit of All"), "work together for long-term strength and stability of our nuclear and fossil fuel industries"),
        ("eco-07", 2, RI_MCKAY("Strengthen Social Security & Medicare"), "Stop government’s deficit spending, Balance the budget."),
        ("imm-01", 1, RI_MCKAY("Secure Our Borders"), "Ray is committed to addressing responsible immigration and enforcement policies that consider the best interest of Rhode Islanders and Americans First."))]},
]

write("data/research/positions.json", races,
      "Positions from campaign sites and news coverage for candidates who had few; researched Oct. 25, 2026.", updated=READ)
