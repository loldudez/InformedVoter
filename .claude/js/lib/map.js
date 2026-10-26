// Interactive SVG maps (national states, or one state's districts) with hover
// highlight, click/keyboard selection, a tooltip, and optional zoom.

import { cssVar } from './charts.js';
import { icon } from '../icons.js';

const W = 960;

// Rating classes, so map colors line up with the "Safe / Likely / Lean / Toss-up" labels.
export function ratingColor(fc) {
  const mid = cssVar('--neutral-mid');
  const poleFor = (party) => (party === 'D' ? cssVar('--dem') : party === 'R' ? cssVar('--rep') : cssVar('--third'));
  if (fc.open) {
    // Open primaries have no win probability; use the forecasters' consensus rating.
    const r = fc.rating || '';
    const t = /Safe|Solid/.test(r) ? 1 : /Likely/.test(r) ? 0.68 : /Lean/.test(r) ? 0.4 : 0;
    return fc.ratingParty ? d3.interpolateLab(mid, poleFor(fc.ratingParty))(t) : mid;
  }
  const p = fc.pLead;
  const t = p >= 0.95 ? 1 : p >= 0.8 ? 0.68 : p >= 0.6 ? 0.4 : 0;
  return d3.interpolateLab(mid, poleFor(fc.lead.party))(t);
}
export const RATING_LEGEND = [
  ['Safe R', 'R', 1], ['Likely R', 'R', 0.68], ['Lean R', 'R', 0.4], ['Toss-up', null, 0],
  ['Lean D', 'D', 0.4], ['Likely D', 'D', 0.68], ['Safe D', 'D', 1],
];
export function ratingLegendHTML(extra = '') {
  const mid = cssVar('--neutral-mid');
  const sw = RATING_LEGEND.map(([label, party, t]) => {
    const pole = party === 'D' ? cssVar('--dem') : party === 'R' ? cssVar('--rep') : mid;
    return `<span><i style="background:${d3.interpolateLab(mid, pole)(t)}"></i>${label}</span>`;
  }).join('');
  return `<div class="map-legend">${sw}${extra}</div>`;
}

export function drawMap(el, fcoll, opts) {
  const {
    fillFor, tooltipFor, onSelect, selectedId = null, labelFor = null,
    zoomable = false, ariaLabel = 'Map', regionLabel = (f) => f.id, maxHeight = 640,
  } = opts;
  el.innerHTML = '';
  el.classList.add('map');

  const proj = d3.geoAlbersUsa();
  const probe = d3.geoPath(proj.fitSize([1000, 1000], fcoll)).bounds(fcoll);
  const aspect = (probe[1][1] - probe[0][1]) / (probe[1][0] - probe[0][0]);
  const H = Math.round(Math.min(maxHeight, Math.max(340, W * aspect)));
  const pad = 14;
  proj.fitExtent([[pad, pad], [W - pad, H - pad]], fcoll);
  const path = d3.geoPath(proj);

  const svg = d3.select(el).append('svg')
    .attr('viewBox', `0 0 ${W} ${H}`).attr('class', 'map-svg')
    .attr('role', 'group').attr('aria-label', ariaLabel);
  const layer = svg.append('g');
  const regions = layer.append('g').attr('class', 'regions');
  const hoverOutline = layer.append('path').attr('class', 'outline-hover');
  const selOutline = layer.append('path').attr('class', 'outline-selected');
  const labels = layer.append('g').attr('class', 'map-labels');

  const tip = document.createElement('div');
  tip.className = 'map-tip';
  tip.hidden = true;
  el.appendChild(tip);

  const showTip = (f, px, py) => {
    const content = tooltipFor ? tooltipFor(f) : null;
    if (!content) { tip.hidden = true; return; }
    tip.innerHTML = String(content);
    tip.hidden = false;
    const r = el.getBoundingClientRect();
    const tw = tip.offsetWidth, th = tip.offsetHeight;
    let left = px + 16, top = py + 16;
    if (left + tw > r.width - 4) left = px - tw - 16;
    if (top + th > r.height - 4) top = py - th - 16;
    tip.style.left = `${Math.max(4, left)}px`;
    tip.style.top = `${Math.max(4, top)}px`;
  };

  let current = selectedId;
  const byId = new Map(fcoll.features.map((f) => [f.id, f]));

  regions.selectAll('path').data(fcoll.features, (f) => f.id).join('path')
    .attr('class', 'region')
    .attr('d', path)
    .attr('fill', (f) => fillFor(f))
    .attr('tabindex', 0)
    .attr('role', 'button')
    .attr('aria-label', (f) => regionLabel(f))
    .attr('aria-pressed', (f) => String(f.id === current))
    .on('pointerenter pointermove', function (ev, f) {
      hoverOutline.attr('d', path(f)).style('opacity', 1);
      const [px, py] = d3.pointer(ev, el);
      showTip(f, px, py);
    })
    .on('pointerleave', () => { hoverOutline.style('opacity', 0); tip.hidden = true; })
    .on('focus', function (ev, f) {
      hoverOutline.attr('d', path(f)).style('opacity', 1);
      const [cx, cy] = path.centroid(f);
      const r = el.getBoundingClientRect();
      showTip(f, (cx / W) * r.width, (cy / H) * r.height);
    })
    .on('blur', () => { hoverOutline.style('opacity', 0); tip.hidden = true; })
    .on('click', (ev, f) => onSelect && onSelect(f))
    .on('keydown', (ev, f) => {
      if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); onSelect && onSelect(f); }
    });

  if (labelFor) {
    labels.selectAll('text').data(fcoll.features.filter((f) => labelFor(f) && path.area(f) > 700)).join('text')
      .attr('transform', (f) => {
        const lp = f.properties.lp ? proj(f.properties.lp) : path.centroid(f);
        return lp ? `translate(${lp[0]},${lp[1]})` : 'translate(-99,-99)';
      })
      .attr('dy', '0.35em').attr('text-anchor', 'middle').text((f) => labelFor(f));
  }

  const select = (id) => {
    current = id;
    const f = byId.get(id);
    selOutline.attr('d', f ? path(f) : null).style('opacity', f ? 1 : 0);
    regions.selectAll('path').attr('aria-pressed', (g) => String(g.id === id));
  };
  select(current);

  let zoom = null;
  if (zoomable) {
    zoom = d3.zoom().scaleExtent([1, 10]).translateExtent([[0, 0], [W, H]])
      .filter((ev) => (ev.type === 'wheel' ? ev.ctrlKey || ev.metaKey : ev.type.startsWith('touch') ? ev.touches.length > 1 : !ev.button))
      .on('zoom', (ev) => {
        layer.attr('transform', ev.transform);
        labels.style('font-size', `${12 / ev.transform.k}px`);
      });
    svg.call(zoom).on('dblclick.zoom', null);
    const ctr = document.createElement('div');
    ctr.className = 'map-zoom';
    ctr.innerHTML = `<button type="button" data-z="in" aria-label="Zoom in">${icon.plus()}</button><button type="button" data-z="out" aria-label="Zoom out">${icon.minus()}</button><button type="button" data-z="reset" aria-label="Reset zoom">${icon.reset()}</button>`;
    ctr.addEventListener('click', (e) => {
      const b = e.target.closest('button');
      if (!b) return;
      const t = svg.transition().duration(300);
      if (b.dataset.z === 'in') zoom.scaleBy(t, 1.6);
      else if (b.dataset.z === 'out') zoom.scaleBy(t, 1 / 1.6);
      else zoom.transform(t, d3.zoomIdentity);
    });
    el.appendChild(ctr);
  }

  return {
    select,
    refill: () => regions.selectAll('path').attr('fill', (f) => fillFor(f)),
    zoomTo(id) {
      const f = byId.get(id);
      if (!f || !zoom) return;
      const [[x0, y0], [x1, y1]] = path.bounds(f);
      const k = Math.min(8, 0.6 / Math.max((x1 - x0) / W, (y1 - y0) / H));
      if (k < 1.6) return; // already easy to see
      const tx = W / 2 - (k * (x0 + x1)) / 2, ty = H / 2 - (k * (y0 + y1)) / 2;
      svg.transition().duration(500).call(zoom.transform, d3.zoomIdentity.translate(tx, ty).scale(k));
    },
  };
}
