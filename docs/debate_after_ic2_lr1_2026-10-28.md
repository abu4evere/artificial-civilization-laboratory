# Debate round 20 (28 October 2026): after IC2 and LR1, back to erosion (opinions, not sign-off)

**The same text to GPT (main chat) and Gemini (ACL session); Claude as council.** The creator chose to pause language
and return to erosion. **Code facts put to both (checked):** founders start as adults aged 16–28 with every skill at
0.2–0.4 (`world.py`, `_make_founders`); every newborn starts at 0 (`person.py`); crafting skill grows only by making or
play. LS1: 0.73 of useful know-how held in years 0–100 is founders'; making falls from 1 in 40 to 1 in 800 choices;
tool use in foraging 0.318 → 0.021. Claude's question: is much of the erosion the founders' unearned head start wearing
off, so that the real question is why world-born people cannot build up from zero? Test: founders at the world-born
level (all skills 0) against today's founders, over 300–500 years.

## Answers
- **GPT: test the head start first; don't change habit learning yet. 85%.**
  - "Yes, partly." But convergence would not prove erosion is only a starting effect: both could approach a low state
    because today's laws block accumulation.
  - Changing founders' skills is "an initial-condition intervention, not a change to the ongoing laws"; fair, but an
    experimental arm, not a read-only audit.
  - The habit evidence is a strong clue but does not say which single change would work; HC1 showed a plausible fix
    can fail.
  - Design: control (today's founders), zero-start founders, a sham; 500 years, paired seeds. **Primary: world-born
    crafting skill in years 300–500.** Secondary: making, tool ownership, useful know-how, population, extinction.
    Measure skill by age and experience, so founder deaths and age structure are not mistaken for learning. Include
    extinct worlds; report survival separately.
  - Readings: both low → a low-learning equilibrium (not proof that the head start caused everything); zero-start
    climbs → something about the head start blocks growth; zero-start collapses → founder skills hold up survival and
    early transmission.
- **Gemini: the same study ("FS1"). 95%.** (Its first reply was cut off by an error; it repeated point 3 on request.)
  - The framing is sound; founders' skills are an initial condition, "not a nature change"; the rules of the world stay
    identical.
  - Don't jump to habit changes: first establish whether a zero-start population converges to the same late state, to
    give a clean baseline for later learning-rule studies.
  - Design: 32 paired seeds, 500 years, v8; control vs zero-start. **Primary: making per adult-year and tools held per
    adult in years 300–500.**

## Council (checked against the code)
- **Agreed by all three:** the head-start test comes first; no learning-rule change yet.
- **Corrected (Gemini):** "zero nature-change risk" is too strong. The zero-start arm needs a new setting in a study
  copy of the code (`founder_skill`, default = today's founders exactly), with zero checks; it is not adopted into
  nature unless the creator decides.
- **A risk both raised, and one more:** zero-start founders also have foraging skill 0, so they may starve early. The
  draft therefore adds a third arm in which only the founders' crafting skill starts at 0, to separate "a head start in
  making" from "a head start in getting food".
- **Primary:** GPT's (world-born adults' crafting skill, by age) is primary; Gemini's (making per adult-year, tools held
  per adult) are the key secondaries.

# Debate round 21 (28 October 2026): the FS1 draft
- **GPT: approve after two changes, 90%.** A ratio margin is fragile when late skill is near 0.05: use an absolute
  difference with a margin tied to how skill affects performance, chosen before data. The pooled skill measure is
  survivor-weighted: report contributing worlds and adult-years, keep extinction separate. 32 seeds are reasonable,
  but an inconclusive result must be reported as such, with no seeds added afterwards. Check that zero-start changes
  nothing else at the start.
- **Gemini: 95%.** Add an absolute equivalence bound (it proposed 0.008). If z collapses, make c the main test. It
  claims 32 seeds give narrow intervals.
- **Council:** all adopted, except the margin: **0.012, from the code** (`skill_gain`, the skill one making act gives
  from zero; tool quality ∝ 55 + 45 × skill, so about 0.5%), not Gemini's unexplained 0.008. Gemini's "narrow
  intervals" is not assumed.

# Debate round 23 (28 October 2026, sleep mode): after FS1, what next?
**Asked:** (A) a read-only audit of how making's value changes over years 0–200, or (B) a nature-change study on how
copied habits are weighted.
- **First answers: both (A).** GPT 90% (follow individuals through life; find which changes first); Gemini 95%
  (decadal crossover with a route ledger).
- **Council check, sent to both:** CL1 (final, v7) already gives that timeline by era. Making's value is always low
  (q 0.025 → 0.043 → 0.049, almost no social part), while the common actions' values rise about threefold (0.38 → 0.86
  → 1.12), mostly through copying in talk (C_talk 0.13 → 0.31 → 0.39). MK1: making's own score is flat; the
  competitors' soft maximum rises 1.30 → 1.94. CO1: habit carries 0.86 of that rise.
- **Second answers: both (B).**
  - **GPT, 80%: "experience-checked copying."** The speaker shares an action and the outcome they personally
    experienced; the listener updates on that evidence instead of taking the speaker's accumulated value. The same rule
    for every action. Safeguard: the shared outcome must be a genuine recorded experience, not a value or an inferred
    success. Arms: v8, the new rule, a sham. Primary: late common-action over-valuation (q − G), with a pre-set
    meaningful reduction and no harm to making's calibration; making and tools secondary. Limit: one person's
    experience may not apply to another.
  - **Gemini, 85%: "experience-grounded copying."** In talk, the listener moves toward the speaker's own-experience
    component (C_TD) instead of the whole value, breaking the copy-of-a-copy loop. Primary: common over-valuation in
    years 100–200 from about +0.42 to at most +0.15; no-harm gates on population and survival.
- **Council:** agreed, B now. Two ways to build it; **GPT's is the more physical** (people tell what happened to them,
  a story of experience), while Gemini's needs each person to carry, as nature, a record of which part of their values
  they learned themselves. Gemini's +0.15 target is an unexplained number. To be drafted and reviewed (round 24).

# Debate round 24 (28 October 2026, sleep mode): the EX1 draft
- **GPT: approve, 85%.** The latest experience, not a random one. Record how often the listener has met that situation.
  Warning: this replaces whole-table telepathy with "one-event telepathy"; fine as a copying experiment, not language.
  Check that no second learning step happens. v8 unchanged until the creator decides.
- **Gemini: approve, 95%.** The latest experience (a buffer would need invented sizes). The record belongs to its owner
  and is not inherited. The learner's own values give the look-ahead.
- **Council:** all adopted; an exact-step zero check added. **Corrected:** Gemini again said "exact log replays"; the
  runs are new worlds with a read-only observer.

# Debate round 25 (29 October 2026, sleep mode): after EX1 (copying is not the cause), what next?
**Put to both:** EX1's result; HL1 (rewards flat, look-ahead 0.06 → 1.26; making 258 times fewer updates;
rich-get-richer 0.83); VC1 (the max gap is 0.35 of the bias). Council reading: practice starvation in a learner whose
values start at 0 and rise only with use. Options: (A) Expected-SARSA look-ahead; (B) a curiosity law towards rarely
tried actions, scaled by the existing curiosity gene; (C) a read-only decomposition of the other 0.65 first.
- **GPT: (B), 85% valid, but only 45% that it meaningfully reduces practice starvation.** A curious person sometimes
  samples among their least-practised feasible actions, "using the existing curiosity trait as the probability";
  same rule for every action; fading with experience; feasibility and safety kept. Primary: the share of feasible
  situation-action pairs that get at least one real learning update, against v8. Expected SARSA as a separate later
  study. "Record our failed EX1 prediction ... an important scientific result, not a setback to hide."
- **Gemini: (B), 85%.** A novelty pull curiosity ÷ √(N(s,a) + 1) added to each option's score, which it calls
  "parameter-free".
- **Council (checked):** both proposals still hide a scale. Gemini's bonus is added to choice scores whose size it fixes
  implicitly (an invented unit). GPT's, taken literally, would make a person with curiosity 0.9 pick an untried
  action 90% of the time. **How strongly curiosity pulls is the kind of number that becomes tuning,** and curiosity is
  the creator's own interest ("laws for learning 'why'"). So the design is **not frozen in sleep mode**: it goes to the
  creator, with a possible anchor to settle first (for example, the share of time young foragers spend in play and
  exploration, from human evidence).
