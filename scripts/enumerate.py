#!/usr/bin/env python3
"""Enumerate Saint Expeditus imagery on Wikimedia Commons -> images/manifest.json"""
import json, re, time, urllib.parse, urllib.request, collections, html, sys, os

API = "https://commons.wikimedia.org/w/api.php"
UA = {"User-Agent": "st-expedite-wiki/1.0 (skunkhaus@gmail.com; harvesting PD/CC imagery)"}
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def api(params):
    params = dict(params, format="json")
    url = API + "?" + urllib.parse.urlencode(params)
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except Exception as e:
            print("retry", attempt, e, file=sys.stderr)
            time.sleep(2 * (attempt + 1))
    raise RuntimeError("API failed: " + url)

# ---- 1. BFS category tree ----
roots = ["Category:Saint Expeditus", "Category:Expeditus"]
seen_cats, queue = set(), list(roots)
file_cats = collections.defaultdict(set)   # file title -> set of categories it was found in
all_cats = []
while queue:
    cat = queue.pop(0)
    if cat in seen_cats:
        continue
    seen_cats.add(cat)
    all_cats.append(cat)
    cont = {}
    while True:
        d = api({"action": "query", "list": "categorymembers", "cmtitle": cat,
                 "cmlimit": "500", "cmtype": "file|subcat", **cont})
        for m in d["query"]["categorymembers"]:
            t = m["title"]
            if t.startswith("Category:"):
                if t not in seen_cats:
                    queue.append(t)
            else:
                file_cats[t].add(cat.replace("Category:", ""))
        if "continue" in d:
            cont = {k: v for k, v in d["continue"].items() if k != "continue"}
        else:
            break
    time.sleep(0.3)

print(f"categories crawled: {len(all_cats)}", file=sys.stderr)
print(f"files from categories: {len(file_cats)}", file=sys.stderr)

# ---- also: full-text search in File namespace ----
searches = ['Expeditus', '"saint expedit"', '"santo expedito"', '"san expedito"',
            '"saint expédit"', '"sant\'espedito"', '"são expedito"']
search_found = set()
for s in searches:
    cont = {}
    while True:
        d = api({"action": "query", "list": "search", "srsearch": s,
                 "srnamespace": "6", "srlimit": "200", **cont})
        for r in d["query"]["search"]:
            search_found.add(r["title"])
        if "continue" in d and len(search_found) < 3000:
            cont = {k: v for k, v in d["continue"].items() if k != "continue"}
        else:
            break
    time.sleep(0.3)
print(f"files from search: {len(search_found)}", file=sys.stderr)

all_files = sorted(set(file_cats) | search_found)
print(f"total unique files: {len(all_files)}", file=sys.stderr)

# ---- 2. imageinfo + categories in batches of 50 ----
info = {}
def norm(v):
    if isinstance(v, dict):
        v = v.get("value", "")
    v = re.sub(r"<[^>]+>", " ", str(v))
    return html.unescape(re.sub(r"\s+", " ", v)).strip()

def fetch_batch(batch, width=True):
    cont = {}
    while True:
        params = {"action": "query", "titles": "|".join(batch),
                  "prop": "imageinfo|categories", "iiprop": "url|extmetadata",
                  "cllimit": "max", **cont}
        if width:
            params["iiurlwidth"] = "1280"
        d = api(params)
        if "query" not in d:
            if len(batch) > 1:
                mid = len(batch) // 2
                fetch_batch(batch[:mid], width)
                fetch_batch(batch[mid:], width)
            elif width:
                fetch_batch(batch, width=False)
            else:
                print("skipping unfetchable:", batch[0], file=sys.stderr)
            return
        for p in d["query"]["pages"].values():
            t = p.get("title")
            if not t:
                continue
            e = info.setdefault(t, {"cats": set()})
            if "imageinfo" in p and "ii" not in e:
                ii = p["imageinfo"][0]
                em = ii.get("extmetadata", {})
                e["ii"] = {
                    "direct_url": ii.get("url"),
                    "thumb_url": ii.get("thumburl"),
                    "license": norm(em.get("LicenseShortName", "")),
                    "artist": norm(em.get("Artist", "")),
                    "date": norm(em.get("DateTimeOriginal", "")),
                    "description": norm(em.get("ImageDescription", ""))[:500],
                    "credit": norm(em.get("Credit", ""))[:200],
                }
            for c in p.get("categories", []):
                e["cats"].add(c["title"].replace("Category:", ""))
        if "continue" in d:
            cont = {k: v for k, v in d["continue"].items() if k != "continue"}
        else:
            return

for i in range(0, len(all_files), 50):
    fetch_batch(all_files[i:i+50])
    print(f"metadata {min(i+50,len(all_files))}/{len(all_files)}", file=sys.stderr)
    time.sleep(0.3)

# ---- guesses ----
def guess_region(t, cats, desc):
    blob = " ".join([t, desc] + list(cats)).lower()
    rules = [
        ("reunion", ["réunion", "reunion", "sainte-suzanne", "la possession",
                     "le tampon", "cilaos", "salazie", "saint-leu", "hell-bourg",
                     "sainte-marie", "saint-denis", "piton"]),
        ("new-orleans", ["new orleans", "louisiana", "our lady of guadalupe chapel"]),
        ("brazil", ["brazil", "brasil", "são paulo", "sao paulo", "mogi", "paróquia",
                    "paroquia", "igreja", "santo expedito"]),
        ("argentina", ["argentina", "buenos aires", "misiones", "bermejo", "balvanera",
                       "puerto leoni", "san expedito"]),
        ("italy", ["italy", "italia", "acireale", "palermo", "sicily", "sicilia",
                   "espedito", "napoli", "naples", "bellona", "melito"]),
        ("germany", ["germany", "austria", "graz", "wien", "vienna", "münchen",
                     "leoben", "steiermark", "deutschland", "kirche"]),
        ("philippines", ["philippines", "filipino", "manila", "cebu"]),
        ("france", ["france", "paris", "toulouse", "église", "eglise", "cathédrale",
                    "creuse", "eure", "rhône", "aude", "yvelines", "cher", "isère",
                    "charente", "alpes-maritimes", "seine-maritime", "loire-atlantique",
                    "ille-et-vilaine", "maine-et-loire", "bouches-du-rhône",
                    "indre-et-loire", "lyon", "marseille", "bordeaux", "nantes", "rouen"]),
    ]
    for region, kws in rules:
        for kw in kws:
            if kw in blob:
                return region
    return "other"

def guess_subject(t, cats, desc):
    blob = " ".join([t, desc] + list(cats)).lower()
    if any(k in blob for k in ["oratoire", "oratory", "oratorio", "shrine", "roadside"]):
        return "shrine"
    if any(k in blob for k in ["holy card", "prayer card", "estampa", "santino",
                               "image pieuse", "engraving", "gravure", "lithograph",
                               "postcard", "print"]):
        return "holy-card"
    if any(k in blob for k in ["painting", "peinture", "fresco", "mural", "retable",
                               "altarpiece", "dipinto", "stained glass", "vitrail"]):
        return "painting"
    if any(k in blob for k in ["altar", "autel"]):
        return "altar"
    if any(k in blob for k in ["statue", "statua", "escultura", "sculpture", "imagen",
                               "bust", "figure"]):
        return "statue"
    if any(k in blob for k in ["church", "église", "eglise", "igreja", "iglesia",
                               "chapel", "chapelle", "capilla", "kirche", "paróquia",
                               "paroquia", "parish", "cathedral", "basilica"]):
        return "church"
    return "other"

manifest = []
for t in all_files:
    e = info.get(t, {})
    ii = e.get("ii")
    if not ii:
        continue
    cats = sorted(e.get("cats", set()) | file_cats.get(t, set()))
    fn = t.replace("File:", "")
    manifest.append({
        "filename": fn,
        "commons_page_url": "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(t.replace(" ", "_")),
        "direct_url": ii["direct_url"],
        "thumb_url": ii["thumb_url"],
        "license": ii["license"],
        "artist": ii["artist"],
        "date": ii["date"],
        "description": ii["description"],
        "credit": ii["credit"],
        "categories": cats,
        "in_expeditus_tree": t in file_cats,
        "region_guess": guess_region(fn, cats, ii["description"]),
        "subject_guess": guess_subject(fn, cats, ii["description"]),
    })

os.makedirs(os.path.join(ROOT, "images"), exist_ok=True)
with open(os.path.join(ROOT, "images", "manifest.json"), "w") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=1)
print(f"manifest entries: {len(manifest)}", file=sys.stderr)
