"""Fetch Wikipedia pages through the MediaWiki API and parse their tables.

Wikipedia is used as an aggregator: its election pages compile candidates,
polls (each with a citation) and forecaster ratings in consistent tables, under
CC BY-SA. The site credits it wherever that data appears.

Pages are cached on disk by revision id, so a refresh only downloads the pages
that were edited since the last run.

Wikimedia's 2026 rate limits allow a script 200 requests a minute when its
User-Agent gives a contact (an email address or full URL) and only 10 when it
doesn't. Put a contact in the INFORMED_VOTER_CONTACT environment variable, or in
~/.informed-voter/contact (outside the website folder, so it is never
published); without one, requests are spaced to stay under 10 a minute.
"""

import gzip
import html
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

API = "https://en.wikipedia.org/w/api.php"
CONTACT_FILE = Path.home() / ".informed-voter" / "contact"


def _contact():
    contact = os.environ.get("INFORMED_VOTER_CONTACT", "").strip()
    if not contact and CONTACT_FILE.exists():
        contact = CONTACT_FILE.read_text(encoding="utf-8").strip()
    return contact


CONTACT = _contact()
UA = (f"InformedVoter/1.0 ({CONTACT}; personal election-information site; data refresh script)" if CONTACT
      else "InformedVoter/1.0 (personal election-information site; data refresh script)")
# Seconds between requests. Past its limit Wikimedia answers 503 and 429 until the
# minute is up, and those refusals count against the limit too.
SPACING = 1.0 if CONTACT else 7.0
CACHE = Path(__file__).resolve().parents[2] / "data" / "cache" / "wiki"
_last = [0.0]
stats = {"requests": 0, "cached": 0}


def api(params, retries=8):
    params = {**params, "format": "json", "formatversion": "2"}
    url = f"{API}?{urllib.parse.urlencode(params)}"
    for attempt in range(retries):
        wait = SPACING - (time.time() - _last[0])
        if wait > 0:
            time.sleep(wait)
        _last[0] = time.time()
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "gzip"})
            with urllib.request.urlopen(req, timeout=90) as r:
                body = r.read()
                if r.headers.get("Content-Encoding") == "gzip":
                    body = gzip.decompress(body)
            stats["requests"] += 1
            return json.loads(body.decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code != 429 and e.code < 500:
                raise
            # Rate-limited or overloaded: wait as long as asked (Retry-After counts down
            # to the end of the minute) and never less than an exponential back-off, so
            # quick retries don't use up the next minute's allowance as well.
            try:
                asked = int(e.headers.get("Retry-After") or 0)
            except ValueError:
                asked = 0
            time.sleep(min(max(asked, 5 * 2 ** attempt), 180) + 1)
        except (urllib.error.URLError, TimeoutError, ConnectionError):
            if attempt == retries - 1:
                raise
            time.sleep(5 * (attempt + 1))
    raise RuntimeError(f"Wikipedia kept refusing the request: {url}")


def revisions(titles):
    """{title: {"revid", "timestamp", "title"} or None if the page is missing}."""
    out = {}
    titles = list(dict.fromkeys(titles))
    for i in range(0, len(titles), 50):
        chunk = titles[i:i + 50]
        q = api({"action": "query", "prop": "revisions", "rvprop": "ids|timestamp",
                 "titles": "|".join(chunk), "redirects": 1})["query"]
        norm = {n["from"]: n["to"] for n in q.get("normalized", [])}
        redir = {n["from"]: n["to"] for n in q.get("redirects", [])}
        pages = {p["title"]: p for p in q.get("pages", [])}
        for t in chunk:
            name = norm.get(t, t)
            name = redir.get(name, name)
            p = pages.get(name)
            if not p or p.get("missing") or not p.get("revisions"):
                out[t] = None
            else:
                rev = p["revisions"][0]
                out[t] = {"revid": rev["revid"], "timestamp": rev["timestamp"], "title": name}
    return out


def _slug(title):
    return re.sub(r"[^A-Za-z0-9]+", "_", title).strip("_")[:120]


def page_at(title, rev):
    """HTML of one revision of a page, from the disk cache when possible."""
    CACHE.mkdir(parents=True, exist_ok=True)
    slug = _slug(title)
    path = CACHE / f"{slug}.{rev['revid']}.html"
    if path.exists():
        stats["cached"] += 1
        return path.read_text(encoding="utf-8")
    d = api({"action": "parse", "oldid": rev["revid"], "prop": "text", "disableeditsection": 1})
    text = d["parse"]["text"]
    for old in CACHE.glob(f"{slug}.*.html"):
        old.unlink()
    path.write_text(text, encoding="utf-8")
    return text


def sections(page):
    return api({"action": "parse", "page": page, "prop": "sections", "redirects": 1})["parse"]["sections"]


def section_html(page, index):
    d = api({"action": "parse", "page": page, "prop": "text", "section": index, "redirects": 1, "disableeditsection": 1})
    return d["parse"]["text"]


def page_html(page):
    d = api({"action": "parse", "page": page, "prop": "text", "redirects": 1, "disableeditsection": 1})
    return d["parse"]["text"], d["parse"]["title"]


def find_section(page, *names):
    """Index of the first section whose heading matches one of `names` (case-insensitive)."""
    wanted = [n.lower() for n in names]
    for s in sections(page):
        if s["line"].strip().lower() in wanted:
            return s["index"]
    return None


_HEADING = re.compile(r'<div class="mw-heading mw-heading(\d)"[^>]*>\s*<h\d[^>]*\bid="([^"]*)"[^>]*>(.*?)</h\d>', re.S)


def split_sections(html_text):
    """[{"level", "id", "title", "html"}] for every heading in a parsed page. Each
    chunk runs to the next heading of the same or a higher level, so it includes
    its subsections."""
    heads = [(m.start(), int(m.group(1)), m.group(2), re.sub(r"<[^>]+>", "", m.group(3)).strip())
             for m in _HEADING.finditer(html_text)]
    out = []
    for i, (pos, level, hid, title) in enumerate(heads):
        end = len(html_text)
        for pos2, level2, _, _ in heads[i + 1:]:
            if level2 <= level:
                end = pos2
                break
        out.append({"level": level, "id": hid, "title": html.unescape(title), "html": html_text[pos:end]})
    return out


def section_by_title(html_text, *titles, level=None):
    wanted = [t.lower() for t in titles]
    for s in split_sections(html_text):
        if s["title"].lower() in wanted and (level is None or s["level"] == level):
            return s["html"]
    return None


_REF_ITEM = re.compile(r'<li id="(cite(?:_|&#95;)note-[^"]+)"[^>]*>(.*?)</li>', re.S)
_EXT_LINK = re.compile(r'<a[^>]*class="external[^"]*"[^>]*href="(https?://[^"]+)"[^>]*>(.*?)</a>', re.S)
_EXT_LINK2 = re.compile(r'<a[^>]*href="(https?://[^"]+)"[^>]*class="external[^"]*"[^>]*>(.*?)</a>', re.S)


def references(html_text):
    """{cite_note id: {"url", "title"}} from a page's reference list."""
    out = {}
    for m in _REF_ITEM.finditer(html_text):
        body = m.group(2)
        link = _EXT_LINK.search(body) or _EXT_LINK2.search(body)
        if link:
            title = html.unescape(re.sub(r"<[^>]+>", "", link.group(2))).strip().strip('"“”')
            out[html.unescape(m.group(1))] = {"url": html.unescape(link.group(1)), "title": title}
    return out


class _Tables(HTMLParser):
    """Collect every <table> as a grid of cells, expanding rowspan/colspan.

    Each cell keeps its text, its links, and the ids of its footnote references
    (whose markers are left out of the text). A table keeps its caption, which is
    how election boxes say "Republican primary results" or "General election".
    Nested tables are parsed separately and their text is kept out of the parent.
    """

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tables = []      # finished tables: {"classes", "rows": [[cell]]}
        self.stack = []       # open tables
        self.skip = 0         # inside <sup class=reference>, <style>, etc.
        self.in_ref = False
        self.link = None      # the <a> whose text is being collected
        self.in_caption = False
        self.span_color = None  # a colored <span>, which is how "▌" party markers are drawn

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "table":
            self.stack.append({"classes": a.get("class", ""), "rows": [], "row": None, "cell": None, "caption": ""})
            return
        if not self.stack:
            return
        t = self.stack[-1]
        if tag in ("sup", "style", "script") and (tag != "sup" or "reference" in (a.get("class") or "")):
            self.skip += 1
            self.in_ref = tag == "sup"
            return
        if self.skip:
            if self.in_ref and tag == "a" and t["cell"] is not None and (a.get("href") or "").startswith("#cite_note"):
                t["cell"]["refs"].append(a["href"][1:])
            return
        if tag == "caption":
            self.in_caption = True
        elif tag == "tr":
            t["row"] = []
        elif tag in ("td", "th") and t["row"] is not None:
            t["cell"] = {"text": "", "links": [], "refs": [], "marks": [], "bold": False, "th": tag == "th",
                         "rowspan": int(re.sub(r"\D", "", a.get("rowspan") or "1") or 1),
                         "colspan": int(re.sub(r"\D", "", a.get("colspan") or "1") or 1),
                         "style": a.get("style") or "", "classes": a.get("class") or ""}
        elif tag == "a" and t["cell"] is not None:
            t["cell"]["links"].append({"href": a.get("href") or "", "title": a.get("title") or "", "text": ""})
            self.link = t["cell"]["links"][-1]
        elif tag == "br" and t["cell"] is not None:
            t["cell"]["text"] += "\n"
        elif tag in ("b", "strong") and t["cell"] is not None:
            t["cell"]["bold"] = True  # election boxes bold the winners and those who advance
        elif tag == "span" and t["cell"] is not None:
            m = re.search(r"color:\s*(#[0-9A-Fa-f]{3,6})", a.get("style") or "")
            self.span_color = m.group(1).lower() if m else None

    def handle_endtag(self, tag):
        if tag in ("sup", "style", "script") and self.skip:
            self.skip -= 1
            if not self.skip:
                self.in_ref = False
            return
        if not self.stack or self.skip:
            return
        t = self.stack[-1]
        if tag == "caption":
            self.in_caption = False
        if tag == "span":
            self.span_color = None
        if tag == "a":
            self.link = None
        if tag in ("td", "th") and t["cell"] is not None and t["row"] is not None:
            c = t["cell"]
            c["text"] = re.sub(r"[ \t\xa0]+", " ", c["text"]).strip()
            t["row"].append(c)
            t["cell"] = None
        elif tag == "tr" and t["row"] is not None:
            t["rows"].append(t["row"])
            t["row"] = None
        elif tag == "table":
            done = self.stack.pop()
            self.tables.append({"classes": done["classes"], "rows": _expand(done["rows"]), "caption": " ".join(done["caption"].split())})

    def handle_data(self, data):
        if self.stack and not self.skip and self.in_caption and self.stack[-1]["cell"] is None:
            self.stack[-1]["caption"] += data
            return
        if self.stack and not self.skip and self.stack[-1]["cell"] is not None:
            self.stack[-1]["cell"]["text"] += data
            if "▌" in data:  # each party marker keeps its color, in order
                self.stack[-1]["cell"]["marks"].extend([self.span_color] * data.count("▌"))
            if self.link is not None:
                self.link["text"] += data


def _expand(rows):
    """Turn rows with rowspan/colspan into a rectangular grid of cell copies."""
    grid, pending = [], {}  # pending[(r, c)] = cell carried down by rowspan
    for r, row in enumerate(rows):
        out, c, it = [], 0, iter(row)
        nxt = next(it, None)
        while nxt is not None or (r, c) in pending:
            if (r, c) in pending:
                out.append(pending.pop((r, c)))
                c += 1
                continue
            cell = nxt
            nxt = next(it, None)
            for k in range(cell["colspan"]):
                out.append(cell)
                for down in range(1, cell["rowspan"]):
                    pending[(r + down, c)] = cell
                c += 1
        grid.append(out)
    return grid


def tables(html_text):
    p = _Tables()
    p.feed(html_text)
    return [t for t in p.tables if t["rows"]]


def text(cell):
    return html.unescape(cell["text"]) if cell else ""


def clean_name(s):
    s = re.sub(r"\([^)]*\)", "", s)           # "(incumbent)", "(Republican)"
    s = re.sub(r"[†‡*]", "", s)      # dagger markers
    return re.sub(r"\s+", " ", s).strip(" ,;")
