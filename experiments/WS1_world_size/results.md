# S1 — World size: results

Frozen as `S1-frozen`. 256 new seeds (3001–3256), 120 years; arms: C (40×40, 20), L (80×80, 20), LP (80×80, 80), P (40×40, 80), S sham. Settings only, in `code_p2` with every setting off.

## Validity

- Zero checks (40×40 and 80×80): **yes**
- Code unchanged: **yes**

**Valid.**

## Baseline (rule 14)

C died out in 107 of 256 worlds (41.8%).

## Manipulation checks (week one, and during the run)

| | C (40×40, 20) | L (80×80, 20) | LP (80×80, 80) | P (40×40, 80) | S sham |
|---|---|---|---|---|---|
| land tiles per founder (week one, median) | 32.00 | 127.90 | 32.00 | 8.00 | 32.00 |
| distance between founding bands (week one, median) | 15.30 | 29.60 | 29.30 | 15.50 | 15.30 |
| possible partners in sight per founder (week one, median) | 2.20 | 2.20 | 9.70 | 9.70 | 2.20 |
| seeker-weeks with an eligible single in sight (whole run) | 0.317 | 0.344 | 0.616 | 0.470 | 0.334 |

## Extinction and growth (the frozen outcomes)

| | C (40×40, 20) | L (80×80, 20) | LP (80×80, 80) | P (40×40, 80) | S sham |
|---|---|---|---|---|---|
| worlds died out (of 256) | **107** | **108** | **2** | **23** | **95** |
| growth multiple (population at year 119 ÷ founders), median [IQR] | 0.65 [0.00, 1.95] | 1.17 [0.00, 3.35] | 1.77 [1.21, 2.30] | 0.56 [0.38, 0.76] | 1.02 [0.00, 2.04] |
| median population, year 119 | 13 | 24 | 142 | 45 | 20 |
| births_per_woman_year | 0.129 | 0.127 | 0.137 | 0.152 | 0.132 |
| child_deaths_per_birth | 0.202 | 0.150 | 0.174 | 0.282 | 0.203 |
| starving_share | 0.036 | 0.027 | 0.034 | 0.046 | 0.036 |
| block_no_partner | 0.564 | 0.568 | 0.480 | 0.462 | 0.551 |

## The three primary questions

### Does a larger world change survival?

L (80×80, 20) against C (40×40, 20): died out 108 vs 107; saved / lost 63 / 64; exact sign test **p = 1.000** (Holm-adjusted 1.000). Effect (C − L extinction share) -0.004, 95% interval [-0.090, +0.082]; half of F2's effect 0.142. Growth multiple, paired Wilcoxon p = 8.42e-05.

Frozen rule: **no meaningful effect** (the interval excludes half of F2's effect).

### Does adding founders change survival, given the larger world?

LP (80×80, 80) against L (80×80, 20): died out 2 vs 108; saved / lost 106 / 0; exact sign test **p = 0.000** (Holm-adjusted 0.000). Effect (L − LP extinction share) +0.414, 95% interval [+0.355, +0.473]; half of F2's effect 0.144. Growth multiple, paired Wilcoxon p = 0.566.

Frozen rule: **the change improves survival**; its size is the effect estimate.

### Does adding founders change survival without more land?

P (40×40, 80) against C (40×40, 20): died out 23 vs 107; saved / lost 88 / 4; exact sign test **p = 0.000** (Holm-adjusted 0.000). Effect (C − P extinction share) +0.328, 95% interval [+0.266, +0.391]; half of F2's effect 0.142. Growth multiple, paired Wilcoxon p = 2.94e-10.

Frozen rule: **the change improves survival**; its size is the effect estimate.

Sham against C: died out 95 vs 107; 46 / 34; p = 0.219.

**Descriptive only:** LP against C (land and people together): died out 2 vs 107; LP against P (land, given 80 founders): 2 vs 23.
