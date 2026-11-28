// Major news, inflation tracker, parties and values, site donations, about the data.

import { html, raw, fetchJSON, fmtDate, timeAgo, fmtPct, fmtNum, fmtInt, signed } from '../util.js';
import { icon } from '../icons.js';
import { PARTIES, GROUPS, PARTIES_AS_OF, PARTIES_AS_OF_FR, ROLE_FR } from '../data/parties.js';
import { L, lang } from '../i18n.js';
import { lineChart, cssVar } from '../lib/charts.js';
import { wireTableToggles } from '../components/race.js';
import { realRaceCount, researchedCount, statusData, modelCheck, racesMeta, controlData, officeCount, officesResearched, resultsIn, certifiedList, allCertified, certExceptions } from '../data/world.js';
import { STATES, stateName } from '../data/states.js';
import { DONATE_URL, SHOW_EARLY_VOTE, SUPPORT_EMAIL, MAIL_SERVICE_URL, REMINDER_FROM } from '../config.js';

const ext = (href, label) => html`<a href="${href}" target="_blank" rel="noopener noreferrer">${label} ${icon.external()}</a>`;

// News ------------------------------------------------------------------------------

let newsCache = null;
const TOPICS = ['Gains & momentum', 'Scandals', 'Endorsements', 'Turnout', 'Money & ads', 'Debates', 'Campaign trail'];
// The filters' values stay in English (they are the feed's tags and the address's query); only their labels change.
const CHIP_FR = { 'Gains & momentum': 'Dynamique', Scandals: 'Scandales', Endorsements: 'Soutiens', Turnout: 'Participation', 'Money & ads': 'Argent et publicités',
  Debates: 'Débats', 'Campaign trail': 'Sur le terrain', Senate: 'Sénat', House: 'Chambre', Governor: 'Gouverneurs', Democrats: 'Démocrates', Republicans: 'Républicains' };
const chipL = (v) => L(CHIP_FR[v] || v, v);

export const news = {
  title: () => L('L’actualité de l’élection', 'Major election news'),
  async render(ctx) {
    try { newsCache = newsCache || await fetchJSON('data/news.json'); } catch { newsCache = null; }
    if (!newsCache) return html`<div class="wrap page"><div class="empty">${icon.news()}<h3>${L('Les actualités ne sont pas disponibles', 'News isn’t available')}</h3><p>${L('Lancez', 'Run')} <code>scripts/update_news.py</code> ${L('pour récupérer les derniers titres.', 'to fetch the latest headlines.')}</p></div></div>`;
    const q = ctx.query;
    const topic = TOPICS.includes(q.topic) ? q.topic : null;
    const race = ['Senate', 'House', 'Governor'].includes(q.race) ? q.race : null;
    const party = ['Democrats', 'Republicans'].includes(q.party) ? q.party : null;
    const items = newsCache.items.filter((it) => (!topic || it.topic === topic || it.topics.includes(topic)) && (!race || it.races.includes(race)) && (!party || it.parties.includes(party)));
    const link = (k, v) => {
      const p = new URLSearchParams({ ...(topic && { topic }), ...(race && { race }), ...(party && { party }) });
      if (p.get(k) === v) p.delete(k); else p.set(k, v);
      return `#/news${p.toString() ? `?${p}` : ''}`;
    };
    const chip = (k, v, cur) => html`<a class="chip" href="${link(k, v)}" ${raw(cur === v ? 'aria-current="page" style="background:var(--text-1);color:var(--bg);border-color:var(--text-1)"' : '')}>${chipL(v)}</a>`;
    return html`<div class="wrap page stack">
      <div><div class="eyebrow">${L('L’actualité de l’élection', 'Major news regarding the election')}</div><h1>${L('Les dernières nouvelles de la campagne', 'The latest from the campaign trail')}</h1>
        <p class="muted">${L(`Les titres sur l’élection de ${newsCache.feeds.length} médias américains de tout le spectre politique, classés par thème et publiés en anglais. Mis à jour ${timeAgo(newsCache.updated)} (${fmtDate(newsCache.updated)}).`, `Election headlines from ${newsCache.feeds.length} outlets across the political spectrum, sorted by topic. Updated ${timeAgo(newsCache.updated)} (${fmtDate(newsCache.updated)}).`)}</p></div>
      <div class="stack-sm">
        <div class="filters" role="group" aria-label="${L('Thème', 'Topic')}"><span class="eyebrow">${L('Thème', 'Topic')}</span>${TOPICS.map((t) => chip('topic', t, topic))}</div>
        <div class="filters" role="group" aria-label="${L('Élection et parti', 'Race and party')}"><span class="eyebrow">${L('Élection', 'Race')}</span>${['Senate', 'House', 'Governor'].map((t) => chip('race', t, race))}<span class="eyebrow" style="margin-left:10px">${L('Parti', 'Party')}</span>${['Democrats', 'Republicans'].map((t) => chip('party', t, party))}</div>
      </div>
      <div class="news-list">${items.length ? items.map((it) => html`<article class="news-item">
        <div class="news-meta"><span class="src">${it.source}</span><span>${it.published ? timeAgo(it.published) : ''}</span><span class="topic-tag">${chipL(it.topic)}</span>${it.races.map((r) => html`<span class="topic-tag">${chipL(r)}</span>`)}</div>
        <a class="headline" href="${it.link}" target="_blank" rel="noopener noreferrer" lang="en">${it.title}</a>
        ${it.summary ? html`<p class="small muted" style="margin:0" lang="en">${it.summary}</p>` : ''}
      </article>`) : html`<div class="empty">${L('Aucun article ne correspond à ces filtres.', 'No stories match these filters.')}</div>`}</div>
      <p class="small faint">${L(`Sources : ${newsCache.feeds.map((f) => f.name).join(', ')}. Les titres renvoient au média d’origine. Les thèmes sont attribués automatiquement d’après des mots-clés et peuvent être faux.`, `Sources: ${newsCache.feeds.map((f) => f.name).join(', ')}. Headlines link to the original publisher. Topic tags are assigned automatically from keywords and can be wrong.`)}</p>
    </div>`;
  },
};

// Inflation -------------------------------------------------------------------------

let inflCache = null;
const GROUP_ORDER = ['Overall', 'Food', 'Energy', 'Cars', 'Housing', 'Health', 'Interest rates'];

function yoy(data) {
  const byMonth = new Map(data);
  return data.map(([m, v]) => {
    const [y, mo] = m.split('-');
    const prev = byMonth.get(`${+y - 1}-${mo}`);
    return [m, prev ? (v / prev - 1) * 100 : null];
  }).filter(([, v]) => v != null);
}
const toDate = (m) => new Date(+m.slice(0, 4), +m.slice(5, 7) - 1, 15);
const loc = () => (lang() === 'fr' ? 'fr-FR' : 'en-US');
const price = (v, d) => (lang() === 'fr' ? `${fmtNum(v, d)} $` : `$${v.toFixed(d)}`);
const seriesFmt = (s) => (s.kind === 'price' ? (v) => price(v, s.unit.includes('kWh') ? 3 : 2) : (v) => fmtPct(v, 1));
const yrs = (n) => L(`${n} an${n > 1 ? 's' : ''}`, `${n} yr${n > 1 ? 's' : ''}`);
// The series' names and units come in English from update_inflation.py.
const SERIES_FR = {
  'All items (headline CPI)': 'Ensemble des prix (IPC)', 'Core CPI (excludes food and energy)': 'IPC sous-jacent (hors alimentation et énergie)',
  'Groceries (food at home)': 'Courses alimentaires (repas à la maison)', 'Restaurants (food away from home)': 'Restaurants (repas pris dehors)',
  'Eggs, grade A large': 'Œufs, gros calibre (catégorie A)', 'Milk, whole': 'Lait entier', 'Bread, white': 'Pain blanc', 'Ground beef': 'Bœuf haché',
  'Chicken, whole': 'Poulet entier', 'Chicken breast, boneless': 'Blanc de poulet, sans os', 'Coffee, ground': 'Café moulu', Bananas: 'Bananes',
  'Cheddar cheese': 'Cheddar', Tomatoes: 'Tomates', 'Flour, all-purpose': 'Farine tout usage', 'Gasoline, regular': 'Essence ordinaire',
  'Gasoline (CPI)': 'Essence (IPC)', Electricity: 'Électricité', 'Electricity (CPI)': 'Électricité (IPC)', 'New vehicles': 'Véhicules neufs',
  'Used cars and trucks': 'Voitures et pick-up d’occasion', Rent: 'Loyers', 'Medical care': 'Soins médicaux', 'Federal funds rate': 'Taux directeur de la Fed',
  '30-year fixed mortgage': 'Prêt immobilier à taux fixe sur 30 ans', '10-year Treasury yield': 'Taux des emprunts d’État à 10 ans',
  'Credit card interest rate': 'Taux des cartes de crédit', 'New car loan rate (48-month)': 'Taux des crédits auto neufs (48 mois)',
};
const UNIT_FR = { '$ per dozen': '$ la douzaine', '$ per gallon': '$ le gallon (3,8 litres)', '$ per lb': '$ la livre (454 g)', '$ per kWh': '$ le kWh', '%': '%' };
const GROUP_FR = { Overall: 'Vue d’ensemble', Food: 'Alimentation', Energy: 'Énergie', Cars: 'Voitures et transports', Housing: 'Logement', Health: 'Santé', 'Interest rates': 'Taux d’intérêt' };
const labelL = (s) => L(SERIES_FR[s.label] || s.label, s.label);
const unitL = (u) => L(UNIT_FR[u] || u, u);

function view(series, years) {
  const raw0 = series.kind === 'index' ? yoy(series.data) : series.data;
  const last = raw0[raw0.length - 1];
  const cutoff = toDate(last[0]);
  cutoff.setFullYear(cutoff.getFullYear() - years);
  const pts = raw0.filter(([m]) => toDate(m) >= cutoff);
  return pts;
}

function seriesCard(s, years, idx) {
  const pts = view(s, years);
  if (!pts.length) return '';
  const [lm, lv] = pts[pts.length - 1];
  const [, fv] = pts[0];
  const fmt = seriesFmt(s);
  let change, changeCls = '';
  if (s.kind === 'price') {
    const pct = (lv / fv - 1) * 100;
    change = L(`${signed(pct, 1, '%')} en ${yrs(years)}`, `${signed(pct, 1, '%')} over ${yrs(years)}`);
    changeCls = pct > 0 ? 'delta-up' : 'delta-down';
  } else {
    const d = lv - fv;
    change = L(`${signed(d, 1, ' pt')} par rapport à il y a ${yrs(years)}`, `${signed(d, 1, ' pts')} vs ${yrs(years)} ago`);
    changeCls = d > 0 ? 'delta-up' : 'delta-down';
  }
  const tid = `itbl-${idx}`;
  return html`<article class="card series-card">
    <div class="head"><div><div class="eyebrow">${s.kind === 'index' ? L('Inflation sur un an', 'Yearly inflation rate') : unitL(s.unit)}</div><h3 style="margin:2px 0 0">${labelL(s)}</h3></div>
      <div style="text-align:right"><div class="val">${fmt(lv)}</div><div class="small ${changeCls}">${change}</div></div></div>
    <div class="chart" data-infl="${s.id}"></div>
    <div class="row between"><span class="tiny faint">${L('Dernière donnée : ', 'Latest: ')}${toDate(lm).toLocaleString(loc(), { month: 'long', year: 'numeric' })} · ${s.id}</span><button type="button" class="btn btn-sm btn-ghost" data-table-toggle="${tid}">${icon.table()} ${L('Tableau', 'Table')}</button></div>
    <div class="table-wrap" id="${tid}" hidden><table class="data"><thead><tr><th>${L('Mois', 'Month')}</th><th class="r">${s.kind === 'index' ? L('Évolution sur un an', 'Change from a year earlier') : L('Valeur', 'Value')}</th></tr></thead><tbody>${pts.slice().reverse().map(([m, v]) => html`<tr><td>${toDate(m).toLocaleString(loc(), { month: 'short', year: 'numeric' })}</td><td class="r">${fmt(v)}</td></tr>`)}</tbody></table></div>
  </article>`;
}

export const inflation = {
  title: () => L('Suivi de l’inflation', 'Inflation tracker'),
  async render(ctx) {
    try { inflCache = inflCache || await fetchJSON('data/inflation.json'); } catch { inflCache = null; }
    if (!inflCache?.series?.length) return html`<div class="wrap page"><div class="empty">${L('Les données sur l’inflation ne sont pas disponibles. Lancez', 'Inflation data isn’t available. Run')} <code>scripts/update_inflation.py</code>.</div></div>`;
    const years = [1, 2, 3, 4, 5].includes(+ctx.query.years) ? +ctx.query.years : 2;
    const byId = Object.fromEntries(inflCache.series.map((s) => [s.id, s]));
    const head = (id) => byId[id] ? yoy(byId[id].data).slice(-1)[0] : null;
    const cpi = head('CPIAUCNS'), core = head('CPILFENS');
    const last = (id) => byId[id]?.data.slice(-1)[0];
    const gas = last('APU000074714'), mort = last('MORTGAGE30US');
    let idx = 0;
    return html`<div class="wrap page stack-lg">
      <div><div class="eyebrow">${L('Suivi de l’inflation', 'Inflation tracker')}</div><h1>${L('Ce que coûtent les choses, et à quelle vitesse les prix changent', 'What things cost, and how fast it’s changing')}</h1>
        <p class="muted">${L(`Les chiffres officiels des prix aux États-Unis : l’indice des prix à la consommation (IPC) et les prix moyens du Bureau of Labor Statistics, et les taux d’intérêt de la Réserve fédérale et de Freddie Mac. Données du ${fmtDate(inflCache.updated)}.`, `Official government price data: the Consumer Price Index and average prices from the Bureau of Labor Statistics, and interest rates from the Federal Reserve and Freddie Mac. Snapshot ${fmtDate(inflCache.updated)}.`)}</p></div>
      <div class="grid grid-4">
        ${cpi ? html`<div class="stat"><div class="eyebrow">${L('Inflation (IPC)', 'Inflation (CPI)')}</div><div class="value">${fmtPct(cpi[1])}</div><div class="sub">${L('sur un an, en', 'year over year,')} ${toDate(cpi[0]).toLocaleString(loc(), { month: 'long' })}</div></div>` : ''}
        ${core ? html`<div class="stat"><div class="eyebrow">${L('Inflation sous-jacente', 'Core inflation')}</div><div class="value">${fmtPct(core[1])}</div><div class="sub">${L('hors alimentation et énergie', 'excluding food and energy')}</div></div>` : ''}
        ${gas ? html`<div class="stat"><div class="eyebrow">${L('Essence', 'Gasoline')}</div><div class="value">${price(gas[1], 2)}</div><div class="sub">${L('le gallon (3,8 litres), ordinaire', 'per gallon, regular')}</div></div>` : ''}
        ${mort ? html`<div class="stat"><div class="eyebrow">${L('Prêt immobilier sur 30 ans', '30-year mortgage')}</div><div class="value">${fmtPct(mort[1], 2)}</div><div class="sub">${L('taux moyen', 'average rate')}</div></div>` : ''}
      </div>
      <div class="row between"><div class="seg" role="group" aria-label="${L('Période', 'Time range')}">${[1, 2, 3, 4, 5].map((y) => html`<a href="#/inflation?years=${y}" ${raw(y === years ? 'aria-current="page"' : '')}>${L(`${y} an${y > 1 ? 's' : ''}`, `${y} year${y > 1 ? 's' : ''}`)}</a>`)}</div>
        <span class="small faint">${L('Les prix qui montent plus vite sont en rouge, ceux qui baissent ou ralentissent en vert.', 'Prices rising faster is shown in red; falling or slowing in green.')}</span></div>
      ${GROUP_ORDER.map((g) => {
        const list = inflCache.series.filter((s) => s.group === g);
        if (!list.length) return '';
        return html`<section><div class="section-head"><h2 style="margin:0">${L(GROUP_FR[g] || g, g === 'Cars' ? 'Cars and transportation' : g)}</h2></div><div class="grid grid-3">${list.map((s) => seriesCard(s, years, idx++))}</div></section>`;
      })}
      <p class="small faint">${L(`Sources : ${inflCache.sources.CPI} ; ${inflCache.sources.MORTGAGE30US} ; ${inflCache.sources.rates}. ${inflCache.sources.via}. L’inflation sur un an compare chaque mois au même mois de l’année précédente. Quelques mois manquent, quand l’administration n’a pas publié de chiffres (par exemple pendant la paralysie budgétaire de l’automne 2025).`, `Sources: ${inflCache.sources.CPI}; ${inflCache.sources.MORTGAGE30US}; ${inflCache.sources.rates}. ${inflCache.sources.via}. Yearly inflation compares each month with the same month a year earlier. A few months are missing where the government did not publish data (for example during the fall 2025 shutdown).`)}</p>
    </div>`;
  },
  mount(root, ctx) {
    if (!inflCache?.series?.length) return;
    const years = [1, 2, 3, 4, 5].includes(+ctx.query.years) ? +ctx.query.years : 2;
    const color = cssVar('--dem');
    root.querySelectorAll('[data-infl]').forEach((el) => {
      const s = inflCache.series.find((x) => x.id === el.dataset.infl);
      const pts = view(s, years);
      const fmt = seriesFmt(s);
      lineChart(el, {
        series: [{ name: labelL(s), color, values: pts.map(([m, v]) => ({ x: toDate(m), y: v })) }],
        height: 150, yFormat: fmt, area: true, baseline: s.kind === 'index' ? 0 : null, endLabels: false,
        label: L(`${labelL(s)} sur ${yrs(years)}`, `${s.label} over ${years} years`),
      });
    });
    wireTableToggles(root);
  },
};

// Parties ---------------------------------------------------------------------------

function ladder(leaders) {
  if (!leaders?.length) return '';
  return html`<ol class="ladder">${leaders.map(([role, who, whoFr]) => html`<li><span><span class="role">${L(ROLE_FR[role] || role, role)}</span><span class="who">${L(whoFr || whoL(who), who)}</span></span></li>`)}</ol>`;
}
// "Rep. Greg Casar (TX)" → "Greg Casar (Chambre, TX)": French has no neutral word for "Rep.".
const whoL = (who) => who.replace(/^Rep\. (.+) \(([^)]+)\)$/, '$1 (Chambre, $2)');
const fr = (o, k) => (lang() === 'fr' && o[`${k}Fr`]) || o[k];
function groupCard(id) {
  const g = GROUPS[id];
  return html`<div class="group-card">
    <div class="row between"><h3 style="margin:0">${fr(g, 'name')}</h3>${ext(g.site, L('Site officiel', 'Official site'))}</div>
    <p class="small muted" style="margin:6px 0 0">${fr(g, 'blurb')}</p>
    <ul class="small muted" style="padding-left:18px;margin:8px 0 0">${fr(g, 'values').map((v) => html`<li style="margin:4px 0">${v}</li>`)}</ul>
    ${ladder(g.leaders)}
    <p class="tiny faint" style="margin:8px 0 0">${L('Source : ', 'Source: ')}${ext(g.source, fr(g, 'sourceLabel'))}</p>
  </div>`;
}
function partyCard(p) {
  return html`<article class="card party-card tone-${p.tone} stack">
    <div class="row between"><h2 style="margin:0">${fr(p, 'name')}</h2>${ext(p.site, L('Site officiel', 'Official site'))}</div>
    <p class="muted" style="margin:0">${fr(p, 'blurb')}</p>
    <div class="grid grid-2" style="align-items:start">
      <div><div class="eyebrow">${L('Ce que le parti dit défendre', 'What the party says it stands for')}</div><ul>${fr(p, 'values').map((v) => html`<li>${v}</li>`)}</ul><p class="tiny faint" style="margin:8px 0 0">${L('Résumé d’après', 'Summarized from')} ${ext(p.source, fr(p, 'sourceLabel'))}</p></div>
      <div><div class="eyebrow">${L('La direction, de haut en bas', 'Leadership, top down')}</div>${ladder(p.leaders) || html`<p class="small muted">${L('Voir le site officiel du parti.', 'See the party’s official site.')}</p>`}</div>
    </div>
    ${p.groups ? html`<div><div class="eyebrow" style="margin-bottom:10px">${L('Les courants du parti', 'Groups within the party')}</div><div class="grid grid-2">${p.groups.map(groupCard)}</div></div>` : ''}
  </article>`;
}

export const parties = {
  title: () => L('Les partis et leurs valeurs', 'Parties and values'),
  render: () => html`<div class="wrap page stack-lg">
    <div><div class="eyebrow">${L('Les principaux partis et leurs valeurs', 'The main parties and values')}</div><h1>${L('Qui sont les partis, et ce qu’ils défendent', 'Who the parties are and what they stand for')}</h1>
      <p class="muted">${L(`Chaque résumé reformule le programme ou la déclaration de principes de l’organisation, traduit ici de l’anglais ; suivez les liens vers les sources (en anglais) pour le texte complet. Direction à jour en ${PARTIES_AS_OF_FR}.`, `Each summary paraphrases the organization’s own platform or statement of principles; follow the source links for the full text. Leadership as of ${PARTIES_AS_OF}.`)}</p></div>
    ${PARTIES.slice(0, 2).map(partyCard)}
    <section><div class="section-head"><h2 style="margin:0">${L('Par-delà les partis', 'Across the aisle')}</h2></div>${groupCard('psc')}</section>
    <section><div class="section-head"><h2 style="margin:0">${L('Les autres partis', 'Other parties')}</h2></div><div class="grid grid-2">${PARTIES.slice(2).map(partyCard)}</div></section>
  </div>`,
};

// Donate to the site ----------------------------------------------------------------

export const donate = {
  title: () => L('Soutenir Informed Voter', 'Support Informed Voter'),
  render: () => html`<div class="wrap page stack" style="max-width:820px">
    <div><div class="eyebrow">${L('Soutenir le site', 'Donating to the site')}</div><h1>${L('Aider Informed Voter à continuer', 'Keep Informed Voter running')}</h1><p class="muted">${L('Informed Voter est indépendant et gratuit. Les dons servent au fonctionnement du site, jamais à un candidat, un parti ou une campagne.', 'Informed Voter is independent and free to use. Donations go to running the site, not to any candidate, party or campaign.')}</p></div>
    <div class="card stack" style="text-align:center;padding:32px">
      <div class="eyebrow">PayPal</div>
      <div><a class="btn btn-primary" href="${DONATE_URL}" target="_blank" rel="noopener noreferrer">${icon.dollar()} ${L('Faire un don via PayPal', 'Donate via PayPal')} ${icon.external()}</a></div>
      <p class="small faint" style="margin:0">${L('Ouvre la page de don PayPal dans un nouvel onglet.', 'Opens PayPal’s donation page in a new tab.')}</p>
    </div>
    <div class="card stack" style="text-align:center;padding:32px">
      <div class="eyebrow">Cash App</div>
      <div class="cashtag grad-text">$KoCai</div>
      <div><a class="btn btn-primary" href="https://cash.app/$KoCai" target="_blank" rel="noopener noreferrer">${icon.dollar()} ${L('Faire un don avec Cash App', 'Donate with Cash App')} ${icon.external()}</a></div>
      <p class="small faint" style="margin:0">${L('Ouvre la page Cash App de $KoCai dans un nouvel onglet.', 'Opens Cash App’s page for $KoCai in a new tab.')}</p>
    </div>
    <p class="small faint">${L('Les dons à Informed Voter ne sont pas des dons politiques et ne sont pas déductibles des impôts.', 'Donations to Informed Voter are not political contributions and are not tax-deductible.')}</p>
  </div>`,
};

// About -----------------------------------------------------------------------------

const fmtWhen = (d) => { d = new Date(d); return lang() === 'fr' ? `${fmtDate(d)}, ${d.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' }).replace(':', ' h ')}` : `${fmtDate(d)}, ${d.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' })}`; };

// The refresh's automatic checks, plus one the browser runs itself: recompute every
// race with this page's copy of the model and compare with the refresh's result.
const ST_FR = { pass: 'réussi', warn: 'à voir', fail: 'échec', info: 'info' };
function statusCard() {
  const st = statusData();
  if (!st) {
    return html`<div class="card" id="status"><h3>${L('État des données', 'Data status')}</h3><p class="muted small" style="margin:0">${L('Aucune mise à jour n’a encore tourné sur cette copie du site. Lancez', 'No refresh has run on this copy of the site yet. Run')} <code>py scripts/refresh_all.py</code>.</p></div>`;
  }
  const mc = modelCheck;
  const checks = [...st.checks];
  if (mc) {
    checks.push({
      lang: lang(), status: mc.mismatches.length ? 'fail' : 'pass', label: L('Le modèle de cette page reproduit celui de la mise à jour', 'This page’s model reproduces the refresh'),
      detail: mc.mismatches.length ? L(`${mc.mismatches.length} élections sur ${mc.checked} diffèrent : ${mc.mismatches.slice(0, 8).map((m) => m.id).join(', ')}`, `${mc.mismatches.length} of ${mc.checked} races differ: ${mc.mismatches.slice(0, 8).map((m) => m.id).join(', ')}`) : L(`Les ${mc.checked} duels recalculés dans votre navigateur donnent tous le même résultat que le calcul en Python de la mise à jour.`, `All ${mc.checked} head-to-head races recomputed in your browser match the refresh’s Python run.`),
    });
  }
  const c = st.counts;
  const next = new Date(new Date(st.updated).getTime() + (st.nextRefreshHours || 8) * 3600e3);
  const tally = { pass: 0, warn: 0, fail: 0, info: 0 };
  checks.forEach((x) => { tally[x.status] = (tally[x.status] || 0) + 1; });
  return html`<div class="card stack" id="status">
    <div class="row between"><h3 style="margin:0">${L('État des données', 'Data status')}</h3><span class="small faint">${L(`Mis à jour ${timeAgo(st.updated)} (${fmtWhen(st.updated)}) · prochaine mise à jour prévue vers ${fmtWhen(next)}`, `Refreshed ${timeAgo(st.updated)} (${fmtWhen(st.updated)}) · next refresh due around ${fmtWhen(next)}`)}</span></div>
    <div class="grid grid-4">
      <div class="stat"><div class="eyebrow">${L('Élections', 'Races')}</div><div class="value">${c.races}</div><div class="sub">${L(`${c.senate} au Sénat · ${c.governor} de gouverneur · ${c.house} à la Chambre`, `${c.senate} Senate · ${c.governor} governor · ${c.house} House`)}</div></div>
      <div class="stat"><div class="eyebrow">${L('Sondages', 'Polls')}</div><div class="value">${fmtInt(c.polls)}</div><div class="sub">${L(`dans ${c.withPolls} élections`, `in ${c.withPolls} races`)}</div></div>
      <div class="stat"><div class="eyebrow">${L('Cotées par les analystes', 'Rated by forecasters')}</div><div class="value">${c.rated}</div><div class="sub">${L('les autres partent de l’orientation partisane', 'the rest start from partisan lean')}</div></div>
      <div class="stat"><div class="eyebrow">${L('Avec financement', 'With fundraising')}</div><div class="value">${c.withMoney}</div><div class="sub">${L(`${c.researched} avec des positions documentées`, `${c.researched} with researched positions`)}</div></div>
    </div>
    <p class="small muted" style="margin:0">${lang() === 'fr' ? `${tally.pass} vérifications réussies${tally.warn ? `, ${tally.warn} à examiner` : ''}${tally.fail ? `, ${tally.fail} en échec` : ''}. Les avertissements sont montrés tels quels : ils signalent où les chiffres du site diffèrent de ceux d’autres sources, pas des erreurs à cacher. Le détail des vérifications, écrit par le script de mise à jour, est en anglais.` : `${tally.pass} checks passed${tally.warn ? `, ${tally.warn} need a look` : ''}${tally.fail ? `, ${tally.fail} failed` : ''}. Warnings are shown as they are: they mark where this site’s numbers differ from someone else’s, not errors to hide.`}</p>
    <ul class="check-list">${checks.map((x) => html`<li lang="${x.lang || 'en'}"><span class="st ${x.status}" lang="${lang()}">${L(ST_FR[x.status] || x.status, x.status)}</span><div><b>${x.label}</b><div class="detail">${x.detail}</div></div></li>`)}</ul>
    ${st.warnings?.length ? html`<details><summary class="small">${L(`${st.warnings.length} remarque${st.warnings.length === 1 ? '' : 's'} de la dernière mise à jour (en anglais)`, `${st.warnings.length} note${st.warnings.length === 1 ? '' : 's'} from the last refresh`)}</summary><ul class="small muted" style="padding-left:18px">${st.warnings.map((w) => html`<li>${w}</li>`)}</ul></details>` : ''}
    <p class="tiny faint" style="margin:0">${L('Sources : ', 'Sources: ')}${(racesMeta()?.sources || []).map((x, i) => html`${i ? ' · ' : ''}${ext(x.url, x.title.replace('Wikipedia: ', ''))}`)} ${L('(Wikipédia en anglais, CC BY-SA, utilisée comme agrégateur ; chaque sondage renvoie à sa propre source) · FEC · Polymarket (pour comparaison seulement).', '(Wikipedia, CC BY-SA, used as an aggregator; each poll links to its own source) · FEC · Polymarket (cross-check only).')}</p>
  </div>`;
}

export const about = {
  title: () => L('À propos des données', 'About the data'),
  render: () => (lang() === 'fr' ? aboutFr() : html`<div class="wrap page stack" style="max-width:960px">
    <div><div class="eyebrow">About the data</div><h1>What’s real, and what’s a placeholder</h1></div>
    <div class="grid grid-2">
      <div class="card"><h3>${icon.check()} Real data</h3><ul class="small muted" style="padding-left:18px">
        ${realRaceCount ? html`<li><b>Every U.S. Senate, U.S. House and governor race</b>, refreshed every 8 hours: the candidates on the ballot, forecasters’ ratings (Cook, Sabato, Inside Elections and up to eight more), polls with a link to each poll’s source, and fundraising reports.</li>
        ${resultsIn() ? html`<li><b>2026 results</b>, re-read every 10 minutes from the day after the election until every race is called, and with every full refresh. A race counts as called only once Wikipedia’s national results table marks its winner. Vote counts come from California’s Secretary of State directly, and elsewhere from each race’s page, which cites the official returns; all are unofficial until each state certifies them. The final forecasts, as they stood when the polls closed, stay on each race page next to the count.</li>
        <li><b>Projections from the count</b> for races counted but not called: each blends the votes counted so far with the final forecast, allowing for how much of the vote is still out (an estimate from the state’s 2024 turnout) and for late ballots leaning differently. They are not calls. The chamber projections count every called seat as it is and each race still out by its projection, or by its final forecast where no count is posted.</li>` : ''}
        <li>${researchedCount} race${researchedCount === 1 ? '' : 's'} also ${researchedCount === 1 ? 'has' : 'have'} hand-researched bios and issue positions, each linked to the candidate’s own words or votes (tagged <span class="real-chip">Sourced</span>).</li>
        <li><b>State legislative races</b>: every seat on the ballot, who holds it, the district’s 2024 presidential margin and the November candidates where Wikipedia’s 2026 chamber page lists them, refreshed every 8 hours. They get no win odds: almost none are polled and few are rated.</li>
        ${officeCount ? html`<li><b>Statewide offices below governor</b> (attorney general, secretary of state, lieutenant governor, treasurer, auditor or comptroller): ${officeCount} races from Wikipedia’s national 2026 pages, with the candidates, who holds each office, Sabato’s Crystal Ball’s ratings and the results. ${officesResearched} of them have researched positions for every main candidate, from the States Newsroom voter guides. No win odds, for the same reason.</li>` : ''}
        ${SHOW_EARLY_VOTE ? html`<li>Early voting: ballots cast so far in each state, and in House districts where the count is complete, from the University of Florida Election Lab’s tracker (Michael McDonald).</li>` : ''}` : ''}
        <li><b><a href="#/upcoming">Upcoming elections</a></b>, 2027 to 2029: each race’s date, who holds the office and whether they can or will run again, and the declared candidates, from Wikipedia’s national pages for each office and year, read once a day. Only people who have announced a run are listed; no forecasts this early.</li>
        <li>District maps: U.S. Census Bureau 2026 TIGER/Line boundaries (120th Congress districts and 2026 state legislative districts), clipped to the shoreline; the home page’s House map joins them into one national map.</li>
        <li>Address lookup: the Census Bureau geocoder, which already reflects mid-decade redistricting.</li>
        <li>How-to-vote links: vote.gov, each state’s official election office, and NASS. Every link checked October 2026.</li>
        <li>News: headlines from 18 outlets’ public feeds, refreshed by script.</li>
        <li>Inflation: BLS price data and Federal Reserve / Freddie Mac rates via FRED.</li>
        <li>Parties: summaries of each party’s own platform, with leadership verified in October 2026.</li>
      </ul></div>
      <div class="card"><h3>${icon.info()} ${realRaceCount ? 'Missing, not invented' : html`Still demo <span class="demo-chip">Demo</span>`}</h3><ul class="small muted" style="padding-left:18px">
        ${realRaceCount ? html`<li>Every race now uses real data. What isn’t known yet is shown as missing, never made up: state legislative candidates a chamber’s page doesn’t list yet, and their positions and money, which aren’t loaded.${resultsIn() ? ' A race nobody has called yet says so rather than showing the forecast as a result.' : ''}</li>
        <li>Issue positions for races not yet researched are left blank rather than guessed, so those races can’t be matched against your views yet.</li>` : html`<li>Candidate names, bios, polls, fundraising and positions are fictional.</li>`}
      </ul><p class="small faint" style="margin:0">Everything demo carries a yellow DEMO tag. See DATA.md in the project for how real data is added.</p></div>
    </div>
    ${statusCard()}
    ${resultsIn() ? certCard() : ''}
    <div class="card"><h3>How the forecast works</h3>
      <p class="muted small">Each race starts from an expected margin. Where forecasters rate the race, their ratings set it: Safe or Solid means at least 15 points, Likely 7 to 15, Lean 3 to 7, Tilt under 3, and a toss-up within 2. The district’s partisan lean (its Cook PVI plus the national generic-ballot average${racesMeta()?.generic ? `, now D ${signed(racesMeta().generic.margin)}` : ''}) places the race inside each rating’s range, and the outlets are averaged. Races no forecaster lists as competitive start from the partisan lean alone, with a wider range of error.</p>
      <p class="muted small">Polls are averaged with more weight on recent (14-day half-life), larger and likely-voter surveys, and the average gets more say the more polling there is, up to 85%. The gap between the top two candidates, divided by a typical polling miss (wider with few polls or more time left), gives each candidate’s chance of winning. Open primaries, where every candidate shares one ballot, show the expected split between the parties instead of a winner.</p>
      <p class="muted small" style="margin:0">Chamber control simulates every race 20,000 times. Each simulation draws one national polling miss (3.5 points on the margin) shared by every race, so races move together the way they do on a real election night. Expected seats are the average across simulations, rounded to whole seats that add up to the full chamber (seats likely to go to independents who caucus with neither party are counted separately); expected gains compare them with each party’s seats today${controlData()?.senate?.current?.asOf ? ` (as of ${fmtDate(controlData().senate.current.asOf + 'T12:00:00')})` : ''}. Every refresh checks the totals add up, compares the polling averages with published ones, compares expected seats with each forecaster’s own count, and compares control odds with the betting market. The results are in Data status above.</p>
    </div>
    <div class="card"><h3>Your privacy</h3><p class="muted small">There are no accounts. Your views, address, stars, likes and picture are stored only in this browser’s local storage. Your address is sent only to the U.S. Census Bureau to find your districts. Clearing your browser data removes all of it.</p>
      <p class="muted small">Help tickets go to ${SUPPORT_EMAIL} (Gmail), with your email address only if you give one, and are used only to answer you.${MAIL_SERVICE_URL ? ` If you sign up for email reminders, your address, the election and the dates you chose are kept in the site’s Google account (a Google Sheets file) and used only to send those reminders, from ${REMINDER_FROM}. Nothing is sent until you confirm by email, and the address is deleted when you unsubscribe (there’s a link in every email), once the election is over, or after 7 days if you never confirm. Gmail keeps a copy of each email the site sends; that copy goes to the trash right away, and Gmail deletes it for good 30 days later.` : ''} To see, correct or delete what the site holds about you, write to ${SUPPORT_EMAIL}. If you’re in the EU or the UK, you can also complain to your data protection authority.</p>
      <p class="muted small" style="margin:0">Ads are served by Google AdSense. Google and its partners use cookies and receive your IP address and the address of the page you’re on to choose and measure ads, including ads based on your visits to other sites. Informed Voter doesn’t send them your views or your address. You can turn off personalized ads in ${ext('https://adssettings.google.com/', 'Google’s Ads Settings')} and read ${ext('https://policies.google.com/technologies/partner-sites', 'how Google uses information from sites that show its ads')}.</p></div>
  </div>`),
};

// The same page in French: a translation of the English one above; change both together.
// Which states have certified their 2026 results (data/certified.json, kept by hand in
// scripts/research/certified_2026.py), and what the strip at the top waits for.
function certCard() {
  const cf = certifiedList();
  const states = cf?.states || {};
  const listed = Object.entries(states).sort((a, b) => a[1].date.localeCompare(b[1].date) || stateName(a[0]).localeCompare(stateName(b[0])));
  const missing = STATES.filter((s) => !states[s.abbr]).map((s) => stateName(s.abbr)).sort((a, b) => a.localeCompare(b, L('fr', 'en')));
  return html`<div class="card stack-sm" id="certification">
    <h3 style="margin:0">${L('Certification des résultats', 'Certification')}</h3>
    <p class="small muted" style="margin:0">${allCertified()
      ? L('Chaque État et le district de Columbia ont certifié leurs résultats : le bandeau en haut de chaque page les dit officiels.', 'Every state and D.C. has certified its results, so the strip at the top of each page calls them official.')
      : L(`Les résultats restent non officiels jusqu’à leur certification par chaque État, selon son propre calendrier, de la mi-novembre à la fin décembre. Le bandeau en haut de chaque page dira « officiels » quand les 50 États et le district de Columbia auront certifié et que chaque élection sera décidée. Un État n’est listé ici qu’après l’annonce de sa certification par son propre service électoral (ou un article de presse sur le vote), vérifiée à la main : d’autres ont peut-être déjà certifié.${cf?.checked ? ` Dernière vérification : ${fmtDate(cf.checked)}.` : ''}`,
        `Results stay unofficial until each state certifies them, on its own schedule, from mid-November to late December. The strip at the top of each page will say “official” once all 50 states and D.C. have certified and every race is decided. A state is listed here only after its own election office announced its certification (or a news report of the vote did), checked by hand, so others may already have certified.${cf?.checked ? ` Last checked ${fmtDate(cf.checked)}.` : ''}`)}</p>
    ${listed.length ? html`<div class="small"><b>${L(`Certifiés à ce jour (${listed.length} sur ${STATES.length})`, `Certified so far (${listed.length} of ${STATES.length})`)}</b>
      <ul class="small muted" style="padding-left:18px;margin:6px 0 0">${listed.map(([st, c]) => {
        const out = certExceptions(c);
        return html`<li>${stateName(st)}, ${fmtDate(c.date)} (<a href="${c.source.url}" target="_blank" rel="noopener noreferrer">${c.source.title.split(':')[0]}</a>)${out.length ? html`${L(', sauf : ', ', except ')}${out.map((x, i) => html`${i ? L(' ; ', '; ') : ''}${x}`)}` : ''}</li>`;
      })}</ul></div>` : ''}
    ${missing.length ? html`<p class="small faint" style="margin:0">${L(`Pas encore listés (${missing.length}) : `, `Not listed yet (${missing.length}): `)}${missing.join(L(', ', ', '))}.</p>` : ''}
  </div>`;
}

function aboutFr() {
  const g = racesMeta()?.generic;
  const asOf = controlData()?.senate?.current?.asOf;
  return html`<div class="wrap page stack" style="max-width:960px">
    <div><div class="eyebrow">À propos des données</div><h1>Ce qui est réel, et ce qui ne l’est pas encore</h1></div>
    <div class="grid grid-2">
      <div class="card"><h3>${icon.check()} Données réelles</h3><ul class="small muted" style="padding-left:18px">
        ${realRaceCount ? html`<li><b>Toutes les élections au Sénat, à la Chambre des représentants et aux postes de gouverneur</b>, mises à jour toutes les 8 heures : les candidatures sur les bulletins, les cotes des analystes (Cook, Sabato, Inside Elections et jusqu’à huit autres), les sondages avec un lien vers la source de chacun, et les déclarations de financement.</li>
        ${resultsIn() ? html`<li><b>Les résultats de 2026</b>, relus toutes les 10 minutes depuis le lendemain de l’élection jusqu’à ce que chaque élection soit attribuée, et à chaque mise à jour complète. Une élection ne compte comme attribuée qu’une fois son vainqueur coché dans le tableau national des résultats de Wikipédia. Les décomptes viennent directement du secrétariat d’État de Californie, et ailleurs de la page de chaque élection, qui cite les résultats officiels ; tous restent non officiels jusqu’à leur certification par chaque État. Les dernières prévisions, telles qu’elles étaient à la fermeture des bureaux de vote, restent sur la page de chaque élection à côté du décompte.</li>
        <li><b>Des projections d’après le décompte</b> pour les élections dépouillées mais pas encore attribuées : chacune combine les voix déjà comptées et la dernière prévision, en tenant compte de la part des voix encore à compter (estimée d’après la participation de 2024 dans l’État) et des bulletins tardifs qui peuvent pencher autrement. Ce ne sont pas des attributions. Les projections par chambre comptent chaque siège attribué tel quel, et chaque élection en cours selon sa projection, ou sa dernière prévision là où aucun décompte n’est publié.</li>` : ''}
        <li>${researchedCount} élection${researchedCount === 1 ? '' : 's'} ${researchedCount === 1 ? 'a' : 'ont'} aussi des biographies et des positions documentées à la main, chacune liée aux propres mots ou votes de la personne candidate (marquées <span class="real-chip">${L('Sourcé', 'Sourced')}</span>).</li>
        <li><b>Les élections aux assemblées des États</b> : chaque siège en jeu, qui l’occupe, l’écart de la présidentielle de 2024 dans la circonscription et les candidatures de novembre là où la page 2026 de la chambre sur Wikipédia les liste, mis à jour toutes les 8 heures. Aucune probabilité de victoire : presque aucune n’est sondée et peu sont cotées.</li>
        ${officeCount ? html`<li><b>Les postes de l’État sous le gouverneur</b> (procureur général, secrétaire d’État, lieutenant-gouverneur, trésorier, auditeur ou contrôleur) : ${officeCount} élections tirées des pages nationales 2026 de Wikipédia, avec les candidatures, les titulaires, les cotes du Crystal Ball de Sabato et les résultats. ${officesResearched} d’entre elles ont des positions documentées pour chaque candidature principale, tirées des guides électoraux de States Newsroom. Pas de probabilités non plus, pour la même raison.</li>` : ''}
        ${SHOW_EARLY_VOTE ? html`<li>Le vote anticipé : les bulletins déjà déposés dans chaque État, et dans les circonscriptions de la Chambre où le décompte est complet, d’après le suivi de l’Election Lab de l’université de Floride (Michael McDonald).</li>` : ''}` : ''}
        <li><b><a href="#/upcoming">Les prochaines élections</a></b>, de 2027 à 2029 : la date de chaque élection, qui occupe le poste et si cette personne peut ou veut se représenter, et les candidatures déclarées, tirées des pages nationales de Wikipédia pour chaque poste et chaque année, lues une fois par jour. Seules les personnes qui ont annoncé leur candidature sont listées ; pas de prévisions si tôt.</li>
        <li>Les cartes des circonscriptions : les limites TIGER/Line 2026 du Bureau du recensement (circonscriptions du 120e Congrès et circonscriptions 2026 des assemblées des États), découpées au trait de côte ; la carte de la Chambre de l’accueil les réunit en une carte nationale.</li>
        <li>La recherche d’adresse : le géocodeur du Bureau du recensement, qui tient déjà compte des redécoupages en cours de décennie.</li>
        <li>Les liens pour voter : vote.gov, le bureau électoral officiel de chaque État et la NASS. Chaque lien vérifié en octobre 2026.</li>
        <li>Les actualités : les titres des flux publics de 18 médias, récupérés par script.</li>
        <li>L’inflation : les prix du BLS et les taux de la Réserve fédérale et de Freddie Mac, via FRED.</li>
        <li>Les partis : des résumés du programme de chaque parti, avec une direction vérifiée en octobre 2026.</li>
      </ul></div>
      <div class="card"><h3>${icon.info()} ${realRaceCount ? 'Manquant, jamais inventé' : html`Encore en démonstration <span class="demo-chip">Démo</span>`}</h3><ul class="small muted" style="padding-left:18px">
        ${realRaceCount ? html`<li>Toutes les élections utilisent désormais de vraies données. Ce qui n’est pas encore connu est montré comme manquant, jamais inventé : les candidatures aux assemblées des États qu’une page de chambre ne liste pas encore, et leurs positions et leur financement, qui ne sont pas chargés.${resultsIn() ? ' Une élection que personne n’a encore attribuée le dit, au lieu de montrer la prévision comme un résultat.' : ''}</li>
        <li>Les positions des élections pas encore documentées restent vides plutôt que devinées : ces élections ne peuvent donc pas encore être comparées à vos opinions.</li>` : html`<li>Les noms, biographies, sondages, financements et positions des candidatures sont fictifs.</li>`}
      </ul><p class="small faint" style="margin:0">Tout ce qui relève de la démonstration porte une étiquette jaune DÉMO. Le fichier DATA.md du projet explique comment ajouter de vraies données.</p></div>
    </div>
    ${statusCard()}
    ${resultsIn() ? certCard() : ''}
    <div class="card"><h3>Comment fonctionne la prévision</h3>
      <p class="muted small">Chaque élection part d’un écart attendu. Là où des analystes cotent l’élection, leurs cotes le fixent : « Safe » ou « Solid » veut dire au moins 15 points, « Likely » de 7 à 15, « Lean » de 3 à 7, « Tilt » moins de 3, et « Toss-up » (indécis) à 2 points près. L’orientation partisane de la circonscription (son Cook PVI plus la moyenne nationale du vote générique${g ? `, aujourd’hui D ${signed(g.margin)}` : ''}) place l’élection dans la fourchette de chaque cote, et l’on fait la moyenne des analystes. Les élections qu’aucun analyste ne juge disputées partent de la seule orientation partisane, avec une marge d’erreur plus large.</p>
      <p class="muted small">Les sondages sont moyennés en donnant plus de poids aux plus récents (demi-vie de 14 jours), aux plus grands et à ceux auprès des électeurs probables, et la moyenne pèse d’autant plus qu’il y a de sondages, jusqu’à 85 %. L’écart entre les deux premiers, divisé par l’erreur typique des sondages (plus large avec peu de sondages ou plus de temps restant), donne à chacun ses chances de gagner. Les primaires ouvertes, où toutes les candidatures partagent un seul bulletin, montrent la répartition attendue entre les partis plutôt qu’un vainqueur.</p>
      <p class="muted small" style="margin:0">Le contrôle des chambres simule chaque élection 20 000 fois. Chaque simulation tire une seule erreur nationale des sondages (3,5 points sur l’écart) commune à toutes les élections, pour qu’elles bougent ensemble comme lors d’une vraie soirée électorale. Les sièges attendus sont la moyenne des simulations, arrondie en sièges entiers qui font le total de la chambre (les sièges promis à des personnes indépendantes qui ne siègent avec aucun des deux partis sont comptés à part) ; les gains attendus les comparent aux sièges actuels de chaque parti${asOf ? ` (au ${fmtDate(asOf + 'T12:00:00')})` : ''}. Chaque mise à jour vérifie que les totaux tombent juste, compare les moyennes de sondages à celles publiées ailleurs, les sièges attendus au décompte de chaque analyste, et les chances de contrôle au marché de paris. Les résultats sont dans « État des données » ci-dessus.</p>
    </div>
    <div class="card"><h3>Votre vie privée</h3><p class="muted small">Il n’y a pas de compte. Vos opinions, votre adresse, les élections que vous suivez, vos favoris et votre photo restent dans le stockage local de ce navigateur. Votre adresse n’est envoyée qu’au Bureau du recensement des États-Unis, pour trouver vos circonscriptions. Effacer les données du navigateur supprime tout.</p>
      <p class="muted small">Les tickets d’aide arrivent à ${SUPPORT_EMAIL} (Gmail), avec votre adresse e-mail seulement si vous la donnez, et ne servent qu’à vous répondre.${MAIL_SERVICE_URL ? ` Si vous vous inscrivez aux rappels par e-mail, votre adresse, l’élection et les dates choisies sont gardées dans le compte Google du site (une feuille Google Sheets) et ne servent qu’à vous envoyer ces rappels, depuis ${REMINDER_FROM}. Rien n’est envoyé avant votre confirmation par e-mail, et l’adresse est effacée quand vous vous désinscrivez (un lien figure dans chaque e-mail), une fois l’élection passée, ou au bout de 7 jours sans confirmation. Gmail garde une copie de chaque e-mail envoyé par le site ; cette copie part aussitôt à la corbeille, et Gmail l’efface définitivement 30 jours plus tard.` : ''} Pour consulter, corriger ou effacer ce que le site garde sur vous, écrivez à ${SUPPORT_EMAIL}. Si vous êtes dans l’Union européenne ou au Royaume-Uni, vous pouvez aussi adresser une réclamation à votre autorité de protection des données.</p>
      <p class="muted small" style="margin:0">Les publicités sont diffusées par Google AdSense. Google et ses partenaires utilisent des cookies et reçoivent votre adresse IP et l’adresse de la page consultée pour choisir et mesurer les annonces, y compris d’après vos visites sur d’autres sites. Informed Voter ne leur envoie ni vos opinions ni votre adresse. Vous pouvez désactiver les annonces personnalisées dans les ${ext('https://adssettings.google.com/', 'paramètres des annonces de Google')} et lire ${ext('https://policies.google.com/technologies/partner-sites?hl=fr', 'comment Google utilise les données des sites qui affichent ses annonces')}.</p></div>
  </div>`;
}
