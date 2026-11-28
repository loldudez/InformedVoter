"""Which states have certified the Nov. 3, 2026 results, checked by hand.

Writes data/certified.json. The results strip at the top of every U.S. page says
"unofficial" until all 50 states and D.C. are listed here with nothing pending and every
Senate, House and governor race is decided; then it says "official" (the owner's choice,
Nov. 4: "Switch when all certify"). Race pages, state pages and "Official results in
<state>" say when a listed state certified.

The rules:
- A state goes in only once its own election office announced the certification (the
  secretary of state's or the state board's release, minutes or canvass), or a news
  report of the vote does, read before it goes in. The date is the day the state's board
  or official certified, not the day of the report.
- Contests a state left out (a recount, Louisiana's Dec. 12 runoffs, the statewide
  offices that Iowa's and Connecticut's legislatures canvass in January) go in `pending`
  by this site's race id when they are races here, in `other` (English, French) when
  they aren't (legislative seats, district attorneys). A race goes in `pending` only when
  the source shows it was left out, never because another state's law would leave it out. They come out, with a `later`
  line naming the day and the source, only once the state certifies them.
- No state is ever assumed certified because its deadline passed. A state the trackers
  call certified but whose own announcement wasn't found stays out.
- Wikipedia's counts on this site are its compilation, which may lag the certified
  canvass: pages say a state certified its results, never that the counts shown are the
  certified ones.

Finders, never cited: congresscountdown.com's certification tracker (deadlines from
Ballotpedia's 2026 calendar) and news round-ups such as The Center Square's (Nov. 24:
"22 states have certified", without naming them). No network; refresh_all.py runs every
file in scripts/research/ each time.

    py scripts/research/certified_2026.py
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "certified.json"
CHECKED = "2026-11-26"   # the last day the list was checked against the states' announcements
JURISDICTIONS = 51       # 50 states and D.C.


def cert(date, title, url, pending=None, other=(), later=()):
    out = {"date": date, "source": {"title": title, "url": url}}
    if pending:
        out["pending"] = pending  # race id -> "recount" | "runoff" | "legislature"
    if other:
        out["other"] = [list(x) for x in other]
    if later:
        out["later"] = [dict(x) for x in later]
    return out


STATES = {
    # Wyoming's results were certified on Tuesday, Nov. 10 (Wyoming Public Media's report
    # that day).
    "WY": cert("2026-11-10", "Wyoming Public Media: Wyoming certifies the general election as officials look to boost turnout",
               "https://www.wyomingpublicmedia.org/politics-government/2026-11-10/wyoming-certifies-the-general-election-as-officials-look-to-boost-turnout"),
    # Vermont's results were certified on Nov. 10 (WCAX's report that day).
    "VT": cert("2026-11-10", "WCAX: Vermont sets midterm turnout record as election results certified",
               "https://www.wcax.com/2026/11/10/vermont-sets-midterm-turnout-record-election-results-certified/"),
    # The State Election Commission certified the statewide general election on
    # Wednesday, Nov. 11 (WACH's report of Nov. 16; scVOTES.gov posts no release).
    "SC": cert("2026-11-11", "WACH: South Carolina certifies 2026 election results with more than 2 million votes cast",
               "https://abcnews4.com/news/local/2026-11-16-south-carolina-certifies-2026-election-results-with-more-than-2-million-votes-cast-early-voting"),
    # The State Canvassing Board certified every contest above the county level on Nov. 18.
    # The state House race in Legislative District 41 qualified for a recount that the
    # trailing candidate could demand until Nov. 21; none was asked for, so the certified
    # results stand (Deputy Secretary of State Sandy McMerty, in the North Dakota Monitor's
    # report republished by KVRR on Nov. 24).
    "ND": cert("2026-11-18", "North Dakota Secretary of State: State Canvassing Board Certifies 2026 General Election Results",
               "https://www.sos.nd.gov/news/state-canvassing-board-certifies-2026-general-election-results"),
    # The State Canvassing Board certified the U.S. Senate and House contests and the
    # state offices on Nov. 19; recounts in Congressional District 1 (Johnson leads Finstad
    # by 324 votes; Finstad asked for one) and Senate District 4, reviewed on Dec. 8.
    "MN": cert("2026-11-19", "Minnesota Secretary of State: State Canvassing Board Certifies Results of the 2026 General Election",
               "https://sos.mn.gov/about-the-office/news-room/state-canvassing-board-certifies-results-of-the-2026-general-election/",
               pending={"MN-H-01": "recount"},
               other=[("Minnesota Senate, District 4 (recount)", "Sénat du Minnesota, district 4 (recompte)")]),
    # Secretary of State Raffensperger certified the results on Friday, Nov. 20 (Capitol
    # Beat's report of Nov. 21). The state House race in District 151 goes to a Dec. 1 runoff.
    "GA": cert("2026-11-20", "Capitol Beat, via Rough Draft Atlanta: It's official: Raffensperger certifies Nov. 3 election results",
               "https://roughdraftatlanta.com/2026/11/21/raffensperger-certifies-georgia-election-results/",
               other=[("Georgia House, District 151 (runoff, Dec. 1)", "Chambre de Géorgie, district 151 (second tour le 1er décembre)")]),
    # The Board of State Canvassers certified the general election on Monday, Nov. 23.
    "MI": cert("2026-11-23", "Michigan Department of State: Michigan Board of State Canvassers certifies record-breaking 2026 General Election",
               "https://www.michigan.gov/sos/resources/news/2026/11/23/michigan-board-of-state-canvassers-certifies-record-breaking-2026-general-election"),
    # Utah's results were certified on Nov. 23 (Utah News Dispatch's report that day).
    "UT": cert("2026-11-23", "Utah News Dispatch: Utah's 2026 election results are certified, solidifying Democrats' gains in the Legislature",
               "https://utahnewsdispatch.com/2026/11/23/utahs-2026-election-results-are-certified-solidifying-democrats-gains-in-the-legislature/"),
    # The Secretary of State, the Governor, the Attorney General and the Chief Justice
    # conducted the official statewide canvass on Nov. 23 (the office's release that day).
    # The second House seat in Legislative District 27 (Fink 313 votes ahead of Rivero)
    # goes to the automatic recount that follows the canvass (KTAR).
    "AZ": cert("2026-11-23", "Arizona Secretary of State: Arizona Secretary of State's Office Releases General Election Voter Numbers",
               "https://azsos.gov/news/1092",
               other=[("Arizona House, District 27, second seat (automatic recount)", "Chambre de l’Arizona, district 27, second siège (recompte automatique)")]),
    # The state canvassing board certified the results on Nov. 23 and set a recount for
    # state Senate District 10 (Alabama Daily News).
    "AL": cert("2026-11-23", "Alabama Daily News: Officials certify election results, set recount for East Alabama's Senate District 10",
               "https://aldailynews.com/officials-certify-election-results-set-recount-for-east-alabamas-senate-district-10/",
               other=[("Alabama Senate, District 10 (recount)", "Sénat de l’Alabama, district 10 (recompte)")]),
    # The State Board of Elections voted 5-0 on Tuesday, Nov. 24, except two contests
    # under recount.
    "NC": cert("2026-11-24", "North Carolina State Board of Elections: State Board Unanimously Certifies Midterm Elections",
               "https://www.ncsbe.gov/news/press-releases/2026/11/24/state-board-unanimously-certifies-midterm-elections",
               other=[("District Attorney, District 21 (recount)", "Procureur de district, district 21 (recompte)"),
                      ("N.C. House, District 62 (recount)", "Chambre de Caroline du Nord, district 62 (recompte)")]),
    # The State Board of Canvassers certified the results on Nov. 24, with the
    # post-election audit's report (the Secretary of State's release).
    "ID": cert("2026-11-24", "Idaho Secretary of State: Board of Canvassers Certifies Election Results; Audit Results Reported",
               "https://press.voteidaho.gov/press-release/2026-results-certified-and-audit-report/"),
    # The State Canvassing Board certified the general election on Nov. 24.
    "NM": cert("2026-11-24", "New Mexico Secretary of State: State Canvassing Board Certifies 2026 General Election Results",
               "https://www.sos.nm.gov/2026/11/24/state-canvassing-board-certifies-2026-general-election-results/"),
    # The State Board of Canvassers certified the results on Nov. 24, unchanged from the
    # unofficial ones (Iowa Capital Dispatch). The governor's race (governor and lieutenant
    # governor run on one ticket) is canvassed by the Legislature when it meets in January.
    "IA": cert("2026-11-24", "Iowa Capital Dispatch: State of Iowa certifies 2026 election results, with no changes from unofficial results",
               "https://iowacapitaldispatch.com/2026/11/24/state-of-iowa-certifies-2026-election-results-with-no-changes-from-unofficial-results/",
               pending={"IA-GOV": "legislature"}),
    # The Board of Elections certified all results at its meeting of Tuesday, Nov. 24,
    # after recounts; a Glocester School Committee tie is left to the town council (Rhode
    # Island Current, Nov. 25).
    "RI": cert("2026-11-24", "Rhode Island Current: A tie for the Glocester School Committee highlights a shortcoming in state law",
               "https://rhodeislandcurrent.com/2026/11/25/a-tie-for-the-glocester-school-committee-highlights-a-shortcoming-in-state-law/"),
    # The Nevada Supreme Court finished the statewide canvass on Nov. 24 (the Secretary of
    # State's voter ID page, which dates the amendment's taking effect from it).
    "NV": cert("2026-11-24", "Nevada Secretary of State: Voter ID Implementation (the Supreme Court finished the statewide canvass Nov. 24)",
               "https://www.nvsos.gov/elections/election-information/voter-id-implementation"),
    # The Secretary of the State, the Treasurer and the Comptroller signed the canvass of
    # the congressional and legislative results on Wednesday, Nov. 25 (CT News Junkie,
    # citing CGS 9-315 and 9-319). The governor and the other statewide officers are
    # declared by the General Assembly in January (CGS 9-318), so their races wait.
    "CT": cert("2026-11-25", "CT News Junkie: CT Officials Complete Election Canvas, Declare Winners 'Duly Elected'",
               "https://ctnewsjunkie.com/2026/11/25/ct-officials-complete-election-canvas-declare-winners-duly-elected/",
               pending={"CT-GOV": "legislature", "CT-AG": "legislature", "CT-AUD": "legislature",
                        "CT-SOS": "legislature", "CT-TREAS": "legislature"}),
}

# Checked on Nov. 26 and still out: Oklahoma (its results page and site say "Official
# Results" with no date; the board was to meet on Nov. 10, and a schedule is not a
# source), South Dakota (its results site still says "Unofficial Results"), and Arkansas,
# Delaware, Florida, Hawaii, Indiana, Kentucky, Louisiana, Tennessee and West Virginia (no
# announcement or report found). Virginia's board certifies on Dec. 7, Mississippi's by
# Dec. 3 and Texas's between Nov. 21 and Dec. 7; most others in December.


def main():
    out = {"checked": CHECKED, "jurisdictions": JURISDICTIONS,
           "states": {st: STATES[st] for st in sorted(STATES)}}
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    pending = sum(len(s.get("pending", {})) for s in STATES.values())
    print(f"wrote {OUT.relative_to(ROOT).as_posix()}: {len(STATES)} of {JURISDICTIONS} certified, {pending} races pending")


if __name__ == "__main__":
    main()
