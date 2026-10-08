# HF3 — Why did gifts fall under HB1, and does losing them explain the hunger? (read-only; SIGNED OFF, questions frozen as `HF3-questions` before any data)

**Signed off by the creator (October 2026):** the decision rule as drafted (gifts ≤ 0.8 ×; rescue within reach ≤ 0.8 ×; channel ≤ 0.9), holdout on new seeds 1501–1516, first 40 years. Nothing has been run.

**Asked by the creator (October 2026), after HF2.** No fixes, no tuning, no code changes. Nothing has been run.

## Why

HB1 (a shared home base) raised extinction (33 of 64 against 22). HF1: not local depletion. HF2: not mouths to feed, not
meat; but a lead written before HF2's holdout and repeated in it: **food received as gifts fell to 0.59 of the
control's** in both sets, about three quarters of the drop in what adults took in, while foraging barely changed. Under
rule 15 that lead is consistent, not confirmed. HF3 tests it with thresholds set in advance and asks **why** gifts fell.

## The code, read before any data (`code_hb1`; `mind.py` "Give food", `actions._give`)

- A person considers giving only to someone **within `reach` (3 tiles)** at the moment they decide (among the twelve
  nearest), and not to their own young dependant (who is fed separately).
- They can give only with a **surplus**: food in hand above **2 weeks of their own need plus their dependants' need**.
- How much they want to give rises with the other's **hunger**, their own **kindness**, **affection**, **kinship**, being
  the other's **partner**, and any **debt** they are repaying; it is scaled by the size of the surplus.
- A gift is up to twice the recipient's weekly need; the giver keeps 1.5 weeks of their own.

So gifts can fall for three distinct reasons, each measurable:

| channel | what falls |
|---|---|
| **G1 meetings** | fewer short people within reach of potential givers |
| **G2 surplus** | fewer adults holding a surplus |
| **G3 choice** | given both, giving is chosen less often |

## Questions

First 40 years, arms H (HB1, `home_base = 1`) and C (the same code, settings off), per adult-week (16+).

1. **The fall, again:** food received as gifts per adult-week; gifts given per adult-week.
2. **The channels:** (G1) share of adult-weeks with at least one **short** person (food in hand below one week of their
   need), other than one's own young dependants, within `reach` when deciding; (G2) share of adult-weeks with a
   **surplus** as the code defines it; (G3) gifts given per adult-week in which both held (an **opportunity**).
3. **Rescue within reach:** for each starving adult-week, was any other adult with a surplus within `reach` at the time of
   deciding? Share of starving adult-weeks with such a potential giver, H against C.
4. **Who gives to whom:** gifts by the giver's and recipient's relation (partner, kin, other) and by whether they share a
   couple home; distance between giver's and recipient's couple homes.
5. **Losing gifts and starving (descriptive):** within each arm, starving share of adult-weeks for adults who received no
   gift in the previous 8 weeks against those who received at least one.

"At the time of deciding" is read from the observer's record of the week before (people's positions and food at the end
of last week are where and what they held when choosing this week's action, before anyone moved): an approximation,
written before data.

## Decision rule (frozen; read on discovery and holdout separately)

| | supported if, in **both** sets |
|---|---|
| **Gifts explain the hunger** | food received as gifts per adult-week in H ≤ 0.8 × C's, **and** the share of starving adult-weeks with a potential giver within reach in H ≤ 0.8 × C's |
| **Channel** | the channel among G1, G2, G3 whose H ÷ C ratio is lowest is named, **if** that ratio is ≤ 0.9 in both sets; otherwise "channel not identified" |

If the first row fails in either set: **gifts do not explain the hunger**; reported as such, the creator decides.

## Worlds

| set | seeds | runs |
|---|---|---|
| **Discovery** | 501–516 | H and C, 40 years |
| **Holdout** | **1501–1516, new**: the gifts lead was seen on 501–516 and 1401–1416, so neither may serve as the holdout (rule 15) | H and C, 40 years |

## Hard stops

- Observer read-only: state hash with and without it after 20 years, both arms, two seeds.
- Replays reproduce: on discovery, H matches HB1's saved populations and C matches F1's (years 10–40).
- Code fingerprint unchanged.

## Priors (written before any run; not predictions to test)

- **Assistant:** gifts explain the hunger, through **G1 meetings**: couples ending every week at home are within reach of
  fewer people from other households, so fewer short people are in reach of anyone with a surplus. Held loosely: the last
  two priors (HF1, HF2) were wrong.

## Decisions (taken by the creator at sign-off)

1. **The decision rule** and thresholds (gifts ≤ 0.8 ×; rescue within reach ≤ 0.8 ×; channel ≤ 0.9).
2. **Holdout on new seeds 1501–1516.**
3. **First 40 years** (as HF1 and HF2).
