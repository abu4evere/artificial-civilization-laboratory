# AG1 — Ageing anchored to forager evidence: results

Frozen as `AG1-frozen`. run_ag1.py, analyse_ag1.py (written before data).

## Validity

- Zero checks: **yes**
- All worlds present (80 of 80): **yes**
- One fingerprint (`code_v9`): **yes**
- Observer deaths equal the world's dead in every world: **yes**

**Valid.**

Paired seeds: 20; mortality_base: v 1.5000e-05, b 4.3373e-06, a 2.8269e-06, x 1.5000e-05.

## Primary — calibration distance

All-cause death rates per person-year, years 100–999, pooled over worlds; reference h(x) = 0.013 + 1.47e-4 exp(0.086 x) at the band midpoints; D = mean |ln(rate / reference)| over the three bands.

| arm | 30–45: deaths / person-years = rate (ref 0.01670) | 45–60: deaths / person-years = rate (ref 0.02643) | 60–70: deaths / person-years = rate (ref 0.05236) | D |
|---|---|---|---|---|
| v | 14006 / 469,840 = 0.0298 | 17294 / 227,052 = 0.0762 | 6001 / 29,779 = 0.2015 | 0.9952 |
| b | 8034 / 483,258 = 0.0166 | 10063 / 354,310 = 0.0284 | 9530 / 135,178 = 0.0705 | 0.1246 |
| a | 5093 / 379,835 = 0.0134 | 6281 / 300,762 = 0.0209 | 6702 / 136,186 = 0.0492 | 0.1723 |
| x | 13226 / 435,753 = 0.0304 | 15941 / 209,638 = 0.0760 | 5527 / 27,117 = 0.2038 | 1.0045 |

Paired world bootstrap, 10,000 replicates (dropped for an empty band: 0).

| arm | D(arm) − D(v) [95%] |
|---|---|
| b | -0.8707 [-0.8799, -0.8234] |
| a | -0.8229 [-0.9057, -0.7456] |
| x | +0.0092 [-0.0171, +0.0356] |

## The frozen rule

- **b:** upper bound -0.8234 below 0 and below the sham's lower bound -0.0171: **more realistic**. Flags: extinct 1 vs v 2 (no flag); living person-years, years 800–999, b ÷ v = 1.034 (no flag).
- **a:** upper bound -0.7456 below 0 and below the sham's lower bound -0.0171: **more realistic**. Flags: extinct 5 vs v 2 (FLAG); living person-years, years 800–999, a ÷ v = 0.774 (FLAG).
- Both are more realistic and their intervals overlap: **both calibrate; the choice is the creator's.**

Exploratory (20 seeds): adoption needs a confirmatory run and the creator's decision.

## Described (not part of the rule)

| arm | adult (16+) deaths | mean adult age at death | adult deaths at 60+ | at 70+ | living aged 60+ (share, years 800–999) | extinct |
|---|---|---|---|---|---|---|
| v | 45320 | 45.1 | 0.147 | 0.014 | 0.013 | 2 of 20 |
| b | 41205 | 54.3 | 0.443 | 0.212 | 0.078 | 1 of 20 |
| a | 31192 | 58.5 | 0.541 | 0.326 | 0.108 | 5 of 20 |
| x | 42470 | 44.8 | 0.143 | 0.013 | 0.013 | 3 of 20 |

| measure (years 800–999) | v | b − v [95%] | a − v [95%] | x − v [95%] |
|---|---|---|---|---|
| world-born adults' (20–40) crafting skill | 0.0871 | -0.0043 [-0.0178, +0.0082] | -0.0104 [-0.0205, -0.0004] | +0.0103 [-0.0110, +0.0374] |
| making events per adult-year | 0.0322 | -0.0040 [-0.0117, +0.0040] | -0.0071 [-0.0120, -0.0020] | +0.0107 [-0.0028, +0.0304] |
| made things held per adult | 0.4313 | +0.0198 [-0.0769, +0.0981] | -0.0006 [-0.1143, +0.1504] | +0.0278 [-0.0816, +0.1779] |

(LC1's skill margin ±0.012, for scale only.)

| arm | mean living per century (worlds alive or 0): 0 / 100 / 200 / 300 / 400 / 500 / 600 / 700 / 800 / 900 |
|---|---|
| v | 119.8 / 141.2 / 113.6 / 95.2 / 93.9 / 103.6 / 112.0 / 120.5 / 124.4 / 130.9 |
| b | 140.1 / 162.8 / 129.2 / 106.0 / 105.0 / 112.7 / 117.3 / 123.3 / 126.7 / 137.1 |
| a | 138.3 / 156.6 / 115.7 / 92.3 / 80.7 / 80.7 / 85.7 / 89.2 / 97.1 / 100.4 |
| x | 111.4 / 124.2 / 97.5 / 86.3 / 89.4 / 96.7 / 106.1 / 116.5 / 121.0 / 129.7 |

| arm | adult causes of death (shares) | child (under 16) deaths from starvation or thirst per child-year |
|---|---|---|
| v | illness 0.43, old age 0.38, starvation 0.12, thirst 0.06, childbirth 0.01, killed 0.00 | 0.0053 |
| b | old age 0.54, illness 0.19, starvation 0.17, thirst 0.09, childbirth 0.01, killed 0.00 | 0.0060 |
| a | old age 0.57, starvation 0.18, illness 0.17, thirst 0.07, childbirth 0.01, killed 0.00 | 0.0057 |
| x | illness 0.43, old age 0.37, starvation 0.13, thirst 0.06, childbirth 0.01, killed 0.00 | 0.0058 |
