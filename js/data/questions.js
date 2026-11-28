// The "My views" questionnaire. Wording is the site owner's and is kept verbatim; the
// French (each question's third entry, Nov. 25, 2026) is a labelled translation. A French
// stem is a noun phrase with its article for "Do you support" questions ("Êtes-vous
// favorable à …?") and a clause for "believe"/"think" ones ("Pensez-vous que …?"), so the
// same stem also makes the candidates' stance sentences.
//
// `scope` limits a category to the races it applies to: federal races skip the
// state-and-local block, state races skip defense and foreign policy.
//
// `demoLean` is used ONLY to generate believable demo candidates (+1: agreeing is
// typically a Democratic position, -1: typically Republican, 0: cross-cutting).
// It is never shown and never used when scoring real matches.

import { L, lang, frType } from '../i18n.js';

// The labels follow the visitor's language when read (getters), as the France section's do.
export const SCALE = [
  [2, 'Tout à fait d’accord', 'Strongly agree'],
  [1, 'Plutôt d’accord', 'Agree'],
  [0, 'Neutre', 'Neutral'],
  [-1, 'Plutôt pas d’accord', 'Disagree'],
  [-2, 'Pas du tout d’accord', 'Strongly disagree'],
].map(([value, fr, en]) => ({ value, get label() { return L(fr, en); } }));
export const SCALE_LABEL = {};
for (const s of SCALE) Object.defineProperty(SCALE_LABEL, s.value, { get: () => s.label, enumerable: true });

const CAT_FR = {
  eco: 'Économie, impôts, entreprises',
  hea: 'Santé et santé publique',
  edu: 'Éducation',
  imm: 'Immigration et sécurité des frontières',
  cri: 'Criminalité, police et justice',
  soc: 'Questions de société et libertés publiques',
  ene: 'Énergie, environnement et climat',
  def: 'Défense, anciens combattants et politique étrangère',
  gov: 'Réforme des institutions et démocratie',
  hou: 'Logement, transports et infrastructures',
  agr: 'Agriculture, industrie et production nationale',
  sta: 'Gouvernement de l’État et collectivités locales',
};

const CATS = [
  ['eco', 'Economy, taxes, business', 'all', [
    ['Do you support increasing taxes on high-income earners to fund public services?', 1, 'la hausse des impôts des hauts revenus pour financer les services publics'],
    ['Do you support lowering taxes on middle- and working-class households?', 0, 'la baisse des impôts des ménages des classes moyennes et populaires'],
    ['Do you support increasing the federal minimum wage?', 1, 'la hausse du salaire minimum fédéral'],
    ['Do you support stronger antitrust laws to prevent monopolies and excessive corporate concentration?', 0.4, 'des lois antitrust plus strictes pour empêcher les monopoles et la concentration excessive des entreprises'],
    ['Do you support tax incentives for companies that manufacture goods domestically?', 0, 'des avantages fiscaux pour les entreprises qui fabriquent leurs produits aux États-Unis'],
    ['Do you support increasing government investment in infrastructure, such as roads, railways, bridges, and ports?', 0.4, 'la hausse des investissements publics dans les infrastructures, comme les routes, les voies ferrées, les ponts et les ports'],
    ['Do you support reducing government spending to lower the national debt?', -1, 'la réduction des dépenses publiques pour diminuer la dette nationale'],
    ['Do you support expanding tax credits for small businesses?', 0, 'l’élargissement des crédits d’impôt pour les petites entreprises'],
    ['Do you support stronger labor protections, including the right to unionize?', 1, 'une meilleure protection des travailleurs, y compris le droit de se syndiquer'],
    ['Do you support tariffs on imported goods to protect domestic industries?', -0.8, 'des droits de douane sur les produits importés pour protéger l’industrie nationale'],
    ['Do you support paid family leave for workers?', 1, 'un congé familial payé pour les salariés'],
    ['Do you support a more progressive tax system in which higher-income households pay a larger share of their income in taxes?', 1, 'un système fiscal plus progressif, dans lequel les ménages aux revenus élevés paient une plus grande part de leurs revenus en impôts'],
    ['Do you support reducing the amount of working hours in a week?', 0.6, 'la réduction du nombre d’heures de travail par semaine'],
  ]],
  ['hea', 'Healthcare/Public Healthcare', 'all', [
    ['Do you support universal healthcare coverage?', 1, 'une couverture santé universelle'],
    ['Do you support allowing the government to negotiate prescription drug prices?', 0.6, 'la possibilité pour l’État de négocier le prix des médicaments sur ordonnance'],
    ['Do you support expanding public health insurance programs?', 1, 'l’extension des programmes publics d’assurance maladie'],
    ['Do you support maintaining a primarily private healthcare system?', -1, 'le maintien d’un système de santé principalement privé'],
    ['Do you support increasing federal funding for medical research?', 0.4, 'la hausse du financement fédéral de la recherche médicale'],
    ['Do you support expanding mental health services?', 0.3, 'le développement des services de santé mentale'],
    ['Do you support government subsidies to make health insurance more affordable?', 1, 'des aides publiques pour rendre l’assurance maladie plus abordable'],
    ['Do you support requiring health insurance plans to cover preexisting conditions?', 0.3, 'l’obligation pour les assurances maladie de couvrir les maladies préexistantes'],
    ['Do you support expanding access to preventive care and vaccinations?', 0.6, 'un meilleur accès aux soins de prévention et aux vaccins'],
    ['Do you support allowing Medicare to cover additional services, such as dental, vision, and hearing care?', 0.8, 'l’extension de Medicare à d’autres soins, comme les soins dentaires, ophtalmologiques et auditifs'],
  ]],
  ['edu', 'Education', 'all', [
    ['Do you support increasing funding for public schools?', 1, 'la hausse du financement des écoles publiques'],
    ['Do you support making public colleges and universities tuition-free?', 1, 'la gratuité des frais de scolarité dans les universités publiques'],
    ['Do you support expanding vocational, apprenticeship, and technical education programs?', 0, 'le développement de la formation professionnelle, de l’apprentissage et de l’enseignement technique'],
    ['Do you support increasing teacher salaries?', 0.4, 'la hausse des salaires des enseignants'],
    ['Do you support student loan forgiveness for some or all borrowers?', 1, 'l’annulation des prêts étudiants pour une partie ou la totalité des emprunteurs'],
    ['Do you support expanding school choice, including charter schools and school voucher programs?', -1, 'l’élargissement du libre choix de l’école, y compris les écoles à charte (charter schools) et les chèques éducation'],
    ['Do you support greater local control over school curricula?', -0.6, 'un plus grand contrôle local sur les programmes scolaires'],
    ['Do you support increasing funding for science, technology, engineering, and mathematics education?', 0.2, 'la hausse du financement de l’enseignement des sciences, des technologies, de l’ingénierie et des mathématiques'],
    ['Do you support providing free school meals to all students?', 1, 'la gratuité des repas scolaires pour tous les élèves'],
    ['Do you support requiring financial literacy and civics courses in high school?', 0, 'des cours obligatoires d’éducation financière et d’éducation civique au lycée'],
  ]],
  ['imm', 'Immigration and Border Security', 'all', [
    ['Do you support increasing funding for border security?', -1, 'la hausse du financement de la sécurité aux frontières'],
    ['Do you support creating a pathway to legal status or citizenship for certain undocumented immigrants?', 1, 'la création d’une voie d’accès à un statut légal ou à la citoyenneté pour certains immigrés sans papiers'],
    ['Do you support expanding legal immigration pathways for skilled workers?', 0.2, 'l’élargissement des voies d’immigration légale pour les travailleurs qualifiés'],
    ['Do you support increasing the number of immigration judges to reduce case backlogs?', 0.2, 'la hausse du nombre de juges de l’immigration pour réduire les dossiers en attente'],
    ['Do you support stricter penalties for employers who knowingly hire unauthorized workers?', -0.5, 'des sanctions plus sévères pour les employeurs qui embauchent sciemment des travailleurs sans autorisation de travail'],
    ['Do you support increasing the number of refugees admitted to the country?', 1, 'la hausse du nombre de réfugiés accueillis dans le pays'],
    ['Do you support prioritizing the deportation of immigrants convicted of serious crimes?', -0.4, 'l’expulsion en priorité des immigrés condamnés pour des crimes graves'],
    ['Do you support increasing funding for immigration enforcement?', -1, 'la hausse du financement de l’application des lois sur l’immigration'],
    ['Do you support expanding temporary work visas for agricultural and other labor shortages?', 0, 'l’élargissement des visas de travail temporaires pour l’agriculture et les autres secteurs qui manquent de main-d’œuvre'],
    ['Do you support requiring stronger employment verification for new hires?', -0.6, 'une vérification renforcée du droit au travail des nouvelles recrues'],
  ]],
  ['cri', 'Crime, Policing, and justice system', 'all', [
    ['Do you support increasing funding for local police departments?', -1, 'la hausse du financement des polices locales'],
    ['Do you support requiring police officers to wear body cameras?', 0.3, 'le port obligatoire de caméras-piétons par les policiers'],
    ['Do you support independent investigations of alleged police misconduct?', 1, 'des enquêtes indépendantes sur les fautes présumées de policiers'],
    ['Do you support longer prison sentences for violent crimes?', -1, 'des peines de prison plus longues pour les crimes violents'],
    ['Do you support expanding rehabilitation and job-training programs for prisoners?', 0.4, 'le développement des programmes de réinsertion et de formation professionnelle pour les détenus'],
    ['Do you support eliminating cash bail for certain nonviolent offenses?', 1, 'la suppression de la caution en argent pour certaines infractions non violentes'],
    ['Do you support increasing funding for community-based crime prevention?', 0.5, 'la hausse du financement de la prévention de la délinquance de proximité'],
    ['Do you support expanding access to mental health and substance-use treatment as alternatives to incarceration for some offenders?', 0.5, 'un meilleur accès aux soins de santé mentale et au traitement des addictions comme alternatives à l’incarcération pour certains délinquants'],
    ['Do you support the death penalty for certain serious crimes?', -1, 'la peine de mort pour certains crimes graves'],
    ['Do you support greater federal oversight of local law enforcement when civil rights violations are established?', 1, 'un contrôle fédéral renforcé sur les polices locales quand des violations des droits civiques sont établies'],
  ]],
  ['soc', 'Social issues and civil liberties', 'all', [
    ['Do you support protecting freedom of speech, including speech that is unpopular or controversial?', 0, 'la protection de la liberté d’expression, y compris pour des propos impopulaires ou controversés'],
    ['Do you support stronger federal protections against discrimination?', 1, 'une protection fédérale renforcée contre les discriminations'],
    ['Do you support legal abortion access?', 1, 'l’accès légal à l’avortement'],
    ['Do you support greater restrictions on abortion?', -1, 'des restrictions plus fortes sur l’avortement'],
    ['Do you support legalizing recreational marijuana for adults?', 0.5, 'la légalisation du cannabis récréatif pour les adultes'],
    ['Do you support stronger protections for religious freedom?', -1, 'une protection renforcée de la liberté religieuse'],
    ['Do you support expanding access to affordable childcare?', 0.5, 'un meilleur accès à des modes de garde d’enfants abordables'],
    ['Do you support stronger privacy protections for personal data collected by technology companies?', 0.2, 'une meilleure protection des données personnelles collectées par les entreprises technologiques'],
    ['Do you support allowing adults to make their own end-of-life medical decisions under legally defined safeguards?', 0.5, 'la possibilité pour les adultes de prendre leurs propres décisions médicales de fin de vie, avec des garanties fixées par la loi'],
    ['Do you support stronger federal protections for same-sex marriage?', 1, 'une protection fédérale renforcée du mariage entre personnes de même sexe'],
    ['Do you support ability for hormone transitioning under 18 years old?', 1, 'la possibilité d’une transition hormonale avant 18 ans'],
    ['Do you support trans rights in general?', 1, 'les droits des personnes trans en général'],
  ]],
  ['ene', 'Energy, environment, and climate', 'all', [
    ['Do you support expanding renewable energy, such as solar and wind?', 1, 'le développement des énergies renouvelables, comme le solaire et l’éolien'],
    ['Do you support expanding nuclear power?', -0.2, 'le développement de l’énergie nucléaire'],
    ['Do you support increasing domestic oil and natural gas production?', -1, 'la hausse de la production nationale de pétrole et de gaz naturel'],
    ['Do you support stronger regulations to reduce air and water pollution?', 1, 'des règles plus strictes pour réduire la pollution de l’air et de l’eau'],
    ['Do you support government investment in electric vehicle infrastructure?', 1, 'l’investissement public dans les infrastructures pour véhicules électriques'],
    ['Do you support carbon emissions limits for major industries?', 1, 'des plafonds d’émissions de carbone pour les grandes industries'],
    ['Do you support expanding public transportation and passenger rail?', 0.8, 'le développement des transports en commun et des trains de voyageurs'],
    ['Do you support increasing funding for flood prevention, hurricane protection, and disaster preparedness?', 0.2, 'la hausse du financement de la prévention des inondations, de la protection contre les ouragans et de la préparation aux catastrophes'],
    ['Do you support providing financial incentives for domestic energy manufacturing?', 0, 'des incitations financières à la fabrication d’équipements énergétiques aux États-Unis'],
    ['Do you support prioritizing affordable energy prices even when doing so may slow the transition to lower-emission energy sources?', -1, 'la priorité à des prix de l’énergie abordables, même si cela peut ralentir la transition vers des sources d’énergie moins émettrices'],
  ]],
  ['def', 'Defense, veterans, and foreign policy', 'federal', [
    ['Do you support increasing defense spending?', -1, 'la hausse des dépenses de défense'],
    ['Do you support maintaining the United States’ existing military alliances?', 0.5, 'le maintien des alliances militaires actuelles des États-Unis'],
    ['Do you support increasing funding for veterans’ healthcare and benefits?', 0, 'la hausse du financement des soins et des prestations des anciens combattants'],
    ['Do you support requiring congressional authorization for most prolonged military engagements?', 0.3, 'l’obligation d’obtenir l’autorisation du Congrès pour la plupart des engagements militaires prolongés'],
    ['Do you support providing military assistance to allied countries facing invasion?', 0.4, 'l’aide militaire aux pays alliés face à une invasion'],
    ['Do you support increasing domestic production of military equipment and ammunition?', 0, 'la hausse de la production nationale d’équipements militaires et de munitions'],
    ['Do you support prioritizing diplomacy over military intervention when national security permits?', 0.4, 'la priorité à la diplomatie plutôt qu’à l’intervention militaire quand la sécurité nationale le permet'],
    ['Do you support maintaining a strong U.S. military presence overseas?', -0.3, 'le maintien d’une forte présence militaire américaine à l’étranger'],
    ['Do you support expanding cybersecurity and critical-infrastructure defenses?', 0, 'le renforcement de la cybersécurité et de la protection des infrastructures critiques'],
    ['Do you support reducing foreign aid to prioritize domestic spending?', -1, 'la réduction de l’aide à l’étranger au profit des dépenses intérieures'],
    ['Do you support Israel’s government?', -0.6, 'le gouvernement israélien'],
    ['Do you support foreign aid for Israel?', -0.4, 'l’aide à Israël'],
    ['Do you support foreign aid for Ukraine?', 0.6, 'l’aide à l’Ukraine'],
    ['Do you believe the current Russian government is a hostile state?', 0.4, 'l’actuel gouvernement russe est un État hostile'],
    ['Do you support intervention in Iran?', -0.5, 'une intervention en Iran'],
    ['Do you think the country should take a harsher stance against China?', -0.3, 'le pays devrait adopter une position plus ferme envers la Chine'],
    ['Do you think the country should work more with the European Union?', 0.6, 'le pays devrait travailler davantage avec l’Union européenne'],
  ]],
  ['gov', 'Government Reform and democracy', 'all', [
    ['Do you support term limits for members of Congress?', -0.3, 'la limitation du nombre de mandats des membres du Congrès'],
    ['Do you support banning members of Congress from trading individual stocks?', 0, 'l’interdiction pour les membres du Congrès d’acheter et de vendre des actions individuelles'],
    ['Do you support stricter campaign finance disclosure requirements?', 0.5, 'des règles plus strictes de transparence sur le financement des campagnes'],
    ['Do you support establishing independent commissions to draw congressional district boundaries?', 0.4, 'la création de commissions indépendantes pour tracer les circonscriptions du Congrès'],
    ['Do you support requiring voter identification at polling places?', -1, 'l’obligation de présenter une pièce d’identité dans les bureaux de vote'],
    ['Do you support expanding early voting and access to mail-in ballots?', 1, 'l’élargissement du vote anticipé et du vote par correspondance'],
    ['Do you support ranked-choice voting in elections?', 0.3, 'le vote par classement (ranked-choice voting) lors des élections'],
    ['Do you support eliminating or reforming the Electoral College?', 1, 'la suppression ou la réforme du collège électoral'],
    ['Do you support stronger ethics rules for elected officials?', 0.2, 'des règles déontologiques plus strictes pour les élus'],
    ['Do you support allowing citizens to propose ballot initiatives directly?', 0, 'la possibilité pour les citoyens de proposer directement des initiatives populaires soumises au vote'],
    ['Do you support reducing the influence of corporate political donations?', 1, 'la réduction de l’influence des dons politiques des entreprises'],
    ['Do you support greater transparency in government contracts and public spending?', 0, 'plus de transparence sur les marchés publics et les dépenses publiques'],
    ['Do you believe that corporations and businesses should be able to finance campaigns?', -1, 'les entreprises et les sociétés devraient pouvoir financer les campagnes électorales'],
  ]],
  ['hou', 'Housing, transportation, and infrastructure', 'all', [
    ['Do you support building more affordable housing through government funding?', 1, 'la construction de davantage de logements abordables grâce à des fonds publics'],
    ['Do you support banning corporate investment into housing?', 0.3, 'l’interdiction des investissements des entreprises dans le logement'],
    ['Do you support increasing government funding for public transportation?', 1, 'la hausse du financement public des transports en commun'],
    ['Do you support zoning reforms that allow more homes to be built?', 0.1, 'des réformes du zonage qui permettent de construire plus de logements'],
    ['Do you support government assistance for first-time homebuyers?', 0.4, 'une aide publique aux primo-accédants'],
    ['Do you support stronger tenant protections against unfair eviction?', 1, 'une meilleure protection des locataires contre les expulsions abusives'],
    ['Do you support expanding passenger rail between major American cities?', 0.8, 'le développement des trains de voyageurs entre les grandes villes américaines'],
    ['Do you support increasing federal funding for highway maintenance and bridge repairs?', 0, 'la hausse du financement fédéral de l’entretien des autoroutes et de la réparation des ponts'],
    ['Do you support expanding broadband internet access in rural communities?', 0, 'l’extension de l’internet haut débit dans les zones rurales'],
    ['Do you support increasing funding for flood control and storm-resistant infrastructure?', 0.1, 'la hausse du financement de la protection contre les inondations et des infrastructures résistantes aux tempêtes'],
    ['Do you support public-private partnerships to finance major infrastructure projects?', -0.3, 'des partenariats public-privé pour financer les grands projets d’infrastructure'],
  ]],
  ['agr', 'Agriculture, manufacturing, and domestic production', 'all', [
    ['Do you support subsidies for American farmers?', -0.1, 'les subventions versées aux agriculteurs américains'],
    ['Do you support expanding domestic semiconductor manufacturing?', 0.1, 'le développement de la fabrication de semi-conducteurs aux États-Unis'],
    ['Do you support incentives for companies to bring manufacturing jobs back to the United States?', 0, 'des incitations pour que les entreprises ramènent des emplois industriels aux États-Unis'],
    ['Do you support investing in domestic pharmaceutical production?', 0, 'l’investissement dans la production pharmaceutique nationale'],
    ['Do you support strengthening the domestic supply chains for critical minerals and industrial materials?', 0, 'le renforcement des chaînes d’approvisionnement nationales en minerais critiques et en matériaux industriels'],
    ['Do you support trade agreements that reduce barriers for American exporters?', 0, 'des accords commerciaux qui réduisent les obstacles pour les exportateurs américains'],
    ['Do you support protecting domestic industries even if it increases some consumer prices?', -0.3, 'la protection de l’industrie nationale, même si certains prix à la consommation augmentent'],
    ['Do you support expanding agricultural research and drought-resistant crop development?', 0.2, 'le développement de la recherche agricole et de cultures résistantes à la sécheresse'],
  ]],
  ['sta', 'State and local government', 'state', [
    ['Do you support increasing funding for local roads and bridges?', 0, 'la hausse du financement des routes et des ponts locaux'],
    ['Do you support increasing funding for public schools?', 1, 'la hausse du financement des écoles publiques'],
    ['Do you support raising the state minimum wage?', 1, 'la hausse du salaire minimum de l’État'],
    ['Do you support property tax relief for homeowners?', -0.3, 'un allègement de la taxe foncière pour les propriétaires'],
    ['Do you support expanding state-funded flood protection and coastal restoration?', 0.1, 'le développement de la protection contre les inondations et de la restauration du littoral financées par l’État'],
    ['Do you support stronger ethics and anti-corruption laws for state officials?', 0.1, 'des lois plus strictes sur l’éthique et la lutte contre la corruption pour les responsables de l’État'],
    ['Do you support expanding technical colleges and workforce training?', 0, 'le développement des écoles techniques et de la formation professionnelle'],
    ['Do you support increasing funding for state and local police?', -1, 'la hausse du financement de la police de l’État et des polices locales'],
    ['Do you support expanding public health clinics in rural communities?', 0.4, 'le développement des centres de santé publics dans les zones rurales'],
    ['Do you support tax incentives for businesses that create jobs within the state?', -0.3, 'des avantages fiscaux pour les entreprises qui créent des emplois dans l’État'],
    ['Do you support reviewing tax exemptions and subsidies to determine whether they deliver measurable public benefits?', 0.2, 'le réexamen des exonérations fiscales et des subventions pour vérifier qu’elles apportent des bénéfices publics mesurables'],
    ['Do you support expanding passenger rail or other public transportation between major cities in your state?', 0.8, 'le développement des trains de voyageurs ou d’autres transports en commun entre les grandes villes de votre État'],
  ]],
];

// "Do you support X?" -> stem "X" with verb "support"; also handles believe/think.
function parse(text) {
  const m = text.match(/^Do you (support|believe|think)\s+(?:that\s+)?(.*?)\??$/i);
  return m ? { verb: m[1].toLowerCase(), stem: m[2] } : { verb: 'support', stem: text.replace(/\?$/, '') };
}

// "à" before a French stem: "à la", "à l’", "à des", but "au" and "aux".
const aFr = (s) => (s.startsWith('le ') ? `au ${s.slice(3)}` : s.startsWith('les ') ? `aux ${s.slice(4)}` : `à ${s}`);

export const CATEGORIES = CATS.map(([id, title, scope, items]) => ({
  id, title, titleFr: CAT_FR[id], scope,
  questions: items.map(([text, demoLean, frStem], i) => {
    const p = parse(text);
    return {
      id: `${id}-${String(i + 1).padStart(2, '0')}`,
      cat: id, text, demoLean, ...p, frStem,
      fr: p.verb === 'support' ? `Êtes-vous favorable ${aFr(frStem)} ?` : `Pensez-vous que ${frStem} ?`,
    };
  }),
}));

// The question and its topic in the visitor's language.
export const qText = (q) => L(q.fr, q.text);
export const catTitle = (c) => L(c.titleFr, c.title);

export const QUESTIONS = CATEGORIES.flatMap((c) => c.questions);
export const QUESTION_BY_ID = Object.fromEntries(QUESTIONS.map((q) => [q.id, q]));
export const CATEGORY_BY_ID = Object.fromEntries(CATEGORIES.map((c) => [c.id, c]));

export function questionsForLevel(level) {
  return CATEGORIES.filter((c) => c.scope === 'all' || c.scope === level).flatMap((c) => c.questions);
}

// "Jordan Lee strongly supports increasing taxes on ..." / "... agrees that the ..."
const SUPPORT = { 2: 'strongly supports', 1: 'supports', 0: 'is neutral or mixed on', '-1': 'opposes', '-2': 'strongly opposes' };
const AGREE = { 2: 'strongly agrees that', 1: 'agrees that', 0: 'is neutral on whether', '-1': 'disagrees that', '-2': 'strongly disagrees that' };
// French, worded so it needs no gender agreement: "Jordan Lee soutient la hausse …",
// "… s’oppose à la hausse …", "… est d’accord pour dire que …".
const SUPPORT_FR = { 2: (s) => `soutient fermement ${s}`, 1: (s) => `soutient ${s}`, 0: (s) => `n’a pas de position tranchée sur ${s}`, '-1': (s) => `s’oppose ${aFr(s)}`, '-2': (s) => `s’oppose fermement ${aFr(s)}` };
const AGREE_FR = { 2: 'est tout à fait d’accord pour dire que', 1: 'est d’accord pour dire que', 0: 'n’a pas d’avis tranché sur l’idée que', '-1': 'n’est pas d’accord pour dire que', '-2': 'n’est pas du tout d’accord pour dire que' };
export function stanceSentence(name, q, stance) {
  if (lang() === 'fr') return frType(`${name} ${q.verb === 'support' ? SUPPORT_FR[stance](q.frStem) : `${AGREE_FR[stance]} ${q.frStem}`}`);
  const phrase = q.verb === 'support' ? SUPPORT[stance] : AGREE[stance];
  return `${name} ${phrase} ${q.stem}`;
}
const YOU_FR = { 2: 'Vous êtes tout à fait d’accord.', 1: 'Vous êtes plutôt d’accord.', 0: 'Vous êtes neutre.', '-1': 'Vous n’êtes plutôt pas d’accord.', '-2': 'Vous n’êtes pas du tout d’accord.' };
export function userSentence(q, answer) {
  return L(YOU_FR[answer], `You ${SCALE_LABEL[answer].toLowerCase()}.`);
}
