# MC1-L — The moving camp re-tested at proper power: findings

Frozen as `MC1L-frozen` (signed off by the creator). MC1's code copy and setting unchanged; 256 new seeds (2001–2256),
120 years; arms C (settings off), M (moving camp), S (sham). Sized from N8's power table (0.92 to detect half of F2's
effect). Tables: `results.md`, from `analyse_mc1l.py`. **Valid:** fingerprint equals MC1's, zero check on seeds 2001 and
2002, code unchanged in every run. (The run was interrupted twice when sessions ended; the runner skips finished outputs,
every saved file was checked as complete, and all 768 carry MC1's fingerprint.)

## Baseline (rule 14)

The control died out in **87 of 256** worlds (34.0%), the same share as on F1's 64 seeds (22 of 64, 34%).

## The frozen reading

| | C | M | S |
|---|---|---|---|
| couples apart, per partnered non-pregnant woman-week (manipulation: ≤ half of C) | 56.9% | **16.4%** | 56.7% |
| worlds died out (of 256) | 87 | **93** | 98 |
| paired against C: saved / lost | – | 29 / 35 | 32 / 43 |
| exact two-sided sign test | – | **p = 0.532** | p = 0.248 |

**Effect** (C − M extinction share): **−0.023, 95% interval [−0.086, +0.039]**. Half of F2's effect on these seeds:
0.116. The upper bound of the interval is below it.

**Frozen rule: MC1 is genuinely weak.** Any benefit of the moving camp on extinction is smaller than half of F2's
effect; the rule says to move to P2 with confidence. The manipulation worked again (couples apart 57% → 16%); the sham
did not reach significance.

## Descriptive (not part of the frozen outcome)

| | C | M | S |
|---|---|---|---|
| births per woman-year | 0.133 | **0.153** | 0.129 |
| child deaths per birth | 0.200 | 0.247 | 0.200 |
| ledger: starving share of adult-weeks | 0.036 | 0.039 | 0.036 |
| ledger: median food held ÷ need at eating | 2.692 | 2.680 | 2.687 |
| women 16–45 without a partner (share of woman-weeks) | 0.551 | 0.578 | 0.567 |
| median population, years 40 / 80 / 119 | 24 / 21 / 20 | 26 / 24 / 22 | 23 / 17 / 12 |

1. **MC1's pattern repeats on new seeds.** More births (+15%, against +12% in MC1), food held at eating unchanged, and
   more of the extra children dying (0.247 against 0.200 per birth; MC1: 0.234 against 0.196). Why the extra births do
   not carry worlds through is still **not measured and not explained**.
2. **The point estimate leans the wrong way**, as in MC1 (26 vs 22): 93 vs 87 here. Neither is significant and the
   interval includes zero; it is recorded, not read as harm.
3. **The noise is as N8's power model assumed.** The sham changed the fate of 75 of 256 worlds (29%; the model used
   18 of 64, 28%). The power calculation this test was sized from holds on fresh seeds.

## Reading (caps)

- What is shown: on 256 new worlds, keeping couples together with a moving camp does not reduce extinction by as much
  as half of what perfect partner finding did; most likely it does little or nothing.
- What is not shown: that it does nothing at all (an effect up to about +0.04 is not excluded), or why its extra
  births are lost.
- Consequence for the thread: pair stability limits births, not survival; this is now a confident null, not an
  underpowered one. F2's lever, finding partners, remains the one to test, at this size (N8: P2, outward dispersal).
- MC1 is not added to ACL's nature by this result; that is the creator's decision.

**Next: the creator decides** whether to design P2 (outward instead of random steps when no eligible partner is in
sight) at 256 worlds, with a sham and a paired test.
