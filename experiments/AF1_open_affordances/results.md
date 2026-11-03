# AF1 — Open what made things can do: results

Frozen as `AF1-frozen`. run_af1.py, analyse_af1.py (written before data).

## Validity

- Zero checks (All: PASS, same `code_af1` fingerprint): **yes**
- All worlds present (160): **yes**
- One fingerprint, `code_af1`'s: **yes**

**Valid.**

## Primary (frozen): R = share of kinds invented in years 100-195 whose own recipe is made again by choice within 5 years (lineage)

| arm | R | kinds | remade |
|---|---|---|---|
| v11 | 0.0003 | 3,414 | 1 |
| S | 0.0006 | 3,437 | 2 |
| K | 0.0000 | 3,150 | 0 |
| S+K | 0.0000 | 3,194 | 0 |
| sham | 0.0000 | 3,346 | 0 |

| contrast | difference [95%] |
|---|---|
| S - v11 | +0.0003 [-0.0007, +0.0012] |
| K - v11 | -0.0003 [-0.0010, +0.0000] |
| S+K - v11 | -0.0003 [-0.0010, +0.0000] |
| S - sham | +0.0006 [+0.0000, +0.0014] |
| K - sham | +0.0000 [+0.0000, +0.0000] |
| S+K - sham | +0.0000 [+0.0000, +0.0000] |
| S+K - S | -0.0006 [-0.0014, +0.0000] |
| S+K - K | +0.0000 [+0.0000, +0.0000] |
| sham - v11 | -0.0003 [-0.0010, +0.0000] |

Rule: inconclusive (sham) if the sham - v11 interval lies wholly outside +-0.01; otherwise an arm is "positive" only if arm - v11 and arm - sham both have intervals above 0 and both points are at least 0.01; otherwise "inconclusive".

**S: inconclusive.** No guard raised.
**K: inconclusive.** No guard raised.
**S+K: inconclusive.** No guard raised.

## Guards (each arm against v11)

- S: population 0.981 [0.868, 1.102]; extinctions beyond v11's -1
- K: population 0.966 [0.847, 1.093]; extinctions beyond v11's +0
- S+K: population 0.974 [0.858, 1.094]; extinctions beyond v11's -1

## Secondary (described, not decisive)

| arm | functional D=5 | D=10 | D=20 | known at 1 yr | 2 yr | 5 yr | stand-in makes per adult-year | made things per adult | materials per adult | makes per adult-year | kinds per 100 adult-years |
|---|---|---|---|---|---|---|---|---|---|---|---|
| v11 | 0.0009 | 0.0103 | 0.0483 | 0.824 | 0.819 | 0.806 | 0.00000 | 0.93 | 11.77 | 0.0715 | 1.117 |
| S | 0.0006 | 0.0102 | 0.0506 | 0.807 | 0.803 | 0.793 | 0.00125 | 0.92 | 11.88 | 0.0752 | 1.144 |
| K | 0.0000 | 0.0076 | 0.0451 | 0.848 | 0.843 | 0.834 | 0.00000 | 0.90 | 12.69 | 0.0681 | 1.071 |
| S+K | 0.0009 | 0.0066 | 0.0476 | 0.845 | 0.840 | 0.829 | 0.00115 | 0.95 | 12.72 | 0.0672 | 1.077 |
| sham | 0.0012 | 0.0105 | 0.0511 | 0.807 | 0.803 | 0.789 | 0.00000 | 0.84 | 11.99 | 0.0705 | 1.136 |

