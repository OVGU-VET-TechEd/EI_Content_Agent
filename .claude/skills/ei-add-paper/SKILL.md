---
name: ei-add-paper
description: Record one reference in the EI literature database with verified APA and BibTeX and a short summary. Use when the user gives a single DOI, title, citation, PDF or link to note, asks to "add this paper", or when another skill needs to record a source.
argument-hint: <DOI | title | PDF path | URL>
---

# Add one reference

1. **Identify it.**
   - DOI given: go to step 2.
   - Title or citation: `python3 scripts/eidb.py search "<first author> <year> <title words>"`. Accept a candidate only if author, year and title match. If two plausible versions exist (preprint vs journal, online-first vs issue), prefer the version of record and note the other.
   - PDF: extract the DOI from the first pages; otherwise use the title page. Record its path relative to a literature dir in `--local-file`.
   - Web page, report, standard or law: no DOI. Open it, confirm it resolves, and note the publisher and year.
2. **Read.** `python3 scripts/eidb.py fetch <DOI>` gives the abstract when the registry has one. Read the PDF if it is local. Decide the status honestly:
   - **P** = you read the full text in this session, or a prior record shows it was read.
   - **S** = DOI record, abstract or title page only.
   - **D** = the content comes from the user's notes or slides.
   - **M** = from memory. Avoid adding M entries; verify first.
3. **Summarise in 1–3 sentences:** what the source claims or does, the design or basis (review, RCT, n, case study, framework), and the scope. If the summary relies on notes rather than the source, say so ("per the user's notes").
4. **Classify:** 2–5 kebab-case topics (reuse existing ones from `eidb.py stats`); the six criteria it bears on; its role for the EI argument.
5. **Add:**

```bash
python3 scripts/eidb.py add --doi <DOI> --summary "..." --topics "..." --criteria "..." --role ... --status S --query "<context>"
# without DOI:
python3 scripts/eidb.py add --type report --authors "Family, Given; Org Name" --year 2025 --title "..." \
  --venue "Publisher" --url "https://..." --summary "..." --status S --verified-via url-check
```

6. **Check the output.** The script prints the APA string. If the registry's metadata is wrong or incomplete (capitalised names, missing volume, a corporate author shown as empty), fix it with `update --set field value`, `--apa` and `--bibtex`, and `--append-note` explaining the correction.
7. If the source belongs in an existing wiki page, cite it there and run `sync`; otherwise tell the user which page it would fit.

**APA note:** registry APA strings keep the publisher's title capitalisation. Convert to sentence case when typesetting a manuscript.
