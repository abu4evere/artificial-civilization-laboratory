# BL0 — does ACL's brain meaningfully learn? Results (holdout)

Frozen as `BL0-frozen`, with Amendment 1 (`BL0-amend1`, part T). run_bl0.py, analyse_bl0.py.

## Validity

- Logging copy reproduces the control world; parts add up (zero check): **yes**
- One code fingerprint (`code_bl0`): **yes**
- I + C + E + T = habit, and the origin split = habit, every person every week: largest error 4.4e-15 (**yes**, ≤ 1e-9)
- People first seen with habits the observer had not followed: 0 (must be 0)
- Worlds: 32; deepest generation: 6

**Valid.**

## Population and survival (rules 14 and 18)

Survived 120 years: 18 of 32. Median population at years 10 / 30 / 60 / 90 / 120: 24 / 25 / 19 / 22 / 18.

## Q1 — habits' effect on scores and on choices

**Choice effect, mean over adult decisions** (probability the choice would differ without the learned term), median across worlds [95% interval]: **0.139 [0.123, 0.150]** → decision rule: **habits steer**

Adult decisions whose top-scoring option changes without the learned term: 0.149 [0.130, 0.155]

| age | choice effect (median of world means) | top option changes |
|---|---|---|
| 1–4 | 0.066 | 0.074 |
| 5–11 | 0.115 | 0.130 |
| 12–15 | 0.139 | 0.148 |
| 16–29 | 0.141 | 0.141 |
| 30–44 | 0.140 | 0.144 |
| 45+ | 0.162 | 0.168 |

Score effect per action (all decisions, all worlds pooled; medians approximate to one histogram bin):

| action | median abs learned | median abs instinct | ratio |
|---|---|---|---|
| rest | 0.0557 | 0.1870 | 0.298 |
| forage | 0.4030 | 0.6813 | 0.591 |
| hunt | 0.0014 | 0.1591 | 0.009 |
| gather | 0.0316 | 0.3293 | 0.096 |
| put | 0.0220 | 0.1199 | 0.183 |
| take | 0.0000 | 0.1106 | 0.000 |
| make | 0.0094 | 0.1796 | 0.052 |
| play | 0.0125 | 0.1354 | 0.092 |
| explore | 0.0106 | 0.1410 | 0.075 |
| give | 0.6543 | 0.0868 | 7.537 |
| care | 0.0403 | 0.1591 | 0.253 |
| talk | 0.2584 | 0.1528 | 1.691 |
| court | 0.0120 | 0.2198 | 0.055 |
| steal | 0.0008 | 0.1657 | 0.005 |
| attack | 0.0000 | 0.3870 | 0.000 |
| flee | 0.0000 | 0.2917 | 0.000 |
| join | 0.1796 | 0.3870 | 0.464 |

## Q2 — where the habit term comes from (adults)

| part | share of the choice effect (weighted) | share of the habit term (unweighted) |
|---|---|---|
| inherited (I) | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| caregiver (C) | 0.064 [0.033, 0.079] | 0.059 [0.026, 0.080] |
| own experience (E) | 0.372 [0.358, 0.400] | 0.427 [0.395, 0.445] |
| copied in talk (T) | 0.560 [0.520, 0.597] | 0.505 [0.467, 0.535] |

Own experience's share → decision rule: **mixed**

By age (yearly snapshots, all worlds pooled): values with |E| ≥ 0.05 (of 544), and each part's share:

| age | people-years | values with own experience | I | C | E | T |
|---|---|---|---|---|---|---|
| 1–4 | 9503 | 6 | 0.036 | 0.824 | 0.048 | 0.092 |
| 5–11 | 15052 | 10 | 0.000 | 0.801 | 0.062 | 0.136 |
| 12–15 | 7960 | 22 | 0.000 | 0.527 | 0.151 | 0.322 |
| 16–29 | 26626 | 34 | 0.000 | 0.143 | 0.408 | 0.449 |
| 30–44 | 19403 | 39 | 0.000 | 0.029 | 0.440 | 0.530 |
| 45+ | 7982 | 42 | 0.000 | 0.007 | 0.363 | 0.629 |

## Q3 — persistence

Later life: when a situation comes back with habits not used for 52+ weeks, their mean abs value 0.320 [0.165, 0.390]; the choice effect of those habits alone 0.065 [0.043, 0.070].

Descendants (all children pooled; correlation over the 544 values with parents' habits at birth, and with an unrelated adult's; described, not thresholded):

| age | children | parents r (mean) | unrelated adult r (mean) | parents − unrelated [95% interval] | I share | E share |
|---|---|---|---|---|---|---|
| 12 | 2023 | 0.964 | 0.922 | 0.043 [0.040, 0.046] | 0.000 | 0.063 |
| 20 | 1733 | 0.955 | 0.914 | 0.040 [0.037, 0.044] | 0.000 | 0.307 |
| 40 | 846 | 0.912 | 0.870 | 0.043 [0.038, 0.048] | 0.000 | 0.366 |

Lineage: adults' share of the habit term that traces to the experience of people two or more generations above them: 0.079 [0.014, 0.086]

## Q4 — reach and staleness

Situations recurring per person-year (32 situations; all worlds pooled): 0.1, 0.1, 0.1, 0.1, 3.1, 2.7, 2.8, 3.9, 0.1, 0.1, 0.1, 0.2, 4.9, 4.8, 4.9, 5.4, 0.1, 0.1, 0.1, 0.1, 4.6, 5.1, 4.8, 3.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.1, 0.0.
Weeks since the chosen habit value last changed, when used: median 3 (capped at 520).

## Do discovery and holdout agree? (a label is read only where they agree)

| rule | discovery | holdout | stands |
|---|---|---|---|
| Q1 | habits steer (0.140 [0.128, 0.159]) | habits steer (0.139 [0.123, 0.150]) | **yes: habits steer** |
| Q2 | mixed (0.372 [0.359, 0.386]) | mixed (0.372 [0.358, 0.400]) | **yes: mixed** |
