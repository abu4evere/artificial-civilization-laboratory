# VW1 blind recompute (7 November 2026)

**What was sent:**
- the file: `recompute/vw1_counts.csv`, from `recompute/build_vw1_counts.py` on the cloud output;
- the prompt: `recompute/prompt.txt`.

Each model got them in a fresh chat, without the analysis script or any earlier result. Every number below was read
from the model's reply.

## GPT (fresh chat https://chatgpt.com/c/6aeffa80-b340-83ea-b74f-7e13e620c581; "Instant"; code)

| quantity | GPT | the frozen analysis (results.md) |
|---|---|---|
| starvation deaths, ratio w / c | 0.8734 [0.7734, 0.9802] | 0.8734 [0.7716, 0.9791] |
| killing deaths, difference | -0.0025 [-0.0105, 0.0050] | -0.0025 [-0.0103, +0.0050] |
| adult health, difference | +0.7025 [0.1417, 1.3059] | +0.7025 [+0.1391, +1.3057] |
| living-weeks, ratio | 1.0722 [0.9582, 1.2112] | 1.0722 [0.9577, 1.2166] |
| extinct worlds, extra | -1 | -1 |
| child deaths, ratio | 0.9352 [0.8108, 1.0849] | 0.9352 [0.8145, 1.0850] |
| child starvation deaths, ratio | 0.8584 [0.7181, 1.0180] | 0.8584 [0.7191, 1.0208] |
| gifts to kin's children, ratio | 1.0778 [0.9560, 1.2059] | 1.0778 [0.9595, 1.2099] |
| guards raised | 0 of 8 | none |
| co-primary 1, any part held, w − c | +0.0084 [-0.0043, 0.0212] | +0.0084 [-0.0046, +0.0210] |
| co-primary 1, x − c | -0.0010 [-0.0193, 0.0169] | -0.0010 [-0.0191, +0.0176] |
| co-primary 2, all parts held, w − c | +0.0063 [-0.0048, 0.0172] | +0.0063 [-0.0049, +0.0171] |
| co-primary 2, x − c | -0.0064 [-0.0167, 0.0035] | -0.0064 [-0.0166, +0.0035] |
| reading | "No harm, no effect" | no harm, no effect |

**GPT matches** every point estimate and the reading. The intervals differ only in the last digits, as different
bootstrap draws do.

## Gemini (fresh chat https://gemini.google.com/app/63a22dd5d0d14b99; Pro, High; code)
The answer appeared only after the chat was reopened. A second attempt in a new chat never sent, so there was no
duplicate.

| quantity | Gemini | the frozen analysis |
|---|---|---|
| starvation deaths, ratio | 0.8734 (0.7764, 0.9793) | 0.8734 [0.7716, 0.9791] |
| killing deaths, difference | -0.0025 (-0.0103, 0.0050) | -0.0025 [-0.0103, +0.0050] |
| adult health, difference | 0.7025 (0.1491, 1.3012) | +0.7025 [+0.1391, +1.3057] |
| living-weeks, ratio | 1.0722 (0.9604, 1.2147) | 1.0722 [0.9577, 1.2166] |
| extinct worlds, difference | -1.0000 | -1 |
| child deaths, ratio | 0.9352 (0.8141, 1.0822) | 0.9352 [0.8145, 1.0850] |
| child starvation deaths, ratio | 0.8584 (0.7236, 1.0210) | 0.8584 [0.7191, 1.0208] |
| gifts to kin's children, ratio | 1.0778 (0.9557, 1.2061) | 1.0778 [0.9595, 1.2099] |
| co-primary 1, w − c | 0.0084 (-0.0050, 0.0214) | +0.0084 [-0.0046, +0.0210] |
| co-primary 1, x − c | -0.0010 (-0.0188, 0.0174) | -0.0010 [-0.0191, +0.0176] |
| co-primary 2, w − c | 0.0063 (-0.0050, 0.0172) | +0.0063 [-0.0049, +0.0171] |
| co-primary 2, x − c | -0.0064 (-0.0170, 0.0035) | -0.0064 [-0.0166, +0.0035] |
| guards raised | "None" | none |
| reading | "no harm, no effect" | no harm, no effect |

**Gemini matches** every point estimate and the reading.

## Verdict
Both recomputes match the frozen analysis in every point estimate, every guard and the reading. **The findings are
final.**
