"""Build the site's map files from U.S. Census Bureau boundary shapefiles.

Inputs (download into one folder, pass it as the first argument):
  GENZ2025  cb_2025_us_state_20m.zip    national map (already generalized)
  GENZ2025  cb_2025_us_state_500k.zip   shoreline outline used to clip districts
  TIGER2026 tl_2026_SS_cd120.zip        120th Congress districts (2026 election maps)
  TIGER2026 tl_2026_SS_sldu.zip         2026 state senate (upper) districts
  TIGER2026 tl_2026_SS_sldl.zip         2026 state house (lower) districts

TIGER/Line districts run out into lakes and coastal water, so each one is clipped
to the cartographic (shoreline) outline of its state. Simplification runs on each
state's districts as one coverage, so neighbouring districts keep a shared border
instead of opening slivers between them.

Rings are written clockwise, which is what d3-geo expects. The GeoJSON spec says
counter-clockwise; d3 reads that as "the whole globe except this shape".

Usage:
  python -I scripts/build_maps.py <census-download-dir> <site>/data/maps
Requires: shapely >= 2.1 (coverage_simplify), pyshp
"""

import json
import os
import sys

import shapefile
import shapely
from shapely.geometry import MultiPolygon, Polygon, mapping, shape
from shapely.geometry.polygon import orient

STATES = {
    "01": "AL", "02": "AK", "04": "AZ", "05": "AR", "06": "CA", "08": "CO", "09": "CT",
    "10": "DE", "11": "DC", "12": "FL", "13": "GA", "15": "HI", "16": "ID", "17": "IL",
    "18": "IN", "19": "IA", "20": "KS", "21": "KY", "22": "LA", "23": "ME", "24": "MD",
    "25": "MA", "26": "MI", "27": "MN", "28": "MS", "29": "MO", "30": "MT", "31": "NE",
    "32": "NV", "33": "NH", "34": "NJ", "35": "NM", "36": "NY", "37": "NC", "38": "ND",
    "39": "OH", "40": "OK", "41": "OR", "42": "PA", "44": "RI", "45": "SC", "46": "SD",
    "47": "TN", "48": "TX", "49": "UT", "50": "VT", "51": "VA", "53": "WA", "54": "WV",
    "55": "WI", "56": "WY",
}

# layer -> (file suffix, district-code field)
LAYERS = {
    "cd": ("cd120", "CD120FP"),
    "sldu": ("sldu", "SLDUST"),
    "sldl": ("sldl", "SLDLST"),
}

# Detail relative to the state's size; ~1/2000 of its extent keeps borders crisp
# when the district map is zoomed a few times.
DETAIL = 2000
DECIMALS = 4


def read_shapes(path):
    with shapefile.Reader(path) as r:
        fields = [f[0] for f in r.fields[1:]]
        for sr in r.iterShapeRecords():
            props = dict(zip(fields, sr.record))
            geom = shape(sr.shape.__geo_interface__)
            if not geom.is_valid:
                geom = shapely.make_valid(geom)
            yield props, geom


def polygons_only(geom):
    if geom.is_empty:
        return None
    if isinstance(geom, (Polygon, MultiPolygon)):
        return geom
    parts = [g for g in getattr(geom, "geoms", []) if isinstance(g, (Polygon, MultiPolygon))]
    if not parts:
        return None
    flat = []
    for p in parts:
        flat.extend(p.geoms if isinstance(p, MultiPolygon) else [p])
    return MultiPolygon(flat)


def drop_specks(geom, min_share=0.0005):
    """Remove clipping debris: polygon parts under min_share of the district's area."""
    if isinstance(geom, Polygon):
        return geom
    total = geom.area
    keep = [p for p in geom.geoms if p.area >= total * min_share]
    if not keep:
        return None
    return keep[0] if len(keep) == 1 else MultiPolygon(keep)


def round_ring(coords, nd):
    out = []
    for x, y in coords:
        pt = [round(x, nd), round(y, nd)]
        if not out or out[-1] != pt:
            out.append(pt)
    if len(out) >= 2 and out[0] != out[-1]:
        out.append(out[0])
    return out if len(out) >= 4 else None


def to_d3_geometry(geom, nd):
    polys = list(geom.geoms) if isinstance(geom, MultiPolygon) else [geom]
    out = []
    for p in polys:
        p = orient(p, sign=-1.0)  # clockwise exterior for d3
        shell = round_ring(p.exterior.coords, nd)
        if not shell:
            continue
        rings = [shell]
        for hole in p.interiors:
            r = round_ring(hole.coords, nd)
            if r:
                rings.append(r)
        out.append(rings)
    if not out:
        return None
    if len(out) == 1:
        return {"type": "Polygon", "coordinates": out[0]}
    return {"type": "MultiPolygon", "coordinates": out}


def extent_of(geom, abbr):
    minx, miny, maxx, maxy = geom.bounds
    if abbr == "AK":  # crosses the antimeridian; bounds span the whole globe, and
        return 60.0   # thousands of islands need a coarser hand than other states
    return max(maxx - minx, maxy - miny)


def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, separators=(",", ":"))
    return os.path.getsize(path)


def build_national(src, out_dir):
    feats = []
    geoms, props = [], []
    for p, g in read_shapes(os.path.join(src, "cb_2025_us_state_20m.zip")):
        if p["STATEFP"] not in STATES:
            continue
        geoms.append(g)
        props.append(p)
    simplified = shapely.coverage_simplify(geoms, 0.01)
    for p, g in zip(props, simplified):
        gj = to_d3_geometry(g, 3)
        feats.append({
            "type": "Feature",
            "id": STATES[p["STATEFP"]],
            "properties": {"name": p["NAME"], "fips": p["STATEFP"]},
            "geometry": gj,
        })
    size = write_json(os.path.join(out_dir, "states.json"), {"type": "FeatureCollection", "features": feats})
    print(f"states.json: {len(feats)} states, {size/1024:.0f} KB")


def build_state_layers(src, out_dir):
    outlines = {}
    for p, g in read_shapes(os.path.join(src, "cb_2025_us_state_500k.zip")):
        if p["STATEFP"] in STATES:
            outlines[p["STATEFP"]] = g

    index = {}
    totals = {k: 0 for k in LAYERS}
    for fips, abbr in STATES.items():
        index[abbr] = {}
        tol = extent_of(outlines[fips], abbr) / DETAIL
        # The 1:500k coastline is far more detailed than the districts need; left
        # alone it dominates file size along every coast.
        outline = outlines[fips].simplify(tol, preserve_topology=True)
        for layer, (suffix, code_field) in LAYERS.items():
            path = os.path.join(src, f"tl_2026_{fips}_{suffix}.zip")
            if not os.path.exists(path):
                continue
            props, geoms = [], []
            for p, g in read_shapes(path):
                code = str(p.get(code_field, "")).strip()
                if not code or set(code) == {"Z"}:  # ZZ/ZZZ = water or unassigned
                    continue
                props.append(p)
                geoms.append(g)
            if not geoms:
                continue
            try:
                simplified = shapely.coverage_simplify(geoms, tol)
            except Exception as e:  # not a clean coverage; fall back per shape
                print(f"  {abbr} {layer}: coverage_simplify failed ({e}); simplifying per shape")
                simplified = [g.simplify(tol, preserve_topology=True) for g in geoms]
            feats = []
            for p, g in zip(props, simplified):
                clipped = polygons_only(g.intersection(outline))
                if clipped is None:
                    continue
                clipped = drop_specks(clipped)
                if clipped is None:
                    continue
                gj = to_d3_geometry(clipped, DECIMALS)
                if gj is None:
                    continue
                lp = clipped.representative_point() if isinstance(clipped, Polygon) else max(clipped.geoms, key=lambda q: q.area).representative_point()
                code = str(p[code_field]).strip()
                feats.append({
                    "type": "Feature",
                    "id": code,
                    "properties": {
                        "n": p.get("NAMELSAD", code),
                        "lp": [round(lp.x, 3), round(lp.y, 3)],
                    },
                    "geometry": gj,
                })
            feats.sort(key=lambda f: (len(f["id"]), f["id"]))
            size = write_json(os.path.join(out_dir, layer, f"{abbr}.json"), {"type": "FeatureCollection", "features": feats})
            index[abbr][layer] = len(feats)
            totals[layer] += len(feats)
            print(f"{abbr} {layer}: {len(feats)} districts, {size/1024:.0f} KB")
    write_json(os.path.join(out_dir, "index.json"), index)
    print("totals:", totals)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    src, out = sys.argv[1], sys.argv[2]
    build_national(src, out)
    build_state_layers(src, out)
