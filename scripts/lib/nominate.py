"""Left-right scores for members of Congress: the first dimension of DW-NOMINATE, from
Voteview (voteview.com, at UCLA). It places every member on the one line that best
explains all the roll calls they have cast, from about -1 (most liberal) to +1 (most
conservative). House and Senate members share the scale, and a member keeps one score
for a whole career in either chamber (Adam Schiff's is -0.353 in the House files and the
Senate's).

It measures how members vote, not what they say: members who vote against their own
party's bills for not going far enough (some progressive Democrats, some hard-right
Republicans) score closer to the center than their stated positions would put them.

For the seat charts on #/congress (owner's request, Nov. 27, 2026: "for the democrats, the
further left they go, the darker blue they become ... Same for the republicans, the more
right they become, the darker red they are"). update_congress.py gives each sitting member
their score and lists the scores of members since the 107th Congress (2001) who aren't
sitting now and were on the 2026 ballot, so the page can place one elected again. A
member with no published score gets none: nothing is estimated here.

Voteview's member files, one per chamber and Congress, are cached in
data/cache/votes/voteview with senate_votes.py's roll calls; the current Congress's are
reread after a day.
"""

import re
import unicodedata

import senate_votes as SV

# The 107th Congress (2001) onward: anyone on the 2026 ballot who served since then, as
# Melissa Bean (House, 2005-2011) and Hilda Solis (2001-2009) did, keeps their score.
CONGRESSES = tuple(range(107, SV.CURRENT + 1))
PARTY = {"100": "D", "200": "R", "328": "I"}


def _fold(s):
    """Lowercase without accents, as the page's fold() (js/data/holders.js) does."""
    return "".join(c for c in unicodedata.normalize("NFKD", s or "") if not unicodedata.combining(c)).lower()


def last_name_of(name):
    """The page's lastNameOf (js/data/holders.js): the last word, without a nickname in
    parentheses or a "Jr." after it."""
    words = re.sub(r"\(.*?\)|,? (jr|sr|ii|iii|iv)\.?$", "", _fold(name)).split()
    return words[-1] if words else ""


def _names(bioname):
    """("last", ["first", ...]) from Voteview's "LAST, First Middle (Nick), Jr.", folded
    like the page's lastNameOf: the last word of the last name ("van drew" gives "drew",
    "ocasio-cortez" stays whole), and every given name and nickname as first names
    (letters only)."""
    last, _, given = bioname.partition(",")
    nick = re.findall(r"\(([^)]+)\)", given)
    given = re.sub(r"\([^)]*\)|,?\s*\b(Jr|Sr|II|III|IV)\b\.?", " ", given)
    firsts = [w for w in (re.sub(r"[^a-z-]", "", _fold(x)) for x in " ".join([given, *nick]).split()) if len(w) > 1]
    words = _fold(last).split()
    return (words[-1] if words else ""), firsts


class Scores:
    def __init__(self, congresses=CONGRESSES):
        self.rows, self.problems = [], []
        for c in congresses:
            for ch in ("H", "S"):
                try:
                    got = SV._get("members", c, ch)
                except Exception as e:  # noqa: BLE001
                    self.problems.append(f"Voteview's {ch}{c} member file couldn't be read ({e})")
                    continue
                for r in got:
                    if r["chamber"] not in ("House", "Senate"):
                        continue
                    try:
                        dim1 = round(float(r["nominate_dim1"]), 3)
                    except (TypeError, ValueError):
                        continue  # no published score
                    last, firsts = _names(r["bioname"])
                    code = r["party_code"].split(".")[0]  # the 117th Congress's files print "100.0"
                    self.rows.append({
                        "congress": c, "chamber": r["chamber"], "bioguide": r["bioguide_id"], "st": r["state_abbrev"],
                        "party": PARTY.get(code, "I"), "last": last, "first": firsts, "dim1": dim1,
                        "votes": int(float(r["nominate_number_of_votes"] or 0)), "died": bool(r.get("died")),
                    })
        if not self.rows:
            raise RuntimeError("; ".join(self.problems) or "no Voteview member file could be read")

    def of(self, bioguide, party=None):
        """A member's score by Bioguide id, from the latest Congress they served in; for a
        member who changed parties, the score Voteview gives them in their current one
        (Kevin Kiley's as an independent)."""
        hits = [r for r in self.rows if bioguide and r["bioguide"] == bioguide]
        if not hits:
            return None
        latest = max(r["congress"] for r in hits)
        hits = [r for r in hits if r["congress"] == latest]
        hits.sort(key=lambda r: (r["party"] == party, r["votes"]), reverse=True)
        return hits[0]["dim1"]

    def senator(self, st, name):
        """The Bioguide id of the sitting senator from `st` named `name` (Wikipedia's list
        gives none), or None unless exactly one matches."""
        last = SV._norm(SV._last_name(name))
        first = SV._norm(name.split()[0]) if name.split() else ""
        letters = lambda s: re.sub(r"[^a-z]", "", s)  # noqa: E731
        hits = {r["bioguide"]: r for r in self.rows
                if r["congress"] == SV.CURRENT and r["chamber"] == "Senate" and r["st"] == st
                and (letters(r["last"]) == last or last.endswith(letters(r["last"])) or letters(r["last"]).endswith(last))}
        if len(hits) > 1 and first:
            hits = {k: r for k, r in hits.items() if any(f[:3] == first[:3] for f in r["first"])} or hits
        return next(iter(hits)) if len(hits) == 1 else None

    def former(self, sitting, ballot=None):
        """Members of these Congresses with a score who aren't sitting now (and are alive):
        [{"st", "last", "first", "party", "nom"}], each from the latest Congress they served
        in, for the page to place one elected again in 2026. With `ballot`, a set of
        (state, last name) from the 2026 races, only the former members who match one;
        without it, only those of the last three Congresses."""
        latest = {}
        for r in self.rows:
            if ballot is None and r["congress"] < SV.CURRENT - 2:
                continue
            if ballot is not None and (r["st"], r["last"]) not in ballot:
                continue
            if r["bioguide"] and r["bioguide"] not in sitting and not r["died"]:
                if r["bioguide"] not in latest or (r["congress"], r["votes"]) > (latest[r["bioguide"]]["congress"], latest[r["bioguide"]]["votes"]):
                    latest[r["bioguide"]] = r
        return sorted(({"st": r["st"], "last": r["last"], "first": r["first"], "party": r["party"], "nom": r["dim1"]}
                       for r in latest.values()), key=lambda m: (m["st"], m["last"]))
