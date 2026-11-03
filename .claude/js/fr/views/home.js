// The France section's homepage: the countdown to the presidential election, France
// by region or department with its largest cities, the first-round poll average,
// the second-round match-ups and the next elections (personal once an address is saved).

import { html, raw } from '../../util.js';
import { icon } from '../../icons.js';
import { L } from '../../i18n.js';
import { frStore } from '../store.js';
import { loadPres, loadRegions, loadDepartements, loadCities, loadCalendar, mainCandidates, isCurrentDuel, fmtDay, fmtInt } from '../data.js';
import { countdown, averageBars, duelCard } from '../components.js';
import { drawFrance } from '../map.js';
import { upcomingFor, electionTile } from '../elections.js';
import { MIN_COMPARED } from '../match.js';
import { QUIZ_URL } from '../compare.js';

export const INSET_NAMES = { 971: 'Guadeloupe', 972: 'Martinique', 973: 'Guyane', 974: 'La Réunion', 976: 'Mayotte' };

export function cityTip(c) {
  return html`<div class="tt-title">${c.name}</div><div class="tt-sub">${fmtInt(c.pop)} ${L('habitants', 'residents')}</div><div class="tt-sub">${L('Voir l’élection dans cette ville', 'See the race in this city')}</div>`;
}

export const frHome = {
  title: () => L('France · présidentielle 2027', 'France · 2027 presidential election'),
  async render(ctx) {
    const [pres, cal] = await Promise.all([loadPres(), loadCalendar()]);
    const layer = ctx.query.carte === 'departements' ? 'departements' : 'regions';
    const ad = frStore.get().address;
    const mine = cal ? upcomingFor(cal, ad).slice(0, 4) : [];
    const rows = pres ? mainCandidates(pres, 2) : [];
    const duels = pres ? pres.r2.filter((d) => isCurrentDuel(d, pres)).slice(0, 4) : [];
    const answered = frStore.answered();
    return html`<div class="wrap page stack-lg">
      <section class="fr-hero card">
        <div>
          <div class="eyebrow" style="color:var(--brand-2)">${L('Élection présidentielle 2027', '2027 presidential election')}</div>
          <h1 style="margin:6px 0 8px">${L('Qui sera le prochain président de la République ?', 'Who will be France’s next president?')}</h1>
          <p class="muted" style="margin:0">${L(
            'Emmanuel Macron ne peut pas se représenter. Si aucun candidat n’obtient la majorité absolue au premier tour, les deux premiers s’affrontent au second tour deux semaines plus tard.',
            'Emmanuel Macron cannot run again. If no candidate wins an outright majority in the first round, the top two meet in a runoff two weeks later.',
          )}</p>
          <div class="row" style="margin-top:14px"><a class="btn btn-primary" href="#/fr/presidentielle">${icon.ballot()} ${L('Sondages des deux tours', 'Polls for both rounds')}</a><a class="btn" href="#/fr/profil/opinions">${icon.check()} ${L('Mes opinions : 144 questions', 'My views: 144 questions')}</a></div>
        </div>
        ${pres ? html`<div class="fr-counts">${countdown(pres.rounds.r1, { label: L('Premier tour', 'First round') })}${countdown(pres.rounds.r2, { label: L('Second tour', 'Second round') })}</div>` : ''}
      </section>

      <section class="fr-start">
        <button type="button" class="btn btn-primary fr-start-btn" aria-expanded="false" aria-controls="fr-start-choices">${icon.ballot()} ${L('Préparer mon vote', 'Get ready to vote')} ${icon.chevronDown()}</button>
        <div class="fr-start-choices" id="fr-start-choices" hidden>
          <a class="card fr-choice" href="#/fr/elections">${icon.calendar()}<span><b>${L('Cliquez ici pour voir mes élections', 'Click here to view my elections')}</b><span class="small muted">${ad
            ? L(`Les prochaines élections à ${ad.city}, celles que vous suivez et vos rappels.`, `The next elections in ${ad.city}, the ones you follow and your reminders.`)
            : L('Les prochaines élections là où vous votez, d’après votre adresse.', 'The next elections where you vote, from your address.')}</span></span>${icon.chevronRight()}</a>
          <a class="card fr-choice" href="${answered >= MIN_COMPARED ? '#/fr/elections/comparer' : QUIZ_URL}">${icon.user()}<span><b>${L('Cliquez ici pour m’aider à trouver le candidat qui me correspond', 'Click here to help find the candidate right for me')}</b><span class="small muted">${answered >= MIN_COMPARED
            ? L(`Les candidats déclarés, classés d’après vos ${answered} réponses à Mes opinions.`, `The declared candidates, ranked by your ${answered} answers in My views.`)
            : L('Répondez à quelques-unes des 144 questions de Mes opinions, puis comparez-les aux positions sourcées des candidats déclarés.', 'Answer some of the 144 questions in My views, then compare them with the declared candidates’ sourced positions.')}</span></span>${icon.chevronRight()}</a>
        </div>
      </section>

      <section>
        <div class="section-head"><div><h2 style="margin:0">${L('La France, région par région', 'France, region by region')}</h2>
          <p class="muted small" style="margin:4px 0 0">${L('Cliquez sur une région ou un département pour l’ouvrir, ou sur une grande ville pour voir l’élection qui s’y joue.', 'Click a region or department to open it, or a large city to see the race there.')}</p></div>
          <nav class="seg" aria-label="${L('Découpage de la carte', 'Map layer')}"><a href="#/fr" ${raw(layer === 'regions' ? 'aria-current="page"' : '')}>${L('Régions', 'Regions')}</a><a href="#/fr?carte=departements" ${raw(layer === 'departements' ? 'aria-current="page"' : '')}>${L('Départements', 'Departments')}</a></nav>
        </div>
        <div class="card" style="padding:10px"><div id="fr-map" class="map-host"></div></div>
        <p class="tiny faint" style="margin-top:6px">${L('Limites : IGN, ADMIN EXPRESS COG CARTO (Licence Ouverte 2.0). Les départements d’outre-mer sont représentés en encarts, à une échelle différente.', 'Boundaries: IGN, ADMIN EXPRESS COG CARTO (Licence Ouverte 2.0). Overseas departments are shown in insets at a different scale.')}</p>
      </section>

      ${pres ? html`<section class="grid grid-2" style="align-items:start">
        <div class="card stack">
          <div><div class="eyebrow">${L('Premier tour', 'First round')}</div><h2 style="margin:4px 0 0">${L('La moyenne des sondages', 'The poll average')}</h2>
          <p class="small muted" style="margin:4px 0 0">${L(
            `${pres.r1.average.polls} sondages publiés du ${fmtDay(pres.r1.average.from, { year: false })} au ${fmtDay(pres.r1.average.to)}. Chaque sondage compte une fois ; le trait clair montre l’écart entre sondages.`,
            `${pres.r1.average.polls} polls published ${fmtDay(pres.r1.average.from, { year: false })} to ${fmtDay(pres.r1.average.to)}. Each poll counts once; the light band shows the spread between polls.`,
          )}</p></div>
          ${averageBars(pres, rows)}
          <a class="btn btn-sm" href="#/fr/presidentielle">${L('Tous les sondages et hypothèses', 'Every poll and line-up')} ${icon.chevronRight()}</a>
        </div>
        <div class="card stack">
          <div><div class="eyebrow">${L('Second tour', 'Second round')}</div><h2 style="margin:4px 0 0">${L('Les duels testés', 'The match-ups tested')}</h2>
          <p class="small muted" style="margin:4px 0 0">${L('Les sondeurs testent plusieurs seconds tours possibles. Ce ne sont pas des prévisions : le second tour dépendra du premier.', 'Pollsters test several possible runoffs. These aren’t forecasts: the runoff depends on the first round.')}</p></div>
          ${duels.map((d) => duelCard(d, pres))}
          <a class="btn btn-sm" href="#/fr/presidentielle?tour=2">${L('Tous les duels', 'Every match-up')} ${icon.chevronRight()}</a>
        </div>
      </section>` : html`<div class="notice warn">${icon.info()}<div>${L('Les données de la présidentielle ne sont pas encore chargées. Lancez py scripts/fr/update_presidentielle.py.', 'The presidential data isn’t loaded yet. Run py scripts/fr/update_presidentielle.py.')}</div></div>`}

      ${cal ? html`<section class="card stack">
        <div class="row between"><div><div class="eyebrow">${ad ? ad.city : L('Partout en France', 'Across France')}</div><h2 style="margin:4px 0 0">${L('Les prochaines élections', 'The next elections')}</h2></div>
          ${ad ? html`<a class="btn btn-sm btn-ghost" href="#/fr/elections">${L('Mes élections', 'My elections')}</a>` : html`<a class="btn btn-sm" href="#/fr/profil?onglet=localisation">${icon.pin()} ${L('Ajouter mon adresse', 'Add my address')}</a>`}</div>
        <div class="fr-next">${mine.map((e) => electionTile(e, { href: `#/fr/calendrier?e=${e.id}` }))}</div>
        <a class="small" href="#/fr/calendrier">${L('Tout le calendrier électoral', 'The full election calendar')}</a>
      </section>` : ''}
    </div>`;
  },
  async mount(root, ctx) {
    // "Préparer mon vote" opens its two choices under the hero.
    const start = root.querySelector('.fr-start-btn');
    start?.addEventListener('click', () => {
      const panel = root.querySelector('#fr-start-choices');
      panel.hidden = !panel.hidden;
      start.setAttribute('aria-expanded', String(!panel.hidden));
    });
    const host = root.querySelector('#fr-map');
    if (!host) return;
    const deps = ctx.query.carte === 'departements';
    const [fc, cities] = await Promise.all([deps ? loadDepartements() : loadRegions(), loadCities()]);
    if (!fc) { host.innerHTML = `<p class="muted">${L('La carte n’a pas pu se charger.', 'The map couldn’t load.')}</p>`; return; }
    drawFrance(host, fc, {
      ariaLabel: deps ? L('Carte des départements', 'Map of the departments') : L('Carte des régions', 'Map of the regions'),
      cities: cities?.cities || [],
      insetNames: INSET_NAMES,
      labelFor: deps ? (f) => f.id : null,
      regionLabel: (f) => (deps ? `${f.properties.name} (${f.id})` : f.properties.name),
      tooltipFor: (f) => html`<div class="tt-title">${f.properties.name}${deps ? ` (${f.id})` : ''}</div><div class="tt-sub">${deps ? L('Ouvrir le département', 'Open the department') : L(`${f.properties.deps.length} départements · ouvrir la région`, `${f.properties.deps.length} departments · open the region`)}</div>`,
      cityTip,
      onSelect: (f) => { location.hash = deps ? `#/fr/departement/${f.id}` : `#/fr/region/${f.id}`; },
      onCity: (c) => { location.hash = `#/fr/ville/${c.code}`; },
    });
  },
};
