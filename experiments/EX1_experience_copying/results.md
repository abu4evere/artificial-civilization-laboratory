# EX1 — Experience telling instead of habit copying. Results

Frozen as `EX1-frozen` (operational note 1). run_ex1.py, analyse_ex1.py (written before data).

## Validity

- Zero checks: **yes**
- All worlds present (96 of 96): **yes**
- One fingerprint (`code_ex1`): **yes**
- TD replay exact in every arm (mismatches 0): **yes**

**Valid.**

Paired seeds: 32. Extinct by year 200: v 0, e 1, x 0.

## Calibration, years 100-200 (adults; bias = mean q − mean realised G)

| measure | v (v8) | e (experience) | x (sham) | improvement v − e [95%] | sham: v − x [95%] |
|---|---|---|---|---|---|
| common actions' bias | +0.4311 | +0.4375 | +0.4228 | -0.0064 [-0.0184, +0.0049] | +0.0082 [-0.0009, +0.0176] |
| make bias | -0.5598 | -0.5552 | -0.5782 | -0.0046 [-0.0250, +0.0166] | +0.0185 [+0.0021, +0.0351] |
| forage bias | +0.4561 | +0.4632 | +0.4470 | -0.0071 [-0.0222, +0.0068] | +0.0091 [-0.0026, +0.0213] |
| give bias | +0.4889 | +0.4861 | +0.4844 | +0.0028 [-0.0074, +0.0125] | +0.0045 [-0.0058, +0.0149] |
| talk bias | +0.3755 | +0.3811 | +0.3720 | -0.0056 [-0.0149, +0.0028] | +0.0036 [-0.0069, +0.0139] |
| gather bias | +0.3822 | +0.3923 | +0.3642 | -0.0100 [-0.0338, +0.0130] | +0.0181 [-0.0006, +0.0376] |
| mean realised G, all actions | +0.6760 | +0.6764 | +0.6883 | -0.0004 [-0.0228, +0.0212] | -0.0124 [-0.0296, +0.0043] |

## The frozen decision rule

- **P (calibration):** improvement in the common actions' bias, v − e = -0.0064 [-0.0184, +0.0049]; at least 0.10 with the lower bound above 0: **does not support**
- **H (realised return):** e − v = +0.0004 [-0.0212, +0.0228]; lower bound above −0.05: **no harm**
- **F (flags):** extinct e 1 vs v 0 (no flag); mean population years 100-200 e 122.7 vs v 123.7 (ratio 0.992; no flag); sham 118.9
- **D:** e's common bias +0.438 outside ±0.10 (reported, not a gate)

**The change is not supported by the frozen rule.** Adoption is left to the creator.

## Described: making and things held (years 100-200, per adult-year)

| measure | v (v8) | e − v [95%] | sham − v [95%] |
|---|---|---|---|
| making events | 0.0472 | -0.0003 [-0.0033, +0.0029] | +0.0012 [-0.0024, +0.0048] |
| made things held | 0.9435 | -0.0587 [-0.2361, +0.1124] | +0.0139 [-0.2060, +0.2199] |

Told experiences in arm e (all years): 2,481,506; about a situation the listener had already learned in: 0.926.

