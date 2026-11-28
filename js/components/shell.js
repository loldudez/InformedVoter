// The frame around every page: countdown bar, header with both menus, the
// closest-races ticker, the demo-data banner and the footer.

import { html, raw, $, fmtProb } from '../util.js';
import { icon, logo } from '../icons.js';
import { store } from '../store.js';
import { daysToElection } from '../model/forecast.js';
import { mainRaces, fc, chamberSummary, raceShortTitle, realRaceCount, researchedCount, officeCount, officesResearched, resultsIn, resultsTally, resultMargin, resultWinners, resultParty, liveFc, stillCounting, racesMeta, allCertified, certifiedCount } from '../data/world.js';
import { lastName, resultMarginStr } from './race.js';
import { section, L, lang, langSwitchHTML, wireLangSwitch } from '../i18n.js';

export const MAIN_MENU = () => [
  ['#/', L('Accueil', 'Homepage'), 'globe'],
  ['#/parties', L('Les principaux partis et leurs valeurs', 'The main parties and values'), 'user'],
  ['#/congress', L('Le Congrès des États-Unis', 'U.S. Congress'), 'parliament'],
  ['#/starred', L('Élections suivies', 'Starred elections'), 'star'],
  ['#/liked', L('Candidats favoris', 'Liked candidates'), 'heart'],
  ['#/close', L('Élections serrées', 'Close elections'), 'ballot'],
  ['#/upcoming', L('Prochaines élections', 'Upcoming elections'), 'calendar'],
  ['#/2028', L('Les candidats à la présidentielle 2028', 'The 2028 presidential field'), 'ballot'],
  ['#/news', L('L’actualité de l’élection', 'Major news regarding the election'), 'news'],
  ['#/inflation', L('Suivi de l’inflation', 'Inflation tracker'), 'dollar'],
  ['#/country', L('Quel pays ?', 'Which country?'), 'globe'],
  ['#/about', L('À propos des données', 'About the data'), 'info'],
  ['#/donate', L('Faire un don au site', 'Donating to the site'), 'dollar'],
];
export const PROFILE_MENU = () => [
  ['#/profile', L('Mon profil', 'My profile'), 'user'],
  ['#/elections', L('Mes élections', 'My elections'), 'ballot'],
  ['#/donations', L('Dons', 'Donations'), 'heart'],
];

// A picture the visitor chose shows in both sections; otherwise each section shows its flag.
export const avatarSrc = () => {
  const a = store.get().avatar;
  if (a && a.startsWith('data:image/')) return a;
  return section() === 'fr' ? 'assets/flag-fr-square.svg' : 'assets/flag-us-square.svg';
};

// On this computer (scripts/test_site.cmd, or serve.py), a tag in the header says the page
// is the test copy, so it is never mistaken for www.informedvoter.io.
export const isTestSite = () => ['localhost', '127.0.0.1', '[::1]', '::1'].includes(location.hostname) || location.hostname.endsWith('.localhost');
export const testChip = () => isTestSite()
  ? html`<span class="test-chip" title="${L('Cette copie tourne sur cet ordinateur ; le site en ligne ne change que lorsque le dossier GitHub est publié.', 'This copy runs on this computer; the live site changes only when the GitHub folder is pushed.')}"><span class="test-long">${L('Site de test', 'Test site')}</span><span class="test-short">Test</span></span>`
  : '';

// After Election Day: seats each party has so far (called races plus seats not up).
function resultsBar() {
  const seg = (label, key) => {
    const t = resultsTally(key);
    const open = t.uncalled.length + t.runoff.length;
    return html`<span class="chamber-odd">${label} <b class="d-text">${t.seats.D} D</b> <b class="r-text">${t.seats.R} R</b>${t.seats.I ? html` <b>${L(`${t.seats.I} autre${t.seats.I > 1 ? 's' : ''}`, `${t.seats.I} other`)}</b>` : ''}${open ? html` <span class="faint">· ${L(`${open} en attente`, `${open} open`)}</span>` : ''}</span>`;
  };
  return html`<div class="wrap">
    ${officialLabel()}
    <span class="faint">${L('Sièges à ce jour :', 'Seats so far:')}</span>
    ${seg(L('Sénat', 'Senate'), 'senate')} ${seg(L('Chambre', 'House'), 'house')} ${seg(L('Gouverneurs', 'Governors'), 'governor')}
    <span class="sep"></span>
    ${link2028()}
    <a href="#/about" class="faint">${L('À propos des données', 'About the data')}</a>
  </div>`;
}

// The 2028 field, at the top of every U.S. page (owner's request, Nov. 25, 2026); first in
// the strip on narrow screens, where the rest scrolls sideways.
// "Unofficial" until every state has certified (data/certified.json), then "official".
function officialLabel() {
  if (allCertified()) return html`<span>${L('Résultats 2026', '2026 results')} · <strong title="${L('Chaque État a certifié ses résultats', 'Every state has certified its results')}">${L('officiels', 'official')}</strong></span>`;
  const n = certifiedCount();
  return html`<span><span class="live"></span>${L('Résultats 2026', '2026 results')} · <strong title="${L(`Non officiels jusqu’à ce que chaque État certifie ses résultats${n ? ` (certification confirmée ici pour ${n} sur 51 à ce jour)` : ''}`, `Unofficial until every state certifies its results${n ? ` (confirmed here for ${n} of 51 so far)` : ''}`)}">${L('non officiels', 'unofficial')}</strong></span>`;
}
const link2028 = () => html`<a href="#/2028" class="top-2028">${L('Voir les candidats potentiels à la présidentielle 2028', 'View the potential candidates for 2028 Presidency')} ${icon.chevronRight()}</a>`;

function topbar() {
  if (resultsIn()) return resultsBar();
  const days = daysToElection();
  const sum = chamberSummary();
  const odd = (label, o) => {
    const pR = o.pR ?? 1 - o.pD;
    const dFav = o.pD >= pR;
    return html`<span class="chamber-odd">${label} <b class="${dFav ? 'd-text' : 'r-text'}">${dFav ? 'D' : 'R'} ${fmtProb(dFav ? o.pD : pR)}</b></span>`;
  };
  return html`<div class="wrap">
    <span><span class="live"></span>${L('Jour de l’élection, 3 nov.', 'Election Day, Nov 3')} · <strong>${days === 0 ? L('aujourd’hui', 'today') : L(`J-${days}`, `${days} day${days === 1 ? '' : 's'}`)}</strong></span>
    <span class="faint">${L('Chances de contrôle', 'Control odds')}${realRaceCount ? '' : html` (${L('démo', 'demo')})`}${L(' :', ':')}</span>
    ${odd(L('Sénat', 'Senate'), sum.senate)} ${odd(L('Chambre', 'House'), sum.house)} ${odd(L('Gouverneurs', 'Governors'), sum.governor)}
    <span class="sep"></span>
    ${link2028()}
    <a href="#/about" class="faint">${L('À propos des données', 'About the data')}</a>
  </div>`;
}

function menuLinks(items) {
  return items.map(([href, label, ic]) => html`<a href="${href}" role="menuitem">${icon[ic]()}<span>${label}</span></a>`);
}

function header() {
  const dark = document.documentElement.dataset.theme !== 'light';
  return html`<div class="wrap">
    <div class="menu-wrap">
      <button type="button" class="pill-btn" id="main-menu-btn" aria-label="${L('Menu principal', 'Main menu')}" aria-haspopup="true" aria-expanded="false" aria-controls="main-menu">${icon.menu()}<span class="hide-sm">Menu</span></button>
      <div class="menu left" id="main-menu" role="menu" hidden>${menuLinks(MAIN_MENU())}</div>
    </div>
    <a class="brand" href="#/" aria-label="${L('Informed Voter, accueil', 'Informed Voter home')}">${logo()}<span class="brand-text">Informed Voter<small>${L('MI-MANDAT 2026', '2026 MIDTERMS')}</small></span></a>
    ${testChip()}
    <span class="header-spacer"></span>
    ${raw(langSwitchHTML())}
    <button type="button" class="pill-btn icon-only" id="theme-btn" aria-label="${dark ? L('Passer au thème clair', 'Switch to light theme') : L('Passer au thème sombre', 'Switch to dark theme')}" title="${L('Changer de thème', 'Switch theme')}">${dark ? icon.sun() : icon.moon()}</button>
    <div class="menu-wrap">
      <button type="button" class="avatar-btn" id="profile-menu-btn" aria-haspopup="true" aria-expanded="false" aria-controls="profile-menu" aria-label="${L('Menu de votre profil', 'Your profile menu')}"><img class="avatar" id="header-avatar" src="${avatarSrc()}" alt=""></button>
      <div class="menu right" id="profile-menu" role="menu" hidden>
        <div class="menu-head"><div class="eyebrow">${L('Votre profil', 'Your profile')}</div><div class="small muted">${L('Enregistré uniquement dans ce navigateur', 'Saved only in this browser')}</div></div>
        ${menuLinks(PROFILE_MENU())}
      </div>
    </div>
  </div>`;
}

// After Election Day: the races still open, then the closest called ones.
function resultsTicker() {
  const rs = mainRaces().filter((r) => r.result && (r.office !== 'house' || r.result.status !== 'won' || (resultMargin(r)?.pts ?? 99) < 3))
    .sort((a, b) => (a.result.status === 'won') - (b.result.status === 'won') || (resultMargin(a)?.pts ?? 99) - (resultMargin(b)?.pts ?? 99))
    .slice(0, 18);
  const items = rs.map((r) => {
    const res = r.result;
    const w = res.status === 'won' ? resultWinners(r)[0] : null;
    const p = resultParty(r);
    const m = resultMarginStr(r, { named: false });
    const who = res.status === 'won' ? (w ? lastName(w.name) : '') : resultMargin(r) ? lastName(resultMargin(r).a.name) : '';
    const label = res.status === 'won' ? L(`${who} l’a emporté`, `${who} won`) : res.status === 'runoff' ? L('Second tour', 'Runoff') : L(`${who} en tête`, `${who} leads`);
    const lv = res.status === 'counting' ? liveFc(r) : null;
    return html`<a href="#/race/${r.id}"><b>${raceShortTitle(r)}</b>${label}${m && res.status !== 'runoff' ? html` <span class="m ${p === 'D' ? 'd-text' : p === 'R' ? 'r-text' : ''}">${m}</span>` : ''}${lv ? html` <span class="faint">· ${lastName(lv.lead.name)} ${fmtProb(lv.pLead)}</span>` : ''}</a>`;
  });
  return html`<div class="inner"><span class="tag">${L('RÉSULTATS', 'RESULTS')}</span><div class="track" aria-hidden="false">${items}${raw('<span aria-hidden="true" style="display:contents">')}${items}${raw('</span>')}</div></div>`;
}

function ticker() {
  if (resultsIn()) return resultsTicker();
  const close = mainRaces().filter((r) => r.office !== 'house' || (!fc(r).open && Math.abs(fc(r).margin) < 4))
    .map((r) => ({ r, f: fc(r) }))
    .filter(({ f }) => !f.open)
    .sort((a, b) => Math.abs(a.f.pLead - 0.5) - Math.abs(b.f.pLead - 0.5))
    .slice(0, 16);
  const items = close.map(({ r, f }) => html`<a href="#/race/${r.id}"><b>${raceShortTitle(r)}</b>${lastName(f.lead.name)} <span class="m ${f.lead.party === 'D' ? 'd-text' : f.lead.party === 'R' ? 'r-text' : ''}">${f.lead.party} +${f.margin.toFixed(1)}</span></a>`);
  const days = daysToElection();
  return html`<div class="inner"><span class="tag">${L(`J-${days}`, `${days} DAYS OUT`)}</span><div class="track" aria-hidden="false">${items}${raw('<span aria-hidden="true" style="display:contents">')}${items}${raw('</span>')}</div></div>`;
}

function banner() {
  if (lang() === 'fr') return bannerFr();
  if (realRaceCount && resultsIn()) {
    return html`<div class="wrap">${icon.info()}<span><b>2026 results for every Senate, House and governor race</b>${officeCount ? html`, and for ${officeCount} statewide offices below governor` : ''}, ${stillCounting() && racesMeta()?.resultsUpdated ? 'with the results re-read every 10 minutes until every race is called' : 'refreshed every 8 hours'} (<span class="live-chip">Live data</span>). A race shows a winner once Wikipedia’s national results table marks one; vote counts are unofficial until each state certifies them. The final forecasts stay on every race page. ${researchedCount + officesResearched} race${researchedCount + officesResearched === 1 ? ' has' : 's have'} researched issue positions with sources (<span class="real-chip">Sourced</span>). <a href="#/about">What’s real?</a></span></div>`;
  }
  if (realRaceCount) {
    return html`<div class="wrap">${icon.info()}<span><b>Real data for every Senate, House and governor race</b>, refreshed every 8 hours: candidates, forecasters’ ratings, polls and fundraising (<span class="live-chip">Live data</span>). ${researchedCount} race${researchedCount === 1 ? ' also has' : 's also have'} researched issue positions with sources (<span class="real-chip">Sourced</span>). State legislative races show the real seats, and the holders and candidates Wikipedia lists, without forecasts. <a href="#/about">What’s real?</a></span></div>`;
  }
  return html`<div class="wrap">${icon.info()}<span><b>Preview with demo data.</b> Candidates, polls, forecasts, positions and fundraising are fictional placeholders. Maps, districts, address lookup, news and inflation are real. <a href="#/about">What’s real?</a></span></div>`;
}

function bannerFr() {
  const n = researchedCount + officesResearched;
  if (realRaceCount && resultsIn()) {
    return html`<div class="wrap">${icon.info()}<span><b>Les résultats 2026 de toutes les élections au Sénat, à la Chambre et aux postes de gouverneur</b>${officeCount ? html`, et de ${officeCount} élections à d’autres postes de l’exécutif des États` : ''}, ${stillCounting() && racesMeta()?.resultsUpdated ? 'relus toutes les 10 minutes jusqu’à ce que chaque élection soit attribuée' : 'mis à jour toutes les 8 heures'} (<span class="live-chip">Données en direct</span>). Une élection affiche un vainqueur dès que le tableau national des résultats de Wikipédia en désigne un ; les décomptes restent non officiels jusqu’à leur certification par chaque État. Les dernières prévisions restent sur chaque page d’élection. ${n} élection${n === 1 ? ' a' : 's ont'} des positions sur les enjeux, recherchées avec leurs sources (<span class="real-chip">Sourcé</span>). <a href="#/about">Qu’est-ce qui est réel ?</a></span></div>`;
  }
  if (realRaceCount) {
    return html`<div class="wrap">${icon.info()}<span><b>Des données réelles pour toutes les élections au Sénat, à la Chambre et aux postes de gouverneur</b>, mises à jour toutes les 8 heures : candidats, cotes des analystes, sondages et levées de fonds (<span class="live-chip">Données en direct</span>). ${researchedCount} élection${researchedCount === 1 ? ' a' : 's ont'} aussi des positions sur les enjeux, recherchées avec leurs sources (<span class="real-chip">Sourcé</span>). Les élections aux assemblées des États montrent les vrais sièges, avec les sortants et les candidats que liste Wikipédia, sans prévisions. <a href="#/about">Qu’est-ce qui est réel ?</a></span></div>`;
  }
  return html`<div class="wrap">${icon.info()}<span><b>Aperçu avec des données de démonstration.</b> Les candidats, sondages, prévisions, positions et levées de fonds sont fictifs. Les cartes, les circonscriptions, la recherche d’adresse, l’actualité et l’inflation sont réelles. <a href="#/about">Qu’est-ce qui est réel ?</a></span></div>`;
}

function footer() {
  return html`<div class="wrap">
    <span>${L('© 2026 Informed Voter · Un guide non partisan, sans lien avec aucun parti, candidat ou organisme public.', '© 2026 Informed Voter · A nonpartisan guide. Not affiliated with any party, candidate or government agency.')}</span>
    <span><a href="#/about">${L('À propos des données', 'About the data')}</a> · <a href="#/donate">${L('Soutenir le site', 'Support the site')}</a></span>
  </div>`;
}

export function renderShell() {
  $('#topbar').innerHTML = String(topbar());
  $('#site-header').innerHTML = String(header());
  $('#ticker').innerHTML = String(ticker());
  $('#demo-banner').innerHTML = String(banner());
  $('#site-footer').innerHTML = String(footer());
  wireMenus();
  wireLangSwitch($('#site-header'));
}

export function refreshAvatar() {
  const img = $('#header-avatar');
  if (img) img.src = avatarSrc();
}

export function markActive(hash) {
  document.querySelectorAll('.menu a').forEach((a) => {
    const href = a.getAttribute('href');
    const on = href === hash || (href !== '#/' && hash.startsWith(href));
    on ? a.setAttribute('aria-current', 'page') : a.removeAttribute('aria-current');
  });
}

function wireMenus() {
  const pairs = [['#main-menu-btn', '#main-menu'], ['#profile-menu-btn', '#profile-menu']];
  const closeAll = (except) => pairs.forEach(([b, m]) => {
    if (m === except || !$(m)) return;
    $(m).hidden = true;
    $(b).setAttribute('aria-expanded', 'false');
  });
  for (const [b, m] of pairs) {
    const btn = $(b), menu = $(m);
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const open = menu.hidden;
      closeAll(m);
      menu.hidden = !open;
      btn.setAttribute('aria-expanded', String(open));
      if (open) menu.querySelector('a')?.focus();
    });
    menu.addEventListener('keydown', (e) => {
      const links = [...menu.querySelectorAll('a')];
      const i = links.indexOf(document.activeElement);
      if (e.key === 'ArrowDown') { e.preventDefault(); links[(i + 1) % links.length].focus(); }
      if (e.key === 'ArrowUp') { e.preventDefault(); links[(i - 1 + links.length) % links.length].focus(); }
      if (e.key === 'Escape') { menu.hidden = true; btn.setAttribute('aria-expanded', 'false'); btn.focus(); }
    });
    menu.addEventListener('click', (e) => { if (e.target.closest('a')) closeAll(); });
  }
  document.addEventListener('click', (e) => { if (!e.target.closest('.menu-wrap')) closeAll(); });
  $('#theme-btn').addEventListener('click', () => {
    const next = document.documentElement.dataset.theme === 'light' ? 'dark' : 'light';
    document.documentElement.dataset.theme = next;
    store.set({ theme: next });
    window.dispatchEvent(new CustomEvent('iv:theme'));
  });
}
