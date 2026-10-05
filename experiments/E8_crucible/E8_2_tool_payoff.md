# E8.2 — Do tools pay? · Predictions (FROZEN)

**Written:** 2026-10-05, after E8.1, before any E8.2 run. Not to be edited after the results.
**Type:** read-only replays of the E7 code (E8 Arm 0), seeds 301–304, 120 years, checked against the saved runs.

**Question:** E8.1 showed that people almost never choose to make. Is that because the things they could make do
not actually help them much (the world gives no reason), or do tools help a lot and people ignore it anyway
(a problem in how they value or decide)?

**Known from the code (not predictions):**
- Foraging yields (12 + 14 × foraging skill) × stage × tool, where tool = 1 + 0.25 × edge + 0.3 × holding. The
  best possible tool adds roughly a fifth to a quarter; skill can more than double the yield.
- Hunting chance is multiplied by 1 + 1.5 × edge × reach + 0.3 × hardness × reach (capped at 0.92).
- Carrying capacity is 100 food, multiplied by 1 + holding.
- Yield is also capped by the plants on the tile and by how much the person can still carry.
- A thing lasts 15 + (30 × hardness + 25 × warmth + 20 × holding)/100 uses.

## Measures (adults 16+, by generation and pooled)

1. **Food from tools:** for every foraging act, the food that came because of the tool, as an upper bound:
   got × (1 − 1/tool). Its share of all food foraged.
2. **Tool payback:** for each made thing, the upper-bound food it added over its life against the cost of making
   it, counted as weeks of foraging forgone (the week of making plus weeks spent gathering its materials,
   estimated as one gathering week per material unit used), valued at the person's mean food per foraging week.
3. **Is food scarce?** Share of adult-weeks with less than a week's need on hand; share starving; share of
   foraging acts cut short by the carrying limit.
4. **Hunting:** share of adult-weeks spent hunting; success with and without a tool in hand.

## Predictions

1. **Tools add little food.** Upper-bound food from tools is under 10% of all food foraged by adults, pooled.
2. **Tools barely pay for themselves.** The median made thing returns, over its life, less than twice the food its
   making cost.
3. **Food is usually not the constraint.** Adults have at least a week's need on hand in at least 70% of
   adult-weeks.
4. **Where tools matter most, nobody goes.** Hunting takes under 2% of adult-weeks, pooled.
