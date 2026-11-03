---
name: ei-status
description: Report what the Education Informatics knowledge base currently holds and what is open — counts, evidence per disciplinarity criterion, unverified sources, thin areas, next steps. Use when the user asks "what do we have", "where are we", "status", "what's missing", or at the start of a planning session.
---

# Knowledge-base status

1. Run:

```bash
python3 scripts/eidb.py stats
python3 scripts/eidb.py validate --quiet
python3 scripts/eidb.py list --status DM
```

2. Read `wiki/README.md` (generated index and criterion table), the top entries of `wiki/log.md`, and `wiki/discipline/open-questions.md`.

3. Report, in this order and briefly:
   - **Size:** references by status; wiki pages by kind; last log entry.
   - **Criteria coverage:** the six criteria with reference and page counts. Name the thinnest one and what would strengthen it. Counts are coverage, not satisfaction (see `wiki/discipline/disciplinarity-criteria.md`).
   - **Health:** validation errors; references with status D/M (to verify); references not discussed in any wiki page; seed pages never reviewed.
   - **Open decisions and top three next steps.** Prefer steps that move C5 (methods) or C2 (knowledge): a systematic rival search, a pilot, verifying key sources, a paper from a mature page.

Do not change anything in this skill. Offer the next step as a question.
