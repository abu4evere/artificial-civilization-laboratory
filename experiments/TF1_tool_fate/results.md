# TF1 — Where do made things go? Results

Frozen as `TF1-frozen` (operational note 1). run_tf1.py, analyse_tf1.py (written before data).

## Validity

- Zero checks: **yes**
- All worlds present (32 of 32): **yes**
- One fingerprint (`code_v7`): **yes**
- The ledger balances in every world (appeared = ended + still in the world): **yes**
- Unknown fates: 489 of 256250 ends (0.0019); under 1%: **yes**

**Valid.**

## Population (worlds alive at each bin's start)

| bin | worlds | mean population |
|---|---|---|
| 0-5 | 32 of 32 | 91.5 |
| 5-10 | 32 of 32 | 98.1 |
| 10-20 | 32 of 32 | 102.6 |
| 20-50 | 32 of 32 | 105.2 |
| 50-100 | 32 of 32 | 119.3 |
| 100-200 | 32 of 32 | 112.5 |

Worlds that ended before year 200: [118, 182].

## Q1 — How do forage tools end? (forage factor > 1; by the bin in which they ended)

| bin | ends | worn_out | deleted_at_limit | used_in_making | lost_at_death | lost_with_body | unknown | life (weeks, mean) | uses left at end (mean) |
|---|---|---|---|---|---|---|---|---|---|
| 0-5 | 5328 | 0.595 | 0.038 | 0.366 | 0.001 | 0.000 | 0.000 | 38.3 | 12.5 |
| 5-10 | 19638 | 0.284 | 0.052 | 0.663 | 0.000 | 0.000 | 0.000 | 38.6 | 27.3 |
| 10-20 | 38325 | 0.416 | 0.061 | 0.521 | 0.000 | 0.000 | 0.001 | 51.8 | 20.6 |
| 20-50 | 65648 | 0.566 | 0.042 | 0.390 | 0.000 | 0.000 | 0.001 | 60.5 | 14.9 |
| 50-100 | 59447 | 0.652 | 0.021 | 0.326 | 0.000 | 0.000 | 0.001 | 60.3 | 12.2 |
| 100-200 | 60308 | 0.708 | 0.013 | 0.277 | 0.000 | 0.000 | 0.002 | 65.4 | 10.3 |

All bins pooled, with world-bootstrap intervals:

- worn_out: 0.576 [0.568, 0.584]
- deleted_at_limit: 0.034 [0.0319, 0.0355]
- used_in_making: 0.388 [0.381, 0.396]
- lost_at_death: 0.000 [0.000276, 0.000408]
- lost_with_body: 0.000 [0, 0]
- unknown: 0.001 [0.00116, 0.00146]
- (forage tools still held at the end: 4321; ended: 248694)

**Forage-tool uses left at the end, by fate** (uses destroyed), per 1,000 person-years:

- worn_out: 233.3
- deleted_at_limit: 389.1
- used_in_making: 4570.2
- lost_at_death: 1.3
- lost_with_body: 0.0
- unknown: 3.2

## Q2 — The carry limit

- Made things deleted at the carry limit: 10666. **Share that were working forage tools: 0.784 [0.757, 0.81].**
- Their uses left (mean): 33.3; their forage factor (mean) 1.125.
- Better forage tool than the worst thing kept: 0.696.
- Holder had a child under 16 in their care: 0.072; anyone within reach: 0.881; a child under 16 within reach: 0.742.
- Forage-tool uses destroyed by the carry limit: 278199; left at wearing out: 166795.

**Gone within the week they were made** (operational note 2; never in the weekly census):

- made in play: 234328; gone the same week 0.124; of those, a kind with worth 0: 0.988
- made in make: 59117; gone the same week 0.041; of those, a kind with worth 0: 0.232

## Q3 — Forage tools at their holder's death

Forage tools whose holder died: 5188. with_body_at_end 0.712, taken_from_body 0.227, inherited 0.044, lost_at_death 0.016.

**Inherited: 0.044 [0.0378, 0.0502].**

| bin | forage-tool uses lost at death or with the body, per 1,000 person-years |
|---|---|
| 0-5 | 0.3 |
| 5-10 | 13.6 |
| 10-20 | 1.8 |
| 20-50 | 3.2 |
| 50-100 | 1.4 |
| 100-200 | 0.2 |

## Q4 — Children and tools

| bin | children (6-15) holding a forage tool | no tool while their carer holds 1+ | no tool while carer holds 2+ | adults holding a forage tool |
|---|---|---|---|---|
| 0-5 | - | - (0 wk) | - | 0.288 |
| 5-10 | 0.949 | 0.031 (28693 wk) | 0.013 | 0.450 |
| 10-20 | 0.781 | 0.156 (244966 wk) | 0.114 | 0.535 |
| 20-50 | 0.569 | 0.350 (331589 wk) | 0.279 | 0.359 |
| 50-100 | 0.345 | 0.603 (228066 wk) | 0.522 | 0.135 |
| 100-200 | 0.228 | 0.740 (180833 wk) | 0.664 | 0.063 |

**Child-weeks with no forage tool while the carer holds one, all bins: 0.421 [0.4, 0.441].**

First forage tool (world-born, 17911 people): median age 3.5 years; before 16: 0.999; how: made 1.000, taken_from_body 0.000.

## Q5 — Replacement within a year, by route

| bin | lost their last forage tool | replaced within a year | made | inherited | taken from a body | other |
|---|---|---|---|---|---|---|
| 0-5 | 1437 | 0.556 | 0.997 | 0.000 | 0.003 | 0.000 |
| 5-10 | 2132 | 0.500 | 0.996 | 0.000 | 0.004 | 0.000 |
| 10-20 | 5450 | 0.541 | 0.995 | 0.001 | 0.004 | 0.000 |
| 20-50 | 18123 | 0.385 | 0.991 | 0.001 | 0.008 | 0.000 |
| 50-100 | 23831 | 0.231 | 0.994 | 0.000 | 0.006 | 0.000 |
| 100-200 | 27217 | 0.136 | 0.994 | 0.000 | 0.005 | 0.000 |

