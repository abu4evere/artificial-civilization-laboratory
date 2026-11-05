# LD1: why the habit look-ahead locks choices, and where remaking fails (results)

Frozen as `LD1-frozen`. run_ld1.py, analyse_ld1.py (written before data). Read-only on v13; adults 16–49, years 130–170.

## Validity

- Zero checks (All: PASS, same `code_v13` fingerprint): **yes**
- All worlds present (64 of 64): **yes**
- One fingerprint, `code_v13`'s: **yes**

**Valid.**

## Part A: the look-ahead

Expected share of adult decisions (softmax probabilities of all scored options) under three score versions (amendment 1). v13's decisions; c0's own decisions for comparison.

| class | v13 actual | v13 scale | v13 none | c0 actual |
|---|---|---|---|---|
| make | 0.0011 | 0.0074 | 0.0064 | 0.0080 |
| gather | 0.2223 | 0.2318 | 0.2189 | 0.2285 |
| forage | 0.4016 | 0.3522 | 0.3541 | 0.3846 |
| play | 0.0011 | 0.0079 | 0.0067 | 0.0062 |
| person | 0.1928 | 0.1589 | 0.1550 | 0.1583 |

**Recovery of the make share** f = (version − actual) ÷ (c0 − actual):

- scale: 0.912 [0.842, 0.987]
- none: 0.770 [0.706, 0.836]

Rule (amendment 1): "direction" if f_none >= 0.5; "scale" if f_none < 0.5 and f_scale >= 0.5; "dynamics" if both are below 0.5 (the lock lies in the states people reach).

**Primary A reading: direction (the scale version also recovers).**

**Described.**

| measure | v13 | c0 |
|---|---|---|
| q entries at the clamp (|q| ≥ 1.49), adults' year ends | 0.0006 | 0.0000 |
| mean |q| | 0.0982 | 0.0180 |
| decisions whose top option changes without the habit term | 0.1611 | 0.0658 |
| mean |habit term| ÷ mean |rest of the score| | 1.2961 | 0.2333 |
| approximation gap mean |q − (q_r + q_f)| | 0.0185 | 0.0041 |
| at make offers: 0.6 × (q_f of make − mean q_f of the options) | -0.2447 | 0.0000 |
| at make offers: 0.6 × (q_r of make − mean q_r of the options) | -0.1069 | -0.0494 |

The look-ahead term at learning, 0.8 × max next q (v13; c0's is 0 by construction), by action learned and by the next week's food band:

| action | mean term | updates |
|---|---|---|
| attack | +1.0780 | 6 |
| care | +1.0013 | 12,572 |
| court | +0.9757 | 5,912 |
| explore | +0.8080 | 6,032 |
| fill | +nan | 0 |
| flee | +0.9672 | 15 |
| forage | +0.9909 | 1,871,410 |
| gather | +0.9284 | 1,035,876 |
| give | +1.0371 | 398,663 |
| heat | +0.9437 | 3 |
| hunt | +0.8141 | 460 |
| join | +0.9420 | 307,263 |
| make | +0.8758 | 5,097 |
| play | +0.8703 | 5,138 |
| put | +0.8907 | 491,609 |
| rest | +0.9351 | 39,367 |
| steal | +0.9244 | 626 |
| take | +0.8422 | 543 |
| talk | +1.0384 | 480,841 |
| next food band 0 | +0.9418 | 782,571 |
| next food band 1 | +0.9273 | 1,941,437 |
| next food band 2 | +1.0391 | 1,906,896 |
| next food band 3 | +0.2624 | 30,529 |

Exactness at each world's end (clean entries, q = q_r + q_f to 1e-9): v13 0 wrong of 943,417; v13, discount 0 0 wrong of 1,102,705.

## Part B: where remaking fails

World-new kinds made in play in years 130–165, followed 5 years in their inventor's weeks; the furthest stage reached.

| stage | v13 | v13, discount 0 |
|---|---|---|
| 0. never held the recipe at a week's end | 0.116 [0.074, 0.169] | 0.642 [0.613, 0.667] |
| 1. held the recipe, never with its inputs | 0.882 [0.830, 0.923] | 0.357 [0.332, 0.386] |
| 2. held both, never while free and valuing it | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.001] |
| 3. free and valuing it, never offered | 0.002 [0.000, 0.007] | 0.000 [0.000, 0.001] |
| 4. offered, never chosen | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| 5. remade | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.001] |
| kinds | 1,039 | 11,357 |

**Primary B, v13: most kinds stop at stage 1 (held the recipe, never with its inputs): 0.882. The first R target decided before data: opportunity, or an intention to gather for a past success.**

**Primary B, v13, discount 0: most kinds stop at stage 0 (never held the recipe at a week's end): 0.642. The first R target decided before data: recipe memory (rules review R1).**

**Described.**

- v13: recipe gone by the first week's end 121 of 1,039; lost because the inventor died 16; learned by anyone else 20; median weeks until lost 0 (of 147 lost).
- v13, discount 0: recipe gone by the first week's end 7,291 of 11,357; lost because the inventor died 107; learned by anyone else 161; median weeks until lost 0 (of 7,747 lost).

## Population (beside every measure)

| world | living-weeks | adult-weeks (16–49) | extinct worlds |
|---|---|---|---|
| v13 | 8,889,569 | 4,662,507 | 1 |
| v13, discount 0 | 10,000,198 | 5,122,594 | 2 |

