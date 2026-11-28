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

import { html, raw, fetchJSON, fmtDate, fmtDR, fmtPct } from '../util.js';
import { icon } from '../icons.js';
import { STATE_BY_ABBR, stateName, chamberOf, inState as inStateL } from '../data/states.js';
import { allRaces, getRace, raceTitle, resultWinners, officeNameL } from '../data/world.js';
import { candBadge, photoCredits } from '../components/race.js';
import { L, lang } from '../i18n.js';

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
// "(siège démocrate)" and "Primaires démocrates": the French words agree with "siège" and "primaires".
const SEAT_FR = { D: 'démocrate', R: 'républicain', L: 'libertarien', G: 'vert', I: 'indépendant' };
const PRIMARY_FR = { D: 'Primaires démocrates', R: 'Primaires républicaines', L: 'Primaires libertariennes', G: 'Primaires vertes', I: 'Primaires indépendantes' };
const FILTERS = {
  all: 'All offices', federal: 'President and Congress', governor: 'Governors', statewide: 'Other statewide offices',
  legislature: 'State legislatures', local: 'Mayors and county offices',
};
const FILTER_FR = { all: 'Tous les postes', federal: 'Présidence et Congrès', governor: 'Gouverneurs', statewide: 'Autres postes de l’État',
  legislature: 'Assemblées des États', local: 'Maires et postes de comté' };
const FEDERAL = new Set(['president', 'senate', 'house']);
const GROUPS = [
  ['president', 'President'], ['senate', 'U.S. Senate'], ['house', 'U.S. House'], ['governor', 'Governor'],
  ['lieutenant-governor', 'Lieutenant governor'], ['attorney-general', 'Attorney general'],
  ['secretary-of-state', 'Secretary of state'], ['treasurer', 'Treasurer'], ['auditor', 'Auditor or comptroller'],
  ['agriculture', 'Agriculture commissioner'], ['insurance', 'Insurance commissioner'],
  ['superintendent', 'Superintendent of education'], ['labor', 'Labor commissioner'], ['lands', 'Public lands commissioner'],
  ['supreme-court', 'State supreme court'], ['legislature', 'State legislature'], ['county', 'County offices'], ['mayor', 'Mayor'],
];
const GROUP_FR = {
  president: 'Présidence', senate: 'Sénat des États-Unis', house: 'Chambre des représentants', governor: 'Gouverneur',
  'lieutenant-governor': 'Lieutenant-gouverneur', 'attorney-general': 'Procureur général', 'secretary-of-state': 'Secrétaire d’État',
  treasurer: 'Trésorier', auditor: 'Auditeur ou contrôleur', agriculture: 'Commissaire à l’agriculture', insurance: 'Commissaire aux assurances',
  superintendent: 'Surintendant de l’éducation', labor: 'Commissaire au travail', lands: 'Commissaire aux terres publiques',
  'supreme-court': 'Cour suprême de l’État', legislature: 'Assemblée de l’État', county: 'Postes de comté', mayor: 'Maire',
};
// The 2026 race of the same office, where the site has one (two-year terms: New Hampshire's
// and Vermont's governors, Vermont's statewide officers).
const CODE_2026 = { governor: 'GOV', 'lieutenant-governor': 'LG', 'attorney-general': 'AG', 'secretary-of-state': 'SOS', treasurer: 'TREAS', auditor: 'AUD' };
const NUMBER = ['', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen'];
const NUMBER_FR = ['', 'un', 'deux', 'trois', 'quatre', 'cinq', 'six', 'sept', 'huit', 'neuf', 'dix', 'onze', 'douze', 'treize', 'quatorze', 'quinze'];
const s_ = (n) => (n > 1 ? 's' : '');
// "Louisiana State Senate" -> "Sénat de l’État de Louisiane": the chamber's own name after the state's.
function chamberL(ch) {
  const st = STATE_BY_ABBR[ch.state]?.name;
  return st && ch.officeName.startsWith(`${st} `) ? chamberOf(ch.state, ch.officeName.slice(st.length + 1)) : ch.officeName;
}
// Wikipedia's statuses (and plansText's plainer words) in French; anything else stays as written.
const STATUS_FR = [
  [/^The appointee’s plans aren’t known yet$/, 'Les intentions de la personne nommée ne sont pas encore connues'],
  [/^Running for another term$|^Running$/i, 'Candidature à un nouveau mandat'],
  [/^Can run again; no announcement yet$/, 'Peut se représenter ; pas encore d’annonce'],
  [/^Hasn’t announced plans yet$/, 'N’a pas encore annoncé ses intentions'],
  [/^Plans not listed yet$/, 'Intentions pas encore indiquées'],
  [/^Term-limited \(22nd Amendment\)$/i, 'A atteint la limite de mandats (22e amendement)'],
  [/^Term-limited$/i, 'A atteint la limite de mandats'],
  [/^Not running again$/i, 'Ne se représente pas'],
  [/^Retiring to run for governor$/i, 'Se retire pour briguer le poste de gouverneur'],
  [/^Retiring to run for lieutenant governor$/i, 'Se retire pour briguer le poste de lieutenant-gouverneur'],
  [/^Retiring$/i, 'Se retire'],
  [/^Running for another office$/i, 'Candidature à un autre poste'],
  [/^Running for governor$/i, 'Candidature au poste de gouverneur'],
  [/^Running for secretary of state$/i, 'Candidature au poste de secrétaire d’État'],
  [/^Resigned before the end of the term; a special election fills the seat$/, 'A démissionné avant la fin du mandat ; une élection partielle pourvoit le siège'],
  [/^Resigned$/i, 'A démissionné'],
  [/^To be filled by appointment until the special election$/, 'Pourvu par nomination jusqu’à l’élection partielle'],
  [/^A new office, elected for the first time in (\d{4})$/, 'Un nouveau poste, pourvu pour la première fois en $1'],
];
const statusL = (s) => {
  if (lang() !== 'fr' || !s) return s;
  const hit = STATUS_FR.find(([re]) => re.test(s));
  return hit ? s.replace(hit[0], hit[1]) : s;
};
const DATE_NOTE_FR = { 'Louisiana’s first round: if no one wins a majority, the top two meet in a runoff.': 'Premier tour en Louisiane : si personne n’obtient la majorité, les deux candidatures arrivées en tête s’affrontent au second tour.' };
// "2016 (special)" -> "2016 (partielle)"; "60.7% R" -> "60,7 % R".
const yearsL = (s) => L(s.replace(/\(special\)/g, '(partielle)').replace(/\(appointed\)/g, '(nomination)').replace(/\blost\b/g, 'perdue'), s);
const shareL = (s) => (lang() === 'fr' ? s.replace(/(\d+(?:\.\d+)?)%/g, (_, n) => fmtPct(+n, (n.split('.')[1] || '').length)) : s);
const sinceL = (s) => {
  if (lang() !== 'fr') return s;
  const d = /^[A-Z][a-z]+ \d{1,2}, \d{4}$/.test(s) ? new Date(s) : null;
  return d && !Number.isNaN(+d) ? `le ${fmtDate(d)}` : s;
};
const partyLetter = (p) => (p && p.length <= 2 ? p : p ? p.slice(0, 3) : '');
const partyColor = (p) => (p === 'D' ? 'var(--dem)' : p === 'R' ? 'var(--rep)' : 'var(--other)');
const dot = (p) => html`<span class="pdot ${p === 'D' || p === 'R' ? p : ''}" aria-hidden="true"></span>`;
const ymd = (s) => { const [y, m, d] = s.split('-').map(Number); return new Date(y, m - 1, d); };
const weekday = (s) => ymd(s).toLocaleDateString(lang() === 'fr' ? 'fr-FR' : 'en-US', { weekday: 'long' });
// "Tuesday, November 2, 2027" / "Mardi 2 novembre 2027".
const dayDate = (s) => (lang() === 'fr' ? `${weekday(s).charAt(0).toUpperCase()}${weekday(s).slice(1)} ${fmtDate(s)}` : `${weekday(s)}, ${fmtDate(s)}`);
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
      ${bio && info.bio ? html`<p class="up-bio" lang="en">${info.bio}</p>` : ''}
      ${site ? html`<div class="tiny"><a href="${site}" target="_blank" rel="noopener noreferrer">${p.site ? L('Site de campagne', 'Campaign site') : L('Site web', 'Website')} ${icon.external()}</a> <span class="faint">${hostOf(site)}</span></div>` : ''}
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

const termsText = (r) => (r.terms ? L(`${NUMBER_FR[r.terms] || r.terms} mandat${s_(r.terms)} jusqu’ici`, `${NUMBER[r.terms] || r.terms} term${r.terms > 1 ? 's' : ''} so far`) : '');

function holderLine(r) {
  const h = r.holder || {};
  const prev = CODE_2026[r.office] && r.state ? getRace(`${r.state}-${CODE_2026[r.office]}`) : null;
  const won = prev ? resultWinners(prev) : [];
  const plans = statusL(plansText(r));
  const label = r.office === 'president' ? L('À la présidence aujourd’hui', 'President now') : r.office === 'mayor' ? L('Maire aujourd’hui', 'Mayor now') : L('En poste aujourd’hui', 'Holds the office now');
  const names = won.map((w, i) => html`${i ? ', ' : ''}${w.name} (${partyLetter(w.party)})`);
  const prevLine = prev && h.name ? html`<div class="small"><span class="faint">2026${L(' :', ':')}</span> ${won.length
    ? (lang() === 'fr' ? html`victoire de ${names} · <a href="#/race/${encodeURIComponent(prev.id)}">voir le résultat</a>` : html`${names} won · <a href="#/race/${encodeURIComponent(prev.id)}">see the result</a>`)
    : html`<a href="#/race/${encodeURIComponent(prev.id)}">${raceTitle(prev)}</a>${L(', pas encore attribuée', ', not called yet')}`}</div>` : '';
  if (h.name) {
    return html`<div class="stack-sm"><div class="tiny faint up-label">${label}</div>
      ${who(h, { note: [termsText(r), plans].filter(Boolean).join(' · ') })}${prevLine}</div>`;
  }
  if (h.appointment) {
    // The departing senator holds the seat until they resign; an appointee then serves
    // until the special election.
    return html`<div class="small"><span class="faint">${L('Jusqu’à l’élection :', 'Until the election:')}</span> <span class="up-who-inline">${dot(h.party)}<span>${L('une personne nommée, pas encore désignée', 'an appointee, still to be named')}${h.party ? html` <span class="faint">(${L(`siège ${SEAT_FR[h.party] || h.party}`, `${PARTY[h.party] || h.party} seat`)})</span>` : ''}</span></span>${plans ? html` <span class="muted">· ${plans}</span>` : ''}</div>`;
  }
  if (prev) {
    // Two-year offices whose 2026 winner Wikipedia's table doesn't name yet: our own
    // 2026 result says who (a winner is only ever a check-marked call).
    if (won.length) {
      return html`<div class="stack-sm"><div class="tiny faint up-label">${L('Victoire en 2026', 'Elected in 2026')}</div>${won.map((w) => who(w))}
        <div class="small"><a href="#/race/${encodeURIComponent(prev.id)}">${L('Voir le résultat', 'See the result')}</a></div></div>`;
    }
    return html`<div class="small"><span class="faint">${label}${L(' :', ':')}</span> ${L('dépend de l’élection de 2026,', 'decided by the 2026 race,')} <a href="#/race/${encodeURIComponent(prev.id)}">${L('pas encore attribuée', 'not called yet')}</a></div>`;
  }
  if (/^A new office\b/.test(r.statusText || '')) {
    // Los Angeles County's executive, first elected in 2028: nobody to list yet.
    return html`<div class="small"><span class="faint">${label}${L(' :', ':')}</span> ${L('personne pour l’instant.', 'no one yet.')} <span class="muted">${statusL(r.statusText)}.</span></div>`;
  }
  return html`<div class="small"><span class="faint">${label}${L(' :', ':')}</span> <span class="faint">${L('pas encore d’information', 'not listed yet')}</span>${plans ? html` <span class="muted">· ${plans}</span>` : ''}</div>`;
}

function record(r) {
  const parts = [];
  if (r.firstElected) {
    const years = r.firstElected.replace(/\s+(?=\d{4})/g, ', ');
    // The tables' "First elected" column: Louisiana's governor was elected in 2023 and
    // took office in 2024.
    parts.push(r.office === 'senate' ? L(`${/lost/.test(years) ? 'Élections au Sénat' : 'Élections remportées'} : ${yearsL(years)}`, `${/lost/.test(years) ? 'Senate races' : 'Elected'} ${years}`) : L(`Première élection : ${yearsL(years)}`, `First elected ${years}`));
  } else if (r.since) parts.push(L(`En poste depuis ${sinceL(r.since)}`, `In office since ${r.since}`));
  if (r.lastRace && /\d/.test(r.lastRace)) parts.push(L(`dernière élection : ${shareL(r.lastRace)}`, `last race ${r.lastRace}`));
  return parts.length ? html`<div class="small faint">${parts.join(' · ')}</div>` : '';
}

function peopleList(list, { incumbentNote = true } = {}) {
  // Long fields (a big city's mayoral race) keep each person to a line or two, and the
  // officeholder's bio is already in the line above.
  const bio = list.length <= 6;
  return html`<div class="up-people">${list.map((c) => who(c, { note: incumbentNote && c.incumbent ? L('en poste', 'incumbent') : '', bio: bio && !c.incumbent }))}</div>`;
}

function declared(r) {
  if (r.office === 'president') {
    const by = (p) => r.candidates.filter((c) => c.party === p);
    const rows = (r.primaries || []).map((pr) => {
      const people = by(pr.party);
      return html`<div class="small"><div class="tiny faint up-label">${L(PRIMARY_FR[pr.party] || `Primaires (${pr.party})`, `${PARTY[pr.party] || pr.party} primaries`)}</div>${people.length
        ? html`<div class="up-people">${people.map((c) => who(c, { note: [c.home, c.announced ? L(`candidature annoncée le ${fmtDate(c.announced)}`, `announced ${fmtDate(c.announced)}`) : ''].filter(Boolean).join('; ') }))}</div>`
        : html`<span class="muted">${L('Aucune candidature déclarée pour l’instant', 'No one has declared yet')}</span>`}</div>`;
    });
    const others = r.candidates.filter((c) => !(r.primaries || []).some((pr) => pr.party === c.party));
    return html`${rows}${others.length ? html`<div class="small"><div class="tiny faint up-label">${L('Autres', 'Others')}</div>${peopleList(others)}</div>` : ''}`;
  }
  if (!r.candidates.length) {
    return html`<div class="small muted">${r.office === 'mayor' && !r.page ? L('Les candidatures ne sont pas encore listées', 'Candidates aren’t listed yet') : L('Aucune candidature déclarée pour l’instant', 'No declared candidates yet')}</div>`;
  }
  return html`<div class="small"><div class="tiny faint up-label">${L('Candidatures déclarées', 'Declared')} · ${r.candidates.length}</div>${peopleList(r.candidates)}</div>`;
}

const sameOffice = (a, b) => a.toLowerCase().replace(/^(state|u\.s\.)\s+/, '') === b.toLowerCase().replace(/^(state|u\.s\.)\s+/, '');

function titleOf(r) {
  if (r.office === 'president') return L('Présidence des États-Unis', 'President of the United States');
  if (r.office === 'mayor') return `${r.place}, ${stateName(r.state)}`;
  if (r.office === 'county') return `${r.county}, ${stateName(r.state)}`;
  return stateName(r.state);
}

function dateLine(r) {
  if (!r.date) return html`<div class="small faint">${L('Date pas encore indiquée', 'Date not listed yet')}</div>`;
  return html`<div class="small"><b>${dayDate(r.date)}</b>${r.dateNote ? html` <span class="muted">· ${L(DATE_NOTE_FR[r.dateNote] || r.dateNote, r.dateNote)}</span>` : ''}</div>`;
}

function sourceLine(r) {
  const asOf = r.source?.asOf ? fmtDate(r.source.asOf.slice(0, 10)) : '';
  const bits = [];
  if (r.page) bits.push(ext(r.page.url, L('En savoir plus sur Wikipédia (en anglais)', 'More on Wikipedia')));
  if (r.holderSource && !r.page) bits.push(html`${L('titulaire d’après', 'officeholder from')} ${ext(r.holderSource.url, r.holderSource.title.replace(/^Wikipedia: /, '').replace(/, infobox$/, ''))}`);
  if (asOf) {
    // Without a page of its own, the list it comes from is the link (mayors, 2028's
    // attorneys general).
    const what = r.source.note || r.office === 'mayor' ? L('Liste de Wikipédia', 'Wikipedia’s list') : r.level ? L('Wikipédia', 'Wikipedia') : L('Tableau de Wikipédia', 'Wikipedia’s table');
    bits.push(html`${!r.page && r.source.url ? ext(r.source.url, what) : what} ${L('au', 'as of')} ${asOf}`);
  }
  return bits.length ? html`<div class="tiny faint">${bits.map((b, i) => html`${i ? ' · ' : ''}${b}`)}</div>` : '';
}

export function card(r, groupLabel = null, { showDate = false } = {}) {
  if (r.office === 'house') {
    return html`<article class="card up-card">
      ${groupLabel ? '' : html`<div class="eyebrow">${L('Chambre des représentants', 'U.S. House')}</div>`}
      <h3 style="margin:0">${L(`Les ${r.seats || 435} sièges`, `All ${r.seats || 435} seats`)}</h3>
      ${showDate ? dateLine(r) : ''}
      <div class="small muted">${lang() === 'fr' ? html`Tous les sièges de la Chambre sont renouvelés tous les deux ans. Le mandat de la Chambre élue le 3 novembre 2026 court jusqu’au 3 janvier ${r.year + 1} ; voir <a href="#/congress">qui siège au Congrès</a>.` : html`Every House seat is up every two years. The members elected on November 3, 2026, serve until January 3, ${r.year + 1}; see <a href="#/congress">who sits in Congress</a>.`}</div>
      <div class="small muted">${L('Les candidatures ne sont pas encore listées.', 'Candidates aren’t listed yet.')}</div>
    </article>`;
  }
  if (r.office === 'legislature') return chamberCard(r, { showDate, groupLabel });
  return html`<article class="card up-card">
    <div class="row between" style="gap:8px;align-items:flex-start">
      <div>${groupLabel && sameOffice(r.officeName, groupLabel) ? '' : html`<div class="eyebrow">${officeNameL(r.officeName)}</div>`}<h3 style="margin:2px 0 0">${titleOf(r)}</h3></div>
      ${r.special ? html`<span class="chip">${L('Élection partielle', 'Special election')}</span>` : ''}
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
  if (lang() === 'fr') {
    return [n.R ? `${n.R} siège${s_(n.R)} républicain${s_(n.R)}` : '', n.D ? `${n.D} siège${s_(n.D)} démocrate${s_(n.D)}` : '',
      n.other ? `${n.other} autre${s_(n.other)} ou vacant${s_(n.other)}` : ''].filter(Boolean).join(', ');
  }
  return [n.R ? `${n.R} Republican${n.R > 1 ? 's' : ''}` : '', n.D ? `${n.D} Democrat${n.D > 1 ? 's' : ''}` : '',
    n.other ? `${n.other} other${n.other > 1 ? 's' : ''} or vacant` : ''].filter(Boolean).join(', ');
}

function chamberCard(ch, { showDate = false, groupLabel = null } = {}) {
  const members = Object.values(ch.districts || {}).flat();
  const leaving = members.filter((m) => m.plans === 'leaving').length;
  const districts = Object.keys(ch.districts || {}).length;
  return html`<article class="card up-card">
    ${groupLabel ? '' : html`<div class="eyebrow">${L('Assemblée de l’État', 'State legislature')}</div>`}
    <h3 style="margin:2px 0 0">${chamberL(ch)}</h3>
    ${showDate ? dateLine(ch) : ''}
    <div class="small">${L(`Les ${ch.seats} sièges${districts !== ch.seats ? ` (${districts} circonscriptions)` : ''} sont en jeu. Aujourd’hui : ${partyCounts(members)}.`, `All ${ch.seats} seats${districts !== ch.seats ? ` (${districts} districts)` : ''} are up. Held now by ${partyCounts(members)}.`)}</div>
    ${leaving ? html`<div class="small muted">${L(`${leaving} membre${s_(leaving)} ne se représente${leaving > 1 ? 'nt' : ''} pas (limite de mandats ou retraite), d’après ce que Wikipédia liste jusqu’ici.`, `${leaving} member${leaving > 1 ? 's are' : ' is'} not running again (term limits or retirement), as Wikipedia lists them so far.`)}</div>` : ''}
    <div class="small"><a href="#/elections">${L('Voir votre circonscription dans Mes élections', 'See your own district in My elections')}</a></div>
    <div class="tiny faint">${ext(ch.page.url, L('En savoir plus sur Wikipédia (en anglais)', 'More on Wikipedia'))} · ${L('membres d’après', 'members from')} ${ext(ch.source.url, ch.source.title.replace(/^Wikipedia: /, '').replace(/, (members|results by district)$/, ''))}</div>
  </article>`;
}

function districtCard(ch, key) {
  const all = ch.districts[key] || [];
  const ms = all.filter((m) => m.name);
  const vacant = all.length - ms.length;
  const dr = ms.find((m) => m.dr != null)?.dr;
  // Always under My elections' "State legislature" heading, so no eyebrow of its own.
  return html`<article class="card up-card">
    <h3 style="margin:0">${L(`${chamberL(ch)}, circonscription ${key}`, `${ch.officeName}, District ${key}`)}</h3>
    ${dateLine(ch)}
    ${ms.length ? html`<div class="stack-sm"><div class="tiny faint up-label">${ms.length > 1 ? L('En poste aujourd’hui', 'Hold the seats now') : L('En poste aujourd’hui', 'Holds the seat now')}</div>
      ${ms.map((m) => who(m, { note: [m.firstElected ? L(`première élection en ${m.firstElected}`, `first elected ${m.firstElected}`) : '', statusL(m.statusText)].filter(Boolean).join(' · ') }))}</div>` : ''}
    ${vacant ? html`<div class="small">${lang() === 'fr' ? (ms.length ? `${vacant > 1 ? `${vacant} sièges sont vacants` : 'Un siège est vacant'} aujourd’hui.` : 'Le siège est vacant aujourd’hui.') : (ms.length ? `${vacant > 1 ? `${vacant} seats are` : 'One seat is'} vacant now.` : 'The seat is vacant now.')} <span class="muted">${L(`L’élection de ${ch.year} le pourvoira, sauf élection partielle avant.`, `The ${ch.year} election fills it, unless a special election comes first.`)}</span></div>` : ''}
    ${dr != null ? html`<div class="small faint">${L(`La circonscription a voté ${fmtDR(dr)} à la présidentielle de 2024.`, `The district voted ${fmtDR(dr)} for president in 2024.`)}</div>` : ''}
    <div class="small muted">${L('Tous les sièges de la chambre sont en jeu. Les candidatures ne sont pas encore listées circonscription par circonscription.', 'Every seat in the chamber is up. Candidates aren’t listed district by district yet.')}</div>
    <div class="tiny faint">${ext(ch.page.url, L('En savoir plus sur Wikipédia (en anglais)', 'More on Wikipedia'))} · ${L('membres d’après', 'members from')} ${ext(ch.source.url, ch.source.title.replace(/^Wikipedia: /, '').replace(/, (members|results by district)$/, ''))}</div>
  </article>`;
}

function summary(rs) {
  if (lang() === 'fr') return summaryFr(rs);
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
function summaryFr(rs) {
  const n = (k) => rs.filter((r) => r.office === k).length;
  const parts = [];
  if (n('president')) parts.push('la présidence');
  if (n('senate')) {
    const k = n('senate');
    const sp = rs.filter((r) => r.office === 'senate' && r.special).length;
    parts.push(`${k} siège${s_(k)} au Sénat${sp && sp < k ? ` (dont ${sp} lors d’une élection partielle)` : sp ? ' (lors d’une élection partielle)' : ''}`);
  }
  if (n('house')) parts.push('tous les sièges de la Chambre');
  if (n('governor')) parts.push(`${n('governor')} poste${s_(n('governor'))} de gouverneur`);
  const other = rs.filter((r) => kindOf(r) === 'statewide').length;
  if (other) parts.push(`${other} autre${s_(other)} poste${s_(other)} de l’État`);
  if (n('legislature')) parts.push(`${n('legislature')} chambre${s_(n('legislature'))} législative${s_(n('legislature'))}`);
  if (n('county')) parts.push(`${n('county')} poste${s_(n('county'))} de comté`);
  if (n('mayor')) parts.push(`${n('mayor')} mairie${s_(n('mayor'))}`);
  if (!parts.length) return '';
  let list = parts.length > 1 ? `${parts.slice(0, -1).join(', ')} et ${parts[parts.length - 1]}` : parts[0];
  list = list.charAt(0).toUpperCase() + list.slice(1);
  const states = new Set(rs.filter((r) => r.state).map((r) => r.state)).size;
  return `${list}${states ? `, dans ${states} État${s_(states)}` : ''}.`;
}

// Runoffs from 2026 still to come, from the race data (Louisiana's December runoffs).
function runoffs(stateF, officeF) {
  const rs = allRaces().filter((r) => !r.demo && r.result?.status === 'runoff')
    .filter((r) => (stateF === 'all' || r.state === stateF) && (officeF === 'all' || (officeF === 'federal' ? FEDERAL.has(r.office) : officeF === 'governor' ? r.office === 'governor' : officeF === 'statewide' && r.format === 'office')))
    .sort((a, b) => String(a.runoff || '').localeCompare(String(b.runoff || '')) || raceTitle(a).localeCompare(raceTitle(b)));
  if (!rs.length) return '';
  return html`<section class="stack" aria-labelledby="up-2026">
    <div><h2 id="up-2026" style="margin:0">${L('2026 : les seconds tours à venir', '2026: runoffs still ahead')}</h2>
      <p class="small muted" style="margin:4px 0 0">${L('Les élections du 3 novembre que personne n’a remportées d’emblée.', 'Races from November 3 that no one won outright.')}</p></div>
    <div class="up-grid">${rs.map((r) => {
      const adv = (r.result.advance || []).map((id) => r.candidates.find((c) => c.id === id)).filter(Boolean);
      return html`<article class="card up-card">
        <div class="eyebrow">${r.runoff ? L(`Second tour le ${weekday(r.runoff)} ${fmtDate(r.runoff)}`, `Runoff ${weekday(r.runoff)}, ${fmtDate(r.runoff)}`) : L('Second tour, date à fixer', 'Runoff, date to be set')}</div>
        <h3 style="margin:2px 0 0"><a href="#/race/${encodeURIComponent(r.id)}" style="text-decoration:none">${raceTitle(r)}</a></h3>
        ${adv.length ? html`<div class="small"><span class="faint">${L('Au second tour :', 'In the runoff:')}</span><ul class="up-who">${adv.map((c) => html`<li>${person(c)}</li>`)}</ul></div>` : ''}
        <div class="small"><a href="#/race/${encodeURIComponent(r.id)}">${L('Résultat du premier tour et candidatures', 'First-round result and the candidates')}</a></div>
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
    <summary><b>${L('Maires', 'Mayors')}</b> <span class="faint">· ${L(`${rs.length} autre${s_(rs.length)} ville${s_(rs.length)}, dates pas encore indiquées`, `${rs.length} more cit${rs.length > 1 ? 'ies' : 'y'}, dates not listed yet`)}</span></summary>
    <p class="small muted" style="margin:8px 0 0">${L('D’après la liste des élections de maires de l’année sur Wikipédia : qui est maire aujourd’hui, et si cette personne peut se représenter. Choisissez un État ci-dessus pour la fiche de chaque ville.', 'From Wikipedia’s list of this year’s mayoral elections: the mayor now and whether they can run again. Pick a state above for each mayor’s card.')}</p>
    <div class="up-mayor-grid">${[...byState].sort((a, b) => stateName(a[0]).localeCompare(stateName(b[0]), lang())).map(([st, list]) => html`<div>
      <h4 class="up-group" style="margin:0">${stateName(st)}</h4>
      <ul class="up-mayor-list">${list.map((r) => html`<li><b>${r.place}</b>${r.special ? L(' (partielle)', ' (special)') : ''} · ${r.holder?.name ? (r.holder.wiki ? ext(r.holder.wiki, r.holder.name) : r.holder.name) : L('pas d’information sur la mairie', 'mayor not listed')}${r.holder?.party ? html` <span class="faint">(${partyLetter(r.holder.party)})</span>` : ''}${r.statusText ? html` <span class="muted">· ${statusL(plansText(r))}</span>` : ''}</li>`)}</ul>
    </div>`)}</div>
  </details>`;
}

function groupBlock(list, { showDate = false } = {}) {
  return GROUPS.filter(([k]) => list.some((r) => r.office === k)).map(([k, label], _, shown) => {
    const group = list.filter((r) => r.office === k);
    const head = shown.length > 1 || group.length > 1;
    return html`<div class="stack-sm">
      ${head ? html`<h3 class="up-group">${L(GROUP_FR[k] || label, label)}${group.length > 1 ? html` <span class="faint">· ${group.length}</span>` : ''}</h3>` : ''}
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
        <div class="up-date"><b>${dayDate(d)}</b>${states.length && states.length <= 3 && list.every((r) => r.state) ? html` <span class="muted">· ${states.map(stateName).join(', ')}</span>` : ''}
          ${notes.map((n) => html`<div class="small muted">${L(DATE_NOTE_FR[n] || n, n)}</div>`)}</div>
        ${groupBlock(list)}
      </div>`;
    })}
    ${undated.length ? (stateF === 'all' ? mayorList(undated) : html`<div class="stack-sm">
      <div class="up-date"><b>${L('Dates pas encore indiquées', 'Dates not listed yet')}</b></div>${groupBlock(undated)}</div>`) : ''}
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
  title: () => L('Les prochaines élections', 'Upcoming elections'),
  async render(ctx) {
    const data = await loadUpcoming();
    const office = FILTERS[ctx.query.office] ? ctx.query.office : 'all';
    const stateF = ctx.query.state && (STATE_BY_ABBR[ctx.query.state] || ctx.query.state === 'DC') ? ctx.query.state : 'all';
    const keep = (r) => (stateF === 'all' || r.state === stateF || (!r.state && (office === 'all' || office === 'federal')))
      && (office === 'all' || kindOf(r) === office);
    const races = allOf(data).filter(keep);
    const years = data?.years || [];
    const states = Object.values(STATE_BY_ABBR).sort((a, b) => stateName(a.abbr).localeCompare(stateName(b.abbr), lang()));
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
      <div><div class="eyebrow">${L('Les prochaines élections', 'Upcoming elections')}</div>
        <h1 style="margin:6px 0 8px">${L('Les trois prochaines années', 'The next three years')}</h1>
        <p class="muted" style="margin:0">${lang() === 'fr'
          ? html`Les élections d’ici à ${years[years.length - 1] || 2029} pour la présidence, le Congrès, les postes de gouverneur et les autres postes de l’État, les assemblées des États et, là où Wikipédia les liste, les maires et les postes de comté : la date de chacune, qui occupe le poste et si cette personne peut ou veut se représenter, qui sont ces personnes, et les candidatures déclarées jusqu’ici. Pas encore de prévisions : ces élections ne sont ni cotées ni sondées si tôt. Lu chaque jour sur Wikipédia en anglais${data?.updated ? ` ; dernière mise à jour le ${fmtDate(data.updated)}` : ''}. <a href="#/elections">Mes élections</a> montre celles de votre propre bulletin.`
          : html`The elections from now through ${years[years.length - 1] || 2029} for president, Congress, governor and the other statewide offices, the state legislatures and, where Wikipedia lists them, mayors and county offices: when each is, who holds the office now and whether they can or will run again, who they are, and the candidates who have declared so far. No forecasts yet: these races aren’t rated or polled this early. Read every day from Wikipedia${data?.updated ? `; last updated ${fmtDate(data.updated)}` : ''}. <a href="#/elections">My elections</a> shows the ones on your own ballot.`}</p></div>
      ${!data ? html`<div class="empty">${icon.calendar()}<h3>${L('Les prochaines élections ne sont pas disponibles', 'The upcoming elections are unavailable')}</h3><p>${L('Lancez scripts/update_upcoming.py pour les construire.', 'Run scripts/update_upcoming.py to build them.')}</p></div>` : html`
      <div class="filters" role="group" aria-label="${L('Filtre', 'Filter')}">
        ${Object.entries(FILTERS).map(([k, l]) => html`<a class="chip" href="${q({ office: k })}" ${raw(k === office ? 'aria-current="page" style="background:var(--text-1);color:var(--bg);border-color:var(--text-1)"' : '')}>${L(FILTER_FR[k], l)}</a>`)}
        <label class="small faint" for="up-state" style="margin-left:4px">${L('État', 'State')}</label>
        <select id="up-state" class="input up-select">
          <option value="all" ${raw(stateF === 'all' ? 'selected' : '')}>${L('Tous les États', 'All states')}</option>
          ${states.map((s) => html`<option value="${s.abbr}" ${raw(s.abbr === stateF ? 'selected' : '')}>${stateName(s.abbr)}</option>`)}
        </select>
      </div>
      <nav class="filters small" aria-label="${L('Années', 'Years')}">${[...(run ? ['2026'] : []), ...years.map(String)].map((y) => html`<a class="chip" href="#/upcoming" data-jump="up-${y}">${y}</a>`)}</nav>
      ${run}
      ${years.map((y) => {
        const rs = races.filter((r) => r.year === y);
        return rs.length ? yearSection(y, rs, { stateF }) : html`<section class="stack" aria-labelledby="up-${y}"><h2 id="up-${y}" style="margin:0">${y}</h2><p class="small muted" style="margin:0">${stateF !== 'all' || office !== 'all' ? L('Rien ne correspond à ces filtres.', 'Nothing matching these filters.') : L('Aucune élection listée pour l’instant.', 'No elections listed yet.')}</p></section>`;
      })}
      ${photoCredits(peopleIn(shown))}
      <p class="tiny faint" style="margin:0">${L('Les dates sont celles du jour du scrutin (la Louisiane vote d’abord lors d’une primaire ouverte). Les primaires ont lieu plus tôt et ne sont pas listées. Les maires viennent de la liste de Wikipédia des élections municipales de chaque année, et les postes de comté seulement des pages de comté qu’elle possède (pour l’instant le procureur de district et le chef de l’exécutif du comté de Los Angeles) ; les procureurs de district ailleurs, les autres postes locaux et les sièges pourvus par circonscription sous l’assemblée de l’État ne sont pas encore couverts. Chaque biographie est le début de l’article Wikipédia en anglais de la personne (CC BY-SA), montré seulement quand le titre de l’article porte son nom ; les sites sont ceux de la campagne quand une page d’élection en donne un, sinon le site officiel de la personne sur Wikidata, et chacun est vérifié : il doit répondre et afficher le nom de la personne.', 'Dates are election days (Louisiana votes first in an open primary). Primaries come earlier and aren’t listed. Mayors come from Wikipedia’s list of each year’s mayoral elections, and county offices only from the county pages it has (so far Los Angeles County’s district attorney and county executive); district attorneys elsewhere, other local offices and seats elected by district below the legislature aren’t covered yet. Each bio is the start of the person’s Wikipedia article (CC BY-SA), shown only when the article’s title has their name; websites are the campaign’s where a race page lists one, else the person’s official site on Wikidata, and each is checked to answer and show the person’s name.')}</p>
      <details class="tiny faint"><summary style="cursor:pointer">${L(`Sources : ${sources.length} pages de Wikipédia en anglais (CC BY-SA)`, `Sources: ${sources.length} Wikipedia pages (CC BY-SA)`)}</summary>
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
    <div class="eyebrow">${L('Chambre des représentants', 'U.S. House')}</div>
    <h3 style="margin:2px 0 0">${prev ? raceTitle(prev) : L(`${stateName(st)} : votre circonscription`, `${stateName(st)}: your district`)}</h3>
    ${dateLine(r)}
    ${won.length ? html`<div class="stack-sm"><div class="tiny faint up-label">${L(`En poste à partir du 3 janvier ${r.year - 1}`, `Holds the seat from January 3, ${r.year - 1}`)}</div>
        ${won.map((w) => who(w, { note: L('victoire en 2026', 'elected in 2026') }))}
        <div class="small"><a href="#/race/${encodeURIComponent(prev.id)}">${L('Voir le résultat de 2026', 'See the 2026 result')}</a></div></div>`
      : prev ? html`<div class="small">${L('Le siège dépend de l’élection de 2026 :', 'Who holds the seat is decided by the 2026 race:')} <a href="#/race/${encodeURIComponent(prev.id)}">${prev.result?.status === 'runoff' ? L('second tour à venir', 'headed to a runoff') : L('pas encore attribuée', 'not called yet')}</a>.</div>` : ''}
    <div class="small muted">${L('Tous les sièges de la Chambre sont renouvelés tous les deux ans. Les candidatures ne sont pas encore listées.', 'Every House seat is up every two years. Candidates aren’t listed yet.')}</div>
  </article>`;
}

const LEVELS = [['federal', 'President and Congress'], ['statewide', 'Statewide'], ['legislature', 'State legislature'], ['local', 'Local']];
const LEVEL_FR = { federal: 'Présidence et Congrès', statewide: 'Postes de l’État', legislature: 'Assemblée de l’État', local: 'Local' };

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
      <div><h2 id="future-h" style="margin:0">${L('Élections à venir', 'Future elections')}</h2>
        <p class="small muted" style="margin:4px 0 0">${lang() === 'fr'
          ? html`Ce qui vous attend sur votre bulletin d’ici à ${last}, tel que Wikipédia le liste aujourd’hui : la date de chaque élection, qui occupe le poste et si cette personne peut se représenter, qui sont ces personnes, et les candidatures déclarées. Seules les années avec une élection pour votre État, vos circonscriptions${ad.place ? ', votre ville' : ''} ou votre comté sont listées. Les primaires, la plupart des postes locaux et les sièges pourvus par circonscription sous l’assemblée de l’État ne sont pas encore couverts. <a href="#/upcoming?state=${st}">Toutes les prochaines élections ${inStateL(st)}</a>.`
          : html`What’s ahead on your ballot through ${last}, as Wikipedia lists it today: when each election is, who holds the office now and whether they can run again, who they are, and who has declared. Only the years with an election for your state, districts${ad.place ? ', city' : ''} or county are listed. Primaries, most local offices and seats elected by district below the legislature aren’t covered yet. <a href="#/upcoming?state=${st}">Every upcoming election in ${stateName(st)}</a>.`}</p></div>
      ${years.map((y) => {
        const items = byYear.get(y).sort((a, b) => sortKey(a).localeCompare(sortKey(b)));
        return html`<details class="card future-year" data-year="${y}" ${raw(openYears.has(y) ? 'open' : '')}>
          <summary><span class="future-head"><span class="future-title">${L(`Élections à venir en ${y}`, `Future elections for ${y}`)}</span><span class="faint small">${L(`${items.length} élection${s_(items.length)}`, `${items.length} election${items.length > 1 ? 's' : ''}`)}</span></span>${icon.chevronDown()}</summary>
          <div class="stack" style="margin-top:14px">${LEVELS.filter(([k]) => items.some((it) => it.level === k)).map(([k, label]) => html`<div class="stack-sm">
            <h3 class="up-group">${L(LEVEL_FR[k], label)}</h3>
            <div class="up-grid">${items.filter((it) => it.level === k).map(cardFor)}</div>
          </div>`)}</div>
        </details>`;
      })}
    </section>`,
  };
}
