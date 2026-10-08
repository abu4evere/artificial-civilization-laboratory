# MC1-L — The moving camp, re-tested at proper power (DRAFT for the creator's sign-off; nothing frozen, nothing run)

## Why

MC1 (frozen, valid) kept couples together (apart 57.8% → 17.0%), raised births 12% and caused no extra hunger, but showed
**no detectable effect on extinction** at 64 worlds (26 vs 22; p = 0.503). N8's power calculation (`N8_partner_finding/
power.md`), built from the control and sham runs, shows that **64 worlds detect half of F2's effect only 32% of the
time**; 256 worlds detect it 92% of the time. MC1's null therefore cannot rule out a benefit up to about half of F2's.
The creator chose to settle this before moving to P2: "Before throwing MC1 away, check whether you simply couldn't see
it." If P2 were run first and helped, its benefit could not be told apart from co-residence's.

## What is re-tested

**Exactly MC1, unchanged:** the same code copy (`MC1_moving_camp/code_mc1`; its fingerprint must equal MC1's), the same
setting (`moving_camp = 1`: partners within reach end each week together on the better of their two tiles), the same
sham (`sham_draw = 1`), the same observers (F1's, C1's for 40 years, HF4's ledger). No pilot (MC1's passed with this
code).

## Worlds

**256 new seeds, 2001–2256**, never run in any arm. MC1's 64 seeds are not reused: their result has been seen, and a
re-test that included them would partly re-count it. Arms on every seed: **C** (settings off), **M** (moving camp),
**S** (sham). 768 world-runs, 120 years each (about 9 hours at MC1's pace).

## Rule 14: baseline survival first

Reported from C on the new seeds before anything else (F1's rate on its seeds was 34%).

## Measures (population beside every measure)

- **Manipulation check:** couples apart per partnered non-pregnant woman-week, M ≤ half of C (as MC1).
- **Primary:** extinctions (of 256), M against C, paired exact two-sided sign test; S against C likewise.
- **Effect size (new, so that a null can be read):** the paired difference in extinction share, C − M, with a 95%
  interval (percentile bootstrap over worlds, 10,000 resamples, fixed generator seed), set against **half of F2's
  effect** in absolute terms on these seeds: half of F2's relative reduction (0.68 / 2 = 0.34) times C's extinction
  share.
- Births per woman-year, food held at eating (ledger), starving share, child deaths per birth, median population.

## Outcome rule (proposed)

| | reading |
|---|---|
| M fewer extinctions than C, sign test p < 0.05 | **co-residence saves worlds**: MC1 is real; its size is the effect estimate |
| M more extinctions than C, p < 0.05 | **co-residence harms survival** (examined read-only) |
| p ≥ 0.05 **and** the interval's upper bound for C − M is below half of F2's effect | **MC1 is genuinely weak**: any benefit is smaller than half of F2's; move to P2 with confidence |
| p ≥ 0.05 and the interval reaches half of F2's effect | **still unresolved** at 256 worlds; reported as such, the creator decides |

Beside it: S against C (should not reach p < 0.05); if it does, the noise is larger than the test assumes and every
reading carries that caveat.

## Hard stops

- `code_mc1`'s fingerprint equals MC1's recorded one before and after every run.
- Zero check repeated on two of the new seeds: settings off with the ledger on equals the control code (state hash).

## Priors (written before any run; not predictions to test)

- **Assistant:** no detectable benefit, and the interval excludes half of F2's effect ("genuinely weak"): MC1's point
  estimate on 64 worlds was four more extinctions, not fewer, and its extra births came with more child deaths. Held
  loosely.
- **The creator's adviser (as quoted):** strong positive, still null, or small positive all considered possible.

## Decisions for the creator

1. **Seeds:** 256 new (proposed), or 192 new plus MC1's 64 (cheaper by a quarter, but partly re-counts a seen result).
2. **Keep the sham arm** (proposed; about 3 of the 9 hours).
3. **The outcome rule**, including the new "genuinely weak" reading against half of F2's effect.
