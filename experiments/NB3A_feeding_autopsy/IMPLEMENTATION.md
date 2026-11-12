# NB3-A: implementation readings (written before any data)

How `run_nb3a.py` and `analyse_nb3a.py` read the points that `questions.md` (NB3A-frozen) leaves open.

## The replay
- **NB3's own program:** `run_nb3.make`, NB3's observer (`NB2Obs`, with NB3's patches), then the autopsy recorder.
  Code `code_nb3`, unchanged.
- **Runs on long-run** (one world per job, checkpoints), because NB3's slowest worlds took up to 165 minutes on the
  cloud without recorders.
- **Read-only:** `zero_nb3a.py` checks it (`zero_local.log`):
  - for each arm, a world run 8 years with and without the recorders ends with the same fingerprint and generator
    state;
  - a checkpointed run equals an unbroken one.

## The hooks (all read-only)
- **`thought.steer`:** which acts were offered to whom this week, for every arm. The old brain also passes its options
  through it.
- **`brain_nb.rescore`:** did the network change the top option. This is computed as NB3's observer does, with H
  counted with the instincts, for every decision (not only every 50th). It is None for the old minds (c).
- **The food acts:** forage, hunt and take are wrapped. The food gained by everyone on the actor's tile during the act
  is counted, so the whole hunting party is credited.
  - **Gather is not a food act:** it brings materials (`p.mats`), not food. The plan's list named it by mistake. This
    was found in the code before freezing the analysis.
- **The body phase:** the food held by the living just before it, and each person's (food held, need) before the
  caregivers feed their dependents.
  - **"Caregiver short"** compares the caregiver's food then against their own need plus the child's want then.
  - These readings come before that week's rotting, which happens first inside the body phase.
- **`world.ledger`:** the world's own logging copy (need, food held before eating, deficit, food fed to dependents).
  It is read and emptied each week, and nothing in the world reads it.

## The records
- **A week's record is taken after the week's step.** A person who dies in the body phase is not living then, so their
  history ends with the week before death.
  - "The last 8 weeks" = the last 8 records; "early" = the first 6 of them (weeks 8 to 3 before death).
- **Food eaten** = food held before eating − food held after the week.
- **Spoiled** = food held before the body phase − food held at the eating step (summed over the living).
- **Stashes** (tile entries) are read only at the week of a death (and for the survivor at the same week), not every
  week: reading every tile every week would be slow.
- **Matched survivors:**
  - at each starvation death, the living people of the same age group are put in a random order by the recorder's
    own generator (`[seed, 85]`), and the first 4 are kept with their histories;
  - 8 weeks later, the first of them still alive is the match;
  - if none is, or the world ends first, it is counted as not found.
- **"Hard times"** is judged at the death's week for both the death and its survivor. So it cannot differ between them,
  and it cannot pass the survivor part of "leads". It is reported anyway.

## Code check
"Held food but did not eat" (deficit ≤ 0.05, food held ≥ need, ate < half the need) is counted per week. It is
expected to be 0, since eating is automatic.
