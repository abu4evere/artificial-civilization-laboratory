# EX1 — Experience telling instead of habit copying: does it correct the over-valuation? (frozen plan)

**A nature-change study** (one law, one setting; adoption is the creator's decision). Chosen in debate round 23
(`docs/debate_after_ic2_lr1_2026-10-28.md`): after the council showed that CL1, MK1 and CO1 already give the timeline,
both models chose a copying-law study (GPT 80%, Gemini 85%). Built on HC1's design and decision rule (thresholds
approved by the creator on 27 October), on nature v8.

## The evidence
- **FS1 (final):** erosion is not the founders' head start. World-born people become skilled early and lose it as
  making falls about tenfold.
- **CL1 (final, v7):** making's habit value is always low (q 0.025 → 0.049), with almost no social part. The common
  actions' values rise about threefold in 200 years (0.38 → 1.12), and over-value what follows by +0.418 in years
  100–200, of which **copying in talk carries +0.391 (0.93)**. MK1, CO1: making is crowded out by the others' rising
  habits.
- **Why copying inflates (code):** in talk, `actions._imitate` moves the learner's whole table of 608 values towards the
  model's whole table. The model's values were themselves partly copied, and are never checked against the learner's
  own returns: a copy of a copy.
- **HC1 (not supported):** copying only the model's current situation did not correct it.

## The law tested (`code_ex1` = `code_v8` + one setting, `talk_copy`, default `"table"` = v8 exactly)

**`talk_copy = "experience"`: people tell what happened to them, not what they believe.** When a learner would copy a
model in talk (same place, same conditions: respect ≥ 0.2, or the model seeming happier by 0.1), the whole-table copy
is replaced by **one piece of experience**:
- each person remembers their own most recent learning event from their own action: the situation, the action, the
  reward they actually felt, and the situation it led to (`last_exp`, written in `biology._learn`, the person's own TD
  step);
- the learner updates **their own** value for that situation and action with that reward, by the same TD rule and the
  same learning rate (0.05) as their own experience, using **their own** estimate of the next situation:
  q_l[s, a] += 0.05 × (r + 0.8 × max q_l[s′] − q_l[s, a]);
- if the model has no experience yet, nothing passes.

**No new number:** the rate, discount and bounds are the existing TD rule's; the conditions are `_imitate`'s. The
precedent is v8's own `_follow` (E13), which already lets a person learn from the harvest they *see* another get.
GPT's safeguard holds: what passes is a genuine recorded outcome, never a habit value. `last_exp` is saved with a
person only when held, so with "table" the world is v8 exactly.

## Arms (32 paired seeds, 20001–20032; LP: 80 founders, 80×80; 200 years; run on GitHub)

| arm | setting |
|---|---|
| **v** | v8 (`talk_copy` "table") |
| **e** | `talk_copy` "experience" |
| **x** | sham: v8 with `sham_draw` 1, the yardstick for world-to-world drift |

## Logged (read-only observer, as VC1, CL1 and HC1: a wrapper on `biology._learn` that replays each update exactly and follows the realised return)
- For every adult TD update: q before; the realised discounted return G (VC1's definition); by action and era.
- A yearly census: living population; making events; made things held per adult; extinction.

## Questions and the frozen decision rule (HC1's, approved by the creator)
- **P (primary: calibration).** The common actions' (forage, give, talk, gather) bias q − G in years 100–200, v against
  e, paired by seed; world bootstrap, 10,000 replicates. **Supports** if the improvement (bias_v − bias_e) is at least
  **0.10** and its 95% interval's lower bound is above 0.
- **H (no harm: realised return).** Mean realised return G over all adult updates, years 100–200, e − v. **No harm** if
  the lower 95% bound is above **−0.05**.
- **F (flags, reported, not gates).** e has 3 or more extinct worlds beyond v, or mean population in years 100–200 below
  0.90 × v. A flag blocks any recommendation to adopt; it does not change "supported".
- **D (described).** Make's bias; per-action biases; making per adult-year and things held per adult (years 100–200);
  the sham's differences from v beside every measure. Making is not a criterion (GPT).
- **Told experience (described, GPT):** how many experiences pass in arm e; and the share told about a situation the
  listener has itself learned in before (an own TD update in that situation earlier in life).

**The change is supported** if P supports and H shows no harm. Then GPT and Gemini recompute blind and are consulted.
**Adoption is left to the creator.**

## What would follow
- **Supported, no flags:** a candidate for nature v9 (the copying law), for the creator.
- **P fails:** the inflation does not come from copying values as such (for example, carers or the look-ahead carry it
  once copying stops). Described.
- **Harm or flags:** experience telling costs real returns or survival. Not recommended.

## The assistant's prior
1. P supports: the common bias falls from about +0.42 to under +0.15 (improvement ≥ 0.25).
2. H: no harm.
3. No flags.
4. Making per adult-year rises somewhat, but stays far below the early level.

## Validity (hard stops)
- **Zero checks:** `code_ex1` with "table" equals `code_v8` (state and random numbers, seeds 501 and 601 at 20 and 60
  years); the observer is read-only in arm e; the setting acts; the sham acts; reload is exact in arm e (with
  `last_exp` saved).
- The TD replay is exact in every arm (mismatch 0).
- All 96 worlds present under one fingerprint.
- An independent recompute by GPT and Gemini (fresh chats, raw per-world numbers) of P and H before the findings are
  final.

## Review (debate round 24, `docs/debate_after_ic2_lr1_2026-10-28.md`)
- **GPT: approve, 85%.** Keep the latest experience (no new random draws or memory size). Record how often the
  listener has met that situation (adopted, as a described measure). "EX1 may effectively replace whole-table telepathy
  with one-event telepathy": acceptable as a copying-mechanism experiment, **not** emergent language. Check that the
  shared event is the speaker's genuine latest TD update and that no second ordinary learning step happens (a zero
  check below). Keep flags visible; v8 unchanged until the creator decides.
- **Gemini: approve, 95%.** The latest experience is right (a buffer would need invented sizes). Clear the record at
  death: a dead person cannot talk, and `last_exp` belongs to its owner only (never inherited by a newborn or carer).
  The learner uses its own current values for the look-ahead (as written).
- **Added zero check (both):** in arm e, every told experience equals the speaker's latest own TD event (situation,
  action, reward, next situation), and the learner's value changes by exactly one TD step and nowhere else.

## Sign-off (28 October 2026)
The assistant, under the creator's sleep-mode autonomy (CLAUDE.md, Sleep mode). GPT 85%, Gemini 95%; the assistant's
estimate is 75% (new law code, a reused but complex observer). Logged in `docs/autonomous_decisions.md`. Frozen as
`EX1-frozen` before any code or data. **Adoption into nature is left to the creator.**
