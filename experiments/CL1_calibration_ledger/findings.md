# CL1 — Which route carries the miscalibration? Findings (recompute by GPT and Gemini pending; not yet final)

Frozen as `CL1-frozen` (operational note 1); decided and signed off in sleep mode (`docs/autonomous_decisions.md`). Run
on GitHub Actions (run 40499977145, `skip_zero=local`). 32 worlds on nature v7, LP (80 founders, 80×80), seeds
19101–19132, 200 years. Every number comes from `analyse_cl1.py`, written before data; full tables are in `results.md`.

**Validity:**
- zero checks pass;
- all 32 worlds are present under one fingerprint (`code_v7`);
- every TD update replays exactly, and HL1's ledger adds up at every update and decade (mismatches 0).

## The answer

**The common actions' over-valuation arrives through copying in talk.** People's own experience values those actions
slightly **below** what actually follows. Making's under-valuation is the opposite case: own experience alone, with
almost nothing copied.

### Q1 — The common actions (forage, give, talk, gather; adults, years 100–200; 11.0 million updates)

q 1.122 − G 0.704 = **+0.418 [+0.410, +0.427]**, exactly:

| term | value [95%] | share |
|---|---|---|
| own experience, C_TD − G | −0.069 [−0.089, −0.049] | −0.16 |
| **copying in talk, C_talk** | **+0.391 [+0.371, +0.412]** | **0.93** |
| carers, C_carer | +0.089 [+0.085, +0.093] | 0.21 |
| birth | 0.000 | 0.00 |
| paid back | +0.008 | 0.02 |

**The term carrying the largest share: copying in talk (0.93).** Own experience (C_TD 0.635) lies a little below the
realised return (0.704). This holds even though the max look-ahead's optimism (0.142) is part of how C_TD was formed.

### Q2 — Make (adults, years 100–200; 10,176 updates)

q 0.049 − G 0.615 = **−0.566 [−0.581, −0.549]**, exactly:

| term | value [95%] |
|---|---|
| **own experience, C_TD − G** | **−0.606 [−0.622, −0.588]** (C_TD only 0.009) |
| copying in talk | +0.030 |
| carers | +0.011 |
| birth, paid | 0 |

Making's value from own experience is almost nothing, against a realised return of 0.615. Copying adds 0.03.

### Q3 — Over time (the common actions)

| years | q − G | own C_TD − G | talk | carers |
|---|---|---|---|---|
| 0–50 | −0.361 | −0.514 | +0.134 | +0.014 |
| 50–100 | +0.146 | −0.230 | +0.311 | +0.055 |
| 100–200 | +0.418 | −0.069 | +0.391 | +0.089 |

- **Own experience never over-values the common actions.** It rises towards the realised return from below.
- **The over-valuation appears when the copied part outgrows own experience's shortfall,** after year 50.
- **Per action, late:**

  | action | own experience | copied in talk |
  |---|---|---|
  | forage | −0.010 | +0.376 |
  | give | −0.228 | +0.530 |
  | talk | −0.227 | +0.480 |
  | gather | −0.000 | +0.283 |

## Against the prior (the assistant's, frozen)
1. "Copying in talk carries the largest share, above own TD": **right** (0.93; own TD −0.16).
2. "C_TD − G positive but smaller than C_talk": **half right.** C_talk is far larger, but C_TD − G is **negative**
   (−0.069), not positive.
3. "For make, C_TD far below G (−0.5 or less), every social part under 0.05": **right** (−0.606; talk 0.030, carers
   0.011).

**GPT's prediction** ("copying amplifies common-action overvaluation while sparse experience sustains making's
underestimation"): **right on both counts.**

## What follows (from the frozen branches)
- **"Copying in talk carries the largest share: a copying-rule study (F) is the targeted next nature-change candidate,
  on calibration grounds."** This is the branch that holds.
- **Expected SARSA (C) is not the target.** Own experience is not over-valued, so the max look-ahead does not, in the
  end, inflate values above what follows.
- **Make:** practice starvation is confirmed at the level of calibration: own experience 0.009 against 0.615 realised.
  Exploration (E) is the next read-only question for making.

**Reading (interpretation, not tested; accounting, not causation, as GPT cautioned):** the whole-table copying in talk
(`actions._imitate`) moves a learner's habits towards a model's whole table. What learners copy are values their models
built partly by copying in turn. Copied values are not checked against the learner's own returns. A change to how habits
are copied, one law, frozen, with a matched control, judged on calibration, not on making, would be the targeted test.
**That is a nature change: the creator's decision** (GPT's caution on adoption stands).
