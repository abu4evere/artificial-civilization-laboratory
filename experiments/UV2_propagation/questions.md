# UV2 — Does the habit floor come from unpractised choices further ahead? A read-only replay of ES2's r arm (frozen plan)

**Read-only: no change to nature.** Live nature stays v11. UV2 replays ES2's r worlds exactly (`code_es2`, unchanged,
`realized_lookahead` 1) with a wider observer.

## Why
- **UV1** (final, persistent bias): under the realized look-ahead, habits practised 80 times or more are still valued
  below what follows. B = −0.108 [−0.111, −0.105] at ages 16–44, against −0.207 at k 0–19. Practice halves the
  under-valuation within about 20 updates; then a floor stays.
- **The leading candidate, propagation:**
  - A habit's target is r + 0.8 × the choice-weighted value of the next decision's options.
  - If some of those options are unpractised, still start-lagged, they pull the target down.
  - Through the chain, even practised next options carry the floor.
- **Debate round 41** (`docs/debate_round41_propagation_2026-11-01.md`): both models chose this test first (GPT 88%,
  Gemini 95%).
  - The council found that a one-step test cannot detect propagation through the chain.
  - Both accepted the discounted version below (GPT 91% with one change, adopted; Gemini 98%).

## The question
Among practised habits, is the under-valuation gone when the person's discounted future choices are almost all among
well-practised options? Or does the floor stay even then?

**What it can and cannot show** (GPT): an association. "Propagation" means evidence consistent with propagation, not
proof. "Not propagation" means propagation is not enough to explain the floor, not that it contributes nothing.
Exposure may go with circumstances, which the secondary tables describe.

## Design
- **Worlds:** ES2's arm r only (`realized_lookahead` 1), the same 32 seeds 21501–21532, LP (80 founders, 80 × 80), 200
  years, the same code and settings. 32 worlds. v11 is not replayed: its look-ahead is the max, not the options.
- **The observer:** UV1's observer, unchanged (k, age, death-closed), plus the following.
  - **Unpractised mass U at each decision** where a held update is completed:
    - the choice-probability mass on options whose habit (that situation and action, the exact q entry) the person
      had updated **fewer than 20 times**;
    - the probabilities are the choice's own softmax over the options' scores at the choice temperature, as the
      look-ahead uses them;
    - with no options, the look-ahead is rest's value, so U = 1 if that habit has fewer than 20 updates, else 0.
  - **Discounted exposure D** for each update t: D_t = Σ_j w_j U_(t+1+j).
    - It is accumulated in the observer **exactly as G is**: the same updates, the same weights (1, 0.8, 0.64 … per
      habit update), and the same closing (weight below 0.001, or death).
    - **Dn = D / W,** where W is the sum of the weights actually accrued (GPT): the weighted mean exposure, in [0, 1].
  - **The one-step U** (the first term) is kept for the secondary.
  - **The year quarter** of the update: 100–124, 125–149, 150–174, 175–199.
- **As in ES2 and UV1:** q is the value just before the update, and G = Σ_j 0.8^j r over the person's next updates.
  Only updates started in years 100–200 are counted.
- **Bins:**
  - **Dn:** 0–0.05, 0.05–0.1, 0.1–0.2, 0.2–0.4, 0.4–1;
  - **U:** 0–0.1, 0.1–0.25, 0.25–0.5, 0.5–1;
  - **k and age:** as in UV1.

## Primary (frozen)
- **The signed bias B = mean(q − G),** pooled as Σ(q − G) / n, over updates that have all of these:
  - k ≥ 80 (the habit is practised);
  - ages 16–44;
  - G not closed by death;
  - **Dn < 0.1** (the discounted future is almost all well-practised choices).
- **The comparison:** B over all Dn in the same updates (k ≥ 80, ages 16–44, not death-closed).
- **Intervals:** 95%, by a world bootstrap (10,000 resamples of the 32 seeds; NumPy seed 20261101).

## Frozen decision rule
- **Propagation:** B(Dn < 0.1)'s 95% interval lies inside [−0.05, +0.05], **and** |B(Dn < 0.1)| ≤ 0.5 × |B(all Dn)|.
- **Not propagation:** B(Dn < 0.1)'s whole 95% interval lies below −0.05.
- **Mixed:** anything else.
- **Coverage guard:** if the Dn < 0.1 cell has fewer than 100,000 updates, or updates in fewer than 24 of the 32
  worlds, the reading is **inconclusive**.

## Secondary (described, not decisive)
- **Dose-response:** B by Dn bin, for k ≥ 80, ages 16–44, not death-closed. Propagation predicts it falls toward 0 as
  Dn falls.
- **B by Dn bin within each k bin** (ages 16–44).
- **The one-step U:** B by U bin, for k ≥ 80, ages 16–44.
- **Year quarters:** B by quarter (cause 3, improving circumstances), and the Dn mix by quarter.
- **Age:** B by Dn bin for each age bin (all k).
- **Coverage:** n and worlds per Dn bin.

## Validity (hard stops)
- **Zero checks:**
  - the observer is read-only: the world state and random numbers are the same with and without it (20 and 60
    years);
  - every habit update replays exactly (mismatch 0);
  - every counted update lands in exactly one bin (the new table's n equals the ES2 table's n);
  - Dn lies in [0, 1] for every closed update.
- **All 32 worlds are present** under `code_es2`'s fingerprint (the same as ES2's).
- **The replay matches ES2:** every world's hash, and its pooled n and Σ|q − G|, equal ES2's r file for the same seed.
- **The primary pooled over all Dn equals UV1's r B_high** (−0.1077) to 4 decimals: the same updates.
- **A blind recompute by GPT and Gemini** of B(Dn < 0.1), B(all Dn), the interval, the coverage and the reading, from
  per-world sums.

## The assistant's prior
1. **Mixed.** B(Dn < 0.1) is clearly less negative than −0.108, but not inside ±0.05.
2. **The dose-response falls toward 0 as Dn falls,** but does not reach it.
3. **Year quarters show little trend.**

## Sign-off (1 November 2026)
The assistant, under the creator's sleep-mode autonomy (a read-only study under the 40% rule). GPT estimates 91%,
Gemini 98% and the assistant 75%. Frozen as `UV2-frozen` before any code or data.

## Operational note 1 (01 November 2026, 16:44, after the cloud run, before any outcome was read)
- **What happened:** `analyse_uv2.py` printed "yes" for every validity check but then "NOT VALID", and stopped before
  computing any outcome.
- **The cause:** the check "the primary pooled over all Dn equals UV1's r B_high" produced a NumPy true/false value.
  The full-data branch tested it with `is True`, which a NumPy value never passes. The smoke branch tested
  `is not False`, so the smoke did not catch it.
- **The fix:** cast that value to a plain Python true/false (`bool(...)`). Nothing else changes: no measure, bin, rule,
  threshold or check.
- No outcome had been computed or read when the fix was made.
