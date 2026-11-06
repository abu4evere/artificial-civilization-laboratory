# VA1: independent blind recompute (5 November 2026, 21:34)

**The inputs:**
- `recompute/va1_kinds.csv` (1,194 rows, one per new kind), built by `recompute/build_va1_kinds.py`, which was
  written before data;
- `recompute/prompt.txt`.

Each was given in a fresh chat, with no analysis script and no earlier result.
- GPT: chat 6aed39bb, "Medium" thinking, with code ("Worked for 10m 57s").
- Gemini (Flash, High): chat e2ea644606a979ee, with code.
- DeepSeek: chat a6401531, no code tool. It said so and wrote "I won't invent numeric results"; it gave a Python script
  instead, written from the prompt and the CSV alone. The assistant ran that script unchanged (only the indentation,
  lost in the page copy, was restored): `recompute/deepseek_script_va1.py`, output in
  `recompute/deepseek_script_va1_output.txt` (run 21:27–21:28).

**The numbers below are read from the replies and from that output.** The time in the title is from the clock.

| quantity | the study | GPT (code) | Gemini (code) | DeepSeek's script (run here) |
|---|---|---|---|---|
| 1. used before lost | 0.824 [0.788, 0.858] | 0.8241 [0.7882, 0.8577]; 984 of 1,194 | 0.8241 [0.7880, 0.8575]; 984 of 1,194 | 0.8241 [0.7882, 0.8569] |
| reading 1 | not shown | not supported | not met | not shown |
| 2. actual survival | 0.871 [0.835, 0.905] | 0.8710 [0.8356, 0.9040]; 1,040 of 1,194 | 0.8710 [0.8357, 0.9033] | 0.8710 [0.8348, 0.9040] |
| 2. v_first | 0.998 [0.995, 1.000] | 0.9982 [0.9947, 1.0000]; 1,139 of 1,141 | 0.9982 [0.9947, 1.0000] | 0.9982 [0.9947, 1.0000] |
| 2. v_sim (no reading) | 1.000 [1.000, 1.000] | 1.0000; 1,188 of 1,188 | 1.0000; 1,188 of 1,188 | 1.0000 [1.0000, 1.0000] |
| 3. corr(v_sim, first felt) | 0.297 [0.245, 0.350]; 1,135 kinds | 0.2970 [0.2443, 0.3494]; 1,135 | 0.2970 [0.2446, 0.3498]; 1,135 | 0.2970 [0.2446, 0.3496] |
| 3. corr(v_mean, first felt) | 0.267 | 0.2669 | 0.2669 | 0.2669 |
| reading 3 | similar experience is informative | supported | similar experience is informative | similar experience is informative |

**All three agree with the study.** Every point estimate matches to the digits shown. The intervals differ only in
the third or fourth decimal, from different bootstrap streams.

**One difference in method, of no consequence here:** GPT (like the study) drew 32 worlds, counting seed 23703 (which
died out and has no kinds) as a world with none. DeepSeek's script drew from the 31 worlds present in the file.
Gemini did not say which. The intervals barely move.

**The models' own remarks (opinions, not sign-off):**
- GPT: the similarity-weighted value's advantage over the plain mean (0.0301) "does not independently establish that
  the difference between correlations is statistically significant". That is right. The frozen rule asked only for
  the point estimate (amendment 1), and the findings already call the margin small.
- GPT: the counterfactual survival shares "are descriptive, not evidence that applying the alternatives would cause
  those outcomes". Also right, and already in `questions.md`'s known limits.
- DeepSeek, in its reasoning, noticed that `held_first_week` is 0 almost exactly when `full` is 1. Checked: 154 of 155
  kinds invented with a full memory were gone by the first week's end, and 1,039 of 1,039 with room were kept. See the
  appended note in `findings.md`.

**VA1's readings stand:** "unvalued at birth dominates" is not shown; "similar experience is informative" (modestly).
The findings are final.
