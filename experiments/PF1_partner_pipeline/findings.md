# PF1 — where partner finding stops: findings

Frozen as `PF1-frozen` (signed off 20 October 2026, all recommendations). Tables: `results.md`, from `analyse_pf1.py`;
measure definitions (question 3): `definitions.md`. 96 of MB1b's worlds replayed exactly (P4, B8, B16; discovery seeds
5301–5316, holdout 5317–5332), with a courting log and a read-only weekly observer.

## Validity

Zero check PASS (logging and observer change nothing against `code_mb1b`, at 20 and 80 founders, P4 and B16); all 96
worlds present; **every replay equals MB1b's saved world** (final state hash, 96 of 96); one code fingerprint.
**Valid.**

## The frozen reading

The bottleneck (the step where the largest share of fertile single woman-weeks stops) is **S5, courting not tried**,
in every arm, in both sets. **Stands.**

| arm | S1 no match alive | S2 none in sight | S3 none in reach | S4 disliked | S5 not tried | S6 refused |
|---|---|---|---|---|---|---|
| P4 (discovery / holdout) | 3.4% / 2.0% | 30.3% / 35.2% | 18.8% / 16.7% | 0.1% / 0.0% | **47.1% / 45.7%** | 0.4% / 0.3% |
| B8 | 2.2% / 1.5% | 31.5% / 31.8% | 16.5% / 17.7% | 0.1% / 0.1% | **49.3% / 48.4%** | 0.4% / 0.4% |
| B16 | 1.2% / 0.8% | 30.2% / 34.9% | 17.9% / 16.9% | 0.1% / 0.2% | **50.1% / 46.7%** | 0.5% / 0.5% |

## What it shows

1. **In about half of the weeks a woman spends single, a suitable man is right there**: single, unrelated, of a
   suitable age, within the 3 tiles where people can act, and neither dislikes the other. **Neither of them courts.**
   In another third, no suitable man is within sight; in about a sixth, one is in sight but not within reach.
2. **The pool is almost never empty.** Weeks with no suitable man alive anywhere are only 1–3%, falling with smaller
   bands (P4 3.4/2.0% → B16 1.2/0.8%). At 80 founders, partner scarcity is not a shortage of men.
3. **Why more contact did not help (question 2).** Smaller bands moved weeks out of "no match alive" and slightly into
   "not tried" (B16 − P4: +3.0 and +1.0 points), and they made courting more frequent: attempts rose from 3,901 to 5,357
   (discovery) and from 3,574 to 5,530 (holdout). But the extra attempts were mostly **refused**: couples formed stayed
   about the same (1,674 → 1,590; 1,573 → 1,751). In the code (`actions._court`), the one courted accepts only if
   attraction exceeds 0.55, and attraction is 0.25 + 0.2 × sociability + affection + 0.2 × respect + 0.1 × health/100:
   with no affection and no respect for the suitor it stays at or below 0.55 (founders' temperaments lie between 0.1 and 0.9; children's drift a little),
   so **a complete stranger can almost never be accepted**. More meetings across lineages produced more courting of people who
   barely knew each other, and those attempts usually fail.
4. **Age.** "None in sight" grows with her age (P4 27% at 16–26 to 40% at 36–45 in discovery), and "not tried" falls;
   the bottleneck is "not tried" at every age.

## Against the prior (frozen; kept as written)

- "The bottleneck is S1, no match alive": **wrong** (1–3%; the bottleneck is S5, not tried).
- "Smaller bands move weeks from S2/S3 to S1": **wrong** (S1 falls with smaller bands; S2 and S3 barely move).
- Second guess, "S5 for women past their mid-thirties": S5 is the bottleneck, but at all ages and least for the oldest.

## What it cannot show

- **Why** courting is not chosen. `court` competes each week with every other action (foraging, talking, giving,
  resting, looking for water); the audit sees that it was not chosen, not what won instead. A next read-only step
  would log the chosen action in those weeks.
- Steps S2–S4 are read from positions at the end of the week, an approximation of what the person saw while deciding.
- It describes MB1b's 80-founder worlds; whether the same step dominates in 20-founder worlds (where a third die out)
  is not shown.
- It locates where partner finding stops; it does not show that changing that step would save worlds.

## Question 3 (GPT's check)

What MB1b's described measures count is written down in `definitions.md`: the blocked share counts **woman-weeks**
aged 16–45 with no partner (a share of time), and cross-lineage couples count **all couples formed** over the run.
