# RF1: independent blind recompute (6 November 2026, 01:06)

**The inputs:**
- `recompute/rf1_kinds.csv` (1,246 rows, one per new kind), built by `recompute/build_rf1_kinds.py`, which was written
  before data;
- `recompute/prompt.txt`.

Each was given in a fresh chat, with no analysis script and no earlier result.
- GPT: chat 6aed6d18, "Medium" thinking, with code (Python, 10,000 world-bootstrap resamples).
- Gemini 3.1 Pro "High": chat f0304a48047777c1, with code.
- DeepSeek: chat b8ced2aa, no code tool.

**The numbers below are read from the replies.** The time in the title is from the clock.

| quantity | the study | GPT (code) | Gemini 3.1 Pro (code) | DeepSeek (no code) |
|---|---|---|---|---|
| kinds; with wanting_weeks = 0 | 1,246; 1,177 | 1,246; 1,177 | (not stated); 1,177 | 1,249; 1,180 (a counting slip, corrected by DeepSeek to 1,246 and 1,177) |
| kinds with a wanting week | 69 | 69 | (69 implied) | 69 |
| stage counts 1–5 | 2, 12, 2, 53, 0 | 2, 12, 2, 53, 0 | (shares only) | 2, 12, 2, 53, 0 |
| 1. cannot obtain | 0.029 [0.000, 0.074] | 0.0290 [0.0000, 0.0746] | 0.0290 [0.0000, 0.0741] | 0.0290 [0.000, 0.067]* |
| 2. not offered | 0.174 [0.092, 0.271] | 0.1739 [0.0933, 0.2712] | 0.1739 [0.0909, 0.2727] | 0.1739 [0.087, 0.261]* |
| 3. out-competed | 0.029 [0.000, 0.080] | 0.0290 [0.0000, 0.0794] | 0.0290 [0.0000, 0.0784] | 0.0290 [0.000, 0.069]* |
| 4. started, never complete | 0.768 [0.657, 0.857] | 0.7681 [0.6596, 0.8592] | 0.7681 [0.6552, 0.8592] | 0.7681 [0.671, 0.865]* |
| 5. complete | 0.000 | 0.0000 | 0.0000 | 0.0000 |
| inability (1 + 2) | 0.203 [0.122, 0.298] | 0.2029 [0.1224, 0.2973] | 0.2029 [0.1216, 0.3000] | 0.2029 [0.118, 0.288]* |
| pursuit fails (3 + 4) | 0.797 [0.702, 0.878] | 0.7971 [0.7027, 0.8776] | 0.7971 [0.7000, 0.8784] | 0.7971 [0.712, 0.882]* |
| reading | pursuit fails | pursuit fails | pursuit fails | pursuit fails |

\* DeepSeek's intervals are approximations, not a bootstrap. Asked in the same chat, it wrote: "No — I did not actually
run a 10,000-draw world bootstrap. The intervals I reported are approximations". It also explained the 3 extra rows as
"a counting artifact" in the zero-wanting tally, which did not touch the 69 kinds' stage counts.

**GPT and Gemini agree with the study in every number**, the intervals differing only in the third or fourth decimal.
DeepSeek agrees in the stage counts, the shares and the reading; its intervals are labelled approximate. RF1's reading
stands: **pursuit fails.** The findings are final.
