// A region (its departments and largest cities), a department, and a city: each
// shows the elections that apply there and the presidential race.

import { html } from '../../util.js';
import { icon } from '../../icons.js';
import { L } from '../../i18n.js';
import { loadPres, loadRegions, loadDepartements, loadCities, loadCalendar, mainCandidates, fmtInt, fmtDay, fmtPctFr, fetchCommune } from '../data.js';
import { candPhoto, partyChip } from '../components.js';
import { drawFrance } from '../map.js';
import { upcomingFor, electionTile, specialNote, electionName } from '../elections.js';
import { cityTip } from './home.js';

function raceCard(pres, { where = '' } = {}) {
  if (!pres) return '';
  const rows = mainCandidates(pres, 4).slice(0, 8);
  return html`<section class="card stack">
    <div class="row between"><div><div class="eyebrow">${L('L’élection qui s’y joue', 'The race here')} · ${fmtDay(pres.rounds.r1)}</div>
      <h2 style="margin:4px 0 0">${L('Présidentielle 2027', '2027 presidential election')}</h2></div>
      <a class="btn btn-sm" href="#/fr/presidentielle">${L('Sondages des deux tours', 'Polls for both rounds')} ${icon.chevronRight()}</a></div>
    <p class="small muted" style="margin:0">${L(
      `C’est une élection nationale : ${where ? `à ${where}, ` : ''}on vote pour les mêmes candidats que partout en France. Les pourcentages sont la moyenne des sondages nationaux ; il n’y a pas de sondage par ville.`,
      `It’s a national election: ${where ? `in ${where}, ` : ''}voters choose among the same candidates as everywhere in France. Percentages are the national poll average; there are no polls by city.`,
    )}</p>
    <div class="fr-faces">${rows.map((c) => html`<div class="fr-face">${candPhoto(c, { size: 84 })}<b>${c.name}</b><span class="tiny">${partyChip(c)}</span><span class="num">${fmtPctFr(c.avg.avg)}</span></div>`)}</div>
  </section>`;
}

function electionsCard(cal, place, title) {
  if (!cal) return '';
  const list = upcomingFor(cal, place);
  const notes = list.map((e) => [e, specialNote(e, place)]).filter(([, n]) => n);
  return html`<section class="card stack">
    <div><div class="eyebrow">${title}</div><h2 style="margin:4px 0 0">${L('Les prochaines élections ici', 'The next elections here')}</h2></div>
    <div class="fr-next">${list.map((e) => electionTile(e, { href: e.href || `#/fr/calendrier?e=${e.id}` }))}</div>
    ${notes.map(([e, n]) => html`<p class="small muted" style="margin:0">${icon.info()} <b>${electionName(e)}</b> : ${n}</p>`)}
  </section>`;
}

export const regionView = {
  title: () => L('Région', 'Region'),
  async render(ctx) {
    const code = ctx.params[0];
    const [regs, deps, cities, pres, cal] = await Promise.all([loadRegions(), loadDepartements(), loadCities(), loadPres(), loadCalendar()]);
    const reg = regs?.features.find((f) => f.id === code);
    if (!reg) return html`<div class="wrap page"><div class="empty"><h3>${L('Région introuvable', 'Region not found')}</h3><a class="btn" href="#/fr">${L('Retour à la carte', 'Back to the map')}</a></div></div>`;
    document.title = `${reg.properties.name} · Informed Voter`;
    const myDeps = deps.features.filter((f) => f.properties.reg === code).sort((a, b) => a.properties.name.localeCompare(b.properties.name, 'fr'));
    const myCities = (cities?.cities || []).filter((c) => c.reg === code);
    return html`<div class="wrap page stack-lg">
      <nav class="crumbs"><a href="#/fr">France</a><span>/</span><span>${reg.properties.name}</span></nav>
      <div><div class="eyebrow">${reg.properties.overseas ? L('Région d’outre-mer', 'Overseas region') : L('Région', 'Region')}</div><h1 style="margin:6px 0 0">${reg.properties.name}</h1>
        <p class="muted" style="margin:6px 0 0">${L(`${myDeps.length} département${myDeps.length > 1 ? 's' : ''}`, `${myDeps.length} department${myDeps.length > 1 ? 's' : ''}`)} · ${L('cliquez sur un département ou une ville', 'click a department or a city')}</p></div>
      <div class="grid grid-2" style="align-items:start">
        <div class="card" style="padding:10px"><div id="fr-map" class="map-host"></div></div>
        <div class="stack">
          <div class="card"><h3>${L('Départements', 'Departments')}</h3><div class="fr-links">${myDeps.map((f) => html`<a href="#/fr/departement/${f.id}">${f.properties.name} <span class="faint">(${f.id})</span></a>`)}</div></div>
          ${myCities.length ? html`<div class="card"><h3>${L('Grandes villes', 'Largest cities')}</h3><div class="fr-links">${myCities.map((c) => html`<a href="#/fr/ville/${c.code}">${c.name} <span class="faint">${fmtInt(c.pop)} ${L('hab.', 'res.')}</span></a>`)}</div></div>` : ''}
        </div>
      </div>
      ${electionsCard(cal, { reg: code }, reg.properties.name)}
      ${raceCard(pres, { where: '' })}
    </div>`;
  },
  async mount(root, ctx) {
    const code = ctx.params[0];
    const [deps, cities] = await Promise.all([loadDepartements(), loadCities()]);
    const host = root.querySelector('#fr-map');
    if (!host || !deps) return;
    const ids = deps.features.filter((f) => f.properties.reg === code).map((f) => f.id);
    drawFrance(host, deps, {
      focusIds: ids, ariaLabel: L('Carte des départements de la région', 'Map of the region’s departments'),
      cities: (cities?.cities || []).filter((c) => c.reg === code), showCityLabels: () => true,
      labelFor: (f) => f.id, maxHeight: 520,
      tooltipFor: (f) => html`<div class="tt-title">${f.properties.name} (${f.id})</div><div class="tt-sub">${L('Ouvrir le département', 'Open the department')}</div>`,
      cityTip,
      onSelect: (f) => { location.hash = `#/fr/departement/${f.id}`; },
      onCity: (c) => { location.hash = `#/fr/ville/${c.code}`; },
    });
  },
};

export const departementView = {
  title: () => L('Département', 'Department'),
  async render(ctx) {
    const code = ctx.params[0].toUpperCase();
    const [regs, deps, cities, pres, cal] = await Promise.all([loadRegions(), loadDepartements(), loadCities(), loadPres(), loadCalendar()]);
    const dep = deps?.features.find((f) => f.id === code);
    if (!dep) return html`<div class="wrap page"><div class="empty"><h3>${L('Département introuvable', 'Department not found')}</h3><a class="btn" href="#/fr">${L('Retour à la carte', 'Back to the map')}</a></div></div>`;
    document.title = `${dep.properties.name} · Informed Voter`;
    const reg = regs.features.find((f) => f.id === dep.properties.reg);
    const myCities = (cities?.cities || []).filter((c) => c.dep === code);
    return html`<div class="wrap page stack-lg">
      <nav class="crumbs"><a href="#/fr">France</a><span>/</span><a href="#/fr/region/${reg.id}">${reg.properties.name}</a><span>/</span><span>${dep.properties.name}</span></nav>
      <div><div class="eyebrow">${L('Département', 'Department')} ${code}</div><h1 style="margin:6px 0 0">${dep.properties.name}</h1>
        <p class="muted" style="margin:6px 0 0">${L('Région', 'Region')} : <a href="#/fr/region/${reg.id}">${reg.properties.name}</a></p></div>
      <div class="grid grid-2" style="align-items:start">
        <div class="card" style="padding:10px"><div id="fr-map" class="map-host"></div></div>
        <div class="stack">
          ${myCities.length ? html`<div class="card"><h3>${L('Grandes villes', 'Largest cities')}</h3><div class="fr-links">${myCities.map((c) => html`<a href="#/fr/ville/${c.code}">${c.name} <span class="faint">${fmtInt(c.pop)} ${L('hab.', 'res.')}</span></a>`)}</div></div>` : ''}
          <div class="card"><h3>${L('Votre commune ?', 'Your commune?')}</h3><p class="small muted" style="margin:0 0 10px">${L('Ajoutez votre adresse pour voir les élections de votre commune, avec les dates.', 'Add your address to see your commune’s elections and dates.')}</p><a class="btn btn-sm" href="#/fr/profil?onglet=localisation">${icon.pin()} ${L('Ajouter mon adresse', 'Add my address')}</a></div>
        </div>
      </div>
      ${electionsCard(cal, { dep: code, reg: reg.id }, dep.properties.name)}
      ${raceCard(pres)}
    </div>`;
  },
  async mount(root, ctx) {
    const code = ctx.params[0].toUpperCase();
    const [deps, cities] = await Promise.all([loadDepartements(), loadCities()]);
    const host = root.querySelector('#fr-map');
    const dep = deps?.features.find((f) => f.id === code);
    if (!host || !dep) return;
    const ids = deps.features.filter((f) => f.properties.reg === dep.properties.reg).map((f) => f.id);
    drawFrance(host, deps, {
      focusIds: ids, selectedId: code, ariaLabel: L('Carte de la région', 'Map of the region'),
      fillFor: (f) => (f.id === code ? 'var(--surface-2)' : 'var(--surface-3)'),
      cities: (cities?.cities || []).filter((c) => c.reg === dep.properties.reg), showCityLabels: () => true,
      labelFor: (f) => f.id, maxHeight: 520,
      tooltipFor: (f) => html`<div class="tt-title">${f.properties.name} (${f.id})</div>`,
      cityTip,
      onSelect: (f) => { location.hash = `#/fr/departement/${f.id}`; },
      onCity: (c) => { location.hash = `#/fr/ville/${c.code}`; },
    });
  },
};

export const villeView = {
  title: () => L('Ville', 'City'),
  async render(ctx) {
    const code = ctx.params[0].toUpperCase();
    const [regs, deps, cities, pres, cal] = await Promise.all([loadRegions(), loadDepartements(), loadCities(), loadPres(), loadCalendar()]);
    // The largest cities ship with the site; any other commune comes from geo.api.gouv.fr.
    const city = (cities?.cities || []).find((c) => c.code === code) || await fetchCommune(code);
    if (!city) return html`<div class="wrap page"><div class="empty"><h3>${L('Commune introuvable', 'Commune not found')}</h3><a class="btn" href="#/fr">${L('Retour à la carte', 'Back to the map')}</a></div></div>`;
    document.title = `${city.name} · Informed Voter`;
    const dep = deps.features.find((f) => f.id === city.dep);
    const reg = regs.features.find((f) => f.id === city.reg);
    return html`<div class="wrap page stack-lg">
      <nav class="crumbs"><a href="#/fr">France</a><span>/</span>${reg ? html`<a href="#/fr/region/${reg.id}">${reg.properties.name}</a><span>/</span>` : ''}${dep ? html`<a href="#/fr/departement/${dep.id}">${dep.properties.name}</a><span>/</span>` : ''}<span>${city.name}</span></nav>
      <div><div class="eyebrow">${L('Commune', 'Commune')}${dep ? ` · ${dep.properties.name} (${dep.id})` : ''}</div><h1 style="margin:6px 0 0">${city.name}</h1>
        ${city.pop ? html`<p class="muted" style="margin:6px 0 0">${fmtInt(city.pop)} ${L('habitants (INSEE)', 'residents (INSEE)')}</p>` : ''}</div>
      ${raceCard(pres, { where: city.name })}
      ${electionsCard(cal, { dep: city.dep, reg: city.reg, commune: city.code }, city.name)}
    </div>`;
  },
};
