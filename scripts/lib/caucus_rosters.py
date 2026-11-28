"""The caucuses' own member rosters (checked Nov. 28, 2026): the House websites of the
Congressional Progressive Caucus, the New Democrat Coalition, the Blue Dog Coalition and
the Main Street Caucus, and for the Republican Governance Group, which has no House site,
the "Congressional Members" list of its PAC (Republican Governance / Tuesday Group PAC).

Wikipedia's lists of these caucuses had drifted from them: members who had left (Seth
Magaziner was still a New Democrat there), members missing (Main Street's five from Iowa
and Kentucky; Ryan Mackenzie in the Governance Group), districts from the 2026 maps
(Utah's), so the rosters decide who belongs now. Wikipedia's lists still give the
members-elect, which no roster lists yet, and the article links. The Freedom Caucus and
the Republican Study Committee publish no roster (the Study Committee stopped on Jan. 25,
2025, and Wikipedia names 150 of its 189 members), so theirs come from Wikipedia alone, as
do the House members of the Democratic Socialists of America.

    read(cid) -> {"house": [{"n", "seat"?}], "senate": [{"n", "st"}], "source": {...}}

Every page is laid out differently, so each has its own reader, and each must find a
minimum number of members: a redesigned page fails loudly instead of emptying a caucus.
The Blue Dogs' and the PAC's pages give names only, without districts.
"""

import re
import urllib.request
from datetime import datetime, timezone
from html.parser import HTMLParser

from elections import STATE_ABBR

UA = "InformedVoterResearch/1.0"
# cid: (roster page, title for the source line, fewest members a good read can have)
ROSTERS = {
    "cpc": ("https://progressives.house.gov/caucus-members", "Congressional Progressive Caucus: Caucus Members", 60),
    "newdem": ("https://newdemocratcoalition.house.gov/members", "New Democrat Coalition: Members", 60),
    "bluedog": ("https://bluedogs-gluesenkampperez.house.gov/members", "Blue Dog Coalition: Members", 5),
    "mainstreet": ("https://mainstreetcaucus.house.gov/membership", "Main Street Caucus: Membership", 40),
    "governance": ("https://republicangovernance.com/", "Republican Governance / Tuesday Group PAC: Congressional Members", 20),
}
ABBR = {**STATE_ABBR, "the District of Columbia": "DC", "Puerto Rico": "PR", "Virgin Islands": "VI",
        "U.S. Virgin Islands": "VI", "Guam": "GU", "American Samoa": "AS", "Northern Mariana Islands": "MP"}
BLOCK = {"p", "div", "br", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6", "section", "article", "td", "th",
         "blockquote", "ul", "ol", "table", "header", "footer"}


class _Text(HTMLParser):
    """A page's text, one line per block element, without scripts and styles."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.skip = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript", "svg"):
            self.skip += 1
        if tag in BLOCK:
            self.out.append("\n")

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript", "svg") and self.skip:
            self.skip -= 1
        if tag in BLOCK:
            self.out.append("\n")

    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)


def lines(doc):
    p = _Text()
    p.feed(doc)
    text = "".join(p.out).replace(" ", " ")
    return [re.sub(r"\s+", " ", l).strip() for l in text.split("\n") if l.strip()]


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.5"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode(r.headers.get_content_charset() or "utf-8", "replace")


def seat(state, d=None):
    st = ABBR.get(state.strip())
    if not st:
        return None
    return f"{st}-{int(d):02d}" if d and str(d).isdigit() and int(d) else f"{st}-00"


def parse_cpc(L):
    """Leadership blocks, then "House Members": a name line, then "12th District of North
    Carolina", "Representing Vermont", "Delaware District at Large" or, for the senator,
    "U.S. Senator for Vermont"."""
    start = next(i for i, l in enumerate(L) if l.startswith("The Congressional Progressive Caucus is composed"))
    roles = {"Chair", "Deputy Chair", "Whip", "Chair Emeriti", "Vice Chairs", "Executive Board Members At Large",
             "Senate Member", "House Members"}
    house, senate, name = [], [], None
    for l in L[start + 1:]:
        if l == "About The CPC":
            break
        if l in roles:
            continue
        s = None
        if m := re.match(r"(\d+)(?:st|nd|rd|th) District of (.+)$", l):
            s = seat(m.group(2), m.group(1))
        elif m := re.match(r"Representing (?:the )?(.+)$", l):
            s = seat(m.group(1))
        elif m := re.match(r"(.+) District at Large$", l):
            s = seat(m.group(1))
        elif m := re.match(r"U\.S\. Senator for (.+)$", l):
            if name and ABBR.get(m.group(1)):
                senate.append({"n": name, "st": ABBR[m.group(1)]})
            name = None
            continue
        if m:
            if name and s:
                house.append({"n": name, "seat": s})
            name = None
        else:
            name = l
    return house, senate


def parse_newdem(L):
    """By state: "Alabama - 07", social links, "VISIT OFFICIAL SITE", then the name. Puerto
    Rico's Resident Commissioner has the territory's name alone ("Puerto Rico")."""
    start = L.index("Alphabetical by State/Territory")
    links = ("Social Link", "VISIT OFFICIAL SITE")
    house, k = [], start + 1
    while k < len(L):
        m = re.match(r"(.+?) - (\d+|At Large|AL)$", L[k])
        alone = not m and L[k] in ABBR and ABBR[L[k]] in ("PR", "GU", "AS", "MP", "VI", "DC") and k + 1 < len(L) and L[k + 1] in links
        if m or alone:
            j = k + 1
            while j < len(L) and L[j] in links:
                j += 1
            s = seat(m.group(1), m.group(2) if m.group(2).isdigit() else None) if m else seat(L[k])
            if j < len(L) and s:
                house.append({"n": L[j], "seat": s})
            k = j
        k += 1
    return house, []


def parse_bluedog(L):
    """Names only, under "Our Chairs" and "Members": "Mr. Jim Costa"."""
    start = L.index("Our Chairs")
    house = []
    for l in L[start + 1:]:
        if l == "Search again":
            break
        if l != "Members":
            house.append({"n": re.sub(r"^(?:Mr|Ms|Mrs|Rep|Dr)\.\s+", "", l).strip()})
    return house, []


def parse_mainstreet(L):
    """"Rep. Mark Alford", then "Missouri's 4th District" ("North Dakota's At Large District")."""
    start = L.index("Caucus Leadership")
    house, name = [], None
    for l in L[start + 1:]:
        if l.startswith("Rep. "):
            name = re.sub(r",?\s+M\.D\.$", "", l[5:]).strip()
            continue
        m = re.match(r"(.+?)\s*'s\s+(\d+|At Large)\s*(?:st|nd|rd|th)?\b", l)
        if m and name:
            s = seat(m.group(1), m.group(2) if m.group(2).isdigit() else None)
            if s:
                house.append({"n": name, "seat": s})
            name = None
    return house, []


def parse_governance(L):
    """Names only, under "Congressional Members": "Congresswoman Young Kim"."""
    start = L.index("Congressional Members")
    house = []
    for l in L[start + 1:]:
        m = re.match(r"Congress(?:man|woman) (.+)$", l)
        if not m:
            break
        house.append({"n": m.group(1).strip()})
    return house, []


PARSERS = {"cpc": parse_cpc, "newdem": parse_newdem, "bluedog": parse_bluedog, "mainstreet": parse_mainstreet,
           "governance": parse_governance}


def read(cid):
    url, title, least = ROSTERS[cid]
    house, senate = PARSERS[cid](lines(fetch(url)))
    if len(house) < least:
        raise ValueError(f"only {len(house)} members read from {url}; has the page changed?")
    return {"house": house, "senate": senate,
            "source": {"title": title, "url": url, "asOf": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}}
