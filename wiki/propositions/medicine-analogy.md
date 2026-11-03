---
title: Propositions from the medicine analogy — for and against
kind: proposition
status: seed
updated: 2026-11-03
summary: Stress test of the "data-driven education as in AI medicine" notes — each proposition with the case for, against, and a verdict
criteria: [methods, object, theory]
related: [concepts/teaching-as-clinical-profession, concepts/lifelong-learner-model, discipline/uniqueness-argument, governance/ai-act-and-learner-data, approaches/data-based-approaches]
---

# Propositions from the medicine analogy: for and against

**Input:** the user's notes on integrating data-driven education into EI after the AIMCare 2026 meeting in Tbilisi (`Thoughts_AI_Medicine.md`, `More_concepts_Learning_in_Dataenvironment.md`). The conference slides are unpublished and not citable; claims are traced to the underlying papers.

**Verdicts:** Keep · Narrow · Test · Replace · Drop · User's decision.

## The analogy itself

**For.** Teachers, like clinicians, judge individual cases under uncertainty. Medicine has tested infrastructure worth borrowing: shared data models and network studies [@Hripcsak2015Observational], micro-randomised trials [@Klasnja2015Microrandomized] and post-deployment monitoring. Medicine also shows that tool capability is not user competence [@Goh2024Large]. Medical education is moving towards Educational Informatics teams [@Turner2024Takes] and precision education [@Triola2023Precision].

**Against.** Diagnosis invites a deficit view. Teaching has no manageable diagnostic classification. Teachers act on groups, in real time. Education's goals are far more contested than health [@Becher2020Teaching; @Biesta2007Works].

**Verdict: Keep, as a transfer of methods, not as a claim about learners.** Never write "learners as patients". Borrow medicine's infrastructure; adapt its reasoning model through Becher and Lefstein ([teaching as a clinical profession](../concepts/teaching-as-clinical-profession.md)).

## Proposition by proposition

| Proposition (from the notes) | For | Against | Verdict |
|---|---|---|---|
| **Biometrics: level of attention** | Attention plausibly matters; sensors make it observable [@Mu2020Multimodal] | Inferring students' interest and attention by emotion-recognition AI in an education institution is **prohibited** [@EC2025Guidelines]; links between physiology and outcomes are inconsistent | **Drop** for schools and institutional use; never a field of the base model |
| **Biometrics: physical disposition** | Fatigue and pain are not "emotions" under the guidelines; gaze point without emotion inference is not prohibited [@EC2025Guidelines] | Still sensitive data; the line blurs if arousal is added; no shown benefit over logs and work samples | **Narrow and test**: consented adult lab study only, as a decision-value test |
| **24-hour social context** | Opportunity to learn and living conditions shape interpretation [@NRC2001Knowing]; DBI treats conditions as adjustable [@NCII2013Databased] | Surveillance, power imbalance, disproportionate for minors; data-derived norms narrow conduct [@Hautz2026Algorithmic] | **Narrow**: only as declared, learner-provided context for a named decision; never continuous capture |
| **Environment (noise, time, place)** | Measurable without inferring anything about the person; DBI already adapts settings | Weak as a universal causal variable; school sensors still need approval | **Keep**: the safest new evidence class. *Measure the room, not the child* |
| **Standardise psychological markers** | Jingle-jangle is real; embeddings can map measures [@Wulff2025Semantic] | Forced harmonisation hides real theoretical differences; evidence is from personality items | **Keep as mapping, not as one standard**: crosswalks with stated uncertainty |
| **More process markers: what, why, how to learn** | Directly supported by the assessment triangle and instructional history [@NRC2001Knowing]; "why" is missing from activity standards [@ADLxAPISpec] | Burden; a "why" can be rationalised after the fact | **Keep: this is the core.** It becomes the aim and inference fields of the [decision record](../concepts/educational-decision-record.md) |
| **Test grouping strategies (learning styles etc.)** | Clean design, high scientific value | Learning styles are already refuted [@Pashler2008Learning]; subgroup analysis invites false positives and labelling | **Keep, redesigned** as negative and positive controls [@Tetzlaff2025Cornerstone] |
| **Structure, check against theory, extend** | Answers weak theory transfer in LA [@Gasevic2014Forget] | Can become endless cataloguing | **Keep, bounded**: only theories that inform a named decision |
| **Theory transfer, e.g. game theory for group work** | Team and group decisions are real educational decisions; game theory supplies formal markers | Lab incentives may not transfer; risk of analogy-hunting | **Test**: one worked example (group formation), not a general programme |
| **The learner as a walking data model** | Learners carry history across institutions; learner ownership is attractive | Kay proposed it [@Kay2008Lifelong]; "walking" implies constant monitoring; critical data studies cut against it | **User's decision**: see [lifelong learner model](../concepts/lifelong-learner-model.md); recommendation is the learner-held computed view |
| **Base model with all parameters across fields** | Standards enable reuse, as in health | "All parameters" is unbounded and unfalsifiable; reviewers will read it as lacking a distinct topic | **Replace** with a minimal core plus extensions justified by decision value |
| **Data bases and standards for intelligent tutoring systems** | Tutors need stable data on knowledge state, practice and feedback; guardrails decide effects [@Bastani2025Generative; @Kestin2025Tutoring] | Tutors are a small part of education; a narrow focus would turn EI into ITS research | **Keep as one test case**, with an AI-off baseline |
| **New protocols for sensitive education data** | Data trusts are feasible [@Wieczorek2026Beyond]; federated analysis [@Hripcsak2015Observational] | Synthetic data is not automatically private; building a new protocol is a large engineering task | **Keep as an extension of existing standards**, with audits; do not invent a competing standard |

## What the test produced

1. The most consequential finding is legal: **attention inference is out** in education institutions. Any proposal built on it fails.
2. The strongest proposition is the least technical one: **record what, why and how**, the decision context. It becomes EI's candidate core ([uniqueness argument](../discipline/uniqueness-argument.md)).
3. New ideas: *measure the room, not the child*; learning styles as a **negative control**; **expiry** of educational inferences as a design parameter.
