# CB1 — why did the extra couples not bring more children? Findings (exploratory)

Frozen as `CB1-frozen` before any analysis. Read-only: CT1's saved C and K1 worlds (seeds 8201–8456, nature v3; 512
worlds). Tables: `results.md`, from `analyse_cb1.py` (committed before the data was read). CT1 was not valid as
committed, so CB1 only describes.

## What it shows

1. **Couples spend most of their fertile weeks apart.** Of a partnered woman's fertile weeks, **61%** are spent with
   her partner beyond the camp radius (C: 2.11 million of 3.46 million woman-weeks; K1 61.5%). Only **17%** are
   "eligible" (together, healthy, not nursing). Nursing takes 18%; low health and hunger take under 4%.
2. **When a couple is together, conception works as the code says:** 0.0407 births per eligible woman-week in C
   (0.0405 in K1), against the code's chance of 0.04.
3. **K1's extra couples are no different.** No block's share changes measurably between K1 and C (the `apart` share is
   +0.003, [−0.002, +0.009]). K1 forms more couples, so it has more partnered weeks (+6.7%) and births (24,122 → 25,449
   pooled), but per woman-year births stay flat, as CT1 found.

## Against the prior (frozen; kept as written)

"K1's extra couples spend more of their weeks apart": **not shown.** All couples are apart most of the time, not
K1's in particular.

## What it means for ACL

This is a known finding, confirmed again on nature v3: F1 and HB1 measured couples apart about 58% of the time.
The step after pairing, **being together**, is where most of a couple's chances go. ACL has tested two fixes:
- **MC1** (a camp that moves with the couple) cut time apart to 17% and raised births 12%, but did not change survival.
- **HB1** (a fixed home) kept couples together but caused hunger and more extinction.

So CB1 does not call for a new change. Togetherness limits births, but changing it alone has not saved worlds. The
partner-finding step (F2's lever) remains the one that mattered in tests. Nothing is proposed.
