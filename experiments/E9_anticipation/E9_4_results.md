# E9.4 — Does the lesson undo itself? · Results

Read-only replays of E9 A2-full (seeds 301–304, 120 years; 11,098 adult-years followed from one autumn to the
next). The probe changed nothing (state hash, 20 years) and all four replays matched E9. Predictions frozen in
E9_4_self_erasing.md (tag `E9.4-frozen`). Data: `output_e94/`.

| group | n | median expectation this autumn | median next autumn | median ratio |
|---|---|---|---|---|
| prepared, no short weeks that winter | 64 | 0.51 | 0.13 | **0.25** |
| prepared, some short weeks | 42 | 0.53 | 0.30 | **0.53** |
| did not prepare, went short (had gone short the winter before) | 4,086 | 0.18 | 0.19 | **1.06** |
| did not prepare, no short weeks | 2,236 | 0.14 | 0.04 | 0.26 |
| prepared two autumns running | 1 | 0.50 | 0.65 | 1.31 |

| | planners | went short last winter, did not prepare |
|---|---|---|
| short weeks in the winter after (mean) | 0.93 | 1.59 |
| winters with no short weeks | 60% | 35% |

Share of adults who prepared, by their winter expectation at the start of autumn:

| expectation | adult-years | prepared |
|---|---|---|
| under 0.1 | 5,810 | 0.0% |
| 0.1–0.2 | 2,705 | 0.0% |
| 0.2–0.3 | 1,253 | 0.1% |
| 0.3–0.4 | 669 | 1.3% |
| 0.4–0.5 | 403 | 7.9% |
| 0.5 and above | 258 | **24.8%** |

## Frozen predictions, scored

1. **wrong (narrowly)** — planners had 0.58× the short weeks of comparable non-planners (prediction: at most 0.5×);
   60% of them had a winter with no short weeks, against 35%.
2. **confirmed** — ratios 0.25 (prepared, no short weeks) ≤ 0.35; 1.06 (did not prepare, went short) ≥ 0.8; 0.53
   (prepared, some short weeks) between.
3. **confirmed, weakly** — planners still at 0.3+ the next autumn prepared again in 1 of 22 cases; below 0.3, in 0 of 84.

## What this says

- **Preparing is a threshold behaviour.** Almost nobody prepares with a winter expectation below about 0.4; a quarter of
  those at 0.5 or more do.
- **Preparation prevents the hunger that taught it.** Planners went short less, and most had no short weeks at all.
- **So the lesson falls below the threshold.** After a well-provisioned winter, a planner's expectation drops to about a
  quarter of what it was (the size of the drop is set by the code's learning rule; that it happens is because
  preparation worked), to a median of 0.13, far below where anyone prepares. They will not prepare again until hunger
  rebuilds the lesson.
- **The self-erasing lesson is now a measured mechanism**, not only an interpretation: successful preparation removes
  the experience that drives preparation.
