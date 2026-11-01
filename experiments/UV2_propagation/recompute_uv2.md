# UV2 — independent blind recompute (1 November 2026)

- **Input:** `recompute/uv2_one_file.csv`, the per-seed sums for the primary (arm r; k ≥ 80, ages 16–44, G not closed
  by death), built by `recompute/build_uv2_one_file.py` (written before data). The exact text sent is
  `recompute/prompt.txt`.
- **Who:** GPT and Gemini, in fresh chats. Each got the same text and the frozen rule. Neither saw the analysis script
  or any earlier result.
  - **Gemini:** chat `9391fd11d93321a7`.
  - **GPT:** chat `6ae7b31e`, on the "High" thinking setting, was still working after about 7 minutes. So the same
    text went to a second fresh GPT chat, `6ae7b519`, on "Instant". **Both GPT chats then answered.** Both replies
    are recorded below; they agree.
- **Recorded only from their actual replies.**

| quantity | analyse_uv2.py | GPT (`6ae7b31e`) | GPT (`6ae7b519`) | Gemini |
|---|---|---|---|---|
| B (Dn < 0.1) | −0.1108 [−0.1151, −0.1064] | −0.1108 [−0.1151, −0.1064] | −0.1108 [−0.1151, −0.1064] | −0.1108 [−0.1154, −0.1063] |
| B (all Dn) | −0.1077 [−0.1106, −0.1047] | −0.1077 [−0.1106, −0.1047] | −0.1077 [−0.1106, −0.1047] | −0.1077 [−0.1106, −0.1046] |
| coverage (n; worlds) | 362,963; 32 | 362,963; 32 | 362,963; 32 | 362,963; 32 |
| reading | not propagation | not propagation | not propagation | not propagation |

- **Notes:**
  - Both GPT chats used NumPy seed 20261101, so their intervals are identical to the analysis's. Gemini's differ in
    the fourth decimal: bootstrap randomness.
  - **GPT (`6ae7b519`):** the absolute-bias ratio is "approximately 1.028". The result "rejects the specified
    propagation criterion, not every possible propagation mechanism".
  - **GPT (`6ae7b31e`):** "does not establish that propagation contributes nothing".

**All agree on every number and on the reading. UV2 is final: not propagation.**
