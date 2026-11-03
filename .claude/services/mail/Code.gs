/**
 * Informed Voter's mail service: email reminders before elections, and help tickets.
 *
 * A Google Apps Script web app run by caissonez@informedvoter.io (Google Workspace), so
 * every reminder is sent from that address. The site (MAIL_SERVICE_URL in js/config.js)
 * posts two kinds of request, as JSON in a text/plain body so browsers send them without
 * a CORS preflight, which Apps Script can't answer:
 *
 *   {type: "reminder", email, election, leads, lang, consent: true}
 *     Stores the sign-up in a Google Sheet and emails a confirmation link. Reminders go
 *     only to confirmed addresses (double opt-in), at the chosen lead times (30, 14 and/or
 *     7 days before each round), each with an unsubscribe link.
 *   {type: "ticket", subject, message, email}
 *     Forwards a help ticket to HELP_TO, with the visitor's address as Reply-To.
 *
 * Election names and dates come from the site's own data/reminders.json, never from the
 * request, so nobody can make this address send text of their choosing. Sign-ups are
 * deleted once the election is over, on unsubscribing, and after 7 days unconfirmed.
 * Confirming and unsubscribing take a button press on the linked page, so a mail
 * scanner that opens links does neither.
 *
 * Setup (README.md, "Email reminders and help tickets"): signed in as
 * caissonez@informedvoter.io, paste this file and appsscript.json into a new Apps Script
 * project, run setup() once, deploy it as a web app (execute as me, anyone can access)
 * and put its /exec address in js/config.js.
 */

const SITE_URL = 'https://www.informedvoter.io/';
const HELP_TO = 'theinformedvoter.help@gmail.com';
const FROM_NAME = 'Informed Voter';
const LEADS = [30, 14, 7];
const GRACE_DAYS = 2;    // a reminder held up by a failed daily run still goes out this late
const PENDING_DAYS = 7;  // unconfirmed sign-ups are deleted after this
// One row per address and election. "next" holds a confirmed sign-up's new choices
// ("14 7|fr") until the confirmation link is used.
const HEAD = ['token', 'email', 'election', 'leads', 'lang', 'status', 'created', 'confirmed', 'sent', 'lastDate', 'next'];
const LIMITS = { signupsPerEmail: 5, signupsPerHour: 100, ticketsPerHour: 20, ticketsPerEmail: 5 };
const HOW_TO_VOTE = {
  us: 'https://vote.gov/',
  fr: 'https://www.service-public.fr/particuliers/vosdroits/services-en-ligne-et-formulaires/ISE',
};

const DAYS = {
  fr: ['dimanche', 'lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi'],
  en: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
};
const MONTHS = {
  fr: ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre'],
  en: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
};
const LEAD_TEXT = { fr: { 30: 'un mois', 14: 'deux semaines', 7: 'une semaine' }, en: { 30: 'a month', 14: 'two weeks', 7: 'a week' } };
const NB = ' ';  // French puts a narrow no-break space before : ; ? !

// Requests from the site ---------------------------------------------------------------

function doPost(e) {
  let req;
  try {
    req = JSON.parse((e && e.postData && e.postData.contents) || '{}');
  } catch (err) {
    return json_({ ok: false, error: 'bad-request' });
  }
  if (!req || typeof req !== 'object') return json_({ ok: false, error: 'bad-request' });
  rememberUrl_();
  try {
    if (req.type === 'reminder') return json_(signup_(req));
    if (req.type === 'ticket') return json_(ticket_(req));
  } catch (err) {
    console.error(err);
    return json_({ ok: false, error: 'server' });
  }
  return json_({ ok: false, error: 'bad-request' });
}

function signup_(req) {
  const email = cleanEmail_(req.email);
  if (!email || req.consent !== true) return { ok: false, error: 'bad-request' };
  const id = String(req.election || '');
  const el = elections_()[id];
  if (!el) return { ok: false, error: 'unknown-election' };
  const lang = el.section === 'fr' && req.lang === 'fr' ? 'fr' : 'en';
  const today = today_();
  // Only lead times still ahead for some round.
  const leads = [...new Set((Array.isArray(req.leads) ? req.leads : []).map(Number))]
    .filter((n) => LEADS.includes(n) && el.rounds.some((r) => addDays_(r.date, -n) >= today))
    .sort((a, b) => b - a);
  if (!leads.length) return { ok: false, error: 'no-dates' };
  if (!allow_('e:' + email, LIMITS.signupsPerEmail, 21600) || !allow_('g:signups', LIMITS.signupsPerHour, 3600)) return { ok: false, error: 'too-many' };
  if (MailApp.getRemainingDailyQuota() < 10) return { ok: false, error: 'quota' };
  const lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    const sh = sheet_();
    const rows = values_(sh);
    const i = rows.findIndex((r, k) => k > 0 && r[1] === email && r[2] === id);
    const now = new Date().toISOString();
    const rec = i > 0 ? fromRow_(rows[i])
      : { token: Utilities.getUuid(), email: email, election: id, leads: [], lang: lang, status: 'pending', created: now, confirmed: '', sent: [], last: '', next: '' };
    // A change to a confirmed sign-up waits for the same confirmation link as a new one,
    // and the answer is the same either way, so nobody learns who has signed up.
    if (rec.status === 'confirmed') rec.next = leads.join(' ') + '|' + lang;
    else Object.assign(rec, { leads: leads, lang: lang, created: now });
    rec.last = el.rounds[el.rounds.length - 1].date;
    write_(sh, i > 0 ? i + 1 : rows.length + 1, [toRow_(rec)]);
    sendConfirm_(email, el, lang, rec.token, leads);
    return { ok: true, status: 'pending' };
  } finally {
    lock.releaseLock();
  }
}

function ticket_(req) {
  const message = String(req.message || '').replace(/\r\n?/g, '\n').trim().slice(0, 8000);
  if (!message) return { ok: false, error: 'bad-request' };
  const subject = String(req.subject || '[Informed Voter] Ticket').replace(/\s+/g, ' ').trim().slice(0, 150);
  const email = cleanEmail_(req.email);
  if (!allow_('g:tickets', LIMITS.ticketsPerHour, 3600)) return { ok: false, error: 'too-many' };
  if (email && !allow_('t:' + email, LIMITS.ticketsPerEmail, 3600)) return { ok: false, error: 'too-many' };
  if (MailApp.getRemainingDailyQuota() < 5) return { ok: false, error: 'quota' };
  const mail = { to: HELP_TO, subject: subject, body: message, name: 'Informed Voter help form' };
  if (email) mail.replyTo = email;
  MailApp.sendEmail(mail);
  return { ok: true };
}

// Confirm and unsubscribe links ---------------------------------------------------------

function doGet(e) {
  rememberUrl_();
  const p = (e && e.parameter) || {};
  const a = p.a === 'confirm' || p.a === 'unsub' ? p.a : '';
  if (!a) return ContentService.createTextOutput('Informed Voter mail service');
  const token = String(p.t || '');
  return page_(a, token, lookup_(token));
}

// Read only: what the page's button will act on.
function lookup_(token) {
  if (!token) return null;
  const r = values_(sheet_()).find((x, k) => k > 0 && x[0] === token);
  if (!r) return null;
  let el = null;
  try {
    el = elections_()[r[2]] || null;
  } catch (err) {
    el = null;
  }
  return { lang: r[4] === 'fr' ? 'fr' : 'en', status: r[5], next: !!r[10], el: el };
}

// Called by the page's button (google.script.run).
function act(action, token) {
  token = String(token || '');
  if ((action !== 'confirm' && action !== 'unsub') || !token) return { state: 'missing' };
  const lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    const sh = sheet_();
    const rows = values_(sh);
    const i = rows.findIndex((r, k) => k > 0 && r[0] === token);
    if (i < 1) return { state: 'missing' };
    if (action === 'unsub') {
      sh.getRange(i + 1, 1, 1, HEAD.length).clearContent();  // the daily run closes the gap
      return { state: 'unsubscribed' };
    }
    const rec = fromRow_(rows[i]);
    if (rec.next) {
      const [leads, lang] = rec.next.split('|');
      rec.leads = leads.split(' ').map(Number).filter((n) => LEADS.includes(n));
      rec.lang = lang === 'fr' ? 'fr' : 'en';
      rec.next = '';
    }
    if (rec.status !== 'confirmed') rec.confirmed = new Date().toISOString();
    rec.status = 'confirmed';
    write_(sh, i + 1, [toRow_(rec)]);
    return { state: 'confirmed' };
  } finally {
    lock.releaseLock();
  }
}

function page_(a, token, info) {
  const lang = info ? info.lang : 'en';
  const fr = lang === 'fr';
  const what = info && info.el ? list_(info.el.rounds.map((r) => `${roundName_(r, lang)} (${fmtDay_(r.date, lang)})`), lang) : '';
  let title = 'Informed Voter';
  let text = `Ce lien n’est plus valable${NB}: le rappel a peut-être déjà été supprimé. This link is no longer valid: the reminder may already have been removed.`;
  let button = '';
  let done = '';
  if (info && a === 'confirm') {
    title = fr ? 'Confirmer vos rappels' : 'Confirm your reminders';
    text = fr ? `Rappels par e-mail avant${NB}: ${what}.` : `Email reminders before: ${what}.`;
    done = fr ? 'C’est confirmé. Chaque rappel contient un lien pour vous désinscrire.' : 'Confirmed. Every reminder has a link to unsubscribe.';
    if (info.status === 'confirmed' && !info.next) text += ' ' + done;
    else button = fr ? 'Confirmer mes rappels' : 'Confirm my reminders';
  } else if (info) {
    title = fr ? 'Se désinscrire' : 'Unsubscribe';
    text = fr ? `Ne plus recevoir de rappels avant${NB}: ${what}.` : `Stop the reminders before: ${what}.`;
    button = fr ? 'Me désinscrire' : 'Unsubscribe me';
    done = fr ? `C’est fait${NB}: votre adresse est effacée pour cette élection.` : 'Done: your address is deleted for this election.';
  }
  const data = JSON.stringify({ a: a, t: token, done: done, fail: fr ? 'Cela n’a pas marché. Réessayez plus tard.' : 'That didn’t work. Please try again later.' })
    .replace(/</g, '\\u003c');
  const html = `<!doctype html><html lang="${lang}"><head><meta charset="utf-8"><style>
    body{font:16px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif;margin:0;padding:32px 16px;color:#1b1a22;background:#f6f5fa}
    main{max-width:560px;margin:0 auto;background:#fff;border-radius:14px;padding:24px;box-shadow:0 1px 3px rgba(0,0,0,.08)}
    h1{font-size:22px;margin:0 0 12px}button{font:inherit;font-weight:600;padding:10px 16px;border:0;border-radius:10px;background:#5b3fd6;color:#fff;cursor:pointer}
    button[disabled]{opacity:.6;cursor:default}a{color:#5b3fd6}</style></head>
    <body><main><h1>${esc_(title)}</h1><p>${esc_(text)}</p>
    ${button ? `<p><button id="go" type="button">${esc_(button)}</button></p><p id="out" role="status"></p>` : ''}
    <p><a href="${SITE_URL}" target="_top">Informed Voter</a></p></main>
    <script>
      const D = ${data};
      const b = document.getElementById('go');
      const out = (s) => { document.getElementById('out').textContent = s; };
      if (b) b.onclick = () => {
        b.disabled = true;
        google.script.run
          .withSuccessHandler((r) => { if (r && r.state !== 'missing') { out(D.done); b.remove(); } else out(D.fail); })
          .withFailureHandler(() => { b.disabled = false; out(D.fail); })
          .act(D.a, D.t);
      };
    </script></body></html>`;
  return HtmlService.createHtmlOutput(html).setTitle(title).addMetaTag('viewport', 'width=device-width, initial-scale=1');
}

// The daily run -------------------------------------------------------------------------

// setup() schedules this every day at 14:00, Paris time (8:00 in New York).
function sendDueReminders() {
  runReminders_(today_());
}

function runReminders_(today) {
  const els = elections_();  // the site unreachable: nothing is sent or deleted; GRACE_DAYS covers it
  const lock = LockService.getScriptLock();
  lock.waitLock(30000);
  try {
    const sh = sheet_();
    const rows = values_(sh);
    const keep = [HEAD];
    let sent = 0;
    let dropped = 0;
    for (const r of rows.slice(1)) {
      if (!r[0]) continue;  // unsubscribed
      const rec = fromRow_(r);
      const el = els[rec.election];
      if (el) rec.last = el.rounds[el.rounds.length - 1].date;
      const over = rec.last && rec.last < today;
      const unconfirmed = rec.status !== 'confirmed' && addDays_(rec.created.slice(0, 10), PENDING_DAYS) < today;
      if (over || unconfirmed) {
        dropped++;
        continue;
      }
      if (rec.status === 'confirmed' && el) {
        for (const due of dueNow_(el, rec, today)) {
          if (due.send) {
            if (MailApp.getRemainingDailyQuota() < 1) continue;  // tried again tomorrow
            try {
              sendReminder_(rec, el, due);
              sent++;
            } catch (err) {
              console.error(`${rec.election} ${due.round.date}: ${err}`);  // a refused address isn't retried
            }
          }
          rec.sent.push(...due.keys);
        }
      }
      keep.push(toRow_(rec));
    }
    sh.clearContents();
    write_(sh, 1, keep);
    console.log(`${sent} reminders sent, ${dropped} sign-ups deleted, ${keep.length - 1} kept`);
  } finally {
    lock.releaseLock();
  }
}

// For each round still ahead, the lead times whose day has come and that weren't sent:
// the latest of them is mailed if it is at most GRACE_DAYS late and, for a second round,
// falls after the first round; all of them are then marked as handled, so a round never
// gets two emails on one day, or a stale one later.
function dueNow_(el, rec, today) {
  const out = [];
  el.rounds.forEach((r, i) => {
    if (r.date <= today) return;
    const due = rec.leads.map((n) => ({ day: addDays_(r.date, -n), key: r.date + '/' + n }))
      .filter((d) => d.day <= today && !rec.sent.includes(d.key));
    if (!due.length) return;
    const latest = due.reduce((x, y) => (x.day > y.day ? x : y)).day;
    const prev = i ? el.rounds[i - 1].date : '';
    out.push({ round: r, days: daysBetween_(today, r.date), keys: due.map((d) => d.key), send: addDays_(latest, GRACE_DAYS) >= today && latest > prev });
  });
  return out;
}

// Emails --------------------------------------------------------------------------------

function sendConfirm_(email, el, lang, token, leads) {
  const fr = lang === 'fr';
  const url = serviceUrl_() + '?a=confirm&t=' + encodeURIComponent(token);
  const rounds = list_(el.rounds.map((r) => `${roundName_(r, lang)} (${fmtDay_(r.date, lang)})`), lang);
  const when = list_(leads.map((n) => LEAD_TEXT[lang][n]), lang);
  send_(email, fr ? 'Confirmez vos rappels d’élection' : 'Confirm your election reminders', fr ? [
    `Vous avez demandé à Informed Voter de vous écrire ${when} avant${NB}: ${rounds}.`,
    '',
    `Pour confirmer, ouvrez ce lien${NB}: ${url}`,
    '',
    `Si vous n’avez rien demandé, ignorez ce message${NB}: rien d’autre ne vous sera envoyé, et une adresse non confirmée est effacée sous ${PENDING_DAYS} jours.`,
  ] : [
    `You asked Informed Voter to email you ${when} before: ${rounds}.`,
    '',
    `To confirm, open this link: ${url}`,
    '',
    `If you didn’t ask for this, ignore this email: nothing more will be sent, and an unconfirmed address is deleted within ${PENDING_DAYS} days.`,
  ]);
}

function sendReminder_(rec, el, due) {
  const lang = rec.lang === 'fr' && el.section === 'fr' ? 'fr' : 'en';
  const fr = lang === 'fr';
  const name = roundName_(due.round, lang);
  const day = fmtDay_(due.round.date, lang);
  const n = due.days;
  const page = SITE_URL + el.page;
  const stop = serviceUrl_() + '?a=unsub&t=' + encodeURIComponent(rec.token);
  send_(rec.email, fr ? `${name}${NB}: dans ${n} jour${n > 1 ? 's' : ''}` : `${name}: ${n} day${n > 1 ? 's' : ''} to go`, fr ? [
    `${name}${NB}: ${day}, dans ${n} jour${n > 1 ? 's' : ''}.`,
    '',
    `Vérifiez votre inscription et votre bureau de vote${NB}: ${HOW_TO_VOTE.fr}`,
    `L’élection sur Informed Voter${NB}: ${page}`,
    '',
    `Vous recevez ce message parce que vous avez demandé ce rappel sur Informed Voter. Pour ne plus en recevoir${NB}: ${stop}`,
  ] : [
    `${name}: ${day}, ${n} day${n > 1 ? 's' : ''} from now.`,
    '',
    el.section === 'us'
      ? `Check your registration, polling place and hours at ${HOW_TO_VOTE.us} or with your state’s election office.`
      : `Check your registration and polling station: ${HOW_TO_VOTE.fr}`,
    `${el.section === 'us' ? 'Your elections' : 'The election'} on Informed Voter: ${page}`,
    '',
    `You’re getting this because you asked for this reminder on Informed Voter. To stop: ${stop}`,
  ]);
}

// Plain text, plus the same text as simple HTML with its links clickable.
function send_(to, subject, lines) {
  const body = lines.join('\n');
  const htmlBody = body.split('\n\n').map((p) => `<p style="margin:0 0 14px">${esc_(p).replace(/\n/g, '<br>')
    .replace(/(https:\/\/[^\s<]+)/g, '<a href="$1">$1</a>')}</p>`).join('');
  MailApp.sendEmail({ to: to, subject: subject, body: body, name: FROM_NAME,
    htmlBody: `<div style="font:15px/1.5 Arial,sans-serif;color:#1b1a22;max-width:560px">${htmlBody}</div>` });
}

// Setup, storage and helpers ------------------------------------------------------------

// Run once from the editor: creates the sign-ups sheet (in this account's Drive) and the
// daily trigger. Running it again keeps the sheet and replaces the trigger.
function setup() {
  const props = PropertiesService.getScriptProperties();
  let ss = null;
  const id = props.getProperty('SHEET_ID');
  if (id) {
    try {
      ss = SpreadsheetApp.openById(id);
    } catch (err) {
      ss = null;
    }
  }
  if (!ss) {
    ss = SpreadsheetApp.create('Informed Voter: email reminder sign-ups');
    props.setProperty('SHEET_ID', ss.getId());
  }
  const sh = ss.getSheets()[0];
  sh.setName('signups');
  if (!sh.getRange(1, 1).getValue()) write_(sh, 1, [HEAD]);
  sh.setFrozenRows(1);
  for (const t of ScriptApp.getProjectTriggers()) {
    if (t.getHandlerFunction() === 'sendDueReminders') ScriptApp.deleteTrigger(t);
  }
  ScriptApp.newTrigger('sendDueReminders').timeBased().everyDays(1).atHour(14).create();
  console.log('Sign-ups sheet: ' + ss.getUrl());
  console.log('Emails this account can still send today: ' + MailApp.getRemainingDailyQuota());
}

function sheet_() {
  const id = PropertiesService.getScriptProperties().getProperty('SHEET_ID');
  if (!id) throw new Error('Run setup() once first.');
  return SpreadsheetApp.openById(id).getSheets()[0];
}

function values_(sh) {
  return sh.getDataRange().getValues().map((r) => HEAD.map((h, k) => cell_(r[k])));
}

// Rows are written as plain text, so Sheets never turns a date or "7" into something else.
function write_(sh, top, rows) {
  const more = top + rows.length - 1 - sh.getMaxRows();
  if (more > 0) sh.insertRowsAfter(sh.getMaxRows(), more);
  sh.getRange(top, 1, rows.length, HEAD.length).setNumberFormat('@').setValues(rows);
}

function cell_(v) {
  if (v instanceof Date) return Utilities.formatDate(v, 'UTC', "yyyy-MM-dd'T'HH:mm:ss'Z'");
  return v == null ? '' : String(v);
}

function fromRow_(r) {
  return { token: r[0], email: r[1], election: r[2], leads: r[3].split(' ').map(Number).filter((n) => LEADS.includes(n)), lang: r[4],
    status: r[5], created: r[6], confirmed: r[7], sent: r[8].split(' ').filter(Boolean), last: r[9].slice(0, 10), next: r[10] };
}

function toRow_(x) {
  return [x.token, x.email, x.election, x.leads.join(' '), x.lang, x.status, x.created, x.confirmed, x.sent.join(' '), x.last, x.next];
}

// The elections the site offers reminders for, from its own data/reminders.json (built by
// scripts/update_reminders.py), kept six hours.
function elections_() {
  const cache = CacheService.getScriptCache();
  const hit = cache.get('elections');
  if (hit) return JSON.parse(hit);
  const res = UrlFetchApp.fetch(SITE_URL + 'data/reminders.json', { muteHttpExceptions: true });
  if (res.getResponseCode() !== 200) throw new Error('data/reminders.json answered ' + res.getResponseCode());
  const all = JSON.parse(res.getContentText()).elections || {};
  const ok = {};
  for (const id of Object.keys(all)) {
    const e = all[id];
    if (/^(us|fr):[\w-]+$/.test(id) && (e.section === 'us' || e.section === 'fr') && /^#\//.test(e.page || '')
      && Array.isArray(e.rounds) && e.rounds.length
      && e.rounds.every((r) => /^\d{4}-\d{2}-\d{2}$/.test(r.date) && r.name && (r.name.en || r.name.fr))) ok[id] = e;
  }
  cache.put('elections', JSON.stringify(ok), 21600);
  return ok;
}

function allow_(key, max, seconds) {
  const cache = CacheService.getScriptCache();
  const n = Number(cache.get(key) || 0);
  if (n >= max) return false;
  cache.put(key, String(n + 1), seconds);
  return true;
}

function cleanEmail_(s) {
  s = String(s || '').trim().toLowerCase();
  return s.length <= 254 && /^[^\s@<>()",;:\\]+@[^\s@<>()",;:\\]+\.[a-z][a-z0-9-]+$/.test(s) ? s : '';
}

function rememberUrl_() {
  const url = ScriptApp.getService().getUrl();
  const props = PropertiesService.getScriptProperties();
  if (url && /\/exec$/.test(url) && props.getProperty('URL') !== url) props.setProperty('URL', url);
}

function serviceUrl_() {
  return PropertiesService.getScriptProperties().getProperty('URL') || ScriptApp.getService().getUrl();
}

function json_(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
}

function esc_(s) {
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function roundName_(r, lang) {
  return r.name[lang] || r.name.en || r.name.fr;
}

function list_(items, lang) {
  return items.length < 2 ? items.join('') : `${items.slice(0, -1).join(', ')} ${lang === 'fr' ? 'et' : 'and'} ${items[items.length - 1]}`;
}

function fmtDay_(ymd, lang) {
  const d = new Date(ymd + 'T12:00:00Z');
  const n = d.getUTCDate();
  const w = DAYS[lang][d.getUTCDay()];
  const m = MONTHS[lang][d.getUTCMonth()];
  return lang === 'fr' ? `${w} ${n === 1 ? '1er' : n} ${m} ${d.getUTCFullYear()}` : `${w}, ${m} ${n}, ${d.getUTCFullYear()}`;
}

function today_() {
  return Utilities.formatDate(new Date(), Session.getScriptTimeZone(), 'yyyy-MM-dd');
}

function addDays_(ymd, n) {
  const d = new Date(ymd + 'T00:00:00Z');
  d.setUTCDate(d.getUTCDate() + n);
  return d.toISOString().slice(0, 10);
}

function daysBetween_(a, b) {
  return Math.round((Date.parse(b + 'T00:00:00Z') - Date.parse(a + 'T00:00:00Z')) / 864e5);
}
