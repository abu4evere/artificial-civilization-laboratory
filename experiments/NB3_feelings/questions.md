# NB3: feelings. Can a neural people live in the open world if it is born with human feelings? (frozen plan)

**Why:** NB2 (final: not viable) gave the neural brain every choice the body allows, and most worlds died out, even
with learning off.
- The old brain's thresholds ("attack only with a grudge", "give only from surplus") were quietly keeping people
  alive.
- The world rewards every attack: +0.1 of feeling, and a kill +0.3 × temper − 0.2 × kindness.

**The creator, 10 November 2026,** asked what feelings would be added, then said "go ahead check the data first then
add them".
- Humans do not live by intelligence alone. They are born with feelings that make harming others feel bad and caring
  feel good, before they learn anything.
- In ACL's terms these are **the body, not the decisions:** a feeling is a change in the weekly feeling number r. The
  brain still chooses; it feels the result.

**Frozen** as git tag `NB3-frozen`, before any NB3 code or data.
**Sign-off:**
- the creator's go-ahead to add the feelings, 10 November 2026 ("go ahead check the data first then add them");
- their standing instruction "do not ask me go ahead bro";
- "keep working i am going sleep keep up all projects" (11 November 2026).

**Council round 84:** `docs/debate_round84_after_2026-11-11.md` (GPT 25%, DeepSeek 35%; Gemini's tab failed).
**The scale audit:** `scale_audit.py` and `scale_audit.json` (throwaway seeds 9001–9002, read for scale only).

**What this plan waited for** (all now done):
- the autopsy NB2-A (what actually killed people), which sets which feelings come first;
- council round 84;
- the creator's standing go-ahead.

## What the autopsy NB2-A found (11 November 2026), and how it shapes this draft
- **Unprovoked violence is the new killer:**
  - killed is 17.7% of adult deaths in NB2 against 0.5% in v17, and 33% of teens';
  - 55–64% of attacks had no grudge, only 3% of attackers were hungry, and 20% of attacks hit children under 12;
  - the world rewards every attack.

  So feeling 0 (no joy in attacking) and feeling 6 (an inborn reluctance to harm, **strong at birth**) come first. Then
  empathy and guilt.
- **Sharing broke down:** about a quarter of those who starved had kin nearby with plenty, and children gave in 3% of
  weeks against 10%. So love of one's own child, empathy, and approval for helping.
- **Even the sham with learning off collapsed:** a bad option offered often enough becomes a frequent act. So the
  reluctance must work from birth, not only through learning.

## The feelings (each a switch and an inherited gene, so evolution can tune its strength)
Base: `code_nb2`, arm n, the full NB2 brain.

0. **No joy in attacking.** The +0.1 per attack and the kill bonus are removed. They were written for the old brain's
   grudge-gated revenge.
1. **Empathy (gene E, start 0.5, range 0–2).**
   - Each week, r −= E × (the weighted mean distress of the people within reach).
   - Distress = (hunger + (1 − health/100)) / 2, plus 1 for someone hurt by violence this week.
   - Weights: kin and partner 1, affection > 0.3 0.5, others 0.2.
2. **Guilt (gene G, start 0.5).**
   - After one's own act, guilt rises:
     - an attack +0.3;
     - a kill +1.0, doubled for kin;
     - a noticed theft +0.15.
   - Each week, r −= G × guilt, and guilt fades × 0.9 a week.
3. **Love of one's own child (gene L, start 0.5).**
   - Each week, r += L × the mean, over one's own children under 6, of (fed and healthy, and with their carer);
   - and +0.1 × L for a week spent caring for, or giving to, one's own child.
4. **Approval and shame (gene A, start 0.3).**
   - Each week, r += A × the sum of the changes in others' affection toward one.
   - A new grudge held against one counts as negative.
5. **Curiosity (gene C, start 0.3).** Each week, r += C × 0.1 / (1 + the times one has done this action in this kind of
   situation).
6. **An inborn reluctance to harm (gene H, start 1.0).**
   - The instinct score of every attack and steal option gets −H.
   - It is part of the newborn's instincts but **not** scaled by g, so evolution sets it on its own.

None of these is a rule. Every act stays possible; only how it feels changes.

## Arms (shaped by the autopsy; the council may change them)
- **c:** v17's old minds, the yardstick.
- **n2:** NB2's full brain, unchanged (the control).
- **f0:** n2 with no joy in attacking.
- **fH:** f0 plus the inborn reluctance to harm.
- **f:** all the feelings (0–6).
- **f−E:** f without empathy (does empathy add to the reluctance?).

16 seeds; 600 years; on the cloud (long-run).

## Outcomes (draft)
- **Viability, as NB2:** extinction, and population against c.
- **Violent deaths and starvation deaths** against c.
- **Survival to 16 per birth.**
- **The genes' trajectories** (E, G, L, A, C, H and g). If feelings help, evolution should keep or raise them.
- **The garden as NB2,** with g held at 0. Can the network, with the feelings, live without the old instincts?

## The assistant's prior (draft)
- f viable: about 55%.
- f0 alone viable: about 20%.
- With the feelings, the network alone lives a year in the garden: about 15%.

## THE FROZEN DESIGN (supersedes the draft lists above where they differ)
**Code:** code_nb3 = code_nb2 + these switches; with all of them off it is code_nb2 exactly. Base arm: NB2's full
brain (n).

0. **No joy in attacking** (`nb3_no_attack_joy`). The +0.1 per attack and the kill bonus (0.3 × temper − 0.2 ×
   kindness) are not given.
1. **Empathy, gene E** (start 0.5).
   - Each week, r −= E × Σ w_q (rise_q + 0.25 × distress_q) / Σ w_q, over the people within reach.
   - distress_q = (hunger_q + 1 − health_q/100) / 2; rise_q = max(0, distress_q − last week's distress_q).
   - Weights: kin and partner 1, affection > 0.3 0.5, others 0.2.
   - It is a weighted mean, so more people do not multiply it (council: GPT's change from level to rise).
2. **Guilt, gene G** (start 0.5).
   - **Only for harm to people,** never prey:
     - an attack one **starts** +0.3;
     - a kill one starts +1.0 (× 2 for kin);
     - a noticed theft +0.15.
   - **An attack on someone who attacked one in the last 4 weeks is defence, and brings no guilt.**
   - Each week, r −= G × guilt, then guilt × 0.9.
3. **Love of one's own child, gene L** (start 1.0).
   - Each week, r += L × (mean over own children under 6 of well_k − 0.5 × mean over own children under 12 of
     distress_k).
   - well_k = 1 if the child holds at least half its need, has health ≥ 50 and is with its carer.
   - Plus 0.1 × L for a week spent caring for, or giving to, one's own child.
   - The concern half is set by the audit, so it does not swamp r.
4. **Approval and shame, gene A** (start 0.5). Each week, r += A × the sum of the affection changes others made toward
   one that week, minus the sum of the grudge increases toward one. They are read from the world's relation updates
   as they happen.
5. **Curiosity, gene C** (start 0.5).
   - Each week, r += C × 0.1 / (1 + the times one has done this action in this situation in one's life).
   - **Never for attack or steal.**
   - The audit shows it is tiny next to r, and it is kept as exploratory (council).
6. **An inborn reluctance to harm, gene H** (start 1.0).
   - The instinct score of every attack and steal option is lowered by H, not scaled by g.
   - **Not for an attack on someone who attacked one in the last 4 weeks** (defence).

**Pain and fear:** the audit found that injury already lowers r, through health in wellbeing and through fear. Being
attacked costs about 0.04–0.1 of r, against a weekly sd of 0.11. No separate pain term is added (council: only if
missing).

**Genes:**
- range 0–2;
- inherited from the parent whose network genome is inherited;
- mutation sd 0.08 (as g);
- founders take the start values;
- no cost or reward for any gene value.

**What the agent observes:** others' hunger, health and relations are the facts NB2's network already sees for the
people in reach.

**Arms** (16 worlds each, seeds 25801–25816, 600 years, LP, on the cloud by long-run):

| arm | what |
|---|---|
| c | v17's old minds (the yardstick) |
| n2 | NB2's full brain, unchanged |
| f0 | n2 with no joy in attacking |
| fH | f0 plus the inborn reluctance |
| f | all feelings, 0–6 |
| f−E | f without empathy |
| f−H | f without the inborn reluctance (council: "the most valuable missing ablation") |

**Primary reading, frozen:** "f viable" if f's extinct worlds are at most c's + 3 and the population ratio f/c (living-weeks,
years 100–600, paired world bootstrap, 10,000 draws, NumPy seed 20261113) has an upper bound ≥ 0.80. Also reported,
as council 84 asked: the point estimate and the lower bound.

**Secondary (with intervals, no gate):**
- f0 − n2, fH − f0, f − fH, f − f−E and f − f−H, on extinction and population;
- the causes of death (as NB2-A) and the share of attacks that are unprovoked;
- survival to 16;
- food given to kin's children;
- hunting;
- the gene trajectories (E, G, L, A, C, H, g);
- the network's share of choices (NB2's override share).

**The garden** (as NB2), for f: generation 1 against 18, with g = 0 and H held at its inherited value, learning off.
Does a feeling brain alone live a year?

**Validity:**
- the zero checks (all switches off = code_nb2; the arms all differ; the observers read-only; the checkpoint continues
  exactly);
- unit checks of each feeling against an independent computation of its formula;
- all worlds present under one fingerprint;
- the blind recompute by GPT and Gemini.

**The assistant's prior:**
- f viable: about 35%;
- f0 viable: about 10%;
- fH viable: about 30%;
- f−H viable: about 15%.
