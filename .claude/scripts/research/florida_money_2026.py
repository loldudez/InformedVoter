"""Money by source for Florida's governor candidates, from the itemized records in the
Florida Division of Elections campaign finance database. Writes
data/research/florida_money.json, which update_races.py merges onto FL-GOV.

Florida itemizes every contribution, so each campaign account is grouped into the
site's funding lines by who gave:
  public  - matching funds paid by the State of Florida (it matches Floridians'
            gifts of $250 or less for candidates who accept spending limits); the
            payments appear as "STATE OF FLORIDA" or "STATE OF FLORIDA DEPARTMENT OF
            FINANCIAL SERVICES"
  self    - the candidate's own money and loans (same name, Florida address)
  party   - the state and county party committees
  pac     - organizations: businesses, unions, PACs and clubs, known by words in
            the name (INC, PAC, UNION...) or an occupation like "POLITICAL
            ORGANIZATION". Florida lets corporations give to state candidates
            directly, up to $3,000 an election.
  small   - people whose gifts total $200 or less
  large   - people who gave more than $200 in all
  other   - loans from anyone else
Refunds are netted against the giver they went back to. A candidate's political
committee raises money separately and without limits; its total and largest givers
go in the note, never into the account's figures.

    py scripts/research/florida_money_2026.py
"""

import hashlib
import re
import sys
import time
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import date

from common import ROOT, write

sys.stdout.reconfigure(encoding="utf-8")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
DOE = "https://dos.elections.myflorida.com"
ELECTION = "20261103-GEN"
ROWS = 30000  # the database's row cap per query; larger values overflow

# (candidate id, last name, first-name filter, own-money pattern, DOE account, committee).
# Records list a candidate either way round ("RUSSO FRANK", "FRANK RUSSO").
CANDIDATES = [
    ("FL-GOV:jolly", "Jolly", "David", r"^(JOLLY,? DAVID|DAVID JOLLY)\b", 89243, "Florida 2026"),
    ("FL-GOV:donalds", "Donalds", "Byron", r"^(DONALDS,? BYRON|BYRON DONALDS)\b", 89042, "Friends of Byron Donalds"),
    ("FL-GOV:russo", "Russo", "Frank", r"^(RUSSO,? FRANK|FRANK RUSSO)\b", 89571, None),
    ("FL-GOV:burkett", "Burkett", "Charles", r"^(BURKETT,? CHARLES|CHARLES BURKETT)\b", 90630, None),
    ("FL-GOV:abrams", "Abrams", "Dean", r"^(ABRAMS,? DEAN|DEAN ABRAMS)\b", 90433, None),
    ("FL-GOV:jewett", "Jewett", "Scott", r"^(JEWETT,? SCOTT|SCOTT JEWETT)\b", 84076, None),
    ("FL-GOV:dimanche", "Dimanche", "Moliere", r"^(DIMANCHE,? (MOLIERE|MOE)|(MOLIERE|MOE) DIMANCHE)\b", 88529, None),
    ("FL-GOV:datto", "Datto", "Jeffrey", r"^(DATTO,? JEFF|JEFF(REY)? DATTO)", 89630, None),
]
# How a few large givers are best written; anything else is title-cased.
DISPLAY = {"AFT COPE DYNAMICS": "AFT COPE Dynamics", "TRIBE OF FLORIDA SEMINOLE": "the Seminole Tribe of Florida",
           "SEMINOLE TRIBE OF FLORIDA": "the Seminole Tribe of Florida", "DEMOCRATIC GOVERNORS ASSOCIATION": "the Democratic Governors Association",
           "REPUBLICAN GOVERNORS ASSOCIATION": "the Republican Governors Association"}
NAMES = {"FL-GOV:jolly": "David Jolly", "FL-GOV:donalds": "Byron Donalds", "FL-GOV:russo": "Frank Russo",
         "FL-GOV:burkett": "Charles Burkett", "FL-GOV:abrams": "Dean Abrams", "FL-GOV:jewett": "Scott Jewett",
         "FL-GOV:dimanche": "Moe Dimanche", "FL-GOV:datto": "Jeffrey Datto"}
PARTIES = {"FL-GOV:jolly": "D", "FL-GOV:donalds": "R", "FL-GOV:jewett": "L"}

# Words that mark an organization when they follow the first word of a name (the
# database lists people surname first, so "COPE KEN" is a person, "UNITED TEACHERS
# OF DADE TIGER COPE INC" is not).
ORG = re.compile(r"\b(INC|INCORPORATED|LLC|L\.L\.C|PAC|COMMITTEE|UNION|ASSOCIATION|ASSN|FUND|CORP|CORPORATION|"
                 r"COMPANY|PARTNERS|PARTNERSHIP|LLP|PLLC|P\.?A|FOUNDATION|FEDERATION|CAUCUS|COALITION|ALLIANCE|"
                 r"SOCIETY|LEAGUE|INSTITUTE|NETWORK|ENTERPRISES|HOLDINGS|INVESTMENTS|PROPERTIES|SERVICES|SOLUTIONS|"
                 r"CONSULTING|LTD|AFL-CIO|SEIU|IBEW|AFSCME|TEAMSTERS|DEMOCRATS|REPUBLICANS|PARTY|ORGANIZATION|"
                 r"POLITICAL|CLUB|COPE|COUNCIL|GROUP|LOCAL|BANK|TRUST)\b|\bCO\.?$")
ALWAYS_ORG = re.compile(r"\b(INC|LLC|PAC|PLLC|LTD|AFL-CIO)\b")
# Political committees often have names like "CONSERVATISM COUNTS"; the occupation
# field gives them away.
ORG_OCCUPATION = re.compile(r"POLITICAL ORGANIZATION|POLITICAL (ACTION )?COMMITTEE|^PAC$|TRADE ASSOCIATION|LAW FIRM$|"
                            r"^(INSURANCE|HEALTH CARE|HOLDING|REAL ESTATE|TECH|CONSTRUCTION) COMPANY$|"
                            r"(ENGINEERING|CONSULTING|LOBBYING) FIRM$|^CORPORATION$|^BUSINESS$|^(LABOR )?UNION$")
CACHE = ROOT / "data" / "cache" / "fl_doe"  # one day's query results, so reruns don't refetch
PARTY = re.compile(r"^(FLORIDA DEMOCRATIC PARTY|REPUBLICAN PARTY OF FLORIDA|DEMOCRATIC PARTY OF .+|REPUBLICAN PARTY OF .+|"
                   r".+ (DEMOCRATIC|REPUBLICAN) EXECUTIVE COMMITTEE|.+ COUNTY (DEMOCRATIC|REPUBLICAN) PARTY|"
                   r"LIBERTARIAN PARTY OF FLORIDA)$")
FL_PLACE = re.compile(r",\s*FL\b|\b3[234]\d{3}\b")  # some records give no ZIP code


def post(script, fields, tries=3):
    data = urllib.parse.urlencode(fields).encode()
    cached = CACHE / f"{date.today()}-{hashlib.sha1(script.encode() + data).hexdigest()[:16]}.tsv"
    if cached.exists():
        return cached.read_text(encoding="utf-8")
    text = _post(script, data, tries)
    CACHE.mkdir(parents=True, exist_ok=True)
    cached.write_text(text, encoding="utf-8")
    return text


def _post(script, data, tries):
    for attempt in range(tries):
        try:
            req = urllib.request.Request(f"{DOE}/cgi-bin/{script}", data=data,
                                         headers={"User-Agent": UA, "Content-Type": "application/x-www-form-urlencoded"})
            with urllib.request.urlopen(req, timeout=240) as r:
                text = r.read().decode("latin-1")
            if "Error in /cgi-bin" in text[:400]:
                raise RuntimeError(text[:300])
            time.sleep(0.5)
            return text
        except Exception:  # noqa: BLE001
            if attempt == tries - 1:
                raise
            time.sleep(5)


def form(**kw):
    base = dict(election=ELECTION, search_on="1", CanFName="", CanLName="", CanNameSrch="2", office="All", cdistrict="",
                cgroup="", party="All", ComName="", ComNameSrch="2", committee="All", cfname="", clname="", namesearch="2",
                ccity="", cstate="", czipcode="", cdollar_minimum="", cdollar_maximum="", rowlimit=str(ROWS),
                csort1="DAT", csort2="CAN", cdatefrom="", cdateto="", queryformat="2", Submit="Submit")
    base.update(kw)
    return base


def rows_of(text):
    out = []
    for line in text.splitlines()[1:]:
        x = line.split("\t")
        if len(x) >= 5 and re.fullmatch(r"\d\d/\d\d/\d{4}", x[1]):
            out.append(x)
    return out


def fetch(script, start, end, **kw):
    """Every record from start to end, split into smaller date ranges where a
    query hits the row cap."""
    text = post(script, form(cdatefrom=start.strftime("%m/%d/%Y"), cdateto=end.strftime("%m/%d/%Y"), **kw))
    rows = rows_of(text)
    if len(rows) >= ROWS and start < end:
        mid = date.fromordinal((start.toordinal() + end.toordinal()) // 2)
        return fetch(script, start, mid, **kw) + fetch(script, date.fromordinal(mid.toordinal() + 1), end, **kw)
    return rows


def months(first, last):
    y, m = first
    while (y, m) <= last:
        nxt = (y + (m == 12), m % 12 + 1)
        yield date(y, m, 1), date.fromordinal(date(*nxt, 1).toordinal() - 1)
        y, m = nxt


def all_rows(script, **kw):
    out = []
    for a, b in months((2023, 1), (date.today().year, date.today().month)):
        out += fetch(script, a, b, **kw)
    return out


def iso(mdy):
    m, d, y = mdy.split("/")
    return f"{y}-{m}-{d}"


def is_org(name):
    return bool(ORG.search(" ".join(name.split()[1:])) or ALWAYS_ORG.search(name))


def classify(rows, own):
    parts = defaultdict(float)
    people = defaultdict(float)
    for x in rows:
        amount, kind, name, place = float(x[2] or 0), x[3], x[4].strip(), x[6]
        occupation = (x[7] if len(x) > 7 else "").strip()
        if name.startswith("STATE OF FLORIDA"):  # matching funds, paid via Financial Services
            parts["public"] += amount
        elif own.search(name) and FL_PLACE.search(place):
            parts["self"] += amount
        elif PARTY.match(name):
            parts["party"] += amount
        elif kind == "LOA":
            parts["other"] += amount
        elif is_org(name) or ORG_OCCUPATION.search(occupation):
            parts["pac"] += amount
        else:
            zip5 = (re.search(r"\d{5}", place) or [""])[0]
            people[(name, zip5)] += amount
    for total in people.values():
        if total > 0:
            parts["small" if total <= 200 else "large"] += total
    return {k: round(v) for k, v in parts.items() if round(v) > 0}


def display(name):
    """'SUSSMAN DONALD' -> 'Donald Sussman'; organizations keep their order."""
    if name in DISPLAY:
        return DISPLAY[name]
    words = name.title().split()
    if is_org(name) or len(words) < 2:
        return re.sub(r"\b(Pac|Llc|Inc|Afl-Cio)\b", lambda m: m.group(1).upper(), name.title())
    return " ".join(words[1:] + words[:1])


def money(v):
    if v >= 1e7:
        return f"${v / 1e6 + 1e-9:.1f} million"
    if v >= 1e6:
        return f"${v / 1e6 + 1e-9:.2f}".rstrip("0").rstrip(".") + " million"
    return f"${v:,.0f}"


AP_MONTHS = ["Jan.", "Feb.", "March", "April", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."]


def ap_date(iso_day):
    d = date.fromisoformat(iso_day)
    return f"{AP_MONTHS[d.month - 1]} {d.day}"


def committee_note(com):
    rows = all_rows("contrib.exe", election="All", search_on="4", ComName=com, ComNameSrch="1")
    rows = [x for x in rows if x[0].startswith(com)]
    total = sum(float(x[2] or 0) for x in rows)
    givers = defaultdict(float)
    for x in rows:
        givers[x[4].strip()] += float(x[2] or 0)
    top = sorted(givers.items(), key=lambda kv: -kv[1])[:3]
    through = max(iso(x[1]) for x in rows)
    names = "; ".join(f"{display(n)}, {money(v)}" for n, v in top)
    name = rows[0][0].replace(" (PAC)", "")
    return (f"His political committee, {name}, separately took in {money(total)} through {ap_date(through)}; "
            f"that money isn’t counted above (largest givers: {names})."), total


def main():
    out = ROOT / "data" / "research" / "florida_money.json"
    # The 8-hour refresh runs every research script; this one reads the state's
    # database at most once a day (py florida_money_2026.py --force to redo it).
    if "--force" not in sys.argv and out.exists() and time.time() - out.stat().st_mtime < 20 * 3600:
        print("florida_money.json is less than a day old; skipping (--force to refetch)")
        return
    if CACHE.exists():
        for old in CACHE.glob("*.tsv"):
            if not old.name.startswith(str(date.today())):
                old.unlink()
    races = []
    cands = []
    for cid, last, first, own, account, com in CANDIDATES:
        rows = [x for x in all_rows("contrib.exe", CanLName=last, CanFName=first, office="GOV") if "(GOV)" in x[0]]
        if not rows:
            print(cid, "no contributions on file")
            continue
        parts = classify(rows, re.compile(own))
        total = round(sum(float(x[2] or 0) for x in rows))
        # The expenditure search rejects date ranges, so it is one query; a campaign
        # with more than ROWS payments would be cut short, and is then left out.
        spent_rows = [x for x in rows_of(post("expend.exe", form(CanLName=last, CanFName=first, office="GOV", cpurpose="")))
                      if "(GOV)" in x[0]]
        spent = round(sum(float(x[2] or 0) for x in spent_rows)) if len(spent_rows) < ROWS else None
        fin = {"total": total, "parts": parts, "spent": spent,
               "from": min(iso(x[1]) for x in rows), "asOf": max(iso(x[1]) for x in rows),
               "source": "Florida Division of Elections", "url": f"{DOE}/candidates/CanDetail.asp?account={account}"}
        if com:
            fin["note"], ctotal = committee_note(com)
            print(f"  {com}: ${ctotal:,.0f}")
        print(cid, f"${total:,}", parts, "spent", spent, fin["from"], fin["asOf"])
        cand = {"id": cid, "name": NAMES[cid], "finance": fin}
        if cid in PARTIES:
            cand["party"] = PARTIES[cid]
        cands.append(cand)
    races.append({"id": "FL-GOV", "financeOnly": True, "candidates": cands})
    write("data/research/florida_money.json", races,
          "Florida governor candidates' campaign accounts grouped by contributor, from the Florida Division of Elections "
          "database, plus each major candidate's political committee in a note.", updated=date.today().isoformat())


if __name__ == "__main__":
    main()
