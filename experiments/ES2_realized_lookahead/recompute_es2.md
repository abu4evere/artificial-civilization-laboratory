# ES2 — independent blind recompute (1 November 2026)

- **Input:** the per-seed, per-arm sums from the raw output:
  - `recompute/es2_one_file.csv`, all actions, for the primary. Built by `recompute/build_es2_one_file.py`, written
    before data.
  - `recompute/es2_rest_guard.csv`, rest only, for the guard that decided the study.
  - The exact text sent is `recompute/prompt.txt`.
- **Who:** GPT (fresh chat `6ae76c59`) and Gemini (fresh chat `e54b764eee75c8e0`), sent at about 11:45. Each got the
  same text and the frozen rule (other guards excluded, as stated). Neither saw the analysis script or any earlier
  result.
- **Recorded only from their actual replies.** The prompt waited from 02:45 to 11:45, while the Chrome extension was
  disconnected.

| quantity | analyse_es2.py | GPT | Gemini |
|---|---|---|---|
| M v11 (mean abs(q − G)) | 0.3911 | 0.3911 | 0.3911 |
| M r | 0.2364 | 0.2364 | 0.2364 |
| M sham | 0.3919 | 0.3919 | 0.3919 |
| D_r = r − v11 | −0.1547 [−0.1614, −0.1480] | −0.1547 [−0.1615, −0.1483] | −0.1547 [−0.1614, −0.1480] |
| D_sham = sham − v11 | +0.0008 [−0.0063, +0.0085] | +0.0008 [−0.0064, +0.0084] | +0.0008 [−0.0062, +0.0084] |
| rest, v11 | 0.237 (0.2367 from the guard file) | 0.2367 | 0.2367 |
| rest, r | 0.391 (0.3912 from the guard file) | 0.3912 | 0.3912 |
| rest's rise (frozen limit 0.10) | +0.155 (+0.1545) | +0.1545 | +0.1545 |
| reading | not supported | not supported | not supported |

- **Notes:**
  - The interval ends differ in the fourth decimal: bootstrap randomness, which does not touch the rule. GPT used
    NumPy seed 20261101.
  - Gemini's totals: n v11 23,879,550, r 27,601,177, sham 24,604,386, the same as `results.md`.
  - **GPT:** the error falls "approximately 39.5%", but rest's error rise exceeds the frozen limit "by 0.0545".
  - Both read the three primary conditions as met and the rest guard as failed.

**All three agree on every number and on the reading. ES2 is final: not supported** (the primary is met; the rest
guard is raised).
