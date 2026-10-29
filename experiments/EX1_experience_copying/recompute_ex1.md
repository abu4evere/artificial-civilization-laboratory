# EX1 — independent recompute

**Who:** GPT and Gemini, each in a fresh chat with no earlier context, from raw per-world numbers only
(`recompute/ex1_one_file.csv`, built from the 96 output JSONs by a short script, not by `analyse_ex1.py`), without the
analysis script. Sent 29 October 2026 (sleep mode).

## GPT (fresh chat https://chatgpt.com/c/6ae2c5ec-5c04-83ea-9a0b-9cc8825ee0dd)

Recorded from its reply:

| measure | analysis | GPT | match |
|---|---|---|---|
| common bias v / e / x | +0.4311 / +0.4375 / +0.4228 | 0.4311 / 0.4375 / 0.4228 | yes |
| **improvement v − e** | **−0.0064 [−0.0184, +0.0049]** | −0.0064 [−0.0184, 0.0050] | yes |
| sham v − x | +0.0082 [−0.0009, +0.0176] | +0.0082 [−0.0008, 0.0179] | yes |
| P | does not support | does not support | yes |
| mean G v / e / x | 0.6760 / 0.6764 / 0.6883 | 0.6760 / 0.6764 / 0.6883 | yes |
| G e − v | +0.0004 [−0.0212, +0.0228] | +0.0004 [−0.0215, 0.0227] | yes |
| H | no harm | no harm | yes |
| extinct v / e / x | 0 / 1 / 0 | 0 / 1 / 0 | yes |
| population v / e (ratio) | 123.7 / 122.7 (0.992) | 123.6913 / 122.7160 (0.9921) | yes |
| flags | none | none | yes |

## Gemini (fresh chat https://gemini.google.com/app/be8acc84405e0f6f)

Recorded from its reply:

| measure | analysis | Gemini | match |
|---|---|---|---|
| common bias v / e / x | +0.4311 / +0.4375 / +0.4228 | 0.4311 / 0.4375 / 0.4228 | yes |
| **improvement v − e** | **−0.0064 [−0.0184, +0.0049]** | −0.0064 [−0.0182, 0.0049] | yes |
| sham v − x | +0.0082 [−0.0009, +0.0176] | 0.0082 [−0.0007, 0.0178] | yes |
| P | does not support | does not support | yes |
| mean G v / e / x | 0.6760 / 0.6764 / 0.6883 | 0.6760 / 0.6764 / 0.6883 | yes |
| G e − v | +0.0004 [−0.0212, +0.0228] | 0.0004 [−0.0214, 0.0232] | yes |
| H | no harm | no harm | yes |
| extinct v / e / x | 0 / 1 / 0 | 0 / 1 / 0 | yes |
| population ratio e / v | 0.992 | 0.9921 | yes |
| flags | none | none | yes |

**Verdict:** every key number and the verdict (not supported; no harm; no flags) agree across the analysis, GPT and
Gemini. The findings are final.
