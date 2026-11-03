"""Write data/fr/calendrier.json: the elections ahead in France, who votes in each,
and the source of every date. Hand-checked (Oct. 28, 2026) against French Wikipedia;
the presidential dates come from data/fr/presidentielle-2027.json, which the daily
refresh rebuilds, so they follow any change there.

Dates that aren't fixed yet carry only a month ("2028-03") and are shown without a
day count; "latest" marks a date that is a deadline (the legislative elections can
come sooner if the Assembly is dissolved).

    py scripts/fr/calendrier.py
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "fr" / "calendrier.json"
CHECKED = "2026-10-28"
WP = "https://fr.wikipedia.org/wiki/"


def src(title):
    return {"title": f"Wikipédia : {title}", "url": WP + title.replace(" ", "_"), "checked": CHECKED}


def main():
    pres = json.loads((ROOT / "data" / "fr" / "presidentielle-2027.json").read_text(encoding="utf-8"))
    elections = [
        {
            "id": "presidentielle-2027", "type": "presidentielle", "date": pres["rounds"]["r1"], "round2": pres["rounds"]["r2"],
            "status": "fixed", "scope": "national",
            "name": {"fr": "Élection présidentielle", "en": "Presidential election"},
            "what": {"fr": "Élection du président de la République pour cinq ans, au suffrage universel direct, en deux tours.",
                     "en": "Elects the President of the Republic for five years by direct universal suffrage, in two rounds."},
            "href": "#/fr/presidentielle",
            "source": pres["meta"]["sources"][0] | {"checked": CHECKED},
        },
        {
            "id": "regionales-2028", "type": "regionales", "month": "2028-03", "status": "expected", "scope": "region",
            "excludeRegs": ["06"],
            "special": {"94": {"fr": "En Corse, l’Assemblée de Corse est élue le même jour.", "en": "In Corsica, the Corsican Assembly is elected the same day."},
                        "02": {"fr": "En Martinique, l’Assemblée de Martinique est élue le même jour.", "en": "In Martinique, the Assembly of Martinique is elected the same day."},
                        "03": {"fr": "En Guyane, l’Assemblée de Guyane est élue le même jour.", "en": "In French Guiana, the Assembly of French Guiana is elected the same day."}},
            "name": {"fr": "Élections régionales", "en": "Regional elections"},
            "what": {"fr": "Renouvellement des conseils régionaux (et des assemblées de Corse, de Martinique et de Guyane), prévu en mars 2028 en même temps que les départementales. Le jour exact n’est pas encore fixé.",
                     "en": "Elects the regional councils (and the assemblies of Corsica, Martinique and French Guiana), planned for March 2028 alongside the departmental elections. The exact day isn’t set yet."},
            "source": src("Élections régionales françaises de 2028"),
        },
        {
            "id": "departementales-2028", "type": "departementales", "month": "2028-03", "status": "expected", "scope": "departement",
            "excludeDeps": ["75", "2A", "2B", "972", "973", "976"],
            "special": {"69": {"fr": "Dans les communes de la Métropole de Lyon, il n’y a pas d’élection départementale : le conseil de la Métropole est élu avec les municipales.",
                               "en": "In the communes of the Lyon Metropolis there is no departmental election: the Metropolis council is elected with the municipal elections."}},
            "name": {"fr": "Élections départementales", "en": "Departmental elections"},
            "what": {"fr": "Renouvellement des 95 conseils départementaux, prévu en mars 2028 en même temps que les régionales. Paris, la Corse, la Martinique, la Guyane et Mayotte n’ont pas de conseil départemental. Le jour exact n’est pas encore fixé.",
                     "en": "Elects the 95 departmental councils, planned for March 2028 alongside the regional elections. Paris, Corsica, Martinique, French Guiana and Mayotte have no departmental council. The exact day isn’t set yet."},
            "source": src("Élections départementales françaises de 2028"),
        },
        {
            "id": "legislatives", "type": "legislatives", "date": "2029-06-17", "round2": "2029-06-24", "status": "latest", "scope": "national",
            "name": {"fr": "Élections législatives", "en": "Legislative elections"},
            "what": {"fr": "Élection des 577 députés de l’Assemblée nationale, au plus tard les 17 et 24 juin 2029 ; plus tôt en cas de dissolution.",
                     "en": "Elects the 577 members of the National Assembly, by June 17 and 24, 2029 at the latest; sooner if the Assembly is dissolved."},
            "source": src("Prochaines élections législatives françaises"),
        },
        {
            "id": "europeennes-2029", "type": "europeennes", "month": "2029-06", "status": "expected", "scope": "national",
            "name": {"fr": "Élections européennes", "en": "European elections"},
            "what": {"fr": "Élection des députés français au Parlement européen. Ces élections ont lieu début juin, tous les cinq ans ; les prochaines auront lieu en 2029.",
                     "en": "Elects France’s members of the European Parliament. They are held in early June every five years; the next are in 2029."},
            "source": src("Élections du Parlement européen"),
        },
        {
            "id": "municipales-2032", "type": "municipales", "month": "2032-03", "status": "expected", "scope": "commune",
            "name": {"fr": "Élections municipales", "en": "Municipal elections"},
            "what": {"fr": "Élection des conseils municipaux, qui élisent le maire. Les dernières ont eu lieu les 15 et 22 mars 2026 ; le mandat dure six ans.",
                     "en": "Elects the municipal councils, which then elect the mayor. The last were held on March 15 and 22, 2026; the term is six years."},
            "source": src("Élections municipales en France"),
        },
    ]
    OUT.write_text(json.dumps({"updated": datetime.now(timezone.utc).isoformat(timespec="minutes"), "elections": elections},
                              ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT).as_posix()}: {len(elections)} elections")


if __name__ == "__main__":
    main()
