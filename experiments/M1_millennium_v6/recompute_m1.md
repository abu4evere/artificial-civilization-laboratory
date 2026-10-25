# M1: independent recompute (25 October 2026)

**Who:** GPT, in a fresh ChatGPT chat (https://chatgpt.com/c/6ade92c6-2ba0-83ea-9a0a-439642f2645b) with no ACL history.
**Given:** the 192 raw output files (zip) and a description of the fields and of the frozen definitions. **Not given:**
`analyse_m1.py`, `results.md` or any of our numbers. GPT wrote and ran its own Python.

| number | `analyse_m1.py` | GPT's recompute | match |
|---|---|---|---|
| files, fingerprints | 192, one (`424c9677…`) | 192, one, before = after | yes |
| alive at year 1,000: LP / D80 / C20 | 45 / 24 / 16 | 45 / 24 / 16 | yes |
| A4 LP: early, late, ratio [95%] | 0.9167, 0.04938, 0.054 [0.046, 0.063] | 0.91671, 0.04938, 0.05387 [0.04556, 0.06356] | yes |
| A4 D80 ratio | 0.038 [0.028, 0.050] | 0.03827 [0.02863, 0.04982] | yes |
| A4 C20 ratio | 0.039 [0.027, 0.055] | 0.03888 [0.02748, 0.05544] | yes |
| B-retained LP: worlds, early, late | 18, 0.1373, 0 | 18, 0.13731, 0 | yes |
| B-retained D80 / C20 | 6 and 3 worlds, late 0 | 6 and 3 worlds, late 0 | yes |

**GPT's caveat, recorded:** the late zero rests on few cases. Only **35 late kinds** qualified across the three arms
(25 LP, 7 D80, 3 C20), and all 35 were unknown 25 years after their maker's death. Many surviving worlds had no
qualifying kind in one era. The decline is clear in the eligible worlds, but the late estimate is thin, and the
[0, 0] interval should not be read as precise for all worlds.

**The recompute agrees on every number. M1's findings stand as final, with the caveat above.**
