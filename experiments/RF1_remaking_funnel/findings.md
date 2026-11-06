# RF1 findings: why do the inputs never come together? (read-only on v13)

**Status: final.** The blind recompute (`recompute_rf1.md`, 6 November 2026, 01:06) matches: GPT and Gemini 3.1 Pro ran code and agree in every number; DeepSeek, with no code tool, agrees in the counts, shares and reading (its intervals approximate, as it said).

Every number is from `results.md` (analyse_rf1.py, frozen before data, with amendment 1 made before data) on run
42164147385:
- 32 worlds of nature v13, seeds 23801–23832, 170 years; no world died out;
- 1,246 world-new kinds first made in play in years 130–165, each followed 5 years in its inventor's weeks;
- zero checks All: PASS (`zero_local.log`, accepted by the cloud with skip_zero=local; `code_v13` fingerprint f8b793bf…);
- in the runs too, the missing inputs were empty exactly when `can_make` was True (wrong 0 of 8,846 wanting weeks).

## The answer in two lines
1. **When a grown inventor wants their thing again, pursuit fails** (0.797). They start gathering, but the set never
   comes together: a gathered input is used up or lost, and the missing inputs are mostly made parts.
2. **But few inventors ever get that far.** 1,062 of 1,246 new kinds were invented by people not yet grown (children
   in play), and only the grown are offered "make again".

## The frozen question, answered
**Primary, the funnel** (69 kinds with at least one wanting week):

| stage | share | 95% | kinds |
|---|---|---|---|
| 1. cannot obtain | 0.029 | [0.000, 0.074] | 2 |
| 2. not offered | 0.174 | [0.092, 0.271] | 12 |
| 3. out-competed | 0.029 | [0.000, 0.080] | 2 |
| 4. started, never complete | **0.768** | [0.657, 0.857] | 53 |
| 5. complete | 0.000 | [0.000, 0.000] | 0 |

- Inability (1 + 2): 0.203 [0.122, 0.298].
- **Pursuit fails (3 + 4): 0.797 [0.702, 0.878].** The interval lies wholly above 0.5.
- **Reading: "pursuit fails".**
- **What follows (decided before data): the council on an intention law** (a held aim toward a state one's own
  experience valued).

## Described
- **Wanting weeks:** 8,846 in all; median 130 per kind that had any. The want lasts: these are long stretches, not a
  passing week.
- **What is missing:** made parts 10,044 times and raw materials 4,071 times, counted over the wanting weeks. No bone or
  hide, no wetness, no fire was ever the missing piece.
- **The carry limit:** in 35% of wanting weeks (3,063) the person was at the limit of 20 units of material.
- **Stage 4, the 53 kinds started but never complete:**
  - every one saw a completed gather of a missing input;
  - in 45 of them, an input once gathered was later lower before the set was complete (used in something else, given,
    set down, or lost).
- **Chosen instead**, in wanting weeks with a choice not toward a missing input (7,687): forage 0.401, gather (another
  material) 0.186, put 0.117, talk 0.110, give 0.086, join 0.085.
- **Amendment 1, the 1,177 kinds with no wanting week**, by the reason most often seen in the inventor's decision weeks:
  - **inventor not grown: 1,062**. New kinds are made in play (`actions.py`, the play action records the recipe as
    "made"). Childhood lasts to age 12, and the make option is offered only to the grown (`mind.decide`, `if grown`);
  - recipe forgotten: 109;
  - valued at or below 0.05: 6.

## Against the assistant's prior (questions.md)
| prior | result |
|---|---|
| "pursuit fails" about 45% | **yes**: 0.797 [0.702, 0.878] |
| "inability dominates" about 30% | no: 0.203 |
| the largest single stage "out-competed" (3) | **no**: "started, never complete" (4) is 0.768. Out-competed is 0.029 |

## What it means (the assistant's reading, for the council)
1. **Among grown inventors, the chain breaks in the middle of a sequence.**
   - The first step happens: they gather a missing input.
   - Then the gathered input does not wait for the rest: it is used for something else, set down or given away (45
     of 53).
   - The missing pieces are mostly made parts, which need their own making first: a sequence of at least two makes.
   - This is what a held aim would change, whether called an intention, GPT's "organising actions across time", or an
     option with interruption (Sutton, Precup & Singh 1999, `docs/research/options_held_aims_2026-11-05.md`): keep the
     gathered pieces for the aim, and pursue the parts in order.
2. **The larger gate is life stage.**
   - 85% of new kinds come from people not yet grown, through play. They are never offered "make again" while they are
     children, and most of the 5 years falls in childhood.
   - This is not a fault in the written rule: the code says "if grown" on purpose.
   - But it means that invention and remaking live in different people, or in different years of one life. Whether
     children should be able to make again deliberately, or whether what a child invented should carry into the
     grown person's making, is a question about the laws of growing up. It is for the council and the creator, with
     evidence on children's tool making (for example among hunter-gatherer children), not a tuning.
3. **Not the look-ahead, not value, not the inputs' availability.** RF1 closes the "inability" branch: only 20% stop
   for lack of inputs or of an option.
