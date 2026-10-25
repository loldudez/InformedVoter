# Informed Voter

A nonpartisan guide to the November 3, 2026 U.S. elections: every race on an
interactive map, the voter's own ballot from their address, forecasts, and a
questionnaire that matches voters with candidates issue by issue, with sources.

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
| **Every U.S. Senate, U.S. House and governor race**, refreshed every 8 hours: candidates on the ballot, forecasters' ratings, polls (each linked to its source), fundraising, forecasts and chamber control | State legislative races (no free nationwide source for their candidates and polls) |
| Issue positions for every current U.S. House member on the ballot, from ten recorded House votes | Issue positions for candidates not yet researched are left blank, not invented |
| Hand-researched races (tagged **SOURCED**): bios, campaign links and positions with sources for Louisiana's Senate race and all six House districts, and the Senate and governor races in Texas, Oklahoma and Ohio | |
| District maps: Census Bureau 2026 TIGER/Line (120th Congress + 2026 state legislative districts) | |
| Address to district lookup (Census Bureau geocoder) | |
| How-to-vote links (vote.gov, every state's election office, NASS), all checked Oct 2026 | |
| News headlines from 18 outlets across the spectrum | |
| Inflation and interest rates (BLS, Federal Reserve, Freddie Mac via FRED) | |
| Party values (from each party's platform) and leadership (verified Oct 2026) | |

Races tagged **LIVE DATA** are refreshed automatically; **SOURCED** races also
carry researched positions. How the data is built and checked is in
**[DATA.md](DATA.md)**, and the site's About page shows the result of every
automatic check from the last refresh.

## Features

- **Intro screen**: choose a country. United States is live; UK, Canada and France are shown greyed out.
- **Homepage map**: hover a state to preview it, click to open it. Color by Senate or governor forecast. Above it, Senate, House and governor control: chance of control, expected seats and the expected gain from today's totals, the 80% range, the betting market for comparison, and how the odds have moved.
- **State page**: Federal / State toggle, then Senators / House Representatives (Nebraska shows its single-chamber Legislature). The governor's race appears whenever there is one. House and legislature views show the real district map; click a district for its race.
- **Race forecasts**: chance of winning, projected vote share and votes, 100 simulated elections, rating, 80% range and forecasters' ratings, plus tabs for polling (every poll as a dot, the average's change over 7 and 30 days, and a check against published averages), the trend since the first poll, early vote, money by source, and positions.
- **Star** races (star icon) and **like** candidates (heart icon); both lists have their own pages showing weekly changes and funding mix.
- **Close elections**: every race within 5 points, with daily trend charts.
- **Major news**: real headlines, filterable by topic (gains, scandals, endorsements, turnout, money, debates), race and party.
- **Inflation tracker**: 28 official series over 1 to 5 years.
- **Parties and values**: platforms and top-down leadership, including groups like DSA, the Progressive Caucus and the Freedom Caucus.
- **My profile**: US-flag avatar (changeable), **My views** (the 136-question questionnaire, one question per slide), **My location** (address with consent, matched by the Census Bureau).
- **My elections**: the races on your ballot; match with My views or answer fresh for one election; a ranking, then Similarities (left), Differences (right) and Unclear (bottom) with sources.
- **Donations**: official donation links for liked candidates (verified domains only).
- **Donate to the site**: Cash App `$KoCai`.
- Dark and light themes; works on phones.

## Privacy

There is no server and no account. Views, address, stars, likes and the profile
picture live only in the browser's localStorage. The address is sent only to the
U.S. Census Bureau geocoder, and only after the visitor ticks the consent box.

## Automatic refresh (every 8 hours)

```
py scripts/refresh_all.py
```

refreshes everything in one go (about 30 seconds once its caches are warm): news,
inflation (daily), the research files, every race, the forecasts and chamber
control, then the validator. If the new race data fails validation, the previous
files are put back and the About page says so. Each run is logged to
`data/cache/refresh.log`.

On this computer it is scheduled in Windows Task Scheduler as
**Informed Voter refresh** (in the InformedVoter folder), running at 6:00, 14:00 and 22:00 (a
missed run, say while the PC was asleep, runs as soon as it wakes). To change or
remove it, open Task Scheduler, or run:

```
schtasks /Delete /TN "\InformedVoter\Informed Voter refresh" /F
```

**Fundraising:** the FEC's shared demo key allows only a few dozen requests an hour,
so until you add your own key the site uses the FEC totals that Wikipedia's race
pages cite (raised, spent and cash on hand, without the donor breakdown). A free
personal key from <https://api.data.gov/signup/> unlocks full FEC data: set it as
the Windows user environment variable `FEC_API_KEY` and the next refresh uses it.

Maps only need rebuilding after redistricting: download the Census files listed
at the top of `scripts/build_maps.py`, then run it (needs `pip install shapely pyshp`).

## Deploying

It is a static site, so any static host works (GitHub Pages, Netlify, Cloudflare
Pages): upload the whole folder except `data/cache/`. To keep a hosted copy fresh
without this computer, `.github/workflows/refresh.yml` runs the same refresh every
8 hours on GitHub Actions and commits the new data (add `FEC_API_KEY` as a
repository secret).

## Project layout

```
index.html, css/styles.css
js/main.js, router.js, store.js (browser storage), util.js, icons.js
js/data/      states, questions, parties, demo dataset, world (data access)
js/model/     forecast.js (polling average, win probability, chamber simulation), match.js
js/lib/       map.js, charts.js, census.js (address lookup)
js/views/     one file per page group
data/races.json, control.json, status.json   every race, chamber control, refresh checks (generated)
data/research/  hand-researched overlays (generated by scripts/research/*.py)
data/news.json, data/inflation.json, data/maps/   (generated)
data/cache/   page and vote caches, refresh log (local only)
scripts/      refresh_all.py, update_races.py, validate_races.py, update_news.py,
              update_inflation.py, build_maps.py, serve.py
scripts/lib/  wikitables.py, elections.py (parsers), model.py (Python copy of the
              forecast), house_votes.py, fec.py
scripts/research/  one script per researched state, plus common.py
vendor/       d3 v7.9.0 (ISC licence)
assets/fonts/ Inter, Bricolage Grotesque, JetBrains Mono (SIL Open Font Licence)
```
