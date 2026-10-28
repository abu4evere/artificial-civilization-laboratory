# PG0 — The "why" audit. Results

Frozen as `PG0-frozen` (operational note 1). run_pg0.py, analyse_pg0.py (written before data).

## Validity

- Zero checks: **yes**
- All worlds present (32 of 32): **yes**
- One fingerprint (`code_v7`): **yes**
- Mismatches 0: **yes**

**Valid.**

32 worlds; mean living population over all years 124.7.

## Q1 — Curiosity: does puzzle-led play find useful new kinds?

Puzzle-led play: 291 of 397147 plays (0.0007).

| play | plays | new-to-world kinds per play | of those, useful | of the useful, remade later |
|---|---|---|---|---|
| led | 291 | 0.1375 [0.1032, 0.1750] (40 / 291) | 1.0000 [1.0000, 1.0000] (40 / 40) | 0.3000 [0.1538, 0.4848] (12 / 40) |
| free | 396856 | 0.1009 [0.0962, 0.1062] (40059 / 396856) | 1.0000 [1.0000, 1.0000] (40059 / 40059) | 0.2213 [0.2169, 0.2259] (8865 / 40059) |

**Useful new-to-world kinds per play, puzzle-led minus other: +0.0365 [+0.0029, +0.0727].** (Described, not causal.)

## Q2 — The zero start

- At first use of a kind: mean |felt − worth before| = 0.1599 [0.1581, 0.1617] (25198 / 157596).
- New useful kinds made in play: used by their maker 29983; lost before use: gone from hand 9939, maker died 171; share lost before use **0.2522** (of 40093; 6 still pending at the end).
- Uses until worth is within 0.1 of the felt value: mean 2.32 (142129 person-kinds learned).

## Q3 — Is information available? Prediction error at first use of a new kind (own past uses only)

| predictor | mean absolute error [95%] |
|---|---|
| own-experience property neighbours (k = 5) | 0.0717 [0.0707, 0.0726] (6100 / 85136) |
| shuffled properties (control) | 0.1053 [0.1042, 0.1065] (8965 / 85136) |
| zero start (today) | 0.1522 [0.1498, 0.1548] (12962 / 85136) |

First uses with at least 5 past uses for the same purpose: 85136; without: 72460.

**Shuffled minus property error: +0.0337 [+0.0329, +0.0343]: information IS available in a person's own past experience.**

