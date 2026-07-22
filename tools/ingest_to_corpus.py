#!/usr/bin/env python3
"""ingest_to_corpus.py — fold the St. Expedite corpus into the shared wichaa
catalog (`manuscript-crawler/crawler/catalog.db`) as a coequal tradition.

This is Layer 2 of the wichaa re-root (see manuscript-wiki/REROOT_PLAN.md):
St. Expedite stops being a federated island and becomes real rows in the same
`sources` + `items` spine that already holds Lanna manuscripts, Lazada amulets,
and museum objects. Tradition is derived from source_id (see taxonomy.py).

Idempotent: it deletes any prior St.-Expedite sources/items (by the marker in
`sources.robots_notes`) and re-inserts from the local geo/ data. Stdlib only.

    python3 tools/ingest_to_corpus.py           # ingest / re-ingest
    python3 tools/ingest_to_corpus.py --dry-run # report only, no writes
"""
import argparse
import json
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
CATALOG = HERE.parent / "manuscript-crawler" / "crawler" / "catalog.db"
MARKER = "wichaa-tradition:st-expedite"   # tag in robots_notes to find our sources
NOW = datetime.now(timezone.utc).isoformat()

# The three provenances St. Expedite content is harvested from.
SOURCES = [
    ("St. Expedite — OpenStreetMap shrines", "https://www.openstreetmap.org", "overpass"),
    ("St. Expedite — Wikimedia Commons imagery", "https://commons.wikimedia.org", "rest_json"),
    ("St. Expedite — research corpus (nanobotco)", "local:st-expedite-wiki", "contributed"),
]


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", (s or "").lower()).strip("-")[:60]


def load_places():
    """Yield normalized item dicts from the OSM + curated geo layers."""
    geo = json.loads((HERE / "geo" / "shrines.geojson").read_text())
    for f in geo["features"]:
        p = f["properties"]
        lon, lat = f["geometry"]["coordinates"]
        yield {
            "prov": "osm",
            "source_identifier": f"osm/{p.get('osm_type','node')}/{p.get('osm_id')}",
            "kind": p.get("kind", "shrine"),
            "title": p.get("name") or "(unnamed shrine)",
            "location": p.get("country", ""),
            "url": f"https://www.openstreetmap.org/{p.get('osm_type','node')}/{p.get('osm_id')}",
            "meta": {"lat": lat, "lon": lon, "osm_id": p.get("osm_id"),
                     "osm_type": p.get("osm_type"), "region": p.get("region_bucket"),
                     "tradition": "St. Expedite"},
        }
    cur = json.loads((HERE / "geo" / "curated_sites.json").read_text())
    for s in cur["sites"]:
        loc = ", ".join(x for x in (s.get("city"), s.get("country")) if x)
        yield {
            "prov": "research",
            "source_identifier": f"curated/{slugify(s['name'])}",
            "kind": "shrine",
            "title": s["name"],
            "location": loc,
            "url": "",
            "meta": {"lat": s.get("lat"), "lon": s.get("lon"), "role": s.get("role"),
                     "confidence": s.get("confidence"), "curated": True,
                     "tradition": "St. Expedite"},
        }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    if not CATALOG.exists():
        sys.exit(f"catalog not found: {CATALOG}")

    places = list(load_places())
    prov_counts = {}
    for pl in places:
        prov_counts[pl["prov"]] = prov_counts.get(pl["prov"], 0) + 1
    print(f"prepared {len(places)} items ({prov_counts})")
    if args.dry_run:
        for pl in places[:3]:
            print("  e.g.", pl["source_identifier"], "|", pl["kind"], "|", pl["title"][:40])
        return

    db = sqlite3.connect(CATALOG)
    db.row_factory = sqlite3.Row
    cur = db.cursor()

    # 1) idempotent cleanup of any prior ingest
    old = [r["id"] for r in cur.execute(
        "SELECT id FROM sources WHERE robots_notes LIKE ?", (f"%{MARKER}%",))]
    if old:
        q = ",".join("?" * len(old))
        n = cur.execute(f"DELETE FROM items WHERE source_id IN ({q})", old).rowcount
        cur.execute(f"DELETE FROM sources WHERE id IN ({q})", old)
        print(f"  cleaned prior ingest: {len(old)} sources, {n} items")

    # 2) insert the three sources
    src_id = {}
    for name, base, api in SOURCES:
        cur.execute(
            "INSERT INTO sources(name, base_url, api_type, robots_notes, status, last_crawled)"
            " VALUES(?,?,?,?,?,?)",
            (name, base, api, f"St. Expedite tradition. {MARKER}. Open/CC-PD data.",
             "crawled", NOW))
        src_id[api] = cur.lastrowid
    osm_src, img_src, res_src = src_id["overpass"], src_id["rest_json"], src_id["contributed"]
    print(f"  sources: OSM={osm_src} Commons={img_src} research={res_src}")

    # 3) insert items
    ins = 0
    for pl in places:
        sid = osm_src if pl["prov"] == "osm" else res_src
        cur.execute(
            "INSERT INTO items(source_id, source_identifier, kind, title_english,"
            " method, medium, location_text, source_url, first_seen, last_seen, raw_metadata)"
            " VALUES(?,?,?,?,?,?,?,?,?,?,?)",
            (sid, pl["source_identifier"], pl["kind"], pl["title"],
             "devotion", "shrine", pl["location"], pl["url"], NOW, NOW,
             json.dumps(pl["meta"], ensure_ascii=False)))
        ins += 1
    db.commit()

    # 4) report
    print(f"  inserted {ins} items (method='devotion')")
    tot = cur.execute("SELECT COUNT(*) FROM items WHERE method='devotion'").fetchone()[0]
    bycountry = cur.execute(
        "SELECT location_text, COUNT(*) c FROM items WHERE method='devotion'"
        " GROUP BY location_text ORDER BY c DESC LIMIT 6").fetchall()
    print(f"  corpus now holds {tot} St. Expedite items; top locations:",
          {r["location_text"]: r["c"] for r in bycountry})
    db.close()
    print("done.")


if __name__ == "__main__":
    main()
