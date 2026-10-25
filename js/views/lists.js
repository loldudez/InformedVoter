// Starred elections, liked candidates, close elections, and profile donations.

import { html, raw, initials, fmtPct, fmtProb, fmtMoney, signed, fmtShortDate } from '../util.js';
import { icon } from '../icons.js';
import { store } from '../store.js';
import { STATE_BY_ABBR } from '../data/states.js';
import { fc, hist, weekChange, allRaces, ensureRace, ensureCandidate, getRace, raceTitle, officeLabel, financeOf, isDemo } from '../data/world.js';
import { candColors, sparkline, lineChart } from '../lib/charts.js';
import { PARTY_NAME, starBtn, heartBtn, demoChip, dataChip, lastName, miniH2H, ratingChip, financeCard, financeNote, leadStr } from '../components/race.js';
import { verifiedDonateUrl } from './elections.js';

const arrow = (d, unit = ' pts', digits = 1) => {
  if (Math.abs(d) < 0.05) return html`<span class="faint">no change</span>`;
  return html`<span class="num">${d > 0 ? icon.arrowUp() : icon.arrowDown()} ${signed(d, digits, unit)}</span>`;
};

// Starred -------------------------------------------------------------------------

// Open primaries have no odds to track week to week; show the field instead.
function openStarredCard(race, f) {
  const poll = race.polls[0];
  const byMoney = [...f.cands].sort((a, b) => (financeOf(b)?.total || 0) - (financeOf(a)?.total || 0));
  const top = poll ? f.cands.filter((c) => poll.results[c.id] != null).slice(0, 3) : [];
  return html`<article class="card stack">
    <div class="row between">
      <div><div class="eyebrow">${officeLabel(race)} · ${STATE_BY_ABBR[race.state].name}</div><h3 style="margin:2px 0 0;font-size:19px"><a href="#/race/${encodeURIComponent(race.id)}" style="text-decoration:none">${raceTitle(race)}</a></h3></div>
      <div class="row">${dataChip(race)}${ratingChip(f)}${starBtn(race.id)}</div>
    </div>
    <div class="grid grid-3">
      <div class="stat"><div class="eyebrow">Format</div><div class="value" style="font-size:20px">Open primary</div><div class="sub">${f.cands.length} candidates on one ballot</div></div>
      <div class="stat"><div class="eyebrow">Latest poll</div>${top.length ? top.map((c) => html`<div class="row between small" style="margin-top:4px"><span>${c.name}</span><b>${c.share.toFixed(1)}%</b></div>`) : html`<div class="sub">No public polls</div>`}</div>
      <div class="stat"><div class="eyebrow">Forecasters</div><div class="value" style="font-size:20px">${f.rating}</div><div class="sub">No week-to-week odds for open primaries</div></div>
    </div>
    <div><div class="eyebrow" style="margin-bottom:8px">Top fundraisers, by source</div><div class="grid grid-2">${byMoney.slice(0, 4).map((c) => financeCard(c))}</div>${financeNote(race)}</div>
  </article>`;
}

function starredCard(race) {
  const f = fc(race);
  if (f.open) return openStarredCard(race, f);
  const wk = weekChange(race);
  const colors = candColors(f.cands);
  const h = hist(race);
  const leadSeries = h.map((d) => (d.fc.cands.find((c) => c.id === f.lead.id)?.win ?? 0) * 100);
  return html`<article class="card stack">
    <div class="row between">
      <div><div class="eyebrow">${officeLabel(race)} · ${STATE_BY_ABBR[race.state].name}</div><h3 style="margin:2px 0 0;font-size:19px"><a href="#/race/${encodeURIComponent(race.id)}" style="text-decoration:none">${raceTitle(race)}</a></h3></div>
      <div class="row">${dataChip(race)}${ratingChip(f)}${starBtn(race.id)}</div>
    </div>
    <div class="grid grid-3">
      <div class="stat"><div class="eyebrow">Chance of winning</div>${f.cands.slice(0, 2).map((c) => html`<div class="row between small" style="margin-top:4px"><span><i class="key-box" style="background:${colors[c.id]}"></i> ${c.name}</span><b>${fmtProb(c.win)}</b></div>`)}</div>
      <div class="stat"><div class="eyebrow">Past 7 days</div>${wk.cands.slice(0, 2).map((d) => {
        const c = f.cands.find((x) => x.id === d.id);
        return html`<div class="row between small" style="margin-top:4px"><span>${lastName(c.name)} odds</span>${arrow(d.win * 100)}</div>`;
      })}<div class="row between small" style="margin-top:4px"><span>Model margin</span>${wk.dr != null ? arrow(wk.dr) : html`<span class="faint">—</span>`}</div></div>
      <div class="stat"><div class="eyebrow">${lastName(f.lead.name)}’s odds, 30 days</div>${raw(sparkline(leadSeries, { width: 220, height: 46, color: colors[f.lead.id], label: `${f.lead.name} win probability over 30 days` }))}<div class="sub">Now ${fmtProb(f.pLead)} · margin ${leadStr(f)}</div></div>
    </div>
    <div><div class="eyebrow" style="margin-bottom:8px">Money raised, by source</div><div class="grid grid-2">${f.cands.slice(0, 2).map((c) => financeCard(c))}</div>${financeNote(race)}</div>
  </article>`;
}

export const starred = {
  title: () => 'Starred elections',
  rerenderOn: ['starred'],
  async render() {
    const ids = store.get().starred;
    const races = (await Promise.all(ids.map((id) => ensureRace(id)))).filter(Boolean);
    return html`<div class="wrap page stack">
      <div><div class="eyebrow">Starred elections</div><h1>Races you’re following</h1><p class="muted">Changes over the past week in odds and polling, plus who is funding each campaign.</p></div>
      ${races.length ? races.map(starredCard) : html`<div class="empty">${icon.star()}<h3>No starred elections yet</h3><p>Tap the star on any race to follow it here.</p><a class="btn" href="#/">Browse the map</a></div>`}
    </div>`;
  },
};

// Liked ---------------------------------------------------------------------------

const SORTS = {
  raised: ['Most raised', (a, b) => raisedOf(b) - raisedOf(a)],
  small: ['Most small-donor funded', (a, b) => share(b, 'small') - share(a, 'small')],
  pac: ['Most PAC funded', (a, b) => share(b, 'pac') - share(a, 'pac')],
  gain: ['Biggest gain this week', (a, b) => b.wk - a.wk],
};
const share = (x, k) => (x.fin && x.fin.total ? (x.fin.parts[k] || 0) / x.fin.total : 0);
const raisedOf = (x) => x.fin?.total || 0;

function likedCard({ c, race, f, fin, wk }) {
  const colors = candColors(f.cands);
  const me = f.cands.find((x) => x.id === c.id);
  const h = hist(race).map((d) => (d.fc.cands.find((x) => x.id === c.id)?.win ?? 0) * 100);
  const grassroots = share({ fin }, 'small') * 100, pac = share({ fin }, 'pac') * 100, pub = share({ fin }, 'public') * 100;
  const hasMoney = fin && fin.total > 0;
  return html`<article class="card stack">
    <div class="row" style="align-items:flex-start">
      <div class="badge" style="background:${colors[c.id]}">${initials(c.name)}</div>
      <div style="flex:1;min-width:0"><div class="cand-name">${c.name}</div><div class="cand-party">${PARTY_NAME[c.party] || c.party} · <a href="#/race/${encodeURIComponent(race.id)}">${raceTitle(race)}</a></div></div>
      <div class="row">${dataChip(race)}${heartBtn(c.id, c.name)}</div>
    </div>
    <div class="grid grid-3">
      ${f.open
        ? html`<div class="stat"><div class="eyebrow">Race format</div><div class="value" style="font-size:20px">Open primary</div><div class="sub">${me.share != null ? `${fmtPct(me.share)} in the latest poll` : 'Not listed in the latest poll'}</div></div>`
        : html`<div class="stat"><div class="eyebrow">Chance of winning</div><div class="value">${fmtProb(me.win)}</div><div class="sub">${arrow(wk * 100)} this week</div></div>`}
      <div class="stat"><div class="eyebrow">Odds, last 30 days</div>${h.length ? raw(sparkline(h, { width: 220, height: 46, color: colors[c.id], label: `${c.name} win probability over 30 days` })) : html`<div class="sub">No daily odds for this race</div>`}</div>
      <div class="stat"><div class="eyebrow">Total raised</div><div class="value">${hasMoney ? fmtMoney(fin.total) : '—'}</div><div class="sub">${!hasMoney ? 'No FEC report on file' : fin.demo ? `+${fmtMoney(fin.total - fin.weekAgoTotal)} this week` : `through ${fmtShortDate(fin.asOf + 'T12:00:00')}`}</div></div>
    </div>
    ${financeCard(c)}
    ${hasMoney ? html`<p class="small muted" style="margin:0">${fmtPct(grassroots, 0)} from small donors · ${fmtPct(pac, 0)} from PACs, where business and labor money shows up${pub > 0 ? ` · ${fmtPct(pub, 0)} public financing` : ''}.</p>` : ''}
  </article>`;
}

export const liked = {
  title: () => 'Liked candidates',
  rerenderOn: ['liked'],
  async render(ctx) {
    const sort = SORTS[ctx.query.sort] ? ctx.query.sort : 'raised';
    const ids = store.get().liked;
    const cands = (await Promise.all(ids.map((id) => ensureCandidate(id)))).filter(Boolean);
    const items = cands.map((c) => {
      const race = getRace(c.raceId);
      const wk = weekChange(race).cands.find((x) => x.id === c.id)?.win ?? 0;
      return { c, race, f: fc(race), fin: financeOf(c), wk };
    }).sort(SORTS[sort][1]);
    return html`<div class="wrap page stack">
      <div><div class="eyebrow">Liked candidates</div><h1>Candidates you’ve liked</h1><p class="muted">Weekly change in their odds, how much they’ve raised, and how much comes from small donors versus PACs or public financing.</p></div>
      ${items.length ? html`<div class="filters" role="group" aria-label="Sort">${Object.entries(SORTS).map(([k, [label]]) => html`<a class="chip" href="#/liked?sort=${k}" ${raw(k === sort ? 'aria-current="page" style="background:var(--text-1);color:var(--bg);border-color:var(--text-1)"' : '')}>${label}</a>`)}</div>
        <div class="notice">${icon.info()}<div>Corporations can’t give directly to federal candidates; their money reaches campaigns through PACs and outside super PAC spending. Some states fund candidates publicly. Real numbers come from FEC and state filings.</div></div>
        ${items.map(likedCard)}`
        : html`<div class="empty">${icon.heart()}<h3>No liked candidates yet</h3><p>Tap the heart on any candidate to keep them here.</p><a class="btn" href="#/">Browse the map</a></div>`}
    </div>`;
  },
};

// Close elections -----------------------------------------------------------------

const OFFICES = { all: 'All', senate: 'Senate', house: 'House', governor: 'Governor' };

export const close = {
  title: () => 'Close elections',
  render(ctx) {
    const office = OFFICES[ctx.query.office] ? ctx.query.office : 'all';
    const races = allRaces().filter((r) => (office === 'all' || r.office === office))
      .map((r) => ({ r, f: fc(r) }))
      .filter(({ f }) => !f.open && f.second && Math.abs(f.dr ?? f.margin) < 5)
      .sort((a, b) => Math.abs(a.f.dr ?? a.f.margin) - Math.abs(b.f.dr ?? b.f.margin));
    return html`<div class="wrap page stack">
      <div><div class="eyebrow">Close elections</div><h1>Races within 5 points</h1><p class="muted">Every Senate, House and governor race where the forecast margin is under 5 points, with the polling average day by day. Results will appear here on election night.</p></div>
      <div class="filters" role="group" aria-label="Office">${Object.entries(OFFICES).map(([k, l]) => html`<a class="chip" href="#/close?office=${k}" ${raw(k === office ? 'aria-current="page" style="background:var(--text-1);color:var(--bg);border-color:var(--text-1)"' : '')}>${l}</a>`)}<span class="small faint">${races.length} races</span></div>
      ${races.length ? html`<div class="grid grid-2">${races.map(({ r, f }) => {
        const h = hist(r);
        const y = h[h.length - 2]?.fc;
        const daily = y && f.dr != null && y.dr != null ? f.dr - y.dr : null;
        return html`<article class="card stack-sm">
          <div class="row between"><div><div class="eyebrow">${officeLabel(r)}</div><h3 style="margin:2px 0 0"><a href="#/race/${encodeURIComponent(r.id)}" style="text-decoration:none">${raceTitle(r)}</a></h3></div><div class="row">${dataChip(r)}${starBtn(r.id, { small: true })}</div></div>
          ${miniH2H(r)}
          <div class="row small muted"><span>Margin <b>${leadStr(f)}</b></span><span>·</span><span>Since yesterday ${daily == null ? '—' : arrow(daily)}</span><span>·</span><span>${f.poll ? `${f.poll.count} polls` : 'no polls'}</span></div>
          <div class="chart" data-close-chart="${r.id}" style="min-height:150px"></div>
          <div class="small faint">Results: not yet available. Polls close November 3.</div>
        </article>`;
      })}</div>` : html`<div class="empty">${icon.ballot()}<h3>No races this close</h3><p>Try another office.</p></div>`}
    </div>`;
  },
  mount(root) {
    root.querySelectorAll('[data-close-chart]').forEach((el) => {
      const race = getRace(el.dataset.closeChart);
      const f = fc(race);
      const colors = candColors(f.cands);
      const h = hist(race);
      const two = f.dr != null ? f.cands.filter((c) => c.party === 'D' || c.party === 'R').slice(0, 2) : [];
      const series = (two.length === 2 ? two : f.cands.slice(0, 2)).map((c) => ({
        name: lastName(c.name), color: colors[c.id],
        values: h.map((d) => ({ x: d.date, y: d.fc.cands.find((x) => x.id === c.id)?.share ?? null })),
      }));
      lineChart(el, { series, height: 150, yFormat: (v) => `${v.toFixed(0)}%`, tipFormat: (v) => `${v.toFixed(1)}%`, label: `${raceTitle(race)}: forecast vote share by day` });
    });
  },
};

// Profile -> Donations ----------------------------------------------------------------

export const donations = {
  title: () => 'Donations',
  rerenderOn: ['liked'],
  async render() {
    const cands = (await Promise.all(store.get().liked.map((id) => ensureCandidate(id)))).filter(Boolean);
    return html`<div class="wrap page stack" style="max-width:900px">
      <div><div class="eyebrow">Donations</div><h1>Donate to candidates you’ve liked</h1><p class="muted">Links go only to each campaign’s official donation page.</p></div>
      <div class="notice">${icon.info()}<div><b>How links are verified.</b> A donation link is shown only when it comes from the campaign’s own official website and points either to that website or to the payment processor the campaign itself uses (ActBlue for most Democrats, WinRed for most Republicans). Lookalike sites, scam PACs and third-party fundraisers are never linked.</div></div>
      ${cands.length ? cands.map((c) => {
        const race = getRace(c.raceId);
        const url = verifiedDonateUrl(c);
        return html`<div class="card row between">
          <div class="row"><div class="badge" style="background:${candColors(fc(race).cands)[c.id]}">${initials(c.name)}</div><div><b>${c.name}</b><div class="small faint">${PARTY_NAME[c.party] || c.party} · ${raceTitle(race)}</div></div></div>
          ${url ? html`<a class="btn btn-primary btn-sm" href="${url}" target="_blank" rel="noopener noreferrer">Donate on official site ${icon.external()}</a>`
            : html`<span class="small faint">${isDemo(c) ? 'Demo candidate: no donation link' : 'No verified official link yet'}</span>`}
        </div>`;
      }) : html`<div class="empty">${icon.heart()}<h3>No liked candidates yet</h3><p>Heart a candidate and their official donation link will appear here.</p></div>`}
    </div>`;
  },
};
