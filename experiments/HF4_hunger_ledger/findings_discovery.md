# HF4 — The hunger ledger: discovery (seeds 501–516; holdout not yet run)

Questions and decision rule frozen as `HF4-questions`. Instrumented logging copy shown to change nothing (state hash
equals HB1's code, both arms, two seeds). Valid: all 32 replays reproduce HB1's and F1's saved populations; code
unchanged. Full table: `results_discovery.md`.

| | H | C | H ÷ C |
|---|---|---|---|
| median coverage (food held ÷ need, at eating) | 2.551 | 2.741 | **r = 0.931** |
| starving share of adult-weeks (actual) | 0.051 | 0.033 | 1.564 |
| shifted prediction (C's coverage × r) | **0.042** | | 0.813 of H's actual |
| share of starving weeks that are deep (< 0.5) | 0.357 | 0.343 | 1.042 |
| adult-weeks with coverage ≥ 3 | 0.373 | 0.430 | 0.868 |
| carers: share of food given to dependants just before eating | 0.222 | 0.189 | |

**Against the frozen rule (discovery only):** r ≥ 0.9 (yes) and the shifted prediction within ±25% of H's actual
starving share (0.813: yes) → **small shifts: yes** on discovery. Tail: no (the prediction is not more than 25% short;
deep starvation is about as common in both).

**A weakness in the frozen rule, recorded now, before the holdout (rule 19):** the ±25% band is measured against H's
*total* starving share. Measured against the *extra* starvation (H's share minus C's: 0.018), the shift accounts for
0.042 − 0.033 = 0.009, **about half**. The rule, as frozen, can pass while explaining only half of what it was meant to
explain. The verdict will be reported by the rule as frozen, with this beside it; the rule is not changed.

**Noted, not read:** the whole distribution moved down a little (fewer adult-weeks with three or more weeks of food in
hand, more in every band below); carers under H gave a larger share of what they held to their dependants (0.222 against
0.189).

Next, frozen order: holdout seeds 1601–1616, then `analyse_hf4.py both` and the frozen rule.
