# E7 — Passive affordances · Results

Design, definitions, predictions and decision rule were frozen in E7_passive.md before any run. Implementation fixes made before the runs are listed in implementation_notes.md. LFA = first year of the latest lasting novelty (E6 definition).

## Validity (kill criteria, §9)

- Recorder read-only (state hash with and without it, 20 years, both arms): **yes** (e7 seed 304, 20 years: without 17e12e4986afa880  with 17e12e4986afa880  -> READ-ONLY; baseline seed 304, 20 years: without 89fa38cbd717bece  with 89fa38cbd717bece  -> READ-ONLY)
- E7 code unchanged during the runs: **yes** (28f3a5265e40310b)
- Baseline code unchanged during the runs, and it is E6's verified code: **yes** (b3f7153accc0e681)
- No world crashed or failed to finish: **yes** (all 16 finished)
- At least 6 worlds completed in each arm: **yes** (E7 8, baseline 8)
- Baseline replicates E6 (population every 10 years and LFA): **yes** (301 yes, 302 yes, 303 yes, 304 yes, 305 yes, 306 yes, 307 yes, 308 yes)
- **The experiment is valid.**

## World by world

| seed | baseline lived | baseline LFA | E7 lived | **E7 LFA** | E7 later? | FEC water | FEC ceramic | FEC food by fire | carried-water drinks | ≥3 tiles | ≥5 tiles | max tiles | fired objects | outlived maker | new traditions after yr 100 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 301 | 1000 | 28 | 1000 | **115** | yes | 1 | 226 | 646 | 0 | 0 | 0 | – | 217 | 9 | 1 |
| 302 | 1000 | 22 | 1000 | **54** | yes | 0 | 100 | 481 | 0 | 0 | 0 | – | 116 | 4 | 2 |
| 303 | 1000 | 25 | 1000 | **25** | no | 0 | 12 | 80 | 0 | 0 | 0 | – | 8 | 0 | 0 |
| 304 | 1000 | 66 | 1000 | **11** | no | 1 | 21 | 133 | 0 | 0 | 0 | – | 15 | 1 | 2 |
| 305 | 70 | 6 | 115 | **17** | yes | 1 | 30 | 100 | 0 | 0 | 0 | – | 29 | 0 | 0 |
| 306 | 124 | 14 | 465 | **19** | yes | 0 | 250 | 595 | 0 | 0 | 0 | – | 250 | 11 | 6 |
| 307 | 103 | 14 | 104 | **12** | no | 0 | 1 | 76 | 0 | 0 | 0 | – | 1 | 0 | 0 |
| 308 | 96 | 14 | 95 | **11** | no | 0 | 7 | 162 | 0 | 0 | 0 | – | 5 | 0 | 0 |

Lasting novelties first appearing in each century (all worlds pooled):

| century | 0–100 | 101–200 | 201–300 | 301–400 | 401–500 | 501–600 | 601–700 | 701–800 | 801–900 | 901–1000 |
|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 578 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| E7 | 628 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

## The frozen decision rule (§7)

- Counted E7 worlds (lived 300+ years): 5 (301, 302, 303, 304, 306); half = 3.
- Counted worlds with LFA ≥ 150: 0 (none).
- Counted worlds with LFA ≤ 50 (or no lasting novelty): 3 (303, 304, 306).
- Seed pairs where E7's LFA is later than the baseline's: 4 of 8.
- Counted worlds with water drunk 5+ tiles from fresh water: 0.
- Worlds where carried water was drunk at all: 0.
- Reading: "water never carried in any world" means no drink from a carried vessel in any E7 world.
- **Verdict: BOTTLENECK REMAINS.**

## Failure mode (§7)

- Pooled FEC: water 3, ceramic 647. New traditions after year 100: 11.
- Reading: the thresholds are applied to totals pooled over the 8 worlds; per-world counts are in the table.
- Neither failure mode's definition is met exactly; see the per-world table.

## Frozen predictions, scored (§8)

1. **wrong** — seed 304: first passive fill year 31; drinks 3+ tiles from fresh water 0, from year – to –. Reading: "lasting tradition" = such drinks spanning 50+ years.
2. **confirmed** — passive firing happened in 8 worlds; fired objects carried 50+ years that outlived their maker: 6.
3. **wrong** — FEC water ≥ 10 in 0 of 8 worlds (needs 6); FEC ceramic ≥ 5 in 7 of 8 (needs 4).
4. **wrong** — E7 LFA after year 100 in 1 of 8 worlds (needs 4).
5. **wrong** — E7 LFA later than baseline in 4 of 8 pairs (needs 6).
6. **confirmed** — E7 worlds alive at year 1000: 4 (301, 302, 303, 304); baseline: 4.
7. **confirmed** — surviving worlds with a new tradition originating after year 100: 3 (needs 3).

New Consequence 3 (food eaten past its natural rot threshold) is not measurable in this world: food is one pooled amount per person with no age. `food_by_fire` counts person-weeks with food beside a fire, where the existing smoke rule already slows rot.
