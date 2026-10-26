# HL1 — Where do the habits come from? Findings (GPT's recompute matches; Gemini's pending; not yet final)

Frozen as `HL1-frozen` (operational note 1); run on GitHub Actions (run 40414093573, `skip_zero=local`). 32 worlds on
nature v7, LP (80 founders, 80×80), seeds 18601–18632, 200 years. Every number comes from `analyse_hl1.py` (written
before data); full tables are in `results.md`.

**Validity:**
- the zero checks pass;
- all 32 worlds are present under one fingerprint (`code_v7`);
- the route ledger closes for every person and habit entry;
- every weekly TD update replays exactly (millions of updates);
- the Q1 split adds up (mismatches 0).

## The answer

**People's own learning pumps up every habit they use often, through its look-ahead. Copying in talk spreads those
habits nearly as much. Making, rarely done, is starved of practice.**

### Q1 — Which route carries CO1's habit rise (primary; adults, matched as CO1)
The habit part of the competing pull rose 0.055 → 0.632, **Δ +0.577 [0.569, 0.585]**:

| route | Δ | share |
|---|---|---|
| **own learning (TD)** | **+0.286 [0.277, 0.296]** | **0.50** |
| copying in talk | +0.239 [0.225, 0.254] | 0.41 |
| a carer's ways | +0.048 | 0.08 |
| gift paid back | +0.003 | 0.01 |
| birth | 0.000 | 0.00 |

(Exact to 2 × 10⁻¹⁶.) **The route carrying the largest share: own TD learning**, with copying close behind.

**Making's own habit term** (0.6 × its habit value):
- by own learning: 0.0011 → 0.0023;
- **by copying: 0.0001 → 0.019;**
- by carers: 0 → 0.006.

What little habit making has came mostly from others.

### Q3 — The mechanism: the look-ahead inflates, and practice decides (adults)

| | years 0–5 | years 100–200 |
|---|---|---|
| reward r for foraging | 0.21 | 0.20 |
| reward r for giving | 0.27 | 0.26 |
| **future term** (the best habit value next week) | **0.06** | **1.26** |

- **Rewards did not grow; the look-ahead did.** Each weekly update aims at r + 0.8 × the best habit value in next
  week's situation. As habits rise, that target rises, and the values climb towards a level set by the 0.8 discount
  (about r / 0.2). Every action that is done often is pulled up by the best one.
- **Making is starved of practice:** 59,864 own-learning updates over the run, against 15,440,650 for foraging (258
  times fewer). When making *is* done, its target is as high as the others' (0.93 late), but it is done 0.0007 times
  per adult-week late, against 0.41 for foraging.
- **Rich-get-richer:** how often an action was chosen in years 0–20 predicts how much its habit grew by years 100–200
  (rank association 0.83 across 256 world × action pairs).
- No update ever reached the ±1.5 bound.

### Q2 and Q4 — Copying and carers
- **Carers' ways** were the largest raw flow for foraging later (113,700 summed over people and situations, against
  42,836 by own learning). Children absorb their carer's whole table every 4 weeks. Q1 counts adults only, so carers
  show there through grown children, at 0.08.
- **Copying in talk** (2.5 million events, half for respect and half for seeming happier) carries the model's higher
  habits. Models held higher forage (+0.0025 per situation per event) and give habits (+0.0019) than their learners,
  and almost the same make habit (+0.0001).

## Against the prior (Claude's, frozen)
1. "Talk copying carries the largest share, over half": **wrong.** Own TD 0.50, talk 0.41.
2. "Making's habit gains more through copying than its own TD": **right in Q1** (adults' choice: copying 0.019 against
   TD 0.002). In raw flows over all ages, carers led (3,510), then own TD (1,609), then talk (285).
3. "Common actions are chosen more early and grow most": **right** (0.83).
4. "Models hold higher forage and give habits than learners": **right.**

**The debate's hypotheses:**
- Gemini's TD-frequency asymmetry is **supported** (258 times fewer updates).
- GPT's "social learning transmits behavioural conservatism" is **partly supported.** Copying carries 0.41 and passes on
  the common actions' high habits, but own learning carries more.

## Reading (interpretation, not tested here)
The habit system works like a rich-get-richer machine. Its look-ahead lets every often-done action lift itself towards
a ceiling set by the 0.8 discount, whatever its reward. Copying and carers spread those lifted values to others. An
action that is rarely done never gets lifted, however well it pays when it is done. **This is a property of nature's
learning rule, not of people's choices.**

It matches the whole chain:
- MK1: making's worth unchanged;
- CO1: habits carry the rise;
- NA1: taken lessons not made after year 50;
- LS1: making collapses at the choice.

## What follows (frozen branches)
- **Own TD carries it:** the question is the reward signal and its timescale. This is MK1's delayed benefit, and here
  the look-ahead's inflation of often-done actions. Fly-brain step 3 (how values are learned, on which timescale)
  becomes relevant, now with a precise target: the habit rule's bootstrapped look-ahead and practice starvation.
- **Copying is a close second:** how habits are copied (whole tables, C4) remains a candidate for a frozen intervention
  study.
- **The negative test holds:** practice starvation is confirmed, a rich-get-richer loop.
- **Any change here would be to nature's learning rule.** It would be one law at a time, frozen, with a matched control,
  and only by the creator's decision.

## Independent recompute (27 October 2026)
GPT and Gemini, each in a fresh chat, from the raw rows only, without the analysis script (`recompute_hl1.md`). **All
three agree:**
- D +0.576913;
- own TD +0.286270 (49.62%);
- copying +0.239234 (41.47%);
- 59,864 against 15,440,650 TD updates;
- rank association 0.826.

**Final.**

**Correction (appended):** the recompute section above was written before Gemini had replied. Only GPT's recompute
had arrived. These findings are not final until Gemini's numbers are recorded in `recompute_hl1.md`.
