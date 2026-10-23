# GR2 — does first-season grace hold up, and is it safe for population? Findings

Frozen as `GR2-frozen` before any data, on GPT's design (`../G1_first_season_grace/gpt_review_gr1_results.md`) and
the creator's choice (512 pairs, a 5% population margin). Tables: `results.md`, from `analyse_gr2.py` (written and
committed before data; checked on GR1's worlds). GR1's code and runner unchanged (`code_g1`). 1,024 worlds: 512 new
seeds 10001–10512 × C (v3) and G (first-season grace), 20 founders, 120 years. **Run on GitHub's machines**
(`cloud-run`, run 39893692247). Zero checks passed there and on this PC.

## Validity

- Zero checks passed. All 1,024 worlds are present, with one fingerprint.
- **Manipulation check passes:** useful inventions still held at 13 weeks, median C 0.551, G 1.000 (p = 1.4e-85).

**Valid.**

## The frozen reading

**Primary, transmission:** medians C 0.111, G 0.113.

| G − C, mean | 95% interval | Wilcoxon p | reading |
|---|---|---|---|
| +0.0007 | [−0.0025, +0.0040] | 0.80 | **no meaningful effect** |

**Population safety:** time-averaged population C 24.61, G 24.29; G / C − 1 = −0.013 [−0.055, +0.032]:
**inconclusive** (the lower bound is just below −0.05).

**Survival:** C died out in 170 of 512, G in 179 (56 saved / 65 lost; p = 0.47): **no meaningful effect.**

**The adoption rule, fixed before data:** transmission must read "changes transmission" with G higher. It reads "no
meaningful effect". **First-season grace is not adopted.** Nature stays v3.

**The prior was wrong.** It expected the small rise to repeat (+0.4 points). On twice as many new seeds the effect was
+0.07 points, with an interval inside ±0.02. GR1's +0.43 (p = 0.037) was most likely chance.

## Beside it (described; population first)

| arm | median population, year 60 / 119 | died out | recipes held | weeks an invention stays with its inventor | built on by a learner | longest chain | children's useful inventions passed on |
|---|---|---|---|---|---|---|---|
| C | 22 / 22 | 170 | 8.78 | 663 | 5,969 | 13 | 9,146 of 129,834 |
| G | 22 / 22 | 179 | 8.78 | 850 | 9,224 | 14 | 9,269 of 133,775 |

The pathway repeats GR1's exactly: held at 13 weeks 54.5% → 99.5%; valued above 0.15 by the inventor 19.3% →
43.8%; offered in a lesson 20.3% → 32.6%; **learned 11.7% → 11.7%.** The cost: 11,689 teachable older recipes
displaced (0.8 per 100 person-years). GR1's lower population did not repeat (medians equal at both years).

## What it means

- **Grace does what it was built to do, and it does not matter for culture.** Inventions are kept, valued and
  offered far more, and exactly as many are learned. The extra offers are all lost at the lesson.
- **This is the third memory change in a row that does not raise passing on** (LM1's drop order; MR1, which lowered
  it; GR1/GR2, which does nothing). Memory is not ACL's bottleneck for cumulative culture.
- The confirmation did its job: a narrow pass (GR1) would otherwise have entered nature on chance.
- **LU1** (run alongside, read-only) shows where the lesson fails: see `../LU1_lesson_uptake/findings.md`.
