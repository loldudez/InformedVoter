// The 2027 presidential election: the first round (poll average and every poll, one
// row per line-up tested), the second round (each match-up tested) and the candidates.

import { html, raw } from '../../util.js';
import { icon } from '../../icons.js';
import { L } from '../../i18n.js';
import { loadPres, loadPositions, mainCandidates, candById, isCurrentDuel, fmtDay, fmtNum, fmtInt, fmtPctFr, partyColor, pollDates, runningIds, usedScenarios, statusLabel } from '../data.js';
import { countdown, averageBars, duelCard, candPhoto, partyChip, partyName, sourceLink, candidacySource } from '../components.js';
import { frStore } from '../store.js';
import { compareFr, MIN_COMPARED } from '../match.js';
import { wireCompare, QUIZ_URL } from '../compare.js';
import { researchedCandidates } from './comparer.js';

const TABS = () => [['1', L('Premier tour', 'First round')], ['2', L('Second tour', 'Second round')], ['c', L('Les candidats', 'The candidates')]];

function firstRound(pres) {
  const rows = mainCandidates(pres, 1);
  const cols = rows.slice(0, 11);
  const val = (v) => (v == null ? html`<span class="faint">—</span>` : v === 0.5 ? '<1' : fmtNum(v, v % 1 ? 1 : 0));
  // Line-ups with people who aren't running are left out unless the average needs
  // them for a declared candidate; those that stay name the non-candidates.
  const running = runningIds(pres);
  const polls = pres.r1.polls.map((p) => ({ ...p, scenarios: usedScenarios(p, running) })).filter((p) => p.scenarios.length);
  const hidden = pres.r1.polls.reduce((n, p) => n + p.scenarios.length, 0) - polls.reduce((n, p) => n + p.scenarios.length, 0);
  const notRunning = (s) => Object.keys(s).filter((id) => !running.has(id)).map((id) => candById(pres, id)?.short || id);
  return html`<div class="stack-lg">
    <div class="card stack">
      <div><h2 style="margin:0">${L('La moyenne des sondages', 'The poll average')}</h2>
      <p class="small muted" style="margin:4px 0 0">${L(
        `Les candidats déclarés, dans les sondages publiés au cours des ${pres.meta.windowDays} jours avant le plus récent (${pres.r1.average.polls} sondages, du ${fmtDay(pres.r1.average.from, { year: false })} au ${fmtDay(pres.r1.average.to)}). Quand un sondage teste plusieurs hypothèses de candidatures, la valeur médiane du candidat est retenue parmi les hypothèses composées uniquement de candidats déclarés (à défaut, parmi toutes celles où il figure), pour que chaque sondage compte une fois. Le trait clair va du sondage le plus bas au plus haut.`,
        `The declared candidates, in the polls published in the ${pres.meta.windowDays} days before the latest one (${pres.r1.average.polls} polls, ${fmtDay(pres.r1.average.from, { year: false })} to ${fmtDay(pres.r1.average.to)}). When a poll tests several line-ups, the candidate’s median value is taken from the line-ups made only of declared candidates (failing that, from every line-up that includes them), so each poll counts once. The light band runs from the lowest poll to the highest.`,
      )}</p></div>
      ${averageBars(pres, rows)}
      <p class="tiny faint" style="margin:0">${L('Un sondage n’est pas une prévision : il mesure les intentions de vote au moment où il est réalisé, avec une marge d’erreur de un à trois points.', 'A poll isn’t a forecast: it measures voting intentions when it is taken, with a margin of error of one to three points.')}</p>
    </div>
    ${pollCheck(pres)}
    <div class="card">
      <h2 style="margin:0 0 4px">${L('Tous les sondages', 'Every poll')}</h2>
      <p class="small muted" style="margin:0 0 12px">${L(
        `Une ligne par hypothèse testée. ${hidden ? `Les ${hidden} hypothèses avec des personnes qui ne sont pas candidates sont masquées, sauf quand un candidat déclaré n’a été testé qu’avec elles : leurs noms sont alors indiqués. ` : ''}Chaque sondeur est relié à la notice officielle déposée à la Commission des sondages.`,
        `One row per line-up tested. ${hidden ? `The ${hidden} line-ups with people who aren’t running are hidden, except where a declared candidate was tested only alongside them; their names are shown there. ` : ''}Each pollster links to the official notice filed with the Commission des sondages.`,
      )}</p>
      <div class="table-wrap"><table class="data fr-polls">
        <thead><tr><th>${L('Sondeur', 'Pollster')}</th><th>${L('Dates', 'Dates')}</th><th class="r">${L('Échantillon', 'Sample')}</th>${cols.map((c) => html`<th class="r" title="${c.name}"><span class="fr-colhead"><i style="background:${partyColor(c.party)}"></i>${c.short}</span></th>`)}</tr></thead>
        <tbody>${polls.flatMap((p) => p.scenarios.map((s, k) => html`<tr${k === 0 ? raw(' class="first"') : ''}>
          <td>${k === 0 ? html`<a href="${p.url}" target="_blank" rel="noopener noreferrer">${p.pollster}</a>` : ''}${notRunning(s).length ? html`<span class="tiny faint" style="display:block">${L('avec', 'with')} ${notRunning(s).join(', ')}</span>` : ''}</td>
          <td class="nowrap">${k === 0 ? pollDates(p.dates.replace(/\s+20\d\d$/, '')) : ''}</td>
          <td class="r num">${k === 0 && p.n ? fmtInt(p.n) : ''}</td>
          ${cols.map((c) => html`<td class="r num">${val(s[c.id])}</td>`)}
        </tr>`))}</tbody>
      </table></div>
    </div>
  </div>`;
}

// How current the polls are: Wikipedia's list is reread every day and checked against
// the notices filed with the Commission des sondages (scripts/fr/update_presidentielle.py).
function pollCheck(pres) {
  const pc = pres.meta.pollCheck;
  const latest = pres.r1.polls[0];
  if (!pc || !latest) return '';
  const checked = fmtDay(pres.meta.updated);
  const missing = pc.missing || [];
  const n = missing.length;
  const status = !pc.read
    ? L('la liste des notices n’a pas pu être lue lors de la dernière mise à jour.', 'the list of notices couldn’t be read at the last update.')
    : !n ? L('aucun sondage plus récent n’y a été déposé.', 'no newer poll has been filed there.')
      : html`${n === 1
        ? L('un sondage déposé n’est pas encore sur la liste de Wikipédia ; il entrera dans la moyenne dès qu’il y sera', 'one poll filed there isn’t on Wikipedia’s list yet; it will join the average once it is')
        : L(`${n} sondages déposés ne sont pas encore sur la liste de Wikipédia ; ils entreront dans la moyenne dès qu’ils y seront`, `${n} polls filed there aren’t on Wikipedia’s list yet; they will join the average once they are`)} (${missing.map((m, i) => html`${i ? ', ' : ''}<a href="${m.url}" target="_blank" rel="noopener noreferrer">${m.title}</a>`)}).`;
  return html`<div class="notice">${icon.info()}<div>${L(
    `Dernier sondage : ${latest.pollster}, ${pollDates(latest.dates)}. La liste est relue chaque jour sur Wikipédia et recoupée avec les notices déposées à la Commission des sondages (vérifié le ${checked}) :`,
    `Latest poll: ${latest.pollster}, ${pollDates(latest.dates)}. The list is reread every day from Wikipedia and checked against the notices filed with the Commission des sondages (checked ${checked}):`,
  )} ${status}</div></div>`;
}

function secondRound(pres) {
  const current = pres.r2.filter((d) => isCurrentDuel(d, pres));
  const older = pres.r2.filter((d) => !isCurrentDuel(d, pres));
  const table = (d) => {
    const a = candById(pres, d.a), b = candById(pres, d.b);
    return html`<details class="fr-duel-polls"><summary>${L(`Les ${d.polls.length} sondages`, `All ${d.polls.length} polls`)}</summary>
      <div class="table-wrap"><table class="data"><thead><tr><th>${L('Sondeur', 'Pollster')}</th><th>${L('Dates', 'Dates')}</th><th class="r">${L('Échantillon', 'Sample')}</th><th class="r">${a.short}</th><th class="r">${b.short}</th></tr></thead>
      <tbody>${d.polls.map((p) => html`<tr><td><a href="${p.url}" target="_blank" rel="noopener noreferrer">${p.pollster}</a></td><td class="nowrap">${pollDates(p.dates)}</td><td class="r num">${p.n ? fmtInt(p.n) : ''}</td><td class="r num">${fmtNum(p.a, p.a % 1 ? 1 : 0)}</td><td class="r num">${fmtNum(p.b, p.b % 1 ? 1 : 0)}</td></tr>`)}</tbody></table></div>
    </details>`;
  };
  return html`<div class="stack-lg">
    <div class="notice">${icon.info()}<div>${L(
      'Au second tour, seuls les deux candidats arrivés en tête du premier tour s’affrontent, le dimanche deux semaines plus tard. Les sondeurs testent dès maintenant plusieurs duels possibles ; ce sont des hypothèses, pas des prévisions.',
      'Only the top two candidates from the first round meet in the second round, two Sundays later. Pollsters already test several possible match-ups; they are hypotheses, not forecasts.',
    )}</div></div>
    <div class="grid grid-2">${current.map((d) => html`<div class="card stack-sm">${duelCard(d, pres)}${table(d)}</div>`)}</div>
    ${older.length ? html`<section><h3>${L('Duels moins testés récemment', 'Match-ups not tested recently')}</h3><div class="grid grid-2">${older.map((d) => html`<div class="card stack-sm">${duelCard(d, pres, { current: false })}${table(d)}</div>`)}</div></section>` : ''}
  </div>`;
}

function candidates(pres, positions) {
  const avg = new Map(pres.r1.average.candidates.map((a) => [a.id, a.avg]));
  const answers = frStore.get().answers;
  const researched = (c) => {
    const mine = positions?.candidates?.[c.id];
    if (!mine) return '';
    const n = Object.keys(mine).length;
    const { score } = compareFr(answers, mine);
    return html`<div class="small" style="margin-top:6px"><a href="#/fr/candidat/${c.id}">${L(`${n} positions sourcées`, `${n} sourced positions`)}</a>${score != null ? html` · ${L('affinité', 'match')} <b>${fmtPctFr(score, 0)}</b>` : ''}</div>
      <button type="button" class="btn btn-sm" data-compare="${c.id}" style="margin-top:8px">${L('Comparer avec mes opinions', 'Compare with my views')}</button>`;
  };
  const answered = frStore.answered();
  const list = pres.candidates.filter((c) => c.declared).sort((a, b) => ((avg.get(b.id) ?? -1) - (avg.get(a.id) ?? -1)) || a.name.localeCompare(b.name, 'fr'));
  const out = pres.candidates.filter((c) => !c.declared).sort((a, b) => a.name.localeCompare(b.name, 'fr'));
  const wiki = (c) => `https://fr.wikipedia.org/wiki/${encodeURIComponent(c.article.replace(/ /g, '_'))}`;
  const checked = pres.meta.candidatesChecked;
  return html`<div class="stack-lg">
    <p class="muted" style="margin:0">${L(
      `${list.length} personnes ont déclaré leur candidature.${checked ? ` Chacune a été vérifiée le ${fmtDay(checked)} dans une source de presse (lien « Candidature » sur chaque carte)` : ''}, et la liste est recoupée chaque jour avec celles de Wikipédia et de franceinfo. Pour figurer sur le bulletin, il faudra encore réunir 500 parrainages d’élus ; le Conseil constitutionnel publiera la liste officielle avant le premier tour.`,
      `${list.length} people have declared their candidacy.${checked ? ` Each was checked on ${fmtDay(checked)} against a news source (the “Candidacy” link on each card)` : ''}, and the list is cross-checked every day with Wikipedia’s and franceinfo’s. To be on the ballot they still need 500 sponsorships from elected officials; the Constitutional Council publishes the official list before the first round.`,
    )}</p>
    ${positions ? html`<div class="card row between fr-compare-cta">
      <div style="flex:1;min-width:240px"><b>${L('Quel candidat vous correspond ?', 'Which candidate matches you?')}</b>
        <p class="small muted" style="margin:2px 0 0">${answered >= MIN_COMPARED
          ? L('Le classement de tous les candidats dont les positions sont sourcées, d’après vos réponses à Mes opinions. Chaque carte ci-dessous a aussi son bouton de comparaison.', 'The ranking of every candidate with sourced positions, from your answers in My views. Each card below also has its own compare button.')
          : L(`Répondez à au moins ${MIN_COMPARED} questions de Mes opinions pour comparer les candidats à vos idées (vous en avez ${answered}).`, `Answer at least ${MIN_COMPARED} questions in My views to compare the candidates with your views (you have ${answered}).`)}</p></div>
      ${answered >= MIN_COMPARED
        ? html`<a class="btn btn-primary" href="#/fr/elections/comparer">${icon.user()} ${L('Comparer avec mes opinions', 'Compare with my views')}</a>`
        : html`<a class="btn" href="${QUIZ_URL}">${icon.user()} ${L('Répondre d’abord à Mes opinions', 'Answer My views first')}</a>`}
    </div>` : ''}
    <div class="grid grid-3">${list.map((c) => html`<article class="card tight fr-cand">
      ${candPhoto(c, { size: 64 })}
      <div style="min-width:0">
        <h3 style="margin:0;font-size:17px"><a href="#/fr/candidat/${c.id}">${c.name}</a></h3>
        <div class="row" style="gap:6px;margin:4px 0">${partyChip(c)}</div>
        ${c.role ? html`<div class="small muted">${c.role}</div>` : ''}
        ${c.slogan ? html`<div class="small" style="margin-top:4px">« ${c.slogan} »</div>` : ''}
        ${avg.has(c.id) ? html`<div class="small" style="margin-top:4px">${L('Moyenne des sondages :', 'Poll average:')} <b>${fmtPctFr(avg.get(c.id))}</b></div>` : ''}
        ${researched(c)}
        <div class="row" style="gap:12px;margin-top:6px">${candidacySource(c)}${c.wiki ? sourceLink(wiki(c), 'Wikipédia') : ''}</div>
      </div>
    </article>`)}</div>
    ${out.length ? html`<details class="card"><summary style="cursor:pointer;font-weight:650">${L(`Sans candidature déclarée (${out.length})`, `Not running (${out.length})`)}</summary>
      <p class="small muted" style="margin:10px 0 0">${L(
        'Des personnalités testées par les sondeurs ou citées comme candidates possibles, qui n’ont pas de candidature déclarée aujourd’hui. Elles ne comptent ni dans la moyenne des sondages ni dans la comparaison avec vos opinions.',
        'People pollsters test or who were mentioned as possible candidates, with no declared candidacy today. They count neither in the poll average nor in the comparison with your views.',
      )}</p>
      <ul class="small fr-out">${out.map((c) => html`<li><b>${c.name}</b> · ${statusLabel(c)}. ${c.statusNote ? L(c.statusNote.fr, c.statusNote.en) : L(
        'Testée dans des sondages, cette personnalité ne figure pas parmi les candidatures recensées par Wikipédia et franceinfo.',
        'Tested in polls, but not among the declared candidates listed by Wikipedia and franceinfo.',
      )} ${candidacySource(c, '')}</li>`)}</ul>
    </details>` : ''}
    <details class="card"><summary style="cursor:pointer;font-weight:650">${L('Crédits photo', 'Photo credits')}</summary>
      <ul class="small" style="margin:10px 0 0">${list.filter((c) => c.photo).map((c) => html`<li>${c.name} : ${c.photo.artist || L('auteur inconnu', 'unknown author')}, ${c.photo.license || ''} — <a href="${c.photo.page}" target="_blank" rel="noopener noreferrer">Wikimedia Commons</a></li>`)}</ul>
      <p class="tiny faint" style="margin:8px 0 0">${L('Photos affichées en noir et blanc. Elles viennent de Wikidata et de Wikimedia Commons, sous les licences indiquées.', 'Photos are shown in black and white. They come from Wikidata and Wikimedia Commons, under the licenses shown.')}</p>
    </details>
  </div>`;
}

export const presidentielle = {
  title: () => L('Présidentielle 2027', '2027 presidential election'),
  async render(ctx) {
    const [pres, positions] = await Promise.all([loadPres(), loadPositions()]);
    if (!pres) return html`<div class="wrap page"><div class="empty"><h3>${L('Données indisponibles', 'Data unavailable')}</h3></div></div>`;
    const tab = ['2', 'c'].includes(ctx.query.tour) ? ctx.query.tour : '1';
    return html`<div class="wrap page stack-lg">
      <nav class="crumbs"><a href="#/fr">${L('France', 'France')}</a><span>/</span><span>${L('Présidentielle 2027', '2027 presidential election')}</span></nav>
      <section class="fr-hero card">
        <div><div class="eyebrow">${L('Élection présidentielle · deux tours', 'Presidential election · two rounds')}</div>
          <h1 style="margin:6px 0 8px">${L('Présidentielle 2027', 'The 2027 presidential election')}</h1>
          <p class="muted" style="margin:0">${L(
            'Le président est élu pour cinq ans au suffrage universel direct. Un candidat qui obtient plus de la moitié des voix au premier tour est élu ; sinon, les deux premiers s’affrontent au second tour.',
            'The president is elected for five years by direct popular vote. A candidate with more than half the votes in the first round wins; otherwise the top two meet in a second round.',
          )}</p>
          <p class="tiny faint" style="margin:10px 0 0">${L('Sources', 'Sources')} : ${pres.meta.sources.map((s, i) => html`${i ? ' · ' : ''}<a href="${s.url}" target="_blank" rel="noopener noreferrer">${s.title}</a>`)} · ${L('mis à jour', 'updated')} ${fmtDay(pres.meta.updated)}</p>
        </div>
        <div class="fr-counts">${countdown(pres.rounds.r1, { label: L('Premier tour', 'First round') })}${countdown(pres.rounds.r2, { label: L('Second tour', 'Second round') })}</div>
      </section>
      <nav class="seg big" aria-label="${L('Sections', 'Sections')}">${TABS().map(([k, label]) => html`<a href="#/fr/presidentielle${k === '1' ? '' : `?tour=${k}`}" ${raw(tab === k ? 'aria-current="page"' : '')}>${label}</a>`)}</nav>
      ${tab === '1' ? firstRound(pres) : tab === '2' ? secondRound(pres) : candidates(pres, positions)}
    </div>`;
  },
  async mount(root, ctx) {
    if (ctx.query.tour !== 'c') return null;
    const [pres, positions] = await Promise.all([loadPres(), loadPositions()]);
    return wireCompare(root, researchedCandidates(pres, positions), positions?.candidates);
  },
};

export { partyName };
