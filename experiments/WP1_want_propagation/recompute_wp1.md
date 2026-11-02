# WP1 — independent blind recompute (2 November 2026)

- **Input:** `recompute/wp1_counts.csv` (128 rows): per arm and world, the kinds invented in years 100–195, how many
  were remade within five years, the living weeks and extinction. Built by `recompute/build_wp1_counts.py`, written
  before data.
- **The exact text sent:** `recompute/prompt.txt`, written and committed before the data existed. The CSV was attached
  as a file.
- **Who:** GPT (fresh chat `6ae8d65a`) and Gemini (on Flash, fresh chat `5e42b2fdb9b18722`, which returned "I
  encountered an error"; then on 3.1 Pro, chat `8a14af5997ab7e3f`). Neither saw the analysis script or any earlier result.
- **Recorded only from their actual replies.**

| quantity | analyse_wp1.py | GPT | Gemini |
|---|---|---|---|
| R: v11 / A1 / A2 / sham | 0.0000 / 0.0003 / 0.0000 / 0.0003 | 0.0000 / 0.0003 / 0.0000 / 0.0003 (0/3,575, 1/3,564, 0/3,760, 1/3,621) | 0.0000 / 0.0003 / 0.0000 / 0.0003 |
| A1 − v11 | +0.0003 [+0.0000, +0.0009] | +0.000281 [0.000000, 0.000875] | +0.0003 [0.0000, 0.0009] |
| A2 − v11 | +0.0000 [+0.0000, +0.0000] | 0.000000 [0.000000, 0.000000] | 0.0000 [0.0000, 0.0000] |
| A2 − A1 | −0.0003 [−0.0009, +0.0000] | −0.000281 [−0.000875, 0.000000] | −0.0003 [−0.0009, 0.0000] |
| sham − v11 | +0.0003 [+0.0000, +0.0009] | +0.000276 [0.000000, 0.000929] | +0.0003 [0.0000, 0.0009] |
| A1 − sham | +0.0000 [−0.0009, +0.0008] | +0.000004 [−0.000854, 0.000787] | 0.0000 [−0.0009, 0.0008] |
| A2 − sham | −0.0003 [−0.0009, +0.0000] | −0.000276 [−0.000929, 0.000000] | −0.0003 [−0.0009, 0.0000] |
| readings | A1 inconclusive; A2 inconclusive; A2 adds: no | the same | the same |
| population ÷ v11 | A1 1.068 [0.971, 1.184]; A2 1.120 [0.995, 1.261] | A1 1.0683 [0.9708, 1.1837]; A2 1.1198 [0.9943, 1.2629] | A1 1.0683 [0.9709, 1.1872]; A2 1.1198 [0.9960, 1.2684] |
| guards | none raised | none raised | none raised |

- **GPT's note:** "Only two remakes occurred across all 128 arm-world observations: one in A1 (seed 22220) and one in
  sham (seed 22222)."
- **GPT and the analysis agree** on every point value, reading and guard. The interval ends differ by at most 0.0003.
- **Gemini (3.1 Pro) and the analysis agree** on every point value, reading and guard. The interval ends differ by at
  most 0.004 (A1's population ratio).

**All three agree: A1 inconclusive, A2 inconclusive, no guard raised. WP1 is final.** Both chat tabs were closed
afterwards.
