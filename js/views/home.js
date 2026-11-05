import { html, raw, fmtProb, fetchJSON, timeAgo, fmtDate } from '../util.js';
import { STATES, STATE_BY_ABBR, legislatureChambers } from '../data/states.js';
import { fc, mainRaces, statewideRaces, houseRaces, chamberSummary, getMapIndex, realRaceCount, racesMeta, getRace, raceTitle,
  resultsIn, resultsTally, resultParty, resultMargin, resultWinners, mapView, setMapView, liveFc, controlData, stillCounting, afterElection } from '../data/world.js';
import { daysToElection } from '../model/forecast.js';
import { drawMap, ratingColor, ratingLegendHTML, resultFill, resultsLegendHTML } from '../lib/map.js';
import { cssVar, sparkline } from '../lib/charts.js';
import { raceRow, lastName, demoChip, resultMarginStr } from '../components/race.js';
import { icon } from '../icons.js';
import { store } from '../store.js';
import { QUESTIONS } from '../data/questions.js';

let statesGeo = null;
let districtsGeo = null; // every House district, loaded the first time the House view is picked
let mode = 'senate';     // which races color the map: 'senate', 'house' or 'governor'
const MODES = [['senate', 'Senate'], ['house', 'House'], ['governor', 'Governor']];
// A district of the national House map ("CA-13") and its race ("CA-H-13").
const districtRace = (f) => getRace(f.id.replace('-', '-H-'));

// Seats come whole: the simulations' averages are rounded so they add up to the
// whole chamber (largest remainder, with independents who caucus with neither party
// as a third share), and the gain is taken from the rounded count so the two agree.
function wholeSeats(o, cur) {
  const total = cur ? cur.D + cur.R + (cur.I || 0) + (cur.vacant || 0) : 0;
  if (!total) return { D: Math.round(o.meanD), R: Math.round(o.meanR), I: 0 };
  const exact = { D: o.meanD, R: o.meanR, I: Math.max(0, total - o.meanD - o.meanR) };
  const seats = { D: Math.floor(exact.D), R: Math.floor(exact.R), I: Math.floor(exact.I) };
  let left = total - seats.D - seats.R - seats.I;
  for (const k of ['D', 'R', 'I'].sort((a, b) => (exact[b] % 1) - (exact[a] % 1))) {
    if (left <= 0) break;
    seats[k]++;
    left--;
  }
  return seats;
}
const seatGain = (seats, cur) => {
  const g = seats.D - cur.D;
  if (g === 0) return html`<b>no net change</b>`;
  return g > 0 ? html`<b class="d-text">Democrats +${g}</b>` : html`<b class="r-text">Republicans +${-g}</b>`;
};

// Chance of control, expected seats and the expected gain from today's totals,
// the 80% range, the betting market for comparison, and how the odds have moved.
function controlTile(label, key, o, unit, sum) {
  const pD = o.pD, pR = o.pR ?? 1 - o.pD, pN = Math.max(0, o.pNone ?? 0);
  const live = sum.source === 'refresh';
  const hist = (sum.history || []).map((h) => h[key]?.pD).filter((v) => v != null);
  const cur = o.current;
  const seats = o.meanD != null ? wholeSeats(o, cur) : null;
  const market = o.market;
  return html`<div class="card control">
    <div class="row between"><div class="eyebrow">${label} control</div>${live ? html`<span class="live-chip" title="Simulated 20,000 times at the last refresh, ${fmtDate(sum.updated)}">Live</span>` : realRaceCount ? '' : demoChip()}</div>
    <div class="bar" role="img" aria-label="${label}: Democrats ${fmtProb(pD)}, Republicans ${fmtProb(pR)}${pN >= 0.005 ? `, no majority ${fmtProb(pN)}` : ''}"><span style="flex:${pD}"></span>${pN >= 0.005 ? html`<span class="n" style="flex:${pN}"></span>` : ''}<span style="flex:${pR}"></span></div>
    <div class="odds"><span><b class="d-text">${fmtProb(pD)}</b>Democrats</span><span style="text-align:right"><b class="r-text">${fmtProb(pR)}</b>Republicans</span></div>
    ${seats ? html`<p class="gain">Expected <b>${seats.D} D</b> – <b>${seats.R} R</b>${seats.I ? html` – <b>${seats.I}</b> independent` : ''} ${unit}${cur ? html`; ${seatGain(seats, cur)} from today’s ${cur.D}–${cur.R}` : ''}.</p>` : ''}
    ${o.range80D ? html`<p class="small faint" style="margin:4px 0 0">8 in 10 simulations: ${o.range80D[0]} to ${o.range80D[1]} Democratic ${unit}.${pN >= 0.005 ? ` ${fmtProb(pN)} chance neither party reaches a majority.` : ''}</p>` : ''}
    ${market ? html`<p class="market">Betting market: ${fmtProb(market.pD)} D on <a href="${market.url}" target="_blank" rel="noopener noreferrer">Polymarket</a> (a cross-check, not an input)</p>` : ''}
    ${hist.length >= 3 ? html`<div class="control-history"><span class="tiny faint">Democrats’ chance since ${fmtDate(sum.history[0].t)}</span>${raw(sparkline(hist.map((v) => v * 100), { width: 260, height: 34, color: cssVar('--dem'), label: `${label}: Democrats' chance of control over time` }))}</div>` : ''}
  </div>`;
}

// What it takes to control each chamber. The vice president, a Republican, breaks
// Senate ties; governorships have no majority to win, so only the count is shown.
const NEEDS = { senate: { D: 51, R: 50 }, house: { D: 218, R: 218 }, governor: null };

// Seats won so far: the called races by the winner's party plus the seats not up this
// year, with the majority line, what is still uncalled or in a runoff, and the seats that
// changed parties among the called races.
function resultsTile(label, key, unit) {
  const t = resultsTally(key);
  const needs = NEEDS[key];
  const open = t.uncalled.length + t.runoff.length;
  const total = t.seats.D + t.seats.R + t.seats.I + open;
  const to = (p) => t.flips.filter((r) => (resultParty(r) === p) || (p === 'I' && !['D', 'R'].includes(resultParty(r)))).length;
  const flipLine = t.flips.length
    ? html`Changed parties: ${[['D', 'Democrats'], ['R', 'Republicans'], ['I', 'independents or others']].filter(([p]) => to(p)).map(([p, who], i) => html`${i ? ', ' : ''}<b class="${p === 'D' ? 'd-text' : p === 'R' ? 'r-text' : ''}">${to(p)} to ${who}</b>`)}.`
    : html`No ${unit} have changed parties among the called races.`;
  let verdict;
  if (needs && t.seats.R >= needs.R) verdict = html`<b class="r-text">Republicans have won control</b> with ${t.seats.R} ${unit}${key === 'senate' ? ' (the vice president breaks a 50–50 tie)' : ''}.`;
  else if (needs && t.seats.D >= needs.D) verdict = html`<b class="d-text">Democrats have won control</b> with ${t.seats.D} ${unit}.`;
  else if (needs) verdict = html`No majority yet: Democrats need <b>${needs.D - t.seats.D}</b> more, Republicans <b>${needs.R - t.seats.R}</b>.`;
  else verdict = html`Before the election: ${t.current.D} D – ${t.current.R} R.`;
  const pending = [...t.runoff.map((r) => `${r.state}${r.office === 'house' ? `-${r.district === '00' ? 'AL' : parseInt(r.district, 10)}` : ''} (runoff)`), ...t.uncalled.map((r) => `${r.state}${r.office === 'house' ? `-${r.district === '00' ? 'AL' : parseInt(r.district, 10)}` : ''}`)];
  const updated = racesMeta()?.resultsUpdated || racesMeta()?.updated;
  // The projection (scripts/update_races.py, after_count): called seats as they are, the
  // races still out from their counts and final forecasts.
  const proj = open ? controlData()?.[key]?.projection : null;
  const won = needs && (t.seats.D >= needs.D || t.seats.R >= needs.R);
  const pSeats = proj ? wholeSeats(proj, { D: total, R: 0 }) : null;
  return html`<div class="card control results-tile">
    <div class="row between"><div class="eyebrow">${label} results</div><span class="live-chip" title="${updated ? `Read at the last refresh, ${timeAgo(updated)}` : 'Read from Wikipedia at each refresh'}${stillCounting() ? '; re-read every 10 minutes until every race is called' : ''}">Live</span></div>
    <div class="seat-bar">
      <div class="bar" role="img" aria-label="${label}: Democrats ${t.seats.D}${t.seats.I ? `, independents and others ${t.seats.I}` : ''}, not called ${open}, Republicans ${t.seats.R}"><span style="flex:${t.seats.D}"></span>${t.seats.I ? html`<span class="i" style="flex:${t.seats.I}"></span>` : ''}${open ? html`<span class="n" style="flex:${open}"></span>` : ''}<span style="flex:${t.seats.R}"></span></div>
      ${needs && total ? html`<i class="maj" title="Half the ${unit}: Democrats need ${needs.D} for control, Republicans ${needs.R}"></i>` : ''}
    </div>
    <div class="odds"><span><b class="d-text">${t.seats.D}</b>Democrats</span>${t.seats.I ? html`<span style="text-align:center"><b>${t.seats.I}</b>Ind. / other</span>` : ''}${open ? html`<span style="text-align:center"><b>${open}</b>Not called</span>` : ''}<span style="text-align:right"><b class="r-text">${t.seats.R}</b>Republicans</span></div>
    <p class="gain">${verdict}</p>
    <p class="small faint" style="margin:4px 0 0">${t.called} of ${t.up} races called${t.hold.D || t.hold.R ? `, plus ${t.hold.D} D and ${t.hold.R} R ${unit} not up this year` : ''}${key === 'senate' ? '; Democrats include the independents who caucus with them' : ''}. ${flipLine}</p>
    ${pSeats ? html`<p class="small" style="margin:8px 0 0">Projected final: <b class="d-text">${pSeats.D} D</b> – <b class="r-text">${pSeats.R} R</b>${pSeats.I ? html` – <b>${pSeats.I}</b> other` : ''} (8 in 10: ${proj.range80D[0]} to ${proj.range80D[1]} Democratic ${unit})${needs && !won ? html`; chance of a majority: <b class="d-text">D ${fmtProb(proj.pD)}</b>, <b class="r-text">R ${fmtProb(proj.pR)}</b>` : ''}.</p>
    <p class="tiny faint" style="margin:2px 0 0">Each race still out counts by its projection from the count so far, or its final forecast where no count is posted.</p>` : ''}
    ${pending.length ? html`<p class="small faint" style="margin:4px 0 0">${t.runoff.length && !t.uncalled.length ? 'Runoff' : 'Not called yet'}: ${pending.slice(0, 12).join(', ')}${pending.length > 12 ? ` and ${pending.length - 12} more` : ''}.</p>` : ''}
  </div>`;
}

// Races with a count and no call yet, closest projection first.
function stillCountingList() {
  return mainRaces().map((r) => ({ r, lv: liveFc(r) })).filter((x) => x.lv)
    .sort((a, b) => a.lv.pLead - b.lv.pLead || a.r.id.localeCompare(b.r.id)).map((x) => x.r);
}

const chamberUp = (c) => (c.up === 'all' ? 'all seats' : c.up === 'partial' ? 'some seats' : 'no election');

// "Get ready to vote", first thing on the page (owner's request, Nov. 4, as on the
// France home page): one button that opens two choices, the visitor's elections or the
// questionnaire the candidate matches are built on (how long it takes, that it can be
// left and resumed, and that matches firm up as more is answered). Stays open across the
// redraws while votes are counted.
let readyOpen = false;
function readyToVote() {
  const { answers, address } = store.get();
  const st = address?.state ? STATE_BY_ABBR[address.state] : null;
  const touched = Object.keys(answers).length;
  const total = QUESTIONS.length;
  const mine = st
    ? (afterElection() ? `Your races in ${st.name} and their 2026 results, the races you follow and your reminders.` : `The races on your ballot in ${st.name}, the races you follow and your reminders.`)
    : 'The races on your ballot, from your address (it stays in this browser).';
  const quiz = touched >= total
    ? `You’ve answered all ${total} questions. Review them, then see which candidates match you in each race on your ballot.`
    : `${touched > 0 ? `You’ve answered ${touched} of ${total} questions; this picks up where you left off. ` : 'Answer the My views questions, then compare your answers with the candidates’ sourced positions. '}Takes less than 20 minutes. You can stop at any time and come back later, but your matches may not be fully accurate until you’ve answered every question.`;
  return html`<section class="fr-start us-start">
    <button type="button" class="btn btn-primary fr-start-btn" aria-expanded="${String(readyOpen)}" aria-controls="us-start-choices">${icon.ballot()} Get ready to vote ${icon.chevronDown()}</button>
    <div class="fr-start-choices" id="us-start-choices" ${raw(readyOpen ? '' : 'hidden')}>
      <a class="card fr-choice" href="#/elections">${icon.calendar()}<span><b>Click here to view my elections</b><span class="small muted">${mine}</span></span>${icon.chevronRight()}</a>
      <a class="card fr-choice" href="#/views">${icon.user()}<span><b>Click here to help find the best candidate for me</b><span class="small muted">${quiz}</span></span>${icon.chevronRight()}</a>
    </div>
  </section>`;
}

// A race in the results map's tooltip: the winner and margin, a runoff, the leader of a
// count still going, or nothing yet.
function tipResult(race) {
  const res = race.result;
  if (!res) return html`<span class="faint">No result yet</span>`;
  const m = resultMarginStr(race);
  if (res.status === 'won') {
    const w = resultWinners(race);
    return html`<b>${icon.check()} ${w.map((c) => `${lastName(c.name)} (${c.party})`).join(', ')}${m ? `, ${m}` : ''}${res.flip ? ' · flip' : ''}</b>`;
  }
  if (res.status === 'runoff') return html`<b>Runoff</b>`;
  const lead = resultMargin(race);
  const lv = liveFc(race);
  return html`<b>${lead ? `${lastName(lead.a.name)} leads, ${m}` : 'Counting'}${lv ? ` · ${lastName(lv.lead.name)} ${fmtProb(lv.pLead)} to win` : ''}</b>`;
}

function districtTip(f) {
  const race = districtRace(f);
  if (!race) return html`<div class="t-title">${f.properties.n || f.id}</div><div class="t-row"><span class="faint">No race found</span></div>`;
  const results = mapView() === 'results';
  const f0 = fc(race);
  const row = results ? tipResult(race)
    : f0.open ? html`<b>${f0.rating}</b>` : html`<b>${lastName(f0.lead.name)} (${f0.lead.party}) ${fmtProb(f0.pLead)}</b>`;
  return html`<div class="t-title">${raceTitle(race)}</div>
    <div class="t-row"><span>${results ? 'Result' : 'Forecast'}</span>${row}</div>
    <div class="tiny faint" style="margin-top:6px">Click to see the race${results ? ' · unofficial counts' : race.demo ? ' · demo forecast' : ''}</div>`;
}

function houseTally(st) {
  const rs = houseRaces(st);
  const n = { D: 0, R: 0, other: 0, open: 0 };
  for (const r of rs) {
    const p = r.result?.status === 'won' ? resultParty(r) : null;
    if (p === 'D' || p === 'R') n[p]++;
    else if (p) n.other++;
    else n.open++;
  }
  return [n.R && `${n.R} R`, n.D && `${n.D} D`, n.other && `${n.other} other`, n.open && `${n.open} not called`].filter(Boolean).join(', ');
}

function tooltip(f) {
  const st = f.id;
  const s = STATE_BY_ABBR[st];
  const { senate, governor } = statewideRaces(st);
  const results = mapView() === 'results';
  const line = (label, race) => {
    if (!race) return html`<div class="t-row"><span>${label}</span><span class="faint">No race</span></div>`;
    if (results) return html`<div class="t-row"><span>${label}</span>${tipResult(race)}</div>`;
    const fc0 = fc(race);
    return html`<div class="t-row"><span>${label}</span><b>${lastName(fc0.lead.name)} (${fc0.lead.party}) ${fmtProb(fc0.pLead)}</b></div>`;
  };
  const nCd = getMapIndex()[st]?.cd || 0;
  const leg = legislatureChambers(st);
  return html`<div class="t-title">${s.name}</div>
    ${line('U.S. Senate', senate)}
    ${line('Governor', governor)}
    <div class="t-row"><span>U.S. House</span><b>${results ? houseTally(st) : st === 'DC' ? 'Delegate' : `${nCd} district${nCd === 1 ? '' : 's'}`}</b></div>
    ${results ? '' : leg.map((c) => html`<div class="t-row"><span>${c.name}</span><b>${chamberUp(c)}</b></div>`)}
    <div class="tiny faint" style="margin-top:6px">Click to explore${results ? ' · unofficial counts' : (senate && senate.demo) || (governor && governor.demo) ? ' · demo forecasts' : ''}</div>`;
}

function fillFor(f, pattern) {
  let race;
  if (mode === 'house') race = districtRace(f);
  else {
    const { senate, governor } = statewideRaces(f.id);
    race = mode === 'senate' ? senate : governor;
  }
  if (!race) return cssVar('--not-up');
  if (mapView() === 'results') return resultFill(race.result, resultParty(race), pattern) || cssVar('--neutral-mid');
  return ratingColor(fc(race));
}

// Races decided by the fewest points, and the seats that changed parties.
const byMargin = (rs) => rs.map((r) => ({ r, m: resultMargin(r) })).filter((x) => x.m).sort((a, b) => a.m.pts - b.m.pts);
const OFFICE_ORDER = { senate: 0, governor: 1, house: 2 };

export const home = {
  live: true, // redrawn when new counts arrive (main.js)
  title: () => (resultsIn() ? '2026 election results map' : '2026 elections map'),
  async render() {
    if (!statesGeo) statesGeo = await fetchJSON('data/maps/states.json');
    const results = resultsIn();
    const sum = chamberSummary();
    const statewide = mainRaces().filter((r) => r.office !== 'house');
    const closest = results
      ? [...statewide.filter((r) => r.result && r.result.status !== 'won'), ...byMargin(statewide.filter((r) => r.result?.status === 'won')).map((x) => x.r)].slice(0, 8)
      : statewide.map((r) => ({ r, f: fc(r) })).sort((a, b) => Math.abs(a.f.pLead - 0.5) - Math.abs(b.f.pLead - 0.5)).slice(0, 8).map((x) => x.r);
    const flips = results ? mainRaces().filter((r) => r.result?.flip).sort((a, b) => OFFICE_ORDER[a.office] - OFFICE_ORDER[b.office] || a.id.localeCompare(b.id)) : [];
    const days = daysToElection();
    const updated = racesMeta()?.resultsUpdated || racesMeta()?.updated;
    const counting = results ? stillCountingList() : [];
    const view = mapView();
    return html`<div class="wrap page stack-lg">
      ${readyToVote()}
      <section class="hero">
        ${results
          ? html`<span class="label-pill"><span class="dots">•••</span> 2026 midterm results${updated ? ` · updated ${timeAgo(updated)}` : ''} <span class="dots">•••</span></span>
        <h1>The <span class="grad-text">2026 results</span>, state by state.</h1>
        <p class="lede">A race counts as called once Wikipedia’s national results table marks its winner; vote counts are unofficial until each state certifies them${stillCounting() && racesMeta()?.resultsUpdated ? ', and are re-read every 10 minutes until every race is called' : ', and refresh every 8 hours'}. Hover over a state or House district to preview it, then click or tap it to see its races, the final forecast beside the result.</p>`
          : html`<span class="label-pill"><span class="dots">•••</span> 2026 midterm elections · ${days} days to go <span class="dots">•••</span></span>
        <h1>Every race on the <span class="grad-text">2026 ballot</span>, state by state.</h1>
        <p class="lede">Hover over a state or House district to preview it, then click or tap it to explore its Senate, House, governor and state legislature races.</p>`}
      </section>
      <div class="control-tiles">
        ${results ? resultsTile('Senate', 'senate', 'seats') : controlTile('Senate', 'senate', sum.senate, 'seats', sum)}
        ${results ? resultsTile('House', 'house', 'seats') : controlTile('House', 'house', sum.house, 'seats', sum)}
        ${results ? resultsTile('Governors', 'governor', 'governorships') : controlTile('Governors', 'governor', sum.governor, 'governorships', sum)}
      </div>
      <section class="card map-card">
        <div class="section-head">
          <div><div class="eyebrow">${view === 'results' ? 'Results map' : results ? 'Final forecast map' : 'Interactive map'}</div><h2 style="margin:4px 0 0" id="map-head">${mode === 'house' ? 'Choose a district' : 'Choose a state'}</h2></div>
          <div class="row">
            ${results ? html`<div class="seg" role="group" aria-label="Show on the map">
              <button type="button" data-view="results" aria-pressed="${String(view === 'results')}">Results</button>
              <button type="button" data-view="forecast" aria-pressed="${String(view === 'forecast')}">Final forecast</button>
            </div>` : ''}
            <div class="seg" role="group" aria-label="Races on the map">
              ${MODES.map(([k, l]) => html`<button type="button" data-mode="${k}" aria-pressed="${String(mode === k)}">${l}</button>`)}
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
      ${counting.length ? html`<section>
        <div class="section-head"><div><div class="eyebrow">Not called yet</div><h2 style="margin:4px 0 0">Still being counted</h2></div><span class="small faint">${counting.length} race${counting.length === 1 ? '' : 's'} with a count, closest first</span></div>
        <p class="small muted" style="margin:0 0 12px">Each projection blends the count so far with the final forecast. It is not a call: a race is called only once Wikipedia’s national results table marks its winner.</p>
        <div class="race-list">${counting.slice(0, 12).map((r) => raceRow(r))}</div>
      </section>` : ''}
      <section>
        <div class="section-head"><div><div class="eyebrow">Senate and governor</div><h2 style="margin:4px 0 0">${results ? 'Closest statewide results' : 'Closest statewide races'}</h2></div><a class="btn btn-sm" href="#/close">All close elections</a></div>
        <div class="race-list">${closest.map((r) => raceRow(r))}</div>
      </section>
      ${flips.length ? html`<section>
        <div class="section-head"><div><div class="eyebrow">Called races</div><h2 style="margin:4px 0 0">Seats that changed parties</h2></div><span class="small faint">${flips.length} so far</span></div>
        <div class="race-list">${flips.map((r) => raceRow(r))}</div>
      </section>` : ''}
    </div>`;
  },
  async mount(root) {
    const start = root.querySelector('.us-start .fr-start-btn');
    start?.addEventListener('click', () => {
      const panel = root.querySelector('#us-start-choices');
      panel.hidden = !panel.hidden;
      readyOpen = !panel.hidden;
      start.setAttribute('aria-expanded', String(readyOpen));
    });
    const el = root.querySelector('#us-map');
    const legend = root.querySelector('#us-legend');
    const go = (st) => { location.hash = `#/state/${st}`; };
    const setLegend = () => {
      const none = mode === 'house' ? '' : `<span><i style="background:${cssVar('--not-up')}"></i>No ${mode === 'senate' ? 'Senate' : 'governor'} race</span>`;
      if (mapView() === 'results') {
        const rs = mainRaces().filter((r) => r.office === mode);
        const other = rs.some((r) => r.result?.status === 'won' && !['D', 'R'].includes(resultParty(r)));
        legend.innerHTML = resultsLegendHTML({
          other, flips: rs.some((r) => r.result?.flip), counting: rs.some((r) => r.result?.status === 'counting'),
          runoff: rs.some((r) => r.result?.status === 'runoff'), extra: none,
        });
      } else legend.innerHTML = ratingLegendHTML(none);
    };
    let map = null;
    let drawn = null; // which geometry is on screen: 'states' or 'districts'
    const draw = async () => {
      const want = mode === 'house' ? 'districts' : 'states';
      if (drawn === want) { map.refill(); return; }
      if (want === 'districts' && !districtsGeo) {
        el.setAttribute('aria-busy', 'true');
        districtsGeo = await fetchJSON('data/maps/cd-us.json');
        el.removeAttribute('aria-busy');
        if (mode !== 'house') return; // the visitor switched back while it loaded
      }
      drawn = want;
      const results = mapView() === 'results';
      map = want === 'districts'
        ? drawMap(el, districtsGeo, {
          fillFor, tooltipFor: districtTip, onSelect: (f) => { location.hash = `#/race/${f.id.replace('-', '-H-')}`; },
          borders: statesGeo, zoomable: true,
          ariaLabel: results ? 'Map of the 435 House districts and D.C., colored by the 2026 results; select a district to see its race' : 'Map of the 435 House districts and D.C.; select a district to see its race',
          regionLabel: (f) => { const r = districtRace(f); return r ? raceTitle(r) : f.id; },
          maxHeight: 600,
        })
        : drawMap(el, statesGeo, {
          fillFor, tooltipFor: tooltip, onSelect: (f) => go(f.id),
          ariaLabel: results ? 'Map of U.S. states colored by the 2026 results; select a state to see its races' : 'Map of U.S. states; select a state to see its races',
          regionLabel: (f) => STATE_BY_ABBR[f.id]?.name || f.id,
          maxHeight: 600,
        });
    };
    await draw();
    setLegend();
    root.querySelectorAll('[data-mode]').forEach((b) => b.addEventListener('click', async () => {
      mode = b.dataset.mode;
      root.querySelectorAll('[data-mode]').forEach((x) => x.setAttribute('aria-pressed', String(x === b)));
      const head = root.querySelector('#map-head');
      if (head) head.textContent = mode === 'house' ? 'Choose a district' : 'Choose a state';
      await draw();
      setLegend();
    }));
    root.querySelectorAll('[data-view]').forEach((b) => b.addEventListener('click', () => {
      setMapView(b.dataset.view);
      root.querySelectorAll('[data-view]').forEach((x) => x.setAttribute('aria-pressed', String(x === b)));
      const eb = root.querySelector('.map-card .eyebrow');
      if (eb) eb.textContent = mapView() === 'results' ? 'Results map' : 'Final forecast map';
      map?.refill();
      setLegend();
    }));
    root.querySelector('#state-jump').addEventListener('change', (e) => e.target.value && go(e.target.value));
  },
};
