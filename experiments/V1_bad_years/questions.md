# V1 — What do ACL's existing bad years do? Questions (written before any data)

**Read-only. No new mechanic, no world changed.** Written while the creator slept, after N4's candidates and before its
evidence review, as the baseline H-L5 needs: ACL already varies from year to year, so before making winters less
predictable, measure what its existing bad years do.

> **H-L5 (the creator):** delayed-return behaviour is primarily an adaptation to uncertainty rather than average
> scarcity.

**What ACL's years are now (from the code):** each year the world draws, uniformly and independently: growing weather
0.65–1.25 (scales all plant growth), wetness 0.45–1.35, winter hardness −0.1 to 0.15 (winter dieback 2.4–3.9% a week, and
cold). The same for the whole world.

**Worlds:** E13R's control (Arm A, A2-full), seeds 501–516, 120 years, replayed with a read-only probe (state hash, 20
years; every replay equal to the saved E13R run). Year by year, the probe records the year's draws, the land (food **per
tile**, L1's lesson, and per person), the population, deaths, and what people did.

## The questions

1. **How variable are ACL's years?** The spread of mid-autumn and mid-winter plant food per land tile from year to year,
   and how much of it the year's draws explain.
2. **Are bad winters deadly?** Winter starvation deaths (adults and children, per person) against the year's winter food
   per tile and hardness; what share of all winter starvation falls in the worst quarter of winters.
3. **Does density absorb bad years?** Population change across a bad winter, and how long it takes to recover.
4. **Do people respond?** In the autumn **after** a bad winter, against the autumn after a mild one: planners (adults
   holding 80+ food in autumn), median household stock ÷ winter need at the next winter's start, carers with food
   stashed, seed sown, and people's learned expectation of going short in winter (A2's `short@winter`).
5. **Do bad years cluster?** Year-to-year correlation of winter food per tile (the draws are independent; the land may
   carry some over).

## Reading rule

Descriptive; nothing scored; associations over 16 worlds × 120 years, not causes. "Bad winter" and "mild winter" are
defined within each world: the worst and best quarter of its winters by winter starvation deaths per person (and,
separately, by winter food per tile), so that worlds of different sizes are compared fairly. V1 changes nothing.
