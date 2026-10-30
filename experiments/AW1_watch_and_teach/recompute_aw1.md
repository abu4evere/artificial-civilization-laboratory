# AW1 — Independent recompute (30 October 2026)

**Who:** GPT and Gemini, each in a fresh chat with no earlier context. GPT:
https://chatgpt.com/c/6ae5006e-8744-83ea-9941-87c0dc163894. Gemini: https://gemini.google.com/app/82e59ce2bfe28b2d.
**What they saw:** `recompute/aw1_one_file.csv` (raw per-world sums over years 100–199, built by
`recompute/build_one_file.py`, which computes no ratio, share or interval) and `recompute/prompt.txt`. **Not** the
analysis script, `results.md` or the findings. Recorded from their replies.

| measure | analysis (`analyse_aw1.py`) | GPT | Gemini | match |
|---|---|---|---|---|
| making per adult-year v / w / t / x | 0.0763 / 0.0754 / 0.0832 / 0.0798 | same | same | yes |
| w − v | −0.0009 [−0.0085, +0.0066] | −0.0009 [−0.0084, 0.0064] | −0.0009 [−0.0082, 0.0063] | yes |
| t − v | +0.0069 [−0.0007, +0.0146] | 0.0069 [−0.0004, 0.0145] | 0.0069 [−0.0003, 0.0147] | yes |
| x − v | +0.0035 [−0.0026, +0.0095] | 0.0035 [−0.0026, 0.0094] | 0.0035 [−0.0027, 0.0096] | yes |
| reading w / t | not supported / not supported | not supported / not supported | not supported / not supported | yes |
| extinct v / w / t / x | 1 / 0 / 0 / 3 | 1 / 0 / 0 / 3 | 1 / 0 / 0 (x not asked) | yes |
| population w ÷ v, t ÷ v | 1.010, 0.962 | 1.0098, 0.9624 | 1.0098, 0.9624 | yes |
| skill v / w / t / x | 0.2616 / 0.2714 / 0.4854 / 0.2749 | 0.2616 / 0.2714 / 0.4854 / 0.2749 | same | yes |
| skill t − v | +0.2238 [+0.1911, +0.2579] | 0.2238 [0.1915, 0.2574] | 0.2238 [0.1918, 0.2580] | yes |

Bootstrap intervals differ only in the fourth decimal, as expected from different random draws.

**Verdict:** every key number and both readings agree. The findings are final.
