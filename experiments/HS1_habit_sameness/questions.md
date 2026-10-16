# HS1 — Why are everyone's habits alike? Same world, or same nature? (frozen as `HS1-frozen` before any data, 16 October 2026)

**Asked by:** the council (16 October 2026, Gemma 4, question A; `drafts/council/synthesis_2026-10-16.md`); approved to
run by the creator ("ok do the habit sameness check", 16 October 2026). **Read-only:** no change to ACL; replays of
existing code with an observer that draws no random numbers from the world and writes nothing to it.

**Background.** BL0: a child's habits at 20 correlate 0.92 with an unrelated adult's and 0.96 with their parents'. TC1:
switching talk-copying off (arm N) makes families only a fifth to a third more distinct from strangers; most of the
sameness stays. TC1 suspected "the world everyone shares", unproven. But "the world" mixes two things: **this world**
(this map, these neighbours, this history) and **nature** (the rules and the body every world shares). A stranger from
**another world** shares nature but not this world. That is the comparison HS1 adds.

## Question

In worlds where talk copies no habits (TC1's N), how much of a child's sameness with strangers comes from sharing their
**world**, and how much from sharing **nature**?

## Design

- **Code:** `code_tc1` (TC1's, unchanged), the control world (`anticipation_weight = 1.0`), as TC1.
- **Arms:** **N** (`talk_copy = "none"`; primary: no copying, so sameness cannot come from talk) and **W** (today's
  rule; described beside it). **Seeds:** TC1's discovery set, 501–516 and 601–616 (32). **Years:** 80. 64 replays.
  (TC1's discovery runs are not re-read: HS1 needs habit tables TC1 did not save. W's and N's worlds are TC1's exactly.)
- **Observer** (reads only; its own `random.Random(seed)`):
  - at every birth (read at the end of the week it happened): the parents' habits (mean of the mother's and the
    living father's, or the mother's twice, as BL0), and the habits of one adult (16+) of kinship 0 with
    the child, drawn as BL0 does: the **same-world stranger**;
  - every year, at the year's last week: the habits of up to 8 adults (16+), drawn by the observer's RNG: the **pool**
    from which other worlds draw strangers;
  - at each child's 20th birthday: the child's habits.
  All habit tables are the whole learned table, stored to 6 significant figures: **608 values** in this code (32
  situations × 19 actions; BL0's and TC1's notes say 544, a mismatch in the records flagged separately, 16 October). A
  parent who died in the week of the birth has an empty table by the week's end: the other parent's table is used, or
  no parent comparison for that child (fixed before any data, after the first zero check crashed on it).
- **Other-world stranger** (computed afterwards, by `analyse_hs1.py`): for a child born in year y of world k, one adult
  from the pool of the **next world in the seed list** (cyclic) at year y, drawn by `random.Random(2026)` in a fixed
  order; if that world has no pool at year y, the nearest earlier year that has one; none if it died before year y.
- **Measure** (BL0's): Pearson correlation over the whole table, child at 20 against each comparison.

## Readings (frozen)

Per world (N arm), means over children reaching 20 of:
- **r_par** (parents at birth), **r_same** (same-world stranger), **r_other** (other-world stranger).
- **World share of stranger sameness** = (r_same − r_other) ÷ r_same, and **nature share** = r_other ÷ r_same.
  Summaries: median over worlds with a 95% bootstrap interval (10,000 resamples, `random.Random(2026)`); paired
  Wilcoxon of r_same against r_other.

Decision rules (N arm):
- **"Mostly nature"**: r_other is at least 0.9 × r_same with the whole 95% interval of the nature share at or above 0.9.
- **"The world adds sameness"**: r_same > r_other, Wilcoxon p < 0.05, and the nature share's interval wholly below 0.9.
- otherwise **"unresolved at this sample"**.
W is described the same way, beside N (no reading). Population first (rule 18): children reaching 20 per world, and
worlds alive at year 80.

**Validity (hard stops; no outcome shown if any fails):** with and without the observer, the final state hash is identical
(seeds 501 and 601, 20 years, both arms); every one of the 64 replays reaches its end; at least 16 worlds per arm with at
least one child reaching 20 and an other-world stranger.

## Caution, written in advance

High correlations can come partly from the table's structure (situations nobody meets stay near zero for everyone; some
actions are valued in every situation). That structure is itself part of "nature", so it counts on the nature side here;
HS1 cannot separate it from shared experience of the same kind of landscape. Every world is drawn by the same map
generator: "another world" still has islands, seasons and the same foods. So "nature" here means **the rules, the body
and the kind of world**, and the note says so.

## The assistant's prior (frozen; held loosely)

Mostly nature: r_other close to r_same (above 0.9 of it) in N. TC1 showed copying adds a little; place and company,
I expect, add little more.
