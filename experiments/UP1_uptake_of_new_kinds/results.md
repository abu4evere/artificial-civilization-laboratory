# UP1 — Why is a new kind never made again? Results

Frozen as `UP1-frozen`. run_up1.py, analyse_up1.py (written before data).

## Validity

- Zero checks (All: PASS, same `code_v11` fingerprint): **yes**
- All worlds present (32): **yes**
- One fingerprint, `code_v11`'s: **yes**
- The reproduced make option equals the code's at every decision (mismatches 0): **yes**

**Valid.**

## Primary (frozen): where new kinds stop (shares of person x kind x decisions, years 100-200)

New kinds: 2,540; person x kind x decisions: 4,977,150 (old kinds: 166,823,584).

| step | new kinds: share [95%] | old kinds: share | new - old [95%] |
|---|---|---|---|
| 1 holding | 0.0008 [0.0006, 0.0010] | 0.0503 | -0.0495 [-0.0565, -0.0431] |
| 2 value floor | 0.1315 [0.1162, 0.1469] | 0.4177 | -0.2863 [-0.3095, -0.2630] |
| 3 cannot make | 0.8672 [0.8518, 0.8825] | 0.4111 | +0.4561 [+0.4375, +0.4748] |
| 4a running-best skip | 0.0001 [0.0001, 0.0002] | 0.0404 | -0.0402 [-0.0424, -0.0379] |
| 4b beaten | 0.0001 [0.0000, 0.0003] | 0.0164 | -0.0163 [-0.0172, -0.0153] |
| 5 eligible, not chosen | 0.0003 [0.0002, 0.0004] | 0.0640 | -0.0637 [-0.0650, -0.0624] |
| made | 0.0000 [0.0000, 0.0000] | 0.0001 | -0.0001 [-0.0002, -0.0001] |

Rule: "mainly blocked at step k" if one step's share has its lower bound above 0.50; otherwise "mixed bottlenecks".

**Reading: mainly blocked at step 3 cannot make.**

Secondary (Gemini): the main difference from old kinds: **3 cannot make**.

## Secondary (described, not decisive)

- new kinds, simple: 1 0.005, 2 0.975, 3 0.020, 4a 0.000, 4b 0.000, 5 0.000, made 0.000 (26,209 decisions)
- old kinds, simple: 1 0.063, 2 0.460, 3 0.335, 4a 0.047, 4b 0.019, 5 0.077, made 0.000 (130,326,718 decisions)
- new kinds, nested: 1 0.001, 2 0.127, 3 0.872, 4a 0.000, 4b 0.000, 5 0.000, made 0.000 (4,950,941 decisions)
- old kinds, nested: 1 0.007, 2 0.267, 3 0.684, 4a 0.017, 4b 0.006, 5 0.019, made 0.000 (36,496,866 decisions)
- new kinds, first five years after invention: 1 0.149, 2 0.151, 3 0.698, 4a 0.001, 4b 0.000, 5 0.001, made 0.000 (21,008)
- new kinds, after five years: 1 0.000, 2 0.131, 3 0.868, 4a 0.000, 4b 0.000, 5 0.000, made 0.000 (4,956,142)
- kind-weighted (each new kind once): 1 0.002, 2 0.134, 3 0.864, 4a 0.000, 4b 0.000, 5 0.000, made 0.000 (2,862 kinds)
- new kinds ever eligible (step 5 or made): 34 of 2,862; ever made: 4
- at step 4, the winning make option was: old kind 1,213
- new kinds as the make option: 1,313 decisions; mean make probability 0.004
- old kinds as the make option: 10,695,546 decisions; mean make probability 0.002

