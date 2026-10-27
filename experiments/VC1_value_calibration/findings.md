# VC1 — Are habits calibrated? Findings (recompute by GPT and Gemini pending; not yet final)

Frozen as `VC1-frozen` (operational note 1); decided and signed off in sleep mode (`docs/autonomous_decisions.md`). Run
on GitHub Actions (run 40491681638, `skip_zero=local`). 32 worlds on nature v7, LP (80 founders, 80×80), seeds
19001–19032, 200 years. Every number comes from `analyse_vc1.py`, written before data; full tables are in `results.md`.

**Validity:**
- zero checks pass;
- all 32 worlds are present under one fingerprint (`code_v7`);
- every adult TD update (about 22.8 million) replays exactly (mismatches 0).

## The answer

**The habit values are miscalibrated, in opposite directions:**
- **late on, they over-value the common actions;**
- **they under-value making;**
- **yet making's realised returns are almost the same as the alternatives'.**

The habits rank making about 1.1 below the common actions. The returns people actually get afterwards rank it about
0.01 below.

### Q1 — Calibration bias, q − G (adults; years 100–200)

| action | updates | mean q | mean realised G | bias q − G |
|---|---|---|---|---|
| **make** | 8,929 | 0.046 | 0.604 | **−0.558 [−0.571, −0.543]** |
| forage | 4,827,401 | 1.178 | 0.738 | +0.440 |
| give | 1,157,022 | 1.377 | 0.906 | +0.471 |
| talk | 1,523,234 | 1.149 | 0.790 | +0.359 |
| gather | 2,235,440 | 0.865 | 0.484 | +0.381 |
| **common, pooled** | 9,743,097 | 1.125 | 0.708 | **+0.418 [+0.406, +0.429]** |

**Make's bias minus the common actions' bias: −0.975 [−0.990, −0.958].**

**Over time:**
- In years 0–50, every action is under-valued: common −0.36, make −0.60. Habits were still rising.
- Common actions cross over to over-valued after year 50: +0.15, then +0.42.
- Make stays under-valued throughout: −0.60, −0.57, −0.56.

### Q2 — The max part
The max look-ahead's optimism, 0.8 × (max q[s′] − q[s′, a_next]), is 0.145 for the common actions late. That is
**0.35 of their bias.** It is 0.124 for make.

**Most of the common actions' over-valuation is not the max.** The rest comes from what HL1 found sets habits besides
own learning: copying in talk (0.41 of the habit rise) and carers. This study does not split it.

### Q3 — Does making pay more?
Realised G of make minus the other actions in the same situation (weighted by make's updates per situation):

| era | difference [95%] |
|---|---|
| 0–50 | −0.041 [−0.048, −0.034] |
| 50–100 | −0.017 [−0.025, −0.008] |
| 100–200 | −0.011 [−0.019, −0.003] |

Making's realised returns are **slightly below** the alternatives', and the gap narrows over time.

**Caution:** G sums 31 weeks of everything a person does next, so it is dominated by what follows, which is mostly the
same for every action. Differences in G are therefore small by construction. What is clear is the contrast:
- the realised difference is about 0.01;
- the habit difference is about 1.1.

### Q4 — Slope and coverage
- **Common actions:** G rises with q only weakly. The slope is 0.39 and the correlation 0.43, against 1 for calibrated
  values. The spread of q is over-confident.
- **Make** (8,929 updates late, against 9.7 million for the common actions): slope 0.45, correlation 0.10.
- The next-week link holds for 0.80–0.91 of updates; 0.02 are censored by death.

## Against the prior (the assistant's, frozen)
1. "Common actions over-valued by at least 0.2, late": **right** (+0.418).
2. "Over half of that bias is the max gap": **wrong** (0.35).
3. "Make's bias lower than the common actions'": **right** (−0.558 against +0.418).
4. "Make's realised G within situations not above the alternatives'": **right** (−0.011).

**GPT's prediction** ("reasonably consistent values for frequently performed actions but weakly supported estimates
for making"):
- **wrong for the frequent actions:** they are over-valued by 0.42, with slope 0.39;
- **right that making is weakly supported:** 8,929 updates, correlation 0.10.

## What follows (from the frozen branches; more than one applies)
- **"Common actions over-valued, mostly through the max gap":** over-valued, yes; mostly through the max, **no**
  (0.35). An Expected-SARSA change would address about a third of the over-valuation, on calibration grounds.
- **"Making under-valued, and making's realised returns at least those of the alternatives":** under-valued, yes
  (−0.56). Its returns are **not** at least the alternatives', though they are within 0.011.
- **"Making's realised returns below the alternatives: people are right not to make":** strictly, yes by 0.011. But
  the habits put it 1.1 below, about a hundred times the real difference. So **people are right in direction but wrong
  in size**, and the size is what decides the softmax choice at T = 0.2.

**Reading (interpretation, not tested):**
- The miscalibration that matters is the common actions' **over-valuation** (+0.42) together with making's
  **under-valuation** (−0.56).
- The first comes mostly from beyond the max look-ahead: copying and carers spreading inflated values (HL1).
- The second comes from practice starvation: making's value is rarely updated, so it stays near its start.

**Any change to the learning or copying rule would now be justified on calibration grounds, not on making.** That is
the creator's decision, one law at a time.
