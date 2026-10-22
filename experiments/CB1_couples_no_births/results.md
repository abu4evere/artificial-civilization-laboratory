# CB1 — why did the extra couples not bring more children? Results (exploratory)

Frozen as `CB1-frozen`. analyse_cb1.py. Read-only: CT1's saved C and K1 worlds (seeds 8201–8456). CT1 was not valid as committed, so this only describes.

All 512 worlds present.

## Q1–Q2: where partnered woman-weeks go (worlds with ≥ 52 partnered weeks in both arms: 256 of 256)

| block | C pooled share (weeks) | K1 pooled share (weeks) | paired K1 − C, mean | 95% interval |
|---|---|---|---|---|
| partner_dead | 0.0% (0) | 0.0% (0) | +0.0000 | [+0.0000, +0.0000] |
| apart | 61.0% (2,110,334.0) | 61.5% (2,268,174.0) | +0.0031 | [-0.0022, +0.0085] |
| low_health | 2.3% (79,445.0) | 2.3% (85,560.0) | +0.0007 | [-0.0004, +0.0018] |
| starving | 1.5% (51,107.0) | 1.5% (55,291.0) | +0.0000 | [-0.0002, +0.0003] |
| partner_child | 0.0% (0) | 0.0% (0) | +0.0000 | [+0.0000, +0.0000] |
| nursing | 18.1% (626,852.0) | 17.7% (652,837.0) | -0.0031 | [-0.0071, +0.0009] |
| eligible | 17.1% (592,445.0) | 17.0% (628,560.0) | -0.0007 | [-0.0028, +0.0013] |

C: pregnant woman-weeks 953,057.0; woman-weeks with no partner 5,213,014.0; partnered woman-weeks 3,460,183.0.

K1: pregnant woman-weeks 1,006,012.0; woman-weeks with no partner 5,321,902.0; partnered woman-weeks 3,690,422.0.

## Q3: births per eligible woman-week (worlds with ≥ 52 eligible weeks in both arms: 256)

- C pooled: 24,122 births / 592,445.0 eligible woman-weeks = 0.0407 a week (the code's conception chance is 0.04; births lag conception by pregnancy).
- K1 pooled: 25,449 births / 628,560.0 eligible woman-weeks = 0.0405 a week (the code's conception chance is 0.04; births lag conception by pregnancy).
- Paired K1 − C: -0.00028 [-0.00088, +0.00033].

## The prior (frozen)

"K1's extra couples spend more of their weeks apart": the `apart` share K1 − C = +0.0031 [-0.0022, +0.0085]: **not shown**.
