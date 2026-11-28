// What is on the ballot in each state on November 3, 2026, plus the links voters need.
//
// Real, checkable facts: which states hold U.S. Senate and governor races, which
// party currently holds each of those seats, legislative chamber sizes and term
// lengths, which chambers elect in 2026, and the official election-office sites
// (every URL checked October 2026).
//
// Two fields exist only to make the demo dataset believable and are never shown
// as facts: `pres24` (approximate 2024 presidential margin, D minus R) and `pop`
// (2020 census population, millions, used to size demo turnout).
//
// Chamber `up`: "all" = every district elects in 2026, "partial" = staggered terms,
// some districts elect, "none" = no election this year. `parity` names which
// districts elect where the pattern is known; otherwise the demo picks half.

import { L } from '../i18n.js';

export const ELECTION_DATE_LABEL = 'Tuesday, November 3, 2026';
export const electionDateLabel = () => L('Mardi 3 novembre 2026', ELECTION_DATE_LABEL);

const S = (abbr, fips, name, pres24, pop, senate, governor, upper, lower, office, extra = {}) => ({
  abbr, fips, name, pres24, pop, senate, governor, upper, lower, office,
  slug: name.toLowerCase().replace(/ /g, '-'),
  ...extra,
});

const sen = (held, type = 'regular') => ({ held, type });
const gov = (held) => ({ held });
const ch = (name, seats, term, up, parity) => ({ name, seats, term, up, ...(parity ? { parity } : {}) });

const SENATE = 'State Senate';
const HOUSE = 'State House';
const ASSEMBLY = 'State Assembly';
const DELEGATES = 'House of Delegates';

export const STATES = [
  S('AL', '01', 'Alabama', -30.5, 5.02, sen('R'), gov('R'), ch(SENATE, 35, 4, 'all'), ch(HOUSE, 105, 4, 'all'), 'https://www.sos.alabama.gov/alabama-votes'),
  S('AK', '02', 'Alaska', -13.1, 0.73, sen('R'), gov('R'), ch(SENATE, 20, 4, 'partial'), ch(HOUSE, 40, 2, 'all'), 'https://www.elections.alaska.gov', { format: 'Alaska uses a top-four primary and ranked-choice voting in the general election.' }),
  S('AZ', '04', 'Arizona', -5.5, 7.15, null, gov('D'), ch(SENATE, 30, 2, 'all'), ch(HOUSE, 60, 2, 'all'), 'https://azsos.gov/elections', { multiMember: 'lower', publicFinancing: true }),
  S('AR', '05', 'Arkansas', -30.6, 3.01, sen('R'), gov('R'), ch(SENATE, 35, 4, 'partial'), ch(HOUSE, 100, 2, 'all'), 'https://www.sos.arkansas.gov/elections'),
  S('CA', '06', 'California', 20.2, 39.5, null, gov('D'), ch(SENATE, 40, 4, 'partial', 'odd'), ch(ASSEMBLY, 80, 2, 'all'), 'https://www.sos.ca.gov/elections', { format: 'California uses a top-two primary, so two candidates of the same party can meet in November.' }),
  S('CO', '08', 'Colorado', 11.0, 5.77, sen('D'), gov('D'), ch(SENATE, 35, 4, 'partial'), ch(HOUSE, 65, 2, 'all'), 'https://www.coloradosos.gov/pubs/elections/'),
  S('CT', '09', 'Connecticut', 14.5, 3.61, null, gov('D'), ch(SENATE, 36, 2, 'all'), ch(HOUSE, 151, 2, 'all'), 'https://portal.ct.gov/sots/election-services', { publicFinancing: true }),
  S('DE', '10', 'Delaware', 14.7, 0.99, sen('D'), null, ch(SENATE, 21, 4, 'partial'), ch(HOUSE, 41, 2, 'all'), 'https://elections.delaware.gov'),
  S('DC', '11', 'District of Columbia', 83.8, 0.69, null, null, null, null, 'https://www.dcboe.org', { noLegislature: true, format: 'D.C. elects a non-voting delegate to the U.S. House and has no state legislature.' }),
  S('FL', '12', 'Florida', -13.1, 21.5, sen('R', 'special'), gov('R'), ch(SENATE, 40, 4, 'partial'), ch(HOUSE, 120, 2, 'all'), 'https://dos.fl.gov/elections/', { publicFinancing: true }),
  S('GA', '13', 'Georgia', -2.2, 10.7, sen('D'), gov('R'), ch(SENATE, 56, 2, 'all'), ch(HOUSE, 180, 2, 'all'), 'https://sos.ga.gov/elections', { format: 'Georgia requires a majority to win; a race where no one passes 50% goes to a runoff.' }),
  S('HI', '15', 'Hawaii', 23.1, 1.46, null, gov('D'), ch(SENATE, 25, 4, 'partial'), ch(HOUSE, 51, 2, 'all'), 'https://elections.hawaii.gov', { publicFinancing: true }),
  S('ID', '16', 'Idaho', -36.5, 1.84, sen('R'), gov('R'), ch(SENATE, 35, 2, 'all'), ch(HOUSE, 70, 2, 'all'), 'https://voteidaho.gov', { multiMember: 'lower' }),
  S('IL', '17', 'Illinois', 10.9, 12.8, sen('D'), gov('D'), ch(SENATE, 59, 4, 'partial'), ch(HOUSE, 118, 2, 'all'), 'https://www.elections.il.gov'),
  S('IN', '18', 'Indiana', -19.0, 6.79, null, null, ch(SENATE, 50, 4, 'partial'), ch(HOUSE, 100, 2, 'all'), 'https://www.in.gov/sos/elections/'),
  S('IA', '19', 'Iowa', -13.2, 3.19, sen('R'), gov('R'), ch(SENATE, 50, 4, 'partial'), ch(HOUSE, 100, 2, 'all'), 'https://sos.iowa.gov/elections/'),
  S('KS', '20', 'Kansas', -16.1, 2.94, sen('R'), gov('D'), ch(SENATE, 40, 4, 'none'), ch(HOUSE, 125, 2, 'all'), 'https://sos.ks.gov/elections/elections.html'),
  S('KY', '21', 'Kentucky', -30.5, 4.51, sen('R'), null, ch(SENATE, 38, 4, 'partial', 'even'), ch(HOUSE, 100, 2, 'all'), 'https://elect.ky.gov'),
  S('LA', '22', 'Louisiana', -22.0, 4.66, sen('R'), null, ch(SENATE, 39, 4, 'none'), ch(HOUSE, 105, 4, 'none'), 'https://voterportal.sos.la.gov', { format: 'Louisiana picked its U.S. Senate nominees in closed party primaries. This year its U.S. House races are open primaries on Nov. 3, with a Dec. 12 runoff if no one wins a majority. The ballot also has 10 proposed constitutional amendments and local races; the legislature next elects in 2027.' }),
  S('ME', '23', 'Maine', 6.9, 1.36, sen('R'), gov('D'), ch(SENATE, 35, 2, 'all'), ch(HOUSE, 151, 2, 'all'), 'https://www.maine.gov/sos/elections-voting', { format: 'Maine uses ranked-choice voting for its U.S. Senate and House races.', publicFinancing: true }),
  S('MD', '24', 'Maryland', 28.5, 6.18, null, gov('D'), ch(SENATE, 47, 4, 'all'), ch(DELEGATES, 141, 4, 'all'), 'https://elections.maryland.gov', { multiMember: 'lower', publicFinancing: true }),
  S('MA', '25', 'Massachusetts', 25.2, 7.03, sen('D'), gov('D'), ch(SENATE, 40, 2, 'all'), ch(HOUSE, 160, 2, 'all'), 'https://www.sec.state.ma.us/divisions/elections/elections-and-voting.htm', { publicFinancing: true }),
  S('MI', '26', 'Michigan', -1.4, 10.1, sen('D'), gov('D'), ch(SENATE, 38, 4, 'all'), ch(HOUSE, 110, 2, 'all'), 'https://www.michigan.gov/sos/elections', { publicFinancing: true }),
  S('MN', '27', 'Minnesota', 4.2, 5.71, sen('D'), gov('D'), ch(SENATE, 67, 4, 'all'), ch(HOUSE, 134, 2, 'all'), 'https://www.sos.mn.gov/elections-voting/', { publicFinancing: true }),
  S('MS', '28', 'Mississippi', -22.9, 2.96, sen('R'), null, ch(SENATE, 52, 4, 'none'), ch(HOUSE, 122, 4, 'none'), 'https://www.sos.ms.gov/elections-voting'),
  S('MO', '29', 'Missouri', -18.4, 6.15, null, null, ch(SENATE, 34, 4, 'partial', 'even'), ch(HOUSE, 163, 2, 'all'), 'https://www.sos.mo.gov/elections'),
  S('MT', '30', 'Montana', -20.0, 1.08, sen('R'), null, ch(SENATE, 50, 4, 'partial'), ch(HOUSE, 100, 2, 'all'), 'https://sosmt.gov/elections/'),
  S('NE', '31', 'Nebraska', -20.5, 1.96, sen('R'), gov('R'), ch('Legislature', 49, 4, 'partial', 'even'), null, 'https://sos.nebraska.gov/elections', { unicameral: true, format: 'Nebraska has a single-chamber, officially nonpartisan Legislature.' }),
  S('NV', '32', 'Nevada', -3.1, 3.10, null, gov('R'), ch(SENATE, 21, 4, 'partial'), ch(ASSEMBLY, 42, 2, 'all'), 'https://www.nvsos.gov/sos/elections'),
  S('NH', '33', 'New Hampshire', 2.8, 1.38, sen('D'), gov('R'), ch(SENATE, 24, 2, 'all'), ch(HOUSE, 400, 2, 'all'), 'https://www.sos.nh.gov/elections', { multiMember: 'lower', format: 'New Hampshire elects its governor every two years.' }),
  S('NJ', '34', 'New Jersey', 5.9, 9.29, sen('D'), null, ch(SENATE, 40, 4, 'none'), ch('General Assembly', 80, 2, 'none'), 'https://www.nj.gov/state/elections/', { format: 'New Jersey elects its legislature in odd-numbered years.' }),
  S('NM', '35', 'New Mexico', 6.0, 2.12, sen('D'), gov('D'), ch(SENATE, 42, 4, 'none'), ch(HOUSE, 70, 2, 'all'), 'https://www.sos.nm.gov/voting-and-elections/'),
  S('NY', '36', 'New York', 12.6, 20.2, null, gov('D'), ch(SENATE, 63, 2, 'all'), ch(ASSEMBLY, 150, 2, 'all'), 'https://elections.ny.gov', { publicFinancing: true, format: 'New York allows fusion voting, so a candidate can appear on more than one party line.' }),
  S('NC', '37', 'North Carolina', -3.2, 10.4, sen('R'), null, ch(SENATE, 50, 2, 'all'), ch(HOUSE, 120, 2, 'all'), 'https://www.ncsbe.gov'),
  S('ND', '38', 'North Dakota', -36.5, 0.78, null, null, ch(SENATE, 47, 4, 'partial'), ch(HOUSE, 94, 4, 'partial'), 'https://vip.sos.nd.gov', { multiMember: 'lower' }),
  S('OH', '39', 'Ohio', -11.2, 11.8, sen('R', 'special'), gov('R'), ch(SENATE, 33, 4, 'partial'), ch(HOUSE, 99, 2, 'all'), 'https://www.ohiosos.gov/elections/'),
  S('OK', '40', 'Oklahoma', -34.3, 3.96, sen('R'), gov('R'), ch(SENATE, 48, 4, 'partial'), ch(HOUSE, 101, 2, 'all'), 'https://oklahoma.gov/elections.html'),
  S('OR', '41', 'Oregon', 14.3, 4.24, sen('D'), gov('D'), ch(SENATE, 30, 4, 'partial'), ch(HOUSE, 60, 2, 'all'), 'https://sos.oregon.gov/voting-elections/', { format: 'Oregon votes entirely by mail.' }),
  S('PA', '42', 'Pennsylvania', -1.7, 13.0, null, gov('D'), ch(SENATE, 50, 4, 'partial', 'even'), ch(HOUSE, 203, 2, 'all'), 'https://www.pa.gov/agencies/vote'),
  S('RI', '44', 'Rhode Island', 13.8, 1.10, sen('D'), gov('D'), ch(SENATE, 38, 2, 'all'), ch(HOUSE, 75, 2, 'all'), 'https://vote.sos.ri.gov', { publicFinancing: true }),
  S('SC', '45', 'South Carolina', -17.8, 5.12, sen('R'), gov('R'), ch(SENATE, 46, 4, 'none'), ch(HOUSE, 124, 2, 'all'), 'https://scvotes.gov'),
  S('SD', '46', 'South Dakota', -29.2, 0.89, sen('R'), gov('R'), ch(SENATE, 35, 2, 'all'), ch(HOUSE, 70, 2, 'all'), 'https://sdsos.gov/elections-voting/', { multiMember: 'lower' }),
  S('TN', '47', 'Tennessee', -29.7, 6.91, sen('R'), gov('R'), ch(SENATE, 33, 4, 'partial', 'even'), ch(HOUSE, 99, 2, 'all'), 'https://sos.tn.gov/elections'),
  S('TX', '48', 'Texas', -13.7, 29.1, sen('R'), gov('R'), ch(SENATE, 31, 4, 'partial'), ch(HOUSE, 150, 2, 'all'), 'https://www.votetexas.gov'),
  S('UT', '49', 'Utah', -21.6, 3.27, null, null, ch(SENATE, 29, 4, 'partial'), ch(HOUSE, 75, 2, 'all'), 'https://vote.utah.gov', { format: 'Utah votes primarily by mail.' }),
  S('VT', '50', 'Vermont', 31.5, 0.64, null, gov('R'), ch(SENATE, 30, 2, 'all'), ch(HOUSE, 150, 2, 'all'), 'https://sos.vermont.gov/elections/', { multiMember: 'both', publicFinancing: true, format: 'Vermont elects its governor every two years.' }),
  S('VA', '51', 'Virginia', 5.8, 8.63, sen('D'), null, ch(SENATE, 40, 4, 'none'), ch(DELEGATES, 100, 2, 'none'), 'https://www.elections.virginia.gov', { format: 'Virginia elects its legislature in odd-numbered years.' }),
  S('WA', '53', 'Washington', 18.2, 7.71, null, null, ch(SENATE, 49, 4, 'partial'), ch(HOUSE, 98, 2, 'all'), 'https://www.sos.wa.gov/elections', { multiMember: 'lower', format: 'Washington uses a top-two primary and votes entirely by mail.' }),
  S('WV', '54', 'West Virginia', -41.9, 1.79, sen('R'), null, ch(SENATE, 34, 4, 'all'), ch(HOUSE, 100, 2, 'all'), 'https://sos.wv.gov/elections', { format: 'Each West Virginia Senate district has two seats; one is elected every two years.' }),
  S('WI', '55', 'Wisconsin', -0.9, 5.89, null, gov('D'), ch(SENATE, 33, 4, 'partial', 'even'), ch(ASSEMBLY, 99, 2, 'all'), 'https://elections.wi.gov'),
  S('WY', '56', 'Wyoming', -45.8, 0.58, sen('R'), gov('R'), ch(SENATE, 31, 4, 'partial'), ch(HOUSE, 62, 2, 'all'), 'https://sos.wyo.gov/Elections/'),
];

export const STATE_BY_ABBR = Object.fromEntries(STATES.map((s) => [s.abbr, s]));
export const STATE_BY_FIPS = Object.fromEntries(STATES.map((s) => [s.fips, s]));

// French names (Nov. 25, 2026): the usual French forms; the other states keep their
// English names in French too. `name` itself stays English, since data is matched on it.
const FR_NAMES = {
  CA: 'Californie', NC: 'Caroline du Nord', SC: 'Caroline du Sud', ND: 'Dakota du Nord', SD: 'Dakota du Sud',
  FL: 'Floride', GA: 'Géorgie', HI: 'Hawaï', LA: 'Louisiane', NM: 'Nouveau-Mexique', PA: 'Pennsylvanie',
  VA: 'Virginie', WV: 'Virginie-Occidentale', DC: 'District de Columbia',
};
export const stateName = (st) => {
  const en = STATE_BY_ABBR[st]?.name || st;
  return L(FR_NAMES[st] || en, en);
};
// "en Californie", "au Texas", "à Hawaï", "dans l’État de New York": French takes a
// different preposition by state (feminine names take "en", masculine "au", islands "à").
const FR_IN = {
  AL: 'en Alabama', AK: 'en Alaska', AZ: 'en Arizona', AR: 'en Arkansas', CA: 'en Californie', CO: 'au Colorado',
  CT: 'dans le Connecticut', DE: 'dans le Delaware', DC: 'dans le district de Columbia', FL: 'en Floride', GA: 'en Géorgie',
  HI: 'à Hawaï', ID: 'dans l’Idaho', IL: 'dans l’Illinois', IN: 'dans l’Indiana', IA: 'dans l’Iowa', KS: 'au Kansas',
  KY: 'au Kentucky', LA: 'en Louisiane', ME: 'dans le Maine', MD: 'dans le Maryland', MA: 'dans le Massachusetts',
  MI: 'dans le Michigan', MN: 'dans le Minnesota', MS: 'dans le Mississippi', MO: 'dans le Missouri', MT: 'dans le Montana',
  NE: 'dans le Nebraska', NV: 'dans le Nevada', NH: 'dans le New Hampshire', NJ: 'dans le New Jersey',
  NM: 'au Nouveau-Mexique', NY: 'dans l’État de New York', NC: 'en Caroline du Nord', ND: 'dans le Dakota du Nord',
  OH: 'dans l’Ohio', OK: 'en Oklahoma', OR: 'en Oregon', PA: 'en Pennsylvanie', RI: 'dans le Rhode Island',
  SC: 'en Caroline du Sud', SD: 'dans le Dakota du Sud', TN: 'dans le Tennessee', TX: 'au Texas', UT: 'dans l’Utah',
  VT: 'dans le Vermont', VA: 'en Virginie', WA: 'dans l’État de Washington', WV: 'en Virginie-Occidentale',
  WI: 'dans le Wisconsin', WY: 'dans le Wyoming',
};
// "de Pennsylvanie", "du Texas", "de l’Ohio", "d’Hawaï" (French only).
const FR_OF = {
  AL: 'de l’Alabama', AK: 'de l’Alaska', AZ: 'de l’Arizona', AR: 'de l’Arkansas', CA: 'de Californie', CO: 'du Colorado',
  CT: 'du Connecticut', DE: 'du Delaware', DC: 'du district de Columbia', FL: 'de Floride', GA: 'de Géorgie', HI: 'd’Hawaï',
  ID: 'de l’Idaho', IL: 'de l’Illinois', IN: 'de l’Indiana', IA: 'de l’Iowa', KS: 'du Kansas', KY: 'du Kentucky',
  LA: 'de Louisiane', ME: 'du Maine', MD: 'du Maryland', MA: 'du Massachusetts', MI: 'du Michigan', MN: 'du Minnesota',
  MS: 'du Mississippi', MO: 'du Missouri', MT: 'du Montana', NE: 'du Nebraska', NV: 'du Nevada', NH: 'du New Hampshire',
  NJ: 'du New Jersey', NM: 'du Nouveau-Mexique', NY: 'de l’État de New York', NC: 'de Caroline du Nord', ND: 'du Dakota du Nord',
  OH: 'de l’Ohio', OK: 'de l’Oklahoma', OR: 'de l’Oregon', PA: 'de Pennsylvanie', RI: 'du Rhode Island', SC: 'de Caroline du Sud',
  SD: 'du Dakota du Sud', TN: 'du Tennessee', TX: 'du Texas', UT: 'de l’Utah', VT: 'du Vermont', VA: 'de Virginie',
  WA: 'de l’État de Washington', WV: 'de Virginie-Occidentale', WI: 'du Wisconsin', WY: 'du Wyoming',
};
export const deState = (st) => FR_OF[st] || `de ${STATE_BY_ABBR[st]?.name || st}`;
// A French name ending "de l’État" takes the state after it without a second "l’État":
// "Sénat de l’État de Pennsylvanie", "Trésorier de l’État de New York".
export const withState = (base, st) => `${base} ${/ de l’État$/.test(base) && (st === 'NY' || st === 'WA') ? `de ${STATE_BY_ABBR[st].name}` : deState(st)}`;
// "Sénat de l’État de Pennsylvanie" / "Pennsylvania State Senate".
export const chamberOf = (st, name) => L(withState(FR_CHAMBERS[name] || name, st), `${STATE_BY_ABBR[st]?.name || st} ${name}`);
export const inState = (st) => L(FR_IN[st] || `dans l’État ${st}`, `in ${STATE_BY_ABBR[st]?.name || st}`);

const FR_CHAMBERS = {
  'State Senate': 'Sénat de l’État', 'State House': 'Chambre des représentants de l’État', 'State Assembly': 'Assemblée de l’État',
  'House of Delegates': 'Chambre des délégués', Legislature: 'Assemblée législative', 'General Assembly': 'Assemblée générale',
  'House of Representatives': 'Chambre des représentants', Senate: 'Sénat',
};
export const chamberName = (name) => L(FR_CHAMBERS[name] || name, name);

const FR_FORMAT = {
  AK: 'L’Alaska a une primaire à quatre qualifiés et le vote par classement à l’élection générale.',
  CA: 'La Californie a une primaire à deux qualifiés : deux candidats du même parti peuvent s’affronter en novembre.',
  DC: 'Le district de Columbia élit un délégué sans droit de vote à la Chambre des représentants et n’a pas d’assemblée d’État.',
  GA: 'La Géorgie exige la majorité pour gagner : une élection où personne ne dépasse 50 % va à un second tour.',
  LA: 'La Louisiane a choisi ses candidats au Sénat fédéral lors de primaires fermées. Cette année, ses élections à la Chambre sont des primaires ouvertes le 3 novembre, avec un second tour le 12 décembre si personne n’obtient la majorité. Le bulletin compte aussi 10 projets d’amendement constitutionnel et des élections locales ; l’assemblée sera élue en 2027.',
  ME: 'Le Maine utilise le vote par classement pour ses élections au Sénat et à la Chambre des représentants.',
  NE: 'Le Nebraska a une assemblée à chambre unique, officiellement non partisane.',
  NH: 'Le New Hampshire élit son gouverneur tous les deux ans.',
  NJ: 'Le New Jersey élit son assemblée les années impaires.',
  NY: 'L’État de New York autorise le vote de fusion : un candidat peut figurer sur la liste de plusieurs partis.',
  OR: 'L’Oregon vote entièrement par correspondance.',
  UT: 'L’Utah vote surtout par correspondance.',
  VT: 'Le Vermont élit son gouverneur tous les deux ans.',
  VA: 'La Virginie élit son assemblée les années impaires.',
  WA: 'L’État de Washington a une primaire à deux qualifiés et vote entièrement par correspondance.',
  WV: 'Chaque circonscription du Sénat de Virginie-Occidentale a deux sièges ; l’un est élu tous les deux ans.',
};
export const stateNote = (s) => (s?.format ? L(FR_FORMAT[s.abbr] || s.format, s.format) : '');

// States whose voter rolls record party registration, so early-vote returns can be
// split by party. Used by the demo early-vote panel.
export const PARTY_REGISTRATION = new Set('AK AZ CA CO CT DE DC FL IA ID KS KY LA ME MD MA NE NV NH NJ NM NY NC OK OR PA RI SD UT WV WY'.split(' '));

// Seats not on the 2026 ballot, by party, as of October 2026, and the current
// totals that expected gains are measured from. The refresh script recomputes both
// from Wikipedia's party summaries (data/control.json); these are the fallback.
// Senate: 53 R / 47 D (two independents caucus with Democrats); 35 seats are up.
// House: 218 R / 214 D / 1 independent / 2 vacant. Governors: 26 R / 24 D; 36 are up.
export const HOLDOVER = {
  senate: { D: 34, R: 31 },   // a 50-50 tie goes to the Republican vice president
  governor: { D: 6, R: 8 },
};
export const CURRENT = {
  senate: { D: 47, R: 53 },
  house: { D: 214, R: 218 },
  governor: { D: 24, R: 26 },
};

export const voteGovUrl = (st) => `https://vote.gov/register/${STATE_BY_ABBR[st].slug}`;
export const NASS_CAN_I_VOTE = 'https://www.nass.org/can-I-vote';

export function legislatureChambers(st) {
  const s = STATE_BY_ABBR[st];
  if (!s || s.noLegislature) return [];
  if (s.unicameral) return [{ key: 'leg', layer: 'sldu', ...s.upper }];
  return [
    { key: 'senate', layer: 'sldu', ...s.upper },
    { key: 'house', layer: 'sldl', ...s.lower },
  ];
}
