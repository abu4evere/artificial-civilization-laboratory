# DG1 — digging: findings

Frozen as `DG1-frozen` before any data, after GPT's review, on the creator's instruction. Tables: `results.md`, from
`analyse_dg1.py` (written before data). Code: `code_dg1` = `code_v4` + `digging`, `pit_keep` (`v4_to_dg1.diff`).
1,536 worlds: 512 new seeds 13001–13512 × C (v4), D (food in a pit rots at half the rate), DW (three quarters),
20 founders, 120 years. **Run on GitHub's machines** (`cloud-run`, run 40028228227). Zero checks passed there and here.

## Validity

Zero checks passed; all worlds present; one fingerprint. **Manipulation check passes:** pits were dug in all 512 D
worlds. **Valid.**

## The frozen reading

| arm | died out (C 139 of 512) | survival | time-averaged population | reading |
|---|---|---|---|---|
| D | 149 | no meaningful effect (59 saved / 69 lost, p = 0.43) | +1.2% [−3.7%, +6.3%] | **safe** |
| DW | 157 | no meaningful effect (57 / 75, p = 0.14) | −0.6% [−5.5%, +4.6%] | inconclusive |

**The adoption rule:** D's survival and population are not worse, so digging **is proposed for nature (v5). The
creator decides.** The sensitivity arm DW does not pass the population margin by a hair, but D and DW behaved the same
(see below), so the difference between them is chance, not the rot setting.

**The prior was right:** pits are dug, out of curiosity; food is almost never put in one; no effect on survival.

## What people did (described)

- **Almost everyone dug once.** 51,889 digs by 50,734 people in D: nearly one dig per person, ever. A quarter of all
  digs came in the first decade; after that a steady trickle (about 3,500 a decade), as each new generation tried it.
- **Food went into a pit 204 times in 512 worlds** (1,329 food units, by 185 people): about once every two or three
  worlds, by chance, where someone happened to store food where a pit was.
- Pits standing at the end: 507 (107 knee-deep). Starvation deaths about the same in all arms.

## What it means

**A possibility is not a use.** Digging became something nearly every person tried once, and almost nobody found a
reason to do it again: a hole gives nothing by itself, and nobody connected "food keeps here" with the pit, because
food was stored in a pit too rarely for anyone to learn it. Real foragers who cached food in the ground did so for a
reason they already had (a surplus to keep, a place they would return to). In ACL, storage itself is still rare
(bottleneck B): digging cannot create a use for storing that does not yet exist.

Digging is harmless and true to nature, so it can enter nature as a possibility for later studies (storage pits,
burial with carrying, wells). That is the creator's decision.
