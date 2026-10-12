# S1 feasibility check: results

Plan: `feasibility_plan.md` (tag `S1-feasibility-plan`). Seeds 9001–9004, 10 years, control code. Population, births, deaths and extinction were not recorded.

| measure | C | L | LP |
|---|---|---|---|
| ran_without_error | 4 of 4 | 4 of 4 | 4 of 4 |
| land_share | 0.4 | 0.4 (0.399–0.4) | 0.4 (0.399–0.4) |
| mean_land_fertility | 0.3705 (0.355–0.375) | 0.3885 (0.378–0.4) | 0.3885 (0.378–0.4) |
| islands | 5.0 (3–5) | 6.0 (4–7) | 6.0 (4–7) |
| animal_groups_per_100_land | 4.14 (4.06–4.22) | 4.38 (4.38–4.42) | 4.38 (4.38–4.42) |
| founders | 20.0 | 20.0 | 80.0 |
| founder_food | 21.0 | 21.0 | 21.0 |
| land_per_founder | 32.0 | 127.9 (127.8–128.0) | 32.0 (31.9–32.0) |
| bands | 4.0 | 4.0 | 4.0 |
| band_sizes | [5, 5, 5, 5]; [5, 5, 5, 5] | [5, 5, 5, 5]; [5, 5, 5, 5] | [20, 20, 20, 20]; [20, 20, 20, 20] |
| mean_gap_between_band_centres | 15.35 (12.8–16) | 30.3 (26.7–35.3) | 31.05 (28.8–34) |
| eligible_founders_per_founder | 10.0 | 10.0 | 40.0 |
| eligible_in_sight_per_founder | 1.95 (1.4–2.4) | 2.0 (1.6–2.4) | 9.8 (9.55–9.95) |
| init_seconds | 0.055 (0.05–0.06) | 0.32 (0.29–0.4) | 0.38 (0.31–0.39) |
| seconds_per_world_year | 0.96 (0.59–1.09) | 1.48 (1.43–1.75) | 5.625 (5.47–6.07) |

**Runtime estimate** for a main run of 256 seeds × C, L, LP (+ sham at C's cost) × 120 years on four workers: about **19 hours** (seconds per world-year: C 0.96, L 1.48, LP 5.625). Early years only; later years may differ as populations change.
