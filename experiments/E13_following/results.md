# E13 — Following those who visibly do well (B2) · Results

Base world A2-full (E9 code, anticipation 1.0). Arm A control; Arm B follows the best-fed visible adult; Arm C the same among adults whose children all live. Seeds 301–304, 120 years. Frozen as `E13-frozen` before any code.

## Validity

- Probe read-only (both codes): **yes**
- All runs finished: **yes**
- Zero check: E13 code with B2 off reproduces E9 A2-full (seed 304): **yes**
- Arm A reproduces E9 A2-full (all seeds): **yes**
- Code unchanged during runs: **yes**
- **Valid.**

## Leak test (hard fail)

- Arm B: – (n=0) vs Arm A – (n=0) → –
- Arm C: 0.385 (n=3) vs Arm A – (n=0) → –

**Leak test FAILED.** (Most adults see a better-fed neighbour forage at some point, so this group is small.)

## Headline: does preparation survive success?

| arm | planner-autumns | followed by planning the next autumn | share |
|---|---|---|---|
| A | 112 of 11560 | 1 | 0.9% |
| B | 462 of 11852 | 29 | 6.3% |
| C | 106 of 10743 | 2 | 1.9% |

## The rest of the chain

| measure | A | B | C |
|---|---|---|---|
| habit value, autumn foraging while stocked (mean of 10-year samples; seeds 301/302/303/304) | 0.183 / 0.185 / 0.166 / 0.185 | 0.287 / 0.227 / 0.307 / 0.344 | 0.220 / 0.239 / 0.233 / 0.102 |
| planners' neighbours, autumn foraging the next year | 0.443 (n=1815) | 0.476 (n=7974) | 0.464 (n=1642) |
| planner-autumns | 112 | 462 | 106 |
| child-winters whose carer holds 20+ | 39.1% | 47.2% | 41.1% |
| children's winter starvation per child-winter | 0.80% | 0.83% | 0.67% |

## Frozen predictions (Arm B), scored

1. **wrong** — headline: 29 of 462 planner-autumns followed by planning (6.3%; needs ≥ 10% with ≥ 20; Arm A 1 of 112).
2. **confirmed** — manipulation check: habit value higher than Arm A in 4 of 4 seeds.
3. **wrong** — planners' neighbours' foraging, B ÷ A: 1.07 (needs ≥ 1.1).
4. **confirmed** — planner-autumns, B ÷ A: 4.12 (needs ≥ 2).
5. **confirmed** — carers with 20+: +8.1 points (needs ≥ +5).
6. **wrong** — children's winter starvation, B ÷ A: 1.04.
7. **wrong** — leak test.

Arm C against Arm B is reported above, with no directional prediction.

**The leak test failed: E13 is declared failed whatever its other results.**

## Reading: the frozen verdict, and why

**By its own frozen rule, E13 is declared failed: the leak test did not pass.** It did not pass because it could not be
performed. The test compares adults who never once saw a better-fed adult forage; over 120 years essentially everyone
does, so the group was empty in Arm A (0) and Arm B (0), and 3 people in Arm C. An empty group cannot show a leak and
cannot show its absence. The assistant designed this test and noted the group would be small, but did not foresee that it
would be empty; the frozen analysis scores an empty test as failed, and that verdict stands.

**What the other measures show (recorded, not claimed as a result).** In Arm B, copying a better-fed neighbour's foraging
moved every link before deaths more than any mechanism tried so far: planner-autumns 4.1× Arm A (462 against 112);
planning the next autumn as well 29 times against once (6.3% against 0.9%, short of the 10% headline); habit value for
autumn foraging while stocked higher in all four seeds; carers holding 20+ food up 8.1 points. Neighbours of planners
foraged only 1.07× as much, and children's winter starvation did not change. Arm C (models restricted to adults whose
children all live) did much less, plausibly because the filter left few models; its seed 304 world died out.

**What would settle it:** a replication, frozen before any run, with a leak test that can be performed: for example,
comparing autumn weeks in which a person had no better-fed forager within sight against matched weeks in the control, and
an automated test proving that B2 changes nothing for anyone with no visible model.
