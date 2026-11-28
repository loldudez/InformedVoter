// Who holds each office after the 2026 election. A seat on the 2026 ballot goes to its
// called winner (scripts/lib/results.py: Wikipedia's check marks); a seat that wasn't up
// stays with the person in office now: the senators in data/congress.json, the governors
// and statewide officers in data/officeholders.json (scripts/update_officeholders.py).
// Anything not decided yet says so instead of guessing. Loaded by the pages that show
// people (the home map, state pages, Congress, the 2028 field).

import { fetchJSON } from '../util.js';
import { statewideRaces, officeRaces, houseRaces, resultWinners, resultAdvancing, resultMargin, photoOf } from './world.js';

let congress = null;
let holders = null;
let loading = null;

export function loadHolders() {
  if (!loading) {
    loading = Promise.all([
      fetchJSON('data/congress.json').catch(() => null),
      fetchJSON('data/officeholders.json').catch(() => null),
    ]).then(([c, h]) => { congress = c; holders = h; });
  }
  return loading;
}
export const congressData = () => congress;
export const holdersData = () => holders;

const linkKey = (u) => {
  if (!u) return null;
  try { return decodeURIComponent(u).replace(/ /g, '_').replace(/^https?:\/\/en\.(m\.)?wikipedia\.org\/wiki\//, ''); } catch { return u; }
};
const fold = (s) => (s || '').normalize('NFKD').replace(/[̀-ͯ]/g, '').toLowerCase();
export const lastNameOf = (name) => {
  const parts = fold(name).replace(/\(.*?\)|,? (jr|sr|ii|iii|iv)\.?$/g, '').split(/\s+/).filter(Boolean);
  return parts[parts.length - 1] || '';
};
const partyCode = (p) => (p === 'D' || p === 'R' ? p : p ? 'I' : null);

// Bio, photo and website from the officeholders file's "people" (Wikipedia and Wikidata).
function enrich(person) {
  const p = person.wiki && holders?.people?.[person.wiki];
  if (p) {
    if (!person.bio && p.bio) { person.bio = p.bio; person.bioFromWiki = true; }
    if (!person.photo && p.photo) person.photo = p.photo;
    if (!person.site && p.site) person.site = p.site;
  }
  if (!person.photo) {
    const ph = photoOf({ wiki: person.wiki });
    if (ph) person.photo = ph;
  }
  return person;
}

// A re-elected member of Congress's id in the sitting Congress (the House Clerk's, or the
// senator's Bioguide id): the one member of the same state, party and last name, in the same
// district if there are two. The caucus lists match by it (caucusesOf), where an article
// link or a first name can differ between sources ("Joe" and "Joseph Morelle").
function sittingId(race, w) {
  if (!w.incumbent || (race.office !== 'house' && race.office !== 'senate')) return null;
  const last = lastNameOf(w.name), party = partyCode(w.party);
  const same = (congress?.chambers?.[race.office]?.members || [])
    .filter((m) => m.st === race.state && lastNameOf(m.n) === last && partyCode(m.party) === party);
  const d = parseInt(race.district, 10) || 0;
  const hit = race.office === 'house' && same.length > 1 ? same.filter((m) => (m.d || 0) === d) : same;
  return hit.length === 1 ? hit[0].id || null : null;
}

// One of a race's called winners as a person.
function electedPerson(race, w) {
  return enrich({
    raceId: race.id, race, office: race.office, st: race.state,
    status: 'elected', key: w.id, candId: w.id, name: w.name, party: w.party, wiki: w.wiki,
    photo: photoOf(w), bio: w.bio, site: w.officialSite || null, positions: w.positions || {},
    positionsFrom: w.positionsFrom || null, finance: w.finance || null, incumbent: !!w.incumbent, flip: !!race.result?.flip,
    ...(race.district != null && race.office === 'house' ? { district: race.district } : {}),
    bioguide: sittingId(race, w),
  });
}

// The person a race puts in office: its called winner, or what's still open.
export function fromRace(race) {
  const res = race?.result;
  const base = { raceId: race.id, race, office: race.office, st: race.state };
  if (res?.status === 'won') {
    const w = resultWinners(race)[0];
    if (w) return electedPerson(race, w);
  }
  if (res?.status === 'runoff') {
    return { ...base, status: 'runoff', key: `${race.id}:runoff`, advancing: resultAdvancing(race), date: res.runoffDate || null };
  }
  if (!res) return { ...base, status: 'no-result', key: `${race.id}:open` };
  const lead = resultMargin(race);
  return { ...base, status: 'uncalled', key: `${race.id}:open`, leader: lead?.a || null };
}

// State legislators -------------------------------------------------------------------
// Who sits in each state legislative district after the 2026 election: the 2026 winners
// where a seat was up (data/legislature, Wikipedia's chamber pages via
// scripts/lib/legislature.py) and Open States' current members for the seats that weren't
// (data/legislators, scripts/update_legislators.py). A 2026 seat whose winner isn't posted
// yet says so; the outgoing member is never shown in its place.
const legislators = new Map();
export function loadLegislators(st) {
  if (!legislators.has(st)) legislators.set(st, fetchJSON(`data/legislators/${st}.json`).catch(() => null));
  return legislators.get(st);
}

const LEG_OFFICE = { senate: 'state-senate', house: 'state-house', leg: 'legislature' };
function sittingLegislator(m, st, chamber, fid) {
  return enrich({
    status: 'holder', key: `leg:${st}:${chamber}:${fid}:${lastNameOf(m.n)}`, office: LEG_OFFICE[chamber] || chamber, st,
    name: m.n, party: m.p || null, wiki: m.wiki || null, site: m.site || null, positions: {}, notUp: true,
  });
}

// One district's members: the race's winners, then the members whose seats weren't up (in
// a district electing only some of its seats), and the race itself as `pending` while its
// winner isn't posted. A district with no 2026 race keeps its sitting members.
export function districtMembers(file, chamber, fid, race) {
  const st = file?.state || race?.state;
  const sitting = file?.chambers?.[chamber]?.[fid] || [];
  if (!race) return { members: sitting.map((m) => sittingLegislator(m, st, chamber, fid)), pending: null };
  const won = race.result?.status === 'won' ? resultWinners(race) : [];
  const up = Math.max(race.seats || 1, won.length);
  const gone = new Set([...(race.incumbents || []).map((i) => i.name), ...won.map((w) => w.name)].filter(Boolean).map(lastNameOf));
  const stay = sitting.filter((m) => !gone.has(lastNameOf(m.n))).slice(0, Math.max(0, sitting.length - up));
  return {
    members: [...won.map((w) => electedPerson(race, w)), ...stay.map((m) => sittingLegislator(m, st, chamber, fid))],
    pending: won.length ? null : race,
  };
}

function sittingSenator(m) {
  const extra = (holders?.senators || []).find((s) => s.st === m.st && fold(s.name) === fold(m.n)) || {};
  const wiki = m.article ? `https://en.wikipedia.org/wiki/${m.article.replace(/ /g, '_')}` : extra.wiki || null;
  return enrich({
    status: 'holder', key: `sen:${m.st}:${lastNameOf(m.n)}`, office: 'senate', st: m.st, name: m.n, party: m.party,
    wiki, since: m.since, up: m.up, cls: m.cls, positions: extra.positions || {}, votesCast: extra.votesCast || 0,
    positionsFrom: extra.positions ? 'votes' : null, bioguide: extra.bioguide || null,
  });
}

// A state's two senators from January 2027: the ones whose seats weren't up, and the
// 2026 race's winner. Senior seat first.
export function senatorsOf(st) {
  const sitting = (congress?.chambers?.senate?.members || []).filter((m) => m.st === st);
  const race = statewideRaces(st).senate;
  const out = sitting.filter((m) => !(race && m.up === 2026)).map(sittingSenator);
  if (race) {
    const won = { ...fromRace(race), up: race.special ? 2028 : 2032 };
    // A re-elected senator keeps the recorded Senate votes too: the race's researched
    // positions first, the votes for questions the research leaves open.
    const rec = won.status === 'elected' && won.incumbent
      ? (holders?.senators || []).find((x) => x.st === st && (linkKey(x.wiki) === linkKey(won.wiki) || lastNameOf(x.name) === lastNameOf(won.name)))
      : null;
    if (rec?.positions) { won.positions = { ...rec.positions, ...won.positions }; won.votesCast = rec.votesCast || 0; }
    out.push(won);
  }
  return out.sort((a, b) => (a.since || '9999').localeCompare(b.since || '9999'));
}

// How a state's delegation colors the map: two of one party, one of each, or with an
// independent; "?" for a seat not decided yet.
export function delegation(st) {
  const seats = senatorsOf(st);
  const parties = seats.map((s) => (s.status === 'elected' || s.status === 'holder' ? partyCode(s.party) : '?'));
  const order = { D: 0, R: 1, I: 2, '?': 3 };
  parties.sort((a, b) => order[a] - order[b]);
  return { seats, parties, kind: parties.join('') };
}

// The governor from January 2027 (or whenever the term starts).
export function governorOf(st) {
  const race = statewideRaces(st).governor;
  if (race) return fromRace(race);
  const h = holders?.offices?.GOV?.[st];
  return h ? holderPerson(h, 'GOV', st, 'governor') : null;
}

function holderPerson(h, key, st, office) {
  return enrich({
    status: 'holder', key: `${key}:${st}:${lastNameOf(h.name)}`, office, st, name: h.name, party: h.party, wiki: h.wiki || null,
    since: h.since || null, termEnd: h.termEnd || null, appointed: !!h.appointed, acting: !!h.acting, ticket: !!h.ticket,
    title: h.title || null, prior: h.prior || null, selection: h.selection || null,
    // Governors carry positions since Nov. 27, 2026 (update_officeholders.py): votes in
    // Congress, bills and hand research. The other offices have none yet.
    positions: h.positions || {}, positionsFrom: h.positionsFrom || null, votesCast: h.votesCast || 0,
    bioguide: h.bioguide || null,
  });
}

export const OFFICE_KEYS = [
  ['LG', 'lieutenant-governor', 'Lieutenant governor'],
  ['AG', 'attorney-general', 'Attorney general'],
  ['SOS', 'secretary-of-state', 'Secretary of state'],
  ['TREAS', 'treasurer', 'Treasurer'],
  ['AUD', 'auditor', 'Auditor'],
];

// The statewide officers below the governor, in the order ballots usually list them:
// each 2026 race's winner, the governor-elect's running mate where the lieutenant
// governor is elected on the governor's ticket, and otherwise the person in office.
export function statewideOfficers(st) {
  const races = officeRaces(st);
  const gov = statewideRaces(st).governor;
  const out = [];
  // One office can sit in two of Wikipedia's lists (Texas's comptroller is both its
  // "treasurer" and its auditor): each title and each person shows once.
  const norm = (t) => fold(t).replace(/\bstate\b|\bof\b|\bthe\b|[^a-z]/g, '');
  const titles = new Set(races.map((r) => norm(r.officeName)).filter(Boolean));
  const people = new Set();
  const fresh = (h) => {
    const t = h.title ? norm(h.title) : null;
    if ((t && titles.has(t)) || (h.wiki && people.has(linkKey(h.wiki)))) return false;
    if (t) titles.add(t);
    if (h.wiki) people.add(linkKey(h.wiki));
    return true;
  };
  for (const [key, office, label] of OFFICE_KEYS) {
    const race = races.find((r) => r.office === office);
    const held = holders?.offices?.[key]?.[st];
    const list = (Array.isArray(held) ? held : held ? [held] : [])
      // Alaska's and Utah's lieutenant governors keep the state's elections; they show once, as lieutenant governor.
      .filter((h) => !(key === 'SOS' && /lieutenant governor/i.test(h.title || '')));
    if (race) {
      const won = { ...fromRace(race), key: `${race.id}`, slot: key, label: race.officeName || label };
      if (won.wiki) people.add(linkKey(won.wiki));
      out.push(won);
      continue;
    }
    if (key === 'LG' && gov?.result?.status === 'won' && list.some((h) => h.ticket || /ticket/i.test(h.selection || ''))) {
      const w = resultWinners(gov)[0];
      const row = (gov.result.rows || []).find((r) => r.id === w?.id);
      out.push(row?.mate
        ? { status: 'elected', key: `${gov.id}:mate`, slot: key, office, st, label, name: row.mate, party: w.party, raceId: gov.id, race: gov, mateOf: w.name, positions: {} }
        : { status: 'mate-unknown', key: `${gov.id}:mate`, slot: key, office, st, label, raceId: gov.id, race: gov, mateOf: w?.name, party: w?.party });
      continue;
    }
    for (const h of list.filter(fresh)) out.push({ ...holderPerson(h, key, st, office), slot: key, label: h.title && key !== 'LG' ? h.title : label });
  }
  return out;
}

// Every House member from January 2027, district by district.
export const houseMembersOf = (st) => houseRaces(st).map((r) => fromRace(r));

// Every caucus whose own list has a member of Congress, in the owner's order (DSA,
// Progressive Caucus, Blue Dogs, New Democrats; Freedom Caucus, Main Street, Governance
// Group, Study Committee). The lists are each caucus's own roster where it publishes one,
// else Wikipedia's (scripts/update_officeholders.py), and every current member carries the
// sitting member's id, so the 119th Congress and the members re-elected to the 120th
// (`bioguide`, sittingId above) match by id. Otherwise the same
// article link matches; a name match needs the same last name and seat (a sitting seat, or
// the district a member-elect won) or state, the same first name too when both sides link
// different articles (a redirect), and from January a member who was re-elected: a
// newcomer needs a members-elect listing. Nov. 28, 2026: a seat alone had handed David
// Scott's and Mikie Sherrill's New Democrat listings to their successors, and a surname
// alone would have made Sylvia Garcia a Blue Dog for member-elect Johnny Garcia.
// Independents can be on either party's lists (Sanders with the Progressives, Kiley with
// the Governance Group).
const firstNamesOf = (name) => fold(name).replace(/\(.*?\)|,? (jr|sr|ii|iii|iv)\.?$/g, ' ').split(/\s+/).slice(0, -1)
  .map((w) => w.replace(/[^a-z-]/g, '')).filter((w) => w.length > 1);
const sameFirstName = (a, b) => { const fa = firstNamesOf(a); return firstNamesOf(b).some((x) => fa.some((y) => x.slice(0, 3) === y.slice(0, 3))); };
export function caucusesOf(person, { chamber = 'house', seat = null, sitting = false } = {}) {
  const cc = holders?.caucuses;
  if (!cc || !person) return [];
  const want = linkKey(person.wiki);
  const last = lastNameOf(person.name);
  const st = person.st;
  const pid = person.id || person.bioguide || null;
  const party = partyCode(person.party);
  const out = [];
  for (const id of cc.order) {
    const d = cc.defs.find((x) => x.id === id);
    if (!d || (party !== 'I' && d.party !== party)) continue;
    const list = chamber === 'senate' ? d.senate || [] : d.house || [];
    const hit = list.some((e) => {
      if (sitting && e.elect) return false;
      if (pid && e.id) return e.id === pid;
      if (want && e.wiki && linkKey(e.wiki) === want) return true;
      if (!sitting && !e.elect && !person.incumbent) return false;
      if (lastNameOf(e.n) !== last) return false;
      if (seat && e.seat && (sitting || e.elect)) return e.seat === seat;
      const est = e.st || (e.seat || '').slice(0, 2);
      return !!est && est === st && (!(want && e.wiki) || sameFirstName(e.n, person.name));
    });
    if (hit) out.push(d);
  }
  return out;
}
// The one caucus a card names: the first of them in the owner's order.
export const caucusOf = (person, opts) => caucusesOf(person, opts)[0] || null;
export const caucusDefs = () => holders?.caucuses?.defs || [];
