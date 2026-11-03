---
title: Data-based approaches in education
kind: approach
status: seed
updated: 2026-11-03
summary: Families of data-based approaches and the characteristics that distinguish them — the comparison grid for any new approach
criteria: [methods, object, theory]
related: [concepts/assessment-triangle, concepts/educational-decision-record, discipline/rival-fields, approaches/learner-portfolios, governance/ai-act-and-learner-data]
---

# Data-based approaches in education

"Data-based" covers very different things: a teacher team reviewing work samples, a predictive dropout model, a sensor-rich classroom. This page sets out **which families exist** and **which characteristics distinguish them**, so that every new approach added to the knowledge base can be placed on the same grid.

## Families

| Family | Core idea | Key sources |
|---|---|---|
| Data-based decision making (DBDM) | Iterative cycle: goals, collecting data, sense-making, improvement action, evaluation; teams and school improvement | [@Schildkamp2019Data; @Mandinach2012Perfect] |
| Instructional data use (IES guide) | Collect, interpret, form hypotheses, modify instruction to test them, re-evaluate; questions determine data | [@Hamilton2009Using] |
| Data-based individualization (DBI) | Progress monitoring says *when* to change, diagnostic assessment says *what* to change; fidelity and adaptation | [@NCII2013Databased] |
| Assessment design as inference | Cognition, observation and interpretation designed together; evidence-centred design; validity arguments | [@NRC2001Knowing; @Mislevy2003Structure; @Kane2013Validating] |
| Formative assessment | Eliciting evidence and acting on it within teaching; five key strategies | [@Black2009Developing; @Anders2022Effect] |
| Learning Analytics / EDM | Traces of learner activity in digital environments; prediction, clustering, knowledge tracing, dashboards | [@Romero2020Educational; @Siemens2013Learning; @Gasevic2014Forget] |
| Educational Data Science | Convergence of LA and EDM; data-science methods and new data sources in education research | [@Cerezo2024Reviewing; @McFarland2021Education; @Aljawarneh2021Data] |
| Explanatory learner models | Models that explain learning, because accuracy alone is not actionable | [@Rose2019Explanatory] |
| Multimodal LA | Fusing physiological, behavioural and contextual streams | [@Mu2020Multimodal] |
| Learning design + analytics | Documented pedagogical intent is needed to read analytics | [@Lockyer2013Informing] |
| Precision education | Personalisation modelled on precision medicine | [@Hart2016Precision; @Triola2023Precision] |
| Learning engineering | Learning sciences plus human-centred engineering and data-informed iteration | [@Goodell2022Learning] |
| Experimentation at decision points | Randomising options repeatedly to estimate time-varying effects | [@Klasnja2015Microrandomized] |
| Portfolio-based evidence | Learner-curated longitudinal evidence with reflection and feedback | [learner portfolios](learner-portfolios.md) |

## Characteristics: the comparison grid

Use these dimensions to describe any data-based approach. They are the "possible characteristics" this page tracks; extend the list when a new approach does not fit.

| # | Characteristic | Question to ask | Range observed |
|---|---|---|---|
| 1 | **Decision anchor** | Which decision does the data serve, and who makes it? | None (exploratory) → named instructional decision (DBI, IES guide) |
| 2 | **Unit of analysis** | Learner, group, course, institution, system? | Learner activity (LA/EDM) → school (DBDM) → system (data infrastructures [@Gulson2018Emerging]) |
| 3 | **Evidence classes** | Work samples, assessments, logs, self-report, context, environment, physiology? | Classroom artefacts → clickstreams → sensors [@Mu2020Multimodal] |
| 4 | **Cycle and timescale** | One-off, termly, weekly, in the moment? | Annual monitoring → just-in-time [@Klasnja2015Microrandomized] |
| 5 | **Actor and agency** | Who interprets? Can the learner see, contest or curate it? | Analyst/algorithm → teacher team → learner (portfolios, open learner models [@Kay2008Lifelong]) |
| 6 | **Theory link** | Is there an explicit model of learning or competence? | Strong (assessment triangle) → weak or absent (much LA [@Gasevic2014Forget]) |
| 7 | **Validity approach** | How is the inference from data to claim justified? | Validity argument [@Kane2013Validating] → predictive accuracy only |
| 8 | **Action repertoire** | What can change: content, feedback, grouping, time, environment? | DBI includes environment and grouping [@NCII2013Databased] |
| 9 | **Evaluation of the action** | Is the change itself evaluated? | Progress monitoring, trials → none |
| 10 | **Governance and law** | Legal basis, steward, retention, prohibited inferences, minors | Often unspecified [@Wieczorek2026Beyond]; emotion inference prohibited in institutions [@EC2025Guidelines] |
| 11 | **Effect on the governed** | Does the approach change conduct or identity? | Documented narrowing of conduct [@Hautz2026Algorithmic] |
| 12 | **Evidence base** | How strong is the evidence that the approach improves learning? | Low-rated (IES guide) → RCTs (formative assessment, AI tutoring [@Anders2022Effect; @Kestin2025Tutoring]) |
| 13 | **Expiry** | When does an inference stop counting? | Rarely specified anywhere (EI candidate contribution) |

## Cross-cutting findings

- **Collect evidence that changes a decision, not simply more data.** DBI, the IES guide and the assessment triangle all make data depend on the decision and the construct [@NCII2013Databased; @Hamilton2009Using; @NRC2001Knowing].
- **Design, not access, decides the direction of effect.** Unrestricted generative AI harmed later performance, while a safeguarded tutor did not [@Bastani2025Generative].
- **Data represent less than they seem.** Monitoring data diverge from what they are taken to represent [@Hartong2019Opening]. Interpretation of educational data is hard and may need new frameworks [@Aljawarneh2021Data].
- **Evidence for data use itself is modest.** The IES guide rated all five recommendations' evidence as low [@Hamilton2009Using].

## EI relevance

Most families fill only some of the 13 characteristics. **No family covers decision anchor, cross-level unit, governance and expiry together.** That gap is what the [decision record](../concepts/educational-decision-record.md) proposes to fill (criterion C5; [uniqueness argument](../discipline/uniqueness-argument.md)).

## Leads to follow up

- Teacher data literacy frameworks beyond [@Mandinach2012Perfect].
- Education-specific micro-randomised trials (none checked yet).
- German "datengestützte Schul- und Unterrichtsentwicklung" literature (not yet in the database).
