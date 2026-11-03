// The U.S. Congress: the House and the Senate as half-circle seat charts
// (js/components/hemicycle.js), Democrats blue, Republicans red and independents gray,
// with the key underneath, the leaders, and every member in a searchable list. The
// House Clerk's member list, English Wikipedia (senators and leaders) and Wikidata (the
// President), reread every day by scripts/update_congress.py.

import { html, fetchJSON, fmtDate, ordinal } from '../util.js';
import { icon } from '../icons.js';
import { STATE_BY_ABBR, ELECTION_DATE_LABEL } from '../data/states.js';
import { ELECTION_DAY } from '../model/forecast.js';
import { getRace } from '../data/world.js';
import { drawHemicycle, swatch } from '../components/hemicycle.js';
import { candBadge, photoCredits } from '../components/race.js';

let cache = null;
async function load() {
  try { cache = cache || await fetchJSON('data/congress.json'); } catch { cache = null; }
  return cache;
}

const COLOR = { dem: 'var(--dem)', rep: 'var(--rep)', other: 'var(--seat-other)' };
const PARTY_COLOR = { D: 'var(--dem)', R: 'var(--rep)' };
const PARTY_NAME = { D: 'Democrat', R: 'Republican', I: 'Independent' };
const SIDE = { D: 'Democrats', R: 'Republicans' };
const stateName = (st) => STATE_BY_ABBR[st]?.name || st;
const seatName = (m, ch) => (ch === 'senate' ? stateName(m.st) : m.d ? `${stateName(m.st)}’s ${ordinal(m.d)} district` : `${stateName(m.st)} at-large`);
const raceId = (m, ch) => (ch === 'senate' ? `${m.st}-SEN` : `${m.st}-H-${String(m.d).padStart(2, '0')}`);
const before = () => new Date() < ELECTION_DAY;
const list = (items) => new Intl.ListFormat('en', { type: 'conjunction' }).format(items);
const fold = (s) => String(s || '').normalize('NFD').replace(/\p{Diacritic}/gu, '').toLowerCase();

// "Majority Leader" becomes "House Majority Leader"; the presiding officers keep their titles.
function roleName(role, ch) {
  if (role === 'Speaker') return 'Speaker of the House';
  if (role === 'President') return 'President of the Senate';
  if (role === 'President pro tempore') return 'President pro tempore of the Senate';
  return `${ch === 'senate' ? 'Senate' : 'House'} ${role}`;
}

function partyLabel(m) {
  if (m.party !== 'I') return PARTY_NAME[m.party] || m.party;
  const side = SIDE[m.g?.split('-')[1]];
  return side ? `Independent (caucuses with ${side})` : 'Independent';
}

const groupsOf = (chamber) => chamber.groups.map((g) => ({ ...g, color: COLOR[g.color] || COLOR.other }));

function tip(m, ch, g) {
  return html`<div class="tt-title">${m.n}</div>
    ${m.role ? html`<div class="tt-sub">${roleName(m.role, ch)}</div>` : ''}
    <div class="t-row"><span>Party</span><b>${swatch(g, 12)}${partyLabel(m)}</b></div>
    <div class="t-row"><span>${ch === 'senate' ? 'State' : 'District'}</span><b>${seatName(m, ch)}</b></div>
    ${m.reg ? html`<div class="t-row"><span>Region</span><b>${m.reg}</b></div>` : ''}
    ${m.since ? html`<div class="t-row"><span>Senator since</span><b>${fmtDate(m.since)}</b></div>` : ''}
    ${m.up ? html`<div class="t-row"><span>Seat on the ballot</span><b>${m.up === 2026 ? 'November 3, 2026' : m.up}</b></div>` : ''}`;
}

// The key: each party's seats, whether it holds the majority, and its top leader.
function keyItem(g, chamber, ch) {
  const side = SIDE[g.id] ? g.id : null;
  const lead = side && (chamber.members.find((m) => m.party === side && m.role === 'Speaker')
    || chamber.members.find((m) => m.party === side && /^(Majority|Minority) Leader$/.test(m.role || '')));
  const status = side ? (side === chamber.control ? 'in the majority' : 'in the minority') : '';
  return html`<span><b>${g.name}</b></span>
    <span class="meta">${g.seats} seat${g.seats === 1 ? '' : 's'}${status ? ` · ${status}` : ''}</span>
    ${lead ? html`<span class="meta">${roleName(lead.role, ch)}: ${lead.n}</span>` : ''}`;
}

// The President and the people who preside over each chamber, with their photos
// (scripts/update_congress.py).
function presiding(data) {
  const find = (ch, office) => data.chambers[ch].leaders.find((l) => l.office === office);
  return [
    ['President of the United States', data.president],
    ['Vice President, President of the Senate', find('senate', 'President')],
    ['Speaker of the House', find('house', 'Speaker')],
    ['President pro tempore of the Senate', find('senate', 'President pro tempore')],
  ].filter(([, p]) => p);
}

function officials(data) {
  const person = (title, p) => html`<div class="parl-person">
      ${candBadge(p, PARTY_COLOR[p.party] || 'var(--seat-other)')}
      <div><div class="eyebrow">${title}</div><b>${p.name}</b>
        <div class="small muted">${[PARTY_NAME[p.party], p.since && `since ${fmtDate(p.since)}`].filter(Boolean).join(' · ')}</div></div>
    </div>`;
  return html`<section class="card stack">
    <div><h2 style="margin:0">Who leads</h2>
      <p class="small muted" style="margin:4px 0 0">The Vice President presides over the Senate and votes only to break a tie. The Speaker, elected by the House, leads it. After the Vice President, the Speaker and then the President pro tempore are next in line to the presidency.</p></div>
    <div class="parl-people">${presiding(data).map(([title, p]) => person(title, p))}</div>
  </section>`;
}

function stats(ch, chamber) {
  const filled = chamber.members.length, vacant = chamber.seats - filled;
  const tile = (label, value, sub) => html`<div class="stat"><div class="eyebrow">${label}</div><div class="value">${value}</div>${sub ? html`<div class="sub">${sub}</div>` : ''}</div>`;
  const side = (p) => {
    const own = chamber.members.filter((m) => m.party === p).length;
    const allied = chamber.members.filter((m) => m.g === `I-${p}`).length;
    return tile(SIDE[p], own, allied ? `plus ${allied} independent${allied > 1 ? 's who caucus' : ' who caucuses'} with them` : '');
  };
  const up = chamber.members.filter((m) => m.up === 2026);
  const specials = up.filter((m) => m.cls !== 2).length;
  return html`<div class="parl-stats">
    ${tile('Seats', chamber.seats, vacant > 0 ? `${filled} filled, ${vacant} vacant` : 'All filled')}
    ${tile('Majority', chamber.majority, ch === 'senate' ? 'or 50 and the Vice President’s tie-breaking vote' : `of the ${chamber.seats} seats`)}
    ${tile('Control', SIDE[chamber.control] || '—', '')}
    ${side('D')}
    ${side('R')}
    ${ch === 'senate'
      ? tile(before() ? 'On the ballot' : 'Were on the ballot', up.length, `November 3, 2026${specials ? `, ${specials} of them special elections` : ''}`)
      : tile(before() ? 'On the ballot' : 'Were on the ballot', chamber.seats, 'Every seat, November 3, 2026')}
  </div>`;
}

function leadersList(ch, chamber) {
  return html`<dl class="kv">${chamber.leaders.filter((l) => l.office !== 'President').map((l) => html`<dt>${l.office}</dt>
    <dd>${l.name} (${l.party})${l.since ? html` <span class="faint" style="font-weight:400;white-space:nowrap">since ${fmtDate(l.since)}</span>` : ''}</dd>`)}</dl>`;
}

function membersList(ch, chamber, groups) {
  const byId = new Map(groups.map((g) => [g.id, g]));
  const rows = [...chamber.members].sort((a, b) => stateName(a.st).localeCompare(stateName(b.st)) || (a.d || 0) - (b.d || 0) || a.n.localeCompare(b.n));
  return html`<details class="card" id="parl-list">
    <summary style="cursor:pointer;font-weight:650">All ${rows.length} ${ch === 'senate' ? 'senators' : 'representatives'}, by state</summary>
    <div class="stack" style="margin-top:12px">
      <div class="row"><input class="input parl-find" id="parl-find" type="search" autocomplete="off" placeholder="Name, state, party…" aria-label="Search the list">
        <span class="small muted" id="parl-count" aria-live="polite"></span></div>
      <div class="table-wrap"><table class="data parl-members">
        <thead><tr><th>Name</th><th>Party</th><th>${ch === 'senate' ? 'State' : 'District'}</th><th>Region</th><th>2026 race</th></tr></thead>
        <tbody>${rows.map((m) => {
          const id = raceId(m, ch);
          const race = (ch === 'house' || m.up === 2026) && getRace(id);
          return html`<tr data-q="${fold([m.n, partyLabel(m), stateName(m.st), m.st, m.reg, m.role].join(' '))}">
            <td><b>${m.n}</b>${m.role ? html`<div class="tiny faint">${roleName(m.role, ch)}</div>` : ''}</td>
            <td>${swatch(byId.get(m.g), 12)} ${partyLabel(m)}</td>
            <td>${seatName(m, ch)}</td><td>${m.reg || '—'}</td>
            <td>${race ? html`<a href="#/race/${id}">${ch === 'senate' ? `${stateName(m.st)} Senate` : `${m.st}-${m.d || 'AL'}`}</a>`
              : html`<span class="faint">${m.up ? `Next up in ${m.up}` : '—'}</span>`}</td></tr>`;
        })}</tbody>
      </table></div>
    </div>
  </details>`;
}

const INTRO = {
  house: () => `Each of the 435 voting members represents one district (seats are shared out among the states by population) and serves a two-year term. ${before()
    ? `Every seat is on the ballot on ${ELECTION_DATE_LABEL}.`
    : 'Every seat was on the ballot on November 3, 2026; the winners take office on January 3, 2027.'} Bills that raise revenue must start in the House, and only the House can impeach. Non-voting members represent the District of Columbia, Puerto Rico and four territories.`,
  senate: (chamber) => {
    const up = chamber.members.filter((m) => m.up === 2026);
    const specials = up.filter((m) => m.cls !== 2).map((m) => stateName(m.st)).sort();
    return `Each state elects two senators, who serve six-year terms; about a third of the seats come up every two years. ${up.length} seats ${before() ? `are on the ballot on ${ELECTION_DATE_LABEL}` : 'were on the ballot on November 3, 2026'}${specials.length ? `, including special elections in ${list(specials)}` : ''}. The Senate confirms the President’s nominees, approves treaties and holds impeachment trials.`;
  },
};

function houseNotes(chamber) {
  return html`<div class="stack-sm">
    ${chamber.vacancies.length ? html`<div><div class="eyebrow" style="margin-bottom:6px">Vacant seats</div>
      <ul class="small" style="margin:0;padding-left:18px">${chamber.vacancies.map((v) => html`<li><b>${seatName(v, 'house')}</b>${v.note ? `: ${v.note}` : ''}</li>`)}</ul></div>` : ''}
    <div><div class="eyebrow" style="margin-bottom:6px">Non-voting members</div>
      <ul class="small" style="margin:0;padding-left:18px">${chamber.delegates.map((d) => html`<li>${d.n} (${d.party}), ${d.where}${d.st === 'PR' ? ' (resident commissioner)' : ''}</li>`)}</ul></div>
  </div>`;
}

function senateNotes(chamber) {
  const allied = chamber.members.filter((m) => m.party === 'I');
  const sides = [...new Set(allied.map((m) => SIDE[m.g?.split('-')[1]]))];
  const who = list(allied.map((m) => `${m.n} (${stateName(m.st)})`));
  return html`<p class="small muted" style="margin:0">${allied.length
    ? `${allied.length === 1 ? 'Independent' : 'Independents'} ${who} ${sides.length === 1 && sides[0] ? `caucus${allied.length === 1 ? 'es' : ''} with the ${sides[0]}` : 'sit in the Senate'}. `
    : ''}A 50–50 Senate is run by the Vice President’s party, since the Vice President breaks ties.</p>`;
}

export const congress = {
  title: () => 'U.S. Congress',
  async render(ctx) {
    const data = await load();
    if (!data) return html`<div class="wrap page"><div class="empty">${icon.info()}<h3>Congress data is unavailable</h3><p>Run scripts/update_congress.py to build it.</p></div></div>`;
    const ch = ctx.query.chamber === 'senate' ? 'senate' : 'house';
    const chamber = data.chambers[ch];
    const groups = groupsOf(chamber);
    const sources = [...chamber.sources, ...(data.president?.source ? [{ title: 'Wikidata (President)', url: data.president.source }] : [])];
    return html`<div class="wrap page stack-lg">
      <div><div class="eyebrow">U.S. Congress${data.congress ? ` · ${ordinal(data.congress)} Congress${data.session ? `, ${ordinal(+data.session)} session` : ''}` : ''}</div>
        <h1 style="margin:6px 0 8px">Who sits in Congress</h1>
        <p class="muted" style="margin:0">Congress has two chambers, the House of Representatives and the Senate. Each dot is a seat, colored by its holder’s party: Democrats blue, Republicans red, independents gray. Hover over or tap a seat to see who holds it. The member lists are reread every day; last updated ${fmtDate(data.updated)}.</p></div>
      <nav class="seg big" aria-label="Chamber">
        <a href="#/congress" aria-current="${ch === 'house' ? 'page' : 'false'}">House of Representatives</a>
        <a href="#/congress?chamber=senate" aria-current="${ch === 'senate' ? 'page' : 'false'}">Senate</a>
      </nav>
      ${officials(data)}
      <section class="card stack">
        <div><h2 style="margin:0">${ch === 'senate' ? 'Senate' : 'House of Representatives'}</h2>
          <p class="small muted" style="margin:4px 0 0">${INTRO[ch](chamber)}</p></div>
        <div id="parl-hemi"></div>
        ${stats(ch, chamber)}
        <div class="grid grid-2" style="gap:18px;align-items:start">
          <div><div class="eyebrow" style="margin-bottom:8px">Leaders</div>${leadersList(ch, chamber)}</div>
          ${ch === 'house' ? houseNotes(chamber) : senateNotes(chamber)}
        </div>
      </section>
      ${membersList(ch, chamber, groups)}
      ${data.checks?.length ? html`<div class="notice warn">${icon.info()}<div><b>Differences between sources, to be checked</b><ul style="margin:6px 0 0">${data.checks.map((c) => html`<li>${c}</li>`)}</ul></div></div>` : ''}
      <p class="tiny faint" style="margin:0">Sources: ${sources.map((s, i) => html`${i ? ' · ' : ''}<a href="${s.url}" target="_blank" rel="noopener noreferrer">${s.revid ? `Wikipedia: ${s.title}` : s.title}</a>${!s.revid && chamber.published && s.url.includes('clerk.house.gov') ? ` (dated ${chamber.published})` : ''}`)}</p>
      ${photoCredits(presiding(data).map(([, p]) => p))}
    </div>`;
  },
  async mount(root, ctx) {
    const data = await load();
    const host = root.querySelector('#parl-hemi');
    if (!data || !host) return null;
    const ch = ctx.query.chamber === 'senate' ? 'senate' : 'house';
    const chamber = data.chambers[ch];
    const groups = groupsOf(chamber);
    const byId = new Map(groups.map((g) => [g.id, g]));
    const vacant = chamber.seats - chamber.members.length;
    const chart = drawHemicycle(host, {
      seats: chamber.seats,
      groups,
      members: chamber.members,
      tipFor: (m) => tip(m, ch, byId.get(m.g)),
      vacantTip: (i) => {
        const v = chamber.vacancies?.[i];
        return html`<div class="tt-title">Vacant seat</div>${v ? html`<div class="tt-sub">${seatName(v, ch)}</div>${v.note ? html`<div class="small" style="margin-top:4px;max-width:260px">${v.note}</div>` : ''}` : ''}`;
      },
      ariaLabel: `${ch === 'senate' ? 'Senate' : 'House of Representatives'}: ${chamber.seats} seats. ${groups.map((g) => `${g.name} ${g.seats}`).join(', ')}${vacant > 0 ? `, ${vacant} vacant` : ''}.`,
      hint: 'Hover over or tap a seat to see who holds it. With the keyboard, the arrow keys move from seat to seat and Page Up and Page Down jump between parties.',
      center: [String(chamber.seats), 'seats', `majority: ${chamber.majority}`],
      legendItem: (g) => keyItem(g, chamber, ch),
      legendLabel: 'Key: parties',
    });

    const find = root.querySelector('#parl-find');
    const count = root.querySelector('#parl-count');
    const rows = [...root.querySelectorAll('#parl-list tbody tr')];
    find?.addEventListener('input', () => {
      const q = fold(find.value.trim());
      let n = 0;
      for (const r of rows) {
        const hit = !q || r.dataset.q.includes(q);
        r.hidden = !hit;
        if (hit) n += 1;
      }
      count.textContent = q ? `${n} result${n === 1 ? '' : 's'}` : '';
    });
    return () => chart.destroy();
  },
};
