# HF4 — The hunger ledger: findings, and the HB1 question closed

Questions and decision rule frozen as `HF4-questions` (signed off by the creator; the HB1 question to be closed after
HF4, whatever it found). Instrumented logging copy of HB1's code, shown to change nothing (state hash equal, both arms, two
seeds). Discovery 501–516 (all replays reproduce HB1's and F1's saved runs); holdout on new seeds 1601–1616. Tables:
`results_both.md`.

## The frozen verdict: small shifts explain the hunger

| | discovery | holdout | rule |
|---|---|---|---|
| r = H's median coverage ÷ C's (food held ÷ need, at eating) | 0.931 | 0.937 | ≥ 0.9 |
| shifted prediction ÷ H's actual starving share | 0.813 | 0.829 | within ±25% |
| deep starvation (coverage < 0.5) as a share of starving weeks, H ÷ C | 1.042 | 0.999 | (tail needs > 1 and prediction > 25% short) |

**By the frozen rule: small shifts explain the hunger**, in both sets. Under HB1 the whole distribution of food held at
the moment of eating moved down by about 6–7%: fewer adult-weeks with three or more weeks of food in hand (0.373 / 0.376
against 0.430 / 0.428), more in every band below. The extra starvation is not a tail of a few badly-off people: deep
starvation is as common a share of starving weeks under HB1 as in the control.

## The caveat (recorded before the holdout; rule 19)

The ±25% band was measured against H's **total** starving share. Against the **extra** starvation HB1 caused, the shift
accounts for **about half**: discovery (0.042 − 0.033) ÷ (0.051 − 0.033) ≈ 0.50; holdout (0.042 − 0.035) ÷ (0.050 − 0.035)
≈ 0.47. The rule as frozen passes while explaining about half of what it was meant to explain. The verdict stands as
frozen; this is its limit.

## The HB1 question, closed (as the creator decided at HF4's sign-off)

| check | question | verdict |
|---|---|---|
| HB1 | does a shared home base keep couples together and worlds alive? | couples together (apart 57.8% → 0.1%), **extinction rose** (33 vs 22 of 64, p = 0.043; sham p = 0.815) |
| HF1 | did food run out around homes? | **not confirmed** (land ~3% less full) |
| HF2 | too many children? meat? | **neither** (dependants +8–12%; meat ~0.02% of food); gifts fell ~40% (lead) |
| HF3 | did lost gifts starve people? | **not supported** (help within reach as often) |
| HF4 | did small shifts push adults over the line? | **yes by the frozen rule**, explaining about half of the extra starvation |

**What is established:** a shared home base, as HB1 built it, makes ACL's people hungrier, through a broad, modest fall in
the food they hold when they eat (a little less food in, fewer adults with food to spare, fewer gifts, carers giving a
larger share to children), not through any single failure. About half of the extra starvation is accounted for by that
shift; the rest is not explained by anything tested. HB2 (a home that moves with the food) is **not** designed: its
premise, local depletion, was not confirmed.

**What follows (the creator's decision at sign-off):** the project returns to keeping couples together, with a different,
evidence-anchored design that does not tie each week's foraging to a fixed home.

## Priors

The assistant's prior (small shifts) matched the frozen verdict, after three wrong priors (HF1, HF2, HF3); given the
caveat, it matched only in part.
