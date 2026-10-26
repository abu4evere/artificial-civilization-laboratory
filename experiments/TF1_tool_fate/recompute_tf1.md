# TF1 — Independent recompute (27 October 2026)

**Who:** GPT and Gemini, each in a fresh chat with no earlier context.
**What they saw:** the raw rows of all 32 worlds and a field dictionary, nothing recomputed or summarised. **Not** the
analysis script, `results.md` or the findings.
- `tf1_tools.csv` has one row per forage tool, with its fate, uses left, and moves between hands.
- `tf1_bins.csv` has the counters used.
- GPT got them zipped. Gemini got them as CSV files (the tools file split in two by seed, under the 10 MB upload limit).

| measure | analysis | GPT | Gemini | match |
|---|---|---|---|---|
| seeds | 32 | 32 | 32 | yes |
| T1 forage-tool ends (not still held) | 248,694 | 248,694 | 248,694 | yes |
| worn out | 0.576 [0.568, 0.584] | 0.5764 [0.5680, 0.5843] | 0.5764 [0.5679, 0.5845] | yes |
| used in making; deleted at the limit; unknown; lost at death | 0.388; 0.034; 0.001; 0.0003 | 0.3884; 0.0336; 0.0013; 0.0003 | 0.3884; 0.0336; 0.0013; 0.0003 | yes |
| T2 forage tools among carry-limit deletions | 0.784 [0.757, 0.81] (10,666) | 0.7842 [0.7578, 0.8108] | 0.7842 [0.7576, 0.8106] | yes |
| T3 tools whose holder died | 5,188 | 5,188 | 5,188 | yes |
| inherited / taken from body / with body at end / lost at death | 0.044 / 0.227 / 0.712 / 0.016 | 0.0439 / 0.2273 / 0.7124 / 0.0164 | 0.0439 / 0.2273 / 0.7124 / 0.0164 | yes |
| inherited interval | [0.038, 0.050] | [0.0377, 0.0500] | [0.0378, 0.0501] | yes |
| T4 child no tool while carer holds one, all bins | 0.421 [0.400, 0.441] | 0.4208 [0.4006, 0.4401] | 0.4208 [0.3997, 0.4402] | yes |
| years 5–10; years 100–200 | 0.031; 0.740 | 0.0312; 0.7405 | 0.0312; 0.7405 | yes |

**Council note:** Gemini's first intervals for T2 and T4 were too narrow, because it resampled rows rather than worlds.
Asked how it resampled, it said so, reran with whole-world resampling, and matched (above). The point estimates were
identical from the start.

**Verdict:** every key number agrees across the analysis, GPT and Gemini. The findings are final.
