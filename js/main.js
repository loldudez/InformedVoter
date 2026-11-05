import { store } from './store.js';
import { icon } from './icons.js';
import { refreshAvatar } from './components/shell.js';
import { route, currentView, currentSection, rerenderShell } from './router.js';
import { refreshData, stillCounting } from './data/world.js';
import { mountHelp } from './components/help.js';
import { wireReminders } from './components/reminders.js';
import { frStore } from './fr/store.js';

// Stars and hearts work anywhere on any page through one delegated handler.
function onClick(e) {
  // France section: its own starred list, in its own store (pages redraw on change).
  const frStar = e.target.closest('[data-fr-star]');
  if (frStar) { frStore.toggle('starred', frStar.dataset.frStar); return; }
  const star = e.target.closest('[data-star]');
  if (star) {
    const id = star.dataset.star;
    const on = store.toggle('starred', id);
    document.querySelectorAll(`[data-star="${CSS.escape(id)}"]`).forEach((b) => {
      b.setAttribute('aria-pressed', String(on));
      b.setAttribute('aria-label', on ? 'Remove from starred elections' : 'Star this election');
      b.title = on ? 'Starred' : 'Star this election';
      b.innerHTML = String(on ? icon.starFill() : icon.star());
    });
    return;
  }
  const like = e.target.closest('[data-like]');
  if (like) {
    const id = like.dataset.like, name = like.dataset.name;
    const on = store.toggle('liked', id);
    document.querySelectorAll(`[data-like="${CSS.escape(id)}"]`).forEach((b) => {
      b.setAttribute('aria-pressed', String(on));
      b.setAttribute('aria-label', on ? `Remove ${name} from liked candidates` : `Like ${name}`);
      b.title = on ? 'Liked' : 'Like this candidate';
      b.innerHTML = String(on ? icon.heartFill() : icon.heart());
    });
  }
}

function boot() {
  document.addEventListener('click', onClick);
  window.addEventListener('hashchange', () => route());
  window.addEventListener('iv:theme', async () => { await rerenderShell(); route({ keepScroll: true }); });
  window.addEventListener('iv:lang', async () => { await rerenderShell(); route({ keepScroll: true }); });
  window.addEventListener('iv:rerender', () => { refreshAvatar(); route({ keepScroll: true }); });
  // Lists that show starred/liked items redraw when those change, in either section.
  const redrawOn = (_, patch) => {
    const v = currentView();
    if (v?.rerenderOn?.some((k) => k in patch)) route({ keepScroll: true });
  };
  store.subscribe(redrawOn);
  frStore.subscribe(redrawOn);
  if (!store.storageOk) console.warn('Storage unavailable: choices will last only for this visit.');
  mountHelp();
  wireReminders();
  route();
  pollResults();
}

// While races are still being counted, U.S. pages ask every 10 minutes whether the
// results refresh (scripts/update_results.py) has written new counts, and redraw the
// header's ticker and the pages that show results (views marked `live`). A hidden tab
// asks again as soon as it is shown.
const POLL_MS = 10 * 60 * 1000;
function pollResults() {
  let last = Date.now();
  const tick = async () => {
    if (document.hidden || currentSection() !== 'us' || !stillCounting()) return;
    last = Date.now();
    try {
      if (!(await refreshData())) return;
      await rerenderShell();
      if (currentView()?.live) route({ keepScroll: true });
    } catch (e) {
      console.warn('Informed Voter: could not check for new results', e);
    }
  };
  setInterval(tick, POLL_MS);
  document.addEventListener('visibilitychange', () => { if (!document.hidden && Date.now() - last > POLL_MS) tick(); });
}

boot();
