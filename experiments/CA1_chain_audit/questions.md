# CA1 — The chain audit: where do ACL's inventions stop accumulating? (SIGNED OFF 18 October 2026; frozen as `CA1-frozen` before any code or data)

**Why.** ACL's people invent, but culture does not build on itself: no new kind of thing appears after year 11 in a
1,000-year world (E5's "freeze"); teaching spreads recipes but watching almost never does, and composite things are
forgotten more often than simple ones (E7.7: kept 79% against 96%). Each of those is one link. Cumulative culture needs
the whole chain to hold: **invention → transmission → retention → improvement → retransmission**. This audit measures
every link in the same worlds, to find where most inventions die, before any change to nature is designed. The idea
came from the creator's conversation with GPT (18 October 2026): "Don't give ACL a cumulative-culture mechanism. Find
the missing condition that prevents cumulative culture from emerging". **Read-only: nothing in ACL changes.**

## Question

For each kind of thing ACL's people invent, how far along the chain does it get, and at which link is the largest share
lost?

## What ACL already records (read from the code, 18 October 2026)

- **Inventions:** `world.knowledge[sig]`: who first knew how to make a kind of thing (`first_by`), when, its recipe and
  properties, and every time it was lost (nobody alive knows it) and found again.
- **Learning:** a `learn` event each time someone gets a recipe they did not have, with **how** (`taught`, `copied` from
  watching, `read` from a mark, `heated`) and from whom.
- **Making:** a `make` event each time a thing is made, with its properties (edge, reach, hardness, and so on).
- **Building on:** a recipe can take a **made** thing as a part (`parts`; only someone who knows how to make the part
  can follow it, `knowhow.can_follow`). So "built on an earlier invention" is a recorded fact, not a judgement.
- **Better:** what a thing does is computed from its properties (`matter.factor`, by use: forage, hunt, wood, cold, and
  so on). So "better" can be measured: a thing whose best use helps more than the best use of any of its parts.

## The chain, as measured (each link a share of the one before)

For every kind of thing (`sig`) first made in a world:

1. **Invented:** first made by someone (any way of first knowing it).
2. **Useful:** its best use helps by at least 5% (`factor` ≥ 1.05 for some use). Things that help with nothing are
   counted but drop out here; they cannot accumulate usefully.
3. **Transmitted:** at least one other person learned it (`learn` event), by any route; the route is reported.
4. **Retained:** someone alive still knew it **after its first maker died**.
5. **Built on:** a later kind of thing has it as a part, and that later thing is **better** (its best use helps more
   than the part's best use).
6. **Retransmitted:** that better thing was itself learned by someone other than its first maker, and outlived them.

A chain that reaches link 6 once is one step of cumulative culture. Also reported: the **longest chain** in each world
(part → better thing → better thing again), and the **generations** a recipe passed through (teacher → learner →
learner's learner).

## Design (the assistant's recommendation; decisions marked)

- **Code:** today's live code (nature v2), unchanged; a read-only observer. Zero check: with the observer, the world's
  state hash equals without it.
- **Worlds (Decision 1):** today's standard world (20 founders, 40 × 40), 120 years. **Discovery** 16 new seeds, then
  **holdout** 16 more, as HF2–HF4 did: a finding counts only if it repeats. Seeds fixed at freezing, unused by any study.
- **Plus (Decision 2):** 4 worlds of 300 years (the freeze appeared at year 11 in E5; longer worlds show whether the
  chain grows later).
- **Computer (Decision 3):** MB1b, RT1b and FX2 use four workers until about 22 October. The audit can run **now on two
  more workers** (the machine has eight; read-only, so the other runs are unaffected except for speed), or wait.

## The frozen reading (proposed)

- **The bottleneck** is the link with the **lowest pass rate** (share of the previous link that reaches it), pooled over
  worlds. It counts as found only if it is **the same link in discovery and holdout**. Otherwise: "no single
  bottleneck", and the drop at every link is reported.
- Population is shown beside every measure (rule 18): living people at each decade; links are also reported per 100
  people alive, because a world of 5 people cannot pass much on.
- **What it cannot show:** why a link breaks. It points to the next study; it does not prove a cause.

## The assistant's prior (to be frozen at sign-off; held loosely)

The bottleneck is **link 5, built on** (an invention rarely becomes the part of a better thing): composites are the
first things forgotten (E7.7), and new kinds stop appearing early (E5). Second guess: link 4 (retained), since small
worlds lose what their makers knew.

## Decisions for the creator

1. Worlds: **16 discovery + 16 holdout, 120 years** (recommended), or 32 in one set.
2. Long worlds: **add 4 of 300 years** (recommended), or not.
3. Computer: **run now on two extra workers** (recommended; a few hours, measured in a pilot), or wait until FX2 ends.
4. The reading: **the lowest pass rate, same in both sets** (recommended), or descriptive only.

## Sign-off (18 October 2026)

The creator: "**approve all CA1 recommendations, freeze it**". So: (1) **16 discovery + 16 holdout worlds, 120 years**;
(2) **plus 4 worlds of 300 years**; (3) **run now on two extra workers**; (4) the reading: **the lowest pass rate, the
same link in both sets**. The prior above is frozen as written.

## Operational details (fixed at freezing, before any code)

- **Code:** `code_v2` with nature v2's four settings (as MB1b, RT1b and FX2 use), unchanged; one read-only observer.
  **Zero check (hard stop):** the state hash with the observer equals without it (seeds 501 and 601, 20 years); one code
  fingerprint across all worlds.
- **Seeds:** discovery **6301–6316**, holdout **6317–6332**, long worlds **6401–6404** (unused by any study). 20 founders,
  40 × 40; 120 years (300 for the long worlds). A pilot first (seed 9921, 10 years; throwaway) to time the runs and check
  the observer; only timing and the observer's working are read from it.
- **A kind of thing** = a `sig` in `world.knowledge`. **Invented** = it enters `world.knowledge` (its first knower and
  how they came to know it are recorded). **Useful** = the largest `matter.factor` over the uses forage, hunt, wood,
  stone, fiber, fight, carry and cold is ≥ 1.05, computed from the properties recorded with it (or, if none, from the
  first `make` event of it).
- **Transmitted** = a `learn` event for that `sig` by someone other than its first knower. A copy that came out different
  (`meant` ≠ `thing`) counts for the kind it actually is, not the one meant; such copies are counted as inventions of
  their own and flagged.
- **Retained** = in some week after its first knower died, someone alive held the recipe. Kinds whose first knower is
  still alive at the end are left out of links 4–6 and counted separately ("not yet testable").
- **Built on** = some later kind's recipe takes it as a part (`parts`, or the `part` heated), and that later kind's largest
  factor is **greater** than this one's. **Retransmitted** = such a better kind itself passed links 3 and 4.
- **Pass rate** of link k = kinds reaching link k ÷ kinds reaching link k − 1 (link 4's base is the kinds testable for
  it), pooled over the worlds of a set. Long worlds are reported beside, not in the reading.
- **Also reported:** the route of each first transmission (taught, copied, read, heated); the longest chain of better
  kinds (part → better → better); the most generations a recipe passed through (first knower 0, each learner one more
  than whoever it learned from); and living people at each decade (rule 18).

## Recorded after freezing, before any data (18 October 2026; rule 19)

- The pilot (seed 9921, 10 years; throwaway) took 11 seconds and the observer followed 128 kinds of thing. **4 of 128
  had no recorded properties** (neither in `world.knowledge` nor in a `make` event), so their usefulness cannot be
  computed. They are **counted as not shown useful** at link 2, and their number is reported. Kinds whose first knower
  first got them by a route other than making or heating (a changed copy, or a recipe taught in a changed form) are
  counted as kinds of their own and reported, as frozen.
- The analysis was tested end to end on two throwaway worlds (seeds 9921–9922, 12 years; `output_pilot/`).
