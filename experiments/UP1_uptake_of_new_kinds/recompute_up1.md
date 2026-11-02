# UP1 — independent blind recompute (2 November 2026)

- **Input:** `recompute/up1_counts.csv` (448 rows): per world, the person × kind × decision counts at each step, for new
  and old kinds. Built by `recompute/build_up1_counts.py`, written before data.
- **The exact text sent:** `recompute/prompt.txt`, written and committed before the data existed. The CSV was attached
  as a file.
- **Who:** GPT (fresh chat `6ae89f21`) and Gemini 3.1 Pro (fresh chat `003f78c1d7b2d7f3`). Neither saw the analysis
  script or any earlier result.
- **Recorded only from their actual replies.**

| quantity | analyse_up1.py | GPT | Gemini |
|---|---|---|---|
| new, step 1 | 0.0008 [0.0006, 0.0010] | 0.0008 [0.0006, 0.0010] | 0.0008 [0.0006, 0.0010] |
| new, step 2 | 0.1315 [0.1162, 0.1469] | 0.1315 [0.1162, 0.1468] | 0.1315 [0.1158, 0.1465] |
| **new, step 3** | **0.8672 [0.8518, 0.8825]** | **0.8672 [0.8519, 0.8825]** | **0.8672 [0.8521, 0.8829]** |
| new, step 4a | 0.0001 [0.0001, 0.0002] | 0.0001 [0.0001, 0.0003] | 0.0001 [0.0001, 0.0002] |
| new, step 4b | 0.0001 [0.0000, 0.0003] | 0.0001 [0.0000, 0.0003] | 0.0001 [0.0000, 0.0003] |
| new, step 5 | 0.0003 [0.0002, 0.0004] | 0.0003 [0.0002, 0.0004] | 0.0003 [0.0002, 0.0004] |
| new, made | 0.0000 [0.0000, 0.0000] | 0.0000 [0.0000, 0.0000] | 0.0000 [0.0000, 0.0000] |
| new − old, step 3 | +0.4561 [+0.4375, +0.4748] | +0.4561 [+0.4376, +0.4753] | +0.4561 [+0.4380, +0.4754] |
| reading | mainly blocked at step 3 | mainly blocked at step 3 | mainly blocked at step 3 |
| largest positive difference | step 3 | step 3 | step 3 |

- **Gemini:**
  - It also gave the old-kind shares, with intervals that match `results.md`'s points, for example old step 3 0.4111
    [0.4031, 0.4188].
  - Every other step's new-minus-old difference matches too.
  - "Frozen reading: mainly blocked at step 3 (the lower bound for new kinds is 0.8521, exceeding the 0.50 threshold)."
- **Gemini and the analysis agree** on every point value and on both readings. The interval ends differ by at most
  0.0006.
- **GPT:**
  - Totals: 4,977,150 new-kind cases and 166,823,584 old-kind cases.
  - Its old-kind shares and every new-minus-old difference match too.
  - "Step 3's new-kind share has a lower confidence bound of 0.8519, exceeding the required 0.50 threshold."

**All three agree on every point value and on both readings: mainly blocked at step 3 ("cannot make"); the largest
difference from old kinds is at step 3. UP1 is final.** Both chat tabs were closed afterwards.
