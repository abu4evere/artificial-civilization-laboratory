# FS1 — Is the erosion the founders' head start wearing off? Results

Frozen as `FS1-frozen`. run_fs1.py, analyse_fs1.py (written before data).

## Validity

- Zero checks: **yes**
- All worlds present (128 of 128): **yes**
- One fingerprint (`code_fs1`): **yes**

**Valid.**

Paired seeds: 32; 500 years.

| arm | extinct by year 100 | extinct by year 500 | mean living, years 0–100 | mean living, years 300–500 |
|---|---|---|---|---|
| t (today) | 0 | 5 | 124.4 | 79.7 |
| z (zero start) | 1 | 6 | 127.7 | 85.2 |
| c (no crafting start) | 0 | 7 | 129.0 | 87.6 |
| x (sham) | 0 | 6 | 128.4 | 82.5 |

**Collapse flag (z has ≥ 4 more worlds extinct by year 100 than t): not raised** (1 vs 0).

## Primary — world-born adults' (20–40) crafting skill, years 300–500

Margin ±0.012 (one making act's skill gain from zero). Survivor-weighted: only living adults count.

| arm | mean skill | contributing worlds | adult-years | − today [95%] | ÷ today [95%] | reading |
|---|---|---|---|---|---|---|
| t (today) | 0.0946 | 31 | 192,395 | | | |
| z (zero start) | 0.0959 | 30 | 205,474 | +0.0013 [-0.0082, +0.0116] | 1.013 [0.917, 1.130] | **converges** |
| c (no crafting start) | 0.0998 | 30 | 213,265 | +0.0052 [-0.0025, +0.0131] | 1.055 [0.975, 1.148] | **not shown** |
| x (sham) | 0.0992 | 29 | 199,607 | +0.0046 [-0.0026, +0.0128] | 1.049 [0.974, 1.142] | **(yardstick)** |

## Key secondaries (years 300–500; per adult-year)

| arm | making events | − today [95%] | made things held | − today [95%] |
|---|---|---|---|---|
| t | 0.0208 | | 0.447 | |
| z | 0.0204 | -0.0004 [-0.0030, +0.0023] | 0.462 | +0.015 [-0.104, +0.150] |
| c | 0.0224 | +0.0016 [-0.0007, +0.0041] | 0.509 | +0.063 [-0.010, +0.145] |
| x | 0.0225 | +0.0016 [-0.0010, +0.0048] | 0.539 | +0.092 [-0.014, +0.219] |

## The start (years 0–100), described

| arm | world-born adults' crafting skill | all adults' crafting skill | making per adult-year | things held per adult |
|---|---|---|---|---|
| t | 0.4358 | 0.4418 | 0.2143 | 1.139 |
| z | 0.4299 | 0.3925 | 0.2151 | 1.127 |
| c | 0.4233 | 0.3869 | 0.2061 | 1.161 |
| x | 0.4347 | 0.4416 | 0.2158 | 1.169 |

## Skill by age (world-born, years 300–500; mean crafting skill, people counted)

| arm | age 10 | age 20 | age 30 | age 40 |
|---|---|---|---|---|
| t | 0.0729 (11,388) | 0.0845 (10,748) | 0.0954 (9,321) | 0.1065 (7,047) |
| z | 0.0743 (12,093) | 0.0862 (11,482) | 0.0967 (9,917) | 0.1067 (7,530) |
| c | 0.0779 (12,290) | 0.0903 (11,808) | 0.1004 (10,315) | 0.1109 (7,866) |
| x | 0.0785 (11,580) | 0.0902 (11,059) | 0.0998 (9,642) | 0.1099 (7,452) |

## By century (all arms; world-born adults' crafting skill / mean living)

| years | t | z | c | x |
|---|---|---|---|---|
| 0–100 | 0.4358 / 124.4 | 0.4299 / 127.7 | 0.4233 / 129.0 | 0.4347 / 128.4 |
| 100–200 | 0.2265 / 129.3 | 0.2219 / 137.9 | 0.2241 / 142.6 | 0.2269 / 136.0 |
| 200–300 | 0.1477 / 96.9 | 0.1414 / 110.3 | 0.1481 / 114.0 | 0.1474 / 103.7 |
| 300–400 | 0.1063 / 81.5 | 0.1060 / 88.9 | 0.1105 / 90.6 | 0.1106 / 86.2 |
| 400–500 | 0.0823 / 77.9 | 0.0846 / 81.5 | 0.0881 / 84.6 | 0.0867 / 78.9 |
