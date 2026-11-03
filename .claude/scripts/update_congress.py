"""Build data/congress.json: who sits in Congress, seat by seat, for the half-circle
charts on #/congress.

Sources, read once a day by scripts/refresh_all.py:
  * The House Clerk's member list (clerk.house.gov/xml/lists/MemberData.xml): every
    representative's party, caucus, state and district, the vacancies and why, and the
    six non-voting delegates.
  * English Wikipedia's "List of current United States senators" (senate.gov refuses
    scripts): every senator's party, state, class and start date. Each chamber's
    Wikipedia infobox gives its leaders and, for the Senate, which side the independents
    caucus with.
  * Wikidata: the President of the United States (P35 of Q30).
  * Wikidata and Commons: the photos of the President and the leaders, with their
    credits (scripts/lib/wikiphotos.py, cached a week with update_photos.py's).

If the Clerk's list or the senators' table can't be read, the previous file is kept.

    py scripts/update_congress.py
"""

import json
import re
import sys
import unicodedata
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "lib"))
import wikitables as W  # noqa: E402
import wikiphotos  # noqa: E402
from elections import party_code  # noqa: E402  - Minnesota's senators are "DFL"

sys.stdout.reconfigure(encoding="utf-8")
OUT = ROOT / "data" / "congress.json"
PHOTOS_CACHE = ROOT / "data" / "cache" / "wiki" / "photos.json"
CLERK = "https://clerk.house.gov/xml/lists/MemberData.xml"
CLERK_UA = "InformedVoter/1.0 (personal election-information site; data refresh script)"
SENATORS = "List of current United States senators"
HOUSE_PAGE = "United States House of Representatives"
SENATE_PAGE = "United States Senate"
WIKIDATA = "https://www.wikidata.org/w/api.php"

STATES = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California", "CO": "Colorado",
    "CT": "Connecticut", "DE": "Delaware", "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho",
    "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana",
    "ME": "Maine", "MD": "Maryland", "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi",
    "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada", "NH": "New Hampshire", "NJ": "New Jersey",
    "NM": "New Mexico", "NY": "New York", "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma",
    "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina", "SD": "South Dakota",
    "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VT": "Vermont", "VA": "Virginia", "WA": "Washington",
    "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming",
}
CODE = {v: k for k, v in STATES.items()}
# The Census Bureau's four regions.
REGIONS = {
    "Northeast": "CT ME MA NH RI VT NJ NY PA",
    "Midwest": "IL IN MI OH WI IA KS MN MO NE ND SD",
    "South": "DE FL GA MD NC SC VA WV AL KY MS TN AR LA OK TX DC",
    "West": "AZ CO ID MT NV NM UT WY AK CA HI OR WA",
}
REGION = {st: reg for reg, sts in REGIONS.items() for st in sts.split()}
PARTY = {"Democratic": "D", "Republican": "R", "Independent": "I"}
SEATS = {"house": 435, "senate": 100}
# Order of the chamber, left to right.
GROUP_ORDER = ["D", "I-D", "I", "I-R", "R"]


def fold(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    return " ".join(re.findall(r"[a-z0-9]+", s))


def iso_day(s):
    try:
        return datetime.strptime(re.sub(r"\s+", " ", s.strip()), "%B %d, %Y").date().isoformat()
    except ValueError:
        return None


def house():
    try:
        req = urllib.request.Request(CLERK, headers={"User-Agent": CLERK_UA})
        with urllib.request.urlopen(req, timeout=90) as r:
            raw = r.read()
        root = ET.fromstring(raw)
    except Exception as e:  # noqa: BLE001
        raise SystemExit(f"the House Clerk's member list couldn't be read ({e}); keeping the old file")
    info = {c.tag: (c.text or "").strip() for c in root.find("title-info")}
    info["published"] = root.get("publish-date")  # "October 1, 2026"
    members, vacancies, delegates = [], [], []
    for el in root.findall("./members/member"):
        mi = el.find("member-info")
        sd = el.findtext("statedistrict") or ""
        st = mi.find("state").get("postal-code")
        dist = int(sd[2:]) if sd[2:].isdigit() else 0
        if not (mi.findtext("lastname") or "").strip():
            vacancies.append({"st": st, "d": dist, "note": (mi.findtext("footnote") or "").strip() or None})
            continue
        m = {
            "n": (mi.findtext("official-name") or "").strip(),
            "party": (mi.findtext("party") or "").strip(),
            "caucus": (mi.findtext("caucus") or "").strip(),
            "st": st, "d": dist, "id": (mi.findtext("bioguideID") or "").strip(),
            "last": (mi.findtext("lastname") or "").strip(), "first": (mi.findtext("firstname") or "").strip(),
        }
        if st not in STATES:  # DC, Puerto Rico and the territories send non-voting members
            delegates.append({"n": m["n"], "party": m["party"], "st": st, "where": mi.find("state").findtext("state-fullname")})
            continue
        members.append(m)
    if len(members) + len(vacancies) != SEATS["house"]:
        raise SystemExit(f"the Clerk's list has {len(members)} members and {len(vacancies)} vacancies, not 435; keeping the old file")
    return members, vacancies, delegates, info


def senators():
    revs = W.revisions([SENATORS])
    html_text = W.page_at(SENATORS, revs[SENATORS])
    out = []
    for tb in W.tables(html_text):
        head = [W.text(c).strip() for c in tb["rows"][0]]
        if "Senator" not in head or "Assumed office" not in head:
            continue
        i_state, i_name = head.index("State"), head.index("Senator")
        i_party = len(head) - 1 - head[::-1].index("Party")  # the first "Party" column is the color bar
        i_since = head.index("Assumed office")
        i_class = next(i for i, h in enumerate(head) if h.startswith("Class"))
        for r in tb["rows"][1:]:
            state = W.text(r[i_state]).strip()
            name = W.clean_name(W.text(r[i_name]))
            if state not in CODE or not name:
                continue
            link = next((l["title"] for l in r[i_name]["links"] if l.get("title")), None)
            cls = W.text(r[i_class])
            up = re.search(r"\b(20\d\d)\b", cls)
            party = party_code(W.text(r[i_party]))
            out.append({"n": name, "party": party if party in ("D", "R") else "I", "st": CODE[state],
                        "article": link, "since": iso_day(W.text(r[i_since])),
                        "cls": int(m.group(1)) if (m := re.search(r"Class\s*(\d)", cls)) else None,
                        "up": int(up.group(1)) if up else None})
        break
    if len(out) != SEATS["senate"]:
        raise SystemExit(f"read {len(out)} senators from Wikipedia, not 100; keeping the old file")
    return out, {"title": SENATORS, "url": "https://en.wikipedia.org/wiki/" + SENATORS.replace(" ", "_"), "revid": revs[SENATORS]["revid"]}


ROLES = {
    "house": ["Speaker", "Majority Leader", "Minority Leader", "Majority Whip", "Minority Whip"],
    "senate": ["President", "President pro tempore", "Majority Leader", "Minority Leader", "Majority Whip", "Minority Whip"],
}


def leaders(title, chamber):
    """[{"office", "name", "party", "since", "article"}] and the "Political groups" text
    from a chamber's Wikipedia infobox."""
    revs = W.revisions([title])
    html_text = W.page_at(title, revs[title])
    found, groups = {}, ""
    for tb in W.tables(html_text)[:3]:
        for r in tb["rows"]:
            if len(r) < 2:
                continue
            label, value = W.text(r[0]).strip(), " ".join(W.text(r[1]).split())
            if label in ROLES[chamber] and label not in found:
                m = re.match(r"(.+?)\s*\(([A-Z])\)\s*since\s+(.+)$", value)
                if m:
                    link = next((l["title"] for l in r[1]["links"] if l.get("title") and not l["title"].startswith("List")), None)
                    found[label] = {"office": label, "name": m.group(1), "party": m.group(2), "since": iso_day(m.group(3)), "article": link}
            elif label == "Political groups" and not groups:
                groups = value
    src = {"title": title, "url": "https://en.wikipedia.org/wiki/" + title.replace(" ", "_"), "revid": revs[title]["revid"]}
    return [found[r] for r in ROLES[chamber] if r in found], groups, src


def senate_caucus(groups_text):
    """Which side the independents sit with, from "Majority (53) Republican (53) Minority
    (47) Democratic (45) Independent (2)": "D", "R" or None when unclear."""
    blocs = re.split(r"\b(?=Majority|Minority)\b", groups_text)
    sides = []
    for b in blocs:
        if "Independent" in b:
            main = re.search(r"(Democratic|Republican)", b)
            sides.append(PARTY[main.group(1)] if main else None)
    return sides[0] if len(set(sides)) == 1 else None


def president():
    ents = W.api({"action": "wbgetentities", "ids": "Q30", "props": "claims"}, base=WIKIDATA)["entities"]
    claims = [c for c in ents["Q30"]["claims"].get("P35", []) if c.get("rank") != "deprecated" and not (c.get("qualifiers") or {}).get("P582")]
    start = lambda c: (((c.get("qualifiers") or {}).get("P580") or [{}])[0].get("datavalue") or {}).get("value", {}).get("time", "")  # noqa: E731
    claims.sort(key=lambda c: (c.get("rank") == "preferred", start(c)), reverse=True)
    if not claims:
        return None
    qid = claims[0]["mainsnak"]["datavalue"]["value"]["id"]
    e = W.api({"action": "wbgetentities", "ids": qid, "props": "labels|sitelinks|claims", "languages": "en|mul", "sitefilter": "enwiki"}, base=WIKIDATA)["entities"][qid]
    labels = e.get("labels") or {}
    name = (labels.get("en") or labels.get("mul") or {}).get("value")
    # The current party (P102 with no end date): Republican Party Q29468, Democratic Party Q29552.
    parties = [c for c in (e.get("claims") or {}).get("P102", []) if c.get("rank") != "deprecated" and not (c.get("qualifiers") or {}).get("P582")]
    parties.sort(key=lambda c: c.get("rank") == "preferred", reverse=True)
    party = {"Q29468": "R", "Q29552": "D"}.get(((parties[0]["mainsnak"].get("datavalue") or {}).get("value") or {}).get("id")) if parties else None
    return {"name": name, "party": party, "since": start(claims[0])[1:11] or None, "article": ((e.get("sitelinks") or {}).get("enwiki") or {}).get("title"),
            "source": f"https://www.wikidata.org/wiki/{qid}"} if name else None


def last_photos():
    """{article: photo} for the President and leaders in the last build."""
    try:
        old = json.loads(OUT.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    people = [old.get("president")] + [l for ch in (old.get("chambers") or {}).values() for l in ch.get("leaders") or []]
    return {p["article"]: p["photo"] for p in people if p and p.get("article") and p.get("photo")}


def add_photos(people):
    """Each person's Wikidata photo with its credit; the last build's when Wikimedia
    can't be read."""
    people = [p for p in people if p and p.get("article")]
    try:
        found = wikiphotos.photos([p["article"] for p in people], api=W.API, cache_file=PHOTOS_CACHE,
                                  max_age_days=7, country="Q30")
        found = {t: wikiphotos.slim(p) for t, p in found.items()}
    except Exception as e:  # noqa: BLE001
        print(f"Wikimedia unreadable for photos ({e}); keeping the last build's")
        found = last_photos()
    for p in people:
        if p["article"] in found:
            p["photo"] = found[p["article"]]


def groups_for(members, chamber):
    counts = {}
    for m in members:
        counts[m["g"]] = counts.get(m["g"], 0) + 1
    names = {"D": "Democrats", "R": "Republicans", "I": "Independents", "I-D": "Independents (caucus with Democrats)",
             "I-R": "Independents (caucus with Republicans)"}
    return [{"id": g, "seats": counts[g], "name": names[g], "color": {"D": "dem", "R": "rep"}.get(g, "other"), "shape": "circle"}
            for g in GROUP_ORDER if counts.get(g)]


def match_house(leader, members):
    """A House leader among the Clerk's members: full name, else last name and first initial."""
    want = fold(leader["name"])
    hits = [m for m in members if fold(f"{m['first']} {m['last']}") == want or fold(m["n"]) == want]
    if not hits:
        parts = want.split()
        hits = [m for m in members if fold(m["last"]) == parts[-1] and fold(m["first"])[:1] == parts[0][:1]]
    return hits[0] if len(hits) == 1 else None


def main():
    h_members, vacancies, delegates, info = house()
    s_members, s_src = senators()
    h_leaders, _, h_src = leaders(HOUSE_PAGE, "house")
    s_leaders, s_groups, s_src2 = leaders(SENATE_PAGE, "senate")
    checks = []

    for m in h_members:
        m["g"] = f"I-{m['caucus']}" if m["party"] == "I" and m["caucus"] in ("D", "R") else m["party"]
    side = senate_caucus(s_groups)
    for m in s_members:
        m["g"] = f"I-{side}" if m["party"] == "I" and side else m["party"]
    for l in h_leaders:
        hit = match_house(l, h_members)
        if hit:
            hit["role"] = l["office"]
        else:
            checks.append(f"House: {l['office']} {l['name']} (Wikipedia) not found in the Clerk's member list")
    for l in s_leaders:
        hit = next((m for m in s_members if l["article"] and m["article"] == l["article"]), None)
        if hit:
            hit["role"] = l["office"]
        elif l["office"] != "President":  # the Vice President presides but isn't a senator
            checks.append(f"Senate: {l['office']} {l['name']} (Wikipedia) not found in the senators' table")

    for ms in (h_members, s_members):
        for m in ms:
            m["reg"] = REGION.get(m["st"])
    rank = {g: i for i, g in enumerate(GROUP_ORDER)}
    h_members.sort(key=lambda m: (rank[m["g"]], m["st"], m["d"]))
    s_members.sort(key=lambda m: (rank[m["g"]], m["st"], m["n"]))
    for m in h_members:
        for k in ("first", "last", "caucus"):
            m.pop(k, None)

    try:
        pres = president()
    except Exception as e:  # noqa: BLE001
        print(f"Wikidata unreadable ({e}); keeping the last build's President")
        try:
            pres = json.loads(OUT.read_text(encoding="utf-8")).get("president")
        except (OSError, ValueError):
            pres = None
    add_photos([pres, *h_leaders, *s_leaders])

    majority_party = info.get("majority")
    data = {
        "updated": datetime.now(timezone.utc).isoformat(timespec="minutes"),
        "congress": int(info.get("congress-num") or 0) or None, "session": info.get("session"),
        "president": pres,
        "chambers": {
            "house": {"seats": SEATS["house"], "majority": SEATS["house"] // 2 + 1, "control": majority_party,
                      "published": info.get("published"), "groups": groups_for(h_members, "house"), "members": h_members,
                      "vacancies": vacancies, "delegates": delegates, "leaders": h_leaders,
                      "sources": [{"title": "Office of the Clerk, U.S. House of Representatives: member data", "url": CLERK}, h_src]},
            "senate": {"seats": SEATS["senate"], "majority": SEATS["senate"] // 2 + 1,
                       "control": next((PARTY[p] for p in re.findall(r"Majority \(\d+\)\s*(Democratic|Republican)", s_groups)), None),
                       "independentsCaucus": side, "groups": groups_for(s_members, "senate"), "members": s_members,
                       "leaders": s_leaders, "sources": [s_src, s_src2]},
        },
        "checks": checks,
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    h, s = data["chambers"]["house"], data["chambers"]["senate"]
    print(f"wrote {OUT.relative_to(ROOT).as_posix()}: House {len(h_members)}/435 "
          f"({', '.join(f'{g['id']} {g['seats']}' for g in h['groups'])}; {len(vacancies)} vacant; {len(delegates)} delegates), "
          f"Senate ({', '.join(f'{g['id']} {g['seats']}' for g in s['groups'])}); President {pres and pres['name']}")
    print("  House leaders:", [(l["office"], l["name"]) for l in h_leaders])
    print("  Senate leaders:", [(l["office"], l["name"]) for l in s_leaders])
    for c in checks:
        print("  check:", c)


if __name__ == "__main__":
    main()
