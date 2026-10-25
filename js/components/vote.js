// "How to vote" steps, built only from official sources (no hard-coded deadlines,
// which change and differ by state).

import { html } from '../util.js';
import { icon } from '../icons.js';
import { STATE_BY_ABBR, ELECTION_DATE_LABEL, voteGovUrl, NASS_CAN_I_VOTE } from '../data/states.js';

const host = (u) => new URL(u).hostname.replace(/^www\./, '');
const ext = (href, label) => html`<a href="${href}" target="_blank" rel="noopener noreferrer">${label} ${icon.external()}</a>`;

export function howToVote(st, { compact = false } = {}) {
  const s = STATE_BY_ABBR[st];
  return html`<div class="card">
    <div class="eyebrow">How to vote in ${s.name}</div>
    <h3 style="margin:4px 0 10px">Steps before ${ELECTION_DATE_LABEL}</h3>
    <ol class="small" style="margin:0;padding-left:20px;display:grid;gap:8px">
      <li><b>Check that you’re registered.</b> Deadlines and same-day options differ by state. ${ext(voteGovUrl(st), `${s.name} rules on vote.gov`)}</li>
      <li><b>Find your polling place, early-voting sites and ID rules</b> on the official election site. ${ext(s.office, host(s.office))}</li>
      <li><b>Vote early, by mail, or in person on Election Day.</b> ${ext(NASS_CAN_I_VOTE, 'Can I Vote? (National Association of Secretaries of State)')}</li>
    </ol>
    ${s.format && !compact ? html`<div class="notice" style="margin-top:12px">${icon.info()}<div>${s.format}</div></div>` : ''}
  </div>`;
}
