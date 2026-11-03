// France's interactive map: regions or departments, with the overseas departments in
// inset frames and the largest cities as clickable markers. Hover or focus shows a
// tooltip; click, Enter or Space opens the region, department or city.
//
// The projection is a conformal conic close to Lambert-93, the official projection for
// mainland France; the overseas insets were moved and scaled by scripts/fr/build_maps_fr.py.

const W = 960;

export function drawFrance(el, fcoll, opts) {
  const {
    fillFor = () => 'var(--surface-3)', tooltipFor, onSelect, onCity, cities = [], labelFor = null,
    selectedId = null, focusIds = null, ariaLabel = 'Carte', regionLabel = (f) => f.properties.name,
    cityLabel = (c) => c.name, maxHeight = 720, insetNames = {}, showCityLabels = (c) => c.pop >= 250000,
  } = opts;
  el.innerHTML = '';
  el.classList.add('map', 'fr-map');

  // Fit to the features in focus (one region's departments), or to everything.
  const fitTo = focusIds ? { type: 'FeatureCollection', features: fcoll.features.filter((f) => focusIds.includes(f.id)) } : fcoll;
  const proj = d3.geoConicConformal().parallels([44, 49]).rotate([-3, 0]);
  const probe = d3.geoPath(proj.fitSize([1000, 1000], fitTo)).bounds(fitTo);
  const aspect = (probe[1][1] - probe[0][1]) / (probe[1][0] - probe[0][0]);
  const H = Math.round(Math.min(maxHeight, Math.max(360, W * aspect)));
  const pad = 18;
  proj.fitExtent([[pad, pad], [W - pad, H - pad]], fitTo);
  const path = d3.geoPath(proj);

  const svg = d3.select(el).append('svg').attr('viewBox', `0 0 ${W} ${H}`).attr('class', 'map-svg')
    .attr('role', 'group').attr('aria-label', ariaLabel);
  const layer = svg.append('g');

  // Inset frames for the overseas departments (only on the whole-country view).
  if (!focusIds && fcoll.insets?.length) {
    const frames = layer.append('g').attr('class', 'fr-insets');
    for (const fr of fcoll.insets) {
      const [x0, y0, x1, y1] = fr.box;
      const a = proj([x0, y1]), b = proj([x1, y0]);
      frames.append('rect').attr('x', a[0]).attr('y', a[1]).attr('width', b[0] - a[0]).attr('height', b[1] - a[1]).attr('rx', 8);
      if (insetNames[fr.code]) frames.append('text').attr('x', a[0] + 6).attr('y', b[1] - 6).text(insetNames[fr.code]);
    }
  }

  const shown = focusIds ? fcoll.features.filter((f) => focusIds.includes(f.id)) : fcoll.features;
  const regions = layer.append('g').attr('class', 'regions');
  const hoverOutline = layer.append('path').attr('class', 'outline-hover');
  const selOutline = layer.append('path').attr('class', 'outline-selected');
  const labels = layer.append('g').attr('class', 'map-labels');
  const dots = layer.append('g').attr('class', 'fr-cities');

  const tip = document.createElement('div');
  tip.className = 'map-tip';
  tip.hidden = true;
  el.appendChild(tip);
  const showTip = (content, px, py) => {
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
  const centerTip = (x, y) => {
    const r = el.getBoundingClientRect();
    return [(x / W) * r.width, (y / H) * r.height];
  };

  regions.selectAll('path').data(shown, (f) => f.id).join('path')
    .attr('class', 'region')
    .attr('d', path)
    .attr('fill', (f) => fillFor(f))
    .attr('tabindex', 0)
    .attr('role', 'button')
    .attr('aria-label', (f) => regionLabel(f))
    .attr('aria-pressed', (f) => String(f.id === selectedId))
    .on('pointerenter pointermove', (ev, f) => {
      hoverOutline.attr('d', path(f)).style('opacity', 1);
      const [px, py] = d3.pointer(ev, el);
      showTip(tooltipFor?.(f), px, py);
    })
    .on('pointerleave', () => { hoverOutline.style('opacity', 0); tip.hidden = true; })
    .on('focus', (ev, f) => {
      hoverOutline.attr('d', path(f)).style('opacity', 1);
      showTip(tooltipFor?.(f), ...centerTip(...path.centroid(f)));
    })
    .on('blur', () => { hoverOutline.style('opacity', 0); tip.hidden = true; })
    .on('click', (ev, f) => onSelect?.(f))
    .on('keydown', (ev, f) => { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); onSelect?.(f); } });

  if (labelFor) {
    labels.selectAll('text').data(shown.filter((f) => labelFor(f) && path.area(f) > 900)).join('text')
      .attr('transform', (f) => { const p = proj(f.properties.lp) || path.centroid(f); return `translate(${p[0]},${p[1]})`; })
      .attr('dy', '0.35em').attr('text-anchor', 'middle').text((f) => labelFor(f));
  }

  const sel = shown.find((f) => f.id === selectedId);
  if (sel) selOutline.attr('d', path(sel)).style('opacity', 1);

  // City markers: a dot for every city in view, a label for the largest.
  const inView = cities.filter((c) => { const p = proj(c.at); return p && p[0] > 0 && p[0] < W && p[1] > 0 && p[1] < H; });
  const g = dots.selectAll('g').data(inView, (c) => c.code).join('g')
    .attr('class', 'fr-city')
    .attr('transform', (c) => { const p = proj(c.at); return `translate(${p[0]},${p[1]})`; })
    .attr('tabindex', 0).attr('role', 'link').attr('aria-label', (c) => cityLabel(c))
    .on('pointerenter pointermove', (ev, c) => { const [px, py] = d3.pointer(ev, el); showTip(opts.cityTip?.(c), px, py); })
    .on('pointerleave', () => { tip.hidden = true; })
    .on('focus', (ev, c) => { const p = proj(c.at); showTip(opts.cityTip?.(c), ...centerTip(p[0], p[1])); })
    .on('blur', () => { tip.hidden = true; })
    .on('click', (ev, c) => { ev.stopPropagation(); onCity?.(c); })
    .on('keydown', (ev, c) => { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); onCity?.(c); } });
  g.append('circle').attr('class', 'hit').attr('r', 11);
  g.append('circle').attr('class', 'dot').attr('r', (c) => (c.pop >= 500000 ? 5.5 : c.pop >= 150000 ? 4.5 : 3.5));
  g.filter((c) => showCityLabels(c)).append('text').attr('x', 8).attr('dy', '0.35em').text((c) => c.name);

  return {
    refill: () => regions.selectAll('path').attr('fill', (f) => fillFor(f)),
  };
}
