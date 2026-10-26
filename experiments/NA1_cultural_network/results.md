# NA1 — Who actually gets a chance to learn? Results

Frozen as `NA1-frozen` (operational note 1). run_na1.py, analyse_na1.py (written before data).

## Validity

- Zero checks: **yes**
- All worlds present (32 of 32): **yes**
- One fingerprint (`code_v7`): **yes**
- Internal checks (non-knowers only; took only in a lesson; each stage within the one before): **yes**

**Valid.**

## Population and people within reach (aged 4+; worlds alive in the era)

| era (years) | worlds | mean population | people within reach (mean) |
|---|---|---|---|
| 0-50 | 32 | 112.5 | 8.88 |
| 50-100 | 32 | 130.0 | 12.55 |
| 100-200 | 32 | 117.4 | 13.73 |

## Q1 — The effective network, per useful world-born kind

Distinct non-knowers (aged 4+) reaching each stage: with the inventor (while alive) and with any knower (the kind's whole life). Mean / median / share of kinds with none.

| era | kinds | inventor: co-present | inventor: talked | inventor: offered | inventor: took | any: co-present | any: talked | any: offered | any: took | any: made | any: passed | any: took a variant |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0-50 | 12047 | 53.33 / 47 / 0.00 | 44.28 / 39 / 0.01 | 6.61 / 0 / 0.58 | 0.04 / 0 / 0.98 | 108.78 / 66 / 0.00 | 93.66 / 56 / 0.01 | 11.58 / 1 / 0.49 | 0.36 / 0 / 0.93 | 0.01 / 0 / 0.99 | 0.01 / 0 / 1.00 | 0.27 / 0 / 0.91 |
| 50-100 | 5029 | 79.77 / 77 / 0.00 | 66.21 / 63 / 0.00 | 10.44 / 3 / 0.41 | 0.03 / 0 / 0.98 | 88.65 / 82 / 0.00 | 73.86 / 68 / 0.00 | 11.30 / 3 / 0.40 | 0.05 / 0 / 0.97 | 0.00 / 0 / 1.00 | 0.00 / 0 / 1.00 | 0.10 / 0 / 0.95 |
| 100-200 | 3517 | 79.64 / 76 / 0.00 | 65.27 / 63 / 0.00 | 10.42 / 3 / 0.38 | 0.03 / 0 / 0.98 | 81.81 / 77 / 0.00 | 67.18 / 65 / 0.00 | 10.63 / 3 / 0.38 | 0.03 / 0 / 0.98 | 0.00 / 0 / 1.00 | 0.00 / 0 / 1.00 | 0.11 / 0 / 0.94 |

Founders' kinds (described): any co-present 314.02, any talked 291.41, any offered 46.42, any took 12.62, any made 1.98, any passed 0.66 (2640 kinds).

## Q2 — The funnel (primary): pooled over world-born useful kinds, any knower, whole life

**all eras**: co-present 2044075, talked 1736075, offered 233771, took 4694, made 156, passed 95.

| step | rate | ln rate |
|---|---|---|
| co-present → talked | 0.8493 [0.843, 0.856] | -0.163 |
| talked → offered | 0.1347 [0.123, 0.146] | -2.005 |
| offered → took | 0.0201 [0.0177, 0.023] | -3.908 |
| took → made | 0.0332 [0.0241, 0.044] | -3.404 |
| made → passed | 0.6090 [0.451, 0.796] | -0.496 |

**The step with the largest loss (all eras): offered → took.**

**0-50**: co-present 1310519, talked 1128349, offered 139543, took 4338, made 156, passed 93.

| step | rate | ln rate |
|---|---|---|
| co-present → talked | 0.8610 | -0.150 |
| talked → offered | 0.1237 | -2.090 |
| offered → took | 0.0311 | -3.471 |
| took → made | 0.0360 | -3.325 |
| made → passed | 0.5962 | -0.517 |

**The step with the largest loss (0-50): offered → took.**

**50-100**: co-present 445818, talked 371437, offered 56846, took 235, made 0, passed 1.

| step | rate | ln rate |
|---|---|---|
| co-present → talked | 0.8332 | -0.183 |
| talked → offered | 0.1530 | -1.877 |
| offered → took | 0.0041 | -5.489 |
| took → made | 0.0000 | fell to zero |
| made → passed | nan | nan |

**The step with the largest loss (50-100): took → made (fell to zero).**

**100-200**: co-present 287738, talked 236289, offered 37382, took 121, made 0, passed 1.

| step | rate | ln rate |
|---|---|---|
| co-present → talked | 0.8212 | -0.197 |
| talked → offered | 0.1582 | -1.844 |
| offered → took | 0.0032 | -5.733 |
| took → made | 0.0000 | fell to zero |
| made → passed | nan | nan |

**The step with the largest loss (100-200): took → made (fell to zero).**

## Q3 — The ratchet ledger (A → B → C, B improving a kind learned socially)

- World-born useful kinds: 20593. Improvements by a social learner (B): 123 (5.97 per 1,000 kinds). **Completed A→B→C chains: 38 (1.85 per 1,000 kinds).**
- 0-50: improvements 108, completed 36
- 50-100: improvements 9, completed 1
- 100-200: improvements 6, completed 1
- Factor gained by the improvement (mean): +0.259.

## Q4 — Network against population (described; worlds × eras)

| era | worlds | mean population | mean reach (any co-present per kind) | mean took per kind |
|---|---|---|---|---|
| 0-50 | 32 | 112.5 | 104.19 | 0.352 |
| 50-100 | 32 | 130.0 | 83.66 | 0.048 |
| 100-200 | 32 | 117.4 | 74.82 | 0.035 |

Rank correlation of population with a kind's mean reach, across world-eras: 0.59 (96 world-eras; described).

