#!/usr/bin/env python3
"""build.py — the whole St. Expedite wiki, rendered to a static ./docs folder.

Stdlib only. No server, no framework, no build step beyond `python3 build.py`.
Deliberately a *simpler* generator than the Lanna manuscript-wiki: content lives
in plain Markdown files under content/, each carrying a small front-matter block
of facets; this script reads them, plus the harvested data assets (images, geo,
ngrams, trends), and emits a browsable site.

    python3 build.py            # writes ./docs, copies media
    python3 build.py --no-media # skip the 52 MB image copy (faster iterate)

Design notes for whoever maintains this next (see HANDOFF.md):
  • To add an article: drop a file in content/. Copy an existing one's header.
  • Facets are just comma lists in the header. Every value becomes a browsable
    node page automatically. Unknown values are fine — they make new nodes.
  • RELIABILITY is the load-bearing facet: every article declares where its
    authority comes from, so devotion, legend, and scholarship never blur.
"""
import argparse
import html
import json
import re
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONTENT = HERE / "content"
DOCS = HERE / "docs"
IMAGES = HERE / "images"
GEO = HERE / "geo"
DATA = HERE / "data"

# ---- facet axis metadata (label + one-line gloss shown on node pages) --------
AXES = {
    "reliability": ("Reliability", "Where a claim's authority comes from — the load-bearing axis."),
    "register": ("Register / lens", "Which world is speaking: scholarship, church, folk-magic, commerce."),
    "geography": ("Geography", "Where on earth the thread lives."),
    "patronage": ("Function / patronage", "What he is asked to do."),
    "type": ("Content type", "The page archetype."),
}
RELIABILITY_GLOSS = {
    "documented": "Verifiable in a primary or solid secondary record.",
    "scholarly-contested": "Real scholars actively disagree.",
    "legend": "Repeated as fact; treated as folk-etymology / apocryphal by scholarship.",
    "practitioner-consensus": "True as a description of what devotees and practitioners do.",
    "commercial-claim": "Evidence of what the trade sells and believes — not historical authority.",
}
RELIABILITY_ORDER = ["documented", "scholarly-contested", "legend",
                     "practitioner-consensus", "commercial-claim"]


# ---- tiny front-matter + markdown -------------------------------------------
def parse_doc(text):
    """Split a content file into (meta dict, body markdown)."""
    meta, body = {}, text
    if text.startswith("---"):
        _, fm, body = text.split("---", 2)
        key = None
        for line in fm.strip().splitlines():
            if line.startswith("- ") and key:            # list continuation
                meta.setdefault(key, [])
                meta[key].append(line[2:].strip())
            elif ":" in line:
                key, val = line.split(":", 1)
                key, val = key.strip(), val.strip()
                if val:
                    meta[key] = val
                else:
                    meta[key] = []                       # list follows
    # facet fields are comma lists
    for f in ("register", "geography", "patronage"):
        v = meta.get(f, "")
        if isinstance(v, str):
            meta[f] = [x.strip() for x in v.split(",") if x.strip()]
    return meta, body.strip()


_INLINE = [
    (re.compile(r"\*\*(.+?)\*\*"), r"<strong>\1</strong>"),
    (re.compile(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)"), r"<em>\1</em>"),
    (re.compile(r"\[(.+?)\]\((.+?)\)"), r'<a href="\2">\1</a>'),
]


def inline(s):
    s = html.escape(s)
    # un-escape our own markdown link brackets after escaping
    s = s.replace("&lt;", "&lt;")
    for pat, rep in _INLINE:
        s = pat.sub(rep, s)
    return s


def md(text):
    """Minimal Markdown → HTML: headings, paragraphs, lists, blockquote, hr, images."""
    out, buf, in_list = [], [], False

    def flush_p():
        if buf:
            out.append("<p>" + " ".join(buf) + "</p>")
            buf.clear()

    def flush_list():
        nonlocal in_list
        if in_list:
            out.append("</ul>")
            in_list = False

    for raw in text.splitlines():
        line = raw.rstrip()
        if not line.strip():
            flush_p(); flush_list(); continue
        if line.startswith("!["):                        # ![alt](file)
            m = re.match(r"!\[(.*?)\]\((.+?)\)", line)
            if m:
                flush_p(); flush_list()
                out.append(f'<figure><img loading="lazy" src="{m.group(2)}" '
                           f'alt="{html.escape(m.group(1))}"><figcaption>'
                           f'{inline(m.group(1))}</figcaption></figure>')
                continue
        if re.match(r"#{1,4}\s", line):
            flush_p(); flush_list()
            n = len(line) - len(line.lstrip("#"))
            out.append(f"<h{n+1}>{inline(line[n:].strip())}</h{n+1}>")
        elif line.startswith("> "):
            flush_p(); flush_list()
            out.append(f"<blockquote>{inline(line[2:])}</blockquote>")
        elif line.strip() in ("---", "***"):
            flush_p(); flush_list(); out.append("<hr>")
        elif line.startswith("- "):
            flush_p()
            if not in_list:
                out.append("<ul>"); in_list = True
            out.append(f"<li>{inline(line[2:])}</li>")
        else:
            flush_list(); buf.append(inline(line))
    flush_p(); flush_list()
    return "\n".join(out)


# ---- page shell --------------------------------------------------------------
CSS = """
:root{--ink:#241c15;--paper:#f7f2e9;--card:#fffdf8;--rule:#d8cdb8;--red:#a3241c;
--muted:#6a5f4d;--link:#8a2b12;--accent:#7c5a1e}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);
font:1.19rem/1.62 Georgia,'Iowan Old Style',serif;-webkit-text-size-adjust:100%}
a{color:var(--link)}a:hover{color:var(--red)}
header.site{background:var(--red);color:#fbeee0;padding:.7rem 1rem;position:sticky;top:0;z-index:5;
box-shadow:0 2px 0 #6d1712}
header.site a{color:#fbeee0;text-decoration:none}
header.site .brand{font-weight:bold;font-size:1.25rem;letter-spacing:.02em}
header.site nav{margin-top:.25rem;font-size:1.02rem;display:flex;flex-wrap:wrap;gap:.2rem 1.1rem}
main{max-width:52rem;margin:0 auto;padding:1.4rem 1.1rem 4rem}
.wide{max-width:66rem}
h1{font-size:2.05rem;line-height:1.15;margin:.2em 0 .35em}
h2{font-size:1.5rem;margin:1.6em 0 .3em;border-bottom:2px solid var(--rule);padding-bottom:.15em}
h3{font-size:1.2rem;margin:1.3em 0 .2em;color:var(--accent)}
img{max-width:100%;height:auto;border-radius:5px}
figure{margin:1.2em 0}figure img{border:1px solid var(--rule)}
figcaption{font-size:.92rem;color:var(--muted);margin-top:.3em;font-style:italic}
blockquote{margin:1em 0;padding:.4em 1em;border-left:4px solid var(--red);background:var(--card);
color:#3d3226}
hr{border:0;border-top:1px solid var(--rule);margin:1.6em 0}
.lead{font-size:1.26rem;color:#3d3226}
.chips{display:flex;flex-wrap:wrap;gap:.4rem;margin:.6rem 0 1rem}
.chip{display:inline-block;padding:.16em .6em;border-radius:1em;font-size:.86rem;
background:var(--card);border:1px solid var(--rule);color:#4a3f2e;text-decoration:none}
.chip:hover{border-color:var(--red)}
.rel{font-weight:bold;border-width:2px}
.rel.documented{border-color:#2e6b3a;color:#2e6b3a}
.rel.scholarly-contested{border-color:#8a6d1e;color:#8a6d1e}
.rel.legend{border-color:#8a2b8a;color:#8a2b8a}
.rel.practitioner-consensus{border-color:#1e5f8a;color:#1e5f8a}
.rel.commercial-claim{border-color:#8a4a1e;color:#8a4a1e}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(15rem,1fr));gap:1rem;margin:1.2rem 0}
.card{background:var(--card);border:1px solid var(--rule);border-radius:7px;overflow:hidden;
display:flex;flex-direction:column}
.card a{text-decoration:none;color:inherit;display:block;height:100%}
.card .body{padding:.6rem .8rem}
.card h3{margin:.1em 0 .2em;color:var(--red)}
.card p{margin:.2em 0;font-size:.97rem;color:#4a3f2e}
.gal{columns:3 13rem;column-gap:.7rem}.gal figure{break-inside:avoid;margin:0 0 .7rem}
.gal img{width:100%}
.sources{font-size:.96rem;background:var(--card);border:1px solid var(--rule);border-radius:6px;
padding:.5rem 1rem}
.note{background:#fdf6e6;border:1px solid #e6d9b8;border-radius:6px;padding:.7rem 1rem;margin:1.2em 0}
#map{height:74vh;min-height:28rem;border:1px solid var(--rule);border-radius:6px}
.legend b{display:inline-block;width:.8em;height:.8em;border-radius:50%;margin-right:.3em;vertical-align:middle}
table{border-collapse:collapse;width:100%;font-size:.98rem}
td,th{border:1px solid var(--rule);padding:.35em .6em;text-align:left}
.footer{color:var(--muted);font-size:.9rem;margin-top:3rem;border-top:1px solid var(--rule);padding-top:1rem}
svg.chart{background:var(--card);border:1px solid var(--rule);border-radius:6px;max-width:100%}
"""

NAV = [
    ("Home", "index.html"),
    ("Articles", "articles.html"),
    ("Map", "map.html"),
    ("The data", "data.html"),
    ("Gallery", "gallery.html"),
    ("How we know", "methods.html"),
]


def page(title, body, wide=False, head_extra="", active=""):
    nav = " ".join(
        f'<a href="{href}"{" style=text-decoration:underline" if lbl==active else ""}>{lbl}</a>'
        for lbl, href in NAV)
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} · St. Expedite Wiki</title>
<style>{CSS}</style>{head_extra}</head><body>
<header class="site"><a href="index.html" class="brand">✠ Saint Expedite</a>
<nav>{nav}</nav></header>
<main class="{'wide' if wide else ''}">{body}
<div class="footer">An open, provenance-transparent wiki on the global cult of Saint Expedite —
a companion corpus to the Lanna manuscript &amp; Lazada amulet collections.
Every claim is tagged by <a href="reliability.html">reliability</a>; sources are cited per page.
Images are CC/PD (<a href="gallery.html">credits</a>). Built by <code>build.py</code>.</div>
</main></body></html>"""


def chip(axis, val, extra=""):
    cls = "chip"
    if axis == "reliability":
        cls += f" rel {val}"
    return f'<a class="{cls}" href="node-{axis}-{slugify(val)}.html">{html.escape(val)}</a>'


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


# ---- ngram SVG charts --------------------------------------------------------
def ngram_series():
    d = json.loads((DATA / "ngrams.json").read_text())
    return {s["ngram"]: s for s in d["series"] if s.get("timeseries")}


def line_chart(series_list, y0, y1, title, sub, colors):
    """series_list: [(label, timeseries, [year_start,year_end])]; each normalized to own max."""
    W, H, pad = 760, 300, 44
    x = lambda yr: pad + (yr - y0) / (y1 - y0) * (W - pad - 10)
    y = lambda v: H - pad - v * (H - pad - 24)
    parts = [f'<svg class="chart" viewBox="0 0 {W} {H}" role="img" aria-label="{html.escape(title)}">']
    parts.append(f'<text x="{pad}" y="18" font-size="15" font-weight="bold" fill="#241c15">{html.escape(title)}</text>')
    parts.append(f'<text x="{pad}" y="34" font-size="11" fill="#6a5f4d">{html.escape(sub)}</text>')
    # axes + decade ticks
    parts.append(f'<line x1="{pad}" y1="{H-pad}" x2="{W-10}" y2="{H-pad}" stroke="#d8cdb8"/>')
    for yr in range(y0, y1 + 1, 20):
        parts.append(f'<line x1="{x(yr):.0f}" y1="{H-pad}" x2="{x(yr):.0f}" y2="{H-pad+4}" stroke="#b7ab93"/>')
        parts.append(f'<text x="{x(yr):.0f}" y="{H-pad+18}" font-size="11" fill="#6a5f4d" text-anchor="middle">{yr}</text>')
    for i, (label, ts, yrs) in enumerate(series_list):
        ys0 = yrs[0]
        mx = max(ts) or 1
        pts = []
        for idx, v in enumerate(ts):
            yr = ys0 + idx
            if y0 <= yr <= y1:
                pts.append(f"{x(yr):.1f},{y(v/mx):.1f}")
        col = colors[i % len(colors)]
        parts.append(f'<polyline fill="none" stroke="{col}" stroke-width="2.2" points="{" ".join(pts)}"/>')
        parts.append(f'<text x="{W-10}" y="{22+i*17}" font-size="12" fill="{col}" text-anchor="end">{html.escape(label)}</text>')
    parts.append("</svg>")
    return "".join(parts)


def build_data_page():
    S = ngram_series()
    reds = ["#a3241c", "#8a6d1e", "#1e5f8a", "#2e6b3a", "#8a2b8a", "#c0561e"]
    body = ["<h1>The data — measuring a saint</h1>",
            '<p class="lead">“Expedite” is also an ordinary English verb, so you cannot '
            "measure the saint by counting the word. Here is how we work around that — "
            "and what the numbers reveal.</p>",
            '<div class="note"><strong>The polysemy problem, shown not hidden.</strong> '
            "We never query the bare verb. Instead we count <em>saint-specific surface forms</em> "
            "in each language (“Saint Expedite”, “Sant’Espedito”, “San Expedito”…), and we normalise "
            "each curve to its own peak so shapes are comparable across corpora. Google Books has "
            "<strong>no Portuguese corpus</strong>, so Brazil — the largest devotion on earth — is "
            "invisible in book data. That gap is a tooling limit, not an absence of devotion.</div>"]

    # Chart A — the 1905 wave across languages
    langs = [("St. Expeditus (EN)", "St. Expeditus"), ("Saint Expédit (FR)", "Saint Expédit"),
             ("Sant'Espedito (IT)", "Sant'Espedito"), ("San Expedito (ES)", "San Expedito"),
             ("Expeditus (DE)", "Expeditus")]
    seriesA = [(lbl, S[k]["timeseries"], S[k]["years"]) for lbl, k in langs if k in S]
    body.append("<h2>One synchronised wave, five languages: the 1905 shock</h2>")
    body.append("<p>Book-mentions of the saint peak in a tight band around 1900–1911 across five "
                "independent national corpora — Spanish 1904, French 1905, Italian 1906, English 1909, "
                "German 1911. That is the signature of the <a href='controversy.html'>Pius X intervention</a> "
                "and the publicity storm around it. The Vatican’s attempt to suppress the cult is exactly "
                "what put it in the world’s books.</p>")
    body.append(line_chart(seriesA, 1850, 2000, "Saint-Expedite mentions by language",
                           "each curve normalised to its own maximum · Google Books Ngrams", reds))

    # Chart B — two waves in English
    en = [("Saint Expedite", "Saint Expedite"), ("St. Expeditus", "St. Expeditus")]
    seriesB = [(lbl, S[k]["timeseries"], S[k]["years"]) for lbl, k in en if k in S]
    body.append("<h2>Two waves, two spellings</h2>")
    body.append("<p>The older Latinate spelling “St. Expeditus” crests around 1909 (the church-history "
                "moment). The vernacular “Saint Expedite” — the spelling of the New Orleans hoodoo revival — "
                "barely exists until the late 20th century and peaks around <strong>2011</strong>. The name "
                "you use dates which wave you belong to.</p>")
    body.append(line_chart(seriesB, 1880, 2019, "English spellings over time",
                           "normalised · the modern curve is the folk-magic revival", reds))

    # Trends section
    body.append("<h2>Google Trends — the living pulse</h2>")
    trends = sorted((DATA / "trends").glob("*.csv"))
    if trends:
        body.append(f"<p>{len(trends)} exported Trends series in <code>data/trends/</code>:</p><ul>")
        for t in trends:
            body.append(f"<li><code>{t.name}</code></li>")
        body.append("</ul><p>(Rendering of these is wired for whoever adds the charts — the CSVs are here.)</p>")
    else:
        body.append('<div class="note">No Trends CSVs exported yet. The disambiguation-safe export '
                    "recipe lives in <code>tools/TRENDS.md</code> — a 10-minute manual pull. The prize to "
                    "watch for: a <strong>monthly sawtooth on the 19th</strong> in Brazil’s daily “Santo "
                    "Expedito” series, which would confirm the <em>dia-19</em> devotion from a completely "
                    "independent data source.</div>")
    (DOCS / "data.html").write_text(page("The data", "\n".join(body), wide=True, active="The data"))


# ---- map page ----------------------------------------------------------------
def build_map_page():
    shrines = json.loads((GEO / "shrines.geojson").read_text())
    curated = json.loads((GEO / "curated_sites.json").read_text())
    csites = curated if isinstance(curated, list) else curated.get("sites", list(curated.values()) if isinstance(curated, dict) else [])
    if isinstance(curated, dict) and "sites" not in curated:
        # dict keyed? our file is a dict-of-lists? we saw a list of dicts under? handle both
        csites = curated if isinstance(curated, list) else list(curated.values())
    # our file: top-level dict with list? we saw count 15 as dict -> values are site dicts
    if isinstance(curated, dict):
        vals = list(curated.values())
        if vals and isinstance(vals[0], dict) and "lat" in vals[0]:
            csites = vals
    (DOCS / "data").mkdir(exist_ok=True)
    (DOCS / "data" / "shrines.geojson").write_text(json.dumps(shrines))
    (DOCS / "data" / "curated_sites.json").write_text(json.dumps(csites))
    n = len(shrines["features"])
    head = ('<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>'
            '<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>')
    body = f"""<h1>Where he lives — {n} mapped shrines</h1>
<p class="lead">Every point is an <strong>OpenStreetMap feature whose name actually contains the
saint</strong> (177 kept, filtered from ~2,700 raw hits). Big amber pins are the
15 canonical sites we verified by hand.</p>
<p class="legend"><b style="background:#a3241c"></b> named OSM shrine &nbsp;
<b style="background:#e0a020"></b> curated canonical site</p>
<div id="map"></div>
<div class="note"><strong>What the map proves — and what it hides.</strong> The living parish
devotion clusters hard in <strong>Brazil (118) and Argentina (40)</strong>. But
<strong>Réunion shows only 7</strong> named points despite its ~340 real red shrines: the world’s
densest Expédit landscape is <em>unmapped by name</em> in OSM (a dedicated island sweep found 398
religious features, nearly all unnamed). Zero-count places aren’t absent either — New Orleans’s
shrine is titled “Our Lady of Guadalupe,” so it lives only in the curated layer. The map is a
floor, not a census. See <a href="reunion.html">Réunion</a>.</div>
<script>
var m=L.map('map').setView([-15,-30],3);
L.tileLayer('https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png',
 {{maxZoom:18,attribution:'© OpenStreetMap contributors (ODbL)'}}).addTo(m);
fetch('data/shrines.geojson').then(r=>r.json()).then(g=>{{
 L.geoJSON(g,{{pointToLayer:(f,ll)=>L.circleMarker(ll,{{radius:5,color:'#a3241c',
  fillColor:'#a3241c',fillOpacity:.7,weight:1}}).bindPopup(
  '<b>'+(f.properties.name||'(unnamed)')+'</b><br>'+(f.properties.kind||'')+
  '<br>'+(f.properties.country||''))}}).addTo(m);}});
fetch('data/curated_sites.json').then(r=>r.json()).then(s=>{{
 s.forEach(c=>{{if(c.lat)L.circleMarker([c.lat,c.lon],{{radius:9,color:'#7a5600',
  fillColor:'#e0a020',fillOpacity:.9,weight:2}}).bindPopup(
  '<b>'+c.name+'</b><br>'+(c.city||'')+'<br><i>'+(c.role||'')+'</i>').addTo(m);}});}});
</script>"""
    (DOCS / "map.html").write_text(page("Map", body, wide=True, head_extra=head, active="Map"))


# ---- gallery -----------------------------------------------------------------
def build_gallery(copy_media=True):
    man = json.loads((IMAGES / "manifest.json").read_text())
    items = man if isinstance(man, list) else list(man.values())[0]
    local = [x for x in items if x.get("local_path")]
    (DOCS / "media").mkdir(exist_ok=True)
    figs, attrib = [], ["# Image credits\n",
                        "All images below are Public Domain or Creative Commons, harvested from "
                        "Wikimedia Commons. One line per file.\n"]
    for x in sorted(local, key=lambda a: a.get("local_path")):
        src = HERE / x["local_path"]
        name = Path(x["local_path"]).name
        if copy_media and src.exists():
            shutil.copy2(src, DOCS / "media" / name)
        desc = (x.get("description") or "").replace("\n", " ")[:110]
        cap = f'{desc} <em>({html.escape(x.get("license","?"))})</em>'
        figs.append(f'<figure><img loading="lazy" src="media/{name}" alt="{html.escape(desc)}">'
                    f'<figcaption>{cap}</figcaption></figure>')
        attrib.append(f"- **{name}** — {desc} · {x.get('artist','?')} · "
                      f"{x.get('license','?')} · {x.get('commons_page_url','')}")
    (IMAGES / "ATTRIBUTION.md").write_text("\n".join(attrib))
    body = (f"<h1>Gallery — {len(local)} images</h1>"
            '<p class="lead">Harvested from Wikimedia Commons, all Public Domain or Creative Commons. '
            "Réunion roadside oratories, Brazilian and Argentine parishes, the vanished Austro-German "
            "cult surviving only in prints, and the HODIE-cross / CRAS-crow holy cards that carry the "
            "whole iconographic pun.</p>"
            f'<div class="gal">{"".join(figs)}</div>')
    (DOCS / "gallery.html").write_text(page("Gallery", body, wide=True, active="Gallery"))
    return {Path(x["local_path"]).name for x in local}


# ---- articles + facet nodes --------------------------------------------------
def build_articles(media_names):
    docs = []
    for f in sorted(CONTENT.glob("*.md")):
        meta, body = parse_doc(f.read_text())
        meta["slug"] = meta.get("slug", f.stem)
        meta["_body"] = body
        docs.append(meta)

    # render each article
    for m in docs:
        chips = []
        if m.get("reliability"):
            chips.append(chip("reliability", m["reliability"]))
        for axis in ("register", "geography", "patronage", "type"):
            for v in (m.get(axis) if isinstance(m.get(axis), list) else [m.get(axis)] if m.get(axis) else []):
                chips.append(chip(axis, v))
        hero = ""
        if m.get("hero") and m["hero"] in media_names:
            hero = f'<figure><img src="media/{m["hero"]}" alt="{html.escape(m.get("title",""))}"></figure>'
        src = ""
        if m.get("sources"):
            lis = []
            for s in m["sources"]:
                if "|" in s:
                    t, u = s.rsplit("|", 1)
                    lis.append(f'<li><a href="{u.strip()}">{html.escape(t.strip())}</a></li>')
                else:
                    lis.append(f"<li>{html.escape(s)}</li>")
            src = f'<h2>Sources</h2><div class="sources"><ul>{"".join(lis)}</ul></div>'
        rel_note = ""
        if m.get("reliability") in RELIABILITY_GLOSS:
            rel_note = (f'<div class="note"><strong>Reliability: {m["reliability"]}.</strong> '
                        f'{RELIABILITY_GLOSS[m["reliability"]]}</div>')
        body = (f"<h1>{html.escape(m.get('title','Untitled'))}</h1>"
                f'<div class="chips">{"".join(chips)}</div>'
                + (f'<p class="lead">{inline(m["summary"])}</p>' if m.get("summary") else "")
                + hero + rel_note + md(m["_body"]) + src)
        (DOCS / f"{m['slug']}.html").write_text(page(m.get("title", "Article"), body, active=""))

    # articles index
    cards = []
    for m in sorted(docs, key=lambda d: d.get("title", "")):
        thumb = f'<img loading="lazy" src="media/{m["hero"]}" alt="">' if m.get("hero") in media_names else ""
        rel = f'<span class="chip rel {m["reliability"]}">{m["reliability"]}</span>' if m.get("reliability") else ""
        cards.append(f'<div class="card"><a href="{m["slug"]}.html">{thumb}<div class="body">'
                     f'<h3>{html.escape(m.get("title",""))}</h3>'
                     f'<p>{html.escape((m.get("summary") or "")[:120])}</p>{rel}</div></a></div>')
    body = ("<h1>Articles</h1><p class='lead'>The wiki, one page per thread. Each is tagged where its "
            "authority comes from.</p>" + f'<div class="grid">{"".join(cards)}</div>')
    (DOCS / "articles.html").write_text(page("Articles", body, wide=True, active="Articles"))

    # facet node pages
    index = {}  # (axis,val) -> [meta]
    for m in docs:
        pairs = [("reliability", m["reliability"])] if m.get("reliability") else []
        pairs += [("type", m["type"])] if m.get("type") else []
        for axis in ("register", "geography", "patronage"):
            pairs += [(axis, v) for v in (m.get(axis) or [])]
        for axis, val in pairs:
            index.setdefault((axis, val), []).append(m)
    for (axis, val), arts in index.items():
        lis = "".join(f'<li><a href="{a["slug"]}.html">{html.escape(a.get("title",""))}</a> '
                      f'— {html.escape((a.get("summary") or "")[:90])}</li>' for a in arts)
        gloss = RELIABILITY_GLOSS.get(val, "") if axis == "reliability" else AXES[axis][1]
        body = (f'<p><a href="reliability.html">← all facets</a></p>'
                f'<h1>{AXES[axis][0]}: <span style="color:var(--red)">{html.escape(val)}</span></h1>'
                f'<p class="lead">{html.escape(gloss)}</p><ul>{lis}</ul>')
        (DOCS / f"node-{axis}-{slugify(val)}.html").write_text(page(f"{val}", body, active=""))
    return docs, index


def build_reliability_hub(index):
    body = ["<h1>Reliability — the load-bearing facet</h1>",
            '<p class="lead">St. Expedite is one saint refracted through worlds that disagree about '
            "what is even true. Rather than sort threads into “real” and “fake,” every claim declares "
            "<em>where its authority comes from</em>. This is the same move the Lanna corpus makes: "
            "the seam is provenance, not structure.</p>"]
    for rel in RELIABILITY_ORDER:
        arts = index.get(("reliability", rel), [])
        body.append(f'<h2><span class="chip rel {rel}">{rel}</span></h2>')
        body.append(f"<p>{RELIABILITY_GLOSS[rel]}</p>")
        if arts:
            body.append("<ul>" + "".join(
                f'<li><a href="{a["slug"]}.html">{html.escape(a.get("title",""))}</a></li>'
                for a in arts) + "</ul>")
        else:
            body.append("<p><em>(no articles yet)</em></p>")
    # other axes
    body.append("<h2>Other ways in</h2>")
    for axis in ("geography", "register", "patronage", "type"):
        vals = sorted({v for (ax, v) in index if ax == axis})
        chips = " ".join(chip(axis, v) for v in vals)
        body.append(f"<p><strong>{AXES[axis][0]}:</strong> {chips}</p>")
    (DOCS / "reliability.html").write_text(page("Reliability", "\n".join(body), active=""))


def build_home(docs):
    feat = {d["slug"]: d for d in docs}
    order = ["overview", "iconography", "new-orleans", "reunion", "brazil-latam",
             "the-crate-legend", "controversy", "prayers-rituals"]
    cards = []
    for slug in order:
        m = feat.get(slug)
        if not m:
            continue
        thumb = f'<img loading="lazy" src="media/{m["hero"]}" alt="">' if m.get("hero") else ""
        cards.append(f'<div class="card"><a href="{m["slug"]}.html">{thumb}<div class="body">'
                     f'<h3>{html.escape(m.get("title",""))}</h3>'
                     f'<p>{html.escape((m.get("summary") or "")[:130])}</p></div></a></div>')
    body = f"""<h1>Saint Expedite</h1>
<p class="lead">The saint of urgent causes — “the one who never delays.” A doubtful name in an
ancient martyr-list who became, improbably, a global folk hero: patron of merchants and students
in Europe, of 70,000-strong feast-day crowds in Buenos Aires, of red roadside shrines across
Réunion, and of pound-cake offerings in New Orleans. One saint; many worlds that barely agree he
was real.</p>
<p>This is an open, provenance-transparent wiki. Every page is tagged by
<a href="reliability.html">where its claims come from</a> — church history, living devotion, folk
legend, or the candle trade — so the record stays honest about a subject where honesty is hard.</p>
<div class="grid">{"".join(cards)}</div>
<h2>Three ways to explore</h2>
<ul>
<li><a href="map.html"><strong>The map</strong></a> — 177 shrines, and the story of the 340 that
aren’t on it.</li>
<li><a href="data.html"><strong>The data</strong></a> — how you measure a saint whose name is also
a verb, and the 1905 wave that shows up in five languages at once.</li>
<li><a href="methods.html"><strong>How we know</strong></a> — the sources, the gaps, and what we
deliberately refused to assert.</li>
</ul>"""
    (DOCS / "index.html").write_text(page("Saint Expedite", body, wide=True, active="Home"))


def build_methods():
    body = """<h1>How we know — sources, gaps, and refusals</h1>
<p class="lead">A wiki about a contested saint has to show its work. Here is the evidentiary spine,
what we could not source, and the claims we actively refused to print as fact.</p>
<h2>The evidentiary spine</h2>
<ul>
<li><strong>Scholarly:</strong> Mathew Kuefler, “The Convertible Saint,” <em>Journal of Religious
History</em> 42.1 (2018); Presses universitaires de Rennes on the Réunion cult; Hippolyte Delehaye
(Bollandists) on the name.</li>
<li><strong>Folklife:</strong> the Louisiana Folklife Program essay; the AIRR / Lucky Mojo
practitioner corpus (reliable <em>as</em> practice, not doctrine).</li>
<li><strong>Material:</strong> 107 Commons images, 177 OSM-mapped shrines, and Google Books Ngram
frequency across five language corpora.</li>
</ul>
<h2>What we refused to assert</h2>
<p>Our verification pass actively killed these popular “facts.” They are <em>not</em> in the wiki as
truth:</p>
<ul>
<li>That he commanded the <em>Legio XII Fulminata</em> — devotional embellishment; no evidence.</li>
<li>Latin-American crowds “in the hundreds of thousands” — the verified ceiling is ~70,000/day
(Buenos Aires, 19 April 2026).</li>
<li>That Réunion’s red comes from the saint’s military cloak — the supported reading is the sacred
red of Tamil/Kali practice.</li>
<li>Any single clean date for a “Vatican removal.” No primary 1905 decree survives; the old Roman
Martyrology <em>kept</em> the entry afterward, so it was an images/devotions action, and he was
never on the General Roman Calendar to begin with.</li>
</ul>
<h2>Known gaps (open invitations)</h2>
<ul>
<li>Réunion’s ~340 shrines are unmapped by name — the map shows 7.</li>
<li>No Portuguese Ngram corpus, so Brazil is invisible in the book data.</li>
<li>Historic US newspaper thank-you notices: the Library of Congress full-text API returned 403 to
our harvester; the search hits are logged in <code>pd-texts/</code> awaiting a gentler fetch.</li>
<li>Peru and Mexico devotion remains thinly sourced; German parish (vs. print) coverage is thin.</li>
</ul>
<div class="note">This page is the honest floor of the project. The underlying research digests
(fully URL-cited, reliability-tagged) live in <code>background/</code>; the verified claim ledger is
<code>research-raw.json</code>. Nothing here is meant to be the last word — only a well-sourced
first one.</div>"""
    (DOCS / "methods.html").write_text(page("How we know", body, active="How we know"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-media", action="store_true", help="skip copying the 52 MB image set")
    args = ap.parse_args()
    if DOCS.exists():
        shutil.rmtree(DOCS)
    DOCS.mkdir()
    media_names = build_gallery(copy_media=not args.no_media)
    docs, index = build_articles(media_names)
    build_reliability_hub(index)
    build_map_page()
    build_data_page()
    build_methods()
    build_home(docs)
    print(f"Built {len(docs)} articles + {len(index)} facet nodes → {DOCS}")
    print("Open:", DOCS / "index.html")


if __name__ == "__main__":
    main()
