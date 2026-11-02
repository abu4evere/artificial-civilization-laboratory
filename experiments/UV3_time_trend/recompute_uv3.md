# UV3 — independent blind recompute (1 November 2026)

- **Input:** `recompute/uv3_cells.csv`, the per-seed, per-cell sums for the primary population (k ≥ 80, ages 16–44, G
  not closed by death) in years 100–124 and 175–199, built by `recompute/build_uv3_cells.py` (written before data).
  The instruction sent is `recompute/prompt.txt` without its DATA part.
- **How it was given:** as planned, the file was attached to each chat (731 rows, 35 KB).
  - ChatGPT: through its "Attach files" input.
  - Gemini: through the hidden document input that appears with its upload menu. No file dialog opened on the
    creator's screen.
- **Who:** GPT (fresh chat `6ae7d1bd`) and Gemini (fresh chat `506e7d98cc646377`). Neither saw the analysis script or
  any earlier result.
- **Recorded only from their actual replies.**

| quantity | analyse_uv3.py | GPT | Gemini |
|---|---|---|---|
| common-support cells | 21 (of 43 in all quarters; 41 in these two) | 21 | 21 (of 41) |
| coverage, years 100–124 / 175–199 | 0.996 / 0.999 | 99.61% / 99.89% | 0.9961 / 0.9989 |
| ΔG | −0.0100 [−0.0157, −0.0039] | −0.0100 [−0.0157, −0.0039] | −0.0100 [−0.0159, −0.0041] |
| reading | returns stable | returns stable | returns stable |

- **Notes:**
  - The analysis counts 43 cells over all four quarters. The file holds the 41 that have updates in the two compared
    quarters; the other two do not affect ΔG or the coverage.
  - Gemini's interval differs in the fourth decimal: bootstrap randomness.
  - **GPT:** the interval is "entirely negative, its magnitude remains within the predefined equivalence band … a
    small negative change, not a substantively large decline", and "this result alone does not establish why habit
    values or calibration bias changed".

**All three agree on every number and on the reading. UV3 is final: returns stable.**
