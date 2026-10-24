# NV5 — Nature version 5: digging goes in (built and checked)

**The creator's decision (24 October 2026):** "yes", to GPT's advice (`../DG1_digging/gpt_view_after_dg1.md`): adopt
digging into nature as a physical possibility, not as a demonstrated cultural innovation. DG1 met its frozen rule
(survival and population not worse); digging was tried by nearly everyone once and almost never used for food.

**v5 = v4 + `digging` (with `pit_keep` 0.5).** `code_v5` is `code_dg1` unchanged (its logging is inert unless a runner
sets it); the whole difference is `v4_to_v5.diff` (actions, config, mind, world).

## Checks (`zero.txt`, `run_nv5.py zero`): **All PASS**

- `code_v5` with `digging` 0 equals `code_v4` (seeds 11 and 501 at 5 years, 501 and 601 at 20).
- v5 equals `code_dg1`'s D arm, the arm DG1 tested (501 and 601, 20 years).
- **The live package `acl/`, with its own defaults, equals v5**; digging acts; reload exact (with a pit held).
- New reference fingerprints "v5"; the live package's regenerated. All 60 tests pass.

## What changes from now

- Future studies run on v5; DG1's D worlds (seeds 13001–13512) are the first v5 control set.
- Still open: realistic rot for bodies (BD2, next, on v5), things on the ground (TG1), water (WA1).
- Tag `nature-v5`.
