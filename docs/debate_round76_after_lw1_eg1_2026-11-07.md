# Council round 76: after LW1 and EG1, toward the making wall (7 November 2026)

The question: `docs/debate_round76_question_2026-11-07.md`. GPT (main chat), Gemini (ACL chat) and DeepSeek (ACL chat
2552dbba) got the same text. **Each answer is that model's opinion, not sign-off.**

## Answers

**GPT's opinion, not sign-off.**
- Verdict: "Correct the best-tile fault first, then investigate the made-part bottleneck. Set LW1 aside."
- (a) A fault, "an unintended inconsistency between feasibility and option generation". Fix it by the fault path with
  a frozen harm check and a sham:
  - choose the best tile among the affordable ones, by the existing ranking;
  - keep the original behaviour when the best is affordable;
  - change no cost.
  - Check starvation, child deaths, adult health, population, extinctions and food production. Given the 35% exposure
    of the dying, prioritise the harm check.
- (b) Set LW1 aside; do not rerun it now. "Do not reinterpret it as supported because alternative bootstrap draws cross
  zero." It may be paired later with a making mechanism, as a new hypothesis.
- (c) A read-only lifecycle audit of made parts. It tracks:
  - the parts' depth;
  - whether they are consumed, given, set down, worn out or lost;
  - whether a set-down part is recovered;
  - whether the full input set ever exists at once;
  - whether the make is then offered and chosen.

  The primary outcome is the distribution of kinds across mutually exclusive failure stages: parts never produced, or
  produced but not kept, or kept but never assembled. No curation law until this is measured.
- (d) Worth a look, but after the fix and the audit. Condition on circumstances, and make no sex-specific change.
- (e) 98% that the fix is a valid fault-fix candidate; 95% that its harm check is informative; 97% that the audit finds
  a meaningful bottleneck.

**Gemini's opinion, not sign-off.**
- (a) A fault, "a search-algorithm bug, not a behavioral law"; the fault path with a harm check.
- (b) Pair LW1 later with a retention or curation law. Rerunning it now is a waste, while making by non-inventors is 0.
- (c) The read-only audit of where made parts go, before any curation law.
- (d) Yes, a read-only look alongside. Its guess: carrying infants restricts women's movement, so the best-tile fault
  hits them more.
- (e) 95%.

**DeepSeek's opinion, not sign-off.**
- (a) A fault, "an interaction between two steps"; the fix offers the best affordable tile instead of dropping forage.
  The check is like FF1 and FF3: a zero check (off = v15), a separate arm and a sham.
- (b) Drop LW1 as a supported law, and do not rerun it now ("a rerun on new seeds would be fishing"). Record its
  directional signal, and revisit it with a making law.
- (c) The parts-flow audit, on new kinds 3 or more parts deep. Follow every made part from creation: worn out, used in
  another thing, set down and not retrieved, given away, inherited. The funnel runs: never all made → all made but not
  held together → held together but the make not offered or not chosen.
- (d) Not a separate study now: the fix may shrink the gap. Re-measure it inside the fix's study as a described
  measure.
- (e) The fix about 92%, the audit about 90%, a LW1 rerun about 55% (not recommended).

## Checked against the code (Claude)
- **The same structure is in three actions, not one:** forage, hunt and gather. Each picks its best target without
  regard to energy, then `add` drops the whole action if that target is unaffordable. The fix is written for all three:
  one rule, "the target is chosen among what you can afford". It is not a forage-only patch.
- **`best_forage`** (the best food in sight) also steers exploring. The fix leaves it as the unconstrained best, because
  it measures what is around, not what is affordable. So exploring is unchanged.
- **Gemini's guess that carrying infants restricts mothers** is not checked here. ACL has no carrying cost for infants
  that this round looked at, so the gap is left to FF4's described measure, as DeepSeek proposed.

## Decision
The assistant, under the creator's standing permissions:
1. **Freeze FF4**, the fault fix for forage, hunt and gather, with CI1's eight guards, a sham, and EG1's measures
   re-measured per arm, including the women's gap. Estimate 88%.
2. **Then freeze the parts-lifecycle audit** (read-only on v15) as the next study toward the making wall.
3. **LW1 is set aside,** to be paired later with a making law as a new hypothesis.
