# ES2 — Do minds learn more accurately when they look ahead by their real next choice? Findings (not final until GPT and Gemini recompute)

**A nature-change test in a copy (`code_es2` = `code_v11` + `realized_lookahead`), not an adoption.** Frozen as
`ES2-frozen`. Signed off by the assistant (GPT 85%, Gemini 80%; debate round 39). Run on GitHub Actions (run
41274072560, `skip_zero=local`). 96 worlds: v11, r (realized look-ahead) and a sham, on 32 paired seeds
(21501–21532); LP (80 founders, 80 × 80), 200 years. Every number comes from `analyse_es2.py`, written before data and
tested on smoke worlds; full tables are in `results.md`.

**Validity:**
- zero checks pass;
- all 96 worlds are present under one fingerprint;
- every habit update replays exactly under its arm's rule (mismatches 0; about 24–28 million closed per arm);
- no held update was left uncompleted.

**Population beside it:** no world died out in any arm. Mean living population, r ÷ v11, was **1.160** [1.029, 1.289];
the sham's was 1.031.

## The answer

**Not supported by the frozen rule, because one guard was raised.** The primary result is large and clean: looking
ahead by the real next choice makes habit values **40% more accurate** overall. But one well-sampled action, **rest**,
becomes less accurate by more than the frozen limit (+0.155 against 0.10). By the rule both models asked for, that one
guard is enough.

### Primary — calibration error across all actions (mean |q − G|, years 100–200)
| arm | mean abs(q − G) |
|---|---|
| v11 | 0.3911 |
| r | **0.2364** |
| sham | 0.3919 |

- **r − v11: −0.155** [−0.161, −0.148]. The sham's difference is +0.001 [−0.006, +0.009]. The primary condition
  (below 0, its upper bound below 0, below the sham's) **is met.**

### Guards
- **Calibration by action** (GPT, frozen: no action with at least 10,000 closed updates may worsen by more than 0.10):
  - **rest: 0.237 → 0.391 (+0.155). RAISED.**
  - In the signed bias, rest goes from −0.145 to −0.387: it becomes more under-valued.
- **Not raised:**
  - uncompleted held updates: 0;
  - population ×1.160 [1.029, 1.289];
  - adult deaths +0.49 per 1,000 adult-years [−0.37, +1.32];
  - extinctions +0.

### Secondary (frozen as reported, not decisive)
- **Ranking accuracy is worse:** −0.055 [−0.094, −0.017] (0.552 → 0.497).
- **Signed bias:** the over-valuation of the common actions mostly disappears:
  - forage +0.41 → −0.17;
  - gather +0.37 → −0.14;
  - give +0.41 → −0.08;
  - put +0.30 → −0.14.
  Making is unchanged (−0.51).
- **Making per adult-year ×3.0** [2.7, 3.3]; **tools' share of foraged food 1.22% → 3.36%** (×2.8); foraged food
  ×1.013.
- **Described:** the instinct share of the options' score variance is 0.78 under v11 and 0.96 under r.

## Against the prior (the assistant's, frozen)
1. "Supported: the error falls": **the error falls strongly (−40%), but a guard blocked support.**
2. "Making rises, but less than in ES1": **right** (×3.0 against ES1's ×5.2).
3. "No guard flag": **wrong** (rest).

## What it means
- **This is the most accurate learning rule tested in ACL so far.** Looking ahead by what a person will actually do,
  instincts included, removes most of the max look-ahead's inflation. Errors fall by 40%. Habits stop over-rating the
  everyday actions, and making triples, with more food and more people and no harm to survival.
- **But it is not clean.** Rest becomes more mis-valued, and the rankings of actions within situations become slightly
  less faithful. The frozen rule, written for exactly this case ("no well-sampled action's calibration may deteriorate
  substantially", GPT), says **not supported**. It is not adopted.
- **What follows** (for debate with GPT and Gemini, and the creator's view; not decided here):
  - **why rest worsens.** Rest is often chosen when tired or ill; perhaps its value comes from what follows a
    recovery week. A read-only look would be first.
  - **whether a rule exists that keeps ES2's gain without the loss**, as a new frozen study. ES2's own rule and guard
    stay as frozen.
- **No change to nature** follows from this study.

## Independent recompute
Pending: GPT and Gemini, each in a fresh chat, from `recompute/es2_one_file.csv` (the primary) and
`recompute/es2_rest_guard.csv` (the guard that decided it). Recorded only from their actual replies.

## Correction (appended 1 November 2026, 10:45)
- **"No held update was left uncompleted" and "uncompleted held updates: 0" above are wrong as worded.**
  - The raw output (`sums.held_dropped`) counts **122** held updates dropped at death in arm r, out of 48,306,910
    updates (a share of 2.5 per million). v11 and the sham have none, since they hold no updates.
  - `results.md` shows the share rounded to five decimals (0.00000), and I read that as zero.
- **The frozen guard is not affected:** it is raised only at 1% of updates or more in any arm. Nothing else changes.
