# CO2 — What makes the other options beat making under nature v9? Results

Frozen as `CO2-frozen`. run_co2.py (CO1's runner on code_v9 + the curiosity split), analyse_co2.py (CO1's analysis + Q5; written before data).

## Validity

- Zero checks: **yes**
- All worlds present (32 of 32): **yes**
- One fingerprint (`code_v9`): **yes**
- The identity holds in every logged week (family and identity mismatches 0): **yes**

**Valid.**

## Population and people within reach (adults, offered weeks; worlds alive at each bin's start)

| bin | worlds | offered weeks | people within reach (mean) | U_other (mean) | chosen / offered |
|---|---|---|---|---|---|
| 0-5 | 32 | 66653 | 7.15 | 1.309 | 0.0353 |
| 5-10 | 32 | 152924 | 6.55 | 1.342 | 0.0306 |
| 10-20 | 32 | 333001 | 7.71 | 1.369 | 0.0257 |
| 20-50 | 32 | 1680166 | 10.23 | 1.585 | 0.0112 |
| 50-100 | 32 | 3817604 | 13.06 | 1.819 | 0.0043 |
| 100-200 | 32 | 8452691 | 14.78 | 2.000 | 0.0020 |

## Q1 — Which families? (adults, offered weeks, all worlds alive at each bin's start)

Share of the competing weight s_a (mean over offered weeks); entries n_a, habit h_a and per-entry score M_a are means over the weeks the family is present.

| family | s 0-5 | s 5-10 | s 10-20 | s 20-50 | s 50-100 | s 100-200 | n early → late | h early → late | M early → late |
|---|---|---|---|---|---|---|---|---|---|
| forage | 0.471 | 0.479 | 0.432 | 0.410 | 0.403 | 0.395 | 1.00 → 1.00 | 0.057 → 0.642 | 0.961 → 0.868 |
| gather | 0.034 | 0.044 | 0.068 | 0.122 | 0.168 | 0.205 | 1.00 → 1.00 | 0.003 → 0.408 | 0.308 → 1.025 |
| talk | 0.111 | 0.111 | 0.132 | 0.119 | 0.117 | 0.114 | 6.62 → 9.72 | 0.027 → 0.520 | 0.213 → 0.166 |
| put | 0.029 | 0.039 | 0.056 | 0.088 | 0.103 | 0.114 | 1.00 → 1.00 | 0.002 → 0.309 | 0.281 → 0.676 |
| give | 0.067 | 0.079 | 0.082 | 0.098 | 0.103 | 0.092 | 6.13 → 9.45 | 0.055 → 0.777 | 0.354 → 0.215 |
| join | 0.127 | 0.113 | 0.121 | 0.111 | 0.083 | 0.066 | 1.62 → 1.73 | 0.008 → 0.389 | 0.519 → 0.498 |
| rest | 0.050 | 0.044 | 0.036 | 0.019 | 0.009 | 0.006 | 1.00 → 1.00 | 0.005 → 0.131 | 0.373 → 0.343 |
| care | 0.030 | 0.022 | 0.016 | 0.009 | 0.004 | 0.002 | 1.40 → 1.25 | 0.008 → 0.115 | 0.443 → 0.393 |
| explore | 0.033 | 0.032 | 0.028 | 0.010 | 0.003 | 0.002 | 1.23 → 1.09 | 0.002 → 0.037 | 0.247 → 0.239 |
| play | 0.028 | 0.021 | 0.016 | 0.006 | 0.003 | 0.001 | 1.00 → 1.00 | 0.002 → 0.047 | 0.240 → 0.243 |

## Q2 — The exact split of the rise in U_other (primary)

Adults, offered weeks; early = years 0-10, late = years 100-200; worlds alive at year 100 (32); 24 matched states (hunger × tool × food), late weighted to the early offered weeks.

- U_other: 1.332 → 1.972; **Δ = +0.639 [0.633, 0.646]**.

| part | Δ | share of the rise |
|---|---|---|
| habit | +0.559 [0.55, 0.569] | 0.87 |
| multiplicity | +0.011 [0.00543, 0.0157] | 0.02 |
| per-entry score | +0.128 [0.115, 0.142] | 0.20 |
| spread | -0.059 [-0.0605, -0.057] | -0.09 |
| **total** | +0.639 | 1.00 |

(Exactness check: Δ minus the parts = -8.88e-16.)

**The part carrying the largest share of the rise: habit.**

By family (habit + multiplicity + per-entry score), largest contributions:

| family | habit | multiplicity | per-entry score | total |
|---|---|---|---|---|
| gather | +0.085 | +0.000 | +0.226 | +0.311 |
| forage | +0.267 | +0.000 | -0.042 | +0.224 |
| put | +0.046 | +0.000 | +0.112 | +0.158 |
| talk | +0.068 | +0.008 | -0.009 | +0.067 |
| give | +0.066 | +0.012 | -0.020 | +0.057 |
| join | +0.027 | -0.006 | -0.066 | -0.044 |
| rest | +0.001 | +0.000 | -0.025 | -0.024 |
| care | +0.000 | -0.001 | -0.019 | -0.020 |

## Q3 — Counterfactual swaps (diagnostic; within each world, its own early means; late = years 100-200)

Mean log-odds of choosing make (matched): early -5.05, late -8.06 (fall 3.00).

| late, with this part set back to its early value | mean log-odds | share of the fall undone |
|---|---|---|
| (i) entries | -7.99 | 0.02 |
| (ii) habits | -5.36 | 0.90 |
| (iii) per-entry scores | -7.35 | 0.24 |
| (iv) all three | -4.41 | 1.21 |

(v) Grouped (every family one entry): early -4.76, late -7.72; actual early -5.05, late -8.06. The swaps interact; their shares need not add up.

## Q4 — Described

Habit h_a (mean when present), by bin, for the main families:

| family | 0-5 | 5-10 | 10-20 | 20-50 | 50-100 | 100-200 |
|---|---|---|---|---|---|---|
| forage | 0.037 | 0.066 | 0.112 | 0.256 | 0.467 | 0.642 |
| gather | 0.001 | 0.004 | 0.014 | 0.071 | 0.223 | 0.408 |
| talk | 0.014 | 0.033 | 0.078 | 0.183 | 0.352 | 0.520 |
| put | 0.000 | 0.002 | 0.008 | 0.049 | 0.162 | 0.309 |
| give | 0.023 | 0.069 | 0.152 | 0.371 | 0.624 | 0.777 |
| join | 0.003 | 0.010 | 0.030 | 0.102 | 0.239 | 0.389 |

Forage per-entry score M by hunger band, early and late:

- hunger band 0: 0.494 → 0.428
- hunger band 1: 0.975 → 0.935
- hunger band 2: 1.393 → 1.375
- hunger band 3: 1.871 → 1.837

## Q5 — Which part carries making's deficit under v9 (primary for v9)

Adults, weeks with making offered, years 100-200 (8,452,691 person-weeks in 32 worlds). The gap U_other - U_m splits exactly into habit, curiosity, multiplicity and spread, and the built-in and thought pull. World bootstrap, 10,000 replicates, generator seed 20261101.

| part | mean per week | share of the gap [95%] |
|---|---|---|
| the gap U_other - U_m | 1.6430 | 1 |
| habit | +0.5772 | +0.351 [+0.346, +0.356] |
| curiosity | -0.0836 | -0.051 [-0.053, -0.049] |
| multiplicity and spread | +0.2262 | +0.138 [+0.133, +0.142] |
| built-in and thought pull | +0.9232 | +0.562 [+0.554, +0.571] |

Making's own score: habit 0.0415, curiosity 0.0913; the competitors' weighted curiosity 0.0076.

**Reading: built-in pull carries it.** **Curiosity works against the gap (it favours making).**

