# UV1 — Does habit under-valuation fade with experience? A read-only replay of ES2 (frozen plan)

**Read-only: no change to nature.** Live nature stays v11. UV1 replays ES2's v11 and r worlds exactly
(`code_es2`, unchanged) with a wider observer.

## Why
- **ES2** (final, not supported by its rest guard): looking ahead by the real next choice made habits 40% more
  accurate overall (mean |q − G| 0.391 → 0.236).
- **An exploratory look** (`../ES2_realized_lookahead/explore_q_vs_G.md`, not frozen) found two things:
  - under r, q falls below G for every well-sampled action row: mean q +0.456 against G +0.656;
  - under v11, the common actions sit above G: +0.967 against +0.664.
- **One candidate cause, from the code:**
  - a newborn's habits start at half the parents' mean (`acl/biology.py` line 553);
  - they move 5% per update;
  - with a constant step size, a learner stays biased by its starting values for a long time (Sutton & Barto 1998,
    section 2.7; `docs/research/initial_values_and_longer_view_2026-11-01.md`).
- **Other candidates** (GPT): the learning target itself, the policy, or changing circumstances.
- **Debate round 40** (`docs/debate_round40_undervaluation_2026-11-01.md`): both models chose this read-only diagnostic
  first (GPT 94%, Gemini 95%). Both accepted the merged design below (GPT 96%, Gemini 98%).

## The question
Under r, is habit under-valuation a **start lag** that fades as a person updates the same habit more often, or a
**persistent bias** that stays among experienced people? v11 is described the same way.

**What it can and cannot show** (GPT): a fading pattern supports a start lag. It is **not proof** that the inherited
start causes it; only an intervention could show that. Restricting the ages reduces the age–experience confound but
does not remove it.

## Design
- **Worlds:** ES2's arms v11 (`realized_lookahead` 0) and r (1). The same 32 seeds 21501–21532, LP (80 founders,
  80 × 80), 200 years, the same code and settings. 64 worlds; no sham, since nothing in nature changes.
- **The observer:** ES2's observer, unchanged, plus, for every habit update:
  - **k:** how many earlier updates the same person had made to the same habit (the same situation and action, the
    exact q entry), counted over the whole life;
  - **age** at the update, in years;
  - **situation:** the crisis situation (weak or under half a week of food, with company: `ctx // 8 == 0` and
    `(ctx % 8) // 4 == 1`) or not;
  - **death-closed:** whether its G was closed by death (censored) or by the weight falling below 0.001.
- **As in ES2:** q is the value just before the update; G = Σ_j 0.8^j r over the person's next updates; only updates
  started in years 100–200 are counted.
- **Bins:**
  - **k:** 0–9, 10–19, 20–39, 40–79, 80–159, 160+;
  - **age (years):** 1–5, 6–11, 12–15, 16–29, 30–44, 45–59, 60+ (habits are learned from age 1).

## Primary (frozen)
- **The signed bias B = mean(q − G).** It is pooled as Σ(q − G) / n, over updates:
  - in arm r;
  - at ages 16–44;
  - whose G was **not** closed by death.
- **B_low:** k 0–19. **B_high:** k 80 and above.
- **Intervals:** 95%, by a world bootstrap (10,000 resamples of the 32 seeds, pooled per resample; NumPy seed
  20261101).

## Frozen decision rule (for r)
- **Start lag:** the 95% interval of B_high lies inside [−0.05, +0.05], **and** |B_high| ≤ 0.5 × |B_low|.
- **Persistent bias:** the whole interval of B_high lies beyond 0.05 on the same side as B_low. If B_low < 0, its
  upper bound is < −0.05; if B_low > 0, its lower bound is > +0.05.
- **Mixed:** anything else.
- **Coverage guard:** if the high-k cell (r, ages 16–44, not death-closed, k ≥ 80) has fewer than 100,000 updates, or
  updates in fewer than 24 of the 32 worlds, the reading is **inconclusive**.

v11 is read with the same rule and reported beside it. It is described, not decisive.

## Secondary (described, not decisive)
- **B by every k bin,** for both arms (ages 16–44, not death-closed).
- **B by every age bin,** for both arms (all k, not death-closed).
- **B by k within each age bin,** for r, with n per cell.
- **The crisis slices** (Gemini), kept descriptive (GPT): rest and talk in the crisis situation, at k 80+ and k 0–19,
  ages 16–44, both arms.
- **The death-closed share** per arm.
- **Coverage:** n, worlds and people per k bin.

## Validity (hard stops)
- **Zero checks:**
  - the observer is read-only: the world state and random numbers are the same with and without it, in both arms
    (20 and 60 years);
  - every habit update replays exactly (mismatch 0);
  - every counted update lands in exactly one bin (the new table's n equals the ES2 table's n).
- **All 64 worlds are present** under `code_es2`'s fingerprint (the same as ES2's).
- **The replay matches ES2:** every world's hash, and its pooled n and Σ|q − G|, equal ES2's file for the same arm and
  seed.
- **A blind recompute by GPT and Gemini** of B_low, B_high, the interval and the reading, from per-world sums.

## The assistant's prior
1. **r: mixed.** The bias shrinks a lot with experience but stays below −0.05 at k 80+.
2. **v11: persistent over-valuation** at high k (the max look-ahead's bias does not fade with experience).
3. **Coverage is met.**

## Sign-off (1 November 2026)
The assistant, under the creator's sleep-mode autonomy (a read-only study under the 40% rule). GPT estimates 96%,
Gemini 98% and the assistant 80%. Frozen as `UV1-frozen` before any code or data.
