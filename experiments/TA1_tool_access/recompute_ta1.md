# TA1 — independent blind recompute (31 October 2026)

- **Input:** `recompute/ta1_one_file.csv`, per-world counts from the raw output JSONs (32 worlds).
- **Who:** GPT (fresh chat `6ae61691`) and Gemini (fresh chat `a0aead5ec654a3a5`). Each got the same text, with the
  columns and the frozen rule. Neither saw `analyse_ta1.py` or any earlier result.
- **Recorded only from their actual replies.**

| quantity | analyse_ta1.py | GPT | Gemini |
|---|---|---|---|
| A, a forage tool within reach (share of bare-handed weeks) | 0.819 [0.802, 0.834] | 0.819 [0.802, 0.834] | 0.819 [0.802, 0.834] |
| B, could make one now | 0.726 [0.712, 0.739] | 0.726 [0.712, 0.739] | 0.726 [0.712, 0.739] |
| F, within reach and room to receive | 0.680 | 0.680 | 0.680 |
| frozen reading | both | both | both |

**Totals (both models):**
- bare-handed weeks 6,310,506;
- A 5,169,652;
- B 4,582,509;
- F 4,291,752.

GPT seeded its bootstrap with 20261031, its own choice.

**All three agree on every number and on the reading. TA1 is final.**
