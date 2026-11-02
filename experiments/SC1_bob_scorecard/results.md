# SC1 — A scorecard of the creator's twelve capacities on live v11: results

Frozen as `SC1-frozen` (operational notes 1 and 2). run_sc1.py, analyse_sc1.py (written before data).

## Validity

- Zero checks (All: PASS, same `code_v11` fingerprint): **yes**
- All worlds present (32): **yes**
- One fingerprint, `code_v11`'s: **yes**
- Every habit update replays exactly (mismatches 0): **yes**

**Valid.**

## Measured capacities (primary contrasts)

| capacity | contrast | value [95%] | min. effect | sample | reading |
|---|---|---|---|---|---|
| 3 (the rule) | C3: mean abs(q - G), k 0-19 minus k 80+, adults 16-44 | -0.0811 [-0.1012, -0.0638] | 0.02 | 23 common cells; 3,113,169 + 1,631,151 updates | **inconclusive** |
| 4 | C4: P(alternative | surprising test) - P(alternative | confirming test) | -0.0381 [-0.1471, +0.0279] | 0.05 | followed tests: surprising 1,372, confirming 1,650 | **inconclusive** |
| 5 | C5: P(make | wanted gather) - P(make | not wanted), standardized | +0.0105 [+0.0085, +0.0495] | 0.05 | gathers: wanted 1,316,549, not wanted 61 | **inconclusive** |
| 6 | C6: P(remade in 5 years | more useful) - P(remade | less useful); fallback (op. note 2): top third (> 1.930) vs bottom third (<= 1.554) | +0.0000 [+0.0000, +0.0000] | 0.05 | world-new kinds 3,883 (more useful 1,275, less 1,312) | **inconclusive** |
| 7 | C7: P(acted | own puzzle) - P(acted | told), size-matched | - [-, -] | 0.05 | told puzzles in the bins 2 (< 30); own 29,743 | **not measurable in v11 (too few told puzzles of matching size)** |
| 9 | C9: P(told place verified) - P(random tile at the same distance passes) | +0.4102 [+0.3925, +0.4283] | 0.1 | checked 396,764 (water 161,974: 161,937 vs 119,072; game 234,790: 212,282 vs 92,377) | **positive contrast detected** |
| 10b | C10b: P(part learned from someone) - repertoire's learned share | -0.0375 [-0.0449, -0.0309] | 0.05 | world-new nested kinds 3,989 (part learned from someone 35) | **inconclusive** |
| 12 | C12: relative cut in held-out error from adding year-t actions to Model A (with habits) | +0.0779 [+0.0719, +0.0840] | 0.05 | person pairs (t, t+5) 56,353 | **positive contrast detected** |

A reading is "positive contrast detected" only when the interval's lower bound exceeds the minimum effect; otherwise "inconclusive" (never "absent"). C3 reads "the written rule works"; C5 reads at most "organized production detected".

## Given (described)

- **1. Perception:** 0.986 of adult decisions have company within reach (17,566,419 decisions).
- **11. Motivation:** adults' mean mood 0.756, loneliness 0.286 (337,000 adult-years).

## Not measurable in v11 (described)

- **2. Memory, retrieval when relevant:** adults hold 45.3 memories on average; 0.36 of them were told.
- **3 (transfer):** one habit value per situation x action; nothing generalizes.
- **8. Self-model:** nothing represents a person's own ability or uncertainty.
- **10a (social cognition):** whom to trust is written. Social learning, the paths of recipe gains: made 0.694, taught 0.120, read 0.086, taught_variant 0.064, heated 0.036.

## Secondary (described, not decisive)

- **C10b improvement:** 0.690 of new nested kinds beat their best part on its best use (3,942 compared).
- **Holders per kind** first made in years 100-200: mean 1.18, median 1 (4,374 kinds).
- **Kinds alive that outlived their first maker:** 0.668 of alive kind-years.
- **Nesting depth** (mean of adults' deepest known kind): years 100-125 2.92, years 175-200 2.45.
- **C12 cross-situation (Gemini):** a person's own choice bias in familiar situations correlates 0.322 with their bias in rare ones (fewer than 5 earlier visits), against 0.008 for a shuffled pairing (11,525 people).

