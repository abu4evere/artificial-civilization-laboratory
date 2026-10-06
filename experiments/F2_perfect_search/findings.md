# F2 — Perfect partner finding: findings

Frozen as `F2-frozen` (signed off by the creator). Diagnostic copy of the control code with oracle pairing; the 64 seeds
of F1, each paired with its own F1 replay. Generated tables: `results.md`; follow-ups: `explore.md` (`explore_f2.py`).
**Valid:** zero checks passed (switch off reproduces the control world on two seeds; switch on pairs), code unchanged,
observer read-only. **Manipulation check passed:** women 16–45 with no partner fell from 55% of their weeks (F1) to 11%;
6,291 oracle pairings.

## The frozen outcome

| | F1 (as now) | F2 (perfect finding) |
|---|---|---|
| worlds died out | 22 of 64 | **7 of 64** |
| median population, year 40 / 80 / 119 | 26 / 23 / 28 | 38 / 57 / 67 |
| births per woman-year | 0.133 | 0.231 |

**Frozen rule (≤ 5 search, ≥ 17 size, 6–16 both): 7 of 64 → "Both."** Search matters, and twenty founders are still
too few for some worlds. (The count is one world above the "search" line; the frozen band is reported as it fell, not
rounded toward either story. The assistant's prior, written before the run, was this middle row; it was a prior, not a
test.)

**Paired:** perfect finding saved **17 of the 22** worlds that died in F1, and lost **2** that had survived in F1 (514,
1104). Five worlds die either way (604, 612, 613, 1110, 1122).

## Reading (descriptive; from `results.md` and `explore.md`)

1. **Search was most of the problem.** Removing it cut extinction from 34% to 11% and let populations grow instead of
   holding still (median 67 at year 119 against 28). F1's mechanism is confirmed by intervention: in most dying worlds,
   partners existed and were not found.
2. **Where search cannot help, the pool is empty.** In the seven worlds that still die, single women of childbearing
   age had **no eligible man anywhere in the world in 100%** of their single years (795 of 795): no unpartnered adult man
   who was not kin and within 15 years of her age. These worlds were already tiny in their first decade (7–19 people at
   year 10 under F2) and lost many children (0.54 deaths under 12 per birth, against 0.25 in F2's survivors). Perfect
   finding delayed the end of the five that die either way (by 7 to 40 years) but could not prevent it. **This is the size story:**
   with ACL's kin rule and age window, a handful of people soon has no one left to pair with.
3. **The two worlds lost under perfect finding** were weak in F1 too (514 ended F1 with 3 people) or took a different
   course from the first decade (1104: 10 people at year 10 under F2 against 27 in F1). Moving men across the world
   changes each world's random history from the first pairing on; two cases cannot separate a harm of the switch from
   chance. Recorded, not interpreted.
4. **Couples do not stay together.** Even with the man brought to her tile, women's weeks blocked because the partner
   was out of reach ("apart") rose from 20% to **46%**: ACL's couples drift apart in the ordinary course of foraging.
   Pairing fixed, proximity becomes the next limit on births. (A finding about ACL's nature for the creator; no change
   proposed.)
5. **Once people pair, food binds.** With more births and larger populations, the share of person-weeks starving rose
   (3.6% → 4.6%), starvation's share of deaths rose (33% → 50%), and child deaths per birth rose (0.20 → 0.26). A
   population freed from the mating bottleneck grows into the food limit: the winter questions of stage 3 return,
   with a people now large enough to face them.

## What it means (caps)

- **Story A (search) is the main cause of ACL's baseline extinction; story B (size) is real at the margin.** Both
  are needed to explain all 22 deaths.
- Perfect finding is a diagnostic, not a realistic human mechanism (the creator, in the design). Real foragers widen
  their mating networks through culture (N5), which ACL may not write. What it shows is that ACL lacks *some*
  mechanism that makes a larger mating network reachable, and, at the margin, enough people.
- F2 changes nothing in ACL's nature. Any change (M1 size, M2 search, M3 dispersal, and now couples' proximity) must be
  anchored to evidence (rule 17), checked for feasibility (rule 12), and signed off.

## For the creator (no choice made)

- **Size (M1):** the five worlds that die either way say twenty founders sometimes run out of eligible partners
  altogether; N5's viability estimates (~75–150) point the same way.
- **Search (M2/M3):** perfect finding saves 17 of 22; a realistic, anchored mechanism (people known, dispersal) would
  recover some part of that.
- **Proximity:** couples apart for nearly half of women's weeks once paired.
- **Food:** larger peoples starve more; the winter questions return once worlds survive.
