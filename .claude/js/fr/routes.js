// The France section's pages, all under #/fr. The router (js/router.js) draws the
// France header for these paths and never loads the U.S. race data for them.

import { frHome } from './views/home.js';
import { presidentielle } from './views/presidentielle.js';
import { regionView, departementView, villeView } from './views/geo.js';
import { calendrier, suivies, aPropos, soutenir } from './views/info.js';
import { profil, opinions, mesElections } from './views/profil.js';
import { partis } from './views/partis.js';
import { candidat } from './views/candidat.js';
import { comparer } from './views/comparer.js';
import { parlement } from './views/parlement.js';
import { enjeux } from './views/enjeux.js';

export const FR_ROUTES = [
  [/^\/fr$/, frHome],
  [/^\/fr\/presidentielle$/, presidentielle],
  [/^\/fr\/candidat\/([a-z0-9-]+)$/, candidat],
  [/^\/fr\/region\/(\d{2})$/, regionView],
  [/^\/fr\/departement\/(\w{2,3})$/, departementView],
  [/^\/fr\/ville\/(\w{5})$/, villeView],
  [/^\/fr\/partis$/, partis],
  [/^\/fr\/parlement$/, parlement],
  [/^\/fr\/enjeux$/, enjeux],
  [/^\/fr\/calendrier$/, calendrier],
  [/^\/fr\/suivies$/, suivies],
  [/^\/fr\/profil$/, profil],
  // The questionnaire lives under "Mon profil"; the old address still works.
  [/^\/fr\/profil\/opinions$/, opinions],
  [/^\/fr\/opinions$/, opinions],
  [/^\/fr\/elections$/, mesElections],
  [/^\/fr\/elections\/comparer$/, comparer],
  [/^\/fr\/a-propos$/, aPropos],
  [/^\/fr\/soutenir$/, soutenir],
];
