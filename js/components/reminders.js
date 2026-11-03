// Election reminders, in "My elections" and the France calendar. A visitor picks
// how far ahead to be reminded (a month, two weeks and/or a week) and gets:
//   * a calendar file (.ics) with an alert at each of those times, which works today
//     in any calendar app and stores nothing anywhere but the visitor's own calendar;
//   * email reminders from REMINDER_FROM, through the site's mail service
//     (MAIL_SERVICE_URL in js/config.js, services/mail/Code.gs), for the elections listed
//     in data/reminders.json. The address is sent only after the visitor ticks the
//     consent box, and nothing more is mailed until they confirm by email. Until the
//     service is set up, the email form is shown as coming soon and no address is
//     collected.
// The choices themselves are saved in this browser, in the section's own store.

import { html, raw, fetchJSON } from '../util.js';
import { icon } from '../icons.js';
import { L, lang } from '../i18n.js';
import { store } from '../store.js';
import { frStore } from '../fr/store.js';
import { MAIL_SERVICE_URL, REMINDER_FROM } from '../config.js';

const LEADS = [['30', 'Un mois avant', 'A month before'], ['14', 'Deux semaines avant', 'Two weeks before'], ['7', 'Une semaine avant', 'A week before']];

const storeFor = (section) => (section === 'fr' ? frStore : store);
// The U.S. section is in English; the France section follows the visitor's language.
const tx = (section, fr, en) => (section === 'fr' ? L(fr, en) : en);
const saved = (e) => (storeFor(e.section).get().reminders || {})[e.id];

// The elections the mail service sends reminders for (null when the list can't be read:
// the service then answers for itself).
let covered = null;
const coveredIds = () => (covered = covered || fetchJSON('data/reminders.json').then((j) => new Set(Object.keys(j.elections || {})), () => null));

// The mail service's refusals, in words.
const SIGNUP_ERRORS = {
  'too-many': ['Trop de demandes pour le moment. Réessayez dans quelques heures.', 'Too many requests for now. Please try again in a few hours.'],
  'no-dates': ['Les dates de rappel choisies sont toutes passées.', 'The reminder dates you chose have all passed.'],
  'unknown-election': ['Les rappels par e-mail ne sont pas proposés pour cette élection.', 'Email reminders aren’t offered for this election.'],
  quota: ['Le site a atteint sa limite d’envois pour aujourd’hui. Réessayez demain.', 'The site has reached its sending limit for today. Please try again tomorrow.'],
  'bad-request': ['Vérifiez votre adresse e-mail.', 'Please check your email address.'],
};

// e: { id, name, date: 'YYYY-MM-DD' | null, month: 'YYYY-MM' | null, date2?, name2?, url?, section: 'us' | 'fr' }
export function reminderButton(e) {
  const on = !!saved(e);
  return html`<button type="button" class="btn btn-sm${on ? '' : ' btn-ghost'}" data-remind="${JSON.stringify(e)}" aria-pressed="${String(on)}">${on ? icon.bellFill() : icon.bell()} ${on ? tx(e.section, 'Rappels choisis', 'Reminders set') : tx(e.section, 'Me le rappeler', 'Remind me')}</button>`;
}

const ymd = (s) => { const [y, m, d] = s.split('-').map(Number); return new Date(y, m - 1, d); };
const today = () => { const n = new Date(); return new Date(n.getFullYear(), n.getMonth(), n.getDate()); };
const addDays = (d, n) => new Date(d.getFullYear(), d.getMonth(), d.getDate() + n);
const fmt = (d, section) => d.toLocaleDateString(section === 'fr' && lang() === 'fr' ? 'fr-FR' : 'en-US', { day: 'numeric', month: 'long', year: 'numeric' });

// RFC 5545: escape text, fold nothing (lines stay short), CRLF line ends.
const icsText = (s) => String(s).replace(/\\/g, '\\\\').replace(/;/g, '\\;').replace(/,/g, '\\,').replace(/\n/g, '\\n');
const icsDate = (d) => `${d.getFullYear()}${String(d.getMonth() + 1).padStart(2, '0')}${String(d.getDate()).padStart(2, '0')}`;

export function icsFor(e, leads) {
  const stamp = new Date().toISOString().replace(/[-:]/g, '').replace(/\.\d+Z$/, 'Z');
  const events = [[e.date, e.name], ...(e.date2 ? [[e.date2, e.name2 || e.name]] : [])];
  const lines = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Informed Voter//Election reminders//EN', 'CALSCALE:GREGORIAN', 'METHOD:PUBLISH'];
  for (const [d, name] of events) {
    const day = ymd(d);
    lines.push('BEGIN:VEVENT', `UID:${e.id.replace(/[^\w-]/g, '-')}-${icsDate(day)}@informed-voter`, `DTSTAMP:${stamp}`,
      `DTSTART;VALUE=DATE:${icsDate(day)}`, `DTEND;VALUE=DATE:${icsDate(addDays(day, 1))}`, `SUMMARY:${icsText(name)}`,
      `DESCRIPTION:${icsText(tx(e.section, 'Rappel d’Informed Voter. Vérifiez votre bureau de vote et les horaires auprès de votre mairie.', 'Reminder from Informed Voter. Check your polling place and hours with your local election office.'))}`);
    if (e.url) lines.push(`URL:${e.url}`);
    for (const lead of leads) {
      if (addDays(day, -lead) < today()) continue;
      lines.push('BEGIN:VALARM', 'ACTION:DISPLAY', `DESCRIPTION:${icsText(name)}`, `TRIGGER:-P${lead}D`, 'END:VALARM');
    }
    lines.push('END:VEVENT');
  }
  lines.push('END:VCALENDAR');
  return lines.join('\r\n') + '\r\n';
}

// mail: 'off' (no mail service yet), 'unset' (no fixed day yet), 'past' (every reminder
// date has passed) or 'on'.
function emailPart(e, mail) {
  const s = e.section;
  const note = (fr, en) => html`<p class="small muted" style="margin:0">${tx(s, fr, en)}</p>`;
  if (mail === 'off') return note('Les rappels par e-mail arrivent bientôt : le site n’a pas encore de service d’envoi. Aucune adresse n’est demandée d’ici là.', 'Email reminders are coming soon: the site doesn’t have a sending service yet. No address is asked for until then.');
  const signed = saved(e)?.email ? note('Une inscription par e-mail a été faite depuis ce navigateur. Pour arrêter les rappels : le lien en bas de chaque e-mail.', 'An email sign-up was made from this browser. To stop the reminders, use the link at the bottom of any email.') : '';
  if (mail === 'unset') return html`${signed}${note('Proposés dès que le jour de l’élection sera officiellement fixé.', 'Offered once the election day is officially set.')}`;
  if (mail === 'past') return html`${signed}${note('Toutes les dates de rappel de cette élection sont passées.', 'All the reminder dates for this election have passed.')}`;
  return html`${signed}<p class="small muted" style="margin:0">${tx(s, 'Envoyés par', 'Sent from')} <b>${REMINDER_FROM}</b>. ${tx(s, 'Un premier e-mail vous demande de confirmer : rien d’autre n’est envoyé avant.', 'A first email asks you to confirm: nothing else is sent until you do.')}</p>
    <div class="field"><label for="rem-email">${tx(s, 'Adresse e-mail', 'Email address')}</label><input class="input" id="rem-email" type="email" autocomplete="email" required></div>
    <label class="check"><input type="checkbox" id="rem-consent" required> <span class="small">${tx(s, 'J’accepte qu’Informed Voter garde mon adresse e-mail pour m’envoyer ces rappels, puis l’efface une fois l’élection passée. Je peux me désinscrire depuis chaque e-mail.', 'I agree that Informed Voter keeps my email address to send me these reminders, and deletes it once the election is over. I can unsubscribe from any email.')}</span></label>
    <p class="small faint" style="margin:0">${tx(s, 'L’adresse est gardée dans le compte Google du site (une feuille Google Sheets) et ne sert à rien d’autre.', 'The address is kept in the site’s Google account (a Google Sheets file) and used for nothing else.')} <a href="${s === 'fr' ? '#/fr/a-propos' : '#/about'}" data-close-modal>${tx(s, 'Confidentialité', 'Privacy')}</a></p>
    <div class="row"><button type="submit" class="btn btn-sm btn-primary">${icon.send()} ${tx(s, 'M’inscrire aux rappels', 'Sign me up')}</button><span class="small faint" role="status" data-rem-status></span></div>`;
}

function dialog(e, mail) {
  const s = e.section;
  const mine = saved(e)?.leads || ['30', '14', '7'];
  const exact = !!e.date;
  const opts = LEADS.map(([n, fr, en]) => {
    const when = exact ? addDays(ymd(e.date), -n) : null;
    const past = when && when < today();
    return html`<label class="check${past ? ' faint' : ''}"><input type="checkbox" name="lead" value="${n}" ${raw(mine.includes(n) && !past ? 'checked' : '')} ${raw(past ? 'disabled' : '')}>
      <span>${tx(s, fr, en)}${when ? html` <span class="small faint">· ${past ? tx(s, 'déjà passé', 'already passed') : fmt(when, s)}</span>` : ''}</span></label>`;
  });
  return html`<div class="modal-backdrop" data-close-modal>
    <div class="modal card stack" role="dialog" aria-modal="true" aria-labelledby="rem-title">
      <div class="row between"><div><div class="eyebrow">${tx(s, 'Rappels', 'Reminders')}</div><h2 id="rem-title" style="margin:4px 0 0;font-size:22px">${e.name}</h2>
        <div class="small muted">${exact ? fmt(ymd(e.date), s) : tx(s, 'Le jour exact n’est pas encore fixé.', 'The exact day isn’t set yet.')}</div></div>
        <button type="button" class="toggle-icon" data-close-modal aria-label="${tx(s, 'Fermer', 'Close')}">${icon.close()}</button></div>
      <fieldset class="stack-sm" style="border:0;padding:0;margin:0"><legend class="small" style="font-weight:650;margin-bottom:6px">${tx(s, 'Me rappeler cette élection :', 'Remind me about this election:')}</legend>${opts}</fieldset>
      <div class="card tight stack-sm" style="background:var(--surface-2)">
        <div class="row" style="gap:8px">${icon.calendar()}<b>${tx(s, 'Dans mon agenda', 'In my calendar')}</b></div>
        <p class="small muted" style="margin:0">${exact
          ? tx(s, 'Un fichier .ics à ouvrir avec Google Agenda, Apple Calendrier ou Outlook : l’élection s’ajoute avec une alerte à chaque date cochée. Rien n’est envoyé à personne.', 'An .ics file for Google Calendar, Apple Calendar or Outlook: the election is added with an alert on each date you ticked. Nothing is sent to anyone.')
          : tx(s, 'Disponible dès que le jour de l’élection sera fixé.', 'Available once the election day is set.')}</p>
        <div><button type="button" class="btn btn-sm" data-rem-ics ${raw(exact ? '' : 'disabled')}>${icon.calendar()} ${tx(s, 'Ajouter à mon agenda (.ics)', 'Add to my calendar (.ics)')}</button></div>
      </div>
      <form class="card tight stack-sm" data-rem-email style="background:var(--surface-2)">
        <div class="row" style="gap:8px">${icon.send()}<b>${tx(s, 'Par e-mail', 'By email')}</b>${mail === 'off' ? html`<span class="chip" style="padding:2px 9px;font-size:12px">${tx(s, 'Bientôt', 'Coming soon')}</span>` : ''}</div>
        ${emailPart(e, mail)}
      </form>
      <div class="row between"><span class="small faint">${tx(s, 'Vos choix restent dans ce navigateur.', 'Your choices stay in this browser.')}</span>
        <div class="row">${saved(e) ? html`<button type="button" class="btn btn-sm btn-ghost" data-rem-clear>${icon.trash()} ${tx(s, 'Retirer', 'Remove')}</button>` : ''}<button type="button" class="btn btn-sm btn-primary" data-rem-save>${icon.check()} ${tx(s, 'Enregistrer mes choix', 'Save my choices')}</button></div></div>
    </div>
  </div>`;
}

async function openReminder(e, opener) {
  let mail = 'off';
  if (MAIL_SERVICE_URL) {
    const ids = e.date ? await coveredIds() : null;
    mail = !e.date || (ids && !ids.has(e.id)) ? 'unset'
      : LEADS.some(([n]) => addDays(ymd(e.date), -n) >= today()) ? 'on' : 'past';
  }
  const root = document.getElementById('overlay-root');
  root.innerHTML = String(dialog(e, mail));
  const modal = root.querySelector('.modal');
  const leads = () => [...modal.querySelectorAll('input[name=lead]:checked')].map((i) => i.value);
  const close = () => { root.innerHTML = ''; document.removeEventListener('keydown', onKey); opener?.focus(); };
  const onKey = (ev) => { if (ev.key === 'Escape') close(); };
  document.addEventListener('keydown', onKey);
  root.querySelector('.modal-backdrop').addEventListener('click', (ev) => { if (ev.target.hasAttribute('data-close-modal') || ev.target.closest('button[data-close-modal]')) close(); });
  const st = storeFor(e.section);
  modal.querySelector('[data-rem-save]').addEventListener('click', () => {
    st.set({ reminders: { ...(st.get().reminders || {}), [e.id]: { ...saved(e), leads: leads(), savedAt: new Date().toISOString() } } });
    close();
  });
  modal.querySelector('[data-rem-clear]')?.addEventListener('click', () => {
    const r = { ...(st.get().reminders || {}) };
    delete r[e.id];
    st.set({ reminders: r });
    close();
  });
  modal.querySelector('[data-rem-ics]')?.addEventListener('click', () => {
    const blob = new Blob([icsFor(e, leads().map(Number))], { type: 'text/calendar;charset=utf-8' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `${e.id.replace(/[^\w-]+/g, '-')}.ics`;
    document.body.appendChild(a);
    a.click();
    setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 1000);
  });
  modal.querySelector('[data-rem-email]').addEventListener('submit', async (ev) => {
    ev.preventDefault();
    const input = modal.querySelector('#rem-email');
    if (!input) return;
    const status = modal.querySelector('[data-rem-status]');
    const button = ev.target.querySelector('button[type=submit]');
    const email = input.value.trim();
    const chosen = leads();
    if (!chosen.length) { status.textContent = tx(e.section, 'Cochez au moins une date ci-dessus.', 'Tick at least one date above.'); return; }
    if (!modal.querySelector('#rem-consent').checked || !email) { status.textContent = tx(e.section, 'Cochez la case d’accord et indiquez votre e-mail.', 'Tick the consent box and enter your email.'); return; }
    status.textContent = tx(e.section, 'Envoi…', 'Sending…');
    button.disabled = true;
    try {
      // text/plain keeps this a "simple" request: Apps Script can't answer a CORS preflight.
      const res = await fetch(MAIL_SERVICE_URL, { method: 'POST', headers: { 'Content-Type': 'text/plain;charset=utf-8' }, signal: AbortSignal.timeout?.(30000),
        body: JSON.stringify({ type: 'reminder', email, election: e.id, leads: chosen.map(Number), lang: e.section === 'fr' ? lang() : 'en', consent: true }) });
      const r = res.ok ? await res.json() : { error: String(res.status) };
      if (!r.ok) throw new Error(r.error || 'server');
      st.set({ reminders: { ...(st.get().reminders || {}), [e.id]: { leads: chosen, email: true, savedAt: new Date().toISOString() } } });
      status.textContent = tx(e.section, 'Presque fini : ouvrez l’e-mail que nous venons d’envoyer et confirmez.', 'Almost done: open the email we just sent and confirm.');
    } catch (err) {
      const msg = SIGNUP_ERRORS[err.message];
      status.textContent = msg ? tx(e.section, ...msg) : tx(e.section, 'L’inscription n’a pas abouti. Réessayez plus tard.', 'Sign-up failed. Please try again later.');
      button.disabled = false;
    }
  });
  modal.querySelector('input:not([disabled]), button')?.focus();
}

let wired = false;
export function wireReminders() {
  if (wired) return;
  wired = true;
  document.addEventListener('click', (ev) => {
    const b = ev.target.closest('[data-remind]');
    if (!b) return;
    let e;
    try { e = JSON.parse(b.dataset.remind); } catch (err) { console.error(err); return; }
    openReminder(e, b).catch((err) => console.error(err));
  });
}
