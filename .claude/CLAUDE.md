# Informed Voter

A nonpartisan voter-information website for the 2026 U.S. elections and the 2027
French presidential election: interactive race maps, forecasts or polls, the
visitor's own ballot from their address, and a questionnaire that matches voters to
candidates with sources. The United States section is finished; the France section
(`#/fr`, started Oct. 28, 2026) is the work in progress; the UK and Canada are
planned and shown greyed out.

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

**The France section is kept apart from the U.S. section**, which the owner considers
finished: routes under `#/fr` (`js/fr/routes.js`), code in `js/fr/`, data in
`data/fr/`, builders in `scripts/fr/`, and visitors' French answers, address, stars and
reminders under their own localStorage key (`iv:fr:v1`, `js/fr/store.js`). Shared code
was only extended, never changed in behavior: the router draws each section's header
(`js/fr/shell.js` reuses the U.S. element ids), loads the 7 MB U.S. race data only for
U.S. pages, and the U.S. pages stay in English. The 144 French questions in
`js/fr/questions.js` are the owner's text, numbered as given; English is a labelled
translation.

**Languages: French or English, from the browser first.** `js/i18n.js` picks the
first French or English entry in the browser's language list, then the visitor's
choice (FR | EN switch, saved as `lang`). France pages carry both languages side by
side with `L('…', '…')`; shared pages (intro, country choice, help) use `t(key)`.
French text gets narrow no-break spaces before `? ! : ;` automatically (`frType`).

**France: declared candidates only, checked by hand.** Only people who have announced
their own candidacy are listed, averaged and compared (owner's request, Nov. 2). French
Wikipedia's "Candidats déclarés" table is the daily aggregator, cross-checked every day
against franceinfo's tracker; `scripts/fr/candidats_2027.py` holds the person-by-person
check (each candidate with the article reporting their own announcement, each person
polls test who isn't running with the reason and its source). A checked person keeps
that status unless the trackers clearly change it, anyone else needs both trackers (the
rules are in that file's docstring and DATA.md), and every disagreement goes to `checks`
on the About page, to be settled in that file with a source. People polls test without
a candidacy (Hollande, Villepin, Bardella) keep their values in the poll tables'
line-ups and their positions on their own pages, and count nowhere else.

**French polls: averages, never odds, refreshed daily.** Every poll counts once (a
candidate's median across the line-ups of declared candidates a poll tested), over the
30 days before the latest poll, and only with its Commission des sondages notice as the
source (taken from the Commission's list when Wikipedia links the pollster instead). No
win probabilities: with a dozen candidates and two rounds a model would invent
precision, as with open primaries. Polls refresh every day, which covers the owner's
"every week".

**Parliaments are half-circle seat charts.** "Parlement français" in the France menu
(`#/fr/parlement`) and "U.S. Congress" in the U.S. menu (`#/congress`, added Nov. 2 at
the owner's request) share `js/components/hemicycle.js`: one button per chamber, seats
colored by group with the key underneath, a tooltip with the member's name, group or
party and constituency, the main offices (President, Prime Minister and both chambers'
presidents; President, Speaker and leaders) and a searchable member list. A French group
takes its main party's `--fr-*` color, gray (`--seat-other`) otherwise, and groups sharing
a color get different seat shapes instead of new colors; U.S. seats are D blue, R red,
independents gray. Built once a day by `scripts/fr/parlement.py` (the chambers' open
data, Wikipedia's group tables, Wikidata) and `scripts/update_congress.py` (the House
Clerk's member list, Wikipedia for senators and leaders, Wikidata); each keeps its old
file when a source fails.

**French positions: the candidate's own text, checked word for word.** Positions on
the 144 questions live in `scripts/fr/positions_2027.py` (→ `data/fr/positions.json`,
rebuilt every refresh, no network): programs, campaign sites, the candidate's speeches,
op-eds and interviews, and party documents labelled as such. Quotes are verbatim, at
most 25 words, and were checked against the source text (the cited PDF page) before
going in; a press summary of a proposal has `quote: None` and says so on the page.
programmes-2027.fr and votons-2027.fr (independent directories) are only finders, never
cited. Pages that refuse scripts are read in the browser pane and their text saved for
the quote check. Partial answers get ±1 (see DATA.md); matching (`js/fr/match.js`) uses
the U.S. rule.

**"Comparer avec mes opinions" works like the U.S. "Match with My views".** "Mes
élections" has the button; it leads to the ranking (`#/fr/elections/comparer`), and a
click on a candidate, or the button on each candidate card and candidate page, opens the
three-panel comparison (`js/fr/compare.js`, the U.S. overlay's layout and CSS): agreements
left, differences right, questions with no known position along the bottom. The
questionnaire lives under "Mon profil" (`#/fr/profil/opinions`; the old `#/fr/opinions`
still works) and has no menu entry of its own, as in the U.S. profile menu. On the France
home page, "Préparer mon vote" under the "Qui sera le prochain président" box opens two
choices (owner's wording): "Cliquez ici pour voir mes élections" (`#/fr/elections`) and
"Cliquez ici pour m'aider à trouver le candidat qui me correspond" (the ranking, or the
questionnaire for a visitor with fewer than 5 answers).

**"Les grands enjeux": official figures, and the median for salaries.** `#/fr/enjeux`
(France menu, owner's request, Nov. 3) has seven tabs: economy, inflation, immigration,
crime, wealth gap, education, salaries in France. Figures come from Eurostat, the OECD,
the World Bank, BLS and the Interior Ministry's SSMSI, rebuilt daily by
`scripts/fr/enjeux.py` (→ `data/fr/enjeux.json`), plus INSEE, ONS and PISA figures typed
in `enjeux_sources.py` with the sentence each comes from. Salaries use the median, never
the mean or GDP per head (owner's request, Nov. 3: "more realistic"; the page explains
why), compared with Germany, Belgium, Italy, Spain, the Netherlands, the UK and the US,
in euros at French prices (household consumption PPPs) by default or at the exchange
rate. No source publishes medians by occupation for these countries (Eurostat's
occupation tables, the OECD's teacher and health pay and INSEE's categories are all
means), so jobs are compared by sector, with Eurostat's median hourly pay in 17 NACE
sections, next to the minimum wage; the averages by job were removed, not relabelled.
Each comparison takes every country from one source wherever one exists; a block whose
source fails keeps its last values and is flagged `stale`. Each country takes its flag's
color (owner's request, Nov. 3; see Conventions). Each tab ends with the declared
candidates' stances on its questions; nothing is inferred from the figures.

**Menus (owner's request, Nov. 3).** The U.S. menu puts "Which country?" just above
"About the data". The France menu has no "Les prochaines élections" entry (the calendar
page and `#/fr/calendrier` stay, linked from the home page) and gains "Les grands enjeux".

**Donations: PayPal, then Cash App** (owner's request, Nov. 3). Both "Support the site"
pages (`#/donate`, `#/fr/soutenir`) show "Donate via PayPal" (`DONATE_URL` in
`js/config.js`, the owner's hosted button) above Cash App `$KoCai`. The old
informedvoter.io payment page is gone.

**Google AdSense on every page** (owner's request, Nov. 3). The owner's tag sits in
`index.html`'s `<head>` exactly as given (the only page; every route uses it), and
`ads.txt` at the root names publisher `pub-5447501670286697`. The README's privacy
section says what Google receives, and both About pages' privacy cards tell visitors,
with links to Google's Ads Settings and its partner-sites page, as AdSense's policies
require. Visitors in the EEA, the UK and Switzerland need
consent through a Google-certified platform, which the owner sets up in AdSense (Privacy
& messaging); nothing in the code does it.

**Help tickets and email reminders go through one mail service** (owner's request,
Nov. 3): `services/mail/Code.gs`, a Google Apps Script web app the owner deploys from
the Workspace account caissonez@informedvoter.io (`REMINDER_FROM`), its `/exec` address
in `MAIL_SERVICE_URL` (`js/config.js`; README, "Email reminders and help tickets").
Tickets go to theinformedvoter.help@gmail.com (`SUPPORT_EMAIL`, the script's `HELP_TO`)
with the visitor's address as Reply-To; until the service is live the form opens the
visitor's own email app addressed there. Reminders are double opt-in behind a consent box
(GDPR): sign-ups sit in a Google Sheet of that account, are deleted when the election is
over, on unsubscribing or after 7 days unconfirmed, and are sent by a daily trigger 30, 14
or 7 days ahead. The script takes elections, names and dates only from the live site's
`data/reminders.json` (`scripts/update_reminders.py`, every refresh), never from the
request, answers every sign-up alike (so the form can't tell who signed up) and
rate-limits both kinds of request. Calendar files (.ics) stay. The README's privacy
section and both About pages' privacy cards say what is kept; change them with it.

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
is CC BY-NC-ND, so every Early vote tab credits it, and since the site carries ads
(Nov. 3) it is neither read nor shown (owner's request, Nov. 3): `EARLY_VOTE` in
`update_races.py` and `SHOW_EARLY_VOTE` in `js/config.js` are off. Turn both back on
together, and only with the Lab's permission or without ads.

**Unverified polls stay out of the average.** A poll is included only with a
verifiable source naming the pollster and dates. Campaign internals are labelled
with their sponsor; claims without details go in race `notes`, not `polls`.

**Real race data is rebuilt automatically every 8 hours, never hand-edited.**
`scripts/refresh_all.py` (Windows Task Scheduler, \InformedVoter\, 6:00/14:00/22:00)
runs `scripts/update_races.py`, which writes `data/races.json`, `control.json`,
`status.json` and `data/legislature/`. Wikipedia is the aggregator for candidates, ratings, PVI and polls;
the FEC API for money (falls back to Wikipedia's cited FEC totals without a key);
the House Clerk's roll-call XML for House members' positions. Hand research goes
in `scripts/research/<state>.py`, which write overlays to `data/research/`. The same run
rebuilds Congress and France's candidates and polls, parties, Parliament and "Les grands
enjeux" figures once a day (when the file is over 20 hours old), and France's calendar
and positions and `data/reminders.json` every run.

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
a match percentage there: Dan Green (FL-09, two), Bill Hill and Sydney Gruters (four
each). Third-party and independent Senate and governor candidates are covered by
`candidates_2026.py` (88 candidates, 678 positions) and House challengers in safer
races by `house_challengers_2026.py` (584 candidates in 369 races, 2,912 positions),
both Oct. 26-28: campaign sites (browser-only ones read in the browser pane), States
Newsroom voter guides (candidates' own answers quoted; summaries cited, not quoted),
KQED's summaries of four Northern California races, KATU's "Know Your Candidates"
transcripts (Oregon, southwest Washington), VOTE411 (the League of Women Voters'
guide, read race by race in the browser; on Oct. 28 also for thin candidates in Texas,
Florida, Illinois, Georgia, Virginia, Ohio, Missouri and New Jersey, where most
Republicans and some others left it blank) and, for officeholders with nothing on
their sites, official records (Oberacker's state Senate releases, Solis's county
record). `ivoterguide_2026.py` adds candidates' own iVoterGuide answers (244
candidates, 2,074 positions) only for questions nothing else answers. All told (Oct.
28 build), 1,305 of 1,418 federal and governor candidates have sourced positions and
1,065 have the five a match percentage needs; 240 have one to four. The 113 with none
(mostly Tennessee and Michigan independents and minor-party House candidates, plus 13
Democrats and Republicans in Louisiana's open primaries and Alaska's top-four races
and 17 others) have no usable site, statement, guide answer or record found so far.
Every current House member on the ballot also has positions from 39 recorded House votes, 2021 to 2026, including
11 war powers resolutions (`scripts/lib/house_votes.py`), so members first elected in
2024 have about 20 each; four former members on the ballot (Peltola, Carl, Allred,
Luria) get theirs by Clerk id (`FORMER_MEMBERS` in `update_races.py`). Money by source
comes from FEC summaries for every Senate candidate and every House candidate with a
2026 report (998 candidates through Oct. 14: `fec_2026.py` for the Senate and
competitive House races, `fec_house_2026.py` for the rest); the other 247 House
candidates, mostly third-party, have a sourced note from an FEC search
(`fec_notes_2026.py`: 177 with no 2026 report yet, rechecked Oct. 27, 69 with no FEC
record for their district, and one whose FEC summary doesn't add up). Governors: totals from
state filings via Wikipedia for 14 races; Florida's every candidate grouped by source
from the Division of Elections database (`florida_money_2026.py`: state matching
funds as public financing, each major candidate's political committee in a note,
fetched at most once a day); for the other 21, the latest news report of the filings
as a dated note with its link (`governor_money_2026.py`), never stretched into a
total. Campaign site links come from each race page's "External links" (a
researched `officialSite` wins, and `officialSite: None` drops a dead or parked
domain); `campaign_sites_2026.py` adds 117 the pages lack, mostly California's, from
candidates' Wikipedia articles and BallotReady profiles, each checked live, and the
research overlays add sites found in VOTE411 and other guides (1,264 of 1,418
candidates now have one). Early voting covered 49 states and 155 House districts until
it was switched off on Nov. 3. State
legislative races are real in all 88 chambers voting this year: 5,615 districts,
3,362 with candidates listed; researched legislative candidates (Oklahoma SD 32 and
HD 85 so far) live in `data/research/legislature/`, written by
`legislature_2026.py`. Pages that still show only declared primary candidates
(Massachusetts, the New York Assembly, Kansas, Iowa House, Florida House and others)
give seats, holders and margins but no candidate lists yet. Who sits in Congress
(`data/congress.json`, Nov. 2 build): House 433 of 435 (two vacancies) plus six
delegates, Senate 100. Photos (`data/photos.json`, Nov. 3 build): 566 of the 1,418
candidates, all 400 incumbents among them, out of the 618 whose name links to a
Wikipedia article (the other 52 articles have no Wikidata image that passes the
checks), plus the President and the 11 officers and party leaders on the Congress page;
everyone else shows initials.

France (Nov. 2, 2026): the 2027 presidential dates, candidates and polls refresh daily
from French Wikipedia (who is running cross-checked with franceinfo and
`candidats_2027.py`), parties and Parliament daily, the calendar and positions every
run: 35 declared candidates of the 47 people listed or polled, 44 first-round polls, 7
second-round match-ups. 27 declared candidates have sourced positions, 851 in all (902
with Villepin, Cazeneuve and Bardella, kept for reference): Tondelier 80, Mélenchon 63,
Glucksmann 60, Roussel 51, Attal 48, Dupont-Aignan 47, Lisnard and Asselineau 46,
Philippe 43, Le Pen, Retailleau and Philippot 41, Branco 38, Legendre 35, Ruffin 34,
Zemmour 24, Kazib 20, Arthaud and Bertrand 16, Polony, Markovic and Bouamrane 11, Labib
10, Batho 6, Becht 5, Egger 4, Mikolajczak 3. Asselineau's come from his 2022 program
(the UPR has published none for 2027), Bardella's from the RN's 2024 programs he led,
Markovic's from the Parti animaliste's 2022 and 2024 programs (none for 2027), Becht's
and Polony's from interviews (Sud Radio; Pleinchamp for Polony), Legendre's from his
manifesto (a Google Doc), Egger's from her party's program, which is limited to
institutions on purpose, and Mikolajczak's from a tract until Équinoxe's program comes
out on Nov. 4. Platret, Durif, Lalanne, Mathieu, Mlekuz, Billetdoux, Collovati and Rohou
have no program or usable statement yet. Each candidate has a page
(`#/fr/candidat/<id>`), dated by the latest day its sources were read (`accessed`, set
by `READ`, `LATER` and `later()` in `positions_2027.py`). Parliament (Nov. 2 build):
Assemblée nationale 574 of 577 seats filled, 11 groups and the non-attached; Sénat 348,
9 groups and three senators in none. "Les grands enjeux" (Nov. 3 build): all 20 blocks
read, none stale; Eurostat's 2022 median hourly pay in 17 sectors for the six EU
countries; INSEE's 2025 salaries (median €2,238 net a month, women €2,128, men €2,328),
the ONS's 2022 and 2026 earnings surveys and PISA 2025 typed in by hand.

## Conventions

- Render with the `html\`\`` tag from `js/util.js`: it escapes every interpolation.
  Outside text (news headlines) must never reach innerHTML unescaped.
- Boolean attributes: write `aria-pressed="${String(on)}"`.
- Party colors: D blue, R red, strongest other candidate green, the rest gray.
  Validated with the dataviz palette checker in both themes; don't eyeball new ones.
  France (`--fr-*` in styles.css, keyed by poll abbreviation in `js/fr/data.js`), left to
  right: LFI purple, PCF red, LE green, PS and PP pink, RE and MoDem yellow (Ensemble),
  Horizons teal-green, LR blue, RN dark blue, Reconquête brown; every other party gray.
  All checks pass in both themes, ordered that way (PYTHONIOENCODING=utf-8 for the
  validator on Windows). A smaller party never borrows a bigger one's color.
- Countries on "Les grands enjeux" wear their flags' colors (owner's request, Nov. 3),
  `--cty-*` in styles.css, one set per theme: France navy (the flag's #000091 on the light
  theme, lightened on the dark one), Spain yellow, the EU white, Germany gray, Belgium
  black, Italy green, the Netherlands orange, the UK red, the US light blue; the OECD
  average stays hatched gray. Each was moved as little as the validator allows from the
  flag's own color (`--pairs all`: colorblind ΔE 8.1 light, 9.1 dark; normal vision 15.8
  and 16.8). A color that vanishes on a theme's page gets an outline (`--cty-*-edge`: the
  EU and Spain on light, Belgium on dark; `edge` in `js/lib/charts.js`). Spain and the US
  fall under 3:1 contrast on the light page, so every bar prints its name and value.
- France's map: IGN ADMIN EXPRESS COG CARTO, simplified as a coverage with the
  overseas departments moved into insets (`scripts/fr/build_maps_fr.py`), drawn with a
  conformal conic close to Lambert-93 (`js/fr/map.js`), rings clockwise.
- Photos of real people come from Wikidata/Commons only, shown in gray with their
  author and license in the tooltip and a "Crédits photo" / "Photo credits" list on the
  page, through one shared reader (`scripts/lib/wikiphotos.py`): France's via
  `frwiki.photos`, U.S. candidates' via `scripts/update_photos.py` → `data/photos.json`
  (keyed by the `wiki` link, loaded with the races; `photoOf`, `candBadge` and
  `photoCredits` in `js/components/race.js`), Congress's President and leaders inside
  `data/congress.json`. A photo needs the Wikidata item to be a person (and a U.S.
  citizen, for U.S. pages, wherever Wikidata gives a citizenship); U.S. candidates also
  need their last name in the linked article's title. Everyone else keeps initials.
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
- **Wikimedia's 2026 rate limits: 10 requests a minute for a script whose User-Agent
  has no contact** (an email address or full URL), 200 with one. Past the limit it
  answers 503 "Wikimedia Error" pages and 429s until the minute is up, and those
  refusals count too, so quick retries kept the evening of Oct. 27 locked out (a
  manual rebuild and the 10 PM refresh failed; the old data stayed). `scripts/lib/wikitables.py`
  reads a contact from `INFORMED_VOTER_CONTACT` or `~/.informed-voter/contact`; none
  is set, since the site has no public URL and on Oct. 28 the owner chose the slower
  pace over sending their email (don't ask again unless the site gets a URL). Without
  one it spaces requests 7 seconds apart and waits out Retry-After. It also sends
  gzip and caches pages by revision id.
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
- **Redistricting gives a district one row per sitting member.** Texas 25 lists Roger
  Williams, then Marc Veasey, sharing one candidates cell; keeping only the last row
  dropped Williams as the incumbent (and his House votes) and called the seat
  Democratic. Alabama 2, California 40 and Texas 18, 33 and 37 had the same. Rows for
  one district are merged (`merge_member_rows` in `update_races.py`): every member
  running stays the incumbent, the seat goes to the first running member's party, and
  every member's article is kept for matching votes.
- **Wikipedia's California House page lists no campaign websites**, so its candidates
  had none. Candidates' own Wikipedia articles ("Campaign website") and BallotReady
  profiles have them (`campaign_sites_2026.py`). Accept a BallotReady profile only
  when it names the state and office, and a site only when it answers and shows the
  candidate's name.
- **Lapsed campaign domains get resold.** Jim Baird's old electjimbaird.com, still
  linked from Wikipedia, now redirects to a gambling site, and Gary Dye's listed site
  is his 2020 blog. Check where a link lands, not just that it answers.
- **Position sources must be https** (the validator says so). Jennifer Moore's
  (NY-10) site serves no working https page, so it can't be cited.
- **French Wikipedia hides a sort key in name cells**: "Arthaud, Nathalie Nathalie
  Arthaud". Read the display name after the key, or parties get read as people.
- **French party infoboxes mix past and present** ("Actuel : … Historique : …", with a
  no-break space or tag before the colon) and nest tables inside; `partis.py` keeps only
  the current part and matches tables by depth. Ideology cells also link congresses.
- **French poll tables put one line-up per row** and other candidates in an "Autres"
  cell as value-then-name ("<1 / Bouamrane"); several rows share one poll and notice.
- **The address API moved.** api-adresse.data.gouv.fr gave way to IGN's Géoplateforme
  geocoder (`data.geopf.fr/geocodage/search`), same answer format, CORS allowed.
- **French program links move.** programmes-2027.fr's link to Place publique's "Acte I"
  answered 404; the party's "Le projet" page links the current copy. LFI's program
  pages no longer load, so L'Avenir en commun is cited from the Wayback Machine. Open a
  link before citing it.
- **PDF text splits words** ("livr et industrie", "travai l", "d’ être"), so quote
  checks compare with and without spaces. Write the quote as printed, not as extracted.
- **"epr" matches inside "Reprendre"** and "réparer": search for `\bepr` when looking
  for EPR reactors in a text.
- **votons-2027.fr's "source" links can point at the wrong place**: a site's home page
  (Génération écologie, Bouamrane, Cazeneuve) or a 2027 page whose measures actually
  come from older programs (Équinoxe). Find the text on the candidate's own page or
  document before citing it: Cazeneuve's is La Convention's "synthèse des mesures" PDF,
  Philippot's the Patriotes' "Projet pour la France" PDF, Asselineau's the UPR's 2022
  program page. generationecologie.fr answers scripts with 403, so it is read in the
  browser pane.
- **Trackers of declared candidates disagree.** On Nov. 2 franceinfo's left out Zemmour
  and Bertrand (both announced) and listed Lassalle (a statement conditional on a
  fundraiser); Wikipedia still listed Cazeneuve (now helping Glucksmann) and missed five
  people franceinfo had. Neither is enough alone, hence `candidats_2027.py`.
- **Wikipedia links some poll rows to the pollster's own page** instead of the
  Commission des sondages notice, which used to drop the poll from the average.
  `notice_finder` takes the one vote-intention notice from that pollster filed within ten
  days after the fieldwork, if exactly one is unused.
- **Wikipedia party links carry disambiguators** ("Union populaire républicaine (2007)").
  `partyName` in `js/fr/components.js` strips them for display only, since `partis.py`
  matches parties by the full article title.
- **Wikidata keeps many French names only in the multilingual label** ("mul"), Macron's
  among them: ask for `languages: "fr|mul"` or names come back empty.
- **The Assembly's open data**: a group president also keeps a current "Membre"
  mandate, so read every group mandate; an organ's `libelleAbrev` is its code ("ECOS",
  "UDDPLR", "BURAN" for the Bureau) and `libelleAbrege` its display name ("EcoS", "UDR");
  seat numbers run from right to left; the files sit under the legislature's number (a
  dissolution starts a new one, tried first).
- **The Senate's open data**: `ODSEN_GENERAL.csv` has been Windows-1252 with lines
  starting "%" that repeat the query, and senators for French people abroad carry
  "(Série 1)" or "(Série 2)" in the constituency name.
- **A Google Doc's edit page draws its text with JavaScript**; the public text view
  (`/mobilebasic`) has it as plain HTML, and its text is saved under the cited link's
  cache key for the quote check (Legendre's manifesto).
- **One API batch can ask for a redirect and its target** ("Olivier Faure (homme
  politique)" and "Olivier Faure"). Mapping answers back from the page to one asked-for
  title left the other without a photo; `wikiphotos.py` follows each asked-for title
  forward through normalization and redirects instead.
- **After editing JS, a hash change isn't enough** in the preview: the page keeps the
  modules it loaded, so call `location.reload()` before checking.
- **A hidden browser pane pauses smooth scrolling**, so `scrollTo` seems to do nothing
  before a screenshot; pass `behavior: 'instant'`.
- **Wikipedia's spellings can hide whole records.** It calls CO-8's Libertarian "Dan
  Wood" (Dave Wood), KY-3's Republican "Maria Rodriquez" (Rodriguez) and MI-6's
  Libertarian "Timothy Tegan" (Teagan); the FEC searches under those spellings filed
  Rodriguez and Teagan as having no FEC record when both do. An overlay's `name` wins
  in the merge; search again under the corrected name.
- **VOTE411 renders in a JavaScript widget.** Read it in the browser: a state's "All
  Races" list, then the race, then each candidate's "View Answers" (answers load per
  candidate). Revisiting a race keeps its comparison selections, so clicking again
  hides answers; reload first. Race ids for citations come from the page's own
  requests in the resource-timing list, which fills after about 250 entries; reload to
  read more. Never take the widget's credentials to call its API directly.
- **iVoterGuide is an advocacy group's guide (AFA Action).** Only candidates' own
  agree/disagree answers and multiple-choice picks are used, never its ratings, with
  the statement-to-question table and caps in `ivoterguide_2026.py`. It is generated
  (scratch `ivg_build.py`) to fill only questions nothing else answers, so regenerate
  it after hand research.
- **`officialSite: None` used to vanish in `combine_overlays`**, which treated None as
  "not researched here", so dead links came back when a later file covered the race;
  an explicit None now survives.
- **A candidate entered twice in one overlay isn't merged** until another file covers
  that race (the merge keeps the last copy). Add to an existing entry with `more()`,
  never a second `cand()`; Tennessee's governor list briefly had Seeman and Brewer twice.
- **Withdrawn candidates can stay on the ballot.** Mike Marvin (NE-SEN) withdrew Aug.
  21 and is still printed; his bio says so.
- **The OECD's SDMX keys need one dot-separated part per dimension** (an empty part for
  every code, or `all` for the whole flow); a key with too few or too many parts is
  refused. oecd.org's own pages answer scripts with 403, so publications such as PISA
  are read in the browser pane; the API at sdmx.oecd.org answers.
- **Eurostat's minimum-wage dataset (`earn_mw_cur`) is half-yearly**: `sinceTimePeriod`
  must be a semester ("2024-S1"), not a year.
- **Eurostat's earnings tables carry several units** (`earn_ses_pub2n`: EUR, NAC and
  PPS). Pin `unit=EUR`: purchasing power standards pass for euros (France's 2022 median
  hourly pay is €16.81, and 15.48 in PPS).
- **The OECD's minimum wages come in each country's own pay period** (`PAY_PERIOD` A, M,
  W or H): Belgium and the Netherlands have no hourly figure, so only the yearly one
  covers every country.
- **`python -I` ignores PYTHONIOENCODING.** Add `-X utf8` (the palette validator, or any
  script that prints French) or printing a non-ASCII character fails.
- **The router scrolls to the top after a view's `mount`, and `requestAnimationFrame`
  never fires in a hidden browser pane.** A view that scrolls itself (the jobs card for
  `#/fr/enjeux?t=salaires&metier=…`) uses `setTimeout(…, 0)`, which runs after the
  router's scroll, and remembers the address it scrolled for so a redraw doesn't jump.
- **A link can't carry a query and an anchor.** `parseHash` splits on the first `?`, so
  a second `#` ends up inside the last query value; scroll in `mount` instead.
- **Bars in one grid row each lose their common scale.** Each row sized its own
  columns, so equal values drew different lengths when a label wrapped; `.enj-bar` rows
  use `subgrid`, so every bar list has one track width.

## Open questions

- France: 27 of the 35 declared candidates have sourced positions (851, Nov. 2, 2026),
  but most cover only 10 to 80 of the 144 questions; Mikolajczak (3) and Egger (4) are
  below the 5 a match percentage needs, and Becht (5) and Batho (6) just above. Eight have
  none yet (Platret, Durif, Lalanne, Mathieu, Mlekuz, Billetdoux, Collovati, Rohou), and
  no candidate's text answers q051, q063, q084, q124, q126, q127, q129, q130, q131 or
  q143. Programs still to come (Équinoxe Nov. 4, Zemmour, the UPR's 2027 one), debates
  and newsroom questionnaires should fill this in. Parties show Wikipedia's ideology
  terms; paraphrased program points would need the same research.
- France by address: the commune, department and region are known, but not the
  legislative circonscription (577 districts; needs a district map) or local
  by-elections, so "next elections" is the national calendar filtered by place.
- The mail service waits for the owner to deploy it (README, "Email reminders and help
  tickets") and set `MAIL_SERVICE_URL`; until then tickets go through visitors' own email
  apps and reminders are calendar files. informedvoter.io has SPF and DKIM but no DMARC
  record, which some inboxes hold against its mail.
- Pay by job in France and next door: medians by occupation exist only in national
  sources (INSEE, Destatis and others), with their own definitions and years, so
  "Les grands enjeux" compares sectors instead.
- Whether the U.S. section should also get a French version (it is English only).
- Where challengers' positions come from at scale: research staff, candidate
  self-reporting (the Wahl-O-Mat model), or public questionnaires like WWNO's, the
  States Newsroom guides and VOTE411. Competitive races are hand-researched; safer
  House races' challengers come from campaign sites, those guides and iVoterGuide's
  answers, but 113 candidates still have no usable site, statement or answer, 240 have
  fewer than five positions, and many VOTE411 respondents answer only some questions
  (most Republican challengers answer none). Incumbents are covered by
  votes; senators need a source senate.gov allows.
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
- AdSense consent for visitors in the EEA, the UK and Switzerland: the owner sets up
  AdSense's "European regulations" message (Privacy & messaging). Also open: whether ads
  should run on the pages that show a visitor's answers, matches and address, since an
  ad script can read any page it runs on (political opinions are special-category data
  under GDPR).
