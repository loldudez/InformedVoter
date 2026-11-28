// The one-question-per-slide questionnaire, used for "My views" and for
// per-election views. Answering moves to the next slide; Back goes back.

import { html, raw, clamp } from '../util.js';
import { icon } from '../icons.js';
import { store } from '../store.js';
import { QUESTIONS, CATEGORY_BY_ID, SCALE, questionsForLevel, qText, catTitle } from '../data/questions.js';
import { ensureRace, raceTitle } from '../data/world.js';
import { annotate, termDefs, termsIn, wireTerms, closeTerm } from '../components/terms.js';
import { L, lang } from '../i18n.js';

function slide({ questions, answers, i, heading }) {
  const q = questions[i];
  const cat = CATEGORY_BY_ID[q.cat];
  const inCat = questions.filter((x) => x.cat === q.cat);
  const catIdx = inCat.indexOf(q);
  const cats = [...new Set(questions.map((x) => x.cat))];
  const curCat = cats.indexOf(q.cat);
  const current = answers[q.id];
  const text = qText(q);
  const hasTerms = termsIn(text).length > 0;
  return html`<div class="quiz">
    <div class="row between" style="margin-bottom:10px"><div class="eyebrow">${heading}</div><div class="eyebrow num">${L(`Question ${i + 1} sur ${questions.length}`, `Question ${i + 1} of ${questions.length}`)}</div></div>
    <div class="progress"><span style="width:${(i / questions.length) * 100}%"></span></div>
    <div class="quiz-cats" aria-hidden="true">${cats.map((c, k) => html`<i class="${k < curCat ? 'done' : k === curCat ? 'cur' : ''}" title="${catTitle(CATEGORY_BY_ID[c])}"></i>`)}</div>
    ${i === 0 ? html`<div class="notice" style="margin-top:16px">${icon.info()}<div>${L(`Les ${questions.length} questions prennent moins de 20 minutes. Vous pouvez vous arrêter à tout moment et reprendre là où vous en étiez, mais vos affinités ne seront pas tout à fait exactes tant que vous n’aurez pas répondu à toutes les questions.`, `All ${questions.length} questions take less than 20 minutes. You can stop at any time and pick up where you left off, but your matches may not be fully accurate until you’ve answered every question.`)}</div></div>` : ''}
    <div class="quiz-card" style="margin-top:18px" tabindex="-1">
      <div class="eyebrow" style="color:var(--brand-2)">${catTitle(cat)} · ${catIdx + 1}/${inCat.length}</div>
      <p class="quiz-q${hasTerms ? ' has-terms' : ''}" id="quiz-q">${annotate(text)}</p>
      ${termDefs(text)}
      ${lang() === 'fr' ? html`<p class="tiny faint" style="margin:-6px 0 12px">Traduit de la question originale en anglais : <span lang="en">“${q.text}”</span></p>` : ''}
      ${hasTerms ? html`<p class="term-hint small faint">${L('Les mots soulignés ont une courte définition : survolez-les, atteignez-les avec la touche Tab ou touchez-les.', 'Underlined words have a short definition: hover over, tab to or tap them.')}</p>` : ''}
      <div class="scale" role="group" aria-labelledby="quiz-q">
        ${SCALE.map((s, k) => html`<button type="button" data-v="${s.value}" aria-pressed="${String(current === s.value)}"><span class="dot"></span>${s.label}<span class="k">${k + 1}</span></button>`)}
      </div>
      <div class="quiz-nav">
        <button type="button" class="btn btn-sm btn-ghost" data-nav="back" ${raw(i === 0 ? 'disabled' : '')}>${icon.chevronLeft()} ${L('Retour', 'Back')}</button>
        <div class="row">
          <button type="button" class="btn btn-sm btn-ghost" data-nav="skip">${current === 'skip' ? L('Passée · suivante', 'Skipped · next') : L('Passer / sans avis', 'Skip / no opinion')}</button>
          ${current != null ? html`<button type="button" class="btn btn-sm" data-nav="next">${L('Suivante', 'Next')} ${icon.chevronRight()}</button>` : ''}
        </div>
      </div>
    </div>
    <p class="small faint" style="text-align:center;margin-top:14px">${L('Les touches 1 à 5 répondent, ← revient en arrière. Vos réponses sont enregistrées dans ce navigateur au fur et à mesure : vous pouvez partir et revenir.', 'Keys 1–5 answer, ← goes back. Saved in this browser as you go, so you can leave and come back.')}</p>
  </div>`;
}

function doneScreen({ answered, total, next, nextLabel, review }) {
  return html`<div class="quiz"><div class="quiz-card" style="text-align:center">
    <div style="font-size:44px">✅</div>
    <h2>${L('Terminé', 'All done')}</h2>
    <p class="muted">${L(`Vous avez répondu à ${answered} questions sur ${total}. Vous pouvez modifier chaque réponse plus tard.`, `You answered ${answered} of ${total} questions. You can change any answer later.`)}</p>
    <div class="row" style="justify-content:center;margin-top:10px"><a class="btn btn-primary" href="${next}">${nextLabel}</a><a class="btn" href="${review}">${L('Revoir mes réponses', 'Review answers')}</a></div>
  </div></div>`;
}

// Runs the slides inside `root`. `save(answers)` persists; `finish()` runs at the end.
function runQuiz(root, { questions, getAnswers, save, start, heading, onPos, finishHTML }) {
  let i = clamp(start, 0, questions.length - 1);
  let busy = false;
  const host = root.querySelector('#quiz-host');
  wireTerms(host);
  const draw = () => {
    closeTerm();
    host.innerHTML = String(slide({ questions, answers: getAnswers(), i, heading }));
    onPos?.(i);
    // Focus the card, not the first answer: a focus ring there looks like a pre-selected answer.
    host.querySelector('.quiz-card')?.focus({ preventScroll: true });
  };
  const advance = () => {
    if (i < questions.length - 1) { i++; draw(); } else { closeTerm(); host.innerHTML = String(finishHTML()); onPos?.(0); }
  };
  const answer = (v) => {
    if (busy) return;
    busy = true;
    save({ ...getAnswers(), [questions[i].id]: v });
    host.querySelectorAll('[data-v]').forEach((b) => b.setAttribute('aria-pressed', String(+b.dataset.v === v)));
    setTimeout(() => { busy = false; advance(); }, 220);
  };
  host.addEventListener('click', (e) => {
    const b = e.target.closest('button');
    if (!b) return;
    if (b.dataset.v != null) answer(+b.dataset.v);
    else if (b.dataset.nav === 'back' && i > 0) { i--; draw(); }
    else if (b.dataset.nav === 'skip') { save({ ...getAnswers(), [questions[i].id]: 'skip' }); advance(); }
    else if (b.dataset.nav === 'next') advance();
  });
  const onKey = (e) => {
    if (!host.querySelector('.scale') || (e.target instanceof Element && e.target.closest('input, textarea, select'))) return;
    if (e.key >= '1' && e.key <= '5') answer(SCALE[+e.key - 1].value);
    else if (e.key === 'ArrowLeft' && i > 0) { i--; draw(); }
  };
  document.addEventListener('keydown', onKey);
  draw();
  return () => document.removeEventListener('keydown', onKey);
}

export const viewsQuiz = {
  title: () => L('Questionnaire « Mes opinions »', 'My views questionnaire'),
  render: () => html`<div class="wrap page"><div id="quiz-host"></div></div>`,
  mount(root, ctx) {
    const start = ctx.query.q != null ? +ctx.query.q : store.get().quizPos || 0;
    return runQuiz(root, {
      questions: QUESTIONS,
      getAnswers: () => store.get().answers,
      save: (answers) => store.set({ answers }),
      start,
      heading: L('Mes opinions', 'My views'),
      onPos: (i) => store.set({ quizPos: i }),
      finishHTML: () => doneScreen({ answered: store.answered(), total: QUESTIONS.length, next: '#/elections', nextLabel: L('Trouver mes affinités', 'Find my matches'), review: '#/profile?tab=views' }),
    });
  },
};

export const electionQuiz = {
  title: () => L('Opinions pour cette élection', 'Views for this election'),
  async render(ctx) {
    const race = await ensureRace(decodeURIComponent(ctx.params[0]));
    if (!race) return html`<div class="wrap page"><p>${L('Élection introuvable.', 'Race not found.')} <a href="#/elections">${L('Retour à mes élections', 'Back to my elections')}</a></p></div>`;
    return html`<div class="wrap page">
      <nav class="crumbs"><a href="#/elections">${L('Mes élections', 'My elections')}</a><span>/</span><span>${raceTitle(race)}</span></nav>
      <div class="notice" style="max-width:760px;margin:0 auto 18px">${icon.info()}<div>${lang() === 'fr'
        ? html`Ces réponses valent seulement pour <b>${raceTitle(race)}</b> et ne changent pas vos opinions enregistrées. Seuls les thèmes qui concernent un poste ${race.level === 'federal' ? 'fédéral' : 'de l’État'} sont abordés.`
        : html`These answers are only for <b>${raceTitle(race)}</b> and don’t change your saved My views. Only topics that apply to a ${race.level === 'federal' ? 'federal' : 'state'} office are asked.`}</div></div>
      <div id="quiz-host"></div>
    </div>`;
  },
  async mount(root, ctx) {
    const race = await ensureRace(decodeURIComponent(ctx.params[0]));
    if (!race) return;
    const questions = questionsForLevel(race.level);
    const get = () => store.get().electionAnswers[race.id] || {};
    return runQuiz(root, {
      questions,
      getAnswers: get,
      save: (answers) => store.set({ electionAnswers: { ...store.get().electionAnswers, [race.id]: answers } }),
      start: 0,
      heading: `${L('Nouvelles opinions', 'New views')} · ${raceTitle(race)}`,
      finishHTML: () => doneScreen({
        answered: store.answered(get()), total: questions.length,
        next: `#/elections/${encodeURIComponent(race.id)}/match?mode=election`, nextLabel: L('Voir qui me correspond', 'See who matches me'),
        review: `#/elections/${encodeURIComponent(race.id)}/quiz`,
      }),
    });
  },
};
