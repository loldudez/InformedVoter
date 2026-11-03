"""Build data/fr/presidentielle-2027.json: the 2027 French presidential election's
dates, declared candidates (with photos and their credits) and every published poll
for both rounds.

Sources, all read through the paced client in frwiki.py:
  * French Wikipedia's "Élection présidentielle française de 2027": the dates (from the
    infobox) and the table of declared candidates.
  * French Wikipedia's "Liste de sondages sur l'élection présidentielle française de
    2027": first-round polls (one row per line-up of candidates tested) and each
    second-round match-up. Every poll links to its official notice at the Commission
    des sondages, which is kept as the poll's source; a row without that link is
    left out, like the U.S. rule that unverified polls stay out of the average.
  * Wikidata and Commons: each person's photo and its credit.
  * The Commission des sondages' list of notices, read every day. A row Wikipedia links
    to the pollster's own page gets its notice from this list (same pollster, filed
    within ten days of the fieldwork, the only such notice), and a vote-intention notice
    newer than every poll on Wikipedia's list is flagged as a poll to add.
  * Who is running: Wikipedia's table, cross-checked every day against franceinfo's
    tracker of declared candidates and the hand check in `candidats_2027.py` (see there
    for how they combine). Only declared candidates are shown and averaged; people polls
    test without a candidacy (Hollande, Villepin, Bardella) keep their poll values in the
    line-ups but nowhere else, and second-round match-ups need two declared candidates.

Averages are plain and published as such: a poll counts once however many line-ups
it tested (a candidate's value in a poll is the median of the line-ups that include
them, preferring line-ups made only of declared candidates), over the 30 days before
the latest poll. There is no win probability: with a dozen candidates and two rounds, a
model would invent precision.

A value cell can name someone tested in that column's place ("6,5 / Hollande (PS)" under
Glucksmann); the value goes to that person, never to the column's candidate.

    py scripts/fr/update_presidentielle.py
"""

import json
import re
import statistics
import sys
import urllib.request
from datetime import date, datetime, timedelta, timezone
from html import unescape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import candidats_2027 as K  # noqa: E402
import frwiki  # noqa: E402
from frwiki import W  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
ROOT = frwiki.ROOT
OUT = ROOT / "data" / "fr" / "presidentielle-2027.json"
FI_CACHE = ROOT / "data" / "cache" / "fr" / "franceinfo-candidats.json"
MAIN = "Élection présidentielle française de 2027"
POLLS = "Liste de sondages sur l'élection présidentielle française de 2027"
WINDOW_DAYS = 30
# The Commission des sondages lists every notice filed; vote-intention polls say "IV" or
# belong to a named presidential series. Notices about other elections are left out.
NOTICES = "https://www.commission-des-sondages.fr/notices/"
NOTICE_IV = re.compile(r"\bIV\b|intentions? de vote|barom[eè]tre (?:de l.)?[ée]lection|presitrack", re.I)
NOTICE_OTHER = re.compile(r"municipal|l[ée]gislativ|europ[ée]en|r[ée]gional|d[ée]partemental|s[ée]natorial|r[ée]f[ée]rendum", re.I)

MONTHS = {"janv": 1, "janvier": 1, "févr": 2, "février": 2, "fevrier": 2, "mars": 3, "avr": 4, "avril": 4, "mai": 5,
          "juin": 6, "juil": 7, "juillet": 7, "août": 8, "aout": 8, "sept": 9, "septembre": 9, "oct": 10,
          "octobre": 10, "nov": 11, "novembre": 11, "déc": 12, "décembre": 12, "decembre": 12}
MONTH_RE = "|".join(sorted(MONTHS, key=len, reverse=True))


def slug(s):
    s = unescape(s).lower()
    for a, b in (("àâä", "a"), ("éèêë", "e"), ("îï", "i"), ("ôö", "o"), ("ùûü", "u"), ("ç", "c")):
        for ch in a:
            s = s.replace(ch, b)
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def parse_end(text, year_hint):
    """End date of "21-22 octobre", "30 sept.-2 oct. 2026" or "1er-3 novembre 2026"."""
    t = unescape(text).lower().replace("1er", "1")
    hits = re.findall(rf"(\d{{1,2}})\s*({MONTH_RE})\.?(?:\s+(\d{{4}}))?", t)
    if not hits:
        return None
    d, m, y = hits[-1]
    try:
        return date(int(y or year_hint), MONTHS[m], int(d)).isoformat()
    except ValueError:
        return None


def number(text):
    t = unescape(text).strip().replace(" ", "").replace("\xa0", "").replace(" ", "")
    if not t or t in ("—", "-", "–", "?"):
        return None
    if t.startswith("<"):
        return 0.5  # "<1": published as under one percent
    m = re.match(r"^(\d+(?:,\d+)?)", t)
    return float(m.group(1).replace(",", ".")) if m else None


def head_cand(cell):
    """("Le Pen", "RN", "Marine Le Pen") from a column header like "Le Pen / (RN)"."""
    txt = W.text(cell)
    m = re.search(r"\(([^)]+)\)", txt)
    abbr = m.group(1).strip() if m else None
    short = txt.split("\n")[0].split("(")[0].strip()
    # The candidate's own link names them; a header whose only link is the party has none.
    last = short.split()[-1] if short else ""
    article = next((l["title"] for l in cell["links"]
                    if l["title"] and not l["href"].startswith("http") and last and last in l["title"]), None)
    return short, abbr, article, [l["title"] for l in cell["links"] if l["title"]]


def notice_number(url):
    m = re.search(r"/(\d{4,6})-[^/]*\.pdf$", url or "")
    return int(m.group(1)) if m else None


def notice_finder(listed, html_text):
    """find(cell, end) -> (URL, number) of the poll's official notice, or (None, None).
    Wikipedia links most polls to their notice; a row linked to the pollster's own page
    instead gets the one vote-intention notice in the Commission's list from that
    pollster, filed within ten days after the fieldwork ended and not already another
    poll's."""
    used = {int(n) for n in re.findall(r"commission-des-sondages\.fr/notices/files/notices/[^\"]*?/(\d{4,6})-", html_text)}
    pool = [n for n in listed or [] if NOTICE_IV.search(n["title"]) and not NOTICE_OTHER.search(n["title"])
            and n["number"] not in used]
    squash = lambda s: re.sub(r"[^a-z0-9]", "", slug(s))  # noqa: E731
    matched = {}

    def filed(n, end):
        m = re.search(rf"(\d{{1,2}})(?:er)?\s+({MONTH_RE})\w*\s*$", n["title"], re.I)
        if not m:
            return None
        month = MONTHS[m.group(2).lower()]
        year = end.year + (1 if month < end.month - 6 else 0)
        try:
            return date(year, month, int(m.group(1)))
        except ValueError:
            return None

    def find(cell, end):
        for l in cell["links"]:
            if "commission-des-sondages.fr" in l["href"]:
                return l["href"], notice_number(l["href"])
        who = squash(W.text(cell))
        if not who or not end:
            return None, None
        if (who, end) not in matched:  # the rows of one poll share its notice
            taken = {n["number"] for n in matched.values() if n}
            day = date.fromisoformat(end)
            hits = [n for n in pool if n["number"] not in taken and who in squash(n["title"])
                    and (d := filed(n, day)) and 0 <= (d - day).days <= 10]
            matched[(who, end)] = hits[0] if len(hits) == 1 else None
            if len(hits) == 1:
                print(f"  notice {hits[0]['number']} ({hits[0]['title']}) matched to {W.text(cell)}, fieldwork ending {end}")
        n = matched[(who, end)]
        return (n["url"], n["number"]) if n else (None, None)
    return find


def stand_in(cell):
    """A value cell can name someone else tested in that column's place: "6,5 / Hollande
    (PS)" under Glucksmann. Returns (article, short, abbr) for that person, ("", "", None)
    when a name is there but links nowhere, or None when the cell is a plain number."""
    lines = [x.strip() for x in W.text(cell).split("\n") if x.strip()]
    label = next((x for x in lines[1:] if re.search(r"[A-Za-zÀ-ÿ]{3}", x) and not x.startswith("[")), None)
    if not label:
        return None
    m = re.search(r"\(([^)]+)\)", label)
    short = label.split("(")[0].strip()
    last = short.split()[-1] if short else ""
    art = next((l["title"] for l in cell["links"]
                if l["title"] and not l["href"].startswith("http") and last and last in l["title"]), "")
    return art, short, (m.group(1).strip() if m else None)


def others(cell):
    """[(value, name, article)] from an "Autres" cell, which lists further candidates as
    value then name ("<1 / Bouamrane"); the text can run a name into the next value
    ("Ruffin1,5"), so it is read as alternating numbers and names."""
    links = [l["title"] for l in cell["links"] if l["title"] and not l["href"].startswith("http")]
    out, value = [], None
    for tok in re.findall(r"<\s*1|\d+(?:[,.]\d+)?|[^\d<]+", W.text(cell)):
        tok = tok.strip(" \n/\xa0")
        if not tok:
            continue
        if re.match(r"^(<\s*1|\d)", tok):
            value = number(tok)
        elif value is not None:
            name = tok.split("(")[0].strip()
            art = next((l for l in links if name and name.split()[-1] in l), None)
            if art:
                out.append((value, name, art))
            value = None
    return out


def section_year(title):
    m = re.search(r"(20\d\d)", title)
    return int(m.group(1)) if m else date.today().year


def first_round(html_text, people, parties, notice):
    polls = {}
    for sec in W.split_sections(html_text):
        if sec["level"] != 5 and not re.search(r"semestre 2026", sec["title"]):
            continue
        if not re.search(r"2026", sec["title"]) or "second tour" in sec["title"].lower():
            continue
        year = section_year(sec["title"])
        for t in W.tables(sec["html"]):
            rows = t["rows"]
            if len(rows) < 4 or W.text(rows[0][0]) != "Sondeur":
                continue
            heads = rows[1]
            cols = {}
            for j, c in enumerate(heads):
                if j < 3 or W.text(c) in ("Autres", "Sondeur", "Date", "Échantillon"):
                    continue
                short, abbr, article, _ = head_cand(c)
                if not article:
                    continue
                cols[j] = article
                people.setdefault(article, {"short": short, "abbr": abbr})
                if abbr and len(c["links"]) > 1:
                    parties.setdefault(abbr, c["links"][1]["title"])
            other_col = next((j for j, c in enumerate(heads) if W.text(c) == "Autres"), None)
            for row in rows[3:]:
                end = parse_end(W.text(row[1]), year)
                url, num = notice(row[0], end)
                if not url or not end:
                    continue
                scen = {}
                for j, art in cols.items():
                    v = number(W.text(row[j]))
                    if v is None:
                        continue
                    sub = stand_in(row[j])
                    if sub is None:
                        scen[art] = v
                    elif sub[0]:
                        # The value is the stand-in's, never the column's candidate's.
                        scen[sub[0]] = v
                        people.setdefault(sub[0], {"short": sub[1], "abbr": sub[2]})
                if other_col is not None:
                    for v, name, art in others(row[other_col]):
                        scen[art] = v
                        people.setdefault(art, {"short": name, "abbr": None})
                if len(scen) < 3:
                    continue
                key = url
                p = polls.setdefault(key, {"pollster": W.text(row[0]), "url": url, "notice": num, "dates": f"{W.text(row[1])} {year}" if not re.search(r"\d{4}", W.text(row[1])) else W.text(row[1]),
                                           "end": end, "n": int(number(W.text(row[2])) or 0) or None, "scenarios": []})
                if scen not in p["scenarios"]:
                    p["scenarios"].append(scen)
    return sorted(polls.values(), key=lambda p: p["end"], reverse=True)


def second_round(html_text, people, parties, notice):
    out = []
    parent = ""
    for sec in W.split_sections(html_text):
        if sec["level"] == 3:
            parent = sec["title"]  # "candidats déclarés ou pressentis" or "candidats absents au premier tour"
        m = re.match(r"Hypothèse (.+?) [–-] (.+)$", sec["title"])
        if not m:
            continue
        for t in W.tables(sec["html"])[:1]:
            rows = t["rows"]
            if len(rows) < 4:
                continue
            heads = rows[1]
            cand_cols = []
            for j, c in enumerate(heads[3:], start=3):
                short, abbr, article, _ = head_cand(c)
                if article:
                    cand_cols.append((j, article))
                    people.setdefault(article, {"short": short, "abbr": abbr})
                    if abbr and len(c["links"]) > 1:
                        parties.setdefault(abbr, c["links"][1]["title"])
            if len(cand_cols) != 2:
                continue
            (ja, a), (jb, b) = cand_cols
            polls = []
            for row in rows[3:]:
                end = parse_end(W.text(row[1]), section_year(W.text(row[1])) if re.search(r"\d{4}", W.text(row[1])) else date.today().year)
                url, num = notice(row[0], end)
                va, vb = number(W.text(row[ja])), number(W.text(row[jb]))
                if url and end and va is not None and vb is not None:
                    polls.append({"pollster": W.text(row[0]), "url": url, "notice": num, "dates": W.text(row[1]), "end": end,
                                  "n": int(number(W.text(row[2])) or 0) or None, "a": va, "b": vb})
            if polls:
                polls.sort(key=lambda p: p["end"], reverse=True)
                out.append({"a": a, "b": b, "label": f"{m.group(1)} – {m.group(2)}",
                            "absent": "absent" in parent.lower(), "polls": polls})
    return out


def window(polls):
    if not polls:
        return []
    last = max(date.fromisoformat(p["end"]) for p in polls)
    start = last - timedelta(days=WINDOW_DAYS)
    return [p for p in polls if date.fromisoformat(p["end"]) > start]


def r1_average(polls, running):
    """The average of declared candidates (`running`, by article). A candidate's value in
    a poll is the median of the line-ups that include them and only declared candidates;
    line-ups with someone who isn't running (Hollande in the Socialist slot, Villepin
    among "Autres") count only for a candidate the poll tested nowhere else."""
    recent = window(polls)
    per = {}
    for p in recent:
        clean, every = {}, {}
        for s in p["scenarios"]:
            ok = all(a in running for a in s)
            for art, v in s.items():
                if art in running:
                    every.setdefault(art, []).append(v)
                    if ok:
                        clean.setdefault(art, []).append(v)
        # A candidate tested only alongside someone who isn't running keeps that value.
        for art, vs in every.items():
            per.setdefault(art, []).append(statistics.median(clean.get(art) or vs))
    avg = [{"article": art, "avg": round(statistics.fmean(vs), 1), "lo": min(vs), "hi": max(vs), "polls": len(vs)}
           for art, vs in per.items()]
    avg.sort(key=lambda x: -x["avg"])
    return {"from": min((p["end"] for p in recent), default=None), "to": max((p["end"] for p in recent), default=None),
            "polls": len(recent), "candidates": avg}


def r2_average(polls):
    recent = window(polls) or polls[:3]
    return {"a": round(statistics.fmean(p["a"] for p in recent), 1), "b": round(statistics.fmean(p["b"] for p in recent), 1),
            "polls": len(recent), "from": min(p["end"] for p in recent), "to": max(p["end"] for p in recent)}


def dates(html_text):
    txt = re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", html_text[:60000])))
    m = re.search(rf"(\d{{1,2}})\s*({MONTH_RE})\s+(20\d\d)\s*\(\s*1\s*er\s*tour\)\s*(\d{{1,2}})\s*({MONTH_RE})\s+(20\d\d)\s*\(\s*2\s*d\s*tour\)", txt)
    if not m:
        raise SystemExit("could not find the two round dates in the infobox")
    r1 = date(int(m.group(3)), MONTHS[m.group(2)], int(m.group(1)))
    r2 = date(int(m.group(6)), MONTHS[m.group(5)], int(m.group(4)))
    return r1.isoformat(), r2.isoformat()


def declared(html_text):
    sec = W.section_by_title(html_text, "Candidats déclarés")
    out = {}
    for t in W.tables(sec or ""):
        for row in t["rows"][1:]:
            cell = row[0]
            links = [l for l in cell["links"] if l["title"] and not l["href"].startswith("http")]
            lines = [x.strip() for x in W.text(cell).split("\n") if x.strip()]
            if not lines:
                continue
            # The first line starts with a hidden sort key: "Arthaud, Nathalie Nathalie Arthaud".
            first = lines[0]
            m = re.match(r"^([^,]+),\s*(\S+(?:-\S+)?)\s+(.+)$", first)
            disp = m.group(3).strip() if m else first
            disp = re.sub(r"\s*\(\d+ ans\)", "", disp).strip()
            if not disp or re.search(r"\d", disp):
                continue
            # A candidate without an article is keyed by name and links nowhere.
            person = [l for l in links if l["title"].split(" (")[0] in disp or disp in l["title"]]
            article = person[0]["title"] if person else disp
            party = next((l["title"] for l in links if l not in person[:1]), None)
            role = W.text(row[3]).split("\n")[0].strip() if len(row) > 3 else ""
            slogan = W.text(row[4]).split("\n")[0].strip() if len(row) > 4 else ""
            slogan = "" if slogan.startswith(("Campagne", "Positions")) else slogan
            out[article] = {"name": re.sub(r"\s*\(\d+ ans\)", "", disp), "party": party, "wiki": bool(person),
                            "role": role if role != "Aucune" else "", "slogan": slogan}
    return out


def notices():
    """The Commission des sondages' list of notices, newest first: [{"number", "title",
    "url"}], or None when the page can't be read (no poll cross-check today)."""
    try:
        req = urllib.request.Request(NOTICES, headers={"User-Agent": W.UA, "Accept-Language": "fr"})
        with urllib.request.urlopen(req, timeout=60) as r:
            page_text = r.read().decode("utf-8", "replace")
    except Exception as e:  # noqa: BLE001 - any failure means "no check today"
        print(f"the Commission des sondages' notices are unreadable ({e})")
        return None
    out = [{"number": int(num), "title": " ".join(unescape(title).split()),
            "url": "https://www.commission-des-sondages.fr" + href}
           for href, num, title in re.findall(r'<a href="(/notices/medias/fichiers/add/\d+)"[^>]*>\s*(\d{4,6})\s+([^<]+)</a>', page_text)]
    return sorted(out, key=lambda n: -n["number"]) or None


def poll_check(cds, r1, r2):
    """Is Wikipedia's list behind? Vote-intention notices at the Commission des sondages
    (`cds`, from notices()) newer than every poll here are polls still to be added (they
    wait for Wikipedia, since a notice carries no results to read). Titles are the
    pollsters' own, so the match is a heuristic: "IV" and the named presidential series,
    other elections left out."""
    have = {p["notice"] for p in r1 + [q for h in r2 for q in h["polls"]] if p.get("notice")}
    newest = max(have, default=0)
    missing = [n for n in cds or [] if n["number"] > newest and NOTICE_IV.search(n["title"])
               and not NOTICE_OTHER.search(n["title"])]
    checks = [{"fr": f"La Commission des sondages a publié la notice {n['number']} ({n['title']}), "
                     "que Wikipédia ne liste pas encore : sondage à reporter.",
               "en": f"The Commission des sondages published notice {n['number']} ({n['title']}), "
                     "which Wikipedia doesn't list yet: a poll still to be added."} for n in missing]
    if cds is None:
        checks.append({"fr": "La liste des notices de la Commission des sondages n’a pas pu être lue : pas de recoupement des sondages aujourd’hui.",
                       "en": "The Commission des sondages' list of notices couldn't be read: no poll cross-check today."})
    return {"url": NOTICES, "read": cds is not None, "newest": newest, "missing": missing}, checks


def franceinfo():
    """{name key: {"name", "party", "status": "candidat" | "retire"}} from franceinfo's tracker
    of declared candidates, a JSON list embedded in the page. A failed read falls back to
    the last copy if it is under a week old; otherwise None (no cross-check today)."""
    try:
        req = urllib.request.Request(K.FRANCEINFO_TRACKER, headers={"User-Agent": W.UA, "Accept-Language": "fr"})
        with urllib.request.urlopen(req, timeout=60) as r:
            page_text = r.read().decode("utf-8", "replace")
        m = re.search(r'<script[^>]*class="if-cand__data"[^>]*>(.*?)</script>', page_text, re.S)
        rows = json.loads(unescape(m.group(1))) if m else []
        out = {}
        for x in rows:
            name = f"{x.get('prenom') or ''} {x.get('nom') or ''}".strip()
            if name and x.get("statut") in ("candidat", "retire"):
                out[name_key(name)] = {"name": name, "party": x.get("parti"), "status": x["statut"]}
        if len(out) < 15:
            raise ValueError(f"only {len(out)} people found")
        FI_CACHE.parent.mkdir(parents=True, exist_ok=True)
        FI_CACHE.write_text(json.dumps({"at": datetime.now(timezone.utc).isoformat(), "people": out},
                                       ensure_ascii=False, indent=1), encoding="utf-8")
        return out
    except Exception as e:  # noqa: BLE001 - any failure means "no fresh copy"
        print(f"franceinfo's tracker unreadable ({e}); using the last copy if recent")
        try:
            old = json.loads(FI_CACHE.read_text(encoding="utf-8"))
            if datetime.now(timezone.utc) - datetime.fromisoformat(old["at"]) < timedelta(days=7):
                return old["people"]
        except (OSError, ValueError, KeyError):
            pass
        return None


def name_key(name):
    """First and last word of a name without accents, so "Sylvain Pierre Durif" meets
    "Sylvain Durif" and "Edouard Philippe" meets "Édouard Philippe"."""
    parts = slug(name.split(" (")[0]).split("-")
    return f"{parts[0]} {parts[-1]}"


def statuses(wiki_people, fi):
    """{name key: (status, source, note)} for everyone in Wikipedia's table, the hand check
    or franceinfo's tracker, plus the checks to settle by hand (see candidats_2027.py)."""
    checks = []
    fi_ok = fi is not None
    fi = fi or {}
    hand = {name_key(n): ("declared", n, d) for n, d in K.DECLARED.items()}
    hand.update({name_key(n): (d["status"], n, d) for n, d in K.NOT_RUNNING.items()})
    wiki = {name_key(n) for n in wiki_people}
    out = {}
    for k in set(hand) | wiki | {k for k, v in fi.items() if v["status"] == "candidat"}:
        f = fi.get(k, {}).get("status")
        name = hand[k][1] if k in hand else (fi.get(k, {}).get("name") or next(n for n in wiki_people if name_key(n) == k))
        both = k in wiki and f == "candidat"
        if k in hand and hand[k][0] == "declared":
            if f == "retire":
                out[k] = ("withdrawn", K.TRACKER, None)
                checks.append({"fr": f"franceinfo indique que {name} s’est retiré(e) : à vérifier.",
                               "en": f"franceinfo marks {name} as withdrawn: to check."})
            elif fi_ok and k not in wiki and f is None:
                out[k] = ("unconfirmed", None, None)
                checks.append({"fr": f"{name} n’est plus listé(e) ni par Wikipédia ni par franceinfo : à vérifier.",
                               "en": f"Neither Wikipedia nor franceinfo lists {name} any more: to check."})
            else:
                out[k] = ("declared", hand[k][2]["source"], None)
                missing = hand[k][2].get("missing", set())
                if fi_ok and f is None and "franceinfo" not in missing:
                    checks.append({"fr": f"{name} est candidat(e) (vérifié), mais absent(e) de la liste de franceinfo.",
                                   "en": f"{name} is a candidate (checked) but missing from franceinfo’s list."})
                if k not in wiki and "wikipedia" not in missing:
                    checks.append({"fr": f"{name} est candidat(e) (vérifié), mais absent(e) de la liste de Wikipédia.",
                                   "en": f"{name} is a candidate (checked) but missing from Wikipedia’s list."})
        elif k in hand:
            d = hand[k][2]
            if both:
                out[k] = ("declared", K.TRACKER, None)
                checks.append({"fr": f"{name} figure désormais sur les deux listes de candidats : à vérifier dans candidats_2027.py.",
                               "en": f"{name} is now on both candidate lists: check and update candidats_2027.py."})
            else:
                out[k] = (d["status"], d["source"], {"fr": d["fr"], "en": d["en"]})
                for which, listed in (("Wikipédia", k in wiki), ("franceinfo", f == "candidat")):
                    if listed and which.lower().replace("é", "e") not in d.get("listed", set()):
                        checks.append({"fr": f"{which} liste {name}, qui n’est pas candidat(e) d’après la vérification du {K.CHECKED_ON}.",
                                       "en": f"{which} lists {name}, who isn’t a candidate as checked on {K.CHECKED_ON}."})
        elif both or (k in wiki and not fi_ok):
            out[k] = ("declared", K.TRACKER if both else None, None)
            checks.append({"fr": f"Nouveau candidat : {name}. À vérifier et à ajouter à candidats_2027.py avec sa source.",
                           "en": f"New candidate: {name}. Check and add to candidats_2027.py with a source."})
        else:
            out[k] = ("unconfirmed", None, None)
            which = "Wikipédia" if k in wiki else "franceinfo"
            checks.append({"fr": f"Seul {which} liste {name} comme candidat(e) : à vérifier.",
                           "en": f"Only {which} lists {name} as a candidate: to check."})
    if not fi_ok:
        checks.append({"fr": "La liste de franceinfo n’a pas pu être lue : pas de double vérification aujourd’hui.",
                       "en": "franceinfo’s list couldn’t be read: no cross-check today."})
    return out, checks


def main():
    main_html, main_title, main_rev = frwiki.page(MAIN)
    poll_html, poll_title, poll_rev = frwiki.page(POLLS)
    r1_date, r2_date = dates(main_html)
    decl = declared(main_html)
    people, parties = {}, {}
    cds = notices()
    find = notice_finder(cds, poll_html)
    r1 = first_round(poll_html, people, parties, find)
    r2 = second_round(poll_html, people, parties, find)
    if not r1 or not decl:
        raise SystemExit(f"parsed {len(r1)} first-round polls and {len(decl)} declared candidates; keeping the old file")
    abbr_for_party = {v: k for k, v in parties.items()}
    fi = franceinfo()
    status, checks = statuses({d["name"]: art for art, d in decl.items()}, fi)
    polls_checked, poll_checks = poll_check(cds, r1, r2)
    checks += poll_checks

    # Everyone in Wikipedia's table, the hand check's declared list or the polls; people
    # without a Wikipedia article are keyed by name and link nowhere.
    extra = {(d.get("article") or n): n for n, d in K.DECLARED.items() if "party" in d}
    articles = list(dict.fromkeys(list(decl) + list(extra) + list(people)))
    pics = frwiki.photos([a for a in articles if a not in extra or K.DECLARED[extra[a]].get("article")])
    cands = []
    for art in articles:
        d, p = decl.get(art, {}), people.get(art, {})
        hand = K.DECLARED.get(extra.get(art, ""), {})
        name = d.get("name") or extra.get(art) or art.split(" (")[0]
        st, source, note = status.get(name_key(name), ("not-declared", None, None))
        cands.append({
            "id": slug(name), "article": art, "name": name,
            "short": p.get("short") or name.split()[-1],
            "party": p.get("abbr") or abbr_for_party.get(d.get("party")) or None,
            "partyName": d.get("party") or hand.get("party") or parties.get(p.get("abbr")),
            "declared": st == "declared", "status": st, "statusSource": source, "statusNote": note,
            "wiki": d.get("wiki", bool(hand.get("article", True))),
            "role": d.get("role") or hand.get("role", ""), "slogan": d.get("slogan", ""),
            "photo": pics.get(art),
        })
    ids = {c["article"]: c["id"] for c in cands}
    running = {c["article"] for c in cands if c["declared"]}
    # Poll tables can link one person under two titles ("Olivier Faure" and "Olivier
    # Faure (homme politique)"): both map to one id, listed once.
    seen = set()
    cands = [c for c in cands if not (c["id"] in seen or seen.add(c["id"]))]

    avg = r1_average(r1, running)
    for a in avg["candidates"]:
        a["id"] = ids[a.pop("article")]
    for p in r1:
        p["scenarios"] = [{ids[k]: v for k, v in s.items()} for s in p["scenarios"]]
    # Second-round match-ups between two declared candidates only.
    duels = []
    for h in r2:
        if h["a"] in running and h["b"] in running:
            duels.append({"id": f"{ids[h['a']]}--{ids[h['b']]}", "a": ids[h["a"]], "b": ids[h["b"]], "label": h["label"],
                          "polls": h["polls"], "average": r2_average(h["polls"])})
    duels.sort(key=lambda d: (-len(window(d["polls"])), d["label"]))

    data = {
        "meta": {
            "updated": datetime.now(timezone.utc).isoformat(timespec="minutes"),
            "sources": [
                {"title": main_title, "url": "https://fr.wikipedia.org/wiki/" + main_title.replace(" ", "_"), "revid": main_rev},
                {"title": poll_title, "url": "https://fr.wikipedia.org/wiki/" + poll_title.replace(" ", "_"), "revid": poll_rev},
            ],
            "windowDays": WINDOW_DAYS,
            # Candidacies: checked one by one on this date (candidats_2027.py), then
            # cross-checked every day against Wikipedia's table and franceinfo's tracker.
            "candidatesChecked": K.CHECKED_ON,
            "crossCheck": {"title": K.TRACKER["title"], "url": K.FRANCEINFO_TRACKER, "read": fi is not None},
            # Polls: Wikipedia's list against the Commission des sondages' notices.
            "pollCheck": polls_checked,
            "checks": checks,
        },
        "rounds": {"r1": r1_date, "r2": r2_date},
        "parties": parties,
        "candidates": cands,
        "r1": {"average": avg, "polls": r1},
        "r2": duels,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    top = ", ".join(f"{c['id']} {c['avg']}" for c in avg["candidates"][:6])
    print(f"wrote {OUT.relative_to(ROOT).as_posix()}: rounds {r1_date} / {r2_date}; {len(running)} declared candidates "
          f"of {len(cands)} people ({len(pics)} photos, {len(checks)} checks to settle); {len(r1)} first-round polls, "
          f"{avg['polls']} in the last {WINDOW_DAYS} days ({top}); {len(duels)} second-round match-ups")
    for c in checks:
        print("  check:", c["en"])


if __name__ == "__main__":
    main()
