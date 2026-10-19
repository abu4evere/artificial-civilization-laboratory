# RT1b — Residence time with the walk to water counted (SIGNED OFF 18 October 2026; frozen as `RT1b-frozen`, no study run before it)

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

## GPT's review under the creator's delegation (18 October 2026) — choices recorded, **not a sign-off**

GPT chose every recommended option and added two points. Its reply, verbatim (RT1b part):

> Arms: C, R4, R4w. No sham needed; the replicated R4 arm already checks the original result.
>
> Seeds: 256 new seeds (5701–5956), 768 worlds. Avoid reusing already-seen outcomes for the primary comparison.
>
> Fix: Count the week's trip to water. Do not restrict where bases can be.
>
> Order: After MB1b. Keep the hard check: fewer than 5% of thirsty adults who walked to water must be turned back
> without getting access to it. Clarify that the check measures the intended water-access mechanism, not merely a change
> in a summary statistic.
>
> For RT1b, also report thirst deaths and actual successful water access—not just extinction. The fix should be
> validated before the full run begins.

Asked whether this counts as the creator's sign-off, GPT replied: "Keep both plans as drafts until Abdurashid reads them
himself. My recommendations and choices are scientific review, not the creator's authorization to freeze plans." It
allowed reversible preparation: "Write the code and run zero checks. For RT1b, use throwaway seeds for a short pilot to
verify that the water-access fix works mechanically. Keep all pilot results separate from study data. Do not freeze/tag
either plan or begin any study runs until Abdurashid approves them." And: "make sure the RT1b pilot tests whether agents
who visit water can actually obtain water despite the base-return rule—not merely whether the new code executes".

**So:** the plan stays a draft. The assistant notes, against the project's own order (plan frozen before code), that the
code and its checks are being prepared before freezing on GPT's direction; the pilot reads only the water mechanism
(no survival, population or death count), on throwaway seeds outside the study's range.

**Added to the design (from GPT's points):** described outcomes also include thirst deaths (all ages, years 0–39 and
0–119) and **successful water access**: the share of adult-weeks in which a person who had chosen a destination with
water in sight still went short of water. The hard check is that share in R4w, below 5%.

## Prepared before sign-off (18 October 2026; GPT's direction; nothing frozen)

- **Code:** `code_rt1b` = `code_rt1` + `water_trip` (`config.py`, `world.py` `_keep_bases`, `weather.drink`); runner
  `run_rt1b.py` (its `run` refuses while this plan is a draft).
- **Zero checks: all PASS** (`zero_rt1b.log`; `output_rt1b/zero.txt`): `water_trip` 0 = `code_rt1` with and without a
  base (seeds 11, 501, 601); `water_trip` 1 without a base = C exactly; R4w differs from R4; observers read-only; a saved
  and reloaded R4w world continues exactly. Fingerprint `5e25a4c6…`.
- **Mechanism pilot** (`pilot_rt1b.log`; throwaway seeds 9801–9804, 15 years; only the water mechanism was read, no
  survival, population or deaths): under R4w, in 13,176 adult-weeks someone ended the week's actions by reachable water
  and was sent back to base; **none** of them went short of water (R4 does not record that place, so it reads 0 there).
  Of thirsty adult-weeks, the share that followed a chosen trip to water: **R4 0.462** (RT1's check: 0.52), **R4w
  0.018**, under the 5% the plan requires. The fix does what it says.

## Sign-off (18 October 2026)

The creator: "**approve RT1b as is, freeze it**". So: arms **C, R4, R4w** (no sham); **256 new seeds, 5701–5956**; the
fix **counts the week's trip to water**; **after MB1b**. Primary, checks, described outcomes (thirst deaths and
successful water access included) and the prior stand as written above. The code, zero checks and mechanism pilot were
prepared before this sign-off (recorded above); they are kept as they are, fingerprint `5e25a4c6…`. The study runner and
analysis are written next, before any study data.
