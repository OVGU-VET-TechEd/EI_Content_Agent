# EI_Content_Agent

A [Claude Code](https://claude.com/claude-code) agent that helps develop **Education Informatics (Bildungsinformatik)** as a discipline. It writes papers, gathers and verifies material, discusses ideas, and acts as a domain expert. Every valid piece of knowledge it finds is recorded in a structured way:

- **one literature database** (CSV, private): every source with APA, BibTeX, a short summary, an evidence-status label and its relevance to the six criteria of disciplinarity;
- **one public wiki** (`wiki/`): concepts, approaches, methods, propositions and the field-level argument, all citable back to the database;
- **skills** (`.claude/skills/`) that hold *how* the agent works and the judgements it has learned, so later papers and proposals follow the field's development.

**Intro page:** [`docs/index.html`](docs/index.html) (structure, commands, workflow).
**Anchor paper:** Tegelbeckers, H., & Bünning, F. (2026). Education Informatics as a discipline for equitable, evidence-informed and sovereign digital education systems: A critical conceptual review. *Information, 17*(9), 827. https://doi.org/10.3390/info17090827

## How it works

```
"I heard about learner portfolios from the UK"
        │
        ▼  ei-ingest (default for anything new)
 research ─► local PDFs/notes → Crossref/DOI → web search → read abstracts/full texts
        │
        ▼
 record   ─► scripts/eidb.py add --doi …   (APA + BibTeX from doi.org, summary, status P/R/S/D/M,
        │                                    criteria C1–C6, role, topics)   → private CSV
        ▼
 structure ► wiki/approaches/… (characteristics grid) + propagate to rival fields,
        │    criteria board, uniqueness argument, open questions, log
        ▼
 learn    ─► ei-learn: lasting judgements go into the skills
        │
        ▼
 check    ─► eidb.py sync · wiki-index · validate (0 errors) · export (.bib/.ris for Zotero)
```

Hooks make it robust. At the start of every session the CSV is backed up and a status line is loaded into context. Direct edits of the CSV are blocked, so only `eidb.py` writes it.

## Setup

Requirements: Python ≥ 3.10 (standard library only), Claude Code, internet access for DOI lookups.

```bash
git clone https://github.com/OVGU-VET-TechEd/EI_Content_Agent.git && cd EI_Content_Agent
cp ei.config.example.json ei.config.json        # set data_dir and literature_dirs (absolute paths)
python3 scripts/eidb.py init                    # creates <data_dir>/ei_literature.csv, backups/, exports/, drafts/
claude                                          # start the agent in this folder
```

If `data_dir` lies outside the repo, allow Claude Code to work there via `.claude/settings.local.json`:

```json
{ "permissions": { "additionalDirectories": ["/absolute/path/to/your/EI folder"] } }
```

Import into Zotero: *File → Import…* → `<data_dir>/exports/library.ris` (or `library.bib`). Run `python3 scripts/eidb.py export` to refresh.

## Commands (skills)

Type them as slash commands, or just talk: the agent routes plain messages ("I heard about …") to `ei-ingest`.

| Command | Use it to |
|---|---|
| `/ei-ingest <topic or source>` | Research a topic, record sources, update the wiki and skills (the main loop) |
| `/ei-add-paper <DOI, title, PDF, URL>` | Record a single reference |
| `/ei-discuss <idea>` | Think an idea through with an expert sparring partner |
| `/ei-proposition-stress-test` | For-and-against verdicts on a set of ideas or notes |
| `/ei-uniqueness-argument` | Build or test the "EI is distinct" argument against rival fields |
| `/ei-write <text type and topic>` | Draft paper sections or abstracts grounded in the knowledge base |
| `/ei-proposal <topic / funder>` | Funder-neutral proposal outline, mapped to any call's review criteria |
| `/ei-source-and-legal-check` | Check citations, evidence status, AI Act lines and AI disclosure |
| `/ei-wiki <page>` | Create, restructure or fix wiki pages |
| `/ei-status` | What the knowledge base holds, what is thin, what is next |
| `/ei-learn` | Fold lasting lessons into the skills |

## Database CLI

```bash
python3 scripts/eidb.py search "Kane 2013 validating interpretations"
python3 scripts/eidb.py add --doi 10.1111/jedm.12000 --summary "…" --topics "validity" \
    --criteria methods --role method --status S --query "argument-based validity"
python3 scripts/eidb.py list --criterion methods | --status DM | --text portfolio
python3 scripts/eidb.py update ID --status P --append-note "read in full"
python3 scripts/eidb.py rename OLD NEW          # citekey changed everywhere, incl. wiki
python3 scripts/eidb.py sync && python3 scripts/eidb.py wiki-index && python3 scripts/eidb.py validate
python3 scripts/eidb.py export                  # library.bib, library.ris, references_apa.md
python3 scripts/eidb.py backup | restore FILE
```

**Columns:** `id, type, authors, year, title, venue, volume, issue, pages, doi, url, apa, bibtex, summary, topics, ei_criteria, ei_role, wiki_pages, source_status, verified_via, local_file, added_on, added_by_query, notes`. Extra columns you add by hand are preserved.

**Evidence status:** P (read in full) · R (cited in the anchor paper, not re-read) · S (DOI record/abstract) · D (from notes/slides) · M (memory, unconfirmed).

## Repository layout

```
CLAUDE.md                 agent persona, routing, standing rules, core knowledge
.claude/skills/           11 skills (see table above)
.claude/settings.json     hooks (session backup, CSV guard) and permissions
scripts/eidb.py           database CLI (stdlib only)
scripts/hooks/            session_start.py, guard_data.py
wiki/                     public knowledge of the field (index: wiki/README.md)
templates/                wiki page types, proposal outline, funder profile, paper outline
eval/                     behaviour scenarios and rating rubric
tests/                    offline unit tests (python3 -m unittest discover -s tests)
docs/                     intro page (index.html), decisions
```

## What is *not* in this repository

The CSV database, its backups, exports, drafts, literature PDFs, notes and `ei.config.json` are excluded by `.gitignore`, and CI fails if such files are ever tracked. The wiki is public. It must not contain personal or career details or reproduce unpublished third-party material.

## Origin

Built on 2026-11-03 from the earlier *EI_Agent* skills (uniqueness argument, proposition stress test, source and legal check; the DFG-specific proposal mapper was replaced by the funder-neutral `ei-proposal`). Repository conventions (validated content, eval rubric, CI, citation file) were adapted from [nexr-hcd-coach](https://github.com/OVGU-VET-TechEd/nexr-hcd-coach).

## Licence

Code: MIT (`LICENSE`). Content (wiki, skills, templates, docs): CC BY 4.0 (`LICENSE-CONTENT.md`). Please cite via `CITATION.cff`.
