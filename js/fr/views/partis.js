// France's main parties: who leads them (photo in gray), where they place themselves,
// their stated ideology, their seats, their official site and their 2027 candidates.
// Everything comes from each party's French Wikipedia infobox (scripts/fr/partis.py),
// reread every day; English mode translates the terms.

import { html } from '../../util.js';
import { icon } from '../../icons.js';
import { L, lang } from '../../i18n.js';
import { loadParties, loadPres, candById, partyColor, fmtDay } from '../data.js';
import { candPhoto } from '../components.js';

const IDEOLOGY_EN = {
  Altermondialisme: 'Alter-globalization', Antilibéralisme: 'Anti-liberalism', Communisme: 'Communism', Conservatisme: 'Conservatism',
  'Conservatisme social': 'Social conservatism', "Critique de l'islam": 'Criticism of Islam', Décroissance: 'Degrowth',
  'Démocratie chrétienne': 'Christian democracy', 'Démocratie participative': 'Participatory democracy', Eurocommunisme: 'Eurocommunism',
  Europhilie: 'Pro-Europeanism', Euroscepticisme: 'Euroscepticism', 'Fédéralisme européen': 'European federalism', Gaullisme: 'Gaullism',
  Humanisme: 'Humanism', Identitarisme: 'Identitarianism', Libertarianisme: 'Libertarianism', 'Libéral-conservatisme': 'Liberal conservatism',
  'Libéralisme économique': 'Economic liberalism', 'Mouvance identitaire': 'Identitarian movement', 'National-conservatisme': 'National conservatism',
  'National-populisme': 'National populism', 'Nationalisme en France': 'French nationalism', 'Nationalisme économique': 'Economic nationalism',
  Nativisme: 'Nativism', 'Néo-conservatisme': 'Neoconservatism', Néolibéralisme: 'Neoliberalism', "Opposition à l'immigration": 'Opposition to immigration',
  'Populisme de droite': 'Right-wing populism', 'Populisme de gauche': 'Left-wing populism', Progressisme: 'Progressivism', 'Progrès social': 'Social progress',
  Protectionnisme: 'Protectionism', Réformisme: 'Reformism', Régionalisme: 'Regionalism', 'Social-démocratie': 'Social democracy',
  'Social-libéralisme': 'Social liberalism', 'Social-écologie': 'Social ecology', Socialisme: 'Socialism', 'Socialisme démocratique': 'Democratic socialism',
  Souverainisme: 'Sovereigntism', Transformisme: 'Transformism', 'Troisième voie': 'Third Way', Ultralibéralisme: 'Ultraliberalism',
  Écoféminisme: 'Ecofeminism', 'Écologie politique': 'Political ecology', Écosocialisme: 'Ecosocialism',
};
// Longest phrases first, so "Centre gauche à gauche" wins over "Centre gauche".
const POSITION_EN = [
  ['Centre gauche à sa fondation', 'centre-left at its founding'], ['Centre gauche à gauche', 'Centre-left to left'],
  ['centre gauche à centre droit', 'centre-left to centre-right'], ['voire extrême gauche', 'or far left'], ['voire extrême centre', 'or radical centre'],
  ['à gauche radicale', 'to radical left'], ['à droite radicale', 'to radical right'], ['Gauche radicale', 'Radical left'],
  ['Extrême droite', 'Far right'], ['Centre gauche', 'Centre-left'], ['Centre droit', 'Centre-right'], ['centre à droite', 'centre to right'],
  ['ou attrape-tout', 'or big tent'], ['à droite', 'to right'], ['(contesté)', '(disputed)'], ['Gauche', 'Left'], ['Droite', 'Right'], ['Centre', 'Centre'],
];
const ROLE_EN = {
  Président: 'President', Présidente: 'President', 'Co-présidents': 'Co-presidents', Coprésidents: 'Co-presidents', 'Premier secrétaire': 'First secretary',
  'Première secrétaire': 'First secretary', 'Secrétaire national': 'National secretary', 'Secrétaire nationale': 'National secretary',
  Coordinateur: 'Coordinator', Coordinatrice: 'Coordinator', 'Secrétaire général': 'Secretary-general', 'Secrétaire générale': 'Secretary-general',
};

const ideo = (t) => (lang() === 'en' ? IDEOLOGY_EN[t] || t : t);
const role = (r) => (lang() === 'en' ? ROLE_EN[r] || r : r);
function position(p) {
  if (!p || lang() !== 'en') return p;
  let s = p;
  for (const [fr, en] of POSITION_EN) s = s.split(fr).join(en);
  return s;
}

function partyCard(p, pres) {
  const cands = p.candidates.map((id) => candById(pres, id)).filter((c) => c?.declared);
  return html`<article class="card fr-party-card" style="--pc:${partyColor(p.abbr)}">
    <div class="fr-party-head"><span class="fr-party-swatch"></span>
      <div><h2 style="margin:0;font-size:22px">${p.name} <span class="faint" style="font-weight:500">(${p.abbr})</span></h2>
      ${lang() === 'en' ? html`<div class="small muted">${p.en}</div>` : ''}</div></div>
    <div class="fr-leaders">${p.leaders.map((l) => html`<div class="fr-leader">${candPhoto({ name: l.name, photo: l.photo, party: p.abbr }, { size: 76 })}<div><div class="eyebrow">${role(l.role)}</div><b>${l.name}</b></div></div>`)}</div>
    <dl class="kv">
      ${p.position ? html`<dt>${L('Positionnement', 'Position')}</dt><dd>${position(p.position)}</dd>` : ''}
      ${p.seats ? html`<dt>${L('Députés', 'National Assembly seats')}</dt><dd>${p.seats}</dd>` : ''}
      ${cands.length ? html`<dt>${L('Candidature 2027', '2027 candidate')}</dt><dd>${cands.map((c, i) => html`${i ? ', ' : ''}<a href="#/fr/presidentielle?tour=c">${c.name}</a>`)}</dd>` : ''}
    </dl>
    ${p.ideology.length ? html`<div><div class="eyebrow" style="margin-bottom:6px">${L('Idéologie', 'Ideology')}</div><div class="fr-tags">${p.ideology.map((t) => html`<span class="chip">${ideo(t)}</span>`)}</div></div>` : ''}
    <div class="row">${p.site ? html`<a class="btn btn-sm" href="${p.site}" target="_blank" rel="noopener noreferrer">${L('Site officiel et programme', 'Official site and platform')} ${icon.external()}</a>` : ''}<a class="src-link" href="${p.source.url}" target="_blank" rel="noopener noreferrer">${L('source', 'source')} ${icon.external()}</a></div>
  </article>`;
}

export const partis = {
  title: () => L('Les partis et leurs valeurs', 'Parties and values'),
  async render() {
    const [data, pres] = await Promise.all([loadParties(), loadPres()]);
    if (!data) return html`<div class="wrap page"><div class="empty"><h3>${L('Données indisponibles', 'Data unavailable')}</h3></div></div>`;
    const leaders = data.parties.flatMap((p) => p.leaders.filter((l) => l.photo));
    return html`<div class="wrap page stack-lg">
      <div><div class="eyebrow">${L('Les principaux partis et leurs valeurs', 'The main parties and values')}</div>
        <h1 style="margin:6px 0 8px">${L('Qui sont les partis, et que défendent-ils ?', 'Who the parties are and what they stand for')}</h1>
        <p class="muted" style="margin:0">${L(
          `Du plus à gauche au plus à droite. Dirigeants, positionnement et idéologie tels que les présente l’article Wikipédia de chaque parti (avec ses sources), relus chaque jour ; mis à jour le ${fmtDay(data.updated)}. Le site officiel de chaque parti présente son programme.`,
          `From left to right. Leaders, position and ideology as each party’s French Wikipedia article presents them (with its sources), reread every day; updated ${fmtDay(data.updated)}. Each party’s official site has its platform.`,
        )}</p></div>
      <div class="grid grid-2">${data.parties.map((p) => partyCard(p, pres))}</div>
      <details class="card"><summary style="cursor:pointer;font-weight:650">${L('Crédits photo', 'Photo credits')}</summary>
        <ul class="small" style="margin:10px 0 0">${leaders.map((l) => html`<li>${l.name} : ${l.photo.artist || L('auteur inconnu', 'unknown author')}, ${l.photo.license || ''} — <a href="${l.photo.page}" target="_blank" rel="noopener noreferrer">Wikimedia Commons</a></li>`)}</ul>
      </details>
    </div>`;
  },
};
