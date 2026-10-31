# HD1 — Can a person hand a made thing to another? Results

Frozen as `HD1-frozen` (operational note 1). run_hd1.py, analyse_hd1.py (written before data).

## Validity

- Zero checks: **yes**
- All worlds present (96 of 96): **yes**
- One fingerprint (`code_hd1`): **yes**
- Forage replay and conservation (mismatches 0): **yes**

**Valid.**

Paired seeds: 32. Extinct: v10 0, h 0, sham 0.

## Primary — food added by tools (share of adults' foraged food, years 100-200)

| arm | R |
|---|---|
| v10 | 0.0103 |
| h (handing) | 0.0128 |
| sham | 0.0105 |

**h - v10: +0.0025 [+0.0018, +0.0034]**; sham - v10: +0.0002 [-0.0006, +0.0009].

## Mechanism (years 100-200)

| measure | v10 | h | sham |
|---|---|---|---|
| handings per adult-year | 0.000 | 0.183 | 0.000 |
| share of adult forage weeks with a tool in hand | 0.104 | 0.137 | 0.105 |
| food gifts per adult-year | 5.56 | 5.41 | 5.30 |
| recipients' forage weeks with a tool (within a year of receiving) | nan | 0.499 | nan |

Reversals in h (handed back to the giver within 4 weeks): 0.0001 of 57,172 handings.

## No-harm flags (h against v10; sham against v10 beside it)

| flag | h ÷ v10 (or −) [95%] | sham ÷ v10 (or −) | raised |
|---|---|---|---|
| population (mean living) (< 0.9 with upper < 1) | 0.965 [0.860, 1.085] | 0.948 | no |
| food per adult (< 0.9 with upper < 1) | 1.000 [0.994, 1.006] | 1.000 | no |
| recipes held per adult (< 0.9 with upper < 1) | 0.995 [0.979, 1.013] | 1.005 | no |
| food gifts per adult-year (< 0.95 with upper < 1) | 0.973 [0.913, 1.034] | 0.953 | no |
| child deaths per 1,000 child-years (h − v10 > 0, lower > 0) | -0.00 [-1.31, +1.32] | +0.59 | no |
| extinctions (h − v10 ≥ 3) | +0 | +0 | no |
| ping-pong (reversals > 10% of handings) | 0.0001 | | no |

## The frozen decision

- h - v10 +0.0025 [+0.0018, +0.0034] (> 0 with lower > 0); sham - v10 +0.0002 (h must exceed it); flags raised: none.
- Handings per adult-year in h: 0.18.

**SUPPORTED.** (A test in a copy; adoption only by the safe path in CLAUDE.md, with a confirmatory run.)

