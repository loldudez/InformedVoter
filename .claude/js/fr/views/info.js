// The France section's reference pages: the election calendar, starred elections,
// what's real and where it comes from, and supporting the site.

import { html } from '../../util.js';
import { icon } from '../../icons.js';
import { L } from '../../i18n.js';
import { frStore } from '../store.js';
import { loadCalendar, loadPres, loadPositions, fmtDay, lastRead } from '../data.js';
import { researchedCandidates } from './comparer.js';
import { upcomingFor, electionName, electionWhat, whenLabel, electionTile, specialNote } from '../elections.js';
import { reminderButton } from '../../components/reminders.js';
import { DONATE_URL, SUPPORT_EMAIL, MAIL_SERVICE_URL, REMINDER_FROM } from '../../config.js';

function frStarBtn(id, name) {
  const on = frStore.get().starred.includes(id);
  return html`<button type="button" class="toggle-icon" data-fr-star="${id}" aria-pressed="${String(on)}" aria-label="${on ? L(`Ne plus suivre : ${name}`, `Unstar ${name}`) : L(`Suivre : ${name}`, `Star ${name}`)}" title="${on ? L('Suivie', 'Starred') : L('Suivre cette élection', 'Star this election')}">${on ? icon.starFill() : icon.star()}</button>`;
}

function electionCard(e, ad) {
  const note = specialNote(e, ad);
  return html`<article class="card stack-sm" id="e-${e.id}">
    <div class="row between" style="align-items:flex-start">
      <div class="row" style="align-items:flex-start;gap:14px">${electionTile(e)}<div><h3 style="margin:0">${electionName(e)}</h3><div class="small muted" style="margin-top:2px">${whenLabel(e)}</div><p class="small" style="margin:8px 0 0">${electionWhat(e)}</p>
        ${note ? html`<p class="small muted" style="margin:6px 0 0">${icon.info()} ${note}</p>` : ''}
        <div class="row" style="margin-top:8px">${e.href ? html`<a class="btn btn-sm" href="${e.href}">${L('Voir l’élection', 'See the election')}</a>` : ''}${reminderButton({ id: `fr:${e.id}`, name: electionName(e), date: e.date || null, month: e.month || null, section: 'fr' })}<a class="src-link" href="${e.source.url}" target="_blank" rel="noopener noreferrer">${L('source', 'source')} ${icon.external()}</a></div></div></div>
      ${frStarBtn(e.id, electionName(e))}
    </div>
  </article>`;
}

export const calendrier = {
  title: () => L('Prochaines élections', 'Upcoming elections'),
  rerenderOn: ['starred', 'reminders'],
  async render() {
    const cal = await loadCalendar();
    const ad = frStore.get().address;
    if (!cal) return html`<div class="wrap page"><div class="empty"><h3>${L('Calendrier indisponible', 'Calendar unavailable')}</h3></div></div>`;
    const mine = upcomingFor(cal, ad);
    const others = cal.elections.filter((e) => !mine.includes(e));
    return html`<div class="wrap page stack-lg" style="max-width:980px">
      <div><div class="eyebrow">${L('Calendrier électoral', 'Election calendar')}</div><h1 style="margin:6px 0 8px">${L('Les prochaines élections en France', 'The next elections in France')}</h1>
        <p class="muted" style="margin:0">${ad
          ? L(`Pour votre adresse à ${ad.city}. Les dates sans jour précis ne sont pas encore fixées par décret.`, `For your address in ${ad.city}. Dates without a day haven’t been set by decree yet.`)
          : L('Ajoutez votre adresse pour ne voir que les élections qui vous concernent. Les dates sans jour précis ne sont pas encore fixées par décret.', 'Add your address to see only the elections that concern you. Dates without a day haven’t been set by decree yet.')}
        ${ad ? '' : html` <a href="#/fr/profil?onglet=localisation">${L('Ajouter mon adresse', 'Add my address')}</a>`}</p></div>
      <div class="stack">${mine.map((e) => electionCard(e, ad))}</div>
      ${others.length ? html`<section><h2>${L('Ailleurs en France', 'Elsewhere in France')}</h2><p class="small muted">${L('Ces élections n’ont pas lieu à votre adresse.', 'These elections aren’t held at your address.')}</p><div class="stack">${others.map((e) => electionCard(e, null))}</div></section>` : ''}
    </div>`;
  },
  mount(root, ctx) {
    if (ctx.query.e) root.querySelector(`#e-${CSS.escape(ctx.query.e)}`)?.scrollIntoView({ block: 'center' });
  },
};

export const suivies = {
  title: () => L('Élections suivies', 'Starred elections'),
  rerenderOn: ['starred'],
  async render() {
    const cal = await loadCalendar();
    const ids = frStore.get().starred;
    const list = (cal?.elections || []).filter((e) => ids.includes(e.id));
    return html`<div class="wrap page stack" style="max-width:980px">
      <div><div class="eyebrow">${L('Élections suivies', 'Starred elections')}</div><h1 style="margin:6px 0 0">${L('Les élections que vous suivez', 'The elections you follow')}</h1></div>
      ${list.length ? html`<div class="stack">${list.map((e) => electionCard(e, frStore.get().address))}</div>`
        : html`<div class="empty">${icon.star()}<h3>${L('Aucune élection suivie', 'No starred elections yet')}</h3><p>${L('Cliquez sur l’étoile d’une élection pour la retrouver ici.', 'Click an election’s star to keep it here.')}</p><a class="btn" href="#/fr/calendrier">${L('Voir le calendrier', 'See the calendar')}</a></div>`}
    </div>`;
  },
};

export const aPropos = {
  title: () => L('À propos des données', 'About the data'),
  async render() {
    const [pres, positions] = await Promise.all([loadPres(), loadPositions()]);
    // Declared candidates only, as everywhere positions are compared.
    const researched = pres && positions ? researchedCandidates(pres, positions) : [];
    const nPos = researched.reduce((n, c) => n + Object.keys(positions.candidates[c.id]).length, 0);
    const read = researched.map((c) => lastRead(positions.candidates[c.id])).filter(Boolean).sort().pop() || null;
    const blank = (pres?.candidates || []).filter((c) => c.declared && !positions?.candidates?.[c.id]).length;
    const row = (what, src, note = '') => html`<tr><td>${what}</td><td>${src}</td><td class="small muted">${note}</td></tr>`;
    return html`<div class="wrap page stack-lg" style="max-width:980px">
      <div><div class="eyebrow">${L('À propos des données', 'About the data')}</div><h1 style="margin:6px 0 8px">${L('Ce qui est réel, et d’où ça vient', 'What’s real, and where it comes from')}</h1>
        <p class="muted" style="margin:0">${L('La section France est indépendante de la section États-Unis : ses données, ses pages et vos réponses sont séparées.', 'The France section is separate from the U.S. section: its data, pages and your answers are kept apart.')}</p></div>
      <div class="table-wrap"><table class="data">
        <thead><tr><th>${L('Quoi', 'What')}</th><th>${L('Source', 'Source')}</th><th>${L('Remarques', 'Notes')}</th></tr></thead>
        <tbody>
          ${row(L('Dates de la présidentielle', 'Presidential election dates'), html`<a href="https://fr.wikipedia.org/wiki/%C3%89lection_pr%C3%A9sidentielle_fran%C3%A7aise_de_2027" target="_blank" rel="noopener noreferrer">Wikipédia</a>`, L('Utilisée comme agrégateur (CC BY-SA), relue chaque jour.', 'Used as an aggregator (CC BY-SA), reread every day.'))}
          ${row(L('Candidats déclarés', 'Declared candidates'), html`${L('Une source de presse par candidature', 'One news source per candidacy')} · <a href="https://fr.wikipedia.org/wiki/%C3%89lection_pr%C3%A9sidentielle_fran%C3%A7aise_de_2027" target="_blank" rel="noopener noreferrer">Wikipédia</a>${pres?.meta.crossCheck ? html` · <a href="${pres.meta.crossCheck.url}" target="_blank" rel="noopener noreferrer">franceinfo</a>` : ''}`, L(
            `Seules les candidatures déclarées sont affichées${pres?.meta.candidatesChecked ? `, chacune vérifiée à la main le ${fmtDay(pres.meta.candidatesChecked)} dans l’article qui l’annonce ou la recense` : ''}. Les personnes que les sondeurs testent sans qu’elles soient candidates sont écartées de la moyenne. La liste est recoupée chaque jour avec celles de Wikipédia et de franceinfo ; un écart entre elles est signalé ci-dessous et vérifié à la main.`,
            `Only declared candidacies are shown${pres?.meta.candidatesChecked ? `, each checked by hand on ${fmtDay(pres.meta.candidatesChecked)} in the article announcing or listing it` : ''}. People pollsters test who aren’t running are left out of the average. The list is cross-checked every day with Wikipedia’s and franceinfo’s; any disagreement between them is flagged below and checked by hand.`,
          ))}
          ${row(L('Sondages des deux tours', 'Polls for both rounds'), html`<a href="https://fr.wikipedia.org/wiki/Liste_de_sondages_sur_l%27%C3%A9lection_pr%C3%A9sidentielle_fran%C3%A7aise_de_2027" target="_blank" rel="noopener noreferrer">Wikipédia</a> · <a href="https://www.commission-des-sondages.fr/" target="_blank" rel="noopener noreferrer">Commission des sondages</a>`, L('Relus chaque jour. Un sondage n’entre dans la moyenne que s’il est relié à sa notice officielle à la Commission des sondages (quand Wikipédia renvoie au site du sondeur, la notice est retrouvée dans la liste de la Commission). Cette liste sert aussi à repérer un sondage déposé que Wikipédia n’a pas encore reporté.', 'Reread every day. A poll counts only when it links to its official notice at the Commission des sondages (when Wikipedia links the pollster’s own site, the notice is found in the Commission’s list). That list also flags a poll filed there that Wikipedia hasn’t added yet.'))}
          ${row(L('Photos', 'Photos'), html`<a href="https://www.wikidata.org/" target="_blank" rel="noopener noreferrer">Wikidata</a> · <a href="https://commons.wikimedia.org/" target="_blank" rel="noopener noreferrer">Wikimedia Commons</a>`, L('Affichées en noir et blanc, avec l’auteur et la licence de chacune (page de la présidentielle, onglet Candidats).', 'Shown in black and white, with each one’s author and license (presidential page, Candidates tab).'))}
          ${row(L('Cartes des régions et départements', 'Region and department maps'), html`<a href="https://geoservices.ign.fr/adminexpress" target="_blank" rel="noopener noreferrer">IGN, ADMIN EXPRESS COG CARTO</a>`, L('Licence Ouverte 2.0. Outre-mer en encarts.', 'Licence Ouverte 2.0. Overseas departments in insets.'))}
          ${row(L('Communes et populations', 'Communes and populations'), html`<a href="https://geo.api.gouv.fr/" target="_blank" rel="noopener noreferrer">geo.api.gouv.fr</a>`, L('Populations INSEE.', 'INSEE populations.'))}
          ${row(L('Adresse vers commune', 'Address to commune'), html`<a href="https://geoservices.ign.fr/documentation/services/services-geoplateforme/geocodage" target="_blank" rel="noopener noreferrer">${L('Géoplateforme (IGN), service de géocodage', 'Géoplateforme (IGN) geocoding service')}</a>`, L('Votre adresse n’est envoyée qu’à ce service, après votre accord, et reste dans ce navigateur.', 'Your address is sent only to this service, after you agree, and stays in this browser.'))}
          ${row(L('Calendrier électoral', 'Election calendar'), L('Wikipédia (une source par élection)', 'Wikipedia (one source per election)'), L('Vérifié le 28 octobre 2026.', 'Checked October 28, 2026.'))}
          ${row(L('Positions des candidats', 'Candidates’ positions'), L('Programmes, sites de campagne, documents des partis, discours, entretiens et articles de presse, relus à la main (un lien par position)', 'Programs, campaign sites, party documents, speeches, interviews and press reports, read by hand (one link per position)'), L(
            `${researched.length} candidats déclarés, ${nPos} positions${read ? ` (sources lues jusqu’au ${fmtDay(read)})` : ''}. Les citations sont reproduites mot pour mot et vérifiées dans leur source ; une position n’est jamais devinée : sans source, la question reste « non documentée » et ne compte pas dans l’affinité.${blank === 1 ? ' Un candidat déclaré n’a encore publié ni programme ni proposition exploitable.' : blank ? ` ${blank} candidats déclarés n’ont encore publié ni programme ni proposition exploitable.` : ''}`,
            `${researched.length} declared candidates, ${nPos} positions${read ? ` (sources read through ${fmtDay(read)})` : ''}. Quotes are reproduced word for word and checked against their source; no position is guessed: without a source, a question stays “not documented” and doesn’t count toward the match.${blank === 1 ? ' One declared candidate hasn’t published a program or usable proposals yet.' : blank ? ` ${blank} declared candidates haven’t published a program or usable proposals yet.` : ''}`,
          ))}
        </tbody>
      </table></div>
      ${pres?.meta.checks?.length ? html`<div class="notice">${icon.info()}<div><b>${L('Écarts entre les sources, à vérifier', 'Sources that disagree, to check')}</b>
        <ul class="small" style="margin:6px 0 0">${pres.meta.checks.map((c) => html`<li>${L(c.fr, c.en)}</li>`)}</ul></div></div>` : ''}
      ${pres ? html`<p class="small faint">${L('Dernière mise à jour des candidats et des sondages', 'Candidates and polls last updated')} : ${fmtDay(pres.meta.updated)}.</p>` : ''}
      <div class="card"><h3>${L('Confidentialité et publicité', 'Privacy and ads')}</h3>
        <p class="muted small">${L('Il n’y a pas de compte : vos réponses, votre adresse, les élections que vous suivez et vos choix de rappels restent dans ce navigateur, et effacer ses données les supprime.', 'There are no accounts: your answers, address, starred elections and reminder choices stay in this browser, and clearing its data removes them.')}</p>
        <p class="muted small">${L(`Les tickets d’aide arrivent à ${SUPPORT_EMAIL} (Gmail), avec votre adresse e-mail seulement si vous la donnez, et ne servent qu’à vous répondre.`, `Help tickets go to ${SUPPORT_EMAIL} (Gmail), with your email address only if you give one, and are used only to answer you.`)}${MAIL_SERVICE_URL ? ' ' + L(`Si vous vous inscrivez aux rappels par e-mail, votre adresse, l’élection et les dates choisies sont gardées dans le compte Google du site (une feuille Google Sheets) et ne servent qu’à vous envoyer ces rappels, depuis ${REMINDER_FROM}. Rien n’est envoyé avant votre confirmation par e-mail, et l’adresse est effacée quand vous vous désinscrivez (un lien figure dans chaque e-mail), une fois l’élection passée, ou au bout de 7 jours sans confirmation.`, `If you sign up for email reminders, your address, the election and the dates you chose are kept in the site’s Google account (a Google Sheets file) and used only to send those reminders, from ${REMINDER_FROM}. Nothing is sent until you confirm by email, and the address is deleted when you unsubscribe (there’s a link in every email), once the election is over, or after 7 days if you never confirm.`) : ''} ${L(`Pour consulter, corriger ou effacer ce que le site garde sur vous, écrivez à ${SUPPORT_EMAIL}. Vous pouvez aussi adresser une réclamation à la`, `To see, correct or delete what the site holds about you, write to ${SUPPORT_EMAIL}. You can also complain to France’s data protection authority, the`)} <a href="https://www.cnil.fr/fr/plaintes" target="_blank" rel="noopener noreferrer">CNIL</a>.</p>
        <p class="muted small" style="margin:0">${L('Les publicités sont diffusées par Google AdSense : Google et ses partenaires utilisent des cookies et reçoivent votre adresse IP et l’adresse de la page consultée pour choisir et mesurer les annonces, y compris d’après vos visites sur d’autres sites. Informed Voter ne leur envoie ni vos opinions ni votre adresse. Vous pouvez désactiver les annonces personnalisées dans les', 'Ads are served by Google AdSense: Google and its partners use cookies and receive your IP address and the address of the page you’re on to choose and measure ads, including ads based on your visits to other sites. Informed Voter doesn’t send them your views or your address. You can turn off personalized ads in')} <a href="https://adssettings.google.com/" target="_blank" rel="noopener noreferrer">${L('paramètres des annonces de Google', 'Google’s Ads Settings')}</a> ${L('ou refuser les cookies publicitaires d’autres entreprises sur', 'or refuse other companies’ ad cookies at')} <a href="${L('https://www.youronlinechoices.com/fr/', 'https://www.youronlinechoices.com/uk/')}" target="_blank" rel="noopener noreferrer">Your Online Choices</a>${L(' ; voir aussi', '; see also')} <a href="${L('https://policies.google.com/technologies/partner-sites?hl=fr', 'https://policies.google.com/technologies/partner-sites')}" target="_blank" rel="noopener noreferrer">${L('comment Google utilise les données des sites partenaires', 'how Google uses information from sites that show its ads')}</a>.</p></div>
    </div>`;
  },
};

export const soutenir = {
  title: () => L('Soutenir le site', 'Support the site'),
  render: () => html`<div class="wrap page stack" style="max-width:820px">
    <div><div class="eyebrow">${L('Soutenir le site', 'Supporting the site')}</div><h1>${L('Aider Informed Voter à continuer', 'Keep Informed Voter running')}</h1><p class="muted">${L('Informed Voter est indépendant et gratuit. Les dons servent au fonctionnement du site, jamais à un candidat ou à un parti.', 'Informed Voter is independent and free. Donations pay for running the site, never a candidate or party.')}</p></div>
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
    <p class="small faint">${L('Les dons à Informed Voter ne sont pas des dons politiques et n’ouvrent droit à aucune réduction d’impôt.', 'Donations to Informed Voter are not political contributions and are not tax-deductible.')}</p>
  </div>`,
};
