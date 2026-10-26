// Underlined glossary terms in the questionnaire. Hovering, focusing or tapping a
// term shows its definition in one shared tooltip, placed next to the term and
// kept inside the screen. Screen readers get the same text as the button's
// description, so the question itself still reads as written.

import { html } from '../util.js';
import { GLOSSARY } from '../data/glossary.js';

const escRe = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
const MATCHERS = GLOSSARY.flatMap((g) => g.phrases.map((p) => ({ g, re: new RegExp(`(?<![\\w-])${escRe(p)}(?![\\w-])`, 'i') })));
const MAX_TERMS = 3;

// The glossary terms in `text`, in reading order: the longest phrase wins where
// two overlap, each term at most once, and at most three per question.
export function termsIn(text) {
  const hits = [];
  for (const { g, re } of MATCHERS) {
    const m = re.exec(text);
    if (m) hits.push({ g, start: m.index, end: m.index + m[0].length });
  }
  hits.sort((a, b) => (b.end - b.start) - (a.end - a.start));
  const kept = [];
  for (const h of hits) {
    if (kept.some((k) => k.g === h.g || (h.start < k.end && k.start < h.end))) continue;
    kept.push(h);
  }
  return kept.slice(0, MAX_TERMS).sort((a, b) => a.start - b.start);
}

// The question text with its glossary terms as buttons.
export function annotate(text) {
  const found = termsIn(text);
  if (!found.length) return text;
  const parts = [];
  let at = 0;
  for (const f of found) {
    parts.push(text.slice(at, f.start));
    parts.push(html`<button type="button" class="term" data-term="${f.g.id}" aria-describedby="def-${f.g.id}" aria-expanded="false">${text.slice(f.start, f.end)}</button>`);
    at = f.end;
  }
  parts.push(text.slice(at));
  return html`${parts}`;
}

// The definitions, hidden on screen, that the term buttons point to.
export function termDefs(text) {
  const found = termsIn(text);
  return found.length ? html`<div class="sr-only">${found.map((f) => html`<span id="def-${f.g.id}">${f.g.def}</span>`)}</div>` : '';
}

const BY_ID = Object.fromEntries(GLOSSARY.map((g) => [g.id, g]));
let tip = null;
let current = null; // the term button the tooltip is showing for
let pinned = false; // opened by a tap or click, so it stays until dismissed
let pinnedAt = 0; // touch screens can send a second click for one tap; ignore it

function tipEl() {
  if (!tip) {
    tip = document.createElement('div');
    tip.className = 'term-tip';
    tip.setAttribute('role', 'tooltip');
    tip.id = 'term-tip';
    tip.hidden = true;
    document.body.appendChild(tip);
    window.addEventListener('hashchange', () => close());
    window.addEventListener('resize', () => { if (current) place(current); });
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && current) { const t = current; close(); t.focus(); } });
    document.addEventListener('click', (e) => { if (pinned && !e.target.closest('.term, .term-tip')) close(); });
  }
  return tip;
}

function open(btn, pin = false) {
  const g = BY_ID[btn.dataset.term];
  if (!g) return;
  const el = tipEl();
  if (current && current !== btn) current.setAttribute('aria-expanded', 'false');
  current = btn;
  pinned = pin;
  if (pin) pinnedAt = Date.now();
  const word = btn.textContent.trim();
  el.innerHTML = String(html`<b>${word.charAt(0).toUpperCase() + word.slice(1)}</b>${g.def}`);
  el.hidden = false;
  btn.setAttribute('aria-expanded', 'true');
  place(btn);
}

// Below the term, centered on it and clamped to the screen with a 16px gutter;
// above it instead when there isn't room underneath.
function place(btn) {
  const el = tipEl();
  const r = btn.getBoundingClientRect();
  const vw = document.documentElement.clientWidth;
  const w = el.offsetWidth, h = el.offsetHeight;
  const left = Math.max(16, Math.min(r.left + r.width / 2 - w / 2, vw - 16 - w));
  let top = r.bottom + 10;
  if (top + h > window.innerHeight - 8 && r.top - 10 - h > 8) top = r.top - 10 - h;
  el.style.left = `${left + window.scrollX}px`;
  el.style.top = `${top + window.scrollY}px`;
}

function close() {
  if (tip) tip.hidden = true;
  if (current) current.setAttribute('aria-expanded', 'false');
  current = null;
  pinned = false;
}
// For views that redraw their terms (the questionnaire moving to the next question).
export const closeTerm = close;

// Wires every term inside `root`, once; terms drawn into it later work too.
export function wireTerms(root) {
  if (!root || root._terms) return;
  root._terms = true;
  root.addEventListener('mouseover', (e) => {
    const b = e.target.closest('.term');
    if (b && !pinned) open(b);
  });
  root.addEventListener('mouseout', (e) => {
    const b = e.target.closest('.term');
    if (b && b === current && !pinned && !b.contains(e.relatedTarget)) close();
  });
  root.addEventListener('focusin', (e) => {
    const b = e.target.closest('.term');
    if (b && b !== current) open(b);
  });
  // Moving focus to anything else closes it, even when a click opened it.
  root.addEventListener('focusout', (e) => {
    const b = e.target.closest('.term');
    if (b && b === current && (!pinned || e.relatedTarget)) close();
  });
  // A tap or click keeps the definition open; a second one on the same term closes it.
  root.addEventListener('click', (e) => {
    const b = e.target.closest('.term');
    if (!b) return;
    e.preventDefault();
    if (b === current && pinned) {
      if (Date.now() - pinnedAt > 400) close();
    } else open(b, true);
  });
}
