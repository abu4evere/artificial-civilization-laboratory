# HC1 — Habit copying in talk: whole table or only the situation at hand? Findings (recompute by GPT and Gemini pending; not yet final)

Frozen as `HC1-frozen`; the creator approved its thresholds on 27 October. A nature-change study:
`code_hc1` = `code_v7` + one setting (`v7_to_hc1.diff`). Run on GitHub Actions (run 40528434282, `skip_zero=local`).
96 worlds: w (v7), s (copy only the model's current situation), x (sham), on the same 32 seeds (19201–19232). LP, 200
years. Every number comes from `analyse_hc1.py`, written before data; the full table is in `results.md`.

**Validity:**
- zero checks pass (`code_hc1` with "whole" equals `code_v7`; the observer is read-only; the setting and sham act;
  reload is exact);
- all 96 worlds are present under one fingerprint;
- every TD update replays exactly (mismatches 0).

## The answer

**By the frozen rule, the change is not supported.** Copying only the situation at hand does not reduce the common
actions' over-valuation. It is +0.436 under the new law against +0.424 under v7, a change of **−0.012 [−0.021, −0.004]**
in the wrong direction. At least +0.10 was needed. Nothing was harmed either:

| measure (adults, years 100–200) | w (v7) | s (situation) | x (sham) | w − s [95%] |
|---|---|---|---|---|
| **common actions' bias q − G** | +0.424 | +0.436 | +0.425 | **−0.012 [−0.021, −0.004]** |
| make bias | −0.571 | −0.565 | −0.573 | −0.006 [−0.018, +0.007] |
| mean realised G, all actions | 0.684 | 0.673 | 0.680 | s − w −0.010 [−0.023, +0.002] |

**The decision rule:**
- **P (calibration):** −0.012, which is not at least 0.10 with a lower bound above 0: **does not support.**
- **H (realised return):** lower bound −0.023, above −0.05: **no harm.**
- **F (flags):**
  - extinct worlds: s 0, w 0 (the sham 1);
  - mean population, years 100–200: s 122.0 against w 130.9, a ratio of 0.932 (≥ 0.90; the sham 119.7).

  No flag.

**Populations:** make updates late, w 10,150, s 9,772, x 9,561.

## Why it did not work (reading; not tested here)
- CL1 showed that the over-valuation **arrives** through copying.
- HC1 shows that **how much** is copied per conversation is not what carries it. A learner copying only the model's
  current situation still copies the situations people are in most of the time: the same common ones where the inflated
  values sit.
- What CL1 also found is unchanged: copied values are **never checked against the learner's own returns**. Narrowing
  the scope of copying leaves that untouched.
- **Accounting is not causation**, as GPT cautioned before the study (CL1's caveat). The route that carries a value is
  not necessarily the rule whose change removes it.

## Against the prior (the assistant's, frozen)
1. "P supports: the bias falls to under +0.20": **wrong** (it rose slightly, to +0.436).
2. "H: no harm; G changes by less than 0.02": **right** (−0.010).
3. "No flags": **right.**
4. "Make's bias changes little": **right** (+0.006).

## What follows (from the frozen branches)
- **"P fails: restricting what is copied does not correct the over-valuation. Copied values arrive through the
  situations people are actually in, or carers take over. Described."** This branch holds; the first reading fits.
- **No nature-v8 candidate. v7 stays live.**
- The next question for the council and the creator: whether copied habits should be **weighed against the learner's
  own experience** (a different law from scope). Or whether the over-valuation should be left alone, since own
  experience is calibrated and people's realised returns did not suffer.
