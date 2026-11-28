// The 2028 presidential field: everyone who has declared, formed an exploratory committee
// or said publicly they're weighing a run (the owner's choice, Nov. 25, 2026), from
// data/president-2028.json (scripts/update_president_2028.py: Wikipedia's 2028 primaries
// pages, read every day). #/2028 opens on three doors, Democrats in blue, Republicans in red,
// independents and other parties in gray (owner's request, Nov. 27), each leading to that
// party's page (#/2028/D, #/2028/R, #/2028/other). Each person has their photo, status,
// office, a summary of their Wikipedia article, what they've said about 2028 with the news
// reports cited for it, their website, and their positions, from their recorded votes and
// from scripts/research/president_2028.py (their own platforms, statements and official
// acts), with "Compare with my views" (js/components/compare.js). Nothing is inferred: no
// polls or odds this early, and no position without a source.

import { html, fetchJSON } from '../util.js';
import { icon } from '../icons.js';
import { L } from '../i18n.js';
import { stateName } from '../data/states.js';
import { photoOf } from '../data/world.js';
import { candBadge, photoCredits, partyClass } from '../components/race.js';
import { dateL, personColor, positionsBlock, compareButton } from '../components/person.js';
import { registerPerson, wireCompare } from '../components/compare.js';

let cache = null;
async function load() {
  try { cache = cache || await fetchJSON('data/president-2028.json'); } catch { cache = null; }
  return cache;
}

const STATUS = {
  declared: ['Candidature déclarée', 'Declared'],
  exploratory: ['Comité exploratoire', 'Exploratory committee'],
  interest: ['Intérêt exprimé', 'Expressed interest'],
};
const GROUP = {
  D: ['Démocrates', 'Democrats'],
  R: ['Républicains', 'Republicans'],
  other: ['Indépendants et autres partis', 'Independents and other parties'],
};
const GROUP_IDS = Object.keys(GROUP);
const CTA = {
  D: ['Voir les démocrates', 'See the Democrats'],
  R: ['Voir les républicains', 'See the Republicans'],
  other: ['Voir les indépendants et autres partis', 'See independents and other parties'],
};
const hasPositions = (p) => Object.values(p.positions || {}).some((x) => x.stance != null);
// "A, B and C" / "A, B et C".
const listOf = (names) => (names.length < 2 ? names.join('') : `${names.slice(0, -1).join(', ')}${L(' et ', ' and ')}${names[names.length - 1]}`);
const PARTY = {
  D: ['Démocrate', 'Democrat'], R: ['Républicain', 'Republican'], I: ['Indépendant', 'Independent'],
  L: ['Parti libertarien', 'Libertarian Party'], G: ['Parti vert', 'Green Party'], Forward: ['Parti Forward', 'Forward Party'],
};
const partyName = (p) => (PARTY[p.party] ? L(...PARTY[p.party]) : p.party || '');
const host = (u) => { try { return new URL(u).hostname.replace(/^www\./, ''); } catch { return u; } };
const ext = (href, label) => html`<a href="${href}" target="_blank" rel="noopener noreferrer">${label} ${icon.external()}</a>`;
const ELECTION = '2028-11-07';

// Age today and on Election Day 2028, from the birth date.
function ageOn(born, iso) {
  if (!/^\d{4}-\d{2}-\d{2}/.test(born || '')) return null;
  const [y, m, d] = born.split('-').map(Number);
  const on = iso ? new Date(`${iso}T12:00:00`) : new Date();
  let a = on.getFullYear() - y;
  if (on.getMonth() + 1 < m || (on.getMonth() + 1 === m && on.getDate() < d)) a -= 1;
  return a;
}

function statusLine(p) {
  if (p.status === 'declared') return p.since ? L(`Candidature annoncée le ${dateL(p.since)}`, `Announced on ${dateL(p.since)}`) : L('Candidature annoncée', 'Has announced a run');
  if (p.status === 'exploratory') return p.since ? L(`Comité exploratoire formé le ${dateL(p.since)}`, `Formed an exploratory committee on ${dateL(p.since)}`) : L('A formé un comité exploratoire', 'Has formed an exploratory committee');
  return L('Wikipédia le classe parmi les personnes qui ont exprimé un intérêt', 'Listed by Wikipedia as having expressed interest');
}

function card(p) {
  const color = personColor(p.party);
  const sub = [partyName(p), p.st && stateName(p.st)].filter(Boolean).join(' · ');
  registerPerson(p.key, { person: p, level: 'federal', color, sub });
  const now = ageOn(p.born), then = ageOn(p.born, ELECTION);
  const [first, ...more] = p.summary || [];
  const cites = p.saidSources || [];
  return html`<article class="card person-card hopeful ${partyClass(p.party)}" id="p-${p.id}">
    <div class="person-main">
      <div class="person-head">
        ${candBadge(p, color)}
        <div style="min-width:0">
          <div class="eyebrow">${L(...STATUS[p.status])}</div>
          <h3 class="person-name">${p.name}</h3>
          <div class="person-sub">${sub}</div>
        </div>
      </div>
      ${p.office ? html`<p class="person-term" lang="en">${p.office}</p>` : ''}
      <p class="person-term">${statusLine(p)}${p.note ? html` <span lang="en">(${p.note})</span>` : ''}${now != null ? html`<br>${L(`Né(e) le ${dateL(p.born)} : ${now} ans, ${then} ans le jour de l’élection`, `Born ${dateL(p.born)}: age ${now}, ${then} on Election Day 2028`)}` : ''}</p>
      ${first ? html`<div class="hope-text">
        <p lang="en">${first}</p>
        ${more.length ? html`<details class="person-more"><summary>${L('Lire la suite', 'Read more')}</summary>${more.map((x) => html`<p lang="en">${x}</p>`)}</details>` : ''}
        <p class="tiny faint">${L('Résumé : début de l’article Wikipédia en anglais (CC BY-SA)', 'Summary: the opening of the Wikipedia article (CC BY-SA)')}</p>
      </div>` : ''}
      ${p.said ? html`<div class="hope-said">
        <div class="eyebrow">${L('Ce qu’on sait de ses intentions pour 2028', 'What they’ve said about 2028')}</div>
        <p lang="en">${p.said}</p>
        <p class="tiny faint">${p.source ? html`<a href="${p.source.url}" target="_blank" rel="noopener noreferrer">${L('Texte de Wikipédia en anglais', 'Text from Wikipedia')}</a>` : L('Texte de Wikipédia en anglais', 'Text from Wikipedia')} (CC BY-SA)${cites.length ? L(', qui cite : ', ', citing: ') : '.'}${cites.map((s, i) => html`${i ? ' · ' : ''}<a href="${s.url}" target="_blank" rel="noopener noreferrer" lang="en">${s.title}</a>`)}</p>
      </div>` : ''}
      <div class="person-links">
        ${p.site ? ext(p.site, p.siteKind === 'campaign' ? L(`Campagne 2028 : ${host(p.site)}`, `2028 campaign: ${host(p.site)}`) : L(`Site : ${host(p.site)}`, `Website: ${host(p.site)}`)) : ''}
        ${p.wiki ? ext(p.wiki, 'Wikipedia') : ''}
        ${p.fec ? ext(p.fec, L('Déclaration à la FEC', 'FEC filing')) : ''}
      </div>
    </div>
    <div class="person-side">
      ${positionsBlock(p, 'federal')}
      <div class="person-actions">${compareButton(p, 'federal')}</div>
    </div>
  </article>`;
}

const statusCounts = (people) => Object.keys(STATUS).map((s) => [s, people.filter((p) => p.status === s).length]).filter(([, n]) => n);
const statusChips = (people) => html`<span class="person-chips">${statusCounts(people).map(([s, n]) => html`<span class="chip">${L(...STATUS[s])} <b>${n}</b></span>`)}</span>`;
const peopleCount = (n) => (n === 1 ? L('1 personne', '1 person') : L(`${n} personnes`, `${n} people`));

// How the statuses and positions work, for the people on the page.
function notice(people) {
  const withPos = people.filter(hasPositions).length;
  const none = people.filter((p) => !hasPositions(p)).map((p) => p.name);
  return html`<div class="notice">${icon.info()}<div class="small">
    <b>${L('Trois statuts, ceux de Wikipédia.', 'Three statuses, as Wikipedia lists them.')}</b>
    ${L('Candidature déclarée : la personne a annoncé sa candidature. Comité exploratoire : elle lève des fonds pour tester une candidature. Intérêt exprimé : elle a dit publiquement envisager de se présenter ; ce qu’elle a dit est cité sous son nom, avec les articles de presse qui le rapportent, même quand elle a depuis pris ses distances.',
      'Declared: they have announced a run. Exploratory committee: they are raising money to test one. Expressed interest: they have said publicly they’re weighing a run; what they said is under their name, with the news reports behind it, even where they have since stepped back.')}
    ${L(`Comparer avec mes opinions : ${withPos} sur ${people.length} ont des positions documentées, par leurs votes et les textes déposés ou cosignés au Congrès depuis 2021, ou par leurs propres programmes, discours, entretiens et actes officiels (lois signées ou bloquées, propositions de loi), chacune avec sa source.`,
      `Compare with my views: ${withPos} of the ${people.length} have positions on file, from their votes in Congress since 2021 and the bills they sponsored or cosponsored there, or from their own platforms, speeches, interviews and official acts (bills signed, vetoed or introduced), each with its source.`)}
    ${none.length ? L(` ${listOf(none)} n’${none.length === 1 ? 'a' : 'ont'} encore rien publié qui réponde au questionnaire.`, ` ${listOf(none)} ${none.length === 1 ? 'has' : 'have'} published nothing yet that answers the questionnaire.`) : ''}
    ${L(' Aucune position n’est devinée.', ' No position is guessed.')}
  </div></div>`;
}

function footer(d, people) {
  return html`${d.checks?.length ? html`<div class="notice warn">${icon.info()}<div><b>${L('À vérifier', 'To be checked')}</b><ul style="margin:6px 0 0" lang="en">${d.checks.map((c) => html`<li>${c}</li>`)}</ul></div></div>` : ''}
    <p class="tiny faint" style="margin:0">${L('Sources : ', 'Sources: ')}${d.sources.map((s, i) => html`${i ? ' · ' : ''}<a href="${s.url}" target="_blank" rel="noopener noreferrer">${s.title}</a>`)} · ${L('votes : ', 'votes: ')}<a href="https://clerk.house.gov/Votes" target="_blank" rel="noopener noreferrer">${L('greffier de la Chambre', 'House Clerk')}</a>, <a href="https://voteview.com/" target="_blank" rel="noopener noreferrer">Voteview</a> · ${L('textes déposés ou cosignés : ', 'bills sponsored or cosponsored: ')}<a href="https://www.govinfo.gov/bulkdata/BILLSTATUS" target="_blank" rel="noopener noreferrer">${L('Bibliothèque du Congrès', 'Library of Congress')}</a> · ${L('autres positions : la source de chacune, sur sa fiche', 'other positions: each one’s source, on its card')} · ${L(`mis à jour le ${dateL(d.updated)}`, `updated ${dateL(d.updated)}`)}</p>
    ${photoCredits(people)}`;
}

const intro = (d) => {
  const inc = d.incumbent;
  return L(
    `Toutes les personnes qui ont déclaré leur candidature, formé un comité exploratoire ou dit publiquement envisager de se présenter. Celles que seuls les médias évoquent et celles qui ont dit non n’y sont pas.${inc?.termLimited ? ` ${inc.name} ne peut pas se représenter : le 22e amendement limite la présidence à deux mandats.` : ''} Pas de sondages ni de pronostics si tôt.`,
    `Everyone who has declared, formed an exploratory committee or said publicly they’re weighing a run. People only the media mention, and people who have said no, aren’t listed.${inc?.termLimited ? ` President ${inc.name} can’t run again: the 22nd Amendment limits presidents to two terms.` : ''} No polls or odds this early.`);
};
const ELECTION_LINE = () => L('Élection présidentielle · 7 novembre 2028', 'Presidential election · November 7, 2028');

// One door per party on #/2028: the party's color with its name and a few faces, then how
// many people it lists and how many have positions.
function door(g) {
  const faces = g.people.filter((p) => photoOf(p)).slice(0, 6);
  const withPos = g.people.filter(hasPositions).length;
  return html`<a class="p28-door ${g.id === 'other' ? 'party-x' : partyClass(g.id)}" href="#/2028/${g.id}">
    <span class="p28-door-top">
      <span class="p28-door-name">${L(...GROUP[g.id])}</span>
      ${faces.length ? html`<span class="p28-faces" aria-hidden="true">${faces.map((p) => candBadge(p, '#fff'))}</span>` : ''}
    </span>
    <span class="p28-door-body">
      <span class="p28-count"><b>${peopleCount(g.people.length)}</b>${g.people.length ? html` · ${L(`${withPos} avec des positions documentées`, `${withPos} with positions on file`)}` : ''}</span>
      ${statusChips(g.people)}
      <span class="p28-cta">${L(...CTA[g.id])} ${icon.chevronRight()}</span>
    </span>
  </a>`;
}

function landing(d) {
  const all = d.groups.flatMap((g) => g.people);
  const byId = Object.fromEntries(d.groups.map((g) => [g.id, g]));
  const shown = GROUP_IDS.flatMap((id) => (byId[id]?.people || []).filter((p) => photoOf(p)).slice(0, 6));
  return html`<div class="wrap page stack-lg">
    <div>
      <div class="eyebrow">${ELECTION_LINE()}</div>
      <h1 style="margin:6px 0 8px">${L('Qui pourrait se présenter à la présidence en 2028', 'Who might run for President in 2028')}</h1>
      <p class="muted" style="margin:0">${intro(d)} ${L('Choisissez un parti :', 'Choose a party:')}</p>
    </div>
    <nav class="p28-doors" aria-label="${L('Partis', 'Parties')}">${GROUP_IDS.map((id) => door(byId[id] || { id, people: [] }))}</nav>
    ${notice(all)}
    ${footer(d, shown)}
  </div>`;
}

function partyPage(d, id) {
  const g = d.groups.find((x) => x.id === id) || { id, people: [] };
  return html`<div class="wrap page stack-lg">
    <div>
      <nav class="crumbs" aria-label="${L('Fil d’Ariane', 'Breadcrumb')}"><a href="#/2028">${L('Présidentielle 2028', '2028 presidential field')}</a><span>/</span><span>${L(...GROUP[id])}</span></nav>
      <div class="eyebrow">${ELECTION_LINE()}</div>
      <h1 class="p28-title ${id === 'other' ? 'party-x' : partyClass(id)}">${L(...GROUP[id])}</h1>
      <p class="muted" style="margin:0">${peopleCount(g.people.length)}. ${intro(d)}</p>
    </div>
    <nav class="p28-tabs" aria-label="${L('Partis', 'Parties')}">${GROUP_IDS.map((x) => {
      const n = d.groups.find((y) => y.id === x)?.people.length || 0;
      return html`<a class="p28-tab ${x === 'other' ? 'party-x' : partyClass(x)}" href="#/2028/${x}" aria-current="${x === id ? 'page' : 'false'}">${L(...GROUP[x])} <b>${n}</b></a>`;
    })}</nav>
    ${statusChips(g.people)}
    ${notice(g.people)}
    ${g.people.length ? html`<div class="people-grid">${g.people.map(card)}</div>` : html`<p class="muted" style="margin:0">${L('Personne pour l’instant.', 'No one yet.')}</p>`}
    ${g.source ? html`<p class="tiny faint" style="margin:0">${L('Liste : ', 'List: ')}<a href="${g.source.url}" target="_blank" rel="noopener noreferrer">${g.source.title}</a></p>` : ''}
    ${footer(d, g.people)}
  </div>`;
}

export const president2028 = {
  title: (ctx) => (GROUP[ctx?.params?.[0]] ? `${L(...GROUP[ctx.params[0]])} · ${L('Présidentielle 2028', '2028 presidential field')}` : L('Présidentielle 2028', '2028 presidential field')),
  async render(ctx) {
    const d = await load();
    if (!d) return html`<div class="wrap page"><div class="empty">${icon.info()}<h3>${L('Données indisponibles', 'This data is unavailable')}</h3><p>${L('Lancez scripts/update_president_2028.py pour les construire.', 'Run scripts/update_president_2028.py to build it.')}</p></div></div>`;
    const id = ctx?.params?.[0];
    return GROUP[id] ? partyPage(d, id) : landing(d);
  },
  mount(root) {
    return wireCompare(root);
  },
};
