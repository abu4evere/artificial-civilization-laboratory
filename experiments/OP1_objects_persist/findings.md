# OP1 — Objects in the world: made things drop instead of vanishing. Findings (recompute by GPT and Gemini pending; not yet final)

Frozen as `OP1-frozen` (operational note 1); decided and signed off in sleep mode (`docs/autonomous_decisions.md`). A
nature-change study: `code_op1` = `code_v7` + one setting (`v7_to_op1.diff`). Run on GitHub Actions (run 40578952705,
`skip_zero=local`). 96 worlds: c (v7), o (things drop), x (sham), on the same 32 seeds (19301–19332). LP, 200 years.
Every number comes from `analyse_op1.py`, written before data; full tables are in `results.md`.

**Validity:**
- zero checks pass (`code_op1` off equals `code_v7`; the observer is read-only; the setting and sham act; reload is
  exact, including the ground);
- all 96 worlds are present under one fingerprint;
- every overflow was dropped, and dropped = picked up + still on the ground in every world (mismatches 0).

## The answer

**By the frozen rule, the change is supported, but it is flagged for population, so adoption is not recommended as
it stands.**

- **M (manipulation): passes.**
  - In arm o, 60,774 carry-limit overflows from making produced 64,345 drops (with inheritance), and nothing was
    deleted.
  - In arm c, 49,874 made things were deleted at the limit.
- **P (primary): supports.**
  - **0.939 [0.917, 0.957]** of dropped things were picked up by a living person.
  - **0.961 of pick-ups were by someone other than the one who dropped it.**
  - The median time on the ground was 5 weeks; 3,911 things were still on the ground at the end.
- **H (flags): population is flagged.**
  - Mean population in years 100–200: o 108.5 against c 128.4, a ratio of **0.845** (below 0.90).
  - The sham was 115.3, a ratio of 0.898.
  - Extinct worlds: c 1, o 0, sham 2 (no flag).
- **D (described, years 50–200):**

  | measure | c | o | sham |
  |---|---|---|---|
  | made things held per adult | 0.555 | **1.018** | 0.525 |
  | making events per adult-year | 0.061 | 0.065 | 0.064 |

## The population flag (described; not a criterion; the frozen rule stands)
- **The worlds drift a lot from small changes.** Paired world-bootstrap ratios against c (computed after the analysis,
  for description only):
  - **o ÷ c 0.845, 95% [0.755, 0.938]** (below 1);
  - the sham ÷ c 0.898, 95% [0.806, 1.014] (includes 1).
- So the sham alone moves population by about 10%, and the flag cannot tell how much of o's 15% is the law. **The
  frozen rule is not re-read:** the flag blocks a recommendation to adopt.
- **A possible cause (not tested):** tools also help fighting (the `fight` use), and people now carry nearly twice as
  many made things. Whether more tools in hand change violence, health or births is not measured here.

## Against the prior (the assistant's, frozen)
1. "M passes": **right.**
2. "P supports: 10–40% picked up, mostly by the dropper": **wrong in size and direction.** 94% are picked up, and 96%
   of those by others: tools pass between people.
3. "No harm flags": **wrong** (population 0.845).
4. "Things accumulate": **partly.** 3,911 were left at the end out of 64,345, so most are picked up within weeks.

## What follows (from the frozen branches)
- **"Supported: a candidate v8 law (things persist), for the creator's decision."** But the flag means the assistant
  does **not** recommend adopting it as it stands.
- **The next question** is why population falls. A read-only look at deaths by cause, births and fighting in arms o and
  c would come before any decision. That is a study for the creator's and the council's choice.
- **The mechanism is the first in ACL's studies to move made things from one person to another at scale:** 58,000
  pick-ups by others across 32 worlds.
