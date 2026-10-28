# LR1 — Does nature v8 stay healthy over 1,000 years? (frozen plan)

**Read-only on nature v8. No change to nature.** This is a description, not an adoption test: v8 stays adopted unless
the creator decides otherwise. Chosen in sleep mode (`docs/autonomous_decisions.md`, 28 October 2026). Both GPT (90%)
and Gemini (95%) chose it first (debate round 16, `docs/debate_after_v8_2026-10-28.md`). It is the long-run check both
asked for at adoption.

**The concern:** under v8, things on the ground never rot. They leave the ground only when someone picks them up. OP1
and PD1 covered 200 years. **Over 1,000 years, do things pile up, and does anything drift?**

## Arms (32 paired seeds, 19601–19632; LP: 80 founders, 80×80; **1,000 years**; run on GitHub; code `code_v8`)

| arm | setting |
|---|---|
| **v7** | `ground_items` 0, which equals `code_v7` exactly (NV8's zero checks) |
| **v8** | the live nature |
| **x** | sham: v8 with `sham_draw` 1, the yardstick for natural world-to-world variation |

## Logged (read-only: the law's `drop` and `pickup` events, and a yearly census)
- **Every year:**
  - the living population (0 once a world has died out);
  - adults;
  - made things held by adults;
  - things lying on the ground, and the most on any one tile;
  - drops and pick-ups (by others or by the dropper) that year.

## Questions (paired by seed; world bootstrap, 10,000 replicates; worlds that died out count as population 0)

- **Q1. Accumulation.**
  - Things on the ground per world at years 200, 400, 600, 800 and 1,000.
  - The slope over years 800–1,000.
  - The most on one tile.
  - Pick-ups as a share of drops, by century.
- **Q2. Demography.**
  - Mean population over years 800–1,000, v8 against v7 and the sham against v7 (extinct worlds count 0).
  - Extinctions per arm.
  - Population by century.
- **Q3. Tools in hand.** Made things held per adult, by century.

## Frozen descriptive flags (reported to the creator; they do not undo v8 by themselves)

- **Flag A (accumulation).** Raised if:
  - the mean things on the ground per world at year 1,000 exceed 5 × its value at year 200, **and**
  - the slope over years 800–1,000 has a 95% interval above 0 (still growing at the end).
- **Flag B (demography).** Raised if:
  - population over years 800–1,000, v8 ÷ v7, is below 0.90 with the interval's upper bound below 1 (counting extinct
    worlds as 0), **or**
  - v8 has 3 or more extinct worlds beyond v7.
- **The sham's numbers are shown beside each,** so chance can be told apart.

## What would follow
- **No flags:** v8 is stable over 1,000 years in these respects. Recorded.
- **Flag A:** things pile up without limit. A candidate follow-up, for the creator: whether things on the ground should
  wear like things in use. That would be a new frozen study, not decided here.
- **Flag B:** a long-run demographic effect not seen in 200 years. The creator decides whether to keep v8.

## The assistant's prior
1. Things on the ground level off (pick-ups balance drops). No flag A.
2. No flag B. Population v8 ÷ v7 is within the sham band.
3. Tools held per adult stay about twice v7's.

## Validity (hard stops)
- **Zero checks:**
  - the observer is read-only in arm v8 (state and random numbers identical with and without it, at 20 and 60 years);
  - `code_v8` off equals `code_v7` (rechecked);
  - reload is exact.
- **Conservation in v8:** drops = pick-ups + on the ground, every year (a mismatch counter that must be 0).
- All 96 worlds are present under one fingerprint.
- An independent recompute by GPT and Gemini (fresh chats, raw files) of the flag numbers before the findings are
  final.

## Sign-off (28 October 2026)
The assistant, under the creator's sleep-mode autonomy (CLAUDE.md, Sleep mode). Both models chose it (GPT 90%, Gemini
95%); the assistant's estimate is 85%. Logged in `docs/autonomous_decisions.md`. Frozen as `LR1-frozen` before any code
or data.

## Operational note 1 (28 October 2026, after freezing, before any data)

How the code (`run_lr1.py`, `analyse_lr1.py`) reads the text where it left a choice, found in 20-year smoke worlds
(seed 9931, all arms; not data):
1. **The arms** run on `code_v8`: c = v7 (`ground_items` 0), o = v8, x = the sham. In outputs and tables, "v7", "v8"
   and "sham" stand for c, o and x.
2. **The census** runs at each year's end. A world that dies out has no later rows. Every later year counts as 0
   living, 0 things on the ground, and so on.
3. **"Most on one tile"** is the largest count of things lying on a single tile in that year. The table shows its
   maximum over worlds.
4. **The slope over years 800–1,000** is a least-squares line through each world's yearly ground count, averaged over
   worlds; its interval is a world bootstrap.
5. **Population over years 800–1,000** is the pooled sum of yearly living counts (extinct = 0), v8 ÷ v7, with a paired
   world bootstrap.
6. **Seeds:** 19601–19632, the same in every arm.
