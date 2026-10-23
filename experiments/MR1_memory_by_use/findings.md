# MR1 — remembering by use, not by slots: findings

Frozen as `MR1-frozen` before any data. A Law 126 study: one candidate change to nature, tested against v3.
Tables: `results.md`, from `analyse_mr1.py` (written and committed before data). Code: `code_mr1` = `code_v3` +
`memory_by_use` (`v3_to_mr1.diff`). 512 worlds: 256 new seeds 9201–9456 × C (v3) and U (forgotten after 2 years
unused, cap 60), 20 founders, 120 years. **Run on GitHub's machines** (`cloud-run`, run 39879935726). Zero checks
passed there and on this PC. GPT's review was not obtained before freezing (see the sign-off in `questions.md`).

## Validity

- Zero checks passed (off = `code_v3` on four runs; U acts; observers change nothing; reload exact).
- All 512 worlds are present, with one fingerprint.
- **Manipulation check passes:** useful inventions still held by their inventor 13 weeks later, median C 0.549,
  U 1.000; U − C +0.457 [+0.445, +0.469], p = 9.6e-44.

**Valid.**

## The frozen reading

**Primary, transmission** (share of useful inventions ever learned by someone else, CA1's link 3): medians C 0.112,
U 0.079.

| U − C, mean | 95% interval | Wilcoxon p | reading |
|---|---|---|---|
| −0.0325 | [−0.0373, −0.0278] | 9.2e-28 | **changes transmission (U lower)** |

**Survival check:** C died out in 88 of 256, U in 90 (32 saved / 34 lost; p = 0.90; C − U −0.008 [−0.070, +0.055]):
**no meaningful effect.**

**The adoption rule, fixed before data:** transmission must rise. It fell. **Memory by use is not adopted.** Nature
stays v3.

**The prior was wrong.** It expected a small rise (3–5 points). Transmission fell by about 3 points.

## Beside it (described; population first)

| arm | median population, year 60 / 119 | died out | recipes held per person | weeks a useful invention stays with its inventor (mean) | built on by a learner | longest part chain (median) | children's useful inventions passed on |
|---|---|---|---|---|---|---|---|
| C | 23 / 22 | 88 | 8.84 | 668.6 | 3,156 | 14 | 4,437 of 66,988 |
| U | 23 / 22 | 90 | 2.32 | 238.4 | 6,228 | 15 | 2,395 of 68,889 |

Deaths by cause are nearly the same in both arms (`results.md`).

## What it means (the assistant's reading; not a frozen test)

- **The fix worked on the step it targeted and broke the next one.** In U a new invention is never pushed out in its
  first season (held at 13 weeks: 55% → 100%). But over a lifetime people hold far fewer recipes (8.8 → 2.3) and keep
  an invention a third as long (669 → 238 weeks). In v3 the 12-slot limit pushes out new things quickly, but whatever
  survives the first season is **kept for life**, used or not. Under "2 years unused", most things people know are
  not used often enough to be kept.
- **So v3's memory is not too short; it is too short at the start and too long afterwards.** Teaching draws on what a
  person still holds and values, so a smaller store means fewer things to teach.
- **"Built on by a learner" doubled (3,156 → 6,228)** while passing on fell. This was described, not tested, and the
  reason is not known. One possibility: people who forget re-invent, and re-inventing on top of someone else's part
  counts as building on it. It should not be read as a gain without a check.
- The 2-year value was a stand-in, never tuned (the plan said so). A different value, or gradual fading, might give
  a different answer. That would be a new study, not a reading of this one.

## Next (for the creator)

The cumulative-culture line has now tested which recipe the limit drops (LM1: no effect), parts-first teaching
(adopted, +2 points), and replacing the limit with forgetting by disuse (MR1: −3 points). A possible next step is to
protect new inventions in their first season (a short grace period) while keeping v3's lifelong memory. That is the
one change this result points to. It needs its own frozen plan and the creator's decision.
