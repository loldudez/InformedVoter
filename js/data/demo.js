// DEMO DATASET — fictional candidates, polls, fundraising and positions.
//
// Everything here is invented so every screen can be built and tried before real
// data is connected. It is generated deterministically from each race id, so it is
// identical on every visit. The races themselves are real (which seats are up in
// 2026, and district boundaries), but nothing about any candidate is.
//
// Pollster names, candidate names and source titles are made up. Any resemblance
// to a real person or firm is coincidental, and the UI labels all of it as demo.

import { STATE_BY_ABBR, STATES, PARTY_REGISTRATION } from './states.js';
import { questionsForLevel } from './questions.js';
import { rng, gauss, pick, clamp, addDays, hashStr } from '../util.js';

const FIRST = [
  'Jordan', 'Taylor', 'Morgan', 'Avery', 'Casey', 'Riley', 'Quinn', 'Rowan', 'Elena', 'Marcus', 'Priya', 'Daniel',
  'Grace', 'Andre', 'Lena', 'Victor', 'Nadia', 'Samuel', 'Hannah', 'Mateo', 'Olivia', 'Isaiah', 'Claire', 'Rafael',
  'Naomi', 'Wesley', 'Imani', 'Owen', 'Sofia', 'Caleb', 'Leah', 'Dominic', 'Maya', 'Teresa', 'Julian', 'Ruth',
  'Tobias', 'Alma', 'Felix', 'Iris', 'Desmond', 'Camila', 'Reid', 'Joanna', 'Malik', 'Paige', 'Hector', 'Lydia',
  'Emmett', 'Bianca', 'Trent', 'Celeste', 'Arjun', 'Noelle', 'Gavin', 'Yvette', 'Corbin', 'Dana', 'Lucas', 'Simone',
  'Abel', 'Renee', 'Darius', 'Fiona', 'Levi', 'Monique', 'Hugo', 'Talia', 'Silas', 'Ingrid', 'Ezra', 'Marisol',
];
const LAST = [
  'Ashford', 'Bellamy', 'Brightwell', 'Calloway', 'Castellano', 'Delacroix', 'Donnelly', 'Easterly', 'Ellison',
  'Fairbanks', 'Fontaine', 'Galloway', 'Greer', 'Hartley', 'Holloway', 'Ingram', 'Iverson', 'Jacobsen', 'Kendrick',
  'Kowalski', 'Langford', 'Lindqvist', 'Marchetti', 'Montoya', 'Nakamura', 'Norwood', 'Okafor', 'Oyelaran',
  'Pemberton', 'Prescott', 'Quintero', 'Ravensworth', 'Rhodes', 'Salazar', 'Sinclair', 'Strickland', 'Thornbury',
  'Tolliver', 'Underhill', 'Valdez', 'Whitaker', 'Winslow', 'Yarborough', 'Zamora', 'Abernathy', 'Bramwell',
  'Carrow', 'Dunleavy-Price', 'Everhart', 'Faraday', 'Goldfarb', 'Hollister', 'Ibarra', 'Jansen', 'Kessler',
  'Larkspur', 'Mendoza-Hale', 'Northcott', 'Ostrander', 'Pacheco', 'Redfern', 'Stanhope', 'Treadwell', 'Upshaw',
  'Varga', 'Wexler', 'Achebe', 'Birch', 'Cordova', 'Dempsey', 'Ferreira', 'Hargrove', 'Lockhart', 'Mallory', 'Quill',
];
const JOBS = [
  'small-business owner', 'nurse', 'public-school teacher', 'attorney', 'Army veteran', 'civil engineer', 'farmer',
  'city council member', 'county commissioner', 'pastor', 'union electrician', 'family physician', 'former prosecutor',
  'firefighter', 'nonprofit director', 'economist', 'Navy veteran', 'software developer', 'rancher', 'school board member',
];
export const DEMO_POLLSTERS = [
  'Bluefinch Research', 'Cobalt Ridge Polling', 'Tallgrass Analytics', 'Ironleaf Surveys',
  'Meridian Hollow Group', 'Quillstone Data', 'Sablewood Research', 'Brightwater Opinion',
];
const SOURCE_KINDS = [
  'Campaign website issues page', 'Candidate questionnaire', 'Debate remarks', 'Local TV interview',
  'Op-ed', 'Town hall remarks', 'Campaign mailer', 'Newspaper endorsement interview',
];

const NOW = new Date();

function ideology(party, r) {
  switch (party) {
    case 'D': return -0.9 + gauss(r) * 0.35;
    case 'R': return 0.9 + gauss(r) * 0.35;
    case 'L': return 0.35 + gauss(r) * 0.45;
    case 'G': return -1.35 + gauss(r) * 0.25;
    default: return gauss(r) * 0.6;
  }
}

function candidatesFor(raceId, r, thirdChance) {
  const usedLast = new Set();
  const name = () => {
    let first, last;
    do { first = pick(r, FIRST); last = pick(r, LAST); } while (usedLast.has(last));
    usedLast.add(last);
    return `${first} ${last}`;
  };
  const parties = ['D', 'R'];
  if (r() < thirdChance) parties.push(pick(r, ['L', 'L', 'G', 'I', 'I']));
  return parties.map((party) => ({
    id: `${raceId}:${party}`,
    raceId,
    party,
    name: name(),
    job: pick(r, JOBS),
    ideology: ideology(party, r),
    demo: true,
  }));
}

// lean: D minus R, in points, before candidate effects.
function makeRace({ id, state, office, level, statewide, district = null, districtName = null, lean, turnout, held = null, special = false, nonpartisan = false }) {
  const r = rng(`demo:${id}`);
  const thirdChance = statewide ? 0.3 : office === 'house' ? 0.12 : 0.05;
  const candidates = candidatesFor(id, r, thirdChance);
  const third = candidates[2];
  const effLean = clamp(lean + gauss(r) * (statewide ? 3 : 4), -70, 70);
  const thirdShare = third ? (third.party === 'I' ? 3 + r() * 8 : third.party === 'L' ? 2 + r() * 3 : 1 + r() * 2.5) : 0;
  const d2 = clamp(50 + effLean / 2, 6, 94);
  const prior = {
    [candidates[0].id]: (d2 * (100 - thirdShare)) / 100,
    [candidates[1].id]: ((100 - d2) * (100 - thirdShare)) / 100,
  };
  if (third) prior[third.id] = thirdShare;

  const race = {
    id, state, office, level, statewide, district, districtName, held, special, nonpartisan,
    candidates, prior, turnout: Math.round(turnout), demo: true, lean: effLean,
    drift: gauss(r) * 3, // how much opinion moved over the last two months
  };
  race.polls = pollsFor(race, r);
  return race;
}

function pollCount(race, r) {
  const a = Math.abs(race.lean);
  if (race.statewide) return a < 10 ? 6 + Math.floor(r() * 7) : a < 20 ? 3 + Math.floor(r() * 4) : Math.floor(r() * 3);
  if (race.office === 'house') return a < 8 ? 1 + Math.floor(r() * 4) : a < 14 && r() < 0.3 ? 1 : 0;
  return 0; // state legislative races are rarely polled
}

function pollsFor(race, r) {
  const n = pollCount(race, r);
  const [d, rep, third] = race.candidates;
  const baseMargin = race.prior[d.id] - race.prior[rep.id];
  const polls = [];
  for (let i = 0; i < n; i++) {
    const daysAgo = 1 + Math.floor(Math.pow(r(), 1.5) * 60);
    const size = 400 + Math.floor(r() * 1100);
    const und = 3 + r() * 8;
    const thirdShare = third ? race.prior[third.id] * (0.7 + r() * 0.6) : 0;
    // Older polls sit further from today's opinion by the race's drift.
    const m = baseMargin - race.drift * (daysAgo / 60) + gauss(r) * 1.8 + gauss(r) * (100 / Math.sqrt(size));
    const two = 100 - und - thirdShare;
    const results = {
      [d.id]: +(two / 2 + m / 2).toFixed(1),
      [rep.id]: +(two / 2 - m / 2).toFixed(1),
    };
    if (third) results[third.id] = +thirdShare.toFixed(1);
    const end = addDays(NOW, -daysAgo);
    polls.push({
      pollster: pick(r, DEMO_POLLSTERS),
      start: addDays(end, -(2 + Math.floor(r() * 4))).toISOString().slice(0, 10),
      end: end.toISOString().slice(0, 10),
      n: size,
      pop: r() < 0.72 ? 'LV' : 'RV',
      results,
      demo: true,
    });
  }
  return polls.sort((a, b) => (a.end < b.end ? 1 : -1));
}

const stateTurnout = (st) => {
  const s = STATE_BY_ABBR[st];
  const r = rng(`turnout:${st}`);
  return s.pop * 1e6 * 0.77 * (0.42 + r() * 0.12);
};

// Senate, governor and U.S. House races for every state.
export function federalAndGovernor(mapIndex) {
  const out = [];
  for (const s of STATES) {
    const turnout = stateTurnout(s.abbr);
    if (s.senate) out.push(makeRace({ id: `${s.abbr}-SEN`, state: s.abbr, office: 'senate', level: 'federal', statewide: true, lean: s.pres24, turnout, held: s.senate.held, special: s.senate.type === 'special' }));
    if (s.governor) out.push(makeRace({ id: `${s.abbr}-GOV`, state: s.abbr, office: 'governor', level: 'state', statewide: true, lean: s.pres24, turnout, held: s.governor.held }));
    const nCd = mapIndex[s.abbr]?.cd || 0;
    for (let i = 1; i <= nCd; i++) {
      const code = s.abbr === 'DC' ? '98' : nCd === 1 ? '00' : String(i).padStart(2, '0');
      const id = `${s.abbr}-H-${code}`;
      const r = rng(`lean:${id}`);
      const lean = nCd === 1 ? s.pres24 : clamp(s.pres24 + gauss(r) * 16, -75, 75);
      out.push(makeRace({
        id, state: s.abbr, office: 'house', level: 'federal', statewide: nCd === 1, district: code,
        districtName: s.abbr === 'DC' ? 'Delegate (at large)' : nCd === 1 ? 'At-large district' : `District ${i}`,
        lean, turnout: (turnout / nCd) * (0.85 + r() * 0.3),
      }));
    }
  }
  return out;
}

// Same rule as district_name in scripts/lib/legislature.py.
export const cleanDistrictName = (n) => n.replace(/\b(State (Senate|House|Legislative)|Assembly|Legislative \((?:House|Senate)\)|Delegate)\s*/g, '').replace(/\s+/g, ' ').trim();

export function districtIsUp(chamber, code, raceId) {
  if (chamber.up === 'all') return true;
  if (chamber.up === 'none') return false;
  const num = parseInt(code, 10);
  if (chamber.parity && !Number.isNaN(num)) return chamber.parity === 'odd' ? num % 2 === 1 : num % 2 === 0;
  return hashStr(raceId) % 2 === 0; // staggered terms, pattern not encoded: demo picks half
}

// State legislative races for one chamber, built from that chamber's district map.
export function legislativeRaces(st, chamber, features) {
  const s = STATE_BY_ABBR[st];
  const prefix = chamber.key === 'leg' ? 'LEG' : chamber.key === 'senate' ? 'SS' : 'SH';
  const office = chamber.key === 'leg' ? 'legislature' : chamber.key === 'senate' ? 'state-senate' : 'state-house';
  const turnout = stateTurnout(st) / features.length;
  const out = new Map();
  for (const f of features) {
    const id = `${st}-${prefix}-${f.id}`;
    if (!districtIsUp(chamber, f.id, id)) { out.set(f.id, null); continue; }
    const r = rng(`lean:${id}`);
    out.set(f.id, makeRace({
      id, state: st, office, level: 'state', statewide: false, district: f.id,
      districtName: cleanDistrictName(f.properties.n), lean: clamp(s.pres24 + gauss(r) * 18, -80, 80),
      turnout: turnout * (0.85 + r() * 0.3), nonpartisan: !!s.unicameral,
    }));
  }
  return out;
}

// Early-vote returns for a state (shared by its statewide races).
export function earlyVote(st) {
  const s = STATE_BY_ABBR[st];
  const r = rng(`early:${st}`);
  const turnout = stateTurnout(st);
  const ballots = turnout * (0.2 + r() * 0.18);
  const dShare = clamp(40 + s.pres24 * 0.35 + gauss(r) * 3, 15, 75);
  const rShare = clamp(40 - s.pres24 * 0.35 + gauss(r) * 3, 15, 75);
  return {
    ballots: Math.round(ballots),
    pctOfTurnout: ballots / turnout,
    byParty: PARTY_REGISTRATION.has(st) ? { D: dShare, R: rShare, other: Math.max(5, 100 - dShare - rShare) } : null,
    of2022: 0.2 + r() * 0.25,
    demo: true,
  };
}

const FINANCE_BASE = { senate: 9e6, governor: 7e6, house: 9e5, 'state-senate': 9e4, 'state-house': 5e4, legislature: 6e4 };

// Categories mirror real campaign-finance reports. Corporations cannot give
// directly to federal candidates, so business money shows up under PACs.
export function finance(cand, race) {
  const r = rng(`money:${cand.id}`);
  const comp = 1 - Math.min(1, Math.abs(race.lean) / 30);
  const total = FINANCE_BASE[race.office] * (0.4 + 3.2 * comp * comp) * Math.exp(gauss(r) * 0.5) * (cand.party === 'D' || cand.party === 'R' ? 1 : 0.06);
  const pubOk = race.level === 'state' && STATE_BY_ABBR[race.state].publicFinancing;
  const raw = {
    small: 0.15 + r() * 0.3,
    large: 0.25 + r() * 0.25,
    pac: race.level === 'federal' ? 0.05 + r() * 0.25 : 0.08 + r() * 0.3,
    party: 0.02 + r() * 0.06,
    self: r() < 0.12 ? 0.2 + r() * 0.4 : r() * 0.02,
    public: pubOk && r() < 0.6 ? 0.1 + r() * 0.3 : 0,
  };
  const sum = Object.values(raw).reduce((a, b) => a + b, 0);
  const parts = Object.fromEntries(Object.entries(raw).map(([k, v]) => [k, (v / sum) * total]));
  const growth = 0.02 + r() * 0.05;
  return {
    total,
    parts,
    cashOnHand: total * (0.15 + r() * 0.3),
    weekAgoTotal: total * (1 - growth),
    demo: true,
  };
}

const KNOWN_SHARE = { senate: 0.72, governor: 0.68, house: 0.52, 'state-senate': 0.38, 'state-house': 0.32, legislature: 0.35 };

export function positions(cand, race) {
  const r = rng(`pos:${cand.id}`);
  const out = {};
  for (const q of questionsForLevel(race.level)) {
    if (r() > KNOWN_SHARE[race.office]) { out[q.id] = null; continue; }
    const s = q.demoLean * -cand.ideology * 1.7 + (q.demoLean === 0 ? 0.6 : 0.15) + gauss(r) * 0.55;
    const stance = s > 1.15 ? 2 : s > 0.35 ? 1 : s > -0.35 ? 0 : s > -1.15 ? -1 : -2;
    out[q.id] = {
      stance,
      source: {
        title: `${pick(r, SOURCE_KINDS)} (demo source)`,
        date: addDays(NOW, -Math.floor(r() * 150)).toISOString().slice(0, 10),
        url: null,
        demo: true,
      },
    };
  }
  return out;
}
