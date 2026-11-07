# FP1: food production by age in nature v15, against forager evidence (results)

Frozen as `FP1-frozen`. run_fp1.py, analyse_fp1.py (written before data). A table beside the evidence; no pass/fail.

## Validity

- Zero checks (All: PASS, `code_v15` fingerprint): **yes**
- All worlds present (32): **yes**
- One fingerprint, `code_v15`'s: **yes**
- Every person-week in every world conserves held food (breaches: 0): **yes**

**Valid.**

## 1. Production ÷ need by age band and sex (forage + hunt, over all weeks) [95%, worlds resampled]

| band | sex | person-weeks | production per person-week | need per person-week | production ÷ need |
|---|---|---|---|---|---|
| 0-2 | F | 631,429 | 0.000 | 3.328 | 0.000 [0.000, 0.000] |
| 3-7 | F | 1,023,025 | 1.766 | 3.998 | 0.442 [0.439, 0.444] |
| 8-11 | F | 814,827 | 4.826 | 3.999 | 1.207 [1.202, 1.213] |
| 12-15 | F | 814,715 | 6.606 | 5.997 | 1.101 [1.099, 1.104] |
| 16-29 | F | 2,752,042 | 8.427 | 7.072 | 1.192 [1.184, 1.200] |
| 30-39 | F | 1,649,778 | 9.496 | 7.126 | 1.333 [1.323, 1.341] |
| 40-49 | F | 1,290,470 | 9.277 | 7.069 | 1.312 [1.301, 1.324] |
| 50+ | F | 1,757,078 | 6.313 | 5.997 | 1.053 [1.050, 1.055] |
| 0-2 | M | 683,831 | 0.000 | 3.327 | 0.000 [0.000, 0.000] |
| 3-7 | M | 1,108,752 | 1.766 | 3.998 | 0.442 [0.440, 0.444] |
| 8-11 | M | 883,142 | 4.828 | 3.998 | 1.207 [1.202, 1.213] |
| 12-15 | M | 885,925 | 6.603 | 5.997 | 1.101 [1.098, 1.104] |
| 16-29 | M | 3,073,868 | 7.682 | 6.997 | 1.098 [1.096, 1.100] |
| 30-39 | M | 2,053,336 | 7.731 | 6.997 | 1.105 [1.103, 1.107] |
| 40-49 | M | 1,856,512 | 7.674 | 6.997 | 1.097 [1.094, 1.100] |
| 50+ | M | 2,741,377 | 6.318 | 5.997 | 1.054 [1.051, 1.056] |

Crossover (the first band whose production ÷ need is at least 1): F: 8-11; M: 8-11. Evidence (Kaplan et al. 2000): no forager child produced as much as consumed until the mid-to-late teens.

## 2. Prime adults: production ÷ need, over all weeks and per active week (forage or hunt)

| band | sex | all weeks | per active week | share of weeks active |
|---|---|---|---|---|
| 30-39 | F | 1.333 [1.323, 1.341] | 2.931 [2.905, 2.960] | 0.453 [0.447, 0.459] |
| 40-49 | F | 1.312 [1.301, 1.324] | 2.962 [2.933, 2.993] | 0.442 [0.435, 0.449] |
| 30-39 | M | 1.105 [1.103, 1.107] | 3.010 [2.976, 3.046] | 0.367 [0.363, 0.371] |
| 40-49 | M | 1.097 [1.094, 1.100] | 3.018 [2.985, 3.054] | 0.363 [0.359, 0.367] |

Evidence (Kaplan et al. 2000, Table 2 ÷ Table 3, the assistant's arithmetic): grown men's production ÷ per-capita intake 1.37–3.22 (eight societies), women's 0.39–1.64. Per-capita intake counts children as full consumers, and ACL's need is a fixed requirement: shape and direction, not level.

## 3. The hunted share

- Of production (forage + hunt): **0.000 [0.000, 0.000]**.
- Hunt per person-week: 0.0000; of all food acquired (production + transfers in): 0.0000.
- Evidence (Kaplan et al. 2000, Table 3): 26–78% of the diet hunted over ten societies, median 68.7%.

## 4. The action budget of the grown (16 and over): share of person-weeks

| action | weeks | share |
|---|---|---|
| forage | 6,759,339 | 0.3936 |
| gather | 4,134,564 | 0.2407 |
| put | 1,981,381 | 0.1154 |
| talk | 1,635,812 | 0.0952 |
| give | 1,365,823 | 0.0795 |
| join | 1,023,950 | 0.0596 |
| rest | 149,862 | 0.0087 |
| care | 35,092 | 0.0020 |
| make | 23,876 | 0.0014 |
| explore | 21,622 | 0.0013 |
| play | 21,126 | 0.0012 |
| court | 15,864 | 0.0009 |
| steal | 2,286 | 0.0001 |
| hunt | 1,880 | 0.0001 |
| take | 1,735 | 0.0001 |
| flee | 195 | 0.0000 |
| heat | 39 | 0.0000 |
| attack | 14 | 0.0000 |
| fill | 1 | 0.0000 |

Forage offered in 12,414,127 of 17,174,461 grown weeks, chosen 6,759,339; hunt offered 234,520, chosen 1,880.

Hunts by party size (tried, succeeded): 1: 2,092, 99.

## 5. Losses and unmet need

| band | rot ÷ production | unmet ÷ need |
|---|---|---|
| 0-2 | nan | 0.0313 |
| 3-7 | 0.0732 | 0.0184 |
| 8-11 | 0.0608 | 0.0001 |
| 12-15 | 0.0730 | 0.0091 |
| 16-29 | 0.0749 | 0.0123 |
| 30-39 | 0.0745 | 0.0132 |
| 40-49 | 0.0761 | 0.0118 |
| 50+ | 0.0758 | 0.0080 |

## 6. Where children's food comes from (under 16)

| source | share |
|---|---|
| their own production | 0.6758 |
| fed_in | 0.2243 |
| by:give | 0.0998 |
| act:take | 0.0000 |
| act:steal | 0.0000 |
| death:inherited | 0.0000 |

