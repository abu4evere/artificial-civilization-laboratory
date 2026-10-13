# LK1 — Location knowledge: results

Frozen as `LK1-frozen`. 256 seeds (4001–4256), 20 founders, 40 × 40, 120 years; arms: C (current location), M (last seen), S sham. `code_lk1`.

## Validity

- Zero checks: **yes**
- Code unchanged in every world (one fingerprint): **yes**
- Manipulation in the main run (M: 0 moves toward an out-of-sight loved one's current tile, must be 0; 451834 toward remembered tiles): **yes**

**Valid.**

## Baseline (rule 14)

C died out in 90 of 256 worlds (35.2%).

## Outcomes (population beside every measure, rule 18)

| | C (current location) | M (last seen) | S sham |
|---|---|---|---|
| **worlds died out** | **90** | **87** | **95** |
| median population, year 119 | 20 | 24 | 21 |
| A5: share of go-to moves toward an out-of-sight loved one's current tile | 0.293 | 0.000 | 0.290 |
| go-to moves toward a remembered tile | 0 | 451834 | 0 |
| pairings per eligible single-year | 0.029 | 0.029 | 0.028 |
| median weeks from eligible single to pairing | 170.000 | 165.000 | 163.000 |
| share of partner-weeks spent beyond sight | 0.243 | 0.302 | 0.243 |
| share of mother–child-weeks (child under 16) beyond sight | 0.033 | 0.041 | 0.032 |
| median spell apart, partners (weeks) | 2.000 | 2.000 | 2.000 |
| median spell apart, mother and child (weeks) | 2.000 | 2.000 | 1.000 |
| births per woman-year | 0.133 | 0.130 | 0.131 |
| A6c: partner-search moves aimed beyond sight | 0.590 | 0.598 | 0.584 |

## The primary question: does knowing where absent loved ones are change survival? (M against C)

Died out: M 87 vs C 90; saved / lost 41 / 38; exact sign test **p = 0.822**. Effect (C − M extinction share) +0.012, 95% interval [-0.059, +0.082]; half of F2's effect 0.120.

Frozen rule: **no meaningful effect on survival** (the interval excludes half of F2's effect).

Sham against C: died out 95 vs 90; 37 / 42; p = 0.653; effect -0.020 [-0.086, +0.047].

## Secondary measures, per world (M against C; paired Wilcoxon; described, not thresholded)

| measure | C median | M median | paired Wilcoxon p | worlds with both |
|---|---|---|---|---|
| pairings per eligible single-year | 0.027 | 0.028 | 0.968 | 256 |
| median weeks from eligible single to pairing | 142.250 | 149.750 | 0.898 | 256 |
| share of partner-weeks spent beyond sight | 0.213 | 0.277 | 1.94e-25 | 256 |
| share of mother–child-weeks (child under 16) beyond sight | 0.030 | 0.037 | 9.48e-17 | 256 |
| median spell apart, partners (weeks) | 1.000 | 2.000 | 1.18e-17 | 256 |
| median spell apart, mother and child (weeks) | 1.000 | 2.000 | 1.92e-12 | 245 |
| births per woman-year | 0.128 | 0.126 | 0.274 | 256 |
| A6c: partner-search moves aimed beyond sight | 0.629 | 0.637 | 0.926 | 256 |
