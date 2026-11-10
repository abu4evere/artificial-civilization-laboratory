# Council round 83: NB2, the answers (10 November 2026)

The question is in `debate_round83_question_2026-11-10.md`. Each model got it in a fresh chat. These are opinions, not
sign-off, and are recorded only from the actual replies.

## GPT (Thinking, medium; chat `6af34a40`)
- **Vote:** proceed with NB2, but keep "the network gets control" separate from "the network learns better". The
  question: "When the inherited instincts stop making the important decisions, can the network learn to make them and
  pass that ability across generations?"
- **(a) The diagnosis is right.** Missed:
  - the gradient must follow the real combined policy; keep the temperature in the math, and control the step by the
    learning rate and clipping, not by deleting 1/T;
  - partial observability: features must be what the person can perceive or remember, not omniscient state;
  - keep learned weights out of inheritance;
  - a better critic cannot fix a reward that does not reward long-term survival or parenting;
  - the −0.30 correlation alone does not prove failure; interventions decide.
- **(b) Priority:** many targets with physical-only limits; raw observable features (both inseparable); actor–critic;
  social learning; candidate-generation engineering.
  - **Arms (paired seeds, 16 or better 32, 600 years):**
    - C, the old brain;
    - S, NB1 as a sham;
    - O, new options and features with NB1's learning;
    - L, O plus actor–critic;
    - N, L plus social learning (the full NB2);
    - Z, N with learning off.
  - Plus a learning-off common garden for generations 1 and 18.
- **(c) Candidate targets:**
  - up to 4 valid targets per action: for places, the 2 nearest, 1 from another direction or distance band and 1 at
    random; for people, prey, recipes and items, up to 4 sampled *without* the old ranking; always a rest option;
  - re-sample each decision, and log coverage;
  - features per option: action type, distance, energy cost, resources seen, water, danger, weather, prey, ingredients,
    item properties, and the person's need, relationship, trust and strength, with a mask for missing fields;
  - do not feed the instinct score to the network; one shared option-scoring network.
- **(d) Learning rules:**
  - γ = 0.95 per week, GAE λ = 0.90;
  - a critic with a separate 16-unit hidden layer;
  - actor learning rate 1e−4, critic 5e−4, gradient clip at norm 1.0;
  - 16-week rollouts, bootstrapped; reward and temperature unchanged;
  - social learning: Δθ = 1e−5 × ∇ log π(observed action | s), one per qualifying observation, at most one per week;
  - children imitate their carer; others imitate a successful forager only when the outcome is seen;
  - no hidden knowledge passes with the imitation.
- **(e) Instincts:** keep g evolvable from 0 to 2; do not force it down. "An inborn prior is biologically reasonable."
- **(f) Primary outcome:** survival to 16, N against Z (learning off), paired.
  - **Network control also needs:**
    - zeroing the network at evaluation loses much;
    - g = 0 at evaluation keeps learned behaviour;
    - generation 18 beats generation 1 in a learning-off garden;
    - choices follow target features where the instinct ranking differs.
  - **Strongest test:** generation 18 against generation 1 genomes in a new place, with g = 0 and learning off.
- **(g) 35%.** Biggest risk: too little useful learning signal for delayed behaviours (storing food, protecting
  children, keeping tools). A feedforward network gives reactive intelligence, not planning. Leave memory to NB3.

## Gemini (3.6 Flash, high; chat `938ce93cd3b18a46`; the Pro model was not offered today)
- **(a) The diagnosis is right.** Missed:
  - the one-week horizon cannot credit work that pays over months;
  - **exploration lethality:** without the thresholds, early random choices may kill many children before learning
    converges;
  - the option list could explode.
- **(b) Priority:** sight and targets, then actor–critic, then threshold removal, then social learning.
  - Test as one package first, with ablations: the old brain, NB1, NB2 full, NB2 without social learning, and NB2
    with REINFORCE instead of actor–critic.
- **(c) At most 25 options:**
  - movement and foraging: 8 adjacent tiles plus the 4 richest in sight;
  - social: the 4 nearest people;
  - making: 3 feasible items;
  - always rest.
  - Features: self (energy, health, age, capacity, mood, social need), option (distance, resource or prey, the target's
    need, stash, trust, grudge, strength ratio, kinship) and context (season, temperature, daylight).
- **(d) Learning rules:**
  - γ = 0.95;
  - a critic of two hidden layers of 32;
  - advantage = TD error;
  - imitation by cross-entropy toward the carer's policy, strength 0.20 for infants, falling to 0 at 14.
- **(e) Instincts:** let g evolve freely to 0; g → 0 would be direct proof.
- **(f) Primary outcome:** an index, survival to 16 × (1 − g/2).
  - **Proof:**
    - g below 0.25 by year 600;
    - the population, survival, starvation and child deaths match the old brain;
    - in a garden, learning off collapses survival, while g = 0 costs nothing.
- **(g) 65%.** Biggest risk: exploration lethality in early generations, which could start extinction cascades.

## DeepSeek (chat `0d16681d`)
- **(a) "Largely right.** NB1 is not a fair test of a neural brain." The −0.30 correlation alone is not decisive; it can
  come from the pre-chosen targets. Missed:
  - **the thresholds are also action priors and safety rails;** removing them all at once may collapse viability and
    select for high g;
  - the exploration policy is unspecified (entropy or epsilon);
  - the sham must control for extra options, compute and randomness;
  - g and learning are confounded (gardens with g fixed, learning on and off);
  - the pre-chosen targets also make social learning nearly impossible.
- **(b) Fixes 1–3 are prerequisites, fix 5 is the main learning fix, and social learning is secondary.** Do not run a
  32-cell factorial. Arms (16 worlds each):
  - the old mind;
  - NB1 frozen;
  - a sham NB2 (same options, features and architecture, learning rates 0, g evolving);
  - A = fixes 1–3 with the old REINFORCE;
  - A + B = A plus actor–critic;
  - A + B + C = the full NB2;
  - A + C if the budget allows.
- **(c) A fixed k per action:**
  - forage 3 nearest visible food tiles, hunt 3 nearest prey, drink 2 nearest water;
  - give, take, steal, attack and care: 3 nearest eligible people each; mating: 3 nearest eligible;
  - all recipes; explore 3 frontier tiles; verb-only actions once;
  - about 30–40 options in all, ranked by distance and visibility only, never by the old utility;
  - state and option features much as proposed, with a feasibility mask; the instinct score never as an input.
- **(d) Learning rules:**
  - a softmax at fixed temperature 1.0, with an entropy bonus of 0.01;
  - a critic as a separate MLP with 16 hidden units; γ = 0.95, 5-step returns;
  - learning rate 1e−3, clip 1.0, weekly updates;
  - social learning: cross-entropy toward the carer's action, weight 0.10 while a child; toward a person whose
    weekly reward is ≥ 0.5 SD above the observer's mean, weight 0.05;
  - no habit-table writes.
- **(e)** Allow g to reach 0, but do not force it: an evolvable newborn prior, and selection decides.
- **(f) Primary: viability over 600 years.** Extinction no worse than the old minds; population and survival to 16
  kept against the sham.
  - **Mechanism:**
    - g falls clearly (for example to ≤ 0.6);
    - in a garden, learning on − off is larger than NB1's and above 0;
    - generation 18 beats generation 1;
    - removing social learning hurts.
- **(g) 55%.** Biggest risk: removing the thresholds and widening the options collapses child survival, so selection
  keeps g high and the network never gets a stable learning signal.

## Where they agree (the assistant's summary)
- **The diagnosis is right** (all three), and the −0.30 correlation alone proves nothing (GPT, DeepSeek).
- **Options and sight first,** as one inseparable step: every action gets real targets, chosen by distance or at
  random, never by the old ranking. Then the actor–critic, then social learning.
- **Test with ablation arms, not one package alone:** the old mind, NB1 or a sham, options only, plus actor–critic,
  plus social learning (full), and full with learning off.
- **γ = 0.95 per week,** and a separate critic (16 or 32 hidden units).
- **Keep g evolvable from 0 to 2; don't force it down.** Gemini would read g → 0 as proof; GPT and DeepSeek prefer
  behavioural tests.
- **The strongest test (GPT):** generation 18 against generation 1 genomes in a learning-off garden with g = 0.
- **The shared biggest risk:** taking away the thresholds may let early random choices kill children (Gemini,
  DeepSeek), or the learning signal is too weak (GPT).
- **Probabilities:** GPT 35%, Gemini 65%, DeepSeek 55%.

## Where they differ
- **Imitation strength:** GPT 1e−5 per observation (gradient step); Gemini 0.20 falling to 0 at 14; DeepSeek 0.10 for
  children, 0.05 for adults (loss weights).
- **The temperature:** GPT keeps it in the gradient; DeepSeek sets the temperature to 1 with an entropy bonus.
- **Options per action:** GPT 4; DeepSeek 3; Gemini about 25 in total.
