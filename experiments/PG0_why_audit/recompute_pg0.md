# PG0 — Independent recompute (GPT and Gemini, fresh chats, raw counts only, no analysis script)

**Input:** `pg0_counts.csv`, one row per world (32), with every raw counter, built from the output JSONs. GPT received
it as a zip; Gemini received the CSV. The attachments were checked before sending.

**The prompt (the same text to both):** the definitions and the tasks:
- (1) the puzzle-led share, and new-to-world kinds per play (led minus free), with a world bootstrap;
- (2) the three predictors' mean errors, and shuffled minus nearest-neighbours, with a world bootstrap;
- (3) the share of new useful kinds lost before use.

No analysis numbers were given.

Chats:
- GPT: https://chatgpt.com/c/6ae14aa6-c0ac-83e9-95e7-d8cf501b5604
- Gemini: https://gemini.google.com/app/ff7014e97124ac22

## GPT (27 October 2026; numbers read from its reply)
Computed with Python; 20,000 replicates.
- **(1)** puzzle-led 291 of 397,147 (0.0007); new-to-world kinds per play: led 0.1375, free 0.1009; led − free
  **+0.0365 [0.0028, 0.0727].**
- **(2)** mean absolute error: nearest-neighbours **0.0717**, shuffled **0.1053**, zero 0.1522; shuffled − nearest
  **+0.0337 [0.0329, 0.0343]** (85,136 first uses).
- **(3)** lost before use: 9,939 + 171 of 40,093 = **0.2522.**

**Against the analysis:** every number matches.

## Gemini (27 October 2026; numbers read from its reply, third attempt, chat https://gemini.google.com/app/bb0b1f16926f5fad)
The first two attempts failed: a tool error, then a script returned instead of numbers (`recompute_pg0.md` history).
The third computed the results, with the exact sums shown, and 100,000 replicates.
- **(1)** puzzle-led 291 / 397,147 ≈ 0.0007; led 40 / 291 = 0.1375; free 40,059 / 396,856 = 0.1009; led − free
  **0.0365 [0.0026, 0.0722].**
- **(2)** 85,136 first uses; nearest-neighbours 6,100.3534 / 85,136 = **0.0717**; shuffled 8,965.2441 / 85,136 =
  **0.1053**; zero 12,961.7649 / 85,136 = 0.1522; shuffled − nearest **0.0337 [0.0329, 0.0343].**
- **(3)** (9,939 + 171) / 40,093 = **0.2522.**

**Against the analysis:** every number matches.

## Verdict
**The analysis, GPT and Gemini agree on every number.** The findings are final.
