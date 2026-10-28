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

## Gemini (pending)
- **First attempt:** an error ("I encountered an error doing what you asked").
- **Retry:** "The direct execution environment is currently unavailable." It returned a Python script instead of
  numbers.

**The script is not run by the assistant.** Running it would make the result the assistant's computation, not an
independent one. Gemini's recompute will be retried in a fresh chat, and **PG0 is not final until its numbers are read
from its reply.**
