# VC1 — Independent recompute (GPT and Gemini, fresh chats, raw cells only, no analysis script)

**Input:** `vc1_cells.csv`, with 1,581 rows (world × era × action) and every raw sum, built from the 32 output JSONs.
GPT received it as a zip; Gemini received the CSV. The attachments were checked before sending.

**The prompt (the same text to both):** the definitions, and the tasks:
- for era 2: make and the common actions pooled (n, mean q, mean G, bias, mean gap);
- make's bias minus the common bias, with a world bootstrap;
- the gap share;
- the per-action bias.

No analysis numbers were given.

Chats:
- GPT: https://chatgpt.com/c/6ae08d39-e2fc-83e8-8385-135e1818f613
- Gemini: https://gemini.google.com/app/c4ce3d394c5941d2

## GPT (27 October 2026; numbers read from its reply)
Computed with Python; 20,000 replicates.

| | n | mean q | mean G | bias | mean gap |
|---|---|---|---|---|---|
| make | 8,929 | 0.046 | 0.604 | −0.558 | 0.124 |
| common | 9,743,097 | 1.125 | 0.708 | +0.418 | 0.145 |

- **Difference:** −0.975 [−0.990, −0.959].
- **Gap share:** 0.347.
- **Per action:** make −0.558, forage +0.440, give +0.471, talk +0.359, gather +0.381.

## Gemini (27 October 2026; numbers read from its reply)
Computed with Python; 200,000 replicates.

| | n | mean q | mean G | bias | mean gap |
|---|---|---|---|---|---|
| make | 8,929 | 0.046 | 0.604 | −0.558 | 0.124 |
| common | 9,743,097 | 1.125 | 0.708 | 0.418 | 0.145 |

- **Difference:** −0.975 [−0.990, −0.959].
- **Gap share:** 0.347.
- **Per action:** make −0.558, forage 0.440, give 0.471, talk 0.359, gather 0.381.

## Verdict
**The analysis, GPT and Gemini agree on every number** (the analysis's interval is [−0.990, −0.958], the same within
bootstrap noise). The findings are final.
