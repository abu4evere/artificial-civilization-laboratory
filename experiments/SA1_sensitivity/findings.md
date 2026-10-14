# SA1 — How much do ACL's findings rest on numbers nobody anchored? Findings

Frozen as `SA1-frozen` (with the note on where the sham runs, appended before any data). Control code (`code_e13r`;
sham in `code_p2`, settings off); F1's 64 seeds; 120 years; one setting × 0.5 or × 2 per arm. Tables: `results.md`, from
`analyse_sa1.py`, unchanged since freezing (run as `PYTHONIOENCODING=utf-8 python analyse_sa1.py`, as LK1's, so the
console can print "×"). Run 13 October 09:04 to 14 October 04:56 (the PC slept about seven hours of it; the runner
resumed by itself).

## Validity

Zero check (observers leave the world unchanged): yes. Control re-run reproduces F1's saved populations on every seed:
yes. One fingerprint per code copy: yes. No error log. **Valid.** The sham was quiet (24 vs 22 died out, p = 0.815).

## Baseline (rule 14)

The control re-run died out in **22 of 64** worlds (34.4%), exactly as F1. Half of F2's effect: **0.117**.

## The frozen reading

| setting | × 0.5 | × 2 |
|---|---|---|
| `perception` (4 tiles) | **sensitive**: 49 died out (effect −0.42, Holm p 6 × 10⁻⁶) | **sensitive**: 8 died out (+0.22, Holm p 0.039) |
| `reach` (3 tiles) | no sign (31; −0.14, p 0.078) | **sensitive**: 36 died out (−0.22, Holm p 0.026) |
| `mortality_base` | no sign (21) | **sensitive**: 34 died out (−0.19, Holm p 0.020) |
| `forage_base` (12) | **sensitive** by the raw test, **not after Holm**: 34 died out (−0.19, p 0.017, Holm 0.135) | no sign (21) |
| `conception_chance` (0.04) | no sign (31; −0.14, p 0.078) | no sign (20) |
| `camp_radius` (2 tiles) | no sign (21) | no sign (27) |

"No sign" is **not** "robust": with 64 worlds the interval is about ±0.12, the size of the threshold itself (the frozen
reading). Two arms sit near the line, with intervals reaching −0.28: `conception_chance` × 0.5 and `reach` × 0.5 (both
31 died out, p = 0.078).

## What it means (the frozen consequences)

1. **ACL's survival rests strongly on how far people see.** Halving sight (4 → 2 tiles) kills three worlds in four
   (49 of 64); doubling it (→ 8) saves most (8 of 64). This is among the largest effects measured in ACL: about the size of WS1's
   80 founders (+0.41), and larger than F2's perfect partner finding (+0.23 on these seeds). Sight is the one sense through which people find partners, food, water and each
   other (14 uses in the code), so the result fits everything since F1: worlds die when people cannot find each other.
2. **Range cuts both ways.** Doubling how far a person can travel in a week (3 → 6) *raised* extinction (36 of 64).
   Why is not measured; the setting acts in 29 places at once. Recorded, not explained.
3. **Mortality's scale moves survival** in the obvious direction (× 2 → 34 died out); halving it showed no sign.
4. **Food:** halving foraging returns raised extinction (34), but the reading does not survive the correction for twelve
   tests; doubling it changed nothing (21), as expected in a world already abundant (E8.2). Tools' share of foraged food
   rose only to 3.5% when food was halved (control 2.6%): even a hungrier world barely makes tools pay.
5. **By the frozen rule, every finding about extinction and partner finding** (F1, F2, the C/MC1/HB1 thread, P2, N8,
   GF1, WS1, AA1's A5 and A6c, LK1) **now carries the note "rests on an unanchored value that moves survival strongly"**
   (perception; also reach and mortality). Comparisons between arms of one study are not undone by this: every arm had the
   same values. What changes is how far an absolute number, such as "34% of worlds die", may be stated.
6. **Evidence first:** `perception`, `reach` and `mortality_base` go first in line for an evidence review (anchor them, if
   evidence exists; Law 126). `mortality_base` has a natural anchor (forager life tables, e.g. Gurven & Kaplan 2007);
   `perception` and `reach` need a scale for a tile first, which N10 found has none.

## The assistant's prior, against the result

| prior | result |
|---|---|
| `conception_chance` sensitive | **not shown** (× 0.5 near the line) |
| `camp_radius` sensitive | **not shown** |
| `perception` sensitive | **right**, in both directions, strongly |
| `mortality_base` moves survival, the obvious way | **right** for × 2 |
| `forage_base`: halving raises extinction; doubling changes little | **right** in direction (halving does not survive Holm) |
| `reach`: unclear | sensitive for × 2, in the direction that raises extinction |

## Next (the creator decides)

- The **256-seed follow-up** approved in principle at sign-off ("only for settings that turn out sensitive or near the
  line"): candidates `perception` (both), `reach` (both), `mortality_base` × 2, `forage_base` × 0.5, `conception_chance`
  × 0.5. Not started: it needs a frozen plan.
- The **evidence reviews** for `perception`, `reach` and `mortality_base`.
- Nothing in nature changes: SA1 adopts no value (frozen: "not tuning").
