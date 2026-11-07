# PC1: the part chains of new kinds (results)

Frozen as `PC1-frozen`. run_pc1.py, analyse_pc1.py (written before data).

## Validity

- Zero checks (All: PASS, `code_v15` fingerprint): **yes**
- All worlds present (32): **yes**
- One fingerprint, `code_v15`'s: **yes**
- Tree checks and part-lesson event checks in every world (mismatches 0): **yes**

**Valid.**

## 1. Trees of the followed kinds (depth = the longest chain of made parts)

| depth | kinds | share |
|---|---|---|
| 0 | 12 | 0.004 [0.002, 0.008] (12 of 2,784) |
| 1 | 359 | 0.129 [0.117, 0.142] (359 of 2,784) |
| 2 | 1,085 | 0.390 [0.372, 0.407] (1,085 of 2,784) |
| 3+ | 1,328 | 0.477 [0.453, 0.499] (1,328 of 2,784) |

## 2. Lessons that failed on a missing part

Failed-on-part top-level lessons of followed kinds: 4,625.

| missing made parts | share |
|---|---|
| 1 | 0.965 [0.948, 0.978] (4,462 of 4,625) |
| 2 | 0.035 [0.022, 0.052] (163 of 4,625) |
| 3+ | 0.000 [0.000, 0.000] (0 of 4,625) |

| deepest missing chain | share |
|---|---|
| 1 | 0.093 [0.078, 0.109] (429 of 4,625) |
| 2 | 0.350 [0.315, 0.387] (1,620 of 4,625) |
| 3+ | 0.557 [0.514, 0.598] (2,576 of 4,625) |

**Does the teacher know the missing parts?**

- all of them: **0.926 [0.899, 0.952] (4,285 of 4,625)**
- some: 0.009 [0.004, 0.016] (43 of 4,625)
- none: **0.064 [0.038, 0.091] (297 of 4,625)**

## 3. The one-level part lesson (NV3's parts-first)

- A part lesson followed: 0.942 [0.916, 0.968] (4,359 of 4,625).
- of those, wasted (the learner knew the part): 0.011 [0.006, 0.018] (50 of 4,359)
- of those, declined: 0.780 [0.761, 0.799] (3,398 of 4,359)
- of those, missing_part: 0.209 [0.191, 0.226] (911 of 4,359)
- of those, taken: 0.000 [0.000, 0.000] (0 of 4,359)
- of those, distrust: 0.000 [0.000, 0.000] (0 of 4,359)
- the part shown was one the learner was missing: 0.990 [0.985, 0.995] (4,314 of 4,359)
- **not helpful** (wasted, declined, nested failure or distrust): **1.000 [1.000, 1.000] (4,359 of 4,359)**

## 4. Within 5 years, per learner and kind (after the first failed lesson)

- learned a missing part: 0.006 [0.004, 0.010] (21 of 3,369)
- learned the kind itself: 0.001 [0.000, 0.002] (2 of 3,369)
- made the kind: 0.000 [0.000, 0.000] (0 of 3,369)

## Reading (frozen)

**a deeper, learner-driven part lesson could help.**

Rule: "could help" if the teacher knows every missing part in more than half of failed lessons and the one-level part lesson is not helpful in more than half of those shown; "could not" if the teacher knows none in more than half; "mixed" otherwise.

