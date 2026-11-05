# LD1: Why does the habit look-ahead lock choices, and where does remaking fail? (frozen plan; read-only)

**Read-only on nature v13.**
- Nothing in nature changes.
- The runner only watches decisions and habit updates from outside (wrappers, as in AM1). Zero checks prove the world
  is unchanged.
- The c0 worlds use an existing setting (`discount` 0) as a comparison, as in PB3.

**Why:**
- PB3 (final): the habit table's one-week look-ahead is the habit trap.
  - Habit update: q ← q + 0.05 × (r + 0.8 × max over next week's situation's 19 habit values − q), clamped to ±1.5.
  - Without it (c0), finished gather-then-make chains rise from 0.0035 to 0.0263.
  - Makes rise about 6.6 times.
  - Yet nothing is ever made again (R = 0 of 11,348 kinds).
- Council round 63 (`docs/debate_round63_after_pb3_2026-11-05.md`): all three models want a read-only diagnosis
  first, then an R decomposition, before any change. GPT 97%, Gemini 95%, DeepSeek about 93%.

**What it asks:**
1. Is the lock a matter of **scale** (look-ahead values swamp the written pulls), of **direction** (acts that do not
   feed you lose next week's best value), both, or neither (it lies in the states people reach, not in single
   choices)?
2. Where along the path from inventing to remaking is each new kind lost?

## Worlds
- **c:** v13.
- **c0:** v13 with `discount` 0.
- 32 new paired seeds **23401–23432**; LP (80 founders, 80 × 80); 170 years.
- Measured over adults 16–49 in years 130–170; population beside every measure.

## Part A: the look-ahead (counted in years 130–170)
**Shadow habit tables (read-only):**
- From year 100, each person also keeps two shadow tables, updated at every habit update by the same rule as q:
  - q_r ← q_r + 0.05 (r − q_r), the part learned from this week's r;
  - q_f ← q_f + 0.05 (0.8 × max next q − q_f), the look-ahead part.
- They start at q_r = q and q_f = 0, from year 100 or the person's first habit update after it.
- Without clamping, q = q_r + q_f exactly. The gap |q − (q_r + q_f)| is reported as the approximation check.

**At every adult decision** (all options, after the thought pulls, as scored for the softmax), the habit term of an
option is h = 0.6 × q[situation, action]. The softmax probabilities with v13's temperature are computed for four
score versions, without changing the choice:
- **actual:** s;
- **scale:** s − h + 0.2 h (q put on the no-look-ahead scale, 1 − 0.8);
- **direction:** s − h + 0.6 × (q_r + the mean of q_f over all 19 actions in that situation). The look-ahead keeps
  its level but loses its differences between actions.
- **none:** s − h + 0.6 × q_r (the habit learned from the same experience without the look-ahead).

**Shares:** the expected share of decisions going to make, gather, forage, play and person-aimed acts, in each
version. The same actual shares in the c0 worlds.

**Primary A: the make share.**
- Recovery of each version: f = (share_version − share_actual) ÷ (share_c0 − share_actual), using v13's decisions,
  with c0 from its paired worlds.
- A paired world bootstrap: 10,000 replicates, NumPy seed 20261116.
- **Reading:**
  - **"scale"** if f_scale ≥ 0.5 and f_direction < 0.5;
  - **"direction"** if f_direction ≥ 0.5 and f_scale < 0.5;
  - **"both"** if both ≥ 0.5;
  - **"neither"** if both < 0.5. The lock then lies in the states people reach (dynamics), not in single choices.
- f_none is reported as the check of the method. If f_none < 0.5, single choices do not explain c0's change, and the
  reading is labelled "dynamics dominate".

**Described:**
- **saturation:** the share of all q entries with |q| ≥ 1.49 at year ends, adults, v13 and c0;
- **the habit term's weight:** the share of decisions whose top option changes when h is removed;
  mean |h| ÷ mean |s − h|;
- **the look-ahead term at learning**, 0.8 × max next q, by action learned and by the next week's food band.

## Part B: where remaking fails (world-new kinds made in play, first made in years 130–165; AF1's rule)
**Each kind is followed for 5 years in its inventor's weeks.** At each week's end, while the inventor lives:
- recipe still held;
- inputs in hand (`can_make`);
- not already holding one of the kind;
- valued above 0.05 (`itemval`). The make choice offers only recipes valued above 0.05, and none already held at that
  value (`acl/mind.py`, lines 300–321).

**At each decision:** whether a make option for the kind was offered. And whether it was made again by the inventor.

**Stages (furthest reached):**
0. lost at once (recipe gone by the first week's end, or the inventor died);
1. held the recipe, but never with its inputs in hand;
2. held both, but never while free and valuing it;
3. free and valuing it, but never offered (another recipe ranked first);
4. offered, never chosen;
5. remade.

**Also:**
- share of others who ever learned the recipe;
- weeks until the recipe was lost.

**Primary B:** the stage with the largest share of kinds lost, in v13 and in c0, with 95% intervals (paired world
bootstrap). **Decided before data, the first R target:**
- **stage 0:** recipe memory (rules review R1);
- **stage 1:** opportunity, or an intention to gather for a past success;
- **stage 2:** the "already holding one" and value rules;
- **stage 3:** the single-offer make rule (rules review R3);
- **stage 4:** valuation, at choice.

## Validity (hard stops)
- **Zero checks:**
  - the observers leave the world unchanged in both arms (hash with and without them, 20 and 60 years);
  - c0 acts;
  - in a world where no other code writes q, q_r + q_f = q wherever q was never clamped (exact).
- **All 2 × 32 worlds** are present under one `code_v13` fingerprint.
- **A smoke run** before the cloud.
- **A blind recompute** by GPT and Gemini (DeepSeek too) of the primary A recoveries and the primary B stage shares.

## Known limits (stated before data)
- The counterfactual versions re-score **single decisions** in the states people actually reached. They do not let
  the world unfold differently, so a "neither" reading points to dynamics, not to "no effect".
- The value test for an offer is approximated by `itemval` > 0.05. The real rule also uses beliefs and puzzles.

## The assistant's prior
1. **Saturation is common** in v13 (a third or more of used q at the clamp) and rare in c0.
2. **Reading A: "both"**, with scale stronger.
3. **Part B:** stage 0 or 1 dominates. Stage 0 is more likely in v13; stage 1 or 2 in c0.

## Sign-off (5 November 2026)
The assistant, under sleep-mode autonomy. Read-only. Council round 63: GPT 97%, Gemini 95%, DeepSeek about 93%; the
assistant 75%. Frozen as `LD1-frozen` before any code or data.

## Amendment 1 (5 November 2026, 11:26; before any data): the "direction" version is the same as "none"
**Found in the smoke run:**
- The "direction" version scored each option as s − h + 0.6 × (q_r + the mean of q_f over the situation's actions).
- Its last term is the same for every option of a decision, and a softmax ignores any amount added equally to every
  option.
- So "direction" gave exactly the same probabilities as "none" (s − h + 0.6 × q_r).

The look-ahead's *level* never affects a single choice; only its *differences between actions* do. The primary A
rule as frozen could not separate the two mechanisms. It is amended before data:
- **Versions:**
  - actual;
  - **scale**: s − h + 0.2 h, all habit differences shrunk to the no-look-ahead scale;
  - **none**: s − h + 0.6 × q_r, the look-ahead's differences between actions removed.

  "direction" is dropped.
- **Primary A reading (make share; recoveries f as before):**
  - **"direction"** if f_none ≥ 0.5. The look-ahead's differences between actions explain at least half of c0's make
    share, within single choices.
  - **"scale"** if f_none < 0.5 and f_scale ≥ 0.5. The habit's overall weight matters, not the look-ahead's
    differences.
  - **"dynamics"** if both are below 0.5. The lock lies in the states people reach.
  - If both are ≥ 0.5, the reading is "direction", and that the scale also recovers is reported.
- **Added, described:** at decisions where a make option is offered, 0.6 × (q_f of make − the mean q_f of all offered
  options), and the same for q_r. The sign of the first shows whether the look-ahead lowers making against the other
  choices of the moment.
- The zero checks are run again on the amended runner. The recompute prompt is amended the same way.
