// Building blocks shared by the France pages.

import { html, raw, initials } from '../util.js';
import { icon } from '../icons.js';
import { L } from '../i18n.js';
import { partyColor, partyKey, fmtNum, fmtPctFr, daysUntil, fmtDay, fmtSourceDate, photoSrc, candById, pollDates } from './data.js';

// A candidate's photo in gray, blended into the page, with the photographer's credit
// (Commons licenses require it) in its tooltip; initials when there is no photo.
export function candPhoto(c, { size = 56, cls = '' } = {}) {
  const src = photoSrc(c);
  const credit = c?.photo ? `${L('Photo', 'Photo')} : ${c.photo.artist || L('auteur inconnu', 'unknown author')} (${c.photo.license || 'Wikimedia Commons'})` : '';
  return html`<span class="fr-photo ${cls}" style="--size:${size}px;--pc:${partyColor(c?.party)}" title="${credit}">${src
    ? html`<img src="${src}" alt="" loading="lazy" decoding="async">`
    : html`<span class="fr-initials">${initials(c?.name || '?')}</span>`}</span>`;
}

// The party's Wikipedia article title without its disambiguation: "(parti politique)",
// "(France)" or a founding year ("Union populaire républicaine (2007)").
export const partyName = (c) => (c?.partyName || '').replace(/\s*\((?:parti[^)]*|France|politique|\d{4})\)\s*$/i, '');

export function partyChip(c) {
  if (!c?.party && !c?.partyName) return '';
  return html`<span class="fr-party"><i style="background:${partyColor(c.party)}"></i>${c.party || partyName(c)}</span>`;
}

export function countdown(iso, { label, small = false } = {}) {
  const n = daysUntil(iso);
  return html`<div class="fr-count${small ? ' small' : ''}">
    <div class="num">${n > 0 ? n : n === 0 ? L('Aujourd’hui', 'Today') : '—'}</div>
    <div class="lbl">${n > 0 ? L(n === 1 ? 'jour' : 'jours', n === 1 ? 'day' : 'days') : ''}</div>
    ${label ? html`<div class="what">${label}</div>` : ''}
    <div class="when faint">${fmtDay(iso, { weekday: true })}</div>
  </div>`;
}

// Horizontal bars of the first-round poll average, in each candidate's party color.
export function averageBars(pres, rows, { max = null } = {}) {
  const top = max ?? Math.max(...rows.map((r) => r.avg.hi), 10);
  const n = (x) => fmtNum(x, x % 1 ? 1 : 0);
  return html`<div class="fr-bars" role="list">${rows.map((r) => html`<div class="fr-bar-row" role="listitem">
    ${candPhoto(r, { size: 40 })}
    <div class="mid">
      <div class="who"><b><a href="#/fr/candidat/${r.id}">${r.name}</a></b>${partyChip(r)}</div>
      <div class="track" aria-hidden="true">
        <span class="range" style="left:${(r.avg.lo / top) * 100}%;width:${Math.max(0.6, ((r.avg.hi - r.avg.lo) / top) * 100)}%"></span>
        <span class="fill" style="width:${(r.avg.avg / top) * 100}%;background:${partyColor(r.party)}"></span>
      </div>
    </div>
    <div class="val num">${fmtPctFr(r.avg.avg)}<span class="tiny faint" title="${L('Du sondage le plus bas au plus haut', 'Lowest to highest poll')}">${n(r.avg.lo)}–${n(r.avg.hi)}</span></div>
  </div>`)}</div>`;
}

// One second-round match-up as a two-sided bar, with its average and poll count.
export function duelCard(duel, pres, { current = true } = {}) {
  const a = candById(pres, duel.a), b = candById(pres, duel.b);
  const av = duel.average;
  const last = duel.polls[0];
  const side = (c, v) => html`<div class="duel-row">${candPhoto(c, { size: 40 })}<div class="who"><b>${c.name}</b>${partyChip(c)}</div><div class="pct num">${fmtPctFr(v)}</div></div>`;
  return html`<div class="fr-duel${current ? '' : ' stale'}">
    ${side(a, av.a)}${side(b, av.b)}
    <div class="duel-bar" aria-hidden="true"><span style="width:${av.a}%;background:${partyColor(a.party)}"></span><span style="width:${av.b}%;background:${partyColor(b.party)}"></span></div>
    <div class="tiny faint">${av.polls > 1
      ? L(`Moyenne de ${av.polls} sondages publiés du ${fmtDay(av.from, { year: false })} au ${fmtDay(av.to)}`, `Average of ${av.polls} polls published ${fmtDay(av.from, { year: false })} to ${fmtDay(av.to)}`)
      : L(`Un seul sondage récent : ${last.pollster}, ${last.dates}`, `One recent poll: ${last.pollster}, ${pollDates(last.dates)}`)}${duel.absent ? L(' · candidat absent du premier tour', ' · includes someone not running') : ''}${current ? '' : L(' · pas testé depuis plus de deux mois', ' · not tested in over two months')}</div>
  </div>`;
}

export const sourceLink = (url, label) => html`<a class="src-link" href="${url}" target="_blank" rel="noopener noreferrer">${label || L('source', 'source')} ${icon.external()}</a>`;

// The news report a person's candidacy, or its absence, was checked against
// (scripts/fr/candidats_2027.py), with the article's title in the tooltip.
export function candidacySource(c, label = L('Candidature :', 'Candidacy:')) {
  const s = c?.statusSource;
  if (!s?.url) return '';
  return html`<a class="src-link" href="${s.url}" target="_blank" rel="noopener noreferrer" title="${s.title}">${label ? `${label} ` : ''}${s.outlet}, ${fmtSourceDate(s.date)} ${icon.external()}</a>`;
}

export const pkey = partyKey;
export { raw };
