# Debate round 35 (31 October 2026, sleep mode): after TR1, an access audit (A) or a handing law (B)? (opinions, not sign-off)

**The same text to GPT (fresh chat `6ae5fa48`) and Gemini (fresh chat `f71be6053aeab1c2`), about 10:30; Claude as
council.**

**The options:**
- **(A)** a read-only access audit on v10. Who holds the best tools; how often a bare-handed forager is near a better
  tool; who makes tools; how tools leave hands.
- **(B)** a frozen nature-change test in a copy. Extend `give` so a person may hand a made thing to someone nearby,
  with the existing choice machinery and no new rewards.

## Answers
- **GPT: A first, 95%.** "B could produce a null result simply because nobody chooses to give, not because
  hand-to-hand transfer is unimportant."
  - B is a fair physical law: "the ability to transfer an object is a physical possibility, not a prescribed custom."
  - **Guards for B:**
    - conserve objects exactly;
    - respect the recipient's hand capacity;
    - use unchanged choice machinery;
    - no gifting bonuses, forced transfers or programmed kin preference;
    - record opportunities apart from actual transfers.
  - "Run A, then freeze B using what A reveals to interpret the causal test, not to engineer its outcome."
- **Gemini: A first, 95%.** A reveals whether the deficit comes from spatial isolation, inventory clogging (the 3-item
  limit), non-foragers holding items, or loss at death.
  - B is fair: "a basic environmental/biomechanical affordance, not a prescribed social norm". It becomes a custom only
    if the code mandates sharing, restricts receivers by role, or rewards giving.
  - **Guards for B:**
    - the recipient must have room (fewer than 3 items);
    - the action costs the same as giving food;
    - a check that handing is not used only to dump items past the 3-item limit.

## Council
- **Both choose A,** for the same reason. All their guards for B are recorded here for when B is drafted.
- **Checked:**
  - `_give` passes food and seeds only;
  - its cost is 5 (`COST["give"]`), the same as Gemini's "parity" would use;
  - transfers among the living happen only by pick-up (v8).

## Round 36: the design check of TA1 (same chats, about 10:45)
- **GPT: sound, 90%.**
  - Keep (a) and (e) as overlapping flags; make (b), (c) and (d) exclusive.
  - Separate proximity from transfer feasibility.
  - Q5 with the tool's real properties and the caps.
  - Verify the wrappers are read-only, and account for every tool's entry and exit.
  - Thresholds are classifications, not causal proof.
- **Gemini: sound, 94%.**
  - A strict priority partition.
  - Empty hands against hands clogged with other things.
  - Track adult tools in children's hands.
- **Council:** all adopted (`experiments/TA1_tool_access/questions.md`). **Corrected:** Gemini attributed tool making
  to ACL's children under 12; that is the forager evidence. ACL's children cannot make known things.
