# LT1 — teach what the learner lacks: findings

Frozen as `LT1-frozen` before any data, after GPT chose the candidate and reviewed the plan (`gpt_review_next.md`).
Tables: `results.md`, from `analyse_lt1.py` (written before data). Code: `code_lt1` = `code_v3` + `teach_what_lacks`
+ LU1's read-only lesson logging (`v3_to_lt1.diff`). 1,024 worlds: 512 new seeds 11001–11512 × C (v3) and T, 20
founders, 120 years. **Run on GitHub's machines** (`cloud-run`, run 39907800636). Zero checks passed there and here.

## Validity

Zero checks passed; all worlds present; one fingerprint. **Manipulation check passes:** useful lessons ending
"already known" fell from 33.0% to 19.9% (per-world means; p = 6.6e-82).

**Valid.**

## The frozen reading

**Primary, useful recipes learned per person-year:** C 0.0891, T 0.0863; T − C −0.0029 [−0.0065, +0.0006], −3.2% of
C's mean, p = 0.11: **no meaningful effect** (the interval lies inside ±10%).

**Secondary, the share of useful lessons taken:** 5.39% → 6.31% (+0.0093, p = 6e-38).

**Safety:** passing on not worse (+0.0037 [+0.0002, +0.0071]); time-averaged population safe (+2.7% [−2.6%, +8.1%]);
survival no meaningful effect (185 vs 188 of 512).

**The adoption rule:** learning must rise by at least 10%. It did not move. **Not adopted.** Nature stays v3.

**The prior was right on direction and size** ("already known" falls only part of the way, the take rate rises
a little, learning does not pass the bar).

## Beside it (described)

| arm | useful lessons offered per person-year | learned per person-year | known | not_open | part_shown | cannot_follow | taken |
|---|---|---|---|---|---|---|---|
| C | 1.99 | 0.105 | 32.6% | 50.7% | 7.9% | 2.3% | 6.5% |
| T | 1.68 | 0.101 | 20.7% | 59.9% | 9.8% | 2.8% | 6.9% |

## What it means

- **GPT's warning came true.** The share of lessons taken rose, but only because fewer wasted lessons were counted:
  teachers offered about 16% fewer lessons about useful things (they turned to other things they valued), and the
  learner's low openness turned the saved lessons into "not taken" instead. The total learned did not change. Judged
  by its first draft (take rate), this change would have looked like a success.
- **The lesson's real limit is the learner, not the teacher's choice.** Removing a third of the waste moved nothing,
  because about nine in ten of the remaining lessons still fail at the learner's openness (a fixed, low chance that
  does not depend on whether the thing would help).
- This points to GPT's other candidate (need-sensitive uptake) or to openness itself as the next question, if the
  culture line continues. That is the creator's choice.
