import { store } from './store.js';
import { icon } from './icons.js';
import { initWorld } from './data/world.js';
import { renderShell, refreshAvatar } from './components/shell.js';
import { route, currentView } from './router.js';

// Stars and hearts work anywhere on any page through one delegated handler.
function onClick(e) {
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

async function boot() {
  const app = document.getElementById('app');
  try {
    await initWorld();
  } catch (e) {
    console.error(e);
    app.innerHTML = `<div class="wrap page"><div class="empty"><h3>The site couldn’t load its data.</h3><p>Open it through a local web server rather than by double-clicking the file. See README.md.</p></div></div>`;
    return;
  }
  renderShell();
  document.addEventListener('click', onClick);
  window.addEventListener('hashchange', () => route());
  window.addEventListener('iv:theme', () => { renderShell(); route({ keepScroll: true }); });
  window.addEventListener('iv:rerender', () => { refreshAvatar(); route({ keepScroll: true }); });
  // Lists that show starred/liked items redraw when those change.
  store.subscribe((_, patch) => {
    const v = currentView();
    if (v?.rerenderOn?.some((k) => k in patch)) route({ keepScroll: true });
  });
  if (!store.storageOk) console.warn('Storage unavailable: choices will last only for this visit.');
  route();
}

boot();
