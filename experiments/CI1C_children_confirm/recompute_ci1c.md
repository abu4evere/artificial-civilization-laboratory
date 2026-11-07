# CI1-C: independent blind recompute (6 November 2026, 19:29)

**The inputs:**
- `recompute/ci1c_counts.csv` (96 rows: 3 arms × 32 seeds), built by `recompute/build_ci1c_counts.py`, written before
  data;
- `recompute/prompt.txt`, also written before data.

Each was given in a fresh chat, with no analysis script and no earlier result. The prompt was sent at about 19:27.
- **GPT:** chat 6aee7050, "Medium" thinking, with code (10,000 paired resamples; its own seed 20261106).
- **Gemini:** chat 41ec8444159c3e8d, with code ("Show code").
- **DeepSeek:** chat d82b802a, no code tool. Its reply was still being worked by hand at the time of this file; see
  below.

**The numbers below are read from the replies.** The time in the title is from the clock.

| quantity | the study | GPT (code) | Gemini (code) |
|---|---|---|---|
| 1. starvation ratio | 0.9942 [0.8759, 1.1290] | 0.9942 [0.8781, 1.1320] | 0.9942 [0.8732, 1.1265] |
| 2. killing difference | −0.0021 [−0.0068, +0.0000] | −0.0021 [−0.0068, 0.0000] | −0.0021 [−0.0069, 0.0000] |
| 3. adult health difference | −0.0774 [−0.6739, +0.5498] | −0.0774 [−0.6814, 0.5264] | −0.0774 [−0.6740, 0.5481] |
| 4. living-weeks ratio | 0.9733 [0.8581, 1.0911] | 0.9733 [0.8581, 1.0931] | 0.9733 [0.8603, 1.0933] |
| 5. extinct (extra) | −2 | −2 [−5, 0] | −2 [−5, 0] |
| 6. child deaths ratio | 0.9259 [0.8097, 1.0697] | 0.9259 [0.8117, 1.0636] | 0.9259 [0.8100, 1.0703] |
| 7. child starvation ratio | 0.9447 [0.8054, 1.1058] | 0.9447 [0.8074, 1.1018] | 0.9447 [0.8064, 1.1037] |
| 8. gifts to kin's children ratio | 1.0221 [0.9339, 1.1305] | 1.0221 [0.9337, 1.1316] | 1.0221 [0.9345, 1.1347] |
| **9. co-primary LG − v14** | **+0.0221 [+0.0166, +0.0283]** | +0.0221 [0.0165, 0.0284] | 0.0221 [0.0165, 0.0283] |
| **10. co-primary LG − sham** | **+0.0218 [+0.0169, +0.0278]** | +0.0218 [0.0169, 0.0277] | 0.0218 [0.0168, 0.0277] |
| 11. remade LG − v14 (secondary) | +0.0073 [+0.0044, +0.0107] | +0.0073 [0.0043, 0.0107] | 0.0073 [0.0044, 0.0107] |
| 12. others share (v14, LG, sham) | 0, 0, 0 | 0, 0, 0 | 0, 0, 0 |
| guards raised | none | 0 of 8 | none |
| reading | **CONFIRMED** | CONFIRMED | confirmed |

GPT also gave the remade shares: v14 2/3,873 = 0.0005, LG 32/4,077 = 0.0078, the sham 0/3,583. It added that the
result "does not establish that the law produces broader cultural transmission" (the others share is 0).

**GPT and Gemini agree with the study, each with code.**
- Every point estimate matches to 4 decimals.
- Their intervals differ only in the third or fourth decimal.
- The reading is the same: **CI1-C confirms LG.** The findings are final.

**DeepSeek:** at 19:29 it was still summing the file by hand. Its working shows the same pooled shares:
- complete: v14 0.004131, LG 0.026245, the sham 0.004465;
- remade: 2 and 32;
- others: 0.

These come from its working, not a finished reply, and are not counted as a recompute. Its reply will be appended
when it comes.
