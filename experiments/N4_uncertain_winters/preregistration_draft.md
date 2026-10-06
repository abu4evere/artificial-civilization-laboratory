# U — Uncertain years: correlated against patchy (pre-registration DRAFT, not frozen)

**Status:** drafted overnight while the creator slept, for the creator's sign-off. **Nothing frozen, no code written, no
world run.** Items marked **[DECIDE]** are the creator's.

## 1. Why

L1 found (post-hoc) that a steady leaner winter is absorbed by density. The creator's hypothesis **H-L5**: delayed-return
behaviour is primarily an adaptation to uncertainty rather than average scarcity. The N4 evidence review sharpened it:
sharing within a group can insure only what is not common to the whole group (Ravallion and Chaudhuri 1997; Townsend
1994), so **storage is the candidate answer to bad years that strike everyone (correlated risk)**, and sharing and moving
the answer to bad years that strike some (idiosyncratic risk; Lewis et al. 2014). ACL's years are far more predictable
than a real grassland's (ACL about 7% coefficient of variation in food from year to year, D1; real grassland production
about 37%, Shi et al. 2014).

## 2. Arms

| arm | change | risk |
|---|---|---|
| **C** control | none | ACL's current mild, world-wide variation |
| **W** wider, world-wide (U1) | the yearly growing-weather range widened around the same mean (0.95) | **correlated** |
| **P** wider, patchy (U4) | the same width, but drawn separately for each region of the world | **idiosyncratic** |

- **W needs no code**: `weather_low` and `weather_high` are settings. Because the number of random draws is unchanged, each
  seed's years are the same draws as the control's, stretched wider: the cleanest possible pairing.
- **P needs code**: a growing-weather factor per region instead of one per world, with the same distribution as W.
  **[DECIDE: region size, for example quarters of the map.]** The code must pass a zero check (with one region it must
  reproduce W exactly).
- People: A2-full, as in every analysis since E9. Code: E13R's.

## 3. The width: anchored, not tuned

The target is a **coefficient of variation of food per land tile near a third** (Shi et al. 2014: 36.6%), not any
behaviour. Because plant caps and winter dieback are not linear, the weather width that gives that food variability must
be found, not assumed. **Calibration step (before freezing the width):** on four calibration seeds of its own, run W at a
small set of widths, reading **only the coefficient of variation of mid-autumn food per land tile** and average food per
tile (to confirm the mean is kept). Pick the width whose food variability is nearest a third. The calibration reads
nothing about people. **[DECIDE: approve this calibration, and a second source on real variability before it.]**

If no width up to the widest possible (weather from 0 to 1.9) reaches a third, the widest is used and the shortfall is
reported: ACL's land itself would then be the limit.

## 4. Pilot (same-seed controls, L1's lesson)

All three arms on eight pilot seeds of their own; population and extinction only. Stop if an arm loses more than one
world beyond the control on the same seeds, or if fewer than five seeds keep all three arms alive. **[DECIDE]**

## 5. Validity

Probe read-only in every arm; code unchanged during runs; the control reproduces itself on a rerun; P's zero check.

## 6. Measures

**Manipulation check, per tile and per person (L1's lesson):** coefficient of variation of food per tile from year to
year; average food per tile (must be close to the control's: mean-preserving); food per person.

**Storage (H-L5's prediction for W):** median household stock ÷ winter need; share of carers with food stashed at the
start of winter; autumn ÷ summer share of weeks foraging (as L1).

**Sharing and moving (H-L5's prediction for P):** food given away per adult-week; tiles moved per adult-week.

**Beside every measure (Amendment 1 of L1, kept):** population per arm, worlds died out; verdict on seeds where all arms
survive; all measures per person or per household.

## 7. Predictions (H-L5, frozen on sign-off)

1. **Storage rises in W more than in P,** and more than in C. Operationally: at least two of the three storage measures
   at least **1.5×** C in W, and W's at least **1.25×** P's. **[DECIDE: thresholds.]**
2. **Sharing or moving rises in P more than in W.** Operationally: food given away per adult-week, or tiles moved per
   adult-week, at least **1.2×** W's in P. **[DECIDE.]**

**Falsification of H-L5's sharpened form:** storage rises as much or more in P as in W, or does not rise in W at all
when the manipulation check shows W's years are as variable as intended.

**Reading a null (as in L1):** a null is read only if the manipulation check shows the intended variability, and only as
"this variability, in ACL's current world, is insufficient", not as evidence that uncertainty is irrelevant.

## 8. Outcomes, written before any data

| outcome | reading |
|---|---|
| storage rises in W, not P | H-L5 supported in its sharpened form |
| storage rises in both alike | uncertainty matters but not its correlation; sharpening fails |
| sharing or moving rises in P, nothing in W | the patchy half supported; correlated uncertainty absorbed some other way |
| nothing moves anywhere | uncertainty at this level is absorbed too (by density or sharing); H-L5 not supported here |
| collapse in W or P | the variability is too harsh for ACL's people; design returns to the creator |

## 9. Order after sign-off

1. Second source on real year-to-year variability (evidence).
2. Write P's code; zero check; tests.
3. Calibration (food variability only), then freeze the width and the whole design (`U-frozen`).
4. Probe and analysis written and tested before any data.
5. Pilot with same-seed controls; then the main run; report in the frozen order.
