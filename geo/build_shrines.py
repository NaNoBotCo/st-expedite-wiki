#!/usr/bin/env python3
"""Build geo/shrines.geojson from Overpass API results for Saint Expedite.

Usage:
    python3 build_shrines.py raw1.json [raw2.json ...]     # from cached Overpass responses
    python3 build_shrines.py --fetch                        # query Overpass live (2 queries, polite)

Stdlib only. Output: shrines.geojson next to this script.

The Overpass queries used (documented in README.md):
  Q1: nwr["name"~"Exp[ee']dit",i]; nwr["dedication"~"Exp[ee']dit",i];
  Q2: nwr["name"~"Espedit",i];     nwr["dedication"~"Espedit",i];   (Italian spelling)

Filtering: an element is kept only if its name/dedication matches a
"Saint + Expedit*" pattern (Santo Expedito / San Expedito / Sao Expedito /
Saint-Expedit / St Expedite / Sant'Espedito ...) AND it is a plausibly
religious feature (place_of_worship, wayside shrine/cross, church/chapel
building, cross, artwork/memorial statue, religious office/landuse) or its
name contains a church-word (chapelle, capela, igreja, oratoire, santuario,
grotte, statue, croix ...). Streets, bus stops, farms, shops, schools,
neighbourhoods and "expedition/expeditie/expeditor" noise are dropped.
"""
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
OVERPASS = "https://overpass-api.de/api/interpreter"

QUERIES = [
    '[out:json][timeout:180];\n(\n  nwr["name"~"Exp[eé]dit",i];\n  nwr["dedication"~"Exp[eé]dit",i];\n);\nout center tags;',
    '[out:json][timeout:180];\n(\n  nwr["name"~"Espedit",i];\n  nwr["dedication"~"Espedit",i];\n);\nout center tags;',
]

# --- filters ------------------------------------------------------------

SAINT_RE = re.compile(
    r"\b(sant'?|santo|san|s[aã]o|saint|st\.?|ste)\b[\s\-'.]*e[sx]?p[eéè]dit", re.I
)
NOISE_RE = re.compile(r"expedition|expeditie|expeditor|exp[eé]ditionn|expeditur", re.I)

CHURCH_WORDS = re.compile(
    r"chapelle|capela|capilla|cappella|kapelle|chiesa|igreja|iglesia|"
    r"[eé]glise|church|basilica|bas[ií]lica|catedral|cathedral|"
    r"oratoire|\borat[oó]rio\b|\boratorio\b|santu[aá]rio|santuario|sanctuaire|shrine|"
    r"par[oó]quia|parroquia|parrocchia|paroisse|parish|"
    r"grotte|gruta|statue|est[aá]tua|croix|cruz|eremo|ermida|ermita|templo|temple",
    re.I,
)

def is_religious(t):
    if t.get("amenity") == "place_of_worship":
        return True
    if t.get("historic") in ("wayside_shrine", "wayside_cross", "chapel", "church",
                             "monastery", "memorial", "monument"):
        return True
    if t.get("building") in ("church", "chapel", "cathedral", "basilica", "shrine",
                             "monastery", "religious", "temple"):
        return True
    if t.get("man_made") == "cross":
        return True
    if t.get("landuse") == "religious":
        return True
    if t.get("tourism") == "artwork":
        return True
    if t.get("office") == "religion":
        return True
    if "religion" in t:
        return True
    return False

NON_FEATURE_KEYS = ("highway", "railway", "public_transport", "waterway", "aeroway")

def keep(t):
    name = (t.get("name") or "")
    ded = (t.get("dedication") or "")
    blob = name + " " + ded
    if NOISE_RE.search(blob) and not SAINT_RE.search(blob):
        return False
    if not SAINT_RE.search(blob):
        return False
    # streets, bus stops etc. named after the saint are not shrines
    if any(k in t for k in NON_FEATURE_KEYS):
        return False
    if is_religious(t):
        return True
    if CHURCH_WORDS.search(name):
        return True
    return False

# --- classification -----------------------------------------------------

def classify(t):
    name = (t.get("name") or "").lower()
    if re.search(r"oratoire|\borat[oó]rio\b|\boratorio\b", name):
        return "oratory"
    if t.get("historic") in ("wayside_shrine", "wayside_cross") or t.get("man_made") == "cross":
        return "wayside-shrine"
    if re.search(r"grotte|gruta|statue|est[aá]tua|\bimagem\b|\baltar\b|monolito|croix|cruz",
                 name) and t.get("building") not in ("church", "chapel"):
        return "wayside-shrine"
    if t.get("building") == "chapel" or re.search(r"chapelle|capela|capilla|cappella|kapelle", name):
        return "chapel"
    if (t.get("building") in ("church", "cathedral", "basilica")
            or re.search(r"chiesa|igreja|iglesia|[eé]glise|church|basilica|catedral|"
                         r"cathedral|santu[aá]rio|santuario|par[oó]quia|parroquia|"
                         r"parrocchia|paroisse", name)):
        return "church"
    if t.get("amenity") == "place_of_worship":
        # unnamed-type PoW: default church
        return "church"
    return "other"

# --- rough country / region from coordinates ----------------------------
# (lat_min, lat_max, lon_min, lon_max) boxes, checked in order. Rough on
# purpose: this is a discovery layer, values are marked OSM-derived.

COUNTRY_BOXES = [
    ("France (Réunion)", -21.6, -20.7, 55.0, 56.0),
    ("Mauritius",            -20.6, -19.9, 57.2, 57.9),
    ("United States",         24.5,  49.5, -125.0, -66.0),
    ("Mexico",                14.5,  32.7, -118.5, -86.5),
    ("Chile",                -56.0, -17.5, -76.0, -69.8),  # core strip incl. Santiago/Valparaíso
    ("Argentina",            -55.0, -21.7, -73.6, -53.6),
    ("Chile",                -26.0, -17.5, -69.8, -68.0),  # far-north fallback
    ("Nicaragua",             10.7,  15.1, -87.7, -82.6),
    ("Portugal (Azores)",     36.8,  39.8, -31.4, -24.9),
    ("Uruguay",              -35.1, -30.0, -58.5, -53.0),
    ("Paraguay",             -27.7, -19.2, -62.7, -54.2),
    ("Bolivia",              -23.0,  -9.6, -69.7, -57.4),
    ("Peru",                 -18.4,  -0.0, -81.4, -68.6),
    ("Colombia",              -4.3,  12.6, -79.1, -66.8),
    ("Venezuela",              0.6,  12.3, -73.4, -59.8),
    ("Ecuador",               -5.1,   1.5, -81.1, -75.2),
    ("Brazil",               -33.8,   5.3, -74.1, -34.7),
    ("Portugal",              36.9,  42.2, -9.6,  -6.1),
    ("Spain",                 35.9,  43.8, -9.4,   3.4),
    ("Italy",                 36.5,  47.1,  6.6,  18.6),
    ("Malta",                 35.7,  36.1, 14.1,  14.6),
    ("Austria",               46.3,  49.1,  9.5,  17.2),
    ("Germany",               47.2,  55.1,  5.8,  15.1),
    ("Belgium",               49.4,  51.6,  2.5,   6.5),
    ("Netherlands",           50.7,  53.6,  3.3,   7.3),
    ("France",                41.2,  51.2, -5.3,   9.7),
    ("United Kingdom",        49.8,  60.9, -8.7,   1.8),
    ("Poland",                49.0,  54.9, 14.1,  24.2),
    ("Philippines",            4.5,  21.3, 116.0, 127.0),
    ("Australia",            -44.0, -10.0, 112.0, 154.0),
    ("India",                  6.5,  35.6,  68.0,  97.5),
    ("Madagascar",           -25.7, -11.9,  43.2,  50.6),
]

def country_of(lat, lon):
    for name, la0, la1, lo0, lo1 in COUNTRY_BOXES:
        if la0 <= lat <= la1 and lo0 <= lon <= lo1:
            return name
    return "unknown"

def region_bucket(lat, lon, country):
    if country == "France (Réunion)":
        return "reunion"
    if country == "Brazil":
        return "brazil"
    if country == "Argentina":
        return "argentina"
    if country == "Italy":
        return "italy"
    if country == "France":
        return "france"
    if country == "Philippines":
        return "philippines"
    if 29.5 <= lat <= 30.3 and -90.6 <= lon <= -89.5:
        return "new-orleans"
    return "other"

# --- main ----------------------------------------------------------------

def fetch():
    raws = []
    for i, q in enumerate(QUERIES):
        data = urllib.parse.urlencode({"data": q}).encode()
        req = urllib.request.Request(OVERPASS, data=data,
                                     headers={"User-Agent": "st-expedite-wiki-geo/1.0"})
        for attempt in range(4):
            try:
                with urllib.request.urlopen(req, timeout=240) as r:
                    raws.append(json.load(r))
                break
            except Exception as e:  # 429/504 etc.
                wait = 30 * (attempt + 1)
                print(f"query {i}: {e}; retrying in {wait}s", file=sys.stderr)
                time.sleep(wait)
        time.sleep(10)  # politeness between queries
    return raws

def main():
    if "--fetch" in sys.argv[1:]:
        raws = fetch()
    else:
        paths = [p for p in sys.argv[1:] if not p.startswith("--")]
        if not paths:
            sys.exit("give cached Overpass JSON files as args, or --fetch")
        raws = [json.load(open(p)) for p in paths]

    seen = set()
    feats = []
    for raw in raws:
        for e in raw.get("elements", []):
            key = (e["type"], e["id"])
            if key in seen:
                continue
            seen.add(key)
            t = e.get("tags", {})
            if not keep(t):
                continue
            if "lat" in e:
                lat, lon = e["lat"], e["lon"]
            elif e.get("center"):
                lat, lon = e["center"]["lat"], e["center"]["lon"]
            else:
                continue
            country = country_of(lat, lon)
            feats.append({
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [round(lon, 7), round(lat, 7)]},
                "properties": {
                    "name": t.get("name") or t.get("dedication") or "(unnamed)",
                    "kind": classify(t),
                    "country": country,
                    "region_bucket": region_bucket(lat, lon, country),
                    "osm_type": e["type"],
                    "osm_id": e["id"],
                    "tags_raw": t,
                },
            })

    feats.sort(key=lambda f: (f["properties"]["region_bucket"],
                              f["properties"]["country"], f["properties"]["name"]))
    fc = {
        "type": "FeatureCollection",
        "properties": {
            "source": "OpenStreetMap via Overpass API",
            "license": "ODbL 1.0 — (c) OpenStreetMap contributors",
            "note": "Discovery layer: country/region derived from rough coordinate "
                    "boxes, not authoritative boundaries.",
            "generated": time.strftime("%Y-%m-%d"),
        },
        "features": feats,
    }
    out = HERE / "shrines.geojson"
    out.write_text(json.dumps(fc, ensure_ascii=False, indent=1))
    # summary
    from collections import Counter
    print(f"wrote {out} — {len(feats)} features")
    for bucket, n in Counter(f["properties"]["region_bucket"] for f in feats).most_common():
        print(f"  {bucket:14s} {n}")
    for kind, n in Counter(f["properties"]["kind"] for f in feats).most_common():
        print(f"  kind={kind:14s} {n}")

if __name__ == "__main__":
    main()
