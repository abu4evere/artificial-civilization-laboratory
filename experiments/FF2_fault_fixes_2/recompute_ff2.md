# FF2: independent blind recompute (3 November 2026, about 20:10)

**The inputs:** `recompute/ff2_counts.csv` (built by `recompute/build_ff2_counts.py`) and `recompute/prompt.txt`, each
given in a fresh chat, with no analysis script and no earlier result. **The numbers below are read from the replies.**

| quantity | the study (`analyse_ff2.py`) | GPT (code) | Gemini 3.1 Pro (code) | DeepSeek (by hand, no code) |
|---|---|---|---|---|
| R = living-weeks f / v12 | 1.0008 [0.8893, 1.1203] | 1.0008 [0.8928, 1.1192] | 1.0008 [0.8913, 1.1241] | 1.0008 (1.000823); no interval, as asked |
| extinct worlds: c, f, f8, f4, f5, x | 0, 0, 0, 0, 1, 0 | the same | the same | the same |
| f − c extinct | 0 | 0 | 0 | 0 |
| reading | no harm | no harm | no harm | no harm |
| adult hunter-weeks per 1,000 adult-weeks: c / f / f8 / f4 / f5 / x | 0.1375 / 0.1085 / 0.1039 / 0.1438 / 0.1436 / 0.1409 | the same | 0.14 / 0.11 / 0.10 / 0.14 / 0.14 / 0.14 (rounded) | 0.1375355 / 0.1084927 / 0.1038850 / 0.1438212 / 0.1435744 / 0.1408655 |
| hunter-weeks ratio f / c | 0.7888 [0.7128, 0.8835] | 0.7888 [0.7141, 0.8849] | 0.7888 [0.7148, 0.8839] | (not given as a ratio; the per-arm values imply 0.7888) |

**Note:** bootstrap draws differ between implementations, so the interval ends differ in the third decimal. That is
expected. Every point value and every reading agrees.

**All three agree with the study.** FF2's reading, "no harm", stands. FF2 is final.
