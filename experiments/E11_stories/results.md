# E11 — Stories that carry a hard season (S1) · Results

Arm 0 = E7 code; S1-low and S1-high = E11 code (O2 on, story 0.25 / 0.50). Seeds 301–304, 120 years. Frozen as `E11-frozen` before any code. Read in the creator's chain order; deaths last.

## Validity

- Probe read-only (both codes): **yes**
- All runs finished: **yes**
- Zero-story E11 code reproduces E10's O2 arm (seed 304): **yes**
- Arm 0 reproduces the saved E7 runs: **yes**
- Code unchanged during runs: **yes**
- **Valid.**

## Leak test (hard fail)

- s1low: 0.445 (n=2295) vs Arm 0 0.441 (n=2727) → 1.009
- s1high: 0.448 (n=2477) vs Arm 0 0.441 (n=2727) → 1.015

**Leak test passed.** (Few adults never hear such a story, so this group is small.)

## The chain, in order

| step | measure | Arm 0 | S1-low | S1-high |
|---|---|---|---|---|
| 1 | starvation deaths | 195 | 172 | 188 |
| 2 | tellings of hunger-death stories | 55489 | 46989 | 47196 |
| 3 | hearings accepted or recognised | 48342 | 40664 | 40927 |
| 4 | autumn foraging, heard a hunger story in the past year, never bereaved | 0.426 | 0.430 | 0.444 |
| 5 | adult-autumns holding 80+ (planners) | 0 | 16 | 53 |
| 6 | planner-autumns followed by planning the next autumn | 0 | 0 | 2 |
| – | median food entering winter | 11.8 | 12.0 | 12.6 |
| – | carriers made | 2038 | 1653 | 1983 |
| 7 | child-winters whose carer holds 20+ | 37.7% | 39.6% | 42.1% |
| 7 | children's winter starvation per child-winter | 0.72% | 0.78% | 0.76% |

## Frozen predictions, scored

1. **wrong** — listeners' autumn foraging, S1-high ÷ Arm 0: 1.04 (needs ≥ 1.2).
2. **wrong** — S1-high planners: 53 of 11554 (0.46%; needs ≥ 1%).
3. **wrong** — headline: planner-autumns followed by planning again, S1-high: 2 of 53 (3.8%; needs ≥ 10% with ≥ 20 planners; E9.3: 1 of 113).
4. **confirmed** — dose response: listeners low 1.01 vs high 1.04; planners low 0.15% vs high 0.46%.
5. **wrong** — carers with 20+: +4.4 points (needs ≥ +5).
6. **wrong** — children's winter starvation S1-high ÷ Arm 0: 1.05 (not interpreted: predictions 1, 2 and 5 did not all hold, so the chain does not reach step 7).
7. **confirmed** — leak test.

## Reading, in the creator's chain order and by the frozen decision table

- **Steps 1–3 are enormous.** About 40,000 hearings of hunger-death stories were accepted or recognised in each S1
  arm. The channel carries the experience exactly as the pilot suggested.
- **The chain breaks at step 4.** Listeners who never lost a child foraged only 1.04× as much in autumn (needs 1.2).
  Every downstream link rose in step with story strength (planners 0 → 16 → 53; carers holding 20+ 37.7% → 39.6% →
  42.1%), so the effect is real and faint. Repeat planning rose from E9.3's 1 in 113 to 2 in 53, too few to read.
- **Step 7 is not read** (predictions 1, 2 and 5 did not all hold); children's winter starvation was unchanged anyway.
- **Why it is faint (arithmetic from the code, not a new measurement).** A story's lesson is STORY × the listener's
  credence in the teller × the story's strength as told, and credence and strength are usually well below 1, so a
  typical lesson is far below 0.5. E9.4 measured that almost nobody prepares below an expectation of about 0.4. At these
  values, stories can rarely lift anyone over that threshold however often they are heard.
- **Decision table, first row:** stories of hunger, renewed for decades, did not move behaviour enough through this
  machinery. The pattern now repeats across E9, E10 and E11: lessons either reach few people strongly (own hunger,
  own loss) or many people faintly (witnessing, stories), and in no form tried has a lesson been both widespread and
  strong enough to cross the threshold at which people prepare.
