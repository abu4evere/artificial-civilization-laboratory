# CO1 — What made the other options stronger? Results

Frozen as `CO1-frozen`. run_co1.py, analyse_co1.py (written before data).

## Validity

- Zero checks: **yes**
- All worlds present (32 of 32): **yes**
- One fingerprint (`code_v7`): **yes**
- The identity holds in every logged week (family and identity mismatches 0): **yes**

**Valid.**

## Population and people within reach (adults, offered weeks; worlds alive at each bin's start)

| bin | worlds | offered weeks | people within reach (mean) | U_other (mean) | chosen / offered |
|---|---|---|---|---|---|
| 0-5 | 32 | 66554 | 7.50 | 1.256 | 0.0262 |
| 5-10 | 32 | 165778 | 7.04 | 1.321 | 0.0213 |
| 10-20 | 32 | 377112 | 8.42 | 1.344 | 0.0189 |
| 20-50 | 32 | 1944908 | 11.48 | 1.554 | 0.0081 |
| 50-100 | 32 | 4118406 | 14.06 | 1.800 | 0.0026 |
| 100-200 | 32 | 8342229 | 15.33 | 1.984 | 0.0011 |

## Q1 — Which families? (adults, offered weeks, all worlds alive at each bin's start)

Share of the competing weight s_a (mean over offered weeks); entries n_a, habit h_a and per-entry score M_a are means over the weeks the family is present.

| family | s 0-5 | s 5-10 | s 10-20 | s 20-50 | s 50-100 | s 100-200 | n early → late | h early → late | M early → late |
|---|---|---|---|---|---|---|---|---|---|
| forage | 0.474 | 0.493 | 0.440 | 0.424 | 0.414 | 0.402 | 1.00 → 1.00 | 0.060 → 0.654 | 0.931 → 0.853 |
| gather | 0.031 | 0.036 | 0.052 | 0.094 | 0.141 | 0.177 | 1.00 → 1.00 | 0.003 → 0.354 | 0.238 → 0.879 |
| talk | 0.124 | 0.121 | 0.149 | 0.142 | 0.136 | 0.134 | 6.89 → 9.88 | 0.030 → 0.542 | 0.171 → 0.163 |
| give | 0.072 | 0.082 | 0.087 | 0.109 | 0.116 | 0.104 | 6.38 → 9.64 | 0.058 → 0.791 | 0.297 → 0.215 |
| put | 0.025 | 0.032 | 0.043 | 0.068 | 0.086 | 0.099 | 1.00 → 1.00 | 0.001 → 0.259 | 0.196 → 0.555 |
| join | 0.134 | 0.119 | 0.131 | 0.119 | 0.088 | 0.074 | 1.64 → 1.74 | 0.008 → 0.397 | 0.493 → 0.501 |
| rest | 0.047 | 0.043 | 0.036 | 0.019 | 0.009 | 0.006 | 1.00 → 1.00 | 0.005 → 0.125 | 0.321 → 0.285 |
| care | 0.025 | 0.020 | 0.013 | 0.008 | 0.003 | 0.002 | 1.42 → 1.28 | 0.007 → 0.096 | 0.366 → 0.297 |
| explore | 0.029 | 0.026 | 0.025 | 0.008 | 0.002 | 0.001 | 1.22 → 1.08 | 0.002 → 0.026 | 0.172 → 0.146 |
| play | 0.025 | 0.018 | 0.015 | 0.006 | 0.002 | 0.001 | 1.00 → 1.00 | 0.002 → 0.036 | 0.173 → 0.167 |

## Q2 — The exact split of the rise in U_other (primary)

Adults, offered weeks; early = years 0-10, late = years 100-200; worlds alive at year 100 (32); 24 matched states (hunger × tool × food), late weighted to the early offered weeks.

- U_other: 1.302 → 1.962; **Δ = +0.660 [0.647, 0.672]**.

| part | Δ | share of the rise |
|---|---|---|
| habit | +0.569 [0.559, 0.577] | 0.86 |
| multiplicity | +0.013 [0.00419, 0.021] | 0.02 |
| per-entry score | +0.130 [0.105, 0.154] | 0.20 |
| spread | -0.052 [-0.0534, -0.0496] | -0.08 |
| **total** | +0.660 | 1.00 |

(Exactness check: Δ minus the parts = 2.22e-16.)

**The part carrying the largest share of the rise: habit.**

By family (habit + multiplicity + per-entry score), largest contributions:

| family | habit | multiplicity | per-entry score | total |
|---|---|---|---|---|
| gather | +0.076 | +0.000 | +0.205 | +0.281 |
| forage | +0.273 | +0.000 | -0.044 | +0.229 |
| put | +0.041 | +0.000 | +0.104 | +0.146 |
| talk | +0.077 | +0.009 | -0.005 | +0.081 |
| give | +0.071 | +0.012 | -0.016 | +0.067 |
| join | +0.030 | -0.005 | -0.061 | -0.036 |
| rest | +0.001 | +0.000 | -0.021 | -0.020 |
| care | -0.000 | -0.001 | -0.016 | -0.018 |

## Q3 — Counterfactual swaps (diagnostic; within each world, its own early means; late = years 100-200)

Mean log-odds of choosing make (matched): early -5.41, late -8.62 (fall 3.21).

| late, with this part set back to its early value | mean log-odds | share of the fall undone |
|---|---|---|
| (i) entries | -8.55 | 0.02 |
| (ii) habits | -5.85 | 0.86 |
| (iii) per-entry scores | -7.87 | 0.23 |
| (iv) all three | -4.89 | 1.16 |

(v) Grouped (every family one entry): early -5.08, late -8.23; actual early -5.41, late -8.62. The swaps interact; their shares need not add up.

## Q4 — Described

Habit h_a (mean when present), by bin, for the main families:

| family | 0-5 | 5-10 | 10-20 | 20-50 | 50-100 | 100-200 |
|---|---|---|---|---|---|---|
| forage | 0.038 | 0.069 | 0.118 | 0.265 | 0.481 | 0.654 |
| gather | 0.001 | 0.004 | 0.011 | 0.057 | 0.189 | 0.354 |
| talk | 0.015 | 0.036 | 0.085 | 0.196 | 0.374 | 0.542 |
| give | 0.025 | 0.071 | 0.158 | 0.383 | 0.645 | 0.791 |
| put | 0.000 | 0.002 | 0.007 | 0.038 | 0.132 | 0.259 |
| join | 0.003 | 0.011 | 0.032 | 0.106 | 0.245 | 0.397 |

Forage per-entry score M by hunger band, early and late:

- hunger band 0: 0.432 → 0.406
- hunger band 1: 0.959 → 0.932
- hunger band 2: 1.387 → 1.368
- hunger band 3: 1.865 → 1.825

