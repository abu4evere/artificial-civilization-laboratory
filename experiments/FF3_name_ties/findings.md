# FF3 findings: memory ties settled by name, a fault fix in nature v13

**Status: not final until the blind recompute** (`recompute_ff3.md`, written from the models' real replies).

Every number is from `results.md` (analyse_ff3.py, frozen before data) on run 42177471748:
- 3 arms × 32 paired seeds 23901–23932, 200 years, years 100–200 counted;
- zero checks All: PASS (`zero_local.log`, accepted by the cloud with skip_zero=local; `code_ff3` fingerprint 2ccd866b…);
- 96 of 96 worlds present under one fingerprint.

## The answer in one line
**No harm.** The fix does what it should: a new recipe that enters a full memory is now kept more often, and the
name no longer decides. By the frozen rule it is adopted as nature v14 (a fault fix; no confirmatory run).

## The frozen decision
- **Population:** living-weeks f ÷ v13 = **0.9636 [0.8506, 1.0867]**. The guard needs below 0.90 with the upper bound
  below 1, so it is not raised. The sham ÷ v13 = 0.9576 [0.8526, 1.0747], the same size of difference.
- **Extinctions:** f 2, v13 1, sham 2. One extra world, not 3 or more, so the guard is not raised.
- **Reading: no harm.**

## The two flags (the frozen rule asks for a read-only explanation before adoption)
1. **Recipe evictions with a tie, per eviction: f ÷ v13 = 0.749 [0.687, 0.822].** This is the fix's own mechanism.
   - In v13 a new recipe enters at value 0 and loses every tie by its name, so the memory keeps old untried recipes at
     0 and keeps tying them with each newcomer.
   - With the fix, the dropped one is drawn among the tied. The newest is dropped less often (per eviction 0.873
     [0.835, 0.905] of v13's), and **kept at birth rises from 0.298 to 0.387** (described).
   - The untried zeros are cleared over time, so fewer evictions meet a tie.
   - The sham shows no such change (0.998). Nothing here points to harm.
2. **Kinds made again by their inventor within 5 years: f ÷ v13 = 0 [0, 0].** One kind in one v13 world, against 0
   in f and 0 in the sham, out of about 3,000 new kinds per arm. A ratio of single events carries no information, and
   remaking was already at the floor (RF1). Nothing here points to harm.

**Neither explanation finds harm, so adoption goes ahead by the frozen rule**, after the blind recompute.

## Described
| arm | recipe evictions; with a tie; the newest dropped; kept at birth | world-new kinds | makes per adult-year |
|---|---|---|---|
| v13 | 17,646; 11,310; 12,387; 0.298 | 3,183 | 0.0724 |
| f | 20,193; 9,691; 12,370; 0.387 | 3,052 | 0.0748 |
| sham | 17,634; 11,282; 12,319; 0.301 | 3,221 | 0.0754 |

- The other memories changed little in rate: known marks, records of sources and puzzles all had f ÷ v13 within
  [0.85, 1.11] and no flag.
- The fix drew 430,729 times over the four memories in years 100–200.

## Against the assistant's prior (questions.md)
| prior | result |
|---|---|
| no guard raised, about 90% | **yes** |
| the newest recipe kept at birth much more often | **yes**, 0.298 → 0.387 |
| world-new kinds and makes change a little; remaking stays near 0 | yes (kinds 0.959, makes 1.033; remaking 0) |

## Found while building, not part of FF3
`marks._link` also trims a mark's links with `sorted(links, key=(strength, text))[:n]`, a tie settled by text. It was
not in the frozen plan and is left as it is. It is noted for a later round.
