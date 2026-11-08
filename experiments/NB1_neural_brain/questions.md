# NB1: can a neural-brained people survive and improve over generations? (frozen plan)

**The first test of the neural brain**, the creator's decision of 8 November 2026 (CLAUDE.md, Direction, step 5): "I
think our current structure is more predetermined we should go back to neural network cuz i think bob's brain will
emerge from neural network"; "go ahead now".
- **Background:** `docs/research/neural_brains_2026-11-08.md`.
- **Council round 82** (`docs/debate_round82_question_2026-11-08.md`, `docs/debate_round82_after_2026-11-08.md`):
  - GPT 85%, Gemini 80%, DeepSeek about 70%;
  - all three have no objection to this design.
- **This is an exploratory law test in a copy of the frozen nature v17.** Nothing here goes live. Any adoption would
  be a later decision, through the safe path.

## The brain (each 0 = v17 exactly)
`code_nb1` = `code_v17` + `nb_brain` (and `nb_learn`).

1. **The body stays; the decisions move to a network.**
   - Candidate options (actions, with their targets chosen by v17's rules) are built as now.
   - Each option's hand-written score (the instinct utility, plus the thought pulls of `thought.steer`) is **multiplied
     by an inherited gene g**, and the network's score is added. **The habit table q is not used.**
   - Then the softmax pick, as now.
   - The feeling that drives learning is v17's own: r = reward + 2 × mood change.
2. **The network:** about 44 inputs, 16 hidden units (tanh), one output score per option, about 737 numbers. Its inputs
   are raw features only, never the hand-written score:
   - **the body:** energy, health, food held relative to need, thirst, cold, hunger, tiredness, loneliness, mood,
     dependents, life stage, season, company;
   - **the option:** action kind, distance, whether the target is a person, and if so kinship and affection;
   - **others:** the share of people nearby whose latest action was this action, and their mean mood change.
3. **Genes:**
   - **Founders:** g = 1; random starting weights from the world's generator, the output layer small, so the network
     starts near 0 and the old instincts dominate at birth; a learning rate of 0.01.
   - **A child** inherits **one parent's whole network genome** (the parent chosen by the world's draw), with small
     Gaussian mutation of every weight. Averaging two parents' networks would scramble hidden units (GPT).
   - g and the learning rate are inherited the same way, with their own mutation; g stays in [0, 1].
   - **Nothing learned is inherited** (Baldwinian).
   - **No cost or reward for any value of g:** only survival and children decide (council point 1).
4. **Learning within a life** (`nb_learn` 1), once a week on the week's chosen option:
   - REINFORCE with a baseline: w ← w + η (r − b) ∇ log π(chosen);
   - b ← b + 0.05 (r − b);
   - weights clamped to ±5.
5. **The chosen constants are recorded as constants, never tuned on outcomes:**
   - hidden size 16;
   - weight mutation sd 0.02;
   - g and η mutation sd 0.08 and 0.002;
   - baseline rate 0.05;
   - clamp ±5.
6. **At death** a person's network is dropped (nothing reads it again), to keep deep-time worlds small.

**Limits, stated in advance:**
- target choice stays rule-based;
- no episodic memory (that is NB2);
- `thought.steer`'s pulls are scaled by g with the instincts.

## Phase 1: deep time
- **Arms:**
  - **c**, v17;
  - **n**, the neural brain with learning;
  - **e**, the neural brain without learning (evolution only; DeepSeek).
- **16 paired seeds,** 25401–25416. LP; **1,000 years**; one world per cloud job, in three launches.
- **Recorded per world** (read-only):
  - every person born: generation, birth, death, age at death, whether they reached 16;
  - yearly: population, mean and sd of g, and genetic variance of the weights (n, e);
  - at sampled decisions: the correlation between the network's score and the scaled hand-written score, and the
    entropy of the action mix;
  - CI1's guard sums over years 100–1,000.
- **Genome samples** for phase 2: the first 60 births of generations 1, 20 and 40 in each n and e world.

## Phase 2: common garden (GPT), after phase 1
- **What goes in:** genomes from generations 1, 20 and 40 of each n world are put, as all the founders, into fresh
  identical v17 worlds with the neural brain. Seeds 25501–25516, one for each source world.
- **Each world runs twice:** learning on and learning off. 60 years each.
- **What is measured:**
  - the founders' living-years;
  - births;
  - the survival to 16 of their children.

## Frozen decision rule (exploratory; no adoption follows from it)
**Viability** (phase 1):
- worlds alive at year 1,000 in n and e against c;
- population (living-weeks, years 100–1,000) as a ratio against c, by paired world bootstrap (10,000 draws, NumPy seed
  20261131).

**Primary 1, improvement within worlds** (DeepSeek):
- in n (and e), the per-world slope over generations 1–40 of survival to 16 per birth, and of adult lifespan (age at
  death of those who reached 16);
- pooled across worlds, with the bootstrap over worlds;
- **"improves" means the lower bound is above 0.**

**Primary 2, inherited improvement** (GPT; phase 2):
- **inherited adaptation:** generation 40 against generation 1, learning off, on the children's survival to 16 per
  birth, paired by source world; "yes" if the lower bound is above 0;
- **lifetime learning:** learning on against off within the same genomes.

**The g readout:** the trajectory of mean g by generation. **g falling while survival holds** means the network does
the work. **g staying near 1** means the network is decorative (the quiet-predetermination failure).

**Guards** (CI1's eight, n against c), **descriptive only:** DeepSeek's power point. 16 seeds cannot gate harm.

**Readings:**
- **"neural people viable"**: no more than 3 extra extinct worlds in n than in c, and the population ratio's upper
  bound ≥ 0.80;
- **"improves by itself"**: primary 1 or primary 2 (inherited) is yes, and g falls;
- **"decorative"**: g stays ≥ 0.9 throughout;
- otherwise **"no improvement shown"**.

## Validity (hard stops)
- **Zero checks:**
  - `code_nb1` with `nb_brain` 0 = `code_v17` (20 and 60 years, world and random stream);
  - the observers are read-only;
  - n and e act, and differ;
  - reload is exact (with networks);
  - learning off leaves the weights equal to the genome;
  - **unit checks** (a 10-year n world):
    - the network's scores equal an independent computation;
    - the learning step equals an independent gradient;
    - a child's genome is one parent's within the mutation size;
    - g is within [0, 1].
- **All worlds present** under one fingerprint.
- **The blind recompute** by GPT and Gemini of the primaries and the viability counts.

## The assistant's prior
- viable: about 55%;
- g falls clearly within 40 generations: about 30%;
- primary 1 yes: about 25%;
- inherited improvement shown: about 20%;
- most likely: "decorative" or "no improvement shown". This is a first step.

## Sign-off (8 November 2026)
- The creator decided the direction and said "go ahead now".
- The design is the assistant's, after council round 82; all three have no objection.
- Frozen as `NB1-frozen` before any code or data.

## Amendment 1 (8 November 2026, before any data)
**g's range is [0, 2], not [0, 1].** A 3-year code test (not data) showed mean g already at 0.988. Founders start at g = 1, the top of [0, 1], so mutation could only lower it. That drift would mimic the very readout "g falls". With [0, 2], mutation from 1 is symmetric, and only selection can move the mean. Everything else is unchanged.

## Amendment 2 (8 November 2026, before any data): 600 years, generations 1, 12 and 24
**The cloud cannot run 1,000-year worlds within its limit.**
- **The evidence**, cloud speed, not outcomes: VW1's cloud run (42439579177) took about 50 minutes per 200-year world when 4 worlds shared a chunk. That is about 15 seconds per world-year.
- **The network** adds about half again (measured locally: 12 seconds against 8 for 3 years).
- **The cost:** a 1,000-year neural world would need about 6 hours. A cloud job stops at 340 minutes.

**So NB1 runs 600 years** (about 27 generations):
- the guard and population window is years 100–600;
- primary 1's slope is over generations 1–24;
- the common garden uses generations **1, 12 and 24** in place of 1, 20 and 40.

**This is below the council's 1,000 years.** If NB1 shows a signal (g falling, or a positive trend), a longer follow-up (checkpointed across jobs) is the next step, as GPT suggested for 3,000–5,000 years. Everything else is unchanged.

## Amendment 3 (8 November 2026, before any data): generations 1, 9 and 18
**The zero checks** (not data) showed a mean generation of only 1.9 at year 60 (seed 601). That is about 31 years per generation. So 600 years give about 19–20 generations, not 27, and generation 24 might never be reached.
- The common garden uses generations **1, 9 and 18**.
- Primary 2 is **generation 18 against 1**.
- Primary 1's slope is over generations **1–20**.

Everything else is unchanged.
