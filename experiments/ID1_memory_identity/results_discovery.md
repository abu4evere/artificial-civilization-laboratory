# ID1 — what makes an ACL person who they are? Results (discovery)

Frozen as `ID1-frozen` (correction of 12 October appended). run_id1.py, analyse_id1.py.

## Validity

- One code fingerprint (`code_e13r`): **yes**
- The original copy reproduces the uncopied world in every world: **yes**
- The sham differs from the original, and every swap was applied and restored (Amendment 2): **yes**
- Swaps that left the final world unchanged (an outcome, not a stop): 2 [(511, 'p00005:beliefs'), (511, 'p00005:places')]
- Worlds: 32; skipped: 1 (seed 513: no eligible focal person)
- Focal people: 57; dropped (alive fewer than 13 weeks, or 2 in the smoke test): weeks 1–26 1, weeks 27–52 2

**Valid.**

## Who (population beside every measure, rule 18)

Median population at the snapshot 27; focal people's median age 40.3; partnered 24 of 57; alive at the end of the 52 weeks (original copy) 55 of 57.

## Q1 — which parts move a person? (weeks 1–26; drift vs sham drift)

| arm | people | median (arm − sham) drift | p | Holm p | moves the person |
|---|---|---|---|---|---|
| temperament | 55 | 0.00337 | 0.348 | 1 | no |
| habits | 56 | -0.0141 | 0.0512 | 0.205 | no |
| memories | 56 | -0.018 | 0.00569 | 0.0341 | no |
| relationships | 56 | 0.00654 | 0.357 | 1 | no |
| knowhow | 56 | -0.0336 | 0.00183 | 0.0128 | no |
| beliefs | 56 | 0.0228 | 0.039 | 0.195 | no |
| places | 56 | -0.00276 | 0.826 | 1 | no |
| all_but_temperament | 55 | 0.085 | 1.89e-08 | 1.51e-07 | **yes** |

## Q2 — pulled toward the donor? (weeks 1–26)

| arm | people | pulled (arm) | pulled (sham) | arm only / sham only | p | Holm p | pulled |
|---|---|---|---|---|---|---|---|
| temperament | 54 | 7 | 4 | 5 / 2 | 0.453 | 1 | no |
| habits | 55 | 6 | 4 | 3 / 1 | 0.625 | 1 | no |
| memories | 55 | 6 | 4 | 4 / 2 | 0.688 | 1 | no |
| relationships | 55 | 8 | 4 | 6 / 2 | 0.289 | 1 | no |
| knowhow | 55 | 5 | 4 | 4 / 3 | 1 | 1 | no |
| beliefs | 55 | 17 | 4 | 14 / 1 | 0.000977 | 0.00684 | **yes** |
| places | 55 | 9 | 4 | 7 / 2 | 0.18 | 1 | no |
| all_but_temperament | 54 | 29 | 4 | 25 / 0 | 5.96e-08 | 4.77e-07 | **yes** |

## Q3 — is temperament enough?

**the person follows their parts, not their temperament**

## Q4 — does restoring bring them back? (weeks 27–52; only arms that moved the person)

| arm | people | median (arm − sham) drift | p | Holm p | reading |
|---|---|---|---|---|---|
| all_but_temperament | 52 | -0.00221 | 0.229 | 0.229 | **no detectable lasting change** |
