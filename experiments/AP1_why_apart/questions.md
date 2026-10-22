# AP1 — Why are couples apart? (SIGNED OFF 22 October 2026; frozen as `AP1-frozen` before any code or data)

**Why.** CB1 (`../CB1_couples_no_births/findings.md`): on nature v3, couples spend **61%** of their fertile partnered
weeks apart (the partner beyond the camp radius of 2 tiles), and only 17% "eligible". This confirms F1 and HB1. Fixes
were tried:
- **MC1**, a camp that follows the couple: births +12%, survival unchanged.
- **HB1**, a fixed home: more hunger, more extinction.

GPT's advice (`../CB1_couples_no_births/gpt_view_next.md`), adopted: **understand why before changing anything**.
Being apart may serve food or care, and that would be a trade-off, not a fault. **Read-only, descriptive, narrow and
time-bounded.** If the record cannot tell the causes apart, AP1 says so and ACL moves on to another bottleneck.

## Questions

1. **What is each partner doing in the weeks they are apart?** For both partners, the action chosen that week
   (`last_action`):
   - subsistence: forage, gather, hunt, take;
   - care: care, give;
   - social: talk, court, play;
   - moving: explore, join, flee, or a voyage;
   - rest;
   - other.
   The pair's two actions give a **reason class**:
   - **both subsistence** (they feed themselves in different places);
   - **one caring** (with children or others);
   - **one moving away** (exploring, seeking, fleeing);
   - **one resting** while the other works;
   - **other**.
2. **Who moves apart?** In weeks when a together couple becomes apart, which partner's step took them out of the camp
   radius (the woman, the man, or both)?
3. **How long are separations?** The length of apart spells in weeks, and how often a spell ends in reunion before the
   end of the record.
4. **Is being apart linked to food?** The share of apart weeks when either partner is starving, against together weeks.
   This is described only; it cannot show cause.
5. **C against K1:** the same measures, paired by seed, as GPT suggested (does K1 change why couples are apart?).

## Worlds and instrument

- CT1's saved **C and K1** worlds, **128 seeds (8201–8328) × 2 = 256 worlds**, **replayed exactly** on GitHub's
  machines with `code_ct1` (C has both settings 0, which equals nature v3, as the zero checks showed). Each replay's
  final state hash must equal CT1's saved one (hard stop).
- A **read-only observer** after each week records, for every couple with a fertile woman: both actions, both
  positions, the distance, who moved, starving flags, and the spell bookkeeping. It draws no random numbers and writes
  nothing to the world. A zero check shows the world is identical with and without it.
- **Eligibility audit (GPT):** the observer's "apart" must match F1's `apart` block week by week on the same worlds
  (a check, reported).

## Readings (described; no tests decide anything)

- Shares of apart couple-weeks by reason class, with counts, pooled and per world (the world is the unit, bootstrap
  over worlds, `random.Random(2026)`).
- The distribution of spell lengths (median, quartiles), and the share of spells ending in reunion.
- Starving share in apart against together weeks.
- C against K1: paired differences with 95% intervals.
- **Stopping rule:** if more than a third of apart weeks fall into "other" or cannot be classified, AP1 reports that
  the causes cannot be told apart from this record, and proposes moving to another bottleneck.

## The assistant's prior (to be frozen at sign-off)

Most apart weeks (over half) are **both subsistence**: each partner forages where the food is, and the camp radius of
2 tiles is small against a reach of 3. "One moving away" is second. Separation is about food, not about anyone leaving.

## Decisions for the creator

1. The worlds (**128 seeds × C and K1, replayed exactly on GitHub**), or C only (128 worlds, cheaper).
2. The reason classes and the stopping rule, as written.
3. The prior, frozen as written.

## Sign-off (22 October 2026)

The creator: "we will go with your reccomendation". That means:
- **C and K1, 128 seeds each (256 worlds), replayed on GitHub;**
- the reason classes and the stopping rule as written;
- the prior as written.

## Operational note (22 October 2026, while building, before any data; rule 19)

- **Two actions not named in the plan are counted as subsistence:** `fill` (fetching water) and `heat` (cooking).
  `put`, `make`, `steal` and `attack` count as "other". A person on a voyage counts as "moving".
- **Pair reason, in this order:**
  - either partner moving → "one moving away";
  - else either caring → "one caring";
  - else both subsistence → "both subsistence";
  - else either resting → "one resting";
  - else "other", which includes social combinations.
- **"Who moved"**, when a couple goes from together to apart: "her" if her new place alone puts them beyond the camp
  radius and his does not; "him" for the reverse; "both" otherwise.
- **The CT1 world fingerprints** are committed as `saved_world_hashes.json`; GitHub writes stub copies so every replay
  is checked there.
- **The eligibility audit** compares the observer's apart weeks with CT1's saved F1 `apart` counts for every world, in
  the analysis.
