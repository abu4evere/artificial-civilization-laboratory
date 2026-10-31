# HD1-C — independent blind recompute (31 October 2026)

- **Input:** `recompute/hd1c_one_file.csv`, per-world, per-arm sums from the raw output (32 paired seeds × 3 arms).
- **Who:** GPT (fresh chat `6ae66b0f`) and Gemini (fresh chat `0810a5fefef3650a`; a first Gemini chat, `fbdb99a259934be0`,
  returned an error and no numbers). Each got the same text and the frozen rule (no-harm flags excluded, as stated).
  Neither saw the analysis script or any earlier result.
- **Recorded only from their actual replies.**

| quantity | analyse (HD1's, unchanged) | GPT | Gemini |
|---|---|---|---|
| R v10 | 0.0103 | 0.0103 (1.0268%) | 0.0103 (0.010268) |
| R h | 0.0128 | 0.0128 (1.2811%) | 0.0128 (0.012811) |
| R sham | 0.0105 | 0.0105 (1.0472%) | 0.0105 (0.010473) |
| D_h = h − v10 | +0.0025 [+0.0018, +0.0034] | +0.0025 [0.0018, 0.0034] | 0.0025 (0.002543) [0.0018, 0.0034] |
| D_sham = sham − v10 | +0.0002 [−0.0006, +0.0009] | +0.0002 [−0.0006, 0.0009] | 0.0002 (0.000205) [−0.0005, 0.0010] |
| reading | supported (confirmed) | supported | supported |

Gemini's sham interval differs in the fourth decimal: bootstrap randomness around zero, which does not touch the rule.

**All three agree on every number and on the reading. HD1-C is final: the handing law is confirmed on new seeds.**
