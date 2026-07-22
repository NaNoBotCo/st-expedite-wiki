#!/usr/bin/env python3
"""Curate ~60-100 free-license images from manifest.json, download 1280px thumbs,
update manifest with local_path, write ATTRIBUTION.md."""
import json, os, re, sys, time, unicodedata, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "images")
OUT = os.path.join(IMG, "commons")
os.makedirs(OUT, exist_ok=True)
UA = {"User-Agent": "st-expedite-wiki/1.0 (skunkhaus@gmail.com; downloading curated free images)"}

manifest = json.load(open(os.path.join(IMG, "manifest.json")))
by_name = {e["filename"]: e for e in manifest}

OK_LICENSE = re.compile(r"^(Public domain|CC0|CC BY(-SA)? \d\.\d.*|No restrictions)$", re.I)

# Curated picks: exact filenames or unique substrings, with a short slug.
PICKS = [
    # --- Réunion red roadside shrines (the star) ---
    ("Bord de Mars oratory 01.jpg", "reunion-bord-de-mars-oratory-1"),
    ("Bord de Mars oratory 02.jpg", "reunion-bord-de-mars-oratory-2"),
    ("Chapelle Sainte-Rita de Pont suspendu Saint Expeditus worship.jpg", "reunion-chapelle-sainte-rita-pont-suspendu"),
    ("Chapelle St Expédit au Serré - panoramio.jpg", "reunion-chapelle-au-serre"),
    ("Chapelle de l'Amitié de La Nouvelle Saint Expeditus.jpg", "reunion-chapelle-amitie-la-nouvelle"),
    ("Intérieur chapelle - panoramio.jpg", "reunion-chapelle-interieur"),
    ("La Réunion Ravine St Expedit.JPG", "reunion-ravine-st-expedit"),
    ("Oratory @ Route forestière de la Roche Merveilleuse 01.jpg", "reunion-oratory-roche-merveilleuse-1"),
    ("Oratory @ Route forestière de la Roche Merveilleuse 03.jpg", "reunion-oratory-roche-merveilleuse-3"),
    ("Oratory @ Sentier Charles Payet.jpg", "reunion-oratory-sentier-charles-payet"),
    ("Oratory @ Sentier des Porteurs 01.jpg", "reunion-oratory-sentier-porteurs-1"),
    ("Oratory @ Sentier des Porteurs 03.jpg", "reunion-oratory-sentier-porteurs-3"),
    ("Oratory RD 242 @ Cilaos 01.jpg", "reunion-oratory-cilaos-rd242-1"),
    ("Oratory RD 242 @ Cilaos 02.jpg", "reunion-oratory-cilaos-rd242-2"),
    ("Oratory col du Taïbit 01.jpg", "reunion-oratory-col-taibit-1"),
    ("Oratory col du Taïbit 04.jpg", "reunion-oratory-col-taibit-4"),
    ("Oratory col du Taïbit 06.jpg", "reunion-oratory-col-taibit-6"),
    ("Saint Expédit Petit Serré dsc03553.jpg", "reunion-petit-serre-altar-1"),
    ("Saint Expédit Petit Serré dsc03555.jpg", "reunion-petit-serre-altar-2"),
    ("Saint Expédit route des plaines dsc02353.jpg", "reunion-route-des-plaines-altar"),
    ("Spring @ Sentier des Porteurs.jpg", "reunion-spring-sentier-porteurs"),
    # --- New Orleans ---
    ("GuadalupeNOLAExpedite.jpg", "new-orleans-guadalupe-chapel-statue"),
    # --- Argentina & Chile ---
    ("Día de San Expedito - Buenos Aires - 01.jpg", "argentina-dia-san-expedito-ba-1"),
    ("Día de San Expedito - Buenos Aires - 04.jpg", "argentina-dia-san-expedito-ba-4"),
    ("Día de San Expedito - Buenos Aires - 06.jpg", "argentina-dia-san-expedito-ba-6"),
    ("Día de San Expedito - Buenos Aires - 09.jpg", "argentina-dia-san-expedito-ba-9"),
    ("Día de San Expedito - Buenos Aires - 13.jpg", "argentina-dia-san-expedito-ba-13"),
    ("Santuario de San Expedito, Bermejo, San Juan, Argentina.jpg", "argentina-santuario-bermejo"),
    ("Estatua de San Expedito en su santuario de Bermejo, San Juan.jpg", "argentina-estatua-bermejo"),
    ("Huesos de San Expedito-2009.jpg", "argentina-relics-huesos"),
    ("Huesos de San Expedito (Detalle)-2009.jpg", "argentina-relics-huesos-detail"),
    ("Puerto Leoni (Provincia de Misiones, Argentina) - Oratorio San Expedito.jpg", "argentina-puerto-leoni-oratorio"),
    ("Puerto Leoni (Provincia de Misiones, Argentina) - Entrada al Oratorio San Expedito.jpg", "argentina-puerto-leoni-entrada"),
    ("Ermita San Expedito en los Saltos del Tabay (Jardín América, Misiones, Argentina).jpg", "argentina-ermita-saltos-tabay"),
    ("Oratorio San Expedito en Iglesia Cristo Redentor", "argentina-oratorio-jardin-america"),
    ("San Expedito..jpg", "argentina-san-expedito-statue"),
    ("Altar San Expedito, Basílica de la Merced, Santiago 20240503 17.jpg", "chile-altar-merced-santiago"),
    ("Estatua San Expedito, Iglesia de Santo Domingo, Santiago 20240503 10.jpg", "chile-estatua-santo-domingo-santiago"),
    ("Estatua de San Expedito, Vitacura, Santiago 20251104.jpg", "chile-estatua-vitacura"),
    ("Puerto Natales, animitas 3.jpg", "chile-puerto-natales-animitas"),
    # --- Brazil ---
    ("Nave da Paróquia Santo Expedito - Mogi Guaçu, Brasil.jpg", "brazil-mogi-guacu-nave"),
    ("Presbitério da Paróquia Santo Expedito - Mogi Guaçu, Brasil.jpg", "brazil-mogi-guacu-presbiterio"),
    ("Santo Expedito - Mogi Guaçu.jpg", "brazil-mogi-guacu-statue"),
    ("Capela Santo Expedito, Pau dos Ferros (RN).jpg", "brazil-capela-pau-dos-ferros"),
    ("Capela de Santo Expedito, José da Penha (RN).JPG", "brazil-capela-jose-da-penha"),
    ("Paróquia Santo Expedito - Goiânia.jpg", "brazil-paroquia-goiania"),
    ("Paróquia Santo Expedito, Cunha-SP, Brazil 2018 029.jpg", "brazil-paroquia-cunha"),
    ("Fachada da Capela Santo Expedito de Dom Lara, Caratinga MG.JPG", "brazil-capela-dom-lara-caratinga"),
    ("Igreja Santo Expedito 01.jpg", "brazil-igreja-santo-expedito-1"),
    ("Igreja Santo Expedito 10.jpg", "brazil-igreja-santo-expedito-10"),
    ("Ceilandia DF Brasil - Igreja de Santo Expedito - panoramio.jpg", "brazil-ceilandia-igreja"),
    ("Santuário de Santo Expedito.jpg", "brazil-santuario"),
    ("Dia de Romaria - Monumento de Santo Expedito", "brazil-dia-de-romaria-monumento"),
    ("Zambelli santo expedito.jpg", "brazil-zambelli-statue"),
    ("Memo-expedito.jpg", "brazil-memo-expedito-statue"),
    ("Igreja São José em Porto Alegre 14.jpg", "brazil-porto-alegre-sao-jose-statue"),
    ("Padroeiro de Tijuaçu, santo Expedito.jpg", "brazil-tijuacu-padroeiro"),
    # --- Portugal ---
    ("Saint Expedito- Igreja de Sao Nicolau Lisbonne.jpg", "portugal-lisbon-sao-nicolau-statue"),
    ("Saint Expeditus na Igreja da Conceição Velha - Lisbon.JPG", "portugal-lisbon-conceicao-velha-statue"),
    # --- Italy & Switzerland ---
    ("San Expedito circa 1781.jpg", "italy-acireale-painting-1781"),
    ("Saint Expeditus. Oil painting by a painter of Palermo Wellcome L0076176.jpg", "italy-palermo-painting-ten-scenes"),
    ("Saint Expeditus. Oil painting by a painter of Palermo, 19th Wellcome L0027951.jpg", "italy-palermo-painting-19c"),
    ("Cuneo, Chiesa di San Sebastiano, interno, statua di Sant'Espedito.jpg", "italy-cuneo-san-sebastiano-statue"),
    ("Pinerolo, San Rocco 004.JPG", "italy-pinerolo-san-rocco-statue"),
    ("Lugano 056.JPG", "switzerland-lugano-san-carlo-statue"),
    ("Sankt Expeditus by Peter Demetz Urtijëi.jpg", "italy-urtijei-demetz-carving"),
    # --- Austria / Central Europe ---
    ("S. Expeditus.jpg", "austria-graz-oil-painting-18c"),
    ("ContentServer-2.jpg", "austria-graz-jungwierth-engraving-1790"),
    ("St. Expeditus lithograph.jpg", "austria-graz-lithograph-19c"),
    ("Saint Expeditus by Jan Jahn.jpg", "czech-jahn-engraving-1766"),
    ("Brno michal expeditus, Scherz.jpg", "czech-brno-scherz-statue-1773"),
    ("Jindřichův-Hradec-sloup-Nejsvětější-Trojice2013j.jpg", "czech-jindrichuv-hradec-column"),
    ("The statue of St. Expeditus.jpg", "poland-warsaw-holy-saviour-statue"),
    # --- Holy cards, prints, medals, devotional paintings ---
    ("Sant'Espedito Martire.jpg", "holycard-1897-milan-chromolithograph"),
    ("Devotieprent van de heilige Expeditus van Melitene, asset M1BSMKRSIi7X896Emj2e7EJj.tif", "holycard-devotieprent-1"),
    ("Devotieprent van de heilige Expeditus van Melitene, asset NegYfDUZFVaJ6VcJk46ddXtA.tif", "holycard-devotieprent-2"),
    ("Devotieprent van de heilige Expeditus van Melitene, asset r2VKThUmddtdL5VyXDgOi1ae.tif", "holycard-devotieprent-3"),
    ("Devotieprent van de heilige Expeditus van Melitene, asset u2YKSphJoaQlGl6XPZMioijI.tif", "holycard-devotieprent-4"),
    ("Medaille met H. Expeditus en opschrift 'St. Expédit priez pour nous', asset o2fPRTMaRQcoTRGagTk", "medal-st-expedit-1"),
    ("Medaille met H. Expeditus en opschrift 'St. Expédit priez pour nous', asset oiRWVaKbUSFHUXJNH3D", "medal-st-expedit-2"),
    ("Saint Expiditus. Engraving by J.P. Wurzer. Wellcome V0033295.jpg", "print-wurzer-engraving"),
    ("Oil painting of St.Expeditus Wellcome L0024780.jpg", "painting-wellcome-l0024780"),
    ("Scenes from St.Expeditus life and martyrdom Wellcome L0024776.jpg", "painting-life-scenes-l0024776"),
    ("St.Expeditus; scenes from his life and martyrdom Wellcome L0024775.jpg", "painting-life-scenes-l0024775"),
    ("St.Expeditus; scenes from his life and martyrdom Wellcome L0024777.jpg", "painting-life-scenes-l0024777"),
    ("Saint Expedit.jpg", "france-private-devotion-image"),
    ("Spedito-ipod.JPG", "modern-icon-on-ipod"),
    # --- France ---
    ("Cancale - Eglise Saint-Méen - Statue de Saint-Expédit.jpg", "france-cancale-statue"),
    ("Honfleur - Eglise Sainte-Catherine - Statue de Saint Expédit.jpg", "france-honfleur-statue"),
    ("Cathédrale Saint-Maurice de Vienne - Statue Saint Expédit (août 2020).jpg", "france-vienne-cathedral-statue"),
    ("Église Sainte-Rita de Paris 13.jpg", "france-paris-sainte-rita-statue"),
    ("Saint Expedit - ND de la Seds - Toulon.jpg", "france-toulon-nd-seds-statue"),
    ("Statue de saint Expédit, Basilique Notre Dame de Bonne Nouvelle, Rennes, France.jpg", "france-rennes-basilica-statue"),
    ("Saint-Expedit , Eglise saint-François , Nîmes.jpg", "france-nimes-statue"),
    ("Église Saint-Vigor de Marly-le-Roi saint expedit.JPG", "france-marly-le-roi-statue"),
    ("Le Mans - cathédrale Saint-Julien, intérieur 016.jpg", "france-le-mans-cathedral-statue"),
    ("Gaillac - Église Saint-Pierre 02.jpg", "france-gaillac-statue"),
    ("Chapelle Saint Expedit Saint Pierre d arene de Nice.jpg", "france-nice-chapelle"),
    ("Rue Saint-Expédit (Toulouse).jpg", "france-toulouse-rue-saint-expedit"),
    ("Thiberville (Eure, Fr) église Saint Taurin, statue Saint Expedit.JPG", "france-thiberville-statue"),
    ("Abbaye Saint-Michel de Frigolet (TARASCON,FR13) statues.jpg", "france-frigolet-abbey-statues"),
    # --- Spain ---
    ("Sevilla - Convento del Santo Ángel, San Expédito.jpg", "spain-sevilla-convento-statue"),
    ("Oviedo - Iglesia de Santa María la Real de la Corte (ex Monasterio de San Vicente) 33", "spain-oviedo-statue"),
    ("Sant Expedito a l'església Nuestra Señora del Carmen de Còrdova.jpg", "spain-cordoba-carmen-statue"),
    ("Ondarroa ermita de San Expedito.jpg", "spain-ondarroa-ermita"),
    # --- Elsewhere ---
    ("0126jfSanta Maria Goretti Parish Church Manilafvf 06.jpg", "philippines-manila-goretti-statue"),
    ("Igl. de la Veracruz - San Expedito - Medellin.jpg", "colombia-medellin-veracruz"),
]

def resolve(pat):
    if pat in by_name:
        return by_name[pat]
    hits = [e for e in manifest if pat in e["filename"]]
    if len(hits) == 1:
        return hits[0]
    if len(hits) > 1:
        hits.sort(key=lambda e: len(e["filename"]))
        return hits[0]
    return None

downloaded, skipped_license, missing = [], [], []
n = 0
for pat, slug in PICKS:
    e = resolve(pat)
    if e is None:
        missing.append(pat)
        continue
    if not OK_LICENSE.match(e["license"]):
        skipped_license.append((e["filename"], e["license"]))
        continue
    n += 1
    url = e["thumb_url"] or e["direct_url"]
    ext = os.path.splitext(url.split("/")[-1])[1].lower().lstrip(".")
    if not ext or len(ext) > 5:
        ext = "jpg"
    local = f"{n:03d}-{slug}.{ext}"
    dest = os.path.join(OUT, local)
    if not os.path.exists(dest):
        req = urllib.request.Request(url, headers=UA)
        try:
            with urllib.request.urlopen(req, timeout=120) as r, open(dest, "wb") as f:
                f.write(r.read())
        except Exception as ex:
            print("DOWNLOAD FAILED:", e["filename"], ex, file=sys.stderr)
            n -= 1
            continue
        time.sleep(0.4)
    e["local_path"] = "images/commons/" + local
    downloaded.append(e)
    print(f"{local}  <- {e['filename'][:70]}  [{e['license']}]")

# rewrite manifest with local_path fields
with open(os.path.join(IMG, "manifest.json"), "w") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=1)

# ---- ATTRIBUTION.md ----
lines = ["# Image Attribution",
         "",
         "All images below were sourced from Wikimedia Commons. Licenses are as recorded",
         "on each file's Commons page at harvest time (2026-07-13). CC BY / CC BY-SA",
         "require this attribution to be retained.",
         ""]
for e in sorted(downloaded, key=lambda x: x["local_path"]):
    artist = e["artist"] or "Unknown"
    artist = re.sub(r"\s+", " ", artist)[:120]
    lines.append(f"- `{os.path.basename(e['local_path'])}` — \"{e['filename']}\" — {artist} — {e['license']} — {e['commons_page_url']}")
with open(os.path.join(IMG, "ATTRIBUTION.md"), "w") as f:
    f.write("\n".join(lines) + "\n")

print(f"\ndownloaded: {len(downloaded)}", file=sys.stderr)
if skipped_license:
    print("skipped (license):", *[f"  {a} [{b}]" for a, b in skipped_license], sep="\n", file=sys.stderr)
if missing:
    print("NOT FOUND:", *missing, sep="\n  ", file=sys.stderr)
