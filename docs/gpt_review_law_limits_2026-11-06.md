# Council on the hand-limits audit (6 November 2026, evening)

The question: `docs/q_law_limits_2026-11-06.txt` (the same text to all three, fresh chats). Audit: `docs/law_limits_audit_2026-11-06.md`.
Chats: GPT https://chatgpt.com/c/6aee57fc-1fdc-83ea-b68b-12328ff42537 ; Gemini https://gemini.google.com/app/bcb733d3360cc674 ;
DeepSeek https://chat.deepseek.com/a/chat/s/688086a7-7114-43fa-bed8-9981b8141b5f .
**Each answer below is that model's opinion, not sign-off.** Summaries in the assistant's words; quotes are short.

A slip, recorded: the ChatGPT input box held an old unsent draft (the CI1 blind-recompute request), so the first send
glued the two together (chat 6aee5789). That reply was abandoned unread; the question was re-sent alone in a new chat
(6aee57fc), with the box cleared first. Lesson: clear the ChatGPT box (selectAll + delete) before inserting.

## Round 1
**GPT.** All 17 have something worth investigating. Hand limits: 1-9, 11-13. Mixed: 10, 14 ("major concern"), 15, 16,
17. First: (1) attack eligibility alone, no hunger bonus; (2) taking/stealing; (3) the forced hunt split; then (6)
automatic retaliation. Disagrees with "any act": should be "any physically and cognitively feasible action".
Missed: one action a week may be the biggest abstraction; audit every event that changes another person's state
without their choice. Log offered / chosen / attempted / successful separately. "The target is not more violence."

**Gemini.** Hand limits: 1-8, 12, 13; 9-11 are missing verbs that must be built. Called 14-17 defensible. First: (4)
hunt split, (1) attack, (5) lifelong pairs. Said threat/display (11) must exist before attack opens. Suggested combat
"might be fundamentally non-lethal" (wrong, see checks).

**DeepSeek.** Hand limits: 1-14; mixed 15-17. First: one bundled conflict law (attack + threat + flee + chosen
victim response), then take/keep/guard/steal, then group defence. Missed: softmax temperature and score scales are
hand parameters too.

## Checks by the assistant (code read this session)
- Combat is already lethal and costly: the loser of a blow loses 25-55 health, a losing attacker 15-35
  (`acl/actions.py:843-848`); LH1's longer look-ahead arm raised killings 2 -> 116 (conflict audit). Gemini's
  "non-lethal" guess is wrong; told to Gemini and to the others.
- **Winning a fight gains nothing.** `_attack` moves no food or things; a dead person's goods go to a partner or grown
  child on the spot, else to the ground (`acl/biology.py:593-620`). And with grudge 0 the attack score has no
  positive term (`mind.py:488-489`: only minus kindness, fear, 0.15, affection). So removing the grudge gate alone
  would open attacks with no reason behind them. This supports Gemini's "attack without stakes only tests baseless
  murder".

## Round 2 (each given the others' main point and the code fact)
- **Gemini** keeps the hunt split first; concedes threat is a new verb and should be its own test; now calls 14
  "forced outcomes" (rewards for kindness and sociability).
- **GPT** withdraws attack-alone first: "open forced hunt sharing/possession first", then a minimal conflict system,
  then take/keep/guard, then pairing and group defence; threat/display before or with attack, tested alone first.
- **DeepSeek** drops its bundle: attack alone first, then the hunt split, then taking; threat a separate later test.

## What survived (the council's view; the creator decides)
1. Items 1-9 and 11-13 are hand limits (all three agree). 14-17 are mixed: body or instinct in part, hand-written in
   the exact numbers.
2. One gate per frozen test; new verbs (threat, guard, coalition) are new laws, each its own test.
3. First test: **who holds a kill** (remove the forced equal split; the meat goes to whoever holds it, and sharing
   becomes a choice). 2 of 3 in round 2, and the code check (fights gain nothing) backs it.
4. Then the attack gate, with a reason to fight: a contested thing. Threat/display as its own test near it.
5. Harm checks as in CI1 (killing, starvation, living-weeks, extinction, children), plus offered/chosen/attempted
   counts, a sham, paired seeds, no retuning after results.
Nothing in nature changed. Waits for CI1-C to finish.
