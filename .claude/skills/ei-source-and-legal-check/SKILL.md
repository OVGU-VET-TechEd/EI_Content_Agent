---
name: ei-source-and-legal-check
description: Check sources, evidence status and legal limits in Education Informatics writing before it is used or submitted. Use whenever a paper, proposal or argument cites literature, makes claims about learner data, biometrics, the EU AI Act, minors or schools, or needs a generative-AI disclosure, and whenever the user asks whether something can be cited, is allowed, or is verified.
---

# Source and legal check

Carried over from EI_Agent (31 Oct 2026); funder-specific rules removed. Check the actual funder or journal rules for each submission.

## 1. Sources

Every citation must resolve to a database entry (`python3 scripts/eidb.py show <id>`). Status codes:

| Code | Meaning | May carry weight? |
|---|---|---|
| P | Primary text read directly | Yes |
| R | Cited in the anchor paper; not re-read | Background only; re-read before it carries an argument |
| S | DOI record, abstract or title page | For what the abstract states; read in full before relying on details or figures |
| D | From the user's notes or slides | No: trace to the source first |
| M | From model memory | No |

Rules:
- Search summaries are not sources. Check author, year and title against the DOI record.
- Report disagreements (year, venue, figures) instead of picking one silently. Online-first vs issue year is common: cite the issue year consistently.
- A failed search is not proof of absence; state how narrow it was.
- Separate what evidence shows, what is plausible but untested, and what is a design commitment.
- Label your own synthesis as your own.
- **Citability:** many funders and journals accept only published works or accepted manuscripts. Conference decks, unpublished drafts and personal communications are traced to the underlying published papers.
- Mark the user's own work clearly as such.

Commands: `python3 scripts/eidb.py list --status DM` (to verify); `cites <wiki page>` (status of each citation on a page).

## 2. Legal line (reading, not legal advice)

The current line is in `wiki/governance/ai-act-and-learner-data.md`; check it against the current text. In short:
- **Prohibited:** emotion-recognition AI in education institutions, including inferring students' interest or attention; also in admission tests; required use of such an app by an institution.
- **Not prohibited per se:** gaze point without emotion inference; physical states such as fatigue; role-play training without effect on evaluation.
- **Research exclusion** (Art. 2(6)) covers AI solely for research; data protection and ethics still apply; real-world testing and later use are not covered.
- **High-risk** (Annex III point 3): admission and assignment, evaluating learning outcomes, assessing the level of education, test proctoring. Verify the application date (Digital Omnibus) in the Official Journal.
- The prohibition concerns **biometric** inference. Do not stretch it to logs or text, and do not assume those are free of GDPR, school-law or ethics limits.

Always add: this is a reading, not legal advice; funded work needs a written legal opinion.

## 3. Safeguards to check in any design

Minors: no biometrics by default; guardian consent and age-appropriate assent; refusal without disadvantage; state approval. Teachers: records are not used to evaluate individuals. Everyone: a named data steward, retention limits, a route to contest.

## 4. Generative-AI disclosure

Check the venue's or funder's current rule. Draft a truthful statement of what the tool did and confirm that the author checked all content and citations, e.g.: "Generative AI (Claude, Anthropic) was used to search and summarise literature, structure the argument and draft text. All content, citations and interpretations were checked by the author(s), who take full responsibility."

## Output

Problems first, by severity. Then the source table (citation → id → status → note). Never mark something verified unless it was read in this session or a prior record shows it was read.
