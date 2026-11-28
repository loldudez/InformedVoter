// What the 2026 winners raised (#/money): every Senate and House race called so far, each
// winner's campaign money by the lines of their FEC filing (owner's request, Nov. 4: "keep
// a view of how much in fundraising ... for those who have been elected"). Each bar splits
// one winner's total by source, full width: on one scale, a $146 million Senate campaign
// left most House winners' bars a few pixels long. The amount is printed beside it, and a
// winner whose figures aren't loaded says so. Unlinked since Nov. 27 (owner's request: the
// money belongs on each politician's card, js/components/person.js); old links still work.

import { html, raw, fmtMoney, fmtPct, fmtDate, pctSign } from '../util.js';
import { icon } from '../icons.js';
import { mainRaces, resultWinners, resultRows, financeOf, hasFigures, raceTitle, fc, certPending } from '../data/world.js';
import { FUNDING_PARTS, FUND_FR, fundColor, candBadge, photoCredits, lastName } from '../components/race.js';
import { candColors } from '../lib/charts.js';
import { L, lang } from '../i18n.js';

const CHAMBERS = { all: ['Les deux chambres', 'Both chambers'], senate: ['Sénat', 'Senate'], house: ['Chambre', 'House'] };
const PARTIES = { all: ['Tous les partis', 'All parties'], D: ['Démocrates', 'Democrats'], R: ['Républicains', 'Republicans'], I: ['Indépendants et autres', 'Independents and others'] };
const SORTS = {
  total: ['Les plus gros montants', 'Most raised'],
  small: ['Part des petits dons', 'Share from small donors'],
  pac: ['Part des PAC', 'Share from PACs'],
  self: ['Part des fonds personnels', 'Share self-funded'],
};
const SHARE_OF = { small: ['de petits dons', 'from small donors'], pac: ['des PAC', 'from PACs'], self: ['de fonds personnels', 'self-funded'] };

const pick = (o, k, d) => (Object.hasOwn(o, k || '') ? k : d);
const partyKey = (p) => (p === 'D' || p === 'R' ? p : 'I');
const partyText = (p) => (p === 'D' ? 'd-text' : p === 'R' ? 'r-text' : 'faint');
const share = (fin, k) => (fin.total > 0 ? ((fin.parts?.[k] || 0) / fin.total) * 100 : 0);
const mode = (xs) => {
  const n = new Map();
  xs.forEach((x) => n.set(x, (n.get(x) || 0) + 1));
  return [...n].sort((a, b) => b[1] - a[1])[0]?.[0] || null;
};

// Called races only: a runoff or a count still going has no winner to list yet.
function winners() {
  const out = [], open = [];
  for (const r of mainRaces()) {
    if ((r.office !== 'senate' && r.office !== 'house') || r.state === 'DC' || r.demo) continue;
    if (r.result?.status !== 'won') { open.push(r); continue; }
    for (const c of resultWinners(r)) out.push({ c, race: r, fin: financeOf(c) });
  }
  return { out, open };
}

// The runner-up in the count, or the forecast's main opponent where no count is posted.
function opponent(race, c) {
  const row = resultRows(race).find((r) => !r.other && r.cand && r.cand.id !== c.id);
  if (row) return row.cand;
  const f = fc(race);
  return [f.lead, f.second].find((x) => x && x.id !== c.id) || null;
}

export const money = {
  live: true, // redrawn when a race is called (main.js)
  title: () => L('Ce qu’ont levé les élus', 'What the winners raised'),
  render(ctx) {
    const chamber = pick(CHAMBERS, ctx.query.chamber, 'all');
    const party = pick(PARTIES, ctx.query.party, 'all');
    const sort = pick(SORTS, ctx.query.sort, 'total');
    const { out, open } = winners();
    const inView = (x) => (chamber === 'all' || x.race.office === chamber) && (party === 'all' || partyKey(x.c.party) === party);
    const rows = out.filter(inView);
    const have = rows.filter((x) => hasFigures(x.fin));
    const missing = rows.filter((x) => !hasFigures(x.fin));
    const metric = (x) => (sort === 'total' ? x.fin.total : share(x.fin, sort));
    have.sort((a, b) => metric(b) - metric(a) || b.fin.total - a.fin.total || a.c.name.localeCompare(b.c.name));
    const sum = have.reduce((s, x) => s + x.fin.total, 0);
    const part = (k) => have.reduce((s, x) => s + (x.fin.parts?.[k] || 0), 0);
    const totals = have.map((x) => x.fin.total).sort((a, b) => a - b);
    const mid = totals.length >> 1;
    const median = !totals.length ? null : totals.length % 2 ? totals[mid] : (totals[mid - 1] + totals[mid]) / 2;
    const asOf = mode(have.map((x) => x.fin.asOf).filter(Boolean));
    const openHere = open.filter((r) => chamber === 'all' || r.office === chamber);
    const parts = FUNDING_PARTS.map(([k, label], i) => ({ k, name: lang() === 'fr' ? FUND_FR[k] : label, color: fundColor(i) }));
    const used = parts.filter((p) => part(p.k) > 0);

    const q = { chamber, party, sort };
    const href = (k, v) => `#/money?${new URLSearchParams({ ...q, [k]: v })}`;
    const chips = (k, opts, cur, label) => html`<div class="filters" role="group" aria-label="${label}">${Object.entries(opts).map(([v, [fr, en]]) => html`<a class="chip" href="${href(k, v)}" ${raw(v === cur ? 'aria-current="page" style="background:var(--text-1);color:var(--bg);border-color:var(--text-1)"' : '')}>${L(fr, en)}</a>`)}</div>`;
    const pctOf = (v) => (!sum ? '—' : v > 0 && v / sum < 0.005 ? `<1${pctSign()}` : fmtPct((v / sum) * 100, 0));

    const row = (x, i) => {
      const { c, race, fin } = x;
      const segs = parts.map((p) => ({ ...p, v: fin.parts?.[p.k] || 0 })).filter((p) => p.v > 0);
      const o = opponent(race, c);
      const of = o && financeOf(o);
      const tip = (p) => `${p.name}${L(' : ', ': ')}${fmtMoney(p.v)} (${fmtPct((p.v / fin.total) * 100, 0)})`;
      const extra = [
        sort !== 'total' ? `${fmtPct(share(fin, sort), 0)} ${L(...SHARE_OF[sort])}` : '',
        o && hasFigures(of) ? L(`face à ${fmtMoney(of.total)} pour ${lastName(o.name)}`, `vs. ${fmtMoney(of.total)} for ${lastName(o.name)}`) : '',
      ].filter(Boolean).join(' · ');
      return html`<li class="money-row">
        <span class="rank">${i + 1}</span>
        <div class="who">${candBadge(c, candColors(fc(race).cands)[c.id])}<div><a href="#/race/${encodeURIComponent(race.id)}"><b>${c.name}</b></a> <span class="${partyText(c.party)}">(${c.party})</span><span class="tiny faint">${raceTitle(race)}</span></div></div>
        <span class="amt">${fmtMoney(fin.total)}</span>
        <div class="bar">
          ${segs.length ? html`<div class="stackbar" role="img" aria-label="${segs.map(tip).join(', ')}">${segs.map((p) => html`<span style="flex:${p.v} 1 0;background:${p.color}" title="${tip(p)}"></span>`)}</div>`
            : html`<span class="tiny faint">${L('Pas de détail par type de donateur', 'No breakdown by type of donor')}</span>`}
          ${extra ? html`<span class="tiny faint">${extra}</span>` : ''}
        </div>
      </li>`;
    };

    return html`<div class="wrap page stack" style="max-width:1040px">
      <div><div class="eyebrow">${L('Campagnes de 2026 : argent levé', '2026 campaign money')}</div><h1>${L('Ce qu’ont levé les élus', 'What the winners raised')}</h1>
        <p class="muted" style="margin:0">${lang() === 'fr'
          ? 'Ce que chaque personne élue au Sénat et à la Chambre le 3 novembre 2026 a levé pour sa campagne, ligne par ligne d’après ses déclarations à la Commission électorale fédérale (FEC) : petits dons (moins de 200 $), gros dons individuels, PAC, comités du parti, fonds personnels, transferts des comités de collecte conjoints et des autres campagnes, et autres recettes. Les entreprises ne peuvent pas donner directement aux candidats fédéraux : leur argent apparaît sous les PAC. Les dépenses extérieures des super PAC sont déclarées à part et ne sont pas comptées ici.'
          : 'How much each person elected to the Senate and the House on Nov. 3, 2026 raised for their campaign, line by line from their filings with the Federal Election Commission: small donors (under $200), large donors, PACs, party committees, their own money, transfers from joint fundraising committees and other campaigns, and other receipts. Corporations can’t give directly to federal candidates, so business money shows up under PACs. Super PACs’ outside spending is reported separately and isn’t counted here.'}</p></div>
      <div class="stack-sm">
        ${chips('chamber', CHAMBERS, chamber, L('Chambre', 'Chamber'))}
        ${chips('party', PARTIES, party, L('Parti', 'Party'))}
        ${chips('sort', SORTS, sort, L('Trier', 'Sort'))}
      </div>
      <div class="grid grid-4">
        <div class="stat"><div class="eyebrow">${L('Total levé', 'Total raised')}</div><div class="value">${fmtMoney(sum)}</div><div class="sub">${L(`par ${have.length} personne${have.length > 1 ? 's' : ''} élue${have.length > 1 ? 's' : ''}`, `by ${have.length} winner${have.length === 1 ? '' : 's'}`)}</div></div>
        <div class="stat"><div class="eyebrow">${L('Montant médian', 'Median winner')}</div><div class="value">${median != null ? fmtMoney(median) : '—'}</div><div class="sub">${L('la moitié a levé davantage', 'half raised more')}</div></div>
        <div class="stat"><div class="eyebrow">${L('Petits dons', 'Small donors')}</div><div class="value">${pctOf(part('small'))}</div><div class="sub">${L('du total, moins de 200 $ par don', 'of the total, under $200 a gift')}</div></div>
        <div class="stat"><div class="eyebrow">${L('PAC', 'PACs')}</div><div class="value">${pctOf(part('pac'))}</div><div class="sub">${L('du total', 'of the total')}</div></div>
      </div>
      ${have.length ? html`<section class="card stack-sm">
        <ul class="money-key" aria-label="${L('Sources de financement', 'Funding sources')}">${used.map((p) => html`<li><i class="key-box" style="background:${p.color}"></i><span>${p.name}</span><b>${pctOf(part(p.k))}</b></li>`)}</ul>
        <ol class="money-list">${have.map(row)}</ol>
        <p class="tiny faint" style="margin:0">${L(`Déclarations à la FEC${asOf ? ` jusqu’au ${fmtDate(asOf)}` : ''} ; les rapports postélectoraux, attendus le 3 décembre, ajouteront les dernières semaines de campagne. Chaque barre répartit le total d’une personne élue entre ses sources ; survolez une couleur pour son montant.`, `FEC filings${asOf ? ` through ${fmtDate(asOf)}` : ''}; the post-general reports, due Dec. 3, will add the campaigns’ final weeks. Each bar splits one winner’s total by source; hover over a color for its amount.`)}</p>
      </section>` : html`<div class="empty">${icon.dollar()}<h3>${L('Personne à montrer', 'No one to show')}</h3><p>${L('Aucune élection attribuée ne correspond à ces choix.', 'No called race matches these choices.')}</p></div>`}
      ${missing.length ? html`<p class="small muted" style="margin:0">${L('Chiffres pas encore chargés : ', 'Figures not loaded yet: ')}${missing.map((x, i) => html`${i ? ', ' : ''}<a href="#/race/${encodeURIComponent(x.race.id)}">${x.c.name}</a>`)}.</p>` : ''}
      ${openHere.length ? html`<p class="small muted" style="margin:0">${L('Pas encore attribuées, donc pas listées : ', 'Not called yet, so not listed: ')}${openHere.map((r, i) => html`${i ? ', ' : ''}<a href="#/race/${encodeURIComponent(r.id)}">${raceTitle(r)}</a> (${r.result?.status === 'runoff' ? L(`second tour${r.runoff ? ` le ${fmtDate(r.runoff)}` : ''}`, `runoff${r.runoff ? ` on ${fmtDate(r.runoff)}` : ''}`) : certPending(r) === 'recount' ? L('recompte', 'recount') : L('dépouillement', 'counting')})`)}.</p>` : ''}
      ${photoCredits(have.map((x) => x.c))}
    </div>`;
  },
};
