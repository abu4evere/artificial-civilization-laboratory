# NV4 — Nature version 4: bodies stay (built and checked)

**The creator's decision (23 October 2026):** "Go with bodies" — BD1's change is adopted into nature by BD1's frozen
rule (survival and population not worse; the creator accepts the evidence), **without** the realistic-rot
confirmation the assistant recommended. That caveat stays on record: in v4 a body rots at v3's rate for loose food
(about two years to bones), longer than real bodies; and BD1's gain goes with disgust at rot (exploratory). A
realistic-rot study on v4 remains open (docs/OPEN_DECISIONS.md).

**v4 = v3 + `bodies_stay`.** `code_v4` is `code_bd1` unchanged (its read-only logging is inert unless a runner sets
it); the whole difference is `v3_to_v4.diff` (config, actions, biology, world).

## Checks (`zero.txt`, `run_nv4.py zero`): **All PASS**

- `code_v4` with `bodies_stay` 0 equals `code_v3` (seeds 11 and 501 at 5 years, 501 and 601 at 20).
- v4 equals `code_bd1`'s B arm, the arm BD1 tested (501 and 601, 20 years).
- **The live package `acl/`, with its own defaults, equals v4** (501 and 601, 20 years): its actions, biology and
  world modules are `code_v4`'s; its config now has `bodies_stay = 1`.
- `bodies_stay` changes the world; reload is exact.
- New reference fingerprints "v4" (`test_nature_v4_replays`); the live package's fingerprints regenerated (now
  equal v4's). All 59 tests pass.

## What changes from now

- **Future studies run on v4**; BD1's B worlds (seeds 12001–12512) are the first v4 control set. Every record names
  its version. v3 and earlier results stay as they were.
- The live world, when next started from its save, continues under v4 (its saved settings have no `bodies_stay`, so
  the new default applies), as happened with v3.
- Tag `nature-v4`.
