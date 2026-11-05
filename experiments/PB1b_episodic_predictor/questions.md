# PB1b: A shadow brain with episodic memory — does remembering similar weeks generalise? (frozen plan; the brain road)

**A read-only study on live nature v13**, like PB1. The predictors live in the observer, steer nothing and change
nothing.
- **Why:** PB1 (final): a fixed-step linear learner lost to the table of the person's own averages (−0.20). Round 60
  (`docs/debate_round60_learning_rule_2026-11-04.md`): all three AIs chose an episodic memory and a two-part gate.
- **What it asks:** does a memory of lived weeks, which uses exact averages where it has them and similar weeks where
  it does not, predict what a person's actions do in combinations they have never lived, better than the table, while
  doing no worse where the table already knows?

## Kept unchanged from PB1 (`experiments/PB1_shadow_predictor/questions.md`, with its amendments 1 and 2)
- The worlds design (v13, LP, to year 120; people born in years 60–100, followed as adults).
- The decision-time inputs, the 9-output vector, standardisation (running past-only spread with the floor of 0.05,
  clip ±10), prequential scoring and the burn-in.
- The case definitions (unfamiliar (situation, action) pairs among common actions; unfamiliar property combinations;
  rare actions; unfamiliar destinations; weeks-lived bands).
- Observation with the actor's state, action and visible outputs; hidden inputs replaced by the observer's running
  means and flagged; hidden outputs left out.
- **The table B** (the baseline): per (situation, action) means, with the action-mean fallback.
- **New seeds:** 32, **23101–23132**.

## The episodic predictor E
- **The memory:** each entry is one week: (the distance inputs, the action, the raw 9-output vector, a weight).
  - Own weeks have weight 1.
  - Observed weeks have the variant's weight; their hidden outputs are missing and are averaged only over the entries
    that have them.
- **Prediction for a week with action a and situation s:**
  1. **if the person has lived (s, a) before:** the weighted mean of the memory's entries in that exact cell, the
     table rule. For E-own this equals B exactly;
  2. **otherwise:** the weighted mean of the **k = 8 most similar entries with the same action a**, each weighted by
     (entry weight) ÷ (distance + 0.05);
  3. **if no entry with action a exists:** B's fallback.
- **The distance:** a weighted Euclidean distance over five input groups, each **group's mean squared difference
  counting equally**:
  1. body: food weeks, health, energy, thirst;
  2. setting: season, rain, people in reach, partner, dependents;
  3. the own tile: plants, water, fire, the 8 materials;
  4. held things: best edge, reach, hardness, containment, and the count;
  5. the target's properties.

  Age band, sex and recent actions are left out (DeepSeek). The inputs are already on fixed 0–1 ranges. **Nothing in
  the distance is learned.**
- **Memory capacity:**
  - all own weeks are kept;
  - observed entries are kept up to **1,000 per action per person**, the most recent (a ring buffer). That is a
    plain limit on what one memory holds, fixed here.

## Variants
| variant | memory | role |
|---|---|---|
| **B** | the table | the baseline |
| **E-own** | own weeks | **the primary predictor** |
| **E-obs** | own + observed weeks; each observed week weighs 1 ÷ (the number of visible observed weeks that observer had that week) | described; preferred for PB2 if it passes the gate and beats E-own |
| **E-obs-0.5** | own + observed at 0.5 each | described |
| **L-obs-0.5** | PB1's best variant (linear, rate 0.1, observed at 0.5), rerun on the new seeds | the reference |

E-own is also evaluated at k = 5 and k = 15, from the same distances. This is described only and never chosen on.

## The gate (frozen; round 60)
For E-own against B:
1. **Unfamiliar cases** (the primary cases of PB1): skill with a world-bootstrap 95% interval **wholly above 0**.
2. **Familiar cases** (own weeks whose (situation, action) was lived before): skill with the interval's lower end
   **≥ −0.02** (non-inferior).

Bootstrap: 10,000 replicates, NumPy seed 20261113.

**The reading:**
- **GO to PB2 with an episodic memory** if both hold;
- **"memory without generalisation"** if (2) holds but not (1);
- **"not yet"** otherwise.

For E-own, (2) holds by construction (the exact cell is B's mean), so the gate turns on (1). For E-obs, both parts
are real tests.

## Described
- Every variant against B on every case type, with intervals.
- Skill by output.
- The learning curve.
- The distance to the nearest memory (unsupported predictions).
- k = 5 and k = 15.
- E-obs against E-own on unfamiliar cases.
- Followed adults, prequential weeks, observed entries, population.

## Validity (hard stops)
- **Zero checks:** as PB1:
  - read-only over 20 and 60 years;
  - prediction before update, applied to the 60-year world;
  - E-own's errors the same alone as beside the other variants;
  - reload is exact;
  - plus **a unit check: on lived cells, E-own's prediction equals B's** (60-year world).
- **All 32 worlds** are present under the `code_v13` fingerprint.
- **A blind recompute** by GPT and Gemini of the gate (both parts) from per-world sums.

## The assistant's prior
1. **GO:** E-own beats B on unfamiliar cases. Similar weeks under the same action predict better than that action's
   plain average.
2. **E-obs is better still on unfamiliar cases,** and non-inferior on familiar ones.
3. **The gain is largest for food and materials,** the outputs where L-own lost most.

## Sign-off (4 November 2026)
The assistant, under the creator's direction (the brain first) and sleep-mode autonomy (the creator, 20:18: "u can use
my pc now at full capacity"). It is read-only. Round 60: GPT (A first), Gemini 92%, DeepSeek about 72%; the assistant
70%. Frozen as `PB1b-frozen` before any code or data.
