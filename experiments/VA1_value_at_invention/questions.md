# VA1: Is a new invention valued before it is lost? A read-only value-at-invention audit (frozen plan)

**Read-only on nature v13.**
- The runner only watches, through wrappers as in LD1.
- Zero checks prove the world is unchanged.

**Why:**
- LD1 found that new kinds are lost before any chance to be made again: 88% of v13's kinds stop at "held the recipe,
  never with its inputs".
- A new recipe enters with value 0 (`acl/knowhow.py` lines 73–82).
- A made thing's value is learned only when it is used (`knowhow.judge_item`).
- The make choice offers only recipes valued above 0.05.
- Council round 65 (`docs/debate_round65_after_he1_2026-11-05.md`): all three models ask for a read-only
  value-at-invention audit before any nature change. GPT: "test whether observable outcomes actually provide enough
  information to assign meaningful initial value".

**What it asks:**
1. Is a new kind ever used, and so valued, before its recipe is lost?
2. Would a value from experience have kept it?
3. Does the person's experience with **similar** things predict how useful a new kind turns out to be?

## Worlds
- v13 only, 32 new seeds **23701–23732**; LP (80 founders, 80 × 80); 170 years.
- Kinds followed are those first made in play in years 130–165 (AF1's and LD1's rule), each for 5 years in its
  inventor's weeks.

## What is recorded for each kind
At invention:
- **the other recipes' values:** the person's other recipes and their `itemval`; the lowest of them is what the new
  kind must beat to survive the 12-cap;
- **v_sim:** the person's mean `itemval` over the kinds they know, each weighted by its property similarity to the new
  kind, 1 − (mean absolute difference of the 10 properties on a 0–1 scale) clipped at 0, using `world.knowledge`
  props. It is None if they know no valued kind.

During the 5 years:
- every use of the kind by the inventor (`judge_item` on it): week, `felt`, value before and after;
- the week the recipe was first gone;
- whether the inputs were ever held while the recipe was held;
- whether a make option for it was offered;
- whether it was remade (LD1's stages, recomputed here).

## Measures
A world bootstrap: 10,000 replicates, NumPy seed 20261119; shares pooled over worlds.

1. **Primary 1, "used before lost":** the share of kinds whose inventor used it at least once before its recipe was
   gone.
   - **"Unvalued at birth dominates"** if this share is below 0.5, with its upper bound below 0.5.
2. **Primary 2, counterfactual retention:** the share of kinds that would beat the lowest of the inventor's other
   recipe values at invention, and so survive the cap, under two first values:
   - v_first, the felt value of the kind's first use (among kinds ever used);
   - v_sim.
   - Each is shown against the share that survived the first week in fact.
3. **Primary 3, is experience informative?** Among kinds both used and with a v_sim, the correlation between v_sim
   and the felt value of the first use.
   - **"Similar experience is informative"** if the correlation's 95% interval lies wholly above 0.2.
   - This decides whether "a new kind's first value comes from similar known kinds" is a law worth testing.
4. **Described:**
   - LD1's stage shares;
   - weeks from invention to first use and to loss;
   - the share of uses with felt > 0.05;
   - the share of kinds whose first value (v_first, v_sim) clears the 0.05 offer threshold;
   - all of these with the number of kinds beside them.

## What follows (decided before data)
- **If "unvalued at birth dominates" and "similar experience is informative":** a nature test in a copy of the law "a
  new kind's first value is the person's experience with similar things" (generalisation from experience, no reward
  for novelty), with harm guards. Council first.
- **If used kinds are still lost, or v_sim is uninformative:** the next target is opportunity or intention (getting the
  inputs again), not value.

## Validity (hard stops)
- **Zero checks:**
  - the observers leave the world unchanged (20 and 60 years);
  - a unit check: every recorded use's value after equals `judge_item`'s rule applied to the value before.
- **All 32 worlds** are present under one `code_v13` fingerprint.
- **A smoke run** before the cloud.
- **A blind recompute** by GPT, Gemini and DeepSeek of the three primaries.

## Known limits
- v_sim weights properties equally. That is a simple general similarity, not tuned.
- The counterfactuals are computed at invention only. They do not replay the world with a different rule.

## The assistant's prior
1. **"Unvalued at birth dominates":** most kinds are never used before being lost.
2. **v_first would keep most of the used kinds; v_sim keeps fewer.**
3. **"Similar experience is informative":** about 50%.

## Sign-off (5 November 2026)
The assistant, under sleep-mode autonomy. Read-only. Council round 65: all three models ask for this audit (Gemini
95%, DeepSeek about 80%, GPT for the audit). The assistant 75% that it is valid and informative. Frozen as
`VA1-frozen` before any code or data.
