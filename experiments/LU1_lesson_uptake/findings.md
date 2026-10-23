# LU1 — why are offered lessons not taken up? Findings

Frozen as `LU1-frozen` before any data. Read-only: `code_lu1` = `code_v3` + logging of each lesson's outcome
(`v3_to_lu1.diff`); zero checks show it changes nothing. Tables: `results.md`, from `analyse_lu1.py` (written before
data). 256 new seeds 10601–10856, v3, 20 founders, 120 years. **Run on GitHub's machines** (`cloud-run`, run
39893702248). Valid: zero checks passed, all worlds present, one fingerprint.

## The frozen reading

1,474,675 lessons about useful inventions; 6.4% taken.

| outcome | share of all | share of those not taken |
|---|---|---|
| **not_open** (the chance of taking it failed) | 51.1% | **54.6%** |
| known (the learner already had it) | 31.8% | 34.0% |
| part_shown (a part was shown instead) | 8.3% | 8.9% |
| cannot_follow (needs a part they cannot make) | 2.4% | 2.6% |
| own_bad | 0.0% | 0.0% |
| taken | 6.4% | |

**By the reading rule: the main reason useful lessons fail is "not_open"** (55% of those not taken). **The prior was
right** on the main reason and on "known" second.

## Beside it (described)

- **The chance of taking a lesson is low by design.** Among "not_open", the chance was under 0.3 in 83% of lessons
  (mean credence 0.63 × mean openness 0.35). Openness = 0.35 × (0.5 + curiosity), so even full trust gives most
  learners a chance near one in three. A parent's lesson doubles it: lessons from a parent were taken 15.8% of the
  time, from anyone else 5.5%.
- **A third of lessons are wasted on what the learner already knows.** The teacher offers one of their own three
  most-valued things, chosen without regard to the learner.
- **Inventors' own lessons are almost never taken: 2.2%** (72% "not_open", 18% "part_shown"), against 9.2% for
  lessons from someone who learned it. New things are the least believed.
- Learning is not using: of the useful lessons taken, **8.9%** of learners later made the thing.
- Population: median 23 at year 60, 16 at year 120; 99 of 256 worlds died out.

## What it means (the assistant's reading; not a frozen test)

The lesson step has three separate leaks, in order of size: the learner's low openness (a fixed rate, about 0.35,
that does not depend on whether the thing would help them), teachers offering what the learner already has, and
learned things rarely being made. GPT's candidate from the GR1 review, **need-sensitive uptake** (more likely to take a
lesson when the thing would help with a problem the learner has now), targets the largest leak, and LU1 now shows
that leak is real. A second candidate is **teaching what the learner lacks** (the teacher offers among the valued
things the learner does not visibly use). Neither is planned yet; the creator chooses.
