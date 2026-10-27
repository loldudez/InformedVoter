import { html } from '../util.js';
import { icon } from '../icons.js';
import { STATE_BY_ABBR } from '../data/states.js';
import { ensureRace, raceTitle } from '../data/world.js';
import { raceFull, mountRaceTabs } from '../components/race.js';
import { howToVote } from '../components/vote.js';

export const racePage = {
  title: () => 'Race forecast',
  async render(ctx) {
    const race = await ensureRace(decodeURIComponent(ctx.params[0]));
    if (!race) {
      return html`<div class="wrap page"><div class="empty">${icon.ballot()}<h3>Race not found</h3><p>It may not be on the 2026 ballot. <a href="#/">Back to the map</a></p></div></div>`;
    }
    document.title = `${raceTitle(race)} forecast · Informed Voter`;
    const s = STATE_BY_ABBR[race.state];
    const level = race.level === 'federal' ? 'federal' : 'state';
    const chamber = race.office === 'house' || race.office === 'state-house' ? 'house' : race.office === 'legislature' ? 'leg' : 'senate';
    const back = race.office === 'governor' ? `#/state/${race.state}` : `#/state/${race.state}?level=${level}&chamber=${chamber}${race.district ? `&d=${race.district}` : ''}`;
    return html`<div class="wrap page">
      <nav class="crumbs" aria-label="Breadcrumb"><a href="#/">Home</a><span>/</span><a href="${back}">${s.name}</a><span>/</span><span>${raceTitle(race)}</span></nav>
      ${raceFull(race)}
      <div style="margin-top:28px">${howToVote(race.state)}</div>
    </div>`;
  },
  mount(root) { mountRaceTabs(root); },
};
