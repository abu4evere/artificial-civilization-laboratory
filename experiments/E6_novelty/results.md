# E6 — Can the world still surprise itself? · Results

Definitions, predictions and the decision rule were frozen in predictions.md before any run. LFA = the first year of the latest lasting novelty in a world (year 0 = the first year).

## Validity (kill criterion)

- Baseline code unchanged during the runs: **yes** (800aa4060848a084).
- E6 code unchanged during the runs: **yes** (b3f7153accc0e681).
- Worlds completed: baseline 8 of 8, E6 8 of 8 (at least 6 each needed).
- Baseline reproduces E5's population every 10 years: 301 yes, 302 yes, 303 yes, 304 yes, 305 yes, 306 yes, 307 yes, 308 yes.
- Recorder read-only (identical state hash with and without it, 20 years): baseline and E6 both verified before the runs.
- **The experiment is valid.**

## Latest first appearance, world by world

| seed | baseline: lived | baseline LFA | baseline share after 100 | E6: lived | **E6 LFA** | E6 share after 100 | E6 later? |
|---|---|---|---|---|---|---|---|
| 301 | 1000 yrs | 206 | 1% | 1000 yrs | **28** | 0% | no |
| 302 | 1000 yrs | 23 | 0% | 1000 yrs | **22** | 0% | no |
| 303 | 1000 yrs | 87 | 0% | 1000 yrs | **25** | 0% | no |
| 304 | 1000 yrs | 13 | 0% | 1000 yrs | **66** | 0% | yes |
| 305 | 54 yrs | 2 | 0% | 70 yrs | **6** | 0% | yes |
| 306 | 1000 yrs | 16 | 0% | 124 yrs | **14** | 0% | no |
| 307 | 53 yrs | 2 | 0% | 103 yrs | **14** | 0% | yes |
| 308 | 419 yrs | 16 | 0% | 96 yrs | **14** | 0% | no |

Lasting novelties first appearing in each century (all worlds pooled):

| century | 0–100 | 101–200 | 201–300 | 301–400 | 401–500 | 501–600 | 601–700 | 701–800 | 801–900 | 901–1000 |
|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 593 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| E6 | 578 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

## The frozen decision rule

- E6 worlds that lived 300+ years (counted): 4 (301, 302, 303, 304).
- Counted E6 worlds with LFA at year 300 or later: 0 (none).
- Counted E6 worlds with LFA at year 100 or earlier: 4 (301, 302, 303, 304).
- Seed pairs where E6's LFA is later than the baseline's: 3 of 8.
- **Verdict: BOTTLENECK REMAINS.**

## Predictions, scored

1. Baseline: LFA ≤ 100 in ≥5 of 8 worlds (7) and under 10% of lasting novelties after year 100 (0.2% pooled). **confirmed**
2. E6: LFA ≥ 300 in at least half the counted worlds (0 of 4). **wrong**
3. E6: ≥25% of lasting novelties after year 100 in ≥5 of 8 worlds (0: none). **wrong**
4. E6: a new tradition (began after year 100, 3+ people, 100+ years) in at least half the surviving worlds (2 of 4). **confirmed**
5. E6: 3 or fewer worlds die out (4: 305, 306, 307, 308). **wrong**
6. E6: a thing shaped from soft stuff, hardened by heat, that holds water, in at least one world (none). **wrong** (reported only)

## New consequences in E6 (descriptive)

| seed | water carried | fire carried |
|---|---|---|
| 301 | 0 | 0 |
| 302 | 0 | 0 |
| 303 | 0 | 0 |
| 304 | 0 | 0 |
| 305 | 0 | 0 |
| 306 | 0 | 0 |
| 307 | 0 | 0 |
| 308 | 0 | 0 |

## The latest lasting novelties in E6 (what appeared last)

- seed 301: year 28: behaviour `('attack',)`; year 16: kind `(('edge', 0), ('reach', 1), ('hard', 0), ('contain', 4), ('warm', 1), ('float', 1), ('tight', 0), ('plastic', `; year 16: behaviour `('play', ('made', (('edge', 0), ('reach', 1), ('hard', 0), ('contain', 4), ('warm', 1), ('float', 1), ('tight'`
- seed 302: year 22: kind `(('edge', 1), ('reach', 1), ('hard', 4), ('contain', 2), ('warm', 0), ('float', 0), ('tight', 0), ('plastic', `; year 22: behaviour `('play', ('made', (('edge', 1), ('reach', 1), ('hard', 4), ('contain', 2), ('warm', 0), ('float', 0), ('tight'`; year 14: behaviour `('flee',)`
- seed 303: year 25: behaviour `('attack',)`; year 18: kind `(('edge', 1), ('reach', 1), ('hard', 4), ('contain', 0), ('warm', 0), ('float', 0), ('tight', 0), ('plastic', `; year 18: behaviour `('play', ('made', (('edge', 1), ('reach', 1), ('hard', 4), ('contain', 0), ('warm', 0), ('float', 0), ('tight'`
- seed 304: year 66: kind `(('edge', 0), ('reach', 3), ('hard', 0), ('contain', 2), ('warm', 0), ('float', 0), ('tight', 0), ('plastic', `; year 66: behaviour `('play', ('made', (('edge', 0), ('reach', 3), ('hard', 0), ('contain', 2), ('warm', 0), ('float', 0), ('tight'`; year 18: behaviour `('make', ('made', (('edge', 0), ('reach', 1), ('hard', 4), ('contain', 0), ('warm', 0), ('float', 0), ('tight'`
- seed 305: year 6: kind `(('edge', 0), ('reach', 3), ('hard', 1), ('contain', 0), ('warm', 0), ('float', 2), ('tight', 2), ('plastic', `; year 6: behaviour `('play', ('made', (('edge', 0), ('reach', 3), ('hard', 1), ('contain', 0), ('warm', 0), ('float', 2), ('tight'`; year 4: behaviour `('make', ('made', (('edge', 0), ('reach', 1), ('hard', 0), ('contain', 3), ('warm', 1), ('float', 1), ('tight'`
- seed 306: year 14: behaviour `('make', ('made', (('edge', 3), ('reach', 0), ('hard', 3), ('contain', 0), ('warm', 0), ('float', 0), ('tight'`; year 14: kind `(('edge', 1), ('reach', 0), ('hard', 4), ('contain', 0), ('warm', 0), ('float', 0), ('tight', 0), ('plastic', `; year 14: behaviour `('make', ('made', (('edge', 1), ('reach', 0), ('hard', 4), ('contain', 0), ('warm', 0), ('float', 0), ('tight'`
- seed 307: year 14: behaviour `('make', ('made', (('edge', 1), ('reach', 0), ('hard', 4), ('contain', 0), ('warm', 0), ('float', 0), ('tight'`; year 12: behaviour `('put', ('thing', 'seeds'), ('into', 'stash'))`; year 6: behaviour `('make', ('made', (('edge', 0), ('reach', 0), ('hard', 4), ('contain', 0), ('warm', 0), ('float', 0), ('tight'`
- seed 308: year 14: kind `(('edge', 0), ('reach', 4), ('hard', 1), ('contain', 4), ('warm', 1), ('float', 3), ('tight', 0), ('plastic', `; year 11: behaviour `('put', ('thing', 'seeds'), ('into', 'stash'))`; year 8: kind `(('edge', 1), ('reach', 1), ('hard', 4), ('contain', 0), ('warm', 0), ('float', 0), ('tight', 0), ('plastic', `

## New traditions in E6 (began after year 100)

- seed 301: `symbol:/\v|grave` 130 years from year 149; `symbol:vo/|grave` 100 years from year 399
- seed 302: none
- seed 303: none
- seed 304: `belief:fiber@2` 670 years from year 339; `belief:fiber@1` 660 years from year 349; `symbol:|^\|water` 110 years from year 349; `symbol:/.\|water` 100 years from year 429
- seed 305: none
- seed 306: none
- seed 307: none
- seed 308: none

## Checks (read-only, after the run)

**Was the new physics used?** (`investigate_e6.py`, from the saved snapshots)
- **Shaping soft clay: yes, heavily.** 36–61 shaped kinds per world, and clay things bound into larger things.
- **Heat: almost never.** In 8 worlds, up to 1000 years each, one thing was ever held in a fire and changed: a
  raw lump of clay fired once in seed 302 (`clay^5`). No shaped thing was ever fired.
- **Food held in a fire:** never by 3 or more people in any decade. No food was kept at the end of any world.
- **Holding water:** one watertight thing was ever made, in seed 304: hide bound to bone with fibre. Nobody
  ever filled anything; no water or fire was ever carried.

So E6 tested a world where the new physics existed but its deep branch stayed out of reach. What people did
use, soft clay shapes, behaves like any other made thing: it helps carry, cut or reach a little better. That is
the fixed list of multipliers again, and its novelties all came in the first decades.

**Why the deep branch stayed shut.** Heat needs a fire where the person stands. Fire was already rare and brief
before E6: in development worlds, adults stood at a burning fire for only tens to about 200 person-weeks in 150
years. On top of that, at a fire the option to heat something competes with everything else they could do,
pulling only as something untried. The creator decided beforehand not to touch fire, so this is what the world
does on its own.

**E6 worlds were harsher, cause not established.**
- 4 worlds died out, against 3 in the baseline. Seed 306 lived 1000 years in the baseline and 124 in E6.
- The four survivors were smaller at year 1000: 37, 56, 58, 38, against 86, 68, 65, 36 (and 61) in the baseline.
- Starvation was a larger share of deaths: 38–55%, against 38–41%.

Time use did not change. In the first century adults spent about 40% of their weeks foraging in both worlds,
and gathering did not grow, so clay did not take time away from food. Histories diverge from the first week
(the new code draws random numbers differently), so with 4 or 5 surviving worlds a difference this size may be
chance. It is not explained here.

**One thing E6 had and the baseline did not: late traditions.** In 2 of the 4 surviving E6 worlds,
traditions began after year 100 and lasted 100–670 years. In seed 304, leaving fibre in summer and autumn
began around year 340 and lasted the rest of the millennium; there were also new mark meanings for water and
graves. No baseline world had any tradition that began after year 100. But these use the old mechanics
(placing things, marks), not the new physics, and 2 worlds against 0 is suggestive at most.
