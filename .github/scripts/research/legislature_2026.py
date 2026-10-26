"""Researched bios, campaign sites and positions for state legislative candidates,
from their own campaign sites and local news (read Oct. 26, 2026). Writes
data/research/legislature/2026.json, which scripts/lib/legislature.py merges onto
the districts it reads from Wikipedia. Positions go only where a page states the
stance; anything else stays "unclear".

    py scripts/research/legislature_2026.py
"""

from common import P, article, page, write

READ = "2026-10-26"


def site(name, url):
    return lambda note: page(f"{name} campaign site: {note}", url, READ)


def cand(cid, name, party, bio, url, *rows):
    out = {"id": cid, "name": name, "party": party, "bio": bio}
    if url:
        out["officialSite"] = url
    if rows:
        out["positions"] = P(*rows)
    return out


# Oklahoma Senate District 32 (Lawton) ---------------------------------------------
NEWTON = site("Booker T. Newton", "https://www.bookertnewton.com/platform")
NEWTON_BIO = site("Booker T. Newton", "https://www.bookertnewton.com/meet-booker-t")
PENA = site("Valentin Peña", "https://www.vp2026.com/my-policies/")

# Oklahoma House District 85 (northwest Oklahoma City) ----------------------------
BRANHAM = site("Chelsey Branham", "https://branhamforoklahoma.com/")
NONDOC_HD85 = article("NonDoc, June 10, 2026", "https://nondoc.com/2026/06/10/cheat-sheet-3-democrats-run-to-succeed-cyndi-munson-in-hd-85/", "2026-06-10")
FALLIN = site("Joe Fallin", "https://www.joefallin.com/joespriorities")

RACES = [
    {"id": "OK-SS-032", "candidates": [
        cand("OK-SS-032:newton", "Booker T. Newton", "D",
             "Retired U.S. Army first sergeant (29 years); now helps soldiers move from military service to civilian jobs.",
             "https://www.bookertnewton.com/",
             ("edu-04", 2, NEWTON("Newton would prioritize increasing teacher pay"), "prioritize increasing teacher pay"),
             ("edu-06", -2, NEWTON("Newton would stop sending public school funds to private schools"), "end the absurd practice of sending public school funds to private schools"),
             ("edu-01", 1, NEWTON_BIO("Newton would strengthen public education"), None),
             ("sta-02", 1, NEWTON_BIO("Newton would strengthen public education"), None),
             ("hea-06", 1, NEWTON("Newton calls for mental health support for children and veterans"), None),
             ("soc-07", 1, NEWTON("Newton wants policies that address the rising cost of child care"), None),
             ("sta-06", 1, NEWTON("Newton would reform the legislative process and demand accountability"), "We must demand accountability and reform the legislative process"),
             ("gov-11", 1, NEWTON("Newton says government should not work just for millionaires funding campaigns"), None)),
        cand("OK-SS-032:pena", "Valentin Peña", "I",
             "Lawton independent running a grassroots campaign; says he takes no corporate or large private donations.",
             "https://www.vp2026.com/",
             ("sta-03", 2, PENA("Peña would raise the minimum wage immediately and tie it to inflation"), "Raise Minimum Wage Immediately"),
             ("eco-13", 2, PENA("Peña would make 32 hours a week full time"), "make 32 hours a week fulltime"),
             ("eco-01", 2, PENA("Peña proposes a 90% marginal tax rate above $1 million a year"), None),
             ("eco-12", 2, PENA("Peña proposes a 90% marginal tax rate above $1 million and lower taxes below it"), None),
             ("eco-02", 2, PENA("Peña would lower taxes on those earning under $1 million"), None),
             ("sta-04", 2, PENA("Peña would end property taxes on properties worth $500,000 or less"), None),
             ("hea-01", 2, PENA("Peña supports Medicare/SoonerCare for all"), "Medicare/Soonercare for all, including vision, dental and hearing."),
             ("hea-10", 2, PENA("Peña would include vision, dental and hearing coverage"), None),
             ("hea-06", 2, PENA("Peña would make therapy more affordable or free"), "Make therapy more affordable or free for the population."),
             ("soc-01", 2, PENA("Peña would protect protest and free speech rights, ending permit requirements for protests"), None),
             ("soc-03", 2, PENA("Peña would codify abortion access in the Oklahoma Constitution"), "codify abortion access in the Oklahoma Constitution"),
             ("soc-04", -2, PENA("Peña opposes legislation on people's bodies"), "no more legislation on our bodies"),
             ("edu-04", 2, PENA("Peña would give teachers raises and expanded benefits"), None),
             ("sta-02", 2, PENA("Peña would give schools more funding"), None),
             ("edu-09", 2, PENA("Peña supports free breakfast and lunch for all children"), "free breakfast and lunch for all children"),
             ("eco-09", 2, PENA("Peña would enshrine workers' and unionization rights"), "Workers rights and Unionization rights enshrined."),
             ("gov-04", 1, PENA("Peña would end gerrymandering in Oklahoma"), "End Gerrymandering in Oklahoma"),
             ("gov-12", 2, PENA("Peña wants transparency audits of all government spending"), None),
             ("sta-06", 2, PENA("Peña would ban lobbyists and stock trading by Oklahoma lawmakers and the governor's staff"), None),
             ("gov-06", 1, PENA("Peña supports automatic voter registration and paid voting holidays"), None),
             ("imm-08", -1, PENA("Peña would make ICE raids unconstitutional in Oklahoma"), "Make Ice raids unconstitutional in Oklahoma itself"))]},
    {"id": "OK-SH-085", "candidates": [
        cand("OK-SH-085:branham", "Chelsey Branham", "D",
             "State representative for House District 83 from 2018 to 2020; founder of One Whole Village Consulting and a Chickasaw citizen.",
             "https://branhamforoklahoma.com/",
             ("edu-01", 2, BRANHAM("Branham would restore full funding to classrooms"), "restoring full funding to our classrooms and paying teachers what they deserve"),
             ("sta-02", 2, BRANHAM("Branham would restore full funding to classrooms"), None),
             ("edu-04", 2, BRANHAM("Branham would pay teachers what they deserve"), None),
             ("sta-07", 1, BRANHAM("Branham would make college and technical training affordable"), None),
             ("edu-03", 1, BRANHAM("Branham would expand job readiness programs"), None),
             ("cri-07", 1, BRANHAM("Branham would redirect money from prisons to community programs"), "redirect money from prisons to programs that rebuild communities and keep families together"),
             ("eco-08", 1, BRANHAM("Branham would support local entrepreneurs and small businesses with tax incentives"), "support local entrepreneurs and small businesses with smart tax incentives"),
             ("ene-01", 1, BRANHAM("Branham would help transition the energy workforce to renewable sources"), None),
             ("hea-06", 2, NONDOC_HD85("Branham wants to increase mental health services"), "increase mental health services"),
             ("soc-03", 2, BRANHAM("Branham would defend reproductive freedom"), "defend reproductive freedom"),
             ("soc-04", -1, BRANHAM("Branham would defend reproductive freedom"), None)),
        cand("OK-SH-085:fallin", "Joe Fallin", "R",
             "Oklahoma City-area dentist and small-business owner.",
             "https://www.joefallin.com/",
             ("sta-08", 1, FALLIN("Fallin would ensure law enforcement has the tools, training and resources it needs"), None),
             ("cri-01", 1, FALLIN("Fallin would stand firmly with law enforcement"), "stand firmly with law enforcement"),
             ("gov-12", 2, FALLIN("Fallin would push for budget transparency"), "Joe will push for budget transparency"),
             ("sta-04", 2, FALLIN("Fallin calls property tax relief essential"), "Property tax relief is essential"))]},
]

write("data/research/legislature/2026.json", RACES,
      "State legislative candidates' bios, campaign sites and positions, researched Oct. 26, 2026.", updated=READ)
