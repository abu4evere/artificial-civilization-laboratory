# BL0 — does ACL's brain meaningfully learn? Results (discovery)

Frozen as `BL0-frozen`, with Amendment 1 (`BL0-amend1`, part T). run_bl0.py, analyse_bl0.py.

## Validity

- Logging copy reproduces the control world; parts add up (zero check): **yes**
- One code fingerprint (`code_bl0`): **yes**
- I + C + E + T = habit, and the origin split = habit, every person every week: largest error 4.9e-15 (**yes**, ≤ 1e-9)
- People first seen with habits the observer had not followed: 0 (must be 0)
- Worlds: 32; deepest generation: 6

**Valid.**

## Population and survival (rules 14 and 18)

Survived 120 years: 24 of 32. Median population at years 10 / 30 / 60 / 90 / 120: 21 / 24 / 26 / 28 / 31.

## Q1 — habits' effect on scores and on choices

**Choice effect, mean over adult decisions** (probability the choice would differ without the learned term), median across worlds [95% interval]: **0.140 [0.128, 0.159]** → decision rule: **habits steer**

Adult decisions whose top-scoring option changes without the learned term: 0.143 [0.131, 0.166]

| age | choice effect (median of world means) | top option changes |
|---|---|---|
| 1–4 | 0.081 | 0.079 |
| 5–11 | 0.122 | 0.133 |
| 12–15 | 0.146 | 0.150 |
| 16–29 | 0.137 | 0.141 |
| 30–44 | 0.134 | 0.138 |
| 45+ | 0.161 | 0.166 |

Score effect per action (all decisions, all worlds pooled; medians approximate to one histogram bin):

| action | median abs learned | median abs instinct | ratio |
|---|---|---|---|
| rest | 0.0604 | 0.1796 | 0.336 |
| forage | 0.4369 | 0.7094 | 0.616 |
| hunt | 0.0018 | 0.1657 | 0.011 |
| gather | 0.0269 | 0.2801 | 0.096 |
| put | 0.0166 | 0.1152 | 0.144 |
| take | 0.0001 | 0.1152 | 0.001 |
| make | 0.0111 | 0.1725 | 0.064 |
| play | 0.0135 | 0.1410 | 0.096 |
| explore | 0.0120 | 0.1410 | 0.085 |
| give | 0.6543 | 0.0801 | 8.171 |
| care | 0.0420 | 0.1528 | 0.275 |
| talk | 0.2801 | 0.1528 | 1.833 |
| court | 0.0135 | 0.2289 | 0.059 |
| steal | 0.0011 | 0.1591 | 0.007 |
| attack | 0.0000 | 0.3717 | 0.000 |
| flee | 0.0000 | 0.2584 | 0.000 |
| join | 0.2028 | 0.4030 | 0.503 |

## Q2 — where the habit term comes from (adults)

| part | share of the choice effect (weighted) | share of the habit term (unweighted) |
|---|---|---|
| inherited (I) | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| caregiver (C) | 0.056 [0.034, 0.079] | 0.052 [0.031, 0.076] |
| own experience (E) | 0.372 [0.359, 0.386] | 0.398 [0.372, 0.441] |
| copied in talk (T) | 0.569 [0.540, 0.603] | 0.524 [0.479, 0.550] |

Own experience's share → decision rule: **mixed**

By age (yearly snapshots, all worlds pooled): values with |E| ≥ 0.05 (of 544), and each part's share:

| age | people-years | values with own experience | I | C | E | T |
|---|---|---|---|---|---|---|
| 1–4 | 11058 | 6 | 0.035 | 0.822 | 0.046 | 0.097 |
| 5–11 | 17213 | 11 | 0.000 | 0.800 | 0.060 | 0.140 |
| 12–15 | 9009 | 22 | 0.000 | 0.512 | 0.147 | 0.340 |
| 16–29 | 29590 | 34 | 0.000 | 0.134 | 0.391 | 0.476 |
| 30–44 | 20891 | 38 | 0.000 | 0.023 | 0.418 | 0.558 |
| 45+ | 8893 | 38 | 0.000 | 0.005 | 0.349 | 0.645 |

## Q3 — persistence

Later life: when a situation comes back with habits not used for 52+ weeks, their mean abs value 0.366 [0.300, 0.395]; the choice effect of those habits alone 0.068 [0.062, 0.072].

Descendants (all children pooled; correlation over the 544 values with parents' habits at birth, and with an unrelated adult's; described, not thresholded):

| age | children | parents r (mean) | unrelated adult r (mean) | parents − unrelated [95% interval] | I share | E share |
|---|---|---|---|---|---|---|
| 12 | 2317 | 0.970 | 0.926 | 0.045 [0.041, 0.048] | 0.000 | 0.061 |
| 20 | 1991 | 0.961 | 0.918 | 0.043 [0.040, 0.047] | 0.000 | 0.300 |
| 40 | 952 | 0.924 | 0.879 | 0.046 [0.040, 0.051] | 0.000 | 0.346 |

Lineage: adults' share of the habit term that traces to the experience of people two or more generations above them: 0.088 [0.072, 0.105]

## Q4 — reach and staleness

Situations recurring per person-year (32 situations; all worlds pooled): 0.0, 0.0, 0.0, 0.1, 3.2, 2.8, 2.8, 4.0, 0.1, 0.1, 0.1, 0.1, 4.9, 4.9, 4.9, 5.4, 0.1, 0.1, 0.1, 0.1, 4.5, 5.0, 4.9, 3.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.0.
Weeks since the chosen habit value last changed, when used: median 3 (capped at 520).
