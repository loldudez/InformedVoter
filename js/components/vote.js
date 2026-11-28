// "How to vote" steps, built only from official sources (no hard-coded deadlines,
// which change and differ by state). After Election Day the card points to the state's
// official results instead, since the counts shown here are unofficial.

import { html, fmtDate } from '../util.js';
import { certifiedIn, certExceptions } from '../data/world.js';
import { icon } from '../icons.js';
import { STATE_BY_ABBR, electionDateLabel, voteGovUrl, NASS_CAN_I_VOTE, inState, deState, stateNote } from '../data/states.js';
import { ELECTION_DAY } from '../model/forecast.js';
import { L, lang } from '../i18n.js';

// "mardi 3 novembre 2026" inside a French sentence.
const dateInText = () => (lang() === 'fr' ? electionDateLabel().replace(/^M/, 'm') : electionDateLabel());

const host = (u) => new URL(u).hostname.replace(/^www\./, '');
const ext = (href, label) => html`<a href="${href}" target="_blank" rel="noopener noreferrer">${label} ${icon.external()}</a>`;

export const afterVoting = (now = new Date()) => now >= ELECTION_DAY;
export const voteCardLabel = (st) => L(`${afterVoting() ? 'Résultats officiels' : 'Comment voter'} ${inState(st)}`, `${afterVoting() ? 'Official results in' : 'How to vote in'} ${STATE_BY_ABBR[st].name}`);

export function howToVote(st, { compact = false } = {}) {
  const s = STATE_BY_ABBR[st];
  if (afterVoting()) {
    const c = certifiedIn(st);
    // Contests the state left out (a recount, a runoff, the legislature's canvass in January).
    const out = c ? certExceptions(c) : [];
    const except = out.length ? html`${L(', sauf : ', ', except ')}${out.map((x, i) => html`${i ? L(' ; ', '; ') : ''}${x}`)}` : '';
    return html`<div class="card">
      <div class="eyebrow">${voteCardLabel(st)}</div>
      <h3 style="margin:4px 0 10px">${L(`Après le ${dateInText()}`, `After ${electionDateLabel()}`)}</h3>
      <ol class="small" style="margin:0;padding-left:20px;display:grid;gap:8px">
        ${lang() === 'fr'
          ? html`${c ? html`<li><b>L’État a certifié ses résultats le ${fmtDate(c.date)}</b>${except}. Les résultats officiels sont sur son site électoral ; les décomptes de ce site, compilés par Wikipédia, peuvent en différer légèrement. ${ext(s.office, host(s.office))}</li>`
            : html`<li><b>Les décomptes de ce site ne sont pas officiels.</b> L’État certifie ses résultats une fois chaque bulletin compté et les publie sur son site électoral officiel. ${ext(s.office, host(s.office))}</li>`}
        <li><b>Les seconds tours et les recomptages</b>, quand une élection en a, y sont aussi annoncés. Consultez ce site pour les dates.</li>
        <li><b>Avant la prochaine élection,</b> vérifiez votre inscription sur les listes électorales. ${ext(voteGovUrl(st), `Les règles ${deState(st)} sur vote.gov`)}</li>`
          : html`${c ? html`<li><b>${s.name} certified its results on ${fmtDate(c.date)}</b>${except}. The official results are on its election site; the counts on this site, as compiled by Wikipedia, may differ slightly. ${ext(s.office, host(s.office))}</li>`
            : html`<li><b>The counts on this site are unofficial.</b> ${s.name} certifies its results after counting every ballot and posts them on its official election site. ${ext(s.office, host(s.office))}</li>`}
        <li><b>Runoffs and recounts</b>, where a race has one, are announced there too. Check that site for dates.</li>
        <li><b>Before the next election,</b> check that you’re registered. ${ext(voteGovUrl(st), `${s.name} rules on vote.gov`)}</li>`}
      </ol>
    </div>`;
  }
  return html`<div class="card">
    <div class="eyebrow">${voteCardLabel(st)}</div>
    <h3 style="margin:4px 0 10px">${L(`Les étapes avant le ${dateInText()}`, `Steps before ${electionDateLabel()}`)}</h3>
    <ol class="small" style="margin:0;padding-left:20px;display:grid;gap:8px">
      ${lang() === 'fr'
        ? html`<li><b>Vérifiez votre inscription sur les listes électorales.</b> Les dates limites et l’inscription le jour même varient selon les États. ${ext(voteGovUrl(st), `Les règles ${deState(st)} sur vote.gov`)}</li>
      <li><b>Trouvez votre bureau de vote, les lieux de vote anticipé et les pièces d’identité demandées</b> sur le site électoral officiel. ${ext(s.office, host(s.office))}</li>
      <li><b>Votez par anticipation, par correspondance ou en personne le jour du scrutin.</b> ${ext(NASS_CAN_I_VOTE, 'Can I Vote? (Association nationale des secrétaires d’État)')}</li>`
        : html`<li><b>Check that you’re registered.</b> Deadlines and same-day options differ by state. ${ext(voteGovUrl(st), `${s.name} rules on vote.gov`)}</li>
      <li><b>Find your polling place, early-voting sites and ID rules</b> on the official election site. ${ext(s.office, host(s.office))}</li>
      <li><b>Vote early, by mail, or in person on Election Day.</b> ${ext(NASS_CAN_I_VOTE, 'Can I Vote? (National Association of Secretaries of State)')}</li>`}
    </ol>
    ${s.format && !compact ? html`<div class="notice" style="margin-top:12px">${icon.info()}<div>${stateNote(s)}</div></div>` : ''}
  </div>`;
}
