"""Refresh data/news.json from publishers' public RSS feeds.

Keeps only election stories, tags each one by topic (gains, scandals,
endorsements, turnout...) and by race type, and stores the headline, a short
publisher-supplied summary and the link. Browsers can't read these feeds
directly (no CORS), so the site shows the snapshot this script writes.

The outlet list deliberately spans left, centre and right publications.

Usage:  python -I scripts/update_news.py [output-path]
Run it every hour or so while the election is on (a scheduled job works well).
"""

import html
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime

FEEDS = [
    ("NPR", "https://feeds.npr.org/1014/rss.xml"),
    ("PBS NewsHour", "https://www.pbs.org/newshour/feeds/rss/politics"),
    ("Politico", "https://rss.politico.com/politics-news.xml"),
    ("The Hill", "https://thehill.com/homenews/campaign/feed/"),
    ("Fox News", "https://moxie.foxnews.com/google-publisher/politics.xml"),
    ("CBS News", "https://www.cbsnews.com/latest/rss/politics"),
    ("ABC News", "https://feeds.abcnews.com/abcnews/politicsheadlines"),
    ("NBC News", "https://feeds.nbcnews.com/nbcnews/public/politics"),
    ("New York Post", "https://nypost.com/politics/feed/"),
    ("Washington Examiner", "https://www.washingtonexaminer.com/section/politics/feed/"),
    ("Washington Times", "https://www.washingtontimes.com/rss/headlines/news/politics/"),
    ("National Review", "https://www.nationalreview.com/feed/"),
    ("The Guardian", "https://www.theguardian.com/us-news/us-politics/rss"),
    ("Axios", "https://api.axios.com/feed/"),
    ("Newsweek", "https://www.newsweek.com/rss"),
    ("Christian Science Monitor", "https://rss.csmonitor.com/feeds/usa"),
    ("Reason", "https://reason.com/feed/"),
    ("Deseret News", "https://www.deseret.com/arc/outboundfeeds/rss/category/politics/"),
]

MAX_AGE_DAYS = 7
MAX_ITEMS = 160
SUMMARY_CHARS = 220

ELECTION = re.compile(
    r"\b(elections?|midterms?|campaign(s|ing)?|candidates?|ballots?|voters?|voting|early vot\w*|turnout|"
    r"polls?|polling|pollsters?|primary|primaries|runoffs?|nominees?|endorse\w*|debates?|redistricting|"
    r"gerrymander\w*|toss-?ups?|battleground|swing (state|district|seat)s?|senate race|house race|"
    r"governor'?s race|gubernatorial|flip(s|ped)?|open seat|super pac|fundrais\w*)\b",
    re.I,
)

# First match wins, so the order is the priority.
TOPICS = [
    ("Scandals", r"scandal|indict|investigat|\bprobe|ethics|charged|lawsuit|\bsue[sd]?\b|suing|allegation|accus|subpoena|resign|misconduct|fraud|controvers"),
    ("Endorsements", r"endors"),
    ("Turnout", r"turnout|early vot|ballots cast|mail(-in)? ballots?|absentee|voter registration|polling place|vote early|voted early|lines? to vote"),
    ("Gains & momentum", r"\bpolls?\b|polling|\bleads?\b|surge|\bgains?\b|momentum|\bahead\b|trail(s|ing)?|\bedge\b|toss-?up|tight race|narrow|flip|lead(ing)? in"),
    ("Money & ads", r"fundrais|raised|\bhaul\b|super pac|\bpac\b|ad buy|\bads?\b|donor|spending"),
    ("Debates", r"debate"),
]
RACES = [
    ("Senate", r"\bsenat(e|or|orial)\b"),
    ("House", r"\bhouse (seat|race|district|majority|control)|congressional|\bdistrict\b|\brep\. "),
    ("Governor", r"governor|gubernatorial"),
]
PARTIES = [
    ("Democrats", r"\bdemocrat|\bdems?\b|\bdnc\b|dccc|dscc"),
    ("Republicans", r"republican|\bgop\b|\brnc\b|nrcc|nrsc|\bmaga\b"),
]

ATOM = "{http://www.w3.org/2005/Atom}"
TAG_RE = re.compile(r"<[^>]+>")


def clean(text):
    text = html.unescape(TAG_RE.sub(" ", text or ""))
    return re.sub(r"\s+", " ", text).strip()


def shorten(text, n):
    if len(text) <= n:
        return text
    cut = text[:n].rsplit(" ", 1)[0]
    return cut.rstrip(",.;:") + "…"


def parse_date(s):
    if not s:
        return None
    s = s.strip()
    try:
        d = parsedate_to_datetime(s)
    except (TypeError, ValueError):
        try:
            d = datetime.fromisoformat(s.replace("Z", "+00:00"))
        except ValueError:
            return None
    if d.tzinfo is None:
        d = d.replace(tzinfo=timezone.utc)
    return d.astimezone(timezone.utc)


def items_of(xml_bytes):
    root = ET.fromstring(xml_bytes)
    for it in root.iter("item"):
        yield {
            "title": it.findtext("title"),
            "link": it.findtext("link"),
            "date": it.findtext("pubDate") or it.findtext("{http://purl.org/dc/elements/1.1/}date"),
            "summary": it.findtext("description"),
        }
    for e in root.iter(f"{ATOM}entry"):
        link = e.find(f"{ATOM}link")
        yield {
            "title": e.findtext(f"{ATOM}title"),
            "link": link.get("href") if link is not None else None,
            "date": e.findtext(f"{ATOM}published") or e.findtext(f"{ATOM}updated"),
            "summary": e.findtext(f"{ATOM}summary"),
        }


def tags(pattern_list, text):
    return [name for name, pat in pattern_list if re.search(pat, text, re.I)]


def main(out_path):
    cutoff = datetime.now(timezone.utc) - timedelta(days=MAX_AGE_DAYS)
    seen, items, ok = set(), [], []
    for source, url in FEEDS:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (InformedVoter news refresh)"})
            with urllib.request.urlopen(req, timeout=30) as r:
                raw = r.read()
            n = 0
            for it in items_of(raw):
                title, link = clean(it["title"]), (it["link"] or "").strip()
                if not title or not link.startswith("http"):
                    continue
                summary = shorten(clean(it["summary"]), SUMMARY_CHARS)
                text = f"{title} {summary}"
                if not ELECTION.search(text):
                    continue
                when = parse_date(it["date"])
                if when and when < cutoff:
                    continue
                key = re.sub(r"[^a-z0-9]", "", title.lower())[:60]
                if key in seen or link in seen:
                    continue
                seen.update((key, link))
                topics = tags(TOPICS, text)
                items.append({
                    "title": title,
                    "link": link,
                    "source": source,
                    "published": when.isoformat(timespec="minutes") if when else None,
                    "summary": summary,
                    "topic": topics[0] if topics else "Campaign trail",
                    "topics": topics,
                    "races": tags(RACES, text),
                    "parties": tags(PARTIES, text),
                })
                n += 1
            ok.append({"name": source, "url": url, "items": n})
            print(f"{source:26} {n:3} election stories")
        except Exception as e:  # one dead feed shouldn't sink the refresh
            print(f"{source:26} FAILED: {e}")
    items.sort(key=lambda x: x["published"] or "", reverse=True)
    items = items[:MAX_ITEMS]
    out = {"updated": datetime.now(timezone.utc).isoformat(timespec="minutes"), "feeds": ok, "items": items}
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    counts = {}
    for it in items:
        counts[it["topic"]] = counts.get(it["topic"], 0) + 1
    print(f"wrote {out_path}: {len(items)} stories {counts}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "data/news.json")
