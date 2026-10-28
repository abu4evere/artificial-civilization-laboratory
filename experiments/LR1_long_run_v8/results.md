# LR1 — Does nature v8 stay healthy over 1,000 years? Results

Frozen as `LR1-frozen` (operational note 1). run_lr1.py, analyse_lr1.py (written before data).

## Validity

- Zero checks: **yes**
- All worlds present (96 of 96): **yes**
- One fingerprint (`code_v8`): **yes**
- Drops = pick-ups + on the ground every year (mismatches 0): **yes**

**Valid.**

Paired seeds: 32; 1000 years. Extinct: v7 8, v8 8, sham 10.

## Q1 — Accumulation: things lying on the ground (mean per world)

| year | v8 | sham | v8: most on one tile (max over worlds) | v8: pick-ups ÷ drops in the century before |
|---|---|---|---|---|
| 200 | 122.3 | 108.2 | 29 | 1.008 |
| 400 | 110.3 | 104.5 | 29 | 1.005 |
| 600 | 82.4 | 84.3 | 18 | 1.052 |
| 800 | 75.8 | 75.0 | 18 | 0.787 |
| 1000 | 77.6 | 75.2 | 18 | 0.993 |

Slope of things on the ground, years 800-1,000 (mean over worlds): +0.003 per year [-0.001, +0.008]. Year 1,000 ÷ year 200: 0.63.

**Flag A (accumulation): not raised** (> 5× year 200 and still growing).

## Q2 — Demography (mean living per world; extinct worlds count 0)

| years | v7 | v8 | sham | v8 ÷ v7 | sham ÷ v7 |
|---|---|---|---|---|---|
| 0-100 | 118.2 | 116.5 | 119.1 | 0.986 | 1.008 |
| 100-200 | 117.9 | 115.0 | 112.5 | 0.975 | 0.955 |
| 200-300 | 82.5 | 82.1 | 78.4 | 0.995 | 0.949 |
| 300-400 | 66.6 | 63.6 | 60.2 | 0.955 | 0.905 |
| 400-500 | 59.5 | 55.3 | 55.3 | 0.928 | 0.929 |
| 500-600 | 55.7 | 52.6 | 55.3 | 0.943 | 0.993 |
| 600-700 | 56.5 | 52.9 | 56.0 | 0.936 | 0.990 |
| 700-800 | 58.4 | 58.0 | 60.0 | 0.994 | 1.028 |
| 800-900 | 62.0 | 61.3 | 63.5 | 0.990 | 1.024 |
| 900-1000 | 65.7 | 64.9 | 66.2 | 0.987 | 1.008 |

Population, years 800-1,000: v8 ÷ v7 **0.988 [0.702, 1.406]**; sham ÷ v7 1.016 [0.771, 1.292].

**Flag B (demography): not raised** (below 0.90 with the upper bound under 1, or 3+ more extinct worlds).

## Q3 — Made things held per adult

| years | v7 | v8 | sham |
|---|---|---|---|
| 0-100 | 0.595 | 1.191 | 1.237 |
| 100-200 | 0.613 | 0.945 | 1.064 |
| 200-300 | 0.523 | 0.879 | 0.881 |
| 300-400 | 0.428 | 0.631 | 0.643 |
| 400-500 | 0.324 | 0.635 | 0.494 |
| 500-600 | 0.268 | 0.569 | 0.391 |
| 600-700 | 0.259 | 0.498 | 0.367 |
| 700-800 | 0.248 | 0.393 | 0.338 |
| 800-900 | 0.231 | 0.370 | 0.379 |
| 900-1000 | 0.197 | 0.323 | 0.371 |

v8: pick-ups by someone other than the dropper: 0.959 of 76639 pick-ups.

