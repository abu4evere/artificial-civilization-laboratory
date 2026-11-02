# Debate round 49: which general condition to test after UP1 (2 November 2026)

**What was asked:** `research/local/round49_next_condition.txt`. It gave UP1's result, the exploratory "what is
missing" check, the code facts, and three candidates:
- **(A) want propagation:** the gather pull uses the value the make choice already gives a wanted part;
- **(B) a goal kept across weeks;**
- **(C) more carrying room.**
- **Who:** GPT (chat `6ae8a4a9`) and Gemini (chat `c3479f18e1de7847`; it answered on Flash because Pro was "in high
  demand").
- **Each answer is an opinion, not a sign-off.**

## First answers
- **GPT: A first, 93%.**
  - "A repairs that discontinuity without introducing memory, persistent goals, or additional carrying capacity. B ...
    should follow if A fails."
  - A is a general law: "propagates existing value through dependencies, without naming inventions, guaranteeing
    completion, or rewarding cultural success". But "verify whether value reaches materials through multiple nested
    levels".
  - **Primary:** the share of kinds invented in years 100–195 made again by anyone within five years.
  - **Positive only if:** A beats both v11 and the sham, with paired intervals above 0, **and** by at least 1 percentage
    point.
  - It gives about **60%** to A alone producing a meaningful rise.
- **Gemini: A first, 88%.**
  - A "directly fixes a structural inconsistency" and is "a minimal, general law".
  - **Its guards:** early invention rates and survival.
  - **Its sham:** random variance in gather pulls. ACL's standard sham is one extra random draw in week one; Gemini was
    told so.

## Second question: one level (A1), the whole chain (A2), or both arms?
- **GPT: both arms (v11, A1, A2, sham), 95%.**
  - **Its three comparisons:** A1 − v11, A2 − A1, sham − v11.
  - **For A2:** the **maximum** propagated value, discounted by 0.8 per step, never summed, and cycles must not amplify
    it.
  - **Its caution:** A2 changes making and gathering together, so A2 − A1 is the package's extra effect.
- **Gemini: both arms, 94%, with A2 as "the true general law".**
  - **Its odds of a meaningful rise:** A1 35%, A2 68%. Inputs "often sit 2+ steps down the chain where A1 leaves gather
    pull at zero".

## Outcome (the assistant, as council)
- **Both agree:** a nature-change test **in a copy** of want propagation, with four arms (v11, A1, A2, sham) on 32
  paired seeds.
- **The primary:** five-year remaking of kinds invented in years 100–195.
- **GPT's reading rule is adopted:** an interval above 0 against both v11 and the sham, and at least 1 percentage
  point.
- **Guards:** population and extinctions. The invention rate is described, not used as a guard; a real change there
  could be part of the effect.
- **Checked against the code:**
  - `_wanted_parts` (make side) is one level deep;
  - `_material_wants` (gather side) counts only `itemval`;
  - each is used once in `mind.decide`.

  So A1 changes one line of meaning (the gather side takes the wanted-part value), and A2 replaces both with one
  recursive rule.
- **Not adoption:** a nature-change test in a copy is allowed in sleep mode with care (`CLAUDE.md`). Adopting anything
  needs the full safe path, and the creator is asked first.
- Both chat tabs were closed afterwards.
