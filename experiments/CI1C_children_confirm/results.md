# CI1-C: children may make again (LG), confirmatory run on new seeds (results)

CI1's frozen analysis on seeds 24101-24132, arms v14 / LG / sham (frozen as `CI1C-frozen`); the CI1-C rule and measures follow it (analyse_ci1c.py, written before data).

Frozen as `CI1-frozen` (amendment 1 before code). run_ci1.py, analyse_ci1.py (written before data).

## Validity

- Zero checks (All: PASS, same `code_ci1` fingerprint): **yes**
- All worlds present (96): **yes**
- One fingerprint, `code_ci1`'s: **yes**

**Valid.**

## Readings (frozen; each arm alone against v14)

- **LG: supported.** Guards raised: none. Complete-set share 0.0262 against v14's 0.0041: +0.0221 [+0.0166, +0.0283].
- Sham: complete-set share +0.0003 [-0.0029, +0.0035] against v14; guards raised: none.

Rule: "supported" if no guard is raised and the complete-set interval (arm − v14) lies wholly above 0; "no harm, no effect" if no guard is raised and it does not; "harm" if any guard is raised. A supported arm goes to a confirmatory run on new seeds before any adoption.

## Co-primary: the share of world-new kinds whose inventor held the complete input set within 5 years

| arm | kinds | complete | share | arm − v14 [95%] |
|---|---|---|---|---|
| v14 | 3,873 | 16 | 0.0041 |  |
| LG | 4,077 | 107 | 0.0262 | +0.0221 [+0.0166, +0.0283] |
| sham | 3,583 | 16 | 0.0045 | +0.0003 [-0.0029, +0.0035] |

## Primary: harm guards, per arm against v14

### LG

| guard | arm | v14 | ratio or difference [95%] |
|---|---|---|---|
| starvation deaths per 1,000 living-years (ratio) | 4.3124 | 4.3377 | 0.9942 [0.8759, 1.1290] |
| killing deaths per 1,000 living-years (difference) | 0.0000 | 0.0021 | -0.0021 [-0.0068, +0.0000] |
| adult health, mean (difference) | 93.4650 | 93.5425 | -0.0774 [-0.6739, +0.5498] |
| living-weeks (ratio) | 24,140,484.0000 | 24,803,159.0000 | 0.9733 [0.8581, 1.0911] |
| extinct worlds (extra) | 0.0000 | 2.0000 | -2.0000 [+nan, +nan] |
| child deaths per 1,000 child-years (ratio) | 7.6837 | 8.2982 | 0.9259 [0.8097, 1.0697] |
| child starvation deaths per 1,000 child-years (ratio) | 4.8301 | 5.1126 | 0.9447 [0.8054, 1.1058] |
| food gifts to kin's children per 1,000 adult-weeks (ratio) | 5.0389 | 4.9301 | 1.0221 [0.9339, 1.1305] |

## Described (not decisive)

| arm | remade within 5 years | made again once complete | child inventors: kinds, complete, remade | grown inventors: kinds, complete, remade |
|---|---|---|---|---|
| v14 | 2 of 3,873 | 2 of 16 | 3,552, 12, 0 | 321, 4, 2 |
| LG | 32 of 4,077 | 32 of 107 | 3,688, 104, 31 | 389, 3, 1 |
| sham | 0 of 3,583 | 0 of 16 | 3,255, 13, 0 | 328, 3, 0 |

| arm | aims formed | ended: complete / value / forgotten / held / interrupted | puts, hands, makes, play trials kept off | child makes per 1,000 child-weeks | makes per adult-year | care per 1,000 adult-weeks | food per adult (year ends) | adult-weeks at the material limit | child health | world-new kinds |
|---|---|---|---|---|---|---|---|---|---|---|
| v14 | 0 | 0 / 0 / 0 / 0 / 0 | 0, 0, 0, 0 | 0.000 | 0.0767 | 2.00 | 6.0 | 0.3294 | 91.6 | 3,873 |
| LG | 0 | 0 / 0 / 0 / 0 / 0 | 0, 0, 0, 0 | 4.464 | 0.0886 | 2.10 | 6.0 | 0.3304 | 91.6 | 4,077 |
| sham | 0 | 0 / 0 / 0 / 0 / 0 | 0, 0, 0, 0 | 0.000 | 0.0742 | 2.03 | 5.8 | 0.3304 | 91.3 | 3,583 |

## The CI1-C rule (frozen)

| condition | value | holds |
|---|---|---|
| 1. no CI1 guard raised for LG against v14 | guards raised: none | yes |
| 2. LG − v14, co-primary, lower bound above 0 | +0.0221 [+0.0166, +0.0283] (CI1's analysis: supported) | yes |
| 3. LG − sham, co-primary, lower bound above 0 | +0.0218 [+0.0169, +0.0278] (LG 107 of 4,077; sham 16 of 3,583) | yes |

**CONFIRMED.** Confirmed only if all three hold; then the blind recompute and the safe path to v15. Otherwise LG is not adopted.

## Pre-registered secondary (not a gate): kinds remade by their inventor within 5 years

| arm | kinds | remade | share |
|---|---|---|---|
| v14 | 3,873 | 2 | 0.0005 |
| LG | 4,077 | 32 | 0.0078 |
| sham | 3,583 | 0 | 0.0000 |

LG − v14: +0.0073 [+0.0044, +0.0107].

## Described (not decisive)

| arm | kinds made by another person within 5 years | share | child makes per 1,000 child-weeks | child starvation deaths per 1,000 child-years | child deaths per 1,000 child-years |
|---|---|---|---|---|---|
| v14 | 0 of 3,873 | 0.0000 | 0.000 | 5.1126 | 8.2982 |
| LG | 0 of 4,077 | 0.0000 | 4.464 | 4.8301 | 7.6837 |
| sham | 0 of 3,583 | 0.0000 | 0.000 | 5.4257 | 8.6356 |

