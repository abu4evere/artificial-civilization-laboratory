# HA1 — independent blind recompute (1 November 2026)

- **Input:** `recompute/ha1_one_file.csv`, the per-seed sums for the primary (eligible decisions, decisions with a
  handing option, summed handing mass), built by `recompute/build_ha1_one_file.py` (written before data). The exact
  text sent is `recompute/prompt.txt`.
- **Who:** GPT (fresh chat `6ae7f6e3`) and Gemini (fresh chat `1a58b00334e4a546`), sent at about 21:40 after the
  creator reconnected Chrome. Neither saw the analysis script or any earlier result.
- **Recorded only from their actual replies.**

| quantity | analyse_ha1.py | GPT | Gemini |
|---|---|---|---|
| totals: decisions / with option / mass | 15,632,590 / 1,108,620 / 59,143.9 | 15,632,590 / 1,108,620 / 59,143.857435 | 15,632,590 / 1,108,620 / 59,143.857435 |
| E | 0.0709 [0.0667, 0.0747] | 0.0709 [0.0667, 0.0747] | 0.0709 [0.0668, 0.0747] |
| C | 0.0533 [0.0503, 0.0572] | 0.0533 [0.0503, 0.0572] | 0.0533 [0.0502, 0.0573] |
| reading | opportunity-limited | opportunity-limited | opportunity-limited |

- GPT used the same NumPy seed, so its intervals are identical. Gemini's differ in the fourth decimal: bootstrap
  randomness.

**All three agree on every number and on the reading. HA1 is final: opportunity-limited.**
