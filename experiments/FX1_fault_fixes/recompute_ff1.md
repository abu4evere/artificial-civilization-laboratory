# FF1 (folder FX1_fault_fixes): independent blind recompute (3 November 2026)

- **Input:** `recompute/fx1_counts.csv` (160 rows). Per arm and world: living weeks, extinction, kinds invented in years
  100–195 and how many were remade within five years. It was built by `recompute/build_fx1_counts.py`, written before
  data.
- **The exact text sent:** `recompute/prompt.txt`, written and committed before the data existed. It calls the study
  "FX1", its name when frozen. The CSV was attached as a file.
- **Who** (each a fresh chat; none saw the analysis script or any earlier result):
  - GPT, chat `6ae98bab`: Python, 10,000 draws;
  - Gemini 3.1 Pro (High), chat `c26932d23dea0964`: it ran code. Its first try was cut off by an Escape key the
    assistant sent, and the same prompt was then sent again in the same chat;
  - DeepSeek, chat `22ef6243`: no code tool. Its sums match exactly, and its intervals are its own approximation.
- **Recorded only from their actual replies.**

| quantity | analyse_fx1.py | GPT | Gemini | DeepSeek |
|---|---|---|---|---|
| f / v11 | 1.0003 [0.8926, 1.1301] | 1.0003 [0.8899, 1.1303] | 1.0003 [0.8933, 1.1251] | 1.0003 (0.8839, 1.1167) |
| f1 / v11 | 1.1040 [0.9840, 1.2631] | 1.1040 [0.9833, 1.2626] | 1.1040 [0.9866, 1.2661] | 1.1040 (0.9687, 1.2393) |
| f23 / v11 | 1.0737 [0.9843, 1.1855] | 1.0737 [0.9856, 1.1857] | 1.0737 [0.9859, 1.1865] | 1.0737 (0.9755, 1.1719) |
| sham / v11 | 1.0307 [0.9155, 1.1636] | 1.0307 [0.9189, 1.1607] | 1.0307 [0.9165, 1.1616] | 1.0307 (0.9097, 1.1517) |
| extinct worlds (v11, f, f1, f23, sham) | 1, 1, 0, 0, 1 | the same | the same | the same |
| reading | no harm | no harm | no harm | no harm |
| R per arm | 0.0003, 0.0003, 0.0000, 0.0000, 0.0003 | the same (1/3,378, 1/3,429, 0/3,413, 0/3,558, 1/3,432) | the same | the same (same sums) |

- **GPT's note:** "the population interval includes meaningful decreases as well as increases, so this does not
  establish equivalence or prove that harm is impossible." This is right, and it is what the frozen harm-only rule
  accepts. The guard asks only that harm is not shown.
- **All three agree with the analysis** on every point value, the extinct counts and the reading. GPT's and Gemini's
  interval ends differ by at most 0.005. DeepSeek's approximate ends differ by up to 0.024.

**FF1 is final: no harm.**

**The browser tabs:** the GPT and Gemini tabs were closed. When the second one closed, the tab group dissolved, so the
DeepSeek tab may still be open outside the assistant's group, where it cannot close it.
