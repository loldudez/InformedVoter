// Upcoming elections (#/upcoming): the elections of the next three years, from
// data/upcoming.json (scripts/update_upcoming.py, read every day from Wikipedia's
// national pages), with the 2026 runoffs still ahead taken from the race data itself.
// Declared candidates only, and no forecasts: nothing is rated or polled this early.

import { html, raw, fetchJSON, fmtDate } from '../util.js';
import { icon } from '../icons.js';
import { STATE_BY_ABBR } from '../data/states.js';
import { allRaces, getRace, raceTitle, resultWinners } from '../data/world.js';

let cache = null;
async function load() {
  try { cache = cache || await fetchJSON('data/upcoming.json'); } catch { cache = null; }
  return cache;
}

const PARTY = { D: 'Democratic', R: 'Republican', L: 'Libertarian', G: 'Green', I: 'Independent' };
const FILTERS = { all: 'All offices', federal: 'President and Congress', governor: 'Governors', statewide: 'Other statewide offices' };
const FEDERAL = new Set(['president', 'senate', 'house']);
const GROUPS = [
  ['president', 'President'], ['senate', 'U.S. Senate'], ['house', 'U.S. House'], ['governor', 'Governor'],
  ['lieutenant-governor', 'Lieutenant governor'], ['attorney-general', 'Attorney general'],
  ['secretary-of-state', 'Secretary of state'], ['treasurer', 'Treasurer'], ['auditor', 'Auditor or comptroller'],
];
// The 2026 race of the same office, where the site has one (two-year terms: New Hampshire's
// and Vermont's governors, Vermont's statewide officers).
const CODE_2026 = { governor: 'GOV', 'lieutenant-governor': 'LG', 'attorney-general': 'AG', 'secretary-of-state': 'SOS', treasurer: 'TREAS', auditor: 'AUD' };

const stateName = (st) => (st === 'DC' ? 'District of Columbia' : STATE_BY_ABBR[st]?.name || st);
const partyLetter = (p) => (p && p.length <= 2 ? p : p ? p.slice(0, 3) : '');
const dot = (p) => html`<span class="pdot ${p === 'D' || p === 'R' ? p : ''}" aria-hidden="true"></span>`;
const ymd = (s) => { const [y, m, d] = s.split('-').map(Number); return new Date(y, m - 1, d); };
const weekday = (s) => ymd(s).toLocaleDateString('en-US', { weekday: 'long' });
const ext = (url, text) => html`<a href="${url}" target="_blank" rel="noopener noreferrer">${text}</a>`;

function person(p) {
  const party = partyLetter(p.party);
  return html`${dot(p.party)}<span>${p.wiki ? ext(p.wiki, p.name) : p.name}${party ? html` <span class="faint">(${party})</span>` : ''}</span>`;
}

// Wikipedia's statuses, in plainer words.
function plansText(r) {
  const s = (r.statusText || '').replace(/^Incumbent[’']?s?\s+/i, '').trim();
  const t = s.toLowerCase();
  if (!r.holder?.name) {
    if (/appointee/.test(t)) return 'The appointee’s plans aren’t known yet';
    return '';
  }
  if (r.plans === 'running') return 'Running for another term';
  if (/^eligible$/.test(t)) return 'Can run again; no announcement yet';
  if (/intent unknown/.test(t)) return 'Hasn’t announced plans yet';
  return s ? s.charAt(0).toUpperCase() + s.slice(1) : '';
}

function holderLine(r) {
  const h = r.holder || {};
  const prev = CODE_2026[r.office] && r.state ? getRace(`${r.state}-${CODE_2026[r.office]}`) : null;
  const won = prev ? resultWinners(prev) : [];
  const plans = plansText(r);
  const resultLink = prev ? html`<a href="#/race/${encodeURIComponent(prev.id)}">see the result</a>` : '';
  let who, label = r.office === 'president' ? 'President now' : 'Holds the office now', fromPrev = false;
  if (h.name) who = html`${person(h)}`;
  else if (h.appointment) {
    // The departing senator holds the seat until they resign; an appointee then serves
    // until the special election.
    label = 'Until the election';
    who = html`${dot(h.party)}<span>an appointee, still to be named${h.party ? html` <span class="faint">(${PARTY[h.party] || h.party} seat)</span>` : ''}</span>`;
  } else if (prev) {
    // Two-year offices whose 2026 winner Wikipedia's table doesn't name yet: our own
    // 2026 result says who (a winner is only ever a check-marked call).
    fromPrev = true;
    if (won.length) { label = 'Elected in 2026'; who = html`${won.map((w) => html`<span class="up-who-inline">${person(w)}</span>`)} <span class="muted">· ${resultLink}</span>`; }
    else who = html`<span>decided by the 2026 race, <a href="#/race/${encodeURIComponent(prev.id)}">not called yet</a></span>`;
  } else who = html`<span class="faint">not listed yet</span>`;
  return html`<div class="small"><span class="faint">${label}:</span>
      <span class="up-who-inline">${who}</span>${plans ? html` <span class="muted">· ${plans}</span>` : ''}</div>
    ${prev && !fromPrev ? html`<div class="small"><span class="faint">2026:</span> ${won.length
      ? html`${won.map((w, i) => html`${i ? ', ' : ''}${w.name} (${partyLetter(w.party)})`)} won · <a href="#/race/${encodeURIComponent(prev.id)}">see the result</a>`
      : html`<a href="#/race/${encodeURIComponent(prev.id)}">${raceTitle(prev)}</a>, not called yet`}</div>` : ''}`;
}

function record(r) {
  const parts = [];
  if (r.firstElected) {
    const years = r.firstElected.replace(/\s+(?=\d{4})/g, ', ');
    parts.push(r.office === 'senate' ? `${/lost/.test(years) ? 'Senate races' : 'Elected'} ${years}` : `In office since ${years}`);
  }
  if (r.lastRace && /\d/.test(r.lastRace)) parts.push(`last race ${r.lastRace}`);
  return parts.length ? html`<div class="small faint">${parts.join(' · ')}</div>` : '';
}

function declared(r) {
  if (r.office === 'president') {
    const by = (p) => r.candidates.filter((c) => c.party === p);
    const rows = (r.primaries || []).map((pr) => {
      const people = by(pr.party);
      return html`<div class="small"><span class="faint">${PARTY[pr.party] || pr.party} primaries:</span> ${people.length
        ? html`<ul class="up-who">${people.map((c) => html`<li>${person(c)}${c.announced || c.home || c.experience ? html`<span class="faint">${[c.experience, c.home, c.announced ? `announced ${fmtDate(c.announced)}` : ''].filter(Boolean).join('; ')}</span>` : ''}</li>`)}</ul>`
        : html`<span class="muted">no one has declared yet</span>`}</div>`;
    });
    const others = r.candidates.filter((c) => !(r.primaries || []).some((pr) => pr.party === c.party));
    return html`${rows}${others.length ? html`<div class="small"><span class="faint">Others:</span><ul class="up-who">${others.map((c) => html`<li>${person(c)}</li>`)}</ul></div>` : ''}`;
  }
  if (!r.candidates.length) return html`<div class="small muted">No declared candidates yet</div>`;
  return html`<div class="small"><span class="faint">Declared:</span><ul class="up-who">${r.candidates.map((c) => html`<li>${person(c)}${c.incumbent ? html`<span class="faint">incumbent</span>` : ''}</li>`)}</ul></div>`;
}

const sameOffice = (a, b) => a.toLowerCase().replace(/^(state|u\.s\.)\s+/, '') === b.toLowerCase().replace(/^(state|u\.s\.)\s+/, '');

function card(r, groupLabel = null) {
  if (r.office === 'house') {
    return html`<article class="card up-card">
      ${groupLabel ? '' : html`<div class="eyebrow">U.S. House</div>`}
      <h3 style="margin:0">All ${r.seats || 435} seats</h3>
      <div class="small muted">Every House seat is up every two years. The members elected on November 3, 2026, serve until January 3, ${r.year + 1}; see <a href="#/congress">who sits in Congress</a>.</div>
      <div class="small muted">Candidates aren’t listed yet.</div>
    </article>`;
  }
  const title = r.office === 'president' ? 'President of the United States' : stateName(r.state);
  return html`<article class="card up-card">
    <div class="row between" style="gap:8px;align-items:flex-start">
      <div>${groupLabel && sameOffice(r.officeName, groupLabel) ? '' : html`<div class="eyebrow">${r.officeName}</div>`}<h3 style="margin:2px 0 0">${title}</h3></div>
      ${r.special ? html`<span class="chip">Special election</span>` : ''}
    </div>
    ${holderLine(r)}
    ${record(r)}
    ${declared(r)}
    <div class="tiny faint">${r.page ? html`${ext(r.page.url, 'More on Wikipedia')} · ` : ''}${r.source?.asOf ? html`Wikipedia’s table as of ${fmtDate(r.source.asOf.slice(0, 10))}` : ''}</div>
  </article>`;
}

function summary(rs) {
  const n = (k) => rs.filter((r) => r.office === k).length;
  const parts = [];
  if (n('president')) parts.push('the President');
  if (n('senate')) {
    const sp = rs.filter((r) => r.office === 'senate' && r.special).length;
    parts.push(`${n('senate')} Senate seat${n('senate') > 1 ? 's' : ''}${sp && sp < n('senate') ? ` (${sp} a special election)` : sp ? ' (a special election)' : ''}`);
  }
  if (n('house')) parts.push('every House seat');
  if (n('governor')) parts.push(`${n('governor')} governor${n('governor') > 1 ? 's' : ''}`);
  const other = rs.filter((r) => !FEDERAL.has(r.office) && r.office !== 'governor').length;
  if (other) parts.push(`${other} other statewide office${other > 1 ? 's' : ''}`);
  if (!parts.length) return '';
  let list = parts.length > 1 ? `${parts.slice(0, -1).join(', ')} and ${parts[parts.length - 1]}` : parts[0];
  list = list.charAt(0).toUpperCase() + list.slice(1);
  const states = new Set(rs.filter((r) => r.state).map((r) => r.state)).size;
  return `${list}${states ? `, in ${states} state${states > 1 ? 's' : ''}` : ''}.`;
}

// Runoffs from 2026 still to come, from the race data (Louisiana's December runoffs).
function runoffs(stateF, officeF) {
  const rs = allRaces().filter((r) => !r.demo && r.result?.status === 'runoff')
    .filter((r) => (stateF === 'all' || r.state === stateF) && (officeF === 'all' || (officeF === 'federal' ? FEDERAL.has(r.office) : officeF === 'governor' ? r.office === 'governor' : r.format === 'office')))
    .sort((a, b) => String(a.runoff || '').localeCompare(String(b.runoff || '')) || raceTitle(a).localeCompare(raceTitle(b)));
  if (!rs.length) return '';
  return html`<section class="stack" aria-labelledby="up-2026">
    <div><h2 id="up-2026" style="margin:0">2026: runoffs still ahead</h2>
      <p class="small muted" style="margin:4px 0 0">Races from November 3 that no one won outright.</p></div>
    <div class="up-grid">${rs.map((r) => {
      const adv = (r.result.advance || []).map((id) => r.candidates.find((c) => c.id === id)).filter(Boolean);
      return html`<article class="card up-card">
        <div class="eyebrow">${r.runoff ? `Runoff ${weekday(r.runoff)}, ${fmtDate(r.runoff)}` : 'Runoff, date to be set'}</div>
        <h3 style="margin:2px 0 0"><a href="#/race/${encodeURIComponent(r.id)}" style="text-decoration:none">${raceTitle(r)}</a></h3>
        ${adv.length ? html`<div class="small"><span class="faint">In the runoff:</span><ul class="up-who">${adv.map((c) => html`<li>${person(c)}</li>`)}</ul></div>` : ''}
        <div class="small"><a href="#/race/${encodeURIComponent(r.id)}">First-round result and the candidates</a></div>
      </article>`;
    })}</div>
  </section>`;
}

function yearSection(y, rs) {
  const byDate = new Map();
  for (const r of rs) {
    if (!byDate.has(r.date)) byDate.set(r.date, []);
    byDate.get(r.date).push(r);
  }
  return html`<section class="stack" aria-labelledby="up-${y}">
    <div><h2 id="up-${y}" style="margin:0">${y}</h2><p class="small muted" style="margin:4px 0 0">${summary(rs)}</p></div>
    ${[...byDate].map(([d, list]) => {
      const notes = [...new Set(list.map((r) => r.dateNote).filter(Boolean))];
      const states = [...new Set(list.map((r) => r.state).filter(Boolean))];
      return html`<div class="stack-sm">
        <div class="up-date"><b>${weekday(d)}, ${fmtDate(d)}</b>${states.length && states.length <= 3 && list.every((r) => r.state) ? html` <span class="muted">· ${states.map(stateName).join(', ')}</span>` : ''}
          ${notes.map((n) => html`<div class="small muted">${n}</div>`)}</div>
        ${GROUPS.filter(([k]) => list.some((r) => r.office === k)).map(([k, label], _, shown) => {
          const group = list.filter((r) => r.office === k);
          const head = shown.length > 1 || group.length > 1;
          return html`<div class="stack-sm">
            ${head ? html`<h3 class="up-group">${label}${group.length > 1 ? html` <span class="faint">· ${group.length}</span>` : ''}</h3>` : ''}
            <div class="up-grid">${group.map((r) => card(r, head ? label : null))}</div>
          </div>`;
        })}
      </div>`;
    })}
  </section>`;
}

export const upcoming = {
  title: () => 'Upcoming elections',
  async render(ctx) {
    const data = await load();
    const office = FILTERS[ctx.query.office] ? ctx.query.office : 'all';
    const stateF = ctx.query.state && (STATE_BY_ABBR[ctx.query.state] || ctx.query.state === 'DC') ? ctx.query.state : 'all';
    const keep = (r) => (stateF === 'all' || r.state === stateF || (!r.state && office !== 'governor' && office !== 'statewide'))
      && (office === 'all' || (office === 'federal' ? FEDERAL.has(r.office) : office === 'governor' ? r.office === 'governor' : !FEDERAL.has(r.office) && r.office !== 'governor'));
    const races = (data?.races || []).filter(keep);
    const years = data?.years || [];
    const states = Object.values(STATE_BY_ABBR).sort((a, b) => a.name.localeCompare(b.name));
    const q = (patch) => {
      const p = new URLSearchParams({ ...(office !== 'all' ? { office } : {}), ...(stateF !== 'all' ? { state: stateF } : {}), ...patch });
      for (const [k, v] of [...p]) if (v === 'all') p.delete(k);
      const s = p.toString();
      return `#/upcoming${s ? `?${s}` : ''}`;
    };
    const run = runoffs(stateF, office);
    return html`<div class="wrap page stack-lg">
      <div><div class="eyebrow">Upcoming elections</div>
        <h1 style="margin:6px 0 8px">The next three years</h1>
        <p class="muted" style="margin:0">Every election for president, Congress, governor and the statewide offices below governor from now through ${years[years.length - 1] || 2029}: when it is, who holds the office now and whether they can or will run again, and the candidates who have declared so far. No forecasts yet: these races aren’t rated or polled this early. Read every day from Wikipedia’s national pages${data?.updated ? `; last updated ${fmtDate(data.updated)}` : ''}.</p></div>
      ${!data ? html`<div class="empty">${icon.calendar()}<h3>The upcoming elections are unavailable</h3><p>Run scripts/update_upcoming.py to build them.</p></div>` : html`
      <div class="filters" role="group" aria-label="Filter">
        ${Object.entries(FILTERS).map(([k, l]) => html`<a class="chip" href="${q({ office: k })}" ${raw(k === office ? 'aria-current="page" style="background:var(--text-1);color:var(--bg);border-color:var(--text-1)"' : '')}>${l}</a>`)}
        <label class="small faint" for="up-state" style="margin-left:4px">State</label>
        <select id="up-state" class="input up-select">
          <option value="all" ${raw(stateF === 'all' ? 'selected' : '')}>All states</option>
          ${states.map((s) => html`<option value="${s.abbr}" ${raw(s.abbr === stateF ? 'selected' : '')}>${s.name}</option>`)}
        </select>
      </div>
      <nav class="filters small" aria-label="Years">${[...(run ? ['2026'] : []), ...years.map(String)].map((y) => html`<a class="chip" href="#/upcoming" data-jump="up-${y}">${y}</a>`)}</nav>
      ${run}
      ${years.map((y) => {
        const rs = races.filter((r) => r.year === y);
        return rs.length ? yearSection(y, rs) : html`<section class="stack" aria-labelledby="up-${y}"><h2 id="up-${y}" style="margin:0">${y}</h2><p class="small muted" style="margin:0">${stateF !== 'all' || office !== 'all' ? 'Nothing matching these filters.' : 'No elections listed yet.'}</p></section>`;
      })}
      <p class="tiny faint" style="margin:0">Dates are election days (Louisiana votes first in an open primary). Primaries come earlier and aren’t listed. State legislatures and local offices aren’t covered yet. Sources, under CC BY-SA: ${data.sources.map((s, i) => html`${i ? ' · ' : ''}${ext(s.url, s.title.replace(/^Wikipedia: /, ''))}`)} (Wikipedia).</p>`}
    </div>`;
  },
  mount(root) {
    root.querySelector('#up-state')?.addEventListener('change', (e) => {
      const p = new URLSearchParams(location.hash.split('?')[1] || '');
      if (e.target.value === 'all') p.delete('state'); else p.set('state', e.target.value);
      const s = p.toString();
      location.hash = `#/upcoming${s ? `?${s}` : ''}`;
    });
    root.querySelectorAll('[data-jump]').forEach((a) => a.addEventListener('click', (e) => {
      e.preventDefault();
      root.querySelector(`#${a.dataset.jump}`)?.scrollIntoView({ behavior: 'instant', block: 'start' });
    }));
    return null;
  },
};
