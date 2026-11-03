# Changelog

## 0.1.0 — 2026-11-03

- First release of EI_Content_Agent.
- `scripts/eidb.py`: single-CSV literature database (DOI-based APA and BibTeX via doi.org content negotiation, Crossref search, validation, wiki cross-check, `.bib`/`.ris` export for Zotero, per-session backups, citekey renaming).
- Hooks: SessionStart backup + status; PreToolUse guard against direct CSV edits.
- 11 skills: `ei-ingest`, `ei-add-paper`, `ei-wiki`, `ei-discuss`, `ei-write`, `ei-proposal`, `ei-status`, `ei-learn`, plus `ei-uniqueness-argument`, `ei-proposition-stress-test`, `ei-source-and-legal-check` carried over from EI_Agent (the DFG-specific proposal mapper replaced by the funder-neutral `ei-proposal`).
- Wiki seeded with 15 content pages; private database seeded with 65 references.
- Offline unit tests (20) and CI.
