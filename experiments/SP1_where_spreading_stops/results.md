# SP1 results (written by analyse_sp1.py; numbers from the raw output files)

Worlds: 32 (expected 32); extinct: 1; fingerprints: ['3d46cd2c1cd2c514d37ec73072c5097854d26270e6ab6fd3da6ab7606b4eb89f']
Run checks pooled: {'taken': 58788, 'taken_mismatch': 0, 'top_lessons': 865204, 'offer_miss': 0}

## The funnel (invented kinds, born in years 100-190; each kind counted once per stage)

- A (born): 3597
- B (offered at least once): 1245
- C (shown at least once): 1196
- Dt (learned by a non-inventor through a lesson): 74
- Dany (learned by a non-inventor by any social route): 74
- Dcopied (learned by watching): 0
- E (a learner had the parts in hand in some week): 8
- F (made by a non-inventor who learned it): 1
- Fany (made by any non-inventor (any route, incl. own)): 6
- copy-error kinds (reported apart): 349

## Primary: conditional pass rate at each step (pooled; world bootstrap 95%, 10,000 draws)

- B|A: 0.3461 [0.3299, 0.3625] (1245 of 3597)
- C|B: 0.9606 [0.9502, 0.9708] (1196 of 1245)
- D-taught|C: 0.0619 [0.0452, 0.0805] (74 of 1196)
- E|D-any: 0.1081 [0.0429, 0.1795] (8 of 74)
- F|E: 0.1250 [0.0000, 0.3333] (1 of 8)

**Lowest step (frozen rule): D-taught|C** = 0.0619 [0.0452, 0.0805]; its interval overlaps: E|D-any, F|E

## Secondary

- Lesson outcomes (top-level lessons of invented kinds, n = 28897): known 180 (0.006); distrust 0 (0.000); declined 23031 (0.797); missing_part 5547 (0.192); taken 89 (0.003); taken_wrong 50 (0.002)
- D-copied | A: 0.0000 [0.0000, 0.0000] (0 of 3597)
- D-any | A: 0.0206 [0.0150, 0.0265] (74 of 3597)
- F-any | A: 0.0017 [0.0005, 0.0032] (6 of 3597)
- inventor ever teaches while knowing K | A: 0.9202 [0.9039, 0.9352] (3310 of 3597)
- inventor's value for K ever > 0.15 | A: 0.3917 [0.3769, 0.4078] (1409 of 3597)
- inventor made K again | A: 0.0114 [0.0079, 0.0154] (41 of 3597)
- a non-inventor got K on their own (own or heated) | A: 0.0550 [0.0472, 0.0632] (198 of 3597)
- lost by year 200 | A: 0.7017 [0.6802, 0.7215] (2524 of 3597)
- learner-weeks with the parts in hand: 0.0091 [0.0012, 0.0232] (782 of 86246)
- non-inventor knower-weeks with value > 0.05: 0.7521 [0.6956, 0.8087] (360405 of 479208)
- non-inventor knower-weeks with the parts in hand: 0.0092 [0.0049, 0.0148] (4390 of 479208)
- non-inventor knower-weeks with make K in the top 4 options: 0.0001 [0.0000, 0.0001] (40 of 479208)
- non-inventor knower-weeks choosing to make K: 0.0000 [0.0000, 0.0000] (7 of 479208)
- inventor knower-weeks with value > 0.05: 0.7846 [0.7651, 0.8054] (5306498 of 6763141)
- inventor knower-weeks with the parts in hand: 0.0009 [0.0006, 0.0013] (5829 of 6763141)

## Per world (kinds per stage)

seed | A | B | C | Dt | Dany | Dcopied | E | F | Fany
---|---|---|---|---|---|---|---|---|---
24401 | 77 | 23 | 23 | 0 | 0 | 0 | 0 | 0 | 1
24402 | 125 | 58 | 58 | 3 | 3 | 0 | 0 | 0 | 0
24403 | 16 | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0
24404 | 79 | 36 | 36 | 2 | 2 | 0 | 0 | 0 | 0
24405 | 131 | 40 | 37 | 5 | 5 | 0 | 1 | 0 | 1
24406 | 107 | 34 | 32 | 1 | 1 | 0 | 0 | 0 | 0
24407 | 199 | 70 | 68 | 2 | 2 | 0 | 0 | 0 | 0
24408 | 128 | 47 | 46 | 3 | 3 | 0 | 0 | 0 | 0
24409 | 77 | 24 | 23 | 1 | 1 | 0 | 0 | 0 | 0
24410 | 32 | 8 | 6 | 1 | 1 | 0 | 0 | 0 | 0
24411 | 197 | 69 | 68 | 2 | 2 | 0 | 0 | 0 | 2
24412 | 121 | 42 | 41 | 6 | 6 | 0 | 2 | 1 | 1
24413 | 135 | 43 | 40 | 2 | 2 | 0 | 0 | 0 | 0
24414 | 152 | 45 | 43 | 1 | 1 | 0 | 0 | 0 | 0
24415 | 99 | 31 | 28 | 4 | 4 | 0 | 0 | 0 | 0
24416 | 78 | 31 | 29 | 1 | 1 | 0 | 0 | 0 | 0
24417 | 108 | 35 | 33 | 2 | 2 | 0 | 1 | 0 | 0
24418 | 205 | 79 | 74 | 1 | 1 | 0 | 0 | 0 | 1
24419 | 65 | 24 | 24 | 2 | 2 | 0 | 0 | 0 | 0
24420 | 47 | 13 | 13 | 0 | 0 | 0 | 0 | 0 | 0
24421 | 161 | 52 | 50 | 4 | 4 | 0 | 0 | 0 | 0
24422 | 118 | 46 | 45 | 1 | 1 | 0 | 1 | 0 | 0
24423 | 143 | 59 | 57 | 3 | 3 | 0 | 1 | 0 | 0
24424 | 120 | 50 | 47 | 2 | 2 | 0 | 0 | 0 | 0
24425 | 119 | 35 | 34 | 3 | 3 | 0 | 1 | 0 | 0
24426 | 26 | 5 | 4 | 1 | 1 | 0 | 0 | 0 | 0
24427 | 116 | 33 | 33 | 0 | 0 | 0 | 0 | 0 | 0
24428 | 138 | 46 | 44 | 0 | 0 | 0 | 0 | 0 | 0
24429 | 98 | 33 | 31 | 2 | 2 | 0 | 0 | 0 | 0
24430 | 79 | 30 | 30 | 5 | 5 | 0 | 0 | 0 | 0
24431 | 105 | 32 | 32 | 5 | 5 | 0 | 1 | 0 | 0
24432 | 196 | 67 | 62 | 9 | 9 | 0 | 0 | 0 | 0
