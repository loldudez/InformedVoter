// "Compare with my views" in the U.S. section: the visitor's My views answers beside one
// person's sourced positions (research overlays, statements, recorded votes), laid out as
// "Match with My views" always was: similarities on the left, differences on the right,
// the person and the score in the middle, and the questions with no known position along
// the bottom. A position is never inferred: an unknown one stays out of the score, and
// below MIN_COMPARED compared questions no percentage is shown.
//
// Used by "Match with My views" (js/views/elections.js) for candidates and by the person
// cards (js/components/person.js) for the people elected or in office.

import { html, fmtDate } from '../util.js';
import { icon } from '../icons.js';
import { L } from '../i18n.js';
import { store } from '../store.js';
import { questionsForLevel, stanceSentence, userSentence, qText } from '../data/questions.js';
import { compare } from '../model/match.js';
import { candBadge, lastName } from './race.js';

export function sourceLink(src) {
  if (!src) return '';
  if (src.url) return html`<a class="src-link" href="${src.url}" target="_blank" rel="noopener noreferrer" title="${src.title}">source ${icon.external()}</a>`;
  return html`<button type="button" class="src-link" title="Demo source: in the live site this links to the candidate’s own statement, vote or questionnaire.">demo source</button>`;
}

export function evidence(item, cand) {
  const who = lastName(cand.name);
  return html`<div class="evidence">
    <div class="q">${qText(item.q)}</div>
    <div class="muted">Based on ${item.source?.title || 'a documented statement'}${item.source?.date ? `, ${item.source.accessed ? 'accessed ' : ''}${fmtDate(item.source.date)}` : ''}, ${stanceSentence(who, item.q, item.stance)}.${item.source?.quote ? html` <span class="quote">“${item.source.quote}”</span>` : ''} ${userSentence(item.q, item.user)} ${sourceLink(item.source)}</div>
  </div>`;
}

// The three panels for one comparison (`row` from compare() or rank()). `sub` is the line
// under the name (party, office), `heart` the like button for candidates.
export function compareOverlay(row, c, { color, sub = '', heart = '' } = {}) {
  const who = lastName(c.name);
  return html`<div class="overlay us-compare" role="dialog" aria-modal="true" aria-label="${L(`${c.name} : points communs et différences`, `${c.name}: similarities and differences`)}">
    <section class="panel p-left"><h3><span class="sim-dot"></span> ${L('Points communs', 'Similarities')} <span class="faint small">(${row.similarities.length})</span></h3>
      ${row.similarities.length ? row.similarities.map((it) => evidence(it, c)) : html`<p class="muted small">${L(`Aucune question sur laquelle ${who} et vous êtes d’accord.`, `No issues where you and ${who} line up.`)}</p>`}</section>
    <section class="panel p-center">
      <button type="button" class="toggle-icon close-x" data-close aria-label="${L('Fermer', 'Close')}">${icon.close()}</button>
      ${candBadge(c, color, 'width:64px;height:64px;font-size:22px;margin:4px auto 10px;border-radius:18px')}
      <h2 style="margin:0">${c.name}</h2>
      <div class="cand-party" style="margin-bottom:10px">${sub}</div>
      <div style="font-size:52px;font-weight:800;letter-spacing:-.03em;line-height:1">${row.score == null ? '—' : L(`${row.score} %`, `${row.score}%`)}</div>
      <div class="small muted">${row.score == null ? L('Pas assez de positions documentées pour un pourcentage', 'Not enough documented positions to score') : L('de points communs avec vous', 'similar to you')}</div>
      <p class="small faint" style="margin:10px 0 0">${L(`Comparé sur ${row.compared} des ${row.userAnswered} questions auxquelles vous avez répondu.`, `Compared on ${row.compared} of the ${row.userAnswered} issues you answered.`)}</p>
      ${heart ? html`<div class="row" style="justify-content:center;margin-top:12px">${heart}</div>` : ''}
    </section>
    <section class="panel p-right"><h3><span class="dif-dot"></span> ${L('Différences', 'Differences')} <span class="faint small">(${row.differences.length})</span></h3>
      ${row.differences.length ? row.differences.map((it) => evidence(it, c)) : html`<p class="muted small">${L(`Aucun désaccord documenté avec ${who}.`, `No documented disagreements with ${who}.`)}</p>`}</section>
    <section class="panel p-bottom"><h3><span class="unc-dot"></span> ${L('Pas de position connue', 'Unclear / no stated position')} <span class="faint small">(${row.unclear.length})</span></h3>
      <p class="small muted" style="margin-top:0">${L(`${who} n’a pas pris de position publique claire sur ces questions : elles sont laissées hors du score plutôt que devinées.`, `${who} hasn’t taken a clear public position on these, so they are left out of the score rather than guessed.`)}</p>
      <div class="answer-list">${row.unclear.map((it) => html`<div class="answer-row"><span>${qText(it.q)}</span><span class="answer-tag">${L('Pas de position claire', 'No clear position')}</span></div>`)}</div></section>
  </div>`;
}

// The visitor's answers to the questions of one level ('federal' or 'state').
export const answeredAt = (level) => {
  const a = store.get().answers;
  return questionsForLevel(level).filter((q) => a[q.id] != null && a[q.id] !== 'skip').length;
};
export const compareWith = (positions, level) => compare(store.get().answers, positions || {}, questionsForLevel(level).map((q) => q.id));

// People shown with a compare button register here, by their key: what the overlay needs.
const shown = new Map();
export const registerPerson = (key, entry) => { shown.set(key, entry); };

// Opens the comparison when an element with data-compare="<key>" inside root is clicked.
// Returns the cleanup for the view's mount (it also closes an open overlay).
export function wireCompare(root) {
  const slot = document.getElementById('overlay-root');
  let lastFocus = null;
  const onKey = (e) => { if (e.key === 'Escape') close(); };
  function close() {
    if (!slot.querySelector('.us-compare')) return;
    slot.innerHTML = '';
    document.body.style.overflow = '';
    document.removeEventListener('keydown', onKey);
    if (lastFocus?.isConnected) lastFocus.focus();
  }
  const onClick = (e) => {
    const b = e.target.closest('[data-compare]');
    if (!b || !root.contains(b)) return;
    const hit = shown.get(b.dataset.compare);
    if (!hit) return;
    e.preventDefault();
    lastFocus = b;
    const row = compareWith(hit.person.positions, hit.level);
    slot.innerHTML = String(compareOverlay(row, hit.person, { color: hit.color, sub: hit.sub }));
    document.body.style.overflow = 'hidden';
    document.addEventListener('keydown', onKey);
    const ov = slot.querySelector('.overlay');
    ov.addEventListener('click', (ev) => { if (ev.target === ov || ev.target.closest('[data-close]')) close(); });
    slot.querySelector('[data-close]')?.focus();
  };
  root.addEventListener('click', onClick);
  return () => { root.removeEventListener('click', onClick); close(); };
}
