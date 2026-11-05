# PB1b: A shadow brain with episodic memory (results)

Frozen as `PB1b-frozen`. run_pb1b.py, analyse_pb1b.py (written before data).

## Validity

- Zero checks (All: PASS, same `code_v13` fingerprint): **yes**
- All worlds present (32): **yes**
- One fingerprint, `code_v13`'s: **yes**

**Valid.**

## The gate (frozen): E-own against the table B

| part | cases | skill of E-own [95%] | holds |
|---|---|---|---|
| 1. unfamiliar (situation, action), common actions | 255,389 | +0.0092 [+0.0081, +0.0103] | yes (interval wholly above 0) |
| 2. familiar (lived before) | 3,826,129 | +0.0000 [+0.0000, +0.0000] | yes (lower end >= -0.02) |

**Reading: GO to PB2 with an episodic memory.**

## E-obs (described; preferred for PB2 if it passes the gate and beats E-own on unfamiliar cases)

- unfamiliar: +0.0839 [+0.0774, +0.0904]; familiar: +0.0319 [+0.0309, +0.0328]; passes the gate: **yes**

## Every variant against B (described; no multiplicity claim)

| cases | weeks | E-own | E-obs | E-obs-0.5 | L-obs-0.5 | E-own k=5 | E-own k=15 |
|---|---|---|---|---|---|---|---|
| unfamiliar pairs (gate part 1) | 255,389 | +0.009 [+0.008, +0.010] | +0.084 [+0.077, +0.090] | +0.099 [+0.092, +0.105] | -0.091 [-0.101, -0.081] | +0.002 [+0.001, +0.004] | +0.011 [+0.010, +0.011] |
| familiar (gate part 2) | 3,826,129 | +0.000 [+0.000, +0.000] | +0.032 [+0.031, +0.033] | +0.041 [+0.039, +0.042] | -0.018 [-0.026, -0.009] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| unfamiliar property combinations | 95,241 | +0.001 [+0.000, +0.001] | +0.252 [+0.240, +0.264] | +0.269 [+0.259, +0.280] | +0.017 [+0.008, +0.025] | -0.000 [-0.001, +0.000] | +0.001 [+0.001, +0.001] |
| all own weeks | 4,102,003 | +0.002 [+0.001, +0.002] | +0.043 [+0.041, +0.044] | +0.053 [+0.051, +0.055] | -0.029 [-0.035, -0.023] | +0.000 [+0.000, +0.001] | +0.002 [+0.002, +0.002] |
| rare actions | 23,977 | +0.000 [-0.001, +0.001] | +0.142 [+0.125, +0.159] | +0.190 [+0.172, +0.206] | +0.057 [+0.033, +0.078] | -0.000 [-0.001, +0.001] | +0.000 [-0.001, +0.001] |
| unfamiliar destination | 183,163 | +0.001 [+0.000, +0.002] | +0.029 [+0.027, +0.031] | +0.044 [+0.041, +0.047] | +0.018 [+0.012, +0.024] | -0.000 [-0.001, +0.001] | +0.001 [+0.001, +0.002] |
| first 100 weeks lived | 393,737 | +0.000 [-0.000, +0.001] | +0.091 [+0.086, +0.095] | +0.115 [+0.110, +0.120] | +0.007 [-0.001, +0.015] | -0.003 [-0.004, -0.003] | +0.001 [+0.001, +0.001] |
| 100-500 weeks | 1,439,796 | +0.001 [+0.001, +0.001] | +0.054 [+0.052, +0.056] | +0.065 [+0.062, +0.067] | -0.036 [-0.043, -0.030] | -0.000 [-0.001, +0.000] | +0.002 [+0.001, +0.002] |
| 500-1,000 weeks | 1,250,866 | +0.002 [+0.002, +0.002] | +0.026 [+0.025, +0.028] | +0.033 [+0.031, +0.035] | -0.037 [-0.046, -0.029] | +0.001 [+0.001, +0.002] | +0.002 [+0.002, +0.002] |
| over 1,000 weeks | 1,017,604 | +0.002 [+0.002, +0.003] | +0.019 [+0.017, +0.020] | +0.025 [+0.023, +0.027] | -0.026 [-0.034, -0.018] | +0.002 [+0.001, +0.002] | +0.002 [+0.002, +0.002] |

- E-obs over E-own on unfamiliar pairs (skill difference): +0.0747 [+0.0684, +0.0812] → **observation is preferred for PB2**.
- Nearest-memory distance on unfamiliar weeks (median of per-world medians): 0.479.

## By output: E-own and E-obs against B, all own weeks (described)

| output | E-own | E-obs | B's mean squared standardised error (headroom) |
|---|---|---|---|
| food gained | +0.000 | +0.112 | 0.111 |
| net food | +0.001 | -0.006 | 0.146 |
| health | +0.007 | -0.011 | 0.852 |
| energy | +0.006 | -0.003 | 0.443 |
| materials | -0.001 | +0.127 | 0.165 |
| things held | +0.000 | +0.110 | 0.943 |
| distance | +0.002 | +0.076 | 0.739 |
| new kind | +0.007 | +0.279 | 0.118 |
| affection | -0.003 | -0.020 | 1.025 |

## Population and sample (beside every measure)

Followed adults 3,976; their own prequential weeks 4,102,980; observed examples 58,831,608; living-weeks 11,658,859; extinct worlds 0.

