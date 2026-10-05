# E8.3 — Starvation autopsy · Results

Read-only replays of the E7 code, seeds 301–304, 120 years. The probe changed nothing (state hash, 20 years);
all four replays matched their saved runs; it recorded all 195 starvation deaths (the same count as E8 Arm 0).
Predictions frozen in E8_3_starvation_autopsy.md (tag `E8.3-frozen`). Data: `output_e83/`.

| measure | result |
|---|---|
| deaths in winter | **71%** (each season is 25% of person-weeks) |
| deaths in winter or the first 4 weeks of spring | **88%** |
| person-weeks spent starving, by season | spring 2.3%, summer 1.0%, autumn 1.2%, **winter 11.1%** |
| life stage of the dead | adults 55%, infants 21%, children 21%, elders 3%, teens 1% |
| … against all person-weeks | adults 53%, children 30%, teens 10%, elders 4%, infants 3% |
| infants and children who starved with their carer still alive | 80 of 81 |
| sick at death | 3% |
| food on hand 8 weeks before death (median) | **0** (need: 7 a week) |
| weeks starving before death (median) | 5 |
| plant food on their own tile ≥ a week's need, final week | 19% |
| plant food on all tiles within reach ≥ a week's need | 100% (median 176, spread over 49 tiles: about 3.6 a tile) |
| no stored food within reach | **84%** |
| carrying something that holds food | **0 of 195** |
| what adults, teens and elders did in their last 8 weeks | forage 46%, join others 19%, rest 15%, care 6%, gather 5%, put 4% |

## Frozen predictions, scored

1. **confirmed** — 88% of starvation deaths in winter or the first four weeks of spring (prediction: ≥ 60%).
2. **wrong** — infants, children and elders were 44% of deaths (prediction: ≥ 50%). Infants alone were 21% of
   deaths against 3% of person-weeks, seven times their share; adults died at about their share.
3. **confirmed as scored, but the measure was too generous** — every death had a week's need of plant food
   somewhere within reach, but spread thin: about 3.6 a tile, against a need of 7. On their own tile, only 19%
   did. The measure should have asked about food on any single reachable tile.
4. **confirmed** — 84% had no stored food within reach (prediction: ≥ 80%).

## The arithmetic of winter (from the code)

Loose food loses 4% a week; over a 13-week winter, food kept from autumn keeps about 59% of itself. Seeds are
edible and lose 0.5% a week; food beside a fire or under a covered heap rots more slowly. Plants regrow at 15% of
the spring rate in winter. Getting through a winter takes about 91 food, so about 150 laid by in autumn. A person
can carry 100 without a container; a carrier doubles it.

## What this says

- **The contradiction is resolved.** Food is plentiful on average because it is plentiful three seasons out of
  four. Hunger is concentrated in winter, and it kills.
- **The dead had laid nothing by.** Eight weeks before death, in late autumn, the typical person who starved had no
  food on hand at all. Most had no stored food anywhere within reach, and not one carried anything that holds food.
- **Storage is physically possible, and it is exactly what carriers and heaps are for.** A winter store needs more
  than one person can carry bare-handed. But no one ever fills even the bare-handed limit (E8.2: foraging was never
  cut short by it), so the carrier's one real use, holding a winter's food, is never experienced, and by Law 124
  never valued.
- **This is the raft again.** The tool exists, its use exists, and nobody lives through the use, so it is never
  valued. The open question is whether people fail to store because nothing in them looks ahead to winter, or
  because autumn gives too little surplus to store. That is the next thing to measure.
