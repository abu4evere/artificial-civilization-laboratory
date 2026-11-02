# SC1 — a scorecard of the creator's twelve capacities on live v11 (DRAFT for the council, 2 November 2026)

**Status: a draft, not frozen.** It comes from debate round 46 (`docs/debate_round46_bob_twelve_2026-11-02.md`),
where GPT and Gemini each put a read-only scorecard first at 90%.

**What it is:** read-only, live v11, no change to nature. It needs a frozen plan (`questions.md`, tag `SC1-frozen`)
before any code or data.

## Principles (from the round)
1. **One measure per capacity, each with its own control.** The measure must ask something that no single written
   formula answers.
2. **Three labels:**
   - **"Measured"**, when the behaviour can occur in v11;
   - **"Given"**, when it is written as a law, so there is nothing emergent to score;
   - **"Not measurable in v11"**, when no mechanism exists. Such a capacity is **never scored zero** (GPT).
3. **No combined score.** Each measured capacity gets one reading: **"evidence"** if its contrast's 95% interval lies
   above 0, otherwise **"no evidence"**.
4. **New seeds and the same setting as recent studies.** LP, 200 years, years 100–200 counted, world bootstrap.
   Population is reported beside every measure.

## The twelve, checked against the code
| # | capacity | label | measure (and its control) | source in v11 |
|---|---|---|---|---|
| 1 | Perception | **Given** | Senses are fixed laws: reach 3, sight 4, the 12 nearest people. Described only: what share of decisions see company, food or water. | `mind.decide`, `config` |
| 2 | Memory, relevant retrieval | **Not measurable** | Memories reach choices only by salience × strength (grief, the worst memory, gossip); nothing recalls a memory because it matches the present. Described only: the count, and lived against told. | `thought.py` 116–132, `information.py` 148 |
| 3 | Learning; transfer | **Measured; transfer not measurable** | Learning: adults' calibration, mean abs(q − G) at k 80+ against k 0–19 (UV1's measure, on new seeds). Transfer: the habit table is per situation, so it cannot generalize. | `biology._learn` |
| 4 | Causal understanding | **Measured (proxy)** | After a test that refutes a belief about what to leave where, or a puzzle tested with a large gap: the share of the next same-domain acts that use an **alternative means** (another thing, season or place), against the same share after a confirming test. | `inquiry.surprised`, `knowhow.associate` |
| 5 | Planning | **Measured (proxy)** | Gathering a material a known recipe needs, then a make of that recipe within 26 weeks, against gathers of materials no known recipe needs. And a part made, then the whole that uses it within 52 weeks. | `_material_wants`, `_wanted_parts` |
| 6 | Invention | **Measured** | New kinds per 100 adult-years (first in the world register), and the share **made again by choice** (a make, by anyone) within 5 years, against the same share for kinds first met by learning. | `world.knowledge`, `actions._make` |
| 7 | Own goals | **Measured (proxy)** | Puzzles from a person's **own** surprise that are later acted on, against told puzzles, at matched hunger. "Focus" is attention with inertia, so this is a proxy, not a stored goal. | `inquiry`, `information._wonder`, `thought.steer` |
| 8 | Self-model | **Not measurable** | Nothing represents a person's own ability or uncertainty. Decisions read skill only inside written formulas (hunting, foraging). | `mind.py` |
| 9 | Communication | **Measured** | Places told (water, game): the share **verified** when the listener checks, against the share verified for places the speaker relayed second-hand; and how often thirsty listeners with no own spring reach told water. Lessons: the share of taught recipes the learner later makes. | `information.tell_place`, `tested`; `show_how` |
| 10a | Social cognition | **Measured** | Share of know-how gained socially (taught, copied, read) against made alone. Given channels, measured use. | `knowhow.remember_recipe` |
| 10b | Cumulative culture | **Measured** | (i) Kinds alive whose first maker is dead; (ii) the distinct holders a kind passed through; (iii) the **nesting depth** of known made things (parts that are themselves made), years 100–125 against 175–200. | `world.knowledge`, recipes |
| 11 | Motivation and regulation | **Given** | Drives, feelings and their decay rates are written. Regulation does not emerge separately. Described only. | `biology._feelings` |
| 12 | Identity and continuity | **Measured** | How well a person's own action profile in year t predicts their profile in year t+5, beyond temperament, age, sex and situation, cross-validated. This is level A of the autonomy note (self-driven behaviour, **not** chosen goals). | all decisions |

## Expected picture (the assistant's prior, to be frozen)
- "Given" for 1 and 11; "not measurable" for 2, 3-transfer and 8.
- **Evidence** for 3-learning, 6, 9, 10a and 12.
- **Weak or no evidence** for 4, 5, 7 and 10b(iii).

## Open questions for the council (debate round 47)
1. Is each measure free of a single-formula echo? Especially 5, which the `_material_wants` pull favours, and 7, which
   the steer bonus favours. The controls are meant to absorb that; are they enough?
2. Is 12 a fair identity measure, or does it only re-measure the habit table's persistence?
3. Should the reading per capacity be "evidence or no evidence", or should SC1 report the contrasts only, with no
   reading at all?
4. Seeds and size: 32 worlds as before, or fewer, since nothing is compared between arms?
