# LR1 — Does nature v8 stay healthy over 1,000 years? Findings (final: recomputed blind by GPT and Gemini; see the end)

Frozen as `LR1-frozen` (operational note 1); decided and signed off in sleep mode (`docs/autonomous_decisions.md`).
Read-only; a description, not an adoption test. Run on GitHub Actions (run 40640605709, `skip_zero=local`). 96 worlds:
v7 (`ground_items` 0), v8 (live nature) and a sham (v8 with one meaningless extra draw), on the same 32 paired seeds
(19601–19632). LP (80 founders, 80×80), **1,000 years**. Every number comes from `analyse_lr1.py`, written before data;
full tables are in `results.md`.

**Validity:** zero checks pass; all 96 worlds are present under one fingerprint (`code_v8`); in v8, drops = pick-ups +
things on the ground in every year (mismatches 0).

## The answer

**v8 is stable over 1,000 years in both respects checked. Neither flag is raised.**

### Q1 — Things on the ground do not pile up
- Mean things on the ground per world: **122.3 at year 200, then 110.3, 82.4, 75.8 and 77.6 at year 1,000** (the sham:
  108.2 → 75.2). Year 1,000 is **0.63** of year 200.
- Slope over years 800–1,000: **+0.003 per year [−0.001, +0.008]**: level.
- The most on any one tile (worst world): 29 at years 200–400, 18 later.
- Pick-ups balance drops: 0.79–1.05 of drops per century. 0.959 of 76,639 pick-ups are by someone other than the
  dropper.
- **Flag A (accumulation): not raised.**

### Q2 — Population, beside the sham
| years | v7 | v8 | sham | v8 ÷ v7 | sham ÷ v7 |
|---|---|---|---|---|---|
| 0–100 | 118.2 | 116.5 | 119.1 | 0.986 | 1.008 |
| 400–500 | 59.5 | 55.3 | 55.3 | 0.928 | 0.929 |
| 900–1,000 | 65.7 | 64.9 | 66.2 | 0.987 | 1.008 |

- Years 800–1,000: v8 ÷ v7 **0.988 [0.702, 1.406]**; the sham ÷ v7 1.016 [0.771, 1.292]. The interval is wide (32
  worlds over 1,000 years drift a lot), and v8 sits inside the sham's range.
- Died out: v7 8, v8 8, sham 10 of 32.
- **Flag B (demography): not raised.**
- **Described:** in all three arms, population falls by about half between years 100 and 500 (about 118 to about 55),
  then recovers slowly (about 65 by year 1,000). This is not v8's doing (v7 does the same). It matches M1's finding that
  surviving worlds erode over 1,000 years.

### Q3 — Made things held per adult
- v8 holds more than v7 in every century: 1.191 against 0.595 in years 0–100 (2.0×), 0.323 against 0.197 in years
  900–1,000 (1.6×). The sham, which is also v8, ends at 0.371.
- In every arm, things held per adult **fall over the centuries** (v8: 1.19 → 0.32; v7: 0.60 → 0.20).

## Against the prior (the assistant's, frozen)
1. "Things on the ground level off; no flag A": **right** (level, and lower than at year 200).
2. "No flag B; v8 ÷ v7 within the sham band": **right.**
3. "Tools held per adult stay about twice v7's": **partly right.** About twice at first, 1.6 times by the end; both
   fall.

## What follows (from the frozen branches)
- **"No flags: v8 is stable over 1,000 years in these respects. Recorded."**
- **Described, for the creator:** the long decline is the bigger story. Population and tools held fall in v7 and v8
  alike over centuries. It is M1's erosion again, on today's nature: ACL's worlds do not build up over 1,000 years.

## Independent recompute
Pending: GPT and Gemini, fresh chats, raw per-world numbers (the ground count at years 200 and 1,000, the slope inputs,
and summed living over years 800–1,000 per arm). Recorded only from their actual replies.

## Independent recompute (28 October 2026)
GPT and Gemini, each in a fresh chat, worked from raw per-world numbers only, without the analysis script
(`recompute_lr1.md`). **All three agree:** ground 122.28 → 77.59 (ratio 0.6346); slope 0.0034; population v8 ÷ v7
0.9882 (sham 1.0158); extinct 8 / 8 / 10; no flags. Gemini's bootstrap put the upper end of v8 ÷ v7's interval at 1.389
instead of 1.406 (different draws; a long-tailed ratio).

**Final.**
