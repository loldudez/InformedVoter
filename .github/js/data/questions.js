// The "My views" questionnaire. Wording is the site owner's and is kept verbatim.
//
// `scope` limits a category to the races it applies to: federal races skip the
// state-and-local block, state races skip defense and foreign policy.
//
// `demoLean` is used ONLY to generate believable demo candidates (+1: agreeing is
// typically a Democratic position, -1: typically Republican, 0: cross-cutting).
// It is never shown and never used when scoring real matches.

export const SCALE = [
  { value: 2, label: 'Strongly agree' },
  { value: 1, label: 'Agree' },
  { value: 0, label: 'Neutral' },
  { value: -1, label: 'Disagree' },
  { value: -2, label: 'Strongly disagree' },
];
export const SCALE_LABEL = Object.fromEntries(SCALE.map((s) => [s.value, s.label]));

const CATS = [
  ['eco', 'Economy, taxes, business', 'all', [
    ['Do you support increasing taxes on high-income earners to fund public services?', 1],
    ['Do you support lowering taxes on middle- and working-class households?', 0],
    ['Do you support increasing the federal minimum wage?', 1],
    ['Do you support stronger antitrust laws to prevent monopolies and excessive corporate concentration?', 0.4],
    ['Do you support tax incentives for companies that manufacture goods domestically?', 0],
    ['Do you support increasing government investment in infrastructure, such as roads, railways, bridges, and ports?', 0.4],
    ['Do you support reducing government spending to lower the national debt?', -1],
    ['Do you support expanding tax credits for small businesses?', 0],
    ['Do you support stronger labor protections, including the right to unionize?', 1],
    ['Do you support tariffs on imported goods to protect domestic industries?', -0.8],
    ['Do you support paid family leave for workers?', 1],
    ['Do you support a more progressive tax system in which higher-income households pay a larger share of their income in taxes?', 1],
    ['Do you support reducing the amount of working hours in a week?', 0.6],
  ]],
  ['hea', 'Healthcare/Public Healthcare', 'all', [
    ['Do you support universal healthcare coverage?', 1],
    ['Do you support allowing the government to negotiate prescription drug prices?', 0.6],
    ['Do you support expanding public health insurance programs?', 1],
    ['Do you support maintaining a primarily private healthcare system?', -1],
    ['Do you support increasing federal funding for medical research?', 0.4],
    ['Do you support expanding mental health services?', 0.3],
    ['Do you support government subsidies to make health insurance more affordable?', 1],
    ['Do you support requiring health insurance plans to cover preexisting conditions?', 0.3],
    ['Do you support expanding access to preventive care and vaccinations?', 0.6],
    ['Do you support allowing Medicare to cover additional services, such as dental, vision, and hearing care?', 0.8],
  ]],
  ['edu', 'Education', 'all', [
    ['Do you support increasing funding for public schools?', 1],
    ['Do you support making public colleges and universities tuition-free?', 1],
    ['Do you support expanding vocational, apprenticeship, and technical education programs?', 0],
    ['Do you support increasing teacher salaries?', 0.4],
    ['Do you support student loan forgiveness for some or all borrowers?', 1],
    ['Do you support expanding school choice, including charter schools and school voucher programs?', -1],
    ['Do you support greater local control over school curricula?', -0.6],
    ['Do you support increasing funding for science, technology, engineering, and mathematics education?', 0.2],
    ['Do you support providing free school meals to all students?', 1],
    ['Do you support requiring financial literacy and civics courses in high school?', 0],
  ]],
  ['imm', 'Immigration and Border Security', 'all', [
    ['Do you support increasing funding for border security?', -1],
    ['Do you support creating a pathway to legal status or citizenship for certain undocumented immigrants?', 1],
    ['Do you support expanding legal immigration pathways for skilled workers?', 0.2],
    ['Do you support increasing the number of immigration judges to reduce case backlogs?', 0.2],
    ['Do you support stricter penalties for employers who knowingly hire unauthorized workers?', -0.5],
    ['Do you support increasing the number of refugees admitted to the country?', 1],
    ['Do you support prioritizing the deportation of immigrants convicted of serious crimes?', -0.4],
    ['Do you support increasing funding for immigration enforcement?', -1],
    ['Do you support expanding temporary work visas for agricultural and other labor shortages?', 0],
    ['Do you support requiring stronger employment verification for new hires?', -0.6],
  ]],
  ['cri', 'Crime, Policing, and justice system', 'all', [
    ['Do you support increasing funding for local police departments?', -1],
    ['Do you support requiring police officers to wear body cameras?', 0.3],
    ['Do you support independent investigations of alleged police misconduct?', 1],
    ['Do you support longer prison sentences for violent crimes?', -1],
    ['Do you support expanding rehabilitation and job-training programs for prisoners?', 0.4],
    ['Do you support eliminating cash bail for certain nonviolent offenses?', 1],
    ['Do you support increasing funding for community-based crime prevention?', 0.5],
    ['Do you support expanding access to mental health and substance-use treatment as alternatives to incarceration for some offenders?', 0.5],
    ['Do you support the death penalty for certain serious crimes?', -1],
    ['Do you support greater federal oversight of local law enforcement when civil rights violations are established?', 1],
  ]],
  ['soc', 'Social issues and civil liberties', 'all', [
    ['Do you support protecting freedom of speech, including speech that is unpopular or controversial?', 0],
    ['Do you support stronger federal protections against discrimination?', 1],
    ['Do you support legal abortion access?', 1],
    ['Do you support greater restrictions on abortion?', -1],
    ['Do you support legalizing recreational marijuana for adults?', 0.5],
    ['Do you support stronger protections for religious freedom?', -1],
    ['Do you support expanding access to affordable childcare?', 0.5],
    ['Do you support stronger privacy protections for personal data collected by technology companies?', 0.2],
    ['Do you support allowing adults to make their own end-of-life medical decisions under legally defined safeguards?', 0.5],
    ['Do you support stronger federal protections for same-sex marriage?', 1],
    ['Do you support ability for hormone transitioning under 18 years old?', 1],
    ['Do you support trans rights in general?', 1],
  ]],
  ['ene', 'Energy, environment, and climate', 'all', [
    ['Do you support expanding renewable energy, such as solar and wind?', 1],
    ['Do you support expanding nuclear power?', -0.2],
    ['Do you support increasing domestic oil and natural gas production?', -1],
    ['Do you support stronger regulations to reduce air and water pollution?', 1],
    ['Do you support government investment in electric vehicle infrastructure?', 1],
    ['Do you support carbon emissions limits for major industries?', 1],
    ['Do you support expanding public transportation and passenger rail?', 0.8],
    ['Do you support increasing funding for flood prevention, hurricane protection, and disaster preparedness?', 0.2],
    ['Do you support providing financial incentives for domestic energy manufacturing?', 0],
    ['Do you support prioritizing affordable energy prices even when doing so may slow the transition to lower-emission energy sources?', -1],
  ]],
  ['def', 'Defense, veterans, and foreign policy', 'federal', [
    ['Do you support increasing defense spending?', -1],
    ['Do you support maintaining the United States’ existing military alliances?', 0.5],
    ['Do you support increasing funding for veterans’ healthcare and benefits?', 0],
    ['Do you support requiring congressional authorization for most prolonged military engagements?', 0.3],
    ['Do you support providing military assistance to allied countries facing invasion?', 0.4],
    ['Do you support increasing domestic production of military equipment and ammunition?', 0],
    ['Do you support prioritizing diplomacy over military intervention when national security permits?', 0.4],
    ['Do you support maintaining a strong U.S. military presence overseas?', -0.3],
    ['Do you support expanding cybersecurity and critical-infrastructure defenses?', 0],
    ['Do you support reducing foreign aid to prioritize domestic spending?', -1],
    ['Do you support Israel’s government?', -0.6],
    ['Do you support foreign aid for Israel?', -0.4],
    ['Do you support foreign aid for Ukraine?', 0.6],
    ['Do you believe the current Russian government is a hostile state?', 0.4],
    ['Do you support intervention in Iran?', -0.5],
    ['Do you think the country should take a harsher stance against China?', -0.3],
    ['Do you think the country should work more with the European Union?', 0.6],
  ]],
  ['gov', 'Government Reform and democracy', 'all', [
    ['Do you support term limits for members of Congress?', -0.3],
    ['Do you support banning members of Congress from trading individual stocks?', 0],
    ['Do you support stricter campaign finance disclosure requirements?', 0.5],
    ['Do you support establishing independent commissions to draw congressional district boundaries?', 0.4],
    ['Do you support requiring voter identification at polling places?', -1],
    ['Do you support expanding early voting and access to mail-in ballots?', 1],
    ['Do you support ranked-choice voting in elections?', 0.3],
    ['Do you support eliminating or reforming the Electoral College?', 1],
    ['Do you support stronger ethics rules for elected officials?', 0.2],
    ['Do you support allowing citizens to propose ballot initiatives directly?', 0],
    ['Do you support reducing the influence of corporate political donations?', 1],
    ['Do you support greater transparency in government contracts and public spending?', 0],
    ['Do you believe that corporations and businesses should be able to finance campaigns?', -1],
  ]],
  ['hou', 'Housing, transportation, and infrastructure', 'all', [
    ['Do you support building more affordable housing through government funding?', 1],
    ['Do you support banning corporate investment into housing?', 0.3],
    ['Do you support increasing government funding for public transportation?', 1],
    ['Do you support zoning reforms that allow more homes to be built?', 0.1],
    ['Do you support government assistance for first-time homebuyers?', 0.4],
    ['Do you support stronger tenant protections against unfair eviction?', 1],
    ['Do you support expanding passenger rail between major American cities?', 0.8],
    ['Do you support increasing federal funding for highway maintenance and bridge repairs?', 0],
    ['Do you support expanding broadband internet access in rural communities?', 0],
    ['Do you support increasing funding for flood control and storm-resistant infrastructure?', 0.1],
    ['Do you support public-private partnerships to finance major infrastructure projects?', -0.3],
  ]],
  ['agr', 'Agriculture, manufacturing, and domestic production', 'all', [
    ['Do you support subsidies for American farmers?', -0.1],
    ['Do you support expanding domestic semiconductor manufacturing?', 0.1],
    ['Do you support incentives for companies to bring manufacturing jobs back to the United States?', 0],
    ['Do you support investing in domestic pharmaceutical production?', 0],
    ['Do you support strengthening the domestic supply chains for critical minerals and industrial materials?', 0],
    ['Do you support trade agreements that reduce barriers for American exporters?', 0],
    ['Do you support protecting domestic industries even if it increases some consumer prices?', -0.3],
    ['Do you support expanding agricultural research and drought-resistant crop development?', 0.2],
  ]],
  ['sta', 'State and local government', 'state', [
    ['Do you support increasing funding for local roads and bridges?', 0],
    ['Do you support increasing funding for public schools?', 1],
    ['Do you support raising the state minimum wage?', 1],
    ['Do you support property tax relief for homeowners?', -0.3],
    ['Do you support expanding state-funded flood protection and coastal restoration?', 0.1],
    ['Do you support stronger ethics and anti-corruption laws for state officials?', 0.1],
    ['Do you support expanding technical colleges and workforce training?', 0],
    ['Do you support increasing funding for state and local police?', -1],
    ['Do you support expanding public health clinics in rural communities?', 0.4],
    ['Do you support tax incentives for businesses that create jobs within the state?', -0.3],
    ['Do you support reviewing tax exemptions and subsidies to determine whether they deliver measurable public benefits?', 0.2],
    ['Do you support expanding passenger rail or other public transportation between major cities in your state?', 0.8],
  ]],
];

// "Do you support X?" -> stem "X" with verb "support"; also handles believe/think.
function parse(text) {
  const m = text.match(/^Do you (support|believe|think)\s+(?:that\s+)?(.*?)\??$/i);
  return m ? { verb: m[1].toLowerCase(), stem: m[2] } : { verb: 'support', stem: text.replace(/\?$/, '') };
}

export const CATEGORIES = CATS.map(([id, title, scope, items]) => ({
  id, title, scope,
  questions: items.map(([text, demoLean], i) => ({
    id: `${id}-${String(i + 1).padStart(2, '0')}`,
    cat: id, text, demoLean, ...parse(text),
  })),
}));

export const QUESTIONS = CATEGORIES.flatMap((c) => c.questions);
export const QUESTION_BY_ID = Object.fromEntries(QUESTIONS.map((q) => [q.id, q]));
export const CATEGORY_BY_ID = Object.fromEntries(CATEGORIES.map((c) => [c.id, c]));

export function questionsForLevel(level) {
  return CATEGORIES.filter((c) => c.scope === 'all' || c.scope === level).flatMap((c) => c.questions);
}

// "Jordan Lee strongly supports increasing taxes on ..." / "... agrees that the ..."
const SUPPORT = { 2: 'strongly supports', 1: 'supports', 0: 'is neutral or mixed on', '-1': 'opposes', '-2': 'strongly opposes' };
const AGREE = { 2: 'strongly agrees that', 1: 'agrees that', 0: 'is neutral on whether', '-1': 'disagrees that', '-2': 'strongly disagrees that' };
export function stanceSentence(name, q, stance) {
  const phrase = q.verb === 'support' ? SUPPORT[stance] : AGREE[stance];
  return `${name} ${phrase} ${q.stem}`;
}
export function userSentence(q, answer) {
  return `You ${SCALE_LABEL[answer].toLowerCase()}.`;
}
