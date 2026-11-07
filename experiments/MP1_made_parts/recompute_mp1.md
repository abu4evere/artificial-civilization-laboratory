# MP1: independent blind recompute (7 November 2026, 17:35)

## The inputs
- `recompute/mp1_counts.csv`: 32 rows, one per world. It was built by `recompute/build_mp1_counts.py`, written before
  data, which counts from the raw world files independently of analyse_mp1.py.
- `recompute/prompt.txt`, also written before data.

Each was given in a fresh chat, with no analysis script and no earlier result:
- **GPT:** chat 6aefa70d, "Medium" thinking, with code (Python; NumPy seed 20261107).
- **Gemini:** chat a15eca8399abcbb5, with code ("Show code").
- **DeepSeek** was not asked this time: in the last four rounds it had no code tool, and its intervals could not be
  counted.

**The numbers below are read from the replies.** The time in the title is from the clock.

## The numbers
| quantity | the study | GPT (code) | Gemini (code) |
|---|---|---|---|
| A + … + E = kinds in every row | yes | yes (0 errors; 3,690) | yes |
| **stage A** | **0.9024 [0.8907, 0.9142]** | 0.9024 [0.8907, 0.9141] | 0.9024 [0.8907, 0.9141] |
| stage B | 0.0564 [0.0470, 0.0666] | 0.0564 [0.0469, 0.0665] | 0.0564 [0.0472, 0.0664] |
| stage C | 0.0100 [0.0065, 0.0135] | 0.0100 [0.0066, 0.0135] | 0.0100 [0.0066, 0.0135] |
| stage D | 0.0168 [0.0136, 0.0202] | 0.0168 [0.0136, 0.0202] | 0.0168 [0.0136, 0.0202] |
| stage E | 0.0144 [0.0103, 0.0193] | 0.0144 [0.0103, 0.0192] | 0.0144 [0.0104, 0.0193] |
| **reading** | **A, clear** | A, clear | A, clear |
| handed | 0.4966 | 0.4966 [0.4278, 0.5560] | 0.4966 [0.4297, 0.5561] |
| worn out in use / by the cold | 0.1383 / 0.0907 | 0.1383 / 0.0907 | 0.1383 / 0.0907 |
| used into another thing / its kind | 0.1293 / 0.0726 | 0.1293 / 0.0726 | 0.1293 / 0.0726 |
| still held / dropped at the carry limit | 0.0476 / 0.0249 | 0.0476 / 0.0249 | 0.0476 / 0.0249 |
| unexplained | 0 | 0 | 0 |

## Verdict
- **GPT and Gemini agree with the study in every point estimate and in the reading,** each with code.
- Their intervals differ from the study's in the fourth decimal at most.

**The findings are final.**
