# Morning report, 5 November 2026 (written in the night; updated as PB2 finishes)

## In short
- **PB2 is running on the cloud** (run 41985849249, launched 02:14). It is the first test where the new brain actually
  **guides people's choices**, in a copy of the world. The live world is untouched.
  - Each adult remembers their own weeks and what they saw others do.
  - When choosing, they ask their memory: "last time I was in a week like this and did this, how did it feel?" That
    answer takes the place of the old habit table.
  - In one arm, people also pick a **goal** for a season: the thing they are learning fastest about (for example
    health or materials). A control arm picks goals at random.
  - The question: does a self-chosen goal help people **finish what they start** (gather materials, then make
    something)?
- **All safety checks passed** before launch:
  - with the brain off, the copy is exactly v13;
  - the read-only memory changes nothing;
  - saving and reloading a world with memories is exact;
  - the brain never touches the world's dice.
- **A problem caught before launch:** memories stayed stored after people died, so a 170-year world could have needed
  several GB. Memories now end with their owner. Nothing reads them after death, so behaviour is the same.

## What I decided without you (all in `docs/autonomous_decisions.md`)
| decision | GPT | Gemini | DeepSeek | me |
|---|---|---|---|---|
| PB2 frozen and run (the brain road, step 3; a test in a copy) | no estimate | 90% | about 72% | 55% |
| Cloud plan: 40 chunks of 4 worlds (one world per core), so no job comes near the 340-minute limit | | | | (engineering) |

## Research (notes in `docs/research/`)
- **People choose what to practise by learning progress** (Ten et al. 2021; 382 people). This is the idea behind the
  goal arm. A difference I noted before any data: people also use how hard a task is, and PB2 uses learning
  progress only.
- **People choose by recalling single past episodes**, not only running averages (Bornstein et al. 2017). This is the
  idea behind the memory steering. A difference I noted before any data: people weigh recent memories more, and PB2
  weighs memories by similarity only.

## Things to know
- **My mistake, corrected in the open:** four decisions (PB0, PB1, PB1b, PB2) were missing from the decisions log.
  They are added now, marked "recorded late".

## What is next
1. When PB2 finishes (about 5–7 hours after launch):
   - fetch the 160 worlds;
   - run the frozen analysis;
   - write the findings;
   - send the blind recompute to GPT, Gemini and DeepSeek.
2. Then the next brain step depends on the result:
   - if the goal helps, a confirmatory run on new seeds;
   - if it does not, find out why before changing anything.
