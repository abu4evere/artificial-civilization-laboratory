# MB1a — do ACL's bands meet? Results (holdout)

Frozen as `MB1a-frozen` (Stage A; correction of 12 October appended). Read-only replays; run_mb1a.py, analyse_mb1a.py.

## Validity

- Observer leaves the world unchanged (zero check): **yes**
- All worlds present: **yes**
- c: one code fingerprint (`e13r`): **yes**
- c: same code as the saved worlds: **yes**; every replay reproduces its saved decade populations (frozen check): **yes**; final state hash also equal: 32 of 32
- c: people of unknown lineage (left out of every pair): 0
- p: one code fingerprint (`p2`): **yes**
- p: same code as the saved worlds: **yes**; every replay reproduces its saved decade populations (frozen check): **yes**; final state hash also equal: 32 of 32
- p: people of unknown lineage (left out of every pair): 0
- lp: one code fingerprint (`p2`): **yes**
- lp: same code as the saved worlds: **yes**; every replay reproduces its saved decade populations (frozen check): **yes**; final state hash also equal: 32 of 32
- lp: people of unknown lineage (left out of every pair): 0

**Valid.**

## Measures (population beside every measure, rule 18)

| | C (20 founders, 40 × 40) | P (80 founders, 40 × 40) | LP (80 founders, 80 × 80) |
|---|---|---|---|
| worlds (survived 120 years) | 32 (18) | 32 (31) | 32 (32) |
| median population, years 10 / 60 / 120 | 24 / 19 / 18 | 62 / 50 / 48 | 98 / 140 / 157 |
| median lineages alive, years 10 / 60 / 120 | 4 / 2 / 1 | 4 / 3 / 2 | 4 / 4 / 3 |
| worlds with no between-lineage adult pair in any year | 0 | 0 | 0 |
| **meeting: median rate per adult pair-year (frozen measure)** | **0.0487** | **0.0446** | **0.0006** |
| **reading** | **rarely** | **rarely** | **bands are effectively closed** |
| same-sex pairs only (Hill et al.'s sample; described) | 0.0416 | 0.0440 | 0.0005 |
| interacting (chose to talk, give or court): median per pair-year | 0.0085 | 0.0091 | 0.0002 |
| interacting, same-sex pairs | 0.0079 | 0.0094 | 0.0002 |
| meeting by period, years 0–29 / 30–59 / 60–89 / 90–119 | 0.0594 / 0.0427 / 0.0009 / 0.0043 | 0.0451 / 0.0538 / 0.0313 / 0.0047 | 0.0019 / 0.0003 / 0.0001 / 0.0000 |
| couples formed: between lineages / all | 118 / 918 (12.9%) | 171 / 3102 (5.5%) | 88 / 5977 (1.5%) |
| worlds with at least one between-lineage couple | 22 of 32 | 27 of 32 | 17 of 32 |
| recipes learned from a person of another lineage / all learned from people | 475 / 9320 (5.1%) | 770 / 15569 (4.9%) | 365 / 59814 (0.6%) |

Thresholds (operational cut-offs informed by Hill et al. 2014, not biological boundaries): ≥ 0.05 meet like forager bands; < 0.005 effectively closed; otherwise rarely. "Within sight" is an upper bound on contact (correction of 12 October).

## Do discovery and holdout agree? (the frozen condition for a reading to stand)

| arm | discovery | holdout | stands |
|---|---|---|---|
| C (20 founders, 40 × 40) | bands meet like forager bands (0.0504) | rarely (0.0487) | no: no reading |
| P (80 founders, 40 × 40) | rarely (0.0469) | rarely (0.0446) | **yes: rarely** |
| LP (80 founders, 80 × 80) | bands are effectively closed (0.0008) | bands are effectively closed (0.0006) | **yes: bands are effectively closed** |
