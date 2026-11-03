"""Build data/fr/enjeux.json: the figures behind "Les grands enjeux" (#/fr/enjeux),
France's economy, inflation, immigration, crime, wealth gap, education and salaries,
next to Germany, Belgium, Italy, Spain, the Netherlands, the United Kingdom and the
United States.

Sources, read once a day by scripts/refresh_all.py:
  * Eurostat (JSON-stat API): inflation (HICP), unemployment, GDP growth, public debt
    and deficit, first residence permits, early school leavers, public spending on
    education, minimum wages and the Structure of Earnings Survey (median pay, overall
    and by sector).
  * The OECD (SDMX API): consumer prices and unemployment for the UK and the US,
    permanent-type migration and asylum seekers, the foreign-born population, income
    inequality and poverty (Income Distribution Database), wealth shares (Wealth
    Distribution Database), young adults' degrees, minimum wages, and its yearly
    exchange rates and purchasing power parities.
  * The World Bank (API): annual GDP growth and GDP per head, population, the UN's
    migrant-stock estimates and UNODC's homicide rates.
  * The U.S. Bureau of Labor Statistics (public API, no key): median usual weekly
    earnings of full-time wage and salary workers (Current Population Survey).
  * France's Interior Ministry statistics service (SSMSI), on data.gouv.fr: crimes
    recorded by the police and the gendarmerie, by region, added up for France.
  * Publications with no API (INSEE's 2025 salaries, the ONS earnings survey, PISA
    2025) are typed in enjeux_sources.py, each checked against its page.

Comparisons take every country from one source wherever one exists, so definitions
match; where only national sources exist (median salaries in the UK and the US) the
page says so. Pay is compared by its median, never its mean, which the highest
salaries pull up: no source publishes medians by occupation for these countries
(Eurostat's and the OECD's pay by occupation, teachers' and health workers' included,
are means), so jobs are compared by sector. Money is converted two ways with the
OECD's yearly figures: at the average exchange rate, and at purchasing power parities
for household consumption ("euros at French prices": what the amount buys in France).

Each block keeps its last good values when its source can't be read; the block's id
then goes into "stale", and the page says those figures weren't refreshed.

    py scripts/fr/enjeux.py
"""

import csv
import gzip
import io
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import frwiki  # noqa: E402
from frwiki import W  # noqa: E402
import enjeux_sources as S  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
ROOT = frwiki.ROOT
OUT = ROOT / "data" / "fr" / "enjeux.json"

ESTAT = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data"
OECD = "https://sdmx.oecd.org/public/rest/data"
WB = "https://api.worldbank.org/v2/country"
BLS = "https://api.bls.gov/publicAPI/v1/timeseries/data/"
SSMSI = "https://www.data.gouv.fr/api/1/datasets/621df2954fa5a3b5a023e23c/"

# The countries compared, keyed as on the page; the OECD and the World Bank use ISO3.
ISO3 = {"FR": "FRA", "DE": "DEU", "BE": "BEL", "IT": "ITA", "ES": "ESP", "NL": "NLD", "UK": "GBR", "US": "USA"}
FROM_ISO3 = {v: k for k, v in ISO3.items()} | {"EUU": "EU", "OECD": "OECD", "UKB": "UK", "BEFL": "BE-FL", "BEFR": "BE-FR"}
OECD_AREAS = "+".join(ISO3.values())
EU_GEO = ["FR", "DE", "BE", "IT", "ES", "NL", "EU27_2020"]
GEO = {"EU27_2020": "EU"}
CURRENCY = {"UK": "GBP", "US": "USD"}  # everyone else pays in euros

# The HICP's French breakdown shown on the page.
HICP_PARTS = ["CP01", "NRG", "SERV", "IGD_NNRG", "TOT_X_NRG_FOOD"]
# OECD categories of permanent-type migration.
MIG_TYPES = ["WO", "AC", "FA", "HU", "FR", "OT"]
# NACE sections in the EU's earnings survey, which leaves out farming and public
# administration (A and O), with all of them together first; names as INSEE's NAF.
SECTORS = {
    "B-S_X_O": ("Tous secteurs (hors administration publique)", "All sectors (except public administration)"),
    "B": ("Industries extractives", "Mining and quarrying"),
    "C": ("Industrie manufacturière", "Manufacturing"),
    "D": ("Électricité et gaz", "Electricity and gas"),
    "E": ("Eau, assainissement et déchets", "Water, sewerage and waste"),
    "F": ("Construction", "Construction"),
    "G": ("Commerce", "Wholesale and retail trade"),
    "H": ("Transports et entreposage", "Transport and storage"),
    "I": ("Hébergement et restauration", "Accommodation and food services"),
    "J": ("Information et communication", "Information and communication"),
    "K": ("Activités financières et d’assurance", "Finance and insurance"),
    "L": ("Activités immobilières", "Real estate"),
    "M": ("Activités spécialisées, scientifiques et techniques", "Professional, scientific and technical activities"),
    "N": ("Activités de services administratifs et de soutien", "Administrative and support services"),
    "P": ("Enseignement", "Education"),
    "Q": ("Santé humaine et action sociale", "Human health and social work"),
    "R": ("Arts, spectacles et activités récréatives", "Arts, entertainment and recreation"),
    "S": ("Autres activités de services", "Other services"),
}
SECTOR_NOTES = {
    "P": ("Tout le personnel des écoles, des universités et des organismes de formation, pas seulement les enseignants.",
          "All staff of schools, universities and training bodies, not only teachers."),
    "Q": ("Tout le personnel salarié des hôpitaux, des cliniques, des cabinets médicaux, des maisons de retraite et de l’action sociale, pas seulement les soignants.",
          "All employees of hospitals, clinics, medical practices, care homes and social services, not only nurses and doctors."),
}


def get(url, data=None, headers=None, timeout=180, tries=3):
    h = {"User-Agent": W.UA, "Accept-Encoding": "gzip", **(headers or {})}
    for k in range(tries):
        try:
            req = urllib.request.Request(url, data=data, headers=h)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                b = r.read()
                return gzip.decompress(b) if r.headers.get("Content-Encoding") == "gzip" else b
        except urllib.error.HTTPError as e:
            if e.code in (400, 403, 404) or k == tries - 1:
                raise
        except (urllib.error.URLError, TimeoutError):
            if k == tries - 1:
                raise
        time.sleep(10 * (k + 1))
    raise RuntimeError("unreachable")


def num(v, d=2):
    return None if v is None else round(float(v), d)


# ---------------------------------------------------------------- source readers

def eurostat(ds, since=None, **params):
    """Records ({dimension: code, "value", "flag"}) of a Eurostat dataset; params pin
    dimensions (a list pins several codes)."""
    q = [(k, x) for k, v in params.items() for x in (v if isinstance(v, (list, tuple)) else [v])]
    if since:
        q.append(("sinceTimePeriod", since))
    q.append(("lang", "EN"))
    j = json.loads(get(f"{ESTAT}/{ds}?" + urllib.parse.urlencode(q)))
    ids, size = j["id"], j["size"]
    cats = []
    for d in ids:
        idx = j["dimension"][d]["category"]["index"]
        cats.append(sorted(idx, key=idx.get))
    values, status = j.get("value", {}), j.get("status", {})
    items = values.items() if isinstance(values, dict) else enumerate(values)
    recs = []
    for flat, v in items:
        if v is None:
            continue
        i, rec = int(flat), {}
        for d, n, c in reversed(list(zip(ids, size, cats))):
            rec[d] = c[i % n]
            i //= n
        rec["value"] = v
        rec["flag"] = status.get(str(flat), "") if isinstance(status, dict) else ""
        recs.append(rec)
    if not recs:
        raise ValueError(f"Eurostat {ds}: no values")
    return recs, {"dataset": ds, "updated": (j.get("updated") or "")[:10]}


def by(recs, key="geo", d=2):
    """{key's code: [[period, value(, flag)], ...]} sorted by period."""
    out = {}
    for r in sorted(recs, key=lambda r: r["time"]):
        pt = [r["time"], num(r["value"], d)] + ([r["flag"]] if r.get("flag") else [])
        out.setdefault(GEO.get(r[key], r[key]), []).append(pt)
    return out


def oecd(flow, key, start=None):
    """Rows (column code -> value) of an OECD dataflow, observations only."""
    q = {"dimensionAtObservation": "AllDimensions", "format": "csvfile"}
    if start:
        q["startPeriod"] = start
    text = get(f"{OECD}/{flow}/{key}?" + urllib.parse.urlencode(q), timeout=300).decode("utf-8-sig")
    time.sleep(3)  # the OECD's API limits how many requests a minute it answers
    rows = [r for r in csv.DictReader(io.StringIO(text)) if r.get("OBS_VALUE") not in (None, "")]
    for r in rows:
        r.setdefault("TIME_PERIOD", r.get("REF_PERIOD", ""))  # for tables with no time dimension
        if not r["TIME_PERIOD"]:
            r["TIME_PERIOD"] = r.get("REF_PERIOD", "")
    if not rows:
        raise ValueError(f"OECD {flow}: no values")
    return rows


def oecd_series(rows, d=2, scale=1.0):
    out = {}
    for r in sorted(rows, key=lambda r: r["TIME_PERIOD"]):
        k = FROM_ISO3.get(r["REF_AREA"], r["REF_AREA"])
        s = out.setdefault(k, [])
        if s and s[-1][0] == r["TIME_PERIOD"]:
            continue  # one value per period
        s.append([r["TIME_PERIOD"], num(float(r["OBS_VALUE"]) * scale, d)])
    return out


def worldbank(indicator, mrv, d=2):
    codes = ";".join(list(ISO3.values()) + ["EUU"])
    j = json.loads(get(f"{WB}/{codes}/indicator/{indicator}?format=json&mrv={mrv}&per_page=500"))
    if len(j) < 2 or not j[1]:
        raise ValueError(f"World Bank {indicator}: no data")
    out = {}
    for r in j[1]:
        if r["value"] is not None:
            out.setdefault(FROM_ISO3.get(r["countryiso3code"], r["countryiso3code"]), []).append([r["date"], num(r["value"], d)])
    for v in out.values():
        v.sort()
    return out, (j[0].get("lastupdated") or "")[:10]


# ---------------------------------------------------------------- source labels

def src_estat(meta, fr, en):
    ds = meta["dataset"]
    return {"fr": f"Eurostat, {fr}", "en": f"Eurostat, {en}", "dataset": ds, "updated": meta["updated"],
            "url": f"https://ec.europa.eu/eurostat/databrowser/view/{ds}/default/table?lang=fr"}


def src_oecd(flow, fr, en):
    agency, df, _ = flow.split(",")
    return {"fr": f"OCDE, {fr}", "en": f"OECD, {en}", "dataset": df,
            "url": "https://data-explorer.oecd.org/vis?" + urllib.parse.urlencode({"df[ds]": "dsDisseminateFinalDMZ", "df[id]": df, "df[ag]": agency})}


def src_wb(indicator, updated, fr, en):
    return {"fr": f"Banque mondiale, {fr}", "en": f"World Bank, {en}", "dataset": indicator, "updated": updated,
            "url": f"https://data.worldbank.org/indicator/{indicator}"}


# ---------------------------------------------------------------- blocks

def b_hicp():
    recs, meta = eurostat("prc_hicp_minr", "2018-01", geo=EU_GEO, unit="RCH_A", coicop18="TOTAL")
    parts, _ = eurostat("prc_hicp_minr", "2018-01", geo="FR", unit="RCH_A", coicop18=HICP_PARTS)
    return {"source": src_estat(meta, "indice des prix à la consommation harmonisé (IPCH), glissement annuel",
                                "harmonised index of consumer prices (HICP), annual rate"),
            "series": by(recs, d=1), "parts": by(parts, key="coicop18", d=1)}


def b_cpi_ukus():
    flow = "OECD.SDD.TPS,DSD_PRICES@DF_PRICES_ALL,1.0"
    rows = oecd(flow, "GBR+USA.M.N.CPI.PA._T.N.GY", "2018-01")
    return {"source": src_oecd(flow, "prix à la consommation (indices nationaux), glissement annuel",
                               "consumer prices (national indices), annual rate"), "series": oecd_series(rows, d=1)}


def b_unemp():
    recs, meta = eurostat("une_rt_m", "2015-01", geo=EU_GEO, s_adj="SA", age="TOTAL", sex="T", unit="PC_ACT")
    return {"source": src_estat(meta, "taux de chômage mensuel (BIT), corrigé des variations saisonnières",
                                "monthly unemployment rate (ILO), seasonally adjusted"), "series": by(recs, d=1)}


def b_unemp_ukus():
    flow = "OECD.SDD.TPS,DSD_LFS@DF_IALFS_UNE_M,1.0"
    rows = oecd(flow, "GBR+USA.UNE_LF_M.PT_LF_SUB..Y._T.Y_GE15..M", "2015-01")
    return {"source": src_oecd(flow, "taux de chômage mensuel, corrigé des variations saisonnières",
                               "monthly unemployment rate, seasonally adjusted"), "series": oecd_series(rows, d=1)}


def b_gdp_q():
    recs, meta = eurostat("namq_10_gdp", "2015-Q1", geo=EU_GEO, unit="CLV_PCH_PRE", s_adj="SCA", na_item="B1GQ")
    return {"source": src_estat(meta, "PIB en volume, variation par rapport au trimestre précédent",
                                "real GDP, change on the previous quarter"), "series": by(recs, d=1)}


def b_gdp_a():
    s, upd = worldbank("NY.GDP.MKTP.KD.ZG", 12, d=1)
    return {"source": src_wb("NY.GDP.MKTP.KD.ZG", upd, "croissance annuelle du PIB en volume", "annual real GDP growth"), "series": s}


def b_debt():
    q, meta_q = eurostat("gov_10q_ggdebt", "2015-Q1", geo=EU_GEO, unit="PC_GDP", sector="S13", na_item="GD")
    a, meta_a = eurostat("gov_10dd_edpt1", "2007", geo=EU_GEO, unit="PC_GDP", sector="S13", na_item=["GD", "B9"])
    return {"source": src_estat(meta_q, "dette publique trimestrielle (au sens de Maastricht), en % du PIB",
                                "quarterly government debt (Maastricht definition), % of GDP"),
            "source_annual": src_estat(meta_a, "dette et déficit publics annuels, en % du PIB",
                                       "annual government debt and deficit, % of GDP"),
            "quarterly": by(q, d=1),
            "debt": by([r for r in a if r["na_item"] == "GD"], d=1),
            "balance": by([r for r in a if r["na_item"] == "B9"], d=1)}


def b_gdp_pc():
    ppp, upd = worldbank("NY.GDP.PCAP.PP.CD", 6, d=0)
    usd, _ = worldbank("NY.GDP.PCAP.CD", 6, d=0)
    eur, meta = eurostat("nama_10_pc", "2015", geo="FR", unit="CP_EUR_HAB", na_item="B1GQ")
    return {"source": src_wb("NY.GDP.PCAP.PP.CD", upd, "PIB par habitant", "GDP per head"),
            "source_fr": src_estat(meta, "PIB par habitant en euros courants", "GDP per head in current euros"),
            "ppp": ppp, "usd": usd, "fr_eur": by(eur, d=0)["FR"]}


def b_min_wage():
    flow = "OECD.ELS.SAE,DSD_EARNINGS@MW_CURP,1.0"
    rows = [r for r in oecd(flow, f"{OECD_AREAS}.SM_WG..A...", "2015") if r["PAY_PERIOD"] == "A"]
    flow2 = "OECD.ELS.SAE,DSD_EARNINGS@MIN2AVE,1.0"
    ratio = [r for r in oecd(flow2, f"{OECD_AREAS}......", "2015") if r["AGGREGATION_OPERATION"] == "MEDIAN"]
    eu, meta = eurostat("earn_mw_cur", "2024-S1", geo=["FR", "DE", "BE", "ES", "NL"], currency="EUR")
    return {"source": src_oecd(flow, "salaires minimums légaux, montant annuel brut", "statutory minimum wages, gross annual amount"),
            "source_ratio": src_oecd(flow2, "salaire minimum rapporté au salaire médian des salariés à temps plein",
                                     "minimum wage relative to the median wage of full-time workers"),
            "source_monthly": src_estat(meta, "salaires minimums mensuels bruts", "gross monthly minimum wages"),
            "annual": oecd_series(rows, d=0), "to_median": oecd_series(ratio, d=1), "monthly_eur": by(eu, d=0)}


def b_population():
    s, upd = worldbank("SP.POP.TOTL", 12, d=0)
    return {"source": src_wb("SP.POP.TOTL", upd, "population", "population"), "series": s}


def b_migrant_share():
    s, upd = worldbank("SM.POP.TOTL.ZS", 8, d=1)
    return {"source": src_wb("SM.POP.TOTL.ZS", upd, "part des personnes nées à l’étranger dans la population (estimations de l’ONU)",
                             "share of people born abroad in the population (UN estimates)"), "series": s}


def b_migration():
    flow = "OECD.ELS.IMD,DSD_MIG_INT@DF_MIG_INT_PER,1.0"
    rows = oecd(flow, f"{OECD_AREAS}....", "2015")
    cats = {}
    for r in rows:
        if r["MIGRATION_TYPE"] in MIG_TYPES:
            k = FROM_ISO3[r["REF_AREA"]]
            cats.setdefault(k, {}).setdefault(r["TIME_PERIOD"], {})[r["MIGRATION_TYPE"]] = round(float(r["OBS_VALUE"]))
    flow2 = "OECD.ELS.IMD,DSD_MIG@DF_MIG,1.0"
    asy = oecd(flow2, f"{OECD_AREAS}.W.A.B13._T...", "2015")
    flow3 = "OECD.ELS.IMD,DSD_MIG_F@DF_MIG_POPF,1.0"
    fb = [r for r in oecd(flow3, f"{OECD_AREAS}.W.A.B14._T...", "2015") if r["BIRTH_COUNTRY"] == "W"]
    return {"source": src_oecd(flow, "entrées de migrants à titre permanent, par catégorie (données standardisées)",
                               "permanent-type migrant inflows by category (standardised)"),
            "source_asylum": src_oecd(flow2, "demandeurs d’asile (entrées)", "asylum seekers (inflows)"),
            "source_born": src_oecd(flow3, "population née à l’étranger", "foreign-born population"),
            "permanent": {k: dict(sorted(v.items())) for k, v in cats.items()},
            "asylum": oecd_series(asy, d=0), "foreign_born": oecd_series(fb, d=0)}


def b_permits_fr():
    recs, meta = eurostat("migr_resfirst", "2010", geo="FR", reason=["TOTAL", "FAM", "EDUC", "EMP", "OTH"],
                          duration="TOTAL", citizen="TOTAL", unit="PER")
    return {"source": src_estat(meta, "premiers titres de séjour délivrés, par motif", "first residence permits, by reason"),
            "series": by(recs, key="reason", d=0)}


def b_crime_fr():
    meta = json.loads(get(SSMSI))
    res = next(r for r in meta["resources"] if r["format"] == "csv" and r["title"].startswith("REG "))
    text = get(res["url"], timeout=300).decode("utf-8-sig")
    rows = list(csv.DictReader(io.StringIO(text), delimiter=";"))
    counts, units, pop, homes, missing = {}, {}, {}, {}, set()
    for r in rows:
        y = int(r["annee"])
        pop.setdefault(y, {})[r["Code_region"]] = int(r["insee_pop"])
        homes.setdefault(y, {})[r["Code_region"]] = int(r["insee_log"])
        units[r["indicateur"]] = r["unite_de_compte"]
        if r["nombre"] in ("", "NA"):
            missing.add((r["indicateur"], y))
            continue
        c = counts.setdefault(r["indicateur"], {})
        c[y] = c.get(y, 0) + int(r["nombre"])
    if len({len(p) for p in pop.values()}) != 1:
        raise ValueError("the SSMSI file doesn't cover the same regions every year")
    popn = {y: sum(p.values()) for y, p in pop.items()}
    homen = {y: sum(p.values()) for y, p in homes.items()}
    out = {}
    for ind, c in counts.items():
        # Like the SSMSI, burglaries per 1,000 homes and everything else per 1,000 people.
        per = "homes" if ind.startswith("Cambriolages") else "people"
        base = homen if per == "homes" else popn
        out[ind] = {"unit": units[ind], "per": per, "series": [[str(y), n, round(1000 * n / base[y], 5)]
                                                                for y, n in sorted(c.items()) if (ind, y) not in missing]}
    return {"source": {"fr": "Ministère de l’Intérieur (SSMSI), délinquance enregistrée par la police et la gendarmerie, par région",
                       "en": "Interior Ministry (SSMSI), crimes recorded by the police and the gendarmerie, by region",
                       "url": meta.get("page") or "https://www.data.gouv.fr/fr/datasets/621df2954fa5a3b5a023e23c/",
                       "updated": (res.get("last_modified") or "")[:10], "file": res["title"]},
            "population": {str(y): n for y, n in sorted(popn.items())}, "indicators": out}


def b_homicide():
    s, upd = worldbank("VC.IHR.PSRC.P5", 12, d=2)
    s.pop("EU", None)  # the World Bank's EU figure stops in 2015
    return {"source": src_wb("VC.IHR.PSRC.P5", upd, "homicides volontaires pour 100 000 habitants (ONUDC)",
                             "intentional homicides per 100,000 people (UNODC)"), "series": s}


def b_inequality():
    flow = "OECD.WISE.INE,DSD_WISE_IDD@DF_IDD,1.0"
    rows = [r for r in oecd(flow, f"{OECD_AREAS}.A.......", "2010") if r["AGE"] == "_T" and r["DEFINITION"] == "D_CUR"]
    pick = {"gini": ("INC_DISP_GINI", "_Z", 100), "s80s20": ("QR_INC_DISP", "_Z", 1), "poverty50": ("PR_INC_DISP", "PL_50", 1),
            "poverty60": ("PR_INC_DISP", "PL_60", 1)}
    out = {}
    for name, (measure, line, scale) in pick.items():
        out[name] = oecd_series([r for r in rows if r["MEASURE"] == measure and r["POVERTY_LINE"] == line], d=2 if name == "s80s20" else 1, scale=scale)
    out["median"] = oecd_series([r for r in rows if r["MEASURE"] == "INC_DISP" and r["STATISTICAL_OPERATION"] == "MEDIAN"], d=0)
    flow2 = "OECD.WISE.INE,DSD_WEALTH@DF_WEALTH,1.0"
    wrows = oecd(flow2, f"{OECD_AREAS}.....", "2010")
    wealth = {m: oecd_series([r for r in wrows if r["MEASURE"] == m], d=1) for m in ("SH_TOP10", "SH_TOP1", "SH_BOT40")}
    return {"source": src_oecd(flow, "base de données sur la distribution des revenus (revenu disponible, après impôts et prestations)",
                               "Income Distribution Database (disposable income, after taxes and benefits)"),
            "source_wealth": src_oecd(flow2, "base de données sur la distribution du patrimoine", "Wealth Distribution Database"),
            **out, "wealth": wealth}


def b_education():
    flow = "OECD.EDU.IMEP,DSD_EAG_LSO_EA@DF_LSO_NEAC_DISTR_EA,1.0"
    rows = [r for r in oecd(flow, f"{OECD_AREAS}._T.Y25T34" + "." * 14, "2015")
            if r["ATTAINMENT_LEV"] == "ISCED11A_5T8" and r["STATISTICAL_OPERATION"] == "OBS"]
    early, meta_e = eurostat("edat_lfse_14", "2010", geo=EU_GEO, sex="T", wstatus="POP", unit="PC", age="Y18-24")
    spend, meta_s = eurostat("gov_10a_exp", "2010", geo=EU_GEO, cofog99="GF09", na_item="TE", sector="S13", unit="PC_GDP")
    return {"source": src_oecd(flow, "part des 25-34 ans diplômés du supérieur", "share of 25-34 year-olds with a tertiary degree"),
            "source_early": src_estat(meta_e, "jeunes de 18 à 24 ans sortis tôt de l’école ou de la formation",
                                      "early leavers from education and training, aged 18-24"),
            "source_spend": src_estat(meta_s, "dépenses publiques d’éducation, en % du PIB", "government spending on education, % of GDP"),
            "tertiary": oecd_series(rows, d=1), "early": by(early, d=1), "spend": by(spend, d=1)}


def b_earnings_eu():
    med, meta = eurostat("earn_ses22_adeci", None, geo=EU_GEO, worktime="FT", quant_inc="MED", unit=["EUR", "NAC"])
    # Medians by sector are hourly (the survey publishes no annual ones), for the latest
    # survey; values Eurostat flags as unreliable or confidential are left out.
    sec, meta2 = eurostat("earn_ses_pub2n", None, geo=EU_GEO, sizeclas="GE10", unit="EUR", nace_r2=list(SECTORS), lastTimePeriod=1)
    median = {GEO.get(r["geo"], r["geo"]): num(r["value"], 0) for r in med if r["unit"] == "EUR"}
    sectors = {}
    for r in sec:
        if not set(r["flag"]) & {"u", "c"}:
            sectors.setdefault(r["nace_r2"], {})[GEO.get(r["geo"], r["geo"])] = [r["time"], num(r["value"], 2)]
    return {"source": src_estat(meta, "enquête sur la structure des salaires 2022, salaire annuel brut médian des salariés à temps plein (hors administration publique)",
                                "2022 Structure of Earnings Survey, median gross annual earnings of full-time employees (excluding public administration)"),
            "source_sectors": src_estat(meta2, "enquête sur la structure des salaires, salaire horaire brut médian par secteur d’activité (salariés hors apprentis, entreprises de 10 salariés ou plus)",
                                        "Structure of Earnings Survey, median gross hourly earnings by economic activity (employees except apprentices, firms with 10 or more employees)"),
            "year": 2022, "median": median, "sectors": sectors}


def b_earnings_us():
    this = datetime.now().year
    body = json.dumps({"seriesid": ["LEU0252881500"], "startyear": "2022", "endyear": str(this)}).encode()
    j = json.loads(get(BLS, data=body, headers={"Content-Type": "application/json"}))
    if j.get("status") != "REQUEST_SUCCEEDED":
        raise ValueError(f"BLS: {j.get('status')} {j.get('message')}")
    pts = []
    for d in j["Results"]["series"][0]["data"]:
        if d["period"].startswith("Q") and d["value"] not in ("-", ""):
            pts.append([f"{d['year']}-{d['period']}", float(d["value"])])
    pts.sort()
    if not any(p[0].startswith("2022") for p in pts):
        raise ValueError("BLS: no 2022 quarters")
    return {"source": {"fr": "Bureau of Labor Statistics (États-Unis), salaire hebdomadaire médian des salariés à temps plein (Current Population Survey)",
                       "en": "U.S. Bureau of Labor Statistics, median usual weekly earnings of full-time wage and salary workers (Current Population Survey)",
                       "dataset": "LEU0252881500", "url": "https://data.bls.gov/timeseries/LEU0252881500"},
            "weekly": pts}


def b_rates():
    flow = "OECD.SDD.NAD,DSD_NAMAIN10@DF_TABLE4,2.0"
    rows = oecd(flow, f"A.{OECD_AREAS}.S1.S1.EXC_A+PPP_P31S14+PPP_B1GQ.F21._Z._Z.XDC_USD._Z.N.T001", "2015")
    out = {}
    for r in rows:
        out.setdefault(r["TRANSACTION"], {}).setdefault(FROM_ISO3[r["REF_AREA"]], {})[r["TIME_PERIOD"]] = float(r["OBS_VALUE"])
    return {"source": src_oecd(flow, "taux de change annuels moyens et parités de pouvoir d’achat",
                               "annual average exchange rates and purchasing power parities"),
            "exchange": out["EXC_A"], "ppp": out["PPP_P31S14"], "ppp_gdp": out["PPP_B1GQ"]}


BLOCKS = {
    "hicp": b_hicp, "cpi_ukus": b_cpi_ukus, "unemp": b_unemp, "unemp_ukus": b_unemp_ukus, "gdp_q": b_gdp_q,
    "gdp_a": b_gdp_a, "debt": b_debt, "gdp_pc": b_gdp_pc, "min_wage": b_min_wage, "population": b_population,
    "migrant_share": b_migrant_share, "migration": b_migration, "permits_fr": b_permits_fr, "crime_fr": b_crime_fr,
    "homicide": b_homicide, "inequality": b_inequality, "education": b_education, "earnings_eu": b_earnings_eu,
    "earnings_us": b_earnings_us, "rates": b_rates,
}


# ---------------------------------------------------------------- conversions

def converter(rates):
    """f(country, year) -> factors turning that country's currency into euros: "xr" at
    the year's average exchange rate, "ppp" at French prices (household consumption
    PPPs, or GDP PPPs with gdp=True). The nearest year's rates stand in for a year
    the OECD hasn't published."""
    def at(table, c, y):
        years = table.get(c) or {}
        if not years:
            return None, None
        ys = str(y) if str(y) in years else min(years, key=lambda k: abs(int(k) - y))
        return years[ys], ys

    def f(c, y, gdp=False):
        ex_c, ey = at(rates["exchange"], c, y)
        ex_f, _ = at(rates["exchange"], "FR", int(ey or y))
        table = rates["ppp_gdp"] if gdp else rates["ppp"]
        p_c, py = at(table, c, y)
        p_f, _ = at(table, "FR", int(py or y))
        if None in (ex_c, ex_f, p_c, p_f):
            return None
        return {"xr": ex_f / ex_c, "ppp": p_f / p_c, "rateYear": ey, "pppYear": py}
    return f


def value(c, year, amount, cur, conv, d=0, **extra):
    v = {"amount": amount, "cur": cur, "year": str(year)[:4]} | extra
    k = conv(c, int(str(year)[:4]))
    if k:
        v |= {"xr": round(amount * k["xr"], d or None), "ppp": round(amount * k["ppp"], d or None),
              "rateYear": k["rateYear"], "pppYear": k["pppYear"]}
    return v


def salaries(blocks):
    """Median pay, living standards and pay by job in every country, with conversions."""
    conv = converter(blocks["rates"])
    eu, us, inc = blocks["earnings_eu"], blocks["earnings_us"], blocks["inequality"]
    # Median full-time pay, 2022: the EU survey's annual figure; the UK's and the US's
    # weekly medians times 52 (the US one averaged over 2022's four quarters).
    wage = {c: value(c, 2022, eu["median"][c], "EUR", conv) for c in ("FR", "DE", "BE", "IT", "ES", "NL") if c in eu["median"]}
    wage["UK"] = value("UK", 2022, round(S.ONS_ASHE[2022]["weekly"] * 52), "GBP", conv, weekly=S.ONS_ASHE[2022]["weekly"])
    q22 = [v for p, v in us["weekly"] if p.startswith("2022")]
    wk = sum(q22) / len(q22)
    wage["US"] = value("US", 2022, round(wk * 52), "USD", conv, weekly=round(wk, 2), quarters=len(q22))
    income = {}
    for c, s in inc["median"].items():
        if c in ISO3:
            y, v = s[-1]
            income[c] = value(c, y, v, CURRENCY.get(c, "EUR"), conv)
    gdp = {}
    for c in ISO3:
        ppp = (blocks["gdp_pc"]["ppp"].get(c) or [None])[-1]
        usd = (blocks["gdp_pc"]["usd"].get(c) or [None])[-1]
        if not ppp or not usd:
            continue
        # International dollars buy what a US dollar buys in the US, so France's GDP PPP
        # turns them into euros at French prices; US dollars go at the exchange rate.
        k_ppp = conv("US", int(ppp[0]), gdp=True)
        k_xr = conv("US", int(usd[0]))
        gdp[c] = {"year": ppp[0], "intl": ppp[1], "usd": usd[1], "xrYear": usd[0],
                  "ppp": round(ppp[1] * k_ppp["ppp"]) if k_ppp else None,
                  "xr": round(usd[1] * k_xr["xr"]) if k_xr else None}
    jobs = []

    def job(jid, fr, en, stat, src, rows, note_fr="", note_en="", per="year"):
        vals = {c: value(c, y, amount, CURRENCY.get(c, "EUR"), conv, d=2 if per == "hour" else 0) for c, (y, amount) in rows.items()}
        if vals:
            jobs.append({"id": jid, "fr": fr, "en": en, "stat": stat, "per": per, "source": src, "noteFr": note_fr, "noteEn": note_en, "values": vals})

    # Median hourly pay by sector, in the EU countries (the EU average has no conversion
    # at French prices), then the minimum wage.
    for code, (fr, en) in SECTORS.items():
        rows = {c: v for c, v in eu.get("sectors", {}).get(code, {}).items() if c in ISO3}
        y = max((v[0] for v in rows.values()), default="")
        extra = SECTOR_NOTES.get(code, ("", ""))
        job("sector-all" if code == "B-S_X_O" else f"sector-{code}", fr, en, "median", "earnings_eu_sectors", rows,
            f"Salaire horaire brut médian en {y} : la moitié des salariés du secteur gagnent moins, l’autre moitié plus. Un secteur compte "
            f"tous ses salariés, quel que soit leur métier : apprentis exceptés, temps partiel compris, dans les entreprises de 10 salariés ou plus. {extra[0]}".strip(),
            f"Median gross hourly pay in {y}: half the sector’s employees earn less, half earn more. A sector counts all its employees, "
            f"whatever their job: apprentices excepted, part-timers included, in firms with 10 or more employees. {extra[1]}".strip(), per="hour")
    mw = blocks["min_wage"]["annual"]
    job("minimum", "Salaire minimum (temps plein)", "Minimum wage (full time)", "legal", "min_wage",
        {c: s[-1] for c, s in mw.items() if c in ISO3},
        "Montant annuel brut pour un temps plein. Italie : pas de salaire minimum légal. États-Unis : minimum fédéral, plus élevé dans de nombreux États.",
        "Gross annual amount for full-time work. Italy: no statutory minimum wage. United States: the federal minimum; many states set a higher one.")
    return {"wage": wage, "income": income, "gdp": gdp, "jobs": jobs}


# ---------------------------------------------------------------- main

def main():
    try:
        last = json.loads(OUT.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        last = {}
    old = last.get("blocks") or {}
    blocks, stale = {}, []
    for name, fn in BLOCKS.items():
        t0 = time.time()
        try:
            blocks[name] = fn() | {"fetched": datetime.now(timezone.utc).isoformat(timespec="minutes")}
            print(f"  {name:<14} ok ({time.time() - t0:.0f}s)")
        except Exception as e:  # noqa: BLE001 - the last good values stand in
            print(f"  {name:<14} FAILED: {type(e).__name__}: {str(e)[:160]}")
            if name in old:
                blocks[name] = old[name]
                stale.append(name)
    needed = {"rates", "earnings_eu", "earnings_us", "inequality", "gdp_pc", "min_wage"}
    if len(blocks) < len(BLOCKS) // 2 or not needed <= blocks.keys():
        raise SystemExit(f"too many sources failed ({', '.join(sorted(set(BLOCKS) - blocks.keys()))}); keeping the old file")
    data = {
        "updated": datetime.now(timezone.utc).isoformat(timespec="minutes"),
        "stale": stale,
        "blocks": blocks,
        "salaries": salaries(blocks),
        "hand": {"insee": S.INSEE_SALAIRES, "ons": {str(k): v for k, v in S.ONS_ASHE.items()}, "pisa": S.PISA_2025},
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT).as_posix()} ({OUT.stat().st_size // 1024} KB): {len(blocks)} blocks"
          + (f", stale: {', '.join(stale)}" if stale else ""))


if __name__ == "__main__":
    main()
