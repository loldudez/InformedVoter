"""Build data/fr/partis.json: France's main parties, who leads them (with a photo and
its credit), where they place themselves, their stated ideology, their seats, their
official site and their 2027 candidates.

Everything about a party comes from its French Wikipedia infobox, read each day like
the polls, so a leadership change shows up on its own; the photos come from Wikidata
and Commons through frwiki.py. The list of parties and their colors is set here.

    py scripts/fr/partis.py
"""

import json
import re
import sys
from datetime import datetime, timezone
from html import unescape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import frwiki  # noqa: E402
from frwiki import W  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
ROOT = frwiki.ROOT
OUT = ROOT / "data" / "fr" / "partis.json"
PRES = ROOT / "data" / "fr" / "presidentielle-2027.json"

# (abbreviation, French Wikipedia page, English name), roughly from left to right.
PARTIES = [
    ("LFI", "La France insoumise", "France Unbowed"),
    ("PCF", "Parti communiste français", "French Communist Party"),
    ("LE", "Les Écologistes", "The Ecologists"),
    ("PS", "Parti socialiste (France)", "Socialist Party"),
    ("PP", "Place publique (parti politique)", "Public Place"),
    ("RE", "Renaissance (parti)", "Renaissance"),
    ("MoDem", "Mouvement démocrate (France)", "Democratic Movement"),
    ("HOR", "Horizons (parti politique)", "Horizons"),
    ("LR", "Les Républicains", "The Republicans"),
    ("UDR", "Union des droites pour la République", "Union of the Right for the Republic"),
    ("RN", "Rassemblement national", "National Rally"),
    ("REC", "Reconquête (parti politique)", "Reconquest"),
]
LEADER_LABELS = ["Président", "Présidente", "Coprésidents", "Co-présidents", "Coprésidentes", "Co-présidente", "Coprésident",
                 "Premier secrétaire", "Première secrétaire", "Secrétaire national", "Secrétaire nationale",
                 "Coordinateur", "Coordinatrice", "Secrétaire général", "Secrétaire générale"]


def clean(s):
    s = re.sub(r"\[\s*(?:\d+|note \d+)\s*\]", "", unescape(s))
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"(\s*,)+\s*(?=[,)]|$)", "", s)       # commas left by removed footnotes
    s = re.sub(r"\(\s+", "(", re.sub(r"\s+\)", ")", s))
    return re.sub(r"\s+,", ",", s).strip(" ,;'")


def infobox(html_text):
    """{label: {"text", "links": [titles], "ext": [urls], "items": [text]}} from the first infobox,
    including rows of tables nested inside it."""
    m = re.search(r'<table class="infobox(?:&#95;|_)v[23]', html_text)
    if not m:
        return {}
    depth, end = 0, None
    for t in re.finditer(r"<(/?)table", html_text[m.start():]):
        depth += -1 if t.group(1) else 1
        if depth == 0:
            end = m.start() + t.end()
            break
    box_html = html_text[m.start():end]
    out = {}
    for row in re.finditer(r"<tr[^>]*>(.*?)</tr>", box_html, re.S):
        cells = re.findall(r"<(t[hd])[^>]*>(.*?)</\1>", row.group(1), re.S)
        if len(cells) != 2:
            continue
        label = clean(re.sub(r"<[^>]+>", " ", cells[0][1]))
        val = cells[1][1]
        val_nosup = re.sub(r"<sup.*?</sup>", "", val, flags=re.S)
        links = [unescape(t) for t in re.findall(r'<a [^>]*href="/wiki/[^"]+"[^>]*title="([^"]+)"', val_nosup)]
        ext = [unescape(u) for u in re.findall(r'<a [^>]*class="external[^"]*"[^>]*href="(https?://[^"]+)"', val_nosup)]
        ext += [unescape(u) for u in re.findall(r'<a [^>]*href="(https?://[^"]+)"[^>]*class="external', val_nosup)]
        parts = [clean(re.sub(r"<[^>]+>", " ", p)) for p in re.split(r"<br\s*/?>|</li>", val_nosup)]
        out.setdefault(label, {"text": clean(re.sub(r"<[^>]+>", " ", val_nosup)), "links": links, "ext": ext,
                               "items": [p for p in parts if p], "html": val_nosup})
    return out


# Infobox fields can list a party's past ("Historique : …") or internal currents
# ("Courants internes : …") beside what it is today ("Actuel : …"); keep today's part.
GAP = r"(?:\s|&#160;|&nbsp;|\xa0|<[^>]+>)*"   # spaces, no-break spaces or tags before the colon
OTHER_PART = re.compile(rf"(Historique|Historiquement|Anciennement|Courants?\s+internes?|Tendances?\s+internes?){GAP}:", re.I)


def current_part(html_value):
    m = re.search(rf"Actuel(?:le)?s?{GAP}:", html_value)
    start = m.end() if m else 0
    rest = html_value[start:]
    stop = OTHER_PART.search(rest)
    return rest[:stop.start()] if stop else rest


def current_links(html_value):
    part = current_part(html_value)
    titles = [unescape(t) for t in re.findall(r'<a [^>]*href="/wiki/[^"]+"[^>]*title="([^"]+)"', part)]
    return [t.split(" (")[0] for t in titles if "congrès" not in t.lower()]


def main():
    pres = json.loads(PRES.read_text(encoding="utf-8"))
    parties = []
    for abbr, page, en in PARTIES:
        html_text, title, rev = frwiki.page(page)
        box = infobox(html_text)
        lead_label = next((l for l in LEADER_LABELS if l in box), None)
        leaders = []
        if lead_label:
            v = box[lead_label]
            people = [t for t in v["links"] if not re.search(r"\b(19|20)\d\d\b", t)][:2]
            leaders = [{"role": lead_label, "article": t, "name": t.split(" (")[0]} for t in people]
        ideology = current_links(box["Idéologie"]["html"]) if "Idéologie" in box else []
        position = clean(re.sub(r"<[^>]+>", " ", current_part(box["Positionnement"]["html"]))) if "Positionnement" in box else None
        site = next(iter((box.get("Site web") or {}).get("ext") or []), None)
        seats = clean((box.get("Députés") or {}).get("text", "")) or None
        cands = [c["id"] for c in pres["candidates"] if c.get("partyName") == title and c.get("declared")]
        parties.append({
            "abbr": abbr, "name": title.split(" (")[0], "en": en, "article": title, "revid": rev,
            "leaders": leaders, "founded": clean((box.get("Fondation") or {}).get("text", "")) or None,
            "position": position or None,
            "ideology": list(dict.fromkeys(ideology))[:8], "site": site, "seats": seats, "candidates": cands,
            "source": {"title": f"Wikipédia : {title}", "url": "https://fr.wikipedia.org/wiki/" + title.replace(" ", "_")},
        })
    photos = frwiki.photos([l["article"] for p in parties for l in p["leaders"]])
    for p in parties:
        for l in p["leaders"]:
            l["photo"] = photos.get(l["article"])
    OUT.write_text(json.dumps({"updated": datetime.now(timezone.utc).isoformat(timespec="minutes"), "parties": parties},
                              ensure_ascii=False, indent=1), encoding="utf-8")
    led = sum(1 for p in parties if p["leaders"])
    print(f"wrote {OUT.relative_to(ROOT).as_posix()}: {len(parties)} parties, {led} with a leader, "
          f"{sum(1 for p in parties for l in p['leaders'] if l.get('photo'))} leader photos")


if __name__ == "__main__":
    main()
