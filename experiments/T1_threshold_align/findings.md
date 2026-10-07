# T1 — Align the two thresholds: findings

Frozen as `T1-frozen` (signed off by the creator). Copy of the control code in which the pull toward a partner begins
beyond 2 tiles (where conception stops) instead of 3; F1's 64 seeds, paired with F1's replays. Tables: `results.md`.
**Valid:** zero checks passed (setting off reproduces the control world on two seeds; on, it differs); code unchanged.

## The frozen reading

**The manipulation check failed.** The share of apart couple-weeks at exactly 3 tiles had to fall to at most half of
C1's (41.8%, so ≤ 20.9%); it was **44.5%**. Couples apart, share of couple-weeks (years 0–39): 48.6% → 44.1%. **By the
frozen rule, the extinction outcome is not read.** It is recorded: 27 of 64 worlds died out (control 22); paired, 7
saved and 12 lost.

## Why the change did not do what it was meant to (exploratory, read-only; `diagnose.md`)

Replaying four T1 worlds for 20 years: when partners were exactly 3 tiles apart, a move toward the partner was among
their four top-scored options **83%** of the time, but was **chosen 19%**; foraging was chosen **50%**. Half the couples
at 3 tiles were back within 2 tiles a week later, and foraging separated them again. **T1 created the pull where it had
been missing, and food outbid it**, as C1 had already found beyond 3 tiles. The gap between the thresholds was real, but
it was not what kept couples apart: what keeps them apart is that each week's foraging choice weighs nothing for being
near a partner.

## How sensitive the worlds are (exploratory; `paired_test.py`)

A change that moved couples' behaviour only slightly still changed the fate of **19 of 64** worlds (7 saved, 12 lost).
An exact two-sided sign test on those 19 gives **p = 0.36**: the move from 22 to 27 extinctions cannot be told from
chance. Any change reshuffles each world's random history from the first week it acts, and extinction in small worlds
is fragile, so **differences of a few worlds out of 64 are within the noise**.

**For the next design (proposed, not adopted):** HB1 should measure this noise directly, for example with a sham arm that
perturbs each world's history without changing any behaviour (as E13R did), and its outcome bands should be set
against that noise.

## What it means (caps)

- Aligning the thresholds, by itself, does not bring couples together in ACL: the pull it adds is outbid by food.
- This strengthens N6's and H1's reading: what is missing is a **shared place that foraging returns to**, not a pull
  toward a partner's current position. Raising the pull's strength until couples stay together would be tuning (rule 17).
- Nothing about extinction is read from T1.
