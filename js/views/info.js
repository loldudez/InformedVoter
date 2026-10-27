// Major news, inflation tracker, parties and values, site donations, about the data.

import { html, raw, fetchJSON, fmtDate, timeAgo, fmtPct, signed } from '../util.js';
import { icon } from '../icons.js';
import { PARTIES, GROUPS, PARTIES_AS_OF } from '../data/parties.js';
import { lineChart, cssVar } from '../lib/charts.js';
import { wireTableToggles } from '../components/race.js';
import { realRaceCount, researchedCount, statusData, modelCheck, racesMeta, controlData } from '../data/world.js';

const ext = (href, label) => html`<a href="${href}" target="_blank" rel="noopener noreferrer">${label} ${icon.external()}</a>`;

// News ------------------------------------------------------------------------------

let newsCache = null;
const TOPICS = ['Gains & momentum', 'Scandals', 'Endorsements', 'Turnout', 'Money & ads', 'Debates', 'Campaign trail'];

export const news = {
  title: () => 'Major election news',
  async render(ctx) {
    try { newsCache = newsCache || await fetchJSON('data/news.json'); } catch { newsCache = null; }
    if (!newsCache) return html`<div class="wrap page"><div class="empty">${icon.news()}<h3>News isn’t available</h3><p>Run <code>scripts/update_news.py</code> to fetch the latest headlines.</p></div></div>`;
    const q = ctx.query;
    const topic = TOPICS.includes(q.topic) ? q.topic : null;
    const race = ['Senate', 'House', 'Governor'].includes(q.race) ? q.race : null;
    const party = ['Democrats', 'Republicans'].includes(q.party) ? q.party : null;
    const items = newsCache.items.filter((it) => (!topic || it.topic === topic || it.topics.includes(topic)) && (!race || it.races.includes(race)) && (!party || it.parties.includes(party)));
    const link = (k, v) => {
      const p = new URLSearchParams({ ...(topic && { topic }), ...(race && { race }), ...(party && { party }) });
      if (p.get(k) === v) p.delete(k); else p.set(k, v);
      return `#/news${p.toString() ? `?${p}` : ''}`;
    };
    const chip = (k, v, cur) => html`<a class="chip" href="${link(k, v)}" ${raw(cur === v ? 'aria-current="page" style="background:var(--text-1);color:var(--bg);border-color:var(--text-1)"' : '')}>${v}</a>`;
    return html`<div class="wrap page stack">
      <div><div class="eyebrow">Major news regarding the election</div><h1>The latest from the campaign trail</h1>
        <p class="muted">Election headlines from ${newsCache.feeds.length} outlets across the political spectrum, sorted by topic. Updated ${timeAgo(newsCache.updated)} (${fmtDate(newsCache.updated)}).</p></div>
      <div class="stack-sm">
        <div class="filters" role="group" aria-label="Topic"><span class="eyebrow">Topic</span>${TOPICS.map((t) => chip('topic', t, topic))}</div>
        <div class="filters" role="group" aria-label="Race and party"><span class="eyebrow">Race</span>${['Senate', 'House', 'Governor'].map((t) => chip('race', t, race))}<span class="eyebrow" style="margin-left:10px">Party</span>${['Democrats', 'Republicans'].map((t) => chip('party', t, party))}</div>
      </div>
      <div class="news-list">${items.length ? items.map((it) => html`<article class="news-item">
        <div class="news-meta"><span class="src">${it.source}</span><span>${it.published ? timeAgo(it.published) : ''}</span><span class="topic-tag">${it.topic}</span>${it.races.map((r) => html`<span class="topic-tag">${r}</span>`)}</div>
        <a class="headline" href="${it.link}" target="_blank" rel="noopener noreferrer">${it.title}</a>
        ${it.summary ? html`<p class="small muted" style="margin:0">${it.summary}</p>` : ''}
      </article>`) : html`<div class="empty">No stories match these filters.</div>`}</div>
      <p class="small faint">Sources: ${newsCache.feeds.map((f) => f.name).join(', ')}. Headlines link to the original publisher. Topic tags are assigned automatically from keywords and can be wrong.</p>
    </div>`;
  },
};

// Inflation -------------------------------------------------------------------------

let inflCache = null;
const GROUP_ORDER = ['Overall', 'Food', 'Energy', 'Cars', 'Housing', 'Health', 'Interest rates'];

function yoy(data) {
  const byMonth = new Map(data);
  return data.map(([m, v]) => {
    const [y, mo] = m.split('-');
    const prev = byMonth.get(`${+y - 1}-${mo}`);
    return [m, prev ? (v / prev - 1) * 100 : null];
  }).filter(([, v]) => v != null);
}
const toDate = (m) => new Date(+m.slice(0, 4), +m.slice(5, 7) - 1, 15);

function view(series, years) {
  const raw0 = series.kind === 'index' ? yoy(series.data) : series.data;
  const last = raw0[raw0.length - 1];
  const cutoff = toDate(last[0]);
  cutoff.setFullYear(cutoff.getFullYear() - years);
  const pts = raw0.filter(([m]) => toDate(m) >= cutoff);
  return pts;
}

function seriesCard(s, years, idx) {
  const pts = view(s, years);
  if (!pts.length) return '';
  const [lm, lv] = pts[pts.length - 1];
  const [, fv] = pts[0];
  const fmt = s.kind === 'price' ? (v) => `$${v.toFixed(s.unit.includes('kWh') ? 3 : 2)}` : (v) => `${v.toFixed(1)}%`;
  let change, changeCls = '';
  if (s.kind === 'price') {
    const pct = (lv / fv - 1) * 100;
    change = `${signed(pct, 1, '%')} over ${years} yr${years > 1 ? 's' : ''}`;
    changeCls = pct > 0 ? 'delta-up' : 'delta-down';
  } else {
    const d = lv - fv;
    change = `${signed(d, 1, ' pts')} vs ${years} yr${years > 1 ? 's' : ''} ago`;
    changeCls = d > 0 ? 'delta-up' : 'delta-down';
  }
  const tid = `itbl-${idx}`;
  return html`<article class="card series-card">
    <div class="head"><div><div class="eyebrow">${s.kind === 'index' ? 'Yearly inflation rate' : s.unit}</div><h3 style="margin:2px 0 0">${s.label}</h3></div>
      <div style="text-align:right"><div class="val">${fmt(lv)}</div><div class="small ${changeCls}">${change}</div></div></div>
    <div class="chart" data-infl="${s.id}"></div>
    <div class="row between"><span class="tiny faint">Latest: ${toDate(lm).toLocaleString('en-US', { month: 'long', year: 'numeric' })} · ${s.id}</span><button type="button" class="btn btn-sm btn-ghost" data-table-toggle="${tid}">${icon.table()} Table</button></div>
    <div class="table-wrap" id="${tid}" hidden><table class="data"><thead><tr><th>Month</th><th class="r">${s.kind === 'index' ? 'Change from a year earlier' : 'Value'}</th></tr></thead><tbody>${pts.slice().reverse().map(([m, v]) => html`<tr><td>${toDate(m).toLocaleString('en-US', { month: 'short', year: 'numeric' })}</td><td class="r">${fmt(v)}</td></tr>`)}</tbody></table></div>
  </article>`;
}

export const inflation = {
  title: () => 'Inflation tracker',
  async render(ctx) {
    try { inflCache = inflCache || await fetchJSON('data/inflation.json'); } catch { inflCache = null; }
    if (!inflCache) return html`<div class="wrap page"><div class="empty">Inflation data isn’t available. Run <code>scripts/update_inflation.py</code>.</div></div>`;
    const years = [1, 2, 3, 4, 5].includes(+ctx.query.years) ? +ctx.query.years : 2;
    const byId = Object.fromEntries(inflCache.series.map((s) => [s.id, s]));
    const head = (id) => byId[id] ? yoy(byId[id].data).slice(-1)[0] : null;
    const cpi = head('CPIAUCNS'), core = head('CPILFENS');
    const last = (id) => byId[id]?.data.slice(-1)[0];
    const gas = last('APU000074714'), mort = last('MORTGAGE30US');
    let idx = 0;
    return html`<div class="wrap page stack-lg">
      <div><div class="eyebrow">Inflation tracker</div><h1>What things cost, and how fast it’s changing</h1>
        <p class="muted">Official government price data: the Consumer Price Index and average prices from the Bureau of Labor Statistics, and interest rates from the Federal Reserve and Freddie Mac. Snapshot ${fmtDate(inflCache.updated)}.</p></div>
      <div class="grid grid-4">
        ${cpi ? html`<div class="stat"><div class="eyebrow">Inflation (CPI)</div><div class="value">${fmtPct(cpi[1])}</div><div class="sub">year over year, ${toDate(cpi[0]).toLocaleString('en-US', { month: 'long' })}</div></div>` : ''}
        ${core ? html`<div class="stat"><div class="eyebrow">Core inflation</div><div class="value">${fmtPct(core[1])}</div><div class="sub">excluding food and energy</div></div>` : ''}
        ${gas ? html`<div class="stat"><div class="eyebrow">Gasoline</div><div class="value">$${gas[1].toFixed(2)}</div><div class="sub">per gallon, regular</div></div>` : ''}
        ${mort ? html`<div class="stat"><div class="eyebrow">30-year mortgage</div><div class="value">${fmtPct(mort[1], 2)}</div><div class="sub">average rate</div></div>` : ''}
      </div>
      <div class="row between"><div class="seg" role="group" aria-label="Time range">${[1, 2, 3, 4, 5].map((y) => html`<a href="#/inflation?years=${y}" ${raw(y === years ? 'aria-current="page"' : '')}>${y} year${y > 1 ? 's' : ''}</a>`)}</div>
        <span class="small faint">Prices rising faster is shown in red; falling or slowing in green.</span></div>
      ${GROUP_ORDER.map((g) => {
        const list = inflCache.series.filter((s) => s.group === g);
        if (!list.length) return '';
        return html`<section><div class="section-head"><h2 style="margin:0">${g === 'Cars' ? 'Cars and transportation' : g}</h2></div><div class="grid grid-3">${list.map((s) => seriesCard(s, years, idx++))}</div></section>`;
      })}
      <p class="small faint">Sources: ${inflCache.sources.CPI}; ${inflCache.sources.MORTGAGE30US}; ${inflCache.sources.rates}. ${inflCache.sources.via}. Yearly inflation compares each month with the same month a year earlier. A few months are missing where the government did not publish data (for example during the fall 2025 shutdown).</p>
    </div>`;
  },
  mount(root, ctx) {
    if (!inflCache) return;
    const years = [1, 2, 3, 4, 5].includes(+ctx.query.years) ? +ctx.query.years : 2;
    const color = cssVar('--dem');
    root.querySelectorAll('[data-infl]').forEach((el) => {
      const s = inflCache.series.find((x) => x.id === el.dataset.infl);
      const pts = view(s, years);
      const fmt = s.kind === 'price' ? (v) => `$${v.toFixed(s.unit.includes('kWh') ? 3 : 2)}` : (v) => `${v.toFixed(1)}%`;
      lineChart(el, {
        series: [{ name: s.label, color, values: pts.map(([m, v]) => ({ x: toDate(m), y: v })) }],
        height: 150, yFormat: fmt, area: true, baseline: s.kind === 'index' ? 0 : null, endLabels: false,
        label: `${s.label} over ${years} years`,
      });
    });
    wireTableToggles(root);
  },
};

// Parties ---------------------------------------------------------------------------

function ladder(leaders) {
  if (!leaders?.length) return '';
  return html`<ol class="ladder">${leaders.map(([role, who]) => html`<li><span><span class="role">${role}</span><span class="who">${who}</span></span></li>`)}</ol>`;
}
function groupCard(id) {
  const g = GROUPS[id];
  return html`<div class="group-card">
    <div class="row between"><h3 style="margin:0">${g.name}</h3>${ext(g.site, 'Official site')}</div>
    <p class="small muted" style="margin:6px 0 0">${g.blurb}</p>
    <ul class="small muted" style="padding-left:18px;margin:8px 0 0">${g.values.map((v) => html`<li style="margin:4px 0">${v}</li>`)}</ul>
    ${ladder(g.leaders)}
    <p class="tiny faint" style="margin:8px 0 0">Source: ${ext(g.source, g.sourceLabel)}</p>
  </div>`;
}
function partyCard(p) {
  return html`<article class="card party-card tone-${p.tone} stack">
    <div class="row between"><h2 style="margin:0">${p.name}</h2>${ext(p.site, 'Official site')}</div>
    <p class="muted" style="margin:0">${p.blurb}</p>
    <div class="grid grid-2" style="align-items:start">
      <div><div class="eyebrow">What the party says it stands for</div><ul>${p.values.map((v) => html`<li>${v}</li>`)}</ul><p class="tiny faint" style="margin:8px 0 0">Summarized from ${ext(p.source, p.sourceLabel)}</p></div>
      <div><div class="eyebrow">Leadership, top down</div>${ladder(p.leaders) || html`<p class="small muted">See the party’s official site.</p>`}</div>
    </div>
    ${p.groups ? html`<div><div class="eyebrow" style="margin-bottom:10px">Groups within the party</div><div class="grid grid-2">${p.groups.map(groupCard)}</div></div>` : ''}
  </article>`;
}

export const parties = {
  title: () => 'Parties and values',
  render: () => html`<div class="wrap page stack-lg">
    <div><div class="eyebrow">The main parties and values</div><h1>Who the parties are and what they stand for</h1>
      <p class="muted">Each summary paraphrases the organization’s own platform or statement of principles; follow the source links for the full text. Leadership as of ${PARTIES_AS_OF}.</p></div>
    ${PARTIES.slice(0, 2).map(partyCard)}
    <section><div class="section-head"><h2 style="margin:0">Across the aisle</h2></div>${groupCard('psc')}</section>
    <section><div class="section-head"><h2 style="margin:0">Other parties</h2></div><div class="grid grid-2">${PARTIES.slice(2).map(partyCard)}</div></section>
  </div>`,
};

// Donate to the site ----------------------------------------------------------------

export const donate = {
  title: () => 'Support Informed Voter',
  render: () => html`<div class="wrap page stack" style="max-width:820px">
    <div><div class="eyebrow">Donating to the site</div><h1>Keep Informed Voter running</h1><p class="muted">Informed Voter is independent and free to use. Donations go to running the site, not to any candidate, party or campaign.</p></div>
    <div class="card stack" style="text-align:center;padding:32px">
      <div class="eyebrow">Cash App</div>
      <div class="cashtag grad-text">$KoCai</div>
      <div><a class="btn btn-primary" href="https://cash.app/$KoCai" target="_blank" rel="noopener noreferrer">${icon.dollar()} Donate with Cash App ${icon.external()}</a></div>
      <p class="small faint" style="margin:0">Opens Cash App’s page for $KoCai in a new tab.</p>
    </div>
    <div class="card"><h3>More ways to give</h3><p class="muted" style="margin:0">Coming soon.</p></div>
    <p class="small faint">Donations to Informed Voter are not political contributions and are not tax-deductible.</p>
  </div>`,
};

// About -----------------------------------------------------------------------------

const fmtWhen = (d) => { d = new Date(d); return `${fmtDate(d)}, ${d.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' })}`; };

// The refresh's automatic checks, plus one the browser runs itself: recompute every
// race with this page's copy of the model and compare with the refresh's result.
function statusCard() {
  const st = statusData();
  if (!st) {
    return html`<div class="card" id="status"><h3>Data status</h3><p class="muted small" style="margin:0">No refresh has run on this copy of the site yet. Run <code>py scripts/refresh_all.py</code>.</p></div>`;
  }
  const mc = modelCheck;
  const checks = [...st.checks];
  if (mc) {
    checks.push({
      status: mc.mismatches.length ? 'fail' : 'pass', label: 'This page’s model reproduces the refresh',
      detail: mc.mismatches.length ? `${mc.mismatches.length} of ${mc.checked} races differ: ${mc.mismatches.slice(0, 8).map((m) => m.id).join(', ')}` : `All ${mc.checked} head-to-head races recomputed in your browser match the refresh’s Python run.`,
    });
  }
  const c = st.counts;
  const next = new Date(new Date(st.updated).getTime() + (st.nextRefreshHours || 8) * 3600e3);
  const tally = { pass: 0, warn: 0, fail: 0, info: 0 };
  checks.forEach((x) => { tally[x.status] = (tally[x.status] || 0) + 1; });
  return html`<div class="card stack" id="status">
    <div class="row between"><h3 style="margin:0">Data status</h3><span class="small faint">Refreshed ${timeAgo(st.updated)} (${fmtWhen(st.updated)}) · next refresh due around ${fmtWhen(next)}</span></div>
    <div class="grid grid-4">
      <div class="stat"><div class="eyebrow">Races</div><div class="value">${c.races}</div><div class="sub">${c.senate} Senate · ${c.governor} governor · ${c.house} House</div></div>
      <div class="stat"><div class="eyebrow">Polls</div><div class="value">${c.polls.toLocaleString('en-US')}</div><div class="sub">in ${c.withPolls} races</div></div>
      <div class="stat"><div class="eyebrow">Rated by forecasters</div><div class="value">${c.rated}</div><div class="sub">the rest start from partisan lean</div></div>
      <div class="stat"><div class="eyebrow">With fundraising</div><div class="value">${c.withMoney}</div><div class="sub">${c.researched} with researched positions</div></div>
    </div>
    <p class="small muted" style="margin:0">${tally.pass} checks passed${tally.warn ? `, ${tally.warn} need a look` : ''}${tally.fail ? `, ${tally.fail} failed` : ''}. Warnings are shown as they are: they mark where this site’s numbers differ from someone else’s, not errors to hide.</p>
    <ul class="check-list">${checks.map((x) => html`<li><span class="st ${x.status}">${x.status}</span><div><b>${x.label}</b><div class="detail">${x.detail}</div></div></li>`)}</ul>
    ${st.warnings?.length ? html`<details><summary class="small">${st.warnings.length} note${st.warnings.length === 1 ? '' : 's'} from the last refresh</summary><ul class="small muted" style="padding-left:18px">${st.warnings.map((w) => html`<li>${w}</li>`)}</ul></details>` : ''}
    <p class="tiny faint" style="margin:0">Sources: ${(racesMeta()?.sources || []).map((x, i) => html`${i ? ' · ' : ''}${ext(x.url, x.title.replace('Wikipedia: ', ''))}`)} (Wikipedia, CC BY-SA, used as an aggregator; each poll links to its own source) · FEC · Polymarket (cross-check only).</p>
  </div>`;
}

export const about = {
  title: () => 'About the data',
  render: () => html`<div class="wrap page stack" style="max-width:960px">
    <div><div class="eyebrow">About the data</div><h1>What’s real, and what’s a placeholder</h1></div>
    <div class="grid grid-2">
      <div class="card"><h3>${icon.check()} Real data</h3><ul class="small muted" style="padding-left:18px">
        ${realRaceCount ? html`<li><b>Every U.S. Senate, U.S. House and governor race</b>, refreshed every 8 hours: the candidates on the ballot, forecasters’ ratings (Cook, Sabato, Inside Elections and up to eight more), polls with a link to each poll’s source, and fundraising reports.</li>
        <li>${researchedCount} race${researchedCount === 1 ? '' : 's'} also ${researchedCount === 1 ? 'has' : 'have'} hand-researched bios and issue positions, each linked to the candidate’s own words or votes (tagged <span class="real-chip">Sourced</span>).</li>
        <li><b>State legislative races</b>: every seat on the ballot, who holds it, the district’s 2024 presidential margin and the November candidates where Wikipedia’s 2026 chamber page lists them, refreshed every 8 hours. They get no win odds: almost none are polled and few are rated.</li>
        <li>Early voting: ballots cast so far in each state, and in House districts where the count is complete, from the University of Florida Election Lab’s tracker (Michael McDonald).</li>` : ''}
        <li>District maps: U.S. Census Bureau 2026 TIGER/Line boundaries (120th Congress districts and 2026 state legislative districts), clipped to the shoreline.</li>
        <li>Address lookup: the Census Bureau geocoder, which already reflects mid-decade redistricting.</li>
        <li>How-to-vote links: vote.gov, each state’s official election office, and NASS. Every link checked October 2026.</li>
        <li>News: headlines from 18 outlets’ public feeds, refreshed by script.</li>
        <li>Inflation: BLS price data and Federal Reserve / Freddie Mac rates via FRED.</li>
        <li>Parties: summaries of each party’s own platform, with leadership verified in October 2026.</li>
      </ul></div>
      <div class="card"><h3>${icon.info()} ${realRaceCount ? 'Missing, not invented' : html`Still demo <span class="demo-chip">Demo</span>`}</h3><ul class="small muted" style="padding-left:18px">
        ${realRaceCount ? html`<li>Every race now uses real data. What isn’t known yet is shown as missing, never made up: state legislative candidates a chamber’s page doesn’t list yet, and their positions and money, which aren’t loaded.</li>
        <li>Issue positions for races not yet researched are left blank rather than guessed, so those races can’t be matched against your views yet.</li>` : html`<li>Candidate names, bios, polls, fundraising and positions are fictional.</li>`}
      </ul><p class="small faint" style="margin:0">Everything demo carries a yellow DEMO tag. See DATA.md in the project for how real data is added.</p></div>
    </div>
    ${statusCard()}
    <div class="card"><h3>How the forecast works</h3>
      <p class="muted small">Each race starts from an expected margin. Where forecasters rate the race, their ratings set it: Safe or Solid means at least 15 points, Likely 7 to 15, Lean 3 to 7, Tilt under 3, and a toss-up within 2. The district’s partisan lean (its Cook PVI plus the national generic-ballot average${racesMeta()?.generic ? `, now D ${signed(racesMeta().generic.margin)}` : ''}) places the race inside each rating’s range, and the outlets are averaged. Races no forecaster lists as competitive start from the partisan lean alone, with a wider range of error.</p>
      <p class="muted small">Polls are averaged with more weight on recent (14-day half-life), larger and likely-voter surveys, and the average gets more say the more polling there is, up to 85%. The gap between the top two candidates, divided by a typical polling miss (wider with few polls or more time left), gives each candidate’s chance of winning. Open primaries, where every candidate shares one ballot, show the expected split between the parties instead of a winner.</p>
      <p class="muted small" style="margin:0">Chamber control simulates every race 20,000 times. Each simulation draws one national polling miss (3.5 points on the margin) shared by every race, so races move together the way they do on a real election night. Expected seats are the average across simulations, rounded to whole seats that add up to the full chamber (seats likely to go to independents who caucus with neither party are counted separately); expected gains compare them with each party’s seats today${controlData()?.senate?.current?.asOf ? ` (as of ${fmtDate(controlData().senate.current.asOf + 'T12:00:00')})` : ''}. Every refresh checks the totals add up, compares the polling averages with published ones, compares expected seats with each forecaster’s own count, and compares control odds with the betting market. The results are in Data status above.</p>
    </div>
    <div class="card"><h3>Your privacy</h3><p class="muted small" style="margin:0">There are no accounts and no server. Your views, address, stars, likes and picture are stored only in this browser’s local storage. Your address is sent only to the U.S. Census Bureau to find your districts. Clearing your browser data removes everything.</p></div>
  </div>`,
};
