# PB3: memory steering as a candidate law — prediction or myopia? (results)

Frozen as `PB3-frozen`. run_pb3.py, analyse_pb3.py (written before data). Adults 16–49, years 130–170.

## Validity

- Zero checks (All: PASS, same `code_pb3` fingerprint): **yes**
- All worlds present (160 of 160): **yes**
- One fingerprint, `code_pb3`'s: **yes**

**Valid.**

## Guards (each arm against v13)

- v13, discount 0: living-weeks ratio 1.166 [1.028, 1.321]; extinct worlds beyond v13's +1 — no guard raised
- P (memory): living-weeks ratio 1.276 [1.231, 1.325]; extinct worlds beyond v13's +0 — no guard raised
- P+ (memory, two-week return): living-weeks ratio 1.306 [1.260, 1.357]; extinct worlds beyond v13's +0 — no guard raised
- sham: living-weeks ratio 1.016 [0.892, 1.154]; extinct worlds beyond v13's +1 — no guard raised

Rule: a guard is raised if the living-weeks ratio is below 0.90 with its upper bound below 1, or 3+ extra extinct worlds. An arm with a guard raised is not read as a success.

## M3, ends-directed chains

P(made a recipe using m within 8 weeks | gathered m, a needed input of a valued recipe, holding < 1) − P(made | an opportunity-matched week).

| arm | M3 | gather chains | matched chains |
|---|---|---|---|
| v13 | 0.0035 | 284,503 | 2,659,469 |
| v13, discount 0 | 0.0263 | 380,653 | 3,640,739 |
| P (memory) | 0.0203 | 258,999 | 3,634,964 |
| P+ (memory, two-week return) | 0.0149 | 293,961 | 3,865,287 |
| sham | 0.0034 | 284,309 | 2,692,961 |

| contrast | M3 difference [95%] |
|---|---|
| P (memory) − v13, discount 0 (primary) | -0.0059 [-0.0076, -0.0044] |
| P (memory) − v13 (co-primary) | +0.0169 [+0.0146, +0.0193] |
| v13, discount 0 − v13 | +0.0228 [+0.0211, +0.0245] |
| P+ (memory, two-week return) − P (memory) | -0.0055 [-0.0067, -0.0042] |
| P+ (memory, two-week return) − v13, discount 0 | -0.0114 [-0.0128, -0.0100] |
| P+ (memory, two-week return) − v13 | +0.0114 [+0.0097, +0.0131] |
| sham − v13 | -0.0000 [-0.0003, +0.0003] |

## Primary: attribution (P − c0 on M3)

Rule: "better prediction" if the 95% interval of P − c0 lies wholly above 0 and its point is at least +0.005; "myopia, not prediction" if it does not lie wholly above 0 while c0 − c lies wholly above 0; otherwise "unclear" (guards first).

**Primary reading: myopia, not prediction.**

Described: Gemini's stricter check, P − c0 ≥ +0.015: no.

## Co-primary: replication of PB2 (P − c on M3, P / c living-weeks)

- P − c on M3: +0.0169 [+0.0146, +0.0193]
- P / c living-weeks: 1.276 [1.231, 1.325]

Rule: "PB2's steering effect replicates" if the M3 interval lies wholly above 0 and the living-weeks interval wholly above 1.

**Co-primary reading: PB2's steering effect replicates.**

## Described (no frozen prediction)

**Living-weeks ratios.**

- v13, discount 0 / v13: 1.166 [1.028, 1.321]
- P+ (memory, two-week return) / P (memory): 1.023 [0.982, 1.068]
- P+ (memory, two-week return) / v13, discount 0: 1.120 [0.991, 1.267]
- P (memory) / v13, discount 0: 1.095 [0.968, 1.239]

**M5 (chains whose next decision was a food action).**

| arm | M5 |
|---|---|
| v13 | 0.0035 |
| v13, discount 0 | 0.0276 |
| P (memory) | 0.0203 |
| P+ (memory, two-week return) | 0.0148 |
| sham | 0.0034 |

| contrast | M5 difference [95%] |
|---|---|
| P (memory) − v13, discount 0 | -0.0073 [-0.0092, -0.0056] |
| P (memory) − v13 | +0.0168 [+0.0145, +0.0194] |
| v13, discount 0 − v13 | +0.0242 [+0.0222, +0.0262] |
| P+ (memory, two-week return) − P (memory) | -0.0055 [-0.0069, -0.0040] |
| P+ (memory, two-week return) − v13, discount 0 | -0.0129 [-0.0147, -0.0111] |
| P+ (memory, two-week return) − v13 | +0.0113 [+0.0094, +0.0134] |
| sham − v13 | -0.0001 [-0.0006, +0.0005] |

**R (lineage remaking, as in PB2) and inventors' opportunities.**

| arm | R | kinds | remade | inventor weeks holding the inputs | of which still knew the recipe | others holding |
|---|---|---|---|---|---|---|
| v13 | 0.0008 | 1,284 | 1 | 64 | 1.000 | 4,095 |
| v13, discount 0 | 0.0000 | 11,348 | 0 | 456 | 0.000 | 21,507 |
| P (memory) | 0.0004 | 2,260 | 1 | 429 | 0.294 | 13,277 |
| P+ (memory, two-week return) | 0.0010 | 2,082 | 2 | 347 | 0.383 | 10,157 |
| sham | 0.0000 | 1,266 | 0 | 0 | nan | 5,016 |

**Action shares (adults, years 130–170).**

| action | v13 | v13, discount 0 | P (memory) | P+ (memory, two-week return) | sham |
|---|---|---|---|---|---|
| attack | 0.0000 | 0.0001 | 0.0000 | 0.0000 | 0.0000 |
| care | 0.0025 | 0.0093 | 0.0156 | 0.0149 | 0.0027 |
| court | 0.0013 | 0.0044 | 0.0043 | 0.0040 | 0.0013 |
| explore | 0.0013 | 0.0075 | 0.0033 | 0.0034 | 0.0014 |
| fill | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| flee | 0.0000 | 0.0001 | 0.0000 | 0.0000 | 0.0000 |
| forage | 0.3933 | 0.3819 | 0.4086 | 0.4089 | 0.3975 |
| gather | 0.2442 | 0.2367 | 0.1922 | 0.1897 | 0.2348 |
| give | 0.0791 | 0.0624 | 0.0955 | 0.1024 | 0.0811 |
| heat | 0.0000 | 0.0001 | 0.0000 | 0.0000 | 0.0000 |
| hunt | 0.0001 | 0.0008 | 0.0001 | 0.0001 | 0.0001 |
| join | 0.0604 | 0.0658 | 0.0600 | 0.0626 | 0.0626 |
| make | 0.0012 | 0.0078 | 0.0049 | 0.0037 | 0.0012 |
| play | 0.0012 | 0.0060 | 0.0034 | 0.0031 | 0.0012 |
| put | 0.1144 | 0.1260 | 0.0872 | 0.0906 | 0.1101 |
| rest | 0.0070 | 0.0152 | 0.0116 | 0.0133 | 0.0077 |
| steal | 0.0001 | 0.0013 | 0.0004 | 0.0004 | 0.0001 |
| take | 0.0001 | 0.0006 | 0.0001 | 0.0001 | 0.0001 |
| talk | 0.0939 | 0.0741 | 0.1128 | 0.1028 | 0.0981 |

Share of acts aimed at a person: v13 0.1768; v13, discount 0 0.1515; P (memory) 0.2286; P+ (memory, two-week return) 0.2244; sham 0.1833. P (memory) − v13, discount 0 +0.0771 [+0.0699, +0.0847]; P (memory) − v13 +0.0517 [+0.0473, +0.0564]; v13, discount 0 − v13 -0.0253 [-0.0329, -0.0176].

| measure | v13 | v13, discount 0 | P (memory) | P+ (memory, two-week return) | sham | P − c0 [95%] | c0 − c [95%] |
|---|---|---|---|---|---|---|---|
| M2 (bits beyond shuffle, per adult-year) | 0.1641 | 0.1255 | 0.1283 | 0.1358 | 0.1585 | +0.0029 [-0.0025, +0.0084] | -0.0386 [-0.0448, -0.0324] |
| M3 among people born after year 100: gather chains made | 0.0037 | 0.0280 | 0.0206 | 0.0153 | 0.0036 | -0.0074 [-0.0091, -0.0057] | +0.0243 [+0.0225, +0.0262] |
|   matched chains made (born after year 100) | 0.0003 | 0.0021 | 0.0012 | 0.0009 | 0.0003 | -0.0009 [-0.0011, -0.0006] | +0.0017 [+0.0015, +0.0020] |
| makes per adult-year | 0.0612 | 0.4062 | 0.2548 | 0.1933 | 0.0624 | -0.1514 [-0.1727, -0.1306] | +0.3450 [+0.3227, +0.3666] |
| world-new kinds per world (years 130–165) | 40.1250 | 354.6250 | 70.6250 | 65.0625 | 39.5625 | -284.0000 [-339.8438, -230.1547] | +314.5000 [+256.5922, +373.4375] |
| edible food per adult (year-end census) | 8.9802 | 8.6502 | 8.6672 | 7.8943 | 8.4515 | +0.0169 [-0.4006, +0.4193] | -0.3300 [-0.8029, +0.1582] |
| decisions falling back to q (share) | nan | nan | 0.0086 | 0.0090 | nan | +nan [+nan, +nan] | +nan [+nan, +nan] |
| adult weeks of people born after year 100 (share) | 0.8710 | 0.8912 | 0.9044 | 0.8979 | 0.8757 | +0.0132 [+0.0053, +0.0210] | +0.0202 [+0.0093, +0.0312] |

## Population (beside every measure)

| arm | living-weeks | adult-weeks (16–49) | extinct worlds |
|---|---|---|---|
| v13 | 9,641,726 | 5,088,418 | 0 |
| v13, discount 0 | 11,239,227 | 5,750,053 | 1 |
| P (memory) | 12,304,600 | 6,227,021 | 0 |
| P+ (memory, two-week return) | 12,592,665 | 6,449,573 | 0 |
| sham | 9,791,413 | 5,123,266 | 1 |

