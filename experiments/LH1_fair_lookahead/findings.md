# LH1 findings: a fairer look-ahead (a test in a copy of v13)

**Status: not final until the blind recompute** (`recompute_lh1.md`, written from the models' real replies).

Every number is from `results.md` (analyse_lh1.py, frozen before data) on run 42127234508:
- 4 arms × 32 paired seeds 23601–23632, 200 years, counted over years 100–200;
- zero checks All: PASS on the cloud (`zero_cloud.log`; `code_lh1` fingerprint b78b1b6d…), matching the local record
  (`zero_local.log`);
- 128 of 128 worlds present under one fingerprint;
- no world died out in v13, e or m; one in the sham.

## The answer in one line
**Neither rule is supported.** Both release making, but both raise starvation past the frozen guard, and m also raises
killing. Nothing is adopted.

## The frozen questions, answered
**e, the real next choice (ES2's rule):**
- **Hunger guard raised:** starvation deaths per 1,000 living-years 4.517 → 6.221, a ratio of **1.377
  [1.267, 1.496]** (the guard: above 1.25 with the lower bound above 1).
- Killing: 0.0045 → 0.0397 per 1,000 living-years, +0.0352 [+0.0070, +0.0750]. That is below the guard's 0.05, so not
  raised, though the interval lies above 0.
- Population: living-weeks ×1.290 [1.138, 1.465]. Extinction: none extra. Health −1.36 [−1.91, −0.79] (not raised).
- Making released: M3 +0.0082 [+0.0075, +0.0089]; makes per adult-year ×3.245 [3.022, 3.465].
- **Reading: not supported.**

**m, the experienced value of the next situation:**
- **Hunger guard raised:** 4.517 → 7.905, a ratio of **1.750 [1.562, 1.939]**.
- **Killing guard raised:** 0.0045 → 0.1963, **+0.1918 [+0.1006, +0.3113]**.
- Population: living-weeks ×1.316 [1.169, 1.494]. Extinction: none extra. Health −1.92 [−2.70, −1.18] (not raised).
- Making released: M3 +0.0184 [+0.0169, +0.0199]; makes per adult-year ×5.739 [5.282, 6.167].
- **Reading: not supported.**

## Described
- **Deaths (years 100–200), v13 / e / m / sham:**
  - starvation 2,029 / 3,604 / 4,672 / 2,374;
  - killed 2 / 23 / 116 / 5;
  - thirst 1,076 / 1,449 / 1,567 / 1,144;
  - illness 1,931 / 2,426 / 2,484 / 2,119.
  - Per living-year, only starvation (and, in m, killing) rises. Thirst and illness stay about level.
- **Stealing:** 0.144‰ of acts in v13; e 0.544‰ (×3.8); m 1.059‰ (×7.4); sham 0.156‰.
- **New kinds:** world-new kinds 3,458 (v13), 16,089 (e), 25,279 (m), 3,512 (sham). **Remade: 0, 2, 2, 1.** Five to seven
  times more new kinds bring no remaking.
- **Food per adult:** 8.47 (v13), 7.81 (e), 8.02 (m), 8.33 (sham).
- **The sham:** living-weeks ×1.067 [0.938, 1.216] against v13, its interval covering 1. One sham world died out.
- **A gap between the plan and the script:** the plan lists M2, M5 and R among the described measures, but
  `analyse_lh1.py` does not print them. The remade counts stand in for R. Nothing primary is affected.

## Against the assistant's prior (questions.md)
| prior | result |
|---|---|
| 1. e: no harm, making ×2–3 | making ×3.2, but **the hunger guard is raised** (×1.38) |
| 2. m: making ×4, hunger a coin toss | making ×5.7; **hunger ×1.75 and killing raised** |
| 3. R near 0 | yes: 2 remakes in each arm, against 16,089 and 25,279 new kinds |
| at least one arm supported, about 60% | **no** |

## An exploratory check (after the data; not frozen, no reading)
Do the rules raise starvation only because they make populations bigger, with more people sharing the same food?
- Per world, the mean population was 140 (v13), 181 (e), 185 (m), 150 (sham).
- **Within each arm, the population does not predict the starvation rate** (correlations −0.15, −0.02, −0.03, −0.01
  over 32 worlds).
- **Adjusting for population leaves the rules' effects unchanged:** e +1.67 and m +3.35 starvation deaths per 1,000
  living-years with population in the fit, against +1.70 and +3.39 without.
- So crowding does not explain the extra hunger at the level of whole worlds. The caution is that population is itself
  an effect of the rules, so this check cannot settle causes.

## What it means (the assistant's reading, for the council)
1. **Three rules, one pattern.** HE1 (no look-ahead), e and m all release making, and all raise starvation:
   - HE1: making ×6.07, starvation ×1.64;
   - e: making ×3.2, starvation ×1.38;
   - m: making ×5.7, starvation ×1.75.

   In v13 the look-ahead that holds making down is also what keeps people fed. Valuing making more seems to take time
   or attention from food. Not one of these rules separates the two.
2. **Remaking stays at zero whatever the look-ahead.** Even with five to seven times more inventions, almost nothing is
   made again. This agrees with VA1 and the exploratory holding check: things do wear out (median about 32 weeks); a
   full memory forgets new recipes at birth; and when the recipe is known and valued, the inputs never come together
   again. **The bottleneck for cumulative making is not the look-ahead.**
3. **Next (for council round 66):**
   - close the look-ahead line for now, without tuning it;
   - target remaking itself: why gathering never assembles a valued thing's inputs (a read-only funnel first), and
     whether an intention law (a held aim toward a thing one's own experience valued) is the general ability missing;
   - the 12-recipe memory's tie-break by name, against nested kinds (VA1's appended note; recency of use is the
     general alternative, `docs/research/memory_recency_forgetting_2026-11-05.md`).
