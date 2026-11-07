# NV16: nature v16 adopted (7 November 2026)

**What changed:** FF4's fault fix (`fix_affordable_target`, default 1). Forage, hunt and gather are offered at the best
target the person can afford when the best one is too far. Under v15 the whole action was dropped, even when a nearer
target was affordable.
- Only `acl/config.py` and `acl/mind.py` change (`v15_to_v16.diff`, 24 lines).
- FF4's study logging is left out.
- The previous nature stays in `experiments/NV15_nature_v15/code_v15`.

## The safe path (CLAUDE.md), step by step
1. **A frozen study supports the change.** FF4 (`experiments/FF4_affordable_targets/findings.md`) reads "no harm": no
   guard raised among CI1's eight, and the sham quiet. A fault fix has no confirmatory run (FF1–FF3).
2. **The blind recompute matches.** GPT and Gemini, each with code, match every point estimate, every guard and the
   reading (`recompute_ff4.md`).
3. **No confirmatory run** is needed for a fault fix (above).
4. **The council agrees on adoption** (`docs/debate_round77_after_ff4_mp1_2026-11-07.md`): GPT yes, 98%; Gemini yes,
   100%; DeepSeek yes, about 94%. The assistant's estimate is 95%.
5. **Zero checks:** `zero.txt`, All: PASS (`run_nv16.py`, run 7 November 2026, finished 17:56):
   - code_v16 with the fix off = code_v15 (world and random stream; 4 cases);
   - v16 = FF4's arm f (2 cases);
   - the live package with its own defaults = v16 (2 cases);
   - the fix acts;
   - reload is exact.
6. **Reference hashes and tests.** `tests/reference_hashes.json` is regenerated for `acl` and `v16`, and the two match.
   `tests/test_reference_replays.py` gains v16. **71 tests pass** (18:02).
7. **The record:** tag `nature-v16`, a line in `docs/autonomous_decisions.md`, and a Telegram message to the creator.

## What v16 changes in the world (FF4, against v15)
- Weeks where food was blocked by energy alone although an affordable tile had food fell tenfold: 0.0069 → 0.0007 of
  non-starving weeks.
- Starving weeks blocked by energy alone fell: 0.0635 → 0.0570. The remaining weeks are real tiredness, where even
  one's own tile is unaffordable.
- No harm measure moved.
- The women 30–49 gap is unchanged. It is a different mechanism; the next read-only study is DF1.
