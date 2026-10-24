# BD2 — bodies with realistic rot: results

Frozen as `BD2-frozen`. run_bd2.py, analyse_bd2.py (written before data).

## Validity

- Zero checks: **yes**
- All worlds present: **yes**
- One fingerprint (`code_bd2`): **yes**
- Manipulation check: median weeks to bones C 118, R 14; foul weeks per person-year C 11.15, R 0.69: **passes**

**Valid.**

## Primary: time-averaged population (GPT's choice)

Means: C (v5, bodies rot as stored food) **29.10**, R (realistic rot) **26.16**, N (no bodies) **24.28**.

| comparison | ratio - 1 | 95% interval | reading |
|---|---|---|---|
| (1) R against C: what realistic rot does | -0.101 | [-0.142, -0.059] | **R lower** |
| (2) R against N: does bodies' gain hold? | +0.077 | [+0.023, +0.134] | **the gain holds** |
| C against N (described: BD1 again, on v5) | +0.199 | [+0.141, +0.260] | |

## Survival (major secondary)

| comparison | died out (arm / other) | saved / lost, p | effect | reading |
|---|---|---|---|---|
| r against c | 177 / 144 | 53 / 86, p 0.00643 | -0.064 [-0.109, -0.020] | **changes survival (r dies out more)** |
| r against n | 177 / 189 | 75 / 63, p 0.349 | +0.023 [-0.021, +0.068] | **no meaningful effect** |
| c against n | 144 / 189 | 99 / 54, p 0.000343 | +0.088 [+0.041, +0.135] | **changes survival (c dies out less)** |

## The adoption rule (frozen)

**Realistic rot is proposed for nature (v6)**: the manipulation check passed, and it is the truer physics. What it does to population and survival is reported above and is not used to accept or refuse it, so the rule never tunes nature toward an outcome. The creator decides.

## What happened to the bodies (described)

| arm | bodies | median weeks to bones | foul person-weeks | meals from bodies | from rotten | by kin | seen | tools to kin |
|---|---|---|---|---|---|---|---|---|
| c | 53,046 | 118 | 19,743,506 | 7,121 | 4,480 | 3,328 | 206,586 | 6,666 |
| r | 47,047 | 14 | 1,100,067 | 2,514 | 651 | 1,213 | 136,690 | 5,756 |

## Beside it (population first)

| arm | median population, year 60 / 120 | deaths | starvation |
|---|---|---|---|
| c | 29 / 33 | 53046 | 19039 |
| r | 26 / 28 | 47047 | 15478 |
| n | 23 / 18 | 45014 | 15052 |
