# IW1 — How does the worth of made things form? (DRAFT, not frozen)

**Read-only on nature v9. No change to nature.** It is CO2's frozen next step for its reading "built-in pull carries
it" (`experiments/CO2_choice_v9/findings.md`): making loses at any moment mostly because a made thing's worth is low
against food and gathering. **Why is that worth low?**

## The decisive split
- **Honest:** made things rarely help much when used, so their worth is truly low. It is then a "world where knowing
  matters" question (the creator's third goal): the world gives tools little to do.
- **Unlearned:** made things would help, but their worth is never learned. A kind starts at 0 when invented or made,
  changes only with use (moving 15% of the way to the felt help each time) and is used too rarely to rise. It is then a
  question of experience and learning.

## How worth works (code, live v9; checked 31 October 2026)
- **Each person holds `itemval[kind]`,** from −1 to 1. It starts at:
  - 0 when the person invents or makes the kind (`knowhow.remember_recipe`);
  - max(old, 0.5 × claim × credence) when taught (`information.hear_how`);
  - max(old, 0.3 × outcome) when watched (`knowhow.watch`).
- **It changes only in `knowhow.judge_item`,** when the thing is used:
  - v ← v + rate × (felt − v), with rate 0.15, or 0.3 when proved wrong in sign;
  - felt = `matter.factor(item, use)` − 1 for tool use, or fixed values for floats, carrying, warmth and wear.
- **No decay with time.** Kinds leave a person through:
  - the 12-recipe limit (lowest worth first);
  - `forget_useless`;
  - death.
- **The make option's score** uses max(itemval, worth as a part, belief, 0.5 × surprise) × diligence and hunger terms.
  Nobody under 12 can choose make.

## Design (32 worlds, seeds to be set; LP: 80 founders, 80×80; 200 years; `code_v9`; one arm)
**The observer only reads:**
- events (`learn`, `make`);
- one wrapper on `knowhow.judge_item` that notes the person, the kind, `felt`, and itemval before and after;
- a census of every (person, kind) in memory once a year.

## Questions
- **Q1** (primary): **calibration.**
  - For each `make` chosen (adults, years 100–200), the maker's itemval of that kind just before making, against
    the mean felt help of that kind:
    - (a) in the maker's own later uses;
    - (b) in everyone's uses of that kind in the same world.
  - **Under-valuation** = mean felt − itemval, with a world-bootstrap 95% interval.
- **Q2: experience.** At each `make`, how many times the maker had used that kind before. Bins: 0, 1–2, 3–5, 6+.
  With rate 0.15, 6 uses close 62% of the gap from a zero start (Gemini's point: 3 uses close only 39%).
- **Q3: the source of first worth** (Gemini). Calibration trajectories (itemval against uses), grouped by how the
  person first got the kind: invented or made, taught, or watched.
- **Q4: help.** The distribution of felt help per use, by kind of use, and the share of uses with felt > 0.1.
- **Q5: leaving.** Of person-kinds with a mean felt help > 0.1, the share that leave memory through the limit,
  `forget_useless` or death, and the share never used before leaving.
- **Q6:** whether the kinds people make are the ones that help most (rank correlation of make counts with mean felt,
  per world).

## Frozen reading (Q1 and Q2)
- **"Unlearned"** if under-valuation (b) is > 0.10 with its lower bound > 0, **and** most makes (> 50%) rest on fewer
  than 6 prior uses.
- **"Honest"** if the mean felt help per use (b) is below 0.10, and itemval is within ±0.05 of it.
- **Otherwise "mixed".**

## What would follow
- **"Unlearned":** the next question is how people could learn a kind's worth without many uses. For example, PG0's
  finding that own past experience predicts a new kind's usefulness. That would be a learning law, the creator's
  decision.
- **"Honest":** the world gives made things too little to do. That is the creator's "world where knowing matters"
  question; measure before making anything harder.
- **"Mixed":** report both, by source and by kind of use.

## Status
**A draft for debate (round 33).**
- **Gemini: yes, 85%.** Its two changes are adopted: the 6-use bins and the trajectory by source.
- **GPT:** not yet reachable. The ChatGPT page stuck on "Loading profile", 31 October about 01:50. It will be asked
  before freezing.
