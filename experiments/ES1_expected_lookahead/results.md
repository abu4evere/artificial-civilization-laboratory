# ES1 — Do minds learn more accurately with an expected look-ahead? Results

Frozen as `ES1-frozen` (operational note 1). run_es1.py, analyse_es1.py (written before data).

## Validity

- Zero checks: **yes**
- All worlds present (96 of 96): **yes**
- One fingerprint (`code_es1`): **yes**
- Every habit update replays under its arm's rule (mismatches 0): **yes**

**Valid.**

Paired seeds: 32. Extinct: v11 2, e 2, sham 2.

## Primary — calibration error across all actions: mean |q - G| (habit updates started in years 100-200)

| arm | mean abs(q - G) | updates closed | censored at death |
|---|---|---|---|
| v11 | 0.3919 | 21,196,861 | 254,829 |
| e (expected look-ahead) | 0.4230 | 25,387,627 | 307,289 |
| sham | 0.3859 | 20,275,937 | 242,533 |

**e - v11: +0.0311 [+0.0218, +0.0398]**; sham - v11: -0.0060 [-0.0149, +0.0032].

## Secondary — signed bias q - G by action (years 100-200)

| action | v11 | e | sham |
|---|---|---|---|
| forage | +0.408 | -0.408 | +0.397 |
| gather | +0.373 | -0.356 | +0.365 |
| talk | +0.134 | -0.507 | +0.127 |
| give | +0.409 | -0.397 | +0.403 |
| rest | -0.158 | -0.483 | -0.159 |
| explore | -0.461 | -0.485 | -0.456 |
| play | -0.437 | -0.496 | -0.436 |
| make | -0.512 | -0.520 | -0.494 |
| hunt | -0.464 | -0.473 | -0.459 |
| care | -0.479 | -0.667 | -0.486 |
| put | +0.302 | -0.378 | +0.287 |
| take | -0.698 | -0.668 | -0.687 |

| secondary (years 100-200) | v11 | e | sham | e ÷ v11 [95%] |
|---|---|---|---|---|
| makes per adult-year | 0.070 | 0.362 | 0.074 | 5.155 [4.744, 5.535] |
| foraged food per adult-year | 405.0 | 414.9 | 404.5 | 1.024 [1.018, 1.031] |
| tools' share of foraged food | 0.0140 | 0.0558 | 0.0143 | 3.986 [3.669, 4.295] |

## Guards

| guard | e against v11 [95%] | sham against v11 | raised |
|---|---|---|---|
| population (e ÷ v11 < 0.90, upper < 1) | 1.205 [1.034, 1.392] | 0.956 | no |
| adult deaths per 1,000 adult-years (e − v11 > 0, lower > 0, > 10% of v11's 26.7) | +0.96 [-0.05, +1.89] | -0.13 | no |
| extinctions (e − v11 ≥ 3) | +0 | +0 | no |

## The frozen decision

- e - v11 +0.0311 [+0.0218, +0.0398] (< 0 with upper < 0); sham - v11 -0.0060 (e must be below it); guard flags: none.

**NOT SUPPORTED.** (A test in a copy; making is reported, not decisive; adoption only by the safe path in CLAUDE.md, with a confirmatory run.)

