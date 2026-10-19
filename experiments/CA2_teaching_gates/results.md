# CA2 — why teaching passes on so little: results

Frozen as `CA2-frozen`. run_ca2.py, analyse_ca2.py. Read-only: a logging copy of nature v2, shown to change nothing.

## Validity

- Zero check (logging copy = code_v2): **yes**
- All worlds present: **yes**
- Every replay ends in CA1's saved state: **yes**
- One fingerprint (`code_ca2`): **yes**

**Valid.**

## Discovery (16 worlds)

| gate | entering | passing | pass rate | stopped here for good |
|---|---|---|---|---|
| G1 meets | 5138 | 2768 | 0.539 | 2370 |
| G2 valued | 2768 | 902 | 0.326 | 1866 |
| G3 offered | 902 | 816 | 0.905 | 86 |
| G4 chosen | 816 | 782 | 0.958 | 34 |
| G5 new to the learner | 782 | 782 | 1.000 | 0 |
| G6 believed | 782 | 663 | 0.848 | 119 |
| G7 followable | 663 | 8 | 0.012 | 655 |

Useful inventions never passed on: **5138**. Of them, 8 were shown and taken, but the learner took away a different kind (counted by CA1 as a new kind).

- **Watching, for the same inventions (outcomes):** not_makers 530 (65%), draw_failed 266 (33%), known 9 (1%), copy_not_new_or_followable 6 (1%), bad_outcome 1 (0%).
- **Kept a year (G8), learners of useful inventions:** kept a year 6408 (97%), died 129 (2%), pushed out by the 12-recipe limit 45 (1%), not testable (world ended) 41 (1%).
- **Who built on what (CA1's link-5 pairs):** unclear, not passed on 2235 (48%), the inventor, not passed on 1916 (41%), unclear, passed on 274 (6%), a learner, not passed on 161 (3%), the inventor, passed on 56 (1%), a learner, passed on 30 (1%).
- **Living people** (median), decades 1–12: 26, 30, 26, 24, 28, 30, 35, 36, 30, 34, 38, 42.
- Log records: 1,446,550; unmatched: 0.

## Holdout (16 worlds)

| gate | entering | passing | pass rate | stopped here for good |
|---|---|---|---|---|
| G1 meets | 4853 | 2624 | 0.541 | 2229 |
| G2 valued | 2624 | 742 | 0.283 | 1882 |
| G3 offered | 742 | 690 | 0.930 | 52 |
| G4 chosen | 690 | 653 | 0.946 | 37 |
| G5 new to the learner | 653 | 653 | 1.000 | 0 |
| G6 believed | 653 | 558 | 0.855 | 95 |
| G7 followable | 558 | 3 | 0.005 | 555 |

Useful inventions never passed on: **4853**. Of them, 3 were shown and taken, but the learner took away a different kind (counted by CA1 as a new kind).

- **Watching, for the same inventions (outcomes):** not_makers 653 (72%), draw_failed 231 (26%), copy_not_new_or_followable 9 (1%), known 6 (1%), bad_outcome 2 (0%).
- **Kept a year (G8), learners of useful inventions:** kept a year 4470 (97%), died 76 (2%), pushed out by the 12-recipe limit 28 (1%), not testable (world ended) 23 (1%).
- **Who built on what (CA1's link-5 pairs):** unclear, not passed on 2072 (49%), the inventor, not passed on 1798 (42%), unclear, passed on 204 (5%), a learner, not passed on 153 (4%), the inventor, passed on 23 (1%), a learner, passed on 9 (0%).
- **Living people** (median), decades 1–12: 26, 28, 29, 27, 28, 26, 24, 21, 24, 26, 28, 24.
- Log records: 1,026,423; unmatched: 0.

## The frozen reading

**Most stopped at G1 meets** in both sets; **the lowest pass rate was elsewhere** (G7 followable in discovery, G7 followable in holdout).
