# LX1 — does parts-first teaching cost survival? Findings

Frozen as `LX1-frozen` before any code or data. A Law 126 check. Tables: `results.md`, from `analyse_lx1.py`
(written and committed before data; tested on LM1's worlds, where it reproduced LM1). The code is `code_lm1`
unchanged, in two arms: C (`parts_first` 0) and L (`parts_first` 1). 1,024 worlds: 512 new seeds 7601–8112 × C and L,
20 founders, 40 × 40, 120 years. **Run on GitHub's machines** (`cloud-run`, run 39657479991). Zero checks passed there
and on this PC.

## Validity

- Zero checks passed.
- All 1,024 worlds are present.
- There is one fingerprint (`code_lm1`).
- Part lessons happened in every L world that lived 10 years; 25,883 of 267,145 were taken.

**Valid.**

## The frozen reading

**Primary, survival:** C died out in **181 of 512**, L in **177 of 512**.

| L saved / lost | sign-test p | effect (C − L) | 95% interval | reading |
|---|---|---|---|---|
| 72 / 68 | 0.80 | +0.008 | [−0.037, +0.053] | **no meaningful effect** |

**Secondary, replication of LM1:** the share of useful inventions passed on, L − C = **+0.0201** [+0.0171, +0.0232],
p = 2.7e-30 (C's median 0.091). **It holds.**

**The adoption rule, fixed before data:** survival reads "no meaningful effect" and the replication holds, so **adopt
L1 (`parts_first`) into nature (v3).**

**The prior was right:** no meaningful effect on survival, the replication holds, and L1 would be adopted.

## Beside it (described; population first)

| arm | median population, year 60 / 119 | died out | deaths | illness | starvation | old age | thirst | other |
|---|---|---|---|---|---|---|---|---|
| C | 24 / 22 | 181 | 45,286 | 16,222 | 14,735 | 8,175 | 4,465 | 1,689 |
| L | 26 / 25 | 177 | 46,961 | 16,434 | 15,661 | 8,401 | 4,728 | 1,737 |

LM1's 93 against 79 was chance: on twice as many new seeds, L died out slightly less often (177 against 181). Births
and partner blocking are not recorded by `code_lm1`, and no new code was allowed.

## What it means for ACL

Parts-first teaching is the first change that has been shown to move CA1's bottleneck (passing on), twice, on 768
seeds in all. It has now been checked not to cost survival. By the rule fixed before data, it enters nature as
**v3 = v2 + `parts_first`**. Before any study runs on v3:

1. A frozen plan for the switch.
2. Zero checks showing v3 equals v2 with the setting off and acts with it on.
3. A new control baseline, because every earlier study's C is v2.

Earlier v2 results stay as they are. The effect is small: about 2 points on a 9% share. Most useful inventions still
die with their makers.
