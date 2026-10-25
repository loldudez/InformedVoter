import { html, raw, fmtProb, fetchJSON, timeAgo, fmtDate } from '../util.js';
import { STATES, STATE_BY_ABBR, legislatureChambers } from '../data/states.js';
import { fc, allRaces, statewideRaces, chamberSummary, getMapIndex, realRaceCount } from '../data/world.js';
import { daysToElection } from '../model/forecast.js';
import { drawMap, ratingColor, ratingLegendHTML } from '../lib/map.js';
import { cssVar, sparkline } from '../lib/charts.js';
import { raceRow, lastName, demoChip } from '../components/race.js';

let statesGeo = null;
let mode = 'senate';

const signedSeats = (x) => `${x >= 0 ? '+' : '−'}${Math.abs(x).toFixed(1)}`;

// Chance of control, expected seats and the expected gain from today's totals,
// the 80% range, the betting market for comparison, and how the odds have moved.
function controlTile(label, key, o, unit, sum) {
  const pD = o.pD, pR = o.pR ?? 1 - o.pD, pN = Math.max(0, o.pNone ?? 0);
  const dFav = pD >= pR;
  const live = sum.source === 'refresh';
  const hist = (sum.history || []).map((h) => h[key]?.pD).filter((v) => v != null);
  const cur = o.current;
  const market = o.market;
  return html`<div class="card control">
    <div class="row between"><div class="eyebrow">${label} control</div>${live ? html`<span class="live-chip" title="Simulated 20,000 times at the last refresh, ${fmtDate(sum.updated)}">Live</span>` : realRaceCount ? '' : demoChip()}</div>
    <div class="bar" role="img" aria-label="${label}: Democrats ${fmtProb(pD)}, Republicans ${fmtProb(pR)}${pN >= 0.005 ? `, no majority ${fmtProb(pN)}` : ''}"><span style="flex:${pD}"></span>${pN >= 0.005 ? html`<span class="n" style="flex:${pN}"></span>` : ''}<span style="flex:${pR}"></span></div>
    <div class="odds"><span><b class="d-text">${fmtProb(pD)}</b>Democrats</span><span style="text-align:right"><b class="r-text">${fmtProb(pR)}</b>Republicans</span></div>
    ${o.meanD != null ? html`<p class="gain">Expected <b>${o.meanD.toFixed(1)} D</b> – <b>${o.meanR.toFixed(1)} R</b> ${unit}${cur ? html`; <b class="${o.gainD >= 0 ? 'd-text' : 'r-text'}">${o.gainD >= 0 ? `Democrats ${signedSeats(o.gainD)}` : `Republicans ${signedSeats(-o.gainD)}`}</b> from today’s ${cur.D}–${cur.R}` : ''}.</p>` : ''}
    ${o.range80D ? html`<p class="small faint" style="margin:4px 0 0">8 in 10 simulations: ${o.range80D[0]} to ${o.range80D[1]} Democratic ${unit}.${pN >= 0.005 ? ` ${fmtProb(pN)} chance neither party reaches a majority.` : ''}</p>` : ''}
    ${market ? html`<p class="market">Betting market: ${fmtProb(market.pD)} D on <a href="${market.url}" target="_blank" rel="noopener noreferrer">Polymarket</a> (a cross-check, not an input)</p>` : ''}
    ${hist.length >= 3 ? html`<div class="control-history"><span class="tiny faint">Democrats’ chance since ${fmtDate(sum.history[0].t)}</span>${raw(sparkline(hist.map((v) => v * 100), { width: 260, height: 34, color: cssVar('--dem'), label: `${label}: Democrats' chance of control over time` }))}</div>` : ''}
  </div>`;
}

const chamberUp = (c) => (c.up === 'all' ? 'all seats' : c.up === 'partial' ? 'some seats' : 'no election');

function tooltip(f) {
  const st = f.id;
  const s = STATE_BY_ABBR[st];
  const { senate, governor } = statewideRaces(st);
  const line = (label, race) => {
    if (!race) return html`<div class="t-row"><span>${label}</span><span class="faint">No race</span></div>`;
    const fc0 = fc(race);
    return html`<div class="t-row"><span>${label}</span><b>${lastName(fc0.lead.name)} (${fc0.lead.party}) ${fmtProb(fc0.pLead)}</b></div>`;
  };
  const nCd = getMapIndex()[st]?.cd || 0;
  const leg = legislatureChambers(st);
  return html`<div class="t-title">${s.name}</div>
    ${line('U.S. Senate', senate)}
    ${line('Governor', governor)}
    <div class="t-row"><span>U.S. House</span><b>${st === 'DC' ? 'Delegate' : `${nCd} district${nCd === 1 ? '' : 's'}`}</b></div>
    ${leg.map((c) => html`<div class="t-row"><span>${c.name}</span><b>${chamberUp(c)}</b></div>`)}
    <div class="tiny faint" style="margin-top:6px">Click to explore${(senate && senate.demo) || (governor && governor.demo) ? ' · demo forecasts' : ''}</div>`;
}

function fillFor(f) {
  const { senate, governor } = statewideRaces(f.id);
  const race = mode === 'senate' ? senate : mode === 'governor' ? governor : null;
  if (mode === 'all') return cssVar('--surface-3');
  return race ? ratingColor(fc(race)) : cssVar('--not-up');
}

export const home = {
  title: () => '2026 elections map',
  async render() {
    if (!statesGeo) statesGeo = await fetchJSON('data/maps/states.json');
    const sum = chamberSummary();
    const closest = allRaces().filter((r) => r.office !== 'house').map((r) => ({ r, f: fc(r) }))
      .sort((a, b) => Math.abs(a.f.pLead - 0.5) - Math.abs(b.f.pLead - 0.5)).slice(0, 8);
    const days = daysToElection();
    return html`<div class="wrap page stack-lg">
      <section class="hero">
        <span class="label-pill"><span class="dots">•••</span> 2026 midterm elections · ${days} days to go <span class="dots">•••</span></span>
        <h1>Every race on the <span class="grad-text">2026 ballot</span>, state by state.</h1>
        <p class="lede">Hover over a state to preview it, then click or tap it to explore its Senate, House, governor and state legislature races.</p>
      </section>
      <div class="control-tiles">
        ${controlTile('Senate', 'senate', sum.senate, 'seats', sum)}
        ${controlTile('House', 'house', sum.house, 'seats', sum)}
        ${controlTile('Governors', 'governor', sum.governor, 'governorships', sum)}
      </div>
      <section class="card map-card">
        <div class="section-head">
          <div><div class="eyebrow">Interactive map</div><h2 style="margin:4px 0 0">Choose a state</h2></div>
          <div class="row">
            <div class="seg" role="group" aria-label="Color the map by">
              <button type="button" data-mode="senate" aria-pressed="${String(mode === 'senate')}">Senate</button>
              <button type="button" data-mode="governor" aria-pressed="${String(mode === 'governor')}">Governor</button>
              <button type="button" data-mode="all" aria-pressed="${String(mode === 'all')}">All states</button>
            </div>
            <label class="sr-only" for="state-jump">Jump to a state</label>
            <select id="state-jump" class="input" style="width:auto;min-height:46px">
              <option value="">Jump to a state…</option>
              ${STATES.map((s) => html`<option value="${s.abbr}">${s.name}</option>`)}
            </select>
          </div>
        </div>
        <div id="us-map" class="map-spot"></div>
        <div id="us-legend"></div>
      </section>
      <section>
        <div class="section-head"><div><div class="eyebrow">Senate and governor</div><h2 style="margin:4px 0 0">Closest statewide races</h2></div><a class="btn btn-sm" href="#/close">All close elections</a></div>
        <div class="race-list">${closest.map(({ r }) => raceRow(r))}</div>
      </section>
    </div>`;
  },
  mount(root) {
    const el = root.querySelector('#us-map');
    const legend = root.querySelector('#us-legend');
    const go = (st) => { location.hash = `#/state/${st}`; };
    const setLegend = () => {
      legend.innerHTML = mode === 'all' ? '' : ratingLegendHTML(`<span><i style="background:${cssVar('--not-up')}"></i>No ${mode === 'senate' ? 'Senate' : 'governor'} race</span>`);
    };
    const map = drawMap(el, statesGeo, {
      fillFor, tooltipFor: tooltip, onSelect: (f) => go(f.id),
      ariaLabel: 'Map of U.S. states; select a state to see its races',
      regionLabel: (f) => STATE_BY_ABBR[f.id]?.name || f.id,
      maxHeight: 600,
    });
    setLegend();
    root.querySelectorAll('[data-mode]').forEach((b) => b.addEventListener('click', () => {
      mode = b.dataset.mode;
      root.querySelectorAll('[data-mode]').forEach((x) => x.setAttribute('aria-pressed', String(x === b)));
      map.refill();
      setLegend();
    }));
    root.querySelector('#state-jump').addEventListener('change', (e) => e.target.value && go(e.target.value));
  },
};
