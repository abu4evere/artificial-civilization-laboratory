# HD1 — independent blind recompute (31 October 2026)

- **Input:** `recompute/hd1_one_file.csv`, per-world, per-arm sums from the raw output JSONs (32 paired seeds × 3
  arms).
- **Who:** GPT (fresh chat `6ae64ef9`) and Gemini (fresh chat `ed86021013cba8ea`). Each got the same text, with the
  columns and the frozen rule (no-harm flags excluded, as stated). Neither saw `analyse_hd1.py` or any earlier result.
- **Recorded only from their actual replies.**

| quantity | analyse_hd1.py | GPT | Gemini |
|---|---|---|---|
| R v10 | 0.0107 | 0.0107 (1.0670%) | 0.0107 (0.010670) |
| R h | 0.0143 | 0.0143 (1.4280%) | 0.0143 (0.014280) |
| R sham | 0.0114 | 0.0114 (1.1365%) | 0.0114 (0.011365) |
| D_h = h − v10 | +0.0036 [+0.0028, +0.0045] | +0.0036 [0.0028, 0.0045] | 0.0036 (0.003610) [0.0028, 0.0045] |
| D_sham = sham − v10 | +0.0007 [−0.0000, +0.0014] | +0.0007 [−0.0000, 0.0014] | 0.0007 (0.000695) [0.0000, 0.0014] |
| reading | supported | supported | supported |

- **The sham interval's lower bound differs in the fifth decimal:**
  - GPT: −0.0000258;
  - Gemini: +0.000022.
  That is bootstrap randomness around zero. It does not touch the rule, which compares D_h with D_sham's point value.
- **GPT:** "This supports the specific measured outcome, not necessarily improvements in cumulative culture or
  autonomous cognition."

**All three agree on every number and on the reading. HD1 is final.**
