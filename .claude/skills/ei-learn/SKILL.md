---
name: ei-learn
description: Fold lasting lessons from a session into the EI_Content_Agent skills so later papers and proposals follow Education Informatics developments. Use at the end of a substantive session, after an ingest that produced a recurring judgement, when the user corrects the agent's approach, or when the user says "remember this for next time" or "update the skills".
---

# Learn: keep the skills current

Skills hold **how to work** and **recurring judgements**. The wiki holds **what is known**. The database holds **sources**. Put each lesson in exactly one place.

## What qualifies

| Lesson | Goes to |
|---|---|
| A verdict likely to recur (e.g. "measure the room, not the child") | `ei-proposition-stress-test` → *Recurring judgements* |
| A new rival or neighbouring field to check every time | `ei-uniqueness-argument` → *Rival audit*, and `wiki/discipline/rival-fields.md` |
| A legal or ethical line | `ei-source-and-legal-check` and `wiki/governance/` |
| A characteristic every approach should be described by | the grid in `wiki/approaches/data-based-approaches.md` and `templates/wiki_approach.md` |
| A better search route or source type | `ei-ingest` → *Research* |
| A positioning rule for proposals | `ei-proposal` → *Positioning rules* |
| A correction of the agent's behaviour by the user | the skill concerned, plus `CLAUDE.md` if it is a standing rule |
| A one-off fact about a topic | **not a skill**: wiki page |
| Personal, career or eligibility details | **never in the repo**: private notes in `<data_dir>` only |

## How

1. List the candidate lessons from the session (at most five) and choose those that would change future behaviour.
2. Edit the skill concisely: one bullet or one table row per lesson, phrased as an instruction, with the source or date if it rests on evidence.
3. Do not let skills drift from the wiki: if a judgement depends on evidence, link the wiki page rather than restating the evidence.
4. If a lesson contradicts an existing instruction, replace the old one; do not keep both.
5. Add a line to `wiki/log.md` ("Skills: …").
6. Tell the user in one or two lines which skills changed and why.

Skill files must keep their front matter (`name`, `description`). The description decides when a skill triggers, so update it when a skill's scope changes.
