# FX2 — food that must be opened: results

Frozen as `FX2-frozen`. run_fx2.py, analyse_fx2.py. `embedded_share` 0.5 and `embedded_bare` 0.2 are operational assumptions, not measured from real land.

## Validity

- Zero checks (share 0 = code_v2; E and E0 act; read-only; reload exact): **yes**
- All worlds present: **yes**
- One fingerprint (`code_fx2`): **yes**
- Manipulation check, e: embedded food is **35.1%** of adults' foraged food (needed ≥ 25%): **yes**
- Manipulation check, e0: embedded food is **30.0%** of adults' foraged food (needed ≥ 25%): **yes**

**Valid.**

## Baseline (rule 14)

C died out in 96 of 256 worlds (37.5%).

## (1) Does making hard things useful change tool use? E against E0

| seeds compared | median share of adult forage-weeks with hardness ≥ 40 in hand, E / E0 | mean difference (E − E0) | 95% interval | p (Wilcoxon) | Holm p | reading |
|---|---|---|---|---|---|---|
| 256 | 0.396 / 0.244 | +0.1241 | [+0.1058, +0.1424] | 1.42e-25 | 2.84e-25 | **making hard things useful changes tool use** |

## (2) Survival when food is harder to reach but tools can help, E against C; (3) does the tool benefit change survival, E against E0

| comparison | E died out | reference died out | saved / lost | p | Holm p | effect (reference − E) | 95% interval | reading |
|---|---|---|---|---|---|---|---|---|
| E against C | 256 | 96 | 0 / 160 | 1.37e-48 | 4.11e-48 | -0.625 | [-0.684, -0.566] | **changes survival** |
| E against E0 | 256 | 256 | 0 / 0 | 1 | 1 | +0.000 | [+0.000, +0.000] | **no meaningful effect** |

## Beside it (described; population first, rule 18)

Holding a hard thing is not proof that anyone found the opening mechanism; the last three columns read what was actually used on embedded food.

| arm | median population, year 60 / 119 | births per woman-year | blocked for want of a partner | embedded share of adults' food | opened with a hard thing (any / ≥ 0.4) | forage-weeks a hard thing was used on embedded food |
|---|---|---|---|---|---|---|
| c | 22 / 22 | 0.128 | 0.550 | 0.0% | – | 0.0% |
| e | 0 / 0 | 0.110 | 0.617 | 35.1% | 68.8% / 63.7% | 38.6% |
| e0 | 0 / 0 | 0.131 | 0.541 | 30.0% | 0.0% / 0.0% | 0.0% |
