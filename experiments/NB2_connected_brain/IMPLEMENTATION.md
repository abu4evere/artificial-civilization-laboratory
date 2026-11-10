# NB2: implementation readings (written before any data)

How `patch_nb2.py`, `brain_nb2.py` and the runners read the points `questions.md` (NB2-frozen) leaves open.

## The options (mind.decide, `nb_options`)
- **Places** (forage tiles; gather tile-and-material; one's own stashes):
  - up to 4 by the frozen rule: the 2 nearest, 1 drawn from those farther than the second, and 1 at random from the
    rest;
  - ties in distance are broken by the target's text;
  - repeated tiles count once.
- **The set of places in sight** is v17's own: here, home, 6 random tiles in reach and the spots heard about. So "the
  rest in sight" means that set.
- **Prey** (hunt tiles), **people** (everyone in reach, for every person action) and **recipes:** up to 4 at random.
  Each person action gets the same 4 people that week.
- **Explore:** the destination v17 draws, plus up to 3 more drawn the same way (a random land tile one reach away).
  Explore and join have no frozen limit of 4; the voyage and "back to land" options are as v17's.
- **Taking from others' stashes:** v17 looks at the first 4 tiles of `tiles` and the first stash on each. That stays;
  only the hunger threshold goes.
- **Thresholds removed** (exactly the frozen list):
  - give: the surplus rule. Giving needs food held;
  - take: hunger > 0.4;
  - steal: hunger > 0.3. The rules "q holds > 4 food", "kin < 0.5" and "not one's partner" stay, as they are not on
    the list;
  - attack: grudge > 0.15;
  - care: kin, partner or affection > 0.3. Care still needs trouble > 0, since there must be something to care for;
  - court: affection > −0.2;
  - make: the value floor and the "already held" rule;
  - "grown only" for explore, join and put. These are now offered from age 3 (not toddlers), since infants and
    toddlers cannot go off alone.
- **Not on the list, so kept:**
  - heat and fill (grown);
  - hunting (grown);
  - "animals heard about further off" (hunger > 0.3);
  - flee (only from a feared, stronger person);
  - "children 0–2 do not gather or play";
  - giving to one's own young in care (the body phase feeds them).
- **The body's limits stay:**
  - `add()` drops any option the energy cannot pay for;
  - courting needs adults of the other sex, not kin, within 15 years of age;
  - recipes need their parts (and a fire for "heat");
  - land and passability.
- **The instinct score of each offered target** is v17's own formula for that target (the utility the old brain used to
  rank them), × g, as NB1. `thought.steer` still adds its pulls before the network, as in NB1.

## The network (brain_nb2)
- **Inputs:** 64.
  - **The body:** NB1's 20 numbers, plus one's own stashes within reach (relative to need, capped at 3).
  - **The option:**
    - NB1's action one-hot, distance, person, kinship and affection;
    - the place: food on the tile relative to need, prey (up to 3), water within reach, fire, a mask;
    - the person: their food relative to their need, hunger, health, trust, grudge, strength against one's own, whether
      they are a child, a mask;
    - the action: its energy cost / 40, and whether the place was heard about;
    - the recipe: its item value (capped at 2), whether one is held, a mask.
  - **Others:** NB1's two numbers.
- **The critic** sees the body's 21 numbers. It is part of the inherited genome (founders random, its output starting
  small), mutated and inherited like the actor. What it learns in a life is not inherited.
- **Learning rates:**
  - arm o uses NB1's rule and constants exactly (η 0.01, mutation sd 0.002, baseline rate 0.05);
  - arms l and n use the frozen actor–critic constants (η 0.001, sd 0.0002, η_V 0.005).
- **The TD step.** The week's learning runs in the body phase, after the week's actions and feelings.
  - V(this) is the critic's value of the state seen at the decision.
  - V(next) is its value of the body now (hunger, tiredness and company recomputed). This is the state the next
    decision starts from, apart from the next week's weather.
  - The actor's step (δ × ∇ log π) and the critic's (δ × ∇V) are each clipped to norm 1.0, then multiplied by η and
    η_V.
- **Social learning:**
  - **A child under 14 whose carer is within reach and decided this week:** the step goes toward the carer's
    (action, target) if offered to the child, else toward the child's first option of that action. Nothing happens if
    the action is not offered.
  - **Otherwise:** the person nearby whose mood rose most *last* week. "Last week" is used so that the order in
    which people are processed in the body phase cannot matter. The step goes toward the first of one's options with
    that person's action.
  - The step is η_S × ∇ log π(that option), clipped to 1.0. There is one social step a week at most, after the
    learning step, and only when learning is on.
- **What is not saved:** the week's working records (the decision, the carer's choice, last week's mood changes) are
  not saved with the world, like NB1's. A world reloaded mid-run starts its first week without last week's social
  record. Cloud worlds run start to end, so this never applies to data. The reload check clears the records in both
  copies.
- **The gardens' fixed g** (`nb_g_fixed`) holds g for every decision. Inherited g values are kept but not used.

## The runs
- **Phase 1:** 5 arms × 16 seeds (25601–25616), 600 years, LP, on the cloud.
- **The primary's births:** people born in years 100–600 whose outcome is known (reached 16, or died before it).
  Those still alive and under 16 at the end are left out, in every arm alike.
- **Phase 2:** genomes from the n worlds' first births of generations 1 and 18 (30 each). Arms g1Z and g18Z (g held at
  0, learning off), g18L and g18N (g as inherited, learning on or off). Seeds 25701–25716; 60 years.

## Running longer than one cloud job (added before any data)
- **The need:** a 600-year NB2 world takes far longer than one cloud job's 6 hours. A profile measured about 20
  seconds per world-year at 60 people.
- **Speed:** within one decision, a place's facts and a person's facts are computed once and reused. Whether fresh
  water is in reach depends only on the map, so it is cached per map. These are read-only computations, so the results
  are unchanged.
- **Checkpoints:** `run_nb2.py part …` runs a world until its time budget is spent at a year's end. It then saves
  everything needed to continue: the world, the observer, and the brain's working records of the week. The next job
  continues from there.
  - The zero checks include "15 years in one job = 1 year, a checkpoint, and 14 more in a second job": the world, the
    brain records and every observed number are equal.
  - The observer's every-50th-decision counter is kept on the observer, so sampling stays in step across jobs.
- **The workflow `long-run.yml`:**
  - one world per job, 20 at once, on the same Windows system as `cloud-run`;
  - every stage checks the committed zero record;
  - the last job of each stage starts the next stage by itself, until all 80 worlds are finished (at most 12 stages);
  - a failed job carries forward the checkpoint it started from.
- **The gardens** (60 years) fit in one job and run on `cloud-run`.
