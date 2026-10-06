# U — Uncertain years: correlated against patchy (pre-registration, SIGNED OFF; width to be set by calibration)

**Status:** signed off by the creator. The creator's decisions: the **grassland** target (food variability about a
third), **quarters** of the map as P's regions, and the pilot rules and prediction thresholds as drafted. Everything
below is fixed except the weather width, which section 3's calibration rule sets mechanically; then the whole design is
frozen and tagged `U-frozen` before any probe, pilot or run. Tagged `U-signoff` now.

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

- **W needs no code**: `weather_low` and `weather_high` are settings.

  **Correction (found by the zero check, before any calibration or run):** this section first said that each seed's
  years under W would be "the same draws as the control's, stretched wider". That is true only of the first year: once
  W's land grows differently, people choose differently and use the world's random numbers differently, and the yearly
  draws diverge, as between any two arms. W and C share a seed's starting world and first year, not its whole sequence
  of years. P's guarantee is likewise narrower than first stated: it makes **no extra draws** from the world's random
  stream (its regions draw from streams of their own).
- **P needs code**: a growing-weather factor per region instead of one per world, with the same distribution as W.
  Regions: **quarters of the map** (the creator). The code must pass a zero check (with one region it must reproduce W
  exactly).
- People: A2-full, as in every analysis since E9. Code: E13R's.

## 3. The width: anchored, not tuned

The target is a **coefficient of variation of food per land tile near a third** (Shi et al. 2014: 36.6%), not any
behaviour. Because plant caps and winter dieback are not linear, the weather width that gives that food variability must
be found, not assumed. **Calibration step (before freezing the width):** on four calibration seeds of its own, run W at a
small set of widths, reading **only the coefficient of variation of mid-autumn food per land tile** and average food per
tile (to confirm the mean is kept). Pick the width whose food variability is nearest a third. The calibration reads
nothing about people. (Approved; the second source on real variability is Knapp and Smith 2001, in `evidence.md`.)

**Calibration, fixed now:** widths around the same mean 0.95, half-widths **0.30 (as now), 0.50, 0.70, 0.95 (the
widest)**, W only, on calibration seeds **801–804**, 120 years. Read: median over the four worlds of the year-to-year
coefficient of variation of mid-autumn plant food per land tile, and mean food per land tile (against 0.30's, to check
the mean is kept). **Rule:** the half-width whose median coefficient of variation is nearest 0.333 is used; if none
reaches 0.333, the widest is used and the shortfall reported. Same width for W and P.

**Which variability is realistic depends on the land.** Knapp and Smith (2001) found a fourfold range in year-to-year
variability across biomes, grasslands the most and forests the least; ACL's present 7–8% may already resemble the least
variable end. **The creator chose grassland:** the target is a coefficient of variation of food per land tile near
**one third** (Shi et al. 2014: 36.6%).

If no width up to the widest possible (weather from 0 to 1.9) reaches a third, the widest is used and the shortfall is
reported: ACL's land itself would then be the limit.

## 4. Pilot (same-seed controls, L1's lesson)

All three arms on eight pilot seeds of their own (**811–818**); population and extinction only. Stop if an arm loses
more than one world beyond the control on the same seeds, or if fewer than five seeds keep all three arms alive.
Main experiment seeds: **901–916** (never run before).

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
   at least **1.5×** C in W, and W's at least **1.25×** P's.
2. **Sharing or moving rises in P more than in W.** Operationally: food given away per adult-week, or tiles moved per
   adult-week, at least **1.2×** W's in P.

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

## 10. Operational definitions (written with the probe and analysis, before the calibration verdict and any data)

Written after sign-off, while the calibration ran and before its verdict was read; they make sections 6–8 computable
and change none of them. Code: `run_u_main.py` (probe, pilot, main), `analyse_u.py` (analysis), both tested on a
throwaway seed (999, 20 years; output discarded) and the probe shown read-only in all three arms.

- **Paired worlds:** seeds where all three arms are alive at year 120. The verdict uses them; pooled values are reported.
- **M1 variability:** for each world, the year-to-year coefficient of variation of mid-autumn plant food per land tile
  (year 1 dropped, as in the calibration); median over paired worlds. For W, over the whole world; for P, **within a
  quarter** (median of the four quarters), because a world-wide average blurs regions that vary separately. The
  intended variability is shown if W's whole-world M1 and P's within-quarter M1 are each **at least 0.75 × the
  calibration's median CV at the chosen width**. Otherwise a null is not read as evidence about H-L5 (section 7).
- **M2 mean kept:** median over paired worlds of mean mid-autumn food per land tile; W and P within **10%** of C. If
  not, the report flags that the arm's world was richer or poorer as well as more variable.
- **M3:** mid-autumn food on land per person, descriptive.
- **Storage measures** (as L1): S1 median over households of (carer's and dependants' food + carer's stashes) ÷
  13 weeks of their need, at the first week of winter; S2 share of carers with any food stashed then; S3 (share of
  adult autumn-weeks foraging) ÷ (share of adult summer-weeks foraging).
- **Sharing and moving:** G food given away per adult-week; M tiles moved per adult-week (wrapped Chebyshev distance
  between an adult's weekly positions); all seasons.
- **Prediction 1 met:** at least two of S1–S3 with **both** W ≥ 1.5× C **and** W ≥ 1.25× P. **Prediction 2 met:**
  P ≥ 1.2× W on G or on M. A ratio whose denominator is zero is met only if the numerator is positive, and flagged.
- **"Storage rose" in an arm:** at least two of S1–S3 at least 1.5× C.
- **Outcome rule (section 8), in this order:** collapse if W or P loses more than one world beyond C; else H-L5
  supported if prediction 1 met; else "both alike" if storage rose in both W and P; else falsified if storage rose in P
  and in more measures than in W; else "patchy half" if prediction 2 met; else "nothing moves" if storage rose in
  neither; else "mixed", reported as it is.
- **Validity:** pilot PASS; probe read-only (20 years, seed 901, every arm); code fingerprint unchanged; C seed 901
  rerun gives the same world hash and populations; P's zero checks PASS.

## 11. Calibration verdict and freeze

Calibration (seeds 801–804, W only, 120 years; `output/calibration/verdict.txt`), applied by section 3's rule without
change:

| half-width | median CV of mid-autumn food per land tile | mean food per land tile (of 0.30's) |
|---|---|---|
| 0.30 (as now) | 0.072 | 1.000 |
| 0.50 | 0.069 | 0.996 |
| 0.70 | 0.084 | 0.992 |
| 0.95 (widest: weather 0 to 1.9) | 0.109 | 0.972 |

**Chosen: half-width 0.95, the widest. None reaches one third: shortfall reported.** Even weather that runs from nothing
to nearly double varies ACL's autumn food by about 11% a year, a third of grassland's 37% and about 1.5× the present 7%.
As section 3 foresaw, **ACL's land itself is the limit**: plants regrow toward their caps, and the swings in the weather
are largely smoothed away before autumn. Consequences, fixed now, before any pilot or main data:

- The U experiment tests **uncertainty about 1.5× the present, not grassland uncertainty.** Section 10's manipulation
  threshold (0.75 × 0.109 = 0.082) checks that the arms deliver what the calibration found, not the grassland target.
- Any null is read, per section 7, only as "this variability, in ACL's current world, is insufficient", and the report
  states beside it that the variability tested was a third of the realistic target.
- Raising the land's own variability (caps, regrowth, dieback) would be a change to nature and a new design for the
  creator, not part of U.

Width for W and P: **weather_low 0.0, weather_high 1.9.** Frozen as `U-frozen`.
