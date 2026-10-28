# PG0 — Does curiosity find useful things, and what does a new thing's zero start cost? The "why" audit (frozen plan)

**Read-only on nature v7. No change to nature.** Chosen in sleep mode (`docs/autonomous_decisions.md`, 27 October 2026).
Both GPT (85%) and Gemini (95%) proposed it as the first step towards people learning "why"
(`docs/gpt_view_why_learning_2026-10-27.md`, `docs/debate_after_op1_2026-10-27.md`).

## How it works in `code_v7` (read from the code)
- **Worth by kind.** People learn the worth of each kind of made thing from using it (`knowhow.judge_item`). A kind new
  to a person starts at worth 0, whatever its properties.
- **How much a thing helps is an exact formula of its properties** (`matter.factor`): for example, wood use =
  1 + 1.2 × edge × hardness. So a predictor given exact properties would do well almost by construction. That is GPT's
  warning about "hidden physics".
- **Puzzles.** A big gap between expected and felt worth becomes a puzzle (`inquiry`). While a puzzle about a made thing
  is a person's leading thought, play picks materials related to it 60% of the time (`actions._play`).

## Logged (read-only: wrappers on `actions._play` and `knowhow.judge_item` that read before calling the originals; weekly events)

**For every thing made in play:**
- whether the maker's leading thought was a puzzle about a made thing (puzzle-led play);
- the kind made: new to the world, new to the maker, or known;
- whether the kind is useful (LS1's definition: some use's factor > 1);
- whether the kind is made again later, by anyone, within the run.

**For every first use of a kind by a person** (the first `judge_item` call for that person and kind, from use):
- the felt value;
- the person's worth before (0 for a new kind);
- **an online prediction from the person's own past uses of other kinds only** (chronological, no future, no hidden
  factor):
  - a nearest-neighbour estimate in property space over their last uses for the same purpose;
  - the same with the property vectors shuffled among those past uses (the shuffled control);
  - the kind-only baseline, 0.

**For every kind a person holds:** how many uses until their worth is within 0.1 of the felt value.

## Questions (primary: world-born kinds; years 0–200; population beside every measure; world bootstrap, 10,000 replicates)

- **Q1 (curiosity).** Of things made in play:
  - the share made in puzzle-led play;
  - for puzzle-led against other play: the share that are new to the world, the share of those that are useful, and the
    share remade later.

  **Named:** whether puzzle-led play finds useful new kinds at a higher rate than other play. This is described, not
  causal (GPT).
- **Q2 (the zero start).**
  - At first use, the mean |felt − worth before| under the zero start.
  - The share of new useful kinds that are never used by their maker before being lost (deleted at the carry limit, or
    the maker dies).
  - Uses until worth is learned.
- **Q3 (information available — primary for the next step).**
  - At first uses of new kinds: the mean absolute error of the own-experience property prediction, against the shuffled
    control and against 0.
  - **Named:** whether the person's own past experience carries information about a new kind's usefulness: property
    prediction better than shuffled, with the paired bootstrap interval of the difference excluding 0.
  - This shows that information is **available**, not that today's mind can learn it (GPT).

## What would follow (stated now)
- **Q3 shows information available** (better than shuffled): a property-learning capacity (PG1) has something real to
  learn. Its design must still decide how people **perceive** properties: exactly, or with error. That is a question for
  the creator, because exact properties would be privileged knowledge (GPT).
- **Q3 shows no gain over shuffled:** past uses don't carry usable information about new kinds, and property-learning
  would not help. Described.
- **Q1:** if puzzle-led play finds useful kinds no more often than other play, today's curiosity is not directed in a
  way that helps. That is a target for the "test by changing one thing" step later.

## The assistant's prior
1. Puzzle-led play is under 20% of play, and finds useful new kinds at about the same rate as other play.
2. Most new useful kinds are lost before their maker ever uses them (the zero start plus the carry limit).
3. Property prediction beats shuffled clearly (the physics is a smooth formula of properties).

## Validity (hard stops)
- **Zero checks:**
  - the wrappers and observer are read-only: state and random numbers identical with and without them, at 20 and 60
    years;
  - reload is exact.
- **The replay:** the observer's reading of the puzzle-led condition equals the code's branch condition (a mismatch
  counter that must be 0).
- All 32 worlds are present under one fingerprint (`code_v7`).
- An independent recompute by GPT and Gemini (fresh chats, raw files) of Q1's rates and Q3's errors before the findings
  are final. A recompute is recorded only from numbers read from the reply.

## Setting
Nature v7, LP (80 founders, 80×80), 32 new seeds (19501–19532), 200 years, run on GitHub.

## Sign-off (27 October 2026)
The assistant, under the creator's sleep-mode autonomy (CLAUDE.md, Sleep mode). Both models proposed it (GPT 85%, Gemini
95%); the assistant's estimate is 70%. Logged in `docs/autonomous_decisions.md`. Frozen as `PG0-frozen` before any code
or data.

## Operational note 1 (27 October 2026, after freezing, before any data)

How the code (`run_pg0.py`, `analyse_pg0.py`) reads the text where it left a choice, found in a 20-year smoke world
(seed 9933, not data):
1. **"Puzzle-led play"** is read before `_play` runs. It means the person's leading thought is a puzzle about a made
   thing whose recipe they hold: the condition under which the code's 60% related-materials branch can apply. **The
   planned replay check** (that the observer's reading equals the code's branch) **is not built.** Knowing whether the
   branch was taken would need the world's random draw, and the observer must not consume it. So "puzzle-led" means
   eligible for that branch, and the mismatch counter has nothing to count. This is recorded here, before data.
2. **"New to the world"** means the kind was not in the world's record before that play. **"Useful"** follows LS1
   (some use's factor > 1). **"Remade later"** means any later `make` or `play` event of that kind.
3. **First use** is the first `_judge_use` call (a use of a held thing for a purpose) for that person and kind. The
   felt value is `factor − 1`, clipped to ±1, as `judge_item` reads it. Fixed-value judgements (floats, warmth) are not
   uses of properties and are left out.
4. **Predictors:**
   - the mean felt value of the 5 nearest past uses for the same purpose, in the 10-property space (scaled 0–1), from
     the person's last 200 uses of **other** kinds;
   - the shuffled control permutes the property vectors among those same past uses, with the observer's own generator;
   - the zero start predicts 0.

   First uses with fewer than 5 such past uses are counted, not predicted.
5. **"Lost before use"** is checked every 4 weeks: the maker died, or the kind is no longer in their hands.
6. **Seeds:** 19501–19532.
