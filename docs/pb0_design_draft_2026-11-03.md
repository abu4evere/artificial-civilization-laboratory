# PB0 draft: would knowing what happens next change people's choices? (3 November 2026; the brain road, step 1)

**What this is:** a draft for council round 57, before a frozen plan. Nothing is frozen or run.
- **The source:** rounds 55 and 56 (`docs/debate_round56_bigger_brain_2026-11-03.md`). It merges GPT's "prediction
  opportunity audit" with DeepSeek's "upper-bound replay".
- **The priority:** the creator's, 3 November ("first of everything we should work on agent brain").

## The question
On v12's own decisions, how often would **knowing each option's real outcome** change which option a person should
take, and by how much would they gain?
- **If almost never:** a predicting brain buys little with today's menu. The wall is then the menu (open actions) or
  goals, not prediction.
- **If often, with real gains:** prediction has room, and a small predictor is worth building (PB1, a test in a copy).

## How a choice is made today (read in `mind.decide`, v12)
- Each option's score is a written pull plus learned habit: `u + learned_weight × q[situation, action]`, where q is
  per situation (32: 4 food bands × company × 4 seasons) × action (19).
- The pick is a softmax over the scores (temperature 0.2).
- Habits learn from `r = p.reward + 2 × (mood change)` with a max look-ahead (`biology._learn`).

## The method: an exact one-option-at-a-time look into the future (read-only)
For a sample of adults' real decisions:
1. **Take the world exactly as it is at that decision.** Copy it (`to_dict` / `from_dict`, as the reload checks do).
2. **For each of the person's top K options by score** (K = 6, plus the option actually chosen), run a copy forward
   with that option forced for that person.
   - Everyone else decides as usual.
   - Every copy starts from the **same random state** (common random numbers), so the forced choice is the only
     difference at the start.
3. **Measure the person's own outcome over H weeks** (H = 1 and H = 4; after week 1 the person decides as usual):
   - the same signal habits learn from: the sum of r;
   - also food, health, and being alive at H.
4. **The oracle's best option** is the one with the highest outcome.

## Measures
- **Primary: S, the option-shift rate.** The share of sampled decisions where the oracle's best option is not the
  person's top-scored option.
- **G, the gain:** the mean outcome of the oracle's best minus that of the top-scored option, beside the outcome noise.
- **Controls:**
  - **shuffled oracle:** outcomes permuted among a decision's options. This gives S by chance, given ties and noise.
  - **noise:** the top-scored option run twice with different random streams after the first step. If its outcome
    varies as much as G, the "better" option cannot be predicted reliably.
- **By kind of decision** (described): food bands, seasons, and whether make, hunt or gather were on offer. Where
  would foresight matter most?

## Go/no-go rule (to be frozen; numbers for the council to set)
**GO to PB1** if, at H = 4:
- S exceeds the shuffled control by at least 10 percentage points (95% interval wholly above);
- and G exceeds the noise SD.

Otherwise **NO-GO:** prediction is not the wall with today's menu, and the brain road turns first to open actions and
goal formation (round 55).

## Sample and cost (a guess, to check in a smoke run)
- **Worlds:** 32 new seeds, v12, LP, run to year 110 as usual.
- **Sample:** about 400 adult decisions per world in years 100–110 (every n-th decision, stratified by food band).
- **Cost:** each sampled decision needs about 7 copies × H weeks, about 3,000 world-weeks of copies per world plus
  copying. On the cloud this is probably 1–2 hours.

## Open questions for the council
1. Is a one-to-four-week oracle a fair **upper bound** for a predictive brain? Planning further (tools, stores) needs
   longer horizons. Should H = 26 be added on a smaller sample?
2. Is r (the habit's own signal) the right outcome, or should survival and food be primary? r includes mood, which is
   partly written pulls.
3. K = 6 plus the chosen option: enough?
4. The go/no-go thresholds.
