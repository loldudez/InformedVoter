"""Build data/photos.json: photos of the U.S. candidates whose name links to a Wikipedia
article, shown on their cards in gray with their credit, as in the France section.

A candidate's article is the one their name links to on the race's Wikipedia page
(`wiki` in data/races.json: every incumbent and most well-known challengers have one).
The photo is that article's Wikidata image (P18) on Wikimedia Commons, with its author
and license (scripts/lib/wikiphotos.py), kept only when the item is a person and a U.S.
citizen wherever Wikidata gives a citizenship, and only when the article's title carries
the candidate's last name, so a link to a namesake or to the wrong article brings no
photo. Everyone else keeps their initials.

Run once a day by scripts/refresh_all.py, after the races. Answers are cached for a
week in data/cache/wiki/photos.json, shared with update_congress.py, so a day's run asks
Wikimedia only about new candidates and week-old answers (three requests per fifty
people).

    py scripts/update_photos.py
"""

import json
import re
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "lib"))
import wikitables as W  # noqa: E402
import wikiphotos  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
RACES = ROOT / "data" / "races.json"
OUT = ROOT / "data" / "photos.json"
CACHE = ROOT / "data" / "cache" / "wiki" / "photos.json"
CACHE_DAYS = 7
WIKI = "https://en.wikipedia.org/wiki/"
SUFFIXES = {"jr", "sr", "ii", "iii", "iv", "v"}


def words(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    return re.findall(r"[a-z0-9]+", s)


def last_name(name):
    w = [x for x in words(name) if x not in SUFFIXES]
    return w[-1] if w else ""


def title_of(url):
    """The article title in a Wikipedia link (".../wiki/Dan_Sullivan_(U.S._senator)" ->
    "Dan Sullivan (U.S. senator)"); None for red links (index.php?...&redlink=1)."""
    if not url or not url.startswith(WIKI):
        return None
    return unquote(url[len(WIKI):].split("#")[0]).replace("_", " ") or None


def main():
    races = json.loads(RACES.read_text(encoding="utf-8"))["races"]
    cands = [c for r in races for c in r["candidates"] if title_of(c.get("wiki"))]
    titles = sorted({title_of(c["wiki"]) for c in cands})
    found = wikiphotos.photos(titles, api=W.API, cache_file=CACHE, max_age_days=CACHE_DAYS, country="Q30")
    photos, skipped = {}, []
    for c in cands:
        t = title_of(c["wiki"])
        if t not in found:
            continue
        if last_name(c["name"]) not in words(t):
            skipped.append(f"{c['name']} links to {t!r}")
            continue
        photos[c["wiki"]] = wikiphotos.slim(found[t])
    OUT.write_text(json.dumps({"updated": datetime.now(timezone.utc).isoformat(timespec="minutes"), "photos": photos},
                              ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT).as_posix()}: photos for {len(photos)} of the {len(cands)} candidates "
          f"with a Wikipedia article ({W.stats['requests']} requests)")
    for s in skipped:
        print("  skipped, last name not in the article's title:", s)


if __name__ == "__main__":
    main()
