# IW1 — independent blind recompute (31 October 2026)

- **Input:** `recompute/iw1_one_file.csv`, per-world sums built from the raw output JSONs, one row per world (32
  worlds).
- **Who:** GPT (fresh chat `6ae5a640`) and Gemini (fresh chat `739056e8d63c2f56`). Each got the same text, with the
  columns and the frozen rule. Neither saw `analyse_iw1.py` or any earlier result.
- **Recorded only from their actual replies.**

| quantity | analyse_iw1.py | GPT | Gemini |
|---|---|---|---|
| U, pooled under-valuation at the make (b) | +0.004 (+0.0040) | 0.0040 | 0.0040 |
| U's 95% world-bootstrap interval | [+0.002, +0.006] | [0.0022, 0.0058] | [0.0022, 0.0058] |
| F, mean felt help per use of the kinds made | 0.163 (0.1628) | 0.1628 | 0.1628 |
| S, share of makes on fewer than 6 prior uses | 0.115 (0.1155) | 0.1155 | 0.1155 |
| frozen reading | mixed | mixed | mixed |

**Totals (both models):**
- makes 17,094; makes of a known kind 17,094;
- sum of felt help minus worth 68.099486;
- sum of felt help 2,782.341561;
- makes on fewer than 6 uses 1,974.

GPT seeded its bootstrap with 20261031, its own choice. GPT: "a classification under the specified numerical rule,
not independent evidence that agents have learned successfully or unsuccessfully."

**All three agree on every number and on the reading. IW1 is final.**
