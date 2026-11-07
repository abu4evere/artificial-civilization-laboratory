# EG1: independent blind recompute (7 November 2026, 13:54)

## The inputs
- `recompute/eg1_counts.csv`: 32 rows, one per world. It was built by `recompute/build_eg1_counts.py`, written before
  data, which counts from the raw world files independently of analyse_eg1.py.
- `recompute/prompt.txt`, also written before data.

Each was given in a fresh chat, with no analysis script and no earlier result:
- **GPT:** chat 6aef723e, "Medium" thinking, with code ("Analyzed").
- **Gemini:** chat a8c1994f1b284299, "Pro / High", with code ("Show code"). The first attempt was lost when the page
  reset, and the same text and file were sent again.
- **DeepSeek:** chat 9a6f304e. It had no code tool, and its own working says it would approximate the intervals ("bootstrap
  10k percentiles impossible manually exactly"). Its point estimates are read below; its intervals are **not counted**.

**The numbers below are read from the replies.** The time in the title is from the clock.

## The numbers
| quantity | the study | GPT (code) | Gemini (code) | DeepSeek (points only) |
|---|---|---|---|---|
| **P = starving_c ÷ starving weeks** | **0.0628 [0.0540, 0.0713]** | 0.0628 [0.0538, 0.0711] | 0.0628 [0.0540, 0.0712] | 0.0628 |
| a / b / c / d | 0.8794 / 0.0578 / 0.0628 / 0.0001 | the same | the same | the same |
| non-starving blocked share | 0.0065 [0.0057, 0.0073] | 0.0065 [0.0057, 0.0073] | 0.0065 [0.0057, 0.0073] | 0.0065 |
| quirk ÷ blocked starving weeks | 0.4289 [0.4201, 0.4367] | 0.4289 [0.4202, 0.4366] | 0.4289 [0.4203, 0.4366] | 0.4289 |
| deaths with a blocked week in the last 4 | 0.3502 [0.3024, 0.3959] | 0.3502 [0.3023, 0.3953] | 0.3502 [0.3021, 0.3965] | 0.3502 |
| a + b + c + d = starving weeks in every row | yes (the builder's check) | yes | yes | yes |
| **reading** | **a minor contributor** | a minor contributor | a minor contributor | a minor contributor |

## Verdict
- **GPT and Gemini agree with the study in every point estimate and in the reading,** each with code. Their intervals
  differ in the fourth decimal at most.
- DeepSeek's point estimates and its reading agree too, but it had no code tool, so its intervals are not counted.

**The findings are final.**
