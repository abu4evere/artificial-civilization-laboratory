# LA1 — Why are lessons refused? Results

Frozen as `LA1-frozen` (operational note 1). run_la1.py, analyse_la1.py (written before data).

## Validity

- Zero checks: **yes**
- All worlds present (32 of 32): **yes**
- One fingerprint (`code_v7`): **yes**
- Credence replays exactly and every outcome matches its gate (mismatches 0): **yes**

**Valid.**

## Q1 — The rejection funnel (world-born useful kinds; all ages)

| era | offered | G1 known | G2 tried-and-bad | G3 not taken up | G4 cannot follow (part shown) | taken | taken exactly as meant | taken, then pushed out of a full memory | overlapping: known / tried-and-bad / cannot follow | shown as a variant | part lessons |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0-50 | 172203 | 0.041 | 0.000 | 0.741 | 0.194 | 0.0236 | 0.0180 | 0.562 of taken | 0.041 / 0.000 / 0.862 | 0.187 | 21953 |
| 50-100 | 173172 | 0.031 | 0.000 | 0.753 | 0.195 | 0.0212 | 0.0154 | 0.547 of taken | 0.031 / 0.000 / 0.876 | 0.215 | 20844 |
| 100-200 | 206088 | 0.033 | 0.000 | 0.766 | 0.177 | 0.0247 | 0.0168 | 0.374 of taken | 0.033 / 0.000 / 0.851 | 0.240 | 21019 |

## Q2 — Threshold margins (lessons reaching G3)

| era | reached G3 | mean p | p < 0.05 | p < 0.10 | p < 0.20 | mean credence | mean openness | parent lessons | credence: base | credence: child | credence: health | credence: evidence | credence: overthink | credence: clamp |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0-50 | 165086 | 0.227 | 0.004 | 0.051 | 0.492 | 0.632 | 0.354 | 0.039 | +0.551 | +0.026 | +0.067 | +0.019 | -0.027 | -0.005 |
| 50-100 | 167789 | 0.223 | 0.002 | 0.043 | 0.569 | 0.598 | 0.362 | 0.067 | +0.513 | +0.030 | +0.068 | +0.013 | -0.022 | -0.004 |
| 100-200 | 199313 | 0.209 | 0.002 | 0.039 | 0.639 | 0.572 | 0.354 | 0.059 | +0.484 | +0.026 | +0.067 | +0.012 | -0.014 | -0.003 |

## Q3 — Acceptance and mean p by kind, relation and age

| group | offered | taken / offered | mean p at G3 |
|---|---|---|---|
| founder kinds, useful | 786106 | 0.0837 | 0.223 |
| world-born kinds, useful | 551463 | 0.0232 | 0.219 |
| world-born kinds, not useful | 19115 | 0.1168 | 0.215 |
| world-born useful, teacher is parent | 34081 | 0.0662 | 0.603 |
| world-born useful, teacher is carer | 1790 | 0.0514 | 0.485 |
| world-born useful, teacher is kin | 228278 | 0.0232 | 0.237 |
| world-born useful, teacher is other | 287314 | 0.0180 | 0.164 |
| world-born useful, learner child | 149023 | 0.0271 | 0.286 |
| world-born useful, learner teen | 60407 | 0.0235 | 0.216 |
| world-born useful, learner adult | 342033 | 0.0215 | 0.190 |
| world-born useful, years 0-50 | 172203 | 0.0236 | 0.227 |
| world-born useful, years 50-100 | 173172 | 0.0212 | 0.223 |
| world-born useful, years 100-200 | 206088 | 0.0247 | 0.209 |

## Q4 — Why acceptance falls after year 50 (primary; years 0-50 against 100-200; world-born useful kinds)

Expected acceptance P(taken) = T1 × T2 × T3 × T4 (p's expectation, not the random draw).

| term | years 0-50 | years 100-200 | Δ ln | share of the fall |
|---|---|---|---|---|
| T1 passes G1 (not known) | 0.9587 | 0.9671 | +0.009 [0.00173, 0.0168] | 0.16 |
| T2 passes G2 (not tried-and-bad) | 1.0000 | 1.0000 | +0.000 [0, 0] | 0.00 |
| T3 mean p at G3 | 0.2272 | 0.2087 | -0.085 [-0.114, -0.0534] | -1.59 |
| T4 passes G4 (can follow; p-weighted) | 0.1082 | 0.1231 | +0.129 [0.0367, 0.228] | 2.43 |
| **P(taken), expected** | 0.0236 | 0.0248 | +0.053 [-0.0376, 0.155] | 1.00 |

**The term carrying the largest share of the fall: T3 mean p at G3.**

Mean p at G3: 0.2272 → 0.2087 (Δ -0.0185) = credence part -0.0211 + openness part +0.0002 + covariance +0.0024.

Mean credence by part: base +0.551 → +0.484; child +0.026 → +0.026; health +0.067 → +0.067; evidence +0.019 → +0.012; overthink -0.027 → -0.014; clamp -0.005 → -0.003 (total 0.632 → 0.572).

## Q5 — Counterfactual gate replay (diagnostic; years 100-200, world-born useful kinds)

Over the 199311 lessons reaching G3 with an early match (2 without one), expected lessons taken: actual 5121.1.

| set back alone | expected taken | × actual |
|---|---|---|
| (a) p to its years 0-50 mean (same relation and learner age) | 5411.7 | 1.06 |
| (b) credence alone | 5382.1 | 1.05 |
| (c) openness alone | 5146.2 | 1.00 |
| (d) G1 removed (all lessons in the era) | 7373.7 | 1.44 (against 5121.1) |
| (e) G4 removed (all lessons in the era) | 41601.4 | 8.12 (against 5121.1) |

