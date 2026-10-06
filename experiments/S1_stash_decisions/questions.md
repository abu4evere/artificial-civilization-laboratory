# S1 — Why does stashing almost never win? Questions (written before any data)

**Read-only.** The creator's five questions after W1, which found that a family's winter could only be held in a stash
and that stashes are almost never used. No new mechanics: the decision process is mapped as it stands.

**Worlds:** E13R's control (Arm A, A2-full), seeds 501–516, 120 years, replayed on an instrumented copy of the E13R code
that only records each adult's options and choice. The copy must leave the world byte-identical (state hash after 20
years) and every replay must equal the saved E13R run.

## How the code decides (read from the code before any data)

- Each week every person scores a list of options; the final score of an option is an **instinct** part plus a **habit**
  part (`learned_weight` × the person's learned value of that action in their situation). One option is drawn by
  softmax at temperature 0.2.
- **Put** is offered at most once a week, for the single thing the person most wants to set down: food, seed or a
  material. Food is eligible only above **two weeks' food for the person and their dependents**; seed likewise.
- The instinct for putting food: `2 × belief(food@season) × (0.5 + 0.5 × diligence)`, or, never tried,
  `0.02 + 0.15 × curiosity`; either way multiplied by `(1 − hunger)`.
- The **belief** about stashing food in a season changes only when the owner takes their own stash back two or more
  weeks later. It is credited by how much the stash kept **against food carried loose**, not by whether it helped
  anyone through winter.
- `put` itself returns no immediate reward to the habit learner.

## The questions

1. **How often is stashing considered?** Share of adult-weeks, by season, in which (a) food or seed is above the
   eligibility line, (b) put-food or put-seed is offered, (c) put is offered for a material instead.
2. **What beats it?** When put-food or put-seed is offered and not chosen: the winning action, the score gap, and the
   probability the softmax gave to putting.
3. **What value does stashing get, against foraging?** The instinct and habit parts of put's score and of forage's,
   in the same weeks; how many adults hold any belief about stashing food, and its size.
4. **Do successful stashers learn that it worked?** Every time an owner takes their own stash back after two or more
   weeks: how much it kept against loose food, and how their belief changed. How often stashes are found gone.
5. **If they learn it, why does it not spread?** Among adults with a positive belief about stashing food: how many
   learned it themselves and how many were told; how many people hold such a belief at once.

## Reading rule

Descriptive; nothing scored. S1 changes nothing in any world.
