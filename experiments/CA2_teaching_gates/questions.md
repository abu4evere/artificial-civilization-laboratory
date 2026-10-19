# CA2 — Why does teaching pass on so little? (SIGNED OFF 19 October 2026; frozen as `CA2-frozen` before any code or data)

**Why.** CA1 (`../CA1_chain_audit/findings.md`, `CA1-done`) found that the chain of cumulative culture breaks at the
first hand-over: only **11% (discovery) and 10% (holdout)** of useful inventions are ever learned by anyone but their
inventor, and about nine in ten first hand-overs are teaching. Before anything in nature is changed, the rule (Rule 12)
is to find where teaching itself loses them. CA1 also left one caveat open: "built on" may be one person improving their
own work. **Read-only: nothing in ACL changes.**

## Questions

1. Of the useful inventions never passed on, at which gate of teaching did they stop?
2. (CA1's caveat) Of the kinds built on, how many were built on by someone other than their first knower?

## How teaching works today (read from `code_v2`, 19 October 2026)

A person can teach only during a `talk` with someone aged 4 or more (`actions._talk` → `knowhow.teach` →
`information.show_how` → `hear_how`). In order, the gates are:

| gate | rule in the code |
|---|---|
| G1 **meets** | the inventor talks with anyone at all while they know the recipe |
| G2 **valued** | the inventor's own value of the recipe (`itemval`) is above 0.15 |
| G3 **offered** | it is among the inventor's top three offers, which recipes **share with beliefs** about where to leave things |
| G4 **chosen** | one of the (up to) three is picked at random |
| G5 **new to the learner** | the learner does not already know it (as they understood it) |
| G6 **believed** | not refused because the learner already tried it and found it no good; then a draw against the learner's credence in the teacher × openness (0.35 × (0.5 + curiosity), doubled from a parent) |
| G7 **followable** | the learner can make any made part it needs (`can_follow`) |
| G8 **kept** | the learner holds it for at least a year: a person keeps at most **12 recipes**, the least valued dropped first (`MAX_RECIPES`), and useless ones are forgotten |

A recipe can also change as it is shown (`_recipe_as_shown`): the learner may take away a different kind. CA1 counted
that as a new kind; CA2 reports how often it happens.

## Design (the assistant's recommendation; decisions marked)

- **Instrument (Decision 1):** a logging copy of `code_v2` that writes, at each gate above, what happened, and nothing
  else, as HF4 did; **shown to change nothing** (state hash equal to `code_v2` with and without logging, seeds 501 and
  601, 20 years). Alternative: an outside observer only, which cannot see gates G3–G6 (they happen inside one week).
- **Worlds (Decision 2):** **CA1's discovery seeds 6301–6316** replayed exactly (each replay's final state hash must
  equal CA1's saved one), so the two audits describe the same worlds; then **holdout on CA1's holdout seeds 6317–6332**.
- **Also saved (question 2):** who first knew each kind and who first made each better kind built on it.
- **Computer:** two spare workers, as CA1 (about 1.5 hours).

## The frozen reading (proposed)

- For useful inventions never passed on, each gate's **pass rate** (attempts passing ÷ attempts reaching it), pooled.
  **The blocking gate** is the one with the lowest pass rate; it counts only if it is the same gate in discovery and
  holdout. Also the share of useful inventions whose inventor **never reached G1** (never talked with anyone while
  knowing it).
- Question 2 is described: of CA1's link-5 kinds, the share built on by someone other than the first knower.
- Population is shown beside (rule 18). It locates the gate; it does not show that opening it would build culture.

## The assistant's prior (to be frozen at sign-off; held loosely)

Blocking gate **G3, offered**: an inventor's many recipes and beliefs compete for three places, so most useful
inventions are never even offered. Second guess: G6, believed. Question 2: most building on (over half) is the
inventor's own work. (My last prior, on CA1, was wrong.)

## Decisions for the creator

1. Instrument: **a logging copy shown to change nothing** (recommended), or an outside observer only.
2. Worlds: **CA1's seeds, discovery then holdout** (recommended), or new seeds.
3. Include question 2 (**yes**, recommended) or leave it.
4. Order: **now, on two spare workers** (recommended), or after FX2.

## GPT's science review (19 October 2026, under the creator's delegation; a review, not a sign-off)

GPT: "Recommend CA2 for Abdurashid's review, with these refinements. Do not freeze it on my authority." Its points, in
short (full wording in the AI World chat), and how the draft now takes them:

1. **"Define the denominator for every gate"**: entering, passing, pass rate with its base, and how many were finally
   passed on. → Adopted: the table reports all four for each gate.
2. **"Separate the first failure from the biggest loss"**: a gate with a low pass rate may touch few inventions. →
   Adopted as **Decision 5**: the reading is either (a) the lowest pass rate (as drafted) or (b) **the gate where the
   most useful inventions stopped for good** (each never-passed invention assigned to the furthest gate it ever reached).
   Recommended: **(b) as the reading, (a) beside it**, both required to agree across discovery and holdout for "one
   bottleneck"; otherwise "no single bottleneck".
3. **Who built on what**: "Original inventor. Someone who learned the invention. Unclear or unrecorded", and whether the
   improved version was passed on. → Adopted for question 2.
4. **"Report teaching and watching separately through the gates."** → Adopted: watching has its own gates (W1 a learner
   sees the thing made and it worked; W2 the 4% × curiosity draw; W3 the copy is new and followable), reported beside
   teaching's.
5. **Integrity:** CA1's exact seeds (replays checked against CA1's saved state hashes), discovery and holdout kept
   separate, missing or ambiguous gate records counted and shown, no threshold changed after results. → Adopted.
6. **"Track the 12-recipe limit explicitly at G8"**: a learner who drops it because the limit pushed it out, forgot it
   as useless, or died, reported apart, "otherwise, label the reason unknown". → Adopted.

GPT's boundary, kept: "identifying a gate associated with failure does not prove that changing it would increase
cumulative culture. That would require a separate, preregistered intervention."

**Decision 5 for the creator:** the reading: **the gate where most stopped, lowest pass rate beside** (recommended), or
the lowest pass rate alone.

## Sign-off (19 October 2026)

The creator: "**approve all CA2 recommendations, freeze it**". So: (1) **a logging copy shown to change nothing**;
(2) **CA1's seeds, discovery 6301–6316 then holdout 6317–6332**, 120 years; (3) **question 2 included**; (4) **now, on
two spare workers**; (5) the reading: **the gate where most stopped, lowest pass rate beside**. GPT's six refinements
(above) are part of the design. The prior above is frozen as written.

## Operational details (fixed at freezing, before any code)

- **Code `code_ca2`:** a copy of `code_v2` plus logging lines only, writing to a list the runner sets on the world
  (`world.ca2log`, not saved, read by nothing in the world; HF4's pattern). Logged: every `talk` in which teaching is
  possible (teacher, learner, the teacher's recipes at that moment); every `show_how` (the recipes valued above 0.15,
  the top three offers, the one chosen); every `hear_how` (its outcome: already known, refused as tried and no good,
  not believed, not followable, taken; and the kind taken); every `watch` (its outcome: already known or not the
  maker's, outcome not good, the draw failed, copy not new or not followable, taken); every recipe dropped (pushed out
  by the 12-recipe limit, or forgotten as useless).
- **Hard stops:** state hash of `code_ca2` with logging on equals `code_v2`'s (seeds 501 and 601, 20 years); every
  replayed world's final state hash equals CA1's saved `world_hash` for that seed; one fingerprint. No outcome is shown
  if any fails. Missing or unmatched log records are counted and reported.
- **Useful inventions** and their links: exactly as CA1 (CA1's observer, loaded unchanged), now also saving each kind's
  first knower.
- **Gates, per useful invention never passed on** (no one but its first knower ever learned it), over its first
  knower's teaching attempts: G1 reached if the first knower ever took part, as teacher, in a teaching-possible talk
  while knowing it; G2 if it was ever among their recipes valued above 0.15 at a `show_how`; G3 if ever in the top
  three; G4 if ever chosen; G5–G7 by `hear_how`'s outcome when it was chosen (G5 passed if not already known; G6 if
  not refused and believed; G7 if followable). **Where it stopped** = the furthest gate it ever reached and did not pass
  (or "never reached G1"). Entering gate g = inventions that reached g; passing = those that got beyond g; pass rate =
  passing ÷ entering.
- **Reading:** (b) the gate where the most never-passed useful inventions stopped, and (a) the gate with the lowest
  pass rate. **"One bottleneck: gate X"** only if (b) is X in both discovery and holdout and (a) is also X in both.
  If (b) agrees across the sets but (a) does not: "most stopped at X; lowest pass rate elsewhere", both reported. If (b)
  differs between the sets: "no single bottleneck".
- **G8 (kept a year), described:** for each learner who took a useful invention by teaching or watching, whether they
  still held it 52 weeks later, else why: pushed out by the limit, forgotten as useless, died, or unknown.
- **Watching, described beside:** for useful never-passed inventions, the watch outcomes, as counts.
- **Question 2, described:** for each CA1 link-5 pair (part X, better kind Y): Y's first knower is X's first knower
  ("the inventor"), or someone who had learned X ("a learner"), or neither ("unclear"); and whether Y was passed on.
