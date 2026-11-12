# NB3-A: why do the feeling people starve? (results)

Frozen as `NB3A-frozen`. run_nb3a.py, analyse_nb3a.py (written before data).

**Correction 1** (questions.md, after the data): replays are read if their history matches NB3's exactly; the frozen fingerprint rule failed (`results_frozen_rule.md`).

## Validity

- Read-only check (zero_local.log, All: PASS): **yes**
- All 48 replays present: **yes**
- Replays with NB3's exact history (Correction 1): 48 of 48; differing (reported beside, not read): none
- **Valid.**

Worlds read: c 16, fH 16, f 16.
Code check, 'held food but did not eat' weeks: 998 (expected 0).

## The six patterns (frozen, last 8 weeks)

| pattern | f deaths | f survivors | fH deaths | c deaths | f/c | f/survivors | leads |
|---|---|---|---|---|---|---|---|
| cannot find | 0.002 (n 5657) | 0.000 (n 5649) | 0.001 (n 5039) | 0.000 (n 4737) | 5.02 | inf | no |
| does not try | 0.126 (n 5657) | 0.079 (n 5649) | 0.127 (n 5039) | 0.121 (n 4737) | 1.05 | 1.59 | no |
| not shared | 0.562 (n 5657) | 0.720 (n 5649) | 0.535 (n 5039) | 0.538 (n 4737) | 1.04 | 0.78 | no |
| caregiver short | 0.239 (n 5657) | 0.070 (n 5649) | 0.212 (n 5039) | 0.201 (n 4737) | 1.19 | 3.42 | no |
| no caregiver | 0.001 (n 5657) | 0.000 (n 5649) | 0.001 (n 5039) | 0.000 (n 4737) | inf | inf | no |
| hard times | 0.589 (n 5657) | 0.588 (n 5649) | 0.629 (n 5039) | 0.620 (n 4737) | 0.95 | 1.00 | no |

Overlaps among f's starvation deaths (both patterns):

- cannot find + does not try: 9
- cannot find + not shared: 7
- cannot find + hard times: 9
- does not try + not shared: 481
- does not try + no caregiver: 1
- does not try + hard times: 404
- not shared + caregiver short: 821
- not shared + no caregiver: 3
- not shared + hard times: 1844
- caregiver short + no caregiver: 1
- caregiver short + hard times: 815
- no caregiver + hard times: 5
- none of the six: 702 of 5657

## Each pattern as deaths per 1,000 living-years (paired seed bootstrap)

| pattern | f | fH | c | f/c [95%] | f/fH [95%] |
|---|---|---|---|---|---|
| all starvation | 12.682 | 11.682 | 5.286 | 2.40 [2.17, 2.66] | 1.09 [0.96, 1.23] |
| cannot find | 0.027 | 0.007 | 0.002 | 12.05 [3.29, 34.44] | 3.87 [1.59, 11.80] |
| does not try | 1.598 | 1.484 | 0.637 | 2.51 [2.05, 3.01] | 1.08 [0.88, 1.29] |
| not shared | 7.124 | 6.245 | 2.843 | 2.51 [2.16, 2.86] | 1.14 [0.97, 1.33] |
| caregiver short | 3.029 | 2.481 | 1.060 | 2.86 [2.32, 3.52] | 1.22 [0.97, 1.55] |
| no caregiver | 0.013 | 0.012 | 0.000 | inf [nan, nan] | 1.16 [0.31, 3.49] |
| hard times | 7.467 | 7.349 | 3.276 | 2.28 [1.99, 2.61] | 1.02 [0.90, 1.16] |

## The six patterns (sensitivity, last 24 weeks)

| pattern | f deaths | f survivors | fH deaths | c deaths | f/c | f/survivors | leads |
|---|---|---|---|---|---|---|---|
| cannot find | 0.000 (n 5657) | 0.000 (n 5649) | 0.000 (n 5039) | 0.000 (n 4737) | 0.00 | nan | no |
| does not try | 0.036 (n 5657) | 0.011 (n 5649) | 0.030 (n 5039) | 0.035 (n 4737) | 1.00 | 3.19 | no |
| not shared | 0.829 (n 5657) | 0.879 (n 5649) | 0.831 (n 5039) | 0.810 (n 4737) | 1.02 | 0.94 | no |
| caregiver short | 0.289 (n 5657) | 0.118 (n 5649) | 0.261 (n 5039) | 0.256 (n 4737) | 1.13 | 2.45 | no |
| no caregiver | 0.001 (n 5657) | 0.000 (n 5649) | 0.001 (n 5039) | 0.000 (n 4737) | inf | inf | no |
| hard times | 0.589 (n 5657) | 0.588 (n 5649) | 0.629 (n 5039) | 0.620 (n 4737) | 0.95 | 1.00 | no |

Rule (frozen): a pattern leads if, among f's starvation deaths, its share is at least 25%, at least 1.5 times c's share and at least 1.5 times its share among f's matched survivors.

## The food economy per adult-week (years 100-600; paired seed bootstrap of f/c)

| measure | f | fH | c | f/c [95%] |
|---|---|---|---|---|
| gained:forage | 9.816 | 9.672 | 9.081 | 1.08 [1.06, 1.10] |
| gained:hunt | 0.000 | 0.000 | 0.000 | nan [nan, nan] |
| gained:take | 0.011 | 0.009 | 0.001 | 17.00 [13.18, 21.84] |
| eaten | 8.961 | 8.866 | 8.410 | 1.07 [1.05, 1.08] |
| fed_to_dependents | 0.692 | 0.668 | 0.463 | 1.49 [1.36, 1.62] |
| given:own_child | 0.052 | 0.041 | 0.067 | 0.77 [0.63, 0.98] |
| given:kin | 0.173 | 0.133 | 0.302 | 0.57 [0.46, 0.74] |
| given:other | 0.195 | 0.177 | 0.401 | 0.49 [0.40, 0.60] |
| stored | 0.110 | 0.072 | 0.008 | 14.37 [10.81, 19.12] |
| spoiled | 0.758 | 0.744 | 0.665 | 1.14 [1.11, 1.17] |

Matched survivors found (alive 8 weeks later): c 4736/4737, fH 5032/5039, f 5649/5657.

