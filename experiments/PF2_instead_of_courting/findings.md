# PF2 — what people do instead of courting: findings

Frozen as `PF2-frozen` (operational note on action groups appended before any data). Tables: `results.md`, from
`analyse_pf2.py`. 64 of MB1b's worlds (P4 and B16; discovery seeds 5301–5316, holdout 5317–5332) replayed exactly with
a logging copy that records each single adult's full option list. Run on GitHub's machines (`cloud-run`, run
39633048493) after 9 worlds had run here; those 9 were identical in both places.

## Validity

Zero check PASS (on GitHub and here); all 64 worlds present; **every replay equals MB1b's saved world** (64 of 64);
one code fingerprint. **Valid.**

## The frozen reading

**What wins instead of courting: subsistence**, in both arms and both sets. **Stands.**

| | P4 (discovery / holdout) | B16 (discovery / holdout) |
|---|---|---|
| **Q1** courting offered to her | 80.5% / 82.4% | 80.5% / 81.0% |
| courting offered to him only | 8.4% / 7.7% | 8.5% / 8.2% |
| not offered to either | 11.1% / 9.9% | 11.1% / 10.7% |
| **Q2** what was chosen instead (when offered): subsistence | 74.4% / 74.8% | 74.9% / 72.6% |
| other social (talk, give, care, play) | 18.7% / 18.4% | 18.5% / 19.7% |
| movement | 5.6% / 5.5% | 5.2% / 6.1% |
| rest | 1.1% / 1.1% | 1.2% / 1.3% |
| **courting's median share of the choice** | **0.1% / 0.1%** | **0.1% / 0.1%** |
| **Q3** (when not offered) crowded out of the nearest 12 | 52.6% / 50.2% | 58.6% / 52.5% |
| not within reach when deciding | 42.7% / 45.3% | 37.7% / 43.5% |

## What it shows

1. **Courting is almost always on the table, and almost never has a chance.** In about nine in ten of the weeks PF1
   called "not tried", courting the suitable man was among her options (or his). But its weight in the choice was
   tiny: a median of **one chance in a thousand**. The choice is weighted by score (softmax, temperature 0.2), so an
   option even a little below the best is very rarely picked, and courting scores well below foraging.
2. **What wins is food.** About three quarters of those weeks went to subsistence (foraging, gathering, taking,
   filling), a fifth to other social acts (talking, giving, caring, playing), and the rest mostly to moving.
3. **When courting was not offered**, it was usually because he was not among the 12 people she considers at the moment
   of deciding: in half of those weeks he was within reach but more than 12 others were nearer; in most of the rest he
   had moved out of reach by then.
4. Together with PF1: a partner is usually right there; courting is usually an option; it almost never wins against
   getting food; and when it is tried with a near-stranger, it is almost always refused. Smaller bands did not change
   any of these steps.

## Against the prior (frozen; kept as written)

- "Courting is usually offered (O1 or O2 in most S5 weeks)": **right** (about 89–90%).
- "It loses to subsistence": **right** (about three quarters).
- "Courting's median share of the choice is small (under 10%)": **right**, far smaller (0.1%).
- Second guess, "when not offered, mostly because he was not within reach at the moment of deciding": **partly
  wrong**: the larger reason is the 12-person limit on whom a person considers.

## What it cannot show

- Why courting scores so low: the code's courting score (`mind.py`) falls with hunger and rises with sociability and
  affection, but this audit records shares of the choice, not the parts of the score. Whether people are hungry in
  these weeks, and by how much, was not measured.
- Whether changing courting's score, the 12-person limit or the choice temperature would save worlds: any of these
  would be a change to nature (Law 126), needing evidence about real people first.
- It describes 80-founder worlds only.
