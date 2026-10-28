# LR1 — independent recompute

**Who:** GPT and Gemini, each in a fresh chat with no earlier context, from raw per-world numbers only
(`recompute/lr1_one_file.csv`, built from the 96 output JSONs by a short script, not by `analyse_lr1.py`), without the
analysis script. Sent 28 October 2026.

Note on years: the file's years are census indices; index 199 is the end of year 200 and index 999 the end of year
1,000, as in the analysis; "years 800–999" is the analysis's years 800–1,000.

## GPT (fresh chat https://chatgpt.com/c/6ae21b78-0960-83ea-97fe-3ff5b43b06d6)

Recorded from its reply:

| measure | analysis | GPT | match |
|---|---|---|---|
| v8 ground, year 200 / 1,000 | 122.3 / 77.6 | 122.2813 / 77.5938 | yes |
| sham ground, year 200 / 1,000 | 108.2 / 75.2 | 108.2500 / 75.1875 | yes |
| v8 ratio 1,000 ÷ 200 | 0.63 | 0.6346 | yes |
| slope, years 800–1,000 | +0.003 [−0.001, +0.008] | 0.0034 [−0.0005, 0.0084] | yes |
| population v8 ÷ v7 | 0.988 [0.702, 1.406] | 0.9882 [0.7024, 1.4061] | yes |
| population sham ÷ v7 | 1.016 [0.771, 1.292] | 1.0158 [0.7712, 1.2915] | yes |
| extinct v7 / v8 / sham | 8 / 8 / 10 | 8 / 8 / 10 | yes |
| flags A / B | not raised / not raised | no / no | yes |

## Gemini

Pending (fresh chat https://gemini.google.com/app/78a7758f88a1e1fd). Recorded only from its actual reply.
