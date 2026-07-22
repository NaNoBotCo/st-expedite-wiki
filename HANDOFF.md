# St. Expedite Wiki — Handoff

A small, self-contained static wiki on the global cult of Saint Expedite. Built to
sit alongside the Lanna manuscript and Lazada amulet corpora as a third domain, and
handed off here for continued, incremental content work by a simpler assistant.

## Run it

- **Double-click `Expedite Wiki.command`** — rebuilds and opens the site. That's the whole workflow.
- Or: `python3 build.py` (add `--no-media` to skip the 52 MB image copy while iterating).
- Output is a plain folder of HTML in `docs/`. No server, no dependencies, stdlib Python only.

## Add or edit an article (the one thing you'll do most)

1. Copy any file in `content/` (e.g. `reunion.md`) to a new `content/your-slug.md`.
2. Edit the header block between the `---` lines, then write the body in Markdown.
3. Rebuild. The article, its facet chips, and its facet-node pages appear automatically.

### The header fields

```
title: New Orleans & hoodoo         # shown as the page H1
slug: new-orleans                   # optional; defaults to the filename
type: practice-ritual               # one archetype (entity, legend-variant, place-shrine, …)
reliability: practitioner-consensus # REQUIRED, pick ONE — see below
register: folk-magic-hoodoo, syncretic-vernacular   # comma list, any number
geography: new-orleans-louisiana    # comma list
patronage: speed, urgent-causes     # comma list
hero: 022-new-orleans-...jpg        # optional; a filename from images/commons/
summary: One sentence for cards and the lead.
sources:
- Title of source | https://url
- Another source | https://url
```

Every comma-list value becomes a browsable **node page** automatically — you don't
register facets anywhere. Inventing a new value just makes a new node. Keep values
lowercase-hyphenated and reuse existing ones where they fit (see the list the build
prints, or the chips at the bottom of `docs/reliability.html`).

### RELIABILITY is the point of this wiki — pick honestly

This is the load-bearing facet. St. Expedite content mixes scholarship, devotion,
legend, and sales copy; the wiki stays honest by tagging **where each page's authority
comes from**, not by ranking pages "true/false." Choose one:

| value | use when the page rests on… |
|---|---|
| `documented` | a primary or solid secondary record |
| `scholarly-contested` | real scholars actively disagree |
| `legend` | a story told as fact but treated as folk-etymology |
| `practitioner-consensus` | what devotees/practitioners actually do |
| `commercial-claim` | what the candle/botánica trade sells and believes |

**In the body**, mark individual claims inline the same way the seed articles do:
`*Documented —*`, `*Scholarship —*`, `*Tradition —*`, `*Practitioner —*`, `*Inference —*`,
`*Contested —*`, `*Refused —*`. This is the house voice; keep it up. Never launder a
devotional embellishment into a plain statement of fact.

## What's already here

- **9 core articles** (`content/`): overview, iconography, the crate legend, New Orleans,
  Réunion, Brazil/Latin America, Italy & the Austro-German cult, the controversy, prayers & rituals.
- **107 images** (`images/commons/`, CC/PD) with `images/manifest.json` (806 enumerated) and
  auto-generated `images/ATTRIBUTION.md`. → the **Gallery** page.
- **Geo**: `geo/shrines.geojson` (177 named OSM shrines) + `geo/curated_sites.json` (15 verified).
  → the **Map** page (Leaflet). Rebuild the harvest with `geo/build_shrines.py --fetch`.
- **Ngrams**: `data/ngrams.json` (5 language corpora). → the **The data** page's SVG charts.
  Refresh with `python3 tools/fetch_ngrams.py`.
- **Trends**: drop hand-exported CSVs in `data/trends/` per `tools/TRENDS.md`; the data page
  lists them (charting them is a nice next task — the CSVs are ready).
- **Research substrate** (not shown on the site, but the source of truth for writing):
  `CONTENT_INVENTORY.md` (the map + taxonomy), `background/01–06` (URL-cited, reliability-tagged
  digests), `research-raw.json` (the verified claim ledger).

## Good next tasks (in rough priority order)

1. **Write more articles** from `background/` — obvious gaps: a dedicated **feast day (19 April
   & the 19th-of-the-month)** page, **relics & holy cards**, **media & music**, per-country stubs
   (Chile, Philippines, Spain). The research is already done and cited in `background/`.
2. **Chart the Trends CSVs** once exported — especially hunt the **19th-of-month sawtooth** in
   Brazil's daily data (would confirm the *dia-19* devotion from independent data).
3. **Re-fetch the newspaper notices**: `tools/fetch_newspapers.py` got HTTP 403 from the Library
   of Congress; the search hits are logged in `pd-texts/newspapers-raw.json` awaiting a gentler pull.
4. **Réunion shrine mapping** — the map shows 7 of ~340; the rest are unnamed in OSM. A long-term
   contribution opportunity, flagged on the map and methods pages.

## Rules of the house

- **Stdlib only.** No pip installs. If a task seems to need a library, it probably doesn't.
- **Cite everything.** Each article needs a `sources:` list; each contested claim gets an inline tag.
- **Don't assert what the research refused.** See `docs/methods.html` — no XII Fulminata legion,
  no "hundreds of thousands," no single clean "Vatican removal" date, no cloak-origin for the red.
- **Represent faithfully, don't editorialize.** Commerce and folk-magic are first-class practice
  here, not lesser forms — tag them by register/reliability, never dismiss them.
