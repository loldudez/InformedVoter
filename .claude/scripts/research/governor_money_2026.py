"""Latest reported fundraising for governor candidates whose state filings Wikipedia
doesn't tabulate, from news reports of those filings. Writes
data/research/governor_money.json, which update_races.py merges onto the races.

A report's figures are shown as written, with their period: a quarter's haul or
cash on hand is never stretched into a campaign total, so these appear as notes
linked to the report rather than as the "Raised" figure. Every figure was checked
against the article's own text, Oct. 26, 2026. Candidates with no report found
(South Dakota's, for one) stay "not loaded yet".

    py scripts/research/governor_money_2026.py
"""

from common import write

AR = ("Steve Brawner’s column, Arkadelphian, July 23, 2026", "https://arkadelphian.com/2026/07/23/governor-has-money-opponents-had-debate/", "2026-07-23")
CO = ("Colorado Newsline, Oct. 8, 2026", "https://coloradonewsline.com/2026/10/08/weiser-democrats-fundraising-edge/", "2026-10-08")
CT = ("CT Mirror, Oct. 13, 2026", "https://ctmirror.org/2026/10/13/fazio-lamont-campaign-finance-report/", "2026-10-13")
HI = ("Hawaii News Now, July 11, 2026", "https://www.hawaiinewsnow.com/2026/07/11/new-campaign-spending-reports-show-fundraising-gaps-across-key-hawaii-races/", "2026-07-11")
IA = ("Iowa Public Radio, Oct. 20, 2026", "https://www.iowapublicradio.org/political-news/2026-10-20/zach-lahn-rob-sand-fundraising-iowa-governors-race-midterm-elections", "2026-10-20")
ID = ("Idaho Capital Sun, June 16, 2026", "https://idahocapitalsun.com/2026/06/16/idaho-gov-brad-little-reports-raising-more-campaign-money-than-all-other-statewide-candidates/", "2026-06-16")
IL = ("Chicago Sun-Times, Oct. 16, 2026", "https://chicago.suntimes.com/elections/2026/10/16/jb-pritzker-darren-bailey-illinois-governor-race-campaign-cash-spending", "2026-10-16")
KS = ("HPPR, Oct. 13, 2026", "https://www.hppr.org/2026-10-13/in-race-for-kansas-governor-masterson-and-holscher-focus-on-taxes-and-education-funding", "2026-10-13")
MA = ("Boston.com, Sept. 17, 2026", "https://www.boston.com/news/politics/2026/09/17/charts-see-how-much-gov-maura-healey-and-mike-minogue-have-raised-so-far/", "2026-09-17")
NE = ("Nebraska Examiner, Oct. 9, 2026", "https://nebraskaexaminer.com/2026/10/09/lindstrom-reports-50-spent-in-2026-ne-gubernatorial-campaign-the-total-is-likely-higher/", "2026-10-09")
NH = ("NHPR, June 18, 2026", "https://www.nhpr.org/politics/2026-06-18/ayotte-warmington-governor-election-2026-fundraising-nh-newhampshire", "2026-06-18")
NV = ("Nevada Current, July 17, 2026", "https://nevadacurrent.com/2026/07/17/billionaire-backers-help-secure-lombardo-campaigns-big-fundraising-advantage/", "2026-07-17")
OK_FOX = ("Fox 25 (KOKH), Aug. 18, 2026", "https://okcfox.com/news/local/gubernatorial-campaign-finance-reports-show-stark-contrasts-in-loans-donors-and-spending-mike-mazzei-gentner-drummond-cyndi-munson", "2026-08-18")
OK_VOICE = ("Oklahoma Voice, Oct. 21, 2026", "https://oklahomavoice.com/2026/10/21/democratic-gubernatorial-nominee-talks-trump-money/", "2026-10-21")
OR = ("Willamette Week, Oct. 22, 2026", "https://www.wweek.com/news/state/2026/10/22/pacs-and-megadonors-shift-millions-as-oregon-governors-race-enters-final-stretch/", "2026-10-22")
PA = ("City & State Pennsylvania, Sept. 23, 2026", "https://www.cityandstatepa.com/politics/2026/09/mind-gap-shapiro-raises-133m-latest-fundraising-period-garrity-brings-18m/416174/", "2026-09-23")
RI = ("Boston Globe, Oct. 7, 2026", "https://www.bostonglobe.com/2026/10/07/metro/rhode-island-campaign-finance-reports-october-2026/", "2026-10-07")
SC = ("SC Daily Gazette, Oct. 20, 2026", "https://scdailygazette.com/2026/10/20/sc-republicans-and-democrats-tout-their-fundraising-hauls-as-proof-of-momentum/", "2026-10-20")
TN = ("Tennessee Lookout, Oct. 15, 2026", "https://tennesseelookout.com/2026/10/15/2026-gov-race-hatley-puts-in-another-5m-blackburn-raises-2-1m-green-1m/", "2026-10-15")
VT = ("Seven Days, Oct. 16, 2026", "https://www.sevendaysvt.com/news/janoo-again-leads-gov-scott-in-fundraising-as-campaign-hits-home-stretch/", "2026-10-16")
WY = ("Cowboy State Daily, Aug. 12, 2026", "https://cowboystatedaily.com/2026/08/12/eric-barlow-earns-most-in-donations-for-gov-race-degenfelder-has-biggest-war-chest/", "2026-08-12")


def reported(report, note):
    outlet, url, date = report
    return {"source": outlet, "url": url, "asOf": date, "note": note, "parts": {}}


RACES = {
    "AR-GOV": {
        "AR-GOV:sanders": reported(AR, "Had raised $7.7 million in all by her June 2026 report, about $198,000 of it that month, and had $5.1 million left in the bank."),
        "AR-GOV:love": reported(AR, "Had raised $193,000 in all by his June 2026 report, $16,300 of it that month, and had $7,500 left in the bank."),
        "AR-GOV:shelby": reported(AR, "Had raised roughly $24,600 by his June 2026 report and had $30,500 left, including $10,000 he had lent the campaign."),
    },
    "CO-GOV": {
        "CO-GOV:weiser": reported(CO, "Raised nearly $1.7 million from July through September 2026, his best quarter since early 2025, and had $724,879 on hand on Oct. 1."),
        "CO-GOV:marx": reported(CO, "Reported just over $1.1 million in contributions from July through September 2026 and had $158,176 on hand on Oct. 1; the total reflects more than $61,000 refunded to donors who gave over the $1,450 limit."),
        "CO-GOV:lopez": reported(CO, "Had raised about $128,000 from supporters and lent his campaign $65,000, with $16,265 on hand on Oct. 1, 2026."),
    },
    "CT-GOV": {
        "CT-GOV:lamont": reported(CT, "Opted out of public financing and has largely paid for his campaign himself. Spent $10.6 million from July through September 2026 and $13.6 million since his campaign opened in 2025, with nearly $2.2 million on hand at the end of September."),
        "CT-GOV:fazio": reported(CT, "Runs on public financing: an $18 million Citizens’ Election Program grant arrived July 15. Spent $9.6 million from July through September 2026 and $10.6 million since his campaign opened, and began October with $8.4 million."),
    },
    # FL-GOV: every candidate's account is grouped by contributor from the state's
    # database in florida_money_2026.py.
    "HI-GOV": {
        "HI-GOV:green": reported(HI, "Had collected $3.5 million since his 2022 win and had $2 million on hand in the July 2026 reports."),
        "HI-GOV:cordery": reported(HI, "Had raised just over $300,000 and spent all of it, reporting $14,000 in debt, in the July 2026 reports."),
    },
    "IA-GOV": {
        "IA-GOV:sand": reported(IA, "Raised $16.3 million from July 15 to Oct. 14, 2026, $5.5 million of it from the Democratic Governors Association; spent $28.9 million and ended the period with $5.35 million on hand and no debt."),
        "IA-GOV:lahn": reported(IA, "Raised nearly $16.9 million from July 15 to Oct. 14, 2026, about $11.8 million of it from the Republican Governors Association’s PAC; spent $17.5 million and ended with about $403,000 on hand and $2.5 million in loans owed."),
    },
    "ID-GOV": {
        "ID-GOV:little": reported(ID, "Had raised $2,080,897.75 in 2026 as of June 15, about half of it from companies, and had about $958,000 on hand."),
        "ID-GOV:pickens": reported(ID, "Had raised $134,734.28 in 2026 as of June 15, nearly all of it from individuals, and had $45,335.84 on hand."),
        "ID-GOV:stegner": reported(ID, "Had raised $365,137.90 in 2026 as of June 15, more than any other challenger, and had $350,265.31 on hand."),
    },
    "IL-GOV": {
        "IL-GOV:pritzker": reported(IL, "Put about $65 million of his own money into his campaign over the summer of 2026, spent nearly $23.8 million from July through September and had $44.4 million on hand for the final month."),
        "IL-GOV:bailey": reported(IL, "Spent about $941,000 from July through September 2026; his campaign raised $1.2 million and entered October with about $482,000 in the bank."),
        "IL-GOV:corbett": reported(IL, "Entered July 2026 with about $379,000, raised $42,000, spent $386,000 and ended September with $35,000."),
    },
    "KS-GOV": {
        "KS-GOV:masterson": reported(KS, "The latest reports before Oct. 13, 2026 left his campaign with about $360,000 more in the bank than Holscher’s."),
        "KS-GOV:holscher": reported(KS, "The latest reports before Oct. 13, 2026 left her campaign with about $360,000 less in the bank than Masterson’s."),
    },
    "MA-GOV": {
        "MA-GOV:healey": reported(MA, "Had raised roughly $4.32 million and had about $6.3 million in the bank in the latest filings with the state’s Office of Campaign and Political Finance as of Sept. 17, 2026."),
        "MA-GOV:minogue": reported(MA, "Had raised about $13.42 million, including $11.8 million of his own money, and had $1.52 million in the bank in the latest filings with the state’s Office of Campaign and Political Finance as of Sept. 17, 2026."),
    },
    "NE-GOV": {
        "NE-GOV:pillen": reported(NE, "Raised $2.4 million, spent $4.4 million and had $7.5 million on hand in the June 17 to Sept. 29, 2026 report."),
        "NE-GOV:walz": reported(NE, "Raised $2.2 million, spent $2 million and had $860,464.44 on hand in the June 17 to Sept. 29, 2026 report."),
        "NE-GOV:lindstrom": reported(NE, "Raised $28,154.90, spent $16,049.50 and had $12,105.40 on hand in the June 17 to Sept. 29, 2026 report."),
        "NE-GOV:beard": reported(NE, "Has filed no campaign finance reports; Nebraska requires them only once a candidate raises or spends $5,000."),
    },
    "NH-GOV": {
        "NH-GOV:ayotte": reported(NH, "Had raised about $3.7 million overall, $1.6 million of it in 2026, with $2 million left to spend, as of the June 2026 filings."),
        "NH-GOV:warmington": reported(NH, "Had raised $635,000 overall, almost all of it since January, as of the June 2026 filings."),
    },
    "NV-GOV": {
        "NV-GOV:lombardo": reported(NV, "His campaign raised nearly $2.3 million from April through June 2026 and had just under $9.2 million on hand; two PACs allied with him raised another $14 million in the quarter."),
        "NV-GOV:ford": reported(NV, "His campaign raised about $1.4 million from April through June 2026 and had $2.6 million on hand; his allied PAC raised more than $1.1 million."),
    },
    "OK-GOV": {
        "OK-GOV:mazzei": reported(OK_FOX, "Had lent his campaign $11 million by Aug. 10, 2026, while individuals had given $1.4 million and PACs $25,000."),
        "OK-GOV:munson": reported(OK_VOICE, "Had raised about $1.7 million as of late October 2026."),
    },
    "OR-GOV": {
        "OR-GOV:kotek": reported(OR, "Raised nearly $20 million for the Nov. 3 election; the Democratic Governors Association gave $4.1 million this cycle."),
        "OR-GOV:drazan": reported(OR, "Raised $16 million in 2026; the Republican Governors Association gave $1 million."),
    },
    "PA-GOV": {
        "PA-GOV:shapiro": reported(PA, "Raised over $13.3 million from June 6 to Sept. 14, 2026, spent $31.8 million and had about $19.8 million on hand; more than $60 million raised this election cycle."),
        "PA-GOV:garrity": reported(PA, "Raised $1.8 million from June 6 to Sept. 14, 2026, spent $1.58 million and had a little over $1.3 million on hand."),
    },
    "RI-GOV": {
        "RI-GOV:foulkes": reported(RI, "Raised more than $529,000 from Sept. 2 to Oct. 5, 2026, including in-kind help from the state Democratic Party, and had $214,871 on hand; she has spent more than $6.3 million in the race."),
        "RI-GOV:block": reported(RI, "Has raised roughly $197,000 and lent himself $200,000 since entering the race in April 2026; had $263,515 on hand on Oct. 5."),
        "RI-GOV:guckian": reported(RI, "Raised less than $7,000 from Sept. 2 to Oct. 5, 2026 and had $7,273 on hand."),
        "RI-GOV:gotra": reported(RI, "Had $1,531 on hand in the Oct. 5, 2026 filings."),
        "RI-GOV:reynolds": reported(RI, "Had $0 on hand in the Oct. 5, 2026 filings."),
    },
    "SC-GOV": {
        "SC-GOV:wilson": reported(SC, "Raised $2.5 million from July 1 through Oct. 14, 2026 and had nearly $1.7 million to spend in the last three weeks."),
        "SC-GOV:johnson": reported(SC, "Raised more than $867,000 in the last pre-election report, his best of the campaign, and had about $136,000 on hand on Oct. 14, 2026."),
    },
    "TN-GOV": {
        "TN-GOV:blackburn": reported(TN, "Raised $2.1 million from the August primary through Sept. 30, 2026 and had $3.1 million for the final weeks."),
        "TN-GOV:green": reported(TN, "Raised nearly $1 million in the report through Sept. 30, 2026, her biggest of the campaign."),
        "TN-GOV:hatley": reported(TN, "Lent his campaign another $5 million in September 2026, $12 million of his own money in all, and had over $6.8 million to spend."),
        "TN-GOV:pinkston": reported(TN, "Raised around $150,000 in the report through Sept. 30, 2026."),
    },
    "VT-GOV": {
        "VT-GOV:janoo": reported(VT, "Had raised $888,000 this campaign, $181,670 of it from Sept. 29 to Oct. 12, 2026, with $307,000 on hand; she has taken no corporate donations."),
        "VT-GOV:scott": reported(VT, "Had raised $590,000 this campaign, $175,406 of it from Sept. 29 to Oct. 12, 2026, with $202,000 on hand; the Republican Governors Association gave $400,000 to a PAC running ads for him."),
    },
    "WY-GOV": {
        "WY-GOV:barlow": reported(WY, "Raised about $1.54 million through the August 2026 primary, $391,710 of it in 2025, with no loans."),
    },
}

write("data/research/governor_money.json",
      [{"id": rid, "financeOnly": True, "candidates": [{"id": cid, "finance": fin} for cid, fin in cands.items()]} for rid, cands in RACES.items()],
      "Reported fundraising for governor candidates from news coverage of state filings, read Oct. 26, 2026.", updated="2026-10-26")
