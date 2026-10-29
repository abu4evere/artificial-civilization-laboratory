# CU1 — independent recompute

**Who:** GPT and Gemini, each in a fresh chat with no earlier context, from raw per-world numbers only
(`recompute/cu1_one_file.csv`, built from the 96 output JSONs by a short script, not by `analyse_cu1.py`), without the
analysis script. Sent 29 October 2026 (sleep mode).

## GPT (fresh chat https://chatgpt.com/c/6ae2f491-5878-83ea-830e-082bcc72b2dc)

Recorded from its reply:

| measure | analysis | GPT | match |
|---|---|---|---|
| practice spread v / c / x | 0.2974 / 0.3156 / 0.2936 | 0.2974 / 0.3156 / 0.2936 | yes |
| **c − v** | **+0.0182 [+0.0157, +0.0205]** | +0.0182 [0.0157, 0.0205] | yes |
| x − v | −0.0038 [−0.0077, −0.0003] | −0.0038 [−0.0077, −0.0003] | yes |
| rule | supports | supports | yes |
| extinct v / c / x | 2 / 1 / 3 | 2 / 1 / 3 | yes |
| population v / c / x (ratio c/v) | 129.6 / 132.8 / 124.0 (1.025) | 129.5822 / 132.7596 / 123.9835 (1.0245) | yes |
| flags | none | none | yes |
| making per adult-year v / c, c − v | 0.0483 / 0.0758, +0.0275 [+0.0227, +0.0320] | 0.0483 / 0.0758, +0.0275 [0.0227, 0.0320] | yes |
| make share practised v / c | 0.0550 / 0.0828 | 0.0550 / 0.0828 | yes |

## Gemini

Pending (fresh chat https://gemini.google.com/app/4b0f081f500eb796). Recorded only from its actual reply.
