# LH1: A fairer look-ahead — keep the protection, lose the familiarity bias (frozen plan)

**A nature-change test in a copy:**
- `code_lh1` = `code_v13` + one setting, `lookahead_rule`. With 0 it is v13 exactly.
- Nothing goes live except by the safe path: a final supported study, blind recomputes, a confirmatory run on new
  seeds, council, zero checks and tests.

**Why:**
- **LD1:** v13's habit look-ahead (r + 0.8 × the max habit value of next week's situation) is a familiarity bias. It
  marks making down, and values being well fed least, because rarely visited situations keep near-start values.
- **HE1:** removing the look-ahead releases making (×6) but raises the starvation rate ×1.64 and killings from 4 to
  216. So the look-ahead also protects against hunger and against harming others.
- **Council round 65** (`docs/debate_round65_after_he1_2026-11-05.md`): test a fairer look-ahead, with harm guards
  first.
  - GPT and Gemini choose (e), the real next choice, as in ES2;
  - DeepSeek chooses (m), the experienced value of the next situation, with (e) as its fallback.
  - GPT warns that (m) may miss delayed consequences.

**What it asks:** does a look-ahead that estimates what actually follows, rather than the best habit of a familiar
situation, release making without more hunger or harm?

## The two rules (general laws; each replaces only the "future" term of the habit update)
The habit update stays q ← q + 0.05 × (r + 0.8 × future − q), clamped. Only "future" changes.

- **e, the real next choice** (ES2's rule, carried over to v13 unchanged):
  - last week's update waits for the next decision;
  - future = the expected habit value of that decision under its own softmax over all scored options (instinct terms
    included), with no random draw.
- **m, the experienced value of the next situation** (new):
  - each person keeps, for each of the 32 situations, the mean r they experienced after deciding there. It is a
    running mean with rate max(1/n, 0.05), the habits' own rate once n ≥ 20;
  - future = that value for next week's situation, read before this week's r is added;
  - a situation never yet experienced takes the person's mean over all situations (0 before any experience);
  - no bootstrap, so no 1 ÷ (1 − 0.8) inflation, and no max over poorly sampled habits;
  - the tables are kept per person and saved.

## Arms (32 new paired seeds **23601–23632**; LP: 80 founders, 80 × 80; 200 years; counted over years 100–200)
| arm | settings |
|---|---|
| **c** | v13 (`lookahead_rule` 0) |
| **e** | `lookahead_rule` 1 |
| **m** | `lookahead_rule` 2 |
| **x** | v13 with `sham_draw` 1 |

## Measures
Pooled sums per world; a paired world bootstrap with 10,000 replicates and NumPy seed 20261118. Every measure has its
population beside it.

### 1. Primary: harm guards (e and m each against c)
A guard is raised by:
- **population:** a living-weeks ratio below 0.90 with its upper bound below 1;
- **extinction:** 3+ extra extinct worlds. Each extinction is listed with the same seed in the other arms;
- **hunger:** a starvation-deaths-per-1,000-living-years ratio above 1.25 with its lower bound above 1;
- **killing:** the rate of deaths by killing per 1,000 living-years higher by more than 0.05, with its lower bound
  above 0. HE1's law rose by about 0.31; v13 is about 0.008;
- **health:** adults' mean health at year ends lower by more than 5 points, with its upper bound below 0.

**"No harm"** if no guard is raised.

### 2. Co-primary: making
- M3 (AM1's ends-directed chains): arm − c with its interval wholly above 0;
- makes per adult-year: arm ÷ c with its lower bound above 1.

### 3. Readings, per arm
- **"Supported"** if there is no harm and making is released. A supported arm goes to a confirmatory run on new seeds.
- If **both** are supported, the council chooses on this frozen data which goes first. Lower starvation, then lower
  killing, is the pre-stated tie-break if the council is split.

### 4. Described
- deaths by cause;
- food per adult;
- acts aimed at a person, steal and attack shares;
- world-new kinds and R;
- M2 and M5;
- living-weeks against the sham;
- the sham against v13.

## Validity (hard stops)
- **Zero checks:**
  - `code_lh1` with rule 0 = `code_v13` (20 and 60 years);
  - the observers leave the world unchanged;
  - e, m and the sham act;
  - reload is exact in e (the held update saved) and in m (the situation tables saved);
  - **unit checks:**
    - in m, every future equals the stored situation value read before the update;
    - in e, every completed update equals ES2's formula.
- **All 4 × 32 worlds** are present under one `code_lh1` fingerprint.
- **A smoke run** before the cloud.
- **A blind recompute** by GPT, Gemini and DeepSeek of the guards and the co-primary for both arms.

## Known limits
- e repeats a rule that failed one per-action calibration guard in ES2 (on v11). LH1 judges it by harm and making, not
  by calibration. Calibration is not measured here.
- m looks ahead one step only. It sees next week's experienced r, not longer chains. If hunger comes after two weeks,
  m may miss it (GPT), and the hunger guard will show it.

## The assistant's prior
1. **e: no harm, making released** (about ×2–3).
2. **m: making released more** (about ×4), **but the hunger guard may be raised.** About a coin toss.
3. **R stays near 0.**

At least one arm supported: about 60%.

## Sign-off (5 November 2026)
The assistant, under the creator's 2 November permission (tests in a copy, the safe path) and standing autonomy.
Council round 65: Gemini 95%, DeepSeek about 80% (for m first), GPT (c) first. The assistant 60%. Frozen as
`LH1-frozen` before any code or data.
