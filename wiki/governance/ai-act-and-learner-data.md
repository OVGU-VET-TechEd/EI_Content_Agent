---
title: AI Act and learner data — where the lines are
kind: governance
status: seed
updated: 2026-11-03
summary: Which learner-data practices are prohibited, high-risk or open under the EU AI Act, plus standing safeguards for research
criteria: [object]
related: [propositions/medicine-analogy, concepts/educational-decision-record, approaches/data-based-approaches]
---

# AI Act and learner data: where the lines are

> A reading of the sources, **not legal advice**. Funded work needs a written legal opinion. Check against the current text before every use.

## Lines drawn by the Commission guidelines

Primary source: Commission guidelines C(2025) 5052 final [@EC2025Guidelines], interpreting Art. 5(1)(f) of the AI Act [@EU2024AIAct].

| Practice | Position | Paragraph |
|---|---|---|
| Emotion-recognition AI in an education institution to infer students' interest and attention | **Prohibited** | 255 |
| Emotion recognition during admission tests | **Prohibited** | 255 |
| An institution requiring learners to use an emotion-recognition app | **Prohibited**; voluntary use outside an institution is not caught | 255 |
| Gaze tracking that only detects where someone looks, without emotion inference | Not prohibited; becomes prohibited if arousal or anxiety is also inferred | 255 |
| Physical states such as pain or fatigue | Not "emotions or intentions" | 249 |
| Role-play training (e.g. teachers, actors) with no effect on evaluation or certification | Allowed | 255 |
| AI solely for scientific research and development | Excluded under Art. 2(6); data protection and ethics still apply | 31, 33 |
| Later use of research results; real-world testing | Not covered by the research exclusion: check separately | 32 |

**Scope of "education institution" (para. 255):** public and private, all ages and levels, online or in person, including vocational and continuing training. Admission candidates are included.

## High-risk uses (Annex III, point 3)

Admission and assignment, evaluating learning outcomes, assessing the appropriate level of education, and monitoring prohibited behaviour during tests [@EU2024AIAct]. The application date for these duties is reported as moved (to 2 December 2027) by the Digital Omnibus. **Verify in the Official Journal before citing.**

## What the prohibition does *not* say

It concerns **biometric** emotion or intention inference. Do not stretch it to inference from logs or text, and do not assume those are free of other limits (GDPR, state school law, ethics review).

## Standing safeguards for EI research

- **Minors:** no biometrics by default; guardian consent and age-appropriate assent; refusal without disadvantage; state approval procedures.
- **Teachers:** records are not used to evaluate individuals.
- **Everyone:** a named data steward, retention limits tied to the expiry field, a route to contest. Data trusts are one governance option [@Wieczorek2026Beyond].
- **Randomisation:** only among options educators judge equivalent; never withhold support known to be needed.

## Consequences for EI design

The [decision record](../concepts/educational-decision-record.md) records the **legal basis per evidence class** and must work without any prohibited inference. The [medicine-analogy test](../propositions/medicine-analogy.md) drops attention biometrics for exactly this reason.
