---
name: ei-ingest
description: The main Education Informatics knowledge loop. Use whenever the user brings a new topic, approach, idea, country example or source ("I heard about data-based approaches", "learner portfolios from the UK", a DOI, a PDF, a link), or asks to research something for EI. Researches it, records every source in the CSV database, creates or updates wiki pages, connects them to the discipline argument, and updates skills if a lasting pattern was learned.
argument-hint: <topic, idea or source>
---

# EI ingest: from a prompt to structured knowledge

The goal is that every prompt leaves the discipline **better structured**: sources recorded and verified, characteristics noted, connections to the six criteria made explicit, and nothing invented.

## 0. Before you start

- The SessionStart hook has already backed up the CSV. If you are unsure, run `python3 scripts/eidb.py backup --reason ingest`.
- Run `python3 scripts/eidb.py list --text "<key words>"` and `grep -ril "<key word>" wiki/` to see what the knowledge base already holds. **Update rather than duplicate.**

## 1. Scope the topic

Restate the topic in one line and name its type: an *approach* (a family of practices), a *concept*, a *method*, a *policy or legal question*, a *rival field*, or a *single source*. Choose up to five concrete research questions, for example: What is it? Where does it come from (country, sector)? What evidence exists? What data does it use, and for which decisions? How does it relate to EI's object and to the six criteria?

If the request is ambiguous in a way that changes the work, ask one short question. Otherwise proceed.

## 2. Research

In this order:

1. **Local first.** Search the literature folders (`literature_dirs` in `ei.config.json`) for PDFs and notes on the topic. Read what is relevant; extract DOIs from PDFs.
2. **Scholarly search.** Use WebSearch (several queries in one turn) and `python3 scripts/eidb.py search "<author year title words>"` to find peer-reviewed sources. Prefer reviews, landmark papers, recent empirical studies, official reports and standards.
3. **Read before you summarise.** For each candidate, run `python3 scripts/eidb.py fetch <DOI>` (title, venue, abstract) or open the page or PDF. The summary may only claim what you read; the status label says how deep you read.
4. **Sanity rules:** search snippets are not sources; check author, year and title against the DOI record; note disagreements; say how narrow a search was if it found nothing.

Aim for the 3–10 sources that matter, not everything that matches.

## 3. Record every source in the database

For each source (or in one `add-batch` JSON file for several):

```bash
python3 scripts/eidb.py add --doi <DOI> \
  --summary "<1–3 sentences: what it claims or does, and on what basis>" \
  --topics "<kebab-case; 2–5 tags>" --criteria "<C1..C6 names it bears on>" \
  --role "<foundation|evidence|rival|critique|method|policy-legal|context>" \
  --status <P|S|D|M> --query "<the user's topic in a few words>" [--local-file "<path relative to a literature dir>"]
```

- No DOI (reports, web pages, standards, laws): pass `--type --authors --year --title --venue --url`. The script builds APA and BibTeX; set `--verified-via url-check|publisher-page|local-pdf`.
- A duplicate exits with code 3 and names the existing id. Use `update` to add topics or notes (`--add-topics`, `--append-note`).
- Reuse existing topic tags where they fit (`python3 scripts/eidb.py stats` lists them).

## 4. Write or update the wiki

- **Approach** → `wiki/approaches/<slug>.md` from `templates/wiki_approach.md`. Fill the **characteristics grid** (the 13 dimensions in `wiki/approaches/data-based-approaches.md`) and add new characteristics there if the topic shows one is missing.
- **Concept / method / governance** → `templates/wiki_concept.md`.
- **Ideas to test** → `templates/wiki_proposition.md`, or a new row in an existing proposition page.
- Cite with `[@citekey]`. Label your own synthesis. Link related pages both ways (front-matter `related:` plus inline links).
- **Propagate:** check and update, where the new knowledge bears on them:
  - `wiki/discipline/rival-fields.md`: is this a rival or a neighbouring label? Add a row with the residual risk.
  - `wiki/discipline/disciplinarity-criteria.md`: does it move evidence on any criterion? Change a status only with a written argument.
  - `wiki/discipline/uniqueness-argument.md`: does it support, refine or **defeat** a claim? Defeaters go in as prominently as support.
  - `wiki/discipline/open-questions.md`: new open questions, weak claims, leads.
  - `wiki/approaches/data-based-approaches.md`: add the family to the table if it is data-based.

## 5. Close the loop

```bash
python3 scripts/eidb.py sync          # wiki_pages column from citations
python3 scripts/eidb.py wiki-index    # regenerate the index in wiki/README.md
python3 scripts/eidb.py validate      # must show 0 errors
python3 scripts/eidb.py export        # refresh .bib/.ris for Zotero
```

Add an entry at the top of `wiki/log.md`: date, topic (not the verbatim prompt), sources added (count and status mix), pages created or changed, follow-ups.

## 6. Learn

If the session produced a **lasting judgement** (a recurring verdict, a new rival, a legal line, a useful search route, a characteristic every approach should be checked for), run `ei-learn` to put it into the right skill. Do not record one-off facts in skills; those belong in the wiki.

## 7. Report back

Lead with the most consequential finding for EI (supports, refines or threatens the argument). Then list: sources added (id, status), wiki pages created or updated (as links), what is still unverified, and one or two suggested next steps. Keep it short; the detail is in the wiki.
