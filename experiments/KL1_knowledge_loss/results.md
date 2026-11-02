# KL1 — Does know-how outlive its holders? Results

Frozen as `KL1-frozen`. run_kl1.py, analyse_kl1.py (written before data).

## Validity

- Zero checks (All: PASS, same `code_v11` fingerprint): **yes**
- All worlds present (32 of 32): **yes**
- One fingerprint, `code_v11`'s: **yes**
- The observer's record of who knows what, and of losses and revivals, matches the world (mismatches 0): **yes**

**Valid.**

## Primary (frozen)

| quantity | value [95%] | count |
|---|---|---|
| **D**: share of world-level losses by death | **0.9025 [0.8911, 0.9129]** | 10,447 of 11,576 |
| **R_markable**: share of markable revivals through marks | **0.0202 [0.0000, 0.0517]** | 2 of 99 |

Readings: loss, death is the main road if D >= 0.5, otherwise forgetting is; marks revive lost know-how if R_markable >= 0.1, marks do not (yet) if below, too few to judge under 30 markable revivals.

**Reading (loss): death is the main road of loss.**

**Reading (marks): marks do not (yet).**

## Secondary (described, not decisive)

### World-level losses by cause

| kinds | death | forgetting | mixed |
|---|---|---|---|
| markable (strike) | 123 (0.992) | 1 (0.008) | 0 (0.000) |
| other | 10,324 (0.902) | 1,125 (0.098) | 3 (0.000) |

### Revivals by path (re-invention is not preservation)

| kinds | made | heated | read | taught with an error | copied with an error |
|---|---|---|---|---|---|
| markable (strike) | 2 | 0 | 2 | 95 | 0 |
| other | 3,490 | 37 | 0 | 483 | 0 |

### Gains of know-how by path (all kinds)

| path | gains | share |
|---|---|---|
| made | 71,505 | 0.672 |
| heated | 3,520 | 0.033 |
| taught | 14,376 | 0.135 |
| copied | 10 | 0.000 |
| read | 8,892 | 0.084 |
| taught_variant | 8,081 | 0.076 |
| copied_variant | 1 | 0.000 |

### Losses from minds by cause

| cause | losses | share |
|---|---|---|
| evicted | 22,139 | 0.179 |
| forgotten | 0 | 0.000 |
| death | 101,302 | 0.821 |

### At a knower's death; lifetimes; knowers

- A dead knower's kinds that survive in someone living: 0.897 (90,825 of 101,302).
- Weeks a kind stayed known before a counted loss: median 2795, mean 2803 (n 11,576).
- Yearly census: kinds alive per world-year 210.7; knowers per kind 6.19; share of kinds with a single knower 0.610.
- `read` events per world-year: 9.22.

