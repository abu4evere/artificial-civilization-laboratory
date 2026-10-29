# PL1 — independent recompute

**Who:** GPT and Gemini, each in a fresh chat with no earlier context, from raw per-world counts only
(`recompute/pl1_one_file.csv`, built from the 32 output JSONs by a short script, not by `analyse_pl1.py`), without the
analysis script. Sent 29 October 2026 (sleep mode). GPT: https://chatgpt.com/c/6ae2de64-c9cc-83ea-94e0-e2287ab118ab.
Gemini: https://gemini.google.com/app/e08a8536e74b4664. Recorded from their replies.

| measure | analysis | GPT | Gemini | match |
|---|---|---|---|---|
| **play share 3–6** | **0.0684 [0.0655, 0.0716]** | 0.0684 [0.0655, 0.0716] | 0.0684 [0.0655, 0.0716] | yes |
| play share 7–12 | 0.0121 [0.0110, 0.0134] | 0.0121 [0.0110, 0.0135] | 0.0121 [0.0110, 0.0134] | yes |
| play share 13–18 | 0.0032 [0.0030, 0.0035] | 0.0032 [0.0030, 0.0035] | 0.0032 [0.0030, 0.0035] | yes |
| available 3–6 / 7–12 / 13–18 | 0.942 / 0.999 / 0.987 | 0.9423 / 0.9991 / 0.9869 | 0.9423 / 0.9991 / 0.9869 | yes |
| 3–6 no-play weeks unavailable | 0.062 | 0.0619 | 0.0619 | yes |
| readings | below; declines; choice | below; yes; choice | below; yes; choice | yes |

**Verdict:** every key number and reading agrees across the analysis, GPT and Gemini. The findings are final.
