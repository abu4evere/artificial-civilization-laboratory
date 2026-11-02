# UV1 — Does habit under-valuation fade with experience? Findings (final: recomputed blind by GPT and Gemini; see the end)

**Read-only: no change to nature.** Frozen as `UV1-frozen`. Signed off by the assistant (GPT 96%, Gemini 98%, the
assistant 80%; debate round 40). Run on GitHub Actions (run 41331098954, `skip_zero=local`). 64 worlds: ES2's v11 and r
arms replayed on its 32 seeds (21501–21532) with a wider observer. Every number comes from `analyse_uv1.py`, written
before data and tested on a smoke world; full tables are in `results.md`.

**Validity:**
- zero checks pass;
- all 64 worlds are present under ES2's fingerprint;
- every habit update replays exactly (mismatches 0);
- **every world matches ES2's file exactly** (hash, pooled n and Σ|q − G|);
- every counted update is binned once.

**Population beside it:** these are ES2's worlds, unchanged. Mean living population, r ÷ v11, was 1.160 [1.029,
1.289] (ES2).

## The answer
**Persistent bias, by the frozen rule.** Under the realized look-ahead, experience halves the under-valuation but
does not remove it.

| arm | B at k 0–19 [95%] | B at k 80+ [95%] | reading |
|---|---|---|---|
| r | −0.207 [−0.210, −0.204] | **−0.108 [−0.111, −0.105]** | **persistent bias** |
| v11 (described) | +0.205 [+0.193, +0.217] | +0.494 [+0.484, +0.505] | persistent bias |

B is the mean of q − G, at ages 16–44, with G not closed by death. Coverage is met: 1,376,008 high-k updates in r,
in all 32 worlds.

### Secondary (described, not decisive)
- **Under r, the fading happens early, then stops.** B by k bin, ages 16–44:

  | k | 0–9 | 10–19 | 20–39 | 40–79 | 80–159 | 160+ |
  |---|---|---|---|---|---|---|
  | B | −0.269 | −0.143 | −0.118 | −0.113 | −0.108 | −0.086 |

  So it is part start lag (the first ~20 updates) and part a lasting floor near −0.11.
- **Under v11, the over-valuation grows with experience:** +0.078 at k 0–9, +0.322 at 10–19, +0.494 at 80–159,
  +0.510 at 160+. The max look-ahead's inflation builds up as a habit is practised.
- **Children are the most under-valued under r, and it does not fade:**
  - B is −0.391 at ages 1–5 and −0.377 at 6–11, against −0.13 to −0.15 for adults.
  - Within ages 1–5 it worsens with k: −0.365, −0.411, −0.439.
  - Under v11, ages 1–5 are also under-valued (−0.145).
- **The crisis slices for ages 16–44 are thin at k 80+ (n 0).** At k 0–19, rest is −0.459 under v11 and −0.607 under
  r.

## Exploratory (not frozen; `explore_crisis_by_age.md`, written before data after the smoke)
- **ES2's rest guard was raised mostly by toddlers.**
  - In the crisis situation (weak or under half a week of food, with company), **94% of rest updates are by children
    aged 1–5:** v11 746,688 of 797,200; r 943,877 of 1,002,638 (updates whose G was not closed by death).
  - Talk is similar (99% in v11).
  - Children hold almost no food, so they always count as "under half a week of food".
  - Rest's bias at ages 1–5 goes from −0.094 (v11) to −0.359 (r).
- **A code fact bearing on it** (`acl/biology.py`, `_upbringing`; not tested): every week, a child under 12 who is with
  their carer moves **every** habit value 8% toward the carer's. In the situations children are mostly in, the carer's
  own values are rarely updated by the carer. That pull is stronger than the child's own learning (5% per update).

## Against the prior (the assistant's, frozen)
1. **"r: mixed"** was wrong as labelled. The pattern foreseen ("shrinks a lot … but stays below −0.05 at k 80+") is
   what happened, but the frozen rule calls that **persistent bias**. The prior was worded against the rule.
2. "v11: persistent over-valuation at high k": **right.**
3. "Coverage is met": **right.**

## What it means
- **The inherited low start explains part of the under-valuation, not all of it.**
  - Practice halves it within about 20 updates.
  - About −0.11 remains for experienced adults.
  - Something in the target, the situations or the circumstances keeps habits lower than what follows.
- **Candidates for the remaining floor** (hypotheses for the council, not findings):
  - **coarse situations.** ACL's 32 situations lump very different states, and one-step learning over lumped states
    may settle away from the realized return. The literature on this, Tsitsiklis & Van Roy (1997) on learning with
    approximation, is **not read**; it is named as a reading to do;
  - **changing circumstances** over a life;
  - for children, **the upbringing pull** toward the carer's values.
- **ES2's failure is reframed, not reversed.** Its rest guard stands as frozen. But the "rest" it caught is mostly
  toddlers' habits in a situation that is not a food crisis for them.
  - So the research note's starvation analogy (Minnesota) does not fit most of these updates.
  - A correction is appended to `docs/research/resting_when_starving_2026-11-01.md`.
- **For Bob:** a mind's values are built from three things: what it inherits, what it is taught (the carer's pull) and
  what it lives. Here the inherited and the taught parts pull values below what life returns. **The minds learn, but
  not only from their own life.** Whether that is a flaw or a feature of a culture-bearing mind is a question for the
  council and the creator.
- **No change to nature** follows from this study.

## Independent recompute (1 November 2026)
GPT and Gemini, each in a fresh chat, from per-seed sums of the raw output only (`recompute_uv1.md`). **All three
agree:** r −0.2071 → −0.1077 [−0.1106, −0.1047]; v11 +0.2050 → +0.4935; coverage met; persistent bias.

**Final: persistent bias.**

## Correction (2 November 2026): how learned values pass between people
Two statements here were wrong, and they also went into other records and into questions put to GPT and Gemini.
1. **The carer pull runs every 4 weeks, not every week.**
   - `acl/biology.py` calls `_upbringing` when `tick % 4 == 0`: 8% about 13 times a year.
   - About a third (0.92^13 ≈ 0.34) of a newborn's starting difference is still there at age one, when habit learning
     begins. It is nearly gone by twelve if the carer stays near.
   - Per week, the pull is about 2%; a child's own learning step is 5% on the habit being updated, while the pull moves
     every entry. So "the pull is stronger than the child's own learning" does not hold as stated.
2. **Values do not pass only from parents and one carer.**
   - In every conversation, the listener also moves part of the way toward the speaker's **whole** habit table, if
     they respect the speaker or the speaker seems happier (`acl/actions.py`, `_imitate`; rate 0.05 × (0.5 +
     curiosity) × (0.5 + respect)).
   - So learning values from other adults and from peers (oblique and horizontal) **already exists in ACL**, at any
     age.
3. **What this changes here:** the code fact under "Exploratory" understated the carer pull's interval and missed the
   talk channel. The frozen reading (persistent bias) and every number above are unchanged; only the candidate
   explanation for the children's values is affected.
