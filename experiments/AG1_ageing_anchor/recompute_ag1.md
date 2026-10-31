# AG1 — Independent recompute (31 October 2026, just after midnight)

**Who:** GPT and Gemini, each in a fresh chat with no earlier context. GPT:
https://chatgpt.com/c/6ae563aa-88a8-83ea-a2d8-aa208b98c91f. Gemini: https://gemini.google.com/app/9b86fe1aa9e35539.
**What they saw:** `recompute/ag1_one_file.csv` (raw per-world counts: deaths and person-years in three age bands,
years 100–999; extinct; living person-years in years 800–999; built by `recompute/build_one_file.py`, which computes no
rate, distance or interval) and `recompute/prompt.txt`. **Not** the analysis script, `results.md` or the findings.
Recorded from their replies.

| measure | analysis (`analyse_ag1.py`) | GPT | Gemini | match |
|---|---|---|---|---|
| rates v (30–45 / 45–60 / 60–70) | 0.0298 / 0.0762 / 0.2015 | same | same | yes |
| rates b | 0.0166 / 0.0284 / 0.0705 | same | same | yes |
| rates a | 0.0134 / 0.0209 / 0.0492 | same | same | yes |
| rates x | 0.0304 / 0.0760 / 0.2038 | same | same | yes |
| D v / b / a / x | 0.9952 / 0.1246 / 0.1723 / 1.0045 | same | same | yes |
| D(b) − D(v) | −0.8707 [−0.8799, −0.8234] | −0.8707 [−0.8799, −0.8234] | −0.8707 [−0.8800, −0.8251] | yes |
| D(a) − D(v) | −0.8229 [−0.9057, −0.7456] | −0.8229 [−0.9057, −0.7456] | −0.8229 [−0.9053, −0.7466] | yes |
| D(x) − D(v) | +0.0092 [−0.0171, +0.0356] | +0.0092 [−0.0171, +0.0356] | +0.0092 [−0.0176, +0.0352] | yes |
| reading b / a | more realistic / more realistic | same | same | yes |
| extinct v / b / a; flag | 2 / 1 / 5; a flagged (+3) | same | same | yes |
| living person-years 800–999, arm ÷ v | b 1.034, a 0.774 (a flagged) | b 1.0335, a 0.7738 | b 1.0335, a 0.7738 | yes |

GPT's intervals are identical to the analysis's to four decimals. GPT reports it used generator seed 20261030 (today's
date), the same seed the frozen analysis uses, with the same resampling; it never saw the script. Gemini's differ in
the fourth decimal, as expected from different random draws.

**Verdict:** every key number, both readings and both flags agree across the analysis, GPT and Gemini. The findings
are final.
