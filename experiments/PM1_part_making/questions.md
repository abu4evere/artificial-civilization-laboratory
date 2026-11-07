# PM1: why are the parts of new kinds never made again? (frozen plan)

**A read-only audit of nature v16.** Council round 77 chose it unanimously (`docs/debate_round77_after_ff4_mp1_2026-11-07.md`;
GPT 97%, Gemini 95%, DeepSeek about 90%), with their amendments built in:
- split by depth (GPT, DeepSeek);
- separate failure reasons (GPT);
- a stage after the make (DeepSeek);
- kinds, not repeated weeks, as the unit (GPT).

**Nothing in nature changes, and PM1 decides no law.**

## Why
**MP1:** for 0.902 of 3,690 new kinds that need a made part, no one who knows the recipe ever holds even one of its
made parts again within 5 years (0.965 at depth 3+). The parts are never remade.

**The make rule in the code** (`mind.decide`, the make block): a recipe is offered for making only when all of these
hold:
- the person knows it;
- the inputs are in hand (`can_make`);
- its value is above 0.05.

The value is the higher of:
- what the thing itself did for them (`itemval`);
- 0.8 × the value of a whole they want that it goes into (`_wanted_parts`), and only when that whole is valued above 0
  and not held.

**Only one make option is offered a week:** the best of the eligible ones.

## Design
- **Code:** `code_v16` (nature v16, live since 7 November 2026), unchanged. One arm, no sham. LP (80 founders, 80 × 80).
- **Seeds 25001–25032** (32 new seeds, used by no study). 200 years. Kinds born in years 100–190 are followed for 5
  years each, as in MP1.

## Followed kinds and their parts
- **Which kinds:** world-new kinds whose recipe needs at least one made part (MP1's rule).
- **Their parts:** for each kind K, its **direct made parts** X, read from K's recipe in `world.knowledge`. Depth is
  MP1's.
- **Knowers:** a knower of K is a living person whose recipes include K at a week's end.

## Primary: the furthest part-making stage each kind reaches
For each followed kind K, over the 5 years after its invention week, take the furthest stage reached for any of its
made parts X, by any knower of K. The stages, in order:

| stage | reached when, for some knower of K and some made part X of K |
|---|---|
| **P0** | the knower does not know X's recipe. Split into **P0a**, where no living person in the world knows X's recipe (the prerequisite is lost or was never learned), and **P0b**, where someone else knows it |
| **P1** | the knower knows X's recipe, but never has its inputs in hand (`can_make` false at every look) |
| **P2** | the knower knows X and has its inputs at some look, but X is never valued above 0.05 then (`itemval[X]` and the value from wanting K) |
| **P3** | the knower knows X, has its inputs and values it, but making X is never the make option offered (another recipe wins the single make slot, or the make option is missing) |
| **P4** | making X is offered, but never chosen |
| **P5** | making X is chosen, but X is never completed (no make or fire event of X by that knower) |
| **P6** | X is made by a knower of K, but not kept: it is never held together with K's other made parts by one person (MP1's stage B/C/D boundary) |
| **P7** | X is made and kept, with all of K's made parts held at once by one knower (MP1's C, D or E) |

- **The looks are at the moment of deciding.** A wrapper on `mind.decide` reads the person's state before the choice,
  and on `thought.steer` reads the options offered. The make block's eligibility is recomputed by the code's own
  functions (`can_make`, `_wanted_parts`, `itemval`) without any random draw.
- **The primary outcome:** the share of followed kinds whose furthest stage is each of P0–P7, pooled over the 32
  worlds. Intervals are a world bootstrap (10,000 draws, NumPy seed 20261127).

**Reading (frozen):**
- Name **the stage where most kinds stop:** the largest share among P0–P6.
- **"Clear"** if its lower bound is above the next largest's upper bound; **"shared"** otherwise.

## Secondaries
1. **By depth (1, 2, 3+):** the stage shares.
2. **The whole's value.** For each kind, whether its inventor ever valued K itself above 0 in the 5 years
   (`itemval[K]`). Without this, K's parts get no value from K. The share of kinds where K was never valued, and the
   stage shares within that group.
3. **Make-slot competition.** In P3 kinds, how often the make option offered at a look where X was eligible was:
   - another part of K;
   - another new kind;
   - an old recipe.
4. **What the knower did instead,** in looks where making X was offered but not chosen (P4): the chosen action's shares.
5. **MP1's stage of each kind,** cross-tabulated with its PM1 stage, as a consistency check against MP1 (on v15).

## Zero checks (hard stops)
1. **Read-only:** world and random-stream hashes with and without the observer (20 and 60 years).
2. **Eligibility check:** in a 30-year world, at every look where the observer judges a recipe eligible for the make
   slot (known, inputs in hand, value above 0.05) and the person is old enough to make (grown, or 3+ under `child_make`),
   a make option must be among the options offered. And every make option offered must be eligible by the observer's
   test. **Any mismatch stops the study.**
3. **Event check:** every P5/P6/P7 "made" agrees with a make or fire event of X by a knower of K.
4. **Reload is exact.**
5. **All 32 worlds** are present under one fingerprint.

## A blind recompute
GPT, Gemini and DeepSeek recompute from a per-world count file built by a script written before data:
- the P0–P7 counts (with P0a and P0b);
- the depth split;
- the never-valued counts;
- the reading.

## Prior (the assistant)
- **P2 (never valued) is the largest stage, about 45%.** The inventor rarely comes to value a new kind, so its parts
  get no value from it.
- **P1 (no inputs) is next, about 25%,** then P0 (the part's recipe unknown), about 15%.
- **P3–P7 are small.**
- **The reading is likely "P2, shared",** about 50%.

## Sign-off (7 November 2026)
The assistant, under the creator's standing permissions (7 November: "you can keep going do not rely on me").

Council round 77:
- GPT 97%;
- Gemini 95%;
- DeepSeek about 90%;
- the assistant 85%.

Frozen as `PM1-frozen` before any code or data.
