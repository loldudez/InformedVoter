"""Researched bios and positions for candidates who had none: mostly third-party and
independent candidates for Senate and governor, and House candidates, from their
own campaign sites (read Oct. 26, 2026) and, where a site says little, news
reports. Writes data/research/candidates.json.

Each file entry covers only some of a race's candidates, so it is marked `partial`:
it adds positions without making the race "researched" (update_races.py), which
would switch on side-by-side matching. A stance goes in only where the page states
it; anything else stays "unclear".

    py scripts/research/candidates_2026.py
"""

from common import P, page, write

READ = "2026-10-26"


def site(name, url):
    return lambda note: page(f"{name} campaign site: {note}", url, READ)


RACES = {}


def cand(race, cid, name, party, bio, *rows):
    out = {"id": cid, "name": name, "party": party}
    if bio:
        out["bio"] = bio
    if rows:
        out["positions"] = P(*rows)
    RACES.setdefault(race, []).append(out)


# Texas Senate: Ted Brown (Libertarian) ---------------------------------------------
BROWN = site("Ted Brown", "https://tedbrown.org/")
cand("TX-SEN", "TX-SEN:brown", "Ted Brown", "L",
     "Retired insurance adjuster from Austin and longtime Libertarian Party officer; the party’s 2024 Senate nominee in Texas.",
     ("eco-01", -2, BROWN("Brown would never vote to raise taxes and would repeal the income tax"), "I will never vote to raise taxes."),
     ("eco-12", -2, BROWN("Brown would repeal the federal income tax and abolish the IRS"), None),
     ("eco-02", 2, BROWN("Brown would repeal the income tax, returning an average $25,844 to each taxpayer"), None),
     ("eco-07", 2, BROWN("Brown would cut federal spending across the board"), "Cut it across the board"),
     ("eco-10", -2, BROWN("Brown would eliminate tariffs"), "Eliminate tariffs that act as taxes on American consumers"),
     ("agr-06", 2, BROWN("Brown supports free trade agreements that reduce barriers"), None),
     ("agr-07", -2, BROWN("Brown calls tariffs hidden taxes on consumers"), None),
     ("imm-08", -2, BROWN("Brown would abolish ICE"), "End the immigration police state and abolish ICE"),
     ("imm-01", -2, BROWN("Brown would end checkpoints and raids and allow free movement across borders"), None),
     ("imm-03", 2, BROWN("Brown would welcome all foreigners after checking for criminal records and diseases"), None),
     ("def-02", -2, BROWN("Brown would withdraw from NATO"), "Withdraw from NATO and other entangling alliances"),
     ("def-08", -2, BROWN("Brown would bring all troops home"), "Bring ALL troops home from foreign assignments"),
     ("def-10", 2, BROWN("Brown would end all foreign aid"), "End all foreign aid payments"),
     ("def-12", -2, BROWN("Brown would end all foreign aid payments"), None),
     ("def-13", -2, BROWN("Brown would end all foreign aid payments"), None),
     ("def-05", -2, BROWN("Brown would end all foreign military interventions and aid"), None),
     ("def-07", 2, BROWN("Brown favors non-intervention in other nations’ affairs"), None),
     ("def-04", 2, BROWN("Brown says only Congress can declare war"), "Only Congress can declare war"),
     ("hea-01", -2, BROWN("Brown says health care should come from free-market competition"), "Health care is not a right or a privilege."),
     ("hea-04", 2, BROWN("Brown favors free-market health care"), None),
     ("edu-06", 2, BROWN("Brown supports tuition tax credits, charter schools and homeschooling"), "Support charter schools and homeschooling"),
     ("soc-05", 2, BROWN("Brown would legalize marijuana"), "Remove marijuana from controlled substances schedule immediately"),
     ("soc-01", 2, BROWN("Brown opposes government censorship of the internet"), "I oppose any government censorship of the internet"),
     ("cri-09", -2, BROWN("Brown opposes the death penalty"), "I don't trust government officials enough to allow them to kill people."),
     ("cri-03", 1, BROWN("Brown would move police misconduct investigations to state attorneys general"), None))

# Arkansas -------------------------------------------------------------------------
WADLIN = site("Jeff Wadlin", "https://www.jeffwadlin.com/issues")
cand("AR-SEN", "AR-SEN:wadlin", "Jeff Wadlin", "L",
     "Bentonville engineer and businessman (Caterpillar, Capital One, Sam’s Club) running as a Libertarian.",
     ("eco-10", -2, WADLIN("Wadlin would eliminate broad tariffs"), "We should eliminate broad tariffs"),
     ("eco-04", 2, WADLIN("Wadlin would enforce antitrust laws and challenge anti-competitive mergers"), "Government should enforce antitrust laws, challenge anti-competitive mergers"),
     ("eco-02", 1, WADLIN("Wadlin supports lower taxes on labor"), None),
     ("eco-03", 1, WADLIN("Wadlin supports gradual, predictable minimum-wage increases"), None),
     ("eco-09", 1, WADLIN("Wadlin says workers should be free to organize and bargain collectively"), None),
     ("hea-01", 2, WADLIN("Wadlin’s goal is to cover everyone"), "My goal is straightforward: cover everyone"),
     ("agr-01", 1, WADLIN("Wadlin supports strong crop insurance and a durable farm bill"), "I support strong crop insurance and a durable Farm Bill"),
     ("agr-06", 1, WADLIN("Wadlin says trade policy should open markets"), None),
     ("def-07", 1, WADLIN("Wadlin would end wars of aggression"), None))
SHELBY = site("Colt Shelby", "https://www.colt4arkansas.org/platform")
SHELBY_ISSUES = site("Colt Shelby", "https://www.colt4arkansas.org/issues")
cand("AR-GOV", "AR-GOV:shelby", "Colt Shelby", "L",
     "Franklin County farmer who has managed oil and gas contracts for two decades; the Libertarian nominee.",
     ("edu-06", -2, SHELBY_ISSUES("Shelby opposes school voucher schemes"), "Colt opposes school voucher schemes"),
     ("gov-12", 2, SHELBY("Shelby would require real-time public disclosure of major state contracts and incentive deals"), None),
     ("sta-11", 2, SHELBY("Shelby wants a full public accounting of state incentive packages with cost and benefit numbers"), None),
     ("sta-06", 1, SHELBY("Shelby wants independent audits of large state contracts"), None),
     ("ene-10", 1, SHELBY_ISSUES("Shelby would put utility ratepayers first as data centers expand"), None))

# Arizona governor -----------------------------------------------------------------
HOURIHAN_FAM = site("Teri Hourihan", "https://teriann4azgov.org/family-policy")
HOURIHAN_ABORT = site("Teri Hourihan", "https://teriann4azgov.org/abortion-law-1")
HOURIHAN_PLAN = site("Teri Hourihan", "https://teriann4azgov.org/teris-plans-policy")
cand("AZ-GOV", "AZ-GOV:hourihan", "Teri Hourihan", "No Labels",
     "Mother and first-time candidate, the No Labels nominee.",
     ("soc-07", 2, HOURIHAN_FAM("Hourihan would implement free universal child care modeled on New Mexico’s"), None),
     ("hea-06", 2, HOURIHAN_FAM("Hourihan would expand access to mental health treatment"), None),
     ("soc-03", 1, HOURIHAN_ABORT("Hourihan would preserve Arizona’s voter-approved abortion laws, and would also sign a born-alive bill"), "preserve Arizona’s current abortion laws"),
     ("ene-01", 1, HOURIHAN_PLAN("Hourihan would develop solar and wind infrastructure"), None),
     ("sta-11", 1, HOURIHAN_PLAN("Hourihan would end data centers’ tax cuts"), None))

# Colorado governor ----------------------------------------------------------------
MULDER = site("Eric Mulder", "https://www.mulderforgovernor.org/on-the-issues")
cand("CO-GOV", "CO-GOV:mulder", "Eric Mulder", "L",
     "Army veteran who served in Afghanistan as a chaplain’s assistant; the Libertarian nominee.",
     ("ene-03", 1, MULDER("Mulder would clear the path for greater energy production, including oil and gas permitting"), "Clear the path for greater energy production"),
     ("ene-01", 1, MULDER("Mulder would put solar on state buildings and support the wind industry"), None),
     ("ene-02", 1, MULDER("Mulder points to the promise of advanced nuclear power"), None),
     ("ene-10", 1, MULDER("Mulder says more affordable energy means a lower cost of living"), None))
UNDERWOOD = site("Erik Underwood", "https://erikunderwood.com/issues/")
cand("CO-GOV", "CO-GOV:underwood", "Erik Underwood", "Approval Voting",
     "Businessman and former U.S. Senate staffer who holds an AI technology patent; the Approval Voting Party nominee.",
     ("hea-01", 2, UNDERWOOD("Underwood has a plan for universal health care in Colorado"), "I have a plan for universal health care in Colorado"),
     ("edu-02", 2, UNDERWOOD("Underwood proposes free college and trade school"), None),
     ("soc-07", 2, UNDERWOOD("Underwood would fund child care with 25 cents per purchase"), None),
     ("hea-06", 1, UNDERWOOD("Underwood has a mental health plan"), None),
     ("hou-05", 1, UNDERWOOD("Underwood proposes affordable home loans with at most $2,500 down"), None),
     ("sta-12", 2, UNDERWOOD("Underwood proposes high-speed rail between Colorado’s cities"), None),
     ("soc-12", 1, UNDERWOOD("Underwood states his support for the LGBTQ+ community"), None),
     ("gov-03", 1, UNDERWOOD("Underwood would sue to make AIPAC register as a foreign agent"), None))

# Florida governor -----------------------------------------------------------------
ABRAMS = site("Dean Abrams", "https://deanabrams.com/")
cand("FL-GOV", "FL-GOV:abrams", "Dean Abrams", "I",
     "Sarasota technology and government-accountability consultant (Microsoft, HP, KPMG), paying for his own campaign.",
     ("sta-04", 2, ABRAMS("Abrams would end property tax on homesteads worth up to twice the county median"), "No property tax on homesteaded homes worth up to twice your county’s median."),
     ("hou-02", 2, ABRAMS("Abrams would stop corporations buying single-family homes"), "Corporations stop buying up single-family homes."),
     ("hea-03", 1, ABRAMS("Abrams would close the coverage gap for roughly 800,000 Floridians"), None))
cand("FL-GOV", "FL-GOV:burkett", "Charles Burkett", "I",
     "Lifelong Floridian and investor from Surfside, running with no party and taking no contributions.")
RUSSO = site("Frank Russo", "https://russo2026.com/priorities/")
cand("FL-GOV", "FL-GOV:russo", "Frank Russo", "I",
     "Insurance executive for more than 30 years, running as an independent.",
     ("edu-04", 2, RUSSO("Russo would raise the average teacher salary to at least $75,000"), "raise Florida’s average teacher salary to at least $75,000"),
     ("edu-03", 2, RUSSO("Russo would expand skilled trades, apprenticeships and career pathways"), None),
     ("sta-04", 1, RUSSO("Russo would pursue more property tax relief for homeowners"), None),
     ("hou-01", 1, RUSSO("Russo would build more housing working Floridians can afford"), None),
     ("sta-11", 1, RUSSO("Russo would demand measurable results where public incentives are involved"), None))

# Iowa Senate ----------------------------------------------------------------------
LAEHN = site("Thomas Laehn", "https://laehn4iowa.org/issues")
cand("IA-SEN", "IA-SEN:laehn", "Thomas Laehn", "L",
     "A prosecutor, running as a Libertarian against what he calls the two-party system itself.",
     ("gov-11", 2, LAEHN("Laehn would sponsor legislation to end the role of PACs and super PACs"), "eliminate the corrupting role of PACs and super PACs in our electoral system"),
     ("def-04", 2, LAEHN("Laehn would block wars declared by presidents without Congress’s consent"), "block foolish wars declared by presidents without the consent of Congress"),
     ("def-08", -2, LAEHN("Laehn would fight to bring troops home"), "I will fight to bring our men and women in uniform home"),
     ("def-07", 1, LAEHN("Laehn would save military strength for rare cases when vital interests are at stake"), None),
     ("eco-07", 2, LAEHN("Laehn would vote against any funding measure that adds to the debt and wants a balanced budget amendment"), "I will also fight for a balanced budget amendment to the Constitution"),
     ("imm-01", 1, LAEHN("Laehn says he will fight for a secure border"), "I will fight for a secure border."),
     ("imm-03", 1, LAEHN("Laehn would raise or eliminate caps on legal immigration"), "raise or to eliminate artificial caps on the number of people who can legally immigrate"),
     ("soc-05", 1, LAEHN("Laehn’s first bill would decriminalize marijuana possession and use"), "decriminalize the possession and use of marijuana"))

# Idaho ----------------------------------------------------------------------------
LOESBY = site("Matt Loesby", "https://www.loesby.us/platform/")
cand("ID-SEN", "ID-SEN:loesby", "Matt Loesby", "L", None,
     ("imm-03", -2, LOESBY("Loesby would close the border to immigrants not invited by U.S. citizen landowners"), "the United States border should be closed to any immigrants"),
     ("imm-02", -2, LOESBY("Loesby would deport any uninvited immigrant"), "Any uninvited immigrant should be deported"),
     ("imm-06", -2, LOESBY("Loesby would deport asylum seekers to the first safe country they passed through"), None),
     ("eco-03", -2, LOESBY("Loesby would push to repeal minimum wage laws"), None),
     ("hea-07", -2, LOESBY("Loesby would push to repeal programs like Obamacare"), None),
     ("eco-01", -1, LOESBY("Loesby would abolish the estate tax"), "I will fight to abolish the Death Tax"),
     ("def-08", -2, LOESBY("Loesby says no troops should be deployed outside U.S. territory"), "No member of the US military should be deployed anywhere outside US territory."),
     ("def-04", 2, LOESBY("Loesby says troops should stay home unless Congress declares war"), None),
     ("def-05", -2, LOESBY("Loesby says the U.S. should not finance other countries’ armies"), "the US should not spend a penny to finance other countries’ armies"),
     ("def-12", -2, LOESBY("Loesby says the U.S. should not finance other countries’ armies"), None),
     ("def-13", -2, LOESBY("Loesby says the U.S. should not finance other countries’ armies"), None))
FLEMING = site("Natalie Fleming", "https://nataliefleming.info/just-a-few-issues/")
FLEMING_POLICY = site("Natalie Fleming", "https://nataliefleming.info/policy/")
cand("ID-SEN", "ID-SEN:fleming", "Natalie Fleming", "I",
     "Independent who grew up partly in Moscow, worked in technology early on and raised four children as a single mother in the Treasure Valley.",
     ("soc-08", 2, FLEMING("Fleming would end mass surveillance and require explicit consent for data collection"), "We will end mass surveillance by corporations and government agencies, establish comprehensive data privacy rights"),
     ("gov-11", 2, FLEMING("Fleming would overturn Citizens United"), "We will end the corporate stranglehold by overturning Citizens United"),
     ("gov-13", -2, FLEMING("Fleming would overturn Citizens United and reform campaign finance"), None),
     ("gov-03", 1, FLEMING("Fleming would reform campaign finance and restore transparency"), None),
     ("edu-01", 1, FLEMING_POLICY("Fleming would fully fund education"), "If we have the money to bomb countries, we have the money to fully fund education"),
     ("edu-03", 1, FLEMING("Fleming would bring back trades and real-life skills in schools"), "Bring back trades, arts, civics, financial literacy, media literacy, and real life skills"),
     ("edu-10", 1, FLEMING("Fleming would bring back civics and financial literacy"), None),
     ("hea-06", 1, FLEMING("Fleming would expand mental health support for veterans and first responders"), "expand mental health support for veterans and first responders"),
     ("def-03", 1, FLEMING("Fleming would improve VA access and streamline benefits"), None),
     ("hou-02", 1, FLEMING("Fleming would curb corporate landlords"), "We will curb corporate landlords, restore affordability"),
     ("soc-06", 1, FLEMING("Fleming would protect religious freedom for all faiths"), "religious freedom for all faiths"),
     ("hea-01", 1, FLEMING("Fleming calls basic health care a question of human decency"), "basic health care is a question of human decency"))
SAND = site("Paul Sand", "https://paulsand.org/")
SAND_ABOUT = site("Paul Sand", "https://paulsand.org/about-me")
cand("ID-GOV", "ID-GOV:sand", "Paul Sand", "L",
     "Retired software engineer and builder from White Bird who served ten years on its city council; says his campaign is not backed by the Libertarian Party.",
     ("soc-04", 2, SAND("Sand says he is strongly opposed to abortion"), "I am strongly opposed to abortion, open borders, and legalizing narcotic drugs."),
     ("soc-03", -2, SAND("Sand says he is strongly opposed to abortion"), None),
     ("eco-02", 1, SAND("Sand supports substantial cuts in state taxes"), "I strongly support substantial reductions in state agencies and state taxes."),
     ("sta-10", -1, SAND("Sand opposes state policies meant to bring more businesses into Idaho"), "I am opposed to any state policies that are intended to bring more businesses and more people into Idaho."),
     ("hou-04", 1, SAND_ABOUT("Sand opposes land use restrictions"), "I oppose all land use restrictions"))

# Illinois governor ----------------------------------------------------------------
CORBETT = site("Collin Corbett", "https://www.collinforil.com/platform/")
CORBETT_HOPE = site("Collin Corbett", "https://www.collinforil.com/hope/")
cand("IL-GOV", "IL-GOV:corbett", "Collin Corbett", "I",
     "Palatine political strategist and small-business owner (Cor Strategies), running as an independent with Carolyn Schofield.",
     ("sta-04", 2, CORBETT("Corbett has a plan to cut property taxes, including a fund that rebates homeowners"), "finally deliver property tax relief for Illinois working families"),
     ("sta-02", 2, CORBETT("Corbett would fully fund schools through the state’s evidence-based formula"), "fully funding our schools through the Evidence-Based Funding (EBF) formula"),
     ("edu-01", 2, CORBETT("Corbett would fully fund schools through the state’s evidence-based formula"), None),
     ("eco-02", 1, CORBETT("Corbett would raise the state EITC and child tax credit once finances allow"), "increase the Earned Income Tax Credit and Child Tax Credit to reduce lower- and middle-income tax bills"),
     ("sta-11", 1, CORBETT("Corbett would make projects that get state tax breaks pay into a property tax fund"), None),
     ("eco-09", 1, CORBETT("Corbett says workers deserve to be paid well and protected"), "We recognize this is a strong union state where workers deserve to be paid well and be protected."),
     ("sta-06", 1, CORBETT_HOPE("Corbett would strengthen ethics rules"), "strengthen ethics so government works for the people again"),
     ("gov-12", 1, CORBETT_HOPE("Corbett promises more transparency and accountability in Springfield"), None),
     ("hou-01", 1, CORBETT_HOPE("Corbett would build new affordable housing"), "building new affordable, quality housing"))

# Kansas and Kentucky Senate -------------------------------------------------------
GRAHAM = site("David Graham", "https://grahamforliberty.com/")
cand("KS-SEN", "KS-SEN:graham", "David Graham", "L",
     "Solo-practice lawyer who grew up in a working-class Kansas home (Shawnee Mission North, Washburn, KU Law); the Libertarian nominee.",
     ("eco-07", 2, GRAHAM("Graham would vote against bailouts and pork to stop the spending"), "David will vote no on the bailouts, the pork, and the agencies nobody can explain"),
     ("gov-02", 2, GRAHAM("Graham would ban congressional stock trading"), "David will vote to ban congressional stock trading"),
     ("gov-09", 2, GRAHAM("Graham would close the revolving door between Congress and lobbyists"), "slam the revolving door between Capitol Hill and K Street"),
     ("soc-05", 2, GRAHAM("Graham would legalize marijuana federally"), "David will vote to legalize marijuana federally"),
     ("soc-04", 2, GRAHAM("Graham would vote for laws that defend the unborn"), "David is pro-life with no hedging."),
     ("soc-03", -2, GRAHAM("Graham is pro-life"), None),
     ("ene-06", -1, GRAHAM("Graham would scrap green mandates and leave energy to the market"), "David will vote to scrap the green mandates"),
     ("def-08", -2, GRAHAM("Graham would bring the troops home"), "Bring the troops home and stop mailing blank checks to foreign governments."),
     ("def-10", 2, GRAHAM("Graham would stop sending money to foreign governments"), None),
     ("def-04", 2, GRAHAM("Graham says Congress must vote before any war"), "If America goes to war, Congress votes on it first, out loud and on the record."))
CAMPBELL = site("Christopher Campbell", "https://campbellforsenate.org/")
cand("KY-SEN", "KY-SEN:campbell", "Christopher Campbell", "I",
     "Kentuckian from Marion County: union member (Local 1076), Kentucky National Guard veteran and Eastern Kentucky University graduate who has worked in health care.",
     ("hea-01", 2, CAMPBELL("Campbell supports Medicare for All"), "Healthcare is a basic human right"),
     ("hea-03", 2, CAMPBELL("Campbell supports a Medicare for All plan"), None),
     ("eco-09", 2, CAMPBELL("Campbell says workers need safe workplaces and a way to raise grievances"), "those workers must have a means to address grievances without fear of retaliation or retribution"),
     ("ene-04", 2, CAMPBELL("Campbell would push a constitutional green amendment guaranteeing a healthy environment"), "I will push for a Constitutional “Green” Amendment"),
     ("ene-06", 1, CAMPBELL("Campbell would bar companies from buying carbon credits to keep polluting"), None),
     ("soc-03", 2, CAMPBELL("Campbell calls reproductive care health care"), "Reproductive Care is Health Care and no American citizen should be deprived of it."),
     ("soc-04", -2, CAMPBELL("Campbell calls reproductive care a constitutionally protected right"), None),
     ("gov-01", 2, CAMPBELL("Campbell would amend the Constitution to set congressional term limits"), "I will push for a Constitutional Amendment to impose term limits on the other two Branches of Government"),
     ("def-01", -2, CAMPBELL("Campbell would cut defense spending toward 1% of GDP"), "My goal would be to get Defense Spending as close to 1% of GDP as possible"),
     ("def-05", -2, CAMPBELL("Campbell wants a moratorium on all military aid to foreign governments"), None),
     ("def-12", -2, CAMPBELL("Campbell wants a moratorium on all military aid to foreign governments"), None),
     ("def-13", -2, CAMPBELL("Campbell wants a moratorium on all military aid to foreign governments"), None),
     ("def-08", -1, CAMPBELL("Campbell would consolidate overseas U.S. military bases"), None),
     ("gov-08", 2, CAMPBELL("Campbell would abolish the Electoral College"), None),
     ("gov-07", 2, CAMPBELL("Campbell would add ranked-choice voting by constitutional amendment"), None),
     ("gov-04", 1, CAMPBELL("Campbell wants stronger guardrails against gerrymandering"), None),
     ("gov-13", -2, CAMPBELL("Campbell would overturn Citizens United by constitutional amendment"), None),
     ("gov-11", 2, CAMPBELL("Campbell would overturn Citizens United by constitutional amendment"), None))

# Massachusetts Senate -------------------------------------------------------------
TACHE = site("Joe Tache", "https://www.tache4ma.com/our-program")
cand("MA-SEN", "MA-SEN:tache", "Joe Tache", "Socialism and Liberation",
     "Boston youth worker and community organizer from Roxbury; a member of the Party for Socialism and Liberation since 2018.",
     ("eco-01", 2, TACHE("Tache proposes a 100% tax on assets above $10 million to fund public needs"), "along with a 100% tax on all assets above 10 million dollars"),
     ("eco-12", 2, TACHE("Tache proposes a 100% tax on assets above $10 million"), None),
     ("hea-01", 2, TACHE("Tache would guarantee health care for all"), "fund quality housing, healthcare, nutritious food, education, childcare, and a dignified retirement for all"),
     ("soc-07", 2, TACHE("Tache would guarantee child care for all"), None),
     ("eco-09", 2, TACHE("Tache would guarantee union jobs"), "we will guarantee well-paid union jobs and job training"),
     ("ene-03", -2, TACHE("Tache would decommission fossil fuel infrastructure"), "seize and decommission the billionaires’ fossil fuel infrastructure"),
     ("ene-01", 2, TACHE("Tache would build a renewable energy grid"), "build a renewable energy grid in its place"),
     ("def-01", -2, TACHE("Tache would cut the military budget by 90%"), "cutting the military budget by 90%"),
     ("def-08", -2, TACHE("Tache would close all overseas military bases"), "closing all 800+ military bases around the world"),
     ("def-12", -2, TACHE("Tache would end all U.S. aid to Israel"), "end all U.S. aid to Israel immediately"),
     ("def-11", -2, TACHE("Tache calls the war in Gaza a genocide and would end aid to Israel"), None),
     ("def-07", 2, TACHE("Tache wants a foreign policy based on diplomacy"), "a new era of foreign policy based on solidarity and diplomacy, not domination"),
     ("def-03", 1, TACHE("Tache would guarantee veterans job training and union jobs"), None),
     ("imm-08", -2, TACHE("Tache would abolish ICE"), "Abolishing ICE and providing a path to citizenship for every person living inside the United States"),
     ("imm-02", 2, TACHE("Tache would provide a path to citizenship for everyone living in the U.S."), None),
     ("soc-03", 2, TACHE("Tache would provide free reproductive health services including abortion"), "Providing free reproductive health services including abortion"),
     ("soc-04", -2, TACHE("Tache would provide free abortion services"), None),
     ("soc-12", 2, TACHE("Tache would ensure the right to gender-affirming health care"), "Ensuring the right to gender-affirming healthcare"),
     ("soc-02", 1, TACHE("Tache would reinstate and expand affirmative action"), None))
AYYADURAI = site("Shiva Ayyadurai", "https://shiva4senate.com/platform/")
cand("MA-SEN", "MA-SEN:ayyadurai", "Shiva Ayyadurai", "I",
     "Scientist and entrepreneur behind EchoMail and CytoSolve, running as an independent.",
     ("soc-01", 2, AYYADURAI("Ayyadurai would end censorship"), "End censorship, protect medical freedom, and return science to the people"),
     ("gov-11", 1, AYYADURAI("Ayyadurai would remove lobbyists and billionaires from government"), "Rip lobbyists and billionaires out of government"),
     ("eco-02", 2, AYYADURAI("Ayyadurai would cut taxes for families"), "Cut taxes for families and small business"),
     ("eco-08", 1, AYYADURAI("Ayyadurai would cut taxes for small businesses"), None),
     ("gov-05", 2, AYYADURAI("Ayyadurai wants voter ID and hand-counted paper ballots"), "Paper ballots, hand-counting, same-day voting, Voter ID."),
     ("def-08", -2, AYYADURAI("Ayyadurai would bring troops home"), "No more trillion-dollar wars abroad. Bring troops home"),
     ("def-12", -2, AYYADURAI("Ayyadurai would stop taxpayer subsidies to Israel"), "Stop taxpayer subsidies to Israel and others."),
     ("def-10", 2, AYYADURAI("Ayyadurai would stop subsidies to Israel and other countries"), None),
     ("gov-01", 2, AYYADURAI("Ayyadurai supports term limits"), "Term limits, ban insider trading"),
     ("gov-02", 1, AYYADURAI("Ayyadurai would ban insider trading by representatives"), None),
     ("edu-03", 1, AYYADURAI("Ayyadurai wants schools to teach trades"), None),
     ("soc-08", 1, AYYADURAI("Ayyadurai proposes a Digital Bill of Rights for privacy"), None),
     ("ene-04", 1, AYYADURAI("Ayyadurai would ban poisons in food and agriculture"), "Ban poisons in food and agriculture, enforce honest labeling."))

# Massachusetts, Maryland and Michigan governors -----------------------------------
JAMES = site("Andrea James", "https://www.ajforma.com/platform")
JAMES_BIO = site("Andrea James", "https://www.ajforma.com/meet-andrea")
cand("MA-GOV", "MA-GOV:james", "Andrea James", "I",
     "Independent whose family has lived in Massachusetts for seven generations; she refuses corporate campaign contributions.",
     ("soc-07", 2, JAMES("James supports universal child care"), None),
     ("hea-01", 2, JAMES("James supports Medicare for All in Massachusetts"), "Medicare for All in Massachusetts"),
     ("hea-03", 2, JAMES("James supports Medicare for All in Massachusetts"), None),
     ("hou-01", 1, JAMES("James supports affordable housing and rent stabilization"), "Affordable Housing & Rent Stabilization"),
     ("hou-06", 1, JAMES("James supports rent stabilization"), None),
     ("sta-03", 2, JAMES("James supports a $25 living wage"), "$25 Living Wage"),
     ("edu-02", 2, JAMES("James would make UMass free"), "Make UMass Free For All"),
     ("ene-01", 2, JAMES("James wants a rapid transition to 100% clean energy"), "Rapid, Just Transition to 100% Clean Energy"),
     ("imm-08", -1, JAMES("James would end state cooperation with ICE"), "End State Cooperation with ICE & Protect Immigrant Families"),
     ("eco-09", 2, JAMES("James supports public-sector union rights"), "Stand Up for Educators and Public Sector Worker Union Rights"),
     ("soc-12", 1, JAMES("James would protect the LGBTQ+ community"), "Protect Our LGBTQ+ Community"),
     ("cri-07", 1, JAMES("James would invest in communities rather than incarceration"), "Invest in Communities, Not Mass Incarceration"),
     ("gov-11", 1, JAMES_BIO("James refuses corporate campaign contributions"), "She refuses campaign contributions from corporations"))
ELLIS = site("Andy Ellis", "https://www.gogreen2026.com/platform")
cand("MD-GOV", "MD-GOV:ellis", "Andy Ellis", "G", None,
     ("sta-02", 2, ELLIS("Ellis would fully fund public education"), "Build out and fully fund our public education system so it truly works for all."),
     ("edu-01", 2, ELLIS("Ellis would fully fund public education"), None))
HUDSON = site("Anthony Hudson", "https://electanthonyhudson.com/")
HUDSON_POL = site("Anthony Hudson", "https://electanthonyhudson.com/policies/")
cand("MI-GOV", "MI-GOV:hudson", "Anthony Hudson", "L",
     "Truck driver for 20 years; born and raised in Texas, he moved to Michigan in 2012.",
     ("sta-04", 2, HUDSON("Hudson would eliminate property taxes"), "eliminate property and state income taxes"),
     ("eco-02", 2, HUDSON("Hudson would eliminate the state income tax"), None),
     ("ene-01", -2, HUDSON("Hudson would eliminate solar and wind farms"), "stop the data center and solar panel invasion of our state"),
     ("ene-03", 1, HUDSON_POL("Hudson would bring back natural gas"), None),
     ("ene-10", 2, HUDSON_POL("Hudson would eliminate renewable energy mandates to lower energy costs"), "Eliminate Renewable Energy Mandates"),
     ("gov-12", 1, HUDSON("Hudson demands transparency and accountability"), None))

# Minnesota Senate -----------------------------------------------------------------
WHITING = site("Rebecca Whiting", "https://whiting4senate.us/")
cand("MN-SEN", "MN-SEN:whiting", "Rebecca Whiting", "L",
     "Homeschooling mother and small-business owner who farms near Bemidji.",
     ("def-08", -2, WHITING("Whiting would bring the troops home"), "Bring the troops home."),
     ("def-02", -2, WHITING("Whiting opposes entangling alliances"), "No more entangling alliances."),
     ("def-07", 2, WHITING("Whiting would adopt a policy of non-intervention"), "Adopt a policy of non-intervention."),
     ("def-04", 1, WHITING("Whiting objects to sending troops abroad without a declaration of war"), None),
     ("def-10", 2, WHITING("Whiting says allies should run their countries without U.S. dollars"), "Our friends need to learn to run their own countries without the use of US dollars."),
     ("def-05", -1, WHITING("Whiting would use the military abroad only if the U.S. is attacked"), None),
     ("eco-07", 2, WHITING("Whiting campaigns to defund the government and end overspending"), None),
     ("eco-01", -2, WHITING("Whiting calls taxation theft"), "Taxation is theft."),
     ("eco-12", -2, WHITING("Whiting calls taxation theft"), None))

# Mississippi Senate ---------------------------------------------------------------
PINKINS_EDU = site("Ty Pinkins", "https://www.typinkins.com/issues-1/education")
PINKINS_HEA = site("Ty Pinkins", "https://www.typinkins.com/issues-1/healthcare")
PINKINS_HOU = site("Ty Pinkins", "https://www.typinkins.com/issues-1/housing")
cand("MS-SEN", "MS-SEN:pinkins", "Ty Pinkins", "I",
     "Army veteran and lawyer from Rolling Fork in the Mississippi Delta (Tougaloo College, Georgetown Law), running as an independent.",
     ("edu-01", 2, PINKINS_EDU("Pinkins would fully and fairly fund public schools"), "fully and fairly funding our schools"),
     ("edu-03", 2, PINKINS_EDU("Pinkins would increase access to career and technical education"), "Increase access to career and technical education (CTE) and vocational programs"),
     ("edu-04", 2, PINKINS_EDU("Pinkins would raise teacher salaries"), "Address the teacher shortage by raising salaries"),
     ("hea-06", 1, PINKINS_EDU("Pinkins would strengthen mental health services in schools"), "Strengthen mental health and counseling services in public schools"),
     ("soc-07", 1, PINKINS_EDU("Pinkins would invest in affordable pre-K and early childhood education"), None),
     ("hea-01", 2, PINKINS_HEA("Pinkins supports the Medicare for All Act"), "I support the Medicare for All Act"),
     ("hea-03", 2, PINKINS_HEA("Pinkins supports the Medicare for All Act"), None),
     ("hou-01", 2, PINKINS_HOU("Pinkins would push for more federal funding for affordable housing"), "push for increased federal funding for affordable housing"),
     ("eco-02", 2, PINKINS_HOU("Pinkins would cut taxes for middle-class families"), "cut taxes for middle-class families"))

# North Carolina Senate ------------------------------------------------------------
DUBLIN = site("Michael Dublin", "https://www.dublinforcongress.com/platform")
DUBLIN_PILLARS = site("Michael Dublin", "https://www.dublinforcongress.com/issues")
cand("NC-SEN", "NC-SEN:dublin", "Michael Dublin", "G",
     "Retired public school teacher and veteran who has led a prison ministry for more than two decades; takes no corporate donations.",
     ("ene-03", -2, DUBLIN("Dublin would ban new oil and gas drilling"), "I support banning new oil and gas drilling"),
     ("ene-01", 2, DUBLIN("Dublin wants a planned transition to 100% renewable energy"), "a democratically planned transition to 100% renewable energy"),
     ("ene-08", 2, DUBLIN("Dublin would fully fund emergency systems for climate disasters"), "I stand for fully funding emergency systems to protect and evacuate people from climate-driven disasters."),
     ("cri-09", -2, DUBLIN("Dublin would abolish the death penalty"), "I stand for abolishing the death penalty"),
     ("cri-05", 2, DUBLIN("Dublin would invest in rehabilitation and jobs rather than prisons"), "I support investing in rehabilitation and living-wage jobs rather than prisons."),
     ("cri-07", 2, DUBLIN_PILLARS("Dublin would invest in community-based alternatives to policing"), "investing in community-based alternatives to policing"),
     ("cri-03", 1, DUBLIN("Dublin would put police under elected civilian boards"), None),
     ("soc-03", 2, DUBLIN("Dublin supports free, legal and accessible abortion"), "free, safe, legal, and accessible abortion"),
     ("soc-04", -2, DUBLIN("Dublin supports free, legal and accessible abortion"), None),
     ("eco-11", 2, DUBLIN("Dublin supports 12 months of paid parental leave"), "I support 12 months of paid parental leave"),
     ("hea-01", 2, DUBLIN("Dublin supports free health care for all"), "free, high-quality healthcare for all, including gender-affirming treatment and mental health services"),
     ("hea-06", 2, DUBLIN("Dublin supports free mental health services"), None),
     ("hea-03", 2, DUBLIN("Dublin would increase Social Security, Medicare and Medicaid benefits"), None),
     ("soc-12", 2, DUBLIN("Dublin supports free gender-affirming treatment"), None),
     ("def-01", -2, DUBLIN("Dublin would drastically cut the military budget"), "drastically cutting the US military budget"),
     ("def-02", -2, DUBLIN("Dublin would abolish NATO"), "I support abolishing NATO and all imperialist alliances."),
     ("def-07", 2, DUBLIN_PILLARS("Dublin favors diplomacy over war"), "Diplomacy over endless war."),
     ("imm-08", -2, DUBLIN("Dublin would abolish ICE"), "I support abolishing ICE"),
     ("imm-02", 2, DUBLIN("Dublin supports legalization for all undocumented immigrants"), "immediate, unconditional legalization and equal rights for all undocumented immigrants"),
     ("eco-01", 2, DUBLIN("Dublin would tax the rich"), "I support taxing the rich their fair share"),
     ("hou-01", 2, DUBLIN("Dublin wants a massive expansion of public, affordable housing"), "a massive expansion of publicly owned, permanently affordable housing"),
     ("hou-06", 1, DUBLIN("Dublin supports universal rent control"), None),
     ("eco-03", 2, DUBLIN("Dublin would raise the federal minimum wage to $25"), "raising the federal minimum wage to $25 an hour"),
     ("eco-13", 2, DUBLIN("Dublin supports a 32-hour work week"), "I stand for a 32-hour work week with no loss in pay or benefits."),
     ("gov-11", 2, DUBLIN_PILLARS("Dublin would overturn Citizens United"), "We will fight to get big money out of politics by overturning Citizens United"),
     ("gov-13", -2, DUBLIN_PILLARS("Dublin would overturn Citizens United"), None),
     ("gov-04", 1, DUBLIN_PILLARS("Dublin would end gerrymandering"), None))
BRAY = site("Shannon Bray", "https://www.shannonbray.us/issues")
BRAY_HOME = site("Shannon Bray", "https://www.shannonbray.us/")
cand("NC-SEN", "NC-SEN:bray", "Shannon Bray", "L",
     "Navy veteran and cybersecurity professional; the Libertarian nominee.",
     ("soc-08", 2, BRAY("Bray says people should own their data, with enforceable consent"), "You should own your data."),
     ("eco-07", 1, BRAY("Bray would end wasteful spending"), "Lower costs, simpler taxes, and an end to wasteful spending."),
     ("imm-01", 1, BRAY("Bray supports secure borders and a workable legal process"), "Secure borders and a fair, workable legal process."),
     ("ene-10", 1, BRAY("Bray wants reliable, affordable power with innovation over mandates"), None),
     ("edu-07", 1, BRAY("Bray supports local control of education"), None),
     ("edu-03", 1, BRAY("Bray supports skills training"), None),
     ("soc-01", 1, BRAY("Bray would defend free speech"), None),
     ("gov-12", 1, BRAY_HOME("Bray wants transparency, oversight and responsible spending"), None))

# Nebraska and New Hampshire Senate ------------------------------------------------
cand("NE-SEN", "NE-SEN:marvin", "Mike Marvin", "Legal Marijuana Now",
     "Retired executive director of NAPE/AFSCME Local 61, the state employees’ union. He remains on the ballot but has urged his supporters to back Dan Osborn.")
CONBOY = site("Chuck Conboy", "https://conboyforsenate.com/platform")
cand("NE-SEN", "NE-SEN:conboy", "Chuck Conboy", "America First",
     "Lifelong Nebraskan who worked in management and sales and as vice president of a local meatpackers and butchers union.",
     ("imm-01", 2, CONBOY("Conboy would seal the southern border"), "Secure the southern border"),
     ("imm-08", 2, CONBOY("Conboy would expand immigration enforcement"), "Expand immigration enforcement to identify and process illegal aliens"),
     ("imm-07", 2, CONBOY("Conboy would deport criminals and dangerous individuals"), "Deport criminals, dangerous individuals, and those who have no claim to remain"),
     ("def-10", 2, CONBOY("Conboy would end blank checks to foreign governments"), "No more blank checks to foreign governments at the expense of Americans"),
     ("def-07", 1, CONBOY("Conboy opposes endless foreign wars"), None),
     ("edu-05", 1, CONBOY("Conboy would end the student debt holding young Americans back"), "End the crushing student debt holding young Americans back"),
     ("edu-03", 2, CONBOY("Conboy would bring back trade schools"), "Bring back trade schools and train the next generation of American craftsmen and skilled workers"),
     ("soc-07", 2, CONBOY("Conboy would make child care affordable"), "Make childcare affordable for American families"))
LAPLANTE = site("Edmond LaPlante", "https://laplante4constitutionalnh.com/my-platform")
cand("NH-SEN", "NH-SEN:laplante", "Edmond LaPlante", "Constitution",
     "Marine veteran, mechanic for more than 40 years and school board member; a former Senate and governor candidate.",
     ("def-10", 2, LAPLANTE("LaPlante would stop sending foreign aid overseas"), "stop sending foreign aid overseas"),
     ("def-08", -1, LAPLANTE("LaPlante would end U.S. involvement in wars abroad"), "end U.S. involvement in wars abroad"),
     ("def-03", 1, LAPLANTE("LaPlante says no veteran should face delayed or denied care"), None),
     ("imm-08", 1, LAPLANTE("LaPlante would start with enforcing existing immigration laws"), "immigration policy must begin with enforcement of the laws already on the books"),
     ("edu-06", 1, LAPLANTE("LaPlante would expand homeschooling freedom"), "I propose expanding homeschooling freedom"))

# New Jersey and Ohio Senate -------------------------------------------------------
FERNANDEZ = site("Veronica Fernandez", "https://veronicaforsenate.com/policies")
cand("NJ-SEN", "NJ-SEN:fernandez", "Veronica Fernandez", "I",
     "Lifelong New Jerseyan from Long Valley who co-owns a small electrical contracting business; formerly a licensed insurance underwriter.",
     ("gov-11", 2, FERNANDEZ("Fernandez would sign on to a 28th Amendment overturning Citizens United"), "Overturning Citizens United IS the game changer for this country"),
     ("gov-13", -2, FERNANDEZ("Fernandez would overturn Citizens United"), None),
     ("hea-01", 2, FERNANDEZ("Fernandez supports Medicare for All"), "I am a FIERCE supporter of M4A"),
     ("hea-03", 2, FERNANDEZ("Fernandez would sign on to Sen. Sanders’s Medicare for All bill"), None),
     ("hea-04", -2, FERNANDEZ("Fernandez says insurance will never work for health care"), None),
     ("imm-08", -2, FERNANDEZ("Fernandez would abolish ICE"), "ABOLISH immediately and replace with a vigorous and fast-tracked path to citizenship."),
     ("imm-02", 2, FERNANDEZ("Fernandez wants a fast-tracked path to citizenship"), None),
     ("def-12", -2, FERNANDEZ("Fernandez would not vote to keep arming Netanyahu’s government"), "I will NOT vote in any way to continue arming Netanyahu"),
     ("def-11", -2, FERNANDEZ("Fernandez says Netanyahu should be tried for war crimes"), None),
     ("gov-04", 2, FERNANDEZ("Fernandez supports independent redistricting commissions"), "support INDEPENDENT commissions to determine our state and congressional district lines"))
LEVY = site("Greg Levy", "https://www.greg4senate.com/platform")
cand("OH-SEN", "OH-SEN:levy", "Greg Levy", "I",
     "Akron-raised community organizer, singer and veteran who founded the Paul Robeson Revolutionary Choir; running as a socialist.",
     ("hea-01", 2, LEVY("Levy would establish single-payer health care"), "establishing a universal, single-payer healthcare system, free at the point of use"),
     ("hea-03", 2, LEVY("Levy would establish single-payer health care"), None),
     ("edu-05", 2, LEVY("Levy would cancel all student debt"), "canceling all student debt"),
     ("edu-02", 2, LEVY("Levy would make public education through college free"), "making public education, from pre-K through college and trade school, completely free"),
     ("hou-06", 2, LEVY("Levy would cap rents nationally and ban evictions"), None),
     ("eco-01", 2, LEVY("Levy would repeal the 2025 tax cuts for the rich"), "We will repeal Trump’s so-called “Big Beautiful” tax cuts for the rich."),
     ("eco-09", 1, LEVY("Levy pushes for 20 million union jobs"), None),
     ("eco-13", 1, LEVY("Levy would use technology to shorten the workweek"), "shorten the workweek"),
     ("ene-01", 1, LEVY("Levy would put union labor to work building renewable energy systems"), None),
     ("gov-11", 2, LEVY("Levy would outlaw corporate lobbying and political donations"), "We will outlaw corporate lobbying and political donations"),
     ("gov-13", -2, LEVY("Levy would outlaw corporate political donations"), None),
     ("cri-03", 1, LEVY("Levy would put police under community control and prosecute police violence"), None))

write("data/research/candidates.json",
      [{"id": rid, "partial": True, "candidates": cands} for rid, cands in RACES.items()],
      "Bios and positions for candidates who had none, from their campaign sites, researched Oct. 26, 2026.", updated=READ)
