# CU1 — A curiosity law: does a pull towards the rarely tried break the practice trap? Findings (final: recomputed blind by GPT and Gemini; see the end)

Frozen as `CU1-frozen` (operational note 1); **signed off by the creator** ("yea draft it and run on github", after
delegating the strength decision; debate round 27). A nature-change study: `code_cu1` = `code_v8` + one setting,
`curiosity_pull` (`v8_to_cu1.diff`). Run on GitHub Actions (run 40826056140, `skip_zero=local`). 96 worlds: v (v8),
c (curiosity pull), x (sham), on the same 32 paired seeds (20201–20232). LP (80 founders, 80×80), 200 years. Every
number comes from `analyse_cu1.py`, written before data; full tables are in `results.md`.

**Validity:** zero checks pass; all 96 worlds present under one fingerprint; in arm c every person's `tried` equals the
observer's count of their own updates (mismatches 0).

**Population beside it:** mean living in years 100–200: v 129.6, **c 132.8 (× 1.025)**, sham 124.0 (× 0.957). Died out
by year 200: v 2, c 1, sham 3.

## The answer

**Yes. A curiosity pull at the strength nature already gives play widens what people practise, clearly more than chance
drift, and making rises by more than half, with no harm.** It is the first change in this line of work to pass its
frozen rule.

### P (primary) — the spread of real practice (adults, years 100–200)
Of the situation–action pairs a person was offered, the share they actually learned from at least once:

| arm | share | − v [95%] |
|---|---|---|
| v (v8) | 0.2974 | |
| **c (curiosity)** | **0.3156** | **+0.0182 [+0.0157, +0.0205]** |
| x (sham) | 0.2936 | −0.0038 [−0.0077, −0.0003] |

**The frozen rule:** the lower bound of c − v (+0.0157) is above 0 and above the sham's upper bound (−0.0003):
**supports.** **Flags: none.** **"The change is supported by the frozen rule."** Adoption is the creator's decision.

The effect on the primary is modest in size (about 6% more of the offered pairs practised), but clear.

### Secondary (described; years 100–200)
| measure | v | c − v [95%] | sham − v |
|---|---|---|---|
| make pairs practised (share of make pairs offered) | 0.055 | **+0.028 [+0.023, +0.032]** (× 1.5) | −0.000 |
| **making events per adult-year** | 0.048 | **+0.028 [+0.023, +0.032]** (× 1.57) | −0.002 |
| made things held per adult | 0.98 | +0.14 [−0.04, +0.31] | −0.07 |
| world-born adults' (20–40) crafting skill | 0.232 | **+0.041 [+0.033, +0.048]** (× 1.18) | −0.005 |

Making, practice with making, and crafting skill all rise beyond the sham; things held rise but not clearly.

## Against the prior (the assistant's, frozen)
1. "P supports": **right.**
2. "No flags": **right** (population up slightly).
3. "Making rises somewhat; skill rises a little": **right**, and more than expected (making × 1.57; skill × 1.18).

GPT gave 55% that the law would meaningfully reduce practice starvation; Gemini expected a threefold rise in making
(not reached: × 1.57).

## What it means
- **The practice trap can be loosened by a general, honest drive,** not by favouring making: the pull is the same for
  every action, its strength is the play instinct's own, and it was not adjusted after PL1. Making rose because it was
  the most starved.
- **It is a step, not the cure.** Making is still rare (0.076 per adult-year against 0.21 in the first century, FS1),
  and 200 years cannot show whether knowledge now builds up over centuries.
- **For the creator:** whether to adopt the curiosity pull as nature v9. If adopted, the natural next steps are a
  long-run check (does the erosion over centuries slow?) and option C (a heritable strength that can evolve).

## Independent recompute
Pending: GPT and Gemini, fresh chats, raw per-world numbers. Recorded only from their actual replies.

## Independent recompute (29 October 2026)
GPT and Gemini, each in a fresh chat, worked from raw per-world numbers only, without the analysis script
(`recompute_cu1.md`). **All three agree:** practice spread c − v +0.0182 (supports; above the sham's band); no flags
(population × 1.0245); making 0.0483 → 0.0758 per adult-year.

**Final.**
