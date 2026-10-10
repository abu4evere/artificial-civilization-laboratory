# G1 — How fluid are ACL's groups? (read-only; questions, measure and reading rule frozen before any run)

**Asked by the creator (October 2026), after N9.** N9 found one pattern attested across foragers, in direction only:
**people move between bands, so band composition is "stable over periods of months but not years"** (Ache; Hill et al.
2014), and camp membership turns over substantially (Agta; Dyble et al. 2021, mean stability 0.51 between researcher
visits whose interval is not known). Are ACL's groups like that, or far more fixed, or far more fluid? **Read-only: no
change to ACL, no tuning; the observer must leave the world bit-identical.**

## Questions

1. **How long do adults stay co-resident?** Of adult pairs living in the same group now, what share still live in the
   same group 4, 12, 24, 52 and 104 weeks later (both still alive and adult)?
2. **How often is a world one single group** (no other group to move to)? Fluidity is impossible there.
3. **Who moves:** is co-residence persistence different for the unpartnered (seekers, as the code defines them) than for
   partnered adults? (Descriptive.)
4. Population beside every figure (rule 18): adults alive, number of groups.

## Definitions (fixed now)

- **Group:** F1's existing definition, unchanged: living people chained by distance ≤ `camp_radius` (2 tiles).
  Sensitivity, reported beside it: chained by distance ≤ `perception` (4 tiles).
- **Adult:** stage "adult" or "elder" (16 and over).
- **Co-resident in a 4-week block:** two adults in the same group in **at least 3 of the block's 4 weekly snapshots**
  (so one week's foraging apart does not count as leaving). Snapshots are taken after every week.
- **Persistence P(Δ):** among adult pairs co-resident in block *b*, both alive and adult in block *b + Δ*, the share
  co-resident in block *b + Δ*. Δ = 1, 3, 6, 13, 26 blocks (≈ 4, 12, 24, 52, 104 weeks). Pooled over all blocks and pairs
  in a world; reported per world (median and quartiles across worlds) and pooled across worlds.
- **Single-group blocks:** blocks in which every adult belongs to one group (by the majority rule).

## Worlds (rule 15)

- **Discovery:** F1's 64 control seeds (501–516, 601–616, 811–818, 1101–1124), 120 years, control code (`code_e13r`),
  each run checked against F1's saved populations.
- **Holdout:** 64 new seeds, **2601–2664**, run only after the discovery reading is written down. The verdict stands only
  if the holdout gives the same reading.

## Reading rule (frozen; a reading of a qualitative benchmark, not an anchored number)

"Stable over months but not years" is read as **P(12 weeks) ≥ 0.5 and P(104 weeks) < 0.5**, on the pooled primary
measure (camp-radius groups).

| | reading |
|---|---|
| P(104 weeks) ≥ 0.5 | **ACL's groups are more fixed than forager bands** (co-residence lasts years) |
| P(12 weeks) < 0.5 | **ACL's groups are more fluid than forager bands** (co-residence does not last months) |
| otherwise | **consistent with the forager benchmark** |

If more than half of all blocks are single-group, this is reported first: persistence there is 1 by construction, and
the reading is also given for blocks with two or more groups (descriptive).

## Hard stops

- The observer is read-only: world state hash identical with and without it (two seeds, 20 years).
- Discovery runs reproduce F1's saved populations; code fingerprint unchanged.

## What this cannot decide

Nothing is changed in ACL by this check. If ACL's groups prove more fixed (or more fluid) than foragers', that is a gap
anchored in direction only; any change would need its own candidates, evidence and sign-off.

## Prior (written before any run; not a prediction to test)

- **Assistant:** ACL's worlds are small and often one or two groups; I expect many single-group blocks and long
  co-residence, i.e. "more fixed than forager bands". Held loosely.
