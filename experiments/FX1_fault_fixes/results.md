# FX1: Fixing three faults in nature v11 (results)

Frozen as `FX1-frozen`. run_fx1.py, analyse_fx1.py (written before data).

## Validity

- Zero checks (All: PASS, same `code_fx1` fingerprint): **yes**
- All worlds present (160): **yes**
- One fingerprint, `code_fx1`'s: **yes**

**Valid.**

## Decision (frozen): a check for harm only, f against v11

| contrast | living-weeks ratio [95%] | extinct worlds (arm, v11) |
|---|---|---|
| f / v11 | 1.0003 [0.8926, 1.1301] | 1, 1 |
| f1 / v11 | 1.1040 [0.9840, 1.2631] | 0, 1 |
| f23 / v11 | 1.0737 [0.9843, 1.1855] | 0, 1 |
| sham / v11 | 1.0307 [0.9155, 1.1636] | 1, 1 |

Guards (f against v11): population if the ratio is below 0.90 with its upper bound below 1; extinctions if f has 3 or more extinct worlds beyond v11's.

**Reading: no harm.** No guard raised.

## Flags for investigation (f against v11; frozen rule: ratio outside [0.8, 1.25] with its 95% interval wholly outside 1)

| measure | f / v11 [95%] | sham / v11 [95%] | flag |
|---|---|---|---|
| makes per adult-year | 1.0547 [0.9749, 1.1406] | 1.0031 [0.9195, 1.0946] | no |
| kinds invented per adult-year | 1.0071 [0.9374, 1.0808] | 0.9817 [0.8931, 1.0801] | no |
| made things held per adult | 1.0676 [0.9414, 1.2213] | 1.0918 [0.9755, 1.2144] | no |
| things on the ground at year 200 | 1.1126 [0.8335, 1.4878] | 0.8818 [0.6060, 1.3031] | no |
| adult-weeks | 1.0079 [0.9058, 1.1307] | 1.0349 [0.9250, 1.1645] | no |

**Flags: none.**

## Described (not decisive)

| arm | adult decisions with a make option | rules differ | offer is the newest recipe | v11 rule's offer is the newest | fixed rule's offer is the newest | heir's things deleted | heir's things dropped | from a body, dropped | makes per adult-year | kinds per 100 adult-years | lineage R (kinds, remade) | made things per adult | on the ground at year 200 (mean per world) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| v11 | 10,236,079 | 0.0859 | 0.0899 | 0.0899 | 0.1057 | 63 | 0 | 531 | 0.0708 | 1.121 | 0.0003 (3,378, 1) | 0.893 | 122.9 |
| f | 10,347,123 | 0.0807 | 0.1074 | 0.0914 | 0.1074 | 0 | 73 | 648 | 0.0747 | 1.129 | 0.0003 (3,429, 1) | 0.953 | 136.8 |
| f1 | 11,230,798 | 0.0863 | 0.1052 | 0.0893 | 0.1052 | 80 | 0 | 772 | 0.0721 | 1.023 | 0.0000 (3,413, 0) | 0.932 | 123.8 |
| f23 | 10,884,101 | 0.0888 | 0.0955 | 0.0955 | 0.1128 | 0 | 109 | 932 | 0.0664 | 1.101 | 0.0000 (3,558, 0) | 0.939 | 113.3 |
| sham | 10,427,291 | 0.0862 | 0.0935 | 0.0935 | 0.1095 | 70 | 0 | 777 | 0.0711 | 1.100 | 0.0003 (3,432, 1) | 0.975 | 108.4 |

