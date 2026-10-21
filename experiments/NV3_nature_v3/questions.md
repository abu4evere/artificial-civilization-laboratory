# NV3 — Nature version 3: parts-first teaching goes in (DRAFT for the creator; nothing built or run)

**Why.** LX1 (`../LX1_parts_first_survival/findings.md`, `LX1-done`) met the adoption rule fixed before its data.
Parts-first teaching (L1) costs no survival: C died out in 181 of 512, L in 177. It raises passing on again, by +2.0
points (LM1: +2.2). By that rule, **L1 enters nature: v3 = v2 + `parts_first`.** This plan says how the switch is
built and checked, so that every result stays traceable. It is not a new experiment.

**What stays.** `nature-v2` stays exactly as it is (tagged). Every result so far stays on the version it ran on and is
never re-read under v3.

## What v3 is

| setting | v2 | v3 | the change |
|---|---|---|---|
| `parts_first` | `0` | `1` | after a visibly failed lesson (the learner could not follow a composite), the teacher shows a part the learner lacks. This is LM1's code, unchanged. |

Nothing else changes. M (`memory_ties_by_age`) stays **off**: it had no meaningful effect in LM1.

## How v3 is built and checked

1. **Code `code_v3`:** a copy of `code_lm1`'s acl package (already proven equal to `code_v2` with its settings off, by
   LM1's and LX1's zero checks), with **`parts_first` defaulting to 1**, in one commit with its own test.
2. **Zero checks (hard stops):**
   - `code_v3` with `parts_first` 0 equals `code_v2` (state hash, seeds 501 and 601, 20 years).
   - `code_v3` as it is (v3) equals `code_lm1` in its L arm on the same seeds: the same world, exactly.
   - Reload is exact.
3. **New reference fingerprints** "v3" (seeds 11 and 501, 5 years) in `tests/reference_hashes.json`, with a test;
   CI green on windows-2022.
4. **No new comparison run (Decision 1).** LX1 already is the v2-against-v3 comparison on 512 new seeds: its C equals
   v2 and its L equals v3, both by zero checks. NV2's sham arm was quiet, so it is not repeated.
5. **Baseline for future studies:** LX1's L worlds (seeds 7601–8112) are the first v3 control set.
6. **The live package** `acl/` is updated to v3 only after the creator signs off, and the website's method page says
   "nature v3".
7. Tag `nature-v3`.

## Decisions for the creator

1. **No new comparison run; LX1 counts as the v2/v3 comparison** (recommended), or a separate 256-seed comparison with
   a sham, as NV2 did (about 2 hours on GitHub).
2. **M stays off** (recommended; no effect in LM1).
3. Go ahead: build and check v3 as above, then move future studies to it.
