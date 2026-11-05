// "My elections": the races on the visitor's ballot, matching against their views,
// and the similarities / differences / unclear breakdown for each candidate.

import { html, fmtPct, fmtProb, fmtDate, fmtDR } from '../util.js';
import { icon } from '../icons.js';
import { store } from '../store.js';
import { STATE_BY_ABBR, legislatureChambers, ELECTION_DATE_LABEL } from '../data/states.js';
import { questionsForLevel, stanceSentence, userSentence } from '../data/questions.js';
import { fc, statewideRaces, officeRaces, getRace, legislativeRaces, ensureRace, raceTitle, officeLabel, positionsOf, isDemo, afterElection, resultRows, rowShare } from '../data/world.js';
import { rank, MIN_COMPARED } from '../model/match.js';
import { howToVote } from '../components/vote.js';
import { reminderButton } from '../components/reminders.js';
import { PARTY_NAME, partyClass, heartBtn, starBtn, demoChip, dataChip, lastName, ratingChip, candBadge, photoCredits, resultChip, raceColors, awaitingResult } from '../components/race.js';

async function ballotFor(ad) {
  const st = ad.state;
  const s = STATE_BY_ABBR[st];
  const items = [];
  const { senate, governor } = statewideRaces(st);
  if (senate) items.push({ race: senate });
  if (governor) items.push({ race: governor });
  // Attorney general, secretary of state, lieutenant governor, treasurer, auditor.
  for (const race of officeRaces(st)) items.push({ race });
  const cd = st === 'DC' ? '98' : ad.cd;
  const house = cd && getRace(`${st}-H-${cd}`);
  if (house) items.push({ race: house });
  for (const ch of legislatureChambers(st)) {
    const code = ch.layer === 'sldu' ? ad.sldu : ad.sldl;
    if (!code) continue;
    if (ch.up === 'none') { items.push({ none: `${s.name} ${ch.name}`, why: `${ch.name} seats are not on the ballot in 2026.` }); continue; }
    const data = await legislativeRaces(st, ch.key);
    const race = data?.races.get(code);
    if (race) items.push({ race });
    else items.push({ none: `${ch.name}, District ${code.replace(/^0+/, '')}`, why: 'Your district’s seat is not up this year (staggered terms).' });
  }
  return items;
}

function raceCard(race) {
  const f = fc(race);
  const colors = raceColors(race);
  const mine = store.get().electionAnswers[race.id];
  const answered = store.answered();
  const id = encodeURIComponent(race.id);
  const res = race.result;
  // With a count in, candidates in its order with their shares. After Election Day
  // without one, the winner (if called) first and no percentages, since the forecast's
  // or the polls' would read as results. Before it, the forecast's order and shares.
  const awaiting = awaitingResult(race);
  const rows = resultRows(race).filter((r) => r.cand);
  const byRow = new Map(rows.map((r) => [r.cand.id, r]));
  const winners = new Set(res?.winners || []), adv = new Set(res?.advance || []);
  const ahead = (c) => (winners.has(c.id) || adv.has(c.id) ? 1 : 0);
  const cands = rows.length ? [...rows.map((r) => f.cands.find((c) => c.id === r.cand.id) || r.cand), ...f.cands.filter((c) => !byRow.has(c.id))]
    : res ? [...f.cands].sort((a, b) => ahead(b) - ahead(a)) : f.cands;
  const office = f.kind === 'office';
  const rated = f.rating && f.rating !== 'Not rated';
  const s = STATE_BY_ABBR[race.state];
  const wonBy = (c) => (byRow.has(c.id) ? byRow.get(c.id).won : winners.has(c.id));
  const sub = (c) => {
    const r = byRow.get(c.id);
    if (r || res || awaiting) {
      const toRunoff = r ? r.advance : adv.has(c.id);
      return html`${wonBy(c) ? html`<span class="win-mark">${icon.check()} Winner</span> · ` : toRunoff ? 'To the runoff · ' : ''}${PARTY_NAME[c.party] || c.party}${c.incumbent && office ? ' · incumbent' : ''}${r?.votes != null ? ` · ${r.votes.toLocaleString('en-US')} votes` : ''}`;
    }
    return html`${PARTY_NAME[c.party] || c.party}${c.incumbent && office ? ' · incumbent' : ''}${f.open ? '' : ` · ${fmtProb(c.win)} to win`}`;
  };
  const share = (c) => {
    const r = byRow.get(c.id);
    if (r) return rowShare(r);
    return rows.length || res || awaiting ? null : c.share;
  };
  const link = res ? 'Full results' : office || f.open ? 'Race details' : awaiting ? 'Race page' : 'Full forecast';
  const pending = !rows.length && (res || awaiting)
    ? (res?.status === 'won' ? 'Called; the vote count isn’t posted yet.' : res?.status === 'runoff' ? 'Headed to a runoff; the vote count isn’t posted yet.' : res ? 'Votes are being counted.' : 'No result yet.')
    : '';
  return html`<article class="card stack">
    <div class="row between">
      <div><div class="eyebrow">${office ? `Statewide · ${officeLabel(race)}` : officeLabel(race)}</div><h3 style="margin:2px 0 0;font-size:19px">${raceTitle(race)}</h3></div>
      <div class="row">${dataChip(race)}${res || awaiting ? resultChip(race) : !office || rated ? ratingChip(f) : ''}${starBtn(race.id, { small: true })}</div>
    </div>
    ${f.kind === 'field' ? html`<p class="small muted" style="margin:0">No forecast for state legislative races. ${f.cands.length ? '' : 'Wikipedia doesn’t list this district’s candidates yet. '}${f.dr != null ? `The district voted ${fmtDR(f.dr)} for president in 2024.` : ''}</p>` : ''}
    ${office ? html`<p class="small muted" style="margin:0">No forecast for statewide offices below governor${rated ? `; Sabato’s Crystal Ball rated it ${f.rating}` : ''}.${f.dr != null ? ` ${s.name} voted ${fmtDR(f.dr)} for president in 2024.` : ''}${rows.length ? ' Vote counts are unofficial until the state certifies them.' : pending ? ` ${pending}` : f.poll ? ' Percentages are the polling average.' : ''}</p>` : ''}
    ${f.open && f.kind === 'open-primary' ? html`<p class="small muted" style="margin:0">Open primary: all ${f.cands.length} candidates share${res || awaiting ? 'd' : ''} one ballot. A majority wins outright; otherwise the top two meet in a runoff${race.runoff ? ` on ${fmtDate(race.runoff + 'T12:00:00')}` : ''}. ${rows.length ? 'Percentages are the unofficial count.' : pending || 'Percentages are from the latest published poll.'}</p>` : ''}
    ${rows.length && !office && !f.open ? html`<p class="small muted" style="margin:0">Unofficial count${res.status === 'won' ? '; the race has been called' : res.status === 'runoff' ? '; the race goes to a runoff' : '; not called yet'}. The final forecast is on the race’s page.</p>` : ''}
    ${pending && !office && !f.open ? html`<p class="small muted" style="margin:0">${pending} The final forecast is on the race’s page.</p>` : ''}
    <div class="grid grid-2" style="gap:10px">${cands.map((c) => html`<div class="compact-cand ${partyClass(c.party)}${wonBy(c) ? ' winner' : ''}">
      ${candBadge(c, colors[c.id])}
      <div style="min-width:0"><div class="nm">${c.name}</div><div class="tiny faint">${sub(c)}</div></div>
      ${share(c) != null ? html`<div class="sh" style="color:${colors[c.id]};font-size:18px">${fmtPct(share(c), rows.length ? 1 : 0)}</div>` : ''}
      ${heartBtn(c.id, c.name, { small: true })}
    </div>`)}</div>
    ${!isDemo(race) && !race.research ? html`<p class="small muted" style="margin:0">${icon.info()} ${f.kind === 'field'
      ? html`The candidates here come from Wikipedia’s 2026 page for this chamber; their issue positions haven’t been researched, so matching isn’t available. <a href="#/race/${id}">See the race</a>.`
      : office
        ? html`${race.candidates.some((c) => Object.keys(c.positions || {}).length) ? 'Some of these candidates’ positions are researched, but not every candidate’s yet' : 'These candidates’ issue positions haven’t been researched yet'}, so matching isn’t available for this race. <a href="#/race/${id}">See the candidates and results</a>.`
        : html`Candidates, ratings, polls and money here are live, but not every candidate’s issue positions have been researched yet, so matching isn’t available for this race. <a href="#/race/${id}">See the ${res ? 'results' : awaiting ? 'race' : 'full forecast'}</a>.`}</p>` : html`<div class="row">
      ${answered >= MIN_COMPARED
        ? html`<a class="btn btn-sm btn-primary" href="#/elections/${id}/match?mode=profile">${icon.user()} Match with My views</a>`
        : html`<a class="btn btn-sm" href="#/views" title="Answer at least ${MIN_COMPARED} questions first">${icon.user()} Answer My views first</a>`}
      <a class="btn btn-sm" href="#/elections/${id}/quiz">New political views for this election</a>
      ${mine && store.answered(mine) ? html`<a class="btn btn-sm btn-ghost" href="#/elections/${id}/match?mode=election">My results for this election</a>` : ''}
      <a class="btn btn-sm btn-ghost" href="#/race/${id}">${link}</a>
    </div>`}
  </article>`;
}

export const elections = {
  live: true, // redrawn when new counts arrive (main.js)
  title: () => 'My elections',
  rerenderOn: ['reminders'],
  async render() {
    const ad = store.get().address;
    if (!ad || !ad.state) {
      return html`<div class="wrap page" style="max-width:860px">
        <div class="eyebrow">My elections</div><h1>Your ballot, from your address</h1>
        <div class="empty">${icon.pin()}<h3>Add your address to see your elections</h3><p>We use the U.S. Census Bureau’s geocoder to find your exact districts. Your address stays in this browser.</p><a class="btn btn-primary" href="#/profile?tab=location">Add my address</a></div>
      </div>`;
    }
    const items = await ballotFor(ad);
    const s = STATE_BY_ABBR[ad.state];
    const over = afterElection();
    // A runoff reminder only for a race of the visitor's that is going to one (or, before
    // the results, could), and only while the date is ahead.
    const today = new Date().toISOString().slice(0, 10);
    const runoff = items.map((it) => it.race).filter((r) => r?.runoff && r.runoff >= today && (!r.result || r.result.status === 'runoff')).map((r) => r.runoff)[0];
    return html`<div class="wrap page stack-lg" style="max-width:1000px">
      <div class="row between" style="align-items:flex-end">
        <div>
          <div class="eyebrow">My elections · ${ELECTION_DATE_LABEL}</div>
          <h1 style="margin:6px 0 8px">${over ? 'Your 2026 races and results' : 'What’s on your ballot'}</h1>
          <p class="muted" style="margin:0">${icon.pin()} ${ad.matched} · <a href="#/profile?tab=location">Change</a></p>
        </div>
        <div class="row">${over ? '' : reminderButton({ id: 'us:general-2026', name: 'Election Day, November 3, 2026', date: '2026-11-03', section: 'us' })}
          ${runoff ? reminderButton({ id: `us:runoff-${ad.state}-${runoff}`, name: `${s.name} runoff`, date: runoff, section: 'us' }) : ''}</div>
      </div>
      ${over ? html`<div class="notice">${icon.info()}<div>Results are unofficial until ${s.name} certifies them. A race shows a winner once Wikipedia’s national results table marks one; each race’s page has the full count, its source and the final forecast. Click a race below for its candidates, where they stand and the results.</div></div>` : ''}
      ${isDemo(items.find((x) => x.race)?.race) ? html`<div class="notice warn">${icon.info()}<div>The offices and districts below are your real 2026 races. The candidates, forecasts and positions are <b>demo data</b> until real candidate data is connected. Always confirm your sample ballot with ${s.name}’s election office.</div></div>` : ''}
      <div class="stack">${items.map((it) => (it.race ? raceCard(it.race) : html`<div class="card tight"><div class="row between"><b>${it.none}</b><span class="chip">No election this year</span></div><p class="small muted" style="margin:6px 0 0">${it.why}</p></div>`))}</div>
      ${howToVote(ad.state)}
      ${photoCredits(items.flatMap((it) => (it.race ? fc(it.race).cands : [])))}
    </div>`;
  },
};

// Ranking + three-panel breakdown --------------------------------------------------

function sourceLink(src) {
  if (!src) return '';
  if (src.url) return html`<a class="src-link" href="${src.url}" target="_blank" rel="noopener noreferrer" title="${src.title}">source ${icon.external()}</a>`;
  return html`<button type="button" class="src-link" title="Demo source: in the live site this links to the candidate’s own statement, vote or questionnaire.">demo source</button>`;
}

function evidence(item, cand) {
  const who = lastName(cand.name);
  return html`<div class="evidence">
    <div class="q">${item.q.text}</div>
    <div class="muted">Based on ${item.source?.title || 'a documented statement'}${item.source?.date ? `, ${item.source.accessed ? 'accessed ' : ''}${fmtDate(item.source.date)}` : ''}, ${stanceSentence(who, item.q, item.stance)}.${item.source?.quote ? html` <span class="quote">“${item.source.quote}”</span>` : ''} ${userSentence(item.q, item.user)} ${sourceLink(item.source)}</div>
  </div>`;
}

function overlay(row, race) {
  const c = row.cand;
  const colors = raceColors(race);
  return html`<div class="overlay" role="dialog" aria-modal="true" aria-label="${c.name}: similarities and differences">
    <section class="panel p-left"><h3><span class="sim-dot"></span> Similarities <span class="faint small">(${row.similarities.length})</span></h3>
      ${row.similarities.length ? row.similarities.map((it) => evidence(it, c)) : html`<p class="muted small">No issues where you and ${lastName(c.name)} line up.</p>`}</section>
    <section class="panel p-center">
      <button type="button" class="toggle-icon close-x" data-close aria-label="Close">${icon.close()}</button>
      ${candBadge(c, colors[c.id], 'width:64px;height:64px;font-size:22px;margin:4px auto 10px;border-radius:18px')}
      <h2 style="margin:0">${c.name}</h2>
      <div class="cand-party" style="margin-bottom:10px">${PARTY_NAME[c.party] || c.party}${isDemo(c) ? ' · demo' : ''}</div>
      <div style="font-size:52px;font-weight:800;letter-spacing:-.03em;line-height:1">${row.score == null ? '—' : `${row.score}%`}</div>
      <div class="small muted">${row.score == null ? 'Not enough documented positions to score' : 'similar to you'}</div>
      <p class="small faint" style="margin:10px 0 0">Compared on ${row.compared} of the ${row.userAnswered} issues you answered.</p>
      <div class="row" style="justify-content:center;margin-top:12px">${heartBtn(c.id, c.name)}</div>
    </section>
    <section class="panel p-right"><h3><span class="dif-dot"></span> Differences <span class="faint small">(${row.differences.length})</span></h3>
      ${row.differences.length ? row.differences.map((it) => evidence(it, c)) : html`<p class="muted small">No documented disagreements with ${lastName(c.name)}.</p>`}</section>
    <section class="panel p-bottom"><h3><span class="unc-dot"></span> Unclear / no stated position <span class="faint small">(${row.unclear.length})</span></h3>
      <p class="small muted" style="margin-top:0">${lastName(c.name)} hasn’t taken a clear public position on these, so they are left out of the score rather than guessed.</p>
      <div class="answer-list">${row.unclear.map((it) => html`<div class="answer-row"><span>${it.q.text}</span><span class="answer-tag">No clear position</span></div>`)}</div></section>
  </div>`;
}

export const match = {
  title: () => 'Candidate match',
  async render(ctx) {
    const race = await ensureRace(decodeURIComponent(ctx.params[0]));
    if (!race) return html`<div class="wrap page"><p>Race not found. <a href="#/elections">Back to my elections</a></p></div>`;
    const mode = ctx.query.mode === 'election' ? 'election' : 'profile';
    const answers = mode === 'election' ? store.get().electionAnswers[race.id] || {} : store.get().answers;
    const qids = questionsForLevel(race.level).map((q) => q.id);
    const answeredHere = qids.filter((id) => answers[id] != null && answers[id] !== 'skip').length;
    const id = encodeURIComponent(race.id);
    if (answeredHere < MIN_COMPARED) {
      return html`<div class="wrap page" style="max-width:820px"><nav class="crumbs"><a href="#/elections">My elections</a><span>/</span><span>${raceTitle(race)}</span></nav>
        <div class="empty">${icon.user()}<h3>Answer a few more questions first</h3><p>You’ve answered ${answeredHere} question${answeredHere === 1 ? '' : 's'} that apply to this race. At least ${MIN_COMPARED} are needed for a fair comparison.</p>
        <a class="btn btn-primary" href="${mode === 'election' ? `#/elections/${id}/quiz` : '#/views'}">Answer questions</a></div></div>`;
    }
    const ranked = rank(answers, fc(race).cands, positionsOf, qids);
    const colors = raceColors(race);
    return html`<div class="wrap page stack" style="max-width:920px">
      <nav class="crumbs"><a href="#/elections">My elections</a><span>/</span><span>${raceTitle(race)}</span></nav>
      <div><div class="eyebrow">Similarity ranking</div><h1 style="font-size:clamp(28px,3.6vw,42px);margin:6px 0 8px">Who matches you in ${raceTitle(race)}?</h1>
        <p class="muted">Using ${mode === 'election' ? 'the views you gave for this election' : 'your saved My views'} (${answeredHere} answers). Click a candidate to see where you agree, where you differ, and what’s unclear.</p></div>
      ${isDemo(race) ? html`<div class="notice warn">${icon.info()}<div>These candidates and their positions are <b>demo data</b>, so this ranking only shows how matching works.</div></div>` : ''}
      <div class="match-list">${ranked.map((row, i) => html`<button type="button" class="match-row" data-cand="${row.cand.id}">
        <span class="rank">${i + 1}</span>
        <span style="min-width:0"><span class="row" style="gap:8px">${candBadge(row.cand, colors[row.cand.id], 'width:30px;height:30px;font-size:11px;border-radius:8px')}<b>${row.cand.name}</b></span><span class="tiny faint">${PARTY_NAME[row.cand.party] || row.cand.party} · compared on ${row.compared} of ${row.userAnswered} issues</span></span>
        <span class="meter"><span style="width:${row.score ?? 0}%"></span></span>
        <span class="pct">${row.score == null ? '—' : `${row.score}%`}</span>
      </button>`)}</div>
      <p class="small faint">How the score works: each issue scores 100% for identical answers down to 0% for opposite extremes, averaged over issues where the candidate’s position is documented. A candidate needs at least ${MIN_COMPARED} documented positions to get a score.</p>
      <div class="row"><a class="btn btn-sm" href="#/elections/${id}/quiz">Answer differently for this election</a><a class="btn btn-sm btn-ghost" href="#/race/${id}">${race.result ? 'Full results' : race.format === 'office' || fc(race).open ? 'Race details' : 'Full forecast'}</a></div>
      ${photoCredits(ranked.map((row) => row.cand))}
    </div>`;
  },
  async mount(root, ctx) {
    const race = await ensureRace(decodeURIComponent(ctx.params[0]));
    if (!race) return;
    const mode = ctx.query.mode === 'election' ? 'election' : 'profile';
    const answers = mode === 'election' ? store.get().electionAnswers[race.id] || {} : store.get().answers;
    const qids = questionsForLevel(race.level).map((q) => q.id);
    const ranked = rank(answers, fc(race).cands, positionsOf, qids);
    const slot = document.getElementById('overlay-root');
    let lastFocus = null;
    const close = () => {
      slot.innerHTML = '';
      document.body.style.overflow = '';
      document.removeEventListener('keydown', onKey);
      lastFocus?.focus();
    };
    const onKey = (e) => { if (e.key === 'Escape') close(); };
    root.querySelectorAll('[data-cand]').forEach((b) => b.addEventListener('click', () => {
      const row = ranked.find((r) => r.cand.id === b.dataset.cand);
      lastFocus = b;
      slot.innerHTML = String(overlay(row, race));
      document.body.style.overflow = 'hidden';
      document.addEventListener('keydown', onKey);
      const ov = slot.querySelector('.overlay');
      ov.addEventListener('click', (e) => { if (e.target === ov || e.target.closest('[data-close]')) close(); });
      slot.querySelector('[data-close]').focus();
    }));
    return close;
  },
};

// Profile -> Donations ---------------------------------------------------------------

// The campaign's own site, plus the processors campaigns use for their official
// donate pages (ActBlue, WinRed, Anedot). Anything else is refused.
const PROCESSORS = ['secure.actblue.com', 'secure.winred.com', 'secure.anedot.com'];
export function verifiedDonateUrl(c) {
  if (!c.donateUrl || !c.officialSite) return null;
  try {
    const u = new URL(c.donateUrl), site = new URL(c.officialSite);
    if (u.protocol !== 'https:') return null;
    const official = site.hostname.replace(/^www\./, '');
    const host = u.hostname;
    if (host === official || host.endsWith(`.${official}`) || PROCESSORS.includes(host)) return u.href;
  } catch { /* malformed */ }
  return null;
}
