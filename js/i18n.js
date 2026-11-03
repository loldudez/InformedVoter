// Interface language. The France section and the pages every visitor shares (the
// country choice, the help button) speak French or English; the U.S. section stays
// in English. The first visit follows the browser's language list (the first French
// or English entry wins); after that, the visitor's own choice is saved.

import { store } from './store.js';

export const LANGS = ['fr', 'en'];

export function browserLang() {
  const list = navigator.languages?.length ? navigator.languages : [navigator.language || ''];
  for (const l of list) {
    const code = String(l).slice(0, 2).toLowerCase();
    if (LANGS.includes(code)) return code;
  }
  return null;
}

// The France section lives under #/fr; everything else is the U.S. section.
export const section = () => (location.hash.replace(/^#/, '').startsWith('/fr') ? 'fr' : 'us');

// Saved choice, then the browser, then French in the France section and English elsewhere.
export function lang() {
  return store.get().lang || browserLang() || (section() === 'fr' ? 'fr' : 'en');
}

export function setLang(l) {
  if (!LANGS.includes(l) || l === lang()) return;
  store.set({ lang: l });
  window.dispatchEvent(new Event('iv:lang'));
}

// French typography: a narrow no-break space before ? ! ; : and inside « », so the
// punctuation never wraps onto a line of its own. Wording is untouched.
export const frType = (s) => String(s).replace(/ ([?!;:»])/g, ' $1').replace(/« /g, '« ');

// L('Accueil', 'Home'): the France section's pages carry both languages side by side.
export const L = (fr, en) => (lang() === 'fr' ? frType(fr) : en);

// makeT({ fr: {...}, en: {...} }) returns t(key, vars): the string for the current
// language with {name} placeholders filled in. A missing key falls back to the other
// language, then to the key itself, so a gap shows up as English rather than blank.
export function makeT(dict) {
  return (key, vars) => {
    const l = lang();
    let s = dict[l]?.[key] ?? dict[l === 'fr' ? 'en' : 'fr']?.[key] ?? key;
    if (typeof s === 'function') s = s(vars || {});
    else if (vars) s = s.replace(/\{(\w+)\}/g, (m, k) => (vars[k] ?? m));
    return l === 'fr' ? frType(s) : s;
  };
}

// Shared strings: the country choice, the language switch and the help button.
export const t = makeT({
  fr: {
    'lang.switch': 'Langue',
    'lang.fr': 'Français',
    'lang.en': 'English',
    'lang.toEn': 'Switch to English',
    'lang.toFr': 'Passer en français',
    'intro.title': 'Choisissez votre pays',
    'intro.tagline': 'Guide électoral non partisan',
    'intro.welcome': 'Bienvenue',
    'intro.h1a': 'Connaissez votre bulletin.',
    'intro.h1b': 'Connaissez vos candidats.',
    'intro.lead': 'Toutes les élections sur une carte, celles qui vous concernent d’après votre adresse, et les candidats qui partagent vos opinions, question par question et avec des sources.',
    'intro.choose': 'Choisissez votre pays',
    'intro.f1t': 'CARTE', 'intro.f1b': 'Chaque élection, région par région', 'intro.f1d': 'États-Unis : Sénat, Chambre, gouverneurs et assemblées des États. France : la présidentielle 2027, les régions et les départements.',
    'intro.f2t': 'BULLETIN', 'intro.f2b': 'Vos élections d’après votre adresse', 'intro.f2d': 'Votre commune, votre département et votre région, avec les dates des prochains scrutins.',
    'intro.f3t': 'AFFINITÉS', 'intro.f3b': 'Les candidats proches de vos idées', 'intro.f3d': 'Répondez à des questions d’accord ou de désaccord et voyez les points communs, sources à l’appui.',
    'intro.f4t': 'CONFIDENTIALITÉ', 'intro.f4b': 'Vos réponses restent sur votre appareil', 'intro.f4d': 'Pas de compte, aucune copie de vos opinions ni de votre adresse sur un serveur.',
    'country.title': 'Quel pays ?',
    'country.h1': 'Choisissez un pays',
    'country.lead': 'Informed Voter couvre les États-Unis et la France. Le Royaume-Uni et le Canada sont prévus ; chacun demande ses propres règles électorales, cartes et données sur les candidats.',
    'country.us': 'États-Unis', 'country.usSub': 'Élections de mi-mandat 2026 · 3 novembre (en anglais)',
    'country.fr': 'France', 'country.frSub': 'Présidentielle 2027 · régions, départements, villes',
    'country.uk': 'Royaume-Uni', 'country.ca': 'Canada', 'country.soon': 'Bientôt disponible',
    'country.soonTitle': '{name} : bientôt disponible',
  },
  en: {
    'lang.switch': 'Language',
    'lang.fr': 'Français',
    'lang.en': 'English',
    'lang.toEn': 'Switch to English',
    'lang.toFr': 'Passer en français',
    'intro.title': 'Choose your country',
    'intro.tagline': 'Nonpartisan election guide',
    'intro.welcome': 'Welcome',
    'intro.h1a': 'Know your ballot.',
    'intro.h1b': 'Know your candidates.',
    'intro.lead': 'See every race on the map, find what’s on your own ballot from your address, and learn which candidates share your views, issue by issue and with sources.',
    'intro.choose': 'Choose your country',
    'intro.f1t': 'MAP', 'intro.f1b': 'Every race, region by region', 'intro.f1d': 'United States: Senate, House, governor and state legislatures. France: the 2027 presidential election, regions and departments.',
    'intro.f2t': 'BALLOT', 'intro.f2b': 'Your elections from your address', 'intro.f2d': 'Your districts or your commune, department and region, with the dates of the next elections.',
    'intro.f3t': 'MATCH', 'intro.f3b': 'Candidates who share your views', 'intro.f3d': 'Answer agree-or-disagree questions and see the overlap, with the evidence behind it.',
    'intro.f4t': 'PRIVACY', 'intro.f4b': 'Your answers stay on your device', 'intro.f4d': 'No account, no server copy of your views or address.',
    'country.title': 'Which country?',
    'country.h1': 'Choose a country',
    'country.lead': 'Informed Voter covers the United States and France. The United Kingdom and Canada are planned; each needs its own election rules, maps and candidate data before it can open.',
    'country.us': 'United States', 'country.usSub': '2026 midterm elections · November 3',
    'country.fr': 'France', 'country.frSub': '2027 presidential election · regions, departments, cities (in French or English)',
    'country.uk': 'United Kingdom', 'country.ca': 'Canada', 'country.soon': 'Coming soon',
    'country.soonTitle': '{name} coverage is coming soon',
  },
});

// The FR | EN switch shown in the France section's header and on the shared pages.
export function langSwitchHTML() {
  const l = lang();
  const b = (code) => `<button type="button" data-lang="${code}" aria-pressed="${String(l === code)}" lang="${code}" title="${code === 'fr' ? t('lang.toFr') : t('lang.toEn')}">${code.toUpperCase()}</button>`;
  return `<div class="lang-switch" role="group" aria-label="${t('lang.switch')}">${b('fr')}${b('en')}</div>`;
}

export function wireLangSwitch(root) {
  root.querySelectorAll('[data-lang]').forEach((b) => b.addEventListener('click', () => setLang(b.dataset.lang)));
}
