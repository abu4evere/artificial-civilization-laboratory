# E4 — Replication: E1 code against E2 code · Results

Worlds: 24 (16 new: 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216; plus 101–108 from E1/E2). Rules and predictions were frozen in predictions.md before the run.

## The decision rule

**Population at year 100.** E1 mean 44.0, E2 mean 25.6. E2 lower in 18 of 24 worlds (rule needs ≥ 17 of 24). Mean gap 18.4, 95% bootstrap interval [9.8, 27.2]. **Verdict: A (a real effect).**
New worlds alone: E1 mean 42.7, E2 mean 24.4; E2 lower in 12 of 16; mean gap 18.3, interval [6.5, 30.6].

**Infant starvation per 1000 infant-years** (worlds with infants under both codes: 24). E1 mean 68.8, E2 mean 67.6. Higher in E2 in 11 of 24. Mean gap -1.1, interval [-24.5, 23.7]. **Verdict: B (noise).** (The rule's 17-of-24 threshold is applied as written; with fewer than 24 worlds it is stricter.)

## Everything else, E1 code against E2 code (mean over worlds)

| measure | E1 | E2 |
|---|---|---|
| population at year 200 | 36.33 | 20.33 |
| worlds died out by 200 | 5 | 9 |
| births per 1000 person-years (first 100 years) | 33.04 | 30.57 |
| deaths per 1000 person-years (first 100 years) | 30.43 | 34.66 |
| births per fertile woman-year | 0.15 | 0.13 |
| infant deaths, all causes, per 1000 infant-years | 76.93 | 82.48 |
| mixed ancestry at year 100 | 72% | 34% |
| techniques tried | 440.50 | 318.04 |
| median technique life (years) | 22.13 | 13.54 |
| claims tested per world-year | 2.15 | 33.38 |
| people carrying a raft (years with 10+ alive) | 4% | 7% |
| open-water crossings | 0.00 | 60.33 |
| techniques taken up from marks | 0.00 | 87.38 |
| reputation tracks accuracy (pooled r, E2 only) | – | 0.644 |

## Frozen predictions, scored

1. Population lower under E2 by under 25%, rule ends unresolved or A: gap 42%, verdict A (a real effect).
2. Infant starvation higher under E2 by under 40%: -2%.
3. Mixing lower under E2 where islands are more than 3 tiles apart: lower in 0 of 0 such worlds (all worlds: 13 of 18).
4. E2's gains in every world: tests ≥ 10 per world-year in 19 of 19; crossings in 19; techniques from marks in 19; pooled reputation r = 0.644.
5. Techniques tried 440 → 318 (-28%); median life 22.1 → 13.5 years (-39%).
6. A new world collapsing under E2 but not E1: 201, 203, 206, 210.

## Per world

| seed | pop @100 E1 → E2 | pop @200 E1 → E2 | infant starvation /1000 E1 → E2 | mixed @100 E1 → E2 |
|---|---|---|---|---|
| 101 | 0 → 0 | 0 → 0 | 97 → 246 | – → – |
| 102 | 61 → 37 | 58 → 30 | 62 → 21 | 0% → 49% |
| 103 | 50 → 41 | 33 → 32 | 38 → 24 | 88% → 0% |
| 104 | 92 → 46 | 87 → 55 | 52 → 68 | 48% → 2% |
| 105 | 30 → 1 | 0 → 0 | 25 → 0 | 100% → 100% |
| 106 | 65 → 32 | 29 → 3 | 44 → 102 | 97% → 22% |
| 107 | 46 → 36 | 52 → 21 | 57 → 168 | 65% → 72% |
| 108 | 29 → 32 | 31 → 29 | 44 → 79 | 97% → 0% |
| 201 | 64 → 6 | 80 → 0 | 100 → 44 | 47% → 100% |
| 202 | 57 → 51 | 97 → 53 | 29 → 42 | 100% → 0% |
| 203 | 26 → 0 | 14 → 0 | 65 → 0 | 42% → – |
| 204 | 22 → 25 | 0 → 14 | 88 → 60 | 68% → 100% |
| 205 | 27 → 25 | 28 → 34 | 77 → 17 | 100% → 0% |
| 206 | 53 → 0 | 39 → 0 | 70 → 111 | 100% → – |
| 207 | 84 → 38 | 45 → 35 | 86 → 63 | 33% → 0% |
| 208 | 1 → 0 | 0 → 0 | 61 → 0 | 100% → – |
| 209 | 27 → 36 | 33 → 30 | 46 → 137 | 93% → 0% |
| 210 | 59 → 0 | 54 → 0 | 68 → 0 | 32% → – |
| 211 | 27 → 1 | 3 → 0 | 56 → 94 | 89% → 0% |
| 212 | 0 → 13 | 0 → 0 | 245 → 134 | – → 100% |
| 213 | 73 → 60 | 56 → 51 | 47 → 68 | 99% → 0% |
| 214 | 77 → 76 | 77 → 65 | 63 → 51 | 78% → 55% |
| 215 | 24 → 33 | 14 → 7 | 70 → 31 | 8% → 0% |
| 216 | 62 → 26 | 42 → 29 | 60 → 62 | 98% → 54% |

## Correction to prediction 3

The analysis first measured the narrowest water between *any* two islands, including empty ones, and found no
qualifying world. Measured between the islands where the bands started, every world still has at least one pair
within 3 tiles, so no world fits the prediction as written: **unclear (untestable as stated)**. In the 18 worlds
where both codes reached year 100, mixing was lower under E2 in 13.

## Why the population is lower: the fate of each founding band

Every world starts with 4 bands of 5 people, each on its own island. For each of the 96 bands (24 worlds × 4),
did it ever have children with another band, and did its line survive?

| | E1 | E2 |
|---|---|---|
| bands that ever mixed with another band | 67 of 96 (70%) | 37 of 96 (39%) |
| line alive at year 100: bands that mixed | 82% | 65% |
| line alive at year 100: bands that never mixed | 17% | 17% |
| line alive at year 200: bands that mixed | 70% | 43% |
| line alive at year 200: bands that never mixed | 17% | 12% |

**Isolation is deadly under both codes.** A band of 5 that never mixes almost always dies out: everyone on its
island ends up related, and nobody is left to pair with. E2 does not make isolation deadlier. It makes it far
more common. With the 3-tile jump gone and rafts carried by only about 7% of people, 59 bands never met another
band, against 29 under E1.

This is the creator's Hypothesis B (island separation), confirmed over 24 worlds. The E3 explanation (infant
starvation in mothers' care) did not replicate: it came from two unusual worlds.

## Summary

- **Population: A, a real effect.** E2 lower in 18 of 24 worlds, mean gap 18.4 at year 100 (95% interval 9.8 to
  27.2); 9 worlds died out by year 200 under E2, against 5 under E1.
- **Cause: isolation of founding bands** (above), not lost fertility within couples and not infant starvation.
- **Infant starvation: B, noise** (68.8 vs 67.6 per 1000 infant-years).
- **E2's gains held in every world that lived:** claims tested ≥ 10 per world-year (19 of 19); crossings and
  techniques from marks in all 19; reputation tracks accuracy (r = 0.64).
- **Costs beyond population:** techniques tried fell 28% and their median life 39%; fewer people keep fewer
  things alive.

## Predictions, final

1. Wrong: the gap was 42%, not under 25% (verdict A).
2. Wrong as worded: infant starvation did not rise (−2%).
3. Unclear: untestable as stated (see correction).
4. Confirmed.
5. Wrong: techniques −28%, median life −39%.
6. Confirmed: seeds 201, 203, 206 and 210 collapsed under E2 but not E1.
