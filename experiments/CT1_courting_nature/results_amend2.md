# CT1 — courting as nature: results — Amendment 2 SENSITIVITY ANALYSIS (post-data, exploratory)

Frozen as `CT1-frozen`. run_ct1.py, analyse_ct1.py. Nature v3.

**Exploratory.** The primary record is `results.md`: NOT VALID under the committed analysis. This file follows Amendment 2 (decided after the manipulation checks were seen, before any outcome): hard-stop checks for K1 and K2 only, as the signed plan text says; K12's checks are described. Nothing here is confirmatory; the assistant recommends no adoption into nature on this run alone.

## Validity

- Zero checks: **yes**
- All worlds present: **yes**
- One fingerprint (`code_ct1`): **yes**
- Manipulation check (Amendment 1), K1: K1 acts, acceptances v3 would have refused: 513 (2.99 per 100 attempts; in 171 of 256 worlds): **yes**
- Manipulation check (Amendment 1), K12: K1 acts, acceptances v3 would have refused: 534 (3.04 per 100 attempts; in 176 of 256 worlds): **yes** (described under Amendment 2)
- Manipulation check, K2: courting attempts per single adult-year rise against C: mean difference +0.003 [-0.001, +0.008], p = 0.0415: **yes**
- Manipulation check, K12: courting attempts per single adult-year rise against C: mean difference +0.000 [-0.004, +0.005], p = 0.47: **NO** (described under Amendment 2; K12 did not show the intended added effect of K2 on courting)

**Valid.**

## Primary: survival (each arm against C, paired by seed)

C died out in **83 of 256**.

| arm | died out | saved / lost | p | Holm p | effect (C − arm) | 95% interval | reading |
|---|---|---|---|---|---|---|---|
| K1 | 81 | 12 / 10 | 0.832 | 0.832 | +0.008 | [-0.027, +0.043] | **no meaningful effect** |
| K2 | 70 | 44 / 31 | 0.165 | 0.496 | +0.051 | [-0.016, +0.117] | **unresolved** |
| K12 | 72 | 45 / 34 | 0.26 | 0.521 | +0.043 | [-0.023, +0.109] | **no meaningful effect** |

## Mechanism outcomes (paired differences against C; mean [95% interval])

| arm | births per woman-year | share of fertile woman-weeks single | couples formed |
|---|---|---|---|
| K1 | +0.0001 [-0.0029, +0.0031] | -0.0046 [-0.0153, +0.0059] | +2.0078 [+0.5352, +3.4883] |
| K2 | +0.0002 [-0.0046, +0.0050] | -0.0076 [-0.0252, +0.0104] | +1.9453 [-0.5508, +4.4453] |
| K12 | +0.0013 [-0.0039, +0.0063] | -0.0117 [-0.0301, +0.0073] | +1.8867 [-0.8008, +4.6250] |
| C (mean level) | 0.1251 | 0.5733 | 31.5 |

## Harm outcomes (C's level; each arm's absolute and relative change, paired 95% interval, Wilcoxon p)

**infant deaths per birth** (C: 0.0732) — serious harm measure

| arm | change | relative | 95% interval | p |
|---|---|---|---|---|
| K1 | -0.0004 | -0.5% | [-0.0042, +0.0035] | 0.967 |
| K2 | +0.0036 | +4.9% | [-0.0036, +0.0106] | 0.543 |
| K12 | +0.0049 | +6.8% | [-0.0021, +0.0120] | 0.281 |

**adult deaths by starvation (per world)** (C: 16.1523) — serious harm measure

| arm | change | relative | 95% interval | p |
|---|---|---|---|---|
| K1 | +1.1602 | +7.2% | [+0.3281, +2.0156] | 0.0316 |
| K2 | +0.3320 | +2.1% | [-1.0000, +1.6914] | 0.615 |
| K12 | +0.7773 | +4.8% | [-0.6562, +2.2305] | 0.386 |

**births to a mother under 18 or a father 15+ years older** (C: 0.0231)

| arm | change | relative | 95% interval | p |
|---|---|---|---|---|
| K1 | +0.0007 | +3.1% | [-0.0013, +0.0026] | 0.361 |
| K2 | +0.0011 | +4.7% | [-0.0020, +0.0042] | 0.346 |
| K12 | +0.0009 | +4.0% | [-0.0020, +0.0040] | 0.323 |

**Couples that split:** 0 in every arm by construction (couples part only at death; operational note).

## Mechanism, described (pooled over worlds)

Acceptance share of courting attempts on someone not yet a partner, by the courted one's familiarity with the suitor:

| arm | fam < 0.05 | fam < 0.15 | fam < 0.35 | fam < 0.6 | fam < 1.01 |
|---|---|---|---|---|---|
| C | 99/1768 | 947/2928 | 2240/4247 | 2969/5141 | 1816/3095 |
| K1 | 144/1859 | 1271/3083 | 2352/4125 | 3103/5199 | 1715/2906 |
| K2 | 115/2217 | 1058/3371 | 2302/4448 | 3198/5426 | 1896/3235 |
| K12 | 118/2134 | 1256/3189 | 2292/4022 | 3055/5129 | 1833/3093 |

Courting attempts per single adult-year, by the suitor's loneliness:

| arm | lonely < 0.25 | lonely < 0.5 | lonely < 0.75 | lonely < 1.01 | suitor knows them well (fam ≥ 0.35) |
|---|---|---|---|---|---|
| C | 0.06 | 0.09 | 0.02 | 0.01 | 47.9% |
| K1 | 0.06 | 0.09 | 0.02 | 0.01 | 47.1% |
| K2 | 0.06 | 0.12 | 0.05 | 0.02 | 46.3% |
| K12 | 0.06 | 0.11 | 0.05 | 0.02 | 46.8% |

Whether the change acts mostly on people who would otherwise rarely pair is not measurable from this log (it records attempts, not who would have paired without the change); not described.

**Interaction on dying out (K12 − K2) − (K1 − C):** +0.016 [-0.039, +0.070] (described).

## The adoption rule (frozen)

- **K1: not adopted (a serious harm rose)**.
- **K2: not adopted (survival: unresolved)**.
- **K12: not proposed** (K1 and K2 do not both qualify alone).
- Births and couples are the mechanism's evidence, shown above; no p-value on them is a condition.
