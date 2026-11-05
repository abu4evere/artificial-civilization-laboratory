# PB1: A shadow brain — can a small predictor learn what ACL's actions do? (results)

Frozen as `PB1-frozen` (with amendment 1). run_pb1.py, analyse_pb1.py (written before data).

## Validity

- Zero checks (All: PASS, same `code_v13` fingerprint): **yes**
- All worlds present (32): **yes**
- One fingerprint, `code_v13`'s: **yes**

**Valid.**

## Primary (frozen): L-own against B on compositionally unfamiliar weeks

| cases | skill of L-own [95%] | reading |
|---|---|---|
| 226,685 unfamiliar (situation, action) weeks of common actions | -0.2017 [-0.2119, -0.1919] | **it does not** |

Skill = 1 − (squared standardised error of the variant ÷ that of B). Rule: the predictor learns and generalises if the 95% interval lies wholly above 0.

## Mandatory secondary: unfamiliar property combinations

L-own against B on 81,801 weeks: **-0.0676 [-0.0788, -0.0560]**.

## Every variant against B (described; no multiplicity claim)

| cases | weeks | L-own | N-own | L-obs | L-obs-0.5 | N-obs |
|---|---|---|---|---|---|---|
| unfamiliar pairs (primary) | 226,685 | -0.202 [-0.212, -0.192] | -0.241 [-0.253, -0.231] | -0.885 [-1.519, -0.400] | -0.103 [-0.114, -0.094] | +nan [+nan, +nan] |
| unfamiliar property combinations | 81,801 | -0.068 [-0.079, -0.056] | -0.078 [-0.090, -0.066] | -0.612 [-1.135, -0.215] | +0.013 [+0.004, +0.024] | +nan [+nan, +nan] |
| all own weeks | 3,741,424 | -0.138 [-0.149, -0.128] | -0.190 [-0.202, -0.178] | -5.059 [-9.043, -2.027] | -0.028 [-0.036, -0.020] | +nan [+nan, +nan] |
| rare actions | 20,982 | +0.016 [-0.008, +0.040] | +0.005 [-0.019, +0.030] | -0.934 [-1.702, -0.350] | +0.052 [+0.030, +0.075] | +nan [+nan, +nan] |
| unfamiliar destination | 155,997 | -0.055 [-0.062, -0.049] | -0.103 [-0.112, -0.096] | -3.261 [-6.233, -1.181] | +0.025 [+0.019, +0.029] | +nan [+nan, +nan] |
| first 100 weeks lived | 347,257 | -0.147 [-0.159, -0.136] | -0.220 [-0.235, -0.207] | -0.656 [-1.160, -0.259] | +0.005 [-0.005, +0.014] | -0.248 [-0.489, -0.071] |
| 100-500 weeks | 1,285,336 | -0.192 [-0.205, -0.181] | -0.288 [-0.303, -0.274] | -3.372 [-6.119, -1.335] | -0.036 [-0.045, -0.027] | +nan [+nan, +nan] |
| 500-1,000 weeks | 1,135,117 | -0.121 [-0.133, -0.110] | -0.147 [-0.161, -0.134] | -5.971 [-10.755, -2.385] | -0.037 [-0.046, -0.027] | +nan [+nan, +nan] |
| over 1,000 weeks | 973,714 | -0.076 [-0.088, -0.066] | -0.084 [-0.095, -0.073] | -8.687 [-15.466, -3.490] | -0.023 [-0.033, -0.014] | +nan [+nan, +nan] |

## For PB2 (frozen preference rules, on the primary cases)

- N-own over L-own (skill difference): -0.0397 [-0.0411, -0.0382] → **linear is kept**.
- L-obs over L-own: -0.6837 [-1.3191, -0.1952] → **own experience only**.

## By output: L-own and L-obs against B, all own weeks (described)

| output | L-own | L-obs | B's mean squared standardised error (headroom) |
|---|---|---|---|
| food gained | -0.818 | -40.276 | 0.108 |
| net food | -0.667 | -0.667 | 0.141 |
| health | -0.024 | -0.024 | 0.850 |
| energy | -0.479 | -0.479 | 0.445 |
| materials | -1.554 | -25.592 | 0.169 |
| things held | +0.007 | -5.563 | 0.901 |
| distance | -0.056 | -7.093 | 0.732 |
| new kind | +0.292 | -33.167 | 0.103 |
| affection | +0.068 | +0.068 | 1.008 |

## Population and sample (beside every measure)

Followed adults 3,502; their own prequential weeks 3,742,401; observed examples 53,354,521; living-weeks 10,233,808; extinct worlds 0.

