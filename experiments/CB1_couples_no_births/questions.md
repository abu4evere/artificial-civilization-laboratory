# CB1 — Why did the extra couples not bring more children? (DRAFT for the creator; nothing run, no data looked at)

**Why.** In CT1's exploratory reading (`../CT1_courting_nature/findings.md`, Amendment 2), K1 (familiarity in
attraction) formed about 2 more couples per world (+2.0, [+0.5, +3.5]). Yet births per woman-year did not move
(+0.0001, [−0.003, +0.003]). If couples form but children don't follow, the partner bottleneck may sit **after** pairing.
CB1 asks where.

**Read-only.** CT1's saved worlds already contain F1's weekly record of each fertile woman's state (`years[y]["r_…"]`),
in the order the code checks conception:
- pregnant;
- no partner;
- partner dead;
- partner apart (beyond the camp radius);
- low health;
- starving;
- partner a child;
- nursing;
- eligible.

No new runs are needed for the main question.

## Questions

1. **Where do partnered women's weeks go?** Among woman-weeks with a living partner, the share in each block (apart, low
   health, starving, nursing, eligible, pregnant), K1 against C.
2. **Do K1's extra couples live apart?** The share of partnered weeks in "apart", K1 against C.
3. **Does eligibility turn into conception?** Births per eligible woman-week, K1 against C. The code's conception
   chance is 0.04 a week; this checks whether the measured rate matches it.

## Worlds and readings (proposed)

- CT1's C and K1, seeds 8201–8456 (256 pairs), saved. **Exploratory:** CT1 was not valid as committed, so CB1 inherits
  that status and can only describe.
- Paired differences (K1 − C) with 95% bootstrap intervals (10,000, `random.Random(2026)`), population counts beside
  each share. No tests decide anything; nature is not changed by CB1.

## The assistant's prior (to be frozen at sign-off)

K1's extra couples spend more of their weeks **apart** (the partner beyond the camp radius), so they rarely reach
"eligible". Births stay flat because pairing does not bring partners together.

## Decisions for the creator

1. Run CB1 (read-only, minutes), or choose CT2 instead (`../CT2_lonely_courting_confirm/questions.md`), or neither.
2. The prior, frozen as written.
