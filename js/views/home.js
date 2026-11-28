import { html, raw, fmtProb, fetchJSON, timeAgo, fmtDate } from '../util.js';
import { STATES, STATE_BY_ABBR, legislatureChambers, stateName, inState, chamberName } from '../data/states.js';
import { fc, mainRaces, statewideRaces, houseRaces, chamberSummary, getMapIndex, realRaceCount, racesMeta, getRace, raceTitle,
  resultsIn, resultsTally, resultParty, resultMargin, resultWinners, mapView, setMapView, liveFc, controlData, stillCounting, afterElection, ratingL } from '../data/world.js';
import { L, lang } from '../i18n.js';
import { daysToElection } from '../model/forecast.js';
import { drawMap, ratingColor, ratingLegendHTML, resultFill, resultsLegendHTML } from '../lib/map.js';
import { cssVar, sparkline } from '../lib/charts.js';
import { raceRow, lastName, demoChip, resultMarginStr } from '../components/race.js';
import { icon } from '../icons.js';
import { store } from '../store.js';
import { QUESTIONS } from '../data/questions.js';
import { loadHolders, delegation, governorOf } from '../data/holders.js';

let statesGeo = null;
let districtsGeo = null; // every House district, loaded the first time the House view is picked
let mode = 'senate';     // which races color the map: 'senate', 'house' or 'governor'
const MODES = () => [['senate', L('Sénat', 'Senate')], ['house', L('Chambre', 'House')], ['governor', L('Gouverneurs', 'Governor')]];
// French names of the three tiles: "Résultats du Sénat", "Sénat : démocrates 47…", and the
// unit counted ("siège" / "sièges").
const TILE_FR = {
  senate: { of: 'du Sénat', name: 'Sénat', one: 'siège', many: 'sièges' },
  house: { of: 'de la Chambre', name: 'Chambre', one: 'siège', many: 'sièges' },
  governor: { of: 'des gouverneurs', name: 'Gouverneurs', one: 'poste de gouverneur', many: 'postes de gouverneur' },
};
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
  if (g === 0) return html`<b>${L('aucun changement net', 'no net change')}</b>`;
  return g > 0 ? html`<b class="d-text">${L('Démocrates', 'Democrats')} +${g}</b>` : html`<b class="r-text">${L('Républicains', 'Republicans')} +${-g}</b>`;
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
  const T = TILE_FR[key];
  const name = L(T.name, label);
  return html`<div class="card control">
    <div class="row between"><div class="eyebrow">${L(`Contrôle ${T.of}`, `${label} control`)}</div>${live ? html`<span class="live-chip" title="${L(`Simulé 20 000 fois lors de la dernière mise à jour, le ${fmtDate(sum.updated)}`, `Simulated 20,000 times at the last refresh, ${fmtDate(sum.updated)}`)}">${L('En direct', 'Live')}</span>` : realRaceCount ? '' : demoChip()}</div>
    <div class="bar" role="img" aria-label="${L(`${name} : démocrates ${fmtProb(pD)}, républicains ${fmtProb(pR)}${pN >= 0.005 ? `, sans majorité ${fmtProb(pN)}` : ''}`, `${label}: Democrats ${fmtProb(pD)}, Republicans ${fmtProb(pR)}${pN >= 0.005 ? `, no majority ${fmtProb(pN)}` : ''}`)}"><span style="flex:${pD}"></span>${pN >= 0.005 ? html`<span class="n" style="flex:${pN}"></span>` : ''}<span style="flex:${pR}"></span></div>
    <div class="odds"><span><b class="d-text">${fmtProb(pD)}</b>${L('Démocrates', 'Democrats')}</span><span style="text-align:right"><b class="r-text">${fmtProb(pR)}</b>${L('Républicains', 'Republicans')}</span></div>
    ${seats ? (lang() === 'fr'
      ? html`<p class="gain">Attendu : <b>${seats.D} D</b> – <b>${seats.R} R</b>${seats.I ? html` – <b>${seats.I}</b> ind.` : ''} (${T.many})${cur ? html` ; ${seatGain(seats, cur)} par rapport aux ${cur.D}–${cur.R} actuels` : ''}.</p>`
      : html`<p class="gain">Expected <b>${seats.D} D</b> – <b>${seats.R} R</b>${seats.I ? html` – <b>${seats.I}</b> independent` : ''} ${unit}${cur ? html`; ${seatGain(seats, cur)} from today’s ${cur.D}–${cur.R}` : ''}.</p>`) : ''}
    ${o.range80D ? html`<p class="small faint" style="margin:4px 0 0">${L(`8 simulations sur 10 : de ${o.range80D[0]} à ${o.range80D[1]} ${T.many} démocrates.${pN >= 0.005 ? ` ${fmtProb(pN)} de chances qu’aucun parti n’atteigne la majorité.` : ''}`, `8 in 10 simulations: ${o.range80D[0]} to ${o.range80D[1]} Democratic ${unit}.${pN >= 0.005 ? ` ${fmtProb(pN)} chance neither party reaches a majority.` : ''}`)}</p>` : ''}
    ${market ? html`<p class="market">${L(`Marché de paris : ${fmtProb(market.pD)} D sur`, `Betting market: ${fmtProb(market.pD)} D on`)} <a href="${market.url}" target="_blank" rel="noopener noreferrer">Polymarket</a> ${L('(une vérification, pas une donnée du modèle)', '(a cross-check, not an input)')}</p>` : ''}
    ${hist.length >= 3 ? html`<div class="control-history"><span class="tiny faint">${L(`Chances des démocrates depuis le ${fmtDate(sum.history[0].t)}`, `Democrats’ chance since ${fmtDate(sum.history[0].t)}`)}</span>${raw(sparkline(hist.map((v) => v * 100), { width: 260, height: 34, color: cssVar('--dem'), label: L(`${name} : chances de contrôle des démocrates dans le temps`, `${label}: Democrats' chance of control over time`) }))}</div>` : ''}
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
  const T = TILE_FR[key];
  const name = L(T.name, label);
  const flipLine = t.flips.length
    ? html`${L('Changements de parti : ', 'Changed parties: ')}${[['D', 'Democrats', 'les démocrates'], ['R', 'Republicans', 'les républicains'], ['I', 'independents or others', 'les indépendants ou autres']].filter(([p]) => to(p)).map(([p, who, whoFr], i) => html`${i ? ', ' : ''}<b class="${p === 'D' ? 'd-text' : p === 'R' ? 'r-text' : ''}">${L(`${to(p)} vers ${whoFr}`, `${to(p)} to ${who}`)}</b>`)}.`
    : html`${L(`Aucun ${T.one} n’a changé de parti parmi les élections attribuées.`, `No ${unit} have changed parties among the called races.`)}`;
  let verdict;
  if (needs && t.seats.R >= needs.R) verdict = html`<b class="r-text">${L('Les républicains ont remporté le contrôle', 'Republicans have won control')}</b> ${L(`avec ${t.seats.R} ${T.many}${key === 'senate' ? ' (le vice-président départage une égalité à 50–50)' : ''}.`, `with ${t.seats.R} ${unit}${key === 'senate' ? ' (the vice president breaks a 50–50 tie)' : ''}.`)}`;
  else if (needs && t.seats.D >= needs.D) verdict = html`<b class="d-text">${L('Les démocrates ont remporté le contrôle', 'Democrats have won control')}</b> ${L(`avec ${t.seats.D} ${T.many}.`, `with ${t.seats.D} ${unit}.`)}`;
  else if (needs) verdict = lang() === 'fr' ? html`Pas encore de majorité : il en manque <b>${needs.D - t.seats.D}</b> aux démocrates et <b>${needs.R - t.seats.R}</b> aux républicains.` : html`No majority yet: Democrats need <b>${needs.D - t.seats.D}</b> more, Republicans <b>${needs.R - t.seats.R}</b>.`;
  else verdict = html`${L('Avant l’élection :', 'Before the election:')} ${t.current.D} D – ${t.current.R} R.`;
  const pending = [...t.runoff.map((r) => `${r.state}${r.office === 'house' ? `-${r.district === '00' ? 'AL' : parseInt(r.district, 10)}` : ''} ${L('(second tour)', '(runoff)')}`), ...t.uncalled.map((r) => `${r.state}${r.office === 'house' ? `-${r.district === '00' ? 'AL' : parseInt(r.district, 10)}` : ''}`)];
  const updated = racesMeta()?.resultsUpdated || racesMeta()?.updated;
  // The projection (scripts/update_races.py, after_count): called seats as they are, the
  // races still out from their counts and final forecasts.
  const proj = open ? controlData()?.[key]?.projection : null;
  const won = needs && (t.seats.D >= needs.D || t.seats.R >= needs.R);
  const pSeats = proj ? wholeSeats(proj, { D: total, R: 0 }) : null;
  return html`<div class="card control results-tile">
    <div class="row between"><div class="eyebrow">${L(`Résultats ${T.of}`, `${label} results`)}</div><span class="live-chip" title="${lang() === 'fr' ? `${updated ? `Lu lors de la dernière mise à jour, ${timeAgo(updated)}` : 'Lu sur Wikipédia à chaque mise à jour'}${stillCounting() ? ' ; relu toutes les 10 minutes jusqu’à ce que chaque élection soit attribuée' : ''}` : `${updated ? `Read at the last refresh, ${timeAgo(updated)}` : 'Read from Wikipedia at each refresh'}${stillCounting() ? '; re-read every 10 minutes until every race is called' : ''}`}">${L('En direct', 'Live')}</span></div>
    <div class="seat-bar">
      <div class="bar" role="img" aria-label="${L(`${name} : démocrates ${t.seats.D}${t.seats.I ? `, indépendants et autres ${t.seats.I}` : ''}, non attribués ${open}, républicains ${t.seats.R}`, `${label}: Democrats ${t.seats.D}${t.seats.I ? `, independents and others ${t.seats.I}` : ''}, not called ${open}, Republicans ${t.seats.R}`)}"><span style="flex:${t.seats.D}"></span>${t.seats.I ? html`<span class="i" style="flex:${t.seats.I}"></span>` : ''}${open ? html`<span class="n" style="flex:${open}"></span>` : ''}<span style="flex:${t.seats.R}"></span></div>
      ${needs && total ? html`<i class="maj" title="${L(`La moitié des ${T.many} : il en faut ${needs.D} aux démocrates pour le contrôle, ${needs.R} aux républicains`, `Half the ${unit}: Democrats need ${needs.D} for control, Republicans ${needs.R}`)}"></i>` : ''}
    </div>
    <div class="odds"><span><b class="d-text">${t.seats.D}</b>${L('Démocrates', 'Democrats')}</span>${t.seats.I ? html`<span style="text-align:center"><b>${t.seats.I}</b>${L('Ind. / autres', 'Ind. / other')}</span>` : ''}${open ? html`<span style="text-align:center"><b>${open}</b>${L('Non attribués', 'Not called')}</span>` : ''}<span style="text-align:right"><b class="r-text">${t.seats.R}</b>${L('Républicains', 'Republicans')}</span></div>
    <p class="gain">${verdict}</p>
    <p class="small faint" style="margin:4px 0 0">${L(`${t.called} élections attribuées sur ${t.up}${t.hold.D || t.hold.R ? `, plus les ${T.many} qui n’étaient pas en jeu cette année (${t.hold.D} D et ${t.hold.R} R)` : ''}${key === 'senate' ? ' ; les démocrates comptent les indépendants qui siègent avec eux' : ''}.`, `${t.called} of ${t.up} races called${t.hold.D || t.hold.R ? `, plus ${t.hold.D} D and ${t.hold.R} R ${unit} not up this year` : ''}${key === 'senate' ? '; Democrats include the independents who caucus with them' : ''}.`)} ${flipLine}</p>
    ${pSeats ? html`<p class="small" style="margin:8px 0 0">${lang() === 'fr'
      ? html`Projection finale : <b class="d-text">${pSeats.D} D</b> – <b class="r-text">${pSeats.R} R</b>${pSeats.I ? html` – <b>${pSeats.I}</b> autres` : ''} (8 sur 10 : de ${proj.range80D[0]} à ${proj.range80D[1]} ${T.many} démocrates)${needs && !won ? html` ; chances d’obtenir la majorité : <b class="d-text">D ${fmtProb(proj.pD)}</b>, <b class="r-text">R ${fmtProb(proj.pR)}</b>` : ''}.`
      : html`Projected final: <b class="d-text">${pSeats.D} D</b> – <b class="r-text">${pSeats.R} R</b>${pSeats.I ? html` – <b>${pSeats.I}</b> other` : ''} (8 in 10: ${proj.range80D[0]} to ${proj.range80D[1]} Democratic ${unit})${needs && !won ? html`; chance of a majority: <b class="d-text">D ${fmtProb(proj.pD)}</b>, <b class="r-text">R ${fmtProb(proj.pR)}</b>` : ''}.`}</p>
    <p class="tiny faint" style="margin:2px 0 0">${L('Chaque élection non attribuée compte selon sa projection à partir du dépouillement, ou selon sa dernière prévision quand aucun décompte n’est publié.', 'Each race still out counts by its projection from the count so far, or its final forecast where no count is posted.')}</p>` : ''}
    ${pending.length ? html`<p class="small faint" style="margin:4px 0 0">${t.runoff.length && !t.uncalled.length ? L('Second tour', 'Runoff') : L('Pas encore attribuées', 'Not called yet')}${L(' : ', ': ')}${pending.slice(0, 12).join(', ')}${pending.length > 12 ? L(` et ${pending.length - 12} autres`, ` and ${pending.length - 12} more`) : ''}.</p>` : ''}
  </div>`;
}

// Races with a count and no call yet, closest projection first.
function stillCountingList() {
  return mainRaces().map((r) => ({ r, lv: liveFc(r) })).filter((x) => x.lv)
    .sort((a, b) => a.lv.pLead - b.lv.pLead || a.r.id.localeCompare(b.r.id)).map((x) => x.r);
}

const chamberUp = (c) => (c.up === 'all' ? L('tous les sièges', 'all seats') : c.up === 'partial' ? L('une partie des sièges', 'some seats') : L('pas d’élection', 'no election'));

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
  const fr = lang() === 'fr';
  const mine = st
    ? (fr
      ? (afterElection() ? `Vos élections ${inState(st.abbr)} et leurs résultats de 2026, les élections que vous suivez et vos rappels.` : `Les élections de votre bulletin ${inState(st.abbr)}, les élections que vous suivez et vos rappels.`)
      : (afterElection() ? `Your races in ${st.name} and their 2026 results, the races you follow and your reminders.` : `The races on your ballot in ${st.name}, the races you follow and your reminders.`))
    : L('Les élections de votre bulletin, d’après votre adresse (elle reste dans ce navigateur).', 'The races on your ballot, from your address (it stays in this browser).');
  const quiz = fr
    ? (touched >= total
      ? `Vous avez répondu aux ${total} questions. Relisez-les, puis voyez quelles candidatures vous correspondent dans chaque élection de votre bulletin.`
      : `${touched > 0 ? `Vous avez répondu à ${touched} questions sur ${total} ; vous reprendrez où vous en étiez. ` : 'Répondez aux questions de « Mes opinions », puis comparez vos réponses avec les positions sourcées des candidats. '}Moins de 20 minutes. Vous pouvez vous arrêter à tout moment et revenir plus tard, mais vos correspondances risquent d’être imprécises tant que vous n’avez pas répondu à toutes les questions.`)
    : touched >= total
      ? `You’ve answered all ${total} questions. Review them, then see which candidates match you in each race on your ballot.`
      : `${touched > 0 ? `You’ve answered ${touched} of ${total} questions; this picks up where you left off. ` : 'Answer the My views questions, then compare your answers with the candidates’ sourced positions. '}Takes less than 20 minutes. You can stop at any time and come back later, but your matches may not be fully accurate until you’ve answered every question.`;
  return html`<section class="fr-start us-start">
    <button type="button" class="btn btn-primary fr-start-btn" aria-expanded="${String(readyOpen)}" aria-controls="us-start-choices">${icon.ballot()} ${L('Préparer mon vote', 'Get ready to vote')} ${icon.chevronDown()}</button>
    <div class="fr-start-choices" id="us-start-choices" ${raw(readyOpen ? '' : 'hidden')}>
      <a class="card fr-choice" href="#/elections">${icon.calendar()}<span><b>${L('Cliquez ici pour voir mes élections', 'Click here to view my elections')}</b><span class="small muted">${mine}</span></span>${icon.chevronRight()}</a>
      <a class="card fr-choice" href="#/views">${icon.user()}<span><b>${L('Cliquez ici pour m’aider à trouver le candidat qui me correspond', 'Click here to help find the best candidate for me')}</b><span class="small muted">${quiz}</span></span>${icon.chevronRight()}</a>
    </div>
  </section>`;
}

// A race in the results map's tooltip: the winner and margin, a runoff, the leader of a
// count still going, or nothing yet.
function tipResult(race) {
  const res = race.result;
  if (!res) return html`<span class="faint">${L('Pas encore de résultat', 'No result yet')}</span>`;
  const m = resultMarginStr(race);
  if (res.status === 'won') {
    const w = resultWinners(race);
    return html`<b>${icon.check()} ${w.map((c) => `${lastName(c.name)} (${c.party})`).join(', ')}${m ? `, ${m}` : ''}${res.flip ? L(' · bascule', ' · flip') : ''}</b>`;
  }
  if (res.status === 'runoff') return html`<b>${L('Second tour', 'Runoff')}</b>`;
  const lead = resultMargin(race);
  const lv = liveFc(race);
  return html`<b>${lead ? L(`${lastName(lead.a.name)} en tête, ${m}`, `${lastName(lead.a.name)} leads, ${m}`) : L('Dépouillement', 'Counting')}${lv ? L(` · ${lastName(lv.lead.name)} ${fmtProb(lv.pLead)} de chances de gagner`, ` · ${lastName(lv.lead.name)} ${fmtProb(lv.pLead)} to win`) : ''}</b>`;
}

function districtTip(f) {
  const race = districtRace(f);
  if (!race) return html`<div class="t-title">${f.properties.n || f.id}</div><div class="t-row"><span class="faint">${L('Aucune élection trouvée', 'No race found')}</span></div>`;
  const results = aligned() || mapView() === 'results';
  const f0 = fc(race);
  const row = results ? tipResult(race)
    : f0.open ? html`<b>${ratingL(f0.rating)}</b>` : html`<b>${lastName(f0.lead.name)} (${f0.lead.party}) ${fmtProb(f0.pLead)}</b>`;
  return html`<div class="t-title">${raceTitle(race)}</div>
    <div class="t-row"><span>${results ? L('Résultat', 'Result') : L('Prévision', 'Forecast')}</span>${row}</div>
    <div class="tiny faint" style="margin-top:6px">${aligned() ? L('Cliquez pour voir la personne élue et comparer vos opinions', 'Click to see who was elected and compare views') : L(`Cliquez pour voir l’élection${results ? ' · décomptes non officiels' : race.demo ? ' · prévision de démonstration' : ''}`, `Click to see the race${results ? ' · unofficial counts' : race.demo ? ' · demo forecast' : ''}`)}</div>`;
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
  return [n.R && `${n.R} R`, n.D && `${n.D} D`, n.other && L(`${n.other} autres`, `${n.other} other`), n.open && L(`${n.open} non attribués`, `${n.open} not called`)].filter(Boolean).join(', ');
}

// After the election the map shows who represents each state from January 2027: both
// senators (the called 2026 winner and the senator whose seat wasn't up), the governor,
// and the House delegation by party.
const aligned = () => resultsIn();
const PARTY_ONE = { D: 'Democrat', R: 'Republican', I: 'independent' };
const PARTY_MANY = { D: 'Democrats', R: 'Republicans', I: 'independents' };
const halves = (base, stripe) => `repeating-linear-gradient(45deg, ${base} 0 4px, ${stripe} 4px 8px)`;
function delegationColor(kind, pattern) {
  const dem = cssVar('--dem'), rep = cssVar('--rep'), ind = cssVar('--seat-other'), mid = cssVar('--neutral-mid');
  const pole = { D: dem, R: rep, I: ind };
  if (!kind) return cssVar('--not-up'); // D.C.: no senators
  if (kind === 'DD') return dem;
  if (kind === 'RR') return rep;
  if (kind === 'II') return ind;
  if (kind === 'DR') return cssVar('--split');
  if (kind === 'DI' || kind === 'RI') return pattern ? pattern(pole[kind[0]], ind, 4, 8) : halves(pole[kind[0]], ind);
  const known = kind.replace(/\?/g, '');
  return known && pattern ? pattern(pole[known[0]], mid, 4, 8) : mid; // a seat not decided yet
}
// In French the label counts seats ("Un siège démocrate, un siège républicain"), so it
// needs no gender agreement with the senators.
const SEAT_FR = { D: 'démocrate', R: 'républicain', I: 'indépendant' };
function delegationLabel(kind) {
  if (lang() === 'fr') {
    if (!kind) return 'Pas de sénateurs';
    if (kind.includes('?') && !(kind[0] === kind[1] && kind[0] !== '?')) return 'Un siège pas encore attribué';
    if (kind[0] === kind[1]) return `Deux sièges ${SEAT_FR[kind[0]]}s`;
    return `Un siège ${SEAT_FR[kind[0]]}, un siège ${SEAT_FR[kind[1]]}`;
  }
  if (!kind) return 'No senators';
  if (kind === 'DR') return 'One Democrat, one Republican';
  if (kind[0] === kind[1] && kind[0] !== '?') return `Two ${PARTY_MANY[kind[0]]}`;
  if (kind.includes('?')) return 'A seat not decided yet';
  return `One ${PARTY_ONE[kind[0]]}, one ${PARTY_ONE[kind[1]]}`;
}
const personLine = (p) => (p.status === 'elected' || p.status === 'holder'
  ? `${p.name} (${p.party === 'D' || p.party === 'R' ? p.party : 'I'})`
  : p.status === 'runoff' ? L('Second tour', 'Runoff') : L('Pas encore attribué', 'Not called yet'));
const seatNote = (p) => (p.status === 'elected' ? (p.flip ? L('victoire en 2026 · bascule', 'won 2026 · flip') : L('victoire en 2026', 'won 2026')) : p.status === 'holder' && p.up ? L(`en jeu en ${p.up}`, `up ${p.up}`) : '');
function alignedTooltip(f) {
  const st = f.id;
  const s = STATE_BY_ABBR[st];
  const d = delegation(st);
  const gov = governorOf(st);
  const tally = houseTally(st);
  return html`<div class="t-title">${stateName(st)}</div>
    <div class="t-row"><span>${L('Sénat des États-Unis', 'U.S. Senate')}</span><b>${delegationLabel(d.kind)}</b></div>
    ${d.seats.map((p) => html`<div class="t-row"><span>${personLine(p)}</span><span class="faint">${seatNote(p)}</span></div>`)}
    <div class="t-row" style="margin-top:4px"><span>${L('Gouverneur', 'Governor')}</span><b>${gov ? personLine(gov) : st === 'DC' ? L('Aucun (D.C. élit un maire)', 'None (D.C. elects a mayor)') : '—'}</b></div>
    <div class="t-row"><span>${L('Chambre des représentants', 'U.S. House')}</span><b>${st === 'DC' ? L('Un siège sans droit de vote', 'Delegate') : tally}</b></div>
    <div class="tiny faint" style="margin-top:6px">${L('À partir de janvier 2027 · cliquez pour les voir et comparer vos opinions', 'From January 2027 · click to see them and compare views')}</div>`;
}
function alignedFill(f, pattern) {
  if (mode === 'governor') {
    const g = governorOf(f.id);
    if (!g) return cssVar('--not-up'); // D.C.
    const p = g.status === 'elected' || g.status === 'holder' ? g.party : null;
    return p === 'D' ? cssVar('--dem') : p === 'R' ? cssVar('--rep') : p ? cssVar('--seat-other') : cssVar('--neutral-mid');
  }
  return delegationColor(delegation(f.id).kind, pattern);
}

function tooltip(f) {
  if (aligned()) return alignedTooltip(f);
  const st = f.id;
  const s = STATE_BY_ABBR[st];
  const { senate, governor } = statewideRaces(st);
  const results = mapView() === 'results';
  const line = (label, race) => {
    if (!race) return html`<div class="t-row"><span>${label}</span><span class="faint">${L('Pas d’élection', 'No race')}</span></div>`;
    if (results) return html`<div class="t-row"><span>${label}</span>${tipResult(race)}</div>`;
    const fc0 = fc(race);
    return html`<div class="t-row"><span>${label}</span><b>${lastName(fc0.lead.name)} (${fc0.lead.party}) ${fmtProb(fc0.pLead)}</b></div>`;
  };
  const nCd = getMapIndex()[st]?.cd || 0;
  const leg = legislatureChambers(st);
  return html`<div class="t-title">${stateName(st)}</div>
    ${line(L('Sénat des États-Unis', 'U.S. Senate'), senate)}
    ${line(L('Gouverneur', 'Governor'), governor)}
    <div class="t-row"><span>${L('Chambre des représentants', 'U.S. House')}</span><b>${results ? houseTally(st) : st === 'DC' ? L('Un siège sans droit de vote', 'Delegate') : L(`${nCd} circonscription${nCd === 1 ? '' : 's'}`, `${nCd} district${nCd === 1 ? '' : 's'}`)}</b></div>
    ${results ? '' : leg.map((c) => html`<div class="t-row"><span>${chamberName(c.name)}</span><b>${chamberUp(c)}</b></div>`)}
    <div class="tiny faint" style="margin-top:6px">${L(`Cliquez pour explorer${results ? ' · décomptes non officiels' : (senate && senate.demo) || (governor && governor.demo) ? ' · prévisions de démonstration' : ''}`, `Click to explore${results ? ' · unofficial counts' : (senate && senate.demo) || (governor && governor.demo) ? ' · demo forecasts' : ''}`)}</div>`;
}

function fillFor(f, pattern) {
  if (aligned() && mode !== 'house') return alignedFill(f, pattern);
  let race;
  if (mode === 'house') race = districtRace(f);
  else {
    const { senate, governor } = statewideRaces(f.id);
    race = mode === 'senate' ? senate : governor;
  }
  if (!race) return cssVar('--not-up');
  if (aligned() || mapView() === 'results') return resultFill(race.result, resultParty(race), pattern) || cssVar('--neutral-mid');
  return ratingColor(fc(race));
}

const mapHead = () => (mode === 'house' ? L('Choisissez une circonscription', 'Choose a district') : L('Choisissez un État', 'Choose a state'));

// Races decided by the fewest points, and the seats that changed parties.
const byMargin = (rs) => rs.map((r) => ({ r, m: resultMargin(r) })).filter((x) => x.m).sort((a, b) => a.m.pts - b.m.pts);
const OFFICE_ORDER = { senate: 0, governor: 1, house: 2 };

export const home = {
  live: true, // redrawn when new counts arrive (main.js)
  title: () => (resultsIn() ? L('Carte des résultats des élections de 2026', '2026 election results map') : L('Carte des élections de 2026', '2026 elections map')),
  async render() {
    if (!statesGeo) statesGeo = await fetchJSON('data/maps/states.json');
    const results = resultsIn();
    if (results) await loadHolders();
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
          ? (lang() === 'fr' ? html`<span class="label-pill"><span class="dots">•••</span> Résultats des élections de mi-mandat 2026${updated ? ` · mis à jour ${timeAgo(updated)}` : ''} <span class="dots">•••</span></span>
        <h1>Les <span class="grad-text">résultats de 2026</span>, État par État.</h1>
        <p class="lede">La carte montre qui représente chaque État à partir de janvier 2027 : ses deux sénateurs (en violet quand il y a un siège démocrate et un siège républicain), son gouverneur et le vainqueur de chaque circonscription de la Chambre. Une élection est attribuée dès que le tableau national des résultats de Wikipédia indique son vainqueur ; les décomptes restent non officiels jusqu’à leur certification par chaque État${stillCounting() && racesMeta()?.resultsUpdated ? ', et sont relus toutes les 10 minutes jusqu’à ce que chaque élection soit attribuée' : ', et se mettent à jour toutes les 8 heures'}. Survolez un État ou une circonscription pour un aperçu, puis cliquez ou appuyez dessus pour voir les élus, leur bilan et la proximité de leurs opinions avec les vôtres.</p>`
          : html`<span class="label-pill"><span class="dots">•••</span> 2026 midterm results${updated ? ` · updated ${timeAgo(updated)}` : ''} <span class="dots">•••</span></span>
        <h1>The <span class="grad-text">2026 results</span>, state by state.</h1>
        <p class="lede">The map shows who represents each state from January 2027: its two senators (purple where they are one Democrat and one Republican), its governor, and every House district’s winner. A race counts as called once Wikipedia’s national results table marks its winner; vote counts are unofficial until each state certifies them${stillCounting() && racesMeta()?.resultsUpdated ? ', and are re-read every 10 minutes until every race is called' : ', and refresh every 8 hours'}. Hover over a state or district to preview it, then click or tap it to see the people elected, their records and how their views compare with yours.</p>`)
          : lang() === 'fr' ? html`<span class="label-pill"><span class="dots">•••</span> Élections de mi-mandat 2026 · J-${days} <span class="dots">•••</span></span>
        <h1>Toutes les élections du <span class="grad-text">bulletin de 2026</span>, État par État.</h1>
        <p class="lede">Survolez un État ou une circonscription de la Chambre pour un aperçu, puis cliquez ou appuyez dessus pour explorer ses élections au Sénat, à la Chambre, au poste de gouverneur et aux assemblées de l’État.</p>`
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
          <div><div class="eyebrow">${results ? L('Qui représente chaque État', 'Who represents each state') : L('Carte interactive', 'Interactive map')}</div><h2 style="margin:4px 0 0" id="map-head">${mapHead()}</h2></div>
          <div class="row">
            <div class="seg" role="group" aria-label="${L('Élections sur la carte', 'Races on the map')}">
              ${MODES().map(([k, l]) => html`<button type="button" data-mode="${k}" aria-pressed="${String(mode === k)}">${l}</button>`)}
            </div>
            <label class="sr-only" for="state-jump">${L('Aller à un État', 'Jump to a state')}</label>
            <select id="state-jump" class="input" style="width:auto;min-height:46px">
              <option value="">${L('Aller à un État…', 'Jump to a state…')}</option>
              ${[...STATES].sort((a, b) => stateName(a.abbr).localeCompare(stateName(b.abbr), lang())).map((s) => html`<option value="${s.abbr}">${stateName(s.abbr)}</option>`)}
            </select>
          </div>
        </div>
        <div id="us-map" class="map-spot"></div>
        <div id="us-legend"></div>
      </section>
      ${counting.length ? html`<section>
        <div class="section-head"><div><div class="eyebrow">${L('Pas encore attribuées', 'Not called yet')}</div><h2 style="margin:4px 0 0">${L('Dépouillement en cours', 'Still being counted')}</h2></div><span class="small faint">${L(`${counting.length} élection${counting.length === 1 ? '' : 's'} avec un décompte, la plus serrée d’abord`, `${counting.length} race${counting.length === 1 ? '' : 's'} with a count, closest first`)}</span></div>
        <p class="small muted" style="margin:0 0 12px">${L('Chaque projection combine le décompte à ce stade et la dernière prévision. Ce n’est pas une attribution : une élection n’est attribuée qu’une fois son vainqueur indiqué dans le tableau national des résultats de Wikipédia.', 'Each projection blends the count so far with the final forecast. It is not a call: a race is called only once Wikipedia’s national results table marks its winner.')}</p>
        <div class="race-list">${counting.slice(0, 12).map((r) => raceRow(r))}</div>
      </section>` : ''}
      <section>
        <div class="section-head"><div><div class="eyebrow">${L('Sénat et gouverneurs', 'Senate and governor')}</div><h2 style="margin:4px 0 0">${results ? L('Les résultats les plus serrés', 'Closest statewide results') : L('Les élections les plus serrées', 'Closest statewide races')}</h2></div><a class="btn btn-sm" href="#/close">${L('Toutes les élections serrées', 'All close elections')}</a></div>
        <div class="race-list">${closest.map((r) => raceRow(r))}</div>
      </section>
      ${flips.length ? html`<section>
        <div class="section-head"><div><div class="eyebrow">${L('Élections attribuées', 'Called races')}</div><h2 style="margin:4px 0 0">${L('Les sièges qui ont changé de parti', 'Seats that changed parties')}</h2></div><span class="small faint">${L(`${flips.length} à ce jour`, `${flips.length} so far`)}</span></div>
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
      if (aligned() && mode === 'senate') {
        const kinds = [...new Set(STATES.map((s) => delegation(s.abbr).kind))];
        const order = ['DD', 'DR', 'RR', 'DI', 'RI', 'II'];
        const shown = order.filter((k) => kinds.includes(k)).concat(kinds.some((k) => k.includes('?')) ? ['?'] : []);
        legend.innerHTML = `<div class="map-legend">${shown.map((k) => `<span><i style="background:${k === '?' ? cssVar('--neutral-mid') : delegationColor(k)}"></i>${k === '?' ? L('Un siège pas encore attribué', 'A seat not decided yet') : delegationLabel(k)}</span>`).join('')}</div>`;
        return;
      }
      if (aligned() && mode === 'governor') {
        const ps = new Set(STATES.map((s) => governorOf(s.abbr)).filter((g) => g && (g.status === 'elected' || g.status === 'holder')).map((g) => (g.party === 'D' || g.party === 'R' ? g.party : 'I')));
        const sw = (c, l) => `<span><i style="background:${c}"></i>${l}</span>`;
        legend.innerHTML = `<div class="map-legend">${sw(cssVar('--dem'), L('Gouverneur : démocrate', 'Democratic governor'))}${sw(cssVar('--rep'), L('Gouverneur : républicain', 'Republican governor'))}${ps.has('I') ? sw(cssVar('--seat-other'), L('Gouverneur : indépendant', 'Independent governor')) : ''}</div>`;
        return;
      }
      const none = mode === 'house' ? '' : `<span><i style="background:${cssVar('--not-up')}"></i>${L(`Pas d’élection ${mode === 'senate' ? 'au Sénat' : 'de gouverneur'}`, `No ${mode === 'senate' ? 'Senate' : 'governor'} race`)}</span>`;
      if (aligned() || mapView() === 'results') {
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
      const results = aligned() || mapView() === 'results';
      map = want === 'districts'
        ? drawMap(el, districtsGeo, {
          fillFor, tooltipFor: districtTip,
          // After the election a district opens its state's House tab on that district: the
          // member elected, their positions and money; before it, the race.
          onSelect: (f) => {
            const [st, d] = f.id.split('-');
            location.hash = aligned() ? `#/state/${st}?level=federal&chamber=house&d=${d}` : `#/race/${f.id.replace('-', '-H-')}`;
          },
          borders: statesGeo, zoomable: true,
          ariaLabel: results ? L('Carte des 435 circonscriptions de la Chambre et de D.C., colorées selon les résultats de 2026 ; choisissez une circonscription pour voir son élection', 'Map of the 435 House districts and D.C., colored by the 2026 results; select a district to see its race') : L('Carte des 435 circonscriptions de la Chambre et de D.C. ; choisissez une circonscription pour voir son élection', 'Map of the 435 House districts and D.C.; select a district to see its race'),
          regionLabel: (f) => { const r = districtRace(f); return r ? raceTitle(r) : f.id; },
          maxHeight: 600,
        })
        : drawMap(el, statesGeo, {
          fillFor, tooltipFor: tooltip, onSelect: (f) => go(f.id),
          ariaLabel: aligned() ? L('Carte des États colorés selon le parti de leurs sénateurs ou de leur gouverneur à partir de janvier 2027 ; choisissez un État pour voir qui le représente', 'Map of U.S. states colored by the party of their senators or governor from January 2027; select a state to see who represents it') : L('Carte des États ; choisissez un État pour voir ses élections', 'Map of U.S. states; select a state to see its races'),
          regionLabel: (f) => (STATE_BY_ABBR[f.id] ? stateName(f.id) : f.id),
          maxHeight: 600,
        });
    };
    await draw();
    setLegend();
    root.querySelectorAll('[data-mode]').forEach((b) => b.addEventListener('click', async () => {
      mode = b.dataset.mode;
      root.querySelectorAll('[data-mode]').forEach((x) => x.setAttribute('aria-pressed', String(x === b)));
      const head = root.querySelector('#map-head');
      if (head) head.textContent = mapHead();
      await draw();
      setLegend();
    }));
    root.querySelectorAll('[data-view]').forEach((b) => b.addEventListener('click', () => {
      setMapView(b.dataset.view);
      root.querySelectorAll('[data-view]').forEach((x) => x.setAttribute('aria-pressed', String(x === b)));
      const eb = root.querySelector('.map-card .eyebrow');
      if (eb) eb.textContent = mapView() === 'results' ? L('Carte des résultats', 'Results map') : L('Carte de la dernière prévision', 'Final forecast map');
      map?.refill();
      setLegend();
    }));
    root.querySelector('#state-jump').addEventListener('change', (e) => e.target.value && go(e.target.value));
  },
};
