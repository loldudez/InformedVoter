// A person elected in 2026 or in office, on the U.S. state pages and the Congress page:
// photo, party, office and term, caucus, a short biography with its source, links, the
// documented positions behind "Compare with my views" (js/components/compare.js) and,
// for the 2026 federal and governor winners, the money their campaign raised (each filing
// line on its own, as on the race pages) beside their main opponent's total. Nothing here is inferred: a person with no documented
// position says so, and a seat not decided yet shows what is still open.

import { html, raw, fmtMoney, fmtDate, fmtPct } from '../util.js';
import { icon } from '../icons.js';
import { L, lang } from '../i18n.js';
import { questionsForLevel, stanceSentence } from '../data/questions.js';
import { hasFigures, resultRows, fc, financeOf } from '../data/world.js';
import { caucusOf } from '../data/holders.js';
import { MIN_COMPARED } from '../model/match.js';
import { stackedBar, cssVar } from '../lib/charts.js';
import { candBadge, lastName, FUNDING_PARTS, FUND_FR, fundColor, partyClass } from './race.js';
import { registerPerson, answeredAt } from './compare.js';

const PARTY = {
  D: ['Parti démocrate', 'Democrat'],
  R: ['Parti républicain', 'Republican'],
  I: ['Sans étiquette', 'Independent'],
  L: ['Parti libertarien', 'Libertarian'],
  G: ['Parti vert', 'Green'],
  N: ['Non partisan', 'Nonpartisan'],
};
export const partyLabel = (p) => (PARTY[p] ? L(...PARTY[p]) : p || L('Parti non indiqué', 'Party not listed'));
export const partyLetter = (p) => (p === 'D' || p === 'R' ? p : 'I');
// D blue, R red, everyone else the independents' gray, as on the Congress page.
export const personColor = (p) => cssVar(p === 'D' ? '--dem' : p === 'R' ? '--rep' : '--seat-other');

const MONTHS_FR = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre'];
// A date in the page's language: "Jan 3, 2021" or "3 janvier 2021"; a bare year stays one.
export function dateL(iso) {
  if (iso == null || iso === '') return '';
  const s = String(iso);
  if (/^\d{4}$/.test(s)) return s;
  const [y, m, d] = s.slice(0, 10).split('-').map(Number);
  if (!y || !m || !d) return s;
  if (lang() !== 'fr') return fmtDate(s.slice(0, 10));
  return `${d === 1 ? '1er' : d} ${MONTHS_FR[m - 1]} ${y}`;
}
// "$1.5M" or "1,5 M$".
export function moneyL(n) {
  if (lang() !== 'fr') return fmtMoney(n);
  const a = Math.abs(n);
  const f = (x, k) => x.toFixed(k).replace('.', ',');
  if (a >= 1e9) return `${f(n / 1e9, 1)} Md $`;
  if (a >= 1e6) return `${f(n / 1e6, a >= 1e7 ? 0 : 1)} M $`;
  if (a >= 1e3) return `${f(n / 1e3, a >= 1e5 ? 0 : 1)} k $`;
  return `${Math.round(n)} $`;
}
const pctL = (x, d) => (lang() === 'fr' ? `${Number(x).toFixed(d).replace('.', ',')} %` : fmtPct(x, d));
// A source's share of the total, keeping tiny and near-total shares' direction.
function shareL(value, total) {
  const pct = (value / total) * 100;
  if (pct > 0 && pct < 0.05) return lang() === 'fr' ? '<0,1 %' : '<0.1%';
  if (pct < 1) return pctL(pct, 1);
  if (pct > 99 && pct < 100) return lang() === 'fr' ? '>99 %' : '>99%';
  return pctL(pct, 0);
}


const ext = (href, label) => html`<a href="${href}" target="_blank" rel="noopener noreferrer">${label} ${icon.external()}</a>`;
const srcLink = (src) => (src?.url ? html`<a class="src-link" href="${src.url}" target="_blank" rel="noopener noreferrer" title="${src.title}">source ${icon.external()}</a>` : '');
const known = (p) => p && (p.status === 'elected' || p.status === 'holder');

// The caucus a member of Congress sits in, linked to the list it comes from.
function caucusChip(p) {
  if (p.office !== 'senate' && p.office !== 'house') return '';
  const seat = p.office === 'house' && p.district != null ? `${p.st}-${p.district}` : null;
  const d = caucusOf(p, { chamber: p.office, seat, sitting: p.status === 'holder' });
  if (!d) return '';
  const title = L(`D’après la liste des membres : ${d.name}`, `From the members list: ${d.name}`);
  return d.source?.url
    ? html`<a class="chip caucus-chip" href="${d.source.url}" target="_blank" rel="noopener noreferrer" title="${title}">${d.short}</a>`
    : html`<span class="chip caucus-chip" title="${title}">${d.short}</span>`;
}

function chips(p) {
  const out = [caucusChip(p)];
  if (p.flip) out.push(html`<span class="chip flip-chip" title="${L('Ce siège a changé de parti en 2026', 'This seat changed parties in 2026')}">${L('Siège gagné', 'Flipped seat')}</span>`);
  if (p.acting) out.push(html`<span class="chip">${L('Par intérim', 'Acting')}</span>`);
  if (p.appointed) out.push(html`<span class="chip">${L('Par nomination', 'Appointed')}</span>`);
  return out.filter(Boolean);
}

function termLine(p) {
  const bits = [];
  if (p.status === 'elected') {
    if (p.mateOf) bits.push(L(`Élection le 3 novembre 2026, sur le ticket de ${p.mateOf}`, `Elected Nov. 3, 2026 on ${p.mateOf}’s ticket`));
    else bits.push(p.incumbent ? L('Réélection le 3 novembre 2026', 'Re-elected Nov. 3, 2026') : L('Élection le 3 novembre 2026', 'Elected Nov. 3, 2026'));
    if (p.up) bits.push(L(`siège de nouveau en jeu en ${p.up}`, `seat next up in ${p.up}`));
  } else if (p.status === 'holder' && p.notUp) {
    bits.push(L('En fonction ; siège pas en jeu en 2026', 'In office; seat not on the 2026 ballot'));
  } else if (p.status === 'holder') {
    if (p.since) bits.push(L(`En fonction depuis le ${dateL(p.since)}`, `In office since ${dateL(p.since)}`));
    if (p.up) bits.push(L(`siège en jeu en ${p.up}`, `seat up in ${p.up}`));
    else if (p.termEnd) bits.push(L(`fin du mandat : ${p.termEnd}`, `term ends ${p.termEnd}`));
  }
  return bits.join(' · ');
}

// The strongest documented positions, and every other one a click away.
export function positionsBlock(p, level) {
  const qs = questionsForLevel(level);
  const pos = p.positions || {};
  const have = qs.filter((q) => pos[q.id] && pos[q.id].stance != null);
  if (!have.length) {
    return html`<p class="small faint" style="margin:0">${L('Aucune position documentée sur les questions du site pour l’instant, donc pas de comparaison possible.', 'No documented positions on the site’s questions yet, so there is nothing to compare.')}</p>`;
  }
  const who = lastName(p.name);
  const strongest = [...have].sort((a, b) => Math.abs(pos[b.id].stance) - Math.abs(pos[a.id].stance));
  const item = (q) => html`<li>${stanceSentence(who, q, pos[q.id].stance)}. ${srcLink(pos[q.id].source)}</li>`;
  // Since Nov. 27, 2026 positions can also come from bills the person sponsored or
  // cosponsored in Congress (kind "bill"), for questions no recorded vote answers.
  const bills = have.some((q) => pos[q.id].kind === 'bill');
  // Research first: a governor who served in Congress is a holder with votes cast and
  // research on top (Nov. 27, 2026), and would otherwise read "from recorded votes".
  const from = p.positionsFrom === 'research+votes'
    ? (bills ? L(' · d’après ses votes, les textes déposés ou cosignés et ses propres textes', ' · from recorded votes, bills they sponsored or cosponsored, and their own statements') : L(' · d’après ses votes et ses propres textes', ' · from recorded votes and their own statements'))
    : p.positionsFrom === 'research' ? L(' · d’après ses propres textes et actes', ' · from their own statements and acts')
    : p.positionsFrom === 'votes' || (p.votesCast && p.status === 'holder')
      ? (bills ? L(' · d’après ses votes enregistrés et les textes déposés ou cosignés', ' · from recorded votes and bills they sponsored or cosponsored') : L(' · d’après ses votes enregistrés', ' · from recorded votes'))
      : '';
  return html`<div class="person-pos">
    <div class="row between"><span class="eyebrow">${L('Positions documentées', 'Documented positions')}</span><span class="tiny faint">${L(`${have.length} question${have.length > 1 ? 's' : ''} sur ${qs.length}`, `${have.length} of ${qs.length} questions`)}${from}</span></div>
    <ul lang="en">${strongest.slice(0, 3).map(item)}</ul>
    ${have.length > 3 ? html`<details class="person-more"><summary>${L(`Voir les ${have.length} positions`, `See all ${have.length} positions`)}</summary><ul lang="en">${strongest.slice(3).map(item)}</ul></details>` : ''}
  </div>`;
}

// The runner-up in the count, or the forecast's main opponent where no count is posted.
function opponentOf(p) {
  const race = p.race;
  if (!race) return null;
  const row = resultRows(race).find((r) => !r.other && r.cand && r.cand.id !== p.candId);
  if (row) return { c: row.cand, counted: true };
  const f = fc(race);
  const c = [f.lead, f.second].find((x) => x && x.id !== p.candId);
  return c ? { c, counted: false } : null;
}

// What the main opponent raised, for scale beside the winner's own total.
function opponentLine(p) {
  const o = opponentOf(p);
  if (!o) return '';
  const fin = financeOf(o.c);
  const who = `${o.c.name} (${partyLetter(o.c.party)})`;
  const role = o.counted ? L('Deuxième place', 'Runner-up') : L('Principal adversaire', 'Main opponent');
  return html`<p class="tiny faint" style="margin:0">${hasFigures(fin)
    ? L(`${role} : ${who}, ${moneyL(fin.total)} levés`, `${role}: ${who} raised ${moneyL(fin.total)}`)
    : L(`${role} : ${who}, chiffres pas encore chargés`, `${role}: ${who}, figures not loaded yet`)}</p>`;
}

// What a 2026 winner's campaign raised, by the filing's own lines: the federal winners
// (FEC) and the governors (state filings, where the race page has them). Since Nov. 27 this
// is the only place the winners' money shows (owner's request: on the politician, not a
// menu page), with the main opponent's total beside it.
function moneyBlock(p) {
  // A member of Congress whose seat wasn't up: said, so both cards of a state keep one shape.
  if (p.status === 'holder' && (p.office === 'senate' || p.office === 'house')) {
    return html`<div class="person-money"><span class="eyebrow">${L('Campagne 2026 : argent levé', '2026 campaign money')}</span>
      <p class="small muted" style="margin:0">${L(`Pas sur le bulletin de 2026${p.up ? ` (siège en jeu en ${p.up})` : ''} : pas d’argent de campagne 2026 à montrer.`, `Not on the 2026 ballot${p.up ? ` (seat up in ${p.up})` : ''}, so there is no 2026 campaign money to show.`)}</p></div>`;
  }
  if (p.status !== 'elected' || (p.race?.level !== 'federal' && p.office !== 'governor')) return '';
  const fin = p.finance;
  if (p.office === 'governor' && !hasFigures(fin) && !fin?.note) return '';
  const fec = fin?.url ? ext(fin.url, fin.source && fin.source !== 'FEC' ? L('Source', 'Source') : 'FEC') : '';
  const head = html`<div class="row between"><span class="eyebrow">${L('Campagne 2026 : argent levé', '2026 campaign money')}</span><span class="tiny">${fec}</span></div>`;
  if (!hasFigures(fin)) {
    return html`<div class="person-money">${head}<p class="small muted" style="margin:0">${fin?.note ? html`<span lang="en">${fin.note}</span>` : L('Les chiffres de cette campagne ne sont pas encore chargés.', 'This campaign’s figures haven’t been loaded yet.')}</p>${opponentLine(p)}</div>`;
  }
  const parts = FUNDING_PARTS.map(([k, label], i) => ({ key: k, name: lang() === 'fr' ? FUND_FR[k] : label, value: fin.parts?.[k] || 0, color: fundColor(i) }))
    .filter((x) => x.value > 0);
  return html`<div class="person-money">
    ${head}
    <div class="money-figs">
      <div><b>${moneyL(fin.total)}</b><span>${L('levés', 'raised')}</span></div>
      ${fin.spent != null ? html`<div><b>${moneyL(fin.spent)}</b><span>${L('dépensés', 'spent')}</span></div>` : ''}
      ${fin.cashOnHand != null ? html`<div><b>${moneyL(fin.cashOnHand)}</b><span>${L('en caisse', 'cash on hand')}</span></div>` : ''}
    </div>
    ${parts.length ? raw(stackedBar(parts, { label: L(`Sources de financement : ${p.name}`, `${p.name} funding sources`) })) : ''}
    ${parts.length
      ? html`<ul class="money-key">${parts.map((x) => html`<li><i class="key-box" style="background:${x.color}"></i><span>${x.name}</span><b>${shareL(x.value, fin.total)}</b></li>`)}</ul>`
      : html`<p class="tiny faint" style="margin:0">${L('Pas encore de détail par type de donateur.', 'No breakdown by type of donor yet.')}</p>`}
    ${fin.asOf ? html`<p class="tiny faint" style="margin:0">${L(`Rapports jusqu’au ${dateL(fin.asOf)}`, `Reports through ${dateL(fin.asOf)}`)}</p>` : ''}
    ${opponentLine(p)}
  </div>`;
}

export function compareButton(p, level) {
  const qs = questionsForLevel(level);
  if (!qs.some((q) => p.positions?.[q.id]?.stance != null)) return '';
  if (answeredAt(level) >= MIN_COMPARED) {
    return html`<button type="button" class="btn btn-sm btn-primary" data-compare="${p.key}">${icon.user()} ${L('Comparer avec mes opinions', 'Compare with my views')}</button>`;
  }
  return html`<a class="btn btn-sm" href="#/views" title="${L(`Répondez d’abord à au moins ${MIN_COMPARED} questions`, `Answer at least ${MIN_COMPARED} questions first`)}">${icon.user()} ${L('Répondre d’abord à Mes opinions', 'Answer My views first')}</a>`;
}

// A seat whose 2026 race isn't decided yet: the runoff, the count, or a running mate the
// source doesn't name yet.
function pendingCard(p, eyebrow, raceLink) {
  const names = (p.advancing || []).map((c) => `${c.name} (${partyLetter(c.party)})`).join(L(' et ', ' and '));
  const line = p.status === 'runoff'
    ? L(`Second tour${p.date ? ` le ${dateL(p.date)}` : ''}${names ? ` : ${names}` : ''}.`, `Runoff${p.date ? ` on ${dateL(p.date)}` : ''}${names ? `: ${names}` : ''}.`)
    : p.status === 'mate-unknown'
      ? L(`Élection le 3 novembre 2026 sur le ticket de ${p.mateOf || 'la personne élue gouverneur'} ; la source ne donne pas encore le nom.`, `Elected Nov. 3, 2026 on ${p.mateOf ? `${p.mateOf}’s` : 'the governor-elect’s'} ticket; the source doesn’t name them yet.`)
      : p.status === 'no-result'
        ? L('La source ne donne pas encore de résultat pour cette élection du 3 novembre 2026.', 'The source hasn’t posted a result for this Nov. 3, 2026 race yet.')
        : p.leader
        ? L(`Pas encore proclamé : ${p.leader.name} (${partyLetter(p.leader.party)}) est en tête.`, `Not called yet: ${p.leader.name} (${partyLetter(p.leader.party)}) leads.`)
        : L('Pas encore proclamé.', 'Not called yet.');
  return html`<article class="card person-card pending">
    <div class="eyebrow">${eyebrow}</div>
    <h3 class="person-name">${p.status === 'runoff' ? L('Second tour à venir', 'Runoff ahead') : p.status === 'mate-unknown' ? L('Nom pas encore publié', 'Name not posted yet') : p.status === 'no-result' ? L('Pas encore de résultat publié', 'No result posted yet') : L('Pas encore décidé', 'Not decided yet')}</h3>
    <p class="small muted" style="margin:0">${line}</p>
    ${raceLink && p.raceId ? html`<div class="person-actions"><a class="btn btn-sm btn-ghost" href="#/race/${encodeURIComponent(p.raceId)}">${L('Voir l’élection', 'See the race')}</a></div>` : ''}
  </article>`;
}

// `level` picks the questions ('federal' or 'state'); `wide` lays the card out in two
// columns (the governor); `raceLink` adds the 2026 race's page.
export function personCard(p, { level, eyebrow = '', wide = false, raceLink = true } = {}) {
  if (!p) return '';
  if (!known(p)) return pendingCard(p, eyebrow, raceLink);
  const color = personColor(p.party);
  const sub = partyLabel(p.party);
  registerPerson(p.key, { person: p, level, color, sub: eyebrow ? `${sub} · ${eyebrow}` : sub });
  const site = p.site ? ext(p.site, L('Site web', 'Website')) : '';
  const wiki = p.wiki ? ext(p.wiki, 'Wikipedia') : '';
  const cs = chips(p);
  return html`<article class="card person-card ${partyClass(p.party)}${wide ? ' wide' : ''}">
    <div class="person-main">
      <div class="person-head">
        ${candBadge(p, color)}
        <div style="min-width:0">
          <div class="eyebrow">${eyebrow}</div>
          <h3 class="person-name">${p.name}</h3>
          <div class="person-sub">${sub}</div>
        </div>
      </div>
      ${cs.length ? html`<div class="person-chips">${cs}</div>` : ''}
      ${termLine(p) ? html`<p class="person-term">${termLine(p)}</p>` : ''}
      ${p.bio ? html`<p class="person-bio" lang="en">${p.bio}${p.bioFromWiki && p.wiki ? html` <span class="faint">(${L('Wikipédia, CC BY-SA', 'Wikipedia, CC BY-SA')})</span>` : ''}</p>` : ''}
      ${site || wiki ? html`<div class="person-links">${site}${wiki}</div>` : ''}
    </div>
    <div class="person-side">
      ${positionsBlock(p, level)}
      ${moneyBlock(p)}
      <div class="person-actions">
        ${compareButton(p, level)}
        ${raceLink && p.raceId ? html`<a class="btn btn-sm btn-ghost" href="#/race/${encodeURIComponent(p.raceId)}">${L('Résultats 2026', '2026 results')}</a>` : ''}
      </div>
    </div>
  </article>`;
}
