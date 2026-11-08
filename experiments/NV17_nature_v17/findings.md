# Nature v17: the world's closed doors opened, then the world frozen (8 November 2026)

**Nature v17 = v16 + OD1's five doors** (`experiments/OD1_open_doors/findings.md`). Each door is a general law through
the 10 properties; none names a thing.
- **D1, similar parts:** an input not held may be replaced by a held thing within 10 in all 10 properties.
- **D2, containers carry:** the carry factor also multiplies the made-thing (3) and material (20) limits. At most it
  doubles them.
- **D3, made binders:** a held made thing with flex ≥ 50 can bind, and it is used up.
- **D4, made hammers:** a held made thing with hard ≥ 50 can strike, and it is not used up. Its own hardness sets the
  force and the sparks.
- **D5, layers add:** for warmth worn and for carrying, the best counts fully and each next one half, capped at 100.
  Every warm layer wears.

## How it was adopted (CLAUDE.md's safe path)
1. **The creator decided** the direction, the package and its bar (7 November 2026): "open the doors once, then freeze
   the world"; live if no harm.
2. **OD1 is final:**
   - no guard was raised;
   - every door was used;
   - the blind recompute by GPT and Gemini matched every point estimate and the reading.
3. **Council round 81** (`docs/debate_round81_adoption_v17_2026-11-08.md`): GPT 82%, Gemini 100%, DeepSeek about 93%;
   the assistant about 85%. No confirmatory run is needed: the creator decided this package and its bar.
4. **Code and checks:**
   - `code_v17` = `code_v16` + `../OD1_open_doors/patch_od1.py`, with the five doors' defaults set to 1
     (`make_v17.py o`; `v16_to_v17.diff`);
   - **zero checks All: PASS** (`zero.txt`):
     - v17 with the doors at 0 = v16 (4 checks);
     - v17 = OD1's arm o (2 seeds);
     - the live package's defaults = v17 (2 seeds);
     - the doors act;
     - reload is exact.
5. **Tests:** reference hashes regenerated (`acl` = `v17`); a v17 replay test added; **72 tests pass.**
6. **Records:** tag `nature-v17`; `docs/autonomous_decisions.md`; a Telegram message to the creator.

## Fingerprints
- live `acl/`: 676f5639f2370f53ae970c0dbc96e3f913e799d8497998f473d137a511d6924d
- `code_v17`: c1db69ab5616f50ce6eb4b6d810119fa4276fe94e77059741ee6382f3084253a

## To watch
These were not raised, but are noted for the review on 7 December:
- starvation, 1.15 [0.99, 1.34];
- child deaths, 1.17 [0.97, 1.44].

## Now
**The world is frozen as v17 until the review on 7 December 2026** (CLAUDE.md, "Direction"). New studies use
`experiments/NV17_nature_v17/code_v17`. v16 stays in `code_v16`, so the change can be undone. The next work is Bob's
brain, which starts together with the creator.
