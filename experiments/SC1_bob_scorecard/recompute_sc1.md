# SC1 — independent blind recompute (2 November 2026)

- **Input:** `recompute/sc1_sums.csv` (15,694 rows): per world, the raw sums behind each primary contrast. Built by
  `recompute/build_sc1_sums.py`, written before data.
- **The C12 caveat:** C12's per-world held-out errors come from the analysis's ridge fits (`recompute/c12_sse.npz`).
  So for C12 the recompute checks the ratio and its interval, not the regression.
- **The exact text sent:** `recompute/prompt.txt`, written and committed before the data existed. The CSV was attached
  as a file. For Gemini, one sentence was added at the end ("Please load the attached file with your code tool and run
  the computation yourself"), because in BN1 it first returned only a script. Nothing about the computation was
  changed.
- **Who:** GPT (fresh chat `6ae86e86`) and Gemini (fresh chat `cc1c6458f546d3f3`). Neither saw the analysis script or
  any earlier result.
- **Recorded only from their actual replies.**

| contrast | analyse_sc1.py | GPT | Gemini | label (all) |
|---|---|---|---|---|
| C3 | −0.0811 [−0.1012, −0.0638] | −0.0811 [−0.1023, −0.0639] | not obtained | inconclusive |
| C4 | −0.0381 [−0.1471, +0.0279] | −0.0381 [−0.1446, +0.0278] | not obtained | inconclusive |
| C5 | +0.0105 [+0.0085, +0.0495] | +0.0105 [+0.0078, +0.0490] | not obtained | inconclusive |
| C6 | 0.0000 [0.0000, 0.0000] | 0.0000 [0.0000, 0.0000] | not obtained | inconclusive |
| C7 | not measurable (2 told) | not measurable (2 told) | not obtained | not measurable |
| C9 | +0.4102 [+0.3925, +0.4283] | +0.4102 [+0.3918, +0.4286] | not obtained | positive contrast detected |
| C10b | −0.0375 [−0.0449, −0.0309] | −0.0375 [−0.0451, −0.0308] | not obtained | inconclusive |
| C12 | +0.0779 [+0.0719, +0.0840] | +0.0779 [+0.0720, +0.0842] | not obtained | positive contrast detected |

- **GPT's notes:**
  - It used 10,000 replicates (NumPy `default_rng(20261102)`).
  - **C3's sample is reported differently.** GPT gives the updates in the 23 common cells, 1,341,993 at k 0–19 and
    283,477 at k 80+. `results.md` gives all updates.
  - **C5 is computed only where both groups occur:** the 10 strata holding 61 unwanted and 112,352 wanted gathers.
  - **C6 used the fallback.** No kind has a best factor below 1.02, so it compared thirds (q1 = 1.5535, q2 = 1.9300).
    "None of the 3,883 kinds was remade, so the contrast and interval are exactly zero."
  - **C3:** "entirely negative, but the prescribed positive label ... is not earned".
- **GPT and the analysis agree** on every point value and every label. The interval ends differ by at most 0.0025
  (C4's lower end), from bootstrap randomness.
- **Gemini: no numbers obtained this time.** Gemini (Flash) could not run its code tool on 2 November. Four attempts in
  three fresh chats:
  1. **chat `cc1c6458f546d3f3`:** it first said the file was "empty or unpopulated". Asked to load it with code, it
     returned "Sorry, something went wrong". Asked again, it said "code execution tools are currently unavailable in
     this turn" and gave only a script.
  2. **chat `52c34083a704cc9b`**, the same file: "I seem to be encountering an error."
  3. **chat `f54a06309dc7fd97`**, with the file split in two and only the non-C3 part (103 KB, `sc1_sums_rest.csv`,
     no numbers changed) sent: "attached without data contents". Asked to load it with code: "I am currently unable to
     execute code", and again only a script.

  **Its scripts were not run by the assistant and counted as Gemini's numbers**: a model's recompute is recorded only
  from numbers in its reply (`CLAUDE.md`).
- **GPT's blind recompute matches every point value and every label.** That meets `CLAUDE.md`'s minimum ("a fresh
  session ... or GPT recomputes the key numbers"). But **SC1's own frozen plan names both GPT and Gemini**, so SC1 is
  **not yet final**: its readings stand on GPT's match until Gemini's recompute is added. The tag `SC1-done` waits for
  it.
- **Gemini's recompute is to be retried** when its code tool works again. Its numbers will be appended here, not
  rewritten.
- All chat tabs were closed afterwards.
