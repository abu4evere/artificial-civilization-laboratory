# VC1 — Are habits calibrated? The value-calibration audit (frozen plan)

**Read-only on nature v7. No change to nature.** Chosen in sleep mode (`docs/autonomous_decisions.md`, 27 October 2026),
after MO1. Both GPT (75%) and Gemini (95%) chose it first (debate round 11, `docs/debate_after_mo1_2026-10-27.md`). It is
GPT's stated precondition for any learning-rule change.

HL1 found that own TD learning and copying lift every often-done action's habit towards a ceiling set by the 0.8
discount, while making is starved of practice. It did not find **whether those habit values are right**: whether they
match the returns people actually go on to get.

## The rule (`biology._learn`, read from the code)

Each week, for the action just done in its situation:

q[s, a] ← q + 0.05 · (r + 0.8 · max_a′ q[s′, a′] − q), clipped to ±1.5,

where:
- **r** = the week's reward + 2 × the change in mood;
- **s′** is the situation at the week's end.

**Two different things q could be compared with** (GPT's correction):
1. **The realised return** under the behaviour actually followed: G = Σ_k 0.8^k r_{t+k}, the discounted sum of the
   person's own later weekly rewards (r as above).
2. **The max-bootstrap target**, which aims at the best next action, not the one actually chosen.

These differ, so a gap between q and G alone does not prove the rule is wrong. The max part's optimism is measured
separately, as 0.8 × (max_a′ q[s′, a′] − q[s′, a_next]), where a_next is the action actually chosen next week (the
sample Expected-SARSA counterpart).

## Logged (read-only: a wrapper on `biology._learn` that replays the update exactly, as HL1's)

For every weekly update of an adult (16+), the observer records:
- the action and situation;
- the era (years 0–50, 50–100, 100–200);
- q before the update;
- r, and the TD target.

Then, as the person's later weeks pass:
- **the realised return G**, summed until the weight falls below 0.001 (31 weeks), or until death. Death ends the
  rewards; it is counted as censored;
- **the max gap**, from the next week's update.

These go into cells (era × action) as sums of q, G, q², G², qG, the max gap, n and censored n. They also go into cells
by situation, for the matched comparison of Q3.

## Questions (primary: adults; population beside every measure; world bootstrap, 10,000 replicates)

**Q1. Calibration bias (primary).** By action and era: the mean of q − G. For make, forage, give, talk and gather.

**Named:** whether make's bias differs from the common actions' bias (forage, give, talk, gather pooled), years
100–200. Is making under-valued (q below G) while common actions are over-valued (q above G)?

**Q2. The max part.** The mean max gap, 0.8 × (max q[s′] − q[s′, a_next]), by action and era. **The share of each
action's bias that the max gap accounts for** (gap / bias).

**Q3. Does making actually pay more?** Realised returns G of make against the other actions **in the same situation**:
the difference within situation, weighted by make's updates per situation, early and late.

**Q4. Calibration slope and coverage.** By action:
- the regression slope of G on q (1 = calibrated, below 1 = over-confident spread);
- the correlation;
- n.

Make's coverage, its count of updates, is reported beside every make number.

## What would follow (stated now; not exclusive)

- **Common actions over-valued, mostly through the max gap:** the bootstrapped max inflates. An Expected-SARSA study
  (C), judged on calibration, gains a calibration-based justification (not an outcome one).
- **Values calibrated** (bias near 0 for all actions): the rule learns what it should. The problem is exploration and
  practice: candidate (E), the exploration audit.
- **Making under-valued** (q below G) **and** making's realised returns at least those of the alternatives in the same
  situations: the habit rule mis-values making specifically. The likely cause is practice starvation (few updates),
  which is then the target.
- **Making's realised returns below the alternatives:** people are right not to make. The tools' long-run pay (MK1)
  is not felt within the 0.8-per-week horizon. That is a timescale question (fly-brain step 3).

## The assistant's prior
1. Common actions' q is above G (over-valued), by at least 0.2, late.
2. Most of that bias (over half) is the max gap.
3. Make's bias is lower than the common actions' (closer to 0 or negative).
4. Make's realised G within situations is not above the alternatives' (the long-run pay is beyond the horizon).

**GPT's prediction (on record):** "reasonably consistent values for frequently performed actions but weakly supported
estimates for making".

## Validity (hard stops)
- **Zero checks:**
  - the observer is read-only: state and random numbers identical with and without it, at 20 and 60 years;
  - reload is exact.
- **The replay of every TD update matches the code** (a mismatch counter that must be 0).
- **The next-week link:** the share of updates whose next update's situation equals s′ is reported. The max gap uses
  only those.
- All 32 worlds are present under one fingerprint (`code_v7`).
- **An independent recompute by GPT and Gemini** (fresh chats, raw files, no analysis script) of Q1's bias for make and
  the common actions, and Q2's gap shares, before the findings are final. A recompute is recorded only from numbers read
  from the reply.

## Setting
Nature v7, LP (80 founders, 80×80), 32 new seeds (19001–19032), 200 years, run on GitHub.

## Sign-off (27 October 2026)
The assistant, under the creator's sleep-mode autonomy (CLAUDE.md, Sleep mode). Both models chose this study (GPT 75%,
Gemini 95%); the assistant's estimate is 65%, above the 40% threshold. Logged in `docs/autonomous_decisions.md`. Frozen
as `VC1-frozen` before any code or data. How the code reads choices the text leaves open goes in operational notes,
appended before any data.

## Operational note 1 (27 October 2026, after freezing, before any data)

How the code (`run_vc1.py`, `analyse_vc1.py`) reads the text where it left a choice, found in a 20-year smoke world
(seed 9943, not data):
1. **r** is the reward the update itself uses: the week's reward + 2 × the mood change, replayed exactly as `_learn`.
   **G** starts with that week's r and adds 0.8^k × r of the person's next weekly updates. Weeks without an update (no
   action recorded) add nothing.
2. **G is closed** once the weight 0.8^k falls below 0.001 (31 updates later), at death (counted as censored: rewards
   end), or not at all if the run ends first. Those still open at the end are excluded; their number is in each output
   file.
3. **The max gap** is 0.8 × (max of q[s′] at the update − q[s′, a_next] from the same snapshot). a_next is the action of
   the person's next update, used only when that update's situation equals s′; the "next-week link" share is reported.
4. **"Common actions"** are forage, give, talk and gather, pooled.
5. **Q3** compares G of make with G of all other actions pooled in the same situation (one of the 32), within era. The
   difference per situation is weighted by make's updates there.
6. **Bootstraps** resample whole worlds (10,000 replicates) and pool sums.
7. **Seeds:** 19001–19032.
