# FF4 findings: a whole action dropped because one target is too far — the fault fix

**Status: final.** The blind recompute (`recompute_ff4.md`, 7 November 2026, 16:57) matches. GPT and Gemini each
used code; every point estimate, every guard and the reading agree. DeepSeek had no code tool, and nothing from it is
counted.

Every number is from `results.md` (analyse_ff4.py, frozen before data) on cloud run 42409853945:
- 3 arms × 32 paired worlds (seeds 24801–24832), on `code_ff4` = `code_v15` + `fix_affordable_target`; LP, 200 years,
  years 100–200 counted;
- zero checks All: PASS (`zero_local.log`):
  - `code_ff4` at 0 = v15;
  - the logs are read-only;
  - the fix and the sham act;
  - the hook matched in arms c and f;
  - the unit checks found 0 errors in 5,073 fixed cases;
  - reload exact;
- in the study run, **the hook check matched in all 118,827,227 logged person-weeks (0 mismatches)**.

## The answer in one line
**The frozen reading: no harm. No guard is raised (nor for the sham).** By the frozen rule, a fault fix with no harm is
adopted as nature v16 by the safe path, with no confirmatory run.

## The guards (f against v15)
| guard | f | v15 | f vs v15 [95%] | raised? |
|---|---|---|---|---|
| starvation deaths per 1,000 living-years | 4.593 | 4.681 | ratio 0.981 [0.892, 1.075] | no |
| killings per 1,000 living-years | 0.0045 | 0.0043 | +0.0002 [−0.0087, +0.0086] | no |
| adult health | 93.37 | 92.89 | +0.49 [−0.10, +1.04] | no |
| living-weeks | 23,152,325 | 23,974,691 | ratio 0.966 [0.878, 1.064] | no |
| extinct worlds | 0 | 0 | 0 | no |
| child deaths per 1,000 child-years | 9.80 | 8.88 | ratio 1.105 [0.942, 1.256] | no |
| child starvation deaths per 1,000 child-years | 5.84 | 5.29 | ratio 1.105 [0.905, 1.312] | no |
| food gifts to kin's children per 1,000 adult-weeks | 4.68 | 4.72 | ratio 0.990 [0.924, 1.068] | no |

The sham's ratios are of the same size and direction as f's for living-weeks and child deaths. For example, its
living-weeks ratio is 0.994 [0.897, 1.106]. These are within the worlds' spread.

## The fix at work
- **The fix acted** in 194,775 forage-weeks, 106,546 gather-weeks and 1,471 hunt-weeks of arm f (counted years). In
  each, the best target was too far for the person's energy, and an affordable one was offered instead.
- **Non-starving weeks with food blocked by energy alone fell tenfold:** 0.0069 → 0.0007, ratio 0.098 [0.091, 0.104].
  - Counts: 143,788 of 20,740,701 weeks, against 13,566 of 20,034,751.
- **Starving weeks blocked by energy alone (EG1's P) fell less:** 0.0635 → 0.0570, ratio 0.898 [0.832, 0.967].
  - Counts: 39,852 of 627,539, against 33,286 of 583,701.
  - EG1 found that 55% of these weeks had even one's own tile unaffordable (energy below 25). No affordable target
    existed there for the fix to offer, so most of the remaining blocked starving weeks are of that kind.
  - Starving weeks themselves fell 7% (627,539 → 583,701).
- **Starvation deaths at 6+ with a blocked starving week in their last 4 decisions:** 0.385 → 0.332, ratio 0.863
  [0.785, 0.948].
- **The women 30–49 gap did not change:**

  | | women 30–49 | men 30–49 |
  |---|---|---|
  | v15 | 0.119 | 0.055 |
  | f | 0.121 | 0.044 |

  The fix helped men (ratio 0.802 [0.723, 0.892]) but not women (1.018 [0.970, 1.068]). **So the women's gap is not
  this fault.**
  - Women's blocked weeks are mostly of the own-tile-unaffordable kind.
  - The likely mechanism, not measured here, is feeding dependents: a short week halves energy recovery
    (`docs/research/mothers_energy_2026-11-07.md`).
- **How time is spent did not change:** the grown's shares of forage, gather, rest, make and talk all have ratios
  within 0.95–1.02.

## The flag, explained (read-only, as the frozen plan asks before adoption)
**Flagged:** "non-starving weeks blocked by energy alone", ratio 0.098, outside [0.8, 1.25].
- **This measure is the fault itself:** weeks where food was offered nowhere although an affordable target existed.
- **Its fall is the fix doing what it says.** EG1 measured that 0.926 of these blocked non-starving weeks had an
  affordable tile with food. The fall to 0.098 matches it: about 90% of them go away.
- **No guard moved, and no other described measure was flagged.**
- **The explanation finds no harm.**

## What it means
- **The fault is fixed with no harm.** "An option is dropped when you cannot afford it" now drops only what cannot be
  afforded. The fix covers forage, hunt and gather, three actions with one structure.
- **Energy was already a minor cause of hunger** (EG1). The fix trims it further, mostly in ordinary weeks. In starving
  weeks the remaining block is real tiredness: energy below the cost of foraging one's own tile.
- **Next:** the women's gap points to who feeds the children. That is a question for a read-only look, not a fault.
