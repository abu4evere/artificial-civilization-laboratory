# BD2 — bodies with realistic rot: findings

Frozen as `BD2-frozen` before any data, on GPT's design (`../DG1_digging/gpt_view_after_dg1.md`) and the creator's
"yes". Tables: `results.md`, from `analyse_bd2.py` (written before data). Code: `code_bd2` = `code_v5` + `body_rot`
(`v5_to_bd2.diff`). 1,536 worlds: 512 new seeds 14001–14512 × C (v5: bodies rot as stored food), R (realistic rot by
degree-days), N (v5 without bodies), 20 founders, 120 years. **Run on GitHub's machines** (`cloud-run`, run
40048036820). Zero checks passed there and here.

## Validity

Zero checks passed; all worlds present; one fingerprint. **Manipulation check passes:** median weeks to bones C 118,
R 14; foul person-weeks per person-year C 11.2, R 0.7. **Valid.**

## The frozen reading

**Primary, time-averaged population:** C 29.10, R 26.16, N 24.28.

| comparison | ratio − 1 | 95% interval | reading |
|---|---|---|---|
| R against C (what realistic rot does) | −10.1% | [−14.2%, −5.9%] | **R lower** |
| R against N (does bodies' gain hold?) | **+7.7%** | [+2.3%, +13.4%] | **the gain holds** |
| C against N (BD1 again, on v5; described) | +19.9% | [+14.1%, +26.0%] | |

**Survival:** R died out in 177 of 512, C in 144, N in 189. R against C: R dies out more (p = 0.006); **R against N:
no meaningful effect** (p = 0.35); C against N: C dies out less (p = 0.0003), repeating BD1.

**The adoption rule:** the manipulation check passed, so **realistic rot is proposed for nature (v6). The creator
decides.** Its effect on population and survival is reported, not used to accept or refuse it.

**The prior was partly wrong.** It expected most of the gain to vanish. About two fifths of it survives in population
(+7.7% of +19.9%), though not in survival.

## Described

| arm | bodies | median weeks to bones | foul person-weeks | meals from bodies (rotten, by kin) | learned a death by sight |
|---|---|---|---|---|---|
| C | 53,046 | 118 | 19.7 million | 7,121 (4,480, 3,328) | 206,586 |
| R | 47,047 | 14 | 1.1 million | 2,514 (651, 1,213) | 136,690 |

Median population at year 60 / 120: C 29 / 33, R 26 / 28, N 23 / 18.

## What it means

- **BD1 replicates on today's nature:** with bodies rotting as stored food, population is 20% higher than with no
  bodies and fewer worlds die out.
- **Most of that was the slow rot.** With rot that follows the weather, the living meet rotting bodies about sixteen
  times less often, and the gain shrinks to about 8% in population and nothing measurable in survival.
- **But a real gain remains:** even when bodies are bones in weeks, worlds with bodies hold more people than worlds
  where the dead vanish. With so little rot left, the cause is not settled: the sight of the dead, the warning of
  rot in summer, the dead's food and tools staying where they fell, or all together. Not tested here.
- For nature: realistic rot is the truer physics. Adopting it costs about 10% of v5's population, the part that came
  from an unrealistic number.
