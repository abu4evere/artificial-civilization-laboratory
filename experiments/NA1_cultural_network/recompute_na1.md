# NA1 — Independent recompute (27 October 2026)

**Who:** GPT and Gemini, each in a fresh chat with no earlier context.
**What they saw:** the raw kind rows (`na1_kinds.csv`) and ratchet rows (`na1_ratchet.csv`), a field dictionary and
the frozen definitions. **Not** the analysis script, `results.md` or the findings. Files were checked as attached
before each message was sent.

| measure | analysis | GPT | Gemini | match |
|---|---|---|---|---|
| seeds; world-born useful kinds | 32; 20,593 | 32; 20,593 | 32; 20,593 | yes |
| co-present / talked / offered / took / made / passed | 2,044,075 / 1,736,075 / 233,771 / 4,694 / 156 / 95 | same | same | yes |
| talked / co-present | 0.8493 | 0.849321 | 0.849321 | yes |
| offered / talked | 0.1347 [0.123, 0.146] | 0.134655 [0.1230, 0.1458] | 0.134655 [0.122978, 0.145919] | yes |
| took / offered | 0.0201 [0.0177, 0.023] | 0.020079 [0.017643, 0.022991] | 0.020079 [0.017629, 0.023033] | yes |
| made / took | 0.0332 [0.0241, 0.044] | 0.033234 [0.023898, 0.044163] | 0.033234 [0.023907, 0.043895] | yes |
| passed / made | 0.6090 | 0.608974 | 0.608974 | yes |
| largest loss | offered → took | offered → took (ln −3.908) | offered → took (ln −3.908) | yes |
| took / offered by era | 0.0311 / 0.0041 / 0.0032 | 0.031087 / 0.004134 / 0.003237 | 0.031087 / 0.004134 / 0.003237 | yes |
| median co-present; median offered (by era) | 66, 82, 77; 1, 3, 3 | same | same | yes |
| improvements; completed chains | 123; 38 (5.97 and 1.85 per 1,000) | 123; 38 (5.9729; 1.8453) | 123; 38 (5.972903; 1.845287) | yes |

**Verdict:** every key number agrees across the analysis, GPT and Gemini. The findings are final.
