# LX1 — does parts-first teaching cost survival? results

Frozen as `LX1-frozen`. run_lx1.py, analyse_lx1.py.

## Validity

- Zero checks: **yes**
- All worlds present: **yes**
- One fingerprint (`code_lm1`): **yes**
- Manipulation check, L: part lessons in every L world living 10 years: **yes**; some taken (25883 of 267145): **yes**

**Valid.**

## Primary: survival (L against C, paired by seed)

C died out in **181 of 512**; L in **177 of 512**.

| L saved / lost (discordant pairs) | sign-test p | effect (C − L) | 95% interval | reading |
|---|---|---|---|---|
| 72 / 68 | 0.8 | +0.008 | [-0.037, +0.053] | **no meaningful effect** |

## Secondary: replication of LM1 (share of useful inventions passed on, CA1's link 3)

Seeds with useful inventions in both arms: 512 of 512. C's median: 0.091.

| L − C, mean | 95% interval | Wilcoxon p | replication |
|---|---|---|---|
| +0.0201 | [+0.0171, +0.0232] | 2.74e-30 | **holds** |

## The adoption rule (frozen)

**Adopt L1 into nature (v3)**, by the frozen rule.

## Beside it (described; population first, rule 18)

| arm | median population, year 60 / 119 | died out | deaths | illness | starvation | old age | thirst | other causes |
|---|---|---|---|---|---|---|---|---|
| c | 24 / 22 | 181 | 45286 | 16222 | 14735 | 8175 | 4465 | 1689 |
| l | 26 / 25 | 177 | 46961 | 16434 | 15661 | 8401 | 4728 | 1737 |

Births and partner blocking are not recorded by `code_lm1` (no new code was allowed), so they are not described.
