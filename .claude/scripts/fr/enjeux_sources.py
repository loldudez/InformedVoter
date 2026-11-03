"""Figures for "Les grands enjeux" (#/fr/enjeux) that no API serves, copied from their
publications and checked against the page text on the day in "accessed". enjeux.py
merges them into data/fr/enjeux.json.

Each entry keeps its source (title, URL, publication date, accessed) and, for the main
figure, the sentence it comes from (verbatim, under 25 words), so a later check can find
it again. When a newer edition comes out (INSEE's salaries every October, ONS's earnings
survey every October, PISA every three years), replace the entry rather than editing
numbers in place.

INSEE and ONS pages answer scripts; oecd.org refuses them, so the PISA figures were read
in the browser pane (Table I.2.1, Table I.2.6 and the chapter's text).
"""

ACCESSED = "2026-11-03"

# INSEE, private-sector salaries in 2025 (France, private-sector employees including
# apprentices, interns and subsidised contracts; excluding agriculture and household
# employers). Monthly, net of social contributions, in full-time equivalent (EQTP: pay
# converted to a full-time job held all year).
INSEE_SALAIRES = {
    "source": {
        "title": "Insee Première n° 2132, « Les salaires dans le secteur privé en 2025 »",
        "url": "https://www.insee.fr/fr/statistiques/9087193",
        "date": "2026-10-22",
        "accessed": ACCESSED,
    },
    "year": 2025,
    "quote": "La moitié des salariés du secteur privé perçoit moins de 2 238 euros net par mois en EQTP.",
    "median_net": 2238,
    "mean_net": 2797,
    "mean_gross": 3693,
    "d1_net": 1519,
    "d9_net": 4441,
    "p99_net": 10552,
    "median_below_mean_pct": 20.0,
    "real_mean_change_pct": 1.5,
    "inflation_pct": 0.9,
    "smic_net": 1426,
    # Figure 4: medians by sex. Pay by occupational category (figure 1) is published
    # only as means, which the page doesn't show.
    "median_net_women": 2128,
    "median_net_men": 2328,
    # Figure 3: thousands of full-time equivalent jobs by monthly net pay, in 100-euro
    # bands ([low, high, thousands]; None = open-ended).
    "distribution": [
        [None, 1300, 787], [1300, 1400, 165], [1400, 1500, 738], [1500, 1600, 932], [1600, 1700, 1055],
        [1700, 1800, 1168], [1800, 1900, 1141], [1900, 2000, 1068], [2000, 2100, 986], [2100, 2200, 896],
        [2200, 2300, 808], [2300, 2400, 726], [2400, 2500, 653], [2500, 2600, 590], [2600, 2700, 534],
        [2700, 2800, 483], [2800, 2900, 436], [2900, 3000, 397], [3000, 3100, 367], [3100, 3200, 335],
        [3200, 3300, 301], [3300, 3400, 274], [3400, 3500, 250], [3500, 3600, 230], [3600, 3700, 212],
        [3700, 3800, 194], [3800, 3900, 178], [3900, 4000, 165], [4000, 4100, 152], [4100, 4200, 140],
        [4200, 4300, 129], [4300, 4400, 119], [4400, 4500, 110], [4500, 4600, 102], [4600, 4700, 95],
        [4700, 4800, 89], [4800, 4900, 81], [4900, 5000, 76], [5000, 5100, 71], [5100, 5200, 66],
        [5200, 5300, 61], [5300, 5400, 57], [5400, 5500, 53], [5500, 5600, 50], [5600, 5700, 47],
        [5700, 5800, 43], [5800, 5900, 40], [5900, 6000, 38], [6000, 6100, 36], [6100, 6200, 34],
        [6200, 6300, 32], [6300, 6400, 30], [6400, 6500, 28], [6500, 6600, 26], [6600, 6700, 25],
        [6700, 6800, 23], [6800, 6900, 22], [6900, 7000, 21], [7000, 7100, 20], [7100, 7200, 19],
        [7200, 7300, 18], [7300, 7400, 17], [7400, 7500, 16], [7500, 7600, 15], [7600, 7700, 14],
        [7700, 7800, 14], [7800, 7900, 13], [7900, 8000, 13], [8000, 8100, 12], [8100, 8200, 12],
        [8200, 8300, 11], [8300, 8400, 11], [8400, 8500, 10], [8500, 8600, 10], [8600, 8700, 9],
        [8700, 8800, 9], [8800, 8900, 9], [8900, 9000, 8], [9000, None, 279],
    ],
    # Figures 2 and 5: net pay in EQTP in constant euros, index 100 in 1996.
    "index_1996": {
        "mean": [100.0, 100.6, 101.5, 103.1, 103.5, 104.2, 104.4, 104.4, 104.5, 105.7, 105.8, 107.6, 107.9, 109.2, 109.7,
                 110.1, 109.6, 109.4, 110.0, 111.2, 111.7, 112.7, 113.0, 114.2, 117.7, 115.5, 114.0, 112.9, 113.8, 115.5],
        "d1": [100.0, 101.4, 103.5, 104.6, 104.4, 106.2, 107.1, 107.1, 108.1, 110.3, 110.1, 110.9, 111.6, 113.8, 113.6,
               113.9, 114.0, 113.4, 113.4, 114.0, 114.2, 115.1, 115.2, 116.7, 117.6, 116.9, 116.5, 116.7, 117.8, 119.0],
        "median": [100.0, 100.7, 101.7, 102.5, 102.2, 102.7, 103.3, 103.4, 103.2, 104.3, 104.3, 105.5, 106.1, 108.2, 108.6,
                   108.9, 108.2, 108.2, 108.3, 109.1, 109.6, 110.5, 110.6, 113.4, 116.2, 114.2, 112.4, 111.8, 112.7, 114.1],
        "d9": [100.0, 100.1, 101.0, 102.8, 103.3, 104.3, 104.1, 103.9, 103.8, 105.0, 104.8, 106.3, 106.3, 108.0, 108.5,
               109.3, 109.1, 108.9, 110.0, 111.5, 112.0, 113.1, 113.6, 114.4, 119.0, 116.0, 114.1, 112.5, 113.3, 115.1],
    },
    "index_first_year": 1996,
    # INSEE on the 2020 peak: it "reflétait des modifications ponctuelles et
    # substantielles de la structure des emplois pendant la crise du Covid".
}

# ONS, Annual Survey of Hours and Earnings: median gross weekly earnings of full-time
# employees in April (UK). 2022 is the year of the EU's latest earnings survey; 2026 is
# the latest (provisional).
ONS_ASHE = {
    2022: {
        "weekly": 640.0,
        "quote": "Median weekly pay for full-time employees was £640 in April 2022",
        "source": {
            "title": "Office for National Statistics, “Employee earnings in the UK: 2022”",
            "url": "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/bulletins/annualsurveyofhoursandearnings/2022",
            "date": "2022-10-26",
            "accessed": ACCESSED,
        },
    },
    2026: {
        "weekly": 811.20,
        "quote": "Median weekly earnings for full-time employees were £811.20 in April 2026",
        "source": {
            "title": "Office for National Statistics, “Employee earnings in the UK: 2026”",
            "url": "https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/bulletins/annualsurveyofhoursandearnings/2026",
            "date": "2026-10-22",
            "accessed": ACCESSED,
        },
    },
}

# OECD, PISA 2025 Results (Volume I). Science was the main subject. Mean scores in
# science (Table I.2.1) and the change from 2022 in each subject (Table I.2.6); the OECD
# averages are in the chapter's text. An asterisk marks countries whose results need
# caution because a PISA sampling standard was not met (the Netherlands; the United
# States, where 9 states were excluded), per the Reader's Guide.
PISA_2025 = {
    "source": {
        "title": "OCDE, Résultats du PISA 2025 (Volume I), chapitre 2 « Student performance in PISA 2025 »",
        "url": "https://www.oecd.org/en/publications/pisa-2025-results-volume-i_73451bc5-en/full-report/student-performance-in-pisa-2025_23e075c2.html",
        "accessed": ACCESSED,
    },
    "notes_url": "https://www.oecd.org/en/publications/pisa-2025-results-volume-i_73451bc5-en/full-report/reader-s-guide_0364240f.html",
    "quote": "In mathematics, students scored 463 points on average across OECD countries.",
    "oecd_average": {"science": 482, "math": 463, "reading": 461},
    "science": {"UK": 511, "US": 502, "BE": 490, "DE": 486, "NL": 485, "FR": 483, "IT": 483, "ES": 477},
    # change 2022 -> 2025: [science, reading, mathematics]
    "change_2022": {
        "FR": [-4, -18, -16], "DE": [-7, -15, -11], "BE": [-1, -13, -10], "IT": [6, -7, -3],
        "ES": [-7, -23, -16], "NL": [-3, -18, -9], "UK": [12, 0, -1], "US": [2, -14, -2],
    },
    "caution": ["NL", "US"],
}
