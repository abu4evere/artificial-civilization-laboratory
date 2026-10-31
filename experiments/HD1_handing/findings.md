# HD1 — Can a person hand a made thing to another? Findings (final: recomputed blind by GPT and Gemini; see the end)

**A nature-change test in a copy (`code_hd1` = `code_v10` + `hand_items`), not an adoption.** Frozen as `HD1-frozen`
(operational note 1). Signed off by the assistant under sleep-mode autonomy (GPT 88%, Gemini 85%; debate round 37).
**The creator, on Telegram (31 October, 13:31):** "I think that law is fine cuz it works in real life we give things to
other people and get from other people."

Run on GitHub Actions (run 41226917887, `skip_zero=local`). 96 worlds: v10 (`hand_items` 0, equal to `code_v10`), h
(`hand_items` 1) and a sham, on 32 paired seeds (21201–21232); LP (80 founders, 80 × 80), 200 years. Every number comes
from `analyse_hd1.py`, written before data and tested on smoke worlds; full tables are in `results.md`.

**Validity:**
- zero checks pass (`code_hd1` off = `code_v10`; the law acts; the sham acts; the observer is read-only; reload is
  exact);
- all 96 worlds are present under one fingerprint;
- every forage replay is exact, and every handing conserves the item (mismatches 0).

**Population beside it:** extinctions were v10 0, h 0, sham 1. Mean living population, h ÷ v10, was 0.980 [0.871,
1.089]; the sham's was 0.955.

## The answer

**Supported, with a small effect.** Letting people hand made things to each other raises what tools add to food by
about a third, and no harm flag is raised. In absolute terms it is +0.36 percentage points of foraged food: far from
TR1's 20% headroom.

### Primary — food added by tools (share of adults' foraged food, years 100–200)
| arm | R |
|---|---|
| v10 | 1.07% |
| h (handing) | 1.43% |
| sham | 1.14% |

- **h − v10: +0.36 points** [+0.28, +0.45].
- **The sham's own difference:** +0.07 [−0.00, +0.14].
- **By the frozen rule** (h − v10 > 0 with its lower bound > 0, above the sham's difference, and no flag):
  **SUPPORTED.**

### Mechanism (described)
- **Handings:** 0.20 per adult-year in h, 64,384 in years 100–200. **Reversals** (handed straight back) are 0.03%.
- **Adult forage weeks with a tool in hand:** v10 11.0%, h **15.6%**, sham 11.5%.
- **Recipients forage with a tool in 51.5% of their forage weeks** in the year after receiving one (about 11% for all
  adults in v10).
- **Food gifts per adult-year:** v10 5.98, h 5.79, sham 5.76. Handing does not crowd out food giving beyond chance.

### No-harm flags (all not raised)
- **Population:** 0.980 [0.871, 1.089].
- **Food per adult:** 1.002.
- **Recipes per adult:** 0.996.
- **Food gifts:** 0.967 [0.900, 1.030]; the sham's is 0.962.
- **Child deaths:** +0.71 per 1,000 child-years [−1.39, +2.91].
- **Extinctions:** +0.
- **Ping-pong:** 0.03%.

## Against the prior (the assistant's, frozen)
1. "Supported: R rises from about 1% to 3–6%": **supported, but the size was wrong** (1.43%).
2. "Handings frequent (more than 1 per adult-year)": **wrong** (0.20).
3. "No flags": **right.**

## What it means
- **The missing ability matters, but handing alone does not close the gap.**
  - Tools reach more hands (11% → 16% of forage weeks), and recipients use them.
  - But people hand things rarely (0.2 a year), so most of TR1's 20% headroom stays unused.
  - This fits TA1: there is **a choice gap as well as an access gap.**
- **It is a fair physical law:** no reward, no custom, objects conserved. Its use is left to people's own choices.
- **What follows, by the safe path in `CLAUDE.md`:**
  1. this study's blind recompute by GPT and Gemini;
  2. **a confirmatory run on new seeds**;
  3. both models consulted on adoption;
  4. then `code_v11` with zero checks, hashes, tests, a tag and a Telegram message.
  Adoption is not decided here.
- **The choice to make** (the creator's learning-rule item) remains the other half.

## Independent recompute (31 October 2026)
GPT and Gemini, each in a fresh chat, worked from per-world sums of the raw output only, without the analysis script
(`recompute_hd1.md`). **All three agree:** R 1.07% / 1.43% / 1.14%; h − v10 +0.0036 [0.0028, 0.0045]; sham +0.0007; supported.
GPT: this supports the measured outcome, not necessarily cumulative culture or autonomy.

**Final.** Next by the safe path in `CLAUDE.md`: a confirmatory run on new seeds, then both models on adoption.
