# Council round 77: adopt FF4 as v16, and the next step after MP1 (7 November 2026)

The question: `docs/debate_round77_question_2026-11-07.md`. GPT (main chat), Gemini (ACL chat) and DeepSeek (ACL chat
2552dbba) got the same text. **Each answer is that model's opinion, not sign-off.**

## Answers

**GPT's opinion, not sign-off.** "Adopt FF4 as v16, investigate why made parts are not produced, and audit dependent
feeding in parallel."
- (a) Yes, 98%, conditional on the safe-path checks:
  - v16 with the fix off equals v15 exactly;
  - v16 with the fix on equals FF4's arm f exactly;
  - hashes, seeds, the diff and the rollback version are archived.

  "Passing the harm guards establishes no detected unacceptable harm, not proof of zero harm."
- (b) The read-only part-making funnel. For every stage-A kind and each required part, it records:
  - recipe known;
  - inputs available, including deeper made parts;
  - the part valued, directly or through the final kind;
  - making offered;
  - making chosen;
  - making succeeds.

  It must separate not knowing the recipe from knowing it but lacking prerequisites, and from having the chance but
  choosing another action. Repeated opportunities must not count as independent.
- (c) Yes, but as a separate frozen study. It would look at feeding by caregiver, recipient age, sex, kinship and
  household, and test whether feeding precedes the caregiver going short and losing energy. No assuming the cause is
  sex or parenting alone.
- (d) 97%. The main risk: a part may be impossible to make because an earlier prerequisite was never learned. Name
  those cases separately.

**Gemini's opinion, not sign-off.**
- (a) Yes, 100%.
- (b) The part-making funnel: "Diagnosing exactly which cognitive or menu node (knowledge, valuation, inputs,
  offering, or choice competition) fails" is the way to an evidence-anchored law.
- (c) Yes, alongside.
- (d) 95%.

**DeepSeek's opinion, not sign-off.**
- (a) Yes, about 94%. Before tagging, confirm:
  - fix off = v15 bit for bit;
  - reload exact;
  - tests and reference hashes;
  - v15 kept.

  Record that the women's gap and the remaining blocked starving weeks are a different, open mechanism.
- (b) The funnel, with two amendments:
  1. split by depth (level-1 against level-2+ parts);
  2. continue past the make: knows → has inputs → values above the 0.05 floor → offered → chosen → completed →
     retained (handed away, worn, used, or held). Without the last stage, "parts are not made" cannot be told from
     "parts are made and given away"; MP1 says both are true.
- (c) Yes, alongside: which parent gives food to dependents, how often giving leaves the giver short, by sex and age
  band, the care trait, and the shortfall after giving.
- (d) About 90%.

## Checked against the code (Claude)
- **The part's value comes from its whole.** `mind._wanted_parts` gives a part value (0.8 × the whole's value) only when
  the person values the whole (`itemval` > 0), does not hold it, and does not hold the part. The make option then needs
  that value above 0.05, the recipe known, and the inputs in hand (`can_make`).
- **So the funnel's valuation step is the likely place to look.** A new kind that its maker never comes to value (never
  judged useful) passes no value to its parts.

## Decision
The assistant, under the creator's standing permissions:
1. **Adopt FF4's fix as nature v16 by the safe path** (estimate 95%). The steps:
   - code_v16 with zero checks (off = v15; on = FF4's arm f; live = v16; acts; reload);
   - reference hashes regenerated and the tests passing;
   - tag `nature-v16`, a line in `docs/autonomous_decisions.md`, and Telegram.
2. **Freeze the part-making funnel next** (PF-style, read-only on v16), with all three models' amendments: depth, the
   separated failure reasons, and the post-make stage.
3. **Freeze the dependents' feeding look** as a separate read-only study.
