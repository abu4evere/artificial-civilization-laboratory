# PB0: independent blind recompute (4 November 2026, about 17:00)

**The inputs:** `recompute/pb0_outcomes.csv` (35,189 rows; built by `recompute/build_pb0_outcomes.py`) and
`recompute/prompt.txt`, each given in a fresh chat, with no analysis script and no earlier result. **The numbers below
are read from the replies.** In both chats the recomputer picked the winner itself, from replays 1–2.

| quantity | the study (`analyse_pb0.py`) | GPT (code) | Gemini 3.1 Pro (code) |
|---|---|---|---|
| decisions | 3,328 | 3,328 (32 worlds × 104) | 3,328 |
| G [95%] | +0.1592 [+0.1512, +0.1672] | 0.1592 [0.1513, 0.1672] | 0.1592 [0.1513, 0.1671] |
| A | 0.5074 | 0.5074 | 0.5074 |
| G / A | 0.314 | 31.36% | 0.3136 |
| reading | GO | GO | GO |
| share where the winner is not the top option | 85.4% (2,842 of 3,328; 486 the same) | 85.40% (2,842) | 85.4% |

**Note:**
- Bootstrap draws differ between implementations, so the interval ends differ in the fourth decimal.
- DeepSeek was not asked this time. The creator asked for fewer browser tabs, and its tab was closed before the
  question was sent. GPT and Gemini satisfy the rule.

**Both agree with the study.** PB0's reading, GO, stands. PB0 is final.
