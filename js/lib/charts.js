// Chart helpers. Specs follow the site's data-viz rules: 2px lines, hairline grid,
// a crosshair tooltip that lists every series, 8px end dots with a surface ring,
// legends for two or more series, and no dual axes.

import { esc, debounce } from '../util.js';

export const cssVar = (name) => getComputedStyle(document.documentElement).getPropertyValue(name).trim();

export const PARTY_VAR = { D: '--dem', R: '--rep' };
// Democrats blue, Republicans red; the strongest other candidate green, the rest gray.
// (Validated as a set: blue/red/green clears the colorblind checks in both themes.)
export function partyColor(party, rankAmongOthers = 0) {
  if (PARTY_VAR[party]) return cssVar(PARTY_VAR[party]);
  return rankAmongOthers === 0 ? cssVar('--third') : cssVar('--other');
}
export function candColors(cands) {
  let others = 0;
  const out = {};
  for (const c of cands) out[c.id] = PARTY_VAR[c.party] ? cssVar(PARTY_VAR[c.party]) : partyColor(c.party, others++);
  return out;
}

const timeFmt = (span) => (span > 400 * 864e5 ? d3.timeFormat('%b %Y') : d3.timeFormat('%b %-d'));

// series: [{ name, color, values: [{ x: Date, y: number }], points?: [{ x: Date, y, title }] }]
// `points` are drawn as dots behind the line (e.g. the individual polls behind an average).
export function lineChart(el, opts) {
  const draw = () => drawLine(el, opts);
  draw();
  if (el._ro) el._ro.disconnect();
  let lastW = el.clientWidth;
  el._ro = new ResizeObserver(debounce(() => {
    if (Math.abs(el.clientWidth - lastW) > 4) { lastW = el.clientWidth; draw(); }
  }, 120));
  el._ro.observe(el);
}

function drawLine(el, { series, height = 220, yFormat = (v) => v.toFixed(1), tipFormat, yDomain, area = false, baseline = null, label = 'Chart', endLabels = true }) {
  el.innerHTML = '';
  const all = series.flatMap((s) => s.values);
  if (!all.length) {
    el.innerHTML = '<p class="muted small">No data yet.</p>';
    return;
  }
  const W = Math.max(280, el.clientWidth || 600);
  const showEnd = endLabels && series.length <= 4;
  const m = { top: 14, right: showEnd ? 58 : 14, bottom: 26, left: 46 };

  if (series.length > 1) {
    const legend = document.createElement('div');
    legend.className = 'chart-legend';
    legend.innerHTML = series.map((s) => `<span><i class="key-line" style="background:${s.color}"></i>${esc(s.name)}</span>`).join('');
    el.appendChild(legend);
  }

  const pts = series.flatMap((s) => s.points || []);
  const x = d3.scaleTime().domain(d3.extent(all, (d) => d.x)).range([m.left, W - m.right]);
  let [lo, hi] = yDomain || d3.extent([...all, ...pts], (d) => d.y);
  if (!yDomain) {
    const pad = (hi - lo) * 0.12 || Math.abs(hi) * 0.1 || 1;
    lo -= pad; hi += pad;
    if (baseline != null) { lo = Math.min(lo, baseline); hi = Math.max(hi, baseline); }
  }
  const y = d3.scaleLinear().domain([lo, hi]).nice(4).range([height - m.bottom, m.top]);

  const svg = d3.select(el).append('svg')
    .attr('viewBox', `0 0 ${W} ${height}`).attr('width', '100%').attr('height', height)
    .attr('role', 'img').attr('aria-label', label).attr('class', 'chart-svg');

  svg.append('g').attr('class', 'grid')
    .selectAll('line').data(y.ticks(4)).join('line')
    .attr('x1', m.left).attr('x2', W - m.right).attr('y1', (d) => y(d)).attr('y2', (d) => y(d));
  svg.append('g').attr('class', 'axis-label')
    .selectAll('text').data(y.ticks(4)).join('text')
    .attr('x', m.left - 8).attr('y', (d) => y(d)).attr('dy', '0.32em').attr('text-anchor', 'end').text(yFormat);
  if (baseline != null && baseline > y.domain()[0] && baseline < y.domain()[1]) {
    svg.append('line').attr('class', 'baseline').attr('x1', m.left).attr('x2', W - m.right).attr('y1', y(baseline)).attr('y2', y(baseline));
  }
  const span = x.domain()[1] - x.domain()[0];
  const fmt = timeFmt(span);
  svg.append('g').attr('class', 'axis-label')
    .selectAll('text').data(x.ticks(Math.max(2, Math.floor(W / 130)))).join('text')
    .attr('x', (d) => x(d)).attr('y', height - 6).attr('text-anchor', 'middle').text(fmt);

  const line = d3.line().defined((d) => d.y != null).x((d) => x(d.x)).y((d) => y(d.y)).curve(d3.curveMonotoneX);
  if (area && series.length === 1) {
    const a = d3.area().defined((d) => d.y != null).x((d) => x(d.x)).y0(y(Math.max(y.domain()[0], baseline ?? y.domain()[0]))).y1((d) => y(d.y)).curve(d3.curveMonotoneX);
    svg.append('path').datum(series[0].values).attr('class', 'area').attr('fill', series[0].color).attr('d', a);
  }
  for (const s of series) {
    if (!s.points?.length) continue;
    svg.append('g').attr('class', 'poll-dots').selectAll('circle').data(s.points.filter((d) => d.x >= x.domain()[0])).join('circle')
      .attr('cx', (d) => x(d.x)).attr('cy', (d) => y(d.y)).attr('r', 3.5).attr('fill', s.color);
  }
  const ends = [];
  for (const s of series) {
    svg.append('path').datum(s.values).attr('class', 'line').attr('stroke', s.color).attr('d', line);
    const last = [...s.values].reverse().find((d) => d.y != null);
    if (last) {
      svg.append('circle').attr('class', 'end-dot').attr('cx', x(last.x)).attr('cy', y(last.y)).attr('r', 4).attr('fill', s.color);
      ends.push({ x: x(last.x) + 8, y: y(last.y), text: yFormat(last.y) });
    }
  }
  if (showEnd) {
    // Nudge end labels apart so close values (48% and 46%) don't print on top of each other.
    ends.sort((a, b) => a.y - b.y);
    for (let i = 1; i < ends.length; i++) ends[i].y = Math.max(ends[i].y, ends[i - 1].y + 13);
    for (const e of ends) svg.append('text').attr('class', 'end-label').attr('x', e.x).attr('y', e.y).attr('dy', '0.32em').text(e.text);
  }

  // Crosshair + one tooltip listing every series at the hovered date.
  const xs = series[0].values.map((d) => d.x);
  const cross = svg.append('line').attr('class', 'crosshair').attr('y1', m.top).attr('y2', height - m.bottom).style('opacity', 0);
  const tip = document.createElement('div');
  tip.className = 'chart-tip';
  tip.hidden = true;
  el.style.position = 'relative';
  el.appendChild(tip);
  const tipFmt = tipFormat || yFormat;
  const bis = d3.bisector((d) => d).center;
  svg.append('rect').attr('class', 'hit').attr('x', m.left).attr('y', m.top).attr('width', W - m.left - m.right).attr('height', height - m.top - m.bottom)
    .on('pointermove', (ev) => {
      const [px] = d3.pointer(ev);
      const i = bis(xs, x.invert(px));
      const dx = xs[i];
      cross.attr('x1', x(dx)).attr('x2', x(dx)).style('opacity', 1);
      const rows = series.map((s) => {
        const pt = s.values.find((v) => +v.x === +dx);
        return `<div class="tip-row"><i class="key-line" style="background:${s.color}"></i><strong>${pt && pt.y != null ? esc(tipFmt(pt.y)) : '—'}</strong><span>${esc(s.name)}</span></div>`;
      }).join('');
      const today = +d3.timeDay.floor(dx);
      const polls = [...new Set(pts.filter((p) => p.title && +d3.timeDay.floor(p.x) === today).map((p) => p.title.split(':')[0]))];
      const pollNote = polls.length ? `<div class="tip-date" style="margin-top:6px">Poll${polls.length > 1 ? 's' : ''} ending this day: ${esc(polls.join(', '))}</div>` : '';
      tip.innerHTML = `<div class="tip-date">${esc(d3.timeFormat('%b %-d, %Y')(dx))}</div>${rows}${pollNote}`;
      tip.hidden = false;
      const rect = el.getBoundingClientRect();
      const left = (x(dx) / W) * rect.width;
      tip.style.left = `${Math.min(rect.width - tip.offsetWidth - 4, Math.max(4, left + 12))}px`;
      tip.style.top = '28px';
    })
    .on('pointerleave', () => { cross.style('opacity', 0); tip.hidden = true; });
}

export function sparkline(values, { width = 120, height = 32, color = 'currentColor', label = '' } = {}) {
  const v = values.filter((d) => d != null);
  if (v.length < 2) return '';
  const lo = Math.min(...v), hi = Math.max(...v);
  const pad = 3;
  const sx = (i) => pad + (i / (values.length - 1)) * (width - pad * 2);
  const sy = (d) => (hi === lo ? height / 2 : pad + (1 - (d - lo) / (hi - lo)) * (height - pad * 2));
  const pts = values.map((d, i) => (d == null ? null : `${sx(i).toFixed(1)},${sy(d).toFixed(1)}`)).filter(Boolean).join(' ');
  const li = values.length - 1;
  return `<svg class="spark" viewBox="0 0 ${width} ${height}" width="${width}" height="${height}" role="img" aria-label="${esc(label)}"><polyline points="${pts}" fill="none" stroke="${color}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/><circle cx="${sx(li)}" cy="${sy(values[li])}" r="3" fill="${color}"/></svg>`;
}

// 100 squares, one per simulated election, filled in order of each side's chance.
export function waffle(parts) {
  const cells = [];
  let n = 0;
  const counts = parts.map((p) => Math.round(p.share * 100));
  const diff = 100 - counts.reduce((a, b) => a + b, 0);
  counts[0] += diff;
  parts.forEach((p, i) => { for (let k = 0; k < counts[i]; k++, n++) cells.push(`<i style="background:${p.color}" title="${esc(p.name)}"></i>`); });
  return `<div class="waffle" role="img" aria-label="${esc(parts.map((p, i) => `${p.name} wins about ${counts[i]} of 100 simulations`).join(', '))}">${cells.join('')}</div>`;
}

// Twenty segments lit in proportion to a share, like a level meter.
export function segments(share, color, total = 20) {
  const lit = Math.round((share / 100) * total);
  let s = '';
  for (let i = 0; i < total; i++) s += `<i${i < lit ? ` style="background:${color}"` : ''}></i>`;
  return `<div class="segments" aria-hidden="true">${s}</div>`;
}

// Horizontal part-to-whole bar with 2px surface gaps between segments.
export function stackedBar(parts, { label = '' } = {}) {
  const total = parts.reduce((a, p) => a + p.value, 0) || 1;
  const segs = parts.filter((p) => p.value > 0).map((p) => `<span style="flex:${p.value / total};background:${p.color}" title="${esc(p.name)}: ${(p.value / total * 100).toFixed(0)}%"></span>`).join('');
  return `<div class="stackbar" role="img" aria-label="${esc(label)}">${segs}</div>`;
}
