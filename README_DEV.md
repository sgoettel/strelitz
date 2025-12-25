# Entwicklung: neue Strelitz-Website

Dieses Repository enthält eine neue statische Site auf Basis von Eleventy (Quellordner `site/`, Ausgabe `dist/`). Die Daten im Ordner `friedhofsregister_der_juedischen_gemeinde_strelitz/` bleiben unverändert und werden direkt aus dem Viewer geladen.

## Voraussetzungen
- Node.js LTS
- Zugriff auf das npm-Registry (für `@11ty/eleventy` und `openseadragon`)

> Hinweis: Falls der Registry-Zugriff eingeschränkt ist, können die vorhandenen statischen HTML-Dateien in `site/` bzw. ein vorab gebautes `dist/` auch ohne Build-Schritt lokal ausgeliefert werden.

## Installation
```
npm install
```

## Development Server
```
npm run dev
```
- Startet Eleventy mit dem Input-Verzeichnis `site/` und schreibt nach `dist/`.
- Passthrough-Kopien sorgen dafür, dass `assets/`, `.nojekyll` und der vendored OpenSeadragon-Build bereitstehen.

## Produktion
```
npm run build
```
- Baut die statische Site nach `dist/`.
- Erstellt vor dem Build ein Scan-Manifest aus TEI + Dateisystem (harte Validierung) und führt einen Post-Build-Link-Audit aus.

## Scan-Manifest (pb → Datei)
- `scripts/build_scan_manifest.js` erzeugt `site/_data/scan-manifest.json` (ignored in Git).
- Mapping basiert auf der Reihenfolge der `<pb n="...">`-Marker in der TEI und der sortierten Bildliste im `jpg/`-Ordner.
- Fehlende Zuordnungen brechen den Build mit einem klaren Fehler ab.

## Lokaler Subpath-Test
```
ELEVENTY_PATH_PREFIX=/strelitz npm run build
```
- Prüft, ob Links, Pagefind Assets und OpenSeadragon-Icons unter `/strelitz/` korrekt sind.

## CI/Post-Build Checks
- `scripts/audit-dist-links.js` prüft `dist/` auf fehlende `href/src`-Ziele (inkl. `_pagefind`, OSD-Icons, Scan-Bilder).

## OpenSeadragon
- Der Viewer ist serverlos und lädt die Fullsize-JPGs direkt aus dem Datenordner.
- Die Bild-URLs kommen aus dem Manifest und sind pathPrefix-safe; fehlende Thumbnails werden ausgeblendet.
