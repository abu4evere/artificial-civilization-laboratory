# OP1 — Objects in the world. Results

Frozen as `OP1-frozen` (operational note 1). run_op1.py, analyse_op1.py (written before data).

## Validity

- Zero checks: **yes**
- All worlds present (96 of 96): **yes**
- One fingerprint (`code_op1`): **yes**
- Every overflow dropped and dropped = picked up + on the ground (mismatches 0): **yes**

**Valid.**

## M — manipulation

Arm o: 60774 carry-limit overflows from making, 64345 drops (with inheritance), 0 deleted; every world with an overflow has drops: True. Arm c: 49874 made things deleted at the limit. **M passes.**

## P — primary: of the things dropped, the share later picked up by a living person (arm o)

Dropped 64345; picked up 60434: **0.9392 [0.9171, 0.9574]**; by someone other than the one who dropped it 0.961 of pick-ups; on the ground at the end 3911; median weeks on the ground (median of world medians) 5.0.
**P supports** (at least 0.05 with the lower bound above 0).

## H — flags

Mean population, years 100-200: c 128.4, o 108.5 (ratio 0.845), sham 115.3 (FLAG). Extinct: c 1, o 0, sham 2 (no flag).

## D — described (years 50-200)

| measure | c | o | sham |
|---|---|---|---|
| made things held per adult | 0.555 | 1.018 | 0.525 |
| making events per adult-year | 0.061 | 0.065 | 0.064 |

**The change is supported by the frozen rule; flagged, so adoption is not recommended.** Adoption is left to the creator.

