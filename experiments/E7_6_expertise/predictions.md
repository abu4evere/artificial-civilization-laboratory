# E7.6 — Expertise retention audit · Predictions (FROZEN)

**Written:** 2026-10-04, before any E7.6 run. Not to be edited after the results.
**Type:** read-only audit. No line of simulation behaviour changes. Every world is a replay of a saved run
(E7 experiment, both arms: the E6 code as `baseline`, the E7 code as `e7`; seeds 301–308), checked against
the saved population at every 10-year sample before its numbers are used.

**Question:** is ACL's bottleneck skill decay, maker decay, recipe decay, or population size?

## Known from the code before running (not predictions)

- Founders start with crafting skill 0.2–0.4; everyone born later starts at 0.
- Crafting skill rises only by practice: each crafting act adds 1.2% of the gap to 1.0 (×1.6 when focused).
  Reaching 0.8 from 0 takes on the order of 130 crafting acts.
- Skill is never taught, inherited or lost while alive. It dies with the person.
- Skill affects how sharp a struck flake is, how fast materials are gathered, and how many errors a teacher
  passes on.

## Measures (recorded every 25 years, or per decade)

- Q1 crafting skill: best living person, mean of the top 10, mean of all living people, mean of adults.
- Q2 recipes held by the living: unique recipes, total holdings, mean holders per recipe, most widely held.
- Q3 making per decade: accidental (a thing made in play) and deliberate (a thing made from a recipe).
- Q4 watertight things (tight ≥ 50 and contain ≥ 40): made per century, carried at each sample, people
  carrying one.
- Q5 per world: peak and mean population, LFA (from the saved run), best skill at years 100 / 500 / end,
  deliberate makes per person-year; Spearman correlations across worlds, reported with n and no p-values
  presented as proof (n ≤ 16).

## Predictions

1. **Skill decays.** In every world that lives 300+ years, the best living crafting skill at year 300 is lower
   than at year 50, and the population mean at year 300 is below 0.15.
2. **Deliberate making is rare and does not grow.** Deliberate makes stay under 1 per person per decade in
   every world after year 100, and the per-person rate after year 100 is lower than in the first 50 years.
3. **Recipes thin out.** Unique recipes held by the living fall by at least half between their peak and year
   500 in every world alive at 500 (matching E5's "knowledge peaks early, then thins").
4. **Vessels are the water bottleneck.** Fewer than 5 watertight things are made per world per century on
   average, and in at least half of all 25-year samples no living person carries one.
5. **Population helps, weakly.** Across worlds, mean population correlates positively with best skill at
   year 500 and with deliberate makes per decade (Spearman ρ > 0.3), but not strongly enough (ρ < 0.7) to be
   the whole story.
6. **E7 does not change expertise.** Passive firing adds accidental clay things, but E7 worlds show no higher
   skill and no more deliberate making than the baseline at matching years.

## Kill criterion (the audit is invalid if)

- any replay fails to match its saved run's population samples;
- the probe changes the world (state hash with and without it, 20 years, both codes);
- any simulation code file changes during the runs.
