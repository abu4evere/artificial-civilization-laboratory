# CI1: independent blind recompute (6 November 2026, 16:29)

**The inputs:**
- `recompute/ci1_counts.csv` (160 rows: 5 arms × 32 seeds), built by `recompute/build_ci1_counts.py`, which was written
  before data;
- `recompute/prompt.txt`, also written before data.

Each was given in a fresh chat, with no analysis script and no earlier result. The prompt was sent at about 16:2x;
the clock read 16:26 when Gemini's reply was saved.
- **GPT:** chat 6aee4580, "Medium" thinking, with code ("Analyzed"; 10,000 paired-world bootstrap resamples).
- **Gemini** (Pro, "High"): chat c8403253ce4934c7, with code ("Show code").
- **DeepSeek:** chat fc094f1c, no code tool.

**The numbers below are read from the replies.** The time in the title is from the clock.

| quantity | the study | GPT (code) | Gemini (code) |
|---|---|---|---|
| LG starvation ratio | 0.9486 [0.7925, 1.1245] | 0.9486 [0.7879, 1.1275] | 0.9486 [0.7948, 1.1305] |
| LG killing difference | +0.0096 [−0.0038, +0.0274] | 0.0096 [−0.0047, 0.0267] | 0.0096 [−0.0034, 0.0279] |
| LG adult health difference | +0.5176 [−0.2041, +1.3070] | 0.5176 [−0.2129, 1.3206] | 0.5176 [−0.2069, 1.3205] |
| LG living-weeks ratio | 1.0553 [0.9414, 1.1924] | 1.0553 [0.9422, 1.1878] | 1.0553 [0.9416, 1.1870] |
| LG child deaths ratio | 1.0005 [0.8183, 1.2137] | 1.0005 [0.8166, 1.2119] | 1.0005 [0.8207, 1.2117] |
| LG child starvation ratio | 0.9378 [0.7130, 1.2223] | 0.9378 [0.7030, 1.2286] | 0.9378 [0.7097, 1.2259] |
| LG gifts to kin's children ratio | 1.1073 [1.0292, 1.2016] | 1.1073 [1.0287, 1.2008] | 1.1073 [1.0290, 1.1979] |
| **LG co-primary difference** | **+0.0183 [+0.0125, +0.0239]** | 0.0183 [0.0125, 0.0239] | 0.0183 [0.0125, 0.0239] |
| IN starvation ratio | 1.0898 [0.9353, 1.2440] | 1.0898 [0.9323, 1.2459] | 1.0898 [0.9362, 1.2470] |
| IN killing difference | +0.0069 [−0.0031, +0.0174] | 0.0069 [−0.0031, 0.0174] | 0.0069 [−0.0030, 0.0172] |
| IN adult health difference | −0.3378 [−1.0190, +0.3658] | −0.3378 [−1.0224, 0.3755] | −0.3378 [−1.0112, 0.3597] |
| IN living-weeks ratio | 1.0870 [0.9687, 1.2148] | 1.0870 [0.9722, 1.2106] | 1.0870 [0.9705, 1.2121] |
| IN child deaths ratio | 1.0248 [0.8371, 1.2570] | 1.0248 [0.8367, 1.2514] | 1.0248 [0.8366, 1.2504] |
| IN child starvation ratio | 0.9841 [0.7692, 1.2456] | 0.9841 [0.7703, 1.2406] | 0.9841 [0.7693, 1.2367] |
| IN gifts ratio | 1.0852 [1.0218, 1.1534] | 1.0852 [1.0207, 1.1536] | 1.0852 [1.0215, 1.1503] |
| **IN co-primary difference** | **+0.0033 [−0.0004, +0.0068]** | 0.0033 [−0.0004, 0.0067] | 0.0033 [−0.0004, 0.0068] |
| LG+IN starvation ratio | 1.1331 [0.9396, 1.3550] | 1.1331 [0.9405, 1.3600] | 1.1331 [0.9466, 1.3533] |
| LG+IN killing difference | +0.0043 [−0.0055, +0.0129] | 0.0043 [−0.0055, 0.0129] | 0.0043 [−0.0054, 0.0128] |
| LG+IN adult health difference | −0.7270 [−1.6139, +0.2006] | −0.7270 [−1.6181, 0.2017] | −0.7270 [−1.6115, 0.2035] |
| LG+IN living-weeks ratio | 1.1270 [1.0218, 1.2535] | 1.1270 [1.0230, 1.2495] | 1.1270 [1.0220, 1.2504] |
| LG+IN child deaths ratio | 1.1029 [0.9042, 1.3631] | 1.1029 [0.8988, 1.3605] | 1.1029 [0.9005, 1.3607] |
| LG+IN child starvation ratio | 1.0359 [0.8085, 1.3513] | 1.0359 [0.8053, 1.3550] | 1.0359 [0.8079, 1.3522] |
| LG+IN gifts ratio | 1.0912 [1.0055, 1.1860] | 1.0912 [1.0046, 1.1854] | 1.0912 [1.0043, 1.1842] |
| **LG+IN co-primary difference** | **+0.0192 [+0.0139, +0.0251]** | 0.0192 [0.0140, 0.0250] | 0.0192 [0.0139, 0.0250] |
| sham co-primary difference | −0.0019 [−0.0047, +0.0011] | −0.0019 [−0.0047, 0.0011] | −0.0019 [−0.0046, 0.0011] |
| extinct worlds (v14, LG, IN, LG+IN, sham) | 0, 1, 1, 1, 2 | 0, 1, 1, 1, 2 | +1 for each of LG, IN, LG+IN |
| guards raised | none | none | none |
| readings LG; IN; LG+IN | supported; no harm, no effect; supported | the same | the same |

GPT also gave the shares: v14 0.4227%, LG 2.2479%, IN 0.7498%, LG+IN 2.3440%, sham 0.2349%. These are 12/2,839,
70/3,114, 27/3,601, 86/3,669 and 7/2,980.

**DeepSeek gave no numbers in its reply.** It wrote that it had no code tool, so it could not "honestly report" the
intervals "without fabricating them", and it gave a Python script instead. Its visible working before that reply
summed the file by hand. The same pooled sums appear there: v14 kinds 2,839 and complete 12; LG 3,114 and 70; IN
3,601 and 27; LG+IN 3,669 and 86; the sham 2,980 and 7. It also gave starvation ratios of 0.9486 (LG), 1.0898 (IN) and
1.133 (LG+IN). These figures come from its working, not its reply. They are recorded as such and are not counted as a
recompute.

**GPT and Gemini agree with the study, each with code.**
- Every point estimate matches to 4 decimals.
- Their intervals differ from the study's only in the third or fourth decimal, which is bootstrap noise.
- Every reading is the same.

CI1's readings stand: **LG supported, IN no harm and no effect, LG+IN supported.** The findings are final.
