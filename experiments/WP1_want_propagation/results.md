# WP1 — Want propagation: results

Frozen as `WP1-frozen`. run_wp1.py, analyse_wp1.py (written before data).

## Validity

- Zero checks (All: PASS, same `code_wp1` fingerprint): **yes**
- All worlds present (128): **yes**
- One fingerprint, `code_wp1`'s: **yes**

**Valid.**

## Primary (frozen): R = share of kinds invented in years 100-195 made again within 5 years

| arm | R | kinds | remade |
|---|---|---|---|
| v11 | 0.0000 | 3,575 | 0 |
| A1 | 0.0003 | 3,564 | 1 |
| A2 | 0.0000 | 3,760 | 0 |
| sham | 0.0003 | 3,621 | 1 |

| contrast | difference [95%] |
|---|---|
| A1 - v11 | +0.0003 [+0.0000, +0.0009] |
| A2 - v11 | +0.0000 [+0.0000, +0.0000] |
| A2 - A1 | -0.0003 [-0.0009, +0.0000] |
| sham - v11 | +0.0003 [+0.0000, +0.0009] |
| A1 - sham | +0.0000 [-0.0009, +0.0008] |
| A2 - sham | -0.0003 [-0.0009, +0.0000] |

Rule: inconclusive (sham) if the sham - v11 interval lies wholly outside +-0.01; otherwise an arm is "positive" only if arm - v11 and arm - sham both have intervals above 0 and both points are at least 0.01; otherwise "inconclusive".

**A1: inconclusive.** No guard raised.
**A2: inconclusive.** No guard raised.

A2 - A1: no added effect shown.

## Guards (each arm against v11)

- A1: population 1.068 [0.971, 1.184]; extinctions beyond v11's +0
- A2: population 1.120 [0.995, 1.261]; extinctions beyond v11's +0

## Secondary (described, not decisive)

| arm | gathers per adult-year | makes per adult-year | nested makes per adult-year | recipes per adult | remade by the inventor | by someone else | median weeks to the first remake | kinds per 100 adult-years |
|---|---|---|---|---|---|---|---|---|
| v11 | 12.783 | 0.0638 | 0.0026 | 10.13 | 0 | 0 | - | 1.115 |
| A1 | 11.914 | 0.0631 | 0.0025 | 10.22 | 1 | 0 | 64 | 1.053 |
| A2 | 12.405 | 0.0597 | 0.0028 | 9.87 | 0 | 0 | - | 1.056 |
| sham | 12.507 | 0.0675 | 0.0028 | 10.21 | 1 | 0 | 63 | 1.059 |

