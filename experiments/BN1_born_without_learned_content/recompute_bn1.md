# BN1 — independent blind recompute (2 November 2026)

- **Input:** `recompute/bn1_cells.csv` (4,104 rows). Per arm, seed and cell (situation|action), the raw sums for
  early-life habit updates: n and sum |q − G|. Built by `recompute/build_bn1_cells.py`, written before data.
- **The exact text sent:** `recompute/prompt.txt`, written and committed **before the data existed**, from the frozen
  rule in `questions.md` (not from the analysis script). The CSV was attached as a file.
- **Who:** GPT (fresh chat `6ae852b9`) and Gemini (fresh chat `1a3a6aeafc603932`). Neither saw the analysis script or
  any earlier result.
- **Recorded only from their actual replies.**

| quantity | analyse_bn1.py | GPT | Gemini |
|---|---|---|---|
| common cells | 28 (of 41) | 28 | 28 |
| coverage c / z / x / s | 1.000 / 1.000 / 1.000 / 1.000 (3 decimals) | 0.9997 / 0.9997 / 0.9996 / 0.9996 | 0.9997 / 0.9997 / 0.9996 / 0.9996 |
| E, v11 (c) | 0.2734 | 0.2734 | 0.2734 |
| E, z | 0.2939 | 0.2939 | 0.2939 |
| E, x | 0.2844 | 0.2844 | 0.2844 |
| E, sham (s) | 0.2733 | 0.2733 | 0.2733 |
| **D_z = z − v11** | **+0.0205 [+0.0157, +0.0252]** | **+0.0205 [+0.0157, +0.0252]** | **+0.0205 [+0.0157, +0.0252]** |
| sham − v11 | −0.0001 [−0.0077, +0.0072] | −0.0001 [−0.0076, +0.0072] | −0.0001 [−0.0077, +0.0071] |
| x − v11 | +0.0110 [+0.0057, +0.0162] | +0.0110 [+0.0056, +0.0162] | +0.0110 [+0.0056, +0.0162] |
| x − z | −0.0095 [−0.0155, −0.0037] | −0.0095 [−0.0154, −0.0036] | −0.0095 [−0.0154, −0.0036] |
| reading | inconclusive | inconclusive | inconclusive |

- **GPT's notes:**
  - It used 10,000 paired replicates with random seed 20261102.
  - "All 28 common cells retained positive counts in every arm in every bootstrap replicate; no replicate-specific
    exclusions were necessary."
  - On the reading: "the interval does not establish the preregistered threshold for declaring z worse."
- **GPT and the analysis agree** on every point value. The interval ends differ by at most 0.0001 (bootstrap
  randomness).
- **Gemini's notes:**
  - Its first reply gave only a script ("unable to execute Python code directly"). Asked to load the attached file
    with its code tool, it ran the script and reported the numbers above.
  - Its own script used 10,000 paired replicates (NumPy seed 42).
  - Its table of **total counts per arm is garbled**: the same 164,136 for every arm, with malformed numbers such as
    "164,0824". Those totals are not used here. Its coverage shares, E values, differences and reading are the ones
    recorded above.
- **Gemini and the analysis agree** on every point value and on the reading. The interval ends differ by at most
  0.0001.

**All three agree on every point value and on the reading: inconclusive. BN1 is final.** Both chat tabs were closed
afterwards.
