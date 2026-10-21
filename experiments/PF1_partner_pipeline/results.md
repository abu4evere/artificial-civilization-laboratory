# PF1 — where partner finding stops: results

Frozen as `PF1-frozen`. run_pf1.py, analyse_pf1.py.

## Validity

- Zero check (logging and observer change nothing against `code_mb1b`): **yes**
- All 96 worlds present: **yes**
- Every replay equals MB1b's saved world (final state hash): **yes** (96 of 96)
- One code fingerprint (`code_pf1`): **yes**

**Valid.**

## Discovery (seeds 5301–5316)

Share of fertile single woman-weeks ending at each step (pooled), with population beside it.

| arm | median alive at the end | single woman-weeks | S1 no match alive | S2 none in sight | S3 none in reach | S4 disliked | S5 not tried | S6 refused | bottleneck |
|---|---|---|---|---|---|---|---|---|---|
| p4 | 48 | 559090 | 3.4% | 30.3% | 18.8% | 0.1% | 47.1% | 0.4% | S5 not tried |
| b8 | 60 | 614347 | 2.2% | 31.5% | 16.5% | 0.1% | 49.3% | 0.4% | S5 not tried |
| b16 | 50 | 627974 | 1.2% | 30.2% | 17.9% | 0.1% | 50.1% | 0.5% | S5 not tried |

Shift, B16 minus P4 (percentage points; described, no test): S1 no match alive -2.2, S2 none in sight -0.0, S3 none in reach -0.9, S4 disliked -0.0, S5 not tried +3.0, S6 refused +0.2

By her age (share of that age group's single woman-weeks at each step):

| arm | age | S1 no match alive | S2 none in sight | S3 none in reach | S4 disliked | S5 not tried | S6 refused |
|---|---|---|---|---|---|---|---|
| p4 | 16–26 | 2.7% | 26.7% | 18.9% | 0.1% | 51.1% | 0.4% |
| p4 | 26–36 | 2.3% | 33.3% | 18.4% | 0.1% | 45.4% | 0.4% |
| p4 | 36–45 | 8.1% | 40.0% | 18.8% | 0.2% | 32.8% | 0.1% |
| b8 | 16–26 | 2.5% | 27.0% | 16.2% | 0.1% | 53.7% | 0.5% |
| b8 | 26–36 | 1.3% | 34.8% | 17.0% | 0.2% | 46.3% | 0.5% |
| b8 | 36–45 | 2.3% | 45.4% | 16.8% | 0.2% | 35.1% | 0.2% |
| b16 | 16–26 | 1.4% | 25.9% | 18.0% | 0.1% | 53.9% | 0.7% |
| b16 | 26–36 | 0.3% | 33.8% | 17.2% | 0.1% | 48.2% | 0.5% |
| b16 | 36–45 | 1.6% | 41.0% | 18.6% | 0.1% | 38.5% | 0.2% |

Courting attempts between people not already partners (all, both sexes): 
- p4: 3901 attempts; paired 1674, refused 2227, one already taken 0; single adult man-weeks per person-week 0.164
- b8: 4718 attempts; paired 1777, refused 2941, one already taken 0; single adult man-weeks per person-week 0.187
- b16: 5357 attempts; paired 1590, refused 3767, one already taken 0; single adult man-weeks per person-week 0.179

## Holdout (seeds 5317–5332)

Share of fertile single woman-weeks ending at each step (pooled), with population beside it.

| arm | median alive at the end | single woman-weeks | S1 no match alive | S2 none in sight | S3 none in reach | S4 disliked | S5 not tried | S6 refused | bottleneck |
|---|---|---|---|---|---|---|---|---|---|
| p4 | 38 | 566372 | 2.0% | 35.2% | 16.7% | 0.0% | 45.7% | 0.3% | S5 not tried |
| b8 | 44 | 568061 | 1.5% | 31.8% | 17.7% | 0.1% | 48.4% | 0.4% | S5 not tried |
| b16 | 61 | 686487 | 0.8% | 34.9% | 16.9% | 0.2% | 46.7% | 0.5% | S5 not tried |

Shift, B16 minus P4 (percentage points; described, no test): S1 no match alive -1.2, S2 none in sight -0.3, S3 none in reach +0.2, S4 disliked +0.1, S5 not tried +1.0, S6 refused +0.2

By her age (share of that age group's single woman-weeks at each step):

| arm | age | S1 no match alive | S2 none in sight | S3 none in reach | S4 disliked | S5 not tried | S6 refused |
|---|---|---|---|---|---|---|---|
| p4 | 16–26 | 1.6% | 31.4% | 16.9% | 0.0% | 49.7% | 0.4% |
| p4 | 26–36 | 1.1% | 38.9% | 16.3% | 0.1% | 43.4% | 0.3% |
| p4 | 36–45 | 5.0% | 43.3% | 16.7% | 0.1% | 34.9% | 0.2% |
| b8 | 16–26 | 1.5% | 27.7% | 18.3% | 0.1% | 51.9% | 0.5% |
| b8 | 26–36 | 1.1% | 35.0% | 16.6% | 0.0% | 46.8% | 0.4% |
| b8 | 36–45 | 2.6% | 44.2% | 17.2% | 0.0% | 35.8% | 0.2% |
| b16 | 16–26 | 0.7% | 30.9% | 17.5% | 0.2% | 50.1% | 0.6% |
| b16 | 26–36 | 0.4% | 38.4% | 16.0% | 0.2% | 44.6% | 0.5% |
| b16 | 36–45 | 2.2% | 46.0% | 15.8% | 0.1% | 35.7% | 0.2% |

Courting attempts between people not already partners (all, both sexes): 
- p4: 3574 attempts; paired 1573, refused 2001, one already taken 0; single adult man-weeks per person-week 0.182
- b8: 4198 attempts; paired 1611, refused 2587, one already taken 0; single adult man-weeks per person-week 0.182
- b16: 5530 attempts; paired 1751, refused 3779, one already taken 0; single adult man-weeks per person-week 0.177

## The frozen reading

| arm | bottleneck, discovery | bottleneck, holdout | reading |
|---|---|---|---|
| p4 | S5 not tried | S5 not tried | **S5 not tried** (stands) |
| b8 | S5 not tried | S5 not tried | **S5 not tried** (stands) |
| b16 | S5 not tried | S5 not tried | **S5 not tried** (stands) |
