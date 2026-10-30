# LS2 — Where does knowledge go under nature v9? Findings (final: recomputed blind by GPT and Gemini; see the end)

Frozen as `LS2-frozen` (operational note 1); signed off by the creator ("yea draft it and run on github"). Read-only:
LS1's observer, ledger and analysis on `code_v9` (live nature v9, the curiosity pull). Run on GitHub Actions (run
40991857659, `skip_zero=local`). LP only: 40 worlds (seeds 20401–20440), 80 founders on 80 × 80, 1,000 years. Every
number comes from `analyse_ls2.py` (LS1's analysis, written before data); full tables are in `results.md`.

**Validity:** zero checks pass; all 40 worlds present under one fingerprint (`code_v9`); the ledger, kind counts and
holdings match in every world (every mismatch count is 0).

**Population beside it:** 101 people at the start, 123 in years 100–200, 96–104 in years 300–700, 146 in years
900–1,000 (worlds alive at each bin's start). 28 of 40 worlds lived to year 1,000 (12 ended between years 117 and 931).
**Comparison with LS1 (v7) is described, not tested:** different seeds, the same design. LS1: 51 of 64 lived to year
1,000; 102 people in years 900–1,000.

## The answer

**Under v9 the leak is where it was under v7.** Knowledge goes with the dead (0.98), it is not replaced, and making
collapses at the choice: people who can make, and weigh making, choose something else. Curiosity changed the levels,
not the shape.

### Q1 — Where copies and kinds are lost (after year 100)
- **Copy loss: death 0.980** [0.978, 0.982] of 487,257 losses; push-out 0.020; forgetting as useless 0. (LS1: 0.979.)
- **Kind extinction: death 0.979** [0.976, 0.981] of 50,086 extinctions. (LS1: 0.979.)
- **Net flow:** positive to year 100, negative from year 100 to 800 (−29 per 1,000 person-years at worst, shrinking),
  then about 0 (+0.1, +1.4). By the frozen rule it **never** turns negative and stays negative: the stock shrinks after
  year 100, then levels off.
- **Inflow by invention** falls from 302 per 1,000 person-years (years 5–10) to 0.5 (years 900–1,000) (LS1: 0.1).
  After year 300, inflow is almost all rediscovery and teaching.

### Q2 — Origin, transmission, persistence (useful kinds)
| origin, era | kinds | ever held by 2+ | held 25 years after the maker's death | held 2+ generations after |
|---|---|---|---|---|
| founder, years 0–100 | 4,878 | 0.651 | 0.432 | 0.590 |
| world-born, years 0–100 | 22,475 | 0.304 | 0.128 | 0.257 |
| world-born, years 100–1,000 | 10,345 | 0.135 | 0.025 | 0.101 |

As on v7 (0.73 / 0.55 / 0.69; 0.30 / 0.14 / 0.25; 0.12 / 0.03 / 0.08): founders' know-how is kept far more often than
what the world's own people invent, and what is invented later is kept least. Founders' share of useful know-how held
in years 0–100: 0.733 [0.719, 0.746] (LS1: 0.73).

### Q3 — The making funnel (adults)
From years 0–10 to years 100–200, making per adult person-week fell by Δ ln **−1.736** (LS1: −1.93):
- **feasible:** Δ ln +0.765 [0.732, 0.799] (it rose);
- **weighed given feasible:** Δ ln +0.387 [0.357, 0.418] (it rose);
- **chosen given weighed:** Δ ln **−2.887** [−2.97, −2.80], **share of the decline 1.66** [1.62, 1.72] (LS1: 1.57).

**The gate carrying the largest share: chosen given weighed.** Chosen given weighed was 0.0367 in years 0–5 and
0.0018 in years 100–200 (about 1 in 560; LS1: 1 in 800), then 0.0010–0.0011 to year 1,000. When making was weighed and
not chosen (after year 100), foraging won 0.67 of the time, then gathering 0.10, putting things down 0.09.

### Q4 — The fall in tools' food (26 worlds alive at year 1,000)
A4 = s × g × k fell by Δ ln −2.335: **s, the share of forage acts with a tool, 0.588 → 0.051, share 1.05**; g (food
per tool act) 21.3 → 21.5; k (the tool's share) 0.119 → 0.132. Tools work as well as ever; almost nobody uses one. In
decades 2–4, tools used were made by the holder 0.559, by someone else 0.064, unknown 0.376 (LS1 on v7: 0.98 by the
holder; v8's things left on the ground can now be picked up). A lost forage tool was replaced within a year 0.64–0.74
of the time in years 0–20, 0.196 in years 100–200, 0.12–0.14 after year 300 (LS1: 0.07 after year 400).

### Q5 — Does each generation take up what it inherits? (world-born, by birth cohort)
- **Inheritance rate:** **0.391** [0.385, 0.398] for people born in years 0–50 (6,057 people); **0.317** for 50–100;
  **0.293** for 100–150; then **0.24–0.27** in every later cohort. It falls, then holds; it never rises. Pooled over
  everyone born from year 100 on: 138,544 / 529,328 = 0.262 (summed from the recompute file; checked separately, as in
  LS1). (LS1: 0.41, 0.32, 0.29, then 0.26–0.29; pooled 0.2775.)
- How it was inherited: taught 0.22 early, 0.32–0.36 late; own making 0.62–0.67 throughout.
- Useful recipes acquired by 30: 14.85 (born 0–50) → 7.49 (150–200) → 3.08 (950–1,000) (LS1: 14.5 → 7.3 → 2.1).
- Of recipes got from others, the share later made: 0.151 (born 0–50), then 0.03–0.05 (LS1: 0.10, then 0.02–0.03).
- Useful kinds invented by world-born people: 29,229; held by someone of a later generation: 0.192 (LS1: 0.19).

## Described: recipe against skill (GPT's addition, debate round 30)
| born (years) | useful recipes by 30 | crafting skill at 16 | at 30 | practice weeks |
|---|---|---|---|---|
| 0–50 | 14.85 | 0.483 | 0.521 | 44.2 |
| 100–200 | 9.13 / 7.49 | 0.196 | 0.219 | 13.6 |
| 400–600 | 4.27–3.60 | 0.083 | 0.099 | 6.0 |
| 900–1,000 | 3.12 / 3.08 | 0.065 | 0.082 | 4.7 |

(Recipes are from Q5's 50-year bands, 100–150 / 150–200 and 900–950 / 950–1,000.) **Both fall, and the skill falls
somewhat more:** recipes by 30 to about a fifth, skill at 30 to about a sixth, practice weeks to about a tenth. People
know some recipes and rarely make them (later made 0.03–0.05), so technique is not practised. LS1 on v7: skill at 16
0.45 → 0.04, practice weeks 39 → 2.5. Under v9 the late levels are higher (skill 0.065 against 0.04; practice 4.7
against 2.5 weeks), the curiosity pull's gain, but the shape is the same.

The habit value for "make" at 16 rises by cohort (0.0068 → 0.0482) and equals the carer's and talk partners' to three
decimals, as on v7. Teaching: lessons offered per person-year rise to 3.56 in years 10–20, then fall to 0.31; the share
taken is low (0.03–0.13); of lessons taken, the share later made falls from 0.41 to 0.05–0.07.

## Against the prior (the assistant's, frozen)
1. "Death is still the dominant channel": **right** (0.980 copies, 0.979 kinds).
2. "Making's decline still carried mostly by the choice gate, but less than on v7": **right that it is the choice
   gate; wrong that it is less.** Its share is 1.66 (LS1 1.57). The total decline is smaller (−1.74 against −1.93), and
   chosen given weighed stays higher (1 in 560 against 1 in 800 in years 100–200), but the choice still carries it all.
3. "The inheritance rate is low and falls over cohorts": **right** (0.39 → 0.25).

## What follows (LS1's frozen branches, applied)
- **Q3's largest share is "chosen" and Q5's rate is low:** each generation does not use what it could make. Next, as
  frozen: how forager children come to make and use tools (apprenticeship, necessity, worth), before any change to
  nature.
- **Kind extinction is mostly death:** knowledge is not passed on before its holder dies. Next: transmission.
- **Q4's fall is carried by s:** tools are not remade or replaced; the tool lifecycle is the leak.
- Copy loss is not push-out (0.02): memory is not the leak.
- **Timing:** the choice to make collapses first (chosen given weighed 0.037 → 0.012 by years 20–50), with replacement
  (0.72 → 0.51 by years 20–50); skill and practice fall by cohort after it.

**For the next steps (the creator's order, 30 October):**
- **Ageing:** knowledge goes with the dead, and a read-only count on 6 throwaway v9 worlds (not this study's data;
  `docs/research/acl_lifespan_v9_2026-10-30.md`) shows world-born adults dying at a mean age of 42. Longer, realistic
  lives would keep holders alive longer; whether that keeps knowledge is the ageing study's question.
- **Apprenticeship:** watching making could pass technique, but LS2 says the deepest gate is the choice to make. A
  technique law alone may raise skill without raising making; the apprenticeship study should keep making as a
  secondary and read it.

**Read with care:** Q1's shares say *when* copies and kinds are lost (when the holder dies), not that death causes the
loss. Q3 places the fall at the choice; it does not show why the choice changes. The LS1 comparison is described only.

## Independent recompute
Pending: GPT and Gemini, fresh chats, from raw per-world numbers (`recompute/ls2_one_file.csv`). Recorded only from
their actual replies.

## Independent recompute (30 October 2026)
GPT and Gemini, each in a fresh chat, worked from raw per-world sums only, without the analysis script
(`recompute_ls2.md`). **All three agree:** death carries 0.9802 of copy loss and 0.9790 of kind extinction; the choice
gate ("chosen given weighed") carries 1.6636 of the decline in making; inheritance 0.3914 / 0.3172 / 0.2933 for the
first three cohorts and 0.2617 pooled from year 100 on.

**Final.**
