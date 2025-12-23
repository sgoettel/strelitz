# AGENTS.md

## Project goal
Modernize the public site for the Strelitz Jewish cemetery register and add full-text search (genealogy-first UX).

## Hard constraints (SAFE / Phase 1)
- Do NOT move/rename/delete:
  `friedhofsregister_der_juedischen_gemeinde_strelitz/`
- Keep this URL stable:
  `friedhofsregister_der_juedischen_gemeinde_strelitz/mets.xml`
- Phase 1 is presentation/indexing only:
  do NOT “clean up” or semantically rewrite TEI/ALTO contents.

## Deliverables (Phase 1)
- New static site (no Jekyll) with:
  - search page (static full-text search)
  - entry pages (one per register entry)
  - primary scan viewing via OpenSeadragon (loads JPGs from the existing data folder)
  - DFG/METS viewer link is optional/legacy
- GitHub Actions deploy to `gh-pages` without touching the data folder.

## Preferred stack
- SSG: Eleventy
- Search: Pagefind
- TEI extraction: Python (lxml) or Node; keep it deterministic.

## Definition of Done
- Site builds locally and in CI.
- Search returns meaningful snippets.
- OpenSeadragon scan pages work.
- DFG/METS links still work (legacy).
- Data folder unchanged (verify by path-level diff).
