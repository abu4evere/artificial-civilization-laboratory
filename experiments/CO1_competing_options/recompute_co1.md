# CO1 — Independent recompute (27 October 2026)

**Who:** GPT and Gemini, each in a fresh chat with no earlier context.
**What they saw:** the raw cell rows (`co1_cells.csv`) and family rows (`co1_family.csv`; split in two for Gemini's
upload limit), a field dictionary and the frozen definitions. **Not** the analysis script, `results.md` or the findings.

**How the run went:**
- **GPT:** the first message reached it without the file (a browser upload failed); the file was attached in a second
  message.
- **Gemini:**
  - its code tool failed twice ("something went wrong"; "execution constraints"), so it wrote a script blind;
  - run locally, that script failed with a pandas error. The error was sent back, not fixed by Claude, to keep the code
    Gemini's;
  - Gemini then ran a corrected version itself and reported the numbers below.

| measure | analysis | GPT | Gemini | match |
|---|---|---|---|---|
| seeds; kept states | 32; 24 | 32; 24 | 32; 24 | yes |
| U_other early → late | 1.302 → 1.962 | 1.302211 → 1.961781 | 1.302211 → 1.961781 | yes |
| Δ (D) | +0.660 [0.647, 0.672] | +0.659570 [0.646948, 0.672085] | +0.659570 | yes |
| habit | +0.569 [0.559, 0.577] (0.86) | +0.568627 [0.559188, 0.577127] (86.21%) | +0.568627 (86.21%) | yes |
| multiplicity; per-entry; spread | +0.013; +0.130; −0.052 | +0.012673; +0.129780; −0.051510 | +0.012673; +0.129780; −0.051510 | yes |
| largest part | habit | habit | habit | yes |
| log-odds early → late | −5.41 → −8.62 | −5.405829 → −8.616536 | −5.405829 → −8.616536 | yes |
| swap: entries; habits (share of the fall undone) | 0.02; 0.86 | 2.09%; 86.02% | 2.09%; 86.02% | yes |
| largest family | gather (+0.281) | gather (+0.280793) | gather (+0.280793) | yes |

Gemini's intervals are in its script but were not reported as numbers. GPT's intervals match the analysis.

**Verdict:** every key number agrees across the analysis, GPT and Gemini. The findings are final.
