# SA1-F — The sensitive and near-the-line settings on 256 new seeds: results

Frozen as `SA1F-frozen`. Control code (sham in `code_p2`); seeds 4301–4556 (256); 120 years.

## Validity

- Zero check (observers leave the world unchanged; code_p2 with every setting off = the control code): **yes**
- All 9 × 256 worlds present: **yes**
- Code unchanged in every world (one fingerprint per code copy): **yes**

**Valid.**

## Baseline (rule 14)

C died out in 82 of 256 worlds (32.0%). Yardstick (half of F2's effect on F1's seeds): **0.117**.

## The four sensitive settings (the frozen reading)

| setting | value | died out (C: 82) | saved / lost | p | Holm p | effect (C − arm) | 95% interval | reading | SA1 (64 worlds) | against SA1 |
|---|---|---|---|---|---|---|---|---|---|---|
| `perception` | 2 | 168 | 11 / 97 | 2.39e-18 | 1.67e-17 | -0.336 | [-0.402, -0.270] | **sensitive** | -0.422 [-0.562, -0.281] | **differs** |
| `perception` | 8 | 31 | 68 / 17 | 2.18e-08 | 1.31e-07 | +0.199 | [+0.133, +0.266] | **sensitive** | +0.219 [+0.078, +0.344] | agrees |
| `reach` | 6 | 103 | 26 / 47 | 0.0186 | 0.0186 | -0.082 | [-0.148, -0.016] | moves survival | -0.219 [-0.344, -0.094] | **differs** |
| `mortality_base` | 3.0e-5 | 115 | 17 / 50 | 6.74e-05 | 0.000202 | -0.129 | [-0.188, -0.066] | **sensitive** | -0.188 [-0.297, -0.094] | agrees |

## The three near the line (the frozen reading)

| setting | value | died out (C: 82) | saved / lost | p | Holm p | effect (C − arm) | 95% interval | reading | SA1 (64 worlds) | against SA1 |
|---|---|---|---|---|---|---|---|---|---|---|
| `forage_base` | 6 | 120 | 18 / 56 | 1.11e-05 | 5.55e-05 | -0.148 | [-0.211, -0.086] | **sensitive** | -0.188 [-0.328, -0.062] | agrees |
| `conception_chance` | 0.02 | 113 | 27 / 58 | 0.00102 | 0.00203 | -0.121 | [-0.191, -0.051] | **sensitive** | -0.141 [-0.281, +0.000] | agrees |
| `reach` | 2 | 120 | 22 / 60 | 3.23e-05 | 0.000129 | -0.148 | [-0.215, -0.082] | **sensitive** | -0.141 [-0.281, +0.000] | agrees |

Sham against C: died out 90 vs 82; 28 / 36; p = 0.382; effect -0.031 [-0.094, +0.027] (quiet).

## Beside them (population first, rule 18)

| arm | median population, year 119 | births per woman-year | decisions blocked for want of a partner | tools' share of foraged food (E8.2, upper bound) |
|---|---|---|---|---|
| c | 26 | 0.132 | 0.553 | 0.026 |
| perception_lo | 0 | 0.134 | 0.563 | 0.032 (Wilcoxon p 8.36e-13) |
| perception_hi | 41 | 0.131 | 0.548 | 0.024 (Wilcoxon p 1.9e-06) |
| reach_hi | 18 | 0.133 | 0.502 | 0.026 (Wilcoxon p 0.266) |
| mortality_hi | 4 | 0.133 | 0.567 | 0.031 (Wilcoxon p 1.11e-08) |
| forage_lo | 1 | 0.138 | 0.539 | 0.033 (Wilcoxon p 1.58e-13) |
| conception_lo | 2 | 0.104 | 0.555 | 0.033 (Wilcoxon p 6.14e-08) |
| reach_lo | 2 | 0.125 | 0.612 | 0.032 (Wilcoxon p 7.52e-05) |
| s | 22 | 0.131 | 0.557 | 0.027 (Wilcoxon p 0.109) |
