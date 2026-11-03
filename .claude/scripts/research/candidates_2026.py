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

from common import P, article, page, write

READ = "2026-10-26"
READ27 = "2026-10-27"  # sites found and read a day later


def site(name, url, read=READ):
    return lambda note: page(f"{name} campaign site: {note}", url, read)


RACES = {}
RACE_FIELDS = {}  # race-level fields, such as candidatesOnly where Wikipedia's list is wrong


def cand(race, cid, name, party, bio, *rows, **fields):
    """fields: other candidate fields, such as officialSite=None to drop a dead
    campaign link that the automatic refresh picked up."""
    out = {"id": cid, "name": name, "party": party, **fields}
    if bio:
        out["bio"] = bio
    if rows:
        out["positions"] = P(*rows)
    RACES.setdefault(race, []).append(out)


def more(race, cid, *rows, bio=None, **fields):
    """Add positions (and a bio, if the entry has none) to a candidate entered earlier
    in this file, so one candidate never gets two entries."""
    entry = next(c for c in RACES[race] if c["id"] == cid)
    if rows:
        added = P(*rows)
        assert not set(added) & set(entry.get("positions", {})), cid
        entry.setdefault("positions", {}).update(added)
    if bio and not entry.get("bio"):
        entry["bio"] = bio
    entry.update(fields)


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
BURKETT = site("Charles Burkett", "https://burkettforgov.com/")
cand("FL-GOV", "FL-GOV:burkett", "Charles Burkett", "I",
     "Real estate investor and longtime mayor of Surfside, including after the 2021 condo collapse; running with no party and taking no contributions.",
     ("sta-04", 2, BURKETT("Burkett would phase out property taxes for long-term residents"), "Slash and eventually eliminate property taxes for vested Florida homeowners and renters."),
     ("hou-04", -1, BURKETT("Burkett would stop the construction boom and favor renovation"), "Stop the current radical new construction boom which is turning our roads into parking lots."),
     ("sta-08", 1, BURKETT("Burkett would give first responders every tool they need"), "Give our first responders every tool they need to be the best in the business."))
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
MM_GOV = lambda note: page(f"Maryland Matters voter guide, candidates’ answers: {note}", "https://marylandmatters.org/voter-guides/contests/governor-lieutenant-governor-general/", READ)
cand("MD-GOV", "MD-GOV:ellis", "Andy Ellis", "G",
     "Debate coach and founder of Debate Strategies LLC, active in the Green Party for a decade.",
     ("sta-02", 2, ELLIS("Ellis would fully fund public education"), "Build out and fully fund our public education system so it truly works for all."),
     ("edu-01", 2, ELLIS("Ellis would fully fund public education"), None),
     ("eco-01", 2, MM_GOV("Ellis would tax the rich and end corporate tax breaks"), "We need to tax the rich and end corporate tax breaks!"),
     ("sta-10", -1, MM_GOV("Ellis would end corporate tax breaks"), None),
     ("eco-02", 1, MM_GOV("Ellis would use the money for bigger tax credits for working-class Marylanders"), None),
     ("gov-07", 2, MM_GOV("Ellis supports ranked-choice voting and proportional representation"), "public financing for all races, and ranked choice voting and proportional representation"),
     ("gov-11", 1, MM_GOV("Ellis supports public financing for all races"), None),
     ("hea-01", 1, MM_GOV("Ellis would explore single-payer health care at the state level"), "We should explore a single-payer model at the state level."),
     ("imm-08", -2, MM_GOV("Ellis says no Maryland government or police agency should work with ICE"), "In Maryland, no government or law enforcement entities should collaborate with ICE"))
cand("MD-GOV", "MD-GOV:white", "Cathy White", "Working Class",
     "Factory worker for 40 years and caregiver for her mother and sister; the Working Class Party nominee.",
     ("hea-01", 1, MM_GOV("White says health care should be a human right"), "Health care should be a human right and not based on how much money you have."),
     ("sta-03", 1, MM_GOV("White says everyone able to work needs a job with a living wage"), "Every person able to work needs a job with a living wage."),
     ("sta-01", 1, MM_GOV("White would put the unemployed to work fixing roads and bridges"), "people who are now unemployed could be put to work fixing the crumbling roads and bridges that need to be repaired or replaced"),
     ("eco-09", 1, MM_GOV("White says workers must organize to win higher wages"), None),
     ("imm-08", -1, MM_GOV("White opposes ICE’s actions"), "I am opposed to the actions of ICE."))
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
     "Retired executive director of NAPE/AFSCME Local 61, the state employees’ union. He withdrew on Aug. 21 (VOTE411) and has urged his supporters to back Dan Osborn, but his name remains on the ballot.")
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
REDPATH = site("Bill Redpath", "https://billredpath.com/faq/")
cand("OH-SEN", "OH-SEN:redpath", "William Redpath", "L",
     "Findlay native, CPA and retired business-valuation analyst; chaired the Libertarian National Committee from 2006 to 2010.",
     ("eco-10", -2, REDPATH("Redpath would end all tariffs"), "The United States should end all tariffs on imported goods and services, regardless of the policies of other nations."),
     ("agr-07", -2, REDPATH("Redpath supports unilateral free trade"), None),
     ("agr-06", 1, REDPATH("Redpath supports unilateral free trade"), None),
     ("eco-07", 2, REDPATH("Redpath calls the debt a spending problem and would eliminate the Education and HUD departments"), "it is a too much spending, not too little taxing, problem."),
     ("agr-01", -2, REDPATH("Redpath would end farm subsidies"), "an end to all corporate welfare and farm subsidies"),
     ("edu-01", -1, REDPATH("Redpath would eliminate the Department of Education"), None),
     ("hou-01", -1, REDPATH("Redpath would eliminate the Department of Housing and Urban Development"), None),
     ("soc-05", 1, REDPATH("Redpath would end federal drug prohibition and leave it to the states"), "the Federal government should end its drug prohibition and allow the states to address this issue"),
     ("def-15", -2, REDPATH("Redpath calls U.S. participation in the war on Iran unconstitutional"), "the United States participation in the war against Iran is clearly unconstitutional"),
     ("def-04", 2, REDPATH("Redpath says the Iran war needed Congress’s approval"), None),
     ("def-12", -1, REDPATH("Redpath would end the special relationship with Israel"), "We should treat Israel like any other allied nation."),
     ("imm-03", 2, REDPATH("Redpath supports open immigration with exceptions for criminals and threats"), "Open immigration would be the greatest anti-poverty program the world has ever known."),
     ("eco-12", -2, REDPATH("Redpath would replace the tax code with a 20% flat tax"), "A Flat Tax of 20 percent on individual income"),
     ("eco-01", -1, REDPATH("Redpath would replace the tax code with a 20% flat tax"), None),
     ("hea-03", -2, REDPATH("Redpath would phase out federal Medicaid funding"), "phasing out Federal subsidies over a ten year period"),
     ("gov-07", 2, REDPATH("Redpath supports ranked-choice voting"), "I support the use of Ranked Choice Voting for single winner elections"))
KISSICK = site("Don Kissick", "https://donkissick.com/on-the-issues")
cand("OH-GOV", "OH-GOV:kissick", "Donald Kissick", "L",
     "Navy veteran (six years, including Desert Storm) from Ottawa in northwestern Ohio; running with James Mills.",
     ("sta-04", 2, KISSICK("Kissick supports the amendment to end property taxes"), "We are in favor of the end property tax amendment."),
     ("sta-10", -1, KISSICK("Kissick would end corporate welfare for large institutions"), "eliminate corporate welfare for the larger institutions"),
     ("gov-11", 2, KISSICK("Kissick wants no more corporate money in politics"), "We want to see no more corporate bribery."),
     ("gov-13", -1, KISSICK("Kissick opposes contributions from regulated monopolies"), None),
     ("sta-06", 2, KISSICK("Kissick would bar legislators from lobbying for five years"), "We want to ban legislators from becoming lobbyists for 5 years after they’re in office."),
     ("gov-12", 2, KISSICK("Kissick wants contracts and budgets in a searchable public database"), "We want total transparency in government contracts and budgets"),
     ("soc-10", 1, KISSICK("Kissick backs the petition to protect same-sex marriage in Ohio’s constitution"), None),
     ("soc-05", 1, KISSICK("Kissick would get government bureaucracy out of the marijuana industry"), None),
     ("imm-02", 2, KISSICK("Kissick supports a clear lawful path to citizenship"), "Immigrants should have a straightforward and clear lawful path to citizenship"),
     ("imm-08", -1, KISSICK("Kissick wants civil, not militarized, immigration enforcement"), "immigration enforcement should be civil not militarized"))

# Oklahoma and Oregon -------------------------------------------------------------
MEINHARDT = site("Ron Meinhardt", "https://www.running4ok.com/")
cand("OK-SEN", "OK-SEN:meinhardt", "Ron Meinhardt", "I",
     "Registered nurse and Oklahoma Republican running as an independent conservative.",
     ("def-04", 2, MEINHARDT("Meinhardt says Congress must authorize war"), "Congress must authorize war."),
     ("def-07", 1, MEINHARDT("Meinhardt opposes forever wars"), None),
     ("imm-01", 1, MEINHARDT("Meinhardt would secure the border and streamline deportation"), "That means securing the border, streamlining deportation, and ensuring a process that is constitutional, enforceable, and accountable."),
     ("imm-08", 1, MEINHARDT("Meinhardt supports enforcing immigration laws"), None),
     ("imm-02", -1, MEINHARDT("Meinhardt criticizes politicians who drift toward amnesty"), None),
     ("ene-10", 1, MEINHARDT("Meinhardt calls affordable domestic energy a family issue"), None),
     ("gov-03", 1, MEINHARDT("Meinhardt says voters deserve to know who funds political influence"), "Voters deserve to know who is funding political influence and what those interests expect in return."),
     ("eco-07", 1, MEINHARDT("Meinhardt wants a solvent future, not endless debt"), None))
STINNETT = site("Curtis Stinnett", "https://www.stinnettforsenate.org/main-ideas")
STINNETT_HOME = site("Curtis Stinnett", "https://www.stinnettforsenate.org/")
cand("OK-SEN", "OK-SEN:stinnett", "Curtis Stinnett", "I",
     "Pharmacist from Lindsay, now in Tulsa; takes no campaign contributions.",
     ("hea-01", 2, STINNETT("Stinnett supports Medicare for All"), "Healthcare is a Human Right"),
     ("hea-03", 2, STINNETT("Stinnett supports Medicare for All"), None),
     ("soc-03", 2, STINNETT("Stinnett would codify Roe"), "Codify Roe"),
     ("soc-04", -2, STINNETT("Stinnett would codify Roe"), None),
     ("gov-11", 2, STINNETT_HOME("Stinnett calls money in politics the main obstacle to better government"), "money in politics is the primary obstacle to better government"),
     ("gov-13", -2, STINNETT("Stinnett would overturn Citizens United"), None),
     ("eco-03", 1, STINNETT("Stinnett supports a living wage"), None))
SMITH = site("Brett Smith", "https://brett-smith.us/")
cand("OR-GOV", "OR-GOV:smith", "Brett Smith", "Pacific Green", None,
     ("sta-06", 2, SMITH("Smith calls corruption the most important issue"), "Corruption is the single most important issue facing us today."),
     ("hea-01", 2, SMITH("Smith would open the Oregon Health Plan to every resident"), "This plan expands the Oregon Health Plan into a universal public option available to every Oregon resident"),
     ("hea-03", 2, SMITH("Smith would open the Oregon Health Plan to every resident"), None))

# Rhode Island and West Virginia Senate --------------------------------------------
BAHRY = site("Michael Bahry", "https://bahryforsenate.com/")
cand("RI-SEN", "RI-SEN:bahry", "Michael Bahry", "I",
     "Retired construction executive who founded the Providence nonprofit Fifty-Three: Five; teaches theology at Salve Regina University.",
     ("gov-01", 2, BAHRY("Bahry supports term limits for Congress"), "term limits break the cycle of financial dominance, name recognition, and office perks"),
     ("def-02", -2, BAHRY("Bahry would withdraw from NATO"), "As for the United States, I believe it's time to withdraw from NATO."),
     ("def-07", 2, BAHRY("Bahry would focus on diplomacy over war"), "We must focus on diplomacy-not war."),
     ("def-01", -1, BAHRY("Bahry says military spending is not a jobs program"), "War and military spending are not sustainable job programs."),
     ("def-13", -1, BAHRY("Bahry wants peace in Ukraine rather than more weapons"), "peace over more bombs"),
     ("def-05", -1, BAHRY("Bahry wants peace in Ukraine rather than more weapons"), None),
     ("def-12", -1, BAHRY("Bahry calls for peace in Gaza, not more bombs"), "A call for peace, not more bombs"),
     ("soc-04", 2, BAHRY("Bahry is pro-life"), "I am Catholic and I am pro-life."),
     ("soc-03", -2, BAHRY("Bahry is pro-life"), None),
     ("imm-02", 1, BAHRY("Bahry wants a compassionate solution rather than removing hardworking people"), "Rhode Islanders want a compassionate solution - not the removal of good hardworking people."),
     ("imm-08", -1, BAHRY("Bahry objects to spending billions on mass deportations"), None),
     ("imm-01", 1, BAHRY("Bahry would secure the border against trafficking"), "We must secure our border to stop human and drug trafficking."),
     ("soc-12", -1, BAHRY("Bahry says biological males should not compete in women’s sports"), "clearly, biological males should not compete in women's or girls' sports"),
     ("soc-11", -2, BAHRY("Bahry opposes medical transition for minors"), "We must protect our children from irreversible decisions they are too young to fully understand"),
     ("soc-06", 1, BAHRY("Bahry’s platform is rooted in religious liberty"), None))
WILSON = site("S. Marshall Wilson", "https://wilsonwv.com/")
cand("WV-SEN", "WV-SEN:wilson", "S. Marshall Wilson", "Constitution",
     "Army combat veteran (Iraq), former missionary in the Peruvian Amazon and former state delegate; the Constitution Party’s 2024 nominee for governor.",
     ("eco-07", 2, WILSON("Wilson would vote against every unbalanced budget"), "Marshall will vote against every budget that doesn't balance"))

# South Carolina ------------------------------------------------------------------
WHITENER = site("Kasie Whitener", "https://kasiesouthcarolina.com/")
cand("SC-SEN", "SC-SEN:whitener", "Kasie Whitener", "L",
     "University of South Carolina business professor, author and radio host from Blythewood; a former chair of the South Carolina Libertarian Party.",
     ("eco-07", 2, WHITENER("Whitener would cut federal spending 5% across all agencies and pass a balanced budget amendment"), "reduce federal spending by 5% across all agencies"),
     ("hea-04", 1, WHITENER("Whitener would separate health insurance from employment with more free-market options"), "Separate health insurance from employment, more free market options"),
     ("def-07", 1, WHITENER("Whitener says no more foreign wars"), "No more foreign wars"),
     ("soc-04", -1, WHITENER("Whitener wants no new federal laws on abortion"), "No new federal laws or taxpayer dollars spent on abortion"),
     ("eco-10", -1, WHITENER("Whitener would end protectionist policies"), "end protectionist policies and laws"),
     ("agr-07", -1, WHITENER("Whitener would end protectionist policies"), None))
HAKIM = site("Walid Hakim", "https://www.walidnhakim.com/Platform.html")
cand("SC-GOV", "SC-GOV:hakim", "Walid Hakim", "G",
     "Marine veteran and Columbia businessman; a former military policeman and executive director of the S.C. Libertarian Party, now the Green nominee.",
     ("sta-02", 2, HAKIM("Hakim would invest deeply in schools rather than cut funding"), "Instead of cutting funding, South Carolina must invest deeply in its schools and students."),
     ("edu-01", 2, HAKIM("Hakim would invest deeply in schools"), None),
     ("edu-09", 2, HAKIM("Hakim would provide breakfast and lunch to all students"), "Every school in South Carolina would provide healthy breakfast and lunch to all students"),
     ("soc-07", 2, HAKIM("Hakim would build child care into the school system"), "Childcare would be incorporated into the state school system"),
     ("edu-03", 2, HAKIM("Hakim would turn grades 11 and 12 into trade school or associate degree programs"), "Grades 11 and 12 would be transformed into trade school or associate degree programs"),
     ("eco-12", 2, HAKIM("Hakim supports a progressive state tax system"), "he would support a progressive tax system where those who earn more contribute more"),
     ("eco-01", 2, HAKIM("Hakim would have those who earn more contribute more"), None),
     ("hea-01", 2, HAKIM("Hakim would create a state-owned insurer covering every resident"), "a state-owned insurer, offering full coverage to every resident"),
     ("hea-03", 2, HAKIM("Hakim would create a state-owned insurer"), None),
     ("hou-02", 1, HAKIM("Hakim would limit ownership to twelve homes per corporation or individual"), "limit property ownership to twelve residential properties per corporation or individual"),
     ("sta-12", 2, HAKIM("Hakim would build high-speed rail between the state’s cities"), "contract the development of a high-speed rail systems connecting the state’s major cities"),
     ("ene-07", 2, HAKIM("Hakim wants free public transportation"), None))

# Tennessee Senate ----------------------------------------------------------------
GERENA = site("Andrew Gerena", "https://www.jeranimo4senate.org/issues")
cand("TN-SEN", "TN-SEN:gerena", "Andrew Gerena", "I",
     "Army veteran who has worked in security, trucking, IT and scientific research; known by his military callsign “Jeranimo.”",
     ("def-01", -1, GERENA("Gerena would redirect money from the war budget to education and infrastructure"), "Re-direct federal funding from the War Budget towards Education, Infrastructure, Research, and Job training programs"),
     ("def-12", -2, GERENA("Gerena would cut military aid to countries suspected of war crimes and separate U.S. forces from Israel’s government"), "Separate our military and intelligence agencies from all branches of the Israeli government"),
     ("def-11", -1, GERENA("Gerena would investigate AIPAC and separate U.S. agencies from Israel’s government"), None),
     ("eco-01", -1, GERENA("Gerena rejects any tax increase"), "Common sense budgeting, rejecting any Tax increase"),
     ("soc-08", 1, GERENA("Gerena wants data privacy rules for AI data centers"), "Serious environmental and data privacy regulations on AI Data centers"),
     ("ene-04", 1, GERENA("Gerena wants environmental rules for AI data centers"), None),
     ("edu-01", 1, GERENA("Gerena would redirect war spending to education"), None),
     ("edu-03", 1, GERENA("Gerena would redirect war spending to job training"), None))
MATTHEWS = site("Yoshi Matthews", "https://yoshimatthewssenate.com/issues/")
cand("TN-SEN", "TN-SEN:matthews", "Yoshi Matthews", "I",
     "Accountant and founder of FTP Nonprofit, which serves local communities and people with disabilities.",
     ("imm-01", 1, MATTHEWS("Matthews would secure the border and enforce immigration laws"), "Secure the border, enforce immigration laws, and support a functional legal immigration system."),
     ("imm-08", 1, MATTHEWS("Matthews would enforce immigration laws"), None))
SUTMAN = site("David Sutman Jr.", "https://sutmanjr4senate.com/")
cand("TN-SEN", "TN-SEN:sutman", "David Sutman Jr.", "I",
     "Working-class Tennessean with a business background, running as an independent.",
     ("gov-01", 1, SUTMAN("Sutman would push for term limits"), "Push for term limits"),
     ("gov-12", 1, SUTMAN("Sutman would increase transparency in spending"), "Increase transparency in spending"),
     ("eco-07", 1, SUTMAN("Sutman would cut wasteful spending"), None))
WHITSON = site("Catherine Whitson", "https://senatorbarcy.org/issues")
cand("TN-SEN", "TN-SEN:whitson", "Catherine Whitson", "I",
     "Pastor, life coach and mentor for 20 years after 30 years in the insurance industry.",
     ("ene-01", 1, WHITSON("Whitson would promote green energy"), "Promoting green energy and creativity"),
     ("edu-01", 2, WHITSON("Whitson would boost funding for public schools"), "Boosting funding for public schools and expanding vocational training programs"),
     ("edu-03", 2, WHITSON("Whitson would expand vocational training"), None),
     ("edu-06", 1, WHITSON("Whitson would also promote private and home schooling"), "promoting private and home schooling initiatives"),
     ("edu-05", 1, WHITSON("Whitson would find ways to pay off student debt"), "Finding ways to pay off student debt"),
     ("hou-01", 1, WHITSON("Whitson supports affordable housing for all Tennesseans"), "Affordable housing for all Tennesseans"),
     ("soc-07", 1, WHITSON("Whitson would promote better child care"), None),
     ("ene-07", 1, WHITSON("Whitson would promote mass transit"), "Promote mass transit options"),
     ("hou-03", 1, WHITSON("Whitson would promote mass transit"), None),
     ("hea-07", 1, WHITSON("Whitson would use the Affordable Care Act to help people without group coverage"), None))

# Tennessee governor ----------------------------------------------------------------
# Wikipedia lists independents Santiago Asconape and Taylor Hafley, who are not on the
# ballot, and leaves out Victor L. Scoggin and Dave Seeman, who are. The Hamilton County
# Election Commission's official sample ballot (the state's own list is a PDF/Excel
# download) gives the 15 names below, as do WSMV and the Tennessee Lookout.
RACE_FIELDS["TN-GOV"] = {
    "candidatesOnly": True,
    "notes": [{"text": "The ballot lists 15 candidates for governor: Republican Marsha Blackburn, Democrat Jerri Green and 13 independents.",
               "source": "Hamilton County Election Commission, official sample ballot, Nov. 3, 2026",
               "url": "https://elect.hamiltontn.gov/Portals/12/HTML/GenSample.html"}],
}
for _cid, _name in (("brewer", "Dean Brewer"), ("brown", "Ray Brown"), ("morgan", "Charles Van Morgan"),
                    ("murphy", "Eddie Lee Murphy"), ("scoggin", "Victor L. Scoggin"), ("seeman", "Dave Seeman"),
                    ("smithson", "Karl Knox Smithson"), ("taylor", "L. Webb Taylor")):
    cand("TN-GOV", f"TN-GOV:{_cid}", _name, "I", None)
HATLEY = site("David Hatley", "https://hatleyforgovernor.com/")
cand("TN-GOV", "TN-GOV:hatley", "David Hatley", "I",
     "East Tennessee manufacturer who built nine companies, including a hot tub maker; running with no party and no donors.",
     ("hou-01", 1, HATLEY("Hatley would give infrastructure grants for developments that set aside starter homes"), "The state helps pay for the water, sewer, and road work a city would otherwise push onto the developer."),
     ("hou-04", 1, HATLEY("Hatley would roll back building-code costs and speed approvals"), "Roll back the code changes that priced people out."),
     ("gov-12", 2, HATLEY("Hatley would post every contract and payment within 30 days"), "Every legally disclosable contract, grant, amendment, and payment posted within 30 days"),
     ("sta-06", 2, HATLEY("Hatley would ban contributions from state contractors and create an elected auditor"), "David Hatley would ban contributions from significant state contractors"),
     ("gov-11", 1, HATLEY("Hatley would ban contributions from state contractors"), None),
     ("sta-11", 1, HATLEY("Hatley would end data center tax breaks"), "ends the giveaways: no PILOTs, no abatements"),
     ("sta-04", 1, HATLEY("Hatley would put data center tax revenue toward cutting homeowners’ property taxes"), None),
     ("sta-07", 2, HATLEY("Hatley would end technical college waitlists and pay instructors competitively"), "Pay TCAT instructors competitively, because you can’t scale a program you can’t staff."),
     ("edu-03", 2, HATLEY("Hatley would double registered apprenticeships"), "Double registered apprenticeships in four years."),
     ("cri-04", 1, HATLEY("Hatley would make life without parole mandatory for repeat child sex offenders"), None),
     ("cri-05", 2, HATLEY("Hatley would start reentry help 180 days before release"), "David Hatley will cut recidivism in half by giving them a path to work"),
     ("cri-08", 2, HATLEY("Hatley would expand drug, mental-health and veterans courts statewide"), "Drug, mental-health, and veterans courts expand to reach every judicial district, with treatment capacity funded alongside them."),
     ("sta-08", 2, HATLEY("Hatley would hire detectives and triple the TBI drug division"), "First we need to triple that division to about 150."))
JACKSON = site("Wendell Jackson", "https://www.wendelljackson4tngov2026.com/")
cand("TN-GOV", "TN-GOV:jackson", "Wendell Jackson", "I",
     "Comedian and spoken-word performer running a campaign that takes no money.",
     ("hea-01", 2, JACKSON("Jackson supports health care for all"), "Healthcare for all."),
     ("hea-06", 1, JACKSON("Jackson includes mental health care"), None),
     ("hou-01", 1, JACKSON("Jackson would make secure housing for all a priority"), "Secure housing for all will be a priority, for all Tennesseans."),
     ("sta-10", 1, JACKSON("Jackson would create incentives for businesses that hire local talent"), "Creating incentives for businesses that hire and train local talent."),
     ("sta-07", 1, JACKSON("Jackson would develop workforce training programs"), "Developing workforce training programs to equip Tennesseans with essential skills and knowledge."),
     ("edu-03", 1, JACKSON("Jackson would develop workforce training programs"), None))
PINKSTON = site("Lauren Pinkston", "https://www.pinkstonfortn.com/issues")
cand("TN-GOV", "TN-GOV:pinkston", "Lauren Pinkston", "I",
     "Former elementary school teacher who has worked against human trafficking for 15 years.",
     ("soc-07", 2, PINKSTON("Pinkston would add 50,000 day care and preschool slots by 2030"), "Add 50,000 daycare and preschool slots by 2030"),
     ("edu-06", -2, PINKSTON("Pinkston would end the 2025 voucher program and move its money to early childhood"), "End the school voucher experiment"),
     ("sta-02", 2, PINKSTON("Pinkston would invest in public schools"), "Lauren will invest in the schools nearly a million Tennessee students actually attend."),
     ("edu-01", 2, PINKSTON("Pinkston would invest in public schools"), None),
     ("edu-04", 2, PINKSTON("Pinkston would better fund teacher salaries"), "Lauren, a former teacher herself, will better fund salaries"),
     ("ene-02", 1, PINKSTON("Pinkston would expand nuclear capacity"), "expand nuclear and renewable capacity"),
     ("ene-01", 1, PINKSTON("Pinkston would expand renewable capacity and cut red tape on renewable projects"), None),
     ("hou-05", 1, PINKSTON("Pinkston would work with banks to lower down payments for first-time buyers"), "Partner with Tennessee banks to expand loan access and lower down payments"),
     ("eco-09", 2, PINKSTON("Pinkston would defend workers’ freedom to organize"), "Lauren will defend every Tennessean's freedom to organize"),
     ("gov-04", 2, PINKSTON("Pinkston wants an independent redistricting commission"), "Establish an independent commission to draw district maps."),
     ("gov-01", 1, PINKSTON("Pinkston supports term limits for legislators"), "Support term limits for legislators"),
     ("gov-07", 1, PINKSTON("Pinkston would repeal the state ban on ranked-choice voting"), "Repeal Tennessee's ban, imposed before it was ever tried"),
     ("gov-11", 1, PINKSTON("Pinkston supports public campaign financing"), None),
     ("sta-04", 1, PINKSTON("Pinkston would fully fund property tax freezes for low-income seniors"), None),
     ("sta-11", 1, PINKSTON("Pinkston would slow tax incentives to large corporations"), "the state should slow down tax incentives to large corporations already benefiting from Tennessee’s tax haven"),
     ("soc-08", 2, PINKSTON("Pinkston would close data broker loopholes in the state privacy law"), "close the loopholes in Tennessee's data privacy law that exempt many data brokers"),
     ("sta-07", 2, PINKSTON("Pinkston would expand technical college scholarships"), "Invest in high school trade education, expand TCAT scholarships"),
     ("edu-03", 2, PINKSTON("Pinkston would invest in high school trade education"), None),
     ("eco-02", 1, PINKSTON("Pinkston would end the grocery tax"), "End the grocery tax"),
     ("sta-12", 1, PINKSTON("Pinkston would explore statewide passenger rail"), "Lauren supports exploring a statewide passenger rail system connecting Memphis to Bristol and Nashville to Chattanooga"),
     ("soc-05", 0, PINKSTON("Pinkston backs medical cannabis and would let evidence guide recreational legalization"), "On recreational legalization, Lauren wants to see a well-run medical program work and let the evidence guide the next steps."),
     ("hea-09", 1, PINKSTON("Pinkston would expand primary and preventive care for adults"), None),
     ("hea-06", 1, PINKSTON("Pinkston would expand rural mental health access"), "support expanding rural mental health access"))
VICK = site("Robert Vick", "https://drvick4tn.com/issues")
cand("TN-GOV", "TN-GOV:vick", "Robert Vick", "I",
     "Career educator from White Pine in Jefferson County: 12 years a teacher and 28 an administrator.",
     ("sta-09", 1, VICK("Vick would fund rural hospitals, ERs and maternity wards for the long term"), "create sustainable, long-term funding models that keep rural ERs and maternity wards open"),
     ("hea-06", 2, VICK("Vick calls mental health a core priority"), "Mental Health is one of my core priorities"),
     ("agr-01", 1, VICK("Vick would expand the farmland preservation fund and cut taxes on farm inputs"), None),
     ("sta-08", 1, VICK("Vick would give officers the training and resources they need"), None),
     ("edu-04", 1, VICK("Vick wants teachers well compensated"), "ensuring our outstanding educators are respected, well-compensated, and supported"),
     ("edu-03", 1, VICK("Vick would push for vocational training"), "I will continue to prioritize literacy and push for vocational training."),
     ("ene-10", 1, VICK("Vick would push TVA to put ratepayers first"), None))

# Texas governor --------------------------------------------------------------------
DIXON = lambda path, note: page(f"Pat Dixon campaign site: {note}", f"https://patdixon.org/{path}/", READ)
cand("TX-GOV", "TX-GOV:dixon", "Pat Dixon", "L",
     "Libertarian and former city council member who has worked with the Texas Legislature since 2004.",
     ("cri-09", -2, DIXON("death-penalty", "Dixon opposes the death penalty and would support repeal"), "I oppose the death penalty."),
     ("soc-04", -1, DIXON("abortion", "Dixon calls himself pro-life but prefers persuasion and adoption to police action"), None),
     ("sta-04", 1, DIXON("property-tax", "Dixon would cut spending first to lower taxes"), "I will work on identifying spending cuts first, which will lead to lower taxes."),
     ("edu-06", 2, DIXON("school-choice", "Dixon would like a statewide scholarship that follows every child"), "Every child would be given the same amount of money to follow them to any school."),
     ("gov-04", 1, DIXON("non-partisan-redistricting", "Dixon supports nonpartisan district maps drawn by software"), "It would allow the software to produce non-partisan district maps that are compact and fair."),
     ("gov-07", 1, DIXON("approval-voting", "Dixon would let cities use approval or ranked-choice voting"), "I also support Ranked Choice"),
     ("imm-03", 1, DIXON("the-border", "Dixon says legal immigration paperwork is nearly impossible"), None),
     ("soc-05", 2, DIXON("texas-cannabis-policy-questionnaire", "Dixon says adult-use cannabis should be legal"), "It should be legal. End the war on drugs."))

# Sites that load only in a browser (read in the browser pane, quotes checked
# against each live page's text) ----------------------------------------------------
LOMBARDO = site("Risa Lombardo", "https://risalombardo.com/issues/")
cand("AZ-GOV", "AZ-GOV:lombardo", "Risa Lombardo", "G",
     "Registered with both major parties over the years, mostly as a Democrat; now the Green Party nominee.",
     ("ene-01", 2, LOMBARDO("Lombardo’s issues page calls for moving off fossil fuels to renewable energy"), "We need to get off fossil fuels and on to renewable energy."),
     ("ene-03", -2, LOMBARDO("Lombardo’s issues page calls for getting off fossil fuels"), None),
     ("sta-03", 1, LOMBARDO("Lombardo’s issues page demands a living wage"), "We demand a living wage and a real safety net."),
     ("gov-11", 1, LOMBARDO("Lombardo’s issues page calls for public financing of elections"), "We demand public financing of elections, open debates, and more representative voting systems."))
HARRINGTON = site("Whitfield Harrington Jr.", "https://whit4ilsenate.com/")
HARRINGTON_QA = site("Whitfield Harrington Jr.", "https://whit4ilsenate.com/where-i-stand")
cand("IL-SEN", "IL-SEN:harrington", "Whitfield Harrington Jr.", "I",
     "Born in Belzoni, Mississippi, the son of a civil rights leader; running as an independent while forming the American Center Party.",
     ("ene-03", 1, HARRINGTON("Harrington would use domestic energy to bring costs down"), "Use America's domestic energy resources to bring costs down now while continuing to build the renewable capacity the country will need for the future."),
     ("ene-01", 1, HARRINGTON("Harrington would keep building renewable capacity"), None),
     ("hou-05", 1, HARRINGTON("Harrington would make smaller mortgages available to working families"), "Make smaller mortgages available so working families can buy affordable homes"),
     ("edu-02", 1, HARRINGTON("Harrington would make the first year of community college free"), "Make the first year of community college free"),
     ("def-01", -1, HARRINGTON("Harrington would redirect part of defense spending to infrastructure at home"), "Redirect a portion of defense spending toward America's bases, roads, bridges, rail, power grid, and strategic stockpiles"),
     ("eco-06", 1, HARRINGTON("Harrington would put money into roads, bridges, rail and the grid"), None),
     ("def-04", 1, HARRINGTON("Harrington wants clear missions and congressional accountability overseas"), None),
     ("def-08", -1, HARRINGTON("Harrington would have allies carry more of their own defense and cut open-ended commitments"), "require allies to carry more of their own defense burden, reduce open-ended commitments"),
     ("gov-01", 2, HARRINGTON("Harrington supports consecutive term limits"), "Break Washington's cycle of permanent power through consecutive term limits"),
     ("imm-07", 2, HARRINGTON("Harrington would deport criminals and prevent family separation"), "deport criminals, enforce the law with dignity, prevent family separation"),
     ("imm-03", 1, HARRINGTON("Harrington would make legal immigration easier than illegal entry"), "make legal immigration easier than illegal entry"),
     ("edu-06", 1, HARRINGTON_QA("Harrington supports school choice"), "I support school choice"),
     ("edu-01", 1, HARRINGTON_QA("Harrington supports fairer funding for schools in poorer communities"), None),
     ("gov-05", 1, HARRINGTON_QA("Harrington supports voter ID"), "I support voter identification, early in-person voting, absentee ballots for people who request or need them"),
     ("gov-06", 0, HARRINGTON_QA("Harrington supports early in-person voting and absentee ballots on request but opposes universal mail-in voting"), "I oppose universal mail-in voting"),
     ("soc-04", 2, HARRINGTON_QA("Harrington is pro-life and would protect unborn life in all circumstances"), "the law should protect that life in all circumstances"),
     ("soc-03", -2, HARRINGTON_QA("Harrington is pro-life"), None),
     ("def-11", 1, HARRINGTON_QA("Harrington says the U.S. should remain a friend of Israel"), None),
     ("def-12", -1, HARRINGTON_QA("Harrington would give military aid as arms sales or loans rather than grants"), "United States military assistance should generally be provided through American arms sales or repayable loans"),
     ("def-13", -1, HARRINGTON_QA("Harrington would give military aid as arms sales or loans rather than grants"), None),
     ("soc-12", -1, HARRINGTON_QA("Harrington opposes biological males in female sports"), "I do not support biological males competing in female sports."),
     ("soc-06", 1, HARRINGTON_QA("Harrington would protect the freedom to practice any faith or none"), None),
     ("soc-10", -1, HARRINGTON_QA("Harrington would vote his biblical view of marriage"), "If called upon to vote on the definition of marriage, I would vote according to my biblical convictions."))
CHRISTENSEN = site("Lydia Christensen", "https://www.lydialynnchristensen.com/issues")
cand("MI-SEN", "MI-SEN:christensen", "Lydia Christensen", "L",
     "Upper Peninsula native from an Ironwood family; the Libertarian nominee.",
     ("soc-08", 2, CHRISTENSEN("Christensen would introduce a Bill of Digital Rights making data your property"), "introduce a Bill of Digital Rights making your data your property"),
     ("soc-05", 2, CHRISTENSEN("Christensen would legalize cannabis and psilocybin federally"), "Lydia will push for federal legalization of cannabis and psilocybin"),
     ("cri-09", -2, CHRISTENSEN("Christensen opposes the death penalty"), "Lydia opposes the death penalty."),
     ("eco-02", 2, CHRISTENSEN("Christensen would end federal income tax on earnings under $150,000"), "No federal income tax on any earnings under $150,000 a year"),
     ("eco-10", -2, CHRISTENSEN("Christensen would remove tariffs"), "Lydia supports removing tariffs and other government barriers to trade."),
     ("agr-07", -2, CHRISTENSEN("Christensen would remove tariffs"), None),
     ("agr-06", 1, CHRISTENSEN("Christensen supports free trade"), None),
     ("ene-02", 1, CHRISTENSEN("Christensen wants faster nuclear licensing"), "faster nuclear licensing without cutting safety"),
     ("ene-01", 1, CHRISTENSEN("Christensen would fix the permitting queue stalling wind and solar"), "a fix for the federal permitting queue stalling wind and solar"),
     ("def-04", 2, CHRISTENSEN("Christensen would vote to end unauthorized hostilities"), "Lydia will vote for binding resolutions to end unauthorized hostilities"),
     ("def-15", -2, CHRISTENSEN("Christensen opposes the war in Iran without authorization"), "oppose further war funding without authorization"),
     ("def-07", 2, CHRISTENSEN("Christensen would make diplomacy the first response"), "restore real diplomacy as the first response"),
     ("def-12", -1, CHRISTENSEN("Christensen would vote against military aid to Israel until compliance is verified"), "Lydia would vote against continued military aid until compliance is independently verified"),
     ("def-11", -1, CHRISTENSEN("Christensen cites findings of genocidal acts in Gaza"), None),
     ("def-01", -1, CHRISTENSEN("Christensen would cap the Pentagon budget to fund rapid rehousing"), "funded by capping the Pentagon budget rather than cutting help for people"),
     ("gov-11", 2, CHRISTENSEN("Christensen would end Citizens United"), "Unchain Michigan’s democracy by ending Citizens United"),
     ("gov-13", -2, CHRISTENSEN("Christensen would end Citizens United"), None),
     ("gov-05", -1, CHRISTENSEN("Christensen opposes voter ID rules that turn away legal citizens"), "oppose voter ID rules that turn away legal citizens over a name or gender-marker mismatch"),
     ("gov-07", 2, CHRISTENSEN("Christensen supports ranked-choice voting"), "Ranked choice voting lets voters rank candidates instead of picking just one, ending the spoiler effect."),
     ("hea-01", 2, CHRISTENSEN("Christensen proposes Medicaid for All"), "Medicaid for All is opt-in coverage for citizens and legal residents."),
     ("hea-03", 2, CHRISTENSEN("Christensen proposes Medicaid for All"), None),
     ("hea-02", 1, CHRISTENSEN("Christensen would fund it partly through drug price negotiation"), None),
     ("eco-03", 2, CHRISTENSEN("Christensen would raise the federal minimum wage to $15"), "a federal minimum wage increase to $15 per hour"),
     ("eco-09", 2, CHRISTENSEN("Christensen would restore secondary and sympathy strikes"), "restore the right to secondary and sympathy strikes"),
     ("soc-02", 2, CHRISTENSEN("Christensen would pass the Equality Act"), "Lydia will fight to pass the Equality Act"),
     ("soc-12", 2, CHRISTENSEN("Christensen would defend LGBTQIA+ civil rights"), None),
     ("soc-10", 2, CHRISTENSEN("Christensen would defend marriage equality in federal law"), "defend equal marriage rights for everyone under federal law"),
     ("soc-03", 2, CHRISTENSEN("Christensen would codify abortion rights up to viability"), "Lydia will codify the right to abortion up to viability"),
     ("soc-04", -2, CHRISTENSEN("Christensen would codify abortion rights"), None),
     ("imm-02", 2, CHRISTENSEN("Christensen would give Dreamers a path to citizenship"), "offering them a pathway to citizenship"),
     ("imm-08", -2, CHRISTENSEN("Christensen would abolish ICE"), "Lydia will work to abolish ICE"),
     ("cri-05", 1, CHRISTENSEN("Christensen would focus the justice system on rehabilitation"), "reforms that reduce mass incarceration and focus on rehabilitation"),
     ("hou-09", 2, CHRISTENSEN("Christensen supports federal investment in fiber broadband for all"), "federal investment in fiber optic broadband for all"),
     ("hou-04", 1, CHRISTENSEN("Christensen would fund zoning reform"), "She will fund zoning reform"),
     ("ene-04", 2, CHRISTENSEN("Christensen wants tougher Clean Water Act enforcement"), "push for federal enforcement of the Clean Water Act with real teeth"))
USTPM = lambda note: page(f"U.S. Taxpayers Party of Michigan candidate page (brandenburgforgovernor.com forwards here): {note}", "https://ustpm.org/candidates?id=74", READ)
cand("MI-GOV", "MI-GOV:brandenburg", "Donna Brandenburg", "U.S. Taxpayers",
     "Michigan-born entrepreneur in energy, real estate, farming and technology.",
     ("sta-04", 2, USTPM("Brandenburg would eliminate property taxes"), "eliminating property taxes and the state income tax"),
     ("eco-02", 2, USTPM("Brandenburg would eliminate the state income tax"), None))
cand("MN-SEN", "MN-SEN:simonetti", "Marisa Simonetti", "I", None, officialSite=None)  # domain is parked
YOUNG = site("Steven Young", "https://steveformngov.info/")
cand("MN-GOV", "MN-GOV:young", "Steven Young", "G",
     "Former Marine, attorney and neighborhood grocery store owner from Minneapolis.",
     ("imm-08", -2, YOUNG("Young would make Minnesota a sanctuary state and resist ICE"), "Abolishing ICE"),
     ("hea-01", 1, YOUNG("Young lists Medicare for All among his answers"), "UBI, M4A, jobs jobs and more jobs!"))
cand("MT-SEN", "MT-SEN:austin", "Kyle Austin", "L",
     "Pharmacist who founded an independent pharmacy in Billings and owns his grandfather’s farm on the Hi-Line.")
RICHARDS = site("Robin Richards", "https://robinforne.com/issues")
cand("NE-SEN", "NE-SEN:richards", "Robin Richards", "Working People",
     "Ralston school board member running for the Nebraska Working People Party.",
     ("edu-01", 2, RICHARDS("Richards wants fully funded public schools"), "Our public schools deserve the support to serve every community."))
LINDSTROM = lambda note: page(f"Brett Lindstrom campaign site (The Nebraska Doctrine): {note}", "https://nebraskadoctrine.com/", READ)
cand("NE-GOV", "NE-GOV:lindstrom", "Brett Lindstrom", "America First", None,
     ("sta-04", 1, LINDSTROM("Lindstrom would take pressure off property taxes"), "Take the pressure off property taxes and make valuations something you can plan around."),
     ("hou-09", 1, LINDSTROM("Lindstrom would finish expanding rural internet"), "Finish the job on rural internet."))
GOTRA = site("Jasjit Gotra", "https://governorgotra.com/")
cand("RI-GOV", "RI-GOV:gotra", "Jasjit Gotra", "I",
     "Entrepreneur from East Greenwich running with the Unaffiliated Movement.",
     ("eco-02", 1, GOTRA("Gotra would end the state tax on Social Security within two years"), None),
     ("hou-04", 2, GOTRA("Gotra would build 20,000 homes in four years and cut zoning barriers"), "Build 20,000 units in 4 years. Cut zoning barriers."),
     ("hea-01", 1, GOTRA("Gotra calls health care a right and would cap out-of-pocket costs"), "Healthcare is a right, not a luxury."),
     ("gov-12", 2, GOTRA("Gotra would publish a quarterly state profit-and-loss statement"), "Every taxpayer sees where every dollar goes."),
     ("ene-10", 1, GOTRA("Gotra would cut energy costs 30% in four years"), None))
cand("SC-GOV", "SC-GOV:addison", "Michael Addison", "United Citizens",
     "Orangeburg medical director and community organizer (foreclosure prevention, job training, homeless relief); also a licensed asbestos inspector.")
JONES = site("Robert Jones", "https://www.robertfortn.com/issues")
cand("TN-SEN", "TN-SEN:jones", "Robert Jones", "I",
     "Independent who takes no campaign donations and asks supporters to give to local nonprofits instead.",
     ("ene-01", 1, JONES("Jones would focus on renewable energy and conservation"), "By focusing on renewable energy, conservation efforts, and responsible resource management"),
     ("eco-09", 1, JONES("Jones would advocate for fair treatment and wages for workers"), "I will advocate for equitable treatment, wages that represent your value, and improved work-life balance."),
     ("gov-11", 1, JONES("Jones would limit big business influence in politics"), "The goal is to limit or prevent any corruptibility of the party system and any large businesses interfering within the political realm."),
     ("def-07", 1, JONES("Jones warns that striking first makes enemies"), "Striking first radicalizes generations of people against your power."))
ABIDI = lambda n, note: page(f"Misam Abidi campaign site: {note}", f"https://www.misamforgovernor.com/pillar/{n}", READ)
cand("TN-GOV", "TN-GOV:abidi", "Misam Abidi", "I",
     "Banker and entrepreneur, including in crypto, from Nolensville; came to the U.S. in 1997.",
     ("hea-07", 1, ABIDI(3, "Abidi would create a state reinsurance program to cut premiums"), "Establish a state reinsurance structure"),
     ("hea-09", 1, ABIDI(3, "Abidi would encourage preventive care"), None),
     ("edu-03", 2, ABIDI(4, "Abidi would guarantee every graduate a practical skill, with trade training and apprenticeships"), "The Tennessee Skills Guarantee ensures every student graduates with at least one practical economic skill they can rely on."),
     ("edu-10", 1, ABIDI(4, "Abidi would teach financial literacy"), None),
     ("sta-07", 1, ABIDI(4, "Abidi would expand trade skill training"), None))
cand("VT-GOV", "VT-GOV:roy", "Dean Roy", "Freedom and Unity",
     "Stowe native and former Vermont legislative page.")
JEWETT = site("Scott Jewett", "https://scottjewett.com/")
JEWETT_PLATFORM = lambda note: page(f"Scott Jewett campaign site, platform page (the Libertarian Party of Florida platform): {note}", "https://scottjewett.com/platform/", READ)
cand("FL-GOV", "FL-GOV:jewett", "Scott Jewett", "L",
     "Boca Raton entrepreneur running as the Libertarian nominee with Nicole Skelly.",
     ("edu-06", 2, JEWETT("Jewett wants education dollars to follow the child"), "We support real school choice so education dollars follow the child, not the system."),
     ("eco-02", 1, JEWETT("Jewett would cut taxes"), "Cut Taxes and Regulations"),
     ("imm-08", -1, JEWETT_PLATFORM("The platform opposes enlisting state and local employees to enforce federal immigration law"), None),
     ("gov-07", 1, JEWETT_PLATFORM("The platform supports ranked-choice voting"), "We support Ranked Choice."),
     ("gov-03", -1, JEWETT_PLATFORM("The platform favors voluntary disclosure of campaign contributions"), "We support a structure for candidates to voluntarily disclose campaign contributions."),
     ("gov-12", 1, JEWETT_PLATFORM("The platform would apply Sunshine laws to all public employees"), None))
KRAWCHUK = lambda path, note: page(f"Ken Krawchuk campaign site: {note}", f"https://www.kenk4pa.com/{path}", READ)
cand("PA-GOV", "PA-GOV:krawchuk", "Ken Krawchuk", "L", None,
     ("edu-06", 2, KRAWCHUK("", "Krawchuk would privatize the public schools"), "Privatize the public schools!"),
     ("sta-02", -1, KRAWCHUK("", "Krawchuk would privatize the public schools"), None),
     ("sta-04", 2, KRAWCHUK("", "Krawchuk would eliminate most property tax"), "Property tax is the worst tax imaginable."),
     ("eco-02", 1, KRAWCHUK("", "Krawchuk would veto all tax increases"), "Veto all tax increases and pork barrel spending."),
     ("soc-05", 2, KRAWCHUK("issues/drugs/", "Krawchuk would decriminalize marijuana and treat it like alcohol"), "Immediately decriminalize marijuana and other drugs, and treat them like we do alcohol."),
     ("cri-08", 1, KRAWCHUK("issues/drugs/", "Krawchuk favors treatment, not jail"), "Treatment, not jail."),
     ("soc-10", 1, KRAWCHUK("issues/lgbt/", "Krawchuk would give same-sex couples the same legal privileges"), "Whatever legal privileges are made available to traditional couples should also be made available for same-sex couples"),
     ("soc-02", -1, KRAWCHUK("issues/lgbt/", "Krawchuk opposes special protections for any group"), "I would oppose any law granting special protections or quotas for gays, women, minorities, businesses, or politicians"),
     ("ene-03", 1, KRAWCHUK("issues/environment/", "Krawchuk calls the fracking boom good for Pennsylvania"), "The fracking boom is good for Pennsylvania"),
     ("gov-06", -2, KRAWCHUK("issues/elections/", "Krawchuk would eliminate mail-in ballots"), "Eliminate mail-in ballots in favor of in-person voting"),
     ("gov-05", 2, KRAWCHUK("issues/elections/", "Krawchuk would require ID to vote"), "Require positive ID for citizens to vote"),
     ("gov-01", 1, KRAWCHUK("issues/elections/", "Krawchuk supports term limits"), "Institute term limits"),
     ("gov-04", 1, KRAWCHUK("issues/elections/", "Krawchuk would end gerrymandering with algorithmic districting"), None),
     ("cri-04", 2, KRAWCHUK("issues/crime/", "Krawchuk would eliminate parole for violent criminals"), "Eliminate parole for violent criminals."))
FORD = site("Danielle Ford", "https://daniellefornevada.com/platform/")
cand("NV-GOV", "NV-GOV:danielle-ford", "Danielle Ford", "I",
     "Las Vegas native and marketer on the Nevada State Board of Education; a former Clark County School District trustee.",
     ("soc-03", 2, FORD("Ford supports Nevada’s protection of abortion access through 24 weeks"), "She supports Nevada’s current legal framework protecting abortion access through 24 weeks"),
     ("soc-04", -1, FORD("Ford supports the current framework"), None),
     ("gov-05", 0, FORD("Ford supports identity verification but only if ID rules are accessible and phased in"), "Any ID or document requirement must be constitutional, funded, accessible, carefully phased in"),
     ("sta-11", 2, FORD("Ford would scrutinize contracts and tax abatements before any new taxes"), "the state should take a much harder look at public contracts, procurement loopholes, no-bid arrangements, tax abatements"),
     ("gov-12", 2, FORD("Ford says public money belongs to the public"), "Public money belongs to the public."),
     ("ene-10", 1, FORD("Ford wants stronger ratepayer protection and affordable energy"), "push for policies that keep energy reliable and affordable"),
     ("imm-07", 1, FORD("Ford would keep enforcement focused on serious harm"), "Danielle does not believe undocumented status alone should be treated the same as violent crime or organized criminal activity."),
     ("sta-02", 1, FORD("Ford wants school funding to reflect the real cost of serving students"), "Danielle believes school funding should reflect the real cost of serving students well."),
     ("edu-01", 1, FORD("Ford wants school funding to reflect the real cost of serving students"), None),
     ("cri-08", 1, FORD("Ford would strengthen mental health care and addiction treatment alongside policing"), "Danielle supports law enforcement while also strengthening mental health care, addiction treatment, crisis response"),
     ("hea-06", 1, FORD("Ford would strengthen mental health care"), None),
     ("hou-02", 1, FORD("Ford would scrutinize corporate ownership and build-to-rent practices"), "scrutinizing corporate ownership and build-to-rent practices"),
     ("gov-03", 2, FORD("Ford supports stronger campaign finance transparency"), "Danielle supports stronger campaign finance transparency"),
     ("gov-11", 1, FORD("Ford supports reforms that reduce the influence of money"), None),
     ("soc-08", 1, FORD("Ford supports privacy protections and student data safeguards"), None))

# Candidates without a working campaign site: news interviews and voter guides --------
NE_EXAMINER = article("Nebraska Examiner, July 27, 2026", "https://nebraskaexaminer.com/2026/07/27/beard-talks-priorities-pivot-from-nebraska-primary-election-to-nov-3-faceoff/", "2026-07-27")
cand("NE-GOV", "NE-GOV:beard", "Rick Beard", "Legal Marijuana Now",
     "Omaha wine professional and private chef; the Legal Marijuana NOW nominee.",
     ("gov-11", 2, NE_EXAMINER("Beard would get corporate and PAC money out of state politics"), "getting corporate and political action committee money out of the state"),
     ("soc-05", 0, NE_EXAMINER("Beard would keep cannabis medical for now, citing federal protections, with a state-run medical program"), None),
     ("sta-10", -1, NE_EXAMINER("Beard says the state must eliminate tax breaks for corporations"), None),
     ("eco-01", 1, NE_EXAMINER("Beard would end tax breaks for Nebraska’s ultra-rich"), None),
     ("sta-04", 1, NE_EXAMINER("Beard would use cannabis revenue to reduce property taxes"), "the actual ability to reduce property taxes"),
     officialSite=None)  # rickforgov.org answers with a 404 page
WHYY_NJ = article("WHYY, Sept. 22, 2026", "https://whyy.org/articles/election-2026-new-jersey-senate-voter-guide-booker/", "2026-09-22")
cand("NJ-SEN", "NJ-SEN:kuniansky", "Joanne Kuniansky", "Socialist Workers",
     "Union activist who has worked as a refinery operator, meatpacker and Walmart deli worker; a Socialist Workers Party member since 1977, from West New York.",
     ("eco-09", 2, WHYY_NJ("Kuniansky calls on workers to build union solidarity"), "The Socialist Workers Party calls on workers to build solidarity with unions fighting attacks on our wages and conditions"),
     ("eco-06", 2, WHYY_NJ("Kuniansky supports a public works program building hospitals, child care centers and other infrastructure"), "a public works program to provide jobs at union-scale wages to build hospitals, child care centers and other infrastructure"),
     ("eco-13", 2, WHYY_NJ("Kuniansky supports a shorter work week with no pay cut"), "She also supports enacting a shorter work week with no pay cuts."),
     ("imm-02", 2, WHYY_NJ("Kuniansky calls for amnesty for workers without papers"), "calling for an amnesty for workers in the U.S. without papers"),
     ("def-15", -2, WHYY_NJ("Kuniansky opposes the U.S. war in Iran"), "an imperialist war by the U.S. rulers to plunder oil, gas and labor of the region"))
SEVEN_DAYS_VT = article("Seven Days, Oct. 13, 2026", "https://www.sevendaysvt.com/guides/electionvoterguide/candidates-vermont-governor-2026/", "2026-10-13")
GOODBAND = site("June Goodband", "https://june4govvt.org/")
cand("VT-GOV", "VT-GOV:goodband", "June Goodband", "Peace and Justice",
     "Licensed clinical mental health counselor from Springfield; the Peace and Justice Party nominee.",
     ("hea-01", 2, SEVEN_DAYS_VT("Goodband would fully implement Vermont’s universal health care law"), "We can cut health care costs by fully implementing our universal health care law, cutting out insurance companies"),
     ("hea-04", -2, SEVEN_DAYS_VT("Goodband would cut insurance companies out of health care"), None),
     ("hou-01", 2, SEVEN_DAYS_VT("Goodband would have the state build and renovate housing"), "The state should build and buy/renovate housing"),
     ("hou-05", 1, GOODBAND("Goodband supports home ownership through co-ops and no-interest mortgages"), None),
     ("sta-03", 2, GOODBAND("Goodband would require profitable businesses to pay a living wage"), "require profitable businesses to pay a living wage so their workers don’t need state assistance"),
     ("eco-01", 2, GOODBAND("Goodband would raise taxes on high incomes"), "Increase taxes on high incomes"),
     ("eco-12", 2, GOODBAND("Goodband would pay for schools with progressive taxes instead of homestead taxes"), "Use Progressive taxation instead of homestead taxes to pay for education."),
     ("cri-07", 1, GOODBAND("Goodband wants safety strategies that work better than prisons"), "Develop creative strategies that protect people, work better than prisons, and cost less."),
     officialSite="https://june4govvt.org/")

HUBER = site("Blake Huber", "https://lpcocolorado.my.canva.site/blake-huber-us-senate-website")
cand("CO-SEN", "CO-SEN:huber", "Blake Huber", "L",
     "Longtime election-reform activist and former property and business manager; a former chair of the Colorado Libertarian Party.",
     ("imm-03", 2, HUBER("Huber would streamline legal entry for background-checked workers"), "We support streamlining legal pathways so that background-checked, hard-working individuals can legally enter, work, and contribute"),
     ("imm-01", 1, HUBER("Huber says a sovereign nation needs secure, orderly borders"), None),
     officialSite="https://lpcocolorado.my.canva.site/blake-huber-us-senate-website")
OCC_SEN = lambda note: page(f"Oregon Capital Chronicle voter guide, candidates’ answers: {note}", "https://oregoncapitalchronicle.com/voter-guides/contests/2026-general-u-s-senate/", READ)
cand("OR-SEN", "OR-SEN:henry", "Chris Henry", "Progressive",
     "Long-haul truck driver and former aircraft electrician; the Progressive and Pacific Green nominee, taking no corporate money.",
     ("edu-02", 2, OCC_SEN("Henry supports free public education from pre-K through college"), "free publicly-funded education from pre-K to trade guilds and higher education"),
     ("hea-01", 2, OCC_SEN("Henry would adopt single-payer health care"), "Adopt comprehensive single-payer medical care for all."),
     ("hea-03", 2, OCC_SEN("Henry would adopt single-payer health care"), None),
     ("hea-02", 2, OCC_SEN("Henry would negotiate prices on all prescription drugs"), "Negotiate prescription-drug prices on all drugs (not just a select few)"),
     ("ene-06", 1, OCC_SEN("Henry would tax emissions that cause climate change"), "Adopt comprehensive taxation of emissions and other practices that contribute to climate change."),
     ("ene-01", 2, OCC_SEN("Henry would accelerate the move to renewable energy"), "Accelerate the transition to renewable energy and energy-efficient buildings and transportation."),
     ("ene-07", 2, OCC_SEN("Henry would expand public transit and passenger rail"), "Expand public transportation, including passenger rail and freight rail"),
     ("ene-03", -1, OCC_SEN("Henry would end fossil fuel subsidies"), None),
     ("eco-01", 2, OCC_SEN("Henry would raise taxes on extreme income and wealth"), "Raise federal taxes on extreme concentrations of income and wealth."),
     ("eco-12", 2, OCC_SEN("Henry supports a progressive wealth tax"), "Establish a carefully designed progressive wealth tax."),
     ("eco-02", 2, OCC_SEN("Henry would substantially cut income taxes for non-wealthy families"), "Substantially reduce federal income taxes on non-wealthy families and individuals."),
     ("imm-02", 2, OCC_SEN("Henry supports a path to citizenship for long-term undocumented residents"), "Establish a fair path to citizenship for long-term undocumented residents."),
     ("imm-04", 2, OCC_SEN("Henry would expand immigration courts and judges"), "Expand immigration courts, judges, interpreters and access to legal representation."),
     ("imm-06", 1, OCC_SEN("Henry would preserve access to asylum and refugee protection"), None),
     ("imm-08", -1, OCC_SEN("Henry would replace ICE’s militarized model"), None),
     ("gov-11", 2, OCC_SEN("Henry would amend the Constitution to reverse Citizens United"), "Reverse Citizens United and establish that corporations do not have the rights of individuals"),
     ("gov-13", -2, OCC_SEN("Henry says corporations do not have the rights of individuals"), None),
     ("gov-06", 2, OCC_SEN("Henry would require vote-by-mail nationwide"), "requiring universal availability of vote-by-mail"),
     ("def-07", 1, OCC_SEN("Henry would end pointless wars"), None),
     ("eco-09", 1, OCC_SEN("Henry supports workplace democracy and strong workplace safety"), None),
     officialSite="https://chrishenry.org/")
cand("OR-SEN", "OR-SEN:dye", "Gary Lyndon Dye", "L",
     "Got 1.8% for the U.S. Senate in 2020 and has run as a Libertarian or Republican in every election since at least 2016; did not answer the Capital Chronicle’s questionnaire.")
cand("OK-GOV", "OK-GOV:brooks", "Robert Brooks Sr.", "I",
     "Independent who would poll voters through an app before signing or vetoing bills.",
     ("sta-06", 1, site("Robert Brooks Sr.", "https://votewethepeople.com/")("Brooks has zero tolerance for pay-to-play politics"), "Zero tolerance for pay-to-play politics."),
     officialSite="https://votewethepeople.com/")
cand("OK-GOV", "OK-GOV:griffin", "Jerry Griffin", "I", None,
     officialSite="https://drjerrtg.substack.com/p/griffin-for-governor-2026")  # governorgriffin2027.com doesn't load

# Campaign sites found Oct. 27 through the candidates' Wikipedia articles and
# BallotReady profiles (the links are in campaign_sites_2026.py) -----------------
WITHROW = site("Adam Withrow", "https://www.senatorwithrow.com/", READ27)
WITHROW2 = site("Adam Withrow", "https://www.senatorwithrow.com/platform-discussion", READ27)
cand("CO-SEN", "CO-SEN:withrow", "Adam Withrow", "Unity", "Former county jail detention officer and contractor, running on the Unity Party line.",
     ("ene-01", 2, WITHROW2("Withrow would raise the solar tax credit, make it permanent and restore rebates"), "Let's increase the solar tax credit, make it permanent, and bring back the rebates!"),
     ("ene-09", 1, WITHROW2("Withrow wants incentives for American companies to make solar panels"), "let's create incentives for American companies to make 'em here"),
     ("ene-03", -1, WITHROW("Withrow calls fossil fuels obsolete and wants a transition away from them"), "Fossil fuels are obsolete."),
     ("hea-01", 1, WITHROW("Withrow wants a health care system that works for everyone"), "Healthcare for all would cost less than half of our defense budget."),
     ("def-07", 2, WITHROW("Withrow is against every war and favors free trade and equality over bombs"), "Free trade and mutual global recognition of equality will accomplish what a billion pounds of bombs can not."),
     ("agr-06", 1, WITHROW("Withrow favors free trade over war"), None),
     ("eco-03", 2, WITHROW2("Withrow says raising the federal minimum wage is vital, pegged to consumer prices"), "I believe a raise in the Federal Minimum Wage is vital."),
     ("def-03", 1, WITHROW2("Withrow supports expanded re-entry programs for veterans"), "Yes, I support expanded re-entry programs to help adapt to civilian life."),
     ("soc-03", 1, WITHROW2("Withrow supports women’s reproductive health care choices"), "Anybody out here think women should have reproductive healthcare choices? Good."))
GILLESPIE = site("Neil Gillespie", "https://neilgillespie4senate.blogspot.com/", READ27)
cand("FL-SEN", "FL-SEN:gillespie", "Neil Gillespie", "I", "Founder and director of the Justice Network, an advocacy blog; a licensed motor vehicle dealer in Pennsylvania before moving to Florida in 1993.",
     ("imm-02", 1, GILLESPIE("Gillespie supports a path to citizenship for immigrants who follow the rules (his League of Women Voters answers)"), "I also support a path to citizenship for immigrants who follow the rules"),
     ("imm-01", 1, GILLESPIE("Gillespie supports secure borders and vetting immigrants (his League of Women Voters answers)"), None),
     ("hea-01", 1, GILLESPIE("Gillespie proposes national health coverage with the ability to opt out"), "I propose national health coverage, with the ability to opt-out."),
     ("def-11", -1, GILLESPIE("Gillespie says Israel’s wars are creating antisemitism worldwide"), "Its wars are creating antisemitism worldwide."),
     ("soc-01", 1, GILLESPIE("Gillespie lists the First Amendment’s freedoms of speech and the press among his top priorities"), None))
MARSH = site("Douglas P. Marsh", "https://www.electmarsh.org/", READ27)
cand("MI-SEN", "MI-SEN:marsh", "Douglas P. Marsh", "G", None,
     ("hea-01", 2, MARSH("Marsh supports a single-payer health system"), "The best way to ensure this is with a single-payer system."),
     ("hea-03", 2, MARSH("Marsh supports a single-payer health system"), None),
     ("hou-02", 2, MARSH("Marsh says private equity companies should not own homes"), "Private equity companies should not own residential property."),
     ("hou-06", 1, MARSH("Marsh would tie rents to local wages and regulate short-term rentals"), "Rental rates should be tied to an area's prevailing wages"),
     ("def-15", -2, MARSH("Marsh would immediately end hostilities against Iran"), "The United States of America should immediately cease hostilities against Iran"),
     ("def-12", -2, MARSH("Marsh calls continued weapons and funding for proxy wars, apartheid and genocide unconscionable"), "The continued supply of weapons and funding for proxy wars, apartheid, and genocide is unconscionable."),
     ("def-13", -1, MARSH("Marsh opposes arming proxy wars and seeks permanent ceasefires, Ukraine included"), None),
     ("def-07", 2, MARSH("Marsh would use U.S. economic and diplomatic leverage for permanent ceasefires"), None),
     ("hou-08", 1, MARSH("Marsh wants jobs rebuilding bridges and roads"), "Michiganders need quality, longterm jobs rebuilding our bridges and roads"),
     ("ene-01", 1, MARSH("Marsh wants jobs developing green energy infrastructure"), None),
     ("ene-03", -1, MARSH("Marsh would build green energy instead of kowtowing to big oil"), "developing green energy infrastructure for our children, instead of kowtowing to big oil"))

# Campaign sites that load only in a browser, read in the browser pane on Oct. 27;
# every quote was checked against the live page's text.
more("OK-GOV", "OK-GOV:griffin", bio="Marine veteran and educator who has taught at the University of Tulsa, Texas State and the University of Oklahoma; chief executive of The Palomega Company.")

# Alaska Senate: the namesake on the ballot ----------------------------------------
cand("AK-SEN", "AK-SEN:dan-j-sullivan", "Dan J. Sullivan", "R",
     "Petersburg resident for nearly 50 years: former U.S. Forest Service timber worker and elementary school teacher. Not the incumbent senator, Dan S. Sullivan.")

# VOTE411, the League of Women Voters' guide: candidates' own unedited answers, read
# Oct. 27 in the browser pane; quotes were checked against the page text.
V411_MIGOV = lambda note: page(f"VOTE411 (League of Women Voters) voter guide, candidates’ answers: {note}", "https://www.vote411.org/ballot?lwv-ballot-widget-raceid=25687753", READ27)  # noqa: E731
cand("MI-GOV", "MI-GOV:campbell", "Douglas Campbell", "G", "Retired registered professional engineer and substitute high-school teacher; takes no corporate PAC contributions.",
     ("edu-06", -2, V411_MIGOV("Campbell would eliminate Michigan’s charter school system"), "Eliminate the charter system."),
     ("hea-01", 2, V411_MIGOV("Campbell wants a not-for-profit national health system"), "We need to create a not-for-profit National Health System."),
     ("ene-01", 2, V411_MIGOV("Campbell would cover every flat roof and parking lot with solar panels"), "Every flat roof and parking lot should be covered with photovoltaic collectors"),
     ("ene-05", 1, V411_MIGOV("Campbell would encourage electric vehicles"), "Electric vehicles should be encouraged at every opportunity."),
     ("ene-04", 1, V411_MIGOV("Campbell would close the Line 5 pipeline to protect the Great Lakes"), "Line 5 needs to be closed before we poison the entire Great Lakes."),
     ("sta-10", -2, V411_MIGOV("Campbell calls incentives for private job creation corporate welfare"), "Every time the government tries encouraging job creation in the private sector, it always ends up as corporate welfare"))

# Tennessee governor in VOTE411, read Oct. 27: of the independents with no site or
# statement, Dave Seeman and Dean Brewer answered; Murphy, Smithson, L. Webb Taylor and
# Scoggin left every question blank.
V411_TNGOV = lambda note: page(f"VOTE411 (League of Women Voters) voter guide, candidates’ answers: {note}", "https://www.vote411.org/ballot?lwv-ballot-widget-raceid=72646085", READ27)  # noqa: E731
more("TN-GOV", "TN-GOV:seeman",
     ("soc-02", 1, V411_TNGOV("Seeman would enact statewide nondiscrimination protections"), "enact statewide nondiscrimination protections in employment, housing, and public accommodations"),
     ("soc-03", 1, V411_TNGOV("Seeman would keep government out of personal medical decisions"), "keep government out of personal medical decisions"),
     ("gov-06", 1, V411_TNGOV("Seeman wants automatic registration and no-excuse absentee voting"), "protect the vote with automatic registration and no-excuse absentee ballots"),
     ("hea-03", 2, V411_TNGOV("Seeman would expand Medicaid"), "I'll close the coverage gap through Medicaid expansion"),
     ("edu-06", -2, V411_TNGOV("Seeman would repeal Tennessee’s private-school voucher program"), "repeal the private-school voucher program"),
     ("sta-02", 2, V411_TNGOV("Seeman would fund public schools through an endowment fed by taxes on extreme wealth"), "fund public schools through the Future Families Fund a permanent endowment fed by two taxes on extreme wealth"),
     ("eco-01", 1, V411_TNGOV("Seeman would tax extreme wealth to fund schools"), None),
     ("sta-03", 2, V411_TNGOV("Seeman would raise the minimum wage to $19 over four years"), "raise the minimum wage from the $7.25 federal floor to a $19 living wage over four years"),
     ("eco-02", 1, V411_TNGOV("Seeman would end the state grocery tax"), "I will end the 4% state grocery tax giving about $400 back to every Tennessee family per year"),
     ("hea-02", 1, V411_TNGOV("Seeman would lower drug prices through state bulk buying"), "bring down prescription prices by buying in bulk for seven million Tennesseans"),
     ("hou-04", 1, V411_TNGOV("Seeman would cut red tape on building homes"), "cut the red tape on building homes"),
     ("hou-01", 1, V411_TNGOV("Seeman would fund community land trusts for permanent affordable housing"), "making affordable housing permanent through state funded community land trusts"),
     ("edu-04", 1, V411_TNGOV("Seeman would pay retention stipends to teachers at high-need schools"), "pay $5,000 retention stipends at the highest-need schools"),
     ("sta-09", 2, V411_TNGOV("Seeman would put a community health center in every county"), "I will put a community health center in each county"),
     bio="Mechanical engineer; co-founder of the design firm Ovyl and founder of Squarish, a public benefit firm.",
     officialSite="https://davefortn.com/")
more("TN-GOV", "TN-GOV:brewer",
     ("sta-01", 1, V411_TNGOV("Brewer would dedicate more money to infrastructure"), "Infrastructure- dedicate more money and expand."),
     ("edu-06", -1, V411_TNGOV("Brewer says state money should stay with public schools"), "State money should stay with public schools."),
     ("edu-04", 1, V411_TNGOV("Brewer would give teachers more money"), "Strive to give teachers more money to attract quality teachers"))

V411 = lambda race_id: lambda note: page(f"VOTE411 (League of Women Voters) voter guide, candidates’ answers: {note}", f"https://www.vote411.org/ballot?lwv-ballot-widget-raceid={race_id}", READ27)  # noqa: E731
V411_COGOV = V411(3697674)
cand("CO-GOV", "CO-GOV:hamilton", "Stephen Hamilton", "American Constitution", "Cañon City small-business owner; his running mate is James Tribert.",
     ("hea-08", 1, V411_COGOV("Hamilton would protect people with pre-existing conditions"), "I believe in access to high-quality, affordable coverage through competition, transparency, and protecting people with pre-existing conditions."),
     ("hea-04", 1, V411_COGOV("Hamilton backs direct primary care and health savings accounts"), "support for direct primary care and Health Savings Accounts so families can actually afford care"),
     ("soc-01", 1, V411_COGOV("Hamilton would protect free speech for everybody"), "protecting free speech for everybody"),
     ("imm-07", 1, V411_COGOV("Hamilton would work with federal authorities against violent criminals"), "I support working with federal authorities to get violent criminals and real public safety threats off our streets"),
     ("imm-01", 1, V411_COGOV("Hamilton wants a secure border"), "We need a secure border and a legal immigration system that actually works"),
     ("ene-10", 1, V411_COGOV("Hamilton would push for energy that keeps bills down"), "push for affordable, reliable energy that keeps bills down"),
     ("edu-03", 1, V411_COGOV("Hamilton would expand vo-tech, apprenticeships and trade schools"), "I'm for expanding vo-tech, apprenticeships, trade schools, and community colleges."),
     ("sta-07", 1, V411_COGOV("Hamilton would expand technical schools and community colleges"), None),
     ("eco-07", 1, V411_COGOV("Hamilton would cut wasteful spending"), "cut wasteful spending to ease tax pressure"),
     ("sta-08", 1, V411_COGOV("Hamilton would train and support local law enforcement"), "properly train and support local law enforcement"))

# Oklahoma governor in VOTE411 (read Oct. 27). Jerry Griffin lists governorgriffin2027.com,
# which didn't load, so his link stays as it was.
V411_OKGOV = lambda note: page(f"VOTE411 (League of Women Voters) voter guide, candidates’ answers: {note}", "https://www.vote411.org/ballot?lwv-ballot-widget-raceid=72638034", READ27)  # noqa: E731
more("OK-GOV", "OK-GOV:griffin",
     ("eco-07", 1, V411_OKGOV("Griffin would have state agencies cut waste and duplication"), "State agencies should regularly review spending and eliminate waste and duplication."),
     ("sta-09", 1, V411_OKGOV("Griffin wants dependable rural access to hospitals, doctors and mental health care"), "Rural communities need dependable access to hospitals, doctors, emergency care, and mental-health services."),
     ("sta-01", 1, V411_OKGOV("Griffin would maintain roads and water systems"), "We must also maintain roads, water systems, and public safety."))

# Dean Abrams's VOTE411 answers (League of Women Voters of Florida, read Oct. 27; quotes
# checked against the page text).
V411_FLGOV = V411(27129037)
more("FL-GOV", "FL-GOV:abrams",
     ("ene-04", 1, V411_FLGOV("Abrams would enforce runoff rules with real inspections and penalties"), "Enforce existing runoff rules with real inspections and penalties, and speed up septic-to-sewer conversion near springs."),
     ("sta-05", 1, V411_FLGOV("Abrams would protect dunes, mangroves and seagrass as storm defenses"), "Protect beach access, dunes, mangroves and seagrass, our first storm defense."),
     ("hea-02", 1, V411_FLGOV("Abrams would pool state drug purchasing and import cheaper drugs"), "pool state drug purchasing, and push to import from other safe countries"),
     ("hea-07", 1, V411_FLGOV("Abrams would seek a reinsurance waiver to lower marketplace premiums"), "Pursue a federal reinsurance waiver to lower marketplace premiums for everyone."),
     ("edu-04", 1, V411_FLGOV("Abrams would set minimum teacher pay by county cost of living"), "Set minimum pay by county, based on local cost of living, so teachers can afford to live where they teach."),
     ("edu-06", 1, V411_FLGOV("Abrams supports vouchers with income limits restored"), "I support vouchers, but restore income limits so public dollars go first to families who need them."),
     ("edu-10", 1, V411_FLGOV("Abrams wants every graduate to understand the Constitution"), "Every graduate should understand the Constitution and the Federalist and Anti-Federalist debates that shaped it."))

write("data/research/candidates.json",
      [{"id": rid, "partial": True, **RACE_FIELDS.get(rid, {}), "candidates": cands} for rid, cands in RACES.items()],
      "Bios and positions for candidates who had none, from their campaign sites, researched Oct. 26, 2026.", updated=READ)
