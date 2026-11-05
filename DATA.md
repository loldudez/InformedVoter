# How the race data is built

`data/races.json` holds every 2026 U.S. Senate, U.S. House and governor race. It is
**generated**: `scripts/update_races.py` rebuilds it every 8 hours (through
`scripts/refresh_all.py`), so don't edit it by hand. To add or correct
researched details, edit the research scripts described below.

Each race in `races.json` replaces the demo race with the same id and loses its
DEMO tag. State legislative races are not in it: they live in one file per state,
`data/legislature/ST.json`, loaded with that state's chamber map (see "State
legislative races").

## Where each piece comes from

| Data | Source | Notes |
|---|---|---|
| Candidates on the ballot, incumbents, partisan lean (Cook PVI) | Wikipedia's national 2026 Senate, governor and House pages | Used as an aggregator (CC BY-SA). Incumbents are identified by the Wikipedia article they link to. |
| Forecasters' ratings | The same pages' prediction tables (Senate, governors) and the House ratings page | Up to 11 outlets: Cook, Inside Elections, Sabato, Decision Desk HQ, The Economist, FiftyPlusOne, Fox News, NBC News, RealClearPolitics, Silver Bulletin, Split Ticket. |
| Polls | Each race's Wikipedia page (House: each state's page, by district) | Only tables whose every candidate is on the ballot, so hypothetical match-ups are skipped. One row per poll (likely-voter version preferred). Each poll links to the citation Wikipedia gives for it. |
| Published polling averages | The aggregator table on each race page | A check on our average, not an input. |
| Fundraising | FEC API when a key is set (see README); FEC financial summaries read on fec.gov for every Senate candidate and every House candidate with a 2026 report (`scripts/research/fec_2026.py`, `fec_house_2026.py`); otherwise the FEC totals cited in Wikipedia's fundraising tables | See "Money by source". Governors: totals from state filings via Wikipedia, without a breakdown; Florida's from the state's own database, grouped by source (`florida_money_2026.py`); where neither exists, the latest news report of the filings as a dated note (`governor_money_2026.py`). |
| Campaign websites | Each race page's "External links" list of official campaign websites, such as "Ted Brown (L)" (`campaign_sites` in `scripts/lib/elections.py`) | Attached when the name (and major party, where given) matches one candidate without doubt. A researched `officialSite` wins; `officialSite: null` in an overlay drops a dead link. California's page lists none, so `scripts/research/campaign_sites_2026.py` adds links from candidates' own Wikipedia articles and BallotReady profiles, kept only when the site answers and shows the candidate's name. |
| National environment | Generic congressional ballot average on the Senate page | Feeds the partisan baseline. |
| Seats held today | Wikipedia's party summaries for the 119th Congress; governors from the 36 races plus the 14 not on the ballot | Expected gains are measured from these. |
| Who sits in Congress (the seat charts on `#/congress`) | The House Clerk's member list (`MemberData.xml`: party, caucus, state, district, vacancies and why, delegates); Wikipedia's "List of current United States senators" (senate.gov refuses scripts) and each chamber's infobox for its leaders and which side the independents caucus with; Wikidata for the President (P35 of Q30) | `scripts/update_congress.py`, once a day; keeps the previous file when the Clerk's list or the senators' table can't be read. Democrats blue, Republicans red, independents gray, with the side they caucus with in the tooltip. |
| Candidates' photos | Wikidata's image (P18) for the Wikipedia article each candidate's name links to (`wiki`), on Wikimedia Commons with its author and license (`scripts/lib/wikiphotos.py`, shared with the France section) | `scripts/update_photos.py` → `data/photos.json`, once a day, answers cached a week in `data/cache/wiki/photos.json`. Kept only when the item is a person, a U.S. citizen wherever Wikidata gives a citizenship, and the article's title carries the candidate's last name. Shown in gray with the credit in the tooltip and a "Photo credits" list on each page; candidates without one keep their initials. The President's and Congress leaders' photos sit in `data/congress.json`. |
| House members' positions | The House Clerk's roll-call XML for 39 votes (2021 to 2026) | See "Positions from votes". |
| Betting market | Polymarket's Senate and House control markets | A cross-check shown beside the model, never an input. |
| Projected votes | 2024 presidential votes by state × 0.75 (House: divided by districts) | Midterm turnout ran 0.71 of the presidential vote in 2022 and 0.85 in 2018. |
| Early vote | The University of Florida Election Lab's 2026 tracker (Michael McDonald): `US.csv` for states, `ST_cd.csv` for House districts (`scripts/lib/early_vote.py`) | Refreshed with the races. Districts only where the file covers every district and 98% of the state's ballots. CC BY-NC-ND: credited on every Early vote tab, no commercial use, so since the site carries ads (Nov. 3, 2026) it is neither read nor shown: `EARLY_VOTE` in `update_races.py` and `SHOW_EARLY_VOTE` in `js/config.js` are off, to be turned back on together. |
| Elections email reminders may cover | Election Day and the runoffs in `data/races.json`; the French elections in `data/fr/calendrier.json` whose dates are fixed | `scripts/update_reminders.py` → `data/reminders.json`, every refresh, no network. The mail service (`services/mail/Code.gs`) reads it from the live site, so its emails carry the site's names and dates, never a visitor's text. |
| State legislative races | Each chamber's 2026 Wikipedia page, such as "2026 Michigan House of Representatives election" (`scripts/lib/legislature.py`) | Seats on the ballot, holders, 2024 presidential margins, November candidates where listed, forecasters' district ratings. No win odds. |
| Results (from Nov. 3, 2026) | Calls: the green check marks in Wikipedia's national Senate, governor, House and down-ballot office tables. Counts: each race page's general-election box, which cites the official returns (`scripts/lib/results.py`) | A race is decided only when a national table check-marks its winner; counts alone never call one. Counts are unofficial until each state certifies them. See "Results". |
| Statewide offices below governor | Wikipedia's national 2026 attorney general, secretary of state, lieutenant governor, state treasurer and state auditor pages (`scripts/lib/offices.py`) | → `data/offices.json`. Candidates, holders, Sabato's Crystal Ball ratings, results, and the race pages' polls, money and campaign sites. No win odds. See "Statewide offices below governor".

Wikipedia pages are cached by revision in `data/cache/wiki/`, so a refresh only
downloads pages edited since the last one (about 30 requests on a quiet day).
Wikimedia's 2026 limits allow a script 200 requests a minute when its User-Agent
gives a contact and 10 when it doesn't, so without a contact
(`INFORMED_VOTER_CONTACT` or `~/.informed-voter/contact`, see README) requests go
out 7 seconds apart, and a 429 or 503 waits out the Retry-After it carries.

## The forecast

1. **Baseline (expected margin).** Where forecasters rate a race, each rating sets a
   band: Safe/Solid 15+ points, Likely 7-15, Lean 3-7, Tilt 0.5-3, Toss-up within 2.
   The partisan lean (2 × PVI + the generic ballot margin) places the race inside
   each band, and the outlets are averaged (`priorKind: "ratings"`). Unrated House
   races start from the lean alone, at least 15 points toward the favored party
   (`priorKind: "pvi"`). One-candidate races are `"uncontested"`.
2. **Polls.** Recency-weighted average (14-day half-life), weighted by sample size
   and voter screen (LV > RV > A); a poll without a sample size counts as 600. The
   average gets up to 85% of the say as polling accumulates.
3. **Uncertainty.** A typical miss of 7 points (statewide) or 8 (district) for rated
   races without polls, 9 or 11 for unrated ones, narrowing to 5.5 or 7 with plenty
   of polls, plus drift for the days left.
4. **Chamber control.** 20,000 simulated elections, each with one shared national
   polling miss of 3.5 points, so races move together. Democrats need 51 Senate seats
   (the vice president breaks ties), 218 House seats and 26 governorships.

**Who the margin is between.** Candidates are ordered by their latest poll share,
then incumbency, then money. The baseline margin is between the strongest
Republican and the strongest non-Republican, which is usually the Democrat but an
independent where one leads the opposition (Nebraska's and Montana's Senate races).
The margin reads "D +x" only when a Democrat and a Republican are the top two;
otherwise it is the leader's margin.

**Ranked-choice races** (Alaska; Maine's Senate and House races, `rcv: true`): the
forecast models the final round, adding each party's other candidates' votes to its
strongest candidate. Independent and third-party votes stay put. Candidate cards
show both rounds.

`scripts/lib/model.py` is a line-for-line Python copy of `js/model/forecast.js`.
Each race carries the Python result (`modelCheck`); the site re-runs the
JavaScript model at the same moment and reports any disagreement on the About page.

**Open primaries** (Louisiana's House races this year) get no win probabilities:
the site shows the field, the polls as published, forecasters' ratings and the
expected split between the parties.

## Automatic checks

Every refresh writes `data/status.json`, shown on the About page:

- every race on the ballot was found (35 Senate, 36 governor, 436 House);
- seats held plus seats on the ballot add up to 100 and 50;
- every race has an expected margin;
- the model's favorite matches the forecasters' consensus (a few disagreements are
  allowed: they are races where polls point the other way);
- our polling average is within 4 points of the published averages;
- expected seats fall within the range of each forecaster's own seat count;
- control odds are within 20 points of the betting market (after Election Day, a note
  of the final forecast next to the settling market instead);
- the national environment was found, and fundraising data is current;
- close statewide races have a poll from the last 30 days (after Election Day, from
  the campaign's last 30 days);
- from Election Day on: how many races each table has called and how many race pages
  have counts, that every check-marked winner leads its count (or is one of the two
  advancing to a runoff; ranked-choice winners can trail the first round, so they
  aren't held to it), and which boxes' shares were worked out from their votes.

`scripts/validate_races.py` then checks the file itself (stances, sources, poll
fields, baseline shares, donation links). If it fails, `refresh_all.py` restores
the last good files.

## Positions from votes

Every current U.S. House member on the ballot gets positions from these votes,
each linked to its roll call on clerk.house.gov:

| Vote | Question | Yes | No |
|---|---|---|---|
| Respect for Marriage Act (2022) | soc-10 | +2 | -1 |
| Women's Health Protection Act (2022) | soc-03 | +2 | -1 |
| ACA premium tax credit extension, H.R. 1834 (2026) | hea-07 | +2 | -1 |
| Inflation Reduction Act (2022) | hea-02; hea-07 without the 2026 vote | +1 | -1 |
| Infrastructure Investment and Jobs Act (2021) | eco-06 | +1 | -1 |
| CHIPS and Science Act (2022) | agr-02 | +1 | -1 |
| H.R. 1 (2025), which cut Medicaid | hea-03 | -1 | not used |
| Ukraine aid, H.R. 8035 (2024) | def-13 | +2 | -2 |
| Ukraine aid, H.R. 2913 (2026) | def-13 without the 2024 vote; def-14 | +1 | -1 (def-13 only) |
| Israel aid, H.R. 8034 (2024) | def-12 | +2 | -2 |
| ICC sanctions, H.R. 23 (2025) | def-11 | +1 | not used |
| Rescissions package, H.R. 4 (2025) | def-10 | +1 | -1 |
| Secure the Border Act (2023) | imm-01 | +1 | not used |
| Laken Riley Act, S. 5 (2025) | imm-07 | +1 | not used |
| Fracking, H.R. 26 (2025), then LNG exports, H.R. 1949 (2025) | ene-03 | +1 | -1 |
| Lower Energy Costs Act (2023), when neither is cast | ene-03 | +1 | not used |
| Methane fee repeal, H.J.Res. 35 (2025) | ene-06 | -1 | +1 |
| California clean-car waiver repeal, H.J.Res. 88 (2025) | ene-04 | -1 | +1 |
| Protection of Women and Girls in Sports Act, H.R. 28 (2025) | soc-12 | -1 | +1 |
| Gender-transition treatment of minors as a federal crime, H.R. 3492 (2025) | soc-11 | -2 | +1 |
| Critical minerals, H.R. 4090 (2026) | agr-05 | +1 | not used |
| Farm bill, H.R. 7567 (2026) | agr-01 | +1 | not used |
| Ending the Canada tariff emergency, H.J.Res. 72 (2026) | eco-10 | -1 | +1 |
| Balanced budget amendment, H.J.Res. 139 (2026) | eco-07 | +1 | -1 |
| Stock-purchase ban with a voter photo ID requirement, H.R. 7008 (2026) | gov-02, gov-05 | +1 | not used |
| Union bargaining: federal workers' rights, H.R. 2550 (2025), and first-contract deadlines, H.R. 5408 (2026) | eco-09 | +2 if every vote cast is yes | -2 for no on both, -1 for a single no; a split is 0 |
| 11 war powers resolutions, 2025-26 (Western Hemisphere, Venezuela twice, Lebanon twice, Iran six times) | def-04; the six Iran votes also def-15, reversed | see below | |

A question answered by several rows takes the first one the member cast, in the
order listed. War powers votes count as a run: all one way gives ±2 with three or
more votes (±1 with fewer), at least 75% one way gives ±1, anything less is 0, and
the source names the votes and how the member cast them. "Not used" marks bills
where a no vote could mean many things (omnibus packages, or a bill that pairs two
issues). The 2025-26 votes give members first elected in 2024 about 20 positions
each. The rules live in `scripts/lib/house_votes.py`. Former members on the 2026 ballot
whose service overlaps these roll calls are named by the Clerk's member id in
`FORMER_MEMBERS` (`update_races.py`: Mary Peltola, Jerry Carl, Colin Allred, Elaine
Luria), checked by hand because a name search also finds relatives and namesakes. When
a sitting member shares a surname with a predecessor the Clerk lists by surname alone
(Adelita and Raúl Grijalva), the one in the latest roll call is used.

## Researched races (overlays)

Hand-researched details live in `data/research/*.json`, written by the scripts in
`scripts/research/`: one per state for the competitive races (`alaska_2026.py`,
`texas_2026.py`, ...), plus `safe_races_2026.py` (safe Senate races and the senators
running for governor), `governors_2026.py` (safe governor races),
`positions_2026.py` (more positions for candidates who had few, from their campaign
sites' issue pages, signed bills and news coverage), `house_2026.py` (both main
candidates in every House race rated Toss-up, Tilt or Lean by any forecaster:
guides.vote voters guides where they exist, campaign issue pages elsewhere, news
reports when a site lists no issues) and `fec_2026.py` (money by source, see above).
`candidates_2026.py` (third-party and independent Senate and governor candidates) and
`house_challengers_2026.py` (House challengers outside the competitive races: 584
candidates, Oct. 26-27) cover only some of each race's candidates, so they are
`partial`. Their sources: campaign sites (those that render only in a browser were
read in the browser pane), newsroom voter guides, KQED's candidate summaries (four
Northern California races), KATU's "Know Your Candidates" interview transcripts
(Oregon and southwest Washington) and VOTE411, the League of Women Voters' guide, whose
candidates answer the League's questions in their own words; VOTE411 renders in a
JavaScript widget, so it was read race by race in the browser. Where a guide prints a
candidate's own answers, they are quoted; where it summarizes in its own words (Iowa
Capital Dispatch, Maine Morning Star, Alabama Reflector, Tennessee Lookout, Virginia
Mercury, Oklahoma Voice, KQED), the summary is the source title and only the
candidate's own words are quoted. `ivoterguide_2026.py` adds candidates' own answers to
iVoterGuide's questionnaire (244 candidates). iVoterGuide is run by AFA Action, the
American Family Association's advocacy arm, so only the candidates' agree/disagree
answers and multiple-choice picks are used, never its ratings, and only for the
statements that ask what one of the site's questions asks; its docstring lists each
statement, the question it answers and the cap on its stance. It adds a question only
where the candidate has no other source for it, so it is regenerated after hand
research. `campaign_sites_2026.py` adds only campaign links (117, mostly
California's), from candidates' Wikipedia articles and BallotReady profiles, each
checked live; the other overlays set `officialSite` for sites found in guides.
Overlays are merged in file-name order, case-insensitively.
`update_races.py` merges each overlay onto the automatic race with the same id;
researched positions are added to the automatic vote positions, winning where both
answer a question. To add a race, copy one of these scripts, keep every source next
to the stance it supports, run it, then run `py scripts/update_races.py`.

`scripts/research/common.py` builds the sources so each one names its evidence:

| Helper | Use |
|---|---|
| `guide(name, url, read_on)` | A guides.vote voters guide, which ties each stance to a vote, bill or statement. |
| `article(outlet, url, date)` | A news report, debate story or newsroom candidate questionnaire, dated when published. |
| `page(title, url, read_on)` | A live page (campaign site, OnTheIssues), dated when read. |
| `vote_positions(member, votes)` | Recorded House votes, by the rules above. |
| `senate_vote_positions(member, url, votes, read_on)` | Key Senate votes as Ballotpedia lists them (senate.gov refuses scripted reads). Same rules as the House votes: `SENATE_RULES` maps the marriage, abortion-rights, Inflation Reduction Act, infrastructure, CHIPS, 2025 tax law, 2024 foreign aid, Laken Riley, voting-rights, 2024 border, retirement-ESG and PACT Act votes; ambiguous "no" votes are not used. |
| `combine(auto_rows, *rows)` | Hand-researched rows plus vote rows, the hand-researched ones winning. |

| Overlay field | What it does |
|---|---|
| `candidates[]` | Matched to the automatic candidates by id, then by name. Adds `bio`, `officialSite`, `donateUrl`, `positions`, `aliases`, `incumbent`; `finance` too, unless the automatic figures are newer (equal totals count as the same report, so the overlay's breakdown and true report date win). Researched ids replace automatic ones everywhere in the race. Two research files may cover one race: candidates merge by id and positions pool by question. |
| `financeOnly: true` | The overlay adds money only (`fec_2026.py`): the race is not marked researched, so matching stays off where positions are missing. |
| `partial: true` | The overlay researches only some of the race's candidates: positions and bios are added, but the race is not marked researched unless another file covering it is. |
| `officialSite: null` (candidate) | Drops the campaign link the refresh found, for a domain that is dead or parked. It survives merging with later research files, where any other `null` means "not researched here". |
| `name` (candidate) | Replaces the automatic name, for spellings Wikipedia gets wrong (Dave Wood, CO-8; Maria Rodriguez, KY-3; Timothy Teagan, MI-6). The id stays the same. |
| `candidatesOnly: true` | The researched list is the qualified list: automatic candidates not on it are dropped, with a note in the refresh log (used where Wikipedia's list was wrong). |
| `aliases[]` (candidate) | Old candidate ids, so visitors' saved likes follow the candidate. |
| `polls[]` | Merged with the automatic polls; the researched version of the same poll (pollster and end date) wins. Poll fields: `sponsor`, `url`, `note`, `approx` (shows "~" before the sample size). |
| `excludePolls[]` | Pollster names to leave out of the average (e.g. a poll whose only source is a social media post). |
| `notes[]` | Context lines under the headline (`text`, optional `source` and `url`). |
| `earlyVote` | `ballots`, `pctOfTurnout`, `asOf`, `label`, `byParty` (registration shares in percent), `mail` and `inPerson` (only when both are reported), `of2022` (ballots as a share of the 2022 total vote), `note`, `source`, `stateSource`. The refresh fills it from the UF Election Lab (`scripts/lib/early_vote.py`); an overlay's figure is used only when it is newer. |
| `turnout`, `format`, `runoff`, `open`, `districtName` | Override the automatic values. |
| `ratings[]`, `ratingsSource` | Used only when no automatic ratings exist. |

### Race ids

| Race | Id | Example |
|---|---|---|
| U.S. Senate | `ST-SEN` | `GA-SEN` |
| Governor | `ST-GOV` | `GA-GOV` |
| U.S. House | `ST-H-DD` (two digits; at-large `00`; D.C. `98`) | `TX-H-23` |
| State senate | `ST-SS-CODE` | `TX-SS-014` |
| State house | `ST-SH-CODE` | `MA-SH-001` |
| Nebraska Legislature | `NE-LEG-CODE` | `NE-LEG-002` |
| Statewide office below governor | `ST-AG`, `ST-SOS`, `ST-LG`, `ST-TREAS`, `ST-AUD` | `AZ-AG` |

Candidate ids are `RACEID:surname` (`TX-SEN:talarico`), or `RACEID:full-name` when
two candidates share a surname (`AK-SEN:dan-s-sullivan`).

### Position fields

- `stance`: 2 strongly supports, 1 supports, 0 neutral or mixed, -1 opposes, -2 strongly opposes.
- `source`: `title`, `url` (https), `date`; `accessed: true` when the date is when a live page was read; optional `quote` (the candidate's own words, 25 words at most).
- Question ids: `eco-01`..`13`, `hea-01`..`10`, `edu-01`..`10`, `imm-01`..`10`, `cri-01`..`10`, `soc-01`..`12`, `ene-01`..`10`, `def-01`..`17`, `gov-01`..`13`, `hou-01`..`11`, `agr-01`..`08`, `sta-01`..`12` (see `js/data/questions.js`). Federal races skip `sta`, state races skip `def`.

## Rules for positions

Each stance needs a source a reader can open: the candidate's own website, a
recorded vote, a bill they signed or wrote, a questionnaire they answered, a
debate, or a news report of their stance. Never infer a stance from party. If a
statement is ambiguous, leave the question out; it shows as "unclear" and is kept
out of the score. Below 5 documented positions a candidate gets no match score,
and races where not every candidate has been researched offer no side-by-side match.

## Money by source

Each candidate's money follows the lines of their FEC report (Form 3, all reports
for the 2026 election), mapped to the Money tab's categories:

| Site category | FEC lines |
|---|---|
| Small donors | Unitemized individual contributions (under $200) |
| Large individual donors | Itemized individual contributions |
| PACs | Other committee contributions (corporations can't give directly; this is where business, labor and issue PACs show up) |
| Party committees | Party committee contributions |
| Self-funding | Candidate contributions plus loans made by the candidate |
| Public financing | Always 0 for Congress |
| Transfers | Transfers from other authorized committees: joint fundraising committees and the candidate's earlier campaigns |
| Other | Other loans, offsets to operating expenditures (refunds) and other receipts |

Each line is rounded to the dollar on its own, so the parts can miss the total by a
few dollars; they are never padded to match. The validator warns when the parts and
total differ by more than $10 or 0.1%. "Other" can come out negative when a filing
reports negative other receipts; the chart leaves it out and the card says why the
rest adds up to more than the total. `fec_2026.py` holds the summaries read on
fec.gov on Oct. 25, 2026 (coverage mostly through Oct. 14): every Senate candidate with
money, Louisiana's 6th District and the 77 House races at least one forecaster rates
Toss-up, Tilt or Lean. `fec_house_2026.py` adds every other House candidate whose FEC
page shows 2026 receipts (read Oct. 26), each matched by state, district and last name
and checked against the page's own name and seat. A newer API report replaces them
automatically. Missing figures are not evidence that a candidate has filed nothing:
the Money tab says the figures haven't loaded and links to an FEC search, and only a
researched note may say "no report on file". A $0 total counts as a figure only with
the filing's coverage dates (`hasFigures` in `js/data/world.js`); Wikipedia lists some
candidates who have filed nothing at a bare $0.

Governors whose state filings Wikipedia doesn't tabulate get the latest news report
of those filings (`governor_money_2026.py`): each candidate's figures as the report
gives them, with their period and a link, shown as a note instead of a "Raised" total.

Florida's governor candidates come from the state itself (`florida_money_2026.py`):
the Division of Elections database itemizes every contribution, so each campaign
account is grouped by who gave. State matching funds (Florida matches Floridians'
gifts of $250 or less for candidates who accept spending limits) are public
financing; the candidate's own money and loans, self-funding; the state and county
parties, party committees; businesses, unions, PACs and clubs (by words in the name
or an occupation such as "POLITICAL ORGANIZATION"), the PAC line, since Florida lets
corporations give to state candidates directly; people whose gifts total $200 or less,
small donors, and the rest large donors. Refunds are netted against the giver.
"Spent" is the sum of the account's expenditures. Each major candidate's political
committee raises unlimited money separately; its total and largest givers are in
the note, never in the account's figures. The script reads the database at most
once a day (the refresh runs it each time; `--force` refetches).

House candidates with nothing to show get a researched note from an FEC search
(`fec_notes_2026.py`, Oct. 26): the FEC lists them but has no 2026 report yet, or no
FEC record for them in that district turned up (candidates who raise or spend under
$5,000 don't have to register). A note never replaces figures: `update_races.py`
uses a note-only overlay only while the candidate has no figures, so a report that
arrives later (from the API once a key is set) shows instead.

## State legislative races

`scripts/lib/legislature.py` reads each chamber's 2026 Wikipedia page during the
refresh (88 chambers in the 46 states with legislative elections) and writes
`data/legislature/ST.json`, one file per state, which the site loads with that
state's chamber map. Districts are matched to the Census map by number ("1st",
"District 1A", "A") or by name ("1st Barnstable", "Addison-1", "Belknap 1").

| What | Where it comes from |
|---|---|
| Seats on the ballot, holder and party | The page's district summary table. Where every seat in the chamber is up, a district the page doesn't cover is still listed, with its candidates "not listed yet". |
| 2024 presidential margin | The summary table's "2024 Pres." column, where the page has one |
| November candidates | In order: the district's general-election box (found by its caption), a "Candidates" column, the district's election infobox, Pennsylvania's combined candidate table, each party's "Nominee" or "Advanced to general" list, and finally the bold winners in the district's primary boxes. Lists of declared primary candidates are never used. |
| Party | The candidate's listed party; where a page marks it only with the color of a "▌" marker (Colorado, Oklahoma), the color. Unknown colors stay "Party not listed". |
| Forecasters' ratings | District rating tables (State Navigate, Capitol Inside, Marquette) where a page has them |

These races carry `format: "field"` and get no win probabilities: almost none are
polled and few are rated, so a forecast would invent precision. The map colors
districts by their 2024 presidential margin, or by the party holding the seat where
a chamber's page has no margins. A race built from nominee lists or primary winners
says that an independent or unopposed candidate may be missing. Candidates' money
isn't loaded for these races. Researched candidates (bios, campaign sites and
positions) go in `data/research/legislature/*.json`, written by
`scripts/research/legislature_2026.py` and merged by race id; a candidate the page
doesn't list is added with a warning, and the race counts as researched only when
every candidate has positions (which turns on its "Where they stand" tab and the
side-by-side match).

## Results

From Election Day (polls close Nov. 3, 2026, 8 p.m. local time: `ELECTION_DAY` in
`js/model/forecast.js`) every race can carry a `result`, built by
`scripts/lib/results.py` during the refresh:

| Field | What it holds |
|---|---|
| `status` | `won` (a national table check-marks the winner), `runoff` (two candidates check-marked for one seat, or listed under "Runoff:" in Louisiana's open primaries) or `counting` (votes posted, nobody marked) |
| `winners`, `advance` | Candidate ids of the check-marked winners and of the candidates going to a runoff |
| `rows` | The race page's general-election box as published, in its order: candidate id, name, party, votes, share, the running mate (`mate`) where a governor's box names one, and `final` (the last round's share) where a ranked-choice tabulation repeats "Votes \| %" per round. Write-in and "other" lines, and names not on the candidate list, have no id |
| `total`, `reporting` | Total votes, and the share of the vote reporting when the box's caption gives one |
| `precincts` | The share of precincts reporting, when that is all a caption gives (never used as a share of the vote) |
| `official`, `countAsOf` | Set when the count comes from the state itself (California, below), with the state's reporting time |
| `outcome`, `note`, `flip` | "Democratic gain", "Republican hold"; the table's status text; whether the winner's party differs from the holder's |
| `source`, `page` | The official returns the box cites; the Wikipedia page read, with its last edit |
| `sharesFromVotes` | Set when the box's percentages didn't match its counts (Iowa's governor box printed 55.5% and 45.5%), so the shares were worked out from the votes |
| `via`, `totalFromShares` | `via: "infobox"` when a statewide race page's results box is still blank and the count comes from its infobox instead (below); `totalFromShares` when the infobox lists only the leading candidates, so the total is worked out from their votes and shares and an "Others" line takes the share that remains |

**The infobox while the box is blank.** On the night of the count, editors often fill a
statewide race page's infobox first ("Reporting 96% as of 6:32 PM EST", citing the AP
and the New York Times, then each leading nominee's "Popular vote" and "Percentage")
and leave the results box blank. `page_box` in results.py reads the infobox only then,
only for Senate, governor and office pages (a state's House page has one infobox for all
its districts), and only when it is dated November 3, 2026 (never a primary's or a
December runoff's): every nominee it names needs votes and a share, and the shares may
not add up to more than 100.5. When they add up to less than 99.95, the total is the
nominees' votes over their shares, rounded to what the printed shares allow (to the
hundred with two decimals, the thousand with one), and "Others" takes the rest; it reads
"About 948,600" on the page. The "Reporting" line becomes `reporting` (or `precincts`
if it says so), and its first cited source becomes `source`. As of Nov. 4, 2026 this
gave counts to 86 statewide races, the four uncalled ones among them (Mississippi's
Senate race: Colom 49.01%, Hyde-Smith 48.89%, 96% reporting).

A race with no mark and no count after Election Day shows "No result yet". The
final forecast stays on every race page ("The final forecast", with the waffle and
stat tiles) and is compared with the count once there is one.

On the site, `resultsIn()` (js/data/world.js) switches maps and lists to results
once any real race has one: the home map and each state's House map open on
**Results** with a **Final forecast** switch (remembered for the visit, `setMapView`);
winners take their party's color, flips the same color with stripes (an SVG pattern,
one id per map), the leader of an uncalled count a lighter tint, runoffs gray
hatching, and races without a result plain gray. The seat tallies count called races
plus the seats not up this year (`holdover` in `control.json`, the same rule as
`seat_tally` in update_races.py); independents are counted apart, since a result
doesn't say whom a newly elected independent caucuses with. Close elections becomes
"Results within 5 points", and My elections, starred races and liked candidates show
each race's result.

### Counts from the states

`scripts/lib/official_results.py` reads a state's own count where a script can: so far
California, whose Secretary of State publishes JSON (`api.sos.ca.gov/returns/<contest>`)
for the governor, the five statewide offices and all 52 House districts (58 contests).
The governor's contest is read first; the rest only when its reporting time has moved
since the last read (cached in `data/cache/official/ca.json`), 0.3 seconds apart, under
the User-Agent "InformedVoterResearch/1.0". A state's count replaces the race page's box
only when its top two names match the race's candidates; it recomputes the shares, drops
`reporting`, `precincts` and `sharesFromVotes`, and links the state's own results page
(`electionresults.sos.ca.gov`, which a script can't read) as the source. Calls still come
only from Wikipedia's check marks. "Precincts reporting" is never read as a share of the
vote: California counts mail ballots for weeks after every precinct has reported.

### Projections from the count

A race counted but not called (`status: counting`) gets a projection, `live()` in
`js/model/forecast.js`, mirrored by `live()` in `scripts/lib/model.py`:

- **How much is counted** (`frac`): the share reporting where the results give one
  (`basis: "reported"`); otherwise the votes counted over the expected turnout
  (`race.turnout`: the state's 2024 presidential vote × 0.75, shared among its districts
  for House seats), tried at five turnouts, 20% (one standard deviation) either side at
  the 10th, 30th, 50th, 70th and 90th percentiles, and never above 98% counted
  (`basis: "estimated"`).
- **The votes still out** lean like the count in proportion to the share counted, and like
  the final forecast otherwise. Their uncertainty runs from the forecast's own (`sigma`)
  when little is counted to 12 points (`REST_SD`) near the end, when the last ballots
  (provisional, late mail) can lean differently, plus 0.3 points for the count itself
  (`COUNT_SD`).
- The chance (`pLead`) is the average over the five turnouts. The projected leader is
  whoever has at least an even chance, so the projected margin's sign can differ from it
  in a near-tie (the page then says "About even"). Shares, the margin and its 80% range
  come from the same blend.
- Ranked-choice races are projected on their final round, as they are forecast; open
  primaries and races without odds get none.

Every counted race carries `modelCheck.live` (`lead`, `pLead`, `margin`, `frac`) from the
Python copy, which the browser checks like the forecast (pLead within 0.002, the margin
within 0.02); the About page reports any mismatch. The final forecast itself is frozen at
poll closing (`forecast_as_of`, `forecastAsOf`: the earlier of now and `ELECTION_DAY`), so
late polls or rating changes never move it.

**Chamber projections** (`control.json`, `projection` in each chamber, after Election
Day): called seats count as they are, and each race still out is drawn on its own,
20,000 times: a counted race by its projected chance, a runoff between the parties by the
seat's lean, any other by its final forecast (`projection_entries` and `project_control`
in model.py). Fields: `pD`, `pR`, `pNone` (each side's chance of a majority, or neither),
`meanD`, `meanR`, `medianD`, `medianR`, `range80D`, `range80R`, `sims`, and `asOf`,
`open` (races still out), `counting` (with a projection) and `runoff`. Races are drawn
independently, so the 80% range is probably a little narrow.

### Results every 10 minutes

`scripts/update_results.py` (README, "Results every 10 minutes") rebuilds only the
results, projections and seat tallies between full refreshes, and stamps when:
`resultsUpdated` in `status.json`, `control.json` and both files' `meta`;
`nextResultsMinutes` in `status.json` (10 while any race is open, null after);
`resultsWarnings` (its last run's warnings, at most 50). Its own status checks start with
"results" and replace the previous run's. The pages re-read `status.json` every 10
minutes while anything is being counted (`refreshData` in js/data/world.js) and redraw
the views marked `live`.

## Statewide offices below governor

`scripts/lib/offices.py` reads Wikipedia's national 2026 pages for attorney general,
secretary of state, lieutenant governor, state treasurer and state auditor (the
comptroller or controller where the state calls it that): each "Race summary" row
gives the state, the officeholder and party, a status and the candidates, check-marked
once called, and links the race's own page, where the refresh reads the results box,
polls, money and campaign sites like any race page. The "Predictions" table carries
Sabato's Crystal Ball, the one outlet that rates these races; its rating is shown as
is (`consensus`), with no margin or odds drawn from it. Lieutenant governors elected
on a ticket with the governor are not separate races (the governor's results box
names the running mate).

The races go to `data/offices.json` with `format: "office"`, `level: "state"` and ids
`ST-AG`, `ST-SOS`, `ST-LG`, `ST-TREAS` and `ST-AUD`. Like state legislative races
they get no win probabilities (almost none are polled), only the state's 2024
presidential margin for context, any rating, and the results. They appear in the
state pages' "Statewide offices" list, in My elections after the governor, and on
their own race pages, where the match with My views uses the state-level questions
(as for governors: defense and foreign policy are left out).

Research overlays merge into them exactly as for federal races.
`scripts/research/offices_2026.py` (→ `data/research/offices.json`) holds positions
from the States Newsroom voter guides' statewide contest pages, read Nov. 4, 2026: the
candidates' own survey answers first published by Ballotpedia, the newsroom's
interviews (quoted) and its platform summaries (cited, not quoted). Eleven states'
guides answer issues (Alabama, Arizona, Colorado, Georgia, Idaho, Indiana, Iowa,
Maryland, Nebraska, New Mexico, Rhode Island); the Arkansas, Florida, Kansas, Michigan,
Minnesota, North Dakota, Ohio, Oklahoma, South Carolina, South Dakota and Wisconsin
pages carry only bios, so their races have no positions yet. A race whose main
candidates all have positions there is marked researched, which turns on side-by-side
matching; otherwise the entry is `partial`. Below five compared questions no
percentage is shown, as everywhere.

## The national House map

`data/maps/cd-us.json`, for the House view of the home page's map, is built by
`scripts/build_house_map.py` from the state district maps (`data/maps/cd/ST.json`, Census
TIGER 2026): each state's districts are simplified again as one coverage (0.012 degrees,
three decimals, islands under 0.2% of their district dropped), so neighbours keep a
shared border, with clockwise rings. Ids are the race ids without the "-H-" (`CA-13` for
`CA-H-13`, `AK-00`, `DC-98`), with `st`, `n` and `lp` as in the state maps; 436 districts,
about 0.9 MB, loaded only when the House view first opens. The state lines are drawn over
them (`borders` in `drawMap`). Rebuild it after `build_maps.py`.

## Upcoming elections (2027-2029)

`data/upcoming.json`, for `#/upcoming`, is rebuilt once a day by
`scripts/update_upcoming.py` from English Wikipedia's national pages for each office and
year (the governor, lieutenant governor, attorney general, secretary of state, treasurer
and auditor pages for 2027-2029 where they exist, the 2028 Senate and presidential pages,
and each odd year's special Senate elections from the "U.S. Senate" line of "<year>
United States elections"). Each entry of `races`:

| Field | What it holds |
|---|---|
| `id` | `2027-KY-GOV`, `2028-AL-SEN`, `2028-TN-SEN-SP` (special), `2028-US-PRES`, `2028-US-HOUSE` |
| `year`, `date` | Election day: the page's own date, "October 9 (Louisiana)" for Louisiana's open primary (`dateNote` says so), else the first Tuesday after the first Monday in November |
| `office`, `officeName`, `state`, `special` | As for the 2026 races; `officeName` from the race page's title ("Auditor of Public Accounts") |
| `holder` | `name`, `party`, `wiki`; `name: null` with `appointment: true` for a seat to be filled by appointment, and with neither where the table says "TBD in 2026" (Vermont's two-year offices: the page then names the 2026 winner from the site's own results) |
| `firstElected`, `lastRace` | The table's "First elected" (or the Senate's "Electoral history") and "Last race" ("52.5% D") |
| `statusText`, `plans` | The table's status as written ("Term-limited", "Incumbent's intent unknown") and `running`, `leaving` or `unknown` |
| `candidates` | Declared candidates only: the "Candidates" column ("TBD" and any part headed "Potential:" or "Declined:" left out), the officeholder added when the status says "Incumbent running"; for president, the "Declared" tables of each party's primaries, with `announced`, `experience` and `home`, and `primaries` counting them per party |
| `page`, `source` | The race's own Wikipedia page (or the national page's section), and the table read, with its last edit (`asOf`) |

No forecasts: none of these races are rated, and the only polls test people who aren't
running. The 2028 House entry has the date only (Wikipedia has no 2028 House page yet).
The 2026 runoffs at the top of the page come from `races.json` (`result.status:
"runoff"`, `runoff` for the date). State legislatures and local offices aren't covered.

## Rules for donation links

A link appears only if `donateUrl` uses https and points either to the
`officialSite` domain or to `secure.actblue.com`, `secure.winred.com` or
`secure.anedot.com`, the processors campaigns use. Copy the link from the
campaign's own site; look-alike and scam-PAC pages are the main risk.

## Sites that refuse scripted reads

senate.gov, GovTrack, the Louisiana Illuminator and fec.gov's bulk downloads refuse
automated requests. The States Newsroom sites (Alaska Beacon, Florida Phoenix, Idaho
Capital Sun and the rest) refuse Python's default user agent but answer requests that
name themselves; keep those requests slow and identified. Don't work around a refusal: read news pages in the browser,
or use a source that cites them (guides.vote and Ballotpedia link each Senate roll
call). Ballotpedia itself starts returning empty pages after about 50 quick loads,
so read its pages one at a time. fec.gov refuses to be framed; read candidate
pages one at a time in a tab of their own (navigating away wipes any script running
in the page).

Summaries from automated page readers can misquote: one returned a Hochul quote that
appears nowhere in the release it cited. Check every quote against the page text
(in the browser pane) before it goes into a research script.

## The France section

Everything for France lives apart from the U.S. data: pages under `#/fr`, code in
`js/fr/`, data in `data/fr/`, builders in `scripts/fr/`, and a visitor's answers and
address under their own browser key (`iv:fr:v1`). `scripts/refresh_all.py` runs the
builders after the U.S. steps; each keeps its previous file if it can't build a new
one, and a France failure never triggers the U.S. restore.

| What | Source | Builder, schedule |
|---|---|---|
| 2027 presidential dates and declared candidates | French Wikipedia, "Élection présidentielle française de 2027" (infobox and the "Candidats déclarés" tables), cross-checked against franceinfo's tracker of declared candidates and the hand check in `candidats_2027.py` | `update_presidentielle.py`, daily |
| First- and second-round polls | French Wikipedia, "Liste de sondages sur l'élection présidentielle française de 2027", each row linked to its notice at the Commission des sondages (or matched to one in the Commission's list of notices) | same |
| Candidates' and leaders' photos | Wikidata (P18) and Commons, with author and license | `frwiki.photos` (`scripts/lib/wikiphotos.py`), cached a day |
| Parties: leader, position, ideology, seats, site | Each party's French Wikipedia infobox, "current" part only | `partis.py`, daily |
| Who sits in Parliament: deputies and senators with their group, party, constituency and seat; the chambers' presidents; the government | The Assemblée nationale's open data (AMO10) and the Sénat's (`senateurs.json`, `ODSEN_GENERAL.csv`), Licence Ouverte; French Wikipedia's tables of each chamber's groups (presidents, declared positions); Wikidata (President P35, Prime Minister P6, chamber presidents P488) | `parlement.py`, daily |
| Election calendar | One French Wikipedia page per election, hand-checked | `calendrier.py`, every run |
| Regions and departments | IGN ADMIN EXPRESS COG CARTO via the Géoplateforme WFS (Licence Ouverte 2.0) | `build_maps_fr.py`, by hand |
| Largest cities | geo.api.gouv.fr (INSEE populations), five per region, two overseas | same |
| Address to commune | Géoplateforme geocoder (IGN), in the browser, after consent | `js/fr/geocode.js` |
| Candidates' positions on the 144 questions | Programs, campaign sites, party documents, speeches, interviews and press reports, read by hand | `positions_2027.py` (no network), every run |
| "Les grands enjeux": economy, inflation, immigration, crime, wealth gap, education, salaries | Eurostat (JSON-stat API), the OECD (SDMX API), the World Bank (API, with the UN's migrant estimates and UNODC's homicide rates), the U.S. BLS (public API), the Interior Ministry's crime statistics (SSMSI, on data.gouv.fr); INSEE's, the ONS's and PISA's published figures typed in `enjeux_sources.py` | `enjeux.py` → `data/fr/enjeux.json`, daily; see "Les grands enjeux" below |

**Who is running.** Only declared candidates are listed, averaged and compared; people
polls test without a candidacy (Hollande, Villepin, Bardella) keep their values in the
poll tables' line-ups and nowhere else. Wikipedia's "Candidats déclarés" table is the daily aggregator, cross-checked every day
against franceinfo's tracker of declared candidates; `scripts/fr/candidats_2027.py`
records the check made person by person on Nov. 2, 2026: each candidate with the
article that reports their own announcement, and the people polls test or trackers list
who aren't running, with the reason and its source. Someone checked as declared stays
declared unless franceinfo marks them withdrawn or neither tracker lists them any more;
someone checked as not running stays out unless both trackers list them; anyone else
needs both. Every disagreement goes to the data's `checks`, shown on the About page, to
be settled in `candidats_2027.py` with a source. On Nov. 2 the trackers differed on
eight people: franceinfo left out Zemmour and Bertrand (both announced) and listed
Lassalle (whose statement was conditional on a fundraiser); Wikipedia still listed
Cazeneuve (who said on Oct. 21 that he would help Glucksmann win) and left out Branco, Legendre, Billetdoux,
Collovati and Rohou. That gave 35 declared candidates of the 47 people listed or tested.
Positions of people who aren't running (Villepin, Cazeneuve, Bardella) stay on their own
pages for reference and count nowhere else.

**Polls.** A row counts only with its notice at the Commission des sondages. Wikipedia
links most rows to it; a row linked to the pollster's own page instead gets the one
vote-intention notice in the Commission's list from that pollster, filed within ten
days after the fieldwork ended and not already another poll's, and stays out without
one. A vote-intention notice newer than every listed poll goes to `checks` as a poll
Wikipedia hasn't added yet. A poll often tests several line-ups of candidates (one
table row each); the average takes each poll once, using the candidate's median across
that poll's line-ups made only of declared candidates (a line-up with someone who isn't
running counts only for a candidate the poll tested nowhere else), over the 30 days
before the latest poll, and shows the lowest-to-highest range beside it. "<1" counts as
0.5, and a value cell that names someone else ("6,5 / Hollande (PS)") goes to that
person. Second-round match-ups need two declared candidates and are averaged the same
way; one not polled in 60 days is shown as stale. There are no win probabilities. Polls
refresh every day (44 first-round polls and 7 match-ups on Nov. 2).

**Parliament** (`#/fr/parlement`, and `#/congress` for the U.S.). Each chamber is a
half-circle of seats (`js/components/hemicycle.js`) filled left to right by group: in the
Assembly by where the group's members sit (the median seat number, which runs from right
to left), in the Senate by each group's stated position in its Wikipedia infobox. A
group takes the color of the party most of its members belong to (the Assembly's data
gives each deputy's party; Senate groups take the first party their infobox lists, set by
group code in `parlement.py`). A group whose party has no color of its own is gray
(`--seat-other`, darker than the parties' gray, which failed the colorblind check beside
pink), and groups sharing a color get a different seat shape (circle, square, diamond).
A seat's tooltip gives the member's name, office if any, group, party (deputies only: the
Senate publishes groups, not parties), constituency and region; empty seats are vacancies. The page names the President of the Republic, the
Prime Minister and government, each chamber's president and the group presidents; the
Wikidata names are checked against the chambers' own data, and a mismatch goes to the
file's `checks`.

**Parties.** Infobox fields often list a party's past beside its present ("Actuel : …
Historique : …") or its internal currents; only the current part is kept, so the
Communist Party shows communism, not the Stalinism of its history. Links to party
congresses are dropped from ideologies. English mode translates the terms
(`js/fr/views/partis.js`).

**Calendar.** Departmental elections leave out Paris, Corsica, Martinique, French Guiana
and Mayotte (no departmental council) and note the Lyon Metropolis; regional elections
leave out Mayotte and note that Corsica, Martinique and French Guiana elect their
assemblies the same day. Dates not yet set by decree carry only a month and show no day
count; the legislative date is a deadline ("au plus tard").

**Questionnaire.** The 144 questions in `js/fr/questions.js` are the owner's French text,
numbered as given; the English is a labelled translation.

### Candidates' positions (France)

`scripts/fr/positions_2027.py` holds every position by hand and writes
`data/fr/positions.json`: for each candidate id, question id → `{stance, source, quote}`.
Stances run from +2 (très favorable / tout à fait d'accord) to -2, as the visitor's
answers do. As of Nov. 2, 2026 it covers 27 of the 35 declared candidates, 851
positions (902 with Villepin, Cazeneuve and Bardella, kept for reference), from 3
(Mikolajczak, until Équinoxe's program on Nov. 4) and 4 (Egger) to 80 (Tondelier). Eight
declared candidates have no program or usable statement yet (Platret, Durif, Lalanne,
Mathieu, Mlekuz, Billetdoux, Collovati, Rohou). Each source records the day it was read
and its quotes checked (`accessed`: Oct. 28, or Nov. 2 for the candidates in `LATER` and
sources wrapped in `later()`); a candidate page shows its latest, and the About page the
latest across declared candidates.

- **Sources.** The candidate's program, campaign site, own speeches, op-eds and
  interviews, and their party's program or booklets (Rassemblement national,
  Renaissance's thematic conventions, Les Républicains' "Nos propositions pour la
  France", Les Écologistes, Place publique, the PCF's congress texts and "cahiers",
  Debout la France, Nouvelle Énergie, Lutte ouvrière), labelled as party documents.
  programmes-2027.fr and votons-2027.fr, independent directories of the programs, were
  used only to find them; nothing is cited from them, and their links were followed to
  the candidate's own text (they sometimes point at a home page or an older program).
  A PDF is cited page by page (`#page=N`). Asselineau's positions come from his 2022
  program, which the UPR still presents as its program (none for 2027 yet); Bardella's
  from the RN's 2024 legislative program (his signed foreword as candidate for Prime
  Minister) and European program (he led the list). Markovic's party (Parti animaliste)
  has no 2027 program, so its 2022 national and 2024 European programs are cited as the
  party's; Egger's party (Solution Démocratique) publishes a program limited on purpose to
  institutions. Legendre's manifesto is a Google Doc, read through its public text view
  (`/mobilebasic`) and cached under the cited link. Becht and Polony have no program yet:
  their positions come from interviews published as transcripts (Sud Radio) and, for
  Polony, Pleinchamp's report of her remarks at the Sommet de l'élevage. Sites that refuse
  scripts (generationecologie.fr) were read in the browser pane; the text read there was
  saved to the check's cache so the quotes could be compared all the same.
- **Quotes.** Copied word for word, at most 25 words, and checked against the source's
  text (on the cited PDF page) before they go in. A press report that describes a
  proposal without quoting the candidate is cited with `quote: null`, and the page
  says it is a press summary.
- **Stances.** Taken from what the text says, never from party or reputation. Where a
  proposal answers a question only partly (repealing a law that sped up evictions, a
  bigger EU budget that may come from its own resources), the stance is ±1. A candidate
  who opposes keeping the retirement age at 64 because they want 65 (Philippe) or no
  legal age at all (Attal) gets -1 there, not -2. A carbon border adjustment isn't read
  as a carbon tax. A program that leaves a choice to a referendum or a constituent or
  citizens' assembly (Legendre's manifesto, Branco's "La Voie") gives no position on it;
  only what it proposes itself counts, and a view on a past reform (Legendre on
  retirement at 60 and the 35-hour week) is a partial answer. A question nothing answers
  stays out.
- **Matching** (`js/fr/match.js`) uses the U.S. rule: each question both sides answered
  scores 1 - |gap| / 4, and fewer than 5 shared questions give no percentage. "Mes
  élections" has the "Comparer avec mes opinions" button, which leads to the ranking
  (`#/fr/elections/comparer`); each candidate card and candidate page
  (`#/fr/candidat/<id>`) has its own button. Each opens the three-panel comparison of
  `js/fr/compare.js`, laid out like the U.S. one: agreements left, differences right,
  questions the visitor answered but the candidate has no known position on along the
  bottom. The candidate page also lists every position by topic with quotes and links.

To add positions: find the candidate's own text, add a row `(qid, stance, source,
quote)` to their list (sources through the helpers at the top of each block), and run
the script; it checks ids, stances, https links and quote length. The quote check
against the source text was done with scratch tools (fetch the page or PDF, extract
the text with pypdf, compare after normalizing spaces, apostrophes and quotation
marks); do the same for new quotes.

### Les grands enjeux (France)

`scripts/fr/enjeux.py` writes `data/fr/enjeux.json` (20 blocks, about 146 KB) once a
day from `refresh_all.py`; the page is `js/fr/views/enjeux.js` (`#/fr/enjeux?t=<tab>`,
in the France menu), seven tabs: economy, inflation, immigration, crime, the wealth gap,
education and salaries in France.

- **One source per comparison.** Every country in a chart comes from the same source
  wherever one exists (Eurostat for EU countries, the OECD or the World Bank where the
  UK and the US are needed), so the definitions match. Where only national sources exist
  (median pay in the UK, from the ONS's earnings survey, and in the US, from BLS's Current
  Population Survey) the page says so. Each block names its dataset and the day its
  source last updated it.
- **Stale blocks.** A block whose source can't be read keeps its last good values and its
  id goes into `stale`; the page then says those figures weren't reread today.
- **Hand figures.** Publications with no API (INSEE's private-sector salaries for 2025,
  the ONS's earnings survey, PISA 2025) are typed in `enjeux_sources.py`, each with its
  source, publication date, `accessed` and the sentence its main figure comes from
  (verbatim, under 25 words). A new edition replaces the entry instead of editing numbers
  in place: INSEE's salaries and the ONS survey every October, PISA every three years.
  oecd.org refuses scripts, so PISA's tables were read in the browser pane.
- **Salaries: the median, never the mean or GDP per head** (the owner asked for medians
  throughout on Nov. 3, as more realistic). GDP per head isn't an income: it divides
  everything produced, company profits, investment and what taxes pay for included, by
  every inhabitant, children and retirees included, and an average is pulled up by the
  highest pay. The median salary is what the employee in the middle earns. The page
  explains this, shows the three measures side by side (median full-time pay, median
  disposable income, GDP per head) and how far the US is ahead of France on each. France's
  own figures are INSEE's: the median, the deciles, and the medians for women and men
  (figure 4). INSEE gives pay by occupational category (cadres, employés, ouvriers) only
  as means, so that chart was dropped; the mean appears only where the page explains
  why it misleads (the "why the median" card, the histogram's dashed line, one choice in
  the index chart, and the net-to-gross note).
- **Money across countries** is converted with the OECD's yearly figures two ways: at the
  year's average exchange rate, and at purchasing power parities for household
  consumption ("euros at French prices": what the amount buys in France), the default.
  GDP per head uses GDP parities. A year the OECD hasn't published takes the nearest
  year's rates.
- **By sector, not by job.** No source publishes median pay by occupation for these
  countries: Eurostat's Structure of Earnings Survey gives occupations only as means
  (`earn_ses22_21`, `_25`, `_28`), with medians only by sex, age, education, contract and
  economic activity, and the OECD's teachers' and health workers' pay are means too. So
  the "By sector" card shows Eurostat's median gross hourly earnings by NACE section
  (`earn_ses_pub2n`: employees except apprentices, part-timers included, firms with 10 or
  more employees; the latest survey, 2022) for France, Germany, Belgium, Italy, Spain and
  the Netherlands, all 17 sections from B to S except O plus all of them together, with
  hourly figures to the cent. A sector counts everyone it employs (education isn't only
  teachers, and the card says so). The statutory minimum wage stays, as a yearly amount
  (the OECD; Italy has none, the US figure is the federal minimum): the OECD has no
  hourly minimum for Belgium or the Netherlands. The teacher and health figures (the
  OECD's `DF_TCH` and `DF_REMUN`) and the eight ISCO groups were removed with this. An
  entry opens directly with `#/fr/enjeux?t=salaires&metier=<id>` (`sector-P`, linked from
  the Education tab; `sector-all`, `minimum`).
- **Country colors.** Each country takes its flag's color (owner's request, Nov. 3):
  France navy, Spain yellow, the EU white, Germany gray, Belgium black, Italy green, the
  Netherlands orange, the UK red, the US light blue (`--cty-*` in `css/styles.css`, one
  set per theme), and the OECD average stays hatched gray. See CLAUDE.md, Conventions.
- **Crime** counts offences recorded by the police and the gendarmerie (SSMSI), not every
  offence committed, and the page says that reporting and police checks move them;
  homicide rates (UNODC, via the World Bank) are the only crime figure compared across
  countries.
- **Candidates.** Each tab ends with the questionnaire's questions on its issue and which
  declared candidates are for, against or have no known position, from `positions.json`;
  nothing is inferred from the figures.
- **Colors.** France in ink (`--text-1`), every other country in gray, aggregates (EU,
  OECD) hatched, so no country borrows a party's color. The pair passes the palette
  validator's colorblind and contrast checks in both themes (CVD ΔE 39.0 dark and 44.4
  light; normal vision 39.1 and 44.3); its lightness-band and chroma checks fail, as they
  do for any neutral pair, and every value is printed beside its bar.
