# LW1: independent blind recompute (7 November 2026, 12:37)

## The inputs
- `recompute/lw1_counts.csv`: 96 rows, one per arm and world. It was built by `recompute/build_lw1_counts.py`, written
  before data, which counts from the raw world files independently of analyse_lw1.py.
- `recompute/prompt.txt`, also written before data.

Each was given in a fresh chat, with no analysis script and no earlier result:
- **GPT:** chat 6aef611c, "Medium" thinking, with code ("Analyzed"). Its bootstrap's random seed was 20261107.
- **Gemini:** chat f23a63061c0ca84c, "Pro / High", with code ("Show code").
- **DeepSeek:** chat 60009f59. It had no code tool, and its own working says it would compute by hand. Its point
  estimates are read below. Its intervals are not a real bootstrap: for example, adult health [−0.12, +0.20] against
  about [−0.80, +0.90] from the others. So its intervals and its reading are **not counted**.

**The numbers below are read from the replies.** The time in the title is from the clock.

## The numbers
| quantity (LW − v15 unless noted) | the study (seed 20261109) | GPT (code) | Gemini (code) | DeepSeek (points only) |
|---|---|---|---|---|
| starvation ratio | 0.9132 [0.7881, 1.0628] | 0.9132 [0.7898, 1.0590] | 0.9132 [0.7857, 1.0582] | 0.9132 |
| killing difference | +0.0118 [+0.0025, +0.0226] | +0.0118 [+0.0025, +0.0223] | 0.0118 [0.0025, 0.0225] | 0.0118 |
| adult health difference | +0.0387 [−0.8053, +0.8976] | +0.0387 [−0.7973, +0.8993] | 0.0387 [−0.7974, 0.9114] | 0.0388 |
| living-weeks ratio | 1.0221 [0.9422, 1.1146] | 1.0221 [0.9412, 1.1155] | 1.0221 [0.9425, 1.1124] | 1.0221 |
| extinct worlds | −1 | −1 | −1 | −1 |
| child deaths ratio | 0.9423 [0.8165, 1.0901] | 0.9423 [0.8190, 1.0926] | 0.9423 [0.8181, 1.0908] | 0.9423 |
| child starvation ratio | 0.8135 [0.7010, 0.9492] | 0.8135 [0.7013, 0.9550] | 0.8135 [0.6992, 0.9527] | 0.8135 |
| gifts to kin's children ratio | 0.9952 [0.9070, 1.0901] | 0.9952 [0.9061, 1.0890] | 0.9952 [0.9085, 1.0877] | 0.9952 |
| guards raised | none | none | none | none |
| **co-primary, LW − v15** | **+0.0070 [−0.0001, +0.0140]** | +0.0070 [+0.0002, +0.0139] | 0.0070 [0.0001, 0.0139] | 0.0070 |
| co-primary, sham − v15 | −0.0022 [−0.0076, +0.0032] | −0.0022 [−0.0079, +0.0032] | −0.0022 [−0.0078, 0.0032] | −0.0022 |
| made by a non-inventor | −0.0003 [−0.0011, +0.0000] | −0.0003 [−0.0011, 0.0000] | −0.0003 [−0.0011, 0.0000] | −0.0003 |
| learned a missing part | +0.0107 [+0.0072, +0.0146] | +0.0107 [+0.0072, +0.0147] | 0.0107 [0.0073, 0.0146] | 0.0107 |
| **reading** | **no harm, no effect** | supported | supported | (not counted) |

## Where they disagree, and why
- **Every point estimate agrees,** in all three, to 4 decimals (DeepSeek's adult health is 0.0388, a rounding).
- **Only the co-primary's lower bound differs:** the study has −0.0001 (−0.00005 unrounded), GPT +0.0002 and Gemini
  +0.0001. That small gap flips the reading.
- **The cause is the bootstrap's own random draws.** The methods are the same:
  - paired draws;
  - pooled sums;
  - percentiles 2.5 and 97.5.

  The check is `recompute/mc_check_lw1.py`, written after data and changing nothing in the frozen analysis. Its output
  is in `recompute/mc_check_lw1.txt`:
  - **With the frozen random seed:** [−0.00005, +0.01401]; 2.6% of draws at or below 0.
  - **With 50 other random seeds** of 10,000 draws each, the lower bound runs from −0.00016 to +0.00012 (median
    +0.00001). It is above 0 in 28 of 50.
  - **With 200,000 draws:** −0.00001; 2.5% of draws at or below 0.
- **So the lower bound is 0 to within the bootstrap's noise.** Whether it prints as just below or just above 0 depends
  on the draw.
- **The frozen rule fixed the random seed (20261109) before data, so the frozen reading stands: no harm, no effect.**
  GPT and Gemini are not wrong. With their draws, the same rule reads "supported". The honest summary is that **the
  effect sits exactly on the line** (one-sided, about 2.5% of draws at or below 0).

**The cause is found and recorded, so the findings can be final.** The frozen reading is kept, and the knife-edge is
stated plainly in the findings.
