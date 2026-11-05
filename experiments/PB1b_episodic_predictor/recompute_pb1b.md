# PB1b: independent blind recompute (4 November 2026, about 23:13; corrected from an estimated "23:40")

**The inputs:** `recompute/pb1b_sums.csv` (built by `recompute/build_pb1b_sums.py`) and `recompute/prompt.txt`, each
given in a fresh chat, with no analysis script and no earlier result. **The numbers below are read from the replies.**

| quantity | the study | GPT (code) | Gemini 3.1 Pro (code) |
|---|---|---|---|
| E-own, unfamiliar [95%] | +0.0092 [+0.0081, +0.0103] | 0.0092 [0.0081, 0.0103] | 0.0092 [0.0081, 0.0103] |
| E-own, familiar | +0.0000 | 0.0000 [0.0000, 0.0000] | 0.0000 [0.0000, 0.0000] |
| E-obs, unfamiliar | +0.0839 [+0.0774, +0.0904] | 0.0839 [0.0776, 0.0904] | 0.0839 [0.0777, 0.0904] |
| E-obs, familiar | +0.0319 [+0.0309, +0.0328] | 0.0319 [0.0309, 0.0328] | 0.0319 [0.0309, 0.0328] |
| readings | E-own GO; E-obs passes | both GO | both GO |
| E-obs − E-own, unfamiliar | +0.0747 [+0.0684, +0.0812] | +0.0747 [0.0685, 0.0811] | 0.0747 [0.0685, 0.0811] |
| cases | 255,389; 3,826,129 | — | 255,389; 3,826,129 |

**Note:** DeepSeek was not asked, to keep tabs few. **Both agree with the study.** PB1b's reading, GO, stands.
PB1b is final.
