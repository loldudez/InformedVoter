"""Who the people on the "Upcoming elections" pages are (scripts/update_upcoming.py): for
each person whose name links to an English Wikipedia article, the first two sentences
of the article's lead, their Wikidata photo, and a website.

  * The bio is the lead as Wikipedia's TextExtracts gives it (plain text, two sentences),
    shown with a link to the article and its CC BY-SA license.
  * The photo comes from scripts/lib/wikiphotos.py with the race pages' checks
    (scripts/update_photos.py): the item is a person and a U.S. citizen wherever
    Wikidata gives a citizenship.
  * The website is the person's campaign site where a race page lists one (its
    "External links" or a declared-candidates table), else their official website on
    Wikidata (P856, values without an end date, the one Wikidata ranks preferred first:
    Trump's own site before his former office's). A site is kept only when it answers
    and its page shows the person's last name: lapsed campaign domains get resold
    (CLAUDE.md, "Pitfalls"), and old official pages move.

A bio, photo or website is kept only when the article's title carries the person's last
name and its Wikidata item is a person, so a link to a namesake or to the wrong article
brings nothing.

Answers are cached in data/cache/: bios and Wikidata facts for three to four weeks
(spread over a week, so they don't all expire on the same day), photos for a week (the
cache update_photos.py uses), site checks for a week. Wikimedia is read through the
paced client in wikitables.py; campaign sites are fetched directly, eight at a time.
"""

import json
import re
import time
import unicodedata
import urllib.error
import urllib.request
import zlib
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import unquote, urlparse

import wikiphotos
import wikitables as W

ROOT = Path(__file__).resolve().parents[2]
CACHE = ROOT / "data" / "cache"
BIO_CACHE = CACHE / "wiki" / "people.json"
PHOTO_CACHE = CACHE / "wiki" / "photos.json"  # shared with update_photos.py and update_congress.py
SITE_CACHE = CACHE / "sites.json"
SPARQL = "https://query.wikidata.org/sparql"
WIKI = "https://en.wikipedia.org/wiki/"
BIO_DAYS, PHOTO_DAYS, SITE_DAYS = 21, 7, 7
FACTS_V = 2  # Wikidata facts' format: 2 orders websites by rank
# Campaign sites are fetched with a user agent that names itself (the States Newsroom
# sites refuse Python's default one); nothing else about the visitor or the owner is sent.
SITE_UA = "InformedVoterResearch/1.0 (election-information site; checks that campaign links still work)"
SUFFIXES = {"jr", "sr", "ii", "iii", "iv", "v"}
# Where a lapsed domain's visitors are sent. Website builders (godaddysites.com, wixsite.com)
# host real campaigns' sites and aren't on the list; their parked pages fail the name check.
PARKING = re.compile(r"(^|\.)(sedoparking|parkingcrew|bodis|hugedomains|afternic|dan|undeveloped|above|parklogic|"
                     r"domainmarket|buydomains|namebright|porkbun)\.(com|net)$", re.I)
PARKED_TEXT = re.compile(r"\b(this domain (name )?(is|may be) for sale|buy this domain|domain (is )?parked|parked free)\b", re.I)


def words(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    return re.findall(r"[a-z0-9]+", s)


def last_name(name):
    w = [x for x in words(name) if x not in SUFFIXES]
    return w[-1] if w else ""


def title_of(url):
    """The article title in a Wikipedia link; None for anything else (red links too)."""
    if not url or not url.startswith(WIKI):
        return None
    return unquote(url[len(WIKI):].split("#")[0]).replace("_", " ") or None


def _load(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def _save(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    tmp = Path(str(path) + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=0), encoding="utf-8")
    tmp.replace(path)


def _spread(key, days):
    """A cache lifetime of `days` plus up to a week, fixed per entry, so entries read on the
    same day expire on different days."""
    return (days + zlib.crc32(key.encode("utf-8")) % 7) * 86400


# A pronunciation respelling ("SPAN-bur-gər", "jə-NOO-lee-əs", "van HOL-ən"): syllables
# joined by hyphens, one of them in capitals, lowercase ones too (so "R-TX" isn't one).
RESPELL = r"(?=[^;)]*\b[A-Z]{2,})(?=[^;)]*-)(?=[^;)]*[a-zəɪʊʌæɒɔɛ])[A-Za-zəɪʊʌæɒɔɛːˈ'’ -]+?"


def tidy_bio(s):
    """Plain text of a lead: collapse spaces, drop pronunciation respellings ("Nungesser
    ( NUN-ghess-ər; born January 10, 1959)") and the empty brackets IPA guides leave
    behind, and cut at a sentence end past 420 characters. Safe to run twice."""
    if not s:
        return None
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\(\s*(?:" + RESPELL + r"|[A-Z]{2,}[A-Z'’]*)\s*;\s*", "(", s)  # "( SHAHTS; born" too
    s = re.sub(r"\s*\(\s*" + RESPELL + r"\s*\)", "", s)
    s = re.sub(r"\(\s*[;,]?\s*\)", "", s)
    s = re.sub(r"\(\s*[;,]\s*", "(", s)
    s = re.sub(r"\(\s+", "(", s)
    s = re.sub(r"\s+([,.;])", r"\1", s)
    s = re.sub(r"\s{2,}", " ", s).strip()
    if len(s) > 420:
        cut = s.rfind(". ", 0, 420)
        s = s[:cut + 1] if cut > 80 else s[:417].rsplit(" ", 1)[0] + "…"
    return s or None


# Wikipedia: the lead and the Wikidata item ---------------------------------------------

def leads(titles):
    """{title: {"title": resolved title, "qid", "bio"}} for each article."""
    cache = _load(BIO_CACHE)
    now = time.time()
    need = [t for t in dict.fromkeys(titles) if now - (cache.get(t) or {}).get("at", 0) > _spread(t, BIO_DAYS)]
    for i in range(0, len(need), 20):
        batch = need[i:i + 20]
        q = W.api({"action": "query", "prop": "extracts|pageprops", "exintro": 1, "explaintext": 1, "exsentences": 2,
                   "exlimit": 20, "ppprop": "wikibase_item|disambiguation", "redirects": 1, "titles": "|".join(batch)})["query"]
        fwd = {n["from"]: n["to"] for n in q.get("normalized", []) + q.get("redirects", [])}
        pages = {p["title"]: p for p in q.get("pages", [])}
        for t in batch:
            cur, seen = t, set()
            while cur in fwd and cur not in seen:
                seen.add(cur)
                cur = fwd[cur]
            p = pages.get(cur) or {}
            pp = p.get("pageprops") or {}
            ok = not p.get("missing") and "disambiguation" not in pp
            cache[t] = {"at": now, "title": cur, "qid": pp.get("wikibase_item") if ok else None,
                        "bio": tidy_bio(p.get("extract")) if ok else None}
        if i % 200 == 0:
            _save(BIO_CACHE, cache)
    if need:
        _save(BIO_CACHE, cache)
    return {t: cache[t] for t in titles if t in cache}


def facts(qids):
    """{qid: {"human": bool, "sites": [official websites without an end date],
    "parties": [current parties' English names]}} from Wikidata's query service, 100
    items a request."""
    cache = _load(BIO_CACHE)
    store = cache.setdefault("@facts", {})
    now = time.time()
    # Entries cached before websites were ordered by rank ("v" missing) are read again.
    need = [q for q in dict.fromkeys(qids)
            if q and ((store.get(q) or {}).get("v") != FACTS_V or now - (store.get(q) or {}).get("at", 0) > _spread(q, BIO_DAYS))]
    for i in range(0, len(need), 100):
        batch = need[i:i + 100]
        sparql = ("SELECT ?item ?site ?srank ?human ?partyLabel WHERE { VALUES ?item { " + " ".join(f"wd:{q}" for q in batch) + " } "
                  "OPTIONAL { ?item p:P856 ?st . ?st ps:P856 ?site ; wikibase:rank ?srank . FILTER NOT EXISTS { ?st pq:P582 ?end } "
                  "FILTER(?srank != wikibase:DeprecatedRank) } "
                  "OPTIONAL { ?item p:P102 ?pst . ?pst ps:P102 ?party . FILTER NOT EXISTS { ?pst pq:P582 ?pend } "
                  "?party rdfs:label ?partyLabel . FILTER(lang(?partyLabel) = \"en\") } "
                  "BIND(EXISTS { ?item wdt:P31 wd:Q5 } AS ?human) }")
        rows = W.api({"query": sparql}, base=SPARQL)["results"]["bindings"]
        got = {q: {"at": now, "v": FACTS_V, "human": False, "sites": [], "parties": []} for q in batch}
        preferred = {q: [] for q in batch}
        for b in rows:
            q = b["item"]["value"].rsplit("/", 1)[-1]
            if q not in got:
                continue
            got[q]["human"] = b.get("human", {}).get("value") == "true"
            site = (b.get("site") or {}).get("value")
            if site and site not in got[q]["sites"]:
                got[q]["sites"].append(site)
                if (b.get("srank") or {}).get("value", "").endswith("#PreferredRank"):
                    preferred[q].append(site)
            party = (b.get("partyLabel") or {}).get("value")
            if party and party not in got[q]["parties"]:
                got[q]["parties"].append(party)
        for q in batch:  # the website Wikidata ranks preferred first, then the rest
            got[q]["sites"] = preferred[q] + [s for s in got[q]["sites"] if s not in preferred[q]]
        store.update(got)
    if need:
        _save(BIO_CACHE, cache)
    return {q: store[q] for q in qids if q in store}


def party_code(names):
    """'D', 'R', 'L' or 'G' when a person's current parties on Wikidata all say the same
    one (the Minnesota DFL counts as Democratic), else None."""
    codes = set()
    for n in names or []:
        t = n.lower()
        if "republican" in t:
            codes.add("R")
        elif "democratic" in t and ("farmer" in t or "nonpartisan league" in t or t.startswith("democratic")):
            codes.add("D")
        elif t.startswith("libertarian"):
            codes.add("L")
        elif t.startswith("green party"):
            codes.add("G")
        else:
            codes.add("?")
    return codes.pop() if len(codes) == 1 and "?" not in codes else None


# Websites -----------------------------------------------------------------------------

def _fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": SITE_UA, "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.5",
                                               "Accept-Language": "en-US,en;q=0.8"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.geturl(), r.read(1_500_000).decode("utf-8", "replace")


def _check(url, name):
    """{"ok", "final" or "why"}: the page answers and shows the person's last name."""
    last = last_name(name)
    tries = [url] if url.startswith("https://") else ["https://" + url.split("://", 1)[-1], url]
    why = "unreachable"
    for u in tries:
        try:
            final, text = _fetch(u)
        except urllib.error.HTTPError as e:
            why = f"HTTP {e.code}"
            continue
        except Exception as e:  # noqa: BLE001  timeouts, TLS and DNS errors, resets
            why = type(e).__name__
            continue
        host = (urlparse(final).hostname or "").lower()
        if PARKING.search(host):
            return {"ok": False, "why": f"parked at {host}"}
        if PARKED_TEXT.search(text[:20000]):
            return {"ok": False, "why": "a parked domain's page"}
        if last and last not in set(words(text)):
            return {"ok": False, "why": "the page doesn't show the name"}
        start = (urlparse(u).hostname or "").lower().removeprefix("www.")
        # Keep the address as given unless it moved to another site (a campaign's new
        # domain), and never keep a redirect's tracking parameters.
        shown = u if host.removeprefix("www.") == start else final.split("?")[0]
        return {"ok": True, "final": shown}
    return {"ok": False, "why": why}


def check_sites(pairs):
    """{(url, name): working address or None} for each website."""
    cache = _load(SITE_CACHE)
    now = time.time()
    key = lambda url, name: f"{url}|{last_name(name)}"  # noqa: E731

    def stale(u, n):
        e = cache.get(key(u, n)) or {}
        why = e.get("why") or ""
        # A refusal under a rule since dropped (website builders once counted as parking).
        return now - e.get("at", 0) > _spread(u, SITE_DAYS) or (why.startswith("parked at ") and not PARKING.search(why[10:]))
    need = [(u, n) for u, n in dict.fromkeys(pairs) if stale(u, n)]
    if need:
        with ThreadPoolExecutor(max_workers=8) as pool:
            for (u, n), res in zip(need, pool.map(lambda p: _check(*p), need)):
                cache[key(u, n)] = {"at": now, **res}
        _save(SITE_CACHE, cache)
    out = {}
    for u, n in pairs:
        e = cache.get(key(u, n)) or {}
        out[(u, n)] = e.get("final") if e.get("ok") else None
    return out


# Everything together --------------------------------------------------------------------

def enrich(persons, log=print):
    """Look up everyone in `persons` (dicts with "name", maybe "wiki" and a campaign
    "site"). Returns ({wiki link: {"bio", "photo", "site"}}, stats) and sets each dict's
    "site" to its checked campaign site or drops it. The bio, photo and official website
    are shared by everyone linking to the same article; the campaign site belongs to the
    candidacy."""
    linked = {}
    for p in persons:
        t = title_of(p.get("wiki"))
        if t and last_name(p["name"]) in words(t):
            linked.setdefault(p["wiki"], (t, p["name"]))
    titles = sorted({t for t, _ in linked.values()})
    lead = leads(titles)
    qids = sorted({e["qid"] for e in lead.values() if e.get("qid")})
    fx = facts(qids)
    human = {t for t, e in lead.items() if e.get("qid") and (fx.get(e["qid"]) or {}).get("human")}
    pics = wikiphotos.photos(sorted(human), api=W.API, cache_file=PHOTO_CACHE, max_age_days=PHOTO_DAYS, country="Q30")
    # Websites to check: each campaign site, and each person's official ones.
    pairs = []
    for p in persons:
        if p.get("site"):
            pairs.append((p["site"], p["name"]))
    for wiki, (t, name) in linked.items():
        if t in human:
            for s in (fx.get(lead[t]["qid"]) or {}).get("sites", [])[:3]:
                pairs.append((s, name))
    ok = check_sites(pairs)
    people = {}
    for wiki, (t, name) in linked.items():
        if t not in human:
            continue
        e = {}
        bio = tidy_bio(lead[t].get("bio"))  # again, so cached bios get today's tidying
        if bio:
            e["bio"] = bio
        if t in pics:
            e["photo"] = wikiphotos.slim(pics[t])
        f = fx.get(lead[t]["qid"]) or {}
        site = next((ok.get((s, name)) for s in f.get("sites", [])[:3] if ok.get((s, name))), None)
        if site:
            e["site"] = site
        party = party_code(f.get("parties"))
        if party:
            e["party"] = party
        if e:
            people[wiki] = e
    dropped = 0
    for p in persons:
        if p.get("site"):
            good = ok.get((p["site"], p["name"]))
            if good:
                p["site"] = good
            else:
                p.pop("site")
                dropped += 1
    stats = {"linked": len(linked), "people": len(people), "bios": sum(1 for e in people.values() if e.get("bio")),
             "photos": sum(1 for e in people.values() if e.get("photo")), "sites": sum(1 for e in people.values() if e.get("site")),
             "campaignSites": sum(1 for p in persons if p.get("site")), "campaignSitesDropped": dropped}
    log(f"  people: {stats['people']} of {stats['linked']} linked articles ({stats['bios']} bios, {stats['photos']} photos, "
        f"{stats['sites']} websites), {stats['campaignSites']} campaign sites ({dropped} dropped: no answer or no name)")
    return people, stats
