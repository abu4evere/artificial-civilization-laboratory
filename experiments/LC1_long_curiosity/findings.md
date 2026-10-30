# LC1 — Does curiosity slow the erosion over 1,000 years? Findings (final: recomputed blind by GPT and Gemini; see the end)

Frozen as `LC1-frozen` (operational note 1); decided and signed off in sleep mode (`docs/autonomous_decisions.md`).
No change to live nature: CU1's code (`code_cu1`) and runner, 1,000 years. Run on GitHub Actions (run 40838846290,
`skip_zero=local`). 96 worlds: v (v8), c (curiosity pull), x (sham), on the same 32 paired seeds (20301–20332). LP (80
founders, 80×80). Every number comes from `analyse_lc1.py`, written before data; full tables are in `results.md`.

**Validity:** zero checks pass; all 96 worlds present under one fingerprint (`code_cu1`); `tried` equals own updates
(mismatches 0). **Noted in the open:** one of 20 cloud chunks (chunk 4) was cancelled by GitHub's 340-minute job limit
at 5 h 40 min, but all of its worlds had already been saved and uploaded; every one of the 96 output files is complete
(each world reached year 1,000 or died out; checked before the analysis was run).

**Population beside it:** died out by year 1,000: **v 12, c 7**, sham 12 (of 32). Mean living in years 800–999: **c ÷ v
= 1.46** (c about 104 against v about 70 by years 900–1,000).

## The answer

**Yes, in part: curiosity keeps skill, making and people at a clearly higher level for 1,000 years, but it does not
stop the erosion.**

### Primary — world-born adults' (20–40) crafting skill, years 800–999
| arm | skill | worlds / adult-years | − v [95%] |
|---|---|---|---|
| v (v8) | 0.0512 | 20 / 161,745 | |
| **c (curiosity)** | **0.0839** | 26 / 235,460 | **+0.0327 [+0.0232, +0.0434]** |
| x (sham) | 0.0474 | 20 / 171,672 | −0.0038 [−0.0109, +0.0028] |

**The frozen reading: "curiosity holds skill higher"** (the lower bound +0.023 is above the +0.012 margin). Skill is
about 64% higher after 1,000 years. Survivor-weighted: more c worlds are alive to contribute (26 against 20).

### Slower erosion, or a parallel shift?
- **In absolute terms, both fall by the same amount:** from years 100–199 to 800–999, v −0.184, c −0.185 (difference
  −0.002 [−0.018, +0.014]). Curiosity does **not** stop the fall.
- **In relative terms, c falls more slowly:** the log-skill slope per century is −0.17 in c against −0.22 in v and the
  sham (described). c starts higher and stays higher, century after century.

| years | skill v / c | mean living v / c | making per adult-year v / c |
|---|---|---|---|
| 0–100 | 0.439 / 0.481 | 120 / 108 | 0.217 / 0.313 |
| 400–500 | 0.083 / 0.115 | 54 / 81 | 0.019 / 0.034 |
| 900–1,000 | 0.049 / 0.083 | 70 / 104 | 0.014 / 0.028 |

### Secondaries (years 800–999)
- **Making per adult-year:** v 0.014, c − v **+0.015 [+0.011, +0.019]** (about twice as much).
- **Made things held per adult:** v 0.22, c − v **+0.15 [+0.04, +0.25]**.
- **Flags: none.** Fewer c worlds die out (7 against 12), and c's populations are larger late on.

## Against the prior (the assistant's, frozen)
1. "The gap persists, but both arms erode": **right**, and the gap is larger than expected ("holds skill higher", not
   "not shown").
2. "No flags": **right**; survival and population are better with curiosity.
3. "Erosion slows somewhat in c": **partly right**: the same absolute fall, a slower relative fall.

GPT gave 55% that curiosity would meet the lasting-improvement threshold; it did.

## What it means
- **Curiosity's gain is not a short-term blip.** After 1,000 years, curious worlds have more skilled people, more
  making, more things, larger populations and fewer extinctions. This strengthens the case for the curiosity pull as
  nature v9 (the creator decides).
- **But it is not the ratchet.** Skill still falls by the same absolute amount from century 2 to century 10. Something
  else still pulls knowledge down over generations (LS1: it goes with the dead; children start from zero). Curiosity
  raises the floor; it does not make knowledge build up.

## Independent recompute
Pending: GPT and Gemini, fresh chats, raw per-world numbers. Recorded only from their actual replies.

## Independent recompute (29 October 2026)
GPT and Gemini, each in a fresh chat, worked from raw per-world numbers only, without the analysis script
(`recompute_lc1.md`). **All three agree:** late skill c − v +0.0327 (curiosity holds skill higher); the same absolute
fall (−0.0018); extinct 12 / 7 / 12. Population: averaged over surviving world-years c ÷ v = 1.165 (both models);
counting died-out worlds as 0 (this study's definition) 1.462; explained in `recompute_lc1.md`.

**Final.**
