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

**Unverified polls stay out of the average.** A poll is included only with a
verifiable source naming the pollster and dates. Campaign internals are labelled
with their sponsor; claims without details go in race `notes`, not `polls`.

**Real race data is rebuilt automatically every 8 hours, never hand-edited.**
`scripts/refresh_all.py` (Windows Task Scheduler, \InformedVoter\, 6:00/14:00/22:00)
runs `scripts/update_races.py`, which writes `data/races.json`, `control.json` and
`status.json`. Wikipedia is the aggregator for candidates, ratings, PVI and polls;
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
forecasts). As of Oct. 25, 2026, every Senate and governor race has sourced
positions for its main candidates (76 researched races with Louisiana's House
districts). Sources: guides.vote for about 20 statewide races, senators' key votes via
Ballotpedia, newsroom questionnaires (Maine Public, KAXE, Flatwater, Source NM),
debate coverage and campaign sites. `positions_2026.py` added stated positions for
25 candidates who had few (campaign issue pages, signed bills, questionnaires, debate
reports); only Casner (WY-GOV) still has none (no WyoFile answers, no campaign site
found), and Wess (AL-SEN) has one. Every current House member on the ballot also has
positions from ten recorded votes. Money by source comes from FEC summaries for every
Senate candidate, LA-6 and the 77 House races rated Toss-up/Tilt/Lean by anyone (262
candidates, `fec_2026.py`, through Oct. 14); the rest of the House needs an FEC key,
and governors have totals only. State legislative races are still demo.

## Conventions

- Render with the `html\`\`` tag from `js/util.js`: it escapes every interpolation.
  Outside text (news headlines) must never reach innerHTML unescaped.
- Boolean attributes: write `aria-pressed="${String(on)}"`.
- Party colors: D blue, R red, strongest other candidate green, the rest gray.
  Validated with the dataviz palette checker in both themes; don't eyeball new ones.
- Map files come from Census TIGER 2026, clipped to the shoreline and
  simplified as a coverage (`scripts/build_maps.py`). Rings are clockwise for d3.

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
  downloads; don't try to work around that.
- **Several news sites block scripted fetches** (Louisiana Illuminator, Verite,
  the States Newsroom sites such as Alaska Beacon and Florida Phoenix). Read them in
  the browser pane instead. senate.gov and GovTrack refuse them too; guides.vote
  links Senate roll calls and can be cited instead.
- **Ballotpedia blocks after about 50 quick page loads** (empty 202 responses).
  Its senator key-vote tables feed `senate_vote_positions` in
  `scripts/research/common.py`; read pages one at a time, never in a loop.
- **Wikipedia rate-limits bursts (HTTP 429).** `scripts/lib/wikitables.py` spaces
  requests, honours Retry-After, sends gzip and caches pages by revision id.
- **Wikipedia's candidate lists can be wrong.** It dropped Chauna Banks and added a
  non-candidate in LA-6; WWNO's qualifying list was right. Research overlays set
  `candidatesOnly: true` to make the researched list authoritative.
- **Party labels vary**: Minnesota's "DFL" and North Dakota's "Dem-NPL" are
  Democrats (`party_code` in `scripts/lib/elections.py`); missing that once made the
  Senate seat total 101.
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
- **Finance-only overlays must not mark races researched** (`financeOnly: true`):
  the research flag turns on candidate matching.
- **A "no" vote isn't always the opposite of a "yes".** Omnibus no votes (H.R. 2 of
  2023, the 2023 energy bill, H.R. 1 of 2025) are not mapped to positions, and no
  votes on the marriage and abortion-rights bills count at half strength.

## Open questions

- Where challengers' positions come from at scale: research staff, candidate
  self-reporting (the Wahl-O-Mat model), or public questionnaires like WWNO's.
  Incumbents are covered by votes; senators need a source senate.gov allows.
- Whether to add 2025-26 House votes so members first elected in 2024 have
  positions (only H.R. 1 of 2025 is in the set now).
- The model has no pollster house effects; Idaho's Senate race shows how far a
  plain average can sit from adjusted ones (flagged in the checks).
- Questionnaire duplicates (public schools, passenger rail and flood protection
  each appear in two or three topics) count those issues double in a match.
