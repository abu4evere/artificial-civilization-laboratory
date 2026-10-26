# TF1 — Where do made things go? Findings (recomputed independently by GPT and Gemini; final)

Frozen as `TF1-frozen` (operational notes 1–2); run on GitHub Actions (run 40365016321). 32 worlds on nature v7, LP
(80 founders, 80×80), seeds 18301–18332, 200 years. Every number comes from `analyse_tf1.py` (written before data); full
tables are in `results.md`.

**Validity:**
- the zero checks pass;
- all 32 worlds are present under one fingerprint (`code_v7`);
- the ledger balances in every world (every made thing that appeared ended in a fate or was still in the world);
- unknown fates: 489 of 256,250 ends (0.19%), under the 1% limit.

**Population:** 92 at the start, 113–119 later; 2 worlds ended (years 118, 182).

## The answer

**Forage tools mostly wear out or are built into bigger things, and then are not remade. The carry limit and death lose
few of them, but almost nothing passes between people.**

### Q1 — How forage tools end (pooled, 248,694 ends)

| fate | share [95%] |
|---|---|
| **worn out** | **0.576 [0.568, 0.584]** (0.60 in years 0–5, 0.28 in 5–10, then rising to 0.71 in 100–200) |
| **used up in making** (bound into a bigger thing) | **0.388 [0.381, 0.396]** (0.66 in years 5–10 → 0.28 in 100–200) |
| deleted at the carry limit | 0.034 [0.032, 0.036] (0.061 in years 10–20 → 0.013 in 100–200) |
| lost at death | 0.0003 |
| lost with the body | 0 |
| unknown | 0.001 |

Tools lived longer later (38 → 65 weeks) and ended with fewer uses left (12.5 → 10.3).

### Q2 — The carry limit
- 10,666 made things were deleted at the carry limit. **0.784 [0.757, 0.81] of them were working forage tools**, with
  33 uses left on average.
- 0.70 were better forage tools than the worst thing the holder kept. The limit drops what its holder values least,
  not what works least.
- A child under 16 was within reach in 0.74 of deletions.
- The carry limit destroyed more forage-tool uses (278,199) than were left at wearing out (166,795). It is a small
  share of tools but a large waste of working ones.
- **Gone the same week they were made** (operational note 2): 0.124 of the 234,328 things made in play, 0.988 of them
  new kinds with worth 0; and 0.041 of the 59,117 things made deliberately. Worth is learned only by use, so a new
  thing deleted at once can never prove itself.

### Q3 — At death
- Only 5,188 forage tools had a holder die. Of these:
  - **inherited: 0.044 [0.038, 0.050]**;
  - taken from the body: 0.227;
  - **still lying with the body at the end of the run: 0.712**. A body with things on it is kept, and only the dead
    person's partner or a child aged 12 or over, on that tile, may take them;
  - lost at death: 0.016.
- Forage-tool uses lost at death are tiny (0.2–13.6 per 1,000 person-years). **Death is not where tools leak,** because
  few people die holding one.

### Q4 — Children and tools
- Children (6–15) holding a forage tool: **0.95 in years 5–10 → 0.23 in 100–200**. Adults holding one:
  0.45 → 0.06.
- Child-weeks with no forage tool while their carer holds one: **0.42 [0.40, 0.44]** overall, **0.03 in years 5–10 →
  0.74 in years 100–200**.
- Every world-born person's first forage tool was self-made (17,911 people; made 1.000), at a median age of 3.5 years,
  in play.

### Q5 — Replacement within a year
- Replacement fell from 0.56 (years 0–5) to 0.14 (years 100–200), as in LS1.
- **0.99 of replacements were made by the person.** Inherited or taken from a body, under 0.01.

## Against the prior (Claude's, frozen)
1. "Most forage tools wear out (over half)": **right** (0.58). "Deletion at the carry limit is the second fate
   (10–30%)": **wrong.** Being built into bigger things is second (0.39); deletion is 0.03.
2. "Over a third of deletions remove working forage tools, some better than the worst kept": **right** (0.78; 0.70).
3. "Under a third of tools at death are inherited": **right** (0.04). But few tools meet a death at all.
4. "Over 80% of child-weeks with a tool-holding carer have no tool": **wrong overall** (0.42). It is right late (0.74)
   and far wrong early (0.03): early children make their own in play. "Almost every first tool is self-made":
   **right** (1.000).
5. "Replacement falls by bin, almost all by making": **right.**

## What follows (frozen branches)
- **"Tools mostly wear out, and are not remade"** (Q1 0.58 worn out; Q5 replacement 0.56 → 0.14, 0.99 by making):
  **the leak is the making choice (MK1), not the lifecycle.** MK1 found that choice is lost to the other options'
  rising scores.
- **"The carry limit destroys a large share of working forage tools"**: **partly.** It is a small share of tool ends
  (0.03), but it wastes more working uses than wear leaves, and it deletes new things before they are ever used
  (0.12 of things made in play). A candidate law for things that can lie in the world remains a separate, lower-priority
  question.
- **"Many working tools are lost at death and children near tool-holding carers hold none"**: **half.** Few tools are
  lost at death, but late in the run most children near a tool-holding carer hold none (0.74), and nothing is ever
  handed over (living transfer is impossible). Material transmission is blocked by construction. Whether opening it
  would matter is the giving candidate's question.
- **Timing:** children's and adults' tool-holding falls from years 20–50, together with the making choice (MK1) and
  replacement.

## Independent recompute (27 October 2026)
GPT and Gemini, each in a fresh chat, from the raw rows only, without the analysis script (`recompute_tf1.md`). **All
three agree on every key number:**
- worn out 0.5764;
- forage tools among deletions 0.7842;
- inherited 0.0439 of 5,188;
- children with no tool beside a tool-holding carer 0.4208 (0.0312 → 0.7405).

Gemini's first intervals were row-level; rerun by whole worlds, they match. **Final.**
