// One 2027 candidate: who they are, where they stand on the questionnaire's 144
// questions (each position with its source and, when there is one, the candidate's own
// words, never translated) and, for a visitor who has answered, how close they are,
// with "Comparer avec mes opinions" opening the side-by-side comparison.

import { html } from '../../util.js';
import { icon } from '../../icons.js';
import { L } from '../../i18n.js';
import { frStore } from '../store.js';
import { loadPres, loadPositions, candById, fmtDay, fmtPctFr, statusLabel, lastRead } from '../data.js';
import { candPhoto, partyChip, partyName, sourceLink, candidacySource } from '../components.js';
import { FR_CATEGORIES, FR_QUESTIONS, catTitle } from '../questions.js';
import { compareFr, MIN_COMPARED } from '../match.js';
import { positionItem, wireCompare, QUIZ_URL } from '../compare.js';

function matchCard(c, res) {
  const short = c.short || c.name;
  if (!res.userAnswered) {
    return html`<section class="card row between">
      <div><h2 style="margin:0">${L(`Vous et ${short}`, `You and ${short}`)}</h2><p class="muted" style="margin:4px 0 0">${L('Répondez au questionnaire Mes opinions pour voir sur quoi vous êtes d’accord et en désaccord.', 'Answer the My views questionnaire to see where you agree and disagree.')}</p></div>
      <a class="btn btn-primary" href="${QUIZ_URL}">${L('Répondre au questionnaire', 'Answer the questionnaire')}</a>
    </section>`;
  }
  return html`<section class="card row between" style="align-items:center">
    <div style="flex:1;min-width:240px"><h2 style="margin:0">${L(`Vous et ${short}`, `You and ${short}`)}</h2>
      <p class="small muted" style="margin:4px 0 12px">${L(
        `${res.similarities.length} points d’accord, ${res.differences.length} de désaccord, ${res.unclear.length} questions sans position connue, sur les ${res.userAnswered} auxquelles vous avez répondu.`,
        `${res.similarities.length} agreements, ${res.differences.length} differences and ${res.unclear.length} questions with no known position, out of the ${res.userAnswered} you answered.`,
      )}</p>
      <button type="button" class="btn btn-primary" data-compare="${c.id}">${icon.user()} ${L('Comparer avec mes opinions', 'Compare with my views')}</button></div>
    <div style="text-align:right"><div class="fr-score num">${res.score == null ? '—' : fmtPctFr(res.score, 0)}</div>
      <div class="tiny faint">${res.score == null ? L(`il faut ${MIN_COMPARED} questions en commun`, `${MIN_COMPARED} shared questions needed`) : L('d’affinité', 'match')}</div></div>
  </section>`;
}

async function load(ctx) {
  const [pres, positions] = await Promise.all([loadPres(), loadPositions()]);
  return { pres, positions, c: candById(pres, ctx.params[0]) };
}

export const candidat = {
  title: () => L('Candidat', 'Candidate'),
  rerenderOn: ['answers'],
  async render(ctx) {
    const { pres, positions, c } = await load(ctx);
    if (!c) return html`<div class="wrap page"><div class="empty"><h3>${L('Candidat introuvable', 'Candidate not found')}</h3><a class="btn" href="#/fr/presidentielle?tour=c">${L('Tous les candidats', 'All the candidates')}</a></div></div>`;
    document.title = `${c.name} · Informed Voter`;
    const mine = positions?.candidates?.[c.id] || {};
    const count = Object.keys(mine).length;
    const read = lastRead(mine);
    const answers = frStore.get().answers;
    const avg = pres.r1.average.candidates.find((a) => a.id === c.id);
    const wiki = c.article ? `https://fr.wikipedia.org/wiki/${encodeURIComponent(c.article.replace(/ /g, '_'))}` : null;
    return html`<div class="wrap page stack-lg" style="max-width:1000px">
      <nav class="crumbs"><a href="#/fr">${L('France', 'France')}</a><span>/</span><a href="#/fr/presidentielle?tour=c">${L('Présidentielle 2027', '2027 presidential election')}</a><span>/</span><span>${c.name}</span></nav>
      <section class="card fr-cand-head">
        ${candPhoto(c, { size: 96 })}
        <div style="min-width:0">
          <div class="eyebrow">${statusLabel(c)}</div>
          <h1 style="margin:4px 0 6px;font-size:clamp(28px,3.4vw,40px)">${c.name}</h1>
          <div class="row" style="gap:8px">${partyChip(c)}${c.party && partyName(c) ? html`<span class="small muted">${partyName(c)}</span>` : ''}</div>
          ${c.role ? html`<div class="small muted" style="margin-top:6px">${c.role}</div>` : ''}
          <div class="row small" style="gap:14px;margin-top:8px">
            ${avg ? html`<span>${L('Moyenne des sondages :', 'Poll average:')} <b>${fmtPctFr(avg.avg)}</b></span>` : ''}
            ${c.declared ? candidacySource(c) : ''}
            ${wiki ? sourceLink(wiki, 'Wikipédia') : ''}
          </div>
        </div>
      </section>
      ${c.declared ? '' : html`<div class="notice">${icon.info()}<div>${c.statusNote ? L(c.statusNote.fr, c.statusNote.en) : L(
        'Testée dans des sondages, cette personnalité ne figure pas parmi les candidatures recensées par Wikipédia et franceinfo.',
        'Tested in polls, but not among the declared candidates listed by Wikipedia and franceinfo.',
      )} ${candidacySource(c, '')} ${L(
        'Ses positions restent affichées pour mémoire, mais ne comptent pas dans la comparaison avec vos opinions.',
        'The positions below stay for reference but don’t count in the comparison with your views.',
      )}</div></div>`}
      ${count && c.declared ? matchCard(c, compareFr(answers, mine)) : ''}
      <section class="stack">
        <div><h2 style="margin:0">${L('Ses positions', 'Where they stand')}</h2>
          <p class="small muted" style="margin:4px 0 0">${count
            ? L(`${count} des ${FR_QUESTIONS.length} questions ont une position sourcée : programme, site de campagne, documents de son parti (indiqués comme tels), discours, entretiens ou articles de presse. Les citations sont reproduites mot pour mot ; les autres questions restent sans position plutôt que d’être devinées.`,
              `${count} of the ${FR_QUESTIONS.length} questions have a sourced position: program, campaign site, party documents (labelled as such), speeches, interviews or press reports. Quotes are reproduced word for word, in French; the other questions stay without a position rather than being guessed.`)
            : L('Aucune position sourcée pour l’instant. Les positions ne sont jamais déduites : elles seront ajoutées quand le candidat aura publié un programme ou des propositions.', 'No sourced positions yet. Positions are never inferred: they will be added once the candidate publishes a program or proposals.')}</p></div>
        ${FR_CATEGORIES.map((cat) => {
          const qs = cat.questions.filter((q) => mine[q.id]);
          return qs.length ? html`<details class="card" open><summary style="cursor:pointer;font-weight:650">${cat.n}. ${catTitle(cat)} <span class="faint small">(${qs.length})</span></summary>
            <div style="margin-top:6px">${qs.map((q) => positionItem(q, mine[q.id], answers[q.id]))}</div></details>` : '';
        })}
        ${read ? html`<p class="tiny faint" style="margin:0">${L('Positions vérifiées le', 'Positions checked on')} ${fmtDay(read)}. ${L('Une erreur ? Signalez-la avec le bouton d’aide.', 'Spotted an error? Report it with the help button.')}</p>` : ''}
      </section>
    </div>`;
  },
  async mount(root, ctx) {
    const { positions, c } = await load(ctx);
    if (!c) return null;
    return wireCompare(root, [c], positions?.candidates);
  },
};
