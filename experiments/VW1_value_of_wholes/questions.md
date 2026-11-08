# VW1: what a valued whole needs is wanted — a law tested in a copy of v16 (frozen plan)

**A test of one law in a copy of nature v16, with a sham.**
- **Council round 78** (`docs/debate_round78_after_pm1_df1_2026-11-07.md`) put this law first. GPT (96%) and DeepSeek
  (about 78%) call it a new law, to test with a sham and a confirmatory run. Gemini (95%) calls it a fault. The stricter
  law path is taken.
- **PM1** found the wall it targets: for 0.710 of new kinds needing a made part, someone who knows the kind knows the
  part's recipe but **never has the part's inputs in hand** (0.838 at depth 3+).

## The law (VW, `want_down` = 1; 0 = v16)
In v16:
- a part gets value for making from a whole the person values directly (`mind._wanted_parts`: 0.8 × the whole's value),
  only one level down;
- raw materials are wanted for gathering only for recipes valued directly (`mind._material_wants`).

The law extends the first rule, and joins it to the second:
1. **Value flows down the recipe tree.** Start from each recipe K the person values directly (`itemval` > 0) and does not
   hold: each made part X of K gets 0.8 × K's value, as now. With the law, **if the person knows X's recipe and does not
   hold X, X's own made parts get 0.8 × X's wanted value**, and so on down.
   - Each thing keeps the highest value that reaches it.
   - The flow stops at raw materials, at recipes the person does not know, at things held, at cycles, and below a value
     of 0.01.
2. **The make rule** uses this value for every known recipe in the tree (in place of v16's one level).
3. **The gather rule:** for every known recipe with a wanted value above 0, not held, its raw materials are wanted at
   that value. The higher of this and v16's own wants counts.

The law names no thing and plans no chain. It adds no reward and no lesson. **Value flows only through recipes the
person already knows** (GPT): nothing is taught, and nothing is given.

## Arms and seeds
- **v16 (c), VW (w), and the sham (x):** the standard sham, one extra draw from the world's generator in week one.
- **Seeds 25201–25232** (32 new paired seeds). LP; 200 years. Kinds born in years 100–190 are followed for 5 years
  (MP1's rule).
- `code_vw1` = `code_v16` + `want_down`.

## Frozen decision rule
- **Guards (VW against v16):** CI1's eight, exactly as in LW1 and FF4. Paired world bootstrap, 10,000 draws, NumPy seed
  20261129.
- **Co-primaries** (GPT's two, with MP1's stages). Among new kinds needing a made part:
  1. **any made part held:** the share where some knower of the kind holds at least one of its made parts at a week's
     end within 5 years (MP1 stage B or beyond), VW − v16;
  2. **all made parts held at once:** the share where one knower holds all of its made parts at once (MP1 stage C or
     beyond), VW − v16.
- **Readings:**
  - **supported:** no guard is raised, and both co-primaries' lower bounds are above 0;
  - **partly supported:** no guard is raised, and only co-primary 1's lower bound is above 0. Not adopted; reported
    for the council;
  - **harm:** any guard is raised;
  - **no harm, no effect:** otherwise.
- A supported reading goes to a confirmatory run on new seeds before any adoption.

## Pre-registered secondaries (not gates)
- Kinds **made again** within 5 years (MP1 stage E), and **made by a non-inventor**, VW − v16 (DeepSeek's mission
  measure).
- **By depth:** the co-primaries at depth 1, 2 and 3+ (DeepSeek's 3+ focus).
- **Food-production displacement** (GPT): the grown's share of weeks foraging, gathering and making, per arm.
- **The funnel's mechanism** (DeepSeek): in VW, how often the make option offered is a part or a sub-part of a valued
  whole, against v16.

## Validity (hard stops)
- **Zero checks:**
  - `code_vw1` at 0 = `code_v16` (20 and 60 years, world and random stream);
  - the observers are read-only (c and w);
  - VW and the sham act;
  - reload is exact;
  - **unit checks** (a VW world, 30 years):
    - at sampled decisions, the wanted-value map equals an independent recursive computation of the law, and v16's
      one-level map is the depth-1 part of it;
    - the materials wanted include those of every known, unheld recipe with a wanted value above 0.
- **All 3 × 32 worlds** are present under one fingerprint.
- **A blind recompute** by GPT and Gemini (and DeepSeek if it has a code tool).

## The assistant's prior
- **Co-primary 1 rises clearly; co-primary 2 rises a little.** Supported about 45%; partly supported about 30%.
- **Starvation is the risk:** HE1 and LH1 raised it whenever making was released. A raised guard is possible, about 20%.

## Sign-off (7 November 2026)
The assistant, under the creator's 2 November permission (new general laws through council, a frozen test in a copy
with a sham, blind recompute, confirmation, the safe path) and 7 November ("you can keep going do not rely on me").

Council round 78:
- GPT 96%;
- Gemini 95% (as a fault);
- DeepSeek about 78%;
- the assistant 80%.

Frozen as `VW1-frozen` before any code or data.
