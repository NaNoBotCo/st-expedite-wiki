# St. Expedite — Annotated Content Inventory

*Research pass for a wichaa-style wiki. Built from a verified deep-research crawl (6 angles, 22 sources fetched, 92 claims extracted, 25 adversarially verified — 18 survived, 7 killed). Raw findings in `research-raw.json`.*

**One-line map of the territory:** Expedite is one saint refracted through **three separate worlds that barely talk to each other** — (A) the Bollandist/church-history record, where he's a doubtful name in a martyr list; (B) Catholic devotion of "urgent causes," strongest in Latin/Mediterranean Europe and Brazil; and (C) a living folk-magic + syncretic cult with two intense poles, **New Orleans hoodoo** and **Réunion Island**. The "sysop nightmare" is that the *same* handful of facts (the crate legend, the crow, the Pius X removal) gets retold in each world with different framing and different reliability. A flat page list drowns; this needs facets.

---

## 1. The reliability problem (read this first — it drives the taxonomy)

Source strength is wildly uneven, and that unevenness is the organizing challenge. Four tiers, and almost every "fact" about Expedite sits in a different one:

| Tier | What it means | Example threads |
|---|---|---|
| **Documented** | Verifiable primary/secondary record | Feast day **19 April**; appears in the Hieronymian Martyrology among six Martyrs of Melitene; 1675 Acta Sanctorum mention; the standard iconographic *type* |
| **Scholarly-contested** | Real academics disagree | Whether he existed at all; Delehaye's "Expeditus = misreading of *Elpidius*" theory; what **Pope Pius X actually did in 1905** and when he was (or wasn't) removed from the calendar |
| **Legend / folk-etymology** | Repeated everywhere as fact, treated as apocryphal by scholarship | The **crate marked "spedito/expédit"** story (≥3 variants: 1781 Paris, New Orleans, Sicilian-immigrant Louisiana) |
| **Practitioner / commercial consensus** | True *as a description of what believers and vendors do* — not doctrinal authority | Pound-cake offerings, red flowers, the petition-and-thanks "contract," Lucky Mojo product lines, Réunion red shrines |

> **Design consequence:** every article and every claim needs a **reliability facet** (same spirit as your manuscript wiki's provenance-is-the-seam principle). Don't sort into "real vs fake" — represent each thread faithfully *and* tag where its authority comes from. This is also the honest way to handle the "is he a fake saint?" question without editorializing.

**Verified-killed claims** (things the crawl actively *refuted* — do NOT put these in the wiki as fact):
- ❌ "Commanded the *Legio XII Fulminata*" — devotional embellishment (0–3).
- ❌ "Crowds of hundreds of thousands in Latin America" — unsupported (0–3).
- ❌ Réunion red = the saint's purple military cloak — refuted; the supported reading is **Kali / Tamil-Malabar sacred red** (0–3 against the cloak theory).
- ⚠️ Réunion diocese "removed him from the calendar in 1965" — did not survive (1–2). Church *discomfort* is real; that specific institutional fact is not.
- ⚠️ Delehaye "Elpidius misreading" — real scholarship, but this specific phrasing split 1–2; include it *as a scholarly hypothesis*, cited, not as settled.

---

## 2. Proposed facet axes (the taxonomy that tames the sprawl)

Rather than a folder tree, model it the way you did the manuscript language decomposition: **facet values become nodes**, and any article can carry several. Five axes:

- **REGISTER / LENS** — `hagiography-scholarly` · `catholic-devotional` · `folk-magic-hoodoo` · `syncretic-vernacular` · `commercial` · `cultural-media`
- **GEOGRAPHY** — `melitene-origin` · `italy` · `france` · `germany` · `reunion` · `new-orleans-louisiana` · `brazil` · `spanish-america` · `philippines` · `global-online`
- **RELIABILITY** — `documented` · `scholarly-contested` · `legend` · `practitioner-consensus` · `commercial-claim` (from §1)
- **CONTENT TYPE (page archetype)** — `entity` · `legend-variant` · `practice-ritual` · `place-shrine` · `prayer-text` · `iconography-element` · `controversy` · `source`
- **FUNCTION / PATRONAGE** — `urgent-causes` · `against-procrastination` · `speed` · `merchants-commerce` · `exams-students` · `sailors` · `justice` · `curse-rival` (the dark Réunion pole)

The two projections (like your bots-vs-humans axes): **bots/search** traverse the facet graph; **human readers** follow desire paths — most will arrive via "New Orleans," "how to petition him," or "why is he holding a crow," not via "Melitene."

---

## 3. Candidate article inventory (annotated)

Grouped into the clusters a reader actually navigates. Each entry: **[reliability tier]** + one-line annotation + source strength. `★` = strong enough to write now; `◐` = writeable but thinly sourced / needs a caveat; `○` = gap, needs dedicated follow-up research.

### Cluster A — The Saint (entity + origin)
- ★ **Expeditus of Melitene** *(entity, documented/contested)* — the hub page. Anchor on what's solid (19 Apr feast; name in Hieronymian Martyrology among six Melitene martyrs; Acta Sanctorum 1675) and hedge the biography hard ("said to have been a Roman soldier"). *Source: Wikipedia (secondary), catholic.org, simple.wiki — converge on hedged form.*
- ★ **The crate legend** *(legend-variant)* — dedicated page with **all three variants side by side**: 1781 Paris convent · New Orleans (Ursulines / Our Lady of Guadalupe) · Sicilian-immigrant Independence, LA. Frame explicitly as folk-etymology. *Source: Wikipedia + Louisiana Folklife Program (state body, solid).* **This is a sysop-nightmare hotspot — see §5.**
- ◐ **Was he removed from the calendar? (Pius X, 1905)** *(controversy)* — the "manufactured saint" anchor. Sources genuinely disagree whether 1905 was about *images/statues* or a *martyrology entry*, and formal suppression is variously dated 1905 / 1969 / 2001. Present the disagreement itself as the content. *Source: Wikipedia citing Kuefler, "The Convertible Saint," J. Religious History 2018.*
- ◐ **The name: "expeditus" and the Elpidius hypothesis** *(scholarly-contested)* — Latin for a lightly-equipped/unencumbered soldier; Delehaye's misreading theory. Cite as hypothesis.

### Cluster B — Iconography
- ★ **The standard image** *(iconography-element, documented)* — Roman legionary; cross reading **HODIE** ("today"); **palm** of martyrdom; **crow/raven underfoot** with **CRAS** ("tomorrow") issuing from its beak; the today-vs-tomorrow pun. Note the minor variant: some early images showed a **clock** instead of the HODIE cross. *Source: 4 independent sources, 3–0.*
- ◐ **Regional image variants** *(iconography-element)* — Réunion's blood-red treatment; Brazilian holy-card conventions. Partly a gap.

### Cluster C — Catholic devotion by country
- ★ **Patron of urgent & just causes** *(entity/function)* — speed, against procrastination, plus merchants, exams, sailors. Well attested as the devotional core. *Source: holyart, catholic.org, reginamag (devotional/blog but consistent).*
- ◐ **Brazil — Santo Expedito** *(geography, practitioner)* — flagged as *huge* (Rio churches, possible November "month") but the crawl's Brazilian claims were thin and the big crowd figure was refuted. **Needs dedicated Portuguese-language research.** *(open question.)*
- ○ **Italy (Acireale, Sicily; Turin)** — essentially unsourced in the verified set. Gap.
- ○ **Germany** — "was popular, then declined" — unsourced. Gap.
- ○ **Chile / Argentina / Peru / Mexico / Spain** — Spanish-America devotion asserted but not yet sourced. Gap.
- ○ **Philippines** — gap.

### Cluster D — New Orleans & hoodoo
- ★ **Our Lady of Guadalupe Chapel statue** *(place-shrine)* — near St. Louis Cemetery No.1 (Marie Laveau's burial); "most photographed saint statue in the city." *Source: Louisiana Folklife + blogs.*
- ★ **Pound cake offerings** *(practice-ritual, practitioner)* — feed the saint (locally, Sara Lee) for granting favors; "one must feed the gods." *Source: Louisiana Folklife (solid) + Wikipedia Louisiana Voodoo.* Caveat: scholars split **hoodoo (folk-magic) vs Voodoo (religion)** — the pound-cake practice is more precisely hoodoo. Handle the blur explicitly.
- ★ **Petition-and-thanks "contract"** *(practice-ritual)* — the deal structure: ask, promise public thanks, and *publish the thank-you* (historically newspaper notices) once granted. *Source: AIRR readersandrootworkers (practitioner-scholarly), aromags.*
- ★ **Syncretism with Louisiana Voodoo** *(syncretic-vernacular)* — "voodoo saint." *Source: Wikipedia Louisiana Voodoo, 3–0.*

### Cluster E — Réunion Island (its own world)
- ★ **The red-shrine cult** *(place-shrine, geography)* — first statue **1931** (St-Denis); ~94 oratories in 1970 → **337–338 + 31 chapels by 1997/98** (Reignier's census / doctoral thesis); "340+" today ≈ one shrine per 2,000 people. Treat 340+ as a **floor** (recycles the '98 census, excludes home shrines). *Source: Presses universitaires de Rennes (academic, primary-ish) + 7 Lames la Mer + les-oratoires.asso.fr.* **Mostly French-language.**
- ★ **Syncretism with Tamil/Hindu & Malagasy practice** *(syncretic-vernacular)* — blood-red from **Kali**; some devotees abstain from meat, pray in Tamil; venerated by Catholics, Hindus, Malagasy alike. *Source: PU Rennes.* (Cloak-origin theory refuted — see §1.)
- ★ **The dark / ambivalent reputation** *(function: curse-rival, controversy)* — invoked not just for jobs/health/exams but to **eliminate rivals in love or business**; feared for swift retribution if a vow goes unpaid ("pay him, and quickly"); official Church uneasy. *Source: PU Rennes, 3–0.* (Specific 1965 diocesan-removal claim refuted.)

### Cluster F — Prayers, rituals, offerings
- ★ **Standard novena + petition prayer** *(prayer-text)* — the 9-day form. *Source: AIRR, aromags.*
- ★ **Offerings catalog** *(practice-ritual)* — red flowers, pound cake, coins, water; and what devotees promise in return. *Source: AIRR (practitioner), Lucky Mojo.*

### Cluster G — Controversy & scholarship
- ◐ **"Is he a fake saint?"** *(controversy)* — synthesize: no reliable evidence he existed; Bollandist skepticism; Pius X action; the "manufactured/commodity saint" framing. Compare to **St. Jude & St. Rita** (emergency/lost-causes saints). *Source: Kuefler academic article is the spine; needs one more scholarly fetch.*

### Cluster H — Media, commerce, culture
- ★ **Botánica & candle commerce** *(commercial)* — Lucky Mojo (cat yronwode) full product line: dressing oil, incense/sachet powders, bath crystals, vigil candles — "rapid results, luck in a hurry." Reliable *as evidence of the trade*, not history. *Source: luckymojo.com (primary for commerce).*
- ○ **Songs / films / literature / place names** — named in the brief, not yet surfaced. Gap.

---

## 4. Source base, annotated by quality

**Strong / citable spine:**
- `books.openedition.org/pur/4689` — Presses universitaires de Rennes, *Mémoire et Histoire: le culte de Saint-Expédit à la Réunion* — **the best scholarly source**, carries the whole Réunion + syncretism cluster. French.
- `louisianafolklife.org/.../lfmexpedito.html` — Louisiana Folklife Program (state body) — spine for New Orleans / Louisiana + the third crate variant.
- `en.wikipedia.org/wiki/Expeditus` + `/Louisiana_Voodoo` — solid secondary hubs; the Kuefler *Journal of Religious History* citation is the academic anchor for the controversy thread.
- `readersandrootworkers.org` (AIRR) — practitioner-scholarly; best hoodoo-side source for ritual structure.
- `luckymojo.com` — primary *for commerce only*.

**Useful but caveated (blogs / devotional / journalistic):** anastpaul, reginamag, holyart, artoftheroot, americashauntedroadtrip, hubpages, jamesduvalier, aromags, 7lameslamer (respected Réunionnais outlet), les-oratoires.asso.fr.

**Flagged unreliable — do not cite as authority:** grokipedia, stexpeditus.org, omunicipio (Brazil blog), reunion-tourisme.info. (Some are still useful as *evidence of vernacular belief*, tagged `commercial-claim`/`practitioner-consensus`.)

---

## 5. The sysop-nightmare hotspots (where content will duplicate & fight)

1. **The crate legend** — retold identically in Paris, New Orleans, and Sicilian-Louisiana framings across a dozen sources, each claiming *its* version. → **One canonical `legend-variant` page with a variants table**, everything else links to it. Don't let it metastasize into every geography page.
2. **Pound cake / offerings** — appears under New Orleans, under hoodoo, under "rituals," under commerce. → **One `practice-ritual` node**, transcluded/linked, not re-written per cluster.
3. **Pius X / "removed from calendar"** — the single most-mangled fact. → Make the *disagreement* the content; never assert a single date.
4. **hoodoo vs Voodoo** — popular sources blur them; scholars don't. → Glossary node defining the distinction, linked wherever the blur appears.
5. **Réunion red = Kali (not cloak)** — an actively-refuted alternative is circulating. → Bake the correction into the page so it doesn't creep back in.
6. **Reliability collision** — the biography (weak) and the practices (well-attested-as-practice) sit on the *same* saint. → the RELIABILITY facet from §2 is what keeps a devotional embellishment from reading as history.

---

## 6. Open gaps → recommended follow-up research (before or during build)

From the crawl's own open-questions, prioritized:
1. **Brazil (Santo Expedito)** — Portuguese-language dive: Rio churches, the November question, actual scale. *Biggest gap vs. the brief.*
2. **Pius X 1905** — pin down the primary act (Congregation of Rites decree on images? martyrology deletion?) and the real calendar-status timeline (1969 vs 2001).
3. **Italy (Acireale, Turin) & Germany** — dedicated Italian/German sourcing; currently unsourced.
4. **Media/culture** — songs, films, place names, churches.
5. **Spanish-America & Philippines** — devotion asserted, not sourced.

Each is a clean, scoped follow-up crawl when you want it — narrow now, easy to widen.

---

## 7. Suggested build shape (for when you greenlight it)

A **small Python generator** (as chosen), simpler than wichaa's dynamic server:
- `content/` — one Markdown-ish data file per article, with YAML front-matter carrying the five facets from §2 + a `sources:` list + per-claim `reliability` tags.
- `build.py` (stdlib only) — reads `content/`, renders static HTML into `docs/`, auto-builds facet index pages (one per node) and a reliability-filtered view. No DB, no server.
- One stylesheet, high-contrast / large-type friendly.
- Start with the **★ articles** (Clusters A–F core) — that's a complete, honest small wiki on day one; the `○` gaps fill in as follow-up research lands.

*Nothing built yet — this is the map. Say the word on scope (all clusters now, or ★-only first) and I'll stand up the generator.*

---

## 8. Addendum — what the background crawl changed (2026-07-13, `background/01–06`)

The five-agent deep crawl (~144 KB of URL-cited digests in `background/`) **upgrades or corrects** the map above:

**Corrections / resolutions:**
- **Pius X 1905** (§3-A, §5.3): no primary decree exists anywhere online — the claim rests entirely on Kuefler 2018. Crucially, the old Roman Martyrology *retained* the six-martyr entry after 1905 → it was an **images/devotions action, not a martyrology deletion**. Contemporary lead to chase: Thurston, "Flotsam and Jetsam," *The Month* 108 (Dec 1905) 546. He was **never on the General Roman Calendar** at all. Effect confirmed by the German cluster: the 1905 intervention is what *killed* the huge Austro-German cult.
- **Réunion 1965** (§1 killed-claims): now **attested with sources** — removal from the Réunion *diocesan* calendar 1965, inside a documented arc: 1931 episcopal blessing → 1965 removal → never condemned → Bp. Aubry's "culte carrefour" stance + Père Payet's imprimatur prayer booklet. The earlier 1–2 kill was over-broad; the wiki page can carry this cited.
- **Crate legend** (§3-A): Times-Picayune dates the New Orleans version to **c. 1921**; a *fourth+* localization exists (São Paulo, Haiti); and it's **disproven as origin** — German/Sicilian veneration predates all versions. Morgenstern's satirical poem "St. Expeditus" (*Palmström*, 1910) is itself a vector that popularized the parcel story.
- **Latin-America scale** (§6.1): biggest verified crowd is **Buenos Aires Balvanera, ~70,000** on 19 Apr 2026 (Archdiocese via La Nación) — not Brazil. "Hundreds of thousands" fails everywhere; full crowd ledger in `05-brazil-latam.md`.

**New structural anchors (become articles):**
- **Italy is the deep root**: Messina 17th c. → Acireale 18th c.; **18 Apr 1781 Expeditus made secondary patron of Acireale** (merchants & navigators) — the *documented* 1781 event mirroring the *legendary* Paris parcel of the same year. Plus Palermo 1935 church, Bologna confraternity 1903, Naples "flying novena" for exams, contested pre-1437 Turin street name.
- **Iconography has a datable evolution**: Sicilian church images (late 17th c.) → German pointing-at-clock type (18th c., no crow) → clock+crow → HODIE-cross+CRAS standard, mass-diffused late 19th c. → distinct Turin old-man-with-clock type.
- **Germany/Austria cluster**: "der eilige Heilige," among the most-beloved folk saints 1870s–1920s (Grabner), Vienna hub, Graz Franziskanerkirche survivor statue.
- **France→Réunion transmission precisely dated**: Fanny Fleurié's WWI-era vow at Marseille Saint-Cannat → statue blessed 3 May 1931, Saint-Denis. Named founder!
- **Réunion depth**: 28% of statues decapitated (four competing meanings); Eve's wandering-souls siting thesis (accident sites, dangerous bends); statues as living bodies (priest-led removal); Madagascar carves "Saint-Expédit malgache" statuettes solely for Réunionnais buyers — no cult there.
- **New Orleans earliest attestation**: Hyatt fieldwork **1935–39** — debt paid in *flowers*, not cake; Baron Samedi link is NOLA-only (Haiti's Ghede use a black/purple cross); chapel = 1827 yellow-fever mortuary chapel.
- **The 19th of every month** is the global observance rhythm (Chile Reñaca: 15–20k *monthly*), not just April 19.
- **Brazil's distinctive practice**: *promessa do milheiro* — vow to print 1,000 santinhos and scatter them; stock product at gráficas (~R$20/thousand); online promessa portals. Flagship shrine: Santuário Diocesano, town of **Santo Expedito, SP** (town named for the saint). São Paulo city site = Capela Militar (ROTA barracks, 1942), *not* Itaquera.
- **Philippines**: 18th-c. Franciscan attribution, 10+ named parishes, Tagalog novenas.
- **Media**: Kuefler notes the image was adopted by **Italian fascists and Haitian vodou** (Haiti *inverts* the image to curse — same saint, opposite polarity). Films: *Cachez ce saint !* (Crutzen 2010), KTO's *Sur les chemins de saint Expedit*. Song: Grant-Lee Phillips "St. Expedite."

**Re-crawl gaps flagged:** louisianafolklife.org (DNS down), readersandrootworkers.org (Cloudflare 403), reginamag (TLS), maloya/NOLA songs unfound, Peru/Mexico thin, no newspaper "graça alcançada" ad specimen captured, 2004 Martyrologium check pending (archive.org lead in `01`).
