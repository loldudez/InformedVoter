import { store } from './store.js';
import { initWorld } from './data/world.js';
import { renderShell, markActive } from './components/shell.js';
import { intro, country } from './views/intro.js';
import { home } from './views/home.js';
import { stateView } from './views/state.js';
import { racePage } from './views/race.js';
import { profile } from './views/profile.js';
import { viewsQuiz, electionQuiz } from './views/quiz.js';
import { elections, match } from './views/elections.js';
import { starred, liked, close, donations } from './views/lists.js';
import { news, inflation, parties, donate, about } from './views/info.js';
import { congress } from './views/congress.js';
import { upcoming } from './views/upcoming.js';
import { FR_ROUTES } from './fr/routes.js';
import { renderFrShell } from './fr/shell.js';
import { lang } from './i18n.js';

const ROUTES = [
  [/^\/$/, home],
  [/^\/intro$/, intro],
  [/^\/country$/, country],
  [/^\/state\/([A-Z]{2})$/, stateView],
  [/^\/race\/(.+)$/, racePage],
  [/^\/profile$/, profile],
  [/^\/views$/, viewsQuiz],
  [/^\/elections$/, elections],
  [/^\/elections\/([^/]+)\/quiz$/, electionQuiz],
  [/^\/elections\/([^/]+)\/match$/, match],
  [/^\/starred$/, starred],
  [/^\/liked$/, liked],
  [/^\/close$/, close],
  [/^\/donations$/, donations],
  [/^\/news$/, news],
  [/^\/inflation$/, inflation],
  [/^\/parties$/, parties],
  [/^\/congress$/, congress],
  [/^\/upcoming$/, upcoming],
  [/^\/donate$/, donate],
  [/^\/about$/, about],
  ...FR_ROUTES,
];

// Pages that every visitor shares, whichever section they came from: they need no
// U.S. race data and keep the header of the section the visitor was in.
const SHARED = new Set([intro, country]);

let current = null;   // { view, path, cleanup }
let token = 0;
let shellFor = null;  // which section's header is on screen
let lastSection = store.get().country === 'fr' ? 'fr' : 'us';

// The U.S. race data (several megabytes) loads once, and only when a U.S. page opens.
let world = null;
export const ensureWorld = () => (world ??= initWorld());

export function parseHash() {
  const h = location.hash.replace(/^#/, '') || '/';
  const [path, qs = ''] = h.split('?');
  return { path: path || '/', query: Object.fromEntries(new URLSearchParams(qs)) };
}

export async function renderCurrentShell(sec = lastSection) {
  if (sec === 'us') await ensureWorld();
  shellFor = sec;
  if (sec === 'fr') await renderFrShell();
  else {
    document.getElementById('ticker').hidden = false; // the France header may have hidden it
    renderShell();
  }
}

// Redraw the header that is on screen (after a theme or language change), if any.
export async function rerenderShell() {
  if (shellFor) await renderCurrentShell(shellFor);
}

export async function route({ keepScroll = false } = {}) {
  const my = ++token;
  const { path, query } = parseHash();
  let view = null, params = [];
  for (const [re, v] of ROUTES) {
    const m = path.match(re);
    if (m) { view = v; params = m.slice(1); break; }
  }
  if (!view) { location.hash = '#/'; return; }
  const st = store.get();
  // Someone who chose France lands on the France section when they open the site.
  if (view === home && st.countryChosen && st.country === 'fr') { location.hash = '#/fr'; return; }
  if (view === home && !st.countryChosen) view = intro;

  const sec = SHARED.has(view) ? lastSection : path.startsWith('/fr') ? 'fr' : 'us';
  lastSection = sec;
  // The intro hides the header, so it needs neither a header nor the U.S. data.
  const needShell = view.bodyClass !== 'is-intro';
  try {
    if (needShell && shellFor !== sec) await renderCurrentShell(sec);
    else if (needShell && sec === 'us') await ensureWorld();
  } catch (e) {
    console.error(e);
    if (my !== token) return;
    document.getElementById('app').innerHTML = `<div class="wrap page"><div class="empty"><h3>The site couldn’t load its data.</h3><p>Open it through a local web server rather than by double-clicking the file. See README.md.</p></div></div>`;
    return;
  }
  if (my !== token) return;
  document.documentElement.lang = sec === 'fr' || SHARED.has(view) ? lang() : 'en';

  const ctx = { path, query, params };
  const app = document.getElementById('app');
  const samePath = current && current.path === path;
  current?.cleanup?.();
  document.body.className = [view.bodyClass || '', `sec-${sec}`].join(' ').trim();
  document.title = `${view.title(ctx)} · Informed Voter`;

  let out;
  try {
    out = await view.render(ctx);
  } catch (e) {
    console.error(e);
    out = `<div class="wrap page"><div class="empty"><h3>${sec === 'fr' && lang() === 'fr' ? 'Cette page n’a pas pu se charger.' : 'Something went wrong loading this page.'}</h3><p>${String(e.message || e).replace(/[<>&]/g, '')}</p><a class="btn" href="${sec === 'fr' ? '#/fr' : '#/'}">${sec === 'fr' && lang() === 'fr' ? 'Retour à la carte' : 'Back to the map'}</a></div></div>`;
  }
  if (my !== token) return; // a newer navigation won the race
  app.innerHTML = String(out);
  current = { view, path, cleanup: null };
  try {
    current.cleanup = (await view.mount?.(app, ctx)) || null;
  } catch (e) {
    console.error(e);
  }
  if (!samePath && !keepScroll) {
    window.scrollTo(0, 0);
    app.focus({ preventScroll: true });
  }
  markActive(`#${path}`);
}

export const currentView = () => current?.view;
export const currentSection = () => lastSection;
