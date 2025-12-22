# Modernization Plan

## Ziel-UX
- **Suche → Treffer → Eintrag → Scan**: Nutzer starten mit einer Volltextsuche über alle Registereinträge. Ergebnisse zeigen Name, Jahr(e) und einen kurzen TEI/ALTO-Snippet. Jeder Treffer öffnet eine dedizierte Eintragsseite.
- **Eintragsseite**: Zeigt strukturierte Felder (Nummer, Personenname, Datumsangaben, Originaltext) und verlinkt den zugehörigen Scan in einem eingebetteten OpenSeadragon-Viewer. Ein Legacy-Link zum DFG-Viewer bleibt verfügbar.
- **Scan-Navigation**: OpenSeadragon lädt die bestehenden Fullsize-JPGs direkt aus `friedhofsregister_der_juedischen_gemeinde_strelitz/jpg/`. Thumbnails werden weiterhin aus `jpg/thumbs/` verwendet, wo sinnvoll (z. B. Ergebnisseite oder Seitenleiste).

## Architektur
- **Daten bleiben unverändert**: TEI, ALTO, METS, JPGs und Thumbnails verbleiben exakt im Verzeichnis `friedhofsregister_der_juedischen_gemeinde_strelitz/`.
- **Statischer Site-Build**: Jekyll wird abgelöst. Die neue statische Site wird mit Eleventy erzeugt; Volltextsuche über Pagefind. Build-Skripte parsen TEI/ALTO deterministisch (Python + lxml oder Node) und generieren JSON/Markdown für Eleventy.
- **Asset-Pfade**: Fullsize-Scans folgen `friedhofsregister_der_juedischen_gemeinde_strelitz/jpg/altstrelitz_friedregister{page}.jpg` (beginnend bei 2); Thumbs liegen als `jpg/thumbs/altstrelitz_friedregister_thumbs_{page}.jpg` (plus ein offensichtlicher Ausreißer `..._thumbs__thumbs_2.jpg`).
- **Seiten-IDs**: TEI-Seiten sind durch `<pb n="…" xml:id="img_XXXX">` nummeriert (1–96). Die Bildpfad-Regel lautet: `image_number = pb@n + 1` → `altstrelitz_friedregister{image_number}.jpg`.

## TEI/Indexing-Strategie
- **Eintragsstruktur**: Einträge stehen als `<item xml:id="…">` innerhalb eines `<list rend="numbered">`. Die Eintragsnummer steckt im `<label>`-Element (z. B. "No 1", "7.").
- **Seitenbezug**: `<pb>`-Marken erscheinen im Lesefluss; alle nachfolgenden `<item>`-Elemente gehören zur zuletzt gesehenen `<pb>` bis zur nächsten Seitenmarke. Der `xml:id` von `<pb>` liefert eine stabile Page-Referenz, `@n` liefert die zählbare Seitenzahl.
- **Page→Image-Mapping**: Für jede `<pb n>` wird `n + 1` mit dem JPEG-Suffix verknüpft. Beispiel: `<pb n="1">` → `altstrelitz_friedregister2.jpg`; `<pb n="2">` → `altstrelitz_friedregister3.jpg`. Thumbnails nutzen denselben Offset (`altstrelitz_friedregister_thumbs_3.jpg` usw.).
- **Index-Output**: Parser erzeugt pro `<item>` eine strukturierte JSON-Repräsentation (id, label/nummer, normalisierte Personennamen, Rohtext), ergänzt um `pageNumber` (aus `<pb n>`), `imageFile` (berechneter JPG-Pfad) und optional `thumbFile`.

## Migration-Schritte
1. **Code-Basis säubern**: Jekyll-Konfiguration und Layout-Dateien entfernen; Build/Deploy auf Eleventy + Pagefind umstellen. Data-Verzeichnis unverändert übernehmen.
2. **Extractor schreiben**: TEI-parser implementieren, der Eintrags-JSON und Seiten-Metadaten erzeugt (inkl. Page→Image-Mapping und Legacy-DFG-Link über `mets.xml`).
3. **Eleventy-Templates**: Suchseite, Trefferliste, Eintragsseiten und OpenSeadragon-Komponente erstellen. Assets aus `assets/` übernehmen oder ersetzen.
4. **Suche integrieren**: Pagefind im Build laufen lassen, Index aus den generierten Eintragsseiten erzeugen; Snippets aus TEI/ALTO (ohne inhaltliche Veränderung).
5. **Deploy-Pipeline**: GitHub Actions anpassen, damit Eleventy + Pagefind nach `gh-pages` deployen und das Datenverzeichnis unverändert ausliefern.
6. **Smoke-Tests**: Prüfen, dass Beispiel-Einträge korrekt auf den zugehörigen Scan linken und OSD lädt; DFG-Viewer-Link weiterhin erreichbar.

## Risiken und Mitigations
- **URL-Stabilität**: Bestehende Daten-URLs (insb. `friedhofsregister_der_juedischen_gemeinde_strelitz/mets.xml` und JPG-Pfade) dürfen nicht verändert werden. Mitigation: Deploy-Skript lässt das Datenverzeichnis unangetastet und serviert neue Site parallel.
- **Offset-Fehler beim Mapping**: Da die METS-Sequenz bei JPG 2 beginnt, ist das `+1`-Offset kritisch. Mitigation: Unit-Test für Parser, der `<pb n="1">` → `altstrelitz_friedregister2.jpg` validiert.
- **Pagefind-Größe**: Volltextindex könnte groß werden. Mitigation: nur relevante Felder indizieren, Assets und Bilder nicht in den Index aufnehmen.
- **Legacy-Link-Risiko**: DFG-Viewer bleibt als Link erhalten; falls extern offline, degradiert nur optionaler Pfad.

## Definition of Done
- Eleventy-Site baut lokal/CI und deployt nach `gh-pages`.
- Pagefind liefert Treffer mit sinnvollen Snippets aus TEI/ALTO.
- Jede Eintragsseite bindet OpenSeadragon mit dem korrekten JPG und optionalem Thumbnail ein; Seitensprünge funktionieren (nächste/vorherige Seite).
- Datenverzeichnis bleibt bit-identisch; `mets.xml` und bestehende URLs bleiben erreichbar.
- Legacy-DFG-Viewer-Link ist vorhanden, aber nicht primär.
