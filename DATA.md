# How the race data is built

`data/races.json` holds every 2026 U.S. Senate, U.S. House and governor race. It is
**generated**: `scripts/update_races.py` rebuilds it every 8 hours (through
`scripts/refresh_all.py`), so don't edit it by hand. To add or correct
researched details, edit the research scripts described below.

Each race in `races.json` replaces the demo race with the same id and loses its
DEMO tag. State legislative races are not in it and stay demo.

## Where each piece comes from

| Data | Source | Notes |
|---|---|---|
| Candidates on the ballot, incumbents, partisan lean (Cook PVI) | Wikipedia's national 2026 Senate, governor and House pages | Used as an aggregator (CC BY-SA). Incumbents are identified by the Wikipedia article they link to. |
| Forecasters' ratings | The same pages' prediction tables (Senate, governors) and the House ratings page | Up to 11 outlets: Cook, Inside Elections, Sabato, Decision Desk HQ, The Economist, FiftyPlusOne, Fox News, NBC News, RealClearPolitics, Silver Bulletin, Split Ticket. |
| Polls | Each race's Wikipedia page (House: each state's page, by district) | Only tables whose every candidate is on the ballot, so hypothetical match-ups are skipped. One row per poll (likely-voter version preferred). Each poll links to the citation Wikipedia gives for it. |
| Published polling averages | The aggregator table on each race page | A check on our average, not an input. |
| Fundraising | FEC API when a key is set (see README); FEC financial summaries read on fec.gov for every Senate candidate and the competitive House races (`scripts/research/fec_2026.py`); otherwise the FEC totals cited in Wikipedia's fundraising tables | See "Money by source". Governors: totals from state filings via Wikipedia, without a breakdown. |
| National environment | Generic congressional ballot average on the Senate page | Feeds the partisan baseline. |
| Seats held today | Wikipedia's party summaries for the 119th Congress; governors from the 36 races plus the 14 not on the ballot | Expected gains are measured from these. |
| House members' positions | The House Clerk's roll-call XML for ten votes (2021 to 2025) | See "Positions from votes". |
| Betting market | Polymarket's Senate and House control markets | A cross-check shown beside the model, never an input. |
| Projected votes | 2024 presidential votes by state × 0.75 (House: divided by districts) | Midterm turnout ran 0.71 of the presidential vote in 2022 and 0.85 in 2018. |

Wikipedia pages are cached by revision in `data/cache/wiki/`, so a refresh only
downloads pages edited since the last one.

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
- control odds are within 20 points of the betting market;
- the national environment was found, and fundraising data is current;
- close statewide races have a poll from the last 30 days.

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
| Inflation Reduction Act (2022) | hea-02, hea-07 | +1 | -1 |
| Infrastructure Investment and Jobs Act (2021) | eco-06 | +1 | -1 |
| CHIPS and Science Act (2022) | agr-02 | +1 | -1 |
| Ukraine aid, H.R. 8035 (2024) | def-13 | +2 | -2 |
| Israel aid, H.R. 8034 (2024) | def-12 | +2 | -2 |
| H.R. 1 (2025), which cut Medicaid | hea-03 | -1 | not used |
| Secure the Border Act (2023) | imm-01 | +1 | not used |
| Lower Energy Costs Act (2023) | ene-03 | +1 | not used |

"Not used" marks omnibus bills where a no vote could mean many things. Members
first elected in 2024 or later have few of these votes, so most of their
positions stay blank. The rules live in `scripts/lib/house_votes.py`.

## Researched races (overlays)

Hand-researched details live in `data/research/*.json`, written by the scripts in
`scripts/research/`: one per state for the competitive races (`alaska_2026.py`,
`texas_2026.py`, ...), plus `safe_races_2026.py` (safe Senate races and the senators
running for governor), `governors_2026.py` (safe governor races),
`positions_2026.py` (more positions for candidates who had few, from their campaign
sites' issue pages, signed bills and news coverage) and `fec_2026.py` (money by
source, see above). Overlays are merged in file-name order, case-insensitively.
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
| `candidatesOnly: true` | The researched list is the qualified list: automatic candidates not on it are dropped, with a note in the refresh log (used where Wikipedia's list was wrong). |
| `aliases[]` (candidate) | Old candidate ids, so visitors' saved likes follow the candidate. |
| `polls[]` | Merged with the automatic polls; the researched version of the same poll (pollster and end date) wins. Poll fields: `sponsor`, `url`, `note`, `approx` (shows "~" before the sample size). |
| `excludePolls[]` | Pollster names to leave out of the average (e.g. a poll whose only source is a social media post). |
| `notes[]` | Context lines under the headline (`text`, optional `source` and `url`). |
| `earlyVote` | `ballots`, `pctOfTurnout`, `asOf`, `label`, `byParty`, `vs2022`, `note`, `source`. |
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
total differ by more than $10 or 0.1%. `fec_2026.py` holds the summaries read on
fec.gov on Oct. 25, 2026 (coverage mostly through Oct. 14): every Senate candidate with
money, Louisiana's 6th District and the 77 House races at least one forecaster rates
Toss-up, Tilt or Lean. A newer API report replaces them automatically. Missing
figures are not evidence that a candidate has filed nothing: the Money tab says the
figures haven't loaded and links to an FEC search, and only a researched note may say
"no report on file".

## Rules for donation links

A link appears only if `donateUrl` uses https and points either to the
`officialSite` domain or to `secure.actblue.com`, `secure.winred.com` or
`secure.anedot.com`, the processors campaigns use. Copy the link from the
campaign's own site; look-alike and scam-PAC pages are the main risk.

## Sites that refuse scripted reads

senate.gov, GovTrack, the Louisiana Illuminator, the States Newsroom sites (Alaska
Beacon, Florida Phoenix, Idaho Capital Sun and the rest) and fec.gov's bulk downloads
refuse automated requests. Don't work around that: read news pages in the browser,
or use a source that cites them (guides.vote and Ballotpedia link each Senate roll
call). Ballotpedia itself starts returning empty pages after about 50 quick loads,
so read its pages one at a time. fec.gov refuses to be framed; read candidate
pages one at a time in a tab of their own (navigating away wipes any script running
in the page).

Summaries from automated page readers can misquote: one returned a Hochul quote that
appears nowhere in the release it cited. Check every quote against the page text
(in the browser pane) before it goes into a research script.
