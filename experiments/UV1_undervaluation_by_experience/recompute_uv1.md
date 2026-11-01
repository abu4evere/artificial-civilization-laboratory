# UV1 — independent blind recompute (1 November 2026)

- **Input:** `recompute/uv1_one_file.csv`, the per-seed, per-arm sums for the primary (ages 16–44, G not closed by
  death), built by `recompute/build_uv1_one_file.py` (written before data). The exact text sent is
  `recompute/prompt.txt`.
- **Who:** GPT (fresh chat `6ae78a23`) and Gemini (fresh chat `07a3071d342f25e0`). Each got the same text and the
  frozen rule. Neither saw the analysis script or any earlier result.
- **Recorded only from their actual replies.**

| quantity | analyse_uv1.py | GPT | Gemini |
|---|---|---|---|
| r: B_low (k 0–19) | −0.2071 [−0.2104, −0.2038] | −0.2071 [−0.2104, −0.2038] | −0.2071 [−0.2104, −0.2037] |
| r: B_high (k 80+) | −0.1077 [−0.1106, −0.1047] | −0.1077 [−0.1106, −0.1047] | −0.1077 [−0.1106, −0.1046] |
| r: coverage (n high; worlds) | 1,376,008; 32 | 1,376,008; 32 | 1,376,008; 32 |
| r: reading | persistent bias | persistent bias | persistent bias |
| v11: B_low | +0.2050 [+0.1931, +0.2165] | +0.2050 [+0.1931, +0.2165] | 0.2050 [0.1930, 0.2166] |
| v11: B_high | +0.4935 [+0.4837, +0.5047] | +0.4935 [+0.4837, +0.5047] | 0.4935 [0.4835, 0.5050] |
| v11: coverage | 1,628,339; 32 | 1,628,339; 32 | 1,628,339; 32 |
| v11: reading (described) | persistent bias | persistent bias | persistent bias |

- **Notes:**
  - GPT used the same NumPy seed (20261101), so its intervals are identical. Gemini's differ in the fourth decimal:
    bootstrap randomness, which does not touch the rule.
  - **GPT:** the absolute bias "decreases by approximately 48.0%", but the high-k interval "remains entirely below
    −0.05". It added that these are "descriptive findings … not proof of the causal mechanism".

**All three agree on every number and on the reading. UV1 is final: persistent bias (for r).**
