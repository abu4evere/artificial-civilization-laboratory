# PB2: independent blind recompute (5 November 2026, 05:29)

**The inputs:**
- `recompute/pb2_counts.csv`, built by `recompute/build_pb2_counts.py`, which was written before data;
- `recompute/prompt.txt`.

Each was given in a fresh chat, with no analysis script and no earlier result.
- GPT: chat 6aec5927, "Medium" thinking, with code.
- Gemini 3.1 Pro: chat 849911e3bedf8754, with code. A first fresh Gemini chat (617f11510960aac1) declined with "I'm
  having a hard time fulfilling your request", so the same text was sent to a new chat.
- DeepSeek: chat 105c2492, DeepThink, no code tool. Still working by hand when this was written; its reply will be
  appended.

**The numbers below are read from the replies.** The time in the title is from the clock.

| quantity | the study | GPT (code) | Gemini 3.1 Pro (code) |
|---|---|---|---|
| M3: c, P, G, G0, x | 0.0034, 0.0210, 0.0203, 0.0200, 0.0035 | 0.0034, 0.0210, 0.0203, 0.0200, 0.0035 | 0.0034, 0.0210, 0.0203, 0.0200, 0.0035 |
| G − P [95%] | −0.0007 [−0.0020, +0.0005] | −0.000728 [−0.001992, +0.000539] | −0.0007 [−0.0020, 0.0005] |
| G − G0 [95%] | +0.0002 [−0.0009, +0.0013] | +0.000241 [−0.000851, +0.001312] | 0.0002 [−0.0009, 0.0013] |
| P − c [95%] | +0.0176 [+0.0157, +0.0194] | +0.017606 [+0.015726, +0.019370] | 0.0176 [0.0156, 0.0194] |
| living-weeks P / c | 1.283 [1.236, 1.335] | 1.2830 [1.2348, 1.3344] | 1.2830 [1.2348, 1.3327] |
| living-weeks G / c | 1.263 [1.211, 1.320] | 1.2629 [1.2081, 1.3190] | 1.2629 [1.2082, 1.3201] |
| living-weeks G0 / c | 1.295 [1.246, 1.350] | 1.2950 [1.2466, 1.3504] | 1.2950 [1.2464, 1.3512] |
| extra extinct worlds (P, G, G0) | 0, 0, 0 | 0, 0, 0 | 0, 0, 0 |
| MSE memory; MSE habit | 0.0027; 0.8021 | 0.002664; 0.802133 | 0.0027; 0.8021 |
| habit − memory [95%] | +0.7995 [+0.7759, +0.8215] | +0.799469 [+0.775361, +0.822136] | 0.7995 [0.7759, 0.8218] |
| reading | not shown (guards none; validity passes; G − P and G − G0 not above 0) | NOT SUPPORTED | not supported |

**Both agree with the study.**
- The point values match to 4 decimals.
- The intervals differ only in the last digit, from different bootstrap random streams. GPT used seed 20261105; the
  study used 20261114.
- GPT added, unasked, that the results support the narrower finding that memory steering (P) improves M3 over the
  baseline with no guard raised. That is the study's reported steering effect.

PB2's frozen reading stands: **the self-chosen goal is not shown to help** (G − P and G − G0 null). The steering effect
P − c, +0.0176 [0.0157, 0.0194], is confirmed. PB2 is final.

## Appended at 05:42 (5 November 2026): DeepSeek's reply
DeepSeek (DeepThink, chat 105c2492, no code tool) hit its length limit while working by hand. "Continue" was pressed
once, and it then gave a final answer. **Read from its reply:**
- M3: c 0.0034, P 0.0210, G 0.0203, G0 0.0200, x 0.0035;
- G − P −0.000728 [−0.00203, 0.00057];
- G − G0 0.000241 [−0.00084, 0.00132];
- P − c 0.017606 [0.01575, 0.01946];
- living-weeks: P / c 1.283 [1.233, 1.332], G / c 1.263 [1.208, 1.318], G0 / c 1.295 [1.243, 1.347]; no extinctions;
  no guard;
- MSE memory 0.002664, MSE habit 0.802133, difference 0.799469 [0.7764, 0.8225]: passes;
- reading: "Not supported".

**DeepSeek agrees with the study and with GPT and Gemini.** All three match.
