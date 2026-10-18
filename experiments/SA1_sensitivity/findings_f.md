# SA1-F — The sensitive and near-the-line settings on 256 new seeds: findings

Frozen as `SA1F-frozen` (signed off 14 October 2026; operational details fixed 16 October, before any data). Table:
`results_f.md`, from `analyse_sa1f.py`. Run: `run_sa1f.py` (resumed twice after interruptions, finished worlds skipped
and checked whole; log `run_sa1f.log`). Part B (the evidence reviews): `evidence_sight_range.md`.

## Validity

Zero check PASS; all 2,304 worlds present; one code fingerprint per code copy; sham quiet (90 vs 82 died out; p = 0.38).
**Valid.** Control: 82 of 256 died out (32.0%; SA1's 64 worlds: 34%).

## The frozen readings

Yardstick: half of F2's effect on F1's seeds, 0.117. Holm over the seven; every reading below survives Holm.

**The four sensitive settings**

| setting | value | died out (C: 82) | effect [95%] | reading | SA1 (64 worlds) | against SA1 |
|---|---|---|---|---|---|---|
| `perception` (sight) | 2 | **168** | −0.336 [−0.402, −0.270] | **sensitive** | −0.422 | differs (smaller) |
| `perception` | 8 | **31** | +0.199 [+0.133, +0.266] | **sensitive** | +0.219 | agrees |
| `reach` | 6 | 103 | −0.082 [−0.148, −0.016] | **moves survival** (below the yardstick) | −0.219 | differs (smaller) |
| `mortality_base` | 3.0e-5 | 115 | −0.129 [−0.188, −0.066] | **sensitive** | −0.188 | agrees |

**The three near the line**

| setting | value | died out | effect [95%] | reading | SA1 | against SA1 |
|---|---|---|---|---|---|---|
| `forage_base` | 6 | 120 | −0.148 [−0.211, −0.086] | **sensitive** | −0.188 | agrees |
| `conception_chance` | 0.02 | 113 | −0.121 [−0.191, −0.051] | **sensitive** | −0.141 | agrees |
| `reach` | 2 | 120 | −0.148 [−0.215, −0.082] | **sensitive** | −0.141 | agrees |

## What it shows

1. **Every one of the seven settings moves survival** at 256 worlds; none reads "no meaningful effect". Six are
   "sensitive" (beyond half of F2's effect); `reach` × 2 moves survival by less (−0.082).
2. **Sight still decides most.** Halving it doubles extinction (82 → 168 of 256); doubling it cuts it by more than half
   (82 → 31). SA1's 64-world estimate of halving was larger than the true effect (−0.42 against −0.34), as small samples
   with a large first effect tend to be.
3. **The three near-the-line settings were real effects that 64 worlds could not show**: less food from foraging, a lower
   chance of conceiving, and a shorter weekly reach each raise extinction by about 12–15 points.
4. **Every halving hurts, and the doublings of sight help**: ACL's worlds sit close to a demographic edge on several
   unanchored numbers at once. This repeats SA1's conclusion with power: extinction findings are relative (between arms
   of one study), never absolute.
5. Described: tools' share of foraged food rises a little in the harder worlds (2.6% → 3.1–3.3%), still small.

## The assistant's prior, against the result

| prior (frozen) | result |
|---|---|
| `perception` both ways and `mortality_base` × 2 stay sensitive | **right** |
| `reach` × 2 stays sensitive but smaller | **half right**: smaller, and below the yardstick (moves survival) |
| near the line: `forage_base` × 0.5 becomes sensitive | **right** |
| the other two near-the-line arms do not | **wrong**: both are sensitive |

## What it decides (the creator decides)

Nothing in nature changes. It strengthens two open decisions: anchoring sight (Part B: as people in contact per week, ACL
9 against a forager camp's 15, `evidence_sight_range.md`) and the ageing scale (mortality × 2 is sensitive; still paused
until ACL's adult mortality is measured). Reach stays unanchorable (Part B). Food from foraging and the chance of
conceiving join the list of unanchored numbers that matter, with the same caveat on every extinction finding.
