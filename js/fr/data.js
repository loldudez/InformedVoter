// Data for the France section, loaded once and only when a France page opens: the
// 2027 presidential election (dates, candidates, polls), the parties, the election
// calendar and the maps. Built by scripts/fr/*.py; see DATA.md.

import { fetchJSON } from '../util.js';
import { lang, L } from '../i18n.js';

const cache = {};
const load = (key, url) => (cache[key] ??= fetchJSON(url).catch((e) => { console.warn(e); delete cache[key]; return null; }));

export const loadPres = () => load('pres', 'data/fr/presidentielle-2027.json');
export const loadParties = () => load('parties', 'data/fr/partis.json');
export const loadCalendar = () => load('calendar', 'data/fr/calendrier.json');
export const loadRegions = () => load('regions', 'data/fr/maps/regions.json');
export const loadDepartements = () => load('deps', 'data/fr/maps/departements.json');
export const loadCities = () => load('cities', 'data/fr/maps/villes.json');
// Candidates' sourced positions on the 144 questions (scripts/fr/positions_2027.py).
export const loadPositions = () => load('positions', 'data/fr/positions.json');
// The day the most recently read of these positions' sources was read and its quotes
// checked. positions.json is rebuilt at every refresh, so its own date says nothing
// about that.
export const lastRead = (byQuestion) => Object.values(byQuestion || {})
  .map((p) => p.source?.accessed).filter(Boolean).sort().pop() || null;
// Who sits in the Assemblée nationale and the Sénat (scripts/fr/parlement.py).
export const loadParliament = () => load('parliament', 'data/fr/parlement.json');
// The figures behind "Les grands enjeux" (scripts/fr/enjeux.py).
export const loadEnjeux = () => load('enjeux', 'data/fr/enjeux.json');

// A source's date: "2026-10-15" is a day, "2025-02" a month.
export function fmtSourceDate(d) {
  if (!d) return '';
  if (/^\d{4}-\d{2}$/.test(d)) {
    return new Date(+d.slice(0, 4), +d.slice(5, 7) - 1, 1).toLocaleDateString(lang() === 'fr' ? 'fr-FR' : 'en-GB', { month: 'long', year: 'numeric' });
  }
  return fmtDay(d);
}

// A commune that isn't among the largest cities: name, population and codes from
// geo.api.gouv.fr (only the commune's INSEE code is sent).
export async function fetchCommune(code) {
  try {
    const c = await fetchJSON(`https://geo.api.gouv.fr/communes/${encodeURIComponent(code)}?fields=nom,code,population,codeDepartement,codeRegion,centre`);
    return { code: c.code, name: c.nom, pop: c.population, dep: c.codeDepartement, reg: c.codeRegion, at: c.centre?.coordinates };
  } catch {
    return null;
  }
}

// Dates ---------------------------------------------------------------------------

// "2027-04-18" is that calendar day wherever the visitor is (see util.js toDate); a
// timestamp ("2026-11-03T00:02+00:00", when a file was built) is its day where the
// visitor is, which can be the day before the UTC date.
export const day = (iso) => {
  if (String(iso).length > 10) return new Date(iso);
  const [y, m, d] = iso.split('-').map(Number);
  return new Date(y, m - 1, d);
};

export function daysUntil(iso, now = new Date()) {
  const a = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  return Math.round((day(iso) - a) / 864e5);
}

export function fmtDay(iso, { weekday = false, year = true } = {}) {
  return day(iso).toLocaleDateString(lang() === 'fr' ? 'fr-FR' : 'en-GB', {
    weekday: weekday ? 'long' : undefined, day: 'numeric', month: 'long', year: year ? 'numeric' : undefined,
  });
}

// Poll dates come from French Wikipedia ("21-22 octobre 2026"); English mode translates the months.
const MONTHS_EN = { janvier: 'January', février: 'February', mars: 'March', avril: 'April', mai: 'May', juin: 'June', juillet: 'July', août: 'August', septembre: 'September', octobre: 'October', novembre: 'November', décembre: 'December' };
export const pollDates = (s) => (lang() === 'en'
  ? String(s).replace(/(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)/g, (m) => MONTHS_EN[m]).replace(/\b1er\b/g, '1')
  : String(s));

export const fmtNum = (x, d = 1) => Number(x).toLocaleString(lang() === 'fr' ? 'fr-FR' : 'en-GB', { minimumFractionDigits: d, maximumFractionDigits: d });
export const fmtPctFr = (x, d = 1) => (lang() === 'fr' ? `${fmtNum(x, d)} %` : `${fmtNum(x, d)}%`);
export const fmtInt = (x) => Math.round(x).toLocaleString(lang() === 'fr' ? 'fr-FR' : 'en-GB');

// Parties -------------------------------------------------------------------------

// Each party's color, by the abbreviation the polls use. Validated with the dataviz
// palette checker in both themes (css/styles.css, --fr-*). Place publique shares the
// Socialists' pink and MoDem shares Ensemble's yellow (allies in the same family);
// every other party is gray rather than borrowing a bigger party's color.
const PARTY_KEY = {
  LFI: 'lfi', PCF: 'pcf', LE: 'le', PS: 'ps', PP: 'ps',
  RE: 'ens', MoDem: 'ens', HOR: 'hor', LR: 'lr', RN: 'rn', REC: 'rec',
};
export const partyKey = (abbr) => PARTY_KEY[abbr] || 'other';
export const partyColor = (abbr) => `var(--fr-${partyKey(abbr)})`;

// Candidates ----------------------------------------------------------------------

export const candById = (pres, id) => pres?.candidates.find((c) => c.id === id) || null;

// The declared candidates whose poll average is at least `min` percent, highest
// first. People polls test without a declared candidacy are left out.
export function mainCandidates(pres, min = 2) {
  return (pres?.r1.average.candidates || [])
    .filter((a) => a.avg >= min && candById(pres, a.id)?.declared)
    .map((a) => ({ ...candById(pres, a.id), avg: a }));
}

// The ids of the declared candidates.
export const runningIds = (pres) => new Set((pres?.candidates || []).filter((c) => c.declared).map((c) => c.id));

// The line-ups of a poll that the average draws on: those made only of declared
// candidates, plus any line-up that tested a declared candidate those leave out
// (scripts/fr/update_presidentielle.py, r1_average). The others are hypotheses with
// people who aren't running.
export function usedScenarios(poll, running) {
  const clean = poll.scenarios.filter((s) => Object.keys(s).every((id) => running.has(id)));
  const inClean = new Set(clean.flatMap((s) => Object.keys(s)));
  return poll.scenarios.filter((s) => clean.includes(s)
    || Object.keys(s).some((id) => running.has(id) && !inClean.has(id)));
}

// What a person's candidacy stands at, from scripts/fr/candidats_2027.py. The
// wording is gender-neutral ("Candidature déclarée") since the data has no gender.
export function statusLabel(c) {
  switch (c?.status) {
    case 'declared': return L('Candidature déclarée', 'Declared candidate');
    case 'rallied': case 'lost-primary': return L('Ne se présente pas', 'Not running');
    case 'withdrawn': return L('Candidature retirée', 'Withdrew');
    case 'unconfirmed': return L('Candidature à confirmer', 'Candidacy unconfirmed');
    default: return L('Pas de candidature déclarée', 'No declared candidacy');
  }
}

// A match-up counts as current when it was polled in the last 60 days.
export const isCurrentDuel = (duel, pres) => {
  const last = duel.polls[0]?.end;
  const latest = pres.r1.average.to || last;
  return last && (day(latest) - day(last)) / 864e5 <= 60;
};

// Wikimedia's thumbnail links carry tracking parameters; the bare file is the same.
export const photoSrc = (c) => (c?.photo?.thumb ? c.photo.thumb.split('?')[0] : null);
