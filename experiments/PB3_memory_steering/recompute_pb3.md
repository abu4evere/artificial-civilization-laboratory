# PB3: independent blind recompute (5 November 2026, 09:37)

**The inputs:**
- `recompute/pb3_counts.csv`, built by `recompute/build_pb3_counts.py`, which was written before data;
- `recompute/prompt.txt`.

Each was given in a fresh chat, with no analysis script and no earlier result.
- GPT: chat 6aec941f, "Medium" thinking, with code.
- Gemini 3.1 Pro: chat 086de33908161035, with code.
- DeepSeek: chat 36e2aac1, DeepThink, no code tool. Still working when this was written; its reply will be appended.

**The numbers below are read from the replies.** The time in the title is from the clock.

| quantity | the study | GPT (code) | Gemini 3.1 Pro (code) |
|---|---|---|---|
| M3: c, c0, P, Pp, x | 0.0035, 0.0263, 0.0203, 0.0149, 0.0034 | 0.0035, 0.0263, 0.0203, 0.0149, 0.0034 | 0.0035, 0.0263, 0.0203, 0.0149, 0.0034 |
| P − c0 [95%] | −0.0059 [−0.0076, −0.0044] | −0.00595 [−0.00753, −0.00434] | −0.0059 [−0.0076, −0.0044] |
| P − c [95%] | +0.0169 [+0.0146, +0.0193] | +0.01686 [+0.01461, +0.01921] | 0.0169 [0.0146, 0.0192] |
| c0 − c [95%] | +0.0228 [+0.0211, +0.0245] | +0.02281 [+0.02111, +0.02449] | 0.0228 [0.0211, 0.0245] |
| living-weeks c0 / c, extra extinct | 1.166 [1.028, 1.321], +1 | 1.1657 [1.0288, 1.3265], +1 | 1.1657 [1.0291, 1.3244], +1 |
| living-weeks P / c, extra extinct | 1.276 [1.231, 1.325], 0 | 1.2762 [1.2303, 1.3241], 0 | 1.2762 [1.2306, 1.3259], 0 |
| living-weeks Pp / c, extra extinct | 1.306 [1.260, 1.357], 0 | 1.3061 [1.2602, 1.3590], 0 | 1.3061 [1.2600, 1.3572], 0 |
| guards | none | none | none |
| primary reading | myopia, not prediction | **myopia, not prediction** (see the note) | myopia, not prediction |
| co-primary reading | replicates | replicates | replicates |

**A note on GPT's reading, recorded as it happened:**
- GPT's reply opens with a summary line, "Primary: Unclear", and its section 4 starts "Result: unclear".
- In the same section it then applies the frozen rule and writes that the results "actually satisfy myopia, not
  prediction".
- Its final verdict table gives "Myopia, not prediction".

GPT's numbers match exactly. Its final reading agrees with the study, after an internal slip that it corrected
itself.

**GPT and Gemini agree with the study.** The point values match. The intervals differ only in the last digit, from
different bootstrap streams; GPT used seed 20261105, and the study used 20261115. PB3's readings stand:
- **primary: "myopia, not prediction"**;
- **co-primary: "PB2's steering effect replicates"**.

## Appended at 09:43 (5 November 2026): DeepSeek's reply
DeepSeek (DeepThink, chat 36e2aac1, no code tool) stopped once at its length limit. "Continue" was pressed once, and
it then answered. **Read from its reply:**
- M3: c 0.0035, c0 0.0263, P 0.0203, Pp 0.0149;
- P − c0 −0.0059 [−0.0084, −0.0035];
- P − c +0.0169 [0.0146, 0.0191];
- c0 − c +0.0228 [0.0208, 0.0248];
- living-weeks: c0 / c 1.1657 [1.019, 1.313] (+1 extinct); P / c 1.2762 [1.230, 1.323]; Pp / c 1.3061 [1.258, 1.354];
- no guard;
- primary "myopia, not prediction"; co-primary replicates.

**The points and both readings match.** Its intervals are somewhat wider than the study's. Its visible working notes
say it used a normal approximation rather than resampling ("Our intervals based on normal not exact"), so its
intervals are not a true bootstrap. All three models agree with the study's readings.
