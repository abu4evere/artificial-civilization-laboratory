# S1 — World size: feasibility check (plan, written and committed before any run)

**Chosen by the creator (October 2026), option (b) of N10:** test more land alone **and** land and people together,
starting with a read-only feasibility check, then a frozen protocol. **This file covers only the feasibility check.**
No outcome (extinction, survival, population trend) is looked at here.

## The three configurations (settings only; the code is unchanged)

| arm | `width × height` | `founders` | question it serves |
|---|---|---|---|
| **C** control | 40 × 40 | 20 | today's world |
| **L** more land | 80 × 80 | 20 | does a larger world change survival? (C vs L) |
| **LP** land and people | 80 × 80 | 80 | does adding founders change survival, given the larger world? (L vs LP) |

LP against C changes both factors at once; on its own it cannot say which one mattered. The 80 / 80 × 80 values keep
ACL's own crowding (founders per tile) in LP; they are **not** set by Hamilton et al. 2007 or White 2017, which describe
different things (typical group sizes; a minimum viable population) and do not establish a founder count or map size for
ACL.

## What the code does with these settings (read-only reading)

- Land: an archipelago with 40% land at every size (`geo.generate`: sea at the 60th height percentile); the number of
  islands grows with area (`max(4, w·h/300)`: 5 at 40 × 40, 21 at 80 × 80); island radius grows with the map.
- Founders: split into `min(4, founders / 4)` bands, each starting on its own island: **4 bands of 5 in C and L; 4
  bands of 20 in LP.** So LP also changes the size of the founding bands. This is the code's own rule and is not altered.
- Animals: groups per species scale with the amount of their habitat (`fauna.populate`), so wildlife per tile is
  comparable.

## Checks (on throwaway seeds 9001–9004, never used later; 10 years per run)

1. **Feasibility:** every configuration initializes and runs 10 years without error, on all four seeds.
2. **Comparable conditions:** land share (expected 40% in all); mean fertility of land tiles; animal groups per land
   tile; starting food per founder (same setting). Reported for each arm.
3. **Manipulation, spatial:** land tiles per founder (expected 4× in L, equal in LP and C); mean distance between
   founding band centres (expected larger in L and LP).
4. **Manipulation, demographic:** founders and founding band size; eligible opposite-sex founders (unrelated, within
   15 years of age) per founder, and within sight (4 tiles) per founder, at week one.
5. **Runtime:** seconds per world-year for each arm (median over seeds), and an estimate for a main run of 256 seeds ×
   arms × 120 years on four workers.

## Pass / stop

- **Pass** if 1 holds for all arms and seeds, land share differs by under 5 percentage points between arms, and the
  manipulation checks move in the expected directions.
- **Stop** (back to the creator) otherwise. Runtime is reported, not gated; the creator decides the sample size from it.
- **Not looked at:** population, births, deaths, extinction. The runs are stopped at 10 years and only the measures
  above are recorded.
