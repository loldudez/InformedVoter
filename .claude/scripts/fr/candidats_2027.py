"""Who is a declared candidate for the 2027 presidential election, checked by hand.

French Wikipedia's "Candidats déclarés" table is the daily aggregator, and
`update_presidentielle.py` cross-checks it every day against franceinfo's tracker of
declared candidates ("Qui sont les candidats déclarés", a list franceinfo updates as
candidacies are announced or withdrawn). This file records what was checked person by
person on Nov. 2, 2026: each declared candidate with the article that reports their
own announcement, and the people polls test or trackers list who are not running, with
the reason and its source.

How the three combine (in `update_presidentielle.py`):
  * someone checked here as declared stays declared unless franceinfo marks them as
    withdrawn, or neither tracker lists them any more (then they wait for a new check);
  * someone checked here as not running stays out unless both trackers list them as a
    candidate (a new announcement);
  * anyone else needs both trackers to list them.
Every disagreement is written to the data's `checks`, shown on the About page, so it can
be settled here with a source.

Known differences, Nov. 2: franceinfo's tracker leaves out Zemmour (who announced "Je serai
candidat" on BFMTV on Sept. 17) and Bertrand (who confirmed on Aug. 26-27), and lists
Lassalle, whose July statement was conditional on a fundraiser. Wikipedia still lists
Cazeneuve, who told Le Figaro on Oct. 21 that he would help Raphaël Glucksmann win, and
leaves out five people franceinfo lists (Branco, Legendre, Billetdoux, Collovati, Rohou).

    py scripts/fr/candidats_2027.py     (checks the list and prints a summary)
"""

import sys

CHECKED_ON = "2026-11-02"
FRANCEINFO_TRACKER = ("https://www.franceinfo.fr/elections/presidentielle/"
                      "portraits-qui-sont-les-candidats-declares-a-l-election-presidentielle-de-2027_8208032.html")


def src(outlet, title, url, date):
    return {"outlet": outlet, "title": title, "url": url, "date": date}


TRACKER = src("franceinfo", "PORTRAITS. Qui sont les candidats (déjà) déclarés à l'élection présidentielle de 2027 ?",
              FRANCEINFO_TRACKER, "2026-10-22")

# Declared candidates, keyed by their French Wikipedia article (or their name when they
# have none, with `article: None`). `party` and `role` are given only for people missing
# from Wikipedia's table, which supplies them for everyone else. `missing` names a
# tracker known to leave someone out, so the daily cross-check doesn't flag it again.
DECLARED = {
    "Nathalie Arthaud": {"source": src(
        "Le Monde", "Nathalie Arthaud, la porte-parole de Lutte ouvrière, annonce sa candidature à la présidentielle de 2027",
        "https://www.lemonde.fr/politique/article/2025/12/08/presidentielle-la-porte-parole-de-lutte-ouvriere-nathalie-arthaud-annonce-sa-candidature_6656468_823448.html",
        "2025-12-08")},
    # The UPR has published no 2027 announcement page; franceinfo's tracker and 20 Minutes
    # (May 19, 2026) both describe him as a 2027 candidate.
    "François Asselineau": {"source": TRACKER},
    "Gabriel Attal": {"source": src(
        "Le Monde", "Présidentielle 2027 : Gabriel Attal officialise sa candidature en Aveyron en espérant s’éloigner de l’héritage d’Emmanuel Macron",
        "https://www.lemonde.fr/politique/article/2026/05/22/presidentielle-2027-gabriel-attal-officialise-sa-candidature-en-aveyron-en-esperant-s-eloigner-de-l-heritage-d-emmanuel-macron_6692277_823448.html",
        "2026-05-22")},
    "Delphine Batho": {"source": src(
        "Le Nouvel Obs", "Delphine Batho : « Je suis candidate à l’élection présidentielle pour reconstruire une écologie capable de gouverner »",
        "https://www.nouvelobs.com/politique/20251125.OBS110076/delphine-batho-je-suis-candidate-a-l-election-presidentielle-pour-reconstruire-une-ecologie-capable-de-gouverner.html",
        "2025-11-25")},
    "Olivier Becht": {"source": src(
        "Paris Match", "EXCLUSIF - « Je suis candidat à la présidentielle » : un ancien ministre d’Élisabeth Borne sort du bois",
        "https://www.parismatch.com/actu/politique/exclusif-je-suis-candidat-a-la-presidentielle-un-ancien-ministre-delisabeth-borne-sort-du-bois-276281",
        "2026-09-24")},
    "Xavier Bertrand": {"missing": {"franceinfo"}, "source": src(
        "Libération", "Le président LR des Hauts-de-France, Xavier Bertrand, confirme qu’il sera candidat à la présidentielle",
        "https://www.liberation.fr/politique/le-president-lr-des-hauts-de-france-xavier-bertrand-confirme-quil-sera-candidat-en-2027-20260827_PF5ERRL6GNEP7PWMY7GQ4SJDL4/",
        "2026-08-27")},
    # He stayed out of the Socialist primary and has not withdrawn since Glucksmann won it
    # (franceinfo's tracker still lists him on Oct. 22).
    "Karim Bouamrane": {"source": src(
        "Le Figaro", "Présidentielle 2027 : «Je suis candidat», annonce le maire socialiste de Saint-Ouen Karim Bouamrane",
        "https://www.lefigaro.fr/politique/presidentielle-2027-je-suis-candidat-annonce-karim-bouamrane-ps-20260609",
        "2026-06-09")},
    "Nicolas Dupont-Aignan": {"source": src(
        "Le Figaro", "Nicolas Dupont-Aignan se déclare candidat à la prochaine élection présidentielle",
        "https://www.lefigaro.fr/politique/nicolas-dupont-aignan-se-declare-candidat-a-la-prochaine-election-presidentielle-20250308",
        "2025-03-08")},
    "Sylvain Durif": {"source": src(
        "RTL", "Christ cosmique, grand monarque et bientôt président de la République ? Le vidéaste complotiste Sylvain Durif se déclare candidat à l'élection de 2027",
        "https://www.rtl.fr/actu/politique/christ-cosmique-grand-monarque-et-bientot-president-de-la-republique-le-videaste-complotiste-sylvain-durif-se-declare-candidat-a-l-election-de-2027-7900664715",
        "2026-08-25")},
    "Clara Egger": {"source": src(
        "Le Dauphiné libéré", "L'Ardéchoise Clara Egger est candidate à l’élection présidentielle pour « rétablir un équilibre démocratique »",
        "https://www.ledauphine.com/politique/2026/05/21/l-ardechoise-clara-egger-est-candidate-a-l-election-presidentielle-pour-retablir-un-equilibre-democratique",
        "2026-05-21")},
    "Raphaël Glucksmann": {"source": src(
        "Libération", "Résultats de la primaire socialiste : Raphaël Glucksmann élu dès le premier tour et propulsé vers la présidentielle",
        "https://www.liberation.fr/politique/elections/resultats-de-la-primaire-socialiste-raphael-glucksmann-elu-des-le-premier-tour-et-propulse-vers-la-presidentielle-20261011_HSXHVD45NJFOHG7JCKCGCYDVDY/",
        "2026-10-11")},
    "Anasse Kazib": {"source": src(
        "franceinfo", "Le cheminot Anasse Kazib annonce sa candidature à la présidentielle 2027",
        "https://www.franceinfo.fr/elections/presidentielle/presidentielle-2027-le-cheminot-anasse-kazib-annonce-sa-candidature_8040020.html",
        "2026-06-01")},
    "Selma Labib": {"source": src(
        "BFMTV", "Présidentielle 2027: le NPA-Révolutionnaires annonce présenter la candidature de sa porte-parole Selma Labib",
        "https://www.bfmtv.com/politique/elections/presidentielle/presidentielle-2027-le-npa-revolutionnaires-annonce-presenter-la-candidature-de-sa-porte-parole-selma-labib_AD-202606170500.html",
        "2026-06-17")},
    "Francis Lalanne": {"source": src(
        "franceinfo", "Présidentielle 2027 : le chanteur Francis Lalanne annonce être candidat, premier meeting vendredi à Paris",
        "https://www.franceinfo.fr/elections/presidentielle/presidentielle-2027-le-chanteur-francis-lalanne-officiellement-candidat-premier-meeting-vendredi-a-paris_8153588.html",
        "2026-08-19")},
    "Marine Le Pen": {"source": src(
        "Euronews", "« Je suis candidate à l’élection présidentielle », annonce Marine Le Pen sur TF1",
        "https://fr.euronews.com/my-europe/2026/07/07/je-suis-candidate-a-lelection-presidentielle-annonce-marine-le-pen-sur-tf1",
        "2026-07-07")},
    "David Lisnard": {"source": src(
        "franceinfo", "Le maire de Cannes, David Lisnard, annonce sa candidature à l'élection présidentielle et officialise son départ des Républicains",
        "https://www.franceinfo.fr/elections/presidentielle/le-maire-de-cannes-david-lisnard-annonce-sa-candidature-a-l-election-presidentielle-et-officialise-son-depart-des-republicains_7907063.html",
        "2026-03-31")},
    "Mira Markovic": {"source": src(
        "Le Monde", "Présidentielle 2027 : le Parti animaliste annonce la candidature de Mira Markovic",
        "https://www.lemonde.fr/politique/article/2026/10/02/presidentielle-2027-le-parti-animaliste-annonce-la-candidature-de-mira-markovic_6787208_823448.html",
        "2026-10-02")},
    "Benoît Mathieu": {"source": src(
        "Le Monde", "Présidentielle 2027 : à vélo sur les routes de France, la campagne décalée d’un candidat « citoyen »",
        "https://www.lemonde.fr/politique/article/2026/06/14/presidentielle-2027-a-velo-sur-les-routes-de-france-la-campagne-decalee-d-un-candidat-citoyen_6702744_823448.html",
        "2026-06-14")},
    "Jean-Luc Mélenchon": {"source": src(
        "Le Monde", "Jean-Luc Mélenchon annonce être candidat à l’élection présidentielle pour la quatrième fois, sur une ligne toujours plus antisystème",
        "https://www.lemonde.fr/politique/article/2026/05/03/jean-luc-melenchon-annonce-etre-candidat-a-l-election-presidentielle-pour-la-quatrieme-fois-sur-une-ligne-toujours-plus-antisysteme_6685247_823448.html",
        "2026-05-03")},
    "Antoine Mikolajczak": {"source": src(
        "L'Alsace", "Présidentielle 2027. Antoine Mikolajczak, candidat attaché « aux faits » et à « la nuance » de passage à Mulhouse",
        "https://www.lalsace.fr/elections/2026/10/03/antoine-mikolajczak-candidat-attache-aux-faits-et-a-la-nuance",
        "2026-10-03")},
    "Manolo Mlekuz": {"source": src(
        "RMC", "« Si j'arrive à l'Elysée... » : ce candidat pour 2027, âgé de 20 ans, veut être un président « sans pouvoir »",
        "https://rmc.bfmtv.com/actualites/politique/si-j-arrive-a-l-elysee-ce-candidat-pour-2027-age-de-20-ans-veut-etre-un-president-sans-pouvoir_AV-202607030571.html",
        "2026-07-03")},
    "Édouard Philippe": {"source": src(
        "Le Point", "EXCLUSIF. Édouard Philippe : « Je serai candidat à la prochaine élection présidentielle »",
        "https://www.lepoint.fr/politique/exclusif-edouard-philippe-je-serai-candidat-a-la-prochaine-election-presidentielle-03-09-2024-2569359_20.php",
        "2024-09-03")},
    "Florian Philippot": {"source": src(
        "franceinfo", "Présidentielle 2027 : le souverainiste Florian Philippot annonce sa candidature à l'Elysée",
        "https://www.franceinfo.fr/elections/presidentielle/presidentielle-2027-le-souverainiste-florian-philippot-annonce-sa-candidature-a-l-elysee_7993346.html",
        "2026-05-09")},
    "Gilles Platret": {"source": src(
        "BFMTV", "Présidentielle 2027: le maire divers droite de Chalon-sur-Saône Gilles Platret annonce sa candidature",
        "https://www.bfmtv.com/politique/elections/presidentielle/presidentielle-2027-le-maire-divers-droite-de-chalon-sur-saone-gilles-platret-annonce-sa-candidature_AN-202610090630.html",
        "2026-10-09")},
    "Natacha Polony": {"source": src(
        "Le Figaro", "Présidentielle 2027 : «Je suis candidate», annonce la journaliste Natacha Polony",
        "https://www.lefigaro.fr/elections/presidentielles/presidentielle-2027-je-suis-candidate-annonce-la-journaliste-natacha-polony-20261014",
        "2026-10-14")},
    "Bruno Retailleau": {"source": src(
        "franceinfo", "Présidentielle 2027 : Bruno Retailleau largement désigné candidat par les adhérents du parti Les Républicains",
        "https://www.franceinfo.fr/politique/les-republicains/presidentielle-2027-bruno-retailleau-largement-designe-candidat-par-les-adherents-du-parti-les-republicains_7949957.html",
        "2026-04-19")},
    "Fabien Roussel": {"source": src(
        "Le Figaro", "Présidentielle 2027 : adoubé par ses militants, le communiste Fabien Roussel officialise sa candidature en solitaire",
        "https://www.lefigaro.fr/elections/presidentielles/candidats/presidentielle-2027-adoube-par-ses-militants-le-communiste-fabien-roussel-officialise-sa-candidature-en-solitaire-20260906",
        "2026-09-06")},
    # "S'il n'y a pas de primaire, moi j'y vais" (May 12); the united-left primary was
    # abandoned in July, and franceinfo's tracker says he maintains his candidacy.
    "François Ruffin": {"source": src(
        "LCP", "Présidentielle 2027: \"S'il n'y a pas de primaire, moi j'y vais\", annonce François Ruffin",
        "https://lcp.fr/actualites/presidentielle-2027-s-il-n-y-a-pas-de-primaire-moi-j-y-vais-annonce-francois-ruffin",
        "2026-05-12")},
    # Les Écologistes' members vote on Dec. 10-13 on keeping her candidacy or joining a
    # left alliance.
    "Marine Tondelier": {"source": src(
        "franceinfo", "La patronne des Ecologistes, Marine Tondelier, se déclare candidate à l'élection présidentielle de 2027",
        "https://www.franceinfo.fr/elections/presidentielle/la-patronne-des-ecologistes-marine-tondelier-se-declare-candidate-a-l-election-presidentielle-de-2027_7568824.html",
        "2025-10-22")},
    "Éric Zemmour": {"missing": {"franceinfo"}, "source": src(
        "BFMTV", "« Je serai candidat » : Éric Zemmour annonce sur BFMTV qu'il se présentera à l'élection présidentielle",
        "https://www.bfmtv.com/politique/elections/presidentielle/je-serai-candidat-eric-zemmour-annonce-sur-bfmtv-qu-il-se-presentera-a-l-election-presidentielle_AV-202609170947.html",
        "2026-09-17")},
    # Not in Wikipedia's table on Nov. 2; listed by franceinfo's tracker, which counts only
    # people who "ont officiellement et publiquement annoncé leur candidature".
    "Juan Branco": {"article": "Juan Branco", "party": "Les Ruches", "missing": {"wikipedia"},
                    "role": "Avocat, fondateur du mouvement Les Ruches", "source": TRACKER},
    "Jean-François Legendre": {"article": None, "party": "À nous maintenant", "missing": {"wikipedia"},
                               "role": "Ancien chef d’entreprise", "source": TRACKER},
    "Augustin Billetdoux": {"article": None, "party": None, "missing": {"wikipedia"},
                            "role": "Auteur, cadre dans une ONG", "source": TRACKER},
    "Christian Collovati": {"article": None, "party": None, "missing": {"wikipedia"},
                            "role": "Ancien officier de marine", "source": TRACKER},
    "Erwan Rohou": {"article": None, "party": "Mouvement écologiste indépendant", "missing": {"wikipedia"},
                    "role": "Trésorier du Mouvement écologiste indépendant", "source": src(
        "RCF Alsace", "Présidentielles : le Mouvement Écologiste indépendant lance sa campagne depuis Strasbourg",
        "https://www.rcf.fr/articles/actualite/presidentielles-le-mouvement-ecologiste-independant-lance-sa-campagne-a",
        "2026-09-11")},
}

# People who are not running: polls test them, or a tracker lists them, but they have
# not declared, withdrew, rallied to someone else or lost a primary. The reason is shown
# on the candidates page, with the source. `listed` names a tracker known to still list
# them, so the daily cross-check doesn't flag it again.
NOT_RUNNING = {
    "Bernard Cazeneuve": {"status": "rallied", "to": "Raphaël Glucksmann", "listed": {"wikipedia"},
        "fr": "A déclaré au Figaro qu’il « aidera » Raphaël Glucksmann à remporter la présidentielle (21 octobre 2026).",
        "en": "Told Le Figaro he will “help” Raphaël Glucksmann win the presidential election (Oct. 21, 2026).",
        "source": src("Le Figaro", "Bernard Cazeneuve au Figaro : «Emmanuel Macron n’est pas responsable de tout, mais il l’est de l’essentiel»",
                      "https://www.lefigaro.fr/elections/presidentielles/bernard-cazeneuve-au-figaro-emmanuel-macron-n-est-pas-responsable-de-tout-mais-il-l-est-de-l-essentiel-20261021",
                      "2026-10-21")},
    "Dominique de Villepin": {"status": "not-declared",
        "fr": "Dit « se battre pour être candidat » et cherche ses parrainages, sans avoir déclaré sa candidature.",
        "en": "Says he is “fighting to be a candidate” and is gathering sponsorships, without having declared.",
        "source": src("franceinfo", "Présidentielle 2027 : \"Je me bats pour être candidat\", déclare Dominique de Villepin, qui revendique \"plusieurs centaines\" de parrainages",
                      "https://www.franceinfo.fr/elections/presidentielle/presidentielle-2027-je-me-bats-pour-etre-candidat-declare-dominique-de-villepin-qui-revendique-plusieurs-centaines-de-parrainages_8169629.html",
                      "2026-08-30")},
    "François Hollande": {"status": "not-declared",
        "fr": "N’a pas déclaré de candidature ; il dit qu’il se prononcera en décembre ou en janvier.",
        "en": "Hasn’t declared; he says he will decide in December or January.",
        "source": src("LCP", "Présidentielle 2027: la liste des candidats déjà en lice et des prétendants",
                      "https://lcp.fr/actualites/presidentielle-2027-la-liste-des-candidats-deja-en-lice-et-des-pretendants-436373",
                      "2026-10-14")},
    "Jordan Bardella": {"status": "not-declared",
        "fr": "Marine Le Pen est la candidate du Rassemblement national ; les sondeurs testent encore Jordan Bardella à sa place.",
        "en": "Marine Le Pen is the Rassemblement national’s candidate; pollsters still test Jordan Bardella in her place.",
        "source": DECLARED["Marine Le Pen"]["source"]},
    "Jean Lassalle": {"status": "not-declared", "listed": {"franceinfo"},
        "fr": "A lancé en juillet une cagnotte « pour pouvoir être de nouveau candidat » ; il n’a pas déclaré sa candidature depuis.",
        "en": "Started a fundraiser in July “to be able to run again”; he hasn’t declared since.",
        "source": src("franceinfo", "Présidentielle 2027 : Jean Lassalle lance une cagnotte pour pouvoir être de nouveau candidat à l'élection",
                      "https://www.franceinfo.fr/elections/presidentielle/presidentielle-2027-jean-lassalle-lance-une-cagnotte-pour-pouvoir-etre-de-nouveau-candidat-a-l-election_8102522.html",
                      "2026-07-15")},
    **{name: {"status": "lost-primary", "to": "Raphaël Glucksmann",
              "fr": "A perdu la primaire socialiste du 11 octobre 2026, remportée par Raphaël Glucksmann.",
              "en": "Lost the Socialist primary of Oct. 11, 2026, which Raphaël Glucksmann won.",
              "source": DECLARED["Raphaël Glucksmann"]["source"]}
       for name in ("Olivier Faure", "Ségolène Royal", "Jérôme Guedj", "Emmanuel Maurel")},
    "Clémentine Autain": {"status": "withdrawn",
        "fr": "A renoncé en juillet 2026, après l’échec du projet de primaire unitaire de la gauche.",
        "en": "Withdrew in July 2026, after the united-left primary was abandoned.",
        "source": TRACKER},
    "Lydie Massard": {"status": "withdrawn",
        "fr": "A renoncé début septembre 2026.",
        "en": "Withdrew in early September 2026.",
        "source": TRACKER},
}

STATUSES = {"declared", "rallied", "not-declared", "lost-primary", "withdrawn"}


def check():
    assert not set(DECLARED) & set(NOT_RUNNING), set(DECLARED) & set(NOT_RUNNING)
    for name, d in {**DECLARED, **NOT_RUNNING}.items():
        s = d["source"]
        assert s["url"].startswith("https://"), name
        assert len(s["date"]) == 10 and s["date"] <= CHECKED_ON, name
        assert s["title"] and s["outlet"], name
    for name, d in NOT_RUNNING.items():
        assert d["status"] in STATUSES, name
        assert d["fr"] and d["en"], name
        if "to" in d:
            assert d["to"] in DECLARED, name


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    check()
    print(f"{len(DECLARED)} declared candidates and {len(NOT_RUNNING)} people not running, checked {CHECKED_ON}")
