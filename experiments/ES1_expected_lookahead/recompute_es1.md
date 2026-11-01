# ES1 — independent blind recompute (31 October 2026)

- **Input:** `recompute/es1_one_file.csv`, per-seed, per-arm sums from the raw output, built by
  `recompute/build_es1_one_file.py` (written before data).
- **Who:** GPT (fresh chat `6ae6a7a6`) and Gemini (fresh chat `f5066b3172729a0d`). Each got the same text and the frozen
  rule (guards excluded, as stated). Neither saw the analysis script or any earlier result.
- **Recorded only from their actual replies.**

| quantity | analyse_es1.py | GPT | Gemini |
|---|---|---|---|
| M v11 (mean abs(q − G)) | 0.3919 | 0.3919 | 0.3919 (0.391898) |
| M e | 0.4230 | 0.4230 | 0.4230 (0.423003) |
| M sham | 0.3859 | 0.3859 | 0.3859 (0.385938) |
| D_e = e − v11 | +0.0311 [+0.0218, +0.0398] | +0.0311 [+0.0218, +0.0398] | +0.0311 [0.0215, 0.0398] |
| D_sham = sham − v11 | −0.0060 [−0.0149, +0.0032] | −0.0060 [−0.0149, +0.0032] | −0.0060 [−0.0149, +0.0034] |
| reading | not supported | not supported | not supported |

- Gemini's interval ends differ in the fourth decimal: bootstrap randomness, which does not touch the rule.
- **GPT:** the error rose "approximately 7.94%".

**All three agree on every number and on the reading. ES1 is final: not supported.**
