# HA1 — Why does handing stay rare? Results

Frozen as `HA1-frozen`. run_ha1.py, analyse_ha1.py (written before data).

## Validity

- Zero checks (All: PASS, same `code_v11` fingerprint): **yes**
- All worlds present (32 of 32): **yes**
- One fingerprint, `code_v11`'s: **yes**
- Every handing came from a decision seen with a handing option to that receiver (mismatches 0): **yes**

**Valid.**

## Primary (frozen)

Eligible decisions (a person holding a made thing, reaching the choice, years 100-200): 15,632,590.

| quantity | value [95%] |
|---|---|
| **E**: share with at least one handing option | **0.0709 [0.0667, 0.0747]** |
| **C**: mean softmax mass on handing, given an option | **0.0533 [0.0503, 0.0572]** |

Rule (hierarchical, on the pooled point estimates): opportunity-limited if E < 0.1; else choice-limited if C < 0.05; else neither.

**Reading: opportunity-limited.**

## Secondary (described, not decisive)

### The funnel (share of eligible decisions)

| stage | share |
|---|---|
| someone within reach with room | 0.9846 |
| someone with net > 0 | 0.0775 |
| a handing option | 0.0709 |
| expected handings (summed mass) | 59,143.9 |
| handings done | 59,178 |
| handings per adult-year | 0.190 |

### By the giver's age

| giver | decisions | E | C | top score minus best handing score |
|---|---|---|---|---|
| child | 2,804,559 | 0.0585 | 0.2150 | 0.575 |
| 12-15 | 958,358 | 0.0729 | 0.0262 | 1.206 |
| 16+ | 11,869,673 | 0.0737 | 0.0252 | 1.238 |

### By relation

| relation | share of handing options | share of handing mass | share of handings |
|---|---|---|---|
| kin | 0.234 | 0.516 | 0.517 |
| partner | 0.006 | 0.007 | 0.008 |
| other | 0.760 | 0.476 | 0.475 |

### Knowledge with the object: receivers who made the kind they received within 5 years

| receiver | handings counted | made it within 5 years |
|---|---|---|
| did not know the kind | 37,569 | 0.001 |
| already knew it | 19,686 | 0.051 |

### Who holds made things (yearly census, years 100-200)

| holder | share of made things held |
|---|---|
| child | 0.173 |
| 12-15 | 0.060 |
| 16-59 | 0.669 |
| 60+ | 0.097 |

