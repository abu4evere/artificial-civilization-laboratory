# HC1 — Independent recompute (GPT and Gemini, fresh chats, raw files only, no analysis script)

**Input:** two files built from the 96 output JSONs:
- `hc1_cells.csv`: 4,799 rows (world × era × action), with sums n, q, G;
- `hc1_census.csv`: 19,185 world-years.

GPT received both in a zip; Gemini received the two CSVs. The attachments were checked before sending.

**The prompt (the same text to both):** the definitions, the paired bootstrap, and the frozen rule, applied verbatim.
No analysis numbers were given.

Chats:
- GPT: https://chatgpt.com/c/6ae0f33a-f68c-83e9-b678-5eed28dc6a84
- Gemini: https://gemini.google.com/app/931d7f172a61d869

## GPT (27 October 2026; numbers read from its reply)
Computed with Python; 10,000 replicates.

| | w | s | x |
|---|---|---|---|
| common actions' bias | 0.4235 | 0.4358 | 0.4251 |
| make bias | −0.5706 | −0.5651 | −0.5726 |
| mean G, all actions | 0.6836 | 0.6733 | 0.6795 |
| mean population, years 100–199 | 130.9138 | 121.9516 | 119.7196 |

- **Improvement w − s:** −0.0123 [−0.0213, −0.0040].
- **Mean G, s − w:** −0.0103 [−0.0233, 0.0024].
- **Population ratio:** 0.9315 (no flag).
- It noted that the sham has 3,185 census rows (one world ended early).
- **"HC1 is not supported under the preregistered decision rule."**

## Gemini (27 October 2026; numbers read from its reply)
Computed with Python; 100,000 replicates.

| | w | s | x |
|---|---|---|---|
| common actions' bias | 0.4235 | 0.4358 | 0.4251 |
| make bias | −0.5707 | −0.5651 | −0.5726 |
| mean G, all actions | 0.6836 | 0.6733 | 0.6795 |

- **Improvement w − s:** −0.0123 [−0.0212, −0.0039].
- **Mean G, s − w:** −0.0103 [−0.0235, 0.0024].
- **Population:** w 130.9138 (418,924 / 3,200), s 121.9516 (390,245 / 3,200), x 119.7196 (381,307 / 3,185); ratio
  0.9315 (no flag).
- **"Verdict: Not supported."**

## Verdict
**The analysis, GPT and Gemini agree on every number and on the verdict: not supported.** The findings are final.
