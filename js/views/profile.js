import { html, raw, fmtDate } from '../util.js';
import { icon } from '../icons.js';
import { store } from '../store.js';
import { STATE_BY_ABBR, stateName, chamberName } from '../data/states.js';
import { CATEGORIES, QUESTIONS, SCALE_LABEL, qText, catTitle } from '../data/questions.js';
import { geocode } from '../lib/census.js';
import { avatarSrc } from '../components/shell.js';
import { L } from '../i18n.js';

const ordinalCd = (cd) => (cd === '00' ? L('Circonscription unique', 'At-large district') : cd === '98' ? L('Circonscription du délégué', 'Delegate district') : L(`Circonscription ${parseInt(cd, 10)}`, `District ${parseInt(cd, 10)}`));
const districtNo = (d) => L(`Circonscription ${d.replace(/^0+/, '')}`, `District ${d.replace(/^0+/, '')}`);

function head() {
  const st = store.get();
  const answered = store.answered();
  return html`<div class="card profile-head">
    <div class="profile-avatar"><img class="avatar" src="${avatarSrc()}" alt="${L('Votre photo de profil', 'Your profile picture')}"></div>
    <div style="flex:1;min-width:220px">
      <div class="eyebrow">${L('Mon profil', 'My profile')}</div>
      <h1 style="font-size:clamp(28px,3.4vw,40px);margin:4px 0 6px">${L('Votre profil d’électeur', 'Your voter profile')}</h1>
      <div class="row small muted"><span>${L(`${answered} réponses sur ${QUESTIONS.length} questions`, `${answered} of ${QUESTIONS.length} questions answered`)}</span><span>·</span><span>${L(`${st.starred.length} élections suivies`, `${st.starred.length} starred elections`)}</span><span>·</span><span>${L(`${st.liked.length} candidats favoris`, `${st.liked.length} liked candidates`)}</span></div>
    </div>
    <div class="row">
      <label class="btn btn-sm" for="avatar-file">${icon.upload()} ${L('Changer de photo', 'Change picture')}</label>
      <input id="avatar-file" type="file" accept="image/*" class="sr-only">
      ${st.avatar ? html`<button type="button" class="btn btn-sm btn-ghost" id="avatar-reset">${L('Utiliser le drapeau', 'Use the flag')}</button>` : ''}
    </div>
  </div>`;
}

function viewsTab() {
  const a = store.get().answers;
  const answered = store.answered();
  const touched = Object.keys(a).length;
  return html`<div class="stack">
    <div class="card">
      <div class="row between">
        <div><h2 style="margin:0">${L('Mes opinions', 'My views')}</h2><p class="muted" style="margin:4px 0 0">${L(`${QUESTIONS.length} questions d’accord ou pas d’accord, en ${CATEGORIES.length} thèmes, une à la fois. Passez celles que vous voulez.`, `${QUESTIONS.length} agree-or-disagree questions in ${CATEGORIES.length} topics, one at a time. Skip any you like.`)}</p></div>
        <a class="btn btn-primary" href="#/views">${touched === 0 ? L('Commencer le questionnaire', 'Start the questionnaire') : touched >= QUESTIONS.length ? L('Tout revoir depuis le début', 'Review from the start') : L('Reprendre là où vous en étiez', 'Continue where you left off')}</a>
      </div>
      <div class="progress" style="margin:16px 0 6px"><span style="width:${(touched / QUESTIONS.length) * 100}%"></span></div>
      <p class="small faint" style="margin:0">${L(`${answered} répondues, ${touched - answered} passées. Vos réponses ne quittent jamais ce navigateur.`, `${answered} answered, ${touched - answered} skipped. Your answers never leave this browser.`)}</p>
    </div>
    <div class="card">
      <h3>${L('Par thème', 'By topic')}</h3>
      ${CATEGORIES.map((c) => {
        const done = c.questions.filter((q) => a[q.id] != null).length;
        const first = QUESTIONS.indexOf(c.questions.find((q) => a[q.id] == null) || c.questions[0]);
        return html`<div class="cat-progress"><a href="#/views?q=${first}">${catTitle(c)}</a><div class="progress"><span style="width:${(done / c.questions.length) * 100}%"></span></div><span class="small faint num">${done}/${c.questions.length}</span></div>`;
      })}
    </div>
    ${touched ? html`<details class="card"><summary style="cursor:pointer;font-weight:650">${L('Revoir et modifier mes réponses', 'Review and edit my answers')}</summary>
      <div class="stack" style="margin-top:14px">${CATEGORIES.map((c) => html`<div><div class="eyebrow" style="margin-bottom:6px">${catTitle(c)}</div><div class="answer-list">${c.questions.filter((q) => a[q.id] != null).map((q) => html`<a class="answer-row" href="#/views?q=${QUESTIONS.indexOf(q)}"><span>${qText(q)}</span><span class="answer-tag">${a[q.id] === 'skip' ? L('Passée', 'Skipped') : SCALE_LABEL[a[q.id]]}</span></a>`)}</div></div>`)}</div>
      <button type="button" class="btn btn-sm btn-ghost" id="clear-answers" style="margin-top:16px">${icon.trash()} ${L('Effacer toutes mes réponses', 'Clear all my answers')}</button>
    </details>` : ''}
  </div>`;
}

function districtsList(ad) {
  const s = STATE_BY_ABBR[ad.state];
  return html`<dl class="kv">
    <dt>${L('État', 'State')}</dt><dd>${s ? stateName(ad.state) : ad.state}</dd>
    ${ad.county ? html`<dt>${L('Comté', 'County')}</dt><dd>${ad.county}</dd>` : ''}
    <dt>${L('Chambre des représentants', 'U.S. House')}</dt><dd>${ad.cd ? ordinalCd(ad.cd) : L('Introuvable', 'Not found')}</dd>
    ${s && !s.noLegislature ? html`<dt>${chamberName(s.unicameral ? 'Legislature' : s.upper.name)}</dt><dd>${ad.sldu ? districtNo(ad.sldu) : L('Introuvable', 'Not found')}</dd>` : ''}
    ${s && s.lower ? html`<dt>${chamberName(s.lower.name)}</dt><dd>${ad.sldl ? districtNo(ad.sldl) : L('Introuvable', 'Not found')}</dd>` : ''}
  </dl>`;
}

function locationTab() {
  const ad = store.get().address;
  if (ad && ad.matched) {
    return html`<div class="stack">
      <div class="card">
        <div class="row between"><div><div class="eyebrow">${L('Adresse enregistrée', 'Saved address')}</div><h2 style="margin:4px 0 0;font-size:22px">${ad.matched}</h2></div>
          <a class="btn btn-primary" href="#/elections">${icon.ballot()} ${L('Voir mes élections', 'See my elections')}</a></div>
        <p class="small faint" style="margin:6px 0 16px">${L(`Trouvée par le Bureau du recensement des États-Unis le ${fmtDate(ad.savedAt)}. Enregistrée uniquement dans ce navigateur.`, `Matched by the U.S. Census Bureau on ${fmtDate(ad.savedAt)}. Stored only in this browser.`)}</p>
        ${districtsList(ad)}
        <div class="row" style="margin-top:18px"><button type="button" class="btn btn-sm" id="change-address">${L('Changer d’adresse', 'Change address')}</button><button type="button" class="btn btn-sm btn-ghost" id="remove-address">${icon.trash()} ${L('Supprimer mon adresse', 'Remove my address')}</button></div>
      </div>
      <div id="address-form-slot" hidden>${addressForm()}</div>
    </div>`;
  }
  return addressForm();
}

function addressForm() {
  const ad = store.get().address;
  return html`<form class="card stack" id="address-form" novalidate>
    <div><h2 style="margin:0">${L('Mon adresse', 'My location')}</h2><p class="muted" style="margin:4px 0 0">${L('Votre adresse complète indique exactement dans quelles circonscriptions vous votez. Le code postal seul ne suffit pas : beaucoup couvrent plusieurs circonscriptions du Congrès.', 'Your full street address tells us exactly which districts you vote in. ZIP codes alone can’t: many span more than one congressional district.')}</p></div>
    <div class="notice">${icon.info()}<div><b>${L('Comment votre adresse est utilisée.', 'How your address is used.')}</b> ${L('Elle est envoyée uniquement au géocodeur public et gratuit du Bureau du recensement des États-Unis pour trouver vos circonscriptions, puis enregistrée dans ce navigateur pour que vous n’ayez pas à la retaper. Informed Voter n’a pas de serveur et ne la reçoit jamais. Elle sert seulement à afficher les élections où vous pouvez voter.', 'It is sent only to the U.S. Census Bureau’s free public geocoder to find your districts, then saved in this browser so you don’t have to retype it. Informed Voter has no server and never receives it. It is used only to show the elections you can vote in.')}</div></div>
    <label class="check"><input type="checkbox" id="consent" ${ad?.consent ? 'checked' : ''}> <span>${L('J’accepte qu’Informed Voter utilise mon adresse uniquement pour trouver les élections de mon bulletin.', 'I agree to let Informed Voter use my address only to find the elections on my ballot.')}</span></label>
    <div class="field"><label for="addr">${L('Adresse du domicile', 'Home street address')}</label><input class="input" id="addr" name="addr" autocomplete="street-address" placeholder="123 Main St, Baton Rouge, LA 70802" value="${ad?.input || ''}"></div>
    <div class="row"><button class="btn btn-primary" type="submit" id="find-btn">${icon.pin()} ${L('Trouver mon adresse', 'Find my address')}</button><span class="small faint" id="addr-status" role="status"></span></div>
    <div id="suggestions" class="stack-sm"></div>
  </form>`;
}

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

export const profile = {
  title: () => L('Mon profil', 'My profile'),
  render(ctx) {
    const tab = ctx.query.tab === 'location' ? 'location' : 'views';
    return html`<div class="wrap page stack" style="max-width:960px">
      ${head()}
      <nav class="seg" aria-label="${L('Sections du profil', 'Profile sections')}"><a href="#/profile?tab=views" ${raw(tab === 'views' ? 'aria-current="page"' : '')}>${L('Mes opinions', 'My views')}</a><a href="#/profile?tab=location" ${raw(tab === 'location' ? 'aria-current="page"' : '')}>${L('Mon adresse', 'My location')}</a></nav>
      ${tab === 'views' ? viewsTab() : locationTab()}
    </div>`;
  },
  mount(root, ctx) {
    const file = root.querySelector('#avatar-file');
    file?.addEventListener('change', async () => {
      const f = file.files?.[0];
      if (!f || !f.type.startsWith('image/') || f.size > 15e6) return;
      try {
        store.set({ avatar: await shrinkImage(f) });
        window.dispatchEvent(new Event('iv:rerender'));
      } catch {
        alert(L('Cette image n’a pas pu être lue. Essayez un fichier JPG ou PNG.', 'That image could not be read. Try a JPG or PNG.'));
      }
    });
    root.querySelector('#avatar-reset')?.addEventListener('click', () => { store.set({ avatar: null }); window.dispatchEvent(new Event('iv:rerender')); });
    root.querySelector('#clear-answers')?.addEventListener('click', () => {
      if (confirm(L('Effacer toutes vos réponses à « Mes opinions » ? C’est définitif.', 'Clear all of your My views answers? This cannot be undone.'))) { store.set({ answers: {}, quizPos: 0 }); window.dispatchEvent(new Event('iv:rerender')); }
    });
    root.querySelector('#remove-address')?.addEventListener('click', () => {
      if (confirm(L('Supprimer l’adresse enregistrée dans ce navigateur ?', 'Remove your saved address from this browser?'))) { store.set({ address: null }); window.dispatchEvent(new Event('iv:rerender')); }
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
      const consent = form.querySelector('#consent').checked;
      const input = form.querySelector('#addr').value.trim();
      sugg.innerHTML = '';
      if (!consent) { status.textContent = L('Cochez d’abord la case de consentement.', 'Please tick the consent box first.'); return; }
      if (input.length < 8) { status.textContent = L('Saisissez votre adresse complète, avec la ville et l’État ou le code postal.', 'Enter your full street address, including city and state or ZIP code.'); return; }
      status.innerHTML = `<span class="spinner"></span> ${L('Interrogation du Bureau du recensement…', 'Asking the U.S. Census Bureau…')}`;
      try {
        const matches = (await geocode(input)).filter((m) => m.state && STATE_BY_ABBR[m.state]);
        if (!matches.length) {
          status.textContent = '';
          sugg.innerHTML = String(html`<div class="notice warn">${icon.info()}<div><b>${L('Aucune adresse trouvée.', 'No match found.')}</b> ${L('Vérifiez l’orthographe, indiquez la ville et l’État (ou le code postal) et retirez les numéros d’appartement. Une boîte postale ne peut pas être rattachée à une circonscription.', 'Check the spelling, include the city and state (or ZIP), and leave out apartment or unit numbers. P.O. boxes can’t be matched to a district.')}</div></div>`);
          return;
        }
        status.textContent = matches.length === 1 ? L('Nous avons trouvé cette adresse. Est-ce la vôtre ?', 'We found this address. Is it yours?') : L(`Nous avons trouvé ${matches.length} adresses possibles. Choisissez la vôtre :`, `We found ${matches.length} possible addresses. Pick yours:`);
        sugg.innerHTML = matches.map((m, i) => String(html`<button type="button" class="suggestion" data-i="${i}">${icon.pin()}<span><b>${m.matched}</b><br><span class="small faint">${m.county || ''}${m.cd ? ` · ${ordinalCd(m.cd)}` : ''}</span></span><span class="btn btn-sm" style="margin-left:auto">${L('Choisir', 'Use this')}</span></button>`)).join('');
        sugg.querySelectorAll('[data-i]').forEach((b) => b.addEventListener('click', () => {
          const m = matches[+b.dataset.i];
          store.set({ address: { ...m, consent: true, input, savedAt: new Date().toISOString() } });
          if (location.hash !== '#/profile?tab=location') location.hash = '#/profile?tab=location';
          else window.dispatchEvent(new Event('iv:rerender'));
        }));
      } catch (err) {
        status.textContent = err.message;
      }
    });
  },
};
