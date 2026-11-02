# UP1 — Why is a new kind never made again? (frozen plan)

**Read-only: no change to nature.** Live v11 (`code_v11`).
- **Its origin:** SC1 found that none of the 3,883 kinds invented in play after year 100 was made again within five
  years.
- **The exploratory check** (`../SC1_bob_scorecard/explore/`) then found that most such kinds are kept, used and
  valued, yet never remade.
- **Debate round 48** (`docs/debate_round48_up1_2026-11-02.md`): GPT 95%, Gemini 95%.
- **Uptake is the first link in any cumulative chain:** a thing nobody makes twice cannot be improved or passed on.

## Worlds
32 new seeds, 22101–22132 (used by no study). LP: 80 founders, 80 × 80, 200 years; years 100–200 counted.

## Units
- **Each unit is a person × kind × decision:** every decision of an adult (16+) who knows the kind (it is in their
  recipes).
- **New kinds:** world-new kinds first made in play in years 100–195 (operational note 1 of SC1: their five-year windows
  fit).
- **Old kinds** (the control): kinds first made before year 100, known by the same people at the same decisions.
- **Complexity:** "nested" if the recipe uses a made part (a bind with a made part, or a heat of a made thing);
  otherwise "simple".

## The funnel (the observer reproduces the make choice in `mind.decide` exactly)
At each decision, every known kind gets the **first** step that applies:

1. **Holding:** the code skips it because the person holds one with more than 5 uses left, and its value v equals its
   item value.
2. **Value floor:** v is at or below 0.05. Here v is the code's: the maximum of the item value, the value as a wanted
   part, a strike belief, and half a puzzle's pull.
3. **Cannot make:** the materials or made parts are not in hand (`can_make`), or it is a heat recipe with no fire here.
4. **Not the best make option.** Two sub-steps are recorded apart:
   - **4a, skipped by the running best:** the code skips a recipe when v ≤ the best pull found so far among the
     recipes before it, in the order they were learned. A recipe learned later is checked later.
   - **4b, beaten:** another recipe ends with the larger pull.

   Also recorded: whether the winner is an old or a new kind.
5. **Eligible but not chosen:** it is the make option, but the choice falls elsewhere. The make option's probability is
   recorded (softmax of the steered scores, temperature 0.2).
6. **Made.**

## Primary (frozen)
- **The measure:** for new kinds, the share of person × kind × decisions ending at each step (1, 2, 3, 4, 5, made),
  weighted by decisions.
- **Intervals:** a world bootstrap, 10,000 replicates, NumPy seed 20261104.
- **Reading:**
  - **"mainly blocked at step k"** if one step's share has its 95% interval's **lower bound above 0.50**;
  - otherwise **"mixed bottlenecks"**, with the shares reported.

## Secondary (described, not decisive)
- **New minus old, step by step** (Gemini). The step with the largest positive difference whose interval excludes 0
  is "the main difference from old kinds".
- **Kind-weighted shares:** each new kind counts once, averaged over its decisions.
- **Complexity:** the split by simple or nested, for new and old kinds alike.
- **Timing:** the first five years after invention, reported apart.
- **Step 4:** 4a against 4b, and whether the winner is old or new.
- **Step 5:** the mean make probability, and the eligible decisions per new kind.
- **Kinds:** the share of new kinds ever eligible (step 5 or made), and ever made within five years.

## Validity (hard stops)
- **Zero checks:**
  - the observer is read-only (state and random stream, at 20 and 60 years, with and without it);
  - **at every decision, the observer's reproduced make option equals the make option the code offered** (mismatch
    0).
- **All 32 worlds** are present under `code_v11`'s fingerprint.
- **A blind recompute by GPT and Gemini** of the primary shares, their intervals and the reading, from per-world sums.

## The assistant's prior
1. **"Mixed bottlenecks":**
   - **step 3 largest:** new kinds are mostly nested, and their made parts are rarely in hand with only 3 carried
     things;
   - **then step 1:** the inventor keeps the thing they made.
2. **The main difference from old kinds is at step 3.**
3. **Step 4a is present:** a newly learned recipe is checked last.

## Sign-off (2 November 2026)
The assistant, under the creator's sleep-mode autonomy (the creator last wrote at about 03:53). A read-only study under
the 40% rule: GPT 95%, Gemini 95% (round 48), the assistant 80%. Frozen as `UP1-frozen` before any code or data.
