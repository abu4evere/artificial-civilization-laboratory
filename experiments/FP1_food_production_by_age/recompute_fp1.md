# FP1: independent blind recompute (7 November 2026, 02:39)

**The inputs:**
- `recompute/fp1_counts.csv` (512 rows: 32 worlds × 8 age bands × 2 sexes), built by `recompute/build_fp1_counts.py`,
  written before data;
- `recompute/prompt.txt`, also written before data.

Each was given in a fresh chat, with no analysis script and no earlier result.
- **GPT:** chat 6aeed507, "Medium" thinking, with code ("Analyzed"; 10,000 world-bootstrap replicates).
- **Gemini:** chat b0e18a83894afda1, with code ("Show code").
- **DeepSeek:** chat 9128e479, no code tool. It replied that it "can't execute code" and so "can't truthfully paste
  computed numeric outputs", and gave a Python script instead (not run). No numbers came from it.

**The numbers below are read from the replies.** The time in the title is from the clock.

| quantity | the study | GPT (code) | Gemini (code) |
|---|---|---|---|
| production ÷ need, F: 0–2 / 3–7 / 8–11 / 12–15 | 0.000 / 0.442 / 1.207 / 1.101 | the same, every interval the same | the same |
| F: 16–29 / 30–39 / 40–49 / 50+ | 1.192 / 1.333 / 1.312 / 1.053 | the same | the same (40–49 [1.300, 1.324] against [1.301, 1.324]) |
| M: 0–2 / 3–7 / 8–11 / 12–15 | 0.000 / 0.442 / 1.207 / 1.101 | the same | the same |
| M: 16–29 / 30–39 / 40–49 / 50+ | 1.098 / 1.105 / 1.097 / 1.054 | the same | the same |
| crossover F; M | 8–11; 8–11 | 8–11; 8–11 (in all 10,000 replicates) | 8–11; 8–11 |
| 30–39 F: all weeks; per active week; active share | 1.333; 2.931 [2.905, 2.960]; 0.453 | the same | 1.333; 2.931 [2.905, 2.961]; 0.453 |
| 40–49 F | 1.312; 2.962; 0.442 | the same | the same |
| 30–39 M | 1.105; 3.010 [2.976, 3.046]; 0.367 | the same | 1.105; 3.010 [2.977, 3.047]; 0.367 |
| 40–49 M | 1.097; 3.018; 0.363 | the same | 1.097; 3.018 [2.985, 3.055]; 0.363 |
| hunted share of production | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| grown (16+) production per person-week | 7.743 (a script on the counts file, 02:39) | 7.743 [7.711, 7.770] | 7.743 [7.711, 7.770] |

**GPT and Gemini agree with the study in every point estimate,** each with code. Their intervals differ in the third
decimal at most. FP1's table stands. The findings are final.
