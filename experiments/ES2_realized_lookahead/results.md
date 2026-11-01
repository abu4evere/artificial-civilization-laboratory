# ES2 — Do minds learn more accurately when they look ahead by their real next choice? Results

Frozen as `ES2-frozen` (operational note 1). run_es2.py, analyse_es2.py (written before data).

## Validity

- Zero checks: **yes**
- All worlds present (96 of 96): **yes**
- One fingerprint (`code_es2`): **yes**
- Every habit update replays under its arm's rule (mismatches 0): **yes**

**Valid.**

Paired seeds: 32. Extinct: v11 0, r 0, sham 0.

## Primary — calibration error across all actions: mean |q - G| (habit updates started in years 100-200)

| arm | mean abs(q - G) | updates closed | censored at death |
|---|---|---|---|
| v11 | 0.3911 | 23,879,550 | 293,142 |
| r (realized look-ahead) | 0.2364 | 27,601,177 | 337,988 |
| sham | 0.3919 | 24,604,386 | 291,809 |

**r - v11: -0.1547 [-0.1614, -0.1480]**; sham - v11: +0.0008 [-0.0063, +0.0085].

## Frozen secondary — ranking accuracy (Spearman of mean q against mean G across actions, within a situation; averaged per world)

| arm | mean over worlds |
|---|---|
| v11 | 0.552 |
| r (realized look-ahead) | 0.497 |
| sham | 0.527 |

r - v11 (paired, worlds with both): -0.055 [-0.094, -0.017] over 32 worlds.

## Secondary — signed bias q - G by action (years 100-200)

| action | v11 | r | sham |
|---|---|---|---|
| forage | +0.410 | -0.173 | +0.407 |
| gather | +0.373 | -0.138 | +0.373 |
| talk | +0.125 | -0.322 | +0.130 |
| give | +0.408 | -0.076 | +0.413 |
| rest | -0.145 | -0.387 | -0.146 |
| explore | -0.463 | -0.475 | -0.462 |
| play | -0.436 | -0.461 | -0.437 |
| make | -0.510 | -0.510 | -0.515 |
| hunt | -0.472 | -0.477 | -0.468 |
| care | -0.471 | -0.572 | -0.489 |
| put | +0.295 | -0.135 | +0.296 |
| take | -0.695 | -0.697 | -0.703 |

| secondary (years 100-200) | v11 | r | sham | r ÷ v11 [95%] |
|---|---|---|---|---|
| makes per adult-year | 0.062 | 0.186 | 0.066 | 3.012 [2.722, 3.320] |
| foraged food per adult-year | 405.1 | 410.4 | 405.3 | 1.013 [1.009, 1.017] |
| tools' share of foraged food | 0.0122 | 0.0336 | 0.0129 | 2.756 [2.517, 2.989] |

Described (Gemini): instinct share of the options' score variance, Var(score - 0.6 q) / Var(score), on every 20th decision: v11 0.779; r (realized look-ahead) 0.959; sham 0.770.

## Guards

| guard | r against v11 [95%] | sham against v11 | raised |
|---|---|---|---|
| calibration by action (largest rise in mean abs(q - G), actions with >= 10,000 updates; > 0.10) | rest +0.155 | | **RAISED** |
| uncompleted (dropped) held updates (>= 1% of updates in any arm) | r 0.00000 | v11 0.00000 | no |
| population (r ÷ v11 < 0.90, upper < 1) | 1.160 [1.029, 1.289] | 1.031 | no |
| adult deaths per 1,000 adult-years (r − v11 > 0, lower > 0, > 10% of v11's 27.1) | +0.49 [-0.37, +1.32] | -0.72 | no |
| extinctions (r − v11 ≥ 3) | +0 | +0 | no |

## The frozen decision

- r - v11 -0.1547 [-0.1614, -0.1480] (< 0 with upper < 0); sham - v11 +0.0008 (r must be below it); guard flags: calibration by action.

**NOT SUPPORTED.** (A test in a copy; making and ranking are reported, not decisive; adoption only by the safe path in CLAUDE.md, with a confirmatory run.)

