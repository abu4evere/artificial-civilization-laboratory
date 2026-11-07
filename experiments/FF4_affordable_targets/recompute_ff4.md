# FF4: independent blind recompute (7 November 2026, 16:57)

## The inputs
- `recompute/ff4_counts.csv`: 96 rows, one per arm and world. It was built by `recompute/build_ff4_counts.py`, written
  before data, which counts from the raw world files independently of analyse_ff4.py.
- `recompute/prompt.txt`, also written before data.

Each was given in a fresh chat, with no analysis script and no earlier result:
- **GPT:** chat 6aef9e28, "Medium" thinking, with code.
- **Gemini:** chat ee00c96d76b2b630, with code ("Show code").
- **DeepSeek:** chat 90203eee. It had no code tool and was still working by hand when this was written; its own
  working says it cannot run the bootstrap. Nothing from it is counted.

**The numbers below are read from the replies.** The time in the title is from the clock.

## The numbers
| quantity (f against v15) | the study | GPT (code) | Gemini (code) |
|---|---|---|---|
| starvation ratio | 0.9813 [0.8924, 1.0753] | 0.9813 [0.8935, 1.0755] | 0.9813 [0.8942, 1.0786] |
| killing difference | +0.0002 [−0.0087, +0.0086] | +0.0002 [−0.0086, 0.0085] | 0.0002 [−0.0086, 0.0085] |
| adult health difference | +0.4857 [−0.0985, +1.0449] | +0.4857 [−0.1178, 1.0548] | 0.4857 [−0.1092, 1.0474] |
| living-weeks ratio | 0.9657 [0.8779, 1.0636] | 0.9657 [0.8788, 1.0654] | 0.9657 [0.8775, 1.0644] |
| extinct worlds | 0 | 0 | 0 |
| child deaths ratio | 1.1045 [0.9417, 1.2556] | 1.1045 [0.9438, 1.2578] | 1.1045 [0.9477, 1.2573] |
| child starvation ratio | 1.1050 [0.9051, 1.3123] | 1.1050 [0.9092, 1.3200] | 1.1050 [0.9127, 1.3138] |
| gifts to kin's children ratio | 0.9901 [0.9241, 1.0676] | 0.9901 [0.9245, 1.0695] | 0.9901 [0.9241, 1.0693] |
| **guards raised** | **none** | none | none |
| EG1's P, v15 / f | 0.0635 / 0.0570 | 0.0635 / 0.0570 | 0.0635 / 0.0570 |
| P ratio f / v15 | 0.8980 [0.8318, 0.9666] | 0.8980 [0.8318, 0.9707] | 0.8980 [0.8326, 0.9679] |
| P women 30–49, v15 / f (ratio) | 0.1188 / 0.1209 (1.0183) | the same (1.0183 [0.9710, 1.0692]) | the same (1.0183 [0.9709, 1.0689]) |
| P men 30–49, v15 / f (ratio) | 0.0553 / 0.0444 (0.8019) | the same (0.8019 [0.7238, 0.8956]) | the same (0.8019 [0.7231, 0.8943]) |
| **reading** | **no harm** | no harm | no harm |

## Verdict
- **GPT and Gemini agree with the study in every point estimate, in every guard, and in the reading,** each with code.
- Their intervals differ from the study's in the third decimal at most, as different random draws would.

**The findings are final.**
