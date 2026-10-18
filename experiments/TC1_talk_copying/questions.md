# TC1 — Does copying whole habit tables in talk make everyone alike? (SIGNED OFF and frozen as `TC1-frozen`; nothing run)

**Asked by the creator (14 October 2026),** after BL0 and the council: "test all three conditions: whole-habit copying,
copying only the situation being discussed, and no copying. Keep other conditions identical so we can compare the
results." And the standing rule: "keep every change traceable, and don't treat a plausible explanation as a proven
cause."

**Why.** BL0 (both sets) found that copying in talk is the largest part of adults' habits (56–57% of the habit term),
own experience 37%, and that a child's habits are nearly as close to a stranger's (0.92) as to the parents' (0.96). The
council called whole-table copying a shortcut that averages people together; Kimi warned that the sameness might come
instead from **everyone facing the same rewards in the same world**. Only a comparison with copying switched off can
tell the two apart.

## What the code does today (`actions._imitate`, read 14 October 2026)

When a person talks with someone they respect (respect ≥ 0.2) or who seems happier, **all 544** of the listener's habit
values move toward the speaker's by `rate` = 0.05 × (0.5 + curiosity) × (0.5 + respect). A situation is food on hand (4
levels) × company (2) × season (4) = 32; each has 17 action values.

## Arms (one new world setting, `talk_copy`; its default must reproduce today's world exactly)

| arm | what moves toward the speaker's habits, at the same rate and under the same conditions | |
|---|---|---|
| **W** | all 544 values (today) | control |
| **S** | only the 17 values of the **speaker's current situation** (what the speaker is living now, and what the listener can see of it) | the change |
| **N** | nothing (no habit copying in talk; everything else in talk unchanged: gossip, places, stories, teaching) | the "same world, same rewards" control |
| **Sham** | as W, plus one extra random draw | as in every study |

**Decision 1 for the creator, the size of S:** the speaker's whole current situation (17 values; Gemma's proposal), or
only the action the speaker last chose in it (1 value; Kimi's)? Recommended: **17 values**: it changes one thing, *how
much* of the table moves, and it is closer to "the situation being discussed"; one value would also change how often a
copy happens to matter, so two things at once.

**Law 126 (draft check of S):** T1 a capacity (learning from what another person is doing now), not a content; T2
human-universal (social learning is domain- and situation-specific: Henrich & Gil-White 2001; reviews since; **the
evidence review is still to be done before freezing**); T3 names no outcome; T4 its only channel is being with the
speaker. N is not a candidate for nature: it is a control.

## Measures (BL0's, unchanged, through BL0's observer; population beside each)

- **Primary 1, sameness:** at age 20, the correlation of a child's habits with their parents' minus with an unrelated
  adult's (BL0: 0.040–0.043).
- **Primary 2, whose habits:** own experience's share of the adult habit term, weighted by the choice effect (BL0: 0.372).
- **Also (described):** the copied share; the choice effect (do habits still steer?); the lineage share (experience two
  generations back; BL0: 8%); **extinction** (rule 14, as every study); births; population.

## Reading (decision rules, as BL0's: they fix what each result leads to and claim no truth)

Paired by seed against W; paired Wilcoxon per measure; bootstrap intervals (10,000 resamples, `random.Random(2026)`).

- **"The copying rule makes people alike":** N's parents − stranger difference is at least **twice** W's, p < 0.05, in
  discovery and holdout.
- **"The world makes them alike":** N's difference is within ± 25% of W's (the interval inside that band) in both sets:
  even without copying, people end up alike.
- **S, read against both:** where S falls between W and N, on each primary measure, with its interval.
- Otherwise: unresolved at this sample.

## Worlds

- F1's 64 seeds and 120 years, **discovery 501–516 + 601–616, holdout 811–818 + 1101–1124**, as BL0. So **W must
  reproduce BL0's saved results exactly** (a hard stop otherwise): every W world is a BL0 world.
- Code: a copy of `code_bl0` (BL0's observer and hooks unchanged) with one setting, `talk_copy` (`"whole"` default).
  Zero checks: the copy with `"whole"` equals `code_bl0` and the control world; with N and S, I + C + E + T still adds up
  (T is then smaller or zero).
- Cost: 4 arms × 64 ≈ 256 worlds at BL0's speed, about 3–4 hours.

**Decision 2 for the creator:** 64 seeds (as BL0, so W is BL0 itself; can find large effects, not small), or 256 new seeds
(about 4 times the time; can find smaller effects, but loses the exact link to BL0). Recommended: **64**.

## The assistant's prior (to be frozen; held loosely)

- N: parents − stranger difference rises, but less than twice W's: much of the sameness is the world, not copying.
- S: own experience's share rises above 50% ("mostly learned" by BL0's rule); the choice effect barely changes.
- Extinction: no meaningful change in any arm.

## What it cannot show

Whether real people copy whole dispositions (evidence, not simulation). What a learned signal would do instead (the
separate open question on talk itself). Anything about 80-founder worlds.

## Decisions for the creator (before freezing)

1. Size of S: 17 values (recommended) or 1.
2. Seeds: 64, as BL0 (recommended), or 256 new.
3. Thresholds as above (decision rules).
4. Order: after ID1 is reported and before nature v2 is built (recommended: TC1 needs no change to nature, only a setting
   in a copy), or after.

## Sign-off (14 October 2026)

The creator: "**TC1 — situation size: 17 values. Seeds: 64. Thresholds: keep the existing thresholds fixed and documented
before running. Order: run after ID1. Conditions: whole-habit copying, situation-only copying, no copying, and sham.
Important check: the current version must reproduce BL0's results across its 64 worlds.**" And: "don't start a run until
its configuration and success criteria are saved. If results contradict expectations, report them rather than changing
thresholds afterward."

Every decision is frozen as recommended: S copies the 17 values of the speaker's current situation; F1's 64 seeds, as
BL0; the thresholds above; after ID1 (done). The prior above is frozen as written.

**On Law 126:** TC1 *tests* S; it does not adopt it. The evidence review of situation-specific copying (T2) is required
before S could ever enter nature, not before this test.

## Operational details (fixed at freezing, before any code)

- **Code `code_tc1`:** a copy of `code_bl0` (BL0's hooks and observer unchanged), plus two settings, both defaulting to
  today's world:
  - `talk_copy`: `"whole"` (default; today's `_imitate`), `"situation"` (only indices of the speaker's `last_ctx`: the 17
    values of the situation the speaker decided in this week), `"none"` (`_imitate` returns before changing anything;
    it draws no random number, so nothing else shifts).
  - `sham_draw`: `0` (default) or `1` (one extra draw from the world's generator in week one, exactly as in `code_p2`).
  - The rate and the conditions for copying (respect ≥ 0.2, or a happier speaker) are unchanged in S.
- **The split (BL0's I + C + E + T):** the hook for imitation passes the indices that moved; T is credited only there,
  and the other parts are scaled only there. The weekly check "parts add up to the habit, to 1e-9" stays a hard stop
  in every arm.
- **Arms:** W (`talk_copy="whole"`), S (`"situation"`), N (`"none"`), sham (`"whole"`, `sham_draw=1`).
- **Hard stops:** (1) zero check: `code_tc1` with defaults equals the control code and `code_bl0` (state hash, seeds 501
  and 601, 20 years); (2) **W reproduces BL0's saved results on all 64 worlds** (final week, world hash, and the BL0
  measures identical); (3) one fingerprint; (4) parts add up in every arm; (5) S and N differ from W.
- **Measures, tests and reading:** as above, by BL0's own analysis functions, per arm. Primary 1 = mean (parents − unrelated)
  correlation at age 20 per world; primary 2 = own experience's weighted share per world; paired by seed against W
  (Wilcoxon), with bootstrap intervals. Extinction against W by the exact sign test, as every study.
- **Rule 15:** discovery 501–516 + 601–616, reading written; then holdout 811–818 + 1101–1124. A reading stands only if
  both agree.
- **Analysis script** written and smoke-tested before any data; it shows no outcome when a run is not valid.

## Scripts (appended 14 October 2026, before any TC1 data; rule 19)

`code_tc1`, `run_tc1.py` and `analyse_tc1.py` written and smoke-tested on a throwaway seed (9601, 10 years, all four
arms; `output_smoke/`, not data): parts add up in every arm (largest error 4 × 10⁻¹⁶); N's copied share is 0 and S's
small, as designed. **One fault found and fixed before any data:** the check "W reproduces BL0" first compared numbers
held in memory with numbers read back from BL0's file, where numeric keys become text and sort differently, so it
reported a difference that did not exist. It now compares both as saved; on seed 501, W then equals BL0 in every
recorded number. The two seed-501 outputs made while checking this (before the zero check) are kept in
`output_precheck/`, not used.


**Correction (18 October 2026, appended; nothing above rewritten):** "all 544" should read **all 608**: this study's code has 32 situations × 19 actions. 544 was the older live package. The design and analysis used the whole table, so nothing changes.
