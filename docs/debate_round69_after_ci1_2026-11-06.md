# Council round 69: what goes to CI1's confirmatory run (6 November 2026, 16:35)

**Opinions of GPT, Gemini and DeepSeek, not sign-off.**
- **The question:** `docs/debate_round69_question_2026-11-06.md` (the same paragraph to all three).
- **The chats:** GPT, the main chat (the reply came on "Instant" thinking); Gemini, chat 87f468c684ee5839 (as round
  68); DeepSeek, chat 2552dbba.
- **Recorded from the replies read in the chats.** The time in the title is from the clock.

## Answers
| | GPT | Gemini | DeepSeek |
|---|---|---|---|
| 1. what to confirm | **LG alone.** LG+IN's small extra does not show an interaction, and confirming both would blur the reading | **LG alone.** +0.0192 against +0.0183 is within noise, and IN "mechanically misfires" | **LG alone.** LG+IN cannot be told from LG; "bundling an unsupported arm into v15 would violate one law at a time" |
| 2. design | Yes: 32 new seeds, nothing changed. **Define "above the sham" by a frozen rule with uncertainty**, not by which point is larger. Keep all guards. Remaking as a **pre-registered secondary**, not a gate. Report child and grown apart, and **tell remaking by the inventor from making by another person** | Right as proposed. 32 seeds suffice. Remaking described, not a gate | 32 seeds suffice. Add, not as gates: the co-primary by inventor age; remaking by the inventor with an interval; a pre-registered handling of a lost world; child makes and child starvation side by side |
| 3. IN | **Set aside, not discarded.** First a read-only audit of how aims form, last, and whether a complete set leads to a make | **Leave aside** until new inventions are valued at birth (a separate study) | **Leave aside, do not revise now**: "not refuted, it is inapplicable". Re-test on v15; the order of making stays a candidate |
| 4. toward Bob | It removes a real developmental limit, but does not yet show a cumulative mind. That needs deliberate remaking, passing to others, improvement and survival across generations | Yes: it removes a hardcoded barrier between discovery in play and making on purpose | "A real step, not arrival": the first inventor remaking ever seen in ACL (0 → 22), but cumulative culture needs passing on and improving |
| 5. confirms LG | **85%** | **95%** | **about 92%** |

## Checked (the assistant as council)
1. **A claim in the question was not measured, and is corrected here.**
   - The question said aims "seldom point at new kinds" because a new kind starts unvalued.
   - In the code (`knowhow.judge_item`), a thing's value moves toward what using it gave, so a new kind that is used
     can pass 0.05 and become an aim.
   - How often aims point at new kinds was not measured in CI1. GPT's read-only audit of aims would measure it.
   - Gemini's and DeepSeek's reasons for setting IN aside lean on that claim. Their conclusion (set IN aside) also
     follows from IN's own result: no effect.
2. **Gemini: "until new inventions are valued at birth".** VA1 found that 0.824 of new kinds are used before their
   recipe is lost, so valuing at birth is not the general bottleneck it found. Whether it limits aims is the same
   open question as point 1.
3. **DeepSeek: a lost world and missing pairs.** Checked in the output. The extinct world stays in the data with its
   counts: LG's seed 24017 ended at year 93, and its row counts zero for years 100–200. So no pair is missing, and
   nothing needs adding.
4. **DeepSeek: inventor age and child makes.** These are already in CI1's described tables and carry over unchanged.
5. **DeepSeek: "only about 2% of kinds are ever learned by anyone else".** Not checked against a record and not used.
   The new measure of making by another person (below) will give a number.
6. **GPT: above the sham, with uncertainty. Adopted.** LG − sham in the co-primary, with its paired-bootstrap lower
   bound above 0.
7. **GPT: remaking by the inventor apart from making by others. Adopted.**
   - Remaking within 5 years becomes the pre-registered secondary: LG − v14 with an interval, not a gate.
   - "Made by another person within 5 years" is added to the read-only observer and described.

## Merged plan (CI1-C, to be frozen)
- **Code:** `code_ci1` unchanged (fingerprint e0ccbf07…). **Arms:** v14, LG, sham. **Seeds:** 24101–24132 (new).
  200 years; years 100–200 counted.
- **Confirmed** only if all three hold:
  1. no CI1 guard is raised for LG against v14;
  2. the LG − v14 co-primary has its lower bound above 0;
  3. the LG − sham co-primary has its lower bound above 0.
- **Secondary (pre-registered, not a gate):** the share of new kinds remade by their inventor within 5 years,
  LG − v14 with an interval.
- **Described:** kinds made by another person within 5 years; everything by inventor age; child makes and child
  starvation side by side.
- **If confirmed:** a blind recompute, then the adoption council, then the safe path to v15 (`code_v15` = `code_v14`
  + the child_make law at default 1). IN is set aside; a read-only audit of aims comes later.
- **The assistant's estimate:** about 80% that CI1-C confirms LG. The rule is a little stricter than CI1's (the sham
  condition), and two of the eight guards had wide intervals.
