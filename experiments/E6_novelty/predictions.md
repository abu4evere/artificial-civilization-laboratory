# E6: Can the world still surprise itself? · Predictions (FROZEN)

**Question** (the creator's): *Can the world still create genuinely new behaviours after year 100?*
Population, survival and births are not the measure.

**Written:** 2026-10-03, before the baseline run and before any E6 code exists. Not to be edited after results.

**Decisions taken by the creator (2026-10-03):**
- Build the core processes only (heat, wetting and drying, containers that hold things, clay). Weight and placed-thing
  physics come later, so that E6 tests one idea.
- All matter properties are whole numbers from 0 to 10, from day one.
- The main measure is the **latest first appearance**.

## Design

- **Baseline:** today's code (world 0.3, agent 0.3; the E5 code, kept as a verified copy in `code_baseline/`), seeds
  301–308, 1000 years, with the novelty recorder. The world is deterministic and the recorder only reads, so the
  baseline is E5 again, measured more finely. Check: the population at year 1000 must equal E5's.
- **E6:** the new physics, the same seeds 301–308 (same maps and founders), 1000 years, with the same recorder.
  Worlds are compared seed by seed.
- The recorder must be proved read-only: identical state hash with and without it over 20 years, under each code.

## Definitions (fixed in advance)

**Kind of thing.** The item's lasting properties, each put in one of 5 bands. Transient states (heat, wetness)
are left out.
- Baseline: values 0–1, band = value × 5, capped at 4.
- E6: values 0–10, bands {0–1, 2–3, 4–5, 6–7, 8–10}.

**Behaviour.** An event kind together with the kinds of things involved and its object: the material, substance,
place it went into, surface, form, or how. Examples: putting fibre into a heap; making a thing of a given kind;
crossing water on a thing of a given kind. The same rule is applied to every event, old or new.

**Novelty.**
- **New kind:** a kind that had never been made in that world, made by 3 or more different people within 10 years
  of its first making.
- **New behaviour:** a behaviour never seen in that world, done by 3 or more different people within 10 years of
  its first appearance.
- **Lasting novelty:** a new kind or new behaviour that is made or done again at least 50 years after it first
  appeared.

**Latest first appearance (LFA).** For each world, the year in which its latest *lasting* novelty first
appeared. This is the creator's main measure.

**Share after year 100.** The share of a world's lasting novelties that first appeared after year 100.

**New tradition.** A technique, practice belief, mark meaning or behaviour that first appeared after year 100, and
was held or done by 3 or more people in every 10-year sample for 100 years or more.

**New consequence** (E6 only; descriptive, since none can happen in the baseline):
- water carried 5+ tiles from any source;
- fire burning where no lightning or sparks started it;
- food eaten after its natural rot time;
- a held thing changed by heat or water and kept.

**Known bias.** E6 things have more properties than baseline things, so more kinds are possible by construction.
The persistence rules (3+ people within 10 years, and still in use 50+ years later) are there to count only what
people found worth repeating. The comparison rests on *when* novelty appears, not on how much.

## Decision rule (fixed in advance)

Only worlds that lived 300+ years count toward the thresholds; the rest are reported.

- **Breakthrough:**
  - E6's LFA is year 300 or later in at least half of the counted E6 worlds, and
  - E6's LFA is later than the baseline's in at least 6 of the 8 seed pairs.
- **Bottleneck remains:** E6's LFA is year 100 or earlier in at least half of the counted E6 worlds. In the
  creator's words: "If everything still appears by year 20 and then freezes forever, the bottleneck remains."
- **Partial:** anything in between, reported as such.

## Predictions

**The creator's:** the world is a breakthrough if it is "still capable of surprising itself centuries later"; the
bottleneck remains if everything still appears by year 20 and then freezes.

**Claude's:**
1. **Baseline:** LFA at or before year 100 in at least 5 of the 8 worlds, and under 10% of lasting novelties after
   year 100. (Measured finely, today's world may show a few late nested bindings, which is why the baseline is
   measured rather than assumed to be year 11.)
2. **E6:** LFA at year 300 or later in at least half of the counted worlds, so the result is a breakthrough.
3. **E6:** at least 25% of lasting novelties after year 100 in at least 5 of 8 worlds.
4. **E6:** at least one new tradition (began after year 100) in at least half of the surviving worlds.
5. **E6:** no more worlds die out than in E5 (3 of 8 or fewer).
6. **E6:** at least one world produces a thing that came from a plastic material, was hardened by heat, and holds
   water. Reported, not part of the decision rule: the question is not "did they make pots".

## Kill criterion (the experiment is invalid if…)

- any run crashes, or the code changes during the baseline or E6 runs;
- fewer than 6 worlds complete (reach year 1000 or die out) in either arm;
- the recorder changes the world (state hashes differ with and without it);
- the baseline does not reproduce E5's populations at year 1000.

## Amendment (2026-10-03, before any E6 run; no E6 result has been seen)

**Scale of lasting properties: whole numbers 0–100 instead of 0–10.** On 0–10, the older physics loses effects it
depends on. A stick sharpened on a stone reaches edge 0.07, and a stone flaked on stone gains 0.07; on a 0–10
scale both round to nothing. Those strikes then always fail, though in E5 they were among the most common
actions. E6 would then change two things at once: the new physics and a coarser old physics. Whole numbers
0–100 are still discrete (v8.1's rule) and keep the old physics as it was.

Wetness and fire heat stay on 0–10. They are passing states, not part of a kind. **Kinds** keep the same five
equal bands, now `value // 20` (capped at 4), which is what the frozen definition means on any scale. No
prediction, threshold or decision rule changes. The creator is told of this change and may reverse it before
E6 runs.

**The creator's decision (2026-10-03):** the 0–100 scale is accepted. Run E6 exactly as it stands, with fire as rare
as the world makes it ("Do not touch fire"). E6 code fingerprint, sha256 of `code_e6/acl/*.py`: b3f7153accc0e6810cd48e8e384c0c73c22d6030f81cca50212b8e7c046980cc.
