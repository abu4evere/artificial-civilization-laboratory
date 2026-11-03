# AM2: AM1's autonomy battery, unchanged, on nature v12 (frozen plan)

**A read-only study on live nature v12.** It runs AM1's frozen battery (`experiments/AM1_autonomy_measures/questions.md`,
with its amendment 1) unchanged on `code_v12`, as AM1 itself planned: "The same frozen battery is to be run unchanged on
v12 ... as the baseline for any redesign. A difference between v11 and v12 never redefines success."
- **Why now:** council round 54 (`docs/debate_round54_after_hn1_am1_2026-11-03.md`) put it in parallel with FF2. All
  three rank it before any habit/ends change (C): GPT 2nd, Gemini and DeepSeek 3rd, with C last. GPT asks for this
  baseline, and a read-only mechanism look, before any change to habits.
- **What it is for:**
  - v12's values of M1–M6b, the baseline for any later redesign;
  - whether AM1's validation results hold on v12. In particular: does "no habits" still complete gather-then-make
    chains more often (AM1's reversal of M3 and M5), now that FF1 fixed the make choice (F1)?

## What is identical to AM1
- **The arms:** c (v12 as live), h (`learned_weight` 0), a (`stage` "E0-C"), t (`choice_temperature` 0.25, AM1's
  amendment 1), x (`sham_draw` 1).
- **The measures** M1, M2, M3, M4, M5, M6a and M6b, with the same definitions, ages, years, windows and matched chains.
- **The validation rule:** directional, per measure. M1, M3 and M5 are predicted lower in h and in t than in c;
  "validated", "partly validated" or "not validated"; "unstable" by the sham; the sanity check in arm a (0 completed M3
  chains).
- **The observer, the analysis and the hard stops** (zero checks, all 5 × 32 worlds under one fingerprint, a blind
  recompute by GPT, Gemini and DeepSeek of M3 and M5 per arm with the c − h and c − t intervals, the readings and the
  sanity count).

## What differs (only these)
- **The code:** `code_v12` (`experiments/NV12_nature_v12/code_v12`) instead of `code_v11`. Its fault fixes are its
  defaults; AM1's other settings are unchanged.
- **The seeds:** 32 new paired seeds, **22801–22832**.
- **The bootstrap seed:** NumPy 20261110.
- **The files:** `run_am2.py` and `analyse_am2.py` are AM1's files with only the code, seeds, bootstrap seed and the
  labels ("v11" → "v12") changed. The difference is kept as `am1_to_am2.diff`.

## Comparison with AM1 (described only)
v12 − v11 is shown per measure for arm c, AM1's seeds against AM2's. These are different seeds, so it is unpaired; its
interval is a two-sample world bootstrap. **It never redefines success** and never changes a validation reading.

## The assistant's prior
1. **M1:** partly validated again (by t, not by h), as on v11.
2. **M3 and M5:** still not validated, with h above c. FF1's F1 changes which recipe is offered, not the habits' pull
   toward common actions, so the reversal remains.
3. **The sanity check passes;** the sham is stable.

## Sign-off (3 November 2026)
The assistant, under the creator's standing autonomy (sleep mode and the 2 November permission). It is read-only.
Council round 54: GPT 97%, Gemini 99%, DeepSeek about 92% for the merged plan; the assistant 85% for AM2. Frozen as
`AM2-frozen` before any code or data.
