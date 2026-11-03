# AM2: independent blind recompute (3 November 2026)

**The inputs:** `recompute/am2_counts.csv` (built by `recompute/build_am2_counts.py`) and `recompute/prompt.txt`. Each
model was given these in a fresh chat, with no analysis script and no earlier result. **The numbers below are read from
their replies.**

| quantity | the study (`analyse_am2.py`) | GPT (fresh chat, code) | Gemini 3.1 Pro (fresh chat, code, on the second ask) |
|---|---|---|---|
| M3: c / h / t / x | 0.0036 / 0.0276 / 0.0076 / 0.0033 | 0.0036 / 0.0276 / 0.0076 / 0.0033 | 0.0036 / 0.0276 / 0.0076 / 0.0033 |
| M5: c / h / t / x | 0.0037 / 0.0305 / 0.0080 / 0.0034 | 0.0037 / 0.0305 / 0.0080 / 0.0034 | 0.0037 / 0.0305 / 0.0080 / 0.0034 |
| M3, c − h [95%] | −0.0240 [−0.0257, −0.0224] | −0.023994 [−0.025781, −0.022347] | −0.0240 [−0.0258, −0.0224] |
| M3, c − t [95%] | −0.0040 [−0.0045, −0.0035] | −0.003985 [−0.004496, −0.003520] | −0.0040 [−0.0045, −0.0035] |
| M5, c − h [95%] | −0.0269 [−0.0287, −0.0250] | −0.026863 [−0.028779, −0.024940] | −0.0269 [−0.0287, −0.0250] |
| M5, c − t [95%] | −0.0043 [−0.0049, −0.0038] | −0.004332 [−0.004942, −0.003768] | −0.0043 [−0.0050, −0.0038] |
| readings | M3 and M5 not validated | not validated, both | not validated, both |
| sanity count (arm a) | 0 | 0 | 0 |
| living-weeks: c / h / a / t / x | 23,176,597 / 18,243,321 / 23,282,840 / 21,224,492 / 23,134,685 | the same | the same |

## Notes
- **The study's intervals** come from its "arm − v12" columns with the sign reversed. Bootstrap draws differ, so the
  last digit may differ by 1 or 2.
- **Arm a:** GPT reports M3 and M5 as undefined (0/0); Gemini prints 0.0000 there. That arm has no gather chains. The
  study prints nan.
- **Gemini** first answered "I'm having a hard time fulfilling your request". It computed after being asked to load
  the file with its code tool. That second request was sent in a tab the session later lost, then again in the same
  chat.
- **DeepSeek** (fresh chat, no code tool) worked by hand, and its reply stopped before a final answer.
  - Its working notes show the same point differences (for example M5 c − t −0.0043315 and c − h about −0.0269), and
    the reading "neither" for validation.
  - Its intervals there were a rough normal approximation, much narrower, and are not used.
- **M1** (self-prediction gain) was not part of this file, as in AM1's prompt. It is not validated in the study.

**All recomputed numbers agree with the study.** The readings (M3 and M5 not validated, both controls higher) stand.
AM2 is final.
