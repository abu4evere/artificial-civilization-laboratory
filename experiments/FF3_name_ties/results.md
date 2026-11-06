# FF3: Memory ties settled by name, a fault fix in nature v13 (results)

Frozen as `FF3-frozen`. run_ff3.py, analyse_ff3.py (written before data). Years 100–200.

## Validity

- Zero checks (All: PASS, same `code_ff3` fingerprint): **yes**
- All worlds present (96): **yes**
- One fingerprint, `code_ff3`'s: **yes**

**Valid.**

## Decision (frozen): a check for harm only, f against v13

| contrast | living-weeks ratio [95%] | extinct worlds (arm, v13) |
|---|---|---|
| f / v13 | 0.9636 [0.8506, 1.0867] | 2, 1 |
| sham / v13 | 0.9576 [0.8526, 1.0747] | 2, 1 |

Guards (f against v13): population if the ratio is below 0.90 with its upper bound below 1; extinctions if f has 3 or more extinct worlds beyond v13's.

**Reading: no harm.** No guard raised.

## Flags for investigation (f against v13; frozen rule: ratio outside [0.8, 1.25] with its 95% interval wholly outside 1)

| measure | f / v13 [95%] | sham / v13 [95%] | flag |
|---|---|---|---|
| recipes: evictions per adult-week | 1.1829 [0.9728, 1.4131] | 1.0459 [0.8369, 1.2798] | no |
| recipes: evictions with a tie, per eviction | 0.7488 [0.6873, 0.8224] | 0.9982 [0.9298, 1.0802] | **FLAG** |
| marks: evictions per adult-week | 1.0444 [0.8516, 1.3084] | 0.9560 [0.7499, 1.2000] | no |
| marks: evictions with a tie, per eviction | 0.8855 [0.8543, 0.9180] | 1.0144 [0.9649, 1.0644] | no |
| records: evictions per adult-week | 1.0931 [0.9180, 1.2932] | 0.7836 [0.6273, 1.0044] | no |
| records: evictions with a tie, per eviction | 0.8358 [0.7572, 0.9284] | 1.0242 [0.8491, 1.2684] | no |
| puzzles: evictions per adult-week | 1.0765 [0.8480, 1.3972] | 0.9468 [0.7618, 1.1685] | no |
| puzzles: evictions with a tie, per eviction | 0.9849 [0.9376, 1.0353] | 1.0448 [0.9243, 1.1574] | no |
| recipes: the newest dropped, per eviction | 0.8727 [0.8347, 0.9054] | 0.9952 [0.9667, 1.0226] | no |
| world-new kinds | 0.9588 [0.8577, 1.0621] | 1.0119 [0.8537, 1.1991] | no |
| kinds made again by their inventor within 5 years | 0.0000 [0.0000, 0.0000] | 0.0000 [0.0000, 0.0000] | **FLAG** |
| makes per adult-week | 1.0334 [0.9439, 1.1287] | 1.0416 [0.9508, 1.1396] | no |
| adult-weeks | 0.9674 [0.8594, 1.0858] | 0.9555 [0.8509, 1.0695] | no |

**Flags: recipes: evictions with a tie, per eviction, kinds made again by their inventor within 5 years.**

## Described (not decisive), per arm

| arm | living-weeks | adult-weeks | recipes: evictions, ties, newest dropped, kept at birth | marks: evictions, ties | records: evictions, ties | puzzles: evictions, ties | draws | world-new kinds, remade | makes per adult-year |
|---|---|---|---|---|---|---|---|---|---|
| v13 | 19,404,795 | 13,891,925 | 17,646, 11,310, 12,387, 0.298 | 1,598,878, 364,548 | 583,933, 62,570 | 438,830, 38,611 | 0 | 3,183, 1 | 0.0724 |
| f | 18,698,034 | 13,439,067 | 20,193, 9,691, 12,370, 0.387 | 1,615,359, 326,134 | 617,492, 55,300 | 457,018, 39,604 | 430,729 | 3,052, 0 | 0.0748 |
| sham | 18,582,683 | 13,273,054 | 17,634, 11,282, 12,319, 0.301 | 1,460,398, 337,759 | 437,170, 47,977 | 396,956, 36,493 | 0 | 3,221, 0 | 0.0754 |

