// The France section's "Mes opinions" questionnaire. The French wording is the site
// owner's and is kept verbatim, numbered as the owner numbered it (1 to 144). The
// English is a translation for visitors who choose English, labelled as such on screen;
// the French text stays the reference.
//
// "Êtes-vous favorable à…" questions answer from "Très favorable" to "Très défavorable";
// "Pensez-vous que…" questions from "Tout à fait d'accord" to "Pas du tout d'accord".
// Both scales run from +2 to -2, so matching treats them alike.

import { L } from '../i18n.js';

const SECTIONS = [
  ['ins', 'Institutions, gouvernement et République française', 'Institutions, government and the French Republic', [
    ["Êtes-vous favorable au maintien de la Ve République, avec un président de la République et un Premier ministre ?", 'Do you support keeping the Fifth Republic, with a President of the Republic and a Prime Minister?'],
    ["Êtes-vous favorable à une réduction des pouvoirs du président de la République ?", 'Do you support reducing the powers of the President of the Republic?'],
    ["Êtes-vous favorable à un renforcement des pouvoirs de l'Assemblée nationale dans l'élaboration des politiques publiques ?", 'Do you support giving the National Assembly more power in making public policy?'],
    ["Êtes-vous favorable au remplacement du scrutin législatif actuel à deux tours par un scrutin proportionnel ?", 'Do you support replacing the current two-round legislative voting system with proportional representation?'],
    ["Êtes-vous favorable à l'abaissement de l'âge du droit de vote de 18 à 16 ans pour les élections nationales ?", 'Do you support lowering the voting age from 18 to 16 for national elections?'],
    ["Êtes-vous favorable à l'obligation de voter aux élections en France ?", 'Do you support making voting compulsory in French elections?'],
    ["Êtes-vous favorable à la mise en place d'un référendum d'initiative citoyenne permettant aux citoyens de soumettre des propositions au vote national selon certaines conditions ?", 'Do you support a citizens’ initiative referendum allowing citizens to put proposals to a national vote under certain conditions?'],
    ["Êtes-vous favorable à des limites plus strictes concernant le nombre de mandats consécutifs que peuvent exercer les élus ?", 'Do you support stricter limits on the number of consecutive terms elected officials can serve?'],
    ["Êtes-vous favorable au transfert de davantage de compétences de l'État vers les régions, les départements et les communes ?", 'Do you support transferring more powers from the State to regions, departments and communes?'],
    ["Êtes-vous favorable au renforcement des obligations de transparence et des mesures de lutte contre la corruption pour les responsables publics ?", 'Do you support stronger transparency obligations and anti-corruption measures for public officials?'],
    ["Êtes-vous favorable à l'inscription dans la loi d'obligations de responsabilité budgétaire pour tous les députés de l'Assemblée nationale, notamment en matière de maîtrise des dépenses publiques ?", 'Do you support writing budget-responsibility obligations into law for all members of the National Assembly, especially on controlling public spending?'],
    ["Êtes-vous favorable à une réduction de la bureaucratie administrative en France afin de simplifier les démarches des citoyens et des entreprises ?", 'Do you support reducing administrative bureaucracy in France to simplify procedures for citizens and businesses?'],
  ]],
  ['eco', 'Économie, fiscalité et finances publiques', 'Economy, taxation and public finances', [
    ["Êtes-vous favorable à une augmentation des impôts pour les personnes aux revenus les plus élevés ?", 'Do you support raising taxes on the highest earners?'],
    ["Êtes-vous favorable à la création ou au renforcement d'un impôt sur les grandes fortunes ?", 'Do you support creating or strengthening a tax on large fortunes?'],
    ["Êtes-vous favorable à une réduction des impôts pour les petites entreprises et les travailleurs indépendants ?", 'Do you support lowering taxes for small businesses and the self-employed?'],
    ["Êtes-vous favorable à une réduction de l'impôt sur les sociétés afin d'encourager l'investissement des entreprises en France ?", 'Do you support cutting corporate tax to encourage business investment in France?'],
    ["Êtes-vous favorable à une augmentation du salaire minimum interprofessionnel de croissance (SMIC) ?", 'Do you support raising the national minimum wage (SMIC)?'],
    ["Êtes-vous favorable à une réduction des impôts pour les personnes dont les revenus sont inférieurs au salaire médian ?", 'Do you support lowering taxes for people earning less than the median wage?'],
    ["Êtes-vous favorable à une réduction de la durée légale du travail en dessous de 35 heures par semaine ?", 'Do you support reducing the legal working week below 35 hours?'],
    ["Êtes-vous favorable à un assouplissement des règles encadrant l'embauche et le licenciement des salariés ?", 'Do you support relaxing the rules on hiring and dismissing employees?'],
    ["Êtes-vous favorable à une augmentation des investissements publics dans l'industrie et la production manufacturière françaises ?", 'Do you support more public investment in French industry and manufacturing?'],
    ["Êtes-vous favorable à la réduction de la dette publique par des diminutions des dépenses de l'État ?", 'Do you support reducing public debt by cutting State spending?'],
    ["Êtes-vous favorable à une augmentation des dépenses publiques consacrées aux services essentiels, même si elle ralentit la réduction du déficit public ?", 'Do you support more public spending on essential services, even if it slows the reduction of the public deficit?'],
    ["Êtes-vous favorable à la suppression de la règle européenne fixant à 3 % du produit intérieur brut (PIB) la valeur de référence pour le déficit public ?", 'Do you support abolishing the European rule that sets 3% of gross domestic product (GDP) as the reference value for the public deficit?'],
    ["Êtes-vous favorable au renforcement des mesures gouvernementales visant à lutter contre la fraude et l'évasion fiscales ?", 'Do you support stronger government measures against tax fraud and tax evasion?'],
    ["Êtes-vous favorable à une augmentation des aides financières publiques destinées aux agriculteurs et aux producteurs agricoles français ?", 'Do you support more public financial aid for French farmers and agricultural producers?'],
    ["Êtes-vous favorable à la nationalisation de secteurs stratégiques tels que l'énergie, les transports et la distribution de l'eau ?", 'Do you support nationalizing strategic sectors such as energy, transport and water distribution?'],
  ]],
  ['ret', 'Retraites, travail et protection sociale', 'Pensions, work and social protection', [
    ["Êtes-vous favorable au maintien de l'âge légal de départ à la retraite à 64 ans ?", 'Do you support keeping the legal retirement age at 64?'],
    ["Êtes-vous favorable à l'abaissement de l'âge légal de départ à la retraite à 62 ans ?", 'Do you support lowering the legal retirement age to 62?'],
    ["Êtes-vous favorable à la possibilité pour les travailleurs exerçant des métiers pénibles de partir à la retraite plus tôt ?", 'Do you support allowing workers in physically demanding jobs to retire earlier?'],
    ["Êtes-vous favorable à un système de retraite reposant davantage sur l'épargne individuelle et les dispositifs privés de retraite complémentaire ?", 'Do you support a pension system relying more on individual savings and private supplementary pension schemes?'],
    ["Êtes-vous favorable au maintien du système français d'assurance maladie universelle ?", 'Do you support keeping France’s universal health insurance system?'],
    ["Êtes-vous favorable à une augmentation des financements publics destinés aux hôpitaux et aux services d'urgence ?", 'Do you support more public funding for hospitals and emergency services?'],
    ["Êtes-vous favorable à une augmentation des allocations chômage pour les personnes qui remplissent les conditions requises ?", 'Do you support higher unemployment benefits for people who meet the requirements?'],
    ["Êtes-vous favorable à des conditions plus strictes pour bénéficier des allocations chômage, notamment en matière de recherche d'emploi ?", 'Do you support stricter conditions for unemployment benefits, especially on job seeking?'],
    ["Êtes-vous favorable à une extension des services publics de garde d'enfants et des congés parentaux ?", 'Do you support expanding public childcare and parental leave?'],
    ["Êtes-vous favorable à une augmentation des aides financières destinées aux ménages à faibles revenus ?", 'Do you support more financial aid for low-income households?'],
    ["Êtes-vous favorable à l'adoption d'un système de retraite inspiré du modèle néerlandais, dans lequel l'âge de départ évolue en fonction de l'espérance de vie et les revenus des retraités reposent sur plusieurs sources complémentaires ?", 'Do you support a pension system inspired by the Dutch model, where the retirement age follows life expectancy and retirees’ income comes from several complementary sources?'],
    ["Êtes-vous favorable à l'interdiction des expulsions locatives tant qu'une solution de relogement n'a pas été proposée aux personnes concernées ?", 'Do you support banning evictions of tenants until rehousing has been offered to them?'],
  ]],
  ['imm', 'Immigration, intégration, citoyenneté et fin de vie', 'Immigration, integration, citizenship and end of life', [
    ["Êtes-vous favorable à une réduction du nombre d'immigrés admis chaque année en France ?", 'Do you support reducing the number of immigrants admitted to France each year?'],
    ["Êtes-vous favorable à une augmentation de l'immigration de travail dans les secteurs confrontés à des pénuries de main-d'œuvre ?", 'Do you support more labor immigration in sectors facing worker shortages?'],
    ["Êtes-vous favorable au renforcement de la protection humanitaire accordée aux réfugiés et aux demandeurs d'asile ?", 'Do you support stronger humanitarian protection for refugees and asylum seekers?'],
    ["Êtes-vous favorable à l'accélération des procédures d'éloignement des personnes dont la demande d'asile a été rejetée et qui n'ont pas le droit de rester en France ?", 'Do you support speeding up removals of people whose asylum claims were rejected and who have no right to stay in France?'],
    ["Êtes-vous favorable à des exigences plus strictes en matière de maîtrise du français pour obtenir la nationalité française par naturalisation ?", 'Do you support stricter French-language requirements for citizenship by naturalization?'],
    ["Êtes-vous favorable à une réduction de la durée de résidence légale exigée pour les personnes souhaitant obtenir la nationalité française par naturalisation ?", 'Do you support shortening the legal residence required to obtain French citizenship by naturalization?'],
    ["Êtes-vous favorable à la régularisation de certains étrangers en situation irrégulière, sous des conditions précises liées notamment à l'emploi ou aux attaches familiales ?", 'Do you support granting legal status to some undocumented foreigners, under specific conditions such as employment or family ties?'],
    ["Êtes-vous favorable à une augmentation des financements publics destinés à l'intégration des immigrés, notamment pour l'apprentissage du français ?", 'Do you support more public funding to integrate immigrants, especially for learning French?'],
    ["Êtes-vous favorable au renforcement des contrôles aux frontières françaises, dans le respect des obligations juridiques européennes et internationales de la France ?", 'Do you support stronger controls at France’s borders, within France’s European and international legal obligations?'],
    ["Êtes-vous favorable au maintien de la possibilité pour les citoyens français et les personnes naturalisées françaises de posséder une double nationalité ?", 'Do you support keeping the right of French citizens, including naturalized citizens, to hold dual nationality?'],
    ["Êtes-vous favorable à l'expulsion du territoire français des étrangers condamnés pour des infractions pénales commises en France, lorsque la loi le permet ?", 'Do you support expelling foreigners convicted of criminal offenses committed in France, where the law allows?'],
    ["Êtes-vous favorable à l'expulsion d'étrangers condamnés pour des infractions pénales même lorsque leur retour dans leur pays d'origine risque de les exposer à des persécutions ou à des violences ?", 'Do you support expelling foreigners convicted of criminal offenses even when returning to their country of origin may expose them to persecution or violence?'],
    ["Êtes-vous favorable à une augmentation du nombre de réfugiés accueillis chaque année par la France ?", 'Do you support France taking in more refugees each year?'],
    ["Êtes-vous favorable à des politiques d'intégration plus strictes, pouvant notamment inclure l'obligation de franciser son nom ou son prénom, ou l'interdiction de certaines pratiques culturelles ou religieuses ?", 'Do you support stricter integration policies, which could include requiring people to gallicize their surname or first name, or banning certain cultural or religious practices?'],
    ["Êtes-vous favorable au droit à l'aide à mourir dans un cadre médical et légal strict ?", 'Do you support a right to assisted dying within a strict medical and legal framework?'],
  ]],
  ['ide', 'Identité française, laïcité et libertés individuelles', 'French identity, secularism and individual freedoms', [
    ["Êtes-vous favorable au maintien de la laïcité, notamment du principe de séparation des religions et de l'État, comme fondement de la République française ?", 'Do you support keeping laïcité, including the separation of religion and State, as a foundation of the French Republic?'],
    ["Êtes-vous favorable à des restrictions plus strictes concernant le port de signes religieux par les agents publics dans l'exercice de leurs fonctions ?", 'Do you support stricter limits on public employees wearing religious symbols on duty?'],
    ["Êtes-vous favorable au maintien de l'interdiction des signes religieux ostensibles dans les écoles, collèges et lycées publics ?", 'Do you support keeping the ban on conspicuous religious symbols in public primary, middle and high schools?'],
    ["Êtes-vous favorable à l'extension des restrictions concernant le port de signes religieux à d'autres espaces publics ?", 'Do you support extending limits on religious symbols to other public spaces?'],
    ["Êtes-vous favorable au renforcement des mesures de lutte contre les discriminations fondées sur la religion ou l'origine culturelle ?", 'Do you support stronger measures against discrimination based on religion or cultural origin?'],
    ["Êtes-vous favorable à une augmentation des financements publics destinés à préserver la langue française et le patrimoine culturel français ?", 'Do you support more public funding to preserve the French language and French cultural heritage?'],
    ["Êtes-vous favorable au renforcement des protections juridiques contre les discriminations visant les personnes LGBTQ+ ?", 'Do you support stronger legal protections against discrimination targeting LGBTQ+ people?'],
    ["Êtes-vous favorable au maintien de la liberté de recourir à l'interruption volontaire de grossesse (IVG), inscrite dans la Constitution française ?", 'Do you support keeping the freedom to have an abortion (IVG), written into the French Constitution?'],
    ["Pensez-vous que la culture française est supérieure à la plupart des autres cultures ?", 'Do you think French culture is superior to most other cultures?'],
    ["Êtes-vous favorable à la mise en œuvre de politiques nationalistes en France ?", 'Do you support implementing nationalist policies in France?'],
    ["Pensez-vous que l'islamophobie constitue un problème en France ?", 'Do you think Islamophobia is a problem in France?'],
    ["Pensez-vous que la place de l'islam en France pose un problème à la société française ?", 'Do you think the place of Islam in France is a problem for French society?'],
  ]],
  ['eur', 'Union européenne, euro, défense et politique étrangère', 'European Union, euro, defense and foreign policy', [
    ["Êtes-vous favorable au maintien de la France au sein de l'Union européenne ?", 'Do you support France staying in the European Union?'],
    ["Êtes-vous favorable au transfert de compétences supplémentaires de la France vers les institutions de l'Union européenne ?", 'Do you support transferring more powers from France to the institutions of the European Union?'],
    ["Êtes-vous favorable au retour de certaines compétences actuellement exercées par les institutions européennes vers les États membres ?", 'Do you support returning some powers now exercised by the European institutions to the member states?'],
    ["Êtes-vous favorable à une intégration économique et politique plus poussée entre les États membres de l'Union européenne ?", 'Do you support deeper economic and political integration among the member states of the European Union?'],
    ["Êtes-vous favorable à l'extension du vote à la majorité qualifiée au sein de l'Union européenne, notamment en matière de politique étrangère et de sécurité ?", 'Do you support extending qualified-majority voting in the European Union, especially on foreign and security policy?'],
    ["Êtes-vous favorable à une augmentation de la contribution financière de la France aux programmes communs européens ?", 'Do you support France contributing more money to joint European programs?'],
    ["Êtes-vous favorable au renforcement des frontières extérieures de l'Union européenne et à la mise en place d'une politique commune plus stricte en matière d'asile ?", 'Do you support strengthening the European Union’s external borders and a stricter common asylum policy?'],
    ["Êtes-vous favorable à une augmentation des dépenses militaires françaises et au renforcement des capacités de défense du pays ?", 'Do you support higher French military spending and stronger national defense capabilities?'],
    ["Êtes-vous favorable au renforcement des capacités de dissuasion nucléaire de la France ?", 'Do you support strengthening France’s nuclear deterrent?'],
    ["Êtes-vous favorable à un renforcement de la coopération militaire entre la France, l'Allemagne et les autres pays européens alliés ?", 'Do you support closer military cooperation between France, Germany and other allied European countries?'],
    ["Êtes-vous favorable à l'octroi d'une aide financière, humanitaire et militaire à l'Ukraine ?", 'Do you support giving financial, humanitarian and military aid to Ukraine?'],
    ["Êtes-vous favorable à l'octroi d'une aide financière à d'autres pays étrangers, à l'exclusion de l'Ukraine, notamment au Maroc, à la Colombie, au Sénégal ou au Brésil ?", 'Do you support giving financial aid to other foreign countries besides Ukraine, such as Morocco, Colombia, Senegal or Brazil?'],
    ["Êtes-vous favorable au rétablissement d'un service militaire obligatoire pour les hommes de nationalité française ?", 'Do you support bringing back compulsory military service for French men?'],
    ["Êtes-vous favorable à l'abandon de l'euro et au retour au franc comme monnaie nationale française ?", 'Do you support leaving the euro and returning to the franc as France’s currency?'],
    ["Pensez-vous que la France devrait renforcer ses relations diplomatiques et économiques avec la Chine ?", 'Do you think France should strengthen its diplomatic and economic ties with China?'],
    ["Pensez-vous que la France devrait renforcer ses relations diplomatiques et économiques avec la Russie ?", 'Do you think France should strengthen its diplomatic and economic ties with Russia?'],
    ["Pensez-vous que la France devrait renforcer ses relations diplomatiques et économiques avec les États-Unis ?", 'Do you think France should strengthen its diplomatic and economic ties with the United States?'],
    ["Êtes-vous favorable au rattachisme, c'est-à-dire au rattachement de la Wallonie à la France ?", 'Do you support “rattachisme”, that is, Wallonia joining France?'],
    ["Êtes-vous favorable à la reconnaissance officielle de la Palestine en tant qu'État par la France ?", 'Do you support France officially recognizing Palestine as a state?'],
    ["Êtes-vous favorable à ce que la France apporte un soutien à Israël dans ses conflits armés, y compris sous la forme d'une aide militaire ?", 'Do you support France backing Israel in its armed conflicts, including with military aid?'],
    ["Pensez-vous qu'Israël doit continuer d'exister en tant qu'État souverain ?", 'Do you think Israel should continue to exist as a sovereign state?'],
  ]],
  ['ene', 'Énergie, climat et infrastructures', 'Energy, climate and infrastructure', [
    ["Êtes-vous favorable à l'augmentation des capacités de production d'énergie nucléaire en France ?", 'Do you support increasing nuclear power generation capacity in France?'],
    ["Êtes-vous favorable à une augmentation des investissements dans les énergies renouvelables, notamment l'énergie éolienne et solaire ?", 'Do you support more investment in renewable energy, especially wind and solar?'],
    ["Êtes-vous favorable à une sortie plus rapide des énergies fossiles, même si cette transition entraîne temporairement une hausse de certains coûts énergétiques ?", 'Do you support moving off fossil fuels faster, even if the transition temporarily raises some energy costs?'],
    ["Êtes-vous favorable au maintien des aides publiques destinées à réduire les factures d'énergie des ménages ?", 'Do you support keeping public aid that lowers households’ energy bills?'],
    ["Êtes-vous favorable à l'extension du réseau de lignes à grande vitesse (TGV) et à l'amélioration des liaisons ferroviaires régionales ?", 'Do you support extending the high-speed rail (TGV) network and improving regional rail links?'],
    ["Êtes-vous favorable à des restrictions plus strictes sur les émissions polluantes des véhicules dans les zones urbaines ?", 'Do you support stricter limits on polluting vehicle emissions in urban areas?'],
    ["Êtes-vous favorable à une augmentation des aides à l'achat de véhicules électriques et au développement des bornes de recharge ?", 'Do you support more aid for buying electric vehicles and building charging stations?'],
    ["Êtes-vous favorable à une augmentation des investissements dans la prévention des inondations, la lutte contre les sécheresses et la prévention des incendies de forêt ?", 'Do you support more investment in flood prevention, drought response and forest-fire prevention?'],
    ["Êtes-vous favorable au développement des transports publics dans les zones rurales ?", 'Do you support developing public transport in rural areas?'],
    ["Êtes-vous favorable à des réglementations environnementales plus strictes pour réduire la pollution liée à l'agriculture ?", 'Do you support stricter environmental rules to reduce pollution from agriculture?'],
    ["Êtes-vous favorable à l'installation et à l'utilisation de systèmes de climatisation dans les lieux publics, notamment les écoles, les gares et les aéroports ?", 'Do you support installing and using air conditioning in public places, including schools, train stations and airports?'],
    ["Êtes-vous favorable au Pacte vert pour l'Europe (European Green Deal) ?", 'Do you support the European Green Deal?'],
    ["Êtes-vous favorable à la suppression progressive des subventions publiques aux énergies fossiles en France ?", 'Do you support phasing out public subsidies for fossil fuels in France?'],
    ["Êtes-vous favorable à la mise en place d'une taxe carbone visant à réduire les émissions de gaz à effet de serre ?", 'Do you support a carbon tax to reduce greenhouse gas emissions?'],
    ["Êtes-vous favorable à la plantation d'arbres supplémentaires dans les zones urbaines afin de réduire les effets des fortes chaleurs et d'améliorer la qualité de l'air ?", 'Do you support planting more trees in urban areas to reduce the effects of heat waves and improve air quality?'],
  ]],
  ['edu', 'Éducation et enseignement supérieur', 'Education and higher education', [
    ["Êtes-vous favorable à une augmentation des salaires et des financements destinés aux enseignants des établissements publics ?", 'Do you support higher pay and more funding for teachers in public schools?'],
    ["Êtes-vous favorable au développement de l'enseignement professionnel et des formations en apprentissage ?", 'Do you support expanding vocational education and apprenticeship training?'],
    ["Êtes-vous favorable à ce que les établissements scolaires publics disposent de davantage de liberté dans le choix de leurs méthodes pédagogiques et de leurs programmes ?", 'Do you support giving public schools more freedom to choose their teaching methods and curricula?'],
    ["Êtes-vous favorable à la suppression du plafonnement du nombre d'étudiants admis en études de médecine en France ?", 'Do you support removing the cap on the number of students admitted to medical school in France?'],
    ["Êtes-vous favorable à l'augmentation des financements publics destinés à réduire le nombre d'élèves par classe ?", 'Do you support more public funding to reduce class sizes?'],
    ["Êtes-vous favorable à l'installation de systèmes de climatisation dans les salles de classe des établissements scolaires ?", 'Do you support installing air conditioning in school classrooms?'],
    ["Êtes-vous favorable à la gratuité des études universitaires pour les étudiants français ?", 'Do you support tuition-free university for French students?'],
    ["Êtes-vous favorable à l'augmentation des aides financières destinées aux étudiants étrangers dans les universités françaises ?", 'Do you support more financial aid for international students at French universities?'],
    ["Êtes-vous favorable à une augmentation des frais d'inscription universitaires pour les étudiants étrangers originaires de pays hors de l'Union européenne ?", 'Do you support higher university fees for international students from outside the European Union?'],
    ["Êtes-vous favorable à une réduction du temps que les enfants passent chaque jour à l'école en France ?", 'Do you support shortening the time children spend at school each day in France?'],
    ["Êtes-vous favorable à une réforme du système Parcoursup d'accès à l'enseignement supérieur ?", 'Do you support reforming Parcoursup, the admission system for higher education?'],
    ["Êtes-vous favorable à l'introduction de l'uniforme dans les établissements scolaires publics ?", 'Do you support introducing uniforms in public schools?'],
    ["Êtes-vous favorable à une réduction des financements publics accordés aux établissements scolaires privés sous contrat ?", 'Do you support less public funding for private schools under contract with the State?'],
    ["Êtes-vous favorable à l'interdiction de l'accès aux réseaux sociaux pour les enfants de moins de 15 ans ?", 'Do you support banning social media for children under 15?'],
  ]],
  ['sec', "Sécurité, justice et maintien de l'ordre", 'Security, justice and policing', [
    ["Êtes-vous favorable à une augmentation des financements et des effectifs de la police nationale ?", 'Do you support more funding and more officers for the national police?'],
    ["Êtes-vous favorable à une extension de l'utilisation des caméras de vidéosurveillance dans les espaces publics ?", 'Do you support wider use of video surveillance cameras in public spaces?'],
    ["Êtes-vous favorable à des peines de prison plus longues pour les personnes reconnues coupables de crimes violents graves ?", 'Do you support longer prison sentences for people convicted of serious violent crimes?'],
    ["Êtes-vous favorable à l'instauration de peines minimales obligatoires pour les personnes en situation de récidive ?", 'Do you support mandatory minimum sentences for repeat offenders?'],
    ["Êtes-vous favorable à ce que les mineurs de moins de 18 ans ayant commis des actes violents ou des infractions répétées soient jugés et sanctionnés comme des adultes ?", 'Do you support trying and sentencing minors under 18 who commit violent acts or repeated offenses as adults?'],
    ["Êtes-vous favorable au rétablissement de la peine de mort en France ?", 'Do you support bringing back the death penalty in France?'],
    ["Êtes-vous favorable au maintien de l'interdiction du cannabis en France ?", 'Do you support keeping cannabis illegal in France?'],
    ["Êtes-vous favorable au maintien de l'interdiction des drogues dites dures en France ?", 'Do you support keeping so-called hard drugs illegal in France?'],
    ["Êtes-vous favorable au développement des programmes de réinsertion et de réhabilitation des personnes détenues ?", 'Do you support expanding reintegration and rehabilitation programs for prisoners?'],
    ["Êtes-vous favorable à la mise en place d'un dispositif permettant aux habitants d'être informés publiquement de la présence, dans leur quartier, de personnes condamnées pour des infractions sexuelles ?", 'Do you support a system that publicly informs residents when people convicted of sexual offenses live in their neighborhood?'],
    ["Pensez-vous que la police devrait être autorisée à recourir à la force lorsque des policiers sont attaqués lors d'une manifestation ?", 'Do you think police should be allowed to use force when officers are attacked during a demonstration?'],
    ["Pensez-vous que la police devrait pouvoir utiliser tous les moyens qu'elle juge nécessaires pour rétablir l'ordre lors d'émeutes ?", 'Do you think police should be able to use any means they deem necessary to restore order during riots?'],
    ["Pensez-vous que la police ne devrait pas intervenir lors des manifestations, même lorsque des troubles à l'ordre public se produisent ?", 'Do you think police should not intervene during demonstrations, even when public disorder occurs?'],
  ]],
  ['loc', 'Collectivités territoriales et gouvernement local', 'Local authorities and local government', [
    ["Êtes-vous favorable à une augmentation des impôts locaux dans votre département, votre intercommunalité ou votre région afin de financer des infrastructures telles que les transports publics, les équipements sportifs et les stades ?", 'Do you support higher local taxes in your department, intercommunality or region to fund infrastructure such as public transport, sports facilities and stadiums?'],
    ["Êtes-vous favorable à une augmentation des impôts locaux sur votre territoire afin de financer les collèges et les lycées, ainsi que de soutenir les universités ?", 'Do you support higher local taxes in your area to fund middle and high schools and support universities?'],
    ["Êtes-vous favorable à ce que les régions disposent de davantage de compétences en matière de transports, d'éducation et de développement économique ?", 'Do you support giving regions more powers over transport, education and economic development?'],
    ["Êtes-vous favorable à ce que les communes puissent conserver une plus grande part des recettes fiscales locales afin de financer leurs services publics ?", 'Do you support letting communes keep a larger share of local tax revenue to fund their public services?'],
    ["Êtes-vous favorable à la gratuité des transports en commun dans la ville où vous habitez ?", 'Do you support free public transport in the city where you live?'],
    ["Pour votre ville, êtes-vous favorable à un renforcement de la réglementation des locations touristiques de courte durée proposées sur des plateformes comme Airbnb ?", 'For your city, do you support tighter rules on short-term tourist rentals offered on platforms like Airbnb?'],
    ["Êtes-vous favorable à une réduction de la dépendance à la voiture dans votre ville, grâce au développement des transports en commun et à la réduction du nombre de voies réservées aux voitures ?", 'Do you support reducing car dependence in your city by developing public transport and reducing the number of car lanes?'],
    ["Êtes-vous favorable à la mise en place de budgets participatifs permettant aux habitants de décider directement de l'affectation d'une partie du budget de leur commune ?", 'Do you support participatory budgets that let residents directly decide how part of their commune’s budget is spent?'],
    ["Êtes-vous favorable à un recours plus fréquent aux référendums locaux pour consulter les habitants sur les grandes décisions municipales ?", 'Do you support more frequent local referendums to consult residents on major municipal decisions?'],
    ["Êtes-vous favorable à une augmentation des investissements locaux dans le logement social et les logements financièrement accessibles ?", 'Do you support more local investment in social housing and affordable housing?'],
    ["Êtes-vous favorable à des règles d'urbanisme plus strictes afin de protéger les espaces verts et de limiter l'étalement urbain ?", 'Do you support stricter planning rules to protect green spaces and limit urban sprawl?'],
    ["Êtes-vous favorable au développement des pistes cyclables et des zones piétonnes, même si cela entraîne une réduction des places de stationnement ou des voies automobiles ?", 'Do you support developing cycle lanes and pedestrian zones, even if it means fewer parking spaces or car lanes?'],
    ["Êtes-vous favorable à un renforcement des moyens et des compétences de la police municipale dans votre ville ?", 'Do you support giving your city’s municipal police more resources and powers?'],
    ["Êtes-vous favorable à une augmentation des financements locaux destinés aux bibliothèques, aux équipements culturels et aux infrastructures sportives ?", 'Do you support more local funding for libraries, cultural facilities and sports facilities?'],
    ["Êtes-vous favorable à une augmentation des investissements locaux dans le tri des déchets, le recyclage et les services de protection de l'environnement ?", 'Do you support more local investment in waste sorting, recycling and environmental protection services?'],
  ]],
];

let n = 0;
export const FR_CATEGORIES = SECTIONS.map(([id, fr, en, items], k) => ({
  id, n: k + 1, fr, en,
  questions: items.map(([qfr, qen]) => {
    n++;
    return { id: `q${String(n).padStart(3, '0')}`, n, cat: id, fr: qfr, en: qen, kind: /^Pensez-vous/.test(qfr) ? 'agree' : 'favor' };
  }),
}));
export const FR_QUESTIONS = FR_CATEGORIES.flatMap((c) => c.questions);
export const FR_QUESTION_BY_ID = Object.fromEntries(FR_QUESTIONS.map((q) => [q.id, q]));
export const FR_CATEGORY_BY_ID = Object.fromEntries(FR_CATEGORIES.map((c) => [c.id, c]));

export const qText = (q) => L(q.fr, q.en);
export const catTitle = (c) => L(c.fr, c.en);

// Answer scales, +2 to -2.
export const scaleFor = (q) => (q.kind === 'agree'
  ? [[2, 'Tout à fait d’accord', 'Strongly agree'], [1, 'Plutôt d’accord', 'Agree'], [0, 'Neutre', 'Neutral'], [-1, 'Plutôt pas d’accord', 'Disagree'], [-2, 'Pas du tout d’accord', 'Strongly disagree']]
  : [[2, 'Très favorable', 'Strongly in favor'], [1, 'Plutôt favorable', 'In favor'], [0, 'Neutre', 'Neutral'], [-1, 'Plutôt défavorable', 'Against'], [-2, 'Très défavorable', 'Strongly against']])
  .map(([value, fr, en]) => ({ value, label: L(fr, en) }));
export const answerLabel = (q, v) => scaleFor(q).find((s) => s.value === v)?.label;
