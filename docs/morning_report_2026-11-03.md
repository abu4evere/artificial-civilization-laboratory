# Morning report, 3 November 2026 (written through the night; updated as things finish)

## In short
- **You gave me permission to edit the world's rules,** and I am using it carefully. Each change is still tested in
  a copy first, with a sham, checks and blind recomputes, and only proven changes go live.
- **DeepSeek is on the council** with GPT and Gemini. I briefed it on all of ACL first. It gave sharp, useful answers,
  and its main point changed the plan: measure autonomy properly now.
- **I checked the rules and found 5 small bugs.** The 3 that matter are being tested now (FF1; its folder is named FX1, an ID an older study already had):
  1. when choosing what to make, people unfairly prefer **old** recipes over new ones;
  2. when someone dies, an heir's extra tools get **deleted** instead of dropped on the ground;
  3. tools taken from a body push out the wrong item.
- **Three studies are running:**
  - **AF1:** can inventions be made again if parts work by what they do, and containers carry more?
  - **FX1:** the bug fixes. If nothing gets worse, they become **nature v12**.
  - **AM1:** which measures of autonomy really work. These will judge the bigger redesigns later.

## What I decided without you (all in `docs/autonomous_decisions.md`)
| decision | GPT | Gemini | DeepSeek | me |
|---|---|---|---|---|
| FX1: fix three bugs; adopt as v12 if no harm | 97% | 99% | about 95% | 85% |
| AM1: measure autonomy against weaker "control" worlds | 94% | 97% | about 92% | 70% |
| BN1: keep birth inheritance for now (the test was inconclusive) | | | | |
| After WP1: carrying room is tested in AF1; "goals across weeks" waits for AM1 | | | | |

## Something surprising
- **People die out when their choices get only slightly more random.** I found this while checking AM1's controls.
  - At choice randomness 0.4 instead of 0.2, a world empties within 11 years.
  - At 0.3, it shrinks to under half in 60 years.
- So ACL's people survive only by choosing almost the "best" thing every week, which is fragile. The finding comes from
  2 test worlds and is only described, but it bears on any redesign that gives people more freedom: freedom has to come
  with ways to survive mistakes.

## Found later in the night
- **Two more faults, held for a second fix round (FF2;** draft `docs/ff2_design_draft_2026-11-02.md`):
  - **F5:** a leaky basket wrongly saves walks to water.
  - **F6:** marks made with made tools are scored about 100 times too deep, a units mix-up.
- **Evidence I read for F6:**
  - real scratches on rock last about 50–200 years (rock wears about 5 mm per thousand years; Portenga & Bierman
    2011);
  - marks on wood last about 10 years (wood wears about 0.05 mm a year; Williams et al. 2001).
  - **ACL's marks wear about 3 times too fast.** A fix anchored to these numbers would let marks, and the knowledge
    in them, outlast their makers, by honest physics.

## Next in line (the review's order)
1. FX1's result, then v12 if it does no harm.
2. AF1's result. If positive, a confirmatory run on v12.
3. AM1's result: which autonomy measures are real.
4. **Next rule tests:**
   - made things as hammers and binders (draft: `docs/mt1_design_draft_2026-11-02.md`);
   - free choice of targets (draft: `docs/ft1_design_draft_2026-11-02.md`);
   - building and storing with made things;
   - the 12-recipe memory cap. The evidence says real groups know far more: 13–71 tool types in **one** domain
     (Kline & Boyd 2010).
5. Later: routines and goals across weeks (research note on the "options" framework).

## Results (filled in as they arrive)
- AF1: running.
- FX1: running.
- AM1: zero checks running.
