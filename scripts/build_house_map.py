"""Build data/maps/cd-us.json: every congressional district in one file, for the House
view of the home page's map, from the per-state district maps build_maps.py wrote
(data/maps/cd/ST.json, Census TIGER 2026 clipped to the shoreline).

Each state's districts are simplified again as one coverage, coarser than the state
maps (the national map draws a district a few pixels wide), so neighbouring districts
keep a shared border. Ids are the race ids' stems ("CA-13", "AK-00", "DC-98"), and rings
stay clockwise, as d3-geo expects (it reads a counter-clockwise ring as "the whole globe
except this shape").

    python scripts/build_house_map.py
Requires: shapely >= 2.1 (coverage_simplify)
"""

import json
import sys
from pathlib import Path

import shapely
from shapely.geometry import MultiPolygon, Polygon, shape
from shapely.geometry.polygon import orient

ROOT = Path(__file__).resolve().parents[1]
MAPS = ROOT / "data" / "maps"
TOLERANCE = 0.012  # degrees, about a kilometre: under a pixel on the national map
DECIMALS = 3
MIN_SHARE = 0.002  # islands smaller than this share of their district are dropped


def round_ring(coords):
    out = []
    for x, y in coords:
        pt = [round(x, DECIMALS), round(y, DECIMALS)]
        if not out or out[-1] != pt:
            out.append(pt)
    if len(out) >= 2 and out[0] != out[-1]:
        out.append(out[0])
    return out if len(out) >= 4 else None


def polygons(geom):
    if isinstance(geom, Polygon):
        return [geom]
    if isinstance(geom, MultiPolygon):
        return list(geom.geoms)
    return [g for g in getattr(geom, "geoms", []) if isinstance(g, Polygon)]


def to_d3(geom):
    polys = [p for p in polygons(geom) if not p.is_empty]
    if not polys:
        return None
    total = sum(p.area for p in polys)
    out = []
    for p in polys:
        if p.area < total * MIN_SHARE:
            continue
        p = orient(p, sign=-1.0)  # clockwise exterior for d3
        shell = round_ring(p.exterior.coords)
        if not shell:
            continue
        rings = [shell] + [r for r in (round_ring(h.coords) for h in p.interiors) if r]
        out.append(rings)
    if not out:
        return None
    return {"type": "Polygon", "coordinates": out[0]} if len(out) == 1 else {"type": "MultiPolygon", "coordinates": out}


def main():
    feats = []
    for path in sorted((MAPS / "cd").glob("*.json")):
        st = path.stem
        src = json.loads(path.read_text(encoding="utf-8"))["features"]
        geoms = []
        for f in src:
            g = shape(f["geometry"])
            geoms.append(g if g.is_valid else g.buffer(0))
        try:
            simplified = shapely.coverage_simplify(geoms, TOLERANCE)
        except Exception as e:  # noqa: BLE001  fall back to shape by shape
            print(f"  {st}: coverage_simplify failed ({e}); simplifying each district")
            simplified = [g.simplify(TOLERANCE, preserve_topology=True) for g in geoms]
        for f, g in zip(src, simplified):
            gj = to_d3(g)
            if gj is None:
                print(f"  {st}-{f['id']}: nothing left after simplifying; kept as in the state map")
                gj = f["geometry"]
            feats.append({"type": "Feature", "id": f"{st}-{f['id']}",
                          "properties": {"st": st, "n": f["properties"].get("n"), "lp": f["properties"].get("lp")},
                          "geometry": gj})
    out = MAPS / "cd-us.json"
    out.write_text(json.dumps({"type": "FeatureCollection", "features": feats}, separators=(",", ":")), encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)}: {len(feats)} districts, {out.stat().st_size / 1024:.0f} KB")
    return 0 if len(feats) == 436 else 1


if __name__ == "__main__":
    sys.exit(main())
