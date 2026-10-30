# CO2 — What makes the other options beat making under nature v9? (frozen plan)

**Read-only on nature v9. No change to nature.** CO1's frozen design (`../CO1_competing_options/questions.md`,
final), re-run on `code_v9` with **one addition**: the curiosity pull is split out of the per-entry score.

**Why.** AW1 (final, 30 October 2026): passing technique nearly doubled skill but did not bring making back, so the
bottleneck is the choice. LS2 (final): under v9 the choice gate still carries making's decline (1.66). On v7, CO1
found that the other options' rise was 0.86 learned habit. Nature v9 added a curiosity pull to every option. Does
habit still carry the gap under v9, or does curiosity change it, and how large is curiosity's part for making against
the others? Debate round 35 (`docs/gpt_view_choice_2026-10-30.md`): Gemini chose this first (95%). GPT could not be
reached (ChatGPT did not load on this PC tonight); its view is asked before any outcome is read and recorded beside
the plan.

## Design: CO1's, on v9
- **Unchanged from CO1:** the identity, families, matched states, early (years 0–10) and late (years 100–200)
  windows, bins, swaps, validity checks, analysis (`analyse_co1.py`, copied with names changed) and "what would
  follow". See CO1's plan.
- **Nature:** `experiments/NV9_nature_v9/code_v9` (fingerprint 8f88ec33…), nature v9's settings explicit (as LS2).
- **World:** LP (80 founders, 80 × 80), 200 years, **32 new seeds (20701–20732)**.
- **The one addition (exact, written before data):** under v9 every option's score includes the curiosity pull
  c_a = 0.3 × curiosity × (1 − hunger) / (1 + tried_a), where tried_a is the person's count of own updates for that
  action in that situation. It is the same for every entry of a family, so CO1's per-entry score splits exactly:
  **M_a = c_a + M'_a.** The observer also records making's own habit h_m and curiosity c_m, so making's score splits
  the same way. `hunger` is `mind.hunger_of` (as in `decide`); `tried` is read before that week's learning.

## The questions
1. **Q1–Q4: CO1's,** on v9.
2. **Q5 (new, primary for v9): in late weeks (years 100–200), with making offered, which part carries making's
   deficit?** The gap U_other − U_m splits exactly into **habit** (Σ s_a h_a − h_m), **curiosity** (Σ s_a c_a − c_m),
   **built-in and thought pull** (Σ s_a M'_a − M'_m), and **multiplicity and spread** (Σ s_a T ln n_a + T·H). Each part
   is reported as a share of the gap, with world-bootstrap 95% intervals (10,000 replicates, generator seed 20261101).
   - **Reading (frozen):**
     - "**habit carries it**" if habit's share has a lower bound above 0.5;
     - "**built-in pull carries it**" if that part's lower bound is above 0.5;
     - "**curiosity works against it**" if curiosity's share is negative with an upper bound below 0 (curiosity
       favours making);
     - otherwise "**mixed**".

## The assistant's prior
1. Habit still carries most of the gap (above 0.5), as on v7.
2. Curiosity's part is negative: it favours making, because making is tried less, but it is small.
3. CO1's swap result holds: setting habits back to early values undoes most of making's fall.

## What would follow
- **Habit carries it:** the learning rule is the leak, as HL1 and VC1 suggested on v7. A learning-rule change (for
  example the max look-ahead) becomes the candidate, as a frozen nature-change study, and **only with the creator**.
- **Built-in pull carries it:** the worth people expect from made things is too low against food now. A read-only
  look at how itemval forms and decays comes next.
- **Mixed:** report the shares; no nature change.

## Validity (hard stops)
CO1's: the observer is read-only (state and random numbers identical with and without it, 20 and 60 years); reload
exact; the identity holds in every week (mismatches 0); all 32 worlds present under one fingerprint (`code_v9`). Added:
the curiosity split is computed only when `curiosity_pull` is on, and the zero checks confirm c_a > 0 in offered weeks.
Independent recompute of Q5's shares and Q2's habit share by GPT and Gemini before the findings are final.

## Sign-off (30 October 2026)
**Signed off by the assistant under the creator's sleep-mode autonomy** (read-only; Gemini 95%; the assistant 80%; GPT
not reachable tonight). Frozen as `CO2-frozen` before any code or data.
