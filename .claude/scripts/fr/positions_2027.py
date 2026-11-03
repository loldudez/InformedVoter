"""Write data/fr/positions.json: where the 2027 presidential candidates stand on the
France section's 144 questions, each position with its source and a verbatim quote.

Rules (as for the U.S. research): a position needs the candidate's own words, from
their program, campaign site or a statement, and is never inferred. Each quote is
copied from the source (≤ 25 words) and checked against the source text before it
is added (scratch tools, see DATA.md). Stances run from +2 (très favorable / tout à
fait d'accord) to -2. A question with no source stays undocumented, and matching
leaves it out.

Sources were found with the help of programmes-2027.fr and votons-2027.fr, independent
directories of the programs, but every quote here comes from the candidate's own
document (or their party's, labelled as such).

    py scripts/fr/positions_2027.py
"""

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "fr" / "positions.json"
PRES = ROOT / "data" / "fr" / "presidentielle-2027.json"
READ = "2026-10-28"
# The candidates whose sources were read on November 2 rather than October 28.
READ_LATER = "2026-11-02"
LATER = {"raphael-glucksmann", "david-lisnard", "marine-tondelier", "francois-ruffin", "fabien-roussel",
         "nicolas-dupont-aignan", "nathalie-arthaud", "xavier-bertrand", "dominique-de-villepin", "florian-philippot",
         "francois-asselineau", "anasse-kazib", "selma-labib", "bernard-cazeneuve", "antoine-mikolajczak",
         "karim-bouamrane", "delphine-batho", "jordan-bardella", "juan-branco", "jean-francois-legendre",
         "clara-egger", "mira-markovic", "olivier-becht", "natacha-polony"}


def src(title, url, date=None):
    return {"title": title, "url": url, "date": date, "accessed": READ}


def later(source):
    """A source read on November 2 for a candidate whose other sources were read earlier."""
    return {**source, "accessed": READ_LATER}


# Jean-Luc Mélenchon (La France insoumise) ---------------------------------------
# His campaign site presents L'Avenir en commun (2025 edition) as his program, while a
# new edition is prepared; its chapter pages no longer load, so the program is cited
# from the Wayback Machine's copy of the PDF, page by page.
AEC = "https://web.archive.org/web/20250603222117/https://programme.lafranceinsoumise.fr/wp-content/uploads/2025/02/A5-PROGRAMME-SITE.pdf"
CNAP = "https://melenchon2027.fr/wp-content/uploads/2026/10/Comment-nous-allons-remettre-de-l-ordre-dans-les-comptes-publics.pdf"
BTP = "https://melenchon2027.fr/wp-content/uploads/2026/09/M-27-PLAN-BTP-LOGEMENT.pdf"


def aec(p):
    return src(f"L’Avenir en commun, programme de La France insoumise (2025), p. {p}", f"{AEC}#page={p}", "2025-02")


def cnap(p):
    return src(f"« Comment nous allons remettre de l’ordre dans les comptes publics », melenchon2027.fr, p. {p}", f"{CNAP}#page={p}", "2026-10")


def btp(p):
    return src(f"Plan d’investissement BTP et logement, melenchon2027.fr, p. {p}", f"{BTP}#page={p}", "2026-09")


def aec2(p):
    return later(aec(p))


LFI_ISLAMOPHOBIE = "Mettre en place un plan interministériel pour analyser, prévenir et lutter contre l’islamophobie et l’antisémitisme en France"
LFI_FOSSILES = "Sortir des énergies carbonées : arrêter les subventions aux énergies fossiles, y compris à l’étranger"
LFI_CLIM = "installerons en cas de besoin des dispositifs de climatisation moins énergivores"  # schools, EHPAD, hospitals
LFI_FRAIS = "Abroger l’augmentation des frais d’inscription décidée par Macron pour les étudiants étrangers"
MELENCHON = [
    ("q001", -2, aec(10), "La Ve République a fait son temps."),
    ("q002", 2, aec(11), "Abolir la monarchie présidentielle"),
    ("q003", 2, aec(11), "Abolir les procédures de « votes forcés » du Parlement comme l’article 49.3 de la Constitution de la Ve République"),
    ("q004", 2, aec(11), "Élire l’Assemblée nationale au scrutin proportionnel"),
    ("q005", 2, aec(12), "Donner le droit de vote à 16 ans"),
    ("q006", 2, aec(12), "mettre en place le vote obligatoire"),
    ("q007", 2, aec(12), "Instaurer le Référendum d’initiative citoyenne (RIC), par lequel les citoyens qui réunissent suffisamment de signatures peuvent révoquer des élus, proposer ou abroger une loi"),
    ("q008", 2, aec2(13), "Rendre effectif le principe du non-cumul des mandats et des indemnités, y compris dans le temps"),
    ("q010", 2, aec(12), "Durcir les règles contre les conflits d’intérêts et interdire le pantouflage"),
    ("q013", 2, aec(26), "en appliquant le principe de progressivité : plus on gagne d’argent, plus on contribue au bien public"),
    ("q014", 2, aec(26), "Rétablir et renforcer l’impôt de solidarité sur la fortune (ISF), incluant un volet climatique visant à taxer les gros pollueurs"),
    ("q017", 2, cnap(9), "Ces mesures d’urgence sociale doivent être complétées par une hausse du SMIC à 1 700 euros net."),
    ("q019", 1, aec(33), "passer aux 32 heures dans les métiers pénibles ou de nuit, et favoriser leur généralisation par la négociation collective"),
    ("q020", -2, aec(16), "Accorder aux comités d’entreprise un droit de veto suspensif sur les plans de licenciements"),
    ("q025", 2, aec2(12), "Supprimer le monopole du déclenchement de poursuites judiciaires par la seule administration fiscale pour toutes les affaires en cas de fraude"),
    ("q027", 2, aec(48), "Renationaliser la SNCF et refuser la mise en concurrence des lignes de transport"),
    ("q028", -2, aec(37), "Abroger la réforme d’Emmanuel Macron passant l’âge de départ à la retraite à 64 ans"),
    ("q029", 2, aec(33), "Rétablir la retraite à 60 ans après quarante années de cotisation"),
    ("q032", 2, aec(55), "instaurer le « 100 % Sécu » en remboursant à 100 % les soins de santé prescrits"),
    ("q033", 2, cnap(10), "Nous proposons une hausse globale de 3 milliards d’euros du budget des hôpitaux avec au moins 10 000 créations de postes de personnel soignant."),
    ("q035", -2, aec(35), "Abroger la loi France Travail et l’obligation de réaliser 15h d’activités hebdomadaires contre le revenu de remplacement"),
    ("q036", 2, aec(20), "Créer un service public de la petite enfance et ouvrir 500 000 places en crèche et modes de garde adaptés sur cinq ans"),
    ("q039", 2, aec(30), "Interdire les expulsions locatives sans relogement public"),
    ("q042", 2, aec2(62), "Assumer notre devoir d’humanité envers les réfugiés"),
    ("q046", 2, aec(62), "régulariser les travailleurs, étudiants, parents d’enfants scolarisés"),
    ("q054", 2, aec(17), "Ajouter le droit de mourir dans la dignité (y compris avec assistance) et l’accès garanti à des soins palliatifs dans la Constitution"),
    ("q055", 2, aec2(13), "nous en tenir aux principes très clairs énoncés par la loi de 1905 de séparation des Églises et de l’État"),
    ("q059", 2, aec2(40), LFI_ISLAMOPHOBIE),
    ("q060", 2, btp(14), "Nous nous donnerons l’objectif de doubler le nombre annuel de monuments dont l’état s’améliore, en multipliant par deux le budget public dédié."),
    ("q061", 2, aec2(17), "Mettre en oeuvre un plan d’éradication des violences à l’encontre des personnes LGBTI"),
    ("q062", 2, aec2(40), "Garantir l’égal accès et l’effectivité du droit à l’IVG et le choix de la méthode d’IVG"),
    ("q065", 2, aec2(40), LFI_ISLAMOPHOBIE),
    ("q072", -1, aec2(65), "Conditionner la contribution française au budget de l’Union européenne"),
    ("q073", -2, aec2(62), "Sortir de l’impasse de la politique de Schengen et Frontex"),
    ("q075", -1, aec2(60), "participer comme observateur au traité d’interdiction des armes nucléaires (TIAN)"),
    ("q076", -2, aec(65), "Suspendre la participation (opt-out) de la France à certains programmes comme l’Europe de la défense"),
    ("q078", 2, aec(63), "Consacrer 0,7 % du revenu national brut à une aide publique au développement"),
    ("q085", 2, aec(61), "Reconnaître l’État de Palestine"),
    ("q086", -2, aec(61), "interrompre les accords de coopération économique avec Israël et décréter un embargo sur les armes"),
    ("q088", -2, aec(49), "Sortir du nucléaire : abandonner les projets d’EPR"),
    ("q089", 2, aec(49), "Pour réduire les émissions de gaz à effet de serre (GES), nous devons atteindre le 100 % d’énergies renouvelables."),
    ("q090", 2, aec2(49), LFI_FOSSILES),
    ("q093", -1, aec2(48), "Décréter un moratoire sur les zones à faibles émissions (ZFE) dans leur conception actuelle"),
    ("q095", 2, cnap(11), "Il faut d’urgence financer les moyens pour s’adapter aux prochaines canicules, incendies, sécheresses"),
    ("q097", 2, aec(51), "Planifier la réduction progressive des doses d’engrais et de pesticides, interdire immédiatement les plus dangereux (glyphosate, néonicotinoïdes)"),
    ("q098", 1, later(btp(12)), LFI_CLIM),
    ("q100", 2, aec2(49), LFI_FOSSILES),
    ("q102", 1, aec2(47), "Mettre en place des défenseurs de la nature chargés de l’eau, l’air, la forêt, la végétalisation et la perméabilité des sols au niveau communal"),
    ("q105", 1, aec2(21), "réaffirmant la liberté pédagogique, notamment dans le primaire"),
    ("q107", 2, cnap(9), "Notre objectif, en un mandat, serait de nous rapprocher de la moyenne européenne (dans le primaire et le secondaire) de 19 élèves par classe"),
    ("q108", 1, later(btp(12)), LFI_CLIM),
    ("q110", 1, aec2(23), LFI_FRAIS),
    ("q111", -2, aec2(23), LFI_FRAIS),
    ("q113", 2, aec(23), "Garantir à tous les bacheliers l’accès sans sélection à la formation de leur choix en démantelant le système Parcoursup"),
    ("q114", -2, aec2(21), "Suspendre l’expérimentation de l’uniforme"),
    ("q115", 1, aec(21), "Appliquer un malus au financement public des établissements privés sous contrat"),
    ("q118", -1, aec2(32), "Interdire dans la loi tout usage des technologies de reconnaissance faciale dans les espaces et établissements publics"),
    ("q123", -2, aec(56), "Légaliser et encadrer par un monopole d’État la consommation, la production et la vente de cannabis à des fins récréatives"),
    ("q125", 2, aec2(31), "assurer aux personnes détenues les moyens de se réinsérer dans notre société"),
    ("q128", -2, aec(18), "Interdire les tasers, les grenades de désencerclement, les « lanceurs de balles de défense 40 » (Flash-Ball)"),
    ("q135", 2, aec(30), "en limitant les locations de courte durée (de type AirBnB) à 60 jours par an"),
    ("q139", 2, aec(30), "Construire 200 000 logements publics par an pendant cinq ans aux normes écologiques les plus ambitieuses"),
    ("q140", 2, aec2(47), "Stopper l’étalement urbain : rapprocher les bassins de vie et les bassins d’emploi"),
]

# Marine Le Pen (Rassemblement national) ---------------------------------------
# Her own project booklet and interviews, and the RN's programs and counter-budgets she
# campaigns on (labelled as party documents). A news summary of a proposal is cited
# without a quote.
RN24 = "https://rassemblementnational.fr/documents/202406-programme.pdf"
RNEU = "https://rassemblementnational.fr/documents/202411-programme-europeennes.pdf"
LIVRET = "https://rassemblementnational.fr/documents/WEB-GRN-LIVRET-ENTREPRISE.pdf"


def rn24(p):
    return src(f"Programme du Rassemblement national, législatives 2024, p. {p}", f"{RN24}#page={p}", "2024-06-25")


def rneu(p):
    return src(f"Programme du Rassemblement national, européennes 2024, p. {p}", f"{RNEU}#page={p}", "2024-05-06")


def livret(p):
    return src(f"« La France entreprend », projet de Marine Le Pen (livret du RN), p. {p}", f"{LIVRET}#page={p}", "2024-09-06")


def grn26(p):
    return src(f"Contre-budget 2026 du groupe RN à l’Assemblée nationale, p. {p}", f"https://rassemblementnational.fr/documents/GRN-CONTRE-BUDGET-2026.pdf#page={p}", "2025-10-23")


def clim(p):
    return src(f"Plan Clim’, groupe RN à l’Assemblée nationale, p. {p}", f"https://back.deputes-rn.fr/wp-content/uploads/2026/07/GRN-DOSSIER-PLAN-CLIM.pdf#page={p}", "2026-07-01")


LP_RETRAITES = src("Europe 1 : Retraites, Marine Le Pen pour une part de capitalisation « volontaire » (France 3)", "https://www.europe1.fr/economie/retraites-marine-le-pen-pour-une-part-de-capitalisation-volontaire-953651", "2026-06-14")
LP_BUDGET = src("Europe 1 : ce qu’il faut retenir du contre-budget 2027 présenté par Marine Le Pen", "https://www.europe1.fr/politique/budget-2027-marine-le-pen-promet-140-milliards-deuros-nets-deconomies-dici-2032-pour-eviter-a-la-france-le-defaut-de-paiement-1126400", "2026-10-06")
LE_PEN = [
    ("q007", 2, later(rn24(8)), "Instaurer dans la Constitution un RIC législatif"),
    ("q011", 1, LP_BUDGET, None),  # a "règle d'or budgétaire" by referendum, to cut the debt every year (news summary)
    ("q012", 2, src("Communiqué du RN signé par Jordan Bardella et Marine Le Pen : freins à la croissance et simplification", "https://rassemblementnational.fr/communiques/freins-a-la-croissance-et-simplification-jordan-bardella-et-marine-le-pen-associent-le-monde-economique", "2026-04-20"),
     "notre objectif est d’élaborer un grand projet d’ordonnance de simplification, qui sera publié, dès le début du mandat"),
    ("q014", 1, grn26(3), "Impôt sur la fortune financière."),
    ("q015", 2, later(livret(10)), "Sa suppression bénéficiera prioritairement aux indépendants, TPE et PME"),  # the CFE
    # Production taxes rather than the corporate income tax, so only "plutôt".
    ("q016", 1, later(grn26(4)), "Baisse impôts de production (CFE, C3S, CVAE)."),
    ("q022", 2, LP_BUDGET, "140 milliards d'euros nets d'économie"),
    ("q025", 2, livret(26), "Cette administration sera dédiée à la lutte contre toutes les formes de fraude, qu’elles soient fiscales, sociales"),
    ("q028", -2, LP_RETRAITES, "progressivement, en fonction de l'âge d'entrée sur le marché du travail, on arrive jusqu'à 42 ans et 62 ans"),
    ("q029", 2, LP_RETRAITES, "ceux qui sont entrés avant 20 ans sur le marché du travail peuvent partir avec 40 annuités à 60 ans"),
    ("q030", 2, later(livret(23)), "prendre en compte la pénibilité réelle des emplois faiblement qualifiés"),
    ("q031", 1, LP_BUDGET, "je proposerai bientôt la création d'un véritable pilier de capitalisation"),
    ("q035", 1, src("Contre-budget 2027 du groupe RN à l’Assemblée nationale, p. 11", "https://back.deputes-rn.fr/wp-content/uploads/2026/10/GRN-CONTRE-BUDGET-2027-DOSSIER.pdf#page=11", "2026-10-15"),
     "Devoir pointer à France Travail une fois par mois pour pouvoir toucher le chômage"),
    ("q040", 2, rn24(6), "Préserver le peuple français de la submersion migratoire"),
    ("q042", -2, later(rneu(5)), "Organiser le traitement des demandes d’asile dans les ambassades et consulats des pays d’origine pour éviter une immigration du fait accompli."),
    ("q046", -2, later(livret(22)), "L’emploi de travailleurs clandestins fera l’objet de poursuites pénales systématiques, et aucune régularisation de complaisance ne sera plus décidée"),
    ("q048", 1, rn24(6), "Ouvrir des négociations avec nos partenaires européens pour réserver la libre-circulation Schengen aux seuls ressortissants européens"),
    ("q050", 2, later(rneu(5)), "Expulser les clandestins, islamistes et délinquants étrangers."),
    ("q058", 2, src("L’Avenir (Belga, AFP) : en cas de victoire, Marine Le Pen veut interdire le voile « de manière progressive » (LCI)", "https://www.lavenir.net/actu/monde/2026/09/17/france-en-cas-de-victoire-marine-le-pen-veut-interdire-le-voile-de-maniere-progressive-4BGF3FXFXZBX7OL5YSN42XFUXM/", "2026-09-16"),
     "L'objectif sera d'interdire le voile et nous le ferons si les Français nous en donnent mandat"),
    ("q068", -2, rneu(2), "la Commission de Bruxelles exploite les crises pour s’arroger des compétences supplémentaires au détriment de la souveraineté des États"),
    ("q070", -2, rneu(4), "qui prône une véritable dissolution des nations dans un État européen centralisé"),
    ("q071", -2, later(rneu(7)), "Garantir le droit de veto des États (règle de l’unanimité) et l’élargir à la compétence du commerce."),
    ("q072", -2, rneu(7), "Baisser la contribution française nette (surplus) versée à l’UE"),
    ("q073", 1, later(rneu(5)), "mettre en place une frontière aux portes de l’Europe en permettant à Frontex de renvoyer les migrants illégaux"),
    ("q074", 1, rn24(6), "Sanctuariser la trajectoire budgétaire de la Loi de Programmation Militaire"),
    # Listed among the "politiques contraires à nos intérêts" the RN would refuse: a
    # European defence, not cooperation between national armies, so only "plutôt".
    ("q076", -1, later(rneu(3)), "Une diplomatie et une défense européennes, dont la dépossession de notre dissuasion nucléaire."),
    ("q077", -1, src("CNews : guerre en Ukraine, « la dissuasion nucléaire n’appartient qu’à la France », juge Marine Le Pen", "https://www.cnews.fr/france/2026-09-24/guerre-en-ukraine-la-dissuasion-nucleaire-nappartient-qua-la-france-juge-marine", "2026-09-24"),
     "plus aider financièrement l’Ukraine"),
    ("q078", -2, later(grn26(3)), "Baisse de l’Aide Publique au Développement."),
    ("q088", 2, rn24(8), "Lancer le plan Marie Curie de relance du nucléaire"),
    ("q089", -2, livret(10), "Le développement de l’énergie éolienne sera abandonné."),
    ("q091", 1, rneu(7), "la baisse de la TVA de 20 à 5,5% sur les énergies"),
    ("q093", -2, rn24(7), "Supprimer les Zones à Faibles Emissions"),
    ("q098", 2, clim(5), "Le plan Clim’, qui s'inscrit dans le cadre du plan 100 % Rénov, s'articule autour de deux axes : le premier autour des bâtiments publics"),
    ("q099", -2, later(rneu(4)), "Le Rassemblement National s’oppose au Pacte des migrations qui organise la submersion du continent, ainsi qu’au Pacte vert qui instaure l’écologie punitive"),
    ("q102", 1, later(clim(4)), "isolation thermique des bâtiments, végétalisation urbaine, préservation et adaptation de nos forêts"),
    ("q104", 2, later(livret(12)), "la dévalorisation des filières professionnelles auxquelles il est urgent, par des moyens adaptés, de redonner leurs lettres de noblesse"),
    ("q108", 2, later(clim(5)), "s'adresse en priorité aux publics les plus vulnérables (crèches, écoles, collèges, lycées, hôpitaux et EHPAD)"),
    ("q113", 1, src("CNews : ce qu’il faut retenir d’« Objectif Élysée 2027 » avec Marine Le Pen", "https://www.cnews.fr/france/2026-10-16/blocus-des-lycees-presidentielle-2027-jordan-bardella-ce-quil-faut-retenir", "2026-10-15"),
     "Suppression ou réforme de Parcoursup, ça revient au même"),
    ("q120", 2, rn24(4), "Mise en place des peines planchers pour les récidivistes"),
    ("q140", -2, src("Lettre ouverte de Marine Le Pen aux professionnels de l’immobilier", "https://rassemblementnational.fr/lettre-ouverte/lettre-ouverte-de-marine-le-pen-aux-professionnels-de-limmobilier", "2026-09-21"),
     "Nous supprimerons le ZAN et rendrons aux communes, en particulier aux communes rurales, la maîtrise de leur foncier."),
    ("q142", 2, rn24(6), "Rendre obligatoire la création d’une police municipale pour les communes de plus de 10 000 habitants"),
]

# Éric Zemmour (Reconquête) --------------------------------------------------------
# Reconquête's tracts and petitions on ericzemmour.fr, and his interviews and speeches
# as the press reported them. His 2027 program isn't published yet.
ZT = "https://assets.ericzemmour.fr/ressources/tracts/"


def ztract(name, title, date, p=2):
    return src(f"Reconquête, tract « {title} », p. {p}", f"{ZT}{name}.pdf#page={p}", date)


Z_POUVOIR = ztract("verite-pouvoir-achat", "Dépenser moins, pour taxer moins, pour gagner plus !", "2025-11-13")
Z_CNEWS = src("CNews : ce qu’il faut retenir de l’interview d’Éric Zemmour sur CNEWS", "https://www.cnews.fr/france/2026-05-19/immigration-negative-erreur-de-la-binationalite-rassemblement-national-ce-quil", "2026-05-19")
Z_MINEURS = src("Le JDD : émeutes lycéennes, « Il faut en finir avec l’excuse de minorité », martèle Éric Zemmour", "https://www.lejdd.fr/politique/emeutes-lyceennes-il-faut-en-finir-avec-lexcuse-de-minorite-martele-eric-zemmour-185988", "2026-10-13")
Z_AVENIR = ztract("avenir-est-a-nous", "L’avenir est à nous", "2026-10-06")
Z_SANTE = ztract("sante", "Urgence nationale : notre système de santé", "2025-06-03")
# His post on X of September 1, 2026, quoted in full by the JDD.
Z_VOILE = src("Le JDD : interdiction du voile dans l’espace public, Éric Zemmour abonde dans le sens du RN", "https://www.lejdd.fr/politique/interdiction-du-voile-dans-lespace-public-eric-zemmour-abonde-dans-le-sens-du-rn-182307", "2026-09-01")
ZEMMOUR = [
    ("q012", 1, Z_POUVOIR, "Supprimer les ARS, l’Ademe, l’ANAH, le CESE, l’Arcom et France Travail"),
    ("q018", 1, Z_AVENIR, "supprimer la CSG sur les revenus du travail"),
    ("q029", -2, Z_CNEWS, None),  # defended raising the retirement age (news summary)
    ("q031", 1, Z_CNEWS, "insufflant dans le système de répartition, une part de capitalisation"),
    ("q033", 2, Z_SANTE, "SAUVER L’HÔPITAL PUBLIC en recrutant 40 000 nouveaux personnels hospitaliers"),
    ("q040", 2, Z_CNEWS, "Les 500.000 immigrés légaux qui viennent chaque année en France fracturent la société"),
    ("q041", -2, src("CNews : « Des robots à la place des immigrés », la proposition choc d’Éric Zemmour pour réduire l’immigration", "https://www.cnews.fr/france/2026-09-18/des-robots-la-place-des-immigres-la-proposition-choc-deric-zemmour-pour-reduire", "2026-09-18"),
     "Des robots à la place des immigrés"),
    ("q042", -2, later(Z_CNEWS), None),  # an end to legal immigration, the right of asylum included (news summary)
    ("q048", 2, later(Z_AVENIR), "Arrêter l’immigration pour que la France retrouve la maîtrise de ses frontières, sa sécurité et sa souveraineté."),
    # He called dual nationality a mistake but, CNews notes, did not call for banning it.
    ("q049", -1, Z_CNEWS, "Nous avons fait une erreur en acceptant la binationalité"),
    ("q050", 2, src("Public Sénat : Éric Zemmour officialise sa candidature à la présidentielle 2027", "https://www.publicsenat.fr/actualites/politique/eric-zemmour-officialise-sa-candidature-a-la-presidentielle-2027", "2026-09-18"),
     None),  # expel foreign prisoners and offenders serving sentences outside prison (news summary)
    ("q052", -2, later(Z_CNEWS), None),  # an end to legal immigration, the right of asylum included (news summary)
    ("q053", 2, later(Z_VOILE), "Je suis totalement d’accord avec la volonté de Marine Le Pen d’interdire le voile dans l’espace public."),
    ("q058", 2, Z_VOILE, "Je suis totalement d’accord avec la volonté de Marine Le Pen d’interdire le voile dans l’espace public."),
    ("q066", 2, later(Z_VOILE), "le voile n’est pas l’arme de prétendus militants islamistes, mais la preuve d’une islamisation profonde et galopante de nos rues et de notre pays"),
    ("q078", -2, Z_POUVOIR, "Supprimer l’aide publique au développement"),
    ("q088", 2, src("Europe 1 : Éric Zemmour appelle à un « vote du sursaut » lors de son discours de rentrée", "https://www.europe1.fr/politique/presidentielle-2027-eric-zemmour-appelle-a-un-vote-du-sursaut-lors-de-son-discours-de-rentree-1075178", "2026-09-13"),
     None),  # six EPR reactors by 2035 and fourteen by 2045 (news summary)
    ("q089", -2, Z_POUVOIR, "Supprimer tous les soutiens publics aux énergies renouvelables"),
    ("q097", -1, ztract("mercosur", "Non à l’accord Mercosur, soutien à nos agriculteurs !", "2025-02-17"), "La fin de la surtransposition des normes européennes qui pénalise uniquement nos agriculteurs"),
    ("q101", -2, src("Reconquête, pétition contre le SEQE 2 (stop-hausse-carburant.fr)", "https://www.stop-hausse-carburant.fr/"), "NON à la nouvelle taxe sur les carburants"),
    ("q104", 2, src("CNews : niveau scolaire français, que propose Éric Zemmour ?", "https://www.cnews.fr/france/2026-10-13/niveau-scolaire-francais-que-propose-eric-zemmour-pour-retablir-la-meilleure", "2026-10-13"),
     "On manque de CAP, donc à partir de la quatrième, il faudra pousser les enfants qui sont beaucoup plus doués pour ça"),
    # Condemns the numerus clausus ("une erreur criminelle") without stating the remedy.
    ("q106", 1, later(Z_SANTE), "Pendant des décennies, l’État a volontairement bridé la formation de médecins avec le numerus clausus."),
    ("q120", 2, Z_MINEURS, None),  # bring back the peines planchers abolished in 2014 (news summary)
    ("q121", 2, Z_MINEURS, "Il faut en finir avec l’excuse de minorité"),
]

# Édouard Philippe (Horizons) -------------------------------------------------------
# The four "priorités" pages of his campaign site are his program; speeches on his and
# Horizons' sites and press reports of interviews fill in the rest.
EP = "https://www.edouardphilippe.fr/priorites/pour-une-france-plus-"


def ep(page, title):
    return src(f"« {title} », priorités d’Édouard Philippe (edouardphilippe.fr)", EP + page)


EP_PROSPERE = ep("prospere", "Pour une France plus prospère")
EP_CONQUERANTE = ep("conquerante", "Pour une France plus conquérante")
EP_ENFANTS = ep("attentive-a-ses-enfants", "Pour une France plus attentive à ses enfants")
EP_SURE = ep("sure", "Pour une France plus sûre")
EP_ANNONCES = src("Trois principales annonces d’Édouard Philippe à « L’Heure de vérité » (edouardphilippe.fr)", "https://www.edouardphilippe.fr/actualites/trois-principales-annonces-dedouard-philippe-a-lheure-de-verite", "2026-10-08")
EP_REIMS = later(src("Discours d’Édouard Philippe au conseil national d’Horizons à Reims (horizonsleparti.fr)", "https://horizonsleparti.fr/discours-dedouard-philippe-lors-du-conseil-national-a-reims-10-mai-2026/", "2026-05-10"))
PHILIPPE = [
    ("q009", 1, src("Discours d’Édouard Philippe au meeting de l’Adidas Arena (horizonsleparti.fr)", "https://horizonsleparti.fr/discours-dedouard-philippe-lors-de-son-grand-meeting-a-ladidas-arena-5-juillet-2026/", "2026-07-05"),
     "décentralisons cette compétence, faisons confiance aux collectivités territoriales"),  # climate policy
    ("q010", 2, EP_SURE, "Un grand plan anticorruption des fonctionnaires : criblage systématique de toutes les fonctions sensibles"),
    ("q011", 1, EP_PROSPERE, "Inscrire dans la Constitution une règle d'or de maîtrise des déficits via un référendum"),
    ("q012", 2, EP_PROSPERE, "Réorganiser massivement l'État en regroupant ou privatisant les agences et opérateurs enchevêtrés, et en simplifiant drastiquement les procédures."),
    ("q019", -2, EP_ANNONCES, "Les 35 heures uniformes pour tout le monde ont fait stagner le salaire des travailleurs."),
    ("q022", 2, EP_PROSPERE, "Supprimer un tiers des fonctionnaires partant à la retraite, soit plus de 250 000 postes sur le quinquennat."),
    ("q024", -2, later(EP_PROSPERE), "Inscrire dans la Constitution une règle d'or de maîtrise des déficits via un référendum"),
    # He wants 65: against keeping 64, but from the other side, so only "plutôt".
    ("q028", -1, EP_PROSPERE, "porter progressivement l'âge de départ à 65 ans et la durée de cotisation à 45 ans en moins de dix ans"),
    ("q029", -2, EP_PROSPERE, "porter progressivement l'âge de départ à 65 ans et la durée de cotisation à 45 ans en moins de dix ans"),
    ("q030", 1, EP_PROSPERE, "les départs anticipés pour carrières longues ; négocier la pénibilité avec les partenaires sociaux"),
    ("q031", 2, EP_PROSPERE, "Généraliser à tous les salariés la retraite par capitalisation collective, qui existe déjà pour les fonctionnaires, et ouvrir un plan d'épargne retraite à chaque Français"),
    ("q035", 1, EP_PROSPERE, "Réduire à 12 mois maximum la durée d'indemnisation chômage pour les moins de 50 ans"),
    ("q036", 1, EP_ENFANTS, "Créer le temps partiel parental : passer à 80% payés 100% pendant 2 mois"),
    ("q040", 2, EP_ANNONCES, "Édouard Philippe se fixe donc l’objectif de diviser au moins l’immigration par deux sur le quinquennat."),
    ("q042", -2, EP_SURE, "Mettre fin au dévoiement de l'asile en faisant voter chaque année par le Parlement une liste de pays sûrs"),
    ("q043", 1, EP_SURE, "Utiliser les centres de retour prévus par le règlement européen retour."),
    ("q046", -1, later(EP_SURE), "Instaurer un « verrou Schengen » : aucun État européen ne doit pouvoir engager seul une régularisation massive au-delà d'un seuil défini collectivement"),
    ("q047", 1, later(EP_SURE), "Mettre en place une véritable politique d'intégration par la langue, le travail et les valeurs républicaines."),
    ("q050", 2, EP_SURE, "Être intraitable avec les étrangers délinquants : expulsion immédiate et fin des aides sociales."),
    ("q055", 2, EP_REIMS, "Choix d’assurer un strict respect de la laïcité républicaine, pour garantir le libre exercice des cultes, sans prosélytisme, obscurantisme religieux, ni religion d’État."),
    ("q067", 2, EP_REIMS, "d’autres populistes, au Royaume-Uni, plongent leur pays, ses entreprises, ses agriculteurs, et ses classes moyennes dans le marasme du Brexit"),
    ("q070", 1, EP_PROSPERE, "Construire une union européenne des marchés de capitaux pour financer l’innovation et la prospérité européenne."),
    ("q073", 2, EP_SURE, "un régime européen d'urgence permettant de suspendre l'enregistrement de nouvelles demandes d'asile face à une attaque hybride sur une frontière"),
    ("q074", 2, EP_SURE, "Massifier nos armées pour garantir la sécurité et la puissance de la France"),
    ("q077", 2, src("Discours d’Édouard Philippe au meeting de l’Adidas Arena (transcription, edouardphilippe.fr)", "https://www.edouardphilippe.fr/actualites/grand-meeting-edouard-philippe-adidas-arena", "2026-07-05"),
     "Aux côtés de l'Ukraine. Sans compromissions, sans ambiguïtés."),
    ("q088", 2, EP_CONQUERANTE, "Assurer notre souveraineté énergétique en relançant le nucléaire (lancement de 8 EPR supplémentaires en plus des 6 déjà prévus)"),
    ("q089", 1, EP_CONQUERANTE, "en développant les renouvelables et en électrifiant massivement nos usages"),
    ("q094", 1, EP_CONQUERANTE, "Verser les mêmes aides pour l’achat d’un véhicule électrique d’occasion qu’on verse pour l’achat d’un véhicule électrique neuf."),
    ("q095", 1, EP_CONQUERANTE, "Créer un fonds unique d'adaptation au changement climatique, réunissant le fonds Barnier et le Fonds vert, doté de 2 milliards d'euros par an"),
    ("q097", -1, EP_PROSPERE, "Renforcer la compétitivité de notre agriculture : zéro surtransposition agricole"),
    ("q098", 2, EP_CONQUERANTE, "Climatiser massivement les lieux accueillant des personnes fragiles."),
    ("q102", 2, EP_CONQUERANTE, "Donner de l'ombre à nos villes en multipliant les plantations d'arbres"),
    ("q103", 2, EP_ENFANTS, "Augmenter de 20 % la rémunération moyenne des enseignants sur le quinquennat"),
    ("q105", 2, EP_ENFANTS, "Faire des chefs d'établissements les véritables patrons de l'école : liberté d'adapter les méthodes et les horaires"),
    ("q107", 1, EP_ENFANTS, "Réduire les effectifs d'élèves en classe, en maternelle et en primaire."),
    ("q110", -1, later(EP_SURE), "vérifier que les étudiants étrangers ont les moyens de leurs études"),
    ("q111", 2, EP_SURE, "appliquer réellement la hausse des droits d'inscription des étudiants extra-européens"),
    ("q112", 1, src("franceinfo (avec AFP) : Édouard Philippe prône une évolution des rythmes scolaires", "https://www.franceinfo.fr/societe/education/blocage-des-lycees/edouard-philippe-prone-une-evolution-des-rythmes-scolaires-avec-un-apprentissage-concentre-en-matinee-et-des-vacances-plus-courtes_8239537.html", "2026-10-16"),
     "Si on veut réduire un petit peu le nombre d'heures d'apprentissage par jour"),
    ("q114", 1, EP_ENFANTS, "liberté d'adapter les méthodes et les horaires, d'imposer l'uniforme"),
    ("q118", 1, later(EP_SURE), "des moyens juridiques d'exception limités dans le temps et dans l'espace, allant jusqu'à l'utilisation ciblée de la reconnaissance faciale"),
    ("q120", 1, EP_SURE, "Mettre en place des peines planchers pour les infractions les plus graves"),
    ("q121", 1, later(EP_SURE), "Lever l'excuse de minorité pour les faits en lien avec le narcotrafic et créer la comparution immédiate des mineurs pour ces infractions."),
    ("q125", 1, later(EP_SURE), "Créer des établissements de réinsertion et de soin pour les mineurs condamnés pour narcotrafic."),
]

# Gabriel Attal (Renaissance) -------------------------------------------------------
# His campaign site (program pages and accounts of his interviews and speeches), his
# letter and Europe speech as PDFs, and Renaissance's thematic conventions, which he
# led as the party's secretary general (labelled as party documents).
AT = "https://attalpresident.fr/actualites/"
DONNE = "https://doc.parti.re/Conventions-thematiques_Nouvelle-donne.pdf"
REGALIEN = "https://doc.parti.re/conventions/Restitution-Regalien-Une-Republique-ferme-une-France-apaisee.pdf"
EUROPE = "https://doc.parti.re/2026/Discours_Europe.pdf"


def at(slug, title, date):
    return src(f"{title} (attalpresident.fr)", AT + slug, date)


def donne(p):
    return src(f"Renaissance, conventions thématiques « Pour une nouvelle donne économique et climatique », p. {p}", f"{DONNE}#page={p}", "2025-07-21")


def regalien(p):
    return src(f"Renaissance, convention régalienne « Une République ferme, une France apaisée », p. {p}", f"{REGALIEN}#page={p}", "2025-05-26")


def europe(p):
    return src(f"Discours de Gabriel Attal « Bâtir les États-Unis d’Europe », Reims, p. {p}", f"{EUROPE}#page={p}", "2026-09-17")


AT_PARISIEN = at("dans-le-parisien-gabriel-attal-vise-le-zero-deficit-en-2037", "Dans Le Parisien, Gabriel Attal vise le zéro déficit en 2037", "2026-07-03")
AT_LYON = at("gabriel-attal-presente-ses-mesures-pour-la-jeunesse-et-l-avenir-de-la-france", "Gabriel Attal présente ses mesures pour la jeunesse et l’avenir de la France", "2026-10-11")
AT_MESSMER = at("gabriel-attal-presente-un-plan-de-desendettement-et-un-messmer-ii-pour-sortir-des-dependances-francaises", "Gabriel Attal présente un plan de désendettement et un « Messmer II » pour sortir des dépendances françaises", "2026-09-23")
AT_BLOIS = at("gabriel-attal-debat-avec-les-francais-a-blois-et-a-bourges", "Gabriel Attal débat avec les Français à Blois et à Bourges", "2026-10-05")
AT_CANICULE = at("face-aux-canicules-gabriel-attal-veut-faire-de-la-geoenergie-le-grand-projet-energetique-de-la-france-du-xxie-siecle", "Face aux canicules, Gabriel Attal veut faire de la géoénergie le grand projet énergétique de la France", "2026-06-25")
AT_TRAVAIL = src("Chantier capital « Travail & salaires », programme de Gabriel Attal (attalpresident.fr)", "https://attalpresident.fr/programme/travail-salaires")
AT_FRONTIERES = src("Chantier capital « Frontières », programme de Gabriel Attal (attalpresident.fr)", "https://attalpresident.fr/programme/frontieres")
AT_MONDE = at("dans-le-monde-gabriel-attal-devoile-son-projet-pour-faire-notre-ecole-la-meilleure-d-europe", "Dans Le Monde, Gabriel Attal dévoile son projet pour faire de notre École la meilleure d’Europe", "2026-08-25")
ATTAL = [
    ("q011", 2, AT_PARISIEN, "proposant d'interdire de se représenter à l'élection suivante les parlementaires ayant voté des budgets qui endettent fortement le pays"),
    ("q012", 2, donne(21), "Un plan de simplification \"Simple comme Bonjour\" pour simplifier les procédures administratives et réduire le nombre de normes."),
    # "Toute hausse d'impôt" rules out a new wealth tax as much as higher income tax.
    ("q013", -1, AT_PARISIEN, "Excluant toute hausse d'impôt durant son quinquennat"),
    ("q014", -1, AT_PARISIEN, "Excluant toute hausse d'impôt durant son quinquennat"),
    # Production taxes rather than the corporate income tax, so only "plutôt".
    ("q016", 1, later(AT_PARISIEN), "poursuivre la baisse des impôts de production"),
    ("q019", -1, AT_TRAVAIL, "Je proposerai de supprimer le plafond d’heures supplémentaires fixé par le Code du travail"),
    ("q020", 1, later(AT_TRAVAIL), "réformer le code du travail pour en faire une constitution du travail avec les grands principes"),
    ("q022", 2, src("Lettre de Gabriel Attal aux Français sur les finances publiques, p. 1", "https://doc.parti.re/2026/Lettre-finances-publiques.pdf#page=1", "2026-10-15"),
     "Ensuite, je lancerai un plan de 150 milliards d’euros d’économies sur le quinquennat."),
    ("q024", -1, later(AT_PARISIEN), "un retour du déficit public sous la barre des 3% est prévu avant 2032"),
    # He would abolish the legal age (a contribution period instead): against keeping 64.
    ("q028", -1, AT_BLOIS, "l’âge légal de départ serait supprimé au profit d’une durée de cotisation décidée par les partenaires sociaux"),
    ("q031", 2, at("aux-assises-de-l-afer-gabriel-attal-defend-une-epargne-qui-finance-l-economie-francaise", "Aux Assises de l’AFER, Gabriel Attal défend une épargne qui finance l’économie française", "2026-09-29"),
     "Élargir progressivement la retraite par capitalisation"),
    ("q034", -1, later(AT_PARISIEN), "afin de remettre les Français en emploi et de générer 5 milliards d'euros d'économies"),  # the unemployment insurance reform
    ("q035", 1, AT_PARISIEN, "la reprise de la réforme de l'assurance chômage initiée lorsqu'il était Premier ministre afin de remettre les Français en emploi"),
    ("q036", 2, donne(29), "Nous proposons de mettre en place un droit opposable à la garde d’enfants, sur le modèle de l’Allemagne"),
    ("q037", -1, AT_PARISIEN, "une « année blanche » gèlera temporairement les prestations sociales, tout en protégeant les petites retraites"),
    ("q040", 1, at("lci-gabriel-attal-defend-un-projet-de-rupture-pour-repondre-aux-grands-defis-du-pays", "LCI : Gabriel Attal défend un projet de rupture pour répondre aux grands défis du pays", "2026-08-25"),
     "réduire l’immigration familiale et étudiante au profit de l’immigration professionnelle"),
    ("q041", 1, AT_FRONTIERES,
     "la préférence travail, où l’on accueille les compétences, les talents dont nous avons besoin sur la base d’un système à points comme au Canada"),
    ("q054", 2, at("gabriel-attal-fin-de-vie-l-aboutissement-d-un-long-chemin-et-la-consecration-d-un-droit-nouveau", "Fin de vie : Gabriel Attal salue la consécration d’un nouveau droit", "2026-07-15"),
     "C’est la consécration d’un droit nouveau et d’une liberté nouvelle pour les Français."),
    # Children only: the same document opposes banning the veil for adult women.
    ("q058", 1, regalien(61), "Protéger les enfants des instrumentalisations et du prosélytisme, en interdisant le voilement des enfants"),
    ("q059", 1, AT_LYON, "Généralisation du testing avec publication des résultats"),
    ("q067", 2, later(europe(10)), "il n’y a que deux choix politiques possibles : le vieux cauchemar du Frexit ou un rêve nouveau"),
    # A federation for the economy, technology and ecology; regalian powers stay national.
    ("q068", 1, europe(20), "au cœur de cette fédération économique, technologique, écologique"),
    ("q070", 2, europe(20), "Je propose de créer ces Etats-Unis d’Europe en faisant le premier référendum européen"),
    # Against unanimity, without naming qualified majority as the remedy.
    ("q071", 1, later(europe(10)), "Sur des décisions essentielles, l’unanimité permet à un seul gouvernement de retenir tous les autres."),
    ("q075", 1, later(AT_FRONTIERES), "Notre dissuasion nucléaire doit être un outil de puissance, à travers notamment la doctrine de dissuasion nucléaire avancée proposée par le président de la République."),
    ("q076", 1, europe(13), "Créer une base industrielle et technologique de défense européenne intégrée pour produire massivement"),
    ("q077", 2, at("gabriel-attal-dans-politico-europe-ukraine-ia-et-finances-publiques-quatre-priorites-pour-preparer-la-france-de-demain", "Gabriel Attal dans POLITICO : Europe, Ukraine, IA et finances publiques", "2026-09-24"),
     "Il faut poursuivre notre soutien à l'Ukraine."),
    ("q088", 2, AT_MESSMER, "Sur le nucléaire, Gabriel Attal veut sécuriser la construction des 14 EPR et retrouver une capacité de construction en série"),
    ("q089", 1, AT_MESSMER, "Il défend aussi l’accélération des énergies renouvelables dans une logique de neutralité technologique."),
    ("q090", 1, AT_MESSMER, "Un « plan Messmer II » pour sortir des énergies fossiles"),
    ("q093", 1, donne(65), "nous rétablirons la possibilité, pour les villes le souhaitant, d’instaurer une Zone à faible émission."),
    ("q094", 1, AT_LYON, "Prime pour les véhicules propres d’occasion"),
    ("q095", 1, at("en-deplacement-a-la-grande-motte-gabriel-attal-va-a-la-rencontre-de-la-france-qui-travaille-l-ete", "En déplacement à La Grande-Motte, Gabriel Attal va à la rencontre de la France qui travaille l’été", "2026-08-13"),
     "renforcer les moyens matériels des secours, notamment avec davantage d’hélicoptères et d’avions bombardiers d’eau"),
    ("q098", 1, AT_CANICULE, "sanctuarisera l'isolation et le rafraîchissement des structures accueillant les publics les plus vulnérables"),
    # A refounded carbon tax ("compte épargne-carbone") to be explored, so only "plutôt".
    ("q101", 1, later(donne(58)), "Explorer une fiscalité carbone entièrement refondée pour être plus juste"),
    ("q103", 2, AT_MONDE, "une nouvelle revalorisation salariale de 200 euros nets par mois pour les enseignants"),
    ("q104", 2, AT_LYON, "Contrat dès la première entre chaque lycéen professionnel et une entreprise pour garantir un emploi ou une alternance après le diplôme"),
    ("q105", 1, later(AT_MONDE), "Gabriel Attal veut renforcer l’autonomie des établissements, y compris dans le primaire."),
    ("q106", 1, AT_BLOIS, "On doit aller plus loin pour arriver à 20 000 formés dans les années qui viennent et faire en sorte qu'ils restent."),
    ("q107", 2, src("Chantier capital « École », programme de Gabriel Attal (attalpresident.fr)", "https://attalpresident.fr/programme/education"),
     "nous devons viser moins de 20 élèves par classe comme dans les meilleurs systèmes éducatifs européens"),
    ("q108", 1, AT_CANICULE, "en poursuivant massivement le mouvement engagé dans les écoles pour les jeunes enfants"),
    ("q113", 2, AT_LYON, "Réforme de Parcoursup avec mentorat, tutorat et stages"),
    ("q116", 2, at("dans-la-tribune-dimanche-gabriel-attal-veut-un-referendum-pour-interdire-les-reseaux-sociaux-aux-moins-de-15-ans", "Dans La Tribune Dimanche, Gabriel Attal veut un référendum pour interdire les réseaux sociaux aux moins de 15 ans", "2026-08-16"),
     "Gabriel Attal veut un référendum pour interdire les réseaux sociaux aux moins de 15 ans"),
    ("q121", 1, at("gabriel-attal-sur-bfm-tv-sa-strategie-de-rupture-pour-rebatir-la-justice-et-proteger-les-enfants", "Sur BFM TV, la stratégie de rupture de Gabriel Attal pour rebâtir la justice et protéger les enfants", "2026-06-10"),
     "Son projet prévoit l'instauration d'une procédure de comparution immédiate pour les mineurs, aujourd'hui inexistante."),
    ("q118", 2, later(regalien(14)), "Prolonger et étendre l’expérimentation du recours à la vidéoprotection algorithmique lancée lors des Jeux Olympiques et Paralympiques"),
    ("q138", 1, at("dans-le-jdd-gabriel-attal-veut-proposer-la-plus-grande-reforme-institutionnelle-depuis-1958", "Dans le JDD, Gabriel Attal veut proposer la plus grande réforme institutionnelle depuis 1958", "2026-08-02"),
     "tout en facilitant le recours aux référendums locaux"),
    # Densifying towns ("surélévation", "division des parcelles") rather than building further out.
    ("q140", 1, later(donne(78)), "Construire plus loin n’est plus soutenable."),
    ("q142", 2, regalien(19), "Donner plus de compétences aux polices municipales"),
]

# Bruno Retailleau (Les Républicains) ---------------------------------------------
# The LR "Nos propositions pour la France" booklets published under his presidency of
# the party, his own op-eds, interviews and statements on republicains.fr, and press
# reports. A carbon border adjustment (his and Philippe's) isn't read as a carbon tax.
LR = "https://republicains.fr/wp-content/uploads/"
LR_ACTU = "https://republicains.fr/actualites/"


def lr(path, title, date, p):
    return src(f"Les Républicains, « Nos propositions pour la France : {title} », p. {p}", f"{LR}{path}#page={p}", date)


def lr_actu(path, title, date):
    return src(f"{title} (republicains.fr)", LR_ACTU + path, date)


R_FIGARO = lr_actu("2026/09/02/en-france-la-seule-cour-supreme-cest-le-peuple-je-lui-donnerai-le-dernier-mot/", "« En France, la seule cour suprême, c’est le peuple », entretien de Bruno Retailleau au Figaro", "2026-09-02")
R_DISSUASION = lr_actu("2026/03/01/la-dissuasion-nucleaire-francaise-ne-se-partage-pas/", "« La dissuasion nucléaire française ne se partage pas », tribune de Bruno Retailleau au JDD", "2026-03-01")
R_LCP = src("LCP : Retraites, Bruno Retailleau veut un âge minimal de départ à 63 ans et un taux plein à 65 ans", "https://lcp.fr/actualites/retraites-bruno-retailleau-veut-un-age-minimal-de-depart-a-63-ans-et-un-taux-plein-a-65", "2026-09-23")
R_ECONOMIES = src("Public Sénat : Bruno Retailleau s’engage sur un plan d’économies de près de 200 milliards d’euros, s’il est élu", "https://www.publicsenat.fr/actualites/economie/presidentielle-2027-bruno-retailleau-sengage-sur-un-plan-deconomies-de-pres-de-200-milliards-deuros-sil-est-elu", "2026-10-12")
R_SCHENGEN = later(lr_actu("2026/08/02/lespace-schengen-doit-etre-reserve-aux-europeens/", "« L’espace Schengen doit être réservé aux Européens ! », entretien de Bruno Retailleau au JDD", "2026-08-02"))
R_CLIMAT = lr_actu("2026/08/09/face-au-rechauffement-climatique-adapter-la-france-plutot-que-punir/", "« Face au réchauffement climatique, adapter la France plutôt que punir », tribune de Bruno Retailleau", "2026-08-09")
R_CHAUD = "S’adapter, c’est équiper enfin nos écoles, nos crèches, nos hôpitaux et nos Ehpad"  # "pour que plus jamais on ne compte les glaçons"


def lr_produire(p):
    return lr("2026/02/LR_Produire_Plus_LIVRET.pdf", "Produire plus pour vivre mieux", "2026-02-19", p)


def lr_ecole(p):
    return lr("2026/09/LR_Ecole_vF.pdf", "Éducation", "2026-09-03", p)


def lr_logement(p):
    return lr("2026/05/LR_Logement.pdf", "Se loger mieux et moins cher", "2026-05-28", p)


RETAILLEAU = [
    ("q012", 2, lr_produire(14),
     "La règle du « un pour un » sera strictement appliquée en valeur, afin de garantir une baisse nette, mesurable et vérifiable des contraintes."),
    ("q020", 1, later(lr_produire(12)), "Refonder le code du travail sur 50 principes, renvoyer le reste à la négociation collective"),
    ("q021", 1, lr_produire(26),
     "Nous créerons un Fonds France Production, intégralement financé, doté de 600 millions d’euros par an, exclusivement dédié à la modernisation de l’outil industriel."),
    ("q022", 2, R_ECONOMIES, None),  # 197 billion euros of savings by 2032, mostly from the State and social spending (news summary)
    ("q029", -1, R_LCP, "L'âge minimal de départ, c'est 63 ans"),
    # Keeps the existing allowances for disability, illness, arduous work and wear (news summary).
    ("q030", 1, later(R_LCP), None),
    ("q031", 1, R_LCP, "C'est fondamental pour les jeunes, mais aussi pour nos entreprises"),  # a funded part "pour les jeunes"
    ("q038", 1, later(R_LCP), "entre l'âge de départ à taux plein et l'espérance de vie"),  # the full-rate age, not the minimum of 63
    ("q035", 2, lr("2026/01/51705_LesRepublicains_Brochures_A5-40P_DEF.pdf", "Le travail gagnant", "2026-01-09", 31),
     "L’assurance chômage doit sécuriser les transitions professionnelles et encourager un retour rapide vers l’emploi, non financer une inactivité durable."),
    ("q036", 2, lr("2026/05/LR_Famille_vFinale.pdf", "Une politique pour toutes les familles de France", "2026-05-04", 18),
     "À son issue, nous proposons d’étendre le congé de naissance jusqu’aux six mois de l’enfant."),
    ("q037", -1, lr("2026/01/51705_LesRepublicains_Brochures_A5-40P_DEF.pdf", "Le travail gagnant", "2026-01-09", 28),
     "Réduire l’assistance grâce au Compte social unique (CSU)"),
    ("q039", -2, lr_logement(36),
     "Nous rétablirons une protection effective du droit de propriété en mettant en place une politique de tolérance zéro contre le squat et les mauvais payeurs."),
    ("q040", 2, lr_actu("2026/02/12/je-suis-candidat-a-lelection-presidentielle/", "« Je suis candidat à l’élection présidentielle », déclaration de Bruno Retailleau", "2026-02-12"),
     "je vous soumettrai directement par référendum plusieurs grands textes de loi : pour réduire drastiquement l’immigration"),
    ("q042", -1, later(R_ECONOMIES), None),  # asylum claims examined outside France's borders (news summary)
    ("q046", -1, R_SCHENGEN, "J’avais indiqué il y a quelques mois que la régularisation massive de près d’un million de personnes en Espagne était totalement irresponsable."),
    ("q048", 2, src("Communiqué de presse de Bruno Retailleau, président des Républicains", "https://republicains.fr/wp-content/uploads/2026/08/CP_BR_31_07_26.pdf", "2026-07-31"),
     "Face à la gravité de la situation, je demande la suspension de la libre circulation des personnes avec l’Espagne au sein de l’Union européenne."),
    ("q053", 1, later(R_FIGARO), "abolir le droit du sol et revenir à l’assimilation pour qu’il n’y ait plus de naturalisations automatiques"),
    ("q055", 2, later(lr_ecole(32)), "La laïcité sera appliquée sans accommodement."),
    ("q058", 1, later(R_FIGARO), "on n’a pas le droit d’installer une crèche de Noël dans une mairie, mais en revanche une conseillère municipale peut y siéger voilée !"),
    ("q068", -1, R_FIGARO, "Je souhaite que les institutions européennes s’en tiennent à leurs attributions"),
    ("q069", 1, R_FIGARO, "Je veux donc préciser à l’article 88 de notre Constitution que le droit européen ne sera supérieur à la loi qu’à deux conditions."),
    ("q073", 2, R_SCHENGEN, "il faut que l’Europe protège fermement ses frontières extérieures"),
    ("q074", 2, lr_actu("2026/07/14/lunite-nationale-premiere-de-nos-armes/", "« L’unité nationale, première de nos armes », tribune de Bruno Retailleau", "2026-07-14"),
     "une loi de programmation militaire comportant cette fois une trajectoire budgétaire sincère et sanctuarisée, pour atteindre 100 milliards d’euros à la fin du quinquennat"),
    ("q075", 1, R_DISSUASION, "Sur le plan militaire, cela passe par la nécessité de maintenir et moderniser une dissuasion autonome"),
    ("q076", 1, R_DISSUASION, "il est dans notre intérêt de renforcer nos coopérations opérationnelles et industrielles avec nos partenaires européens quand c’est possible"),
    ("q078", -1, R_SCHENGEN, "conditionner l’aide au développement à la reprise des ressortissants lorsqu’ils sont expulsés"),
    ("q088", 2, lr("2026/05/LR_Electricite_vFF070626.pdf", "Électricité", "2026-05-07", 9), "CONFIRMER les nouveaux EPR2 en veillant à la tenue des coûts et des délais."),
    ("q089", -2, lr("2026/05/LR_Electricite_vFF070626.pdf", "Électricité", "2026-05-07", 9),
     "STOPPER le subventionnement de nouvelles capacités éoliennes et photovoltaïques en France métropolitaine et contenir les coûts réseaux."),
    ("q095", 1, R_CLIMAT, "S’adapter, c’est stocker l’eau l’hiver, quand elle est abondante, pour irriguer nos champs pendant l’été."),
    ("q097", -2, lr("2026/03/LR_Agriculture.pdf", "Réarmer notre agriculture", "2026-03-03", 17),
     "Nous autoriserons de nouveau l’usage de certains néonicotinoïdes, dont l’acétamipride"),
    ("q098", 2, later(R_CLIMAT), R_CHAUD),
    ("q103", 2, lr_ecole(10),
     "Nous alignerons ainsi intégralement le début de carrière sur la moyenne européenne, soit 135 euros nets de plus chaque mois"),
    ("q105", 2, later(lr_ecole(22)), "Un grand vent de liberté soufflera sur les établissements."),
    ("q108", 1, later(R_CLIMAT), R_CHAUD),
    ("q110", -1, later(lr_logement(47)), "Exclusion des APL pour les étudiants étrangers non boursiers"),
    ("q113", 2, later(lr_ecole(27)), "Dans le cadre de la refondation de Parcoursup et de la revalorisation du Baccalauréat, nous proposons d’intégrer les résultats du Bac au processus d’orientation."),
    ("q118", 1, lr("2026/07/LR_IA.pdf", "L’IA au service des Français", "2026-07-07", 37),
     "nous autoriserons, dans un cadre légal et contrôlé, l’usage de la vision par ordinateur pour certains objectifs de sécurité et de protection"),
    ("q120", 2, R_FIGARO, "si aujourd’hui les peines minimales existent, leur application dépend du juge. Je veux qu’elles soient désormais obligatoires"),
    ("q132", 1, later(R_ECONOMIES), None),  # vocational training handed to the regions (news summary)
    ("q135", 1, later(lr_logement(35)), "Mieux réguler les meublés touristiques (type Airbnb)"),
    ("q140", -2, lr_logement(8),
     "Nous abrogerons le Zéro artificialisation nette qui bloque des territoires entiers et empêche de construire."),
]

# Raphaël Glucksmann (Place publique) ---------------------------------------------
# Place publique's program "Acte I" (June 2025), which he presents as his project (the
# copy on the party's "Le projet" page; an older link to it is dead), and press reports
# of the socialist primary's debates.
PP = "https://place-publique.eu/document/6J8wjk3EW8dBCLwKxa7J96/projet-placepublique-acte1.pdf"


def pp(p):
    return src(f"Place publique, « Notre vision pour la France. Acte I », p. {p}", f"{PP}#page={p}", "2025-06-23")


GL_ROYAL = src("LCP : Glucksmann face à Royal, divisions sur LFI, lycées… Ce qu’il faut retenir du dernier débat de la primaire socialiste", "https://lcp.fr/actualites/glucksmann-face-a-royal-divisions-sur-lfi-lycees-ce-qu-il-faut-retenir-du-dernier-debat", "2026-10-05")
GLUCKSMANN = [
    ("q001", -1, pp(46), "Lancer en parallèle une grande convention citoyenne qui jettera les bases d’une assemblée constituante pour changer la Constitution."),
    ("q002", 2, pp(46), "Supprimer l’article 16 de la Constitution (pouvoirs exceptionnels du Président en temps de crise)"),
    ("q003", 1, pp(46), "Investir le premier ministre par un vote de confiance de l’Assemblée nationale"),
    ("q004", 2, pp(46), "Instaurer immédiatement la proportionnelle, de préférence par circonscriptions régionales avec un fléchage départemental des candidats."),
    # As written, the vote at 16 may be meant for local elections only.
    ("q005", 1, pp(47), "Ouvrir le droit de vote à 16 ans et pour les étrangers extra-communautaires aux élections locales"),
    ("q007", 2, pp(47), "Instaurer un droit d’initiative citoyenne, permettant de déclencher des séquences démocratiques avec des référendums"),
    ("q009", 2, pp(47), "Porter une nouvelle loi de décentralisation qui sera en même temps une loi de clarification des compétences de notre organisation territoriale"),
    ("q010", 2, pp(48), "Agir contre le pantouflage, renforcer la transparence comme la lutte contre la corruption"),
    ("q014", 2, pp(85), "Effort fiscal nouveau, ciblé sur les très hauts patrimoines et les grands groupes, pour contrer leur optimisation fiscale"),
    ("q017", 2, pp(40), "Augmenter le SMIC à 1600 euros net dans les deux ans qui suivent notre accession au pouvoir."),
    ("q018", 1, GL_ROYAL, None),  # tax inheritances over two million euros to cut the CSG on wages (news summary)
    ("q026", 1, pp(34), "Instaurer un revenu de transition écologique pour soutenir agriculteurs et pêcheurs passant au bio ou à des pratiques durables."),
    ("q028", -2, GL_ROYAL, "Nous abrogerons la réforme injuste de 2023."),
    ("q029", 2, GL_ROYAL, "On ne pourra pas faire 60 ans, ce sera 62 ans"),
    ("q030", 2, src("Public Sénat : fiscalité, école, immigration, ce que propose Raphaël Glucksmann", "https://www.publicsenat.fr/actualites/politique/fiscalite-ecole-immigration-ce-que-propose-raphael-glucksmann", "2026-08-24"),
     "L’équité exige que ceux qui ont les carrières les plus hachées et les métiers les plus difficiles puissent partir à la retraite plus tôt."),
    ("q031", -2, GL_ROYAL, None),  # he and Royal both oppose adding individual funded pensions (news summary)
    ("q032", 2, pp(53), "Ouvrir un grand chantier afin d’aller vers une Sécurité sociale unique, simple et juste, qui fusionne tous les régimes"),
    ("q035", -2, pp(53), "Abroger la réforme Macron de l’assurance chômage, injuste et inefficace."),
    ("q036", 2, pp(78), "Investir dans le service public de la petite enfance, créer un droit opposable à la garde"),
    ("q039", 1, pp(64), "abroger la loi Kasbarian au profit d’un dispositif plus équilibré"),
    ("q040", -1, pp(82), "Abroger la loi immigration de 2024."),
    ("q041", 1, pp(82), "Créer des voies légales et sécurisées d’immigration de travail"),
    ("q042", 2, pp(82), "ouvrir le droit au travail, sans autorisation spécifique, dès l’enregistrement de la demande d’asile"),
    ("q043", 1, pp(82), "Mettre fin au système de la politique du chiffre sur les OQTF, et appliquer celles délivrées."),
    ("q046", 2, pp(82), "Faciliter les démarches de régularisation des travailleurs sans papiers"),
    ("q055", 2, pp(73), "Nous défendons fermement la laïcité républicaine."),
    ("q059", 1, pp(80), "Généraliser les récépissés de contrôle d’identité."),
    ("q061", 2, pp(79), "Nous allons défendre les droits des personnes LGBTQIA+, partout en France et en Europe."),
    ("q062", 2, pp(78), "aux inégalités d’accès à l’IVG, à l’ignorance des douleurs menstruelles ou de l’endométriose, nous exigeons une réponse à la hauteur"),
    ("q070", 2, pp(12), "notre ambition fédérale pour l’Europe est donc guidée par le souci de l’efficacité et du réalisme"),
    ("q071", 2, pp(12), "clarifiant et démocratisant le fonctionnement de l’Union passant à la majorité qualifiée au Conseil européen"),
    ("q072", 1, pp(12), "Augmenter massivement le budget de l’Union pour lui permettre de lancer des politiques publiques"),
    ("q074", 2, pp(10), "Lancer de grands programmes de production de drones, de modernisation de nos capacités spatiales"),
    ("q075", 1, pp(11), "Proposer à nos partenaires de l’UE d’étendre la dissuasion nucléaire française aux autres pays de l’Union européenne"),
    ("q076", 2, pp(11), "Oeuvrer à la mise en place rapide d’un fonds européen de défense de 500 milliards d’euros via un emprunt commun."),
    ("q077", 2, GL_ROYAL, None),  # wants to "renforcer" aid to Ukraine, paid for by seizing Russian assets (news summary)
    ("q078", 2, pp(83), "atteindre progressivement 0,7 % du RNB dédié à l’aide publique au développement"),
    ("q082", -2, pp(17), "Interdire immédiatement toute importation de gaz russe"),
    ("q085", 2, pp(83), "reconnaître enfin un Etat Palestinien aux côtés d’Israël"),
    ("q087", 2, pp(83), "reconnaître enfin un Etat Palestinien aux côtés d’Israël"),
    ("q088", 1, pp(17), "Conforter le rôle du nucléaire, énergie pilotable et décarbonée, en assurant la sûreté des centrales existantes et la construction à temps de nouvelles unités."),
    ("q089", 2, pp(17), "Lancer un grand plan d’investissement pluriannuel dans toutes les énergies renouvelables."),
    ("q090", 2, pp(17), "Pour redevenir une puissance industrielle et nous libérer de notre dépendance aux puissances fossiles, nous devons opérer une véritable révolution énergétique."),
    ("q091", 2, src("LCP : accord avec LFI, Moyen-Orient, pouvoir d’achat, ce qu’il faut retenir du premier débat de la primaire de gauche", "https://lcp.fr/actualites/accord-avec-lfi-moyen-orient-pouvoir-d-achat-ce-qu-il-faut-retenir-du-premier-debat-de", "2026-09-23"),
     "triplement du chèque énergie"),
    ("q092", 2, pp(29), "Relancer les trains de nuit, accélérer les LGV et les liaisons prioritaires pour faire l’Europe du Rail."),
    ("q096", 2, pp(29), "Créer un service public de transport rural pour désenclaver les territoires"),
    ("q097", 2, pp(35), "Éliminer les produits chimiques dangereux en interdisant les pesticides les plus néfastes, glyphosate, néonicotinoïdes tueurs d’abeilles"),
    ("q100", 2, pp(29), "Mettre fin aux privilèges actuels des transports polluants : suppression des exonérations de TVA et de taxe sur le kérosène"),
    ("q103", 2, pp(68), "Revaloriser le salaire de tous les enseignants de manière continue et planifiée sur 5 ans."),
    ("q107", 2, pp(68), "Réduire le nombre d’élèves par enseignant en primaire et l’expérimenter dans le second degré"),
    ("q113", 2, pp(25), "Repenser en profondeur Parcoursup à travers une concertation réunissant parents, étudiants, universités et acteurs de l’éducation."),
    ("q116", 2, pp(21), "Interdire les réseaux sociaux pour les moins de 15 ans"),
    ("q117", 1, pp(60), "Faire renaître une police de proximité moderne, ancrée localement, centrée sur la prévention, la médiation et la résolution de conflits."),
    # A citizens' convention to decide on legalization: undecided, not for or against.
    ("q123", 0, pp(60), "Organiser une convention citoyenne sur la politique vis-à-vis des drogues, notamment la question de la légalisation du cannabis."),
    ("q125", 2, pp(61), "en investissant dans des prisons rénovées et dignes et dans le renforcement des parcours individualisés de réinsertion"),
    ("q133", 1, pp(47), "en renforçant le pouvoir d’imposition des collectivités"),
    ("q135", 2, pp(64), "Réguler et maîtriser davantage les meublés touristiques comme au Pays basque et en Suisse pour limiter les activités des plateformes telles que Airbnb."),
    ("q137", 2, pp(28), "Grâce aux débats et à des outils comme les budgets participatifs verts ou les parlements de l’eau, les citoyens coconstruiront les politiques locales de l’environnement."),
    ("q139", 2, pp(64), "Créer un fonds national pour aider les collectivités à acquérir du foncier et y développer du logement abordable"),
    ("q140", 2, pp(28), "Défendre résolument les objectifs du Zéro Artificialisation Nette des sols (ZAN)"),
]

# David Lisnard (Nouvelle Énergie) -------------------------------------------------
# His party's program pages, its booklets and his speeches, and its "Questions" pages,
# which state his positions with links to the interviews they come from.
NE = "https://www.unenouvelleenergie.fr/"
NOIR = f"{NE}api/media/file/Nouvelle_energie_Livre_noir_pages_20_24_inversees.pdf"


def ne_q(slug, title, date):
    return src(f"Nouvelle Énergie (parti de David Lisnard), « {title} »", f"{NE}questions/{slug}/", date)


def ne_prog(slug, title):
    return src(f"Nouvelle Énergie, programme : « {title} »", f"{NE}notre-programme/{slug}/")


def noir(p):
    return src(f"Nouvelle Énergie, « Le livre noir : en finir avec la bureaucratie », p. {p}", f"{NOIR}#page={p}", "2026-04-22")


NE_RETRAITE = ne_q("quel-age-de-depart-a-la-retraite-david-lisnard-defend-il", "Quel âge de départ à la retraite David Lisnard défend-il ?", "2026-10-03")
NE_CIVIQUE = ne_prog("generer-un-renouveau-civique", "Générer un renouveau civique")
NE_AMBITION = ne_prog("reussir-une-nouvelle-ambition-francaise", "Réussir une nouvelle ambition française")
NE_ECOLE = ne_prog("education", "École")
NE_SECURITE = ne_prog("securite", "Sécurité")
NE_IMMIGRATION = ne_prog("immigration", "Immigration")
NE_DESTIN = ne_prog("etre-maitre-de-notre-destin", "Être maître de notre destin")
NE_DEFICIT = "la France doit désormais s’astreindre à une règle institutionnelle de limitation des déficits publics"
NE_ARMEE = ne_q("quel-candidat-veut-renforcer-l-armee", "Quel candidat à la présidentielle 2027 veut renforcer l’armée ?", "2026-10-16")
NE_UKRAINE = ne_q("quelle-est-la-position-de-david-lisnard-sur-la-guerre-en-ukraine", "Quelle est la position de David Lisnard sur la guerre en Ukraine ?", "2026-10-16")


def bayeux(p):
    return src(f"Discours de David Lisnard à Bayeux, p. {p}", f"https://nouvelle-energie-media-prod.s3.fr-par.scw.cloud/media/legacy/2026/06/Discours-de-David-Lisnard-a-Bayeux-17062026.pdf#page={p}", "2026-06-17")


LISNARD = [
    ("q002", 1, NE_DESTIN, "A l’opposé de l’« hyperprésidentialisme jupitérien », le rôle du Président de la République doit être recentré sur son statut constitutionnel"),
    ("q007", 2, bayeux(9),
     "Le référendum d’initiative populaire sera vraiment institué et rendu praticable, avec un seuil de signatures atteignable et, au terme du délai, un vote garanti."),
    ("q009", 2, NE_DESTIN, "placer la subsidiarité – et donc la décentralisation – au cœur du fonctionnement démocratique français"),
    ("q011", 1, NE_DESTIN, NE_DEFICIT),
    ("q012", 2, noir(16), "Le «Silence vaut accord» généralisé et les délais opposables."),
    ("q014", -2, noir(7), "supprimer l’IFI et le remplacer par une fiscalité foncière assise sur des valeurs vénales actualisées"),
    ("q015", 1, noir(7), "Exonérer de CFE et de cotisations URSSAF toute entreprise nouvelle pendant les douze premiers mois."),
    ("q016", 2, ne_q("quel-candidat-veut-baisser-les-impots", "Quel candidat à la présidentielle 2027 veut baisser les impôts ?", "2026-10-16"),
     "ramener l’impôt sur les sociétés à 20 % avec une part variable laissée aux collectivités locales entre 0 et 5 %"),  # quoting his book
    ("q019", -1, noir(6), "35 heures : renchérissement des heures supplémentaires, trois semaines de moins travaillées par an qu’en Allemagne."),
    ("q020", 1, NE_AMBITION, "l’instauration d’un contrat de travail unique pour les nouveaux emplois, fusionnant CDI et CDD avec des indemnités de licenciement qui seraient progressives"),
    ("q022", 2, ne_q("quelles-economies-david-lisnard-propose-t-il-et-ou-exactement", "Quelles économies propose David Lisnard ?", "2026-10-03"),
     "Le rythme annoncé est de 80 milliards d’euros dès la première année, pour au moins 200 milliards en trajectoire."),
    ("q024", -2, NE_DESTIN, NE_DEFICIT),
    # He keeps the 2023 reform but calls it insufficient and answers with funded pensions, not age.
    ("q028", 1, NE_RETRAITE, "Cette augmentation de la durée de vie au travail est nécessaire mais pas suffisante"),
    ("q029", -2, NE_RETRAITE, "il ne faut pas défaire la réforme des retraites de 2023, ni celle de l’assurance chômage"),
    ("q031", 2, ne_q("david-lisnard-est-il-favorable-a-la-retraite-par-capitalisation", "David Lisnard est-il favorable à la retraite par capitalisation ?", "2026-10-03"),
     "Obligatoire, donc universel : il insiste sur l’universalité de la capitalisation, pour qu’elle ne bénéficie pas seulement à ceux qui peuvent épargner."),
    ("q035", 2, ne_q("quel-candidat-veut-reformer-l-assurance-chomage", "Quel candidat à la présidentielle 2027 veut réformer l’assurance chômage ?", "2026-10-16"),
     "David Lisnard est favorable à la dégressivité des allocations chômage, associée à une vraie formation des demandeurs d’emploi en difficulté."),
    ("q037", -1, ne_q("quel-candidat-veut-regrouper-les-aides-sociales-en-une-allocation-unique", "Quel candidat veut regrouper les aides sociales en une allocation unique ?", "2026-10-03"),
     "David Lisnard propose de regrouper l’ensemble des aides sociales en une allocation unique, plafonnée à un pourcentage du SMIC."),
    ("q040", 2, NE_IMMIGRATION, "Diviser par huit la délivrance de titres de séjour"),
    ("q042", -1, NE_IMMIGRATION, "Traiter les demandes d’asiles au sein de nos consulats à l’étranger"),
    ("q050", 2, NE_IMMIGRATION, "Expulser systématiquement les étrangers condamnés pour délits graves et les fichés S étrangers"),
    ("q058", 2, NE_SECURITE, "interdiction du voile à l’université"),
    ("q069", 2, bayeux(10), "Il nous faudra suivre la voie ouverte par le Danemark qui a obtenu d’être dispensé des règles communes d’asile et d’immigration."),
    ("q073", 1, NE_AMBITION, "Le meilleur contrôle effectif des frontières doit s’appuyer sur le renforcement des dispositifs nationaux avec le concours des nouveaux moyens de Frontex."),
    ("q074", 2, NE_ARMEE, "David Lisnard juge « incontournable » d’augmenter le budget de la défense et veut une armée forte pour garantir la paix."),
    ("q075", 1, NE_ARMEE, "Il plaide pour un système de combat aérien souverain bâti sur le Rafale, ses drones et la dissuasion nucléaire"),
    ("q077", 2, NE_UKRAINE, "Il défend le droit du peuple ukrainien à disposer de lui-même et demande de produire et de livrer des armes"),
    ("q082", -1, NE_UKRAINE, "l’intérêt du pays est que la Russie ne gagne pas cette guerre"),
    ("q088", 2, ne_q("quel-candidat-veut-construire-de-nouveaux-reacteurs-nucleaires", "Quel candidat à la présidentielle 2027 veut construire de nouveaux réacteurs nucléaires ?", "2026-10-03"),
     "prolonger les réacteurs existants jusqu’à soixante ans, construire une première série de six EPR, déployer des mini-réacteurs pour renouveler le parc"),
    ("q089", -2, NE_CIVIQUE, "Il faut mettre un terme à cette gabegie en faisant rentrer ces projets dans le droit commun"),  # renewables' special regime
    ("q093", -2, ne_q("quel-candidat-veut-supprimer-les-zones-a-faibles-emissions-zfe", "Quel candidat à la présidentielle 2027 veut supprimer les zones à faibles émissions (ZFE) ?", "2026-10-16"),
     "David Lisnard s’engage à supprimer les zones à faibles émissions par une loi dès son arrivée au pouvoir"),
    ("q092", 1, NE_AMBITION, "un plan d’investissement dans les infrastructures routières et ferroviaires"),
    ("q101", 1, NE_CIVIQUE, "Le prix du carbone et la fiscalité verte pour facturer la pollution."),  # at constant total taxation
    ("q103", 1, NE_ECOLE, "Nous proposons une augmentation de 20 % des rémunérations en cinq ans, conditionnée à une réorganisation profonde"),
    ("q104", 1, NE_AMBITION, "Enfin, la limite d’âge pour l’apprentissage sera revue à la baisse."),
    ("q105", 2, NE_ECOLE, "la liberté donnée aux chefs d’établissement de recruter leurs équipes pédagogiques, d’appliquer leurs méthodes, de gérer leur budget"),
    ("q106", 1, src("Nouvelle Énergie, « Les Carnets : Santé », p. 4", "https://nouvelle-energie-media-prod.s3.fr-par.scw.cloud/media/legacy/2026/05/Livret-Sante-Nouvelle-Energie.pdf#page=4", "2026-05-05"),
     "Doubler le nombre d'étudiants formés d'ici 2030"),
    ("q113", 2, noir(9), "Supprimer Parcoursup et le remplacer par un système d’affectation fondé sur les résultats scolaires objectifs."),
    ("q115", -2, NE_ECOLE, "un financement public équivalent, que la famille choisisse l’enseignement public ou privé"),
    ("q118", 1, NE_SECURITE, "réduire la bureaucratie policière et moderniser les outils (vidéoprotection, radios numériques, IA de prévention"),
    ("q119", 2, ne_q("quel-candidat-veut-que-les-peines-soient-reellement-executees", "Quel candidat à la présidentielle 2027 veut que les peines soient réellement exécutées ?", "2026-10-16"),
     "David Lisnard s’engage à ce que les peines prononcées soient intégralement exécutées, et propose d’instaurer la perpétuité réelle."),
    ("q120", 2, NE_SECURITE, "rétablir les peines planchers pour les récidivistes"),
    ("q121", 2, NE_SECURITE, "Nous voulons abaisser la majorité pénale à 16 ans, inverser le principe de l’excuse de minorité dès 13 ans"),
    ("q133", 1, NE_CIVIQUE, "Les recettes fiscales et autres ressources propres doivent redevenir « une part déterminante de l’ensemble de leurs ressources »."),
    ("q139", -1, NE_AMBITION, "une mesure essentielle sera la suppression de l’article 55 de la loi SRU"),
    ("q140", -1, noir(7), "Décentraliser l’objectif ZAN aux EPCI."),
    ("q142", 2, NE_SECURITE, "Il faut ainsi permettre aux communes volontaires d’armer leur police municipale et de disposer d’outils réels : accès aux fichiers, possibilité de verbalisation renforcée"),
]

# Marine Tondelier (Les Écologistes) -----------------------------------------------
# The party's program "Pour une prospérité écologique" (July 2026), on which she runs.
EC = "https://lesecologistes.fr/document/3N4JsAEmq6vsx42IITGNZa/vdef-programme-1.pdf"


def ec(p):
    return src(f"Les Écologistes, « Pour une prospérité écologique », programme, p. {p}", f"{EC}#page={p}", "2026-07-01")


EC_FEDERALE = "La France est puissante dans le cadre d’une Europe fédérale et solidaire."
EC_CLIM = "Rafraîchir les bâtiments publics (hôpitaux, EHPAD, établissements de santé, crèches, écoles et établissements éducatifs) par la rénovation et l’installation de climatiseurs"
EC_SOBRIETE = "comme la limitation de l’étalement urbain, la baisse du trafic aérien, le report modal vers les transports en commun"
TONDELIER = [
    ("q001", -2, ec(159), "Convoquer un processus constituant transparent, participatif, pluraliste et indépendant pour abolir la monarchie présidentielle"),
    ("q002", 2, ec(159), "Convoquer un processus constituant transparent, participatif, pluraliste et indépendant pour abolir la monarchie présidentielle"),
    ("q003", 2, ec(160), "Renforcer le pouvoir législatif bicaméral et démocratique."),
    ("q004", 2, ec(162), "Instaurer la proportionnelle intégrale sans prime majoritaire aux élections législatives"),
    ("q005", 2, ec(163), "Ouvrir le droit de vote à 16 ans avec une formation civique."),
    ("q007", 2, ec(161), "Renforcer la démocratie directe par la mise en œuvre du Référendum d’Initiative Citoyenne (RIC) propositionnel ou abrogatif"),
    ("q008", 2, ec(163), "Limiter le cumul des mandats dans le temps (trois par type de mandat)."),
    ("q010", 2, ec(7), "Nous ferons de la lutte contre la corruption une priorité"),
    ("q013", 2, ec(68), "Créer une nouvelle tranche à 60 % au-delà de 250 000€ annuels."),
    ("q014", 2, ec(66), "Rétablir l’Impôt sur la Fortune (ISF) en lui ajoutant une composante climatique"),
    ("q015", 1, ec(55), "un ajustement à la baisse du taux réduit de l’impôt sur les sociétés et de la taxe sur les salaires"),  # for small firms
    ("q017", 2, ec(55), "Passer le salaire minimum à 2000€ brut par mois dès 2027."),
    ("q018", 2, ec(68), "Diminuer l’impôt sur le revenu pour les plus tranches les plus basses."),  # sic
    ("q019", 1, ec(57), "Passer aux 32 heures sans perte de salaire dans les métiers pénibles ou de nuit"),
    ("q020", -2, ec(57), "Abroger les dispositions régressives des lois travail (loi El Khomri, ordonnances Macron…)"),
    ("q021", 1, ec(77), "Créer un fonds souverain assis sur un « livret industrie »"),
    ("q024", 1, ec(64), "Exclure immédiatement les investissements liés à la transition écologique"),  # from the deficit rule
    ("q027", 1, ec(25), "Renationaliser progressivement les autoroutes afin d’investir dans les infrastructures de transport"),
    ("q028", -2, ec(116), "Abroger l’âge légal de départ à la retraite à 64 ans (réforme Borne) pour revenir immédiatement à un âge minimum à 62 ans"),
    ("q029", 2, ec(116), "Abroger l’âge légal de départ à la retraite à 64 ans (réforme Borne) pour revenir immédiatement à un âge minimum à 62 ans"),
    ("q030", 2, ec(117), "Réintroduire les 4 critères ouvrant le droit à une retraite anticipée qui ont été supprimés en 2017"),
    ("q031", -2, ec(117), "Refuser toute forme d’évolution vers une retraite par capitalisation en particulier la retraite à points."),
    ("q032", 2, ec(111), "Garantir un remboursement total des soins essentiels"),
    ("q035", -2, ec(58), "Abroger les réformes régressives adoptées lors des deux derniers quinquennats"),  # of unemployment insurance
    ("q036", 2, ec(124), "Instaurer l’égalité des congés de parentalité afin d’égaliser la prise en charge du travail domestique."),
    ("q037", 2, ec(119), "Créer une garantie d’autonomie qui respecte la dignité et les droits des personnes allocataires en remplacement du Revenu de Solidarité Active (RSA)."),
    ("q039", 1, ec(20), "Abroger la loi Kasbarian qui criminalise les locataires."),
    ("q040", -2, ec(177), "Nous devons changer de logique : rompre avec les politiques de peur et de fermeture"),
    ("q042", 2, ec(178), "Automatiser le droit au travail dès la délivrance de l’attestation de demande d’asile sans délai et sans autorisation de travail."),
    ("q043", -1, ec(178), "En finir avec la rétention administrative, coûteuse et indigne."),
    ("q046", 2, ec(178), "Régulariser les travailleur·ses, les étudiant·es et les parents d’enfants scolarisés sur la base de critères objectifs"),
    ("q054", 2, ec(130), "Instaurer un droit à mourir dans la dignité par l’adoption des deux lois sur la fin de vie."),
    ("q055", 2, ec(172), "La laïcité implique que les institutions républicaines et religieuses soient séparées."),
    ("q058", -2, ec(172), "La laïcité impose la neutralité au service public et à ses agent·es, pas à ses usagers ni aux habitant·es."),
    ("q059", 2, ec(146), "Créer un Observatoire des discriminations en capacité de financer la recherche sur les différentes formes de racisme, l’antisémitisme et l’islamophobie"),
    ("q061", 2, ec(140), "Mettre en œuvre un plan d’éradication des violences et des discriminations à l’encontre des personnes LGBTQIA+."),
    ("q062", 2, ec(138), "Garantir l’égal accès, la gratuité et l’effectivité du droit à la contraception et à l’interruption volontaire de grossesse (IVG)"),
    ("q065", 2, ec(145), "Racisme, islamophobie, antisémitisme, antitsiganisme et toutes les formes de haine et de discriminations constituent des crimes qui fragilisent durablement la cohésion sociale."),
    ("q067", 2, ec(188), EC_FEDERALE),
    ("q068", 2, ec(188), EC_FEDERALE),
    ("q069", -1, ec(188), EC_FEDERALE),
    ("q070", 2, ec(189), "seule une Europe fédérale puissante peut défendre ses valeurs démocratiques, écologiques et solidaires"),
    ("q071", 2, ec(190), "une majorité qualifiée en matière de protection des droits fondamentaux, de protection sociale et d’intégration fiscale européenne et la politique étrangère et de sécurité commune"),
    ("q072", 1, ec(190), "Augmenter les moyens budgétaires de l’Union Européenne pour atteindre 2 % du PIB européen en 2035 et 5 % du PIB en 2050."),
    ("q073", -2, ec(179), "Démanteler l’agence Frontex et créer une agence en charge de la protection des droits fondamentaux des personnes migrantes"),
    ("q076", 2, ec(195), "Créer un commandement militaire intégré européen sous la tutelle du Conseil de l’Union Européenne sans capacité de mobiliser directement les armées nationales"),
    ("q077", 2, ec(196), "notre pays doit se tenir résolument en soutien de l’Ukraine, en proie avant d’autres à l’impérialisme militarisé russe."),
    ("q078", 2, ec(205), "Retrouver une trajectoire correspondant à nos engagements internationaux (0,7 % du PNB)"),
    ("q086", -2, ec(202), "Adopter un embargo sur les livraisons d’armes et les matériels à double emploi"),  # to Israel
    ("q087", 2, ec(201), "dans la perspective d’une solution à deux États"),
    ("q088", -2, ec(17), "Planifier la sortie du nucléaire."),
    ("q089", 2, ec(16), "pour que la part des ENR atteigne 44 % de la consommation finale brute d’électricité en 2030"),
    ("q090", 1, ec(16), "Mieux informer la population et les entreprises du calendrier de sortie des énergies fossiles."),
    ("q091", 1, ec(15), "doivent conserver leur qualité de vie par un bouclier climat qui les préserve des augmentations des prix"),
    ("q093", 1, ec(108), "Améliorer la qualité de l’air en modifiant les conditions des ZFE (Zones à Faibles Émissions). Développer les Zones à Trafic Limité."),
    ("q094", 2, ec(23), "Créer une offre de location sociale (leasing social) d’un million de véhicules sur le quinquennat en favorisant les véhicules européens."),
    ("q095", 2, ec(27), "Doter de 7 milliards d’euros par an d'ici 2032 le Plan national d’adaptation au changement climatique pour affronter les risques climatiques"),
    ("q097", 2, ec(29), "Interdire immédiatement les pesticides cancérigènes, mutagènes, toxiques (CMR)"),
    ("q098", 2, ec(27), EC_CLIM),
    ("q100", 2, ec(66), "Diminuer les niches fiscales fossiles en transformant les taux réduits sur les produits fossiles en aides forfaitaires"),
    ("q102", 1, ec(92), "Accélérer la rénovation et la végétalisation des écoles (bâtiments et cours) en soutenant financièrement les collectivités locales avec le Fonds Vert."),
    ("q103", 2, ec(90), "Réhabiliter les métiers de l’Education nationale en augmentant les salaires des enseignant·es de 15 % en 5 ans."),
    ("q104", 1, ec(91), "Valoriser les lycées professionnels et techniques en rétablissant le baccalauréat professionnel en 4 ans"),
    ("q105", 1, ec(92), "Développer la liberté pédagogique."),
    ("q107", 2, ec(90), "Faire de l’école primaire une priorité absolue en réduisant la taille des classes à 19 élèves en 2032"),
    ("q108", 2, ec(27), EC_CLIM),
    ("q113", 2, ec(93), "Réhabiliter le droit à des études supérieures en remplaçant ParcourSup et MonMaster par une vraie plateforme d’orientation"),
    ("q115", 2, ec(92), "Réviser la loi Debré de 1959 pour diminuer la part de financement public à 50 %"),
    ("q117", 1, ec(164), "Créer une police nationale de proximité visant à rétablir un lien quotidien et permanent avec la population"),
    ("q118", -1, ec(165), "Encadrer la vidéosurveillance et renforcer la présence humaine."),
    ("q123", -2, ec(184), "Légaliser et encadrer la production, la vente et la consommation de cannabis."),
    ("q125", 2, ec(170), "L’objectif ultime doit rester la réinsertion des personnes condamnées y compris si c’est à long terme."),
    ("q128", -2, ec(165), "Interdire les lanceurs de balles de défense (LBD40) et les grenades mutilantes."),
    ("q133", 1, ec(88), "Réformer la fiscalité locale afin de pouvoir financer de manière autonome de véritables politiques économiques, foncières, culturelles et écologiques."),
    ("q135", 2, ec(20), "Renforcer les obligations et le contrôle des plateformes de location telles que Airbnb."),
    ("q136", 1, ec(15), EC_SOBRIETE),
    ("q137", 2, ec(161), "Développer des budgets participatifs sur le fonctionnement des collectivités territoriales."),
    ("q139", 2, ec(20), "Renforcer les sanctions financières et préfectorales en cas de manquement à l’obligation d’atteindre 20 ou 25 % de logements sociaux"),
    ("q140", 2, ec(15), EC_SOBRIETE),
    ("q141", 1, ec(25), "développement des pistes et voies cyclables"),
]

# François Ruffin (Debout!) ---------------------------------------------------------
# His campaign booklets ("cahiers de campagne") on nouspresident.fr, his movement's
# founding manifesto, his op-ed on Europe in Le Grand Continent, and press reports.
NP = "https://nouspresident.fr/wp-content/uploads/"


def cahier(path, n, title, date, p):
    return src(f"Cahier de campagne n° {n} de François Ruffin, « {title} », p. {p}", f"{NP}{path}#page={p}", date)


def travaillisme(p):
    return cahier("2026/09/Livret-Campagne-5-Travaillisme-Ecologique-VDEF.pdf", 5, "Face au chantier du siècle : pour un travaillisme écologique", "2026-09-09", p)


def logement(p):
    return cahier("2026/09/CC_Logement.pdf", 6, "Face à la crise du logement : faire sauter le verrou", "2026-09-24", p)


def probite(p):
    return cahier("2026/07/Debout-Livret-Probite-Web-1.pdf", 2, "Pour une loi de séparation de l’argent et de l’État", "2026-07-02", p)


RF_MANIFESTE = src("Manifeste fondateur de Debout!, le mouvement de François Ruffin", "https://debout.fr/notre-manifeste/", "2026-04-10")
RF_EUROPE = src("Le Grand Continent : « Pour une déclaration d’indépendance », tribune de François Ruffin sur l’Europe", "https://legrandcontinent.eu/fr/2026/02/25/pour-une-declaration-dindependance-la-doctrine-ruffin-sur-leurope/", "2026-02-25")
RF_ETAU = "desserrer l’étau, s’éloigner des États-Unis, se protéger de la Russie et de la Chine"
RUFFIN = [
    ("q002", 1, probite(53), "Pour mettre fin au pouvoir exorbitant de nominations du Président de la République, nous proposons de revoir l’article 13 de la Constitution"),
    ("q007", 2, travaillisme(28), "Les idées de référendum devront aussi et surtout venir des citoyens, avec le Référendum d’initiative citoyenne (RIC), enfin."),
    ("q010", 2, probite(44), "ENCADRER STRICTEMENT LE PANTOUFLAGE ET INTERDIRE LE RÉTRO-PANTOUFLAGE."),
    ("q017", 2, src("Orange Actu (6medias) : François Ruffin lance sa campagne en se posant en défenseur des travailleurs essentiels", "https://actu.orange.fr/france/presidentielle-2027-francois-ruffin-lance-sa-campagne-en-se-posant-en-defenseur-des-travailleurs-essentiels-magic-CNT000002oTqjw.html", "2026-04-26"),
     None),  # a SMIC of 1,700 euros net a month (news summary)
    ("q026", 1, cahier("2026/10/Debout-Livret-Campagne-Agriculture-vWeb.pdf", 4, "Pour une exception agriculturelle française", "2026-10-07", 36),
     "GÉNÉRALISER LES PAIEMENTS POUR SERVICES ENVIRONNEMENTAUX"),
    ("q027", 1, travaillisme(40), "nous reviendrons progressivement à un modèle 100 % public de production"),  # electricity
    ("q028", -2, RF_MANIFESTE, "Le premier pas, ce sont des impôts justes et l’abrogation de la retraite à 64 ans."),
    ("q029", 1, RF_MANIFESTE, "Le premier pas, ce sont des impôts justes et l’abrogation de la retraite à 64 ans."),
    ("q030", 2, cahier("2026/04/Debout-Livret-Campagne_Web.pdf", 1, "Pour un statut des travailleuses et travailleurs essentiels", "2026-04-13", 20),
     "GARANTIR UN DROIT À LA RETRAITE ANTICIPÉE POUR COMPENSER LA PÉNIBILITÉ."),
    ("q039", 1, logement(37), "il est urgent d’abroger la loi « Kasbarian-Bergé » qui a fait exploser le nombre d’expulsions"),
    ("q041", -2, RF_MANIFESTE, "Nous sommes opposés à la volonté du patronat de filières d’immigration pour trouver une main d’œuvre manquante."),
    ("q046", 2, RF_MANIFESTE, "Tous les travailleurs et travailleuses sur notre territoire doivent être régularisés pour ne plus vivre dans la peur du lendemain."),
    ("q049", 1, RF_EUROPE, "les binationaux, les diasporas africaine, marocaine, algérienne, vietnamienne, chinoise, ne doivent plus être traités avec soupçon mais au contraire vues comme une chance"),
    ("q055", 2, RF_MANIFESTE, "la République et sa laïcité –la loi de 1905, toute la loi de 1905, rien que la loi de 1905"),
    ("q068", -2, RF_EUROPE, "La Commission dispose déjà d’assez de « compétences »"),
    ("q071", -2, RF_EUROPE, "La France doit s’y opposer avec fermeté : la diplomatie et la défense relèvent des États et doivent le rester."),
    ("q076", 2, RF_EUROPE, "Et oui, dès aujourd’hui, il nous faut renforcer cette industrie de défense et le faire avec nos voisins européens."),
    ("q078", 2, RF_EUROPE, "Que nous compensions, en partie au moins, les coupes effectuées par Donald Trump dans les budgets d’aide au développement américains."),
    ("q081", -1, RF_EUROPE, RF_ETAU),
    ("q082", -2, RF_EUROPE, RF_ETAU),
    ("q083", -2, RF_EUROPE, RF_ETAU),
    ("q085", 2, RF_MANIFESTE, "quand l’Irlande reconnaît la Palestine comme État, c’est un point d’appui ici, pour nous."),
    ("q086", -2, RF_MANIFESTE, "condamnant l’invasion russe en Ukraine, et avec la même force, avec les mêmes sanctions, le génocide à Gaza, les colonies en Cisjordanie"),
    ("q088", 1, travaillisme(40), "En matière de production nucléaire, nous prolongerons la durée de vie des centrales existantes"),
    ("q089", 1, travaillisme(40), "Cela permettra un développement des projets d’énergie renouvelable planifié entre EDF et les collectivités locales"),
    ("q090", 1, travaillisme(10), "remplacer les chaudières fossiles par des pompes à chaleur, passer à la voiture ou au vélo électrique, ce n’est pas seulement bon pour le climat"),
    ("q092", 1, travaillisme(36), "développer l’utilisation des lignes de train du quotidien, en faisant rouler davantage de trains sur l’infrastructure existante"),
    ("q094", 2, travaillisme(36), "Nous équiperons ainsi 3 millions d’automobilistes des classes moyennes et populaires au cours du quinquennat"),  # in social leasing
    ("q095", 1, src("Plan d’action « Urgence climat » de la campagne de François Ruffin, p. 4", f"{NP}2026/10/PA_Urgence_Climat_VF.pdf.pdf#page=4", "2026-10-12"),
     "DES MOYENS À LA HAUTEUR POUR LES POMPIERS ET LA SÉCURITÉ CIVILE."),
    ("q102", 2, travaillisme(63), "L’organisation de grands chantiers, ainsi que de travaux participatifs à l’échelle des quartiers, en matière de végétalisation et d’ombrage des espaces publics"),
    ("q135", 2, logement(34), "les obligations pesant sur les locations ordinaires (ex. interdiction de location des passoires énergétiques) devraient être identiques pour les meublés touristiques"),
    ("q139", 2, logement(40), "PRODUIRE 200 000 NOUVEAUX LOGEMENTS « PUBLICS »"),
    ("q140", 1, logement(49), "la réduction de l’artificialisation des sols devra également passer par un meilleur encadrement des implantations d’espaces commerciaux, de plateformes logistiques ou encore de data centers"),
    ("q144", 1, travaillisme(17), "assurer des niveaux de financement suffisants pour les services publics de gestion des déchets"),
]

# Fabien Roussel (PCF) --------------------------------------------------------------
# The PCF's 40th congress issue of CommunisteS (his closing speech and the texts the
# congress adopted), the party's "cahiers thématiques des jours heureux" and his
# campaign documents, plus press reports.
PCF = "https://assets.nationbuilder.com/pcf/pages/"


def congres(p):
    return src(f"PCF, CommunisteS n° 1095, 40e congrès (discours de clôture de Fabien Roussel et textes adoptés), p. {p}",
               f"{PCF}42499/attachments/original/1784128307/document_1095_CommunisteS_40e_Congre%CC%80s.pdf#page={p}", "2026-07-15")


def jours_heureux(path, theme, date, p):
    return src(f"PCF, « Les cahiers thématiques des jours heureux » : {theme}, p. {p}", f"{PCF}{path}#page={p}", date)


def secu(p):
    return jours_heureux("36196/attachments/original/1766073347/document_-_cahier_se%CC%81cu_v2.pdf", "Sécurité sociale", "2025-12-18", p)


def mobilite(p):
    return jours_heureux("36198/attachments/original/1766073432/document_-_cahier_mobilite_ppp.pdf", "Mobilité", "2025-12-18", p)


def paix(p):
    return jours_heureux("41211/attachments/original/1779954906/document_cahier_paix_ppp_stc.pdf", "Paix & défense nationale", "2026-05-28", p)


PCF_RETENTION = "Les communistes s’opposent à toutes réglementations visant à expulser et à enfermer des migrants dans des centres de rétention quels qu’ils soient"
PCF_ECOLE = "il propose d’augmenter le temps scolaire et de baisser les effectifs par classe"
ROUSSEL = [
    ("q001", -1, congres(35), "Il est temps d’ouvrir le chantier d’une nouvelle République."),
    ("q002", 2, congres(35), "Rompre avec le présidentialisme signifie refonder l’État"),
    ("q003", 1, congres(35), "Le Parlement, pourtant dépositaire de la souveraineté nationale, est trop souvent réduit à entériner les choix de l’exécutif"),
    ("q004", 2, congres(35), "L’instauration d’une proportionnelle réelle, assurant à tous les courants une représentation correspondant à leur influence électorale, est indispensable"),
    ("q007", 2, congres(35), "référendum d’initiative citoyenne encadré et droit de pétition effectif"),
    ("q014", 2, congres(42), "il revendique l’imposition des grosses fortunes, la suppression des exonérations fiscales dont bénéficient les grandes entreprises, la taxation des profits"),
    ("q020", -2, congres(45), "Dans l’immédiat, l’urgence est à un moratoire sur les licenciements et les fermetures de sites."),
    ("q022", -2, congres(5), "avec leur obsession de la réduction sans fin de la dépense publique au nom d’une dette qu’ils ont eux-mêmes créée"),
    ("q025", 2, congres(6), "Nous nous battrons contre l’évasion fiscale et les délinquants en col blanc."),
    ("q027", 2, congres(9), "Et nous continuerons de défendre la nationalisation de Total qui profite de la guerre pour nous faire les poches."),
    ("q028", -2, secu(21), "La retraite à 60 ans, c’est possible et juste !"),
    ("q029", 2, secu(21), "La retraite à 60 ans, c’est possible et juste !"),
    ("q031", -2, secu(19), "La capitalisation « système cannibale »"),
    ("q032", 2, secu(15), "L’urgence d’aller vers le remboursement à 100% par la Sécurité sociale des soins prescrits"),
    ("q036", 2, secu(26), "La mise en place d’un véritable service public gratuit de la petite enfance est une nécessité"),
    ("q037", 1, jours_heureux("36199/attachments/original/1766073478/document_-_cahier_handicap_ppp.pdf", "Handicap", "2025-12-18", 9),
     "Remplacer l’AAH par un revenu au niveau du SMIC revalorisé, pour les personnes handicapées ne pouvant pas ou peu travailler."),
    ("q039", 2, jours_heureux("36197/attachments/original/1766073372/document_-_cahier_logement_ppp.pdf", "Logement", "2025-12-18", 35), "Pas d’expulsion sans contrepartie"),
    ("q042", 1, congres(39), "Ils refusent la stigmatisation de l’immigration au nom de l’insécurité, la remise en cause du droit du sol et du droit d’asile."),
    ("q043", -2, congres(39), PCF_RETENTION),
    ("q046", 2, congres(39), "la régularisation des travailleuses et travailleurs sans papiers comme des familles dont les enfants sont scolarisés sur le sol français"),
    ("q055", 2, congres(37), "Les communistes réaffirment que la laïcité est un principe non négociable, indispensable à l’émancipation des femmes et à l’égalité."),
    ("q061", 2, congres(38), "Face aux violences, aux discriminations et aux discours réactionnaires, le PCF exige l’égalité pleine et entière"),
    ("q065", 2, congres(38), "Les citoyennes et citoyens de religion ou de culture musulmane subissent aujourd’hui des discours et des actes racistes intolérables"),
    ("q073", -1, congres(39), "Ils dénoncent l’opacité des moyens alloués à l’agence Frontex et exigent qu’une enquête soit faite"),
    ("q074", -2, src("LCP : à la Fête de l’Huma, Fabien Roussel au défi de prouver l’utilité d’une candidature communiste", "https://lcp.fr/actualites/presidentielle-a-la-fete-de-l-huma-fabien-roussel-au-defi-de-prouver-l-utilite-d-une", "2026-09-11"),
     "réorienter l'argent du ministère de la guerre vers les services publics"),
    ("q075", -2, paix(41), "La France, en tant que signataire du TNP, doit agir pour relancer l’activité diplomatique pour l’élimination des armes nucléaires"),
    ("q076", -1, congres(31), "aux projets d’une armée européenne ou de mutualisation des moyens sous commandement de l’OTAN"),  # which the PCF opposes
    ("q085", 2, paix(40), "l’établissement d’un État de Palestine d’un seul tenant sur la base des frontières de 1967"),
    ("q086", -2, paix(40), "pas une arme, pas une balle, pas une technologie, pas une puce électronique ne doit être livrée à Israël"),
    ("q087", 2, paix(40), "La solution à deux États est la seule qui puisse permettre une paix juste et durable"),
    ("q088", 2, congres(47), "Il est possible d’y parvenir par une production massive d’électricité grâce à un mix décarboné alliant nucléaire et renouvelables"),
    ("q089", 1, congres(47), "Il est possible d’y parvenir par une production massive d’électricité grâce à un mix décarboné alliant nucléaire et renouvelables"),
    ("q090", 1, congres(47), "Le PCF défend l’objectif de s’affranchir à terme des combustibles fossiles afin d’atteindre la neutralité carbone en 2050"),
    ("q091", 1, congres(9), "Nous continuerons de défendre la baisse de 30 % des tarifs de l’électricité et du gaz pour les ménages et les entreprises."),
    ("q092", 2, mobilite(11), "10 milliards d’euros par an pendant 20 ans pour un plan d’investissements dans les infrastructures"),
    ("q093", -1, mobilite(12), "la mise en place des ZFE, qui sont bien souvent injustes socialement"),
    ("q094", 2, mobilite(17), "Nous proposons un dispositif de prêt à taux zéro ouvert à une large partie des ménages pour se doter d’un véhicule électrique."),
    ("q095", 1, src("PCF, tract de campagne de Fabien Roussel « Des moyens pour nos pompiers », p. 2", f"{PCF}44583/attachments/original/1791210341/tract_pompier.pdf#page=2", "2026-10-05"),
     "porter à 5000 le nombre de camions de lutte contre les feux de forêts"),
    ("q103", 1, src("Plan « Jeunesse 2027-2032 » de Fabien Roussel, p. 6", f"{PCF}44609/attachments/original/1791282014/Plan_Jeunesse_2027-2032.pdf#page=6", "2026-10-06"),
     "Recruter 90 000 enseignants en cinq ans"),
    ("q104", 1, congres(50), "le PCF veut le renforcement du service public de l’Éducation nationale, de la formation professionnelle, de la formation initiale et continue"),
    ("q107", 2, congres(50), PCF_ECOLE),
    ("q112", -2, congres(50), PCF_ECOLE),
    ("q113", 2, src("Plan « Jeunesse 2027-2032 » de Fabien Roussel, p. 8", f"{PCF}44609/attachments/original/1791282014/Plan_Jeunesse_2027-2032.pdf#page=8", "2026-10-06"),
     "Parcoursup et MonMaster seront supprimés et la sélection à l'entrée de l'université prendra fin."),
    ("q115", 2, congres(50), "Nous portons la fin du financement public des écoles privées sous contrat."),
    ("q125", 1, congres(36), "Il est nécessaire de construire des alternatives à un système carcéral aujourd’hui marqué par l’inhumanité et l’inefficacité."),
    ("q128", -1, congres(33), "la brutale répression du mouvement des Gilets jaunes et les stratégies policières provocatrices mises en œuvre contre les manifestations du mouvement social"),
    ("q134", 2, mobilite(9), "La gratuité des transports en commun est loin d’être une utopie."),
    ("q139", 2, jours_heureux("36197/attachments/original/1766073372/document_-_cahier_logement_ppp.pdf", "Logement", "2025-12-18", 13),
     "Nous proposons de créer les conditions qui nous permettront de construire 200 000 logements publics par an et ce pendant 5 ans"),
    ("q140", 1, congres(46), "À ce titre, les communistes combattent l’artificialisation des sols."),
    ("q141", 2, mobilite(19), "Construire 100 000 km de pistes cyclables pour atteindre une part modale du vélo de 15% en 2030"),
    ("q142", -1, congres(36), "La police municipale ne doit pas devenir le supplétif de la police nationale."),
]

# Nicolas Dupont-Aignan (Debout la France) ----------------------------------------
# His party's program pages on debout-la-france.fr and his campaign site.
DLF = "https://www.debout-la-france.fr/projet/"


def dlf(slug, theme, date):
    return src(f"Projet de Debout la France : {theme}", f"{DLF}{slug}/", date)


DLF_ECO = dlf("economie-travail", "Économie", "2026-10-10")
DLF_LOGEMENT = dlf("logement", "Logement", "2026-09-30")
DLF_IMMIGRATION = dlf("immigration-et-assimilation", "Immigration et assimilation", "2026-03-03")
DLF_JUSTICE = dlf("justice", "Justice", "2026-10-12")
DLF_FAMILLE = dlf("famille", "Famille", "2026-06-09")
DLF_ECOLE = dlf("instruction-publique", "Éducation (instruction publique)", "2026-10-12")
NDA_RENTREE = src("Discours de rentrée de Nicolas Dupont-Aignan « Libérons la France ! » (dupontaignan.fr)", "https://www.dupontaignan.fr/actualite/liberons-la-france-%c2%b7-discours-de-rentree-de-nicolas-dupont-aignan/", "2026-09-19")
DUPONT_AIGNAN = [
    ("q007", 2, dlf("refonder-et-moraliser-notre-democratie", "Refonder et moraliser notre démocratie", "2026-06-09"),
     "Instaurer le référendum d’initiative citoyenne constituant (RIC) pour rendre les citoyens acteurs de l’élaboration des lois et maîtres de leur Constitution."),
    ("q010", 2, NDA_RENTREE, "doit s’accompagner d’une lutte impitoyable contre la corruption qui gangrène notre nation"),
    ("q012", 2, DLF_ECO, "Supprimer le millefeuille administratif et les agences d’État inutiles."),
    ("q016", 1, DLF_ECO, "division par 2 de l’IS pour les bénéfices réinvestis en France"),
    ("q026", 1, dlf("agriculture", "Agriculture", "2026-02-16"), "Supprimer les cotisations sociales agricoles qui pèsent sur nos exploitations afin de rendre nos productions plus compétitives"),
    ("q027", 1, dlf("transport-automobilistes", "Automobilistes et motards", "2026-10-15"),
     "Renationaliser les autoroutes (qui réalisent des bénéfices de l’ordre de 4 milliards d’euros par an)"),
    # Written in February 2024, when the "current level" was the 2023 reform's.
    ("q028", 1, dlf("retraites", "Retraites", "2024-02-05"), "Maintenir l’âge minimum de départ à la retraite et la durée de cotisations aux niveaux actuels."),
    ("q030", 1, dlf("retraites", "Retraites", "2024-02-05"),
     "Mieux prendre en compte la pénibilité du travail pour tous les travailleurs du privé et du public ainsi que les situations de handicap."),
    ("q031", 1, NDA_RENTREE, "Il propose également 10 000 € à chaque naissance, placés dans un fonds souverain"),
    ("q033", 2, dlf("equilibre-territoire-monde-rural", "Équilibre du territoire", "2026-02-16"),
     "Faire en sorte que chaque français dispose d’un hôpital à moins de 45 minutes en voiture, doté d’un service d’urgence, d’un scanner et d’un IRM."),
    ("q036", 2, DLF_FAMILLE, "Lancer un plan national de création de 100 000 places de crèches en 5 ans."),
    ("q040", 1, DLF_IMMIGRATION, "Limiter strictement le regroupement familial et supprimer le régime d’exception accordé aux Algériens"),
    ("q042", -2, DLF_IMMIGRATION, "le droit d’asile n’est accordé qu’en cas de menace individuelle, et mettre fin à la jurisprudence de la CNDA qui étend sans fondement ce droit"),
    ("q044", 2, DLF_IMMIGRATION, "Renforçant l’assimilation via la maîtrise de la langue, l’adhésion aux valeurs de la République et un service civique obligatoire de 3 mois"),  # to naturalize
    ("q045", -2, DLF_IMMIGRATION, "Exigeant 10 ans de résidence en France comme minimum pour évaluer l’assimilation réelle."),
    ("q046", -2, DLF_IMMIGRATION, "supprimer la régularisation pour les étrangers en situation irrégulière"),
    ("q048", 2, DLF_IMMIGRATION, "nous affirmons que notre pays doit rétablir ses frontières"),
    ("q050", 2, DLF_IMMIGRATION, "Tout étranger condamné à une prison ferme sera expulsé dès sa sortie, avec retrait définitif de son titre de séjour"),
    ("q056", 2, DLF_IMMIGRATION, "Interdire tous les signes religieux visibles dans le service public, notamment dans les universités et les hôpitaux, et refuser tout accommodement."),
    ("q060", 2, dlf("culture-patrimoine", "Culture et patrimoine", "2024-02-05"),
     "Rétablir les crédits d’entretien et de restauration du patrimoine amputés ces dernières années et consacrer 400 M d’€ par an"),
    ("q066", 1, DLF_IMMIGRATION, "l’État doit fixer des règles claires définissant la place de l’islam comme religion respectant les principes républicains"),
    ("q067", -2, NDA_RENTREE, "Sortir de l’Union européenne pour rendre à la France son indépendance"),
    ("q069", 2, dlf("affaires-europeennes", "Affaires européennes", "2026-10-05"),
     "Nous rétablirons la primauté du droit national sur le droit européen afin de ne plus subir la dérive supranationale."),
    ("q072", -2, dlf("affaires-europeennes", "Affaires européennes", "2026-10-05"),
     "Supprimer la contribution nette de la France et la réattribuer à des secteurs clés de notre pays"),
    ("q074", 2, dlf("defense", "Défense nationale", "2026-10-08"),
     "nous nous engageons à augmenter notre budget de défense pour atteindre le chiffre raisonnable de 2,5% du PIB"),
    ("q075", 2, dlf("defense", "Défense nationale", "2026-10-08"),
     "Sacraliser le territoire français et protéger notre peuple en renforçant notre dissuasion nucléaire"),
    ("q077", -2, NDA_RENTREE, "dilapider des dizaines de milliards d’euros pour leur Union européenne, leur copain Zelensky"),
    ("q079", 1, DLF_FAMILLE, "Rétablir un service national d’une durée de trois mois, incluant le passage du permis de conduire financé par l’État"),
    ("q082", 1, DLF_ECO, "nous réautoriserons les importations de gaz russe parce qu’il est bon marché"),
    ("q083", -1, dlf("affaires-etrangeres", "Affaires étrangères", None),
     "la France s’est égarée en se soumettant à une ligne unique, inspirée par les États-Unis"),
    ("q088", 2, DLF_ECO, "l’électricité est l’avenir de l’énergie et le nucléaire est l’avenir de l’électricité"),
    ("q089", -2, DLF_ECO, "Supprimer les aides de l’État à l’installation des éoliennes et des panneaux solaires en annulant le décret sur la PPE3"),
    ("q093", -2, dlf("transport-automobilistes", "Automobilistes et motards", "2026-10-15"), "Acter la suppression définitive des zones à faibles émissions."),
    ("q099", -2, dlf("agriculture", "Agriculture", "2026-02-16"), "simplifiant les procédures (fin du pacte vert européen, des quotas de jachères, etc…)"),
    ("q101", -2, NDA_RENTREE, "Une Nouvelle taxe carbone qui fera exploser les prix de l’énergie."),
    ("q103", 2, DLF_ECOLE, "Augmenter de 15 % en 4 ans les salaires nets des professeurs."),
    ("q104", 2, DLF_FAMILLE, "Doper l’apprentissage en valorisant les filières professionnelles et en simplifiant l’accès aux entreprises."),
    ("q113", 2, DLF_ECOLE, "Réformer le système Parcoursup afin de le rendre équitable et transparent."),
    ("q114", 2, DLF_ECOLE, "Uniforme obligatoire, niveau de langage minimum et vouvoiement."),
    ("q117", 2, dlf("securite", "Sécurité", "2025-11-01"), "10 000 policiers et gendarmes supplémentaires nets en 5 ans."),
    ("q119", 2, DLF_JUSTICE, "Instaurer une peine de perpétuité réelle et non modifiable"),
    ("q120", 2, DLF_JUSTICE, "Réinstaurer et élargir les peines planchers pour toute agression contre policiers, gendarmes, pompiers, enseignants, soignants."),
    ("q121", 2, DLF_JUSTICE, "Abroger l’ordonnance de 1945 concernant la justice des mineurs. Baisser la majorité pénale à 16 ans."),
    ("q122", 1, src("Pétition « Pour un référendum sur la peine de mort pour les meurtriers d’enfants » (dupontaignan.fr)", "https://www.dupontaignan.fr/actualite/pour-un-referendum-sur-la-peine-de-mort-pour-les-meurtriers-d-enfants/", "2026-06-11"),
     "Je suis convaincu que la peine de mort pour les meurtriers d’enfants aura un effet dissuasif."),
    ("q133", 1, dlf("equilibre-territoire-monde-rural", "Équilibre du territoire", "2026-02-16"),
     "Revoir la fiscalité locale pour rétablir l’autonomie et la responsabilité financière des collectivités."),
    ("q135", 2, DLF_LOGEMENT, "Réguler les locations de tourisme type Airbnb en harmonisant l’abattement fiscal par rapport aux locations standards"),
    ("q140", -2, DLF_LOGEMENT, "Réformer intégralement la loi Climat et Résilience pour mettre fin à l’objectif de Zéro Artificialisation Nette (ZAN)"),
]

# Nathalie Arthaud (Lutte ouvrière) -------------------------------------------------
# Lutte ouvrière's campaign brochure, her meeting speech and the weekly editorials she signs.
LO = "https://lutte-ouvriere.org/portail/editoriaux/"
LO_BROCHURE = "https://www.lutte-ouvriere.org/medias/document/fichiers/2026/06/brochure-ete-2026.pdf"


def lo_edito(slug, title, date):
    return src(f"Éditorial de Nathalie Arthaud (Lutte ouvrière) : « {title} »", LO + slug, date)


def lo_brochure(p):
    return src(f"Lutte ouvrière, brochure « Nathalie Arthaud – Présidentielle 2027 », p. {p}", f"{LO_BROCHURE}#page={p}", "2026-06-26")


LO_FRONTIERES = "Régularisation de tous les sans-papiers, liberté de circulation et d’installation pour chaque être humain de cette planète !"
LO_MEETING = src("Meeting du 26 septembre 2026 : discours de Nathalie Arthaud (lutte-ouvriere.org)", "https://www.lutte-ouvriere.org/portail/brochures/meeting-26-septembre-2026-discours-nathalie-arthaud-197446.html", "2026-09-29")
LO_BESOINS = "les consacrer aux besoins de la population : aux hôpitaux qui manquent de soignants, aux écoles où les classes sont surchargées"
ARTHAUD = [
    ("q014", 1, LO_MEETING, "Mais la couverture n’est petite que parce que tous ces politiciens refusent d’aller chercher dans les profits et les grandes fortunes."),
    ("q017", 2, LO_MEETING, "Nous défendrons le SMIC à 2 200 € nets."),
    ("q019", 1, lo_brochure(12), "Il faut baisser le temps et la charge de travail sans perte de salaire pour permettre à tous de vivre."),
    ("q020", -2, lo_edito("interdiction-licenciements-sous-peine-requisition-184019.html", "Interdiction des licenciements sous peine de réquisition !", "2025-05-05"),
     "INTERDICTION DES LICENCIEMENTS SOUS PEINE DE RÉQUISITION !"),
    ("q023", 2, lo_edito("vive-mobilisation-lyceenne-faisons-naitre-travailleurs-mardi-6-octobre-mobilises-197642.html", "Vive la mobilisation lycéenne, et faisons naître celle des travailleurs ! Mardi 6 octobre, tous mobilisés !", "2026-10-04"),
     "Il faut les réquisitionner pour les consacrer aux salaires, à nos conditions de vie, à l’éducation, la santé et l’avenir de nos enfants !"),
    ("q027", 2, lo_brochure(14), "Expropriation sans indemnité ni rachat de leurs actionnaires en commençant par ceux de l’industrie pétrolière et des industries de guerre !"),
    ("q033", 2, LO_MEETING, LO_BESOINS),  # the confiscated profits
    ("q040", -2, lo_brochure(16), LO_FRONTIERES),
    ("q043", -2, lo_brochure(16), "À bas les barbelés, les traques, les expulsions !"),
    ("q046", 2, lo_brochure(16), LO_FRONTIERES),
    ("q048", -2, lo_brochure(16), LO_FRONTIERES),
    ("q064", -2, LO_MEETING, "Le nationalisme, même quand il n’est pas teinté de racisme crasse, est un poison !"),
    ("q073", -2, lo_brochure(16), "À bas l’Europe-forteresse !"),
    ("q074", -2, lo_edito("euro-larmee-homme-guerre-182538.html", "Pas un euro de plus pour l’armée ! Pas un homme pour la guerre !", "2025-03-10"), "Pas un euro de plus pour l'armée !"),
    ("q079", -2, lo_edito("galonnes-cherchent-chair-canon-188858.html", "Galonnés cherchent chair à canon !", "2025-12-01"),
     "Galonnés cherchent chair à canon !"),  # her editorial against bringing back military service
    ("q107", 1, LO_MEETING, LO_BESOINS),
]

# Xavier Bertrand (Nous France) -----------------------------------------------------
# Interviews and reports that his movement reproduces on nousfrance.fr (credited to the
# outlet). His words are quoted; a journalist's summary has no quote.
NF = "https://www.nousfrance.fr/"


def nf(path, outlet, title, date):
    return src(f"{outlet} : « {title} » (reproduit sur nousfrance.fr)", NF + path, date)


NF_OPINION = nf("2026/08/presidentielle-2027-xavier-bertrand-un-non-candidat-en-campagne-lopinion/", "L’Opinion", "Présidentielle 2027 : Xavier Bertrand, un non candidat en campagne", "2026-08-19")
NF_AFP = nf("2025/10/xavier-bertrand-se-presente-comme-le-candidat-des-classes-moyennes-contre-les-extremes-afp/", "AFP", "Xavier Bertrand se présente comme le candidat des classes moyennes, contre les extrêmes", "2025-10-25")
NF_LIBE = nf("2025/10/avant-la-presidentielle-xavier-bertrand-se-pose-en-opposant-dinteret-general-liberation/", "Libération", "Avant la présidentielle, Xavier Bertrand se pose en opposant d’intérêt général", "2025-10-25")
NF_PROVENCE = nf("2026/07/rencontres-economiques-daix-il-faut-une-republique-des-territoires-et-un-mandat-unique-pour-xavier-bertrand-la-provence/", "La Provence", "Il faut une République des territoires et un mandat unique", "2026-07-05")
NF_VARMATIN = nf("2026/08/je-my-prepare-pas-encore-officiellement-candidat-xavier-bertrand-pose-les-bases-de-son-projet-pour-la-presidentielle-avec-la-culture-en-toile-de-fond-var-matin/", "Var-Matin", "Je m’y prépare : Xavier Bertrand pose les bases de son projet pour la présidentielle", "2026-08-03")
BERTRAND = [
    ("q008", 1, NF_PROVENCE, "Il faut une République des territoires et un mandat unique"),  # a single presidential term
    ("q009", 2, NF_PROVENCE, "Je prône un changement de logiciel complet : la « République des territoires », ou ce que Jean-Louis Borloo appelle une « France fédérale »."),
    ("q011", 1, NF_LIBE, None),  # a "règle d'or budgétaire" to put to a referendum (news summary)
    ("q014", -2, nf("2025/10/que-letat-arrete-de-nous-faire-les-poches-a-saint-quentin-xavier-bertrand-sechauffe-pour-la-presidentielle-le-point/", "Le Point", "Que l’État arrête de nous faire les poches : à Saint-Quentin, Xavier Bertrand s’échauffe pour la présidentielle", "2025-10-26"),
     "Ce n’est plus de la justice fiscale, c’est une connerie fiscale"),  # on the Zucman wealth tax
    ("q018", 1, NF_AFP, None),  # lower income tax "pour les premières tranches" (news summary)
    ("q022", 2, NF_OPINION, None),  # cut public spending by 20 billion euros a year for five years (news summary)
    ("q028", -1, NF_OPINION, "Si on vit plus longtemps, il faut accepter de travailler plus longtemps, de repousser l’âge légal"),
    ("q029", -2, NF_OPINION, "Si on vit plus longtemps, il faut accepter de travailler plus longtemps, de repousser l’âge légal"),
    ("q031", 2, NF_OPINION, None),  # a compulsory funded tier ("étage de capitalisation obligatoire") (news summary)
    ("q040", 1, NF_AFP, None),  # "quotas migratoires" (news summary)
    ("q060", 1, NF_VARMATIN, "Si les Français me font confiance, en 2032, 1 % du budget de l’État sera consacré à la culture."),
    # The fuel-tax windfall paid back to those who must drive: energy-cost aid, but for fuel only.
    ("q091", 1, src("Nous France, « Hausse du carburant – La proposition de Xavier Bertrand »", NF + "2026/04/hausse-du-carburant-la-proposition-de-xavier-bertrand/", "2026-04-15"),
     "Il doit être redistribué aux artisans, aux infirmiers et aux salariés qui n’ont pas d’autre choix que de prendre leur voiture."),
    ("q095", 1, NF_VARMATIN, "Il est temps de mettre notre protection civile au niveau des nouveaux risques et des nouveaux incendies"),
    ("q097", -1, nf("2026/01/xavier-bertrand-on-ne-dirige-pas-un-pays-par-la-peur-le-parisien/", "Le Parisien", "Xavier Bertrand : On ne dirige pas un pays par la peur", "2026-01-10"),
     "Déjà, revenons sur les surtranspositions franco-françaises dès cette année."),
    ("q120", 1, NF_LIBE, None),  # "peines planchers", to put to a referendum (news summary)
    # Asked how to give the regions more power; the State would keep justice, security,
    # immigration control, defence and diplomacy. "Local", not "regional", so only "plutôt".
    ("q132", 1, NF_PROVENCE, "Pour tout le reste, la gestion de la vie quotidienne doit être locale."),
]

# Dominique de Villepin (La France humaniste) ----------------------------------------
# His movement's program ("Projet France 2027") and his speeches and op-eds on its site.
FH = "https://lafrancehumaniste.fr/"
FH_ECO = src("La France humaniste, « Projet économique : 20 propositions pour 2027 »", f"{FH}programme/economie.html")
FH_SORBONNE = src("« Le moment français », discours de Dominique de Villepin à la Sorbonne (lafrancehumaniste.fr)", f"{FH}articles/le-moment-francais-sorbonne.html", "2026-03-27")
FH_SOCIAL = src("« Vers une protection sociale rénovée », La France humaniste", f"{FH}articles/protection-sociale.html", "2025-12-04")
VILLEPIN = [
    ("q007", 2, FH_SORBONNE, "Nous avons besoin pour débloquer le pays d'un référendum d'initiative citoyenne, inscrit dans un processus législatif rigoureux, préparé par une convention citoyenne permanente."),
    ("q014", 2, FH_ECO, "Un impôt unique sur le patrimoine des 1 %"),  # from 2.2 million euros, steeply progressive
    # Tax rises and spending cuts together, so only "plutôt".
    ("q022", 1, src("« La dette c’est la défaite : choisir le sursaut », chronique de Dominique de Villepin (lafrancehumaniste.fr)", f"{FH}articles/la-dette-cest-la-defaite.html", "2026-08-21"),
     "il faudra des hausses d’impôt justes et des baisses de dépenses ciblées, à hauteur des besoins, c’est-à-dire pour plus de 120 Mds€ à l’horizon 2031"),
    ("q028", -1, FH_SORBONNE, "Il supprimerait l’âge légal et reposerait sur une règle de durée de cotisations, avec une prise en compte sérieuse de la pénibilité des métiers."),
    ("q030", 1, FH_SORBONNE, "Il supprimerait l’âge légal et reposerait sur une règle de durée de cotisations, avec une prise en compte sérieuse de la pénibilité des métiers."),
    ("q031", 1, FH_ECO, "Rendement garanti, avec un livret universel ouvert à la naissance, abondé par les droits de succession."),
    ("q032", 1, FH_SOCIAL, "Cette clarification doit être couplée à un bouclier sanitaire limitant le reste à charge annuel d’un ménage en fonction de son revenu."),
    ("q070", 1, src("« Le moment européen : manifeste pour une Europe souveraine », Dominique de Villepin (lafrancehumaniste.fr)", f"{FH}articles/moment-europeen-europe-souveraine.html", "2026-03-06"),
     "La clé, c’est à la fois davantage de ressources propres européennes et l’emprunt mutualisé à l’échelle de l’Union"),
    ("q086", -2, src("« Un génocide à Gaza », tribune de Dominique de Villepin dans Le Monde (reprise sur lafrancehumaniste.fr)", f"{FH}articles/un-genocide-a-gaza.html", "2025-07-31"),
     "en décrétant la suspension immédiate de l’accord d’association entre l’Union européenne et Israël, tant que les violations des droits humains persistent"),
    ("q088", 2, FH_ECO, "6 EPR2, éolien en mer industrialisé, électrification massive des usages, pour les ménages comme pour l’industrie."),
    ("q089", 1, FH_ECO, "6 EPR2, éolien en mer industrialisé, électrification massive des usages, pour les ménages comme pour l’industrie."),
    ("q094", 2, FH_ECO, "1 million de voitures électriques en leasing social, 1 million de pompes à chaleur, dividende climatique."),
    ("q097", 2, src("« Pour la souveraineté agricole et alimentaire », La France humaniste", f"{FH}articles/souverainete-agricole-et-alimentaire.html", "2026-02-25"),
     "Il faut réduire de moitié l’usage total des produits phytosanitaires d’ici 2030"),
    ("q101", 2, src("« Big Bang : la règle républicaine », La France humaniste", f"{FH}articles/big-bang-la-regle-republicaine.html", "2026-08-28"),
     "Un impôt de justice environnementale fusionnant l’ensemble des taxes existantes, autour du grand principe d’un prix unique du carbone incitant à la décarbonation"),
    ("q103", 1, src("« Refonder l’école pour refaire société », La France humaniste", f"{FH}articles/refonder-lecole-pour-refaire-societe.html", "2026-09-01"),
     "Cela permettra à l’horizon de 10 ans l’augmentation des dépenses réelles par élèves d’au moins 20%."),
    ("q133", 1, FH_ECO, "Une compétence, une collectivité, un impôt voté localement : les maires en première ligne de l’action publique."),
    ("q139", 1, FH_SOCIAL, "Le quota de logements sociaux doit être relevé dans les zones où les tensions sont les plus fortes"),
]

# Florian Philippot (Les Patriotes) -------------------------------------------------
# His party's program "Projet pour la France", 2026-2027 edition (PDF), page by page.
PATRIOTES = "https://les-patriotes.fr/wp-content/uploads/2026/09/Projet-pour-la-France-2026-v2.pdf"


def patriotes(p):
    return src(f"Les Patriotes, « Projet pour la France », édition 2026-2027, p. {p}", f"{PATRIOTES}#page={p}", "2026-09")


LP_SOUVERAINETE = "La France doit retrouver sa souveraineté nationale en quittant toutes les instances supranationales : UE, Euro, Schengen, CEDH, OTAN, OMS."
LP_REFORMES = "visant à raboter les indemnités chômage, à fermer des lits à l’hôpital ou à arrêter le remboursement des médicaments pourront être supprimées"
PHILIPPOT = [
    ("q007", 2, patriotes(2), "Créer le référendum d’initiative citoyenne (RIC) sur tout sujet et l’inscrire dans la Constitution."),
    ("q010", 2, patriotes(2), "Mise en place de l’inéligibilité à vie et interdiction de toute charge publique pour les élus et responsables publics condamnés définitivement pour corruption."),
    ("q015", 2, patriotes(3), "Soutenir les créateurs en France : artisans, TPE/PME, par une politique sociale et fiscale très avantageuse"),
    ("q021", 1, patriotes(3), "permettre à l’État investisseur de jouer pleinement son rôle d’impulsion à côté des entreprises commerciales"),
    ("q022", -2, patriotes(4), "Mettre un terme aux plans d’austérité."),
    ("q023", 1, patriotes(4), "Mettre un terme aux plans d’austérité."),
    ("q025", 1, patriotes(9), "lutter contre la fraude fiscale et sociale créera les conditions d’une économie dynamique mais juste"),
    ("q027", 2, patriotes(3), "Rétablir le monopole public national d’EDF."),
    # "Baisser l'âge de départ", without a figure: against keeping 64, "plutôt" for 62.
    ("q028", -2, patriotes(4), "Baisser l’âge de départ à la retraite."),
    ("q029", 1, patriotes(4), "Baisser l’âge de départ à la retraite."),
    ("q033", 1, patriotes(4), LP_REFORMES),  # reforms the program would undo
    ("q035", -1, patriotes(4), LP_REFORMES),
    ("q036", 1, patriotes(6), "Il faut créer davantage de places en crèches spécifiquement aménagées pour accueillir les tout-petits atteints de handicaps physiques, sensoriels ou cognitifs"),
    ("q040", 2, patriotes(10), "L’objectif est de mettre un terme à la politique d’immigration massive en revenant à des flux extrêmement limités"),
    ("q041", -2, patriotes(10), "Mettre fin à l’immigration de travail et à la directive européenne des travailleurs détachés."),
    ("q043", 2, patriotes(10), "Renvoyer les clandestins chez eux et appliquer les OQTF (Obligation de Quitter le Territoire)."),
    ("q048", 2, patriotes(10), "Pour retrouver la maîtrise de nos frontières nationales, il est impératif de quitter l’Union européenne et l’espace Schengen"),
    ("q050", 2, patriotes(11), "Construire les dizaines de milliers de places de prison qui manquent et expulser les prisonniers étrangers"),
    ("q053", 2, patriotes(10), "Les étrangers qui veulent vivre en France devront choisir une parfaite assimilation à notre pays ou partir."),
    ("q054", -1, patriotes(6), "Refuser toute politique d’incitation à l’euthanasie, assumée ou déguisée, des personnes en situation de handicap."),
    ("q055", 2, patriotes(7), "La laïcité, l’universalisme, l’assimilation doivent redevenir les piliers de l’école républicaine."),
    ("q067", -2, patriotes(2), LP_SOUVERAINETE),
    ("q068", -2, patriotes(2), LP_SOUVERAINETE),
    ("q069", 2, patriotes(2), LP_SOUVERAINETE),
    ("q070", -2, patriotes(2), LP_SOUVERAINETE),
    ("q072", -2, patriotes(8), "Économiser 20 milliards d’euros par an par le Frexit."),
    # Against EU borders because he wants national ones (Frexit), not looser borders.
    ("q073", -2, patriotes(10), "Dissoudre Frontex. L’agence européenne chargée du contrôle des frontières extérieures de l’UE, organise l’immigration clandestine bien plus qu’elle ne l’empêche."),
    ("q075", 1, patriotes(10), "Conserver notre dissuasion nucléaire."),
    ("q076", -1, patriotes(10), "Rejeter la création d’une armée européenne."),
    ("q077", -2, patriotes(8), "Couper les financements de la guerre en Ukraine, qui disparaissent dans la corruption."),
    ("q080", 2, patriotes(3), "La sortie de l’euro et l’instauration d’une nouvelle monnaie nationale est une condition absolue de notre bonne santé économique."),
    ("q082", 1, patriotes(10), "les sanctions contre la Russie, qui se sont retournées contre nous, notamment en alimentant l’inflation des prix de l’énergie"),
    ("q083", -1, patriotes(10), "la voix de la France est considérablement affaiblie, car de plus en plus assimilée à celle des Etats-Unis"),
    ("q088", 2, patriotes(3), "Investir massivement dans le nucléaire et choisir notre mix énergétique."),
    ("q089", -2, patriotes(3), "En finir avec les éoliennes sur terre et en mer."),
    ("q097", 1, patriotes(6), "La France doit accompagner la transition des exploitations agricoles vers la permaculture, les pratiques respectueuses des sols, et la production biologique."),
    ("q104", 2, patriotes(7), "La voie professionnelle doit être revalorisée, qualifiante et connectée aux besoins économiques réels du pays."),
    ("q117", 1, patriotes(11), "Recréer une police de proximité visible et permanente."),
    ("q120", 2, patriotes(11), "Il convient donc de réinstaurer les peines planchers et de généraliser les sanctions dès la première infraction."),
    ("q121", 1, patriotes(11), "La responsabilité doit primer et l’excuse de minorité ne doit s’appliquer qu’à la condition que le juge la motive spécialement."),
    ("q140", 2, patriotes(6), "Il est temps de sanctuariser les espaces naturels, de replanter les haies bocagères, de renforcer les réserves écologiques et d’interdire les pratiques destructrices."),
]

# François Asselineau (UPR) ---------------------------------------------------------
# The UPR has published no 2027 program yet; its site still presents his 2022
# presidential program as "notre programme", so that is the source, dated as such.
UPR22 = src("UPR, programme présidentiel de François Asselineau (2022, le plus récent publié par l’UPR)", "https://upr.fr/notre-programme/programme-2022", "2022")
UPR_SORTIE = "Cela impose en premier lieu de dénoncer juridiquement les traités européens, de sortir de l’UE et de l’euro, de sortir de l’OTAN"
UPR_BRICS = "Nous rapprocherons la France des BRICS (groupe des nouvelles puissances : Brésil, Russie, Inde, Chine et Afrique du Sud)"
UPR_LIGNES = "Interdisant toute fermeture de petite ligne ferroviaire et en réexaminant le dossier des lignes fermées pour motifs économiques ces quinze dernières années"
ASSELINEAU = [
    ("q004", 1, UPR22, "Introduire un système de proportionnelle partielle aux élections législatives"),
    ("q007", 2, UPR22, "Nous proposerons aux Français d’adopter le référendum d’initiative citoyenne et démocratiserons les institutions."),
    ("q010", 2, UPR22, "Nous créerons une Commission de contrôle des conflits d’intérêts des élus et hauts-fonctionnaires"),
    ("q013", 2, UPR22, "À la création de deux nouvelles tranches d’imposition pour les très hauts revenus (supérieurs à 250 000 € et 500 000 € par an)"),
    ("q014", 1, UPR22, "un impôt exceptionnel de solidarité pour les quelques dizaines de très grandes fortunes s’étant accrues pendant la crise de la Covid-19"),
    ("q015", 1, UPR22, "Nous diminuerons les charges patronales de 50% pour les petites et moyennes entreprises"),
    ("q017", 2, UPR22, "Nous augmenterons le SMIC brut de +24% sur le quinquennat"),
    ("q022", 1, UPR22, "Nous réaliserons le plus grand plan d’économies budgétaires des 50 dernières années, sans dégrader la qualité des services publics."),
    ("q025", 2, UPR22, "Nous porterons un coup d’arrêt à l’évasion fiscale et aux délocalisations en établissant immédiatement un contrôle des changes et des mouvements de capitaux."),
    ("q026", 2, UPR22, "Nous garantirons et revaloriserons de 25% les revenus des agriculteurs"),
    ("q027", 2, UPR22, "Nous renationaliserons ou cesserons le processus de privatisation rampante et de dégradation de la qualité de service de plusieurs grandes entreprises"),
    ("q031", -2, UPR22, "Nous sauvegarderons les retraites par répartition, qui sont un gage de solidarité nationale et permettent d’éviter de jouer les revenus des retraités en bourse."),
    ("q032", 2, UPR22, "pour interdire la privatisation de la Sécurité sociale et des services stratégiques de sécurité, de santé et d’éducation"),
    ("q033", 2, UPR22, "Nous augmenterons de 15% le budget de l’hôpital public dès le premier budget voté sous le quinquennat"),
    ("q035", 2, UPR22, "Ainsi, les allocations-chômage pourront être supprimées après deux refus de propositions d’embauche correspondant aux critères géographiques du demandeur d’emploi."),
    ("q036", 2, UPR22, "Nous aiderons toutes les familles en versant plus équitablement les allocations familiales, et créerons 150 000 places de crèches."),
    ("q040", 2, UPR22, "Nous ferons respecter nos frontières dès la première année du quinquennat, en donnant un coup d’arrêt à l’immigration subie."),
    ("q043", 2, UPR22, "Notre objectif sera de porter à 75% minimum le taux effectif des expulsions"),
    ("q048", 2, UPR22, "nous nous retirerons de l’Espace Schengen et établirons des contrôles à toutes les frontières"),
    ("q050", 2, UPR22, "Permettre aux préfets de systématiser le prononcé de décisions d’éloignement du territoire français à l’encontre des étrangers reconnus coupables d’infractions criminelles ou délictuelles"),
    ("q053", 1, UPR22, "ne doivent intégrer la communauté nationale par naturalisation que les personnes manifestant une claire volonté d’assimilation"),
    ("q055", 1, UPR22, "souhaitent que la France reste la France et préserve les valeurs chères aux Français de laïcité, d’égalité des sexes et de liberté religieuse"),
    ("q060", 2, UPR22, "Nous investirons massivement pour sauver le patrimoine national"),
    ("q067", -2, UPR22, UPR_SORTIE),
    ("q068", -2, UPR22, "Interdire tous les transferts de souveraineté à des institutions supranationales qui ne soient pas strictement limités dans leur objet et dans leur temps"),
    ("q069", 2, UPR22, UPR_SORTIE),
    ("q070", -2, UPR22, UPR_SORTIE),
    ("q072", -2, UPR22, "Suppression des coûts budgétaires liés à notre appartenance à l’Union européenne (12 milliards d’euros par an d’économies)"),
    ("q074", 2, UPR22, "Nous porterons le budget de la défense à 3% du PIB en fin de quinquennat"),
    ("q075", 2, UPR22, "il est indispensable de donner les moyens nécessaires à notre force de dissuasion et à son exercice dans de bonnes conditions"),
    ("q080", 2, UPR22, UPR_SORTIE),
    ("q081", 1, UPR22, UPR_BRICS),
    ("q082", 1, UPR22, UPR_BRICS),
    ("q091", 1, UPR22, "les tarifs de l’électricité et du gaz seront gelés pendant au moins les deux premières années du mandat"),
    ("q092", 1, UPR22, UPR_LIGNES),
    ("q096", 1, UPR22, UPR_LIGNES),
    ("q097", 2, UPR22, "Nous interdirons les pesticides dangereux pour la santé humaine et la biodiversité tels le glyphosate"),
    ("q103", 1, UPR22, "c’est l’échelle des rémunérations et, en priorité, celle des fonctionnaires de terrain (personnel hospitalier, policiers et gendarmes, militaires, enseignants) qui sera revue"),
    ("q104", 1, UPR22, "Nous redonnerons leur plein rôle aux organismes de formation professionnelle liés aux chambres des métiers"),
    ("q114", 1, UPR22, "Le port de vêtements neutres pour les élèves sera favorisé"),
    ("q117", 2, UPR22, "Nous augmenterons de 20% le budget de la justice et de 20% le budget de la police pour renforcer la chaîne pénale"),
    ("q119", 1, UPR22, "Nous introduirons dans notre droit pénal la peine de perpétuité incompressible pour les auteurs de crimes terroristes."),
    ("q120", 2, UPR22, "Nous rétablirons des peines planchers pour les auteurs récidivistes de ces mêmes infractions, avec des planchers augmentant à chaque nouvelle récidive"),
    ("q125", 1, UPR22, "Nous les remplacerons par des remises de peine conditionnées à la présentation d’un projet réel et de garanties de réinsertion."),
    ("q132", -2, UPR22, "Suppression des Conseils régionaux – remplacés par des Établissements publics administratifs de coopération légers"),
    ("q140", 1, UPR22, "un moratoire de 5 ans sera institué sur la création de zones commerciales en périphérie des villes de moins de 30 000 habitants"),
]

# Anasse Kazib (Révolution permanente) ---------------------------------------------
KZ = src("Programme d’Anasse Kazib (anasse2027.fr)", "https://anasse2027.fr/programme", "2026-10")
KZ_RETRAITE = "Retraite à 60 ans et 55 ans pour les métiers pénibles, sans conditions d'annuité."
KZ_FRONTIERES = "Régularisation de tous les sans-papiers, liberté de circulation et d'installation."
KZ_VE = "Fin de la Ve République, du Sénat et de la figure présidentielle."
KZ_LOIS = "Abrogation de toutes les lois sécuritaires, racistes et islamophobes, à commencer par la loi de 2004."
KZ_SALAIRES = "SMIC à 2000 € net, revalorisation de toutes les allocations, augmentation des salaires de 500 €, indexation sur l'inflation."
KAZIB = [
    ("q001", -2, KZ, KZ_VE),
    ("q002", 2, KZ, KZ_VE),
    ("q017", 2, KZ, KZ_SALAIRES),
    ("q019", 2, KZ, "Répartition du travail pour une semaine de 28h sans baisse de salaire."),
    ("q020", -2, KZ, "Interdiction des licenciements."),
    ("q023", 2, KZ, "Investissements massifs dans les services publics, qui doivent être placés sous le contrôle des travailleur·ses."),
    ("q027", 2, KZ, "Expropriation des secteurs stratégiques (énergie, transports, banques, santé, …) et placement sous contrôle des travailleur·ses."),
    ("q028", -2, KZ, KZ_RETRAITE),
    ("q029", 2, KZ, KZ_RETRAITE),
    ("q030", 2, KZ, KZ_RETRAITE),
    ("q037", 2, KZ, KZ_SALAIRES),
    ("q040", -2, KZ, KZ_FRONTIERES),
    ("q046", 2, KZ, KZ_FRONTIERES),
    ("q048", -2, KZ, KZ_FRONTIERES),
    ("q057", -2, KZ, KZ_LOIS),  # the 2004 law bans conspicuous religious symbols in public schools
    ("q058", -2, KZ, KZ_LOIS),
    ("q062", 2, KZ, "Avortement, PMA, transitions libres et gratuits."),
    ("q065", 2, KZ, KZ_LOIS),
    ("q074", -2, KZ, "Pas un euro pour la guerre, démantèlement de la machine de guerre française, 2ème exportateur d'armes mondial."),
    ("q079", -2, KZ, "Non au SNU et à la militarisation de nos écoles et de nos facs."),
]

# Selma Labib (NPA – Révolutionnaires) ----------------------------------------------
NPA = src("Intervention de Selma Labib à la fête de l’Humanité 2026 (NPA – Révolutionnaires)", "https://npa-revolutionnaires.org/articles/intervention-de-selma-labib-a-la-fete-de-lhumanite-2026", "2026-09")
LABIB = [
    ("q017", 2, NPA, "Il ne faut pas un seul revenu sous les 2000 euros net."),
    ("q019", 2, NPA, "oui il faut drastiquement diminuer le temps de travail sans perte de salaire et sans augmentation de la charge de travail"),
    ("q020", -2, NPA, "pour imposer l’interdiction des licenciements, c’est maintenant que ça se joue aussi"),
    ("q040", -2, NPA, "liberté de circulation et d’installation, régularisation de tous les sans-papiers"),
    ("q046", 2, NPA, "liberté de circulation et d’installation, régularisation de tous les sans-papiers"),
    ("q048", -2, NPA, "pour un monde sans frontières ni patrons"),
    ("q065", 2, NPA, "Le racisme, que ce soit sous la forme de l’islamophobie, de l’antisémitisme, ou du suprémacisme blanc"),
    ("q074", -2, NPA, "pas un homme, pas une femme, pas un euro pour les guerres impérialistes"),
    ("q079", -2, NPA, "La France c’est donc le retour du service militaire, c’est un record de dépenses militaires pour préparer des guerres impérialistes"),
    # The higher fees for non-EU students ("Bienvenue en France"), which she calls to repeal.
    ("q111", -2, NPA, "l’abrogation de cette mesure raciste inspirée par Le Pen, que le gouvernement a osé appeler « bienvenue en France »"),
]

# Bernard Cazeneuve (La Convention) -------------------------------------------------
# The summary of measures from his letter to the French, published by La Convention.
CONV = "https://assets.nationbuilder.com/laconvention/pages/2513/attachments/original/1784135398/Synthese_mesuresVfinale.pdf"


def conv(p):
    return src(f"La Convention, synthèse des mesures de la lettre de Bernard Cazeneuve aux Français, p. {p}", f"{CONV}#page={p}", "2026-07")


CZ_ENERGIE = "assumer le nucléaire, planifier le renouvellement du parc, rationaliser les investissements dans les renouvelables, s'émanciper des fossiles"
CZ_IMPOT = "que les plus hauts revenus, les grandes fortunes et les rentes financières contribuent à proportion de ce qu'ils tirent de la vie nationale"
CAZENEUVE = [
    ("q003", 1, conv(7), "Premier ministre engageant systématiquement sa responsabilité devant le Parlement lorsque les circonstances l’exigent, d'abord à son entrée en fonction"),
    ("q009", 1, conv(7), "Décentralisation : refonder la territorialité de la République, clarifier qui fait quoi, faire confiance aux territoires"),
    ("q012", 2, conv(3), "une politique de simplification réelle : revue systématique des normes et compensation obligatoire, deux normes supprimées pour une créée"),
    ("q013", 1, conv(3), CZ_IMPOT),
    ("q014", 1, conv(3), CZ_IMPOT),
    ("q021", 1, conv(8), "plan de réindustrialisation sur dix ans : filières stratégiques sécurisées par l'État"),
    # More contribution years rather than a higher legal age: in favour of keeping 64.
    ("q028", 1, conv(7), "durée de cotisation plutôt que recul de l'âge légal, en reprenant sur des bases nouvelles et négociées la trajectoire d'allongement de 2014"),
    ("q030", 2, conv(7), "pénibilité rétablie (postures contraignantes, port de charges, vibrations, risques chimiques), ouvrant droit au départ anticipé"),
    ("q042", 1, conv(5), "humanité (le droit d'asile comme engagement de civilisation)"),
    ("q070", 1, conv(5), "réforme budgétaire, politique industrielle commune, concurrence moins dogmatique, commerce moins naïf, et surtout décision à la majorité"),
    ("q071", 2, conv(5), "et surtout décision à la majorité, l'unanimité étant devenue « le levier de ceux qui veulent paralyser le continent depuis l'intérieur »"),
    ("q074", 1, conv(8), "Notre sécurité extérieure : réarmement à proportion de la menace, moyens rendus aux forces"),
    ("q076", 1, conv(8), "industrie de défense consolidée, coopérations européennes planifiées, préférence aux productions nationales et continentales"),
    ("q088", 1, conv(4), CZ_ENERGIE),
    ("q090", 1, conv(4), CZ_ENERGIE),
    ("q103", 2, conv(4), "Les enseignants tiennent la première place : mieux formés, mieux payés, mieux considérés"),
    ("q104", 1, conv(4), "La réindustrialisation passe par les territoires (villes moyennes, régions ouvrières, campagnes) et par la réhabilitation des métiers manuels"),
    ("q117", 1, conv(7), "police de proximité dotée d'effectifs dédiés et formés"),
    ("q139", 1, conv(7), "grand plan de constructions et de rénovations, à la fois social et écologique"),
]

# Antoine Mikolajczak (Équinoxe) ----------------------------------------------------
# Équinoxe publishes its 2027 program on November 4, 2026; until then, its campaign tract.
EQX = src("Équinoxe, tract de campagne d’Antoine Mikolajczak (2027)", "https://parti-equinoxe.fr/wp-content/uploads/2026/07/Parti-equinoxe-Tracts.pdf#page=2", "2026-07")
MIKOLAJCZAK = [
    ("q009", 2, EQX, "Plus de pouvoirs et de moyens pour les territoires"),
    ("q012", 2, EQX, "simplifier le droit et réduire le nombre de normes"),
    ("q007", 1, EQX, "développer la démocratie directe et les conventions citoyennes"),
]

# Karim Bouamrane (PS) ---------------------------------------------------------------
KB = src("Manifeste de Karim Bouamrane, « La France humaine et forte » (karimbouamrane2027.org)", "https://www.karimbouamrane2027.org/manifeste.html")
BOUAMRANE = [
    ("q012", 2, KB, "Nous simplifierons l'action publique. Nous réduirons les doublons administratifs."),
    ("q042", 1, KB, "La France est de longue date une terre d’asile et elle doit le rester."),
    ("q043", 1, KB, "et reconduire ceux qui se maintiennent irrégulièrement sur notre territoire"),
    ("q049", 1, KB, "Une France forte, c’est une France qui sait saisir la chance que représentent les plus de trois millions de binationaux que compte notre pays."),
    ("q055", 2, KB, "Une France humaine, c’est une France fraternellement laïque, qui combat le racisme, les discriminations et toutes les formes de violences."),
    ("q059", 2, KB, "Une France humaine, c’est une France fraternellement laïque, qui combat le racisme, les discriminations et toutes les formes de violences."),
    ("q061", 1, KB, "Une France qui protège les personnes LGBT+ contre les agressions et les discriminations."),
    ("q065", 1, KB, "Une France qui protège nos compatriotes musulmans contre l’islamophobie."),
    ("q074", 1, KB, "Une France forte, c'est une France qui investit dans sa défense, pour éviter la guerre."),
    ("q075", 1, KB, "La dissuasion ne dissuade que si elle est crédible et nos soldats méritent les moyens de leur mission."),
    ("q078", 1, KB, "agir à la source des migrations par le développement et la coopération"),
]

# Delphine Batho (Génération écologie) ----------------------------------------------
# Her party's statements on generationecologie.fr, which refuses scripted reads: the
# pages were read in the browser pane and the quotes checked against their text.
GE = "https://www.generationecologie.fr/"
GE_DEFENSE = src("Génération écologie : « Oui à la défense contre les menaces du nouveau Yalta des prédateurs »", f"{GE}2025/12/10/oui-la-defense-contre-les-menaces-du-nouveau-yalta-des-predateurs/", "2025-12-10")
GE_ESSENCE = src("Génération écologie : « Prix de l’essence à la pompe : l’urgence d’agir ! »", f"{GE}2026/04/10/prix-de-lessence-a-la-pompe-lurgence-dagir/", "2026-04-10")
BATHO = [
    ("q037", 1, GE_ESSENCE, "Mise en place d’un dispositif d’aide aux familles les plus vulnérables avec versement automatique dès les premières hausses de prix"),
    ("q074", 2, GE_DEFENSE, "Face aux menaces de Poutine et de Trump, Delphine Batho estime vital l'effort de défense."),
    ("q075", 1, GE_DEFENSE, "Il implique non seulement de renforcer notre dissuasion militaire, mais aussi une dissuasion civile fondée sur la réduction de nos dépendances"),
    ("q076", 2, GE_DEFENSE, "nous estimons vital l’effort de défense pour construire une Europe de la défense autonome sur le plan stratégique."),
    ("q090", 2, GE_ESSENCE, "Génération Écologie demande des aides d’urgences, l’organisation de la sortie des énergies fossiles"),
    ("q097", 1, src("Génération écologie : « Loi Duplomb 2 : on s’en souviendra en 2027 ! »", f"{GE}2026/07/21/loi-duplomb-2-on-sen-souviendra-en-2027/", "2026-07-21"),
     "une loi agricole obscurantiste, qui autorise le poison des néonicotinoïdes"),
]

# Juan Branco (Les Ruches) ------------------------------------------------------------
# "La Voie : pour sauver le peuple français", the program he wrote with Les Ruches (845
# measures). Measures it offers a constituent assembly as alternatives ("proposant
# alternativement", e.g. laïcité or a concordat, drug policy) are not read as positions.
def voie(p):
    return src(f"« La Voie : pour sauver le peuple français », programme de Juan Branco et des Ruches, p. {p}", f"https://ruches.org/projet-1784217879253.pdf#page={p}")


VOIE_SORTIE = "Sortie de l’Union Européenne, de l’euro, du Conseil de l’Europe et/ou de l’espace Schengen."
BRANCO = [
    ("q001", -2, voie(9), "Référendum fondé sur l’article 11 de la Constitution proposant la convocation d’une assemblée constituante dotée d’un mandat de 12 mois"),
    ("q003", 2, voie(10), "Abrogation des articles 49.3 et assimilés de la Constitution."),
    # 200 of the 314 deputies by list proportional representation, the rest in single-member seats.
    ("q004", 1, voie(10), "Concernant la chambre basse : élection à scrutin proportionnel sur listes à un tour pour 200 députés"),
    ("q007", 2, voie(8), "Création d’un RIC en toutes matières."),
    ("q010", 2, voie(14), "Transparence absolue et intégrale des agendas ministériels, membres du gouvernement et élus à l’égard du public"),
    ("q012", 2, voie(26), "la bureaucratisation et les charges impositives sont devenues insupportables"),
    ("q014", 2, voie(29), "Rétablissement de l’ISF avec un mécanisme de précompte sur les droits de succession."),
    # A higher national floor, set regionally above it.
    ("q017", 1, voie(30), "Déconcentration du SMIC, avec réhaussement du seuil minimal national à 1500 euros net."),
    ("q020", 2, voie(30), "Référendum proposant une réforme à la suisse unifiant les statuts de travail et créant la possibilité d’un licenciement simple avec préavis."),
    # Alongside a surplus target and "un accroissement contrôlé de l'inflation".
    ("q022", 1, voie(27), "un changement de la politique allocative aux fins de baisse des dépenses"),
    ("q025", 2, voie(29), "Création d’un programme de dénonciation des délits d’initiés et de la fraude fiscale sur le modèle de l’IRS whistleblower program, avec récompenses financières proportionnelles."),
    ("q027", 2, voie(54), "Expropriation des compagnies d’autoroutes."),
    ("q032", 2, voie(40), "Le rétablissement d’un service public de la santé universel, égalitaire et accessible à tous les citoyens, sans condition de ressources"),
    # Lower benefits over time, though resigning would open three months of rights.
    ("q034", -1, voie(30), "Dégressivité des allocations chômage à partir de la première année"),
    ("q036", 2, voie(39), "Droit opposable à la place en crèche."),
    ("q037", 2, voie(29), "Déconditionnalisation du RSA, attribution automatique des minima sociaux afin de sortir de la pauvreté ceux qui n’ont même pas les moyens de les réclamer."),
    ("q041", 1, voie(22), "Développement d’une politique d’attractivité en faveur des individus à haut niveau de qualification"),
    # Conditions for regularizing people without residence permits.
    ("q046", 1, voie(21), "Mise en place de critères objectivables d’intégration concernant les étrangers, accompagnée d’obligations de service à la nation"),
    # Put to a referendum, with "et/ou" leaving open which exits: only "plutôt".
    ("q067", -1, voie(8), VOIE_SORTIE),
    ("q077", -1, voie(25), "Arrêt des livraisons d’armes à l’Ukraine."),
    ("q078", -1, voie(23), "réduction de l’aide au développement multilatérale aux chantiers prioritaires et transformation des autres crédits en crédits de coopération"),
    # For everyone, with a civil option, rather than for men only.
    ("q079", 1, voie(24), "Référendum proposant un service militaire obligatoire pour tous, avec options civile et militaire"),
    ("q080", 1, voie(8), VOIE_SORTIE),
    ("q083", -1, voie(8), "Sortie de l’OTAN (commandement intégré ou du Traité)."),
    ("q088", 2, voie(52), "Construction de 14 EPR 2, développement d’une filière intégrée RNR-NA."),
    # Solar subsidies confined to existing sites and tied to local manufacturing.
    ("q089", -1, voie(52), "Concentration des subventions photovoltaïques aux installations sur emprises déjà existantes (terrains militaires, gares, parkings…)"),
    ("q090", 1, voie(52), "La souveraineté énergétique et en particulier la fin de la dépendance aux flux fossiles importés sera érigée en priorité nationale."),
    ("q092", 2, voie(54), "lancement d’un grand plan d’investissement dans les lignes secondaires, notamment des 4000 kilomètres de lignes menacées d’effondrement"),
    ("q093", -2, voie(54), "Abolition des Zones à Faibles Émissions."),
    ("q095", 2, voie(25), "Renforcement de la politique de défense civile (UIISC), et lancement d’un programme de dronification de la lutte anti-incendie accompagnée d’un programme de bombardiers d’eau européen."),
    ("q097", 2, voie(48), "Interdiction à horizon quinquennal des pesticides CMR de catégorie 1 et perturbateurs endocriniens identifiés, et réduction des CMR de catégorie 2."),
    ("q103", 2, voie(37), "Revalorisation salariale des enseignants en début de carrière"),
    # Page 37 reaches fewer pupils partly through more selection at entry to the lycée.
    ("q107", 1, voie(36), "la revalorisation salariale des enseignants du secondaire et du supérieur, la réduction du nombre d’élèves et le changement de modèle éducatif"),
    ("q109", 2, voie(36), "Rétablissement de la gratuité réelle des études universitaires pour tout résident Français."),
    ("q113", 2, voie(37), "Fin des MIG (ex-SNU) et de Parcoursup."),
    # Also the BRAV-M dissolved; about policing protests, not riots as such.
    ("q128", -1, voie(21), "Abandon des outils de maintien de l’ordre « intermédiaires »"),
    # A property surtax; foreign platforms such as Airbnb would also be banned (p. 32).
    ("q135", 2, voie(53), "avec un coefficient doublé pour les logements vacants et triplé pour les meublés touristiques en zone tendue"),
    ("q140", 2, voie(53), "Plan d’arrêt et de reconversion des sols artificialisés durcissant les ZAN"),
]

# Jean-François Legendre (À nous maintenant) -----------------------------------------
# His manifesto "64 % – vers une alternative citoyenne en France", which the movement's
# site links as its founding text ("Mon manifeste"); a Google Doc, read through its
# public text view. It leaves many choices to referendums and to a citizens' assembly,
# so only what it proposes itself is used, and views on past reforms (retirement at 60,
# the 35 hours) count as partial answers.
LEG = src("« 64 % – vers une alternative citoyenne en France », manifeste de Jean-François Legendre (À nous maintenant)",
          "https://docs.google.com/document/d/1G4dUZaI20umZghEgSgRGCQeiWDJ2fiwhLZvtUK7hofc/edit?usp=sharing")
LEGENDRE = [
    ("q007", 2, LEG, "Le RIG et le RIC associés, constituent une des bases de la démocratie citoyenne que nous défendons."),
    ("q011", 1, LEG, "Les budgets devront au minimum être à l'équilibre."),
    ("q012", 1, LEG, "Beaucoup de bonnes volontés sont découragées par le parcours du combattant que représente la création d'une activité en France"),
    ("q013", 2, LEG, "L'augmentation des impôts concernera uniquement les hauts revenus"),
    # New businesses only, for their first three years.
    ("q015", 1, LEG, "Nous proposerons qu’il n’y ait pas d'impôts et seulement des charges sociales symboliques pendant les trois premières années d'existence."),
    ("q019", -1, LEG, "en 1981 était irresponsable, le passage au 35 heures payées 39 l'était tout autant"),
    ("q021", 2, LEG, "des sites industriels reprendront vie avec le concours des pouvoirs publics"),
    ("q022", 2, LEG, "Les efforts demandés ne seront pas des taxes supplémentaires, ils consisteront en des réductions des versements de l’État"),
    ("q023", -1, LEG, "Que ce soit celui de la Sécurité sociale, celui des retraites, celui de l’État... pas de déficit."),
    ("q025", 2, LEG, "il sera procédé à une forte réduction des possibilités d'optimisation fiscale et d'évasion vers les paradis fiscaux"),
    ("q026", 1, LEG, "L'aide aux petits agriculteurs sera une priorité."),
    ("q029", -1, LEG, "Le passage de l'âge de la retraite de 65 ans à 60 ans en 1981 était irresponsable"),
    # Under "La santé": care paid in full by the state's insurers.
    ("q032", 2, LEG, "C'est merveilleux, il faut préserver ce système, mais il faut savoir que cela n'existe que dans de très rares pays."),
    ("q034", -2, LEG, "Donc moins de remboursements pour les actes médicaux et les médicaments, moins de prestations chômage, moins de prestations sociales"),
    ("q037", -1, LEG, "il faut également admettre que notre système est trop généreux et accepter de réduire la voilure pendant quelques années"),
    ("q040", 1, LEG, "La France doit faire sa part pour soulager la souffrance humaine et répondre aux appels de détresse, mais il y aura obligatoirement des limites."),
    ("q041", -1, LEG, "il est peu probable que quelqu'un qui arrive de l'étranger, qui ne parle pas le français, puisse trouver un emploi"),
    # Refugees welcomed for a time, with unpaid work in return and no naturalization.
    ("q042", -1, LEG, "Nous pensons qu'il faut accueillir temporairement ces personnes aux conditions qu'elles repartent dans leur pays lorsque la situation politique le permettra"),
    ("q043", 1, LEG, "Les migrants clandestins, donc illégaux, qui ne bénéficieront pas d'aides et qui sont voués à être renvoyés dans leur pays d'origine."),
    # Also: "Nos alliances et partenariats (Union Européenne, OTAN, ONU, OMC…) : ils doivent
    # perdurer et être renforcés", too long to quote whole.
    ("q067", 2, LEG, "c'était la contrepartie à la création de cet ensemble robuste, qui permet aux 27 États d'exister et de faire entendre une voix commune"),
    ("q068", -1, LEG, "D'autres exemples illustrent l'intrusion excessive de l'UE et de la Commission dans l'organisation de la société française."),
    ("q069", 1, LEG, "certaines législations ou directives éditées par l'Union sont trop pénalisantes pour les États et devront être renégociées"),
    ("q071", 2, LEG, "supprimer la règle de l'unanimité au sein de l'UE ou celle du veto au sein de l'ONU"),
    # Drones yes ("il faut réfléchir à compléter notre panoplie"), a war economy no.
    ("q074", -1, LEG, "Les efforts qui seront demandés et les économies réalisées devront financer autre chose que des bombes et des chars."),
    ("q076", 1, LEG, "Il faut cependant rester modeste et miser sur l'union qui, comme chacun sait, fait la force."),
    ("q081", -1, LEG, "On reverra des étiquettes “made in France” au lieu de celles, omniprésentes, “made in China”."),
    ("q088", 1, LEG, "Nous sommes résolument en faveur du nucléaire, aucun autre système de production d'énergie électrique ne pourrait suffire à notre consommation."),
    # Lower prices rather than aid.
    ("q091", -1, LEG, "Pourquoi donner des chèques énergie plutôt que de réduire les prix du gaz ou de l’électricité"),
    # One of the school reforms it lists as possible ("Les pistes de changement pourraient être").
    ("q104", 1, LEG, "Les stages en entreprises et à l'étranger seront intensifiés."),
    # Under "L'éducation": no fees from nursery school to university.
    ("q109", 2, LEG, "C'est merveilleux, il faut préserver ce système, mais il faut savoir que cela n'existe dans aucun autre pays."),
    ("q110", -1, LEG, "les aides au logement, les restaurants universitaires, rendent la destination France très attractive. Sommes nous obligés d'en faire autant ?"),
    ("q117", 2, LEG, "De nouvelles unités du RAID et du GIGN seront créées. Nous ouvrirons des commissariats dans les villes ou villages qui en auront besoin."),
    ("q119", 2, LEG, "La législation doit être renforcée, les peines augmentées et surtout appliquées."),
    # Among the steps of "notre cheminement" that give France its standing.
    ("q122", -1, LEG, "à la rédaction de la Déclaration des droits de l'Homme, et plus récemment à l'abolition de la peine de mort"),
    ("q144", 1, LEG, "Nous développerons toutes les activités permettant le recyclage, la réparation, la ré-utilisation, la fabrication de biens “qui durent toute la vie”"),
]

# Clara Egger (Solution Démocratique) -------------------------------------------------
# A program "volontairement limité" to institutions: the citizens' constitutional
# initiative and decentralization from the bottom up. Her party's pages, labelled as such.
def soldem(path, title, date=None):
    return src(f"Solution Démocratique (parti de Clara Egger), « {title} »", f"https://solutiondemocratique.fr/{path}/", date)


EGGER = [
    ("q002", 1, soldem("clara-egger", "Clara Egger, candidate à l’élection présidentielle de 2027", "2024-09-13"),
     "elle porte une conception de la présidence fondée sur l’arbitrage, le respect des équilibres des pouvoirs et la garantie d’un État impartial"),
    ("q007", 2, soldem("notre-solution", "Notre solution (et notre stratégie)"),
     "en instaurant deux outils simples mais puissants : l’initiative citoyenne constituante ; le référendum obligatoire pour modifier la Constitution"),
    ("q009", 2, soldem("proposition-de-revision-legislative-pour-instaurer-la-democratie-directe-dans-les-communes", "Proposition de révision législative pour permettre à la France de se décentraliser par le bas"),
     "Ainsi, l’État doit (et non peut) déléguer une compétence à une collectivité qui lui en fait la demande."),
    # Any authority may ask; when a region and a commune both do, the smaller one wins.
    ("q132", 1, soldem("proposition-de-revision-legislative-pour-instaurer-la-democratie-directe-dans-les-communes", "Proposition de révision législative pour permettre à la France de se décentraliser par le bas"),
     "Certainement toutes les compétences qui ne sont pas inscrites dans la Constitution, comme par exemple le développement durable, les transports, la sécurité."),
]

# Mira Markovic (Parti animaliste) ---------------------------------------------------
# The party calls itself "transpartisan et monothématique" and has published no 2027
# program; its "Programmes" page still presents the national program of 2022 and the
# European program of 2024. Both are the party's, labelled as such. It leaves France's
# energy choices (nuclear, renewables) to a national debate and referendum.
PA = src("Parti animaliste (parti de Mira Markovic), programme national 2022 « Sauver les animaux et nous sauver nous-mêmes »", "https://parti-animaliste.fr/programme", "2022")


def pa_eu(path, title):
    return src(f"Parti animaliste (parti de Mira Markovic), programme européen 2024, « {title} »", f"https://parti-animaliste.fr/{path}", "2024")


MARKOVIC = [
    ("q004", 2, PA, "Instaurer un scrutin proportionnel pour les élections législatives."),
    ("q007", 2, PA, "Instaurer le Référendum d’initiative citoyenne – législatif et abrogatoire – (RIC) en toutes matières"),
    # Access to administrative documents, not officials' own declarations.
    ("q010", 1, PA, "Mettre en place des mesures de transparence et faciliter l’accès aux données administratives : accorder un pouvoir de sanction et d’astreinte à la CADA"),
    # Aid to change farming practices.
    ("q026", 1, pa_eu("pour-une-europe-plus-democratique", "Pour une Europe plus démocratique"), "Nos agriculteurs sont les premiers à vouloir évoluer, nous devons les aider financièrement pour le faire."),
    ("q068", 1, pa_eu("pour-une-europe-plus-democratique", "Pour une Europe plus démocratique"), "Donner à l’Union européenne une compétence explicite en matière de protection animale."),
    ("q097", 2, PA, "Augmenter les lieux d’interdiction de pesticides en incluant une interdiction dans un périmètre d’un kilomètre des zones habitées."),
    ("q101", 1, pa_eu("pour-une-agriculture-davenir", "Pour une agriculture d’avenir"), "Inclure l’élevage dans le projet de taxe carbone européen."),
    # Trees on private land, for wildlife.
    ("q102", 1, PA, "Encourager la plantation d’arbres et arbustes de variétés locales, pour favoriser la présence d’animaux sauvages dans les espaces privatifs"),
    ("q117", 1, PA, "Créer dans chaque département des unités de police et de gendarmerie attachées à la protection animale."),
    ("q138", 1, PA, "Soumettre à référendum local l’implantation d’antennes relais ou d’éoliennes à une distance de 5 km des habitations"),
    ("q140", 2, PA, "Lutter contre l’étalement urbain et l’artificialisation des sols."),
]

# Olivier Becht --------------------------------------------------------------------
# His "Projet France" is not published yet; his answers in a Sud Radio interview as a
# candidate, transcribed on the station's site.
BECHT_SUD = src("Sud Radio, « Le Grand Matin week-end », entretien avec Olivier Becht",
                "https://www.sudradio.fr/politique/olivier-becht-je-suis-candidat-a-lelection-presidentielle-et-jirai-jusquau-bout", "2026-10-11")
BECHT = [
    ("q009", 2, BECHT_SUD, "aller vers davantage de fédéralisme dans l’organisation de la République, afin de donner du pouvoir à ceux qui sont sur le terrain"),
    # A salary floor between jobs, on condition of taking a suitable job, training or volunteering.
    ("q035", 1, BECHT_SUD, "Il s’agirait d’une forme de revenu universel, assorti de trois conditions : accepter un emploi correspondant à ses qualifications"),
    ("q070", 1, BECHT_SUD, "Je défends également une nouvelle dynamique européenne, autour d’un noyau dur de six, sept ou peut-être huit États"),
    ("q090", 1, BECHT_SUD, "Je souhaite notamment engager une révolution énergétique, avec le développement des carburants de synthèse, pour réduire notre dépendance aux importations pétrolières."),
    ("q113", 2, BECHT_SUD, "Les lycéens ont raison de dire que Parcoursup est une boîte noire qui doit être supprimée et remplacée."),
]

# Natacha Polony (Nous sommes la France) ------------------------------------------------
# No program yet. Her answers in a Sud Radio interview (a month before she declared),
# transcribed on the station's site, and her words quoted by Pleinchamp at the Sommet
# de l'élevage, a week before.
POLONY_SUD = src("Sud Radio, « Le Grand Matin », entretien avec Natacha Polony",
                 "https://www.sudradio.fr/sud-radio/natacha-polony-je-lance-un-appel-aux-orphelins-de-la-politique", "2026-09-15")
POLONY_PC = src("Pleinchamp, « Natacha Polony candidate à l’Élysée, avec l’agriculture comme champ de bataille » (propos recueillis au Sommet de l’élevage)",
                "https://www.pleinchamp.com/actualite/natacha-polony-candidate-a-l-elysee-avec-l-agriculture-comme-champ-de-bataille", "2026-10-14")
POLONY = [
    ("q012", 1, POLONY_SUD, "le rôle de l'État, ce n'est pas de venir expliquer aux gens à quelle hauteur il faut faire les barrières devant les écoles"),
    ("q021", 1, POLONY_SUD, "L'urgence absolue est de bâtir une politique ambitieuse pour la production et les salaires."),
    ("q022", 1, POLONY_SUD, "C'est à l'État de commencer par faire les efforts. Donc, il se réforme, parce que vous avez des dépenses qui sont illégitimes."),
    ("q026", 2, POLONY_PC, "un grand plan de soutien aux revenus des agriculteurs"),
    ("q027", 1, POLONY_SUD, "Quand, par exemple, l'Union Européenne essaye de nous expliquer qu'il faut privatiser notre énergie hydroélectrique, nos barrages, c'est non. Et on renationalise EDF"),
    ("q050", 2, POLONY_SUD, "ceux qui enfreignent les règles doivent être punis et on doit les inviter à quitter le territoire quand ils ne sont pas des Français"),
    # She also opposes renationalizing the CAP ("C'est une ligne rouge", Pleinchamp), so
    # returning powers to the member states (q069) is left open.
    ("q068", -1, POLONY_SUD, "vous avez une Commission européenne qui outrepasse systématiquement ses prérogatives qui ne respectent même pas les traités"),
    ("q072", -1, POLONY_SUD, "faire comme avait fait l'Angleterre quand elle était encore dans l'Europe et de dire, je ne paierai pas tant que je serai mis en danger"),
    # To stop the war that closed the Strait of Hormuz.
    ("q083", -1, POLONY_SUD, "nous devons utiliser la puissance économique de l'Europe et nos outils de coercition pour signifier aux États-Unis que cela suffit"),
    ("q088", 1, POLONY_SUD, "on met en place une véritable politique urgente de défense du nucléaire"),
    # A fuel tax that falls when prices rise.
    ("q091", 1, POLONY_SUD, "La taxe flottante sur les produits pétroliers est une mesure de bon sens qui s'adapte à la réalité du moment"),
]

# Jordan Bardella (Rassemblement national) ------------------------------------------
# Tested in polls, not declared. The RN's 2024 programs were his own campaigns: the
# legislative program opens with his signed foreword as candidate for Prime Minister,
# and he led the RN's European list. Le Pen's rows cite the same documents.
def bardella24(p):
    return src(f"Programme du RN pour les législatives 2024, présenté par Jordan Bardella (candidat à Matignon), p. {p}", f"{RN24}#page={p}", "2024-06-25")


def bardellaeu(p):
    return src(f"Programme du RN pour les européennes 2024 (liste menée par Jordan Bardella), p. {p}", f"{RNEU}#page={p}", "2024-05-06")


BARDELLA = [
    ("q012", 1, bardella24(4), "Lancement des états généraux de la simplification"),
    ("q040", 2, bardella24(6), "Préserver le peuple français de la submersion migratoire"),
    ("q048", 1, bardella24(6), "Ouvrir des négociations avec nos partenaires européens pour réserver la libre-circulation Schengen aux seuls ressortissants européens"),
    ("q050", 1, bardella24(4), "Suppression de toutes les dérogations qui empêchent les expulsions d’étrangers"),
    ("q068", -2, bardellaeu(2), "la Commission de Bruxelles exploite les crises pour s’arroger des compétences supplémentaires au détriment de la souveraineté des États"),
    ("q070", -2, bardellaeu(4), "qui prône une véritable dissolution des nations dans un État européen centralisé"),
    ("q072", -2, bardellaeu(7), "Baisser la contribution française nette (surplus) versée à l’UE"),
    ("q074", 1, bardella24(6), "Sanctuariser la trajectoire budgétaire de la Loi de Programmation Militaire"),
    ("q088", 2, bardella24(8), "Lancer le plan Marie Curie de relance du nucléaire"),
    ("q091", 1, bardellaeu(7), "la baisse de la TVA de 20 à 5,5% sur les énergies"),
    ("q093", -2, bardella24(7), "Supprimer les Zones à Faibles Emissions"),
    ("q106", 2, bardella24(7), "Augmenter le nombre d’étudiants en médecine (fin du numerus apertus)"),
    ("q120", 2, bardella24(4), "Mise en place des peines planchers pour les récidivistes"),
    ("q121", 2, bardella24(6), "Réformer une partie de la justice des mineurs (abaissement de la majorité pénale à 16 ans, possibilité de comparution immédiate…)"),
    ("q142", 2, bardella24(6), "Rendre obligatoire la création d’une police municipale pour les communes de plus de 10 000 habitants"),
]

CANDIDATES = {
    "jean-luc-melenchon": MELENCHON,
    "marine-le-pen": LE_PEN,
    "eric-zemmour": ZEMMOUR,
    "edouard-philippe": PHILIPPE,
    "gabriel-attal": ATTAL,
    "bruno-retailleau": RETAILLEAU,
    "raphael-glucksmann": GLUCKSMANN,
    "david-lisnard": LISNARD,
    "marine-tondelier": TONDELIER,
    "francois-ruffin": RUFFIN,
    "fabien-roussel": ROUSSEL,
    "nicolas-dupont-aignan": DUPONT_AIGNAN,
    "nathalie-arthaud": ARTHAUD,
    "xavier-bertrand": BERTRAND,
    "dominique-de-villepin": VILLEPIN,
    "florian-philippot": PHILIPPOT,
    "francois-asselineau": ASSELINEAU,
    "anasse-kazib": KAZIB,
    "selma-labib": LABIB,
    "bernard-cazeneuve": CAZENEUVE,
    "antoine-mikolajczak": MIKOLAJCZAK,
    "karim-bouamrane": BOUAMRANE,
    "delphine-batho": BATHO,
    "juan-branco": BRANCO,
    "jean-francois-legendre": LEGENDRE,
    "clara-egger": EGGER,
    "mira-markovic": MARKOVIC,
    "olivier-becht": BECHT,
    "natacha-polony": POLONY,
    "jordan-bardella": BARDELLA,
}


def check(cid, rows, valid_ids):
    # A candidate who leaves the race drops out of presidentielle-2027.json; their
    # positions are kept (the site shows only listed candidates) rather than failing.
    if cid not in valid_ids:
        print(f"note: {cid} is not among the presidential candidates any more")
    seen = set()
    for qid, stance, source, quote in rows:
        assert re.fullmatch(r"q\d{3}", qid) and 1 <= int(qid[1:]) <= 144, f"{cid}: bad question {qid}"
        assert qid not in seen, f"{cid}: {qid} twice"
        seen.add(qid)
        assert stance in (-2, -1, 0, 1, 2), f"{cid} {qid}: stance {stance}"
        assert source["url"].startswith("https://"), f"{cid} {qid}: source must be https"
        # No quote only for a news summary of a proposal; otherwise ≤ 25 words, verbatim.
        assert quote is None or (quote and len(quote.split()) <= 25), f"{cid} {qid}: quote over 25 words"


def main():
    pres = json.loads(PRES.read_text(encoding="utf-8"))
    valid = {c["id"] for c in pres["candidates"]}
    out = {}
    for cid, rows in CANDIDATES.items():
        check(cid, rows, valid)
        read = {"accessed": READ_LATER} if cid in LATER else {}
        out[cid] = {qid: {"stance": s, "source": {**src_, **read}, "quote": q} for qid, s, src_, q in sorted(rows)}
    OUT.write_text(json.dumps({"updated": datetime.now(timezone.utc).isoformat(timespec="minutes"), "candidates": out},
                              ensure_ascii=False, indent=1), encoding="utf-8")
    counts = ", ".join(f"{cid} {len(rows)}" for cid, rows in CANDIDATES.items())
    print(f"wrote {OUT.relative_to(ROOT).as_posix()}: {sum(len(r) for r in CANDIDATES.values())} positions ({counts})")


if __name__ == "__main__":
    main()
