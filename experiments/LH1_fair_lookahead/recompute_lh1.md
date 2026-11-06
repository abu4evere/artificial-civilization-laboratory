# LH1: independent blind recompute (5 November 2026, 22:09)

**The inputs:**
- `recompute/lh1_counts.csv` (128 rows: 4 arms × 32 seeds), built by `recompute/build_lh1_counts.py`, which was
  written before data;
- `recompute/prompt.txt`.

Each was given in a fresh chat, with no analysis script and no earlier result.
- GPT: chat 6aed41f0, "Medium" thinking, with code ("Worked for 5m 19s").
- DeepSeek: chat fa0480a4, no code tool. It said so, computed the pooled point estimates by hand, and wrote a script
  blind. The assistant ran that script unchanged (only the indentation, lost in the page copy, was restored):
  `recompute/deepseek_script_lh1.py`, output in `recompute/deepseek_script_lh1_output.txt`.
- Gemini: Flash (chat c25a32b0d672117e) twice said code execution was unavailable and offered a script instead; the
  file was re-attached once. A fresh Gemini 3.1 Pro chat lost its first attempt (the page reset with no reply). The
  second, Gemini 3.1 Pro "High" (chat d406b3ebfe96bf38), ran code and answered; see its section below.

**The numbers below are read from the replies and from that output.** The time in the title is from the clock.

| quantity | the study | GPT (code) | DeepSeek (by hand / its script run here) |
|---|---|---|---|
| e: living-weeks ratio | 1.290 [1.138, 1.465] | 1.2898 [1.1412, 1.4737] | 1.2898 / [1.1409, 1.4671] |
| e: starvation ratio | 1.377 [1.267, 1.496] | 1.3771 [1.2670, 1.4947] | 1.377 / [1.2710, 1.4966] |
| e: killing difference | +0.0352 [+0.0070, +0.0750] | +0.0352 [0.0068, 0.0742] | +0.03525 / [0.0074, 0.0751] |
| e: health difference | −1.36 [−1.91, −0.79] | −1.3595 [−1.9101, −0.7983] | −1.3596 / [−1.9124, −0.8123] |
| e: M3 difference | +0.0082 [+0.0075, +0.0089] | +0.0081850 [0.0074733, 0.0089401] | +0.008185 / [0.0074703, 0.0089578] |
| e: makes ratio | 3.245 [3.022, 3.465] | 3.2448 [3.0183, 3.4694] | 3.2448 / [3.0229, 3.4702] |
| m: living-weeks ratio | 1.316 [1.169, 1.494] | 1.3158 [1.1698, 1.4887] | 1.3158 / [1.1720, 1.4913] |
| m: starvation ratio | 1.750 [1.562, 1.939] | 1.7499 [1.5634, 1.9372] | 1.750 / [1.5685, 1.9367] |
| m: killing difference | +0.1918 [+0.1006, +0.3113] | +0.1918 [0.1001, 0.3127] | +0.19181 / [0.1004, 0.3141] |
| m: health difference | −1.92 [−2.70, −1.18] | −1.9233 [−2.6932, −1.1668] | −1.9233 / [−2.6906, −1.1922] |
| m: M3 difference | +0.0184 [+0.0169, +0.0199] | +0.0184471 [0.0169494, 0.0199380] | +0.018447 / [0.0169387, 0.0199761] |
| m: makes ratio | 5.739 [5.282, 6.167] | 5.7388 [5.3013, 6.1706] | 5.7388 / [5.2899, 6.1666] |
| extra extinct (e, m) | 0, 0 | 0, 0 | 0, 0 |
| guards raised | e: hunger; m: hunger, killing | e: starvation; m: starvation, killing | e: starvation; m: starvation, killing |
| reading | neither supported | neither supported | neither supported |

**GPT and DeepSeek agree with the study.** Every point estimate matches. The intervals differ only in the third or
fourth decimal, from different bootstrap streams. LH1's reading stands: **neither rule is supported.**

## Gemini 3.1 Pro (code, chat d406b3ebfe96bf38), read from its reply
| quantity | e | m |
|---|---|---|
| living-weeks ratio | 1.2898 [1.1376, 1.4688] | 1.3158 [1.1671, 1.4860] |
| extra extinct | 0 | 0 |
| starvation per 1,000 living-years (c 4.5172) | 6.2206; ratio 1.3771 [1.2669, 1.4960] | 7.9046; ratio 1.7499 [1.5680, 1.9381] |
| killing per 1,000 living-years (c 0.0045) | 0.0397; difference 0.0352 [0.0076, 0.0744] | 0.1963; difference 0.1918 [0.1004, 0.3079] |
| health (c 93.0942) | 91.7346; difference −1.3595 [−1.9047, −0.7860] | 91.1709; difference −1.9233 [−2.6761, −1.1870] |
| M3 difference | 0.0082 [0.0075, 0.0089] | 0.0184 [0.0169, 0.0199] |
| makes per adult-year (c 0.0581) | 0.1884; ratio 3.2448 [3.0208, 3.4686] | 0.3332; ratio 5.7388 [5.2890, 6.1642] |
| guards | starvation raised | starvation and killing raised |
| reading | not supported | not supported |

**All three agree with the study.** The findings are final.
