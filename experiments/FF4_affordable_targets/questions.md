# FF4: a whole action dropped because one target is too far — a fault fix in nature v15 (frozen plan)

**A fault-fix check in a copy, not a new law** (the fourth round, after FF1, FF2 and FF3).
- **The copy:** `code_ff4` = `code_v15` + one setting, `fix_affordable_target`. With 0 it is v15 exactly.
- **The authority:** the creator, 2 November 2026: "I give you permission to edit world rules … If you find something
  fix it"; and 7 November: "you can keep going do not rely on me".
- **The sources:**
  - EG1's findings (`experiments/EG1_energy_gate/findings.md`), which show the fault;
  - council round 75, where it was found;
  - council round 76 (`docs/debate_round76_after_lw1_eg1_2026-11-07.md`). All three models call it a fault, to be fixed
    by the fault path with a harm check and a sham: GPT 98%, Gemini 95%, DeepSeek about 92%.

## The fault
The energy gate in `mind.decide`'s `add` says: an option is dropped when the person's energy is below its cost (the
action's cost + 4 a tile). But for three actions, `decide` first picks the **single best target** among the tiles it
looked at, without regard to energy, and only then applies the gate. So **the whole action is dropped when that one
target is too far, even when another target looked at was affordable.**

| action | where | target chosen by |
|---|---|---|
| forage | `decide`, "# Forage" | the best tile by expected food |
| hunt (the grown) | "# Hunt: better with others." | the best tile with prey, by expected meat |
| gather | "# Gather: …" | the best (tile, material) by want |

**EG1 measured it for food:**
- In **0.429 [0.420, 0.437]** of the starving weeks where food was blocked by energy alone (15,988 of 37,276), a tile
  that was looked at had food and **was affordable**.
- In non-starving weeks the share was 0.926.
- No comment or plan says an affordable target should be refused. The council reads it as an interaction of two steps,
  not a designed law.

## The fix (setting `fix_affordable_target` = 1)
- **When the best target is affordable, nothing changes:** the same target, the same score.
- **When it is not,** the option is offered at **the best target among the affordable ones**, by the code's own ranking
  and score. That ranking is expected food for forage, expected meat for hunt, and want for gather.
- **If no target is affordable,** nothing is offered, as now.
- **Unchanged:**
  - every cost and every recovery;
  - the tiles looked at, and the scores;
  - `best_forage`, which still measures the best food in sight (it steers exploring);
  - all random draws (the fix draws nothing).

## Arms (32 paired seeds 24801–24832, used by no study; LP: 80 founders, 80 × 80; 200 years; years 100–200 counted)
| arm | setting | |
|---|---|---|
| **v15** (c) | `fix_affordable_target` 0 | = `code_v15` (shown by the zero checks) |
| **f** | 1 | the candidate nature v16 |
| **sham** (x) | 0, with `sham_draw` 1 | |

## Decision (frozen): a check for harm only
- **Guards** (f against v15): CI1's eight, exactly as in LW1. The intervals are a paired world bootstrap, 10,000 draws,
  NumPy seed 20261123. A guard is raised when:
  - **starvation deaths** per 1,000 living-years: the ratio is above 1.25 with its lower bound above 1;
  - **killings:** the difference is above 0.05 per 1,000 living-years with its lower bound above 0;
  - **adult health:** the difference is below −5 with its upper bound below 0;
  - **living-weeks:** the ratio is below 0.90 with its upper bound below 1;
  - **extinctions:** f has 3 or more more extinct worlds than v15;
  - **child deaths:** the ratio is above 1.25, its lower bound is above 1, and the rate rises by 3 or more per 1,000
    child-years;
  - **child starvation deaths:** the ratio is above 1.25 with its lower bound above 1;
  - **food gifts to kin's children:** the ratio is below 0.80 with its upper bound below 1.
- **Reading:**
  - **"No harm"** if no guard is raised. f is then adopted as **nature v16** by the safe path. A fault fix restores what
    the gate says; it is not a new law, so there is no confirmatory run (FF1–FF3).
  - **"Harm: investigate"** if a guard is raised. The cause is found and appended first.
- **Flag for investigation** (not a stop): any described measure below whose ratio f ÷ v15 lies outside [0.8, 1.25]
  with its interval wholly outside 1. A read-only explanation is then written before adoption.
- **The sham:** sham − v15 is shown beside every contrast.

## Described (not decisive), per arm
- **The fix at work.** The code's own log counts the weeks where the fix offered a different, affordable target, per
  action (forage, hunt, gather), and where v15 would have offered nothing.
- **EG1 re-measured in each arm** (EG1's definitions, logging in `code_ff4`):
  - the share of starving person-weeks with food feasible but blocked by energy alone (EG1's P);
  - its split by age band and sex, including **the gap for women aged 30–49** (council round 76: re-measure it after the
    fix);
  - the share of starvation deaths at 6+ with a blocked starving week in their last 4 decisions.
- The grown's weeks spent foraging, hunting, gathering and resting.
- Starvation deaths at 6+ per 1,000 living-years at 6+.

## Validity (hard stops)
- **Zero checks:**
  - `code_ff4` with 0 = `code_v15` (state and random stream; 20 and 60 years);
  - the observer and the logs are read-only (c and f, the same state with and without them);
  - the fix and the sham act;
  - reload is exact (arm f);
  - **unit checks** (an f world, 30 years), for every offered forage, hunt and gather:
    - the target offered is the best-scored affordable target among those weighed;
    - when the unconstrained best is affordable, it is the one offered;
    - and the gate never drops an option the fix offered.
- **All 3 × 32 worlds** are present under one `code_ff4` fingerprint.
- **A blind recompute** by GPT, Gemini and DeepSeek, from per-world counts, of the guards, EG1's P per arm, and the
  reading.

## Adoption (if "no harm")
1. `code_v16` = `code_v15` with `fix_affordable_target` defaulting to 1.
2. **Zero checks:** v16 with 0 = `code_v15`; v16 = FF4's arm f.
3. Reference hashes are regenerated, and the tests pass.
4. Tag `nature-v16`, a line in `docs/autonomous_decisions.md`, and a Telegram message to the creator.

## The assistant's prior
1. **No guard raised:** about 85%.
2. **EG1's P falls** from about 0.063 to about 0.035. Starvation deaths fall a little, which is not a gate.
3. **The women's gap narrows,** but does not close.

## Sign-off (7 November 2026)
The assistant, under the creator's 2 November permission to edit world rules, and their 7 November messages ("you can
keep going do not rely on me"; "do not ask for permissions from me just go").
- Council round 76 calls it a fault: GPT 98%, Gemini 95%, DeepSeek about 92%.
- The assistant's estimate that this check is valid and informative is 88%.

Frozen as `FF4-frozen` before any code or data.
