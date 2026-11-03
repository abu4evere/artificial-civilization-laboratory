# Measuring autonomy before redesigning action: a draft for the council (2 November 2026)

**Why now:**
- **DeepSeek's first reply** (`docs/deepseek_intro_2026-11-02.md`): the action architecture, one of 19 purpose-named
  actions a week with targets mostly picked by formula, is the real barrier to Bob's autonomy. It said: "the council
  should at least develop the measures and validation approach for general verbs in parallel".
- **Round 51 agreed to start it now, read-only:**
  - GPT: "distinguish novel action sequences from genuinely new action capabilities. Diversity alone is not autonomy";
  - DeepSeek: the measures must first show that they tell v11 apart from a deliberately more constrained control.
- **It builds on** `docs/research/measuring_autonomy_2026-11-02.md` (published measures, abstracts read) and SC1's
  scorecard.

**What this is:** a draft, not a frozen plan. Nothing is run. The council will be asked about it in round 52.

## Three levels, kept apart (from the research note)
- **A. Self-driven behaviour:** does a person's own past predict their next choice beyond their situation?
  - The measure is G-autonomy-style (Seth 2010; Bertschinger et al. 2008).
  - SC1 already found a real personal style, so A is measurable today.
  - **The caution:** strong habits also score high on A.
- **B. Self-chosen goals:** does a person hold an end across weeks and organise actions toward it (autotelic agents,
  Colas et al. 2022)? Today nothing in the code stores a goal. Any B signal must come from behaviour.
- **C. Power over the world:** how much can a person's actions change what they will later perceive? This is
  empowerment (Salge et al. 2013), and it is costly to measure. It is a measure of cumulative capacity rather than of
  choosing goals.

## Candidate measures (each per adult aged 16–49, years 100–200, with the population beside it)
1. **M1, self-prediction gain (A).**
   - **What it is:** the cross-validated gain in log-likelihood of the next action when the person's own last k
     actions are added to a predictor that already has the situation (the 32 contexts × season), age and temperament.
   - **What it shows:** whether choices carry a personal trajectory.
2. **M2, sequence variety (A/B boundary).**
   - **What it is:** the entropy rate of a person's action 3-grams, against the same person's actions shuffled in time.
   - **What it shows:** structure in what follows what, beyond how often each action is done.
3. **M3, ends-directed chains (B).**
   - **What it is:** the share of "make" actions whose inputs were gathered, taken or received **by the same person in
     the previous 1–8 weeks** for that recipe, against a baseline with the person's weeks shuffled.
   - **What it shows:** steps toward an end, held across weeks.
   - The same is measured for other chains: setting food down, then taking it back in a hungry season; walking toward
     water before thirst.
4. **M4, new targets (capability, GPT's point).**
   - **What it is:** the share of choices whose target was never chosen before by that person or anyone they watched:
     a new place, a new partner for an act, a new recipe.
   - **The split:** new targets inside the existing menu, kept apart from new *kinds* of act (which cannot happen in
     v11 and would be 0 by construction).
5. **M5, persistence against interruption (B).**
   - **What it is:** after a chain in M3 is interrupted (for example by hunger), how often it is resumed within 4 weeks,
     against the shuffled baseline.
   - **What it shows:** a goal kept, not a habit repeated.

## Validation (DeepSeek's condition): each measure must tell apart worlds that differ in autonomy by construction
- **Proposed controls, each a copy of v11 with one existing setting changed (no new code in nature):**
  - **"No learned habits":** `learned_weight` 0. Choices come from instinct and the situation only. M1, M3 and M5
    should fall.
  - **"Fewer acts":** stage E0-C instead of E0-D (no make, play, heat or fill). M3 should fall to 0, as a check of the
    measure, not of people.
  - **"More chance":** `choice_temperature` raised from 0.2 to 0.6. M1 and M3 should fall, and M2's shuffled gap
    should shrink.
- **The rule (to be frozen):** a measure is **validated** if v11 − control has a paired-bootstrap interval above 0
  for the control it is meant to detect. A measure that does not separate them is dropped before it is used to judge
  any redesign.
- **The caution:** the controls change the world's history, population included. Each measure is reported per adult
  and against its shuffled baseline, so that population and activity levels do not pass for autonomy.

## Questions for the council (round 52)
1. Are M1–M5 the right first set? What is missing, especially to tell "new capability" from "new combination"?
2. Are the three controls sound? Is "more chance" a fair less-autonomous control, or could randomness look like freedom?
3. Should this be a read-only study on v11 now, or wait for v12 (FX1) so that it is the baseline for the redesign?
