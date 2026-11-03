// France's Parliament: the Assemblée nationale and the Sénat as half-circle seat charts
// (js/components/hemicycle.js), colored by group with the key underneath, who holds the
// main offices, and every member in a searchable list. The chambers' open data, French
// Wikipedia (each group's president and declared position) and Wikidata (the President
// and the Prime Minister), reread every day by scripts/fr/parlement.py.

import { html, ordinal, initials } from '../../util.js';
import { icon } from '../../icons.js';
import { L } from '../../i18n.js';
import { loadParliament, fmtDay, photoSrc } from '../data.js';
import { drawHemicycle, swatch } from '../../components/hemicycle.js';

const colorOf = (key) => (key === 'other' ? 'var(--seat-other)' : `var(--fr-${key})`);
const POSITION = () => ({
  'Groupe majoritaire': L('Groupe majoritaire', 'Majority group'),
  'Groupe minoritaire': L('Groupe minoritaire', 'Minority group'),
  Opposition: L('Opposition', 'Opposition'),
});
// French titles follow the person's gender; f is null when the source doesn't say.
const byGender = (f, masc, fem, neutral) => (f === true ? fem : f === false ? masc : neutral);
const seatsWord = (n) => (n > 1 ? L('sièges', 'seats') : L('siège', 'seat'));
const pct = (n, d) => Math.round((100 * n) / d);

function groupsOf(ch, chamber) {
  return chamber.groups.map((g) => ({
    ...g,
    key: g.color,
    color: colorOf(g.color),
    name: g.id === 'NI' ? L('Non-inscrits (aucun groupe)', 'Non-attached (in no group)') : g.name.replace(/^Groupe (du |de la |de l’|de l')?/i, ''),
  }));
}

function roleOf(m, ch, g) {
  const f = m.f;
  if (m.role === 'president') {
    return ch === 'an'
      ? L(f ? 'Présidente de l’Assemblée nationale' : 'Président de l’Assemblée nationale', 'President of the National Assembly')
      : L(f ? 'Présidente du Sénat' : 'Président du Sénat', 'President of the Senate');
  }
  const house = ch === 'an' ? L('de l’Assemblée nationale', 'of the National Assembly') : L('du Sénat', 'of the Senate');
  const parts = [];
  if (m.role === 'group-president') parts.push(L(`${f ? 'Présidente' : 'Président'} du groupe ${g.short}`, `President of the ${g.short} group`));
  if (m.bureau === 'vp') parts.push(L(`${f ? 'Vice-présidente' : 'Vice-président'} ${house}`, `Vice-president ${house}`));
  if (m.bureau === 'quaestor') parts.push(L(`${f ? 'Questeure' : 'Questeur'} ${house}`, `Quaestor ${house}`));
  if (m.bureau === 'secretary') parts.push(L(`Secrétaire ${house}`, `Secretary ${house}`));
  return parts.join(' · ');
}

// "apparenté": sits with the group without joining it; "rattaché": attached for
// administrative purposes only (Senate).
const attachment = (m) => (m.app === 'A' ? L(m.f ? 'apparentée' : 'apparenté', 'affiliated')
  : m.app === 'R' ? L(m.f ? 'rattachée' : 'rattaché', 'attached') : '');

const placeOf = (m) => (m.circo ? L(`${m.depName} (${m.circo === 1 ? '1re' : `${m.circo}e`})`, `${m.depName} (${ordinal(m.circo)})`) : m.depName);

function tip(m, ch, g) {
  const role = roleOf(m, ch, g);
  return html`<div class="tt-title">${m.n}</div>
    ${role ? html`<div class="tt-sub">${role}</div>` : ''}
    <div class="t-row"><span>${L('Groupe', 'Group')}</span><b>${swatch(g, 12)}${g.short}${m.app ? ` (${attachment(m)})` : ''}</b></div>
    ${m.p ? html`<div class="t-row"><span>${L('Parti', 'Party')}</span><b>${m.p}</b></div>` : ''}
    <div class="t-row"><span>${L('Circonscription', 'Constituency')}</span><b>${placeOf(m)}</b></div>
    ${m.reg ? html`<div class="t-row"><span>${L('Région', 'Region')}</span><b>${m.reg}</b></div>` : ''}`;
}

function keyItem(g, members) {
  const lead = members.find((m) => m.g === g.id && m.role === 'group-president');
  const label = lead ? L(lead.f ? 'Présidente :' : 'Président :', 'President:') : L('Présidence :', 'President:');
  return html`<span><b>${g.short}</b>${g.short !== g.name ? html` · ${g.name}` : ''}</span>
    <span class="meta">${g.seats} ${seatsWord(g.seats)}${g.position ? ` · ${POSITION()[g.position] || g.position}` : ''}</span>
    ${g.president ? html`<span class="meta">${label} ${g.president}</span>` : ''}`;
}

function photo(p, key) {
  const src = photoSrc(p);
  const credit = p?.photo ? `${L('Photo :', 'Photo:')} ${p.photo.artist || L('auteur inconnu', 'unknown author')} (${p.photo.license || 'Wikimedia Commons'})` : '';
  return html`<span class="fr-photo" style="--size:64px;--pc:${key ? colorOf(key) : 'var(--fr-other)'}" title="${credit}">${src
    ? html`<img src="${src}" alt="" loading="lazy" decoding="async">`
    : html`<span class="fr-initials">${initials(p?.name || p?.n || '?')}</span>`}</span>`;
}

function person(p, key, title, name, extra) {
  return html`<div class="parl-person">${photo(p, key)}<div><div class="eyebrow">${title}</div><b>${name}</b>${extra ? html`<div class="small muted">${extra}</div>` : ''}</div></div>`;
}

function officials(data) {
  const o = data.officials || {};
  const an = data.chambers.an, sen = data.chambers.senat;
  const groupOf = (ch, m) => data.chambers[ch].groups.find((g) => g.id === m.g);
  const since = (d) => (d ? L(`depuis le ${fmtDay(d)}`, `since ${fmtDay(d)}`) : '');
  const people = [];
  if (o.president) {
    people.push(person(o.president, null, L(byGender(o.president.f, 'Président de la République', 'Présidente de la République', 'Présidence de la République'), 'President of the Republic'),
      o.president.name, since(o.president.since)));
  }
  if (o.pm) {
    people.push(person(o.pm, null, L(byGender(o.pm.f, 'Premier ministre', 'Première ministre', 'Chef du gouvernement'), 'Prime Minister'),
      o.pm.name, [since(o.pm.since), o.government ? L(`gouvernement ${o.government.name}`, `${o.government.name} government`) : ''].filter(Boolean).join(' · ')));
  }
  for (const [ch, m] of [['an', an.president], ['senat', sen.president]]) {
    if (!m) continue;
    const g = groupOf(ch, m);
    people.push(person({ ...m, name: m.n }, g?.color, roleOf(m, ch, g), m.n, `${g?.short || ''} · ${m.depName}`));
  }
  return html`<section class="card stack">
    <div><h2 style="margin:0">${L('Qui dirige ?', 'Who holds the main offices')}</h2>
      <p class="small muted" style="margin:4px 0 0">${L(
        'Le président de la République nomme le Premier ministre, qui dirige le gouvernement et en répond devant l’Assemblée nationale. Chaque chambre élit son président.',
        'The President of the Republic appoints the Prime Minister, who leads the government and answers to the National Assembly. Each chamber elects its own president.',
      )}</p></div>
    <div class="parl-people">${people}</div>
  </section>`;
}

function stats(ch, chamber, groups) {
  const sum = (gs) => gs.reduce((a, g) => a + g.seats, 0);
  const shorts = (gs) => gs.map((g) => g.short).join(', ');
  const notOpp = groups.filter((g) => g.position && g.position !== 'Opposition');
  const opp = groups.filter((g) => g.position === 'Opposition');
  const ni = groups.filter((g) => g.id === 'NI');
  const filled = chamber.members.length, vacant = chamber.seats - filled;
  const women = chamber.members.filter((m) => m.f).length;
  const tile = (label, value, sub) => html`<div class="stat"><div class="eyebrow">${label}</div><div class="value">${value}</div>${sub ? html`<div class="sub">${sub}</div>` : ''}</div>`;
  return html`<div class="parl-stats">
    ${tile(L('Sièges', 'Seats'), chamber.seats, vacant > 0 ? L(`${filled} occupés, ${vacant} vacant${vacant > 1 ? 's' : ''}`, `${filled} filled, ${vacant} vacant`) : L('Tous occupés', 'All filled'))}
    ${tile(L('Majorité absolue', 'Absolute majority'), chamber.majority, seatsWord(chamber.majority))}
    ${tile(L('Groupes non déclarés d’opposition', 'Groups not declared in opposition'), sum(notOpp), shorts(notOpp))}
    ${tile(L('Groupes d’opposition', 'Opposition groups'), sum(opp), shorts(opp))}
    ${ni.length ? tile(L('Non-inscrits', 'In no group'), sum(ni), '') : ''}
    ${tile(L('Femmes', 'Women'), women, L(`${pct(women, filled)} % des membres`, `${pct(women, filled)}% of members`))}
  </div>`;
}

// Departments in their usual order: 01…95 with Corsica's 2A and 2B after 19, then
// overseas, then French people abroad.
const depKey = (m) => (m.dep === '2A' ? 20.1 : m.dep === '2B' ? 20.2 : m.dep === '099' ? 9999 : /^\d+$/.test(m.dep || '') ? Number(m.dep) : 9998);
const fold = (s) => String(s || '').normalize('NFD').replace(/\p{Diacritic}/gu, '').toLowerCase();

function membersList(ch, chamber, groups) {
  const byId = new Map(groups.map((g) => [g.id, g]));
  const rows = [...chamber.members].sort((a, b) => depKey(a) - depKey(b) || (a.circo || 0) - (b.circo || 0) || a.n.localeCompare(b.n, 'fr'));
  const who = ch === 'an' ? L('députés', 'deputies') : L('sénateurs', 'senators');
  return html`<details class="card" id="parl-list">
    <summary style="cursor:pointer;font-weight:650">${L(`Les ${rows.length} ${who}, par circonscription`, `All ${rows.length} ${who}, by constituency`)}</summary>
    <div class="stack" style="margin-top:12px">
      <div class="row"><input class="input parl-find" id="parl-find" type="search" autocomplete="off"
        placeholder="${L('Nom, département, groupe…', 'Name, department, group…')}" aria-label="${L('Rechercher dans la liste', 'Search the list')}">
        <span class="small muted" id="parl-count" aria-live="polite"></span></div>
      <div class="table-wrap"><table class="data parl-members">
        <thead><tr><th>${L('Nom', 'Name')}</th><th>${L('Groupe', 'Group')}</th>${ch === 'an' ? html`<th>${L('Parti de rattachement', 'Party')}</th>` : ''}<th>${L('Circonscription', 'Constituency')}</th><th>${L('Région', 'Region')}</th></tr></thead>
        <tbody>${rows.map((m) => {
          const g = byId.get(m.g);
          const role = roleOf(m, ch, g);
          return html`<tr data-q="${fold([m.n, g.short, g.name, m.p, m.depName, m.reg].join(' '))}">
            <td><b>${m.n}</b>${role ? html`<div class="tiny faint">${role}</div>` : ''}</td>
            <td>${swatch(g, 12)} ${g.short}${m.app ? html` <span class="faint">(${attachment(m)})</span>` : ''}</td>
            ${ch === 'an' ? html`<td>${m.p || '—'}</td>` : ''}
            <td>${placeOf(m)}</td><td>${m.reg || '—'}</td></tr>`;
        })}</tbody>
      </table></div>
    </div>
  </details>`;
}

const INTRO = {
  an: () => L(
    'Les 577 députés sont élus au suffrage universel direct, un par circonscription, pour cinq ans au plus (le président de la République peut dissoudre l’Assemblée). L’Assemblée vote la loi, contrôle le gouvernement et peut le renverser par une motion de censure ; elle a le dernier mot quand les deux chambres ne s’accordent pas.',
    'The 577 deputies are elected by direct popular vote, one per constituency, for up to five years (the President can dissolve the Assembly). The Assembly passes laws, oversees the government and can bring it down with a motion of censure; it has the last word when the two chambers disagree.',
  ),
  senat: () => L(
    'Les 348 sénateurs sont élus au suffrage universel indirect, par des grands électeurs qui sont surtout des élus locaux, pour six ans ; le Sénat est renouvelé par moitié tous les trois ans. Il vote la loi et contrôle le gouvernement, mais ne peut pas le renverser, et représente les collectivités territoriales.',
    'The 348 senators are elected indirectly, by electors who are mostly local officials, for six years; half the Senate is renewed every three years. It passes laws and oversees the government but cannot bring it down, and it represents local governments.',
  ),
};

export const parlement = {
  title: () => L('Parlement français', 'French Parliament'),
  async render(ctx) {
    const data = await loadParliament();
    if (!data) return html`<div class="wrap page"><div class="empty"><h3>${L('Données indisponibles', 'Data unavailable')}</h3></div></div>`;
    const ch = ctx.query.chambre === 'senat' ? 'senat' : 'an';
    const chamber = data.chambers[ch];
    const groups = groupsOf(ch, chamber);
    const name = ch === 'an' ? L('Assemblée nationale', 'National Assembly') : L('Sénat', 'Senate');
    const tabs = [['an', L('Assemblée nationale', 'National Assembly')], ['senat', L('Sénat', 'Senate')]];
    const shown = [data.officials?.president, data.officials?.pm, data.chambers.an.president, data.chambers.senat.president]
      .filter((p) => p?.photo).map((p) => ({ name: p.name || p.n, photo: p.photo }));
    const sources = [...chamber.sources, ...(data.officials?.president ? [{ title: L('Wikidata (président de la République, Premier ministre)', 'Wikidata (President, Prime Minister)'), url: data.officials.president.source }] : [])];
    return html`<div class="wrap page stack-lg">
      <nav class="crumbs"><a href="#/fr">${L('France', 'France')}</a><span>/</span><span>${L('Parlement français', 'French Parliament')}</span></nav>
      <div><div class="eyebrow">${L('Parlement français', 'French Parliament')}</div>
        <h1 style="margin:6px 0 8px">${L('Qui siège au Parlement ?', 'Who sits in Parliament')}</h1>
        <p class="muted" style="margin:0">${L(
          `Le Parlement a deux chambres, l’Assemblée nationale et le Sénat. Chaque point est un siège, coloré selon le groupe de son occupant ; survolez-le ou touchez-le pour voir qui y siège. Données officielles des deux chambres, relues chaque jour ; mises à jour le ${fmtDay(data.updated)}.`,
          `Parliament has two chambers, the National Assembly and the Senate. Each dot is a seat, colored by its holder’s group; hover over or tap it to see who sits there. The chambers’ official data, reread every day; updated ${fmtDay(data.updated)}.`,
        )}</p></div>
      <nav class="seg big" aria-label="${L('Chambre', 'Chamber')}">${tabs.map(([k, label]) => html`<a href="#/fr/parlement${k === 'an' ? '' : '?chambre=senat'}" aria-current="${k === ch ? 'page' : 'false'}">${label}</a>`)}</nav>
      ${officials(data)}
      <section class="card stack">
        <div><h2 style="margin:0">${name}</h2><p class="small muted" style="margin:4px 0 0">${INTRO[ch]()}</p></div>
        <div id="parl-hemi"></div>
        <p class="tiny faint" style="margin:10px 0 0">${L(
          ch === 'an'
            ? 'Couleur : celle du parti auquel la plupart des membres du groupe sont rattachés ; gris quand ce parti n’a pas de couleur sur ce site. Les groupes de même couleur ont des formes différentes. Les groupes vont de gauche à droite selon leur place dans l’hémicycle.'
            : 'Couleur : celle du premier parti que cite la fiche Wikipédia du groupe ; gris quand ce parti n’a pas de couleur sur ce site. Les groupes de même couleur ont des formes différentes. Les groupes vont de gauche à droite selon leur positionnement déclaré.',
          ch === 'an'
            ? 'Color: the party most of the group’s members belong to; gray when that party has no color on this site. Groups sharing a color have different shapes. Groups run left to right by where they sit in the chamber.'
            : 'Color: the first party listed in the group’s Wikipedia infobox; gray when that party has no color on this site. Groups sharing a color have different shapes. Groups run left to right by their stated position.',
        )}</p>
        ${stats(ch, chamber, groups)}
        <p class="small muted" style="margin:0">${L(
          'Chaque groupe déclare s’il est d’opposition. Parmi les autres, le plus nombreux est dit majoritaire et les autres minoritaires ; aucun ne doit pour autant soutenir le gouvernement.',
          'Each group declares whether it is in opposition. Among the others, the largest is called the majority group and the rest minority groups; none is bound to support the government.',
        )}${ch === 'an' ? L(' Le parti de rattachement est celui que chaque député déclare chaque année pour le financement public des partis.', ' A deputy’s party is the one they declare each year for the public funding of parties.') : L(' Le Sénat publie les groupes de ses membres, pas leurs partis.', ' The Senate publishes its members’ groups, not their parties.')}</p>
      </section>
      ${membersList(ch, chamber, groups)}
      ${data.checks?.length ? html`<div class="notice warn">${icon.info()}<div><b>${L('Écarts entre les sources, à vérifier', 'Differences between sources, to be checked')}</b><ul style="margin:6px 0 0">${data.checks.map((c) => html`<li>${L(c.fr, c.en)}</li>`)}</ul></div></div>` : ''}
      <p class="tiny faint" style="margin:0">${L('Sources :', 'Sources:')} ${sources.map((s, i) => html`${i ? ' · ' : ''}<a href="${s.url}" target="_blank" rel="noopener noreferrer">${s.revid ? L(`Wikipédia : ${s.title}`, `French Wikipedia: ${s.title}`) : s.title}</a>`)}</p>
      ${shown.length ? html`<details class="card"><summary style="cursor:pointer;font-weight:650">${L('Crédits photo', 'Photo credits')}</summary>
        <ul class="small" style="margin:10px 0 0">${shown.map((p) => html`<li>${p.name} : ${p.photo.artist || L('auteur inconnu', 'unknown author')}, ${p.photo.license || ''} — <a href="${p.photo.page}" target="_blank" rel="noopener noreferrer">Wikimedia Commons</a></li>`)}</ul>
        <p class="tiny faint" style="margin:8px 0 0">${L('Photos affichées en noir et blanc. Elles viennent de Wikidata et de Wikimedia Commons, sous les licences indiquées.', 'Photos are shown in black and white. They come from Wikidata and Wikimedia Commons, under the licenses shown.')}</p>
      </details>` : ''}
    </div>`;
  },
  async mount(root, ctx) {
    const data = await loadParliament();
    const host = root.querySelector('#parl-hemi');
    if (!data || !host) return null;
    const ch = ctx.query.chambre === 'senat' ? 'senat' : 'an';
    const chamber = data.chambers[ch];
    const groups = groupsOf(ch, chamber);
    const byId = new Map(groups.map((g) => [g.id, g]));
    const vacant = chamber.seats - chamber.members.length;
    const name = ch === 'an' ? L('Assemblée nationale', 'National Assembly') : L('Sénat', 'Senate');
    const chart = drawHemicycle(host, {
      seats: chamber.seats,
      groups,
      members: chamber.members,
      tipFor: (m) => tip(m, ch, byId.get(m.g)),
      vacantTip: html`<div class="tt-title">${L('Siège vacant', 'Vacant seat')}</div>`,
      ariaLabel: L(
        `${name} : ${chamber.seats} sièges. ${groups.map((g) => `${g.short} ${g.seats}`).join(', ')}${vacant > 0 ? `, ${vacant} vacants` : ''}.`,
        `${name}: ${chamber.seats} seats. ${groups.map((g) => `${g.short} ${g.seats}`).join(', ')}${vacant > 0 ? `, ${vacant} vacant` : ''}.`,
      ),
      hint: L(
        'Survolez ou touchez un siège pour voir qui l’occupe. Au clavier : flèches pour passer d’un siège à l’autre, Page suivante et Page précédente pour changer de groupe.',
        'Hover over or tap a seat to see who holds it. With the keyboard: arrow keys move from seat to seat, Page Down and Page Up jump between groups.',
      ),
      center: [String(chamber.seats), seatsWord(chamber.seats), L(`majorité absolue : ${chamber.majority}`, `majority: ${chamber.majority}`)],
      legendItem: (g) => keyItem(g, chamber.members),
      legendLabel: L('Légende : groupes politiques', 'Key: political groups'),
    });

    const find = root.querySelector('#parl-find');
    const count = root.querySelector('#parl-count');
    const rows = [...root.querySelectorAll('#parl-list tbody tr')];
    find?.addEventListener('input', () => {
      const q = fold(find.value.trim());
      let n = 0;
      for (const r of rows) {
        const hit = !q || r.dataset.q.includes(q);
        r.hidden = !hit;
        if (hit) n += 1;
      }
      count.textContent = q ? L(`${n} résultat${n > 1 ? 's' : ''}`, `${n} result${n === 1 ? '' : 's'}`) : '';
    });
    return () => chart.destroy();
  },
};
