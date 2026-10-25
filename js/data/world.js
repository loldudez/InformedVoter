// One place the views ask for races, candidates and forecasts.
//
// Races start as the demo set. data/races.json (written every 8 hours by
// scripts/update_races.py, see DATA.md) replaces each demo race with the same id
// with real data. data/control.json holds the chamber-control simulation and
// data/status.json the refresh's automatic checks.

import { STATES, STATE_BY_ABBR, HOLDOVER, CURRENT, legislatureChambers } from './states.js';
import * as demo from './demo.js';
import { forecast, history, chamberOdds, pollAverage, simEntry, day } from '../model/forecast.js';
import { fetchJSON } from '../util.js';
import { store } from '../store.js';

const races = new Map();
const candidates = new Map();
const aliases = new Map();   // old candidate id -> current id (e.g. LA-SEN:R -> LA-SEN:letlow)
const fcCache = new Map();
const histCache = new Map();
const pollHistCache = new Map();
const layerCache = new Map();
const legCache = new Map();
let mapIndex = {};
let summaryCache = null;
let control = null;
let status = null;
let meta = null;
export let realRaceCount = 0;
export let researchedCount = 0;
export let modelCheck = null; // { checked, mismatches: [{id, expected, got}] }

function addRace(race) {
  races.set(race.id, race);
  for (const c of race.candidates) {
    candidates.set(c.id, { ...c, raceId: race.id });
    for (const a of c.aliases || []) aliases.set(a, c.id);
  }
  fcCache.delete(race.id);
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

export async function initWorld() {
  mapIndex = await fetchJSON('data/maps/index.json');
  demo.federalAndGovernor(mapIndex).forEach(addRace);
  const [real, ctl, st] = await Promise.all([optional('data/races.json'), optional('data/control.json'), optional('data/status.json')]);
  if (real) {
    const list = (real.races || []).map(normalizeReal);
    list.forEach(addRace);
    realRaceCount = list.length;
    researchedCount = list.filter((r) => r.research).length;
    meta = real.meta || null;
    // Likes saved under an old candidate id follow the candidate to the new one.
    if (aliases.size) store.renameIds('liked', aliases);
    modelCheck = verifyModel(list);
  }
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
    if (!mc || r.format === 'open-primary') continue;
    checked++;
    const f = forecast(r, new Date(mc.asOf));
    if (f.lead.id !== mc.lead || Math.abs(f.pLead - mc.pLead) > 0.002 || Math.abs(f.margin - mc.margin) > 0.02) {
      mismatches.push({ id: r.id, expected: mc, got: { lead: f.lead.id, pLead: f.pLead, margin: f.margin } });
    }
  }
  if (mismatches.length) console.warn(`Informed Voter: the browser model disagrees with the refresh in ${mismatches.length} races`, mismatches);
  return { checked, mismatches };
}

export const getMapIndex = () => mapIndex;
export const getRace = (id) => races.get(id) || legRaceById(id);
export const getCandidate = (id) => candidates.get(id) || candidates.get(aliases.get(id));
export const allRaces = () => [...races.values()];
export const controlData = () => control;
export const statusData = () => status;
export const racesMeta = () => meta;

// Open ("jungle") primaries put every candidate on one ballot with a runoff for the
// top two. The head-to-head model doesn't fit, so these races report the field,
// the polls as published and the forecasters' consensus rating, with no win odds.
// The expected margin is between the parties' combined vote (`lean`).
function fieldForecast(race) {
  const avg = pollAverage(race.polls, new Date());
  const raised = (c) => c.finance?.total || 0;
  const cands = race.candidates
    .map((c) => ({ ...c, share: avg?.shares[c.id] ?? null, poll: avg?.shares[c.id] ?? null, win: null, votes: null }))
    .sort((a, b) => (b.share ?? -1) - (a.share ?? -1) || raised(b) - raised(a));
  const rating = race.consensus?.rating || 'Not rated';
  const ratingParty = / R$/.test(rating) ? 'R' : / D$/.test(rating) ? 'D' : null; // "Safe R" -> R
  return {
    open: true, asOf: new Date(), cands, lead: cands[0], second: cands[1],
    margin: null, dr: race.lean ?? null, pollDR: null, pollMargin: null, sigma: 12, range80: null,
    pLead: null, rating, ratingParty, poll: avg, turnout: race.turnout,
  };
}

export function fc(race) {
  let f = fcCache.get(race.id);
  if (!f) { f = race.format === 'open-primary' ? fieldForecast(race) : forecast(race); fcCache.set(race.id, f); }
  return f;
}

export function hist(race) {
  if (race.format === 'open-primary') return [];
  let h = histCache.get(race.id);
  if (!h) { h = history(race, 30); histCache.set(race.id, h); }
  return h;
}

// Daily history over a window long enough to include the polls behind the
// average: from the first poll of the last 180 days, and never under 30 days.
export function pollHist(race) {
  if (race.format === 'open-primary') return [];
  let h = pollHistCache.get(race.id);
  if (!h) {
    const now = new Date();
    const recent = race.polls.map((p) => day(p.end).getTime()).filter((t) => now - t <= 180 * 864e5);
    const first = recent.length ? Math.min(...recent) : now - 30 * 864e5;
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

export async function loadLayer(st, layer) {
  const key = `${layer}/${st}`;
  if (!layerCache.has(key)) layerCache.set(key, fetchJSON(`data/maps/${layer}/${st}.json`));
  return layerCache.get(key);
}

// Legislative races are built on demand from the chamber's district map.
export async function legislativeRaces(st, chamberKey) {
  const key = `${st}:${chamberKey}`;
  if (legCache.has(key)) return legCache.get(key);
  const chamber = legislatureChambers(st).find((c) => c.key === chamberKey);
  if (!chamber) return null;
  const fcoll = await loadLayer(st, chamber.layer);
  const built = demo.legislativeRaces(st, chamber, fcoll.features);
  for (const [code, race] of built) {
    if (!race) continue;
    const realOne = races.get(race.id); // real data wins
    built.set(code, realOne || race);
    if (!realOne) for (const c of race.candidates) candidates.set(c.id, { ...c, raceId: race.id });
  }
  const result = { chamber, features: fcoll, races: built };
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
export function earlyVoteOf(race) {
  if (!race.statewide || race.office === 'house') return null;
  return race.demo ? demo.earlyVote(race.state) : race.earlyVote || null;
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

export function raceTitle(race) {
  const s = STATE_BY_ABBR[race.state];
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
  switch (race.office) {
    case 'senate': return `${s} Sen`;
    case 'governor': return `${s} Gov`;
    case 'house': return race.district === '00' || race.state === 'DC' ? `${s}-AL` : `${s}-${parseInt(race.district, 10)}`;
    default: return `${s} ${race.districtName}`;
  }
}
export function officeLabel(race) {
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
