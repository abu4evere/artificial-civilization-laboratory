# Morning report, 5 November 2026 (written in the night)

## In short
- **PB2 is done and checked.** GPT, Gemini and DeepSeek each recomputed every number blind, and all three match.
  - **Memory works.** When people choose using their own memory of past weeks instead of the old habit table:
    - they finish about **6 times** more "gather materials, then make something" tasks;
    - they make about 4 times as much;
    - the worlds hold **28% more people**;
    - no world died out.
  - **The self-chosen goal added nothing.** A goal picked by "what am I learning fastest" did no better than no goal,
    or than a random goal.
  - **Re-making inventions is still almost absent.** Almost nobody makes a new kind of thing a second time.
  - **Nothing in the live world changed.** This was a test in a copy.
- **Why "memory works" needs one more test.** The old habit table looks one week ahead, and the memory does not.
  Maybe people do better simply because they stop looking ahead, and not because memory predicts better. All three
  AIs said to test this first (council round 62).
- **PB3 is frozen and being built:**
  - five arms: v13, v13 with the look-ahead switched off, memory, memory with a two-week view, and a sham;
  - 32 new worlds;
  - the safety checks are running now, then the cloud.
- **About re-making:**
  - In PB2, inventors almost never held the materials for their own new thing: 143 weeks for 1,192 new kinds.
  - When they did, they had usually forgotten the recipe already. A new recipe enters memory with value 0 and is the
    first forgotten once a person knows 12 (`acl/knowhow.py` lines 78–82).
  - **Correction:** I first wrote this up as a new clue. It is not: this rule was already found (rules review R1) and
    partly tested earlier (MO1: people kept recipes longer, but did not make more). Holding the materials looks like
    the bigger gap.

## What I decided without you (all in `docs/autonomous_decisions.md`)
| decision | GPT | Gemini | DeepSeek | me |
|---|---|---|---|---|
| PB2 frozen and run (the brain road, step 3; a test in a copy) | no estimate | 90% | about 72% | 55% |
| Cloud plan for PB2: 40 chunks of 4 worlds (jobs took 48–91 minutes, far inside the limit) | | | | (engineering) |
| PB3 frozen: memory steering as a candidate law; is it prediction or just "no look-ahead"? | 94% | 95% | about 80% | 70% |

## Research (notes in `docs/research/`)
- **People choose what to practise by learning progress** (Ten et al. 2021). This was the idea behind the goal arm;
  PB2 found it adds nothing in ACL as built.
- **People choose by recalling single past episodes** (Bornstein et al. 2017). This is the idea behind memory
  steering, which worked.
- **The brain balances habit and deliberate prediction by how reliable each has been** (Lee et al. 2014). This is a
  principled option if memory alone ever needs to be mixed with habit.

## Things to know
- **My mistake, corrected in the open:** four decisions (PB0, PB1, PB1b, PB2) were missing from the decisions log.
  They are added now, marked "recorded late".
- **A memory problem caught before launch:** memories stayed stored after people died, so a 170-year world could
  have needed several GB. Memories now end with their owner; behaviour is unchanged.

## What is next
1. PB3's safety checks, a short test, then the cloud (about 3–4 hours).
2. If memory steering beats "no look-ahead" and PB2's effect replicates, then memory becomes a **candidate law**. It
   still needs a confirmatory run on new seeds before anything goes live.
3. Then re-making: the council chooses between "remembering new recipes" (already partly tested) and "wanting to make a past success again" (gathering its materials on purpose).
