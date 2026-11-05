"""Researched positions for candidates for statewide offices below governor (attorney
general, secretary of state, lieutenant governor, treasurer, auditor or comptroller),
from the States Newsroom voter guides' statewide contest pages, read Nov. 4, 2026.
Writes data/research/offices.json, merged into data/offices.json by update_races.py.

The guides come in three kinds, named in each source:
  - candidates' own survey answers ("Key messages", "Policy passions" and the like),
    first published by Ballotpedia and republished with permission;
  - the newsroom's interviews, with the candidates' quotes;
  - the newsroom's summary of each platform (cited, never quoted).
A stance goes in only where the candidate's words (or the summary of them) answer the
question as worded; endorsements, records the guide doesn't describe and party never
count. Anything else stays "unclear". Quotes are verbatim, at most 25 words, checked
against the cached page text.

A race whose main candidates (the Democrat and the Republican, or the top two where
the field differs) all have positions here is marked researched, which switches on
side-by-side matching, as for any race; otherwise the entry is `partial`. Below five
compared questions no match percentage is shown, as everywhere on the site.

    py scripts/research/offices_2026.py
"""

from common import P, page, write

READ = "2026-11-04"

ANSWERS = "candidates’ survey answers, first published by Ballotpedia"
INTERVIEWS = "the newsroom’s interviews with the candidates"
SUMMARY = "the newsroom’s summary of each platform"
POSITIONS = "the newsroom’s summary of each candidate’s record and statements"


def sn(outlet, url, kind):
    return lambda note: page(f"{outlet} voter guide ({kind}): {note}", url, READ)


RACES = {}
MAIN = {}  # race -> the ids of its main candidates


def cand(race, cid, name, party, bio, *rows, **fields):
    out = {"id": f"{race}:{cid}", "name": name, "party": party, **fields}
    if bio:
        out["bio"] = bio
    if rows:
        out["positions"] = P(*rows)
    assert not any(c["id"] == out["id"] for c in RACES.get(race, [])), out["id"]
    RACES.setdefault(race, []).append(out)


def main(race, *cids):
    MAIN[race] = [f"{race}:{c}" for c in cids]


# Alabama ---------------------------------------------------------------------------
AL_AUD = sn("Alabama Reflector", "https://alabamareflector.com/voter-guides/contests/alstateauditor/", SUMMARY)
cand("AL-AUD", "edwards", "Violet Edwards", "D", None,
     ("gov-12", 1, AL_AUD("Edwards would bring transparency to the state auditor’s office"), None))
main("AL-AUD", "sorrell", "edwards")

AL_TREAS = sn("Alabama Reflector", "https://alabamareflector.com/voter-guides/contests/alstatetreasurer/", SUMMARY)
cand("AL-TREAS", "houston", "Rosilyn Houston", "D", "Banking executive.",
     ("gov-12", 1, AL_TREAS("Houston would modernize the treasurer’s office to improve transparency on the spending of state funds"), None))
main("AL-TREAS", "boozer", "houston")

# Arizona ---------------------------------------------------------------------------
AZ_AG = sn("Arizona Mirror", "https://azmirror.com/voter-guides/contests/attorney-general/", ANSWERS)
cand("AZ-AG", "mayes", "Kris Mayes", "D", None,
     ("soc-03", 2, AZ_AG("Mayes says she fought to protect access to reproductive care"), "She fought to protect access to reproductive care"),
     ("soc-08", 1, AZ_AG("Mayes says she has defended Arizonans’ private personal data"), "defend Arizonan’s private personal data"),
     ("eco-09", 2, AZ_AG("Mayes created the state’s first Worker Protection Unit to investigate wage theft and defended prevailing wage laws"), "She created the state's first Worker Protection Unit to investigate wage theft and other workplace abuses."),
     ("eco-04", 1, AZ_AG("Mayes sued landlords over alleged rent collusion and blocked the Albertsons-Kroger merger"), "She sued RealPage and eight major landlords for colluding to artificially inflate rent across Arizona."),
     ("eco-10", -1, AZ_AG("Mayes counts overturning tariffs she calls illegal among her wins"), "overturning illegal tariffs costing Arizonans an average $1,500 a year"))
cand("AZ-AG", "petersen", "Warren Petersen", "R", None,
     ("imm-01", 1, AZ_AG("Petersen wants to secure the border through measures like the Border Security Act"), "securing the border through measures like the Border Security Act"),
     ("sta-06", 1, AZ_AG("Petersen promises to eliminate corruption through transparency and accountability"), "Eliminating corruption starts with transparency and accountability at the highest levels of our state agencies."),
     ("gov-12", 2, AZ_AG("Petersen would review state contracts so every tax dollar is spent legally and ethically"), "conduct a review of state contracts and regulatory decisions to ensure that every dollar of your tax money is spent legally and ethically"))
main("AZ-AG", "mayes", "petersen")

AZ_SOS = sn("Arizona Mirror", "https://azmirror.com/voter-guides/contests/secretary-of-state/", POSITIONS)
cand("AZ-SOS", "fontes", "Adrian Fontes", "D", None,
     ("gov-06", 2, AZ_SOS("Fontes would expand mail, early and in-person voting and backed a longer early voting period"), "Mail-in voting has been a cornerstone of secure and accessible elections."))
cand("AZ-SOS", "kolodin", "Alexander Kolodin", "R", None,
     ("gov-06", -2, AZ_SOS("Kolodin introduced a ballot measure to end the Active Early Voter List and shorten early voting"), None))
main("AZ-SOS", "fontes", "kolodin")

# Colorado --------------------------------------------------------------------------
CO_TREAS = sn("Colorado Newsline", "https://coloradonewsline.com/voter-guides/contests/2026-general-colorado-treasurer/", SUMMARY)
cand("CO-TREAS", "bridges", "Jeff Bridges", "D", None,
     ("hou-01", 1, CO_TREAS("Bridges would invest some state money in housing, infrastructure and clean energy"), None),
     ("ene-01", 1, CO_TREAS("Bridges would invest some state money in clean energy"), None))
main("CO-TREAS", "bridges", "grantham")

# Georgia ---------------------------------------------------------------------------
GA_AG = sn("Georgia Recorder", "https://georgiarecorder.com/voter-guides/contests/2026-attorney-general/", INTERVIEWS)
cand("GA-AG", "miller", "Tanya F. Miller", "D",
     "Lawyer and former Fulton County homicide prosecutor; state representative since 2023 and chair of the House Democratic Caucus.",
     ("eco-04", 1, GA_AG("Miller would investigate corporations that collude on prices or violate antitrust rules"), "violating antitrust rules and rigging the economy against working and middle class folks, they need to be held to account"),
     ("ene-04", 1, GA_AG("Miller would hold corporations to account for ignoring environmental regulations and poisoning water"), "ignoring environmental regulations and poisoning our water with forever chemicals"),
     ("gov-12", 2, GA_AG("Miller would extend the Open Records Act to the Legislature"), "Lawmakers who make decisions about how to spend taxpayer money should not be the only Georgians exempt from the sunshine."),
     ("sta-06", 1, GA_AG("Miller would push to extend the Open Records Act to legislators’ offices"), "I think the act should be extended to the House, the Senate, their offices, including my own chamber"))
cand("GA-AG", "strickland", "Brian Strickland", "R",
     "Lawyer from McDonough; in the Legislature since 2013, now a state senator and chair of the Senate Judiciary Committee.",
     ("gov-12", 1, GA_AG("Strickland would make the attorney general’s office a leader on enforcing open records laws"), "We have to make sure that local governments, in particular, are not acting in secret"),
     ("soc-08", 1, GA_AG("Strickland wants greater oversight of tech companies and protections for users, especially children"), "We also have to hold Big Tech accountable."))
main("GA-AG", "miller", "strickland")

GA_LG = sn("Georgia Recorder", "https://georgiarecorder.com/voter-guides/contests/2026-lieutenant-governor/", INTERVIEWS)
cand("GA-LG", "dolezal", "Greg Dolezal", "R",
     "Business owner from Cumming; state senator and chair of the Senate Transportation Committee.",
     ("edu-06", 1, GA_LG("Dolezal points to the Georgia Promise Scholarship, state money for private school or homeschooling, as a good example of lawmaking"), None),
     ("eco-07", 1, GA_LG("Dolezal would prioritize cutting government spending"), "We can ensure that we right-size government"),
     ("eco-02", 1, GA_LG("Dolezal cites state income tax cuts, gas tax suspensions and property tax refunds as making Georgia affordable"), "All of those things are directly putting money into the pockets of average Georgians"),
     ("sta-04", 2, GA_LG("Dolezal centered his campaign on cutting property taxes"), None))
cand("GA-LG", "mclaurin", "Josh McLaurin", "D",
     "Attorney from Sandy Springs; state legislator since 2019, now a state senator.",
     ("hea-03", 2, GA_LG("McLaurin would expand Medicaid under the ACA and use state money to replace lost subsidies"), "I am not only an advocate of expanding Medicaid under the ACA, which my opponent is not"),
     ("soc-03", 2, GA_LG("McLaurin would repeal Georgia’s six-week abortion ban"), None),
     ("soc-04", -2, GA_LG("McLaurin would repeal Georgia’s six-week abortion ban"), None),
     ("hou-04", 1, GA_LG("McLaurin would push zoning and permitting reform to bring down the cost of building homes"), "modest zoning and design standard reform"))
main("GA-LG", "mclaurin", "dolezal")

GA_SOS = sn("Georgia Recorder", "https://georgiarecorder.com/voter-guides/contests/2026-secretary-of-state/", INTERVIEWS)
cand("GA-SOS", "reynolds", "Penny Brown Reynolds", "D",
     "Former Fulton County state judge; helped lead the civil rights office at the U.S. Department of Agriculture under President Biden.",
     ("gov-06", 1, GA_SOS("Brown Reynolds says voting by mail must stay an option"), "So voting by mail has to become and stay a viable alternative for people to vote."),
     ("gov-05", 1, GA_SOS("Brown Reynolds supports requiring voters to show identification"), "I believe that ID procedures that we have now have been working."))
cand("GA-SOS", "fleming", "Tim Fleming", "R",
     "State representative from Covington and former deputy secretary of state under Brian Kemp.",
     ("gov-06", -2, GA_SOS("Fleming would support limiting absentee ballots to elderly, disabled, military and overseas voters"), "I believe with all the opportunities we have to vote, we need to make it a priority to vote in person"))
main("GA-SOS", "reynolds", "fleming")

# Iowa ------------------------------------------------------------------------------
IA_AG = sn("Iowa Capital Dispatch", "https://iowacapitaldispatch.com/voter-guides/contests/2026-iowa-attorney-general/", SUMMARY)
cand("IA-AG", "willems", "Nathan Willems", "D",
     "Labor lawyer in Cedar Rapids; state representative from 2008 to 2012.",
     ("eco-09", 1, IA_AG("Willems would set up a wage theft recovery unit in the attorney general’s office"), None),
     ("ene-04", 1, IA_AG("Willems would seek meaningful penalties for companies polluting Iowa’s air and water"), None))
main("IA-AG", "bird", "willems")

IA_AUD = sn("Iowa Capital Dispatch", "https://iowacapitaldispatch.com/voter-guides/contests/2026-iowa-auditor-general/", SUMMARY)
cand("IA-AUD", "wettach", "Taylor Wettach", "D", None,
     ("gov-12", 1, IA_AUD("Wettach would reverse the 2023 law limiting the auditor’s access to information in investigations"), None))
main("IA-AUD", "wettach", "cournoyer")

IA_SOS = sn("Iowa Capital Dispatch", "https://iowacapitaldispatch.com/voter-guides/contests/2026-iowa-secretary-of-state/", SUMMARY)
cand("IA-SOS", "pate", "Paul Pate", "R", None,
     ("gov-05", 2, IA_SOS("Pate points to his support for and work on Iowa’s voter identification requirements"), None))
cand("IA-SOS", "peterman", "Ryan Peterman", "D", None,
     ("gov-06", 1, IA_SOS("Peterman opposes the changes that shortened Iowa’s early voting window"), None))
main("IA-SOS", "pate", "peterman")

IA_TREAS = sn("Iowa Capital Dispatch", "https://iowacapitaldispatch.com/voter-guides/contests/2026-iowa-treasurer/", SUMMARY)
cand("IA-TREAS", "smith", "Roby Smith", "R", None,
     ("edu-10", 1, IA_TREAS("Smith supports improving financial literacy education across the state"), None))
main("IA-TREAS", "smith", "norwood")

# Idaho (Idaho Capital Sun's questionnaire, candidates' own answers) -------------------
ID_AG = sn("Idaho Capital Sun", "https://idahocapitalsun.com/voter-guides/contests/2026-general-attorney-general/", "candidates’ answers to the newsroom’s questionnaire")
cand("ID-AG", "hickman", "Lori Hickman", "D", "Attorney in Boise.",
     ("soc-03", 2, ID_AG("Hickman supports Proposition 1, which would end Idaho’s strict abortion ban"), "I support Proposition 1"),
     ("soc-04", -1, ID_AG("Hickman supports Proposition 1, which would end Idaho’s strict abortion ban"), None),
     ("gov-10", 2, ID_AG("Hickman believes in voters’ right to propose ballot initiatives"), "I believe in respecting the right of Idaho voters to propose ballot initiatives and participate directly in our democratic process."),
     ("ene-02", 1, ID_AG("Hickman is open to strengthening Idaho’s role in nuclear energy, with enforceable protections"), "I am open to innovation and to strengthening Idaho’s role in nuclear energy"))
cand("ID-AG", "labrador", "Raúl Labrador", "R", None,
     ("soc-03", -2, ID_AG("Labrador opposes Proposition 1, which would end Idaho’s strict abortion ban"), "I oppose Proposition 1 because it is too extreme."),
     ("ene-02", 1, ID_AG("Labrador says Idaho should remain open to responsible nuclear innovation"), "Idaho should be proud of that legacy and remain open to responsible nuclear innovation."))
main("ID-AG", "labrador", "hickman")

ID_LG = sn("Idaho Capital Sun", "https://idahocapitalsun.com/voter-guides/contests/2026-general-lieutenant-governor/", "candidates’ answers to the newsroom’s questionnaire")
cand("ID-LG", "bedke", "Scott Bedke", "R", "Rancher from Oakley; the incumbent lieutenant governor.",
     ("sta-01", 1, ID_LG("Bedke would invest in water and transportation infrastructure"), "investing in water and transportation infrastructure"),
     ("hou-04", 1, ID_LG("Bedke would ease regulations and permitting barriers so the private sector builds more housing"), "addressing unnecessary regulations, permitting barriers, and infrastructure costs while respecting local communities"),
     ("edu-06", 1, ID_LG("Bedke wants families to have more choices in education"), "parents should have options when deciding what is best for their children"),
     ("soc-03", -1, ID_LG("Bedke opposes Proposition 1, which would end Idaho’s strict abortion ban"), "I oppose Proposition 1"))
cand("ID-LG", "myricks", "Eric Myricks", "D", "Entrepreneur from Nampa.",
     ("edu-04", 2, ID_LG("Myricks would push for teacher pay competitive with the region"), "I'll push for teacher pay that's competitive with the region"),
     ("edu-06", -2, ID_LG("Myricks would cap Idaho’s private school tax credit and work toward repealing it"), "I support capping the credit now and working toward repealing HB 93 over time."),
     ("eco-02", 1, ID_LG("Myricks would reduce or repeal Idaho’s sales tax on groceries"), "I'll work to reduce or repeal the tax."),
     ("soc-03", 2, ID_LG("Myricks supports Proposition 1, which would end Idaho’s strict abortion ban"), "Medical decisions belong between a woman and her doctor. The government has no place in the exam room."),
     ("soc-04", -2, ID_LG("Myricks supports Proposition 1, which would end Idaho’s strict abortion ban"), None),
     ("hou-04", 1, ID_LG("Myricks would let communities allow greater density and manufactured housing"), "letting communities allow greater density and manufactured housing where it makes sense"),
     ("eco-07", -1, ID_LG("Myricks opposes paying for tax cuts with across-the-board budget cuts"), "You can't build the roads and schools that growth demands on unrealistic, shrinking budgets."),
     ("sta-02", 1, ID_LG("Myricks would fight for rural school funding"), "I'd fight for rural school funding at least equal, per student, to the benefit flowing to urban and suburban areas."),
     ("edu-01", 1, ID_LG("Myricks would use his platform to support education funding"), None))
main("ID-LG", "bedke", "myricks")

ID_SOS = sn("Idaho Capital Sun", "https://idahocapitalsun.com/voter-guides/contests/2026-general-secretary-of-state/", "candidates’ answers to the newsroom’s questionnaire; Shawn Keenan did not respond")
cand("ID-SOS", "mcgrane", "Phil McGrane", "R", None,
     ("gov-06", 1, ID_SOS("McGrane says Idahoans should keep the option to vote absentee by mail, without needless restrictions"), "Idaho voters should continue to have the option to vote absentee by mail."),
     ("gov-05", 1, ID_SOS("McGrane points to Idaho’s voter identification requirement as part of a strong system"), "We require voter identification, maintain a statewide voter registration system"),
     ("gov-03", 2, ID_SOS("McGrane would modernize Idaho’s campaign finance disclosure laws"), "Idaho voters deserve timely, meaningful information about who is funding political activity in our state."))
main("ID-SOS", "mcgrane", "keenan")

ID_AUD = sn("Idaho Capital Sun", "https://idahocapitalsun.com/voter-guides/contests/2026-general-controller/", "candidates’ answers to the newsroom’s questionnaire")
cand("ID-AUD", "woolf", "Brandon Woolf", "R", "Idaho’s state controller for nearly 14 years; built the Transparent Idaho and Townhall Idaho sites.",
     ("gov-12", 2, ID_AUD("Woolf calls transparency in state spending his true north"), "if the state is spending a dollar, citizens should be able to find out how, when, and why."))
cand("ID-AUD", "mohan", "Rakesh Mohan", "D", "Retired legislative auditor and evaluator (36 years in four states, 21 in Idaho); visiting professor of public policy at Boise State.",
     ("gov-12", 2, ID_AUD("Mohan would make government transparency one of his highest priorities"), "If elected, government transparency will be one of my highest priorities."))
main("ID-AUD", "woolf", "mohan")

# Indiana (Indiana Capital Chronicle: candidates’ survey answers, quoted, and the
# newsroom’s summaries where a candidate didn’t answer) ----------------------------------
IN_SOS = sn("Indiana Capital Chronicle", "https://indianacapitalchronicle.com/voter-guides/contests/secretary-of-state/", "candidates’ survey answers and the newsroom’s summaries")
cand("IN-SOS", "ballard", "Greg Ballard", "I",
     "Former Republican mayor of Indianapolis (2008–2015) and retired Marine lieutenant colonel, running on the new Lincoln Party line.",
     ("gov-09", 1, IN_SOS("Ballard pledges not to endorse, donate to or raise money for candidates whose elections his office oversees"), "I will not endorse, donate to, or raise money for candidates whose elections my office oversees."),
     ("soc-07", 1, IN_SOS("Ballard created a pre-K scholarship program as mayor and says no family should wonder where to find childcare"), "No family should ever worry about a roof over their head or wonder where to find food or childcare for their children."))
cand("IN-SOS", "bayh", "Beau Bayh", "D",
     "Indianapolis attorney who rose to captain in the Marine Corps and its reserve; clerked for federal appeals judge David Hamilton.",
     ("gov-10", 2, IN_SOS("Bayh would implement citizen-led ballot initiatives"), "implementing citizen-led ballot initiatives, protecting early voting"),
     ("gov-06", 1, IN_SOS("Bayh would protect early voting"), None),
     ("eco-02", 2, IN_SOS("Bayh says working Hoosiers need tax relief, starting with the gas tax and the sales tax on utilities"), "I believe that working Hoosiers are in desperate need of tax relief."),
     ("gov-12", 1, IN_SOS("Bayh would open an independent audit of the secretary of state’s office on day one"), "Cleaning up the corruption in the Secretary of State’s office by opening an Independent audit on day one."))
cand("IN-SOS", "engling", "Max Engling", "R",
     "Former regional director for Sen. Jim Banks and U.S. House Republican staffer, including for Speaker Kevin McCarthy.",
     ("sta-04", 1, IN_SOS("Engling would reduce property taxes while letting local governments fund their operations"), "I believe it is important to reduce property taxes"))
cand("IN-SOS", "shillings", "Lauri Shillings", "L", "Chair of the Libertarian Party of Hamilton County; creative director at the University of Indianapolis.",
     ("gov-03", 1, IN_SOS("Shillings would show who is paying for politicians at every level"), "I want to make it so you can see who is paying for your politicians at every level."),
     ("gov-12", 1, IN_SOS("Shillings wants an assessment of how tax dollars are used"), "an assessment of how our tax dollars are used might be in order"))
main("IN-SOS", "bayh", "engling")

IN_AUD = sn("Indiana Capital Chronicle", "https://indianacapitalchronicle.com/voter-guides/contests/comptroller-general/", "candidates’ survey answers and the newsroom’s summaries")
cand("IN-AUD", "bailey", "Jessica Bailey", "D", "Circuit court clerk in her second term; former Portage Township school board member.",
     ("gov-12", 2, IN_AUD("Bailey would make the state transparency portal easier to use for contracts, vendor payments and salaries"), None),
     ("sta-04", 1, IN_AUD("Bailey supports property tax relief for homeowners, though not eliminating property taxes"), None),
     ("hou-05", 2, IN_AUD("Bailey supports tax-free savings and a grant for first-time homebuyers"), None),
     ("soc-07", 2, IN_AUD("Bailey supports childcare tax credits and vouchers"), None))
cand("IN-AUD", "nieshalla", "Elise Nieshalla", "R", None,
     ("eco-07", 1, IN_AUD("Nieshalla promotes national fiscal solvency as chair of state financial officers’ National Debt Crisis Taskforce"), None),
     ("gov-12", 1, IN_AUD("Nieshalla promotes transparency through the state transparency portal and a federal funding dashboard"), None))
cand("IN-AUD", "schick", "John Schick", "L", "Business consultant and former state Libertarian Party treasurer.",
     ("eco-07", 1, IN_AUD("Schick told the newsroom in 2022 he wants reduced government spending"), None))
main("IN-AUD", "nieshalla", "bailey")

IN_TREAS = sn("Indiana Capital Chronicle", "https://indianacapitalchronicle.com/voter-guides/contests/treasurer/", "the newsroom’s summaries; Daniel Elliott did not return its questionnaire")
cand("IN-TREAS", "kebe", "Coumba Kebe", "D", "Health care executive; founded Scope Consulting, which works with home care agencies.",
     ("hou-01", 1, IN_TREAS("Kebe would help finance affordable workforce housing through state bonding"), None),
     ("soc-07", 1, IN_TREAS("Kebe would help secure low-cost financing to expand childcare"), None),
     ("gov-12", 1, IN_TREAS("Kebe proposes plain-language reporting on state finances and investments"), None))
main("IN-TREAS", "elliott", "kebe")

# Maryland (Maryland Matters' questionnaire, candidates' own answers) ------------------
MD_AG = sn("Maryland Matters", "https://marylandmatters.org/voter-guides/contests/attorney-general/", "candidates’ answers to the newsroom’s questionnaire")
cand("MD-AG", "brown", "Anthony Brown", "D", None,
     ("cri-05", 1, MD_AG("Brown would expand mental health and reentry support and invest in rehabilitation"), "We must reduce recidivism, expand mental health and reentry support, and invest in prevention and rehabilitation alongside accountability."),
     ("cri-08", 1, MD_AG("Brown supports restorative justice and diversion programs for young people"), "I support evidence-based approaches, including restorative justice and diversion programs"),
     ("cri-07", 1, MD_AG("Brown would invest in prevention"), None),
     ("soc-02", 1, MD_AG("Brown would enforce civil rights laws and protections against discrimination"), None),
     ("soc-03", 1, MD_AG("Brown names the erosion of reproductive freedom among the greatest threats to civil rights"), "The greatest threat to civil rights is the erosion of equal protection, voting rights, reproductive freedom, and protections against discrimination."))
cand("MD-AG", "rutledge", "James Rutledge III", "R",
     "Attorney in private practice in Harford County for four decades; Bel Air town commissioner from 2023 to 2025.",
     ("soc-01", 2, MD_AG("Rutledge would never use the office to punish political speech, which he calls censorship"), "that path leads to censorship, which I condemn."),
     ("ene-04", 1, MD_AG("Rutledge would investigate and prosecute environmental crimes that harm clean water and the Chesapeake Bay"), "Protect clean water and our Chesapeake Bay by investigating and prosecuting environmental crimes that harm them."))
main("MD-AG", "brown", "rutledge")

MD_AUD = sn("Maryland Matters", "https://marylandmatters.org/voter-guides/contests/comptroller-comptroller/", "candidates’ answers to the newsroom’s questionnaire")
cand("MD-AUD", "dunn", "Sonya Dunn", "R", "Business executive and retired military spouse.",
     ("eco-01", -1, MD_AUD("Dunn opposed the 2025 capital gains tax on high earners"), "2% capital gains tax on high earners and 3% tax on IT/data services discourages investment"),
     ("sta-10", 1, MD_AUD("Dunn backs tax bills she says help retain manufacturing jobs in Maryland"), "Short term revenue loss but helps retain manufacturing jobs and reduce food deserts in Maryland."),
     ("gov-12", 1, MD_AUD("Dunn would strengthen oversight of budgets and contracts"), "Strengthen financial management oversight of budgets and contracts."))
cand("MD-AUD", "lierman", "Brooke Lierman", "D", None,
     ("gov-12", 2, MD_AUD("Lierman modernized contract spending reporting so Marylanders can see how their money is spent"), "I've also modernized contract spending reporting so Marylanders can see exactly how their money is being spent."),
     ("eco-02", 1, MD_AUD("Lierman has championed access to the Earned Income and Child Tax Credits"), "I've championed access to Earned Income Tax Credit and the Child Tax Credit"))
main("MD-AUD", "lierman", "dunn")

# New Mexico (Source NM's interviews, candidates' own words) ---------------------------
NM_AG = sn("Source NM", "https://sourcenm.com/voter-guides/contests/attorney-general/", INTERVIEWS)
cand("NM-AG", "torrez", "Raúl Torrez", "D", "Attorney general since 2023; former Bernalillo County district attorney and federal prosecutor.",
     ("soc-08", 2, NM_AG("Torrez would modernize consumer protection law and the laws regulating big tech, including data brokering"), "We have a lot of work to do in both modernizing our consumer protection and our laws that regulate big tech."),
     ("soc-02", 1, NM_AG("Torrez will seek new authority for his office to investigate civil rights"), "We’re also going to push for new authority to investigate civil rights"))
cand("NM-AG", "kane", "Sam Kane", "R", "Las Cruces lawyer in private practice since 2004, mostly personal injury cases; has contracted with the public defender’s office.",
     ("cri-04", 1, NM_AG("Kane supports a bill toughening penalties for juveniles who commit serious, heinous crimes"), "there are situations where if you kill in cold blood, then you need to be tried as an adult."),
     ("cri-07", 1, NM_AG("Kane would put much of his energy into preventing crime"), "I would put a lot of my energy on preventing it from happening in the first place."))
main("NM-AG", "torrez", "kane")

NM_SOS = sn("Source NM", "https://sourcenm.com/voter-guides/contests/secretary-of-state/", INTERVIEWS)
cand("NM-SOS", "goolsby", "Ramona Goolsby", "R", "Retired nurse practitioner and rancher; moved to New Mexico in 2019.",
     ("gov-05", 1, NM_SOS("Goolsby wants a voter ID bill debated in the 2027 session, with help for voters who lack documents"), "Voter ID is something that’s very important to the public."))
main("NM-SOS", "askin", "goolsby")

NM_AUD = sn("Source NM", "https://sourcenm.com/voter-guides/contests/state-auditor/", INTERVIEWS)
cand("NM-AUD", "lawrence", "Joshua Lawrence", "R", "Tucumcari resident; previously ran for Bernalillo County sheriff.",
     ("gov-12", 2, NM_AUD("Lawrence would set up a New Mexico DOGE office to show where every penny is spent"), "see where every penny is spent, and making it completely transparent so that people can see everything that’s going on."),
     ("eco-07", 1, NM_AUD("Lawrence plans to shrink the auditor’s office toward small government"), "Ultimately, the plan is for small government."))
main("NM-AUD", "maestas", "lawrence")

NM_TREAS = sn("Source NM", "https://sourcenm.com/voter-guides/contests/state-treasurer/", INTERVIEWS)
cand("NM-TREAS", "montoya", "Laura Montoya", "D", "State treasurer since 2023; Sandoval County treasurer for two terms before that.",
     ("edu-10", 2, NM_TREAS("Montoya wants financial literacy to be a high school graduation requirement"), "financial literacy as a graduation requirement"),
     ("eco-10", -1, NM_TREAS("Montoya says tariffs’ costs fall on U.S. consumers"), "The burden is on whoever purchases in the United States, which then goes on to the consumer"))
cand("NM-TREAS", "ellison", "Jim Ellison", "R", "Chartered financial analyst; researched natural disasters’ effect on the power grid at Sandia National Laboratories.",
     ("gov-12", 1, NM_TREAS("Ellison would publish a plain-English investment performance report with benchmarks"), "which would be in plain English and would have appropriate benchmarks"))
main("NM-TREAS", "montoya", "ellison")

# Rhode Island (Rhode Island Current's questionnaire, candidates' own answers) ---------
RI_AG = sn("Rhode Island Current", "https://rhodeislandcurrent.com/voter-guides/contests/2026-general-attorney-general/", "candidates’ answers to the newsroom’s questionnaire")
cand("RI-AG", "ahern", "Kimberly Ahern", "D", "Former state prosecutor (Special Victims Unit) and state government administrator; first run for office.",
     ("eco-09", 1, RI_AG("Ahern would fight for workers’ rights and fair wages for health care providers and staff"), "It means fighting for workers’ rights and fair wages for providers and staff."),
     ("hea-03", 1, RI_AG("Ahern would sue the federal government over cuts to Medicare and Medicaid"), "taking the federal government to court over President Trump’s unconscionable cuts to Medicare and Medicaid"),
     ("soc-10", 1, RI_AG("Ahern says the Trump administration is attacking her right to be married to her wife, and she would fight it"), "The Trump administration is attacking my right to be married to my wife."),
     ("soc-03", 1, RI_AG("Ahern says the administration is attacking her daughters’ right to control their own bodies"), "They are attacking my three daughters’ rights to control their own bodies."),
     ("ene-04", 1, RI_AG("Ahern opposes federal moves she says undermine clean air and water"), "They are undermining the clean air we breathe, the clean water we drink"))
cand("RI-AG", "gordon", "Alan Gordon", "R", "Canon lawyer from West Greenwich; ran for attorney general as an independent in 2018.",
     ("gov-09", 1, RI_AG("Gordon would recuse the office from open-records cases about itself, as he reads state ethics law"), "I will not only recuse the office properly for the first time"),
     ("gov-12", 1, RI_AG("Gordon would end what he calls the office’s history of hiding open records"), "The Rhode Island Attorney General’s Office has a long history of hiding supposedly open records, and I will end that."),
     ("cri-03", 1, RI_AG("Gordon says someone other than the police must investigate when police are investigating themselves"), "When the police are investigating themselves, someone else has to step in."))
main("RI-AG", "ahern", "gordon")

RI_LG = sn("Rhode Island Current", "https://rhodeislandcurrent.com/voter-guides/contests/2026-general-lieutenant-governor/", "candidates’ answers to the newsroom’s questionnaire")
cand("RI-LG", "loughlin", "John Loughlin", "R", "Retired Army Reserve lieutenant colonel, combat veteran and former radio host; former state representative and House minority whip.",
     ("gov-12", 2, RI_LG("Loughlin would have the office hire auditors to review government spending, at no new cost"), "This would give Rhode Islanders clearer insight into how their tax dollars are being spent."),
     ("eco-07", 1, RI_LG("Loughlin would identify government waste, duplication and inefficiency to save taxpayers money"), "identify government waste, duplication, and inefficiency"))
cand("RI-LG", "matos", "Sabina Matos", "D", "Lieutenant governor since 2021; former Providence City Council president.",
     ("hou-01", 2, RI_LG("Matos has pushed for historic state investments in affordable housing"), "advocating for the state to make historic investments in affordable housing"),
     ("soc-03", 2, RI_LG("Matos says she has fought to protect reproductive freedoms"), "I’ve also faced the tough fights to protect reproductive freedoms"))
main("RI-LG", "matos", "loughlin")

RI_TREAS = sn("Rhode Island Current", "https://rhodeislandcurrent.com/voter-guides/contests/2026-general-general-treasurer/", "candidates’ answers to the newsroom’s questionnaire; Micholas Credle did not respond")
cand("RI-TREAS", "diossa", "James Diossa", "D", "General treasurer since 2023; former mayor of Central Falls.",
     ("hou-05", 2, RI_TREAS("Diossa set up RI AnchorHome, which uses state deposits to make mortgages cheaper for first-time homebuyers"), "The program developed in my first term, RI AnchorHome, has already delivered meaningful results"))
main("RI-TREAS", "diossa", "credle")

RI_SOS = sn("Rhode Island Current", "https://rhodeislandcurrent.com/voter-guides/contests/2026-general-secretary-of-state/", "candidates’ answers to the newsroom’s questionnaire")
cand("RI-SOS", "amore", "Gregg Amore", "D", "Secretary of state since 2023; state representative for 10 years before that.",
     ("gov-12", 1, RI_SOS("Amore supports changes to the public records law that make records easier and cheaper to get"), "I support changes to the APRA that make public records easier to access, reduce unnecessary costs and delays"))
main("RI-SOS", "amore")

# Nebraska (Nebraska Examiner's questionnaire, candidates' own answers) ----------------
NE_AG = sn("Nebraska Examiner", "https://nebraskaexaminer.com/voter-guides/contests/2026-general-nebraska-attorney-general/", "candidates’ answers to the newsroom’s questionnaire")
cand("NE-AG", "brasher", "Jocelyn Brasher", "D", "Former assistant attorney general in Nebraska’s Consumer Protection Bureau (five years).",
     ("eco-04", 2, NE_AG("Brasher would use antitrust law aggressively against price gouging and corporate consolidation"), "using our consumer protection and antitrust laws to ensure markets are fair and competitive so life stays affordable for Nebraskans"))
main("NE-AG", "hilgers", "brasher")

NE_SOS = sn("Nebraska Examiner", "https://nebraskaexaminer.com/voter-guides/contests/2026-general-nebraska-secretary-of-state/", "candidates’ answers to the newsroom’s questionnaire")
cand("NE-SOS", "krist", "Bob Krist", "America First", "State senator for 10 years.",
     ("gov-06", 1, NE_SOS("Krist would keep absentee, early and mail-in voting, including the all-mail counties"), "In-person, absentee, early and mail-in voting must be protected!"),
     ("gov-10", 1, NE_SOS("Krist would work to enact initiatives voters pass"), "When 72% of the voters petition an action, we need to listen, regardless of any bias."))
cand("NE-SOS", "petersen", "Scott Petersen", "R", None,
     ("gov-06", -1, NE_SOS("Petersen wants in-person voting to stay the primary method, with mail voting kept for those who rely on it"), "I believe in-person voting should remain the primary method of casting a ballot whenever practical."),
     ("gov-10", 1, NE_SOS("Petersen calls the initiative and referendum process an important constitutional right"), "Nebraska's initiative and referendum process is an important constitutional right that allows citizens to bring issues directly before the voters."))
cand("NE-SOS", "rumbaugh", "Paul Rumbaugh", "Working People", None,
     ("gov-10", 1, NE_SOS("Rumbaugh calls ballot measures a vital tool for everyday Nebraskans"), "My stance on ballot measures is that they are a vital tool for giving a voice to everyday Nebraskans."))
cand("NE-SOS", "slattery", "Sarah Slattery", "D", None,
     ("gov-06", 1, NE_SOS("Slattery would keep mail-in voting as it is, including the all-mail counties"), "eliminating mail-in options for rural communities is simply the wrong move."),
     ("gov-10", 1, NE_SOS("Slattery calls the ballot initiative process a vital constitutional tool"), "The voter-led ballot initiative process is a vital constitutional tool designed to give everyday Nebraskans a direct voice in our democracy."),
     ("gov-03", 1, NE_SOS("Slattery says Nebraskans have a right to know who funds petition campaigns"), "Nebraskans have a fundamental right to know who is funding these campaigns"))
main("NE-SOS", "petersen", "slattery")

NE_TREAS = sn("Nebraska Examiner", "https://nebraskaexaminer.com/voter-guides/contests/2026-general-nebraska-state-treasurer/", "candidates’ answers to the newsroom’s questionnaire; Daniel Ebers did not respond to most of it")
cand("NE-TREAS", "spellerberg", "Joey Spellerberg", "R", None,
     ("gov-12", 2, NE_TREAS("Spellerberg’s priorities include increasing transparency in government spending"), "Nebraskans should be able to see where their tax dollars are coming from and where they are going."),
     ("edu-10", 1, NE_TREAS("Spellerberg would expand financial literacy"), None))
main("NE-TREAS", "spellerberg", "ebers")

NE_AUD = sn("Nebraska Examiner", "https://nebraskaexaminer.com/voter-guides/contests/2026-general-nebraska-auditor-of-public-accounts/", "candidates’ answers to the newsroom’s questionnaire")
cand("NE-AUD", "knight", "John Knight", "America First", None,
     ("sta-11", 2, NE_AUD("Knight would oversee economic development subsidies such as tax increment financing"), "taxpayers deserve to know whether these programs actually deliver what they promise"),
     ("gov-12", 1, NE_AUD("Knight would post a public dashboard tracking every audit recommendation"), "I would post a public, searchable dashboard that tracks every recommendation"))
cand("NE-AUD", "foley", "Mike Foley", "R", None,
     ("gov-12", 1, NE_AUD("Foley posts every audit report and finding on the office’s website"), "Every audit report, audit letter or other official statement of findings is always posted immediately to our website."))
main("NE-AUD", "foley", "knight")


def entry(rid, cands):
    have = {c["id"] for c in cands if c.get("positions")}
    out = {"id": rid, "candidates": cands}
    if all(m in have for m in MAIN.get(rid, [])) and MAIN.get(rid):
        out["researchNote"] = ("Positions from a States Newsroom voter guide, read Nov. 4, 2026: the candidates’ "
                               "own answers, or the newsroom’s summary of them where the source says so.")
    else:
        out["partial"] = True
    return out


assert set(RACES) <= set(MAIN), set(RACES) - set(MAIN)
write("data/research/offices.json", [entry(rid, cands) for rid, cands in sorted(RACES.items())],
      "Positions for candidates for statewide offices below governor, from the States Newsroom voter guides, read Nov. 4, 2026.", updated=READ)
