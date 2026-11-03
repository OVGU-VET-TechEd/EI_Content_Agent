---
title: Uniqueness argument — answering "no method of its own"
kind: discipline
status: seed
updated: 2026-11-03
summary: Working proposal for what makes EI methodologically specific — constitutive artefact, validity test, design rule — with defeat conditions
criteria: [methods, theory, object]
related: [discipline/disciplinarity-criteria, discipline/rival-fields, concepts/educational-decision-record, concepts/interface-discipline, methods/method-repertoire, propositions/medicine-analogy]
---

# Uniqueness argument: answering "no method of its own"

> **Status: working proposal (own synthesis).** It goes beyond the published anchor paper and says so openly. No part of it is a published finding. Sections marked *own synthesis* need their own literature check before they carry weight in a proposal.

## 1. The objection and where the anchor paper leaves it

A new field is usually challenged for having no unique methodology. The anchor paper concedes most of this: methods are "partly satisfied; no methodological novelty is claimed", accumulated knowledge and institutional manifestation are "not satisfied", and the claim is "about allocation rather than about method" [@Tegelbeckers2026Education]. That is honest but thin. A reviewer can accept every finding and still ask what EI does that Learning Analytics, Information Systems or Learning Engineering could not ([rival fields](rival-fields.md)).

Two weak warrants are **not** used here. Structural parity with Business Informatics is ruled out by the paper's own sentence, "a domain pairing establishes a programme, not a field" [@Tegelbeckers2026Education]. Labour-market demand does not answer a question about method.

## 2. Thesis

EI becomes methodologically specific if it owns three things **together**:

| Layer | Content | Status |
|---|---|---|
| **Constitutive artefact** | A formal model of the *educational decision* as the field's basic unit ([educational decision record](../concepts/educational-decision-record.md)) | Proposal |
| **Validity test** | Evidence is valid when it *justifiably changes a defensible decision* beyond what cheaper evidence does, and the changed decision helps those it is meant to help under the declared aim (the **decision-value test**) | Proposal |
| **Design rule** | Aims, expiry and contestability are recorded as *data*, because education's constraints make them part of what the evidence means | Proposal |

No single layer is new. The claim is that nobody yet combines them under one accountable model, and that the combination can be tested empirically. This is a claim about **combination**, not invention.

## 3. How other interface fields became distinct (own synthesis)

| Field | Constitutive artefact | Validity test imposed by the domain | What the parent disciplines did not supply |
|---|---|---|---|
| Business Informatics | Process and enterprise models, reference models, IS designs [@Helfert2008Business; @Osterle2011Memorandum] | Does the designed system work in the organisation? | CS has no account of the firm; business administration does not build systems |
| Engineering Informatics | Product, simulation and digital-twin models [@Xu2014Engineering] | Does the model predict the physical artefact within tolerance? | Engineering needs information models that are physically faithful and documented for compliance |
| Medical informatics (contrast) | Patient record, terminologies, a shared common data model [@Hripcsak2015Observational] | Do results replicate across sites, and do they improve care? | Clinical medicine needs observations comparable across institutions |
| **Education Informatics (proposed)** | **Educational decision record**, with a computed learner view | **Decision-value test** (section 2) | Education science has the criteria of judgement; informatics has the systems; neither formally models the decision |

**Pattern:** these fields did not become distinct through a new statistical technique. Each owns a formal model of what its domain acts on, plus a test of that model that the domain imposes. This pattern is an interpretation, and a good candidate for a short paper of its own ([open questions](open-questions.md)).

## 4. What education forces on the method

Each feature is shared with some other domain. The **combination** forces the design.

| Feature of education | Source | What the data model must therefore do |
|---|---|---|
| Aims are contested; "what works?" hides "for what?" | [@Biesta2007Works; @Becher2020Teaching] | Record the aim; evidence is valid only relative to it |
| Teaching is collective: one act affects a group | [@Becher2020Teaching] | Represent group decisions and trade-offs between learners |
| Decisions happen in seconds; non-action is a response | [@Becher2020Teaching; @Wise2019Teaching] | Low-effort capture that includes waiting and declining to act |
| Learning is intended change; measurement alters conduct | [@Hautz2026Algorithmic; @Gasevic2014Forget] | Give each inference an expiry; audit effects on conduct |
| Constructs are latent and labelled inconsistently | [@Wulff2025Semantic] (psychology; transfer untested) | Map constructs before pooling data |
| Law limits inference directly (emotion recognition in education institutions is prohibited) | [@EC2025Guidelines] | Record the legal basis per evidence class; work without prohibited inference |
| Learners include minors; records cross institutions for decades | [@Kay2008Lifelong; @Wieczorek2026Beyond] | Learner control, retention limits, a named data steward |
| Outcomes arrive late and are weakly evidenced | [@Hamilton2009Using] (evidence rated low) | Separate proximal response from later outcome; never let proxies pose as outcomes |
| Monitoring data diverge from what they represent | [@Hartong2019Opening] | Keep provenance and the inference warrant with every datum |

Becher and Lefstein give the sharpest requirement. They adapt medicine's diagnosis, treatment and inference into **prioritisation and noticing, disciplined improvisation, and room to manoeuvre** [@Becher2020Teaching]. As data, this means recording what was prioritised and what was set aside, how the action departed from the plan, and which options were really available. A clickstream holds none of this. See [teaching as a clinical profession](../concepts/teaching-as-clinical-profession.md).

## 5. The method: decision-anchored evidence engineering (working label)

1. **Model the decision first.** Establish the options (including doing nothing) and the aim before choosing data. This follows decision-based data use [@Hamilton2009Using; @Schildkamp2019Data] and the assessment triangle [@NRC2001Knowing].
2. **Write the inference chain.** State what must hold for this evidence to support this conclusion. This extends evidence-centred design and argument-based validation [@Mislevy2003Structure; @Kane2013Validating] from assessment to the decision lifecycle.
3. **Test decision value.** An evidence class stays only if it changes a defensible decision beyond cheaper evidence. This settles questions such as biometrics or 24-hour context empirically, not by preference ([medicine-analogy propositions](../propositions/medicine-analogy.md)).
4. **Test the changed decision.** Where options are equally defensible, randomise at the decision point, as in micro-randomised trials [@Klasnja2015Microrandomized], adapted to cluster structure because teachers act on classes. Replicate across sites through a shared model, as OHDSI does in health [@Hripcsak2015Observational].
5. **Connect levels.** The same record structure covers classroom decisions, institutional decisions (choosing a platform) and system decisions (a procurement rule). This links learner data to the anchor paper's governance object and opens a new question: *which institutional decisions constrain which classroom decisions?*

**Calibration before discovery.** The infrastructure must reproduce known results before it is trusted on new ones:

- **Negative control:** matching instruction to "learning styles" shows no meaningful benefit [@Pashler2008Learning].
- **Positive control:** instruction interacts with prior knowledge (expertise reversal) [@Kalyuga2007Expertise; @Tetzlaff2025Cornerstone].

If the system "finds" learning-style effects or misses expertise reversal, the fault lies in the system. This also answers the idea of "testing existing grouping strategies with education markers".

## 6. What would defeat the claim

Any one of these would:

- An existing field already uses a shared decision model across levels (check Learning Engineering and learning-design models first; [rival fields](rival-fields.md)).
- The decision record cannot represent real decisions across sectors without constant extension.
- Capture cost makes it unusable by educators.
- Decision-value testing never changes a retention decision about an evidence class.
- Results transport between settings no better than with activity data alone.

The anchor paper sets the same standard for its own claim: it "fails in the ordinary way" if the integration already exists in an established field [@Tegelbeckers2026Education].

## 7. Further candidates for uniqueness (ranked by weight they can bear)

1. **Expiry as a first-class concept.** The learner changes, so the inference must follow; the institution should forget, so the record must allow it. A measurable *half-life of an educational inference* would be a new, citable contribution.
2. **The AI-on vs AI-off gap as a standard measure.** Design, not access, decided the direction of effects in recent trials [@Bastani2025Generative; @Kestin2025Tutoring], and capability did not become competence in medicine [@Goh2024Large]. An "AI-off" baseline in the response record protects unassisted competence.
3. **Decision rights as data.** Who may decide, see and contest a record. This turns the governance argument [@Wieczorek2026Beyond] into a technical structure.
