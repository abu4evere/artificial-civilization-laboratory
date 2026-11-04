# The ACL brain: a design draft (3 November 2026; the brain road)

**What this is:** a working draft. Nothing is frozen or built. It goes to the council after PB0's result.
- **Its inputs:**
  - rounds 55–57;
  - AM1 and AM2;
  - a vision the creator shared on 3 November: eight capabilities, cooperating systems, and a "breakthrough sequence".
    The text appears to come from a ChatGPT reply; it is used as GPT's opinion, not as a plan.
- **The rule it keeps** (the shared text and the assistant agree): "We can design the mechanisms that make autonomous
  goals possible. But if we directly write what Bob must want, we've missed the central experiment." Every part is a
  general ability. No part names a goal, an invention or a sequence.

## The eight capabilities: what ACL's people have today (v13, read in the code) and what is missing
| capability | today | missing |
|---|---|---|
| 1. learning relations and generalising | habits per situation (32) × action (19): no transfer between situations; item worths (`itemval`) and beliefs per key (`beliefs`, `expect`) | a learned model that carries a lesson to similar situations and materials |
| 2. autobiographical memory | partly: event memories (`memories`), places (`places`), people (trust, affection, familiarity, grudge, respect), recipes, item worths, mark meanings; but 98% of know-how is lost at death (LS2) | memories that act on choices (today many feed only scores), and what lasts beyond a life |
| 3. imagination and prediction | none: choice = written pull + learned habit; no look-ahead beyond the habit's one-step max | a forward model ("if I do this, then that") — PB0 measures whether it would pay |
| 4. self-generated goals | none: every option is chosen fresh each week; AM1 and AM2 show that habits pull people away from finishing gather-then-make chains (about 7.7× fewer than without habits) | a goal memory: an end held across weeks, formed from experience and never named by us |
| 5. social intelligence | partly: individual relations, gifts, care, courting, watching (`knowhow.watch`), teaching (automatic, `knowhow.teach`), marks with shared meanings | teaching as a choice; learning a model from what others' actions led to |
| 6. creativity and invention | partly: play and strike make new things; but UP1 and AF1 show that late inventions are never made again ("cannot make") | remembering why a discovery was useful, and wanting to remake and improve it |
| 7. metacognition | none (`expect` tracks averages, not uncertainty) | knowing what one does not know: prediction error used to seek information |
| 8. persistent identity | partly: temperament genes, relations, places, recipes | long projects (needs 4) |

**The clearest wall, measured twice:** step "Year 6" of the shared sequence, "deliberately tries to reproduce it".
- In ACL today, a world-new kind made in play is remade by its own recipe within 5 years in **0–2 of about 3,300 cases
  per arm** (AF1's lineage measure R).
- That is the step a goal memory and a predictor are meant to open.

## The systems (the shared picture, mapped to ACL)
1. **Perception and attention:** what the person senses now (already computed in `mind.decide`: tiles, people, things
   in reach).
2. **World model (predictor):** a small learned model of what an action does to the person's food, energy, health,
   materials and things, given what they perceive. It is trained only on the person's own experience and on what they
   see others do.
3. **Memory:** the existing stores, plus the predictor's learned weights. What a child inherits is **readiness** (the
   model's structure and learning rate, as genes), never the weights.
4. **Motivation:** the existing bodily needs and feelings. These are written, as evolution wrote ours.
5. **Self-model:** the predictor's own error by kind of situation ("where am I often wrong?"). It feeds curiosity,
   which already exists in v9 as a pull toward the untried.
6. **Goal formation and planning:**
   - **Forming a goal:** a goal is a predicted future state the person comes to value, for example "holding a
     cutting thing" or "having stored food". It forms when the predictor shows a state that would have raised their
     outcome often in the past.
   - **Holding it:** the person keeps it for weeks.
   - **Planning:** a short planner (2–4 steps) uses the predictor to choose actions toward the goal.
   - **The rule:** goals are states, never named things. The code knows no "spear", only properties (edge, reach,
     hardness…).
7. **Action → world → learning:** as today.

## The order (the shared text and rounds 56–57 agree)
1. **Predictive learning and generalisation** (PB0 gates it; if NO-GO, goal memory comes first).
2. **Persistent memory that acts.**
3. **Goal formation and maintenance.**
4. **Planning.**
5. **Metacognition and social learning of models.**

Each step is a frozen nature-change test in a copy: council, a sham, blind recomputes, the safe path.

## How success is measured (no named invention)
Each is a measure that already exists or can be built read-only:
- **Remaking:** AF1's lineage R, the share of new kinds remade within 5 years.
- **Improvement:** a remade kind's later versions score better on their own use (food, cutting) than the first.
- **Passing on:** a kind still made 20 years after its inventor's death.
- **Goal-holding:** AM's chain measures (M3, M5), re-validated in the new brain's own battery; M2 (sequence structure),
  the one measure that held in AM1 and AM2.

The shared "breakthrough sequence" is then a pattern these measures can detect: discovered, remade, improved, taught,
outlives its inventor. It must never be written as a target.

**"Remade" is not "remade on purpose"** (the creator, 3 November 2026: "Making something again isn't necessarily making it
again on purpose."). A remake can come by chance (play, a habit, a lucky mix of materials at hand). Intent has to be
shown by tests that chance cannot pass:
1. **Above chance.** The inventor remakes more often than matched people who had the same materials and chances but
   never made the thing.
2. **Prepared.** The make follows gathering of its specific inputs that the person did not otherwise need, as in M3:
   preparation against opportunity-matched weeks.
3. **Persistent.** After an interruption (hunger, a move), the person comes back to it, as in M5.
4. **Causal (the strongest).** In a copy of the world, the person's memory of the discovery is removed (its worth, or
   the goal), and nothing else changes. Remaking must then drop. If it does not, the remake was not driven by the
   memory, and it was not on purpose. This uses PB0's copy method.
5. **Flexible.** The person reaches the same end by a different route when the usual input is missing (a substitute
   material, or a new place).

A goal memory is internal state we built, so we can read it. Reading it is not evidence, though: only behaviour that
passes tests 1–5 counts.

## Open questions for the council (after PB0)
1. **The predictor:** linear over a fixed set of perceived features, or a small network? Which features, so that no
   outcome is built in?
2. **Goals as valued predicted states:** is this a general law, or does it sneak in a target? How is "valued" learned?
3. **Data:** about 2,000 weekly choices a life (round 56). How much should come from watching others versus one's own
   acts, and how are those weighted?
4. **Cost:** a world 10–100 × slower. Should worlds be smaller and longer, or larger and shorter?
