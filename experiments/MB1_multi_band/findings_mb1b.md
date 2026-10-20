# MB1b — same 80 people, divided differently: findings

Frozen as `MB1b-frozen` (Amendment 1 and its torus correction appended before any data; confirmed by the creator).
Tables: `results_mb1b.md`, from `analyse_mb1b.py`. 1,024 worlds (256 seeds × 4 arms), 40 × 40, 80 founders, 120 years,
nature v2. The run stopped once when the computer restarted (607 of 1,024 saved, files intact) and resumed; the first
log is kept as `run_mb1b_part1.log`.

## Validity

Zero checks PASS (setting 0 = `code_v2` at 20 and at 80 founders; b8 and b16 change the world; observers read-only).
All 1,024 worlds present; one code fingerprint; manipulation check PASS (every world founded with as many bands, of the
size, its arm says). **Valid.**

## The frozen reading (extinction, each arm against P4, paired by seed)

Baseline: **P4 (4 bands of 20) died out in 13 of 256 worlds (5.1%).**

| arm | died out (of 256) | saved / lost against P4 | Holm p | effect (P4 − arm) | 95% interval | reading |
|---|---|---|---|---|---|---|
| B8 (8 × 10) | 8 | 12 / 7 | 0.42 | +0.020 | [−0.016, +0.055] | **no meaningful effect** |
| B16 (16 × 5) | 7 | 11 / 5 | 0.42 | +0.023 | [−0.008, +0.055] | **no meaningful effect** |
| sham | 19 | 4 / 10 | 0.18 (unadjusted) | −0.023 | [−0.051, +0.004] | quiet, as it must be |

## Beside it (described; population first)

| arm | median population, year 60 / 119 | births per woman-year | decisions blocked for want of a partner | between-lineage meeting per adult pair-year | couples across lineages | lineages alive at the end (median) | most bands on one island (median) | smallest gap between band centres (median, tiles) |
|---|---|---|---|---|---|---|---|---|
| P4 | 50 / 50 | 0.146 | 0.455 | 0.076 | 6.4% | 2 | 1 | 10 |
| B8 | 59 / 56 | 0.146 | 0.461 | 0.210 | 29.4% | 3 | 2 | 6 |
| B16 | 59 / 60 | 0.143 | 0.466 | 0.290 | 54.0% | 4 | 4 | 3 |
| sham | 51 / 48 | 0.146 | 0.455 | 0.079 | 6.8% | 2 | 1 | 10 |

## What it shows

1. **With 80 founders, dividing them into more, smaller bands does not change survival.** Both readings are "no
   meaningful effect": the intervals sit well inside the yardstick (±0.117). The point estimates lean the other way
   from the prior (fewer worlds die out with smaller bands, 8 and 7 against 13), but not beyond chance.
2. **The test had little room.** Eighty founders on this land rarely die out at all (5%), so there was little extinction
   for band size to change. The study answers the question at 80 founders; it does not say what band size does in
   today's 20-founder worlds, where a third die out.
3. **Smaller bands mix far more.** Between-lineage meeting rises about fourfold (0.076 → 0.290) and the share of couples
   across lineages about eightfold (6% → 54%); more lineages are alive at the end (2 → 4) and populations end a little
   larger (50 → 60). As the plan warned, this cannot be separated from crowding: in B16 four bands share each island and
   band centres start 3 tiles apart instead of 10.
4. **More mixing did not unblock partners.** The share of decisions blocked for want of a partner stays at about 0.46
   in every arm, and births per woman-year do not move. Bands meeting and marrying across lines more often did not, by
   this measure, make partners easier to find.

## Against the prior (frozen; kept as written)

- "B16 dies out more than P4, B8 in between": **wrong** (no meaningful effect; if anything the other way).
- "Bands meet more in B8 and B16 than in P4": **right**, strongly.
- "If B16 dies out more despite meeting more, band size matters more than contact": does not apply.

## What it cannot show

Band size and crowding move together here (more bands means more bands per island), so the mixing rise is the two
together. Survival was near its floor at 80 founders, so a real effect of band size on survival in small worlds is not
ruled out. Band sizes are operational choices within the range of forager groups (Hamilton et al. 2007), not
measurements.
