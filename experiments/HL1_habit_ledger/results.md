# HL1 — Where do the habits come from? Results

Frozen as `HL1-frozen`. run_hl1.py, analyse_hl1.py (written before data).

## Validity

- Zero checks: **yes**
- All worlds present (32 of 32): **yes**
- One fingerprint (`code_v7`): **yes**
- The ledger closes, every TD update replays exactly, the Q1 split adds up (mismatches 0): **yes**

**Valid.**

## Q1 — Which route carries CO1's habit rise (primary)

Adults, weeks in which make was offered; early = years 0-10, late = years 100-200; worlds alive at year 100 (32); 24 matched states (hunger × tool × food), late weighted to the early offered weeks.

- The habit part of the competing pull (Σ s_a·h_a): 0.055 → 0.632; **Δ = +0.577 [0.569, 0.585]**.

| route | early | late | Δ | share of the rise |
|---|---|---|---|---|
| td | 0.0496 | 0.3359 | +0.2863 [0.277, 0.296] | 0.50 |
| talk | 0.0048 | 0.2440 | +0.2392 [0.225, 0.254] | 0.41 |
| carer | 0.0000 | 0.0484 | +0.0484 [0.0454, 0.0511] | 0.08 |
| birth | 0.0000 | 0.0000 | +0.0000 [1.25e-08, 2.63e-08] | 0.00 |
| paid | 0.0006 | 0.0036 | +0.0030 [0.00275, 0.00329] | 0.01 |

(Exactness check: Δ minus the routes = 2.22e-16.)

**The route carrying the largest share of the rise: td.**

Making's own habit term (0.6 × its habit value), by route: td 0.00109 → 0.00231, talk 0.00007 → 0.01913, carer 0.00000 → 0.00622, birth 0.00000 → 0.00000, paid 0.00000 → 0.00000.

## Q2 — Raw flows: total change in habit values by route (summed over situations and people)

| bin | forage: td / talk / carer / paid | give: td / talk / carer / paid | talk: td / talk / carer / paid | gather: td / talk / carer / paid | put: td / talk / carer / paid | copying events | carer events |
|---|---|---|---|---|---|---|---|
| 0-5 | 2685 / 34 / 819 / 0 | 443 / 23 / 123 / 174 | 1223 / 2 / -81 / 0 | 73 / 0 / 7 / 0 | 25 / 0 / 4 / 0 | 19201 | 41452 |
| 5-10 | 1929 / 40 / 1691 / 0 | 616 / 100 / 325 / 207 | 2046 / 14 / -652 / 0 | 236 / -2 / -48 / 0 | 61 / 2 / 27 / 0 | 39620 | 94857 |
| 10-20 | 4061 / 106 / 2213 / 0 | 1735 / 302 / 723 / 1030 | 5062 / 78 / -1698 / 0 | 700 / -4 / -0 / 0 | 283 / 9 / 123 / 0 | 137625 | 199144 |
| 20-50 | 11992 / 471 / 11672 / 0 | 2381 / 597 / 6751 / 5369 | 16732 / 107 / -3276 / 0 | 5219 / 9 / 1488 / 0 | 2826 / 56 / 1509 / 0 | 401649 | 450112 |
| 50-100 | 13814 / 1166 / 30664 / 0 | -1645 / 850 / 19928 / 12474 | 33973 / -57 / -4029 / 0 | 12308 / 124 / 7216 / 0 | 7077 / 129 / 6303 / 0 | 694856 | 794626 |
| 100-200 | 8355 / 3369 / 66641 / 0 | -6103 / 2530 / 51552 / 20383 | 52907 / 363 / 6637 / 0 | 15517 / 959 / 23589 / 0 | 8985 / 709 / 18391 / 0 | 1233909 | 1427210 |

## Q3 — Rich-get-richer (adults)

| bin | action | chosen per adult-week | TD updates per adult-week | mean reward r | mean future | mean TD target | mean habit value |
|---|---|---|---|---|---|---|---|
| 0-5 | forage | 0.5015 | 0.5012 | 0.208 | 0.056 | 0.253 | 0.0190 |
| 0-5 | give | 0.0527 | 0.0527 | 0.265 | 0.077 | 0.327 | 0.0035 |
| 0-5 | talk | 0.1341 | 0.1341 | 0.168 | 0.070 | 0.224 | 0.0057 |
| 0-5 | gather | 0.0269 | 0.0269 | 0.022 | 0.068 | 0.076 | 0.0003 |
| 0-5 | make | 0.0028 | 0.0028 | 0.097 | 0.080 | 0.161 | 0.0001 |
| 5-10 | forage | 0.5135 | 0.5131 | 0.187 | 0.147 | 0.305 | 0.0509 |
| 5-10 | give | 0.0734 | 0.0734 | 0.293 | 0.186 | 0.442 | 0.0154 |
| 5-10 | talk | 0.1165 | 0.1165 | 0.169 | 0.178 | 0.312 | 0.0166 |
| 5-10 | gather | 0.0370 | 0.0369 | 0.018 | 0.154 | 0.141 | 0.0017 |
| 5-10 | make | 0.0079 | 0.0079 | 0.098 | 0.146 | 0.215 | 0.0005 |
| 10-20 | forage | 0.4575 | 0.4569 | 0.173 | 0.263 | 0.383 | 0.0886 |
| 10-20 | give | 0.0790 | 0.0788 | 0.302 | 0.319 | 0.557 | 0.0375 |
| 10-20 | talk | 0.1373 | 0.1370 | 0.172 | 0.305 | 0.416 | 0.0368 |
| 10-20 | gather | 0.0571 | 0.0570 | 0.017 | 0.248 | 0.216 | 0.0059 |
| 10-20 | make | 0.0102 | 0.0102 | 0.098 | 0.240 | 0.290 | 0.0019 |
| 20-50 | forage | 0.4297 | 0.4291 | 0.195 | 0.595 | 0.671 | 0.1834 |
| 20-50 | give | 0.0990 | 0.0989 | 0.295 | 0.631 | 0.800 | 0.1042 |
| 20-50 | talk | 0.1336 | 0.1334 | 0.170 | 0.638 | 0.680 | 0.0940 |
| 20-50 | gather | 0.1036 | 0.1035 | 0.016 | 0.527 | 0.438 | 0.0311 |
| 20-50 | make | 0.0053 | 0.0052 | 0.098 | 0.481 | 0.483 | 0.0056 |
| 50-100 | forage | 0.4214 | 0.4209 | 0.198 | 1.007 | 1.003 | 0.3279 |
| 50-100 | give | 0.1087 | 0.1085 | 0.274 | 1.060 | 1.122 | 0.2069 |
| 50-100 | talk | 0.1340 | 0.1338 | 0.170 | 1.073 | 1.028 | 0.1924 |
| 50-100 | gather | 0.1464 | 0.1463 | 0.017 | 0.883 | 0.723 | 0.0979 |
| 50-100 | make | 0.0018 | 0.0018 | 0.097 | 0.807 | 0.742 | 0.0100 |
| 100-200 | forage | 0.4142 | 0.4136 | 0.203 | 1.259 | 1.209 | 0.4384 |
| 100-200 | give | 0.1003 | 0.1002 | 0.257 | 1.306 | 1.301 | 0.3289 |
| 100-200 | talk | 0.1363 | 0.1361 | 0.172 | 1.311 | 1.220 | 0.3015 |
| 100-200 | gather | 0.1770 | 0.1768 | 0.016 | 1.162 | 0.945 | 0.1837 |
| 100-200 | make | 0.0007 | 0.0007 | 0.097 | 1.043 | 0.931 | 0.0145 |

Rank association, across worlds × 8 families, of how often an action was chosen in years 0-20 with the growth of its mean habit value to years 100-200: **0.83** (256 pairs; described).

**The negative test (making, all bins):** change in its habit by own TD +1609.34 (59864 updates); by copying in talk +284.54; by carer +3509.74. Forage: TD +42836.08 (15440650 updates); talk +5185.95; carer +113699.60.

## Q4 — Social amplification (copying in talk)

Copying events: 2526860; for respect 1295201, for seeming happier 1231659.

| action | mean model − learner habit gap per copying event (per situation) | total change copied |
|---|---|---|
| forage | +0.0025 | +5186.0 |
| give | +0.0019 | +4400.9 |
| talk | +0.0007 | +507.1 |
| gather | +0.0006 | +1085.8 |
| put | +0.0005 | +905.2 |
| join | +0.0012 | +3042.0 |
| rest | -0.0006 | -2107.3 |
| make | +0.0001 | +284.5 |

