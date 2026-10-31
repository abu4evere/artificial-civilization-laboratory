# Debate round 34 (31 October 2026, sleep mode): TR1, what do tools really add? (opinions, not sign-off)

**The same text to GPT (fresh chat `6ae5b429`) and Gemini (fresh chat `ba26c2914973cdfe`), about 05:30; Claude as
council.**

## Answers
- **GPT: yes, 85%.**
  - Measure zero-gain and partly constrained uses separately.
  - Compare felt help with the normalized realized gain.
  - Separate the globally best-known tools from those the individual knows.
  - Use paired expected kill chances, and keep expected kills apart from food.
  - Report intervals; avoid a firm label when the interval crosses a threshold.
  - "Before asking why civilization doesn't accumulate knowledge, determine whether knowledge offers enough real-world
    advantage to be worth accumulating."
- **Gemini: yes, 85%.**
  - Q2 exposes "phantom utility".
  - Hunting headroom would vanish against all food, so judge it against hunting.
  - Add a continuous efficiency ratio.
  - Later, a sweep with doubled carry and Aché-calibrated hunting.

## Council (checked against the code)
- **The counterfactuals are computable from the same state with pure functions:** `forage_rate`, the room
  (`carry_capacity`), and the tile's crop and plants, by `_forage`'s own arithmetic. `resolve_hunts` is called as
  `actions.resolve_hunts` from `world.step`, and foraging through `actions.HANDLERS`, so both can be wrapped.
- **The "best-known tool" is taken from existing items,** not from recorded kind properties.
  `world.knowledge[sig]["props"]` is filled only when a kind is first recorded through making, so it is incomplete.
- **Gemini's TR1b changes nature settings** (carry, hunting). It is a nature-change test, so it is the creator's
  candidate, not part of this read-only study.
- **Every other addition is adopted.**
