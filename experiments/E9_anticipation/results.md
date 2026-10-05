# E9 — Anticipation (A2) · Results

Arm 0 = E7 code; A2-low and A2-full = E7 code + A2 at weight 0.375 and 1.0. Seeds 301–304, 120 years. Pre-registration frozen as `E9-frozen` before any code. Analysis order fixed by the creator: validity, causal links, then survival.

## 1. Validity

- Probe read-only (both codes): **yes**
- All runs finished: **yes**
- Zero-weight A2 code reproduces Arm 0 (seed 304, every 10 years): **yes**
- Arm 0 reproduces the saved E7 runs: **yes**
- Code unchanged during runs: **yes**
- **Valid.**

## 2. Leak test (hard fail)

Autumn foraging share of adults who have never gone short in any winter.

| seed | arm 0 | A2-low | A2-full |
|---|---|---|---|
| 301 | 0.510 (n=38) | 0.471 (n=32) | 0.491 (n=37) |
| 302 | 0.454 (n=52) | 0.477 (n=55) | 0.501 (n=41) |
| 303 | 0.482 (n=30) | 0.477 (n=30) | 0.493 (n=29) |
| 304 | 0.485 (n=40) | 0.477 (n=35) | 0.438 (n=49) |
| pooled | 0.480 (n=160) | 0.476 (n=152) | 0.477 (n=156) |

**Leak test passed** (A2 arms within ±10% of Arm 0, pooled).

## 3. Causal links

| seed | arm | autumn foraging, short last winter | median winter entry | adult-autumns reaching 80 | carriers made | carrier worth @120 |
|---|---|---|---|---|---|---|
| 301 | arm0 | 0.417 (n=1141) | 12.2 | 0 of 2326 | 406 | 0.131 |
| 301 | a2low | 0.444 (n=666) | 12.8 | 2 of 1686 | 368 | 0.092 |
| 301 | a2full | 0.457 (n=1534) | 12.3 | 22 of 2666 | 444 | 0.108 |
| 302 | arm0 | 0.437 (n=2828) | 14.0 | 0 of 4564 | 887 | 0.126 |
| 302 | a2low | 0.414 (n=2984) | 13.9 | 1 of 4790 | 869 | 0.148 |
| 302 | a2full | 0.448 (n=1994) | 13.0 | 36 of 3476 | 510 | 0.123 |
| 303 | arm0 | 0.437 (n=1805) | 12.8 | 0 of 2757 | 347 | 0.088 |
| 303 | a2low | 0.426 (n=516) | 11.8 | 0 of 1405 | 359 | 0.092 |
| 303 | a2full | 0.432 (n=2049) | 11.8 | 26 of 3268 | 363 | 0.109 |
| 304 | arm0 | 0.450 (n=1463) | 11.9 | 0 of 2185 | 398 | 0.092 |
| 304 | a2low | 0.447 (n=1341) | 11.7 | 2 of 2066 | 315 | 0.104 |
| 304 | a2full | 0.464 (n=1312) | 12.3 | 28 of 2150 | 321 | 0.094 |

## 4. Survival (looked at last)

| seed | arm | winter starvation deaths | all starvation deaths | infant deaths | pop @60 / 90 / 120 | plants left at end of autumn (mean) |
|---|---|---|---|---|---|---|
| 301 | arm0 | 13 | 23 | 4 | 34 / 31 / 40 | 16396 |
| 301 | a2low | 3 | 4 | 2 | 21 / 26 / 25 | 17221 |
| 301 | a2full | 32 | 52 | 15 | 48 / 42 / 38 | 16091 |
| 302 | arm0 | 52 | 78 | 16 | 68 / 90 / 96 | 15828 |
| 302 | a2low | 31 | 57 | 18 | 67 / 83 / 92 | 16160 |
| 302 | a2full | 31 | 46 | 8 | 63 / 58 / 55 | 16496 |
| 303 | arm0 | 44 | 55 | 13 | 43 / 52 / 50 | 15975 |
| 303 | a2low | 3 | 8 | 2 | 14 / 16 / 19 | 17254 |
| 303 | a2full | 30 | 42 | 9 | 51 / 71 / 73 | 15702 |
| 304 | arm0 | 30 | 39 | 12 | 30 / 39 / 39 | 18115 |
| 304 | a2low | 24 | 37 | 12 | 23 / 37 / 42 | 17134 |
| 304 | a2full | 40 | 43 | 5 | 27 / 39 / 38 | 18256 |

## 5. Frozen predictions, scored

1. **wrong** (manipulation check) — A2-full autumn foraging of adults short last winter, ÷ Arm 0: 301: 1.09, 302: 1.02, 303: 0.99, 304: 1.03 (0 of 4 ≥ 1.3).
2. **confirmed** — dose response (A2-low rise smaller than A2-full) in 4 of 4 seeds: 301: 1.06 vs 1.09, 302: 0.95 vs 1.02, 303: 0.98 vs 0.99, 304: 0.99 vs 1.03.
3. **wrong** — A2-full median winter entry ≥ 2× Arm 0 in 0 of 4 seeds: 301: 12.3 vs 12.2, 302: 13.0 vs 14.0, 303: 11.8 vs 12.8, 304: 12.3 vs 11.9.
4. **wrong** — winter starvation deaths, A2-full 133 vs Arm 0 139 (needs ≤ 80%).
5. **wrong** — A2-full adult-autumns reaching 80 food in hand: 112 of 11560 (0.97%; needs ≥ 1%).
6. **confirmed** — leak test (section 2).

## 6. Descriptive: the people who reached the carrying limit (not a frozen test)

| arm | adult-autumns reaching 80 | went short last winter | autumn weeks foraging | food entering winter (median) | everyone else's |
|---|---|---|---|---|---|
| arm0 | 0 | – | – | – | 12 |
| A2-low | 5 | 60% | 55% | 39 | 13 |
| A2-full | 112 | 100% | 73% | 74 | 12 |

For the few people it moved, A2 did what the hypothesis said: they foraged much more in autumn and entered winter
with six times the food. It moved too few to change any frozen measure. E9.1 asks why.

## Reading, per the frozen decision table

Prediction 1 (the manipulation check) failed in A2-full: anticipating a season one has gone short in, as built,
does not change autumn behaviour enough to matter, even at full strength. The leak test passed, so the mechanism did
not act on anyone who had nothing to anticipate. The table's next step is to ask why the lesson is so faint for most
adults; E9.1 does that.
