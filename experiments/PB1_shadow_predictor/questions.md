# PB1: A shadow brain — can a small predictor learn what ACL's actions do? (frozen plan; the brain road, step 2)

**A read-only study on live nature v13.** The predictors live in the observer, steer nothing and change nothing in the
world.
- **Why:**
  - PB0 (final: GO): foresight has room;
  - round 58: test a predictor on its own before it steers anything;
  - round 59 (`docs/debate_round59_pb1_2026-11-04.md`): GPT 94%, Gemini 95%, DeepSeek about 82%, with the merged
    changes below.
- **What it asks:** can a small predictor, learning only from what one person lives through and sees, predict what
  that person's actions do, and do so in combinations they have never lived?

## Worlds and people
- **Worlds:** 32 new seeds, **23001–23032**; v13 (`code_v13`), LP (80 founders, 80 × 80); each world runs to **year
  120**.
- **Followed people:** everyone born in years 60–100. Each is followed from their first adult week (age 16) to death or
  year 120.
- **Each followed person carries one copy of every predictor variant.** Weights start fresh: linear at 0, the network
  from a fixed seeded draw. Nothing is inherited or shared between people.

## Each week of a followed adult (prequential: predict first, then learn)
**Inputs** (perceived at the decision; no names, no outcomes, no recipes):
- **Body:**
  - edible food in weeks of need (÷ 6, capped at 1), health ÷ 100, energy ÷ 100, thirst;
  - age band (teen, adult or elder), sex;
  - partner in reach; dependents in reach.
- **Setting:**
  - season (4, one-hot); rain this week;
  - people in reach (÷ 12);
  - the own tile: plants (÷ 10, capped), fresh water in sight, fire, and the raw materials lying there (each ÷ 20,
    capped).
- **Held things:** the best edge, reach, hardness and containment among things in hand (0–1); the number held (÷ 3).
- **Recent actions:** the person's last 2 actions (19 + 19, one-hot).
- **The action taken** (19, one-hot).
- **The target's properties** (0 where the action has none):
  - **forage or hunt:** the target tile's plants and prey;
  - **gather:** the material's own 10 property values (0–1);
  - **give, care, talk, court, steal or attack:** the person's affection, trust and familiarity toward the target;
  - **make:** the 10 known properties of the recipe's result (0–1).

**Outputs** (the vector of changes over the week; **never one combined score**):
1. food gained by the week's own action (forage, hunt share, take, harvest);
2. the net change in edible food;
3. the change in health;
4. the change in energy;
5. the change in raw materials held;
6. the change in things held;
7. distance moved;
8. whether a new kind was made;
9. the change in summed affection toward others.

Each output is standardised by a running, past-only spread per world (Welford, from the first followed week). Errors
are squared standardised differences.

## The predictor variants (rates fixed here, never tuned on data)
| variant | form | learns from |
|---|---|---|
| **B (baseline)** | a table of running means per (situation index, action), the habit table's index. For a pair never lived: the person's own mean for that action; failing that, the person's overall mean; failing that, the world's running mean | own weeks |
| **L-own** | linear, normalised least mean squares, rate 0.1 | own weeks |
| **N-own** | one hidden layer of 16 tanh units, stochastic gradient, rate 0.01 | own weeks |
| **L-obs** | as L-own | own weeks + observed weeks at weight 1.0 |
| **L-obs-0.5** | as L-own | own weeks + observed weeks at weight 0.5 |
| **N-obs** | as N-own | own weeks + observed weeks at weight 1.0 |

**Observed weeks:** each week, a followed adult observes every other person aged 16+ who acted within their perception
radius.
- **The example** uses the **actor's** perceived inputs, action and target, with the actor's own **visible** outputs:
  1 (food gained), 5 (materials), 6 (things held), 7 (distance) and 8 (new kind).
- **The actor's hidden inputs** (food stores, health, energy, thirst) are replaced by the observer's own running mean
  of that input, and a flag input marks the example as observed (0 for own weeks).
- **Hidden outputs** (2, 3, 4, 9) are left out of the update, never set to 0.
- Visible failures (no gain) are kept.

## Primary measure (frozen)
**Skill** = 1 − (summed squared standardised error of the variant ÷ that of B), over the cases in question, pooled per
world.
- **The primary contrast:** **L-own against B**, on **compositionally unfamiliar weeks**. These are a followed adult's
  own weeks whose (situation index, action) they have never lived before, among the common actions: forage, gather,
  give, talk, put, join, rest, take, care, make.
- **The interval:** a world bootstrap, 10,000 replicates, NumPy seed 20261112.
- **The reading:**
  - **"the predictor learns and generalises"** if the 95% interval lies wholly above 0;
  - otherwise **"it does not"**, and the brain road stops to rethink inputs or learning before PB2.

## Secondary and described
- **Mandatory secondary:** L-own against B on **unfamiliar property combinations**. These are own weeks whose
  (action, held best edge in 3 bands, held best hardness in 3 bands, target material or target kind) the person never
  had before. It is reported with its own interval.
- **The other variants against B** on the primary cases, each with its interval. They are described, not decisive (no
  multiplicity claim). For PB2:
  - a network is preferred only if N-own beats L-own with an interval above 0;
  - observation is preferred only if L-obs beats L-own with an interval above 0.
- **Described:**
  - skill on all own weeks;
  - skill by output (each of the 9);
  - skill by weeks lived (the learning curve: 0–100, 100–500, 500–1,000, over 1,000);
  - rare actions;
  - unfamiliar places (a tile never stood on);
  - B's own error (headroom);
  - followed adults, prequential weeks and observed examples, beside every measure;
  - population.

## Validity (hard stops)
- **Zero checks:**
  - the observer and its predictors are read-only (the same world state and random state with and without them,
    over 20 and 60 years, following people born after year 5 for the check);
  - the predictors are prequential: a test confirms that each week's prediction is recorded before that week's
    update, and that no variant reads another's state;
  - reload is exact.
- **All 32 worlds** are present under the `code_v13` fingerprint.
- **A blind recompute** by GPT and Gemini (and DeepSeek if possible), from per-world sums of squared errors per
  variant and case type, of the primary skill, its interval and the reading.

## The assistant's prior (before any data)
1. **The predictor learns and generalises:** L-own beats B on unfamiliar pairs. B's fallback, the action mean, ignores
   the situation, while L-own uses body and tile.
2. **Observation helps:** L-obs > L-own, chiefly early in life.
3. **The network does not beat linear** in about 2,000 weeks of data.
4. **Skill is best for food gained and distance, and worst for affection and new kinds** (rare events).

## Sign-off (4 November 2026)
The assistant, under the creator's direction (the brain first: "keep working") and standing autonomy. It is
read-only. Council round 59: GPT 94%, Gemini 95%, DeepSeek about 82%; the assistant 80%. Frozen as `PB1-frozen` before
any code or data.
