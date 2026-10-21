# FX3 — food that must be opened, at gentler settings: results

Frozen as `FX3-frozen` (Revision 2). run_fx3.py, analyse_fx3.py; code `code_fx2` unchanged. Settings are operational.

## Validity

- Zero checks (share 0 = code_v2; every arm acts; the tool route acts; read-only; reload exact): **yes**
- All worlds present: **yes**
- One fingerprint (`code_fx2`): **yes**

**Valid.**

## Baseline (rule 14)

C died out in 80 of 256 worlds (31.2%).

## Primary 1: does the tool route change survival? (always read)

| comparison | tool arm died out | tool-free arm died out | saved / lost | p | Holm p | effect (tool-free − tool) | 95% interval | reading |
|---|---|---|---|---|---|---|---|---|
| S25 against S25_0 | 176 | 184 | 47 / 39 | 0.451 | 0.901 | +0.031 | [-0.039, +0.102] | **no meaningful effect** |
| B50 against B50_0 | 137 | 145 | 49 / 41 | 0.461 | 0.901 | +0.031 | [-0.039, +0.102] | **no meaningful effect** |

## Primary 2: does the tool route change tool use? (carrying a hard thing)

| comparison | seeds compared | median share of adult forage-weeks with hardness ≥ 40 in hand, tool / tool-free | mean difference | 95% interval | p | Holm p | reading |
|---|---|---|---|---|---|---|---|
| S25 against S25_0 | 256 | 0.404 / 0.300 | +0.0928 | [+0.0748, +0.1100] | 3.77e-19 | 7.53e-19 | **the tool route changes tool use** |
| B50 against B50_0 | 256 | 0.280 / 0.270 | +0.0220 | [+0.0052, +0.0396] | 0.0219 | 0.0219 | **the tool route changes tool use** |

## Each arm against C (described)

| arm | died out | against C: saved / lost | effect (C − arm) | 95% interval |
|---|---|---|---|---|
| s25 | 176 | 10 / 106 | -0.375 | [-0.441, -0.309] |
| s25_0 | 184 | 9 / 113 | -0.406 | [-0.473, -0.340] |
| b50 | 137 | 16 / 73 | -0.223 | [-0.289, -0.156] |
| b50_0 | 145 | 15 / 80 | -0.254 | [-0.320, -0.184] |

## Beside it (described; population first)

Carrying a hard thing is not using it; the last two columns read what was actually used on embedded food.

| arm | median population, year 60 / 119 | births per woman-year | blocked for want of a partner | embedded share of adults' food | opened with a hard thing (any / ≥ 0.4) | forage-weeks a hard thing was used on embedded food |
|---|---|---|---|---|---|---|
| c | 26 / 26 | 0.133 | 0.534 | 0.0% | – | 0.0% |
| s25 | 7 / 0 | 0.126 | 0.575 | 13.4% | 57.3% / 52.4% | 24.3% |
| s25_0 | 7 / 0 | 0.126 | 0.583 | 10.9% | 0.0% / 0.0% | 0.0% |
| b50 | 12 / 0 | 0.131 | 0.540 | 38.1% | 34.9% / 30.7% | 23.5% |
| b50_0 | 10 / 0 | 0.127 | 0.553 | 37.1% | 0.0% / 0.0% | 0.0% |
