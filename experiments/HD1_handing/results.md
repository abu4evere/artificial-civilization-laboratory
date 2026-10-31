# HD1 — Can a person hand a made thing to another? Results

Frozen as `HD1-frozen` (operational note 1). run_hd1.py, analyse_hd1.py (written before data).

## Validity

- Zero checks: **yes**
- All worlds present (96 of 96): **yes**
- One fingerprint (`code_hd1`): **yes**
- Forage replay and conservation (mismatches 0): **yes**

**Valid.**

Paired seeds: 32. Extinct: v10 0, h 0, sham 1.

## Primary — food added by tools (share of adults' foraged food, years 100-200)

| arm | R |
|---|---|
| v10 | 0.0107 |
| h (handing) | 0.0143 |
| sham | 0.0114 |

**h - v10: +0.0036 [+0.0028, +0.0045]**; sham - v10: +0.0007 [-0.0000, +0.0014].

## Mechanism (years 100-200)

| measure | v10 | h | sham |
|---|---|---|---|
| handings per adult-year | 0.000 | 0.199 | 0.000 |
| share of adult forage weeks with a tool in hand | 0.110 | 0.156 | 0.115 |
| food gifts per adult-year | 5.98 | 5.79 | 5.76 |
| recipients' forage weeks with a tool (within a year of receiving) | nan | 0.515 | nan |

Reversals in h (handed back to the giver within 4 weeks): 0.0003 of 64,384 handings.

## No-harm flags (h against v10; sham against v10 beside it)

| flag | h ÷ v10 (or −) [95%] | sham ÷ v10 (or −) | raised |
|---|---|---|---|
| population (mean living) (< 0.9 with upper < 1) | 0.980 [0.871, 1.089] | 0.955 | no |
| food per adult (< 0.9 with upper < 1) | 1.002 [0.994, 1.008] | 0.999 | no |
| recipes held per adult (< 0.9 with upper < 1) | 0.996 [0.977, 1.015] | 0.989 | no |
| food gifts per adult-year (< 0.95 with upper < 1) | 0.967 [0.900, 1.030] | 0.962 | no |
| child deaths per 1,000 child-years (h − v10 > 0, lower > 0) | +0.71 [-1.39, +2.91] | -0.84 | no |
| extinctions (h − v10 ≥ 3) | +0 | +1 | no |
| ping-pong (reversals > 10% of handings) | 0.0003 | | no |

## The frozen decision

- h - v10 +0.0036 [+0.0028, +0.0045] (> 0 with lower > 0); sham - v10 +0.0007 (h must exceed it); flags raised: none.
- Handings per adult-year in h: 0.20.

**SUPPORTED.** (A test in a copy; adoption only by the safe path in CLAUDE.md, with a confirmatory run.)

