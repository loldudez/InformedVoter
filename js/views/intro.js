import { html, raw } from '../util.js';
import { logo, icon } from '../icons.js';
import { FLAGS } from '../components/flags.js';
import { store } from '../store.js';

const COUNTRIES = [
  { id: 'us', name: 'United States', sub: '2026 midterm elections · November 3', active: true },
  { id: 'uk', name: 'United Kingdom', sub: 'Coming soon' },
  { id: 'ca', name: 'Canada', sub: 'Coming soon' },
  { id: 'fr', name: 'France', sub: 'Bientôt disponible · coming soon' },
];

export function countryPicker() {
  return html`<div class="countries">${COUNTRIES.map((c) => (c.active
    ? html`<a class="country" href="#/" data-choose-country="${c.id}"><span class="flag">${raw(FLAGS[c.id])}</span><span><span class="cn">${c.name}</span><br><span class="cs">${c.sub}</span></span><span class="go">${icon.chevronRight()}</span></a>`
    : html`<div class="country disabled" aria-disabled="true" title="${c.name} coverage is coming soon"><span class="flag">${raw(FLAGS[c.id])}</span><span><span class="cn">${c.name}</span><br><span class="cs">${c.sub}</span></span></div>`))}</div>`;
}

export function wireCountryPicker(root) {
  root.querySelectorAll('[data-choose-country]').forEach((a) => a.addEventListener('click', (e) => {
    e.preventDefault();
    store.set({ countryChosen: true });
    // The intro lives at #/ too, so changing the hash alone wouldn't redraw.
    if (location.hash === '#/') window.dispatchEvent(new Event('iv:rerender'));
    else location.hash = '#/';
  }));
}

export const intro = {
  title: () => 'Choose your country',
  bodyClass: 'is-intro',
  render: () => html`<div class="intro"><div class="intro-card">
    <div class="intro-top">${logo()}<div><div class="display" style="font-size:30px;line-height:1">Informed Voter</div><div class="eyebrow" style="margin-top:6px">Nonpartisan election guide</div></div></div>
    <div class="intro-body">
      <div class="eyebrow" style="color:var(--brand-2)">Welcome</div>
      <h2 style="margin-top:6px">Know your ballot. <span class="grad-text">Know your candidates.</span></h2>
      <p class="muted">See every race on the map, find what’s on your own ballot from your address, and learn which candidates share your views, issue by issue and with sources.</p>
      <div class="eyebrow" style="margin-top:22px">Choose your country</div>
      ${countryPicker()}
      <dl class="features">
        <div><dt>MAP</dt><dd><b>Every 2026 race, state by state</b>Senate, House, governor and state legislatures, on the real 2026 district maps.</dd></div>
        <div><dt>BALLOT</dt><dd><b>Your elections from your address</b>Matched to your districts by the U.S. Census Bureau, with official how-to-vote links.</dd></div>
        <div><dt>MATCH</dt><dd><b>Candidates who share your views</b>Answer agree-or-disagree questions and see the overlap, with the evidence behind it.</dd></div>
        <div><dt>PRIVACY</dt><dd><b>Your answers stay on your device</b>No account, no server copy of your views or address.</dd></div>
      </dl>
    </div>
  </div></div>`,
  mount: (root) => wireCountryPicker(root),
};

export const country = {
  title: () => 'Which country?',
  render: () => html`<div class="wrap page" style="max-width:880px">
    <div class="eyebrow">Which country?</div>
    <h1>Choose a country</h1>
    <p class="muted">Informed Voter covers the United States today. The United Kingdom, Canada and France are planned; each needs its own election rules, maps and candidate data before it can open.</p>
    ${countryPicker()}
  </div>`,
  mount: (root) => wireCountryPicker(root),
};
