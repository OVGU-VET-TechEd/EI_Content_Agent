---
name: ei-proposition-stress-test
description: Turn research notes or ideas about data-driven education into a for-and-against assessment with clear verdicts. Use when the user asks to argue for and against propositions, test ideas from notes, or decide what to keep, or when notes mention biometrics, learner data models, 24-hour context, markers, learning styles, grouping learners, base models, or analogies between teaching and medicine.
---

# Proposition stress test

Carried over from EI_Agent (31 Oct 2026). The worked example is `wiki/propositions/medicine-analogy.md`; copy its structure.

## Method

1. **Extract every proposition,** including implied ones. Keep the user's wording and split compound claims. "Biometrics" contains attention (legally restricted) and physical state (less so).
2. **Give each the strongest case on both sides,** with evidence from the database (`[@keys]`). Do not soften the "against" side to protect the user's idea.
3. **Run four tests on each:**
   - **Decision:** which decision would this evidence change?
   - **Increment:** what does it add beyond cheaper evidence? Has anyone measured that?
   - **Lawful and ethical:** does it hold for minors and in institutions? (`wiki/governance/ai-act-and-learner-data.md`, `ei-source-and-legal-check`)
   - **Falsifiable:** what result would count against it? "All parameters" fails this.
4. **Assign one verdict:** Keep, Narrow, Test, Replace, Drop, or User's decision.
5. **Say how each kept idea enters the design:** a data field, a hypothesis, a control or a work package.

Use "User's decision" only for choices that are truly the user's (e.g. the field's core unit), and still recommend. Do not reopen decisions the user has made.

## Recurring judgements

Reuse these only after checking that the sources are still current (each is argued in the wiki).

- **Medical analogy:** keep as a transfer of methods (shared data models, network studies, micro-randomised trials, post-deployment monitoring). Adapt the reasoning model through Becher & Lefstein (prioritisation and noticing, disciplined improvisation, room to manoeuvre). Never "learners as patients".
- **Attention from biometrics in education institutions:** drop (prohibited; Commission guidelines para. 255).
- **Physical state (fatigue, gaze point without emotion inference):** narrow to a consented adult lab study, as a decision-value test.
- **24-hour context:** declared by the learner, for a named decision; never continuous.
- **Environment:** a safer evidence class. Measure the room, not the child.
- **Psychological markers:** map constructs with uncertainty rather than force one standard.
- **Learning styles:** a negative control, not a research hope.
- **Universal base model:** replace with a minimal core plus extensions justified by decision value.
- **Walking data model:** a learner-held view computed from decision records (prior art: Kay).
- **ITS data:** one test case with an AI-off baseline, not the field's centre.

## Output

A table with proposition, for, against and verdict, followed by the two or three new ideas the test produced. Put the most consequential finding first. If a proposition conflicts with the user's own published work, say so directly. Offer to save the result as a proposition page (`templates/wiki_proposition.md`).
