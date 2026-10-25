# TW1 — Twins and the sex ratio at birth: findings

Frozen as `TW1-frozen`; run on GitHub Actions (run 40210448166), 512 worlds (arms C and T, 256 seeds each, 16101–16356,
120 years). Every number below comes from `analyse_tw1.py` (written before data); the full tables are in `results.md`.

## Verdict under the frozen rule

**Valid, and the manipulation checks pass.** Zero checks passed (settings off = code_v6 exactly, nursing fix
included; observers read-only; reload exact; unit tests). All 512 worlds are present under one fingerprint.

- Twin deliveries: 337 of 23,652 (14.2 per 1,000; target 14; exact p = 0.74).
- Identical-twin deliveries: 89 of 23,652 (3.8 per 1,000; target 4; p = 0.61).
- Boys among independent sex draws: 12,346 of 23,900 (106.9 boys per 100 girls; target 105; p = 0.18).
- Arm C: no twins.

**So by the frozen adoption rule, both settings are proposed for nature v7. The creator decides.** Nothing below was
used to accept or refuse.

## Described only (no test was frozen for these)

- **Independence.** The twin rate is flat across the mother's age (13.5–15.1 per 1,000), previous births (14.1–14.4) and
  population (13.1–15.0), as the code says it must be.
- **Twins die more, with no extra rule.** Survival to age 5: singletons 0.836 (of 22,496), fraternal twins 0.663 (of
  472), identical twins 0.557 (of 176). Nothing was added for twins. The higher deaths come only from two infants
  sharing one carer's food. The direction matches the human evidence (twins under five die about three times as often
  without modern medicine; Monden & Smits 2017). The size is not calibrated and should not be read as realistic.
  Mothers of twins who died within a year of the delivery: 31 of 329. Identical pairs in which both reached 16: 28.
- **Population and survival (population first).**

  | arm | time-avg pop. | median pop. year 60 / 120 | died out (of 256) |
  |---|---|---|---|
  | C | 24.52 | 24 / 25 | 83 |
  | T | 24.53 | 22 / 18 | 97 |

  The time-averaged population is the same. Arm T has more extinctions and a lower median at year 120. **This is
  described, not tested:** no comparison was frozen, and it is not evidence that the settings harm or help.
- **Adult sex ratio.** Men outlive women in both arms. Boys per 100 girls reaching 16 / 30 / 50: C 98 / 110 / 141;
  T 109 / 126 / 166. At birth arm T starts 105:100, so it has fewer adult women. The book should know this: in ACL
  women already die younger than men (why was not analysed here), and a human birth ratio makes women scarcer still. A real
  forager check of adult sex ratios would be the evidence to look at before reading anything into it.

## Limits

- The body has no prematurity or birth weight, so the extra risk twins face at birth is missing. This is reported, not
  patched.
- 120 years only; the long-run effect of fewer adult women is unknown (M1 runs on v6 without these settings).

## What happens next

The creator decides whether v7 = v6 + `twins` + `sex_ratio_birth` (+ the nursing fix). If yes, v7 is cut as
`code_v7` with these settings on, tests are updated, and later studies run on v7. M1 and RH1 stay on v6 as frozen.
