# Debate round 7 (27 October 2026): habits first, or lessons first? (opinions, not sign-off)

**The creator:** "ask gpt and gemini which one to do first". The same text went to GPT and Gemini, with Claude as
council:
- **(1)** what drives the habits (own TD learning, copying whole habit tables in talk, children absorbing the carer's
  table; a rich-get-richer loop?);
- **(2)** why lessons stop being taken after year 50.

## Both: (1) first, (2) second, separate studies
**GPT:** "my vote is (1)". CO1 found the dominant score component, "not yet its causal origin". Even the few lessons
taken are rarely made, so raising uptake alone "could result in many more people knowing recipes that they still never
manufacture".

**GPT's design for (1), a read-only habit accumulation audit:**
- **H1, sources:** every habit update attributed to its source (own TD update, copying in talk, carer absorption), with
  old and new value, situation, action and source person. The ledger must close exactly: ΔH = ΣΔH_TD + ΣΔH_talk +
  ΣΔH_carer.
- **H2, what rewards reinforce it:** action, reward, TD target and error, future-value part, update.
- **H3, rich-get-richer:** does early action frequency predict later habit growth, and does that predict later choice,
  conditional on opportunities? A key negative test: do rarely done actions still gain habit through copying?
- **H4, social amplification:** which habits are copied, from whom to whom, and whether copying increases their
  competitive advantage.
- Report each source's contribution to the **choice score**, not only to raw habit values.
- **Caution:** the ledger is accounting, not causal attribution. An "imitation off" test would be a later, frozen
  intervention.

GPT's leading hypothesis (not a finding): "social learning might be transmitting behavioral conservatism more
effectively than technological knowledge". It would change nothing in γ, the imitation rule or openness until that
survives the audit. On (2): a failed lesson is not necessarily a malfunction (poor timing, an irrelevant lesson, a
variant already held, rightful distrust). The audit should establish whether acceptance is malfunctioning, not assume
that more is better. Shared observer infrastructure is fine, but keep separate plans and inference.

**Gemini:** (1) first. It proposed a split of habit growth into TD, peer copying and carer absorption, and a
frequency-asymmetry ratio between forage and make. Keep the studies separate.

## Council checks (Gemini accepted all three)
| claim | check | result |
|---|---|---|
| NA1's lesson-taking collapse is a downstream symptom, since taking a lesson cannot beat U_other in the decision | Taking an offered lesson is decided inside `information.hear_how` (credence × openness), not in `mind.decide`; habits matter at most indirectly | **Withdrawn** |
| "0.86 of make's 1.03 log-odds collapse"; "restores 83%" | Habit is 0.86 of the rise in U_other; setting habits back undoes 0.86 of the fall in log-odds | **Corrected** |
| Zero imitation as part of the study | That is an intervention on nature, not read-only; GPT's update ledger is the read-only design | **Withdrawn; GPT's design adopted** |

**Agreed:** (1) first, as a read-only, source-attributed habit-update audit; (2) after it, separately. No change to
nature yet. (The ID "HB1" is taken; the study needs another name.)
