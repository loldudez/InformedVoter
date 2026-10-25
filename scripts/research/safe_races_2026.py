"""Researched positions for safe 2026 Senate races (incumbents and challengers),
and for senators running for governor. Writes data/research/safe-races.json.

Senators' positions come from their key Senate votes as Ballotpedia lists them
(read Oct. 25, 2026), turned into questionnaire answers by the same rules as the
House votes (see SENATE_RULES in common.py); Ballotpedia shows only 2025 votes
for Hickenlooper. Debate and campaign coverage adds statements, and is the only
source for challengers. Researched Oct. 25, 2026.

    py scripts/research/safe_races_2026.py
"""

from common import P, article, combine, page, senate_vote_positions, write

READ = "2026-10-25"
BP = "https://ballotpedia.org/"


def senator(cid, name, last, party, bio, page, votes, *rows):
    """A senator: key-vote positions, overridden where `rows` (sourced statements)
    answer the same question."""
    auto = senate_vote_positions(last, BP + page, votes, READ)
    if cid.split(":")[0].endswith("-GOV"):
        auto = [r for r in auto if not r[0].startswith("def-")]  # state races don't ask foreign policy
    return {"id": cid, "name": name, "party": party, "bio": bio, "positions": P(*combine(auto, *rows))}


def candidate(cid, name, party, bio, *rows):
    out = {"id": cid, "name": name, "party": party, "positions": P(*rows)}
    if bio:
        out["bio"] = bio
    return out


CO_GUIDE = article("Colorado Politics, Oct. 2, 2026", "https://www.coloradopolitics.com/2026/10/02/mark-baisley-john-hickenlooper-us-senate/", "2026-10-02")
ID_SUN = article("Idaho Capital Sun, Aug. 5, 2026", "https://idahocapitalsun.com/2026/08/05/risch-v-achilles-may-be-idahos-most-competitive-us-senate-race-in-years-heres-where-they-stand/", "2026-08-05")
AR_DEBATE = article("Talk Business & Politics debate report, Oct. 12, 2026", "https://talkbusiness.net/2026/10/shoffner-wadlin-hold-senate-debate-cotton-a-no-show/", "2026-10-12")
DE_FOX = article("Fox News, Sept. 15, 2026", "https://www.foxnews.com/politics/gop-anesthesiologist-receives-nod-uphill-race-challenge-top-senate-democrat", "2026-09-15")
MA_DEBATE = article("WBUR debate report, Oct. 14, 2026", "https://www.wbur.org/news/2026/10/14/senate-markey-deaton-debate-trump-healthcare-energy-massachusetts", "2026-10-14")
KY_DEBATE = article("WKYT debate report, Oct. 19, 2026", "https://www.fox19.com/2026/10/20/barr-booker-clash-prices-surveillance-cameras-mcconnells-legacy/", "2026-10-19")
NM_SOURCE = article("Source NM candidate interviews, Sept. 11, 2026", "https://sourcenm.com/2026/09/11/new-mexico-election-2026-us-senator/", "2026-09-11")
IL_DEBATE = article("Chicago Sun-Times debate report, Oct. 21, 2026", "https://www.wbez.org/government-politics/elections/2026/10/21/takeaways-senate-debate-juliana-stratton-don-tracy-midterm-election", "2026-10-21")
RI_CHART = article("ecoRI News candidate chart, Aug. 2026", "https://ecori.org/wp-content/uploads/2026/08/2026-Senator-Candidate-Charts.pdf", "2026-08-23")
SD_NEWS = article("Dakota News Now, Sept. 3, 2026", "https://www.dakotanewsnow.com/2026/09/04/bengs-continues-call-out-rounds-focusing-big-money-avoiding-debates/", "2026-09-03")
AL_SPEECH = article("Alabama Reflector, July 27, 2026", "https://alabamareflector.com/2026/07/27/doug-jones-calls-for-affordability-measures-government-reforms-in-policy-speech/", "2026-07-27")
OR_OTI = lambda note: page(f"OnTheIssues, David Brock Smith: {note}", "https://ontheissues.org/Senate/David_Brock_Smith.htm", READ)  # noqa: E731
TN_SITE = lambda note: page(f"Marquita Bradshaw campaign site: {note}", "https://www.marquitabradshaw.com/priorities", READ)  # noqa: E731
TN_NC5 = lambda note: page(f"NewsChannel 5 interview: {note}", "https://www.newschannel5.com/plus/inside-politics/election-2026-tn-governors-race-jerri-green", READ)  # noqa: E731


R_VOTES = dict  # each call is one senator's key votes as Ballotpedia shows them

races = [
    {"id": "AR-SEN", "candidates": [senator(
        "AR-SEN:cotton", "Tom Cotton", "Cotton", "R",
        "U.S. senator from Arkansas since 2015, chair of the Senate Republican Conference and an Army veteran.", "Tom_Cotton",
        R_VOTES(rfma="Nay", whpa="Nay", ira="Nay", iija="Nay", chips="Nay", obbba="Yea", supp2024="Yea", laken="Yea", ftv="Nay", border2024="Nay", esg="Yea", pact="Yea")),
        candidate(
            "AR-SEN:shoffner", "Hallie Shoffner", "D", "Arkansas farmer.",
            ("agr-01", 1, AR_DEBATE("Shoffner would make passing a full Farm Bill a top priority"), None),
            ("eco-10", 0, AR_DEBATE("Shoffner says blanket tariffs don't work but targeted ones can help"), "Blanket tariffs don't work as an economic development tool"),
            ("def-15", -1, AR_DEBATE("Shoffner criticizes the Iran war's cost at the pump"), "now we are paying for it at the pump"),
            ("imm-07", 1, AR_DEBATE("Shoffner supports legal immigration and deporting violent criminals"), None),
            ("imm-08", -1, AR_DEBATE("Shoffner opposes heavy-handed immigration enforcement"), None))]},
    {"id": "CO-SEN", "candidates": [senator(
        "CO-SEN:hickenlooper", "John Hickenlooper", "Hickenlooper", "D",
        "U.S. senator from Colorado since 2021 and governor of Colorado from 2011 to 2019.", "John_Hickenlooper",
        R_VOTES(obbba="Nay", laken="Nay"),
        ("hea-01", 1, CO_GUIDE("Hickenlooper would reverse the federal health care cuts"), "set the table for universal coverage"),
        ("hea-02", 1, CO_GUIDE("Hickenlooper touts letting Medicare negotiate drug prices and the $35 insulin cap"), None),
        ("eco-10", -2, CO_GUIDE("Hickenlooper opposes the administration's tariffs"), "illegal tariffs that are increasing gas and grocery prices"),
        ("def-15", -2, CO_GUIDE("Hickenlooper would end the war with Iran"), None),
        ("ene-06", 2, CO_GUIDE("Hickenlooper would fight climate change and cites backing the largest climate bill ever"), None),
        ("imm-08", -1, CO_GUIDE("Hickenlooper would go after ICE's violence"), None),
        ("gov-06", 1, CO_GUIDE("Hickenlooper would reject voter suppression efforts"), None)),
        candidate(
            "CO-SEN:baisley", "Mark Baisley", "R", "Colorado state senator with a background in aerospace.",
            ("hou-05", 1, CO_GUIDE("Baisley would give lenders incentives so first-time buyers get mortgage rates tied to the 10-year Treasury yield"), None),
            ("eco-07", 1, CO_GUIDE("Baisley would shrink government to restore affordability"), "reducing the footprint of government"))]},
    {"id": "DE-SEN", "candidates": [senator(
        "DE-SEN:coons", "Chris Coons", "Coons", "D",
        "U.S. senator from Delaware since 2010.", "Chris_Coons",
        R_VOTES(rfma="Yea", whpa="Yea", ira="Yea", iija="Yea", chips="Yea", obbba="Nay", supp2024="Yea", laken="Nay", ftv="Yea", border2024="Yea", esg="Nay", pact="Yea")),
        candidate(
            "DE-SEN:katz", "Michael Katz", "R", "Anesthesiologist and former Delaware state senator.",
            ("eco-07", 1, DE_FOX("Katz would cut federal spending"), None))]},
    {"id": "ID-SEN", "candidates": [senator(
        "ID-SEN:risch", "Jim Risch", "Risch", "R",
        "U.S. senator from Idaho since 2009 and a former governor of Idaho.", "Jim_Risch",
        R_VOTES(rfma="Nay", whpa="Nay", ira="Nay", iija="Yea", chips="Nay", obbba="Yea", supp2024="Yea", laken="Yea", ftv="Nay", border2024="Nay", esg="Yea", pact="Nay"),
        ("hea-04", 2, ID_SUN("Risch says the ACA is a mess and health care must move back into the private sector"), "moved significantly more back into the private sector"),
        ("gov-05", 2, ID_SUN("Risch backs the SAVE Act's proof-of-citizenship rules"), "I'm all in on the Save Act."),
        ("imm-09", 2, ID_SUN("Risch wants the H-2A farm worker visa opened to year-round work"), None),
        ("imm-02", -2, ID_SUN("Risch opposes a path to citizenship for people who entered illegally"), "That is a non-starter for us")),
        candidate(
            "ID-SEN:achilles", "Todd Achilles", "I", "Former Idaho state representative and Army tank commander, running as an independent.",
            ("hea-07", 1, ID_SUN("Achilles criticized Congress for letting the enhanced ACA tax credits expire and wants the ACA reformed"), None),
            ("gov-05", -1, ID_SUN("Achilles calls the SAVE Act's proof-of-citizenship rules federal overreach"), "The SAVE Act is federal overreach"),
            ("imm-01", 1, ID_SUN("Achilles backs the approach of the 2013 bipartisan immigration bill, which boosted border enforcement"), None))]},
    {"id": "MA-SEN", "candidates": [senator(
        "MA-SEN:markey", "Ed Markey", "Markey", "D",
        "U.S. senator from Massachusetts since 2013, after 37 years in the U.S. House.", "Ed_Markey",
        R_VOTES(rfma="Yea", whpa="Yea", ira="Yea", iija="Yea", chips="Yea", obbba="Nay", supp2024="Yea", laken="Nay", ftv="Yea", border2024="Nay", esg="Nay", pact="Yea"),
        ("hea-01", 2, MA_DEBATE("Markey supports Medicare for All"), None),
        ("hea-04", -2, MA_DEBATE("Markey supports Medicare for All"), None),
        ("ene-06", 2, MA_DEBATE("Markey sponsors the Green New Deal"), "break our dependence upon that fossil fuel monopoly"),
        ("ene-01", 2, MA_DEBATE("Markey wants the administration's halt of offshore wind projects reversed"), None)),
        candidate(
            "MA-SEN:deaton", "John Deaton", "R", "Marine veteran and trial attorney; the 2024 Republican nominee against Sen. Elizabeth Warren.",
            ("hea-04", 1, MA_DEBATE("Deaton calls Medicare for All unrealistic"), None),
            ("eco-04", 1, MA_DEBATE("Deaton would lower health costs by breaking up large insurance companies"), None),
            ("ene-02", 2, MA_DEBATE("Deaton proposes small modular nuclear reactors in Massachusetts"), "four small modular reactors and expands natural gas in Massachusetts"),
            ("ene-03", 1, MA_DEBATE("Deaton would expand natural gas in Massachusetts"), None),
            ("ene-10", 1, MA_DEBATE("Deaton says the Green New Deal's mandates drive up energy prices"), None),
            ("def-15", -1, MA_DEBATE("Deaton breaks with the president on the Iran war"), None),
            ("eco-10", -1, MA_DEBATE("Deaton breaks with the president on tariffs"), None))]},
    {"id": "NM-SEN", "candidates": [senator(
        "NM-SEN:lujan", "Ben Ray Luján", "Luján", "D",
        "U.S. senator from New Mexico since 2021 and earlier a U.S. representative.", "Ben_Ray_Luj%C3%A1n",
        R_VOTES(rfma="Yea", ira="Yea", iija="Yea", chips="Yea", obbba="Nay", supp2024="Yea", laken="Nay", ftv="Yea", border2024="Yea", esg="Nay", pact="Yea"),
        ("eco-10", -1, NM_SOURCE("Luján says the administration's tariffs are arbitrarily hurting New Mexicans"), None),
        ("imm-01", 1, NM_SOURCE("Luján backs screening everything crossing the southern border, inbound and outbound"), "We need to have smart immigration policy and strong border security in America."),
        ("gov-06", 1, NM_SOURCE("Luján says Republicans are trying to end voting by mail"), None),
        ("agr-01", 1, NM_SOURCE("Luján is working on a bipartisan farm bill supporting food programs, farmers and ranchers"), None),
        ("hea-03", 1, NM_SOURCE("Luján says the 2025 budget law, with its Medicaid cuts, made New Mexico families sicker and poorer"), None)),
        candidate(
            "NM-SEN:marker", "Larry Marker", "R", "Roswell oil and gas businessman.",
            ("eco-07", 1, NM_SOURCE("Marker calls the national debt the biggest issue"), None),
            ("def-04", 1, NM_SOURCE("Marker says the Constitution meant to limit the president's power to wage war and Congress must act on Iran"), None),
            ("eco-10", -1, NM_SOURCE("Marker says the president lacks the constitutional authority to levy tariffs"), None),
            ("imm-01", 2, NM_SOURCE("Marker on the border"), "We need a very, very strong, secure border"),
            ("imm-03", 1, NM_SOURCE("Marker wants a legal way to immigrate that isn't cumbersome or expensive"), None),
            ("ene-03", 2, NM_SOURCE("Marker would support the oil and gas industry and rebuild mining"), None))]},
    {"id": "KY-SEN", "candidates": [
        candidate(
            "KY-SEN:barr", "Andy Barr", "R", "U.S. representative for Kentucky's 6th District since 2013.",
            ("eco-01", -1, KY_DEBATE("Barr backed the 2025 tax cut law"), "I supported the largest tax cut in American history"),
            ("ene-03", 2, KY_DEBATE("Barr would lower prices through American energy dominance and more fossil fuel production"), None),
            ("def-15", 2, KY_DEBATE("Barr says victory is the exit strategy in Iran"), None)),
        candidate(
            "KY-SEN:booker", "Charles Booker", "D", "Former Kentucky state representative and the 2022 Democratic Senate nominee.",
            ("def-15", -2, KY_DEBATE("Booker would end the Iran war"), "stopping the madness in Iran"),
            ("soc-08", 1, KY_DEBATE("Booker opposes Flock surveillance cameras"), None))]},
    {"id": "IL-SEN", "candidates": [
        candidate(
            "IL-SEN:stratton", "Juliana Stratton", "D", "Lieutenant governor of Illinois since 2019.",
            ("eco-03", 2, IL_DEBATE("Stratton supports a $25 federal minimum wage"), "livable wage, not just the bare minimum"),
            ("eco-01", 2, IL_DEBATE("Stratton supports a millionaire's tax"), None),
            ("imm-08", -2, IL_DEBATE("Stratton would abolish ICE"), None),
            ("imm-02", 2, IL_DEBATE("Stratton wants a path to citizenship"), "real path to legal citizenship, including for Dreamers"),
            ("eco-10", -2, IL_DEBATE("Stratton calls the administration's tariffs illegal and wants refunds sent to people"), None)),
        candidate(
            "IL-SEN:tracy", "Don Tracy", "R", "Former chair of the Illinois Republican Party.",
            ("eco-03", -2, IL_DEBATE("Tracy opposes a $25 minimum wage"), "a death sentence for small businesses everywhere"),
            ("eco-10", 1, IL_DEBATE("Tracy sees tariffs as a tool to reset world trade"), "a tool to reset world trade policy"),
            ("imm-08", 1, IL_DEBATE("Tracy praises cooperation between local police and federal immigration agents"), None))]},
    {"id": "OR-SEN", "candidates": [senator(
        "OR-SEN:merkley", "Jeff Merkley", "Merkley", "D",
        "U.S. senator from Oregon since 2009.", "Jeff_Merkley",
        R_VOTES(rfma="Yea", whpa="Yea", ira="Yea", iija="Yea", chips="Yea", obbba="Nay", supp2024="Nay", laken="Nay", ftv="Yea", border2024="Yea")),
        candidate(
            "OR-SEN:smith", "David Brock Smith", "R", "Oregon state senator from the south coast.",
            ("gov-06", -2, OR_OTI("Smith sponsored a bill to end Oregon's vote-by-mail system (March 2026)"), None),
            ("imm-08", 1, OR_OTI("Smith opposes Oregon's sanctuary state status (April 2026)"), None),
            ("eco-01", -1, OR_OTI("Smith pledges no new taxes (May 2026)"), None),
            ("eco-07", 1, OR_OTI("Smith would cut unnecessary government spending (May 2026)"), None),
            ("cri-01", 1, OR_OTI("Smith backs law enforcement and accountability for repeat offenders (May 2026)"), None))]},
    {"id": "RI-SEN", "candidates": [senator(
        "RI-SEN:reed", "Jack Reed", "Reed", "D",
        "U.S. senator from Rhode Island since 1997 and an Army veteran.", "Jack_Reed",
        R_VOTES(rfma="Yea", whpa="Yea", ira="Yea", iija="Yea", chips="Yea", obbba="Nay", supp2024="Yea", laken="Nay", ftv="Yea", border2024="Yea", esg="Nay", pact="Yea"),
        ("ene-06", 2, RI_CHART("Reed backs a national energy policy that limits carbon pollution"), None),
        ("ene-01", 2, RI_CHART("Reed has pushed for offshore wind and clean, renewable energy and opposed the administration's offshore wind buyouts"), None),
        ("ene-04", 1, RI_CHART("Reed has fought efforts to weaken the Clean Water Act"), None),
        ("hou-03", 2, RI_CHART("Reed has pushed for national public transit funding"), None)),
        candidate(
            "RI-SEN:mckay", "Raymond McKay", "R", "Former member of the Rhode Island Republican Party's state committee.",
            ("ene-01", -1, RI_CHART("McKay says offshore wind hurts fishers and ruins Rhode Island's views"), None),
            ("ene-10", 1, RI_CHART("McKay blames energy policies adopted for environmental reasons for high energy costs"), "under the guise of environmental responsibility"))]},
    {"id": "SD-SEN", "candidates": [senator(
        "SD-SEN:rounds", "Mike Rounds", "Rounds", "R",
        "U.S. senator from South Dakota since 2015 and governor of South Dakota from 2003 to 2011.", "Mike_Rounds",
        R_VOTES(rfma="Nay", whpa="Nay", ira="Nay", chips="Nay", obbba="Yea", supp2024="Yea", laken="Yea", ftv="Nay", border2024="Nay", esg="Yea", pact="Yea")),
        candidate(
            "SD-SEN:bengs", "Brian Bengs", "I", "Air Force veteran running as an independent; the 2022 Democratic Senate nominee.",
            ("gov-11", 2, SD_NEWS("Bengs is running on getting money out of politics"), "getting money out of politics"))]},
    {"id": "TN-SEN", "candidates": [senator(
        "TN-SEN:hagerty", "Bill Hagerty", "Hagerty", "R",
        "U.S. senator from Tennessee since 2021 and U.S. ambassador to Japan from 2017 to 2019.", "Bill_Hagerty",
        R_VOTES(rfma="Nay", whpa="Nay", ira="Nay", iija="Nay", chips="Yea", obbba="Yea", supp2024="Nay", laken="Yea", ftv="Nay", esg="Yea", pact="Yea")),
        candidate(
            "TN-SEN:bradshaw", "Marquita Bradshaw", "D", "Memphis environmental activist and the 2020 Democratic Senate nominee.",
            ("edu-01", 1, TN_SITE("Bradshaw supports well-funded public schools"), "Every student deserves a well-funded public school"),
            ("edu-04", 1, TN_SITE("Bradshaw supports competitive teacher pay"), None),
            ("hou-01", 1, TN_SITE("Bradshaw would expand affordable housing"), None),
            ("hou-05", 1, TN_SITE("Bradshaw would help first-time homebuyers"), None),
            ("hea-01", 1, TN_SITE("Bradshaw says health care is a right"), "Healthcare should serve people, not profits."),
            ("hea-06", 1, TN_SITE("Bradshaw would expand mental health services"), None),
            ("gov-04", 2, TN_SITE("Bradshaw supports independent redistricting to end gerrymandering"), None),
            ("hou-09", 2, TN_SITE("Bradshaw wants affordable high-speed internet for every Tennessean, especially rural areas"), None),
            ("ene-01", 1, TN_SITE("Bradshaw promotes clean energy"), None),
            ("ene-04", 1, TN_SITE("Bradshaw would reduce pollution"), "Every community deserves clean air, safe water"))]},
    {"id": "WV-SEN", "candidates": [senator(
        "WV-SEN:capito", "Shelley Moore Capito", "Capito", "R",
        "U.S. senator from West Virginia since 2015, after 14 years in the U.S. House.", "Shelley_Moore_Capito",
        R_VOTES(rfma="Yea", whpa="Nay", ira="Nay", iija="Yea", chips="Yea", obbba="Yea", supp2024="Yea", laken="Yea", ftv="Nay", border2024="Nay", esg="Yea", pact="Yea"))]},
    {"id": "AL-GOV", "candidates": [senator(
        "AL-GOV:tuberville", "Tommy Tuberville", "Tuberville", "R",
        "U.S. senator from Alabama since 2021 and a former college football coach.", "Tommy_Tuberville",
        R_VOTES(rfma="Nay", whpa="Nay", ira="Nay", iija="Nay", chips="Nay", obbba="Yea", laken="Yea", ftv="Nay", esg="Yea", pact="Nay")),
        candidate(
            "AL-GOV:jones", "Doug Jones", "D", "U.S. senator from Alabama from 2018 to 2021 and a former U.S. attorney.",
            ("hea-03", 2, AL_SPEECH("Jones would expand Medicaid one way or another"), "Medicaid expansion is not a handout, it's a hand up"),
            ("eco-02", 2, AL_SPEECH("Jones would end Alabama's taxes on groceries, tips and overtime"), None),
            ("gov-10", 2, AL_SPEECH("Jones would create a citizen ballot initiative process"), None),
            ("gov-06", 2, AL_SPEECH("Jones would bring early voting to Alabama"), None),
            ("eco-11", 1, AL_SPEECH("Jones will fight for paid family leave"), None),
            ("soc-07", 1, AL_SPEECH("Jones would invest in affordable child care"), None),
            ("hou-01", 1, AL_SPEECH("Jones would invest more in housing"), None))]},
    {"id": "TN-GOV", "candidates": [senator(
        "TN-GOV:blackburn", "Marsha Blackburn", "Blackburn", "R",
        "U.S. senator from Tennessee since 2019, after 16 years in the U.S. House.", "Marsha_Blackburn",
        R_VOTES(rfma="Nay", whpa="Nay", ira="Nay", iija="Nay", chips="Nay", obbba="Yea", supp2024="Nay", laken="Yea", ftv="Nay", border2024="Nay", esg="Yea", pact="Yea")),
        candidate(
            "TN-GOV:green", "Jerri Green", "D", None,
            ("eco-02", 2, TN_NC5("Green would end Tennessee's grocery tax"), "We need to end the grocery tax"),
            ("edu-06", -2, TN_NC5("Green opposes school vouchers"), "vouchers are failing our public school students"),
            ("sta-02", 2, TN_NC5("Green would fully fund public schools"), None),
            ("gov-11", 1, TN_NC5("Green says she takes no money from dark money donors or special interests"), None))]},
]

write("data/research/safe-races.json", races, "Incumbent senators in safe races, and senators running for governor, from their key Senate votes; researched Oct. 25, 2026.", updated=READ)
