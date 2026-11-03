# PB0: Would knowing what happens next change people's choices? (frozen plan; the brain road, step 1)

**A read-only study on live nature v12.** No setting changes and no nature changes. Copies of the world are run
forward beside it, and the real world never sees them.
- **Why:**
  - the creator made the brain ACL's first priority (3 November 2026: "first of everything we should work on agent
    brain");
  - council rounds 55–57 (`docs/debate_round57_pb0_2026-11-03.md`; the design draft `docs/pb0_design_draft_2026-11-03.md`).
- **What it is for:** an upper bound on what **foresight** could gain with today's menu and today's learning signal.
  It is a gate before building a predicting brain (PB1).
  - A negative result does not rule out world models, longer planning, open actions or self-made goals (GPT, round 57).

## Worlds
- **32 new seeds, 22901–22932;** v12 (`code_v12`), LP (80 founders, 80 × 80).
- **Each world runs to year 110.** Decisions are sampled in years 100–110.

## The sample (the observer's own random stream, seeded by the world seed; never the world's)
- **The main sample:** at the start of every 5th week in years 100–110, one living adult (16 and over) is drawn at
  random. Their decision that week is studied. That gives 104 decisions a world.
- **The all-options sample:** every 4th sampled decision also has all of the person's options replayed, not only the
  top K.
- **The long-horizon sample:** every 8th sampled decision is also replayed to H = 13 and H = 26 weeks.

## The method for one sampled decision
1. **The copy:** at the start of the week, before anyone acts, the world is copied (`to_dict`, then `from_dict` via
   JSON, as the reload checks do).
2. **The record run:** the copy runs the week unchanged. It records the person's full option list (scores after
   `thought.steer`) at their turn, and the option the softmax picked.
3. **The options studied:**
   - the top K = 6 by score, plus the option actually picked;
   - in the all-options sample, every option.
4. **Each option is played in its own copy.** Each copy starts from the same start-of-week copy, with the same random
   state. In the person's turn `mind.decide` runs as usual, so it draws and records as usual; then its returned option
   is replaced by the studied one. Everyone else acts as usual.
5. **Replays:** after week 1, each option's copy is copied 4 times (replays 1–4). Replay i reseeds the copy's random
   generator with a seed made from (world seed, decision number, i). The same seed is used for every option (common
   random numbers). Each replay runs to week H.
6. **The outcome:** the person's own learning signal summed over weeks 1..H, r = reward + 2 × (mood − mood at the
   week's start), as `biology._learn` uses it. Also recorded:
   - the reward and mood parts apart;
   - the person's food, health, and whether they are alive at H (a death ends the sum).

## Primary measure (frozen): held-out gain G at H = 4
- **The winner:** for each decision, the option with the highest mean outcome over replays 1–2 ("the oracle's
  winner").
- **The gain:** on replays 3–4 (held out), the winner's mean outcome minus the **top-scored option's** mean outcome.
  This is 0 when they are the same option.
- **G** is the mean gain over all sampled decisions, pooled; its 95% interval comes from a world bootstrap (10,000
  replicates, NumPy seed 20261111).
- **The scale:** A = the mean absolute outcome of the top-scored option on replays 3–4.

## Go/no-go (frozen)
- **GO to PB1** (a frozen test of a small predictor in a copy of nature) if G's 95% interval lies wholly above 0
  **and** G ≥ 0.05 × A.
- **NO-GO** otherwise. Foresight over today's menu is then not the wall, and the brain road turns first to goal memory
  and open actions (round 55).

## Described (no decision drawn from these)
- **S, a regret share:** the share of decisions where the held-out gain exceeds one noise SD. The noise SD is the SD
  of the top-scored option's outcome across replays 3–4, averaged.
- **G at H = 1** (no replay spread), and at H = 13 and 26 (the long sample).
- **The parts of the gain:** from reward and from mood (DeepSeek: flag where mood supplies the gain). Food, health and
  alive at H.
- **The all-options sample:** how often the full-menu winner (on replays 1–2) lies outside the top 6.
- **The softmax pick against the top-scored option:** the held-out gain of the oracle over the actual pick.
- **By kind:** food band; season; whether the winner is make, hunt, gather or a food action.
- **Population beside it:** living-weeks and adult-weeks in years 100–110.

## Validity (hard stops)
- **Zero checks:**
  - the observer and its copies are read-only. The real world's state and random state are the same with and without
    the observer, over 20 and 60 years, with sampling on from year 10 for the check;
  - a copy with no option forced reproduces the real world's next week exactly;
  - forcing the option the softmax actually picked reproduces the record run exactly;
  - reload is exact.
- **All 32 worlds** are present under the `code_v12` fingerprint.
- **A blind recompute** by GPT, Gemini and DeepSeek, from per-decision outcomes (top-scored and winner, replays 3–4,
  by world), of G, its interval, A and the reading.

## The assistant's prior (before any data)
1. **NO-GO, narrowly:** G is positive but below 5% of A. With 4 weeks of foresight over the same menu, the
   habit-plus-pull scores already pick nearly the best for food and rest.
2. **Where gains appear, they come mostly from mood** (social actions), not from food.
3. **The full-menu winner** lies outside the top 6 in under 10% of decisions.

## Sign-off (3 November 2026)
The assistant, under the creator's direction (the brain first) and sleep-mode autonomy. It is read-only. Council
round 57: Gemini 85%, DeepSeek about 80% after the control fix; GPT's held-out design adopted. The assistant 70%.
Frozen as `PB0-frozen` before any code or data.
