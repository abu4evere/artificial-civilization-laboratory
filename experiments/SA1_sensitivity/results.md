# SA1 — Sensitivity audit: results

Frozen as `SA1-frozen`. Control code; F1's 64 seeds; 120 years; one setting changed per arm.

## Validity

- Zero check (observers leave the world unchanged): **yes**
- Control re-run reproduces F1's saved populations on every seed: **yes**
- Code unchanged in every world (one fingerprint per code copy): **yes**

**Valid.**

## Baseline (rule 14)

C (control re-run) died out in 22 of 64 worlds (34.4%). Half of F2's effect: **0.117**.

## Extinction, each setting against the control (the frozen reading)

| setting | value | died out (C: 22) | saved / lost | p | Holm p | effect (C − arm) | 95% interval | reading |
|---|---|---|---|---|---|---|---|---|
| `conception_chance` | 0.02 | 31 | 6 / 15 | 0.0784 | 0.548 | -0.141 | [-0.281, +0.000] | no sign at this sample |
| `conception_chance` | 0.08 | 20 | 9 / 7 | 0.804 | 1 | +0.031 | [-0.094, +0.156] | no sign at this sample |
| `perception` | 2 | 49 | 2 / 29 | 4.63e-07 | 5.55e-06 | -0.422 | [-0.562, -0.281] | **sensitive** |
| `perception` | 8 | 8 | 18 / 4 | 0.00434 | 0.0391 | +0.219 | [+0.078, +0.344] | **sensitive** |
| `reach` | 2 | 31 | 6 / 15 | 0.0784 | 0.548 | -0.141 | [-0.281, +0.000] | no sign at this sample |
| `reach` | 6 | 36 | 3 / 17 | 0.00258 | 0.0258 | -0.219 | [-0.344, -0.094] | **sensitive** |
| `camp_radius` | 1 | 21 | 10 / 9 | 1 | 1 | +0.016 | [-0.109, +0.141] | no sign at this sample |
| `camp_radius` | 4 | 27 | 9 / 14 | 0.405 | 1 | -0.078 | [-0.219, +0.062] | no sign at this sample |
| `mortality_base` | 0.75e-5 | 21 | 7 / 6 | 1 | 1 | +0.016 | [-0.094, +0.125] | no sign at this sample |
| `mortality_base` | 3.0e-5 | 34 | 1 / 13 | 0.00183 | 0.0201 | -0.188 | [-0.297, -0.094] | **sensitive** |
| `forage_base` | 6 | 34 | 5 / 17 | 0.0169 | 0.135 | -0.188 | [-0.328, -0.062] | **sensitive** (does not survive Holm) |
| `forage_base` | 24 | 21 | 10 / 9 | 1 | 1 | +0.016 | [-0.109, +0.156] | no sign at this sample |

Sham against C: died out 24 vs 22; 8 / 10; p = 0.815; effect -0.031 [-0.156, +0.094].

## Beside them (population first, rule 18)

| arm | median population, year 119 | births per woman-year | decisions blocked for want of a partner | tools' share of foraged food (E8.2, upper bound) |
|---|---|---|---|---|
| c | 28 | 0.133 | 0.550 | 0.026 |
| conception_lo | 2 | 0.102 | 0.560 | 0.033 (Wilcoxon p 0.00355) |
| conception_hi | 30 | 0.155 | 0.562 | 0.024 (Wilcoxon p 0.508) |
| perception_lo | 0 | 0.128 | 0.590 | 0.035 (Wilcoxon p 7.96e-05) |
| perception_hi | 32 | 0.121 | 0.577 | 0.024 (Wilcoxon p 0.0238) |
| reach_lo | 2 | 0.112 | 0.655 | 0.033 (Wilcoxon p 0.0146) |
| reach_hi | 0 | 0.124 | 0.548 | 0.030 (Wilcoxon p 0.00875) |
| camp_lo | 14 | 0.109 | 0.551 | 0.029 (Wilcoxon p 0.611) |
| camp_hi | 14 | 0.151 | 0.565 | 0.025 (Wilcoxon p 0.784) |
| mortality_lo | 21 | 0.131 | 0.550 | 0.025 (Wilcoxon p 0.273) |
| mortality_hi | 0 | 0.135 | 0.563 | 0.032 (Wilcoxon p 0.00136) |
| forage_lo | 0 | 0.133 | 0.559 | 0.035 (Wilcoxon p 0.000374) |
| forage_hi | 29 | 0.132 | 0.561 | 0.024 (Wilcoxon p 0.508) |
| s | 22 | 0.134 | 0.546 | 0.026 (Wilcoxon p 0.552) |
