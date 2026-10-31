# TA1 — Why do tools not reach hands? Results

Frozen as `TA1-frozen` (operational note 1). run_ta1.py, analyse_ta1.py (written before data).

## Validity

- Zero checks: **yes**
- All worlds present (32 of 32): **yes**
- One fingerprint (`code_v10`): **yes**
- Forage-tool accounting exact; no worn tool still in hand (mismatches 0): **yes**

**Valid.**

Worlds: 32; extinct 0. Mean living population 141.7; adults in years 100-200: 105.8 per world-year; forage tools in hand at year ends (years 100-200): 35.9 per world.
Adult forage weeks, years 100-200: 7,026,833; bare-handed 6,310,506 (0.898 [0.892, 0.904]).

## Q1 — Why is a forager bare-handed? (share of bare-handed adult forage weeks)

| flag | share [95%] |
|---|---|
| **(a) a forage tool in someone's hands within 3 tiles** | **0.819 [0.802, 0.834]** |
| (a') the same, and the forager has room to receive it | 0.680 [0.649, 0.709] |
| **(b) knows a helpful kind and could make it now** | **0.726 [0.712, 0.739]** |
| (c) knows a helpful kind but lacks the materials | 0.268 [0.257, 0.280] |
| (d) knows no helpful kind | 0.005 [0.002, 0.010] |
| (e) hands full (3 items, none for foraging) | 0.161 [0.131, 0.193] |
| empty hands (0 items) | 0.479 [0.441, 0.519] |
| hands holding other things (1-3 non-forage items) | 0.521 [0.481, 0.559] |

Priority partition (Gemini): e 0.161; b 0.608; c 0.226; d 0.005.

**Q5** (described): in the (a') weeks, the nearest holder's actual tool would add 0.099 [0.097, 0.100] to those forages' food (TR1's arithmetic, with the carry room and plants).

## Q2 — Who holds forage tools (person-weeks, years 100-200)

| age | person-weeks | share holding a forage tool |
|---|---|---|
| 0-11 | 5,405,470 | 0.392 |
| 12-15 | 1,785,023 | 0.137 |
| 16-39 | 9,874,992 | 0.105 |
| 40-59 | 5,700,171 | 0.111 |
| 60+ | 2,063,758 | 0.111 |

Adult holders who foraged that week: 0.367 of 1,901,473 holder-weeks.

## Q3 and Q4 — How forage tools enter and leave hands (all ages, whole run)

| enter | count | share |
|---|---|---|
| made | 360,470 | 0.869 |
| picked_up | 46,691 | 0.113 |
| passed | 4,528 | 0.011 |
| from_body | 3,043 | 0.007 |

| leave | count | share |
|---|---|---|
| used_or_changed | 230,247 | 0.556 |
| worn | 153,392 | 0.371 |
| dropped | 16,895 | 0.041 |
| to_body | 8,814 | 0.021 |
| passed | 4,528 | 0.011 |
| lost_at_death | 51 | 0.000 |

Mean weeks a forage tool stays in one hand: 58.6 (413,927 exits).
Forage-tool makes by someone already holding one: 0.545 of 86,586.

## The frozen reading

- (a) 0.819 [0.802, 0.834] (>= 0.50 for 'access gap'); (b) 0.726 [0.712, 0.739] (>= 0.50 for 'choice gap').

**Reading: BOTH.** (A classification, not causal proof; GPT.)

