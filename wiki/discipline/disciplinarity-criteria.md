---
title: Six criteria of disciplinarity — status board
kind: discipline
status: seed
updated: 2026-11-03
summary: The standard EI is judged against; current status of each criterion and the evidence that would move it
criteria: [object, knowledge, theory, terminology, methods, institutions]
related: [discipline/definition-and-object, discipline/uniqueness-argument, methods/method-repertoire, discipline/open-questions]
---

# Six criteria of disciplinarity: status board

The anchor paper adopts an account of disciplinary formation from Krishnan [@Krishnan2009Academic]. On this account a discipline has six features. It assesses EI against all six and reports a deliberately mixed result [@Tegelbeckers2026Education]. **Every argument in this knowledge base starts from these concessions; it does not repeat claims the paper already withdrew.**

| # | Criterion | Requires | Status (anchor paper, Aug 2026) | What would settle it | Where this wiki works on it |
|---|---|---|---|---|---|
| C1 | Object of research | An object constitutive of the field | **Specified**: the educational socio-technical system | Showing that an existing field already claims this object would defeat the proposal | [Definition](definition-and-object.md), [rival fields](rival-fields.md) |
| C2 | Accumulated specialist knowledge | Knowledge about the object, specific to the field | **Not satisfied**: no definitional core, no citation community, corpus median of one citation | A citable body of work grows under a stable referent; argument cannot achieve this | The literature database itself; [open questions](open-questions.md) |
| C3 | Organising theories and concepts | Traditions adequate to the object | **Partly**: socio-technical systems, infrastructure studies, critical data studies, data-governance studies. All diagnostic, not constructive | Whether integrating them is productive or mere juxtaposition | [Uniqueness argument](uniqueness-argument.md) |
| C4 | Specific terminology | Language adjusted to the object | **Partly**: stipulated, not shared | Other authors take up the terms in the defined sense | [Definition](definition-and-object.md) |
| C5 | Specific research methods | Methods answering the object's requirements | **Partly**: no methodological novelty claimed; repertoire drawn from IS and educational research. "A claim about allocation rather than about method" | Whether the combination is distinctive in use rather than merely assembled | [Method repertoire](../methods/method-repertoire.md), [uniqueness argument](uniqueness-argument.md) |
| C6 | Institutional manifestation | Programmes, departments, associations, venues | **Not satisfied**: no journal home; the curriculum is a proposal, not evidence | Independently developed programmes converge and a venue emerges | [Definition: pathways](definition-and-object.md#three-institutionalisation-pathways) |

## The critique this board answers

The standard objection to a new field is that **it has no unique set of methods**. The anchor paper accepts that methodological *novelty* is not claimed. Its account requires methodological *specificity*. Methods are the weakest of the partly satisfied criteria. A reader who demands novelty "is entitled to" reject the proposal [@Tegelbeckers2026Education]. The [uniqueness argument](uniqueness-argument.md) is the attempt to move C5 (and with it C3) from "partly" towards "satisfied" through a specific *combination* that education requires.

## Evidence ledger

The private database tags every reference with the criteria it bears on (`ei_criteria`). To see the current evidence for a criterion:

```bash
python3 scripts/eidb.py list --criterion methods
python3 scripts/eidb.py stats          # counts per criterion
```

The generated table in the [wiki index](../README.md) shows the current counts. Rules for updating this board:

- A new source changes a **status** only with a written argument on this page and a log entry. Counts alone never change a status.
- C2 and C6 cannot be met by argument. Only track evidence of uptake: citations of EI in the defined sense, programmes, venues, role definitions.
- Record defeaters as carefully as support. A source showing that an existing field already claims the object (C1) or the method combination (C5) goes into [rival fields](rival-fields.md) **and** here.
