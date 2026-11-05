# HE1: independent blind recompute (5 November 2026, 17:42)

**The inputs:**
- `recompute/he1_counts.csv`, built by `recompute/build_he1_counts.py`, which was written before data;
- `recompute/prompt.txt`.

Each was given in a fresh chat, with no analysis script and no earlier result.
- GPT: chat 6aed05bf, "Medium" thinking, with code.
- Gemini 3.1 Pro: chat 67ba3f6dfccd3b91, with code.
- DeepSeek: chat dbb06321, DeepThink, no code tool. Its reply will be appended.

**The numbers below are read from the replies.** The time in the title is from the clock.

| quantity | the study | GPT (code) | Gemini 3.1 Pro (code) |
|---|---|---|---|
| living-weeks h / c | 1.329 [1.222, 1.447] | 1.3291 [1.2215, 1.4483] | 1.3291 [1.2258, 1.4444] |
| extra extinct | +0 | 0 | 0 |
| starvation per 1,000 living-years, c / h | 4.647 / 7.637 | 4.6471 / 7.6371 | 4.6471 / 7.6371 |
| starvation ratio h / c | 1.643 [1.467, 1.842] | 1.6434 [1.4706, 1.8391] | 1.6434 [1.4687, 1.8421] |
| health c / h; difference | 93.08 / 91.50; −1.58 [−2.39, −0.81] | 93.0757 / 91.4959; −1.5798 [−2.3740, −0.8042] | (read: the guard not raised) |
| M3 c / h; h − c | 0.0036 / 0.0257; +0.0221 [+0.0209, +0.0233] | 0.003631 / 0.025744; +0.022113 [+0.020955, +0.023324] | h − c +0.022113 [0.020935, 0.023329] |
| makes per adult-year c / h; ratio | 0.0631 / 0.3827; 6.065 [5.490, 6.643] | 0.063093 / 0.382654; 6.0649 [5.5029, 6.6146] | 0.0631 / 0.3827; 6.0649 [5.4853, 6.6233] |
| guards | hunger raised | starvation raised; the others not | starvation raised; the others not |
| reading | not supported | not supported (a harm guard raised) | not supported |

**Both agree with the study.** The intervals differ only in the last digit, from different bootstrap streams. HE1's
reading stands: **not supported**. The hunger guard is raised, so the law is not adopted.

## Appended at 17:46 (5 November 2026): DeepSeek's reply
DeepSeek (DeepThink, chat dbb06321, no code tool) wrote: "I can't execute the bootstrap in this chat interface, so I
won't invent percentile intervals". It then gave the pooled sums and exact point estimates, and a Python script for
the bootstrap, which was not run here.

**Read from its reply:**
- living-weeks ratio 1.32909;
- extra extinct 0;
- starvation per 1,000 living-years 4.64708 (c) and 7.63708 (h), ratio 1.64342;
- adults' mean health (c) 93.07567;
- pooled sums such as m3_g_made 3,036 and 33,756, and makes 16,877 and 131,807.

**Every point matches the study.** No intervals are claimed, as is right. It is an honest partial recompute.
