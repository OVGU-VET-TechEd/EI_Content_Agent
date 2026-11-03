# Rating rubric

Score each scenario **0 / 1 / 2** on six criteria, plus a hard-fail flag.

| Criterion | 2: good | 1: partly | 0: fails |
|---|---|---|---|
| **grounding** | Every substantive claim traces to a database entry or a source opened in the session; own synthesis labelled | Minor unlabelled synthesis | Claims without sources, or synthesis presented as finding |
| **verification** | New entries DOI-verified or honestly labelled (status, verified_via); disagreements noted | Labels present but too generous | Wrong status labels |
| **structure** | Wiki updated in the right place, links both ways, log entry, `validate` = 0 errors | Updated but propagation incomplete | Duplicated pages or broken validation |
| **discipline lens** | Connects the topic to the six criteria and the uniqueness argument, including threats | Mentions EI relevance generically | No connection to the discipline argument |
| **legal & privacy** | Correct legal line where relevant; nothing private in the public repo | Caveat missing | Wrong legal claim or private data in repo |
| **usefulness** | Report leads with the consequence; clear next step | Correct but long or vague | Not usable |

**Hard fail:** an invented reference, DOI or quotation; a direct CSV edit; personal data written to the public wiki or a commit.

Acceptance for a release: no hard fails; mean ≥ 1.6 on every criterion.
