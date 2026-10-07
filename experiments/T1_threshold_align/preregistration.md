# T1 — Align the two thresholds (candidate L1 of N6) (pre-registration, SIGNED OFF and frozen as `T1-frozen`)

**Signed off by the creator (October 2026):** the change as written (the pull toward a partner begins beyond 2 tiles), the outcome bands (≤ 15 / 16–20 / ≥ 21 of 64), and the same 64 seeds as F1. Nothing has been run.

## Why

C1 (confirmed on a holdout): two in five of the weeks couples spend apart are at exactly 3 tiles, where conception is
impossible (it needs partners within `camp_radius` = 2) yet nothing pulls them back (the pull toward a partner applies only
beyond `reach` = 3). H1: partners' homes coincide only half the time, so this gap is not the whole story, but it is a
genuine inconsistency between two thresholds written separately. The creator chose to test it alone first (L1), then a
shared home base (L2) as its own experiment, so that each change's effect can be measured by itself.

**Plan (the creator):** T1 (this; candidate L1) → HB1 (a shared home base, candidate L2, separate pre-registration) → F3
(control, T1, HB1, and optionally both, compared on the same seeds). Named T1 and HB1 because "L1" is already the
name of an earlier experiment (`L1_no_winter_growth`).

## The change

In `mind._far_people`, loved ones within `reach` (3 tiles) are skipped, so the "join" pull toward them does not exist.
**L1: for the partner only, the skip uses `camp_radius` (2) instead of `reach`**, so a partner more than 2 tiles away,
the distance at which conception stops, is someone to be drawn toward. Parents, children and friends keep `reach`, since
nothing about them depends on 2 tiles. The pull's strength, its competition with food, and everything else are unchanged.

**Not chosen (the alternative):** raising the conception distance to 3 would also close the gap, but it changes the
fertility rule itself and would raise births directly rather than by bringing couples together. That is closer to tuning
toward the answer (rule 17), so it is set aside unless the creator decides otherwise.

**Anchor (rule 17):** internal consistency (the pull should apply where conception does not) and N6 (real couples are
together at the scale of a week). No value is tuned: the threshold becomes the one the code already uses for conception.

## Rule 14: baseline survival first

Control worlds die out at 22 of 64 (34%) on the seeds used here (F1). L1 is compared with the same 64 seeds' F1 replays.

## Worlds and code

A copy of the control code with one setting (`partner_pull_radius`, default 0 = as now; L1 = 2). Zero check: with the
setting at its default, the copy reproduces the control world exactly (state hash, two seeds, 20 years). The 64 F1 seeds,
120 years, A2-full people. Measured with F1's observer and C1's observer together (both read-only).

## Manipulation check (frozen with the design)

Over years 0–39 (C1's window), the share of apart couple-weeks at exactly 3 tiles must fall **to at most half** of C1's
(41–43%, so at most about 21%). If it does not, L1 did not do what it was meant to, and the outcome is not read.

## Measures (population beside every measure, rule 18)

- **Primary:** worlds died out (of 64), against F1's 22; paired: saved, lost.
- Couples apart per partnered, non-pregnant woman-week (as `C1/reconcile.py`): F1 57.8%.
- Births per woman-year; median population at years 40, 80, 119; child deaths per birth; starvation.

## Outcomes (thresholds proposed; the creator decides)

| T1 extinctions (of 64; F1: 22) | reading |
|---|---|
| ≤ 15 | **large effect:** the threshold gap mattered a great deal |
| 16–20 | **modest effect** |
| ≥ 21 | **no effect, or worse:** the gap was not a driver of extinction |

Beside it, whatever the band: the change in couples apart and in births, which say whether L1 worked through the
mechanism it targets.

## Priors (written before any run; not predictions to test)

- **Assistant:** a modest effect. C1's gap is two in five apart weeks, but H1 shows partners' homes are 4+ tiles apart in
  about 30% of couple-weeks, which L1 does not touch, and the pull, once present, still loses to food most weeks (C1).
- **Creator's adviser (as quoted by the creator):** "modest improvement."

## Order after sign-off

1. Freeze (`T1-frozen`). 2. Copy the code, add the setting, zero check, smoke test on a throwaway seed. 3. Run the 64
seeds. 4. Report in the frozen order; index, roadmap, picture, book.

## Decisions for the creator

1. The change as above (partner pull beyond 2), or the alternative (conception within 3)?
2. The outcome bands (≤ 15 / 16–20 / ≥ 21 of 64)?
3. The same 64 seeds, paired with F1?
