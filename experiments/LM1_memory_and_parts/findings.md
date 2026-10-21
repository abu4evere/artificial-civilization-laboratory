# LM1 — memory or parts: findings

Frozen as `LM1-frozen` (Amendment 1 to the memory manipulation check, approved by the creator before any data). A Law
126 study: two candidate changes to nature, tested in four arms. Tables: `results.md`, from `analyse_lm1.py`. 1,024
worlds (256 seeds 7001–7256 × C, M, L, ML), 20 founders, 40 × 40, 120 years. **Run on GitHub's machines** (`cloud-run`,
run 39632158072, 20 jobs; zero checks passed there and here) and fetched for analysis.

- **M (`memory_ties_by_age`):** when memory is full and recipes tie in value, the longest-held is dropped, not the
  first by name (the naming accident CA3 found, which dropped composites first).
- **L (`parts_first`):** after a visibly failed lesson (the learner could not follow a composite), the teacher shows a
  part the learner lacks.

## Validity

Zero checks PASS; all 1,024 worlds present; one fingerprint; manipulation checks PASS: in M and ML the longest-held
recipe was dropped in 100% of ties, and composites fell from 84.4% of tie drops (C) to 56.1%; part lessons happened in
every L and ML world that lived 10 years (24,991 taken of 312,389). **Valid.**

## The frozen reading (share of useful inventions passed on to anyone else, CA1's link 3)

C's median: **0.090**. Worlds with useful inventions in every arm: 256 of 256.

| arm against C | mean difference | 95% interval | Holm p | reading |
|---|---|---|---|---|
| M | +0.0006 | [−0.0030, +0.0041] | 0.868 | **no meaningful effect** |
| L | **+0.0215** | [+0.0171, +0.0259] | 4.2e-17 | **changes transmission** |
| ML | **+0.0225** | [+0.0182, +0.0268] | 1.4e-19 | **changes transmission** |

Interaction (ML − L) − (M − C): +0.0003 [−0.0056, +0.0065]: **interaction not shown.**

## Beside it (described; population first)

| arm | median population, year 60 / 119 | died out (of 256) | useful kinds created (median) | passed on (median) | made by a learner | improved by a learner | improvement passed on |
|---|---|---|---|---|---|---|---|
| C | 24 / 25 | 79 | 334 | 33 | 2,228 | 2,743 | 252 |
| M | 26 / 26 | 79 | 344 | 33 | 2,176 | 3,512 | 305 |
| L | 22 / 24 | 93 | 328 | 38 | 2,479 | 3,076 | 294 |
| ML | 26 / 26 | 86 | 344 | 40 | 2,533 | 3,919 | 401 |

## What it shows

1. **Teaching the parts first works.** When a lesson fails because the learner cannot make a part, showing that part
   raises the share of useful inventions ever passed on by **2.2 points on average** (C's median share is 9.0%), far beyond chance,
   in both L and ML. It is the first change in ACL's line of transmission studies (CA1–CA3) that moves the bottleneck
   CA1 found.
2. **The memory accident did not matter for transmission.** Removing the naming accident (M) changed what was
   forgotten, as intended, but not how much was passed on. The two changes do not interact.
3. The effect is real but small: about one more invention in fifty passed on. Most useful inventions are still never
   learned by anyone else.
4. Described only (not tested): improvements made by learners are more frequent in M and ML (3,512 and 3,919 against
   2,743), and improvements passed on rise most in ML (401 against 252). Extinction varies by arm (79–93 of 256); it was
   not a frozen test here.

## Against the prior (frozen; kept as written)

- "M alone: small rise in link 3": **wrong** (no meaningful effect).
- "L alone: small rise": **right** (+2.2 points).
- "ML: larger than either, but the interaction not shown": interaction not shown, **right**; ML is about the same as
  L, not clearly larger.
- "Improvement by a learner stays rare (under 10% of link-5 pairs)": not read here (the analysis reports counts, not
  that share).

## What it cannot show

- Whether L should become nature: a Law 126 adoption is a separate decision for the creator, with this study and
  CA3's evidence notes on learning parts before wholes as its case.
- Whether the rise in transmission builds longer chains of inventions over time (cumulative culture), or changes
  survival; those were described, not tested.
- L's teaching rule is one operational form of "parts first", not measured from real teaching.
