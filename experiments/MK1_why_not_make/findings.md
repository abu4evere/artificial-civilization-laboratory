# MK1 — Why is making not chosen? Findings (recomputed independently by GPT and Gemini; final)

Frozen as `MK1-frozen` (with draft revision 1; operational note 1); run on GitHub Actions (run 40348264686). 32 worlds
on nature v7, LP (80 founders, 80×80), seeds 18201–18232, 200 years. Every number comes from `analyse_mk1.py` (written
before data); full tables are in `results.md`.

**Validity:**
- the zero checks pass;
- all 32 worlds are present under one fingerprint (`code_v7`);
- the observer's replay of every decision matched the decision exactly in every world (offer and worth-term
  mismatches 0);
- the softmax's own probability matches the observed choice rate in every bin (e.g. 0.0263 against 0.0263 in years
  0–5).

**Population:** 95 at the start, 132 in years 100–200. No world ended.

## The answer

**Making did not get worse. Everything else got stronger.** From years 0–10 to years 100–200 (adults, matched on
hunger, holding a tool and food on the tile):
- the chance of choosing to make when it was offered fell from 0.0232 to 0.0020;
- the mean log-odds fell by 3.12 [3.05, 3.19].

How that change splits, exactly:

| part of the change in log-odds | Δ | share |
|---|---|---|
| **the other options' soft maximum (U_other rising 1.30 → 1.94)** | **−3.20 [−3.28, −3.13]** | **1.03** |
| making's learned worth v (0.144 → 0.144) | −0.001 [−0.024, +0.022] | 0.00 |
| diligence, hunger, worth covariance | −0.002 | 0.00 |
| thought's pull | −0.05 | 0.01 |
| habit for making (rose) | **+0.13** | −0.04 |
| **total** | −3.12 | 1.00 |

(Exactness check: the parts add up to within 2 × 10⁻¹⁵.)

- **The part carrying the largest share is the other options.** Making's own score was the same at the end as at the
  start, and the habit for making rose, slightly offsetting the fall.
- 0.83 of the raw fall in "chosen given offered" remains within matched states. The rest comes from the mix of states.

### The offer gate (Q1)
- Making became feasible more often (0.24 → 0.82 of adult weeks) and was offered more often (0.50 → 0.82 of feasible
  weeks).
- When feasible but not offered, the reason was mostly that every feasible recipe's worth was at most 0.05 (0.67 → 0.93).
- When offered and not chosen, foraging won 0.48 → 0.40 of the time. Gathering rose (0.03 → 0.15), and putting things
  down rose (→ 0.09).

### Skill and worth (Q2, described; skill and worth cause each other)
- Within matched states, choosing to make rises with crafting skill. Standardised, it is 0.0006 for skill under 0.1
  and 0.0050 for 0.5+, eight times as often. v rises too (0.120 → 0.163).
- But the learned worth of the same kind 52 weeks after making is no lower for low-skill makers (relative −0.002 to
  +0.005).
- Forage tools made at every skill had similar factors (1.15–1.17).

### Does making pay? (Q4, an observational benefit-cost proxy, not a causal return)
- A forage tool made deliberately earned its maker 29 food in its first year in years 0–5, and 44 food in years
  100–200 (lifetime 34 → 52). One forage act's food (the cost of the making week) was about 19–22.
- **Proxy at 52 weeks: +10.5 early, +24.1 late.** By this measure, making paid more in the late period, when people
  made least.
- Low-skill makers' tools earned the most (53 food by 52 weeks for skill under 0.1, against 29 for 0.5+). This is
  probably because they had fewer other tools, but that was not tested.
- 0.45 of late tools were still held past 52 weeks. Tools stopped being followed mostly because their maker no longer
  held them (54,801), rarely because the maker died (2,033).

### The three hypotheses (all may hold)

| hypothesis | reading |
|---|---|
| **Low-skill trap** | **Weak.** Skill goes with choosing to make, but learned worth did not fall over time and is not lower for the same kind in low-skill hands. The decline is not carried by worth. |
| **Opportunity cost** | **Supported, in a specific form.** The other options' soft maximum carries the whole fall, and even the most skilled rarely make (0.005). But making does not pay less than foraging over a year (proxy > 0), so the "cost" is in the *scores* of other options, not in food. |
| **Delayed-benefit failure** | **Supported.** Tools pay about 1.5 (early) to 2.2 (late) times their cost within a year, while learned worth stays at about 0.14–0.15 and choosing to make falls about twelvefold within matched states. What a tool gives over time is not what the decision sees. |

## Against the prior (Claude's, frozen)
1. "The gap is mostly the item worth term": **wrong.** Worth did not move; the other options carry it.
2. "Skill and learned worth are associated within matched states": **partly right** (v and choice rise with skill), but
   worth of the same kind does not differ by skill.
3. "A forage tool pays over a year even for low-skill makers": **right** (the proxy is largest for low skill).

**The debate's predictions, recorded before the data** (`debate_round1.md`): GPT and Gemini both predicted that the
rise of the other options' soft maximum would carry the fall. **They were right.**

## What follows (frozen branches)
- **Delayed-benefit failure is supported** ("making pays but is not chosen"): fly-brain step 3 (how worth is learned,
  on which timescale) becomes relevant.
- **Opportunity cost (here, rising scores of the other options)** carries the decline. **Not tested and next to
  read:** which options' scores rose, and why. Candidates, as hypotheses only:
  - habits for those actions rising through copying (C4);
  - more option entries as more people are near, since every nearby person adds give, talk, court and take options to
    the softmax's sum;
  - more food on the tile.
  A read-only follow-up can split U_other's rise by action and by the number of entries.
- **The low-skill trap is weak**, so handing tools to children (the giving candidate) would not by itself raise
  making. It may still matter for tools in use (TF1, and GPT's prediction in debate round 3).

## Independent recompute (27 October 2026)
GPT and Gemini, each in a fresh chat, from the raw rows only, without the analysis script (`recompute_mk1.md`).

**All three agree on every key number:**
- the log-odds change, −3.119983;
- its −U_other part, −3.203736 (102.7%);
- v, 0.143778 → 0.143844;
- U_other, 1.296 → 1.937;
- the matched rate, 0.023215 → 0.001989.

One difference (tools' food by 52 weeks in years 100–200: 45.59 against 44.44) comes from adults only against all
makers, as checked. **Final.**
