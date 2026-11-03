// The frame around every France page: the countdown bar, the header (menu, French
// flag profile picture, FR | EN switch, theme), the latest-polls ticker, the data
// note and the footer. It reuses the U.S. shell's element ids so the same CSS applies.

import { html, raw, $ } from '../util.js';
import { icon, logo } from '../icons.js';
import { store } from '../store.js';
import { L, langSwitchHTML, wireLangSwitch } from '../i18n.js';
import { avatarSrc } from '../components/shell.js';
import { loadPres, daysUntil, fmtDay, fmtNum, candById, pollDates, runningIds, usedScenarios } from './data.js';

export const FR_MENU = () => [
  ['#/fr', L('Accueil et carte', 'Home and map'), 'globe'],
  ['#/fr/presidentielle', L('Présidentielle 2027 : les deux tours', '2027 presidential election: both rounds'), 'ballot'],
  ['#/fr/partis', L('Les principaux partis et leurs valeurs', 'The main parties and values'), 'user'],
  ['#/fr/parlement', L('Parlement français', 'French Parliament'), 'parliament'],
  ['#/fr/suivies', L('Élections suivies', 'Starred elections'), 'star'],
  ['#/fr/enjeux', L('Les grands enjeux', 'Major issues'), 'chart'],
  ['#/country', L('Quel pays ?', 'Which country?'), 'globe'],
  ['#/fr/a-propos', L('À propos des données', 'About the data'), 'info'],
  ['#/fr/soutenir', L('Soutenir le site', 'Supporting the site'), 'dollar'],
];
export const FR_PROFILE_MENU = () => [
  ['#/fr/profil', L('Mon profil', 'My profile'), 'user'],
  ['#/fr/elections', L('Mes élections', 'My elections'), 'ballot'],
];

function topbar(pres) {
  if (!pres) return html`<div class="wrap"><span>${L('Présidentielle 2027', '2027 presidential election')}</span><span class="sep"></span><a href="#/fr/a-propos" class="faint">${L('À propos des données', 'About the data')}</a></div>`;
  const d1 = daysUntil(pres.rounds.r1), d2 = daysUntil(pres.rounds.r2);
  const days = (n) => (n === 0 ? L('aujourd’hui', 'today') : L(`J-${n}`, `${n} day${n === 1 ? '' : 's'}`));
  const top = pres.r1.average.candidates.slice(0, 3).map((a) => {
    const c = candById(pres, a.id);
    return html`<span class="chamber-odd">${c.short} <b>${fmtNum(a.avg)}</b></span>`;
  });
  return html`<div class="wrap">
    <span><span class="live"></span>${L('Présidentielle', 'Presidential election')} · ${L('1er tour', 'Round 1')} ${fmtDay(pres.rounds.r1, { year: false })} · <strong>${d1 >= 0 ? days(d1) : L('passé', 'held')}</strong></span>
    <span class="faint">${L('2nd tour', 'Round 2')} ${fmtDay(pres.rounds.r2, { year: false })}${d2 >= 0 ? ` · ${days(d2)}` : ''}</span>
    <span class="faint">${L('Moyenne des sondages :', 'Poll average:')}</span> ${top}
    <span class="sep"></span>
    <a href="#/fr/a-propos" class="faint">${L('À propos des données', 'About the data')}</a>
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
      <div class="menu left" id="main-menu" role="menu" hidden>${menuLinks(FR_MENU())}</div>
    </div>
    <a class="brand" href="#/fr" aria-label="${L('Informed Voter, accueil France', 'Informed Voter France home')}">${logo()}<span class="brand-text">Informed Voter<small>${L('FRANCE · PRÉSIDENTIELLE 2027', 'FRANCE · 2027 ELECTIONS')}</small></span></a>
    <span class="header-spacer"></span>
    ${raw(langSwitchHTML())}
    <button type="button" class="pill-btn icon-only" id="theme-btn" aria-label="${dark ? L('Passer au thème clair', 'Switch to light theme') : L('Passer au thème sombre', 'Switch to dark theme')}" title="${L('Changer de thème', 'Switch theme')}">${dark ? icon.sun() : icon.moon()}</button>
    <div class="menu-wrap">
      <button type="button" class="avatar-btn" id="profile-menu-btn" aria-haspopup="true" aria-expanded="false" aria-controls="profile-menu" aria-label="${L('Menu de votre profil', 'Your profile menu')}"><img class="avatar" id="header-avatar" src="${avatarSrc()}" alt=""></button>
      <div class="menu right" id="profile-menu" role="menu" hidden>
        <div class="menu-head"><div class="eyebrow">${L('Votre profil', 'Your profile')}</div><div class="small muted">${L('Enregistré uniquement dans ce navigateur', 'Saved only in this browser')}</div></div>
        ${menuLinks(FR_PROFILE_MENU())}
      </div>
    </div>
  </div>`;
}

// The latest polls scroll past, each with its top three candidates.
function ticker(pres) {
  if (!pres) return '';
  const running = runningIds(pres);
  const items = pres.r1.polls.slice(0, 10).map((p) => {
    const s = usedScenarios(p, running)[0] || p.scenarios[0];
    const top = Object.entries(s).filter(([id]) => running.has(id)).sort((a, b) => b[1] - a[1]).slice(0, 3)
      .map(([id, v]) => `${candById(pres, id)?.short || id} ${fmtNum(v, v % 1 ? 1 : 0)}`).join(' · ');
    return html`<a href="#/fr/presidentielle"><b>${p.pollster}</b>${pollDates(p.dates.replace(/\s+20\d\d$/, ''))} <span class="m">${top}</span></a>`;
  });
  return html`<div class="inner"><span class="tag">${L('SONDAGES', 'POLLS')}</span><div class="track">${items}${raw('<span aria-hidden="true" style="display:contents">')}${items}${raw('</span>')}</div></div>`;
}

function banner() {
  return html`<div class="wrap">${icon.info()}<span><b>${L('Données réelles :', 'Real data:')}</b> ${L(
    'candidats déclarés et sondages publiés, chacun relié à sa notice officielle de la Commission des sondages, mis à jour chaque jour. Les positions des candidats sur le questionnaire viennent de leurs programmes et déclarations, chacune avec sa source : rien n’est deviné.',
    'declared candidates and published polls, each linked to its official notice at the Commission des sondages (France’s polling regulator), updated every day. Candidates’ positions on the questionnaire come from their programs and statements, each with its source: nothing is guessed.',
  )} <a href="#/fr/a-propos">${L('Ce qui est réel', 'What’s real?')}</a></span></div>`;
}

function footer() {
  return html`<div class="wrap">
    <span>© 2026 Informed Voter · ${L('Guide non partisan, sans lien avec aucun parti, candidat ni administration.', 'A nonpartisan guide. Not affiliated with any party, candidate or government agency.')}</span>
    <span><a href="#/fr/a-propos">${L('À propos des données', 'About the data')}</a> · <a href="#/fr/soutenir">${L('Soutenir le site', 'Support the site')}</a></span>
  </div>`;
}

let wiredDocument = false;

export async function renderFrShell() {
  const pres = await loadPres();
  $('#topbar').innerHTML = String(topbar(pres));
  $('#site-header').innerHTML = String(header());
  const tk = $('#ticker');
  tk.innerHTML = String(ticker(pres));
  tk.hidden = !pres;
  $('#demo-banner').innerHTML = String(banner());
  $('#site-footer').innerHTML = String(footer());
  wireMenus();
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
  if (!wiredDocument) {
    wiredDocument = true;
    document.addEventListener('click', (e) => { if (!e.target.closest('.menu-wrap')) closeAll(); });
  }
  wireLangSwitch($('#site-header'));
  $('#theme-btn').addEventListener('click', () => {
    const next = document.documentElement.dataset.theme === 'light' ? 'dark' : 'light';
    document.documentElement.dataset.theme = next;
    store.set({ theme: next });
    window.dispatchEvent(new CustomEvent('iv:theme'));
  });
}
