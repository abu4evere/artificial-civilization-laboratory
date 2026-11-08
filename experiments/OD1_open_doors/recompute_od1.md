# OD1 blind recompute (8 November 2026)

**What was sent:**
- the file: `recompute/od1_counts.csv`, from `recompute/build_od1_counts.py` on the cloud output (run 42457601901);
- the prompt: `recompute/prompt.txt`.

Each model got them in a fresh chat, without the analysis script or any earlier result. Every number below was read
from the model's reply.

## GPT (fresh chat https://chatgpt.com/c/6af042b2-8054-83e8-8ef8-1ebce72ebf76; "Instant"; code)

| guard (arm vs v16) | GPT, doors (o) | analysis, o | GPT, without D1 (p) | analysis, p | GPT, sham (x) | analysis, x |
|---|---|---|---|---|---|---|
| starvation ratio | 1.1469 [0.9935, 1.3415] | 1.1469 [0.9946, 1.3428] | 1.0723 [0.9564, 1.2042] | 1.0723 [0.9579, 1.2051] | 1.0955 [0.9513, 1.2492] | 1.0955 [0.9536, 1.2453] |
| killing difference | 0.0088 [-0.0023, 0.0238] | +0.0088 [-0.0023, +0.0236] | 0.0021 [-0.0050, 0.0095] | +0.0021 [-0.0048, +0.0093] | 0.0023 [-0.0048, 0.0102] | +0.0023 [-0.0047, +0.0103] |
| adult health difference | -0.3382 [-0.9072, 0.2015] | -0.3382 [-0.9036, +0.2044] | -0.1976 [-0.7600, 0.4103] | -0.1976 [-0.7516, +0.4063] | -0.2677 [-0.7810, 0.2547] | -0.2677 [-0.7698, +0.2409] |
| living-weeks ratio | 1.0096 [0.9077, 1.1222] | 1.0096 [0.9090, 1.1195] | 1.0367 [0.9399, 1.1503] | 1.0367 [0.9402, 1.1478] | 0.9954 [0.9061, 1.0963] | 0.9954 [0.9054, 1.0959] |
| extinct worlds, extra | -1 | -1 | -1 | -1 | 0 | 0 |
| child deaths ratio | 1.1728 [0.9642, 1.4364] | 1.1728 [0.9664, 1.4351] | 1.1219 [0.9545, 1.3246] | 1.1219 [0.9563, 1.3247] | 1.0619 [0.9179, 1.2430] | 1.0619 [0.9249, 1.2405] |
| child starvation ratio | 1.1864 [0.9241, 1.5322] | 1.1864 [0.9278, 1.5337] | 1.1514 [0.9217, 1.4504] | 1.1514 [0.9237, 1.4532] | 1.0190 [0.8296, 1.2619] | 1.0190 [0.8314, 1.2641] |
| kin-child gifts ratio | 1.0123 [0.9210, 1.1048] | 1.0123 [0.9206, 1.1018] | 0.9648 [0.8850, 1.0513] | 0.9648 [0.8863, 1.0523] | 1.0223 [0.9278, 1.1206] | 1.0223 [0.9288, 1.1183] |
| guards raised | 0 of 8 | none | 0 of 8 | none | 0 of 8 | none |

**Manipulation counts in o (GPT):**
- stand-ins 4,983 (99.7358 per 1,000 makes);
- over the old item limit 99,329; over the old material limit 1,125,147;
- made binders 5,765; made hammers 20,561;
- layered warmth 59,473; layered carrying 59,938.

All are the same as the analysis. In c and x, all are 0.

**GPT's reading:** "OD1 decision: Adopt all five doors, D1–D5. None qualifies as barely exercised." It also wrote:
"This is a pass under the predefined guard rules, not proof that the package has no adverse effects."

**GPT matches** every point estimate, every guard and the reading. The intervals differ in the last digits, as
bootstrap draws do.

## Gemini (fresh chat https://gemini.google.com/app/b6cf3b71b5085e1b; Pro, High; code)
An earlier chat (ebb4b966c47052c7) only wrote a script. Asked to run it, it said its "code execution capabilities are
currently exhausted for this session". A new chat with the same file and prompt ran the code. Only numbers read from
that reply are recorded.

| guard (arm vs v16) | Gemini, o | Gemini, p | Gemini, x |
|---|---|---|---|
| starvation ratio | 1.1469 (0.9941, 1.3442) | 1.0723 (0.9552, 1.2089) | 1.0955 (0.9534, 1.2478) |
| killing difference | 0.0088 (-0.0024, 0.0234) | 0.0021 (-0.0050, 0.0095) | 0.0023 (-0.0048, 0.0101) |
| adult health difference | -0.3382 (-0.9080, 0.2098) | -0.1976 (-0.7564, 0.4106) | -0.2677 (-0.7769, 0.2442) |
| living-weeks ratio | 1.0096 (0.9088, 1.1193) | 1.0367 (0.9394, 1.1471) | 0.9954 (0.9035, 1.0917) |
| extinct worlds, difference | -1.0000 | -1.0000 | 0.0000 |
| child deaths ratio | 1.1728 (0.9695, 1.4414) | 1.1219 (0.9515, 1.3238) | 1.0619 (0.9233, 1.2387) |
| child starvation ratio | 1.1864 (0.9257, 1.5422) | 1.1514 (0.9223, 1.4498) | 1.0190 (0.8317, 1.2572) |
| kin-child gifts ratio | 1.0123 (0.9190, 1.1025) | 0.9648 (0.8872, 1.0527) | 1.0223 (0.9286, 1.1188) |
| guards raised | "None" | "None" | "None" |

**Manipulation counts in o (Gemini):**
- stand-ins 4,983 (99.7358 per 1,000 makes);
- over the old item limit 99,329; over the old material limit 1,125,147;
- made binders 5,765; made hammers 20,561;
- layered warmth 59,473; layered carrying 59,938.

**Gemini's reading:** "Arm O goes live because it raises zero experimental guards." "No doors are barely exercised."

**Gemini matches** every point estimate, every guard and the reading.

## Verdict
GPT and Gemini both match the frozen analysis in every point estimate, every guard and the reading: the full package
(o) goes live; no door is barely exercised. **The findings are final.**
