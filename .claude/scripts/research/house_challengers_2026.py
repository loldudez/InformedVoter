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

from common import P, article, page, write

READ = "2026-10-26"
READ27 = "2026-10-27"  # sites found and read a day later


def site(name, url, read=READ):
    return lambda note: page(f"{name} campaign site: {note}", url, read)


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
# Loran Ayles (R, 3rd; his KATU interview is used below) and the Pacific Greens Justin
# Filip (4th) and Andrea Townsend (5th) answered nothing and have no sites.
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
     ("def-10", 1, site("Ronnie Hopkins", "https://hopkinsforcongress.wixsite.com/ronnie-hopkins-for-c/about-5", READ27)("Hopkins supports cutting foreign aid"), "I support cutting foreign aid."),
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

# New York: campaign sites. Lewis Mizrahi (R, 8th), Joel Azumah (R, 9th) and Stylo
# Sapaskis (R, 15th) have no sites (Wilneida Negron's, 12th, turned up in VOTE411); Jomo Williams' (R, 13th)
# only attacks his opponent, and Jennifer Moore's (R, 10th) serves no https page to
# cite. Blay Tarnoff's (L, 4th) and George Marsh's (R, 5th) turned up later (below).
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

# Campaign sites found Oct. 27 through the candidates' Wikipedia articles and
# BallotReady profiles (the links are in campaign_sites_2026.py). Kymone Freeman's
# renders only in a browser; its quotes were checked against the live page.
WESLEY = site("Benjamin Wesley", "https://benwesleyforcongress.com/priorities-1", READ27)
WESLEY2 = site("Benjamin Wesley", "https://benwesleyforcongress.com/", READ27)
cand("CT-H-04", "CT-H-04:wesley", "Benjamin Wesley", "I", None,
     ("def-12", -2, WESLEY("Wesley would end all weapons sales and donations to Israel"), "Passing the \"Block the Bombs\" legislation (H.R. 3565) would be a great start to ending arms sales."),
     ("def-11", -2, WESLEY2("Wesley says U.S. taxes are paying for a genocide"), "A genocide of a people paid for with our hard earned tax-dollars."),
     ("def-01", -2, WESLEY("Wesley says America doesn’t need a trillion-dollar defense budget"), "America does not need the one trillion dollar plus annual defense budget that it currently has."),
     ("def-08", -1, WESLEY("Wesley says America doesn’t need 800 bases abroad"), "It does not need the more than 800 bases it currently maintains worldwide."),
     ("def-07", 1, WESLEY("Wesley calls for a peace conference on Israel and Palestine"), "Demand a peace conference of leading nations to establish a lasting political settlement between Palestine and Israel"),
     ("def-04", 2, WESLEY("Wesley won’t vote for war funding without a congressional war resolution"), "I will not vote for a single dollar of supplemental funding for foreign wars without a congressional war resolution"),
     ("hea-01", 2, WESLEY("Wesley would invest in Medicare for All"), "Now is the time, to invest in “Medicare for All” as a nation"),
     ("edu-01", 1, WESLEY("Wesley would bring more federal money to local schools"), "will fight to get more federal dollars into our children's schools"),
     ("hou-01", 1, WESLEY("Wesley would work to increase lower- and middle-income housing"), "ways to increase the lower to middle income housing inventory"),
     ("hou-07", 1, WESLEY("Wesley wants Connecticut to lead the nation in maglev trains"), None))
ROSADO = site("Denise Rosado", "https://rosadoforcongress.com/platform", READ27)
ROSADO2 = site("Denise Rosado", "https://rosadoforcongress.com/", READ27)
cand("DC-H-98", "DC-H-98:rosado", "Denise Rosado", "R", None,
     ("cri-01", 1, ROSADO2("Rosado wants smarter, tougher public safety policy"), "smarter, tougher public safety policy"),
     ("eco-02", 1, ROSADO("Rosado would end federal taxes on D.C. residents"), "Ending Federal taxes on residents will put more money into the pockets of every DC resident right away"),
     ("hou-04", 1, ROSADO("Rosado would cut red tape to build housing on derelict lots"), "I will advocate for new development and less bureaucracy ASAP."),
     ("gov-12", 1, ROSADO2("Rosado would hold government accountable for its spending"), "holding government accountable to responsible use of our tax dollars"))
FREEMAN = site("Kymone Freeman", "https://www.freeman4congress.com/", READ27)
cand("DC-H-98", "DC-H-98:freeman", "Kymone Freeman", "G", None,
     ("cri-01", -1, FREEMAN("Freeman would put housing, health care and education ahead of policing"), "prioritizing housing, healthcare, and education over policing and displacement"),
     ("cri-07", 1, FREEMAN("Freeman would tackle the root causes of crime with economic opportunity and mental health care"), "We will tackle the root causes by investing in economic opportunity, mental health resources, and ending the school-to-prison pipeline"))
TE_BROWN = site("Te Mayonna Brown", "https://tebrownforflorida.com/issues/", READ27)
cand("FL-H-24", "FL-H-24:brown", "Te Mayonna Brown", "R", None,
     ("edu-06", 2, TE_BROWN("Brown would give federal education money to parents to choose schools"), "putting that money directly in the hands of parents by funding students, not systems"),
     ("hou-05", 1, TE_BROWN("Brown would redirect housing money to help low-income families buy first homes"), "helping low-income families in our district buy their first home"),
     ("imm-02", 2, TE_BROWN("Brown will fight for an earned path to citizenship for Haitian residents"), "In Congress, I will fight for an earned path to citizenship."),
     ("imm-07", 2, TE_BROWN("Brown would prioritize removing criminals and threats to public safety"), "prioritizing the removal of criminals and those who pose a threat to public safety"),
     ("imm-01", 1, TE_BROWN("Brown supports securing the southern border"), "I support securing our southern border"),
     ("imm-03", -1, TE_BROWN("Brown would reserve H-1B visas for jobs Americans can’t fill"), "reserve H-1B visas for legitimate high-skill workforce needs where American workers cannot fill the position"),
     ("def-03", 1, TE_BROWN("Brown wants faster VA care and real mental health support"), "Faster care, real mental health support, and full accountability at the VA"))
STEWART = site("Rick Stewart", "https://www.rickstewart.com/drug-war/", READ27)
STEWART2 = site("Rick Stewart", "https://www.rickstewart.com/clean-iowa/", READ27)
cand("IA-H-02", "IA-H-02:stewart", "Rick Stewart", "L", "Founder of Frontier Cooperative Herbs; earlier ran for Iowa governor, U.S. Senate and Iowa secretary of agriculture as a Libertarian.",
     ("soc-05", 2, STEWART("Stewart would end the drug war, treating illegal drugs like alcohol and tobacco"), "End the Drug War"),
     ("ene-04", 1, STEWART2("Stewart says polluters should stop polluting or pay, with watershed co-ops held to clean-water results"), "the people who pollute should stop polluting, or pay for it."))
CASTILLO2 = site("Lupe Castillo", "https://castillolupe.com/values/", READ27)
cand("IL-H-04", "IL-H-04:castillo", "Lupe Castillo", "R", None,
     ("eco-02", 1, CASTILLO2("Castillo supports no tax on tips and overtime"), "I am the Only Candidate who supports NO TAX ON TIPS AND OVERTIME"),
     ("soc-12", -1, CASTILLO2("Castillo would protect women’s sports and girls’ bathrooms"), "I am the Only Candidate that will protect women’s sports and girl’s bathrooms."),
     ("edu-06", 1, CASTILLO2("Castillo supports school choice for poor families"), "I am the Only Candidate who supports school choice for poor families."),
     ("soc-11", -1, CASTILLO2("Castillo opposes gender surgery for minors without parental consent"), "protect our children from predators and from mutilation surgery of their bodies without parental consent"),
     ("cri-01", 1, CASTILLO2("Castillo supports law enforcement"), "I am the Only Candidate who supports law enforcement over criminals"),
     ("gov-05", 2, CASTILLO2("Castillo supports voter ID for voting and registration"), "supports Voter ID for voting and registration in order to prevent ongoing election fraud"))
KOVALY = site("Doc Kovaly", "https://www.doc.vote/", READ27)
cand("MI-H-01", "MI-H-01:kovaly", "Doc Kovaly", "U.S. Taxpayers", None,
     ("soc-04", 2, KOVALY("Kovaly’s campaign ads call for ending abortion"), "To end abortion, we too must show the victims."),
     ("soc-03", -2, KOVALY("Kovaly opposes abortion"), None))
MAGOON = site("Charlotte Magoon", "https://www.charlottemagoon4office.com/", READ27)
cand("MI-H-02", "MI-H-02:magoon", "Charlotte Magoon", "G", "Nurse.",
     ("hea-01", 2, MAGOON("Magoon supports Medicare for All"), "I support Medicare for All"),
     ("hea-03", 2, MAGOON("Magoon supports single-payer coverage for every American"), "a single-payer system that covers every American for medical, dental, vision, and mental health"),
     ("hea-10", 1, MAGOON("Magoon’s Medicare for All would cover dental and vision care"), None),
     ("hea-02", 2, MAGOON("Magoon would let Medicare negotiate drug prices"), "We also must allow Medicare to negotiate prescription drug prices"),
     ("eco-03", 1, MAGOON("Magoon supports raising the federal minimum wage"), "I support raising the federal minimum wage"),
     ("eco-09", 1, MAGOON("Magoon says workers have the right to organize and strike"), "Workers have the right to organize, bargain collectively, and strike without fear of retaliation."),
     ("eco-01", 1, MAGOON("Magoon would make the wealthiest Americans pay their fair share"), "I support making the wealthiest Americans and profitable corporations pay their fair share"),
     ("ene-04", 2, MAGOON("Magoon would protect the Great Lakes and defend clean air standards"), "I will fight to protect the Great Lakes from pollution, defend clean air standards"),
     ("ene-01", 2, MAGOON("Magoon would invest in clean renewable energy"), "invest in clean renewable energy that creates good-paying jobs right here in the district"),
     ("ene-03", -1, MAGOON("Magoon would stop subsidizing the fossil fuel industry"), "We must stop subsidizing the fossil fuel industry"),
     ("hou-01", 1, MAGOON("Magoon supports more affordable housing construction"), "I support expanding affordable housing construction, strengthening tenant protections, ending regulations that block new supply"),
     ("hou-06", 1, MAGOON("Magoon would strengthen tenant protections"), None),
     ("hou-04", 1, MAGOON("Magoon would end regulations that block new housing"), None),
     ("edu-02", 2, MAGOON("Magoon supports tuition-free public college"), "I support tuition-free public college and university"),
     ("edu-05", 2, MAGOON("Magoon would cancel student debt"), "canceling student debt that has become a generational anchor dragging down families"),
     ("edu-01", 1, MAGOON("Magoon would fully fund public schools"), "fully funding public schools so that a child's ZIP code does not determine the quality of their education"),
     ("edu-04", 1, MAGOON("Magoon says teachers deserve to be paid like it"), "Teachers do one of the most important jobs in our society and deserve to be paid like it."),
     ("def-07", 1, MAGOON("Magoon would invest in diplomacy rather than endless conflict"), "We should be investing in diplomacy, international cooperation, and the wellbeing of our veterans"),
     ("def-03", 1, MAGOON("Magoon would invest in veterans’ wellbeing"), None),
     ("gov-11", 2, MAGOON("Magoon would ban corporate political money"), "I support banning corporate political money"),
     ("gov-13", -2, MAGOON("Magoon would ban corporate political money"), None),
     ("gov-04", 1, MAGOON("Magoon would end partisan gerrymandering"), None),
     ("gov-06", 2, MAGOON("Magoon supports automatic registration and no-reason absentee voting"), "automatic voter registration at 18, no-reason absentee voting"),
     ("soc-02", 1, MAGOON("Magoon will fight for equal justice regardless of race, gender or sexual orientation"), "I will fight for equal justice under the law regardless of race, gender, sexual orientation, religion, disability, or national origin."))
SILLS2 = site("Richard Sills", "https://richardsills.com/about-richard", READ27)
cand("MI-H-02", "MI-H-02:sills", "Richard Sills", "Natural Law", None,
     ("def-10", 1, SILLS2("Sills objects to spending billions overseas while needs at home go unmet"), "allocating billions providing free education, free healthcare and infrastructure overseas while our students face double digit interest loans"))
BARNETT = site("Shafina Che Barnett", "https://www.shafinabarnettforcongress4thdistrict.com/", READ27)
cand("MI-H-04", "MI-H-04:barnett", "Shafina Che Barnett", "G", None,
     ("edu-01", 1, BARNETT("Barnett would invest in public schools"), "Investing in public schools, vocational training, and affordable higher education"),
     ("edu-03", 1, BARNETT("Barnett would invest in vocational training"), None),
     ("hou-08", 1, BARNETT("Barnett would upgrade roads and bridges"), "Upgrading roads, bridges, and safeguarding our Great Lakes and local drinking water systems."))
PETTUS = site("Mia C. Pettus", "https://pettusforcongress.org/priorities/", READ27)
cand("MI-H-08", "MI-H-08:pettus", "Mia C. Pettus", "L", "Former Philadelphia police officer and Defense Department civilian police officer; publishes the PALS Report on Substack.",
     ("gov-12", 1, PETTUS("Pettus makes transparency in federal spending, contracts and grants a priority"), "Government Transparency, Accountability & Oversight"),
     ("imm-01", 1, PETTUS("Pettus wants secure borders"), "Secure Borders. Secure Energy. Secure America."))
cand("MI-H-10", "MI-H-10:nkromo", "Kwabena Nkromo", "G", "Green Party organizer and food-policy advocate in Flint; formerly chaired an Atlanta neighborhood planning unit and ran for the Georgia House in 2012.")
SALIBA = site("Mike Saliba", "https://votesaliba.com/issues/", READ27)
cand("MI-H-10", "MI-H-10:saliba", "Mike Saliba", "L", None,
     ("def-08", -2, SALIBA("Saliba would bring U.S. troops home from around the world"), "We must initiate the return of our soldiers from around the world, including Korea, Japan, Europe, and the entire Middle East."),
     ("def-15", -2, SALIBA("Saliba opposes threats and plans to attack Iran"), "We must cease the war propaganda, threats of a blockade, and plans for attacks on Iran"),
     ("def-07", 2, SALIBA("Saliba would talk to all countries and offer friendship and trade"), "We must be willing to talk to all countries and offer friendship and trade and travel to all who are willing."),
     ("eco-07", 2, SALIBA("Saliba wants no increase in the national debt"), "I believe that there should be no increase in the national debt."),
     ("eco-05", -1, SALIBA("Saliba opposes corporate subsidies and bailouts"), "There should be no taxpayer bailouts of corporations and no corporate subsidies."),
     ("soc-08", 1, SALIBA("Saliba would deny immunity to corporations that spy on people for the government"), "We must deny immunity for corporations that spy willingly on the people for the benefit of the government."))
cand("MI-H-11", "MI-H-11:teasdale", "Ryan Teasdale", "G", "Left a 13-year corporate job to organize community wellness events with the Social Wellness Action Now group; nominated by the Green Party.")
SANDERS = site("Brenda K. Sanders", "https://www.brendaksanders.com/issues", READ27)
SANDERS2 = site("Brenda K. Sanders", "https://www.brendaksanders.com/meet_brenda_k", READ27)
cand("MI-H-12", "MI-H-12:sanders", "Brenda K. Sanders", "G", "Lawyer who practiced for 21 years in Wayne, Oakland and Washtenaw counties; a former Washtenaw County public defender.",
     ("hea-07", 1, SANDERS("Sanders would restore Medicare Part D prescription subsidies in full"), "I will immediately bring a resolution and request a vote to restore Medicare Part D Prescription Subsidies in full."),
     ("eco-03", 2, SANDERS2("Sanders wants a federal minimum wage of $25 or more"), "make sure the federal minimum wage is at 25.00 or more"),
     ("gov-06", -1, SANDERS("Sanders calls mail-in voting an albatross"), "I believe that mail-in has become somewhat of an albatross around our electoral necks."))
HOLBROOK = site("Thomas Holbrook", "https://thomasholbrook.com/where-i-stand", READ27)
cand("MO-H-04", "MO-H-04:holbrook", "Thomas Holbrook", "L", None,
     ("gov-04", 2, HOLBROOK("Holbrook would have nonpartisan committees draw district maps"), "we need to ban the practice altogether by having non-partisan committees draw up state maps"),
     ("soc-01", 1, HOLBROOK("Holbrook opposes banning TikTok or other social media"), "I oppose the banning of TikTok and any other social media platform as that is an overreach by the US Congress."),
     ("eco-10", -2, HOLBROOK("Holbrook opposes all import tariffs"), "To be clear, I oppose any tariffs against any other country for imports."),
     ("agr-07", -1, HOLBROOK("Holbrook says everybody loses in trade wars"), None),
     ("soc-05", 2, HOLBROOK("Holbrook would fully legalize marijuana"), "I would go further in supporting legislation that would fully legalize marijuana."),
     ("cri-08", 1, HOLBROOK("Holbrook would treat addiction as a medical crisis rather than a criminal one"), "treating addiction as a medical crisis instead of a criminal crisis"),
     ("edu-07", 1, HOLBROOK("Holbrook favors more local control so parents have more say"), "I am more in favor of granting more local control so that parents have more of a say in the education of their children"),
     ("edu-06", -1, HOLBROOK("Holbrook calls charter schools another form of government subsidy"), "Advocates for Charter Schools may find themselves disheartened, as this represents yet another method of government subsidization."))
HAMMER = site("Trygve Hammer", "https://www.hammerfornd.com/priorities", READ27)
cand("ND-H-00", "ND-H-00:hammer", "Trygve Hammer", "D", "Marine veteran who worked on oilfield rigs and taught science in grades 7-12 in North Dakota.",
     ("eco-01", 1, HAMMER("Hammer says corporations and the ultra wealthy must pay their fair share"), "Profitable corporations and the ultra wealthy need to be paying their fair share."),
     ("edu-01", 1, HAMMER("Hammer wants support for rural public schools"), "We need support for, rather than attacks on, the public schools"))
cand("NJ-H-03", "NJ-H-03:welzer", "Steven Welzer", "G", "Longtime Green Party activist from East Windsor who taught economics at the college level.")
JINETE = site("Andres Jinete", "https://www.andresjinete.org/about", READ27)
cand("NJ-H-12", "NJ-H-12:jinete", "Andres Jinete", "G", "Member of the Central Jersey Tenant Union who worked for years at a community library.",
     ("hou-06", 2, JINETE("Jinete is a tenant-union member who advocates rent control and tenant rights"), "a staunch advocate for rent control and tenant rights"))
KAMERATH = site("Jon Kamerath", "https://www.jonkamerath.org/", READ27)
cand("NV-H-03", "NV-H-03:kamerath", "Jon Kamerath", "Independent American", None,
     ("soc-04", 1, KAMERATH("Kamerath believes in the sanctity of human life"), "Jon believes in the sanctity of human life."),
     ("eco-02", 1, KAMERATH("Kamerath would end the federal gas tax and bar property taxes on primary homes"), "Jon wants to eliminate the Federal gas tax and put a national ban on property tax for people's primary home."))
TARNOFF = site("Blay Tarnoff", "https://tarnoff.mystrikingly.com/", READ27)
cand("NY-H-04", "NY-H-04:tarnoff", "Blay Tarnoff", "L", None,
     ("hea-04", 2, TARNOFF("Tarnoff would end government involvement in health care"), "We must end government involvement in health care and allow free market competition"),
     ("hea-03", -2, TARNOFF("Tarnoff would end government involvement in health care"), None),
     ("ene-04", -1, TARNOFF("Tarnoff says regulation protects big polluters and would restore pollution lawsuits instead"), "Government supposedly protecting the environment is tantamount to allowing the fox to guard the hen house."))
G_MARSH = site("George Marsh", "https://georgemarshforcongress.com/", READ27)
cand("NY-H-05", "NY-H-05:marsh", "George Marsh", "R", "Raised in Astoria’s public housing; a former employee of the New York City Mayor’s Office.",
     ("eco-06", 2, G_MARSH("Marsh would reintroduce the Infrastructure Investment and Jobs Act on day one"), "I will re-introduce the infrastructure investment & Jobs Act (IIJA) on day one"),
     ("hou-03", 1, G_MARSH("Marsh would invest in reliable public transit"), "Invest in reliable public transit"),
     ("edu-03", 1, G_MARSH("Marsh would expand apprenticeships in the skilled trades"), "Expand apprenticeships that connect people to good-paying careers in skilled trades"),
     ("def-03", 1, G_MARSH("Marsh would protect veterans’ earned benefits"), "Protect veterans’ earned benefits"))
FILIP = site("Justin Filip", "https://www.justin4congress.com/", READ27)
cand("OR-H-04", "OR-H-04:filip", "Justin Filip", "Pacific Green", "Scorekeeper in Eugene and secretary of the Pacific Green Party.",
     ("def-12", -2, FILIP("Filip calls for suspending all military and foreign aid to Israel"), "We call on the U.S. President and Congress to suspend all military and foreign aid, including loans and grants, to Israel"),
     ("def-11", -2, FILIP("Filip accuses Israel of apartheid toward its non-Jewish citizens"), "dismantles settler colonies and systemic apartheid toward its non-Jewish citizens"),
     ("ene-04", 1, FILIP("Filip would protect the environment and federal lands"), "We must protect our environment and our federal lands."))
R_KING = site("Rodney Joe King", "https://www.rodneykingforcongress.com/", READ27)
cand("TN-H-03", "TN-H-03:king", "Rodney Joe King", "I", "Retired Navy captain who served on the submarine USS Nathan Hale; born in Jefferson City in 1955, he now farms.",
     ("gov-02", 1, R_KING("King pledges to buy no stock and do no insider trading in office"), "I will not profit from the job, buy no stock, do no insider trading"),
     ("def-04", 2, R_KING("King says no wars without Congress’s approval"), "No wars without congress giving approval"))
cand("TN-H-03", "TN-H-03:arnold", "Dean Arnold", "I", "Author and filmmaker; his work has included pro-life activism, news publishing and screenwriting.")
PURDY = site("Angus Purdy", "https://www.anguspurdy.com/", READ27)
cand("TN-H-06", "TN-H-06:purdy", "Angus Purdy", "I", "Vanderbilt graduate who works at an Italian market in Nashville’s Hillsboro Village; grew up on a small farm in Spring Hill.",
     ("eco-01", 1, PURDY("Purdy would return to tax rates that make the ultra wealthy pay their fair share"), "We need to return to tax rates that force the ultra wealthy to pay their fair share."),
     ("eco-09", 1, PURDY("Purdy lists workers’ rights among his priorities"), None),
     ("def-04", 2, PURDY("Purdy would return war declarations and military spending to Congress"), "put declarations of war and military spending back in the hands of Congress"),
     ("gov-09", 1, PURDY("Purdy would hold officials of all parties criminally liable for corruption"), "We need to hold elected officials of all parties criminally liable for any corruption."),
     ("soc-07", 1, PURDY("Purdy lists affordable child care among his first goals"), "rent control, and affordable childcare are just the beginning"),
     ("hou-06", 1, PURDY("Purdy lists rent control among his first goals"), None),
     ("agr-01", 1, PURDY("Purdy lists farm subsidies among his first goals"), None),
     ("edu-01", 1, PURDY("Purdy lists investment in public education among his first goals"), None))


# Campaign sites that load only in a browser, read in the browser pane on Oct. 27;
# every quote was checked against the live page's text.
GRIJALVA = site("Adelita Grijalva", "https://www.adelitaforcongress.com/issues", READ27)
cand("AZ-H-07", "AZ-H-07:grijalva", "Adelita Grijalva", "D", None,
     ("imm-02", 2, GRIJALVA("Grijalva supports comprehensive immigration reform with a pathway to legalization"), "Will continue holding officials and ICE officers accountable and push for comprehensive immigration reform with a pathway to legalization."),
     ("imm-08", -2, GRIJALVA("Grijalva sponsored bills to end mandatory and family detention and phase out private detention"), None),
     ("eco-10", -2, GRIJALVA("Grijalva opposes harmful tariffs"), "Opposes harmful tariffs and wasteful border militarization that can increase costs and hurt small businesses."),
     ("imm-01", -1, GRIJALVA("Grijalva opposes wasteful border militarization"), None),
     ("eco-01", 1, GRIJALVA("Grijalva would ask the wealthy to pay their fair share"), "while asking the wealthy to pay their fair share"),
     ("eco-02", 1, GRIJALVA("Grijalva supports a larger Earned Income Tax Credit and Child Tax Credit"), None),
     ("eco-03", 2, GRIJALVA("Grijalva supports the Raise the Wage Act’s $17 minimum wage"), "including an initial $17 minimum wage tied to cost-of-living increases"),
     ("eco-09", 2, GRIJALVA("Grijalva supports the PRO Act and the right to unionize"), "and workers’ right to unionize and bargain collectively"),
     ("eco-11", 1, GRIJALVA("Grijalva supports paid family and medical leave"), "paid family medical leave, and childcare"),
     ("ene-01", 2, GRIJALVA("Grijalva supports investment in solar, wind and batteries"), "and investments in solar, wind, battery projects, green infrastructure, and multimodal transportation."),
     ("ene-04", 1, GRIJALVA("Grijalva supports stronger environmental standards"), "Supports stronger environmental standards and"),
     ("hea-07", 1, GRIJALVA("Grijalva would extend Affordable Care Act premium assistance"), "and extending premium assistance"),
     ("hea-03", 1, GRIJALVA("Grijalva would restore federal Medicaid funding"), "funding and repealing cuts that threaten coverage for 400,000 Arizonans."),
     ("hea-05", 2, GRIJALVA("Grijalva supports more medical research and opposes NIH cuts"), "and opposing cuts to the National Institutes of Health."),
     ("soc-03", 2, GRIJALVA("Grijalva supports reproductive freedom and access to medication abortion"), "Supports reproductive freedom and access to medication abortion and contraceptives"),
     ("soc-04", -2, GRIJALVA("Grijalva supports reproductive freedom and access to medication abortion"), None),
     ("edu-04", 2, GRIJALVA("Grijalva supports a national minimum salary for new teachers"), "competitive national minimum salary for first-year teachers"),
     ("edu-01", 1, GRIJALVA("Grijalva would rebuild and properly fund the Education Department"), "Opposes dismantling the Department of Education and supports rebuilding and properly funding it."),
     ("edu-06", -1, GRIJALVA("Grijalva wants accountability for private and charter schools"), "Supports accountability for private and charter schools and protecting the rights of students and educators."),
     ("def-03", 2, GRIJALVA("Grijalva would add VA resources to cut wait times and backlogs"), "Will fight for additional VA resources to reduce wait times and address benefit backlogs."),
     ("hou-05", 1, GRIJALVA("Grijalva supports down payment assistance for first-generation homebuyers"), None),
     ("hou-02", 1, GRIJALVA("Grijalva supports stronger limits on large institutional investors buying homes"), "Supports stronger restrictions on large institutional investors buying neighborhoods and driving up home prices."),
     ("hou-01", 2, GRIJALVA("Grijalva would fully fund and expand Section 8"), "fully funding and expanding Section 8"))
STERBINSKY = site("Dani Sterbinsky", "https://www.sterbinskyforcongress.com/", READ27)
cand("AZ-H-09", "AZ-H-09:sterbinsky", "Dani Sterbinsky", "D", "Navy veteran (an operations specialist on the destroyer USS Bainbridge) and certified human resources professional from Wittmann.",
     ("gov-11", 2, STERBINSKY("Sterbinsky backs a constitutional amendment overturning Citizens United"), "overturning Citizens United, ending corporate personhood, and declare that money is not speech"),
     ("gov-13", -2, STERBINSKY("Sterbinsky would end corporate personhood and declare that money is not speech"), None),
     ("hou-05", 1, STERBINSKY("Sterbinsky would help first-time buyers with down payments"), "help first-time buyers with down-payment support, provide rental assistance"),
     ("soc-07", 1, STERBINSKY("Sterbinsky would work toward affordable, quality child care"), "work toward affordable, quality childcare so no parent has to choose between a paycheck and caring for their kids"),
     ("hea-03", 1, STERBINSKY("Sterbinsky would offer a public health insurance option"), "offer a public option so families have affordable coverage"),
     ("eco-03", 1, STERBINSKY("Sterbinsky would raise the federal minimum wage"), "raise the federal minimum wage"),
     ("eco-04", 2, STERBINSKY("Sterbinsky would break up corporate consolidation and algorithmic price fixing"), "break up corporate consolidation and crack down on algorithmic price fixing"),
     ("hou-09", 1, STERBINSKY("Sterbinsky would expand rural broadband"), "Expand broadband"))
KURDIAN = site("Armen Kurdian", "https://kurdianforcongress.com/issues", READ27)
cand("CA-H-49", "CA-H-49:kurdian", "Armen Kurdian", "R", "Retired Navy captain who served 25 years, with a search-and-rescue background.",
     ("eco-07", 1, KURDIAN("Kurdian would cut wasteful government spending"), "Cut wasteful government spending"),
     ("eco-01", -1, KURDIAN("Kurdian opposes new federal taxes"), "Oppose new federal taxes"),
     ("ene-03", 1, KURDIAN("Kurdian supports responsible domestic energy production"), "Support responsible domestic energy production"),
     ("edu-03", 1, KURDIAN("Kurdian would expand trade and apprenticeship programs"), "Expand trade & apprenticeship programs"),
     ("agr-03", 1, KURDIAN("Kurdian would bring back manufacturing"), "Bring back manufacturing"),
     ("cri-01", 1, KURDIAN("Kurdian would back the police and first responders"), "Back the blue and support first responders"),
     ("def-01", 1, KURDIAN("Kurdian would fully fund national defense"), "Fully fund our national defense"),
     ("def-03", 1, KURDIAN("Kurdian would ensure veterans get quality health care"), "Ensure veterans receive quality healthcare"),
     ("gov-01", 2, KURDIAN("Kurdian supports congressional term limits"), "Support congressional term limits"),
     ("gov-12", 1, KURDIAN("Kurdian would make government transparent and accountable"), "Make government transparent and accountable"))
HUMPHREY = site("Chad Humphrey", "https://liberty4the1st.com/", READ27)
cand("CO-H-01", "CO-H-01:humphrey", "Chad Humphrey", "L", "Denver entrepreneur and self-taught programmer; a retired Marine officer who served in Operation Enduring Freedom.",
     ("eco-12", -1, HUMPHREY("Humphrey would abolish the IRS and the Federal Reserve"), "abolish the IRS, stop the corporate tax monopolies, and put your money back where it belongs"),
     ("soc-05", 1, HUMPHREY("Humphrey says government should stay out of your marijuana, phone and bank account"), "From your marijuana to your phone to your bank account, the government needs to stay out of your business."),
     ("def-08", -2, HUMPHREY("Humphrey wants no new wars and no more playing world police"), "No new wars. No more playing world police."),
     ("def-07", 1, HUMPHREY("Humphrey would keep veterans out of foreign conflicts"), "We honor our veterans by keeping them out of foreign conflicts that have nothing to do with defending our dirt."))
MANGERIS = site("Douglas Mangeris", "https://mangeris4thepeople2026.vote/", READ27)
cand("CO-H-04", "CO-H-04:mangeris", "Douglas Mangeris", "L", "Construction superintendent from Loveland and a federal firearms licensee.",
     ("gov-01", 2, MANGERIS("Mangeris supports term limits"), "It's time for term limits and fresh leadership accountable to the people."),
     ("def-10", 2, MANGERIS("Mangeris would send no foreign aid until the national debt is zero"), "NO foreign aid will be sent to ANYONE until the USA has a $0 National Debt."),
     ("def-12", -2, MANGERIS("Mangeris would send no foreign aid to anyone until the debt is paid"), None),
     ("def-13", -2, MANGERIS("Mangeris would send no foreign aid to anyone until the debt is paid"), None),
     ("eco-07", 2, MANGERIS("Mangeris wants no more generational debt"), "We need to leave this country in better shape than we found it"))
M_RYAN = site("Meredith Ryan", "https://votemeredithryan.com/", READ27)
cand("CO-H-06", "CO-H-06:ryan", "Meredith Ryan", "Unity", "Former Aurora Public Schools paraeducator with a Master of Divinity, after a 25-year career supporting legal teams.",
     ("imm-08", -2, M_RYAN("Ryan supports defunding ICE and closing detention centers"), "I support defunding ICE and closing the detention centers."),
     ("hea-01", 2, M_RYAN("Ryan supports Medicare for All"), "It is time to end tax breaks for corporations and the rich and fund universal healthcare."),
     ("eco-01", 1, M_RYAN("Ryan would end tax breaks for corporations and the rich"), None),
     ("def-12", -2, M_RYAN("Ryan pledges to end weapons sales to Israel"), "End weapon sales to Israel"),
     ("gov-02", 2, M_RYAN("Ryan pledges to ban congressional stock trading"), "Ban Congressional stock trading"),
     ("gov-01", 1, M_RYAN("Ryan signed a term limits pledge"), "Term Limits Pledge"),
     ("ene-01", 1, M_RYAN("Ryan signed the Green New Deal pledge"), "Green New Deal Pledge"),
     ("def-07", 1, M_RYAN("Ryan would uphold international law and national sovereignty"), "I will uphold international law, respect national sovereignty"))
YONCE = site("Eric Yonce", "https://www.yonceforcongress.com/top-issues", READ27)
cand("FL-H-06", "FL-H-06:yonce", "Eric Yonce", "D", "Business owner and community advocate.",
     ("hou-01", 1, YONCE("Yonce would expand affordable and workforce housing"), "Expand affordable and workforce housing while protecting renters and homeowners."),
     ("gov-02", 2, YONCE("Yonce would ban congressional stock trading"), "Fight price gouging, enforce antitrust laws, and ban congressional stock trading."),
     ("eco-04", 1, YONCE("Yonce would enforce antitrust laws"), None),
     ("edu-03", 1, YONCE("Yonce would create apprenticeships and reskilling programs"), "Create apprenticeships and reskilling programs for an economy reshaped by technology."),
     ("eco-09", 2, YONCE("Yonce would protect organizing rights and strengthen unions"), "Protect organizing rights and strengthen unions."),
     ("eco-01", 1, YONCE("Yonce would ask the wealthiest to contribute a fairer share"), "Ask the wealthiest Americans to contribute a fairer share."),
     ("hea-02", 2, YONCE("Yonce would negotiate prescription prices"), "Negotiate prescription prices and strengthen meaningful cost-of-living adjustments."),
     ("soc-03", 2, YONCE("Yonce would protect reproductive freedom"), "Protect reproductive freedom and personal medical privacy."),
     ("soc-04", -2, YONCE("Yonce would keep health decisions between patients and providers"), "Keep healthcare decisions between patients and their providers."),
     ("soc-06", 1, YONCE("Yonce would defend freedom of religion and from government-imposed religion"), "Defend freedom of religion—and freedom from government-imposed religion."),
     ("def-07", 2, YONCE("Yonce would prioritize diplomacy and partnerships"), "Prioritize diplomacy, partnerships, and genuine strategic threats."),
     ("def-08", -1, YONCE("Yonce would reduce military intervention where the U.S. isn’t directly threatened"), "Reduce military intervention when the United States is not directly threatened."),
     ("imm-01", 1, YONCE("Yonce would secure the border with technology and staffing"), "Use modern technology and proper staffing to secure borders."),
     ("imm-07", 2, YONCE("Yonce would focus enforcement on real public-safety threats"), "Focus enforcement on real public-safety threats, not contributing families and students."),
     ("imm-02", 2, YONCE("Yonce would create pathways to citizenship"), "Create clear pathways to citizenship through lasting bipartisan reform."),
     ("edu-04", 2, YONCE("Yonce would raise teacher pay"), "Raise teacher pay and help rural schools recruit and retain staff."),
     ("edu-08", 1, YONCE("Yonce would expand vocational, technical and STEM pathways"), "Expand vocational, technical, and STEM pathways tied to local careers."),
     ("ene-08", 1, YONCE("Yonce would expand resilience grants and stormwater projects"), "Expand resilience grants, stormwater projects, and green infrastructure."),
     ("def-03", 2, YONCE("Yonce would expand VA care and suicide prevention"), "Expand VA care, transitional housing, and suicide-prevention services."))
G_AUSTIN = site("George Austin", "https://votegeorgeforcongress.com/", READ27)
G_AUSTIN2 = site("George Austin", "https://votegeorgeforcongress.com/dollars-and-sense/", READ27)
G_AUSTIN3 = site("George Austin", "https://votegeorgeforcongress.com/building-opportunity/", READ27)
G_AUSTIN4 = site("George Austin", "https://votegeorgeforcongress.com/secure-our-borders/", READ27)
cand("CT-H-02", "CT-H-02:austin", "George Austin", "R", "Construction business owner with a construction management degree from Central Connecticut State University; the son of a Mexican immigrant.",
     ("eco-07", 1, G_AUSTIN("Austin wants Washington to cut waste and stop abusing the taxpayer credit card"), "do your job, cut waste, and stop abusing the taxpayer credit card with impunity"),
     ("def-03", 1, G_AUSTIN("Austin says veterans should be cared for, not left fighting the VA"), "who should be honored and cared for, not left fighting the VA."),
     ("gov-01", 1, G_AUSTIN2("Austin supports term limits"), None),
     ("eco-02", 1, G_AUSTIN2("Austin would deliver tax relief"), None),
     ("ene-10", 1, G_AUSTIN2("Austin wants energy policies that lower utility bills and rejects “extreme green ideology”"), "And I refuse to bow to extreme green ideology that relies on shame, propaganda, and fear instead of real solutions."),
     ("edu-03", 2, G_AUSTIN3("Austin would direct federal money to apprenticeships and technical education"), "In Congress, I’ll fight to direct federal funds toward apprenticeships, job training, and technical education that connect students directly with local employers."),
     ("imm-01", 1, G_AUSTIN4("Austin would strengthen border security, including physical barriers where appropriate"), "Strengthen border security and restore order."),
     ("imm-04", 1, G_AUSTIN4("Austin would increase asylum adjudication capacity to cut backlogs"), "Raising standards, reducing backlogs, and increasing adjudication capacity"),
     ("imm-03", 1, G_AUSTIN4("Austin would modernize legal immigration pathways and cut visa wait times"), "Modernize legal immigration pathways."),
     ("imm-02", 1, G_AUSTIN4("Austin would treat long-term residents differently from recent unlawful entrants"), "distinguish between recent unlawful entry and individuals who have lived, worked, and raised families here for many years"))
PERICOLA = site("James Pericola", "https://jamespericola.com/", READ27)
cand("FL-H-11", "FL-H-11:pericola", "James Pericola", "D", "Attorney and government affairs executive; a Clinton administration appointee at the National Transportation Safety Board and an early aide to Sen. Bob Graham.",
     ("hea-02", 2, PERICOLA("Pericola would let Medicare negotiate lower drug prices"), "push to let Medicare negotiate lower prescription drug costs for seniors"),
     ("hea-07", 1, PERICOLA("Pericola would protect the Affordable Care Act"), "Expand access to affordable, high-quality healthcare by protecting the Affordable Care Act."),
     ("hou-01", 1, PERICOLA("Pericola would secure federal money to combat the housing crisis"), "Secure federal funding to combat our housing crisis and lower property insurance costs."),
     ("eco-02", 2, PERICOLA("Pericola would end income taxes for people earning under $100,000"), "Work to eliminate income taxes for those making less than $100,000 a year and cut taxes for middle-class families."),
     ("gov-04", 1, PERICOLA("Pericola would end gerrymandering"), "James will fight to end gerrymandering, pass the John Lewis Voting Rights Act, and defend our democracy from MAGA attacks."))
JENKINS = site("Jennifer Jenkins", "https://jenkinsforfl.com/priorities/", READ27)
cand("FL-H-08", "FL-H-08:jenkins", "Jennifer Jenkins", "D", "Former Brevard County School Board member who defeated a co-founder of Moms for Liberty in 2020; the daughter of a corrections officer.",
     ("eco-10", -1, JENKINS("Jenkins opposes reckless tariffs"), "Oppose reckless tariffs that drive up the cost of everyday goods."),
     ("hea-03", 2, JENKINS("Jenkins would expand Medicaid"), "Expand Medicaid so Floridians aren’t forced into emergency care or medical debt."),
     ("hea-07", 2, JENKINS("Jenkins would restore and strengthen ACA subsidies"), "Restore and strengthen ACA subsidies to lower premiums immediately."),
     ("hea-08", 2, JENKINS("Jenkins would protect coverage for pre-existing conditions"), "Protect coverage for pre-existing conditions and invest in access to mental health care."),
     ("hea-06", 1, JENKINS("Jenkins would invest in access to mental health care"), None),
     ("cri-07", 1, JENKINS("Jenkins supports evidence-based strategies that reduce violence and recidivism"), "Support evidence-based public safety strategies that reduce violence and recidivism."),
     ("edu-01", 2, JENKINS("Jenkins would expand Title I and invest in teachers and classrooms"), "Expand Title I and invest in teachers, classrooms, and student mental health."))
SCRIVENER = site("Branden Scrivener", "https://brandenscrivenerfl.info/", READ27)
cand("FL-H-12", "FL-H-12:scrivener", "Branden Scrivener", "I", "Health care worker who secures insurance authorizations for patients; a father of two with a bachelor’s degree in human services.",
     ("gov-01", 2, SCRIVENER("Scrivener wants strict term limits for every office"), "All political offices need strict term limits."),
     ("gov-11", 2, SCRIVENER("Scrivener would rework campaign finance law to stop unlimited corporate spending"), "Campaign Finance law needs to be reworked to prevent unlimited corporate spending, and create clear transparency & accountability."),
     ("gov-13", -1, SCRIVENER("Scrivener would prevent unlimited corporate spending in campaigns"), None),
     ("gov-03", 1, SCRIVENER("Scrivener wants clear campaign finance transparency"), None),
     ("edu-06", -1, SCRIVENER("Scrivener says public school money shouldn’t be diverted to charter and other programs"), "Funding for public education should not be diverted to these programs."),
     ("edu-01", 1, SCRIVENER("Scrivener would invest in local public education"), "Invest in local public education"),
     ("soc-08", 1, SCRIVENER("Scrivener would require a warrant for government access to personal data"), "Your data should be protected and required to be accessed by the government with the use of a warrant."),
     ("hou-03", 1, SCRIVENER("Scrivener would expand public transportation"), "We need to expand public transportation to reduce traffic"),
     ("ene-07", 1, SCRIVENER("Scrivener would expand public transportation"), None))
R_PEOPLE = site("Robert People", "https://www.peopleforcongress.com/general-7", READ27)
R_PEOPLE2 = site("Robert People", "https://www.peopleforcongress.com/", READ27)
cand("FL-H-15", "FL-H-15:people", "Robert People", "D", "Retired Army soldier (21 years, with two tours in Iraq and one in Afghanistan) who served as an ammunition specialist and journalist; born in Baltimore in 1979.",
     ("gov-02", 2, R_PEOPLE("People would ban congressional stock trading"), "Robert is looking to support or put forth legislation to ban congressional stock trading."),
     ("hea-01", 2, R_PEOPLE("People supports Medicare for All"), "Robert will support universal healthcare to ensure that our citizens receive the healthcare they need"),
     ("def-12", -2, R_PEOPLE("People would vote against further arms for Israel"), "Robert will also always vote and/or support NO further arms being sent to Israel under this administration."),
     ("def-11", -2, R_PEOPLE("People calls Israel’s war in Gaza a genocide"), "Robert will NOT support Israel's GENOCIDE against the people of Palestine."),
     ("edu-09", 2, R_PEOPLE("People would make school breakfast and lunch free for all children"), "Robert will fight for FREE school breakfasts and lunches for ALL our children."),
     ("soc-03", 2, R_PEOPLE("People says reproductive decisions are up to a woman and her doctor"), "Reproductive health and decisions are always up to a woman and her doctor."),
     ("soc-04", -2, R_PEOPLE("People says reproductive decisions are up to a woman and her doctor"), None),
     ("hea-05", 1, R_PEOPLE("People would fund research into women’s health"), "will support federal grant funding for these initiatives"),
     ("imm-02", 2, R_PEOPLE("People wants a clearer, faster path to citizenship"), "There needs to be a much better and clearer path to citizenship"),
     ("edu-04", 2, R_PEOPLE("People would set a minimum teacher salary in every state"), "One way Robert will look to do this is to establish a minimum salary in every state."),
     ("eco-12", 1, R_PEOPLE("People would raise the Social Security tax cap"), "Robert will propose raising the Social Security tax cap."),
     ("soc-02", 1, R_PEOPLE("People says LGBTQ+ rights are human rights"), "LGBTQ+ rights are human rights, and this is not a radical concept."),
     ("ene-01", 1, R_PEOPLE("People would expand clean energy investment"), "Robert's policies on lowering utility costs, expanding clean energy investments, restoring Environmental Protection Agency (EPA) standards"),
     ("ene-04", 1, R_PEOPLE("People would restore EPA standards"), None),
     ("ene-08", 1, R_PEOPLE("People would restore FEMA programs"), None),
     ("gov-06", 1, R_PEOPLE2("People supports voting by mail"), "protecting Social Security, Medicare for All, Vote by Mail, protecting people and the environment"))
GILBERT = site("Oliver Gilbert", "https://olivergilbert.vote/issues/", READ27)
cand("FL-H-24", "FL-H-24:gilbert", "Oliver Gilbert", "D", "Miami-Dade County commissioner and former mayor of Miami Gardens; a lawyer raised in Miami Gardens.",
     ("hea-01", 2, GILBERT("Gilbert would make health care a right for every American"), "In Congress, Oliver will fight for a pathway to ensure that healthcare is a right for every American."),
     ("eco-02", 2, GILBERT("Gilbert would eliminate income taxes for working families"), "Eliminate Income Taxes for Working Families"),
     ("eco-12", 1, GILBERT("Gilbert says working families shouldn’t carry billionaires’ tax burden"), "Families who are working hard to make ends meet shouldn’t have to carry the same tax burden as billionaires."),
     ("imm-08", -2, GILBERT("Gilbert would end funding for mass deportation"), "It’s time to end funding for these shameful deportation policies and redirect that investment where it belongs: into our communities."),
     ("soc-07", 2, GILBERT("Gilbert supports universal child care and pre-K"), "Universal Childcare & Pre-K"),
     ("hou-03", 1, GILBERT("Gilbert would secure federal money to expand rapid transit"), "Expand Rapid Transit"),
     ("ene-07", 1, GILBERT("Gilbert would expand rapid transit"), None),
     ("edu-03", 2, GILBERT("Gilbert would reinvest in job training and expand apprenticeships"), "Oliver will fight in Washington to reinvest in job training"))
ANDERSEN = site("Brent Andersen", "https://brentandersenfl.com/issues/", READ27)
cand("FL-H-20", "FL-H-20:andersen", "Brent Andersen", "R", "Pompano Beach small-business owner with 16 years in the insurance industry.",
     ("imm-01", 1, ANDERSEN("Andersen opposes open borders"), "I oppose the chaos of open borders."),
     ("imm-03", 1, ANDERSEN("Andersen supports legal immigration and a functioning asylum system"), "I support legal immigration, a functioning asylum system, and real protections for families who followed the rules."),
     ("cri-01", 1, ANDERSEN("Andersen will support law enforcement"), "I will support our law enforcement and oppose policies that make our neighborhoods less secure."),
     ("soc-12", -1, ANDERSEN("Andersen faults his opponent for voting against the women’s sports bill"), "Voted against the Protection of Women and Girls in Sports Act (H.R. 28)"),
     ("soc-11", -1, ANDERSEN("Andersen faults his opponent for votes against limits on gender procedures for minors"), "Voted against criminalizing gender surgeries on minors (H.R. 3492)"),
     ("gov-02", 1, ANDERSEN("Andersen faults his opponent for voting against a congressional stock trading ban"), "Voted against banning congressional stock trading (H.R. 7008)"))
MAXIME = site("Kedner Maxime", "https://www.maximeforcongress.com/immigration", READ27)
MAXIME2 = site("Kedner Maxime", "https://www.maximeforcongress.com/healthcare", READ27)
MAXIME3 = site("Kedner Maxime", "https://www.maximeforcongress.com/education", READ27)
cand("FL-H-20", "FL-H-20:maxime", "Kedner Maxime", "Independent Party of Florida", "Pastor for 16 years and founder of a tax consulting firm (1996); a longtime radio host who came to the U.S. from Haiti in 1981.",
     ("imm-01", 1, MAXIME("Maxime wants secure borders"), "Secure borders that protect our communities."),
     ("imm-07", 2, MAXIME("Maxime would deport those who commit crimes"), "Deportation of those who commit crimes."),
     ("imm-02", 2, MAXIME("Maxime supports a pathway to citizenship for those who contribute"), "A pathway to citizenship for those who contribute to our society."),
     ("imm-04", 1, MAXIME("Maxime wants fair, faster immigration processing"), "Fair, faster processing so people who follow the rules aren't punished for doing so."),
     ("hea-08", 2, MAXIME2("Maxime would protect coverage for pre-existing conditions"), "Protect coverage for people with pre-existing conditions"),
     ("hea-01", 1, MAXIME2("Maxime calls health care a right"), "Healthcare is not a luxury. It's a right."),
     ("edu-01", 2, MAXIME3("Maxime would raise public school funding"), "Raise public-school funding so classrooms have the resources, materials, and support they need."),
     ("edu-04", 2, MAXIME3("Maxime would raise teacher salaries"), "Raise teacher salaries so we can recruit and keep the great educators our children deserve."),
     ("edu-03", 2, MAXIME3("Maxime would expand vocational and technical training"), "Expand vocational and technical training so students who don't take a four-year path still have a real path."))
DUFFIE = site("James Duffie", "https://jimduffie.com/", READ27)
cand("GA-H-04", "GA-H-04:duffie", "James Duffie", "R", "Navy veteran of the nuclear submarine service with more than 30 years in business; a DeKalb County resident.",
     ("eco-12", -1, DUFFIE("Duffie backs the FairTax, replacing income, payroll and estate taxes with a consumption tax"), "Eliminate federal income tax, payroll tax, and estate tax"),
     ("cri-01", 1, DUFFIE("Duffie supports law enforcement and first responders"), "Jim supports law enforcement, first responders, veterans"),
     ("edu-03", 1, DUFFIE("Duffie wants schools that prepare students for work and the trades"), "Jim supports education that teaches real skills, rewards responsibility, and prepares young people for work, trades, business, military service, college, and productive citizenship."),
     ("eco-07", 1, DUFFIE("Duffie faults politicians for spending money they don’t have"), "politicians keep spending money they do not have."))
ESTI = site("Kelly Esti", "https://www.kellyesti4congress.com/", READ27)
cand("GA-H-08", "GA-H-08:esti", "Kelly Esti", "D", "Navy veteran, small-business owner and former chief financial officer with a PhD.",
     ("edu-01", 1, ESTI("Esti would push for funding that keeps learning affordable"), "push for funding that keeps learning affordable"),
     ("hea-03", 1, ESTI("Esti would strengthen federal health programs and fund rural clinics"), "my role is to strengthen federal health programs, support funding for rural clinics and hospitals"),
     ("hou-09", 1, ESTI("Esti would secure federal money for broadband and transportation"), "my job is to secure federal funding for transportation and broadband projects"),
     ("eco-09", 1, ESTI("Esti would support federal labor standards and workplace protections"), "my role is to support federal labor standards, work with agencies to enforce workplace protections"),
     ("def-03", 1, ESTI("Esti would make sure veterans get the support they earned"), "My goal is to ensure that service members, veterans, and their families receive the support they have earned through their service."))
GEGEN = site("Caitlyn Gegen", "https://www.caitlynforgeorgia.com/pages/solutions.html", READ27)
cand("GA-H-09", "GA-H-09:gegen", "Caitlyn Gegen", "D", None,
     ("hea-01", 2, GEGEN("Gegen will fight for Medicare for All"), "I will fight for Medicare for All"),
     ("eco-03", 1, GEGEN("Gegen supports a livable minimum wage"), "I am committed to fighting for a livable minimum wage, expanding the stock of affordable housing, and advocating for universal healthcare."),
     ("hou-01", 1, GEGEN("Gegen would expand the stock of affordable housing"), None),
     ("eco-01", 1, GEGEN("Gegen says the wealthiest must pay their fair share in taxes"), "The Epstein Class needs to pay their fair share in taxes"),
     ("def-04", 2, GEGEN("Gegen would help Congress take back its war powers"), "I will fight to help Congress to take back its war and taxation powers."),
     ("eco-04", 2, GEGEN("Gegen would break up corporate consolidation and monopolies"), "I am committed to breaking up consolidation and monopolization in the marketplace"),
     ("eco-09", 2, GEGEN("Gegen supports the PRO Act"), "I’m committed to fighting for the PRO Act and a livable minimum wage."),
     ("imm-08", -2, GEGEN("Gegen would abolish ICE"), "Abolish ICE"),
     ("soc-02", 2, GEGEN("Gegen will fight discrimination in all forms"), "I will fight against discrimination in all forms, including in healthcare, in the workplace, in the military, and in the making of a family."),
     ("soc-12", 1, GEGEN("Gegen would protect LGBTQIA+ rights"), "I am committed to taking a proactive approach to protecting women’s rights, LGBTQIA+ rights, and the right to due process."),
     ("soc-03", 2, GEGEN("Gegen supports the Women’s Health Protection Act"), "Every woman should have the right to her own body"),
     ("soc-04", -2, GEGEN("Gegen supports the Women’s Health Protection Act"), None),
     ("ene-01", 1, GEGEN("Gegen would invest in clean energy"), "Invest in Clean Energy in Georgia"),
     ("ene-04", 1, GEGEN("Gegen would remove lead water pipes"), "I will fight for the funding we need to remove lead water pipes and ensure access to clean drinking water."),
     ("gov-11", 2, GEGEN("Gegen would cap campaign spending and overturn Citizens United"), "I will advocate for campaign spending caps and legislation that overturns the Citizens United decision."),
     ("gov-13", -2, GEGEN("Gegen would overturn Citizens United"), None),
     ("soc-08", 1, GEGEN("Gegen says license-plate-reader companies infringe on rights"), "Private companies with ALPRs are infringing on our rights, and tech companies are not acting responsibly."))
HARDEN = site("Chris Harden", "https://www.electharden.com/", READ27)
more("GA-H-11", "GA-H-11:harden",
     ("soc-03", 2, HARDEN("Harden calls reproductive freedom a fundamental right, abortion care included"), "Chris believes reproductive freedom is a fundamental right."),
     ("soc-04", -2, HARDEN("Harden calls reproductive freedom a fundamental right"), None),
     ("hea-07", 2, HARDEN("Harden would restore and expand ACA premium tax credits"), "Chris will fight to restore and expand those credits so families are not hit with higher premiums because Congress fails to act."),
     ("hea-03", 1, HARDEN("Harden would protect and strengthen Medicare and Medicaid"), "He will work to protect and strengthen Medicare and Medicaid"),
     ("hea-06", 1, HARDEN("Harden would expand access to mental health services"), "expand access to mental health services, and improve rural access to care"),
     ("hea-01", 1, HARDEN("Harden says health care should be a right"), "Healthcare should be a right, not a privilege."),
     ("eco-02", 2, HARDEN("Harden would cut middle-class taxes"), "Chris will fight for middle-class tax relief while ensuring that large corporations and the wealthiest Americans contribute their fair share."),
     ("eco-01", 1, HARDEN("Harden would make the wealthiest pay their fair share"), None),
     ("gov-11", 2, HARDEN("Harden would close loopholes that let unlimited spending overwhelm voters"), "closing loopholes that allow unlimited spending to overwhelm the voices of everyday voters"),
     ("gov-03", 1, HARDEN("Harden supports greater campaign finance transparency"), "He supports greater transparency, stronger enforcement of campaign finance laws"),
     ("eco-03", 1, HARDEN("Harden supports raising the minimum wage"), "he supports raising the minimum wage so that a full day’s work can support a stable life."),
     ("ene-04", 1, HARDEN("Harden supports clean air and clean water"), "Chris supports clean air, clean water, responsible growth"),
     ("edu-03", 1, HARDEN("Harden supports career and technical education and apprenticeships"), "Chris supports strong public schools, career and technical education, apprenticeship programs, workforce training, and affordable routes to higher education."),
     ("gov-04", 2, HARDEN("Harden supports independent redistricting commissions"), "Chris supports independent redistricting commissions that draw fair maps, respect real communities, and create more competitive elections."),
     ("def-03", 2, HARDEN("Harden would expand VA health care and cut wait times"), "Chris will work to expand access to VA healthcare and reduce wait times"),
     ("ene-01", 1, HARDEN("Harden supports expanding clean-energy development"), "He also supports modernizing the electric grid and expanding clean-energy development"),
     ("hou-08", 1, HARDEN("Harden supports investment in roads and bridges"), "Chris supports investments in roads, bridges, water systems, broadband, and traffic improvements"),
     ("gov-02", 2, HARDEN("Harden would ban stock trading by members of Congress"), "Harden supports a full ban on stock trading for members of Congress, federal judges, senior Executive Branch officials, and their immediate families."),
     ("gov-09", 2, HARDEN("Harden would bar former members of Congress from lobbying for life"), "Harden supports a lifetime ban on former members of Congress lobbying the federal government."))
J_CLARK = site("Jasmine Clark", "https://www.jasmine4ga.com/agenda", READ27)
more("GA-H-13", "GA-H-13:clark",
     ("soc-07", 1, J_CLARK("Clark would lower the price of child care and offer pre-K for all"), "Lower the Price of Childcare and Pre-K for All"),
     ("edu-01", 2, J_CLARK("Clark would increase K-12 funding"), "Increase K-12 Funding"),
     ("edu-06", -1, J_CLARK("Clark opposes diverting funding to private and charter schools"), "divert funding to unaccountable private and charter schools"),
     ("edu-03", 1, J_CLARK("Clark would invest in trades and apprenticeships"), "Investing in Trades and Apprenticeship Programs"),
     ("eco-01", 1, J_CLARK("Clark says billionaires and corporations should pay their fair share"), "Billionaires and Corporations Should Pay Their Fair Share"),
     ("eco-09", 1, J_CLARK("Clark would protect unions"), "Protect our Unions"),
     ("imm-08", -1, J_CLARK("Clark would stop unconstitutional ICE raids"), "Stop Unconstitutional ICE Raids"),
     ("soc-03", 1, J_CLARK("Clark would restore reproductive health care"), "Restore Reproductive Healthcare"),
     ("soc-12", 1, J_CLARK("Clark would protect LGBTQ+ rights"), "Protect LGBTQ+ Rights"),
     ("gov-04", 1, J_CLARK("Clark would end partisan gerrymandering"), "End Partisan Gerrymandering"),
     ("gov-02", 2, J_CLARK("Clark would ban stock trading by members of Congress"), "Ban Stock Trading by Members of Congress"),
     ("hea-05", 1, J_CLARK("Clark would restore research funding"), "Restoring Research Funding And Stand Up For Science"),
     ("def-03", 1, J_CLARK("Clark would build a world-class VA health system"), "Build a World-Class VA Health System"),
     ("ene-04", 1, J_CLARK("Clark would stop environmental racism and protect the climate"), "Stop Environmental Racism and Protect Our Climate"))
AWA = site("Brenton Awa", "https://www.votebrentonawa.com/", READ27)
AWA2 = site("Brenton Awa", "https://www.votebrentonawa.com/issues", READ27)
cand("HI-H-02", "HI-H-02:awa", "Brenton Awa", "R", "Hawaii Senate minority leader, representing Kaneohe through the North Shore of Oahu since 2022.",
     ("hou-02", 1, AWA("Awa would limit how many single-family homes corporations can buy"), "Limit the number of single family homes corporations can acquire"),
     ("hou-05", 2, AWA("Awa would create federal down payment help for first-time buyers"), "Create federal down payment assistance targeted toward first-time homebuyers in Hawaii"),
     ("hea-09", 1, AWA2("Awa would expand federally funded community health centers"), "We can expand federally funded community health centers across Hawaii that focus on care rather than copays."),
     ("eco-02", 1, AWA2("Awa would increase the child tax credit"), "Increase the child tax credit to provide greater tax relief for families."),
     ("soc-07", 1, AWA2("Awa would expand federal child care assistance"), "Expand existing federal childcare assistance so more families can receive direct help with childcare costs."),
     ("ene-10", 1, AWA2("Awa says energy policy can’t move faster than people’s ability to pay"), "Clean energy matters, but energy policy cannot move faster than people's ability to pay their bills."),
     ("agr-01", 1, AWA2("Awa would restore canceled USDA grants, including direct help for farmers"), "providing farmers with direct assistance"))
MAXWELL = site("Christian Maxwell", "https://christianmaxwellforcongress.com/Issues", READ27)
MAXWELL2 = site("Christian Maxwell", "https://christianmaxwellforcongress.com/ImmigrationStance", READ27)
MAXWELL3 = site("Christian Maxwell", "https://christianmaxwellforcongress.com/", READ27)
cand("IL-H-01", "IL-H-01:maxwell", "Christian Maxwell", "R", "Small-business owner and homeschooling mother of four.",
     ("cri-01", 1, MAXWELL("Maxwell supports stronger policing and federal public-safety grants"), "I support safer communities, stronger policing, and real accountability."),
     ("edu-07", 1, MAXWELL("Maxwell would tie federal school money to parental notice and consent while keeping local control"), "I will support federal parental-rights legislation that ties federal education funding to transparency, notice, and consent standards while preserving local control over schools."),
     ("edu-05", 1, MAXWELL("Maxwell would erase unpaid student-loan interest after 12 consecutive payments"), "After 12 consecutive payments, erase unpaid interest"),
     ("hou-05", 1, MAXWELL("Maxwell supports help for first-time homebuyers"), "Support for first-time buyers"),
     ("eco-02", 1, MAXWELL("Maxwell supports tax relief for working families"), "I support tax relief for working families, homeowners, and small businesses."),
     ("imm-01", 1, MAXWELL2("Maxwell believes in protecting the border and enforcing the law"), "in protecting our borders and enforcing the law"),
     ("def-03", 1, MAXWELL3("Maxwell would fix the VA and end the waitlists"), "Fix the VA, protect earned benefits, and end the waitlists."),
     ("soc-06", 1, MAXWELL3("Maxwell would protect the right to pray and live one’s convictions in public"), "Protect the right to pray, to gather, and to live your convictions in the public square."),
     ("eco-07", 1, MAXWELL3("Maxwell would stop runaway spending"), "Stop the spending that bills our children for a future they didn't choose."))
J_DAVIS = site("Jennifer Davis", "https://www.votejenniferdavis.com/issues", READ27)
cand("IL-H-08", "IL-H-08:davis", "Jennifer Davis", "R", "Co-founder of the software company Davisware and author of a business book; a mother of ten.",
     ("edu-06", 1, J_DAVIS("Davis supports public, charter, private and home school options"), "She supports a range of educational options—public, charter, private, or home schools—so families can choose what works best for their children."),
     ("edu-03", 1, J_DAVIS("Davis wants vocational training tied to local careers"), "as well as vocational training and business partnerships that connect students to high-paying local careers"),
     ("imm-01", 1, J_DAVIS("Davis would secure the border with advanced technology"), "secures our borders with advanced technology, enforces existing laws, and prioritizes legal immigration for skilled workers"),
     ("imm-03", 1, J_DAVIS("Davis would prioritize legal immigration for skilled workers"), None),
     ("imm-07", 2, J_DAVIS("Davis would deport criminal aliens"), "Jennifer will also work to deport criminal aliens"),
     ("def-09", 1, J_DAVIS("Davis would build a “Digital Dome” against foreign cyberattacks"), "a national shield that protects families, communities, and our military from foreign cyberattacks"),
     ("ene-03", 1, J_DAVIS("Davis would expand American oil and gas production"), "By expanding American oil, gas, and renewable production"),
     ("ene-01", 1, J_DAVIS("Davis would expand renewable production"), None),
     ("eco-08", 1, J_DAVIS("Davis would cut small-business taxes and use smart tax incentives"), "cutting excessive taxes, streamlining regulations, and opening new pathways for growth through community partnerships and smart tax incentives"))
REINHOLD = site("Lauren Reinhold", "https://www.laurenforkansas.com/priorities", READ27)
more("KS-H-01", "KS-H-01:reinhold",
     ("imm-02", 2, REINHOLD("Reinhold supports a fair path to citizenship for those already contributing"), "It’s time for common-sense immigration reform that secures our borders while providing a fair path to citizenship for those already contributing to our communities."),
     ("imm-01", 1, REINHOLD("Reinhold would secure the borders as part of immigration reform"), None),
     ("imm-04", 1, REINHOLD("Reinhold would fix backlogged immigration courts"), "By fixing backlogged courts and stabilizing our agricultural workforce"),
     ("imm-09", 1, REINHOLD("Reinhold would stabilize the agricultural workforce"), None),
     ("eco-09", 1, REINHOLD("Reinhold would strengthen workers’ rights"), "An economy truly prospers when it stops favoring corporate monopolies and starts honoring the dignity of a hard day's work."),
     ("eco-04", 1, REINHOLD("Reinhold would favor family farms over corporate monopolies"), "prioritizes producers, family operations and support the small businesses that line our main streets over corporate monopolies"))
WEIN = site("Mikel Wein", "https://www.weinforky5.com/", READ27)
more("KY-H-05", "KY-H-05:wein",
     ("eco-09", 1, WEIN("Wein says strong unions make lives better"), "They reminded me that strong unions and organizing make our lives better."),
     ("hea-01", 2, WEIN("Wein wants the Medicare for All Act passed"), "to guarantee healthcare for all and save our rural hospitals in eastern Kentucky."),
     ("gov-11", 1, WEIN("Wein wants government free of large private donations and PAC money"), "a government that has not been corrupted by large private donations, PACs, influence-peddling, or bribery."))
BOWMAN = site("Jay Bowman", "https://www.bowman2026.com/issues", READ27)
more("KY-H-06", "KY-H-06:bowman",
     ("eco-09", 1, BOWMAN("Bowman would strengthen workers’ right to organize and bargain"), "Promoting policies that protect and strengthen workers' rights to organize and bargain collectively"),
     ("hea-01", 2, BOWMAN("Bowman would design a single-payer health care system"), "Design a single-payer healthcare system that covers essential medical services"),
     ("eco-10", -1, BOWMAN("Bowman would reverse course on tariffs that hurt farmers"), "On tariffs and other economically restrictive measures."),
     ("agr-01", 1, BOWMAN("Bowman would pass the 2026 farm bill to lock in support for farms"), "lock in long-term support for Kentucky farms"),
     ("hou-09", 1, BOWMAN("Bowman would expand rural broadband"), "Expand for Smarter Farming"),
     ("gov-01", 2, BOWMAN("Bowman supports congressional term limits"), "Stop career politicians prioritizing re-election over problem-solving."),
     ("def-02", 1, BOWMAN("Bowman would work closely with allies to share the defense burden"), "Work closely with allies and partners to share resources, intelligence, and coordinate defense strategies, reducing the burden on the US military."))
HOHE = site("Steven Hohe", "https://stevehoheforkansas.wordpress.com/", READ27)
more("KS-H-03", "KS-H-03:hohe",
     ("eco-07", 2, HOHE("Hohe would get “Spartan” on spending and shrink government"), "We’ve got to get Spartan on spending, downsizing the scope of government, end corporate and foreign aid"),
     ("def-10", 2, HOHE("Hohe would end foreign aid"), None),
     ("eco-12", -2, HOHE("Hohe would replace the income tax with a flat tax of at most 10%"), "replacing it with a Flat Tax and creating a Staged Tariff System"),
     ("eco-10", 1, HOHE("Hohe would create a staged tariff system on imports"), None),
     ("edu-06", 2, HOHE("Hohe would give each child an education account controlled by parents"), "The Educational Account should follow the Child with the Parent"))
MILLERON = site("Nadia Milleron", "https://www.nadiaforcongress.com/", READ27)
cand("MA-H-01", "MA-H-01:milleron", "Nadia Milleron", "I", "Attorney and Sheffield farmer who led families of Boeing 737 MAX crash victims, her daughter among them, in pushing a 2020 aircraft safety law; won about 37% against Richard Neal in 2024.",
     ("eco-02", 2, MILLERON("Milleron would end federal income tax on earnings under $100,000"), "Nadia supports eliminating the federal income tax on earnings under $100,000, giving working people more money to keep up with rising costs."),
     ("def-10", 1, MILLERON("Milleron would vote against funding foreign wars and spend at home instead"), "Nadia will vote against sending taxpayer money to fund foreign wars."),
     ("def-12", -2, MILLERON("Milleron says U.S. tax dollars fund the destruction of Palestinian lives"), "U.S. tax dollars are funding the destruction of Palestinian lives"),
     ("def-11", -2, MILLERON("Milleron supports ending what she calls the genocide in Palestine"), "Nadia supports ending the genocide in Palestine, and equal rights for all people."),
     ("gov-11", 2, MILLERON("Milleron would keep corporations out of politics"), "Corporations should not be able to purchase political influence or determine the rules under which they operate."),
     ("gov-13", -2, MILLERON("Milleron would keep corporations out of the political process"), "Nadia supports keeping corporations out of the political process"),
     ("agr-03", 1, MILLERON("Milleron would rebuild American manufacturing"), "Nadia will work to rebuild American manufacturing with strong labor and environmental standards"),
     ("agr-04", 2, MILLERON("Milleron wants a federal medical manufacturing zone to make generic drugs"), "Nadia supports securing a Federal Medical Manufacturing Zone in the 1st District to produce generic drugs and essential hospital supplies"),
     ("hou-02", 2, MILLERON("Milleron would ban corporate speculators from buying up neighborhoods"), "capping runaway rents, banning corporate speculators from buying up local neighborhoods"),
     ("hou-06", 1, MILLERON("Milleron would cap runaway rents"), None),
     ("hou-01", 1, MILLERON("Milleron would direct federal money into community housing developments"), "directing federal funding straight into community housing developments"),
     ("hea-01", 2, MILLERON("Milleron supports Healthcare for All legislation"), "She supports Healthcare for All legislation designed to reduce healthcare costs and expand access to care for everyone including abortion and gender affirming care."),
     ("hea-04", -2, MILLERON("Milleron would remove insurance companies from their dominant role in health care"), "Nadia will push to remove corporate insurance companies from their dominant role in healthcare"),
     ("soc-03", 2, MILLERON("Milleron’s health plan would cover abortion care"), None),
     ("soc-12", 1, MILLERON("Milleron’s health plan would cover gender-affirming care"), None),
     ("gov-01", 2, MILLERON("Milleron supports term limits and would serve no more than three terms"), "I will champion term limits for politicians and lead by example, serving no more than 6 years if elected."))
M_JONES = site("Micah Jones", "https://micahqjones.com/accountability-plan/", READ27)
M_JONES2 = site("Micah Jones", "https://micahqjones.com/opportunity-plan/", READ27)
M_JONES3 = site("Micah Jones", "https://micahqjones.com/security-plan/", READ27)
cand("MA-H-06", "MA-H-06:jones", "Micah Jones", "R", "Attorney and former Army captain.",
     ("gov-02", 2, M_JONES("Jones would ban individual stock trading by members of Congress and spouses"), "Ban the trading of individual stocks by members of Congress and their spouses."),
     ("gov-09", 1, M_JONES("Jones would make members’ financial disclosures simple and searchable"), "Make financial disclosures simple, searchable, and accessible to the public."),
     ("ene-03", 1, M_JONES2("Jones would expand natural gas pipelines from Pennsylvania to New England"), "I will advocate to surge federal resources to expand critical Liquified Natural Gas"),
     ("ene-02", 2, M_JONES2("Jones would modernize nuclear permitting and accelerate next-generation nuclear"), "Modernize nuclear permitting and accelerate next-generation nuclear"),
     ("ene-01", 1, M_JONES2("Jones would expand renewables without pushing costs onto households"), "Expand renewable energy without pushing costs onto households"),
     ("ene-10", 1, M_JONES2("Jones would put affordability and reliability alongside clean energy goals"), "Prioritize affordability and reliability alongside clean energy goals"),
     ("hou-04", 1, M_JONES2("Jones would fix permitting bottlenecks that make building too slow"), "A major driver of our high costs is that it is simply too difficult, slow, and expensive to build."),
     ("imm-01", 1, M_JONES3("Jones would strengthen border enforcement with staffing and technology"), "Authorize the strengthening of border enforcement with better staffing, technology, and faster adjudication"),
     ("imm-04", 2, M_JONES3("Jones would surge immigration judges and court capacity"), "Expand court capacity to ensure timely, fair decisions."),
     ("imm-03", 1, M_JONES3("Jones would align legal immigration with workforce needs"), "Modernize legal immigration to reduce backlogs and align with current workforce needs"),
     ("cri-01", 1, M_JONES3("Jones supports police training, recruitment and retention"), "Support training, recruitment, and retention for law enforcement agencies."),
     ("cri-07", 1, M_JONES3("Jones would invest in violence prevention and mental health response"), "Invest in targeted violence prevention and coordinated mental health response systems."),
     ("def-09", 1, M_JONES3("Jones would harden cybersecurity and critical infrastructure"), "Harden Cybersecurity and Critical Infrastructure"))
AMBROSE = site("Ben Ambrose", "https://ambrose4congress.com/priorities", READ27)
cand("MI-H-02", "MI-H-02:ambrose", "Ben Ambrose", "D", "Marine Corps infantryman for nearly 20 years, with multiple combat tours; grew up on a farm in Hesperia.",
     ("hea-01", 2, AMBROSE("Ambrose supports Medicare for All"), "Ben proudly supports Medicare for All and is committed to making affordable, accessible healthcare a reality for every American."),
     ("eco-08", 1, AMBROSE("Ambrose would support small businesses with tax incentives"), "Support small businesses with tax incentives and reduced red tape"),
     ("eco-09", 1, AMBROSE("Ambrose would strengthen collective bargaining"), "Strengthen workers' rights and collective bargaining"),
     ("agr-03", 1, AMBROSE("Ambrose would bring manufacturing back through Buy American policies"), "Bring manufacturing jobs back to Michigan through 'Buy American' policies"),
     ("edu-01", 2, AMBROSE("Ambrose would increase federal funding for public schools"), "Increase federal funding for public schools and reduce class sizes"),
     ("edu-04", 1, AMBROSE("Ambrose would support teachers with better pay"), "Support teachers with better pay and professional development"),
     ("edu-03", 1, AMBROSE("Ambrose would invest in vocational training and apprenticeships"), "Invest in vocational training and apprenticeship programs"),
     ("hea-06", 1, AMBROSE("Ambrose would expand mental health and addiction treatment"), "Expand mental health services and addiction treatment"),
     ("soc-03", 1, AMBROSE("Ambrose would ensure access to reproductive health care"), "Ensure women have access to reproductive healthcare"),
     ("def-03", 1, AMBROSE("Ambrose would ensure veterans get the best health care"), "Ensuring veterans have access to the best possible health care"),
     ("ene-04", 1, AMBROSE("Ambrose would protect the Great Lakes from pollution"), "Protect the Great Lakes from pollution and invasive species"),
     ("ene-01", 1, AMBROSE("Ambrose would transition to clean energy"), "Transition to clean energy sources and reduce carbon emissions"),
     ("cri-07", 1, AMBROSE("Ambrose would invest in violence prevention and intervention"), "Invest in violence prevention and intervention programs"))
VUKASOVICH = site("Christian Vukasovich", "https://christian4michigan.com/", READ27)
cand("MI-H-05", "MI-H-05:vukasovich", "Christian Vukasovich", "D", "Teacher and union organizer who worked his way through school as a bricklayer.",
     ("eco-03", 1, VUKASOVICH("Vukasovich fights for living wages"), "Fighting for living wages, good union jobs, and an economy that rewards hard work and dignity."),
     ("eco-09", 1, VUKASOVICH("Vukasovich fights for good union jobs"), None),
     ("hea-01", 1, VUKASOVICH("Vukasovich calls affordable health care a fundamental right"), "Ensuring every person has access to quality, affordable healthcare as a fundamental right."),
     ("edu-03", 1, VUKASOVICH("Vukasovich would invest in education and workforce training"), "Investing in education, workforce training, and opportunity for all Michiganders."))
T_SMITH = site("Thomas Smith", "https://tomsmithformi.com/", READ27)
cand("MI-H-08", "MI-H-08:smith", "Thomas Smith", "R", "Former General Motors employee from Flint who founded Jar Head Salsa with his son in 2009.",
     ("imm-01", 2, T_SMITH("Smith would finish the border wall and end catch-and-release"), "Finishing the wall, restoring deportations, and ending catch-and-release to stop the national security crisis."),
     ("imm-08", 1, T_SMITH("Smith would restore deportations"), None),
     ("eco-07", 1, T_SMITH("Smith would cut wasteful spending"), "Cutting wasteful spending, reducing regulations, and lowering taxes so families keep more of what they earn."),
     ("eco-02", 1, T_SMITH("Smith would lower taxes for families"), None),
     ("soc-01", 1, T_SMITH("Smith would protect First and Second Amendment rights"), "Protecting the 1st and 2nd Amendment rights of every American against federal overreach."))
SMILEY = site("Heather Smiley", "https://smileyforcongress.com/?page_id=269", READ27)
cand("MI-H-06", "MI-H-06:smiley", "Heather Smiley", "R", "Retired after 32 years at Ford in product development and strategy; a volunteer first responder and trainer.",
     ("eco-07", 2, SMILEY("Smiley would eliminate wasteful spending and balance the budget"), "Work Smarter; Eliminate wasteful spending/departments, increase transparency & informed decisions, balance the budget."),
     ("gov-01", 2, SMILEY("Smiley wants term limits for all elected officials"), "Transparency, terms limits for all elected officials, blind-trust investments, personal/legal accountability."),
     ("gov-02", 1, SMILEY("Smiley wants officials’ investments in blind trusts"), None),
     ("soc-04", 1, SMILEY("Smiley would protect life in the womb"), "Protect life (womb, special needs, elderly)"),
     ("agr-04", 1, SMILEY("Smiley would in-source drug production"), None),
     ("imm-01", 2, SMILEY("Smiley would close the borders"), "Close the borders, remediate illegal entrants, address chain migration, protect existing guest-worker provisions."),
     ("cri-01", 1, SMILEY("Smiley would support law enforcement"), "Enable and support law enforcement to effectively perform their duties, and enforce the rule of law."),
     ("ene-04", 1, SMILEY("Smiley would protect and restore air, water and land"), "Protect and restore air/water/land, wildlife and their habitats, and the human condition"),
     ("def-01", 1, SMILEY("Smiley would rebuild the military arsenal"), "Restore/build arsenal and focus on lethality & protection from enemies both foreign and domestic."),
     ("soc-06", 1, SMILEY("Smiley would protect the free practice of religion"), "Allow the free practice of religion without fear, government overreach, and judicial bias."),
     ("agr-03", 1, SMILEY("Smiley would in-source manufacturing"), "Unleash the free market, in-source manufacturing, protect citizen jobs, and ensure reciprocal trade practices."),
     ("soc-01", 1, SMILEY("Smiley would protect unrestricted speech on all media platforms"), "Protect and ensure original, impartial & unrestricted creation and distribution amongst all media platforms."))
WIKSTROM = site("Paul Wikstrom", "https://www.wikstromforcongress.com/", READ27)
cand("MN-H-04", "MN-H-04:wikstrom", "Paul Wikstrom", "R", "Electrical engineer with 35 years in Minnesota medtech and aerospace companies.",
     ("eco-02", 2, WIKSTROM("Wikstrom would end taxes on tips and overtime and expand the child tax credit"), "eliminate tax on tips, no tax on overtime, expand child tax credits"),
     ("hea-04", 1, WIKSTROM("Wikstrom would bring back competition, including insurance sales across state lines"), "allow purchase of insurance across state lines"),
     ("agr-03", 1, WIKSTROM("Wikstrom would invest first in domestic manufacturing"), "starting with domestic manufacturing and energy independence."),
     ("edu-03", 1, WIKSTROM("Wikstrom would expand vocational training"), "prepare our children to succeed by focusing on academics, not political agendas, and expanding vocational training opportunities."),
     ("imm-01", 1, WIKSTROM("Wikstrom would enforce real border security against fentanyl"), "Enforcing real border security to keep fentanyl from flowing freely over the border"),
     ("cri-01", 2, WIKSTROM("Wikstrom would protect and expand COPS and Byrne JAG police grants"), "Protecting and expanding COPS and Byrne JAG grants to put more officers on St. Paul foot patrols and response teams."),
     ("cri-04", 1, WIKSTROM("Wikstrom wants tougher penalties for criminals who flee or attack police"), "tougher federal penalties for criminals who flee from or attack police officers"),
     ("gov-12", 2, WIKSTROM("Wikstrom would require audits of all major federal spending"), "for all major federal spending."))
DAUGHERTY = site("Brandon Daugherty", "https://bcd4mo.com/", READ27)
cand("MO-H-02", "MO-H-02:daugherty", "Brandon Daugherty", "L", None,
     ("def-12", -2, DAUGHERTY("Daugherty would send no more money to Israel"), "No more money for Israel, Ukraine, or any other \"ally.\""),
     ("def-13", -2, DAUGHERTY("Daugherty would send no more money to Ukraine"), None),
     ("def-10", 2, DAUGHERTY("Daugherty would end aid to allies"), None),
     ("eco-07", 2, DAUGHERTY("Daugherty wants no more debt"), "No More Debt."),
     ("ene-04", -1, DAUGHERTY("Daugherty would abolish the EPA"), "Abolish FBI, Dept. of Ed., EPA, you name it."),
     ("soc-01", 2, DAUGHERTY("Daugherty says government has no right to tell you what to say"), "Government has no right to tell you what to say."))
LASZACS = site("Matthew Laszacs", "https://matt4nc.us/", READ27)
cand("NC-H-02", "NC-H-02:laszacs", "Matthew Laszacs", "L", None,
     ("edu-06", 2, LASZACS("Laszacs would expand education savings accounts, vouchers and scholarships"), "Expand opportunities for parents to select the best educational options for their children through initiatives such as educational savings accounts, vouchers, and scholarships."),
     ("hou-04", 1, LASZACS("Laszacs would reduce zoning and licensing rules"), "Reduce occupational licensing rules, zoning laws, and other regulations"),
     ("hea-04", 1, LASZACS("Laszacs would bring price competition into health care"), "introduce price competition into our state healthcare system"))
ABU_GHAZALAH = site("Maad Abu-Ghazalah", "https://getmaad.org/", READ27)
cand("NC-H-07", "NC-H-07:abu-ghazalah", "Maad Abu-Ghazalah", "L", None,
     ("def-12", -2, ABU_GHAZALAH("Abu-Ghazalah would stop arming Israel"), "We need to stop arming Israel and other foreign regimes like Egypt, Jordan and the Ukraine"),
     ("def-13", -2, ABU_GHAZALAH("Abu-Ghazalah would stop arming Ukraine"), None),
     ("def-07", 2, ABU_GHAZALAH("Abu-Ghazalah would use U.S. leverage for peace through diplomacy"), "start using our leverage to create peace in the world through diplomacy"),
     ("def-08", -1, ABU_GHAZALAH("Abu-Ghazalah wants to end U.S. military involvement in the Middle East"), "Most Americans want to end our military involvement in the Middle East."))
OJEDA = site("Richard Ojeda", "https://ojedafornc.com/", READ27)
cand("NC-H-09", "NC-H-09:ojeda", "Richard Ojeda", "D", "Retired Army major and former teacher and state legislator.",
     ("def-03", 2, OJEDA("Ojeda would protect and improve VA care and veterans’ mental health support"), "Protect and improve VA care, pensions, and mental health support for veterans."),
     ("edu-04", 2, OJEDA("Ojeda would raise teacher pay"), "Raise teacher pay, cut student debt, and keep politics out of the classroom."),
     ("edu-05", 1, OJEDA("Ojeda would cut student debt"), None),
     ("hea-03", 1, OJEDA("Ojeda would strengthen Medicare and Medicaid"), "Strengthen Medicare and Medicaid, protect body autonomy."),
     ("soc-03", 1, OJEDA("Ojeda would protect bodily autonomy"), None),
     ("eco-09", 1, OJEDA("Ojeda would defend labor rights"), "Boost wages, support farmers, defend labor rights, and invest in skilled trades."),
     ("edu-03", 1, OJEDA("Ojeda would invest in the skilled trades"), None),
     ("eco-12", 1, OJEDA("Ojeda would raise the Social Security income cap"), "Raise the income cap and stop retirement age hikes."))
MAHROU = site("Robbie Mahrou", "https://livefreenh02.com/platform/", READ27)
MAHROU2 = site("Robbie Mahrou", "https://livefreenh02.com/", READ27)
cand("NH-H-02", "NH-H-02:mahrou", "Robbie Mahrou", "I", None,
     ("eco-02", 2, MAHROU("Mahrou would make every household’s first $105,000 free of federal income tax"), "the first $105,000 of every household's income free of federal income tax"),
     ("eco-05", -1, MAHROU("Mahrou would eliminate corporate welfare"), "Eliminate corporate welfare that distorts markets against small businesses and working families"),
     ("eco-10", -1, MAHROU("Mahrou would offset tariffs that act as hidden taxes"), "Offset tariffs that act as hidden taxes on groceries, building materials, and energy."),
     ("eco-07", 1, MAHROU("Mahrou would match any debt ceiling increase with spending discipline"), "to ensure any debt ceiling increase is matched with real spending discipline."),
     ("hou-04", 1, MAHROU2("Mahrou would cut federal red tape on housing"), "Cut federal red tape so young families can afford to stay in the towns they grew up in."))
MCGUIRE = site("Michael McGuire", "https://michaelmcguireforcongress.com/issues/", READ27)
cand("NJ-H-03", "NJ-H-03:mcguire", "Michael McGuire", "R", "Member of the U.S. Marine Corps.",
     ("eco-07", 1, MCGUIRE("McGuire would cut wasteful government spending"), "That starts with cutting wasteful and ineffective government spending that fuels inflation and drives up costs for everyone."),
     ("eco-02", 1, MCGUIRE("McGuire would lower taxes on middle- and working-class families"), "It means lowering the tax burden on middle- and working-class families so they can keep more of their earnings."),
     ("gov-01", 2, MCGUIRE("McGuire supports congressional term limits"), "Term limits are about restoring accountability and rebuilding trust between citizens and their government."),
     ("def-03", 1, MCGUIRE("McGuire would deliver quality health care for veterans"), "delivering high-quality, accessible healthcare, including mental health services, for veterans and their families"),
     ("def-01", 1, MCGUIRE("McGuire would fund military readiness and modernization"), "Our national defense depends on funding readiness, rigorous training, and modernization"))
RUEDA = site("Adam Rueda", "https://adamruedafornj5.com/", READ27)
cand("NJ-H-05", "NJ-H-05:rueda", "Adam Rueda", "I", "Bucknell business graduate who worked as a financial analyst at a commercial real estate brokerage; a founder of a new party, greenparty2.0.",
     ("gov-02", 2, RUEDA("Rueda would end insider trading in Congress and pledges never to own stocks in office"), "I pledge to never own stocks or crypto while serving in office."),
     ("hea-01", 2, RUEDA("Rueda supports Medicare for All"), "Universal Human Rights, Free Speech, Anti-Corruption, Pro-Earth, Pro-Health, Pro-Science, Medicare for All"),
     ("soc-03", 2, RUEDA("Rueda is pro-choice"), "We are pro-choice and defend women's right to women's healthcare."),
     ("soc-04", -2, RUEDA("Rueda is pro-choice"), None),
     ("def-12", -2, RUEDA("Rueda objects to U.S. funding of what he calls genocide"), "our country’s participation in and funding of genocide"),
     ("def-11", -2, RUEDA("Rueda cites egregious human rights violations in Gaza and the West Bank"), "We have egregious human rights violations that have occurred and are still happening now in Gaza, the West Bank and greater Palestine."),
     ("ene-04", 1, RUEDA("Rueda wants closer attention to pollution of air and water"), "It is of upmost importance that we pay much closer attention to the chemicals and pollution we are releasing into the air, our waters"),
     ("gov-11", 2, RUEDA("Rueda would severely limit corporate influence on Congress"), "We must work to severely limit corporate and international interests' impact on our Congressional processes"))
HERZIG = site("Hillary Herzig", "https://www.herzigforcongress.com/", READ27)
cand("NJ-H-06", "NJ-H-06:herzig", "Hillary Herzig", "R", "Grew up in the district; has worked with the Key West Police Department.",
     ("eco-02", 1, HERZIG("Herzig would lower taxes so families keep more of their paychecks"), "Hillary will fight for lower property taxes, reduced cost of living, and keeping more of your paycheck in your home."),
     ("soc-08", 1, HERZIG("Herzig would limit police technology used to spy on Americans"), "protect personal liberties, limit use of LE TECH to spy on Americans."),
     ("ene-04", 2, HERZIG("Herzig would reduce pollution and hold polluters accountable"), "Reduce pollution, protect drinking water, and hold polluters accountable so our communities stay healthy."),
     ("gov-01", 2, HERZIG("Herzig supports term limits"), "Term limits restore accountability, fresh thinking, and government that works for the people"),
     ("gov-02", 1, HERZIG("Herzig would ban congressional insider trading"), "Ban Congressional Insider Trading, Public office is for public service, not private profit."),
     ("eco-04", 2, HERZIG("Herzig would break up monopolies"), "Break up monopolies, restore fair competition, and put Main Street before special interests."))
BOND = site("Alan Bond", "https://hopefortomorrownj.org/", READ27)
cand("NJ-H-11", "NJ-H-11:bond", "Alan Bond", "I", None,
     ("edu-03", 1, BOND("Bond would expand training and apprenticeships"), "Expand training, apprenticeships, and pathways into careers that support families."),
     ("hou-08", 1, BOND("Bond wants safe roads and bridges and reliable transit"), "New Jersey needs reliable transit, safe roads and bridges, modern infrastructure, responsible investment, and accountability for the results taxpayers receive."),
     ("def-03", 1, BOND("Bond wants timely health care and easier benefits for veterans"), "Keeping our promise to veterans means timely healthcare, easier benefits, civilian career pathways, mental-health resources, housing stability, and support for military families."))
W_JORDAN = site("Winston Jordan", "https://www.winstonforcongress.com/", READ27)
W_JORDAN2 = site("Winston Jordan", "https://www.winstonforcongress.com/policy", READ27)
cand("NJ-H-12", "NJ-H-12:jordan", "Winston Jordan", "I", None,
     ("gov-11", 2, W_JORDAN("Jordan accepts no donations and calls his campaign an answer to Citizens United"), "It's a peaceful way to answer the Supreme Court's Citizens United decision at the ballot box"),
     ("gov-13", -2, W_JORDAN("Jordan rejects the idea that money is speech and corporations are people"), None),
     ("hou-09", 2, W_JORDAN2("Jordan would treat broadband as a public utility"), "High-speed internet treated like water and electricity, a basic right"),
     ("ene-01", 1, W_JORDAN2("Jordan would invest in renewable energy production"), "Invest in renewable energy production, sustainable materials, and clean technology"))
ZAMORA = site("Martin Zamora", "https://zamorafornewmexico.com/", READ27)
cand("NM-H-03", "NM-H-03:zamora", "Martin Zamora", "R", "Born on a farm near Clovis, from a long line of eastern New Mexico farmers, ranchers and cattlemen.",
     ("cri-01", 1, ZAMORA("Zamora will stand with law enforcement"), "As your congressman, I will stand with law enforcement and fight to restore law and order."),
     ("imm-01", 1, ZAMORA("Zamora wants the southern border secured"), "A nation without borders is not a nation."))
GIES = site("Aaron Gies", "https://aaronforny23.com/", READ27)
cand("NY-H-23", "NY-H-23:gies", "Aaron Gies", "D", "Teacher, nonprofit leader and person of faith; raised by a small contractor and a school secretary.",
     ("hea-01", 2, GIES("Gies supports universal health care"), "Universal\nHealthcare"),
     ("soc-03", 2, GIES("Gies would codify Roe and vote against a national abortion ban"), "I support a woman’s right to choose."),
     ("soc-04", -2, GIES("Gies would vote no on any national abortion ban"), None),
     ("eco-09", 1, GIES("Gies would raise wages and strengthen workers’ bargaining power"), "Aaron supports raising wages and strengthening workers’ bargaining power."),
     ("edu-01", 1, GIES("Gies opposes cuts to federal education funding"), "there are efforts to cut federal education investments that support rural schools, special education, Head Start, Job Corps, and Pell Grants"),
     ("imm-09", 1, GIES("Gies supports a guest worker program"), "a guest worker program that serves our country’s economic needs"),
     ("eco-12", 2, GIES("Gies would lift the cap on Social Security earnings"), "Aaron would respond by eliminating the cap on Social Security earnings"),
     ("soc-08", 1, GIES("Gies would update privacy laws against AI surveillance"), "I support updating our privacy laws"),
     ("ene-01", 2, GIES("Gies would fight for federal money for renewable energy"), "Renewable energy makes us more resilient and energy independent and I’ll fight for federal dollars for these projects"),
     ("ene-02", -2, GIES("Gies opposes new nuclear projects and fracking"), "I oppose irresponsible data center buildout, fracking and new nuclear projects."),
     ("ene-03", -1, GIES("Gies opposes fracking"), None),
     ("gov-02", 2, GIES("Gies supports strict bans on stock trading by Congress and officials"), None),
     ("gov-11", 2, GIES("Gies would end Citizens United"), "we must end Citizens United and prohibit members of Congress from becoming lobbyists for seven years after they leave office"),
     ("gov-13", -2, GIES("Gies would end Citizens United"), None),
     ("gov-09", 1, GIES("Gies would bar members of Congress from lobbying for seven years"), None),
     ("soc-01", 1, GIES("Gies supports freedom of speech"), "I support the constitutional freedoms guaranteed by our Bill of Rights, including freedom of speech,"))
MCINTYRE = site("Virginia McIntyre", "https://virginiamcintyreforcongress.com/", READ27)
cand("NY-H-25", "NY-H-25:mcintyre", "Virginia McIntyre", "R", "Monroe County legislator, language professor and interpreter; born and raised in Gates.",
     ("gov-01", 2, MCINTYRE("McIntyre supports term limits for Congress"), "Term limits for Congress"),
     ("eco-02", 1, MCINTYRE("McIntyre supports no tax on Social Security, tips or overtime"), "No tax on Social Security, tips, or overtime"),
     ("eco-08", 1, MCINTYRE("McIntyre supports small-business tax relief and enhanced child tax credits"), "Simpler tax filings, small-business relief, and enhanced child tax credits"),
     ("eco-07", 1, MCINTYRE("McIntyre would eliminate fraud and wasteful spending"), "Eliminating fraud and wasteful spending"))
KOLASINSKI = site("Joshua Kolasinski", "https://www.joshuaforohio.com/", READ27)
cand("OH-H-04", "OH-H-04:kolasinski", "Joshua Kolasinski", "D", "Small-business owner who installs, tests and repairs medical equipment; lives in Delaware, Ohio.",
     ("edu-06", -2, KOLASINSKI("Kolasinski opposes vouchers that fund for-profit schools at public schools’ expense"), "School voucher programs are trying to fund for-profit schools at the cost of public education for Ohio’s youth."),
     ("hea-02", 2, KOLASINSKI("Kolasinski would let Medicare negotiate drug prices"), "Allow Medicare to negotiate drug prices"),
     ("hea-06", 1, KOLASINSKI("Kolasinski would prioritize mental health and addiction treatment"), "Prioritize preventive care, mental and emotional health, and addiction treatment"),
     ("hea-09", 1, KOLASINSKI("Kolasinski would prioritize preventive care"), None),
     ("cri-08", 1, KOLASINSKI("Kolasinski would treat addiction as a health issue"), "Treat addiction as health issue instead of moral failure"),
     ("hou-09", 1, KOLASINSKI("Kolasinski would expand rural high-speed internet"), "Streamline the expansion of high-speed internet in rural communities"),
     ("gov-11", 2, KOLASINSKI("Kolasinski would repeal Citizens United"), "Repeal Citizens United and regulate campaign funding through enhanced disclosure; encourage small donor campaigns"),
     ("gov-13", -2, KOLASINSKI("Kolasinski would repeal Citizens United"), None),
     ("gov-03", 1, KOLASINSKI("Kolasinski would require enhanced campaign finance disclosure"), None),
     ("gov-02", 2, KOLASINSKI("Kolasinski would ban members of Congress from trading stocks"), "Ban members of Congress from trading individual stocks"),
     ("gov-01", 1, KOLASINSKI("Kolasinski supports term limits"), "Support term limits"))
JUKIC = site("Maria Jukic", "https://www.mariajukicforcongress.com/healthcare-the-road-to-universal-coverage/", READ27)
JUKIC2 = site("Maria Jukic", "https://www.mariajukicforcongress.com/campaign-finance-reform/", READ27)
cand("OH-H-14", "OH-H-14:jukic", "Maria Jukic", "D", "Attorney with a health care career and former city councilwoman; the child of immigrants, from a union family.",
     ("hea-01", 1, JUKIC("Jukic calls health care a basic human right and wants a road to universal coverage"), "it is a basic human right and a foundation of a strong, productive society"),
     ("hea-03", 2, JUKIC("Jukic would lower the Medicare eligibility age to 62"), "lower the Medicare eligibility age from 65 to 62"),
     ("eco-04", 1, JUKIC("Jukic supports breaking up health care monopolies"), "Maria supports the Break Up Big Medicine Act of 2026"),
     ("hea-02", 2, JUKIC("Jukic would let Medicare negotiate drug prices"), "Maria supports allowing Medicare to negotiate drug prices directly with pharmaceutical companies"),
     ("gov-11", 1, JUKIC2("Jukic says corporations shouldn’t have outsized influence in democracy"), "Maria believes corporations shouldn’t have outsized influence in our democracy."))
CROISANT = site("John Croisant", "https://www.croisantforcongress.com/issues", READ27)
more("OK-H-01", "OK-H-01:croisant",
     ("edu-06", -1, CROISANT("Croisant would stop public money flowing to private schools with no strings attached"), "stopping the flow of public money to private schools with no strings attached"),
     ("hea-03", 2, CROISANT("Croisant supports Medicaid expansion, ACA subsidies or broader universal coverage"), "I support expanding access through Medicaid expansion, ACA subsidies, or a broader universal coverage model."),
     ("hea-07", 1, CROISANT("Croisant supports ACA subsidies"), None),
     ("hou-01", 1, CROISANT("Croisant wants HUD focused on building affordable housing"), "HUD should be focused on supporting local communities and building affordable housing."),
     ("soc-07", 1, CROISANT("Croisant would invest in affordable child care"), "Investing in childcare is investing in Oklahoma's workforce and economy."),
     ("gov-01", 1, CROISANT("Croisant supports term limits"), None),
     ("gov-11", 2, CROISANT("Croisant would overturn Citizens United"), "Overturn Citizens United and get money out of elections"),
     ("gov-13", -2, CROISANT("Croisant would overturn Citizens United"), None),
     ("gov-02", 2, CROISANT("Croisant would end stock trading for all branches of government"), "End stock trading for all branches of government, no profiting off insider knowledge"),
     ("gov-09", 1, CROISANT("Croisant would bar lobbying for five years after leaving office"), "Lobbying restrictions: no revolving door for five years after leaving office"),
     ("def-08", -1, CROISANT("Croisant opposes starting or continuing forever wars"), "not starting nor continuing forever wars around the world"),
     ("imm-02", 2, CROISANT("Croisant supports a real path to citizenship for long-term residents"), "Long-term residents who pay taxes, contribute to their communities, and have built their lives here should have a real, accessible path to citizenship"),
     ("imm-04", 2, CROISANT("Croisant would redirect ICE resources to immigration courts"), "We should redirect ICE resources toward immigration courts to clear the backlog and make the system more efficient."),
     ("imm-08", -1, CROISANT("Croisant would redirect ICE resources to the courts"), None),
     ("imm-01", 1, CROISANT("Croisant believes in a secure border"), "I believe in a secure border"),
     ("def-09", 1, CROISANT("Croisant would invest in cybersecurity"), "investing in cybersecurity"))
GUY = site("Tony Guy", "https://tonyguyforcongress.com/", READ27)
more("PA-H-17", "PA-H-17:guy",
     ("cri-01", 1, GUY("Guy will always back the police and first responders"), "A career law enforcement officer who will always Back the Blue and stand with our first responders."),
     ("imm-01", 2, GUY("Guy would fund the wall"), "No more open borders. Fund the wall, deport criminal illegals, and stop the flow of deadly fentanyl."),
     ("imm-07", 2, GUY("Guy would deport criminals in the country illegally"), None),
     ("ene-03", 1, GUY("Guy would unleash energy dominance"), "Pro-growth policies that empower small businesses, unleash energy dominance, and create good-paying jobs."))
DESOUZA = site("Pedro DeSouza", "https://pedroforri.com/", READ27)
cand("RI-H-01", "RI-H-01:desouza", "Pedro DeSouza", "I", "Small-business owner and data professional.",
     ("hou-02", 2, DESOUZA("DeSouza would bar Wall Street from buying up single-family homes"), "Wall Street should not be allowed to buy up single-family homes and turn neighborhoods into investment portfolios while working families are priced out."),
     ("hou-04", 1, DESOUZA("DeSouza would cut regulations to make homes easier to build"), "we need to make it easier and more affordable to build homes by cutting unnecessary regulations"),
     ("hea-01", 2, DESOUZA("DeSouza supports single-payer health care"), "Single-payer healthcare would cut out that waste, cover every American, and put patients before profits."),
     ("hea-04", -2, DESOUZA("DeSouza supports single-payer health care"), None),
     ("def-08", -1, DESOUZA("DeSouza would end forever wars"), "No more forever wars. No more blank checks."),
     ("eco-07", 1, DESOUZA("DeSouza wants Congress to take the national debt seriously"), "Congress must stop bankrupting America and start answering to the taxpayers who fund it."))
ETHRIDGE = site("Jessica Ethridge", "https://www.jessica4sc.com/", READ27)
cand("SC-H-04", "SC-H-04:ethridge", "Jessica Ethridge", "L", "Paralegal and compliance professional from Greer; the Libertarian nominee for lieutenant governor in 2022.",
     ("eco-07", 2, ETHRIDGE("Ethridge would eliminate wasteful spending and reduce the national debt"), "I will work to identify and eliminate wasteful federal spending and support policies that reduce our national debt"),
     ("def-08", -1, ETHRIDGE("Ethridge says Washington acts like the world’s police force"), "For too long, Washington has acted like America is the world’s police force while hardworking families here at home pay the price."),
     ("def-07", 1, ETHRIDGE("Ethridge wants a foreign policy focused on peace"), "I will fight for a foreign policy focused on peace, accountability, and putting Americans first."))
MONDAY = site("Christopher Monday", "https://cmondayforliberty.com/", READ27)
cand("TN-H-06", "TN-H-06:monday", "Christopher Monday", "I", "Born in South Carolina and diagnosed with cerebral palsy as a child; an honors graduate of Cookeville High School.",
     ("eco-07", 2, MONDAY("Monday supports balanced budget reforms and opposes omnibus bills"), "Support balanced budget reforms"),
     ("hou-09", 1, MONDAY("Monday would strengthen rural broadband responsibly"), "Strengthen rural broadband responsibly"),
     ("soc-04", 2, MONDAY("Monday supports pro-life legislation"), "Support pro-life legislation consistent with constitutional authority"),
     ("soc-03", -2, MONDAY("Monday supports pro-life legislation"), None),
     ("def-04", 1, MONDAY("Monday would reevaluate foreign conflicts fought without congressional authorization"), "Reevaluate perpetual foreign conflicts that cost innocent lives without proper congressional authorization"),
     ("soc-01", 1, MONDAY("Monday would protect First Amendment freedoms"), "Protect First Amendment freedoms"))
PEARCE = site("Jason Pearce", "https://pearcefortexas.com/", READ27)
cand("TX-H-04", "TX-H-04:pearce", "Jason Pearce", "D", "Former mortgage and finance professional from Plano.",
     ("hea-01", 2, PEARCE("Pearce supports Medicare for All"), "Medicare for All."),
     ("hou-01", 1, PEARCE("Pearce calls housing a human right"), "Housing is a human right."),
     ("ene-04", 1, PEARCE("Pearce wants clean water, clean air and accountable corporations"), "Clean water. Clean air. Accountable corporations."),
     ("def-07", 1, PEARCE("Pearce says endless war is a policy choice that can be changed"), "Endless war is a policy choice — and we can choose differently."))
BAUMAN = site("Adam Bauman", "https://www.adambaumanforcongress.com/", READ27)
cand("TX-H-16", "TX-H-16:bauman", "Adam Bauman", "R", "Retired Border Patrol agent who served on its tactical unit (BORTAC); a Navy special warfare combatant-craft crewman veteran.",
     ("imm-01", 1, BAUMAN("Bauman supports Customs and Border Protection’s mission to secure the border"), "I am committed to supporting the Custom's and Border Protection mission to protect our border and keep El Paso safe."),
     ("def-03", 1, BAUMAN("Bauman would cut the red tape that delays veterans’ benefits"), "I am dedicated to ensure our Veterans receive the care they deserve, cutting the red tape that delays benefits"),
     ("hea-07", -1, BAUMAN("Bauman would make insurance more affordable without federal subsidies"), "make insurance more affordable without the federal government subsidizing these costs"),
     ("soc-12", -1, BAUMAN("Bauman objects to what he calls attacks on women’s sports and women-only restrooms"), "The attack on women's sports and women only restrooms continues."))
SIMS = site("Dione Sims", "https://dionesimsforcongress.com/platform/healthcare", READ27)
SIMS2 = site("Dione Sims", "https://dionesimsforcongress.com/", READ27)
cand("TX-H-25", "TX-H-25:sims", "Dione Sims", "D", None,
     ("hea-03", 2, SIMS("Sims would push Texas to expand Medicaid"), "Dione will advocate for Texas to capture available federal healthcare resources"),
     ("hea-07", 1, SIMS("Sims supports targeted help making Marketplace coverage affordable"), "Dione will support targeted federal assistance that makes Marketplace coverage more affordable for working families"),
     ("hea-02", 2, SIMS("Sims would strengthen Medicare drug price negotiation"), "Dione will support strengthening Medicare's ability to negotiate the prices of high-cost prescription drugs"),
     ("hea-01", 1, SIMS("Sims calls affordable health care fundamental"), "Dione Sims believes access to affordable healthcare is fundamental to the freedom to pursue the American Dream."),
     ("soc-07", 1, SIMS2("Sims has a plan for affordable, accessible child care"), "Dione Sims’ Plan for Affordable, Accessible Childcare for Texas Families"))
LLOYD = site("Tanya Lloyd", "https://www.tanyafortx27.com/", READ27)
cand("TX-H-27", "TX-H-27:lloyd", "Tanya Lloyd", "D", "Fifth-generation Texan and public school teacher in the Lockhart Independent School District; earlier worked in car dealerships and real estate.",
     ("hea-01", 2, LLOYD("Lloyd calls health care a universal right"), "Healthcare is a universal right, not a privilege; and people have guaranteed access to abortion and full reproductive rights."),
     ("soc-03", 2, LLOYD("Lloyd supports guaranteed access to abortion"), None),
     ("eco-03", 1, LLOYD("Lloyd wants every job to pay a living wage"), "Every job pays a living wage, and families benefit from universal daycare."),
     ("soc-07", 2, LLOYD("Lloyd supports universal day care"), None),
     ("edu-01", 2, LLOYD("Lloyd wants public education fully funded"), "Public education is fully funded, and all children have access to early education."))
FIERRO = site("Martha Fierro", "https://www.fierrofortexas.com/", READ27)
cand("TX-H-29", "TX-H-29:fierro", "Martha Fierro", "R", None,
     ("hea-04", 1, FIERRO("Fierro would make health care affordable through competition, not mandates"), "By raising competition, expanding access, and protecting patient choice"),
     ("edu-06", 1, FIERRO("Fierro would empower parents with school choice"), "Empower parents with school choice, defend parental rights, and protect the values that make Texas strong."),
     ("eco-07", 1, FIERRO("Fierro would cut reckless federal spending"), "Make Houston Affordable Again by cutting reckless federal spending and fighting inflation to lower costs for gas, groceries, and housing."),
     ("ene-03", 1, FIERRO("Fierro supports oil and natural gas"), "Protect Texas energy independence — keep energy decisions in Texas, support oil and natural gas, and strengthen grid reliability to lower bills."),
     ("imm-01", 1, FIERRO("Fierro supports the Border Patrol"), "Support Border Patrol and stop policies that encourage illegal crossings and human trafficking."))
E_JACKSON = site("Everett Jackson", "https://jacksonfortexas.com/", READ27)
cand("TX-H-30", "TX-H-30:jackson", "Everett Jackson", "R", None,
     ("imm-01", 1, E_JACKSON("Jackson would secure the borders"), None),
     ("def-16", 1, E_JACKSON("Jackson would confront China’s aggression"), None),
     ("edu-01", 1, E_JACKSON("Jackson would invest in schools"), None))
HART = site("Rhonda Hart", "https://hart4congress.com/", READ27)
cand("TX-H-36", "TX-H-36:hart", "Rhonda Hart", "D", "Disabled military veteran whose 14-year-old daughter was killed in the 2018 Santa Fe High School shooting; she worked to pass the Kimberly Vaughan Safe Storage of Firearms Act.",
     ("edu-06", -2, HART("Hart opposes school vouchers completely"), "The voucher scheme being pushed in Texas is a direct attack on public education"),
     ("edu-01", 2, HART("Hart would invest more in public education"), "We should be investing more in public education, not less"),
     ("edu-04", 1, HART("Hart would pay teachers what they deserve"), None),
     ("ene-01", 2, HART("Hart would invest seriously in solar and wind"), "We need to protect our natural resources and invest seriously in renewable energy — solar and wind in particular."),
     ("imm-08", -1, HART("Hart says ICE operates with virtually no accountability"), "operating with masks on, no body cameras, and virtually no accountability"),
     ("def-08", -1, HART("Hart would stop sending troops into unnecessary Middle East wars"), "We need to stop sending our troops into random, unnecessary wars in the Middle East."),
     ("soc-12", 1, HART("Hart would reverse the ban on transgender troops"), "The ban on transgender troops must be reversed."),
     ("eco-03", 1, HART("Hart would raise the minimum wage"), "Raise the minimum wage."),
     ("eco-01", 1, HART("Hart would tax billionaires"), "Tax billionaires."),
     ("eco-10", -1, HART("Hart would end the chaotic tariffs"), "End the chaotic, reckless tariffs."),
     ("hea-01", 2, HART("Hart wants health care not tied to a paycheck"), "Every American deserves healthcare that isn't tied to a paycheck or a premium."),
     ("def-03", 2, HART("Hart would spend what it takes to care for veterans"), "If we can spend billions sending people to war, we can spend what it takes to take care of them when they come home."))
PENA = site("Lauren Peña", "https://www.lauren4congress.com/", READ27)
cand("TX-H-37", "TX-H-37:pena", "Lauren Peña", "R", "Human trafficking survivor and mother of six.",
     ("gov-12", 1, PENA("Peña would audit every agency and expose fraud"), "Lauren will audit every agency, expose the fraud, and prosecute the corrupt."),
     ("edu-06", 1, PENA("Peña would defend school choice"), "Lauren will defend parental rights, school choice, and the values that built Texas."),
     ("cri-01", 2, PENA("Peña would restore full police funding"), "Lauren will restore full law enforcement funding and make Austin safe again."),
     ("def-03", 1, PENA("Peña wants world-class care for veterans"), "The men and women who served this country deserve world-class care, not bureaucratic neglect."),
     ("eco-07", 1, PENA("Peña would cut federal spending that drives inflation"), "Lauren will cut federal spending driving inflation"))
WEST = site("Jesse West", "https://www.jessewest2026.com/", READ27)
more("UT-H-01", "UT-H-01:west",
     ("def-08", -2, WEST("West would bring the troops home"), "The best way to support the troops is to bring them home."),
     ("def-03", 1, WEST("West would take care of veterans when they come home"), "Take care of veterans when they come home — for real"),
     ("cri-09", -2, WEST("West would end the federal death penalty"), "The state shouldn't have irreversible power over human life"),
     ("imm-02", 2, WEST("West would create clear legal pathways to citizenship"), "Create clear, accessible legal pathways to citizenship"),
     ("imm-08", -1, WEST("West opposes oppressive immigration enforcement"), "opposing oppressive immigration enforcement"),
     ("soc-05", 2, WEST("West supports cannabis legalization"), "Cannabis legalization — what you do with your body is your business"))
UDELL = site("Kent Udell", "https://www.kentudellforcongress.com/", READ27)
more("UT-H-03", "UT-H-03:udell",
     ("hea-03", 2, UDELL("Udell would expand programs like Medicare to be accessible to all"), "expand programs, such as Medicare, to be accessible to all"),
     ("hea-04", -1, UDELL("Udell would diminish insurance companies’ influence"), None),
     ("ene-01", 1, UDELL("Udell supports all-of-the-above energy and leadership in clean-energy technology"), "We can strengthen energy security, protect water and land, and lead in clean-energy technologies"),
     ("gov-09", 1, UDELL("Udell would fight for ethics reforms"), "I will fight for transparency, accountability, and ethics reforms that put American interests, not special interests, first."))
WOLL = site("Stephen Woll", "https://www.stevewoll.com/issues", READ27)
cand("VA-H-03", "VA-H-03:woll", "Stephen Woll", "I", "Navy veteran, scientist and businessman who came to Hampton Roads with the Navy more than 25 years ago.",
     ("gov-04", 2, WOLL("Woll would end gerrymandering with independent citizen commissions"), "End partisan gerrymandering - independent citizen commissions only"),
     ("gov-11", 2, WOLL("Woll would reverse Citizens United"), "Reverse Citizens United - elections should not be an auction"),
     ("gov-13", -2, WOLL("Woll would reverse Citizens United"), None),
     ("gov-02", 2, WOLL("Woll would ban congressional and executive branch stock trading"), "Ban congressional and executive branch stock trading and political betting markets"),
     ("gov-09", 2, WOLL("Woll would bar lobbying for 10 years after leaving Congress"), "No lobbying for 10 years after leaving Congress"),
     ("eco-07", 2, WOLL("Woll would balance the budget"), "Balance the budget."),
     ("def-02", 2, WOLL("Woll would re-embrace NATO"), "Re-embrace NATO - 80 years of the most effective peacekeeping force in history"),
     ("def-10", -2, WOLL("Woll would restore international aid programs"), "Restore our international aid programs - the most potent instrument of soft power available"),
     ("def-13", 2, WOLL("Woll would support Ukraine fully"), "Support Ukraine fully - a democracy brutally attacked by a dictator deserves our backing"),
     ("def-05", 2, WOLL("Woll would back democracies facing invasion, Ukraine first"), None),
     ("def-16", 1, WOLL("Woll would build a Pacific alliance to balance China and back Taiwan’s independence"), "Assemble a Pacific alliance among democratic nations in the region as a balance to China"),
     ("def-15", -1, WOLL("Woll would wind down the Iran war"), "Control and wind down the Iran war"),
     ("def-11", -1, WOLL("Woll calls the Netanyahu government’s actions against Palestinians reprehensible"), "The Netanyahu government's actions against the general Palestinian population in Gaza and the West Bank have been equally reprehensible"),
     ("eco-10", -1, WOLL("Woll blames across-the-board tariffs for reigniting inflation"), "The inflation has been reignited by across-the-board tariffs"),
     ("eco-12", 1, WOLL("Woll objects to billionaires paying lower tax rates than workers"), "while paying a lower tax rate than a welder or a nurse"))
E_RIVERA = site("Edwin Rivera", "https://edwinriveraforcongress.com/", READ27)
more("VA-H-03", "VA-H-03:rivera",
     ("cri-01", 1, E_RIVERA("Rivera supports law enforcement"), "Supporting law enforcement, preventing crime, and building safer neighborhoods."),
     ("edu-01", 1, E_RIVERA("Rivera would invest in schools and support teachers"), "Investing in schools, supporting teachers, and preparing students for a brighter future."))
GAINES = site("Makiba Gaines", "https://www.makibagaines4congress.com/blank-1", READ27)
more("VA-H-03", "VA-H-03:gaines",
     ("eco-07", 1, GAINES("Gaines would eliminate government fraud and waste"), "Congress must stand up for the American public and eliminate or reduce government corruption, fraud, and other wasteful spending."),
     ("cri-07", 1, GAINES("Gaines would increase funding for community crime-prevention programs"), "I intend to increase funding to community programs to establish strong partnerships with Americans who want to create change"),
     ("hou-05", 1, GAINES("Gaines would fund home-ownership programs"), "We can reduce poverty and crime by increasing funding to home-ownership- and entrepreneurship programs and incentives."),
     ("hea-03", 1, GAINES("Gaines demands proper funding of Medicare and Medicaid"), "As Americans, we must demand proper funding of Medicare, Medicaid, and Social Security programs."),
     ("eco-04", 1, GAINES("Gaines says Congress should limit media monopolies"), "The Congress has the power to limit media monopolies"))
FELLER = site("Edwin Feller", "https://fellerforcongress.com/", READ27)
cand("WA-H-02", "WA-H-02:feller", "Edwin Feller", "R", "Grew up on a Whatcom County dairy farm.",
     ("cri-01", 1, FELLER("Feller supports robust law enforcement"), "He supports robust law enforcement, secure borders, fair elections, and balanced budgets."),
     ("imm-01", 1, FELLER("Feller supports secure borders"), None),
     ("eco-07", 1, FELLER("Feller supports balanced budgets"), None),
     ("soc-12", -2, FELLER("Feller would define sex in Title IX as biological sex"), "Codifying that \"sex\" in Title IX refers exclusively to biological sex"),
     ("soc-11", -2, FELLER("Feller would ban irreversible medical procedures for minors"), "Implementing a federal ban on irreversible medical procedures for minors"),
     ("ene-02", 2, FELLER("Feller would expand nuclear and hydroelectric power"), "Dismantling radical environmental mandates, streamlining energy permits, expanding nuclear and hydroelectric capacity, and repealing federal carbon taxes"),
     ("ene-06", -1, FELLER("Feller would dismantle environmental mandates and repeal carbon taxes"), None),
     ("imm-03", 1, FELLER("Feller would move to a merit-based points system"), "Overhauling immigration to prioritize nuclear families and a merit-based points system"))
T_FOX = site("Teresa Fox", "https://foxforwa.com/", READ27)
cand("WA-H-06", "WA-H-06:fox", "Teresa Fox", "R", "Safety professional and emergency manager who has worked in shipyards, on naval bases and on Bering Sea fish processing vessels.",
     ("eco-07", 1, T_FOX("Fox would stop runaway government spending"), "Stop runaway government spending"),
     ("cri-01", 1, T_FOX("Fox wants proper police staffing for rural communities"), "Proper police staffing for rural communities"),
     ("gov-01", 1, T_FOX("Fox supports term limits"), "End career politics and restore citizen service"))
ARNDT = site("Matthew Arndt", "https://endthecartel.com/", READ27)
more("WI-H-06", "WI-H-06:arndt",
     ("eco-04", 2, ARNDT("Arndt would bust up monopolies"), "I’m here to bust up monopolies."),
     ("hea-01", 2, ARNDT("Arndt supports Medicare for All"), "Get us Medicare for All."),
     ("def-08", -1, ARNDT("Arndt would stop the endless wars"), "Stop the endless wars."),
     ("def-12", -2, ARNDT("Arndt would cut ties with Israel"), "Cut ties with Israel."),
     ("def-11", -2, ARNDT("Arndt would cut ties with Israel"), None),
     ("eco-05", -1, ARNDT("Arndt would end corporate welfare"), "End corporate welfare."),
     ("def-10", 2, ARNDT("Arndt would take care of Americans before another dime leaves the country"), "That means taking care of our own people before another dime leaves this country."))
CROSSON = site("Rick Crosson", "https://rickcrosson.com/priorities/", READ27)
more("WI-H-08", "WI-H-08:crosson",
     ("eco-03", 1, CROSSON("Crosson wants a fair, living wage as a floor"), "A fair and living wage no one should fall below."),
     ("hea-01", 2, CROSSON("Crosson wants guaranteed health care for everyone"), "Affordable, Accessible, Guaranteed Healthcare for Everyone."),
     ("eco-10", -1, CROSSON("Crosson would stand up for family farms against tariffs"), "Keeping our farms profitable and in the family, and standing up for them against tariffs, and corporate squeezing."),
     ("edu-02", 2, CROSSON("Crosson would make public education free from pre-K through trade school or college"), "From Pre-K through trade school or a degree, public education should be free."),
     ("soc-03", 2, CROSSON("Crosson says reproductive decisions belong to a woman and her doctors"), "A woman’s right to choose her reproductive healthcare, and to access it, belongs with her and her doctors, not the government."),
     ("soc-04", -2, CROSSON("Crosson says reproductive decisions belong to a woman and her doctors"), None),
     ("def-03", 1, CROSSON("Crosson would fix VA wait times and support veterans’ mental health"), "fixing VA wait times and standing up for veterans’ mental health"))
C_GRAY = site("Chuck Gray", "https://chuckforwyoming.com/", READ27)
cand("WY-H-00", "WY-H-00:gray", "Chuck Gray", "R", "Wyoming’s secretary of state, elected in 2022; earlier served six years in the Wyoming House.",
     ("gov-05", 2, C_GRAY("Gray was the lead sponsor of Wyoming’s 2021 voter ID law"), "Chuck was the lead sponsor of Wyoming's landmark voter ID law passed in 2021"),
     ("soc-04", 2, C_GRAY("Gray wrote Wyoming’s 2017 ultrasound law"), "the first pro-life legislation to pass the Wyoming Legislature in 30 years"),
     ("soc-03", -2, C_GRAY("Gray wrote Wyoming’s 2017 ultrasound law"), None),
     ("ene-03", 1, C_GRAY("Gray has fought to protect coal, oil and gas jobs"), "Chuck has consistently fought to protect coal, oil, and gas jobs from coastal elites and radical environmental activists."),
     ("gov-07", -2, C_GRAY("Gray led efforts to ban ranked-choice voting"), "He also led efforts to ban ranked-choice voting"))
HAGGIT = site("Jeffrey Haggit", "https://haggitforhouse.com/", READ27)
cand("WY-H-00", "WY-H-00:haggit", "Jeffrey Haggit", "Constitution", None,
     ("def-09", 1, HAGGIT("Haggit would protect and upgrade the electrical grid against foreign compromise"), "The protection of our national electrical grid from foreign compromise must be a priority, as well as upgrading it."))
KIRRANE = site("Sean Kirrane", "https://www.seankirrane.com/homepage", READ27)
cand("NJ-H-05", "NJ-H-05:kirrane", "Sean Kirrane", "R", "Health care, finance and technology executive who has turned around failing hospitals; calls himself a socially moderate, fiscally disciplined Republican.",
     ("eco-02", 1, KIRRANE("Kirrane would reduce and streamline taxes for families"), "Reduce and streamline taxes for hardworking American families."),
     ("imm-01", 1, KIRRANE("Kirrane would secure the borders"), "Secure our borders and enforce immigration laws."),
     ("ene-03", 1, KIRRANE("Kirrane would establish American energy dominance"), "Establish American energy dominance and independence."))

# Campaign links that no longer reach a campaign site (checked Oct. 27): Michael Gist's
# deployment is gone (404), Victor Arias's old host suspended the account (his new
# site, from VOTE411, is set below), Renada Collins's
# domain answers 404, Paul Berry's and Matthew Althaus's Wix domains aren't connected to
# any site, Eric Hafner's domain only frames google.com, Alaha Ahrar's doesn't resolve
# and Tim Sharman's fails its TLS handshake. Phil Ehr's site answers only over http.
# Mike Croley's old domain (mikefortn6.com, still on Wikipedia) fails too; the site he
# gives VOTE411, croleyforcongress.com, works and is used below.
for _race, _cid, _name, _party in (
        ("FL-H-06", "FL-H-06:gist", "Michael Gist", "I"),
        ("FL-H-19", "FL-H-19:arias", "Victor Arias", "D"),
        ("LA-H-02", "LA-H-02:collins", "Renada “Honey” Collins", "D"),
        ("MO-H-01", "MO-H-01:berry", "Paul Berry", "R"),
        ("OH-H-09", "OH-H-09:althaus", "Matthew Althaus", "L"),
        ("AK-H-00", "AK-H-00:hafner", "Eric Hafner", "D"),
        ("VA-H-07", "VA-H-07:ahrar", "Alaha Ahrar", "I"),
        ("VA-H-08", "VA-H-08:sharman", "Tim Sharman", "I"),
):
    cand(_race, _cid, _name, _party, None, officialSite=None)
cand("FL-H-28", "FL-H-28:ehr", "Phil Ehr", "D", None, officialSite="http://ehrforcongress.us/")


# Campaign sites whose fetched text states positions that were not mapped the first
# time through (re-read Oct. 27).
SWANSON2 = site("Trina Swanson", "https://trinaforcongress.com/priorities/", READ27)
cand("MN-H-08", "MN-H-08:swanson", "Trina Swanson", "D", "Worked at the Department of Homeland Security, including on efforts to stop human trafficking; the DFL-endorsed candidate.",
     ("hea-01", 2, SWANSON2("Swanson will fight for universal health care"), "I will fight for universal healthcare."),
     ("hea-07", 2, SWANSON2("Swanson would protect ACA premium tax credits"), "I will protect health insurance tax credits so 90,000 Minnesotans don’t see costs jump $177 a month, on average."),
     ("eco-04", 1, SWANSON2("Swanson wants antitrust laws enforced on food and fuel costs"), "We need antitrust laws enforced so a handful of companies can’t drive up the cost of food, fuel, and everyday essentials."),
     ("ene-01", 1, SWANSON2("Swanson wants investment in clean energy, steel and batteries"), "We need investment in new industries like clean energy, steel, and batteries to store renewable energy"),
     ("eco-09", 1, SWANSON2("Swanson wants jobs with livable wages and strong union protections"), "Minnesotans deserve jobs close to home with livable wages, strong union protections, and stability."),
     ("ene-04", 1, SWANSON2("Swanson says mining must protect the environment and would protect the Boundary Waters"), "Mining must benefit our communities, prioritize our workforce, and protect our environment."),
     ("agr-05", 1, SWANSON2("Swanson supports domestic mining of critical minerals"), "We need to reduce reliance on other nations, but not by letting foreign corporations take these minerals and ship them overseas."),
     ("imm-02", 2, SWANSON2("Swanson supports permanent legal status for Dreamers"), "I support permanent legal status for Dreamers who grew up here and contribute to our communities."),
     ("imm-07", 2, SWANSON2("Swanson would focus enforcement on violent criminals"), "Our priority should be violent criminals and those who pose a genuine risk to public safety"),
     ("imm-03", 1, SWANSON2("Swanson supports visas for foreign students at U.S. universities"), "We need visas for the students studying at our great universities that may come up with the next cure."),
     ("imm-09", 2, SWANSON2("Swanson supports seasonal visas for farmworkers"), "We must have seasonal visas for the critical workforce our farmers rely upon."))
JOYCE = site("Jamie Joyce", "https://www.jamiejoyce.com/", READ27)
JOYCE2 = site("Jamie Joyce", "https://www.jamiejoyce.com/jamies-background", READ27)
more("CA-H-12", "CA-H-12:joyce",
     ("def-12", -2, JOYCE("Joyce would block the bombs to Israel"), "Block the bombs, bring in the humanitarian aide, and end the famine."),
     ("def-11", -1, JOYCE("Joyce supports Israel’s right to exist but opposes its campaign in Gaza"), "Jamie supports Israel’s right to exist, but not its interest in colonizing Gaza"),
     ("imm-08", -1, JOYCE("Joyce would rein in ICE"), "Get ICE off our streets"),
     ("gov-03", 1, JOYCE("Joyce would shine a light on dark money"), "shining a light on dark money"),
     ("hea-03", 1, JOYCE2("Joyce says the nation should provide health care and at-home support to those in need"), "For Jamie, having quality healthcare and at-home support should be something that our nation collectively provides to those in need."))
S_LEWIS2 = site("Shane Lewis", "https://www.shanelewisforcongress.com/issues", READ27)
more("CA-H-18", "CA-H-18:lewis",
     ("edu-10", 2, S_LEWIS2("Lewis would require civics and personal finance for every student"), "every student should graduate with practical knowledge of personal finance, budgeting, saving, investing, and how our economy works."),
     ("edu-07", 1, S_LEWIS2("Lewis proposes a Protect Parental Rights and Local Control Act"), "Protect Parental Rights and Local Control Act"),
     ("ene-03", 1, S_LEWIS2("Lewis would keep using domestic fossil fuels, especially natural gas"), "Maintain and responsibly utilize domestic fossil fuels (especially natural gas) as a reliable bridge and backup source."),
     ("ene-01", 1, S_LEWIS2("Lewis supports battery storage and advanced renewables"), "Support breakthroughs in battery storage, advanced renewables, carbon capture, and next-generation solutions"))
BOYANTON = site("Carl Boyanton", "https://carl4congress.com/", READ27)
BOYANTON2 = site("Carl Boyanton", "https://carl4congress.com/position-on-federal-budget/", READ27)
BOYANTON3 = site("Carl Boyanton", "https://carl4congress.com/just-5-to-stand-up-for-mississippi-small-businesses/", READ27)
BOYANTON4 = site("Carl Boyanton", "https://carl4congress.com/position-on-immigration/", READ27)
more("MS-H-04", "MS-H-04:boyanton",
     ("eco-07", 2, BOYANTON2("Boyanton would end deficit spending and pass a balanced budget amendment"), "an end to deficit spending as usual, and passage of a balanced budget amendment"),
     ("soc-04", 2, BOYANTON2("Boyanton would prohibit abortion in all but exceptional circumstances"), "I proudly stand as a pro-life advocate."),
     ("soc-03", -2, BOYANTON("Boyanton would prohibit abortion in all but exceptional circumstances"), None),
     ("def-10", 2, BOYANTON3("Boyanton’s campaign says he doesn’t believe in giving money to any other country"), "Carl doesn’t believe in giving money to any other country."),
     ("def-12", -1, BOYANTON("Boyanton’s campaign, asked about Israel, says he doesn’t believe in giving money to any other country"), None),
     ("imm-01", 2, BOYANTON4("Boyanton says strong border security, with physical barriers, is non-negotiable"), "Strong border security is non-negotiable."))
K_MARTIN2 = site("Kevin Martin", "https://kevinmartinforcongress.com/issues/budget", READ27)
cand("GA-H-06", "GA-H-06:martin", "Kevin Martin", "R", None,
     ("eco-07", 1, K_MARTIN2("Martin would end earmarks and pork-barrel spending"), "End earmarks and pork-barrel spending."),
     ("gov-12", 1, K_MARTIN2("Martin would make every program justify itself before new appropriations"), "Every program should have to answer one question before it gets another appropriation"))
STEINMANN = site("Jessica Hart Steinmann", "https://www.jessicasteinmann.com/", READ27)
more("TX-H-08", "TX-H-08:steinmann",
     ("imm-01", 1, STEINMANN("Steinmann will fight to keep the border secure"), "I will fight to keep our border secure, support our military, cut reckless spending, protect our religious liberty"),
     ("eco-07", 1, STEINMANN("Steinmann would cut reckless spending"), None),
     ("soc-06", 1, STEINMANN("Steinmann would protect religious liberty"), None),
     ("soc-12", -2, STEINMANN("Steinmann led the legal fight to keep transgender girls out of girls’ sports"), "I led the legal fight to keep boys out of girls’ sports"))
B_FOSTER2 = site("Bennie Foster", "https://www.electbenniefoster.com/policies", READ27)
cand("MS-H-02", "MS-H-02:foster", "Bennie Foster", "I", "Educator who has worked in both public and private schools.",
     ("edu-06", 2, B_FOSTER2("Foster says education tax money should follow the student"), "He believes that tax money paid by parents towards their child’s education should be well accounted for and follow the student."),
     ("edu-03", 1, B_FOSTER2("Foster wants career-path programs starting in middle school"), "We must be intentional about programs that connect students with career paths and workforce opportunities as early as middle school."))
JACOB = site("Mitchell Jacob", "https://www.mitchelljacob.com/", READ27)
more("OK-H-04", "OK-H-04:jacob",
     ("eco-07", 2, JACOB("Jacob would stop raising the debt limit and cut spending"), "We need to stop raising the debt limit, cut spending, and eliminate the federal debt."),
     ("edu-01", 1, JACOB("Jacob says public schools should be funded and serve free meals"), "Our public schools should be funded and provide free meals."),
     ("edu-09", 2, JACOB("Jacob supports free school meals"), None),
     ("imm-03", 1, JACOB("Jacob would process work visas, asylum claims and refugee requests swiftly"), "We should process work visas, asylum claims, and refugee requests fairly and swiftly, allowing people to contribute to our economy."),
     ("hea-01", 1, JACOB("Jacob calls health care a human right"), "Ultimately, healthcare is a human right, and no one, including insurance companies, should take that away."),
     ("cri-05", 2, JACOB("Jacob says rehabilitation is the first pillar of criminal justice"), "I believe the first pillar of criminal justice is rehabilitation, followed by punishment."),
     ("eco-03", 1, JACOB("Jacob supports a living wage"), "I support a living wage, investment in public education, and a criminal justice system that prioritizes rehabilitation."),
     ("soc-03", 1, JACOB("Jacob says a woman’s rights should be the same across state lines"), "A woman's rights should remain consistent regardless of state lines."),
     ("def-12", -2, JACOB("Jacob would cut off support for Israel until it ends its campaign in Gaza"), "I believe the United States must cease all economic, political, and military support for Israel until they cease their campaign of violence and aggression."),
     ("def-11", -2, JACOB("Jacob calls Israel’s bombing of civilians war crimes"), "Israel’s indiscriminate bombing and killing of civilians are clearly war crimes"))
HASKIN2 = site("Seth Haskin", "https://www.sethhaskinforfl.com/policy", READ27)
cand("FL-H-19", "FL-H-19:haskin", "Seth Haskin", "I", None,
     ("eco-12", -2, HASKIN2("Haskin would repeal the 16th Amendment and end the federal income tax"), "I support repealing the 16th Amendment and ending the federal income tax."),
     ("eco-07", 1, HASKIN2("Haskin would restrain federal spending and borrowing"), "Congress must restrain spending, borrowing, and monetary expansion that diminish purchasing power"))
BULLER = site("Kailee Buller", "https://kaileebuller.com/", READ27)
more("NY-H-22", "NY-H-22:buller",
     ("soc-07", 1, BULLER("Buller would expand access to affordable child care"), "Kailee believes we need practical solutions that expand access to affordable, high-quality childcare and give parents the flexibility they need."),
     ("eco-02", 1, BULLER("Buller would expand the Child and Dependent Care Tax Credit"), "Expanding the Child and Dependent Care Tax Credit which will put more money directly back in parents’ pockets"),
     ("ene-10", 1, BULLER("Buller would repeal costly climate mandates for all-of-the-above energy"), "she supports repealing those costly climate mandates and advancing an all-of-the-above energy policy"),
     ("ene-06", -1, BULLER("Buller would repeal costly climate mandates"), None),
     ("hou-04", 1, BULLER("Buller would cut regulations to increase housing supply"), "She supports policies that encourage responsible development, cut unnecessary regulations, and make it easier for first-time buyers to enter the market."),
     ("hou-05", 1, BULLER("Buller would make it easier for first-time buyers to enter the market"), None))
LEBRUN = site("Tia LeBrun", "https://lebrun4la.com/", READ27)
LEBRUN2 = site("Tia LeBrun", "https://lebrun4la.com/keyissues", READ27)
LEBRUN3 = site("Tia LeBrun", "https://lebrun4la.com/policy-plans", READ27)
cand("LA-H-03", "LA-H-03:lebrun", "Tia LeBrun", "D", None,
     ("edu-06", -2, LEBRUN2("LeBrun says public money should not go to private schools"), "Public money should not go to private schools."),
     ("imm-01", 1, LEBRUN3("LeBrun would secure the border with technology and targeted enforcement"), "Secure the border with modern technology and targeted enforcement."),
     ("imm-02", 1, LEBRUN3("LeBrun would protect Dreamers"), "Protect Dreamers brought here as children."),
     ("imm-03", 1, LEBRUN3("LeBrun would expand legal immigration for industries short of workers"), "Expand legal immigration pathways for industries facing labor shortages."),
     ("soc-07", 1, LEBRUN3("LeBrun would expand child care assistance"), "Expand childcare assistance for working families."),
     ("edu-03", 2, LEBRUN3("LeBrun would expand career and technical education"), "Expand and modernize career and technical education."),
     ("eco-02", 2, LEBRUN3("LeBrun would increase middle-class tax relief and expand the Child Tax Credit"), "Increase tax relief for middle-class households."),
     ("eco-01", 1, LEBRUN3("LeBrun would close loopholes for billionaires and large corporations"), "Close loopholes that allow billionaires and large corporations to pay"),
     ("ene-08", 1, LEBRUN("LeBrun would invest in coastal restoration and hurricane protection"), None))
TACKETT2 = site("Tracey Tackett", "https://www.traceytackett.org/issues", READ27)
cand("OH-H-04", "OH-H-04:tackett", "Tracey Tackett", "I", None,
     ("imm-01", 2, TACKETT2("Tackett would end all illegal immigration"), "We must end all illegal immigration."),
     ("gov-04", 2, TACKETT2("Tackett would require independent, nonpartisan redistricting"), "We must require independent, non-partisan redistricting"),
     ("cri-01", 1, TACKETT2("Tackett would fund police and frontline workers in every community"), "Every community will have the needed funding for frontline workers, police, and firemen."))
KIRKLAND = site("Kyle Kirkland", "https://kirkland2026.com/", READ27)
more("CA-H-21", "CA-H-21:kirkland",
     ("cri-01", 1, KIRKLAND("Kirkland would back the police and end soft-on-crime policies"), "Back the blue, support first responders, and end soft-on-crime policies that put families at risk."),
     ("gov-12", 1, KIRKLAND("Kirkland would demand audits so every tax dollar delivers results"), "Stop waste and fraud, demand audits, and require government to serve families"),
     ("imm-01", 1, KIRKLAND("Kirkland makes strong border security a top priority"), "Top priorities: affordable abundance, government accountability, and strong border security to protect working families."),
     ("edu-03", 1, KIRKLAND("Kirkland would expand career pathways"), "Return to high standards, empower parents, and expand career pathways for the next generation."))
LOCKLIN2 = site("Nicole Locklin", "https://locklinforcongress.com/issues-affordability", READ27)
cand("FL-H-26", "FL-H-26:locklin", "Nicole Locklin", "D", None,
     ("ene-01", 1, LOCKLIN2("Locklin would invest in sustainable energy"), "Invest in sustainable energy."),
     ("def-15", -1, LOCKLIN2("Locklin would end wars, like the Iran war, that disrupt energy markets"), "End wars that disrupt energy markets."),
     ("imm-03", 1, LOCKLIN2("Locklin calls legal immigration an economic strength"), "We should also recognize that legal immigration as an economic strength."))
OAKLEY2 = site("Angel Oakley", "https://www.libertyangel.us/policy", READ27)
more("IL-H-03", "IL-H-03:oakley",
     ("gov-03", 1, OAKLEY2("Oakley would ban dark money in elections"), "Ban on foreign influence and dark money in elections"),
     ("agr-03", 1, OAKLEY2("Oakley supports American manufacturing and supply chain independence"), "Support American manufacturing and supply chain independence"),
     ("edu-03", 1, OAKLEY2("Oakley would expand workforce training and apprenticeships"), "Expand workforce training and apprenticeship pathways"),
     ("imm-01", 1, OAKLEY2("Oakley would strengthen border security"), "Strengthening border security to stop cartels, trafficking, and illegal entry"),
     ("hea-04", 1, OAKLEY2("Oakley would expand competition among doctors, hospitals and insurers"), "Expand choice and competition among doctors, hospitals, insurers, pharmacies, and other providers"),
     ("soc-08", 2, OAKLEY2("Oakley would strengthen safeguards for personal data"), "Protect citizens' privacy by strengthening safeguards for personal data and limiting unnecessary government and corporate surveillance"),
     ("def-07", 1, OAKLEY2("Oakley would protect U.S. interests without endless wars"), "We must deter threats abroad, defend our borders, and protect our interests without endless wars."),
     ("edu-07", 1, OAKLEY2("Oakley would expand parental involvement and curriculum transparency"), "Expand parental involvement and transparency in curriculum"))
BAEZ = site("Edgardo Rafael Baez", "https://www.drbaezforcongress.com/", READ27)
more("TX-H-20", "TX-H-20:baez",
     ("cri-01", 1, BAEZ("Báez strongly supports law enforcement"), "we fiercely support law enforcement and advocate for safer streets"))
PINO = site("Rosie Pino", "https://rosiepinofornj.com/", READ27)
PINO2 = site("Rosie Pino", "https://rosiepinofornj.com/issues/", READ27)
more("NJ-H-09", "NJ-H-09:pino",
     ("eco-07", 1, PINO2("Pino would oppose massive spending packages"), "In Congress, I will oppose massive spending packages and bureaucratic expansions that fuel inflation and drive up the cost of living."),
     ("eco-02", 1, PINO2("Pino supports cutting taxes for working families"), "I support President Trump’s efforts to cut taxes for working families, eliminate burdensome taxes, and unleash American energy"),
     ("ene-03", 1, PINO("Pino would unleash American energy and restore energy independence"), None),
     ("hea-04", 1, PINO2("Pino would lower health costs through competition, transparency and choice"), "I support lowering healthcare costs and expanding access by increasing competition, transparency, and choice."),
     ("hea-08", 2, PINO2("Pino supports protecting people with pre-existing conditions"), "I support protecting people with pre-existing conditions, while fixing what’s broken in our system"),
     ("edu-06", 1, PINO2("Pino’s plan includes school choice"), "Read the plan for energy independence, school choice, and border security."))
TYNDELL = site("Katy Tyndell", "https://katyforkansas.com/", READ27)
TYNDELL2 = site("Katy Tyndell", "https://katyforkansas.com/issues/", READ27)
more("KS-H-04", "KS-H-04:tyndell",
     ("eco-10", -2, TYNDELL2("Tyndell would reverse the tariffs hurting Kansas agriculture"), "Katy will fight to reverse the tariff giveaways that are strangling Kansas agriculture"),
     ("agr-07", -1, TYNDELL("Tyndell says reckless tariffs devalued Kansas farm products"), None),
     ("def-15", -1, TYNDELL2("Tyndell would work to end the war with Iran"), "work across party lines to reopen the Strait of Hormuz and end the War with Iran"),
     ("soc-08", 2, TYNDELL2("Tyndell would protect online privacy against tech companies mining personal data"), "Katy will champion legislation to protect the privacy of people online"),
     ("ene-04", 1, TYNDELL2("Tyndell would fight pesticide deregulation that threatens rural Kansans’ health"), "fight the large-scale industrial encroachment and pesticide deregulation that threaten the health of rural Kansans"))
MCMENEMY = site("Alex McMenemy", "https://alexforthepeople.org/", READ27)
MCMENEMY2 = site("Alex McMenemy", "https://alexforthepeople.org/our-platform/", READ27)
cand("TX-H-38", "TX-H-38:mcmenemy", "Alex McMenemy", "G", None,
     ("edu-02", 2, MCMENEMY("McMenemy fights for free higher education"), "my fight for not just free higher education, but for higher wages and stronger unions, too"),
     ("eco-09", 1, MCMENEMY("McMenemy fights for stronger unions"), None),
     ("eco-03", 1, MCMENEMY("McMenemy fights for higher wages"), None),
     ("hea-01", 2, MCMENEMY("McMenemy wants free universal health care"), "The only way to end this cruelty is for every Texan family to receive free universal healthcare"),
     ("gov-02", 2, MCMENEMY2("McMenemy would ban congressional stock trading"), "Ban Congressional Stock Trading"),
     ("gov-11", 2, MCMENEMY2("McMenemy would end super PACs and political lobbying"), "End SuperPACs and Political Lobbying"),
     ("gov-13", -2, MCMENEMY("McMenemy would end super PACs"), None),
     ("imm-08", -2, MCMENEMY2("McMenemy would abolish ICE"), "Abolish ICE and charge anyone who participated in it’s operations as terrorists"),
     ("def-11", -2, MCMENEMY2("McMenemy supports boycotting, divesting from and sanctioning Israel"), "Boycott, Divest, and Sanction the settler-colonial state of Israel until Palestine is Free"),
     ("def-12", -2, MCMENEMY("McMenemy supports sanctions on Israel"), None),
     ("ene-01", 2, MCMENEMY2("McMenemy wants a quick transition to clean energy"), "Make a Quick Transition to Clean Energy"),
     ("ene-07", 1, MCMENEMY2("McMenemy would expand public transportation"), "Expand Transportation Freedom with Public Transport"))
MCMAHON = site("Patty McMahon", "https://www.mcmahonforcongress.com/", READ27)
MCMAHON2 = site("Patty McMahon", "https://www.mcmahonforcongress.com/on-the-issues", READ27)
more("CO-H-06", "CO-H-06:mcmahon",
     ("def-04", 2, MCMAHON2("McMahon says war must be a last resort and constitutionally authorized"), "Unnecessary military intervention should be opposed because war should only be a last resort, clearly justified, and constitutionally authorized."),
     ("def-07", 1, MCMAHON("McMahon opposes unnecessary military intervention"), None),
     ("gov-12", 1, MCMAHON2("McMahon would introduce a TRUST Act so money is spent as Congress authorized"), "to ensure federal dollars are spent exactly as Congress authorized"))
HULUM2 = site("Jeffrey Hulum III", "https://www.jeffreyhulumiiiforcongress.com/issues", READ27)
more("MS-H-04", "MS-H-04:hulum",
     ("eco-03", 1, HULUM2("Hulum says families should be able to earn a living wage"), "Families should be able to earn a living wage, support their children, and build a secure life right here at home."),
     ("edu-01", 1, HULUM2("Hulum calls investing in schools the best investment"), "Strong schools build strong communities"),
     ("cri-05", 1, HULUM2("Hulum wants a justice system that ensures rehabilitation"), "Our justice system should keep communities safe while ensuring fairness, accountability, and rehabilitation."))
BERNING = site("Nathan Berning", "https://berningforcongress.com/", READ27)
more("HI-H-01", "HI-H-01:berning",
     ("soc-03", -1, BERNING("Berning calls himself pro-life and focuses on support so poverty pushes no mother toward abortion"), "I also believe being pro-life must mean more than telling a frightened woman what she should not do."),
     ("hou-01", 1, BERNING("Berning would fight for federal housing partnerships"), "I will fight for federal housing and infrastructure partnerships that expand opportunity without erasing community"))
HOOK2 = site("Kristin Hook", "https://www.drkristinhook.org/issues", READ27)
cand("TX-H-21", "TX-H-21:hook", "Kristin Hook", "D", None,
     ("soc-03", 1, HOOK2("Hook’s platform calls for restoring abortion freedoms"), "Abortion: Restoring Our Freedoms"))
STIGALL = site("Chris Stigall", "https://www.stigallforcongress.com/", READ27)
STIGALL2 = site("Chris Stigall", "https://www.stigallforcongress.com/issues", READ27)
more("MO-H-06", "MO-H-06:stigall",
     ("soc-04", 2, STIGALL2("Stigall is pro-life and would oppose taxpayer funding for abortion"), "I am proudly pro-life and believe every human life is a gift from God that deserves protection."),
     ("soc-03", -2, STIGALL("Stigall is pro-life"), None),
     ("edu-06", 1, STIGALL("Stigall and his wife have promoted school choice"), "have worked actively to promote school choice"))
VERBICA2 = site("Peter Coe Verbica", "https://peterverbica.com/about", READ27)
more("CA-H-19", "CA-H-19:verbica",
     ("gov-05", 1, VERBICA2("Verbica supports California’s voter ID initiative"), "He supports the California Voter ID initiative which is slated for the 2026 ballot"))
GRAGE2 = site("Rachel Grage", "https://rachelgrage.com/", READ27)
more("FL-H-05", "FL-H-05:grage",
     ("ene-08", 1, GRAGE2("Grage would expand conservation funding and invest in disaster resilience"), "Defend coastal ecosystems, expand conservation funding, and invest in disaster resilience."),
     ("soc-02", 1, GRAGE2("Grage would ensure equality under the law for all Americans"), "Protect personal privacy and access to healthcare, ensure equality under the law for all Americans, and uphold dignity and due process in immigration policy."))
BARRIOS = site("Dan Barrios", "https://www.danbarriosforcongress.com/", READ27)
cand("TX-H-32", "TX-H-32:barrios", "Dan Barrios", "D", None,
     ("hea-01", 1, BARRIOS("Barrios says nobody should be without affordable, quality care"), "Healthcare is a basic necessity and Dan believes nobody should be left without access to affordable and quality medical care."))
WHIPPLE = site("Cody Whipple", "https://codyk4congress.com/", READ27)
WHIPPLE2 = site("Cody Whipple", "https://codyk4congress.com/issues/", READ27)
more("NV-H-04", "NV-H-04:whipple",
     ("edu-06", 2, WHIPPLE("Whipple strongly advocates school choice"), "He is a strong advocate for school choice, career and technical education, and expanding youth sports opportunities"),
     ("edu-03", 1, WHIPPLE("Whipple advocates career and technical education"), None),
     ("eco-02", 1, WHIPPLE2("Whipple would eliminate taxes on tips"), "Protect tipped workers by eliminating taxes on tips and defending overtime pay."))
ST_JOHN = site("Steven St. John", "https://chaplainstevenstjohnforcongress.com/", READ27)
more("NV-H-01", "NV-H-01:john",
     ("hea-03", 1, ST_JOHN("St. John would protect Medicare and Medicaid"), "Advocating for access to care, protecting Medicare and Medicaid, and lowering the burden of medical costs."))
KINNEY2 = site("Lisa Kinney", "https://lisakinneyforcongress.com/meet-lisa-kinney/", READ27)
cand("WY-H-00", "WY-H-00:kinney", "Lisa Kinney", "D", None,
     ("gov-09", 1, KINNEY2("Kinney says officials shouldn’t make decisions that enrich themselves"), "elected officials should not make decisions to increase their wealth while cutting benefits to Wyoming people"))
FOX_SPENCER = site("Belinda Fox-Spencer", "https://www.belindafoxspencerwv.com/", READ27)
cand("WV-H-01", "WV-H-01:fox-spencer", "Belinda Fox-Spencer", "Constitution", None,
     ("soc-04", 1, FOX_SPENCER("Fox-Spencer is proudly pro-life"), "I am proudly pro-life"),
     ("soc-03", -1, FOX_SPENCER("Fox-Spencer is proudly pro-life"), None))
HERRERA2 = site("Jordan Herrera", "https://jordanjherrera.com/issues/", READ27)
cand("MO-H-04", "MO-H-04:herrera", "Jordan Herrera", "D", "Disabled Air Force veteran and former union member who began his career in the trades.",
     ("soc-03", 1, HERRERA2("Herrera says the federal government shouldn’t regulate your body or personal decisions"), "The federal government should not be able to regulate your body, your marriage, your religion in schools, or your personal life decisions."),
     ("def-03", 1, HERRERA2("Herrera supports the military and veterans"), "I support our nation’s military and our veterans."))
CRAIG = site("Kevin Craig", "https://www.kevincraig.us/", READ27)
cand("MO-H-07", "MO-H-07:craig", "Kevin Craig", "L", None,
     ("eco-07", 2, CRAIG("Craig would cut a trillion dollars from federal spending"), "Kevin Craig wants to cut a trillion dollars from federal spending"))

# KQED's voter guide (read Oct. 27) summarizes four Northern California House races
# from interviews, questionnaires, debates and news coverage, quoting the candidates.
# Its paraphrases are KQED's; the quotes are the candidates' words as KQED gives them.
KQED = lambda slug, d: lambda note: page(f"KQED voter guide, U.S. House District {d}: {note}", f"https://www.kqed.org/voterguide/{slug}", READ27)  # noqa: E731
KQED1 = KQED("sonoma/congress-1st-district", 1)
more("CA-H-01", "CA-H-01:mcguire",
     ("eco-10", -2, KQED1("McGuire would eliminate Trump’s tariffs, which he says are wreaking havoc on the economy"), "wreaking havoc on our economy"),
     ("hea-07", 1, KQED1("McGuire would repeal the Medicaid and Affordable Care Act cuts and restore the federal subsidy that kept Medicare Part D premiums down"), None))
cand("CA-H-01", "CA-H-01:gallagher", "James Gallagher", "R", None,
     ("eco-10", 1, KQED1("Gallagher wants to use tariffs to win better deals for American farms"), "Tariffs in the interim have had an increase in some supply costs, but it’s also helping to get better trade deals"),
     ("ene-10", 1, KQED1("Gallagher would press the state to cut the gas tax and exempt some fuels from cap-and-invest"), "it’s kind of a double taxation when you put fuels under cap-and-[invest] as well"),
     ("imm-07", 1, KQED1("Gallagher says ICE should focus on violent criminals rather than broad sweeps and raids"), None),
     ("ene-08", 1, KQED1("Gallagher wants more funding for fuel reduction and wildfire prevention"), "We need to get on top of the issue fast."))
KQED4 = KQED("california/congress-4th-district", 4)
cand("CA-H-04", "CA-H-04:jones", "Eric Jones", "D", "Former venture capitalist and CEO of the American Dream Institute, a nonprofit; 35 and running for office for the first time.",
     ("hea-01", 2, KQED4("Jones supports Medicare for All"), "I believe that healthcare is a human right and that everyone should have access to it."),
     ("hea-10", 2, KQED4("Jones would expand Medicare to cover in-home nursing, dental, vision and hearing care"), None),
     ("imm-08", -1, KQED4("Jones would move ICE out of the Department of Homeland Security and eliminate the funding it received last year"), None),
     ("eco-04", 1, KQED4("Jones would push to break up PG&E’s monopoly"), "PG&E cannot be held accountable because they’re a state-regulated monopoly and there is no competition"),
     ("agr-01", 1, KQED4("Jones wants U.S. farm subsidies on par with what the EU spends on its farmers"), None),
     ("agr-06", 1, KQED4("Jones would expand export promotion for specialty crops and enforce foreign trade agreements that aren’t being honored"), None))
KQED11 = KQED("sanfrancisco/congress-11th-district", 11)
more("CA-H-11", "CA-H-11:chan",
     ("hea-01", 2, KQED11("Chan would pass Medicare for All"), "We must lower costs beyond housing by passing Medicare for All, capping childcare expenses, expanding the Child Tax Credit"),
     ("soc-07", 2, KQED11("Chan would cap childcare expenses and fund universal childcare"), None),
     ("eco-02", 1, KQED11("Chan would expand the Child Tax Credit and give renters tax deductions"), None),
     ("eco-01", 2, KQED11("Chan supports raising taxes on Americans with fortunes over $50 million to fund housing, childcare, schools and healthcare"), "A billionaire should not pay a smaller share of their income in taxes than our teachers and nurses"),
     ("eco-12", 1, KQED11("Chan supports a corporate minimum tax and higher taxes on the largest fortunes"), None),
     ("hou-01", 2, KQED11("Chan would repeal the Faircloth Amendment and add housing tax credits, Section 8 vouchers and financing for affordable housing"), None),
     ("hou-06", 1, KQED11("Chan wants stronger tenant protections"), None),
     ("eco-09", 1, KQED11("Chan wants living wages and strong unions"), "ensure workers have living wages, strong unions, safe workplaces and a voice in the technologies reshaping their jobs"),
     ("def-11", -2, KQED11("Chan says the Israeli government is committing genocide in Gaza"), "The Israeli government is committing genocide in Gaza and violating the Leahy Law, and our relationship cannot continue as a blank check."),
     ("def-12", -2, KQED11("Chan would block all weapons transfers to Israel"), None),
     ("def-15", -2, KQED11("Chan says Congress must end the war with Iran"), "Congress must end this war, reassert constitutional authority over war powers and pursue diplomacy and regional peace"))
more("CA-H-11", "CA-H-11:wiener",
     ("eco-01", 2, KQED11("Wiener supports Elizabeth Warren’s Ultramillionaire Tax on fortunes over $50 million, saying public services are severely underfunded"), None),
     ("eco-11", 1, KQED11("Wiener would enact paid family leave and a low-cost childcare program"), "enact paid family leave and a low-cost childcare program and expand public transportation"),
     ("soc-07", 1, KQED11("Wiener would create a low-cost childcare program"), None),
     ("ene-07", 1, KQED11("Wiener would expand public transportation"), None),
     ("hou-06", 1, KQED11("Wiener wants stronger renter protections"), None),
     ("hou-01", 1, KQED11("Wiener would build 8 million homes at all income levels, reversing federal tax cuts to pay for it"), None),
     ("def-12", -2, KQED11("Wiener opposes U.S. funding for the Israeli military and the sale of offensive arms"), "the U.S. must not enable the destruction of Palestinian and Lebanese communities"),
     ("def-15", -2, KQED11("Wiener opposes funding the war in Iran"), "illegal, immoral and a disaster"))
KQED14 = KQED("alameda/congress-14th-district", 14)
cand("CA-H-14", "CA-H-14:hernandez", "Melissa Hernandez", "D", "BART board director, former mayor of Dublin and a healthcare director in Alameda County Supervisor David Haubert’s office; lost the August special election for this seat to Aisha Wahab.",
     ("hea-03", 1, KQED14("Hernandez would protect Medicare and restore the Medicaid cuts in Trump’s “one big beautiful bill”"), None),
     ("eco-10", -1, KQED14("Hernandez says she will work to overturn Trump’s tariffs"), None))
cand("CA-H-14", "CA-H-14:wahab", "Aisha Wahab", "D", None,
     ("hea-01", 1, KQED14("Wahab says Congress should move toward a Medicare for All model of single-payer healthcare"), None),
     ("def-11", -2, KQED14("Wahab criticizes Israel’s actions in Gaza as a genocide"), "Israel has a full right to defend itself, but it has gone too far, and it’s at a point where it is a genocide"),
     ("def-12", -2, KQED14("Wahab supports ending military aid to Israel"), None),
     ("hou-01", 1, KQED14("Wahab will prioritize more federal funding for affordable housing"), None))

# KATU's "Know Your Candidates" interviews (Portland, October 2026) post a lightly
# edited transcript of each candidate's answers to the same questions; the quotes
# are from those transcripts.
KATU = lambda slug: lambda note: page(f"KATU Know Your Candidates interview: {note}", f"https://katu.com/news/know-your-candidates/{slug}", READ27)  # noqa: E731
KATU_AYLES = KATU("loran-ayles-us-house-district-3")
cand("OR-H-03", "OR-H-03:ayles", "Loran Ayles", "R", "Trade union worker who grew up in Estacada and lives in Hood River.",
     ("def-15", -1, KATU_AYLES("Ayles doesn’t fully agree with Trump’s approach to Iran and wants the conflict ended"), "I would like to see the conflict ended in a way that brings peace and stability back to the region"),
     ("def-04", 1, KATU_AYLES("Ayles says Congress is constitutionally bound to authorize war"), "Congress is the one constitutionally bound to authorize war ongoing."))
more("OR-H-01", "OR-H-01:kahl",
     ("def-15", 1, KATU("barbara-kahl-us-house-district-1")("Kahl supports military action against Iran, with no ground troops"), "I do support military action, maybe not exactly how President Trump is enacting it"))
KATU_DESPAIN = KATU("monique-despain-us-house-district-4")
more("OR-H-04", "OR-H-04:despain",
     ("def-15", 1, KATU_DESPAIN("DeSpain backs disarming Iran of nuclear weapons, swiftly"), "we need to swiftly accomplish the mission, which is to disarm Iran of nuclear weapons and get out of there"),
     ("def-04", 1, KATU_DESPAIN("DeSpain says Congress should not shirk its oversight of military action"), "Congress has oversight of these decisions and Congress should not shirk from those responsibilities"),
     ("hou-01", -1, KATU_DESPAIN("DeSpain wants housing working people can afford, not subsidized housing"), "The housing solution is affordable housing, not subsidized housing, not free housing"))
KATU_ADAIR = KATU("patti-adair-us-house-district-5")
more("OR-H-05", "OR-H-05:adair",
     ("def-04", 1, KATU_ADAIR("Adair would vote for a war powers resolution on Iran"), "when I'm there, I would vote for the war powers act"),
     ("def-15", -1, KATU_ADAIR("Adair would vote for a war powers resolution because the Iran war has gone on so long"), None),
     ("eco-07", 1, KATU_ADAIR("Adair wants the national debt reined back to pre-COVID levels"), "We have to really not spend our children's inheritance."))
KATU_RUSS = KATU("david-russ-us-house-district-6")
more("OR-H-06", "OR-H-06:russ",
     ("eco-03", -1, KATU_RUSS("Russ says government can’t tell companies what to pay their employees"), "We can't go around telling companies what price to charge or what to pay their employees."),
     ("def-08", -1, KATU_RUSS("Russ opposes taking part in other countries’ wars"), "We need to stay on our own land and take care of ourselves unless there's clearly an obvious and imminent national security issue."))

# VOTE411, the League of Women Voters' guide, publishes candidates' own unedited answers
# to the League's questions. Read Oct. 27 in the browser pane (the guide renders with
# JavaScript), one race at a time; quotes were checked against the page text. Working
# Class Party candidates list the party's campaign site as their own.
V411 = lambda race_id: lambda note: page(f"VOTE411 (League of Women Voters) voter guide, candidates’ answers: {note}", f"https://www.vote411.org/ballot?lwv-ballot-widget-raceid={race_id}", READ27)  # noqa: E731
WCP = "https://workingclassfight.com/"
V411_IL4 = V411(6475590)
cand("IL-H-04", "IL-H-04:hershey", "Ed Hershey", "Working Class",
     "Has worked in Chicago Public Schools for two decades at Lindblom High School, twelve years of them as a union representative.",
     ("gov-06", 2, V411_IL4("Hershey says voting should be as easy as possible, with mail-in voting, early voting and drop boxes"), "Voting should be made as easy as possible. Mail-in voting, early voting and drop boxes all work."),
     ("def-15", -2, V411_IL4("Hershey opposes U.S. tax dollars going to wars in Gaza, Lebanon, Syria and Iran"), "We should not accept that our tax dollars go to wreak destruction in Gaza, Lebanon, Syria and Iran"),
     ("def-12", -2, V411_IL4("Hershey opposes tax dollars going to the war in Gaza"), None),
     ("def-01", -2, V411_IL4("Hershey would spend the billions that go to weapons on infrastructure, education and health care"), "those billions that are diverted to build weapons of war, should be spent to shore up our infrastructure"),
     ("eco-06", 1, V411_IL4("Hershey would spend weapons money on infrastructure"), None),
     ("imm-08", -2, V411_IL4("Hershey calls immigration enforcement state terrorism against immigrant workers"), "We must end the state terrorism that is being carried out against the immigrant part of the working class."),
     officialSite=WCP)
V411_MI1 = V411(25687793)
cand("MI-H-01", "MI-H-01:hakola", "Liz Hakola", "Working Class", "Retired after 31 years as a utility company worker.",
     ("hea-01", 2, V411_MI1("Hakola calls universal health care for all residents a basic human right"), "Universal health care for all residents regardless of citizenship is a basic human right."),
     ("eco-10", -1, V411_MI1("Hakola blames high tariffs for falling earning power"), "high tariffs (a tax) put on basically everything"),
     ("imm-08", -1, V411_MI1("Hakola condemns current immigration enforcement"), "Immigration policies are barbaric, inhumane, racist and cruel."),
     ("def-15", -1, V411_MI1("Hakola wants the wars stopped"), "Stop the wars and the destruction of the planet."),
     officialSite=WCP)
cand("MI-H-01", "MI-H-01:satterla", "Arnett Satterla", "L", "Industrial field service engineering and maintenance worker.",
     ("hea-01", -1, V411_MI1("Satterla opposes a federal takeover of health care"), "I do not support a one-size-fits-all federal takeover."),
     ("hea-04", 1, V411_MI1("Satterla wants competition, price transparency and patient choice in health care"), "I would support reforms that increase competition, price transparency, patient choice, and access to care."),
     ("eco-02", 1, V411_MI1("Satterla supports lower taxes"), "I would support lower taxes, less unnecessary regulation on small businesses, more competition, responsible spending"),
     ("imm-01", 1, V411_MI1("Satterla supports securing the border"), "I support securing the border, stopping unlawful entry, ending catch-and-release, and deporting everyone here illegally."),
     ("imm-02", -2, V411_MI1("Satterla supports deporting everyone here illegally"), None),
     ("imm-03", -1, V411_MI1("Satterla supports a full pause on immigration"), "I also support a full pause on immigration until we restore enforcement, screening, and confidence in the system."),
     ("eco-07", 1, site("Arnett Satterla", "https://sites.google.com/view/arnettforcongress/issues", READ27)("Satterla says Washington spends too much"), "Washington has grown too large, spends too much, regulates too much, and reaches too far into people’s daily lives."),
     officialSite="https://sites.google.com/view/arnettforcongress")
V411_MI5 = V411(25687923)
MUSZYNSKI = site("Ron Muszynski", "https://www.rescuemichigan.net/", READ27)  # renders only in a browser
cand("MI-H-05", "MI-H-05:muszynski", "Ronald A. Muszynski", "L", "Retired turbine engine design engineer and longtime Grass Lake resident.",
     ("agr-06", 1, V411_MI5("Muszynski faults the U.S. for not forming trade partnerships"), "At every turn we are regulating, blaming and punishing industry and not forming trade partnerships with the world."),
     ("eco-07", 1, MUSZYNSKI("Muszynski would balance the budget"), "Balance The Budget"),
     ("def-07", 2, MUSZYNSKI("Muszynski says war should be last on a very long list"), "Sending immature children to kill another countries children should be last on a very long list."),
     ("def-15", -1, MUSZYNSKI("Muszynski disputes the case for the war with Iran"), "Every government intelligence agency agreed that Iran was holding up its end of all previous nuclear negotiations."),
     ("soc-08", 1, MUSZYNSKI("Muszynski objects to government and big business recording people’s data"), "Government and Big Business records and stores all of your phone calls, text messages, emails, digital purchases and daily travels."),
     officialSite="https://www.rescuemichigan.net/")
cand("MI-H-05", "MI-H-05:renier", "Sharon M. Renier", "U.S. Taxpayers", "Organic farmer and, for 45 years, a paralegal.",
     ("hea-01", -1, V411_MI5("Renier says the Constitution guarantees no health care"), "There is NOTHING in the Constitution that guarantees health care."),
     ("edu-03", 1, V411_MI5("Renier wants more apprenticeship programs"), "We need more apprentice programs--teaching people how to use their hands for more than a phone."),
     ("ene-01", -1, V411_MI5("Renier objects to solar panels and windmills on farmland"), "the electric company wants to take valuable farm land and put solar panels and windmills all over the place"))
BRONKE = lambda page_path: site("Jim Bronke", f"https://www.bronkeforcongress.org/{page_path}", READ27)  # noqa: E731
cand("MI-H-05", "MI-H-05:bronke", "Jim Bronke", "G", "Retired electrical engineer with 30 years of experience.",
     ("def-01", -1, V411_MI5("Bronke would cut military spending"), "Cut military spending."),
     ("def-15", -2, BRONKE("")("Bronke opposes the war with Iran"), "I am not a supporter of this war"),
     ("ene-01", 1, BRONKE("climate-change-issues/")("Bronke supports solar, wind and nuclear power"), "I certainly will support solar, wind and even nuclear power improvements that present as CO2 alternative to our future."),
     ("ene-02", 1, BRONKE("climate-change-issues/")("Bronke supports nuclear power improvements"), None),
     ("eco-07", 1, BRONKE("about-us/")("Bronke says government must get its spending under control"), "our government must get its spending under control"),
     officialSite="https://www.bronkeforcongress.org/")
cand("MI-H-08", "MI-H-08:goodwin", "Kathy Goodwin", "Working Class", "Healthcare social worker from the Flint area, with a master’s degree in social work from the University of Michigan.",
     ("hea-01", 2, V411(25687766)("Goodwin calls health care a basic human right"), "I believe that healthcare is a basic human right."),
     ("soc-03", 1, V411(25687766)("Goodwin supports self-determination over one’s own body and health care"), "I stand for the right to self-determination about one’s own body and one’s own healthcare decisions."),
     ("eco-03", 1, V411(25687766)("Goodwin wants wages to rise automatically with prices"), "I think wages, pensions and disability payments need to automatically and immediately increase whenever prices increase."),
     ("ene-01", 1, V411(25687766)("Goodwin supports renewable energy under local control"), "I am all for renewable energy, under the control of the population who lives in the area where the energy is produced."),
     ("soc-01", 1, V411(25687766)("Goodwin supports the right to free speech"), "The 1st Amendment is the Right to Free Speech. I am for this right."),
     officialSite=WCP)
V411_MI9 = V411(25687821)
cand("MI-H-09", "MI-H-09:vayko", "Kevin Vayko", "L", "Environmental engineer.",
     ("def-10", 1, V411_MI9("Vayko would subsidize Americans’ health care before foreign aid and foreign conflicts"), "If the US can afford to subsidize Isreali healthcare and useless foreign conflicts, why not subsidize healthcare for its own citizens?"),
     ("hea-07", 1, V411_MI9("Vayko would subsidize health care for Americans"), None),
     ("hea-09", 1, V411_MI9("Vayko says preventive care is critical"), "Simplifying healthcare to allow preventative care is critical to mitigate long term costs."))
cand("MI-H-09", "MI-H-09:walkowicz", "Jim Walkowicz", "Working Class", "Retired UAW union representative, elected by co-workers from 1981 to 2022.",
     ("hea-01", 2, V411_MI9("Walkowicz says health care should be a basic right for all"), "Everyone is entitled to health care. This should be a basic right for all people."),
     ("eco-03", 1, V411_MI9("Walkowicz says the lowest wages need to go up"), "Wages for those making the least amount of money, needs to go up. Everyone should receive a living wage."),
     ("eco-06", 1, V411_MI9("Walkowicz wants money spent modernizing infrastructure"), "Money should go to modernizing the infrastructure rather than as profits to the rich."),
     officialSite=WCP)
cand("MI-H-10", "MI-H-10:kirby", "Andrea L. Kirby", "Working Class", "Union representative.",
     ("hea-01", 2, V411(25687822)("Kirby says only a true universal health care system is the answer"), "Only a true universal health care system is the answer."),
     officialSite=WCP)
V411_MI12 = V411(25687874)
cand("MI-H-12", "MI-H-12:walkowicz", "Gary Walkowicz", "Working Class", "Retired after 45 years at Ford on the assembly line and as an elected UAW representative; ran for UAW president.",
     ("hea-01", 2, V411_MI12("Walkowicz wants a national health care system"), "We must have a national health care system."),
     ("eco-03", 2, V411_MI12("Walkowicz says the minimum wage should be five times higher"), "The minimum wage should be 5 times higher."),
     ("imm-02", 2, V411_MI12("Walkowicz says people who come here to work should not be illegal"), "If someone comes here to work, they should not be \"illegal\"."),
     ("imm-08", -1, V411_MI12("Walkowicz says immigrant workers should not have their homes invaded by ICE"), None),
     officialSite=WCP)
cand("MI-H-13", "MI-H-13:coleman", "Simone R. Coleman", "Working Class", "Retired after 30 years in road construction; works in home health care.",
     ("hea-01", 2, V411(25687894)("Coleman says everyone deserves universal health care"), "Everyone in America deserves universal health care."),
     ("eco-03", 1, V411(25687894)("Coleman says a living wage should be the starting wage of all jobs"), "A living wage should be the starting wage of all jobs."),
     ("soc-01", 1, V411(25687894)("Coleman supports freedom of speech and peaceful assembly"), "People should have the right to freedom of speech (no harm to others) and peaceful assembly."),
     officialSite=WCP)

# Campaign sites found Oct. 27 by searching for candidates who had none.
HELI = lambda page_path: site("Heli Rodriguez Prilliman", f"https://www.helifortexas.com/{page_path}", READ27)  # noqa: E731
cand("TX-H-12", "TX-H-12:prilliman", "Angela Rodriguez Prilliman", "D",
     "Fort Worth entrepreneur raised in Stephenville and a Texas A&M graduate; founded Lacquerbar and was on the founding team of the software company Fivestars.",
     ("hea-01", 2, HELI("issues")("Prilliman advocates a universal health care system"), "I'm advocating for a universal healthcare system and a universal child care system"),
     ("soc-07", 2, HELI("issues")("Prilliman advocates universal child care"), None),
     ("eco-01", 2, HELI("issues")("Prilliman would pay for universal health and child care by taxing billionaires"), "all paid for by taxing the small group of billionaires who have taken advantage of American workers"),
     ("gov-11", 1, HELI("")("Prilliman would remove billionaire money from politics"), "the removal of billionaire money in politics"),
     ("edu-01", 1, HELI("")("Prilliman would fully fund public schools"), "fully funding our public schools"),
     ("imm-08", -1, HELI("issues")("Prilliman calls ICE lawless"), None),
     officialSite="https://www.helifortexas.com/")
VERLATO = site("April Verlato", "https://verlatoforcongress.com/?page_id=120", READ27)
cand("CA-H-28", "CA-H-28:verlato", "April Verlato", "R",
     "Attorney who took over her father’s law practice in 2000; two terms on the Arcadia City Council and mayor during COVID-19. Ran against Judy Chu in 2024.",
     ("imm-01", 1, VERLATO("Verlato advocates stronger border security"), "advocating for stronger border security measures"),
     ("cri-01", 1, VERLATO("Verlato backed every budget request from Arcadia’s police chief"), "voted to support all plans, ordinances, and budget requests from the Police Chief"),
     ("cri-06", -1, VERLATO("Verlato organized support for the lawsuit against zero bail"), "organizing support for the lawsuit against the zero bail policy"),
     ("eco-01", -1, VERLATO("Verlato opposes tax increases and backs the Taxpayer Protection Pledge"), "A proponent of the Taxpayer Protection Pledge"),
     ("eco-07", 1, VERLATO("Verlato would address the national debt"), "responsible budgeting, targeted spending reviews, and bipartisan collaboration"),
     ("def-01", 1, VERLATO("Verlato supports enhancing America’s military strength"), "April supports enhancing America’s military strength and ensuring energy independence"),
     ("def-03", 1, VERLATO("Verlato wants more veteran clinics and a major medical center in the San Gabriel Valley"), "establishing more veteran clinics and a major medical center in the San Gabriel Valley"),
     ("hea-06", 1, VERLATO("Verlato advocated better mental health and substance abuse treatment"), "advocating for better mental health and substance abuse treatment facilities"),
     ("hea-04", 1, site("April Verlato", "https://verlatoforcongress.com/", READ27)("Verlato champions market-driven health care"), "championing market-driven healthcare solutions"),
     officialSite="https://verlatoforcongress.com/")

# Tennessee in VOTE411 (the League of Women Voters of Tennessee's guide), read Oct. 27.
# Of the independents with no site or statement, only Blankenship and Ward answered;
# Ashburn, Baker, Campbell, Cody, McClain (1st), Howard-Hill, Ownby, Roland (3rd),
# Faircloth (4th), James Johnson (5th), Koontz (7th), Horace Taylor, Austill, Futch (8th),
# Head and Clark (9th) left every question blank.
V411_TN5, V411_TN6, V411_TN8 = V411(68459359), V411(68459384), V411(68459415)
cand("TN-H-05", "TN-H-05:leary", "Micheál O'Leary", "I",
     "Former mayor of Culver City, Calif., with eight years in elected office; hospitality business owner and No Labels delegate who studied agricultural science at University College Dublin.",
     ("def-04", 1, V411_TN5("O’Leary blames rising costs on a war Congress never approved"), "The big driver is a war Congress never approved."),
     ("def-15", -1, V411_TN5("O’Leary faults the unauthorized war for rising fuel and fertilizer prices"), None),
     ("eco-10", -1, V411_TN5("O’Leary says tariffs added to the cost of living"), "Tariffs on top of that, with unintended consequences nobody in Washington wants to talk about."),
     ("edu-03", 1, V411_TN5("O’Leary wants schools to train students for all jobs, not just the best-paid"), "Curriculum should be built around all employment, not just the high-earning tracks."))
CROLEY = site("Mike Croley", "https://croleyforcongress.com/", READ27)
more("TN-H-06", "TN-H-06:croley",
     ("hou-01", 1, V411_TN6("Croley would expand affordable housing through federal incentives"), "expanding the supply of affordable housing through federal incentives"),
     ("eco-04", 1, V411_TN6("Croley would enforce antitrust laws"), "enforcing antitrust laws to promote competition"),
     ("eco-06", 1, V411_TN6("Croley would invest in infrastructure"), "investing in infrastructure that creates good-paying jobs"),
     ("eco-12", 1, V411_TN6("Croley would reform the tax code so working families don’t pay a higher share than billionaires"), "reforming the tax code so working families are not paying a higher share than billionaires and large corporations"),
     ("gov-11", 1, V411_TN6("Croley supports campaign finance reform"), "support campaign finance reform"),
     ("edu-03", 1, V411_TN6("Croley would expand career and technical education"), "expanding career and technical education"),
     ("hou-09", 1, V411_TN6("Croley would improve rural broadband"), "improving rural broadband access"),
     ("eco-10", -2, CROLEY("Croley would get rid of Trump’s tariffs"), "Get rid of Trump’s reckless tariffs."),
     ("eco-01", 1, CROLEY("Croley would tax the rich fairly and close loopholes"), "Tax the rich fairly and close tax loopholes."),
     ("hou-02", 1, CROLEY("Croley would cap private equity firms’ holdings"), "Cap private equity firm holdings."),
     ("agr-03", 1, CROLEY("Croley would invest in American industry"), "Invest in American industry and American trades."),
     ("eco-09", 1, CROLEY("Croley would make unionizing easier"), "Strengthen labor standards and make unionization easier"),
     officialSite="https://croleyforcongress.com/")
cand("TN-H-08", "TN-H-08:blankenship", "Wells Blankenship", "I", "Fifty years in small business and in broadcast and grocery-chain advertising.",
     ("eco-07", 2, V411_TN8("Blankenship would cut federal spending by half"), "Cut Federal Spending by 50%"),
     ("ene-02", 2, V411_TN8("Blankenship supports small modular and molten salt nuclear reactors"), "Support the development and implementation of Small Modular Reactors and Molten Salt Reactors to provide the cleanest and most affordable energy."))
cand("TN-H-08", "TN-H-08:ward", "Henry Ward III", "I", "Owner of Ward’s Home Inspectors since 1993; University of Memphis graduate.",
     ("eco-02", 2, V411_TN8("Ward would end income tax for those earning under $100,000"), "The income tax on individuals should be eliminated for those earning below $100,000 and reduced for those who earn under $300,000."),
     ("def-08", -1, V411_TN8("Ward would cut the number of overseas military bases"), "We must reduce the number of overseas military bases and installations and begin to divorce our nation from foreign entanglements."),
     ("eco-06", 1, V411_TN8("Ward would spend the savings on domestic infrastructure"), "These installations could be reduced and those funds directed to upgrade domestic infrastructure and fund the growth of our economy."),
     ("edu-07", 1, V411_TN8("Ward wants education run locally"), "Education should continue to be administered on a local level as the people deem to be appropriate."),
     ("soc-08", 1, V411_TN8("Ward would regulate data centers to protect citizens’ private information"), "The data centers would have to be regulated to protect the private information of citizens"))

# Colorado in VOTE411 (League of Women Voters of Colorado), read Oct. 27. Critter Milton
# (Unity, 1st), Gaylon Kent (L, 2nd), Lawrence Clark (Constitution) and Susan Hall
# (Unity, 7th) left every question blank. Wikipedia calls the 8th's Libertarian "Dan
# Wood"; the ballot, VOTE411 and his own site say Dave Wood.
cand("CO-H-03", "CO-H-03:robertson", "Cory Robertson", "L", None,
     ("eco-04", 1, V411(68344457)("Robertson would keep large corporations from monopolizing prices"), "I would restrict the market in the sense of keeping large corporations from shutting out the competition and being able to monopolize prices."),
     ("gov-11", 1, V411(68344457)("Robertson calls corporate lobbying the biggest threat to a free economy"), "Corporate lobbying is the biggest threat to a free economy."))
V411_CO5 = V411(68344523)
cand("CO-H-05", "CO-H-05:elworth", "Mark Elworth", "L", None,
     ("def-07", 1, V411_CO5("Elworth would oppose unnecessary foreign conflicts and rely on diplomacy"), "I would work to restore accountability, strengthen our relationships with allies, protect our constitutional rights, and oppose unnecessary foreign conflicts."),
     ("def-02", 1, V411_CO5("Elworth would strengthen relationships with allies"), None),
     ("eco-02", 1, V411_CO5("Elworth would reduce the tax burden on families"), "I would work to reduce the tax burden on American families"),
     ("eco-10", -1, V411_CO5("Elworth would restore free and open trade"), "eliminate unnecessary regulations, and restore free and open trade"),
     ("def-15", -1, V411_CO5("Elworth points to the war with Iran’s cost to energy prices"), "We should consider the economic and energy consequences before entering foreign wars"))
V411_CO8 = V411(3676098)
cand("CO-H-08", "CO-H-08:wood", "Dave Wood", "L", "Retired; ran for the Colorado House as a Libertarian in 2000.",
     ("def-04", 2, V411_CO8("Wood would tighten the War Powers Resolution after the undeclared war with Iran"), "I would work to strengthen that to prevent future presidential authority to arbitrary decide to send our forces to war"),
     ("def-15", -1, V411_CO8("Wood calls the Iran war undeclared"), None),
     ("eco-10", -2, V411_CO8("Wood would stop imposing tariffs"), "Stop imposing tariffs on other countries to favor special interests which causes inflation and hurts the poor more than the rich."),
     ("agr-06", 1, V411_CO8("Wood wants to return to free trade"), "We should go back to free trade"),
     ("eco-07", 2, V411_CO8("Wood would stop deficit spending and shrink the federal government"), "Reduce the size and expense of our federal government as much as possible to lower our tax burdens."),
     ("ene-02", 2, V411_CO8("Wood would remove federal barriers to nuclear power"), "As nuclear power is the cleanest, most reliable and now safest alternative energy source we have, I would work to remove any existing federal barriers."),
     ("eco-01", 1, V411_CO8("Wood would add a tax on incomes over $200,000 for Social Security"), "Create an additional tax similar to the current “Additional Medicare Tax” on incomes over $200,000."),
     officialSite="https://davewood4colorado.com/")

# New Jersey in VOTE411 (League of Women Voters of New Jersey), read Oct. 27. Seamus
# O'Toole (7th, on the ballot as "Stop Israel's Genocide") left every question blank.
# Ryan Kelly's site (kellyfornj03.com) comes from his VOTE411 email address and answers
# with his name; his iVoterGuide answers already cover legal abortion access.
V411_NJ2 = V411(68198479)
cand("NJ-H-02", "NJ-H-02:mora", "Ramon Mora Jr.", "I", None,
     ("imm-08", -2, V411_NJ2("Mora would abolish ICE"), "ICE: Abolish, Prosecute those responsible, and replace with the ADU."),
     ("gov-11", 2, V411_NJ2("Mora would end Citizens United and remove corporate money from politics"), "End Citizens United, Remove corporate money from Politics, Ban Foreign spending on campaigns, Ban individual Stock trading"),
     ("gov-13", -2, V411_NJ2("Mora would end Citizens United"), None),
     ("gov-02", 2, V411_NJ2("Mora would ban individual stock trading by members"), None),
     ("eco-04", 1, V411_NJ2("Mora would break up monopolies to cut food prices"), "Reduce Food prices by breaking up monopolies, unfair market manipulation amongst corporations"),
     ("hea-01", 2, V411_NJ2("Mora supports Medicare for All, a single-payer system"), "proceed with a Medicare for all / Single payer system"),
     ("hea-04", -2, V411_NJ2("Mora would end private insurance as the mainstay of health care"), "I would move to see that sector removed as the main stay way of dealing with healthcare"),
     ("imm-02", 1, V411_NJ2("Mora wants better pathways to citizenship"), "There needs to be better pathways to citizenship and residencies."),
     ("imm-04", 1, V411_NJ2("Mora wants more immigration judges"), "That is accomplished by having better, secured, efficient ports of entry, and more immigration judges and lawyers."),
     ("soc-03", 2, V411_NJ2("Mora is pro-choice"), "I am First and Foremost Pro-Choice."),
     ("soc-04", -2, V411_NJ2("Mora opposes abortion bans"), None),
     ("ene-03", -1, V411_NJ2("Mora wants less dependence on oil and gas"), "I would like to see less dependence on Oil and Gas while promoting other means of electricity generation."),
     ("gov-06", 2, V411_NJ2("Mora wants same-day registration and wider mail voting"), "Same day Voter Registration, Expanded mail-in ballot access, Voter work protections for in-person voting."),
     ("gov-07", 1, V411_NJ2("Mora backs ranked-choice voting"), "Rank-Choice Voting would be a system I back"))
V411_NJ3 = V411(68198480)
cand("NJ-H-03", "NJ-H-03:kelly", "Ryan Kelly", "I", "Worked nearly 13 years in civil-rights and civil-liberties oversight at the Department of Homeland Security.",
     ("hea-01", 2, V411_NJ3("Kelly supports a universal single-payer health system"), "I support a universal single-payer healthcare system that includes medical, prescription, mental health, and preventive care."),
     ("imm-08", -2, V411_NJ3("Kelly would abolish ICE and replace it with accountable institutions"), "I support abolishing ICE and replacing it with accountable institutions focused on legitimate public-safety and immigration functions"),
     ("imm-02", 1, V411_NJ3("Kelly supports paths to legal status and citizenship"), "providing workable paths to legal status and citizenship"),
     ("imm-06", 1, V411_NJ3("Kelly would protect asylum, refugee and TPS programs"), "I support protecting asylum, refugee and TPS programs"),
     ("def-04", 1, V411_NJ3("Kelly says Congress must reclaim its war powers"), "Congress must protect constitutional rights, reclaim its responsibility over war powers"),
     ("eco-09", 1, V411_NJ3("Kelly supports collective bargaining"), "I support raising wages, protecting collective bargaining"),
     ("hea-08", 1, V411_NJ3("Kelly would protect people with preexisting conditions"), "protect people with preexisting conditions"),
     ("hea-06", 1, V411_NJ3("Kelly would expand community mental health services"), "expand community-based mental health services"),
     ("ene-08", 1, V411_NJ3("Kelly would invest in flood mitigation and emergency preparedness"), "I support investing in flood mitigation, stormwater systems, resilient roads and bridges, the electric grid, emergency preparedness"),
     ("gov-06", 1, V411_NJ3("Kelly supports early and mail voting"), "I support strong voting-rights protections, accessible registration and voting, early and mail voting"),
     ("gov-03", 1, V411_NJ3("Kelly supports campaign-finance transparency"), "I also support campaign-finance transparency and reducing the influence of concentrated special-interest money."),
     ("gov-11", 1, V411_NJ3("Kelly would reduce the influence of special-interest money"), None),
     ("ene-01", 1, V411_NJ3("Kelly would accelerate clean energy"), "I also support accelerating clean energy while protecting consumers and workers during the transition."),
     officialSite="https://www.kellyfornj03.com/")
V411_NJ8 = V411(68198485)
cand("NJ-H-08", "NJ-H-08:honts", "Craig Honts", "Socialist Workers", None,
     ("def-08", -2, V411_NJ8("Honts wants U.S. troops out of the Middle East"), "US troops out of the Middle East!"),
     ("eco-06", 1, V411_NJ8("Honts calls for a public works program to build hospitals, childcare centers and infrastructure"), "We call for a public works program to provide jobs at union-scale wages to build hospitals, childcare centers and other infrastructure."),
     ("eco-13", 2, V411_NJ8("Honts calls for a shorter workweek with no cut in pay"), "We call for a shorter workweek with no cut in pay, with regular hours."),
     ("eco-09", 1, V411_NJ8("Honts builds solidarity with unions on strike"), "The Socialist Workers Party calls on fellow workers to join us at strike picket lines and to build solidarity with unions"),
     ("imm-02", 2, V411_NJ8("Honts calls for amnesty for all workers without papers"), "A union-led fight for amnesty for all workers in the US without papers is needed to unify the working class."),
     ("imm-08", -2, V411_NJ8("Honts opposes ICE raids and deportations"), "The SWP opposes raids, deportations and brutal treatment of immigrant workers at the hands of ICE agents."),
     ("soc-03", 2, V411_NJ8("Honts supports decriminalizing abortion"), "The Socialist Workers Party unconditionally supports the decriminalization of abortion and joins others in fighting for it."),
     ("ene-02", 1, V411_NJ8("Honts supports nuclear power under workers’ control"), "Nuclear power, which produces no greenhouse gas emissions, could solve this and improve lives, provided it is run under workers control"))
cand("NJ-H-08", "NJ-H-08:hughey", "Da'Shone Hughey", "I", "Running on the We the People line; takes no PAC, AIPAC or special-interest money.",
     ("hou-03", 1, V411_NJ8("Hughey would strengthen public transportation"), "strengthen public transportation"),
     ("edu-03", 1, V411_NJ8("Hughey would expand AI, robotics, advanced manufacturing and skilled-trade education"), "expanding access to AI, robotics, advanced manufacturing, and skilled-trade education"),
     ("hea-06", 1, V411_NJ8("Hughey wants greater access to mental health care"), "We need greater access to counseling, crisis services, and community-based care"),
     ("hea-09", 1, V411_NJ8("Hughey would expand affordable primary and preventive care"), "expand access to affordable primary and preventive care"),
     ("imm-01", 1, V411_NJ8("Hughey wants stronger border security"), "We need stronger border security, a faster and more efficient legal immigration process"),
     ("imm-02", 1, V411_NJ8("Hughey supports a path forward for immigrants who have built their lives here"), "a practical path forward for people who have built their lives in America and contribute to our communities"),
     ("soc-03", 1, V411_NJ8("Hughey says abortion decisions belong to a woman and her doctor"), "I believe reproductive healthcare decisions should remain between a woman and her doctor, without unnecessary government interference."),
     ("gov-06", 2, V411_NJ8("Hughey would fight for early voting, no-excuse mail voting and paid time to vote"), "Early voting, no-excuse mail voting, and paid time to vote"),
     ("gov-04", 1, V411_NJ8("Hughey supports independent redistricting"), "Independent redistricting to end partisan gerrymandering"),
     ("ene-08", 1, V411_NJ8("Hughey would invest in flood protection and resilient infrastructure"), "I would support federal investment in resilient infrastructure, including stronger stormwater systems, upgraded power grids, flood protection"),
     ("gov-11", 1, V411_NJ8("Hughey would end PAC and dark-money influence"), "An end to PAC and dark-money influence over election administration"),
     officialSite="https://votedashonehughey.com/")

# Texas in VOTE411 (the League of Women Voters of Texas's local guides), read Oct. 27.
# Ronald Whitfield (R, 18th), Ben Mendoza (I, 23rd, in both local guides) and Phil Gray
# (L, 26th) left every question blank, and Nevada's Bobby Khan, Russell Best and William
# Johnson and Oklahoma's Sevier White, Orlando Bush, Rocco Bonacci and Austin Nieves did
# the same in their states' guides.
V411_TX8 = V411(71560477)
cand("TX-H-08", "TX-H-08:jones", "Laura Jones", "D", None,
     ("eco-03", 1, V411_TX8("Jones will fight for a living wage"), "I'll fight for a living wage, so a full-time job actually covers the basics"),
     ("eco-04", 1, V411_TX8("Jones would push back on price gouging and support competition"), "I'll push back on price gouging and support more competition to keep food prices honest."),
     ("soc-07", 1, V411_TX8("Jones would back tax credits and investment to make child care affordable"), "I'll back tax credits and real investment to make childcare affordable"),
     ("hou-04", 1, V411_TX8("Jones would cut the red tape that slows home building"), "I'll support building more homes and cutting the red tape that slows construction and drives up costs."),
     ("imm-08", -1, V411_TX8("Jones opposes current immigration enforcement and detention policies"), "I oppose current federal immigration enforcement and detention policies."),
     ("gov-06", 2, V411_TX8("Jones would expand mail-in and early voting and back same-day registration"), "I support expanding mail-in and early voting options, since they make voting easier for working families, seniors, and people with disabilities"),
     ("ene-08", 1, V411_TX8("Jones would fund flood mitigation"), "Flood mitigation third — preventing flood damage costs far less than cleaning up after a disaster."),
     ("hou-08", 1, V411_TX8("Jones would repair roads and bridges before building new projects"), "Transportation second — repair our roads, bridges, and transit before building new projects."),
     officialSite="https://www.laura4tx.com/")
V411_TX34 = V411(69005953)
cand("TX-H-34", "TX-H-34:espinoza", "Eddie Espinoza", "G", "Army combat veteran, retired elementary school teacher and climate and peace activist; takes no PAC money.",
     ("gov-11", 2, V411_TX34("Espinoza wants a constitutional amendment to end Citizens United"), "We need a Constitutional Amendment to end Citizens United and rein in PACs, dark money, and billionaires."),
     ("gov-13", -2, V411_TX34("Espinoza would end Citizens United"), None),
     ("imm-08", -2, V411_TX34("Espinoza would abolish ICE and DHS"), "Abolish ICE. Abolish DHS."),
     ("hea-01", 2, V411_TX34("Espinoza supports Medicare for All"), "We need Medicare for All!"),
     ("hea-10", 2, V411_TX34("Espinoza wants Medicare to include dental, vision and hearing aids"), "With prescriptions, dental, vision, hearing aids, and mental health included."),
     ("edu-02", 1, V411_TX34("Espinoza supports free college"), "We could have Medicare for All, Free College, and so much more."),
     ("ene-01", 2, V411_TX34("Espinoza wants a transition to 100% clean renewable energy"), "Climate scientists agree: we must transition to 100% clean renewable energy."),
     ("ene-03", -2, V411_TX34("Espinoza would cancel the Port of Brownsville refinery and LNG export terminals"), "The new refinery and the new export LNG terminals at the Port of Brownsville must be canceled."),
     officialSite="https://espinoza4tx.com/")

# Florida in VOTE411 (League of Women Voters of Florida), read Oct. 27. Jeffrey Datto
# (governor) and Peter Jassenoff (L, 25th) left every question blank. Victor Arias now
# campaigns at ariasforcongress.us; Michael Gist's listed site still answers 404.
V411_FL26 = V411(71841240)
cand("FL-H-26", "FL-H-26:hosey", "Deborah Ann Meidinger Hosey", "I", "Weston resident with a master’s degree in educational leadership from the University of South Florida.",
     ("imm-02", 2, V411_FL26("Hosey would restore TPS and DACA and protect Dreamers permanently"), "TPS and DACA must be restored and expanded, and Dreamers must have permanent protection and access to education."),
     ("imm-07", 1, V411_FL26("Hosey would focus a smaller enforcement agency on serious criminals"), "modernize enforcement by transitioning from ICE to a smaller, accountable system focused on serious criminals"),
     ("imm-08", -1, V411_FL26("Hosey would replace ICE with a smaller agency"), None),
     ("hea-01", 1, V411_FL26("Hosey supports universal health care"), "I also support universal healthcare to reduce premiums, lower prescription costs"),
     ("hou-01", 1, V411_FL26("Hosey would expand housing tax credits and Section 8 vouchers"), "expands tax credits for multigenerational and workforce housing, increases Section 8 and VASH vouchers"),
     ("edu-09", 1, V411_FL26("Hosey would reinstate universal school breakfast and lunch"), "reinstates universal school breakfast and lunch"),
     ("soc-07", 1, V411_FL26("Hosey would expand childcare assistance and Head Start"), "affordable childcare and early learning through expanded childcare assistance, Head Start, Early Head Start"),
     ("soc-01", 1, V411_FL26("Hosey calls free speech one of America’s most essential rights"), "Freedom of speech, protected by the First Amendment, is one of America’s most essential rights."),
     ("edu-01", 1, V411_FL26("Hosey would fully fund special education"), "fully fund IDEA, and expand school breakfast and lunch programs"),
     officialSite="https://deborahforcongress.com/")
V411_FL6 = V411(71841180)
more("FL-H-06", "FL-H-06:gist",
     ("imm-02", -2, V411_FL6("Gist says those here illegally should return home and apply the right way"), "If you want citizenship, return home and apply the right way."),
     ("ene-10", 1, V411_FL6("Gist says climate change is no reason to keep raising power bills"), "I do not believe “climate change” is a reason to keep raising bills."),
     ("soc-01", 2, V411_FL6("Gist says free speech covers unpopular speech and speech that challenges power"), "including speech that is unpopular and speech that challenges people in power"),
     ("edu-06", 1, V411_FL6("Gist wants federal school dollars to follow the student"), "K-12 federal dollars should follow the student through Freedom Accounts"),
     ("edu-07", 1, V411_FL6("Gist says education is a state and local job"), "Education is a state and local job, not a federal one."),
     ("eco-07", 1, V411_FL6("Gist would vote against more debt"), "Vote for affordability, legal immigration, reliable energy, and against more debt that raises prices."),
     ("agr-03", 1, V411_FL6("Gist wants more production in the U.S."), "More production in the USA not abroad."))
V411_FL19 = V411(71841219)
more("FL-H-19", "FL-H-19:arias",
     ("imm-02", 1, V411_FL19("Arias would give long-term residents who pass background checks a fair legal status"), "Establish a fair legal status for long-term residents who pass background checks, pay taxes, and live by the rules to protect the labor market."),
     ("imm-01", 1, V411_FL19("Arias supports technologically advanced border security"), "I support smart, technologically advanced border security measures alongside an increase in the number of immigration judges, asylum officers, and border personnel."),
     ("imm-04", 1, V411_FL19("Arias would add immigration judges and asylum officers"), None),
     ("ene-01", 1, V411_FL19("Arias wants the U.S. to lead in clean energy technology"), "We must approach this as an opportunity to lead the world in clean energy technology."),
     ("ene-08", 1, V411_FL19("Arias would secure funding to fortify infrastructure against severe weather"), "fortify our infrastructure against severe weather. I will work across the aisle to secure funding."),
     ("soc-01", 1, V411_FL19("Arias calls free speech the bedrock of American democracy"), "I view Freedom of Speech as a constitutional mandate and the bedrock of American democracy!"),
     ("edu-07", 1, V411_FL19("Arias says education decisions belong close to home"), "Education is most effective when decisions are made closest to home by parents, teachers, and local school administrators."),
     bio="Fort Myers attorney who has practiced law in Florida for 35 years.",
     officialSite="https://ariasforcongress.us/")

# New York in VOTE411 (League of Women Voters of New York State), read Oct. 27. Lewis
# Mizrahi (8th), Joel Azumah (9th), Stylo Sapaskis and Gonzalo Duran (15th) left every
# question blank.
V411_NY12 = V411(26978858)
cand("NY-H-12", "NY-H-12:negron", "Wilneida Negron", "I",
     "Labor and technology policy specialist who has advised two presidential administrations; Upper West Side public school parent with a Ph.D. from the CUNY Graduate Center. On the ballot as For All of Us.",
     ("soc-07", 1, V411_NY12("Negron would pass a refundable Family Care Credit for child and elder care"), "I'll pass a refundable Family Care Credit for child and elder care"),
     ("eco-02", 1, V411_NY12("Negron would make the Child Tax Credit fully refundable"), "a fully refundable Child Tax Credit, which cut child poverty nearly in half in 2021"),
     ("gov-02", 2, V411_NY12("Negron would ban congressional stock trading"), "I'll ban congressional stock trading, force dark money disclosure, protect inspectors general, and restore independent federal data."),
     ("gov-03", 1, V411_NY12("Negron would force dark money disclosure"), None),
     ("edu-02", 1, V411_NY12("Negron backs tuition-free community college retraining"), "tuition-free community college retraining"),
     ("gov-04", 2, V411_NY12("Negron would ban partisan gerrymandering through independent commissions"), "ban partisan gerrymandering nationwide through independent redistricting commissions"),
     ("ene-08", 1, V411_NY12("Negron would fund flood protection and grid upgrades"), "I will push to fund flood protection, cooling, and grid upgrades in vulnerable neighborhoods"),
     ("ene-09", 1, V411_NY12("Negron would rebuild domestic battery and clean energy manufacturing"), "rebuild American manufacturing of batteries and clean energy components"),
     ("def-02", 1, V411_NY12("Negron would keep U.S. commitments to NATO"), "We should keep our commitments, and expect allies to pay their fair share."),
     ("def-04", 2, V411_NY12("Negron says no war without a vote of Congress"), "No war without a vote of Congress, no arms transfers without real review"),
     ("gov-11", 1, V411_NY12("Negron wants elections to answer to voters, not the biggest spenders"), "The federal government's job is to make sure elections answer to voters, not to whoever spends the most."),
     officialSite="https://www.wilneidany12.com/")

# California in VOTE411 (League of Women Voters of California), read Oct. 27. Peter
# Soulé (16th), Joe Males (25th), Sam Gallucci (26th), Eric Ching (31st), Hilda Solis
# (38th), Steve Manos (39th), Jenny Le Roux (47th), Steve Cohen (50th), Robb Tucker (3rd),
# Mai Vang (7th), Rudy Recile (8th), Kyle Kirkland (21st), Tessa Lynn Hodge (23rd), Jason
# Gibbs (27th), Houston Brignano (36th), Samantha Mota (37th) and Mitch Clemmons (41st)
# answered no questions, though several list campaign sites the other sources lacked.
V411_CA17 = V411(6388242)
cand("CA-H-17", "CA-H-17:tandon", "Ritesh Tandon", "R",
     "Engineer and Bay Area business leader for 26 years and a research fellow at UC Berkeley’s Haas School of Business; won Tandon v. Newsom (2021) at the U.S. Supreme Court.",
     ("eco-02", 1, V411_CA17("Tandon would lower taxes on working families"), "Lower taxes on working families, simplify the tax code, back small business"),
     ("edu-06", 1, V411_CA17("Tandon would fund the child, not the bureaucracy"), "Fund the child, not the bureaucracy."),
     ("gov-05", 1, V411_CA17("Tandon supports voter ID and citizenship verification"), "Only U.S. citizens should decide American elections — support Voter ID and citizenship verification."),
     ("gov-02", 2, V411_CA17("Tandon would end congressional stock trading"), "end Congressional stock trading"),
     ("imm-01", 2, V411_CA17("Tandon would fully fund border security and targeted barriers"), "Fully fund modern border security, targeted physical barriers where needed, and anti-cartel operations"),
     ("imm-04", 1, V411_CA17("Tandon would expand immigration courts"), "set fast adjudication timelines and expand immigration courts"),
     ("imm-03", 1, V411_CA17("Tandon supports merit-based pathways for high-skill immigrants"), "Modernize merit-based pathways for high-skill talent in critical sectors, with wage safeguards that protect American workers."),
     ("imm-07", 1, V411_CA17("Tandon would prioritize removing public-safety threats"), "Prioritize removal of public-safety threats"),
     ("gov-03", 2, V411_CA17("Tandon wants full, timely disclosure of donors to campaigns and super PACs"), "Full, timely disclosure of donors to candidates, parties, PACs, and Super-PACs"),
     ("gov-01", 1, V411_CA17("Tandon supports 8-year term limits"), "No stock trading by members of Congress, real-time financial disclosure, and 8-year term limits"),
     ("soc-06", 2, V411_CA17("Tandon won a Supreme Court religious liberty case against Gov. Newsom"), "In 2021, I stood up to Governor Newsom and won a landmark 5–4 ruling at the U.S. Supreme Court"),
     officialSite="https://www.tandonforcongress.com/")
V411_CA29 = V411(6388680)
cand("CA-H-29", "CA-H-29:duenas", "Angelica Dueñas", "D", "Working-class mother of five and community organizer from Sun Valley who won a seat on her neighborhood council; running for the seat for the third time.",
     ("imm-08", -2, V411_CA29("Dueñas would abolish ICE"), "This needs to stop, we need to abolish ICE, and make sure that our communities aren’t terrorized ever again."),
     ("hou-02", 2, V411_CA29("Dueñas wants a national ban on Wall Street buying rental property"), "We need a national ban on Wall Street buying rental property"),
     ("hea-01", 2, V411_CA29("Dueñas is an adamant supporter of Medicare for All"), "This is why I’m an adamant supporter of health policy like Medicare For All"),
     ("ene-04", 1, V411_CA29("Dueñas supports environmental justice laws and California’s environmental review law"), None),
     ("imm-02", 1, V411_CA29("Dueñas wants reform that makes it easier to become a citizen"), "We need comprehensive immigration reform that makes it easier for people to become citizens"),
     ("gov-11", 2, V411_CA29("Dueñas would overturn Citizens United"), "This is why I support overturning Citizen’s United."),
     ("gov-13", -2, V411_CA29("Dueñas would overturn Citizens United"), None),
     ("gov-03", 1, V411_CA29("Dueñas supports real-time reporting of super PAC donors"), "I support real time reporting of all SuperPAC donors"),
     ("eco-06", 1, V411_CA29("Dueñas would invest in public infrastructure such as water pipes"), "pass a public infrastructure investment to update our pipes across the country"),
     officialSite="https://angelica4congress.com/")
V411_CA2 = V411(6388620)
more("CA-H-02", "CA-H-02:littau",
     ("edu-06", 2, V411_CA2("Littau fully supports school choice"), "I am in full support of school choice."),
     ("agr-01", 1, V411_CA2("Littau says farmers need federal and state support"), "Farmers desperately need Federal and State support to increase farming production"),
     ("eco-02", 1, V411_CA2("Littau would cut burdensome taxes"), "by decreasing burdensome taxation and hindering legislation"))
V411_CA5 = V411(6387748)
more("CA-H-05", "CA-H-05:masuda",
     ("hea-06", 1, V411_CA5("Masuda would expand mental health services and rural hospital funding"), "I will fight for rural hospital funding, expanded telehealth and maternal care, and better access to mental health services"),
     ("imm-02", 1, V411_CA5("Masuda supports a path to citizenship for Dreamers"), "I support keeping families together and giving Dreamers and DACA recipients a clear path to citizenship."),
     ("imm-04", 1, V411_CA5("Masuda would fund more immigration judges"), "I will also support better funding for our immigration courts so we can hire more judges to get through backlogs of asylum claims."),
     ("imm-01", 1, V411_CA5("Masuda would fund smarter border security"), "I will support funding for smarter border security"),
     ("gov-02", 2, V411_CA5("Masuda would co-sponsor a ban on congressional stock trading"), "I will co-sponsor measures to ban congressional stock trading."),
     ("gov-03", 2, V411_CA5("Masuda would co-sponsor the DISCLOSE Act"), "In Congress, I will co-sponsor the DISCLOSE Act to ensure Super-PACs must publicly disclose donors."),
     ("gov-09", 1, V411_CA5("Masuda backs a five-year lobbying ban for former members"), "This includes a ban on stock trading, ending Citizens United and big money in campaigns, a 5-year ban on lobbying in Congress after leaving office"),
     ("gov-11", 1, V411_CA5("Masuda would end Citizens United and big money in campaigns"), None),
     ("gov-01", 1, V411_CA5("Masuda supports congressional term limits"), "an enforceable judicial code of ethics, and congressional term limits"),
     bio="Engineer who worked on military defense systems at the Johns Hopkins Applied Physics Laboratory and as a foreign affairs officer at the State Department.")
V411_CA6 = V411(6388374)
cand("CA-H-06", "CA-H-06:pan", "Richard Pan", "D", None,
     ("eco-10", -1, V411_CA6("Pan would oppose Trump’s tariffs"), "I will oppose Trump’s chaotic tariffs and unconstitutional wars increasing the cost of gas, food, and housing"),
     ("def-15", -1, V411_CA6("Pan calls the wars unconstitutional"), None),
     ("eco-03", 1, V411_CA6("Pan voted to raise California’s minimum wage"), "I voted to increase the minimum wage."),
     ("hea-08", 2, V411_CA6("Pan wrote California’s ban on discrimination against patients with pre-existing conditions"), "I authored the state ban on discriminating against patients with pre-existing health conditions"),
     ("hea-05", 1, V411_CA6("Pan would support medical research"), "advancing legislation to achieve universal health care and support medical research"),
     ("imm-02", 1, V411_CA6("Pan supports an expedited path to legal status for Dreamers and long-term residents"), "Dreamers and long-term undocumented immigrants who are part of our communities should have an expedited path to permanent legal status."),
     ("gov-11", 1, V411_CA6("Pan would overturn Citizens United"), "I support comprehensive campaign finance reform, including overturning Citizens United through a constitutional amendment or other legal reforms"),
     ("gov-13", -1, V411_CA6("Pan would overturn Citizens United"), None),
     ("gov-03", 1, V411_CA6("Pan would require disclosure of all donors, including to super PACs"), "I would support legislation requiring disclosure of all donors to political campaigns and outside spending groups"),
     ("def-04", 1, V411_CA6("Pan wants Congress to assert its authority over war"), "I will demand Congress assert its constitutional authority over taxation, war, and appropriation."),
     ("ene-04", 1, V411_CA6("Pan would strengthen and enforce federal clean water standards"), "federal clean water standards need to be strengthened and enforced so people have access to clean water"),
     ("ene-08", 1, V411_CA6("Pan would invest in flood protection and levees"), "I will support increased federal investment in water infrastructure, including flood protection, levee improvements, and water storage."),
     ("soc-03", 2, V411_CA6("Pan voted to enshrine reproductive rights in California’s constitution"), "I voted to enshrine reproductive and LGBTQ+ rights in California’s Constitution"),
     ("soc-10", 1, V411_CA6("Pan voted to enshrine LGBTQ+ rights in California’s constitution"), None))
V411_CA42 = V411(6388739)
more("CA-H-42", "CA-H-42:burley",
     ("ene-03", 1, V411_CA42("Burley supports expanding domestic energy production"), "I also support expanding domestic energy production to help bring prices down."),
     ("imm-08", 1, V411_CA42("Burley would increase immigration enforcement resources"), "I support policies that secure the border, increase enforcement resources and restore order to the immigration system."),
     ("imm-01", 1, V411_CA42("Burley supports more border staffing, technology and infrastructure"), "I support increased staffing, technology and infrastructure to stop illegal crossings and disrupt trafficking of drugs and people."),
     ("gov-03", 1, V411_CA42("Burley would require timely disclosure of large donors"), "I would back legislation requiring timely public disclosure of donors while protecting small dollar contributors’ privacy."))
V411_CA51 = V411(6388160)
more("CA-H-51", "CA-H-51:cabrera",
     ("eco-07", 1, V411_CA51("Cabrera would cut wasteful spending"), "I will push for pro-growth policies that cut wasteful spending, reduce red tape"),
     ("imm-01", 2, V411_CA51("Cabrera would finish physical barriers and add border personnel"), "Secure the border first — Finish physical barriers, increase technology and personnel, and end catch-and-release policies."),
     ("imm-10", 2, V411_CA51("Cabrera wants mandatory E-Verify nationwide"), "Mandatory E-Verify nationwide, swift deportation of illegal immigrants, and an end to sanctuary policies that protect lawbreakers."),
     ("imm-02", -2, V411_CA51("Cabrera supports swift deportation of immigrants here illegally"), None),
     ("imm-03", 1, V411_CA51("Cabrera wants a merit-based legal immigration system"), "Shift to a merit-based system that prioritizes skills, education, and self-sufficiency"),
     ("gov-03", 2, V411_CA51("Cabrera strongly supports real-time disclosure of every donor"), "I strongly support legislation that requires complete, real-time transparency for every donor to political campaigns and Super PACs."),
     bio="San Diego small business owner and cybersecurity professional.")
V411_CA14 = V411(6389079)
more("CA-H-14", "CA-H-14:hernandez",
     ("hou-05", 1, V411_CA14("Hernandez would make home loans easier for first-time buyers"), "making it easier for first-time homebuyers to get a home loan"),
     ("hou-01", 1, V411_CA14("Hernandez would provide incentives to build housing"), "providing incentives to build new housing"),
     ("hea-07", 1, V411_CA14("Hernandez would restore insurance premium subsidies"), "restore insurance subsidies to reduce the cost of insurance premiums"),
     ("hea-09", 1, V411_CA14("Hernandez would prioritize preventive care"), "I will prioritize patient health and preventative care"),
     ("soc-03", 1, V411_CA14("Hernandez would restore reproductive freedom"), "I will also fight to protect reproductive healthcare and restore reproductive freedom."),
     ("soc-07", 1, V411_CA14("Hernandez would expand the Child Tax Credit and pay childcare workers more"), "I support expanding the Child Tax Credit, recruiting and training qualified childcare workers, and paying them more."),
     ("eco-02", 1, V411_CA14("Hernandez would expand the Child Tax Credit"), None),
     ("eco-11", 1, V411_CA14("Hernandez supports paid family and medical leave"), "I also support Paid and Family Medical Leave."),
     ("imm-07", 1, V411_CA14("Hernandez supports deporting criminals"), "I support deporting criminals."),
     ("imm-02", 1, V411_CA14("Hernandez supports a path to citizenship for Dreamers"), "I support giving a pathway to citizenship for DREAMERS."),
     ("imm-01", 1, V411_CA14("Hernandez supports strong border protections"), "I support strong border protections."),
     ("gov-03", 1, V411_CA14("Hernandez supports the DISCLOSE Act"), "I support the Disclose Act, a campaign finance transparency bill"),
     ("gov-11", 1, V411_CA14("Hernandez supports an amendment to overturn Citizens United"), "And, I support a constitutional amendment to overturn Citizens United."),
     officialSite="https://melissahernandez2026.com/")
SOULE = site("Peter Soulé", "https://souleforcongress.com/issues", READ27)
cand("CA-H-16", "CA-H-16:soule", "Peter Soulé", "R",
     "Worked in the family business, Soule Steel, in San Francisco and Los Angeles; served on the San Jose Civil Service Commission from 2007 to 2011.",
     ("imm-07", 1, SOULE("Soulé would withhold federal money from sanctuary cities that block deporting criminals"), "Withholding Federal dollars going to cities who enforce sanctuary city policies that prevent the deportation of criminals who are here illegally."),
     ("ene-03", 1, SOULE("Soulé would remove restrictions on drilling and refineries in California"), "Make energy more affordable by removing restrictions on drilling for oil and building refineries in California."),
     ("hou-02", 1, SOULE("Soulé would ban large financial institutions from buying single-family homes"), "Banning large financial institutions from buying single-family homes"),
     ("imm-03", -1, SOULE("Soulé would reform H-1B visas to favor hiring Americans"), "Reforming the HB-1 Visa program to favor the hiring of Americans over foreigners."),
     ("def-16", 1, SOULE("Soulé would bar China from buying farmland near military bases"), "Restricting Red China from buying American farmland near our military bases."),
     ("hou-07", -1, SOULE("Soulé backs defunding California’s high-speed rail project"), "End waste, fraud and abuse such as Congressman Kiely modeled when he introduced a bill in January to DEFUND the High-Speed Rail Project"),
     ("eco-07", 1, SOULE("Soulé would cut wasteful spending"), "California’s economy is being strangled by excessive regulations and wasteful spending."),
     ("edu-06", 1, SOULE("Soulé would let parents send children to the school of their choice"), "Enact Federal policies to protect parental rights and enable parents to send their children to their school of choice."),
     ("edu-03", 1, SOULE("Soulé would give all children chances at vocational training"), "Provide opportunities for all children to explore vocational training."),
     officialSite="https://souleforcongress.com/")
MANOS = site("Steve Manos", "https://www.manosforcongress.com/", READ27)
cand("CA-H-39", "CA-H-39:manos", "Steve Manos", "R",
     "Lake Elsinore City Council member since 2012 and four-time mayor; business owner since 1996 and past president of the Inland Valleys Association of Realtors.",
     ("hou-04", 1, MANOS("Manos would remove regulatory barriers that raise housing costs"), "remove the regulatory barriers that increase the cost of housing and basic needs"),
     ("hou-08", 1, MANOS("Manos would fund repairs on the 215 freeway"), "We must immediately fund freeway repairs along the 215 freeway"),
     officialSite="https://www.manosforcongress.com/")

# California campaign sites that turned up in VOTE411 and render only in a browser, read
# in the browser pane on Oct. 27; quotes were checked against the live pages. Sam
# Gallucci's issues open as pop-ups from his home page.
CHING = site("Eric Ching", "https://www.ericchingforcongress.com/", READ27)
cand("CA-H-31", "CA-H-31:ching", "Eric Ching", "R",
     "Former mayor of Walnut, elected to the city council in 2012, 2016 and 2020; business owner for 30 years.",
     ("soc-01", 1, CHING("Ching would protect freedom of religion, speech and the press"), "I will support our rights to the freedom of religion, freedom of speech, freedom of the press"),
     ("soc-06", 1, CHING("Ching would protect freedom of religion"), None),
     ("imm-01", 1, CHING("Ching would secure the border against illegal movement of weapons, drugs and people"), "supporting ways to best secure our border from the illegal movement of weapons, drugs, contraband, and people"),
     ("gov-01", 1, CHING("Ching supports term limits"), "I will support term limits for federal, state, and local officials."),
     ("hea-06", 1, CHING("Ching would encourage treatment centers for substance abuse"), "I will support legislation to encourage various treatment centers to help victims with substance abuse"),
     ("edu-06", 1, CHING("Ching supports school choice"), "I support school choice, and I will empower parents to use their ability to decide which schools are best for their kids."),
     officialSite="https://www.ericchingforcongress.com/")
cand("CA-H-47", "CA-H-47:roux", "Jenny Le Roux", "R",
     "Executive director of CAL DOGE, which audits California state spending; co-built companies in energy and financial services and ran a tech-enabled services firm.",
     ("eco-07", 1, site("Jenny Rae Le Roux", "https://jennyraeca.com/", READ27)("Le Roux would cut the waste that drives up the cost of living"), "cutting the waste that's driving up the cost of living here"),
     officialSite="https://jennyraeca.com/")
GALLUCCI = site("Sam Gallucci", "https://www.samgallucci.com/#issues", READ27)
cand("CA-H-26", "CA-H-26:gallucci", "Sam Gallucci", "R",
     "Business executive and pastor who led Embrace! Church and founded four nonprofits that feed and house people in need.",
     ("ene-03", 1, GALLUCCI("Gallucci would unleash American energy and streamline permits for domestic production"), "Unleash American energy to lower utility bills; streamline permits for domestic production and grid upgrades."),
     ("hou-04", 1, GALLUCCI("Gallucci would streamline regulations that delay homebuilding"), "Incentivize homebuilding near jobs and transit; streamline federal regulations that delay and inflate construction costs."),
     ("eco-07", 1, GALLUCCI("Gallucci would rein in wasteful spending while defending SNAP"), "Responsibly rein in wasteful spending that fuels inflation while uncompromisingly defending SNAP and other critical social services."),
     ("eco-08", 1, GALLUCCI("Gallucci supports small-business tax relief"), "Support small-business tax relief and deregulation that lowers prices and keeps jobs local."),
     ("gov-02", 2, GALLUCCI("Gallucci would ban stock trading by members of Congress"), "Ban stock trading by members of Congress."),
     ("soc-12", -1, GALLUCCI("Gallucci would use federal funding against groups that let transgender women compete in women’s sports"), "PROTECT women's sports by leveraging federal funding against groups that allow biological males to participate in women's events."),
     ("imm-07", 2, GALLUCCI("Gallucci would fund the mass removal of criminal immigrants"), "Support and fund the mass removal of criminal illegal aliens."),
     ("imm-08", 1, GALLUCCI("Gallucci would fund removals"), None),
     ("imm-09", 1, GALLUCCI("Gallucci would streamline work permits in fields with labor shortages"), "Streamline work permitting in fields with labor shortages so employers can fill needed jobs."),
     ("agr-03", 1, GALLUCCI("Gallucci would incentivize domestic manufacturing"), "Incentivize domestic manufacturing and job creation—especially with critical minerals, semiconductors, and defense supply chains."),
     ("agr-02", 1, GALLUCCI("Gallucci would incentivize semiconductor manufacturing"), None),
     ("agr-05", 1, GALLUCCI("Gallucci would incentivize critical mineral supply chains"), None),
     ("def-03", 1, GALLUCCI("Gallucci would cut VA wait times and expand veterans’ mental health care"), "Cut VA wait times with 'care where you are' access and expand mental-health support."),
     ("cri-01", 1, GALLUCCI("Gallucci would increase resources for local policing"), "Increase resources for local policing, fentanyl interdiction, and gang task forces."),
     ("cri-06", -2, GALLUCCI("Gallucci would ban cashless bail"), "END the instant release of career violent criminals by banning cashless bail."),
     ("cri-05", 1, GALLUCCI("Gallucci would expand drug courts and reentry programs"), "Expand evidence-backed solutions like drug courts and reentry programs tied to work and mentorship."),
     ("cri-08", 1, GALLUCCI("Gallucci would expand drug courts"), None),
     ("hea-02", 1, GALLUCCI("Gallucci would lower drug prices with most-favored-nation pricing"), "Drastically lower prescription costs by giving direct-to-consumer and most-favoured-nation pricing alternatives."),
     ("eco-02", 1, GALLUCCI("Gallucci would expand child tax credits"), "Reduce the barriers to starting a family by expanding child tax credits."),
     ("ene-08", 1, GALLUCCI("Gallucci would invest in wildfire fuel reduction"), "Invest in wildfire fuel reduction, forest management, and resilient power infrastructure."),
     ("hea-06", 1, GALLUCCI("Gallucci would fund mental health care and detox for homeless people"), "Fund recover-to-work models: detox, mental-health care, transitional housing, and job placement."),
     officialSite="https://www.samgallucci.com/")

# More Texas answers in VOTE411 (read Oct. 27) for candidates whose sites gave nothing
# to map; Frederick Haynes III (30th) left every question blank.
V411_TX10 = V411(6436415)
more("TX-H-10", "TX-H-10:rourk",
     ("hea-07", 1, V411_TX10("Rourk would protect and strengthen the Affordable Care Act"), "Congress should protect and strengthen the Affordable Care Act"),
     ("imm-01", 1, V411_TX10("Rourk would secure the border and invest in ports of entry"), "securing the border, investing in technology and ports of entry"),
     ("imm-04", 1, V411_TX10("Rourk would add asylum officers and judges"), "adding asylum officers and judges"),
     ("imm-03", 1, V411_TX10("Rourk would expand legal immigration pathways"), "expanding legal pathways"),
     ("imm-02", 1, V411_TX10("Rourk supports an earned path for Dreamers and long-term residents"), "providing an earned path for Dreamers and long-term residents"),
     ("soc-07", 1, V411_TX10("Rourk would expand the supply of child care"), "I’ll tackle the underlying costs by building more housing, expanding childcare supply"),
     ("gov-09", 1, V411_TX10("Rourk would protect inspectors general and strengthen safeguards against corruption"), "protecting independent inspectors general and whistleblowers, demanding transparency, and strengthening safeguards against corruption"))
V411_TX31 = V411(71558716)
more("TX-H-31", "TX-H-31:early",
     ("hea-03", 1, V411_TX31("Early wants a federal fallback for Medicaid coverage"), "ensuring coverage through a federal fallback for Medicaid and supporting community clinics"),
     ("hou-04", 1, V411_TX31("Early backs zoning reform"), "I'll back zoning reform to build more housing"),
     ("soc-07", 1, V411_TX31("Early would use tax credits to cap child care costs"), "push tax credits to cap childcare costs"),
     ("ene-03", 1, V411_TX31("Early would expand domestic energy production"), "expand domestic energy production to lower utility bills"),
     ("eco-04", 1, V411_TX31("Early supports antitrust enforcement against grocery price-fixing"), "support antitrust enforcement against price-fixing in groceries"),
     ("imm-02", 1, V411_TX31("Early would push for a clear pathway to citizenship"), "I'll push for a clear pathway to citizenship, end family separation and for-profit detention, protect Dreamers permanently"),
     ("def-04", 1, V411_TX31("Early would restore Congress’s war powers"), "I'll push to restore war powers and spending oversight"),
     ("gov-09", 1, V411_TX31("Early would protect inspectors general and whistleblowers"), "protect inspectors general from political removal, strengthen whistleblower protections"))
V411_TX33 = V411(25678627)
more("TX-H-33", "TX-H-33:allred",
     ("gov-06", 2, V411_TX33("Allred would guarantee the right to vote by mail"), "passing the Civil Rights Act of the 2020s to guarantee every American access to the ballot, including the right to vote by mail"),
     ("gov-04", 1, V411_TX33("Allred would end gerrymandering"), "It also means ending gerrymandering and getting big money out of politics."),
     ("gov-11", 1, V411_TX33("Allred would get big money out of politics"), None),
     ("gov-02", 2, V411_TX33("Allred would ban congressional stock trading"), "banning congressional stock trading and getting corporate PAC money out of our elections for good"),
     ("imm-08", -2, V411_TX33("Allred would abolish ICE and rebuild enforcement"), "We need to abolish ICE and rebuild enforcement around accountability and due process"),
     ("imm-02", 1, V411_TX33("Allred supports a pathway to citizenship"), "create a real pathway to citizenship, protect Dreamers and asylum seekers"),
     ("eco-10", -2, V411_TX33("Allred would repeal Trump’s tariffs"), "Congress must repeal Trump's tariffs, the largest tax hike on working families in modern history"),
     ("hea-02", 2, V411_TX33("Allred would let Medicare negotiate all drug prices"), "let Medicare negotiate all drug prices"),
     ("hou-01", 1, V411_TX33("Allred would expand the Low-Income Housing Tax Credit"), "I'll fight to expand the Low-Income Housing Tax Credit to spur construction of affordable housing"),
     ("hou-05", 1, V411_TX33("Allred would create a tax credit for first-time homebuyers"), "establish a refundable tax credit for first-time homebuyers"),
     ("ene-01", 1, V411_TX33("Allred would protect clean energy tax credits and restore renewables"), "protecting clean energy tax credits, restoring renewables, holding polluters accountable"),
     ("gov-09", 1, V411_TX33("Allred would pass ethics reform"), "I'll fight to ban congressional stock trading, get big money out of politics, and pass real ethics reform"))
cand("TX-H-34", "TX-H-34:royal", "Chris Royal", "L", "Attorney, teacher, author, programmer and Army veteran who helped run a family business.",
     ("eco-07", 1, V411_TX34("Royal ties economic opportunity to reducing the national debt"), "So until we see a decrease in the US debt, we will not be expanding economic opportunity for the lower working class."))

# More VOTE411 answers, read Oct. 27 (quotes checked against the page text). In these
# states' guides the following left every question blank: Joshua Ertle and Alaha Ahrar
# (VA-7), Brian Judd and Dean Roy (VT governor), Phoenix Altair and Ryan Walton (VT),
# Tom Bailey, Daniel Cavender (NC-1, NC-3) and Steven Swinton (NC-13), Paul Berry and
# Randy Langkraehr (MO-1, MO-5), Mary Sanders (CT-1), Bobby Wilson (AR-3), Jereme Peters
# (AZ-6), Don Coover (KS-2), Robert Burke (MA-8), George McDermott and Scott Collier
# (MD-4, MD-7), Johnny Baucom (MS-1), Nick Sheedy and Patrick McCracken (MT-1, MT-2) and
# Daniel Hartong (NE-1). Thomas Egan (CT-3) and James Sceniak (IN-7) aren't in their
# states' guides; Brendan Gomez's (ID-1) answers state no policies to map.
cand("VA-H-02", "VA-H-02:staten", "Geral Staten", "I", "Suffolk native who ran for mayor in 2016; an Amazon employee and public-address announcer for Kings Fork High School basketball.",
     ("hea-01", 1, V411(73042324)("Staten supports universal health care for all"), "Universal Healthcare For All."))
V411_VA8 = V411(73041026)
more("VA-H-08", "VA-H-08:sharman",
     ("imm-01", 1, V411_VA8("Sharman would fund border enforcement with strong oversight"), "Congress should provide the funding necessary for effective border enforcement, but that funding must come with strong oversight."),
     ("gov-11", 1, V411_VA8("Sharman opposes Citizens United"), "I oppose the Citizens United decision"),
     ("gov-13", -1, V411_VA8("Sharman would limit what corporations can spend on elections"), None),
     ("gov-03", 1, V411_VA8("Sharman wants more transparency about who funds political activity"), "together with much greater transparency about who is funding political activity"),
     ("eco-04", 1, V411_VA8("Sharman would look at excessive profits from non-competitive practices"), "look hard at areas of excessive corporate profits due to non-competitive practices"),
     bio="Immigrant from the United Kingdom.")
V411_VT = V411(72768506)
cand("VT-H-00", "VT-H-00:ortiz", "Adam Ortiz", "I", None,
     ("cri-05", 1, V411_VT("Ortiz would copy other states’ prison work-release programs"), "Work release is done in different States so just Copy and Paste what works."),
     ("def-07", 1, V411_VT("Ortiz says he can calm relations with Canada, Venezuela and Cuba"), "I can help calm things down with Canada Venezuela and Cuba."))
V411_NC5 = V411(20903487)
cand("NC-H-05", "NC-H-05:luffman", "Robert Luffman", "L", "Owner-operator truck driver for 27 years and a photographer.",
     ("gov-01", 2, V411_NC5("Luffman would push for term and age limits"), "I would push for term and now, age limits for public office."),
     ("gov-02", 2, V411_NC5("Luffman would ban stock trading by officeholders"), "Along with other measures such as banning stock trading and other financial investments for those that hold public office."),
     ("eco-02", 2, V411_NC5("Luffman would end income tax for individuals under $150,000"), "I'd love to eliminate income tax for individuals making less than 150k and households making 300k."),
     ("def-10", 2, V411_NC5("Luffman would stop sending money overseas except humanitarian aid"), "Stop sending money overseas."),
     ("eco-07", 1, V411_NC5("Luffman would scale government back to a set budget"), "Cut back on the blank checks that currently being written until the government is scaled back and runs within a set budget."),
     ("ene-04", -1, V411_NC5("Luffman faults EPA diesel rules as costly"), "EPA regulations being fast forwarded on diesel vehicles to the point of making them utterly useless and costly."))
V411_MO8 = V411(72611110)
cand("MO-H-08", "MO-H-08:lombard", "Rebecca Sharpe Lombard", "L", None,
     ("eco-07", 2, V411_MO8("Lombard’s top priority is slashing federal spending"), "Slashing federal spending and ending corporate welfare are my top priorities."),
     ("eco-02", 1, V411_MO8("Lombard would reduce taxes"), "we need to reduce taxes so that people can keep more of their money"),
     ("def-08", -1, V411_MO8("Lombard would defund global resource deployments"), "We must refuse to raise the debt ceiling without fiscal reforms and defund global resource deployments."))
V411_KS1 = V411(68742092)
more("KS-H-01", "KS-H-01:jacob",
     ("eco-07", 2, V411_KS1("Jacob calls the national debt the biggest national security threat"), "Our National Debt is the biggest national security threat we have."),
     ("hea-03", -1, V411_KS1("Jacob says government involvement makes health care worse"), "Government involvement always makes this worse."),
     ("imm-01", 2, V411_KS1("Jacob says securing the border is a must"), "Securing the border is a must."),
     ("imm-02", 1, V411_KS1("Jacob opposes deporting hard-working immigrants"), "But deporting hard working people who have done nothing but make America better is wrong."),
     ("gov-05", 1, V411_KS1("Jacob says a valid ID is enough to vote"), "I think a vaild ID is enough."),
     ("hea-06", 1, V411_KS1("Jacob would spend more on mental health"), "That will entail more mental health spending."))
V411_MA3 = V411(72660320)
cand("MA-H-03", "MA-H-03:conlon", "Dennis Conlon", "I", None,
     ("ene-01", -1, V411_MA3("Conlon dismisses clean energy advocates"), "Energy will come down as we continue to give less attention to the so called clean energy fear mongers."),
     ("ene-03", 1, V411_MA3("Conlon credits natural gas and opposes blocking gas pipelines"), "Meanwhile, the #1 gift to the environment in this state over the past 25 years was the conversion of power plants to natural gas"))
V411_MS1 = V411(71654256)
more("MS-H-01", "MS-H-01:johnson",
     ("hea-07", 1, V411_MS1("Johnson would make ACA subsidies permanent"), "I would make the ACA subsidies permanent and vote to repeal the Trump Administration's budget bill."),
     ("hea-03", 1, V411_MS1("Johnson would encourage Mississippi to expand Medicaid"), "I would provide incentives for Medicaid expansion in Mississippi"),
     ("hea-01", 1, V411_MS1("Johnson calls health care a basic human right"), "We must view health care as a basic human right and not use it as a political tool."),
     ("imm-02", 1, V411_MS1("Johnson supports a path to permanent status for long-term residents"), "provide a common-sense path to permanent status for immigrants who have lived here and not committed serious crimes"),
     ("imm-01", 1, V411_MS1("Johnson supports modern border security"), "Our immigration efforts should focus on modern and effective border security."),
     ("def-02", 1, V411_MS1("Johnson would repair ties with allies"), "The United States must take seriously its relationship with allies"),
     ("def-07", 1, V411_MS1("Johnson wants diplomacy beyond threats and would renew USAID"), "Diplomacy should be more than threats of military and economic sanctions, and we should renew USAID."),
     ("def-10", -1, V411_MS1("Johnson would renew USAID"), None))
cand("DC-H-98", "DC-H-98:white", "Robert White", "D",
     "D.C. Council at-large member, first elected in 2016, and chair of its Committee on Housing since 2023; former legislative counsel to Delegate Eleanor Holmes Norton.",
     ("imm-08", -1, site("Robert White", "https://www.joinrobertwhite.com/", READ27)("White would protect Washingtonians from ICE"), "protect Washingtonians from ICE and unaccountable federal agents"),
     officialSite="https://www.joinrobertwhite.com/")

# VOTE411 answers for candidates whose own sites gave nothing to map (read Oct. 27).
# Matthew Althaus (OH-9) isn't in Ohio's guide; CD Reynolds (RI governor), Mark Hackett
# (SC Senate), Dayna Alane Smith (SC-2), Courtney McClain (SC-4), Daniel Cottam (UT-2),
# Jennifer Moore (NY-10), Jomo Williams (NY-13), Peter Oberacker (NY-19) and Ryan
# Teasdale (MI-11) left every question blank.
V411_OH2 = V411(72021464)
more("OH-H-02", "OH-H-02:mazzuckelli",
     ("gov-06", 1, V411_OH2("Mazzuckelli backs the John Lewis Voting Rights Act and the For the People Act"), "I would help make sure the John Lewis Voting Rights Act and the For the People Act have a chance to be passed."),
     ("gov-11", 1, V411_OH2("Mazzuckelli would reduce the influence of big money on elections"), "We also need to reduce the influence of both foreign actors and the enormous sums of money on our elections."),
     ("eco-07", 1, V411_OH2("Mazzuckelli would make reducing the deficit a first priority"), "our first priority should be to reduce our deficit which is rapidly approaching $39 trillion"),
     ("eco-01", 1, V411_OH2("Mazzuckelli wants the wealthiest to pay their fair share of taxes"), "I also believe that it would better serve the public good if the \"Epstein class\" paid at least their fair share of taxes"),
     ("def-07", 1, V411_OH2("Mazzuckelli would prioritize diplomacy over military force"), "prioritizes diplomacy unless there are no other options than to use miitary force"),
     ("imm-04", 1, V411_OH2("Mazzuckelli wants more immigration judges and courts"), "I've learned that we need more immigration judges and courts to efficiently process the applications."),
     ("imm-01", 1, V411_OH2("Mazzuckelli would fully fund Customs and Border Protection"), "We need to fully fund CBP to ensure proper vetting and processing"))
V411_OH10 = V411(72021634)
cand("OH-H-10", "OH-H-10:mcmasters", "Thomas McMasters", "L", "Retired Air Force officer and former mayor of Huber Heights; accepts no campaign donations.",
     ("ene-01", 1, V411_OH10("McMasters says the country can’t be antagonistic to green energy"), "We aren't going to get rid of fossil fuel-based power, but we can't be antagonist to green energy either."),
     ("imm-03", -1, V411_OH10("McMasters opposes policies that promote large numbers of people settling here permanently"), "I am not interested in an immigration policy that promotes large numbers of people permanently settling in the United States"))
V411_OH11 = V411(72021667)
cand("OH-H-11", "OH-H-11:kirchner", "Mike Kirchner", "R", None,
     ("imm-03", 1, V411_OH11("Kirchner would encourage immigration by people who can succeed in the economy"), "I would encourage immigration that involves people that could participate in our economy successfully."),
     ("eco-04", 1, V411_OH11("Kirchner would promote more competition"), "I would try to promote more competition where there isn’t."))
V411_NY7 = V411(26979297)
more("NY-H-07", "NY-H-07:ghaznavi",
     ("soc-07", 1, V411_NY7("Ghaznavi would improve access to affordable child care"), "I would expand housing and homeownership opportunities, improve access to affordable healthcare and childcare, support small businesses"),
     ("ene-01", 1, V411_NY7("Ghaznavi supports clean-energy innovation"), "I support climate-resilient infrastructure, clean-energy innovation and stronger sustainability standards."),
     ("gov-11", 1, V411_NY7("Ghaznavi opposes unlimited super PAC spending and would explore equal public financing"), "I also oppose unlimited Super PAC spending, which could undermine equal candidate financing."),
     ("gov-13", -1, V411_NY7("Ghaznavi opposes unlimited super PAC spending"), None),
     ("hou-07", 1, V411_NY7("Ghaznavi wants a more connected passenger rail system"), "I support stronger sustainability standards for federal projects and a more connected, accessible, climate-conscious passenger rail system."),
     ("ene-08", 1, V411_NY7("Ghaznavi would invest in climate-resilient infrastructure"), "The federal government should invest in clean energy, efficient buildings and climate-resilient infrastructure"),
     ("def-02", 1, V411_NY7("Ghaznavi supports the U.S. commitment to NATO"), "I support U.S. participation in the UN and our commitment to NATO."))
V411_MI10 = V411(25687822)
more("MI-H-10", "MI-H-10:nkromo",
     ("hea-09", 1, V411_MI10("Nkromo supports stronger preventive care"), "I also support stronger preventive care, including USDA policies that encourage a more nutrient-dense food system"),
     ("hou-01", 1, V411_MI10("Nkromo would expand affordable housing and community land trusts"), "expand truly affordable housing and Community Land Trusts"),
     ("ene-01", 1, V411_MI10("Nkromo supports moving away from fossil fuels toward cleaner energy"), "I support accelerating the transition away from overdependence on fossil fuels while investing in resilient infrastructure, efficiency, cleaner energy, and good local jobs."),
     ("ene-02", 1, V411_MI10("Nkromo supports revisiting nuclear power"), "I support revisiting nuclear power, including advanced technologies and safety systems"),
     ("imm-02", 1, V411_MI10("Nkromo supports a workable pathway to citizenship"), "I support humane immigration reform that protects due process, family unity, asylum and labor rights, and a workable pathway to citizenship."),
     ("ene-04", 1, V411_MI10("Nkromo would hold polluters accountable"), "Federal policy should protect consumers and hold polluters accountable."))
V411_NJ3W = V411(68198480)
more("NJ-H-03", "NJ-H-03:welzer",
     ("def-01", -2, V411_NJ3W("Welzer would cut the military budget by half"), "If we cut the military budget by 50% our country would still be spending twice as much as any other country in the world."),
     ("def-07", 2, V411_NJ3W("Welzer wants a foreign policy based on diplomacy and international law"), "We must create a new foreign policy based on diplomacy, international law, and human rights."),
     ("ene-01", 2, V411_NJ3W("Welzer calls for substantial funding for renewable energy"), "We call for allocating substantial funding to support renewable energy and clean transportation technology."),
     ("hou-01", 2, V411_NJ3W("Welzer would invest in public social housing"), "Implement public housing investment with a goal to make 60% of the market high-quality, income-based units"),
     ("hou-02", 2, V411_NJ3W("Welzer would bar finance capital from buying homes and rental housing"), "Prohibit finance capital from buying up single-family homes and rental housing stock."),
     ("eco-02", 1, V411_NJ3W("Welzer would cut taxes on incomes below the median"), "Reduce taxes on incomes below the real median income of $75,000 per household."),
     ("eco-12", 2, V411_NJ3W("Welzer wants strongly progressive taxes on income and wealth"), "Institute strongly progressive taxation for incomes and wealth, and increase the estate tax."),
     ("eco-04", 2, V411_NJ3W("Welzer would break up big tech monopolies"), "Break up monopolies in big tech and require data centers to provide their own energy generation."),
     ("eco-09", 1, V411_NJ3W("Welzer would expand the right to unionize"), "Expand and defend workers’ right to unionize."),
     ("hea-01", 2, V411_NJ3W("Welzer supports a universal single-payer health system"), "Under a universal, comprehensive, single-payer system, the administrative waste of private insurance corporations would be redirected to patient care."),
     ("hea-04", -2, V411_NJ3W("Welzer would replace private insurance with single payer"), None),
     ("imm-02", 1, V411_NJ3W("Welzer supports a path to citizenship for immigrants, asylum seekers and refugees"), "We need properly funded institutions to ensure a timely, ethical, transparent, and dignified path to citizenship for immigrants, asylum seekers, and refugees."),
     ("imm-08", -1, V411_NJ3W("Welzer would shut down detention centers"), "We need an overhaul of the immigration system, including transfer of courts to the federal judiciary, shutting down detention centers, and more efficient processes."))

# Last VOTE411 batch (read Oct. 27). Chris Chung (WA-10), Dennis Mahoney (PA-3) and Maria
# Rodriguez (KY-3) left every question blank; Joseph Kibler (WY governor) isn't in
# Wyoming's guide. Wikipedia spells Rodriguez's name "Rodriquez"; her own site and the
# ballot say Rodriguez.
more("KY-H-03", "KY-H-03:rodriquez", name="Maria Rodriguez")
V411_PA2 = V411(50206738)
more("PA-H-02", "PA-H-02:arriaga",
     ("edu-06", 1, V411_PA2("Arriaga puts school choice among the most important issues"), "When I think about the most important issues facing our community and our country, i think about our children especially education and school choice."),
     ("hea-03", 1, V411_PA2("Arriaga would fully fund and protect Medicaid"), "fully fund and protect medicaid for those who needed most"),
     ("hea-09", 1, V411_PA2("Arriaga would expand preventive care"), "cap skyrocketing, prescription drug prices, expand preventative care"),
     ("hea-01", 1, V411_PA2("Arriaga calls health care a basic human right"), "Healthcare is not a luxury, it's a basic human right."),
     ("def-07", 1, V411_PA2("Arriaga would lead with diplomacy and avoid unnecessary conflict"), "lead, with diplomacy, and protect American interests without rushing into unnecessary conflict"),
     ("def-02", 1, V411_PA2("Arriaga would stand with U.S. allies"), "We must stand strong with our allies"),
     ("def-04", 1, V411_PA2("Arriaga says Congress authorizes the use of military force"), "Congress plays a critical role in foreign policies by providing oversight, approving funding and authorizing the use of military Force."))
V411_WV2 = V411(72176432)
more("WV-H-02", "WV-H-02:parsi",
     ("gov-07", 1, V411_WV2("Parsi supports ranked-choice voting"), "a rank choice voting system to give voters more options"),
     ("gov-06", 1, V411_WV2("Parsi would make it easier to vote"), "I also believes in other measures to make it easier to vote, take money out of politics"),
     ("gov-11", 1, V411_WV2("Parsi would take money out of politics"), None),
     ("def-15", -2, V411_WV2("Parsi opposes the continued war in Iran"), "Absolutely not. There has been no strategy, no authorization, and massive costs."),
     ("def-04", 2, V411_WV2("Parsi says Congress must authorize war"), "Congress, under the Constitution, must authorize war."),
     ("imm-07", 1, V411_WV2("Parsi would direct enforcement at violent offenders"), "I believe that immigration enforcement investments should be directed towards violent offenders"),
     ("hea-01", 1, V411_WV2("Parsi would work toward universal health care"), "work towards universal healthcare as a human right"),
     ("hea-02", 1, V411_WV2("Parsi would have Medicare and Medicaid negotiate drug prices"), "have Medicare and Medicaid negotiate with drug companies"),
     ("ene-04", 1, V411_WV2("Parsi would penalize polluters of drinking water"), "I would also advocate accountability for polluters and invoke civil and criminal penalties for decisions that pollute water."))
V411_WI3 = V411(50370669)
more("WI-H-03", "WI-H-03:provance",
     ("cri-05", 1, V411_WI3("Provance wants criminal justice reform that reduces recidivism"), "Criminal Justice reform. Lower cost while working on how to reducing the recidivism rate in our country as well as Wisconsin."),
     ("soc-01", 1, V411_WI3("Provance would secure free speech on social media"), "Securing the American people's rights again. Rights to free speech on social media, our rights to the Second Amendment."),
     ("agr-06", 1, V411_WI3("Provance wants farmers to have more countries to sell to"), "so that our farmer's have more countries to sell our products to"),
     ("hea-03", 1, V411_WI3("Provance would start a basic three-tier government health plan"), "Start a 3 tier government Healthcare plan. Something that covers the basic."),
     ("imm-02", -1, V411_WI3("Provance would treat people here illegally like others who broke the law"), "I would set their treatment the same way we currently treat our inmates."))
cand("WI-H-03", "WI-H-03:kent", "Alexander Kent", "I", "Social worker with a master’s degree from the University of Chicago; founder of the Voter Directed Network, which proposes issue-by-issue online voting.",
     ("hea-01", 1, V411_WI3("Kent calls health care a human right"), "Healthcare is a human right."),
     ("gov-06", 1, V411_WI3("Kent would make Election Day a holiday and protect mail ballots"), "Election Day needs to be a holiday, mail-in ballots must be protected"),
     ("gov-11", 1, V411_WI3("Kent opposes donors, lobbyists and super PACs using money in politics"), "This means NO donors, lobbyists, Super PACs, or political parties using money to corrupt our political system."),
     ("soc-03", 0, V411_WI3("Kent calls himself both pro-life and pro-choice"), "I also consider myself honestly Pro-Life and Pro-Choice."),
     officialSite="https://www.voterdirectednetwork.com/")

# Florida's 28th in VOTE411 (read Oct. 27). Jim Schwartzel (19th), Deborah Adeimy (23rd)
# and Andrew Parrott (6th) left every question blank, as did Alaska's Gerald Heikes, Dan
# J. Sullivan and Eric Hafner, North Dakota's Charles Tuttle and Louisiana's Renada
# Collins, Peter Williams, Kate Cotten, Omar Dantzler and Dan McKay.
V411_FL28 = V411(71841246)
more("FL-H-28", "FL-H-28:ehr",
     ("imm-02", 1, V411_FL28("Ehr would provide an earned path to legal residency"), "Provide an Earned Path to Legal Residency"),
     ("imm-03", 1, V411_FL28("Ehr would expedite legal immigration"), "Modernize and Expedite the Legal Immigration Process"),
     ("imm-01", 1, V411_FL28("Ehr would upgrade ports of entry and border agent training"), "Upgrade Ports of Entry and the training of Boarder agents"),
     ("ene-08", 1, V411_FL28("Ehr would expand federal grants to harden homes against storms"), "expanding federal mitigation grants for homeowners to harden their properties against storm damage"),
     ("gov-06", 2, V411_FL28("Ehr supports automatic and same-day voter registration"), "Establish Automatic Voter Registration (AVR) and Same-Day Registration"),
     ("edu-06", -2, V411_FL28("Ehr opposes dismantling public education through vouchers"), "The federal government cannot take a backseat or leave public education to be dismantled by vouchers, austerity, and privatization."),
     ("edu-01", 1, V411_FL28("Ehr wants robust federal investment in education"), "We need robust federal investment, strict accountability for equity, and total protection of students' civil rights."))

# Officeholders whose campaign sites stated no positions but whose records do: Hilda
# Solis's site describes what she did as a supervisor and labor secretary, and Peter
# Oberacker's state Senate office describes the bills he passed (read Oct. 27; his
# Senate pages refuse scripts, so it was read in the browser pane).
SOLIS = lambda path: site("Hilda Solis", f"https://www.hildasolis.com/{path}", READ27)  # noqa: E731
more("CA-H-38", "CA-H-38:solis",
     ("hea-07", 1, SOLIS("meet-hilda/")("Solis helped pass the Affordable Care Act as labor secretary and expanded its reach in L.A. County"), "After helping pass the Affordable Care Act as President Obama’s Secretary of Labor, Hilda led efforts to implement it and expand access to affordable healthcare"),
     ("hou-01", 1, SOLIS("meet-hilda/")("Solis helped pass Measure H to fund housing for homeless people"), "Solis helped pass Measure H, a groundbreaking effort bringing in hundreds of millions of dollars to house tens of thousands of people experiencing homelessness."),
     ("cri-08", 1, SOLIS("meet-hilda/")("Solis backs a “Care First, Jail Last” approach to public safety"), "reimagining public safety to prioritize Care First, Jail Last"),
     ("edu-03", 1, SOLIS("meet-hilda/")("Solis funded a $20 million workforce and job training program"), "Solis led a team to develop and fully fund a $20 million workforce and job training program"),
     ("ene-04", 1, SOLIS("meet-hilda/")("Solis led the cleanup of lead contamination near the Exide plant"), "helped to clean up poisonous lead in thousands of homes"),
     ("hea-06", 1, SOLIS("fighting-covid-19/")("Solis had the county expand mental health services for Latino communities"), "Hilda Solis directed the County Department of Mental Health to expand mental health services for Latino immigrant and nonimmigrant populations impacted by COVID-19."),
     ("hou-03", 1, SOLIS("metro-chair-solis-supports-free-ride-program-for-lausd-students-9-23-21/")("As Metro chair, Solis launched fare-free transit for students"), "Metro, at the direction of Chair Solis, has launched a 23-month pilot program which will allow K-12 and community college students to ride Metro fare-free."))
NY_SENATE = lambda note: page(f"New York State Senate, Sen. Oberacker press release, June 13, 2025: {note}", "https://www.nysenate.gov/newsroom/press-releases/2025/peter-oberacker/senator-oberacker-highlights-legislative-wins-2025-0", READ27)  # noqa: E731
more("NY-H-19", "NY-H-19:oberacker",
     ("gov-11", 1, NY_SENATE("Oberacker passed a bill barring utilities from spending ratepayer money on lobbying and political contributions"), "another to ban the use of ratepayer dollars for lobbying, public relations, or political contributions"),
     ("def-03", 1, NY_SENATE("Oberacker sponsored a statewide job database for veterans"), "creating a statewide career and job listing database tailored to veterans"),
     bio="State senator since 2021, food scientist and founder of FormTech Solutions; a volunteer firefighter and EMT for nearly four decades.")

# Wikipedia spells the 6th district's Libertarian "Tegan"; the FEC and VOTE411 say Teagan.
cand("MI-H-06", "MI-H-06:tegan", "Timothy A. Teagan", "L", None)

# A news report where a candidate has no site and answered no guide.
NBCPS_CA25 = article("NBC Palm Springs, May 15, 2026", "https://www.nbcpalmsprings.com/decision-2026/2026/05/15/candidates-lay-out-key-issues-in-californias-25th-congressional-district-race", "2026-05-15")
cand("CA-H-25", "CA-H-25:males", "Joe Males", "R", "Marine veteran and Hemet City Council member, on the ballot as mayor pro tem.",
     ("eco-02", 1, NBCPS_CA25("Males says cutting gas taxes and rolling back regulations would lower families’ costs"), None),
     ("imm-01", 1, NBCPS_CA25("Males emphasizes stronger border enforcement"), None))

# Texas candidates with few positions, from their VOTE411 answers (read Oct. 27; quotes
# checked against the page text). Espoir Ngabo (G, 7th), Alex Mealer (R, 9th), Chris
# Gober (R, 10th), Adam Bauman (R, 16th), Casey Shepard (D, 17th), Trever Nehls (R, 22nd)
# and Everett Jackson (R, 30th) left every question blank; the 4th, 14th and 19th
# districts have no VOTE411 guide.
V411_TX2 = V411(71560439)
more("TX-H-02", "TX-H-02:finnie",
     ("ene-08", 1, V411_TX2("Finnie would increase funding for flood mitigation"), "I will work with colleagues on both sides of the aisle to increase funding for flood mitigation"),
     ("eco-10", -1, V411_TX2("Finnie calls the current tariffs destructive"), "This has led to wildly destructive tariffs that have sent our prices skyrocketing."),
     ("def-15", -2, V411_TX2("Finnie calls the war in Iran pointless"), "The pointless and costly war in Iran has only worsened the situation"),
     ("soc-07", 1, V411_TX2("Finnie would expand child care tax credits"), "Congress should also work to expand tax credits for childcare services"),
     ("hou-04", 1, V411_TX2("Finnie wants local zoning eased so more affordable housing is built"), "ensure that local municipalities ease zoning restrictions and work with developers to increase the amount of affordable housing built throughout the US"),
     ("imm-02", 1, V411_TX2("Finnie supports gradual citizenship for long-settled, law-abiding immigrants"), "implementing a system that gradually provides citizenship to those who have been in the country for years"),
     ("imm-07", 1, V411_TX2("Finnie would focus ICE on deporting violent criminals"), "directing its day-to-day operations to deporting violent criminals"),
     ("imm-08", -1, V411_TX2("Finnie would return ICE to its pre-2025 funding"), "We need to reverse the expansion of ICE by returning the agency to its pre-2025 funding levels"),
     ("gov-05", 1, V411_TX2("Finnie calls Texas’s elections, where every voter shows identification, ideal"), "I believe that Texas has an ideal electoral system"))
V411_TX6 = V411(6505533)
more("TX-H-06", "TX-H-06:minton",
     ("imm-02", 2, V411_TX6("Minton wants a clear path to citizenship"), "We must create a clear, fair path to citizenship so people can live and work here legally."),
     ("gov-09", 1, V411_TX6("Minton would end officials’ use of office to get rich"), "End the presidential grift, where leaders use their office to get rich."),
     ("eco-10", -1, V411_TX6("Minton would stop the current tariffs"), "Stop the illegal tariffs that raise prices."),
     ("hea-03", 2, V411_TX6("Minton supports Medicare for All"), "I support Medicare for All, so every person is covered no matter their job or income."),
     ("eco-12", 1, V411_TX6("Minton would lift the Social Security tax cap"), "Lift the Social Security cap so the rich pay on all of their income, not just part."),
     ("eco-01", 1, V411_TX6("Minton would make billionaires pay more"), "Make billionaires pay their fair share."),
     bio="Surgical technology specialist with more than 30 years in health care; zoology degree from the University of Oklahoma.")
V411_TX21 = V411(73698106)
more("TX-H-21", "TX-H-21:hook",
     ("hea-03", 1, V411_TX21("Hook would close the Medicaid coverage gap"), "closing the Medicaid coverage gap in states that haven't expanded it"),
     ("gov-11", 1, V411_TX21("Hook would get money out of politics"), "I will work to get money out of politics."),
     ("eco-02", 1, V411_TX21("Hook would lower taxes for working families"), "I will fight to lower taxes for working families, raise wages, lower everyday costs"),
     ("def-03", 1, V411_TX21("Hook would expand veterans’ benefits"), "expand earned benefits like Social Security and the VA"),
     ("edu-01", 1, V411_TX21("Hook would invest in public schools"), "I will expand opportunity by investing in public schools"),
     ("hea-01", 1, V411_TX21("Hook advocates health care for all"), "advocating for healthcare for all"),
     ("hea-02", 2, V411_TX21("Hook would expand Medicare’s power to negotiate drug prices"), "Congress must hold Big Insurance and Big Pharma accountable by cracking down on price-gouging and expanding Medicare's power to negotiate drug prices."),
     ("hea-07", 1, V411_TX21("Hook would strengthen and defend the Affordable Care Act"), "We should strengthen and defend the Affordable Care Act"),
     ("eco-06", 1, V411_TX21("Hook would expand federal funding for rural water infrastructure"), "I'll fight to expand federal funding for rural water infrastructure and drought resilience"),
     bio="Scientist with a PhD in animal behavior, former middle school teacher and federal government employee.")
V411_TX28 = V411(71563707)
more("TX-H-28", "TX-H-28:duran",
     ("gov-11", 2, V411_TX28("Durán wants a constitutional amendment against Citizens United"), "We need an Anti-Citizens United Constitutional Amendment to end the power of billionaire donors and their PACs."),
     ("gov-13", -2, V411_TX28("Durán would end Citizens United"), None),
     ("imm-07", -2, V411_TX28("Durán would end all detention and deportations"), "End all immigration detention and deportations."),
     ("imm-01", -2, V411_TX28("Durán would demilitarize the border and tear down the wall"), "Let’s demilitarize our border and tear down the wall!"),
     ("def-01", -2, V411_TX28("Durán would cut military spending by 90%"), "We'll cut 90% of military spending"),
     ("def-08", -2, V411_TX28("Durán would close all foreign bases"), "close all foreign bases, and reinvest that money into our communities"),
     ("edu-02", 2, V411_TX28("Durán promises free college"), "we will have Medicare for All, Free College, Free Childcare, Food Stamps for All"),
     ("soc-07", 2, V411_TX28("Durán promises free child care"), "we will have Medicare for All, Free College, Free Childcare, Food Stamps for All"),
     ("edu-05", 2, V411_TX28("Durán would forgive all student loans"), "a federal jobs guarantee, forgive all student loans and more!"),
     ("eco-01", 2, V411_TX28("Durán would redistribute billionaires’ wealth"), "Let’s abolish billionaires and redistribute their wealth to the 99% via Universal Basic Income."),
     ("ene-01", 2, V411_TX28("Durán wants a rapid transition to 100% renewable energy"), "massively subsidize a rapid and just transition to 100% renewable energy"),
     ("ene-03", -2, V411_TX28("Durán would shut down the fossil fuel industry"), "nationalize and shut down the fossil fuel industry"),
     ("hea-01", 2, V411_TX28("Durán supports Medicare for All"), "We need Medicare for All!"),
     ("hea-10", 2, V411_TX28("Durán wants Medicare to cover dental, vision and hearing aids"), "It will include prescriptions, dental, vision, hearing aids, and mental health."))
V411_TX32 = V411(25679078)
more("TX-H-32", "TX-H-32:barrios",
     ("gov-01", 1, V411_TX32("Barrios supports congressional term limits"), "I support congressional term limits"),
     ("gov-11", 1, V411_TX32("Barrios supports overturning Citizens United"), "overturning Citizens United"),
     ("gov-13", -1, V411_TX32("Barrios supports overturning Citizens United"), None),
     ("gov-09", 1, V411_TX32("Barrios would ban former members from lobbying for five years"), "a five-year lobbying ban for former members of Congress"),
     ("gov-02", 1, V411_TX32("Barrios would ban members from trading stocks"), "banning members from trading individual stocks"),
     ("imm-02", 1, V411_TX32("Barrios would create pathways for DREAMers and long-term residents"), "create pathways for DREAMers and long-term residents"),
     ("imm-07", 1, V411_TX32("Barrios would focus enforcement on criminals, gangs and traffickers"), "Enforcement should focus on criminals, gangs, and human traffickers while protecting due process and family unity."),
     ("eco-02", 1, V411_TX32("Barrios would expand the Child Tax Credit and Earned Income Tax Credit"), "I also support expanding the Child Tax Credit and Earned Income Tax Credit"),
     ("ene-01", 1, V411_TX32("Barrios would expand wind, solar and other new energy"), "expanding wind, solar, batteries, geothermal, and emerging technologies"),
     ("ene-03", 1, V411_TX32("Barrios says Texas should build on its oil and gas strength"), "Texas should build on its strength in oil and gas"),
     ("ene-08", 1, V411_TX32("Barrios wants better preparation for floods and extreme weather"), "better preparation for floods, droughts, and extreme weather"),
     ("def-04", 1, V411_TX32("Barrios says Congress should take responsibility for sustained military action"), "Congress should take responsibility for sustained military action, including in Iran."),
     bio="Sales executive and teacher by background, with business degrees from the University of North Texas and Western Governors University.")

# Florida candidates with few positions, from their VOTE411 answers (League of Women
# Voters of Florida, read Oct. 27; quotes checked against the page text).
V411_FL1 = V411(71841165)
more("FL-H-01", "FL-H-01:valimont",
     ("imm-01", 1, V411_FL1("Valimont would strengthen border security with technology and resources"), "I believe we should strengthen border security through better technology, resources, and more immigration judges"),
     ("imm-04", 1, V411_FL1("Valimont wants more immigration judges"), "more immigration judges so cases can be processed efficiently and fairly"),
     ("imm-02", 1, V411_FL1("Valimont supports a pathway to citizenship, including for Dreamers"), "I also support creating a clear pathway to citizenship for immigrants who contribute to our communities"),
     ("ene-08", 1, V411_FL1("Valimont would invest in resilient infrastructure and disaster preparedness"), "Investing in resilient infrastructure, cleaner energy, and disaster preparedness will help reduce long-term costs"),
     ("ene-01", 1, V411_FL1("Valimont would invest in cleaner energy"), "Investing in resilient infrastructure, cleaner energy, and disaster preparedness will help reduce long-term costs"),
     ("soc-02", 1, V411_FL1("Valimont would strengthen the John Lewis Voting Rights Act"), "strengthen the John Lewis Voting Rights Act, and push back against tactics that make participation harder"),
     ("soc-07", 1, V411_FL1("Valimont would expand affordable early education and child care"), "I support expanding access to affordable early childhood education and childcare"),
     ("edu-01", 1, V411_FL1("Valimont wants reliable federal funding for schools"), "the federal government should provide reliable funding, support teacher training and mental health services"),
     ("edu-04", 1, V411_FL1("Valimont would raise teacher pay"), "I would advocate to raise teacher pay"),
     ("edu-03", 1, V411_FL1("Valimont supports job training and apprenticeships"), "supporting job training and apprenticeships that lead to good-paying careers"),
     ("soc-01", 1, V411_FL1("Valimont would protect speech she disagrees with"), "I also believe freedom of speech means protecting the voices of people who I may strongly disagree."),
     bio="Grew up in Thomaston, Georgia; health and exercise science degree from Georgia Southern University and an M.A. in education from Troy State University.")
more("FL-H-01", "FL-H-01:davis",
     ("imm-07", 1, V411_FL1("Davis would move serious or repeat offenders into deportation faster"), "Individuals who commit serious crimes or repeatedly offend should be detained and moved into deportation proceedings more quickly."),
     ("edu-03", 1, V411_FL1("Davis would expand career and technical training and apprenticeships"), "expand career and technical training, support apprenticeships alongside college pathways"),
     ("edu-10", 1, V411_FL1("Davis would improve financial, civic and technology literacy"), "improve financial, civic, and technology literacy so every American is prepared for the future"),
     ("gov-12", 1, V411_FL1("Davis wants more transparency in government spending"), "greater transparency in spending and decision-making, and stronger oversight so citizens can clearly see how their tax dollars are being used"),
     ("soc-01", 1, V411_FL1("Davis would protect the right to criticize the government"), "Freedom of speech protects every American's right to express their opinions, question authority, and criticize their government without fear of government censorship."),
     bio="From Cantonment in Escambia County; bachelor of applied science in business and management.")
V411_FL3 = V411(71841171)
more("FL-H-03", "FL-H-03:klein",
     ("imm-02", 1, V411_FL3("Klein would protect Dreamers and give them a path to citizenship"), "Protect Dreamers and provide a path to citizenship."),
     ("ene-08", 1, V411_FL3("Klein calls climate resilience an investment"), "We should stop treating climate resilience as an environmental expense. It is an investment in economic stability."),
     ("eco-04", 1, V411_FL3("Klein would confront monopoly power and price manipulation"), "confronting monopoly power and price manipulation"),
     ("eco-06", 1, V411_FL3("Klein would invest in infrastructure"), "investing in American agriculture, manufacturing, energy, and infrastructure"),
     ("gov-03", 1, V411_FL3("Klein supports campaign finance reform and greater transparency"), "I support campaign-finance reform, greater transparency, stronger ethics and anti-corruption laws, restricting congressional stock trading"),
     ("gov-09", 1, V411_FL3("Klein supports stronger ethics and anti-corruption laws"), "stronger ethics and anti-corruption laws"),
     ("gov-02", 1, V411_FL3("Klein would restrict congressional stock trading"), "restricting congressional stock trading, and reducing the power of special interests"),
     ("soc-01", 2, V411_FL3("Klein says free speech matters most when it is unpopular"), "It matters most when speech is unpopular, uncomfortable, or challenges those in power."),
     ("edu-01", 1, V411_FL3("Klein would help close school funding gaps"), "help close funding gaps, and invest in teachers, technology, and career education"),
     ("edu-03", 1, V411_FL3("Klein wants stronger pathways into apprenticeships and technical careers"), "We need stronger pathways into universities, community colleges, apprenticeships, and technical careers"))

# Illinois and Georgia candidates with few positions, in VOTE411 (read Oct. 28; quotes
# checked against the page text). Michael Noack (R, 2nd), La Shawn Ford (7th), Melissa
# Bean (8th), Jennifer Todd (15th) and Dillan Vancil (R, 17th) left every question blank
# (the 5th district's guide lists only Mike Quigley, not Tommy Hanson), as did Georgia's Maura Keller (3rd),
# Jim Duffie (R, 4th), Tony Kozycki (7th), Pam Delancy and Houston Gaines (10th),
# Ceretta Smith (12th) and Jonathan Chavez (R, 13th).
V411_IL2 = V411(71914062)
more("IL-H-02", "IL-H-02:miller",
     ("def-04", 2, V411_IL2("Miller would reclaim Congress’s war powers"), "The Constitution is clear: Congress decides when the nation goes to war."),
     ("soc-02", 1, V411_IL2("Miller would pass the John R. Lewis Voting Rights Advancement Act"), "I will fight to pass the John R. Lewis Voting Rights Advancement Act"),
     ("gov-11", 2, V411_IL2("Miller supports a constitutional amendment to overturn Citizens United"), "I will also support a constitutional amendment to overturn Citizens United."),
     ("gov-13", -2, V411_IL2("Miller would overturn Citizens United"), None),
     ("imm-02", 2, V411_IL2("Miller wants a swift path to citizenship"), "I would focus on a swift and humane path to citizenship for migrants, due process for all"),
     ("eco-02", 1, V411_IL2("Miller would curtail taxes that hurt working families"), "curtailing taxes and tariffs that disproportionately hurt working families, small businesses and local governing bodies"),
     ("eco-10", -1, V411_IL2("Miller would curtail tariffs that hurt working families"), "curtailing taxes and tariffs that disproportionately hurt working families, small businesses and local governing bodies"),
     ("eco-06", 1, V411_IL2("Miller would fund state infrastructure projects"), "Congressionally approved support for state infrastructure projects with the greatest potential benefit to struggling cities and farming communities"))
V411_IL12 = V411(71780848)
more("IL-H-12", "IL-H-12:fortier",
     ("gov-02", 2, V411_IL12("Fortier would bar officials and their families from trading stocks"), "no one who serves in the executive, legislative, or judicial branch, or their spouses or dependents should be allowed to own or trade individual stocks"),
     ("gov-09", 2, V411_IL12("Fortier answers “Absolutely” to stricter ethics rules for Congress"), None),
     ("eco-03", 1, V411_IL12("Fortier would raise the minimum wage"), "The most effective way is to increase minimum wage and remove the additional tariffs that this administration has put on goods."),
     ("eco-10", -1, V411_IL12("Fortier would remove the administration’s added tariffs"), "The most effective way is to increase minimum wage and remove the additional tariffs that this administration has put on goods."),
     ("hea-01", 2, V411_IL12("Fortier wants universal health care"), "The government should work hard to have a Universal Healthcare plan for all of its citizens."),
     ("imm-02", 1, V411_IL12("Fortier supports a path to citizenship for taxpaying immigrants"), "The US can have a program that allows tax paying immigrants a clear path to become citizens without hostility or threats."))
V411_IL16 = V411(71843421)
more("IL-H-16", "IL-H-16:nolley",
     ("gov-11", 1, V411_IL16("Nolley supports campaign finance reform to reduce money’s role in elections"), None),
     ("imm-02", 2, V411_IL16("Nolley would give DREAMers legal status and a path to citizenship"), "DACA recipients and DREAMers need to be fully protected and immediately granted legal status with a straightforward path to citizenship."),
     ("ene-01", 2, V411_IL16("Nolley would restore and expand renewable energy investment"), "We must begin by restoring and expanding investments in renewable energy projects cut by the Big Beautiful Bill."))

# Virginia candidates with few positions, in VOTE411 (League of Women Voters of
# Virginia, read Oct. 28; quotes checked against the page text). J. Matt Baker (I, 2nd),
# Edwin Rivera Jr. (R, 3rd), Robert Murray Jr. (R) and Joan Bell (I) in the 4th, and Doug
# Ollivant (R) and Randall Terry (I) in the 7th left every question blank.
V411_VA5 = V411(73041851)
more("VA-H-05", "VA-H-05:harvey",
     ("gov-13", -2, V411_VA5("Harvey would strip corporations of the rights that permit their election spending"), "I would encourage states to pass laws stripping corporations of their granted rights which permitted this corporate spending in elections."),
     ("hea-09", 1, V411_VA5("Harvey would provide basic preventive care for all citizens"), "I would advocate for the implementation of basic preventative healthcare for all citizens including mental health services."),
     ("hea-06", 1, V411_VA5("Harvey would include mental health services in basic care for all"), "I would advocate for the implementation of basic preventative healthcare for all citizens including mental health services."),
     ("def-15", -2, V411_VA5("Harvey would vote to end the war in Iran"), "advocate for the end of the war in Iran, specifically on the war powers resolution act to end military hostilities in Iran"),
     ("def-04", 1, V411_VA5("Harvey backs the war powers resolution on Iran"), "advocate for the end of the war in Iran, specifically on the war powers resolution act to end military hostilities in Iran"),
     ("eco-07", 2, V411_VA5("Harvey would pass a budget that cuts deficit spending"), "Secondly is the moral and ethical choice to pass a federal budget that cuts deficit spending."))
V411_VA6 = V411(73042264)
more("VA-H-06", "VA-H-06:macy",
     ("imm-07", 1, V411_VA6("Macy faults ICE for not focusing on deporting hardened criminals"), "Instead of deporting hardened criminals, ICE has separated families"),
     ("imm-09", 2, V411_VA6("Macy would make H-2A farm visas easier to use"), "Congress must reform the H-2A visa program to make it easier for farmers to hire workers with less bureaucratic red tape."),
     ("gov-11", 1, V411_VA6("Macy refuses corporate PAC money as a corrupting influence"), "I do not take corporate PAC money because I believe it is a corrupting influence in U.S. politics."),
     ("gov-09", 2, V411_VA6("Macy would lower gift limits and pass binding ethics reform"), "We need to lower the gift limits and pass legally binding ethics reform."),
     ("gov-03", 2, V411_VA6("Macy would bring full transparency to campaign finance"), "would champion efforts to bring unassailable transparency to campaign finance laws"),
     ("eco-10", -2, V411_VA6("Macy calls Trump’s tariffs ruinous"), "I will work to make Congress regain its spine and stand up to Trump’s ruinous tariff and trade wars."),
     ("hea-01", 2, V411_VA6("Macy would fight for universal coverage, including Medicare for All"), "I will fight for universal healthcare coverage including Medicare for All."))

# More Virginia answers in VOTE411 (read Oct. 28); Tony Sabio (R, 8th) left every question blank.
V411_VA9 = V411(73042128)
more("VA-H-09", "VA-H-09:powers",
     ("imm-08", -1, V411_VA9("Powers would stop writing blank checks to ICE"), "Congress should stop writing blank checks to ICE and demand real oversight, transparency, and accountability for abuses."),
     ("imm-07", 1, V411_VA9("Powers wants enforcement focused on trafficking and violent crime"), "We need secure borders and enforcement focused on trafficking, violent crime, and genuine threats to public safety"),
     ("gov-03", 1, V411_VA9("Powers supports stronger disclosure and closing dark-money loopholes"), "I support stronger disclosure requirements, closing dark-money loopholes, tougher enforcement of campaign finance laws, and reforms that amplify small-dollar donors."),
     ("gov-11", 1, V411_VA9("Powers supports an amendment allowing limits on political spending"), "I would also support a constitutional amendment allowing reasonable limits on political spending."),
     ("gov-13", -1, V411_VA9("Powers would allow limits on political spending"), None),
     ("soc-07", 1, V411_VA9("Powers would prioritize child care in federal spending"), "I would prioritize rural hospitals, 340B, Medicare and Medicaid, affordable housing, broadband, childcare, and food security."),
     ("edu-03", 1, V411_VA9("Powers would expand apprenticeships and career and technical education"), "expanding apprenticeships, protecting miners and black lung benefits, strengthening public schools and CTE"))
V411_VA11 = V411(73041197)
more("VA-H-11", "VA-H-11:blais",
     ("imm-08", -2, V411_VA11("Blais would eliminate funding for ICE"), "I'd like to eliminate funding for ICE (which didn't exist before 2003)"),
     ("imm-01", -2, V411_VA11("Blais would cut the Customs and Border Protection budget significantly"), "decrease significantly the CBP budget"),
     ("gov-13", -1, V411_VA11("Blais wants every campaign federally funded"), "All campaigns should be federally funded and of a short duration."),
     ("hea-01", 2, V411_VA11("Blais wants a national health care program"), "We badly need a national health care program."),
     ("eco-03", 2, V411_VA11("Blais says the minimum wage must be raised"), "No full-time worker should need federal assistance so the minimum wage must be raised."))

# Ohio candidates with few positions, in VOTE411 (League of Women Voters of Ohio, read
# Oct. 28; quotes checked against the page text). Carey Coleman (R, 13th) left every
# question blank; Elizabeth Kirtley's answers (6th) repeat positions she already has.
V411_OH1 = V411(72021430)
more("OH-H-01", "OH-H-01:weise",
     ("gov-07", 2, V411_OH1("Weise fully supports the push for ranked-choice voting in Ohio"), "I fully support that effort, and I would also support Approval Voting (AV)."),
     ("def-10", 2, V411_OH1("Weise would end foreign aid"), "I support ending foreign aid."),
     ("def-01", -2, V411_OH1("Weise would significantly shrink the military"), "I also support significantly reducing the size and scope of our military."),
     ("eco-10", -2, V411_OH1("Weise says tariffs act as taxes on consumers"), "Tariffs and other trade barriers often function as taxes on consumers, raising prices for Americans."),
     ("agr-06", 1, V411_OH1("Weise supports free trade"), "I support free trade policies that increase competition and lower the cost of everyday goods."),
     ("def-08", -2, V411_OH1("Weise would bring troops home from bases abroad"), "But we need to bring the troops home. Not just from war zones, but from Germany, Australia, Japan, and elsewhere."),
     ("imm-03", 1, V411_OH1("Weise wants a much simpler path to a green card"), "The United States needs a much simpler path to a Green Card and eventual citizenship."),
     ("imm-08", -1, V411_OH1("Weise opposes militarized immigration enforcement"), "I do not support militarized immigration enforcement."))
V411_OH4 = V411(72021498)
more("OH-H-04", "OH-H-04:tackett",
     ("gov-03", 2, V411_OH4("Tackett would require donor reporting and end dark money"), "Campaign Finance Reform to increase transparency and require reporting of donors. No more dark money."),
     ("hou-04", 1, V411_OH4("Tackett would make it easier to build new housing"), "Support efforts to make it easier to build new housing and to scale construction and development."),
     ("ene-01", 1, V411_OH4("Tackett would speed up solar and batteries"), "An All of the Above Energy Policy, speeding up the development of solar, batteries, nuclear, and natural gas."),
     ("ene-02", 1, V411_OH4("Tackett would speed up nuclear power"), "An All of the Above Energy Policy, speeding up the development of solar, batteries, nuclear, and natural gas."),
     ("ene-03", 1, V411_OH4("Tackett would speed up natural gas"), "An All of the Above Energy Policy, speeding up the development of solar, batteries, nuclear, and natural gas."),
     ("eco-10", -2, V411_OH4("Tackett rejects both parties’ tariffs"), "Reject the price setting and tariffs of the Democrats and Republicans which only raise prices and reduce supply."),
     ("eco-07", 1, V411_OH4("Tackett would balance the budget and bring down the debt"), "Balance the budget and start bringing down the debt."),
     ("def-04", 1, V411_OH4("Tackett opposes unconstitutional wars"), "no more unconstitutional wars, no more reckless trade wars"),
     ("def-02", 2, V411_OH4("Tackett would recommit to strong alliances"), "The best deterrence is strong alliances: recommit to our friends, trade and invest more with nations that share our values"),
     ("imm-07", 1, V411_OH4("Tackett would prioritize enforcement against violent criminals"), "prioritize enforcement for these here illegally already against violent criminals"),
     ("imm-02", 1, V411_OH4("Tackett supports a path to citizenship for long-settled, working immigrants"), "a pathway to citizenship for those here for years, working and following the law"),
     ("imm-03", 1, V411_OH4("Tackett wants more visas for high-skilled innovators"), "more visas for high-skilled innovators and the seasonal ag labor Ohio farms depend on"),
     ("imm-09", 1, V411_OH4("Tackett wants more seasonal farm labor visas"), "more visas for high-skilled innovators and the seasonal ag labor Ohio farms depend on"),
     bio="Springfield’s assistant mayor, elected to the city commission in 2023; master’s in public policy and leadership from Ohio State.")
V411_OH5 = V411(72021507)
more("OH-H-05", "OH-H-05:shaver",
     ("hou-01", 1, V411_OH5("Shaver would invest in affordable rural housing"), "investing in modest, affordable housing in rural communities"),
     ("gov-09", 1, V411_OH5("Shaver wants guardrails against officials profiting from office"), "clear guardrails to prevent elected officials from profiting from their positions"),
     ("def-04", 1, V411_OH5("Shaver says Congress should reassert its war powers"), "Congress should reassert its authority, especially when it comes to whether offensive or preemptive military action is even justified."))
V411_OH8 = V411(72021586)
more("OH-H-08", "OH-H-08:enoch",
     ("gov-06", 1, V411_OH8("Enoch would protect early, absentee and mail-in voting"), "we can protect early, absentee, and mail-in voting for seniors, veterans, and working families"),
     ("gov-04", 2, V411_OH8("Enoch would end partisan gerrymandering"), "I'll fight to end partisan gerrymandering through fair, citizen-centered redistricting"),
     ("gov-03", 1, V411_OH8("Enoch wants full transparency to get secret money out of politics"), "I'll work to get secret money out of politics through full transparency and empowering small-dollar donors."),
     ("soc-07", 1, V411_OH8("Enoch would make child care affordable"), "making childcare and eldercare affordable so parents can work with peace of mind"),
     ("def-07", 1, V411_OH8("Enoch would invest in diplomacy that prevents conflict"), "invest in the diplomacy and deterrence that prevent conflict in the first place"),
     ("def-03", 1, V411_OH8("Enoch would fight for veterans’ care"), "And I'll fight to give our veterans the care they earned when they come home."),
     ("imm-01", 1, V411_OH8("Enoch would secure the border with technology and personnel"), "I'll support securing our borders with smart technology and enough personnel to stop trafficking and fentanyl"),
     ("imm-02", 2, V411_OH8("Enoch would fight for an earned path to citizenship"), "I'll fight for a real, earned path to citizenship for Dreamers and for those already contributing here"))

# Missouri candidates with few positions, in VOTE411 (League of Women Voters of
# Missouri's local guides, read Oct. 28; quotes checked against the page text). Chris
# Stigall (R, 6th) left every question blank; Chris Reichard's answers (8th) name no
# policies to map.
V411_MO1 = V411(72611019)
more("MO-H-01", "MO-H-01:schmitz",
     ("def-10", 2, V411_MO1("Schmitz would end foreign aid"), "We need a foreign policy of peace, non-interventionism and an end to foreign aid."),
     ("hea-04", 2, V411_MO1("Schmitz wants an absolute free-market health system"), "We need an absolute free-market healthcare system."),
     ("def-15", -2, V411_MO1("Schmitz would end the Iran war immediately"), "Bring an immediate end to the Iran war"),
     ("ene-02", 1, V411_MO1("Schmitz would allow free-market construction of nuclear plants"), "Battle global climate change by allowing free-market construction of new nuclear power plants."),
     bio="Criminal defense attorney with a law degree from Creighton University.")
V411_MO3 = V411(72611085)
more("MO-H-03", "MO-H-03:mann",
     ("hea-01", 2, V411_MO3("Mann champions health care for all"), "I champion healthcare for all, union protections and public education"),
     ("eco-09", 2, V411_MO3("Mann would fight for collective bargaining and workplace protections"), "I am committed to fighting for fair pay, collective bargaining and robust workplace protections for all."),
     ("eco-04", 1, V411_MO3("Mann prioritizes anti-monopoly enforcement"), "My rural agenda prioritizes anti-monopoly enforcement, farmworker rights and critical infrastructure investment."),
     ("eco-06", 1, V411_MO3("Mann prioritizes infrastructure investment"), "My rural agenda prioritizes anti-monopoly enforcement, farmworker rights and critical infrastructure investment."),
     bio="Environmental chemist (an ion chromatography specialist) with a chemistry degree from the University of Illinois Springfield.")
V411_MO4 = V411(68484949)
more("MO-H-04", "MO-H-04:herrera",
     ("gov-11", 1, V411_MO4("Herrera would remove money from politics"), "ban insider trading and lobbyists, remove money from politics, and protect every eligible voter’s right to participate"),
     ("edu-04", 1, V411_MO4("Herrera wants well-paid public educators"), "a good education with well-paid public educators"),
     ("eco-04", 2, V411_MO4("Herrera would fight for stronger competition in farm and food markets"), "Farmers and consumers deserve markets that are not controlled by a handful of powerful corporations."))
V411_MO6 = V411(68484993)
more("MO-H-06", "MO-H-06:smead",
     ("imm-04", 1, V411_MO6("Smead wants enough immigration courts to process cases"), "Even constitutional rights can be defended better if we had enough immigration courts to process cases."),
     ("hea-06", 1, V411_MO6("Smead wants mental health clinics within easy reach"), "We need mental and physical health clinics within easy access of all who need it."))
more("MO-H-06", "MO-H-06:maidment",
     ("eco-02", 1, V411_MO6("Maidment would lower taxes by streamlining government"), "Lower taxes and reducing the need for taxes by streamlining government and government programs."))
V411_MO7 = V411(22209669)
more("MO-H-07", "MO-H-07:craig",
     ("def-04", 1, V411_MO7("Craig would work across parties to oppose unconstitutional wars"), "breaking ranks with the establishment to oppose unconstitutional wars and wasteful spending"),
     ("eco-02", 1, V411_MO7("Craig says taxpayers should keep the money they earn"), "Taxpayers should be allowed to keep the money they earned and to spend that money on services which benefit the public."))

# New Jersey candidates with few positions, in VOTE411 (League of Women Voters of New
# Jersey, read Oct. 28; quotes checked against the page text). Sean Kirrane (R, 5th),
# Terrisa Bukovinac (Save Our Babies, 9th), Joe Hathaway (R, 11th) and Adam Hamawy (12th)
# left every question blank.
V411_NJ1 = V411(68198477)
more("NJ-H-01", "NJ-H-01:galdo",
     ("agr-05", 1, V411_NJ1("Galdo would strengthen supply chains at home"), "We should also strengthen supply chains here at home to reduce reliance on foreign countries."),
     ("hea-06", 1, V411_NJ1("Galdo wants better access to mental health services"), "We need better access to mental health services, especially for veterans, first responders, and young people."),
     ("ene-08", 1, V411_NJ1("Galdo would invest in flood control and stormwater systems"), "That includes investing in flood control, stormwater systems, and resilient construction practices."))
V411_NJ4 = V411(68198481)
more("NJ-H-04", "NJ-H-04:peace",
     ("eco-11", 2, V411_NJ4("Peace says the country needs paid family leave"), "That’s why we need paid family leave, so that parents can be there for their child during the critical stages of development"),
     ("soc-07", 1, V411_NJ4("Peace would expand pre-K from age three as child care costs soar"), "With childcare more costly than a mortgage, parents need the option to return to work"),
     ("eco-03", 1, V411_NJ4("Peace will advocate for living wages"), "I’ll advocate for living wages for everyone, adjusting for inflation and geographic realities."),
     ("hou-05", 1, V411_NJ4("Peace would widen home-buying assistance programs"), "I’d like to increase income limits for programs that reduce financial barriers to home ownership"),
     ("hea-01", 1, V411_NJ4("Peace says everyone should be able to see a doctor when sick"), "Our campaign is grounded in the premise that everyone should be able to see the doctor when they are sick."),
     ("imm-09", 1, V411_NJ4("Peace proposes a “missing middle” work visa"), "Meaningful reform should include the creation of a “missing middle” visa and job portal."),
     ("imm-08", -1, V411_NJ4("Peace would shift resources from detention to community alternatives"), "Reallocating resources toward these alternatives could improve outcomes for individuals and reduce strain on taxpayers."),
     ("soc-03", 2, V411_NJ4("Peace says reproductive care must be accessible to all"), "Reproductive care must be accessible regardless of income, geography, sex/gender, documentation, or insurance status."),
     ("ene-01", 2, V411_NJ4("Peace says clean energy must expand"), "we must expand clean energy and promote transit-oriented development to reduce pollution and congestion"),
     ("soc-02", 1, V411_NJ4("Peace would restore and strengthen the Voting Rights Act"), "We must restore and strengthen the Voting Rights Act"),
     ("gov-07", 1, V411_NJ4("Peace supports ranked-choice voting"), "I support open primaries and ranked choice voting."),
     ("gov-11", 2, V411_NJ4("Peace would overturn Citizens United and eliminate dark money and PACs"), "overturn Citizens United, eliminate dark money, PACs, Super PACs, foreign and domestic lobbies"),
     ("gov-13", -2, V411_NJ4("Peace would overturn Citizens United"), None),
     ("gov-03", 2, V411_NJ4("Peace would strengthen disclosure of donations"), "strengthen disclosure requirements for donations"),
     ("gov-09", 2, V411_NJ4("Peace would strengthen ethics enforcement"), "Finally, we must strengthen ethics enforcement for elected officials."))
V411_NJ12 = V411(68198489)
more("NJ-H-12", "NJ-H-12:jinete",
     ("eco-03", 2, V411_NJ12("Jinete would raise the minimum wage to $25"), "The time has come to raise the minimum wage to $25 an hour and index it to inflation"),
     ("hou-01", 2, V411_NJ12("Jinete wants income-based public housing"), "We need income-based public housing."),
     ("hea-01", 2, V411_NJ12("Jinete wants universal health care through Medicare for everyone"), "We believe in creating a universal healthcare system by expanding medicare to cover everyone, regardless of status."),
     ("hea-03", 2, V411_NJ12("Jinete would expand Medicare to everyone"), "We believe in creating a universal healthcare system by expanding medicare to cover everyone, regardless of status."),
     ("edu-05", 1, V411_NJ12("Jinete supports student debt relief"), "We support national rent control, social housing, a $25 minimum wage, universal healthcare, student debt relief, free college"),
     ("edu-02", 2, V411_NJ12("Jinete supports free college"), "We support national rent control, social housing, a $25 minimum wage, universal healthcare, student debt relief, free college"),
     ("imm-08", -2, V411_NJ12("Jinete would dismantle ICE and DHS"), "Both of these agencies need to be dismantled."),
     ("imm-02", 2, V411_NJ12("Jinete wants a general amnesty"), "We need a general amnesty that provides paths of legalization for those are already here"),
     ("soc-03", 2, V411_NJ12("Jinete supports abortion access paid for by the state"), "We are staunch supporters of every person's right to bodily autonomy and access to ALL healthcare, including abortion, paid for by the state."),
     ("ene-01", 2, V411_NJ12("Jinete says renewable energy must scale up quickly"), "For this end, renewable energy has to scale up quickly."),
     ("ene-03", -2, V411_NJ12("Jinete says fossil fuels can no longer power the economy"), "Fossil fuels can no longer power the economies of the global north."),
     ("gov-07", 1, V411_NJ12("Jinete’s Green Party backs ranked-choice voting"), "The Green Party has been a long-time supported of ranked choice voting and multi-member districts."),
     ("gov-11", 1, V411_NJ12("Jinete would limit PAC spending and publicly fund elections"), "limiting campaign spending for PACs and publicly funding our elections"))

write("data/research/house_challengers.json",
      [{"id": rid, "partial": True, "candidates": cands} for rid, cands in RACES.items()],
      "Bios and positions for House challengers and third-party candidates, from their campaign sites and newsroom questionnaires, researched Oct. 26, 2026.", updated=READ)
