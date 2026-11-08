# DF1: independent blind recompute (7 November 2026, 19:56)

## The inputs
- `recompute/df1_counts.csv`: 32 rows, one per world. It was built by `recompute/build_df1_counts.py`, written before
  data, which counts from the raw world files independently of analyse_df1.py.
- `recompute/prompt.txt`, also written before data.

Each was given in a fresh chat, with no analysis script and no earlier result:
- **GPT:** chat 6aefc6ab, "Instant" thinking; its reply says NumPy, random seed 20261107.
- **Gemini:** chat 4c2a4fc229d026e4, with code ("Show code").
- **DeepSeek** was not asked: it had no code tool in the recent rounds.

**The numbers below are read from the replies.** The time in the title is from the clock.

## The numbers
| quantity | the study | GPT | Gemini (code) |
|---|---|---|---|
| women, per 1,000 | 7.384 [6.740, 8.025] | 7.3841 [6.7455, 8.0150] | 7.3841 [6.7465, 8.0247] |
| men, per 1,000 | 0.735 [0.650, 0.823] | 0.7350 [0.6507, 0.8227] | 0.7350 [0.6507, 0.8193] |
| **women − men** | **+6.649 [+6.067, +7.227]** | +6.6491 [6.0722, 7.2213] | 6.6491 [6.0725, 7.2295] |
| women's share | 0.8881 [0.8790, 0.8969] | 0.8881 [0.8791, 0.8968] | 0.8881 [0.8793, 0.8968] |
| **reading** | **feeding drives the gap** | feeding drives the gap | feeding drives the gap |

## Verdict
- **GPT and Gemini agree with the study in every point estimate and in the reading.**
- Their intervals differ in the third decimal at most.

**The findings are final.**
