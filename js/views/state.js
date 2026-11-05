import { html, raw, fmtProb, fmtPct, fmtDR } from '../util.js';
import { icon } from '../icons.js';
import { STATE_BY_ABBR, legislatureChambers, ELECTION_DATE_LABEL } from '../data/states.js';
import { fc, statewideRaces, houseRaces, officeRaces, loadLayer, legislativeRaces, mapView, setMapView, resultsIn, resultParty, resultWinners, resultMargin } from '../data/world.js';
import { cleanDistrictName } from '../data/demo.js';
import { drawMap, ratingColor, ratingLegendHTML, resultFill, resultsLegendHTML } from '../lib/map.js';
import { cssVar } from '../lib/charts.js';
import { raceFull, compactRace, raceRow, mountRaceTabs, leadStr, lastName, photoCredits, resultMarginStr } from '../components/race.js';
import { howToVote, voteCardLabel } from '../components/vote.js';

const ODD_YEAR_STATES = new Set(['LA', 'MS', 'NJ', 'VA']);

function chips(st) {
  const s = STATE_BY_ABBR[st];
  const { senate, governor } = statewideRaces(st);
  const out = [];
  if (senate) out.push(html`<span class="chip">${icon.check()} U.S. Senate${senate.special ? ' (special)' : ''}</span>`);
  if (governor) out.push(html`<span class="chip">${icon.check()} Governor</span>`);
  out.push(html`<span class="chip">${icon.check()} U.S. House</span>`);
  for (const r of officeRaces(st)) out.push(html`<span class="chip">${icon.check()} ${r.officeName}${r.special ? ' (special)' : ''}</span>`);
  for (const c of legislatureChambers(st)) if (c.up !== 'none') out.push(html`<span class="chip">${icon.check()} ${c.name}${c.up === 'partial' ? ' (some seats)' : ''}</span>`);
  return out;
}

// The statewide offices below governor, each opening its own race page.
function officesSection(st) {
  const rs = officeRaces(st);
  if (!rs.length) return '';
  return html`<section class="card stack-sm" style="margin-bottom:20px">
    <div class="section-head"><div><div class="eyebrow">Statewide offices</div><h2 style="margin:4px 0 0">Below the governor</h2></div><span class="small faint">${rs.length} race${rs.length === 1 ? '' : 's'} · click one for the candidates, their positions and the results</span></div>
    <div class="race-list">${rs.map((r) => raceRow(r))}</div>
  </section>`;
}

// A House district on the results map: winner and margin, runoff, leader, or nothing yet.
function districtResult(r) {
  const res = r.result;
  if (!res) return { text: 'No result yet', party: null, won: false };
  if (res.status === 'won') {
    const w = resultWinners(r)[0];
    return { text: `${w ? lastName(w.name) : ''} ${resultMarginStr(r) || ''}${res.flip ? ' · flip' : ''}`.trim(), party: w?.party, won: true };
  }
  if (res.status === 'runoff') return { text: 'Runoff', party: null, won: false };
  const m = resultMargin(r);
  return { text: m ? `${lastName(m.a.name)} leads, ${resultMarginStr(r)}` : 'Counting', party: m?.a.party || null, won: false };
}

function parseMode(st, q) {
  const s = STATE_BY_ABBR[st];
  const level = q.level === 'state' ? 'state' : 'federal';
  let chamber = q.chamber;
  if (level === 'federal') chamber = chamber === 'house' || !s.senate ? 'house' : 'senate';
  else if (s.unicameral) chamber = 'leg';
  else chamber = chamber === 'house' ? 'house' : 'senate';
  if (st === 'DC') chamber = 'house';
  return { level, chamber };
}

const href = (st, level, chamber) => `#/state/${st}?level=${level}&chamber=${chamber}`;

function toggles(st, { level, chamber }) {
  const s = STATE_BY_ABBR[st];
  const cur = (on) => (on ? raw('aria-current="page"') : '');
  const second = level === 'federal'
    ? html`<a href="${href(st, 'federal', 'senate')}" ${cur(chamber === 'senate')}>Senators</a><a href="${href(st, 'federal', 'house')}" ${cur(chamber === 'house')}>House Representatives</a>`
    : s.unicameral
      ? html`<a href="${href(st, 'state', 'leg')}" aria-current="page">Legislature (single chamber)</a>`
      : html`<a href="${href(st, 'state', 'senate')}" ${cur(chamber === 'senate')}>Senators</a><a href="${href(st, 'state', 'house')}" ${cur(chamber === 'house')}>House Representatives</a>`;
  return html`<div class="toggles">
    <nav class="seg big" aria-label="Election level">
      <a href="${href(st, 'federal', 'senate')}" ${cur(level === 'federal')}>Federal elections</a>
      <a href="${href(st, 'state', s.unicameral ? 'leg' : 'senate')}" ${cur(level === 'state')}>State elections</a>
    </nav>
    ${st === 'DC' ? '' : html`<nav class="seg" aria-label="Chamber">${second}</nav>`}
  </div>`;
}

function emptyState(title, body) {
  return html`<div class="empty">${icon.ballot()}<h3>${title}</h3><p style="margin:0">${body}</p></div>`;
}

export const stateView = {
  live: true, // redrawn when new counts arrive (main.js)
  title: (ctx) => STATE_BY_ABBR[ctx.params[0]]?.name || 'State',
  async render(ctx) {
    const st = ctx.params[0];
    const s = STATE_BY_ABBR[st];
    if (!s) return html`<div class="wrap page">${emptyState('State not found', 'Pick a state from the map on the homepage.')}</div>`;
    const m = parseMode(st, ctx.query);
    const { senate, governor } = statewideRaces(st);

    let body;
    const results = m.level === 'federal' && m.chamber === 'house' && resultsIn();
    if (m.level === 'federal' && m.chamber === 'senate') {
      body = senate
        ? html`<section class="card" style="padding:clamp(16px,3vw,28px)">${raceFull(senate, { tag: 'h2', credits: false })}</section>`
        : emptyState(`No U.S. Senate election in ${s.name} in 2026`, `Neither of ${s.name}’s Senate seats is on the ballot this year. They are next up in 2028 and 2030.`);
    } else if (m.level === 'state' && st === 'DC') {
      body = html`${officesSection(st)}${emptyState('No state legislature', 'The District of Columbia has a city council instead of a state legislature, so there are no state legislative races here.')}`;
    } else {
      const chamber = m.level === 'federal' ? null : legislatureChambers(st).find((c) => c.key === m.chamber);
      if (chamber && chamber.up === 'none') {
        body = emptyState(`No ${chamber.name} elections in ${s.name} in 2026`, ODD_YEAR_STATES.has(st) ? `${s.name} elects its legislature in odd-numbered years; the next election is in 2027.` : `${s.name}’s ${chamber.name} has four-year terms and is next elected in 2028.`);
      } else {
        const label = m.level === 'federal' ? (st === 'DC' ? 'Delegate to the U.S. House' : 'U.S. House districts') : `${chamber.name} districts`;
        const view = mapView();
        body = html`<section class="stack">
          <div class="card map-card">
            <div class="section-head">
              <div><div class="eyebrow">${m.level === 'federal' ? 'Federal' : 'State'} · 2026 district ${results ? (view === 'results' ? 'results' : 'final forecast') : 'map'}</div><h2 style="margin:4px 0 0">${label}</h2></div>
              <div class="stack-sm" style="align-items:flex-end">
                ${results ? html`<div class="seg" role="group" aria-label="Show on the map">
                  <button type="button" data-view="results" aria-pressed="${String(view === 'results')}">Results</button>
                  <button type="button" data-view="forecast" aria-pressed="${String(view === 'forecast')}">Final forecast</button>
                </div>` : ''}
                <p class="small muted" style="margin:0">${chamber && chamber.up === 'partial' ? 'Staggered terms: only some districts elect in 2026; the rest are grayed out. ' : ''}Click a district to see its race. Ctrl + scroll or the buttons to zoom.</p>
              </div>
            </div>
            <div id="district-map"><div class="row muted"><span class="spinner"></span> Loading district map…</div></div>
            <div id="district-legend"></div>
          </div>
          <div id="district-race"></div>
          <div class="card"><div class="section-head"><h3 style="margin:0">All districts</h3><span class="small faint" id="district-count"></span></div><div class="district-grid" id="district-list"></div></div>
        </section>`;
      }
    }

    // One credits list for the governor's two candidates and, on the Senate view, the
    // Senate race's; a district's race brings its own when it opens.
    const credits = photoCredits([
      ...(governor && !fc(governor).open ? fc(governor).cands.slice(0, 2) : []),
      ...(senate && m.level === 'federal' && m.chamber === 'senate' ? fc(senate).cands : []),
    ]);
    return html`<div class="wrap page">
      <nav class="crumbs" aria-label="Breadcrumb"><a href="#/">Home</a><span>/</span><span>${s.name}</span></nav>
      <div class="state-head">
        <div><div class="eyebrow">${ELECTION_DATE_LABEL}</div><h1 style="margin:6px 0 10px">${s.name}</h1><div class="ballot-chips">${chips(st)}</div></div>
        <a class="btn" href="#how-to-vote" data-scroll="how-to-vote">${icon.ballot()} ${voteCardLabel(st)}</a>
      </div>
      ${toggles(st, m)}
      ${governor ? html`<div style="margin-bottom:20px">${compactRace(governor, { label: 'Statewide · Governor' })}</div>` : ''}
      ${m.level === 'state' && st !== 'DC' ? officesSection(st) : ''}
      ${body}
      <div id="how-to-vote" style="margin-top:28px">${howToVote(st)}</div>
      ${credits ? html`<div style="margin-top:20px">${credits}</div>` : ''}
    </div>`;
  },

  async mount(root, ctx) {
    const st = ctx.params[0];
    if (!STATE_BY_ABBR[st]) return;
    mountRaceTabs(root);
    root.querySelector('[data-scroll]')?.addEventListener('click', (e) => {
      e.preventDefault();
      root.querySelector('#how-to-vote').scrollIntoView({ behavior: 'smooth' });
    });
    const mapEl = root.querySelector('#district-map');
    if (!mapEl) return;
    const m = parseMode(st, ctx.query);

    let features, races;
    if (m.level === 'federal') {
      features = await loadLayer(st, 'cd');
      races = new Map(houseRaces(st).map((r) => [r.district, r]));
    } else {
      const data = await legislativeRaces(st, m.chamber);
      features = data.features;
      races = data.races;
    }
    if (!root.isConnected) return;

    const raceFor = (f) => races.get(f.id) || null;
    const panel = root.querySelector('#district-race');
    const list = root.querySelector('#district-list');
    const up = [...races.values()].filter(Boolean);
    root.querySelector('#district-count').textContent = `${up.length} of ${features.features.length} districts elect in 2026`;

    // Real state legislative races have no forecast: color them by how the district
    // voted for president in 2024 where the page gives it, else by the party holding the seat.
    const field = up.filter((r) => r.format === 'field');
    const byLean = field.length > 0 && field.filter((r) => r.pres24 != null).length >= 0.8 * field.length;
    const mid = cssVar('--neutral-mid');
    const pole = (p) => (p === 'D' ? cssVar('--dem') : p === 'R' ? cssVar('--rep') : mid);
    const fieldColor = (r) => {
      if (byLean) {
        if (r.pres24 == null) return mid;
        const a = Math.abs(r.pres24);
        return d3.interpolateLab(mid, pole(r.pres24 > 0 ? 'D' : 'R'))(a >= 15 ? 1 : a >= 7 ? 0.68 : a >= 3 ? 0.4 : 0);
      }
      return r.held === 'D' || r.held === 'R' ? d3.interpolateLab(mid, pole(r.held))(0.68) : mid;
    };
    // House results (federal level, after Election Day): see resultFill in lib/map.js.
    const withResults = m.level === 'federal' && resultsIn();
    const showResults = () => withResults && mapView() === 'results';
    const fillFor = (r, pattern) => {
      if (!r) return cssVar('--not-up');
      if (r.format === 'field') return fieldColor(r);
      if (showResults()) return resultFill(r.result, resultParty(r), pattern) || mid;
      return ratingColor(fc(r));
    };

    const few = features.features.length <= 40;
    const map = drawMap(mapEl, features, {
      fillFor: (f, pattern) => fillFor(raceFor(f), pattern),
      tooltipFor: (f) => {
        const r = raceFor(f);
        const name = r ? r.districtName : f.properties.n;
        if (!r) return html`<div class="t-title">${name}</div><div class="faint small">No election in 2026</div>`;
        const ff = fc(r);
        if (showResults()) {
          const res = r.result;
          const rows = (res?.rows || []).filter((x) => !x.other).slice().sort((a, b) => (b.final ?? b.pct ?? 0) - (a.final ?? a.pct ?? 0)).slice(0, 3);
          const won = new Set(res?.winners || []);
          return html`<div class="t-title">${name}</div>
            ${rows.length ? rows.map((x) => html`<div class="t-row"><span>${won.has(x.id) ? html`${icon.check()} ` : ''}${x.name} (${x.party || '?'})</span><b>${(x.final ?? x.pct) != null ? fmtPct(x.final ?? x.pct) : '—'}</b></div>`) : html`<div class="faint small">No vote count yet</div>`}
            <div class="t-row"><span>Result</span><b>${!res ? 'Not in yet' : res.status === 'won' ? `Called${res.flip ? ' · flip' : ''}` : res.status === 'runoff' ? 'Runoff' : 'Not called yet'}</b></div>
            <div class="t-row"><span>Final forecast</span><b>${ff.rating}</b></div>`;
        }
        if (ff.kind === 'field') {
          const incs = (r.incumbents || []).filter((i) => i.name);
          return html`<div class="t-title">${name}</div>
            ${r.pres24 != null ? html`<div class="t-row"><span>2024 president</span><b>${fmtDR(r.pres24)}</b></div>` : ''}
            ${incs.length ? html`<div class="t-row"><span>Held by</span><b>${incs.map((i) => `${lastName(i.name)} (${i.party || '?'})`).join(', ')}</b></div>` : ''}
            <div class="t-row"><span>Candidates</span><b>${ff.cands.length || 'not listed yet'}</b></div>
            ${r.consensus ? html`<div class="t-row"><span>Forecasters</span><b>${ff.rating}</b></div>` : ''}`;
        }
        if (ff.open) return html`<div class="t-title">${name}</div><div class="t-row"><span>Open primary</span><b>${ff.cands.length} candidates</b></div><div class="t-row"><span>Forecasters</span><b>${ff.rating}</b></div>`;
        return html`<div class="t-title">${name}</div>${ff.cands.slice(0, 2).map((c) => html`<div class="t-row"><span>${c.name} (${c.party})</span><b>${fmtPct(c.share)}</b></div>`)}<div class="t-row"><span>${ff.rating}</span><b>${fmtProb(ff.pLead)}</b></div>`;
      },
      onSelect: (f) => select(f.id, true),
      labelFor: few ? (f) => String(parseInt(f.id, 10) || f.id) : null,
      regionLabel: (f) => {
        const r = raceFor(f);
        if (r && showResults() && r.format !== 'field') return `${r.districtName}: ${districtResult(r).text}`;
        return r ? `${r.districtName}: ${r.format === 'field' ? leadStr(fc(r)) : fc(r).rating}` : `${f.properties.n}: no election in 2026`;
      },
      zoomable: true,
      ariaLabel: 'District map',
    });
    const notUp = `<span><i style="background:${cssVar('--not-up')}"></i>No election in 2026</span>`;
    const sw = (c, label) => `<span><i style="background:${c}"></i>${label}</span>`;
    const resultsLegend = () => resultsLegendHTML({
      other: up.some((r) => r.result?.status === 'won' && !['D', 'R'].includes(resultParty(r))),
      flips: up.some((r) => r.result?.flip), counting: up.some((r) => r.result?.status === 'counting'),
      runoff: up.some((r) => r.result?.status === 'runoff'), extra: notUp,
    });
    root.querySelector('#district-legend').innerHTML = !field.length
      ? (showResults() ? resultsLegend() : ratingLegendHTML(notUp))
      : byLean
        ? `<div class="map-legend"><span class="faint">2024 president:</span>${[['R', 1, 'R+15 or more'], ['R', 0.68, 'R+7 to 15'], ['R', 0.4, 'R+3 to 7'], [null, 0, 'Within 3'], ['D', 0.4, 'D+3 to 7'], ['D', 0.68, 'D+7 to 15'], ['D', 1, 'D+15 or more']]
          .map(([p, t, label]) => sw(d3.interpolateLab(mid, pole(p))(t), label)).join('')}${notUp}</div>`
        : `<div class="map-legend"><span class="faint">Seat now held by:</span>${sw(d3.interpolateLab(mid, pole('R'))(0.68), 'Republican')}${sw(d3.interpolateLab(mid, pole('D'))(0.68), 'Democrat')}${sw(mid, 'Other, split, vacant or not listed')}${notUp}</div>`;

    const fillList = () => {
      list.innerHTML = features.features.map((f) => {
        const r = raceFor(f);
        const label = r ? r.districtName : cleanDistrictName(f.properties.n);
        if (!r) return String(html`<span class="district-btn not-up"><span class="dn">${label}</span><span class="tiny faint">No 2026 race</span></span>`);
        const ff = fc(r);
        if (showResults() && r.format !== 'field') {
          const dr = districtResult(r);
          const color = dr.party === 'D' ? 'd-text' : dr.party === 'R' ? 'r-text' : '';
          return String(html`<button type="button" class="district-btn" data-district="${f.id}" aria-pressed="false"><span class="dn">${label}</span><span class="dm ${color}">${dr.won ? html`<span class="win-tick">${icon.check()}</span>` : ''}${dr.text}</span></button>`);
        }
        const lp = ff.kind === 'field' ? (ff.dr != null ? (ff.dr > 0 ? 'D' : 'R') : ff.held) : ff.open ? ff.ratingParty : ff.lead.party;
        const color = lp === 'D' ? 'd-text' : lp === 'R' ? 'r-text' : '';
        return String(html`<button type="button" class="district-btn" data-district="${f.id}" aria-pressed="false"><span class="dn">${label}</span><span class="dm ${color}">${leadStr(ff)}</span></button>`);
      }).join('');
    };
    fillList();
    root.querySelectorAll('[data-view]').forEach((b) => b.addEventListener('click', () => {
      setMapView(b.dataset.view);
      root.querySelectorAll('[data-view]').forEach((x) => x.setAttribute('aria-pressed', String(x === b)));
      const eb = root.querySelector('.map-card .eyebrow');
      if (eb) eb.textContent = `Federal · 2026 district ${mapView() === 'results' ? 'results' : 'final forecast'}`;
      map.refill();
      root.querySelector('#district-legend').innerHTML = showResults() ? resultsLegend() : ratingLegendHTML(notUp);
      const pressed = list.querySelector('[aria-pressed="true"]')?.dataset.district;
      fillList();
      if (pressed) list.querySelector(`[data-district="${CSS.escape(pressed)}"]`)?.setAttribute('aria-pressed', 'true');
    }));
    list.addEventListener('click', (e) => {
      const b = e.target.closest('[data-district]');
      if (b) select(b.dataset.district, true);
    });

    function select(code, fromUser) {
      const r = races.get(code);
      map.select(code);
      list.querySelectorAll('[data-district]').forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.district === code)));
      if (!r) {
        panel.innerHTML = String(emptyState('No election here in 2026', 'This district’s seat is not on the ballot this year because of staggered terms.'));
        return;
      }
      panel.innerHTML = String(html`<section class="card" style="padding:clamp(16px,3vw,28px)">${raceFull(r, { tag: 'h2' })}</section>`);
      mountRaceTabs(panel);
      if (fromUser) {
        const q = new URLSearchParams({ level: m.level, chamber: m.chamber, d: code });
        history.replaceState(null, '', `#/state/${st}?${q}`);
        map.zoomTo(code);
        panel.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }

    // Start on the requested district, else the closest race, so the panel is never empty.
    // (For state legislative races, the closest 2024 presidential result with candidates listed.)
    const closeField = field.filter((r) => r.candidates.length && r.pres24 != null).sort((a, b) => Math.abs(a.pres24) - Math.abs(b.pres24))[0];
    // (With results in, the closest count: an uncalled race first.)
    const closeResult = withResults ? up.filter((r) => resultMargin(r))
      .sort((a, b) => (a.result.status === 'won') - (b.result.status === 'won') || resultMargin(a).pts - resultMargin(b).pts)[0] : null;
    const start = ctx.query.d && races.has(ctx.query.d) ? ctx.query.d
      : (closeField || closeResult || up.find((r) => !r.demo) || up.slice().sort((a, b) => Math.abs((fc(a).pLead ?? 1) - 0.5) - Math.abs((fc(b).pLead ?? 1) - 0.5))[0])?.district;
    if (start) select(start, false);
  },
};
