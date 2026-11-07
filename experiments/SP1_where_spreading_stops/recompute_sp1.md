# SP1: independent blind recompute (7 November 2026, 04:39)

**The inputs:**
- `recompute/sp1_counts.csv` (32 rows, one per world), built by `recompute/build_sp1_counts.py`, written before data
  by the Telegram session;
- `recompute/prompt.txt`, also written before data.

Each was given in a fresh chat, with no analysis script and no earlier result.
- **GPT:** chat 6aeef140, "Medium" thinking, with code (pandas and NumPy; its own bootstrap seed 20261107).
- **Gemini:** chat e3425aeb18623dba, with code ("Show code").
- **DeepSeek:** chat d3401264, no code tool. At 04:39 it was still working the percentiles by hand (screenshot of its
  working). No finished reply was read, and none is counted.

**The numbers below are read from the replies.** The time in the title is from the clock.

| quantity | the study | GPT (code) | Gemini (code) |
|---|---|---|---|
| totals: born, offered, shown | 3,597; 1,245; 1,196 | the same | the same |
| learned_taught, learned_social, had parts, made | 74; 74; 8; 1 | the same | the same |
| lessons shown, declined, missing part, taken | 28,897; 23,031; 5,547; 89 | the same | the same |
| offered ∣ born | 0.3461 [0.3299, 0.3625] | 0.3461 [0.3299, 0.3625] | 0.3461 [0.3304, 0.3628] |
| shown ∣ offered | 0.9606 [0.9502, 0.9708] | 0.9606 [0.9503, 0.9705] | 0.9606 [0.9502, 0.9705] |
| **learned through a lesson ∣ shown** | **0.0619 [0.0452, 0.0805]** | 0.0619 [0.0454, 0.0807] | 0.0619 [0.0450, 0.0809] |
| had parts ∣ learned | 0.1081 [0.0429, 0.1795] | 0.1081 [0.0423, 0.1803] | 0.1081 [0.0428, 0.1800] |
| made ∣ had parts | 0.1250 [0.0000, 0.3333] | 0.1250 [0.0000, 0.3333] | 0.1250 [0.0000, 0.3333] |
| lowest step; overlaps | learned ∣ shown; overlaps the last two | the same | the same (as read) |
| declined ÷ shown | 0.797 | 0.7970 [0.7875, 0.8063] | 0.7970 [0.7872, 0.8060] |
| missing part ÷ shown | 0.192 | 0.1920 [0.1825, 0.2017] | 0.1920 [0.1825, 0.2019] |
| taken ÷ shown | 0.003 | 0.0031 [0.0021, 0.0043] | (not read) |

GPT also noted that 3 of its 10,000 draws had no learner with the parts, and it left them out of the last ratio. It
added that the three outcome shares sum to 0.992, not 1. The counts file has no column for lessons already known or
taken with a copying error, which the study reports apart (0.006 and 0.002).

**GPT and Gemini agree with the study in every total and point estimate,** each with code. Their intervals differ in
the fourth decimal. SP1's reading stands: spreading stops at the lesson, with the last two steps overlapping. The
findings are final.
