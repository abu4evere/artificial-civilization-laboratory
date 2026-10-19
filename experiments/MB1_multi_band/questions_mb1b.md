# MB1b — Same 80 people, divided differently: does band size change survival and meeting? (SIGNED OFF 18 October 2026; frozen as `MB1b-frozen` before any code or data)

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

## Sign-off (18 October 2026)

The creator: "**approve all MB1b recommendations**". So: (1) arms **P4, B8, B16 and sham**; (2) **256 seeds**; (3) bands
**spread over the islands in turn**; (4) **right after RT1** (now). The prior above is frozen as written.

## Operational details (fixed at freezing, before any code)

- **Code `code_mb1b`:** a copy of `code_v2` (nature v2 as its defaults) in one commit, then **one commit** adding
  `founding_bands` (default 0 = today's rule). When it is set to n > 0: the founders are split into n bands (founder i
  joins band i mod n, as today), and band k is placed on island **k mod (number of islands)**, with today's search for a
  spot more than 6 tiles from earlier centres (200 tries; the last try is kept if none succeeds, as today).
- **World:** 40 × 40, **80 founders**, 120 years, nature v2. **Arms:** `p4` (`founding_bands` 0: 4 bands of 20), `b8`
  (8 of 10), `b16` (16 of 5), `sham` (`p4` with `sham_draw` 1). **Seeds 5301–5556** (the island count of 5301–5330 was read
  on 18 October from the generated land only, before any run: no outcome was seen). 1,024 worlds; 4 workers.
- **Observers** (read-only; checked): F1's probe and MB1a's lineage observer, both loaded unchanged; plus, at week one,
  the **placement**: each founding band's island and centre (mean founder position), giving bands per island and the
  smallest distance between band centres.
- **Hard stops:** zero check (`founding_bands` 0 = `code_v2`, settings left out of the hash, seeds 11 and 501 for 5 years
  and 501 and 601 for 20, at 20 founders and at 80); b8 and b16 change the world; observers leave it unchanged; **the
  manipulation check**: in every world, MB1a's observer finds as many founding bands as the arm says (4, 8, 16), each of
  the stated size (20, 10, 5); one code fingerprint; all 1,024 worlds present. No outcome is shown if any fails.
- **Primary:** extinction (not reaching year 120 with someone alive), b8 and b16 each against p4, paired by seed: exact
  sign test; effect = p4's extinction share − the arm's; 95% bootstrap (10,000 resamples, `random.Random(2026)`); **Holm
  over the two**; yardstick ±0.117. Readings: p < 0.05 (after Holm) "**dividing changes survival**"; p ≥ 0.05 and the
  interval inside ±0.117 "**no meaningful effect**"; otherwise "**unresolved**". Sham against p4 must be quiet.
- **Described:** as listed above (population, births, blocked decisions, between-lineage meeting and cross-lineage
  couples by MB1a's measures, lineages alive at the end, placement).

## Amendment 1 (18 October 2026, before any data): placement

**Why.** The smoke test (throwaway seeds 9701–9702, 8 years; code check only, no outcome read) showed that with 8 or
16 bands several bands share an island, the frozen search (a spot more than 6 tiles from earlier centres, 200 tries,
the last try kept if none succeeds) often fails on small islands, and some band centres ended **0–2 tiles apart**.
That would mix "smaller bands" with "bands starting merged".

**Change.** When `founding_bands` > 0, each band after the first takes, of 200 tries on its island, **the spot
farthest from the band centres already placed** (largest of the smallest Chebyshev distances, as the frozen rule
measures it), instead of the first try more than 6 tiles away or else the last. `founding_bands` 0 (P4, sham) is
unchanged. Nothing else changes. Zero checks and the smoke test are re-run; the pre-amendment logs are kept
(`zero_mb1b_pre_amendment.log`, `output_mb1b/zero_pre_amendment.txt`, `output_mb1b_smoke_pre_amendment/`). The actual
starting gaps are still reported; the amendment is not assumed to remove every placement problem.

**Approval.** Approved via GPT (creator's delegation, 18 Oct 2026). The assistant asked: "A) Run as frozen, and report
the placement ... B) Amendment 1, before any data: place each band at the spot on its island that is as far as possible
from the bands already placed (best of the 200 tries, instead of the last try)." GPT's reply, verbatim:

> 1. MB1b placement: B — Amendment 1.
>
> Apply the best-of-200 placement rule before examining any experimental outcomes. Keep everything else unchanged and
> rerun all zero checks. Record the amendment and its rationale. This reduces the risk of confounding band size with
> bands starting nearly merged. Also report actual starting gaps; don't assume the amendment eliminates all placement
> problems.
>
> Important: Keep MB1b frozen after Amendment 1. Don't make further changes once its data collection starts without a
> separately documented amendment.

### Amendment 1, correction (18 October 2026, still before any data): distance on the torus

The re-run smoke test of Amendment 1 as first written still showed a gap of 1 between two band centres (b8, seed 9702).
Tracing it (throwaway seed; placement only, no outcome read) found two errors of the assistant's, both about the world
wrapping at its edges:

1. Amendment 1 measured distance on the flat map ("as the frozen rule measures it"), but the world is a torus and people
   walk across its edges, so a band at x = 39 was counted 29 tiles from one at x = 10 that is really 11 away. The
   amended rule now uses the world's own distance (`util.distance`, Chebyshev on the torus). The frozen rule for
   `founding_bands` 0 (P4, sham) is untouched.
2. The read-only placement observer took a plain mean of founder positions, so a band straddling an edge (founders at
   x = 39 and x = 0) was reported in the middle of the map. It now takes the mean on the torus (offsets from the first
   founder). This changes only what is reported, not the world.

The intent approved via GPT ("as far as possible from the bands already placed") is unchanged; this makes the code do
it. Zero checks and the smoke test are re-run again; the first amended run's logs are kept with the suffix
`_amendment1_flat`. GPT is told of this correction.

### Note on the approval (18 October 2026, appended; rule 19)

Later the same day GPT wrote, of its own answers: "Claude may maintain records and investigate implementation issues
that don't alter the experiment, but it shouldn't treat my recommendations as creator authorization." Amendment 1 was
applied and the run started on GPT's reply under the creator's explicit delegation ("gpt is me"), before any data. It is
flagged for the creator to confirm on return; if he does not, the run's placement is reported as it stands and the
pre-amendment rule's runs can be made separately.

### Creator's confirmation (18 October 2026)

The creator, on return: "**confirm amendment 1, keep MB1b running**". Amendment 1 (with its torus correction) is
confirmed by the creator directly; the run continues unchanged.
