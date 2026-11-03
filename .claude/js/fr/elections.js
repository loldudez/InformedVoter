// Which elections ahead apply to a French address, and how to show their dates.
// The calendar (data/fr/calendrier.json) lists each election with the regions or
// departments it leaves out; a saved address carries its department and region codes.

import { html } from '../util.js';
import { L, lang } from '../i18n.js';
import { daysUntil, fmtDay, day } from './data.js';

export const electionName = (e) => e.name[lang()] || e.name.fr;
export const electionWhat = (e) => e.what[lang()] || e.what.fr;

export function appliesTo(e, ad) {
  if (!ad) return true;
  if (e.excludeRegs?.includes(ad.reg)) return false;
  if (e.excludeDeps?.includes(ad.dep)) return false;
  return true;
}

export function specialNote(e, ad) {
  const s = ad && (e.special?.[ad.reg] || e.special?.[ad.dep]);
  return s ? s[lang()] || s.fr : null;
}

// Elections without a fixed day sort at the start of their month.
const sortKey = (e) => e.date || `${e.month}-01`;

export function upcomingFor(cal, ad) {
  return cal.elections
    .filter((e) => appliesTo(e, ad) && (!e.date || daysUntil(e.round2 || e.date) >= 0))
    .sort((a, b) => sortKey(a).localeCompare(sortKey(b)));
}

export function monthLabel(ym) {
  const [y, m] = ym.split('-').map(Number);
  return new Date(y, m - 1, 1).toLocaleDateString(lang() === 'fr' ? 'fr-FR' : 'en-GB', { month: 'long', year: 'numeric' });
}

export function whenLabel(e) {
  if (!e.date) return L(`${monthLabel(e.month)} · jour pas encore fixé`, `${monthLabel(e.month)} · day not yet set`);
  const r1 = fmtDay(e.date, { weekday: true });
  if (e.status === 'latest') return L(`au plus tard le ${fmtDay(e.date)} (1er tour)`, `by ${fmtDay(e.date)} at the latest (round 1)`);
  return e.round2 ? L(`${r1} · 2nd tour le ${fmtDay(e.round2)}`, `${r1} · round 2 on ${fmtDay(e.round2)}`) : r1;
}

// A countdown tile: days for a fixed date, the month alone otherwise.
export function electionTile(e, { href = null } = {}) {
  const n = e.date ? daysUntil(e.date) : null;
  // Without a fixed day: months ahead, or years once it is more than two years off.
  const months = !e.date ? Math.max(0, Math.round((day(`${e.month}-01`) - new Date()) / (30.44 * 864e5))) : null;
  const years = months != null && months >= 24 ? Math.round(months / 12) : null;
  const body = html`<div class="fr-count small">
    <div class="num">${n != null ? (n > 0 ? n : L('Auj.', 'Today')) : `~${years ?? months}`}</div>
    <div class="lbl">${n != null ? L(n === 1 ? (e.status === 'latest' ? 'jour max.' : 'jour') : (e.status === 'latest' ? 'jours max.' : 'jours'), n === 1 ? 'day' : (e.status === 'latest' ? 'days at most' : 'days')) : years != null ? L('ans', 'years') : L('mois', 'months')}</div>
    <div class="what">${electionName(e)}</div>
    <div class="when faint">${e.date ? fmtDay(e.date) : monthLabel(e.month)}</div>
  </div>`;
  return href ? html`<a class="fr-next-item" href="${href}">${body}</a>` : html`<div class="fr-next-item">${body}</div>`;
}
