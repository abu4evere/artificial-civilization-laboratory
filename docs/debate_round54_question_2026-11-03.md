# ACL council, round 54: after HN1 and AM1 (3 November 2026, about 03:55 New York)

The same question goes to GPT, Gemini and DeepSeek. Your answer is an opinion, not sign-off.

## New since round 53 (all final, recomputed blind by all three of you)
- **Nature v12 is live:** FF1's three fault fixes, no harm.
- **HN1** (read-only, v11, 32 worlds):
  - **Hunts never fail for lack of prey.** F = 0: hunters pick tiles where prey stand, and animals move only before
    decisions. 94.6% fail at the success roll; success is 5.4%.
  - **Weapons barely help:** 5.8% armed against 4.7% bare-handed.
  - **The return ratio** (hunting ÷ foraging food per adult-week) is **0.023 [0.019, 0.027]**. The Aché's is about 1.1.
  - **Hunting is chosen** in one adult-week in about 7,650.
  - **F8:** the decision expects 36.75 meat per success, but kills give 8.79.
  - **The frozen routing rule** says HR1 calibrates the base chance. **But even 100% success gives a ratio of 0.42**,
    because a forage-week yields 20.77 food and a kill 8.79. The base chance alone cannot reach the frozen 0.5–1.5
    range.
  - **F7:** each species has a catch rate written in the table but never used (rabbit 0.40, deer 0.16, bison 0.10, fish
    0.25). The code uses one flat 0.10.
    - **Assistant's arithmetic** (lone hunter, skill 0.3, no tool): using the table's rate in place of 0.10 would lift a
      rabbit hunt's ratio from 0.035 to 0.14, deer 0.085 → 0.14, fish 0.04 → 0.10, and bison unchanged at 0.21.
- **AM1** (read-only, v11, 160 worlds):
  - **M1** (a person's own past predicts their choices): **partly validated**. It falls under more chance, but not
    without habits.
  - **M3 and M5** (gather a needed input, then make within 8 weeks, against matched weeks): **not validated, and
    reversed.**
    - Worlds where **learned habits do not steer choice** complete these chains about **8 times** more often (+0.026
      [+0.024, +0.028] against v11's 0.0036).
    - Those worlds also have 25% fewer living-weeks.
    - So in v11, habits help survival but pull people back to common actions and away from finishing what they
      started.
  - **M2** (sequence structure beyond a time-shuffle) falls in both controls. It is a candidate measure.

## Code facts (checked by the assistant, 3 November 11:25, live `acl/` = v12; added after the round was sent, not seen by the models)
- The success roll (`actions.resolve_hunts`) uses `hunt_chance` = min(0.92, 0.10 × n^1.5 × (0.5 + skill) × tool).
  The species is picked **after** success, at random among the prey groups on the tile (`fauna.take_prey`). So using
  each species' own rate needs the species chosen before the roll.
- The `catch` field has been in the species table since the first commit, and no code has ever read it. The table's
  own comment explains every other field, but not `catch`.
- The decision's 25 + 12n (`config.hunt_prey_base`, `hunt_prey_per_hunter`) is also from the first commit. It is used
  only in the decision (`mind.py`), never in what a kill gives.

## Options for the next study
- **A.** Redesign HR1 to calibrate **two** existing things to evidence: the success chance and the meat per kill (the
  prey mix or species meat). It would be chosen on calibration distance and safety only.
- **B.** Fix the hunting faults first, as **FF2-hunt**, a harm-only fault-fix check like FF1:
  - **F7:** the hunt chance uses the species' own catch rate, which the table already declares, instead of the flat
    0.10;
  - **F8:** the decision expects the meat a kill really gives (the prey present), not 25 + 12n.

  Then measure the ratio again, and calibrate only what is still off.
- **C.** Keep hunting as it is, and turn to AM1's **habit/ends tension** with a test in a copy, for example a routine
  or option law (`docs/research/options_routines_2026-11-02.md`) or a learning-rule change. The judge would be M2 and a
  re-validated M3.
- **D.** First rerun AM1's battery on v12 (planned in round 52), then decide.

## Questions
1. Rank A–D, with an estimate (%) that your first choice succeeds (valid, answers its question, keeps to ACL's rules).
2. **Is F7 a fault** (the table says one thing, the code does another) to be fixed like FF1, or is it a calibration
   choice needing evidence? Same question for F8.
3. **On AM1:** is "habits suppress following through" a fault, a calibration problem (VC1: habits over-value common
   actions), or a real trade-off to leave alone?

Please answer briefly (under 400 words).
