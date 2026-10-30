# LC1 — Does curiosity slow the erosion over 1,000 years? Results

Frozen as `LC1-frozen`. run_lc1.py (CU1's runner), analyse_lc1.py (written before data).

## Validity

- Zero checks: **yes**
- All worlds present (96 of 96): **yes**
- One fingerprint (`code_cu1`): **yes**
- `tried` equals own updates (mismatches 0): **yes**

**Valid.**

Paired seeds: 32; 1,000 years. Extinct by year 1,000: v 12, c 7, x 12.

## Primary — world-born adults' (20–40) crafting skill, years 800–999

Margin ±0.012 (FS1). Survivor-weighted: only living adults in worlds still alive count.

| arm | skill | worlds / adult-years | − v [95%] |
|---|---|---|---|
| v (v8) | 0.0512 | 20 / 161,745 | |
| c (curiosity) | 0.0839 | 26 / 235,460 | **+0.0327 [+0.0232, +0.0434]** |
| x (sham) | 0.0474 | 20 / 171,672 | -0.0038 [-0.0109, +0.0028] |

**Reading: curiosity holds skill higher.**

## Slower erosion or a parallel shift?

| arm | skill years 100–199 | skill years 800–999 | change |
|---|---|---|---|
| v | 0.2348 | 0.0512 | -0.1835 |
| c | 0.2692 | 0.0839 | -0.1853 |
| x | 0.2286 | 0.0474 | -0.1812 |

Change in c minus change in v: -0.0018 [-0.0176, +0.0141] (positive = c falls less).

Century-by-century (world-born adults' crafting skill; mean living; making per adult-year):

| years | v | c | x |
|---|---|---|---|
| 0–100 | 0.4386 / 120.2 / 0.2168 | 0.4810 / 108.1 / 0.3134 | 0.4238 / 124.3 / 0.2047 |
| 100–200 | 0.2348 / 116.2 / 0.0467 | 0.2692 / 114.6 / 0.0755 | 0.2286 / 117.9 / 0.0436 |
| 200–300 | 0.1489 / 81.0 / 0.0282 | 0.1806 / 96.3 / 0.0478 | 0.1483 / 82.4 / 0.0252 |
| 300–400 | 0.1100 / 62.8 / 0.0205 | 0.1399 / 82.6 / 0.0403 | 0.1075 / 64.2 / 0.0200 |
| 400–500 | 0.0826 / 53.7 / 0.0191 | 0.1153 / 81.0 / 0.0342 | 0.0861 / 58.0 / 0.0170 |
| 500–600 | 0.0712 / 50.5 / 0.0181 | 0.1043 / 83.0 / 0.0308 | 0.0708 / 57.2 / 0.0164 |
| 600–700 | 0.0625 / 55.7 / 0.0148 | 0.0947 / 85.2 / 0.0310 | 0.0608 / 58.9 / 0.0142 |
| 700–800 | 0.0571 / 63.6 / 0.0145 | 0.0903 / 89.4 / 0.0303 | 0.0533 / 61.6 / 0.0131 |
| 800–900 | 0.0532 / 66.5 / 0.0145 | 0.0846 / 95.1 / 0.0300 | 0.0491 / 69.5 / 0.0117 |
| 900–1000 | 0.0493 / 69.7 / 0.0140 | 0.0832 / 104.1 / 0.0284 | 0.0458 / 75.0 / 0.0107 |

Log-skill slope per century (least squares over the centuries with data; described):

- v: -0.2224 per century
- c: -0.1735 per century
- x: -0.2291 per century

## Flags (CU1's)

- Extinct c 7 vs v 12: no flag.
- Population years 800–999 c ÷ v = 1.462: no flag.

## Secondaries (years 800–999, per adult-year)

| measure | v | c − v [95%] |
|---|---|---|
| making events | 0.0142 | +0.0150 [+0.0109, +0.0191] |
| made things held | 0.2237 | +0.1499 [+0.0435, +0.2520] |
