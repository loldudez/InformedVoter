// One place the views ask for races, candidates, forecasts and results.
//
// Races start as the demo set. data/races.json (written every 8 hours by
// scripts/update_races.py, see DATA.md) replaces each demo race with the same id
// with real data. data/offices.json adds the statewide offices below governor
// (attorney general, secretary of state, lieutenant governor, treasurer, auditor),
// which have no demo stand-ins. data/control.json holds the chamber-control
// simulation and data/status.json the refresh's automatic checks.

import { STATES, STATE_BY_ABBR, HOLDOVER, CURRENT, legislatureChambers } from './states.js';
import * as demo from './demo.js';
import { forecast, history, chamberOdds, pollAverage, simEntry, day, live, forecastAsOf, ELECTION_DAY } from '../model/forecast.js';
import { fetchJSON } from '../util.js';
import { store } from '../store.js';

const races = new Map();
const candidates = new Map();
const aliases = new Map();   // old candidate id -> current id (e.g. LA-SEN:R -> LA-SEN:letlow)
const fcCache = new Map();
const liveCache = new Map();
const histCache = new Map();
const pollHistCache = new Map();
const layerCache = new Map();
const legCache = new Map();
let mapIndex = {};
let summaryCache = null;
let control = null;
let status = null;
let meta = null;
let photos = {};
export let realRaceCount = 0;
export let researchedCount = 0;
export let officeCount = 0;
export let officesResearched = 0;
export let modelCheck = null; // { checked, mismatches: [{id, expected, got}] }

function addRace(race) {
  races.set(race.id, race);
  for (const c of race.candidates) {
    candidates.set(c.id, { ...c, raceId: race.id });
    for (const a of c.aliases || []) aliases.set(a, c.id);
  }
  fcCache.delete(race.id);
  liveCache.delete(race.id);
  histCache.delete(race.id);
  pollHistCache.delete(race.id);
}

function normalizeReal(r) {
  const statewide = r.office === 'senate' || r.office === 'governor' || !!r.statewide;
  const cands = r.candidates.map((c) => ({ ...c, raceId: r.id, demo: false }));
  let prior = r.prior;
  if (!prior || cands.some((c) => prior[c.id] == null)) {
    // No baseline supplied: start from the state's recent lean.
    const lean = STATE_BY_ABBR[r.state]?.pres24 ?? 0;
    const d = cands.find((c) => c.party === 'D'), rep = cands.find((c) => c.party === 'R');
    prior = Object.fromEntries(cands.map((c) => [c.id, 100 / cands.length]));
    if (d && rep) {
      const rest = cands.length > 2 ? 4 : 0;
      cands.forEach((c) => { prior[c.id] = rest / Math.max(1, cands.length - 2); });
      prior[d.id] = (50 + lean / 2) * (1 - rest / 100);
      prior[rep.id] = (50 - lean / 2) * (1 - rest / 100);
    }
  }
  const earlyVote = r.earlyVote ? { ...r.earlyVote, demo: false } : null;
  return { ...r, statewide, candidates: cands, prior, polls: r.polls || [], earlyVote, demo: false, lean: r.lean ?? 0 };
}

const optional = (url) => fetchJSON(url).catch(() => null);

// State legislative races the refresh read from Wikipedia, one file per state
// (data/legislature/ST.json, see scripts/lib/legislature.py), loaded with the chamber map.
const legFiles = new Map();
function legFile(st) {
  if (!legFiles.has(st)) legFiles.set(st, optional(`data/legislature/${st}.json`));
  return legFiles.get(st);
}

// Races shown as a field with no win odds: open primaries, state legislative races
// and the statewide offices below governor.
const noOdds = (race) => race.format === 'open-primary' || race.format === 'field' || race.format === 'office';

export async function initWorld() {
  mapIndex = await fetchJSON('data/maps/index.json');
  demo.federalAndGovernor(mapIndex).forEach(addRace);
  const [real, ctl, st, ph, off] = await Promise.all([optional('data/races.json'), optional('data/control.json'), optional('data/status.json'), optional('data/photos.json'), optional('data/offices.json')]);
  photos = ph?.photos || {};
  loadRaces(real, off, ctl, st);
  loaded = true;
}

// While races are still being counted, scripts/update_results.py rewrites the race files
// every 10 minutes. Open pages ask for status.json on the same beat (main.js) and reload
// the races when it is newer than what they have. True when something changed.
let loaded = false;
const fresh = (url) => optional(`${url}?t=${Date.now()}`);
const stampOf = (st) => st?.resultsUpdated || st?.updated || null;
export async function refreshData() {
  if (!loaded) return false;
  const st = await fresh('data/status.json');
  if (!st || !stampOf(st) || stampOf(st) === stampOf(status)) return false;
  const [real, ctl, off] = await Promise.all([fresh('data/races.json'), fresh('data/control.json'), fresh('data/offices.json')]);
  if (!real) return false;
  loadRaces(real, off, ctl, st);
  return true;
}

// Races not called yet (a runoff counts as decided until its own day), the ones the
// 10-minute results refresh keeps reading.
const decided = (r) => r.result?.status === 'won' || r.result?.status === 'runoff';
export const stillCounting = () => afterElection() && allRaces().some((r) => !r.demo && !decided(r));

function loadRaces(real, off, ctl, st) {
  summaryCache = null;
  if (real) {
    const list = (real.races || []).map(normalizeReal);
    list.forEach(addRace);
    realRaceCount = list.length;
    researchedCount = list.filter((r) => r.research).length;
    meta = real.meta || null;
    modelCheck = verifyModel(list);
  }
  if (off) {
    const list = (off.races || []).map(normalizeReal);
    list.forEach(addRace);
    officeCount = list.length;
    officesResearched = list.filter((r) => r.research).length;
  }
  // Likes saved under an old candidate id follow the candidate to the new one.
  if (aliases.size) store.renameIds('liked', aliases);
  control = ctl;
  status = st;
}

// Each real race carries the Python model's result from the last refresh. Re-run
// the JavaScript model at that same moment: the two must agree.
function verifyModel(list) {
  const mismatches = [];
  let checked = 0;
  for (const r of list) {
    const mc = r.modelCheck;
    if (!mc || noOdds(r)) continue;
    checked++;
    const f = forecast(r, new Date(mc.asOf));
    if (f.lead.id !== mc.lead || Math.abs(f.pLead - mc.pLead) > 0.002 || Math.abs(f.margin - mc.margin) > 0.02) {
      mismatches.push({ id: r.id, expected: mc, got: { lead: f.lead.id, pLead: f.pLead, margin: f.margin } });
    }
    // The count-adjusted projection of a race still being counted, the same way.
    const lv = live(r, f);
    if (!!lv !== !!mc.live || (lv && (lv.lead.id !== mc.live.lead || Math.abs(lv.pLead - mc.live.pLead) > 0.002 || Math.abs(lv.margin - mc.live.margin) > 0.02))) {
      mismatches.push({ id: r.id, expected: { live: mc.live || null }, got: { live: lv ? { lead: lv.lead.id, pLead: lv.pLead, margin: lv.margin } : null } });
    }
  }
  if (mismatches.length) console.warn(`Informed Voter: the browser model disagrees with the refresh in ${mismatches.length} races`, mismatches);
  return { checked, mismatches };
}

// A person's photo and its credit: one the data carries (Congress's leaders), else the
// candidate's from data/photos.json (scripts/update_photos.py), keyed by the Wikipedia
// article their name links to. Null for everyone else, who keeps their initials.
export const photoOf = (c) => c?.photo || (c?.wiki && photos[c.wiki]) || null;

export const getMapIndex = () => mapIndex;
export const getRace = (id) => races.get(id) || legRaceById(id);
export const getCandidate = (id) => candidates.get(id) || candidates.get(aliases.get(id));
export const allRaces = () => [...races.values()];
// The Senate, House and governor races, the ones the maps, control tiles and close-race
// lists are about (allRaces also holds the statewide offices below governor).
const FEDERAL_AND_GOVERNOR = new Set(['senate', 'house', 'governor']);
export const mainRaces = () => allRaces().filter((r) => FEDERAL_AND_GOVERNOR.has(r.office));
export const controlData = () => control;
export const statusData = () => status;
export const racesMeta = () => meta;

// Open ("jungle") primaries put every candidate on one ballot with a runoff for the
// top two. The head-to-head model doesn't fit, so these races report the field,
// the polls as published and the forecasters' consensus rating, with no win odds.
// The expected margin is between the parties' combined vote (`lean`).
// State legislative races (kind "field") and the statewide offices below governor (kind
// "office") work the same way, except that `dr` is the 2024 presidential margin of the
// district or state, not an expected result.
function fieldForecast(race) {
  const kind = race.format === 'field' ? 'field' : race.format === 'office' ? 'office' : 'open-primary';
  const avg = pollAverage(race.polls, new Date());
  const raised = (c) => c.finance?.total || 0;
  const cands = race.candidates
    .map((c) => ({ ...c, share: avg?.shares[c.id] ?? null, poll: avg?.shares[c.id] ?? null, win: null, votes: null }))
    .sort((a, b) => (b.share ?? -1) - (a.share ?? -1) || raised(b) - raised(a));
  const rating = race.consensus?.rating || 'Not rated';
  const ratingParty = / R$/.test(rating) ? 'R' : / D$/.test(rating) ? 'D' : null; // "Safe R" -> R
  return {
    open: true, kind, asOf: new Date(), cands, lead: cands[0], second: cands[1],
    margin: null, dr: kind === 'open-primary' ? race.lean ?? null : race.pres24 ?? null, pollDR: null, pollMargin: null, sigma: 12, range80: null,
    pLead: null, rating, ratingParty, held: race.held || null, poll: avg, turnout: race.turnout,
  };
}

// The forecast, run for now until the polls close and frozen at Election Day after that
// (the final forecast).
export function fc(race) {
  let f = fcCache.get(race.id);
  if (!f) { f = noOdds(race) ? fieldForecast(race) : forecast(race, forecastAsOf()); fcCache.set(race.id, f); }
  return f;
}

// After Election Day, the final forecast adjusted for the votes counted so far, for a race
// that has a count and no call yet (null otherwise, and always for races with no odds).
export function liveFc(race) {
  if (!race || noOdds(race) || !afterElection()) return null;
  if (!liveCache.has(race.id)) liveCache.set(race.id, live(race, fc(race)));
  return liveCache.get(race.id);
}

export function hist(race) {
  if (noOdds(race)) return [];
  let h = histCache.get(race.id);
  if (!h) { h = history(race, 30, forecastAsOf()); histCache.set(race.id, h); }
  return h;
}

// Daily history over the race's whole polling record: from its first poll (the
// refresh keeps polls since January 2025), and never under 30 days. Each day is
// re-run with only the polls published by then, so the line moves when real
// polls came out and holds steady between them.
export function pollHist(race) {
  if (noOdds(race)) return [];
  let h = pollHistCache.get(race.id);
  if (!h) {
    const now = forecastAsOf();
    const ends = race.polls.map((p) => day(p.end).getTime()).filter((t) => t <= now.getTime());
    const first = ends.length ? Math.min(...ends) : now - 30 * 864e5;
    const days = Math.max(30, Math.ceil((now - first) / 864e5) + 2);
    h = history(race, days, now);
    pollHistCache.set(race.id, h);
  }
  return h;
}

// How the polling average and the forecast moved over the last `days` days.
export function changeOver(race, days) {
  const h = pollHist(race);
  if (h.length < 2) return null;
  const now = h[h.length - 1].fc, then = h[Math.max(0, h.length - 1 - days)].fc;
  if (!now.second) return null;
  const lastPoll = race.polls.reduce((m, p) => (p.end > m ? p.end : m), '');
  const pollsIn = race.polls.filter((p) => day(p.end) > new Date(Date.now() - days * 864e5)).length;
  // Both moves are measured between the same two candidates the margin is shown
  // for, and the polls on their first-round averages (as charted), so a
  // ranked-choice race compares like with like across the window.
  const d = now.cands.find((c) => c.party === 'D'), r = now.cands.find((c) => c.party === 'R');
  const [a, b] = now.dr != null && d && r ? [d, r] : [now.lead, now.second];
  const gap = (f) => (f.poll && f.poll.shares[a.id] != null && f.poll.shares[b.id] != null ? f.poll.shares[a.id] - f.poll.shares[b.id] : null);
  const share = (f, id) => f.cands.find((c) => c.id === id)?.share ?? 0;
  return {
    days, pollsIn, lastPoll: lastPoll || null,
    poll: gap(now) != null && gap(then) != null ? gap(now) - gap(then) : null,
    pollStarted: gap(now) != null && gap(then) == null,
    margin: share(now, a.id) - share(now, b.id) - (share(then, a.id) - share(then, b.id)),
    win: now.pLead - (then.cands.find((c) => c.id === now.lead.id)?.win ?? 0),
  };
}

// Change over the past seven days, per candidate and in the margin.
export function weekChange(race) {
  const h = hist(race);
  if (h.length < 2) return { cands: [], dr: null };
  const now = h[h.length - 1].fc, then = h[Math.max(0, h.length - 8)].fc;
  const winThen = Object.fromEntries(then.cands.map((c) => [c.id, c.win]));
  const shareThen = Object.fromEntries(then.cands.map((c) => [c.id, c.share]));
  return {
    cands: now.cands.map((c) => ({ id: c.id, win: c.win - (winThen[c.id] ?? 0), share: c.share - (shareThen[c.id] ?? 0) })),
    dr: now.dr != null && then.dr != null ? now.dr - then.dr : null,
  };
}

export function statewideRaces(st) {
  return { senate: races.get(`${st}-SEN`) || null, governor: races.get(`${st}-GOV`) || null };
}
export function houseRaces(st) {
  return allRaces().filter((r) => r.state === st && r.office === 'house').sort((a, b) => a.district.localeCompare(b.district));
}
// The statewide offices below governor on a state's 2026 ballot, in the order ballots
// usually list them.
const OFFICE_ORDER = ['lieutenant-governor', 'attorney-general', 'secretary-of-state', 'treasurer', 'auditor'];
export function officeRaces(st) {
  return allRaces().filter((r) => r.state === st && r.format === 'office')
    .sort((a, b) => OFFICE_ORDER.indexOf(a.office) - OFFICE_ORDER.indexOf(b.office) || a.id.localeCompare(b.id));
}

// Results ----------------------------------------------------------------------------
//
// After Election Day the pages lead with the results the refresh reads
// (scripts/lib/results.py): a race is decided only once Wikipedia's national table
// marks its winner, and vote counts are unofficial until the state certifies them. The
// pre-election forecast stays on each race page, labelled as such.

export const afterElection = (now = new Date()) => now >= ELECTION_DAY;
export const resultOf = (race) => race?.result || null;
// Any real race with results in: the switch that turns maps and lists to results.
export const resultsIn = () => afterElection() && mainRaces().some((r) => r.result);
// What the maps show: the results (the default once any are in) or the pre-election
// forecast, as the visitor last chose during this visit.
let mapViewChoice = null;
export const mapView = () => (resultsIn() ? mapViewChoice || 'results' : 'forecast');
export const setMapView = (v) => { mapViewChoice = v; };

// A row's share: the final round where a ranked-choice count has one.
export const rowShare = (row) => row.final ?? row.pct ?? null;

// The results box joined to the race's candidates, strongest first (by the final round
// in a ranked-choice count), with write-in and "others" lines last.
export function resultRows(race) {
  const res = race?.result;
  if (!res?.rows?.length) return [];
  const byId = new Map(race.candidates.map((c) => [c.id, c]));
  const won = new Set(res.winners || []), adv = new Set(res.advance || []);
  const key = (r) => rowShare(r) ?? (r.votes != null && res.total ? (100 * r.votes) / res.total : -1);
  return res.rows
    .map((r) => ({ ...r, cand: r.id ? byId.get(r.id) || null : null, won: won.has(r.id), advance: adv.has(r.id) }))
    .sort((a, b) => !!a.other - !!b.other || key(b) - key(a));
}

export const resultWinners = (race) => (race?.result?.winners || []).map((id) => race.candidates.find((c) => c.id === id)).filter(Boolean);
export const resultAdvancing = (race) => (race?.result?.advance || []).map((id) => race.candidates.find((c) => c.id === id)).filter(Boolean);

// The gap between the top two in the count, and who they are.
export function resultMargin(race) {
  const rows = resultRows(race).filter((r) => !r.other && rowShare(r) != null);
  if (rows.length < 2) return null;
  return { a: rows[0], b: rows[1], pts: rowShare(rows[0]) - rowShare(rows[1]) };
}

// The party a results map colors the race by: the winner's once called, the leader's
// while votes are counted (shown lighter), none for a runoff or before any count.
export function resultParty(race) {
  const res = race?.result;
  if (!res) return null;
  if (res.status === 'won') return resultWinners(race)[0]?.party || null;
  if (res.status === 'counting') {
    const top = resultRows(race).find((r) => !r.other);
    return top?.party || null;
  }
  return null;
}

// Seats each party has won so far in a chamber (governorships for "governor"): the
// called races by the winner's party, plus the seats not up this year. Independents and
// third parties are counted apart, since results don't say whom a newly elected
// independent caucuses with. The same rule as seat_tally in scripts/update_races.py.
export function resultsTally(office) {
  const rs = mainRaces().filter((r) => r.office === office && !(office === 'house' && r.state === 'DC'));
  const hold = control?.[office]?.holdover || (office === 'house' ? { D: 0, R: 0 } : HOLDOVER[office]);
  const won = { D: 0, R: 0, I: 0 };
  const flips = [], uncalled = [], runoff = [], counting = [];
  for (const r of rs) {
    const res = r.result;
    if (res?.status === 'won') {
      const p = resultParty(r);
      won[p === 'D' || p === 'R' ? p : 'I']++;
      if (res.flip) flips.push(r);
    } else if (res?.status === 'runoff') runoff.push(r);
    else {
      uncalled.push(r);
      if (res?.status === 'counting') counting.push(r);
    }
  }
  return {
    up: rs.length, called: won.D + won.R + won.I, won, hold,
    seats: { D: won.D + (hold.D || 0), R: won.R + (hold.R || 0), I: won.I + (hold.I || 0) },
    flips, uncalled, runoff, counting, current: control?.[office]?.current || CURRENT[office],
  };
}

export async function loadLayer(st, layer) {
  const key = `${layer}/${st}`;
  if (!layerCache.has(key)) layerCache.set(key, fetchJSON(`data/maps/${layer}/${st}.json`));
  return layerCache.get(key);
}

// Legislative races are built on demand from the chamber's district map: the real
// races from data/legislature where the refresh found them, the demo set elsewhere.
export async function legislativeRaces(st, chamberKey) {
  const key = `${st}:${chamberKey}`;
  if (legCache.has(key)) return legCache.get(key);
  const chamber = legislatureChambers(st).find((c) => c.key === chamberKey);
  if (!chamber) return null;
  const [fcoll, file] = await Promise.all([loadLayer(st, chamber.layer), legFile(st)]);
  const info = file?.chambers?.find((c) => c.key === chamberKey) || null;
  const real = new Map((file?.races || []).filter((r) => r.chamber === chamberKey).map((r) => [r.district, normalizeReal(r)]));
  const built = demo.legislativeRaces(st, chamber, fcoll.features);
  for (const [code, race] of built) {
    // Real data wins. Where the page lists the seats on the ballot, a district it
    // leaves out has no election this year (the demo only guesses for staggered terms).
    const r = real.get(code) || (race && races.get(race.id)) || (info?.complete ? null : race);
    built.set(code, r);
    if (r) for (const c of r.candidates) candidates.set(c.id, { ...c, raceId: r.id });
  }
  const result = { chamber, features: fcoll, races: built, info };
  legCache.set(key, result);
  return result;
}

function legRaceById(id) {
  for (const { races: m } of legCache.values()) for (const r of m.values()) if (r && r.id === id) return r;
  return null;
}

// Ensure a legislative race exists (e.g. a starred one) before rendering it.
export async function ensureRace(id) {
  if (getRace(id)) return getRace(id);
  const m = id.match(/^([A-Z]{2})-(SS|SH|LEG)-(.+)$/);
  if (!m) return null;
  await legislativeRaces(m[1], m[2] === 'SS' ? 'senate' : m[2] === 'SH' ? 'house' : 'leg');
  return getRace(id);
}
export async function ensureCandidate(id) {
  if (getCandidate(id)) return getCandidate(id);
  await ensureRace(id.split(':')[0]);
  return getCandidate(id) || null;
}

export function positionsOf(cand) {
  const race = getRace(cand.raceId);
  return cand.demo ? demo.positions(cand, race) : cand.positions || {};
}
export function financeOf(cand) {
  const race = getRace(cand.raceId);
  return cand.demo ? demo.finance(cand, race) : cand.finance || null;
}
// A total counts as a figure when it is positive, or $0 from a filed summary with its
// coverage dates. Wikipedia lists candidates who have filed nothing at a bare $0, and
// that means "not loaded yet", never "raised nothing".
export const hasFigures = (fin) => !!fin && fin.total != null && (fin.total > 0 || !!fin.from);
// Real races carry the early vote their state or district has reported (House
// districts only where the Election Lab's district file is complete).
export function earlyVoteOf(race) {
  if (race.demo) return race.statewide && race.office !== 'house' ? demo.earlyVote(race.state) : null;
  return race.earlyVote || null;
}

// Senate, House and governor control. The refresh's simulation (data/control.json,
// 20,000 runs) is used when present; otherwise the same simulation runs here.
export function chamberSummary() {
  if (summaryCache) return summaryCache;
  if (control?.senate && control?.house && control?.governor) {
    summaryCache = { senate: control.senate, house: control.house, governor: control.governor, history: control.history || [], source: 'refresh', updated: control.updated };
    return summaryCache;
  }
  const entries = (pred) => allRaces().filter(pred).map((r) => simEntry(r, fc(r)));
  const withGains = (o, cur) => ({ ...o, current: cur, gainD: o.meanD - cur.D, gainR: o.meanR - cur.R });
  summaryCache = {
    senate: withGains(chamberOdds(entries((r) => r.office === 'senate'), { holdD: HOLDOVER.senate.D, holdR: HOLDOVER.senate.R, dNeeds: 51, rNeeds: 50, seed: 'senate' }), CURRENT.senate),
    // D.C.'s delegate can't vote on the floor, so it doesn't count toward control.
    house: withGains(chamberOdds(entries((r) => r.office === 'house' && r.state !== 'DC'), { dNeeds: 218, rNeeds: 218, seed: 'house' }), CURRENT.house),
    governor: withGains(chamberOdds(entries((r) => r.office === 'governor'), { holdD: HOLDOVER.governor.D, holdR: HOLDOVER.governor.R, dNeeds: 26, rNeeds: 26, seed: 'gov' }), CURRENT.governor),
    history: [], source: 'browser', updated: null,
  };
  return summaryCache;
}

// The office's own name in that state ("State Comptroller", "Lieutenant Governor"),
// short forms for tight spots.
const OFFICE_SHORT = { 'attorney-general': 'AG', 'secretary-of-state': 'SoS', 'lieutenant-governor': 'Lt. Gov.' };
export function raceTitle(race) {
  const s = STATE_BY_ABBR[race.state];
  if (race.format === 'office') return `${s.name} ${race.officeName}${race.special ? ' (special)' : ''}`;
  switch (race.office) {
    case 'senate': return `${s.name} Senate${race.special ? ' (special)' : ''}`;
    case 'governor': return `${s.name} Governor`;
    case 'house':
      if (race.state === 'DC') return 'D.C. Delegate to the U.S. House';
      return race.district === '00' ? `${s.name} At-Large House Seat` : `${s.name} ${ordinalDistrict(race.district)} District`;
    case 'state-senate': return `${s.name} ${s.upper.name}, ${race.districtName}`;
    case 'state-house': return `${s.name} ${s.lower.name}, ${race.districtName}`;
    case 'legislature': return `${s.name} Legislature, ${race.districtName}`;
    default: return race.id;
  }
}
export function raceShortTitle(race) {
  const s = race.state;
  if (race.format === 'office') return `${s} ${OFFICE_SHORT[race.office] || race.officeName.replace(/^State /, '')}`;
  switch (race.office) {
    case 'senate': return `${s} Sen`;
    case 'governor': return `${s} Gov`;
    case 'house': return race.district === '00' || race.state === 'DC' ? `${s}-AL` : `${s}-${parseInt(race.district, 10)}`;
    default: return `${s} ${race.districtName}`;
  }
}
export function officeLabel(race) {
  if (race.format === 'office') return race.officeName;
  return {
    senate: 'U.S. Senate', governor: 'Governor', house: 'U.S. House',
    'state-senate': STATE_BY_ABBR[race.state].upper?.name, 'state-house': STATE_BY_ABBR[race.state].lower?.name,
    legislature: 'Legislature',
  }[race.office];
}
function ordinalDistrict(code) {
  const n = parseInt(code, 10);
  const s = ['th', 'st', 'nd', 'rd'], v = n % 100;
  return n + (s[(v - 20) % 10] || s[v] || s[0]);
}

export const isDemo = (raceOrCand) => raceOrCand?.demo !== false;
// 'demo' (fictional), 'auto' (refreshed from public sources every 8 hours) or
// 'research' (also hand-researched: bios, positions with sources, curated polls).
export const dataKind = (race) => (isDemo(race) ? 'demo' : race.research ? 'research' : 'auto');
export { STATES };
