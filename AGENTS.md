# AGENTS.md

## Project goal
Provide a durable, genealogy-first static website for the Strelitz Jewish cemetery register:
fast search, stable entry pages, and reliable scan viewing (OpenSeadragon) — without changing the underlying data or breaking URLs.

## Non-negotiable invariants (do not break)
- Do NOT move/rename/delete the data folder:
  `friedhofsregister_der_juedischen_gemeinde_strelitz/`
- Do NOT modify the TEI source file (taboo; read-only):
  `friedhofsregister_der_juedischen_gemeinde_strelitz/TEI/jacobson_strelitzfriedhofsregister_1929.txt.xml`
- Keep this URL stable and the file unchanged:
  `friedhofsregister_der_juedischen_gemeinde_strelitz/mets.xml`
- No semantic “cleanups” of TEI/ALTO content:
  parsing/extraction + presentation/indexing only.

## Build output is read-only
- Do NOT edit `dist/` (build output). Only change source files under `site/`, `scripts/`, `assets/`, or config.

## Public URL stability
These routes must remain valid:
- `/entry/<id>/`
- `/scan/<pb>/`
- `/search/`
Also keep existing data URLs stable under:
- `/friedhofsregister_der_juedischen_gemeinde_strelitz/...`

## Runtime environment constraints (GitHub Pages)
- The site is served under the subpath `/strelitz/` (pathPrefix matters everywhere).
- GitHub Pages has **no directory listing**:
  never link to folder URLs like `/.../jpg/` or `/.../alto/` unless you generate an `index.html` for them.
- All asset/data URLs must be pathPrefix-safe:
  use Eleventy’s `url` filter (or an equivalent, single-source base URL mechanism) consistently.

## Stack (current)
- SSG: Eleventy
- Search: Pagefind (output in `dist/_pagefind`)
- Scan viewer: OpenSeadragon
- TEI extraction: deterministic, build-time (Python lxml or Node)

## Must-have engineering rules
### 1) pb@n → scan filename mapping
- Do NOT rely on arithmetic rules (e.g. `pb + 1`) in templates or runtime JS.
- Generate a build-time manifest from the filesystem + TEI `<pb n="...">`:
  `pb -> { image, thumb? }`.
- If any `<pb>` cannot be resolved to a scan image: **fail the build** (exit != 0) with a clear error message.

### 2) OpenSeadragon must work on GitHub Pages subpath
- Initialize the viewer from a template-provided, already pathPrefix-safe image URL (e.g. via `data-image-url`).
- Ensure the OSD control icon prefix is pathPrefix-safe and published.
- On failure: show a visible error in the viewer and log the actual URL + error.

### 3) Pagefind must be content-scoped and pathPrefix-safe
- Ensure the search query is passed to Pagefind unchanged.
- Scope indexing to the real content area:
  use `data-pagefind-body` / `data-pagefind-ignore` (or equivalent) to avoid nav/footer boilerplate polluting results.
- Pagefind assets must load under `/strelitz/` (pathPrefix-safe).

### 4) Transcription rendering must be safe and deterministic
- Render TEI-derived transcription as HTML only if it is produced by a whitelist-based serializer (DOM-based),
  not by regex/string concatenation.
- Only map a controlled subset of TEI tags for display (e.g. `lb`, `label`, `fw`, `persName`, `date`,
  `placeName`, `ref`, `unclear`, `foreign`, `del`). Everything else must degrade gracefully to plain text/spans.

### 5) CI should catch broken links/assets
- Add/keep a post-build audit that checks `dist/` references (href/src) against existing files:
  fail CI on missing assets (including `_pagefind`, OSD icons, manifest-resolved images).

## Deliverables (stabilization scope)
- Working scan pages (`/scan/<pb>/`) with OpenSeadragon viewer.
- Working search (`/search/`) with plausible results for common names (e.g. “Meyer”).
- Entry pages (`/entry/<id>/`) with human-readable rendering (no “raw HTML dump” look).
- Downloads/data page without dead directory links; use file lists, GitHub browse links, or archive assets.
- GitHub Actions deploys to `gh-pages` deterministically without modifying the data folder.

## Definition of Done (acceptance checks)
- Build succeeds locally and in CI.
- Data folder unchanged (verify by path-level diff).
- Several `/scan/<pb>/` pages load images + zoom; no TileSource error.
- `/search/` loads Pagefind assets under subpath and returns plausible matches for “Meyer”.
- At least one `e####` entry and one `i-#` entry render cleanly (readable transcription + extracted fields).
- No “directory” links on downloads/data pages that 404 on GitHub Pages.
