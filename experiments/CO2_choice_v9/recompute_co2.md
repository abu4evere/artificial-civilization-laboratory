# CO2 — Independent recompute (31 October 2026, just after midnight)

**Who:** GPT and Gemini, each in a fresh chat with no earlier context. GPT:
https://chatgpt.com/c/6ae563f4-fb38-83ea-ac5f-fd0f0374df45. Gemini: https://gemini.google.com/app/79cd08cfad35ec3c.
An earlier Gemini attempt (chat 4f626029c4a2e8dd) never finished: the Chrome extension dropped mid-calculation and the
chat was not saved. It was resent in a fresh chat, with one added sentence asking for vectorised bootstrap code; the
computation asked for is unchanged.
**What they saw:** `recompute/co2_one_file.csv` (raw per-world sums: Q5's parts over late adult offered weeks, and Q2's
counters per period and matched state; built by `recompute/build_one_file.py`, which computes no ratio, weight or
interval) and `recompute/prompt.txt`. **Not** the analysis script, `results.md` or the findings. Recorded from their
replies.

| measure | analysis (`analyse_co2.py`) | GPT | Gemini | match |
|---|---|---|---|---|
| Q5 habit share | +0.351 [+0.346, +0.356] | 0.3513 [0.3460, 0.3563] | 0.3513 [0.3460, 0.3564] | yes |
| Q5 curiosity share | −0.051 [−0.053, −0.049] | −0.0509 [−0.0526, −0.0490] | −0.0509 [−0.0526, −0.0490] | yes |
| Q5 multiplicity and spread | +0.138 [+0.133, +0.142] | 0.1377 [0.1327, 0.1420] | 0.1377 [0.1329, 0.1420] | yes |
| Q5 built-in and thought pull | +0.562 [+0.554, +0.571] | 0.5619 [0.5533, 0.5710] | 0.5619 [0.5534, 0.5708] | yes |
| Q5 reading | built-in pull carries it; curiosity works against the gap | built-in carries it; curiosity upper bound below 0 | same | yes |
| Q2 kept states | 24 | 24 | 24 | yes |
| Q2 Δ U_other | +0.639 [0.633, 0.646] | 0.6394 [0.6330, 0.6454] | 0.6394 [0.6330, 0.6454] | yes |
| Q2 Δ habit | +0.559 [0.55, 0.569] | 0.5592 [0.5497, 0.5689] | 0.5592 [0.5498, 0.5687] | yes |
| Q2 multiplicity / per-entry / spread | +0.011 / +0.128 / −0.059 | 0.0107 / 0.1282 / −0.0587 | same | yes |
| Q2 habit share | 0.87 | 0.8747 | 0.8747 | yes |

**Verdict:** every key number and the reading agree across the analysis, GPT and Gemini. The findings are final.
