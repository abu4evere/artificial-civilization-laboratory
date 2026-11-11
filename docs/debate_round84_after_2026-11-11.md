# Council round 84: NB3, feelings, the answers (11 November 2026)

The question is in `debate_round84_question_2026-11-11.md`. These are opinions, not sign-off, recorded only from the
actual replies. **Gemini:** its tab kept reloading and refusing input (as for Cradle council 4); to be retried.

## GPT (Thinking, medium; chat `6af40bb2`): approve the direction, revise before freezing; 25%
- **(a)** Removing the attack reward is "essential". Keep empathy, guilt, love of one's child, approval and the
  reluctance; curiosity is exploratory ("the autopsy does not identify insufficient curiosity").
  - **Corrections:**
    1. empathy should respond to **changes** in distress, not levels, or living near hungry people is punished even
       while one helps;
    2. guilt should not treat **defence** like an unprovoked attack;
    3. love of one's child should also feel the child's **unmet needs** (hunger, danger), not only reward when it is
       well;
    4. add **fear and pain of being hurt**, but check first whether injury already reaches the learning signal through
       mood.
- **(b)** Starts, all with range 0–2: E 0.5, G 0.5, **L 1.0**, A 0.5, C 0.5, H 1.0.
  - **First run a scale audit:** compare each term with the existing reward and instinct-score spread. "A penalty of 1
    could be enormous." The audit is not permission to optimise survival.
  - Freeze everything; if a bug or scale mismatch appears, version the experiment and run a new cohort.
  - Use what the agent can observe where possible.
- **(c)** H is "a hand-written behavioral prior. But it is not a prohibition." Acceptable if it can evolve to 0 and the
  network can override it; track H and the attack rates.
- **(d)** Add **f−H** (all feelings without the reluctance), "the most valuable missing ablation", and f−L if
  affordable.
  - "An upper confidence bound of 0.80 is a very weak population criterion"; report the point estimate and the lower
    bound too.
  - **Secondary:** attack initiation, child deaths, starvation, food transfers, reproduction, defence, hunting, gene
    trajectories, and **whether the network makes meaningful choices or just inherits strong biases.**
- **(e) Risks:**
  - passivity (no defence; empathy discouraging hunting);
  - empathy overload (normalise so that more people do not multiply the burden);
  - reward exploitation (feeding already-fed children, curiosity cycling);
  - learning instability. Log each term separately.
- **(f) 25%.** The learning-off collapse "suggests that the problem extends beyond learning and aggression." "Give the
  people reasons to care. Do not give them instructions for how to behave."

## DeepSeek (chat `ffaf9ff0`): 35%
- **(a)** Strong support for removing the attack reward; plausible for empathy, guilt and love; weak for approval and
  curiosity. H is "an anti-aggression bias", not a feeling.
  - **Missing:** one's own pain and injury; a learned fear of retaliation; one's own child's hunger beyond age 6.
  - **Wrong as written:**
    - **guilt's "kill" must mean killing a person, not prey,** or hunting is punished;
    - **curiosity must not reward attack or steal,** or it rewards novel violence;
    - **define attack against defence,** so H does not stop self-defence.
- **(b)** All genes start at 1.0 (the midpoint), range 0–2; the same in every arm; fixed mutation; sensitivity at 0.5
  and 1.5 pre-registered.
- **(c)** A rule-like prior; acceptable only because it can evolve to 0, with no gate or threshold.
- **(d)** Add **f−H**, and leave-one-outs (f−G, f−L, f−A, f−C) if affordable.
  - Primary: f's extinctions at most c's + 3 (≤ 7), and a population ratio f/c whose one-sided lower bound is
    ≥ 0.80.
  - Secondary: causes of death, unprovoked attacks, child victims, kin food transfers, child survival, gene values.
- **(e)** Too much E, G and H reduces defence; love can keep carers from foraging; empathy for strangers can cause
  costly sharing; curiosity can reward risky acts.
- **(f) 35%.**

## What NB3 takes (the assistant)
1. **Guilt** counts only harm to people: attacks, kills (×2 for kin) and noticed thefts. Never prey.
2. **Initiating versus defending:** guilt and the reluctance apply to attacks one starts. An attack on someone who
   attacked one in the last 4 weeks counts as defence.
3. **Empathy** follows the week's *rise* in the distress of those within reach, plus a small part of its level. It is a
   weighted mean, so the number of people does not multiply it.
4. **Love of one's child** also feels the child's hunger: concern, not only reward.
5. **Pain and fear:** the scale audit first checks how much injury already reaches r through mood. A pain term is added
   only if it does not.
6. **Curiosity** never rewards attack or steal.
7. **The scale audit before freezing:** each term is measured against the spread of the existing reward and instinct
   scores, in a short run of the code, read for scale only, never for survival.
8. **Arms:** c, n2, f0, fH, f, f−E and **f−H**.
   - Primary: viability against c (as NB2).
   - Also reported: the point estimate and lower bound of the population ratio, and whether the network makes the
     choices (NB2's override share, and the g-zero garden).
9. **Starts:** E 0.5, G 0.5, L 1.0, A 0.5, C 0.5, H 1.0 (GPT), all with range 0–2. DeepSeek's sensitivity runs at 0.5×
   and 1.5× are an exploratory follow-up.
