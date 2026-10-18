# MB1b — Same 80 people, divided differently: does band size change survival and meeting? (DRAFT for the creator's sign-off; nothing built or run)

**The creator's decision (14 October 2026):** "MB1b: move to 40×40 with 80 founders (P), documented as a different
setting, with the original baseline kept." Stage B of `questions.md` was drafted in LP (80 × 80), where MB1a found bands
effectively closed (0.0007 per adult pair-year); it moves to **P**, where bands meet "rarely" (0.047 / 0.045). The LP
draft stays on record above it; this file replaces it as the design, as a different setting.

**Why it matters (WS1):** 80 founders survived far better than 20 (P died out in 23 of 256 worlds against C's 107), but
WS1's 80 founders came in **bigger bands** (4 × 20 against 4 × 5): WS1 could not say whether it was the number of people
or the size of the bands. MB1b holds the people and the land fixed and changes only how the founders are divided.

**New studies start from nature v2** (signed off 16 October). So the reference arm is re-run on v2, not read from WS1
(which ran on v1): WS1's numbers are the expectation, not the comparison.

## Question

With the same 80 founders on the same 40 × 40 world, does dividing them into more, smaller founding bands change whether
the world survives, and how often its bands meet and mix?

## What the code does now, and the one change needed (read today, `acl/world.py`, `_make_founders`)

- Founders split into `min(4, founders // 4)` bands, so 80 founders make **4 bands of 20**; the code caps bands at 4.
- Each band starts on its own island; **bands beyond the number of islands all go to the largest island**
  (`masses[k] if k < len(masses) else masses[0]`).
- Measured today on 30 new seeds (5301–5330): a 40 × 40 world has **4 islands** (median; range 3–5). So 8 or 16 bands
  cannot each have an island, and under today's rule 12 of 16 bands would crowd the largest one: band size and crowding
  would be confounded.

**One new setting, `founding_bands`** (default `0` = today's rule exactly): when set, the founders are split into that
many bands, and bands are spread over the islands **in turn** (band k on island k mod number of islands), each placed as
far from the others as today's rule allows. Nothing about meeting, visiting, marriage or movement is added. With
`founding_bands = 0` the code must reproduce `code_v2` exactly (zero check).

## Design (the assistant's recommendation; decisions marked)

| arm | founding bands × size | bands per island (4 islands) | role |
|---|---|---|---|
| **P4** | 4 × 20 (today's rule) | 1 | reference |
| **B8** | 8 × 10 | 2 | |
| **B16** | 16 × 5 (today's band size) | 4 | |
| **sham** | 4 × 20, one extra random draw | 1 | chance alone |

- **Code:** a copy of `code_v2` + the one setting (one commit). 40 × 40, 80 founders, 120 years.
- **Seeds (Decision 2):** 256 new seeds, 5301–5556 (recommended: the same power as NV2, RT1 and SA1-F; about 40 hours on
  four workers), or 128 (about 20 hours; intervals about ±0.08 instead of ±0.06).
- **Primary: extinction**, each arm against P4, paired by seed: exact sign test; effect with a 95% bootstrap interval
  (10,000 resamples, `random.Random(2026)`); yardstick ±0.117 (half of F2's effect, as every recent study); Holm over
  B8 and B16. Readings as NV2/RT1: "changes survival" (p < 0.05), "no meaningful effect" (p ≥ 0.05 and the interval
  inside ±0.117), otherwise "unresolved".
- **Described** (population first, rule 18): median population at years 60 and 119; births per woman-year; decisions
  blocked for want of a partner; **between-lineage meeting per adult pair-year** and **cross-lineage couples** (MB1a's
  measures, its observer loaded unchanged); lineages alive at year 120; the actual placement (bands per island, distance
  between band centres), because placement is part of what the arms change.
- **Checks (hard stops):** zero check (setting 0 = `code_v2`); the setting acts (B8, B16 differ); every world's founding
  bands are the size and number its arm says (manipulation check, read at week one); observers read-only; one code
  fingerprint; no outcome shown if any fails.

## What it can and cannot show

It can show whether, at fixed people and land, band size changes survival and mixing in ACL. It cannot separate band
size from the crowding of several bands on one island (in a 40 × 40 world, more bands means more bands per island); the
placement is reported so the reader can see it. Band sizes are operational choices, spanning the range of forager
dispersed groups (Hamilton et al. 2007: geometric mean 15.6), labelled as such.

## The assistant's prior (to be frozen at sign-off; held loosely)

B16 dies out more than P4 (bands of 5 are what today's 20-founder worlds have, and they die out often), B8 in between;
bands meet more in B8 and B16 than in P4, because several share an island. If B16 dies out more despite meeting more,
band size matters more than contact.

## Decisions for the creator

1. Arms: **P4, B8, B16 and sham** (recommended), or only P4 against B16.
2. Seeds: **256** (recommended, about 40 hours) or 128 (about 20 hours).
3. Placement: **spread bands over the islands in turn** (recommended), or keep today's rule (extra bands on the largest
   island).
4. Order: **right after RT1** (recommended; nothing else is queued), or later.
