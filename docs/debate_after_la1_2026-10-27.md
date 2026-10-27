# Debate round 9 (27 October 2026, sleep mode): after LA1, which first? (opinions, not sign-off)

The creator was asleep. Under sleep-mode autonomy, the assistant put the same question to GPT (main chat) and Gemini
(ACL session), with Claude as council.

**The candidates:**
- **(A)** a parts-first audit;
- **(B)** a memory audit;
- **(C)** a value-calibration audit;
- **(D)** an Expected SARSA nature-change study.

## First answers
- **GPT: (A), 85%.** "The crucial question is whether ACL's intended solution — teaching the missing part first —
  actually works." Its order is A, B, C, D:
  - B is second, because eviction could interrupt the chain;
  - D is last, since changing nature before knowing whether learning works is premature.

  It cautions that LA1's flat per-lesson acceptance and NA1's per-kind fall have different denominators, and that the
  ×8.1 replay is not a prediction.
- **Gemini: (A), 95%.** G4 is "the single largest empirical bottleneck". It also called the audit a "deterministic
  replay".

## Council checks
| claim | who | check | result |
|---|---|---|---|
| The audit is a deterministic replay | Gemini | It is a read-only observer on 32 new worlds; zero checks prove it changes nothing | corrected (told) |
| Parts-first shows the missing part | (design assumption) | `hear_how` shows the **first** made part the teacher knows, without checking the learner; there is a second belief draw; it goes one level deep | told to both; built into PT1 |
| A just-taught recipe competes for memory at its lesson value | (design assumption) | `remember_recipe` adds it at 0 and evicts **before** `hear_how` sets 0.5 × claim × credence | told to both; built into PT1 (Q3) |
| Signature tie-breaking penalises composites, "as identified in E7.7" | Gemini | Composite signatures begin with "(", which sorts before letters, so on a tie a composite is evicted first. **E7.7 found something else** (watching almost never passes things on) | the measurement is adopted (Q3); the citation is wrong |

## Design notes adopted into PT1
- **GPT:**
  - the full set of missing parts and the stopping gate of the part lesson;
  - conditional probabilities at every step;
  - an exact one-event memory replay (lesson value set first);
  - chain ids, censoring (death, run end), and acquisition by any route;
  - recursive depth;
  - **primary: the share of G4 failures parts-first can reach at all, then completion among the reachable.**
- **Gemini:**
  - the "blind teacher" subtypes: the teacher knows no part; the teacher shows an already-held part; the part is too deep;
  - composite eviction against the held share;
  - the cost of the second belief draw.

## Predictions on record
- **GPT:** several independent bottlenecks (wrong part, second draw, eviction, depth), not one.
- **Gemini:** the blind teacher and the memory order are "devastating structural design flaws".
