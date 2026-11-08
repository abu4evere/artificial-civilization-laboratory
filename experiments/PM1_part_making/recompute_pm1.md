# PM1: independent blind recompute (7 November 2026, 20:10)

## The inputs
- `recompute/pm1_counts.csv`: 32 rows, one per world. It was built by `recompute/build_pm1_counts.py`, written before
  data, which counts from the raw world files independently of analyse_pm1.py.
- `recompute/prompt.txt`, also written before data.

Each was given in a fresh chat, with no analysis script and no earlier result:
- **GPT:** chat 6aefcba8, "Instant" thinking; its reply says Python.
- **Gemini:** chat 8e771db55d92de44, with code ("Show code").
- **DeepSeek** was not asked: it had no code tool in the recent rounds.

**The numbers below are read from the replies.** The time in the title is from the clock.

## The numbers
| quantity | the study | GPT | Gemini (code) |
|---|---|---|---|
| stages sum to kinds in every row | yes (3,929 kinds) | yes (3,929) | yes |
| P0a | 0.1013 [0.0850, 0.1180] | 0.1013 [0.0850, 0.1180] | 0.1013 [0.0852, 0.1184] |
| P0b | 0.0260 [0.0203, 0.0323] | 0.0260 [0.0201, 0.0324] | 0.0260 [0.0203, 0.0325] |
| **P1** | **0.7096 [0.6879, 0.7289]** | 0.7096 [0.6885, 0.7287] | 0.7096 [0.6883, 0.7289] |
| P2 | 0.0468 [0.0408, 0.0531] | 0.0468 [0.0407, 0.0531] | 0.0468 [0.0406, 0.0531] |
| P3 | 0.0097 [0.0071, 0.0122] | 0.0097 [0.0072, 0.0123] | 0.0097 [0.0072, 0.0123] |
| P4 | 0.0506 [0.0438, 0.0579] | 0.0506 [0.0439, 0.0580] | 0.0506 [0.0439, 0.0578] |
| P5 | 0.0000 | 0.0000 | 0.0000 |
| P6 | 0.0262 [0.0216, 0.0309] | 0.0262 [0.0218, 0.0308] | 0.0262 [0.0217, 0.0308] |
| P7 | 0.0298 [0.0221, 0.0385] | 0.0298 [0.0223, 0.0386] | 0.0298 [0.0222, 0.0384] |
| never valued ÷ kinds | 0.1451 | 0.1451 [0.1283, 0.1615] | 0.1451 [0.1286, 0.1616] |
| P0a ÷ never valued | 0.6526 (372 of 570) | 0.6526 [0.5976, 0.7025] | 0.6526 [0.5970, 0.7024] |
| **reading** | **P1, clear** | P1, clear | P1, clear |

## Verdict
- **GPT and Gemini agree with the study in every point estimate and in the reading.**
- Their intervals differ in the fourth decimal at most.

**The findings are final.**
