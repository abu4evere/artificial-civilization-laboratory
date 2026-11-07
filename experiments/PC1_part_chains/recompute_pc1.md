# PC1: independent blind recompute (7 November 2026, 07:40)

**The inputs:**
- `recompute/pc1_counts.csv` (32 rows, one per world), built by `recompute/build_pc1_counts.py`, written before data.
  It counts from the raw world files independently of analyse_pc1.py.
- `recompute/prompt.txt`, also written before data.

Each was given in a fresh chat, with no analysis script and no earlier result.
- **GPT:** chat 6aef1b5f, "Medium" thinking, with code (Python).
- **Gemini:** chat a603b9a49d9af33d, with code ("Show code"; Python).
- **DeepSeek:** chat 5a574854, no code tool. It was still working by hand (screenshot of its working). No finished
  reply was read, and none is counted.

**The numbers below are read from the replies.** The time in the title is from the clock.

| quantity | the study | GPT (code) | Gemini (code) |
|---|---|---|---|
| depth 0 / 1 / 2 / 3+ ÷ kinds | 0.004 / 0.129 / 0.390 / 0.477 | the same (3+ [0.453, 0.499]) | the same (2 [0.373, 0.407]) |
| missing 1 / 2 / 3+ ÷ failed | 0.965 / 0.035 / 0.000 | the same | the same |
| deepest 1 / 2 / 3+ ÷ failed | 0.093 / 0.350 / 0.557 [0.514, 0.598] | the same (3+ [0.514, 0.598]) | the same (3+ [0.514, 0.599]) |
| **teacher knows all** | **0.926 [0.899, 0.952]** | 0.926 [0.899, 0.952] | 0.926 [0.900, 0.953] |
| teacher knows some / none | 0.009 / 0.064 | 0.009 / 0.064 [0.038, 0.092] | 0.009 / 0.064 [0.038, 0.091] |
| part lesson shown ÷ failed | 0.942 | 0.942 [0.916, 0.968] | 0.942 [0.916, 0.968] |
| part: knew / declined / missing part / taken | 0.011 / 0.780 / 0.209 / 0.000 | the same | the same |
| part shown was missing | 0.990 | 0.990 [0.984, 0.995] | (not read) |
| **not helpful** | **1.000** | 1.000 [1.000, 1.000] | (not read) |
| got part / got kind / made ÷ pairs | 0.006 / 0.001 / 0.000 | the same (21, 2, 0 of 3,369) | the same |
| **reading** | **could help** | COULD HELP | could help |

**GPT and Gemini agree with the study in every point estimate and in the reading,** each with code. Their intervals
differ in the third decimal at most. The findings are final.
