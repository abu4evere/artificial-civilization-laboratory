# HB1 — A shared home base: results

Frozen as `HB1-frozen`. Arms on F1's 64 seeds, 120 years: C control (F1's replays), H shared home base, S sham (one extra random draw in week one).

## Validity

- Zero checks: **yes**
- Feasibility pilot: HB1 feasibility pilot, seeds 1201-1204, 20 years: couples apart in 0.0% of 13,899 couple-weeks (must be at most 24%): PASS: **yes**
- Code unchanged: **yes**

**Valid.**

## Baseline (rule 14)

Control on these seeds: 22 of 64 died out.

## Manipulation check

- Couples apart, per partnered non-pregnant woman-week: C 0.578, H 0.001 (must be at most half of C's), S 0.569: **yes**

## Extinction (the frozen outcome)

| | C control | H home base | S sham |
|---|---|---|---|
| worlds died out (of 64) | 22 | **33** | 24 |
| paired against C: saved / lost | – | 7 / 18 | 8 / 10 |
| exact two-sided sign test | – | **p = 0.043** | p = 0.815 |
| median population, year 40 | 26 | 20 | 24 |
| median population, year 80 | 23 | 10 | 23 |
| median population, year 119 | 28 | 0 | 22 |
| births_per_woman_year | 0.133 | 0.120 | 0.134 |
| block_no_partner | 0.550 | 0.683 | 0.546 |
| child_deaths_per_birth | 0.196 | 0.206 | 0.195 |
| starving_share | 0.036 | 0.049 | 0.037 |
| cause_illness | 0.357 | 0.324 | 0.349 |
| cause_starvation | 0.332 | 0.358 | 0.335 |
| deaths_per_person_year | 0.030 | 0.033 | 0.030 |

H saved [513, 604, 611, 811, 813, 817, 1118]; H lost [502, 503, 505, 510, 514, 602, 615, 812, 814, 1102, 1104, 1105, 1111, 1115, 1117, 1121, 1123, 1124].

Frozen rule (paired sign test, p < 0.05): **HB1 increases extinction** (to be examined read-only: crowding, food near home).
