# PD1 — Why does population fall when made things persist? Results

Frozen as `PD1-frozen` (operational note 1). run_pd1.py, analyse_pd1.py (written before data).

## Validity

- Zero checks: **yes**
- All worlds present (192 of 192): **yes**
- One fingerprint (`code_op1`): **yes**
- Founders + births − deaths = living at the end, in every world (mismatches 0): **yes**

**Valid.**

Paired seeds: 64. Extinct by year 200: c 0, o 1, x 0.

## Q1 — The exact split of the gap in final population (pooled over paired worlds; extinct worlds count 0)

Living at year 200 = founders + births − deaths, so the gap = Δbirths − Σ Δdeaths by cause.

| component | o − c [95%] | share of the o − c gap | x − c (sham yardstick) [95%] |
|---|---|---|---|
| births | -909 [-3244, +1504] | 4.09 | -1998 [-5126, +1025] |
| deaths: hunger | -128 [-835, +588] | 0.58 | +105 [-633, +884] |
| deaths: thirst | +39 [-322, +405] | -0.18 | +263 [-182, +704] |
| deaths: cold | -1 [-3, +0] | 0.00 | -1 [-3, +0] |
| deaths: illness | +568 [-254, +1386] | -2.56 | +870 [-172, +1950] |
| deaths: childbirth | +5 [-67, +76] | -0.02 | +5 [-64, +75] |
| deaths: violence | -8 [-53, +36] | 0.04 | -24 [-79, +30] |
| deaths: animals | -1 [-4, +2] | 0.00 | +2 [-2, +7] |
| deaths: other | +213 [-318, +754] | -0.96 | +450 [-217, +1152] |
| **total: living at year 200** | **-222 [-900, +485]** | 1.00 | -328 [-1041, +345] |

Final living: c 7323, o 7101, x 6995 (summed over 64 worlds).

**The component carrying the largest share of the o − c gap: births (share 4.09).**

## Q2 — Rates (per 1,000 person-years, or woman-years 16-45 for births; years 0-200)

| rate | c | o | x | o − c [95%] | x − c [95%] |
|---|---|---|---|---|---|
| births per 1,000 woman-years (16-45) | 118.52 | 120.10 | 119.99 | +1.58 [-1.28, +4.38] | +1.47 [-1.58, +4.53] |
| all deaths | 26.60 | 26.81 | 26.78 | +0.21 [-0.23, +0.65] | +0.19 [-0.23, +0.58] |
| deaths: hunger | 6.32 | 6.55 | 6.55 | +0.23 [-0.15, +0.61] | +0.23 [-0.14, +0.61] |
| deaths: thirst | 3.10 | 3.16 | 3.08 | +0.05 [-0.16, +0.26] | -0.02 [-0.25, +0.19] |
| deaths: cold | 0.00 | 0.00 | 0.00 | +0.00 [+0.00, +0.00] | +0.00 [+0.00, +0.00] |
| deaths: illness | 10.34 | 10.23 | 10.27 | -0.11 [-0.30, +0.09] | -0.07 [-0.26, +0.12] |
| deaths: childbirth | 0.28 | 0.28 | 0.29 | +0.00 [-0.04, +0.04] | +0.01 [-0.03, +0.05] |
| deaths: violence | 0.09 | 0.10 | 0.11 | +0.01 [-0.02, +0.04] | +0.02 [-0.01, +0.05] |
| deaths: animals | 0.00 | 0.00 | 0.00 | +0.00 [-0.00, +0.00] | -0.00 [-0.00, +0.00] |
| deaths: other | 6.47 | 6.49 | 6.49 | +0.02 [-0.16, +0.21] | +0.02 [-0.13, +0.16] |
| all deaths, childs (per 1,000 child-years) | 12.70 | 12.63 | 12.84 | -0.06 [-0.85, +0.70] | +0.15 [-0.62, +0.93] |
| all deaths, teens (per 1,000 teen-years) | 7.19 | 7.96 | 7.72 | +0.77 [+0.05, +1.52] | +0.53 [-0.33, +1.39] |
| all deaths, adults (per 1,000 adult-years) | 27.04 | 27.40 | 27.16 | +0.36 [-0.30, +1.00] | +0.12 [-0.45, +0.68] |
| all deaths, elders (per 1,000 elder-years) | 119.63 | 120.49 | 121.14 | +0.86 [-1.24, +2.99] | +1.51 [-0.71, +3.79] |

## Q3 — Fighting

| measure | c | o | x | o − c [95%] | x − c [95%] |
|---|---|---|---|---|---|
| attacks per 1,000 adult-years | 2.95 | 2.73 | 3.17 | -0.23 [-0.55, +0.12] | +0.22 [-0.21, +0.64] |
| killings per 1,000 adult-years | 0.11 | 0.12 | 0.14 | +0.01 [-0.02, +0.05] | +0.03 [-0.02, +0.07] |
| share of attacks with a fighting tool in hand (×1,000) | 399.53 | 592.51 | 386.84 | +192.98 [+147.27, +238.36] | -12.69 [-47.36, +22.20] |
| kill rate per attack with a tool (×1,000) | 38.82 | 46.78 | 39.97 | +7.96 [-7.58, +23.34] | +1.15 [-13.88, +15.38] |
| kill rate per attack without a tool (×1,000) | 34.25 | 39.52 | 44.53 | +5.27 [-9.96, +20.74] | +10.28 [-5.26, +25.37] |
| attackers who died (per 1,000 attacks) | 12.81 | 13.48 | 12.83 | +0.67 [-5.49, +6.67] | +0.02 [-5.78, +5.89] |

