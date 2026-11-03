---
name: ei-proposal
description: Develop a research project proposal on an Education Informatics topic and fit it to any funder — DFG, ERC, BMBF/BMFTR, Horizon Europe, Erasmus+, foundations. Use when the user mentions a proposal, grant, call, funder, Antrag, Ausschreibung or deadline, or asks to turn an EI idea into a project, work packages or a schedule.
argument-hint: <topic and/or funder/call>
---

# EI project proposal (funder-neutral)

This skill uses a **general outline** that maps onto any funder. Funder rules change and are never taken from memory: each call gets a fresh **funder profile** built from the current documents.

## Order of work

1. **Download the current call and rules.** Record each document's title, version and date. If the user has not named a funder, build the scientific core first (steps 3–5) and map it later.
2. **Build the funder profile** (`templates/funder_profile.md`): eligibility, structure and page limits, review criteria (word for word where possible), attachments, budget rules, AI-disclosure rule, deadlines. Save it to `<data_dir>/drafts/funder_<name>_<date>.md`. Funder profiles are private.
3. **Check eligibility and blocking issues first** and report them before drafting anything. Ask only for facts you cannot find.
4. **Build the scientific core** from the knowledge base, using `templates/proposal_outline.md`:
   - problem and gap: from `wiki/discipline/*` and the topic's wiki pages;
   - objectives and **falsifiable hypotheses**, each with a "fails if…" condition;
   - work packages with a question, method, sample/setting, output and month range; methods from `wiki/methods/method-repertoire.md`;
   - calibration or quality measures (pre-registration, controls, double coding);
   - ethics, data and legal lines (`wiki/governance/`; `ei-source-and-legal-check`);
   - a risk table with responses.
5. **Map the core to the review criteria,** not only to the form headings. Every review question needs a visible place in the text. Make a table: criterion → section → the sentence that answers it.
6. **Draft in the funder's structure.** Put facts you do not have in `[brackets]`. **Never invent** a track record, partner, letter of support, budget figure, preliminary result or contact.
7. **Schedule logic:** stage gates that follow from the funder's reporting points; dependencies between work packages.
8. **Open-items list:** decisions for the user, attachments, verification, page count.

## Positioning rules for EI proposals

- Start from the anchor paper's concessions (no accumulated knowledge, no institutional manifestation, method only partly specific) and show how the project **produces** what is missing. Do not claim the field already exists.
- Claim a **combination**, not a new statistical method, and name the rival that would challenge it (Learning Engineering first).
- A project that only builds a curriculum argues the weakest criterion (C6). The anchor paper says the academic pathway comes last.
- Keep the topic distinct: "all parameters" and "the whole field" read as no distinct topic.
- Biometrics, minors and AI evaluation need explicit legal handling (`wiki/governance/ai-act-and-learner-data.md`).
- Pilot data beat argument: if the applicant's preliminary work is conceptual, plan a small empirical pilot before submission.

## Output

1. Blocking issues; 2. the draft in the funder's structure (saved to `<data_dir>/drafts/`); 3. the review-criteria map; 4. open items. Keep funder-facing text separate from internal commentary.

## Record what you learn

Once a call has been worked through, record the reusable parts (review-criteria wording, typical pitfalls) in the private funder profile and, if general, in `ei-learn`. Personal eligibility details stay private, never in the repo.
