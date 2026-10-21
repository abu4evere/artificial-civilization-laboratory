# RT1b — residence time with the walk to water counted: results

Frozen as `RT1b-frozen`. run_rt1b.py, analyse_rt1b.py.

## Validity

- Zero checks (off = code_rt1; without a base it does nothing; it acts; read-only; reload exact): **yes**
- All worlds present: **yes**
- One fingerprint (`code_rt1b`): **yes**
- Manipulation check, r4: adults change the tile they sleep on in **20.5%** of weeks (needed 15–35%): **yes**
- Manipulation check, r4w: adults change the tile they sleep on in **20.4%** of weeks (needed 15–35%): **yes**
- Manipulation check, the fix: of R4w's thirsty adult-weeks, **1.1%** followed a chosen trip to water (needed under 5%): **yes**

**Valid.**

## Baseline (rule 14)

C died out in 91 of 256 worlds (35.5%).

## Extinction (the frozen reading)

| comparison | R4w died out | reference died out | saved / lost | p | Holm p | effect (reference − R4w) | 95% interval | reading |
|---|---|---|---|---|---|---|---|---|
| R4w against C | 143 | 91 | 25 / 77 | 2.45e-07 | 4.9e-07 | -0.203 | [-0.277, -0.129] | **changes survival** |
| R4w against R4 | 143 | 148 | 45 / 40 | 0.665 | 0.665 | +0.020 | [-0.051, +0.090] | **no meaningful effect** |

## Beside it (described; population first, rule 18)

| arm | median population, year 60 / 119 | births per woman-year | blocked for want of a partner | between-lineage meeting | thirst deaths, years 0–39 / 0–119 | adult starvation deaths, years 0–39 | weeks changing tile | thirsty after a chosen trip to water | sent back from water and still short |
|---|---|---|---|---|---|---|---|---|---|
| c | 23 / 20 | 0.131 | 0.536 | 0.1942 | 1801 / 2400 | 1979 | 55.1% | 1.0% | – |
| r4 | 8 / 0 | 0.128 | 0.534 | 0.2362 | 2859 / 3343 | 1943 | 20.5% | 50.4% | – |
| r4w | 10 / 0 | 0.127 | 0.534 | 0.1924 | 2782 / 3215 | 2182 | 20.4% | 1.1% | 0.000 (of 4996417) |
