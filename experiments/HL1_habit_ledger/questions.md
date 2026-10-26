# HL1 — Where do the habits come from? The habit ledger (frozen plan)

**Read-only on nature v7. No change to nature.** From debate round 7 (`docs/debate_habits_or_lessons_2026-10-27.md`):
GPT's design, adopted by Gemini.

CO1 (final) found that learned habits carry 0.86 of the rise in the other options' pull, which is what makes making lose
(MK1). It did not find where those habits come from. GPT's leading hypothesis (not a finding): "social learning might be
transmitting behavioral conservatism more effectively than technological knowledge".

## How habits change in `code_v7` (read from the code)

Each person holds a habit value q for every situation × action (32 × 19). It changes only by these routes:

| route | where | form |
|---|---|---|
| **own experience (TD)** | `biology._learn`, every week | q ← q + 0.05·(r + 0.8·future − q), for the action just done in its situation |
| **copying in talk** | `actions._imitate` | q ← q + rate·(model's q − q) for the whole table, when the learner respects the model (≥ 0.2) or the model seems happier |
| **carer's ways** | `biology._upbringing`, every 4 weeks for children under 12 on the carer's tile | q ← q + 0.08·(carer's q − q) |
| **birth** | `biology._born` | a child starts at 0.25 × (mother's + father's) q |
| **paid back** | `actions._give` | +0.025 to the giver's "give" habit when a gift is paid back |

Every update is clipped to [−1.5, 1.5].

## The exact ledger (written before data)

For every person and every habit entry, the observer keeps **components by route**, which always add up to the value:

q = C_TD + C_talk + C_carer + C_birth + C_paid + C_clip.

- An update of the form q ← q + k·(target − q) shrinks every existing component by (1 − k) and adds k·target to its
  own route.
- An additive update (paid back) adds to its route.
- Anything removed by clipping goes to C_clip.

This is accounting of how each value **arrived**, not of whose experience it ultimately came from. A value copied in
talk counts as talk, even if the model learned it by TD.

## Questions (LS1's bins up to 200 years; worlds alive at each bin's start; population beside every measure)

**Q1. Which route carries CO1's habit rise (primary).** In every person-week in which "make" is offered (adults, as
CO1), the habit part of the competing pull, Σ_a s_a · h_a (h_a = 0.6 × the habit value, s_a = the family's share of
the competing weight, exactly as CO1), splits exactly by route. From years 0–10 to years 100–200, matched as CO1
(hunger × tool × food, late weighted to the early offered weeks), the change in that habit part is split into own TD,
talk, carer, birth, paid back and clip. **The route carrying the largest share is named.** World bootstrap (10,000
replicates). Making's own habit term is split the same way.

**Q2. The raw flows.** By bin and action family: the total change in habit values by route, and the number of updates.

**Q3. Rich-get-richer.** By bin and action family:
- how often the action is chosen (share of adult person-weeks);
- the number of TD updates;
- the mean reward r and future term in those updates;
- the mean TD target.

Make against forage, give, talk and gather.

Then, across worlds and families, the rank association between how often an action was chosen in years 0–20 and the
growth of its habit from years 0–20 to years 100–200. **The negative test:** does making's habit gain anything through
talk, while it gains almost nothing through its own TD (practice starvation)?

**Q4. Social amplification.** In copying events:
- by action family, the mean difference between the model's habit and the learner's;
- the total change copied;
- how often the model was copied for respect, against for seeming happier.

Do copied habits favour the common actions over making?

## What would follow (stated now; not exclusive)

- **Talk copying carries the largest share** of CO1's habit rise: habits spread socially and crowd out making. A
  candidate for a later, frozen intervention study (how habits are copied, C4: one situation, or the whole table) is the
  creator's to decide. Fly-brain gap 4 becomes relevant.
- **Own TD carries it:** people learn from their own rewards that common actions pay. Then the question is the reward
  signal and timescale (making's delayed benefit, MK1). Fly-brain step 3 becomes relevant.
- **Carer or birth carries it:** habits are inherited down generations. That is a developmental question.
- **The negative test holds** (making gains almost nothing by TD because it is rarely done): practice starvation
  confirmed, a rich-get-richer loop.

## The assistant's prior (separate predictions)

1. **Talk copying carries the largest share** of the habit rise in U_other (over half). Own TD is second.
2. Making's habit gains more through copying than through its own TD. It is rarely done, so it is rarely updated by TD.
3. Common actions (forage, give, talk) are chosen far more often early, and their habits grow most (positive rank
   association).
4. Models copied hold higher forage and give habits than the learners who copy them.

**On record from the debate:**
- GPT's leading hypothesis: social learning transmits behavioural conservatism.
- Gemini: TD frequency asymmetry may lock out rare actions.

## Validity (hard stops)

- **Zero checks:**
  - the observer and wrappers are read-only: state and random numbers identical with and without them, at 20 and 60
    years;
  - reload is exact.
- **The ledger closes:** at every decade boundary, for every living person and every entry, |q − Σ components| < 10⁻⁹
  (a mismatch counter that must be 0).
- **Every change to q is attributed:** at each decade, the sum of attributed changes equals the change in q.
- All 32 worlds are present under one fingerprint (`code_v7`).
- **An independent recompute by GPT and Gemini** (fresh chats, raw files, no analysis script) of Q1's split and its
  largest route, and of Q3's make TD updates against forage, before the findings are final.

## Setting

Nature v7, LP (80 founders, 80×80), 32 new seeds (18601–18632), 200 years, run on GitHub.

## Sign-off (27 October 2026)

The creator: "yea draft it, approve and freeze", on this plan (debate round 7: GPT's design, adopted by Gemini). Frozen as
`HL1-frozen` before any code or data. How the code reads choices the text leaves open goes in operational notes,
appended before any data.

## Operational note 1 (27 October 2026, after freezing, before any data)

How the code (`run_hl1.py`, `analyse_hl1.py`) reads the text where it left a choice, found in a 15-year smoke world
(seed 9951, not data):
1. **Clipping.** Each route's update is clipped to [−1.5, 1.5] inside the code itself. The ledger therefore adds a
   clipped update's actual change to the route that made it, rather than keeping a separate C_clip. How often a TD
   update would have passed the bound is counted, and reported with Q3. (In the smoke world it never did.) The ledger
   still closes exactly.
2. **Inferring the copying rate.** For copying in talk and the carer's ways, the rate k is read from the change itself:
   k = (new − old) / (model's or carer's value − old), at the first entry where they differ. Every entry is then
   accounted with that k. The ledger's closure checks that this is exact.
3. **The TD replay.** The observer recomputes each weekly update's reward r and future value exactly as `_learn` does,
   and checks the result against the update (a mismatch counter that must be 0). In the smoke world it was 0.
4. **Q1** reads adults (16+), as CO1. **Q3's** learning counts, rewards and future values are adults only, so they
   compare with adults' choices. **Q2's** flows count everyone aged 1+ (habits are learned from age 1).
5. **Mean habit values** (Q3) are sampled every 4 weeks over adults, averaged over the 32 situations.
6. **Seeds** 18601–18632.
