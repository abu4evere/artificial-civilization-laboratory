# PT1 — Does parts-first teaching work? Results

Frozen as `PT1-frozen` (operational note 1). run_pt1.py, analyse_pt1.py (written before data).

## Validity

- Zero checks: **yes**
- All worlds present (32 of 32): **yes**
- One fingerprint (`code_v7`): **yes**
- Gate outcomes, part selection and eviction replay match the code (mismatches 0): **yes**

**Valid.**

Mean population (living, sampled yearly): years 0-50: 104.5; years 50-100: 111.5; years 100-200: 107.7 (32 worlds).

## Q1 — Is the parts-first route reachable? (primary; G4 failures of world-born useful kinds)

| era | G4 failures | (a) none: teacher knows no made part | (b) wrong: part shown already held | (c) deep: part shown needs a missing part | (d) reachable |
|---|---|---|---|---|---|
| all | 95580 | 0.098 | 0.044 | 0.579 | 0.278 |
| 0-50 | 31911 | 0.107 | 0.040 | 0.627 | 0.227 |
| 50-100 | 30853 | 0.124 | 0.042 | 0.578 | 0.257 |
| 100-200 | 32816 | 0.064 | 0.052 | 0.535 | 0.350 |

World bootstrap 95% (all eras): none [0.0841, 0.11]; wrong [0.0389, 0.0493]; deep [0.559, 0.604]; reach [0.266, 0.29].

**Share of G4 failures that parts-first can reach at all: 0.278 [0.266, 0.29].**

### The completion funnel (chains: one learner and one whole kind, ever reachable; followed until death or the run's end)

| step | chains reaching it | conditional on the step before [95%] | stopped here by death | median weeks from the first G4 failure |
|---|---|---|---|---|
| reachable G4 failure (start) | 19472 | - | - | - |
| part shown and taken | 6092 | 0.313 [0.302, 0.325] | 12298 | 0 |
| part kept (not pushed out) | 3900 | 0.640 [0.62, 0.661] | 2129 | 0 |
| part made | 436 | 0.112 [0.0985, 0.125] | 3021 | 530 |
| every missing part held | 346 | 0.794 [0.755, 0.833] | 85 | 0 |
| whole taken again | 215 | 0.621 [0.559, 0.678] | 124 | 120 |
| whole made | 12 | 0.056 [0.0288, 0.0881] | 191 | 552 |

**The step with the largest loss among reachable chains: whole made (conditional 0.056).**

All world-born useful chains (any class): 59990; whole later held by any route 0.021; whole made 0.001.

## Q2 — The selection rule (world-born useful)

| era | G4 failures | wrong-part rate | teacher knew a missing part but showed another | teacher knows any missing part | mean p, whole lesson | reachable: part lesson G1 / G2 / G3 / G4 / taken | reachable: mean p, part lesson | reachable: part kept / taken |
|---|---|---|---|---|---|---|---|---|
| all | 95580 | 0.044 | 0.025 | 0.883 | 0.290 | 0.014 / 0.000 / 0.734 / 0.000 / 0.252 | 0.251 | 0.605 |
| 0-50 | 31911 | 0.040 | 0.018 | 0.872 | 0.278 | 0.009 / 0.000 / 0.723 / 0.000 / 0.268 | 0.262 | 0.529 |
| 50-100 | 30853 | 0.042 | 0.021 | 0.855 | 0.309 | 0.015 / 0.000 / 0.736 / 0.000 / 0.249 | 0.254 | 0.543 |
| 100-200 | 32816 | 0.052 | 0.035 | 0.919 | 0.284 | 0.016 / 0.000 / 0.739 / 0.000 / 0.245 | 0.243 | 0.702 |

## Q3 — Memory: lesson-added recipes that overflow the 12-recipe memory

| lessons | kinds | overflows | evicted is the new lesson | mean evicted value | tied at the lowest value | evicted is composite / composite share held | replay (lesson value set first): new lesson survives | of evicted new lessons, would survive | mean lesson value / mean value evicted in replay | relearned | mean weeks to relearn |
|---|---|---|---|---|---|---|---|---|---|---|---|
| whole | all kinds | 41808 | 0.714 | 0.0022 | 0.652 | 0.728 / 0.681 | 0.957 | 0.940 | 0.070 / 0.0098 | 0.145 | 283 |
| whole | world-born useful | 9865 | 0.784 | 0.0021 | 0.623 | 0.819 / 0.692 | 0.957 | 0.945 | 0.071 / 0.0109 | 0.144 | 235 |
| part | all kinds | 4906 | 0.737 | 0.0018 | 0.685 | 0.842 / 0.691 | 0.975 | 0.965 | 0.082 / 0.0086 | 0.164 | 296 |
| part | world-born useful | 1127 | 0.808 | 0.0016 | 0.675 | 0.900 / 0.705 | 0.977 | 0.971 | 0.082 / 0.0090 | 0.131 | 251 |

Whole lessons, all kinds, world bootstrap 95%: evicted is the new lesson [0.691, 0.732]; survives in the replay [0.945, 0.971].

## Q4 — Depth (G4 failures of world-born useful kinds)

| era | G4 failures | levels needed: 1 | 2 | 3 or more | mean missing parts (direct) | mean missing parts (all levels) | needs two or more levels |
|---|---|---|---|---|---|---|---|
| all | 95580 | 0.319 | 0.323 | 0.358 | 1.19 | 2.70 | 0.681 |
| 0-50 | 31911 | 0.252 | 0.293 | 0.455 | 1.20 | 3.04 | 0.748 |
| 50-100 | 30853 | 0.300 | 0.331 | 0.368 | 1.21 | 2.76 | 0.700 |
| 100-200 | 32816 | 0.403 | 0.343 | 0.254 | 1.16 | 2.32 | 0.597 |

