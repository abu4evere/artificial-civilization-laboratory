# TR1 — independent blind recompute (31 October 2026)

- **Input:** `recompute/tr1_one_file.csv`, per-world sums from run 2's raw output JSONs (32 worlds). It was built by
  `recompute/build_tr1_one_file.py`, written before data.
- **Who:** GPT (fresh chat `6ae5ec8a`) and Gemini (fresh chat `c87d999aa5203d58`). Each got the same text, with the
  columns and the frozen rule. Neither saw `analyse_tr1.py` or any earlier result.
- **Recorded only from their actual replies.**

| quantity | analyse_tr1.py | GPT | Gemini |
|---|---|---|---|
| R, realized share of foraged food added by tools | 0.010 [0.010, 0.011] (0.0104) | 0.010 [0.010, 0.011] (0.010430) | 0.010 [0.010, 0.011] |
| H, headroom with the world's best tool | 0.200 [0.195, 0.204] (0.1996) | 0.200 [0.195, 0.204] (0.199572) | 0.200 [0.195, 0.204] |
| A, headroom with the best tool the forager knows | 0.127 (0.1273) | 0.127 (0.127268) | 0.127 |
| frozen reading | knowing matters but is unused | same | same |

- **Totals (Gemini):** with 127,116,518.791; without 125,790,708.972; world's best 152,485,642.825; known best
  143,294,326.697.
- **GPT's caution:** these are "counterfactual improvements for the same forage actions, not predictions of changes
  in overall food production".

**All three agree on every number and on the reading. TR1 is final.**
