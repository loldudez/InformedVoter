// "Mon profil" (picture, answers by topic, address), the "Mes opinions" questionnaire
// (one question per slide) and "Mes élections" (the elections at the visitor's address,
// with countdowns and reminders).

import { html, raw, clamp } from '../../util.js';
import { icon } from '../../icons.js';
import { L, lang } from '../../i18n.js';
import { store } from '../../store.js';
import { frStore } from '../store.js';
import { avatarSrc } from '../../components/shell.js';
import { reminderButton } from '../../components/reminders.js';
import { FR_CATEGORIES, FR_QUESTIONS, FR_CATEGORY_BY_ID, qText, catTitle, scaleFor, answerLabel } from '../questions.js';
import { geocodeFr } from '../geocode.js';
import { loadCalendar, loadPres, loadPositions, fmtDay, mainCandidates, fmtPctFr } from '../data.js';
import { upcomingFor, electionName, electionWhat, whenLabel, electionTile, specialNote } from '../elections.js';
import { candPhoto, partyChip } from '../components.js';
import { MIN_COMPARED } from '../match.js';
import { QUIZ_URL } from '../compare.js';
import { researchedCandidates } from './comparer.js';

async function shrinkImage(file) {
  const url = URL.createObjectURL(file);
  try {
    const img = await new Promise((res, rej) => { const i = new Image(); i.onload = () => res(i); i.onerror = rej; i.src = url; });
    const size = 256;
    const c = document.createElement('canvas');
    c.width = c.height = size;
    const s = Math.min(img.width, img.height);
    c.getContext('2d').drawImage(img, (img.width - s) / 2, (img.height - s) / 2, s, s, 0, 0, size, size);
    return c.toDataURL('image/jpeg', 0.86);
  } finally {
    URL.revokeObjectURL(url);
  }
}

function head() {
  const st = frStore.get();
  const answered = frStore.answered();
  return html`<div class="card profile-head">
    <div class="profile-avatar"><img class="avatar" src="${avatarSrc()}" alt="${L('Votre photo de profil', 'Your profile picture')}"></div>
    <div style="flex:1;min-width:220px">
      <div class="eyebrow">${L('Mon profil', 'My profile')}</div>
      <h1 style="font-size:clamp(28px,3.4vw,40px);margin:4px 0 6px">${L('Votre profil d’électeur', 'Your voter profile')}</h1>
      <div class="row small muted"><span>${L(`${answered} questions répondues sur ${FR_QUESTIONS.length}`, `${answered} of ${FR_QUESTIONS.length} questions answered`)}</span><span>·</span><span>${st.address ? st.address.city : L('pas d’adresse', 'no address')}</span></div>
    </div>
    <div class="row">
      <label class="btn btn-sm" for="avatar-file">${icon.upload()} ${L('Changer de photo', 'Change picture')}</label>
      <input id="avatar-file" type="file" accept="image/*" class="sr-only">
      ${store.get().avatar ? html`<button type="button" class="btn btn-sm btn-ghost" id="avatar-reset">${L('Revenir au drapeau', 'Use the flag')}</button>` : ''}
    </div>
  </div>`;
}

function opinionsTab() {
  const a = frStore.get().answers;
  const touched = Object.keys(a).length;
  return html`<div class="stack">
    <div class="card">
      <div class="row between">
        <div><h2 style="margin:0">${L('Mes opinions', 'My views')}</h2><p class="muted" style="margin:4px 0 0">${L(`${FR_QUESTIONS.length} questions en ${FR_CATEGORIES.length} thèmes, une à la fois. Vous pouvez passer celles que vous voulez.`, `${FR_QUESTIONS.length} questions in ${FR_CATEGORIES.length} topics, one at a time. Skip any you like.`)}</p></div>
        <a class="btn btn-primary" href="${QUIZ_URL}">${touched === 0 ? L('Commencer le questionnaire', 'Start the questionnaire') : touched >= FR_QUESTIONS.length ? L('Revoir depuis le début', 'Review from the start') : L('Reprendre où j’en étais', 'Continue where I left off')}</a>
      </div>
      <div class="progress" style="margin:16px 0 6px"><span style="width:${(touched / FR_QUESTIONS.length) * 100}%"></span></div>
      <p class="small faint" style="margin:0">${L(`${frStore.answered()} répondues, ${touched - frStore.answered()} passées. Vos réponses ne quittent jamais ce navigateur.`, `${frStore.answered()} answered, ${touched - frStore.answered()} skipped. Your answers never leave this browser.`)}</p>
    </div>
    <div class="card"><h3>${L('Par thème', 'By topic')}</h3>
      ${FR_CATEGORIES.map((c) => {
        const done = c.questions.filter((q) => a[q.id] != null).length;
        const first = FR_QUESTIONS.indexOf(c.questions.find((q) => a[q.id] == null) || c.questions[0]);
        return html`<div class="cat-progress"><a href="${QUIZ_URL}?q=${first}">${c.n}. ${catTitle(c)}</a><div class="progress"><span style="width:${(done / c.questions.length) * 100}%"></span></div><span class="small faint num">${done}/${c.questions.length}</span></div>`;
      })}
    </div>
    ${touched ? html`<details class="card"><summary style="cursor:pointer;font-weight:650">${L('Revoir et modifier mes réponses', 'Review and edit my answers')}</summary>
      <div class="stack" style="margin-top:14px">${FR_CATEGORIES.map((c) => html`<div><div class="eyebrow" style="margin-bottom:6px">${catTitle(c)}</div><div class="answer-list">${c.questions.filter((q) => a[q.id] != null).map((q) => html`<a class="answer-row" href="${QUIZ_URL}?q=${FR_QUESTIONS.indexOf(q)}"><span>${q.n}. ${qText(q)}</span><span class="answer-tag">${a[q.id] === 'skip' ? L('Passée', 'Skipped') : answerLabel(q, a[q.id])}</span></a>`)}</div></div>`)}</div>
      <button type="button" class="btn btn-sm btn-ghost" id="clear-answers" style="margin-top:16px">${icon.trash()} ${L('Effacer toutes mes réponses', 'Clear all my answers')}</button>
    </details>` : ''}
  </div>`;
}

function addressForm() {
  const ad = frStore.get().address;
  return html`<form class="card stack" id="address-form" novalidate>
    <div><h2 style="margin:0">${L('Ma localisation', 'My location')}</h2><p class="muted" style="margin:4px 0 0">${L('Votre adresse indique votre commune, votre département et votre région, donc les élections qui vous concernent.', 'Your address tells us your commune, department and region, and so the elections that concern you.')}</p></div>
    <div class="notice">${icon.info()}<div><b>${L('Utilisation de votre adresse.', 'How your address is used.')}</b> ${L('Elle est envoyée uniquement au service public de géocodage de l’IGN (Géoplateforme) pour trouver votre commune, puis enregistrée dans ce navigateur. Informed Voter n’a pas de serveur et ne la reçoit jamais.', 'It is sent only to IGN’s public geocoding service (Géoplateforme) to find your commune, then saved in this browser. Informed Voter has no server and never receives it.')}</div></div>
    <label class="check"><input type="checkbox" id="consent" ${raw(ad?.consent ? 'checked' : '')}> <span>${L('J’accepte qu’Informed Voter utilise mon adresse uniquement pour trouver les élections qui me concernent.', 'I agree to let Informed Voter use my address only to find the elections that concern me.')}</span></label>
    <div class="field"><label for="addr">${L('Adresse postale', 'Street address')}</label><input class="input" id="addr" autocomplete="street-address" placeholder="${L('8 rue de Rivoli, 75004 Paris', '8 rue de Rivoli, 75004 Paris')}" value="${ad?.input || ''}"></div>
    <div class="row"><button class="btn btn-primary" type="submit">${icon.pin()} ${L('Trouver mon adresse', 'Find my address')}</button><span class="small faint" id="addr-status" role="status"></span></div>
    <div id="suggestions" class="stack-sm"></div>
  </form>`;
}

function locationTab() {
  const ad = frStore.get().address;
  if (!ad) return addressForm();
  return html`<div class="stack">
    <div class="card">
      <div class="row between"><div><div class="eyebrow">${L('Adresse enregistrée', 'Saved address')}</div><h2 style="margin:4px 0 0;font-size:22px">${ad.label}</h2></div>
        <a class="btn btn-primary" href="#/fr/elections">${icon.ballot()} ${L('Voir mes élections', 'See my elections')}</a></div>
      <p class="small faint" style="margin:6px 0 16px">${L(`Trouvée par la Géoplateforme (IGN) le ${fmtDay(ad.savedAt.slice(0, 10))}. Enregistrée uniquement dans ce navigateur.`, `Matched by the Géoplateforme (IGN) on ${fmtDay(ad.savedAt.slice(0, 10))}. Stored only in this browser.`)}</p>
      <dl class="kv"><dt>${L('Commune', 'Commune')}</dt><dd><a href="#/fr/ville/${ad.citycode}">${ad.city}</a> (${ad.citycode})</dd>
        <dt>${L('Département', 'Department')}</dt><dd><a href="#/fr/departement/${ad.dep}">${ad.depName || ad.dep}</a> (${ad.dep})</dd>
        <dt>${L('Région', 'Region')}</dt><dd>${ad.reg ? html`<a href="#/fr/region/${ad.reg}">${ad.regName || ad.reg}</a>` : '—'}</dd></dl>
      <div class="row" style="margin-top:18px"><button type="button" class="btn btn-sm" id="change-address">${L('Changer d’adresse', 'Change address')}</button><button type="button" class="btn btn-sm btn-ghost" id="remove-address">${icon.trash()} ${L('Supprimer mon adresse', 'Remove my address')}</button></div>
    </div>
    <div id="address-form-slot" hidden>${addressForm()}</div>
  </div>`;
}

export const profil = {
  title: () => L('Mon profil', 'My profile'),
  rerenderOn: ['answers', 'address'],
  render(ctx) {
    const tab = ctx.query.onglet === 'localisation' ? 'localisation' : 'opinions';
    return html`<div class="wrap page stack" style="max-width:960px">
      ${head()}
      <nav class="seg" aria-label="${L('Sections du profil', 'Profile sections')}"><a href="#/fr/profil" ${raw(tab === 'opinions' ? 'aria-current="page"' : '')}>${L('Mes opinions', 'My views')}</a><a href="#/fr/profil?onglet=localisation" ${raw(tab === 'localisation' ? 'aria-current="page"' : '')}>${L('Ma localisation', 'My location')}</a></nav>
      ${tab === 'opinions' ? opinionsTab() : locationTab()}
    </div>`;
  },
  mount(root) {
    const file = root.querySelector('#avatar-file');
    file?.addEventListener('change', async () => {
      const f = file.files?.[0];
      if (!f || !f.type.startsWith('image/') || f.size > 15e6) return;
      try {
        store.set({ avatar: await shrinkImage(f) });
        window.dispatchEvent(new Event('iv:rerender'));
      } catch {
        alert(L('Cette image n’a pas pu être lue. Essayez un JPG ou un PNG.', 'That image could not be read. Try a JPG or PNG.'));
      }
    });
    root.querySelector('#avatar-reset')?.addEventListener('click', () => { store.set({ avatar: null }); window.dispatchEvent(new Event('iv:rerender')); });
    root.querySelector('#clear-answers')?.addEventListener('click', () => {
      if (confirm(L('Effacer toutes vos réponses ? C’est définitif.', 'Clear all of your answers? This cannot be undone.'))) frStore.set({ answers: {}, quizPos: 0 });
    });
    root.querySelector('#remove-address')?.addEventListener('click', () => {
      if (confirm(L('Supprimer votre adresse de ce navigateur ?', 'Remove your saved address from this browser?'))) frStore.set({ address: null });
    });
    root.querySelector('#change-address')?.addEventListener('click', () => {
      const slot = root.querySelector('#address-form-slot');
      slot.hidden = false;
      slot.querySelector('#addr')?.focus();
    });
    const form = root.querySelector('#address-form');
    if (!form) return;
    const status = form.querySelector('#addr-status');
    const sugg = form.querySelector('#suggestions');
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const input = form.querySelector('#addr').value.trim();
      sugg.innerHTML = '';
      if (!form.querySelector('#consent').checked) { status.textContent = L('Cochez d’abord la case d’accord.', 'Please tick the consent box first.'); return; }
      if (input.length < 6) { status.textContent = L('Indiquez votre adresse complète, avec la commune ou le code postal.', 'Enter your full address, including the commune or postcode.'); return; }
      status.innerHTML = `<span class="spinner"></span> ${L('Recherche auprès de la Géoplateforme…', 'Asking the Géoplateforme…')}`;
      try {
        const matches = await geocodeFr(input);
        if (!matches.length) {
          status.textContent = '';
          sugg.innerHTML = String(html`<div class="notice warn">${icon.info()}<div>${L('Aucune adresse trouvée. Vérifiez l’orthographe et ajoutez la commune ou le code postal.', 'No address found. Check the spelling and add the commune or postcode.')}</div></div>`);
          return;
        }
        status.textContent = matches.length === 1 ? L('Est-ce bien votre adresse ?', 'Is this your address?') : L('Choisissez votre adresse :', 'Pick your address:');
        sugg.innerHTML = matches.map((m, i) => String(html`<button type="button" class="suggestion" data-i="${i}">${icon.pin()}<span><b>${m.label}</b><br><span class="small faint">${m.depName ? `${m.depName} (${m.dep})` : m.dep}</span></span><span class="btn btn-sm" style="margin-left:auto">${L('Choisir', 'Use this')}</span></button>`)).join('');
        sugg.querySelectorAll('[data-i]').forEach((b) => b.addEventListener('click', async () => {
          const m = matches[+b.dataset.i];
          const regs = await import('../data.js').then((d) => d.loadRegions());
          const regName = regs?.features.find((f) => f.id === m.reg)?.properties.name || null;
          frStore.set({ address: { ...m, regName, consent: true, input, savedAt: new Date().toISOString() } });
          if (location.hash !== '#/fr/profil?onglet=localisation') location.hash = '#/fr/profil?onglet=localisation';
        }));
      } catch (err) {
        status.textContent = L(`La recherche a échoué (${err.message}). Réessayez.`, `The search failed (${err.message}). Please try again.`);
      }
    });
  },
};

// The questionnaire ----------------------------------------------------------------

function slide(i, answers) {
  const q = FR_QUESTIONS[i];
  const cat = FR_CATEGORY_BY_ID[q.cat];
  const inCat = cat.questions;
  const current = answers[q.id];
  return html`<div class="quiz">
    <div class="row between" style="margin-bottom:10px"><nav class="crumbs" style="margin:0"><a href="#/fr/profil">${L('Mon profil', 'My profile')}</a><span>/</span><span>${L('Mes opinions', 'My views')}</span></nav><div class="eyebrow num">${L(`Question ${i + 1} sur ${FR_QUESTIONS.length}`, `Question ${i + 1} of ${FR_QUESTIONS.length}`)}</div></div>
    <div class="progress"><span style="width:${(i / FR_QUESTIONS.length) * 100}%"></span></div>
    <div class="quiz-cats" aria-hidden="true">${FR_CATEGORIES.map((c) => html`<i class="${c.n < cat.n ? 'done' : c.n === cat.n ? 'cur' : ''}" title="${catTitle(c)}"></i>`)}</div>
    ${i === 0 ? html`<div class="notice" style="margin-top:16px">${icon.info()}<div>${L('Comptez environ vingt minutes pour les 144 questions. Vous pouvez vous arrêter quand vous voulez et reprendre plus tard : vos réponses sont enregistrées dans ce navigateur.', 'Allow about twenty minutes for all 144 questions. You can stop at any time and pick up later: your answers are saved in this browser.')}</div></div>` : ''}
    <div class="quiz-card" style="margin-top:18px" tabindex="-1">
      <div class="eyebrow" style="color:var(--brand-2)">${cat.n}. ${catTitle(cat)} · ${inCat.indexOf(q) + 1}/${inCat.length}</div>
      <p class="quiz-q" id="quiz-q" lang="${L('fr', 'en')}">${qText(q)}</p>
      ${lang() === 'en' ? html`<p class="tiny faint" style="margin:-6px 0 12px">Translated from the original French: <span lang="fr">« ${q.fr} »</span></p>` : ''}
      <div class="scale" role="group" aria-labelledby="quiz-q">
        ${scaleFor(q).map((s, k) => html`<button type="button" data-v="${s.value}" aria-pressed="${String(current === s.value)}"><span class="dot"></span>${s.label}<span class="k">${k + 1}</span></button>`)}
      </div>
      <div class="quiz-nav">
        <button type="button" class="btn btn-sm btn-ghost" data-nav="back" ${raw(i === 0 ? 'disabled' : '')}>${icon.chevronLeft()} ${L('Retour', 'Back')}</button>
        <div class="row">
          <button type="button" class="btn btn-sm btn-ghost" data-nav="skip">${current === 'skip' ? L('Passée · suivante', 'Skipped · next') : L('Passer / sans avis', 'Skip / no opinion')}</button>
          ${current != null ? html`<button type="button" class="btn btn-sm" data-nav="next">${L('Suivante', 'Next')} ${icon.chevronRight()}</button>` : ''}
        </div>
      </div>
    </div>
    <p class="small faint" style="text-align:center;margin-top:14px">${L('Touches 1 à 5 pour répondre, ← pour revenir. Enregistré au fur et à mesure dans ce navigateur.', 'Keys 1–5 answer, ← goes back. Saved in this browser as you go.')}</p>
  </div>`;
}

function done() {
  return html`<div class="quiz"><div class="quiz-card" style="text-align:center">
    <div style="font-size:44px">✅</div>
    <h2>${L('C’est terminé', 'All done')}</h2>
    <p class="muted">${L(`Vous avez répondu à ${frStore.answered()} questions sur ${FR_QUESTIONS.length}. Vous pouvez modifier chaque réponse plus tard.`, `You answered ${frStore.answered()} of ${FR_QUESTIONS.length} questions. You can change any answer later.`)}</p>
    <div class="row" style="justify-content:center;margin-top:10px"><a class="btn btn-primary" href="#/fr/elections/comparer">${L('Comparer avec les candidats', 'Compare with the candidates')}</a><a class="btn" href="#/fr/elections">${L('Voir mes élections', 'See my elections')}</a><a class="btn" href="#/fr/profil">${L('Revoir mes réponses', 'Review answers')}</a></div>
  </div></div>`;
}

export const opinions = {
  title: () => L('Mes opinions', 'My views'),
  render: () => html`<div class="wrap page"><div id="quiz-host"></div></div>`,
  mount(root, ctx) {
    const host = root.querySelector('#quiz-host');
    let i = clamp(ctx.query.q != null ? +ctx.query.q : frStore.get().quizPos || 0, 0, FR_QUESTIONS.length - 1);
    let busy = false;
    const draw = () => {
      host.innerHTML = String(slide(i, frStore.get().answers));
      frStore.set({ quizPos: i });
      host.querySelector('.quiz-card')?.focus({ preventScroll: true });
    };
    const advance = () => { if (i < FR_QUESTIONS.length - 1) { i++; draw(); } else { host.innerHTML = String(done()); frStore.set({ quizPos: 0 }); } };
    const save = (v) => frStore.set({ answers: { ...frStore.get().answers, [FR_QUESTIONS[i].id]: v } });
    const answer = (v) => {
      if (busy) return;
      busy = true;
      save(v);
      host.querySelectorAll('[data-v]').forEach((b) => b.setAttribute('aria-pressed', String(+b.dataset.v === v)));
      setTimeout(() => { busy = false; advance(); }, 220);
    };
    host.addEventListener('click', (e) => {
      const b = e.target.closest('button');
      if (!b) return;
      if (b.dataset.v != null) answer(+b.dataset.v);
      else if (b.dataset.nav === 'back' && i > 0) { i--; draw(); }
      else if (b.dataset.nav === 'skip') { save('skip'); advance(); }
      else if (b.dataset.nav === 'next') advance();
    });
    const onKey = (e) => {
      if (!host.querySelector('.scale') || (e.target instanceof Element && e.target.closest('input, textarea, select'))) return;
      if (e.key >= '1' && e.key <= '5') answer(scaleFor(FR_QUESTIONS[i])[+e.key - 1].value);
      else if (e.key === 'ArrowLeft' && i > 0) { i--; draw(); }
    };
    document.addEventListener('keydown', onKey);
    draw();
    return () => document.removeEventListener('keydown', onKey);
  },
};

// My elections ---------------------------------------------------------------------

// "Comparer avec mes opinions", as on the U.S. side's "Match with My views": the ranking
// page (#/fr/elections/comparer) once the visitor has answered enough questions,
// otherwise a way to the questionnaire.
function compareBlock(pres, positions, answered) {
  const n = researchedCandidates(pres, positions).length;
  if (!n) return '';
  const ready = answered >= MIN_COMPARED;
  return html`<div class="fr-compare-cta row between">
    <div style="flex:1;min-width:240px"><b>${L('Comparer les candidats avec mes opinions', 'Compare the candidates with my views')}</b>
      <p class="small muted" style="margin:2px 0 0">${ready
        ? L(`${n} candidats ont des positions sourcées. Voyez lequel vous correspond le mieux, puis, pour chacun, vos points d’accord, vos désaccords et les questions sans position connue.`, `${n} candidates have sourced positions. See which matches you best, then, for each, where you agree, where you differ and the questions with no known position.`)
        : L(`Répondez à au moins ${MIN_COMPARED} questions de Mes opinions (vous en avez ${answered}) pour comparer les ${n} candidats dont les positions sont sourcées.`, `Answer at least ${MIN_COMPARED} questions in My views (you have ${answered}) to compare the ${n} candidates with sourced positions.`)}</p></div>
    ${ready
      ? html`<a class="btn btn-primary" href="#/fr/elections/comparer">${icon.user()} ${L('Comparer avec mes opinions', 'Compare with my views')}</a>`
      : html`<a class="btn" href="${QUIZ_URL}">${icon.user()} ${L('Répondre d’abord à Mes opinions', 'Answer My views first')}</a>`}
  </div>`;
}

export const mesElections = {
  title: () => L('Mes élections', 'My elections'),
  rerenderOn: ['address', 'reminders'],
  async render() {
    const ad = frStore.get().address;
    const [cal, pres, positions] = await Promise.all([loadCalendar(), loadPres(), loadPositions()]);
    if (!ad) {
      return html`<div class="wrap page" style="max-width:860px">
        <div class="eyebrow">${L('Mes élections', 'My elections')}</div><h1>${L('Vos élections, d’après votre adresse', 'Your elections, from your address')}</h1>
        <div class="empty">${icon.pin()}<h3>${L('Ajoutez votre adresse pour voir vos élections', 'Add your address to see your elections')}</h3><p>${L('Votre commune, votre département et votre région déterminent les élections qui vous concernent. L’adresse reste dans ce navigateur.', 'Your commune, department and region decide which elections concern you. The address stays in this browser.')}</p><a class="btn btn-primary" href="#/fr/profil?onglet=localisation">${L('Ajouter mon adresse', 'Add my address')}</a></div>
        ${pres ? html`<section class="card stack" style="margin-top:24px"><h2 style="margin:0">${L('Présidentielle 2027', '2027 presidential election')}</h2>${compareBlock(pres, positions, frStore.answered())}</section>` : ''}
      </div>`;
    }
    const list = cal ? upcomingFor(cal, ad) : [];
    const answered = frStore.answered();
    const rows = pres ? mainCandidates(pres, 4).slice(0, 8) : [];
    return html`<div class="wrap page stack-lg" style="max-width:1000px">
      <div><div class="eyebrow">${L('Mes élections', 'My elections')}</div><h1 style="margin:6px 0 8px">${L('Les élections qui vous concernent', 'The elections that concern you')}</h1>
        <p class="muted" style="margin:0">${icon.pin()} ${ad.label} · <a href="#/fr/profil?onglet=localisation">${L('Changer', 'Change')}</a></p></div>
      <div class="fr-next">${list.map((e) => electionTile(e, { href: `#/fr/calendrier?e=${e.id}` }))}</div>
      ${pres ? html`<section class="card stack">
        <div class="row between"><div><div class="eyebrow">${L('La prochaine', 'The next one')} · ${whenLabel(cal.elections.find((e) => e.id === 'presidentielle-2027'))}</div><h2 style="margin:4px 0 0">${L('Présidentielle 2027', '2027 presidential election')}</h2></div>
          ${reminderButton({ id: 'fr:presidentielle-2027', name: L('Présidentielle 2027, 1er tour', '2027 presidential election, round 1'), date: pres.rounds.r1, date2: pres.rounds.r2, name2: L('Présidentielle 2027, 2nd tour', '2027 presidential election, round 2'), section: 'fr' })}</div>
        <div class="fr-faces">${rows.map((c) => html`<a class="fr-face" href="#/fr/candidat/${c.id}">${candPhoto(c, { size: 72 })}<b>${c.name}</b><span class="tiny">${partyChip(c)}</span><span class="num">${fmtPctFr(c.avg.avg)}</span></a>`)}</div>
        ${compareBlock(pres, positions, answered)}
        <div class="row"><a class="btn btn-sm" href="#/fr/presidentielle">${L('Sondages des deux tours', 'Polls for both rounds')}</a><a class="btn btn-sm" href="#/fr/presidentielle?tour=c">${L('Les candidats', 'The candidates')}</a><a class="btn btn-sm btn-ghost" href="${QUIZ_URL}">${answered ? L('Continuer le questionnaire', 'Continue the questionnaire') : L('Répondre au questionnaire', 'Answer the questionnaire')}</a></div>
      </section>` : ''}
      <section class="stack">
        <h2 style="margin:0">${L('Toutes vos prochaines élections', 'All your upcoming elections')}</h2>
        ${list.map((e) => {
          const note = specialNote(e, ad);
          return html`<article class="card tight"><div class="row between"><div><b>${electionName(e)}</b><div class="small muted">${whenLabel(e)}</div></div>
            ${reminderButton({ id: `fr:${e.id}`, name: electionName(e), date: e.date || null, date2: e.round2 || null, month: e.month || null, section: 'fr' })}</div>
            <p class="small" style="margin:8px 0 0">${electionWhat(e)}</p>${note ? html`<p class="small muted" style="margin:6px 0 0">${icon.info()} ${note}</p>` : ''}</article>`;
        })}
      </section>
    </div>`;
  },
};
