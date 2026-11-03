// "Les grands enjeux" (#/fr/enjeux): the official figures behind seven debates of the
// 2027 campaign (economy, inflation, immigration, crime, the wealth gap, education and
// salaries), France beside Germany, Belgium, Italy, Spain, the Netherlands, the United
// Kingdom and the United States, and where the declared candidates stand on the
// questionnaire's questions on each topic. data/fr/enjeux.json is rebuilt every day by
// scripts/fr/enjeux.py (Eurostat, the OECD, the World Bank, the BLS and the Interior
// Ministry's statistics service); INSEE's, the ONS's and PISA's published figures are
// typed in scripts/fr/enjeux_sources.py.
//
// France is drawn in ink (--text-1) and other countries in gray (--other): every hue on
// France pages stands for a party, so the country in focus takes none. The pair passes
// the palette validator's colorblind, normal-vision and contrast checks in both themes
// (ΔE 39 dark, 44 light); its lightness-band and chroma checks are for hued palettes.

import { html, esc, debounce } from '../../util.js';
import { icon } from '../../icons.js';
import { L, lang } from '../../i18n.js';
import { lineChart, cssVar } from '../../lib/charts.js';
import { loadEnjeux, loadPres, loadPositions, runningIds, fmtDay, fmtNum, fmtInt, fmtPctFr } from '../data.js';
import { FR_QUESTION_BY_ID, qText } from '../questions.js';

const TABS = [
  ['economie', 'Économie', 'Economy'],
  ['inflation', 'Inflation', 'Inflation'],
  ['immigration', 'Immigration', 'Immigration'],
  ['criminalite', 'Criminalité', 'Crime'],
  ['ecart', 'Écart de richesse', 'Wealth gap'],
  ['education', 'Éducation', 'Education'],
  ['salaires', 'Salaires en France', 'Salaries in France'],
];

// The questionnaire's questions shown under each topic (js/fr/questions.js).
const QUESTIONS = {
  economie: ['q022', 'q023', 'q024', 'q016', 'q020', 'q021', 'q035'],
  inflation: ['q017', 'q037', 'q018'],
  immigration: ['q040', 'q041', 'q042', 'q043', 'q044', 'q046', 'q048', 'q052'],
  criminalite: ['q117', 'q118', 'q119', 'q120', 'q121', 'q123', 'q125', 'q050'],
  ecart: ['q013', 'q014', 'q025', 'q018', 'q037'],
  education: ['q103', 'q107', 'q104', 'q109', 'q113', 'q115'],
  salaires: ['q017', 'q019', 'q020', 'q103', 'q018'],
};

const NAMES = {
  FR: ['France', 'France'], DE: ['Allemagne', 'Germany'], BE: ['Belgique', 'Belgium'], IT: ['Italie', 'Italy'],
  ES: ['Espagne', 'Spain'], NL: ['Pays-Bas', 'Netherlands'], UK: ['Royaume-Uni', 'United Kingdom'], US: ['États-Unis', 'United States'],
  EU: ['Union européenne', 'European Union'], OECD: ['Moyenne de l’OCDE', 'OECD average'],
  'BE-FL': ['Belgique (Flandre)', 'Belgium (Flanders)'], 'BE-FR': ['Belgique (Wallonie-Bruxelles)', 'Belgium (Wallonia-Brussels)'],
  ENG: ['Angleterre', 'England'],
};
const cname = (c) => (NAMES[c] ? L(...NAMES[c]) : c);
// Each country's color comes from its flag (--cty-* in styles.css); England and Belgium's
// communities take their country's. White, black and yellow get an outline where they
// would vanish on the page (--cty-*-edge).
const CTY = { FR: 'fr', EU: 'eu', DE: 'de', BE: 'be', 'BE-FL': 'be', 'BE-FR': 'be', IT: 'it', ES: 'es', NL: 'nl', UK: 'uk', ENG: 'uk', US: 'us' };
const EDGED = new Set(['eu', 'be', 'es']);
// A country's line: its color, and its outline when the theme needs one.
function ctyLine(c) {
  const k = CTY[c];
  if (!k) return { color: cssVar('--other') };
  const edge = EDGED.has(k) ? cssVar(`--cty-${k}-edge`) : '';
  return { color: cssVar(`--cty-${k}`), edge: edge && edge !== 'transparent' ? edge : undefined };
}
// The order of the "Compare France with" menus.
const ORDER = ['EU', 'DE', 'BE', 'IT', 'ES', 'NL', 'UK', 'US'];

// What the visitor picked in the page's menus and switches, kept while the site is
// open: a theme or language change redraws the page and shouldn't reset them.
const picks = {};
const pick = (key, options, fallback) => (options.includes(picks[key]) ? picks[key] : fallback);
// The address the jobs card was last scrolled to (#/fr/enjeux?t=salaires&metier=…), so
// a redraw doesn't scroll there again.
let scrolledTo = null;

// Formats ----------------------------------------------------------------------------

const LOC = () => (lang() === 'fr' ? 'fr-FR' : 'en-GB');
const pct = (v, d = 1) => fmtPctFr(v, d);
const sgn = (v, d = 1) => `${v > 0 ? '+' : v < 0 ? '−' : ''}${fmtNum(Math.abs(v), d)}`;
const sPct = (v, d = 1) => (lang() === 'fr' ? `${sgn(v, d)} %` : `${sgn(v, d)}%`);
const axisPct = (v) => fmtPctFr(v, Number.isInteger(v) ? 0 : 1);
const num1 = (v) => fmtNum(v, 1);
const money = (v, cur = 'EUR', d = 0) => new Intl.NumberFormat(LOC(), { style: 'currency', currency: cur, minimumFractionDigits: d, maximumFractionDigits: d }).format(v);
const change = (now, before) => (before ? (100 * (now - before)) / Math.abs(before) : null);

// Periods as the sources write them: "2026-09" (month), "2026-Q3" (quarter), "2026-S2"
// (half-year) or "2025" (year).
function periodDate(p) {
  const [y, r] = String(p).split('-');
  if (!r) return new Date(+y, 0, 1);
  if (r[0] === 'Q') return new Date(+y, (+r.slice(1) - 1) * 3, 1);
  if (r[0] === 'S') return new Date(+y, (+r.slice(1) - 1) * 6, 1);
  return new Date(+y, +r - 1, 1);
}
function fmtPeriod(p) {
  const [y, r] = String(p).split('-');
  if (!r) return y;
  if (r[0] === 'Q') return L(`T${+r.slice(1)} ${y}`, `Q${+r.slice(1)} ${y}`);
  if (r[0] === 'S') return L(`${+r.slice(1) === 1 ? '1er' : '2e'} semestre ${y}`, `H${+r.slice(1)} ${y}`);
  return periodDate(p).toLocaleDateString(LOC(), { month: 'long', year: 'numeric' });
}
const DATES = {
  M: {
    axis: (d) => (d.getMonth() ? d.toLocaleDateString(LOC(), { month: 'short', year: 'numeric' }) : String(d.getFullYear())),
    tip: (d) => d.toLocaleDateString(LOC(), { month: 'long', year: 'numeric' }),
  },
  Q: { axis: (d) => String(d.getFullYear()), tip: (d) => L(`T${d.getMonth() / 3 + 1} ${d.getFullYear()}`, `Q${d.getMonth() / 3 + 1} ${d.getFullYear()}`) },
  A: { axis: (d) => String(d.getFullYear()), tip: (d) => String(d.getFullYear()) },
};
const last = (s) => (s?.length ? s[s.length - 1] : null);
const total = (o) => Object.values(o || {}).reduce((a, b) => a + b, 0);
const points = (s, since) => (s || []).filter(([p, v]) => v != null && (!since || p >= since)).map(([p, v]) => ({ x: periodDate(p), y: v }));
// Eurostat flags provisional figures with "p".
const periodNote = (l) => fmtPeriod(l[0]) + (String(l[2] || '').includes('p') ? L(', provisoire', ', provisional') : '');

// Pieces ------------------------------------------------------------------------------

const tile = (label, value, sub) => html`<div class="stat"><div class="eyebrow">${label}</div><div class="value num">${value}</div>${sub ? html`<div class="sub">${sub}</div>` : ''}</div>`;
const tiles = (...ts) => html`<div class="enj-tiles">${ts.filter(Boolean)}</div>`;

// Horizontal bars from zero (diverging when a value is negative), each country in its
// flag's color and the OECD average hatched gray; every row prints its name and value,
// so color is never the only cue. A list of France's own figures (all rows in focus) is
// all navy.
function bars(rows, { label = '' } = {}) {
  if (!rows.length) return html`<p class="small muted" style="margin:0">${L('Pas de données.', 'No data.')}</p>`;
  const vals = rows.map((r) => r.value);
  const lo = Math.min(0, ...vals), hi = Math.max(0, ...vals), span = hi - lo || 1;
  const zero = (-lo / span) * 100;
  const solo = rows.every((r) => r.focus);
  return html`<div class="enj-bars${solo ? ' solo' : ''}" role="list" aria-label="${label}">${rows.map((r) => {
    const left = ((Math.min(0, r.value) - lo) / span) * 100;
    const width = Math.max((Math.abs(r.value) / span) * 100, 0.6);
    const k = r.ref ? null : CTY[r.key] || (r.focus ? 'fr' : null);
    const color = k ? `--bar:var(--cty-${k})${EDGED.has(k) ? `;--bar-edge:var(--cty-${k}-edge)` : ''}` : '';
    return html`<div class="enj-bar${r.focus ? ' is-focus' : ''}${r.ref ? ' is-ref' : ''}${r.value < 0 ? ' neg' : ''}" style="${color}" role="listitem" title="${L(`${r.label} : ${r.text}`, `${r.label}: ${r.text}`)}${r.sub ? ` (${r.sub})` : ''}">
      <span class="who">${r.label}</span>
      <span class="track">${lo < 0 ? html`<i class="zero" style="left:${zero.toFixed(2)}%"></i>` : ''}<i class="fill" style="left:${left.toFixed(2)}%;width:${width.toFixed(2)}%"></i></span>
      <span class="val">${r.text}</span>
      ${r.sub ? html`<span class="sub">${r.sub}</span>` : ''}
    </div>`;
  })}</div>`;
}

function latestRows(series, fmt, { order = 'desc' } = {}) {
  const rows = [];
  for (const [c, s] of Object.entries(series || {})) {
    const l = last(s);
    if (!l || l[1] == null || !NAMES[c]) continue;
    rows.push({ key: c, label: cname(c), value: l[1], text: fmt(l[1]), sub: periodNote(l), focus: c === 'FR', ref: c === 'OECD' });
  }
  return rows.sort((a, b) => (order === 'asc' ? a.value - b.value : b.value - a.value));
}

function tableView(title, rows, first = L('Pays', 'Country'), third = L('Période', 'Period')) {
  return html`<details class="enj-table"><summary class="small">${L('Voir en tableau', 'Show as a table')}</summary>
    <div class="table-wrap" style="margin-top:8px"><table class="data"><caption class="sr-only">${title}</caption>
      <thead><tr><th>${first}</th><th class="r">${L('Valeur', 'Value')}</th><th>${third}</th></tr></thead>
      <tbody>${rows.map((r) => html`<tr><td>${r.label}</td><td class="r">${r.text}</td><td>${r.sub || ''}</td></tr>`)}</tbody></table></div></details>`;
}

function sourcesLine(list) {
  const items = (list || []).filter(Boolean);
  if (!items.length) return '';
  return html`<p class="tiny faint" style="margin:0">${items.length > 1 ? L('Sources :', 'Sources:') : L('Source :', 'Source:')} ${items.map((s, i) => html`${i ? ' · ' : ''}<a href="${s.url}" target="_blank" rel="noopener noreferrer">${s.title || L(s.fr, s.en)}</a>${s.date ? `, ${fmtDay(s.date)}` : ''}${s.updated ? L(` (mise à jour du ${fmtDay(s.updated)})`, ` (updated ${fmtDay(s.updated)})`) : ''}`)}</p>`;
}

const notes = (items) => html`<section class="card enj-notes"><h3 style="margin:0 0 10px">${L('Comprendre ces chiffres', 'Reading these figures')}</h3><ul>${items.filter(Boolean).map((t) => html`<li>${t}</li>`)}</ul></section>`;

// One indicator across countries: France against the country picked in the menu over
// time (line), and every country's latest value (bars), with a table view.
function compareCard(m) {
  const opts = ORDER.filter((c) => m.series?.[c]?.length);
  const vs = pick(`vs:${m.id}`, opts, opts.includes(m.vs) ? m.vs : opts[0]);
  const rows = latestRows(m.series, m.fmt, { order: m.order });
  return html`<section class="card stack enj-card" id="enj-${m.id}">
    <div><h3 style="margin:0">${m.title}</h3>${m.lead ? html`<p class="small muted" style="margin:4px 0 0">${m.lead}</p>` : ''}</div>
    ${m.line === false || !m.series?.FR?.length ? '' : html`
      ${opts.length ? html`<label class="enj-vs small muted">${L('Comparer la France avec', 'Compare France with')}
        <select class="input enj-select" data-vs="${m.id}">${opts.map((c) => html`<option value="${c}" ${c === vs ? 'selected' : ''}>${cname(c)}</option>`)}</select></label>` : ''}
      <div class="enj-line" data-line="${m.id}"></div>`}
    <div><div class="eyebrow" style="margin-bottom:8px">${m.barsTitle || L('Dernière valeur connue', 'Latest value')}</div>${bars(rows, { label: m.title })}</div>
    ${m.missing ? html`<p class="tiny faint" style="margin:0">${m.missing}</p>` : ''}
    ${tableView(m.title, rows)}
    ${sourcesLine(m.sources)}
  </section>`;
}

function chartOpts(name, fmt, axis, freq, baseline) {
  const f = DATES[freq || 'A'];
  return { height: 240, yFormat: axis || fmt, tipFormat: fmt, baseline: baseline ?? null, label: name, xFormat: f.axis, tipDate: f.tip, emptyText: L('Pas de données.', 'No data.') };
}

function drawLines(root, m) {
  const host = root.querySelector(`[data-line="${m.id}"]`);
  if (!host) return;
  const sel = root.querySelector(`select[data-vs="${m.id}"]`);
  const draw = () => {
    const series = [{ name: cname('FR'), ...ctyLine('FR'), values: points(m.series.FR, m.since) }];
    if (sel?.value && m.series[sel.value]) series.push({ name: cname(sel.value), ...ctyLine(sel.value), values: points(m.series[sel.value], m.since) });
    lineChart(host, { series, ...chartOpts(m.title, m.fmt, m.axis, m.freq, m.baseline) });
  };
  sel?.addEventListener('change', () => { picks[`vs:${m.id}`] = sel.value; draw(); });
  draw();
}

// One French series in navy, with an optional reference line in gray.
function drawSingle(host, { name, values, fmt, axis, freq, baseline, ref }) {
  const series = [{ name, ...ctyLine('FR'), values }];
  if (ref) series.push({ name: ref.name, color: cssVar('--other'), values: ref.values });
  lineChart(host, { series, ...chartOpts(name, fmt, axis, freq, baseline) });
}

// Where the declared candidates stand on the topic's questions, each name linking to
// the candidate's page and its sources.
function candidatesBlock(qids, pres, positions) {
  const running = runningIds(pres);
  const cands = (pres?.candidates || []).filter((c) => running.has(c.id))
    .sort((a, b) => (a.short || a.name).localeCompare(b.short || b.name, 'fr'));
  if (!cands.length || !qids?.length) return '';
  const link = (c) => html`<a class="chip enj-cand" href="#/fr/candidat/${c.id}">${c.short || c.name}</a>`;
  const items = qids.map((id) => FR_QUESTION_BY_ID[id]).filter(Boolean).map((q) => {
    const g = { pos: [], zero: [], neg: [] };
    for (const c of cands) {
      const p = positions?.candidates?.[c.id]?.[q.id];
      if (p?.stance == null) continue;
      g[p.stance > 0 ? 'pos' : p.stance < 0 ? 'neg' : 'zero'].push(c);
    }
    const unknown = cands.length - g.pos.length - g.zero.length - g.neg.length;
    const labels = q.kind === 'agree'
      ? [L('D’accord', 'Agree'), L('Neutres', 'Neutral'), L('Pas d’accord', 'Disagree')]
      : [L('Favorables', 'In favor'), L('Neutres', 'Neutral'), L('Défavorables', 'Against')];
    const group = (list, label) => (list.length ? html`<div class="enj-stance"><span class="small muted">${label} (${list.length})</span><div class="row" style="gap:6px">${list.map(link)}</div></div>` : '');
    return html`<div class="enj-q">
      <div class="q">${q.n}. ${qText(q)}</div>
      ${group(g.pos, labels[0])}${group(g.zero, labels[1])}${group(g.neg, labels[2])}
      <div class="tiny faint">${unknown === cands.length
        ? L('Aucun candidat déclaré n’a encore de position sourcée sur cette question.', 'No declared candidate has a sourced position on this question yet.')
        : L(`Sans position connue : ${unknown} candidat${unknown > 1 ? 's' : ''}.`, `No known position: ${unknown} candidate${unknown === 1 ? '' : 's'}.`)}</div>
    </div>`;
  });
  return html`<section class="card stack">
    <div><h2 style="margin:0">${L('Ce qu’en disent les candidats', 'What the candidates say')}</h2>
      <p class="small muted" style="margin:4px 0 0">${L(
        `Positions des ${cands.length} candidats déclarés sur les questions du questionnaire liées à ce thème, tirées de leurs programmes et déclarations ; la source de chacune est sur la page du candidat. Une position absente n’est jamais devinée.`,
        `Where the ${cands.length} declared candidates stand on the questionnaire’s questions on this topic, from their programs and statements; each one’s source is on the candidate’s page. A missing position is never guessed.`,
      )}</p></div>
    ${items}
    <div class="row"><a class="btn btn-sm" href="#/fr/elections/comparer">${icon.user()} ${L('Comparer avec mes opinions', 'Compare with my views')}</a></div>
  </section>`;
}

// Économie ----------------------------------------------------------------------------

function economie(d) {
  const b = d.blocks;
  const unemp = { ...b.unemp?.series, ...b.unemp_ukus?.series };
  const gq = last(b.gdp_q?.series?.FR), u = last(unemp.FR), dq = last(b.debt?.quarterly?.FR), bal = last(b.debt?.balance?.FR);
  const euOnly = L('Eurostat ne couvre que l’Union européenne : le Royaume-Uni et les États-Unis n’y figurent pas.', 'Eurostat covers the European Union only: the United Kingdom and the United States aren’t included.');
  const cards = [
    {
      id: 'chomage', title: L('Taux de chômage', 'Unemployment rate'),
      lead: L('Part des actifs sans emploi qui en cherchent un, chaque mois, corrigée des variations saisonnières.', 'Share of the labour force out of work and looking for a job, each month, seasonally adjusted.'),
      series: unemp, freq: 'M', since: '2015-01', vs: 'EU', fmt: pct, axis: axisPct, sources: [b.unemp?.source, b.unemp_ukus?.source],
    },
    {
      id: 'croissance', title: L('Croissance du PIB, par année', 'GDP growth, by year'),
      lead: L('Variation du produit intérieur brut en volume, c’est-à-dire hors inflation, d’une année sur l’autre.', 'Change in gross domestic product in real terms, that is after inflation, from one year to the next.'),
      series: b.gdp_a?.series, freq: 'A', since: '2014', vs: 'EU', fmt: sPct, axis: axisPct, baseline: 0, sources: [b.gdp_a?.source],
    },
    {
      id: 'dette', title: L('Dette publique', 'Government debt'),
      lead: L('Dette de l’ensemble des administrations publiques (État, collectivités locales, sécurité sociale), en % du PIB, au sens du traité de Maastricht.', 'Debt of general government (central and local government and social security), as a % of GDP, as defined by the Maastricht Treaty.'),
      series: b.debt?.debt, freq: 'A', since: '2007', vs: 'EU', fmt: pct, axis: axisPct, missing: euOnly, sources: [b.debt?.source_annual],
    },
    {
      id: 'solde', title: L('Solde public', 'Government balance'),
      lead: L('Recettes moins dépenses publiques de l’année, en % du PIB : un chiffre négatif est un déficit.', 'Government revenue minus spending over the year, as a % of GDP: a negative figure is a deficit.'),
      series: b.debt?.balance, freq: 'A', since: '2007', vs: 'EU', fmt: sPct, axis: axisPct, baseline: 0, missing: euOnly, sources: [b.debt?.source_annual],
    },
  ];
  return {
    intro: L('Croissance, chômage et finances publiques : où en est la France par rapport à ses voisins.', 'Growth, unemployment and public finances: where France stands next to its neighbours.'),
    blocks: ['unemp', 'unemp_ukus', 'gdp_q', 'gdp_a', 'debt'],
    cards,
    body: html`${tiles(
      gq && tile(L('Croissance du PIB', 'GDP growth'), sPct(gq[1]), L(`au ${fmtPeriod(gq[0])}, sur un trimestre`, `in ${fmtPeriod(gq[0])}, on the previous quarter`)),
      u && tile(L('Chômage', 'Unemployment'), pct(u[1]), L(`des actifs, ${fmtPeriod(u[0])}`, `of the labour force, ${fmtPeriod(u[0])}`)),
      dq && tile(L('Dette publique', 'Government debt'), pct(dq[1]), L(`du PIB, fin du ${fmtPeriod(dq[0])}`, `of GDP, end of ${fmtPeriod(dq[0])}`)),
      bal && tile(bal[1] < 0 ? L('Déficit public', 'Government deficit') : L('Excédent public', 'Government surplus'), pct(Math.abs(bal[1])), L(`du PIB en ${bal[0]}`, `of GDP in ${bal[0]}`)),
    )}
    ${cards.map((m) => compareCard(m))}
    ${notes([
      L('Chômage au sens du Bureau international du travail (BIT) : être sans emploi, disponible et en chercher un activement. Pour la France, les chiffres mensuels d’Eurostat sont établis à partir de l’enquête Emploi trimestrielle de l’Insee, qui reste la référence nationale. Le nombre d’inscrits à France Travail est une autre mesure, plus large.',
        'Unemployment as defined by the International Labour Organization (ILO): being without a job, available and actively looking for one. For France, Eurostat’s monthly figures are derived from INSEE’s quarterly Labour Force Survey, which remains the national reference. The number of people registered with France Travail, the public employment service, is a different and broader measure.'),
      L('Le PIB mesure la valeur de tout ce qui est produit dans le pays en un an. Les derniers chiffres sont provisoires et révisés pendant plusieurs années.', 'GDP measures the value of everything produced in the country in a year. The latest figures are provisional and revised for several years.'),
      L('Le traité de Maastricht fixe des valeurs de référence : 60 % du PIB pour la dette publique et 3 % pour le déficit.', 'The Maastricht Treaty sets reference values of 60% of GDP for government debt and 3% for the deficit.'),
    ])}`,
  };
}

// Inflation ---------------------------------------------------------------------------

const HICP_PARTS = [
  ['CP01', 'Alimentation et boissons non alcoolisées', 'Food and non-alcoholic drinks'],
  ['NRG', 'Énergie', 'Energy'],
  ['SERV', 'Services', 'Services'],
  ['IGD_NNRG', 'Produits manufacturés', 'Manufactured goods'],
  ['TOT_X_NRG_FOOD', 'Tout sauf énergie, alimentation, alcool et tabac', 'All but energy, food, alcohol and tobacco'],
];

function inflation(d) {
  const b = d.blocks;
  const prices = { ...b.hicp?.series, ...b.cpi_ukus?.series };
  const parts = b.hicp?.parts || {};
  const fr = last(prices.FR), eu = last(prices.EU), food = last(parts.CP01), energy = last(parts.NRG);
  const cards = [{
    id: 'inflation', title: L('Inflation sur un an', 'Inflation over twelve months'),
    lead: L('Hausse des prix à la consommation par rapport au même mois de l’année précédente.', 'Rise in consumer prices compared with the same month a year earlier.'),
    series: prices, freq: 'M', since: '2018-01', vs: 'EU', fmt: sPct, axis: axisPct, baseline: 0, sources: [b.hicp?.source, b.cpi_ukus?.source],
  }];
  const kinds = HICP_PARTS.filter(([k]) => parts[k]?.length);
  const partRows = kinds.map(([k, f, e]) => {
    const l = last(parts[k]);
    return { key: k, label: L(f, e), value: l[1], text: sPct(l[1]), sub: fmtPeriod(l[0]), focus: true };
  }).sort((a, z) => z.value - a.value);
  const title = L('Inflation par poste de dépenses', 'Inflation by type of spending');
  const poste = pick('poste', kinds.map(([k]) => k), kinds[0]?.[0]);
  return {
    intro: L('La hausse des prix en France et chez ses voisins, et ce qui la tire.', 'Rising prices in France and next door, and what drives them.'),
    blocks: ['hicp', 'cpi_ukus'],
    cards,
    body: html`${tiles(
      fr && tile(L('Inflation en France', 'Inflation in France'), sPct(fr[1]), L(`sur un an, ${fmtPeriod(fr[0])}`, `over a year, ${fmtPeriod(fr[0])}`)),
      eu && tile(L('Union européenne', 'European Union'), sPct(eu[1]), fmtPeriod(eu[0])),
      energy && tile(L('Énergie, en France', 'Energy, in France'), sPct(energy[1]), fmtPeriod(energy[0])),
      food && tile(L('Alimentation, en France', 'Food, in France'), sPct(food[1]), fmtPeriod(food[0])),
    )}
    ${cards.map((m) => compareCard(m))}
    <section class="card stack enj-card">
      <div><h3 style="margin:0">${L('En France, poste par poste', 'In France, by type of spending')}</h3>
        <p class="small muted" style="margin:4px 0 0">${L('Inflation sur un an de chaque grand poste de dépenses, comparée à l’ensemble des prix.', 'Inflation over a year for each main type of spending, compared with all prices.')}</p></div>
      <label class="enj-vs small muted">${L('Poste', 'Type')} <select class="input enj-select" data-pick="poste">${kinds.map(([k, f, e]) => html`<option value="${k}" ${k === poste ? 'selected' : ''}>${L(f, e)}</option>`)}</select></label>
      <div class="enj-line" data-chart="poste"></div>
      <div><div class="eyebrow" style="margin-bottom:8px">${L('Dernier mois connu', 'Latest month')}</div>${bars(partRows, { label: title })}</div>
      ${tableView(title, partRows, L('Poste', 'Type'))}
      ${sourcesLine([b.hicp?.source])}
    </section>
    ${notes([
      L('L’inflation mesure la hausse des prix sur douze mois. Pour l’Union européenne, c’est l’indice des prix à la consommation harmonisé (IPCH), calculé de la même façon dans tous les pays membres. L’Insee publie aussi l’indice des prix à la consommation (IPC), la référence nationale : les deux sont proches sans être identiques.',
        'Inflation measures the rise in prices over twelve months. For the European Union it is the harmonised index of consumer prices (HICP), computed the same way in every member country. INSEE also publishes the consumer price index (CPI), the national reference: the two are close but not identical.'),
      L('Royaume-Uni et États-Unis : leurs indices nationaux, d’après l’OCDE. Le CPI britannique suit la méthode de l’IPCH ; celui des États-Unis compte aussi le logement des propriétaires, que l’IPCH laisse de côté.',
        'United Kingdom and United States: their national indices, from the OECD. The British CPI follows the HICP method; the American one also counts owner-occupied housing, which the HICP leaves out.'),
      L('Une inflation de 3 % ne veut pas dire que chaque prix monte de 3 % : c’est une moyenne sur un panier de dépenses, et chaque ménage a le sien.', 'Inflation of 3% doesn’t mean every price rises by 3%: it is an average over a basket of spending, and each household has its own.'),
    ])}`,
    mount(root) {
      const sel = root.querySelector('[data-pick="poste"]'), host = root.querySelector('[data-chart="poste"]');
      if (!sel || !host) return;
      const draw = () => {
        const [k, f, e] = HICP_PARTS.find((p) => p[0] === sel.value);
        drawSingle(host, { name: L(f, e), values: points(parts[k], '2018-01'), fmt: sPct, axis: axisPct, freq: 'M', baseline: 0, ref: { name: L('Ensemble des prix', 'All prices'), values: points(prices.FR, '2018-01') } });
      };
      sel.addEventListener('change', () => { picks.poste = sel.value; draw(); });
      draw();
    },
  };
}

// Immigration -------------------------------------------------------------------------

const MIG_TYPES = [
  ['FA', 'Famille', 'Family'],
  ['AC', 'Famille accompagnant un travailleur', 'Family accompanying a worker'],
  ['WO', 'Travail', 'Work'],
  ['HU', 'Raisons humanitaires (dont réfugiés)', 'Humanitarian (including refugees)'],
  ['FR', 'Libre circulation (citoyens européens)', 'Free movement (EU citizens)'],
  ['OT', 'Autres', 'Other'],
];
const PERMITS = [
  ['TOTAL', 'Tous motifs', 'All reasons'],
  ['FAM', 'Famille', 'Family'],
  ['EDUC', 'Études', 'Education'],
  ['EMP', 'Travail', 'Work'],
  ['OTH', 'Autres motifs (dont protection internationale)', 'Other reasons (including international protection)'],
];

// Counts per year -> per 1,000 inhabitants, with the World Bank's population that year.
function perThousand(counts, pop) {
  const out = {};
  for (const [c, s] of Object.entries(counts || {})) {
    const ps = pop?.[c];
    if (!ps?.length) continue;
    out[c] = s.map(([y, n]) => [y, Math.round((10000 * n) / (ps.find(([py]) => py === y) || last(ps))[1]) / 10]);
  }
  return out;
}

function immigration(d) {
  const b = d.blocks, pop = b.population?.series;
  const perm = b.migration?.permanent || {};
  const permCounts = Object.fromEntries(Object.entries(perm).map(([c, ys]) => [c, Object.keys(ys).sort().map((y) => [y, total(ys[y])])]));
  const permRate = perThousand(permCounts, pop);
  const asylumRate = perThousand(b.migration?.asylum, pop);
  const share = last(b.migrant_share?.series?.FR);
  const pc = last(permCounts.FR), pr = last(permRate.FR), asy = last(b.migration?.asylum?.FR);
  const permits = b.permits_fr?.series || {}, pt = last(permits.TOTAL);
  const frCats = (pc && perm.FR?.[pc[0]]) || {};
  const catRows = MIG_TYPES.filter(([k]) => frCats[k]).map(([k, f, e]) => ({ key: k, label: L(f, e), value: frCats[k], text: fmtInt(frCats[k]), sub: pct((100 * frCats[k]) / total(frCats), 0), focus: true }))
    .sort((a, z) => z.value - a.value);
  const kinds = PERMITS.filter(([k]) => permits[k]?.length);
  const permitRows = kinds.filter(([k]) => k !== 'TOTAL').map(([k, f, e]) => {
    const l = permits[k].find(([y]) => y === pt?.[0]) || last(permits[k]);
    return { key: k, label: L(f, e), value: l[1], text: fmtInt(l[1]), sub: pt ? pct((100 * l[1]) / pt[1], 0) : '', focus: true };
  }).sort((a, z) => z.value - a.value);
  const cards = [
    {
      id: 'nes-etranger', title: L('Personnes nées à l’étranger', 'People born abroad'),
      lead: L('Part de la population née dans un autre pays, quelle que soit sa nationalité (estimations de l’ONU).', 'Share of the population born in another country, whatever their nationality (UN estimates).'),
      series: b.migrant_share?.series, line: false, fmt: pct, sources: [b.migrant_share?.source],
    },
    {
      id: 'permanents', title: L('Entrées de migrants à titre permanent, pour 1 000 habitants', 'Permanent-type migrant inflows per 1,000 people'),
      lead: L('Personnes autorisées à s’installer durablement dans l’année, tous motifs confondus, rapportées à la population.', 'People allowed to settle for the long term during the year, for any reason, relative to the population.'),
      series: permRate, freq: 'A', since: '2015', vs: 'DE', fmt: num1, axis: num1, sources: [b.migration?.source, b.population?.source],
    },
    {
      id: 'asile', title: L('Demandes d’asile, pour 1 000 habitants', 'Asylum applications per 1,000 people'),
      lead: L('Personnes ayant demandé l’asile dans l’année, rapportées à la population.', 'People who applied for asylum during the year, relative to the population.'),
      series: asylumRate, freq: 'A', since: '2015', vs: 'DE', fmt: num1, axis: num1, sources: [b.migration?.source_asylum, b.population?.source],
    },
  ];
  const catTitle = L(`En France, par motif d’entrée${pc ? ` (${pc[0]})` : ''}`, `In France, by reason for entry${pc ? ` (${pc[0]})` : ''}`);
  const permitTitle = L('Premiers titres de séjour délivrés en France', 'First residence permits issued in France');
  const titre = pick('titres', kinds.map(([k]) => k), 'TOTAL');
  return {
    intro: L('Combien de personnes s’installent en France, pour quels motifs, et comment la France se compare.', 'How many people settle in France, why, and how France compares.'),
    blocks: ['population', 'migrant_share', 'migration', 'permits_fr'],
    cards,
    body: html`${tiles(
      share && tile(L('Nés à l’étranger', 'Born abroad'), pct(share[1]), L(`de la population en ${share[0]} (ONU)`, `of the population in ${share[0]} (UN)`)),
      pc && tile(L('Entrées à titre permanent', 'Permanent-type inflows'), fmtInt(pc[1]), L(`en ${pc[0]}, soit ${num1(pr[1])} pour 1 000 habitants (OCDE)`, `in ${pc[0]}, or ${num1(pr[1])} per 1,000 people (OECD)`)),
      asy && tile(L('Demandes d’asile', 'Asylum applications'), fmtInt(asy[1]), L(`en ${asy[0]} (OCDE)`, `in ${asy[0]} (OECD)`)),
      pt && tile(L('Premiers titres de séjour', 'First residence permits'), fmtInt(pt[1]), L(`délivrés en ${pt[0]} (Eurostat)`, `issued in ${pt[0]} (Eurostat)`)),
    )}
    ${compareCard(cards[0])}
    ${compareCard(cards[1])}
    <section class="card stack enj-card">
      <div><h3 style="margin:0">${catTitle}</h3>
        <p class="small muted" style="margin:4px 0 0">${L('Entrées à titre permanent selon la raison du titre de séjour, et leur part du total.', 'Permanent-type inflows by the reason for the residence permit, and their share of the total.')}</p></div>
      ${bars(catRows, { label: catTitle })}
      ${tableView(catTitle, catRows, L('Motif', 'Reason'), L('Part du total', 'Share of total'))}
      ${sourcesLine([b.migration?.source])}
    </section>
    ${compareCard(cards[2])}
    <section class="card stack enj-card">
      <div><h3 style="margin:0">${permitTitle}</h3>
        <p class="small muted" style="margin:4px 0 0">${L('Titres délivrés pour la première fois dans l’année, étudiants compris, selon le motif.', 'Permits issued for the first time during the year, students included, by reason.')}</p></div>
      <label class="enj-vs small muted">${L('Motif', 'Reason')} <select class="input enj-select" data-pick="titres">${kinds.map(([k, f, e]) => html`<option value="${k}" ${k === titre ? 'selected' : ''}>${L(f, e)}</option>`)}</select></label>
      <div class="enj-line" data-chart="titres"></div>
      <div><div class="eyebrow" style="margin-bottom:8px">${pt ? pt[0] : ''}</div>${bars(permitRows, { label: permitTitle })}</div>
      ${tableView(permitTitle, permitRows, L('Motif', 'Reason'), L('Part du total', 'Share of total'))}
      ${sourcesLine([b.permits_fr?.source])}
    </section>
    ${notes([
      L('Immigré ou étranger : un immigré est né étranger à l’étranger, et peut être devenu français ; un étranger n’a pas la nationalité française, même s’il est né en France. L’ONU compte toutes les personnes nées à l’étranger, y compris les Français nés hors de France : son chiffre est plus élevé que le nombre d’immigrés publié par l’Insee.',
        'Immigrant or foreigner: in French statistics, an immigrant was born a foreigner abroad and may have become French; a foreigner doesn’t hold French nationality, even if born in France. The UN counts everyone born abroad, including French citizens born outside France, so its figure is higher than the number of immigrants INSEE publishes.'),
      L('Entrées à titre permanent (OCDE) : personnes autorisées à s’installer durablement, y compris les citoyens européens qui viennent librement ; les étudiants et les travailleurs temporaires n’y figurent pas. L’OCDE harmonise ces chiffres pour qu’ils se comparent d’un pays à l’autre.',
        'Permanent-type inflows (OECD): people allowed to settle for the long term, including EU citizens moving freely; students and temporary workers are not included. The OECD standardises these figures so they compare across countries.'),
      L('Toutes les demandes d’asile ne mènent pas à une protection. Les chiffres de l’OCDE et d’Eurostat ne comptent pas exactement de la même façon que ceux du ministère de l’Intérieur.', 'Not every asylum application leads to protection. The OECD’s and Eurostat’s figures don’t count exactly as the Interior Ministry’s do.'),
    ])}`,
    mount(root) {
      const sel = root.querySelector('[data-pick="titres"]'), host = root.querySelector('[data-chart="titres"]');
      if (!sel || !host) return;
      const draw = () => {
        const [k, f, e] = PERMITS.find((p) => p[0] === sel.value);
        drawSingle(host, { name: L(f, e), values: points(permits[k]), fmt: fmtInt, axis: fmtInt, freq: 'A' });
      };
      sel.addEventListener('change', () => { picks.titres = sel.value; draw(); });
      draw();
    },
  };
}

// Criminalité -------------------------------------------------------------------------

const CRIMES = [
  ['Homicides', 'Homicides'],
  ["Tentatives d'homicide", 'Attempted homicides'],
  ['Violences physiques hors cadre familial', 'Physical violence outside the family'],
  ['Violences physiques intrafamiliales', 'Physical violence within the family'],
  ['Violences sexuelles', 'Sexual violence'],
  ['Vols avec armes', 'Armed robbery'],
  ['Vols violents sans arme', 'Violent theft without a weapon'],
  ['Vols sans violence contre des personnes', 'Theft from people without violence'],
  ['Cambriolages de logement', 'Home burglary'],
  ['Vols de véhicule', 'Vehicle theft'],
  ['Vols dans les véhicules', 'Theft from vehicles'],
  ["Vols d'accessoires sur véhicules", 'Theft of vehicle parts'],
  ['Destructions et dégradations volontaires', 'Criminal damage'],
  ['Escroqueries et fraudes aux moyens de paiement', 'Fraud, including payment fraud'],
  ['Trafic de stupéfiants', 'Drug trafficking'],
  ['Usage de stupéfiants', 'Drug use'],
  ['Usage de stupéfiants (AFD)', 'Drug use: on-the-spot fines'],
  ['Usage de stupéfiants (hors AFD)', 'Drug use: other proceedings'],
];
const UNITS = {
  Victime: ['victimes', 'victims'], 'Victime entendue': ['victimes entendues', 'victims heard'], Infraction: ['infractions', 'offences'],
  Véhicule: ['véhicules', 'vehicles'], 'Mis en cause': ['personnes mises en cause', 'suspects'],
};

function crimeRows(inds) {
  return CRIMES.filter(([k]) => inds[k]?.series?.length).map(([k, en]) => {
    const ind = inds[k], s = ind.series, l = last(s), prev = s[s.length - 2];
    const first = s.find((r) => r[1] > 0);
    // Rare offences per 100,000 people, burglaries per 1,000 homes, the rest per 1,000 people.
    const scale = ind.per !== 'homes' && Math.max(...s.map((r) => r[2])) < 0.5 ? 100 : 1;
    const per = ind.per === 'homes' ? L('pour 1 000 logements', 'per 1,000 homes')
      : scale === 100 ? L('pour 100 000 habitants', 'per 100,000 people') : L('pour 1 000 habitants', 'per 1,000 people');
    return {
      key: k, label: L(k.replace(/'/g, '’'), en), unit: L(...(UNITS[ind.unit] || [ind.unit, ind.unit])), per, scale,
      year: l[0], n: l[1], rate: l[2] * scale, series: s,
      since: first && first[0] !== l[0] ? { year: first[0], pct: change(l[2], first[2]) } : null,
      yoy: prev && prev[1] ? change(l[1], prev[1]) : null,
    };
  });
}

function criminalite(d) {
  const b = d.blocks, inds = b.crime_fr?.indicators || {};
  const rows = crimeRows(inds);
  const byKey = Object.fromEntries(rows.map((r) => [r.key, r]));
  const crimeTile = (k, label) => {
    const r = byKey[k];
    if (!r) return '';
    const unitWord = r.key.startsWith('Cambriolages') ? L('par logement', 'per home') : L('par habitant', 'per person');
    return tile(label, fmtInt(r.n), L(`${r.unit} en ${r.year}${r.since ? ` · ${sPct(r.since.pct, 0)} ${unitWord} depuis ${r.since.year}` : ''}`,
      `${r.unit} in ${r.year}${r.since ? ` · ${sPct(r.since.pct, 0)} ${unitWord} since ${r.since.year}` : ''}`));
  };
  const afd = byKey['Usage de stupéfiants (AFD)'];
  const cards = [{
    id: 'homicides', title: L('Homicides volontaires pour 100 000 habitants', 'Intentional homicides per 100,000 people'),
    lead: L('L’infraction la plus comparable d’un pays à l’autre, d’après l’Office des Nations unies contre la drogue et le crime (ONUDC).', 'The offence that compares best across countries, from the United Nations Office on Drugs and Crime (UNODC).'),
    series: b.homicide?.series, freq: 'A', since: '2012', vs: 'DE', fmt: num1, axis: num1, sources: [b.homicide?.source],
  }];
  const title = L('Faits enregistrés en France, par type', 'Offences recorded in France, by type');
  const cur = pick('crime', rows.map((r) => r.key), 'Violences physiques hors cadre familial');
  return {
    intro: L('Les infractions enregistrées par la police et la gendarmerie depuis 2016, et les homicides comparés entre pays.', 'Offences recorded by the police and the gendarmerie since 2016, and homicide compared across countries.'),
    blocks: ['crime_fr', 'homicide'],
    cards,
    body: html`${tiles(
      crimeTile('Homicides', L('Homicides', 'Homicides')),
      crimeTile('Violences physiques hors cadre familial', L('Violences hors famille', 'Violence outside the family')),
      crimeTile('Violences sexuelles', L('Violences sexuelles', 'Sexual violence')),
      crimeTile('Cambriolages de logement', L('Cambriolages', 'Burglaries')),
    )}
    <section class="card stack enj-card">
      <div><h3 style="margin:0">${title}</h3>
        <p class="small muted" style="margin:4px 0 0">${L('Faits constatés par la police et la gendarmerie, rapportés à la population, en France entière (outre-mer compris).', 'Offences recorded by the police and the gendarmerie, relative to the population, for the whole of France (overseas included).')}</p></div>
      <label class="enj-vs small muted">${L('Infraction', 'Offence')} <select class="input enj-select" data-pick="crime">${rows.map((r) => html`<option value="${r.key}" ${r.key === cur ? 'selected' : ''}>${r.label}</option>`)}</select></label>
      <div class="enj-line" data-chart="crime"></div>
      <div class="table-wrap"><table class="data"><caption class="sr-only">${title}</caption>
        <thead><tr><th>${L('Infraction', 'Offence')}</th><th class="r">${L('Nombre', 'Number')}</th><th class="r">${L('Taux', 'Rate')}</th><th class="r">${L('Évolution du taux', 'Change in rate')}</th><th class="r">${L('Sur un an', 'Over a year')}</th></tr></thead>
        <tbody>${rows.map((r) => html`<tr>
          <td>${r.label}<div class="tiny faint">${r.unit}</div></td>
          <td class="r">${fmtInt(r.n)}<div class="tiny faint">${r.year}</div></td>
          <td class="r">${fmtNum(r.rate, r.scale === 100 ? 1 : 2)}<div class="tiny faint">${r.per}</div></td>
          <td class="r">${r.since ? html`${sPct(r.since.pct, 0)}<div class="tiny faint">${L(`depuis ${r.since.year}`, `since ${r.since.year}`)}</div>` : '—'}</td>
          <td class="r">${r.yoy != null ? sPct(r.yoy, 1) : '—'}</td></tr>`)}</tbody></table></div>
      ${sourcesLine([b.crime_fr?.source])}
    </section>
    ${cards.map((m) => compareCard(m))}
    ${notes([
      L('Ces chiffres comptent les faits enregistrés par la police et la gendarmerie, pas tous les faits commis : ils montent aussi quand les victimes portent plainte plus souvent ou quand les forces de l’ordre font plus de contrôles. L’enquête annuelle « Vécu et ressenti en matière de sécurité » du ministère de l’Intérieur mesure aussi les faits qui ne sont pas déclarés.',
        'These figures count offences recorded by the police and the gendarmerie, not every offence committed: they also rise when victims report more often or when the police carry out more checks. The Interior Ministry’s annual survey, “Vécu et ressenti en matière de sécurité”, also measures offences that go unreported.'),
      afd ? L(`Usage de stupéfiants : depuis septembre 2020, il peut être sanctionné par une amende forfaitaire délictuelle (AFD), ce qui a fait nettement augmenter les faits enregistrés (${fmtInt(afd.n)} amendes en ${afd.year}).`,
        `Drug use: since September 2020 it can be punished with an on-the-spot criminal fine (amende forfaitaire délictuelle, AFD), which sharply raised the number of offences recorded (${fmtInt(afd.n)} fines in ${afd.year}).`) : '',
      L('Taux : pour 1 000 habitants, pour 1 000 logements pour les cambriolages, et pour 100 000 habitants pour les faits les plus rares, avec la population que donne le SSMSI pour chaque année.', 'Rates: per 1,000 people, per 1,000 homes for burglaries and per 100,000 people for the rarest offences, using the population the SSMSI gives for each year.'),
      L('Comparaisons internationales : les homicides sont l’infraction la mieux comparable ; l’ONUDC ne les compte pas tout à fait comme le ministère de l’Intérieur, et les années disponibles diffèrent.', 'International comparisons: homicide compares best; UNODC doesn’t count it exactly as the Interior Ministry does, and the years available differ.'),
    ])}`,
    mount(root) {
      const sel = root.querySelector('[data-pick="crime"]'), host = root.querySelector('[data-chart="crime"]');
      if (!sel || !host) return;
      const draw = () => {
        const r = byKey[sel.value];
        const digits = r.scale === 100 ? 1 : 2;
        drawSingle(host, { name: `${r.label}, ${r.per}`, values: r.series.map(([y, , v]) => ({ x: periodDate(y), y: v * r.scale })), fmt: (v) => fmtNum(v, digits), axis: (v) => fmtNum(v, Number.isInteger(v) ? 0 : digits), freq: 'A' });
      };
      sel.addEventListener('change', () => { picks.crime = sel.value; draw(); });
      draw();
    },
  };
}

// Écart de richesse -------------------------------------------------------------------

function ecart(d) {
  const q = d.blocks.inequality || {};
  const g = last(q.gini?.FR), s = last(q.s80s20?.FR), p60 = last(q.poverty60?.FR), top = last(q.wealth?.SH_TOP10?.FR);
  const cards = [
    {
      id: 'gini', title: L('Inégalités de revenus : l’indice de Gini', 'Income inequality: the Gini index'),
      lead: L('De 0 (tout le monde a le même revenu) à 100 (une seule personne reçoit tout), sur le revenu disponible après impôts et prestations.', 'From 0 (everyone has the same income) to 100 (one person receives everything), on disposable income after taxes and benefits.'),
      series: q.gini, freq: 'A', since: '2010', vs: 'DE', fmt: num1, axis: num1, sources: [q.source],
    },
    {
      id: 'pauvrete', title: L('Taux de pauvreté', 'Poverty rate'),
      lead: L('Part des personnes vivant avec moins de 60 % du revenu médian de leur pays.', 'Share of people living on less than 60% of their country’s median income.'),
      series: q.poverty60, freq: 'A', since: '2010', vs: 'DE', fmt: pct, axis: axisPct, sources: [q.source],
    },
  ];
  const side = [
    {
      id: 's80s20', title: L('Les 20 % les plus aisés et les 20 % les plus modestes', 'The richest 20% and the poorest 20%'),
      lead: L('Combien de fois le revenu total des 20 % les plus aisés dépasse celui des 20 % les plus modestes (rapport S80/S20).', 'How many times the total income of the richest 20% exceeds that of the poorest 20% (the S80/S20 ratio).'),
      series: q.s80s20, line: false, fmt: num1, sources: [q.source],
    },
    {
      id: 'pauvrete50', title: L('Taux de pauvreté au seuil de 50 %', 'Poverty rate at the 50% line'),
      lead: L('Part des personnes vivant avec moins de la moitié du revenu médian, le seuil le plus utilisé par l’OCDE.', 'Share of people living on less than half the median income, the line the OECD uses most.'),
      series: q.poverty50, line: false, fmt: pct, sources: [q.source],
    },
  ];
  const wealth = [
    { id: 'top10', title: L('Part du patrimoine des 10 % les plus riches', 'Share of wealth held by the richest 10%'), series: q.wealth?.SH_TOP10, line: false, fmt: pct, sources: [q.source_wealth] },
    { id: 'top1', title: L('Part du patrimoine des 1 % les plus riches', 'Share of wealth held by the richest 1%'), series: q.wealth?.SH_TOP1, line: false, fmt: pct, sources: [q.source_wealth] },
    { id: 'bot40', title: L('Part du patrimoine des 40 % les moins riches', 'Share of wealth held by the poorest 40%'), series: q.wealth?.SH_BOT40, line: false, fmt: pct, sources: [q.source_wealth] },
  ];
  return {
    intro: L('Comment les revenus et le patrimoine se répartissent, en France et ailleurs.', 'How income and wealth are shared out, in France and elsewhere.'),
    blocks: ['inequality'],
    cards,
    body: html`${tiles(
      g && tile(L('Indice de Gini', 'Gini index'), num1(g[1]), L(`revenu disponible, ${g[0]}`, `disposable income, ${g[0]}`)),
      s && tile(L('Rapport S80/S20', 'S80/S20 ratio'), num1(s[1]), L(`fois le revenu des 20 % les plus modestes, pour les 20 % les plus aisés (${s[0]})`, `times the income of the poorest 20%, for the richest 20% (${s[0]})`)),
      p60 && tile(L('Taux de pauvreté', 'Poverty rate'), pct(p60[1]), L(`sous 60 % du revenu médian, ${p60[0]}`, `below 60% of median income, ${p60[0]}`)),
      top && tile(L('Patrimoine des 10 % les plus riches', 'Wealth of the richest 10%'), pct(top[1]), L(`du patrimoine des ménages, ${top[0]}`, `of household wealth, ${top[0]}`)),
    )}
    ${cards.map((m) => compareCard(m))}
    <div class="grid-2 enj-grid">${side.map((m) => compareCard(m))}</div>
    <h3 style="margin:0">${L('Le patrimoine', 'Wealth')}</h3>
    <div class="grid-3 enj-grid">${wealth.map((m) => compareCard(m))}</div>
    ${notes([
      L('Revenu disponible : revenus du travail et du patrimoine, plus les prestations sociales, moins les impôts directs et les cotisations. Pour tenir compte de la taille des ménages, l’OCDE divise le revenu de chaque ménage par la racine carrée du nombre de ses membres ; l’Insee utilise une autre échelle, d’où des chiffres un peu différents des siens.',
        'Disposable income: income from work and assets, plus social benefits, minus direct taxes and contributions. To allow for household size, the OECD divides each household’s income by the square root of its number of members; INSEE uses a different scale, so its figures differ somewhat.'),
      L('Seuils de pauvreté : 60 % du revenu médian dans l’Union européenne et à l’Insee, 50 % le plus souvent à l’OCDE. C’est une pauvreté relative, qui dépend du niveau de vie de chaque pays.', 'Poverty lines: 60% of median income in the European Union and at INSEE, 50% most often at the OECD. This is relative poverty, which depends on each country’s living standards.'),
      L('Patrimoine : ce que possèdent les ménages (logement, épargne, placements, entreprises) moins leurs dettes. Il est bien plus concentré que le revenu. Les enquêtes sur le patrimoine sont espacées de plusieurs années et n’ont pas lieu la même année partout : chaque barre indique la sienne. Une part négative veut dire que les dettes de ce groupe dépassent ce qu’il possède.',
        'Wealth: what households own (housing, savings, investments, businesses) minus their debts. It is far more concentrated than income. Wealth surveys are several years apart and don’t take place in the same year everywhere: each bar shows its own. A negative share means the group owes more than it owns.'),
    ])}`,
  };
}

// Éducation ---------------------------------------------------------------------------

function education(d) {
  const e = d.blocks.education || {}, pisa = d.hand?.pisa;
  const t = last(e.tertiary?.FR), el = last(e.early?.FR);
  const avg = pisa?.oecd_average?.science;
  const pisaRows = pisa ? Object.entries(pisa.science).map(([c, v]) => {
    const ch = pisa.change_2022?.[c];
    return {
      key: c, label: cname(c) + (pisa.caution.includes(c) ? ' *' : ''), value: v - avg, focus: c === 'FR',
      text: `${fmtInt(v)} points`,
      sub: [L(`écart à la moyenne de l’OCDE : ${sgn(v - avg, 0)}`, `gap from the OECD average: ${sgn(v - avg, 0)}`), ch ? L(`depuis 2022 : ${sgn(ch[0], 0)}`, `since 2022: ${sgn(ch[0], 0)}`) : ''].filter(Boolean).join(' · '),
    };
  }).sort((a, z) => z.value - a.value) : [];
  const cards = [
    {
      id: 'diplomes', title: L('Jeunes adultes diplômés du supérieur', 'Young adults with a tertiary degree'),
      lead: L('Part des 25-34 ans ayant un diplôme de l’enseignement supérieur (de bac+2 au doctorat).', 'Share of 25 to 34-year-olds with a tertiary degree (from two-year diplomas to doctorates).'),
      series: e.tertiary, freq: 'A', since: '2015', vs: 'DE', fmt: pct, axis: axisPct, sources: [e.source],
    },
    {
      id: 'sortants', title: L('Jeunes sortis tôt de l’école', 'Early school leavers'),
      lead: L('Part des 18-24 ans sans diplôme du second cycle du secondaire (CAP, BEP ou bac) qui ne suivent ni études ni formation.', 'Share of 18 to 24-year-olds without an upper-secondary qualification who are in neither education nor training.'),
      series: e.early, freq: 'A', since: '2010', vs: 'EU', fmt: pct, axis: axisPct, missing: L('Eurostat ne couvre que l’Union européenne.', 'Eurostat covers the European Union only.'), sources: [e.source_early],
    },
    {
      id: 'depense', title: L('Dépenses publiques d’éducation', 'Government spending on education'),
      lead: L('Dépenses de l’ensemble des administrations publiques pour l’éducation, de la maternelle à l’université, en % du PIB.', 'General government spending on education, from nursery school to university, as a % of GDP.'),
      series: e.spend, freq: 'A', since: '2010', vs: 'EU', fmt: pct, axis: axisPct, missing: L('Eurostat ne couvre que l’Union européenne.', 'Eurostat covers the European Union only.'), sources: [e.source_spend],
    },
  ];
  const pisaTitle = L('PISA 2025 : sciences', 'PISA 2025: science');
  const fr = pisa?.change_2022?.FR;
  return {
    intro: L('Le niveau des élèves, les diplômes et ce que dépense l’État.', 'Pupils’ results, degrees and what government spends.'),
    blocks: ['education'],
    cards,
    body: html`${tiles(
      pisa && tile(L('PISA 2025, sciences', 'PISA 2025, science'), fmtInt(pisa.science.FR), L(`points ; moyenne de l’OCDE : ${avg}`, `points; OECD average: ${avg}`)),
      fr && tile(L('PISA, mathématiques', 'PISA, mathematics'), sgn(fr[2], 0), L('points depuis 2022', 'points since 2022')),
      t && tile(L('Diplômés du supérieur', 'Tertiary graduates'), pct(t[1]), L(`des 25-34 ans, ${t[0]}`, `of 25 to 34-year-olds, ${t[0]}`)),
      el && tile(L('Sortis tôt de l’école', 'Early school leavers'), pct(el[1]), L(`des 18-24 ans, ${el[0]}`, `of 18 to 24-year-olds, ${el[0]}`)),
    )}
    ${pisa ? html`<section class="card stack enj-card">
      <div><h3 style="margin:0">${pisaTitle}</h3>
        <p class="small muted" style="margin:4px 0 0">${L(`Score moyen des élèves de 15 ans en sciences, matière principale de l’édition 2025. Les barres montrent l’écart à la moyenne des pays de l’OCDE (${avg} points).`, `Mean score of 15-year-old students in science, the main subject of the 2025 round. The bars show the gap from the OECD average (${avg} points).`)}</p></div>
      ${bars(pisaRows, { label: pisaTitle })}
      <details class="enj-table"><summary class="small">${L('Voir en tableau, avec l’évolution depuis 2022 dans les trois matières', 'Show as a table, with the change since 2022 in all three subjects')}</summary>
        <div class="table-wrap" style="margin-top:8px"><table class="data"><caption class="sr-only">${pisaTitle}</caption>
          <thead><tr><th>${L('Pays', 'Country')}</th><th class="r">${L('Sciences 2025', 'Science 2025')}</th><th class="r">${L('Sciences', 'Science')}</th><th class="r">${L('Compréhension de l’écrit', 'Reading')}</th><th class="r">${L('Mathématiques', 'Mathematics')}</th></tr></thead>
          <tbody>${Object.entries(pisa.science).sort((a, z) => z[1] - a[1]).map(([c, v]) => {
            const ch = pisa.change_2022[c] || [];
            return html`<tr><td>${cname(c)}${pisa.caution.includes(c) ? ' *' : ''}</td><td class="r">${v}</td>${ch.map((x) => html`<td class="r">${sgn(x, 0)}</td>`)}</tr>`;
          })}</tbody></table></div>
        <p class="tiny faint" style="margin:6px 0 0">${L('Évolution entre 2022 et 2025, en points.', 'Change between 2022 and 2025, in points.')}</p></details>
      <p class="tiny faint" style="margin:0">${L('* Pays-Bas et États-Unis : l’OCDE signale que leur échantillon ne respecte pas toutes ses normes ; leurs résultats sont à lire avec prudence.', '* Netherlands and United States: the OECD notes that their samples don’t meet all its standards; read their results with caution.')}</p>
      ${sourcesLine([pisa.source, { title: L('OCDE, PISA 2025, guide du lecteur', 'OECD, PISA 2025, Reader’s Guide'), url: pisa.notes_url }])}
    </section>` : ''}
    ${cards.map((m) => compareCard(m))}
    <div class="notice">${icon.info()}<div>${L('Le salaire médian dans l’enseignement, en France et chez nos voisins, est dans l’onglet', 'Median pay in education, in France and next door, is in the')} <a href="#/fr/enjeux?t=salaires&amp;metier=sector-P">${L('Salaires en France', 'Salaries in France')}</a>${L('.', ' tab.')}</div></div>
    ${notes([
      L('PISA : l’OCDE teste tous les trois ans des élèves de 15 ans en mathématiques, en compréhension de l’écrit et en sciences. Les scores sont des estimations : un écart de quelques points entre deux pays n’est souvent pas significatif.', 'PISA: every three years the OECD tests 15-year-old students in mathematics, reading and science. Scores are estimates: a gap of a few points between two countries is often not significant.'),
      L('Diplômes : la classification internationale (CITE) range au même niveau des diplômes comparables d’un pays à l’autre ; en France, le supérieur commence au BTS.', 'Degrees: the international classification (ISCED) puts comparable qualifications at the same level across countries; in France, tertiary education starts with two-year vocational diplomas (BTS).'),
    ])}`,
  };
}

// Salaires en France ------------------------------------------------------------------

const IDX = [['d1', '1er décile (D1)', '1st decile (D1)'], ['d9', '9e décile (D9)', '9th decile (D9)'], ['mean', 'Salaire moyen', 'Mean pay']];
const METRICS = [
  ['wage', 'Salaire médian à temps plein', 'Median full-time pay'],
  ['income', 'Niveau de vie médian', 'Median disposable income'],
  ['gdp', 'PIB par habitant', 'GDP per head'],
];
const METRIC_LEAD = {
  wage: () => L('Salaire annuel brut médian des salariés à temps plein en 2022 : enquête européenne sur la structure des salaires (entreprises de 10 salariés ou plus, hors administration publique) ; Royaume-Uni et États-Unis : salaire hebdomadaire médian multiplié par 52.',
    'Median gross annual pay of full-time employees in 2022: the EU Structure of Earnings Survey (firms with 10 or more employees, excluding public administration); United Kingdom and United States: median weekly pay times 52.'),
  income: () => L('Revenu disponible annuel médian par personne, après impôts et prestations, ajusté à la taille du ménage (OCDE).', 'Median annual disposable income per person, after taxes and benefits, adjusted for household size (OECD).'),
  gdp: () => L('Valeur de tout ce qui est produit dans le pays en un an, divisée par le nombre d’habitants (Banque mondiale).', 'Value of everything produced in the country in a year, divided by the number of inhabitants (World Bank).'),
};
const MODES = [['ppp', 'Aux prix français (PPA)', 'At French prices (PPP)'], ['xr', 'Au taux de change', 'At market exchange rates']];
const JOB_GROUPS = [
  [/^sector-/, 'Salaire horaire médian par secteur (pays de l’UE)', 'Median hourly pay by sector (EU countries)'],
  [/^minimum$/, 'Salaire minimum (montant annuel)', 'Minimum wage (yearly amount)'],
];
const JOB_SOURCES = {
  min_wage: (b) => b.min_wage?.source, earnings_eu_sectors: (b) => b.earnings_eu?.source_sectors,
};

const vsFrance = (v, fr) => (fr ? L(`${sPct(change(v, fr), 0)} par rapport à la France`, `${sPct(change(v, fr), 0)} vs France`) : '');

function intlRows(sal, metric, mode) {
  const src = sal?.[metric] || {};
  const fr = src.FR?.[mode];
  return Object.entries(src).filter(([c, v]) => NAMES[c] && v?.[mode] != null).map(([c, v]) => ({
    key: c, label: cname(c), value: v[mode], text: money(v[mode]), focus: c === 'FR',
    sub: [v.year, c !== 'FR' ? vsFrance(v[mode], fr) : ''].filter(Boolean).join(' · '),
    orig: metric === 'gdp' ? (mode === 'ppp' ? L(`${fmtInt(v.intl)} dollars internationaux`, `${fmtInt(v.intl)} international dollars`) : money(v.usd, 'USD')) : money(v.amount, v.cur),
  })).sort((a, z) => z.value - a.value);
}

// Hourly figures keep their cents and say "/h"; yearly ones are whole euros.
function jobRows(job, mode) {
  const fr = job?.values.FR?.[mode];
  const hourly = job?.per === 'hour';
  const amt = (v, cur) => (hourly ? `${money(v, cur, 2)}/h` : money(v, cur));
  return Object.entries(job?.values || {}).filter(([, v]) => v?.[mode] != null).map(([c, v]) => ({
    key: c, label: cname(c), value: v[mode], text: amt(v[mode]), focus: c === 'FR',
    sub: [v.year, c !== 'FR' ? vsFrance(v[mode], fr) : ''].filter(Boolean).join(' · '), orig: amt(v.amount, v.cur),
  })).sort((a, z) => z.value - a.value);
}

function moneyTable(title, rows) {
  return html`<details class="enj-table"><summary class="small">${L('Voir en tableau', 'Show as a table')}</summary>
    <div class="table-wrap" style="margin-top:8px"><table class="data"><caption class="sr-only">${title}</caption>
      <thead><tr><th>${L('Pays', 'Country')}</th><th class="r">${L('En euros', 'In euros')}</th><th class="r">${L('Montant d’origine', 'Original amount')}</th><th>${L('Année, écart avec la France', 'Year, gap with France')}</th></tr></thead>
      <tbody>${rows.map((r) => html`<tr><td>${r.label}</td><td class="r">${r.text}</td><td class="r">${r.orig}</td><td>${r.sub}</td></tr>`)}</tbody></table></div></details>`;
}

// The job's own note, plus a warning when France's latest year isn't every country's.
function jobNote(job) {
  if (!job) return '';
  const fr = job.values.FR?.year;
  const years = new Set(Object.values(job.values).map((v) => v.year));
  return L(job.noteFr, job.noteEn) + (fr && years.size > 1
    ? L(` Les années diffèrent selon les pays (France : ${fr}) : un écart avec la France compare alors deux années différentes.`, ` Years differ by country (France: ${fr}), so a gap with France then compares two different years.`)
    : '');
}
const metricTitle = (metric) => L(...METRICS.find((m) => m[0] === metric).slice(1));
const jobTitle = (job) => (!job ? '' : job.per === 'hour' ? L(`Salaire horaire médian : ${job.fr}`, `Median hourly pay: ${job.en}`) : L(job.fr, job.en));

// INSEE's 100-euro bands of monthly net pay in a light shade of France's navy, with the
// median (solid) and the mean (dashed) as ink lines named in the legend, which fits any
// width.
function drawHistogram(host, ins) {
  const bands = ins.distribution.filter(([lo, hi]) => lo != null && hi != null);
  if (!bands.length) return;
  const draw = () => {
    host.innerHTML = '';
    const legend = document.createElement('div');
    legend.className = 'chart-legend';
    legend.innerHTML = `<span><i class="key-line enj-key-solid"></i>${esc(`${L('Médiane', 'Median')} ${money(ins.median_net)}`)}</span><span><i class="key-line enj-key-dash"></i>${esc(`${L('Moyenne', 'Mean')} ${money(ins.mean_net)}`)}</span>`;
    host.appendChild(legend);
    const W = Math.max(300, host.clientWidth || 640), H = 240;
    const m = { top: 12, right: 14, bottom: 28, left: 48 };
    const x = d3.scaleLinear().domain([bands[0][0], bands[bands.length - 1][1]]).range([m.left, W - m.right]);
    const y = d3.scaleLinear().domain([0, d3.max(bands, (b) => b[2])]).nice(4).range([H - m.bottom, m.top]);
    const svg = d3.select(host).append('svg').attr('viewBox', `0 0 ${W} ${H}`).attr('width', '100%').attr('height', H).attr('class', 'chart-svg').attr('role', 'img')
      .attr('aria-label', L(`Répartition des salaires nets mensuels en équivalent temps plein dans le secteur privé en ${ins.year}. Médiane : ${money(ins.median_net)}. Moyenne : ${money(ins.mean_net)}.`,
        `Distribution of monthly net full-time-equivalent pay in the private sector in ${ins.year}. Median: ${money(ins.median_net)}. Mean: ${money(ins.mean_net)}.`));
    svg.append('g').attr('class', 'grid').selectAll('line').data(y.ticks(4)).join('line')
      .attr('x1', m.left).attr('x2', W - m.right).attr('y1', (v) => y(v)).attr('y2', (v) => y(v));
    svg.append('g').attr('class', 'axis-label').selectAll('text').data(y.ticks(4)).join('text')
      .attr('x', m.left - 8).attr('y', (v) => y(v)).attr('dy', '0.32em').attr('text-anchor', 'end').text((v) => fmtInt(v));
    const step = W < 560 ? 2000 : 1000;
    svg.append('g').attr('class', 'axis-label').selectAll('text').data(d3.range(Math.ceil(bands[0][0] / step) * step, bands[bands.length - 1][1], step)).join('text')
      .attr('x', (v) => x(v)).attr('y', H - 8).attr('text-anchor', 'middle').text((v) => money(v));
    const bandW = x(bands[0][1]) - x(bands[0][0]);
    const bw = Math.max(1, bandW - 1);
    svg.append('g').selectAll('rect').data(bands).join('rect').attr('class', 'enj-hbar')
      .attr('x', (b) => x(b[0]) + 0.5).attr('width', bw).attr('y', (b) => y(b[2])).attr('height', (b) => y(0) - y(b[2])).attr('rx', Math.min(1.5, bw / 2));
    for (const [v, dash] of [[ins.median_net, null], [ins.mean_net, '5 4']]) {
      svg.append('line').attr('class', 'enj-mark').attr('x1', x(v)).attr('x2', x(v)).attr('y1', m.top).attr('y2', H - m.bottom).attr('stroke-dasharray', dash);
    }
    const tip = document.createElement('div');
    tip.className = 'chart-tip';
    tip.hidden = true;
    host.appendChild(tip);
    svg.append('g').selectAll('rect').data(bands).join('rect').attr('class', 'hit')
      .attr('x', (b) => x(b[0])).attr('width', bandW).attr('y', m.top).attr('height', H - m.top - m.bottom)
      .on('pointermove', (ev, b) => {
        tip.innerHTML = `<div class="tip-date">${esc(`${money(b[0])} – ${money(b[1])}`)}</div><div class="tip-row"><strong>${esc(fmtInt(b[2] * 1000))}</strong><span>${esc(L('emplois en EQTP', 'FTE jobs'))}</span></div>`;
        tip.hidden = false;
        const rect = host.getBoundingClientRect();
        tip.style.left = `${Math.min(rect.width - tip.offsetWidth - 4, Math.max(4, (x(b[0]) / W) * rect.width + 12))}px`;
        tip.style.top = '24px';
      })
      .on('pointerleave', () => { tip.hidden = true; });
  };
  draw();
  host._ro?.disconnect();
  let lastW = host.clientWidth;
  host._ro = new ResizeObserver(debounce(() => {
    if (Math.abs(host.clientWidth - lastW) > 4) { lastW = host.clientWidth; draw(); }
  }, 120));
  host._ro.observe(host);
}

function salaires(d, ctx) {
  const b = d.blocks, ins = d.hand?.insee, sal = d.salaries || {};
  if (!ins) return { blocks: [], body: html`<p class="muted">${L('Données indisponibles.', 'Data unavailable.')}</p>` };
  const insSrc = { title: ins.source.title, url: ins.source.url, date: ins.source.date };
  const ons = d.hand?.ons?.['2022']?.source;
  const gdpFr = last(b.gdp_pc?.fr_eur);
  const gap = (metric) => {
    const s = sal[metric];
    return s?.US?.ppp && s?.FR?.ppp ? { pct: change(s.US.ppp, s.FR.ppp), year: s.US.year } : null;
  };
  const gGdp = gap('gdp'), gWage = gap('wage'), gInc = gap('income');
  const ry = Object.keys(b.rates?.exchange?.FR || {}).sort().pop();
  const xr = ry && b.rates.exchange.FR[ry], pppFr = ry && b.rates.ppp?.FR?.[ry];
  const jobs = sal.jobs || [];
  const job0 = jobs.find((j) => j.id === ctx.query.metier) || jobs.find((j) => j.id === picks.metier) || jobs[0];
  const metric0 = pick('metric', METRICS.map(([k]) => k), 'wage'), mode0 = pick('mode', MODES.map(([k]) => k), 'ppp');
  const mw = last(b.min_wage?.monthly_eur?.FR);
  const bands = ins.distribution;
  const below = bands.find(([lo]) => lo == null), above = bands.find(([, hi]) => hi == null);
  const intl0 = intlRows(sal, metric0, mode0);
  const jobs0 = jobRows(job0, mode0);
  const modeButtons = html`<div class="seg" role="group" aria-label="${L('Conversion en euros', 'Conversion to euros')}">${MODES.map(([k, f, e]) => html`<button type="button" data-mode="${k}" aria-pressed="${String(k === mode0)}">${L(f, e)}</button>`)}</div>`;
  const cards = [{
    id: 'smic', title: L('Le salaire minimum comparé au salaire médian', 'The minimum wage relative to the median wage'),
    lead: L(`Salaire minimum brut en % du salaire brut médian des salariés à temps plein (OCDE).${mw ? ` En France, le SMIC brut était de ${money(mw[1])} par mois au ${fmtPeriod(mw[0])} (Eurostat).` : ''}`,
      `Gross minimum wage as a % of the gross median wage of full-time employees (OECD).${mw ? ` In France, the gross minimum wage (SMIC) was ${money(mw[1])} a month in ${fmtPeriod(mw[0])} (Eurostat).` : ''}`),
    series: b.min_wage?.to_median, freq: 'A', since: '2015', vs: 'DE', fmt: pct, axis: axisPct,
    missing: L('Italie : pas de salaire minimum légal. États-Unis : minimum fédéral ; beaucoup d’États en fixent un plus élevé.', 'Italy: no statutory minimum wage. United States: the federal minimum; many states set a higher one.'),
    sources: [b.min_wage?.source_ratio, mw && b.min_wage?.source_monthly],
  }];
  return {
    intro: L('Ce que gagne un salarié typique en France, mesuré par le salaire médian plutôt que par la moyenne ou le PIB par habitant, et ce que gagnent les mêmes secteurs chez nos voisins.', 'What a typical employee earns in France, measured by the median salary rather than the mean or GDP per head, and what the same sectors pay next door.'),
    blocks: ['earnings_eu', 'earnings_us', 'rates', 'min_wage', 'gdp_pc', 'inequality'],
    cards,
    body: html`${tiles(
      tile(L('Salaire médian', 'Median pay'), money(ins.median_net), L(`net par mois en ${ins.year}`, `net per month in ${ins.year}`)),
      ins.median_net_women && tile(L('Salaire médian des femmes', 'Women’s median pay'), money(ins.median_net_women), L(`net par mois ; hommes : ${money(ins.median_net_men)}`, `net per month; men: ${money(ins.median_net_men)}`)),
      tile(L('10 % gagnent moins de', 'The bottom 10% earn under'), money(ins.d1_net), L('net par mois (1er décile)', 'net per month (1st decile)')),
      tile(L('10 % gagnent plus de', 'The top 10% earn over'), money(ins.d9_net), L('net par mois (9e décile)', 'net per month (9th decile)')),
    )}
    <p class="small muted" style="margin:0">${L(
      `Salariés du secteur privé en équivalent temps plein, d’après l’Insee (${ins.year}). Le SMIC net était de ${money(ins.smic_net)} par mois.`,
      `Private-sector employees in full-time equivalent, from INSEE (${ins.year}). The net minimum wage (SMIC) was ${money(ins.smic_net)} a month.`,
    )}</p>
    <section class="card stack enj-card">
      <h3 style="margin:0">${L('Pourquoi le salaire médian, et pas la moyenne ou le PIB par habitant ?', 'Why the median salary, and not the mean or GDP per head?')}</h3>
      <blockquote class="enj-quote"><span lang="fr">«&#8239;${ins.quote}&#8239;»</span> <span class="tiny faint">Insee, ${fmtDay(ins.source.date)}</span>
        ${lang() === 'en' ? html`<span class="small muted enj-quote-en">Translation: “Half of private-sector employees earn less than ${money(ins.median_net)} net a month in full-time equivalent.”</span>` : ''}</blockquote>
      <ul class="enj-why">
        ${gdpFr ? html`<li>${L(
          `Le PIB par habitant n’est pas un revenu. Celui de la France était de ${money(gdpFr[1])} en ${gdpFr[0]}${String(gdpFr[2] || '').includes('p') ? ' (chiffre provisoire)' : ''}, soit ${money(gdpFr[1] / 12)} par mois et par habitant : il divise toute la richesse produite dans le pays, y compris les bénéfices des entreprises, l’investissement et ce que financent les impôts, par tous les habitants, enfants et retraités compris.`,
          `GDP per head isn’t an income. France’s was ${money(gdpFr[1])} in ${gdpFr[0]}${String(gdpFr[2] || '').includes('p') ? ' (provisional)' : ''}, or ${money(gdpFr[1] / 12)} a month per inhabitant: it divides everything produced in the country, including company profits, investment and what taxes pay for, by every inhabitant, children and retirees included.`,
        )}</li>` : ''}
        <li>${L(
          `La moyenne est tirée vers le haut par les plus hauts salaires : en ${ins.year}, le salaire moyen était de ${money(ins.mean_net)} net par mois, mais la moitié des salariés gagnaient moins de ${money(ins.median_net)}. La médiane coupe les salariés en deux moitiés égales : quelques très hauts salaires ne la font pas bouger.`,
          `The mean is pulled up by the highest salaries: in ${ins.year}, mean pay was ${money(ins.mean_net)} net a month, but half of employees earned less than ${money(ins.median_net)}. The median splits employees into two equal halves: a few very high salaries don’t move it.`,
        )}</li>
        ${gGdp && gWage && gInc ? html`<li>${L(
          `Entre pays, l’écart dépend de la mesure. Aux prix français, les États-Unis dépassent la France de ${pct(gGdp.pct, 0)} en PIB par habitant (${gGdp.year}), mais de ${pct(gWage.pct, 0)} en salaire médian à temps plein (${gWage.year}) et de ${pct(gInc.pct, 0)} en niveau de vie médian (${gInc.year}).`,
          `Between countries, the gap depends on the measure. At French prices, the United States is ahead of France by ${pct(gGdp.pct, 0)} in GDP per head (${gGdp.year}), but by ${pct(gWage.pct, 0)} in median full-time pay (${gWage.year}) and ${pct(gInc.pct, 0)} in median disposable income (${gInc.year}).`,
        )}</li>` : ''}
        <li>${L(
          'Le salaire médian de l’Insee ne couvre que les salariés du privé : ni les fonctionnaires, ni les indépendants, ni les chômeurs, ni les retraités. Le niveau de vie médian, dans le comparatif ci-dessous, couvre toute la population, après impôts et prestations.',
          'INSEE’s median salary covers private-sector employees only: not civil servants, the self-employed, the unemployed or retirees. Median disposable income, in the comparison below, covers the whole population, after taxes and benefits.',
        )}</li>
      </ul>
      ${sourcesLine([insSrc, b.gdp_pc?.source_fr])}
    </section>
    <section class="card stack enj-card">
      <div><h3 style="margin:0">${L(`Combien gagnent les salariés du privé (${ins.year})`, `What private-sector employees earn (${ins.year})`)}</h3>
        <p class="small muted" style="margin:4px 0 0">${L('Emplois en équivalent temps plein, en milliers, par tranche de 100 € de salaire net mensuel.', 'Full-time-equivalent jobs, in thousands, by €100 band of monthly net pay.')}</p></div>
      <div class="enj-hist" data-chart="hist"></div>
      ${below && above ? html`<p class="small muted" style="margin:0">${L(
        `Hors graphique : ${fmtInt(below[2] * 1000)} emplois sous ${money(below[1])}, en grande partie des apprentis et des stagiaires, dont les salaires ne suivent pas les règles du SMIC (Insee), et ${fmtInt(above[2] * 1000)} à ${money(above[0])} ou plus.`,
        `Not shown: ${fmtInt(below[2] * 1000)} jobs under ${money(below[1])}, largely apprentices and interns, whose pay isn’t bound by the minimum-wage rules (INSEE), and ${fmtInt(above[2] * 1000)} at ${money(above[0])} or more.`,
      )}</p>` : ''}
      <details class="enj-table"><summary class="small">${L('Voir en tableau', 'Show as a table')}</summary>
        <div class="table-wrap" style="margin-top:8px"><table class="data"><caption class="sr-only">${L('Répartition des salaires', 'Pay distribution')}</caption>
          <thead><tr><th>${L('Salaire net mensuel', 'Monthly net pay')}</th><th class="r">${L('Emplois en EQTP', 'FTE jobs')}</th></tr></thead>
          <tbody>${bands.map(([lo, hi, n]) => html`<tr><td>${lo == null ? L(`moins de ${money(hi)}`, `under ${money(hi)}`) : hi == null ? L(`${money(lo)} ou plus`, `${money(lo)} or more`) : `${money(lo)} – ${money(hi)}`}</td><td class="r">${fmtInt(n * 1000)}</td></tr>`)}</tbody></table></div></details>
      ${sourcesLine([insSrc])}
    </section>
    <section class="card stack enj-card">
      <div><h3 style="margin:0">${L(`Depuis ${ins.index_first_year}, hors inflation`, `Since ${ins.index_first_year}, after inflation`)}</h3>
        <p class="small muted" style="margin:4px 0 0">${L(`Salaires nets en équivalent temps plein, en euros constants, indice 100 en ${ins.index_first_year}.`, `Net full-time-equivalent pay in constant euros, index 100 in ${ins.index_first_year}.`)}</p></div>
      <label class="enj-vs small muted">${L('Comparer le salaire médian avec', 'Compare median pay with')} <select class="input enj-select" data-pick="indice">${IDX.map(([k, f, e]) => html`<option value="${k}" ${k === picks.indice ? 'selected' : ''}>${L(f, e)}</option>`)}</select></label>
      <div class="enj-line" data-chart="indice"></div>
      <p class="tiny faint" style="margin:0">${L('Selon l’Insee, le pic de 2020 reflète des modifications ponctuelles de la structure des emplois pendant la crise du Covid.', 'According to INSEE, the 2020 peak reflects one-off changes in the mix of jobs during the Covid crisis.')}</p>
      ${sourcesLine([insSrc])}
    </section>
    <section class="card stack enj-card" id="enj-intl">
      <div><h3 style="margin:0">${L('La France et ses voisins', 'France and its neighbours')}</h3>
        <p class="small muted" style="margin:4px 0 0">${L('Trois mesures du niveau de vie, par an, en euros. Le salaire médian et le niveau de vie médian disent ce que touche une personne ordinaire ; le PIB par habitant mesure la taille de l’économie.', 'Three measures of living standards, per year, in euros. Median pay and median disposable income say what an ordinary person receives; GDP per head measures the size of the economy.')}</p></div>
      <div class="row enj-switches">
        <div class="seg" role="group" aria-label="${L('Mesure', 'Measure')}">${METRICS.map(([k, f, e]) => html`<button type="button" data-metric="${k}" aria-pressed="${String(k === metric0)}">${L(f, e)}</button>`)}</div>
        ${modeButtons}
      </div>
      <p class="small muted" data-out="metric-lead" style="margin:0">${METRIC_LEAD[metric0]()}</p>
      <div data-out="intl">${bars(intl0, { label: metricTitle(metric0) })}</div>
      <div data-out="intl-table">${moneyTable(metricTitle(metric0), intl0)}</div>
      ${xr && pppFr ? html`<p class="tiny faint" style="margin:0">${L(
        `Conversion : en ${ry}, 1 $ valait en moyenne ${fmtNum(xr, 2)} € au taux de change, mais ce qui coûte 1 $ aux États-Unis coûtait en moyenne ${fmtNum(pppFr, 2)} € en France (parités de pouvoir d’achat de la consommation des ménages, OCDE). « Aux prix français » dit ce qu’un montant permettrait d’acheter en France ; c’est la méthode de l’OCDE pour comparer les salaires.`,
        `Conversion: in ${ry}, $1 was worth €${fmtNum(xr, 2)} on average at the market exchange rate, but what costs $1 in the United States cost €${fmtNum(pppFr, 2)} on average in France (purchasing power parities for household consumption, OECD). “At French prices” says what an amount would buy in France; it is how the OECD compares pay.`,
      )}</p>` : ''}
      ${sourcesLine([b.earnings_eu?.source, ons, b.earnings_us?.source, b.inequality?.source, b.gdp_pc?.source, b.rates?.source])}
    </section>
    <section class="card stack enj-card" id="enj-jobs">
      <div><h3 style="margin:0">${L('Par secteur', 'By sector')}</h3>
        <p class="small muted" style="margin:4px 0 0">${L('Salaire brut, avant l’impôt sur le revenu, converti en euros : le salaire horaire médian de chaque secteur, ou le montant annuel du salaire minimum. La note sous le menu dit ce que mesure chaque chiffre.', 'Gross pay, before income tax, converted to euros: the median hourly pay in each sector, or the yearly amount of the minimum wage. The note under the menu says what each figure measures.')}</p></div>
      <div class="row enj-switches">
        <label class="enj-vs small muted">${L('Comparer', 'Compare')} <select class="input enj-select" data-pick="metier">${JOB_GROUPS.map(([re, f, e]) => {
          const js = jobs.filter((j) => re.test(j.id));
          return js.length ? html`<optgroup label="${L(f, e)}">${js.map((j) => html`<option value="${j.id}" ${j === job0 ? 'selected' : ''}>${L(j.fr, j.en)}</option>`)}</optgroup>` : '';
        })}</select></label>
        ${modeButtons}
      </div>
      <p class="small muted" data-out="job-note" style="margin:0">${jobNote(job0)}</p>
      <div data-out="jobs">${bars(jobs0, { label: jobTitle(job0) })}</div>
      <div data-out="jobs-table">${moneyTable(jobTitle(job0), jobs0)}</div>
      <div data-out="job-src">${sourcesLine([JOB_SOURCES[job0?.source]?.(b), b.rates?.source])}</div>
    </section>
    ${cards.map((m) => compareCard(m))}
    ${notes([
      L(`Net et brut : le salaire net est le brut moins les cotisations et contributions sociales (dont la CSG et la CRDS) payées par le salarié, environ un quart du brut (en ${ins.year}, ${money(ins.mean_gross)} brut pour ${money(ins.mean_net)} net en moyenne). L’impôt sur le revenu n’est pas déduit.`,
        `Net and gross: net pay is gross pay minus the social contributions (including the CSG and CRDS levies) paid by the employee, about a quarter of gross pay (in ${ins.year}, ${money(ins.mean_gross)} gross for ${money(ins.mean_net)} net on average). Income tax is not deducted.`),
      L('Équivalent temps plein (EQTP) : chaque salaire est ramené à un poste à temps plein occupé toute l’année. Champ de l’Insee : salariés du privé, alternants, stagiaires et contrats aidés compris, hors agriculture et particuliers employeurs.',
        'Full-time equivalent (FTE): each salary is converted to a full-time job held all year. INSEE’s scope: private-sector employees, including apprentices, interns and subsidised contracts, excluding agriculture and household employers.'),
      L('Comparaisons entre pays : salaires bruts, avant les cotisations du salarié et l’impôt. Ce que paient ces prélèvements diffère d’un pays à l’autre : en France, ils financent notamment l’assurance maladie et la retraite ; aux États-Unis, beaucoup de salariés paient en plus une partie de leur assurance santé sur leur salaire.',
        'Comparisons between countries: gross pay, before employees’ contributions and income tax. What those deductions pay for differs from country to country: in France they fund health insurance and pensions, among other things; in the United States, many employees also pay part of their health insurance out of their pay.'),
      L(`Médiane plutôt que moyenne : Eurostat et l’OCDE publient la rémunération par métier (enseignants, infirmiers, médecins, grandes familles de métiers) en moyenne, pas en médiane, tout comme l’Insee celle des catégories (cadres, employés, ouvriers) dans sa publication sur ${ins.year} ; la page compare donc les secteurs, dont Eurostat publie la médiane. Un secteur compte tous ses salariés, quel que soit leur métier. Les années sont indiquées à chaque fois.`,
        `Median rather than mean: Eurostat and the OECD publish pay by occupation (teachers, nurses, doctors, broad occupation groups) as means, not medians, as does INSEE’s release on ${ins.year} for occupational categories (managers, clerical workers, manual workers); the page therefore compares sectors, for which Eurostat publishes the median. A sector counts all its employees, whatever their job. Years are shown each time.`),
    ])}`,
    mount(root) {
      const hist = root.querySelector('[data-chart="hist"]');
      if (hist) drawHistogram(hist, ins);
      const isel = root.querySelector('[data-pick="indice"]'), ihost = root.querySelector('[data-chart="indice"]');
      if (isel && ihost) {
        const idx = (k) => ins.index_1996[k].map((v, i) => ({ x: new Date(ins.index_first_year + i, 0, 1), y: v }));
        const drawIdx = () => {
          const [k, f, e] = IDX.find((p) => p[0] === isel.value);
          drawSingle(ihost, { name: L('Salaire médian', 'Median pay'), values: idx('median'), fmt: (v) => fmtNum(v, 1), axis: (v) => fmtNum(v, 0), freq: 'A', ref: { name: L(f, e), values: idx(k) } });
        };
        isel.addEventListener('change', () => { picks.indice = isel.value; drawIdx(); });
        drawIdx();
      }
      let metric = metric0, mode = mode0, job = job0;
      if (job && job.id === ctx.query.metier) picks.metier = job.id;
      const out = (k) => root.querySelector(`[data-out="${k}"]`);
      const renderIntl = () => {
        const rows = intlRows(sal, metric, mode);
        out('intl').innerHTML = String(bars(rows, { label: metricTitle(metric) }));
        out('intl-table').innerHTML = String(moneyTable(metricTitle(metric), rows));
        out('metric-lead').textContent = METRIC_LEAD[metric]();
      };
      const renderJobs = () => {
        const rows = jobRows(job, mode);
        out('jobs').innerHTML = String(bars(rows, { label: jobTitle(job) }));
        out('jobs-table').innerHTML = String(moneyTable(jobTitle(job), rows));
        out('job-note').textContent = jobNote(job);
        out('job-src').innerHTML = String(sourcesLine([JOB_SOURCES[job?.source]?.(b), b.rates?.source]));
      };
      root.querySelectorAll('[data-metric]').forEach((btn) => btn.addEventListener('click', () => {
        metric = picks.metric = btn.dataset.metric;
        root.querySelectorAll('[data-metric]').forEach((x) => x.setAttribute('aria-pressed', String(x === btn)));
        renderIntl();
      }));
      // Both cards share one conversion, so either switch moves both.
      root.querySelectorAll('[data-mode]').forEach((btn) => btn.addEventListener('click', () => {
        mode = picks.mode = btn.dataset.mode;
        root.querySelectorAll('[data-mode]').forEach((x) => x.setAttribute('aria-pressed', String(x.dataset.mode === mode)));
        renderIntl();
        renderJobs();
      }));
      root.querySelector('[data-pick="metier"]')?.addEventListener('change', (e) => {
        job = jobs.find((j) => j.id === e.target.value) || job;
        picks.metier = job.id;
        // The address names the job, so it can be shared and a redraw keeps it.
        history.replaceState(null, '', `#/fr/enjeux?t=salaires&metier=${encodeURIComponent(job.id)}`);
        scrolledTo = location.hash;
        renderJobs();
      });
      // A link to one job (from the education tab, or shared) lands on the jobs card. The
      // timer runs after the router's own scroll to the top, which follows this mount.
      if (ctx.query.metier && scrolledTo !== location.hash) {
        scrolledTo = location.hash;
        setTimeout(() => root.querySelector('#enj-jobs')?.scrollIntoView({ block: 'start', behavior: 'instant' }), 0);
      }
    },
  };
}

// The page ----------------------------------------------------------------------------

const BUILDERS = { economie, inflation, immigration, criminalite, ecart, education, salaires };
const tabOf = (ctx) => (BUILDERS[ctx.query.t] ? ctx.query.t : 'economie');

export const enjeux = {
  title: () => L('Les grands enjeux', 'Major issues'),
  async render(ctx) {
    const [d, pres, positions] = await Promise.all([loadEnjeux(), loadPres(), loadPositions()]);
    if (!d) return html`<div class="wrap page"><div class="empty"><h3>${L('Données indisponibles', 'Data unavailable')}</h3><p>${L('Les chiffres n’ont pas pu être chargés. Réessayez plus tard.', 'The figures couldn’t be loaded. Please try again later.')}</p></div></div>`;
    const t = tabOf(ctx);
    const tab = BUILDERS[t](d, ctx);
    const [, fr, en] = TABS.find(([k]) => k === t);
    const stale = (tab.blocks || []).some((k) => d.stale?.includes(k));
    return html`<div class="wrap page stack-lg">
      <nav class="crumbs"><a href="#/fr">${L('France', 'France')}</a><span>/</span><span>${L('Les grands enjeux', 'Major issues')}</span></nav>
      <div><div class="eyebrow">${L('Les grands enjeux', 'Major issues')}</div>
        <h1 style="margin:6px 0 8px">${L('Les grands enjeux en chiffres', 'The major issues in numbers')}</h1>
        <p class="muted" style="margin:0;max-width:860px">${L(
          `Les chiffres officiels derrière les grands débats de la présidentielle, la France comparée à ses voisins et aux États-Unis, et ce qu’en disent les candidats déclarés. Chaque chiffre vient d’un organisme statistique public ou international, avec sa source ; les données sont relues chaque jour (dernière mise à jour le ${fmtDay(d.updated)}).`,
          `The official figures behind the main debates of the presidential race, France next to its neighbours and the United States, and what the declared candidates say. Every figure comes from a public or international statistics body, with its source; the data is reread every day (last updated ${fmtDay(d.updated)}).`,
        )}</p></div>
      <nav class="seg big enj-tabs" aria-label="${L('Thèmes', 'Topics')}">${TABS.map(([k, f, e]) => html`<a href="#/fr/enjeux?t=${k}" aria-current="${k === t ? 'page' : 'false'}">${L(f, e)}</a>`)}</nav>
      ${stale ? html`<div class="notice warn">${icon.info()}<div>${L('Certaines sources n’ont pas pu être relues aujourd’hui : les chiffres concernés sont ceux de la dernière lecture réussie.', 'Some sources couldn’t be reread today: the figures concerned are from the last successful read.')}</div></div>` : ''}
      <div><h2 style="margin:0">${L(fr, en)}</h2><p class="muted" style="margin:6px 0 0">${tab.intro || ''}</p></div>
      ${tab.body}
      ${candidatesBlock(QUESTIONS[t], pres, positions)}
    </div>`;
  },
  async mount(root, ctx) {
    const d = await loadEnjeux();
    if (!d) return null;
    const tab = BUILDERS[tabOf(ctx)](d, ctx);
    for (const m of tab.cards || []) if (m.line !== false) drawLines(root, m);
    tab.mount?.(root);
    return () => root.querySelectorAll('.enj-line, .enj-hist').forEach((el) => el._ro?.disconnect());
  },
};
