"""French Wikipedia, Wikidata and Commons for the France section, through the same
paced client as the U.S. refresh (`scripts/lib/wikitables.py`), so both stay under
Wikimedia's request limits together.

French pages are cached by revision in `data/cache/wiki-fr/`; photo details from
Wikidata and Commons (scripts/lib/wikiphotos.py, shared with the U.S. pages) are cached
for a day in `data/cache/wiki-fr/media.json` (three batched requests cover fifty
people), so a new photo or credit shows up the next day.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "lib"))
import wikitables as W  # noqa: E402
import wikiphotos  # noqa: E402

FR = "https://fr.wikipedia.org/w/api.php"
WD = wikiphotos.WIKIDATA
COMMONS = wikiphotos.COMMONS
CACHE = ROOT / "data" / "cache" / "wiki-fr"
MEDIA = CACHE / "media.json"
MEDIA_DAYS = 0.8  # under a day, so each daily run rereads them


def page(title):
    """(html, title, revid) of a French Wikipedia page's latest revision."""
    q = W.api({"action": "query", "prop": "revisions", "rvprop": "ids", "titles": title, "redirects": 1}, base=FR)["query"]
    p = q["pages"][0]
    if p.get("missing"):
        raise LookupError(f"French Wikipedia has no page {title!r}")
    rev = p["revisions"][0]["revid"]
    CACHE.mkdir(parents=True, exist_ok=True)
    slug = W._slug(p["title"])
    path = CACHE / f"{slug}.{rev}.html"
    if path.exists():
        W.stats["cached"] += 1
        return path.read_text(encoding="utf-8"), p["title"], rev
    d = W.api({"action": "parse", "oldid": rev, "prop": "text", "disableeditsection": 1}, base=FR)
    text = d["parse"]["text"]
    for old in CACHE.glob(f"{slug}.*.html"):
        old.unlink()
    path.write_text(text, encoding="utf-8")
    return text, p["title"], rev


def photos(article_titles, width=320):
    """{French article title: {"thumb", "file", "page", "artist", "license", "licenseUrl"}}
    for each person's Wikidata image (P18), with the credit Commons requires.
    People without an image on Wikidata are left out."""
    return wikiphotos.photos(article_titles, api=FR, cache_file=MEDIA, max_age_days=MEDIA_DAYS, width=width, lang="fr")
