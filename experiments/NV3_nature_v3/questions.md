# NV3 — Nature version 3: parts-first teaching goes in (SIGNED OFF 21 October 2026; frozen as `NV3-frozen` before any code)

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

## Sign-off (21 October 2026)

The creator passed on GPT's recommendations as the answer (the creator has delegated these decisions to GPT's
review before):
1. Use LX1 as the v2-against-v3 comparison, provided its design supports it. **Checked:** LX1's seeds, arms, outcomes
   and analysis were frozen before any data (`LX1-frozen`). Its C is `code_lm1` with both settings 0, shown equal
   to `code_v2` by zero checks, and its L differs from C only by `parts_first`. So L against C is v3 against v2, and
   LX1 counts. No new comparison run.
2. The memory fix stays **off**.
3. Build and check v3, but do not switch studies to it until the checks pass. Preserve v2. Document the v2–v3
   difference. Label the version in every record.
- The Minecraft idea stays parked.

## Operational note (before any code; rule 19)

- `code_v3` is `code_v2` plus **only** LM1's `parts_first` lines (`information.hear_how`, `config`), without the
  memory setting and without LM1's logging. The full v2–v3 difference is that diff, kept as `v2_to_v3.diff`.
- Following NV2's convention, the setting defaults to the old behaviour (`parts_first = 0`), and **v3 is selected
  by settings**: v2's four plus `parts_first = 1`, in a `V3` dict. This replaces "defaulting to 1" in step 1.
  Behaviour is the same either way, and "v3 with the setting off = v2" stays a direct check.
- Added zero check: v3 equals `code_lm1`'s L arm (with v2's settings) on seeds 501 and 601 over 20 years.
