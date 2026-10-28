# NV8 — Nature version 8: made things drop instead of vanishing (built and checked)

**The creator's decision (27 October 2026):** asked whether to make OP1's law real ("If yes: both models consulted,
code_v8 with zero checks, the tests, and a nature-v8 tag"), the creator answered **"go ahead"**.

## The evidence
- **OP1 (final; recomputed blind by GPT and Gemini):** the law was supported on its mechanism.
  - 0.939 [0.917, 0.957] of dropped things were picked up, 0.961 by others;
  - made things held per adult rose from 0.555 to 1.018;
  - the run was flagged for population (0.845).
- **PD1 (final; 64 paired seeds; recomputed by both):** the flag does not repeat.
  - Population in years 100–200: o ÷ c **0.985** (the sham 0.957).
  - No cause of death or birth rate differs beyond the sham band.
  - Fighting tools are more often in hand (0.40 → 0.59), but there are no more attacks or killings.
- **Both models consulted on adoption** (`docs/gpt_view_adopt_v8_2026-10-27.md`): GPT yes (90%), Gemini yes (98%).

## v8 = v7 + `ground_items` on
- **Drop, not delete:** whenever the 3-item carry limit removes a made thing (by making, heating, or inheritance from a
  body), it is left on the ground where the person stands, unchanged.
- **Picking up:** each week, a person aged 12+ standing on a tile with things on the ground, with room in hand, picks
  them up: the one they value most first, until full. This draws no random numbers.
- **Things on the ground do not rot or wear,** as with tools on a body.

`code_v8` is OP1's `code_op1` with the setting's default changed to 1. The difference from v7 is `v7_to_v8.diff`.

## Checks (`zero.txt`, `run_nv8.py zero`): **All PASS**
- `code_v8` with `ground_items` 0 equals `code_v7` (seeds 11 and 501 for 5 years; seeds 501 and 601 for 20 years).
- v8 equals `code_op1`'s arm o, the arm OP1 and PD1 tested (seeds 501 and 601, 20 years).
- The live package `acl/` with its own defaults equals v8.
- The setting acts.
- Reload is exact with things on the ground.
- **Tests:**
  - new reference hashes "v8";
  - the live package's hashes regenerated, and equal to v8's;
  - v7's kept unchanged;
  - **all 63 tests pass.**

## Known limits (recorded at adoption; GPT's and Gemini's notes)
- **Picking up is passive** (ages 12+, room in hand, the most valued first, no choice). It is "physical persistence plus
  passive acquisition, not evidence that agents learned to retrieve tools" (GPT).
- **Things on the ground never decay.** OP1 left 3,911 on the ground at year 200 across 32 worlds (about 120 per
  world). Accumulation over 1,000 years is to be checked.
- **Fighting tools are more often in hand** (0.40 → 0.59), though attacks and killings did not rise (PD1).
- **v7's findings stay v7's.** They do not become v8 findings. Every study from now states its nature version.

## From now
Future studies run on v8 (`experiments/NV8_nature_v8/code_v8`). `code_v7` is kept, so the change can be undone. Tag
`nature-v8`.
