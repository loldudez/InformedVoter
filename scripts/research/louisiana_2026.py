"""Researched details for the Louisiana races on a ZIP 70820 (Baton Rouge) ballot:
the U.S. Senate race and the 6th Congressional District open primary.

Every figure and position below was researched on Oct 24, 2026, and its source
travels with it into the JSON. To update: edit the data here, then run
    py scripts/research/louisiana_2026.py
    py scripts/update_races.py

This writes data/research/LA.json, an overlay that update_races.py merges onto the
automatically refreshed race data (candidates, ratings, polls, money).
Fundraising comes from the FEC API (candidate totals, reports through Oct 14).
"""
import json, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "data/research/LA.json"
TODAY = "2026-10-24"

S = {
    "letlow_plan": ("Julia Letlow campaign site, “Julia’s Plan”", "https://www.julialetlow.com/policyplan", TODAY),
    "knoe_letlow": ("KNOE: Julia Letlow focuses on energy and education in Senate race", "https://knoe.com/2026/06/01/julia-letlow-focuses-energy-education-senate-race/", "2026-06-01"),
    "illum_afford": ("Louisiana Illuminator: congressional candidates float ideas for affordable gas, groceries", "https://lailluminator.com/2026/10/12/louisianas-congressional-candidates-float-ideas-for-affordable-gas-groceries/", "2026-10-12"),
    "illum_dobbs": ("Louisiana Illuminator: what Louisiana officials said after the Supreme Court’s abortion ruling", "https://lailluminator.com/2022/06/24/what-louisiana-elected-officials-are-saying-about-abortion-after-the-supreme-courts-ruling/", "2022-06-24"),
    "roll_151": ("U.S. House roll call 151 (H.R. 8035, Ukraine aid): Letlow voted No", "https://clerk.house.gov/Votes/2024151", "2024-04-20"),
    "roll_152": ("U.S. House roll call 152 (H.R. 8034, Israel aid): Letlow voted Yes", "https://clerk.house.gov/Votes/2024152", "2024-04-20"),
    "roll_190": ("U.S. House roll call 190 (H.R. 1, which cut federal Medicaid spending): Letlow voted Yes", "https://clerk.house.gov/Votes/2025190", "2025-07-03"),
    "wwno_senate": ("WWNO/WRKF election guide: Davis’s questionnaire answers", "https://www.wwno.org/2026-10-19/nov-3-election-guide-meet-the-u-s-senate-candidates", "2026-10-19"),
    "wafb_davis": ("WAFB: A farmer’s longshot: Jamie Davis’s bid for U.S. Senate", "https://www.wafb.com/2026/06/24/farmers-longshot-jamie-daviss-bid-us-senate/", "2026-06-24"),
    "ktbs_davis": ("KTBS: Meet the candidate: Jamie Davis", "https://www.ktbs.com/meet-the-candidate-jamie-davis/article_30a0be6e-452a-43ad-b3c3-3b1b7121dd68.html", "2026-05-01"),
    "davis_site": ("Jamie Davis campaign site", "https://www.jamieforlouisiana.com/", TODAY),
    "miguez_issues": ("Blake Miguez campaign site, Issues", "https://blakemiguez.com/issues/", TODAY),
    "edmonds_site": ("Rick Edmonds campaign site", "https://rickedmonds.com/", TODAY),
    "illum_forum": ("Louisiana Illuminator: 6 takeaways from the 6th District candidates forum (Oct. 9)", "https://lailluminator.com/2026/10/10/6th-district-forum/", "2026-10-10"),
    "illum_gonzales": ("Louisiana Illuminator: 6th District field on petrochemical limits, health care and immigration (Oct. 13 forum)", "https://lailluminator.com/2026/10/14/most-of-6th-district-field-sees-need-for-more-petrochemical-industry-limits/", "2026-10-14"),
    "banks_site": ("Chauna Banks campaign site", "https://chaunabanksforcongress.vote/", TODAY),
    "forbes_issues": ("Pat Forbes campaign site, Issues", "https://www.patforbes.com/about-pat", TODAY),
    "wagley_issues": ("Stephen Wagley campaign site, Issues", "https://www.wagleyforcongress.com/issues", TODAY),
    "wagley_home": ("Stephen Wagley campaign site", "https://www.wagleyforcongress.com/", TODAY),
    "appeaning_site": ("Monique Appeaning campaign site", "https://www.appeaningforcongress.com/", TODAY),
    "ldavis_policies": ("Larry Davis III campaign site, Policies", "https://www.larrydavisforcongress.com/policies", TODAY),
    "mebruer_about": ("Michael Mebruer campaign site, About", "https://www.mebruerforcongress.com/about", TODAY),
}


def P(*rows):
    """rows: (question id, stance, source key, quote or None)"""
    out = {}
    for qid, stance, key, quote in rows:
        title, url, date = S[key]
        src = {"title": title, "url": url, "date": date}
        if date == TODAY:
            src["accessed"] = True  # a live campaign page: the date is when it was read
        if quote:
            src["quote"] = quote
        assert qid not in out, qid
        out[qid] = {"stance": stance, "source": src}
    return out


def fec(cid, total, small=0, large=0, pac=0, party=0, self_=0, cash=None, note=None):
    other = round(total - (small + large + pac + party + self_))
    assert other >= 0, (cid, other)
    f = {
        "total": total,
        "parts": {"small": small, "large": large, "pac": pac, "party": party, "self": self_, "public": 0, "other": other},
        "cashOnHand": cash, "asOf": "2026-10-14", "source": "FEC", "fecId": cid,
        "url": f"https://www.fec.gov/data/candidate/{cid}/?cycle=2026&election_full=true",
    }
    if note:
        f["note"] = note
    return f


NO_FEC = {"total": 0, "parts": {}, "note": "No campaign finance report on file with the FEC as of Oct. 24, 2026."}

senate = {
    "id": "LA-SEN", "state": "LA", "office": "senate", "level": "federal", "district": None,
    "held": "R", "open": True, "turnout": 1383000,
    "ratings": [
        {"outlet": "Cook Political Report", "rating": "Solid R", "date": "2026-10-20"},
        {"outlet": "Inside Elections", "rating": "Solid R", "date": "2026-10-15"},
        {"outlet": "Sabato’s Crystal Ball", "rating": "Safe R", "date": "2026-10-14"},
        {"outlet": "Decision Desk HQ", "rating": "Likely R", "date": "2026-10-22"},
        {"outlet": "Silver Bulletin", "rating": "Likely R", "date": "2026-10-22"},
    ],
    "ratingsSource": {"title": "Wikipedia’s ratings table", "url": "https://en.wikipedia.org/wiki/2026_United_States_Senate_election_in_Louisiana"},
    "notes": [
        {"text": "Sen. Bill Cassidy lost the May 16 Republican primary; Letlow then beat Treasurer John Fleming in the June 27 runoff.", "source": "WAFB", "url": "https://www.wafb.com/2026/06/28/julia-letlow-jamie-davis-advance-louisiana-us-senate-race-ap-projects/"},
        {"text": "Projected votes assume about 1.38 million voters, close to Louisiana’s 2022 Senate turnout."},
        {"text": "A Hart Research (D) poll from September (Letlow 48%, Davis 44%) is listed by Wikipedia, but its only source is a social media post, so it is left out of the average."},
        {"text": "Davis says his campaign’s internal polling shows him 4 points behind. No pollster, dates or sample were released, so it is not in the average.", "source": "WAFB, Oct. 19", "url": "https://wafb.com/2026/10/19/breaking-down-dollars-us-senate-race/"},
    ],
    "excludePolls": ["hart research"],
    "polls": [
        {"pollster": "Public Policy Polling", "sponsor": "Released by the Davis campaign (D)", "start": "2026-07-21", "end": "2026-07-22", "n": 518, "pop": "RV",
         "results": {"LA-SEN:letlow": 41, "LA-SEN:davis": 37}, "url": "https://www.wwno.org/2026-08-19/poll-shows-4-point-difference-between-letlow-and-davis-for-u-s-senate-1-in-5-undecided",
         "note": "22% undecided. A campaign’s own poll; treat with caution."},
    ],
    "earlyVote": {
        "ballots": 115000, "asOf": "2026-10-20", "label": "first day", "pctOfTurnout": round(115000 / 1383000, 3),
        "byParty": None, "vs2022": None,
        "note": "About 115,000 people voted on the first day of early voting. Black voters made up almost 32% of them, a larger share than in almost any election since 2008. Early voting runs through Oct. 27.",
        "source": {"title": "Louisiana Illuminator, Oct. 22, 2026 (Secretary of State data)", "url": "https://lailluminator.com/2026/10/22/black-voter-turnout-higher-than-normal-for-louisianas-first-day-of-early-voting/"},
    },
    "candidates": [
        {
            "id": "LA-SEN:letlow", "aliases": ["LA-SEN:R"], "name": "Julia Letlow", "party": "R", "incumbent": False,
            "bio": "U.S. Representative for Louisiana’s 5th District since 2021; serves on the House Appropriations Committee.",
            "officialSite": "https://www.julialetlow.com/", "donateUrl": "https://www.julialetlow.com/donate",
            "finance": fec("S6LA00664", 7062069, small=169337, large=1400944, pac=1243600, party=62000, cash=443170,
                           note="Includes a $4.18M transfer from her U.S. House campaign"),
            "positions": P(
                ("eco-01", -1, "letlow_plan", "Permanently extend the Trump tax cuts"),
                ("eco-02", 2, "letlow_plan", "Make the One Big Beautiful Bill’s no-tax-on-tips provision permanent"),
                ("eco-07", 1, "letlow_plan", "Reduce government spending that fuels inflation"),
                ("eco-10", 2, "illum_afford", None),
                ("agr-07", 1, "illum_afford", None),
                ("hea-03", -1, "roll_190", None),
                ("hea-05", 1, "letlow_plan", "Expand research into chronic disease prevention"),
                ("edu-06", 2, "knoe_letlow", "I want to fight for school choice and our charter schools and homeschooling"),
                ("edu-07", 2, "letlow_plan", "Stop federal interference in local education decisions"),
                ("imm-01", 2, "letlow_plan", "Finish construction of the border wall"),
                ("imm-07", 2, "letlow_plan", "Deport criminal illegal aliens and gang members"),
                ("imm-10", 2, "letlow_plan", "Require E-Verify nationwide"),
                ("soc-03", -2, "illum_dobbs", "today is a monumental win for the unborn"),
                ("soc-04", 2, "illum_dobbs", "today is a monumental win for the unborn"),
                ("soc-11", -2, "letlow_plan", "Ban gender transition procedures for minors"),
                ("soc-12", -1, "letlow_plan", "Keep biological men out of women’s sports"),
                ("ene-03", 2, "letlow_plan", "Expand oil and natural gas production"),
                ("ene-04", -1, "letlow_plan", "Reverse anti-energy regulations"),
                ("ene-06", -1, "knoe_letlow", None),
                ("ene-10", 1, "letlow_plan", "Increase American energy production to bring down gas and utility bills"),
                ("ene-08", 2, "letlow_plan", "Strengthen levee and flood protection systems"),
                ("hou-10", 2, "letlow_plan", "Improve hurricane resilience infrastructure"),
                ("hou-09", 2, "letlow_plan", "Expand access to rural broadband"),
                ("agr-01", 2, "letlow_plan", "Protect crop insurance programs"),
                ("agr-08", 2, "letlow_plan", "Strengthen agricultural research and extension programs"),
                ("def-01", 1, "letlow_plan", "Increase Navy and Coast Guard ship procurement"),
                ("def-03", 1, "letlow_plan", "Reduce VA wait times"),
                ("def-06", 2, "letlow_plan", "Expand defense manufacturing jobs"),
                ("def-12", 2, "roll_152", None),
                ("def-13", -2, "roll_151", None),
                ("def-15", 2, "illum_afford", None),
                ("def-16", 1, "letlow_plan", "Ban Chinese ownership of American farmland"),
                ("gov-02", 2, "letlow_plan", "Ban Members of Congress from trading individual stocks"),
                ("gov-05", 2, "letlow_plan", "Strengthen voter ID requirements"),
                ("gov-09", 1, "letlow_plan", "Strengthen financial disclosure requirements"),
                ("gov-12", 2, "letlow_plan", "Increase transparency in government spending"),
            ),
        },
        {
            "id": "LA-SEN:davis", "aliases": ["LA-SEN:D"], "name": "Jamie Davis", "party": "D", "incumbent": False,
            "bio": "Farmer from Waterproof in Tensas Parish; former Tensas Parish Police Jury member.",
            "officialSite": "https://www.jamieforlouisiana.com/", "donateUrl": "https://secure.actblue.com/donate/sendafarmertowashington",
            "finance": fec("S6LA00615", 5019888, small=3743089, large=1206146, pac=10000, party=1000, self_=54000, cash=1254929),
            "positions": P(
                ("soc-03", 2, "wwno_senate", "a woman should have the right to make decisions about her body with her doctor"),
                ("soc-04", -2, "wwno_senate", "a woman should have the right to make decisions about her body with her doctor"),
                ("imm-02", 2, "wwno_senate", "I believe we should protect the Dreamers."),
                ("imm-01", 1, "wafb_davis", None),
                ("gov-02", 2, "wwno_senate", "I want a full ban."),
                ("gov-09", 1, "wwno_senate", "ban public officials from signing non-disclosure agreements"),
                ("hea-01", 2, "wafb_davis", None),
                ("hea-03", 2, "ktbs_davis", None),
                ("hea-07", 2, "wafb_davis", None),
                ("hea-06", 2, "ktbs_davis", None),
                ("eco-03", 2, "wwno_senate", "higher federal minimum wages"),
                ("eco-10", -2, "illum_afford", "It’s basically just a tax. We all have to pay it."),
                ("agr-07", -1, "illum_afford", "It’s basically just a tax. We all have to pay it."),
                ("def-15", -2, "wwno_senate", "harmful policies, like tariffs, the OBBBA, and the war in Iran"),
                ("ene-08", 2, "wwno_senate", "Congress should fully fund it"),
                ("hou-10", 2, "wwno_senate", "restore the pre-disaster mitigation grants that the current administration terminated"),
                ("ene-01", 1, "wwno_senate", "we need to lean into all forms of energy"),
                ("ene-03", 1, "wwno_senate", "we need to lean into all forms of energy"),
                ("edu-01", 1, "ktbs_davis", None),
                ("edu-04", 1, "ktbs_davis", None),
                ("edu-03", 1, "ktbs_davis", None),
                ("eco-06", 1, "ktbs_davis", None),
                ("agr-01", 1, "wwno_senate", "The Farmer’s Farm Bill that supports family farmers"),
                ("gov-04", 2, "wafb_davis", None),
                ("gov-05", 1, "wafb_davis", None),
                ("gov-06", 1, "wafb_davis", None),
                ("gov-11", 1, "davis_site", "I don’t take their money, and I won’t do their bidding."),
                ("soc-12", 1, "wafb_davis", None),
            ),
        },
    ],
}


def cand(slug, name, party, bio, site, donate, finance, positions):
    c = {"id": f"LA-H-06:{slug}", "name": name, "party": party, "incumbent": False, "bio": bio, "finance": finance, "positions": positions}
    if site:
        c["officialSite"] = site
    if donate:
        c["donateUrl"] = donate
    return c


house = {
    "id": "LA-H-06", "state": "LA", "office": "house", "level": "federal", "district": "06", "districtName": "District 6",
    "format": "open-primary", "runoff": "2026-12-12", "held": "D", "open": True, "turnout": 230000, "candidatesOnly": True,
    "consensus": {"rating": "Safe R"},
    "ratings": [
        {"outlet": "Cook Political Report", "rating": "Solid R", "date": "2026-06-01"},
        {"outlet": "Inside Elections", "rating": "Solid R", "date": "2026-06-11"},
        {"outlet": "Sabato’s Crystal Ball", "rating": "Safe R", "date": "2026-06-03"},
        {"outlet": "Decision Desk HQ", "rating": "Safe R", "date": "2026-07-14"},
    ],
    "ratingsSource": {"title": "Wikipedia’s ratings table", "url": "https://en.wikipedia.org/wiki/2026_United_States_House_of_Representatives_elections_in_Louisiana"},
    "notes": [
        {"text": "Rep. Cleo Fields (D) is not running. After the Supreme Court’s Louisiana v. Callais ruling, the Legislature redrew this district to favor a Republican.", "source": "Louisiana Illuminator", "url": "https://lailluminator.com/2026/10/10/6th-district-forum/"},
        {"text": "Cook Political Report estimates the new district would have voted for Trump by more than 30 points in 2024.", "source": "Cook Political Report", "url": "https://www.cookpolitical.com/analysis/house/redistricting/new-louisiana-map-hands-republicans-another-seat"},
        {"text": "Blake Miguez skipped the Oct. 9 and Oct. 13 forums and several interviews, so his positions come only from his campaign site.", "source": "Louisiana Illuminator", "url": "https://lailluminator.com/2026/10/14/most-of-6th-district-field-sees-need-for-more-petrochemical-industry-limits/"},
        {"text": "Candidate backgrounds are from the Louisiana Illuminator’s voter guide.", "source": "voter guide", "url": "https://lailluminator.com/voter-guides/contests/louisiana-house-6/"},
    ],
    "polls": [
        {"pollster": "Poll commissioned by WBRZ-TV", "start": "2026-09-19", "end": "2026-09-21", "n": 800, "approx": True, "pop": "LV",
         "results": {"LA-H-06:edmonds": 13.8, "LA-H-06:banks": 13.2, "LA-H-06:miguez": 9.7, "LA-H-06:garcia": 7.7, "LA-H-06:forbes": 7.6},
         "url": "https://lailluminator.com/2026/10/10/6th-district-forum/",
         "note": "Every other candidate polled 4% or lower. The pollster and the undecided share were not reported."},
    ],
    "candidates": [
        cand("miguez", "Blake Miguez", "R", "State senator from New Iberia (in the Legislature since 2015); manages a family oil and gas business.",
             "https://blakemiguez.com/", "https://secure.winred.com/blake-miguez/donate-today",
             fec("H6LA05234", 7749606, small=587711, large=3236952, pac=138919, self_=3514561, cash=1534513, note="Includes $3.51M in loans from the candidate"),
             P(("imm-01", 2, "miguez_issues", "finish the wall, fund the agents, end catch-and-release, mandate E-Verify"),
               ("imm-08", 2, "miguez_issues", "finish the wall, fund the agents, end catch-and-release, mandate E-Verify"),
               ("imm-10", 2, "miguez_issues", "finish the wall, fund the agents, end catch-and-release, mandate E-Verify"),
               ("imm-07", 2, "miguez_issues", "quickly deport violent illegal immigrants"),
               ("ene-03", 2, "miguez_issues", "get LNG export permits approved, stop the slow-walking of Gulf leasing"),
               ("ene-01", -1, "miguez_issues", "end the government handouts that keep certain energy sources afloat"),
               ("cri-01", 1, "miguez_issues", None),
               ("cri-04", 1, "miguez_issues", "stop treating repeat offenders like first-timers"),
               ("soc-03", -2, "miguez_issues", "he will vote against taxpayer funding for abortion"),
               ("soc-04", 1, "miguez_issues", "he will vote against taxpayer funding for abortion"),
               ("edu-03", 2, "miguez_issues", "back the trades and technical training that put people to work"),
               ("edu-07", 1, "miguez_issues", "parents should be in charge of their children’s health and their children’s education"),
               ("gov-05", 2, "miguez_issues", "Voter ID, proof of citizenship, and no foreign money running our elections"),
               ("gov-01", 2, "miguez_issues", "push term limits and a permanent ban on members trading individual stocks"),
               ("gov-02", 2, "miguez_issues", "push term limits and a permanent ban on members trading individual stocks"),
               ("gov-09", 1, "miguez_issues", "extending Louisiana’s statute of limitations on political corruption"),
               ("soc-12", -1, "miguez_issues", None))),
        cand("edmonds", "Rick Edmonds", "R", "State senator from Baton Rouge (in the Legislature since 2015); Baptist pastor.",
             "https://rickedmonds.com/", "https://secure.anedot.com/rick-for-louisiana/contribute",
             fec("H6LA05226", 697139, small=1885, large=503517, pac=36600, self_=155000, cash=134635),
             P(("cri-01", 1, "edmonds_site", "Back the Blue and stand with law enforcement"),
               ("eco-07", 1, "edmonds_site", "Cut wasteful spending"),
               ("ene-08", 1, "edmonds_site", "Protect access to critical flood insurance and disaster relief"),
               ("eco-06", 1, "edmonds_site", "Improve infrastructure to reduce traffic and attract new jobs"),
               ("hou-08", 1, "edmonds_site", "Improve infrastructure to reduce traffic and attract new jobs"),
               ("ene-03", 1, "edmonds_site", "Strengthen Louisiana’s energy industry and protect energy jobs"),
               ("soc-03", -1, "edmonds_site", "Defend life, faith, and family values"),
               ("soc-04", 1, "edmonds_site", "Defend life, faith, and family values"),
               ("def-15", 2, "illum_forum", None),
               ("imm-07", 1, "illum_forum", "it’s going to err on the side of people that have lost their lives"),
               ("gov-01", 1, "illum_forum", None),
               ("gov-02", 1, "illum_forum", None))),
        cand("banks", "Chauna Banks", "D", "Longtime teacher; former East Baton Rouge Parish Metro Council member.",
             "https://chaunabanksforcongress.vote/", "https://secure.anedot.com/chauna-banks-for-congress/donate", NO_FEC,
             P(("hea-01", 1, "banks_site", "Protect and expand access to affordable, quality healthcare for all families."),
               ("edu-01", 1, "banks_site", "Invest in our schools, support teachers"),
               ("edu-03", 1, "banks_site", "expand workforce training"),
               ("def-15", -2, "illum_forum", "We must stop the war in Iran"),
               ("eco-10", -2, "illum_forum", "we have to do something about the tariffs"),
               ("imm-08", -1, "illum_gonzales", "It’s inhumane"),
               ("gov-01", 1, "illum_forum", None),
               ("gov-02", 1, "illum_forum", None))),
        cand("forbes", "Pat Forbes", "D", "Engineer; former head of Louisiana’s Office of Community Development (disaster recovery) under Gov. John Bel Edwards.",
             "https://www.patforbes.com/", "https://secure.actblue.com/donate/patrick-forbes-2",
             fec("H6LA06190", 156334, small=40991, large=105475, self_=9856, cash=97400),
             P(("ene-08", 2, "forbes_issues", "In Congress I’ll fight for the funding to keep doing it."),
               ("hou-10", 2, "forbes_issues", "Invest in what actually reduces the risk."),
               ("hea-07", 2, "forbes_issues", "Restore the premium help that let working families buy a plan"),
               ("hea-03", 1, "illum_gonzales", None),
               ("eco-04", 1, "forbes_issues", "I’ll back real rules against price-fixing"),
               ("eco-12", 1, "forbes_issues", "The current one hands the biggest breaks to the people who need them least"),
               ("eco-01", 1, "forbes_issues", "The current one hands the biggest breaks to the people who need them least"),
               ("eco-10", -2, "forbes_issues", "End the tariffs. They are a tax on everything you buy."),
               ("def-15", -2, "illum_afford", "We started a war that accomplished nothing but raising gas and diesel prices."),
               ("def-04", 1, "forbes_issues", "Congress is supposed to be a check on the President, not a rubber stamp"),
               ("gov-04", 2, "forbes_issues", "Take the map away from the politicians."),
               ("gov-06", 2, "forbes_issues", "Make it easier to vote, not harder."),
               ("gov-02", 2, "forbes_issues", "Ban members of Congress from trading stock."),
               ("gov-11", 2, "forbes_issues", "Cap what the super PACs can take."),
               ("edu-03", 1, "forbes_issues", "the training has to start before the ribbon is cut"),
               ("ene-04", 2, "illum_gonzales", None),
               ("cri-01", 1, "illum_forum", None),
               ("gov-01", 1, "illum_forum", None),
               ("imm-08", -1, "illum_forum", "Do we need to put our neighbors out of church or out of court"))),
        cand("garcia", "Lindsay “Rubia” Garcia", "D", "Lawyer from Walker and former New Orleans social studies teacher; endorsed by the Louisiana Democratic Party.",
             "https://www.rubiagarcia.com/", "https://secure.actblue.com/donate/lindsay-garcia-1",
             fec("H6LA05309", 97007, small=70209, large=21484, self_=2965, cash=21654),
             P(("def-15", -2, "illum_forum", None),
               ("eco-10", 1, "illum_afford", "I support targeted tariffs when there is a clear purpose"),
               ("ene-04", 2, "illum_gonzales", "have a nationwide rule put in place by the EPA"),
               ("hea-07", 2, "illum_gonzales", None),
               ("hea-03", 1, "illum_gonzales", None),
               ("imm-08", -1, "illum_gonzales", "The nanny that is cleaning houses and the like is not the problem"),
               ("gov-01", 1, "illum_forum", None),
               ("gov-02", 1, "illum_forum", None))),
        cand("wagley", "Stephen Wagley", "R", "Chief operating officer of Delta College, his family’s healthcare workforce school; lives in Central.",
             "https://www.wagleyforcongress.com/", "https://secure.winred.com/wagley-for-congress/donate-today",
             fec("H6LA06182", 874344, small=668, large=8175, self_=865500, cash=195633, note="Almost entirely loans from the candidate"),
             P(("eco-01", -1, "wagley_issues", "I will fight to make sure that the Trump tax cuts stay permanent"),
               ("eco-07", 2, "wagley_issues", "Stop the spending spree."),
               ("imm-01", 2, "wagley_issues", "LET’S BUILD THE WALL!"),
               ("ene-03", 2, "wagley_issues", "Unleash American energy."),
               ("ene-10", 1, "wagley_issues", "Cheap, reliable energy is the fastest way to cut costs"),
               ("cri-01", 1, "wagley_issues", "I support the Blue."),
               ("soc-03", -2, "wagley_issues", "Life begins at conception."),
               ("soc-04", 2, "wagley_issues", "Life begins at conception."),
               ("edu-06", 2, "wagley_home", "He has fought for school choice"),
               ("edu-03", 1, "wagley_issues", "technical training partnerships between local businesses, community colleges and technical schools"),
               ("gov-05", 1, "wagley_issues", "The SAVE AMERICA ACT simply requires proof of citizenship to vote."),
               ("hea-04", 1, "wagley_issues", "Make insurance companies compete, not collude."),
               ("def-03", 1, "wagley_home", None))),
        cand("appeaning", "Monique Appeaning", "R", "Former chief administrative officer for East Baton Rouge Mayor-President Sid Edwards.",
             "https://www.appeaningforcongress.com/", "https://secure.anedot.com/committee-to-elect-monique-appeaning/donate",
             fec("H6LA06158", 109183, small=450, large=49760, pac=50, self_=50667, cash=14709),
             P(("cri-01", 1, "appeaning_site", "Back the Blue"),
               ("def-01", 1, "appeaning_site", "Strengthen and modernize our military"),
               ("eco-02", 2, "appeaning_site", "Large tax cuts for hardworking people"),
               ("eco-07", 2, "appeaning_site", "Work toward a balanced federal budget and reduce national debt"),
               ("agr-03", 2, "appeaning_site", "Stop outsourcing and rebuild American manufacturing"),
               ("ene-03", 1, "appeaning_site", "Achieve full American energy independence"),
               ("agr-01", 1, "appeaning_site", "Protect Louisiana farmers and defend American agriculture"),
               ("hou-04", 1, "appeaning_site", "Build more homes to lower prices"),
               ("edu-03", 2, "appeaning_site", "Support multiple pathways such as apprenticeships, job training"),
               ("soc-03", -2, "appeaning_site", "PRO-LIFE."),
               ("soc-04", 1, "appeaning_site", "PRO-LIFE."),
               ("imm-02", -1, "illum_gonzales", None))),
        cand("ldavis", "Larry Davis III", "R", "Self-described middle-class worker; member of the Livingston Parish Republican Executive Committee.",
             "https://www.larrydavisforcongress.com/", "https://secure.winred.com/larry-davis-for-congress/donate-today",
             fec("H6LA05168", 33216, large=21640, pac=2000, cash=809, note="Part of the total is not broken out in the data retrieved"),
             P(("imm-01", 2, "ldavis_policies", "Strong border enforcement, physical barriers where necessary"),
               ("cri-01", 1, "ldavis_policies", "Support police"),
               ("cri-04", 2, "ldavis_policies", "increase penalties for violent crime"),
               ("edu-06", 2, "ldavis_policies", "School choice and support for vocational programs."),
               ("edu-03", 1, "ldavis_policies", "School choice and support for vocational programs."),
               ("ene-03", 2, "ldavis_policies", "Increase domestic drilling, expand refining capacity"),
               ("ene-02", 1, "ldavis_policies", "support nuclear advancement"),
               ("eco-07", 2, "ldavis_policies", "Balanced budget approach."),
               ("def-03", 1, "ldavis_policies", "Support veterans through healthcare streamlining and faster claims"),
               ("hou-09", 2, "ldavis_policies", "expand rural broadband"),
               ("gov-05", 2, "ldavis_policies", "Voter ID."),
               ("agr-01", 1, "ldavis_policies", "Support family farms"),
               ("imm-02", -1, "illum_gonzales", "They are taking money away from your families"))),
        cand("mebruer", "Michael Mebruer", "R", "Traveling health care professional from St. Francisville.",
             "https://www.mebruerforcongress.com/", None,
             fec("H6LA05259", 70714, cash=10987, note="Part of the total is not broken out in the data retrieved"),
             P(("eco-07", 2, "mebruer_about", "Washington’s spending and debt are placing the country on an unsustainable path."))),
        cand("craig", "Rufus Craig", "L", "Attorney with more than 40 years of practice in criminal defense, family law and successions.",
             None, None, NO_FEC,
             P(("imm-05", 2, "illum_gonzales", "instead of arresting the immigrants, let’s arrest the gringos that gave them the job"))),
    ],
}

out = {"updated": TODAY, "note": "Louisiana races on a ZIP 70820 (Baton Rouge) ballot, researched Oct. 24, 2026.", "races": [senate, house]}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
n = sum(len(c["positions"]) for r in out["races"] for c in r["candidates"])
print(f"wrote {OUT}: {len(out['races'])} races, {sum(len(r['candidates']) for r in out['races'])} candidates, {n} sourced positions")
