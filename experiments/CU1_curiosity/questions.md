# CU1 — A curiosity law: does a pull towards the rarely tried break the practice trap? (frozen plan)

**A nature-change study** (one law, one setting; adoption is the creator's decision). The creator said yes to a
curiosity law (29 October 2026) and delegated the strength decision ("ask gemini and gpt then you decide"); decided in
debate round 27 (`docs/debate_after_ic2_lr1_2026-10-28.md`). The creator then approved: "yea draft it and run on
github".

## Why
- **EX1 (final):** habit inflation is not caused by copying; people's own learning produces it.
- **HL1 (final):** habits grow only for what is done (rewards flat, the look-ahead 0.06 → 1.26); making gets 258 times
  fewer own updates than foraging; what is chosen early grows most (rank 0.83). A rich-get-richer trap: practice
  starvation.
- **Science:** curiosity is an inner, partly heritable drive switched on by novelty and gaps in knowledge (Loewenstein
  1994; Kidd et al. 2012; Gruber et al. 2014). ACL has the inner part (the `curiosity` gene, the play instinct, puzzles
  from surprise) but no pull towards actions a person has never or rarely tried.

## The law tested (`code_cu1` = `code_v8` + one setting, `curiosity_pull`, default 0 = v8 exactly)
**`curiosity_pull = 1`:** each person remembers how often they have learned from each action in each situation
(`tried`, counted at their own TD update in `biology._learn`). When the mind weighs an option, an action rarely tried in
the current situation gets a pull of

  **0.3 × curiosity × (1 − hunger) ÷ (1 + times tried in this situation)**

- **The strength is borrowed, not invented:** 0.3 × curiosity × (1 − hunger) is the play instinct's own curiosity pull
  (`mind.py`). It is never adjusted after seeing PL1 or any result (GPT).
- **The fading 1/(1 + n) is a design choice,** recorded openly: novelty wears off with experience without ending after
  one try (GPT; Gemini's fading by the learning rate not adopted, since that rate belongs to value updating).
- The same rule for every action; feasibility and safety are unchanged (only options already offered get the pull).
- `tried` is saved with a person only when held, so with 0 the world is v8 exactly.

## Arms (32 paired seeds, 20201–20232; LP: 80 founders, 80×80; 200 years; run on GitHub)
| arm | setting |
|---|---|
| **v** | v8 |
| **c** | `curiosity_pull` 1 |
| **x** | sham: v8 with `sham_draw` 1, the yardstick for world-to-world drift |

## Questions
- **P (primary, GPT): the spread of real practice.** For adults (16+) in years 100–200: of the situation–action pairs a
  person was offered (the options weighed), the share in which they had at least one own learning update in that
  period. Pooled per world (summed over people), compared c − v, paired by seed; world bootstrap, 10,000 replicates.
  Counted from real experience, not from availability (GPT).
- **The frozen rule for P:** **supports** if the lower 95% bound of (c − v) is above 0 **and** above the upper 95% bound
  of the sham's difference (x − v), i.e. the change is clearly larger than what a meaningless change produces.
- **F (flags, not gates; HC1's):** c has 3 or more extinct worlds beyond v, or mean population in years 100–200 below
  0.90 × v. A flag blocks any recommendation to adopt.
- **Secondary (described; not success criteria):** making events per adult-year; world-born adults' (20–40) crafting
  skill (FS1's measure); made things held per adult; the share of make in the offered pairs updated; all in years
  100–200, c − v and x − v.

## What would follow
- **Supports, no flags:** a candidate for nature v9, for the creator's decision; then C (a heritable strength).
- **Does not support:** a general curiosity pull at the play instinct's strength does not widen practice; described.
- **Flags:** curiosity costs survival or food. Not recommended as it stands.

## The assistant's prior
1. P supports: practice spreads clearly more than the sham's drift.
2. No flags.
3. Making per adult-year rises somewhat; crafting skill rises a little.
(GPT: 55% that it meaningfully reduces practice starvation.)

## Validity (hard stops)
- **Zero checks:** `code_cu1` with 0 equals `code_v8` (state and random numbers, seeds 501 and 601 at 20 and 60 years);
  the setting acts; the sham acts; the observer is read-only in arms c and v; reload exact in arm c (with `tried`
  saved); in arm c every person's `tried` equals the observer's count of their own updates (mismatch 0).
- All 96 worlds present under one fingerprint.
- An independent recompute by GPT and Gemini (fresh chats, raw per-world counts) of P and the flags before the findings
  are final.

## Sign-off (29 October 2026)
**The creator: "yea draft it and run on github"**, after delegating the strength decision. Frozen as `CU1-frozen`
before any code or data beyond the law itself (the law was written to `code_cu1` while drafting, run on nothing).

## Operational note 1 (29 October 2026, after freezing, before any data)
How the code (`code_cu1`, `run_cu1.py`, `analyse_cu1.py`) reads the text where it left a choice; checked on 20-year
smoke worlds (seeds 9990 and 9991, all arms; not data). Nothing in the plan, the strength or the rule was changed.
1. **The law** (`v8_to_cu1.diff`): `biology._learn` counts each own update in `tried` (608 per person, created at the
   first update); `mind.decide`'s `add` adds the pull to an offered option's score before the habit term, after the
   dry-ground cost. The pull uses the hunger the mind already computed for that week. Children's 1.6 play factor is not
   part of the borrowed strength (the strength is the play instinct's curiosity term, as decided in round 27).
2. **Offered pairs** are the (situation, action) pairs among the options returned by `thought.steer` for adults (16+)
   in weeks 5,200–10,399 (years 100–199); the situation is `p.last_ctx`, set by the mind before weighing.
   **Practised pairs** are those with an own TD update in the same window. A pair is offered or practised at most once
   per person (sets).
3. **P** pools over people and then over seeds (summed practised ÷ summed offered); the paired bootstrap resamples
   seeds once per replicate for both arms. The sham's interval is (x − v) from the same replicates' scheme.
4. **Secondaries** come from the yearly census (years 100–199): making events, made things held by adults, and
   world-born adults' (20–40) crafting skill, each per adult-year or per head.
5. **The zero checks passed locally** (`zero_local.log`): with 0 the code equals v8 at 20 and 60 years; the setting and
   the sham act; the observer is read-only in arms c and v; `tried` equals the observer's count of own updates for every
   person (0 mismatches); reload exact with `tried` saved; fingerprint 12bdc869.
