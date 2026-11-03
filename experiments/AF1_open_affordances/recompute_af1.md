# AF1: independent blind recompute (3 November 2026)

- **Input:** `recompute/af1_counts.csv` (160 rows). Per arm and world: the kinds invented in years 100–195, how many
  had their own recipe made again within five years, the living weeks and extinction. It was built by
  `recompute/build_af1_counts.py`, written before data.
- **The exact text sent:** `recompute/prompt.txt`, written and committed before the data existed. The CSV was attached
  as a file.
- **Who** (each a fresh chat; none saw the analysis script or any earlier result):
  - GPT, chat `6ae97939`: Python, 10,000 draws;
  - Gemini 3.1 Pro (High), chat `6f881f4f9bb44719`: it ran code ("Show code");
  - DeepSeek, chat `0edb4e50`: **it had no code tool**. It summed the columns by hand (its kind totals match exactly)
    and gave bootstrap intervals by its own approximation of the resampling.
- **Recorded only from their actual replies.**

| quantity | analyse_af1.py | GPT | Gemini | DeepSeek |
|---|---|---|---|---|
| R: v11 / S / K / S+K / sham | 0.0003 / 0.0006 / 0.0000 / 0.0000 / 0.0000 | the same (1/3,414, 2/3,437, 0/3,150, 0/3,194, 0/3,346) | the same | the same (same sums) |
| S − v11 | +0.0003 [−0.0007, +0.0012] | +0.000289 [−0.000637, +0.001208] | +0.0003 [−0.0007, 0.0012] | +0.000289 [−0.00059, +0.00116] |
| K − v11 | −0.0003 [−0.0010, +0.0000] | −0.000293 [−0.000972, 0] | −0.0003 [−0.0010, 0.0000] | −0.000293 [−0.00089, 0] |
| S+K − v11 | −0.0003 [−0.0010, +0.0000] | −0.000293 [−0.000972, 0] | −0.0003 [−0.0010, 0.0000] | −0.000293 [−0.00089, 0] |
| S − sham | +0.0006 [+0.0000, +0.0014] | +0.000582 [0, +0.001375] | +0.0006 [0.0000, 0.0014] | +0.000582 [0, +0.00143] |
| K − sham, S+K − sham, S+K − K | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] |
| S+K − S | −0.0006 [−0.0014, +0.0000] | −0.000582 [−0.001375, 0] | −0.0006 [−0.0014, 0.0000] | −0.000582 [−0.00143, 0] |
| sham − v11 | −0.0003 [−0.0010, +0.0000] | −0.000293 [−0.000972, 0] | −0.0003 [−0.0010, 0.0000] | −0.000293 [−0.00089, 0] |
| readings | S, K, S+K inconclusive | the same | the same | the same |
| population ÷ v11 | S 0.981 [0.868, 1.102]; K 0.966 [0.847, 1.093]; S+K 0.974 [0.858, 1.094] | S 0.9805 [0.8665, 1.0990]; K 0.9658 [0.8468, 1.0975]; S+K 0.9735 [0.8599, 1.0939] | S 0.9805 [0.8664, 1.0993]; K 0.9658 [0.8463, 1.0926]; S+K 0.9735 [0.8602, 1.0943] | S 0.9805 [0.86, 1.10]; K 0.9658 [0.84, 1.09]; S+K 0.9735 [0.85, 1.09] |
| extinctions (v11 2) | S 1, K 2, S+K 1 | the same | the same | the same |
| guards | none raised | none raised | none raised | none raised |

- **GPT's note:** "Only 3 remakes among 16,541 invented kinds occurred across all five arms". Also, "a zero-width
  bootstrap interval for contrasts between k, sk, and x reflects zero observed remakes in those arms, not proof of
  equivalent underlying remake probabilities."
- **GPT and Gemini agree with the analysis** on every point value, reading and guard. Their interval ends differ by at
  most 0.004 (population ratios).
- **DeepSeek agrees** on every point value, reading and guard. Its intervals are hand approximations, so its interval
  ends differ by up to 0.0001 on R and by up to 0.01 on population. Nothing that decides a reading depends on those
  digits.

**All three agree: S, K and S+K inconclusive; no guard raised. AF1 is final.**

**The browser tabs:** the AF1 tabs were closed. When the first tab closed, the tab group dissolved, so the original
Gemini and DeepSeek tabs may still be open outside the assistant's group, where it cannot close them.
