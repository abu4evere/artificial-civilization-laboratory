# Debate round 17 (28 October 2026, sleep mode): the IC1 draft, the language groundwork audit (opinions, not sign-off)

**The same text to GPT (main chat) and Gemini (ACL session); Claude as council.** The question: the draft IC1 (called
TC0 in round 16), read-only on v8. Is it the right audit before a water-signal law? Are B1 and B2 sensible? What is
missing?

## Answers
- **GPT: yes, 90%.**
  - "NEW doesn't necessarily mean useful": add whether the told place is the listener's first water option. Report how
    many places were checked.
  - "Five shared-attention events do not prove five learning opportunities": record whether a pair meets at different
    water sources.
  - The most important missing measure is whether a listener acts on a told place **out of sight**: distance at the
    telling, and whether a later thirst decision selects it.
  - Habit-copy counts are not amounts of information.
- **Gemini: yes, 95%.**
  - B2 lacks a measure of how ambiguous the scene is (clutter): how many other things are in the shared view.
  - Add the listener's thirst at the telling, how many consecutive weeks pairs share water, and the distance to the
    told spot.

## Council (checked against the code)
- **Every addition can be observed without changing behaviour.** All are adopted:
  - `fresh_near`, `fauna.near` and the distance are pure reads;
  - the listener's thirst is a field;
  - per-telling use is matched in the `_nearest_spring` wrapper.
- **Clutter is measured for what can be seen cheaply:** shared fresh tiles and animal groups both see. Other people
  are not counted.
- **Corrected:** Gemini names a "Law 33 water-signaling study". No such law or study exists. It also suggests running
  the zero checks "across seeds 19701–19732". As before, the zero checks use seeds 501 and 601 at 20 and 60 years.
- **Agreed by all three:** B1 and B2 are descriptive branches for the creator's language decision, not pass/fail
  tests.
