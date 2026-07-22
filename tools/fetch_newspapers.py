#!/usr/bin/env python3
"""fetch_newspapers.py — harvest period newspaper mentions of St. Expedite from
the Library of Congress Chronicling America collection (all pre-1930 = PD).

Stdlib only, polite (2s between requests). Writes pd-texts/newspapers-raw.json
with an OCR excerpt window around each mention; the good ones become quotable
primary sources on the wiki (link back to the LOC scan for the facsimile).

    python3 tools/fetch_newspapers.py
"""
import json
import re
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
OUT = HERE / "pd-texts" / "newspapers-raw.json"
UA = {"User-Agent": "st-expedite-wiki-research (polite stdlib fetcher)"}

SEARCHES = ['%22st.+expedite%22', '%22saint+expedite%22', '%22st.+expeditus%22']


def get(url, tries=3):
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode())
        except Exception:
            if attempt == tries - 1:
                raise
            time.sleep(8 * (attempt + 1))  # LOC throws transient 525s


def get_text(url, tries=3):
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read().decode("utf-8", "replace")
        except Exception:
            if attempt == tries - 1:
                raise
            time.sleep(8 * (attempt + 1))


def ocr_url(resource_id):
    """Map a www.loc.gov resource id to the legacy Chronicling America ocr.txt.

    http://www.loc.gov/resource/sn90059959/1906-02-03/ed-1/?sp=4
      -> https://chroniclingamerica.loc.gov/lccn/sn90059959/1906-02-03/ed-1/seq-4/ocr.txt
    """
    m = re.search(r"/resource/([^/]+)/([\d-]+)/(ed-\d+)/\?sp=(\d+)", resource_id)
    if not m:
        return None
    lccn, date, ed, seq = m.groups()
    return f"https://chroniclingamerica.loc.gov/lccn/{lccn}/{date}/{ed}/seq-{seq}/ocr.txt"


def main():
    hits = []
    for q in SEARCHES:
        try:
            d = get(f"https://www.loc.gov/collections/chronicling-america/?q={q}&fo=json&c=30")
            hits.extend(d.get("results", []))
            time.sleep(2)
        except Exception as e:
            print("search fail", q, e)

    seen, uniq = set(), []
    for it in hits:
        rid = it.get("id")
        if rid and rid not in seen:
            seen.add(rid)
            uniq.append(it)
    print("unique pages:", len(uniq))

    out = []
    for it in sorted(uniq, key=lambda x: x.get("date", "")):
        rid = it.get("id")
        try:
            txt_url = ocr_url(rid)
            ft = get_text(txt_url) if txt_url else ""
            ft = re.sub(r"\s+", " ", ft)
            m = re.search(r"(st\.?|saint)\s+expedit\w*", ft, re.I)
            window = ft[max(0, m.start() - 1200):m.end() + 1200] if m else "(term not located in OCR)"
            out.append({"date": it.get("date"),
                        "paper": (it.get("partof_title") or [it.get("title", "")])[0],
                        "state": it.get("location_state"), "url": rid, "excerpt": window})
            print("ok  ", it.get("date"), (it.get("partof_title") or [""])[0][:45])
        except Exception as e:
            out.append({"date": it.get("date"),
                        "paper": (it.get("partof_title") or [""])[0],
                        "url": rid, "excerpt": f"(fetch failed: {e})"})
            print("fail", it.get("date"), e)
        time.sleep(2)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print("saved", len(out), "->", OUT)


if __name__ == "__main__":
    main()
