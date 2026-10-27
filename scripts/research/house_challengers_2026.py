"""Researched bios and positions for House candidates outside the competitive races:
challengers in safer seats and third-party candidates, from their own campaign sites
and from newsroom voter guides in which they answered questions (States Newsroom
outlets such as the Oregon Capital Chronicle and Maryland Matters), read Oct. 26,
2026. Writes data/research/house_challengers.json.

Like candidates_2026.py, each race entry covers only some candidates (`partial`), so
it adds positions without making the race "researched". A stance goes in only where
the page states it; anything else stays "unclear". Quotes were checked against each
page's text.

    py scripts/research/house_challengers_2026.py
"""

from common import P, page, write

READ = "2026-10-26"


def site(name, url):
    return lambda note: page(f"{name} campaign site: {note}", url, READ)


def guide_answers(outlet, url):
    """A States Newsroom voter guide page with candidates' own questionnaire answers
    (a live page, dated when read)."""
    return lambda note: page(f"{outlet} voter guide, candidates’ answers: {note}", url, READ)


RACES = {}


def cand(race, cid, name, party, bio, *rows, **fields):
    out = {"id": cid, "name": name, "party": party, **fields}
    if bio:
        out["bio"] = bio
    if rows:
        out["positions"] = P(*rows)
    RACES.setdefault(race, []).append(out)


# Arizona ---------------------------------------------------------------------------
AZ_MIRROR = lambda d: guide_answers("Arizona Mirror", f"https://azmirror.com/voter-guides/contests/congressional-district-{d}/")  # noqa: E731
ALPONTE = site("Monica Alponte", "https://monicaalponteaz.com/")
cand("AZ-H-01", "AZ-H-01:alponte", "Monica Alponte", "L", None,
     ("def-07", 2, AZ_MIRROR(1)("Alponte is committed to non-intervention and peace"), "I am committed to a policy of non-intervention and peace."),
     ("def-10", 2, ALPONTE("Alponte would stop sending tax dollars into foreign wars"), "No more sending American taxpayer dollars into endless foreign wars."),
     ("gov-11", 2, ALPONTE("Alponte would overturn Citizens United"), "Overturn Citizens United"),
     ("gov-13", -2, ALPONTE("Alponte would overturn Citizens United"), None),
     ("eco-07", 2, AZ_MIRROR(1)("Alponte would control spending and abolish the IRS and the Fed"), None),
     ("imm-01", 1, ALPONTE("Alponte lists a secure border among her priorities"), None),
     ("soc-01", 1, ALPONTE("Alponte lists free speech among her priorities"), None))
cand("AZ-H-02", "AZ-H-02:goodwin", "Curtis Goodwin", "L", None,
     ("eco-07", 1, AZ_MIRROR(2)("Goodwin calls the federal deficit a spending problem"), "Washington doesn't have a revenue problem—it has a spending problem."))
AVERSA = site("Alan Aversa", "https://aversa.vote/")
cand("AZ-H-03", "AZ-H-03:aversa", "Alan Aversa", "No Labels",
     "Physics and programming teacher, now a substitute teacher at charter schools.",
     ("soc-04", 2, AVERSA("Aversa wants abortion ended and the right to life protected"), "so that child-killing ends and the right to life is protected for all"),
     ("soc-03", -2, AVERSA("Aversa opposes abortion"), None),
     ("edu-06", 1, AVERSA("Aversa says parents have a right to choose how their children are educated"), None),
     ("soc-12", -1, AVERSA("Aversa opposes promoting transgender ideas in schools"), None),
     ("def-12", -2, AVERSA("Aversa opposes U.S. funding of the wars of Israel, Ukraine and others"), "involvement and funding of genocidal wars by the State of Israel"),
     ("def-13", -2, AVERSA("Aversa opposes U.S. funding of the war in Ukraine"), None))
REDKEY = site("David Redkey", "https://www.davidredkey4congress.com/")
cand("AZ-H-03", "AZ-H-03:redkey", "David Redkey", "G",
     "Certified teacher who has lived in Arizona for nearly four decades.",
     ("soc-03", 2, REDKEY("Redkey calls reproductive rights fundamental human rights"), "I believe every woman has the absolute right to decide what happens to her own body"),
     ("soc-04", -2, REDKEY("Redkey says no lawmaker should take that choice away"), None))
JASSER = site("Zuhdi Jasser", "https://zuhdijasser.com/")
cand("AZ-H-04", "AZ-H-04:jasser", "Zuhdi Jasser", "R",
     "Primary-care physician for 26 years, Navy veteran and small-business owner; the son of immigrants.",
     ("eco-07", 2, JASSER("Jasser supports a balanced budget amendment"), "I support a Balanced Budget Amendment to the United States Constitution."),
     ("imm-01", 1, JASSER("Jasser would support more resources for border agents"), "I will support more resources for our border agents"),
     ("edu-06", 1, JASSER("Jasser supports funding students, not systems"), "That’s why I support educational freedom in education, and funding students"),
     ("def-01", 2, JASSER("Jasser says defense spending as a share of GDP is far too low"), "The current percent of GDP related to our defense forces is far below where we should be"),
     ("eco-02", 1, JASSER("Jasser would let Americans keep more of their money"), "letting Americans keep more of their hard-earned money"),
     ("agr-03", 1, JASSER("Jasser would bring manufacturing home"), "We must bring manufacturing home"))
BENOIT = site("Tisha Benoit", "https://tishabenoit.com/")
cand("AZ-H-04", "AZ-H-04:benoit", "Tisha Benoit", "No Labels", None,
     ("eco-07", 1, BENOIT("Benoit would put both spending cuts and new revenue on the table"), "I believe we’re going to have to put both spending cuts and additional revenue on the table."))
cand("AZ-H-06", "AZ-H-06:swing", "Gary Swing", "G", None,
     ("def-01", -2, AZ_MIRROR(6)("Swing would cut the military budget by 90%"), "Reduce the military budget by 90%."),
     ("def-08", -2, AZ_MIRROR(6)("Swing would close all foreign military bases"), "Close all foreign military bases."),
     ("def-05", -2, AZ_MIRROR(6)("Swing would end all foreign military aid"), "End all foreign military aid."),
     ("def-12", -2, AZ_MIRROR(6)("Swing would end all foreign military aid"), None),
     ("def-13", -2, AZ_MIRROR(6)("Swing would end all foreign military aid"), None),
     ("def-11", -2, AZ_MIRROR(6)("Swing says Israel has committed genocide in Gaza"), "Israel has committed genocide against Gaza."),
     ("imm-08", -2, AZ_MIRROR(6)("Swing would abolish ICE"), "Abolish ICE."),
     ("imm-01", -2, AZ_MIRROR(6)("Swing opposes a border wall"), "No border wall."),
     ("ene-01", 2, AZ_MIRROR(6)("Swing would move from fossil fuels and nuclear power to renewables"), "Transition away from fossil fuels and nuclear energy to renewable energy sources."),
     ("ene-02", -2, AZ_MIRROR(6)("Swing would move away from nuclear power"), None),
     ("ene-03", -2, AZ_MIRROR(6)("Swing would move away from fossil fuels"), None),
     ("ene-06", 1, AZ_MIRROR(6)("Swing would tax pollution"), None),
     ("hea-01", 2, AZ_MIRROR(6)("Swing supports Medicare for All"), "Medicare for all."),
     ("edu-05", 2, AZ_MIRROR(6)("Swing would forgive student loan debt"), "Forgive student loan debt and subsidize higher education."),
     ("soc-03", 2, AZ_MIRROR(6)("Swing would secure abortion rights in federal law"), "Pass federal legislation to secure abortion rights."),
     ("soc-04", -2, AZ_MIRROR(6)("Swing would secure abortion rights in federal law"), None),
     ("gov-08", 2, AZ_MIRROR(6)("Swing would abolish the Senate and the Electoral College"), "Abolish the US Senate and the Electoral College."),
     ("gov-10", 2, AZ_MIRROR(6)("Swing supports a national initiative and referendum process"), None),
     ("gov-11", 1, AZ_MIRROR(6)("Swing supports public campaign financing and spending limits"), None))
BUTIEREZ = site("Daniel Butierez", "https://butierezforcongress.com/")
cand("AZ-H-07", "AZ-H-07:butierez", "Daniel Butierez", "R", None,
     ("imm-01", 2, BUTIEREZ("Butierez would give the Border Patrol the resources it needs"), "Secure the Southern Border and fight to give U.S. Border Patrol the resources they need to do their job."),
     ("eco-08", 1, BUTIEREZ("Butierez would cut taxes and simplify the tax code for small businesses"), "Fight to cut taxes and make the tax code simpler for small businesses."),
     ("eco-12", -1, BUTIEREZ("Butierez wants a flatter tax code and to eliminate the IRS"), None))
GREENE_PLACENTIA = site("Bernadette Greene-Placentia", "https://www.bgp4az.com/")
cand("AZ-H-08", "AZ-H-08:greene-placentia", "Bernadette Greene-Placentia", "D",
     "Former long-haul trucker who ran her own trucking business.",
     ("def-03", 2, GREENE_PLACENTIA("Greene-Placentia would fully fund the VA and expand mental health care for veterans"), "Fully fund the VA, reduce intake delays, expand mental-health care"),
     ("hea-08", 2, GREENE_PLACENTIA("Greene-Placentia would protect coverage for pre-existing conditions"), "Protect pre-existing condition coverage"),
     ("imm-01", 1, GREENE_PLACENTIA("Greene-Placentia would secure the border humanely"), "Secure the border without sacrificing humanity"))

# Colorado: Colorado Newsline's guide summarizes each candidate's stances, quoting them
CO_NEWSLINE = lambda d: (lambda note: page(f"Colorado Newsline voter guide: {note}", f"https://coloradonewsline.com/voter-guides/contests/2026-general-u-s-house-{d}-district/", READ))  # noqa: E731
KIROS = site("Melat Kiros", "https://www.kirosforco.com/")
cand("CO-H-01", "CO-H-01:kiros", "Melat Kiros", "D", "Rejects all corporate PAC money.",
     ("hea-01", 2, KIROS("Kiros would pass Medicare for All"), "It's time we pass Medicare for All."),
     ("hea-03", 2, KIROS("Kiros would pass Medicare for All"), None),
     ("soc-07", 2, KIROS("Kiros stands for universal child care"), "I'll always stand for Medicare for All, Housing First, Universal Childcare, and an Arms Embargo."),
     ("def-12", -2, KIROS("Kiros supports an arms embargo on Israel"), None),
     ("def-11", -2, CO_NEWSLINE("1st")("Kiros accuses Israel of genocide in Gaza"), None),
     ("def-07", 2, CO_NEWSLINE("1st")("Kiros would end wars and lead with diplomacy"), "lead with diplomacy instead"),
     ("imm-08", -2, CO_NEWSLINE("1st")("Kiros supports abolishing ICE"), None),
     ("imm-02", 2, CO_NEWSLINE("1st")("Kiros supports pathways to citizenship"), None),
     ("eco-01", 2, CO_NEWSLINE("1st")("Kiros backs an ultra-millionaire tax and higher top income and corporate rates"), None),
     ("eco-12", 2, CO_NEWSLINE("1st")("Kiros backs higher top income tax rates"), None),
     ("ene-01", 1, CO_NEWSLINE("1st")("Kiros supports the Green New Deal"), None),
     ("gov-11", 1, KIROS("Kiros rejects corporate PAC money"), "rejecting all corporate PAC money"))
cand("CO-H-01", "CO-H-01:blau", "Shimon Blau", "I",
     "Physician and son of immigrants (his father survived the Holocaust), running as an independent.",
     ("hea-01", 1, CO_NEWSLINE("1st")("Blau now supports universal health care"), None),
     ("imm-03", 1, CO_NEWSLINE("1st")("Blau wants a faster legal immigration system alongside border security"), "a faster, more efficient legal immigration system"),
     ("imm-01", 1, CO_NEWSLINE("1st")("Blau pairs border security with immigration reform"), None),
     ("imm-08", -1, CO_NEWSLINE("1st")("Blau opposes ICE’s presence in Colorado"), "very much against ICE being here in Colorado"),
     ("def-15", -1, CO_NEWSLINE("1st")("Blau opposes the war in Iran"), None),
     ("gov-06", 1, CO_NEWSLINE("1st")("Blau supports Colorado’s universal mail ballots"), "I fully support maintaining our current universal mail-in ballot framework"))
cand("CO-H-01", "CO-H-01:peterson", "Christy Peterson", "R", None,
     ("imm-08", 1, CO_NEWSLINE("1st")("Peterson supports ICE"), "I support ICE."),
     ("eco-07", 1, CO_NEWSLINE("1st")("Peterson calls government programs bloat"), "All these government programs are just causing government bloat."),
     ("eco-02", 1, CO_NEWSLINE("1st")("Peterson’s platform calls for low taxes"), None),
     ("def-11", 1, CO_NEWSLINE("1st")("Peterson’s platform promises to protect Israel"), None))
cand("CO-H-02", "CO-H-02:dennison", "Kelley Dennison", "R", None,
     ("imm-08", 1, CO_NEWSLINE("2nd")("Dennison supports detaining and deporting people who broke immigration law"), "There must still be detention and deportation of people who violated our sovereignty"),
     ("imm-03", 1, CO_NEWSLINE("2nd")("Dennison supports legal immigration"), None),
     ("eco-07", 1, CO_NEWSLINE("2nd")("Dennison blames reckless federal spending for rising costs"), "Washington's reckless spending"))
BROWN_CO = site("Clifton Brown", "https://www.ruhero.com/")
cand("CO-H-03", "CO-H-03:brown", "Clifton Brown", "I", None,
     ("gov-02", 2, BROWN_CO("Brown would end stock trading by officials"), "End stock trading, book deals, and all moonlighting by federal judges and elected officials."),
     ("gov-09", 1, BROWN_CO("Brown would pass anti-corruption laws"), None),
     ("def-01", -2, BROWN_CO("Brown would cut military spending and close foreign bases"), "Cut military spending, End all foreign wars, Close all foreign military bases."),
     ("def-08", -2, BROWN_CO("Brown would close all foreign military bases"), None),
     ("gov-05", 2, BROWN_CO("Brown would create a national ID to vote"), "Create national ID to vote or donate money, end mail-in voting."),
     ("gov-06", -2, BROWN_CO("Brown would end mail-in voting"), None),
     ("eco-07", 2, BROWN_CO("Brown would pass a balanced budget amendment"), None),
     ("eco-13", 1, BROWN_CO("Brown would promote a 32-hour workweek"), None),
     ("hea-01", 2, BROWN_CO("Brown would make health care a constitutional right"), "making healthcare a constitutionally protected right"),
     ("soc-08", 1, BROWN_CO("Brown would establish a right to privacy"), None),
     ("soc-05", 1, BROWN_CO("Brown would end the drug war"), None))
WITTA = site("Samir Ezzeldin Witta", "https://www.wittaforcongress.com/")
cand("CO-H-06", "CO-H-06:witta", "Samir Ezzeldin Witta", "I",
     "Has worked in cancer research, refugee education and nonprofit leadership.",
     ("gov-02", 2, WITTA("Witta would ban congressional stock trading"), "A real ban on congressional stock trading"),
     ("hou-06", 1, WITTA("Witta would cap rent and HOA fees"), "Cap rent and HOA fees, and hold management companies accountable"))
cand("CO-H-06", "CO-H-06:clark", "Jason Clark", "R", None,
     ("eco-10", -1, CO_NEWSLINE("6th")("Clark opposes Trump’s tariffs"), None),
     ("imm-01", 1, CO_NEWSLINE("6th")("Clark wants secure borders and a legal immigration process"), None),
     ("def-15", -1, CO_NEWSLINE("6th")("Clark opposes the war in Iran"), None))
cand("CO-H-07", "CO-H-07:bennett", "Tim Bennett", "R", "Army veteran of 32 years.",
     ("imm-01", 1, CO_NEWSLINE("7th")("Bennett would secure the borders"), None),
     ("imm-05", 1, CO_NEWSLINE("7th")("Bennett would hold employers accountable for exploiting unauthorized workers"), None),
     ("eco-07", 1, CO_NEWSLINE("7th")("Bennett would stop reckless federal spending"), None),
     ("def-10", 1, CO_NEWSLINE("7th")("Bennett would stop sending American dollars overseas"), None))
KRZECZKOWSKI = site("Joe Krzeczkowski", "https://votejoek.com/")
cand("CO-H-07", "CO-H-07:krzeczkowski", "Joe Krzeczkowski", "I", "Engineer with a technology background.",
     ("eco-01", 2, KRZECZKOWSKI("Krzeczkowski would balance the budget by taxing the elite"), "balancing our budget by taxing the elite"),
     ("gov-11", 2, KRZECZKOWSKI("Krzeczkowski would eliminate corporate election interference"), "Eliminate corporate election interference"),
     ("eco-09", 1, KRZECZKOWSKI("Krzeczkowski would enhance worker protections"), "Enhance worker rights and protections from corporate greed"),
     ("ene-01", 1, KRZECZKOWSKI("Krzeczkowski would fund clean energy"), "Fund clean energy independence"))
SALLIS = site("Dan Sallis", "https://dankilo.com/")
cand("CO-H-07", "CO-H-07:sallis", "Dan Sallis", "L", None,
     ("eco-07", 2, SALLIS("Sallis supports a balanced budget amendment"), "Support for balanced-budget amendments, opposition to unauthorized spending"),
     ("edu-06", 2, SALLIS("Sallis supports school choice for every family"), "School choice for every family."),
     ("soc-05", 1, SALLIS("Sallis would end the war on drugs"), "End the war on drugs."),
     ("cri-08", 1, SALLIS("Sallis would treat drug use as a health matter"), "Treat substance issues as health matters, not crimes."),
     ("eco-02", 2, SALLIS("Sallis would cut federal taxes across the board"), None),
     ("eco-01", -2, SALLIS("Sallis opposes all tax increases"), "Oppose all tax increases."),
     ("hea-04", 1, SALLIS("Sallis would let insurance be sold across state lines"), None))

# Pennsylvania ----------------------------------------------------------------------
PA_STAR = lambda d: guide_answers("Pennsylvania Capital-Star", f"https://penncapital-star.com/voter-guides/contests/2026-general-u-s-house-district-{d}/")  # noqa: E731
RABB = site("Chris Rabb", "https://www.chrisrabb.com/")
cand("PA-H-03", "PA-H-03:rabb", "Chris Rabb", "D",
     "Pennsylvania state representative from Philadelphia; a progressive who twice won without the city party’s backing.",
     ("eco-03", 1, RABB("Rabb supports a living wage for all"), "Universal basic income and a living wage for all will help tackle the affordability crisis"),
     ("ene-07", 2, RABB("Rabb would create free high-speed public transit"), "free high-speed public transit"),
     ("ene-01", 2, RABB("Rabb wants a transition to 100% renewable energy"), "A Just Transition to 100% Renewable Energy"),
     ("cri-07", 2, RABB("Rabb would reduce violence by investing in housing, education, jobs and mental health care"), "Real safety comes from strong communities, not over-policing or over-prosecuting."),
     ("cri-01", -1, RABB("Rabb opposes over-policing"), None),
     ("imm-08", -1, RABB("Rabb says ICE terrorizes communities"), None),
     ("hea-01", 1, RABB("Rabb would guarantee access to health care"), "guarantee access to healthcare"),
     ("eco-09", 1, RABB("Rabb would strengthen workers’ rights"), "strengthen workers’ rights"))
STUSKI = site("Aurora Stuski", "https://aurora4pa.com/")
cand("PA-H-04", "PA-H-04:stuski", "Aurora Stuski", "R", None,
     ("eco-07", 1, STUSKI("Stuski would fight inflationary spending"), "Fight inflationary spending"),
     ("cri-01", 1, STUSKI("Stuski would back law enforcement"), "Back law enforcement, prosecute violent crime"),
     ("imm-01", 1, STUSKI("Stuski calls for a secure border"), "Secure Border, Secure Pennsylvania"),
     ("gov-12", 1, STUSKI("Stuski believes in transparency in government"), "I believe in transparency and accountability in government."))
cand("PA-H-06", "PA-H-06:young", "Marty Young", "R",
     "West Point graduate and Army chaplain, now a National Guard lieutenant colonel; spent 25 years turning around struggling companies.",
     ("hea-09", 1, PA_STAR(6)("Young would use TRICARE to guarantee preventive, prenatal and mental health care for children and young adults"), "to guarantee preventive care, mental health, prenatal care, delivery, and a baby’s first year"),
     ("hou-05", 2, PA_STAR(6)("Young proposes 0% 15-year loans for families buying a median-priced first home"), "qualifying families buying a starter or modest family home at or below the local median should get a 0% interest, 15-year loan"))
cand("PA-H-02", "PA-H-02:arriaga", "Jessica Arriaga", "R", "Philadelphia native who works in health care.")
cand("PA-H-03", "PA-H-03:mahoney", "Dennis Mahoney", "I", "Founder of AOI Solutions, a consulting firm; earlier worked for anti-hunger and disaster relief nonprofits.")
cand("PA-H-05", "PA-H-05:manganaro", "Nicholas Manganaro", "R", "Former Wall Street bond trader, portfolio manager and risk manager.")
cand("PA-H-17", "PA-H-17:guy", "Tony Guy", "R", "Beaver County sheriff, elected in 2015; formerly with the Pennsylvania State Police.")
WALLACE = site("Rachel Wallace", "https://www.wallaceforcongress.com/")
cand("PA-H-09", "PA-H-09:wallace", "Rachel Wallace", "D",
     "Pottsville native and the daughter of a pastor and a nurse; her family has lived in Berks and Schuylkill counties for 10 generations.",
     ("def-15", -2, WALLACE("Wallace would vote to end the war in Iran"), "I would start by voting to end the war in Iran."),
     ("eco-10", -1, WALLACE("Wallace would vote against blanket tariffs but use tariffs carefully"), "I’ll also vote against blanket tariffs"))
MANNION = site("Nancy Mannion", "https://www.nancymannion.com/")
cand("PA-H-11", "PA-H-11:mannion", "Nancy Mannion", "D",
     "Registered nurse for more than 40 years and former health care executive.",
     ("eco-03", 2, MANNION("Mannion would fight to raise the federal minimum wage"), "She’ll fight to raise the federal minimum wage"),
     ("eco-10", -1, MANNION("Mannion would get rid of the Trump tariffs"), "getting rid of the Trump tariffs will help bring down the cost of groceries"),
     ("hea-01", 1, MANNION("Mannion supports affordable health care for all"), "She supports affordable healthcare for all"),
     ("hou-01", 1, MANNION("Mannion would build more affordable housing"), "building more affordable housing"),
     ("edu-01", 1, MANNION("Mannion would invest in education from preschool through college"), "investing in education from preschool all the way through college"),
     ("soc-03", 1, MANNION("Mannion says reproductive decisions belong to patients"), "She believes reproductive decisions should be made only between the patient"))
HAYES = site("James Hayes", "https://jameshayesforpa.com/")
cand("PA-H-12", "PA-H-12:hayes", "James Hayes", "R",
     "Pittsburgh business and manufacturing executive, the son of a steelworker.",
     ("edu-06", 1, HAYES("Hayes supports expanding school choice"), "I support expanding school choice so families can find the best fit for their children."),
     ("def-11", 1, HAYES("Hayes would stand by allies including Israel"), "I also believe in standing by our allies, including Israel"),
     ("ene-03", 1, HAYES("Hayes supports an all-of-the-above energy strategy"), "I support an all-of-the-above energy strategy"),
     ("ene-01", 1, HAYES("Hayes supports an all-of-the-above energy strategy"), None),
     ("eco-07", 1, HAYES("Hayes would rein in wasteful spending and balance the books"), "It’s time to rein in wasteful government spending."),
     ("cri-07", 1, HAYES("Hayes would invest in crime prevention"), "investing in crime prevention"),
     ("cri-04", 1, HAYES("Hayes would hold repeat violent offenders accountable"), "making sure repeat violent offenders are held accountable"))
FARNHAM = site("Beth Farnham", "https://www.bethfarnhamforcongress.com/")
cand("PA-H-13", "PA-H-13:farnham", "Beth Farnham", "D", None,
     ("soc-03", 2, FARNHAM("Farnham would enshrine reproductive freedom in law"), "enshrine into law our Reproductive Freedom, Gun Safety, Universal Healthcare, and Immigration Reform"),
     ("soc-04", -2, FARNHAM("Farnham would enshrine reproductive freedom in law"), None),
     ("hea-01", 2, FARNHAM("Farnham would enshrine universal health care in law"), None))
cand("PA-H-14", "PA-H-14:bradstock", "Alan Bradstock", "D", "Desert Storm combat veteran and retired FBI agent.",
     ("hea-01", 1, site("Alan Bradstock", "https://www.bradstockforcongress.com/")("Bradstock would make health care affordable and accessible for every American"),
      "Making healthcare affordable and accessible for every American by lowering costs and ending medical debt."))
BILGER = site("Ray Bilger", "https://bilgerforcongress.com/")
cand("PA-H-15", "PA-H-15:bilger", "Ray Bilger", "D",
     "Air Force combat veteran from Centre County who served in the intelligence community and the State Department.",
     ("def-04", 2, PA_STAR(15)("Bilger would enforce the War Powers Act on the Iran war"), "enforcing the War Powers Act to rein in the war in Iran"),
     ("def-15", -1, PA_STAR(15)("Bilger would rein in the war in Iran"), None),
     ("hea-07", 1, BILGER("Bilger would protect affordable coverage, faulting the vote against extending marketplace tax credits"), "protecting affordable insurance coverage, lowering prescription drug costs, defending Medicare and Medicaid"))
cand("PA-H-16", "PA-H-16:wagner", "Justin Wagner", "D", "Veteran and engineer.",
     ("eco-09", 1, site("Justin Wagner", "https://www.justinwagnerforcongress.com/")("Wagner calls himself pro-union and pro-worker"), "Pro-Union. Pro-Worker."))

# Indiana: the Indiana Capital Chronicle's guide quotes each candidate's survey answers
IN_ICC = lambda d: guide_answers("Indiana Capital Chronicle", f"https://indianacapitalchronicle.com/voter-guides/contests/congressional-district-{d}/")  # noqa: E731
cand("IN-H-01", "IN-H-01:regnitz", "Barb Regnitz", "R", None,
     ("imm-01", 1, IN_ICC(1)("Regnitz’s platform calls for stronger border enforcement"), None),
     ("eco-07", 1, IN_ICC(1)("Regnitz would reduce federal spending and the debt"), None))
cand("IN-H-02", "IN-H-02:decio", "Jamee Decio", "D", None,
     ("eco-03", 2, IN_ICC(2)("Decio would raise the minimum wage to a living wage"), "raising the minimum wage to a living wage"),
     ("eco-10", -2, IN_ICC(2)("Decio would eliminate tariffs"), "eliminating tariffs"),
     ("eco-02", 2, IN_ICC(2)("Decio would cut middle-class taxes"), "giving the middle class a tax cut"),
     ("eco-01", 2, IN_ICC(2)("Decio would raise taxes on billionaires"), "imposing much higher taxes on billionaires who need to pay their fair share"),
     ("hea-01", 1, IN_ICC(2)("Decio says health care should be a right"), "Healthcare should be a right."),
     ("hea-03", 1, IN_ICC(2)("Decio would vote to restore Medicaid"), "I will also vote to restore Medicaid"))
HENRY_IN = site("William Henry", "https://www.williamhenry.us/")
cand("IN-H-02", "IN-H-02:henry", "William Henry", "L", None,
     ("eco-02", 2, IN_ICC(2)("Henry supports any tax reduction"), "Yes, I support any reduction in taxes in at all levels of government."),
     ("eco-01", -1, IN_ICC(2)("Henry supports any tax reduction"), None),
     ("eco-07", 2, HENRY_IN("Henry would cut federal agency budgets and staff"), "Reduce federal agency budgets and personnel"),
     ("def-08", -1, HENRY_IN("Henry would end costly overseas contingency operations"), "Reduce and end foreign conflict and costly overseas contingency operations and contracts"),
     ("def-04", 2, HENRY_IN("Henry supports “Defend the Guard” legislation, which bars deploying the Guard to undeclared wars"), 'Support "Defend the Guard" legislation'),
     ("def-03", 1, HENRY_IN("Henry would expand community health care programs for veterans"), "Expand community healthcare programs for veterans"),
     ("hou-04", 1, IN_ICC(2)("Henry would cut regulations and permitting delays that raise housing costs"), None))
cand("IN-H-03", "IN-H-03:thompson", "Kelly Thompson", "D", "Business owner and nonprofit founder.",
     ("hou-04", 2, IN_ICC(3)("Thompson supports removing zoning barriers to affordable housing"), None),
     ("hou-02", 2, IN_ICC(3)("Thompson would stop venture capitalists from buying homes"), None),
     ("soc-07", 1, IN_ICC(3)("Thompson argues investing in child care pays off"), None),
     ("eco-04", 2, IN_ICC(3)("Thompson would push the Justice Department to enforce antitrust laws"), None),
     ("eco-10", -1, IN_ICC(3)("Thompson says tariffs have driven up household costs"), None),
     ("def-15", -1, IN_ICC(3)("Thompson would work to end the war with Iran"), None))
COX_IN = site("Drew Cox", "https://www.drewcox.org/")
cand("IN-H-04", "IN-H-04:cox", "Drew Cox", "D",
     "Veteran raised by a farmer and a public school teacher; takes no corporate PAC money.",
     ("def-15", -2, IN_ICC(4)("Cox would vote to end the war in Iran"), "I would vote to end the war in Iran"),
     ("hou-04", 2, IN_ICC(4)("Cox would deregulate home building to make affordable housing easier to build"), "We need to deregulate the home building industry to make it easier for affordable housing to be built"),
     ("hou-02", 2, IN_ICC(4)("Cox would stop corporations from buying up single-family homes"), "prevent corporations like BlackRock from buying up single family homes"),
     ("def-07", 1, IN_ICC(4)("Cox would restore diplomacy in foreign relations"), "restores diplomacy and basic decency to our foreign relations"),
     ("gov-11", 1, COX_IN("Cox refuses corporate PAC donations"), "refusing to accept any corporate PAC donations"))
cand("IN-H-06", "IN-H-06:wirth", "Cinde Wirth", "D",
     "Seventh-generation Hoosier who taught high school biology and environmental science; a scientist and small-business owner.",
     ("hou-02", 1, IN_ICC(6)("Wirth says investors buying up homes and raising rents must stop"), "This is exploitative and needs to stop."),
     ("soc-07", 2, IN_ICC(6)("Wirth supports federal investment in universal child care"), "universal, educational childcare programs that working families need"))
cand("IN-H-07", "IN-H-07:mcauley", "Patrick McAuley", "R", None,
     ("edu-03", 1, IN_ICC(7)("McAuley would prioritize trades and apprenticeships"), None))
ALLEN_IN = site("Mary Allen", "https://www.maryallenforcongress.com/")
cand("IN-H-08", "IN-H-08:allen", "Mary Allen", "D",
     "Evansville at-large city councilor, small-business owner and Army Reserve veteran.",
     ("hea-01", 2, ALLEN_IN("Allen calls health care a human right"), "Healthcare is a human right."),
     ("hea-03", 1, IN_ICC(8)("Allen would vote to reverse the Medicaid cuts"), "I would vote to reverse those cuts"),
     ("soc-07", 2, IN_ICC(8)("Allen supports universal child care, capped at 7% of income"), "we should provide for universal childcare and early learning"),
     ("eco-09", 2, IN_ICC(8)("Allen would strengthen unions"), "We should strengthen unions and raise the minimum wage"),
     ("eco-03", 2, IN_ICC(8)("Allen would raise the minimum wage"), None),
     ("hou-01", 2, IN_ICC(8)("Allen would invest in affordable housing and fully fund federal housing programs"), "We should invest in building affordable housing for people at all income levels and fully fund federal housing programs."),
     ("def-15", -2, IN_ICC(8)("Allen would end the war in Iran"), "We should end the war in Iran"),
     ("ene-01", 1, IN_ICC(8)("Allen would reinvest in clean energy"), "re-invest in clean energy"),
     ("eco-04", 2, IN_ICC(8)("Allen would break up corporate consolidation"), "We should break up corporate consolidation"),
     ("gov-04", 1, IN_ICC(8)("Allen wants to end partisan gerrymandering"), "I strongly believe we need to end partisan gerrymandering"))
cand("IN-H-09", "IN-H-09:meyer", "Brad Meyer", "D", None,
     ("hea-01", 2, IN_ICC(9)("Meyer supports Medicare for All"), "Medicare for all. Healthcare should be available and affordable for everyone."),
     ("hea-03", 2, IN_ICC(9)("Meyer supports Medicare for All"), None),
     ("eco-03", 1, IN_ICC(9)("Meyer supports a meaningful minimum wage"), "I support a meaningful minimum wage"),
     ("eco-02", 2, IN_ICC(9)("Meyer would make the first $20,000 in wages tax-free"), "making the first $20,000 in wages tax-free"),
     ("eco-09", 1, IN_ICC(9)("Meyer would let more people qualify for overtime pay"), "changing the rules so more people qualify for overtime pay"),
     ("gov-04", 2, IN_ICC(9)("Meyer wants redistricting done by an independent, nonpartisan group"), "carried out by an independent, nonpartisan group"))
HUDSON_IN = site("Tonya Hudson", "https://tonyaforcongress.com/")
cand("IN-H-09", "IN-H-09:hudson", "Tonya Hudson", "L", "Real estate broker.",
     ("eco-07", 2, HUDSON_IN("Hudson calls for a balanced budget"), "A balanced budget is required!"),
     ("eco-12", -2, HUDSON_IN("Hudson would abolish the IRS for a sales tax like the FairTax"), "Abolish the IRS and move forward to a system similar to a FAIR tax/sales tax"),
     ("def-07", 1, IN_ICC(9)("Hudson would vote to end the wars"), "If elected to Congress, I would vote to end the wars."))

# Utah: Utah News Dispatch's guide prints each candidate's own answers
UT_UND = lambda d: guide_answers("Utah News Dispatch", f"https://utahnewsdispatch.com/voter-guides/contests/2026-general-u-s-house-district-{d}/")  # noqa: E731
cand("UT-H-01", "UT-H-01:mcadams", "Ben McAdams", "D",
     "Former congressman (2019–2021) and Salt Lake County mayor; a seventh-generation Utahn.",
     ("eco-10", -2, UT_UND(1)("McAdams would vote to end the tariffs"), "Tariffs are a tax families pay at the grocery checkout, and I'll vote to end them."),
     ("ene-01", 1, UT_UND(1)("McAdams would add solar, batteries and geothermal and cut dependence on fossil fuels over time"), "Over time, we have to reduce our dependence on fossil fuels and do our part to stop climate change"))
cand("UT-H-01", "UT-H-01:owen", "Riley Owen", "R", None,
     ("hou-02", 2, UT_UND(1)("Owen would get big investors out of single-family homes"), "Congress needs to get big investors out of single family homes"),
     ("hou-04", 2, UT_UND(1)("Owen would tie federal funds to local zoning reform"), "conditionalize federal funds to localities implementing common sense zoning reforms"),
     ("eco-11", 1, UT_UND(1)("Owen would expand the business tax credit for paid maternity leave"), "expanding the business tax credit to those offering paid maternity leave"),
     ("ene-02", 1, UT_UND(1)("Owen would invest in small modular reactors"), None),
     ("ene-10", 1, UT_UND(1)("Owen supports an all-of-the-above approach to lower energy costs"), None))
cand("UT-H-02", "UT-H-02:crosby", "Peter Crosby", "D", None,
     ("eco-10", -1, UT_UND(2)("Crosby says the tariff regime raised the cost of everything"), None),
     ("ene-01", 1, UT_UND(2)("Crosby calls solar a common-sense choice for Utah"), "making solar a common sense choice"))
cand("UT-H-02", "UT-H-02:moesinger", "Robert Moesinger", "I", "Running on electoral reform and a multiparty democracy.",
     ("hou-04", 1, UT_UND(2)("Moesinger would cut regulatory barriers and encourage zoning that lets communities grow"), "We need to make it easier to build more housing through decreased regulatory burden"),
     ("ene-02", 1, UT_UND(2)("Moesinger backs nuclear power as reliable, low-carbon electricity"), "Nuclear power can provide reliable, low-carbon electricity"))
cand("UT-H-02", "UT-H-02:bowen", "Carlton Bowen", "Independent American", "Air Force veteran.",
     ("def-07", 1, UT_UND(2)("Bowen opposes forever wars"), "I'm opposed to the forever wars, where we keep spending our strength warring in foreign lands that aren't attacking us or our allies."),
     ("eco-07", 1, UT_UND(2)("Bowen says the national debt is killing us"), "our national debt is killing us"),
     ("ene-03", 1, UT_UND(2)("Bowen supports an all-of-the-above policy including natural gas and coal"), None),
     ("ene-09", -1, UT_UND(2)("Bowen opposes federal energy subsidies"), "I don't support federal subsidies or policies designed to pick winners and losers."))
cand("UT-H-03", "UT-H-03:easley", "Cassie Easley", "Constitution", None,
     ("eco-12", -2, UT_UND(3)("Easley would repeal the 16th Amendment, ending the income tax"), "repeal the 16th Amendment"),
     ("eco-01", -1, UT_UND(3)("Easley would repeal the income tax"), None))
cand("UT-H-03", "UT-H-03:scott", "Ayden Scott", "I", None,
     ("hou-05", 1, UT_UND(3)("Scott proposes a flexible-rate program for first-time home buyers"), "a flexible interest rate program for our first time home buyers with strict criteria"),
     ("ene-02", 1, UT_UND(3)("Scott wants nuclear energy to make initial strides in Utah"), None))
cand("UT-H-03", "UT-H-03:stoddard", "Michael Stoddard", "L", "CPA who has spent his career auditing government spending.",
     ("gov-12", 1, site("Michael Stoddard", "https://2amike4congress.org/")("Stoddard would publish the government’s full balance sheet"), "Publish the full balance sheet"))
cand("UT-H-04", "UT-H-04:larsen", "Jonny Larsen", "D", "Marine combat veteran.",
     ("def-15", -2, UT_UND(4)("Larsen calls the Iran war illegal and opposes it"), "As a United States Marine combat veteran, I do not support this war."),
     ("ene-01", 2, UT_UND(4)("Larsen would incentivize solar and invest in battery technology"), "incentivizing solar and investing federal resources in better battery technology"),
     ("ene-09", 1, UT_UND(4)("Larsen would put federal money into better batteries"), None))
cand("UT-H-04", "UT-H-04:burt", "Steven Burt", "I",
     "South Jordan lawyer for nearly 20 years, the last 10 as an in-house attorney and executive in the solar industry.",
     ("def-15", -2, UT_UND(4)("Burt calls starting the Iran war disastrous"), "Nothing has impacted affordability more than the disastrous decision to start a war in Iran"),
     ("hou-04", 1, UT_UND(4)("Burt would encourage local zoning reform"), "encourages local governments to reform zoning laws"),
     ("hou-01", 1, UT_UND(4)("Burt supports the low-income housing tax credit and public housing"), "developing public housing"),
     ("eco-10", -1, UT_UND(4)("Burt would rein in the Trump tariffs"), "rein in the Trump tariffs"),
     ("eco-07", 2, UT_UND(4)("Burt would end deficit spending and balance the budget"), "we must end deficit spending and balance the budget"),
     ("ene-01", 1, UT_UND(4)("Burt would prioritize renewables within an all-of-the-above strategy"), "we should prioritize renewables"),
     ("ene-02", 1, UT_UND(4)("Burt would also prioritize nuclear power"), None))
cand("UT-H-04", "UT-H-04:wright", "Taylor Wright", "L", None,
     ("hou-04", 2, UT_UND(4)("Wright would stop zoning, permitting and mandates from restricting housing supply"), "Government should stop artificially restricting it through unnecessary zoning, permitting delays, mandates, and regulations"),
     ("ene-09", -1, UT_UND(4)("Wright would end energy subsidies"), None))

# Nebraska: the Nebraska Examiner's guide (Dan Hartong, America First, did not answer it
# and has no site, so he has nothing yet)
NE_EXAMINER = lambda d: guide_answers("Nebraska Examiner", f"https://nebraskaexaminer.com/voter-guides/contests/2026-general-u-s-house-district-{d}/")  # noqa: E731
cand("NE-H-01", "NE-H-01:sandman", "Nik Sandman", "L",
     "Retired farmer and rural mail carrier from Lincoln, 78; calls himself basically conservative and wants parity prices for farm goods.",
     ("def-04", 2, NE_EXAMINER(1)("Sandman supports the Constitution’s requirement that Congress declare war"), "I support the Constitution and its requirement that Congress declare war."),
     ("def-07", 1, NE_EXAMINER(1)("Sandman says the country should seek peace"), "We should seek peace and pursue it."))
cand("NE-H-02", "NE-H-02:foreman", "Eric Foreman", "L", "Omaha property manager and maintenance worker, 46.",
     ("eco-12", -2, NE_EXAMINER(2)("Foreman would work to eliminate the federal income tax"), "I would work to eliminate the federal income tax."),
     ("eco-07", 2, NE_EXAMINER(2)("Foreman would cut federal spending so ending the income tax does not add to the debt"), "At the same time we must cut federal spending so that the loss of income tax revenue does not simply add to the debt."),
     ("eco-02", 1, site("Eric Foreman", "https://foremantakebackourhouse.com/")("Foreman supports lower taxes for working families"), "lower taxes for working families"),
     ("ene-09", -1, NE_EXAMINER(2)("Foreman opposes subsidies and mandates for ethanol"), "I also oppose subsidies and mandates that prop up the ethanol industry."),
     ("imm-01", 1, NE_EXAMINER(2)("Foreman would secure the border first with walls and technology"), "Secure the borders first, with walls, technology and sheriffs’ oversight."),
     ("imm-05", 1, NE_EXAMINER(2)("Foreman would crack down on employers who exploit undocumented workers"), "Crack down on employers who exploit undocumented workers for cheap labor."),
     ("imm-07", 1, NE_EXAMINER(2)("Foreman would deport real criminals rather than make blanket sweeps"), "Deport real criminals."),
     ("gov-05", 1, NE_EXAMINER(2)("Foreman supports voter ID, cleaner voter rolls and paper ballots"), "Requiring voter identification, regular cleaning of voter rolls, paper ballots with auditable trails"),
     ("soc-05", 2, NE_EXAMINER(2)("Foreman supports legal marijuana, medical or recreational"), "Whether for medical relief or recreational purposes, what a person does with their own body is their own decision"),
     ("def-07", 1, NE_EXAMINER(2)("Foreman wants a foreign policy of nonintervention"), "The United States should pursue a foreign policy of peace through strength, free trade and nonintervention."),
     ("def-08", -1, NE_EXAMINER(2)("Foreman says the U.S. should not police the world"), "Not to police the world or fund endless foreign conflicts."),
     ("def-10", 1, NE_EXAMINER(2)("Foreman would end open-ended aid packages"), "should end open-ended aid packages that lack clear objectives and exit strategies"),
     ("def-12", -1, NE_EXAMINER(2)("Foreman would reduce support for Israel"), "With Israel we should reduce our support"),
     ("def-13", -1, NE_EXAMINER(2)("Foreman opposes continued massive funding for Ukraine without a path to peace"), "In Ukraine and Russia, continued massive U.S. funding without a realistic path to negotiated peace serves neither American taxpayers nor long-term stability."))
cand("NE-H-03", "NE-H-03:stille", "Becky Stille", "D",
     "Works in the biofuels industry in South Sioux City, 56; spent 20 years in agriculture and calls herself a moderate Democrat.",
     ("eco-03", 2, NE_EXAMINER(3)("Stille would raise the $7.25 federal minimum wage"), "We need to raise the federal minimum wage — $7.25/hour is absurd, period."),
     ("eco-01", 1, NE_EXAMINER(3)("Stille would remove permanent tax breaks for corporations and the wealthy"), "remove permanent tax breaks for corporations and the wealthy and give those breaks to the working people"),
     ("eco-02", 1, NE_EXAMINER(3)("Stille would make tax breaks permanent for working families"), "Tax breaks should be made permanent for working families, not corporations and the wealthy."),
     ("imm-08", -1, NE_EXAMINER(3)("Stille opposes the administration’s deportation approach"), "I do not support the deportation approach of this administration."),
     ("def-04", 2, NE_EXAMINER(3)("Stille says Congress should decide how the country responds to conflicts"), "First and foremost, Congress should decide how our country responds to international conflicts."),
     ("soc-03", 2, site("Becky Stille", "https://www.beckystille2026.com/")("Stille would restore women’s reproductive freedoms"), "restore women’s reproductive freedoms"),
     ("hea-06", 1, site("Becky Stille", "https://www.beckystille2026.com/")("Stille would bring mental health care to rural communities"), "bring health care & mental health care to rural communities"))
cand("NE-H-03", "NE-H-03:cohen", "Mark Cohen", "I",
     "Semiretired lawyer and karate instructor from Lemoyne, 68; former Air Force judge advocate and special assistant U.S. attorney, with a master of laws in agricultural law. Says he won’t caucus with either party.",
     ("eco-10", -2, NE_EXAMINER(3)("Cohen calls unilateral tariffs a tax on farmers"), "Unilateral tariffs are a tax on the people who grow that food, and the retaliation hits rural areas the hardest."),
     ("eco-01", 2, site("Mark Cohen", "https://www.markfornebraska.org/")("Cohen would make billionaires pay their fair share to balance the budget"), "fight for policies that make the billionaires pay their fair share so we can balance our budget once and for all"),
     ("eco-12", 1, NE_EXAMINER(3)("Cohen wants a tax structure like Eisenhower’s, with high top rates"), "I want a tax structure closer to the one that had bipartisan support under Eisenhower."),
     ("eco-04", 2, NE_EXAMINER(3)("Cohen would enforce and strengthen antitrust laws"), "I’ll work to enforce and strengthen our antitrust laws to protect Nebraska’s farmers, ranchers and small businesses."),
     ("soc-08", 1, NE_EXAMINER(3)("Cohen would defend privacy against data tracking"), "I will defend our privacy against a system that tracks everything we do"),
     ("imm-02", 2, NE_EXAMINER(3)("Cohen supports a path to citizenship"), "The solution is a real path to citizenship for those willing to work hard and learn English."),
     ("imm-08", -2, NE_EXAMINER(3)("Cohen would cut ICE funding to pre-2025 levels"), "I would reduce ICE funding to pre-2025 levels"),
     ("imm-01", 1, NE_EXAMINER(3)("Cohen backs a bipartisan border bill like the 2024 Lankford deal"), "push for a bipartisan border control bill like the one Republican Sen. James Lankford negotiated in 2024"),
     ("def-02", 2, NE_EXAMINER(3)("Cohen backs NATO and Pacific alliances"), "weakening proven alliances is foolish"),
     ("def-04", 2, NE_EXAMINER(3)("Cohen would defend Congress’s war powers under any president"), "I would defend Congress’ power to declare war"),
     ("gov-13", -2, NE_EXAMINER(3)("Cohen supports an amendment saying money isn’t speech and corporations aren’t people"), "Money is not speech. Corporations are not people. I support a constitutional amendment to make that clear."),
     ("gov-11", 2, NE_EXAMINER(3)("Cohen wants big money out of politics"), None),
     ("soc-05", 2, NE_EXAMINER(3)("Cohen supports legal, regulated marijuana for adults"), "I support legalizing and regulating marijuana for adults."))
cand("NE-H-03", "NE-H-03:budke", "Macey Budke", "Working People",
     "Behavioral health practice manager from North Platte, 36; wrote 365 letters to elected officials in one year before deciding to run.",
     ("hea-03", 1, NE_EXAMINER(3)("Budke supports stronger Medicaid coverage protections"), "I would also support stronger Medicaid coverage protections, lower prescription costs and simpler administration"),
     ("imm-08", -1, NE_EXAMINER(3)("Budke opposes President Trump’s broad deportation approach"), "I do not support President Trump’s broad deportation approach."),
     ("imm-04", 1, NE_EXAMINER(3)("Budke would add immigration judges and case staff"), "I would support more immigration judges and case staff, faster processing of asylum and visa applications"),
     ("imm-09", 1, NE_EXAMINER(3)("Budke wants legal work pathways that fit farm labor needs"), "stronger legal workforce pathways that reflect agricultural and rural labor needs"),
     ("imm-05", 1, NE_EXAMINER(3)("Budke supports enforcement against employers who exploit undocumented workers"), "firm enforcement against trafficking and employers who knowingly exploit undocumented workers"),
     ("imm-07", 1, NE_EXAMINER(3)("Budke would prioritize removing people who pose a public safety threat"), "People who pose a genuine public safety threat should be prioritized for removal through due process"),
     ("def-13", 1, NE_EXAMINER(3)("Budke supports helping Ukraine defend itself"), "I support helping Ukraine defend itself, pursuing a negotiated end to the conflict and establishing a path toward NATO membership."),
     ("def-12", 0, NE_EXAMINER(3)("Budke opposes unconditional aid to Israel while backing its right to defend itself"), "Israel has a right to exist and defend itself, but that does not justify unconditional aid"),
     ("def-04", 2, NE_EXAMINER(3)("Budke says Congress must reclaim its war powers"), "Congress must reclaim its constitutional authority over war"),
     ("gov-06", 1, NE_EXAMINER(3)("Budke would keep early and mail voting"), "maintaining meaningful early and mail voting options"))
cand("NE-H-03", "NE-H-03:else", "David Else", "Legal Marijuana Now",
     "Lifetime farmer from Overton: a dairy farmer for 22 years, then grain and cattle. Ran in 2022 to protect the Affordable Care Act.",
     ("hea-08", 1, NE_EXAMINER(3)("Else wants to keep the Affordable Care Act and its coverage of preexisting conditions"), "This was before Obamacare, which we need to keep."),
     ("eco-10", -1, NE_EXAMINER(3)("Else opposes trade wars and says consumers pay the tariffs"), "I don't like trade wars with other countries."),
     ("imm-02", 1, NE_EXAMINER(3)("Else supports work visas leading to citizenship"), "I would like to make it easier for immigrants to get a work visa, then a pathway to U.S. citizenship if they are not criminals"),
     ("def-08", -1, NE_EXAMINER(3)("Else says the U.S. should stop policing the world"), "Internationally I think we need to stop policing the whole world."),
     ("def-14", 1, NE_EXAMINER(3)("Else would stand up to Putin over Ukraine"), "But we need to stand up to Putin for what he has done to Ukraine."),
     ("def-15", -1, NE_EXAMINER(3)("Else wants Congress to stop the war"), "they need to stop him on most things. Like this war and his trade wars"))

# Oregon: the Oregon Capital Chronicle's guide (its contest addresses differ by district).
# Loran Ayles (R, 3rd) and the Pacific Greens Justin Filip (4th) and Andrea Townsend
# (5th) answered nothing and have no sites.
OR_OCC = lambda slug: guide_answers("Oregon Capital Chronicle", f"https://oregoncapitalchronicle.com/voter-guides/contests/{slug}/")  # noqa: E731
KAHL = site("Barbara Kahl", "https://drkahlforcongress.com/")
cand("OR-H-01", "OR-H-01:kahl", "Barbara Kahl", "R",
     "Veterinarian with a century of family roots in northwest Oregon; worked 20 years in business, including finance at Intel, and served as a Navy Volunteer Ombudsman while her husband was in the Navy.",
     ("hou-04", 1, KAHL("Kahl would streamline permitting to expand housing supply"), "I support expanding housing supply at every price point, streamlining permitting so projects don't die in bureaucratic delay"),
     ("hou-05", 1, KAHL("Kahl would use federal incentives to help first-time buyers"), "leveraging federal incentives to reduce financing barriers for first-time buyers and working families"),
     ("edu-06", 1, KAHL("Kahl supports school choice, with funding that follows the student"), "funding that follows the student"),
     ("edu-03", 1, KAHL("Kahl supports vocational pathways"), None),
     ("eco-06", 1, KAHL("Kahl supports infrastructure investment"), "Small business support, infrastructure investment, and jobs that keep families in Oregon."))
BECK = OR_OCC("2026-general-us-house-district-2")
cand("OR-H-02", "OR-H-02:beck", "Chris Beck", "D",
     "Former Oregon legislator and legislative staffer; spent six years on rural policy at the U.S. Department of Agriculture.",
     ("def-15", -2, BECK("Beck would use Congress’s war powers to end the Iran war"), "Use Congress’s constitutional war powers to end the Iran War"),
     ("def-04", 2, BECK("Beck says Congress has the authority to end the war and should use it"), "Congress has the constitutional authority to end this war, and it should use it."),
     ("eco-10", -2, BECK("Beck would repeal most tariffs"), "repeal most tariffs, especially on our allies"),
     ("eco-01", 1, BECK("Beck wants the wealthiest to pay their fair share"), "with the wealthiest paying their fair share"),
     ("hou-05", 2, BECK("Beck would offer government-backed financing for first-time buyers"), "offer government-backed financing for first time home buyers"),
     ("hou-01", 1, BECK("Beck wants the federal government to help finance affordable housing again"), "I want to reform federal housing policy so the federal government once again helps finance affordable housing and provides rental housing vouchers."),
     ("hea-07", 2, BECK("Beck would restore the Medicaid and ACA subsidy funding cut by H.R. 1"), "Restore funding that HR 1 stripped from Medicaid, ACA subsidies, and food assistance."),
     ("hea-03", 2, BECK("Beck would create an optional public plan modeled on the Oregon Health Plan"), "create an optional public plan modeled after the Oregon Health Plan, available to anyone who wants it"),
     ("imm-08", -2, BECK("Beck would repeal the recent expansion of ICE funding"), "I would repeal recently expanded funding for ICE."),
     ("imm-01", 1, BECK("Beck backs a bill like the 2024 Senate border deal, with more border resources"), "I would support bipartisan legislation modeled after the bipartisan Senate border agreement from 2024, which included more resources for border security"),
     ("imm-04", 1, BECK("Beck supports more funding for immigration judges"), "more funding for judges to provide due process"),
     ("imm-02", 1, BECK("Beck would add a path to citizenship for Dreamers"), "I’d add a path to citizenship for “Dreamers”"),
     ("imm-09", 1, BECK("Beck would fix the agricultural visa system"), "I’d also fix our agricultural visa system so farms and food processors in places such as Hermiston and Ontario have a stable, legal workforce."),
     ("ene-01", 2, BECK("Beck supports strong incentives for renewable energy"), "I support strong incentives for renewable energy"),
     ("ene-08", 1, BECK("Beck would restore Forest Service wildfire prevention funding"), "I’d start by restoring the 40% cut to Forest Service wildfire prevention funding"),
     ("gov-06", 2, BECK("Beck would defend vote by mail against efforts to roll it back"), "I’ll defend it against efforts in Washington to roll it back"))
DESPAIN = OR_OCC("2026-general-us-house-district-4")
cand("OR-H-04", "OR-H-04:despain", "Monique DeSpain", "R",
     "Retired Air Force colonel (30 years, including as a judge advocate) and Oregon lawyer for 27 years; raised her sons in Eugene as a single mother.",
     ("eco-07", 1, DESPAIN("DeSpain would fight tax-and-spend policies"), "I will fight the reckless tax and spend policies that drive inflation"),
     ("hou-04", 2, DESPAIN("DeSpain would remove federal permitting costs and land use limits on new homes"), "I will push to remove the federal permitting costs, red tape and outdated land use restrictions that stifle new construction"),
     ("cri-01", 1, DESPAIN("DeSpain would give law enforcement more resources"), "giving law enforcement the resources to do its job"),
     ("gov-12", 1, DESPAIN("DeSpain would post every vote and expose wasteful spending"), "I will post every vote and my reasoning, and I will use my legal training to expose wasteful spending"),
     ("imm-07", 1, DESPAIN("DeSpain wants enforcement to put dangerous criminals first"), "Congress should make sure enforcement puts dangerous criminals, gang members and cartel operatives first"),
     ("imm-01", 2, DESPAIN("DeSpain supports barriers, sensors, drones and a fully staffed Border Patrol"), "I support an all-of-the-above approach: physical barriers, sensors, drones, strong cybersecurity and a fully staffed Border Patrol."),
     ("hea-04", 1, DESPAIN("DeSpain wants more private choices, such as buying coverage across state lines"), "Families need more choices and real competition, including the ability to buy coverage across state lines."),
     ("ene-10", 1, DESPAIN("DeSpain opposes forced energy transitions that raise prices"), "I will protect access to reliable, affordable options and oppose forced transitions that raise what families pay for gas and power."),
     ("gov-10", 1, DESPAIN("DeSpain praises Oregon’s citizen initiative process"), "Oregon's citizen initiative process is one of our state's greatest strengths."))
ADAIR = site("Patti Adair", "https://www.pattiforcongress.com/")
cand("OR-H-05", "OR-H-05:adair", "Patti Adair", "R",
     "Deschutes County commissioner since 2018 and fourth-generation Oregonian; lives on a horse ranch in Sisters.",
     ("gov-02", 1, ADAIR("Adair would ban insider trading by members of Congress"), "Ban insider trading by Members of Congress."),
     ("eco-02", 1, ADAIR("Adair would make no tax on tips, overtime and Social Security permanent"), "Make no tax on tips, overtime, and Social Security permanent, and increase the limits."),
     ("cri-01", 1, ADAIR("Adair fully supports law enforcement"), "Fully support law enforcement to keep our communities safe."),
     ("hou-04", 1, ADAIR("Adair testified for Oregon’s accessory dwelling unit bill"), "Testified for SB 391 in support of Accessory Dwelling Units in coordination with SB 762 which will increase affordable housing."))
RUSS = OR_OCC("2026-general-u-s-house-district-6")
cand("OR-H-06", "OR-H-06:russ", "David Russ", "R", "Small business owner for more than 45 years.",
     ("hea-01", -2, RUSS("Russ rejects the idea that health care is a human right"), "There are many people who have been convinced by the Democratic Socialists that “healthcare is a human right.” That is absolutely not true."),
     ("hea-07", -2, RUSS("Russ opposes making people pay for others’ health care"), "Forcing people to pay for someone else’s health care is taking away that person’s “human rights”"),
     ("hou-01", -1, RUSS("Russ says Congress has no authority to act directly on housing costs"), "directly acting on the costs for gas, groceries and housing is absolutely NOT something Congress is authorized to do under the Constitution"),
     ("eco-07", 1, RUSS("Russ would cut fraud, waste and abuse and programs that fund nonprofits"), "I will be focusing on reducing and eliminating fraud, waste and abuse"),
     ("edu-07", 1, site("David Russ", "https://www.russisforus.com/")("Russ would end federal control of local schools"), "End Federal Control of our Local Schools"))

# Idaho: the Idaho Capital Sun's guide (Brendan Gomez, Constitution, 1st, answered nothing
# and has no site)
ID_SUN = lambda d: guide_answers("Idaho Capital Sun", f"https://idahocapitalsun.com/voter-guides/contests/2026-general-{d}-congressional-district/")  # noqa: E731
PETERSON = site("Kaylee Peterson", "https://kayleeforcongress.com/")
cand("ID-H-01", "ID-H-01:peterson", "Kaylee Peterson", "D", "Organizer from Eagle, 36; calls herself a labor-first, union-first candidate.",
     ("gov-02", 2, PETERSON("Peterson would ban stock trades by members of Congress, their families and associates"), "Ban trades for members of Congress, their family, and associates."),
     ("gov-11", 2, PETERSON("Peterson would overturn Citizens United"), "Working to ban corporate political dominance at the state level in Idaho until we can achieve it at the federal level."),
     ("gov-13", -2, ID_SUN("1st")("Peterson lists overturning Citizens United among her top issues"), "Overturning Citizens United."),
     ("gov-01", 1, ID_SUN("1st")("Peterson lists term limits among her top issues"), "Term limits."),
     ("eco-02", 1, PETERSON("Peterson would cut tax rates on the middle class"), "Cut tax rates and regulations on middle-class Americans and local Idaho businesses."),
     ("eco-09", 2, PETERSON("Peterson would protect collective bargaining and repeal right-to-work laws"), "I am a labor-first, union-first candidate always."),
     ("eco-01", 1, ID_SUN("1st")("Peterson would lift the Social Security income cap"), "Lifting the Social Security income cap is not only fair"),
     ("eco-12", 1, ID_SUN("1st")("Peterson wants high earners to pay Social Security tax on all earnings"), "High-earners should be paying Social Security tax on all their earnings"),
     ("hou-01", 1, PETERSON("Peterson would use the tax code to support affordable housing and child care"), "Reform the tax code to support affordable housing, childcare, public transportation, and infrastructure."),
     ("soc-07", 1, PETERSON("Peterson would use the tax code to support child care"), None),
     ("hea-01", 2, ID_SUN("1st")("Peterson supports a single-payer system"), "Taking health insurance companies out of the equation and moving to a single payer system is the best and cheapest way forward."),
     ("hea-03", 1, ID_SUN("1st")("Peterson would fight health care cuts"), "I will fight cuts that close rural hospitals, take healthcare away from working families"),
     ("imm-04", 2, ID_SUN("1st")("Peterson would drastically expand immigration judges and court attorneys"), "drastically expand the number of immigration judges and court attorneys to clear massive backlogs"),
     ("imm-01", 1, ID_SUN("1st")("Peterson would hire border agents for high-traffic entry points"), "hire professional border agents for high-traffic entry points"),
     ("imm-09", 1, ID_SUN("1st")("Peterson backs the Farm Workforce Modernization Act"), "If career politicians in Congress actually cared about fixing legal immigration, they would have passed the Farm Workforce Modernization Act years ago."),
     ("imm-08", -1, ID_SUN("1st")("Peterson calls ICE’s actions extreme government overreach"), "The extreme government overreach weaponized by ICE across America goes against every single protection we have from government intrusion."))
cand("ID-H-01", "ID-H-01:zabel", "Sarah Zabel", "I", "Retired; lives in Bayview.",
     ("imm-09", 1, ID_SUN("1st")("Zabel supports the Securing Agriculture’s Workforce Act for farm worker visas"), "I support the Securing Agriculture's Workforce Act"),
     ("imm-03", 1, ID_SUN("1st")("Zabel wants enough temporary and permanent visas to meet economic needs"), "our system provides enough temporary and permanent visas to meet our economic needs, while still protecting American workers"),
     ("eco-01", 1, ID_SUN("1st")("Zabel would raise Social Security’s taxable earnings ceiling"), "lifting the taxable earnings ceiling to cover 90% of wages"))
cand("ID-H-02", "ID-H-02:gilbreath", "Ellie Gilbreath", "D", "Mediator and attorney from Ketchum, 64.",
     ("imm-01", 1, ID_SUN("2nd")("Gilbreath wants a strong, secure border"), "We need a strong secure border."),
     ("imm-09", 1, ID_SUN("2nd")("Gilbreath wants a streamlined farm guest worker program and more farm work visas"), "expanded work visas for seasonal and year-round farm and dairy positions"),
     ("imm-02", 1, ID_SUN("2nd")("Gilbreath supports legal status for longtime farm workers"), "a clear pathway to legal status for longtime agricultural workers"),
     ("hea-07", 2, ID_SUN("2nd")("Gilbreath would restore Medicaid funding and ACA premium tax credits"), "Restore Medicaid funding, reinstate ACA premium tax credits, and treat rural healthcare access as the infrastructure problem it is."),
     ("hea-03", 1, ID_SUN("2nd")("Gilbreath would restore Medicaid funding"), None),
     ("eco-01", 1, ID_SUN("2nd")("Gilbreath objects to tax cuts for people who don’t deserve them"), "We are accelerating toward insolvency while cutting taxes for people who don't deserve them"))
cand("ID-H-02", "ID-H-02:hutchinson", "Tripp Hutchinson", "I", "Ketchum city councilman, 28.",
     ("eco-04", 2, ID_SUN("2nd")("Hutchinson would break up big agriculture monopolies"), "Break Up Big-Agriculture Monopolies."),
     ("imm-02", 2, ID_SUN("2nd")("Hutchinson wants a more robust path to citizenship"), "Congress needs to legislate a much more efficient and robust pathway to citizenship for law abiding immigrants that are already in our country."),
     ("imm-01", 1, ID_SUN("2nd")("Hutchinson wants more border personnel rather than barriers"), "our border security needs more people, not more physical barriers"),
     ("imm-08", -1, ID_SUN("2nd")("Hutchinson says ICE most likely needs to be disbanded and replaced"), "ICE most likely needs to be disbanded and replaced by a new organization"),
     ("hea-01", 2, ID_SUN("2nd")("Hutchinson supports working toward single-payer"), "working towards a public single-payer system"),
     ("eco-01", 1, ID_SUN("2nd")("Hutchinson would raise the Social Security cap"), "This one is simple: Raise The Cap."))
HOUSER = site("Emre Houser", "https://www.houserforidaho.com/")
cand("ID-H-02", "ID-H-02:houser", "Emre Houser", "I",
     "Air Force veteran and Idaho National Guard member who deployed to Iraq in 2003; small business owner in Idaho for more than 15 years.",
     ("gov-02", 2, HOUSER("Houser would bar members from trading individual stocks and bonds"), "I believe that members of Congress should not be allowed to invest in individual stocks and bonds while serving in Congress."),
     ("gov-01", 2, HOUSER("Houser supports term limits and pledges to serve no more than two terms"), "Term limits are important to reduce the influence of long-term lobbyists and special interest groups"),
     ("gov-13", -2, HOUSER("Houser would get rid of Citizens United"), "None of us can out donate a massive corporation. They should not be able to influence government."),
     ("eco-04", 2, HOUSER("Houser would break up meatpacking, dairy and media consolidation"), "We need LESS mega-corporations influence and MORE competition which benefit farmers and consumers."),
     ("eco-10", -1, HOUSER("Houser says tariffs sent buyers such as China to other suppliers"), "Tariffs causing other nations to switch their supplier countries"),
     ("hea-02", 1, HOUSER("Houser wants Medicare and Medicaid to pay the drug prices the VA negotiates"), "If the drug prices that the Veterans Administration pays for drugs were applied to Medicare and Medicaid"),
     ("def-03", 1, HOUSER("Houser would properly fund the VA"), "We must properly fund the VA so that our national heroes receive what they are due."))
JOHANSON = site("Will Johanson", "https://www.johansonforidaho.com/")
cand("ID-H-02", "ID-H-02:johanson", "Will Johanson", "L", "Engineer and veteran, raised in California’s Central Valley.",
     ("eco-07", 2, JOHANSON("Johanson would vote no on any budget that increases the debt"), "In Congress, I will vote “No” on any budget that will increase the national debt."),
     ("ene-03", 1, JOHANSON("Johanson supports drilling and fracking in the U.S."), "Protect the environment by drilling, fracking, and mining essential minerals in the USA."),
     ("agr-05", 1, JOHANSON("Johanson supports mining essential minerals in the U.S."), None),
     ("imm-01", 1, JOHANSON("Johanson would close the border"), "Immigration? Close the border."),
     ("soc-04", 0, JOHANSON("Johanson takes no side on abortion"), "Abortion? Not my axe to grind."))

# Iowa: the Iowa Capital Dispatch's guide summarizes each platform in its own words, so
# only the words it quotes from a candidate are quoted here. Rick Stewart (L, 2nd) has
# no site, and his State Fair proposals (a land tax, a universal basic income) don't
# match a question.
IA_ICD = lambda slug: lambda note: page(f"Iowa Capital Dispatch voter guide: {note}", f"https://iowacapitaldispatch.com/voter-guides/contests/{slug}/", READ)  # noqa: E731
cand("IA-H-01", "IA-H-01:bridgford", "Michael Bridgford", "I",
     "Independent financial advisor from Bettendorf, 41; formerly co-owned a small logistics business.",
     ("eco-04", 1, IA_ICD("2026-us-house-district-1-general")("Bridgford supports enforcing agriculture antitrust laws to break up seed, fertilizer and meatpacking monopolies"), None))
cand("IA-H-02", "IA-H-02:bushaw", "Dave Bushaw", "I",
     "Squash farmer in Hawkeye, 32, and folk and labor musician who has played at strikes and organized for Bernie Sanders’ 2020 campaign.",
     ("hea-01", 2, site("Dave Bushaw", "https://www.davebushaw.com/")("Bushaw supports universal public health care"), "Abolish Private Taxes & Create Universal Public Healthcare"),
     ("hea-04", -2, site("Dave Bushaw", "https://www.davebushaw.com/")("Bushaw would replace premiums, copays and deductibles with public health care"), None),
     ("eco-09", 1, IA_ICD("2026-us-house-2-general")("Bushaw has advocated for stronger workers’ rights and union protections"), None),
     ("gov-10", 1, IA_ICD("2026-us-house-2-general")("Bushaw would support national ballot initiatives"), None))
IA4 = IA_ICD("2026-us-house-district-4-general")
MCGOWAN = site("Chris McGowan", "https://mcgowanforiowa.com/")
cand("IA-H-04", "IA-H-04:mcgowan", "Chris McGowan", "R",
     "President of the Siouxland Chamber of Commerce and former chair of the Iowa Chamber Alliance; Iowa Air National Guard veteran, including as an intelligence officer.",
     ("imm-01", 2, MCGOWAN("McGowan would complete the job of securing the border"), "The first obligation of the federal government is the protection of our citizens — and that begins with a secure border."),
     ("imm-08", 1, MCGOWAN("McGowan says officials must support ICE’s arrest and removal operations"), "political officials must support the ERO mission"),
     ("soc-04", 2, MCGOWAN("McGowan would defend life from conception"), "including defending life from conception to natural death"),
     ("def-16", 1, MCGOWAN("McGowan would stand up to China"), "I’ll join the administration in putting America First and standing up to China, bringing jobs back to America, and restoring energy independence."),
     ("agr-06", 1, MCGOWAN("McGowan supports trade agreements for farm goods"), "supporting President Trump’s efforts to secure free and fair-trade agreements for the goods our farmers produce"),
     ("eco-07", 1, MCGOWAN("McGowan would eliminate wasteful spending"), "Eliminating wasteful spending"))
cand("IA-H-04", "IA-H-04:dawson", "David Dawson", "D",
     "Former Iowa House member (2013–2017) and Woodbury County prosecutor.",
     ("hea-05", 1, IA4("Dawson would invest in medical research"), "invest in medical research"),
     ("hea-06", 1, IA4("Dawson would keep mental health care close to home"), "ensure mental health services are available close to home"),
     ("hou-09", 1, IA4("Dawson would expand broadband and repair roads and bridges"), "I will work to expand broadband, repair roads and bridges, strengthen family farms, make housing more affordable, and support small businesses."),
     ("hou-08", 1, IA4("Dawson would repair roads and bridges"), None),
     ("eco-04", 1, IA4("Dawson would crack down on corporate monopolies"), "crack down on corporate monopolies that hurt farmers, small business owners, and consumers"))

# Maine: the Maine Morning Star's guide summarizes answers in its own words (no quotes)
ME_MMS = lambda note: page(f"Maine Morning Star voter guide: {note}", "https://mainemorningstar.com/voter-guides/contests/2026-general-u-s-house-district-1-2026-general-u-s-house/", READ)  # noqa: E731
cand("ME-H-01", "ME-H-01:russell", "Ronald Russell", "R",
     "Native Mainer raised on a potato farm in Fort Fairfield; veteran and business owner.",
     ("hea-01", -1, ME_MMS("Russell believes any government-run health care system will not work"), None),
     ("hea-07", -1, ME_MMS("Russell would try to move the U.S. away from the Affordable Care Act"), None),
     ("imm-01", 1, ME_MMS("Russell would curb illegal border crossings"), None),
     ("ene-09", -1, ME_MMS("Russell would immediately remove all subsidies for renewable energy"), None),
     ("eco-02", 1, ME_MMS("Russell backs extra inflation adjustments for lower and middle tax brackets"), None),
     ("eco-10", 1, ME_MMS("Russell thinks tariffs have been a good tool to get to fairer trade"), None),
     ("def-04", 1, ME_MMS("Russell believes Congress should regain its power over overseas conflicts"), None),
     ("edu-07", 1, ME_MMS("Russell would eliminate the Education Department and send its money to states and localities"), None))

# Montana: the Daily Montanan's guide and campaign sites. Nick Sheedy (L, 1st) and
# Patrick McCracken (L, 2nd) have answered nothing and post no issues.
MT2_DM = guide_answers("Daily Montanan", "https://dailymontanan.com/voter-guides/contests/2026-general-u-s-house-of-representatives-district-2-central-eastern/")
cand("MT-H-02", "MT-H-02:miller", "Brian Miller", "D", "Helena attorney; born in Cleveland in 1972 and raised in Gulf Breeze, Fla.",
     ("def-15", -2, MT2_DM("Miller would end the war in Iran"), "we need to end the war in Iran and get our military out of unnecessary conflicts throughout the world"),
     ("def-08", -1, MT2_DM("Miller would get the military out of unnecessary conflicts"), None),
     ("def-03", 2, MT2_DM("Miller would add VA staff and cut wait times"), "we need to do much more to help our veterans by increasing staffing at the VA, reducing wait times"),
     ("eco-10", -2, MT2_DM("Miller would get rid of tariffs"), "we need to get rid of tariffs"),
     ("eco-01", 1, MT2_DM("Miller wants corporations and the wealthy to pay their fair share"), "having corporations and wealthy people pay their fair share of taxes"),
     ("hea-01", 1, MT2_DM("Miller lists health care for all Americans as common ground"), "healthcare for all Americans"),
     ("hea-04", -1, MT2_DM("Miller would take the profit motive out of health care"), "We need to get the profit motive out of healthcare"),
     ("gov-11", 1, MT2_DM("Miller would get special interest money out of government"), "get as much of the money and influence that special interest groups have out of the equation"))
EISENHAUER = site("Mike Eisenhauer", "https://eisenhauerforcongress.com/issues/")
cand("MT-H-02", "MT-H-02:eisenhauer", "Michael Eisenhauer", "I",
     "Cardiologist and retired Army colonel (more than 20 years of service), from a family of teachers; his family still runs a small farm in Nebraska.",
     ("eco-10", -2, EISENHAUER("Eisenhauer calls tariffs an indirect tax on Americans"), "Tariffs will not make America rich again."),
     ("eco-02", 1, EISENHAUER("Eisenhauer supports targeted tax relief for the middle and lower classes"), "Support efforts for targeted tax relief for the middle- and lower-classes, and for small business fairness"),
     ("eco-12", 1, EISENHAUER("Eisenhauer opposes tax cuts for the very rich and large corporations"), "It is not fair to cut or reduce taxes on multi-millionaires, billionaires and large multi-national corporations"),
     ("eco-04", 2, EISENHAUER("Eisenhauer would pass antitrust laws and break up seed and fertilizer companies if needed"), "This will very likely require significant anti-trust legislation and legal enforcement, and may require a physical corporate break-up to reverse prior mergers."),
     ("agr-01", 1, EISENHAUER("Eisenhauer suggests a federal price floor for some farm products"), "The federal government may need to set a reasonable but formal ‘price floor’ for certain agricultural products"),
     ("hea-03", 1, EISENHAUER("Eisenhauer would restore the Medicaid and SNAP cuts"), "Work with a bipartisan coalition to restore cuts in Medicaid and SNAP assistance, without delay"),
     ("hea-01", -1, EISENHAUER("Eisenhauer doesn’t believe single-payer would work"), "I do not believe that a single-payer system will be workable"),
     ("hea-08", 2, EISENHAUER("Eisenhauer would keep coverage for preexisting conditions"), "Any successful effort must first protect a person’s ability to see the doctor of their choice, and must retain coverage for preexisting conditions."),
     ("hea-06", 1, EISENHAUER("Eisenhauer would restore permanent telehealth coverage for mental health"), "Fight to restore full and permanent tele-health coverage for all mental or behavioral health issues"),
     ("def-03", 1, EISENHAUER("Eisenhauer supports more VA funding for veterans’ mental health care"), "Support enhanced VA funding for Veteran’s mental health care"),
     ("hou-04", 1, EISENHAUER("Eisenhauer supports zoning changes for duplexes, triplexes and apartments"), "Zoning changes that remove barriers to the construction of duplexes, triplexes or multi-family housing in residential areas"),
     ("hou-05", 2, EISENHAUER("Eisenhauer supports significant down-payment help for first-time buyers"), "Significant down-payment assistance"),
     ("imm-07", 1, EISENHAUER("Eisenhauer supports removing immigrants convicted of serious crimes"), "It is entirely reasonable to remove illegal immigrants who have been convicted of serious crimes or violence against others"),
     ("imm-09", 1, EISENHAUER("Eisenhauer says migrant farm labor needs to be supported"), "Many agricultural sectors are dependent upon migrating workers to harvest their crops – this needs to be supported."),
     ("imm-02", 1, EISENHAUER("Eisenhauer opposes deporting Dreamers"), "I do not think it is fair to force that young adult to deport to another country for which they feel no bond"),
     ("ene-03", 1, EISENHAUER("Eisenhauer supports oil, gas and coal production in Montana"), "Promote ‘all of the above’ energy policies supporting oil/gas/coal industries and energy production in Montana"),
     ("ene-02", 2, EISENHAUER("Eisenhauer would invest federally in small modular reactors"), "Work in a bipartisan manner to federally invest into Small Modular Nuclear Reactors (SMRs), and to foster a growing nuclear power industry"),
     ("ene-01", 1, EISENHAUER("Eisenhauer’s all-of-the-above policy includes solar, wind, hydropower and geothermal"), None),
     ("def-15", -1, EISENHAUER("Eisenhauer would end the war in the Middle East while keeping shipping open"), "End the War in the Middle East"),
     ("cri-01", 1, EISENHAUER("Eisenhauer would protect and increase federal funding for police and first responders"), "I will work to protect and increase federal funding for these vital services"),
     ("edu-01", 1, EISENHAUER("Eisenhauer backs well-funded public schools and opposed closing the Education Department"), "Strong and well-funded public schools are the backbone of the American education system"))

# New Mexico: Source NM's guide prints interview answers in the candidates' words. State
# Rep. Martin Zamora (R, 3rd) declined its interview, and his site refuses scripted reads.
NM1_SOURCE = guide_answers("Source NM", "https://sourcenm.com/voter-guides/contests/u-s-congress-district-1/")
cand("NM-H-01", "NM-H-01:okpareke", "Didi Okpareke", "R",
     "Has run a compounding pharmacy in Rio Rancho for nearly 10 years; raised in California’s Bay Area by parents who immigrated from Nigeria, she moved to Albuquerque in the late 1990s.",
     ("gov-01", 2, NM1_SOURCE("Okpareke names term limits as her priority legislation"), "Term limits. I think that we should constantly have new people in Congress"),
     ("imm-01", 1, NM1_SOURCE("Okpareke counts closing the border among the administration’s positives"), "I think one of the positives is closing the border."),
     officialSite="https://www.didiforcongress.com/")

# North Carolina: campaign sites, and NC Newsline's guide where it gathers a candidate's
# past statements. Tom Bailey (L, 1st), Eugene Douglass (R, 2nd), Daniel Cavender (L,
# 3rd), Steven Swinton (L, 13th) and the Libertarians whose sites list no issues
# (Laszacs, Luffman, Abu-Ghazalah) have nothing yet; Richard Ojeda's site (D, 9th)
# refuses scripted reads.
GANORKAR = site("Max Ganorkar", "https://maxforcongress.com/")
cand("NC-H-04", "NC-H-04:ganorkar", "Max Ganorkar", "R", None,
     ("edu-06", 2, GANORKAR("Ganorkar would fund students directly through vouchers"), "I believe expanding school choice and privatizing education would create more opportunities for students"),
     ("hea-07", 1, GANORKAR("Ganorkar would give people health insurance vouchers through their tax returns"), "providing healthcare vouchers directly to citizens through the tax-filing process"),
     ("hea-04", 1, GANORKAR("Ganorkar would let people buy insurance from anywhere in the country"), "Americans should be able to purchase insurance from anywhere in the country to increase competition and lower costs."))
MEILLEUR = site("Guy Meilleur", "https://guy4nc.org/")
cand("NC-H-04", "NC-H-04:meilleur", "Guy Meilleur", "L", None,
     ("imm-01", 1, MEILLEUR("Meilleur would pass the Lankford border bill"), "respect peaceful compromise by passing the Lankford Border Bill"),
     ("eco-07", 1, MEILLEUR("Meilleur wants inspectors general so Congress can cut budgets"), "so legislators can cut budgets while retaining essential services"),
     ("hea-04", 1, MEILLEUR("Meilleur would emulate Singapore’s market-driven health care system"), "We can emulate Singapore’s market-driven health care system"),
     ("def-13", 1, MEILLEUR("Meilleur says Ukraine should be able to buy anti-missile systems"), "Tel Aviv and Kyiv deserve Iron Domes"),
     ("def-15", -1, MEILLEUR("Meilleur opposes attacking Iran and Venezuela"), "Our country will be safer when our alliances are not enabling warlords, or attacking Iran and Venezuela!"),
     ("edu-06", 1, MEILLEUR("Meilleur supports school choice"), "It’s time for North Carolinians to choose freedom, which includes school choice for maximum education opportunities"))
HUBBARD = site("Chuck Hubbard", "https://hubbardforcongress.com/")
cand("NC-H-05", "NC-H-05:hubbard", "Chuck Hubbard", "D", None,
     ("eco-03", 1, HUBBARD("Hubbard would raise the minimum wage"), "We need to raise the minimum wage."),
     ("eco-12", 1, HUBBARD("Hubbard would shift the tax base toward the rich and corporations"), "And we must shift the tax base more to rich people and wealth corporations."),
     ("eco-01", 1, HUBBARD("Hubbard would shift more of the tax burden to the rich"), None),
     ("edu-01", 1, HUBBARD("Hubbard would support public schools, teachers and school buildings"), "Congress must do everything it can to support public education, teachers, and the physical infrastructure needed"),
     ("hou-09", 1, HUBBARD("Hubbard would expand rural broadband"), "we must ensure access to high-speed broadband"),
     ("hea-03", 2, HUBBARD("Hubbard supports a government health care option"), "I believe that it is our responsibility to provide a government option"),
     ("soc-03", 2, HUBBARD("Hubbard would codify abortion rights nationally"), "Abortion is a medical procedure and should have been codified into law nationally long ago."),
     ("soc-04", -2, HUBBARD("Hubbard says government has no place in abortion decisions"), "There’s no room for the government in that conversation."),
     ("soc-12", 1, HUBBARD("Hubbard calls attacks on LGBTQ neighbors un-American"), "Attacks on minority communities and our LGBTQ neighbors are outright un-American."),
     ("gov-13", -2, HUBBARD("Hubbard would overturn Citizens United"), "We need to push to overturn Citizens United"),
     ("gov-11", 2, HUBBARD("Hubbard would reduce corporate PAC influence"), "do everything we can to reduce the influence of corporate political action committees (PACs) in our elections"),
     ("gov-02", 2, HUBBARD("Hubbard would immediately ban members of Congress from trading stocks"), "We must immediately ban Members of Congress from trading stocks."))
JEFFERSON = site("Cyril Jefferson", "https://www.cyrilforcongress.com/")
cand("NC-H-06", "NC-H-06:jefferson", "Cyril Jefferson", "D", "Former teacher and High Point mayor.",
     ("hea-06", 1, JEFFERSON("Jefferson would expand mental health care"), "Cyril will protect Medicaid and Medicare, lower drug costs, and expand mental-health care"),
     ("edu-04", 1, JEFFERSON("Jefferson would raise teacher pay"), "Cyril will raise teacher pay, expand affordable childcare, and create debt-free career pathways through apprenticeships"),
     ("soc-07", 1, JEFFERSON("Jefferson would expand affordable child care"), None),
     ("edu-03", 1, JEFFERSON("Jefferson would create apprenticeship pathways"), None),
     ("eco-06", 1, JEFFERSON("Jefferson would bring federal money home for roads, rail and broadband"), "Cyril will bring federal dollars home to modernize roads, rail, and broadband"),
     ("imm-01", 1, JEFFERSON("Jefferson supports securing the border with bipartisan measures"), "Cyril supports immigration reform and securing the border with smart, bipartisan measures"),
     ("def-01", 1, JEFFERSON("Jefferson would rebuild the military’s edge"), "rebuilding America’s military edge"))
HARDY = site("Kimberly Hardy", "https://www.kimberlyhardyforcongress.com/")
cand("NC-H-07", "NC-H-07:hardy", "Kimberly Hardy", "D", None,
     ("eco-03", 1, HARDY("Hardy supports raising the federal minimum wage"), "Raising the federal minimum wage for the first time in nearly 30 years."),
     ("eco-06", 1, HARDY("Hardy supports rail, internet and port projects"), "Support projects to improve our infrastructure, including rail and internet connectivity and port logistics."),
     ("ene-01", 1, HARDY("Hardy supports solar, wind and geothermal"), "Support homegrown energy initiatives including solar, wind, and geothermal."),
     ("hou-10", 1, HARDY("Hardy would fund coastal resilience and storm water infrastructure"), "Advocate for infrastructure funding to ensure coastal resilience"),
     ("hea-05", 1, HARDY("Hardy would roll back cuts to cancer research at NIH"), "Rollback cuts to cancer research and other vital programs at the National Institutes for Health"),
     ("edu-01", 1, HARDY("Hardy would seek capital improvement money for schools"), "Advocate for capital improvement funds to help our schools"))
WATSON = site("Colby Watson", "https://www.colbyforcongress.com/")
cand("NC-H-08", "NC-H-08:watson", "Colby Watson", "D", "Homeschooled by his parents; pledges to take no corporate or foreign lobbyist money.",
     ("gov-02", 2, WATSON("Watson would bar members of Congress from trading stocks"), "Having access to privileged information while buying and selling stock is a clear conflict of interest."),
     ("gov-11", 1, WATSON("Watson wants campaign finance reform to limit special-interest money"), "That's why we need real campaign finance reform to limit the influence of special-interest money and return power to the American people."),
     ("edu-07", 1, WATSON("Watson would keep education decisions with parents and communities"), "Keep education decisions with parents and local communities, not bureaucrats in Washington."),
     ("edu-03", 1, WATSON("Watson would expand career and technical education"), "Expand career and technical education, apprenticeships, and the skilled trades."),
     ("soc-08", 1, WATSON("Watson would ban social media companies from collecting data on children"), "Ban social media companies from collecting data on children under 18."),
     ("imm-01", 1, WATSON("Watson wants a secure border with technology and personnel"), "We need a secure border, modern technology, sufficient personnel"))
WHITEHEAD = site("Bo Whitehead", "https://whiteheadforcongressnc.carrd.co/")
cand("NC-H-08", "NC-H-08:whitehead", "Bo Whitehead", "G",
     "Warehouse supervisor in Charlotte and caregiver for his disabled wife; grew up on a small farm in Georgia.",
     ("eco-03", 1, WHITEHEAD("Whitehead would raise the minimum wage"), "Raising the minimum wage, universal healthcare, abolishing ICE, ending wars, legalizing marijuana, prison reform"),
     ("hea-01", 2, WHITEHEAD("Whitehead wants universal health care as soon as possible"), "Universal healthcare, universal childcare, and a complete overhaul of our mental health system must be implemented"),
     ("soc-07", 2, WHITEHEAD("Whitehead wants universal child care"), None),
     ("hea-06", 2, WHITEHEAD("Whitehead would overhaul the mental health system"), None),
     ("imm-08", -2, WHITEHEAD("Whitehead would abolish ICE"), None),
     ("soc-05", 1, WHITEHEAD("Whitehead would legalize marijuana"), None),
     ("def-10", 1, WHITEHEAD("Whitehead would end foreign aid"), None),
     ("def-07", 1, WHITEHEAD("Whitehead says wars must end"), "Wars and genocides must end today."))
BELL = site("Ashley Bell", "https://www.ashleybellforcongress.com/")
cand("NC-H-10", "NC-H-10:bell", "Ashley Bell", "D",
     "Physician assistant and former university professor who trained PAs; earlier a junior high and high school band director in Texas.",
     ("gov-02", 1, BELL("Bell supports banning congressional stock trading"), "Ashley supports banning congressional stock trading and ending Citizens United."),
     ("gov-13", -1, BELL("Bell supports ending Citizens United"), None),
     ("edu-01", 1, BELL("Bell wants public schools fully funded"), "Ashley wants public schools fully funded and teachers paid what they're worth."),
     ("edu-04", 1, BELL("Bell wants teachers paid what they’re worth"), None),
     ("soc-03", 1, BELL("Bell would protect reproductive rights"), "Ashley will protect reproductive rights and defend access to contraception and the vote."),
     ("hea-03", 1, BELL("Bell supports expanded Medicaid access"), "Ashley supports full ADA enforcement, expanded Medicaid access, and stronger employment protections."),
     ("imm-08", -1, BELL("Bell would abolish ICE and replace it with an accountable agency"), "Ashley wants to abolish ICE and establish an accountable agency in its place"),
     ("def-12", -2, BELL("Bell would stop funding Israel’s war in Gaza"), "Stop funding Israel's genocide on the Palestinian people."),
     ("gov-04", 1, BELL("Bell would ban partisan gerrymandering"), "Ban partisan gerrymandering."),
     ("ene-01", 2, BELL("Bell supports a Green New Deal with more clean energy"), "Green New Deal. More clean energy jobs, less pollution, and expanded public transit."),
     ("hou-03", 1, BELL("Bell wants expanded public transit"), None))
FELDMAN = site("Steve Feldman", "https://www.stevefeldmanforcongress.com/my-positions")
cand("NC-H-10", "NC-H-10:feldman", "Steve Feldman", "L",
     "Dermatologist and medical scientist trained at Duke and UNC, in North Carolina for more than 40 years.",
     ("eco-07", 2, FELDMAN("Feldman says the government must spend less and pay down the debt"), "We must spend less and pay down the debt."),
     ("eco-12", -1, FELDMAN("Feldman suggests a flat tax and sales tax with a rebate up to the poverty level"), "One simple, transparent approach would be a flat tax and sales tax"),
     ("hea-04", 1, FELDMAN("Feldman wants market forces to cut Medicare and Medicaid costs"), "We need market forces to reduce the costs of Medicare and Medicaid."),
     ("def-07", 2, FELDMAN("Feldman calls war immoral and counterproductive"), "War is immoral, counterproductive, and costly."),
     ("def-08", -1, FELDMAN("Feldman wants the military focused on defending U.S. borders"), "Our military should defend our borders, not tell others how to live"),
     ("def-12", -1, FELDMAN("Feldman would stop supporting Israel’s treatment of Palestinians"), "Stop supporting Israel's mistreatment and killing of Palestinian families"),
     ("def-11", -2, FELDMAN("Feldman calls the Israeli government’s policy morally and strategically wrong"), "I passionately believe that the Israeli government's current policy is morally and strategically wrong"))
BARRINGER = site("Paul Barringer", "https://paulbarringer.com/")
cand("NC-H-13", "NC-H-13:barringer", "Paul Barringer", "D", "Lawyer, Eagle Scout and Sunday school teacher who lives on a farm in Lee County.",
     ("imm-01", 1, BARRINGER("Barringer wants effective enforcement to stop illegal crossings"), "Border security is a basic function of government, and we need smart, effective enforcement to stop illegal crossings"),
     ("imm-03", 1, BARRINGER("Barringer would modernize legal immigration for agriculture, health care and tech"), "we need to modernize our legal immigration system to meet workforce needs—especially in agriculture, health care, and tech"),
     ("eco-07", 1, BARRINGER("Barringer wants spending restraint and a balanced budget"), "we need to get serious about spending restraint and work toward a balanced budget"),
     ("edu-07", 1, BARRINGER("Barringer wants parents to have a say in what’s taught"), "parents should have a real seat at the table when it comes to what’s being taught in the classroom"))
WOMACK = site("LaKesha Womack", "https://www.womack4nc14.com/")
cand("NC-H-14", "NC-H-14:womack", "Lakesha Womack", "D", None,
     ("hea-07", 1, WOMACK("Womack would protect and strengthen the Affordable Care Act"), "Protect and strengthen the Affordable Care Act"),
     ("eco-03", 1, WOMACK("Womack supports raising the federal minimum wage"), "Support raising the federal minimum wage"),
     ("eco-02", 1, WOMACK("Womack would advance tax policies for working and middle-class households"), "Advance tax policies that benefit working- and middle-class households"),
     ("hou-01", 1, WOMACK("Womack supports investment in affordable housing"), "Support investments in affordable housing development"),
     ("hou-06", 1, WOMACK("Womack would protect renters"), "Protect renters and first-time homebuyers"),
     ("edu-01", 1, WOMACK("Womack would increase federal investment in public schools"), "Increase federal investment in public schools and educator support"),
     ("edu-03", 1, WOMACK("Womack would expand apprenticeships and workforce training"), "Expand apprenticeship and workforce training programs"),
     ("edu-05", 1, WOMACK("Womack supports student debt relief"), "Support affordable higher education and student debt relief"))
NC11_NEWSLINE = lambda note: page(f"NC Newsline voter guide: {note}", "https://ncnewsline.com/voter-guides/contests/2026-general-u-s-house-11th-congressional-district/", READ)  # noqa: E731
cand("NC-H-11", "NC-H-11:groo", "Travis Groo", "L", "Ran for the state Senate in 2020 and the Holly Springs Town Council in 2023.",
     ("hou-04", 1, NC11_NEWSLINE("Groo backed zoning that allows townhomes, duplexes, triplexes and tiny homes (2023)"), None),
     ("imm-03", 1, NC11_NEWSLINE("Groo backed immigration reform letting anyone immigrate (2020)"), None),
     ("hea-04", 1, NC11_NEWSLINE("Groo said government shouldn’t be involved in health care (2020)"), None))
CODIGA = site("Jack Codiga", "https://www.codigaforcongress.com/")
cand("NC-H-12", "NC-H-12:codiga", "Jack Codiga", "R", None,
     ("hou-04", 2, CODIGA("Codiga would limit zoning to infrastructure and pollution concerns"), "Zoning should be limited to genuine infrastructure or pollution concerns."),
     ("hea-03", -2, CODIGA("Codiga would phase out welfare programs, including government health care and Social Security"), "we must reform and phase out all welfare programs, including Social Security (the godfather of all Ponzi schemes), government healthcare, and government-backed mortgages"),
     ("hea-01", -2, CODIGA("Codiga would phase out government health care"), None),
     ("gov-05", 2, CODIGA("Codiga would mandate voter ID and paper ballots in federal elections"), "America’s federal election system must mandate voter ID and paper ballots at the federal level to ensure honest elections."),
     ("gov-08", -1, CODIGA("Codiga would keep the Electoral College"), "while keeping the Electoral College for President"),
     ("soc-08", 1, CODIGA("Codiga would let users opt out of sharing personal data"), "Users should have the ability to opt out of sharing their personal information to access digital services."))

# Rhode Island: the Rhode Island Current's guide (Pedro DeSouza, I, 1st, didn't answer
# and his site lists no issues) and campaign sites
RI1_CURRENT = guide_answers("Rhode Island Current", "https://rhodeislandcurrent.com/voter-guides/contests/2026-general-1st-congressional-district/")
cand("RI-H-01", "RI-H-01:keenan", "Kellie Keenan", "R", "Background in health care operations, program management and community health.",
     ("imm-01", 2, RI1_CURRENT("Keenan strongly supports enforcing immigration laws and securing the border"), "I strongly support enforcing our immigration laws and securing the border."),
     ("imm-08", 1, RI1_CURRENT("Keenan would fund immigration officers’ staffing, technology and training, with oversight"), "I would support funding that gives federal immigration officers the staffing, technology, training, and resources necessary to do their jobs effectively"),
     ("gov-02", 1, RI1_CURRENT("Keenan would bar members from actively trading individual stocks"), "I support prohibiting members from actively trading individual stocks while serving in Congress"))
cand("RI-H-02", "RI-H-02:mellor", "Vic Mellor", "R",
     "Marine Corps veteran and entrepreneur who ran a business for three decades; a founding member of the Global Allied Health Association.")

# South Carolina: campaign sites (the SC Daily Gazette's guide has no questionnaire). Dayna
# Alane Smith (Workers, 2nd) has no site, and Jessica Ethridge's (L, 4th) lists no issues.
KHALIFA = site("Zyon Khalifa", "https://www.khalifaforcongress.com/")
cand("SC-H-02", "SC-H-02:khalifa", "Zyon Khalifa", "D", None,
     ("eco-03", 1, KHALIFA("Khalifa would raise the minimum wage"), "Implement a minimum wage increase so that full-time workers can achieve financial stability"),
     ("eco-11", 2, KHALIFA("Khalifa supports mandatory paid maternity leave"), "Supporting working families through enacting a mandatory paid maternity leave and affordable childcare."),
     ("soc-07", 1, KHALIFA("Khalifa supports affordable child care"), None),
     ("edu-01", 1, KHALIFA("Khalifa would increase funding for public schools"), "Prioritize increased funding for public schools to improve facilities, classroom resources, and educational programs"),
     ("hea-06", 1, KHALIFA("Khalifa would expand mental health services"), "Expand access to mental health services"),
     ("hou-08", 1, KHALIFA("Khalifa would repair roads and bridges"), "Commit to repairing and upgrading roads, bridges, and essential infrastructure"),
     ("ene-01", 1, KHALIFA("Khalifa supports solar, wind and other renewables"), "Advocating for policies that promote solar, wind, and other renewable energy sources to reduce carbon emissions."),
     ("ene-06", 1, KHALIFA("Khalifa supports a net-zero emissions target"), "Supporting legislation that aims for net-zero greenhouse gas emissions by a specified target year."),
     ("ene-04", 1, KHALIFA("Khalifa supports stricter air quality standards"), "Promoting regulations that reduce air pollution and protect public health."),
     ("soc-03", 1, KHALIFA("Khalifa would protect access to reproductive health care"), "Protecting access to reproductive healthcare"))
LEHMACHER = site("Eunice Lehmacher", "https://www.euniceforsc.com/")
cand("SC-H-03", "SC-H-03:lehmacher", "Eunice Lehmacher", "D",
     "Licensed professional counselor in Oconee and Pickens counties since 2002, including at Oconee Memorial Hospital and Clemson University.",
     ("eco-10", -1, LEHMACHER("Lehmacher calls the tariffs illegal and costly"), "the imposition of the illegal tariffs that have cost the average household well over a thousand dollars"),
     ("imm-08", -1, LEHMACHER("Lehmacher condemns masked, untrained ICE agents"), "the reckless brutality of masked, untrained ICE agents"),
     ("hea-07", 1, LEHMACHER("Lehmacher objects to the lapse in health insurance funding"), "There’s simply no excuse for the lapse in health insurance funding for millions of us"),
     ("def-02", 1, LEHMACHER("Lehmacher objects to the sabotage of U.S. alliances"), "the sabotage of our closest alliances and partnerships"))
CORRIEA = site("Brian Corriea", "https://www.brianforliberty.com/")
cand("SC-H-03", "SC-H-03:corriea", "Brian Corriea", "L", "Navy veteran from Williamston.",
     ("eco-10", -2, CORRIEA("Corriea opposes protective tariffs"), "Brian maintains that you cannot support a “pro-market” position while endorsing protective tariffs or state interference in trade"),
     ("hea-04", 1, CORRIEA("Corriea wants market-oriented health care reforms"), "He advocates for market-oriented reforms that expand choice, reduce regulatory barriers, and let competition lower costs."),
     ("hea-03", -1, CORRIEA("Corriea opposes expanding government in health care"), "Brian argues against expanding government in healthcare"),
     ("eco-07", 1, CORRIEA("Corriea criticizes wasteful spending and rising debt"), "he consistently criticizes wasteful spending, unsustainable budget practices, and policies that increase debt"),
     ("gov-12", 1, CORRIEA("Corriea supports open records and clear budgeting"), "Brian supports open, accountable government with accessible records, clear budgeting, and robust accountability for public dollars."))
cand("SC-H-04", "SC-H-04:mcclain", "Courtney McClain", "D",
     "Civil rights advocate who has lobbied the South Carolina Legislature; a former Congressional Black Caucus Institute fellow in Toyota’s government affairs office.")
CLIMER = site("Wes Climer", "https://wesclimer.com/")
cand("SC-H-05", "SC-H-05:climer", "Wes Climer", "R", "South Carolina state senator.",
     ("edu-06", 2, CLIMER("Climer expanded school choice in the state Senate"), "Expanded school choice so every child can access the best education regardless of ZIP code"),
     ("gov-12", 2, CLIMER("Climer led the fight to ban secret spending in the state budget"), "Led the fight to ban secret spending in the state budget so taxpayers know where every dollar goes"),
     ("eco-02", 1, CLIMER("Climer passed state tax cuts for families and small businesses"), "Passed over $2 billion in tax cuts for South Carolina families and small businesses"))
DITTMER = site("Mallory Dittmer", "https://www.dittmerforcongress.com/")
cand("SC-H-05", "SC-H-05:dittmer", "Mallory Dittmer", "D", None,
     ("imm-02", 1, DITTMER("Dittmer backs the Farm Workforce Modernization Act’s path to legal status"), "Support the Farm Workforce Modernization Act, a bipartisan bill which creates a pathway to legal status and eventual citizenship for undocumented agricultural workers"),
     ("imm-09", 1, DITTMER("Dittmer backs the Farm Workforce Modernization Act"), None),
     ("hou-09", 1, DITTMER("Dittmer would invest in rural broadband"), "Invest in rural broadband as a catalyst for economic growth"),
     ("soc-07", 1, DITTMER("Dittmer would lower child care costs"), "Lower child care costs and improve access so parents can work and kids can thrive"),
     ("hou-01", 1, DITTMER("Dittmer would expand affordable housing with government incentives"), "Lower rent and home prices by expanding affordable housing supply through government incentives and tax credits"),
     ("eco-03", 1, DITTMER("Dittmer would raise the $7.25 minimum wage"), "Raise the $7.25/hour minimum wage"),
     ("eco-01", 1, DITTMER("Dittmer would make billionaires and corporations pay their fair share"), "make billionaires and corporations pay their fair share"),
     ("edu-01", 2, DITTMER("Dittmer would fully fund public schools"), "I’ll fight to fully fund our public schools, support educators, and keep political culture wars out of the classroom."),
     ("edu-06", -2, DITTMER("Dittmer would keep public money in public schools"), "Protect funding for public education and special education by ensuring public, taxpayer funds stay within the public school system"))
PETERSON_SC = site("John Peterson", "https://www.johnpeterson.org/")
cand("SC-H-06", "SC-H-06:peterson", "John Peterson", "R", None,
     ("eco-07", 2, PETERSON_SC("Peterson would vote to cut spending and the debt"), "Vote for bills in Congress that are fiscally conservative that cut spending, reduce inflation, and bring down the national debt"),
     ("gov-05", 2, PETERSON_SC("Peterson would require voter ID"), "Fight for Free and Fair Elections that require Voter I.D."),
     ("cri-04", 1, PETERSON_SC("Peterson would champion tough-on-crime bills"), "Champion bills that are tough on crime that protect law abiding citizens and keep violent criminals off the street"))
VINCENT = site("John Vincent", "https://www.vincent4congress.org/")
cand("SC-H-07", "SC-H-07:vincent", "John Vincent", "D", "Navy career veteran and small business owner; pledges to take no corporate PAC money.",
     ("def-04", 2, VINCENT("Vincent would pass the War Powers Resolution to rein in the war"), "Work with all members of Congress to pass the War Powers Resolution so Congress can reel in this unconstitutional war"),
     ("def-15", -2, VINCENT("Vincent calls the war unconstitutional"), None),
     ("eco-01", 2, VINCENT("Vincent would remove the Social Security income cap"), "Introduce legislation to remove the Social Security income cap."),
     ("hea-03", 1, VINCENT("Vincent proposes low-cost public insurance for anyone who chooses it"), "One will provide low-cost insurance for every American who chooses it, without eliminating private insurance and without adding one dollar to the debt."),
     ("eco-07", 1, VINCENT("Vincent proposes a plan to bring federal spending under control"), "puts strict accountability measures in place through a 6-part plan to bring federal spending under control"),
     ("def-03", 1, VINCENT("Vincent would pass the Major Richard Star Act and other veterans’ bills"), "he will champion Veterans"))

# Washington: campaign sites, and the Washington State Standard's primary guide for the
# open 4th. Edwin Feller (R, 2nd) and Teresa Fox (R, 6th) list no issues; Chris Chung
# (R, 10th) has no site.
WA4_STANDARD = guide_answers("Washington State Standard (primary)", "https://washingtonstatestandard.com/voter-guides/contests/washington-4th-congressional-district-2026-primary/")
SILVA = site("Mary Silva", "https://www.marysilvaforcongress.com/")
cand("WA-H-01", "WA-H-01:silva", "Mary Silva", "R", None,
     ("agr-02", 1, SILVA("Silva would bring chip fabrication back to the U.S."), "Bring semiconductor manufacturing, IT, AI, and cybersecurity operations back to the U.S."),
     ("edu-03", 1, SILVA("Silva would expand apprenticeships and trade education"), "Expand apprenticeships, federal reskilling programs, and trade education as fast-track alternatives to four-year degrees"),
     ("imm-01", 1, SILVA("Silva would fortify border security"), "Fortify border security and overhaul high-level security clearance procedures to combat foreign espionage."),
     ("soc-08", 1, SILVA("Silva would require warrants before agencies or vendors collect location data"), "Enforce strict federal privacy standards requiring explicit warrants before government agencies or third-party vendors can collect, store, or share citizens’ location data"))
cand("WA-H-04", "WA-H-04:mckinney", "Amanda McKinney", "R", "Yakima County commissioner since 2019; former mortgage banker and small business owner.",
     ("eco-07", 1, WA4_STANDARD("McKinney would cut wasteful and fraudulent spending"), "Congress must restore fiscal responsibility by cutting wasteful and fraudulent spending"),
     ("eco-02", 1, WA4_STANDARD("McKinney would make the Trump tax cuts permanent"), "make the Trump tax cuts permanent"),
     ("ene-03", 1, WA4_STANDARD("McKinney would expand oil, gas, hydro and nuclear energy"), "restore American energy dominance through expansion of oil, gas, hydro and nuclear energy sectors"),
     ("ene-02", 2, WA4_STANDARD("McKinney would accelerate advanced and small modular reactors"), "We should accelerate the deployment of advanced nuclear reactors and small modular reactors"),
     ("imm-01", 2, WA4_STANDARD("McKinney would finish physical barriers and add border monitoring"), "Congress must build on that success by permanently securing the border, finishing physical barriers and installing enhanced monitoring and detection systems"),
     ("imm-08", 2, WA4_STANDARD("McKinney would strengthen interior enforcement and scale up courts for mass deportations"), "strengthen interior enforcement, scale-up the judicial system necessary for mass deportations"),
     ("soc-12", -2, WA4_STANDARD("McKinney backs the initiative on girls’ sports and says there are two sexes"), "Men are men. Women are Women. There are two sexes."))
DURESKY = site("John Duresky", "https://johnduresky4congress.com/")
cand("WA-H-04", "WA-H-04:duresky", "John Duresky", "D",
     "Retired Air Force major (24 years, including as a cyberspace officer) and project controls officer at the Hanford Field Office.",
     ("gov-01", 1, DURESKY("Duresky supports term limits"), "Term limits, ban stock trading, and overturn Citizens United."),
     ("gov-02", 1, DURESKY("Duresky would ban stock trading by members of Congress"), None),
     ("gov-13", -1, DURESKY("Duresky would overturn Citizens United"), None),
     ("hea-07", 1, DURESKY("Duresky would restore ACA subsidies"), "Keep rural hospitals open, restore ACA subsidies, and protect Medicare and Medicaid."),
     ("hea-03", 1, WA4_STANDARD("Duresky would strike Medicaid work requirements"), "I would strike the work requirements immediately"),
     ("eco-10", -1, WA4_STANDARD("Duresky would reduce the tariffs"), "Reduce the tariffs and end the war in Iran."),
     ("eco-09", 1, WA4_STANDARD("Duresky would support labor unions and raise the minimum wage"), "We need to support labor unions, protect Social Security, and raise the minimum wage."),
     ("eco-03", 1, WA4_STANDARD("Duresky would raise the minimum wage"), None),
     ("eco-12", 1, WA4_STANDARD("Duresky would rework taxes to favor working families over billionaires"), "We also need to rework our tax structure to benefit small businesses and working families instead of billionaires and corporations."),
     ("def-15", -2, WA4_STANDARD("Duresky opposes the war with Iran"), "I do NOT support the U.S. war with Iran."),
     ("def-04", 2, WA4_STANDARD("Duresky says war powers should go through Congress"), "War powers of any kind should go through Congress, every time."),
     ("imm-02", 2, WA4_STANDARD("Duresky supports legal status for immigrants here more than five years"), "I stand for a fast, fair and affordable path to legal status for all immigrants who have lived here for more than five years"),
     ("imm-08", -1, WA4_STANDARD("Duresky calls the administration’s enforcement immoral"), "The Trump administration’s immigration enforcement is immoral and un-American."),
     ("soc-12", 1, WA4_STANDARD("Duresky opposes the initiative on transgender athletes"), "I believe that everyone has the right to live their lives as their most authentic selves free from persecution or retribution"))
cand("WA-H-07", "WA-H-07:sheth", "Nirav Sheth", "R",
     "Came to the U.S. from India in 2008 to study engineering; served four years in the Marines, then as a Lakewood police officer; now a Pierce County business owner.",
     ("cri-01", 1, site("Nirav Sheth", "https://shethforcongress.com/")("Sheth would support emergency services and police"), "Supporting our emergency services and making crime illegal again"))
MELINE = site("Spencer Meline", "https://www.melineforcongress.com/")
cand("WA-H-08", "WA-H-08:meline", "Spencer Meline", "R", None,
     ("gov-01", 1, MELINE("Meline supports term limits"), "I support term limits for Congress."),
     ("gov-02", 2, MELINE("Meline would end congressional stock trading"), "Members of Congress should not be trading individual stocks while making laws that can affect those investments."),
     ("gov-12", 1, MELINE("Meline wants federal spending searchable"), "Federal spending should be easily searchable and understandable."),
     ("eco-07", 1, MELINE("Meline wants limits on deficit growth and less unnecessary spending"), "Congress needs enforceable restraints on deficit growth and a serious commitment to reducing waste, duplication, and unnecessary federal spending."),
     ("eco-08", 1, MELINE("Meline would create small business tax incentives"), "Create tax incentives that reward small businesses for investing, hiring, and growing here in America."),
     ("hou-04", 1, MELINE("Meline would cut regulatory barriers to housing"), "Encourage housing construction by reducing unnecessary regulatory barriers"),
     ("hou-05", 1, MELINE("Meline would give first-time buyers tax relief"), "Provide targeted tax relief that helps working Americans overcome the enormous upfront cost of purchasing their first home."),
     ("ene-08", 1, MELINE("Meline would shift resources to year-round wildfire prevention"), "Shift more resources toward year-round prevention and mitigation rather than spending enormous sums only after fires become emergencies."),
     ("ene-03", 1, MELINE("Meline supports all-of-the-above energy, including gas and oil"), "America should pursue abundant, reliable energy, including hydropower, nuclear power, renewables, natural gas, and domestic oil production"),
     ("ene-02", 1, MELINE("Meline’s all-of-the-above energy includes nuclear"), None),
     ("ene-01", 1, MELINE("Meline’s all-of-the-above energy includes renewables"), None),
     ("edu-03", 1, MELINE("Meline would expand apprenticeships and technical education"), "Expand access to apprenticeships, technical education, and career training"),
     ("soc-08", 2, MELINE("Meline would establish strong federal privacy protections"), "Establish strong federal privacy protections giving individuals greater transparency and control over how their personal information is collected, stored, sold, and used."))
cand("WA-H-09", "WA-H-09:basler", "Doug Basler", "R",
     "Three decades in business, media and advertising; a former youth and worship pastor who worked on homelessness outreach with rescue missions.",
     ("ene-06", -1, site("Doug Basler", "https://www.dougbasler.com/")("Basler says Washington’s Climate Commitment Act drives up energy costs"), "The Climate Commitment Act may sound good, but in practice it is driving up the cost of energy"))

# Alaska: Eric Hafner (D) posts no issues.
MCDERMOTT = site("Jim McDermott", "https://jamesmcdermott.org/")
cand("AK-H-00", "AK-H-00:mcdermott", "Jim McDermott", "L",
     "Retired Air Force master sergeant (22.5 years) who has taught business at UAF for more than eight years; in Alaska 35 years.",
     ("eco-07", 2, MCDERMOTT("McDermott promises to add nothing to the debt"), "Zero is what he has promised to add to the debt through his tenure."),
     ("eco-10", -1, MCDERMOTT("McDermott would have voted against keeping tariffs on Canada"), "Jim would have voted no on both."),
     ("gov-01", 2, MCDERMOTT("McDermott supports term limits and would not seek a third term"), "He supports term limits and practices what he preaches: he would not seek a third term."))

# Alabama: the Alabama Reflector's guide summarizes platforms in its own words; campaign
# sites for quotes
AL_REFLECTOR = lambda d: lambda note: page(f"Alabama Reflector voter guide: {note}", f"https://alabamareflector.com/voter-guides/contests/al0{d}/", READ)  # noqa: E731
cand("AL-H-01", "AL-H-01:carl", "Jerry Carl", "R", "Represented Alabama’s 1st District in Congress from 2021 to 2025; former Mobile County commissioner.",
     ("imm-01", 2, site("Jerry Carl", "https://jerrycarlforcongress.com/")("Carl helped pass a border bill funding a wall and Border Patrol agents"), "including funding to build a border wall and hire a record number of Border Patrol agents"),
     ("soc-04", 1, AL_REFLECTOR(1)("Carl would support abortion restrictions"), None),
     ("eco-07", 1, AL_REFLECTOR(1)("Carl supports a balanced budget amendment"), None))
JONES_AL = site("Clyde Jones", "https://clydeforcongress.com/")
cand("AL-H-01", "AL-H-01:jones", "Clyde Jones Jr.", "D",
     "Episcopal minister, decorated Army combat veteran and retired DuPont safety coordinator; former board president of Alabama Arise.",
     ("hea-03", 1, JONES_AL("Jones supports expanding Medicaid"), "I believe in the expansion of Medicaid"),
     ("hea-07", 1, JONES_AL("Jones supports the ACA’s enhanced premium tax credits"), None),
     ("hea-01", 1, JONES_AL("Jones is running on health care for all"), "Committed to serving people over corporate pacs, Congressional reform, and healthcare for all."),
     ("gov-13", -2, JONES_AL("Jones would vote to overturn Citizens United"), "Corporations are NOT people, and they don't have the same interests."),
     ("gov-11", 2, JONES_AL("Jones would get corporate PACs out of elections"), "and get Corporate PACs out of our elections"),
     ("gov-02", 2, JONES_AL("Jones would ban stock trading by members and their families"), "In Congress I'll advocate and vote for a ban on stock trading for members and their immediate families."),
     ("imm-08", -1, JONES_AL("Jones says ICE has gotten out of control"), "Secure borders are necessary, but ICE has gotten out of control."),
     ("imm-01", 1, JONES_AL("Jones says secure borders are necessary"), None),
     ("imm-02", 2, JONES_AL("Jones would fight for a path for undocumented people to get documented"), "I will fight for real immigration reform — a clear, straightforward path for undocumented people"))
cand("AL-H-03", "AL-H-03:mcinnis", "Lee McInnis", "D", "Retired from the military.",
     ("gov-01", 1, AL_REFLECTOR(3)("McInnis would push for 12-year term limits"), None),
     ("gov-11", 1, AL_REFLECTOR(3)("McInnis would limit PAC money"), None),
     ("eco-09", 1, AL_REFLECTOR(3)("McInnis would advocate for union rights"), None))
cand("AL-H-04", "AL-H-04:pusczek", "Amanda Pusczek", "D", "Nurse.",
     ("hea-03", 1, AL_REFLECTOR(4)("Pusczek supports letting Alabamians enroll directly in Medicaid expansion"), None),
     ("eco-03", 1, AL_REFLECTOR(4)("Pusczek supports a $15 minimum wage"), None),
     ("eco-09", 1, AL_REFLECTOR(4)("Pusczek supports union rights"), None),
     ("soc-03", 1, AL_REFLECTOR(4)("Pusczek supports federal protections for abortion rights"), None),
     ("edu-01", 1, AL_REFLECTOR(4)("Pusczek supports federal education aid"), None))
cand("AL-H-05", "AL-H-05:sneed", "Andrew Sneed", "D", "Businessman.",
     ("hea-03", 1, AL_REFLECTOR(5)("Sneed would expand Medicaid eligibility"), None),
     ("hou-01", 1, AL_REFLECTOR(5)("Sneed would expand affordable housing"), None),
     ("eco-10", -1, AL_REFLECTOR(5)("Sneed would repeal President Trump’s tariffs"), None),
     ("edu-06", -1, AL_REFLECTOR(5)("Sneed opposes school vouchers"), None),
     ("gov-01", 1, AL_REFLECTOR(5)("Sneed supports House term limits"), None),
     ("gov-02", 1, AL_REFLECTOR(5)("Sneed supports banning stock trading by members"), None),
     ("gov-11", 1, AL_REFLECTOR(5)("Sneed supports limits on dark money"), None))
cand("AL-H-06", "AL-H-06:mercer", "Maurice Mercer", "D", "Former Pelham city councilman.",
     ("hea-06", 1, site("Maurice Mercer", "https://www.mauricemercer.com/")("Mercer supports better mental health services"), "I support expanding access to affordable healthcare, protecting rural healthcare providers, improving mental health services, and increasing transparency in prescription drug pricing."),
     ("eco-03", 1, AL_REFLECTOR(6)("Mercer supports raising the $7.25 federal minimum wage"), None))
AKIN = site("Ammie Akin", "https://www.akinforcongress.com/")
cand("AL-H-07", "AL-H-07:akin", "Ammie Akin", "R", "Former educator and founder of a nonprofit.",
     ("eco-07", 1, AKIN("Akin would fight wasteful spending"), "Fight wasteful Washington spending and demand responsible, accountable use of taxpayer dollars."),
     ("cri-01", 1, AKIN("Akin would give law enforcement the resources it needs"), "Support law enforcement, first responders, and the military with the resources they need"))

# Maryland: Maryland Matters' guide (George McDermott, R, 4th, and Scott Collier, R, 7th,
# did not answer it) and campaign sites
MD_MM = lambda slug: guide_answers("Maryland Matters", f"https://marylandmatters.org/voter-guides/contests/{slug}/")  # noqa: E731
MD1, MD2, MD3, MD4, MD5, MD6, MD8 = (MD_MM(s) for s in ("u-s-house-1st-district", "2nd-district", "3rd-district", "4th-district", "5th-district", "6th-district", "8th-district"))
cand("MD-H-01", "MD-H-01:schwartz", "Dan Schwartz", "D", "Consumer watchdog who has worked with state and federal regulators on financial misconduct for more than 14 years.",
     ("gov-04", 1, MD1("Schwartz would ban partisan gerrymandering and use independent commissions"), "support legislation to ban partisan gerrymandering and put redistricting decisions in the hands of independent state commissions"),
     ("gov-06", 1, MD1("Schwartz supports the For the People Act, which expands early and mail voting"), "I would also support the For the People Act which better funds equipment upgrades, provides security standards, broadens ways to register and expands early/mail voting."),
     ("imm-08", -2, MD1("Schwartz would reallocate much of ICE’s budget"), "ICE should not have a larger budget than the Marine Corps. Much of its budget must be reallocated"),
     ("eco-10", -1, MD1("Schwartz would rein in the president’s use of tariffs"), "I will support legislation to rein in the President’s use of tariffs"),
     ("eco-01", 2, MD1("Schwartz would roll back tax cuts for billionaires"), "I will fight to roll back the President’s tax cuts for billionaires"),
     ("eco-02", 1, MD1("Schwartz wants permanent tax cuts for working-class families"), "We will seek permanent tax cuts for working class families instead of billionaires."),
     ("hea-03", 1, MD1("Schwartz would let people buy into Medicare"), "Another step is allowing people to choose to buy into Medicare if they want."),
     ("def-10", -1, MD1("Schwartz defends foreign aid such as PEPFAR"), "By feeding kids in war-stricken nations, fighting HIV/AIDS (PEPFAR program) etc. we build long term political and economic influence around the world."))
cand("MD-H-02", "MD-H-02:wallace", "Dave Wallace", "R", None,
     ("gov-05", 2, MD2("Wallace calls the SAVE Act essential for photo voter ID"), "The Save Act is essential to assure photo Voter Identification"),
     ("gov-06", -2, MD2("Wallace would eliminate most mail-in ballots"), "That we eliminate mail in ballots except in cases of special circumstances, and military service members."),
     ("imm-01", 1, MD2("Wallace would maintain secure borders"), "We must maintain secure borders, as they establish our safety, security, and sovereignty."),
     ("ene-03", 1, MD2("Wallace would expand U.S. energy, including LNG exports from Baltimore"), "Create abundant U.S. energy; establish Baltimore LNG exports"),
     ("eco-10", 1, MD2("Wallace supports reciprocal tariffs to restore industry"), "use wage-disparity and reciprocal tariffs to restore U.S. industry"),
     ("def-14", 1, MD2("Wallace would sanction Russia over Ukraine"), "sanction Russia for its war against Ukraine"),
     ("def-16", 1, MD2("Wallace would deter Chinese aggression"), "deter Chinese aggression"),
     ("hea-06", 1, MD2("Wallace would expand mental health capacity"), "Expand mental health capacity"),
     ("hou-04", 1, MD2("Wallace would cut red tape on housing"), "Cut red tape lowering housing and business costs."),
     ("cri-01", 1, site("Dave Wallace", "https://davewallace.us/")("Wallace would give police the resources they need"), "He will vote to give them the resources and equipment they need to protect us from criminals both foreign and domestic."))
cand("MD-H-03", "MD-H-03:flowers", "Berney Flowers", "R", None,
     ("gov-05", 1, MD3("Flowers supports voter ID and post-election audits"), "I support voter ID, regular maintenance of voter rolls, secure chain-of-custody for ballots, and transparent post-election audits."),
     ("imm-01", 1, MD3("Flowers wants a secure border and faster legal processing"), "We need a secure border, consistent enforcement, and faster processing so people who want to immigrate legally can do so."),
     ("ene-03", 1, MD3("Flowers would expand American energy production"), "expand American energy production to lower fuel and utility costs"),
     ("hou-04", 1, MD3("Flowers would reduce federal barriers to housing"), "reduce federal barriers that make housing more expensive"),
     ("eco-07", 1, MD3("Flowers would fight for fiscal discipline"), "I’ll fight for fiscal discipline to control inflation"),
     ("def-02", 1, MD3("Flowers backs strong alliances"), "We preserve peace through strong alliances, a capable military, and smart diplomacy."))
cand("MD-H-04", "MD-H-04:husseini", "Sam Husseini", "G",
     "Journalist and communications director of the Institute for Public Accuracy; a longtime 4th District resident.",
     ("imm-08", -2, MD4("Husseini says ICE enforcement should be stopped"), "not solely enforcement which is ICE and should be stopped"),
     ("eco-01", 2, MD4("Husseini says oligarchs should be taxed more"), "They should obviously be taxed more, more properly regulated"),
     ("gov-13", -2, MD4("Husseini would confront corporate personhood"), "the legal structure of corporate power, which perverted the 14th Amendment"),
     ("gov-11", 1, MD4("Husseini wants public campaign funding to counter big money"), "big money groups like AIPAC, so we need public funding"),
     ("def-12", -2, MD4("Husseini opposes backing Israel’s war in Gaza"), "The establishment parties have made our country more of an empire, backing imperial Israel’s genocide"),
     ("def-15", -2, MD4("Husseini calls the attacks on Yemen, Iran and Venezuela unconstitutional"), "unconstitutionally attacking Yemen, Iran and Venezuela"),
     ("def-01", -2, MD4("Husseini would demilitarize"), "Demilitarize and abide by the law."),
     ("hea-04", -1, MD4("Husseini would stop the privatization of Medicare and Medicaid"), "It’s crucial to stop the privatization slide of Medicare and Medicaid and the threat to Social Security."),
     ("hea-01", 1, MD4("Husseini cites a study that expanding Medicare could cover everyone"), None),
     officialSite="https://samhusseini.com/")
BOAFO = site("Adrian Boafo", "https://www.adrianboafo.com/")
cand("MD-H-05", "MD-H-05:boafo", "Adrian Boafo", "D", "Maryland state delegate.",
     ("eco-03", 2, BOAFO("Boafo would raise the federal minimum wage to $15 tied to inflation"), "Follow Maryland’s lead by raising the federal minimum wage from $7.25 to $15 an hour and tie it to inflation"),
     ("eco-02", 1, BOAFO("Boafo would cut taxes for working and middle-class families"), "Cut taxes for working and middle-class families while closing loopholes that let big corporations and the ultra-wealthy avoid paying their fair share."),
     ("eco-01", 1, BOAFO("Boafo would close loopholes for the ultra-wealthy"), None),
     ("soc-07", 2, BOAFO("Boafo would guarantee universal child care"), "Guarantee universal childcare so no parent has to choose between earning a paycheck and caring for their child."),
     ("imm-08", -2, MD5("Boafo says ICE must be abolished in its current form"), "In its current form, ICE must be abolished."),
     ("imm-07", 1, MD5("Boafo would focus enforcement on violent offenders and traffickers"), "Immigration enforcement resources should prioritize violent offenders, traffickers, cartel networks, and those who endanger public safety"),
     ("hou-02", 2, MD5("Boafo introduced a state bill banning hedge funds from buying single-family homes"), "I introduced legislation this session to ban hedge funds from buying up single-family homes"),
     ("hea-01", 1, MD5("Boafo supports Medicare for All with a private option"), "For healthcare, I'd support Medicare for All with a private option."),
     ("gov-03", 1, MD5("Boafo supports the DISCLOSE Act"), "I will support The Freedom to Vote Act, The John R. Lewis Voting Rights Advancement Act, and The DISCLOSE Act."),
     ("def-07", 1, MD5("Boafo wants to lead with diplomacy, not military intervention"), "We can return to a country that leads with diplomacy & development, not military intervention."),
     ("def-02", 1, MD5("Boafo would repair relationships with allies"), "we must do everything we can to repair the relationships we've frayed with our allies"))
cand("MD-H-05", "MD-H-05:chaffee", "Chris Chaffee", "R", None,
     ("gov-05", 1, MD5("Chaffee supports voter ID"), "We should have a ID for voting."),
     ("imm-01", 1, MD5("Chaffee would keep the borders closed"), "Keeping our borders closed is the best way to move forward."),
     ("ene-10", 1, MD5("Chaffee would reopen closed coal plants to lower electricity prices"), "Begin with electricity prices, move to re-open all coal plants shut down by Annapolis."),
     ("hou-04", 1, MD5("Chaffee would make it easier to build homes"), "Encourage local governments to make it easier to build homes."),
     ("soc-07", 1, MD5("Chaffee would raise the child care tax credit"), "Increase the childcare tax credit to 100 percent."),
     ("def-07", 1, MD5("Chaffee calls war the last resort"), "War should be the last resort."))
FICKER = site("Robin Ficker", "https://voteficker.com/")
cand("MD-H-06", "MD-H-06:ficker", "Robin Ficker", "R",
     "Longtime taxpayer activist who led petition drives for charter amendments limiting property tax increases and setting term limits.",
     ("eco-07", 2, FICKER("Ficker would slash wasteful spending and reduce the deficit"), "In Congress, he will work to slash wasteful spending, reduce the federal deficit, and restore sanity to the budget process."),
     ("eco-01", -1, MD6("Ficker would oppose tax increases"), "I’ll oppose tax increases and endorse a balanced budget."),
     ("cri-01", 1, FICKER("Ficker would support police and oppose soft-on-crime policies"), "Robin Ficker will support our police, hold criminals accountable, and fight against soft-on-crime policies"),
     ("gov-05", 2, MD6("Ficker supports mandatory voter ID"), "Mandatory voter ID same as required for driving, boarding an airplane"),
     ("imm-01", 1, MD6("Ficker would keep the borders secured"), "Keep borders secured to stop illegal immigration."),
     ("def-16", 1, MD6("Ficker calls China the greatest adversary"), "China is our greatest adversary."),
     ("def-14", 1, MD6("Ficker urges wariness of Putin"), "Wariness of today’s Stalin—Putin—is important."),
     ("def-11", 1, MD6("Ficker would be friendly to Israel"), "Be friendly to Canada, Mexico, and Israel."),
     ("agr-05", 1, MD6("Ficker would develop U.S. rare minerals"), "Develop US rare minerals and energy."))
LANDMAN = site("Moshe Landman", "https://www.moshelandman.us/")
cand("MD-H-06", "MD-H-06:landman", "Moshe Landman", "G", None,
     ("hea-01", 2, LANDMAN("Landman would implement universal health care"), "Implement a universal healthcare system that will save 100,000 lives per year"),
     ("def-01", -2, LANDMAN("Landman would cut defense spending significantly"), "It must be cut significantly"),
     ("gov-07", 1, MD6("Landman supports ranked-choice voting"), "I support ranked-choice voting, independent redistricting commissions, and equal ballot access"),
     ("gov-04", 1, MD6("Landman supports independent redistricting commissions"), None),
     ("gov-11", 1, MD6("Landman supports public financing and limits on corporate influence"), "I also support public financing of campaigns and stronger limits on corporate and special-interest influence."),
     ("imm-02", 1, MD6("Landman supports a fair path to legal status"), "provides a fair path to legal status"),
     ("imm-08", -1, MD6("Landman opposes raids, detention and punitive enforcement"), "I do not support current approaches that rely on raids, detention, family separation, and punitive enforcement."),
     ("hou-01", 1, MD6("Landman would expand affordable housing"), "expanding affordable housing and housing assistance"),
     ("eco-01", 1, MD6("Landman would lift the Social Security payroll-tax cap"), "I support lifting the Social Security payroll-tax cap on high earners"),
     ("def-07", 1, MD6("Landman would resolve disputes through diplomacy"), "I support resolving disputes through diplomacy and international institutions"))
cand("MD-H-08", "MD-H-08:riley", "Cheryl Riley", "R", None,
     ("gov-05", 1, MD8("Riley would require REAL ID to vote"), "requiring REAL ID for voter identification"),
     ("gov-06", -2, MD8("Riley would limit mail voting to overseas military and voters with disabilities"), "limiting mail-in voting to active-duty military overseas and citizens with documented disabilities"),
     ("imm-07", 1, MD8("Riley would halt immigration until dangerous people already here are removed"), "I support halting immigration until we identify and remove dangerous individuals already here."),
     ("eco-07", 1, MD8("Riley would cut wasteful spending"), "I’ll support cutting wasteful spending"),
     ("ene-03", 1, MD8("Riley wants energy independence through oil, gas and nuclear"), "achieve energy independence via domestic oil, gas, and nuclear"),
     ("ene-02", 1, MD8("Riley supports nuclear power"), None),
     ("eco-10", 1, MD8("Riley wants reciprocal trade deals that mirror partners’ tariffs"), "We must pursue reciprocal trade deals that mirror partners' tariff rates"),
     ("eco-01", 1, MD8("Riley supports raising the Social Security payroll tax cap"), "I support raising the payroll tax cap"))
NWALLACE = site("Nancy Wallace", "https://www.nancywallace.us/")
cand("MD-H-08", "MD-H-08:wallace", "Nancy Wallace", "G", None,
     ("ene-01", 2, NWALLACE("Wallace wants an emergency transformation to renewable energy"), "We need a major, emergency economic transformation to renewable energy and green jobs"),
     ("ene-02", -2, NWALLACE("Wallace would switch from nuclear power to local renewables"), "as we switch from nuclear power to safe, local renewable electricity"),
     ("cri-03", 2, NWALLACE("Wallace wants an automatic outside investigation of every police killing"), "Automatic external investigation of every police killing"),
     ("cri-02", 1, NWALLACE("Wallace would make police body camera footage public"), "Police body camera footage as public property"),
     ("hea-01", 2, MD8("Wallace supports free universal health care"), "I support free universal health care, like most civilized countries"),
     ("soc-07", 2, MD8("Wallace supports free child care and early education"), "free early childhood education especially the Montessori method, with free childcare"),
     ("eco-01", 2, MD8("Wallace supports a wealth tax on fortunes over $10 million"), "I support 1% annual tax on wealth over $10 million, rising to 4% on wealth above $1 billion"),
     ("hou-06", 1, MD8("Wallace supports rent control"), "I support fair, stable rent control."),
     ("imm-08", -1, MD8("Wallace would disband ICE and start a new agency"), "ICE should be disbanded, its culture is too contaminated"),
     ("def-01", -2, MD8("Wallace opposes military buildup and arms sales"), "War, and massive arms sales overseas, and military buildup is the opposite of civilization."),
     ("hea-06", 1, MD8("Wallace would emphasize mental health programs"), "We must emphasize mental health programs to avoid many conditions leading to crises"))

# Tennessee: campaign sites, and the Tennessee Lookout's guide for bios and platform
# summaries (in its words). Most of the state's many independents have no site and no
# entry beyond their name.
TN_LOOKOUT = lambda slug: lambda note: page(f"Tennessee Lookout voter guide: {note}", f"https://tennesseelookout.com/voter-guides/contests/{slug}/", READ)  # noqa: E731
TN = {d: TN_LOOKOUT(f"congressional-district-{d}-u-s-house-of-representatives") for d in (1, 2, 3, 4, 5, 8, 9)}
TN[6], TN[7] = TN_LOOKOUT("congressional-district-6-2"), TN_LOOKOUT("congressional-district-7-2")
BURKE = site("Kristi Burke", "https://www.votekristiburke.com/")
cand("TN-H-01", "TN-H-01:burke", "Kristi Burke", "D",
     "Muralist and mother who decided to run after security removed her from Rep. Diana Harshbarger’s 2025 town hall as she asked about Medicaid cuts.",
     ("hea-01", 2, BURKE("Burke supports Medicare for All"), "I support a universal, single-payer system."),
     ("hea-04", -2, BURKE("Burke would replace the profit-driven system"), "I will fight to replace our current profit-driven system with one that puts people first."),
     ("edu-01", 2, BURKE("Burke says public education must be fully funded"), "PUBLIC EDUCATION MUST BE FULLY FUNDED"),
     ("edu-06", -2, BURKE("Burke opposes private school vouchers"), "Public dollars must go to public schools"))
cand("TN-H-02", "TN-H-02:barnett", "Michaela Barnett", "D",
     "Civil engineer (Ph.D.) who opened KnoxFill, a refill store, and was a congressional fellow with Rep. Paul Tonko.",
     ("eco-06", 1, site("Michaela Barnett", "https://www.michaelafortennessee.com/")("Barnett would bring federal infrastructure money home"), "We deserve a Representative who will fight to bring those dollars home and invest in our region."))
cand("TN-H-02", "TN-H-02:fine", "Bruce Fine", "I", None,
     ("gov-01", 1, TN[2]("Fine supports term limits"), None),
     ("gov-11", 1, TN[2]("Fine supports campaign finance reform"), None),
     ("edu-03", 1, TN[2]("Fine supports more access to community college and vocational education"), None))
HEIMERMAN = site("Adam Heimerman", "https://www.vote4heimerman.com/")
cand("TN-H-02", "TN-H-02:heimerman", "Adam Heimerman", "I", "Loudon County resident.",
     ("gov-13", -2, HEIMERMAN("Heimerman would abolish super PACs and overturn Citizens United"), "Corporations are not people. Super PACs must be abolished."),
     ("gov-11", 2, HEIMERMAN("Heimerman would aggressively pursue ending Citizens United"), "Adam despises the black hole that is Citizens United and will aggressively pursue its destruction."),
     ("imm-01", 1, HEIMERMAN("Heimerman wants secure borders"), "sovereign nations must have secure borders"),
     ("imm-02", 1, HEIMERMAN("Heimerman wants better paths to citizenship"), "We need better paths to citizenship while showing compassion to those seeking the legal route."),
     ("hou-05", 1, TN[2]("Heimerman wants more help for first-time homebuyers"), None),
     officialSite="https://www.vote4heimerman.com/")
GOLLADAY = site("Anna Golladay", "https://annagolladay.com/")
cand("TN-H-03", "TN-H-03:golladay", "Anna Golladay", "D",
     "Chattanooga entrepreneur (Biased Apparel) and CEO of Work of Place; former associate pastor at St. Elmo Methodist Church.",
     ("eco-03", 1, GOLLADAY("Golladay would raise the federal minimum wage"), "Raise the federal minimum wage"),
     ("hou-01", 1, GOLLADAY("Golladay would expand the Low-Income Housing Tax Credit"), "Expand the Low-Income Housing Tax Credit"),
     ("hou-05", 2, GOLLADAY("Golladay backs a down-payment tax credit of up to $50,000"), "A down-payment tax credit worth up to $50,000 opens the door to homeownership"),
     ("eco-02", 1, GOLLADAY("Golladay would restore and expand the Child Tax Credit"), "Restore and Expand the Child Tax Credit"),
     ("eco-10", -1, GOLLADAY("Golladay would require Congress to approve tariffs"), "Requiring Congress — not one administration — to sign off on tariffs"),
     ("hea-01", 1, GOLLADAY("Golladay calls health care a human right"), "Health care is a human right"),
     ("hea-03", 1, GOLLADAY("Golladay faults Tennessee for refusing to expand Medicaid"), None))
BRODERICK = site("Victoria Broderick", "https://www.victoria4tennessee.org/")
cand("TN-H-04", "TN-H-04:broderick", "Victoria Broderick", "D",
     "Works in logistics and technology; former chair of the Lincoln County Democratic Party.",
     ("eco-01", 1, BRODERICK("Broderick wants the wealthiest to pay their fair share"), "I believe the wealthiest individuals and the biggest corporations should pay their fair share"),
     ("soc-03", 1, BRODERICK("Broderick ran after Roe was overturned"), "a country that no longer trusted women to make decisions about their own bodies and their own families"),
     ("soc-05", 1, BRODERICK("Broderick would end federal marijuana penalties"), "end federal marijuana penalties for good"),
     ("imm-01", 1, BRODERICK("Broderick would secure the border"), "secure the border and ensure a fair immigration process"),
     ("soc-08", 1, BRODERICK("Broderick would protect privacy from new technology"), "Protect Your Privacy in the Age of New Technology"),
     ("hea-01", 1, TN[4]("Broderick’s platform includes universal health care"), None))
ANDERS = site("Jacob Anders", "https://jacobanders.org/")
cand("TN-H-04", "TN-H-04:anders", "Jacob Anders", "I", "Historian and author.",
     ("gov-01", 2, ANDERS("Anders would limit House members to three terms and senators to two"), "We're going to limit politicians to 3 terms in the House of Representatives"),
     ("gov-02", 2, ANDERS("Anders would ban members and their families from trading stocks"), "I support a full ban on members of Congress, their spouses, and children buying or selling individual stocks."),
     ("eco-01", 2, ANDERS("Anders would eliminate the Social Security tax cap"), "we must eliminate the tax cap so the ultra-wealthy pay into Social Security on every dollar of their income"),
     ("def-04", 2, ANDERS("Anders would repeal the AUMFs so Congress votes on war"), "Congress must reclaim its Constitutional duty to debate and vote on war."),
     ("soc-08", 1, ANDERS("Anders would regulate or ban mass surveillance technology such as Flock"), "I call for either heavy regulations or a ban of mass surveillance technology like Flock & Axon."),
     ("hea-01", 2, ANDERS("Anders would move to a single-payer system"), "By transitioning to a streamlined, single-payer framework, we eliminate the middlemen who profit from complexity."))
cand("TN-H-04", "TN-H-04:faircloth", "Clay Faircloth", "I", "Ran in the Democratic primary for the 6th District in 2022 and 2024.",
     officialSite="https://claycares.org/")
HATCHER = site("Charlie Hatcher", "https://charliehatcher.com/")
cand("TN-H-05", "TN-H-05:hatcher", "Charlie Hatcher", "R",
     "Fifth-generation Williamson County dairy farmer and livestock veterinarian; Tennessee agriculture commissioner from 2018 to 2025.",
     ("eco-07", 1, HATCHER("Hatcher would fight inflationary federal spending"), "Washington cannot spend and borrow its way to prosperity."),
     ("ene-03", 1, HATCHER("Hatcher supports expanding American energy production"), "He supports expanding American energy production"),
     ("imm-01", 1, HATCHER("Hatcher would give Border Patrol more personnel and technology"), "Charlie supports enforcing America’s immigration laws, providing Border Patrol with the personnel, technology, infrastructure, and resources necessary to do its job"))
MOLDER = site("Chaz Molder", "https://chazmolder.com/")
cand("TN-H-05", "TN-H-05:molder", "Chaz Molder", "D", "Mayor of Columbia in his second term; a lawyer.",
     ("gov-02", 1, MOLDER("Molder would ban stock trading by members of Congress"), "I will be committed to restoring trust in our government by advocating for a ban on stock trading by members of Congress."),
     ("eco-09", 1, MOLDER("Molder would protect the right to organize"), "We also must empower workers by standing up for the right to organize and strengthening labor protections."),
     ("hea-09", 1, MOLDER("Molder would expand coverage and invest in preventive care"), "We must work to eliminate barriers to care, expand health insurance coverage, and invest in preventive services"))
GARRETT = site("Johnny Garrett", "https://johnnygarrettforcongress.com/")
cand("TN-H-06", "TN-H-06:garrett", "Johnny Garrett", "R", "State representative since 2018 and House Republican whip since 2019; a lawyer.",
     ("imm-08", 2, GARRETT("Garrett created a state border czar to work with ICE on deportations"), "work hand in glove with ICE to deport all illegal aliens from the Volunteer State"),
     ("imm-01", 2, GARRETT("Garrett says a physical border wall is a necessity"), "Johnny believes that a physical border wall is a necessity to keep our border secure for years to come."),
     ("soc-12", -1, GARRETT("Garrett passed a state ban on transgender women in women’s sports"), "As State Representative, Johnny passed legislation banning men from competing in women’s sports"))
cand("TN-H-06", "TN-H-06:croley", "Mike Croley", "D",
     "Navy veteran, former Tennessee State Park ranger and Presidential Management Fellow at the State and Agriculture departments; a Vanderbilt-trained engineer.")
COPELAND = site("Darden Copeland", "https://www.dardenforcongress.com/")
cand("TN-H-07", "TN-H-07:copeland", "Darden Copeland", "D",
     "Founder and CEO of Calvert Street Group, a Nashville public affairs firm; ran in the 2025 special election for the seat.",
     ("gov-02", 2, COPELAND("Copeland would ban stock trading by members, families and executive officials"), "Darden supports a full ban on stock trading by members of Congress, their families, and members of the Executive Branch."),
     ("gov-01", 1, COPELAND("Copeland supports term limits"), "He supports term limits, because Congress should be a period of service — not a lifetime career."),
     ("hea-07", 1, COPELAND("Copeland would defend affordable premiums and Medicaid"), "In Congress, he'll fight to protect Medicaid, defend affordable health care premiums, lower prescription drug costs, and keep rural hospitals open"))
cand("TN-H-07", "TN-H-07:reynolds", "Lowell Reynolds", "I", "Grammy-winning music engineer in Nashville and a law student at Syracuse.")
KUHN = site("Heidi Kuhn", "https://www.kuhnforcongress.com/")
cand("TN-H-08", "TN-H-08:kuhn", "Heidi Kuhn", "D",
     "Shelby County criminal court clerk; earlier led the county’s Crime Victims Center.",
     ("eco-03", 2, KUHN("Kuhn backs the Raise the Wage Act’s $17 minimum by 2030"), "Heidi will vote to raise the minimum wage by signing onto the “Raise the Wage” act"),
     ("eco-09", 2, KUHN("Kuhn would sign onto the PRO Act"), "Heidi will sign onto the PRO Act (Protect the Right to Organize), which will strengthen collective bargaining and protect unions."),
     ("eco-02", 1, KUHN("Kuhn would expand the Child Tax Credit"), "Heidi will expand the Child Tax Credit to make it more affordable for parents to raise children."),
     ("hou-01", 1, KUHN("Kuhn would expand the Low-Income Housing Tax Credit"), "Heidi will expand the Low-Income Housing Tax Credit and stand up to Wall Street Investors that are buying up housing"),
     ("eco-04", 1, KUHN("Kuhn would oppose grocery chain mergers"), "Heidi will oppose monopolistic mergers of large grocery chains"),
     ("eco-10", -1, KUHN("Kuhn would oppose tariffs on farm equipment and fertilizer"), "Heidi will oppose tariffs on equipment and fertilizer that drive up costs for Tennessee farmers"),
     ("def-15", -2, KUHN("Kuhn would vote to end the war"), "Heidi will vote to end the a war that has hit fertilizer and fuel costs hard"),
     ("hea-03", 1, KUHN("Kuhn would repeal the Medicare and Medicaid cuts"), "Heidi will repeal cuts to Medicare and Medicaid that are stripping health coverage from seniors and working families across Tennessee"),
     ("hou-09", 1, KUHN("Kuhn would expand rural high-speed internet"), "Heidi will expand Access to high-speed internet and other advanced technology to help West TN farmers"),
     ("agr-01", 1, KUHN("Kuhn wants a better safety net for small farmers"), "instead advocating for a bill that provides a better safety net for small farmers"),
     ("imm-08", -1, KUHN("Kuhn is concerned about racial profiling by ICE"), "What we are seeing from ICE raises serious concerns about racial profiling"))
cand("TN-H-08", "TN-H-08:taylor", "Horace Taylor", "I", "Retired Army major who owns a small engine repair shop in Germantown.")
cand("TN-H-08", "TN-H-08:futch", "Antonio Futch", "I", "Marine Corps veteran, educator and entertainment executive from Memphis.",
     officialSite="https://www.misterfutch.com/mister-futch/")
cand("TN-H-08", "TN-H-08:moses", "Pamela Moses", "I", "Black Lives Matter activist and former candidate for Memphis mayor.",
     ("ene-06", 1, TN[8]("Moses’ platform includes reducing carbon emissions"), None),
     ("hea-06", 1, TN[8]("Moses’ platform includes expanding mental health care"), None))
BTAYLOR = site("Brent Taylor", "https://brenttaylorforcongress.com/")
cand("TN-H-09", "TN-H-09:taylor", "Brent Taylor", "R",
     "State senator since 2022; former Memphis City Council member and Shelby County commissioner.",
     ("edu-06", 1, TN[9]("Taylor supported Gov. Bill Lee’s private school voucher plan"), None),
     ("cri-06", -1, BTAYLOR("Taylor cracked down on revolving-door bail policies"), "cracking down on revolving-door bail policies"))
PEARSON = site("Justin J. Pearson", "https://www.votejustinj.com/")
cand("TN-H-09", "TN-H-09:pearson", "Justin Pearson", "D",
     "State representative since 2023, one of the “Tennessee Three” expelled that year over a gun-reform protest and returned to office; co-founded Memphis Community Against the Pipeline.",
     ("eco-03", 1, PEARSON("Pearson wants a living minimum wage"), "Ensure the minimum wage is a true living wage"),
     ("eco-09", 2, PEARSON("Pearson would pass the PRO Act"), "Pass the PRO Act to protect and restore workers’ right to organize."),
     ("edu-01", 2, PEARSON("Pearson would fully fund public education"), "Fully fund our public education system and rein in voucher scams."),
     ("edu-06", -2, PEARSON("Pearson would rein in vouchers"), None),
     ("gov-13", -2, PEARSON("Pearson would overturn Citizens United"), "Get big corporate money out of politics by overturning Citizens United."),
     ("gov-02", 2, PEARSON("Pearson would ban members of Congress from trading stock"), "Ban career politicians and members of Congress from trading stock and getting rich while in office."))
cand("TN-H-09", "TN-H-09:clark", "Dennis Clark", "I", "Ran as an independent for the 9th District in 2020, 2022 and 2024.",
     officialSite="https://dennisclarkforcongresscom.wordpress.com/")

# Virginia: campaign sites, and the Virginia Mercury's guide for bios and priorities (in
# its words). Stephen Woll (I, 3rd), Alaha Ahrar (I, 7th) and Joshua Ertle (I, 7th) post
# no issues; Geral Staten (I, 2nd) has only a Facebook page.
VA_MERCURY = lambda slug: lambda note: page(f"Virginia Mercury voter guide: {note}", f"https://virginiamercury.com/voter-guides/contests/{slug}/", READ)  # noqa: E731
VA = {2: VA_MERCURY("2026-general-election-2nd-district"), 3: VA_MERCURY("2026-general-election-3rd-congressional-district"),
      4: VA_MERCURY("2026-general-election-4th-congressional-district"), 5: VA_MERCURY("2026-general-election-5th-congressional-district"),
      6: VA_MERCURY("2026-general-election-6th-congressional-district"), 7: VA_MERCURY("general-election-7th-congressional-district"),
      8: VA_MERCURY("general-election-8th-district"), 9: VA_MERCURY("2026-general-election-9th-congressional-district"),
      10: VA_MERCURY("2026-general-election-10th-congressional-district"), 11: VA_MERCURY("2026-general-election-11th-congressional-district")}
ABORTION_AD = "To end abortion, we too must show the victims."
cand("VA-H-02", "VA-H-02:baker", "J. Matt Baker", "I", "Retired Marine Corps colonel who says he would act as a conduit between Republicans and Democrats.",
     ("def-15", -1, VA[2]("Baker would advocate ending the war in Iran"), None),
     officialSite="https://www.mattbakerindependent.com/")
cand("VA-H-03", "VA-H-03:rivera", "Edwin Rivera", "R", "Army veteran who served several combat tours in the Middle East; a father of seven.")
cand("VA-H-03", "VA-H-03:gaines", "Makiba Gaines", "I", "Civil rights attorney.")
cand("VA-H-04", "VA-H-04:murray", "Robert Murray", "R", "Retired IT professional who consulted for public and private organizations.",
     ("def-08", -2, site("Robert Murray", "https://www.murrayforcongress.com/")("Murray would bring overseas troops home by 2032"), "Overseas military brought back home by 2032."))
cand("VA-H-04", "VA-H-04:bell", "Joan Bell", "I", "Anti-abortion activist arrested some 200 times at demonstrations.",
     ("soc-04", 2, site("Joan Bell", "https://joan.vote/")("Bell’s campaign is built on ending abortion"), ABORTION_AD))
cand("VA-H-05", "VA-H-05:harvey", "Cooke Harvey", "I", "Carpenter.",
     ("gov-01", 1, VA[5]("Harvey highlights term limits"), None),
     ("gov-11", 1, VA[5]("Harvey highlights campaign finance reform"), None))
cand("VA-H-06", "VA-H-06:macy", "Beth Macy", "D", "Author of “Dopesick” and a Roanoke Times reporter for 25 years.",
     ("hea-06", 1, site("Beth Macy", "https://bethmacyforcongress.com/")("Macy would expand access to mental health care"), "Beth is running to make life affordable again for working families, expand access to health and mental health care, invest in rural communities"))
OLLIVANT = site("Doug Ollivant", "https://www.dougforvirginia.com/")
cand("VA-H-07", "VA-H-07:ollivant", "Doug Ollivant", "R", "Retired Army officer from Culpeper.",
     ("ene-02", 1, OLLIVANT("Ollivant would center energy policy on small modular reactors and natural gas"), "I support a common sense all-of-the-above approach, with small modular nuclear reactors and natural gas at the center."),
     ("ene-03", 1, OLLIVANT("Ollivant puts natural gas at the center of energy policy"), None),
     ("ene-01", 1, OLLIVANT("Ollivant would add wind, rooftop solar and hydropower"), "By pairing these strengths with American innovation in wind, rooftop solar, hydropower, and carbon capture"),
     ("edu-03", 1, OLLIVANT("Ollivant would promote the skilled trades"), "It also means protecting parental rights, promoting skilled trades"))
cand("VA-H-07", "VA-H-07:terry", "Randall Terry", "I", "Founder of the anti-abortion group Operation Rescue.",
     ("soc-04", 2, site("Randall Terry", "https://www.terry.vote/")("Terry’s campaign is built on ending abortion"), ABORTION_AD))
LOPEZ = site("Taner Demirci Lopez", "https://lopezforva.com/")
cand("VA-H-07", "VA-H-07:lopez", "Taner Demirci Lopez", "L", None,
     ("imm-02", 1, LOPEZ("Lopez proposes legal work status for undocumented immigrants already here"), "creating a lawful, vetted, accountable process for undocumented immigrants already here to come out of the shadows, work legally, pay taxes"),
     ("imm-01", 1, LOPEZ("Lopez would restore control at the border"), "would restore control at the border"),
     ("def-03", 1, LOPEZ("Lopez would guarantee veterans community care after 28 days"), "if the VA cannot provide a veteran with an appointment within 28 days, the veteran would have access to community care"))
SABIO = site("Tony Sabio", "https://sabioforcongress.com/")
cand("VA-H-08", "VA-H-08:sabio", "Tony Sabio", "R", "Navy veteran.",
     ("hea-04", 1, SABIO("Sabio would let people buy insurance plans nationwide"), "Purchase insurance plans nationwide"),
     ("hea-08", 1, SABIO("Sabio would guarantee coverage despite illness or job loss"), "No American will be permanently denied access to healthcare because of job loss, illness, financial hardship, or a lapse in coverage."),
     ("agr-03", 1, VA[8]("Sabio names expanding domestic manufacturing as a key goal"), None))
cand("VA-H-08", "VA-H-08:arnoldi", "Shelly Arnoldi", "L",
     "Navy veteran and licensed professional engineer who has managed military, Defense Department school and Smithsonian facilities projects for 27 years.",
     ("eco-08", 1, site("Shelly Arnoldi", "https://shellyarnoldi4va.org/")("Arnoldi would cut taxes and red tape on small businesses"), "Cut taxes and red tape that hurt small businesses so our local economy can thrive."),
     ("gov-01", 1, VA[8]("Arnoldi’s priorities include term limits"), None))
POWERS = site("Joy Powers", "https://www.joyforva.com/")
cand("VA-H-09", "VA-H-09:powers", "Joy Powers", "D",
     "Bedford County cattle farmer who ran her family’s farm equipment dealership; a former House of Delegates candidate.",
     ("hea-06", 1, POWERS("Powers would expand mental health and addiction treatment"), "Joy will protect rural hospitals, expand mental health and addiction treatment, and grow the healthcare workforce"),
     ("hou-09", 1, POWERS("Powers would rebuild roads and broadband"), "rebuild infrastructure like roads and broadband"),
     ("hou-01", 1, POWERS("Powers would build affordable homes"), "Joy will fight to lower costs by holding corporations accountable, building affordable homes"))
BECKWITH = site("Dave Beckwith", "https://www.beckwithforcongress.com/")
cand("VA-H-10", "VA-H-10:beckwith", "Dave Beckwith", "R",
     "Air Force veteran (30 years) and former deputy assistant secretary of defense; a two-time cancer survivor who lost the 2022 Republican primary for this seat.",
     ("eco-07", 1, BECKWITH("Beckwith would eliminate wasteful spending"), "He will be a steadfast voice for eliminating wasteful spending"),
     ("ene-02", 2, BECKWITH("Beckwith wants a bold reinvestment in nuclear power"), "including a bold reinvestment in nuclear power to lower costs and create good jobs"),
     ("ene-09", -1, BECKWITH("Beckwith would end market-distorting energy subsidies"), "an all-of-the-above energy strategy that ends market-distorting subsidies"),
     ("edu-06", 1, BECKWITH("Beckwith supports school choice"), "parental rights & school choice"),
     ("edu-03", 1, BECKWITH("Beckwith would expand vocational training and apprenticeships"), "work to expand access to vocational training and apprenticeships"),
     ("def-03", 1, BECKWITH("Beckwith would fight for veterans’ timely health care"), "Dave will fight for the veterans who defended this country, ensuring they get timely healthcare, real support for their mental health"))
MALIK = site("Ahsen Malik", "https://ahsenmalik.com/")
cand("VA-H-10", "VA-H-10:malik", "Ahsen Malik", "I", "Middle school teacher and son of an immigrant.",
     ("soc-03", 0, MALIK("Malik supports abortion rights early in pregnancy and limits late in pregnancy"), "I am pro-choice in the first trimester and pro-life in the last trimester"),
     ("ene-01", 2, MALIK("Malik supports a climate bill that aggressively expands clean energy"), "I support a bipartisan climate bill that aggressively expands clean and renewable energy"),
     ("agr-05", 1, MALIK("Malik would invest in mineral supply chains"), "invests in the mineral supply chains and domestic manufacturing capacity"))
cand("VA-H-11", "VA-H-11:purves", "Arthur Purves", "R", "President of the Fairfax County Taxpayers Alliance for 29 years.",
     ("eco-07", 1, site("Arthur Purves", "https://www.votepurves.org/")("Purves would cut federal spending by reducing chronic disease"), "Soaring government spending is a crisis"))
cand("VA-H-11", "VA-H-11:blais", "Dianne Blais", "G",
     "A former co-president of the League of Women Voters and the American Association of University Women; has lived in Fairfax County since eighth grade.",
     ("def-07", 1, VA[11]("Blais names ending wars as a priority"), None))

# Georgia: campaign sites (bios partly from the Georgia Recorder's guide). James Duffie
# (R, 4th), Kelly Esti (D, 8th) and Caitlyn Gegen (D, 9th) post no issues.
KINGSTON = site("Jim Kingston", "https://www.jimkingston.org/")
cand("GA-H-01", "GA-H-01:kingston", "Jim Kingston", "R", "Insurance executive; son of former Rep. Jack Kingston, who held the seat from 1993 to 2015.",
     ("eco-02", 1, KINGSTON("Kingston would lower taxes across the board"), "I will always fight to lower taxes across the board so families keep more of what they earn"),
     ("eco-07", 1, KINGSTON("Kingston would rein in spending and return to balanced budgets"), "Washington’s addiction to spending is bankrupting future generations."),
     ("hea-03", -1, KINGSTON("Kingston supports Medicaid work requirements"), "I support work requirements for able-bodied adults and no Medicaid handouts to illegal aliens."))
HOLLOWELL = site("Amanda Hollowell", "https://www.amandaforga.com/")
cand("GA-H-01", "GA-H-01:hollowell", "Amanda Hollowell", "D", "Chief of campaigns at Color of Change, a racial justice organization.",
     ("hea-06", 1, HOLLOWELL("Hollowell would expand mental health services and protect Medicaid"), "Amanda will fight to fully fund rural hospitals, expand mental health services, and protect Medicaid from harmful cuts."),
     ("hea-03", 1, HOLLOWELL("Hollowell faults Georgia for refusing to expand Medicaid"), None),
     ("hou-10", 1, HOLLOWELL("Hollowell would invest in flood protection and resilient infrastructure"), "Amanda will champion federal investment in flood protection, resilient infrastructure, and clean energy job creation."),
     ("ene-01", 1, HOLLOWELL("Hollowell would invest in clean energy jobs"), None),
     ("soc-12", 1, HOLLOWELL("Hollowell would defend LGBTQ+ rights"), "Amanda will defend LGBTQ+ rights, fight for reproductive freedom"),
     ("soc-03", 1, HOLLOWELL("Hollowell would fight for reproductive freedom"), None),
     ("soc-02", 1, HOLLOWELL("Hollowell would fight discrimination"), "Every Georgian deserves to live free from discrimination, no matter who they are or who they love."),
     ("eco-11", 1, HOLLOWELL("Hollowell supports paid leave"), "Paid Leave & Family Support"))
DAY = site("Matt Day", "https://www.votemattday.com/")
cand("GA-H-02", "GA-H-02:day", "Matt Day", "R", "Grew up in a blue-collar family in Southeast Georgia; studied at South Georgia College and East Central Tech.",
     ("eco-07", 2, DAY("Day would balance the budget by cutting the size of government"), "Balancing the Budget is as easy, we just need to cut the size of the government back."),
     ("soc-04", 2, DAY("Day will fight for the unborn"), "Matt will fight for the unborn."),
     ("def-10", 1, DAY("Day would send only American-made goods as foreign aid"), "No more Pallets of Cash for foreign Aid."))
KELLER = site("Maura Keller", "https://maurakeller.com/")
cand("GA-H-03", "GA-H-03:keller", "Maura Keller", "D",
     "Army veteran (26 years, from enlisted military police officer to lieutenant colonel) who later worked in health care at the Atlanta VA.",
     ("eco-03", 1, KELLER("Keller would raise the minimum wage"), "She’s committed to raising the minimum wage, advocating for higher paying jobs, and fixing social security."),
     ("def-03", 1, KELLER("Keller puts veterans’ care and benefits first"), "Maura’s first thoughts are with supporting veteran care and benefits programs"))
cand("GA-H-05", "GA-H-05:salvesen", "John Oscar Salvesen", "R", None,
     ("gov-02", 1, site("John Salvesen", "https://www.bongo4congress.com/")("Salvesen pledges to own no stock, calling it a conflict of interest"), "If I am elected, I promise I will own no stock, believing it as a conflict of interest."))
KOZYCKI = site("Tony Kozycki", "https://kozyckiforcongress.com/")
cand("GA-H-07", "GA-H-07:kozycki", "Tony Kozycki", "D", "Combat veteran (three deployments, three Air Medals) and attorney.",
     ("gov-02", 2, KOZYCKI("Kozycki would ban congressional insider trading on day one"), "Tony will vote to ban congressional insider trading on day one"),
     ("imm-01", 1, KOZYCKI("Kozycki wants a secure border and a working system"), "We need a secure border and a system that actually works."),
     ("def-02", 1, KOZYCKI("Kozycki would stand by allies"), "America is strongest when we lead with strength and stand by our allies."))
GAINES = site("Houston Gaines", "https://houstongaines.com/")
cand("GA-H-10", "GA-H-10:gaines", "Houston Gaines", "R", "State representative since 2019; director of business development at a Watkinsville engineering firm.",
     ("imm-08", 1, GAINES("Gaines passed a state law requiring cooperation with ICE"), "His legislation ensured total cooperation with ICE"),
     ("imm-01", 1, GAINES("Gaines says deportations must continue and the border stay secure"), "Deportations must continue, and the border must stay secure."),
     ("cri-01", 2, GAINES("Gaines added hundreds of millions for law enforcement in Georgia"), "We need to invest in public safety, help law enforcement and crack down on crime."),
     ("eco-07", 2, GAINES("Gaines would cut spending and taxes"), "Cut spending and cut taxes."))
DELANCY = site("Pam DeLancy", "https://www.votepamdelancy.com/")
cand("GA-H-10", "GA-H-10:delancy", "Pam Delancy", "D",
     "Retired Army colonel (39 years, including six at the Pentagon on medical readiness) and registered nurse; a cancer survivor.",
     ("hea-06", 1, DELANCY("DeLancy wants more robust mental health policies"), "I will address the need for more robust mental health policies"),
     ("def-03", 1, DELANCY("DeLancy would protect veterans’ health benefits"), "I will address the threat of veterans earned healthcare benefits being diminished or abolished."),
     ("imm-01", 1, DELANCY("DeLancy wants a secure border and a humane system"), "We need a secure border and a functional immigration system"))
cand("GA-H-11", "GA-H-11:harden", "Chris Harden", "D", "Woodstock defense attorney who has worked in juvenile courts across North Georgia; calls himself a moderate Democrat.")
COWAN = site("John Cowan", "https://www.cowanforcongress.com/")
cand("GA-H-11", "GA-H-11:cowan", "John Cowan", "R",
     "Neurosurgeon and small business owner from Bartow County; lost the 2020 Republican runoff in the 14th District to Marjorie Taylor Greene.",
     ("gov-02", 1, COWAN("Cowan would ban congressional stock trading"), "Clean up Washington by banning Congressional stock trading, strengthening ethics rules, and fighting for term limits"),
     ("gov-09", 1, COWAN("Cowan would strengthen ethics rules"), None),
     ("gov-01", 1, COWAN("Cowan would fight for term limits"), None),
     ("eco-02", 1, COWAN("Cowan would deliver tax relief for families"), "delivering meaningful tax relief for families and small businesses"))
cand("GA-H-12", "GA-H-12:smith", "Ceretta Smith", "D", "Army medic, federal labor leader and Grovetown city councilwoman.",
     ("hea-06", 1, site("Ceretta Smith", "https://cerettaforgeorgia.com/")("Smith would expand counseling and crisis services"), "Mental health support: expand counseling and crisis services."))
cand("GA-H-13", "GA-H-13:clark", "Jasmine Clark", "D",
     "State representative since 2019 and assistant clinical professor at Emory, with a Ph.D. in microbiology and molecular genetics.")
CHAVEZ = site("Jonathan Chavez", "https://jonathanchavezforcongress.com/")
cand("GA-H-13", "GA-H-13:chavez", "Jonathan Chavez", "R",
     "Air Force veteran (23 years, including deployments to Iraq) with master’s degrees from Harvard and Johns Hopkins.",
     ("hea-03", 1, CHAVEZ("Chavez supports Medicaid expansion and rural telehealth"), "Expand affordable options—Medicaid expansion and rural telehealth—so care is closer and costs are lower."),
     ("hou-09", 1, CHAVEZ("Chavez wants reliable broadband"), "Safer transit, reliable broadband, and classrooms that prepare students for real opportunity."))
HARRIS_GA = site("Shawn Harris", "https://www.shawnforgeorgia.com/")
cand("GA-H-14", "GA-H-14:harris", "Shawn Harris", "D",
     "Retired Army brigadier general and Polk County cattle farmer; ran against Marjorie Taylor Greene in 2024 and in this year’s special election.",
     ("gov-01", 2, HARRIS_GA("Harris would limit House members to three terms"), "Three 2-year terms in the US House"),
     ("gov-02", 2, HARRIS_GA("Harris supports the ETHICS Act’s ban on members owning or trading stocks"), "Support the ETHICS Act which bans members, spouses and dependent children from owning or trading individual stocks"),
     ("gov-09", 2, HARRIS_GA("Harris wants independent ethics investigations that continue after a member resigns"), "Investigations should be run by independent third parties who can continue the investigation even if an official resigns."))

# Kentucky: campaign sites (bios partly from the Kentucky Lantern's guide)
WILLIAMS_KY = site("Drew Williams", "https://www.williamsforky.com/")
cand("KY-H-01", "KY-H-01:williams", "Drew Williams", "D",
     "Has worked in family businesses in Western Kentucky; with his wife, revived the Tater Day festival in Benton.",
     ("eco-12", 2, WILLIAMS_KY("Williams proposes a smooth income tax scale rising from 1% at $100,000 to 35% at $1 million"), "Tax rates increase smoothly from 1% at $100,000 to 35% at $1 million"),
     ("eco-02", 2, WILLIAMS_KY("Williams would exempt about the first $100,000 of income from federal income tax"), "Ensures low- and middle-income families owe nothing on basic living income"),
     ("eco-01", 2, WILLIAMS_KY("Williams would tax very large unrealized investment gains"), "you should not be able to legally pay zero in taxes just because you never sell anything"),
     officialSite="https://www.williamsforky.com/")
WINGFIELD = site("Megan Wingfield", "https://meganwingfieldforcongress.com/")
cand("KY-H-02", "KY-H-02:wingfield", "Megan Wingfield", "D", "Mechanic and activist from Bowling Green.",
     ("gov-01", 2, WINGFIELD("Wingfield signed the U.S. Term Limits pledge"), "I’ve proudly signed the U.S. Term Limits pledge"),
     ("hea-01", 2, WINGFIELD("Wingfield supports Medicare for All"), "Expanding affordable housing programs and supporting Medicare for All to ease financial burdens."),
     ("hou-01", 1, WINGFIELD("Wingfield would expand affordable housing programs"), None),
     ("eco-03", 1, WINGFIELD("Wingfield would raise the minimum wage and protect union organizing"), "Raising the minimum wage and protecting gig workers and union organizing efforts."),
     ("eco-09", 1, WINGFIELD("Wingfield would protect union organizing"), None),
     ("eco-12", 1, WINGFIELD("Wingfield wants corporations and the ultra-wealthy to pay their fair share"), "Pushing for tax equity—where corporations and the ultra-wealthy pay their fair share."),
     ("soc-03", 1, WINGFIELD("Wingfield would protect the right to choose"), "Protect reproductive freedom and the right to choose."),
     ("soc-07", 1, WINGFIELD("Wingfield supports universal pre-K and affordable child care"), "Universal Pre-K and affordable childcare."),
     ("def-03", 1, WINGFIELD("Wingfield would expand VA care"), "Expand access to VA care and mental health services."),
     ("soc-10", 2, WINGFIELD("Wingfield would codify same-sex marriage"), "Codifying same-sex marriage in federal law to protect love and families."),
     ("soc-12", 2, WINGFIELD("Wingfield supports nationwide protections for transgender people"), "Nationwide protections for transgender and non-binary individuals"))
cand("KY-H-02", "KY-H-02:loecken", "Thomas Loecken", "I", "Retired civil service worker who owns a farm.")
cand("KY-H-03", "KY-H-03:rodriquez", "Maria Rodriquez", "R",
     "Trauma nurse and business owner in Louisville; came to the U.S. from Cuba at 21 after an 11-year asylum process and became a citizen.")
GALLREIN = site("Ed Gallrein", "https://www.edgallrein.com/")
cand("KY-H-04", "KY-H-04:gallrein", "Ed Gallrein", "R", "Former Navy SEAL and Shelby County farmer; ran for the state Senate in 2024.",
     ("eco-07", 1, GALLREIN("Gallrein would stop reckless spending"), "stop the reckless spending that has driven up inflation"),
     ("imm-01", 2, GALLREIN("Gallrein would finish the wall"), "finish the wall, fully fund Border Patrol & ICE"),
     ("imm-08", 2, GALLREIN("Gallrein would fully fund Border Patrol and ICE"), None),
     ("def-01", 1, GALLREIN("Gallrein would rebuild the military"), "rebuild our military to support our national security"),
     ("soc-04", 2, GALLREIN("Gallrein is anti-abortion"), "Gallrein is Pro-Life!"))
STRANGE = site("Melissa Strange", "https://strangeforky.com/")
cand("KY-H-04", "KY-H-04:strange", "Melissa Strange", "D",
     "Supply chain director for a global nutrition and agribusiness company, with 27 years in food manufacturing; lives in Erlanger.",
     ("eco-10", -1, STRANGE("Strange would end inflationary tariffs"), "end inflationary tariffs"),
     ("hea-03", 1, STRANGE("Strange would protect and expand Medicare and Medicaid"), "Protect and expand Medicare, Medicaid, and Social Security."),
     ("imm-01", 1, STRANGE("Strange would increase border security to fight the drug crisis"), "Fight the drug crisis through increased border security, expanded access to treatment and rehab"),
     ("edu-03", 1, STRANGE("Strange would invest in career and technical education"), "Invest in career and technical education"),
     ("eco-09", 1, STRANGE("Strange supports unions"), "Support KY Workers and Unions"))
cand("KY-H-04", "KY-H-04:todd", "Jeremy Todd", "L", "Business manager who has led teams of up to 300 people; entered after Rep. Thomas Massie lost the primary.",
     ("def-07", 1, site("Jeremy Todd", "https://jeremy-todd.com/")("Todd calls himself the anti-war, anti-spending candidate"), "anti-war, anti-spending, anti-establishment"),
     ("eco-07", 1, site("Jeremy Todd", "https://jeremy-todd.com/")("Todd calls himself the anti-spending candidate"), None))
PILLERSDORF = site("Ned Pillersdorf", "https://nedforcongress.com/")
cand("KY-H-05", "KY-H-05:pillersdorf", "Ned Pillersdorf", "D",
     "Prestonsburg attorney who represented thousands of Eastern Kentuckians who lost disability benefits after the Eric Conn fraud.",
     ("hea-03", 1, PILLERSDORF("Pillersdorf opposes cutting Medicaid and Medicare"), None),
     ("eco-01", 1, PILLERSDORF("Pillersdorf opposes a tax break for the billionaire class"), None))
cand("KY-H-05", "KY-H-05:wein", "Mikel Wein", "I", "Lives in Letcher County in a house that has been in his family for generations.")
cand("KY-H-05", "KY-H-05:serrano", "Gerardo Serrano", "I", "Ran for Congress before as a Republican against Rep. Hal Rogers.")
cand("KY-H-06", "KY-H-06:bowman", "Jay Bowman", "I", "Business owner who ran as a write-in presidential candidate in some states in 2024.")
LYNCH = site("Pete Lynch", "https://petelynchforkentucky.com/")
cand("KY-H-06", "KY-H-06:lynch", "Pete Lynch", "Kentucky",
     "University of Kentucky political science lecturer with a Ph.D. in American politics; calls himself an economic populist.",
     ("gov-11", 2, LYNCH("Lynch would tax election spending above $2,500 per donor at 100%"), "Tax every dollar spent on elections above $2,500 per individual or corporation per calendar year at 100%"),
     ("gov-03", 1, LYNCH("Lynch would make all political spending transparent"), "Make all campaign contributions and political spending fully transparent"),
     ("gov-02", 2, LYNCH("Lynch would ban members from trading stocks"), "Ban all members of Congress from buying or selling individual stocks"),
     ("hea-01", 2, LYNCH("Lynch supports Medicare for All"), "Provide universal healthcare coverage for all Americans"),
     ("hou-02", 2, LYNCH("Lynch would ban hedge fund ownership of single-family homes"), "Ban foreign and hedge fund ownership of single-family homes"),
     ("hou-06", 1, LYNCH("Lynch would cap rent increases in corporate-owned rentals"), "Cap rent increases for corporate-owned rental properties"))

# Oklahoma: the Oklahoma Voice's guide (bios and priorities in its words) and campaign
# sites. Rocco Bonacci (I, 4th) has only a Facebook page; Austin Nieves (I, 5th) nothing.
OK_VOICE = lambda d: lambda note: page(f"Oklahoma Voice voter guide: {note}", f"https://oklahomavoice.com/voter-guides/contests/u-s-representative-district-{d}-2026-general/", READ)  # noqa: E731
cand("OK-H-01", "OK-H-01:tedford", "Mark Tedford", "R", "State representative and Tulsa businessman.",
     ("eco-07", 1, OK_VOICE(1)("Tedford would work to balance the federal budget"), None),
     ("imm-01", 1, OK_VOICE(1)("Tedford would combat illegal immigration"), None),
     ("agr-03", 1, OK_VOICE(1)("Tedford would rebuild American industry"), None))
cand("OK-H-01", "OK-H-01:croisant", "John Croisant", "D", "Former teacher and local businessman.")
cand("OK-H-02", "OK-H-02:wade", "Brandon Wade", "D", "Third-generation union worker; vice president of IUOE Local 351 in Bartlesville.",
     ("soc-03", 1, OK_VOICE(2)("Wade would protect women’s health care choices"), None),
     ("def-03", 1, site("Brandon Wade", "https://brandon4congress.com/")("Wade wants better VA access and mental health care"), "Better VA access, mental health care, and support that doesn’t stop."))
cand("OK-H-02", "OK-H-02:hopkins", "Ronnie Hopkins", "I", None,
     officialSite="https://hopkinsforcongress.wixsite.com/ronnie-hopkins-for-c")
cand("OK-H-03", "OK-H-03:byrd", "Suzie Byrd", "D", "Former Oklahoma State athlete and Enid News & Eagle reporter.",
     ("hea-01", 1, OK_VOICE(3)("Byrd supports universal health care"), None),
     ("def-01", -1, OK_VOICE(3)("Byrd won’t vote to increase defense spending"), None))
cand("OK-H-04", "OK-H-04:jacob", "Mitchell Jacob", "D",
     "Army veteran (cryptologic linguist, deployed to Syria) and public defender; formerly a stockbroker and banker.")
cand("OK-H-05", "OK-H-05:nelson", "Jena Nelson", "D", "Educator for more than 16 years; most recently led the nonprofit Oklahoma Faith Network.",
     ("hea-09", 1, OK_VOICE(5)("Nelson would expand access to preventive care"), None))
HENRI = site("Robert Henri", "https://projectduecourse.org/")
cand("OK-H-05", "OK-H-05:henri", "Robert Henri", "I", None,
     ("gov-02", 1, HENRI("Henri objects to members trading stocks on inside information"), "Congress still trades stocks on information you'll never see"),
     ("gov-12", 1, HENRI("Henri wants transparency on who funds officials and how money is spent"), "People deserve to know what their government officials are saying, who's funding them and how the tax payers money is being spent."),
     ("gov-09", 1, OK_VOICE(5)("Henri would bring ethics rules to the Supreme Court and stop hidden lobbying"), None))

# Wisconsin: campaign sites (bios partly from the Wisconsin Examiner's guide). Alexander
# Kent (I, 3rd) has nothing; Matthew Arndt's (G, 6th) and Rick Crosson's (D, 8th) sites
# list no issues.
cand("WI-H-03", "WI-H-03:provance", "Rustin Provance", "I", "HVAC-R technician who moved to Wisconsin from Minnesota.")
ROGERS_WI = site("Tim Rogers", "https://www.rogersforwisconsin.com/")
cand("WI-H-04", "WI-H-04:rogers", "Tim Rogers", "R", "Milwaukee native who has run for this seat every cycle since 2018.",
     ("edu-06", 2, ROGERS_WI("Rogers supports universal school choice and vouchers"), "I support School Choice and School Voucher programs."),
     ("cri-04", 2, ROGERS_WI("Rogers supports harsh punishment for violent criminals"), "I support harsh punishment for violent criminals"))
BURKS = site("Arthur Burks", "https://www.burks4congress.com/")
cand("WI-H-04", "WI-H-04:burks", "Arthur Burks", "I", "Milwaukee business owner.",
     ("hea-06", 1, BURKS("Burks would expand community clinics and mental health facilities"), "Arthur supports expanding community clinics and mental health facilities"),
     ("cri-07", 1, BURKS("Burks would fund violence interruption programs"), "funding for violence interruption programs"),
     ("edu-01", 1, BURKS("Burks would seek federal money for Milwaukee school buildings"), "Arthur will push for federal funding to upgrade MKE school infrastructure"),
     ("hou-01", 1, BURKS("Burks would seek federal subsidies for affordable housing"), "Arthur will fight for federal subsidies to expand Milwaukee's affordable housing units"),
     ("hou-06", 1, BURKS("Burks would protect residents from predatory landlords"), "protect residents from predatory landlords and displacement"))
cand("WI-H-05", "WI-H-05:beck", "Andrew Beck", "D", "West Bend resident who has worked in product development at GE Healthcare and as an MRI technologist.",
     ("soc-03", 2, site("Andy Beck", "https://www.beckforcongress.com/")("Beck wants consistent reproductive rights protections in every state"), "Women must have the right to make their own decisions on reproductive health"))
SMITH_WI = site("Brad Smith", "https://www.bradsmithforcongress.com/")
cand("WI-H-06", "WI-H-06:smith", "Brad Smith", "D", "Army National Guard veteran (2000–2008) and management consultant.",
     ("eco-03", 1, SMITH_WI("Smith would raise the minimum wage"), "Raise minimum wage, expand apprenticeships"),
     ("edu-03", 1, SMITH_WI("Smith would expand apprenticeships"), None),
     ("hea-01", 1, SMITH_WI("Smith calls affordable health care a right"), "Affordable, Usable Healthcare as a Right"),
     ("hea-08", 1, SMITH_WI("Smith would protect coverage for preexisting conditions"), "protect coverage for pre-existing conditions"),
     ("eco-09", 1, SMITH_WI("Smith would protect the right to organize and restore prevailing wage"), "Restore prevailing wage, strengthen Project Labor Agreements, and protect the right to organize."),
     ("imm-09", 1, SMITH_WI("Smith wants year-round legal workforce solutions for farms"), "year-round legal workforce solutions"),
     ("hou-09", 1, SMITH_WI("Smith wants broadband on every farm"), "broadband on every farm"))
THUROW = site("Mike Thurow", "https://www.thurowforcongress.com/")
cand("WI-H-06", "WI-H-06:thurow", "Michael Thurow", "I", "Union fire captain and Navy veteran from Mequon; a father of four.",
     ("eco-04", 2, THUROW("Thurow would break up monopolies in the food supply chain"), "We must also break up the monopolization of our food supply chains"),
     ("hou-01", 1, THUROW("Thurow would expand affordable housing programs"), "I will fight to expand federal and state affordable housing programs"),
     ("eco-02", 1, THUROW("Thurow wants tax relief for the middle class"), "advocate for tax relief targeted to middle-class families, not billionaires and large corporations"),
     ("hea-02", 2, THUROW("Thurow wants Medicare to negotiate all drug prices"), "Medicare needs to negotiate all drug prices directly."))
FITZGIBBON = site("Elizabeth Fitzgibbon", "https://www.fitzgibbonforcongress.com/")
cand("WI-H-06", "WI-H-06:fitzgibbon", "Elizabeth Fitzgibbon", "I", "Describes herself as a mother, neighbor and advocate.",
     ("eco-07", 1, FITZGIBBON("Fitzgibbon would reduce wasteful spending"), "Elizabeth will fight to reduce wasteful spending"),
     ("gov-12", 1, FITZGIBBON("Fitzgibbon would expose federal spending and insider deals"), "Elizabeth will fight to shine a light on federal spending, agency decisions, conflicts of interest"))
cand("WI-H-06", "WI-H-06:arndt", "Matthew Arndt", "G", "Green Bay native who runs a tax and investing firm.")
cand("WI-H-08", "WI-H-08:crosson", "Rick Crosson", "D", "Army veteran who worked in trucking; a Green Bay School Board member.")

# Utah, the rest: campaign sites (none of these answered Utah News Dispatch)
MONTGOMERY = site("Elias Montgomery", "https://www.eliasmontgomery.com/")
cand("UT-H-01", "UT-H-01:montgomery", "Elias Montgomery", "I", "Policy analyst; a graduate of West Jordan High School and the University of Utah.",
     ("hou-02", 1, MONTGOMERY("Montgomery would discourage institutional purchases of single-family homes"), "Discourage large-scale institutional purchase of single-family homes and prioritize owner-occupants."),
     ("hou-04", 2, MONTGOMERY("Montgomery would legalize missing-middle housing"), 'Legalize and streamline "missing-middle" housing like duplexes, townhomes, and small apartments.'),
     ("eco-06", 1, MONTGOMERY("Montgomery would prioritize infrastructure, water and transit projects"), "Prioritize infrastructure and resilience projects like energy efficiency, water security, and transit."))
cand("UT-H-01", "UT-H-01:west", "Jesse West", "L", "Family law attorney and skier.")
cand("UT-H-02", "UT-H-02:cottam", "Daniel Cottam", "L", "Business owner, bariatric surgeon and consultant.")
cand("UT-H-03", "UT-H-03:udell", "Kent Udell", "D",
     "Mechanical engineer and former professor and researcher at UC Berkeley and the University of Utah; served on federal advisory committees.")
cand("UT-H-03", "UT-H-03:hooslyn", "Adonis Hooslyn", "I", "Raised in Ogden in a working-class immigrant family; holds degrees in film and business.",
     ("hea-01", 2, site("Adonis Hooslyn", "https://www.hooslynforhouse.com/")("Hooslyn advocates Medicare for All"), "Dealing with health issues in my 20s has strongly pushed me to advocate for Medicare for All."))

# Kansas: campaign sites (bios partly from the Kansas Reflector's guide). Steven Jacob
# (L, 1st) has only a Facebook page.
cand("KS-H-01", "KS-H-01:reinhold", "Lauren Reinhold", "D", "Lawrence attorney who formerly worked for the Social Security Administration.")
cand("KS-H-01", "KS-H-01:jacob", "Steven Jacob", "L",
     "Retired City of Lawrence worker; ran for the Douglas County Commission in 2022 and 2024 and the Lawrence City Commission in 2025.")
cand("KS-H-02", "KS-H-02:coover", "Don Coover", "D",
     "Galesburg veterinarian, rancher and owner of a beef cattle genetics company; a former Army captain and pilot.")
HAUER = site("John Hauer", "https://www.hauerforcongress.com/")
cand("KS-H-02", "KS-H-02:hauer", "John Hauer", "L", "Army veteran from Topeka.",
     ("eco-12", -2, HAUER("Hauer would eliminate the federal income tax"), "Eliminate federal income tax and drastically cut spending."),
     ("eco-07", 2, HAUER("Hauer would drastically cut spending"), None),
     ("def-10", 2, HAUER("Hauer would stop sending tax dollars overseas"), "No more sending tax dollars overseas, every dollar stays here."))
JENKINS = site("Eric Jenkins", "https://ericjenkinsforkansas.com/")
cand("KS-H-03", "KS-H-03:jenkins", "Eric Jenkins", "R",
     "Retired Army colonel (34 years) from Shawnee; former Shawnee City Council member (2015–2023) who worked for FEMA.",
     ("eco-07", 1, JENKINS("Jenkins would cut wasteful spending and balance the books"), "Eric will fight to cut wasteful spending, balance the books, and protect taxpayers."),
     ("eco-02", 1, JENKINS("Jenkins wants lower taxes"), "Lower taxes, affordable energy, and real border security"),
     ("imm-01", 1, JENKINS("Jenkins would support resources to secure the border"), "Eric will support the resources and policies needed to protect our communities."))
cand("KS-H-03", "KS-H-03:hohe", "Steven Hohe", "L",
     "Air Force veteran (11 years) who has worked in trades and sales; ran for this seat in 2016, 2020 and 2022.")
cand("KS-H-04", "KS-H-04:tyndell", "Katy Tyndell", "D",
     "Works in her family’s Wichita oil and gas company; co-founder of the bipartisan nonprofit Leading Kansas and former attorney for the National Congress of American Indians.")
CRANMER = site("Drew Cranmer", "https://drew4kansas.com/")
cand("KS-H-04", "KS-H-04:cranmer", "Drew Cranmer", "L", "Wichita data engineer and founder of a church-management software company.",
     ("def-04", 2, CRANMER("Cranmer opposes wars launched without a congressional vote"), "No to unconstitutional wars launched without a congressional vote."),
     ("soc-08", 1, CRANMER("Cranmer opposes government cameras tracking drivers"), "No to government cameras cataloguing where you drive"),
     ("eco-07", 1, CRANMER("Cranmer wants Congress to balance its books"), "no to a Congress too cowardly to balance its own books"),
     ("cri-09", -2, CRANMER("Cranmer opposes the death penalty"), "And no to a government that claims the authority to execute its own citizens in your name"))

# Arkansas: campaign sites (bios partly from the Arkansas Advocate's guide)
GREEN_AR = site("Terri Green", "https://terrigreen26.com/")
cand("AR-H-01", "AR-H-01:green", "Terri Green", "D", "Retired pathologist and laboratory medical director.",
     ("eco-03", 1, GREEN_AR("Green would raise the minimum wage"), "Raising the minimum wage so work actually pays."),
     ("hou-09", 1, GREEN_AR("Green wants safe roads, bridges and reliable broadband"), "Strong infrastructure, including safe roads and bridges, reliable broadband, excellent public schools"),
     ("hou-08", 1, GREEN_AR("Green wants safe roads and bridges"), None))
PARSONS = site("Steve Parsons", "https://www.steve-parsons.com/")
cand("AR-H-01", "AR-H-01:parsons", "Steve Parsons", "L", "Retired consultant and economist; the Libertarian nominee here in 2024.",
     ("soc-05", 1, PARSONS("Parsons opposes government intrusion into choices such as smoking marijuana"), "less government intrusion into personal decisions such as whether one uses a seat belt or smokes marijuana"),
     ("def-15", -2, PARSONS("Parsons would end the war in Iran"), "Stop being the puppet of Israel and end the war in Iran"),
     ("def-12", -1, PARSONS("Parsons says the U.S. should stop being Israel’s puppet"), None),
     ("eco-10", -2, PARSONS("Parsons would eliminate trade tariffs"), "Eliminate trade tariffs"),
     ("def-08", -1, PARSONS("Parsons would stop the U.S. being the world police"), "Stop Being the World Charity and the World Police"),
     ("def-10", 1, PARSONS("Parsons would stop the U.S. being the world’s charity"), None),
     ("eco-07", 1, PARSONS("Parsons faults both parties for failing to control spending"), None))
cand("AR-H-03", "AR-H-03:ryerse", "Robb Ryerse", "D",
     "Springdale pastor who started Vintage Fellowship church and co-founded Vortex PAC; ran for the Republican nomination here in 2018.",
     ("gov-04", 1, site("Robb Ryerse", "https://www.robbforcongress.com/")("Ryerse would end gerrymandering"), "I will end gerrymandering, protect voting rights"))
cand("AR-H-03", "AR-H-03:wilson", "Bobby Wilson", "L", "The Libertarian nominee here in 2024.")
cand("AR-H-04", "AR-H-04:russell", "James Russell", "D", "Mental health care provider since 2014; ran for the Democratic nomination for governor in 2022.",
     ("gov-13", -1, site("James Russell", "https://russellforar.com/")("Russell would end Citizens United"), "End Citizens United / UnRig Washington"))

# Texas: campaign sites (the Texas Tribune's guide isn't States Newsroom and wasn't read).
# Sites that render only in a browser (Pearce, Bauman, Sims, Fierro, Jackson, Hart, Peña)
# and those that list no issues (Teixeira, Hook, Barrios, Royal, McMenemy, Haynes'
# headings) give little or nothing yet.
PRINCE = site("Yolanda Prince", "https://yolandaprince.com/")
cand("TX-H-01", "TX-H-01:prince", "Yolanda Prince", "D", None,
     ("eco-03", 2, PRINCE("Prince would raise the minimum wage to at least $15"), "I support raising the minimum wage to at least $15 per hour"),
     ("edu-04", 1, PRINCE("Prince would raise teacher pay and provide universal school meals"), "I support raising teacher pay, protecting public education, expanding special education services, providing universal school meals, and investing in universal pre-kindergarten."),
     ("edu-09", 1, PRINCE("Prince supports universal school meals"), None),
     ("hea-01", 2, PRINCE("Prince supports Medicare for All"), "I support a Medicare for All single-payer healthcare systems, that guarantees health insurance coverage for every American."),
     ("hou-05", 1, PRINCE("Prince would make homeownership easier for first-time buyers"), "I will also work to make homeownership more attainable for first-time buyers"))
TOTH = site("Steve Toth", "https://stevetothforcongress.com/")
cand("TX-H-02", "TX-H-02:toth", "Steve Toth", "R", "State representative and member of the Texas House Appropriations Committee.",
     ("imm-01", 2, TOTH("Toth secured billions in state money to finish the border wall"), "I fought successfully to appropriate billions of dollars toward finishing the wall and investing in critical border security initiatives"),
     ("soc-12", -1, TOTH("Toth wrote the Texas ban on social transitioning of children in schools"), "His landmark legislation banning both Critical Race Theory and the social transitioning of children in Texas schools"))
FINNIE = site("Shaun Finnie", "https://shaunfinnieforcongress.com/")
cand("TX-H-02", "TX-H-02:finnie", "Shaun Finnie", "D", "Businessman with economics, law and Northwestern MBA degrees who grew up on a farm.",
     ("eco-07", 1, FINNIE("Finnie would address the federal debt"), "Address the federal debt to protect the economic futures of our young people."),
     ("hea-05", 1, FINNIE("Finnie would invest in medical and scientific research"), "Invest in public education and in medical and scientific research."),
     ("edu-01", 1, FINNIE("Finnie would invest in public education"), None))
HUNT = site("Evan Hunt", "https://www.electevanhunt.com/")
cand("TX-H-03", "TX-H-03:hunt", "Evan Hunt", "D", "Retired Air Force lieutenant colonel and B-1 weapons systems officer with combat deployments; a business leader.",
     ("eco-10", -1, HUNT("Hunt says emergency powers shouldn’t be used to raise tariffs"), "Emergency powers should not be invoked to raise taxes or tariffs"),
     ("hea-07", 1, HUNT("Hunt would keep the ACA subsidies until there is a better plan"), "The ACA subsidies shouldn’t be expired until we have a better plan."),
     ("edu-06", -2, HUNT("Hunt is firmly against vouchers"), "I’m firmly against voucher initiatives which will inevitably harm public schools"),
     ("edu-01", 1, HUNT("Hunt would fully fund public schools and promote local control"), "That means fully funding our public schools, promoting local control, and keeping politics out of the classroom."),
     ("edu-04", 1, HUNT("Hunt supports merit-informed teacher pay raises"), "I support reasonable, merit-informed increases in teacher pay"),
     ("imm-01", 1, HUNT("Hunt wants strong border security with more enforcement resources"), "We need strong, smart border security to keep our communities safe."),
     ("imm-08", 1, HUNT("Hunt wants more resources for enforcement"), "That means more resources for enforcement"))
HOCKETT = site("Chelsey Hockett", "https://chelseyhockettforcongress.com/")
cand("TX-H-05", "TX-H-05:hockett", "Chelsey Hockett", "D", "East Texas mother.",
     ("eco-03", 1, HOCKETT("Hockett would raise the minimum wage and guarantee child care and paid leave"), "Raise the minimum wage, expand Social Security, and guarantee universal childcare and paid leave."),
     ("soc-07", 2, HOCKETT("Hockett would guarantee universal child care"), None),
     ("eco-11", 2, HOCKETT("Hockett would guarantee paid leave"), None),
     ("hea-01", 2, HOCKETT("Hockett would enact Medicare for All"), "Enact Medicare for All."),
     ("edu-01", 1, HOCKETT("Hockett would fully fund Title I, special education and Head Start"), "Protect and fully fund Title I, Special Education, and Head Start."),
     ("edu-06", -2, HOCKETT("Hockett calls vouchers scams that defund public schools"), "our public schools get defunded by voucher scams"))
MINTON = site("Danny Minton", "https://dannyminton.com/")
cand("TX-H-06", "TX-H-06:minton", "Danny Minton", "D", None,
     ("def-04", 2, MINTON("Minton wants Congress to vote before Americans are sent to war"), "Built for a Congress that votes before Americans are sent to war, not presidents who go it alone."),
     ("imm-01", 1, MINTON("Minton wants secure borders and humane immigration"), "Built for secure borders, safe communities, and basic human dignity"),
     ("hea-01", 1, MINTON("Minton says universal, affordable health care works"), "Universal, affordable healthcare actually works."),
     ("edu-06", -1, MINTON("Minton opposes billionaires cashing in on classrooms with vouchers"), "not West Texas Billionaires trying to cash in on our classrooms"))
HALE = site("Alexander Hale", "https://www.halefortexas.com/")
cand("TX-H-07", "TX-H-07:hale", "Alexander Hale", "R", None,
     ("ene-09", -1, HALE("Hale opposes subsidizing competitors of Houston’s energy companies"), "TX-07 deserves a representative who will fight for our energy companies - not subsidize inefficient competitors."),
     ("ene-03", 1, HALE("Hale would champion Houston’s energy industry"), None),
     ("eco-07", 1, HALE("Hale would cut wasteful spending"), "I'll fight to cut wasteful spending"),
     ("cri-01", 1, HALE("Hale would seek federal resources for Houston policing"), "I'll fight to secure Houston the federal resources needed to catch criminals"),
     ("hou-04", 1, HALE("Hale would cut federal red tape on building homes"), "Cut the federal red tape that makes it more expensive to build a house"))
NGABO = site("Espoir Ngabo", "https://www.espoirfortexas.com/")
cand("TX-H-07", "TX-H-07:ngabo", "Espoir Ngabo", "G", None,
     ("hou-01", 1, NGABO("Ngabo would expand affordable housing"), "Congress can step in to expand affordable housing"),
     ("hea-01", 2, NGABO("Ngabo would guarantee free, universal single-payer care"), "guarantee free, universal, single-payer care"),
     ("eco-03", 2, NGABO("Ngabo would raise the minimum wage to $25"), "Raise to $25 Minimum Wage"),
     ("hou-10", 1, NGABO("Ngabo would invest more in flood mitigation"), "Increase Investment in Flood Mitigation"))
cand("TX-H-08", "TX-H-08:steinmann", "Jessica Hart Steinmann", "R",
     "Directed the Justice Department’s Office for Victims of Crime in President Trump’s first term; earlier worked for Sen. Ted Cruz.")
MEALER = site("Alex Mealer", "https://alexandramealer.com/")
cand("TX-H-09", "TX-H-09:mealer", "Alex Mealer", "R", "West Point graduate and combat veteran; former oil and gas banker and small business owner.",
     ("gov-02", 2, MEALER("Mealer would ban members from trading individual stocks"), "I will fight to BAN members of Congress from trading individual stocks while serving in office and implement term limits for Congress."),
     ("gov-01", 1, MEALER("Mealer would implement term limits"), None),
     ("eco-02", 1, MEALER("Mealer would cut taxes"), "I will fight to cut taxes and unnecessary regulations"))
cand("TX-H-09", "TX-H-09:gutierrez", "Leticia Gutierrez", "D", "Community organizer in the district for 15 years; the daughter of farm laborers.",
     ("eco-06", 1, site("Leticia Gutierrez", "https://www.leticiaforcongress.com/")("Gutierrez would prepare infrastructure for storms"), "I want to ensure that our infrastructure is prepared to take care of you"))
cand("TX-H-10", "TX-H-10:gober", "Chris Gober", "R", "Lawyer (Texas A&M, Harvard Law) who worked at the Justice Department and built his own businesses.",
     ("imm-01", 1, site("Chris Gober", "https://www.chrisgober.com/")("Gober would keep the border secure"), "keep our border secure"))
cand("TX-H-10", "TX-H-10:rourk", "Caitlin Rourk", "D", "Army veteran who has worked on energy and deficit policy and led communications at Dell Technologies.")
REYNOLDS_TX = site("Claire Reynolds", "https://clairereynoldsforcongress.org/")
cand("TX-H-11", "TX-H-11:reynolds", "Claire Reynolds", "D", None,
     ("hea-01", 1, REYNOLDS_TX("Reynolds points to Medicare and the VA as single-payer models"), "A single-payer health insurance system may seem out of reach"),
     ("imm-01", 1, REYNOLDS_TX("Reynolds wants a strong border and immigration reform"), "We can have a strong border while reforming our draconian and unwieldy immigration system."),
     ("imm-03", 1, REYNOLDS_TX("Reynolds wants faster legal immigration"), "If good people want to live and work here legally, it shouldn’t take them decades to make that happen."),
     ("soc-03", 1, REYNOLDS_TX("Reynolds wants abortion safe, legal and rare"), "Abortion in Texas should be safe, legal, and rare."),
     ("def-15", -1, REYNOLDS_TX("Reynolds faults Rep. Pfluger’s vote against ending the Iran war"), "Congress has the chance to require the President to end the conflict, and August Pfluger voted no."),
     ("ene-01", 1, REYNOLDS_TX("Reynolds welcomes the growth of green energy jobs"), None))
NAIR = site("Mark Nair", "https://www.marknair.com/platform")
cand("TX-H-13", "TX-H-13:nair", "Mark Nair", "D", None,
     ("eco-10", -1, NAIR("Nair would return tariff power to Congress"), "Tariffs belong in Congress's hands, not the president's."),
     ("soc-08", 2, NAIR("Nair would ban using personal information to train AI"), "I will author comprehensive legislation that will protect privacy, including banning the use of personal information to train AI."),
     ("eco-04", 1, NAIR("Nair would pursue antitrust enforcement"), "I will pursue effective and diligent anti-trust enforcement, limiting the power of corporate interests."),
     ("hea-01", 1, NAIR("Nair would work toward Medicare for All"), "He'll work toward Medicare for All"),
     ("hou-01", 1, NAIR("Nair would expand incentives for affordable housing"), "He'll expand federal incentives for building affordable housing in underserved communities"),
     ("hou-02", 1, NAIR("Nair would restrict corporate purchases of single-family homes"), "restrict corporations from seizing single family homes"),
     ("hou-06", 1, NAIR("Nair would protect renters"), "protect renters from predatory companies"))
BARTIE = site("Thurman Bartie", "https://votebartie.org/")
cand("TX-H-14", "TX-H-14:bartie", "Thurman Bartie", "D", "Former Port Arthur mayor and the first Black justice of the peace in Precinct 8; a minister and educator.",
     ("edu-01", 1, BARTIE("Bartie supports investing in teachers and classrooms"), "I support investment in teachers, modernized classrooms, and pathways to success for every child."),
     ("hou-10", 1, BARTIE("Bartie supports resilient infrastructure for hurricanes and floods"), "I support smart infrastructure, energy reliability, and resilient systems that protect our families and our businesses."))
SHEPARD = site("Casey Shepard", "https://caseyshepardforcongress.com/")
cand("TX-H-17", "TX-H-17:shepard", "Casey Shepard", "D", None,
     ("edu-09", 1, SHEPARD("Shepard would fully fund school breakfast and lunch"), "Strengthen support for families by fully funding SNAP and school breakfast and lunch programs."),
     ("hea-03", 1, SHEPARD("Shepard would restore Medicaid and Medicare support"), "Restore support for Medicaid and Medicare to ensure seniors, families, and people with disabilities receive the care they need."))
cand("TX-H-19", "TX-H-19:sell", "Tom Sell", "R", "Former top aide to Rep. Larry Combest when he chaired the House Agriculture Committee.")
RABLE = site("Kyle Rable", "https://www.rableforwesttexas.com/")
cand("TX-H-19", "TX-H-19:rable", "Kyle Rable", "D", None,
     ("hou-02", 1, RABLE("Rable would limit large corporations’ home purchases"), "I will enact legislation limiting large corporations' ability to purchase homes"),
     ("hou-05", 1, RABLE("Rable supports tax credits for first-time buyers"), "support opportunities for family tax credits for first-time home purchasers"),
     ("soc-07", 1, RABLE("Rable would expand the child care workforce and facilities"), "I will introduce legislation to provide better training to childcare professionals, more robust facilities, and increase the number of workers"),
     ("eco-10", -1, RABLE("Rable opposes the trade war"), "Americans should not bear the brunt of Trump's trade war"))
cand("TX-H-20", "TX-H-20:baez", "Edgardo Rafael Baez", "R", "Army veteran, critical care nurse and attorney for more than two decades.")
cand("TX-H-21", "TX-H-21:teixeira", "Mark Teixeira", "R", "Former MLB All-Star first baseman, including five seasons with the Texas Rangers.")
NEHLS = site("Trever Nehls", "https://www.trevernehlsforcongress.com/")
cand("TX-H-22", "TX-H-22:nehls", "Trever Nehls", "R", "Retired Army Reserve colonel (33 years) who led troops in Iraq and Afghanistan; awarded three Bronze Stars.",
     ("imm-01", 1, NEHLS("Nehls would secure the border"), "Secure the Border and Enforce Immigration Laws"),
     ("cri-01", 1, NEHLS("Nehls would fund law enforcement"), "Fund & Support Law Enforcement"),
     ("edu-06", 1, NEHLS("Nehls would empower parental choice"), "Protect Our Children and Empower Parental Choice"),
     ("hou-10", 1, NEHLS("Nehls would focus on flood mitigation"), "Focusing On Critical Infrastructure: Mobility, Flood Mitigation"))
cand("TX-H-22", "TX-H-22:greene-scott", "Marquette Greene-Scott", "D", None,
     ("def-03", 1, site("Marquette Greene-Scott", "https://marquettegreenescott.com/")("Greene-Scott would do more for veterans’ care"), "We owe it to them to ensure they receive the care and resources they so desperately need."))
BURGE = site("Kevin Burge", "https://www.burgeforcongress.com/")
cand("TX-H-24", "TX-H-24:burge", "Kevin Burge", "D", "Marine Corps veteran in Tarrant County.",
     ("hea-01", 2, BURGE("Burge supports Medicare for All"), "Kevin’s top priorities include affordable housing, restoring checks & balances, medicare for all, immigration reform"),
     ("edu-02", 2, BURGE("Burge supports tuition-free public college and trade school"), "tuition-free public college & trade education"),
     ("soc-03", 2, BURGE("Burge would restore abortion rights"), "restoring abortion rights"),
     ("hou-01", 1, BURGE("Burge would fast-track affordable housing"), "Fast-track funding and building affordable housing"),
     ("eco-03", 1, BURGE("Burge would raise the minimum wage"), "Vote to raise the federal minimum wage"),
     ("edu-05", 1, BURGE("Burge would get relief for struggling student loan borrowers"), "Get relief for student loan borrowers struggling to make payments"),
     ("hea-03", 1, BURGE("Burge would push Texas to expand Medicaid"), "Expand Funding and Incentives for Texas to Expand Medicaid."))
SHOOK = site("Steven Shook", "https://shookforcongress2026.com/")
cand("TX-H-26", "TX-H-26:shook", "Steven Shook", "D", "Critical care provider since 2009; born and raised in Fort Worth.",
     ("hea-01", 1, SHOOK("Shook would phase in universal health care"), "Implement planned step-by step transition to universal healthcare."),
     ("hea-02", 2, SHOOK("Shook would extend Medicare drug price negotiation to all plans"), "Lower prescription drug prices by expanding Medicare price negotiation to all insurance plans."),
     ("hea-08", 1, SHOOK("Shook would protect coverage for preexisting conditions"), "Cap out-of-pocket medication costs and protect coverage for pre-existing conditions."),
     ("hea-06", 1, SHOOK("Shook would expand mental health services"), "Expand mental health services and crisis intervention, especially in rural communities."))
cand("TX-H-28", "TX-H-28:duran", "Marlón Durán", "G", "Community organizer and English–Spanish translator who grew up undocumented in McAllen.",
     ("imm-08", -1, site("Marlón Durán", "https://marlonduran.com/")("Durán says ICE and the border agencies tear families apart"), "Marlón knows that ICE, DHS, and CPB harm our community and tear families apart."))
cand("TX-H-30", "TX-H-30:haynes", "Frederick Haynes III", "D", "Longtime Dallas pastor and activist.")
cand("TX-H-31", "TX-H-31:early", "Justin Early", "D", "Army veteran (a paratrooper, later at the Defense Intelligence Agency) and cybersecurity architect at Dell Technologies.")
cand("TX-H-31", "TX-H-31:stoker", "Greg Stoker", "G", "Former Army Ranger with four combat deployments in Afghanistan; a political analyst.",
     ("def-07", 1, site("Greg Stoker", "https://www.stokerfortexas.com/")("Stoker speaks out against war"), "I've made a career as a political analyst, speaking out against genocide and war."))
YARBROUGH = site("Jace Yarbrough", "https://www.jaceforcongress.com/")
cand("TX-H-32", "TX-H-32:yarbrough", "Jace Yarbrough", "R", "Air Force veteran and constitutional lawyer (UT Austin, Stanford Law); co-founded a classical Christian academy.",
     ("imm-01", 1, YARBROUGH("Yarbrough would keep the border closed"), "Keeping the Border Closed"),
     ("ene-03", 1, YARBROUGH("Yarbrough would unleash American energy"), "Unleashing American Energy"),
     ("eco-07", 1, YARBROUGH("Yarbrough would cut runaway spending"), "Cutting Runaway Spending and Making Washington Live Within Its Means"))
cand("TX-H-33", "TX-H-33:allred", "Colin Allred", "D",
     "Former congressman (2019–2025), NFL linebacker and civil rights lawyer; the 2024 Democratic Senate nominee.")
cand("TX-H-33", "TX-H-33:gillespie", "Patrick Gillespie", "R", None,
     ("imm-01", 1, site("Patrick Gillespie", "https://patrickgillespie4congress33.com/")("Gillespie wants immigrants vetted and illegal crossings stopped"), "We must have immigrants vetted and not allow an invasion of tens of thousands crossing our border illegally daily."))
cand("TX-H-38", "TX-H-38:bonck", "Jon Bonck", "R", "Houston-area mortgage executive and deacon at Second Baptist Church.",
     ("soc-04", 1, site("Jon Bonck", "https://www.jonbonck.com/")("Bonck has supported anti-abortion causes"), "he’s supported pro-life causes"))
MCDONOUGH = site("Melissa McDonough", "https://melissaforcongress.com/platform/")
cand("TX-H-38", "TX-H-38:mcdonough", "Melissa McDonough", "D", "Has worked as an election worker.",
     ("eco-10", -1, MCDONOUGH("McDonough says the China trade war cost Americans $80 billion"), "Donald Trump’s trade war with China cost Americans $80 billion in new taxes"),
     ("edu-06", -1, MCDONOUGH("McDonough criticizes the push for vouchers"), "Governor Abbott’s relentless push for vouchers"),
     ("edu-02", 1, MCDONOUGH("McDonough wants college open to everyone, citing tuition-free systems abroad"), "Going to college should be an option for all who wish to learn, and not a privilege for only the wealthy."),
     ("gov-06", 2, MCDONOUGH("McDonough would make mail-in voting easier"), "We need to make mail-in voting easier, continue to allow county-wide voting, have more accessible polling locations"),
     ("ene-01", 1, MCDONOUGH("McDonough would embrace renewable energy"), "we need to embrace renewable energy innovation"),
     ("def-13", 1, MCDONOUGH("McDonough would keep sending Ukraine older military equipment"), "We should continue to support Ukraine with our old military equipment"),
     ("def-14", 1, MCDONOUGH("McDonough calls Russia a direct threat"), "Russia presents a direct threat to America and our allies"),
     ("soc-12", 1, MCDONOUGH("McDonough decries injustice against LGBTQ+ people"), "Injustice against the LGBTQ+ community continues to plague our institutions"))

# Florida: campaign sites (the Florida Phoenix's guide had only a few bios). Sites that
# render only in a browser (Yonce, Gist, Jenkins, Pericola, Scrivener, People, Arias,
# Maxime, Andersen, Gilbert, Ehr) and those listing no issues (Grage's headings, Haskin,
# Adeimy, Locklin, Schwartzel) give little yet.
VALIMONT = site("Gay Valimont", "https://www.gayforcongress.com/")
cand("FL-H-01", "FL-H-01:valimont", "Gay Valimont", "D", None,
     ("hou-01", 1, VALIMONT("Valimont would expand affordable housing"), "Expand Affordable Housing"),
     ("def-03", 1, VALIMONT("Valimont would deliver a full-service VA hospital"), "delivering the full-service VA hospital our veterans need"))
cand("FL-H-01", "FL-H-01:davis", "Tyler Davis", "I", None,
     ("hou-09", 1, site("Tyler Davis", "https://www.tylerdavisforcongress.com/")("Davis wants infrastructure including broadband"), "including broadband, energy resilience, and water protection"))
HARP = site("Seth Harp", "https://www.sethharpforcongress.com/")
cand("FL-H-03", "FL-H-03:harp", "Seth Harp", "D", None,
     ("eco-01", 2, HARP("Harp would raise the payroll tax cap to $250,000"), "Protect and strengthen Social Security by raising the payroll tax cap to $250,000"),
     ("hea-01", 1, HARP("Harp would guarantee affordable health care for every American"), "Guarantee affordable health care for every American"),
     ("soc-07", 1, HARP("Harp would subsidize child care on a sliding scale"), "Expand affordable child care through a sliding-scale subsidy"),
     ("hou-02", 1, HARP("Harp would tax large corporate home purchases"), "The H.E.A.R.T. Act imposes escalating taxes on large-scale corporate home acquisitions"),
     ("hou-01", 1, HARP("Harp would give builders incentives for affordable homes"), None),
     ("hea-06", 2, HARP("Harp would double the behavioral health workforce"), "The D.O. Initiative will double America's behavioral health workforce over the next decade"))
cand("FL-H-03", "FL-H-03:klein", "Mike Klein", "I", "Fifth-generation Floridian raised in Gainesville.",
     ("gov-11", 1, site("Mike Klein", "https://mikeklein4congress.com/")("Klein would get money out of politics"), "get money out of our politics so the voices of the many outweigh the greed of the few"))
HOLLOWAY = site("LaShonda Holloway", "https://www.hollowayforcongress.com/")
cand("FL-H-04", "FL-H-04:holloway", "LaShonda Holloway", "D", "Lawyer with a law degree from the University of Florida.",
     ("hea-01", 1, HOLLOWAY("Holloway calls health care a basic human right"), "Access to quality healthcare is a basic human right that should not be determined by one's income."),
     ("hea-06", 1, HOLLOWAY("Holloway would expand mental health services and preventive care"), "we must be committed to expanding healthcare coverage, promoting preventative care initiatives, and increasing access to mental health services"),
     ("hea-09", 1, HOLLOWAY("Holloway would promote preventive care"), None))
cand("FL-H-04", "FL-H-04:sell", "Mike Sell", "Florida Forward", "Business executive who started in a minimum-wage job; raised in a Navy family.")
SCHAEFER = site("Todd Schaefer", "https://www.toddforfl4.com/")
cand("FL-H-04", "FL-H-04:schaefer", "Todd Schaefer", "I", "Retired Navy veteran.",
     ("eco-03", 1, SCHAEFER("Schaefer would pass a living wage"), "Passing a Fair and Lasting Living Wage"),
     ("gov-13", -2, SCHAEFER("Schaefer says Citizens United legalized bribery"), "Citizens United and SpeechNow.org v. FEC have legalized bribery by equating money with speech."),
     ("gov-11", 2, SCHAEFER("Schaefer would get big money out of politics"), None))
cand("FL-H-05", "FL-H-05:grage", "Rachel Grage", "D", "Has worked in health care; a mother of four.")
DENNISON = site("Christopher Dennison", "https://dennison4congress.com/")
cand("FL-H-07", "FL-H-07:dennison", "Christopher Dennison", "L", "Air Force veteran and father of two.",
     ("def-08", -2, DENNISON("Dennison would end deployments and close unneeded bases"), "We end the deployments, close the bases we do not need"),
     ("soc-08", 1, DENNISON("Dennison would remove Flock and Axon surveillance from public spaces"), "I will get these systems out of public spaces and keep the Fourth Amendment from becoming a technicality."),
     ("soc-04", 0, DENNISON("Dennison says abortion belongs to the states and won’t vote on it either way"), "This belongs to the states, and I will not vote to hand Washington power over it in either direction."),
     ("cri-09", -2, DENNISON("Dennison opposes the death penalty"), "I would rather one hundred guilty men live out their sentences than watch this country put one innocent man to death."))
STRADA = site("Joe Strada", "https://votestrada.com/")
cand("FL-H-11", "FL-H-11:strada", "Joe Strada", "R", "Businessman who invested in paid trade-training programs.",
     ("gov-09", 1, STRADA("Strada supports investigating congressional insider trading"), "Joe supports serious investigations into potential congressional insider trading and real accountability"),
     ("eco-07", 1, STRADA("Strada supports a balanced budget amendment"), "Joe supports a balanced budget amendment requiring Washington to live within its means, confront wasteful spending"),
     ("edu-03", 2, STRADA("Strada puts apprenticeships and technical education at the center of his campaign"), "workforce development, apprenticeships, and career and technical education are central to his campaign"))
GROVES = site("Ralph Groves", "https://www.grovesforcongress.com/")
cand("FL-H-11", "FL-H-11:groves", "Ralph Groves", "L", "Army and Iraq War veteran and former Defense Department analyst.",
     ("def-04", 2, GROVES("Groves would hold presidents to the War Powers Act’s 60-day limit"), "Uphold the War Powers Act."),
     ("soc-03", 0, GROVES("Groves is neither pro-choice nor pro-life; he wants abortion available, in hospitals"), "Abortions should be available, especially for medical purpose and performed in hospitals, not in outside clinics."))
OVERMAN = site("Kimberly Overman", "https://kimberlyoverman.com/")
cand("FL-H-12", "FL-H-12:overman", "Kimberly Overman", "D", "Former Hillsborough County commissioner and small business owner.",
     ("hea-01", 1, OVERMAN("Overman calls health care a right"), "Healthcare isn’t a luxury—it’s a right."),
     ("soc-03", 1, OVERMAN("Overman would defend reproductive rights"), "defend reproductive rights and mental health services"),
     ("edu-01", 1, OVERMAN("Overman would fully fund public schools and raise teacher pay"), "Kimberly will fight for fully funded public schools, better teacher pay"),
     ("edu-04", 1, OVERMAN("Overman would raise teacher pay"), None),
     ("hou-01", 1, OVERMAN("Overman would fight for affordable housing"), "she’ll fight for real solutions to rising costs, including affordable housing, infrastructure investment, and fair wages"))
ARRIGO = site("Tony D’Arrigo", "https://tonydarrigo.com/")
cand("FL-H-13", "FL-H-13:arrigo", "Tony D'Arrigo", "I", None,
     ("hea-01", 2, ARRIGO("D’Arrigo would guarantee coverage for every American"), "Guaranteed Coverage for All: Every American, no exceptions"),
     ("ene-05", 2, ARRIGO("D’Arrigo would build charging stations with money now spent on oil subsidies"), "Charging infrastructure and fueling stations, built on public land, with funds previously given as oil subsidies"))
LAMBERT = site("Brian Lambert", "https://www.brianlambertforcongress.com/")
cand("FL-H-14", "FL-H-14:lambert", "Brian Lambert", "L", "Navy veteran.",
     ("eco-07", 2, LAMBERT("Lambert would fight for balanced budgets"), "Washington does not have a revenue problem—it has a spending problem."),
     ("eco-02", 1, LAMBERT("Lambert wants lower taxes"), "Lower taxes. Responsible spending. End government waste."),
     ("gov-01", 1, LAMBERT("Lambert wants citizen legislators who serve for a time"), "Congress should be filled with citizens who serve for a time—not politicians who build lifelong careers in Washington."))
MDAVIS = site("Mark Davis", "https://markdavisforcongress.com/")
cand("FL-H-16", "FL-H-16:davis", "Mark Davis", "I", "Air Force veteran (eight years) and small business owner who spent 16 years in retail management.",
     ("hea-01", 2, MDAVIS("Davis calls universal health care common sense"), "Universal healthcare isn’t some scary monster—it’s common sense."),
     ("soc-03", 1, MDAVIS("Davis would protect reproductive freedom"), "We can protect reproductive freedom and protect public safety."),
     ("imm-08", -1, MDAVIS("Davis opposes militarizing streets over immigration"), "We’re not going to militarize our streets just because someone’s peddling fear."))
MONTAVON = site("Matthew Montavon", "https://www.montavonforcongress.com/")
cand("FL-H-17", "FL-H-17:montavon", "Matthew Montavon", "D", None,
     ("imm-01", 1, MONTAVON("Montavon would modernize border security"), "Modernizing border security infrastructure, technologies, and staffing"),
     ("imm-09", 1, MONTAVON("Montavon wants a legal workforce for farms, hotels and construction"), "ensuring our local agricultural, hospitality, and construction sectors have access to a predictable, legal workforce"),
     ("hou-01", 1, MONTAVON("Montavon would incentivize affordable housing"), "Incentivizing Affordable Housing"))
QUIRK = site("Michael Quirk", "https://www.michaelquirkforcongress.com/")
cand("FL-H-17", "FL-H-17:quirk", "Michael Quirk", "I", "Cybersecurity professional for 30 years who started a small business in Sarasota in 2024.",
     ("gov-01", 1, QUIRK("Quirk supports term limits and a congressional stock trading ban"), "Open party primaries to all voters, term limits, no congressional stock trading, no budget, no pay."),
     ("gov-02", 1, QUIRK("Quirk would ban congressional stock trading"), None),
     ("def-04", 2, QUIRK("Quirk wants Congress to vote before Americans fight or fund a war"), "No more blank checks. Congress debates and votes before Americans fight or fund a war."))
SIMMONS = site("Deva Simmons", "https://devasimmonsnpa.com/")
cand("FL-H-18", "FL-H-18:simmons", "Deva Simmons", "I", "Educator for more than 20 years; a Brooklyn native in Polk County since 2002.",
     ("hea-06", 1, SIMMONS("Simmons would increase access to mental health services"), "Increasing access to mental health services"),
     ("edu-04", 1, SIMMONS("Simmons would increase teacher pay"), "Increasing teacher pay and support"),
     ("eco-03", 1, SIMMONS("Simmons would raise the minimum wage to a living wage"), "Raising the minimum wage to a living wage"),
     ("ene-01", 1, SIMMONS("Simmons would create clean energy jobs"), "Creating good-paying jobs in clean energy"))
GIBSON = site("Curtis Gibson", "https://votecurtisgibson.com/")
cand("FL-H-18", "FL-H-18:gibson", "Curtis Gibson", "D", "Former Lake Wales city commissioner and professional wrestler.",
     ("def-03", 1, GIBSON("Gibson would give veterans a path to local providers when the VA can’t serve them"), "If the VA cannot provide care close to home and within a reasonable timeframe, veterans should have a clear path to covered local providers"),
     ("agr-01", 1, GIBSON("Gibson would support growers replanting resilient citrus"), "I’ll fight for smarter support for growers"))
cand("FL-H-19", "FL-H-19:schwartzel", "Jim Schwartzel", "R", "Southwest Florida native with a finance degree from Stetson University.")
MARTIN_FL = site("James Martin", "https://www.jamesmartinforflorida.com/")
cand("FL-H-21", "FL-H-21:martin", "James Martin", "D", "Coast Guard veteran and national security expert who advised White House leaders; a fourth-generation Floridian.",
     ("eco-10", -1, MARTIN_FL("Martin would end reckless tariffs"), "ending reckless tariffs driving up the price of groceries"),
     ("eco-04", 2, MARTIN_FL("Martin would use antitrust laws to break up corporate consolidation"), "using antitrust laws to break up the corporate consolidation that is squeezing consumers"),
     ("ene-04", 1, MARTIN_FL("Martin would never curtail bedrock environmental laws"), "never compromising or curtailing bedrock environmental laws"),
     ("gov-11", 1, MARTIN_FL("Martin would get big money out of politics"), "James is committed to getting big money out of politics"))
cand("FL-H-21", "FL-H-21:cooke", "Alexander Cooke", "I", None,
     ("gov-12", 1, site("Alex Cooke", "https://www.alexcookeforcongress.com/")("Cooke demands transparency on federal spending"), "Demand transparency on federal spending that fuels inflation"))
cand("FL-H-23", "FL-H-23:adeimy", "Deborah Adeimy", "R", "Certified financial planner who has advised clients at JP Morgan, Merrill Lynch, Morgan Stanley and Citi.")

# New York: campaign sites. Blay Tarnoff (L, 4th), George Marsh (R, 5th), Lewis Mizrahi
# (R, 8th), Joel Azumah (R, 9th), Wilneida Negron (I, 12th) and Stylo Sapaskis (R, 15th)
# have no sites; Jomo Williams' (R, 13th) only attacks his opponent, and Jennifer
# Moore's (R, 10th) serves no https page to cite.
CHOU = site("Joseph Chou", "https://josephforny.com/")
cand("NY-H-06", "NY-H-06:chou", "Joseph Chou", "R", None,
     ("eco-02", 1, CHOU("Chou wants a tax policy that lightens burdens on working families"), "A balanced tax policy that fosters growth and lightens burdens, particularly for our working families"),
     ("edu-06", 1, CHOU("Chou supports public, private and alternative school pathways"), "Education. Support for public, private and alternative pathways"),
     ("soc-07", 1, CHOU("Chou wants affordable child care"), "with better access to healthcare and affordable childcare"),
     ("cri-06", -1, CHOU("Chou would reform cashless bail"), "reform of the cashless bail system"))
VALDEZ = site("Claire Valdez", "https://clairevaldezforcongress.com/")
cand("NY-H-07", "NY-H-07:valdez", "Claire Valdez", "D",
     "State Assembly member, union organizer (UAW Local 2110) and democratic socialist; a citizen of the Ysleta del Sur Pueblo Nation.",
     ("eco-09", 2, VALDEZ("Valdez wants a golden age for organized labor"), "We will usher in a golden age for organized labor"),
     ("eco-01", 2, VALDEZ("Valdez has fought to tax the rich in the Assembly"), "she has fought to tax the rich, protect tenants, and empower working people"),
     ("hou-06", 1, VALDEZ("Valdez has fought to protect tenants"), None),
     ("def-15", -2, VALDEZ("Valdez calls the Iran bombing illegal and would fight to end such wars"), "the illegal bombing campaign"),
     ("def-12", -2, VALDEZ("Valdez opposes sending money to Israel’s war in Gaza"), "Like Joe Biden before him, Trump sent billions to fund genocide in Palestine."),
     ("def-01", -1, VALDEZ("Valdez criticizes the military-industrial complex"), "The military-industrial complex doesn't just enrich arms manufacturers"),
     ("imm-08", -2, VALDEZ("Valdez would abolish ICE"), "Abolish ICE and Protect Immigrants"))
cand("NY-H-07", "NY-H-07:ghaznavi", "Priscilla Ghaznavi", "I", "Born in Washington, D.C., to immigrant parents from Iran and Bolivia.")
RIVERA_NY = site("Melvin Rivera", "https://melvinforcongress.com/")
cand("NY-H-07", "NY-H-07:rivera", "Melvin Rivera", "R", "Bushwick community activist and tenant organizer for more than 30 years.",
     ("eco-09", 1, RIVERA_NY("Rivera would protect workers’ right to organize"), "Protect the right of workers to: Organize"),
     ("cri-07", 1, RIVERA_NY("Rivera would expand community policing"), "Expand community policing"),
     ("gov-12", 1, RIVERA_NY("Rivera would expand freedom-of-information access"), "Expand FOIL access to all publicly funded"))
LANDER = site("Brad Lander", "https://www.bradlanderforcongress.com/")
cand("NY-H-10", "NY-H-10:lander", "Brad Lander", "D",
     "Former New York City comptroller and City Council member; earlier led two affordable housing groups. Federal agents arrested him while he was defending immigrants from ICE.",
     ("imm-08", -1, LANDER("Lander would fight a federal government he says is abducting neighbors"), "Fight against an authoritarian federal government that is abducting our neighbors."),
     ("gov-11", 1, LANDER("Lander would get money out of politics"), "Fight to get money out of politics, instead of raking in Wall Street, crypto, and AIPAC contributions."))
DECILLIS = site("Michael DeCillis", "https://www.decillisforcongress.com/")
cand("NY-H-11", "NY-H-11:decillis", "Michael DeCillis", "D", "Former teacher and union member with 35 years in public service; a fourth-generation Staten Islander.",
     ("eco-02", 1, DECILLIS("DeCillis would cut taxes on the working class"), "Mike will advocate to reduce the tax burden on the working class and the billionaires need to pay their fair share."),
     ("eco-01", 1, DECILLIS("DeCillis wants billionaires to pay their fair share"), None),
     ("edu-01", 1, DECILLIS("DeCillis would invest more in public education"), "believes that more investments need to be made in public education"))
LASHER = site("Micah Lasher", "https://micahlasher.com/")
cand("NY-H-12", "NY-H-12:lasher", "Micah Lasher", "D", "Former state Assembly member who held senior posts in city government and the state attorney general’s office.",
     ("hea-01", 2, LASHER("Lasher would push to pass Medicare for All or a similar universal plan"), "Push to pass Medicare for All, or a similar plan that ensures universal care."),
     ("hea-06", 1, LASHER("Lasher would fund community health and mental health care"), "Increase funding for community-based health services and mental healthcare."),
     ("hea-03", 1, LASHER("Lasher would reverse the Medicaid cuts"), "Reverse the Republicans’ harsh and misguided cuts to Medicaid."),
     ("hea-09", 1, LASHER("Lasher would reverse the attacks on vaccines"), "reverse the attacks on vaccines and science-driven health policy"),
     ("eco-01", 1, LASHER("Lasher would repeal the tax breaks for the rich"), "Repeal Trump’s tax breaks to the rich and restore devastating cuts to the social safety net."),
     ("soc-07", 2, LASHER("Lasher would massively expand federal investment in child care"), "Massively expand federal investment in child care."),
     ("hou-01", 1, LASHER("Lasher would expand housing tax credits and rental assistance"), "Expand housing tax credits and increase funding and eligibility for rental assistance."),
     ("hou-04", 1, LASHER("Lasher would use federal money to spur pro-housing local policies"), "Leverage federal dollars to spur pro-housing policies at the state and local level."),
     ("eco-03", 2, LASHER("Lasher would raise the minimum wage and index it to inflation"), "Raise the minimum wage across the nation and index it to inflation."),
     ("gov-03", 1, LASHER("Lasher backs the For the People Act’s dark-money rules"), "Fight to pass the For the People Act to expand voting rights and tighten “dark money” regulation."),
     ("soc-03", 1, LASHER("Lasher champions reproductive freedom"), "Championing Reproductive Health and Freedom"),
     ("imm-08", -1, LASHER("Lasher would hold hearings to curtail ICE abuses"), "expose and curtail abuses by ICE"))
SHINKLE = site("Caroline Shinkle", "https://www.carolinefornewyork.com/")
cand("NY-H-12", "NY-H-12:shinkle", "Caroline Shinkle", "R", "Midtown Manhattan resident and MIT economics graduate.",
     ("eco-02", 1, SHINKLE("Shinkle would reduce taxes on work"), "Allow New Yorkers to keep more of what they earn by reducing tax on work."),
     ("eco-07", 1, SHINKLE("Shinkle would offer balanced budget amendments"), "Offer balanced budget amendments to keep Washington spending in check"),
     ("cri-01", 1, SHINKLE("Shinkle would champion law enforcement"), "Champion and support our law enforcement officers and first responders"),
     ("def-11", 2, SHINKLE("Shinkle stands unapologetically with Israel"), "Unapologetically stand with the Jewish community of New York City and with Israel."),
     ("def-02", 1, SHINKLE("Shinkle would stand with allies"), "Stand with our allies"))
ORTIZ = site("Karen Ortiz", "https://ko4congress.com/")
cand("NY-H-12", "NY-H-12:ortiz", "Karen Ortiz", "I", None,
     ("hea-01", 2, ORTIZ("Ortiz supports Medicare for All"), "We need Medicare for All to ensure that everyone has access to truly affordable, quality healthcare"),
     ("soc-03", 2, ORTIZ("Ortiz supports abortion without oppressive restrictions"), "which includes gender-affirming healthcare, abortion without oppressive restrictions"),
     ("soc-12", 1, ORTIZ("Ortiz supports gender-affirming care"), None),
     ("def-12", -2, ORTIZ("Ortiz would impose an arms embargo on Israel"), "We must impose an arms embargo on and stop sending our tax dollars to Israel."),
     ("def-01", -1, ORTIZ("Ortiz calls the military budget bloated"), "The U.S. Military has a bloated budget"))
CHEVALIER = site("Darializa Avila Chevalier", "https://www.darializaforcongress.com/")
cand("NY-H-13", "NY-H-13:chevalier", "Darializa Avila Chevalier", "D", None,
     ("hea-01", 2, CHEVALIER("Chevalier would fight for Medicare for All"), "Darializa will fight for Medicare for All: a free, universal system that covers primary and mental health care, dental, vision, hearing"),
     ("hea-10", 2, CHEVALIER("Chevalier’s Medicare for All would cover dental, vision and hearing"), None),
     ("eco-03", 1, CHEVALIER("Chevalier backs a $15 minimum wage"), "Darializa will sign onto these bills to secure housing as a human right, universal healthcare, union protections, a $15 minimum wage and more."),
     ("eco-09", 2, CHEVALIER("Chevalier would increase union density"), "Darializa will fight to protection workers' rights, increase union density, raise the minimum wage"),
     ("imm-08", -2, CHEVALIER("Chevalier would abolish the deportation machine"), "Darializa will fight to abolish the deportation machine, expand pathways to citizenship, secure free legal representation for immigrants"),
     ("imm-02", 2, CHEVALIER("Chevalier would expand pathways to citizenship"), None),
     ("def-01", -1, CHEVALIER("Chevalier would divest from wars abroad"), "Darializa will fight to divest the billions of taxpayer dollars we spend on senseless wars abroad"),
     ("hou-01", 2, CHEVALIER("Chevalier would fully fund Section 8 and NYCHA and build affordable housing"), "Darializa will fight to protect all tenants, fully fund Section 8, fully fund NYCHA, prevent deed theft, and build affordable housing."),
     ("hou-06", 1, CHEVALIER("Chevalier would protect all tenants"), None),
     ("edu-02", 2, CHEVALIER("Chevalier supports free public education from child care through college"), "Darializa will fight for our right to free, quality public education from childcare to college."),
     ("soc-07", 1, CHEVALIER("Chevalier supports free child care"), None),
     ("eco-04", 1, CHEVALIER("Chevalier would fight monopolies and super PACs"), "will fight against monopolies, price gouging, and super PACs"),
     ("gov-11", 1, CHEVALIER("Chevalier would fight super PACs"), None))
cand("NY-H-14", "NY-H-14:hysenaj", "Diamant Hysenaj", "R", "Construction small business owner who came to the U.S. at age nine.",
     ("imm-01", 1, site("Diamant Hysenaj", "https://votefordiamant.com/")("Hysenaj wants secure borders and faster citizenship for the law-abiding"), "I’ll demand a system that’s tough but fair: secure borders, faster citizenship for the law-abiding"))
VEGA = site("Jose Vega", "https://votevega.nyc/")
cand("NY-H-15", "NY-H-15:vega", "Jose Vega", "I", None,
     ("hea-01", 2, VEGA("Vega supports Medicare for All"), "A real medicare for all policy"),
     ("agr-03", 1, VEGA("Vega supports reindustrialization"), "Medicare for All, reindustrialization, and peace through development"))
EASTON = site("Andre Easton", "https://www.andreforthebronx.nyc/")
cand("NY-H-15", "NY-H-15:easton", "Andre Easton", "Socialism and Liberation", None,
     ("hou-01", 2, EASTON("Easton would repeal the federal ban on new public housing"), "Step one: repeal the “Faircloth Amendment,” the federal ban that’s blocked new public housing construction for decades."),
     ("hou-02", 1, EASTON("Easton would take the profit motive out of housing"), "The only solution is to take the profit motive out of housing."))
CINQUEMANI = site("Joseph Cinquemani", "https://www.cinquemaniforcongress.com/")
cand("NY-H-16", "NY-H-16:cinquemani", "Joseph Cinquemani", "R", None,
     ("eco-07", 1, CINQUEMANI("Cinquemani would pay for tax relief by cutting spending"), "We are focused on tax relieve by cutting spending"),
     ("ene-03", 2, CINQUEMANI("Cinquemani would reopen Indian Point and expand drilling"), 'reducing energy costs by recommissioning IPEC, "Drill, baby, drill!"'),
     ("ene-02", 1, CINQUEMANI("Cinquemani would recommission the Indian Point nuclear plant"), None),
     ("hou-04", 1, CINQUEMANI("Cinquemani would cut regulation so the market builds housing"), "eliminating unnecessary regulation to encourage market forces to build housing"))
AURINGER = site("Jackie Auringer", "https://winwithjackie.com/")
cand("NY-H-18", "NY-H-18:auringer", "Jacqueline Auringer", "R", "Works in the construction business.",
     ("hea-06", 1, AURINGER("Auringer supports mental health"), "Supports mental health and community well-being"),
     ("edu-03", 1, AURINGER("Auringer would focus on skilled trades and career education"), "Focusing on good-paying jobs, small business growth, skilled trades, and education connected to careers in the region."))
cand("NY-H-19", "NY-H-19:oberacker", "Peter Oberacker", "R", "State senator.")
AMBROSIO = site("Ralph Ambrosio", "https://ambrosioforcongress.com/")
cand("NY-H-20", "NY-H-20:ambrosio", "Ralph Ambrosio", "R", "Navy veteran (1970–1976), former New York State Police trooper and lawyer.",
     ("eco-02", 1, AMBROSIO("Ambrosio would cut taxes and regulation"), "We have to tackle crushing costs and lack of opportunity through tax cutting and deregulation."),
     ("ene-10", 1, AMBROSIO("Ambrosio would push all-of-the-above energy to drive down costs"), "I'll push and all-of-the-above energy strategy that will produce abundant supply while driving down costs."),
     ("gov-01", 1, AMBROSIO("Ambrosio supports term limits and voter ID"), "This means support for term limits, Voter ID, parental rights in education, and rooting out corruption"),
     ("gov-05", 1, AMBROSIO("Ambrosio supports voter ID"), None),
     ("cri-01", 1, AMBROSIO("Ambrosio would support law enforcement"), "supporting law enforcement"))
cand("NY-H-22", "NY-H-22:buller", "Kailee Buller", "R", "Auburn native and former chief of staff to the U.S. agriculture secretary; a former CEO.")
ELLMAN = site("Alissa Ellman", "https://www.ellmanforcongress.com/")
cand("NY-H-24", "NY-H-24:ellman", "Alissa Ellman", "D", "Grew up in rural Houghton.",
     ("soc-07", 1, ELLMAN("Ellman would expand affordable child care"), "Expanding access to affordable childcare"),
     ("hou-01", 1, ELLMAN("Ellman would expand the Low-Income Housing Tax Credit"), "Expanding the Low-Income Housing Tax Credit to help create and preserve affordable housing."),
     ("hou-03", 1, ELLMAN("Ellman would fund wider rural bus networks"), "Alissa will fight for funding to expand bus networks"),
     ("eco-06", 1, ELLMAN("Ellman would secure money to modernize water systems and infrastructure"), "secure federal funding to modernize water systems, repair aging infrastructure"))
HANNON = site("Dennis Hannon", "https://www.hannonforcongress.com/")
cand("NY-H-26", "NY-H-26:hannon", "Dennis Hannon", "R", "Grew up working in his father’s construction business.",
     ("imm-07", 1, HANNON("Hannon would prioritize serious public safety threats in immigration enforcement"), "Enforce immigration and border protection policies with a priortization on serious public safety threats"),
     ("eco-02", 1, HANNON("Hannon would give working families tax rebates"), "Provide relief to struggling working class families through tax rebates"),
     ("soc-11", -1, HANNON("Hannon opposes pushing minors toward irreversible medical decisions"), "I watched powerful institutions try to push my child toward irreversible medical decisions without real transparency"))

# Illinois: campaign sites
MILLER_IL = site("Donna Miller", "https://donnaforcongress.com/")
cand("IL-H-02", "IL-H-02:miller", "Donna Miller", "D", "Cook County commissioner with a background in health care consulting.",
     ("hea-01", 2, MILLER_IL("Miller supports a Medicare for All framework"), "Health care is a human right and I support a Medicare for All framework."),
     ("soc-03", 2, MILLER_IL("Miller would codify Roe v. Wade"), "In Congress, my focus will be to codify Roe v. Wade"))
cand("IL-H-02", "IL-H-02:noack", "Michael Noack", "R", "Truck driver from Bonfield, in Kankakee County for 32 years.",
     ("ene-01", 1, site("Mike Noack", "https://noack4congress.com/")("Noack supports hydroelectric and clean energy investment"), "Mike supports hydroelectric and clean energy investment that creates real jobs right here in Illinois"))
cand("IL-H-03", "IL-H-03:oakley", "Angel Oakley", "R", "Entrepreneur and former village official who calls herself a conservative moderate.")
GARCIA_IL = site("Patty Garcia", "https://pattyforillinois.com/")
cand("IL-H-04", "IL-H-04:garcia", "Patty Garcia", "D", "Holds a Ph.D. in education policy.",
     ("eco-03", 1, GARCIA_IL("Garcia would raise the federal minimum wage"), "Raising the federal minimum wage"),
     ("eco-02", 1, GARCIA_IL("Garcia would expand the Child Tax Credit"), "Expanding the Child Tax Credit"),
     ("imm-08", -2, GARCIA_IL("Garcia would abolish ICE"), "Fundamentally restructuring immigration enforcement agencies, including abolishing ICE"),
     ("eco-09", 2, GARCIA_IL("Garcia calls herself 100% pro-union and backs prevailing wages"), "100% Pro-Union Investment"),
     ("hea-01", 2, GARCIA_IL("Garcia backs Medicare for All"), "Patty backs Medicare for All to ensure healthcare as a human right"),
     ("hea-02", 1, GARCIA_IL("Garcia would let Medicare bargain over drug prices"), "Letting Medicare bargain for better prescription prices from pharmaceutical companies"),
     ("hea-06", 1, GARCIA_IL("Garcia would increase mental health care"), "Increasing mental health care"),
     ("edu-06", -1, GARCIA_IL("Garcia opposes privatizing public education"), "Public education should be funded, protected, and accountable to students, parents, and educators — not privatized for profit."),
     ("edu-05", 1, GARCIA_IL("Garcia supports student debt relief and bigger Pell Grants"), "Making college more affordable through expanded Pell Grants and student debt relief"),
     ("gov-13", -1, GARCIA_IL("Garcia would reverse Citizens United"), "Reversing Citizens United"),
     ("gov-02", 1, GARCIA_IL("Garcia would end stock trading by members of Congress"), "Ending stock-trading by congressional"))
cand("IL-H-04", "IL-H-04:getty", "Chris Getty", "I", "Lyons native and Lyons Township official, including on its mental health board.")
HANSON = site("Tommy Hanson", "https://votetommyhanson.com/")
cand("IL-H-05", "IL-H-05:hanson", "Tommy Hanson", "R", None,
     ("eco-10", 1, HANSON("Hanson supports sensible tariffs"), "Plus implementing sensible tariffs and a Fair Tax"),
     ("imm-08", -1, HANSON("Hanson would let ICE work only in states that want it"), "I.C.E. will only work in the states that demand their services"),
     ("soc-04", 1, HANSON("Hanson is anti-abortion"), "I am pro-life"))
CONFORTI = site("Niki Conforti", "https://conforti4congress.com/")
cand("IL-H-06", "IL-H-06:conforti", "Niki Conforti", "R", "Has worked in the health care industry.",
     ("hea-04", 1, CONFORTI("Conforti wants more marketplace options and portable policies"), "consumers should have more options in the marketplace and their policies should be transportable across state lines"),
     ("eco-07", 2, CONFORTI("Conforti opposes raising the debt ceiling"), "I am opposed to raising the Debt Ceiling."),
     ("eco-10", 1, CONFORTI("Conforti says tariffs will bring back manufacturing"), "Tariffs will help bring back manufacturing and add jobs"))
cand("IL-H-07", "IL-H-07:ford", "La Shawn Ford", "D",
     "State representative for 18 years, a former Chicago Public Schools teacher and coach, and a West Side real estate business owner.",
     ("hea-06", 1, site("La Shawn Ford", "https://fordforcongress.com/")("Ford passed state laws expanding mental health supports"), "mental health supports, recovery housing, and opioid treatment reporting"))
BEAN = site("Melissa Bean", "https://www.melissabeanforillinois.com/")
cand("IL-H-08", "IL-H-08:bean", "Melissa Bean", "D", "Represented the 8th District in Congress from 2005 to 2011.",
     ("edu-03", 1, BEAN("Bean would invest in public education and apprenticeships"), "Invest in public education, workforce training, and apprenticeships tied to good-paying jobs"),
     ("edu-01", 1, BEAN("Bean would invest in public education"), None),
     ("imm-08", -1, BEAN("Bean objects to masked ICE agents in neighborhoods"), "Americans feel unsafe when masked ICE agents are deployed into their neighborhoods unnecessarily."))
BISS = site("Daniel Biss", "https://www.danielbiss.com/")
cand("IL-H-09", "IL-H-09:biss", "Daniel Biss", "D", "Mayor of Evanston and former state senator.",
     ("soc-03", 2, BISS("Biss enacted major abortion rights legislation as a legislator"), "enacting major abortion rights legislation"),
     ("soc-12", 1, BISS("Biss passed protections for LGBTQ+ youth"), "passing protections for LGBTQ+ youth"),
     ("soc-08", 1, BISS("Biss strengthened technology privacy requirements"), "strengthening technology privacy requirements to protect civil liberties"),
     ("ene-06", 1, BISS("Biss passed an Evanston ordinance to curb building carbon emissions"), "pass a first-in-the-state Healthy Buildings Ordinance to curb carbon emissions"),
     ("gov-11", 1, BISS("Biss enacted campaign finance reform as mayor"), "enact desperately-needed campaign finance reform"),
     ("cri-08", 1, BISS("Biss created a non-police response to low-risk calls"), "a non-police response to low-risk service calls"))
WALTER = site("Jeff Walter", "https://www.jeffwalterforcongress.com/")
cand("IL-H-11", "IL-H-11:walter", "Jeff Walter", "R", "Businessman and Navy veteran.",
     ("eco-10", 1, WALTER("Walter supports tariffs that protect American workers"), "he supports Trump’s America First economic plan, including tariffs that protect American workers and jobs"),
     ("eco-02", 1, WALTER("Walter would make the Trump tax cuts permanent"), "Jeff supports making the Trump tax cuts permanent"),
     ("cri-01", 1, WALTER("Walter would fully fund law enforcement"), "Jeff supports fully funding law enforcement, ending soft-on-crime policies"),
     ("ene-03", 1, WALTER("Walter would unleash American energy"), "we must unleash American energy"))
FORTIER = site("Julie Fortier", "https://juliefortier.org/")
cand("IL-H-12", "IL-H-12:fortier", "Julie Fortier", "D", "Air Force veteran (Desert Shield) and cancer research scientist in Southern Illinois for more than 25 years.",
     ("eco-09", 1, FORTIER("Fortier supports union jobs and workforce training"), "Julie supports good union jobs, workforce training"),
     ("soc-03", 1, FORTIER("Fortier would defend reproductive rights"), "Julie will stand with women in Illinois to defend reproductive rights"))
WILSON_IL = site("Jeff Wilson", "https://www.wilsonforcongress.com/")
cand("IL-H-13", "IL-H-13:wilson", "Jeff Wilson", "R", "Navy veteran who served on a nuclear-powered submarine; master’s in nuclear engineering from the University of Illinois.",
     ("imm-01", 1, WILSON_IL("Wilson would secure the border"), "Securing the Border & Defending Law Enforcement"),
     ("ene-10", 1, WILSON_IL("Wilson would expand Midwest energy to lower bills"), "expanding Midwest energy to lower utility bills"))
cand("IL-H-14", "IL-H-14:marter", "James Marter", "R", "Hosts a weekly radio show, “Saving the American Dream.”",
     ("eco-07", 1, site("James Marter", "https://marter4congress.us/")("Marter would stop waste, fraud and abuse"), "work hard to stop the waste, fraud and abuse that is robbing you of your hard earned income"))
TODD_IL = site("Jennifer Todd", "https://www.jentodd2026.us/")
cand("IL-H-15", "IL-H-15:todd", "Jennifer Todd", "D", "Nurse.",
     ("soc-02", 1, TODD_IL("Todd would oppose discrimination in any form"), "I will oppose discrimination in any form and support equal rights and equal opportunity for all."),
     ("soc-07", 1, TODD_IL("Todd would ease the burden of child care"), "I will also work to ease the burden of childcare"))
cand("IL-H-16", "IL-H-16:nolley", "Paul Nolley", "D", None,
     ("hea-01", 2, site("Paul Nolley", "https://www.nolleyforcongress.com/")("Nolley would open Medicare to every American with no premiums or copays"), "we need to expand Medicare to cover all medically necessary care and make it available to every American, regardless of age"))
cand("IL-H-17", "IL-H-17:vancil", "Dillan Vancil", "R",
     "Railroad worker and former state legislative director of the SMART-TD union; a school board member and coffee business owner.",
     ("agr-03", 1, site("Dillan Vancil", "https://www.vancilforcongress.com/")("Vancil would bring manufacturing jobs back to Illinois"), "Dillan will be a voice for small businesses and will fight everyday to bring Manufacturing and real American Jobs back to Illinois."))

# Ohio: campaign sites (the Ohio Capital Journal's guide wasn't readable)
WEISE = site("Nathan Weise", "https://www.weiseforcongress.com/")
cand("OH-H-01", "OH-H-01:weise", "Nathan Weise", "L", None,
     ("eco-07", 1, WEISE("Weise supports responsible spending reforms"), "Nathan supports responsible spending reforms"),
     ("soc-08", 1, WEISE("Weise opposes unwarranted government monitoring"), "Nathan believes that Americans should be free from unwarranted government monitoring"),
     ("def-07", 1, WEISE("Weise would end ongoing foreign wars"), "Nathan supports ending ongoing foreign wars"))
cand("OH-H-02", "OH-H-02:mazzuckelli", "Jennifer Mazzuckelli", "D", "Former high school English teacher.")
DULANEY = site("Cleophus Dulaney", "https://votedulaney.org/")
cand("OH-H-03", "OH-H-03:dulaney", "Cleophus Dulaney", "R", None,
     ("hea-02", 1, DULANEY("Dulaney would let Medicare negotiate drug prices"), "I will push to lower prescription drug prices by letting Medicare negotiate directly"),
     ("eco-02", 1, DULANEY("Dulaney supports tax relief for working and middle-class families"), "I will support targeted tax relief for working and middle"),
     ("ene-01", 1, DULANEY("Dulaney would invest in clean energy jobs and infrastructure"), "I will support investment in infrastructure, advanced manufacturing, and clean energy jobs"),
     ("eco-06", 1, DULANEY("Dulaney would invest in infrastructure"), None),
     ("edu-03", 1, DULANEY("Dulaney would back apprenticeships"), "I’ll back apprenticeship and training programs"))
cand("OH-H-05", "OH-H-05:shaver", "Brian Shaver", "D", "Fostoria City Council president and social studies teacher.",
     ("gov-01", 1, site("Brian Shaver", "https://www.brianshaverforcongress.com/")("Shaver backs term limits, campaign finance limits and guardrails on profiting from office"), "He advocates for reforms such as campaign finance limits, term limits, stronger checks and balances, transparency in legislation"),
     ("gov-11", 1, site("Brian Shaver", "https://www.brianshaverforcongress.com/")("Shaver backs campaign finance limits"), None))
KIRTLEY = site("Elizabeth Kirtley", "https://www.elizabethforus.com/")
cand("OH-H-06", "OH-H-06:kirtley", "Elizabeth Kirtley", "D", None,
     ("imm-08", -2, KIRTLEY("Kirtley would abolish ICE"), "Abolish Ice"),
     ("soc-03", 2, KIRTLEY("Kirtley would codify Roe"), "Life, Liberty, and the Pursuit of Happiness includes a Woman’s Right to Choose."),
     ("hea-01", 1, KIRTLEY("Kirtley supports universal health care"), "Universal Healthcare"))
ENOCH = site("Vanessa Enoch", "https://enochforcongress.com/")
cand("OH-H-08", "OH-H-08:enoch", "Vanessa Enoch", "D", None,
     ("def-04", 2, ENOCH("Enoch says the power to declare war belongs to Congress"), "The United States Constitution is clear: the power to declare war belongs to Congress."),
     ("soc-03", 2, ENOCH("Enoch would fight for reproductive rights"), "I will fight every day for a woman’s right to safe, accessible, and affordable reproductive care"))
CHRISTIAN_OH = site("Jerrad Christian", "https://www.christianforohio.com/")
cand("OH-H-12", "OH-H-12:christian", "Jerrad Christian", "D", "Navy veteran and software engineer.",
     ("gov-13", -2, CHRISTIAN_OH("Christian would end Citizens United"), "When the Supreme Court handed down Citizens United, it opened the floodgates for unlimited corporate spending"),
     ("gov-11", 2, CHRISTIAN_OH("Christian says billionaires shouldn’t have a louder voice"), "Billionaires should not have a louder voice than a teacher, a mechanic, a nurse or a janitor."))
COLEMAN_OH = site("Carey Coleman", "https://careycoleman.com/")
cand("OH-H-13", "OH-H-13:coleman", "Carey Coleman", "R", "Longtime Northeast Ohio radio host on WNIR.",
     ("eco-07", 1, COLEMAN_OH("Coleman would rein in federal spending"), "He supports reining in out-of-control federal spending, restoring fiscal discipline, and ending wasteful programs that drive inflation."),
     ("imm-01", 1, COLEMAN_OH("Coleman would secure the borders"), "secure our borders"),
     ("ene-03", 1, COLEMAN_OH("Coleman would unleash American energy production"), "Carey will fight to unleash American energy production"))
DIXIT = site("Sandeep Dixit", "https://www.sandeepforcongress2026.com/")
cand("OH-H-13", "OH-H-13:dixit", "Sandeep Dixit", "I", None,
     ("edu-03", 2, DIXIT("Dixit would invest $500 million per district in vocational training"), "Significant investment, $500 million per district, in vocational and skilled trades training."),
     ("eco-03", 1, DIXIT("Dixit would raise the minimum wage"), "Raise the minimum wage so full-time work makes living affordable."),
     ("ene-04", 1, DIXIT("Dixit wants strict enforcement of environmental and privacy laws"), "Strict enforcement of environmental regulations and privacy protection laws."),
     ("soc-08", 1, DIXIT("Dixit makes citizens’ privacy a top priority"), None))
BARRINGTON = site("Brennan Barrington", "https://barrington.lpo.org/")
cand("OH-H-15", "OH-H-15:barrington", "Brennan Barrington", "L", None,
     ("def-01", -2, BARRINGTON("Barrington would cut the military-industrial complex"), "Stop the Wars; Cut the Military-Industrial Complex"),
     ("gov-07", 1, BARRINGTON("Barrington supports ranked-choice voting for Senate races"), "For Senate elections, ranked choice voting"),
     ("eco-07", 1, BARRINGTON("Barrington would cut or eliminate federal bureaucracies"), "Federal Bureaucracies to Cut or Eliminate"))

# Missouri: campaign sites. Jordan Herrera's (D, 4th) shows only endorsements; Kevin
# Craig's (L, 7th) lists no specific positions.
cand("MO-H-01", "MO-H-01:schmitz", "Tom Schmitz", "L", None,
     ("def-07", 1, site("Tom Schmitz", "https://www.tomschmitzforliberty.com/")("Schmitz fights against endless war"), "I will never stop fighting for individualism and peace, and against the darkness of forced collectivism and endless war."))
MANN = site("Bethany Mann", "https://bethanymannforcongress.com/")
cand("MO-H-03", "MO-H-03:mann", "Bethany Mann", "D", None,
     ("def-04", 2, MANN("Mann calls on Congress to reclaim its war powers"), "Mann Opposes Unauthorized War with Iran, Calls on Congress to Reclaim War Powers"),
     ("def-15", -1, MANN("Mann opposes the unauthorized war with Iran"), None),
     ("edu-01", 1, MANN("Mann supports full and equal public school funding"), "Bethany supports full and equal funding for public education"))
cand("MO-H-05", "MO-H-05:brattin", "Rick Brattin", "R", "State senator and Marine veteran (six years); a small business owner from Greenwood.",
     ("imm-01", 1, site("Rick Brattin", "https://rickbrattin.com/")("Brattin would help secure the border and cut spending"), "help President Trump secure our border, restore energy independence, cut wasteful spending"),
     ("eco-07", 1, site("Rick Brattin", "https://rickbrattin.com/")("Brattin would cut wasteful spending"), None))
cand("MO-H-06", "MO-H-06:stigall", "Chris Stigall", "R",
     "Nationally syndicated conservative radio host; earlier a field representative and deputy communications director for Rep. Sam Graves.")
SMEAD = site("Josh Smead", "https://votesmead.com/")
cand("MO-H-06", "MO-H-06:smead", "Josh Smead", "D", None,
     ("agr-06", 1, SMEAD("Smead would expand access to global markets for farmers"), "Expand access to current and new U.S. and global markets"),
     ("hou-09", 1, SMEAD("Smead supports rural internet access"), "Support infrastructure growth and internet access"),
     ("eco-06", 1, SMEAD("Smead would release the 2021 infrastructure law’s funding"), "We need to stop the current administration from holding up funding from the 2021 Bipartisan Infrastructure Law."),
     ("ene-01", 1, SMEAD("Smead supports the Grain Belt Express wind power line"), "Support the Grain Belt Express project for stable, low-cost power"))
MAIDMENT = site("Andy Maidment", "https://www.maidmentformissouri.com/")
cand("MO-H-06", "MO-H-06:maidment", "Andy Maidment", "L", None,
     ("edu-07", 1, MAIDMENT("Maidment would eliminate the Education Department"), "Eliminate Federal departments which have no Constitutional basis to exist starting with Education, Commerce, and Homeland Security."),
     ("eco-07", 1, MAIDMENT("Maidment would eliminate whole federal departments"), None),
     ("eco-12", -2, MAIDMENT("Maidment opposes the income tax"), "Taxes simply take money away from those who produce and give it to those who do not."))
HESKETH = site("Missi Hesketh", "https://missiheskethforcongress.com/")
cand("MO-H-07", "MO-H-07:hesketh", "Missi Hesketh", "D", "Teacher for 22 years and former mayor; lives in Forsyth.",
     ("eco-01", 1, HESKETH("Hesketh would close loopholes that benefit billionaires"), "Close Tax Loopholes to End Billionaire Welfare"),
     ("edu-03", 1, HESKETH("Hesketh would invest in rural education and workforce training"), "Invest in rural education and workforce training"),
     ("soc-08", 1, HESKETH("Hesketh supports comprehensive data privacy for children"), "Comprehensive Data Privacy for Children"),
     ("hea-03", 1, HESKETH("Hesketh supports Medicare for all who want it"), "Medicare for all who want it"),
     ("hea-02", 1, HESKETH("Hesketh supports Medicare drug price negotiation"), "Medicare Drug Price Negotiation"),
     ("gov-02", 1, HESKETH("Hesketh would ban congressional stock trading"), "Ban Congressional Stock Trading"),
     ("gov-09", 1, HESKETH("Hesketh would impose a lifetime lobbying ban on members"), "Lifetime lobbying ban for members of Congress"),
     ("gov-13", -1, HESKETH("Hesketh would end Citizens United"), "Ban dark money, end Citizens United"))
REICHARD = site("Chris Reichard", "https://www.reichardforrep.com/")
cand("MO-H-08", "MO-H-08:reichard", "Chris Reichard", "D", "Disabled Army veteran of the Iraq war and second-generation IBEW Local 1 member from Arnold.",
     ("eco-09", 2, REICHARD("Reichard would push the PRO Act"), "pushing the PRO Act to protect the right to organize"),
     ("def-07", 1, REICHARD("Reichard would keep the U.S. out of another forever war"), "fighting to keep us out of another forever war"),
     ("gov-13", -2, REICHARD("Reichard would end Citizens United and dark money"), "ending Citizens United and shutting down dark money"),
     ("gov-11", 2, REICHARD("Reichard would shut down dark money"), None))

# Michigan: campaign sites (the Michigan Advance's guide wasn't readable)
BARR = site("Callie Barr", "https://callieforcongress.com/")
cand("MI-H-01", "MI-H-01:barr", "Callie Barr", "D", "Teacher, attorney and veterans’ advocate from Traverse City and Cheboygan; a Marine spouse and caregiver.",
     ("hea-03", 2, BARR("Barr would make Medicare an option for everyone from birth"), "Make Medicare an option that is available to everyone from the moment they are born."),
     ("hea-01", 1, BARR("Barr calls health care a right"), "Health care should be a right, not a privilege."),
     ("hou-04", 1, BARR("Barr would cut red tape for local home builders"), "Build homes people can afford, cut red tape for trusted local builders"),
     ("eco-09", 1, BARR("Barr would support unions and expand child care"), "Reward work, support unions, protect Social Security, expand childcare, and invest in small businesses, farms, broadband, and infrastructure."),
     ("soc-07", 1, BARR("Barr would expand child care"), None),
     ("hou-09", 1, BARR("Barr would invest in broadband"), None))
FEATHERLY = site("Zebulon Featherly", "https://www.zebulonforcongress.com/")
cand("MI-H-01", "MI-H-01:featherly", "Zebulon Featherly", "I", None,
     ("hea-01", 2, FEATHERLY("Featherly would make universal health care a reality"), "I’ll work to make universal healthcare and tuition-free higher education a reality"),
     ("edu-02", 2, FEATHERLY("Featherly supports tuition-free higher education"), None),
     ("hea-05", 1, FEATHERLY("Featherly would expand research and clean energy"), "I will fight to expand research, push clean energy advancements, cut waste"),
     ("ene-01", 1, FEATHERLY("Featherly would push clean energy advancements"), None),
     ("eco-02", 1, FEATHERLY("Featherly would block new taxes on working families"), "I will block new taxes on working families"))
DEBOER = site("Terri DeBoer", "https://terrideboerforcongress.com/")
cand("MI-H-03", "MI-H-03:deboer", "Terri DeBoer", "R", None,
     ("hea-04", 1, DEBOER("DeBoer would expand health care choice and competition"), "Expand healthcare choice and competition to lower costs."),
     ("eco-07", 1, DEBOER("DeBoer would cut taxes and spending"), "Cut taxes and reduce government spending to fight inflation."),
     ("eco-02", 1, DEBOER("DeBoer would cut taxes"), None),
     ("ene-02", 1, DEBOER("DeBoer would expand nuclear energy"), "Expand clean, dependable nuclear energy production."),
     ("ene-10", 1, DEBOER("DeBoer opposes costly energy mandates"), "Oppose costly energy mandates that increase utility bills for families."),
     ("imm-01", 1, DEBOER("DeBoer would secure the border"), "Secure the border and enforce immigration laws."))
POOLEY = site("Ray Pooley", "https://www.pooley4congress.com/")
cand("MI-H-09", "MI-H-09:pooley", "Ray Pooley", "D", None,
     ("eco-12", 1, POOLEY("Pooley would make the ultra-wealthy pay their fair share and cut taxes for workers"), "simplifying the tax code so the ultra-wealthy pay their fair share, allowing us to cut taxes for working families"),
     ("eco-02", 1, POOLEY("Pooley would cut taxes for working families"), None),
     ("eco-03", 1, POOLEY("Pooley would raise the minimum wage and cap CEO pay ratios"), "raising the minimum wage while putting a maximum ratio for CEO pay"),
     ("eco-09", 1, POOLEY("Pooley would protect the right to organize"), "We will ensure these new jobs pay a living wage by protecting the right to organize and join a union."),
     ("edu-03", 1, POOLEY("Pooley would expand trade schools"), "expanding trade schools"))
cand("MI-H-11", "MI-H-11:moss", "Jeremy Moss", "D", "State senator and president pro tem of the Michigan Senate; an Oakland County native.",
     ("soc-03", 2, site("Jeremy Moss", "https://votejeremymoss.com/")("Moss protected and expanded reproductive freedom in Michigan"), "he successfully implemented effective gun safety laws, protected and expanded reproductive freedom, and provided tax relief for seniors and working families"),
     ("eco-02", 1, site("Jeremy Moss", "https://votejeremymoss.com/")("Moss provided state tax relief for working families"), None))
cand("MI-H-11", "MI-H-11:kumar", "Anil Kumar", "I", None,
     ("hea-01", 1, site("Anil Kumar", "https://www.drkumarforcongress.org/")("Kumar calls quality, affordable health care a right"), "quality, affordable healthcare is a right, not a privilege"))
cand("MI-H-11", "MI-H-11:baker", "Ethan Baker", "R", None,
     ("edu-07", 1, site("Ethan Baker", "https://www.bakerforcongress.com/")("Baker wants education decisions made locally"), "with education decisions made at the local level"))
cand("MI-H-12", "MI-H-12:hooper", "James Hooper", "R", "Former manager of a water and sanitation program for Samaritan’s Purse in Liberia.",
     ("soc-04", 2, site("James Hooper", "https://jameshooperforcongress.com/")("Hooper is anti-abortion from conception"), "James Hooper is unapologetically PRO-LIFE from conception to natural death."))
MCKINNEY_MI = site("Donavan McKinney", "https://www.donavanforcongress.com/")
cand("MI-H-13", "MI-H-13:mckinney", "Donavan McKinney", "D", "State representative from Detroit and a Detroit Public Schools graduate.",
     ("eco-01", 2, MCKINNEY_MI("McKinney would raise taxes on billionaires and corporations"), "Raising taxes on billionaires and corporations could fund crucial investments our community needs"),
     ("eco-09", 1, MCKINNEY_MI("McKinney would protect the right to form a union"), "I’m fighting for all my union family and for every worker to have the right to form a union"),
     ("ene-01", 2, MCKINNEY_MI("McKinney backs a Green New Deal moving to 100% clean energy"), "A Green New Deal transitioning to 100% clean and renewable energy"),
     ("hou-03", 1, MCKINNEY_MI("McKinney would expand public transit"), "investment to build and expand public transit"),
     ("gov-13", -2, MCKINNEY_MI("McKinney calls Citizens United disastrous"), "Because of the Supreme Court’s disastrous Citizens United decision 15 years ago"),
     ("gov-11", 2, MCKINNEY_MI("McKinney has fought to get big money out of politics"), "I’ve fought to get big money out of politics"),
     ("edu-01", 2, MCKINNEY_MI("McKinney would put federal money back in public schools and raise teacher pay"), "I’m going to Washington to put federal dollars back in our public schools"),
     ("edu-04", 1, MCKINNEY_MI("McKinney would raise teacher pay"), None),
     ("edu-09", 2, MCKINNEY_MI("McKinney supports universal free school lunches"), None))
cand("MI-H-13", "MI-H-13:nykoriak", "T. P. Nykoriak", "R", None,
     ("soc-05", 2, site("T. P. Nykoriak", "https://tp313.org/")("Nykoriak would remove marijuana from the federal controlled-substances list"), "TP Nykoriak believes Congress should work with the President to remove marijuana from the federal list of controlled substances"))

# New Jersey: campaign sites
cand("NJ-H-01", "NJ-H-01:galdo", "Damon Galdo", "R", "Union carpenter.",
     ("eco-07", 1, site("Damon Galdo", "https://votedamongaldo.com/")("Galdo would reduce unnecessary federal spending"), "to reduce unnecessary federal spending"))
PEACE = site("Rachel Peace", "https://www.peace4shore.com/")
cand("NJ-H-04", "NJ-H-04:peace", "Rachel Peace", "D", None,
     ("ene-08", 1, PEACE("Peace wants big oil to pay to prepare for future hurricanes"), "I urged state lawmakers to send the bill to big oil—not taxpayers—to actively prepare for (not react to) future hurricanes."),
     ("ene-04", 1, PEACE("Peace objects to cutting clean air and ocean pollution rules"), "regulations that protect clean air for our children and prevent ocean pollution were cut"))
cand("NJ-H-08", "NJ-H-08:eliopoulos", "Aristotle Eliopoulos", "I", "Jersey City teacher and union representative; the son of Greek immigrants.")
cand("NJ-H-09", "NJ-H-09:pino", "Rosie Pino", "R", "Clifton city councilwoman and former Treasury Department bank examiner; left the Democratic Party to become a Republican.")
cand("NJ-H-09", "NJ-H-09:bukovinac", "Terrisa Bukovinac", "I", "Anti-abortion activist who calls herself a progressive pro-lifer.",
     ("soc-04", 2, site("Terrisa Bukovinac", "https://terrisa2026.com/")("Bukovinac’s campaign is built on ending abortion"), "Abortion is genocide and I’m going to act like it."))
cand("NJ-H-10", "NJ-H-10:bucco", "Carmen Bucco", "R", None,
     ("cri-01", 1, site("Carmen Bucco", "https://carmenbucco.com/")("Bucco would support police and be tough on violent crime"), "We must always support our police and first responders and need to be tough on violent crimes"),
     ("cri-04", 1, site("Carmen Bucco", "https://carmenbucco.com/")("Bucco would be tough on violent crime"), None))
HATHAWAY = site("Joe Hathaway", "https://www.joehathawayforcongress.com/")
cand("NJ-H-11", "NJ-H-11:hathaway", "Joe Hathaway", "R", "Mayor of Randolph in 2025 and a township council member since 2022; a Yale graduate and former football player.",
     ("cri-02", 1, HATHAWAY("Hathaway deployed body-worn cameras as mayor"), "deployed body-worn cameras"),
     ("cri-01", 1, HATHAWAY("Hathaway restored full police staffing in Randolph"), "restored full police staffing"))
HAMAWY = site("Adam Hamawy", "https://hamawyfornj.com/")
cand("NJ-H-12", "NJ-H-12:hamawy", "Adam Hamawy", "D", "Surgeon, veteran and small business owner.",
     ("hea-01", 2, HAMAWY("Hamawy would pass Medicare for All"), "starting with passing Medicare for All and fixing our broken healthcare system"),
     ("imm-08", -2, HAMAWY("Hamawy opposes funding ICE’s tactics"), "It is absolutely unacceptable to use our tax dollars to fund the terrorizing of hardworking families"),
     ("def-01", -1, HAMAWY("Hamawy would spend on communities instead of bombs"), "But there's always money for bombs."))
MELE = site("Gregg Mele", "https://www.mele4america.com/")
cand("NJ-H-12", "NJ-H-12:mele", "Gregg Mele", "R", None,
     ("eco-07", 1, MELE("Mele would fight for responsible budgets"), "Gregg will fight for responsible budgets"),
     ("ene-03", 1, MELE("Mele would expand American energy"), "Expand reliable American energy to lower costs and strengthen national security."),
     ("def-11", 1, MELE("Mele would support Israel"), "Defend parents, restore academic excellence, support Israel, and lead with moral clarity."),
     ("imm-01", 1, MELE("Mele would secure the border"), "Secure the border. Enforce the law. Protect our communities."),
     ("cri-01", 1, MELE("Mele would support law enforcement"), "Enforce the law, support law enforcement"))

# California: campaign sites (found through the candidates' Wikipedia articles and
# BallotReady profiles, since Wikipedia's California page lists none; the links
# themselves are in campaign_sites_2026.py)
MCGUIRE = site("Mike McGuire", "https://www.votemikemcguire.com/")
cand("CA-H-01", "CA-H-01:mcguire", "Mike McGuire", "D", "State senator from Geyserville and former leader of the California Senate.",
     ("hea-03", 1, MCGUIRE("McGuire kept rural hospitals open and expanded coverage"), "When Trump cut health care, Mike McGuire kept rural hospitals open and expanded coverage."),
     ("soc-03", 2, MCGUIRE("McGuire led the fight to keep California’s Planned Parenthood centers open"), "When Trump defunded Planned Parenthood, Mike led the fight to keep all 100 of their California health centers open."),
     ("ene-08", 2, MCGUIRE("McGuire doubled state firefighters and invested billions in wildfire prevention"), "Mike doubled the number of state firefighters and invested billions in wildfire prevention"))
LITTAU = site("Robin Littau", "https://www.littauforcongress.com/")
cand("CA-H-02", "CA-H-02:littau", "Robin Littau", "R", "Enterprise Elementary school board member, Coast Guard veteran and owner of a cleaning company in Redding.",
     ("eco-07", 1, LITTAU("Littau would require responsible spending"), "Require Responsible Spending"),
     ("cri-01", 1, LITTAU("Littau supports law enforcement"), "Support Law Enforcement"))
cand("CA-H-03", "CA-H-03:tucker", "Robb Tucker", "R", "Nevada County supervisor since 2024 and former CEO of a family business.",
     ("imm-01", 1, site("Robb Tucker", "https://robbtucker.com/")("Tucker would hold Washington accountable for securing the border"), "hold Washington strictly accountable for the things only the federal government can do: securing the border"))
cand("CA-H-05", "CA-H-05:masuda", "Michael Masuda", "D", None,
     ("ene-08", 1, site("Michael Masuda", "https://www.votemasuda.com/")("Masuda would reduce wildfire risk"), "rural California deserves a representative who will fight to lower costs, keep hospitals open, reduce wildfire risk"))
VANG = site("Mai Vang", "https://www.maiforus.com/")
cand("CA-H-07", "CA-H-07:vang", "Mai Vang", "D", "Sacramento City Council member and teacher; a daughter of Hmong refugees.",
     ("hea-01", 2, VANG("Vang would pass Medicare for All"), "one with the guts to pass Medicare for All"),
     ("imm-08", -1, VANG("Vang opposes the mass deportation machine"), "our immigrant neighbors face a mass deportation machine"))
RECILE = site("Rudy Recile", "https://rudyforuscongress.com/")
cand("CA-H-08", "CA-H-08:recile", "Rudy Recile", "R", None,
     ("edu-06", 1, RECILE("Recile supports school choice"), "Education and School Choice"),
     ("eco-07", 1, RECILE("Recile says government spending is out of control"), "Government spending is out of control."),
     ("ene-03", 1, RECILE("Recile objects to shutting fossil fuel power plants"), "The left vilifies the use of carbon fuels and as a result power plants are being shut down."))
FRESE = site("Jeff Frese", "https://freseforcongress.com/")
cand("CA-H-10", "CA-H-10:frese", "Jeff Frese", "R", None,
     ("gov-01", 2, FRESE("Frese wants 8-year term limits"), "8-year term limits."),
     ("gov-02", 2, FRESE("Frese would ban members from trading stocks"), "Ban members of Congress from trading stocks."),
     ("gov-09", 1, FRESE("Frese would close the revolving door to lobbying"), "Close the revolving door. No cashing out as a lobbyist."))
WIENER = site("Scott Wiener", "https://www.scottwiener.com/")
cand("CA-H-11", "CA-H-11:wiener", "Scott Wiener", "D", "State senator from San Francisco and a leader of California’s pro-housing (YIMBY) movement.",
     ("hea-01", 2, WIENER("Wiener supports Medicare for All"), "We need Medicare for All."),
     ("hea-06", 1, WIENER("Wiener forced insurers to cover mental health care"), "forcing insurance companies to cover mental healthcare"),
     ("imm-08", -2, WIENER("Wiener would abolish ICE"), "In Congress, Scott will fight to protect our immigrant neighbors and ABOLISH ICE!!!"),
     ("hou-04", 2, WIENER("Wiener wrote California’s housing streamlining laws"), "authoring California's most consequential streamlining laws resulting in the construction of tens of thousands of homes"),
     ("soc-12", 2, WIENER("Wiener would fight for LGBTQ people"), "to fight for LGBTQ people and vulnerable communities"))
cand("CA-H-11", "CA-H-11:chan", "Connie Chan", "D", "San Francisco supervisor, endorsed by Nancy Pelosi.")
cand("CA-H-12", "CA-H-12:joyce", "Jamie Joyce", "D", "AI researcher and founding executive director of the Society Library, a nonprofit.")
HOELTER = site("Charles Hoelter", "https://www.hoelterforuscongress.com/")
cand("CA-H-15", "CA-H-15:hoelter", "Charles Hoelter", "R", None,
     ("ene-03", 1, HOELTER("Hoelter supports American energy production"), "Charles supports American energy production to lower costs"),
     ("def-03", 1, HOELTER("Hoelter wants better health care for veterans"), "Our veterans deserve better healthcare, better support"),
     ("eco-07", 1, HOELTER("Hoelter would fight for lower taxes and less spending"), "Charles will fight for lower taxes, reduced government spending"),
     ("cri-01", 1, HOELTER("Hoelter supports law enforcement"), "Charles supports law enforcement"),
     ("imm-01", 1, HOELTER("Hoelter calls a secure border a national security issue"), "A secure border is a national security issue and must be treated as one"))
cand("CA-H-18", "CA-H-18:lewis", "Shane Lewis", "R", "Marine Corps veteran (a qualified paratrooper) in San Jose for 28 years.")
cand("CA-H-19", "CA-H-19:verbica", "Peter Coe Verbica", "R", "Wealth manager (a managing director at Silicon Private Wealth) and author.")
cand("CA-H-21", "CA-H-21:kirkland", "Kyle Kirkland", "R", "Cardroom executive and president of the California Gaming Association; endorsed by the Fresno Police Officers’ Association.")
cand("CA-H-23", "CA-H-23:hodge", "Tessa Lynn Hodge", "D", "Licensed clinical social worker with nearly a decade working with foster children and students.",
     ("hea-06", 1, site("Tessa Hodge", "https://www.tessaforca.com/")("Hodge would prioritize mental health"), "Prioritizing Mental Health"))
cand("CA-H-26", "CA-H-26:irwin", "Jacqui Irwin", "D",
     "State Assembly member who chairs the Joint Legislative Committee on Climate Change Policies and the Select Committee on Cybersecurity.",
     ("ene-06", 1, site("Jacqui Irwin", "https://jacquiirwin.com/")("Irwin helped reauthorize California’s cap-and-trade climate law, as an endorser on her site notes"), None),
     ("def-03", 1, site("Jacqui Irwin", "https://jacquiirwin.com/")("Irwin wrote Proposition 1, which funds housing for homeless veterans, an endorser on her site notes"), None))
GIBBS = site("Jason Gibbs", "https://www.jasongibbsforcongress.com/")
cand("CA-H-27", "CA-H-27:gibbs", "Jason Gibbs", "R", "Santa Clarita City Council member and engineer who helped build rocket fueling systems.",
     ("eco-01", -1, GIBBS("Gibbs opposes new taxes"), "Jason will fight to lower the cost of living by opposing new taxes"),
     ("cri-01", 1, GIBBS("Gibbs would support law enforcement against soft-on-crime policies"), "Jason will support law enforcement and stand up to the “soft-on-crime” policies"),
     ("eco-07", 1, GIBBS("Gibbs would hold government accountable for wasteful spending"), "holding government accountable for wasteful spending"))
TORRES_CA = site("Angela Gonzales-Torres", "https://www.angela4congress.com/")
cand("CA-H-34", "CA-H-34:gonzales-torres", "Angela Gonzales-Torres", "D", "Grew up in Section 8 housing after her father was deported.",
     ("imm-08", -2, TORRES_CA("Gonzales-Torres would end ICE and for-profit prisons"), "Abolition: Ending ICE & for-profit prisons"),
     ("eco-01", 2, TORRES_CA("Gonzales-Torres backs a billionaire tax"), "Progressive tax policies and a billionaire tax to make the wealthy pay their fair share"),
     ("eco-12", 2, TORRES_CA("Gonzales-Torres backs progressive tax policies"), None),
     ("gov-13", -2, TORRES_CA("Gonzales-Torres would abolish super PACs and overturn Citizens United"), "she's fighting to abolish Super PACs, overturn Citizens United"),
     ("gov-11", 2, TORRES_CA("Gonzales-Torres would bar utilities and contractors from funding campaigns"), None),
     ("hou-01", 2, TORRES_CA("Gonzales-Torres wants guaranteed housing vouchers and community land trusts"), "she's fighting for a federal housing system built on vouchers as a guarantee, community land trusts"),
     ("ene-08", 1, TORRES_CA("Gonzales-Torres wants bold investment in climate resilience"), "Bold investment in climate response and resilience to protect communities"))
cand("CA-H-36", "CA-H-36:brignano", "Houston Brignano", "R", "Marine Corps veteran with two tours in Iraq; a South Bay native.",
     ("edu-03", 1, site("Houston Brignano", "https://www.voteforhouston.com/")("Brignano would fund reskilling for workers facing automation"), "protect jobs from automation through smart policies and reskilling programs"))
MOTA = site("Samantha Mota", "https://www.motaforcongress.com/")
cand("CA-H-37", "CA-H-37:mota", "Samantha Mota", "D", None,
     ("imm-08", -2, MOTA("Mota would dismantle ICE"), "Dismantle ICE and end for-profit detention"),
     ("hea-01", 2, MOTA("Mota would fight for universal health care"), "To renew the efforts of universal health care, we will fight for"),
     ("hea-07", 1, MOTA("Mota would repeal the Medicaid and ACA subsidy cuts"), "Repeal Medicaid and ACA Subsidy cuts"),
     ("edu-05", 1, MOTA("Mota supports student loan forgiveness"), "Student Loan Forgiveness and Tuition Costs"))
cand("CA-H-38", "CA-H-38:solis", "Hilda Solis", "D", "Los Angeles County supervisor; U.S. labor secretary from 2009 to 2013 and a congresswoman before that.")
CLEMMONS = site("Mitch Clemmons", "https://electmitchclemmons.com/")
cand("CA-H-41", "CA-H-41:clemmons", "Mitch Clemmons", "R", None,
     ("hou-04", 1, CLEMMONS("Clemmons would lower barriers that raise housing costs"), "Lower barriers that increase housing costs and expand practical paths to homeownership for working families."),
     ("cri-01", 1, CLEMMONS("Clemmons supports law enforcement and secure borders"), "Support law enforcement, first responders, secure borders, and policies focused on public safety."),
     ("imm-01", 1, CLEMMONS("Clemmons supports secure borders"), None))
BURLEY = site("Brian Burley", "https://www.burley4congress.com/")
cand("CA-H-42", "CA-H-42:burley", "Brian Burley", "R", "Huntington Beach City School District trustee who works in information technology and higher education.",
     ("eco-02", 1, BURLEY("Burley would advocate tax relief for families"), "Advocate for Tax Relief to Families and Business Owners"),
     ("cri-01", 1, BURLEY("Burley fully supports law enforcement"), "Fully Support Our Law Enforcement and Our Military"))
PAN_CA = site("David Pan", "https://www.davidpan4congress.com/")
cand("CA-H-46", "CA-H-46:pan", "David Pan", "R", None,
     ("edu-06", 2, PAN_CA("Pan supports charter schools and vouchers"), "I support charter schools and school vouchers to allow all parents to choose the best education for their children."),
     ("cri-01", 1, PAN_CA("Pan would recruit more police"), "we need to recruit more police and enforce our laws"),
     ("imm-01", 1, PAN_CA("Pan would secure the border"), "we need to secure our border"),
     ("eco-08", 1, PAN_CA("Pan would cut taxes on small businesses"), "Reducing taxes and regulations on small businesses will create jobs and renew our communities."),
     ("eco-07", 1, PAN_CA("Pan wants to confront the national debt"), "The United States has a debt problem."))
cand("CA-H-50", "CA-H-50:cohen", "Steve Cohen", "R", "Veteran San Diego television journalist (KUSI) with five decades in broadcasting.")
cand("CA-H-51", "CA-H-51:cabrera", "Ricardo Cabrera", "R", None,
     ("gov-01", 2, site("Ricardo Cabrera", "https://www.cabreraforcongress2026.com/")("Cabrera supports congressional term limits"), "I support congressional term limits because fresh leadership creates greater accountability"))

# The rest: campaign sites in states with only a few challengers left
BRONIN = site("Luke Bronin", "https://broninforcongress.com/")
cand("CT-H-01", "CT-H-01:bronin", "Luke Bronin", "D", "Former mayor of Hartford.",
     ("imm-08", -2, BRONIN("Bronin would abolish ICE"), "Abolishing ICE & Fixing Our Immigration System"),
     ("hea-01", 1, BRONIN("Bronin is pushing for universal health care"), "Protecting Medicare, Medicaid, & Pushing for Universal Healthcare"),
     ("soc-07", 1, BRONIN("Bronin wants affordable child care and elder care"), "Affordable Childcare & Eldercare"),
     ("eco-06", 1, BRONIN("Bronin would build modern infrastructure"), "Building Modern Infrastructure"))
LANCIA = site("Chris Lancia", "https://lanciaforcongress2026.org/")
cand("CT-H-03", "CT-H-03:lancia", "Chris Lancia", "R", "Coast Guard veteran from Bridgeport who lives in Milford.",
     ("imm-01", 1, LANCIA("Lancia calls border security national security"), "I believe that border security is national security"),
     ("def-13", -1, LANCIA("Lancia puts America first, “not Ukraine”"), "I believe in putting America First —not China, not Ukraine, not the United Nations."))
GOLDSTEIN = site("Michael Goldstein", "https://goldsteinforcongress.com/")
cand("CT-H-04", "CT-H-04:goldstein", "Michael Goldstein", "R", "Surgeon for more than 30 years.",
     ("hea-04", 1, GOLDSTEIN("Goldstein blames regulation for eliminating competition in health care"), "Healthcare costs are high because government regulation has eliminated competition."),
     ("ene-03", 1, GOLDSTEIN("Goldstein objects to federal limits on natural gas pipelines into New England"), "Federal policy has blocked natural gas pipeline capacity into New England."))
SHEA = site("Chris Shea", "https://chrissheaforcongress.com/")
cand("CT-H-05", "CT-H-05:shea", "Chris Shea", "R", "Navy SEAL veteran, former Pentagon official, firefighter and paramedic.",
     ("eco-07", 1, SHEA("Shea would cut wasteful spending"), "cut wasteful spending in Washington"),
     ("cri-01", 1, SHEA("Shea would support law enforcement"), "support law enforcement"))
cand("DE-H-00", "DE-H-00:arminio", "Joseph Arminio", "R", None,
     ("def-07", 1, site("Joseph Arminio", "https://drjoeforcongress.com/")("Arminio would stop endless wars"), "stop endless wars"))
cand("CO-H-06", "CO-H-06:mcmahon", "Patty McMahon", "L", "Serves on several Colorado nonprofit and civic boards.")
GROSSI = site("Gary Grossi", "https://www.votegarygrossi.com/")
cand("MA-H-03", "MA-H-03:grossi", "Gary Grossi", "R", "Retired Army colonel who grew up in Cambridge’s Corcoran Park housing project.",
     ("hou-04", 1, GROSSI("Grossi would stop regulations that limit housing supply"), "Stop unrealistic regulations that drive up housing costs and limit supply."),
     ("cri-01", 1, GROSSI("Grossi supports law enforcement and community mental health services"), "Supporting law enforcement with community partnerships"),
     ("hea-06", 1, GROSSI("Grossi supports community-based mental health services"), "community-based mental health services"))
cand("MA-H-04", "MA-H-04:stalcup", "Thomas Stalcup", "R", "A former Bernie Sanders supporter now running as an anti-war Republican, as his site puts it.",
     ("def-07", 1, site("Tom Stalcup", "https://tomstalcup.com/")("Stalcup’s site describes him as an anti-war Republican"), None))
KOH = site("Dan Koh", "https://www.kohforcongress.com/")
cand("MA-H-06", "MA-H-06:koh", "Dan Koh", "D", None,
     ("hea-01", 1, KOH("Koh supports universal health care through default Medicare enrollment"), "I support universal healthcare – and a Medicare for All system that enrolls all Americans by default and preserves private insurance if desired."),
     ("hou-01", 1, KOH("Koh would prioritize building affordable homes"), "Housing will become more affordable if we prioritize building more homes that people can actually afford."),
     ("imm-08", -1, KOH("Koh condemns masked ICE agents"), "send masked ICE agents to murder our neighbors"))
cand("MA-H-08", "MA-H-08:walters", "Rasheed Walters", "I", None,
     ("hou-08", 1, site("Rasheed Walters", "https://www.voterasheed.com/")("Walters would fix potholes"), "The War on Potholes: Because Drivers Shouldn't Have to Replace Rims Every Spring"))
MACALLISTER = site("Tyler MacAllister", "https://www.macallister4congress.com/")
cand("MA-H-09", "MA-H-09:macallister", "Tyler MacAllister", "R", "Has fished off the South Coast for more than 40 years.",
     ("eco-07", 1, MACALLISTER("MacAllister would cut waste in Washington"), "Cut the waste, end the games"),
     ("def-03", 1, MACALLISTER("MacAllister would honor promises to veterans"), "Honor the promises made to those who served"))
cand("HI-H-01", "HI-H-01:berning", "Nathan Berning", "I", "Pregnancy-support advocate who helps women in financial crisis who want to keep their babies.")
CONLEY = site("Jordan Conley", "https://www.jordanforhawaii.com/")
cand("HI-H-01", "HI-H-01:conley", "Jordan Conley", "G", "Coach, fitness professional, teacher and community organizer.",
     ("eco-03", 1, CONLEY("Conley supports a higher minimum wage and a basic income"), "Higher Minimum Wage / Universal Basic Income (UBI)"),
     ("hou-01", 1, CONLEY("Conley supports Housing First for homelessness"), "Homelessness - Housing First"),
     ("gov-07", 1, CONLEY("Conley supports ranked-choice voting and public campaign financing"), "Ranked Choice Voting / Campaign Public Finance"),
     ("gov-11", 1, CONLEY("Conley supports public campaign financing"), None))
LITTLE = site("Matt Little", "https://littleforcongress.com/")
cand("MN-H-02", "MN-H-02:little", "Matt Little", "D", "Former Lakeville mayor and state senator; owns a law firm representing seniors and people with disabilities.",
     ("hea-01", 2, LITTLE("Little is fighting for Medicare for All"), "I’m fighting for Medicare for All"),
     ("eco-01", 2, LITTLE("Little would tax the ultrawealthy"), "That’s why I’m fighting for progressive policies like Medicare for All, affordable childcare, tax breaks for everyday Americans, and a tax on the ultrawealthy."),
     ("soc-07", 1, LITTLE("Little supports affordable child care"), None),
     ("eco-02", 1, LITTLE("Little supports tax breaks for everyday Americans"), None),
     ("gov-13", -2, LITTLE("Little would end Citizens United and dark money"), "an end to Citizens United and the dark money that flows through our government"))
PRATT = site("Eric Pratt", "https://www.ericprattmn.com/")
cand("MN-H-02", "MN-H-02:pratt", "Eric Pratt", "R", "State senator since 2012 and former banker at Target and U.S. Bank; earlier on the Prior Lake–Savage school board.",
     ("soc-07", 1, PRATT("Pratt has worked in the state Senate to expand child care access"), "expanding childcare access and affordability"),
     ("cri-01", 1, PRATT("Pratt supports law enforcement"), "Eric Pratt supports law enforcement, first responders"))
BASS = site("Tyler Bass", "https://bassforcongress.com/")
cand("MN-H-03", "MN-H-03:bass", "Tyler Bass", "R", "Former licensed life and health insurance agent and lifelong gun owner.",
     ("imm-08", 2, BASS("Bass would deport every illegal immigrant and fully support ICE"), "Deport every illegal immigrant, no matter how long they've been here. Support ICE and law enforcement, 100%."),
     ("imm-02", -2, BASS("Bass would deport immigrants however long they have been here"), None),
     ("imm-01", 2, BASS("Bass would secure the border"), "Secure the border."),
     ("imm-03", -1, BASS("Bass would cut H-1B loopholes"), "Cut the H-1B loopholes."),
     ("hea-04", 1, BASS("Bass wants people to pay for their own risk in fully underwritten policies"), "Pay for your own risk — not someone else's."))
NAGEL = site("John Nagel", "https://nagelforcongress.com/")
cand("MN-H-05", "MN-H-05:nagel", "John Nagel", "R", "Law enforcement officer.",
     ("eco-07", 1, NAGEL("Nagel would cut taxes and eliminate waste"), "I will cut taxes, fight inflation, eliminate fraud and waste"),
     ("cri-01", 1, NAGEL("Nagel wants police to get the funding they deserve"), "our men and women in blue receive the funding and support they deserve"),
     ("imm-01", 2, NAGEL("Nagel would lock down the border"), "In Congress, I will fight to make sure our border is locked down so tightly that Democrats can never tear it open again."))
JACKSON_MN = site("DeVelle Jackson", "https://jacksonforcongress.us/")
cand("MN-H-05", "MN-H-05:jackson", "DeVelle Jackson", "I", None,
     ("soc-08", 2, JACKSON_MN("Jackson would ban unauthorized sales of personal data"), "A ban on unauthorized data sales and compensation when personal data is knowingly monetized"),
     ("eco-01", 1, JACKSON_MN("Jackson proposes a tax on the rich"), "Rich Tax & Civic Service"))
CHAPIN = site("Doug Chapin", "https://www.chapinforcongress.com/")
cand("MN-H-06", "MN-H-06:chapin", "Doug Chapin", "D", None,
     ("hea-01", 2, CHAPIN("Chapin would fight for single-payer health care"), "I will fight for single-payer healthcare (like Medicare for All)"),
     ("def-12", -1, CHAPIN("Chapin would withhold or restrict aid to Israel until the Gaza war ends"), "I support withholding or restricting aid to Israel until it ends its war of terror in Gaza."),
     ("def-11", -2, CHAPIN("Chapin calls the Israeli government out of control"), "the current Israeli government is completely out of control"),
     ("eco-01", 2, CHAPIN("Chapin would eliminate the Social Security tax cap"), "I will fight to eliminate the cap on Social Security taxes"),
     ("hea-05", 1, CHAPIN("Chapin objects to cuts in federal medical research"), None))
OSBERG = site("Erik Osberg", "https://www.erikosberg4congress.com/")
cand("MN-H-07", "MN-H-07:osberg", "Erik Osberg", "D", None,
     ("gov-13", -2, OSBERG("Osberg backs an amendment ending Citizens United"), "We believe in a constitutional amendment ending Citizens United."),
     ("gov-02", 1, OSBERG("Osberg would ban individual stock trading by members"), "We believe in banning individual stock trading for congress."),
     ("gov-11", 1, OSBERG("Osberg wants dark money out of politics"), "We want dark money out of politics."),
     ("edu-01", 1, OSBERG("Osberg would protect and expand federal support for public schools"), "Protect & expand strong federal support for public schools"))
cand("LA-H-04", "LA-H-04:gromlich", "Matt Gromlich", "D", "Educator.",
     ("soc-07", 1, site("Matt Gromlich", "https://mattgromlichforcongress.com/")("Gromlich would reduce child care costs"), "This means lowering housing costs, lowering the cost of groceries, bringing down gas prices, lowering utility costs, and reducing the cost of childcare."))
cand("LA-H-05", "LA-H-05:cathey", "Stewart Cathey Jr.", "R", "State senator and Army engineer officer with two deployments to Afghanistan.")
cand("LA-H-05", "LA-H-05:wilson", "Antonio Wilson", "D", None,
     ("eco-06", 1, site("Antonio Wilson", "https://wilsonforlouisiana.com/")("Wilson runs on a Builder’s Agenda of infrastructure"), "We focus on economic development, modern infrastructure, stronger healthcare, resilient rural communities"))
cand("MS-H-01", "MS-H-01:johnson", "Cliff Johnson", "D", "Former Justice Department health care fraud coordinator in Mississippi; a Columbia Law graduate.")
cand("MS-H-02", "MS-H-02:eller", "Ron Eller", "R", "Military veteran (20 years) who has worked 20 years in private health care and started manufacturing businesses.",
     ("cri-05", 1, site("Ron Eller", "https://www.voteroneller.com/")("Eller would reform prisons so inmates become productive"), "By reforming the prison population we can make them productive members of society."))
CHIARADIO = site("Michael Chiaradio", "https://michaelachiaradio.com/")
cand("MS-H-03", "MS-H-03:chiaradio", "Michael Chiaradio", "D", None,
     ("eco-06", 1, CHIARADIO("Chiaradio would invest in factories, farms and infrastructure"), "America’s future depends on our federal government’s ability to invest in factories, farms, and infrastructure."),
     ("agr-03", 1, CHIARADIO("Chiaradio would expand American factories"), None))
cand("MS-H-04", "MS-H-04:boyanton", "Carl Boyanton", "I", "Co-founder of Farmed Fresh for Mississippi, a nonprofit delivering food to veterans and families.")
cand("MS-H-04", "MS-H-04:hulum", "Jeffrey Hulum III", "D", "Retired Army sergeant major (22 years) from Gulfport; founder of the nonprofit Extend A Hand, Help A Friend.")
cand("ND-H-00", "ND-H-00:neville", "Helene Neville", "I", "Has worked for decades in hospitals and public health.",
     ("soc-07", 1, site("Helene Neville", "https://heleneforcongress.com/")("Neville addresses rising child care costs"), "Childcare and Working Families"))
WILLIAMS_NH = site("Lily Tang Williams", "https://www.lilytangwilliams.com/congress/")
cand("NH-H-02", "NH-H-02:williams", "Lily Tang Williams", "R", "Manages rental properties with her husband in Weare and works part-time as an expert witness on China-related cases.",
     ("gov-02", 2, WILLIAMS_NH("Williams would ban stock trading by members and their families"), "Prohibit members of Congress, their spouses, and dependent children from trading individual stocks while in office."),
     ("eco-07", 2, WILLIAMS_NH("Williams supports a balanced budget amendment"), "Pass a constitutional amendment requiring the federal government to balance its budget"),
     ("gov-12", 1, WILLIAMS_NH("Williams wants real-time disclosure of trades, contributions and lobbying"), "Require immediate public disclosure of all stock trades, campaign contributions, and lobbying contacts"),
     ("gov-03", 1, WILLIAMS_NH("Williams wants immediate disclosure of campaign contributions"), None))
cand("NV-H-01", "NV-H-01:john", "Steven St. John", "I", "Hospital chaplain in Las Vegas.")
cand("NV-H-04", "NV-H-04:whipple", "Cody Whipple", "R", "Hiko rancher who runs a regional communications network company.")
JACKLEY = site("Marty Jackley", "https://martyjackley.com/")
cand("SD-H-00", "SD-H-00:jackley", "Marty Jackley", "R", "South Dakota attorney general, raised in Sturgis.",
     ("cri-01", 1, JACKLEY("Jackley would back police, sheriffs and prosecutors"), "In Congress I will back our police, sheriffs, and prosecutors with the tools and the respect they have earned."),
     ("imm-01", 2, JACKLEY("Jackley would finish the wall"), "Secure the border, finish the wall, and let law enforcement do its job."),
     ("eco-02", 1, JACKLEY("Jackley would cut taxes"), "Secure the border, cut taxes, and put America first."))
cand("SD-H-00", "SD-H-00:gronli", "Nikki Gronli", "D", None,
     ("edu-03", 1, site("Nikki Gronli", "https://www.nikkigforsd.com/")("Gronli would invest in career and technical training"), "investing in education, career and technical training, apprenticeships"))
cand("VT-H-00", "VT-H-00:malloy", "Gerald Malloy", "R", "West Point graduate and retired Army officer (22 years); the 2022 Republican nominee for U.S. Senate.")
SEYMOUR = site("Suz Seymour", "https://ruokvt.com/")
cand("VT-H-00", "VT-H-00:seymour", "Suz Seymour", "I", None,
     ("eco-07", 1, SEYMOUR("Seymour would eliminate fraud and waste"), "I’ll work to eliminate fraud, waste, and abuse in Washington"),
     ("gov-12", 1, SEYMOUR("Seymour wants transparent government"), "I’ll fight for election integrity, transparent government"),
     ("hea-06", 1, SEYMOUR("Seymour supports better mental health resources"), "better mental health resources"),
     ("eco-06", 1, SEYMOUR("Seymour would bring federal infrastructure money to Vermont"), "bring federal resources to Vermont that strengthen our infrastructure"))
cand("VT-H-00", "VT-H-00:walton", "Ryan Walton", "I", "Vermont property rehabilitator and software developer.")
GEORGE = site("Vince George", "https://www.vincegeorgeforcongress.com/")
cand("WV-H-01", "WV-H-01:george", "Vince George", "D", "Former teacher.",
     ("eco-03", 1, GEORGE("George objects that the minimum wage has stayed at $8.75"), "Minimum wage has stayed at $8.75."),
     ("hea-03", 1, GEORGE("George opposes the cuts to Medicaid"), None))
cand("WV-H-02", "WV-H-02:parsi", "Ace Parsi", "D", "Iranian-American who fled an authoritarian regime as a child and grew up in poverty in the U.S.")
cand("WY-H-00", "WY-H-00:johnson", "Shawn Johnson", "L", "Lawyer, Iraq veteran and former police officer; served two terms on the Casper City Council, including a year as vice mayor.",
     ("def-07", 1, site("Shawn Johnson", "https://www.shawnforwyoming.com/")("Johnson says sending Americans into harm’s way should be a last resort"), "He believes sending Americans into harm’s way should be a last resort."))

write("data/research/house_challengers.json",
      [{"id": rid, "partial": True, "candidates": cands} for rid, cands in RACES.items()],
      "Bios and positions for House challengers and third-party candidates, from their campaign sites and newsroom questionnaires, researched Oct. 26, 2026.", updated=READ)
