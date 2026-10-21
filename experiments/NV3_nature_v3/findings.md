# NV3 — Nature version 3: built and checked

Frozen as `NV3-frozen` (the creator passed on GPT's recommendations). **v3 = v2 + `parts_first`**: after a visibly
failed lesson, the teacher shows a part the learner lacks.

## What was built

- `code_v3`: a copy of `code_v2` plus LM1's `parts_first` lines only, without the memory setting and without LM1's
  logging. The whole difference is `v2_to_v3.diff` (config: one setting; `information.hear_how`: the part lesson).
- **v3 is selected by settings:** v2's four plus `parts_first = 1`.
- **The live package `acl/`** now defaults to v3 (`parts_first = 1`). Its information module is identical to
  `code_v3`'s.

## Checks (`zero.txt`, `run_nv3.py zero`): **All PASS**

- `code_v3` with `parts_first` 0 equals `code_v2` (seeds 11 and 501 at 5 years, 501 and 601 at 20 years).
- v3 equals `code_lm1`'s L arm, the arm LX1 tested, on seeds 501 and 601 over 20 years.
- `parts_first` changes the world (it acts).
- Reload is exact.
- New reference fingerprints "v3" are in `tests/reference_hashes.json` with `test_nature_v3_replays`. The live
  package's fingerprints now equal v3's. All 58 tests pass locally.

## The comparison

LX1 is the v2-against-v3 comparison (512 new seeds, frozen before data). Its C equals v2 and its L equals v3, both
shown by zero checks. Extinction was 181 in C against 177 in L: no meaningful effect. Passing on rose by +2.0 points.
No new run was made.

## What changes from now

- **Future studies run on v3**, and every record names its version. LX1's L worlds (seeds 7601–8112) are the first
  v3 control set.
- `nature-v2`, `code_v2` and every earlier result stay as they were and are never re-read under v3.
- Tag `nature-v3`.
