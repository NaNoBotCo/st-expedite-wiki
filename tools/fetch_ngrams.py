#!/usr/bin/env python3
"""fetch_ngrams.py — pull Google Books Ngram time-series for Saint-Expedite terms.

Stdlib only. Polite: one request per corpus batch, 2s sleep between.

The polysemy problem (and how we solve it): "expedite" is an ordinary English
verb, so the bare word measures nothing about the saint. We therefore query
SAINT-SPECIFIC SURFACE FORMS per language ("Saint Expedite", "saint Expédit",
"Sant'Espedito"...) and ALSO fetch the bare verb as an explicit noise baseline,
so the wiki can show the separation rather than hide it. Google Ngrams is
case-sensitive, which works in our favour: the saint is always capitalized.

Known limitation surfaced deliberately: Google has NO Portuguese corpus, so
Brazil — the largest devotion on earth — is invisible in book data. The wiki's
methods page states this out loud.

    python3 tools/fetch_ngrams.py            # writes data/ngrams.json
"""
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
OUT = HERE / "data" / "ngrams.json"

YEAR_START, YEAR_END, SMOOTHING = 1800, 2019, 3
UA = {"User-Agent": "Mozilla/5.0 (st-expedite-wiki research; polite stdlib fetcher)"}

# (corpus, [phrases], note) — phrases in one request share a corpus.
# Case matters: saint names are capitalized, the noise baseline is not.
QUERIES = [
    ("en-2019", ["Saint Expedite", "St. Expeditus", "Saint Expeditus", "Expeditus"],
     "English saint-specific forms"),
    ("en-2019", ["expedite"],
     "NOISE BASELINE — the ordinary English verb; shown to demonstrate the polysemy problem"),
    ("fr-2019", ["saint Expédit", "Saint Expédit"],
     "French forms (feeds Réunion + metropolitan France)"),
    ("it-2019", ["Sant'Espedito", "sant'Espedito", "Espedito"],
     "Italian forms (Acireale/Palermo/Naples root cult)"),
    ("es-2019", ["San Expedito"],
     "Spanish forms (Argentina/Chile/Mexico/Spain)"),
    ("de-2019", ["Expeditus", "heilige Expeditus"],
     "German forms (the great 1870s-1920s Austro-German cult)"),
]


def fetch(corpus: str, phrases: list[str]) -> list[dict]:
    qs = urllib.parse.urlencode({
        "content": ",".join(phrases),
        "year_start": YEAR_START,
        "year_end": YEAR_END,
        "corpus": corpus,
        "smoothing": SMOOTHING,
    })
    url = f"https://books.google.com/ngrams/json?{qs}"
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())


def main() -> int:
    series = []
    for corpus, phrases, note in QUERIES:
        try:
            rows = fetch(corpus, phrases)
        except Exception as e:  # keep going; record the failure honestly
            print(f"  !! {corpus} {phrases}: {e}", file=sys.stderr)
            series.append({"corpus": corpus, "requested": phrases, "note": note,
                           "error": str(e)})
            time.sleep(2)
            continue
        got = {row["ngram"] for row in rows}
        for row in rows:
            ts = row["timeseries"]
            nz = [i for i, v in enumerate(ts) if v > 0]
            series.append({
                "ngram": row["ngram"],
                "corpus": corpus,
                "note": note,
                "first_year": YEAR_START + nz[0] if nz else None,
                "peak_year": YEAR_START + ts.index(max(ts)) if nz else None,
                "years": [YEAR_START, YEAR_END],
                "timeseries": ts,
            })
            print(f"  ok {corpus:8s} {row['ngram']!r:28s} first={YEAR_START + nz[0] if nz else '-'} "
                  f"peak={YEAR_START + ts.index(max(ts)) if nz else '-'}")
        for missing in set(phrases) - got:
            print(f"  -- {corpus:8s} {missing!r}: no hits in corpus")
            series.append({"ngram": missing, "corpus": corpus, "note": note,
                           "first_year": None, "peak_year": None,
                           "years": [YEAR_START, YEAR_END], "timeseries": []})
        time.sleep(2)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "generated_note": "Google Books Ngram data; smoothing=3; case-sensitive. "
                          "No Portuguese corpus exists — Brazil is invisible here by "
                          "tooling limitation, not by absence of devotion.",
        "params": {"year_start": YEAR_START, "year_end": YEAR_END, "smoothing": SMOOTHING},
        "series": series,
    }, ensure_ascii=False, indent=1))
    print(f"\nwrote {OUT} ({len(series)} series)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
