"""Photos of real people: each person's Wikidata image (P18) on Wikimedia Commons, with
the author and license Commons requires us to credit. The France section
(scripts/fr/frwiki.py) and the U.S. pages (scripts/update_photos.py, update_congress.py)
both read them here, through the paced client in wikitables.py.

Three batched requests cover fifty people: Wikipedia article -> Wikidata item -> image
file -> thumbnail and credit. Answers are cached in a JSON file per caller for a set
number of days. A photo is kept only when the article's Wikidata item is a person
(P31 human) and, with `country`, a citizen of that country wherever Wikidata gives a
citizenship (P27), so a link to a namesake abroad, or to something that isn't a person,
brings no photo.
"""

import json
import re
import time
from html import unescape
from pathlib import Path

import wikitables as W

WIKIDATA = "https://www.wikidata.org/w/api.php"
COMMONS = "https://commons.wikimedia.org/w/api.php"
HUMAN = "Q5"


def _strip(s):
    """Text of a Commons credit's HTML, without the space a dropped link leaves before
    punctuation ("James086 , original author is ...")."""
    s = re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", s or ""))).strip()
    return re.sub(r" ([,.;:)])", r"\1", s)


def _load(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def _ids(claims, prop):
    """The items a property points to, leaving out deprecated statements."""
    out = set()
    for c in claims.get(prop) or []:
        v = ((c.get("mainsnak") or {}).get("datavalue") or {}).get("value")
        if c.get("rank") != "deprecated" and isinstance(v, dict) and v.get("id"):
            out.add(v["id"])
    return out


def photos(article_titles, *, api, cache_file, max_age_days, width=320, country=None, lang="en"):
    """{article title: {"thumb", "file", "page", "artist", "license", "licenseUrl"}} for
    each person's Wikidata image (P18), with the credit Commons requires. People without
    an image, and articles whose item isn't a person (or, with `country`, a citizen of
    it), are left out."""
    cache = _load(cache_file)
    cutoff = time.time() - max_age_days * 86400
    need = [t for t in dict.fromkeys(article_titles) if (cache.get(t) or {}).get("at", 0) < cutoff]
    if need:
        # Article -> Wikidata item. Titles are followed forward through normalization and
        # redirects, since one batch can ask for a redirect and its target both
        # ("Olivier Faure (homme politique)" and "Olivier Faure").
        items = {}
        for i in range(0, len(need), 50):
            batch = need[i:i + 50]
            q = W.api({"action": "query", "prop": "pageprops", "ppprop": "wikibase_item", "redirects": 1,
                       "titles": "|".join(batch)}, base=api)["query"]
            fwd = {n["from"]: n["to"] for n in q.get("normalized", []) + q.get("redirects", [])}
            qid_of = {p["title"]: (p.get("pageprops") or {}).get("wikibase_item") for p in q.get("pages", [])}
            for t in batch:
                cur, seen = t, set()
                while cur in fwd and cur not in seen:
                    seen.add(cur)
                    cur = fwd[cur]
                if qid_of.get(cur):
                    items[t] = qid_of[cur]
        # Wikidata item -> image file (P18), preferring a "preferred" rank claim.
        files, descs = {}, {}
        qids = list(dict.fromkeys(items.values()))
        for i in range(0, len(qids), 50):
            ents = W.api({"action": "wbgetentities", "ids": "|".join(qids[i:i + 50]), "props": "claims|descriptions",
                          "languages": lang}, base=WIKIDATA)["entities"]
            for qid, e in ents.items():
                claims = e.get("claims") or {}
                descs[qid] = ((e.get("descriptions") or {}).get(lang) or {}).get("value")
                if HUMAN not in _ids(claims, "P31"):
                    continue
                citizen = _ids(claims, "P27")
                if country and citizen and country not in citizen:
                    continue
                for c in sorted(claims.get("P18") or [], key=lambda c: c.get("rank") != "preferred"):
                    v = (c.get("mainsnak") or {}).get("datavalue", {}).get("value")
                    if v and c.get("rank") != "deprecated":
                        files[qid] = v
                        break
        # Image file -> thumbnail and credit.
        info = {}
        names = list(dict.fromkeys(files.values()))
        for i in range(0, len(names), 50):
            batch = names[i:i + 50]
            q = W.api({"action": "query", "prop": "imageinfo", "iiprop": "url|extmetadata", "iiurlwidth": width,
                       "titles": "|".join("File:" + n for n in batch)}, base=COMMONS)["query"]
            fwd = {n["from"]: n["to"] for n in q.get("normalized", [])}
            pages = {p["title"]: p for p in q.get("pages", [])}
            for name in batch:
                p = pages.get(fwd.get("File:" + name, "File:" + name)) or {}
                ii = (p.get("imageinfo") or [None])[0]
                if not ii:
                    continue
                meta = ii.get("extmetadata") or {}
                info[name] = {
                    "thumb": ii.get("thumburl") or ii.get("url"),
                    "file": name,
                    "page": ii.get("descriptionurl"),
                    "artist": _strip((meta.get("Artist") or {}).get("value")),
                    "license": _strip((meta.get("LicenseShortName") or {}).get("value")),
                    "licenseUrl": _strip((meta.get("LicenseUrl") or {}).get("value")) or None,
                }
        now = time.time()
        for t in need:
            qid = items.get(t)
            f = files.get(qid)
            cache[t] = {"at": now, "qid": qid, "desc": descs.get(qid), "photo": info.get(f) if f else None}
        Path(cache_file).parent.mkdir(parents=True, exist_ok=True)
        Path(cache_file).write_text(json.dumps(cache, ensure_ascii=False, indent=1), encoding="utf-8")
    return {t: cache[t]["photo"] for t in article_titles if (cache.get(t) or {}).get("photo")}


def slim(p):
    """What a page needs to show a photo and credit it, without the tracking parameters
    Commons adds to thumbnail links (the bare file is the same)."""
    return {"thumb": (p.get("thumb") or "").split("?")[0], "page": p.get("page"),
            "artist": _strip(p.get("artist")) or None, "license": _strip(p.get("license")) or None}


def cached(cache_file, title):
    """The cache's entry for one article: {"at", "qid", "desc", "photo"} or None."""
    return _load(cache_file).get(title)
