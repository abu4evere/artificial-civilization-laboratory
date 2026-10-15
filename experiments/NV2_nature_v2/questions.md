# NV2 — Nature version 2: what goes in, and how it is checked (DRAFT for the creator's sign-off; nothing built or run)

**The creator's decisions so far:**
- 13 October: "approve last-seen + A1 for nature v2, after BL0" (one change, one record).
- 14 October: include the raft fix and the knowledge-record quirk "only after reviewing their evidence"; keep mortality
  paused until adult deaths are measured. Rule: "keep every change traceable, and don't treat a plausible explanation as a
  proven cause."

**What nature v2 is.** A new, numbered version of ACL's rules. `nature-v1` stays exactly as it is (tagged; code copies kept);
**every result so far stays on v1**, and is never re-run or re-read under v2. v2 is the version future studies start
from, once it is built, checked and signed off.

## The candidates and their evidence

| # | change | status | evidence (what was measured; nothing assumed) |
|---|---|---|---|
| 1 | **Last-seen memory replaces A5** (walk to where an absent loved one was last seen, not to where they are now) | **approved** | AA1 measured A5 (~30% of go-to moves, a channel nobody wrote); LK1 tested the replacement on 256 worlds: no meaningful effect on survival, partner finding or births; families apart more. Passes T1–T4 (LK1's freeze). |
| 2 | **A1 fix** (water touching only at a corner blocks a diagonal step) | **approved**; built on branch `nature-v2-a1` (commit `5c612d1`, with a test) | AA1: corner crossings were 83% / 30% of water crossings, concentrated in one world in three (a hidden land bridge nobody intended). |
| 3 | **ST1 fix** (a float that breaks at sea puts its owner ashore half-drowned, as the code already does when a float is missing) | **for review** | ST1 (`experiments/ST1_stranded_at_sea/finding.md`): found by the property tests; a raft that breaks after the walk strands its owner on water against Rule 3: **22 person-weeks in 1,291,054** (13 of 40 worlds; never more than one week). Same in every arm of every study. A breach of a written rule, small. |
| 4 | **Knowledge-record quirk** (record a first-baked thing's properties as a copy, not the item itself) | **for review** | ID1's trace (`experiments/ID1_memory_identity/questions.md`, 14 October): the record follows one item's wetness and contents; checked week by week on one world: **no person's behaviour differs**; only the record, and so a saved-and-loaded world is not bit-exact. A bookkeeping flaw, not behaviour. |
| — | Mortality scale | **paused** (creator) | SA1's evidence note: ACL's illness risk is 5.4 × the forager average at every age (Gurven & Kaplan 2007). Waits for a measurement of ACL's total adult mortality. |

**Recommendation on 3 and 4** (the evidence above is what exists; nothing more can be measured about them without
fixing them):
- **ST1: include.** It breaks a written rule (Rule 3). It is rare, so its effect on outcomes is expected to be nil, and v2's
  comparison will show that rather than assume it.
- **Knowledge record: include.** It changes no behaviour (measured), and fixing it makes saved worlds exact, which every
  copy-based study (ID1) relies on. Of the four, it is the only one that should leave every world bit-identical in
  behaviour: the v2 comparison can check exactly that.

## How v2 is built and checked (each step traceable)

1. **One branch, one commit per change**, each with its own test (A1's exists). The approved order: 1, 2, then 3 and 4 if
   approved.
2. **Zero checks per change:** with each change switched off by a setting, the code equals `nature-v1` exactly (state
   hash, two seeds, 20 years). With 4 on and the others off: people's choices and events identical to v1 over 120 years
   on two seeds (only the knowledge record may differ).
3. **New reference hashes** for v2 (`tests/reference_hashes.json`), CI green on windows-2022.
4. **A frozen comparison, v1 against v2**, before v2 is used: 256 new seeds, 20 founders, 120 years, arms v1, v2 and a
   sham; extinction (paired sign test, bootstrap interval, as every study) and BL0/LK1/MB1a's main measures described.
   Its purpose is to **measure** what v2 changes, not to make v2 "better": any result is reported, and v2 is not tuned.
   (A separate questions file, frozen before it runs.)
5. **The creator signs off v2** after reading that comparison. Only then do studies move to it.

## Decisions for the creator

1. Include **ST1** (recommended) and the **knowledge-record fix** (recommended)?
2. The comparison as described (256 new seeds; v1, v2, sham), or smaller?
3. Order: build v2 now, while TC1 is decided (TC1 runs on v1 and does not depend on v2), or after TC1.
