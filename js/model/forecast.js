// The forecast: a recency-weighted polling average blended with a fundamentals
// prior, turned into win probabilities with an explicit uncertainty.
//
// It is deliberately simple and transparent, and runs the same on demo or real
// polls. Inputs per race: `candidates`, `prior` (fundamentals share per candidate,
// summing to 100), `priorKind`, `polls`, `turnout`, `statewide`.
//
// scripts/lib/model.py is a line-for-line Python copy used by the 8-hourly
// refresh; each real race carries the Python result (`modelCheck`) and the site
// checks that this file reproduces it.

import { gauss, rng } from '../util.js';

export const ELECTION_DAY = new Date(2026, 10, 3, 20, 0, 0); // polls close, Nov 3 2026 (local time)

// Calendar days, so the evening of Oct 24 reads "10 days" rather than rounding up.
export function daysToElection(now = new Date()) {
  const midnight = (d) => new Date(d.getFullYear(), d.getMonth(), d.getDate()).getTime();
  return Math.max(0, Math.round((midnight(ELECTION_DAY) - midnight(now)) / 864e5));
}

// Abramowitz & Stegun 7.1.26
function erf(x) {
  const s = Math.sign(x);
  x = Math.abs(x);
  const t = 1 / (1 + 0.3275911 * x);
  const y = 1 - ((((1.061405429 * t - 1.453152027) * t + 1.421413741) * t - 0.284496736) * t + 0.254829592) * t * Math.exp(-x * x);
  return s * y;
}
export const normCdf = (z) => 0.5 * (1 + erf(z / Math.SQRT2));

const POP_WEIGHT = { LV: 1, RV: 0.9, A: 0.75 }; // likely voters > registered > all adults
const HALF_LIFE_DAYS = 14;
const DEFAULT_N = 600; // polls that don't report a sample size count as a typical 600
const Z80 = 1.2816;
export const NAT = 3.5; // shared national polling miss on the margin, in points

// Dates as YYYY-MM-DD are local calendar days (matching the Python model).
export const day = (s) => (typeof s === 'string' && s.length === 10 ? new Date(`${s}T00:00:00`) : new Date(s));

export function pollAverage(polls, asOf) {
  const live = (polls || []).filter((p) => day(p.end) <= asOf);
  if (!live.length) return null;
  const acc = {}, wts = {};
  let total = 0;
  for (const p of live) {
    const age = (asOf - day(p.end)) / 864e5;
    const w = Math.pow(0.5, age / HALF_LIFE_DAYS) * Math.sqrt(Math.min(p.n || DEFAULT_N, 2000) / 600) * (POP_WEIGHT[p.pop] ?? 0.8);
    total += w;
    for (const [id, v] of Object.entries(p.results)) {
      acc[id] = (acc[id] || 0) + w * v;
      wts[id] = (wts[id] || 0) + w;
    }
  }
  const shares = {};
  for (const id in acc) shares[id] = acc[id] / wts[id];
  return { shares, weight: total, count: live.length };
}

export function rating(party, p) {
  if (p >= 0.95) return `Safe ${party}`;
  if (p >= 0.8) return `Likely ${party}`;
  if (p >= 0.6) return `Lean ${party}`;
  return 'Toss-up';
}

export function verdict(p) {
  if (p >= 0.95) return 'very likely';
  if (p >= 0.8) return 'likely';
  if (p >= 0.6) return 'slightly favored';
  return null; // toss-up: phrased separately
}

// Typical miss on the margin with no polls: tighter when forecasters have rated the race.
export function blindSigma(race) {
  if (race.priorKind === 'ratings') return race.statewide ? 7 : 8;
  return race.statewide ? 9 : 11;
}

export function forecast(race, asOf = new Date()) {
  const cands = race.candidates;
  const avg = pollAverage(race.polls, asOf);
  const days = Math.max(0, (ELECTION_DAY - asOf) / 864e5);

  // Polls get more say the more (and fresher) of them there are, capped at 85%.
  let k = 0;
  const shares = {};
  if (avg) {
    const decided = cands.reduce((s, c) => s + (avg.shares[c.id] || 0), 0) || 1;
    k = Math.min(0.85, avg.weight / (avg.weight + 1.5));
    for (const c of cands) {
      const polled = ((avg.shares[c.id] || 0) / decided) * 100; // undecideds split pro rata
      shares[c.id] = k * polled + (1 - k) * race.prior[c.id];
    }
  } else {
    for (const c of cands) shares[c.id] = race.prior[c.id];
  }

  const ranked = [...cands].sort((a, b) => shares[b.id] - shares[a.id]);
  const [lead, second] = ranked;
  const margin = shares[lead.id] - (second ? shares[second.id] : 0);

  // Typical polling miss on the margin, wider with no polls, plus drift for time left.
  const polledSigma = race.statewide ? 5.5 : 7;
  const blind = blindSigma(race);
  const pollSigma = blind - (blind - polledSigma) * (k / 0.85);
  const sigma = Math.sqrt(pollSigma ** 2 + 0.06 * days);

  const pLead = second ? normCdf(margin / sigma) : 1;
  const win = Object.fromEntries(cands.map((c) => [c.id, 0]));
  win[lead.id] = pLead;
  if (second) win[second.id] = 1 - pLead;

  const out = ranked.map((c) => ({
    ...c,
    share: shares[c.id],
    win: win[c.id],
    votes: (race.turnout * shares[c.id]) / 100,
    poll: avg ? avg.shares[c.id] ?? null : null,
  }));

  // Each party's strongest candidate (races like Alaska's can list several per party).
  const d = ranked.find((c) => c.party === 'D');
  const r = ranked.find((c) => c.party === 'R');
  const dr = d && r ? shares[d.id] - shares[r.id] : null;
  const pollDR = d && r && avg && avg.shares[d.id] != null && avg.shares[r.id] != null ? avg.shares[d.id] - avg.shares[r.id] : null;
  const center = dr ?? margin;

  return {
    asOf,
    cands: out,
    lead: out[0],
    second: out[1] || null,
    margin,
    dr,
    pollDR,
    pollMargin: avg && second ? (avg.shares[lead.id] ?? 0) - (avg.shares[second.id] ?? 0) : null,
    sigma,
    range80: [center - Z80 * sigma, center + Z80 * sigma],
    pLead,
    rating: rating(lead.party, pLead),
    poll: avg,
    pollWeight: k,
    turnout: race.turnout,
  };
}

// Daily forecast snapshots, for trend lines and "change over the past week".
export function history(race, days = 30, now = new Date()) {
  const out = [];
  for (let i = days; i >= 0; i--) {
    const asOf = new Date(now.getTime() - i * 864e5);
    const fc = forecast(race, asOf);
    out.push({ date: asOf, fc });
  }
  return out;
}

// --- Chamber control ----------------------------------------------------------

const side = (p) => (p === 'D' ? 1 : p === 'R' ? -1 : 0);
const caucus = (c) => (c.caucus === 'D' || c.caucus === 'R' ? c.caucus : c.party === 'D' || c.party === 'R' ? c.party : 'O');

// One race as the simulation sees it: the top two contenders, the expected margin
// between them, its uncertainty, and how much a national swing toward Democrats
// moves it (1 for D vs R, 0.5 when one side is an independent).
export function simEntry(race, fc) {
  if (race.format === 'open-primary') return { a: 'D', b: 'R', m: race.lean || 0, sigma: blindSigma(race), nat: 1 };
  const a = caucus(fc.lead);
  if (!fc.second) return { a, b: a, m: 100, sigma: 1, nat: 0 };
  const b = caucus(fc.second);
  return { a, b, m: fc.margin, sigma: fc.sigma, nat: (side(a) - side(b)) / 2 };
}

// Seat totals by simulation. Every simulated election shares one national polling
// miss, so races move together the way they do on a real election night.
// The refresh script runs the same simulation in Python (data/control.json); the
// site uses this only when that file is missing.
export function chamberOdds(entries, { holdD = 0, holdR = 0, dNeeds, rNeeds, sims = 4000, seed = 'chamber' }) {
  const r = rng(seed);
  let dCtrl = 0, rCtrl = 0, sumD = 0, sumR = 0;
  const dist = new Map();
  for (let s = 0; s < sims; s++) {
    const nat = gauss(r) * NAT;
    let d = holdD, rep = holdR;
    for (const e of entries) {
      let w = e.a;
      if (e.a !== e.b) {
        const local = Math.sqrt(Math.max(e.sigma ** 2 - (NAT * e.nat) ** 2, 4));
        w = e.m + e.nat * nat + gauss(r) * local > 0 ? e.a : e.b;
      }
      if (w === 'D') d++;
      else if (w === 'R') rep++;
    }
    dist.set(d, (dist.get(d) || 0) + 1);
    sumD += d; sumR += rep;
    if (d >= dNeeds) dCtrl++;
    if (rep >= rNeeds) rCtrl++;
  }
  const keys = [...dist.keys()].sort((a, b) => a - b);
  const q = (cut) => { let acc = 0; for (const k of keys) { acc += dist.get(k); if (acc >= sims * cut) return k; } return keys[keys.length - 1]; };
  return {
    pD: dCtrl / sims, pR: rCtrl / sims, pNone: Math.max(0, 1 - (dCtrl + rCtrl) / sims),
    meanD: sumD / sims, meanR: sumR / sims, medianD: q(0.5), range80D: [q(0.1), q(0.9)], sims,
  };
}
