# CL1 — Independent recompute (GPT and Gemini, fresh chats, raw cells only, no analysis script)

**Input:** `cl1_cells.csv`, with 1,601 rows (world × era × action) and every raw sum, built from the 32 output JSONs.
GPT received it as a zip; Gemini received the CSV. The attachments were checked before sending.

**The prompt (the same text to both):** the sums and the exact split, and the tasks:
- for era 2: the common actions' terms, shares and largest term, with a bootstrap interval for C_talk;
- make's terms.

No analysis numbers were given.

Chats:
- GPT: https://chatgpt.com/c/6ae0a02d-37e8-83ea-9b50-f8c99a290517
- Gemini: https://gemini.google.com/app/c44f31acdb38e8f0

## GPT (27 October 2026; numbers read from its reply)
Computed with Python; 20,000 replicates. It verified that the terms sum to the bias (+0.418344106 and −0.565756729).

**Common actions** (n 11,034,243): q 1.122, G 0.704, q − G +0.418.

| term | value | share |
|---|---|---|
| C_td − G | −0.069 | −16.458% |
| **C_talk** | **+0.391 [0.371, 0.412]** | **93.427%** (largest) |
| C_carer | +0.089 | 21.214% |
| C_birth | +0.000 | 0.000% |
| C_paid | +0.008 | 1.817% |

**Make** (n 10,176): q 0.049, G 0.615, q − G −0.566.

| term | value |
|---|---|
| C_td − G | −0.606 |
| C_talk | +0.030 |
| C_carer | +0.011 |
| C_birth | 0 |
| C_paid | 0 |

**Against the analysis:** every number matches.

## Gemini (27 October 2026; numbers read from its reply)
Computed with Python; 1,000,000 replicates.

**Common actions** (n 11,034,243): q 1.122, G 0.704, q − G 0.418.

| term | value | share |
|---|---|---|
| C_td − G | −0.069 | −0.165 |
| **C_talk** | **0.391 [0.371, 0.411]** | **0.934** (largest; the share's interval is [0.882, 0.988]) |
| C_carer | 0.089 | 0.212 |
| C_birth | 0.000 | 0 |
| C_paid | 0.008 | 0.018 |

**Make** (n 10,176): q 0.049, G 0.615, q − G −0.566.

| term | value |
|---|---|
| C_td − G | −0.606 |
| C_talk | 0.030 |
| C_carer | 0.011 |
| C_birth | 0 |
| C_paid | 0 |

**Against the analysis:** every number matches. The upper bootstrap bound is 0.411 against 0.412, which is noise.

## Verdict
**The analysis, GPT and Gemini agree on every number:**
- copying in talk carries 0.93 of the common actions' over-valuation;
- make's under-valuation is own experience (−0.606).

The findings are final.
