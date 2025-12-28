## Friedhofsregister der jüdischen Gemeinde zu Strelitz (1740–1923)

Das Datenset steht unter der [Lizenz CC BY-SA 4](https://creativecommons.org/licenses/by-sa/4.0/deed.de).

Neue statische Website mit OpenSeadragon-Viewer und stabilen Datenpfaden:
- https://sgoettel.github.io/strelitz/
- Scan-URL-Schema: `/scan/<pb>/`
- Auflösung von `pb` zu Scans erfolgt **build-time** über `site/_data/scan-manifest.json` (generiert durch `scripts/build_scan_manifest.js`).
- Es werden **keine arithmetischen Regeln** zur Zuordnung von `pb` zu Dateinamen verwendet.
- Legacy DFG-Viewer bleibt über die METS erreichbar.

Kontakt, Fragen, Anregungen: sebastian.goettel at bbaw de

## Lokale Entwicklung

Für die Build-Skripte werden Python-Abhängigkeiten benötigt:

```sh
python3 -m pip install -r requirements.txt
```

<img src="https://i.imgur.com/gxswSPg.jpg" alt="Inneres der Strelitzer Synagoge" width="400"/>

Inneres der Synagoge in Strelitz: *Georg, Kurt: Kunst- und Geschichts-Denkmäler des Freistaates Mecklenburg-Strelitz.
I Band: Das Land Stargard. Neubrandenburg: Brünslowsche Verlagsbuchhandlung 1921, S. 131*.
