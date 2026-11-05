# PB1: independent blind recompute (4 November 2026, about 22:00)

**The inputs:** `recompute/pb1_sums.csv` (built by `recompute/build_pb1_sums.py`) and `recompute/prompt.txt`, each
given in a fresh chat, with no analysis script and no earlier result. **The numbers below are read from the replies.**

| quantity | the study (`analyse_pb1.py`) | GPT (code) | Gemini 3.1 Pro (code) |
|---|---|---|---|
| primary skill of L-own against B [95%] | −0.2017 [−0.2119, −0.1919] | −0.2017 [−0.2123, −0.1916] | −0.2017 [−0.2119, −0.1917] |
| reading | it does not | it does not | it does not |
| secondary skill (property combinations) [95%] | −0.0676 [−0.0788, −0.0560] | −0.0676 [−0.0787, −0.0556] | −0.0676 [−0.0789, −0.0558] |
| cases (primary, secondary) | 226,685; 81,801 | the same | the same |

**Note:** bootstrap draws differ between implementations, so the interval ends differ in the fourth decimal. DeepSeek
was not asked, to keep browser tabs few (the creator's request); GPT and Gemini satisfy the rule.

**Both agree with the study.** PB1's reading, "it does not", stands. PB1 is final.
