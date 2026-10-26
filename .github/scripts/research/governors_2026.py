"""Researched positions for safe 2026 governor races. Writes
data/research/governors.json.

Each race's positions come from coverage of the candidates' debates and
campaigns, and from bills incumbents signed. Researched Oct. 25, 2026.

    py scripts/research/governors_2026.py
"""

from common import P, article, write

READ = "2026-10-25"

# California
CA_DEBATE = article("ABC30 debate report, Oct. 1, 2026", "https://abc30.com/post/xavier-becerra-steve-hilton-clash-key-issues-california-gubernatorial-debate/19894941/", "2026-10-01")
CA_AP = article("Associated Press debate report via Scripps News, Oct. 1, 2026", "https://www.scrippsnews.com/politics/america-votes/california-governor-rivals-clash-over-costs-homelessness-and-trump-in-only-debate", "2026-10-01")
CA_SCHOOLS = article("EdSource debate report, Oct. 1, 2026", "https://edsource.org/2026/california-debate-becerra-hilton-education/767280", "2026-10-01")

# Pennsylvania
PA_SPOTLIGHT = article("Spotlight PA debate report, Oct. 7, 2026", "https://www.spotlightpa.org/news/2026/10/josh-shapiro-stacy-garrity-pennsylvania-governor-debate-elections/", "2026-10-07")
PA_FOX = article("FOX 29 debate report, Oct. 8, 2026", "https://fox29.com/news/shapiro-garrity-debate-recap-key-takeaways-from-pa-governors-race", "2026-10-08")

# New York
NY_SPECTRUM = article("Spectrum News debate report, Oct. 14, 2026", "https://spectrumlocalnews.com/nys/central-ny/politics/2026/10/14/hochul-and-blakeman-trade-barbs-in-only-governor-debate", "2026-10-14")
NY_NBC = article("NBC New York debate report, Oct. 13, 2026", "https://www.nbcnewyork.com/news/politics/hochul-blakeman-debate-ny-governor-race-recap-key-moments/6559134/", "2026-10-13")

# Illinois
IL_DEBATE = article("Chicago Sun-Times debate report, Oct. 14, 2026", "https://www.nprillinois.org/government-politics/2026-10-14/6-takeaways-from-the-only-gubernatorial-debate-between-gov-pritzker-and-darren-bailey", "2026-10-14")
IL_PREVIEW = article("Chicago Sun-Times, Oct. 13, 2026", "https://chicago.suntimes.com/elections/2026/10/13/jb-pritzker-darren-bailey-collin-corbett-illinois-governor-election-november-midterm", "2026-10-13")

# Massachusetts
MA_DEBATE = article("Boston.com debate report, Oct. 16, 2026", "https://www.boston.com/news/politics/2026/10/16/healey-and-minogue-made-their-final-pitches-to-voters-in-a-tense-debate-here-are-4-takeaways/", "2026-10-16")

# Maryland
MD_MATTERS = article("Maryland Matters debate report, Oct. 6, 2026", "https://www.newsfromthestates.com/article/moore-and-cox-bring-heat-debate-will-it-alter-race", "2026-10-06")

# Connecticut
CT_MIRROR = article("CT Mirror, July 9, 2026", "https://ctmirror.org/2026/07/09/fazio-housing-transportation-energy-election/", "2026-07-09")

# Arkansas
AR_DEBATE = article("Arkansas Advocate debate report, Oct. 13, 2026", "https://www.newsfromthestates.com/article/challengers-call-arkansas-governors-policy-priorities-misplaced-debate", "2026-10-13")

# Idaho
ID_FORUM = article("Idaho Capital Sun forum report, Oct. 6, 2026", "https://idahocapitalsun.com/2026/10/06/pickens-stegner-pledge-policy-changes-in-idaho-gubernatorial-candidate-forum/", "2026-10-06")

# South Dakota
SD_FAIR = article("South Dakota Searchlight debate report, Sept. 5, 2026", "https://southdakotasearchlight.com/2026/09/05/south-dakota-governor-challenger-both-slam-trump-on-beef-imports-but-clash-on-other-debate-topics/", "2026-09-05")
SD_SDPB = article("South Dakota Searchlight debate report, Sept. 29, 2026", "https://www.newsfromthestates.com/article/south-dakota-governor-candidates-clash-data-centers-education-economic-development", "2026-09-29")

# Hawaii
HI_BEAT = article("Honolulu Civil Beat, Oct. 4, 2026", "https://www.civilbeat.org/2026/10/cordery-runs-against-hawaii-gov-josh-green/", "2026-10-04")

# Colorado
CO_DEBATE = article("Colorado Newsline debate report, Aug. 27, 2026", "https://coloradonewsline.com/2026/08/27/weiser-lopez-colorado-debate-marx-absent/", "2026-08-27")

# Rhode Island
RI_DEBATE_1 = article("NBC 10 debate report, Oct. 7, 2026", "https://turnto10.com/politics/foulkes-guckian-block-spar-over-housing-morales-abortion-gubernatorial-debate-october-7-2026", "2026-10-07")
RI_DEBATE_2 = article("NBC 10 debate report, Oct. 20, 2026", "https://turnto10.com/politics/foulkes-guckian-and-block-debate-housing-health-care-in-final-televised-matchup-october-20-2026", "2026-10-20")

# Connecticut (Lamont) and Wyoming
CT_WFSB = article("WFSB, Aug. 20, 2026", "https://www.wfsb.com/2026/08/20/lamont-fazio-spar-over-housing-legislation-governors-race-heats-up/", "2026-08-20")
WY_DEBATE = article("WyoFile debate report, Oct. 15, 2026", "https://www.newsfromthestates.com/article/four-takeaways-wyoming-governors-debate", "2026-10-15")

races = [
    {"id": "CA-GOV", "candidates": [
        {"id": "CA-GOV:becerra", "name": "Xavier Becerra", "party": "D",
         "bio": "U.S. secretary of health and human services from 2021 to 2025 and earlier California attorney general.",
         "positions": P(
             ("edu-06", -2, CA_SCHOOLS("Becerra would keep public school money in public schools and opposes Hilton's voucher-style accounts"), "those dollars, taxpayer dollars, stay in our public schools"),
             ("edu-04", 1, CA_SCHOOLS("Becerra says teachers are underpaid"), None),
             ("hea-09", 2, CA_SCHOOLS("Becerra firmly backs California's school vaccine requirements"), "We know vaccines work."))},
        {"id": "CA-GOV:hilton", "name": "Steve Hilton", "party": "R",
         "bio": "Former Fox News host and adviser to British Prime Minister David Cameron.",
         "positions": P(
             ("eco-02", 2, CA_AP("Hilton would end state income tax on the first $150,000 of earnings"), None),
             ("edu-06", 2, CA_SCHOOLS("Hilton proposes savings accounts letting parents spend public school money at schools of their choice"), None),
             ("imm-07", 2, CA_AP("Hilton would prioritize removing dangerous criminals while protecting legal immigrant communities"), None),
             ("sta-12", -2, CA_DEBATE("Hilton would cancel California's high-speed rail project"), "Canceling high-speed rail"),
             ("hou-07", -2, CA_DEBATE("Hilton would cancel California's high-speed rail project"), None))},
    ]},
    {"id": "PA-GOV", "candidates": [
        {"id": "PA-GOV:shapiro", "name": "Josh Shapiro", "party": "D",
         "bio": "Governor of Pennsylvania since 2023 and earlier state attorney general.",
         "positions": P(
             ("cri-09", -2, PA_FOX("Shapiro no longer supports the death penalty"), "the state should not be in the business of putting people to death."),
             ("edu-06", 1, PA_FOX("Shapiro says he believes in school choice and would sign a bill both chambers agree on"), "Put the bill on my desk, and I'll sign it into law."),
             ("sta-02", 2, PA_SPOTLIGHT("Shapiro defends his increases in school spending"), "Graduation rates are up and truancy is down and it is working."),
             ("edu-09", 2, PA_SPOTLIGHT("Shapiro defends free school breakfast for all students"), None),
             ("hou-03", 2, PA_SPOTLIGHT("Shapiro would tax skill games and put much of the money into mass transit"), None),
             ("edu-03", 1, PA_SPOTLIGHT("Shapiro defends funding for apprenticeships and vo-tech"), None),
             ("gov-05", 1, PA_SPOTLIGHT("Shapiro would sign a voter ID bill that doesn't disenfranchise voters"), "I'm open to putting a voter ID bill on my desk for my signature."))},
        {"id": "PA-GOV:garrity", "name": "Stacy Garrity", "party": "R",
         "bio": "Pennsylvania state treasurer since 2021 and a retired Army Reserve colonel.",
         "positions": P(
             ("edu-06", 2, PA_SPOTLIGHT("Garrity would join the federal private school tax credit program on her first day"), "parents, not bureaucrats, know the best way to educate their kids."),
             ("cri-09", 1, PA_FOX("Garrity supports enforcing Pennsylvania's death penalty"), None),
             ("hea-03", -2, PA_SPOTLIGHT("Garrity supports the federal Medicaid cuts and would require healthy adults without young children to work, train or volunteer"), None),
             ("gov-05", 2, PA_SPOTLIGHT("Garrity supports requiring voter ID for all voters"), None),
             ("sta-02", -1, PA_SPOTLIGHT("Garrity opposes adding school money without better results"), "we can't just keep throwing more money at an issue."),
             ("eco-02", 1, PA_SPOTLIGHT("Garrity proposes a $750 summer rebate for drivers and a pause in gas and diesel taxes"), None),
             ("hea-09", 1, PA_SPOTLIGHT("Garrity says she is vaccinated and supports vaccines"), None))},
    ]},
    {"id": "NY-GOV", "candidates": [
        {"id": "NY-GOV:hochul", "name": "Kathy Hochul", "party": "D",
         "bio": "Governor of New York since 2021.",
         "positions": P(
             ("imm-08", -1, NY_SPECTRUM("Hochul criticizes ICE operations in Nassau County"), "ICE is out of control, it's out of control in Nassau County."),
             ("eco-10", -1, NY_SPECTRUM("Hochul blames the administration's tariffs for higher farm costs"), None))},
        {"id": "NY-GOV:blakeman", "name": "Bruce Blakeman", "party": "R",
         "bio": "Nassau County executive since 2022.",
         "positions": P(
             ("soc-03", 1, NY_NBC("Blakeman calls himself pro-choice"), None),
             ("imm-08", 1, NY_SPECTRUM("Blakeman defends Nassau County's cooperation with federal immigration authorities and blames New York's sanctuary policy"), "Kathy Hochul has made us a sanctuary state."),
             ("cri-06", -2, NY_SPECTRUM("Blakeman blames cashless bail and other criminal justice changes for crime"), "a revolving door of criminality, cashless bail, raise the age"))},
    ]},
    {"id": "IL-GOV", "candidates": [
        {"id": "IL-GOV:pritzker", "name": "JB Pritzker", "party": "D",
         "bio": "Governor of Illinois since 2019, seeking a third term.",
         "positions": P(
             ("hea-01", 2, IL_DEBATE("Pritzker on health care"), "I've been fighting for universal health care."),
             ("cri-06", 2, IL_DEBATE("Pritzker opposes returning to cash bail and says judges and prosecutors should decide pretrial release"), None),
             ("sta-08", 1, IL_DEBATE("Pritzker wants more state police"), None),
             ("soc-03", 2, IL_PREVIEW("Pritzker signed a series of laws making Illinois a haven for abortion care"), None),
             ("eco-12", 2, IL_PREVIEW("Pritzker spent $58 million backing the failed 2020 amendment for a graduated income tax"), None),
             ("sta-03", 2, IL_PREVIEW("Pritzker raised the state minimum wage to $15 an hour"), None),
             ("soc-05", 2, IL_PREVIEW("Pritzker shepherded the legalization of recreational marijuana"), None),
             ("sta-01", 2, IL_PREVIEW("Pritzker championed a $45 billion infrastructure plan"), None))},
        {"id": "IL-GOV:bailey", "name": "Darren Bailey", "party": "R",
         "bio": "Former Illinois state senator and the 2022 Republican nominee for governor.",
         "positions": P(
             ("cri-06", -2, IL_DEBATE("Bailey would repeal the SAFE-T Act, which ended cash bail, and renegotiate it with police and prosecutors"), "We need to repeal it"),
             ("soc-03", -2, IL_PREVIEW("Bailey staunchly opposes abortion rights"), None))},
    ]},
    {"id": "MA-GOV", "candidates": [
        {"id": "MA-GOV:healey", "name": "Maura Healey", "party": "D",
         "bio": "Governor of Massachusetts since 2023 and earlier state attorney general.",
         "positions": P(
             ("soc-03", 2, MA_DEBATE("Healey signed a law in August 2026 expanding abortion protections and shields providers from out-of-state legal action"), "I trust women and their doctors."),
             ("hou-04", 1, MA_DEBATE("Healey says she cut housing permit times from a year to 30 days"), None),
             ("ene-01", 1, MA_DEBATE("Healey backs an all-of-the-above energy mix of natural gas, wind, solar, geothermal and hydropower"), None),
             ("imm-08", -1, MA_DEBATE("Healey opposes the administration's immigration enforcement actions"), None),
             ("eco-02", 1, MA_DEBATE("Healey cites the tax relief she signed"), None))},
        {"id": "MA-GOV:minogue", "name": "Mike Minogue", "party": "R",
         "bio": "Former medical device company chief executive, running for office for the first time.",
         "positions": P(
             ("soc-03", -1, MA_DEBATE("Minogue is pro-life but says he would follow Massachusetts law"), "I will follow the law."),
             ("ene-03", 1, MA_DEBATE("Minogue wants more natural gas pipeline capacity"), None),
             ("ene-01", -1, MA_DEBATE("Minogue criticizes the state's reliance on wind and solar"), None),
             ("ene-02", 1, MA_DEBATE("Minogue wants more focus on nuclear power"), None),
             ("hou-04", 1, MA_DEBATE("Minogue would give towns financial incentives to ease building requirements"), None),
             ("imm-08", 1, MA_DEBATE("Minogue wants local, state and federal authorities to cooperate on immigration enforcement"), "cooperate with local, state, and federal authorities"))},
    ]},
    {"id": "MD-GOV", "candidates": [
        {"id": "MD-GOV:moore", "name": "Wes Moore", "party": "D",
         "bio": "Governor of Maryland since 2023.",
         "positions": P(
             ("eco-10", -1, MD_MATTERS("Moore says Maryland is fighting the administration's tariffs"), None),
             ("hea-03", 1, MD_MATTERS("Moore says Maryland is fighting the federal health care cuts"), None))},
        {"id": "MD-GOV:cox", "name": "Dan Cox", "party": "R",
         "bio": "Former Maryland state delegate and the 2022 Republican nominee for governor.",
         "positions": P(
             ("eco-01", -1, MD_MATTERS("Cox pledges no new taxes or fees"), "I will not raise taxes and fees on my watch."))},
    ]},
    {"id": "CT-GOV", "candidates": [
        {"id": "CT-GOV:lamont", "name": "Ned Lamont", "party": "D",
         "bio": "Governor of Connecticut since 2019, seeking a third term.",
         "positions": P(
             ("hou-04", 1, CT_WFSB("Lamont backs the 2025 law requiring towns to plan for more housing"), None),
             ("eco-11", 1, CT_WFSB("Lamont says he is strengthening paid family leave for working parents"), None))},
        {"id": "CT-GOV:fazio", "name": "Ryan Fazio", "party": "R",
         "bio": "Connecticut state senator from Greenwich.",
         "positions": P(
             ("eco-02", 1, CT_MIRROR("Fazio would lower state income taxes"), None),
             ("sta-04", 2, CT_MIRROR("Fazio would cap future property tax rate increases and raise state education grants to towns"), None),
             ("sta-11", 1, CT_MIRROR("Fazio would reduce property tax exemptions for private universities and hospitals"), None),
             ("hou-04", 1, CT_MIRROR("Fazio would allow homes in mixed-use areas and reform single-stairwell rules"), None),
             ("ene-10", 1, CT_MIRROR("Fazio would cut electric bills 15% to 20%"), "cut out-of-control costs like energy costs and energy bills"))},
    ]},
    {"id": "AR-GOV", "candidates": [
        {"id": "AR-GOV:sanders", "name": "Sarah Huckabee Sanders", "party": "R",
         "bio": "Governor of Arkansas since 2023 and White House press secretary from 2017 to 2019.",
         "positions": P(
             ("edu-06", 2, AR_DEBATE("Sanders defends the voucher program created by her 2023 LEARNS Act"), "What's not fair is trapping kids in failing schools"),
             ("edu-04", 1, AR_DEBATE("Sanders points to the teacher pay raises in the LEARNS Act"), None),
             ("hea-03", -1, AR_DEBATE("Sanders backs Medicaid work requirements and opposes extending postpartum Medicaid to 12 months"), None),
             ("eco-02", 1, AR_DEBATE("Sanders touts her record of tax cuts"), None))},
        {"id": "AR-GOV:love", "name": "Fredrick Love", "party": "D",
         "bio": "Arkansas state senator from Little Rock.",
         "positions": P(
             ("edu-06", -2, AR_DEBATE("Love would end the school voucher program by executive order"), None),
             ("hea-03", 2, AR_DEBATE("Love would invest more in hospitals and Medicaid and supports 12-month postpartum coverage"), None),
             ("eco-02", 1, AR_DEBATE("Love supports suspending the state gas tax"), None))},
    ]},
    {"id": "ID-GOV", "candidates": [
        {"id": "ID-GOV:little", "name": "Brad Little", "party": "R",
         "bio": "Governor of Idaho since 2019, seeking a third term.",
         "positions": P(
             ("edu-06", 2, ID_FORUM("Little signed the Idaho Parental Choice Tax Credit for private school and homeschool costs (H.B. 93, 2025)"), None))},
        {"id": "ID-GOV:pickens", "name": "Terri Pickens", "party": "D",
         "bio": "Trial attorney and small business owner; the 2022 Democratic nominee for lieutenant governor.",
         "positions": P(
             ("hea-03", 2, ID_FORUM("Pickens's first budget would restore Medicaid expansion funding cut in 2026"), "It's going to restore Medicaid expansion."),
             ("hea-06", 1, ID_FORUM("Pickens would restore mental health funding"), None),
             ("sta-02", 2, ID_FORUM("Pickens would restore full funding for public schools"), None),
             ("soc-03", 2, ID_FORUM("Pickens supports Proposition 1, restoring the right to an abortion in Idaho"), None),
             ("imm-08", -2, ID_FORUM("Pickens would sign no 287(g) agreements and give ICE no state resources"), "I don't think we need to be providing them with state resources"),
             ("gov-10", 1, ID_FORUM("Pickens opposes HJR 4, which would bar voters from legalizing marijuana by ballot initiative"), None))},
        {"id": "ID-GOV:stegner", "name": "John Stegner", "party": "I",
         "bio": "Retired Idaho Supreme Court justice, running as an independent.",
         "positions": P(
             ("edu-06", -2, ID_FORUM("Stegner would try to repeal the Parental Choice Tax Credit and challenge it in court"), None),
             ("soc-03", 2, ID_FORUM("Stegner supports Proposition 1, restoring the right to an abortion in Idaho"), None),
             ("imm-08", -2, ID_FORUM("Stegner would not have signed the state's 287(g) agreement with ICE"), None),
             ("gov-10", 1, ID_FORUM("Stegner opposes HJR 4, which would bar voters from legalizing marijuana by ballot initiative"), None))},
    ]},
    {"id": "SD-GOV", "candidates": [
        {"id": "SD-GOV:rhoden", "name": "Larry Rhoden", "party": "R",
         "bio": "Governor of South Dakota since 2025, a western South Dakota rancher and former lieutenant governor.",
         "positions": P(
             ("sta-04", 2, SD_SDPB("Rhoden signed property tax cuts he says will lower the average homeowner's bill 36% (2026)"), "the largest property tax cut in the history of the state"),
             ("sta-02", 1, SD_SDPB("Rhoden says state school funding has risen faster than the formula requires"), None),
             ("hea-03", -1, SD_FAIR("Rhoden opposed Medicaid expansion over fears federal funding will be pulled"), None),
             ("eco-10", 1, SD_FAIR("Rhoden opposes the administration's pause on tariffs for imported beef"), None))},
        {"id": "SD-GOV:ahlers", "name": "Dan Ahlers", "party": "D",
         "bio": "Small business owner and former Democratic state legislator from Dell Rapids.",
         "positions": P(
             ("hea-03", 2, SD_FAIR("Ahlers opposes rolling back the voter-approved Medicaid expansion"), "when we have healthcare, and everyone has access to it, we all do better"),
             ("edu-09", 2, SD_SDPB("Ahlers would have the state pay for school lunches"), None),
             ("soc-07", 1, SD_SDPB("Ahlers proposes a child care tax credit or rebate"), None),
             ("edu-04", 1, SD_SDPB("Ahlers says the state should prioritize teacher pay"), None),
             ("sta-02", 2, SD_SDPB("Ahlers would put more state money into schools to ease property taxes"), None),
             ("sta-04", 1, SD_SDPB("Ahlers would expand property tax relief for seniors, veterans and people with disabilities"), None))},
    ]},
    {"id": "HI-GOV", "candidates": [
        {"id": "HI-GOV:green", "name": "Josh Green", "party": "D",
         "bio": "Governor of Hawaii since 2022, a physician and former lieutenant governor.",
         "positions": P(
             ("hou-01", 1, HI_BEAT("Green's campaign says he will build more housing and reduce homelessness"), None),
             ("eco-02", -1, HI_BEAT("Green proposed freezing the 2024 income tax cuts to help balance future budgets"), None))},
        {"id": "HI-GOV:cordery", "name": "Gary Cordery", "party": "R",
         "bio": "Hawaii contractor.",
         "positions": P(
             ("soc-03", -2, HI_BEAT("Cordery would sign a bill overturning abortion rights"), "I would sign it"),
             ("soc-04", 2, HI_BEAT("Cordery would sign a bill overturning abortion rights"), None),
             ("hea-09", -2, HI_BEAT("Cordery opposes any government vaccine requirement and urged people to reject vaccines"), "You MUST reject all vaccines, PERIOD."),
             ("eco-02", 2, HI_BEAT("Cordery would end the state excise tax on food and opposes freezing the 2024 income tax cuts"), None),
             ("sta-04", 1, HI_BEAT("Cordery would freeze property taxes at retirement age for homeowners"), None),
             ("ene-06", -1, HI_BEAT("Cordery says the climate change agenda adds costs and needs review"), None))},
    ]},
    {"id": "CO-GOV", "candidates": [
        {"id": "CO-GOV:weiser", "name": "Phil Weiser", "party": "D",
         "bio": "Colorado attorney general since 2019.",
         "positions": P(
             ("hou-04", 1, CO_DEBATE("Weiser would push towns to cut permit fees and reward building starter homes, balancing state mandates and local control"), None),
             ("hea-09", 1, CO_DEBATE("Weiser would expand free primary care"), None),
             ("eco-04", 2, CO_DEBATE("Weiser sued to block the Kroger-Albertsons grocery merger"), None),
             ("gov-06", 1, CO_DEBATE("Weiser opposes federal efforts to interfere with mail ballots"), None))},
    ]},
    {"id": "RI-GOV", "candidates": [
        {"id": "RI-GOV:foulkes", "name": "Helena Foulkes", "party": "D",
         "bio": "Former CVS Health executive and president of Hudson's Bay Company.",
         "positions": P(
             ("hou-01", 2, RI_DEBATE_2("Foulkes would build 20,000 homes for the middle class, paid for by the state's new tax on income over $1 million"), "I want to build housing for the middle class, housing they can afford."),
             ("eco-01", 1, RI_DEBATE_1("Foulkes backs using the tax on income over $1 million for housing and says tax cuts aren't realistic now"), None),
             ("soc-12", 2, RI_DEBATE_1("Foulkes supports letting transgender girls play girls' sports"), None),
             ("imm-08", -2, RI_DEBATE_1("Foulkes on immigration enforcement"), "ICE is not welcome when I am governor."),
             ("hea-07", 1, RI_DEBATE_2("Foulkes would fight to preserve the Affordable Care Act and help residents keep their benefits"), None))},
        {"id": "RI-GOV:block", "name": "Ken Block", "party": "I",
         "bio": "Software entrepreneur and founder of the Moderate Party, running as an independent.",
         "positions": P(
             ("soc-03", 2, RI_DEBATE_1("Block supports abortion rights"), "I am pro-choice, I have always been pro-choice."),
             ("soc-12", -1, RI_DEBATE_1("Block opposes transgender girls playing in girls' sports"), None),
             ("hou-01", 1, RI_DEBATE_2("Block would have the state acquire land and work with towns and developers to build housing"), "we will build the units we need"))},
        {"id": "RI-GOV:guckian", "name": "Aaron Guckian", "party": "R",
         "positions": P(
             ("eco-02", 1, RI_DEBATE_2("Guckian pledges to lower taxes and fees, including the tax on second homes"), None),
             ("soc-12", -1, RI_DEBATE_1("Guckian opposes transgender girls playing in girls' sports"), None),
             ("imm-08", 1, RI_DEBATE_1("Guckian says ICE would be welcome in Rhode Island"), "We need to get the bad actors out."),
             ("hou-04", 1, RI_DEBATE_2("Guckian would appoint a permitting czar to cut red tape for housing"), None))},
    ]},
    {"id": "WY-GOV", "candidates": [
        {"id": "WY-GOV:barlow", "name": "Eric Barlow", "party": "R",
         "bio": "Wyoming state senator from Gillette.",
         "positions": P(
             ("sta-04", 0, WY_DEBATE("Barlow opposes Proposition 1's new residential property tax exemption, citing the local services it funds and earlier property tax cuts"), None))},
    ]},
]

write("data/research/governors.json", races, "Safe 2026 governor races, researched Oct. 25, 2026.", updated=READ)
