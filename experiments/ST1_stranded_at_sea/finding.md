# ST1 — Stranded at sea: a breach of Rule 3 found by the property tests (October 2026)

**How it was found.** The new property test `test_laws_hold_every_week` (tests/test_properties.py) failed on GitHub's
machine, which draws its own random worlds. Replayed locally: world 601, week 58, person p00021 stood on water with
nothing that floats. Rule 3 says a person can stand on water only if they carry something that floats.

**Two different things were behind it** (read-only tracing; no code was changed):

1. **A carried child (intended; the test was too strict).** p00021 was four months old. Infants and children go where
   their caregiver goes (`acl/world.py`, end of `step`), and the caregiver was crossing water on something that floats.
   A child in the carer's boat is not a breach. The test now accepts it: a child on the same tile as a carer who floats.
2. **Stranding (a real flaw in ACL's nature).** A raft is also the person's best container, edge or weapon, so foraging,
   gathering, hunting or fighting **at sea** uses it (`matter.wear`, called from `actions.py` via `best_item`). If that
   use is its last, it breaks *after* the walk has already found the person afloat, and they end the week standing on
   open water. Children with them are stranded too. Traced example: world 803, p00002, a raft with one use left, a theft
   at sea in week 50, ending on water with no items.

**Size** (`check.py`, ACL's live code, 20 founders, 30 years, 40 fixed seeds; output/check.json):

| measure | value |
|---|---|
| person-weeks | 1,291,054 |
| weeks on water, afloat | 2,942 |
| weeks on water, a child carried by an afloat carer | 219 |
| **weeks stranded** | **22** (15 adults, 7 children) |
| worlds with any stranding | 13 of 40 |
| stranded share of weeks on water | 0.7% |
| longest stranding | 1 week (they reach land the next week) |

**Reading.** Rare and short: about 2 per 100,000 person-weeks, never more than one week. It is the same in every arm of
every experiment run so far (the frozen code copies share it), so it cannot explain a difference between arms. It
cannot be ruled out that it changes who survives a crossing in individual worlds.

**What is not done.** Nature is not changed here. A fix (for example: a float that breaks at sea puts its owner ashore
half-drowned, as `_over_water` already does when a float is missing) is a change to ACL's nature: it needs the
creator's sign-off, becomes a new version, and needs its own zero checks and replay hashes (tests/reference_hashes.json).
It is not part of AA1, whose frozen plan allows no new shortcuts after freezing.

**The test.** `test_laws_hold_every_week` checks every law except stranding; `test_nobody_is_stranded_at_sea` checks it
and is marked as an expected failure naming this finding, so it is tracked, not hidden. If the flaw is fixed, that test
starts passing and the mark is removed.
