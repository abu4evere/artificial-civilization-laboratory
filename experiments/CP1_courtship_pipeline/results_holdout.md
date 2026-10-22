# CP1 Results — Holdout Set

**Sample:** 256 control worlds (80 extinct, 176 surviving to year 120). Worlds with < 100 fertile woman-weeks total are excluded from averages (extinct: 0, surviving: 0, all: 0).

---

## Pipeline gates: per-world mean share of fertile woman-weeks

Shares are **per-world means** (equal weight per world). G1+G2+G3 sum to the share of woman-weeks spent single (partnerless). G4 is partner-alive-but-apart. G5 is physiological blockers (starving + nursing). G6-eligible counts weeks where every gate is passed; G6-pregnant counts weeks already carrying.

| Gate | Name | Extinct | Surviving | Excess (ext − surv) |
|---|---|---:|---:|---:|
| G1 | Mate pool: no eligible man alive anywhere | 20.36% | 7.58% | +12.78 pp |
| G2 | Encounter: man alive but not within sight | 42.47% | 23.43% | +19.04 pp |
| G3 | Courtship + acceptance: man within sight, still single | 2.89% | 20.83% | -17.94 pp |
| G4 | Co-residence: partnered, apart from partner | 13.07% | 22.77% | -9.71 pp |
| G5 | Physiological blockers (starving + nursing) | 6.86% | 7.51% | -0.65 pp |
| G6-eligible | All gates passed, could conceive | 4.97% | 6.58% | -1.61 pp |
| G6-pregnant | Already pregnant | 8.38% | 10.40% | -2.02 pp |
| residual | r_partner_dead + r_low_health + r_partner_child (not stored) | 1.02% | 0.90% | +0.12 pp |

**Total share of woman-weeks spent single (partnerless):** extinct 65.7%, surviving 51.8%.
**Mean fertile woman-weeks per world (included):** extinct 13851, surviving 49504.

---

## Births per partnered fertile woman-year

- **Extinct:** mean 0.322, median 0.321
- **Surviving:** mean 0.285, median 0.284
- **Overall (per fertile woman-year, not just partnered):** extinct 0.109, surviving 0.137

---

## Frozen reading

Top excess gate in extinct: G2 (+19.0 pp). Confirmation against discovery done in findings.md.

Full ranking of (extinct − surviving) excesses among G1–G4:

- **G2:** +19.04 pp
- **G1:** +12.78 pp
- **G4:** -9.71 pp
- **G3:** -17.94 pp
