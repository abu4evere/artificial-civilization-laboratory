# NB3: feelings. Can a neural people live in the open world if it is born with human feelings? (DRAFT, not frozen)

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

**This draft waits for:**
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
