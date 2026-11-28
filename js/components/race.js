// Race-level building blocks shared by the state page, race page and lists.

import { html, raw, fmtPct, fmtInt, fmtProb, fmtDR, fmtMoney, fmtCompact, initials, fmtShortDate, fmtDate, timeAgo, fmtNum, pctSign } from '../util.js';
import { icon } from '../icons.js';
import { store } from '../store.js';
import { STATE_BY_ABBR, PARTY_REGISTRATION, stateName, deState, withState, inState } from '../data/states.js';
import { QUESTION_BY_ID, stanceSentence, questionsForLevel, qText } from '../data/questions.js';
import { fc, pollHist, changeOver, getRace, raceTitle, raceShortTitle, officeLabel, financeOf, hasFigures, earlyVoteOf, positionsOf, isDemo, racesMeta, photoOf,
  resultRows, resultWinners, resultAdvancing, resultMargin, rowShare, afterElection, liveFc, stillCounting, officeNameL, ratingL, certifiedRace, certPending, certifiedIn, certWait } from '../data/world.js';
import { L, lang } from '../i18n.js';
import { verdict, day } from '../model/forecast.js';
import { candColors, waffle, segments, stackedBar, lineChart, cssVar } from '../lib/charts.js';
import { SHOW_EARLY_VOTE } from '../config.js';

// Read in the visitor's language (getters), so the many `PARTY_NAME[c.party]` stay as they are.
const getters = (o) => Object.defineProperties({}, Object.fromEntries(Object.entries(o).map(([k, [fr, en]]) => [k, { get: () => L(fr, en), enumerable: true }])));
export const PARTY_NAME = getters({ D: ['Démocrate', 'Democrat'], R: ['Républicain', 'Republican'], L: ['Libertarien', 'Libertarian'], G: ['Vert', 'Green'], I: ['Indépendant', 'Independent'], N: ['Non partisan', 'Nonpartisan'] });
export const PARTY_PLURAL = getters({ D: ['démocrates', 'Democrats'], R: ['républicains', 'Republicans'] });
export const partyClass = (p) => (p === 'D' || p === 'R' ? `party-${p}` : 'party-x');
export const lastName = (n) => n.replace(/\s+(Jr\.|Sr\.|II|III|IV)$/, '').split(' ').slice(-1)[0];
export const demoChip = (on = true) => (on ? html`<span class="demo-chip" title="${L('Données de démonstration fictives : ni un vrai candidat ni un vrai sondage', 'Fictional demo data, not a real candidate or poll')}">${L('Démo', 'Demo')}</span>` : '');
// Demo races get the DEMO tag. Real races are either refreshed automatically from
// public sources ("Live data") or also hand-researched ("Sourced").
export function dataChip(x) {
  if (isDemo(x)) return demoChip();
  if (x.office && !x.research) return html`<span class="live-chip" title="${L('Les candidats, les cotes des analystes, les sondages et les levées de fonds sont mis à jour automatiquement toutes les 8 heures à partir de sources publiques. Les positions des membres actuels de la Chambre viennent de leurs votes ; les autres positions sont recherchées élection par élection.', 'Candidates, forecaster ratings, polls and fundraising refresh automatically every 8 hours from public sources. Current House members’ positions come from their recorded votes; other issue positions are researched race by race.')}">${L('Données en direct', 'Live data')}</span>`;
  return html`<span class="real-chip" title="${L('Données recherchées : chaque chiffre et chaque position renvoie à sa source', 'Researched data: every figure and position links to its source')}">${L('Sourcé', 'Sourced')}</span>`;
}
const ext = (href, label) => html`<a href="${href}" target="_blank" rel="noopener noreferrer">${label} ${icon.external()}</a>`;

export function starBtn(raceId, { small = false } = {}) {
  const on = store.isStarred(raceId);
  return html`<button type="button" class="toggle-icon star${small ? ' sm' : ''}" data-star="${raceId}" aria-pressed="${String(on)}" aria-label="${on ? L('Retirer des élections suivies', 'Remove from starred elections') : L('Suivre cette élection', 'Star this election')}" title="${on ? L('Suivie', 'Starred') : L('Suivre cette élection', 'Star this election')}">${on ? icon.starFill() : icon.star()}</button>`;
}
export function heartBtn(candId, name, { small = false } = {}) {
  const on = store.isLiked(candId);
  return html`<button type="button" class="toggle-icon heart${small ? ' sm' : ''}" data-like="${candId}" data-name="${name}" aria-pressed="${String(on)}" aria-label="${on ? L(`Retirer ${name} des candidats favoris`, `Remove ${name} from liked candidates`) : L(`Ajouter ${name} aux favoris`, `Like ${name}`)}" title="${on ? L('Favori', 'Liked') : L('Ajouter aux candidats favoris', 'Like this candidate')}">${on ? icon.heartFill() : icon.heart()}</button>`;
}

// A candidate's badge: their Wikidata photo in gray, ringed in their color, with the
// author and license in the tooltip (as in the France section), or their initials on
// that color when there is no photo. `style` sizes it where the surrounding CSS doesn't.
export function candBadge(c, color, style = '') {
  const p = photoOf(c);
  if (!p) return html`<span class="badge" style="background:${color};${style}" aria-hidden="true">${initials(c.name)}</span>`;
  return html`<span class="badge photo" style="--party:${color};${style}" title="${L('Photo :', 'Photo:')} ${p.artist || L('auteur inconnu', 'unknown author')} (${p.license || 'Wikimedia Commons'})"><img src="${p.thumb}" alt="" loading="lazy" decoding="async"></span>`;
}

// The credits Commons licenses ask for, for the people pictured on a page.
export function photoCredits(people) {
  const shown = new Map();
  for (const c of people) {
    const p = photoOf(c);
    if (p && !shown.has(c.name)) shown.set(c.name, p);
  }
  if (!shown.size) return '';
  return html`<details class="card"><summary style="cursor:pointer;font-weight:650">${L('Crédits photo', 'Photo credits')}</summary>
    <ul class="small" style="margin:10px 0 0">${[...shown].map(([name, p]) => html`<li>${name}${L(' : ', ': ')}${p.artist || L('auteur inconnu', 'unknown author')}${p.license ? `, ${p.license}` : ''} — <a href="${p.page}" target="_blank" rel="noopener noreferrer">Wikimedia Commons</a></li>`)}</ul>
    <p class="tiny faint" style="margin:8px 0 0">${L('Les photos sont en noir et blanc. Elles viennent de Wikidata et de Wikimedia Commons, sous les licences indiquées.', 'Photos are shown in black and white. They come from Wikidata and Wikimedia Commons, under the licenses shown.')}</p>
  </details>`;
}

export function ratingChip(f) {
  const party = f.open ? f.ratingParty : f.lead.party;
  const cls = f.rating === 'Toss-up' || !party ? 'rating-T' : party === 'D' ? 'rating-D' : party === 'R' ? 'rating-R' : 'rating-T';
  return html`<span class="chip ${cls}" ${raw(f.open ? `title="${L('Cote consensuelle des analystes', 'Forecasters’ consensus rating')}"` : '')}><b>${ratingL(f.rating)}</b></span>`;
}
export const leadStr = (f) => {
  if (f.kind === 'field' || f.kind === 'office') {
    if (f.dr != null) return L(`${fmtDR(f.dr)} en 2024`, `${fmtDR(f.dr)} in 2024`);
    if (f.held) return L(`Sortant : ${f.held}`, `Held by ${f.held}`);
    return f.cands.length ? L(`${f.cands.length} candidat${f.cands.length === 1 ? '' : 's'}`, `${f.cands.length} candidate${f.cands.length === 1 ? '' : 's'}`) : L('Pas encore de liste', 'Not listed yet');
  }
  return f.open ? (f.dr != null ? L(`${fmtDR(f.dr)} par parti`, `${fmtDR(f.dr)} by party`) : L('Primaire ouverte', 'Open primary')) : f.dr != null ? fmtDR(f.dr) : `${f.lead.party} +${fmtNum(f.margin)}`;
};
export const pollStr = (f) => {
  if (!f.poll) return L('pas encore de sondage', 'no polls yet');
  if (f.pollDR != null) return fmtDR(f.pollDR);
  return `${f.lead.party} +${fmtNum(f.pollMargin ?? 0)}`;
};
function rangeStr(f) {
  let [a, b] = f.range80;
  if (f.dr == null) return L(`${fmtNum(a)} à ${pointsFr(b)}`, `${a.toFixed(1)} to ${b.toFixed(1)} pts`);
  if (a < 0 && b < 0) [a, b] = [b, a]; // read outward: R +6.7 to R +22.5
  return L(`${fmtDR(a)} à ${fmtDR(b)}`, `${fmtDR(a)} to ${fmtDR(b)}`);
}

// French: always a masculine noun ("le siège", "le poste"), so the sentences around it agree.
function seatPhraseFr(race) {
  const st = race.state;
  if (race.format === 'office') {
    const name = officeNameL(race.officeName);
    return `le poste de ${withState(name.charAt(0).toLowerCase() + name.slice(1), st)}`;
  }
  switch (race.office) {
    case 'senate': return `le siège de sénateur ${deState(st)}`;
    case 'governor': return `le poste de gouverneur ${deState(st)}`;
    case 'house': {
      if (st === 'DC') return 'le siège de délégué de D.C.';
      const n = parseInt(race.district, 10);
      return race.district === '00' ? `le siège unique ${deState(st)} à la Chambre` : `le siège de la ${n === 1 ? '1re' : `${n}e`} circonscription ${deState(st)}`;
    }
    default: return `ce siège (${officeLabel(race)})`;
  }
}
function seatPhrase(race) {
  if (lang() === 'fr') return seatPhraseFr(race);
  const s = STATE_BY_ABBR[race.state];
  if (race.format === 'office') return `the ${s.name} ${race.officeName.replace(/^State /, 'state ').toLowerCase()} race`;
  switch (race.office) {
    case 'senate': return `${s.name}’s Senate seat`;
    case 'governor': return `the ${s.name} governor’s race`;
    case 'house': return race.state === 'DC' ? 'the D.C. delegate seat' : race.district === '00' ? `${s.name}’s at-large House seat` : `${s.name}’s ${raceTitle(race).replace(s.name + ' ', '')}`;
    default: return `this ${officeLabel(race)} seat`;
  }
}

function heldPhrase(race) {
  if (!race.held) return '';
  if (lang() === 'fr') return race.open ? `, un siège sans sortant aujourd’hui détenu par les ${PARTY_PLURAL[race.held]}` : `, un siège aujourd’hui détenu par les ${PARTY_PLURAL[race.held]}`;
  return race.open ? `, an open seat now held by ${PARTY_PLURAL[race.held]}` : `, a seat now held by ${PARTY_PLURAL[race.held]}`;
}

// Published ratings from outside forecasters, with where they were compiled from.
export function forecasterRatings(race) {
  if (!race.ratings?.length) return '';
  return html`<div class="ratings-row">
    <span class="eyebrow">${L('L’avis des analystes', 'What forecasters say')}</span>
    ${race.ratings.map((r) => html`<span class="chip"><b>${ratingL(r.rating)}</b>&nbsp;${r.outlet}${r.date ? ` · ${fmtShortDate(r.date)}` : ''}</span>`)}
    ${race.ratingsSource ? html`<span class="tiny faint">${L('Compilé depuis', 'Compiled from')} ${ext(race.ratingsSource.url, race.ratingsSource.title)}</span>` : ''}
  </div>`;
}

function raceNotes(race) {
  if (!race.notes?.length) return '';
  return html`<ul class="race-notes" lang="en">${race.notes.map((n) => html`<li>${n.text}${n.url ? html` ${ext(n.url, n.source || 'source')}` : ''}</li>`)}</ul>`;
}

// When the data behind a real race was last refreshed (demo races: today's run).
function updatedChip(race) {
  const meta = !isDemo(race) && racesMeta();
  const when = meta && (meta.resultsUpdated || meta.updated);
  const every = meta?.resultsUpdated && stillCounting()
    ? L('les résultats sont relus toutes les 10 minutes pendant le dépouillement, le reste toutes les 8 heures', 'results are re-read every 10 minutes while races are counted, everything else every 8 hours')
    : L('les données sont mises à jour toutes les 8 heures', 'the data refreshes every 8 hours');
  return when
    ? html`<span class="chip" title="${L(`Mis à jour le ${fmtDate(when)} ; ${every}`, `Refreshed ${fmtDate(when)}; ${every}`)}">${L('Mis à jour', 'Refreshed')} <b>${timeAgo(when)}</b></span>`
    : html`<span class="chip">${L('Mis à jour le', 'Updated')} <b>${fmtDate(new Date())}</b></span>`;
}

// Results ------------------------------------------------------------------------
//
// The winner as Wikipedia's national table marks it once the race is called, and the
// vote counts its race page cites (scripts/lib/results.py), unofficial until the state
// certifies them. The forecast stays below, labelled as the pre-election forecast.

const partyCls = (p) => (p === 'D' ? 'verdict-d' : p === 'R' ? 'verdict-r' : 'verdict-x');
const cap = (s) => s.charAt(0).toUpperCase() + s.slice(1);
const nameList = (cands) => cands.map((c) => c.name).join(L(' et ', ' and '));
const OUTCOME_PARTY = { D: 'Democrats', R: 'Republicans', I: 'an independent', L: 'a Libertarian', G: 'a Green' };
const OUTCOME_PARTY_FR = { D: 'les démocrates', R: 'les républicains', I: 'un indépendant', L: 'un libertarien', G: 'un écologiste' };

// "D +4.1" when a Democrat and a Republican are the top two in the count, else the
// leader's last name: the site's rule for margins.
// `named: false` drops the name where the text beside it already gives it ("Begich leads +9.9").
export function resultMarginStr(race, { named = true } = {}) {
  const m = resultMargin(race);
  if (!m) return null;
  const dr = (m.a.party === 'D' && m.b.party === 'R') || (m.a.party === 'R' && m.b.party === 'D');
  return dr ? `${m.a.party} +${fmtNum(m.pts)}` : `${named ? `${lastName(m.a.name)} ` : ''}+${fmtNum(m.pts)}`;
}

// A real Senate, House, governor or statewide-office race after Election Day with
// nothing called or counted yet.
export const awaitingResult = (race) => afterElection() && !race.result && !isDemo(race) && race.format !== 'field';

// The colors a race's page gives its candidates (the strongest other candidate green):
// in the count's order where the race had no forecast, else in the forecast's.
export function raceColors(race) {
  const f = fc(race);
  if (!f.open) return candColors(f.cands);
  const rows = resultRows(race).filter((r) => r.cand);
  const listed = new Set(rows.map((r) => r.cand.id));
  return candColors([...rows.map((r) => r.cand), ...f.cands.filter((c) => !listed.has(c.id))]);
}

// One line on where the race stands: who won and by how much, who is in the runoff,
// or who leads the count.
export function resultLine(race) {
  if (lang() === 'fr') return resultLineFr(race);
  const res = race.result;
  if (!res) return 'Results not in yet';
  const m = resultMargin(race);
  if (res.status === 'won') {
    const w = resultWinners(race);
    const who = w.map((c) => `${lastName(c.name)} (${c.party})`).join(', ');
    return `${who} won${m && w.length === 1 ? ` by ${m.pts.toFixed(1)} pts` : ''}`;
  }
  if (res.status === 'runoff') {
    const a = resultAdvancing(race);
    return a.length >= 2 ? `Runoff: ${a.map((c) => `${lastName(c.name)} (${c.party})`).join(' vs ')}` : 'Headed to a runoff';
  }
  const lv = liveFc(race);
  const proj = lv ? ` · ${lastName(lv.lead.name)} ${fmtProb(lv.pLead)} to win` : '';
  return m ? `Counting: ${lastName(m.a.name)} leads by ${m.pts.toFixed(1)}${proj}` : 'Votes being counted';
}

function resultLineFr(race) {
  const res = race.result;
  if (!res) return 'Pas encore de résultats';
  const m = resultMargin(race);
  const tag = (c) => `${lastName(c.name)} (${c.party})`;
  if (res.status === 'won') {
    const w = resultWinners(race);
    return `${w.map(tag).join(', ')} ${w.length > 1 ? 'l’ont emporté' : 'l’a emporté'}${m && w.length === 1 ? ` avec ${pointsFr(m.pts)} d’avance` : ''}`;
  }
  if (res.status === 'runoff') {
    const a = resultAdvancing(race);
    return a.length >= 2 ? `Second tour : ${a.map(tag).join(' contre ')}` : 'Vers un second tour';
  }
  const lv = liveFc(race);
  const proj = lv ? ` · ${lastName(lv.lead.name)}, ${fmtProb(lv.pLead)} de chances de gagner` : '';
  return m ? `Dépouillement : ${lastName(m.a.name)} en tête de ${pointsFr(m.pts)}${proj}` : 'Dépouillement en cours';
}

// The projection in words: who it favors and how far the count has got.
const countedPhrase = (race, lv) => (lv.basis === 'reported'
  ? L(`${fmtPct(race.result.reporting, race.result.reporting % 1 ? 1 : 0)} des voix dépouillées`, `${fmtPct(race.result.reporting, race.result.reporting % 1 ? 1 : 0)} of the vote counted`)
  : L(`environ ${Math.min(98, Math.round(lv.frac * 100))} % des voix attendues dépouillées`, `about ${Math.min(98, Math.round(lv.frac * 100))}% of the expected vote counted`));
export function liveSentence(race) {
  const lv = liveFc(race);
  if (!lv) return '';
  return L(`Avec ${countedPhrase(race, lv)}, selon la projection à partir du dépouillement, ${lastName(lv.lead.name)} gagne dans ${fmtProb(lv.pLead)} des cas.`,
    `With ${countedPhrase(race, lv)}, the projection from the count has ${lastName(lv.lead.name)} winning ${fmtProb(lv.pLead)} of the time.`);
}

// A chip for lists and cards: the winner, a runoff or a count still going.
export function resultChip(race) {
  const res = race.result;
  if (!res) return awaitingResult(race) ? html`<span class="chip result-chip" title="${L('Aucun vainqueur n’est indiqué dans le tableau national des résultats de Wikipédia et aucun décompte n’est publié', 'No winner is marked in Wikipedia’s national results table and no count is posted yet')}"><b>${L('Pas encore attribuée', 'Not called yet')}</b></span>` : '';
  if (res.status === 'won') {
    const w = resultWinners(race);
    const cls = w.length === 1 && (w[0].party === 'D' || w[0].party === 'R') ? `rating-${w[0].party}` : 'rating-T';
    return html`<span class="chip ${cls} result-chip" title="${L(`Attribuée : le tableau national des résultats de Wikipédia indique le vainqueur${res.flip ? '. Le siège a changé de parti' : ''}`, `Called: Wikipedia’s national results table marks the winner${res.flip ? '. The seat changed parties' : ''}`)}">${icon.check()} <b>${w.map((c) => lastName(c.name)).join(', ')}</b>${res.flip ? L(' · bascule', ' · flip') : ''}</span>`;
  }
  if (res.status === 'runoff') return html`<span class="chip rating-T result-chip" title="${L('Aucun candidat n’a gagné dès le premier tour', 'No candidate won outright')}"><b>${L('Second tour', 'Runoff')}</b></span>`;
  return html`<span class="chip rating-T result-chip" title="${L('Le dépouillement continue ; l’élection n’est pas encore attribuée', 'Votes are still being counted; the race hasn’t been called')}"><b>${L('Dépouillement', 'Counting')}</b></span>`;
}

function resultHeadFr(race) {
  const res = race.result;
  const seat = seatPhrase(race);
  if (!res) return html`${cap(seat)} : <span class="grad-text likely">pas encore de résultat</span>.`;
  if (res.status === 'won') {
    const w = resultWinners(race);
    if (!w.length) return html`${cap(seat)} est attribué.`;
    if (w.length === 1) return html`<span class="${partyCls(w[0].party)}">${w[0].name}</span> remporte ${seat}.`;
    return html`${w.map((c, i) => html`${i ? ' et ' : ''}<span class="${partyCls(c.party)}">${c.name}</span>`)} remportent ${seat}.`;
  }
  if (res.status === 'runoff') {
    const a = resultAdvancing(race);
    if (a.length >= 2) return html`<span class="${partyCls(a[0].party)}">${a[0].name}</span> et <span class="${partyCls(a[1].party)}">${a[1].name}</span> s’affrontent au <span class="grad-text likely">second tour</span> pour ${seat}.`;
    return html`${cap(seat)} se jouera au <span class="grad-text likely">second tour</span>.`;
  }
  return html`Le <span class="grad-text likely">dépouillement se poursuit</span> pour ${seat}.`;
}

function resultHead(race) {
  if (lang() === 'fr') return resultHeadFr(race);
  const res = race.result;
  const seat = seatPhrase(race);
  if (!res) return html`${cap(seat)}: <span class="grad-text likely">no result yet</span>.`;
  if (res.status === 'won') {
    const w = resultWinners(race);
    if (!w.length) return html`${cap(seat)} has been called.`;
    if (w.length === 1) return html`<span class="${partyCls(w[0].party)}">${w[0].name}</span> wins ${seat}.`;
    return html`${w.map((c, i) => html`${i ? ' and ' : ''}<span class="${partyCls(c.party)}">${c.name}</span>`)} win ${seat}.`;
  }
  if (res.status === 'runoff') {
    const a = resultAdvancing(race);
    if (a.length >= 2) return html`<span class="${partyCls(a[0].party)}">${a[0].name}</span> and <span class="${partyCls(a[1].party)}">${a[1].name}</span> go to a <span class="grad-text likely">runoff</span> for ${seat}.`;
    return html`${cap(seat)} goes to a <span class="grad-text likely">runoff</span>.`;
  }
  return html`Votes are <span class="grad-text likely">still being counted</span> in ${seat}.`;
}

// The count in a sentence: the top candidates' shares and votes, how much is in, and
// who held the seat.
function resultLedeFr(race) {
  const res = race.result;
  if (!res) return `Le tableau national des résultats de Wikipédia n’indique pas encore de vainqueur, et la page de l’élection n’a pas encore de décompte. ${stillCounting() && racesMeta()?.resultsUpdated ? 'Les résultats sont relus toutes les 10 minutes jusqu’à ce que chaque élection soit attribuée.' : 'Les résultats arrivent à chaque mise à jour, toutes les 8 heures.'}`;
  const rows = resultRows(race).filter((r) => !r.other && rowShare(r) != null).slice(0, 3);
  const runoffDate = race.runoff ? fmtDate(race.runoff + 'T12:00:00') : null;
  const count = rows.length
    ? `Décompte non officiel${race.rcv && rows.some((r) => r.final != null) ? ', dernier tour' : ''} : ${rows.map((r) => `${lastName(r.name)} ${fmtPct(rowShare(r))}${r.votes != null && r.final == null ? ` (${fmtInt(r.votes)} voix)` : ''}`).join(', ')}${res.reporting != null ? `, ${fmtPct(res.reporting, res.reporting % 1 ? 1 : 0)} dépouillés` : ''}.`
    : 'Les décomptes ne sont pas encore publiés sur la page de l’élection.';
  const held = race.held && PARTY_PLURAL[race.held];
  const noun = race.office === 'governor' ? 'le poste de gouverneur' : race.format === 'office' ? 'le poste' : 'le siège';
  let seatLine = '';
  if (res.status === 'won' && held) {
    const p = resultWinners(race)[0]?.party;
    seatLine = res.flip ? ` ${cap(noun)} change de mains : les ${held} le détenaient, ${OUTCOME_PARTY_FR[p] || 'un autre parti'} l’emporte.` : ` Les ${held} conservent ${noun}.`;
  }
  const runoffLine = res.status === 'runoff' ? (runoffDate ? ` Le second tour a lieu le ${runoffDate}.` : ' Aucun candidat n’a obtenu la majorité : les deux premiers s’affrontent de nouveau.') : '';
  const liveLine = res.status === 'counting' && liveFc(race) ? ` ${liveSentence(race)}` : '';
  return `${count}${seatLine}${runoffLine}${liveLine}`;
}

function resultLede(race) {
  if (lang() === 'fr') return resultLedeFr(race);
  const res = race.result;
  if (!res) return `Wikipedia’s national results table hasn’t marked a winner, and the race’s page has no count yet. ${stillCounting() && racesMeta()?.resultsUpdated ? 'Results are re-read every 10 minutes until every race is called.' : 'Results come in with each refresh, every 8 hours.'}`;
  const rows = resultRows(race).filter((r) => !r.other && rowShare(r) != null).slice(0, 3);
  const runoffDate = race.runoff ? fmtDate(race.runoff + 'T12:00:00') : null;
  const count = rows.length
    ? `Unofficial count${race.rcv && rows.some((r) => r.final != null) ? ', final round' : ''}: ${rows.map((r) => `${lastName(r.name)} ${fmtPct(rowShare(r))}${r.votes != null && r.final == null ? ` (${fmtInt(r.votes)} votes)` : ''}`).join(', ')}${res.reporting != null ? `, ${fmtPct(res.reporting, res.reporting % 1 ? 1 : 0)} reporting` : ''}.`
    : 'The vote counts haven’t been posted to the race’s page yet.';
  const held = race.held && PARTY_PLURAL[race.held];
  const noun = race.office === 'governor' ? 'governorship' : race.format === 'office' ? 'office' : 'seat';
  let seatLine = '';
  if (res.status === 'won' && held) {
    const p = resultWinners(race)[0]?.party;
    seatLine = res.flip ? ` The ${noun} changes hands: ${held} held it, and ${OUTCOME_PARTY[p] || 'another party'} won it.` : ` ${held} keep the ${noun}.`;
  }
  const runoffLine = res.status === 'runoff' ? (runoffDate ? ` The runoff is on ${runoffDate}.` : ' No candidate won a majority, so the top two meet again.') : '';
  const liveLine = res.status === 'counting' && liveFc(race) ? ` ${liveSentence(race)}` : '';
  return `${count}${seatLine}${runoffLine}${liveLine}`;
}

function resultChips(race) {
  const res = race.result;
  if (!res) return html`<span class="chip" title="${L('Aucun vainqueur n’est encore indiqué dans le tableau national des résultats de Wikipédia', 'No winner is marked in Wikipedia’s national results table yet')}">${L('Résultat', 'Result')} <b>${L('Pas encore attribuée', 'Not called yet')}</b></span>`;
  const status = res.status === 'won' ? L('Attribuée', 'Called') : res.status === 'runoff' ? L('Second tour', 'Runoff') : L('Pas encore attribuée', 'Not called yet');
  return html`<span class="chip ${res.status === 'won' ? 'rating-T' : ''}" title="${res.status === 'won' ? L('Le tableau national des résultats de Wikipédia indique le vainqueur', 'Wikipedia’s national results table marks the winner') : res.status === 'runoff' ? L('Aucun candidat n’a gagné dès le premier tour', 'No candidate won outright') : L('Le dépouillement continue', 'Votes are still being counted')}">${L('Résultat', 'Result')} <b>${status}</b></span>
    ${res.outcome ? html`<span class="chip" lang="en"><b>${res.outcome}</b></span>` : ''}
    ${certChip(race)}`;
}

// Whether the state has certified its results (data/certified.json). The counts shown
// stay Wikipedia's compilation either way.
function certChip(race) {
  const c = certifiedRace(race), held = certPending(race);
  if (c) return html`<span class="chip" title="${L(`Résultats certifiés par l’État le ${fmtDate(c.date)}`, `${STATE_BY_ABBR[race.state].name} certified its results on ${fmtDate(c.date)}`)}">${L('Certifié par l’État', 'Certified by the state')}</span>`;
  if (!race.result?.rows?.length) return '';
  return html`<span class="chip" title="${held ? L(`L’État a certifié ses autres résultats ; celle-ci attend ${certWait(held)}`, `The state certified its other results; this race waits for ${certWait(held)}`) : L('Les résultats restent non officiels jusqu’à leur certification par l’État', 'Results are unofficial until the state certifies them')}">${L('Décompte non officiel', 'Unofficial count')}</span>`;
}

// How a race's results note opens: the state's certification, or that it hasn't come yet.
const certBy = (c) => ext(c.source.url, c.source.title.split(':')[0]);
function certLead(race) {
  const c = certifiedRace(race), held = certPending(race), cs = held && certifiedIn(race.state), name = STATE_BY_ABBR[race.state].name;
  if (lang() === 'fr') {
    if (c) return html`L’État a certifié ses résultats le ${fmtDate(c.date)} (${certBy(c)}). Les décomptes affichés peuvent encore différer du décompte certifié`;
    if (held) return html`L’État a certifié ses autres résultats le ${fmtDate(cs.date)} (${certBy(cs)}), mais cette élection attend ${certWait(held)} : ses décomptes restent non officiels jusque-là`;
    return html`Les décomptes restent non officiels jusqu’à la certification des résultats ${deState(race.state)}`;
  }
  if (c) return html`${name} certified its results on ${fmtDate(c.date)} (${certBy(c)}). The counts shown may lag its certified canvass`;
  if (held) return html`${name} certified its other results on ${fmtDate(cs.date)} (${certBy(cs)}), but this race waits for ${certWait(held)}: its counts are unofficial until then`;
  return html`Vote counts are unofficial until ${name} certifies its results`;
}

// The full count as the race's page publishes it, write-ins included, with its source.
export function resultsTable(race) {
  const res = race.result;
  if (!res?.rows?.length) return '';
  const f = fc(race);
  const colors = candColors(f.cands);
  // A write-in line the page lists without any figures says nothing; leave it out.
  const rows = resultRows(race).filter((r) => !(r.other && r.votes == null && r.pct == null && r.final == null));
  const finals = rows.some((r) => r.final != null);
  const page = res.page;
  return html`<section class="card stack-sm results-card">
    <div class="row between"><div><div class="eyebrow">${certifiedRace(race) ? L('Résultats', 'Results') : L('Résultats non officiels', 'Unofficial results')}</div><h3 style="margin:2px 0 0">${L('Le décompte', 'The count')}${res.reporting != null ? L(`, ${fmtPct(res.reporting, res.reporting % 1 ? 1 : 0)} dépouillés`, `, ${fmtPct(res.reporting, res.reporting % 1 ? 1 : 0)} reporting`) : ''}</h3></div>${resultChip(race)}</div>
    <div class="table-wrap"><table class="data results-table"><thead><tr><th>${L('Candidat', 'Candidate')}</th><th>${L('Parti', 'Party')}</th><th class="r">${L('Voix', 'Votes')}</th><th class="r">${finals ? L('Premier tour', 'First round') : L('Part', 'Share')}</th>${finals ? html`<th class="r">${L('Dernier tour', 'Final round')}</th>` : ''}</tr></thead><tbody>
      ${rows.map((r) => {
        const color = r.cand ? colors[r.cand.id] : null;
        return html`<tr class="${r.won ? 'won' : ''}">
          <td><span class="res-name">${color ? html`<i class="key-box" style="background:${color}"></i>` : html`<i class="key-box" style="background:var(--surface-3)"></i>`}<span>${r.name}${r.won ? html` <span class="win-mark">${icon.check()} ${L('Victoire', 'Winner')}</span>` : ''}${r.advance ? html` <span class="win-mark">${L('Au second tour', 'To the runoff')}</span>` : ''}${r.mate ? html`<span class="tiny faint" style="display:block">${L('avec', 'with')} ${r.mate}</span>` : ''}</span></span></td>
          <td>${r.other ? '—' : PARTY_NAME[r.party] || r.party || '—'}</td>
          <td class="r">${r.votes != null ? fmtInt(r.votes) : '—'}</td>
          <td class="r">${r.pct != null ? fmtPct(r.pct, 2) : '—'}</td>
          ${finals ? html`<td class="r">${r.final != null ? fmtPct(r.final, 2) : '—'}</td>` : ''}
        </tr>`;
      })}
      ${res.total ? html`<tr class="total"><td>Total</td><td></td><td class="r">${res.totalFromShares ? L('Environ ', 'About ') : ''}${fmtInt(res.total)}</td><td class="r">${fmtPct(100, 0)}</td>${finals ? html`<td></td>` : ''}</tr>` : ''}
    </tbody></table></div>
    ${lang() === 'fr' ? resultsNoteFr(race, res, page, finals) : html`<p class="tiny faint" style="margin:0">${res.status === 'won' ? 'Called: Wikipedia’s national results table marks the winner. ' : res.status === 'runoff' ? 'Wikipedia’s national results table marks the candidates advancing to the runoff. ' : 'Not called yet: no winner is marked in Wikipedia’s national results table. '}${certLead(race)}${res.official
      ? html`; they come straight from ${ext(res.source.url, res.source.title)}${res.countAsOf ? `, posted ${timeAgo(res.countAsOf)}` : ''}`
      : html`${res.source ? html`; they come from ${ext(res.source.url, res.source.title)}, as compiled` : '; they are as compiled'} by ${page ? html`${ext(page.url, page.title.replace(/^Wikipedia: /, 'Wikipedia’s page '))}${page.asOf ? `, last edited ${timeAgo(page.asOf)}` : ''}` : 'Wikipedia'}`}.${res.via === 'infobox' ? ` The page’s results table is still blank, so this is the count in its infobox, which lists only the leading candidates${res.totalFromShares ? ': “Others” is the share that remains, and the total is worked out from the shares' : ''}.` : ''}${res.sharesFromVotes ? ' Shares are worked out from those counts, since the page’s percentages didn’t match them.' : ''}${finals ? ' This race uses ranked-choice voting: the final round is the count after the trailing candidates’ ballots moved to voters’ next choices.' : ''}</p>`}
  </section>`;
}

function resultsNoteFr(race, res, page, finals) {
  const called = res.status === 'won' ? 'Attribuée : le tableau national des résultats de Wikipédia indique le vainqueur. '
    : res.status === 'runoff' ? 'Le tableau national des résultats de Wikipédia indique les candidats qualifiés pour le second tour. '
      : 'Pas encore attribuée : aucun vainqueur n’est indiqué dans le tableau national des résultats de Wikipédia. ';
  return html`<p class="tiny faint" style="margin:0">${called}${certLead(race)}${res.official
    ? html` ; ils viennent directement de ${ext(res.source.url, res.source.title)}${res.countAsOf ? `, publiés ${timeAgo(res.countAsOf)}` : ''}`
    : html`${res.source ? html` ; ils viennent de ${ext(res.source.url, res.source.title)}, compilés` : ' ; ils sont compilés'} par ${page ? html`${ext(page.url, page.title.replace(/^Wikipedia: /, 'la page Wikipédia '))}${page.asOf ? `, modifiée ${timeAgo(page.asOf)}` : ''}` : 'Wikipédia'}`}.${res.via === 'infobox' ? ` Le tableau des résultats de la page est encore vide : c’est donc le décompte de son infobox, qui ne liste que les candidats en tête${res.totalFromShares ? ' ; « Autres » est la part restante, et le total est calculé à partir des parts' : ''}.` : ''}${res.sharesFromVotes ? ' Les parts sont calculées à partir des voix, car les pourcentages de la page ne leur correspondaient pas.' : ''}${finals ? ' Cette élection utilise le vote par classement : le dernier tour est le décompte après le report des bulletins des derniers candidats sur les choix suivants des électeurs.' : ''}</p>`;
}

// The candidates' cards with their results: share and votes, the winner marked, and the
// final forecast for comparison. Anyone the count doesn't list keeps a card, last.
function resultCards(race) {
  const f = fc(race);
  const colors = candColors(f.cands);
  const rows = resultRows(race).filter((r) => r.cand);
  const listed = new Set(rows.map((r) => r.cand.id));
  const fcOf = new Map(f.cands.map((c) => [c.id, c]));
  const winners = new Set(race.result?.winners || []), adv = new Set(race.result?.advance || []);
  const lv = liveFc(race);
  const lvOf = new Map((lv?.cands || []).map((x) => [x.id, x]));
  const card = (c, r) => {
    const share = r ? rowShare(r) : null;
    const fcc = fcOf.get(c.id);
    const lvc = lvOf.get(c.id);
    const won = r ? r.won : winners.has(c.id), toRunoff = r ? r.advance : adv.has(c.id);
    return html`<article class="cand ${partyClass(c.party)}${won ? ' winner' : ''}">
      <div class="cand-top">
        ${candBadge(c, colors[c.id])}
        <div><div class="cand-name">${c.name}</div><div class="cand-party">${PARTY_NAME[c.party] || c.party}${c.incumbent ? L(' · en poste', ' · incumbent') : ''}</div></div>
        <div class="cand-actions">${heartBtn(c.id, c.name)}</div>
      </div>
      <div class="big" style="color:${colors[c.id]}">${share != null ? fmtPct(share) : '—'}</div>
      <div class="votes">${won ? html`<span class="win-mark">${icon.check()} ${L('Victoire', 'Winner')}</span> ` : toRunoff ? html`<span class="win-mark">${L('Au second tour', 'To the runoff')}</span> ` : ''}${r?.votes != null ? L(`${fmtInt(r.votes)} voix`, `${fmtInt(r.votes)} votes`) : rows.length ? L('Pas encore dans le décompte', 'Not in the count yet') : L('Décompte pas encore publié', 'Vote count not posted yet')}${r?.final != null ? L(` · dernier tour (premier tour : ${fmtPct(r.pct)})`, ` · final round (first round ${fmtPct(r.pct)})`) : ''}</div>
      ${raw(segments(share ?? 0, colors[c.id]))}
      ${lvc ? html`<div class="small" style="margin-top:8px"><b>${L('Projection', 'Projected')}${L(' : ', ': ')}${fmtPct(lvc.share)}</b>, ${L(`${fmtProb(lvc.win)} de chances de gagner`, `${fmtProb(lvc.win)} to win`)}</div>` : ''}
      ${fcc && !f.open ? html`<div class="tiny faint" style="margin-top:${lvc ? 2 : 8}px">${L(`Dernière prévision : ${fmtPct(fcc.share)} des voix, ${fmtProb(fcc.win)} de chances de gagner`, `Final forecast: ${fmtPct(fcc.share)} of the vote, ${fmtProb(fcc.win)} to win`)}</div>` : ''}
      <div class="meta">${candMeta(c)}</div>
    </article>`;
  };
  const rest = f.cands.filter((c) => !listed.has(c.id)).sort((a, b) => (winners.has(b.id) || adv.has(b.id)) - (winners.has(a.id) || adv.has(a.id)));
  return html`<div class="cands">${rows.map((r) => card(r.cand, r))}${rest.map((c) => card(c, null))}</div>`;
}

// "3 candidatures" / "3 candidates": the French word needs no gender agreement.
// "0,8 point", "2,5 points": French takes the plural from 2.
export const pointsFr = (x) => `${fmtNum(x)} point${Math.abs(Math.round(x * 10) / 10) >= 2 ? 's' : ''}`;
const candCount = (n) => L(`${n} candidature${n === 1 ? '' : 's'}`, `${n} candidate${n === 1 ? '' : 's'}`);
// What the holder of a seat is doing, from the data's English status ("Retiring").
const STATUS_FR = [[/retir/i, 'ne se représente pas'], [/term/i, 'a atteint la limite de mandats'], [/lost/i, 'a perdu la primaire'], [/running for/i, 'se présente à un autre poste'], [/resign/i, 'a démissionné']];
const statusL = (s) => (lang() === 'fr' ? (STATUS_FR.find(([re]) => re.test(s))?.[1] || s) : s.toLowerCase());
// Poll samples: likely voters, registered voters, voters, adults.
const POP_FR = { LV: 'électeurs probables', RV: 'inscrits', V: 'votants', A: 'adultes' };
const popL = (pop) => L(POP_FR[pop] || pop || '', pop || '');
const lcFirst = (s) => s.charAt(0).toLowerCase() + s.slice(1);

// The waffle's caption, worded in French so it needs no gender agreement.
const capLine = (a, p) => (lang() === 'fr'
  ? (p >= 0.97 ? `Victoire quasi certaine de ${lastName(a.name)}` : p >= 0.85 ? `Net avantage à ${lastName(a.name)}` : p >= 0.65 ? `Avantage à ${lastName(a.name)}` : 'Trop serré pour trancher')
  : (p >= 0.97 ? `${lastName(a.name)} all but certain` : p >= 0.85 ? `${lastName(a.name)} clearly favored` : p >= 0.65 ? `${lastName(a.name)} favored` : 'Too close to call'));

// While a race is counted and not called: the final forecast adjusted for the votes
// counted so far (`live` in js/model/forecast.js, the same as scripts/lib/model.py).
// A margin from the leader's side, "D +x" between a Democrat and a Republican.
const sideMargin = (lv, m) => {
  const dr = (lv.lead.party === 'D' && lv.second.party === 'R') || (lv.lead.party === 'R' && lv.second.party === 'D');
  const who = m >= 0 ? lv.lead : lv.second;
  return `${dr ? who.party : lastName(who.name)} +${fmtNum(Math.abs(m))}`;
};
export function liveBlock(race) {
  const lv = liveFc(race);
  if (!lv) return '';
  const res = race.result;
  const colors = candColors(fc(race).cands);
  const a = lv.lead, b = lv.second;
  const p = lv.pLead;
  const cap = capLine(a, p);
  const [lo, hi] = lv.range80;
  const flipped = lv.countLead.id !== a.id;
  const when = res.countAsOf || res.page?.asOf;
  return html`<section class="card stack live-card">
    <div class="row between">
      <div><div class="eyebrow">${L('Projection à partir du dépouillement', 'Projection from the count so far')}</div><h3 style="margin:2px 0 0">${L(`${lastName(a.name)} gagne dans ${fmtProb(p)} des cas`, `${lastName(a.name)} wins ${fmtProb(p)} of the time`)}</h3></div>
      <span class="chip rating-T" title="${L('Aucun vainqueur n’est encore indiqué dans le tableau national des résultats de Wikipédia', 'No winner is marked in Wikipedia’s national results table yet')}"><b>${L('Pas encore attribuée', 'Not called yet')}</b></span>
    </div>
    <div class="waffle-wrap">
      <div class="waffle-side"><div class="p" style="color:${colors[a.id]}">${fmtProb(p)}</div><div class="n">${lastName(a.name)}</div></div>
      ${raw(waffle([{ name: a.name, share: p, color: colors[a.id] }, { name: b.name, share: 1 - p, color: colors[b.id] }]))}
      <div class="waffle-side"><div class="p" style="color:${colors[b.id]}">${fmtProb(1 - p)}</div><div class="n">${lastName(b.name)}</div></div>
    </div>
    <div class="waffle-caption"><strong>${cap}</strong><span class="eyebrow">${L('Chaque carré est une issue possible pour le reste du dépouillement', 'Each square is one way the rest of the count could go')}</span></div>
    <div class="grid grid-4">
      <div class="stat"><div class="eyebrow">${L('Dépouillé à ce jour', 'Counted so far')}</div><div class="value">${lv.basis === 'reported' ? fmtPct(res.reporting, res.reporting % 1 ? 1 : 0) : `~${Math.min(98, Math.round(lv.frac * 100))}${pctSign()}`}</div><div class="sub">${res.totalFromShares ? L('Environ ', 'About ') : ''}${L(`${fmtInt(lv.counted)} voix`, `${fmtInt(lv.counted)} votes`)}${lv.basis === 'reported' ? L(', selon les résultats publiés', ', as the results report it') : L(` sur environ ${fmtCompact(lv.expected)} attendues`, ` of about ${fmtCompact(lv.expected)} expected`)}</div></div>
      <div class="stat"><div class="eyebrow">${L('Écart projeté', 'Projected margin')}</div><div class="value">${lv.margin < 0.05 ? L('À égalité', 'About even') : sideMargin(lv, lv.margin)}</div><div class="sub">${L('Décompte actuel :', 'Count now:')} ${sideMargin({ ...lv, lead: lv.countLead, second: lv.countSecond }, lv.countMargin)}</div></div>
      <div class="stat"><div class="eyebrow">${L('Fourchette à 80 %', '80 percent range')}</div><div class="value" style="font-size:21px">${sideMargin(lv, lo)} ${L('à', 'to')} ${sideMargin(lv, hi)}</div><div class="sub">${L('8 projections sur 10 tombent ici', '8 in 10 projections land here')}</div></div>
      <div class="stat"><div class="eyebrow">${L('Voix projetées', 'Projected votes')}</div><div class="value">${fmtCompact(lv.expected)}</div><div class="sub">${lastName(a.name)} ${fmtPct(lv.shares[a.id])} · ${lastName(b.name)} ${fmtPct(lv.shares[b.id])}</div></div>
    </div>
    ${lang() === 'fr' ? html`<p class="tiny faint" style="margin:0">Ce n’est pas une attribution. La projection combine le décompte${when ? ` (${res.official ? 'publié' : 'relevé'} ${timeAgo(when)})` : ''} et la dernière prévision : les voix restantes devraient pencher comme le décompte en proportion de la part déjà dépouillée, et comme la prévision sinon, avec une marge pour que les derniers bulletins penchent tout autrement.${lv.basis === 'reported' ? '' : ' La part restante est elle-même une estimation : les voix attendues sont celles de la présidentielle de 2024 dans l’État, multipliées par le rapport habituel des élections de mi-mandat, qui peut se tromper d’un cinquième dans un sens ou dans l’autre ; la projection en fait la moyenne.'}${race.rcv ? ' Dans cette élection au vote par classement, elle lit le décompte comme le ferait le dernier tour, les voix des autres candidats de chaque parti allant à son candidat le plus fort.' : ''}${flipped ? ` La prévision tire la projection vers ${lastName(a.name)}, derrière dans le décompte à ce stade.` : ''} Les résultats sont relus toutes les 10 minutes jusqu’à l’attribution de l’élection.</p>` : html`<p class="tiny faint" style="margin:0">This is not a call. It blends the count${when ? ` (${res.official ? 'posted' : 'as of'} ${timeAgo(when)})` : ''} with the final forecast: the votes still out are expected to lean like the count in proportion to how much of the vote is in, and like the forecast otherwise, with room for the last ballots to lean quite differently.${lv.basis === 'reported' ? '' : ' How much is still out is itself an estimate: the expected vote is the state’s 2024 presidential vote times the usual midterm ratio, which can be off by a fifth either way, so the projection averages over that.'}${race.rcv ? ' In this ranked-choice race it reads the count as the final round would, with each party’s other candidates’ votes going to its strongest one.' : ''}${flipped ? ` The forecast pulls the projection toward ${lastName(a.name)}, who trails the count so far.` : ''} The results are re-read every 10 minutes until the race is called.</p>`}
  </section>`;
}

// How the final forecast compares with the count.
function forecastRecap(race) {
  const f = fc(race);
  if (f.open || !f.second) return '';
  const res = race.result;
  const w = res?.status === 'won' ? resultWinners(race) : [];
  const m = resultMargin(race);
  const fr = lang() === 'fr';
  const wonBy = (c) => (fr ? (c.id === f.lead.id ? ` ${lastName(c.name)} l’a emporté` : ` C’est ${lastName(c.name)} qui l’a emporté`) : ` ${lastName(c.name)} ${c.id === f.lead.id ? 'won' : 'won instead'}`);
  const after = w.length === 1 && m
    ? `${wonBy(w[0])}, ${m.a.cand?.id === w[0].id ? L(`avec ${pointsFr(m.pts)} d’avance`, `by ${m.pts.toFixed(1)} points`) : L('au décompte final', 'in the final count')}${certifiedRace(race) ? '.' : L(' selon les résultats non officiels.', ' in the unofficial results.')}`
    : w.length === 1 ? `${wonBy(w[0])}.`
      : res?.status === 'runoff' ? L(' L’élection va au second tour.', ' The race goes to a runoff.') : '';
  return html`<section class="stack">
    <div><div class="eyebrow">${L('Avant l’élection', 'Before the election')}</div><h3 style="margin:2px 0 0">${L('La dernière prévision', 'The final forecast')}</h3>
      <p class="small muted" style="margin:4px 0 0">${L(`Le dernier calcul du modèle avant la fermeture des bureaux de vote donnait ${lastName(f.lead.name)} en tête de ${pointsFr(f.margin)}, gagnant dans ${fmtProb(f.pLead)} des élections simulées (analystes : ${ratingL(race.consensus?.rating || f.rating)}).`, `The model’s last run before polls closed had ${lastName(f.lead.name)} ahead by ${f.margin.toFixed(1)} points, winning ${fmtProb(f.pLead)} of simulated elections (forecasters: ${race.consensus?.rating || f.rating}).`)}${after}</p></div>
    ${waffleBlock(race)}
    ${statTiles(race)}
  </section>`;
}

function resultsHero(race, { tag }) {
  const f = fc(race);
  const H = raw(tag);
  return html`<section class="hero">
    <span class="label-pill"><span class="dots">•••</span> ${L('Résultats 2026', '2026 results')} · ${raceShortTitle(race)} <span class="dots">•••</span></span>
    <${H} ${tag === 'h2' ? raw('class="display" style="font-size:clamp(26px,3.4vw,40px);margin:14px auto 10px;max-width:820px"') : ''}>${resultHead(race)}</${H}>
    <p class="lede">${resultLede(race)}</p>
    <div class="row" style="justify-content:center">
      ${resultChips(race)}
      ${f.open ? '' : html`<span class="chip" title="${L('La dernière prévision du modèle, avant la fermeture des bureaux de vote', 'The model’s final forecast, before polls closed')}">${L('Prévision', 'Forecast')} <b>${ratingL(f.rating)}</b></span>`}
      ${updatedChip(race)}
      ${dataChip(race)}
      ${starBtn(race.id)}
    </div>
    ${raceNotes(race)}
    ${race.rcv ? html`<p class="small faint" style="margin-top:10px">${L('Cette élection utilise le vote par classement : si personne n’a la majorité des premiers choix, les derniers candidats sont éliminés et leurs bulletins vont aux choix suivants des électeurs.', 'This race uses ranked-choice voting: if no one has a majority of first choices, the trailing candidates are eliminated and their ballots move to voters’ next choices.')}</p>` : ''}
  </section>`;
}

const VERDICT_FR = { 'very likely': 'a de très fortes chances de remporter', likely: 'a de fortes chances de remporter', 'slightly favored': 'a un léger avantage pour remporter' };

export function raceHero(race, { tag = 'h1' } = {}) {
  if (race.result || awaitingResult(race)) return resultsHero(race, { tag });
  const f = fc(race);
  const v = verdict(f.pLead);
  const cls = f.lead.party === 'D' ? 'verdict-d' : f.lead.party === 'R' ? 'verdict-r' : 'verdict-x';
  const seat = seatPhrase(race);
  const fr = lang() === 'fr';
  const head = fr
    ? (!f.second
      ? html`<span class="${cls}">${f.lead.name}</span> <span class="grad-text likely">n’a pas d’adversaire</span> pour ${seat}.`
      : v
        ? html`<span class="${cls}">${f.lead.name}</span> <span class="grad-text likely">${VERDICT_FR[v]}</span> ${seat}.`
        : html`${cap(seat)} : <span class="grad-text likely">issue incertaine</span>.`)
    : !f.second
      ? html`<span class="${cls}">${f.lead.name}</span> is <span class="grad-text likely">unopposed</span> for ${seat}.`
      : v
        ? html`<span class="${cls}">${f.lead.name}</span> is <span class="grad-text likely">${v}</span> to win ${seat}.`
        : html`${seat.charAt(0).toUpperCase() + seat.slice(1)} is a <span class="grad-text likely">toss-up</span>.`;
  const H = raw(tag);
  const lede = fr
    ? (f.second
      ? `${f.cands.slice(0, 2).map((c) => c.name).join(' contre ')}${heldPhrase(race)}. Le modèle place ${lastName(f.lead.name)} en tête de ${pointsFr(f.margin)}, gagnant dans ${fmtProb(f.pLead)} des élections simulées.`
      : `${f.lead.name} est la seule candidature sur le bulletin${heldPhrase(race)}.`)
    : f.second
      ? `${f.cands.slice(0, 2).map((c) => c.name).join(' vs ')}${heldPhrase(race)}. The model has ${lastName(f.lead.name)} ahead by ${f.margin.toFixed(1)} points, winning ${fmtProb(f.pLead)} of simulated elections.`
      : `${f.lead.name} is the only candidate on the ballot${heldPhrase(race)}.`;
  const cons = !isDemo(race) && race.consensus?.outlets ? race.consensus : null;
  return html`<section class="hero">
    <span class="label-pill"><span class="dots">•••</span> ${L('Prévision 2026', '2026 forecast')} · ${raceShortTitle(race)} <span class="dots">•••</span></span>
    <${H} ${tag === 'h2' ? raw('class="display" style="font-size:clamp(26px,3.4vw,40px);margin:14px auto 10px;max-width:820px"') : ''}>${head}</${H}>
    <p class="lede">${lede}</p>
    <div class="row" style="justify-content:center">
      ${ratingChip(f)}
      <span class="chip">${L('Modèle', 'Model')} <b>${leadStr(f)}</b></span>
      <span class="chip">${L('Sondages', 'Polls')} <b>${pollStr(f)}</b></span>
      ${cons ? html`<span class="chip" title="${L(`Moyenne des cotes de ${cons.outlets} analystes`, `Average of ${cons.outlets} forecasters’ ratings`)}">${L('Analystes', 'Forecasters')} <b>${ratingL(cons.rating)}</b></span>` : ''}
      ${updatedChip(race)}
      ${dataChip(race)}
      ${starBtn(race.id)}
    </div>
    ${forecasterRatings(race)}
    ${raceNotes(race)}
    ${race.nonpartisan ? html`<p class="small faint" style="margin-top:10px">${L('L’assemblée du Nebraska est non partisane : les étiquettes de parti n’apparaissent pas sur le bulletin. L’affiliation déclarée est indiquée pour information.', 'Nebraska’s Legislature is nonpartisan: party labels do not appear on the ballot. Party registration is shown for context.')}</p>` : ''}
    ${race.rcv ? html`<p class="small faint" style="margin-top:10px">${L('Cette élection utilise le vote par classement : la prévision modélise donc le dernier tour.', 'This race uses ranked-choice voting, so the forecast models the final round.')} ${race.finalPolls?.length ? L('Elle utilise le dernier tour que donnent les sondages par classement, présentés sous Sondages.', 'It uses the final round that ranked-choice polls report, shown under Polling.') : L('Faute de sondages par classement, elle suppose que les voix des autres candidats de chaque parti vont à son candidat le plus fort.', 'With no ranked-choice polls yet, it assumes votes for each party’s other candidates move to its strongest candidate.')}</p>` : ''}
    ${multiMemberNote(race)}
  </section>`;
}

function multiMemberNote(race) {
  const mm = STATE_BY_ABBR[race.state].multiMember;
  const applies = mm && ((race.office === 'state-house' && (mm === 'lower' || mm === 'both')) || (race.office === 'state-senate' && mm === 'both'));
  return applies ? html`<p class="small faint" style="margin-top:6px">${L('Cette chambre a des circonscriptions à plusieurs sièges : le vrai bulletin peut donc compter plusieurs élus ici. La démo montre un seul duel.', 'This chamber uses multi-member districts, so the real ballot may list several winners here. The demo shows one head-to-head.')}</p>` : '';
}

function candMeta(c) {
  if (c.demo) return L(`Candidature fictive de démonstration · ${c.job}`, `Fictional demo candidate · ${c.job}`);
  const links = html`${c.officialSite ? html` ${ext(c.officialSite, L('Site de campagne', 'Campaign site'))}` : ''}${!c.bio && c.wiki ? html` ${ext(c.wiki, 'Wikipedia')}` : ''}`;
  return html`${c.bio ? html`<span lang="en">${c.bio}</span>` : c.incumbent ? L('En poste.', 'Incumbent.') : ''}${links}`;
}

export function candidateCards(race) {
  const f = fc(race);
  const colors = candColors(f.cands);
  return html`<div class="cands">${f.cands.map((c) => html`
    <article class="cand ${partyClass(c.party)}">
      <div class="cand-top">
        ${candBadge(c, colors[c.id])}
        <div><div class="cand-name">${c.name}</div><div class="cand-party">${PARTY_NAME[c.party] || c.party}</div></div>
        <div class="cand-actions">${heartBtn(c.id, c.name)}</div>
      </div>
      ${c.firstRound != null && c.share === 0
        ? html`<div class="big" style="color:${colors[c.id]}">${fmtPct(c.firstRound)}</div>
      <div class="votes">${L('part au premier tour · hors course avant le dernier tour, quand ces bulletins vont aux choix suivants des électeurs', 'first-round share · eliminated before the final round, when these ballots move to voters’ next choices')}</div>
      ${raw(segments(c.firstRound, colors[c.id]))}`
        : html`<div class="big" style="color:${colors[c.id]}">${fmtPct(c.share)}</div>
      <div class="votes">${c.firstRound != null ? L(`dernier tour (premier tour : ${fmtPct(c.firstRound)}) · `, `final round (first round ${fmtPct(c.firstRound)}) · `) : L(`${fmtInt(c.votes)} voix projetées · `, `${fmtInt(c.votes)} projected votes · `)}${L(`${fmtProb(c.win)} de chances de gagner`, `${fmtProb(c.win)} to win`)}</div>
      ${raw(segments(c.share, colors[c.id]))}`}
      <div class="meta">${candMeta(c)}</div>
    </article>`)}</div>`;
}

export function waffleBlock(race) {
  const f = fc(race);
  if (!f.second) return '';
  const colors = candColors(f.cands);
  const a = f.lead, b = f.second;
  const p = f.pLead;
  const cap = capLine(a, p);
  return html`<div class="waffle-wrap">
      <div class="waffle-side"><div class="p" style="color:${colors[a.id]}">${fmtProb(a.win)}</div><div class="n">${lastName(a.name)}</div></div>
      ${raw(waffle([{ name: a.name, share: a.win, color: colors[a.id] }, { name: b.name, share: b.win, color: colors[b.id] }]))}
      <div class="waffle-side"><div class="p" style="color:${colors[b.id]}">${fmtProb(b.win)}</div><div class="n">${lastName(b.name)}</div></div>
    </div>
    <div class="waffle-caption"><strong>${cap}</strong><span class="eyebrow">${L('Chaque carré est une soirée électorale simulée', 'Each square is one simulated election night')}</span></div>`;
}

export function statTiles(race) {
  const f = fc(race);
  return html`<div class="grid grid-4">
    <div class="stat"><div class="eyebrow">${L('Cote', 'Rating')}</div><div class="value">${ratingL(f.rating)}</div><div class="sub">${L(`${fmtProb(f.pLead)} de chances pour ${lastName(f.lead.name)}`, `${fmtProb(f.pLead)} chance for ${lastName(f.lead.name)}`)}</div></div>
    <div class="stat"><div class="eyebrow">${L('Écart du modèle', 'Model margin')}</div><div class="value">${leadStr(f)}</div><div class="sub">${L('Sondages :', 'Polls')} ${pollStr(f)}</div></div>
    <div class="stat"><div class="eyebrow">${L('Fourchette à 80 %', '80 percent range')}</div><div class="value" style="font-size:21px">${rangeStr(f)}</div><div class="sub">${L('8 simulations sur 10 tombent ici', '8 in 10 simulations land here')}</div></div>
    <div class="stat"><div class="eyebrow">${L('Voix projetées', 'Projected votes')}</div><div class="value">${fmtInt(f.turnout)}</div><div class="sub">${lastName(f.lead.name)} ${fmtPct(f.lead.share)}</div></div>
  </div>`;
}

// Open ("jungle") primaries: everyone on one ballot, top two to a runoff. With many
// candidates and thin polling a win probability would be false precision, so this
// view shows the field, the polls and the forecasters' ratings instead.
function openPrimaryFull(race, { tag, credits }) {
  const f = fc(race);
  const res = race.result;
  const byRow = new Map(resultRows(race).filter((r) => r.cand).map((r) => [r.cand.id, r]));
  const winners = new Set(res?.winners || []), adv = new Set(res?.advance || []);
  const ahead = (c) => (winners.has(c.id) || adv.has(c.id) ? 1 : 0);
  const cands = byRow.size ? [...f.cands].sort((a, b) => (rowShare(byRow.get(b.id) || {}) ?? -1) - (rowShare(byRow.get(a.id) || {}) ?? -1))
    : res ? [...f.cands].sort((a, b) => ahead(b) - ahead(a)) : f.cands;
  const colors = raceColors(race);
  const H = raw(tag);
  const poll = race.polls[0];
  const runoff = race.runoff ? fmtDate(race.runoff + 'T12:00:00') : null;
  return html`<div class="stack-lg">
    <section class="hero">
      <span class="label-pill"><span class="dots">•••</span> ${res ? L('Résultats 2026', '2026 results') : '2026'} · ${raceShortTitle(race)} · ${L('primaire ouverte', 'open primary')} <span class="dots">•••</span></span>
      <${H} ${tag === 'h2' ? raw('class="display" style="font-size:clamp(26px,3.4vw,40px);margin:14px auto 10px;max-width:820px"') : ''}>${res ? resultHead(race) : L(html`${raceTitle(race)} : <span class="grad-text">${candCount(f.cands.length)}</span>, un seul bulletin.`, html`${raceTitle(race)}: <span class="grad-text">${f.cands.length} candidates</span>, one ballot.`)}</${H}>
      <p class="lede">${res ? `${resultLede(race)} ` : ''}${lang() === 'fr' ? `Tous les candidats, de tous les partis, ${res ? 'étaient' : 'sont'} sur le même bulletin du 3 novembre. Une majorité absolue suffit pour gagner dès le premier tour ; sinon, les deux premiers s’affrontent au second tour${runoff && !res ? ` le ${runoff}` : ''}. Avec autant de candidats et peu de sondages publics, Informed Voter n’a pas estimé les chances de chacun ; il a montré à la place la répartition attendue entre les partis et les cotes des analystes.` : ''}${lang() === 'fr' ? '' : html`Every candidate, of every party, ${res ? 'was' : 'is'} on the same November 3 ballot. A majority wins outright; otherwise the top two meet in a runoff${runoff && !res ? ` on ${runoff}` : ''}. With this many candidates and little public polling, Informed Voter didn’t estimate each candidate’s chances; it showed the expected split between the parties and forecasters’ ratings instead.`}</p>
      <div class="row" style="justify-content:center">
        ${res ? resultChips(race) : ''}
        ${ratingChip(f)}
        ${f.dr != null ? html`<span class="chip" title="${L('Écart attendu entre l’ensemble des candidats démocrates et l’ensemble des candidats républicains, d’après les cotes des analystes et l’orientation partisane de la circonscription', 'Expected margin between all Democratic and all Republican candidates combined, from forecasters’ ratings and the district’s partisan lean')}">${L('Attendu', 'Expected')} <b>${fmtDR(f.dr)}</b> ${L('par parti', 'by party')}</span>` : ''}
        ${runoff && res?.status !== 'won' ? html`<span class="chip">${L('Second tour', 'Runoff')} <b>${runoff}</b>${res?.status === 'runoff' ? '' : L(' si nécessaire', ' if needed')}</span>` : ''}
        ${updatedChip(race)}
        ${dataChip(race)}
        ${starBtn(race.id)}
      </div>
      ${forecasterRatings(race)}
      ${raceNotes(race)}
    </section>
    <div class="field-grid">${cands.map((c) => {
      const fin = financeOf(c);
      const inPoll = poll && poll.results[c.id] != null;
      const r = byRow.get(c.id);
      const won = r ? r.won : winners.has(c.id), toRunoff = r ? r.advance : adv.has(c.id);
      return html`<article class="cand ${partyClass(c.party)} field-cand${won ? ' winner' : ''}">
        <div class="cand-top">
          ${candBadge(c, colors[c.id])}
          <div style="min-width:0"><div class="cand-name">${c.name}</div><div class="cand-party">${PARTY_NAME[c.party] || c.party}</div></div>
          <div class="cand-actions">${heartBtn(c.id, c.name, { small: true })}</div>
        </div>
        ${won ? html`<div style="margin-top:10px"><span class="win-mark">${icon.check()} ${L('Victoire', 'Winner')}</span></div>` : toRunoff ? html`<div style="margin-top:10px"><span class="win-mark">${L('Au second tour', 'To the runoff')}</span></div>` : ''}
        <div class="field-stats">
          ${byRow.size
            ? html`<div><div class="eyebrow">${L('Voix', 'Vote')}</div><b>${r && rowShare(r) != null ? fmtPct(rowShare(r)) : '—'}</b>${r?.votes != null ? html`<div class="tiny faint">${L(`${fmtInt(r.votes)} voix`, `${fmtInt(r.votes)} votes`)}</div>` : ''}</div>`
            : html`<div><div class="eyebrow">${L('Dernier sondage', 'Latest poll')}</div><b>${inPoll ? fmtPct(poll.results[c.id]) : poll ? L('4 % ou moins', '4% or less') : '—'}</b></div>`}
          <div><div class="eyebrow">${L('Fonds levés', 'Raised')}</div><b>${hasFigures(fin) ? fmtMoney(fin.total) : L('Pas encore chargé', 'Not loaded yet')}</b></div>
        </div>
        <div class="meta">${candMeta(c)}</div>
      </article>`;
    })}</div>
    ${resultsTable(race)}
    ${raceTabs(race)}
    ${credits ? photoCredits(f.cands) : ''}
  </div>`;
}

// State legislative races: the field as Wikipedia lists it, who holds the seat, how
// the district voted for president in 2024 and any forecasters' ratings, with no
// odds (almost none are polled and few are rated; see scripts/lib/legislature.py).
function legislativeFull(race, { tag }) {
  const f = fc(race);
  const colors = candColors(f.cands);
  const H = raw(tag);
  const seats = race.seats || 1;
  const n = f.cands.length;
  const incs = (race.incumbents || []).filter((i) => i.name);
  const leaving = (s) => /retir|term|lost|running for|resign/i.test(s || '');
  const src = race.sources?.[0];
  return html`<div class="stack-lg">
    <section class="hero">
      <span class="label-pill"><span class="dots">•••</span> 2026 · ${raceShortTitle(race)} <span class="dots">•••</span></span>
      <${H} ${tag === 'h2' ? raw('class="display" style="font-size:clamp(26px,3.4vw,40px);margin:14px auto 10px;max-width:820px"') : ''}>${raceTitle(race)}${L(' : ', ': ')}<span class="grad-text">${n ? candCount(n) : L('candidatures pas encore listées', 'candidates not listed yet')}</span>${seats > 1 ? L(` pour ${seats} sièges`, ` for ${seats} seats`) : ''}.</${H}>
      <p class="lede">${seats > 1 ? L(`Cette circonscription élit ${seats} membres. `, `This district elects ${seats} members. `) : ''}${L('Informed Voter ne fait pas de prévisions pour les élections aux assemblées des États : presque aucune n’est sondée et peu sont cotées. Cette page montre donc qui se présente, qui détient le siège et comment la circonscription a voté à la présidentielle de 2024.', 'Informed Voter doesn’t forecast state legislative races: almost none are polled and few are rated, so this page shows who is running, who holds the seat and how the district voted for president in 2024.')}</p>
      <div class="row" style="justify-content:center">
        ${ratingChip(f)}
        ${f.dr != null ? html`<span class="chip" title="${L('Le vote de la circonscription à la présidentielle de 2024 (pas une prévision)', 'How the district voted for president in 2024 (not a forecast)')}">${L('Présidentielle 2024', '2024 president')} <b>${fmtDR(f.dr)}</b></span>` : ''}
        ${dataChip(race)}
        ${starBtn(race.id)}
      </div>
      ${incs.length ? html`<p class="small muted" style="margin:10px 0 0">${L('Siège actuellement détenu par', 'Now held by')} ${incs.map((i) => `${i.name} (${PARTY_NAME[i.party] || i.party || L('parti non indiqué', 'party not listed')})${leaving(i.status) ? `, ${statusL(i.status)}` : ''}`).join(L(' ; ', '; '))}.</p>` : ''}
      ${forecasterRatings(race)}
    </section>
    ${n ? html`<div class="field-grid">${f.cands.map((c) => html`<article class="cand ${partyClass(c.party)} field-cand">
        <div class="cand-top">
          ${candBadge(c, colors[c.id])}
          <div style="min-width:0"><div class="cand-name">${c.name}</div><div class="cand-party">${PARTY_NAME[c.party] || c.party}${c.incumbent ? L(' · en poste', ' · incumbent') : ''}${c.seat ? ` · ${c.seat}` : ''}</div></div>
          <div class="cand-actions">${heartBtn(c.id, c.name, { small: true })}</div>
        </div>
        ${c.bio || c.officialSite ? html`<div class="meta">${candMeta(c)}</div>` : ''}
      </article>`)}</div>`
      : html`<div class="notice">${icon.info()}<div>${L('La page Wikipédia de cette chambre ne donne pas encore les candidatures de novembre dans cette circonscription.', 'Wikipedia’s page for this chamber doesn’t list this district’s November candidates yet.')}</div></div>`}
    <p class="tiny faint" style="margin:0">${race.candidatesFrom === 'nominees' ? L('Voici les candidatures investies par les partis, telles que la page les liste ; une candidature indépendante ou sans adversaire peut manquer. ', 'These are the parties’ nominees as the page lists them; an independent or an unopposed candidate may be missing. ') : ''}${L('Source : ', 'Source: ')}${src ? ext(src.url, src.title) : L('Wikipédia', 'Wikipedia')}. ${race.candidates.some((c) => c.positions) ? L('Les positions ont été recherchées à la main, chacune liée à sa source ; les fonds levés des candidatures aux assemblées des États ne sont pas chargés.', 'Positions were researched by hand, each linked to its source; fundraising for state legislative candidates isn’t loaded.') : L('Les positions et les fonds levés des candidatures aux assemblées des États ne sont pas chargés.', 'Positions and fundraising for state legislative candidates aren’t loaded.')}</p>
    ${raceTabs(race)}
  </div>`;
}

// Everything for one race, top to bottom. `credits: false` leaves the photo credits to
// a page that lists them for every race it shows.
export function raceFull(race, { tag = 'h1', credits = true } = {}) {
  const f0 = fc(race);
  if (f0.open) {
    if (f0.kind === 'field') return legislativeFull(race, { tag });
    if (f0.kind === 'office') return officeFull(race, { tag, credits });
    return openPrimaryFull(race, { tag, credits });
  }
  if (race.result || awaitingResult(race)) {
    return html`<div class="stack-lg">
      ${resultsHero(race, { tag })}
      ${resultCards(race)}
      ${liveBlock(race)}
      ${resultsTable(race)}
      ${forecastRecap(race)}
      ${raceTabs(race)}
      ${credits ? photoCredits(f0.cands) : ''}
    </div>`;
  }
  return html`<div class="stack-lg">
    ${raceHero(race, { tag })}
    ${candidateCards(race)}
    ${waffleBlock(race)}
    ${statTiles(race)}
    ${raceTabs(race)}
    ${credits ? photoCredits(f0.cands) : ''}
  </div>`;
}

// The statewide offices below governor (attorney general, secretary of state, lieutenant
// governor, treasurer, auditor or comptroller): who ran, who held the office, how the
// state voted for president in 2024, any forecaster's rating and the results, with no
// odds (few are polled; see scripts/lib/offices.py). Positions, where researched, are
// under "Where they stand", matched with the same scale as every other race.
function officeFull(race, { tag, credits }) {
  const f = fc(race);
  const H = raw(tag);
  const res = race.result;
  const rows = resultRows(race).filter((r) => r.cand);
  const byRow = new Map(rows.map((r) => [r.cand.id, r]));
  const winners = new Set(res?.winners || []), adv = new Set(res?.advance || []);
  const ahead = (c) => (winners.has(c.id) || adv.has(c.id) ? 1 : 0);
  const order = [...rows.map((r) => f.cands.find((c) => c.id === r.cand.id)).filter(Boolean), ...f.cands.filter((c) => !byRow.has(c.id)).sort((a, b) => ahead(b) - ahead(a))];
  const colors = raceColors(race);
  const n = f.cands.length;
  const s = STATE_BY_ABBR[race.state];
  const held = race.held && (PARTY_PLURAL[race.held] || PARTY_NAME[race.held]);
  const rated = f.rating && f.rating !== 'Not rated';
  const after = res || awaitingResult(race);
  return html`<div class="stack-lg">
    <section class="hero">
      <span class="label-pill"><span class="dots">•••</span> ${after ? L('Résultats 2026', '2026 results') : '2026'} · ${raceShortTitle(race)} <span class="dots">•••</span></span>
      <${H} ${tag === 'h2' ? raw('class="display" style="font-size:clamp(26px,3.4vw,40px);margin:14px auto 10px;max-width:820px"') : ''}>${after ? resultHead(race) : html`${raceTitle(race)}${L(' : ', ': ')}<span class="grad-text">${candCount(n)}</span>.`}</${H}>
      <p class="lede">${after ? resultLede(race) : ''} ${L(`Informed Voter ne fait pas de prévisions pour ces élections : peu sont sondées, et seul le Crystal Ball de Sabato en cote certaines. Cette page montre les candidatures, qui occupait le poste${race.pres24 != null ? ', le vote de l’État à la présidentielle de 2024' : ''} et les résultats.`, `Informed Voter doesn’t forecast these races: few are polled, and only Sabato’s Crystal Ball rates some of them. This page shows who ran, who held the office${race.pres24 != null ? `, how ${s.name} voted for president in 2024` : ''} and the results.`)}</p>
      <div class="row" style="justify-content:center">
        ${after ? resultChips(race) : ''}
        ${rated ? ratingChip(f) : ''}
        ${held ? html`<span class="chip">${L('Détenu par', 'Held by')} <b>${held}</b>${race.open ? L(' · poste à pourvoir', ' · open seat') : ''}</span>` : ''}
        ${race.pres24 != null ? html`<span class="chip" title="${L('Le vote de l’État à la présidentielle de 2024 (pas une prévision)', 'How the state voted for president in 2024 (not a forecast)')}">${L('Présidentielle 2024', '2024 president')} <b>${fmtDR(race.pres24)}</b></span>` : ''}
        ${dataChip(race)}
        ${starBtn(race.id)}
      </div>
      ${forecasterRatings(race)}
      ${raceNotes(race)}
    </section>
    <div class="field-grid">${order.map((c) => {
      const r = byRow.get(c.id);
      const fin = financeOf(c);
      const won = r ? r.won : winners.has(c.id), toRunoff = r ? r.advance : adv.has(c.id);
      return html`<article class="cand ${partyClass(c.party)} field-cand${won ? ' winner' : ''}">
        <div class="cand-top">
          ${candBadge(c, colors[c.id])}
          <div style="min-width:0"><div class="cand-name">${c.name}</div><div class="cand-party">${PARTY_NAME[c.party] || c.party}${c.incumbent ? L(' · en poste', ' · incumbent') : ''}</div></div>
          <div class="cand-actions">${heartBtn(c.id, c.name, { small: true })}</div>
        </div>
        ${won ? html`<div style="margin-top:10px"><span class="win-mark">${icon.check()} ${L('Victoire', 'Winner')}</span></div>` : toRunoff ? html`<div style="margin-top:10px"><span class="win-mark">${L('Au second tour', 'To the runoff')}</span></div>` : ''}
        <div class="field-stats">
          <div><div class="eyebrow">${L('Voix', 'Vote')}</div><b>${r && rowShare(r) != null ? fmtPct(rowShare(r)) : res?.rows?.length ? '—' : L('Pas encore publié', 'Not posted yet')}</b>${r?.votes != null ? html`<div class="tiny faint">${L(`${fmtInt(r.votes)} voix`, `${fmtInt(r.votes)} votes`)}</div>` : ''}</div>
          <div><div class="eyebrow">Positions</div><b>${Object.keys(c.positions || {}).length || '—'}</b><div class="tiny faint">${Object.keys(c.positions || {}).length ? L('sourcées', 'sourced') : L('pas encore recherchées', 'not researched yet')}</div></div>
        </div>
        ${hasFigures(fin) ? html`<div class="tiny faint" style="margin-top:8px">${L(`Fonds levés : ${fmtMoney(fin.total)}${fin.asOf ? ` au ${fmtShortDate(day(fin.asOf))}` : ''}`, `Raised ${fmtMoney(fin.total)}${fin.asOf ? ` through ${fmtShortDate(day(fin.asOf))}` : ''}`)}</div>` : ''}
        ${c.bio || c.officialSite || c.wiki ? html`<div class="meta">${candMeta(c)}</div>` : ''}
      </article>`;
    })}</div>
    ${resultsTable(race)}
    <p class="tiny faint" style="margin:0">${L('Candidatures d’après ', 'Candidates from ')}${race.sources?.[0] ? ext(race.sources[0].url, race.sources[0].title) : L('Wikipédia', 'Wikipedia')}${race.sources?.[1] ? html`${L(' et ', ' and ')}${ext(race.sources[1].url, race.sources[1].title)}` : ''}. ${L('Les positions sont ajoutées à la main, chacune liée aux propres mots de la personne candidate, et ne sont jamais déduites du parti.', 'Issue positions are added by hand, each linked to the candidate’s own words, and are never inferred from party.')}</p>
    ${raceTabs(race)}
    ${credits ? photoCredits(f.cands) : ''}
  </div>`;
}

export function compactRace(race, { label } = {}) {
  const f = fc(race);
  if (f.open) return raceRow(race);
  const colors = candColors(f.cands);
  const rows = resultRows(race).filter((r) => r.cand);
  if (race.result || awaitingResult(race)) {
    // After Election Day: the count's top two, or, before any count is posted, the
    // winner (if called) and the runner-up of the final forecast, with no shares.
    const res = race.result;
    const winners = new Set(res?.winners || []), adv = new Set(res?.advance || []);
    const byRow = new Map(rows.map((r) => [r.cand.id, r]));
    const ahead = (c) => (winners.has(c.id) || adv.has(c.id) ? 1 : 0);
    const top = rows.length ? rows.slice(0, 2).map((r) => r.cand) : [...f.cands].sort((a, b) => ahead(b) - ahead(a)).slice(0, 2);
    return html`<div class="card">
      <div class="row between" style="margin-bottom:12px">
        <div><div class="eyebrow">${label || officeLabel(race)}</div><h3 style="margin:2px 0 0">${raceTitle(race)}</h3></div>
        <div class="row">${dataChip(race)}${resultChip(race)}${starBtn(race.id)}</div>
      </div>
      <div class="compact-race">
        <div class="h2h">${top.map((c) => {
          const r = byRow.get(c.id);
          const won = r ? r.won : winners.has(c.id), toRunoff = r ? r.advance : adv.has(c.id);
          return html`<div class="compact-cand ${partyClass(c.party)}${won ? ' winner' : ''}">
          ${candBadge(c, colors[c.id])}
          <div style="min-width:0"><div class="nm">${c.name}</div><div class="tiny faint">${won ? html`<span class="win-mark">${icon.check()} ${L('Victoire', 'Winner')}</span> ` : toRunoff ? L('Au second tour · ', 'To the runoff · ') : ''}${PARTY_NAME[c.party] || c.party}${r?.votes != null ? L(` · ${fmtCompact(r.votes)} voix`, ` · ${fmtCompact(r.votes)} votes`) : ''}</div></div>
          <div class="sh" style="color:${colors[c.id]}">${r && rowShare(r) != null ? fmtPct(rowShare(r), 1) : '—'}</div>
          ${heartBtn(c.id, c.name, { small: true })}
        </div>`;
        })}</div>
        <a class="btn btn-sm" href="#/race/${race.id}">${res ? L('Tous les résultats', 'Full results') : L('Page de l’élection', 'Race page')}</a>
      </div>
      ${rows.length ? (liveFc(race) ? html`<p class="tiny faint" style="margin:10px 0 0">${L('Pas encore attribuée.', 'Not called yet.')} ${liveSentence(race)}</p>` : '') : html`<p class="tiny faint" style="margin:10px 0 0">${res ? L('Décompte pas encore publié.', 'Vote count not posted yet.') : L('Pas encore de résultat.', 'No result yet.')} ${L(`Dernière prévision : ${ratingL(f.rating)}, ${lastName(f.lead.name)} ${fmtProb(f.pLead)} de chances de gagner.`, `Final forecast: ${f.rating}, ${lastName(f.lead.name)} ${fmtProb(f.pLead)} to win.`)}</p>`}
    </div>`;
  }
  return html`<div class="card">
    <div class="row between" style="margin-bottom:12px">
      <div><div class="eyebrow">${label || officeLabel(race)}</div><h3 style="margin:2px 0 0">${raceTitle(race)}</h3></div>
      <div class="row">${dataChip(race)}${ratingChip(f)}${starBtn(race.id)}</div>
    </div>
    <div class="compact-race">
      <div class="h2h">${f.cands.slice(0, 2).map((c) => html`<div class="compact-cand ${partyClass(c.party)}">
        ${candBadge(c, colors[c.id])}
        <div style="min-width:0"><div class="nm">${c.name}</div><div class="tiny faint">${PARTY_NAME[c.party] || c.party} · ${L(`${fmtProb(c.win)} de chances de gagner · ${fmtCompact(c.votes)} voix`, `${fmtProb(c.win)} to win · ${fmtCompact(c.votes)} votes`)}</div></div>
        <div class="sh" style="color:${colors[c.id]}">${fmtPct(c.share, 1)}</div>
        ${heartBtn(c.id, c.name, { small: true })}
      </div>`)}</div>
      <a class="btn btn-sm" href="#/race/${race.id}">${L('Prévision complète', 'Full forecast')}</a>
    </div>
  </div>`;
}

// The count's top two, Democrat on the left when they are a Democrat and a Republican,
// the winner checked.
function miniResult(race) {
  const m = resultMargin(race);
  const st = race.result?.status;
  if (!m || !m.a.cand || !m.b.cand) {
    const rows = resultRows(race).filter((r) => !r.other && rowShare(r) != null);
    const text = rows.length ? rows.slice(0, 2).map((r) => `${lastName(r.name)} ${fmtPct(rowShare(r), 1)}`).join(' · ')
      : st === 'won' ? (race.candidates.length === 1 ? L('Sans adversaire', 'Ran unopposed') : L('Décompte pas encore publié', 'Vote count not posted yet'))
        : st === 'runoff' ? L('Vers un second tour', 'Headed to a runoff') : st === 'counting' ? L('Dépouillement en cours', 'Votes being counted') : L('Pas encore attribuée', 'Not called yet');
    return html`<div class="mini-h2h"><span class="small muted">${text}</span></div>`;
  }
  const colors = candColors(fc(race).cands);
  const [lt, rt] = m.b.party === 'D' || (m.a.party === 'R' && m.b.party !== 'R') ? [m.b, m.a] : [m.a, m.b];
  const tot = rowShare(lt) + rowShare(rt) || 1;
  const nm = (r) => html`${r.won ? html`<span class="win-tick" title="${L('Victoire', 'Winner')}">${icon.check()}</span>` : ''}${lastName(r.name)}`;
  return html`<div class="mini-h2h">
    <span class="l">${nm(lt)} <b>${fmtPct(rowShare(lt), 1)}</b></span>
    <span class="bar"><span style="flex:${rowShare(lt) / tot};background:${colors[lt.cand.id]}"></span><span style="flex:${rowShare(rt) / tot};background:${colors[rt.cand.id]}"></span></span>
    <span><b>${fmtPct(rowShare(rt), 1)}</b> ${nm(rt)}</span>
  </div>`;
}

// Left-right mini head-to-head, Democrat on the left when there is one.
export function miniH2H(race) {
  const f = fc(race);
  if (race.result || awaitingResult(race)) return miniResult(race);
  if (f.kind === 'office') return html`<div class="mini-h2h"><span class="small muted">${candCount(f.cands.length)}${afterElection() ? L(' · résultats pas encore connus', ' · results not in yet') : ''}</span></div>`;
  if (f.kind === 'field') return html`<div class="mini-h2h"><span class="small muted">${f.cands.length ? candCount(f.cands.length) : L('Candidatures pas encore listées', 'Candidates not listed yet')}</span></div>`;
  if (f.open) return html`<div class="mini-h2h"><span class="small muted">${L(`${f.cands.length} candidatures · primaire ouverte`, `${f.cands.length} candidates · open primary`)}</span></div>`;
  if (!f.second) return html`<div class="mini-h2h"><span class="small muted">${lastName(f.lead.name)}${L(' sans adversaire', ' unopposed')}</span></div>`;
  const colors = candColors(f.cands);
  const d = f.cands.find((c) => c.party === 'D'), r = f.cands.find((c) => c.party === 'R');
  const [lc, rc] = f.dr != null && d && r ? [d, r] : [f.second, f.lead];
  const tot = lc.share + rc.share;
  return html`<div class="mini-h2h">
    <span class="l">${lastName(lc.name)} <b>${fmtPct(lc.share, 1)}</b></span>
    <span class="bar"><span style="flex:${lc.share / tot};background:${colors[lc.id]}"></span><span style="flex:${rc.share / tot};background:${colors[rc.id]}"></span></span>
    <span><b>${fmtPct(rc.share, 1)}</b> ${lastName(rc.name)}</span>
  </div>`;
}

export function raceRow(race, { right } = {}) {
  const f = fc(race);
  const sub = race.result || awaitingResult(race)
    ? `${officeLabel(race)} · ${race.result ? resultLine(race) : L('Pas encore attribuée', 'Not called yet')}${f.open ? '' : L(` · prévision ${ratingL(f.rating)}`, ` · forecast ${f.rating}`)}`
    : f.kind === 'office' ? `${officeLabel(race)}${f.rating !== 'Not rated' ? ` · ${ratingL(f.rating)}` : ''}${f.dr != null ? L(` · ${fmtDR(f.dr)} en 2024`, ` · ${fmtDR(f.dr)} in 2024`) : ''}`
      : `${officeLabel(race)} · ${ratingL(f.rating)} · ${leadStr(f)}`;
  return html`<a class="race-row" href="#/race/${encodeURIComponent(race.id)}">
    <div><div class="title">${raceTitle(race)}</div><div class="sub">${sub}</div></div>
    ${miniH2H(race)}
    <div class="row">${right || ''}${race.result ? resultChip(race) : ''}${dataChip(race)}</div>
  </a>`;
}

// Tabs ------------------------------------------------------------------------

export function raceTabs(race) {
  if (fc(race).kind === 'office') {
    // Statewide offices: "Where they stand" first (the reason to open these pages), then
    // any polls the race's page lists and any money its state filings report.
    const tabs = [['issues', L('Leurs positions', 'Where they stand')]];
    if (race.polls.length) tabs.push(['polls', L('Sondages', 'Polling')]);
    if (race.candidates.some((c) => hasFigures(c.finance) || c.finance?.note)) tabs.push(['money', L('Financement', 'Money')]);
    return html`<div class="race-tabs" data-race="${race.id}">
      <div class="tabs" role="tablist" aria-label="${L('Détails de l’élection', 'Race details')}">${tabs.map(([k, l], i) => html`<button role="tab" type="button" data-tab="${k}" aria-selected="${String(i === 0)}">${l}</button>`)}</div>
      <div class="tab-panel" role="tabpanel"></div>
    </div>`;
  }
  if (fc(race).kind === 'field') {
    // State legislative races load no polls or money: only "Where they stand", once
    // some candidate's positions have been researched.
    if (!race.candidates.some((c) => Object.keys(c.positions || {}).length)) return '';
    return html`<div class="race-tabs" data-race="${race.id}">
      <div class="tabs" role="tablist" aria-label="${L('Détails de l’élection', 'Race details')}"><button role="tab" type="button" data-tab="issues" aria-selected="true">${L('Leurs positions', 'Where they stand')}</button></div>
      <div class="tab-panel" role="tabpanel"></div>
    </div>`;
  }
  const open = fc(race).open;
  const tabs = [['polls', L('Sondages', 'Polling')]];
  if (!open) tabs.push(['trend', L('Évolution', 'Trend')]);
  if (SHOW_EARLY_VOTE && earlyVoteOf(race)) tabs.push(['early', L('Vote anticipé', 'Early vote')]);
  tabs.push(['money', L('Financement', 'Money')], ['issues', L('Leurs positions', 'Where they stand')]);
  return html`<div class="race-tabs" data-race="${race.id}">
    <div class="tabs" role="tablist" aria-label="${L('Détails de l’élection', 'Race details')}">${tabs.map(([k, l], i) => html`<button role="tab" type="button" data-tab="${k}" aria-selected="${String(i === 0)}">${l}</button>`)}</div>
    <div class="tab-panel" role="tabpanel"></div>
  </div>`;
}

export function mountRaceTabs(root) {
  root.querySelectorAll('.race-tabs').forEach((wrap) => {
    if (wrap._mounted) return;
    wrap._mounted = true;
    const race = getRace(wrap.dataset.race);
    const panel = wrap.querySelector('.tab-panel');
    const show = (k) => {
      wrap.querySelectorAll('[data-tab]').forEach((b) => b.setAttribute('aria-selected', String(b.dataset.tab === k)));
      panel.innerHTML = String(TABS[k].render(race));
      TABS[k].mount?.(panel, race);
    };
    wrap.querySelector('.tabs').addEventListener('click', (e) => {
      const b = e.target.closest('[data-tab]');
      if (b) show(b.dataset.tab);
    });
    show(wrap.querySelector('[data-tab]').dataset.tab); // the first tab: polling, or "Where they stand" alone
  });
}

const tableToggle = (id) => html`<button type="button" class="btn btn-sm btn-ghost" data-table-toggle="${id}">${icon.table()} ${L('Tableau', 'Table')}</button>`;
export function wireTableToggles(root) {
  root.querySelectorAll('[data-table-toggle]').forEach((b) => {
    b.addEventListener('click', () => {
      const t = root.querySelector(`#${b.dataset.tableToggle}`);
      if (t) t.hidden = !t.hidden;
    });
  });
}

function pollsterCell(p) {
  const name = p.url ? ext(p.url, p.pollster) : p.pollster;
  return html`${name}${p.demo ? html` ${demoChip()}` : ''}${p.sponsor ? html`<div class="tiny faint">${p.sponsor}</div>` : ''}`;
}

function pollNotes(race) {
  const notes = race.polls.filter((p) => p.note);
  return notes.length ? html`<ul class="race-notes" style="text-align:left">${notes.map((p) => html`<li>${p.pollster}${L(' : ', ': ')}<span lang="en">${p.note}</span></li>`)}</ul>` : '';
}

// The two candidates a margin is measured between: the strongest Democrat and
// Republican when there are both, otherwise the top two.
function marginPair(f) {
  const d = f.cands.find((c) => c.party === 'D'), r = f.cands.find((c) => c.party === 'R');
  return f.dr != null && d && r ? [d, r] : [f.lead, f.second];
}
const shiftText = (x, a, b) => {
  if (x == null) return '—';
  if (Math.abs(x) < 0.05) return L('Aucun changement', 'No change');
  const toward = x > 0 ? a : b;
  return toward.party === 'D' || toward.party === 'R' ? `${toward.party} +${fmtNum(Math.abs(x))}` : `${lastName(toward.name)} +${fmtNum(Math.abs(x))}`;
};

// How far the polling average and the forecast moved over the last week and month.
function changeStats(race) {
  const f = fc(race);
  if (!f.second) return '';
  const [a, b] = marginPair(f);
  const week = changeOver(race, 7), month = changeOver(race, 30);
  if (!week || !month) return '';
  const last = race.polls.reduce((m, p) => (!m || p.end > m.end ? p : m), null);
  const cell = (c, label) => {
    const quiet = c.pollsIn === 0;
    const value = c.pollStarted ? L('Premiers sondages', 'First polls') : quiet && c.poll != null && Math.abs(c.poll) < 0.05 ? L('Aucun changement', 'No change') : shiftText(c.poll, a, b);
    const sub = c.pollsIn
      ? L(`${c.pollsIn} nouveau${c.pollsIn === 1 ? '' : 'x'} sondage${c.pollsIn === 1 ? '' : 's'} ; évolution de la prévision : ${shiftText(c.margin, a, b)}`, `${c.pollsIn} new poll${c.pollsIn === 1 ? '' : 's'}; the forecast moved ${shiftText(c.margin, a, b)}`)
      : L('Aucun nouveau sondage : la moyenne ne bouge pas', 'No new polls, so the average holds steady');
    return html`<div class="stat"><div class="eyebrow">${L(`Moyenne des sondages, ${label}`, `Polling average, ${label}`)}</div><div class="value" style="font-size:22px">${value}</div><div class="sub">${sub}</div></div>`;
  };
  return html`<div class="grid grid-3">
    ${cell(week, L('7 derniers jours', 'last 7 days'))}
    ${cell(month, L('30 derniers jours', 'last 30 days'))}
    <div class="stat"><div class="eyebrow">${L('Dernier sondage', 'Latest poll')}</div><div class="value" style="font-size:22px">${last ? fmtShortDate(day(last.end)) : '—'}</div><div class="sub">${last ? `${last.pollster}${last.n ? `, ${fmtInt(last.n)} ${popL(last.pop)}` : ''}` : ''}</div></div>
  </div>`;
}

// Ranked-choice races: the final round each poll reported, which drives the forecast.
function finalRoundTable(race) {
  const polls = race.finalPolls || [];
  if (!race.rcv || !polls.length) return '';
  const ids = [...new Set(polls.flatMap((p) => Object.keys(p.results)))];
  const name = (id) => race.candidates.find((c) => c.id === id)?.name || id;
  return html`<div class="stack-sm">
    <div><h3 style="margin:0">${L('Dernier tour des sondages par classement', 'Final round of the ranked-choice polls')}</h3><p class="small muted" style="margin:0">${L('Après élimination des candidats les moins bien classés de chaque sondage et report de leurs bulletins sur les choix suivants des électeurs. Ce sont ces chiffres qui fixent le dernier tour de la prévision.', 'After each poll’s lower-ranked candidates were eliminated and their ballots moved to voters’ next choices. These set the forecast’s final round.')}</p></div>
    <div class="table-wrap"><table class="data"><thead><tr><th>${L('Institut', 'Pollster')}</th><th>Dates</th><th class="r">${L('Tour', 'Round')}</th>${ids.map((id) => html`<th class="r">${lastName(name(id))}</th>`)}</tr></thead><tbody>
      ${polls.map((p) => html`<tr><td>${pollsterCell(p)}</td><td>${p.start ? `${fmtShortDate(day(p.start))}–` : ''}${pollDate(day(p.end))}</td><td class="r">${p.round}</td>${ids.map((id) => html`<td class="r">${p.results[id] != null ? fmtPct(p.results[id], 1) : '—'}</td>`)}</tr>`)}
    </tbody></table></div>
  </div>`;
}

// Our average next to the published averages Wikipedia compiles, as a check.
function aggregatorCheck(race) {
  const aggs = (race.aggregates || []).filter((x) => !x.average);
  const f = fc(race);
  if (!aggs.length || !f.poll || !f.second) return '';
  const [a, b] = marginPair(f);
  const m = (res) => (res[a.id] != null && res[b.id] != null ? res[a.id] - res[b.id] : null);
  const ours = m(f.poll.shares);
  const theirs = aggs.map((x) => m(x.results)).filter((x) => x != null);
  const avg = theirs.length ? theirs.reduce((s, x) => s + x, 0) / theirs.length : null;
  const close = avg != null && ours != null && Math.abs(avg - ours) <= 4;
  return html`<div class="card tight">
    <div class="row between"><div class="eyebrow">${L('Comparée aux moyennes de sondages publiées', 'Checked against published polling averages')}</div>${avg != null ? html`<span class="small ${close ? 'good-text' : 'warn-text'}">${close ? L('À moins de 4 points', 'Within 4 points') : L('Plus de 4 points d’écart', 'More than 4 points apart')}</span>` : ''}</div>
    <div class="ratings-row" style="justify-content:flex-start;margin-top:10px">
      <span class="chip">Informed Voter <b>${shiftText(ours, a, b)}</b></span>
      ${aggs.map((x) => html`<span class="chip">${x.source} <b>${shiftText(m(x.results), a, b)}</b>${x.updated ? html`&nbsp;· ${fmtShortDate(day(x.updated))}` : ''}</span>`)}
    </div>
    <p class="tiny faint" style="margin:8px 0 0">${L('Chaque agrégateur pondère et ajuste les sondages à sa façon ; la nôtre est une moyenne simple pondérée par l’ancienneté, la taille de l’échantillon et le filtre d’électeurs, sans correction des effets d’institut. Moyennes publiées compilées par ', 'Each aggregator weights and adjusts polls its own way; ours is a plain average weighted by recency, sample size and voter screen, with no house-effect adjustments. Published averages compiled by ')}${race.sources?.[0] ? ext(race.sources[0].url, L('Wikipédia', 'Wikipedia')) : L('Wikipédia', 'Wikipedia')}.</p>
  </div>`;
}

// Polling reaches back into last year, so an earlier date names its year.
const pollDate = (d) => (d.getFullYear() < new Date().getFullYear() ? fmtDate(d) : fmtShortDate(d));

const TABS = {
  polls: {
    render(race) {
      const f = fc(race);
      if (!race.polls.length) {
        return html`<div class="notice">${icon.info()}<div>${L('Aucun sondage public de cette élection pour l’instant.', 'No public polls of this race yet.')} ${f.open ? '' : L(`La prévision s’appuie donc sur l’orientation partisane de ${race.statewide ? 'l’État' : 'la circonscription'}, d’où une fourchette plus large.`, `The forecast leans on the ${race.statewide ? 'state' : 'district'}’s partisan baseline instead, so its range is wider.`)}</div></div>`;
      }
      const tid = `polltbl-${race.id.replace(/[^\w-]/g, '')}`;
      const polledCands = f.cands.filter((c) => race.polls.some((p) => p.results[c.id] != null));
      const table = html`<div class="table-wrap" id="${tid}" ${raw(f.open ? '' : 'hidden')}><table class="data"><thead><tr><th>${L('Institut', 'Pollster')}</th><th>Dates</th><th class="r">${L('Échantillon', 'Sample')}</th>${polledCands.map((c) => html`<th class="r">${lastName(c.name)}</th>`)}</tr></thead><tbody>
          ${race.polls.map((p) => html`<tr><td>${pollsterCell(p)}</td><td>${p.start ? `${fmtShortDate(day(p.start))}–` : ''}${pollDate(day(p.end))}</td><td class="r">${p.n ? `${p.approx ? '~' : ''}${fmtInt(p.n)}` : '—'} ${popL(p.pop)}</td>${polledCands.map((c) => html`<td class="r">${p.results[c.id] != null ? fmtPct(p.results[c.id], 1) : '—'}</td>`)}</tr>`)}
        </tbody></table></div>`;
      if (f.kind === 'office') {
        return html`<div class="stack"><div><h3 style="margin:0">${L('Sondages de cette élection', 'Polls of this race')}</h3><p class="small muted" style="margin:0">${L('Présentés tels que publiés. Informed Voter ne fait ni moyenne ni prévision pour ces postes.', 'Shown as published. Informed Voter doesn’t average or forecast races for these offices.')}</p></div>${table}${pollNotes(race)}</div>`;
      }
      if (f.open) {
        return html`<div class="stack"><div><h3 style="margin:0">${L('Sondages de la primaire ouverte', 'Polls of the open primary')}</h3><p class="small muted" style="margin:0">${L('Présentés tels que publiés. Avec beaucoup d’indécis et un seul sondage, c’est un instantané, pas une prévision.', 'Shown as published. With many undecided voters and one poll, treat these as a snapshot, not a forecast.')}</p></div>${table}${pollNotes(race)}</div>`;
      }
      const colors = candColors(f.cands);
      const h = pollHist(race);
      const since = h.length ? pollDate(h[0].date) : '';
      return html`<div class="stack">
        <div class="row between"><div><h3 style="margin:0">${L(`Moyenne des sondages depuis le ${since}`, `Polling average since ${since}`)}</h3><p class="small muted" style="margin:0">${L('Chaque point est un sondage ; la ligne est la moyenne du jour, pondérée par l’ancienneté (demi-vie de 14 jours), la taille de l’échantillon et le filtre d’électeurs. Les indécis sont indiqués tels que sondés.', 'Each dot is one poll; the line is the average on that day, weighted by recency (14-day half-life), sample size and voter screen. Undecideds are shown as polled.')}</p></div>${tableToggle(tid)}</div>
        ${changeStats(race)}
        <div class="chart" data-chart="polls"></div>
        ${table}
        <div class="legend-list">${f.cands.filter((c) => c.poll != null).map((c) => html`<span><i class="key-line" style="background:${colors[c.id]}"></i>${L(`${c.name} : ${fmtPct(c.poll)} dans la moyenne`, `${c.name}: ${fmtPct(c.poll)} in the average`)}</span>`)}</div>
        ${finalRoundTable(race)}
        ${aggregatorCheck(race)}
        ${pollNotes(race)}
      </div>`;
    },
    mount(panel, race) {
      wireTableToggles(panel);
      const el = panel.querySelector('[data-chart="polls"]');
      if (!el) return;
      const f = fc(race);
      const colors = candColors(f.cands);
      const days = pollHist(race);
      const start = days[0].date;
      // Candidates polling under 8% stay in the legend but off the chart, so the
      // main contest isn't flattened against a 0% baseline.
      const shown = f.cands.filter((c) => c.poll != null && (c.poll >= 8 || f.cands.filter((x) => x.poll != null).indexOf(c) < 2));
      const series = shown.map((c) => ({
        name: c.name, color: colors[c.id],
        values: days.map((d) => ({ x: d.date, y: d.fc.poll ? d.fc.poll.shares[c.id] ?? null : null })),
        points: race.polls.filter((p) => p.results[c.id] != null && day(p.end) >= start).map((p) => ({ x: day(p.end), y: p.results[c.id], title: L(`${p.pollster} : ${String(p.results[c.id]).replace('.', ',')}${pctSign()}`, `${p.pollster}: ${p.results[c.id]}%`) })),
      }));
      lineChart(el, { series, yFormat: (v) => fmtPct(v, 0), tipFormat: (v) => fmtPct(v, 1), label: L(`Moyenne des sondages depuis le ${pollDate(start)}`, `Polling average since ${pollDate(start)}`) });
    },
  },
  trend: {
    render(race) {
      const h = pollHist(race);
      return html`<div class="stack"><div><h3 style="margin:0">${L(`Chances de gagner depuis le ${h.length ? pollDate(h[0].date) : ''}`, `Chance of winning since ${h.length ? pollDate(h[0].date) : ''}`)}</h3><p class="small muted" style="margin:0">${L('Recalculées pour chaque jour avec les seuls sondages publiés à cette date.', 'Re-run for each day using only the polls published by then.')}</p></div><div class="chart" data-chart="trend"></div></div>`;
    },
    mount(panel, race) {
      const f = fc(race);
      const colors = candColors(f.cands);
      const days = pollHist(race);
      const series = f.cands.slice(0, 2).map((c) => ({
        name: c.name, color: colors[c.id],
        values: days.map((d) => ({ x: d.date, y: (d.fc.cands.find((x) => x.id === c.id)?.win ?? 0) * 100 })),
      }));
      lineChart(panel.querySelector('[data-chart="trend"]'), { series, yDomain: [0, 100], baseline: 50, yFormat: (v) => fmtPct(v, 0), label: L('Probabilité de victoire dans le temps', 'Win probability over time') });
    },
  },
  early: {
    render(race) {
      const ev = earlyVoteOf(race);
      const f = fc(race);
      const s = STATE_BY_ABBR[race.state];
      const when = ev.asOf ? L(`au ${fmtShortDate(ev.asOf + 'T12:00:00')}`, `as of ${fmtShortDate(ev.asOf + 'T12:00:00')}`) + (ev.label ? ` (${ev.label})` : '') : L('à ce jour', 'so far');
      const where = race.statewide ? s.name : `${s.name}’s ${race.districtName || 'district'}`;
      const head = lang() === 'fr'
        ? `Bulletins déposés ${race.statewide ? inState(race.state) : `dans la ${lcFirst(raceTitle(race))}`}, ${when}`
        : `Ballots cast in ${where}, ${when}`;
      return html`<div class="stack">
        <div class="row between"><h3 style="margin:0">${head}</h3>${ev.auto ? html`<span class="live-chip" title="${L('Mis à jour toutes les 8 heures à partir du suivi du vote anticipé de l’UF Election Lab', 'Refreshed every 8 hours from the UF Election Lab’s early-vote tracker')}">${L('Données en direct', 'Live data')}</span>` : dataChip(ev)}</div>
        ${ev.caveat ? html`<p class="small muted" style="margin:0" lang="en">${ev.caveat}</p>` : ''}
        <div class="grid grid-${2 + (ev.mail != null) + (ev.of2022 != null)}">
          <div class="stat"><div class="eyebrow">${L('Bulletins déposés', 'Ballots cast')}</div><div class="value">${fmtInt(ev.ballots)}</div><div class="sub">${ev.pctOfTurnout != null ? L(`${fmtPct(ev.pctOfTurnout * 100, 0)} de la participation projetée`, `${fmtPct(ev.pctOfTurnout * 100, 0)} of projected turnout`) : L('avant le jour du scrutin', 'before Election Day')}</div></div>
          ${ev.mail != null ? html`<div class="stat"><div class="eyebrow">${L('Par correspondance · en personne', 'By mail · in person')}</div><div class="value">${fmtCompact(ev.mail)} · ${fmtCompact(ev.inPerson)}</div><div class="sub">${L('bulletins par correspondance reçus · votes anticipés en personne', 'mail ballots returned · early in-person votes')}</div></div>` : ''}
          ${ev.of2022 != null ? html`<div class="stat"><div class="eyebrow">${L('Par rapport à 2022', 'Versus 2022')}</div><div class="value">${fmtPct(ev.of2022 * 100, 0)}</div><div class="sub">${L('du total des voix des élections de mi-mandat de 2022, déjà déposés', 'of the total 2022 midterm vote, already cast')}</div></div>` : ''}
          <div class="stat"><div class="eyebrow">${L('Total projeté', 'Projected total')}</div><div class="value">${fmtCompact(f.turnout)}</div><div class="sub">${L('voix attendues d’ici le soir de l’élection', 'votes expected by election night')}</div></div>
        </div>
        ${ev.byParty ? html`<div class="card tight"><div class="eyebrow" style="margin-bottom:8px">${L('Bulletins anticipés par affiliation déclarée', 'Early ballots by party registration')}</div>
          ${raw(stackedBar([{ name: L('Démocrates inscrits', 'Registered Democrats'), value: ev.byParty.D, color: cssVar('--dem') }, { name: L('Républicains inscrits', 'Registered Republicans'), value: ev.byParty.R, color: cssVar('--rep') }, { name: L('Autres / sans affiliation', 'Other / unaffiliated'), value: ev.byParty.other, color: cssVar('--other') }], { label: L('Bulletins anticipés par affiliation déclarée', 'Early ballots by party registration') }))}
          <div class="legend-list"><span><i class="key-box" style="background:var(--dem)"></i>${L('Démocrates', 'Democrats')} ${fmtPct(ev.byParty.D, 0)}</span><span><i class="key-box" style="background:var(--rep)"></i>${L('Républicains', 'Republicans')} ${fmtPct(ev.byParty.R, 0)}</span><span><i class="key-box" style="background:var(--other)"></i>${L('Autres', 'Other')} ${fmtPct(ev.byParty.other, 0)}</span></div>
          <p class="small faint" style="margin:8px 0 0">${L('L’affiliation déclarée n’est pas un décompte des voix : beaucoup d’électeurs votent pour l’autre camp.', 'Party registration is not a vote count: many registered voters cross over.')}</p></div>`
          : html`<p class="small muted">${PARTY_REGISTRATION.has(race.state) ? L('La répartition de ces bulletins par affiliation déclarée n’est pas encore publiée.', 'A breakdown of these ballots by party registration has not been published yet.') : L('Cet État n’enregistre pas l’affiliation partisane des électeurs : les bulletins anticipés ne peuvent donc pas être répartis ainsi.', `${s.name} does not register voters by party, so early ballots can’t be split that way.`)}</p>`}
        ${ev.note ? html`<p class="small muted" style="margin:0" lang="en">${ev.note}</p>` : ''}
        ${ev.source ? html`<p class="tiny faint" style="margin:0">${L('Source : ', 'Source: ')}${ext(ev.source.url, ev.source.title)}${ev.stateSource ? html` · ${ext(ev.stateSource, L('les chiffres de l’État', 'the state’s own figures'))}` : ''}</p>` : ''}
      </div>`;
    },
  },
  money: {
    render(race) {
      const f = fc(race);
      return html`<div class="stack">
        <div class="row between"><h3 style="margin:0">${L('Fonds levés', 'Fundraising')}</h3>${dataChip(race)}</div>
        <div class="grid grid-2">${f.cands.map((c) => financeCard(c))}</div>
        ${financeNote(race)}
      </div>`;
    },
  },
  issues: {
    render(race) {
      const f = fc(race);
      if (!isDemo(race) && !race.candidates.some((c) => Object.keys(c.positions || {}).length)) {
        return html`<div class="notice">${icon.info()}<div><b>${L('Les positions de cette élection n’ont pas encore été recherchées.', 'Positions for this race haven’t been researched yet.')}</b> ${race.format === 'office' ? L('Les candidatures, les cotes et les résultats se mettent à jour automatiquement toutes les 8 heures.', 'Candidates, ratings and results here refresh automatically every 8 hours.') : L('Les candidatures, les cotes, les sondages et les fonds levés se mettent à jour automatiquement toutes les 8 heures.', 'Candidates, ratings, polls and fundraising here refresh automatically every 8 hours.')} ${L('Les positions sont ajoutées à la main, chacune avec un lien vers les propos ou les votes de la personne candidate, et ne sont jamais déduites du parti.', 'Issue positions are added by hand, each with a link to the candidate’s own words or votes, and are never inferred from party.')} ${f.cands.filter((c) => c.wiki || c.officialSite).map((c) => html`<span class="nowrap">${ext(c.officialSite || c.wiki, c.name)}</span> `)}</div></div>`;
      }
      const fromVotes = !isDemo(race) && !race.research && race.candidates.some((c) => c.positionsFrom === 'votes');
      return html`<div class="stack">
        <div class="row between"><div><h3 style="margin:0">${L('Les positions des candidats', 'Where the candidates stand')}</h3><p class="small muted" style="margin:0">${L('Positions sur les questions du site, chacune liée à une source. Celles qui manquent restent vides, jamais devinées.', 'Positions on the site’s issue questions, each tied to a source. Missing ones are left blank, never guessed.')}</p></div>
          ${fromVotes ? '' : html`<a class="btn btn-sm btn-primary" href="#/elections/${race.id}/match?mode=profile">${L('Comparer avec mes opinions', 'Compare with my views')}</a>`}</div>
        ${fromVotes ? html`<div class="notice">${icon.info()}<div>${L('Les positions des membres actuels de la Chambre viennent de leurs votes enregistrés (2021 à 2026), chacun lié au scrutin publié par le greffier de la Chambre, et, pour les questions qu’aucun vote ne tranche, des textes déposés ou cosignés (santé, droits des personnes trans, énergie, actions en bourse, argent en politique, immigration), liés à Congress.gov. Les positions des autres candidatures de cette élection n’ont pas encore été recherchées : la comparaison côte à côte n’est donc pas proposée.', 'Positions shown for current House members come from their recorded House votes (2021 to 2026), each linked to the Clerk’s roll call, and, where no vote answers a question, from the bills they sponsored or cosponsored (health care, trans rights, energy, stock trading, money in politics, immigration), linked to Congress.gov. Other candidates’ positions in this race haven’t been researched yet, so a side-by-side match isn’t offered.')}</div></div>` : ''}
        <div class="grid grid-2">${f.cands.map((c) => positionsCard(c, race))}</div>
      </div>`;
    },
  },
};

// The receipt lines of a campaign finance report, in filing order.
export const FUNDING_PARTS = [
  ['small', 'Small donors (under $200)'],
  ['large', 'Large individual donors'],
  ['pac', 'PACs (business, labor, issue groups)'],
  ['party', 'Party committees'],
  ['self', 'Self-funding (candidate’s own money and loans)'],
  ['public', 'Public financing'],
  ['transfers', 'Transfers from joint fundraising committees and the candidate’s other campaigns'],
  ['other', 'Other (outside loans, refunds and other receipts)'],
];
export const FUND_FR = {
  small: 'Petits dons (moins de 200 $)',
  large: 'Gros dons individuels',
  pac: 'PAC (entreprises, syndicats, groupes d’intérêt)',
  party: 'Comités du parti',
  self: 'Fonds personnels (argent et prêts de la personne candidate)',
  public: 'Financement public',
  transfers: 'Transferts (comités de collecte conjoints et autres campagnes)',
  other: 'Autres (prêts extérieurs, remboursements, autres recettes)',
};
// Fixed categorical order: the reference palette's eight slots, whose adjacent
// pairs clear the colorblind checks in both themes.
const FUND_HEX = {
  dark: ['#3987e5', '#d95926', '#199e70', '#c98500', '#d55181', '#008300', '#9085e9', '#e66767'],
  light: ['#2a78d6', '#eb6834', '#1baf7a', '#eda100', '#e87ba4', '#008300', '#6250d6', '#e34948'],
};
export function fundColor(i) {
  const theme = document.documentElement.dataset.theme === 'light' ? 'light' : 'dark';
  return FUND_HEX[theme][i];
}

export function financeCard(c, { compact = false } = {}) {
  const fin = financeOf(c);
  if (!hasFigures(fin)) {
    return html`<div class="card tight"><div class="row between"><b>${c.name}</b><span class="faint small">${PARTY_NAME[c.party] || c.party}</span></div>
      <p class="small muted" style="margin:8px 0 0">${fin?.note || noFigures(c)}${fin?.note && fin.url ? html` <span class="faint">${ext(fin.url, fin.source || 'Source')}</span>` : ''}</p></div>`;
  }
  const parts = FUNDING_PARTS.map(([k, label], i) => ({ key: k, name: lang() === 'fr' ? FUND_FR[k] : label, value: (fin.parts || {})[k] || 0, color: fundColor(i) })).filter((p) => p.value > 0);
  const real = !fin.demo;
  return html`<div class="card tight">
    <div class="row between"><b>${c.name}</b><span class="faint small">${PARTY_NAME[c.party] || c.party}</span></div>
    <div class="row" style="gap:18px;margin:8px 0 10px">
      <div><div class="eyebrow">${L('Fonds levés', 'Raised')}</div><div style="font-size:22px;font-weight:750">${fmtMoney(fin.total)}</div></div>
      ${real ? '' : html`<div><div class="eyebrow">${L('Cette semaine', 'This week')}</div><div style="font-size:16px;font-weight:650">+${fmtMoney(fin.total - fin.weekAgoTotal)}</div></div>`}
      ${real && fin.spent != null ? html`<div><div class="eyebrow">${L('Dépensés', 'Spent')}</div><div style="font-size:16px;font-weight:650">${fmtMoney(fin.spent)}</div></div>` : ''}
      <div><div class="eyebrow">${L('En caisse', 'Cash on hand')}</div><div style="font-size:16px;font-weight:650">${fin.cashOnHand != null ? fmtMoney(fin.cashOnHand) : '—'}</div></div>
      ${real && fin.debts ? html`<div><div class="eyebrow">${L('Dettes', 'Debts')}</div><div style="font-size:16px;font-weight:650">${fmtMoney(fin.debts)}</div></div>` : ''}
    </div>
    ${parts.length ? raw(stackedBar(parts, { label: L(`Sources de financement : ${c.name}`, `${c.name} funding sources`) })) : html`<p class="small muted" style="margin:0">${noBreakdown(fin, c)}</p>`}
    ${compact || !parts.length ? '' : html`<table class="fund-table"><tbody>${parts.map((p) => html`<tr><td><span class="fund-label"><i class="key-box" style="background:${p.color}"></i>${p.name}</span></td><td class="num">${fmtMoney(p.value, { exact: true })}</td><td class="num faint">${fundShare(p.value, fin.total)}</td></tr>`)}</tbody></table>`}
    ${real && fin.asOf ? html`<p class="tiny faint" style="margin:8px 0 0">${lang() === 'fr' ? `Déclarations ${fin.from ? `du ${fmtDate(day(fin.from))} ` : ''}jusqu’au ${fmtDate(day(fin.asOf))}` : html`Reports ${fin.from ? html`from ${fmtDate(day(fin.from))} ` : ''}through ${fmtDate(day(fin.asOf))}`}${fin.url ? html` · ${ext(fin.url, sourceLabel(fin, c))}` : ''}${fin.note ? html` · <span lang="en">${fin.note}</span>` : ''}</p>` : ''}
  </div>`;
}

// Where the figures came from: the FEC for federal candidates (directly or as
// Wikipedia cites it), state filings for governors, or the named news report.
function sourceLabel(fin, c) {
  if (fin.source === 'FEC' || !fin.source) return 'FEC';
  if (getRace(c.raceId)?.level === 'federal') return L('FEC, via Wikipédia', 'FEC, via Wikipedia');
  return /via Wikipedia$/.test(fin.source) ? L('Déclarations à l’État, via Wikipédia', 'State filings, via Wikipedia') : fin.source;
}

// Missing figures are not evidence of no fundraising (a refresh may simply lack
// them), so only a researched note may say a candidate has filed nothing.
function noFigures(c) {
  const none = L('Les chiffres de financement de cette candidature ne sont pas encore chargés.', 'Fundraising figures for this candidate haven’t been loaded yet.');
  if (getRace(c.raceId)?.level !== 'federal') return none;
  return html`${none} ${ext(`https://www.fec.gov/data/candidates/?q=${encodeURIComponent(c.name)}`, L('Chercher les déclarations à la FEC', 'Search FEC filings'))}`;
}

// A source's share of the total: tiny and near-total shares keep their direction
// instead of rounding to 0% or 100% beside other sources.
function fundShare(value, total) {
  const pct = (value / total) * 100;
  if (pct > 0 && pct < 0.05) return `<${fmtNum(0.1)}${pctSign()}`;
  if (pct < 1) return fmtPct(pct, 1);
  if (pct > 99 && pct < 100) return `>99${pctSign()}`;
  return fmtPct(pct, 0);
}

function noBreakdown(fin, c) {
  if (fin.total === 0) return L('Aucun fonds levé dans les déclarations à ce jour.', 'No money raised in the filings so far.');
  if (fin.source === 'FEC' || getRace(c.raceId)?.level === 'federal') {
    return L(`La répartition par type de donateur de cette candidature n’est pas encore chargée${fin.url ? ' ; le lien FEC ci-dessous la donne' : ''}.`, `This candidate’s breakdown by type of donor hasn’t been loaded yet${fin.url ? '; the FEC link below has it' : ''}.`);
  }
  return L('Les déclarations de cet État ne donnent pour l’instant que des totaux : l’argent n’est donc pas réparti par type de donateur.', 'Only totals are available from this state’s filings so far, so the money isn’t split by type of donor.');
}

export function financeNote(race) {
  const pf = STATE_BY_ABBR[race.state].publicFinancing;
  return html`<p class="small faint">${race.level === 'federal'
    ? L('Les entreprises ne peuvent pas donner directement aux candidats fédéraux : l’argent des entreprises apparaît donc sous les PAC (et dans les dépenses extérieures des super PAC, déclarées à part). Les candidats fédéraux ne reçoivent aucun financement public.', 'Corporations can’t donate directly to federal candidates, so business money appears under PACs (and in outside spending by super PACs, which is reported separately). Federal candidates get no public financing.')
    : L(`Les règles varient selon les États.${pf ? ' Cet État offre un financement public aux candidatures qui remplissent les conditions.' : ''} Les chiffres réels viennent des déclarations de financement de campagne de l’État.`, `State rules vary. ${pf ? `${STATE_BY_ABBR[race.state].name} offers public financing to qualifying candidates.` : ''} Real figures come from the state’s campaign-finance filings.`)}</p>`;
}

function positionsCard(c, race) {
  const pos = positionsOf(c);
  const known = Object.entries(pos).filter(([, v]) => v && v.stance != null);
  const total = c.demo ? Object.keys(pos).length : questionsForLevel(race.level).length;
  const strongest = known.sort((a, b) => Math.abs(b[1].stance) - Math.abs(a[1].stance)).slice(0, 5);
  return html`<div class="card tight">
    <div class="row between"><b>${c.name}</b><span class="faint small">${L(`${known.length} sujets documentés sur ${total}`, `${known.length} of ${total} issues documented`)}</span></div>
    ${strongest.length ? html`<ul class="small muted" style="padding-left:18px;margin:8px 0 0">${strongest.map(([qid, v]) => html`<li style="margin:5px 0">${stanceSentence(lastName(c.name), QUESTION_BY_ID[qid], v.stance)}. <span class="faint">${v.source.url ? ext(v.source.url, v.source.title) : v.source.title}</span></li>`)}</ul>`
      : html`<p class="small muted" style="margin:8px 0 0">${L('Aucune position documentée trouvée pour l’instant sur les questions du site.', 'No documented positions found on the site’s questions yet.')}</p>`}
  </div>`;
}
