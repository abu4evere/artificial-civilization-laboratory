# NB2: connect the world to the neural brain. Can the network decide? (frozen plan)

**Frozen** as git tag `NB2-frozen`, before any code or data.
**Sign-off:** the creator, 10 November 2026, in the Claude Code session, answering "Shall I freeze NB2 and build it?": "do not
ask me go ahead bro".

**Why:** the creator, 10 November 2026: "Check the world itself laws and nature if anything against our new neural
brain fix it … we gotta stay with this brain and connect it to world not against its laws."
- **Background:**
  - NB1 (`experiments/NB1_neural_brain/findings.md`): decorative; g rose; learning hurt;
  - the audit (`docs/brain_world_audit_2026-11-10.md`);
  - council round 83 (`docs/debate_round83_after_2026-11-10.md`): GPT 35%, Gemini 65%, DeepSeek 55%. All three say
    the diagnosis is right.
- **The question (GPT):** "When the inherited instincts stop making the important decisions, can the network learn to
  make them and pass that ability across generations?"
- **Status:** an exploratory test in a copy of the frozen nature v17. Physics, biology and the feelings are unchanged.
  Nothing goes live from it.

## What changes (code_nb2 = code_nb1 + the switches below; all 0 = NB1's n arm exactly)
1. **Options are what the body can do** (`nb_options`).
   - **Targets:** up to **4 targets per action** (GPT's rule):
     - for places: the 2 nearest valid targets, 1 from a farther ring, and 1 at random from the rest in sight;
     - for people, prey and recipes: up to 4 drawn at random from those in reach.

     Never ranked by the old formulas, and drawn fresh each decision from the world's generator.
   - **Rest** is always offered.
   - **The old brain's thresholds go:**
     - give: the "> 2 × need" surplus rule;
     - take: hunger > 0.4;
     - steal: hunger > 0.3;
     - attack: grudge > 0.15;
     - care: kin or affection > 0.3;
     - court: affection > −0.2;
     - make: the value floor and the "already held" rule;
     - "grown only" for explore, join and put.
   - **The body's limits stay:**
     - the energy for the action and the walk;
     - adulthood for courting, and no kin as mates;
     - having food to give, something to take, or the parts for a recipe;
     - a hunter's age (teens and adults);
     - land and passability.
2. **The network sees the facts** (`nb_sight`). Raw numbers per option, with a mask where a fact does not apply:
   - **the place:** food on the tile, prey seen there, water within reach, fire;
   - **the person:** their food relative to need, hunger, health, stage, kinship, affection, trust, grudge and
     strength relative to one's own;
   - **the action:** the energy cost; whether it was heard about from others; the recipe's item value and whether one
     is already held;
   - **one's own:** stash nearby, and the old inputs (body, stage, season, company, others' recent actions).

   The instinct score is never an input.
3. **Learning that looks ahead** (`nb_critic`):
   - **an actor–critic:** a critic network (the same inputs without the option part, 16 hidden units) learns V(state);
   - the advantage is the TD error, δ = r + 0.95 V(next week) − V(this week). The feeling r is unchanged;
   - **the actor step:** w ← w + η δ ∇ log π(chosen), with the exact gradient (the temperature kept, GPT), clipped to
     norm 1.0;
   - **the critic step:** v ← v + η_V δ ∇V, also clipped to 1.0.
4. **Learning from others, into the network** (`nb_social`):
   - **a child under 14 with its carer in reach:** a step toward the carer's action, if that action is among the
     child's own options;
   - **anyone who sees a person nearby whose mood rose last week:** a smaller step toward that person's action, if
     that action is among their options;
   - each step is η_S ∇ log π(observed); at most one social step per person per week;
   - only actions are seen, never the other person's knowledge.
5. **Instincts:**
   - the hand-written score is computed for every offered option and stays only as an inborn bias × g;
   - **g is evolvable in [0, 2] and is never forced down;**
   - no cost or reward for any g. Only survival and children decide.

**Chosen constants** (recorded as constants, never tuned on outcomes):
- critic hidden size 16;
- discount 0.95 per week (about a 20-week horizon);
- founders' η = 0.001 (evolvable, sd 0.0002), η_V = 0.005 (fixed);
- clip at norm 1.0;
- social step η_S: for a child, 0.5 × η; for someone watched, 0.2 × η.

Everything else is as NB1: hidden 16, mutation sd 0.02, one parent's genome, nothing learned inherited.

## Phase 1: deep time (600 years, 16 paired seeds, 25601–25616; LP)
| arm | options and sight | learning | social |
|---|---|---|---|
| **c** | v17's old minds | – | – |
| **s** (sham / learning off) | new | none (η = 0) | none |
| **o** | new | NB1's REINFORCE | none |
| **l** | new | actor–critic | none |
| **n** (full NB2) | new | actor–critic | yes |

80 worlds on the cloud. The same records as NB1, plus:
- the share of choices where the network's top option differs from the instinct's top option;
- target coverage (how often each offered target was taken).

## Phase 2: common gardens (after phase 1)
- **Inherited competence (GPT's strongest test):**
  - genomes from generations 1 and 18 of each n world become all the founders of fresh identical worlds;
  - **g is set to 0 and learning is off**, so only the inherited network decides;
  - 16 seeds; 60 years.
- **Learning's worth:** the same generation-18 genomes with learning on against off (g as inherited).

## Outcomes and reading (exploratory)
- **Primary:** survival to 16 per birth (years 100–600), n against s, paired by seed, with the bootstrap as in NB1.
- **Readings:**
  - **"the network decides"** needs all of these:
    - n − s survival has a lower bound above 0;
    - n is viable against c (no more than 3 extra extinct worlds, and the population ratio's upper bound ≥ 0.80);
    - in the inherited garden, generation 18 − generation 1 survival has a lower bound above 0 (g = 0, learning off);
  - **"learning helps, but the instincts still carry it":** n − s above 0, but the inherited garden is not;
  - **"not viable"**, or else **"no improvement shown"**.
- **Secondary** (with intervals, no gate):
  - o − s, l − o and n − l: what each fix adds;
  - g's trajectory;
  - CI1's eight guards against c;
  - the share of choices where the network overrides the instinct.

## Risks, stated in advance (council)
- **Without the thresholds, early random choices may kill children** (Gemini, DeepSeek). The instinct bias × g is the
  newborn's safety net, and the sham shows its effect.
- **The learning signal may still be too weak** for delayed work (GPT).
- **A feedforward network reacts; it does not plan.** Memory is for NB3.

## The assistant's prior
- n viable: about 65%;
- n − s survival above 0: about 45%;
- the inherited garden above 0: about 25%;
- "the network decides": about 20%.
