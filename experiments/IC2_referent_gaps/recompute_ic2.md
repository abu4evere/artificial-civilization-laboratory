# IC2 — independent recompute

**Who:** GPT and Gemini, each in a fresh chat with no earlier context, from raw per-world counts only
(`recompute/ic2_one_file.csv`, built from the 32 output JSONs by a short script, not by `analyse_ic2.py`), without the
analysis script. Sent 28 October 2026, after the Chrome extension was signed in to this account.

GPT: https://chatgpt.com/c/6ae21b12-e84c-83ea-833b-aab9ebd60dd9. Gemini: https://gemini.google.com/app/4068de4bb376b35b.
Recorded from their replies.

| measure | analysis | GPT | Gemini | match |
|---|---|---|---|---|
| water: shared per adult-year | 4.05 [3.73, 4.36] | 4.0515 [3.7345, 4.3566] | 4.0515 [3.7325, 4.3578] | yes |
| water: repeated pairs | 0.870 | 0.8703 | 0.8703 | yes |
| water: gaps / relevant per adult-year | 0.05 / 0.000 | 0.0535 / 0.0000 | 0.0535 / 0.0000 | yes |
| game: shared per adult-year | 2.00 [1.76, 2.24] | 1.9962 [1.7603, 2.2402] | 1.9962 [1.7590, 2.2353] | yes |
| game: repeated pairs | 0.807 [0.786, 0.828] | 0.8071 [0.7857, 0.8280] | 0.8071 [0.7855, 0.8277] | yes |
| game: gaps per adult-year | 2.23 | 2.2317 | 2.2317 | yes |
| **game: relevant per adult-year** | **0.404 [0.340, 0.468]** | 0.4036 [0.3403, 0.4678] | 0.4036 [0.3386, 0.4675] | yes |
| danger: shared per adult-year | 0.02 | 0.0159 | 0.0159 | yes |
| danger: repeated pairs | 0.332 | 0.3317 | 0.3317 | yes |
| danger: gaps / relevant | 0.00 / 0.000 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | yes |
| workable referents | none | none | none | yes |

Interval ends differ in the third decimal at most, from different bootstrap draws.

**Verdict:** every key number agrees across the analysis, GPT and Gemini. The findings are final.
