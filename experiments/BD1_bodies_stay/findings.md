# BD1 — bodies stay: findings

Frozen as `BD1-frozen` before any data, after GPT's ideas and review, on the creator's instruction. Tables:
`results.md`, from `analyse_bd1.py` (written before data). Code: `code_bd1` = `code_v3` + `bodies_stay`
(`v3_to_bd1.diff`). 1,024 worlds: 512 new seeds 12001–12512 × C (v3) and B, 20 founders, 120 years. **Run on GitHub's
machines** (`cloud-run`, run 39911136459). Zero checks passed there and here.

## Validity

Zero checks passed; all worlds present; one fingerprint. **Manipulation check passes:** a body in every world with a
death; bodies turn to bones; rotten bodies met in all 512 worlds. **Valid.**

## The frozen reading

| check | C (v3) | B (bodies stay) | effect | reading |
|---|---|---|---|---|
| died out | 189 of 512 | **146 of 512** | 95 saved / 52 lost, p = 0.0005; C − B +0.084 [+0.037, +0.129] | **changes survival (B dies out less)** |
| time-averaged population | 24.08 | **28.62** | +18.9% [+12.7%, +25.3%] | **safe** |

**The adoption rule:** survival and population are not worse, so `bodies_stay` **is proposed for nature (v4). The
creator decides.**

**The prior was wrong.** It expected no effect on survival. Bodies staying saved about one world in twelve.

## What happened to the bodies (described)

- 51,500 bodies; 49,232 became bones; median **119 weeks** to bones (the body rots at v3's rate for loose food).
- **Eating from bodies: 7,009 meals** in 496 of 512 worlds (from 7,006 bodies, by 6,255 people): almost always one
  meal per body. 3,275 by kin of the dead; 4,524 from a rotten body. 74,000 food units eaten of 769,000 in bodies (10%).
  Meals rose over time (335 in the first decade, about 900 a decade by the end), with the population.
- People next to a rotten body: **19.3 million person-weeks**, about 11 weeks per person-year.
- 200,340 times someone learned of a death from the sight of the body; 6,653 times a partner or child took the tools.

## Why (exploratory, after the results; `explore/results_explore.md`)

A breakdown on 64 of the same seeds, each arm switching one part off, labelled exploratory: without **disgust at
rot**, 26 of 64 worlds died out (C 21, B 12); without knowing by sight, 14; without meat (and so without rot), 20. The
gain goes with **disgust at rot**, not with eating the dead or with knowing of deaths.

The assistant's reading (not tested): disgust works through people's memory of places. A rotten body makes a place
feel worse, and **people die most where life is hard**: so the living learn to leave the places that are killing
them. The dead become, without anyone meaning it, a warning about the land. That is a real effect of a real feeling,
but its size here depends on a number that is not realistic: bodies rot for about two years (v3's rate for stored
plant food), so the living meet rotting bodies for far longer than real bodies take to become bones (weeks to months
in warm weather, longer in cold; GPT's point that rot should follow conditions).

## The assistant's recommendation (for the creator)

Do **not** adopt BD1 as it is, despite passing its rule. First correct the rot to a realistic, weather-dependent
time (a separate, frozen confirmation: "BD2"), and test again with disgust's size as a documented assumption. If the
gain holds with realistic rot, bodies (and disgust) enter nature with their real effect known. If it shrinks, the
first result came from a number, not from nature.
