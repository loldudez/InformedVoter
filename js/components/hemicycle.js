// Half-circle seat charts for parliaments: France's Assemblée nationale and Sénat
// (js/fr/views/parlement.js) and the U.S. House and Senate (js/views/congress.js).
// Seats sit in concentric rows, each holding as many as its length allows, and fill
// left to right in the groups' order, so each group forms a wedge; empty seats stay
// hollow at the right end. Groups that share a color get their own seat shape.
// Hovering or tapping a seat, or moving through the seats with the arrow keys, shows
// who sits there; the key under the chart highlights a group.

import { html, raw, esc } from '../util.js';

const W = 1000;
const R = 480; // the outer row's radius in the viewBox
const INNER = 0.36; // the inner row's radius, as a share of the outer one
const r1 = (v) => Math.round(v * 10) / 10;

// n seats in half-circle rows: their centers from left to right, and the seat size.
export function seatLayout(n) {
  // Seats per row follow the row's length, and the number of rows keeps the gap
  // between rows close to the gap between neighbors in a row.
  const k = (Math.PI * (1 + INNER)) / (2 * (1 - INNER));
  const rows = Math.max(2, Math.round((1 + Math.sqrt(1 + (4 * n) / k)) / 2));
  const radii = Array.from({ length: rows }, (_, i) => INNER + ((1 - INNER) * i) / (rows - 1));
  const sum = radii.reduce((a, b) => a + b, 0);
  const exact = radii.map((r) => (n * r) / sum);
  const counts = exact.map(Math.floor);
  const short = n - counts.reduce((a, b) => a + b, 0);
  exact.map((x, i) => [x - counts[i], i]).sort((a, b) => b[0] - a[0]).slice(0, short)
    .forEach(([, i]) => { counts[i] += 1; });
  const polar = [];
  radii.forEach((r, i) => {
    for (let j = 0; j < counts[i]; j++) polar.push({ r, a: counts[i] === 1 ? Math.PI / 2 : Math.PI * (1 - j / (counts[i] - 1)) });
  });
  // Left to right; on the same ray, the inner row first.
  polar.sort((p, q) => q.a - p.a || p.r - q.r);
  const gap = Math.min((1 - INNER) / (rows - 1), ...radii.map((r, i) => (counts[i] > 1 ? (Math.PI * r) / (counts[i] - 1) : 1)));
  const size = 0.4 * gap * R;
  const cy = R + size + 3;
  return {
    size, cy, height: cy + size + 3,
    seats: polar.map(({ r, a }) => ({ x: W / 2 + Math.cos(a) * r * R, y: cy - Math.sin(a) * r * R })),
  };
}

// One seat: circle, square, diamond or triangle of about the same weight.
function mark(shape, x, y, s) {
  x = r1(x); y = r1(y);
  if (shape === 'square') { const h = r1(s * 0.88); return `<rect x="${r1(x - h)}" y="${r1(y - h)}" width="${r1(2 * h)}" height="${r1(2 * h)}" rx="${r1(s * 0.2)}"/>`; }
  if (shape === 'diamond') { const h = r1(s * 1.22); return `<path d="M${x} ${r1(y - h)}L${r1(x + h)} ${y}L${x} ${r1(y + h)}L${r1(x - h)} ${y}Z"/>`; }
  if (shape === 'triangle') { const h = s * 1.3; return `<path d="M${x} ${r1(y - h)}L${r1(x + h * 0.87)} ${r1(y + h / 2)}L${r1(x - h * 0.87)} ${r1(y + h / 2)}Z"/>`; }
  return `<circle cx="${x}" cy="${y}" r="${r1(s)}"/>`;
}

// A group's seat shape in its color, for keys and tooltips.
export const swatch = (g, px = 14) => raw(`<svg class="hemi-swatch" width="${px}" height="${px}" viewBox="0 0 16 16" aria-hidden="true" focusable="false" style="fill:${esc(g.color)}">${mark(g.shape, 8, 8, 6)}</svg>`);

export function drawHemicycle(el, opts) {
  const {
    seats: total, groups, tipFor, vacantTip = '', ariaLabel = '', hint = '', center = [],
    legendItem = (g) => g.id, legendLabel = '',
  } = opts;
  const order = new Map(groups.map((g, i) => [g.id, i]));
  const members = opts.members.filter((m) => order.has(m.g)).sort((a, b) => order.get(a.g) - order.get(b.g));
  const lay = seatLayout(Math.max(total, members.length));
  const { size } = lay;

  // Seat i holds members[i]; the seats after the last member are vacant.
  const starts = [];
  let at = 0;
  const layers = groups.map((g) => {
    const n = members.filter((m) => m.g === g.id).length;
    starts.push(at);
    const body = lay.seats.slice(at, at + n).map((p) => mark(g.shape, p.x, p.y, size)).join('');
    at += n;
    return `<g class="hemi-group" data-g="${esc(g.id)}" style="fill:${esc(g.color)}">${body}</g>`;
  }).join('');
  const vacant = lay.seats.slice(at).map((p) => mark('circle', p.x, p.y, size * 0.8)).join('');
  // Up to three lines in the middle: a big number, then two short labels.
  const lines = center.slice(0, 3).map((t, i) => `<text class="hemi-c${i}" x="${W / 2}" y="${r1(lay.cy - [74, 40, 12][i])}">${esc(t)}</text>`).join('');
  const hintId = `hemi-hint-${Math.random().toString(36).slice(2, 8)}`;

  el.innerHTML = String(html`<div class="hemi-chart">
      <svg class="hemi-svg" viewBox="0 0 ${W} ${r1(lay.height)}" role="img" tabindex="0" aria-label="${ariaLabel}" ${raw(hint ? `aria-describedby="${hintId}"` : '')}>${raw(layers)}<g class="hemi-vacant">${raw(vacant)}</g>${raw(lines)}<circle class="hemi-ring" r="${r1(size + 4)}" cx="-50" cy="-50"/></svg>
      <div class="map-tip" hidden></div>
    </div>
    ${hint ? html`<p class="tiny faint hemi-hint" id="${hintId}">${hint}</p>` : ''}
    <p class="sr-only" aria-live="polite"></p>
    <div class="hemi-key" role="group" aria-label="${legendLabel}">${groups.map((g) => html`<button type="button" class="hemi-key-item" data-g="${g.id}" aria-pressed="false">${swatch(g)}<span class="hemi-key-text">${legendItem(g)}</span></button>`)}</div>`);

  const chart = el.querySelector('.hemi-chart');
  const svg = chart.querySelector('svg');
  const tip = chart.querySelector('.map-tip');
  const ring = svg.querySelector('.hemi-ring');
  const live = el.querySelector('[aria-live]');
  let active = -1, pinned = null;

  const hide = () => { tip.hidden = true; ring.style.opacity = 0; active = -1; };
  // vacantTip is one tooltip for every empty seat, or a function of the empty seat's
  // number (0 for the first).
  const show = (i, px, py) => {
    const content = i < members.length ? tipFor(members[i])
      : typeof vacantTip === 'function' ? vacantTip(i - members.length) : vacantTip;
    if (!content) { hide(); return; }
    tip.innerHTML = String(content);
    tip.hidden = false;
    const r = chart.getBoundingClientRect();
    const tw = tip.offsetWidth, th = tip.offsetHeight;
    let left = px + 16, top = py + 16;
    if (left + tw > r.width - 4) left = px - tw - 16;
    if (top + th > r.height - 4) top = py - th - 16;
    tip.style.left = `${Math.max(4, left)}px`;
    tip.style.top = `${Math.max(4, top)}px`;
    ring.setAttribute('cx', r1(lay.seats[i].x));
    ring.setAttribute('cy', r1(lay.seats[i].y));
    ring.style.opacity = 1;
    active = i;
  };
  // The nearest seat within reach of the pointer, so the gaps between seats count too.
  const seatAt = (ev) => {
    const m = svg.getScreenCTM();
    if (!m) return -1;
    const p = new DOMPoint(ev.clientX, ev.clientY).matrixTransform(m.inverse());
    let best = -1, bd = (size * 2.2) ** 2;
    lay.seats.forEach((s, i) => { const d = (s.x - p.x) ** 2 + (s.y - p.y) ** 2; if (d < bd) { bd = d; best = i; } });
    return best;
  };
  const onPointer = (ev) => {
    const i = seatAt(ev);
    if (i < 0) { hide(); return; }
    const r = chart.getBoundingClientRect();
    show(i, ev.clientX - r.left, ev.clientY - r.top);
  };
  svg.addEventListener('pointermove', onPointer);
  svg.addEventListener('pointerdown', onPointer);
  // A finger lifting also "leaves"; a tap elsewhere closes the tooltip instead.
  svg.addEventListener('pointerleave', (ev) => { if (ev.pointerType === 'mouse') hide(); });
  const outside = (ev) => { if (!svg.contains(ev.target)) hide(); };
  document.addEventListener('pointerdown', outside);

  svg.addEventListener('keydown', (ev) => {
    const last = lay.seats.length - 1;
    const group = starts.findLastIndex((s) => s <= Math.max(0, active));
    let i;
    if (ev.key === 'ArrowRight' || ev.key === 'ArrowDown') i = Math.min(last, active + 1);
    else if (ev.key === 'ArrowLeft' || ev.key === 'ArrowUp') i = Math.max(0, active - 1);
    else if (ev.key === 'PageDown') i = group + 1 < starts.length ? starts[group + 1] : last;
    else if (ev.key === 'PageUp') i = active > starts[group] ? starts[group] : starts[Math.max(0, group - 1)];
    else if (ev.key === 'Home') i = 0;
    else if (ev.key === 'End') i = last;
    else if (ev.key === 'Escape') { hide(); return; }
    else return;
    ev.preventDefault();
    const m = svg.getScreenCTM();
    const r = chart.getBoundingClientRect();
    const p = new DOMPoint(lay.seats[i].x, lay.seats[i].y).matrixTransform(m);
    show(i, p.x - r.left, p.y - r.top);
    live.textContent = tip.hidden ? '' : tip.textContent.replace(/\s+/g, ' ').trim();
  });
  svg.addEventListener('blur', hide);

  // The key: hover or focus previews a group, a click keeps it highlighted.
  const layerEls = [...svg.querySelectorAll('.hemi-group')];
  const vacantEl = svg.querySelector('.hemi-vacant');
  const keys = [...el.querySelectorAll('.hemi-key-item')];
  const highlight = (id) => {
    layerEls.forEach((g) => g.classList.toggle('dim', id != null && g.dataset.g !== id));
    vacantEl.classList.toggle('dim', id != null);
  };
  for (const b of keys) {
    b.addEventListener('click', () => {
      pinned = pinned === b.dataset.g ? null : b.dataset.g;
      keys.forEach((x) => x.setAttribute('aria-pressed', String(x.dataset.g === pinned)));
      highlight(pinned);
    });
    b.addEventListener('pointerenter', (ev) => { if (ev.pointerType === 'mouse') highlight(b.dataset.g); });
    b.addEventListener('pointerleave', (ev) => { if (ev.pointerType === 'mouse') highlight(pinned); });
    b.addEventListener('focus', () => highlight(b.dataset.g));
    b.addEventListener('blur', () => highlight(pinned));
  }

  return { destroy: () => document.removeEventListener('pointerdown', outside) };
}
