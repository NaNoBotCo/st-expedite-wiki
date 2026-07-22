# geo/ — GIS layer for the Saint Expedite wiki

Harvested 2026-07-13. Two files, two provenances: an OSM discovery layer and a
hand-curated canonical-sites layer. They are complementary — neither replaces
the other.

## Files

### `shrines.geojson`
FeatureCollection of **177 Point features**: every OpenStreetMap element
worldwide whose `name` or `dedication` references Saint Expedite AND that is a
plausibly religious feature. Ways/relations are reduced to their Overpass
`center` point.

Feature properties: `name`, `kind` (church / chapel / oratory / wayside-shrine
/ other), `country`, `region_bucket` (reunion / brazil / argentina / italy /
new-orleans / philippines / france / other), `osm_type`, `osm_id`, `tags_raw`
(the full original OSM tag dict).

### `curated_sites.json`
**15 hand-curated canonical sites** from the wiki's own research (New Orleans,
Réunion, Argentina, Brazil, Chile, Italy, Austria, France), each with
coordinates verified against Nominatim/OSM. Fields: `name`, `city`, `country`,
`lat`, `lon`, `role` (one line on why it matters), `confidence`
(verified / approximate). All 15 geocoded as **verified**.

### `build_shrines.py`
The stdlib-only generator for `shrines.geojson`. Rerun any time:

    python3 build_shrines.py --fetch          # queries Overpass live (polite: 2 queries, retries on failure)
    python3 build_shrines.py raw1.json ...    # or from cached Overpass responses

## How shrines.geojson was produced

Two Overpass API queries against `https://overpass-api.de/api/interpreter`
(POST, `data=` urlencoded):

```
[out:json][timeout:180];
(
  nwr["name"~"Exp[eé]dit",i];
  nwr["dedication"~"Exp[eé]dit",i];
);
out center tags;
```

and a second identical query with `"Espedit"` — the Italian spelling
(Sant'Espedito) that the first regex misses.

Raw yield was ~2,700 elements, heavily polluted by streets named after the
saint (or after people named Expedito), "Expedition"-named features, farms,
shops and bus stops. Post-processing keeps an element only if:

1. name/dedication matches a *saint* pattern —
   `\b(sant'?|santo|san|são|saint|st\.?|ste)\b[\s\-'.]*e[sx]?p[eé]dit` (case-insensitive); and
2. it carries no street/transport tags (`highway`, `railway`,
   `public_transport`, ...); and
3. it is religious by tags (`amenity=place_of_worship`,
   `historic=wayside_shrine|wayside_cross|memorial|monument`,
   `building=church|chapel|...`, `man_made=cross`, `tourism=artwork`,
   any `religion=*`) **or** its name contains a church-word
   (chapelle, capela, igreja, chiesa, oratoire, santuário, grotte, statue, croix, ...).

## Counts (2026-07-13 snapshot)

By region_bucket:

| bucket    | features |
|-----------|---------:|
| brazil    | 118 |
| argentina | 40 |
| other     | 9 (Chile 4, Bolivia, Nicaragua, Azores, Spain, USA-Louisiana) |
| reunion   | 7 |
| italy     | 3 |
| france / new-orleans / philippines | 0 |

By kind: church 92, chapel 49, wayside-shrine 27, other 8 (statues, murals,
altars, communities), oratory 1.

## Data-quality caveats

- **Réunion is massively under-represented.** The island's famous red roadside
  shrines number in the hundreds, but OSM has only 7 *named* Saint-Expédit
  features there. A dedicated bbox sweep of Réunion
  (`historic=wayside_shrine` + `amenity=place_of_worship`, bbox
  −21.5,55.1,−20.8,55.9) found 398 religious features, of which 55 are wayside
  shrines — but most are unnamed or Marian-named, so they cannot be attributed
  to the saint from OSM data alone. Treat the Réunion layer as a floor, not a
  count; field survey or the wiki's own research must fill the gap.
- **Zero hits for new-orleans / france / philippines is an artifact of
  dedication, not absence.** The New Orleans shrine is the *Our Lady of
  Guadalupe* chapel; the historic French sites (Marseille, Bordeaux, Toulouse)
  are churches dedicated to other patrons that merely house the devotion.
  Those live in `curated_sites.json` instead.
- `country` and `region_bucket` come from **rough coordinate bounding boxes**,
  not authoritative boundaries — border-zone features (esp. Chile/Argentina
  Andes, France/Italy Alps) may be mis-bucketed. This is a discovery layer;
  verify before citing.
- Near-duplicate features exist where OSM mappers added both a node and a way
  for the same shrine (e.g. Sainte-Suzanne, Réunion).
- Brazilian dominance (118/177) partly reflects real devotional density and
  partly Brazil's very active OSM community; absence elsewhere is weak
  evidence of absence.

## Attribution (required)

`shrines.geojson` is derived from **OpenStreetMap** data, © OpenStreetMap
contributors, licensed under the **Open Database License (ODbL) 1.0**
(opendatacommons.org/licenses/odbl/). Any wiki page, map tile, or derived
dataset that displays or redistributes this layer must credit
"© OpenStreetMap contributors" and, if the data is redistributed or adapted,
must be shared under ODbL. Curated-site coordinates were verified via OSM's
Nominatim geocoder and inherit the same attribution requirement.
