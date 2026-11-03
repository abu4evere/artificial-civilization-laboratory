# FF2: Fixing three more faults, in nature v12 (results)

Frozen as `FF2-frozen`. run_ff2.py, analyse_ff2.py (written before data).

## Validity

- Zero checks (All: PASS, same `code_ff2` fingerprint): **yes**
- All worlds present (192): **yes**
- One fingerprint, `code_ff2`'s: **yes**

**Valid.**

## Decision (frozen): a check for harm only, f against v12

| contrast | living-weeks ratio [95%] | extinct worlds (arm, v12) |
|---|---|---|
| f / v12 | 1.0008 [0.8893, 1.1203] | 0, 0 |
| f8 / v12 | 1.0284 [0.9359, 1.1345] | 0, 0 |
| f4 / v12 | 0.9425 [0.8362, 1.0492] | 0, 0 |
| f5 / v12 | 0.9293 [0.7924, 1.0747] | 1, 0 |
| sham / v12 | 0.9524 [0.8689, 1.0475] | 0, 0 |

Guards (f against v12): population if the ratio is below 0.90 with its upper bound below 1; extinctions if f has 3 or more extinct worlds beyond v12's.

**Reading: no harm.** No guard raised.

## Flags for investigation (f against v12; frozen rule: ratio outside [0.8, 1.25] with its 95% interval wholly outside 1)

| measure | f / v12 [95%] | sham / v12 [95%] | flag |
|---|---|---|---|
| hunt options per adult-week | 1.1341 [1.0178, 1.2753] | 1.0119 [0.8865, 1.1423] | no |
| food per success the option expects, v12's rule | 0.9942 [0.9872, 1.0008] | 1.0091 [1.0008, 1.0181] | no |
| food per success the option expects, fixed rule | 1.0261 [1.0155, 1.0372] | 1.0010 [0.9892, 1.0123] | no |
| adult hunter-weeks per adult-week | 0.7888 [0.7128, 0.8835] | 1.0242 [0.8934, 1.1671] | **FLAG** |
| hunt success share | 0.9501 [0.7199, 1.2390] | 0.9523 [0.7229, 1.2573] | no |
| meat from hunts per adult-week | 0.7542 [0.5535, 1.0308] | 0.9897 [0.7072, 1.4154] | no |
| material units past the limit, hunts | nan [nan, nan] | nan [nan, nan] | no |
| material units past the limit, inheritance | 0.9501 [0.8049, 1.1306] | 0.9762 [0.8021, 1.1960] | no |
| water-walk weeks with a carry thing that cannot hold water, per walk week | 1.0155 [0.9380, 1.1058] | 1.0477 [0.9623, 1.1452] | no |
| makes per adult-week | 0.9236 [0.8357, 1.0179] | 0.9865 [0.9109, 1.0674] | no |
| made things held per adult | 0.9369 [0.8273, 1.0574] | 1.0089 [0.8906, 1.1464] | no |
| adult-weeks | 1.0050 [0.8933, 1.1237] | 0.9543 [0.8706, 1.0486] | no |

**Flags: adult hunter-weeks per adult-week.**

## Described (not decisive), per arm

| arm | living-weeks | adult-weeks | hunt options per 1,000 adult-weeks | expected food per success (v12 rule, fixed rule) | adult hunter-weeks per 1,000 adult-weeks | hunts, successes (share) | meat from hunts per adult-year | units past the limit: hunts, inheritance | water-walk weeks (adults), with a leaky carry thing | makes per adult-year | made things per adult |
|---|---|---|---|---|---|---|---|---|---|---|---|
| v12 | 23,614,153 | 16,737,496 | 182.148 | 35.60, 8.45 | 0.1375 | 2,574, 137 (0.0532) | 0.0038 | 0.0, 4418.4 | 447,970, 41,209 | 0.0727 | 0.953 |
| f | 23,633,592 | 16,821,414 | 206.576 | 35.40, 8.67 | 0.1085 | 2,017, 102 (0.0506) | 0.0028 | 0.0, 4197.9 | 432,902, 40,441 | 0.0672 | 0.893 |
| f8 | 24,283,717 | 17,143,957 | 203.128 | 35.41, 8.62 | 0.1039 | 1,992, 104 (0.0522) | 0.0030 | 0.0, 4173.1 | 444,188, 40,021 | 0.0687 | 0.958 |
| f4 | 22,256,712 | 15,707,001 | 183.200 | 35.60, 8.43 | 0.1438 | 2,528, 150 (0.0593) | 0.0045 | 0.0, 4034.2 | 381,731, 36,404 | 0.0681 | 0.883 |
| f5 | 21,945,463 | 15,657,385 | 185.441 | 35.56, 8.46 | 0.1436 | 2,534, 123 (0.0485) | 0.0037 | 0.0, 3946.5 | 422,279, 38,171 | 0.0713 | 1.002 |
| sham | 22,491,147 | 15,972,683 | 184.320 | 35.93, 8.46 | 0.1409 | 2,545, 129 (0.0507) | 0.0037 | 0.0, 4313.3 | 408,576, 39,377 | 0.0718 | 0.962 |

