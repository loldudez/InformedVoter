// "My elections": the races on the visitor's ballot, matching against their views,
// and the similarities / differences / unclear breakdown for each candidate.

import { html, fmtPct, fmtProb, fmtDate, fmtDR, fmtInt, pctSign } from '../util.js';
import { icon } from '../icons.js';
import { store } from '../store.js';
import { STATE_BY_ABBR, legislatureChambers, electionDateLabel, chamberOf, chamberName, inState } from '../data/states.js';
import { L, lang } from '../i18n.js';
import { questionsForLevel } from '../data/questions.js';
import { fc, statewideRaces, officeRaces, getRace, legislativeRaces, ensureRace, raceTitle, officeLabel, positionsOf, isDemo, afterElection, resultRows, rowShare, ratingL, certSentence, certifiedIn } from '../data/world.js';
import { rank, MIN_COMPARED } from '../model/match.js';
import { howToVote } from '../components/vote.js';
import { reminderButton } from '../components/reminders.js';
import { PARTY_NAME, partyClass, heartBtn, starBtn, demoChip, dataChip, lastName, ratingChip, candBadge, photoCredits, resultChip, raceColors, awaitingResult } from '../components/race.js';
import { futureElections } from './upcoming.js';
import { compareOverlay } from '../components/compare.js';

// The "Future elections for <year>" disclosures the visitor has open, kept across the
// redraws while votes are counted (the view is `live`).
const openYears = new Set();

async function ballotFor(ad) {
  const st = ad.state;
  const s = STATE_BY_ABBR[st];
  const items = [];
  const { senate, governor } = statewideRaces(st);
  if (senate) items.push({ race: senate });
  if (governor) items.push({ race: governor });
  // Attorney general, secretary of state, lieutenant governor, treasurer, auditor.
  for (const race of officeRaces(st)) items.push({ race });
  const cd = st === 'DC' ? '98' : ad.cd;
  const house = cd && getRace(`${st}-H-${cd}`);
  if (house) items.push({ race: house });
  for (const ch of legislatureChambers(st)) {
    const code = ch.layer === 'sldu' ? ad.sldu : ad.sldl;
    if (!code) continue;
    if (ch.up === 'none') { items.push({ none: chamberOf(st, ch.name), why: L('Aucun siège de cette chambre n’est en jeu en 2026.', `${ch.name} seats are not on the ballot in 2026.`) }); continue; }
    const data = await legislativeRaces(st, ch.key);
    const race = data?.races.get(code);
    if (race) items.push({ race });
    else items.push({ none: L(`${chamberName(ch.name)}, circonscription ${code.replace(/^0+/, '')}`, `${ch.name}, District ${code.replace(/^0+/, '')}`), why: L('Le siège de votre circonscription n’est pas en jeu cette année (mandats échelonnés).', 'Your district’s seat is not up this year (staggered terms).') });
  }
  return items;
}

function raceCard(race) {
  const f = fc(race);
  const colors = raceColors(race);
  const mine = store.get().electionAnswers[race.id];
  const answered = store.answered();
  const id = encodeURIComponent(race.id);
  const res = race.result;
  // With a count in, candidates in its order with their shares. After Election Day
  // without one, the winner (if called) first and no percentages, since the forecast's
  // or the polls' would read as results. Before it, the forecast's order and shares.
  const awaiting = awaitingResult(race);
  const rows = resultRows(race).filter((r) => r.cand);
  const byRow = new Map(rows.map((r) => [r.cand.id, r]));
  const winners = new Set(res?.winners || []), adv = new Set(res?.advance || []);
  const ahead = (c) => (winners.has(c.id) || adv.has(c.id) ? 1 : 0);
  const cands = rows.length ? [...rows.map((r) => f.cands.find((c) => c.id === r.cand.id) || r.cand), ...f.cands.filter((c) => !byRow.has(c.id))]
    : res ? [...f.cands].sort((a, b) => ahead(b) - ahead(a)) : f.cands;
  const office = f.kind === 'office';
  const rated = f.rating && f.rating !== 'Not rated';
  const s = STATE_BY_ABBR[race.state];
  const wonBy = (c) => (byRow.has(c.id) ? byRow.get(c.id).won : winners.has(c.id));
  const sub = (c) => {
    const r = byRow.get(c.id);
    if (r || res || awaiting) {
      const toRunoff = r ? r.advance : adv.has(c.id);
      return html`${wonBy(c) ? html`<span class="win-mark">${icon.check()} ${L('Victoire', 'Winner')}</span> · ` : toRunoff ? L('Au second tour · ', 'To the runoff · ') : ''}${PARTY_NAME[c.party] || c.party}${c.incumbent && office ? L(' · en poste', ' · incumbent') : ''}${r?.votes != null ? L(` · ${fmtInt(r.votes)} voix`, ` · ${fmtInt(r.votes)} votes`) : ''}`;
    }
    return html`${PARTY_NAME[c.party] || c.party}${c.incumbent && office ? L(' · en poste', ' · incumbent') : ''}${f.open ? '' : L(` · ${fmtProb(c.win)} de chances de gagner`, ` · ${fmtProb(c.win)} to win`)}`;
  };
  const share = (c) => {
    const r = byRow.get(c.id);
    if (r) return rowShare(r);
    return rows.length || res || awaiting ? null : c.share;
  };
  const link = res ? L('Tous les résultats', 'Full results') : office || f.open ? L('Détails de l’élection', 'Race details') : awaiting ? L('Page de l’élection', 'Race page') : L('Prévision complète', 'Full forecast');
  const pending = !rows.length && (res || awaiting)
    ? (res?.status === 'won' ? L('Attribuée ; le décompte n’est pas encore publié.', 'Called; the vote count isn’t posted yet.') : res?.status === 'runoff' ? L('Vers un second tour ; le décompte n’est pas encore publié.', 'Headed to a runoff; the vote count isn’t posted yet.') : res ? L('Dépouillement en cours.', 'Votes are being counted.') : L('Pas encore de résultat.', 'No result yet.'))
    : '';
  const fr = lang() === 'fr';
  const seeForecast = L('La dernière prévision figure sur la page de l’élection.', 'The final forecast is on the race’s page.');
  return html`<article class="card stack">
    <div class="row between">
      <div><div class="eyebrow">${office ? L(`À l’échelle de l’État · ${officeLabel(race)}`, `Statewide · ${officeLabel(race)}`) : officeLabel(race)}</div><h3 style="margin:2px 0 0;font-size:19px">${raceTitle(race)}</h3></div>
      <div class="row">${dataChip(race)}${res || awaiting ? resultChip(race) : !office || rated ? ratingChip(f) : ''}${starBtn(race.id, { small: true })}</div>
    </div>
    ${f.kind === 'field' ? html`<p class="small muted" style="margin:0">${L('Pas de prévision pour les élections aux assemblées des États.', 'No forecast for state legislative races.')} ${f.cands.length ? '' : L('Wikipédia ne liste pas encore les candidatures de cette circonscription. ', 'Wikipedia doesn’t list this district’s candidates yet. ')}${f.dr != null ? L(`La circonscription a voté ${fmtDR(f.dr)} à la présidentielle de 2024.`, `The district voted ${fmtDR(f.dr)} for president in 2024.`) : ''}</p>` : ''}
    ${office ? html`<p class="small muted" style="margin:0">${fr
      ? `Pas de prévision pour les postes de l’État sous le gouverneur${rated ? ` ; le Crystal Ball de Sabato l’a coté ${ratingL(f.rating)}` : ''}.${f.dr != null ? ` L’État a voté ${fmtDR(f.dr)} à la présidentielle de 2024.` : ''}${rows.length ? ` ${certSentence(race)}` : pending ? ` ${pending}` : f.poll ? ' Les pourcentages sont la moyenne des sondages.' : ''}`
      : `No forecast for statewide offices below governor${rated ? `; Sabato’s Crystal Ball rated it ${f.rating}` : ''}.${f.dr != null ? ` ${s.name} voted ${fmtDR(f.dr)} for president in 2024.` : ''}${rows.length ? ` ${certSentence(race)}` : pending ? ` ${pending}` : f.poll ? ' Percentages are the polling average.' : ''}`}</p>` : ''}
    ${f.open && f.kind === 'open-primary' ? html`<p class="small muted" style="margin:0">${fr
      ? `Primaire ouverte : les ${f.cands.length} candidatures ${res || awaiting ? 'partageaient' : 'partagent'} un seul bulletin. Une majorité absolue suffit pour gagner dès le premier tour ; sinon, les deux premiers s’affrontent au second tour${race.runoff ? ` le ${fmtDate(race.runoff + 'T12:00:00')}` : ''}. ${rows.length ? 'Les pourcentages sont le décompte non officiel.' : pending || 'Les pourcentages viennent du dernier sondage publié.'}`
      : `Open primary: all ${f.cands.length} candidates share${res || awaiting ? 'd' : ''} one ballot. A majority wins outright; otherwise the top two meet in a runoff${race.runoff ? ` on ${fmtDate(race.runoff + 'T12:00:00')}` : ''}. ${rows.length ? 'Percentages are the unofficial count.' : pending || 'Percentages are from the latest published poll.'}`}</p>` : ''}
    ${rows.length && !office && !f.open ? html`<p class="small muted" style="margin:0">${fr
      ? `Décompte non officiel${res.status === 'won' ? ' ; l’élection est attribuée' : res.status === 'runoff' ? ' ; l’élection va au second tour' : ' ; pas encore attribuée'}.`
      : `Unofficial count${res.status === 'won' ? '; the race has been called' : res.status === 'runoff' ? '; the race goes to a runoff' : '; not called yet'}.`} ${seeForecast}</p>` : ''}
    ${pending && !office && !f.open ? html`<p class="small muted" style="margin:0">${pending} ${seeForecast}</p>` : ''}
    <div class="grid grid-2" style="gap:10px">${cands.map((c) => html`<div class="compact-cand ${partyClass(c.party)}${wonBy(c) ? ' winner' : ''}">
      ${candBadge(c, colors[c.id])}
      <div style="min-width:0"><div class="nm">${c.name}</div><div class="tiny faint">${sub(c)}</div></div>
      ${share(c) != null ? html`<div class="sh" style="color:${colors[c.id]};font-size:18px">${fmtPct(share(c), rows.length ? 1 : 0)}</div>` : ''}
      ${heartBtn(c.id, c.name, { small: true })}
    </div>`)}</div>
    ${!isDemo(race) && !race.research ? html`<p class="small muted" style="margin:0">${icon.info()} ${fr
      ? (f.kind === 'field'
        ? html`Ces candidatures viennent de la page Wikipédia 2026 de cette chambre ; leurs positions n’ont pas été recherchées, la comparaison n’est donc pas disponible. <a href="#/race/${id}">Voir l’élection</a>.`
        : office
          ? html`${race.candidates.some((c) => Object.keys(c.positions || {}).length) ? 'Les positions de certaines de ces candidatures sont recherchées, mais pas encore toutes' : 'Les positions de ces candidatures n’ont pas encore été recherchées'} : la comparaison n’est donc pas disponible pour cette élection. <a href="#/race/${id}">Voir les candidatures et les résultats</a>.`
          : html`Les candidatures, les cotes, les sondages et les fonds levés sont à jour, mais les positions de chaque candidature n’ont pas encore toutes été recherchées : la comparaison n’est donc pas disponible pour cette élection. <a href="#/race/${id}">Voir ${res ? 'les résultats' : awaiting ? 'l’élection' : 'la prévision complète'}</a>.`)
      : f.kind === 'field'
      ? html`The candidates here come from Wikipedia’s 2026 page for this chamber; their issue positions haven’t been researched, so matching isn’t available. <a href="#/race/${id}">See the race</a>.`
      : office
        ? html`${race.candidates.some((c) => Object.keys(c.positions || {}).length) ? 'Some of these candidates’ positions are researched, but not every candidate’s yet' : 'These candidates’ issue positions haven’t been researched yet'}, so matching isn’t available for this race. <a href="#/race/${id}">See the candidates and results</a>.`
        : html`Candidates, ratings, polls and money here are live, but not every candidate’s issue positions have been researched yet, so matching isn’t available for this race. <a href="#/race/${id}">See the ${res ? 'results' : awaiting ? 'race' : 'full forecast'}</a>.`}</p>` : html`<div class="row">
      ${answered >= MIN_COMPARED
        ? html`<a class="btn btn-sm btn-primary" href="#/elections/${id}/match?mode=profile">${icon.user()} ${L('Comparer avec mes opinions', 'Match with My views')}</a>`
        : html`<a class="btn btn-sm" href="#/views" title="${L(`Répondez d’abord à au moins ${MIN_COMPARED} questions`, `Answer at least ${MIN_COMPARED} questions first`)}">${icon.user()} ${L('Répondre d’abord au questionnaire', 'Answer My views first')}</a>`}
      <a class="btn btn-sm" href="#/elections/${id}/quiz">${L('De nouvelles opinions pour cette élection', 'New political views for this election')}</a>
      ${mine && store.answered(mine) ? html`<a class="btn btn-sm btn-ghost" href="#/elections/${id}/match?mode=election">${L('Mes résultats pour cette élection', 'My results for this election')}</a>` : ''}
      <a class="btn btn-sm btn-ghost" href="#/race/${id}">${link}</a>
    </div>`}
  </article>`;
}

export const elections = {
  live: true, // redrawn when new counts arrive (main.js)
  title: () => L('Mes élections', 'My elections'),
  rerenderOn: ['reminders'],
  async render() {
    const ad = store.get().address;
    if (!ad || !ad.state) {
      return html`<div class="wrap page" style="max-width:860px">
        <div class="eyebrow">${L('Mes élections', 'My elections')}</div><h1>${L('Votre bulletin, d’après votre adresse', 'Your ballot, from your address')}</h1>
        <div class="empty">${icon.pin()}<h3>${L('Ajoutez votre adresse pour voir vos élections', 'Add your address to see your elections')}</h3><p>${L('Nous utilisons le géocodeur du Census Bureau américain pour trouver vos circonscriptions exactes. Votre adresse reste dans ce navigateur.', 'We use the U.S. Census Bureau’s geocoder to find your exact districts. Your address stays in this browser.')}</p><a class="btn btn-primary" href="#/profile?tab=location">${L('Ajouter mon adresse', 'Add my address')}</a></div>
      </div>`;
    }
    const items = await ballotFor(ad);
    const future = await futureElections(ad, openYears);
    const s = STATE_BY_ABBR[ad.state];
    const over = afterElection();
    // A runoff reminder only for a race of the visitor's that is going to one (or, before
    // the results, could), and only while the date is ahead.
    const today = new Date().toISOString().slice(0, 10);
    const runoff = items.map((it) => it.race).filter((r) => r?.runoff && r.runoff >= today && (!r.result || r.result.status === 'runoff')).map((r) => r.runoff)[0];
    return html`<div class="wrap page stack-lg" style="max-width:1000px">
      <div class="row between" style="align-items:flex-end">
        <div>
          <div class="eyebrow">${L('Mes élections', 'My elections')} · ${electionDateLabel()}</div>
          <h1 style="margin:6px 0 8px">${over ? L('Vos élections de 2026 et leurs résultats', 'Your 2026 races and results') : L('Ce qui figure sur votre bulletin', 'What’s on your ballot')}</h1>
          <p class="muted" style="margin:0">${icon.pin()} ${ad.matched} · <a href="#/profile?tab=location">${L('Modifier', 'Change')}</a></p>
        </div>
        <div class="row">${over ? '' : reminderButton({ id: 'us:general-2026', name: L('Jour du scrutin, 3 novembre 2026', 'Election Day, November 3, 2026'), date: '2026-11-03', section: 'us' })}
          ${runoff ? reminderButton({ id: `us:runoff-${ad.state}-${runoff}`, name: L(`Second tour ${inState(ad.state)}`, `${s.name} runoff`), date: runoff, section: 'us' }) : ''}</div>
      </div>
      ${over ? html`<div class="notice">${icon.info()}<div>${certifiedIn(s.abbr) ? L(`Résultats certifiés par l’État le ${fmtDate(certifiedIn(s.abbr).date)}. `, `${s.name} certified its results on ${fmtDate(certifiedIn(s.abbr).date)}. `) : ''}${L(`${certifiedIn(s.abbr) ? '' : 'Les résultats restent non officiels jusqu’à leur certification par l’État. '}Une élection affiche un vainqueur dès que le tableau national des résultats de Wikipédia en indique un ; la page de chaque élection donne le décompte complet, sa source et la dernière prévision. Cliquez sur une élection ci-dessous pour voir ses candidatures, leurs positions et les résultats.`, `${certifiedIn(s.abbr) ? '' : `Results are unofficial until ${s.name} certifies them. `}A race shows a winner once Wikipedia’s national results table marks one; each race’s page has the full count, its source and the final forecast. Click a race below for its candidates, where they stand and the results.`)}</div></div>` : ''}
      ${isDemo(items.find((x) => x.race)?.race) ? html`<div class="notice warn">${icon.info()}<div>${lang() === 'fr' ? html`Les postes et circonscriptions ci-dessous sont vos vraies élections de 2026. Les candidatures, prévisions et positions sont des <b>données de démonstration</b> tant que les vraies données ne sont pas branchées. Vérifiez toujours votre bulletin type auprès du bureau électoral de l’État.` : html`The offices and districts below are your real 2026 races. The candidates, forecasts and positions are <b>demo data</b> until real candidate data is connected. Always confirm your sample ballot with ${s.name}’s election office.`}</div></div>` : ''}
      <div class="stack">${items.map((it) => (it.race ? raceCard(it.race) : html`<div class="card tight"><div class="row between"><b>${it.none}</b><span class="chip">${L('Pas d’élection cette année', 'No election this year')}</span></div><p class="small muted" style="margin:6px 0 0">${it.why}</p></div>`))}</div>
      ${future.html}
      ${howToVote(ad.state)}
      ${photoCredits([...items.flatMap((it) => (it.race ? fc(it.race).cands : [])), ...future.people])}
    </div>`;
  },
  mount(root) {
    root.querySelectorAll('details.future-year').forEach((d) => d.addEventListener('toggle', () => {
      const y = Number(d.dataset.year);
      if (d.open) openYears.add(y); else openYears.delete(y);
    }));
    return null;
  },
};

// Ranking + three-panel breakdown --------------------------------------------------

// The three-panel breakdown (js/components/compare.js), for a candidate in a race.
function overlay(row, race) {
  const c = row.cand;
  return compareOverlay(row, c, {
    color: raceColors(race)[c.id],
    sub: `${PARTY_NAME[c.party] || c.party}${isDemo(c) ? L(' · démo', ' · demo') : ''}`,
    heart: heartBtn(c.id, c.name),
  });
}

export const match = {
  title: () => L('Comparaison des candidats', 'Candidate match'),
  async render(ctx) {
    const race = await ensureRace(decodeURIComponent(ctx.params[0]));
    if (!race) return html`<div class="wrap page"><p>${L('Élection introuvable.', 'Race not found.')} <a href="#/elections">${L('Retour à mes élections', 'Back to my elections')}</a></p></div>`;
    const mode = ctx.query.mode === 'election' ? 'election' : 'profile';
    const answers = mode === 'election' ? store.get().electionAnswers[race.id] || {} : store.get().answers;
    const qids = questionsForLevel(race.level).map((q) => q.id);
    const answeredHere = qids.filter((id) => answers[id] != null && answers[id] !== 'skip').length;
    const id = encodeURIComponent(race.id);
    if (answeredHere < MIN_COMPARED) {
      return html`<div class="wrap page" style="max-width:820px"><nav class="crumbs"><a href="#/elections">${L('Mes élections', 'My elections')}</a><span>/</span><span>${raceTitle(race)}</span></nav>
        <div class="empty">${icon.user()}<h3>${L('Répondez d’abord à quelques questions de plus', 'Answer a few more questions first')}</h3><p>${L(`Vous avez répondu à ${answeredHere} question${answeredHere > 1 ? 's' : ''} qui ${answeredHere > 1 ? 'concernent' : 'concerne'} cette élection. Il en faut au moins ${MIN_COMPARED} pour une comparaison équitable.`, `You’ve answered ${answeredHere} question${answeredHere === 1 ? '' : 's'} that apply to this race. At least ${MIN_COMPARED} are needed for a fair comparison.`)}</p>
        <a class="btn btn-primary" href="${mode === 'election' ? `#/elections/${id}/quiz` : '#/views'}">${L('Répondre aux questions', 'Answer questions')}</a></div></div>`;
    }
    const ranked = rank(answers, fc(race).cands, positionsOf, qids);
    const colors = raceColors(race);
    return html`<div class="wrap page stack" style="max-width:920px">
      <nav class="crumbs"><a href="#/elections">${L('Mes élections', 'My elections')}</a><span>/</span><span>${raceTitle(race)}</span></nav>
      <div><div class="eyebrow">${L('Classement par proximité', 'Similarity ranking')}</div><h1 style="font-size:clamp(28px,3.6vw,42px);margin:6px 0 8px">${L(`${raceTitle(race)} : qui vous correspond ?`, `Who matches you in ${raceTitle(race)}?`)}</h1>
        <p class="muted">${L(`D’après ${mode === 'election' ? 'les opinions données pour cette élection' : 'vos opinions enregistrées'} (${answeredHere} réponses). Cliquez sur une candidature pour voir vos accords, vos différences et ce qui reste incertain.`, `Using ${mode === 'election' ? 'the views you gave for this election' : 'your saved My views'} (${answeredHere} answers). Click a candidate to see where you agree, where you differ, and what’s unclear.`)}</p></div>
      ${isDemo(race) ? html`<div class="notice warn">${icon.info()}<div>${lang() === 'fr' ? html`Ces candidatures et leurs positions sont des <b>données de démonstration</b> : ce classement montre seulement comment fonctionne la comparaison.` : html`These candidates and their positions are <b>demo data</b>, so this ranking only shows how matching works.`}</div></div>` : ''}
      <div class="match-list">${ranked.map((row, i) => html`<button type="button" class="match-row" data-cand="${row.cand.id}">
        <span class="rank">${i + 1}</span>
        <span style="min-width:0"><span class="row" style="gap:8px">${candBadge(row.cand, colors[row.cand.id], 'width:30px;height:30px;font-size:11px;border-radius:8px')}<b>${row.cand.name}</b></span><span class="tiny faint">${PARTY_NAME[row.cand.party] || row.cand.party} · ${L(`${row.compared} sujets comparés sur ${row.userAnswered}`, `compared on ${row.compared} of ${row.userAnswered} issues`)}</span></span>
        <span class="meter"><span style="width:${row.score ?? 0}%"></span></span>
        <span class="pct">${row.score == null ? '—' : `${row.score}${pctSign()}`}</span>
      </button>`)}</div>
      <p class="small faint">${L(`Comment le score est calculé : chaque sujet vaut 100 % pour des réponses identiques et 0 % pour des positions extrêmes opposées, en moyenne sur les sujets où la position de la candidature est documentée. Il faut au moins ${MIN_COMPARED} positions documentées pour obtenir un score.`, `How the score works: each issue scores 100% for identical answers down to 0% for opposite extremes, averaged over issues where the candidate’s position is documented. A candidate needs at least ${MIN_COMPARED} documented positions to get a score.`)}</p>
      <div class="row"><a class="btn btn-sm" href="#/elections/${id}/quiz">${L('Répondre autrement pour cette élection', 'Answer differently for this election')}</a><a class="btn btn-sm btn-ghost" href="#/race/${id}">${race.result ? L('Tous les résultats', 'Full results') : race.format === 'office' || fc(race).open ? L('Détails de l’élection', 'Race details') : L('Prévision complète', 'Full forecast')}</a></div>
      ${photoCredits(ranked.map((row) => row.cand))}
    </div>`;
  },
  async mount(root, ctx) {
    const race = await ensureRace(decodeURIComponent(ctx.params[0]));
    if (!race) return;
    const mode = ctx.query.mode === 'election' ? 'election' : 'profile';
    const answers = mode === 'election' ? store.get().electionAnswers[race.id] || {} : store.get().answers;
    const qids = questionsForLevel(race.level).map((q) => q.id);
    const ranked = rank(answers, fc(race).cands, positionsOf, qids);
    const slot = document.getElementById('overlay-root');
    let lastFocus = null;
    const close = () => {
      slot.innerHTML = '';
      document.body.style.overflow = '';
      document.removeEventListener('keydown', onKey);
      lastFocus?.focus();
    };
    const onKey = (e) => { if (e.key === 'Escape') close(); };
    root.querySelectorAll('[data-cand]').forEach((b) => b.addEventListener('click', () => {
      const row = ranked.find((r) => r.cand.id === b.dataset.cand);
      lastFocus = b;
      slot.innerHTML = String(overlay(row, race));
      document.body.style.overflow = 'hidden';
      document.addEventListener('keydown', onKey);
      const ov = slot.querySelector('.overlay');
      ov.addEventListener('click', (e) => { if (e.target === ov || e.target.closest('[data-close]')) close(); });
      slot.querySelector('[data-close]').focus();
    }));
    return close;
  },
};

// Profile -> Donations ---------------------------------------------------------------

// The campaign's own site, plus the processors campaigns use for their official
// donate pages (ActBlue, WinRed, Anedot). Anything else is refused.
const PROCESSORS = ['secure.actblue.com', 'secure.winred.com', 'secure.anedot.com'];
export function verifiedDonateUrl(c) {
  if (!c.donateUrl || !c.officialSite) return null;
  try {
    const u = new URL(c.donateUrl), site = new URL(c.officialSite);
    if (u.protocol !== 'https:') return null;
    const official = site.hostname.replace(/^www\./, '');
    const host = u.hostname;
    if (host === official || host.endsWith(`.${official}`) || PROCESSORS.includes(host)) return u.href;
  } catch { /* malformed */ }
  return null;
}
