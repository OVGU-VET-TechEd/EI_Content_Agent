# Decisions

## Made at setup (2026-11-03)

| Decision | Choice | Why |
|---|---|---|
| Runtime | Claude Code project: `CLAUDE.md` + skills + hooks + a stdlib Python CLI | The agent must research the web, write files and keep a database consistent. A RAG chatbot (the NEXR_Agent pattern) cannot do that. NEXR's content-validation, eval and CI patterns were reused |
| Single source of truth | One CSV (`ei_literature.csv`) written only by `scripts/eidb.py` | Requested by the user; readable in Excel; one hook prevents direct edits |
| Where data lives | Nextcloud folder outside the repo (`ei.config.json`, gitignored) | Literature and the database may be sensitive; Nextcloud syncs and backs them up |
| Bibliographic data | APA and BibTeX from doi.org content negotiation (CSL `apa` style); manual formatting only without a DOI | Prevents invented or mistyped references |
| Zotero | Export `library.bib` / `library.ris` for import; no API write access | No credentials needed; the CSV stays the master |
| Backups | One timestamped copy per session (SessionStart hook) plus before restore | Requested; cheap; keeps every state recoverable |
| Wiki | Public markdown in the repo, Pandoc citation keys, minimal front matter, generated index | Versioned with git; renders on GitHub; can feed Pandoc papers later |
| Evidence labels | P/R/S/D/M from the earlier EI_Agent work | Keeps verification depth visible everywhere |
| Proposal skill | Funder-neutral outline + per-call private funder profile | User's instruction: replace the specific DFG Emmy Noether outline with a general one |
| Repository visibility | Public, OVGU-VET-TechEd | User's choice. Hence: no personal or career data in wiki, skills or commits |

## Open

| Decision | Default | If changed |
|---|---|---|
| Core unit of EI (decision record vs lifelong learner model) | Decision record with a learner-held computed view (recommendation) | Rewrite `concepts/` pages and the uniqueness argument |
| GitHub Pages for `docs/index.html` | Off | Enable Pages from `/docs` in the repo settings |
| Sentence-case conversion of APA titles | Not automated (registry capitalisation kept) | Add a converter with an acronym list |
| German-language wiki pages | English only | Add `lang:` to front matter and parallel pages |
