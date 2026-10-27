# MO1 — Independent recompute (GPT and Gemini, fresh chats, raw files only, no analysis script)

**Input:** two files built from the 96 output JSONs:
- `mo1_counts.csv`: one row per world, every raw counter;
- `mo1_census.csv`: 19,072 world-year rows.

GPT received both in a zip; Gemini received the two CSVs. The attachments were checked before sending.

**The prompt (the same text to both):** the definitions of M, P1, P2 and P3, the paired world bootstrap, and the frozen
rule, applied verbatim. No analysis numbers were given.

Chats:
- GPT: https://chatgpt.com/c/6ae07d7b-def0-83ea-a32a-3e0945698faa
- Gemini: https://gemini.google.com/app/39495c78ae230348

## GPT (27 October 2026; numbers read from its reply)
Computed with Python. It checked 96 count rows, 32 per arm, on the same seeds. It ran 20,000 paired replicates.

| measure | c | o | s | o − c [95%] |
|---|---|---|---|---|
| M | 0.2962 | 0.8365 | 0.3032 | +0.5403 [0.4939, 0.6010] |
| P1 | 0.6719 | 0.9149 | 0.6790 | +0.2430 [0.2191, 0.2727] |
| P2 | 9.3349 | 9.1421 | 9.4463 | −0.1929 [−0.3142, −0.0629] |
| P3 | 0 | 0 | 0 | 0 [0, 0] |

**Rule:**
- M **fails** (o 0.8365 < 0.90);
- P1 passes;
- P2 passes (the bound is −0.4667);
- P3 passes.

**"Final decision: MO1 does not support the change under its frozen four-part rule."**

**Against the analysis:** every number and the verdict match. The bootstrap bounds agree within noise.

## Gemini (27 October 2026; numbers read from its reply)
Computed with Python. It ran 100,000 paired replicates.

| measure | c | o | s | o − c [95%] |
|---|---|---|---|---|
| M | 13,980 / 47,196 = 0.2962 | 36,069 / 43,118 = 0.8365 | 13,005 / 42,890 = 0.3032 | +0.5403 [0.4943, 0.6009] |
| P1 | 59,231 / 88,155 = 0.6719 | 74,412 / 81,336 = 0.9149 | 54,616 / 80,432 = 0.6790 | +0.2430 [0.2194, 0.2723] |
| P2 | 9.3349 | 9.1421 | 9.4463 | −0.1929 [−0.3147, −0.0602] |
| P3 | 0 | 0 | 0 | 0 [0, 0] |

**Rule:**
- M **FAILED** (o 0.8365 < 0.90);
- P1 passed;
- P2 passed (−0.3147 > −0.4667);
- P3 passed.

**"The change is NOT supported because criterion M fails."**

**Against the analysis:** every number and the verdict match.

## Verdict
**The analysis, GPT and Gemini agree on every number and on the verdict: not supported** (M fails). The findings are
final.
