---
name: ei-write
description: Draft academic text for Education Informatics grounded in the knowledge base — paper sections, abstracts, literature reviews, position statements, responses to reviewers. Use when the user asks to write, draft, outline, rewrite or shorten a text about EI or a related topic.
argument-hint: <text type and topic, e.g. "intro section on data-based approaches">
---

# Write from the knowledge base

## 1. Brief

Settle these from the request or context. Ask only for what you cannot infer:

- **Type and venue:** journal article (which journal or style), conference paper, abstract, chapter, position paper, reviewer response.
- **Argument:** the one claim the text must carry, and which of the six criteria it serves.
- **Length and language.**

## 2. Gather

- Read the relevant wiki pages; they hold the current argument and its limits.
- Pull the sources: `python3 scripts/eidb.py list --topic <t>` / `--criterion <c>` / `--text "<words>"`, then `show <id>` for details.
- **Gaps:** if the argument needs a source the database lacks, run `ei-ingest` or `ei-add-paper` first. Never cite from memory.
- Check statuses. A claim that rests on **D** or **M** sources must not carry weight; flag it or verify first.

## 3. Outline before prose

Use `templates/paper_outline.md` for articles. Give the user a short outline (headings plus one line each) for anything longer than about 1,000 words, and wait for agreement if the structure is not obvious.

## 4. Draft

- **Claims calibrated to evidence.** Use the anchor paper's three-way distinction: what evidence shows, what is plausible but untested, and what is a design commitment.
- **Citations:** Pandoc keys `[@key]` in the draft. The user can render with `library.bib` from `<data_dir>/exports/` (`pandoc --citeproc --bibliography library.bib --csl apa.csl`). For Word output, also give an APA reference list from `references_apa.md`.
- **Own work vs others':** mark the user's own prior work as such.
- **No analogy as warrant:** Business-Informatics parity and market demand are context, not arguments (see `ei-uniqueness-argument`).
- **Plain, precise academic English** (or German if requested). Active voice, short sentences, defined terms used consistently (see `wiki/discipline/definition-and-object.md`).

## 5. Save and hand over

- Save drafts to `<data_dir>/drafts/<YYYY-MM-DD>_<slug>.md` (private; `eidb.py status` shows `data_dir`). Never save drafts in the repo.
- End with: an unverified-claims list (claims resting on S/D/M sources, with ids); sources that should be read in full before submission; a suggested generative-AI disclosure sentence if the venue requires one ("Generative AI (Claude, Anthropic) was used to … All content and citations were checked by the author(s)").
- Run `ei-source-and-legal-check` before anything is submitted.
