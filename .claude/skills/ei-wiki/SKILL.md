---
name: ei-wiki
description: Create, update, restructure or check pages of the public Education Informatics wiki. Use when the user asks to write up a concept, approach, method or argument as a wiki page, to change or merge pages, to fix links or citations, or when another skill needs a new page.
argument-hint: <page or topic>
---

# EI wiki maintenance

The wiki is **public**. It holds the field's structured knowledge, citable to the private database. No personal data, no career details, no verbatim private notes, and no reproduction of unpublished third-party material.

## Page anatomy

```yaml
---
title: Human-readable title
kind: discipline | concept | approach | method | proposition | governance | rival | other
status: seed | draft | reviewed
updated: YYYY-MM-DD
summary: One line, shown in the generated index
criteria: [object, knowledge, theory, terminology, methods, institutions]   # those the page informs
related: [folder/slug, ...]          # paths relative to wiki/, without .md; must exist
---
```

Front matter uses only `key: value` and `key: [a, b]` lines (the validator's parser is minimal).

**Where pages go:** `wiki/discipline/` (field-level arguments), `wiki/concepts/`, `wiki/approaches/`, `wiki/methods/`, `wiki/propositions/`, `wiki/governance/`. File names are kebab-case slugs.

**Templates:** `templates/wiki_approach.md`, `templates/wiki_concept.md`, `templates/wiki_proposition.md`, `templates/wiki_discipline.md`.

## Writing rules

- One idea per page. Split a page when it has two stories.
- Open with the claim or definition; follow with a table where comparison helps.
- Cite with `[@key]` or `[@key1; @key2]`. Examples in backticks are ignored by the validator.
- Mark **own synthesis** and **proposal** explicitly; never present them as findings.
- Every approach page includes the characteristics grid and an **EI relevance** section (which criterion it informs; does it support, refine or threaten the uniqueness argument?).
- Link both ways: if A relates to B, B's `related:` lists A.
- `status`: `seed` = written by the agent from limited reading; `draft` = substantially worked; `reviewed` = the user has checked it. Only the user's explicit approval makes a page `reviewed`.
- Update `updated:` whenever the content changes.

## After editing

```bash
python3 scripts/eidb.py sync && python3 scripts/eidb.py wiki-index && python3 scripts/eidb.py validate
```

Add a line to `wiki/log.md`. When renaming a page, update every `related:` entry and inline link (`grep -rn "old-slug" wiki/`). When renaming a citekey, use `eidb.py rename OLD NEW`, which also rewrites the wiki.
