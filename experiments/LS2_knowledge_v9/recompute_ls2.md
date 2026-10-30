# LS2 — Independent recompute (30 October 2026)

**Who:** GPT and Gemini, each in a fresh chat with no earlier context. GPT:
https://chatgpt.com/c/6ae46bac-bb50-83ea-ba36-6fb8d8e1123c. Gemini: https://gemini.google.com/app/f902c6b39d589367
(Gemini first said it could not read the attached file; asked again to load it with code, it did).
**What they saw:** `recompute/ls2_one_file.csv` (raw per-world sums of the ledger's counters, built from the 40 output
JSONs by `recompute/build_one_file.py`, which computes no ratio, share or interval) and `recompute/prompt.txt`.
**Not** the analysis script, `results.md` or the findings. Recorded from their replies.

| measure | analysis (`analyse_ls2.py`) | GPT | Gemini | match |
|---|---|---|---|---|
| worlds alive at year 100 | 40 | 40 | 40 | yes |
| Q1 copy loss: death share | 0.980 [0.978, 0.982] | 0.9802 [0.9785, 0.9819] | 0.9802 [0.9784, 0.9819] | yes |
| Q1 copy loss: push-out; useless | 0.020; 0 | 0.0198; 0 | 0.0198; 0 | yes |
| Q1 copy-loss events | 487,257 | 487,257 | 487,257 | yes |
| Q1 kind extinction: death share | 0.979 [0.976, 0.981] | 0.9790 [0.9764, 0.9814] | 0.9790 [0.9764, 0.9813] | yes |
| Q1 kind-extinction events | 50,086 | 50,086 | 50,086 | yes |
| Q3 Δ ln feasible / weighed / chosen | +0.765 / +0.387 / −2.887 | +0.7651 / +0.3867 / −2.8875 | +0.7651 / +0.3867 / −2.8875 | yes |
| Q3 total | −1.736 | −1.7357 | −1.7357 | yes |
| Q3 share of "chosen given weighed" | 1.66 [1.62, 1.72] | 1.6636 [1.6174, 1.7162] | 1.6636 [1.6190, 1.7164] | yes |
| Q3 largest gate | chosen given weighed | T3 | T3 | yes |
| Q5 inheritance, born 0–50 (people) | 0.391 [0.385, 0.398] (6,057) | 0.3914 [0.3844, 0.3979] (6,057) | 0.3914 [0.3847, 0.3981] (6,057) | yes |
| Q5 born 50–100 | 0.317 [0.307, 0.328] (5,399) | 0.3172 [0.3071, 0.3274] | 0.3172 [0.3071, 0.3272] | yes |
| Q5 born 100–150 | 0.293 [0.281, 0.306] (5,342) | 0.2933 [0.2813, 0.3054] | 0.2933 [0.2812, 0.3056] | yes |
| Q5 pooled, born year 100 on | 138,544 / 529,328 = 0.262 (checked separately) | 0.2617 [0.2555, 0.2682]; 72,551 people | 0.2617 [0.2555, 0.2683]; 72,551 people | yes, exactly |

Bootstrap intervals differ only in the third or fourth decimal, as expected from different random draws.

**Verdict:** every key number and the dominant channels agree across the analysis, GPT and Gemini. The findings are
final.
