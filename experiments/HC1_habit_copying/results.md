# HC1 — Habit copying in talk. Results

Frozen as `HC1-frozen` (operational note 1). run_hc1.py, analyse_hc1.py (written before data).

## Validity

- Zero checks: **yes**
- All worlds present (96 of 96): **yes**
- One fingerprint (`code_hc1`): **yes**
- TD replay exact in every arm (mismatches 0): **yes**

**Valid.**

Paired seeds: 32. Extinct by year 200: w 0, s 0, x 1.

## Calibration, years 100-200 (adults; bias = mean q − mean realised G)

| measure | w (v7) | s (situation) | x (sham) | improvement w − s [95%] | sham: w − x [95%] |
|---|---|---|---|---|---|
| common actions' bias | +0.4235 | +0.4358 | +0.4251 | -0.0123 [-0.0213, -0.0040] | -0.0017 [-0.0122, +0.0084] |
| make bias | -0.5706 | -0.5651 | -0.5726 | -0.0055 [-0.0180, +0.0071] | +0.0019 [-0.0154, +0.0209] |
| forage bias | +0.4456 | +0.4609 | +0.4493 | -0.0153 [-0.0268, -0.0045] | -0.0037 [-0.0165, +0.0088] |
| give bias | +0.4867 | +0.4920 | +0.4830 | -0.0054 [-0.0129, +0.0028] | +0.0037 [-0.0085, +0.0163] |
| talk bias | +0.3732 | +0.3762 | +0.3668 | -0.0030 [-0.0116, +0.0058] | +0.0064 [-0.0061, +0.0182] |
| gather bias | +0.3724 | +0.3878 | +0.3791 | -0.0155 [-0.0314, +0.0001] | -0.0067 [-0.0204, +0.0073] |
| mean realised G, all actions | +0.6836 | +0.6733 | +0.6795 | +0.0103 [-0.0024, +0.0233] | +0.0041 [-0.0145, +0.0201] |

## The frozen decision rule

- **P (calibration):** improvement in the common actions' bias, w − s = -0.0123 [-0.0213, -0.0040]; at least 0.10 with the lower bound above 0: **does not support**
- **H (realised return):** s − w = -0.0103 [-0.0233, +0.0024]; lower bound above −0.05: **no harm**
- **F (flags):** extinct s 0 vs w 0 (no flag); mean population years 100-200 s 122.0 vs w 130.9 (ratio 0.932; no flag); sham 119.7
- **D:** s's common bias +0.436 outside ±0.10 (reported, not a gate)

**The change is not supported by the frozen rule.** Adoption is left to the creator.

