import { html, raw } from '../util.js';
import { logo, icon } from '../icons.js';
import { FLAGS } from '../components/flags.js';
import { store } from '../store.js';
import { t, langSwitchHTML, wireLangSwitch } from '../i18n.js';

// These pages are shared by both sections, so they speak the visitor's language.
const COUNTRIES = () => [
  { id: 'us', name: t('country.us'), sub: t('country.usSub'), href: '#/', active: true },
  { id: 'fr', name: t('country.fr'), sub: t('country.frSub'), href: '#/fr', active: true },
  { id: 'uk', name: t('country.uk'), sub: t('country.soon') },
  { id: 'ca', name: t('country.ca'), sub: t('country.soon') },
];

export function countryPicker() {
  return html`<div class="countries">${COUNTRIES().map((c) => (c.active
    ? html`<a class="country" href="${c.href}" data-choose-country="${c.id}"><span class="flag">${raw(FLAGS[c.id])}</span><span><span class="cn">${c.name}</span><br><span class="cs">${c.sub}</span></span><span class="go">${icon.chevronRight()}</span></a>`
    : html`<div class="country disabled" aria-disabled="true" title="${t('country.soonTitle', { name: c.name })}"><span class="flag">${raw(FLAGS[c.id])}</span><span><span class="cn">${c.name}</span><br><span class="cs">${c.sub}</span></span></div>`))}</div>`;
}

export function wireCountryPicker(root) {
  root.querySelectorAll('[data-choose-country]').forEach((a) => a.addEventListener('click', (e) => {
    e.preventDefault();
    const id = a.dataset.chooseCountry;
    store.set({ countryChosen: true, country: id });
    const to = a.getAttribute('href');
    // The intro lives at #/ too, so changing the hash alone wouldn't redraw.
    if (location.hash === to || (to === '#/' && !location.hash)) window.dispatchEvent(new Event('iv:rerender'));
    else location.hash = to;
  }));
}

export const intro = {
  title: () => t('intro.title'),
  bodyClass: 'is-intro',
  render: () => html`<div class="intro"><div class="intro-card">
    <div class="intro-top">${logo()}<div style="flex:1"><div class="display" style="font-size:30px;line-height:1">Informed Voter</div><div class="eyebrow" style="margin-top:6px">${t('intro.tagline')}</div></div>${raw(langSwitchHTML())}</div>
    <div class="intro-body">
      <div class="eyebrow" style="color:var(--brand-2)">${t('intro.welcome')}</div>
      <h2 style="margin-top:6px">${t('intro.h1a')} <span class="grad-text">${t('intro.h1b')}</span></h2>
      <p class="muted">${t('intro.lead')}</p>
      <div class="eyebrow" style="margin-top:22px">${t('intro.choose')}</div>
      ${countryPicker()}
      <dl class="features">
        ${[1, 2, 3, 4].map((k) => html`<div><dt>${t(`intro.f${k}t`)}</dt><dd><b>${t(`intro.f${k}b`)}</b>${t(`intro.f${k}d`)}</dd></div>`)}
      </dl>
    </div>
  </div></div>`,
  mount: (root) => { wireCountryPicker(root); wireLangSwitch(root); },
};

export const country = {
  title: () => t('country.title'),
  render: () => html`<div class="wrap page" style="max-width:880px">
    <div class="row between"><div class="eyebrow">${t('country.title')}</div>${raw(langSwitchHTML())}</div>
    <h1>${t('country.h1')}</h1>
    <p class="muted">${t('country.lead')}</p>
    ${countryPicker()}
  </div>`,
  mount: (root) => { wireCountryPicker(root); wireLangSwitch(root); },
};
