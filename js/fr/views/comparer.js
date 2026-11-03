// "Comparer avec mes opinions": every candidate with sourced positions, ranked by how
// closely they match the visitor's answers; a click opens the side-by-side comparison
// (js/fr/compare.js). The France counterpart of the U.S. match page.

import { html } from '../../util.js';
import { icon } from '../../icons.js';
import { L } from '../../i18n.js';
import { frStore } from '../store.js';
import { loadPres, loadPositions, candById, fmtPctFr } from '../data.js';
import { candPhoto, partyChip } from '../components.js';
import { rankFr, MIN_COMPARED } from '../match.js';
import { wireCompare, QUIZ_URL } from '../compare.js';

// The candidates with sourced positions who are still in the presidential data.
export const researchedCandidates = (pres, positions) => Object.keys(positions?.candidates || {})
  .map((id) => candById(pres, id)).filter((c) => c?.declared);

export const comparer = {
  title: () => L('Comparer avec mes opinions', 'Compare with my views'),
  async render() {
    const [pres, positions] = await Promise.all([loadPres(), loadPositions()]);
    const cands = researchedCandidates(pres, positions);
    const answered = frStore.answered();
    const crumbs = html`<nav class="crumbs"><a href="#/fr/elections">${L('Mes élections', 'My elections')}</a><span>/</span><span>${L('Comparer avec mes opinions', 'Compare with my views')}</span></nav>`;
    if (answered < MIN_COMPARED) {
      return html`<div class="wrap page" style="max-width:820px">${crumbs}
        <div class="empty">${icon.user()}<h3>${L('Répondez d’abord à quelques questions', 'Answer a few more questions first')}</h3>
          <p>${L(`Vous avez répondu à ${answered} question${answered > 1 ? 's' : ''} de Mes opinions. Il en faut au moins ${MIN_COMPARED} pour une comparaison honnête.`, `You’ve answered ${answered} question${answered === 1 ? '' : 's'} in My views. At least ${MIN_COMPARED} are needed for a fair comparison.`)}</p>
          <a class="btn btn-primary" href="${QUIZ_URL}">${L('Répondre au questionnaire', 'Answer the questionnaire')}</a></div></div>`;
    }
    const ranked = rankFr(frStore.get().answers, cands, positions.candidates);
    return html`<div class="wrap page stack" style="max-width:920px">
      ${crumbs}
      <div><div class="eyebrow">${L('Présidentielle 2027 · classement des affinités', '2027 presidential election · similarity ranking')}</div>
        <h1 style="font-size:clamp(28px,3.6vw,42px);margin:6px 0 8px">${L('Quel candidat vous correspond ?', 'Which candidate matches you?')}</h1>
        <p class="muted" style="margin:0">${L(
          `D’après vos ${answered} réponses à Mes opinions. Cliquez sur un candidat pour voir vos points d’accord (à gauche), vos désaccords (à droite) et les questions sans position connue (en bas).`,
          `Using your ${answered} answers in My views. Click a candidate to see where you agree (left), where you differ (right) and the questions with no known position (bottom).`,
        )}</p></div>
      <div class="match-list">${ranked.map((row, i) => html`<button type="button" class="match-row" data-compare="${row.cand.id}">
        <span class="rank">${i + 1}</span>
        <span style="min-width:0"><span class="row" style="gap:8px">${candPhoto(row.cand, { size: 30 })}<b>${row.cand.name}</b>${partyChip(row.cand)}</span><span class="tiny faint">${L(`comparé sur ${row.compared} de vos ${row.userAnswered} réponses`, `compared on ${row.compared} of your ${row.userAnswered} answers`)}</span></span>
        <span class="meter"><span style="width:${row.score ?? 0}%"></span></span>
        <span class="pct">${row.score == null ? '—' : fmtPctFr(row.score, 0)}</span>
      </button>`)}</div>
      <p class="small faint" style="margin:0">${L(
        `Calcul : chaque question compte 100 % pour des réponses identiques et 0 % pour des positions opposées, en moyenne sur les questions où la position du candidat est sourcée. Sans ${MIN_COMPARED} questions en commun, pas de pourcentage. Les positions viennent des programmes et déclarations des candidats, jamais devinées.`,
        `How the score works: each question scores 100% for identical answers down to 0% for opposite positions, averaged over the questions where the candidate’s position is sourced. Without ${MIN_COMPARED} shared questions, no percentage. Positions come from the candidates’ programs and statements, never guessed.`,
      )}</p>
      <div class="row"><a class="btn btn-sm" href="${QUIZ_URL}">${L('Modifier mes réponses', 'Change my answers')}</a><a class="btn btn-sm btn-ghost" href="#/fr/presidentielle?tour=c">${L('Tous les candidats', 'All the candidates')}</a></div>
    </div>`;
  },
  async mount(root) {
    const [pres, positions] = await Promise.all([loadPres(), loadPositions()]);
    return wireCompare(root, researchedCandidates(pres, positions), positions?.candidates);
  },
};
