# Informed Voter

A nonpartisan guide to the November 3, 2026 U.S. elections and the April 2027
French presidential election: every race on an interactive map, the voter's own
ballot from their address, forecasts or polls, and a questionnaire that matches
voters with candidates issue by issue, with sources. The France section speaks
French or English (the browser's language picks the first one; a switch in the
header changes it); the U.S. section is in English.

## Run it

You need Python (already installed on this machine). From this folder:

```
py scripts/serve.py
```

(`py` is the Windows Python launcher; on a Mac or Linux use `python3`.)

Then open <http://localhost:8765>. Double-clicking `index.html` will **not**
work: browsers block a page opened from disk from loading its own data files.

## What's real and what's demo

| Real | Demo (fictional, tagged **DEMO** on screen) |
|---|---|
| **Every U.S. Senate, U.S. House and governor race**, refreshed every 8 hours: candidates on the ballot, forecasters' ratings, polls (each linked to its source), fundraising, forecasts and chamber control | Nothing in the races is fictional; what isn't known yet is shown as missing |
| **Every state legislative seat on the 2026 ballot** (88 chambers), refreshed every 8 hours from Wikipedia's chamber pages: who holds it, the district's 2024 presidential margin, and the November candidates where the page lists them (about 3,400 of 5,600 districts). No win odds for these races | State legislative candidates' positions and money aren't loaded |
| Early voting by state and House district, from the University of Florida Election Lab's tracker: switched off while the site carries ads, since the Lab's data is for non-commercial use only (`SHOW_EARLY_VOTE` in `js/config.js` and `EARLY_VOTE` in `scripts/update_races.py` turn it back on together) | |
| Issue positions for every current U.S. House member on the ballot, and four former members running again, from 39 recorded House votes (2021 to 2026, including war powers resolutions) | Issue positions for candidates not yet researched are left blank, not invented |
| Hand-researched races (tagged **SOURCED**): bios and positions with sources for every Senate and governor race on the 2026 ballot, including 88 third-party and independent candidates, both main candidates in the 78 competitive House races (rated Toss-up, Tilt or Lean by any forecaster), Louisiana's six House districts, and 584 House challengers in safer seats, from campaign sites, newsroom voter guides and interviews, VOTE411 (the League of Women Voters' guide) and candidates' own iVoterGuide answers; sourced positions for 1,305 of the 1,418 federal and governor candidates (1,065 with the five a match percentage needs); campaign website links for 1,264 of them; money by source from FEC reports for every Senate candidate and every House candidate with a 2026 report; governors' fundraising from state filings (Florida's broken down by source from the state's own database, with each major candidate's political committee), or the latest news report of them where no table exists | About 113 candidates, mostly minor-party and independent, have no usable site, statement or guide answer; House candidates with no 2026 FEC report yet, and three governor candidates, show money as not loaded yet |
| District maps: Census Bureau 2026 TIGER/Line (120th Congress + 2026 state legislative districts) | |
| Address to district lookup (Census Bureau geocoder) | |
| How-to-vote links (vote.gov, every state's election office, NASS), all checked Oct 2026 | |
| News headlines from 18 outlets across the spectrum | |
| Inflation and interest rates (BLS, Federal Reserve, Freddie Mac via FRED) | |
| Party values (from each party's platform) and leadership (verified Oct 2026) | |
| Who sits in the U.S. House and Senate (the House Clerk's member list; Wikipedia for senators and leaders), refreshed daily | |
| **France:** the 2027 presidential election's dates and its 35 declared candidates only (each checked against a news report of their own announcement and franceinfo's tracker; people polls test who aren't running stay out of the average and the comparison), every published poll for both rounds (each linked to its official notice at the Commission des sondages), 12 parties with their leaders, position and ideology, and who sits in the Assemblée nationale and the Sénat (the chambers' own open data), and the official figures behind seven major issues (Eurostat, the OECD, the World Bank, BLS, the Interior Ministry's crime statistics, INSEE), all refreshed daily; photos from Wikidata and Commons with credits; IGN region and department maps; the election calendar with a source for each date; sourced positions on the 144 French questions for 27 declared candidates (851 positions, each quote checked against its source), a page per candidate, and "Comparer avec mes opinions" as on the U.S. side: a ranking, then agreements, differences and unknown positions side by side | Eight declared candidates have no program or usable statement yet (Platret, Durif, Lalanne and others); most candidates cover 10 to 80 of the 144 questions, and the rest stay undocumented rather than guessed |

Races tagged **LIVE DATA** are refreshed automatically; **SOURCED** races also
carry researched positions. How the data is built and checked is in
**[DATA.md](DATA.md)**, and the site's About page shows the result of every
automatic check from the last refresh.

## Features

- **Intro screen**: choose a country. The United States and France are live; the UK and Canada are shown greyed out. A FR | EN switch sits at the top right.
- **France (`#/fr`)**: countdowns to both rounds of the presidential election (Sunday 18 April and Sunday 2 May 2027); France by region or department, with the largest cities clickable (each opens the race there and the elections that apply); the first-round poll average and every poll and line-up tested; every second-round match-up; the declared candidates in gray photos that blend into the page; the main parties with their leaders; the election calendar (linked from the home page), personal once an address is added; the 144-question "Mes opinions" questionnaire; "Mes élections" with reminders. Under the headline, "Préparer mon vote" opens two choices: see my elections, or help find the candidate right for me (the ranking against the visitor's answers, or the questionnaire first). Candidates and parties are colored by party (LFI purple, RN dark blue, LR blue, Ensemble yellow, Les Écologistes green, and so on).
- **Parlement français (`#/fr/parlement`, in the France menu)**: the Assemblée nationale and the Sénat as half-circle seat charts, one button for each, colored by group with a key underneath; hover over or tap a seat for the member's name, group, party (deputies only: the Senate publishes groups, not parties), constituency and region. Above the chart: the President of the Republic, the Prime Minister and government, and both chambers' presidents; below it, every member in a searchable list.
- **U.S. Congress (`#/congress`, in the U.S. menu)**: the House and the Senate the same way, one button for each: Democrats blue, Republicans red, independents gray, with the leaders, the vacancies and every member's state and district.
- **Les grands enjeux (`#/fr/enjeux`, in the France menu)**: the official figures behind seven debates, one tab each (economy, inflation, immigration, crime, the wealth gap, education, salaries in France), with France next to Germany, Belgium, Italy, Spain, the Netherlands, the UK and the US wherever the figures compare, and what the declared candidates answer on the questionnaire's matching questions. Salaries are measured by the median, never the mean or GDP per head (the page explains why): INSEE's median, deciles and medians for women and men in France, and, next door, median full-time pay, median disposable income, Eurostat's median hourly pay in 17 sectors (no source publishes medians by job for these countries; the averages by job were dropped) and the minimum wage, in euros at French prices or at the exchange rate. Each country takes its flag's color: France navy, Spain yellow, the EU white, Germany gray, Belgium black, Italy green, the Netherlands orange, the UK red and the US light blue.
- **Help button** (bottom right, every page): shortcuts to the main pages (search as you type), short answers, and a form to send a ticket about a question, an error or a data correction, which goes to theinformedvoter.help@gmail.com.
- **Reminders** in My elections (both countries) and the French calendar: a month, two weeks and/or a week before an election, as a calendar file, and by email from caissonez@informedvoter.io once the mail service is deployed (see below).
- **Homepage map**: hover a state to preview it, click to open it. Color by Senate or governor forecast. Above it, Senate, House and governor control: chance of control, expected seats and the expected gain from today's totals, the 80% range, the betting market for comparison, and how the odds have moved.
- **State page**: Federal / State toggle, then Senators / House Representatives (Nebraska shows its single-chamber Legislature). The governor's race appears whenever there is one. House and legislature views show the real district map; click a district for its race. State legislative districts are colored by their 2024 presidential margin (or by the party holding the seat where a chamber's page has no margins), with no win odds.
- **Candidate photos**: candidates with a Wikipedia article show their Wikidata photo in black and white, ringed in their party's color, as on the France pages, with the photographer and license in the tooltip and a "Photo credits" list on each page; the others keep their initials. Congress's leaders have theirs too.
- **Race forecasts**: chance of winning, projected vote share and votes, 100 simulated elections, rating, 80% range and forecasters' ratings, plus tabs for polling (every poll as a dot, the average's change over 7 and 30 days, and a check against published averages), the trend since the first poll, early vote, money by source, and positions.
- **Star** races (star icon) and **like** candidates (heart icon); both lists have their own pages showing weekly changes and funding mix.
- **Close elections**: every race within 5 points, with daily trend charts.
- **Major news**: real headlines, filterable by topic (gains, scandals, endorsements, turnout, money, debates), race and party.
- **Inflation tracker**: 28 official series over 1 to 5 years.
- **Parties and values**: platforms and top-down leadership, including groups like DSA, the Progressive Caucus and the Freedom Caucus.
- **My profile**: US-flag avatar (changeable), **My views** (the 136-question questionnaire, one question per slide, with short definitions for harder terms on hover, focus or tap; the homepage's top button goes straight to it), **My location** (address with consent, matched by the Census Bureau).
- **My elections**: the races on your ballot; match with My views or answer fresh for one election; a ranking, then Similarities (left), Differences (right) and Unclear (bottom) with sources.
- **Donations**: official donation links for liked candidates (verified domains only).
- **Donate to the site** (`#/donate`, and `#/fr/soutenir` in French): "Donate via PayPal" first (`DONATE_URL` in `js/config.js`), then Cash App `$KoCai`.
- Dark and light themes; works on phones.

## Privacy

There is no server and no account. Views, address, stars, likes, reminder choices and
the profile picture live only in the browser's localStorage (the France section keeps
its own copy, apart from the U.S. one). Two things leave the browser, and only when the
visitor sends them: a help ticket, and the email address of a visitor who signs up for
email reminders (below). An address is sent only to a public geocoder
(the U.S. Census Bureau's, or IGN's Géoplateforme for France), and only after the
visitor ticks the consent box. Candidates' photos load from Wikimedia's image servers,
which, like any image host, see the visitor's IP address; nothing else is sent there.

**Ads.** `index.html`, the one page every route uses, loads Google AdSense (publisher
`ca-pub-5447501670286697`). Google and its ad partners therefore receive each visitor's
IP address, browser details and the page's address, and may set cookies to choose and
measure ads. The site sends them nothing else: answers, address and stars stay in the
browser. But the ad script runs inside every page, as ad scripts do, including the pages
that show a visitor's answers and matches. For visitors in the EEA, the UK and
Switzerland, Google requires consent through a Google-certified consent platform: set up
the "European regulations" message under Privacy & messaging in AdSense (no code change
here). Both About pages tell visitors this in their privacy card, with links to
Google's Ads Settings and its page on partner sites, as AdSense's policies require.
`ads.txt` names the publisher account for ad buyers.

**Email reminders and help tickets** go through one small mail service,
`services/mail/Code.gs`: a Google Apps Script web app that sends from the site's Google
Workspace account, caissonez@informedvoter.io. Help tickets are forwarded to
theinformedvoter.help@gmail.com, with the visitor's address as Reply-To. Reminders are
double opt-in: the visitor ticks a consent box, gets a confirmation email, and only then
receives reminders a month, two weeks and/or a week before each round, each with an
unsubscribe link. A sign-up (email address, election, chosen dates, language) is kept in
a Google Sheet of that account and deleted once the election is over, on unsubscribing,
or after 7 days unconfirmed. The emails' election names and dates come from the live
site's `data/reminders.json` (written by `scripts/update_reminders.py` at every refresh),
never from the request, so nobody can make the address send text of their choosing.
Both About pages' privacy cards say all this to visitors.

To turn it on:

1. Signed in to Google as caissonez@informedvoter.io, create a project at
   script.google.com. In Project Settings, tick "Show 'appsscript.json' manifest file in
   editor", then paste `services/mail/appsscript.json` into that file and
   `services/mail/Code.gs` into Code.gs.
2. Pick `setup` in the function menu and Run it once, accepting the permissions it asks
   for (send email, Google Sheets, read the site, triggers). It creates the sheet
   "Informed Voter: email reminder sign-ups" and a daily run at 14:00, Paris time.
3. Deploy → New deployment → Web app, with "Execute as: Me" and "Who has access:
   Anyone". If "Anyone" isn't offered, the Workspace admin console has to allow sharing
   outside the domain (Apps → Google Workspace → Drive and Docs → Sharing settings).
4. Copy the web app's address (ending in `/exec`) into `MAIL_SERVICE_URL` in
   `js/config.js`, and publish the site, `data/reminders.json` included.

Until `MAIL_SERVICE_URL` is set, the ticket form opens the visitor's own email app
addressed to theinformedvoter.help@gmail.com, reminders are calendar files only, and no
email address is collected. After editing Code.gs, publish it as a new version of the
same deployment (Deploy → Manage deployments → Edit → New version) so the address stays
the same. Apps Script lets a Workspace account send about 1,500 emails a day. To help
delivery, add a DMARC record to informedvoter.io's DNS (SPF and DKIM are already set
up): a TXT record named `_dmarc` with `v=DMARC1; p=none`.

## Automatic refresh (every 8 hours)

```
py scripts/refresh_all.py
```

refreshes everything in one go (about 30 seconds once its caches are warm): news,
inflation (daily), the research files, every race, the forecasts and chamber
control, then the validator. If the new race data fails validation, the previous
files are put back and the About page says so. Who sits in Congress and the
candidates' photos are reread once a day. Then the France section, in files of their own: its candidates and polls, parties,
Parliament and the figures behind "Les grands enjeux" once a day (at the first run more
than 20 hours after the last), the
election calendar and the candidates' positions every run. Last, every run writes
`data/reminders.json`, the elections email reminders may cover. Each run is logged to
`data/cache/refresh.log`.

On this computer it is scheduled in Windows Task Scheduler as
**Informed Voter refresh** (in the InformedVoter folder), running at 6:00, 14:00 and 22:00 (a
missed run, say while the PC was asleep, runs as soon as it wakes). To change or
remove it, open Task Scheduler, or run:

```
schtasks /Delete /TN "\InformedVoter\Informed Voter refresh" /F
```

**Fundraising:** the FEC's shared demo key allows only about ten requests an hour,
so without your own key the full breakdown by source (small and large donors, PACs,
party, self-funding, transfers) comes from the FEC summaries read on fec.gov on
Oct. 25-26, 2026 (`scripts/research/fec_2026.py` and `fec_house_2026.py`): every
Senate candidate with money and every House candidate with a 2026 report, through
Oct. 14. Candidates with nothing to show get a note from an FEC search. A
free personal key from <https://api.data.gov/signup/> unlocks full, self-updating FEC
data for every candidate: set it as the Windows user environment variable
`FEC_API_KEY` (or save it in `%USERPROFILE%\.informed-voter\fec_api_key`) and the next
refresh uses it.

**Wikipedia:** since 2026 Wikimedia allows a script only 10 requests a minute
unless its User-Agent gives a way to reach whoever runs it, so the refresh waits 7
seconds between requests (a few extra minutes per run). To let it run at full
speed (200 a minute), save an email address or the site's URL in
`%USERPROFILE%\.informed-voter\contact` (or the user environment variable
`INFORMED_VOTER_CONTACT`); it is sent only to Wikipedia, in the User-Agent header.

Maps only need rebuilding after redistricting: download the Census files listed
at the top of `scripts/build_maps.py`, then run it (needs `pip install shapely pyshp`).

## Deploying

It is a static site, so any static host works (GitHub Pages, Netlify, Cloudflare
Pages): upload the whole folder except `data/cache/`. AdSense reads `ads.txt` only at
the root of the domain, so a site served from a subfolder (a GitHub Pages project
site, say) needs it copied to the domain's root. To keep a hosted copy fresh
without this computer, `.github/workflows/refresh.yml` runs the same refresh every
8 hours on GitHub Actions and commits the new data (add `FEC_API_KEY` as a
repository secret).

## Project layout

```
index.html (the only page; it carries the AdSense tag), ads.txt, css/styles.css
js/main.js, router.js, store.js (browser storage), util.js, icons.js,
   i18n.js (French/English), config.js (mail service, ticket address, donation link,
   early-vote switch)
js/components/help.js (help button), reminders.js (reminders and calendar files),
   hemicycle.js (half-circle seat charts for both parliaments)
js/fr/        the France section: routes, shell, store, data, map, questions, match, compare, views/
data/fr/      presidentielle-2027.json, partis.json, parlement.json, calendrier.json,
              positions.json, enjeux.json, maps/ (generated)
scripts/fr/   update_presidentielle.py, candidats_2027.py (hand check of who is running),
              partis.py, parlement.py, calendrier.py, positions_2027.py, build_maps_fr.py, frwiki.py,
              enjeux.py and enjeux_sources.py (the figures behind "Les grands enjeux")
services/mail/ Code.gs and appsscript.json: the mail service (reminders and tickets), a
              Google Apps Script the owner deploys; data/reminders.json lists the
              elections it may send for (scripts/update_reminders.py)
js/data/      states, questions, parties, demo dataset, world (data access)
js/model/     forecast.js (polling average, win probability, chamber simulation), match.js
js/lib/       map.js, charts.js, census.js (address lookup)
js/views/     one file per page group
data/races.json, control.json, status.json   every race, chamber control, refresh checks (generated)
data/congress.json  who sits in Congress (generated by scripts/update_congress.py)
data/photos.json    candidates' photos and credits (generated by scripts/update_photos.py)
data/legislature/  state legislative races, one file per state (generated)
data/research/  hand-researched overlays (generated by scripts/research/*.py)
data/news.json, data/inflation.json, data/maps/   (generated)
data/cache/   page and vote caches, refresh log (local only)
scripts/      refresh_all.py, update_races.py, validate_races.py, update_news.py,
              update_inflation.py, update_congress.py, update_photos.py, build_maps.py, serve.py
scripts/lib/  wikitables.py, elections.py (parsers), model.py (Python copy of the
              forecast), house_votes.py, fec.py, early_vote.py, legislature.py,
              wikiphotos.py (people's photos from Wikidata and Commons, both sections)
scripts/research/  one script per researched state, plus common.py
vendor/       d3 v7.9.0 (ISC licence)
assets/fonts/ Inter, Bricolage Grotesque, JetBrains Mono (SIL Open Font Licence)
```
