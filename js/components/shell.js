// The frame around every page: countdown bar, header with both menus, the
// closest-races ticker, the demo-data banner and the footer.

import { html, raw, $, fmtProb } from '../util.js';
import { icon, logo } from '../icons.js';
import { store } from '../store.js';
import { daysToElection } from '../model/forecast.js';
import { allRaces, fc, chamberSummary, raceShortTitle, realRaceCount, researchedCount } from '../data/world.js';
import { lastName } from './race.js';

export const MAIN_MENU = [
  ['#/', 'Homepage', 'globe'],
  ['#/country', 'Which country?', 'globe'],
  ['#/parties', 'The main parties and values', 'user'],
  ['#/starred', 'Starred elections', 'star'],
  ['#/liked', 'Liked candidates', 'heart'],
  ['#/close', 'Close elections', 'ballot'],
  ['#/news', 'Major news regarding the election', 'news'],
  ['#/inflation', 'Inflation tracker', 'dollar'],
  ['#/donate', 'Donating to the site', 'dollar'],
];
export const PROFILE_MENU = [
  ['#/profile', 'My profile', 'user'],
  ['#/elections', 'My elections', 'ballot'],
  ['#/donations', 'Donations', 'heart'],
];

export const avatarSrc = () => {
  const a = store.get().avatar;
  return a && a.startsWith('data:image/') ? a : 'assets/flag-us-square.svg';
};

function topbar() {
  const days = daysToElection();
  const sum = chamberSummary();
  const odd = (label, o) => {
    const pR = o.pR ?? 1 - o.pD;
    const dFav = o.pD >= pR;
    return html`<span class="chamber-odd">${label} <b class="${dFav ? 'd-text' : 'r-text'}">${dFav ? 'D' : 'R'} ${fmtProb(dFav ? o.pD : pR)}</b></span>`;
  };
  return html`<div class="wrap">
    <span><span class="live"></span>Election Day, Nov 3 · <strong>${days === 0 ? 'today' : `${days} day${days === 1 ? '' : 's'}`}</strong></span>
    <span class="faint">Control odds${realRaceCount ? '' : html` (demo)`}:</span>
    ${odd('Senate', sum.senate)} ${odd('House', sum.house)} ${odd('Governors', sum.governor)}
    <span class="sep"></span>
    <a href="#/about" class="faint">About the data</a>
  </div>`;
}

function menuLinks(items) {
  return items.map(([href, label, ic]) => html`<a href="${href}" role="menuitem">${icon[ic]()}<span>${label}</span></a>`);
}

function header() {
  const dark = document.documentElement.dataset.theme !== 'light';
  return html`<div class="wrap">
    <div class="menu-wrap">
      <button type="button" class="pill-btn" id="main-menu-btn" aria-label="Main menu" aria-haspopup="true" aria-expanded="false" aria-controls="main-menu">${icon.menu()}<span class="hide-sm">Menu</span></button>
      <div class="menu left" id="main-menu" role="menu" hidden>${menuLinks(MAIN_MENU)}</div>
    </div>
    <a class="brand" href="#/" aria-label="Informed Voter home">${logo()}<span class="brand-text">Informed Voter<small>2026 MIDTERMS</small></span></a>
    <span class="header-spacer"></span>
    <button type="button" class="pill-btn icon-only" id="theme-btn" aria-label="Switch to ${dark ? 'light' : 'dark'} theme" title="Switch theme">${dark ? icon.sun() : icon.moon()}</button>
    <div class="menu-wrap">
      <button type="button" class="avatar-btn" id="profile-menu-btn" aria-haspopup="true" aria-expanded="false" aria-controls="profile-menu" aria-label="Your profile menu"><img class="avatar" id="header-avatar" src="${avatarSrc()}" alt=""></button>
      <div class="menu right" id="profile-menu" role="menu" hidden>
        <div class="menu-head"><div class="eyebrow">Your profile</div><div class="small muted">Saved only in this browser</div></div>
        ${menuLinks(PROFILE_MENU)}
      </div>
    </div>
  </div>`;
}

function ticker() {
  const close = allRaces().filter((r) => r.office !== 'house' || (!fc(r).open && Math.abs(fc(r).margin) < 4))
    .map((r) => ({ r, f: fc(r) }))
    .filter(({ f }) => !f.open)
    .sort((a, b) => Math.abs(a.f.pLead - 0.5) - Math.abs(b.f.pLead - 0.5))
    .slice(0, 16);
  const items = close.map(({ r, f }) => html`<a href="#/race/${r.id}"><b>${raceShortTitle(r)}</b>${lastName(f.lead.name)} <span class="m ${f.lead.party === 'D' ? 'd-text' : f.lead.party === 'R' ? 'r-text' : ''}">${f.lead.party} +${f.margin.toFixed(1)}</span></a>`);
  const days = daysToElection();
  return html`<div class="inner"><span class="tag">${days} DAYS OUT</span><div class="track" aria-hidden="false">${items}${raw('<span aria-hidden="true" style="display:contents">')}${items}${raw('</span>')}</div></div>`;
}

function banner() {
  if (realRaceCount) {
    return html`<div class="wrap">${icon.info()}<span><b>Real data for every Senate, House and governor race</b>, refreshed every 8 hours: candidates, forecasters’ ratings, polls and fundraising (<span class="live-chip">Live data</span>). ${researchedCount} race${researchedCount === 1 ? ' also has' : 's also have'} researched issue positions with sources (<span class="real-chip">Sourced</span>). State legislative races are still demo placeholders. <a href="#/about">What’s real?</a></span></div>`;
  }
  return html`<div class="wrap">${icon.info()}<span><b>Preview with demo data.</b> Candidates, polls, forecasts, positions and fundraising are fictional placeholders. Maps, districts, address lookup, news and inflation are real. <a href="#/about">What’s real?</a></span></div>`;
}

function footer() {
  return html`<div class="wrap">
    <span>© 2026 Informed Voter · A nonpartisan guide. Not affiliated with any party, candidate or government agency.</span>
    <span><a href="#/about">About the data</a> · <a href="#/donate">Support the site</a></span>
  </div>`;
}

export function renderShell() {
  $('#topbar').innerHTML = String(topbar());
  $('#site-header').innerHTML = String(header());
  $('#ticker').innerHTML = String(ticker());
  $('#demo-banner').innerHTML = String(banner());
  $('#site-footer').innerHTML = String(footer());
  wireMenus();
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
    if (m === except) return;
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
