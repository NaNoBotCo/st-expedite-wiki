# Google Trends — manual export workflow

Google Trends has no stable public API (automated requests get 429'd; the
unofficial libraries break regularly). Rather than build on sand, we ingest
**CSV files exported by hand from the Trends UI** — a 10-minute task that only
needs redoing when we want fresher data. The wiki's methods page states this
choice openly: it's part of showing the process.

## The disambiguation trick

"Expedite" is an ordinary English verb, so never query the bare word.
Two clean routes:

1. **Topic entity (best):** in the Trends search box type `Expeditus` and pick
   the suggestion labeled **"Expeditus — Saint"** (a knowledge-graph topic, not
   a string). Google disambiguates at the source, all languages roll up into one
   series. Use this for the headline chart.
2. **Saint-specific phrases (per-country texture):** the phrases below are
   unambiguous because nobody types them about logistics.

## What to export (each = one CSV via the ⬇ button on the chart)

Save into `data/trends/` with EXACTLY these names:

| File | Query | Geo | Time |
|---|---|---|---|
| `topic-worldwide-2004.csv` | topic "Expeditus — Saint" | Worldwide | 2004–present |
| `santo-expedito-BR-5y.csv` | `"santo expedito"` | Brazil | past 5 years |
| `santo-expedito-BR-90d.csv` | `"santo expedito"` | Brazil | past 90 days (**daily** — hunting the 19th-of-month sawtooth) |
| `san-expedito-AR-5y.csv` | `"san expedito"` | Argentina | past 5 years |
| `san-expedito-CL-5y.csv` | `"san expedito"` | Chile | past 5 years |
| `saint-expedit-RE-5y.csv` | `"saint expédit"` | Réunion | past 5 years |
| `saint-expedite-US-5y.csv` | `"saint expedite"` | United States | past 5 years |
| `topic-worldwide-region.csv` | topic, "interest by subregion" table | Worldwide | 2004–present |

Optional extras that would be lovely: related-queries CSVs for Brazil and
Réunion (what people ask *alongside* the saint).

## What we expect to see (hypotheses the charts test)

- **April 19 spike** everywhere, annually.
- **Monthly sawtooth on the 19th** in the Brazil daily data (the dia-19 practice).
- Réunion's interest sustained year-round (roadside cult, not calendar cult).
- US interest flatter, spiking with media moments (the hoodoo revival wave).

`build.py` ingests whatever CSVs exist in `data/trends/` and skips gracefully
when a file is absent — export what you feel like, the site adapts.
