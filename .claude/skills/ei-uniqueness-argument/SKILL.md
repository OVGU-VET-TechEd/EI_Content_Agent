---
name: ei-uniqueness-argument
description: Build or test the claim that Education Informatics (Bildungsinformatik) is a distinct field with its own method. Use when writing a disciplinary argument, a proposal's state of the art, or a reply to "a new field needs a unique method", or when comparing EI with Learning Analytics, EDM, Educational Data Science, Learning Engineering, Business or Engineering Informatics — even if the user only says "make it more unique".
---

# EI uniqueness argument

Carried over from EI_Agent (31 Oct 2026); now grounded in the wiki and database.

## Starting position

Read `wiki/discipline/disciplinarity-criteria.md` and `wiki/discipline/uniqueness-argument.md` first; they are more current than this skill. The anchor paper [@Tegelbeckers2026Education] sets the standard: six criteria (object, accumulated knowledge, theories, terminology, methods, institutional manifestation). It concedes that methods are only partly met and that knowledge and institutions are unmet. New arguments start from these concessions; they do not repeat earlier claims.

## Rules of argument

1. **Never argue from analogy alone.** "A domain pairing establishes a programme, not a field." Parity with Business Informatics and market demand are context, not warrants.
2. **Claim combination, not invention.** Do not claim a new statistical method. Say which combination is new and why the domain requires it.
3. **Locate distinctiveness in three layers:** the constitutive artefact (a formal model of what the domain acts on), the validity test (what the domain requires of that model), and the design rule (what the domain forces into the data).
4. **Current proposal for the layers:** the educational decision record (aim, decision, evidence, inference, action, response, expiry); the decision-value test; aims, expiry and contestability as data. It is a *proposal*. Check `wiki/discipline/open-questions.md` for whether the user has since chosen a core unit.
5. **Link levels.** Connect classroom data to the anchor paper's governance object (procurement, architecture, stewardship). If an argument leaves governance behind, flag it as a change of topic.
6. **Answer the critics you cite.** Arguments for more data must face Biesta, Hartong & Förschler, Hautz & Lipp and Richter et al. (all in the database).

## Required steps

1. Comparison table: interface field → constitutive artefact → validity test → what the parent disciplines did not supply.
2. Education's constraints, each with a source and what it forces on the model; say which are shared with other domains.
3. **Rival audit** (below): what each rival does, what it lacks, residual risk (low/medium/high). Update `wiki/discipline/rival-fields.md` with anything new.
4. **Defeat conditions:** at least one way each central claim could fail.
5. **Calibration design:** known results. Current: learning styles as negative control [@Pashler2008Learning]; expertise reversal as positive control [@Tetzlaff2025Cornerstone].

## Rival audit (minimum)

Learning Analytics and EDM; Educational Data Science; learning design + LA (Lockyer et al.); xAPI and Caliper; evidence-centred design and argument-based validity; data-based decision making and DBI; **Learning Engineering (strongest rival)**; open/lifelong learner models (Kay); precision education; experimentation platforms and MRTs; IS design science; neighbouring labels (TCR 2010 Education Informatics, Eduinformatics, eLearning Informatics); German Bildungsinformatik groups such as DIPF (not yet audited).

A search that finds nothing is not evidence of absence. Report how the search was done, and run a proper documented search before a proposal relies on a gap.

## Output

Verdict first. Then the argument, the rivals table, residual risks and defeat conditions. Mark synthesis as your own interpretation, and run `ei-source-and-legal-check` on the citations.
