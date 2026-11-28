import { html } from '../util.js';
import { icon } from '../icons.js';
import { stateName } from '../data/states.js';
import { L } from '../i18n.js';
import { ensureRace, raceTitle } from '../data/world.js';
import { raceFull, mountRaceTabs, awaitingResult } from '../components/race.js';
import { howToVote } from '../components/vote.js';

export const racePage = {
  live: true, // redrawn when new counts arrive (main.js)
  title: () => L('Prévision de l’élection', 'Race forecast'),
  async render(ctx) {
    const race = await ensureRace(decodeURIComponent(ctx.params[0]));
    if (!race) {
      return html`<div class="wrap page"><div class="empty">${icon.ballot()}<h3>${L('Élection introuvable', 'Race not found')}</h3><p>${L('Elle n’est peut-être pas sur le bulletin de 2026.', 'It may not be on the 2026 ballot.')} <a href="#/">${L('Retour à la carte', 'Back to the map')}</a></p></div></div>`;
    }
    const kind = race.result || awaitingResult(race) ? ['résultats', 'results'] : race.format === 'field' || race.format === 'office' ? ['élection', 'race'] : ['prévision', 'forecast'];
    document.title = L(`${raceTitle(race)} : ${kind[0]} · Informed Voter`, `${raceTitle(race)} ${kind[1]} · Informed Voter`);
    const level = race.level === 'federal' ? 'federal' : 'state';
    const chamber = race.office === 'house' || race.office === 'state-house' ? 'house' : race.office === 'legislature' ? 'leg' : 'senate';
    const back = race.office === 'governor' ? `#/state/${race.state}` : `#/state/${race.state}?level=${level}&chamber=${chamber}${race.district ? `&d=${race.district}` : ''}`;
    return html`<div class="wrap page">
      <nav class="crumbs" aria-label="${L('Fil d’Ariane', 'Breadcrumb')}"><a href="#/">${L('Accueil', 'Home')}</a><span>/</span><a href="${back}">${stateName(race.state)}</a><span>/</span><span>${raceTitle(race)}</span></nav>
      ${raceFull(race)}
      <div style="margin-top:28px">${howToVote(race.state)}</div>
    </div>`;
  },
  mount(root) { mountRaceTabs(root); },
};
