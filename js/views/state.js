import { html, raw, fmtProb, fmtPct, fmtDR, fmtDate } from '../util.js';
import { icon } from '../icons.js';
import { L, lang } from '../i18n.js';
import { STATE_BY_ABBR, legislatureChambers, electionDateLabel, stateName, inState, chamberOf, chamberName } from '../data/states.js';
import { fc, statewideRaces, houseRaces, officeRaces, loadLayer, legislativeRaces, mapView, setMapView, resultsIn, resultParty, resultWinners, resultMargin, districtNameL, ratingL, officeNameL, certifiedIn } from '../data/world.js';
import { cleanDistrictName } from '../data/demo.js';
import { drawMap, ratingColor, ratingLegendHTML, resultFill, resultsLegendHTML } from '../lib/map.js';
import { cssVar } from '../lib/charts.js';
import { raceFull, compactRace, raceRow, mountRaceTabs, leadStr, lastName, photoCredits, resultMarginStr } from '../components/race.js';
import { howToVote, voteCardLabel } from '../components/vote.js';
import { loadHolders, senatorsOf, governorOf, statewideOfficers, fromRace, delegation, loadLegislators, districtMembers } from '../data/holders.js';
import { personCard, partyLetter } from '../components/person.js';
import { wireCompare } from '../components/compare.js';

const ODD_YEAR_STATES = new Set(['LA', 'MS', 'NJ', 'VA']);
let scrolledFor = null; // the address whose district the page last scrolled to

function chips(st) {
  const { senate, governor } = statewideRaces(st);
  const out = [];
  const special = L(' (partielle)', ' (special)');
  if (senate) out.push(html`<span class="chip">${icon.check()} ${L('Sénat des États-Unis', 'U.S. Senate')}${senate.special ? special : ''}</span>`);
  if (governor) out.push(html`<span class="chip">${icon.check()} ${L('Gouverneur', 'Governor')}</span>`);
  out.push(html`<span class="chip">${icon.check()} ${L('Chambre des représentants', 'U.S. House')}</span>`);
  for (const r of officeRaces(st)) out.push(html`<span class="chip">${icon.check()} ${officeNameL(r.officeName)}${r.special ? special : ''}</span>`);
  for (const c of legislatureChambers(st)) if (c.up !== 'none') out.push(html`<span class="chip">${icon.check()} ${chamberName(c.name)}${c.up === 'partial' ? L(' (une partie des sièges)', ' (some seats)') : ''}</span>`);
  return out;
}

// Before the results: the statewide offices below governor, each opening its own race page.
function officesSection(st) {
  const rs = officeRaces(st);
  if (!rs.length) return '';
  return html`<section class="card stack-sm" style="margin-bottom:20px">
    <div class="section-head"><div><div class="eyebrow">${L('Postes à l’échelle de l’État', 'Statewide offices')}</div><h2 style="margin:4px 0 0">${L('Sous le gouverneur', 'Below the governor')}</h2></div><span class="small faint">${L(`${rs.length} élection${rs.length === 1 ? '' : 's'} · cliquez sur l’une d’elles pour les candidatures, leurs positions et les résultats`, `${rs.length} race${rs.length === 1 ? '' : 's'} · click one for the candidates, their positions and the results`)}</span></div>
    <div class="race-list">${rs.map((r) => raceRow(r))}</div>
  </section>`;
}

// After the results: who holds each statewide office from January 2027 (the 2026 winner,
// the governor-elect's running mate, or the person in office), with their positions.
const OFFICER_FR = { LG: 'Lieutenant-gouverneur', AG: 'Procureur général', SOS: 'Secrétaire d’État', TREAS: 'Trésorier', AUD: 'Auditeur ou contrôleur' };
const officerLabel = (p) => L(OFFICER_FR[p.slot] || p.label, p.label);
function officersSection(st) {
  const people = statewideOfficers(st);
  if (!people.length) return '';
  return html`<section class="stack-sm" style="margin-bottom:24px">
    <div class="section-head"><div><div class="eyebrow">${L('Exécutif de l’État', 'Statewide officers')}</div><h2 style="margin:4px 0 0">${L('Sous le gouverneur', 'Below the governor')}</h2></div>
      <span class="small faint">${L('Élection du 3 novembre 2026, ou en fonction si le poste n’était pas en jeu', 'Elected Nov. 3, 2026, or in office where the seat wasn’t up')}</span></div>
    <div class="people-grid">${people.map((p) => personCard(p, { level: 'state', eyebrow: officerLabel(p) }))}</div>
  </section>`;
}

const tally = (parties) => ['D', 'R', 'I'].map((p) => [p, parties.filter((x) => x === p).length]).filter(([, n]) => n).map(([p, n]) => `${n} ${p}`).join(' · ');

function senatorsSection(st, senate) {
  const s = STATE_BY_ABBR[st];
  const sens = senatorsOf(st);
  if (!sens.length) return emptyState(L('Pas de sénateurs', 'No senators'), L('Le district de Columbia n’a pas de siège au Sénat.', 'The District of Columbia has no seats in the Senate.'));
  const d = delegation(st);
  return html`<section class="stack">
    <div class="section-head"><div><div class="eyebrow">${L('Sénat des États-Unis · à partir de janvier 2027', 'U.S. Senate · from January 2027')}</div><h2 style="margin:4px 0 0">${L('Les deux sièges de l’État au Sénat', `${s.name}’s two senators`)}</h2></div><span class="small faint">${tally(d.parties)}</span></div>
    <div class="people-grid">${sens.map((p) => personCard(p, { level: 'federal', eyebrow: L('Sénat des États-Unis', 'U.S. Senate') }))}</div>
    ${senate ? html`<div class="stack-sm"><div class="eyebrow">${L('L’élection sénatoriale de 2026', 'The 2026 Senate race')}</div><div class="race-list">${raceRow(senate)}</div></div>` : ''}
  </section>`;
}

// A House district on the results map: winner and margin, runoff, leader, or nothing yet.
function districtResult(r, { full = false } = {}) {
  const res = r.result;
  if (!res) return { text: L('Pas encore de résultat', 'No result yet'), party: null, won: false };
  if (res.status === 'won') {
    const w = resultWinners(r)[0];
    if (full && w) return { text: `${w.name} (${partyLetter(w.party)})`, party: w.party, won: true };
    return { text: `${w ? lastName(w.name) : ''} ${resultMarginStr(r) || ''}${res.flip ? L(' · bascule', ' · flip') : ''}`.trim(), party: w?.party, won: true };
  }
  if (res.status === 'runoff') return { text: L('Second tour', 'Runoff'), party: null, won: false };
  const m = resultMargin(r);
  return { text: m ? L(`${lastName(m.a.name)} en tête, ${resultMarginStr(r)}`, `${lastName(m.a.name)} leads, ${resultMarginStr(r)}`) : L('Dépouillement', 'Counting'), party: m?.a.party || null, won: false };
}

function parseMode(st, q) {
  const s = STATE_BY_ABBR[st];
  const level = q.level === 'state' ? 'state' : 'federal';
  let chamber = q.chamber;
  // Before the election the Senate view is the state's 2026 race; after it, every state's
  // two senators, whether or not a seat was up (Vermont's Sanders and Welch).
  const senators = s.senate || (resultsIn() && st !== 'DC');
  if (level === 'federal') chamber = chamber === 'house' || !senators ? 'house' : 'senate';
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
    ? html`<a href="${href(st, 'federal', 'senate')}" ${cur(chamber === 'senate')}>${L('Sénateurs', 'Senators')}</a><a href="${href(st, 'federal', 'house')}" ${cur(chamber === 'house')}>${L('Représentants', 'House Representatives')}</a>`
    : s.unicameral
      ? html`<a href="${href(st, 'state', 'leg')}" aria-current="page">${L('Législature (une seule chambre)', 'Legislature (single chamber)')}</a>`
      : html`<a href="${href(st, 'state', 'senate')}" ${cur(chamber === 'senate')}>${L('Sénateurs', 'Senators')}</a><a href="${href(st, 'state', 'house')}" ${cur(chamber === 'house')}>${L('Représentants', 'House Representatives')}</a>`;
  return html`<div class="toggles">
    <nav class="seg big" aria-label="${L('Niveau', 'Election level')}">
      <a href="${href(st, 'federal', 'senate')}" ${cur(level === 'federal')}>${L('Élections fédérales', 'Federal elections')}</a>
      <a href="${href(st, 'state', s.unicameral ? 'leg' : 'senate')}" ${cur(level === 'state')}>${L('Élections de l’État', 'State elections')}</a>
    </nav>
    ${st === 'DC' ? '' : html`<nav class="seg" aria-label="${L('Chambre', 'Chamber')}">${second}</nav>`}
  </div>`;
}

function emptyState(title, body) {
  return html`<div class="empty">${icon.ballot()}<h3>${title}</h3><p style="margin:0">${body}</p></div>`;
}

// State legislatures after the 2026 election -------------------------------------------
// Each district in its members' party: the 2026 winners where a seat was up, Open States'
// members where none was (holders.js, districtMembers). Purple where a district's members
// are of both parties; a seat whose winner isn't posted yet stays gray and says so.
const CHAMBER_FR = {
  'State Senate': 'Sénat de l’État', 'State House': 'Chambre des représentants de l’État', 'State Assembly': 'Assemblée de l’État',
  'House of Delegates': 'Chambre des délégués', 'General Assembly': 'Assemblée générale', Legislature: 'Législature',
};
const chamberL = (c) => L(CHAMBER_FR[c.name] || c.name, c.name);
// Short party marks for the legislatures, where Nebraska's members are nonpartisan.
const markOf = (p) => ({ D: 'D', R: 'R', I: 'I', L: 'L', G: 'G', N: L('SP', 'NP') }[p] || (p && p !== 'Party not listed' ? p.slice(0, 1).toUpperCase() : '?'));
const poleKey = (p) => (p === 'D' || p === 'R' ? p : 'O');

function membersSection(st, chamber) {
  const s = STATE_BY_ABBR[st];
  const note = chamber.up === 'none'
    ? (ODD_YEAR_STATES.has(st)
      ? L('L’État élit sa législature les années impaires (prochaine élection en 2027) : la carte montre les membres en fonction.', `${s.name} elects its legislature in odd-numbered years (next in 2027), so the map shows the members in office.`)
      : L(`Pas d’élection pour cette chambre en 2026 (mandats de quatre ans, prochaine élection en 2028) : la carte montre les membres en fonction.`, `This chamber had no election in 2026 (four-year terms, next elected in 2028), so the map shows the members in office.`))
    : chamber.up === 'partial'
      ? L('Mandats décalés : les circonscriptions qui votaient le 3 novembre 2026 montrent la personne élue, les autres le membre en fonction.', 'Staggered terms: districts that voted on Nov. 3, 2026 show who was elected, the others the member in office.')
      : L('Chaque circonscription votait le 3 novembre 2026.', 'Every district voted on Nov. 3, 2026.');
  const np = s.unicameral ? html` ${L('La Législature du Nebraska est officiellement non partisane : ses membres sont élus sans étiquette, d’où une seule couleur.', 'Nebraska’s Legislature is officially nonpartisan: members are elected without party labels, so the map has one color.')}` : '';
  return html`<section class="stack">
    <div class="card map-card">
      <div class="section-head">
        <div><div class="eyebrow">${L(`${chamberL(chamber)} · après l’élection de 2026`, `${chamber.name} · after the 2026 election`)}</div><h2 style="margin:4px 0 0">${L(`Qui siège, circonscription par circonscription`, 'Who sits for each district')}</h2></div>
        <p class="small muted" style="margin:0;max-width:440px">${note}${np} ${L('Cliquez sur une circonscription pour voir ses élus. Ctrl + molette ou les boutons pour zoomer.', 'Click a district to see who represents it. Ctrl + scroll or the buttons to zoom.')}</p>
      </div>
      <div id="members-tally"></div>
      <div id="district-map"><div class="row muted"><span class="spinner"></span> ${L('Chargement de la carte…', 'Loading district map…')}</div></div>
      <div id="district-legend"></div>
      <p class="tiny faint" id="members-source" style="margin:8px 0 0"></p>
    </div>
    <div id="district-race"></div>
    <div class="card"><div class="section-head"><h3 style="margin:0">${L('Toutes les circonscriptions', 'Every district')}</h3><span class="small faint" id="district-count"></span></div><div class="district-grid wide" id="district-list"></div></div>
  </section>`;
}

// Whether the state certified its legislative results (data/certified.json), with the
// seats it left out (recounts).
function legCert(st) {
  const c = certifiedIn(st);
  if (!c) return L('non officiels jusqu’à la certification', 'unofficial until certified');
  const out = (c.other || []).map((o) => L(o[1], o[0]));
  return html`${L(`certifiés par l’État le ${fmtDate(c.date)}`, `certified by the state on ${fmtDate(c.date)}`)} (<a href="${c.source.url}" target="_blank" rel="noopener noreferrer">${c.source.title.split(':')[0]}</a>)${out.length ? L(`, sauf : ${out.join(' ; ')}`, `, except ${out.join('; ')}`) : ''}`;
}

async function mountMembers(root, ctx, st, m, cleanup) {
  const chamber = legislatureChambers(st).find((c) => c.key === m.chamber);
  const mapEl = root.querySelector('#district-map');
  if (!chamber || !mapEl) return cleanup;
  const [features, data, file] = await Promise.all([
    loadLayer(st, chamber.layer),
    chamber.up === 'none' ? null : legislativeRaces(st, m.chamber),
    loadLegislators(st),
  ]);
  if (!root.isConnected) return cleanup;
  const races = data?.races || new Map();
  const dist = new Map(features.features.map((f) => {
    const r = races.get(f.id);
    const race = r && !r.demo ? r : null;
    // Every seat was up but the page has no race here: nothing posted yet, and the outgoing
    // member isn't shown as if still seated.
    const d = !race && chamber.up === 'all'
      ? { members: [], pending: { status: 'no-result', key: `${st}:${m.chamber}:${f.id}:open` } }
      : districtMembers(file, m.chamber, f.id, race);
    return [f.id, { f, race, name: districtNameL(race?.districtName || cleanDistrictName(f.properties.n)), ...d }];
  }));
  const panel = root.querySelector('#district-race');
  const list = root.querySelector('#district-list');

  const dem = cssVar('--dem'), rep = cssVar('--rep'), other = cssVar('--seat-other'), mid = cssVar('--neutral-mid'), split = cssVar('--split');
  const pole = { D: dem, R: rep, O: other };
  const kinds = (d) => new Set(d.members.map((p) => poleKey(p.party)));
  const fillFor = (d, pattern) => {
    if (!d.members.length) return mid; // not posted yet, or vacant
    const ks = kinds(d);
    if (ks.size === 1) {
      const base = pole[[...ks][0]];
      return d.members.length === 1 && d.members[0].flip && pattern ? pattern(base, cssVar('--bg')) : base;
    }
    if (ks.has('D') && ks.has('R')) return split;
    const p = ks.has('D') ? dem : rep; // a party's member beside an independent
    return pattern ? pattern(p, other, 4, 8) : p;
  };
  const who = (p) => `${p.name} (${markOf(p.party)})`;
  const statusText = (d) => (d.members.length
    ? d.members.map(who).join(', ')
    : d.pending ? L('Pas encore de résultat publié', 'No result posted yet') : L('Siège vacant', 'Vacant'));

  const few = features.features.length <= 40;
  const map = drawMap(mapEl, features, {
    fillFor: (f, pattern) => fillFor(dist.get(f.id), pattern),
    tooltipFor: (f) => {
      const d = dist.get(f.id);
      return html`<div class="t-title">${d.name}</div>
        ${d.members.map((p) => html`<div class="t-row"><span>${p.status === 'elected' ? L('Élu en 2026', 'Elected 2026') : L('En fonction', 'In office')}</span><b>${who(p)}${p.flip ? L(' · siège gagné', ' · flipped') : ''}</b></div>`)}
        ${d.pending ? html`<div class="t-row"><span>${L('Élection 2026', '2026 race')}</span><b>${L('Pas encore de résultat publié', 'No result posted yet')}</b></div>` : ''}
        ${!d.members.length && !d.pending ? html`<div class="faint small">${L('Aucun membre indiqué pour ce siège', 'No member listed for this seat')}</div>` : ''}
        <div class="tiny faint" style="margin-top:6px">${L('Cliquez pour voir ses élus', 'Click to see who represents it')}</div>`;
    },
    onSelect: (f) => select(f.id, true),
    labelFor: few ? (f) => String(parseInt(f.id, 10) || f.id) : null,
    regionLabel: (f) => { const d = dist.get(f.id); return `${d.name}${L(' : ', ': ')}${statusText(d)}`; },
    zoomable: true,
    ariaLabel: L('Carte des circonscriptions, colorée selon le parti des élus', 'District map colored by the party of each district’s members'),
  });

  // The chamber's seats by party, and what isn't known yet.
  const all = [...dist.values()];
  const count = { D: 0, R: 0, O: 0 };
  for (const d of all) for (const p of d.members) count[poleKey(p.party)] += 1;
  const pendingSeats = all.reduce((n, d) => n + (d.pending ? Math.max(1, d.race?.seats || 1) : 0), 0);
  const known = count.D + count.R + count.O;
  const vacant = Math.max(0, (chamber.seats || 0) - known - pendingSeats);
  const otherLabel = STATE_BY_ABBR[st].unicameral ? L('Non partisans', 'Nonpartisan') : L('Indépendants ou autres', 'Independent or other');
  const segs = [['D', dem, L('Démocrates', 'Democrats')], ['O', other, otherLabel], ['R', rep, L('Républicains', 'Republicans')]]
    .filter(([k]) => count[k]).map(([k, c, label]) => ({ n: count[k], c, label }));
  if (pendingSeats) segs.push({ n: pendingSeats, c: mid, label: L('Pas encore publiés', 'Not posted yet') });
  const off = file?.unmatched?.filter((u) => u.chamber === m.chamber).length || 0; // members of districts the map doesn't draw
  if (vacant) segs.push({ n: vacant, c: cssVar('--not-up'), label: off ? L('Vacants ou hors carte', 'Vacant or not on the map') : L('Vacants ou non indiqués', 'Vacant or not listed') });
  root.querySelector('#members-tally').innerHTML = String(html`<div class="leg-tally">
    <div class="leg-bar" role="img" aria-label="${segs.map((x) => `${x.label}: ${x.n}`).join(', ')}">${segs.map((x) => html`<i style="flex:${x.n} 1 0;background:${x.c}"></i>`)}</div>
    <div class="leg-key">${segs.map((x) => html`<span><i class="key-box" style="background:${x.c}"></i>${x.label} <b>${x.n}</b></span>`)}<span class="faint">${L(`sur ${chamber.seats} sièges`, `of ${chamber.seats} seats`)}</span></div>
  </div>`);

  const has = (fn) => all.some(fn);
  const sw = (bg, label) => `<span><i style="background:${bg}"></i>${label}</span>`;
  const stripe = (a, b) => `repeating-linear-gradient(45deg, ${a} 0 4px, ${b} 4px 8px)`;
  root.querySelector('#district-legend').innerHTML = `<div class="map-legend">${[
    has((d) => kinds(d).has('D') && kinds(d).size === 1) ? sw(dem, L('Démocrate', 'Democrat')) : '',
    has((d) => kinds(d).has('R') && kinds(d).size === 1) ? sw(rep, L('Républicain', 'Republican')) : '',
    has((d) => kinds(d).has('O') && kinds(d).size === 1) ? sw(other, otherLabel) : '',
    has((d) => kinds(d).has('D') && kinds(d).has('R')) ? sw(split, L('Les deux partis (plusieurs sièges)', 'Both parties (multi-seat district)')) : '',
    has((d) => kinds(d).has('O') && kinds(d).size === 2) ? sw(stripe(dem, other), L('Un parti et un indépendant', 'A party and an independent')) : '',
    has((d) => d.members.length === 1 && d.members[0].flip) ? sw(stripe(rep, cssVar('--bg')), L('Siège gagné en 2026 (rayé)', 'Flipped in 2026 (striped)')) : '',
    has((d) => !d.members.length) ? sw(mid, L('Pas encore publié ou vacant', 'Not posted yet or vacant')) : '',
  ].join('')}</div>`;

  const posted = all.filter((d) => d.race && d.race.result?.status === 'won').length;
  const upCount = all.filter((d) => d.race || d.pending).length;
  root.querySelector('#district-count').textContent = chamber.up === 'none'
    ? L(`${all.length} circonscriptions`, `${all.length} districts`)
    : L(`${posted} des ${upCount} élections de 2026 ont un résultat publié`, `${posted} of ${upCount} 2026 races have a result posted`);
  const src = [];
  if (data?.info?.url) src.push(html`${L('Élus de 2026 : page Wikipédia de la chambre', '2026 winners: Wikipedia’s chamber page')} (<a href="${data.info.url}" target="_blank" rel="noopener noreferrer">${data.info.title}</a>), ${legCert(st)}`);
  if (file && all.some((d) => d.members.some((p) => p.notUp))) {
    src.push(html`${L('membres en fonction : ', 'members in office: ')}<a href="${file.source.url}" target="_blank" rel="noopener noreferrer">${file.source.title}</a> (${file.source.license}, ${L('relu chaque jour', 'checked daily')})`);
  }
  root.querySelector('#members-source').innerHTML = String(html`${src.map((x, i) => html`${i ? ' · ' : ''}${x}`)}.${off ? L(' Certaines circonscriptions ne sont pas dessinées sur la carte (celles qui en chevauchent d’autres, comme les circonscriptions flottantes du New Hampshire) : leurs sièges comptent comme hors carte.', ' Some districts aren’t drawn on the map (those overlapping others, like New Hampshire’s floterial districts), so their seats count as not on the map.') : ''}`);

  list.innerHTML = features.features.map((f) => {
    const d = dist.get(f.id);
    const ks = kinds(d);
    const color = ks.size === 1 && ks.has('D') ? 'd-text' : ks.size === 1 && ks.has('R') ? 'r-text' : '';
    const flip = d.members.some((p) => p.flip);
    const text = `${statusText(d)}${flip ? L(' · gagné', ' · flip') : ''}`;
    return String(html`<button type="button" class="district-btn" data-district="${f.id}" aria-pressed="false" title="${d.name}: ${text}"><span class="dn">${d.name}</span><span class="dm ${color}">${d.members.some((p) => p.status === 'elected') ? html`<span class="win-tick">${icon.check()}</span>` : ''}${text}</span></button>`);
  }).join('');
  list.addEventListener('click', (e) => {
    const b = e.target.closest('[data-district]');
    if (b) select(b.dataset.district, true);
  });

  function select(code, fromUser) {
    const d = dist.get(code);
    if (!d) return;
    map.select(code);
    list.querySelectorAll('[data-district]').forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.district === code)));
    const eyebrow = `${chamberL(chamber)} · ${d.name}`;
    const one = d.members.length === 1 && !d.pending; // one member: one wide card, as on the U.S. House map
    const cards = d.members.map((p) => personCard(p, { level: 'state', eyebrow, wide: one }));
    if (d.pending) cards.unshift(personCard(d.pending.id ? fromRace(d.pending) : d.pending, { level: 'state', eyebrow }));
    panel.innerHTML = String(html`<section class="stack-sm">
      ${cards.length > 1 ? html`<div class="section-head"><div><div class="eyebrow">${chamberL(chamber)}</div><h2 style="margin:4px 0 0">${d.name}</h2></div>
        <span class="small faint">${L(`${d.members.length} membre${d.members.length === 1 ? '' : 's'}`, `${d.members.length} member${d.members.length === 1 ? '' : 's'}`)}</span></div>` : ''}
      ${!cards.length ? emptyState(L(`${d.name} : siège vacant`, `${d.name}: vacant seat`), L('Aucun membre n’est indiqué pour cette circonscription.', 'No member is listed for this district.'))
        : one ? cards[0] : html`<div class="people-grid">${cards}</div>`}
      ${photoCredits(d.members.filter((p) => p.photo))}
    </section>`);
    if (fromUser) {
      const q = new URLSearchParams({ level: m.level, chamber: m.chamber, d: code });
      history.replaceState(null, '', `#/state/${st}?${q}`);
      map.zoomTo(code);
      panel.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }

  // Start on the district asked for, else the closest 2026 count, else the first district.
  const closest = all.filter((d) => d.race && d.race.result?.status === 'won' && resultMargin(d.race))
    .sort((a, b) => resultMargin(a.race).pts - resultMargin(b.race).pts)[0];
  const start = ctx.query.d && dist.has(ctx.query.d) ? ctx.query.d : (closest?.f.id || features.features[0]?.id);
  if (start) select(start, false);
  if (start && ctx.query.d === start && scrolledFor !== location.hash) {
    scrolledFor = location.hash;
    map.zoomTo(start);
    setTimeout(() => panel.scrollIntoView({ block: 'start', behavior: 'instant' }), 0);
  }
  return cleanup;
}

export const stateView = {
  live: true, // redrawn when new counts arrive (main.js)
  title: (ctx) => (STATE_BY_ABBR[ctx.params[0]] ? stateName(ctx.params[0]) : L('État', 'State')),
  async render(ctx) {
    const st = ctx.params[0];
    const s = STATE_BY_ABBR[st];
    if (!s) return html`<div class="wrap page">${emptyState(L('État introuvable', 'State not found'), L('Choisissez un État sur la carte de la page d’accueil.', 'Pick a state from the map on the homepage.'))}</div>`;
    const m = parseMode(st, ctx.query);
    const { senate, governor } = statewideRaces(st);
    // After the election the page shows the people elected (or still in office), with
    // their records; before it, the races.
    const after = resultsIn();
    if (after) await loadHolders();
    const shown = []; // people pictured, for the photo credits

    let body;
    const houseResults = m.level === 'federal' && m.chamber === 'house' && after;
    if (m.level === 'federal' && m.chamber === 'senate') {
      if (after) {
        body = senatorsSection(st, senate);
        shown.push(...senatorsOf(st));
      } else {
        body = senate
          ? html`<section class="card" style="padding:clamp(16px,3vw,28px)">${raceFull(senate, { tag: 'h2', credits: false })}</section>`
          : emptyState(L(`Pas d’élection au Sénat ${inState(st)} en 2026`, `No U.S. Senate election in ${s.name} in 2026`), L('Aucun des deux sièges de l’État au Sénat n’est en jeu cette année. Ils le seront en 2028 et en 2030.', `Neither of ${s.name}’s Senate seats is on the ballot this year. They are next up in 2028 and 2030.`));
      }
    } else if (m.level === 'state' && st === 'DC') {
      body = html`${after ? '' : officesSection(st)}${emptyState(L('Pas de législature d’État', 'No state legislature'), L('Le district de Columbia a un conseil municipal au lieu d’une législature d’État : il n’y a donc pas d’élections législatives d’État ici.', 'The District of Columbia has a city council instead of a state legislature, so there are no state legislative races here.'))}`;
    } else if (m.level === 'state' && after) {
      const chamber = legislatureChambers(st).find((c) => c.key === m.chamber);
      body = chamber ? membersSection(st, chamber) : '';
    } else {
      const chamber = m.level === 'federal' ? null : legislatureChambers(st).find((c) => c.key === m.chamber);
      if (chamber && chamber.up === 'none') {
        body = lang() === 'fr'
          ? emptyState(`${chamberOf(st, chamber.name)} : pas d’élection en 2026`, ODD_YEAR_STATES.has(st) ? 'L’État élit sa législature les années impaires ; la prochaine élection a lieu en 2027.' : 'Cette chambre a des mandats de quatre ans ; sa prochaine élection a lieu en 2028.')
          : emptyState(`No ${chamber.name} elections in ${s.name} in 2026`, ODD_YEAR_STATES.has(st) ? `${s.name} elects its legislature in odd-numbered years; the next election is in 2027.` : `${s.name}’s ${chamber.name} has four-year terms and is next elected in 2028.`);
      } else {
        const label = m.level === 'federal'
          ? (st === 'DC' ? L('Délégué à la Chambre des représentants', 'Delegate to the U.S. House') : L('Circonscriptions de la Chambre des représentants', 'U.S. House districts'))
          : L(`${chamberName(chamber.name)} : les circonscriptions`, `${chamber.name} districts`);
        const view = mapView();
        const eyebrow = houseResults
          ? L('Chambre des représentants · à partir de janvier 2027', 'U.S. House · from January 2027')
          : lang() === 'fr'
            ? `${m.level === 'federal' ? 'Fédéral' : 'État'} · ${after && m.level === 'federal' ? (view === 'results' ? 'résultats 2026 par circonscription' : 'dernière prévision 2026 par circonscription') : 'carte 2026 des circonscriptions'}`
            : `${m.level === 'federal' ? 'Federal' : 'State'} · 2026 district ${after && m.level === 'federal' ? (view === 'results' ? 'results' : 'final forecast') : 'map'}`;
        const help = houseResults
          ? L('Cliquez sur une circonscription pour voir qui a été élu, ses positions et l’argent de sa campagne. Ctrl + molette ou les boutons pour zoomer.', 'Click a district to see who was elected, their positions and their campaign money. Ctrl + scroll or the buttons to zoom.')
          : lang() === 'fr'
            ? `${chamber && chamber.up === 'partial' ? 'Mandats échelonnés : seules certaines circonscriptions votent en 2026 ; les autres sont grisées. ' : ''}Cliquez sur une circonscription pour voir son élection. Ctrl + molette ou les boutons pour zoomer.`
            : `${chamber && chamber.up === 'partial' ? 'Staggered terms: only some districts elect in 2026; the rest are grayed out. ' : ''}Click a district to see its race. Ctrl + scroll or the buttons to zoom.`;
        body = html`<section class="stack">
          <div class="card map-card">
            <div class="section-head">
              <div><div class="eyebrow">${eyebrow}</div><h2 style="margin:4px 0 0">${label}</h2></div>
              <p class="small muted" style="margin:0;max-width:420px">${help}</p>
            </div>
            <div id="district-map"><div class="row muted"><span class="spinner"></span> ${L('Chargement de la carte…', 'Loading district map…')}</div></div>
            <div id="district-legend"></div>
          </div>
          <div id="district-race"></div>
          <div class="card"><div class="section-head"><h3 style="margin:0">${houseResults ? L('Toutes les circonscriptions', 'Every district') : L('Toutes les circonscriptions', 'All districts')}</h3><span class="small faint" id="district-count"></span></div><div class="district-grid${houseResults ? ' wide' : ''}" id="district-list"></div></div>
        </section>`;
      }
    }

    // The governor at the top of every tab, and on the state side the officers below.
    const gov = after ? governorOf(st) : null;
    if (gov) shown.push(gov);
    const officers = after && m.level === 'state' ? statewideOfficers(st) : [];
    shown.push(...officers);
    const top = after
      ? html`${gov ? html`<div style="margin-bottom:24px">${personCard(gov, { level: 'state', eyebrow: L('Gouverneur', 'Governor'), wide: true })}</div>` : ''}
        ${m.level === 'state' ? officersSection(st) : ''}`
      : html`${governor ? html`<div style="margin-bottom:20px">${compactRace(governor, { label: L('À l’échelle de l’État · Gouverneur', 'Statewide · Governor') })}</div>` : ''}
        ${m.level === 'state' && st !== 'DC' ? officesSection(st) : ''}`;

    // One credits list for the people pictured; a district's person brings their own.
    const credits = after ? photoCredits(shown.filter((p) => p.status === 'elected' || p.status === 'holder')) : photoCredits([
      ...(governor && !fc(governor).open ? fc(governor).cands.slice(0, 2) : []),
      ...(senate && m.level === 'federal' && m.chamber === 'senate' ? fc(senate).cands : []),
    ]);
    return html`<div class="wrap page">
      <nav class="crumbs" aria-label="${L('Fil d’Ariane', 'Breadcrumb')}"><a href="#/">${L('Accueil', 'Home')}</a><span>/</span><span>${stateName(st)}</span></nav>
      <div class="state-head">
        <div><div class="eyebrow">${electionDateLabel()}</div><h1 style="margin:6px 0 10px">${stateName(st)}</h1><div class="ballot-chips">${chips(st)}</div></div>
        <a class="btn" href="#how-to-vote" data-scroll="how-to-vote">${icon.ballot()} ${voteCardLabel(st)}</a>
      </div>
      ${toggles(st, m)}
      ${top}
      ${body}
      <div id="how-to-vote" style="margin-top:28px">${howToVote(st)}</div>
      ${credits ? html`<div style="margin-top:20px" id="state-credits">${credits}</div>` : ''}
    </div>`;
  },

  async mount(root, ctx) {
    const st = ctx.params[0];
    if (!STATE_BY_ABBR[st]) return null;
    const cleanup = wireCompare(root);
    mountRaceTabs(root);
    root.querySelector('[data-scroll]')?.addEventListener('click', (e) => {
      e.preventDefault();
      root.querySelector('#how-to-vote').scrollIntoView({ behavior: 'smooth' });
    });
    const mapEl = root.querySelector('#district-map');
    if (!mapEl) return cleanup;
    const m = parseMode(st, ctx.query);
    if (m.level === 'state' && resultsIn()) return mountMembers(root, ctx, st, m, cleanup);

    let features, races;
    if (m.level === 'federal') {
      features = await loadLayer(st, 'cd');
      races = new Map(houseRaces(st).map((r) => [r.district, r]));
    } else {
      const data = await legislativeRaces(st, m.chamber);
      features = data.features;
      races = data.races;
    }
    if (!root.isConnected) return cleanup;

    const raceFor = (f) => races.get(f.id) || null;
    const panel = root.querySelector('#district-race');
    const list = root.querySelector('#district-list');
    const up = [...races.values()].filter(Boolean);
    // After the election the House map shows who was elected in every district.
    const elected = m.level === 'federal' && resultsIn();
    root.querySelector('#district-count').textContent = elected
      ? L(`${up.length} circonscription${up.length === 1 ? '' : 's'}`, `${up.length} district${up.length === 1 ? '' : 's'}`)
      : L(`${up.length} circonscriptions sur ${features.features.length} votent en 2026`, `${up.length} of ${features.features.length} districts elect in 2026`);

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
    const showResults = () => elected;
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
        const name = districtNameL(r ? r.districtName : f.properties.n);
        if (!r) return html`<div class="t-title">${name}</div><div class="faint small">${L('Pas d’élection en 2026', 'No election in 2026')}</div>`;
        const ff = fc(r);
        if (showResults()) {
          const res = r.result;
          const rows = (res?.rows || []).filter((x) => !x.other).slice().sort((a, b) => (b.final ?? b.pct ?? 0) - (a.final ?? a.pct ?? 0)).slice(0, 3);
          const won = new Set(res?.winners || []);
          const w = res?.status === 'won' ? resultWinners(r)[0] : null;
          return html`<div class="t-title">${name}</div>
            ${w ? html`<div class="t-row"><span>${L('Élu en 2026', 'Elected 2026')}</span><b>${w.name} (${partyLetter(w.party)})${res.flip ? L(' · bascule', ' · flip') : ''}</b></div>` : ''}
            ${rows.length ? rows.map((x) => html`<div class="t-row"><span>${won.has(x.id) ? html`${icon.check()} ` : ''}${x.name} (${x.party || '?'})</span><b>${(x.final ?? x.pct) != null ? fmtPct(x.final ?? x.pct) : '—'}</b></div>`) : html`<div class="faint small">${L('Pas encore de décompte publié', 'No vote count posted yet')}</div>`}
            ${w ? '' : html`<div class="t-row"><span>${L('Résultat', 'Result')}</span><b>${!res ? L('Pas encore connu', 'Not in yet') : res.status === 'runoff' ? L('Second tour', 'Runoff') : L('Pas encore proclamé', 'Not called yet')}</b></div>`}
            <div class="tiny faint" style="margin-top:6px">${L('Cliquez pour voir la personne élue et comparer vos opinions', 'Click to see who was elected and compare views')}</div>`;
        }
        if (ff.kind === 'field') {
          const incs = (r.incumbents || []).filter((i) => i.name);
          return html`<div class="t-title">${name}</div>
            ${r.pres24 != null ? html`<div class="t-row"><span>${L('Présidentielle 2024', '2024 president')}</span><b>${fmtDR(r.pres24)}</b></div>` : ''}
            ${incs.length ? html`<div class="t-row"><span>${L('Détenu par', 'Held by')}</span><b>${incs.map((i) => `${lastName(i.name)} (${i.party || '?'})`).join(', ')}</b></div>` : ''}
            <div class="t-row"><span>${L('Candidatures', 'Candidates')}</span><b>${ff.cands.length || L('pas encore listées', 'not listed yet')}</b></div>
            ${r.consensus ? html`<div class="t-row"><span>${L('Analystes', 'Forecasters')}</span><b>${ratingL(ff.rating)}</b></div>` : ''}`;
        }
        if (ff.open) return html`<div class="t-title">${name}</div><div class="t-row"><span>${L('Primaire ouverte', 'Open primary')}</span><b>${L(`${ff.cands.length} candidatures`, `${ff.cands.length} candidates`)}</b></div><div class="t-row"><span>${L('Analystes', 'Forecasters')}</span><b>${ratingL(ff.rating)}</b></div>`;
        return html`<div class="t-title">${name}</div>${ff.cands.slice(0, 2).map((c) => html`<div class="t-row"><span>${c.name} (${c.party})</span><b>${fmtPct(c.share)}</b></div>`)}<div class="t-row"><span>${ratingL(ff.rating)}</span><b>${fmtProb(ff.pLead)}</b></div>`;
      },
      onSelect: (f) => select(f.id, true),
      labelFor: few ? (f) => String(parseInt(f.id, 10) || f.id) : null,
      regionLabel: (f) => {
        const r = raceFor(f);
        const sep = L(' : ', ': ');
        if (r && showResults() && r.format !== 'field') return `${districtNameL(r.districtName)}${sep}${districtResult(r, { full: true }).text}`;
        return r ? `${districtNameL(r.districtName)}${sep}${r.format === 'field' ? leadStr(fc(r)) : ratingL(fc(r).rating)}` : `${districtNameL(f.properties.n)}${sep}${L('pas d’élection en 2026', 'no election in 2026')}`;
      },
      zoomable: true,
      ariaLabel: elected ? L('Carte des circonscriptions, colorée selon le parti de la personne élue en 2026', 'District map colored by the party of the person elected in 2026') : L('Carte des circonscriptions', 'District map'),
    });
    const notUp = `<span><i style="background:${cssVar('--not-up')}"></i>${L('Pas d’élection en 2026', 'No election in 2026')}</span>`;
    const sw = (c, label) => `<span><i style="background:${c}"></i>${label}</span>`;
    const resultsLegend = () => resultsLegendHTML({
      other: up.some((r) => r.result?.status === 'won' && !['D', 'R'].includes(resultParty(r))),
      flips: up.some((r) => r.result?.flip), counting: up.some((r) => r.result?.status === 'counting'),
      runoff: up.some((r) => r.result?.status === 'runoff'), extra: '',
    });
    root.querySelector('#district-legend').innerHTML = !field.length
      ? (showResults() ? resultsLegend() : ratingLegendHTML(notUp))
      : byLean
        ? `<div class="map-legend"><span class="faint">${L('Présidentielle 2024 :', '2024 president:')}</span>${[['R', 1, L('R+15 ou plus', 'R+15 or more')], ['R', 0.68, L('R+7 à 15', 'R+7 to 15')], ['R', 0.4, L('R+3 à 7', 'R+3 to 7')], [null, 0, L('Moins de 3', 'Within 3')], ['D', 0.4, L('D+3 à 7', 'D+3 to 7')], ['D', 0.68, L('D+7 à 15', 'D+7 to 15')], ['D', 1, L('D+15 ou plus', 'D+15 or more')]]
          .map(([p, t, label]) => sw(d3.interpolateLab(mid, pole(p))(t), label)).join('')}${notUp}</div>`
        : `<div class="map-legend"><span class="faint">${L('Siège actuellement détenu par :', 'Seat now held by:')}</span>${sw(d3.interpolateLab(mid, pole('R'))(0.68), L('Républicain', 'Republican'))}${sw(d3.interpolateLab(mid, pole('D'))(0.68), L('Démocrate', 'Democrat'))}${sw(mid, L('Autre, partagé, vacant ou non indiqué', 'Other, split, vacant or not listed'))}${notUp}</div>`;

    const fillList = () => {
      list.innerHTML = features.features.map((f) => {
        const r = raceFor(f);
        const label = districtNameL(r ? r.districtName : cleanDistrictName(f.properties.n));
        if (!r) return String(html`<span class="district-btn not-up"><span class="dn">${label}</span><span class="tiny faint">${L('Pas d’élection en 2026', 'No 2026 race')}</span></span>`);
        const ff = fc(r);
        if (showResults() && r.format !== 'field') {
          const dr = districtResult(r, { full: true });
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
      map.refill();
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
        panel.innerHTML = String(emptyState(L('Pas d’élection ici en 2026', 'No election here in 2026'), L('Le siège de cette circonscription n’est pas en jeu cette année en raison des mandats échelonnés.', 'This district’s seat is not on the ballot this year because of staggered terms.')));
        return;
      }
      if (elected) {
        const p = fromRace(r);
        panel.innerHTML = String(html`${personCard(p, { level: 'federal', eyebrow: districtNameL(r.districtName), wide: true })}
          ${p.status === 'elected' ? photoCredits([p]) : ''}`);
      } else {
        panel.innerHTML = String(html`<section class="card" style="padding:clamp(16px,3vw,28px)">${raceFull(r, { tag: 'h2' })}</section>`);
        mountRaceTabs(panel);
      }
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
    const closeResult = elected ? up.filter((r) => resultMargin(r))
      .sort((a, b) => (a.result.status === 'won') - (b.result.status === 'won') || resultMargin(a).pts - resultMargin(b).pts)[0] : null;
    const start = ctx.query.d && races.has(ctx.query.d) ? ctx.query.d
      : (closeField || closeResult || up.find((r) => !r.demo) || up.slice().sort((a, b) => Math.abs((fc(a).pLead ?? 1) - 0.5) - Math.abs((fc(b).pLead ?? 1) - 0.5))[0])?.district;
    if (start) select(start, false);
    // A district asked for in the address (a click on the home map): zoom to it and show
    // its member, once per address, so the 10-minute redraws don't jump.
    if (start && ctx.query.d === start && scrolledFor !== location.hash) {
      scrolledFor = location.hash;
      map.zoomTo(start);
      setTimeout(() => panel.scrollIntoView({ block: 'start', behavior: 'instant' }), 0); // after the router's scroll to the top
    }
    return cleanup;
  },
};
