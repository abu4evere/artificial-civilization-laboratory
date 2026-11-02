# KL1 — Does know-how outlive its holders? A read-only audit on live nature v11 (frozen plan)

**Read-only: no change to nature.** Live nature v11 (`experiments/NV11_nature_v11/code_v11`, the frozen copy of `acl/`).
This is **IQ1-H3, step 1** (`docs/research/iq1_islamic_sources_report_2026-11-01.md`). It is **inspired** by Q 96:4,
"Who taught by the pen", and Sahih Muslim 1631, that among a person's deeds "knowledge (by which people) benefit"
continues after death. The sources are inspiration only. This study tests nothing about them, and its result can
neither confirm nor refute them.

## Why
- **HA1** (final): made objects carry no know-how. Receivers who could not make a thing almost never made it later
  (0.1%).
- **AW1** (final): being taught doubles crafting skill; watching passes little.
- **The open question for a cumulative mind:** how much know-how is lost when its holders die, and what saves it?
- **Debate round 44** (`docs/debate_round44_knowledge_loss_2026-11-01.md`): both models accepted the design with
  changes, both adopted (GPT 91%, Gemini 75%).

## How know-how lives and dies in v11 (from the code)
- **Gained** only through `remember_recipe`, by one of five paths: **made** (making it), **heated**, **taught**,
  **copied** (watching a maker) and **read** (from a mark).
- **Lost from a mind** in exactly three ways:
  - **evicted:** a person knows at most 12 recipes; when a 13th comes, the least valued goes;
  - **forgotten:** `forget_useless` drops recipes the person values below −0.15;
  - **death:** "A person's memories, habits and know-how end with them" (`acl/biology.py`).
- **Lost to the world:** the world marks a recipe kind **lost** when no living person knows it (`check_lost`), and
  alive again if someone learns it.
- **Marks** on rock last generations but carry only simple **"strike this kind of stone"** know-how. A recipe kind is
  **markable** if its recipe's verb is `strike`.
- **Teaching and copying need a living knower.** So a kind lost to everyone can come back only by being **made**,
  **heated** or **read**.

## Design
- **Worlds:** live v11, unchanged. **32 new seeds 21701–21732**, LP (80 founders, 80 × 80), 200 years. Years 100–200
  are counted.
- **The observer** (read-only) wraps `remember_recipe`, `forget_useless` and `check_lost`, and reads death events. It
  keeps its own record of who knows what, and logs:
  - **every gain:** person, kind, path;
  - **every loss from a mind,** with its cause (evicted, forgotten, death), from the events themselves (GPT);
  - **at every world-level loss** (a kind becomes lost), the cause, from the losses since the last check by the people
    who had known it:
    - **death:** all of them died;
    - **forgetting:** all of them are alive (evicted or forgotten);
    - **mixed:** otherwise;
  - **at every revival** (a lost kind becomes known again): the path of the gain that revived it, and whether the kind
    is markable;
  - **for each death of a knower:** how many of their kinds survive in someone living, and how many are lost with
    them;
  - `read` events per year.

## Primary (frozen)
- **D:** the share of world-level losses in years 100–200 that are **by death**. Mixed losses count in the
  denominator, not the numerator.
- **R_markable:** among **revivals of markable kinds** in years 100–200, the share that came through **read**.
- Both are pooled over the 32 worlds, with 95% world-bootstrap intervals (10,000 resamples; NumPy seed 20261101).

## Frozen readings (descriptive; two separate statements)
1. **Loss:** "death is the main road of loss" if D ≥ 0.5; otherwise "forgetting is".
2. **Marks:**
   - "marks revive lost know-how" if R_markable ≥ 0.10;
   - "marks do not (yet)" if R_markable < 0.10;
   - "too few to judge" if there are fewer than 30 revivals of markable kinds.

A threshold crossing describes. It is not proof of a mechanism (GPT).

## Secondary (described, not decisive)
- **Revival paths** for markable and other kinds: made, heated, read. **Re-invention is not preservation** (GPT): a
  kind made again is "revived" but not transmitted.
- **Gains by path** (all kinds): made, heated, taught, copied, read.
- **Losses from minds by cause:** evicted, forgotten, death.
- **At a knower's death:** the share of their kinds that survive in someone else.
- **Lifetimes of kinds:** weeks from first known to lost, and how many kinds are alive at a time.
- **Knowers per kind** (yearly census): the mean, and the share known by only one person.
- `read` events per year.

## Validity (hard stops)
- **Zero checks** (on GitHub while the creator uses the PC):
  - the observer is read-only: the world state and random numbers are the same with and without it (20 and 60
    years);
  - **the observer's record of who knows what equals the people's actual recipes** at every check (mismatch 0);
  - every world-level loss and revival the observer records matches the world's own register (mismatch 0).
- **All 32 worlds are present** under `code_v11`'s fingerprint.
- **A blind recompute by GPT and Gemini** of D, R_markable, their intervals and the readings, from per-world sums.

## The assistant's prior
1. **Forgetting is the main road of loss** (D < 0.5). With a 12-recipe cap and value-based dropping, most kinds die in
   living minds.
2. **Marks do not (yet)** revive lost know-how: R_markable < 0.10, and most markable revivals are re-made.
3. **At a knower's death, most of their kinds survive in someone else.**

## Sign-off (1 November 2026)
The assistant, with the creator present ("keep working"; a read-only study under the 40% rule, within IQ1's rules). GPT
estimates 91%, Gemini 75% and the assistant 80%. Frozen as `KL1-frozen` before any code or data.
