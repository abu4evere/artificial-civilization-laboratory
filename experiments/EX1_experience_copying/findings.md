# EX1 — Experience telling instead of habit copying: does it correct the over-valuation? Findings (final: recomputed blind by GPT and Gemini; see the end)

Frozen as `EX1-frozen` (operational note 1); decided and signed off in sleep mode (`docs/autonomous_decisions.md`).
A nature-change study: `code_ex1` = `code_v8` + one setting, `talk_copy` (`v8_to_ex1.diff`). Run on GitHub Actions
(run 40808047321, `skip_zero=local`). 96 worlds: v (v8: whole-table copying), e (experience telling), x (sham), on the
same 32 paired seeds (20001–20032). LP (80 founders, 80×80), 200 years. Every number comes from `analyse_ex1.py`,
written before data; full tables are in `results.md`.

**Validity:** zero checks pass; all 96 worlds present under one fingerprint; the TD replay is exact and every told
experience was checked exactly (mismatches 0). In arm e, 2,481,506 experiences were told instead of table copies; 0.926
were about a situation the listener had already learned in.

**Population beside it:** mean living in years 100–200: v 123.7, e 122.7 (ratio 0.992), sham 118.9. Died out by year
200: v 0, e 1, sham 0.

## The answer

**No. Replacing whole-table copying with experience telling does not change the over-valuation at all.**

| measure (years 100–200, adults) | v (v8) | e (experience) | improvement v − e [95%] | sham: v − x |
|---|---|---|---|---|
| **common actions' bias (q − G)** | **+0.431** | **+0.438** | **−0.006 [−0.018, +0.005]** | +0.008 |
| make's bias | −0.560 | −0.555 | −0.005 [−0.025, +0.017] | +0.019 |
| mean realised return G | 0.676 | 0.676 | e − v +0.000 [−0.021, +0.023] | |

**The frozen rule:**
- **P (calibration): does not support** (improvement −0.006; needed at least 0.10 with the lower bound above 0).
- **H (realised return): no harm** (lower bound −0.021, above −0.05).
- **F (flags): none** (extinct 1 vs 0; population ratio 0.992).
- **"The change is not supported by the frozen rule."** No nature-v9 candidate.

**Described:** making per adult-year 0.047 in v, e − v −0.000 [−0.003, +0.003]; made things held per adult 0.94, e − v
−0.06 [−0.24, +0.11]. Every per-action bias is within ±0.01 of v's.

## Against the prior (the assistant's, frozen)
1. "P supports: the bias falls to under +0.15": **wrong.** It did not move (+0.431 → +0.438).
2. "H: no harm": **right.**
3. "No flags": **right.**
4. "Making rises somewhat": **wrong** (unchanged).

GPT's and Gemini's expectations (both chose this law, 80% and 85%) are not supported either.

## What it means
- **Copying is not what causes the over-valuation.** CL1 found that 0.93 of it *arrives* through copying in talk, but,
  as GPT cautioned then, that was "exact accounting of how the value arrived, not causal attribution". With whole-table
  copying gone, people's own learning produces the same inflated values: copying was only the road, not the source.
  HC1's failure fits the same picture.
- **The likely source is the habit rule's own look-ahead** (described, not tested here): HL1 found that rewards stay
  flat while the look-ahead term (0.8 × the best habit value next week) grows from 0.06 to 1.26, so often-done actions
  lift themselves. A max over many noisy values is biased upwards, and that bias feeds itself. **This points at the
  learning rule itself** (for example how the next week is valued: the best option vs what is actually chosen), which
  is the next question for GPT, Gemini and the creator.
- **Also learned:** a whole channel of "telepathy" (copying entire habit tables) can be replaced by people telling one
  real experience at a time, at no cost to returns, population or survival. That may matter later for the language
  line, where removing telepathy is the plan. It is not proposed for nature by this study's rule.

## Independent recompute
Pending: GPT and Gemini, fresh chats, raw per-world numbers. Recorded only from their actual replies.

## Independent recompute (29 October 2026)
GPT and Gemini, each in a fresh chat, worked from raw per-world numbers only, without the analysis script
(`recompute_ex1.md`). **All three agree:** improvement −0.0064 (not supported); G e − v +0.0004 (no harm); population
ratio 0.9921; no flags.

**Final.**
