# PG0 — Does curiosity find useful things, and what does a new thing's zero start cost? Findings (final: recomputed blind by GPT and Gemini)

Frozen as `PG0-frozen` (operational note 1); decided and signed off in sleep mode (`docs/autonomous_decisions.md`). Run
on GitHub Actions (run 40607486899, `skip_zero=local`). 32 worlds on nature v7, LP, seeds 19501–19532, 200 years. Mean
living population 124.7. Every number comes from `analyse_pg0.py`, written before data; full tables are in
`results.md`.

**Validity:**
- zero checks pass (the wrappers and observer are read-only; reload is exact);
- all 32 worlds are present under one fingerprint (`code_v7`);
- mismatches 0. The planned puzzle-branch replay check was not built (operational note 1).

## The answer

**A person's own past experience carries real information about what a brand-new thing will do.** Today's mind does
not use it: every new kind starts at worth 0. Curiosity-led play exists but is very rare.

### Q3 — Is information available? (primary for the next step; 85,136 first uses of a kind with ≥ 5 past uses)

| predictor at first use | mean absolute error [95%] |
|---|---|
| **own past uses, nearest in property space (k = 5)** | **0.0717 [0.0707, 0.0726]** |
| the same, properties shuffled (control) | 0.1053 [0.1042, 0.1065] |
| zero start (today's mind) | 0.1522 [0.1498, 0.1548] |

- **Shuffled minus property error: +0.0337 [+0.0329, +0.0343].** Information is available.
- **72,460 first uses had fewer than 5 past uses for that purpose.** No prediction was possible there; that is
  experience too thin to generalise from.
- **As GPT cautioned,** this shows the information exists in each person's experience, not that today's mind can learn
  it. Because usefulness is an exact formula of the properties, the result also depends on people perceiving properties
  as they are, which is a design question for any later law.

### Q1 — Curiosity (397,147 plays)
- **Puzzle-led play** (the leading thought is a puzzle about a made thing) is **291 plays: 0.07%.**
- **It finds new-to-world kinds a little more often:** 0.138 per play against 0.101, a difference of **+0.037 [+0.003,
  +0.073]** (described, not causal).
- **Those kinds are remade later** 0.30 [0.15, 0.48] of the time, against 0.22.
- **Every new kind counts as "useful"** under LS1's definition (some use's factor > 1), so that column does not
  discriminate.

### Q2 — The zero start
- **At first use,** worth is off by 0.160 on average.
- **Of 40,093 useful new kinds made in play, 0.252 are lost before their maker ever uses them:** 9,939 gone from hand,
  171 makers died. A kind that is never used can never prove its worth.
- **Once used, worth is learned fast:** 2.3 uses on average to come within 0.1 (142,129 person-kinds).

## Against the prior (the assistant's, frozen)
1. "Puzzle-led play under 20% of play, finds useful kinds at about the same rate": **first part right** (0.07%),
   **second wrong.** It finds slightly more.
2. "Most new useful kinds are lost before their maker uses them": **wrong** (a quarter).
3. "Property prediction beats shuffled clearly": **right.**

**GPT's framing** (information available, not learned) is confirmed in direction.

## What follows (from the frozen branches)
- **"Q3 shows information available: a property-learning capacity (PG1) has something real to learn."** Its design must
  first settle **how people perceive properties**, exactly or with error, because exact properties would be privileged
  knowledge (GPT). **That is the creator's question.**
- **Curiosity is rarely in charge of play** (0.07%). Directing it more (the "test by changing one thing" step) is a
  later candidate.
- **The quarter of new kinds lost unused** mostly vanish at the carry limit ("gone from hand"). OP1's law would leave
  them on the ground instead.

## Independent recompute (27 October 2026)
GPT and Gemini (on its third attempt), each in a fresh chat, worked from the raw counts only, without the analysis
script (`recompute_pg0.md`). **All three agree on every number:**
- led − free +0.0365;
- errors 0.0717 / 0.1053 / 0.1522;
- the gain +0.0337 [0.0329, 0.0343];
- lost before use 0.2522.

**Final.**
