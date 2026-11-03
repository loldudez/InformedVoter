"""Build the France section's maps: data/fr/maps/departements.json, regions.json
and villes.json.

Boundaries: IGN's ADMIN EXPRESS COG CARTO (the map-scale edition), read from the
Géoplateforme WFS (data.geopf.fr) under the Licence Ouverte 2.0. Departments are
simplified together as one coverage, so neighbours keep identical borders, and each
region is the union of its simplified departments, so the two layers line up.

The five overseas departments (Guadeloupe, Martinique, Guyane, La Réunion, Mayotte)
are moved into inset boxes beside the mainland, as French maps usually show them;
each inset has its own scale, noted in `insets`.

Cities: every commune's population and centre from geo.api.gouv.fr (INSEE figures),
keeping the largest communes of each region.

Rings are wound clockwise, as d3 expects. Only needs rerunning when boundaries change.

    py scripts/fr/build_maps_fr.py
"""

import json
import sys
import urllib.request
from pathlib import Path

import shapely
from shapely.affinity import scale, translate
from shapely.geometry import MultiPolygon, Polygon, mapping, shape
from shapely.geometry.polygon import orient

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "fr" / "maps"
UA = "InformedVoter/1.0 (personal election-information site; map build script)"
WFS = ("https://data.geopf.fr/wfs/ows?SERVICE=WFS&VERSION=2.0.0&REQUEST=GetFeature&TYPENAMES={}"
       "&OUTPUTFORMAT=application/json&SRSNAME=EPSG:4326&COUNT=1000")
COMMUNES = "https://geo.api.gouv.fr/communes?fields=nom,code,population,centre,codeDepartement,codeRegion&format=json&geometry=centre"
TOLERANCE = 0.012          # degrees, about a kilometre
DIGITS = 3                 # about 100 m
CITIES_PER_REGION = {"metro": 5, "drom": 2}

# Overseas departments -> centre of their inset box (lon, lat) beside the Bay of Biscay,
# and the box size in degrees. Each is scaled to fit its box, so sizes aren't comparable.
INSETS = {"971": (-6.2, 46.3), "972": (-6.2, 45.0), "973": (-6.2, 43.7), "974": (-6.2, 42.4), "976": (-6.2, 41.1)}
BOX = (1.5, 1.05)


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=120) as r:
        return json.loads(r.read())


def fit_inset(geom, code):
    """Scale and move an overseas department into its box; returns (geom, transform)."""
    minx, miny, maxx, maxy = geom.bounds
    k = min(BOX[0] / (maxx - minx), BOX[1] / (maxy - miny))
    cx, cy = (minx + maxx) / 2, (miny + maxy) / 2
    tx, ty = INSETS[code]
    g = translate(scale(geom, k, k, origin=(cx, cy)), tx - cx, ty - cy)
    return g, {"k": k, "cx": cx, "cy": cy, "tx": tx, "ty": ty}


def move_point(lon, lat, t):
    return t["tx"] + (lon - t["cx"]) * t["k"], t["ty"] + (lat - t["cy"]) * t["k"]


def clockwise(geom):
    polys = list(geom.geoms) if isinstance(geom, MultiPolygon) else [geom]
    out = [orient(p, sign=-1.0) for p in polys if not p.is_empty and p.area > 1e-7]
    return out[0] if len(out) == 1 else MultiPolygon(out)


def rounded(geom):
    def ring(coords):
        pts = [(round(x, DIGITS), round(y, DIGITS)) for x, y in coords]
        return [p for i, p in enumerate(pts) if i == 0 or p != pts[i - 1]]
    polys = list(geom.geoms) if isinstance(geom, MultiPolygon) else [geom]
    out = []
    for p in polys:
        ext = ring(p.exterior.coords)
        if len(ext) >= 4:
            out.append([ext] + [r for r in (ring(i.coords) for i in p.interiors) if len(r) >= 4])
    return {"type": "MultiPolygon", "coordinates": out} if len(out) > 1 else {"type": "Polygon", "coordinates": out[0]}


def label_point(geom):
    biggest = max(geom.geoms, key=lambda p: p.area) if isinstance(geom, MultiPolygon) else geom
    p = biggest.representative_point()
    return [round(p.x, DIGITS), round(p.y, DIGITS)]


def main():
    regs = get(WFS.format("ADMINEXPRESS-COG-CARTO.LATEST:region"))["features"]
    deps = get(WFS.format("ADMINEXPRESS-COG-CARTO.LATEST:departement"))["features"]
    reg_name = {f["properties"]["code_insee"]: f["properties"]["nom_officiel"] for f in regs}
    print(f"{len(regs)} regions, {len(deps)} departments from IGN")

    codes, geoms, meta, moves = [], [], {}, {}
    for f in sorted(deps, key=lambda f: f["properties"]["code_insee"]):
        p = f["properties"]
        code = p["code_insee"]
        g = shape(f["geometry"]).buffer(0)
        if code in INSETS:
            g, moves[code] = fit_inset(g, code)
        codes.append(code)
        geoms.append(g)
        meta[code] = {"name": p["nom_officiel"], "reg": p["code_insee_de_la_region"]}

    simple = list(shapely.coverage_simplify(geoms, TOLERANCE))
    dep_geom = {c: clockwise(g.buffer(0)) for c, g in zip(codes, simple)}

    dep_features = [{"type": "Feature", "id": c, "properties": {**meta[c], "lp": label_point(dep_geom[c])},
                     "geometry": rounded(dep_geom[c])} for c in codes]
    by_reg = {}
    for c in codes:
        by_reg.setdefault(meta[c]["reg"], []).append(dep_geom[c])
    reg_features = []
    for rc, gs in sorted(by_reg.items()):
        g = clockwise(shapely.union_all(gs).buffer(0))
        reg_features.append({"type": "Feature", "id": rc,
                             "properties": {"name": reg_name.get(rc, rc), "deps": sorted(c for c in codes if meta[c]["reg"] == rc),
                                            "lp": label_point(g), "overseas": rc in {"01", "02", "03", "04", "06"}},
                             "geometry": rounded(g)})

    # Inset frames, drawn around each overseas department.
    frames = [{"code": c, "box": [round(x, DIGITS) for x in (t["tx"] - BOX[0] / 2 - 0.12, t["ty"] - BOX[1] / 2 - 0.1,
                                                              t["tx"] + BOX[0] / 2 + 0.12, t["ty"] + BOX[1] / 2 + 0.1)]}
              for c, t in moves.items()]

    communes = get(COMMUNES)
    cities = []
    for rc in by_reg:
        overseas = rc in {"01", "02", "03", "04", "06"}
        pool = [c for c in communes if c.get("codeRegion") == rc and c.get("population") and c.get("centre")]
        pool.sort(key=lambda c: -c["population"])
        for c in pool[:CITIES_PER_REGION["drom" if overseas else "metro"]]:
            lon, lat = c["centre"]["coordinates"]
            dep = c["codeDepartement"]
            if dep in moves:
                lon, lat = move_point(lon, lat, moves[dep])
            cities.append({"code": c["code"], "name": c["nom"], "dep": dep, "reg": rc, "pop": c["population"],
                           "at": [round(lon, DIGITS), round(lat, DIGITS)]})

    OUT.mkdir(parents=True, exist_ok=True)
    src = {"boundaries": "IGN, ADMIN EXPRESS COG CARTO (Géoplateforme WFS), Licence Ouverte 2.0",
           "cities": "geo.api.gouv.fr (INSEE populations), Licence Ouverte 2.0"}
    (OUT / "departements.json").write_text(json.dumps({"type": "FeatureCollection", "source": src["boundaries"], "insets": frames,
                                                       "features": dep_features}, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    (OUT / "regions.json").write_text(json.dumps({"type": "FeatureCollection", "source": src["boundaries"], "insets": frames,
                                                  "features": reg_features}, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    (OUT / "villes.json").write_text(json.dumps({"source": src["cities"], "cities": cities}, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    sizes = ", ".join(f"{p.name} {p.stat().st_size // 1024} KB" for p in sorted(OUT.glob("*.json")))
    print(f"wrote {len(dep_features)} departments, {len(reg_features)} regions, {len(cities)} cities: {sizes}")


if __name__ == "__main__":
    main()
