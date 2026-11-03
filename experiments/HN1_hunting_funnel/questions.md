# HN1: Where do v11's hunts fail? (frozen plan)

**A read-only study on live nature v11 (`code_v11`).** Nothing in nature changes.
- **Why:** council round 53 (`docs/debate_round53_after_af1_2026-11-03.md`): GPT 95%, Gemini 98%, DeepSeek about 78%.
- **The evidence it rests on:**
  - AF1: people rarely make anything;
  - TR1: hunting gives about 0.001% of food;
  - the older review `experiments/FX1_extracted_foods/evidence.md`: ACL's hunting returns about 4% of foraging, against
    about 1.1 among the Aché.
- **Its use:** HN1 is step 1. It decides, by a rule written now, which **one** existing setting HR1 (step 2) may
  calibrate toward forager evidence.
- **It also measures two faults** from the rules review: F7 (unused per-species catch rates) and F8 (the decision
  expects about 37 food per kill; kills give far less).

## Sample (32 new seeds 22601–22632; LP: 80 founders, 80 × 80; 200 years; years 100–200 counted)
- **Hunter-weeks:** every adult (aged 16–49) hunt resolved in `actions.resolve_hunts`.
- **Forage-weeks:** every adult forage.

## Measures
1. **The failure funnel** (shares of adult hunter-weeks):
   - **(a) no prey:** no prey on the tile where the hunt is resolved, so the chance is 0;
   - **(b) the roll failed:** prey were there, but the roll failed;
   - **(c) success.**

   Within (c), the share of the hunter's meat share **lost to carrying room**. Each is reported for armed hunters (best
   hunt factor above 1) and bare-handed ones.
2. **The return ratio (primary for HR1's target).**
   - **The pooled ratio:** R = food per adult hunter-week (meat kept) ÷ food per adult forage-week, from sums pooled per
     world.
   - **A matched version (GPT):** for each hunter-week, the same person's forage-weeks in the same season and year, on
     tiles in the same plant-stock band (the tile's plants + crop before foraging: below 10, 10–40, above 40). Each
     hunter-week is compared with the mean of its matches; weeks without a match are dropped and counted.
3. **F8, expected against realized:** the meat share a lone hunter expects in the decision (25 + 12 × n) ÷ n, against
   the meat per success actually kept.
4. **F7, success by species:** the success rate by the species taken, against the unused table rates.

**Intervals:** a world bootstrap, 10,000 replicates, NumPy seed 20261109.

## The routing rule for HR1 (frozen now)
- **F = the share of failed hunts with no prey on the tile,** that is (a) ÷ ((a) + (b)), pooled.
- **If F > 0.5** (point estimate), HR1 calibrates **prey encounter** (the density of prey groups, `fauna.DENSITY`).
  Otherwise it calibrates **the base chance** (`hunt_base_chance`).
- The interval for F is reported. If it straddles 0.5, HR1's plan says so and the council is asked before HR1 is
  frozen.
- **HR1's target:** the return ratio R moved toward the Aché's about 1.1 (an accepted range of 0.5–1.5, a
  population-specific reference, not a universal one).
  - The arms are chosen only on calibration distance and safety (population and extinctions first).
  - Armed and bare-handed returns are reported, and their ratio is flagged before adoption (DeepSeek).
  - Remaking and tool use are described only.
  - Hold-out seeds confirm.

## Validity (hard stops)
- **Zero checks:**
  - the observer is read-only (the same state with and without it, 20 and 60 years);
  - reload is exact;
  - **the funnel adds up:** (a) + (b) + (c) = all hunter-weeks in a 30-year test world.
- **All 32 worlds** are present under the `code_v11` fingerprint.
- **A blind recompute** by GPT, Gemini and DeepSeek of F, R and the funnel shares, with intervals, from per-world sums.

## The assistant's prior
1. **F > 0.5.** Prey often flee before the hunt is resolved (`flee`), and a hunter blocked short of the target tile
   hunts where they stopped.
2. **R between 0.02 and 0.10**, near the old review's 4%.
3. **Expected meat per success is about 3 times the realized.**

## Sign-off (3 November 2026)
The assistant, under the creator's sleep-mode autonomy and the permission of 2 November. It is read-only. Council round
53: GPT 95%, Gemini 98%, DeepSeek about 78%, the assistant 80%. Frozen as `HN1-frozen` before any code or data.
