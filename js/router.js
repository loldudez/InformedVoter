import { store } from './store.js';
import { markActive } from './components/shell.js';
import { intro, country } from './views/intro.js';
import { home } from './views/home.js';
import { stateView } from './views/state.js';
import { racePage } from './views/race.js';
import { profile } from './views/profile.js';
import { viewsQuiz, electionQuiz } from './views/quiz.js';
import { elections, match } from './views/elections.js';
import { starred, liked, close, donations } from './views/lists.js';
import { news, inflation, parties, donate, about } from './views/info.js';

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
  [/^\/donate$/, donate],
  [/^\/about$/, about],
];

let current = null;   // { view, path, cleanup }
let token = 0;

export function parseHash() {
  const h = location.hash.replace(/^#/, '') || '/';
  const [path, qs = ''] = h.split('?');
  return { path: path || '/', query: Object.fromEntries(new URLSearchParams(qs)) };
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
  if (view === home && !store.get().countryChosen) view = intro;

  const ctx = { path, query, params };
  const app = document.getElementById('app');
  const samePath = current && current.path === path;
  current?.cleanup?.();
  document.body.className = view.bodyClass || '';
  document.title = `${view.title(ctx)} · Informed Voter`;

  let out;
  try {
    out = await view.render(ctx);
  } catch (e) {
    console.error(e);
    out = `<div class="wrap page"><div class="empty"><h3>Something went wrong loading this page.</h3><p>${String(e.message || e).replace(/[<>&]/g, '')}</p><a class="btn" href="#/">Back to the map</a></div></div>`;
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
