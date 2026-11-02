# KL1 — independent blind recompute (2 November 2026)

- **Input:** `recompute/kl1_one_file.csv`, the per-seed counts for the primary (world-level losses by cause; revivals
  of markable kinds, through reading and in total), built by `recompute/build_kl1_one_file.py` (written before data).
  The exact text sent is `recompute/prompt.txt`.
- **Who:** GPT (fresh chat `6ae81975`) and Gemini (fresh chat `002646d1fa4c0e3d`). Neither saw the analysis script or
  any earlier result. Both tabs were closed afterwards.
- **Recorded only from their actual replies.**

| quantity | analyse_kl1.py | GPT | Gemini |
|---|---|---|---|
| losses: death / forgetting / mixed (all) | 10,447 / 1,126 / 3 (11,576) | 10,447 / 1,126 / 3 (11,576) | 10,447 / 1,126 / 3 (11,576) |
| D | 0.9025 [0.8911, 0.9129] | 0.9025 [0.8910, 0.9129] | 0.9025 [0.8912, 0.9133] |
| markable revivals: read / all | 2 / 99 | 2 / 99 | 2 / 99 |
| R_markable | 0.0202 [0.0000, 0.0517] | 0.0202 [0.0000, 0.0538] | 0.0202 [0.0000, 0.0526] |
| reading (loss) | death is the main road of loss | same | same |
| reading (marks) | marks do not (yet) | same | same |

- **Note:** `results.md` splits forgetting losses as 1 markable + 1,125 other, the same 1,126 total. The interval ends
  differ in the third or fourth decimal: bootstrap randomness. GPT used a different seed (20261102).
- **GPT:** the reading "does not mean marks can never preserve knowledge. It means the observed contribution in KL1
  does not meet the frozen criterion."

**All three agree on every number and on both readings. KL1 is final.**
