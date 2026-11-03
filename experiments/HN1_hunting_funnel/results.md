# HN1: Where do v11's hunts fail? (results)

Frozen as `HN1-frozen`. run_hn1.py, analyse_hn1.py (written before data).

## Validity

- Zero checks (All: PASS, same `code_v11` fingerprint): **yes**
- All worlds present (32): **yes**
- One fingerprint, `code_v11`'s: **yes**

**Valid.**

## The routing rule for HR1 (frozen)

- F = failed hunts with no prey on the tile ÷ all failed hunts = **0.0000 [0.0000, 0.0000]** (0 with no prey, 1,732 with a failed roll).
- **HR1 calibrates the base chance (hunt_base_chance).**

## The return ratio (HR1's target: the Aché's about 1.1; accepted range 0.5–1.5)

- **Pooled:** food kept per adult hunter-week ÷ food per adult forage-week = **0.0229 [0.0186, 0.0272]** (1,831 hunter-weeks, 5,583,050 forage-weeks).
- **Matched** (same person, season, year and plant-stock band): **0.0177 [0.0138, 0.0219]** (1,570 hunter-weeks matched, 261 without a match, dropped).

## The failure funnel (shares of adult hunter-weeks)

| hunters | hunter-weeks | (a) no prey | (b) roll failed | (c) success | food kept per hunter-week |
|---|---|---|---|---|---|
| all | 1,831 | 0.0000 | 0.9459 | 0.0541 | 0.475 |
| armed | 1,186 | 0.0000 | 0.9418 | 0.0582 | 0.517 |
| bare-handed | 645 | 0.0000 | 0.9535 | 0.0465 | 0.398 |

- **Meat lost to carrying room** (successes): 0.0000 of the meat share.
- **F8, expected against realized:** the decision's expected share per success averages 36.75; the meat share actually taken averages 8.79 and the meat kept 8.79 (successes 99).
- **Population beside it:** 26,623,393 living-weeks, 14,006,788 adult-weeks (16–49); extinct worlds 0.

## F7: success by species (tiles with a single prey species), against the unused table rates

| species | attempts | successes | rate | table rate (unused) |
|---|---|---|---|---|
| rabbit | 14,128 | 1,106 | 0.0783 | 0.40 |
| deer | 596 | 59 | 0.0990 | 0.16 |
| bison | 254 | 25 | 0.0984 | 0.10 |
| fish | 7,784 | 764 | 0.0982 | 0.25 |

