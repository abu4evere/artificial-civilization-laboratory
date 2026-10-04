# E7: implementation notes (written before any run)

`E7_passive.md` is the frozen pre-registration and is not edited. This file records what was changed in
`code_e7/` after an audit against that spec on 2026-10-04, **before any E7 run**, and how the parts of the
spec that cannot be implemented literally were read.

Only `code_e7/acl/biology.py` differs from the verified E6 code (`../E6_novelty/code_e6/`, fingerprint
`b3f7153accc0e681`). `mind.py`, `person.py`, `thought.py` and `actions.py` are byte-identical to E6, as §2 requires.

## Fixes to the E7 code

| # | Problem in the first E7 code | Spec | Fix |
|---|---|---|---|
| 1 | **Crash.** A passively fired thing was learned as `{"verb": "heat", "target": ...}`; every reader of a heat recipe (`mind.py`, `knowhow.py`, `historian.py`, `actions.py`) uses `"part"`. The next decision raised `KeyError: 'part'`, so the first passive firing in any world would have ended that run (§9 kill criterion). The tests passed because none ran the world after a firing. | §3.2, §9 | Recipe is `{"verb": "heat", "part": ..., "level": ...}`, the same shape as an active one. New test runs a year after a firing. |
| 2 | Food on a fire tile was made `kept` (as if held in the fire), so every person by a fire got the 15% "goes further" benefit and the slow-rot-anywhere benefit for free. | §3.2.3 says only that food by a fire rots at `smoke_keep`, which E6 already does. | Removed. Person-weeks with food beside a fire are only counted (`food_by_fire`) for FEC_preserved. |
| 3 | Firing used a fixed heat of 6, whatever the fire. | §3.2.2: only at heat ≥ 6, hardness scales with fire intensity. | Uses the tile's `fire_heat`; nothing fires below 6 (a fiber fire is 5). |
| 4 | Only shaped clay things fired; carried raw clay did not. | §3.2.2: "a plastic material (clay) or shaped clay item". | Dry raw clay carried by a hot fire fires one lump a week, through the same `matter.heat` rule the active action uses. The lump joins what is carried under the usual 3-thing limit (lowest-valued thing dropped). |
| 5 | Wading never filled anything: river tiles are not `water` tiles in this world (they can be walked), so only lake/sea tiles, reachable only by boat, counted. | §3.1.2: "a river or lake tile". | A river tile counts as submerging. |
| 6 | Rain was blocked by a heap with cover ≥ 0.3 (the soaking threshold). | §3.1.1: blocked only if cover > 0.5. | Uses > 0.5. |

## Readings of the spec

- **Items on uncovered tiles (§3.1.1, §3.2.1).** In this world, made things are only ever carried. Nobody
  can set one down, and a dead person's things go to an heir or are lost. Nothing can lie on a tile, so
  that part of the spec has nothing to act on. Material heaps on fire tiles are not fired either, because
  a heap holds amounts of raw material, not things.
- **"Accumulates water proportional to rainfall" (§3.1.1).** Rain is one yes/no per week, so a rainy week
  fills an open watertight thing to capacity.
- **Wading "through" a river (§3.1.2).** Only the tile a person ends the week on is checked. Tiles they
  passed through are not.
- **Drinking (§3.1.3)** already existed in E6 (`weather.drink`): carried water is drunk only where no fresh
  water can be reached, and it credits the thing through `knowhow.judge_item`.
- **New Consequence 3 (food eaten past its rot threshold)** cannot be measured. Food is one pooled amount
  per person with no age.
- **Event names.** `food_by_fire` is not `food_smoked`, because the P1 test bans "smoked" as an invention
  word.

## Recorder and scripts (new, written before any run)

- `novelty_e7.py`: E6's recorder unchanged, plus FEC counts, distance to fresh water (river or lake tile)
  for every drink from a carried vessel, and fired-clay objects followed from first carrier to last
  carrier.
- `run_e7.py`: runs both arms, checks the recorder is read-only first, and records each run's code
  fingerprint before and after.
- `analyse_e7.py`: applies §7–§9 as written. Its operational readings are printed as "Reading:" lines in
  `results.md`.

E7 code fingerprint after these fixes: see `code_e7/CODE_HASH.txt` (sha256 over `code_e7/acl/*.py`, the
E6 convention).
