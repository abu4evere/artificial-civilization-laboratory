# RT1b — Residence time with the walk to water counted (DRAFT, 18 October 2026; not frozen, nothing run)

**Why.** RT1 (`findings.md`, `RT1-done`) found that keeping a base for 4 weeks (R4) killed far more worlds than today's
rule (164 of 256 against 93), through thirst (2,864 deaths against 1,740, years 0–39). The check showed why: ACL counts
water only within sight of where a person **started or ended** the week (`weather.drink`), and R4 returns people to their
base at the end of the week, so a walk to water followed by the return home counted for nothing (52% of R4's thirsty
adult-weeks followed a chosen trip to water; C: 0.9%). RT1 therefore measured a flaw in the base rule, not residence
time. GPT, under the creator's delegation (18 Oct 2026), advised fixing the water-trip flaw first and drafting it for
sign-off, with no runs before then.

## Question

With the week's trip to water counted, as a forager's daily walk from camp to water and back is, does keeping a base for
4 weeks change whether a world survives, compared with today's rule?

## The one change (a study setting, not a change to nature)

`code_rt1b` = a copy of `code_rt1` (nature v2 + `residence_weeks`, RT1's Amendment 1 included), plus one setting,
`water_trip` (default 0 = `code_rt1` exactly):

- When `water_trip` = 1 and a person is moved back to their base at the end of the week (`_keep_bases`), the place where
  they ended the week's actions is remembered for that week only.
- `weather.drink` then looks for reachable fresh water within sight of **where they started, where they went, and where
  they end** (today: started and end). The walking cost is computed as today, from the nearest of these to the water.
- Nothing else changes: not what people choose, not how far they travel, not the base rule. Without a base (arm C) the
  setting does nothing, because nobody is moved back.

**Known limit (stated before any data).** The return walk from water to base costs nothing beyond the week's own travel;
the base itself is still wherever a person stopped in a move week, not chosen for water. The alternative fix (a base may
only be set within reach of fresh water) changes what a base is, so it is listed as an option, not recommended.

## Design (the assistant's recommendation; decisions marked)

| arm | rule | role |
|---|---|---|
| **C** | today's rule (`residence_weeks` 0) | reference |
| **R4** | RT1's base rule, as run | the flaw, replicated |
| **R4w** | R4 + `water_trip` 1 | the question |

- **Seeds (Decision 2):** 256 new, **5701–5956** (unused by any study), 20 founders, 40 × 40, 120 years; 768 worlds,
  about 30 hours on four workers, after MB1b. Or reuse RT1's seeds 5001–5256 and its saved C and R4 worlds, after an exact
  replay check, and run only R4w (256 worlds, about 10 hours); cheaper, but the outcomes of those seeds are already seen.
- **Primary: extinction.** (1) R4w against C (the question); (2) R4w against R4 (does the fix remove RT1's harm?). Each
  paired by seed: exact sign test; effect with a 95% bootstrap interval (10,000 resamples, `random.Random(2026)`); Holm
  over the two; yardstick ±0.117. Readings as RT1: p < 0.05 after Holm "changes survival"; p ≥ 0.05 and the interval
  inside ±0.117 "no meaningful effect"; otherwise "unresolved".
- **No sham** (Decision 1): RT1's sham was quiet (94 against 93) on the same code; or keep one (a fourth arm, 256 more
  worlds).
- **Described** (population first, rule 18): median population at years 60 and 119; deaths by cause, years 0–39 (thirst
  first); births per woman-year; blocked for want of a partner; between-lineage meeting; share of weeks a base moves.

## Checks (hard stops; no outcome shown if any fails)

1. **Zero:** `water_trip` 0 equals `code_rt1` exactly (state hash without the settings; seeds 11 and 501 for 5 years,
   501 and 601 for 20 years, both with `residence_weeks` 0 and 4); `water_trip` 1 with `residence_weeks` 0 equals C
   exactly (it must do nothing without a base); `water_trip` 1 with `residence_weeks` 4 differs (it acts); observers
   read-only; a saved and reloaded R4w world continues exactly; one fingerprint.
2. **Manipulation check, R4 and R4w:** adults change the tile they sleep on in 15–35% of weeks (as RT1).
3. **Manipulation check, the fix:** by `thirst_check.py`'s measure, the share of R4w's thirsty adult-weeks that followed
   a chosen trip to water is **below 5%** (R4: 52%; C: 0.9%). If not, the fix did not do what it says and no outcome is
   shown.

## What it can and cannot show

It can show whether residence time matters in ACL once the walk to water is not thrown away. It cannot show what real
camp moves do: ACL's bases are not chosen for water, food or shelter, and a forager's daily foraging round from camp is
not modelled beyond one week's trip.

## The assistant's prior (to be frozen at sign-off; held loosely)

R4w against C: **no meaningful effect** (RT1's harm was the water flaw; starvation, births and partner finding were
unchanged). R4w against R4: **changes survival** (R4w dies out much less). Thirst deaths in R4w close to C's. If R4w still
dies out more than C, something else in the base rule costs lives, and that is the next thing to find.

## Decisions for the creator

1. Arms: **C, R4, R4w** (recommended), or add a sham.
2. Seeds: **256 new, 5701–5956** (recommended), or reuse RT1's seeds and run only R4w.
3. Fix: **count the week's trip** (recommended), or bases only within reach of water.
4. Order: **after MB1b** (recommended; the computer has four workers and MB1b uses them).
