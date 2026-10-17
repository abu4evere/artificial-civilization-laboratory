# RT1 — Do people who move as often as real camps find partners and survive better? (SIGNED OFF 16 October 2026; frozen as `RT1-frozen` before any code or data)

**Why.** SA1-F's evidence review (`experiments/SA1_sensitivity/evidence_sight_range.md`, 16 October 2026) measured that
ACL's adults change the place they sleep in **59% of weeks**, while forager camps move every **4.3 weeks** (median of
175 fully mobile societies, Binford 2001), about **23% of weeks**: ACL's people relocate about **2.5 times as often**. Three
council models independently proposed testing this (16 October; `drafts/council/synthesis_2026-10-16.md`). The creator
asked for this draft ("draft the residence-time study", 16 October).

**What is already known, and must not be repeated** (`experiments/INDEX.md`):
- **HB1** (a fixed couple home, partners return to it each week): couples together, but **more worlds died** (33 vs 22 of
  64), from extra hunger whose cause is still open (HF1: not food running out near home; hunting fell). The home never
  moved.
- **MC1 / MC1-L** (partners within reach end the week together): couples together, births up, **no effect on survival**
  (256 worlds).
- So RT1 is not about couples. It is about **everyone's** base moving at a forager's pace, the base following the food.

## Question

If people keep a base and move it about as often as forager camps do (every 4 weeks), instead of most weeks, does that
change whether worlds survive, how often people find partners, and how often bands meet?

## Design (the assistant's recommendation; decisions for the creator are marked)

**The rule** (one new setting, `residence_weeks`; 0 = today's world, exactly):
- Every person 16 or older has a **base**: the tile they slept on when it was last set. Children go where their carer
  goes, as now.
- **In ordinary weeks**, people choose and do their week's action as now, anywhere within reach; at the end of the week,
  if they are within reach of their base, they **go back to it** (they foraged out and returned, as foragers do daily).
- **Every `residence_weeks` weeks** (counted per person from when the base was last set), the base moves: that week the
  person does not go back, and where they end the week becomes the new base.
- If anything takes a person beyond reach of their base (fleeing, a long walk to water), that place becomes the new base
  at once: the rule never pulls anyone back over a distance they could not walk.

**Decision 1 (the important one): how far can a base move?**
- **(B) recommended: a camp move is a journey.** In a move week, a person can travel up to `residence_weeks × reach`
  tiles (12 at today's values), so the **distance a month stays about the same** as today. This matches the evidence (camps
  move at least twice their foraging radius in one go, Binford's leapfrog) and the council's control (Gemma: "keep the
  total distance moved per month identical"). It touches the code that offers destinations, in move weeks only.
- (A) simpler: a base moves at most `reach` (3 tiles) every 4 weeks. Monthly travel then falls to about a quarter; any
  effect could be from travelling less, not from staying put (the HB1 trap). Not recommended.

**Decision 2: how often?** `residence_weeks = 4` (Binford's median 4.3, rounded; chosen from evidence, never tuned).
Optional second arm `residence_weeks = 2` (Nemotron's suggestion: shows whether any effect grows with the interval).
Recommended: **4 only** (one arm, more power, half the run time).

**Decision 3: whose base?** Recommended: **each adult has their own** (one change only). Couples or families sharing a
base would mix in MC1/HB1's lever. A shared base could be a later study.

**Code:** a copy of `code_v2` (nature v2, signed off; new studies start from it) with the one setting; one commit; zero
checks below. **Seeds:** 256 new, **5001–5256**, 20 founders, 40 × 40, 120 years. **Arms:** **C** (v2 as it is), **R4**
(`residence_weeks = 4`), **sham** (C with `sham_draw = 1`). 768 worlds, about 10 hours (as NV2). **Order (Decision 4):**
after SA1-F finishes (about a day), before MB1b; or after MB1b.

## Checks (hard stops, before any reading)

1. **Zero:** with `residence_weeks = 0` the code equals `code_v2` exactly (state hash, seeds 501 and 601, 20 years) and
   reproduces v2's reference fingerprints. The observers leave the world unchanged.
2. **The rule acts as intended** (manipulation check, measured on the main run, as `acl_ratios.py` does):
   - R4's adults change the place they sleep in **15–35% of weeks** (forager camps: about 23%); C about 59%;
   - **R4's distance a month within ±25% of C's** (Decision 1 B's purpose). If it falls outside, the run is reported as
     not testing what it meant to, and no reading is made.

## Readings (frozen when signed off)

- **Primary: extinction**, R4 against C, paired by seed: exact sign test; effect with a 95% bootstrap interval (10,000
  resamples, `random.Random(2026)`); yardstick half of F2's effect (0.117), as LK1, NV2 and SA1-F:
  - p < 0.05: "**residence time changes survival**" (direction and size reported);
  - p ≥ 0.05 and the interval inside ±0.117: "**no meaningful effect on survival**";
  - otherwise "**unresolved at this sample**".
- **Described** (population first, rule 18): median population at years 60 and 119; births per woman-year; decisions
  blocked for want of a partner (F1's probe); **between-lineage meeting per adult pair-year** (MB1a's measure);
  **adult starvation deaths and hunting** (HB1's warning signs); the sham against C (must be quiet).

## What it decides

Nothing automatically. If R4 changes survival, partner finding or meeting, the creator decides whether a residence time
goes to nature (Law 126: its evidence is Binford's data, already in hand). If it changes nothing, ACL's frequent moving is
recorded as a difference from foragers that does not matter for survival.

## The assistant's prior (to be frozen; held loosely)

**No meaningful effect on survival**, fewer between-band meetings (people roam less between camp moves) and fewer
starvation deaths than HB1 (the base follows the food). Honestly uncertain: HB1 went the other way for reasons nobody has
found.

## Decisions for the creator

1. How far a base can move: **(B) a journey, same distance a month** (recommended), or (A) at most 3 tiles.
2. How often: **4 weeks only** (recommended), or also 2.
3. Whose base: **each adult's own** (recommended), or shared by couples or families.
4. When: after SA1-F (recommended), before or after MB1b.

## Sign-off (16 October 2026)

The creator: "**approve all four recommendations, freeze it**". So: (1) **a camp move is a journey** (up to
`residence_weeks × reach` tiles in a move week, the same distance a month); (2) **`residence_weeks = 4` only**; (3) **each
adult's own base**; (4) **after SA1-F, before MB1b**. The prior above is frozen as written.

## Operational details (fixed at freezing, before any code)

- **Code `code_rt1`:** a copy of `code_v2` (nature v2 is its defaults: `anticipation_weight = 1.0`, last-seen, corner
  block, ashore if a float breaks, knowledge copy), then **one commit** adding `residence_weeks` (default 0 = v2 exactly).
- **Base.** A person gets a base the first week they end as an adult (16 or older): the tile they end that week on, and
  `weeks since set` = 0. The base and its count are part of the world's saved state (so saved worlds stay exact), and only
  exist when `residence_weeks` > 0.
- **The week, for an adult with a base** (after everyone's action and the hunts, before children join their carers, as
  HB1's step):
  - if `weeks since set` + 1 = `residence_weeks` (a **move week**): the base becomes where they ended the week; count 0;
  - otherwise, if they ended the week within `reach` of their base: they go back to it; count + 1;
  - otherwise (beyond reach, by any route): the base becomes where they are; count 0.
- **In a move week**, every distance a person can *travel* that week is `residence_weeks × reach` (12): the cap on the
  week's move and the destinations offered for exploring, joining people, fleeing and going to water, fire or home. Every
  other use of `reach` (who counts as near, care of children, one's own store, company) is unchanged. Sight is unchanged.
- **Zero checks (hard stops):** with `residence_weeks = 0`, the state hash equals `code_v2`'s (seeds 501 and 601, 20 years)
  and v2's reference fingerprints (seeds 11 and 501, 5 years); observers leave the world unchanged (with and without them,
  seed 501, 20 years, both arms); with `residence_weeks = 4` the world differs (it acts); and a saved and reloaded R4
  world continues exactly (base state kept).
- **Manipulation check (measured on the main run; no reading if it fails):** per adult person-week, whether the tile
  slept on changed from the week before; R4's share must be **15–35%**. **Distance a month:** per adult, the Chebyshev
  distance between where they slept at the start and the end of each run of 4 weeks (weeks 0–3, 4–7, … of their life as
  an adult), mean over all such months; R4's must be **within ±25% of C's**.
- **Observers:** F1's probe (populations, births, deaths by cause, blocked decisions) and MB1a's lineage observer
  (between-lineage meeting per adult pair-year), loaded unchanged; RT1's own read-only observer for the manipulation
  check and hunting (successful hunts per adult-year).
- **Seeds** 5001–5256; arms `c`, `r4`, `sham` (C with `sham_draw = 1`); 120 years; 4 workers.
- **The analysis shows no outcome if the run is not valid** (zero checks, manipulation check, all 768 worlds present,
  one code fingerprint).
