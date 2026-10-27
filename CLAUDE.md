# Informed Voter

A nonpartisan voter-information website for the 2026 U.S. elections: interactive
race maps, forecasts, the visitor's own ballot from their address, and a
questionnaire that matches voters to candidates with sources. The United States
comes first; the UK, Canada and France are planned and shown greyed out.

## Decisions already made (do not relitigate without asking)

**Static site, no backend, no build step.** Plain HTML/CSS/ES modules plus
vendored D3 v7.9.0. Runs with `python scripts/serve.py`; deploys to any static host.

**No server-side storage of anyone's views or address.** Everything a visitor
saves lives in localStorage (`js/store.js`). Political opinions are special-category
data under GDPR, which matters for the UK/France expansion, and a database of
them is a liability. Matching runs in the browser.

**Full street address, never ZIP code, for districts.** ZIPs span multiple
congressional districts for ~22 million Americans. The address goes only to the
Census Bureau geocoder (JSONP, because it sends no CORS headers), and only after
an explicit consent checkbox.

**Never fabricate facts about real people.** Candidates, polls, fundraising and
positions are a clearly tagged fictional demo set (`js/data/demo.js`) until real
data is added in `data/races.json` (see DATA.md). Demo names are invented;
pollster names are invented. Everything demo shows a DEMO chip.

**Positions are never inferred.** A candidate stance needs a source. Unknown means
"unclear", shown to the user and excluded from the score. Below 5 compared
questions no percentage is shown.

**Research may cover only some of a race's candidates.** `partial` overlays
(`candidates_2026.py` for third-party and independent Senate and governor candidates,
`house_challengers_2026.py` for House challengers) add bios and positions without
marking the race researched, so side-by-side matching stays off until every main
candidate is covered.

**Questionnaire wording is the site owner's**, kept verbatim in `js/data/questions.js`
(136 questions, 12 topics). `demoLean` there only drives demo generation.

**Funding categories mirror real filings**: small donors, large donors, PACs,
party, self-funding, public financing, transfers (joint fundraising committees and the
candidate's other campaigns) and other (loans, refunds). Each part is the filing's own
line, rounded on its own and never padded to the total. Corporations can't give
directly to federal candidates, so "corporate money" is explained as PAC and super PAC
money. Missing figures mean "not loaded yet", never "no report on file".

**Donation links**: official site domain or ActBlue/WinRed/Anedot only (`verifiedDonateUrl`).

**Open (jungle) primaries get no win probabilities.** Louisiana's 2026 House races
put every candidate on one ballot with a December runoff. With many candidates
and one poll, the head-to-head model would invent precision (it would call the
poll leader the favorite in a Trump +30 seat), so `format: "open-primary"` races
show the field, polls as published and forecasters' ratings instead.

**State legislative races get no win probabilities either.** Almost none are polled
and few are rated, so they carry `format: "field"`: the candidates, who holds the
seat, the district's 2024 presidential margin and any district ratings. The map
colors them by that margin (by the holder's party where a chamber page has no
margins). They live in `data/legislature/ST.json`, written by
`scripts/lib/legislature.py` from each chamber's 2026 Wikipedia page during the
refresh and loaded with a state's chamber map, so they never weigh down races.json.

**Early voting comes from the UF Election Lab's tracker** (`scripts/lib/early_vote.py`),
refreshed with the races: every state's total, mail and in-person split and party
registration split, plus House districts only where the Lab's district file covers
every district and 98% of the state's ballots. The Lab's per-state notes become
short caveats in our own words (Missouri counts St. Louis County only). The data
is CC BY-NC-ND, so every Early vote tab credits it, and the site stays non-commercial.

**Unverified polls stay out of the average.** A poll is included only with a
verifiable source naming the pollster and dates. Campaign internals are labelled
with their sponsor; claims without details go in race `notes`, not `polls`.

**Real race data is rebuilt automatically every 8 hours, never hand-edited.**
`scripts/refresh_all.py` (Windows Task Scheduler, \InformedVoter\, 6:00/14:00/22:00)
runs `scripts/update_races.py`, which writes `data/races.json`, `control.json`,
`status.json` and `data/legislature/`. Wikipedia is the aggregator for candidates, ratings, PVI and polls;
the FEC API for money (falls back to Wikipedia's cited FEC totals without a key);
the House Clerk's roll-call XML for House members' positions. Hand research goes
in `scripts/research/<state>.py`, which write overlays to `data/research/`.

**Baselines come from forecasters' ratings, placed by partisan lean.** Rating
bands (Safe 15+, Likely 7-15, Lean 3-7, Tilt 0.5-3, Toss-up ±2) with 2×PVI plus
the generic ballot positioning the race inside each band. This replaced the
2024-presidential baseline, which left every rated race's margin wrong.

**The Python and JavaScript models must stay identical.** `scripts/lib/model.py`
mirrors `js/model/forecast.js`; every race carries `modelCheck` and the About page
reports any mismatch. Change both files together.

**Betting markets are a cross-check, never an input.** Polymarket's control odds
appear beside the model and in the checks.

**Ranked-choice races are forecast on their final round.** Alaska (every race) and
Maine (federal races) set `rcv: true`. Wikipedia's "Ranked-choice polls" tables
give each poll's final round (`finalPolls`), which sets how the two finalists
split; without them, each party's other candidates' shares go to its strongest
candidate. Plurality math called Alaska's governor race a certainty when
forecasters rated it Lean D.

**The margin is between the actual top two.** Candidates are ordered by poll
share, then incumbency, then money; an independent who leads the opposition
(Nebraska, Montana) is the main challenger, and "D +x" is shown only when a
Democrat and a Republican are the top two.

## Real data so far

Every Senate, House and governor race is live (candidates, ratings, polls, money,
forecasts). As of Oct. 26, 2026, every Senate and governor race has sourced
positions for its main candidates, and so do both main candidates in the 78 House
races anyone rates Toss-up, Tilt or Lean (155 researched races in all, with
Louisiana's House districts). Statewide sources: guides.vote for about 20 races,
senators' key votes via Ballotpedia, newsroom questionnaires (Maine Public, KAXE,
Flatwater, Source NM), debate coverage and campaign sites. `positions_2026.py` added
stated positions for candidates who had few (campaign issue pages, signed bills,
questionnaires, debate reports); only Wess (AL-SEN, one) and Casner (WY-GOV, two) are
still thin. State records where they are readable: N.C. House roll calls for Balkcom,
Minnesota House votes for Demuth, and bills Abbott and Ayotte signed. `house_2026.py`
covers the competitive House races: guides.vote voters guides for 34 of them, campaign
issue pages for the rest, and news reports where a site lists no issues (Balkcom
NC-11, Alvarado KY-06, McGuire VA-05, Alaska, CA-06). Still below the five needed for
a match percentage there: Dan Green (FL-09, two), Bill Hill, Richard Pan and Sydney
Gruters (four each). Third-party and independent Senate and governor candidates are
covered by `candidates_2026.py` (75 candidates, 610 positions, Oct. 26) from their
campaign sites and newsroom voter guides; about 35 have no site or statement anywhere
(Tennessee's dozen independents, Michigan's minor parties). House challengers in
safer races are in `house_challengers_2026.py` (422 candidates in 296 races, 1,428
positions, Oct. 26-27): questionnaire answers from States Newsroom voter guides where
a state's outlet ran one (quoted), their bios and summaries elsewhere (not quoted),
and campaign issue pages; about 200 House candidates, mostly third-party, have no
site or statement to use. Every
current House member on the ballot also has positions from 39 recorded House votes,
2021 to 2026, including 11 war powers resolutions (`scripts/lib/house_votes.py`), so
members first elected in 2024 have about 20 each. Money by source comes from FEC
summaries for every Senate candidate and every House candidate with a 2026 report
(997 candidates through Oct. 14: `fec_2026.py` for the Senate and competitive House
races, `fec_house_2026.py` for the rest); the other 248 House candidates, mostly
third-party, have a sourced note from an FEC search (`fec_notes_2026.py`: 176 with no
2026 report yet, 71 with no FEC record for their district). Governors: totals from
state filings via Wikipedia for 14 races; Florida's every candidate grouped by source
from the Division of Elections database (`florida_money_2026.py`: state matching
funds as public financing, each major candidate's political committee in a note,
fetched at most once a day); for the other 21, the latest news report of the filings
as a dated note with its link (`governor_money_2026.py`), never stretched into a
total. Campaign site links come from each race page's "External links" (a
researched `officialSite` wins, and `officialSite: None` drops a dead or parked
domain); `campaign_sites_2026.py` adds 118 the pages lack, mostly California's, from
candidates' Wikipedia articles and BallotReady profiles, each checked live (1,242 of
1,418 candidates now have one). Early voting covers 49 states and 155 House districts. State
legislative races are real in all 88 chambers voting this year: 5,615 districts,
3,362 with candidates listed; researched legislative candidates (Oklahoma SD 32 and
HD 85 so far) live in `data/research/legislature/`, written by
`legislature_2026.py`. Pages that still show only declared primary candidates
(Massachusetts, the New York Assembly, Kansas, Iowa House, Florida House and others)
give seats, holders and margins but no candidate lists yet.

## Conventions

- Render with the `html\`\`` tag from `js/util.js`: it escapes every interpolation.
  Outside text (news headlines) must never reach innerHTML unescaped.
- Boolean attributes: write `aria-pressed="${String(on)}"`.
- Party colors: D blue, R red, strongest other candidate green, the rest gray.
  Validated with the dataviz palette checker in both themes; don't eyeball new ones.
- Map files come from Census TIGER 2026, clipped to the shoreline and
  simplified as a coverage (`scripts/build_maps.py`). Rings are clockwise for d3.
- Questionnaire definitions live in `js/data/glossary.js`: neutral wording and no
  claims about current law that can go stale. `js/components/terms.js` underlines at
  most three per question (hover, focus or tap), and the question text stays verbatim.

## Pitfalls hit already

- **Two CSS rules with one class name.** `.stack` was both a spacing helper and the
  stacked-bar chart, which silently squashed every spaced section to 12px.
  The bar is now `.stackbar`.
- **`html\`\`` used to render `true` as an empty string**, so `aria-pressed` came out
  `""` and pressed styles never applied. Fixed in `util.js`.
- **Shared SVG gradient ids break when the first copy is hidden.** The logo now
  generates a unique id per copy.
- **Browser caching of JS modules** with Python's plain `http.server`: use
  `scripts/serve.py`, which sends `Cache-Control: no-store` and correct MIME types.
- **Python on this machine** is `C:/Users/kober/AppData/Local/Python/pythoncore-3.14-64/python.exe`;
  `python` in Git Bash resolves to the Microsoft Store stub, which fails with `-c` and `-m`.
- **The browser pane pauses animations when hidden**, so screenshots can catch
  overlays mid-fade. Finish animations via `document.getAnimations()` before judging.
- **The Bash tool collapses `\\` to `\`.** A heredoc patch meant to write the regex
  `\b` wrote backspace characters into world.js instead. Put code that contains
  backslashes in files via Write/Edit, then run them; never in an inline heredoc.
- **Date-only strings parse as UTC midnight**, which displays as the previous day
  in U.S. time zones. `fmtDate`/`fmtShortDate` in util.js read `YYYY-MM-DD` as a
  local date; keep using them.
- **FEC API `DEMO_KEY` allows about 10 calls an hour** (down from 40), and failed retries count. Get a free
  key at api.data.gov before bulk refreshes. fec.gov's bulk files reject scripted
  downloads; don't try to work around that. Its HTML candidate pages and search page
  are readable by script (three at a time is plenty).
- **FEC name searches hit namesakes.** "Mike Kelly" first matched a different Kelly
  (H4PA03117, not the incumbent's H0PA03271). Accept a result only for the same state
  and district, then check the page's own name and "Seat:" line. At-large seats print
  "House District" with no number, and negative lines print as "-$7,520.20".
- **The House Clerk answers a missing roll call with an ordinary 200 page**, not a
  404; treat anything that isn't XML as missing.
- **Chrome freezes background tabs**, so a long `javascript_tool` loop in an unfocused
  tab stalls. Front the tab and give every fetch a timeout (`AbortSignal.timeout`).
- **Every state's chamber page is laid out differently.** Candidates sit in a
  general-election box (known only by its `<caption>`), a "Candidates" column, a
  district infobox, Pennsylvania's combined table, "Nominee" or "Advanced to
  general" lists, or as bold winners in primary boxes; Colorado and Oklahoma give
  a party only as the color of a "▌" marker. `wikitables.py` keeps captions, bold
  cells and marker colors for this. Lists of declared primary candidates (still up
  on Massachusetts' and New York's Assembly pages) are never nominees.
- **Election boxes repeat fusion candidates** on each party line plus a "Total" row
  (Connecticut, New York): keep one entry per candidate, skip "Total" and write-ins.
- **The UF Election Lab's district files can be partial** (mail ballots only in
  Idaho and Connecticut), and a statewide row can be too (Missouri: St. Louis
  County only). Check coverage before trusting a file, and say so where it's partial.
- **Several news sites block scripted fetches** (Louisiana Illuminator, Verite).
  Read them in the browser pane instead. The States Newsroom sites refuse Python's
  default user agent but answer one that names itself
  ("InformedVoterResearch/1.0"); their voter guides' contest pages carry candidates'
  own questionnaire answers in one layout across states. senate.gov and GovTrack
  refuse scripts too, and senate.gov shows a bot check even in the browser pane;
  guides.vote links Senate roll calls and can be cited instead.
- **Ballotpedia blocks after about 50 quick page loads** (empty 202 responses).
  Its senator key-vote tables feed `senate_vote_positions` in
  `scripts/research/common.py`; read pages one at a time, never in a loop.
- **Wikipedia rate-limits bursts (HTTP 429).** `scripts/lib/wikitables.py` spaces
  requests, honours Retry-After, sends gzip and caches pages by revision id.
- **Wikipedia's candidate lists can be wrong.** It dropped Chauna Banks and added a
  non-candidate in LA-6; WWNO's qualifying list was right. It still listed Jon Kiper
  (NH-GOV, missed the signature cutoff) and Sondra Wilson (IA-GOV, kept off) and
  missed Stephen Villee (NH-GOV, qualified Oct. 20). Research overlays set
  `candidatesOnly: true` to make the researched list authoritative. Governor
  candidates come from the national "2026 United States gubernatorial elections"
  table, whose Tennessee list cites the Secretary of State's January list;
  Tennessee Lookout's guide differs by four independents, and the official list is
  only a PDF/Excel file that refuses scripted reads, so it is unresolved.
- **Party labels vary**: Minnesota's "DFL" and North Dakota's "Dem-NPL" are
  Democrats (`party_code` in `scripts/lib/elections.py`); missing that once made the
  Senate seat total 101. Vermont's "Green Mountain" (Peace and Justice) party is not
  the Green Party.
- **Opening a PDF link in the browser pane starts a download** and shows the user a
  save dialog (Iowa's candidate list did). Don't navigate the pane to PDFs; WebFetch
  gets 403 from those state hosts too.
- **Campaign domains die.** Marisa Simonetti's site is a parked GoDaddy page and Rick
  Beard's answers 404; an overlay sets `officialSite: None` so the link disappears.
- **Florida's finance database caps a query at 30,000 rows** (a larger `rowlimit`
  fails with "Overflow Error Number = 6"), so contributions are fetched month by
  month and split further when a month hits the cap; its expenditure search rejects
  date ranges. Matching funds appear as "STATE OF FLORIDA" or "STATE OF FLORIDA
  DEPARTMENT OF FINANCIAL SERVICES", candidates' own loans either name order
  ("RUSSO FRANK", "FRANK RUSSO"), sometimes without a ZIP code, and political
  committees hide behind ordinary names ("CONSERVATISM COUNTS"): their occupation
  field ("POLITICAL ORGANIZATION") gives them away.
- **Namesakes on one ballot** (Alaska's Dan S. and Dan J. Sullivan): incumbents are
  matched by the Wikipedia article both cells link to, not by name.
- **Automated page summaries can misquote.** A fetch tool returned a Hochul quote that
  appears nowhere in the release it cited. Check every quote against the page text in
  the browser pane before it goes into a research script.
- **fec.gov refuses to be framed, and navigating a tab wipes its scripts.** Run long
  page-reading loops in a tab of their own; `preview_start` with a url reuses the
  current tab. A browser restart also cleared the page's localStorage.
- **Missing money isn't evidence of no filings.** The DEMO_KEY ran out and left 443
  federal candidates without figures; the Money tab once said they had no FEC report.
  Wikipedia also lists some candidates who have filed nothing at a bare $0, so
  `hasFigures` (world.js) counts $0 only with the filing's coverage dates.
- **Finance-only overlays must not mark races researched** (`financeOnly: true`):
  the research flag turns on candidate matching. Neither may `partial` overlays,
  which research only some candidates.
- **A flex `<td>` leaves the table layout.** The money table's dividers sat at
  different heights whenever a label wrapped; the flex now lives on an inner
  `.fund-label` span.
- **A "no" vote isn't always the opposite of a "yes".** Omnibus no votes (H.R. 2 of
  2023, the 2023 energy bill, H.R. 1 of 2025) are not mapped to positions, and no
  votes on the marriage and abortion-rights bills count at half strength.
- **Voters guides can paste one candidate's record under another.** guides.vote's
  CA-22 voting-rules entry for Villegas repeats Valadao's House votes, though Villegas
  never served in Congress; it is left out of `house_2026.py`. Read each entry before
  mapping it.
- **Campaign sites hide issue text from scripted reads.** Some render with JavaScript
  (Mullock, Beltran), refuse scripts (Benitez-Thompson, Flippo) or keep each issue in
  a Wix lightbox with its own URL (Baumgartner's /tax, /border). Read them in the
  browser and check quotes against the live page's `textContent`, since collapsed
  sections drop out of `innerText`.

## Open questions

- Where challengers' positions come from at scale: research staff, candidate
  self-reporting (the Wahl-O-Mat model), or public questionnaires like WWNO's and
  the States Newsroom guides. Competitive races are hand-researched; safer House
  races' challengers are being added from campaign sites and those guides, but about
  200 have no site at all. Incumbents are covered by votes; senators need a source
  senate.gov allows.
- Senators' recorded votes: senate.gov can't be read, so senators have only
  Ballotpedia's key votes and what guides.vote cites, while House members have 39
  roll calls. State legislators' votes are hand-picked where the legislature
  publishes them as pages (N.C., Minnesota); Kentucky and Florida publish PDFs.
- The model has no pollster house effects; Idaho's Senate race shows how far a
  plain average can sit from adjusted ones (flagged in the checks).
- State legislative races: whether to forecast the rated ones (State Navigate rates
  districts in a few chambers), and where candidates' positions and money could come
  from (state filing systems differ in every state).
- Questionnaire duplicates (public schools, passenger rail and flood protection
  each appear in two or three topics) count those issues double in a match.
