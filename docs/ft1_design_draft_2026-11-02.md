# FT1 draft: free choice of targets (2 November 2026)

**What this is:** a draft for a later council round, step 2 of `docs/action_audit_2026-11-02.md`. Nothing is frozen
or run. It is meant to run after AM1 has validated measures, so that it can be judged by them, especially M4 (new
targets) and M3 (ends-directed chains).

## The restriction (v11, read from `mind.decide`)
- **For most actions, the code first picks the single best target by a written formula.** Only that target is
  offered.
  - **forage:** the best of a few tiles (here, home, 6 random tiles within reach, and tiles heard of);
  - **hunt:** the same;
  - **gather:** the best (tile, material) pair;
  - **make:** the best recipe;
  - **put:** the best thing.
- **So within an action, a person can never pick the second-best place or a different material on purpose.** Two
  people in the same spot with the same instincts always aim at the same target. Their differences show only in which
  action they choose.

## The rule (a general law of choice; it names no target)
**T, "choose the target as you choose the act"** (setting `free_targets`).
- **The act is chosen exactly as in v11:** its score is the best target's score, so actions keep their v11 weights.
- **Then the target is drawn** from that act's candidates by the same softmax and temperature (0.2) that choose acts,
  using each candidate's own utility from the existing formula.
- **What a person can consider does not change:** the same candidate lists. The best target stays the most likely,
  but no longer certain.
- **One extra random draw per decision with candidates.** The sham arm carries the same kind of draw, so the
  difference of history alone is measured.

## Why this form
- **It keeps habit values meaning what they mean.** A version that offered every target as its own option would
  inflate actions with many targets (more options in the softmax). The two-stage form avoids that.
- **It is the smallest general opening.** People's own differences can now show *within* an act: where, what and
  which recipe.
- **A later step can widen the candidate lists** (for example, all tiles in sight instead of 6 random ones). That is a
  separate law about perception, tested on its own.

## Questions for a later round
1. Two-stage choice, or targets as separate options with the act's habit value shared out?
2. **Primary:**
   - AM1's M4 (new targets) **only if AM1 validates it**; otherwise M3;
   - or simply food and population, as a check that it does no harm, with the measures described.
3. Is the sham right as "one extra draw per decision", to match the extra randomness?
