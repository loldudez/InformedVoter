"""Researched positions for South Carolina's U.S. Senate race (Graham vs. Andrews).
Writes data/research/SC.json.

Sen. Darline Graham was appointed in July 2026 after the death of her brother,
Sen. Lindsey Graham, so she has almost no voting record and no published
platform. Positions come from debate and campaign coverage and from Andrews's
campaign site (read Oct. 25, 2026). Researched Oct. 25, 2026.

    py scripts/research/south_carolina_2026.py
"""

from common import P, article, page, write

READ = "2026-10-25"
DEBATE = article("SC Daily Gazette debate report, Oct. 12, 2026", "https://www.newsfromthestates.com/article/social-security-data-centers-and-healthcare-senate-candidates-exchange-jabs-while-talking", "2026-10-12")
MARION = article("ABC News 4, Sept. 12, 2026", "https://abcnews4.com/news/lowcountry-and-state-politics/annie-andrews-discusses-affordability-immigration-and-abortion-during-marion-stop-race-senator-us-campaign-priorities-november-election", "2026-09-12")
TRAIL = article("ABC News 4, Sept. 21, 2026", "https://abcnews4.com/newsletter-daily/south-carolina-senate-hopefuls-graham-andrews-campaign-statewide-ahead-of-nov-3-vote", "2026-09-21")
WBTV = article("WBTV, Aug. 26, 2026", "https://www.wbtv.com/2026/08/26/dr-annie-andrews-aims-become-south-carolinas-first-democratic-us-senator-years/", "2026-08-26")
TRANSITION = article("ABC News 4, Aug. 9, 2026", "https://abcnews4.com/news/state/i-feel-like-ive-been-drinking-out-of-a-fire-hose-graham-discusses-senate-transition-gop-primary-race-news-local-politics-charleston-south-carolina-ruuseel-fry-lindsey-graham-president-trump-government-campaign-local", "2026-08-09")
SITE = lambda note: page(f"Annie Andrews campaign site: {note}", "https://drannieandrews.com/", READ)  # noqa: E731

senate = {
    "id": "SC-SEN",
    "candidates": [
        {"id": "SC-SEN:andrews", "name": "Annie Andrews", "party": "D",
         "bio": "Pediatrician and the 2022 Democratic nominee for South Carolina's 1st Congressional District.",
         "officialSite": "https://drannieandrews.com/",
         "positions": P(
             ("soc-03", 2, MARION("Andrews supports restoring a framework like Roe v. Wade's"), "between a woman and her doctor"),
             ("soc-04", -2, SITE("Andrews's platform says to trust women to make their own reproductive decisions"), None),
             ("imm-01", 1, MARION("Andrews supports border security and enforcing existing immigration laws, while criticizing recent ICE tactics"), "we need to have a secure border to be a secure nation"),
             ("hea-03", 2, DEBATE("Andrews would expand Medicaid eligibility and reverse the 2025 Medicaid changes"), None),
             ("hea-07", 2, DEBATE("Andrews would restore the enhanced ACA subsidies"), None),
             ("hea-01", 1, DEBATE("Andrews would let anyone buy a discounted government health plan, though she calls single-payer Medicare for All outdated"), None),
             ("def-15", -2, DEBATE("Andrews opposes the Iran war, saying the money would be better spent on health care, infrastructure and schools"), None),
             ("eco-10", -1, WBTV("Andrews would use congressional oversight on tariffs she says are raising grocery prices"), None),
             ("eco-02", 1, TRAIL("Andrews would lower taxes for working South Carolina families"), None),
             ("eco-01", 1, DEBATE("Andrews would raise the Social Security wage cap so the highest earners pay more"), None),
             ("soc-07", 1, SITE("Andrews's platform calls for affordable child care"), None))},
        {"id": "SC-SEN:graham", "name": "Darline Graham", "party": "R",
         "bio": "U.S. senator since July 2026, appointed after the death of her brother, Sen. Lindsey Graham.",
         "positions": P(
             ("soc-03", -2, TRAIL("Graham opposes abortion"), None),
             ("imm-08", 1, TRAIL("Graham calls for stricter enforcement of immigration laws"), None),
             ("gov-05", 2, TRANSITION("Graham wanted the Senate to stay in session until it passed the SAVE America Act"), "I wanted to stay in session until we passed the Save America Act"),
             ("def-04", -1, DEBATE("Graham wants the Iran war to end, but not through Congress while Iran is still dangerous; Andrews said she voted against war powers resolutions three times"), None),
             ("def-15", 1, TRANSITION("Graham backs President Trump's approach to Iran"), "Iran would also be wise to listen to President Trump and make a deal."),
             ("def-14", 1, TRANSITION("Graham championed the Lindsey Graham Sanctioning Russia and Iran Act of 2026"), "a critical tool for President Trump"),
             ("hea-01", -1, DEBATE("Graham opposes government-funded health care for all"), None),
             ("hea-03", -1, DEBATE("Graham backs Medicaid work requirements"), None),
             ("hea-04", 1, DEBATE("Graham supports price transparency to spur competition and cosponsored a bill letting small businesses buy insurance at large-company rates"), None))},
    ],
    "notes": [{"text": "Darline Graham was appointed in July 2026 and has published no platform, so most questions are unclear for her rather than guessed.", "source": "ABC News 4", "url": "https://abcnews4.com/news/lowcountry-and-state-politics/annie-andrews-discusses-affordability-immigration-and-abortion-during-marion-stop-race-senator-us-campaign-priorities-november-election"}],
}

GOV_DEBATE = article("SC Daily Gazette debate report, Oct. 7, 2026", "https://www.newsfromthestates.com/article/sc-governor-candidates-agree-abortion-differ-gambling-and-medicaid", "2026-10-07")
WRDW = article("WRDW debate report, Oct. 6, 2026", "https://www.wrdw.com/2026/10/07/wilson-johnson-debate-race-sc-governor/", "2026-10-06")

governor = {
    "id": "SC-GOV",
    "candidates": [
        {"id": "SC-GOV:wilson", "name": "Alan Wilson", "party": "R",
         "bio": "South Carolina attorney general since 2011.",
         "positions": P(
             ("soc-03", -1, GOV_DEBATE("Wilson backs the six-week abortion ban, with exceptions for fatal fetal anomalies and for rape or incest up to 12 weeks"), None),
             ("soc-04", -1, GOV_DEBATE("Wilson would not make South Carolina's abortion restrictions any stricter"), None),
             ("hea-03", -2, WRDW("Wilson opposes expanding Medicaid, saying the state can't afford it"), "you're not going to be able to afford teacher pay raises"),
             ("soc-02", 1, GOV_DEBATE("Wilson is open to adding prison time for crimes motivated by race, gender or sexual orientation"), None))},
        {"id": "SC-GOV:johnson", "name": "Jermaine Johnson", "party": "D",
         "bio": "South Carolina state representative.",
         "positions": P(
             ("soc-04", -2, GOV_DEBATE("Johnson opposes South Carolina's anti-abortion laws and would not make them stricter"), None),
             ("soc-03", 1, GOV_DEBATE("Johnson opposes the Republican anti-abortion laws"), None),
             ("hea-03", 2, WRDW("Johnson would expand Medicaid"), "It's good economic policy"),
             ("soc-02", 2, GOV_DEBATE("Johnson says South Carolina needs a state hate crime law"), None),
             ("soc-08", 1, WRDW("Johnson would ban Flock license plate cameras statewide over privacy concerns and misuse"), None))},
    ],
}

write("data/research/SC.json", [senate, governor], "South Carolina U.S. Senate and governor races, researched Oct. 25, 2026.", updated=READ)
