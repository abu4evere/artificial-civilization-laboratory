# IW1 — How does the worth of made things form? Results

Frozen as `IW1-frozen` (operational note 1). run_iw1.py, analyse_iw1.py (written before data).

## Validity

- Zero checks: **yes**
- All worlds present (32 of 32): **yes**
- One fingerprint (`code_v9`): **yes**
- Worth updates and make scores replay exactly (mismatches 0): **yes**

**Valid.**

Worlds: 32; extinct 0. Mean living population 119.9; adults in years 100-200: 81.0 per world-year.

## Q1 — Calibration at the make (adults, years 100-200)

Makes: 17,094. Under-valuation = mean felt help of the kind - the maker's worth just before making (positive = worth below the help).

| measure | value [95%] |
|---|---|
| **(b) under-valuation, against everyone's uses of the kind** (17,094 makes; kind never used by anyone: 0) | **+0.004 [+0.002, +0.006]** |
| (b) mean felt help per use of the kinds made | 0.163 [0.160, 0.166] |
| (a) under-valuation, against the maker's own later uses (16,495 makes; no later use: 599) | +0.009 [+0.008, +0.011] |

| first source of the kind (the maker's) | makes | mean under-valuation (b) |
|---|---|---|
| made | 13,704 | +0.000 |
| taught | 3,114 | +0.023 |
| read | 276 | -0.024 |

## Q2 — Experience: the maker's prior uses of the kind at each make

| prior uses | makes | share |
|---|---|---|
| 0 | 1,252 | 0.073 |
| 1-2 | 284 | 0.017 |
| 3-5 | 438 | 0.026 |
| 6+ | 15,120 | 0.885 |

**Share resting on fewer than 6 uses: 0.115 [0.101, 0.132].** (GPT: a diagnostic bin, not proof of inadequate learning.)

## Q3 — Worth against uses, by how the person first got the kind (all ages, all years)

Each cell: mean worth just before the use / mean felt help of that use (uses).

| source | use 0 | use 1 | use 2 | use 5 | use 10+ |
|---|---|---|---|---|---|
| made | 0.00 / 0.13 (141,026) | 0.02 / 0.13 (134,103) | 0.04 / 0.12 (129,446) | 0.07 / 0.11 (121,450) | 0.13 / 0.13 (5,329,328) |
| initial | 0.00 / 0.15 (80,515) | 0.02 / 0.16 (76,308) | 0.04 / 0.15 (74,180) | 0.08 / 0.14 (70,382) | 0.14 / 0.15 (2,041,436) |
| taught | 0.08 / 0.18 (8,008) | 0.10 / 0.18 (7,853) | 0.11 / 0.18 (7,772) | 0.13 / 0.17 (7,651) | 0.18 / 0.18 (611,799) |
| read | 0.00 / 0.09 (2,402) | 0.01 / 0.09 (2,366) | 0.02 / 0.08 (2,342) | 0.05 / 0.08 (2,294) | 0.11 / 0.12 (120,326) |
| heated | 0.00 / 0.29 (2,388) | 0.05 / 0.29 (1,580) | 0.08 / 0.29 (1,120) | 0.16 / 0.28 (617) | 0.22 / 0.23 (12,104) |
| copied | 0.18 / 0.16 (31) | 0.17 / 0.19 (31) | 0.16 / 0.24 (31) | 0.17 / 0.16 (30) | 0.09 / 0.09 (1,185) |

## Q4 — Felt help per use (all ages, all years)

| law that judged the use | uses | < 0 | 0-0.1 | 0.1-0.3 | > 0.3 |
|---|---|---|---|---|---|
| `_judge_use` | 5,823,974 | 0.000 | 0.356 | 0.505 | 0.139 |
| `body_phase` | 4,344,112 | 0.000 | 0.415 | 0.566 | 0.018 |
| `_over_water` | 20,259 | 0.000 | 0.000 | 0.418 | 0.582 |
| `_judge_carry` | 902 | 0.000 | 0.000 | 1.000 | 0.000 |
| `drink` | 106 | 0.000 | 0.000 | 0.000 | 1.000 |

Share of all uses with felt help > 0.1: 0.620 of 10,189,353.

## Q5 — How kinds leave a person (classified by that person's own uses)

| reason | helpful (own mean felt > 0.1) | unhelpful | never used by them |
|---|---|---|---|
| limit | 771 | 5,789 | 135,262 |
| forget | 0 | 0 | 0 |
| death | 77,365 | 56,214 | 59,016 |

## Q6 — Are the kinds made the ones that help most?

Spearman correlation per world (late adult makes per kind against the kind's mean felt help): mean -0.091 over 32 worlds (min -0.137, max -0.039).

## Q7 — Offered but not chosen (adults, years 100-200)

Weeks: 8,784,929 (kind never used by anyone: 77). Under-valuation (b): **+0.015 [+0.013, +0.017]**; mean felt help of the kinds offered 0.152 [0.150, 0.155].

Prior uses in these weeks: 0 0.133; 1-2 0.022; 3-5 0.032; 6+ 0.813.

## Q8 — Which term carries making's worth when it is offered (adults, years 100-200, all offers)

| term | share |
|---|---|
| itemval | 0.807 |
| part | 0.181 |
| belief | 0.010 |
| surprise | 0.001 |

## The frozen reading

- Under-valuation (b) +0.004 (lower bound +0.002; needs > 0.10 and > 0 for 'unlearned'); share of makes on fewer than 6 uses 0.115 (needs > 0.5).
- Mean felt help (b) 0.163 (needs < 0.10 for 'honest', with worth within ±0.05).

**Reading: MIXED.**

Sensitivity (described, not decisive): threshold 0.05 / ±0.03: mixed; threshold 0.15 / ±0.03: mixed; threshold 0.05 / ±0.05: mixed; threshold 0.15 / ±0.05: mixed.

