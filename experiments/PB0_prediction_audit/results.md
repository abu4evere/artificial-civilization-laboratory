# PB0: Would knowing what happens next change people's choices? (results)

Frozen as `PB0-frozen`. run_pb0.py, analyse_pb0.py (written before data).

## Validity

- Zero checks (All: PASS, same `code_v12` fingerprint): **yes**
- All worlds present (32): **yes**
- One fingerprint, `code_v12`'s: **yes**

**Valid.**

## Primary (frozen): held-out gain of foresight at 4 weeks

| decisions studied | G (held-out gain over the top-scored option) [95%] | A (mean abs. outcome of the top option) | G / A | reading |
|---|---|---|---|---|
| 3,328 (skipped 0) | +0.1592 [+0.1512, +0.1672] | 0.5074 | 0.314 | **GO** |

Rule: GO to PB1 if G's 95% interval lies wholly above 0 and G >= 0.05 x A; otherwise NO-GO.

## Described (no decision drawn)

- **S, regret share:** 0.5589 of decisions have a held-out gain above the mean noise SD (0.0985).
- **The gain's parts** (mean per decision): from reward +0.1475, from mood +0.0117.
- **At 4 weeks, winner against top** (held-out means): alive 0.9986 against 0.9982; food 12.526 against 12.555; health 91.71 against 92.11.
- **The winner's kind:** other 2688, same 486, food 68, make 40, gather 38, hunt 8.
- **H = 1** (in sample, one run per option): mean gain +0.1315 over 3328 decisions.
- **H = 13** (long sample, held out): mean gain +0.1592 over 416 decisions.
- **H = 26** (long sample, held out): mean gain +0.1600 over 416 decisions.
- **All-options sample:** the full-menu winner lies outside the top 6 in 551 of 832 decisions.
- **Against the softmax's actual pick:** held-out gain +0.1522 over 3328 decisions.

| food band | decisions | mean held-out gain |
|---|---|---|
| starving or weak | 531 | +0.0502 |
| under 2 weeks | 1355 | +0.1451 |
| 2-6 weeks | 1426 | +0.2120 |
| 6+ weeks | 16 | +0.2521 |

| season | decisions | mean held-out gain |
|---|---|---|
| spring | 832 | +0.1412 |
| summer | 832 | +0.1599 |
| autumn | 832 | +0.1715 |
| winter | 832 | +0.1640 |

## Population (beside the measure)

Living-weeks 2,399,884 and adult-weeks 1,644,931 in the sampling window; extinct worlds 0.

