# MP1: where do the made parts of new kinds go? (results)

Frozen as `MP1-frozen`. run_mp1.py, analyse_mp1.py (written before data).

## Validity

- Zero checks (All: PASS, `code_v15` fingerprint): **yes**
- All worlds present (32): **yes**
- One fingerprint, `code_v15`'s: **yes**
- In every world: tracked parts 441; gone unexplained 0; stage checks failed 0: **yes**

**Valid.**

## Primary: how far each followed kind gets (3,690 new kinds with made parts, years 100-190)

| stage | | kinds | share [95%] |
|---|---|---|---|
| A | no knower holds any of its made parts | 3,330 | 0.9024 [0.8907, 0.9142] |
| B | some parts held, never all at once | 208 | 0.0564 [0.0470, 0.0666] |
| C | all made parts held, but cannot make it | 37 | 0.0100 [0.0065, 0.0135] |
| D | could make it, never made again | 62 | 0.0168 [0.0136, 0.0202] |
| E | made again | 53 | 0.0144 [0.0103, 0.0193] |

**Reading (frozen): most kinds stop at A (no knower holds any of its made parts), clear** (A 0.9024 [0.8907, 0.9142] against the next, B, 0.0564 [0.0470, 0.0666]).

Rule: the largest share among A-D; 'clear' if its lower bound is above the next largest's upper bound.

## By depth (the longest chain of made parts)

| depth | kinds | A | B | C | D | E |
|---|---|---|---|---|---|---|
| 1 | 437 | 0.684 | 0.192 | 0.055 | 0.046 | 0.023 |
| 2 | 1,402 | 0.887 | 0.061 | 0.006 | 0.022 | 0.024 |
| 3+ | 1,851 | 0.965 | 0.021 | 0.002 | 0.006 | 0.005 |

## The inventor alone

| stage | share |
|---|---|
| A | 0.9081 [0.8973, 0.9191] |
| B | 0.0566 [0.0473, 0.0667] |
| C | 0.0100 [0.0065, 0.0135] |
| D | 0.0173 [0.0141, 0.0208] |
| E | 0.0079 [0.0059, 0.0098] |

## Secondary: the first fate of each tracked part (441 parts)

| fate | parts | share [95%] |
|---|---|---|
| handed to another | 219 | 0.4966 [0.4295, 0.5551] |
| worn out in use | 61 | 0.1383 [0.1042, 0.1789] |
| used: into another thing | 57 | 0.1293 [0.0866, 0.1720] |
| worn out by the cold | 40 | 0.0907 [0.0644, 0.1253] |
| used: into its kind | 32 | 0.0726 [0.0533, 0.0964] |
| still held | 21 | 0.0476 [0.0292, 0.0698] |
| dropped at the carry limit | 11 | 0.0249 [0.0049, 0.0528] |

After a drop at the carry limit (11): picked up by someone else 11 (1.000)
Left with a body and later taken: 0.

## Described

- Knower-weeks at the 3-thing carry limit: 32,770 of 878,365 (0.0373).
- Drops of tracked parts by the carry-limit step: 11 (8 of them the part just made, dropped at once); the dropped part was its holder's least valued thing in 11; valued 0 by its holder in 6.
- New kinds made by a non-inventor within 5 years: 24 of 3,690.

