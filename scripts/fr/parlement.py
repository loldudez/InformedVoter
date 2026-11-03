"""Build data/fr/parlement.json: who sits in France's Parliament, seat by seat, for the
half-circle charts on #/fr/parlement.

Sources, read once a day by scripts/refresh_all.py:
  * The Assemblée nationale's open data (Licence Ouverte): every sitting deputy with
    their group, their party of attachment, their constituency and their seat, the
    group presidents, the Bureau's president and the current government (AMO10,
    "députés actifs, mandats actifs, organes").
  * The Sénat's open data (Licence Ouverte): every sitting senator with their group,
    department, renewal series and seat (senat.fr/api-senat/senateurs.json), and the
    Bureau's functions (data.senat.fr, ODSEN_GENERAL.csv).
  * French Wikipedia's table of each chamber's groups: each group's president and its
    declared position (majority, minority or opposition), which the chambers' files
    don't carry.
  * Wikidata: the President of the Republic (France's P35), the Prime Minister (P6) and
    the chambers' presidents (P488), with their photos, each checked against the
    chambers' own data (the government's name, the presidency's label, the Bureaus).

Colors: a group takes the color of the party most of its members belong to (the
Assembly's data gives each deputy's party; for the Senate, each group's Wikipedia
infobox lists its parties, set below by group code). A group whose party has no color
of its own is gray, and groups sharing a color get a different seat shape, so no new
colors are needed. Groups run left to right: in the Assembly by where their members
sit (the median seat number, which runs from right to left), in the Senate by each
group's stated position.

If a chamber's files can't be read, the previous file is kept.

    py scripts/fr/parlement.py
"""

import csv
import io
import json
import re
import statistics
import sys
import unicodedata
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import frwiki  # noqa: E402
from frwiki import W  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
ROOT = frwiki.ROOT
OUT = ROOT / "data" / "fr" / "parlement.json"
MAPS = ROOT / "data" / "fr" / "maps"

# The Assembly's file sits under the legislature's number; a newer legislature (after a
# dissolution) is tried first.
AN_ZIP = ("https://data.assemblee-nationale.fr/static/openData/repository/{leg}/amo/"
          "deputes_actifs_mandats_actifs_organes/AMO10_deputes_actifs_mandats_actifs_organes.json.zip")
AN_LEGISLATURES = (18, 17)
SENAT_JSON = "https://www.senat.fr/api-senat/senateurs.json"
SENAT_CSV = "https://data.senat.fr/data/senateurs/ODSEN_GENERAL.csv"
AN_PAGE = "Assemblée nationale (France)"
SENAT_PAGE = "Sénat (France)"

# Seats in each chamber, set by the electoral code; seats without a member are vacant.
SEATS = {"an": 577, "senat": 348}

# A party's name -> its color on the site (css/styles.css, --fr-*). Parties not listed
# here are gray. "Ensemble ! (majorité présidentielle)" is the party of attachment of
# Renaissance's and the MoDem's deputies.
PARTY_COLORS = [
    (r"France insoumise", "lfi"), (r"Parti communiste", "pcf"), (r"[ÉE]cologistes", "le"),
    (r"Parti socialiste", "ps"), (r"Ensemble|Renaissance|Mouvement d[ée]mocrate", "ens"),
    (r"^Horizons", "hor"), (r"Les R[ée]publicains", "lr"), (r"Rassemblement national", "rn"),
    (r"Reconqu[êe]te", "rec"),
]
# Senate groups by the Senate's code, from each group's Wikipedia infobox ("Affiliation
# partisane", first party listed; checked Nov. 2, 2026): Les Républicains, Parti
# socialiste, Parti communiste français, Les Écologistes, Renaissance (RDPI), Horizons
# (Les Indépendants) and the Rassemblement national (UNT). The Union centriste (UDI
# first), the RDSE (Parti radical de gauche first) and senators in no group are gray.
SENAT_COLORS = {"UMP": "lr", "SOC": "ps", "CRC": "pcf", "GEST": "le", "LREM": "ens", "RTLI": "hor", "UNT": "rn"}
# Left to right by each group's stated position in its Wikipedia infobox: radical left
# (CRCE-K), left (GEST), centre-left to left (SER), centre-left to centre-right (RDSE),
# third way and centre (RDPI), centre to centre-right (UCI), centre-right (Les
# Indépendants), right (Les Républicains), far right (UNT); groups not listed go before
# the senators in no group.
SENAT_ORDER = ["CRC", "GEST", "SOC", "RDSE", "LREM", "UC", "RTLI", "UMP", "UNT"]
SHAPES = ["circle", "square", "diamond", "triangle"]


def fetch(url, timeout=120):
    req = urllib.request.Request(url, headers={"User-Agent": W.UA, "Accept-Language": "fr"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read(), r.headers.get("Last-Modified")


def fold(s):
    """Lowercase, no accents, no punctuation: "Groupe Les Indépendants - République" ->
    "groupe les independants republique"."""
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    return " ".join(re.findall(r"[a-z0-9]+", s))


def party_color(name):
    return next((key for pat, key in PARTY_COLORS if re.search(pat, name or "", re.I)), "other")


def regions():
    """Department code -> region name, from the map files."""
    deps = json.loads((MAPS / "departements.json").read_text(encoding="utf-8"))["features"]
    regs = {f["id"]: f["properties"]["name"] for f in json.loads((MAPS / "regions.json").read_text(encoding="utf-8"))["features"]}
    return {f["id"]: regs.get(f["properties"]["reg"]) for f in deps}


def wiki_groups(title):
    """{folded code or name: {"code", "name", "president", "position"}} from a chamber's
    table of groups on French Wikipedia (the one whose header says "Positionnement")."""
    html, t, rev = frwiki.page(title)
    out = {}
    for tb in W.tables(html):
        rows = tb["rows"]
        if not rows or "Positionnement" not in " ".join(W.text(c) for r in rows[:2] for c in r):
            continue
        for r in rows[2:]:
            cells = [" ".join(W.text(c).split()) for c in r]
            if len(cells) < 5 or not cells[1] or cells[1].startswith("Total"):
                continue
            g = {"code": cells[1], "name": cells[2], "president": cells[-2] or None, "position": cells[-1] if cells[-1] not in ("", "/") else None}
            out[fold(g["code"])] = g
            out[fold(g["name"])] = g
        break
    return out, {"title": t, "url": "https://fr.wikipedia.org/wiki/" + t.replace(" ", "_"), "revid": rev}


def match_wiki(wg, code, name):
    if fold(code) in wg:
        return wg[fold(code)]
    n = fold(re.sub(r"^Groupe\s+(du\s+|de\s+l.)?", "", name or "", flags=re.I))
    return next((g for k, g in wg.items() if k and n and (k.startswith(n[:40]) or n.startswith(k[:40]))), None)


def bureau_role(fn):
    """A Bureau function, from either chamber's wording ("Vice-Président",
    "Vice-présidente du Sénat", "Questeure du Sénat"...): "vp", "quaestor", "secretary"."""
    fn = fold(fn)
    return next((code for word, code in (("vice presiden", "vp"), ("questeur", "quaestor"), ("secretaire", "secretary")) if word in fn), None)


def shapes_and_order(groups):
    """Set each group's seat shape: groups sharing a color get circle, square, diamond...
    by size. `groups` is already in left-to-right order."""
    by_color = {}
    for g in sorted(groups, key=lambda g: -g["seats"]):
        n = by_color.setdefault(g["color"], 0)
        g["shape"] = SHAPES[min(n, len(SHAPES) - 1)]
        by_color[g["color"]] += 1
    return groups


def assembly(wg, reg_of):
    data, modified, leg, errors = None, None, None, []
    for leg in AN_LEGISLATURES:
        try:
            data, modified = fetch(AN_ZIP.format(leg=leg))
            z = zipfile.ZipFile(io.BytesIO(data))
            if sum(1 for n in z.namelist() if "/acteur/" in n) >= 400:
                break
            errors.append(f"legislature {leg}: too few deputies")
        except Exception as e:  # noqa: BLE001 - try the next legislature, then give up
            errors.append(f"legislature {leg}: {e}")
        data = None
    if not data:
        raise SystemExit(f"the Assemblée nationale's open data couldn't be read ({'; '.join(errors)}); keeping the old file")
    organes, acteurs = {}, []
    for n in z.namelist():
        j = json.loads(z.read(n))
        if "organe" in j:
            organes[j["organe"]["uid"]] = j["organe"]
        elif "acteur" in j:
            acteurs.append(j["acteur"])

    def mandats(a):
        m = a["mandats"]["mandat"]
        return [x for x in (m if isinstance(m, list) else [m]) if not x.get("dateFin")]

    def ref(m):
        r = (m.get("organes") or {}).get("organeRef")
        return r[0] if isinstance(r, list) else r

    members, president, checks = [], None, []
    for a in acteurs:
        cur = mandats(a)
        seat_m = next((m for m in cur if m["typeOrgane"] == "ASSEMBLEE"), None)
        gp = next((m for m in cur if m["typeOrgane"] == "GP"), None)
        if not seat_m or not gp:
            continue
        pp = next((m for m in cur if m["typeOrgane"] == "PARPOL"), None)
        ident = a["etatCivil"]["ident"]
        lieu = (seat_m.get("election") or {}).get("lieu") or {}
        place = (seat_m.get("mandature") or {}).get("placeHemicycle")
        # A group president also keeps a current "Membre" mandate, so read them all.
        quals = [((x.get("infosQualite") or {}).get("codeQualite") or "").lower() for x in cur if x["typeOrgane"] == "GP"]
        bureau = [(x.get("infosQualite") or {}).get("codeQualite") or "" for x in cur
                  if x["typeOrgane"] == "BUREAU" and organes.get(ref(x), {}).get("libelleAbrev") == "BURAN"]
        m = {
            "n": f"{ident['prenom']} {ident['nom']}", "f": ident.get("civ") == "Mme",
            "g": organes[ref(gp)]["libelleAbrev"], "p": organes.get(ref(pp), {}).get("libelle") if pp else None,
            "dep": lieu.get("numDepartement"), "depName": lieu.get("departement"),
            "circo": int(lieu["numCirco"]) if (lieu.get("numCirco") or "").isdigit() else None,
            # Regions by the map's names (the Assembly writes "Ile-de-France"); overseas
            # collectivities and French people abroad have none.
            "reg": reg_of.get(lieu.get("numDepartement")), "seat": int(place) if (place or "").isdigit() else None,
        }
        if any("appar" in q for q in quals):
            m["app"] = "A"
        if any(q.startswith("présiden") for q in quals):
            m["role"] = "group-president"
        if bureau_role(" ".join(bureau)):
            m["bureau"] = bureau_role(" ".join(bureau))
        if any(q in ("Président", "Présidente") for q in bureau):
            m["role"] = "president"
            president = m
        members.append(m)

    groups = []
    for code in sorted({m["g"] for m in members}):
        org = next(o for o in organes.values() if o["codeType"] == "GP" and o["libelleAbrev"] == code)
        mine = [m for m in members if m["g"] == code]
        parties = {}
        for m in mine:
            if m["p"]:
                parties[m["p"]] = parties.get(m["p"], 0) + 1
        top = max(parties, key=parties.get) if parties else None
        short = org.get("libelleAbrege") or code  # "EcoS", "Dem", "UDR" (ids ECOS, DEM, UDDPLR)
        w = match_wiki(wg, short, org["libelle"]) or {}
        lead = next((m["n"] for m in mine if m.get("role") == "group-president"), None) or w.get("president")
        if w.get("president") and lead and fold(w["president"]) != fold(lead):
            checks.append({"fr": f"Assemblée : Wikipédia donne {w['president']} comme président(e) du groupe {short}, les données de l’Assemblée {lead}.",
                           "en": f"Assembly: Wikipedia names {w['president']} as the {short} group's president, the Assembly's data {lead}."})
        seats = sorted(m["seat"] for m in mine if m["seat"] is not None)
        groups.append({
            "id": code, "short": short, "name": org["libelle"],
            "color": "other" if code == "NI" or not top else party_color(top),
            "party": top if code != "NI" else None, "seats": len(mine), "president": lead,
            "position": w.get("position"), "median": statistics.median(seats) if seats else 0,
        })
    # Seat numbers run from the right of the chamber to the left; the deputies in no
    # group come last.
    groups.sort(key=lambda g: (g["id"] == "NI", -g["median"]))
    for g in groups:
        del g["median"]
    order = {g["id"]: i for i, g in enumerate(groups)}
    members.sort(key=lambda m: (order[m["g"]], -(m["seat"] or 0)))

    gov = next((o for o in organes.values() if o["codeType"] == "GOUVERNEMENT" and not (o.get("viMoDe") or {}).get("dateFin")), None)
    presrep = next((o for o in organes.values() if o["codeType"] == "PRESREP" and not (o.get("viMoDe") or {}).get("dateFin")), None)
    chamber = {
        "seats": SEATS["an"], "majority": SEATS["an"] // 2 + 1, "legislature": leg,
        "president": president, "groups": shapes_and_order(groups), "members": members,
        "sources": [{"title": "Assemblée nationale, données ouvertes : députés en exercice",
                     "url": "https://data.assemblee-nationale.fr/acteurs/deputes-en-exercice", "date": modified}],
    }
    gov_info = {"label": (gov.get("libelleAbrege") or "").title().replace(" Ii", " II").replace(" Iii", " III") if gov else None,
                "since": (gov.get("viMoDe") or {}).get("dateDebut") if gov else None,
                "presidency": presrep.get("libelle") if presrep else None}
    return chamber, gov_info, checks


def senate(wg, reg_of):
    try:
        sen = json.loads(fetch(SENAT_JSON)[0])
        raw, modified = fetch(SENAT_CSV)
    except Exception as e:  # noqa: BLE001
        raise SystemExit(f"the Sénat's open data couldn't be read ({e}); keeping the old file")
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError:  # the file has been Windows-1252 so far
        text = raw.decode("cp1252", "replace")
    # Lines starting with "%" repeat the query that made the file.
    rows = list(csv.DictReader(io.StringIO("\n".join(l for l in text.splitlines() if not l.startswith("%")))))
    bureau = {r["Matricule"]: r["Fonction au Bureau du Sénat"] for r in rows if r.get("État") == "ACTIF" and r.get("Fonction au Bureau du Sénat")}
    if len(sen) < 300:
        raise SystemExit(f"only {len(sen)} senators read; keeping the old file")
    members, president, checks = [], None, []
    groups = {}
    for s in sen:
        g = s["groupe"]
        groups.setdefault(g["code"], {"id": g["code"], "short": g["libelleCourt"], "name": g["libelle"], "seats": 0})["seats"] += 1
        dep = (s.get("circonscription") or {}).get("code")
        # "Français établis hors de France (Série 1)": the series is kept apart.
        place = re.sub(r"\s*\(S[ée]rie \d\)$", "", (s.get("circonscription") or {}).get("libelle") or "")
        m = {"n": f"{s['prenom']} {s['nom']}", "f": bool(s.get("feminise")), "g": g["code"],
             "dep": dep, "depName": place, "reg": reg_of.get(dep), "seat": s.get("siege"), "serie": s.get("serie")}
        if g.get("codeTypeAppartenance") in ("A", "R"):
            m["app"] = g["codeTypeAppartenance"]
        fn = bureau.get(s["matricule"], "")
        if fn.startswith("Président"):
            m["role"] = "president"
            president = m
        elif bureau_role(fn):
            m["bureau"] = bureau_role(fn)
        members.append(m)
    out = []
    for code, g in groups.items():
        w = match_wiki(wg, g["short"], g["name"]) or {}
        # Senators in no group have a delegate, not a president.
        lead = w.get("president") if code != "NI" else None
        if lead:
            hit = next((m for m in members if m["g"] == code and fold(m["n"]) == fold(lead)), None)
            if hit and hit.get("role") != "president":
                hit["role"] = "group-president"
            elif not hit:
                checks.append({"fr": f"Sénat : {lead}, président(e) du groupe {g['short']} selon Wikipédia, n’est pas dans ce groupe d’après le Sénat.",
                               "en": f"Senate: {lead}, the {g['short']} group's president per Wikipedia, isn't in that group per the Senate."})
        out.append({**g, "short": "NI" if code == "NI" else g["short"], "color": SENAT_COLORS.get(code, "other"),
                    "president": lead, "position": w.get("position")})
    rank = {c: i for i, c in enumerate(SENAT_ORDER)}
    out.sort(key=lambda g: (g["id"] == "NI", rank.get(g["id"], len(rank))))
    order = {g["id"]: i for i, g in enumerate(out)}
    members.sort(key=lambda m: (order[m["g"]], m["n"]))
    chamber = {
        "seats": SEATS["senat"], "majority": SEATS["senat"] // 2 + 1,
        "president": president, "groups": shapes_and_order(out), "members": members,
        "sources": [{"title": "Sénat, liste des sénateurs", "url": "https://www.senat.fr/senateurs/senatl.html", "date": modified},
                    {"title": "Sénat, données ouvertes", "url": "https://data.senat.fr/les-senateurs/", "date": modified}],
    }
    return chamber, checks


def wikidata_people():
    """{"president", "pm", "an", "senat"}: {"qid", "name", "article"} from Wikidata."""
    q = W.api({"action": "query", "prop": "pageprops", "ppprop": "wikibase_item", "redirects": 1,
               "titles": f"{AN_PAGE}|{SENAT_PAGE}"}, base=frwiki.FR)["query"]
    items = {p["title"]: (p.get("pageprops") or {}).get("wikibase_item") for p in q["pages"]}
    an_q, sen_q = items.get(AN_PAGE), items.get(SENAT_PAGE)
    ents = W.api({"action": "wbgetentities", "ids": "|".join(x for x in ("Q142", an_q, sen_q) if x), "props": "claims"},
                 base=frwiki.WD)["entities"]

    def current(qid, prop):
        """The claim with no end date, preferred first: (item, start day or None)."""
        claims = [c for c in ((ents.get(qid) or {}).get("claims") or {}).get(prop) or []
                  if c.get("rank") != "deprecated" and not (c.get("qualifiers") or {}).get("P582")]
        start = lambda c: (((c.get("qualifiers") or {}).get("P580") or [{}])[0].get("datavalue") or {}).get("value", {}).get("time", "")  # noqa: E731
        claims.sort(key=lambda c: (c.get("rank") == "preferred", start(c)), reverse=True)
        if not claims:
            return None, None
        return ((claims[0]["mainsnak"].get("datavalue") or {}).get("value") or {}).get("id"), start(claims[0])[1:11] or None

    who = {"president": current("Q142", "P35"), "pm": current("Q142", "P6"), "an": current(an_q, "P488"), "senat": current(sen_q, "P488")}
    ids = [x for x in dict.fromkeys(q for q, _ in who.values()) if x]
    # Many people's names now sit only in the multilingual label ("mul"), Macron's among
    # them; the French article's title is the last resort.
    people = W.api({"action": "wbgetentities", "ids": "|".join(ids), "props": "labels|sitelinks|claims",
                    "languages": "fr|mul", "sitefilter": "frwiki"}, base=frwiki.WD)["entities"] if ids else {}
    out = {}
    for role, (qid, since) in who.items():
        e = people.get(qid) if qid else None
        if not e:
            continue
        labels = e.get("labels") or {}
        article = ((e.get("sitelinks") or {}).get("frwiki") or {}).get("title")
        name = (labels.get("fr") or labels.get("mul") or {}).get("value") or re.sub(r"\s*\(.*\)$", "", article or "")
        # Sex or gender (P21), for the French title ("Première ministre"); anything other
        # than these four leaves the title in its neutral form.
        sex = next((((c["mainsnak"].get("datavalue") or {}).get("value") or {}).get("id") for c in (e.get("claims") or {}).get("P21") or []), None)
        f = {"Q6581097": False, "Q2449503": False, "Q6581072": True, "Q1052281": True}.get(sex)
        if name:
            out[role] = {"qid": qid, "name": name, "article": article, "since": since, "f": f}
    return out


def wiki_or_last(title, key, last):
    """wiki_groups(), or, when French Wikipedia can't be read, the groups' presidents and
    positions from the last build."""
    try:
        return wiki_groups(title)
    except Exception as e:  # noqa: BLE001
        print(f"French Wikipedia unreadable for {title} ({e}); keeping the groups' presidents and positions from the last build")
        ch = ((last or {}).get("chambers") or {}).get(key) or {}
        wg = {}
        for g in ch.get("groups", []):
            entry = {"code": g["short"], "name": g["name"], "president": g.get("president"), "position": g.get("position")}
            wg[fold(g["short"])] = wg[fold(g["name"])] = entry
        return wg, next((s for s in ch.get("sources", []) if s.get("revid")), None)


def main():
    try:
        last = json.loads(OUT.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        last = None
    reg_of = regions()
    an_wiki, an_src = wiki_or_last(AN_PAGE, "an", last)
    sen_wiki, sen_src = wiki_or_last(SENAT_PAGE, "senat", last)
    an, gov, checks = assembly(an_wiki, reg_of)
    sen, sen_checks = senate(sen_wiki, reg_of)
    checks += sen_checks
    an["sources"] += [an_src] if an_src else []
    sen["sources"] += [sen_src] if sen_src else []

    try:
        wd = wikidata_people()
        photos = frwiki.photos([p["article"] for p in wd.values() if p.get("article")])
        people = {role: {"name": p["name"], "f": p["f"], "article": p["article"], "since": p["since"], "photo": photos.get(p["article"]),
                         "source": f"https://www.wikidata.org/wiki/{p['qid']}"} for role, p in wd.items()}
    except Exception as e:  # noqa: BLE001 - the last build's officials stand in
        print(f"Wikidata unreadable ({e}); keeping the officials from the last build")
        people = {role: p for role, p in ((last or {}).get("officials") or {}).items() if role in ("president", "pm")}
        for key, ch in (("an", an), ("senat", sen)):
            old = (((last or {}).get("chambers") or {}).get(key) or {}).get("president") or {}
            if old.get("n"):
                people[key] = {"name": old["n"], "article": old.get("article"), "photo": old.get("photo")}
    officials = {}
    for role in ("president", "pm"):
        p = people.get(role)
        if not p:
            continue
        # The chambers' data must agree: the presidency's label names the President, the
        # government's name carries the Prime Minister's.
        ok = fold(p["name"]) in fold(gov["presidency"] or "") if role == "president" else \
            fold(p["name"]).split()[-1] in fold(gov["label"] or "")
        if not ok:
            checks.append({"fr": f"Wikidata donne {p['name']} ({role}), ce que les données de l’Assemblée ne confirment pas.",
                           "en": f"Wikidata gives {p['name']} ({role}), which the Assembly's data doesn't confirm."})
            continue
        officials[role] = p
    if gov["label"]:
        officials["government"] = {"name": gov["label"], "since": gov["since"]}
    for key, ch in (("an", an), ("senat", sen)):
        p, mine = people.get(key), ch["president"]
        if mine and p and fold(p["name"]) == fold(mine["n"]):
            mine["photo"] = p.get("photo")
            mine["article"] = p.get("article")

    data = {"updated": datetime.now(timezone.utc).isoformat(timespec="minutes"), "officials": officials,
            "chambers": {"an": an, "senat": sen}, "checks": checks}
    OUT.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT).as_posix()}: Assemblée {len(an['members'])}/{an['seats']} in {len(an['groups'])} groups, "
          f"Sénat {len(sen['members'])}/{sen['seats']} in {len(sen['groups'])} groups; "
          f"{', '.join(f'{k} {v['name']}' for k, v in officials.items())}; {len(checks)} checks")
    for g in an["groups"] + sen["groups"]:
        print(f"  {g['id']:<8} {g['seats']:>3} {g['color']:<5} {g['shape']:<8} {g.get('president') or '':<22} {g.get('position') or ''}")
    for c in checks:
        print("  check:", c["en"])


if __name__ == "__main__":
    main()
