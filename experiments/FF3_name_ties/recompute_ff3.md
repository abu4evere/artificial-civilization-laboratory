# FF3: independent blind recompute (6 November 2026, 03:58)

**The inputs:**
- `recompute/ff3_counts.csv` (96 rows: 3 arms × 32 seeds), built by `recompute/build_ff3_counts.py`, which was written
  before data;
- `recompute/prompt.txt`.

Each was given in a fresh chat, with no analysis script and no earlier result.
- GPT: chat 6aed8f5a, "Medium" thinking, with code (Python, 10,000 paired-world bootstrap resamples).
- DeepSeek: chat 0c463f1e, no code tool.
- Gemini 3.1 Pro: a first chat (d25aaaabe0994ce2) stalled for about 25 minutes, and on reload its reply was gone. A
  fresh chat was asked at 03:5x. Its reply will be appended if it comes.

**The numbers below are read from the replies.** The time in the title is from the clock.

| quantity | the study | GPT (code) | DeepSeek (no code) |
|---|---|---|---|
| living-weeks f / c | 0.9636 [0.8506, 1.0867] | 0.9636 [0.8532, 1.0873] | 0.96358 [0.848, 1.079]* |
| living-weeks x / c | 0.9576 [0.8526, 1.0747] | 0.9576 [0.8549, 1.0771] | 0.95763 [0.849, 1.066]* |
| extinct c, f, x; f − c | 1, 2, 2; +1 | 1, 2, 2; +1 [0, 3] | 1, 2, 2; +1 |
| tie share of recipe evictions c, f, x | (described) 11,310/17,646, 9,691/20,193, 11,282/17,634 | 0.6409, 0.4799, 0.6398 | 0.64094, 0.47992, 0.63979 |
| tie-share ratio f / c | 0.749 [0.687, 0.822] | 0.7488 [0.6862, 0.8211] | 0.74878 (interval approximate)* |
| reading | no harm | no harm | no harm |

\* DeepSeek's intervals are approximations. Asked in the same chat, it wrote that it "did not actually run a 10,000-draw
paired bootstrap" and that the intervals "should be labeled as approximate".

**GPT and DeepSeek agree with the study.** Every point estimate matches, and GPT's intervals differ only in the third
decimal. FF3's reading stands: **no harm.** The findings are final.

**On the "03:5x" above:** the fresh Gemini chat was sent after the 03:54 heartbeat and before this file's time,
03:58; its exact minute was not read from the clock.
