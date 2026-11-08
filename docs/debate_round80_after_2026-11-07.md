# Council round 80: the doors package (7 November 2026)

The question and the follow-up: `docs/debate_round80_question_2026-11-07.md`. GPT answered in a fresh chat
(https://chatgpt.com/c/6aeff36a-4664-83ea-81f5-92b44edc78d8), with one line of context added, because the creator was
using the main chat and the old council chat was frozen. Gemini (ACL chat) and DeepSeek (ACL chat) got the same text.
**Each answer is that model's opinion, not sign-off.**

## First answers
**GPT's opinion, not sign-off.**
- (a) D1–D5 are general laws. D1's ±10 "is a tunable parameter, even if applied universally". Heaps out is right.
- (b) Missing doors: made shaping tools, made heating tools, repair. But do "not delay the December freeze", and repair
  "introduces new behavior rather than merely removing a restriction".
- (c) One package, plus per-door checks; single-door arms would be ideal.
- (d) Diagnostics: hoarding, combat by layered protection, resource displacement, runaway carrying.
- (e) 75%. "Describe the result as 'no detected harm under the tested conditions,' not 'the doors are harmless.'"
  "Stop optimizing the world to produce intelligence."

**Gemini's opinion, not sign-off.**
- (a) "Pure general laws"; heaps out is right.
- (b) Missing doors: a made cutting tool (edge ≥ 50), made fuel, repair.
- (c) One package: "separating them will yield almost zero signal per arm".
- (d) Encumbrance starvation, recursive crafting loops, endless layering.
- (e) 80%. Its risk: "'no harm' might simply mean 'no data'".

**DeepSeek's opinion, not sign-off.**
- (a) D2–D5 reuse existing constants. D1 should be recorded "as a calibrated constant, not a law-derived value". Heaps
  out is right.
- (b) Missing: containers holding things (D6). Not repair, and not made shaping tools.
- (c) A package with one split arm, doors without D1.
- (d) Descriptives: killings by made-hammer holders, the factor of stand-in-made things, the spread of carried things,
  and the manipulation counts "as a pre-condition".
- (e) About 85%. Pre-register "no harm, doors barely exercised".

## Checked against the code (Claude), sent back to all three
- **Made fuel is already open.** A made thing held in a fire burns and feeds it (`actions._hold_in_fire`).
- **Made cutting is already open.** Any made thing's edge counts in `matter.factor`.
- **"Containers hold things"** means carrying room in ACL, which is D2.
- **There is no weight cost to moving.** The item and material limits are the only stand-in for weight.
- **Repair needs a new constant,** so it stays out. Shaping is done by hand.

## Final answers
**GPT's opinion, not sign-off.** "No objection. … ensure the eight guards are evaluated separately against v16 for both
candidate packages, with sham results reported as a validity check."

**Gemini's opinion, not sign-off.** "No objection; the design correctly tests the properties as general physical laws
with appropriate safety boundaries and isolates D1's substitution risk."

**DeepSeek's opinion, not sign-off.** It objected that the "at most double, also with D5" claim needs checking:
uncapped layering of two contain-100 containers "give[s] … 2.5, not 2". "Otherwise no objection."
- **Taken:** D5 caps the layered value at 100, as `bind` caps `_layer`. So carrying is at most doubled.

## Decision
OD1 is frozen with arms v16 / doors / doors without D1 / sham. The gate is CI1's eight guards. The creator's no-harm bar
and the fallback order are pre-registered.
