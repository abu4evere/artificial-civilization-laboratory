# PB2: The episodic brain helps choose — a test in a copy of nature (frozen plan; the brain road, step 3)

**A nature-change test in a copy:** `code_pb2` = `code_v13` + the settings below; with `brain` = 0 it is v13 exactly.
Nothing goes live except by the safe path (a final supported study, recomputes, a confirmatory run on new seeds,
council, zero checks, tests).
- **Why:**
  - PB1b (final): an episodic memory that also learns from watching others (E-obs) predicts the effects of actions
    better than the habit table;
  - PB0: steering by today's reward alone makes people social, not inventive;
  - AM1 and AM2: habits suppress gather-then-make chains (about 7.7 times);
  - council round 61 (`docs/debate_round61_pb2_2026-11-04.md`).
- **What it asks:**
  - Does choosing by the memory's prediction of one's own learning signal (instead of the habit table) change what
    people do?
  - Does a self-chosen goal, picked by learning progress, help them **finish what they start**, beyond steering alone
    and beyond random goals?

## The brain (in the copy; general abilities only)
1. **Memory (from year 100, empty at the start):** each adult keeps PB1b's E-obs memory.
   - It holds their own weeks (PB1's decision-time inputs, action, situation index, the 9 observable changes, **and
     the week's learning signal r** = reward + 2 × mood change).
   - It also holds the visible weeks of people they see. These carry no r, since others' feelings are not observable.
   - At most 1,000 observed entries per action are kept.
2. **r̂ for an option:** the memory's estimate of r for that action and target, from **own entries only**: the exact
   (situation, action) cell's mean if lived, else the 8 most similar own weeks with that action (PB1b's distance).
   - If the person has no own week with that action, there is no r̂.
3. **Steering (arms P, G, G0):** in `mind.decide`, the habit term `learned_weight × q[situation, action]` becomes
   `learned_weight × r̂ₛ`.
   - **r̂ₛ** is r̂ put on q's scale: (r̂ − mean r̂) ÷ sd(r̂) × sd(q) + mean(q). Means and spreads are running, per
     world, over the decisions made so far with the brain.
   - Where there is no r̂, q is used as now. The share of such fallbacks is reported.
   - Everything else is unchanged: the written pulls, curiosity, the softmax and its temperature. Habits are still
     learned. They just steer only in the fallback.
4. **A self-chosen goal (arm G):**
   - **The goal outputs (7):** food gained, net food, health, energy, materials held, things held, affection.
     **"A new kind made" and distance are excluded:** invention is never a goal dimension (round 61).
   - **Learning progress (LP)** of an output is the mean absolute standardised prediction error of the memory on that
     output over the person's last 26 own weeks, subtracted from the same over the 26 weeks before.
   - **Choosing:** at the start of each season, if the person has no goal, they adopt the output with the highest LP,
     **if that LP > 0.05**. The **direction** is the sign of the correlation, in their own memory, between that
     output's change and r (+1 if undefined).
   - **Keeping it:** the goal is kept until a season's LP on it is ≤ 0, or for 4 seasons at most. At most one change
     per season.
   - **The bonus:** an option whose memory-predicted change in the goal output × direction is > 0 gets
     **+0.3 × curiosity gene × (1 − hunger)** to its score. That is the size of v9's curiosity pull; no new weight.
5. **G0 (the ablation):** as G, but each new goal's output and direction are drawn at random. The draw comes from a
   private generator seeded by (world seed, person, week), never the world's.

## Arms (32 paired seeds **23201–23232**; LP: 80 founders, 80 × 80; 170 years; brain from year 100)
| arm | `brain` | |
|---|---|---|
| **c** | 0 | v13. A **shadow** memory (read-only, `brain_shadow` 1) scores r̂ against q as predictors of r: the validity check |
| **P** | 1 | r̂ replaces q |
| **G** | 2 | P + a learning-progress goal |
| **G0** | 3 | P + a random goal |
| **sham** | 0 | v13 with `sham_draw` 1 |

## Measures (adults 16–49, years 130–170; population beside every measure)
- **Primary: M3**, AM1's ends-directed chains, unchanged: P(made a recipe using material m within 8 weeks | gathered
  m, a needed input of a valued recipe, holding < 1) − P(made | an opportunity-matched week).
  - **The contrasts:** **G − P** (goal over steering) and **G − G0** (learning progress over random goals). Each has a
    paired world-bootstrap interval (10,000 replicates, NumPy seed 20261114).
  - **The reading:** **"a self-chosen goal helps people finish what they start"** if both intervals lie wholly
    above 0.
  - **P − c** (steering) is reported with its interval as the steering effect.
- **Co-primary: R**, AF1's lineage remaking: the share of world-new kinds first made in years 130–165 whose recipe is
  made again within 5 years. Contrasts as for M3. With intent tests 1–3:
  1. **above chance:** remakes by the inventor against matched non-inventors who held the inputs;
  2. **preparation:** the share of remakes preceded within 8 weeks by gathering an input;
  3. **persistence:** M5, the chains whose next decision was a food action.

  "M3 up, R null" is a real finding, not a failure.
- **Guards first** (G, P and G0 each against c):
  - living-weeks ratio below 0.90 with its upper bound below 1;
  - or 3+ extra extinct worlds.

  A guard raised means "harm: investigate"; the arm is not read as a success.
- **The validity check (arm c's shadow):** prequential squared error of r̂ against the habit q's own estimate (q of the
  chosen action) as predictors of the week's r.
  - If r̂ is not better (interval), P and G are reported as **"not a test of predictive steering"**, and their effects
    are described only.
- **Described:**
  - PB0's warning: the action shares in P and G against c (a shift to social acts);
  - M2 and M5;
  - goals: which outputs and directions are adopted, how long they are kept, LP at adoption;
  - fallbacks to q;
  - makes per adult-year and kinds;
  - food and survival;
  - people born after year 100 apart from the others.

## Validity (hard stops)
- **Zero checks:**
  - `code_pb2` with `brain` 0 = `code_v13` (20 and 60 years);
  - the shadow memory is read-only (arm c with `brain_shadow` 1 = without);
  - P, G, G0 and the sham act;
  - reload is exact with the brain on (memories and goals are saved);
  - **unit checks:**
    - with no own week for an action, the score uses q exactly;
    - the goal outputs never include "new kind" or distance;
    - G0's draws never touch the world's random state.
- **All 5 × 32 worlds** are present under one `code_pb2` fingerprint.
- **A timed smoke run** before the cloud, to size the chunks.
- **A blind recompute** by GPT and Gemini of the M3 contrasts, the guards and the validity check.

## A known limit (stated before data)
q carries a one-step look-ahead (max over next week's habits) and r̂ does not. P − c therefore mixes "a better
predictor" with "no look-ahead" (DeepSeek, round 61). G − P and G − G0, the primary contrasts, are not affected,
because P, G and G0 all use r̂.

## The assistant's prior
1. **The validity check passes:** r̂ predicts r better than q.
2. **P shifts people toward social acts** (PB0), and M3 changes little.
3. **G − P > 0 on M3, but G − G0 is not clear.** Any goal may help as much as a learning-progress goal.
4. **R stays near 0 in every arm.**
5. **No guard is raised.**

## Sign-off (5 November 2026)
The assistant, under the creator's direction (the brain first), the 2 November permission to edit world rules (tests
in a copy), and sleep-mode autonomy. Council round 61: Gemini 90%, DeepSeek about 72%; the assistant 55%. Frozen as
`PB2-frozen` before any code or data.
