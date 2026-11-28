// The U.S. Congress: the House and the Senate as half-circle seat charts
// (js/components/hemicycle.js). After the 2026 election the page opens on the 120th
// Congress, which meets on January 3, 2027: each House district's 2026 winner and each
// state's two senators (js/data/holders.js), with the seats not decided yet left hollow.
// A switch shows the 119th Congress sitting now (data/congress.json, the House Clerk's
// member list, English Wikipedia and Wikidata, reread every day by
// scripts/update_congress.py).
//
// Every seat wears its party's color: Democrats blue, Republicans red, independents gray
// (owner's request, Nov. 27, 2026, after a day of shading by score). Each party's seats
// run from its most moderate members, nearest the middle, to those furthest left or right,
// on the outer edge, by left-right score: DW-NOMINATE's first dimension from Voteview,
// built from every roll call a member has cast (scripts/lib/nominate.py, `nom` in
// data/congress.json); members with no score yet sit in the middle of their party. The
// score itself is no longer shown anywhere (owner's request, Nov. 28, 2026: "remove this
// altogether as it's more complicated than necessary. The seat order can stay"). The
// caucus buttons above the chart (same request: "showing the different caucuses by
// highlighting the individuals a part of them") light up one caucus's members wherever
// they sit and narrow the member list to them; a member can belong to several
// (caucusesOf in holders.js: each caucus's own roster where it publishes one, else
// Wikipedia's list).

import { html, fetchJSON, ordinal } from '../util.js';
import { icon } from '../icons.js';
import { L } from '../i18n.js';
import { STATES, stateName } from '../data/states.js';
import { ELECTION_DAY } from '../model/forecast.js';
import { getRace, houseRaces, resultsIn, resultMargin, allCertified } from '../data/world.js';
import { loadHolders, senatorsOf, fromRace, caucusesOf, caucusDefs, lastNameOf } from '../data/holders.js';
import { drawHemicycle, swatch } from '../components/hemicycle.js';
import { candBadge, photoCredits } from '../components/race.js';
import { dateL } from '../components/person.js';

let cache = null;
async function load() {
  try { cache = cache || await fetchJSON('data/congress.json'); } catch { cache = null; }
  return cache;
}

const partyKey = (p) => (p === 'D' || p === 'R' ? p : 'I');
const COLOR = { D: 'var(--dem)', R: 'var(--rep)', I: 'var(--seat-other)' };
const PARTY_NAME = { D: ['Démocrate', 'Democrat'], R: ['Républicain', 'Republican'], I: ['Indépendant', 'Independent'] };
const SIDE = { D: ['les démocrates', 'Democrats'], R: ['les républicains', 'Republicans'] };
const SIDE_TITLE = { D: ['Démocrates', 'Democrats'], R: ['Républicains', 'Republicans'] };
const ordL = (n) => L(`${n}${n === 1 ? 're' : 'e'}`, ordinal(n));
const seatName = (m, ch) => (ch === 'senate' ? stateName(m.st)
  : m.d ? L(`${ordL(m.d)} circonscription, ${stateName(m.st)}`, `${stateName(m.st)}’s ${ordinal(m.d)} district`)
    : L(`${stateName(m.st)}, circonscription unique`, `${stateName(m.st)} at-large`));
const seatCode = (m) => `${m.st}-${m.d || 'AL'}`;
const raceIdOf = (m, ch) => (ch === 'senate' ? `${m.st}-SEN` : `${m.st}-H-${String(m.d || 0).padStart(2, '0')}`);
const before = () => new Date() < ELECTION_DAY;
const list = (items) => new Intl.ListFormat(L('fr', 'en'), { type: 'conjunction' }).format(items);
const fold = (s) => String(s || '').normalize('NFD').replace(/\p{Diacritic}/gu, '').toLowerCase();

// The caucuses the buttons highlight, in the owner's order.
const CAUCUSES = { D: ['dsa', 'cpc', 'bluedog', 'newdem'], R: ['freedom', 'mainstreet', 'governance', 'rsc'] };
const inCaucus = (m, id) => !!m?.caucuses?.some((c) => c.id === id);
// The caucus each chamber's chart highlights, kept while the page is redrawn (a language
// switch) and when the visitor comes back to that chamber.
const picked = {};

// One group per party, seated left to right: Democrats, independents, Republicans.
function groupsFor(members) {
  return ['D', 'I', 'R'].map((p) => {
    const seats = members.filter((m) => m.g === p).length;
    return seats ? { id: p, party: p, seats, shape: 'circle', color: COLOR[p], name: L(...COLUMN[p]), short: L(...COLUMN[p]) } : null;
  }).filter(Boolean);
}

// Left to right within each party by score, so each party's most moderate members sit
// nearest the middle (Democrats from the furthest left in, Republicans from the middle
// out); members with no score yet sit in the middle of their party. Sorted in place: the
// chart keeps this order within each group.
function byScore(members) {
  const out = [];
  for (const p of ['D', 'I', 'R']) {
    const own = members.filter((m) => m.party === p);
    own.forEach((m) => { m.g = p; });
    const scored = own.filter((m) => m.nom != null).sort((a, b) => a.nom - b.nom);
    const half = Math.floor(scored.length / 2);
    out.push(...scored.slice(0, half), ...own.filter((m) => m.nom == null), ...scored.slice(half));
  }
  members.splice(0, members.length, ...out);
  return members;
}

// A 120th Congress member's score: the 119th Congress member in the same seat's, else that
// of the one sitting member of either chamber, or recent former member (data/congress.json's
// "voteview"), from the same state with the same last name, party and first name. Anyone
// else is new to Congress and has none yet.
const firstNames = (name) => fold(name).replace(/\(.*?\)/g, ' ').split(/\s+/).slice(0, -1)
  .map((w) => w.replace(/[^a-z-]/g, '')).filter((w) => w.length > 1);
function scoreOf(p, st, data, d = null) {
  const last = lastNameOf(p.name);
  const { house, senate } = data.chambers;
  const same = d != null
    ? house.members.find((m) => m.st === st && (m.d || 0) === d && lastNameOf(m.n) === last)
    : senate.members.find((m) => m.st === st && lastNameOf(m.n) === last);
  if (same) return same.nom ?? null;
  const party = partyKey(p.party);
  const mine = firstNames(p.name);
  const sameFirst = (names) => names.some((f) => mine.some((g) => f.slice(0, 3) === g.slice(0, 3)));
  const hits = [
    ...[...house.members, ...senate.members].filter((m) => m.st === st && lastNameOf(m.n) === last && partyKey(m.party) === party && sameFirst(firstNames(m.n))),
    ...(data.voteview?.former || []).filter((m) => m.st === st && m.last === last && m.party === party && sameFirst(m.first)),
  ];
  return hits.length === 1 && hits[0].nom != null ? hits[0].nom : null;
}

// The 119th Congress, sitting now.
function sitting(data, ch) {
  const c = data.chambers[ch];
  const members = c.members.map((m) => {
    const wiki = m.article ? `https://en.wikipedia.org/wiki/${m.article.replace(/ /g, '_')}` : null;
    const seat = ch === 'house' ? `${m.st}-${String(m.d || 0).padStart(2, '0')}` : null;
    return { ...m, party: partyKey(m.party), side: m.g, caucuses: caucusesOf({ name: m.n, party: m.party, st: m.st, wiki, id: m.id }, { chamber: ch, seat, sitting: true }) };
  });
  return { which: 119, seats: c.seats, majority: c.majority, control: c.control, members: byScore(members), open: [], vacancies: c.vacancies || [] };
}

// The 120th Congress: the 2026 winners, the senators whose seats weren't up, and the seats
// still open (a runoff, a count, nothing posted yet).
function incoming(data, ch) {
  const members = [], open = [];
  const was = data.chambers[ch].members;
  for (const s of STATES) {
    if (s.abbr === 'DC') continue; // a non-voting delegate, listed under the chart
    if (ch === 'house') {
      for (const r of houseRaces(s.abbr)) {
        const p = fromRace(r);
        const d = parseInt(r.district, 10) || 0;
        if (p.status === 'elected') {
          const old = was.find((m) => m.st === s.abbr && (m.d || 0) === d && lastNameOf(m.n) === lastNameOf(p.name))
            || was.find((m) => m.st === s.abbr && lastNameOf(m.n) === lastNameOf(p.name));
          members.push({ n: p.name, party: partyKey(p.party), st: s.abbr, d, person: p, race: r.id, flip: p.flip, inc: p.incumbent,
            side: old?.g, nom: scoreOf(p, s.abbr, data, d), caucuses: caucusesOf(p, { chamber: 'house', seat: `${s.abbr}-${r.district}`, sitting: false }) });
        } else open.push({ st: s.abbr, d, race: r.id, p });
      }
    } else {
      for (const p of senatorsOf(s.abbr)) {
        if (p.status === 'elected' || p.status === 'holder') {
          const old = was.find((m) => m.st === s.abbr && lastNameOf(m.n) === lastNameOf(p.name));
          members.push({ n: p.name, party: partyKey(p.party), st: s.abbr, person: p, race: p.status === 'elected' ? p.raceId : null,
            up: p.up, since: p.since, flip: p.flip, inc: p.incumbent, side: old?.g, held: p.status === 'holder',
            nom: scoreOf(p, s.abbr, data), caucuses: caucusesOf(p, { chamber: 'senate', seat: null, sitting: p.status === 'holder' }) });
        } else open.push({ st: s.abbr, race: p.raceId, p });
      }
    }
  }
  byScore(members);
  const seats = ch === 'house' ? 435 : 100;
  const majority = ch === 'house' ? 218 : 51;
  const sideOf = (m) => (m.party === 'I' ? (m.side || '').split('-')[1] || null : m.party);
  const d = members.filter((m) => sideOf(m) === 'D').length;
  const r = members.filter((m) => sideOf(m) === 'R').length;
  // A 50-50 Senate goes to the Vice President's party.
  const vp = data.chambers.senate.leaders.find((l) => l.office === 'President')?.party;
  const control = d >= majority ? 'D' : r >= majority ? 'R'
    : ch === 'senate' && !open.length && d === 50 && r === 50 && vp ? vp : null;
  return { which: 120, seats, majority, control, members, open, vacancies: [] };
}

// "Majority Leader" becomes "House Majority Leader"; the presiding officers keep their titles.
const ROLE_FR = { Speaker: 'Président de la Chambre', 'Majority Leader': 'chef de la majorité', 'Minority Leader': 'chef de la minorité',
  'Majority Whip': 'whip de la majorité', 'Minority Whip': 'whip de la minorité', President: 'Président du Sénat', 'President pro tempore': 'Président pro tempore du Sénat' };
function roleName(role, ch) {
  if (role === 'Speaker') return L(ROLE_FR.Speaker, 'Speaker of the House');
  if (role === 'President') return L(ROLE_FR.President, 'President of the Senate');
  if (role === 'President pro tempore') return L(ROLE_FR['President pro tempore'], 'President pro tempore of the Senate');
  return L(`${ROLE_FR[role] ? ROLE_FR[role].replace(/^./, (c) => c.toUpperCase()) : role} (${ch === 'senate' ? 'Sénat' : 'Chambre'})`, `${ch === 'senate' ? 'Senate' : 'House'} ${role}`);
}

// An independent's side is a fact of the 119th Congress; for someone elected in 2026 the
// page says so rather than assume the 120th.
function partyLabel(m) {
  if (m.party !== 'I') return L(...PARTY_NAME[m.party]);
  const side = SIDE[(m.side || '').split('-')[1]];
  if (!side) return L(...PARTY_NAME.I);
  return m.race ? L(`Indépendant (siégeait avec ${side[0]} au 119e Congrès)`, `Independent (caucused with ${side[1]} in the 119th Congress)`)
    : L(`Indépendant (siège avec ${side[0]})`, `Independent (caucuses with ${side[1]})`);
}

function statusLine(m, model) {
  if (model.which === 119) return m.since ? L(`Au Sénat depuis le ${dateL(m.since)}`, `Senator since ${dateL(m.since)}`) : '';
  if (m.held) return L(`En fonction ; siège en jeu en ${m.up}`, `In office; seat up in ${m.up}`);
  return m.inc ? L('Réélection le 3 novembre 2026', 'Re-elected Nov. 3, 2026') : L('Élection le 3 novembre 2026', 'Elected Nov. 3, 2026');
}

// The caucus row: every caucus a member belongs to. In the House a member of a party with
// caucus lists who is in none says so; the Senate shows the row only for its one member
// on a list (the Progressive Caucus counts a senator).
function caucusRow(m, ch) {
  const names = (m.caucuses || []).map((c) => c.short);
  if (!names.length && (ch === 'senate' || m.party === 'I')) return '';
  return html`<div class="t-row"><span>${names.length > 1 ? L('Caucus', 'Caucuses') : L('Caucus', 'Caucus')}</span><b>${names.length ? list(names) : L('Aucun de ces caucus', 'None of these caucuses')}</b></div>`;
}

function tip(m, ch, g, model, caucuses) {
  const line = statusLine(m, model);
  return html`<div class="tt-title">${m.n}</div>
    ${m.role ? html`<div class="tt-sub">${roleName(m.role, ch)}</div>` : line ? html`<div class="tt-sub">${line}</div>` : ''}
    <div class="t-row"><span>${L('Parti', 'Party')}</span><b>${swatch(g, 12)}${partyLabel(m)}</b></div>
    ${caucuses ? caucusRow(m, ch) : ''}
    <div class="t-row"><span>${ch === 'senate' ? L('État', 'State') : L('Circonscription', 'District')}</span><b>${seatName(m, ch)}</b></div>
    ${m.flip ? html`<div class="t-row"><span>${L('Siège', 'Seat')}</span><b>${L('Gagné sur l’autre parti en 2026', 'Flipped in 2026')}</b></div>` : ''}
    ${model.which === 119 && m.up ? html`<div class="t-row"><span>${L('Siège en jeu', 'Seat on the ballot')}</span><b>${m.up === 2026 ? dateL('2026-11-03') : m.up}</b></div>` : ''}`;
}

// What a seat not decided yet is waiting for.
function openLine(o) {
  const p = o.p;
  if (p.status === 'runoff') {
    const names = (p.advancing || []).map((c) => `${c.name} (${partyKey(c.party)})`).join(L(' et ', ' and '));
    return L(`Second tour${p.date ? ` le ${dateL(p.date)}` : ''}${names ? ` : ${names}` : ''}`, `Runoff${p.date ? ` on ${dateL(p.date)}` : ''}${names ? `: ${names}` : ''}`);
  }
  if (p.status === 'uncalled') {
    const lead = p.leader || (o.race && resultMargin(getRace(o.race))?.a);
    return lead ? L(`Pas encore proclamé ; ${lead.name} (${partyKey(lead.party)}) en tête`, `Not called yet; ${lead.name} (${partyKey(lead.party)}) leads`) : L('Pas encore proclamé', 'Not called yet');
  }
  return L('Pas encore de résultat publié', 'No result posted yet');
}

// The key: each party's seats.
function keyItem(g) {
  return html`<span><b>${g.short}</b></span><span class="meta">${L(`${g.seats} siège${g.seats === 1 ? '' : 's'}`, `${g.seats} seat${g.seats === 1 ? '' : 's'}`)}</span>`;
}

// The caucus buttons: each caucus with members in this chamber, Democrats' then
// Republicans', with how many of them sit here.
function caucusPicker(model, ch) {
  const defs = caucusDefs();
  const count = (id) => model.members.filter((m) => inCaucus(m, id)).length;
  const shown = ['D', 'R'].flatMap((p) => CAUCUSES[p]).map((id) => defs.find((d) => d.id === id)).filter((d) => d && count(d.id));
  if (!shown.length) return '';
  return html`<div class="parl-caucuses">
    <div class="eyebrow" id="parl-caucus-label">${L('Mettre en évidence les membres d’un caucus', 'Highlight a caucus’s members')}</div>
    <div class="filters" role="group" aria-labelledby="parl-caucus-label">${shown.map((d) => html`<button type="button" class="chip parl-caucus" data-c="${d.id}" aria-pressed="false" title="${d.name}">${swatch({ color: COLOR[d.party], shape: 'circle' }, 11)}${d.short} <b>${count(d.id)}</b></button>`)}</div>
    <p class="tiny faint" style="margin:0" id="parl-caucus-note" aria-live="polite">${ch === 'senate'
      ? L('Ces caucus sont des groupes de la Chambre ; seul le Progressive Caucus compte aussi un sénateur.', 'These caucuses are House groups; only the Progressive Caucus also counts a senator.')
      : L('Un membre peut appartenir à plusieurs caucus. Touchez un caucus pour éclairer ses membres, encore une fois pour tout revoir.', 'A member can belong to several caucuses. Tap one to light up its members, and again to see everyone.')}</p>
  </div>`;
}

// The President and the people who preside over each chamber, with their photos
// (scripts/update_congress.py).
function presiding(data) {
  const find = (ch, office) => data.chambers[ch].leaders.find((l) => l.office === office);
  return [
    [L('Président des États-Unis', 'President of the United States'), data.president],
    [L('Vice-président, président du Sénat', 'Vice President, President of the Senate'), find('senate', 'President')],
    [L('Président de la Chambre des représentants', 'Speaker of the House'), find('house', 'Speaker')],
    [L('Président pro tempore du Sénat', 'President pro tempore of the Senate'), find('senate', 'President pro tempore')],
  ].filter(([, p]) => p);
}

function officials(data, model) {
  const person = (title, p) => html`<div class="parl-person">
      ${candBadge(p, COLOR[partyKey(p.party)])}
      <div><div class="eyebrow">${title}</div><b>${p.name}</b>
        <div class="small muted">${[L(...PARTY_NAME[partyKey(p.party)]), p.since && L(`depuis le ${dateL(p.since)}`, `since ${dateL(p.since)}`)].filter(Boolean).join(' · ')}</div></div>
    </div>`;
  return html`<section class="card stack">
    <div><h2 style="margin:0">${L('Qui dirige', 'Who leads')}</h2>
      <p class="small muted" style="margin:4px 0 0">${L('Le vice-président préside le Sénat et ne vote que pour départager une égalité. Le président de la Chambre (Speaker), élu par elle, la dirige. Après le vice-président, le Speaker puis le président pro tempore sont les suivants dans l’ordre de succession à la présidence.', 'The Vice President presides over the Senate and votes only to break a tie. The Speaker, elected by the House, leads it. After the Vice President, the Speaker and then the President pro tempore are next in line to the presidency.')}
      ${model.which === 120 ? html` <b>${L('Le 120e Congrès élit son Speaker et son président pro tempore quand il se réunit le 3 janvier 2027 ; ceux montrés ici sont ceux du 119e.', 'The 120th Congress elects its Speaker and President pro tempore when it meets on January 3, 2027; the ones shown are the 119th Congress’s.')}</b>` : ''}</p></div>
    <div class="parl-people">${presiding(data).map(([title, p]) => person(title, p))}</div>
  </section>`;
}

function stats(ch, model) {
  const { members, open } = model;
  const tile = (label, value, sub) => html`<div class="stat"><div class="eyebrow">${label}</div><div class="value">${value}</div>${sub ? html`<div class="sub">${sub}</div>` : ''}</div>`;
  const side = (p) => {
    const own = members.filter((m) => m.party === p).length;
    const allied = members.filter((m) => m.party === 'I' && (m.side || '').endsWith(`-${p}`)).length;
    return tile(L(...SIDE_TITLE[p]), own, allied ? L(`plus ${allied} indépendant${allied > 1 ? 's' : ''} qui siège${allied > 1 ? 'nt' : ''} avec eux`, `plus ${allied} independent${allied > 1 ? 's who caucus' : ' who caucuses'} with them`) : '');
  };
  const control = model.control ? L(...SIDE_TITLE[model.control]) : L('Pas encore fixé', 'Not settled yet');
  if (model.which === 120) {
    const flips = members.filter((m) => m.flip).length;
    return html`<div class="parl-stats">
      ${tile(L('Sièges', 'Seats'), model.seats, open.length ? L(`${members.length} pourvus, ${open.length} pas encore décidés`, `${members.length} decided, ${open.length} not yet`) : L('Tous décidés', 'All decided'))}
      ${tile(L('Majorité', 'Majority'), model.majority, ch === 'senate' ? L('ou 50 et la voix du vice-président', 'or 50 and the Vice President’s tie-breaking vote') : L(`des ${model.seats} sièges`, `of the ${model.seats} seats`))}
      ${tile(L('Contrôle en janvier 2027', 'Control from January 2027'), control, '')}
      ${side('D')}
      ${side('R')}
      ${tile(L('Sièges qui ont changé de parti', 'Seats that changed parties'), flips, L('le 3 novembre 2026', 'on November 3, 2026'))}
    </div>`;
  }
  const filled = members.length, vacant = model.seats - filled;
  const up = members.filter((m) => m.up === 2026);
  const specials = up.filter((m) => m.cls !== 2).length;
  return html`<div class="parl-stats">
    ${tile(L('Sièges', 'Seats'), model.seats, vacant > 0 ? L(`${filled} pourvus, ${vacant} vacants`, `${filled} filled, ${vacant} vacant`) : L('Tous pourvus', 'All filled'))}
    ${tile(L('Majorité', 'Majority'), model.majority, ch === 'senate' ? L('ou 50 et la voix du vice-président', 'or 50 and the Vice President’s tie-breaking vote') : L(`des ${model.seats} sièges`, `of the ${model.seats} seats`))}
    ${tile(L('Contrôle', 'Control'), control, '')}
    ${side('D')}
    ${side('R')}
    ${ch === 'senate'
      ? tile(before() ? L('En jeu', 'On the ballot') : L('Étaient en jeu', 'Were on the ballot'), up.length, L(`le 3 novembre 2026${specials ? `, dont ${specials} élection${specials > 1 ? 's' : ''} partielle${specials > 1 ? 's' : ''}` : ''}`, `November 3, 2026${specials ? `, ${specials} of them special elections` : ''}`))
      : tile(before() ? L('En jeu', 'On the ballot') : L('Étaient en jeu', 'Were on the ballot'), model.seats, L('Tous les sièges, le 3 novembre 2026', 'Every seat, November 3, 2026'))}
  </div>`;
}

const COLUMN = { D: ['Démocrates', 'Democrats'], I: ['Indépendants', 'Independents'], R: ['Républicains', 'Republicans'] };
const partySeats = (groups, p) => groups.filter((g) => g.party === p).reduce((s, g) => s + g.seats, 0);

// How the seats are ordered, in plain words (the score itself isn't shown: owner's request,
// Nov. 28, 2026), and where the caucus lists come from: each caucus's own roster where it
// publishes one, else Wikipedia's list.
function seatNote() {
  const defs = caucusDefs();
  const link = (d) => (d.source?.url ? html`<a href="${d.source.url}" target="_blank" rel="noopener noreferrer">${d.short}</a>` : d.short);
  const series = (list, linked = true) => list.map((d) => (linked ? link(d) : d.short))
    .flatMap((x, i) => (i === 0 ? [x] : [i === list.length - 1 ? L(' et ', ' and ') : ', ', x]));
  const shown = [...CAUCUSES.D, ...CAUCUSES.R].map((id) => defs.find((d) => d.id === id)).filter(Boolean);
  const own = shown.filter((d) => d.fromRoster), wiki = shown.filter((d) => !d.fromRoster);
  const pac = own.some((d) => d.id === 'governance'), partial = wiki.some((d) => d.id === 'rsc');
  // The two caucuses that publish no member list (checked Nov. 28, 2026); the DSA's members
  // in Congress come from Wikipedia too, but that says nothing about what the DSA publishes.
  const none = wiki.filter((d) => d.id === 'freedom' || d.id === 'rsc');
  return html`<p class="tiny faint" style="margin:0">${L('Ordre des sièges dans chaque parti : les votes nominatifs des membres, d’après ', 'Seat order within each party: members’ roll-call votes, from ')}<a href="https://voteview.com/" target="_blank" rel="noopener noreferrer">Voteview</a>${L(
    ' ; ceux qui votent contre les textes de leur parti parce qu’ils ne vont pas assez loin siègent plus près du centre, et les nouveaux venus au centre de leur parti.',
    '; members who vote against their party’s bills for not going far enough sit nearer the middle, and newcomers in the middle of their party.')}
    ${shown.length ? html`${L(' Membres des caucus : ', ' Caucus members: ')}${own.length ? html`${L('la liste que publie chaque caucus pour ', 'each caucus’s own published list for ')}${series(own)}${pac ? L(' (celle de son PAC pour le Governance Group)', ' (its PAC’s, for the Governance Group)') : ''}` : ''}${own.length && wiki.length ? L(' ; ', '; ') : ''}${wiki.length ? html`${L('celles de Wikipédia pour ', 'Wikipedia’s for ')}${series(wiki)}${none.length ? html` (${series(none, false)}${none.length > 1 ? L(' ne publient pas de liste', ' publish no list') : L(' ne publie pas de liste', ' publishes no list')}${partial ? L(' ; Wikipédia ne nomme qu’une partie des membres du Study Committee', '; Wikipedia names only some of the Study Committee’s members') : ''})` : ''}` : ''}${L('. Les membres élus viennent des listes de Wikipédia jusqu’à ce que les caucus les ajoutent.', '. Members-elect come from Wikipedia’s lists until the caucuses add them.')}` : ''}</p>`;
}

function leadersList(ch, data) {
  const chamber = data.chambers[ch];
  return html`<dl class="kv">${chamber.leaders.filter((l) => l.office !== 'President').map((l) => html`<dt>${roleName(l.office, ch)}</dt>
    <dd>${l.name} (${partyKey(l.party)})${l.since ? html` <span class="faint" style="font-weight:400;white-space:nowrap">${L(`depuis le ${dateL(l.since)}`, `since ${dateL(l.since)}`)}</span>` : ''}</dd>`)}</dl>`;
}

function membersList(ch, model, groups) {
  const byId = new Map(groups.map((g) => [g.id, g]));
  const rows = [...model.members].sort((a, b) => stateName(a.st).localeCompare(stateName(b.st), L('fr', 'en')) || (a.d || 0) - (b.d || 0) || a.n.localeCompare(b.n));
  const caucusNames = (m) => (m.caucuses || []).map((c) => c.short);
  const who = ch === 'senate' ? L('sénateurs', 'senators') : L('représentants', 'representatives');
  return html`<details class="card" id="parl-list">
    <summary style="cursor:pointer;font-weight:650">${L(`Les ${rows.length} ${who}, par État`, `All ${rows.length} ${who}, by state`)}</summary>
    <div class="stack" style="margin-top:12px">
      <div class="row"><input class="input parl-find" id="parl-find" type="search" autocomplete="off" placeholder="${L('Nom, État, parti, caucus…', 'Name, state, party, caucus…')}" aria-label="${L('Chercher dans la liste', 'Search the list')}">
        <span class="small muted" id="parl-count" aria-live="polite"></span></div>
      <div class="table-wrap"><table class="data parl-members">
        <thead><tr><th>${L('Nom', 'Name')}</th><th>${L('Parti', 'Party')}</th><th>${L('Caucus', 'Caucuses')}</th><th>${ch === 'senate' ? L('État', 'State') : L('Circonscription', 'District')}</th><th>${L('Élection de 2026', '2026 race')}</th></tr></thead>
        <tbody>${rows.map((m) => {
          const g = byId.get(m.g);
          const id = m.race || raceIdOf(m, ch);
          const race = (model.which === 120 ? !!m.race : (ch === 'house' || m.up === 2026)) && getRace(id);
          // In the 120th Congress a name opens the member's card on their state page: their
          // positions, "Compare with my views" and, for the 2026 winners, their campaign money.
          const card = model.which === 120 && m.st !== 'DC'
            ? (ch === 'senate' ? `#/state/${m.st}?level=federal&chamber=senate` : `#/state/${m.st}?level=federal&chamber=house&d=${String(m.d || 0).padStart(2, '0')}`) : null;
          return html`<tr data-q="${fold([m.n, partyLabel(m), ...(m.caucuses || []).flatMap((c) => [c.short, c.name]), stateName(m.st), m.st, m.reg, m.role].join(' '))}" data-c="${(m.caucuses || []).map((c) => c.id).join(' ')}">
            <td><b>${card ? html`<a href="${card}" title="${L('Voir sa fiche : positions et argent de campagne', 'See their card: positions and campaign money')}">${m.n}</a>` : m.n}</b>${m.role ? html`<div class="tiny faint">${roleName(m.role, ch)}</div>` : ''}</td>
            <td style="white-space:nowrap">${g ? swatch(g, 12) : ''} ${partyLabel(m)}</td>
            <td>${caucusNames(m).length ? list(caucusNames(m)) : '—'}</td>
            <td>${seatName(m, ch)}</td>
            <td>${race ? html`<a href="#/race/${id}">${ch === 'senate' ? L(`Sénat, ${stateName(m.st)}`, `${stateName(m.st)} Senate`) : seatCode(m)}</a>${m.flip ? html` <span class="tiny faint">${L('bascule', 'flip')}</span>` : ''}`
              : html`<span class="faint">${m.up ? L(`Prochaine élection en ${m.up}`, `Next up in ${m.up}`) : '—'}</span>`}</td></tr>`;
        })}</tbody>
      </table></div>
    </div>
  </details>`;
}

const INTRO = {
  house: (model) => L(
    `Chacun des 435 membres votants représente une circonscription (les sièges sont répartis entre les États selon leur population) pour un mandat de deux ans. ${model.which === 120 ? 'Tous les sièges étaient en jeu le 3 novembre 2026 ; les personnes élues prennent leurs fonctions le 3 janvier 2027.' : before() ? 'Tous les sièges sont en jeu le 3 novembre 2026.' : 'Tous les sièges étaient en jeu le 3 novembre 2026 ; les personnes élues prennent leurs fonctions le 3 janvier 2027.'} Les lois de finances commencent à la Chambre, et seule la Chambre peut mettre en accusation (impeachment). Des membres sans droit de vote représentent le district de Columbia, Porto Rico et quatre territoires.`,
    `Each of the 435 voting members represents one district (seats are shared out among the states by population) and serves a two-year term. ${model.which === 120 ? 'Every seat was on the ballot on November 3, 2026; the winners take office on January 3, 2027.' : before() ? 'Every seat is on the ballot on November 3, 2026.' : 'Every seat was on the ballot on November 3, 2026; the winners take office on January 3, 2027.'} Bills that raise revenue must start in the House, and only the House can impeach. Non-voting members represent the District of Columbia, Puerto Rico and four territories.`),
  senate: (model, data) => {
    const up = data.chambers.senate.members.filter((m) => m.up === 2026);
    const specials = up.filter((m) => m.cls !== 2).map((m) => stateName(m.st)).sort();
    return L(
      `Chaque État élit deux sénateurs pour six ans ; environ un tiers des sièges sont renouvelés tous les deux ans. ${up.length} sièges ${before() ? 'sont en jeu le 3 novembre 2026' : 'étaient en jeu le 3 novembre 2026'}${specials.length ? `, dont des élections partielles en ${list(specials)}` : ''}. Le Sénat confirme les nominations du président, approuve les traités et juge les procédures de destitution.`,
      `Each state elects two senators, who serve six-year terms; about a third of the seats come up every two years. ${up.length} seats ${before() ? 'are on the ballot on November 3, 2026' : 'were on the ballot on November 3, 2026'}${specials.length ? `, including special elections in ${list(specials)}` : ''}. The Senate confirms the President’s nominees, approves treaties and holds impeachment trials.`);
  },
};

function openList(model, ch) {
  if (!model.open.length) return '';
  return html`<div><div class="eyebrow" style="margin-bottom:6px">${L('Pas encore décidés', 'Not decided yet')}</div>
    <ul class="small" style="margin:0;padding-left:18px">${model.open.map((o) => html`<li><b>${o.race ? html`<a href="#/race/${o.race}">${seatName(o, ch)}</a>` : seatName(o, ch)}</b>${L(' : ', ': ')}${openLine(o)}</li>`)}</ul></div>`;
}

function houseNotes(data, model) {
  const chamber = data.chambers.house;
  if (model.which === 120) {
    const dc = houseRaces('DC')[0];
    const p = dc ? fromRace(dc) : null;
    return html`<div class="stack-sm">
      ${openList(model, 'house')}
      <div><div class="eyebrow" style="margin-bottom:6px">${L('Membres sans droit de vote', 'Non-voting members')}</div>
        <p class="small" style="margin:0">${p?.status === 'elected' ? L(`District de Columbia : ${p.name} (${partyKey(p.party)}), élection du 3 novembre 2026. `, `District of Columbia: ${p.name} (${partyKey(p.party)}), elected November 3, 2026. `) : ''}${L('Les délégués des cinq territoires, élus le même jour, ne sont pas encore dans les données du site ; ceux du 119e Congrès sont sur l’autre onglet.', 'The five territories’ delegates, elected the same day, aren’t in the site’s data yet; the 119th Congress’s are on the other tab.')}</p></div>
    </div>`;
  }
  return html`<div class="stack-sm">
    ${chamber.vacancies.length ? html`<div><div class="eyebrow" style="margin-bottom:6px">${L('Sièges vacants', 'Vacant seats')}</div>
      <ul class="small" style="margin:0;padding-left:18px">${chamber.vacancies.map((v) => html`<li><b>${seatName(v, 'house')}</b>${v.note ? html`${L(' : ', ': ')}<span lang="en">${v.note}</span>` : ''}</li>`)}</ul></div>` : ''}
    <div><div class="eyebrow" style="margin-bottom:6px">${L('Membres sans droit de vote', 'Non-voting members')}</div>
      <ul class="small" style="margin:0;padding-left:18px">${chamber.delegates.map((d) => html`<li>${d.n} (${d.party}), ${d.where}${d.st === 'PR' ? L(' (commissaire résident)', ' (resident commissioner)') : ''}</li>`)}</ul></div>
  </div>`;
}

function senateNotes(model) {
  const allied = model.members.filter((m) => m.party === 'I');
  const sides = [...new Set(allied.map((m) => (m.side || '').split('-')[1] || null))];
  const who = list(allied.map((m) => `${m.n} (${stateName(m.st)})`));
  const one = allied.length === 1;
  const side = sides.length === 1 && SIDE[sides[0]];
  return html`<div class="stack-sm">
    ${openList(model, 'senate')}
    <p class="small muted" style="margin:0">${allied.length
      ? L(`${one ? 'L’indépendant' : 'Les indépendants'} ${who} ${side ? `siège${one ? '' : 'nt'} avec ${side[0]}` : `siège${one ? '' : 'nt'} au Sénat`}. `,
        `${one ? 'Independent' : 'Independents'} ${who} ${side ? `caucus${one ? 'es' : ''} with the ${side[1]}` : 'sit in the Senate'}. `)
      : ''}${L('Un Sénat à 50-50 est dirigé par le parti du vice-président, qui départage les égalités.', 'A 50–50 Senate is run by the Vice President’s party, since the Vice President breaks ties.')}</p>
  </div>`;
}

function whichOf(ctx) {
  const after = resultsIn();
  return { after, which: after && ctx.query.congress !== '119' ? 120 : 119 };
}

export const congress = {
  title: () => L('Congrès des États-Unis', 'U.S. Congress'),
  async render(ctx) {
    const [data] = await Promise.all([load(), loadHolders()]);
    if (!data) return html`<div class="wrap page"><div class="empty">${icon.info()}<h3>${L('Données du Congrès indisponibles', 'Congress data is unavailable')}</h3><p>${L('Lancez scripts/update_congress.py pour les construire.', 'Run scripts/update_congress.py to build it.')}</p></div></div>`;
    const ch = ctx.query.chamber === 'senate' ? 'senate' : 'house';
    const { after, which } = whichOf(ctx);
    const model = which === 120 ? incoming(data, ch) : sitting(data, ch);
    const groups = groupsFor(model.members);
    const q = (o) => `#/congress${new URLSearchParams(Object.entries({ chamber: ch === 'senate' ? 'senate' : '', congress: '', ...o }).filter(([, v]) => v)).toString().replace(/^(?=.)/, '?')}`;
    const chamberLink = (c) => q({ chamber: c === 'senate' ? 'senate' : '', congress: which === 119 && after ? '119' : '' });
    const sources = [...data.chambers[ch].sources, ...(data.president?.source ? [{ title: 'Wikidata (President)', url: data.president.source }] : [])];
    const title = ch === 'senate' ? L('Sénat', 'Senate') : L('Chambre des représentants', 'House of Representatives');
    return html`<div class="wrap page stack-lg">
      <div><div class="eyebrow">${L('Congrès des États-Unis', 'U.S. Congress')} · ${which === 120
          ? L('120e Congrès, à partir du 3 janvier 2027', '120th Congress, from January 3, 2027')
          : data.congress ? L(`${data.congress}e Congrès${data.session ? `, ${data.session}e session` : ''}`, `${ordinal(data.congress)} Congress${data.session ? `, ${ordinal(+data.session)} session` : ''}`) : ''}</div>
        <h1 style="margin:6px 0 8px">${which === 120 ? L('Qui siégera au Congrès', 'Who will sit in Congress') : L('Qui siège au Congrès', 'Who sits in Congress')}</h1>
        <p class="muted" style="margin:0">${which === 120
          ? L('Les personnes élues le 3 novembre 2026 et les sénateurs dont le siège n’était pas en jeu, chambre par chambre. Chaque point est un siège, à la couleur du parti : démocrates en bleu, républicains en rouge, indépendants en gris. Dans chaque parti, les membres les plus modérés siègent au centre et les plus à gauche ou à droite sur le bord extérieur, selon leurs votes au Congrès ; les sièges vides ne sont pas encore décidés. Les boutons des caucus éclairent les membres de chacun. Survolez ou touchez un siège pour voir qui l’occupe. ' + (allCertified() ? 'Chaque État a certifié ses résultats.' : 'Résultats non officiels jusqu’à leur certification par chaque État.'),
            'The people elected on November 3, 2026 and the senators whose seats weren’t up, chamber by chamber. Each dot is a seat in its holder’s party color: Democrats blue, Republicans red, independents gray. Within each party, the most moderate members sit nearest the middle and those furthest left or right on the outer edge, by how they’ve voted in Congress; hollow seats aren’t decided yet. The caucus buttons light up each caucus’s members. Hover over or tap a seat to see who holds it. ' + (allCertified() ? 'Every state has certified its results.' : 'Results are unofficial until every state certifies them.'))
          : L(`Le Congrès a deux chambres, la Chambre des représentants et le Sénat. Chaque point est un siège, à la couleur du parti de son titulaire : démocrates en bleu, républicains en rouge, indépendants en gris ; dans chaque parti, les membres les plus modérés siègent au centre et les plus à gauche ou à droite sur le bord extérieur, selon leurs votes. Les boutons des caucus éclairent les membres de chacun. Survolez ou touchez un siège pour voir qui l’occupe. Listes relues chaque jour ; dernière mise à jour le ${dateL(data.updated)}.`,
            `Congress has two chambers, the House of Representatives and the Senate. Each dot is a seat, colored by its holder’s party: Democrats blue, Republicans red, independents gray; within each party, the most moderate members sit nearest the middle and those furthest left or right on the outer edge, by how they vote. The caucus buttons light up each caucus’s members. Hover over or tap a seat to see who holds it. The member lists are reread every day; last updated ${dateL(data.updated)}.`)}</p></div>
      <div class="parl-toggles">
        ${after ? html`<nav class="seg" aria-label="${L('Congrès', 'Congress')}">
          <a href="${q({ congress: '' })}" aria-current="${which === 120 ? 'page' : 'false'}">${L('120e Congrès (janvier 2027)', '120th Congress (January 2027)')}</a>
          <a href="${q({ congress: '119' })}" aria-current="${which === 119 ? 'page' : 'false'}">${L('119e Congrès (actuel)', '119th Congress (now)')}</a>
        </nav>` : ''}
        <nav class="seg" aria-label="${L('Chambre', 'Chamber')}">
          <a href="${chamberLink('house')}" aria-current="${ch === 'house' ? 'page' : 'false'}">${L('Chambre des représentants', 'House of Representatives')}</a>
          <a href="${chamberLink('senate')}" aria-current="${ch === 'senate' ? 'page' : 'false'}">${L('Sénat', 'Senate')}</a>
        </nav>
      </div>
      ${officials(data, model)}
      <section class="card stack">
        <div><h2 style="margin:0">${title}</h2>
          <p class="small muted" style="margin:4px 0 0">${INTRO[ch](model, data)}</p></div>
        ${caucusPicker(model, ch)}
        <div id="parl-hemi"></div>
        ${seatNote()}
        ${stats(ch, model)}
        <div class="grid grid-2" style="gap:18px;align-items:start">
          ${which === 120
            ? html`<div><div class="eyebrow" style="margin-bottom:8px">${L('Dirigeants', 'Leaders')}</div><p class="small muted" style="margin:0">${ch === 'senate'
              ? L('Chaque parti choisit ses dirigeants au Sénat avant le 3 janvier 2027, et le Sénat élit son président pro tempore quand il se réunit. Ceux du 119e Congrès sont sur l’autre onglet.', 'Each party picks its Senate leaders before January 3, 2027, and the Senate elects its President pro tempore when it meets. The 119th Congress’s are on the other tab.')
              : L('Chaque parti choisit ses dirigeants avant le 3 janvier 2027, et la Chambre élit son Speaker ce jour-là. Ceux du 119e Congrès sont sur l’autre onglet.', 'Each party picks its leaders before January 3, 2027, and the House elects its Speaker that day. The 119th Congress’s are on the other tab.')}</p></div>`
            : html`<div><div class="eyebrow" style="margin-bottom:8px">${L('Dirigeants', 'Leaders')}</div>${leadersList(ch, data)}</div>`}
          ${ch === 'house' ? houseNotes(data, model) : senateNotes(model)}
        </div>
      </section>
      ${membersList(ch, model, groups)}
      ${which === 119 && data.checks?.length ? html`<div class="notice warn">${icon.info()}<div><b>${L('Différences entre sources, à vérifier', 'Differences between sources, to be checked')}</b><ul style="margin:6px 0 0" lang="en">${data.checks.map((c) => html`<li>${c}</li>`)}</ul></div></div>` : ''}
      <p class="tiny faint" style="margin:0">${L('Sources : ', 'Sources: ')}${which === 120 ? html`${L('les résultats de 2026 (pages des élections, tableaux nationaux de Wikipédia : non officiels jusqu’à certification)', 'the 2026 results (each race’s page; Wikipedia’s national tables, unofficial until certified)')} · ` : ''}${sources.map((s, i) => html`${i ? ' · ' : ''}<a href="${s.url}" target="_blank" rel="noopener noreferrer">${s.revid ? `Wikipedia: ${s.title}` : s.title}</a>${!s.revid && data.chambers[ch].published && s.url.includes('clerk.house.gov') ? L(` (du ${data.chambers[ch].published})`, ` (dated ${data.chambers[ch].published})`) : ''}`)}</p>
      ${photoCredits(presiding(data).map(([, p]) => p))}
    </div>`;
  },
  async mount(root, ctx) {
    const [data] = await Promise.all([load(), loadHolders()]);
    const host = root.querySelector('#parl-hemi');
    if (!data || !host) return null;
    const ch = ctx.query.chamber === 'senate' ? 'senate' : 'house';
    const { which } = whichOf(ctx);
    const model = which === 120 ? incoming(data, ch) : sitting(data, ch);
    const groups = groupsFor(model.members);
    const byId = new Map(groups.map((g) => [g.id, g]));
    const empty = model.seats - model.members.length;
    const chart = drawHemicycle(host, {
      seats: model.seats,
      groups,
      members: model.members,
      tipFor: (m) => tip(m, ch, byId.get(m.g), model, model.members.some((x) => x.caucuses?.length)),
      vacantTip: (i) => {
        if (which === 120) {
          const o = model.open[i];
          return o ? html`<div class="tt-title">${L('Pas encore décidé', 'Not decided yet')}</div><div class="tt-sub">${seatName(o, ch)}</div><div class="small" style="margin-top:4px;max-width:260px">${openLine(o)}</div>` : '';
        }
        const v = model.vacancies?.[i];
        return html`<div class="tt-title">${L('Siège vacant', 'Vacant seat')}</div>${v ? html`<div class="tt-sub">${seatName(v, ch)}</div>${v.note ? html`<div class="small" style="margin-top:4px;max-width:260px" lang="en">${v.note}</div>` : ''}` : ''}`;
      },
      ariaLabel: `${ch === 'senate' ? L('Sénat', 'Senate') : L('Chambre des représentants', 'House of Representatives')}${L(' : ', ': ')}${model.seats} ${L('sièges', 'seats')}. ${['D', 'I', 'R'].filter((p) => partySeats(groups, p)).map((p) => `${L(...COLUMN[p])} ${partySeats(groups, p)}`).join(', ')}${empty > 0 ? `, ${empty} ${which === 120 ? L('pas encore décidés', 'not decided yet') : L('vacants', 'vacant')}` : ''}.`,
      hint: L('Survolez ou touchez un siège pour voir qui l’occupe. Au clavier, les flèches passent d’un siège à l’autre, Page précédente et Page suivante d’un parti à l’autre.', 'Hover over or tap a seat to see who holds it. With the keyboard, the arrow keys move from seat to seat and Page Up and Page Down jump between parties.'),
      center: [String(model.seats), L('sièges', 'seats'), L(`majorité : ${model.majority}`, `majority: ${model.majority}`)],
      legendItem: (g) => keyItem(g),
      legendLabel: L('Légende : partis', 'Key: parties'),
      // Seats not decided yet (and vacant ones) in the middle, between the two sides.
      vacantAfter: [...groups].reverse().find((g) => g.party !== 'R')?.id,
    });

    const find = root.querySelector('#parl-find');
    const count = root.querySelector('#parl-count');
    const rows = [...root.querySelectorAll('#parl-list tbody tr')];
    const key = `${which}-${ch}`;
    // The member list: the search words and, while a caucus is lit up, its members only.
    const filter = () => {
      const qy = fold(find?.value.trim() || '');
      const c = picked[key];
      let n = 0;
      for (const r of rows) {
        const hit = (!qy || r.dataset.q.includes(qy)) && (!c || r.dataset.c.split(' ').includes(c));
        r.hidden = !hit;
        if (hit) n += 1;
      }
      if (count) count.textContent = qy || c ? L(`${n} résultat${n === 1 ? '' : 's'}`, `${n} result${n === 1 ? '' : 's'}`) : '';
    };
    find?.addEventListener('input', filter);

    // The caucus buttons: one caucus at a time, its members lit up on the chart.
    const buttons = [...root.querySelectorAll('.parl-caucus')];
    const note = root.querySelector('#parl-caucus-note');
    const hintText = note?.textContent || '';
    const pick = (id) => {
      const d = id ? caucusDefs().find((x) => x.id === id) : null;
      picked[key] = d ? id : null;
      buttons.forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.c === picked[key])));
      chart.mark(d ? (m) => inCaucus(m, id) : null);
      if (note) {
        const n = d ? model.members.filter((m) => inCaucus(m, id)).length : 0;
        note.textContent = d ? L(`${d.name} : ${n} membre${n === 1 ? '' : 's'} en évidence ; la liste des membres ci-dessous ne montre que ces personnes.`,
          `${d.name}: ${n} member${n === 1 ? '' : 's'} lit up; the member list below shows only them.`) : hintText;
      }
      filter();
    };
    buttons.forEach((b) => b.addEventListener('click', () => pick(picked[key] === b.dataset.c ? null : b.dataset.c)));
    if (picked[key]) pick(picked[key]);
    return () => chart.destroy();
  },
};
