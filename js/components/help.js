// The floating help button, on every page of both sections: shortcuts to the main
// pages (filtered as you type), short answers to common questions, and a form to send
// a ticket (a question, an error on the site, a data correction).
//
// Tickets go to SUPPORT_EMAIL (js/config.js): sent by the site's mail service
// (MAIL_SERVICE_URL, services/mail/Code.gs) once it is set up, else through the
// visitor's email app, filled in. If the service fails, the form offers the email app
// instead; with no address at all, it offers to copy the ticket. Technical details (the
// page, the browser, the site's last few error messages) are attached only if the
// visitor ticks the box.

import { html } from '../util.js';
import { icon } from '../icons.js';
import { L, section } from '../i18n.js';
import { SUPPORT_EMAIL, MAIL_SERVICE_URL, REMINDER_FROM } from '../config.js';

// The site's own recent errors, kept in memory for an error report.
const errors = [];
const keep = (msg) => { errors.push(`${new Date().toISOString()} ${msg}`.slice(0, 300)); if (errors.length > 5) errors.shift(); };
window.addEventListener('error', (e) => keep(`${e.message} (${(e.filename || '').split('/').pop()}:${e.lineno})`));
window.addEventListener('unhandledrejection', (e) => keep(`Promise: ${e.reason?.message || e.reason}`));

const SHORTCUTS = () => (section() === 'fr' ? [
  ['#/fr', L('Accueil et carte de France', 'Home and map of France'), 'globe'],
  ['#/fr/presidentielle', L('Présidentielle 2027 : sondages du premier tour', '2027 presidential: first-round polls'), 'ballot'],
  ['#/fr/presidentielle?tour=2', L('Second tour : les duels testés', 'Second round: match-ups tested'), 'ballot'],
  ['#/fr/presidentielle?tour=c', L('Les candidats', 'The candidates'), 'user'],
  ['#/fr/profil/opinions', L('Répondre au questionnaire (Mon profil, Mes opinions)', 'Answer the questionnaire (My profile, My views)'), 'check'],
  ['#/fr/elections/comparer', L('Comparer les candidats avec mes opinions', 'Compare the candidates with my views'), 'user'],
  ['#/fr/profil?onglet=localisation', L('Ajouter ou changer mon adresse', 'Add or change my address'), 'pin'],
  ['#/fr/elections', L('Mes élections et mes rappels', 'My elections and reminders'), 'bell'],
  ['#/fr/calendrier', L('Les prochaines élections', 'Upcoming elections'), 'calendar'],
  ['#/fr/partis', L('Les partis et leurs valeurs', 'Parties and values'), 'user'],
  ['#/fr/enjeux', L('Les grands enjeux : économie, inflation, immigration, salaires…', 'Major issues: economy, inflation, immigration, salaries…'), 'chart'],
  ['#/fr/a-propos', L('D’où viennent les données', 'Where the data comes from'), 'info'],
  ['#/country', L('Changer de pays', 'Change country'), 'globe'],
] : [
  ['#/', L('Carte des élections américaines', 'Homepage map'), 'globe'],
  ['#/elections', L('Mes élections (bulletin, rappels)', 'My elections (ballot, reminders)'), 'ballot'],
  ['#/views', L('Mes opinions : le questionnaire', 'My views questionnaire'), 'check'],
  ['#/profile?tab=location', L('Ajouter ou changer mon adresse', 'Add or change my address'), 'pin'],
  ['#/close', L('Élections serrées', 'Close elections'), 'ballot'],
  ['#/parties', L('Les partis et leurs valeurs', 'Parties and values'), 'user'],
  ['#/news', L('Actualités', 'News'), 'news'],
  ['#/about', L('D’où viennent les données', 'Where the data comes from'), 'info'],
  ['#/country', L('Changer de pays', 'Change country'), 'globe'],
]);

const FAQ = () => [
  [L('Mes réponses sont-elles envoyées quelque part ?', 'Are my answers sent anywhere?'),
    L('Non. Vos réponses, votre adresse et vos choix restent dans ce navigateur. Votre adresse n’est envoyée qu’au service public de géocodage, après votre accord, pour trouver vos élections. Seul ce que vous choisissez d’envoyer en sort : un ticket d’aide, ou votre e-mail si vous vous inscrivez aux rappels.', 'No. Your answers, address and choices stay in this browser. Your address goes only to the public geocoder, after you agree, to find your elections. Only what you choose to send leaves it: a help ticket, or your email address if you sign up for reminders.')],
  [L('Pourquoi certains candidats n’ont pas de score d’affinité ?', 'Why do some candidates have no match score?'),
    L('Une position n’est jamais devinée : il faut une source. Sans au moins cinq questions documentées en commun, aucun pourcentage n’est affiché.', 'A position is never guessed: it needs a source. Without at least five documented questions in common, no percentage is shown.')],
  [L('D’où viennent les sondages ?', 'Where do the polls come from?'),
    L('Des sondages publiés, chacun relié à sa source : la Commission des sondages en France, l’institut ou le média aux États-Unis.', 'Published polls, each linked to its source: the Commission des sondages in France, the pollster or outlet in the United States.')],
  [L('Comment recevoir un rappel avant une élection ?', 'How do I get a reminder before an election?'),
    MAIL_SERVICE_URL
      ? L(`Dans « Mes élections » ou le calendrier, cliquez sur « Me le rappeler » et choisissez un mois, deux semaines ou une semaine avant : dans votre agenda (fichier .ics) ou par e-mail, envoyé par ${REMINDER_FROM} une fois votre inscription confirmée.`, `In “My elections” or the calendar, click “Remind me” and pick a month, two weeks or a week before: in your calendar (an .ics file) or by email from ${REMINDER_FROM}, once you confirm your sign-up.`)
      : L('Dans « Mes élections » ou le calendrier, cliquez sur « Me le rappeler » et choisissez un mois, deux semaines ou une semaine avant : l’élection s’ajoute à votre agenda (fichier .ics). Les rappels par e-mail arrivent bientôt.', 'In “My elections” or the calendar, click “Remind me” and pick a month, two weeks or a week before: the election goes into your calendar (an .ics file). Email reminders are coming soon.')],
];

// Search ignores case and accents: "elections" finds "Élections".
const fold = (s) => String(s).normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();

const KINDS = () => [
  ['question', L('Une question', 'A question')],
  ['bug', L('Une erreur sur le site', 'An error on the site')],
  ['data', L('Une donnée à corriger', 'Data to correct')],
  ['other', L('Autre chose', 'Something else')],
];

function panel(tab) {
  const delivery = MAIL_SERVICE_URL && SUPPORT_EMAIL ? 'post' : SUPPORT_EMAIL ? 'mail' : 'none';
  return html`<div class="help-panel card" role="dialog" aria-modal="false" aria-labelledby="help-title">
    <div class="row between"><h2 id="help-title" style="margin:0;font-size:20px">${L('Besoin d’aide ?', 'Need help?')}</h2>
      <button type="button" class="toggle-icon" data-help-close aria-label="${L('Fermer l’aide', 'Close help')}">${icon.close()}</button></div>
    <nav class="seg" aria-label="${L('Aide', 'Help')}"><button type="button" data-help-tab="go" aria-pressed="${String(tab === 'go')}">${L('Aller à', 'Go to')}</button><button type="button" data-help-tab="faq" aria-pressed="${String(tab === 'faq')}">${L('Questions', 'Questions')}</button><button type="button" data-help-tab="ticket" aria-pressed="${String(tab === 'ticket')}">${L('Ticket', 'Ticket')}</button></nav>
    ${tab === 'go' ? html`<div class="stack-sm">
      <label class="sr-only" for="help-q">${L('Chercher une page', 'Search for a page')}</label>
      <div class="help-search">${icon.search()}<input class="input" id="help-q" type="search" placeholder="${L('Que cherchez-vous ?', 'What are you looking for?')}" autocomplete="off"></div>
      <div class="help-links">${SHORTCUTS().map(([href, label, ic]) => html`<a href="${href}" data-help-link data-label="${fold(label)}">${icon[ic]()}<span>${label}</span></a>`)}</div>
      <p class="small faint" data-help-empty hidden style="margin:0">${L('Rien trouvé. Essayez un autre mot, ou envoyez-nous un ticket.', 'Nothing found. Try another word, or send us a ticket.')}</p>
    </div>` : ''}
    ${tab === 'faq' ? html`<div class="stack-sm">${FAQ().map(([q, a]) => html`<details class="help-faq"><summary>${q}</summary><p class="small muted">${a}</p></details>`)}</div>` : ''}
    ${tab === 'ticket' ? html`<form class="stack-sm" data-help-form novalidate>
      <div class="field"><label for="help-kind">${L('C’est à propos de', 'This is about')}</label>
        <select class="input" id="help-kind">${KINDS().map(([v, label]) => html`<option value="${v}">${label}</option>`)}</select></div>
      <div class="field"><label for="help-msg">${L('Votre message', 'Your message')}</label>
        <textarea class="input" id="help-msg" rows="4" required placeholder="${L('Décrivez la question ou l’erreur. Pour une erreur : ce que vous faisiez et ce qui s’est passé.', 'Describe the question or error. For an error: what you were doing and what happened.')}"></textarea></div>
      <div class="field"><label for="help-email">${L('Votre e-mail, pour une réponse (facultatif)', 'Your email, for a reply (optional)')}</label>
        <input class="input" id="help-email" type="email" autocomplete="email"></div>
      <label class="check"><input type="checkbox" id="help-tech" checked> <span class="small">${L('Joindre la page, le navigateur et les dernières erreurs du site (aucune réponse ni adresse)', 'Attach the page, browser and the site’s latest errors (no answers or address)')}</span></label>
      ${delivery === 'none' ? html`<div class="notice warn small">${icon.info()}<div>${L('L’envoi des tickets n’est pas encore relié à une adresse de support. Vous pouvez copier votre ticket en attendant.', 'Tickets aren’t connected to a support address yet. You can copy your ticket for now.')}</div></div>`
        : html`<p class="small faint" style="margin:0">${L('Les tickets arrivent à', 'Tickets go to')} <a href="mailto:${SUPPORT_EMAIL}">${SUPPORT_EMAIL}</a>.</p>`}
      <div class="row">
        ${delivery === 'none'
          ? html`<button type="submit" class="btn btn-sm btn-primary" data-help-copy>${L('Copier le ticket', 'Copy the ticket')}</button>`
          : html`<button type="submit" class="btn btn-sm btn-primary">${icon.send()} ${delivery === 'mail' ? L('Ouvrir dans ma messagerie', 'Open in my email app') : L('Envoyer le ticket', 'Send the ticket')}</button>`}
        <span class="small faint" role="status" data-help-status></span>
      </div>
    </form>` : ''}
  </div>`;
}

function ticketText(form) {
  const kind = KINDS().find(([v]) => v === form.querySelector('#help-kind').value)?.[1] || '';
  const msg = form.querySelector('#help-msg').value.trim();
  const email = form.querySelector('#help-email').value.trim();
  const lines = [`[Informed Voter] ${kind}`, '', msg, ''];
  if (email) lines.push(`Reply to: ${email}`);
  if (form.querySelector('#help-tech').checked) {
    lines.push(`Page: ${location.href}`, `Language: ${document.documentElement.lang}`, `Browser: ${navigator.userAgent}`,
      `Screen: ${window.innerWidth}x${window.innerHeight}`, `Time: ${new Date().toISOString()}`);
    if (errors.length) lines.push('Recent errors:', ...errors);
  }
  return { kind, msg, email, text: lines.join('\n') };
}

export function mountHelp() {
  const host = document.createElement('div');
  host.className = 'help-root';
  document.body.appendChild(host);
  let open = false, tab = 'go';
  const draw = () => {
    host.innerHTML = `${open ? String(panel(tab)) : ''}<button type="button" class="help-fab" aria-expanded="${String(open)}" aria-label="${open ? L('Fermer l’aide', 'Close help') : L('Aide', 'Help')}">${open ? icon.close() : icon.help()}<span>${L('Aide', 'Help')}</span></button>`;
    if (open) (host.querySelector('#help-q') || host.querySelector('#help-kind') || host.querySelector('summary'))?.focus();
  };
  host.addEventListener('click', (e) => {
    if (e.target.closest('.help-fab')) { open = !open; draw(); if (!open) host.querySelector('.help-fab').focus(); return; }
    if (e.target.closest('[data-help-close]')) { open = false; draw(); host.querySelector('.help-fab').focus(); return; }
    const t = e.target.closest('[data-help-tab]');
    if (t) { tab = t.dataset.helpTab; draw(); return; }
    if (e.target.closest('[data-help-link]')) { open = false; setTimeout(draw, 0); }
  });
  host.addEventListener('input', (e) => {
    if (e.target.id !== 'help-q') return;
    const q = fold(e.target.value.trim());
    let shown = 0;
    host.querySelectorAll('[data-help-link]').forEach((a) => { const on = !q || a.dataset.label.includes(q); a.hidden = !on; shown += on; });
    host.querySelector('[data-help-empty]').hidden = shown > 0;
  });
  host.addEventListener('submit', async (e) => {
    e.preventDefault();
    const form = e.target.closest('[data-help-form]');
    if (!form) return;
    const status = form.querySelector('[data-help-status]');
    const t = ticketText(form);
    if (!t.msg) { status.textContent = L('Écrivez d’abord votre message.', 'Write your message first.'); form.querySelector('#help-msg').focus(); return; }
    const mailto = `mailto:${SUPPORT_EMAIL}?subject=${encodeURIComponent(`[Informed Voter] ${t.kind}`)}&body=${encodeURIComponent(t.text)}`;
    if (MAIL_SERVICE_URL && SUPPORT_EMAIL) {
      const button = form.querySelector('button[type=submit]');
      status.textContent = L('Envoi…', 'Sending…');
      button.disabled = true;
      try {
        // text/plain keeps this a "simple" request: Apps Script can't answer a CORS preflight.
        const res = await fetch(MAIL_SERVICE_URL, { method: 'POST', headers: { 'Content-Type': 'text/plain;charset=utf-8' }, signal: AbortSignal.timeout?.(30000),
          body: JSON.stringify({ type: 'ticket', subject: `[Informed Voter] ${t.kind}`, message: t.text, email: t.email || undefined }) });
        const r = res.ok ? await res.json() : {};
        if (!r.ok) throw new Error(r.error || String(res.status));
        form.reset();
        status.textContent = L('Merci ! Votre ticket est envoyé.', 'Thank you! Your ticket was sent.');
      } catch {
        status.innerHTML = String(html`${L('L’envoi a échoué.', 'Sending failed.')} <a href="${mailto}">${L('L’envoyer depuis ma messagerie', 'Send it from my email app')}</a>`);
      }
      button.disabled = false;
    } else if (SUPPORT_EMAIL) {
      location.href = mailto;
      status.textContent = L('Votre messagerie s’ouvre avec le ticket rempli.', 'Your email app opens with the ticket filled in.');
    } else {
      try {
        await navigator.clipboard.writeText(t.text);
        status.textContent = L('Ticket copié.', 'Ticket copied.');
      } catch {
        // No clipboard access: show the ticket, selected, to copy by hand.
        status.textContent = L('Copiez le texte ci-dessous :', 'Copy the text below:');
        let box = form.querySelector('[data-help-copybox]');
        if (!box) {
          box = document.createElement('textarea');
          box.className = 'input';
          box.rows = 6;
          box.readOnly = true;
          box.setAttribute('data-help-copybox', '');
          form.appendChild(box);
        }
        box.value = t.text;
        box.focus();
        box.select();
      }
    }
  });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && open) { open = false; draw(); host.querySelector('.help-fab').focus(); } });
  window.addEventListener('iv:lang', draw);
  window.addEventListener('hashchange', () => { if (open) draw(); });
  draw();
}
