# LD1: independent blind recompute (5 November 2026, 13:02)

**The inputs:**
- `recompute/ld1_counts.csv`, built by `recompute/build_ld1_counts.py`, written before data and amended with the
  plan (amendment 1);
- `recompute/prompt.txt`.

Each was given in a fresh chat, with no analysis script and no earlier result.
- GPT: chat 6aecc443, "Medium" thinking, with code.
- Gemini 3.1 Pro: chat be17babd6929dec1, with code.
- DeepSeek: chat 67041a65, DeepThink, no code tool. Its reply will be appended.

**The numbers below are read from the replies.** The time in the title is from the clock.

| quantity | the study | GPT (code) | Gemini 3.1 Pro (code) |
|---|---|---|---|
| make share: c actual, scale, none; c0 actual | 0.0011, 0.0074, 0.0064; 0.0080 | 0.0011, 0.0074, 0.0064; 0.0080 | 0.0011, 0.0074, 0.0064; 0.0080 |
| f_scale [95%] | 0.912 [0.842, 0.987] | 0.9124 [0.8415, 0.9861] | 0.9124 [0.8424, 0.9856] |
| f_none [95%] | 0.770 [0.706, 0.836] | 0.7702 [0.7043, 0.8339] | 0.7702 [0.7057, 0.8335] |
| reading A | direction (scale also recovers) | direction (both intervals above 0.5) | direction |
| c stages 0 / 1 / 3 | 0.116 / 0.882 / 0.002 | 11.65%... / 88.16% [83.08, 92.36] / 0.19% | 0.1165 [0.0741, 0.1676] / 0.8816 [0.8310, 0.9235] / 0.0019 |
| c0 stages 0 / 1 / 2, 3, 5 | 0.642 / 0.357 / 0.000 each | 64.19% [61.42, 66.69] / 35.73% [33.23, 38.52] / 0.03% each | 0.6419 [0.6136, 0.6666] / 0.3573 [0.3325, 0.3858] / 0.0003 each |
| largest stage | c: 1; c0: 0 | c: 1 (916 of 1,039); c0: 0 (7,290 of 11,357) | c: 1; c0: 0 |

**Both agree with the study.** The intervals differ only in the last digit, from different bootstrap streams; GPT
used seed 20261105, and the study used 20261116.

GPT notes that **3 kinds in c0 reached stage 5** (made again; 0.03%), against none in c. The study's table shows
this as 0.000 [0.000, 0.001]. The count is the same, rounded.

LD1's readings stand:
- **A: "direction" (the scale version also recovers)**;
- **B: v13 stage 1 (held the recipe, never its inputs)**;
- **B: c0 stage 0 (never held the recipe at a week's end)**.
