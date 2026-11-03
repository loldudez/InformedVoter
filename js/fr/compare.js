// "Comparer avec mes opinions": the visitor's answers beside one candidate's sourced
// positions, laid out as in the U.S. section (js/views/elections.js): where they agree
// on the left, where they differ on the right, the candidate and the score in the
// middle, and the questions with no known position along the bottom.

import { html } from '../util.js';
import { icon } from '../icons.js';
import { L } from '../i18n.js';
import { frStore } from './store.js';
import { fmtPctFr, fmtSourceDate } from './data.js';
import { candPhoto, partyChip, sourceLink } from './components.js';
import { qText, answerLabel } from './questions.js';
import { compareFr, MIN_COMPARED } from './match.js';

export const QUIZ_URL = '#/fr/profil/opinions';

const answeredValue = (v) => v != null && v !== 'skip';

// A position: the question, the stance, the quote (or why there is none) and the source.
export function positionItem(q, pos, user) {
  const s = pos.source;
  return html`<div class="evidence fr-pos">
    <div class="q">${q.n}. ${qText(q)}</div>
    <div class="row" style="gap:6px;margin:2px 0 6px">
      <span class="answer-tag fr-stance">${answerLabel(q, pos.stance)}</span>
      ${answeredValue(user) ? html`<span class="tiny faint">${L('Vous :', 'You:')} ${answerLabel(q, user)}</span>` : ''}
    </div>
    ${pos.quote
      ? html`<div class="quote" lang="fr">« ${pos.quote} »</div>`
      : html`<div class="small muted">${L('Résumé de presse : la source décrit la proposition sans citer le candidat.', 'Press summary: the source describes the proposal without quoting the candidate.')}</div>`}
    <div class="tiny faint" style="margin-top:4px"><span lang="fr">${s.title}</span>${s.date ? ` · ${fmtSourceDate(s.date)}` : ''} ${sourceLink(s.url)}</div>
  </div>`;
}

export function compareOverlay(c, positions) {
  const res = compareFr(frStore.get().answers, positions || {});
  const short = c.short || c.name;
  const status = !res.userAnswered
    ? L('Vous n’avez pas encore répondu au questionnaire.', 'You haven’t answered the questionnaire yet.')
    : res.score == null
      ? L(`Pas de pourcentage avec moins de ${MIN_COMPARED} questions en commun.`, `No percentage with fewer than ${MIN_COMPARED} shared questions.`)
      : L('d’affinité avec vous', 'similar to you');
  return html`<div class="overlay fr-compare" role="dialog" aria-modal="true" aria-label="${L(`${c.name} : accords et désaccords`, `${c.name}: agreements and differences`)}">
    <section class="panel p-left"><h3><span class="sim-dot"></span> ${L('Points d’accord', 'Where you agree')} <span class="faint small">(${res.similarities.length})</span></h3>
      ${res.similarities.length ? res.similarities.map((it) => positionItem(it.q, it.pos, it.user)) : html`<p class="muted small">${L(`Aucune question sourcée où ${short} et vous êtes d’accord.`, `No sourced question where you and ${short} line up.`)}</p>`}</section>
    <section class="panel p-center">
      <button type="button" class="toggle-icon close-x" data-close aria-label="${L('Fermer', 'Close')}">${icon.close()}</button>
      ${candPhoto(c, { size: 80 })}
      <h2 style="margin:10px 0 6px">${c.name}</h2>
      <div style="margin-bottom:12px">${partyChip(c)}</div>
      <div class="fr-score num">${res.score == null ? '—' : fmtPctFr(res.score, 0)}</div>
      <div class="small muted" style="margin-top:4px">${status}</div>
      ${res.userAnswered ? html`<p class="small faint" style="margin:10px 0 0">${L(`Comparé sur ${res.compared} des ${res.userAnswered} questions auxquelles vous avez répondu.`, `Compared on ${res.compared} of the ${res.userAnswered} questions you answered.`)}</p>` : ''}
      <div class="row" style="justify-content:center;margin-top:14px">
        ${res.userAnswered < MIN_COMPARED ? html`<a class="btn btn-sm btn-primary" href="${QUIZ_URL}">${L('Répondre au questionnaire', 'Answer the questionnaire')}</a>` : ''}
        <a class="btn btn-sm" href="#/fr/candidat/${c.id}">${L('Toutes ses positions', 'All their positions')}</a>
      </div>
    </section>
    <section class="panel p-right"><h3><span class="dif-dot"></span> ${L('Points de désaccord', 'Where you differ')} <span class="faint small">(${res.differences.length})</span></h3>
      ${res.differences.length ? res.differences.map((it) => positionItem(it.q, it.pos, it.user)) : html`<p class="muted small">${L(`Aucun désaccord sourcé avec ${short}.`, `No sourced disagreement with ${short}.`)}</p>`}</section>
    <section class="panel p-bottom"><h3><span class="unc-dot"></span> ${L('Sans position connue', 'Unclear / no stated position')} <span class="faint small">(${res.unclear.length})</span></h3>
      <p class="small muted" style="margin-top:0">${L(
        `Vous avez répondu à ces questions, mais aucune position sourcée de ${short} n’a été trouvée : elles sont laissées de côté plutôt que devinées. Les questions passées (« sans avis ») ne comptent pas.`,
        `You answered these, but no sourced position from ${short} was found, so they are left out rather than guessed. Questions you skipped (“no opinion”) don’t count.`,
      )}</p>
      <div class="answer-list">${res.unclear.map((it) => html`<div class="answer-row"><span>${it.q.n}. ${qText(it.q)}</span><span class="answer-tag">${L('Vous :', 'You:')} ${answerLabel(it.q, it.user)}</span></div>`)}</div></section>
  </div>`;
}

// Opens the comparison when an element with data-compare="<candidate id>" inside root
// is clicked. Returns the cleanup for the view's mount (it also closes an open panel).
export function wireCompare(root, cands, positionsById) {
  const slot = document.getElementById('overlay-root');
  let lastFocus = null;
  const onKey = (e) => { if (e.key === 'Escape') close(); };
  function close() {
    if (!slot.querySelector('.fr-compare')) return;
    slot.innerHTML = '';
    document.body.style.overflow = '';
    document.removeEventListener('keydown', onKey);
    if (lastFocus?.isConnected) lastFocus.focus();
  }
  const onClick = (e) => {
    const b = e.target.closest('[data-compare]');
    if (!b || !root.contains(b)) return;
    const c = cands.find((x) => x.id === b.dataset.compare);
    if (!c) return;
    e.preventDefault();
    lastFocus = b;
    slot.innerHTML = String(compareOverlay(c, positionsById?.[c.id]));
    document.body.style.overflow = 'hidden';
    document.addEventListener('keydown', onKey);
    const ov = slot.querySelector('.overlay');
    ov.addEventListener('click', (ev) => { if (ev.target === ov || ev.target.closest('[data-close]')) close(); });
    slot.querySelector('[data-close]')?.focus();
  };
  root.addEventListener('click', onClick);
  return () => { root.removeEventListener('click', onClick); close(); };
}
