# ID1 — what makes an ACL person who they are? Results (holdout)

Frozen as `ID1-frozen` (correction of 12 October appended). run_id1.py, analyse_id1.py.

## Validity

- One code fingerprint (`code_e13r`): **yes**
- The original copy reproduces the uncopied world in every world: **yes**
- The sham and every swap differ from the original: **NO**
- Worlds: 32; skipped: 1 (seed 1101: no eligible focal person)
- Focal people: 52; dropped (alive fewer than 13 weeks, or 2 in the smoke test): weeks 1–26 0, weeks 27–52 2

**NOT VALID: no outcome below may be read.**

## Who (population beside every measure, rule 18)

Median population at the snapshot 27; focal people's median age 39.8; partnered 33 of 52; alive at the end of the 52 weeks (original copy) 47 of 52.

## Q1 — which parts move a person? (weeks 1–26; drift vs sham drift)

| arm | people | median (arm − sham) drift | p | Holm p | moves the person |
|---|---|---|---|---|---|
| temperament | 50 | -0.0116 | 0.605 | 0.624 | no |
| habits | 52 | -0.0333 | 0.00265 | 0.0133 | no |
| memories | 52 | -0.0342 | 5.92e-05 | 0.000414 | no |
| relationships | 52 | 0.0197 | 0.0405 | 0.121 | no |
| knowhow | 52 | -0.0342 | 0.000753 | 0.00452 | no |
| beliefs | 52 | 0.00344 | 0.312 | 0.624 | no |
| places | 50 | -0.0224 | 0.0186 | 0.0742 | no |
| all_but_temperament | 51 | 0.0546 | 5.46e-06 | 4.37e-05 | **yes** |

## Q2 — pulled toward the donor? (weeks 1–26)

| arm | people | pulled (arm) | pulled (sham) | arm only / sham only | p | Holm p | pulled |
|---|---|---|---|---|---|---|---|
| temperament | 49 | 8 | 9 | 6 / 7 | 1 | 1 | no |
| habits | 51 | 6 | 11 | 3 / 8 | 0.227 | 0.906 | no |
| memories | 51 | 6 | 11 | 1 / 6 | 0.125 | 0.754 | no |
| relationships | 51 | 8 | 11 | 7 / 10 | 0.629 | 1 | no |
| knowhow | 51 | 5 | 11 | 3 / 9 | 0.146 | 0.754 | no |
| beliefs | 51 | 15 | 11 | 14 / 10 | 0.541 | 1 | no |
| places | 50 | 4 | 11 | 3 / 10 | 0.0923 | 0.738 | no |
| all_but_temperament | 51 | 20 | 11 | 17 / 8 | 0.108 | 0.754 | no |

## Q3 — is temperament enough?

**changed, but not into the donor**

## Q4 — does restoring bring them back? (weeks 27–52; only arms that moved the person)

| arm | people | median (arm − sham) drift | p | Holm p | reading |
|---|---|---|---|---|---|
| all_but_temperament | 48 | 0.0274 | 0.0247 | 0.0247 | **a lasting change** |

## Do discovery and holdout agree? (a reading stands only if they agree in direction and significance)

| question | discovery | holdout | stands |
|---|---|---|---|
| Q1 temperament moves | False | False | yes |
| Q1 habits moves | False | False | yes |
| Q1 memories moves | False | False | yes |
| Q1 relationships moves | False | False | yes |
| Q1 knowhow moves | False | False | yes |
| Q1 beliefs moves | False | False | yes |
| Q1 places moves | False | False | yes |
| Q1 all_but_temperament moves | True | True | yes |
| Q2 temperament pulled | False | False | yes |
| Q2 habits pulled | False | False | yes |
| Q2 memories pulled | False | False | yes |
| Q2 relationships pulled | False | False | yes |
| Q2 knowhow pulled | False | False | yes |
| Q2 beliefs pulled | True | False | no |
| Q2 places pulled | False | False | yes |
| Q2 all_but_temperament pulled | True | False | no |
| Q3 | the person follows their parts, not their temperament | changed, but not into the donor | no |
| Q4 all_but_temperament | no detectable lasting change | a lasting change | no |
