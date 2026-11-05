// Upcoming elections (#/upcoming): the elections of the next three years, from
// data/upcoming.json (scripts/update_upcoming.py, read every day from Wikipedia), with
// the 2026 runoffs still ahead taken from the race data itself. Declared candidates only,
// and no forecasts: nothing is rated or polled this early.
//
// Beyond president, Congress and the statewide offices, the file lists the other
// statewide offices ("more"), mayors and county offices ("local") and the state
// legislatures by district ("legislatures"), and who each person is ("people": the first
// sentences of their Wikipedia article, their Wikidata photo and a checked website).
// "My elections" shows a visitor's own future races through futureElections() below.

import { html, raw, fetchJSON, fmtDate, fmtDR } from '../util.js';
import { icon } from '../icons.js';
import { STATE_BY_ABBR } from '../data/states.js';
import { allRaces, getRace, raceTitle, resultWinners } from '../data/world.js';
import { candBadge, photoCredits } from '../components/race.js';

let cache = null;
const JUDICIAL = new Set(['supreme-court']);
export async function loadUpcoming() {
  if (cache) return cache;
  try { cache = await fetchJSON('data/upcoming.json'); } catch { cache = null; return null; }
  // Each person's bio, photo, party and official website, shared by every race they're in.
  const info = cache.people || {};
  const attach = (p, party = true) => {
    const i = p?.name && p.wiki && info[p.wiki];
    if (!i) return;
    p.info = i;
    if (i.photo && !p.photo) p.photo = i.photo;
    if (party && !p.party && i.party) p.party = i.party;
  };
  for (const r of [...(cache.races || []), ...(cache.more || []), ...(cache.local || [])]) {
    // Judges keep only the party their page's list gives them (most ballots print none);
    // the party of an earlier career, from Wikidata, stays off the page.
    const party = !JUDICIAL.has(r.office);
    attach(r.holder, party);
    (r.candidates || []).forEach((c) => attach(c, party));
  }
  for (const ch of cache.legislatures || []) for (const ms of Object.values(ch.districts || {})) ms.forEach(attach);
  return cache;
}

const PARTY = { D: 'Democratic', R: 'Republican', L: 'Libertarian', G: 'Green', I: 'Independent' };
const FILTERS = {
  all: 'All offices', federal: 'President and Congress', governor: 'Governors', statewide: 'Other statewide offices',
  legislature: 'State legislatures', local: 'Mayors and county offices',
};
const FEDERAL = new Set(['president', 'senate', 'house']);
const GROUPS = [
  ['president', 'President'], ['senate', 'U.S. Senate'], ['house', 'U.S. House'], ['governor', 'Governor'],
  ['lieutenant-governor', 'Lieutenant governor'], ['attorney-general', 'Attorney general'],
  ['secretary-of-state', 'Secretary of state'], ['treasurer', 'Treasurer'], ['auditor', 'Auditor or comptroller'],
  ['agriculture', 'Agriculture commissioner'], ['insurance', 'Insurance commissioner'],
  ['superintendent', 'Superintendent of education'], ['labor', 'Labor commissioner'], ['lands', 'Public lands commissioner'],
  ['supreme-court', 'State supreme court'], ['legislature', 'State legislature'], ['county', 'County offices'], ['mayor', 'Mayor'],
];
// The 2026 race of the same office, where the site has one (two-year terms: New Hampshire's
// and Vermont's governors, Vermont's statewide officers).
const CODE_2026 = { governor: 'GOV', 'lieutenant-governor': 'LG', 'attorney-general': 'AG', 'secretary-of-state': 'SOS', treasurer: 'TREAS', auditor: 'AUD' };
const NUMBER = ['', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen'];

const stateName = (st) => (st === 'DC' ? 'District of Columbia' : STATE_BY_ABBR[st]?.name || st);
const partyLetter = (p) => (p && p.length <= 2 ? p : p ? p.slice(0, 3) : '');
const partyColor = (p) => (p === 'D' ? 'var(--dem)' : p === 'R' ? 'var(--rep)' : 'var(--other)');
const dot = (p) => html`<span class="pdot ${p === 'D' || p === 'R' ? p : ''}" aria-hidden="true"></span>`;
const ymd = (s) => { const [y, m, d] = s.split('-').map(Number); return new Date(y, m - 1, d); };
const weekday = (s) => ymd(s).toLocaleDateString('en-US', { weekday: 'long' });
const ext = (url, text) => html`<a href="${url}" target="_blank" rel="noopener noreferrer">${text}</a>`;
const hostOf = (u) => { try { return new URL(u).hostname.replace(/^www\./, ''); } catch { return ''; } };
export const kindOf = (r) => (FEDERAL.has(r.office) ? 'federal' : r.office === 'governor' ? 'governor' : r.office === 'legislature' ? 'legislature'
  : r.level === 'local' ? 'local' : 'statewide');

function person(p) {
  const party = partyLetter(p.party);
  return html`${dot(p.party)}<span>${p.wiki ? ext(p.wiki, p.name) : p.name}${party ? html` <span class="faint">(${party})</span>` : ''}</span>`;
}

// A person with their photo, who they are (their Wikipedia article's first sentences)
// and their website: the campaign's where a race page lists one, else their official one.
function who(p, { note = '', bio = true } = {}) {
  const info = p.info || {};
  const party = partyLetter(p.party);
  const site = p.site || info.site;
  return html`<div class="up-person">
    ${candBadge(p, partyColor(p.party))}
    <div class="up-person-main">
      <div class="up-person-name">${p.wiki ? ext(p.wiki, p.name) : p.name}${party ? html` <span class="faint">(${party})</span>` : ''}${note ? html` <span class="up-note">· ${note}</span>` : ''}</div>
      ${p.experience ? html`<div class="tiny muted">${p.experience}</div>` : ''}
      ${bio && info.bio ? html`<p class="up-bio">${info.bio}</p>` : ''}
      ${site ? html`<div class="tiny"><a href="${site}" target="_blank" rel="noopener noreferrer">${p.site ? 'Campaign site' : 'Website'} ${icon.external()}</a> <span class="faint">${hostOf(site)}</span></div>` : ''}
    </div>
  </div>`;
}

// Wikipedia's statuses, in plainer words.
function plansText(r) {
  const s = (r.statusText || '').replace(/^Incumbent[’']?s?\s+/i, '').trim();
  const t = s.toLowerCase();
  if (!r.holder?.name) {
    if (/appointee/.test(t)) return 'The appointee’s plans aren’t known yet';
    return r.level ? s : '';
  }
  if (r.plans === 'running') return 'Running for another term';
  if (/^eligible$/.test(t)) return 'Can run again; no announcement yet';
  if (/intent unknown/.test(t)) return 'Hasn’t announced plans yet';
  return s ? s.charAt(0).toUpperCase() + s.slice(1) : r.level || r.holderSource ? 'Plans not listed yet' : '';
}

const termsText = (r) => (r.terms ? `${NUMBER[r.terms] || r.terms} term${r.terms > 1 ? 's' : ''} so far` : '');

function holderLine(r) {
  const h = r.holder || {};
  const prev = CODE_2026[r.office] && r.state ? getRace(`${r.state}-${CODE_2026[r.office]}`) : null;
  const won = prev ? resultWinners(prev) : [];
  const plans = plansText(r);
  const label = r.office === 'president' ? 'President now' : r.office === 'mayor' ? 'Mayor now' : 'Holds the office now';
  const prevLine = prev && h.name ? html`<div class="small"><span class="faint">2026:</span> ${won.length
    ? html`${won.map((w, i) => html`${i ? ', ' : ''}${w.name} (${partyLetter(w.party)})`)} won · <a href="#/race/${encodeURIComponent(prev.id)}">see the result</a>`
    : html`<a href="#/race/${encodeURIComponent(prev.id)}">${raceTitle(prev)}</a>, not called yet`}</div>` : '';
  if (h.name) {
    return html`<div class="stack-sm"><div class="tiny faint up-label">${label}</div>
      ${who(h, { note: [termsText(r), plans].filter(Boolean).join(' · ') })}${prevLine}</div>`;
  }
  if (h.appointment) {
    // The departing senator holds the seat until they resign; an appointee then serves
    // until the special election.
    return html`<div class="small"><span class="faint">Until the election:</span> <span class="up-who-inline">${dot(h.party)}<span>an appointee, still to be named${h.party ? html` <span class="faint">(${PARTY[h.party] || h.party} seat)</span>` : ''}</span></span>${plans ? html` <span class="muted">· ${plans}</span>` : ''}</div>`;
  }
  if (prev) {
    // Two-year offices whose 2026 winner Wikipedia's table doesn't name yet: our own
    // 2026 result says who (a winner is only ever a check-marked call).
    if (won.length) {
      return html`<div class="stack-sm"><div class="tiny faint up-label">Elected in 2026</div>${won.map((w) => who(w))}
        <div class="small"><a href="#/race/${encodeURIComponent(prev.id)}">See the result</a></div></div>`;
    }
    return html`<div class="small"><span class="faint">${label}:</span> decided by the 2026 race, <a href="#/race/${encodeURIComponent(prev.id)}">not called yet</a></div>`;
  }
  if (/^A new office\b/.test(r.statusText || '')) {
    // Los Angeles County's executive, first elected in 2028: nobody to list yet.
    return html`<div class="small"><span class="faint">${label}:</span> no one yet. <span class="muted">${r.statusText}.</span></div>`;
  }
  return html`<div class="small"><span class="faint">${label}:</span> <span class="faint">not listed yet</span>${plans ? html` <span class="muted">· ${plans}</span>` : ''}</div>`;
}

function record(r) {
  const parts = [];
  if (r.firstElected) {
    const years = r.firstElected.replace(/\s+(?=\d{4})/g, ', ');
    // The tables' "First elected" column: Louisiana's governor was elected in 2023 and
    // took office in 2024.
    parts.push(r.office === 'senate' ? `${/lost/.test(years) ? 'Senate races' : 'Elected'} ${years}` : `First elected ${years}`);
  } else if (r.since) parts.push(`In office since ${r.since}`);
  if (r.lastRace && /\d/.test(r.lastRace)) parts.push(`last race ${r.lastRace}`);
  return parts.length ? html`<div class="small faint">${parts.join(' · ')}</div>` : '';
}

function peopleList(list, { incumbentNote = true } = {}) {
  // Long fields (a big city's mayoral race) keep each person to a line or two, and the
  // officeholder's bio is already in the line above.
  const bio = list.length <= 6;
  return html`<div class="up-people">${list.map((c) => who(c, { note: incumbentNote && c.incumbent ? 'incumbent' : '', bio: bio && !c.incumbent }))}</div>`;
}

function declared(r) {
  if (r.office === 'president') {
    const by = (p) => r.candidates.filter((c) => c.party === p);
    const rows = (r.primaries || []).map((pr) => {
      const people = by(pr.party);
      return html`<div class="small"><div class="tiny faint up-label">${PARTY[pr.party] || pr.party} primaries</div>${people.length
        ? html`<div class="up-people">${people.map((c) => who(c, { note: [c.home, c.announced ? `announced ${fmtDate(c.announced)}` : ''].filter(Boolean).join('; ') }))}</div>`
        : html`<span class="muted">No one has declared yet</span>`}</div>`;
    });
    const others = r.candidates.filter((c) => !(r.primaries || []).some((pr) => pr.party === c.party));
    return html`${rows}${others.length ? html`<div class="small"><div class="tiny faint up-label">Others</div>${peopleList(others)}</div>` : ''}`;
  }
  if (!r.candidates.length) {
    return html`<div class="small muted">${r.office === 'mayor' && !r.page ? 'Candidates aren’t listed yet' : 'No declared candidates yet'}</div>`;
  }
  return html`<div class="small"><div class="tiny faint up-label">Declared · ${r.candidates.length}</div>${peopleList(r.candidates)}</div>`;
}

const sameOffice = (a, b) => a.toLowerCase().replace(/^(state|u\.s\.)\s+/, '') === b.toLowerCase().replace(/^(state|u\.s\.)\s+/, '');

function titleOf(r) {
  if (r.office === 'president') return 'President of the United States';
  if (r.office === 'mayor') return `${r.place}, ${stateName(r.state)}`;
  if (r.office === 'county') return `${r.county}, ${stateName(r.state)}`;
  return stateName(r.state);
}

function dateLine(r) {
  if (!r.date) return html`<div class="small faint">Date not listed yet</div>`;
  return html`<div class="small"><b>${weekday(r.date)}, ${fmtDate(r.date)}</b>${r.dateNote ? html` <span class="muted">· ${r.dateNote}</span>` : ''}</div>`;
}

function sourceLine(r) {
  const asOf = r.source?.asOf ? fmtDate(r.source.asOf.slice(0, 10)) : '';
  const bits = [];
  if (r.page) bits.push(ext(r.page.url, 'More on Wikipedia'));
  if (r.holderSource && !r.page) bits.push(html`officeholder from ${ext(r.holderSource.url, r.holderSource.title.replace(/^Wikipedia: /, '').replace(/, infobox$/, ''))}`);
  if (asOf) {
    // Without a page of its own, the list it comes from is the link (mayors, 2028's
    // attorneys general).
    const what = r.source.note || r.office === 'mayor' ? 'Wikipedia’s list' : r.level ? 'Wikipedia' : 'Wikipedia’s table';
    bits.push(html`${!r.page && r.source.url ? ext(r.source.url, what) : what} as of ${asOf}`);
  }
  return bits.length ? html`<div class="tiny faint">${bits.map((b, i) => html`${i ? ' · ' : ''}${b}`)}</div>` : '';
}

export function card(r, groupLabel = null, { showDate = false } = {}) {
  if (r.office === 'house') {
    return html`<article class="card up-card">
      ${groupLabel ? '' : html`<div class="eyebrow">U.S. House</div>`}
      <h3 style="margin:0">All ${r.seats || 435} seats</h3>
      ${showDate ? dateLine(r) : ''}
      <div class="small muted">Every House seat is up every two years. The members elected on November 3, 2026, serve until January 3, ${r.year + 1}; see <a href="#/congress">who sits in Congress</a>.</div>
      <div class="small muted">Candidates aren’t listed yet.</div>
    </article>`;
  }
  if (r.office === 'legislature') return chamberCard(r, { showDate, groupLabel });
  return html`<article class="card up-card">
    <div class="row between" style="gap:8px;align-items:flex-start">
      <div>${groupLabel && sameOffice(r.officeName, groupLabel) ? '' : html`<div class="eyebrow">${r.officeName}</div>`}<h3 style="margin:2px 0 0">${titleOf(r)}</h3></div>
      ${r.special ? html`<span class="chip">Special election</span>` : ''}
    </div>
    ${showDate ? dateLine(r) : ''}
    ${holderLine(r)}
    ${record(r)}
    ${declared(r)}
    ${sourceLine(r)}
  </article>`;
}

function partyCounts(members) {
  const n = { D: 0, R: 0, other: 0 };
  for (const m of members) {
    if (m.party === 'D' || m.party === 'R') n[m.party] += 1; else n.other += 1;
  }
  return [n.R ? `${n.R} Republican${n.R > 1 ? 's' : ''}` : '', n.D ? `${n.D} Democrat${n.D > 1 ? 's' : ''}` : '',
    n.other ? `${n.other} other${n.other > 1 ? 's' : ''} or vacant` : ''].filter(Boolean).join(', ');
}

function chamberCard(ch, { showDate = false, groupLabel = null } = {}) {
  const members = Object.values(ch.districts || {}).flat();
  const leaving = members.filter((m) => m.plans === 'leaving').length;
  const districts = Object.keys(ch.districts || {}).length;
  return html`<article class="card up-card">
    ${groupLabel ? '' : html`<div class="eyebrow">State legislature</div>`}
    <h3 style="margin:2px 0 0">${ch.officeName}</h3>
    ${showDate ? dateLine(ch) : ''}
    <div class="small">All ${ch.seats} seats${districts !== ch.seats ? ` (${districts} districts)` : ''} are up. Held now by ${partyCounts(members)}.</div>
    ${leaving ? html`<div class="small muted">${leaving} member${leaving > 1 ? 's are' : ' is'} not running again (term limits or retirement), as Wikipedia lists them so far.</div>` : ''}
    <div class="small"><a href="#/elections">See your own district in My elections</a></div>
    <div class="tiny faint">${ext(ch.page.url, 'More on Wikipedia')} · members from ${ext(ch.source.url, ch.source.title.replace(/^Wikipedia: /, '').replace(/, (members|results by district)$/, ''))}</div>
  </article>`;
}

function districtCard(ch, key) {
  const all = ch.districts[key] || [];
  const ms = all.filter((m) => m.name);
  const vacant = all.length - ms.length;
  const dr = ms.find((m) => m.dr != null)?.dr;
  // Always under My elections' "State legislature" heading, so no eyebrow of its own.
  return html`<article class="card up-card">
    <h3 style="margin:0">${ch.officeName}, District ${key}</h3>
    ${dateLine(ch)}
    ${ms.length ? html`<div class="stack-sm"><div class="tiny faint up-label">${ms.length > 1 ? 'Hold the seats now' : 'Holds the seat now'}</div>
      ${ms.map((m) => who(m, { note: [m.firstElected ? `first elected ${m.firstElected}` : '', m.statusText].filter(Boolean).join(' · ') }))}</div>` : ''}
    ${vacant ? html`<div class="small">${ms.length ? `${vacant > 1 ? `${vacant} seats are` : 'One seat is'} vacant now.` : 'The seat is vacant now.'} <span class="muted">The ${ch.year} election fills it, unless a special election comes first.</span></div>` : ''}
    ${dr != null ? html`<div class="small faint">The district voted ${fmtDR(dr)} for president in 2024.</div>` : ''}
    <div class="small muted">Every seat in the chamber is up. Candidates aren’t listed district by district yet.</div>
    <div class="tiny faint">${ext(ch.page.url, 'More on Wikipedia')} · members from ${ext(ch.source.url, ch.source.title.replace(/^Wikipedia: /, '').replace(/, (members|results by district)$/, ''))}</div>
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
  const other = rs.filter((r) => kindOf(r) === 'statewide').length;
  if (other) parts.push(`${other} other statewide office${other > 1 ? 's' : ''}`);
  if (n('legislature')) parts.push(`${n('legislature')} legislative chamber${n('legislature') > 1 ? 's' : ''}`);
  if (n('county')) parts.push(`${n('county')} county office${n('county') > 1 ? 's' : ''}`);
  if (n('mayor')) parts.push(`${n('mayor')} mayor${n('mayor') > 1 ? 's' : ''}`);
  if (!parts.length) return '';
  let list = parts.length > 1 ? `${parts.slice(0, -1).join(', ')} and ${parts[parts.length - 1]}` : parts[0];
  list = list.charAt(0).toUpperCase() + list.slice(1);
  const states = new Set(rs.filter((r) => r.state).map((r) => r.state)).size;
  return `${list}${states ? `, in ${states} state${states > 1 ? 's' : ''}` : ''}.`;
}

// Runoffs from 2026 still to come, from the race data (Louisiana's December runoffs).
function runoffs(stateF, officeF) {
  const rs = allRaces().filter((r) => !r.demo && r.result?.status === 'runoff')
    .filter((r) => (stateF === 'all' || r.state === stateF) && (officeF === 'all' || (officeF === 'federal' ? FEDERAL.has(r.office) : officeF === 'governor' ? r.office === 'governor' : officeF === 'statewide' && r.format === 'office')))
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

// Mayors whose dates Wikipedia doesn't list, as one compact list by state.
function mayorList(rs) {
  const byState = new Map();
  for (const r of rs) {
    if (!byState.has(r.state)) byState.set(r.state, []);
    byState.get(r.state).push(r);
  }
  return html`<details class="card up-mayors">
    <summary><b>Mayors</b> <span class="faint">· ${rs.length} more cit${rs.length > 1 ? 'ies' : 'y'}, dates not listed yet</span></summary>
    <p class="small muted" style="margin:8px 0 0">From Wikipedia’s list of this year’s mayoral elections: the mayor now and whether they can run again. Pick a state above for each mayor’s card.</p>
    <div class="up-mayor-grid">${[...byState].sort((a, b) => stateName(a[0]).localeCompare(stateName(b[0]))).map(([st, list]) => html`<div>
      <h4 class="up-group" style="margin:0">${stateName(st)}</h4>
      <ul class="up-mayor-list">${list.map((r) => html`<li><b>${r.place}</b>${r.special ? ' (special)' : ''} · ${r.holder?.name ? (r.holder.wiki ? ext(r.holder.wiki, r.holder.name) : r.holder.name) : 'mayor not listed'}${r.holder?.party ? html` <span class="faint">(${partyLetter(r.holder.party)})</span>` : ''}${r.statusText ? html` <span class="muted">· ${plansText(r)}</span>` : ''}</li>`)}</ul>
    </div>`)}</div>
  </details>`;
}

function groupBlock(list, { showDate = false } = {}) {
  return GROUPS.filter(([k]) => list.some((r) => r.office === k)).map(([k, label], _, shown) => {
    const group = list.filter((r) => r.office === k);
    const head = shown.length > 1 || group.length > 1;
    return html`<div class="stack-sm">
      ${head ? html`<h3 class="up-group">${label}${group.length > 1 ? html` <span class="faint">· ${group.length}</span>` : ''}</h3>` : ''}
      <div class="up-grid">${group.map((r) => card(r, head ? label : null, { showDate }))}</div>
    </div>`;
  });
}

function yearSection(y, rs, { stateF }) {
  const dated = rs.filter((r) => r.date);
  const undated = rs.filter((r) => !r.date);
  const byDate = new Map();
  for (const r of dated) {
    if (!byDate.has(r.date)) byDate.set(r.date, []);
    byDate.get(r.date).push(r);
  }
  return html`<section class="stack" aria-labelledby="up-${y}">
    <div><h2 id="up-${y}" style="margin:0">${y}</h2><p class="small muted" style="margin:4px 0 0">${summary(rs)}</p></div>
    ${[...byDate].sort((a, b) => a[0].localeCompare(b[0])).map(([d, list]) => {
      const notes = [...new Set(list.map((r) => r.dateNote).filter(Boolean))];
      const states = [...new Set(list.map((r) => r.state).filter(Boolean))];
      return html`<div class="stack-sm">
        <div class="up-date"><b>${weekday(d)}, ${fmtDate(d)}</b>${states.length && states.length <= 3 && list.every((r) => r.state) ? html` <span class="muted">· ${states.map(stateName).join(', ')}</span>` : ''}
          ${notes.map((n) => html`<div class="small muted">${n}</div>`)}</div>
        ${groupBlock(list)}
      </div>`;
    })}
    ${undated.length ? (stateF === 'all' ? mayorList(undated) : html`<div class="stack-sm">
      <div class="up-date"><b>Dates not listed yet</b></div>${groupBlock(undated)}</div>`) : ''}
  </section>`;
}

// Every person a list of races shows, for the photo credits.
function peopleIn(rs) {
  const out = [];
  for (const r of rs) {
    if (r.office === 'legislature') continue;
    if (r.holder?.name) out.push(r.holder);
    out.push(...(r.candidates || []));
  }
  return out;
}

function allOf(data) {
  return [...(data?.races || []), ...(data?.more || []), ...(data?.legislatures || []), ...(data?.local || [])];
}

export const upcoming = {
  title: () => 'Upcoming elections',
  async render(ctx) {
    const data = await loadUpcoming();
    const office = FILTERS[ctx.query.office] ? ctx.query.office : 'all';
    const stateF = ctx.query.state && (STATE_BY_ABBR[ctx.query.state] || ctx.query.state === 'DC') ? ctx.query.state : 'all';
    const keep = (r) => (stateF === 'all' || r.state === stateF || (!r.state && (office === 'all' || office === 'federal')))
      && (office === 'all' || kindOf(r) === office);
    const races = allOf(data).filter(keep);
    const years = data?.years || [];
    const states = Object.values(STATE_BY_ABBR).sort((a, b) => a.name.localeCompare(b.name));
    const q = (patch) => {
      const p = new URLSearchParams({ ...(office !== 'all' ? { office } : {}), ...(stateF !== 'all' ? { state: stateF } : {}), ...patch });
      for (const [k, v] of [...p]) if (v === 'all') p.delete(k);
      const s = p.toString();
      return `#/upcoming${s ? `?${s}` : ''}`;
    };
    const run = runoffs(stateF, office);
    const shown = races.filter((r) => stateF !== 'all' || r.office !== 'mayor' || r.date);
    const sources = [...(data?.sources || []), ...(data?.moreSources || [])];
    return html`<div class="wrap page stack-lg">
      <div><div class="eyebrow">Upcoming elections</div>
        <h1 style="margin:6px 0 8px">The next three years</h1>
        <p class="muted" style="margin:0">The elections from now through ${years[years.length - 1] || 2029} for president, Congress, governor and the other statewide offices, the state legislatures and, where Wikipedia lists them, mayors and county offices: when each is, who holds the office now and whether they can or will run again, who they are, and the candidates who have declared so far. No forecasts yet: these races aren’t rated or polled this early. Read every day from Wikipedia${data?.updated ? `; last updated ${fmtDate(data.updated)}` : ''}. <a href="#/elections">My elections</a> shows the ones on your own ballot.</p></div>
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
        return rs.length ? yearSection(y, rs, { stateF }) : html`<section class="stack" aria-labelledby="up-${y}"><h2 id="up-${y}" style="margin:0">${y}</h2><p class="small muted" style="margin:0">${stateF !== 'all' || office !== 'all' ? 'Nothing matching these filters.' : 'No elections listed yet.'}</p></section>`;
      })}
      ${photoCredits(peopleIn(shown))}
      <p class="tiny faint" style="margin:0">Dates are election days (Louisiana votes first in an open primary). Primaries come earlier and aren’t listed. Mayors come from Wikipedia’s list of each year’s mayoral elections, and county offices only from the county pages it has (so far Los Angeles County’s district attorney and county executive); district attorneys elsewhere, other local offices and seats elected by district below the legislature aren’t covered yet. Each bio is the start of the person’s Wikipedia article (CC BY-SA), shown only when the article’s title has their name; websites are the campaign’s where a race page lists one, else the person’s official site on Wikidata, and each is checked to answer and show the person’s name.</p>
      <details class="tiny faint"><summary style="cursor:pointer">Sources: ${sources.length} Wikipedia pages (CC BY-SA)</summary>
        <p style="margin:6px 0 0">${sources.map((s, i) => html`${i ? ' · ' : ''}${ext(s.url, s.title.replace(/^Wikipedia: /, ''))}`)}</p></details>`}
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

// "My elections": the visitor's own future races -------------------------------------

const fold = (s) => (s || '').normalize('NFKD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[.'’]/g, '').replace(/\s+/g, ' ').trim();
// The Census Bureau names places "Baton Rouge city", "Nashville-Davidson metropolitan
// government (balance)" or "Boise City city"; Wikipedia's lists say "Baton Rouge",
// "Nashville" and "Boise".
const PLACE_KIND = /\s+(city|town|village|borough|municipality|cdp|metropolitan government|metro government|consolidated government|unified government|urban county|charter township|township|plantation|corporation|city and borough)$/;
function placeBase(s) {
  let b = fold(s).replace(/\s*\(balance\)$/, '');
  for (let i = 0; i < 2; i += 1) b = b.replace(PLACE_KIND, '');
  return b;
}
export function samePlace(listed, censusName) {
  if (!listed || !censusName) return false;
  const a = placeBase(listed), b = placeBase(censusName);
  return a === b || b.startsWith(`${a}-`) || b.startsWith(`${a}/`) || b === `${a} city`;
}
const sameCounty = (a, b) => !!a && !!b && fold(a) === fold(b);
const districtKey = (code) => {
  if (!code) return null;
  const n = parseInt(code, 10);
  return Number.isFinite(n) ? String(n) : String(code).replace(/^0+/, '');
};

function myHouseCard(r, ad) {
  const st = ad.state;
  const cd = st === 'DC' ? '98' : ad.cd;
  const prev = cd ? getRace(`${st}-H-${cd}`) : null;
  const won = prev ? resultWinners(prev) : [];
  return html`<article class="card up-card">
    <div class="eyebrow">U.S. House</div>
    <h3 style="margin:2px 0 0">${prev ? raceTitle(prev) : `${stateName(st)}: your district`}</h3>
    ${dateLine(r)}
    ${won.length ? html`<div class="stack-sm"><div class="tiny faint up-label">Holds the seat from January 3, ${r.year - 1}</div>
        ${won.map((w) => who(w, { note: 'elected in 2026' }))}
        <div class="small"><a href="#/race/${encodeURIComponent(prev.id)}">See the 2026 result</a></div></div>`
      : prev ? html`<div class="small">Who holds the seat is decided by the 2026 race: <a href="#/race/${encodeURIComponent(prev.id)}">${prev.result?.status === 'runoff' ? 'headed to a runoff' : 'not called yet'}</a>.</div>` : ''}
    <div class="small muted">Every House seat is up every two years. Candidates aren’t listed yet.</div>
  </article>`;
}

const LEVELS = [['federal', 'President and Congress'], ['statewide', 'Statewide'], ['legislature', 'State legislature'], ['local', 'Local']];

// {html, people}: one "Future elections for <year>" disclosure for each year with an
// election on the visitor's ballot (their state, congressional and legislative districts,
// city or county), open where `openYears` says.
export async function futureElections(ad, openYears = new Set()) {
  const data = await loadUpcoming();
  if (!data || !ad?.state) return { html: '', people: [] };
  const st = ad.state;
  const byYear = new Map();
  const add = (y, level, item) => {
    if (!byYear.has(y)) byYear.set(y, []);
    byYear.get(y).push({ level, ...item });
  };
  for (const r of data.races || []) {
    if (r.office === 'president' || r.office === 'house') add(r.year, 'federal', { r });
    else if (r.state === st) add(r.year, FEDERAL.has(r.office) ? 'federal' : 'statewide', { r });
  }
  for (const r of data.more || []) if (r.state === st) add(r.year, 'statewide', { r });
  for (const ch of data.legislatures || []) {
    if (ch.state !== st) continue;
    // New Jersey's Assembly districts are its Senate districts.
    const key = districtKey(ch.layer === 'sldu' ? ad.sldu : (ad.sldl || (st === 'NJ' ? ad.sldu : null)));
    if (key && ch.districts?.[key]) add(ch.year, 'legislature', { ch, key });
  }
  for (const r of data.local || []) {
    if (r.state === st && ((r.place && samePlace(r.place, ad.place)) || (r.county && sameCounty(r.county, ad.county)))) add(r.year, 'local', { r });
  }
  const years = [...byYear.keys()].sort();
  if (!years.length) return { html: '', people: [] };
  const people = [];
  const cardFor = (it) => {
    if (it.ch) {
      people.push(...it.ch.districts[it.key].filter((m) => m.name));
      return districtCard(it.ch, it.key);
    }
    if (it.r.office === 'house') return myHouseCard(it.r, ad);
    if (it.r.holder?.name) people.push(it.r.holder);
    people.push(...(it.r.candidates || []));
    return card(it.r, null, { showDate: true });
  };
  const sortKey = (it) => {
    const r = it.r || it.ch;
    const rank = GROUPS.findIndex(([k]) => k === r.office);
    return `${r.date || '9999'}|${String(rank).padStart(2, '0')}|${it.ch?.chamber === 'house' ? 1 : 0}`;
  };
  const last = data.years?.[data.years.length - 1] || years[years.length - 1];
  return {
    people,
    html: html`<section class="stack" aria-labelledby="future-h">
      <div><h2 id="future-h" style="margin:0">Future elections</h2>
        <p class="small muted" style="margin:4px 0 0">What’s ahead on your ballot through ${last}, as Wikipedia lists it today: when each election is, who holds the office now and whether they can run again, who they are, and who has declared. Only the years with an election for your state, districts${ad.place ? ', city' : ''} or county are listed. Primaries, most local offices and seats elected by district below the legislature aren’t covered yet. <a href="#/upcoming?state=${st}">Every upcoming election in ${stateName(st)}</a>.</p></div>
      ${years.map((y) => {
        const items = byYear.get(y).sort((a, b) => sortKey(a).localeCompare(sortKey(b)));
        return html`<details class="card future-year" data-year="${y}" ${raw(openYears.has(y) ? 'open' : '')}>
          <summary><span class="future-head"><span class="future-title">Future elections for ${y}</span><span class="faint small">${items.length} election${items.length > 1 ? 's' : ''}</span></span>${icon.chevronDown()}</summary>
          <div class="stack" style="margin-top:14px">${LEVELS.filter(([k]) => items.some((it) => it.level === k)).map(([k, label]) => html`<div class="stack-sm">
            <h3 class="up-group">${label}</h3>
            <div class="up-grid">${items.filter((it) => it.level === k).map(cardFor)}</div>
          </div>`)}</div>
        </details>`;
      })}
    </section>`,
  };
}
