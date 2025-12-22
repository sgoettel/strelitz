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
- Das Facsimile unter `/scan/<pb>/` lädt automatisch `imageNumber = pb + 1` aus `friedhofsregister_der_juedischen_gemeinde_strelitz/jpg/`.

## OpenSeadragon
- Der Viewer ist serverlos und lädt die Fullsize-JPGs direkt aus dem Datenordner.
- Thumbnails werden unter `/friedhofsregister_der_juedischen_gemeinde_strelitz/jpg/thumbs/altstrelitz_friedregister_thumbs_<imageNumber>.jpg` erwartet und ausgeblendet, falls nicht vorhanden.
