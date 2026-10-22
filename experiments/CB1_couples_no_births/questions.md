# CB1 — Why did the extra couples not bring more children? (SIGNED OFF 22 October 2026; frozen as `CB1-frozen` before any analysis)

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

## Sign-off (22 October 2026)

The creator: "run acl project also from where we stoped". The open choice was CB1 or CT2, and the assistant
recommended CB1, so this is taken as approval of CB1 and its prior, as written.

## Operational definitions (fixed at freezing, before any data)

- **Partnered woman-weeks:** the woman-weeks in F1's blocks `partner_dead`, `apart`, `low_health`, `starving`,
  `partner_child`, `nursing` and `eligible`. These are the blocks the code reaches only when she has a partner.
  `pregnant` is checked first, so pregnancy weeks are reported separately.
- **Shares (Q1, Q2):** per world, each block's share of partnered woman-weeks; worlds with at least 52 partnered
  woman-weeks in both arms are counted. Paired difference K1 − C, mean with a 95% bootstrap interval.
- **Births per eligible woman-week (Q3):** per world, births ÷ eligible woman-weeks (worlds with at least 52 eligible
  weeks in both arms); paired K1 − C. Pooled rates are also shown, with C's set against the code's 0.04 a week.
- **Prior check:** "right" if the `apart` share is higher in K1 and its 95% interval is above 0; otherwise "not shown".
- Exploratory throughout; the counts are reported beside every share.
