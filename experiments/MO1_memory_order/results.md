# MO1 — The memory order. Results

Frozen as `MO1-frozen` (operational note 1). run_mo1.py, analyse_mo1.py (written before data).

## Validity

- Zero checks: **yes**
- All worlds present (96 of 96): **yes**
- One fingerprint (`code_mo1`): **yes**
- Every predicted deletion matches the code's (mismatches 0): **yes**

**Valid.**

Paired seeds: 32. Worlds extinct by year 200: c 1, o 0, s 1.

## The measures (pooled over paired worlds; 95% paired world bootstrap, 10,000 replicates)

| measure | c | o | s | o − c [95%] | s − c [95%] (sham yardstick) |
|---|---|---|---|---|---|
| M: new recipe survives a learning-caused overflow | 0.2962 | 0.8365 | 0.3032 | +0.5403 [+0.4937, +0.6012] | +0.007006 [-0.01486, +0.02843] |
| P1: taken recipes still held 52 weeks later | 0.6719 | 0.9149 | 0.679 | +0.243 [+0.2195, +0.2727] | +0.007137 [-0.01477, +0.02743] |
|   P1, taught | 0.6719 | 0.9148 | 0.6791 | +0.243 [+0.2194, +0.2726] | +0.007206 [-0.01425, +0.02775] |
|   P1, copied by watching | 0.7436 | 1 | 0.56 | +0.2564 [+0.125, +0.383] | -0.1836 [-0.3833, -0.01087] |
| P2: useful recipes held per adult (years 50-200) | 9.335 | 9.142 | 9.446 | -0.1929 [-0.3154, -0.05861] | +0.1113 [-0.09019, +0.3009] |
| P3: taken recipes found bad within 52 weeks | 0 | 0 | 0 | +0 [+0, +0] | +0 [+0, +0] |
| taken recipes made within 52 weeks | 0.004787 | 0.005164 | 0.004252 | +0.0003767 [-0.0003901, +0.001268] | -0.000535 [-0.001609, +0.0004149] |
| value of the recipe deleted instead (when the new one survives) | 0.004743 | 0.01697 | 0.004968 | +0.01222 [+0.009641, +0.01453] | +0.0002252 [-0.0008178, +0.001367] |
| deleted instead: a useful kind | 0.9687 | 0.9185 | 0.9729 | -0.05018 [-0.06694, -0.03193] | +0.004187 [-0.008925, +0.01634] |
| deleted instead: made by its holder in the past 52 weeks | 0.001144 | 0.002717 | 0.0009227 | +0.001573 [+0.0007096, +0.002395] | -0.0002218 [-0.0009086, +0.0005334] |
| evicted recipes relearned, per learned recipe | 0.1278 | 0.1142 | 0.1274 | -0.0136 [-0.02759, -0.00123] | -0.0004048 [-0.009878, +0.01004] |
| making events per adult-year | 0.1275 | 0.1298 | 0.1321 | +0.002295 [-0.005555, +0.009599] | +0.004536 [-0.005728, +0.01545] |
| mean living population, years 150-200 | 116.7 | 110.7 | 110.1 | -5.958 [-20.15, +8.52] | -6.643 [-26.18, +12.42] |
| world-born kinds held by anyone alive at year 200 (mean per world) | 98.62 | 100.1 | 91.28 | +1.5 [-11.09, +13.91] | -7.344 [-23.22, +9] |

## The frozen decision rule

- **M (manipulation):** o 0.837 ≥ 0.90 and c 0.296 ≤ 0.40: **FAILS**
- **P1 (retention):** o − c +0.2430 [+0.2195, +0.2727], lower bound above 0: **supports**
- **P2 (knowledge kept):** o − c -0.1929 [-0.3154, -0.0586], lower bound above −5% of c (-0.4667): **no harm**
- **P3 (reliability):** o − c +0.0000 [+0.0000, +0.0000], upper bound below +0.02: **no harm**

**The change is not supported by the frozen rule.** Adoption as nature v8 is left to the creator.

