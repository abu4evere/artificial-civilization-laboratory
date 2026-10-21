# RT1b — residence time with the walk to water counted: findings

Frozen as `RT1b-frozen`. Tables: `results_rt1b.md`, from `analyse_rt1b.py`. 768 worlds (256 seeds 5701–5956 × C, R4,
R4w), 40 × 40, 20 founders, 120 years, nature v2. The run paused about 11 hours while the computer slept (20–21 October)
and resumed by itself; nothing was lost.

## Validity

Zero checks PASS; all worlds present; one code fingerprint; manipulation checks PASS: in R4 and R4w adults change the
tile they sleep on in about 20% of weeks (needed 15–35%), and **the fix works**: of R4w's thirsty adult-weeks, only
**1.1%** followed a chosen trip to water (R4: 50.4%; needed under 5%). **Valid.**

## The frozen reading (extinction)

Baseline: **C died out in 91 of 256 worlds (35.5%).**

| comparison | R4w died out | reference died out | saved / lost | Holm p | effect (reference − R4w) | 95% interval | reading |
|---|---|---|---|---|---|---|---|
| R4w against C | 143 | 91 | 25 / 77 | 4.9e-07 | −0.203 | [−0.277, −0.129] | **changes survival** (R4w dies out more) |
| R4w against R4 | 143 | 148 | 45 / 40 | 0.665 | +0.020 | [−0.051, +0.090] | **no meaningful effect** |

## Beside it (described; population first)

| arm | median population, year 60 / 119 | births per woman-year | blocked for want of a partner | thirst deaths, years 0–39 / 0–119 | adult starvation deaths, years 0–39 | weeks changing tile | thirsty after a chosen trip to water |
|---|---|---|---|---|---|---|---|
| C | 23 / 20 | 0.131 | 0.536 | 1,801 / 2,400 | 1,979 | 55.1% | 1.0% |
| R4 | 8 / 0 | 0.128 | 0.534 | 2,859 / 3,343 | 1,943 | 20.5% | 50.4% |
| R4w | 10 / 0 | 0.127 | 0.534 | 2,782 / 3,215 | 2,182 | 20.4% | 1.1% |

## What it shows

1. **Fixing the flaw did not save the worlds.** Counting the week's trip to water removed the flaw RT1 found (thirst
   right after a chosen trip fell from 50% to 1%), but R4w died out as often as R4 (143 against 148) and far more than
   C (143 against 91). The median R4w world is empty by year 119.
2. **Thirst is still the difference.** Thirst deaths in R4w stay about 50% above C's in the first 40 years (2,782
   against 1,801), and adult starvation is a little higher too. Births and partner finding do not differ. So keeping a
   base still costs lives through water, by a route other than being sent back after a trip: people who keep a base
   are thirsty without having chosen to walk to water.
3. RT1's conclusion stands in a narrower form: **this base rule, as built, kills worlds**; the walk-to-water flaw was
   real but was not the main way it does.

## Against the prior (frozen; kept as written)

- "R4w against C: no meaningful effect": **wrong** (R4w dies out much more).
- "R4w against R4: changes survival (R4w much less)": **wrong** (no meaningful effect).
- "Thirst deaths in R4w close to C's": **wrong** (about 50% higher in years 0–39).
- The frozen fallback applies: "If R4w still dies out more than C, something else in the base rule costs lives, and
  that is the next thing to find."

## What it cannot show

Which part of the base rule still causes thirst: being based at a dry tile, not choosing to walk to water when thirsty,
or travel time lost to the base. That needs a read-only look at R4w's thirsty weeks (where the person was based, how far
water was, what they chose instead). Nothing in nature is changed by this study.
