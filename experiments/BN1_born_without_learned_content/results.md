# BN1 — Born without learned content: results

Frozen as `BN1-frozen`. run_bn1.py, analyse_bn1.py (written before data).

## Validity

- Zero checks (All: PASS, same `code_bn1` fingerprint): **yes**
- All worlds present (128 arm worlds, 8 reference worlds): **yes**
- One fingerprint, `code_bn1`'s: **yes**
- Every habit update replays exactly, and every newborn follows its arm's law (mismatches 0): **yes**

**Valid.**

## Primary (frozen): early-life calibration (ages 52-103 weeks), standardized over cells

| arm | E (mean abs(q - G)) | early-life updates | coverage |
|---|---|---|---|
| v11 | 0.2734 | 489,996 | 1.000 |
| z (born at 0) | 0.2939 | 476,491 | 1.000 |
| x (scrambled) | 0.2844 | 435,588 | 1.000 |
| sham | 0.2733 | 472,650 | 1.000 |

Common cells: 28 of 41; weights from 8 reference worlds.

| contrast | difference [95%] |
|---|---|
| **D_z = z - v11** | **+0.0205 [+0.0157, +0.0252]** |
| sham - v11 | -0.0001 [-0.0077, +0.0072] |
| x - v11 (content) | +0.0110 [+0.0057, +0.0162] |
| x - z (level) | -0.0095 [-0.0155, -0.0037] |

Rule: inconclusive if coverage < 0.8 in any arm, or if the sham's point difference lies outside +-0.01; else z better if D_z's upper bound < -0.02; z not worse if its upper bound < +0.02; z worse if its lower bound > +0.02; else inconclusive.

**Reading: inconclusive.** No guard raised.

GPT's caution: this measures early-life calibration, not pure learning speed.

## Guards (z against v11)

- Child deaths per 1,000 child-years: z 7.98, v11 8.10; difference [-1.19, +0.89]: **not raised**
- Population z / v11: 0.957 [0.872, 1.048]: **not raised**
- Extinctions: v11 1, z (born at 0) 1, x (scrambled) 1, sham 1: **not raised**

## Secondary (described, not decisive)

| arm | early signed bias mean(q - G) | death-closed early updates | all-age calibration | recipes per adult | making per adult-year | mean living |
|---|---|---|---|---|---|---|
| v11 | -0.2031 | 3,652 | 0.4009 | 10.07 | 0.0650 | 159.2 |
| z (born at 0) | -0.2495 | 3,903 | 0.3895 | 10.15 | 0.0685 | 152.4 |
| x (scrambled) | -0.2333 | 3,198 | 0.3895 | 10.23 | 0.0686 | 143.6 |
| sham | -0.2025 | 3,560 | 0.4010 | 10.02 | 0.0642 | 153.1 |

