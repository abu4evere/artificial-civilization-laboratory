# AP1 — why are couples apart? Results (described)

Frozen as `AP1-frozen`. run_ap1.py, analyse_ap1.py. CT1's C and K1 worlds (seeds 8201–8328) replayed exactly with a read-only observer; nature v3.

## Validity

- Zero check (observer changes nothing): **yes**
- All 256 worlds present: **yes**
- Every replay equals CT1's saved world: **yes** (256 of 256)
- Audit: observer's apart weeks equal CT1's F1 `apart` count in every world: **yes**

**Valid.**

## Q1: what couples are doing when apart (pair reason, share of apart couple-weeks)

| reason | C (weeks) | K1 (weeks) | K1 − C per world, mean | 95% interval |
|---|---|---|---|---|
| both subsistence | 38.8% (395,338) | 37.8% (421,365) | -0.0049 | [-0.0106, +0.0005] |
| one moving | 18.8% (191,324) | 19.4% (216,358) | +0.0039 | [-0.0021, +0.0100] |
| one caring | 15.0% (152,573) | 15.6% (173,452) | +0.0026 | [-0.0010, +0.0061] |
| one resting | 3.3% (33,541) | 3.4% (37,501) | +0.0004 | [-0.0010, +0.0018] |
| other | 24.1% (245,538) | 23.8% (265,649) | -0.0019 | [-0.0062, +0.0021] |

C: partnered fertile woman-weeks 1,667,740; apart 1,018,314 (61.1%); mean distance when apart 5.1 tiles.

K1: partnered fertile woman-weeks 1,814,108; apart 1,114,325 (61.4%); mean distance when apart 5.1 tiles.

Each partner's action when apart (C):

| action class | her | him |
|---|---|---|
| subsistence | 68.3% | 56.0% |
| moving | 6.7% | 13.3% |
| care | 8.6% | 9.2% |
| social | 9.0% | 12.4% |
| rest | 2.5% | 1.8% |
| other | 5.0% | 7.4% |

## Q2: who moves apart (weeks a together couple becomes apart)

| | her | him | both |
|---|---|---|---|
| C (203,066) | 38.3% | 38.6% | 23.2% |
| K1 (223,180) | 37.8% | 38.4% | 23.8% |

## Q3: how long separations last

| spell length (weeks) | 1 | 2 | 3–4 | 5–8 | 9–13 | 14–26 | 27–52 | 53–104 | 105+ |
|---|---|---|---|---|---|---|---|---|---|
| C | 37.2% | 18.3% | 17.4% | 13.0% | 6.2% | 5.3% | 2.1% | 0.4% | 0.1% |
| K1 | 37.1% | 18.1% | 17.5% | 13.1% | 6.4% | 5.3% | 2.0% | 0.4% | 0.1% |

C: 205,597 spells, mean 5.0 weeks; ended in reunion 97.1%.

K1: 225,976 spells, mean 4.9 weeks; ended in reunion 97.1%.

## Q4: hunger (described, not a cause)

- C: either partner starving in 9.6% of apart weeks against 6.6% of together weeks.
- K1: either partner starving in 9.8% of apart weeks against 6.7% of together weeks.

## Stopping rule and the prior (frozen)

- "Other" share (C): 24.1%: under a third, so the record does tell the causes apart.
- Prior "most apart weeks (over half) are both subsistence; one moving away is second": both subsistence 38.8%, second is other: **wrong**.
