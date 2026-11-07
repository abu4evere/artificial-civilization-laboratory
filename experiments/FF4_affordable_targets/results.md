# FF4: a whole action dropped because one target is too far (results)

Frozen as `FF4-frozen`. run_ff4.py, analyse_ff4.py (written before data).

## Validity

- Zero checks (All: PASS, `code_ff4` fingerprint): **yes**
- All worlds present (96): **yes**
- One fingerprint, `code_ff4`'s: **yes**
- Hook check in every world (forage, hunt and gather offered exactly when the log predicts; 118,827,227 person-weeks aged 6+): mismatches 0: **yes**

**Valid.**

## Reading (frozen)

- **f: no harm.** Guards raised: none.
- Sham: guards raised: none.

Rule: "no harm" if no guard is raised (f is then adopted as nature v16 by the safe path; a fault fix has no confirmatory run); otherwise "harm: investigate".

## Guards (f against v15; the sham against v15 beside it)

| guard | f | v15 | f vs v15 [95%] | sham vs v15 [95%] |
|---|---|---|---|---|
| starvation deaths per 1,000 living-years (ratio) | 4.5931 | 4.6806 | 0.9813 [0.8924, 1.0753] | 0.9615 [0.8474, 1.0845] |
| killing deaths per 1,000 living-years (difference) | 0.0045 | 0.0043 | +0.0002 [-0.0087, +0.0086] | +0.0022 [-0.0070, +0.0114] |
| adult health, mean (difference) | 93.3733 | 92.8876 | +0.4857 [-0.0985, +1.0449] | +0.2428 [-0.4133, +0.9094] |
| living-weeks (ratio) | 23,152,325.0000 | 23,974,691.0000 | 0.9657 [0.8779, 1.0636] | 0.9938 [0.8967, 1.1062] |
| extinct worlds (extra) | 0.0000 | 0.0000 | +0.0000 [+nan, +nan] | +1.0000 [+nan, +nan] |
| child deaths per 1,000 child-years (ratio) | 9.8027 | 8.8754 | 1.1045 [0.9417, 1.2556] | 0.9754 [0.8579, 1.1073] |
| child starvation deaths per 1,000 child-years (ratio) | 5.8421 | 5.2871 | 1.1050 [0.9051, 1.3123] | 0.9712 [0.8096, 1.1587] |
| food gifts to kin's children per 1,000 adult-weeks (ratio) | 4.6761 | 4.7230 | 0.9901 [0.9241, 1.0676] | 1.0313 [0.9328, 1.1409] |

## Described (not decisive; flagged if f / v15 is outside [0.8, 1.25] with its interval wholly outside 1)

| measure | v15 | f | sham | f / v15 [95%] | sham / v15 [95%] | |
|---|---|---|---|---|---|---|
| EG1's P: starving weeks blocked by energy alone | 0.0635 | 0.0570 | 0.0648 | 0.8980 [0.8318, 0.9666] | 1.0204 [0.9299, 1.1159] |  |
| starving weeks: food offered and chosen | 0.8763 | 0.8802 | 0.8774 | 1.0045 [0.9968, 1.0131] | 1.0013 [0.9911, 1.0122] |  |
| starving weeks: offered, not chosen | 0.0602 | 0.0627 | 0.0578 | 1.0415 [0.9761, 1.1093] | 0.9604 [0.8833, 1.0410] |  |
| starving weeks: no food feasible | 0.0001 | 0.0001 | 0.0000 | 1.4130 [0.8745, 2.3327] | 0.5041 [0.3030, 0.7917] |  |
| non-starving weeks blocked by energy alone | 0.0069 | 0.0007 | 0.0071 | 0.0977 [0.0914, 0.1037] | 1.0272 [0.9425, 1.1126] | FLAG |
| P, women 30-49 | 0.1188 | 0.1209 | 0.1218 | 1.0183 [0.9700, 1.0679] | 1.0258 [0.9747, 1.0808] |  |
| P, men 30-49 | 0.0553 | 0.0444 | 0.0550 | 0.8019 [0.7232, 0.8921] | 0.9939 [0.8705, 1.1285] |  |
| starvation deaths at 6+ per 1,000 living-years at 6+ | 3.9790 | 3.7453 | 3.7930 | 0.9413 [0.8693, 1.0230] | 0.9533 [0.8407, 1.0768] |  |
| starvation deaths at 6+ with a blocked starving week in their last 4 decisions (share) | 0.3847 | 0.3320 | 0.3983 | 0.8630 [0.7850, 0.9483] | 1.0354 [0.9094, 1.1808] |  |
| grown weeks: forage (share) | 0.3937 | 0.3943 | 0.3945 | 1.0016 [0.9933, 1.0101] | 1.0019 [0.9913, 1.0122] |  |
| grown weeks: hunt (share) | 0.0001 | 0.0001 | 0.0001 | 0.9257 [0.8186, 1.0499] | 1.0641 [0.9233, 1.2270] |  |
| grown weeks: gather (share) | 0.2467 | 0.2500 | 0.2431 | 1.0133 [0.9678, 1.0726] | 0.9851 [0.9303, 1.0591] |  |
| grown weeks: rest (share) | 0.0086 | 0.0081 | 0.0084 | 0.9452 [0.8664, 1.0278] | 0.9744 [0.8891, 1.0581] |  |
| grown weeks: make (share) | 0.0014 | 0.0013 | 0.0013 | 0.9796 [0.9163, 1.0478] | 0.9393 [0.8472, 1.0407] |  |
| grown weeks: talk (share) | 0.0916 | 0.0917 | 0.0949 | 1.0021 [0.9479, 1.0609] | 1.0371 [0.9608, 1.1198] |  |

Flagged: non-starving weeks blocked by energy alone. A flag asks for a read-only explanation before adoption; it is not a stop.

## The fix at work (weeks where the best target was unaffordable but another was affordable; counted years)

| arm | forage | of them starving | hunt | gather | logged person-weeks aged 6+ |
|---|---|---|---|---|---|
| v15 | 161,407 | 17,934 | 1,765 | 91,635 | 21,368,240 |
| f (the fix) | 194,775 | 16,812 | 1,471 | 106,546 | 20,618,452 |
| sham | 163,822 | 17,734 | 2,029 | 99,263 | 21,167,712 |

In v15 and the sham these are the weeks the fix would have acted in; in f, the weeks it did.

## EG1's split by age band and sex, starving weeks (share blocked by energy alone)

| ages | v15 women | v15 men | f women | f men |
|---|---|---|---|---|
| 6-11 | 0.003 (947) | 0.005 (964) | 0.012 (832) | 0.015 (853) |
| 12-15 | 0.048 (23,833) | 0.051 (24,362) | 0.038 (21,621) | 0.038 (22,193) |
| 16-29 | 0.077 (109,432) | 0.055 (98,186) | 0.071 (100,465) | 0.044 (92,108) |
| 30-49 | 0.119 (115,809) | 0.055 (120,384) | 0.121 (108,718) | 0.044 (111,793) |
| 50+ | 0.022 (53,235) | 0.025 (80,387) | 0.018 (45,946) | 0.019 (79,172) |

