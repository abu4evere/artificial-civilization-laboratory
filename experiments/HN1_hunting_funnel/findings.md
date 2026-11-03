# HN1: Where do v11's hunts fail? — findings

**A read-only study on nature v11** (`code_v11`).
- Frozen as `HN1-frozen`.
- Signed off under the creator's sleep-mode autonomy. Council round 53: GPT 95%, Gemini 98%, DeepSeek about 78%, the
  assistant 80%.

**The run:**
- GitHub Actions run 41595719392.
- The zero checks ran locally (`zero_local.log`: All: PASS). They show:
  - the observer is read-only;
  - reload is exact;
  - the funnel adds up, against an independent count from the hunt events (359 = 359).
- 32 worlds (seeds 22601–22632). LP, 200 years; years 100–200 counted.
- Every number comes from `analyse_hn1.py`, written before data. Full tables are in `results.md`.

**Validity:** the zero checks pass; all 32 worlds are present under `code_v11`'s fingerprint.

## The answer
**Hunts fail at the roll, never for lack of prey. A hunting week returns about 2% of a foraging week. Even a hunt that
always succeeded could not reach the forager range, because a kill is small.**

| quantity | value [95%] |
|---|---|
| F, the failed hunts with no prey on the tile | **0.0000 [0.0000, 0.0000]** (0 of 1,732 failures) |
| routing for HR1 (frozen) | **the base chance** (`hunt_base_chance`) |
| return ratio, pooled (food per hunter-week ÷ food per forage-week) | **0.0229 [0.0186, 0.0272]** |
| return ratio, matched (same person, season, year, plant band) | 0.0177 [0.0138, 0.0219] (1,570 matched, 261 dropped) |
| funnel: no prey / roll failed / success | 0.000 / 0.946 / **0.054** |
| success, armed / bare-handed | **0.058 / 0.047** |
| food kept per hunter-week, armed / bare-handed | 0.517 / 0.398 |
| meat lost to carrying room | 0.000 |
| **F8:** meat the decision expects per success / meat actually taken | **36.75 / 8.79** |
| adult hunter-weeks / adult-weeks (16–49) | 1,831 / 14,006,788 (one week in about 7,650) |

**The ceiling** (arithmetic on the numbers above, by the assistant; checked by script):
- a forage-week yields 20.77 food, and a success yields 8.79;
- **at the cap of 0.92 success, the ratio would be 0.39. At 100% it would be 0.42.**
- Reaching 0.5 would need a 118% success rate, and the Aché's 1.1 would need 260%.
- **So calibrating the base chance alone cannot reach the frozen target range (0.5–1.5).**

**The assistant's prior:**
1. F > 0.5: **wrong**. F = 0: hunters pick tiles where prey stand, and animals move only before decisions.
2. R between 0.02 and 0.10: **right** (0.023).
3. Expected meat per success about 3 times the realized: **right**, a little stronger (4.2 times).

## Described
- **F7, success by species on single-species tiles:** rabbit 0.078, deer 0.099, bison 0.098, fish 0.098, against the
  unused table rates of 0.40, 0.16, 0.10 and 0.25.
  - **A correction to the plan's description:** these counts were taken for **every** hunt in all 200 years and at all
    ages (14,128 rabbit attempts and so on), not only adults in years 100–200 as the other measures were. The code
    counts them before its age and year filter. They describe the whole run.
  - **The flat base chance dominates.** Each species' success sits near 0.08–0.10, whatever the table says.
- **Hunting is almost never chosen:** one adult week in about 7,650. The decision still expects more than four times
  the meat a kill gives (F8), so the stale expectation makes hunting look **better** than it is, and it is still not
  chosen.
- **Weapons barely help:** armed hunters succeed 5.8% against 4.7% bare-handed. The tool factor multiplies a tiny base.

## What it means for HR1 (for the council, round 54)
- **The frozen routing rule picks the base chance,** but the frozen target range cannot be reached with it alone.
- **The other limit is the size of a kill:** small game dominates (rabbits give 3 each), and meat per success is 8.8.
- **HR1 must therefore be redesigned before it is frozen.** Choices to put to the council:
  - (a) calibrate **two** existing things, the base chance and the meat per kill (species meat, or the mix of prey),
    each to evidence;
  - (b) fix F7 (use the per-species catch rates the table already holds) and F8 (the decision expects what a kill
    really gives), then measure again;
  - (c) accept a target below 0.5, set from the evidence that is reachable;
  - (d) stop the hunting line and turn to the habit/ends tension AM1 found.

## Blind recompute (`recompute_hn1.md`)
- **GPT** (chat `6ae99e3b`), **Gemini 3.1 Pro** (chat `a43e31c647c81a4e`) and **DeepSeek** (chat `c685650b`, by hand)
  recomputed F, the routing, R and the funnel shares, blind, from the per-world counts.
- **All three match every value, the routing and the shares.** Interval ends differ by at most 0.0004.
- **HN1 is final.**
