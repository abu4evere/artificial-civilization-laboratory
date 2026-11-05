# HE1 findings: habits learn from experience — a law test in a copy

**Status: final.** Blind recompute by GPT and Gemini (fresh chats, with code) matches every number and the reading (`recompute_he1.md`); DeepSeek's reply is appended there when it ends.

Every number is from `results.md` (analyse_he1.py, frozen before data) on run 42099596852:
- 96 worlds: v13, the law (`discount` 0) and the sham, 32 paired seeds 23501–23532, 200 years;
- counted over years 100–200;
- zero checks All: PASS (local record, accepted by the cloud; `code_v13` fingerprint f8b793bf…).

## The answer in one line
**Not supported: harm.** Removing the habit look-ahead releases making again (makes ×6.1, finished chains ×7), but
**people starve more often**. Starvation deaths per 1,000 living-years rise by 64% [47%, 84%], above the frozen
guard. The law is not adopted, and no confirmatory run follows.

## The frozen questions, answered
1. **Harm guards (primary): the hunger guard is raised.**
   - **Hunger:** starvation deaths per 1,000 living-years, v13 4.647 against the law 7.637; ratio **1.643 [1.467,
     1.842]**. The rule raises the guard above 1.25 with the lower bound above 1. Raised.
   - **Population:** living-weeks ratio 1.329 [1.222, 1.447], more people. Not raised.
   - **Extinction:** 0 in every arm. Not raised.
   - **Health:** adults' mean at year ends, 93.08 against 91.50; difference −1.58 [−2.39, −0.81]. That is below zero but
     within the frozen −5 limit. Not raised.
2. **The effect (co-primary): "the law releases making".**
   - M3: v13 0.0036 (769,844 gather chains, 7,226,376 matched), law 0.0257 (1,222,172; 11,365,310). Difference
     +0.0221 [+0.0209, +0.0233].
   - Makes per adult-year: 0.0631 against 0.3827; ratio 6.065 [5.490, 6.643].
3. **Reading: not supported** (no harm is required, and the hunger guard is raised).

## Described (no frozen prediction; population beside each)
- **Deaths by cause, years 100–200** (v13 / law / sham):
  - starvation 2,361 / **5,157** / 2,472;
  - thirst 1,106 / 1,687 / 1,202;
  - illness 2,138 / 3,014 / 2,205;
  - **killed 4 / 216 / 4**;
  - neglect 36 / 67 / 35;
  - childbirth 102 / 168 / 107;
  - old age 4,877 / 4,664 / 5,253.

  The law's worlds hold 33% more living-weeks, so the raw counts partly reflect size. The starvation **rate** is the
  frozen guard, and it is up 64%.
- **Violence:** deaths by killing rise from 4 to 216.
  - Steal is chosen about 9 times as often (0.15‰ → 1.39‰ of adult decisions) and attack goes from 0 to 0.14‰ (a
    check of the action counts, described).
  - Without the look-ahead, habits do not count next week's consequences of harming others.
- **Acts aimed at a person** are fewer: −0.033 [−0.044, −0.023].
- **Food per adult** at year ends is not distinguishable: −0.30 [−0.77, +0.13]. M2 is lower (−0.037).
- **World-new kinds** in years 100–195: v13 3,867, the law 36,284. **Remade: 1 and 1. R is still zero.**
- **The sham against v13:** living-weeks 1.043 [0.949, 1.141]; M3 +0.0001. Clean.

## Against the assistant's prior (questions.md)
| prior | result |
|---|---|
| 1. no harm (living-weeks about +15%, hunger deaths not higher) | **no:** living-weeks +33%, but the starvation rate +64% (the guard) and killings ×54 |
| 2. the law releases making | **yes** (×6) |
| 3. R stays near 0 | **yes** (1 of 36,284) |
| overall "supported" about 75% | **not supported** |

## What it means (the assistant's reading)
- **The look-ahead was doing real work as well as harm.**
  - LD1 showed it marks making down through a familiarity bias.
  - HE1 shows that without it people also stop counting next week's cost of going hungry, or of hurting others: more
    starvation and far more killing.
  - It was crude foresight, but foresight nonetheless.
- **This confirms the caution written before this result** (`docs/research/habits_bootstrap_caution_2026-11-05.md`):
  real habit learning does look ahead, so "no look-ahead" was never likely to be the right law.
- **The candidate that remains:** a look-ahead that is **not biased toward familiarity**. For example, it bootstraps
  only from situations that are well learned, or values a rarely seen situation by the person's own experience
  rather than by its near-zero start. That keeps the look-ahead's protection against hunger and harm and removes its
  bias against making. It goes to the council as its own frozen test.
- **Remaking stays the deeper problem.** Even 36,284 new kinds produce one remake.
