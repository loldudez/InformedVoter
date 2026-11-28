"""Bills that members of Congress sponsored or cosponsored, turned into sourced positions
on the site's questions where no recorded vote answers them.

The owner asked (Nov. 27, 2026) for positions on universal health care, trans rights,
oil and gas, renewable energy, stock trading by members of Congress, money in politics
and immigration that rest on the voting record first and, where there is none, on what
members put their names to while in office. Recorded votes come first (house_votes.py,
senate_votes.py); a bill answers only the questions no vote answered.

The bills' records come from the Library of Congress's bill status files on govinfo.gov
(BILLSTATUS, public domain): the sponsor, every cosponsor and the date each signed on.
A sponsor's or cosponsor's name on a bill counts for the question the bill squarely
answers, at the strengths house_votes.py uses (2 for a bill about that one issue, 1 where
the bill reaches only part of the way). Not cosponsoring says nothing, and a cosponsor
who withdrew is left out. Each position cites the bill's page on congress.gov.

Files of finished Congresses never change and are downloaded once; the current
Congress's are read again when over a week old. Every file's own title is checked
against the one written here, so a wrong number can't attach a member to another bill.
"""

import re
import time
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CACHE = ROOT / "data" / "cache" / "bills"
BASE = "https://www.govinfo.gov/bulkdata/BILLSTATUS"
UA = "InformedVoterResearch/1.0"
CURRENT = 119
MAX_AGE = 7 * 24 * 3600

CITE = {"hr": "H.R.", "s": "S.", "hres": "H.Res.", "sres": "S.Res.", "hjres": "H.J.Res.", "sjres": "S.J.Res."}
PATH = {"hr": "house-bill", "s": "senate-bill", "hres": "house-resolution", "sres": "senate-resolution",
        "hjres": "house-joint-resolution", "sjres": "senate-joint-resolution"}

# Each family: the bills (Congress, type, number, the title the Library of Congress gives
# it, then the name and description shown where they differ from the family's), what
# they would do, and the stance a sponsor's or cosponsor's name on any of them gives.
# Where several families answer one question, the first one listed that a member signed
# wins.
DREAM = "which would give immigrants brought to the U.S. as children a path to citizenship"
DIGNITY = "which would give undocumented immigrants who have lived in the U.S. for years a path to legal status"
BLIND_TRUST = "which would require members of Congress, their spouses and dependent children to put their stocks and similar investments in a blind trust"

FAMILIES = [
    {"label": "the Medicare for All Act",
     "what": "which would cover every U.S. resident under one national health insurance program",
     "q": {"hea-01": 2},
     "bills": [(117, "hr", 1976, "Medicare for All Act of 2021"), (118, "hr", 3421, "Medicare for All Act"),
               (118, "s", 1655, "Medicare for All Act"), (119, "hr", 3069, "Medicare for All Act"),
               (119, "s", 1506, "Medicare for All Act")]},
    {"label": "the Transgender Bill of Rights",
     "what": "a resolution calling on the federal government to protect transgender and nonbinary people’s rights in law, including their access to medical care",
     "q": {"soc-12": 2},
     "bills": [(118, "hres", 269, "Recognizing that it is the duty of the Federal Government to develop and implement a Transgender Bill of Rights"),
               (118, "sres", 144, "A resolution recognizing that it is the duty of the Federal Government to develop and implement a Transgender Bill of Rights")]},
    {"label": "the Protection of Women and Girls in Sports Act",
     "what": "which would bar transgender women and girls from women’s and girls’ school sports",
     "q": {"soc-12": -1},
     "bills": [(118, "s", 613, "Protection of Women and Girls in Sports Act of 2023")]},
    {"label": "the Equality Act",
     "what": "which would add sexual orientation and gender identity to federal civil rights law",
     "q": {"soc-02": 2, "soc-12": 1},
     "bills": [(117, "hr", 5, "Equality Act"), (117, "s", 393, "Equality Act"), (118, "hr", 15, "Equality Act"),
               (118, "s", 5, "Equality Act"), (119, "hr", 15, "Equality Act"), (119, "s", 1503, "Equality Act")]},
    {"label": "the Protect Children’s Innocence Act",
     "what": "which would make gender-transition treatment of minors a federal crime",
     "q": {"soc-11": -2},
     "bills": [(118, "hr", 1399, "Protect Children’s Innocence Act"), (118, "s", 2357, "Protect Children’s Innocence Act")]},
    {"label": "the Green New Deal resolution",
     "what": "which calls for meeting all U.S. power demand from clean, renewable and zero-emission energy sources",
     "q": {"ene-01": 2},
     "bills": [(117, "hres", 332, "Recognizing the duty of the Federal Government to create a Green New Deal"),
               (118, "hres", 319, "Recognizing the duty of the Federal Government to create a Green New Deal"),
               (118, "sres", 173, "A resolution recognizing the duty of the Federal Government to create a Green New Deal")]},
    {"label": "a bill to stop members of Congress from trading individual stocks",
     "what": "which would require members of Congress to sell their individual stocks or put them in a blind trust",
     "q": {"gov-02": 2},
     "bills": [(117, "hr", 336, "TRUST in Congress Act", "the TRUST in Congress Act", BLIND_TRUST),
               (117, "s", 3494, "Ban Congressional Stock Trading Act", "the Ban Congressional Stock Trading Act", BLIND_TRUST),
               (118, "hr", 345, "TRUST in Congress Act", "the TRUST in Congress Act", BLIND_TRUST),
               (118, "s", 1171, "Ending Trading and Holdings In Congressional Stocks (ETHICS) Act", "the ETHICS Act",
                "which would require members of Congress, their spouses and dependent children to sell their stocks and similar investments or put them in a blind trust"),
               (119, "hr", 5106, "Restore Trust in Congress Act", "the Restore Trust in Congress Act",
                "which would bar members of Congress, their spouses and dependent children from owning or trading stocks and similar investments"),
               (119, "s", 1498, "Halting Ownership and Non-Ethical Stock Transactions (HONEST) Act", "the HONEST Act",
                "which would bar members of Congress and their spouses from holding, buying or selling stocks and similar investments while in office")]},
    {"label": "the DISCLOSE Act",
     "what": "which would require groups that spend more than $10,000 on elections to disclose their large donors",
     "q": {"gov-03": 2},
     "bills": [(118, "s", 512, "DISCLOSE Act of 2023")]},
    {"label": "a constitutional amendment limiting the Constitution’s rights to natural persons",
     "what": "which would have governments regulate, limit or prohibit campaign contributions and spending, and says spending money to influence elections is not speech",
     "q": {"gov-13": -2, "gov-11": 2},
     "bills": [(117, "hjres", 48, "Proposing an amendment to the Constitution of the United States providing that the rights extended by the Constitution are the rights of natural persons only"),
               (118, "hjres", 54, "Proposing an amendment to the Constitution of the United States providing that the rights protected and extended by the Constitution are the rights of natural persons only")]},
    {"label": "a constitutional amendment on campaign money",
     "what": "which would let Congress and the states limit money raised and spent to influence elections, including by barring corporations from such spending",
     "q": {"gov-11": 2, "gov-13": -1},
     "bills": [(117, "hjres", 1, "Proposing an amendment to the Constitution of the United States relating to contributions and expenditures intended to affect elections"),
               (118, "hjres", 13, "Proposing an amendment to the Constitution of the United States relating to the authority of Congress and the States to regulate contributions and expenditures")]},
    {"label": "a bill giving undocumented immigrants a path to legal status",
     "what": "",
     "q": {"imm-02": 2},
     "bills": [(117, "s", 264, "Dream Act of 2021", "the Dream Act of 2021", DREAM),
               (118, "s", 365, "Dream Act of 2023", "the Dream Act of 2023", DREAM),
               (118, "hr", 16, "American Dream and Promise Act of 2023", "the American Dream and Promise Act of 2023",
                "which would give immigrants brought to the U.S. as children, and people with Temporary Protected Status, a path to citizenship"),
               (118, "hr", 3599, "DIGNIDAD (Dignity) Act of 2023", "the Dignity Act of 2023", DIGNITY),
               (119, "hr", 4393, "DIGNIDAD (Dignity) Act of 2025", "the Dignity Act of 2025", DIGNITY)]},
    {"label": "the Farm Workforce Modernization Act",
     "what": "which would expand the H-2A farmworker visa program and let farmworkers earn legal status",
     "q": {"imm-09": 2},
     "bills": [(118, "hr", 4319, "Farm Workforce Modernization Act of 2023")]},
]

MONTHS = ["Jan.", "Feb.", "March", "April", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."]


def _day(d):
    y, m, dd = d[:10].split("-")
    return f"{MONTHS[int(m) - 1]} {int(dd)}, {y}"


def _norm(s):
    s = (s or "").replace("’", "'").replace("‘", "'")
    return re.sub(r"\s+", " ", s).strip().rstrip(".").lower()


def _list(items):
    return items[0] if len(items) == 1 else f"{', '.join(items[:-1])} and {items[-1]}"


def bill_url(c, t, n, tab=""):
    return f"https://www.congress.gov/bill/{c}th-congress/{PATH[t]}/{n}" + (f"/{tab}" if tab else "")


def _get(c, t, n):
    name = f"BILLSTATUS-{c}{t}{n}.xml"
    path = CACHE / name
    fresh = path.exists() and (c != CURRENT or time.time() - path.stat().st_mtime < MAX_AGE)
    if not fresh:
        CACHE.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(f"{BASE}/{c}/{t}/{name}", headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                body = r.read()
            ET.fromstring(body)  # a refusal page isn't XML
            path.write_bytes(body)
        except Exception:
            if not path.exists():
                raise
            # An old copy still has everyone who had signed on before it was saved.
        time.sleep(0.5)
    return ET.fromstring(path.read_bytes()).find("bill")


class Cosponsors:
    """Who sponsored and cosponsored each bill above, searchable by Bioguide id."""

    def __init__(self):
        self.signed = {}   # bioguide -> {(c, t, n): (role, date)}
        self.problems = []
        self.bills = 0
        for fam in FAMILIES:
            for c, t, n, title, *_ in fam["bills"]:
                try:
                    bill = _get(c, t, n)
                except Exception as e:  # noqa: BLE001  one missing file mustn't stop the others
                    self.problems.append(f"{CITE[t]} {n} ({c}th Congress): bill status unavailable ({e})")
                    continue
                if bill is None or not _norm(bill.findtext("title")).startswith(_norm(title)):
                    got = bill.findtext("title") if bill is not None else "nothing"
                    self.problems.append(f"{CITE[t]} {n} ({c}th Congress) is “{(got or '')[:80]}”, not “{title[:80]}”; left out")
                    continue
                self.bills += 1
                sp = bill.find("sponsors/item")
                if sp is not None and sp.findtext("bioguideId"):
                    self.signed.setdefault(sp.findtext("bioguideId"), {})[(c, t, n)] = ("introduced", bill.findtext("introducedDate") or "")
                for it in bill.findall("cosponsors/item"):
                    bg = it.findtext("bioguideId")
                    if not bg or it.findtext("sponsorshipWithdrawnDate"):
                        continue
                    self.signed.setdefault(bg, {})[(c, t, n)] = ("cosponsored", it.findtext("sponsorshipDate") or "")

    def positions(self, bioguide, member):
        """{question: position} from the bills `bioguide` sponsored or cosponsored, each
        marked kind "bill" so the site can say where it came from."""
        mine = self.signed.get(bioguide) or {}
        out = {}
        if not mine:
            return out
        for fam in FAMILIES:
            rows = [(b, mine[b[:3]]) for b in fam["bills"] if b[:3] in mine]
            if not rows:
                continue
            src = self._source(fam, rows, member)
            for q, stance in fam["q"].items():
                out.setdefault(q, {"stance": stance, "source": src, "kind": "bill"})
        return out

    @staticmethod
    def _source(fam, rows, member):
        """The latest bill the member signed, with its date and link, then the older
        ones of the same family: "and cosponsored its versions in the 117th and 118th
        Congresses", or by name where the bills differ."""
        name = lambda b: b[4] if len(b) > 4 else fam["label"]  # noqa: E731
        rows = sorted(rows, key=lambda r: (r[1][1], r[0][0]))
        bill, (role, date) = rows[-1]
        c, t, n = bill[:3]
        what = bill[5] if len(bill) > 5 else fam["what"]
        head = f"{CITE[t]} {n} ({c}th Congress), {name(bill)}{', ' + what if what else ''}: {member} {role} it" + (f" on {_day(date)}" if date else "")
        parts = []
        for verb in ("introduced", "cosponsored"):
            older = [b for b, (r, _) in rows[:-1] if r == verb]
            if not older:
                continue
            if all(name(b) == name(bill) for b in older):
                parts.append(f"{verb} its version{'s' if len(older) > 1 else ''} in the {_list([f'{b[0]}th' for b in older])} "
                             f"Congress{'es' if len(older) > 1 else ''}")
            else:
                groups = {}
                for b in older:
                    groups.setdefault(name(b), []).append(f"{CITE[b[1]]} {b[2]}, {b[0]}th Congress")
                parts.append(f"{verb} " + _list([f"{nm} ({'; '.join(cites)})" for nm, cites in groups.items()]))
        if parts:
            head += ", and " + " and ".join(parts) if all("its version" in p for p in parts) else "; also " + " and ".join(parts)
        return {"title": head, "url": bill_url(c, t, n, "" if role == "introduced" else "cosponsors"), "date": date[:10] or None}
