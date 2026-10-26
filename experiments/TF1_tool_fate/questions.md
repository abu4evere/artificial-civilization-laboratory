# TF1 — Where do made things go? The tool lifecycle audit (frozen plan)

**Read-only on nature v7. No change to nature.** It follows LS1's frozen branch "Q4's fall is carried by s: tools are
not remade or replaced; the tool lifecycle is the leak", the code review `docs/tool_transfer_review_2026-10-27.md`, and
debate rounds 2–3 there (GPT and Gemini, Claude as council).

## Why

- **LS1 (final):** 0.98 of tools used were made by their holder, and 0.013 by someone else. Replacing a lost forage
  tool within a year fell from 0.59 to 0.07. Tools' food fell because almost nobody held one (s carries 0.97 of A4's
  fall).
- **The code (v7):** a living person cannot give a made thing to anyone (give = food only). Made things change hands
  only at death: to the partner, or to a child aged 12+ on the same tile, or from the body to those same people. A
  person carries at most 3 made things, and a fourth **deletes** the least valued. Tiles cannot hold made things.
- The debate agreed that **access to artefacts** may matter for learning a thing's worth (forager, chimpanzee, crow
  and capuchin evidence, to be checked). It also agreed that two candidate laws (handing things over; things that can
  lie in the world) should not be designed until we know where made things actually go.

## Setting

- Nature v7 (`code_v7`) unchanged, LP (80 founders, 80×80).
- 32 new seeds, 200 years: the same span as MK1, covering the start and LS1's decline period.
- Run on GitHub.

## Logged (a read-only weekly observer; no wrappers needed)

Every week the observer lists every made thing in the world: in each living person's hands, and with each body. It
follows each thing by identity from the week it first appears to its end.

For each thing it records:
- its kind, and its forage factor (and its best factor for any use);
- who made it, if seen made, and when;
- every holder, in order;
- its uses left each week;
- its **fate**, read from the change between two weeks.

| fate | what the observer sees |
|---|---|
| **worn out** | gone from the world, last seen with 1 or fewer uses left |
| **deleted at the carry limit** | gone, its holder alive, with uses left, and the holder gained a made thing that week |
| **used up in making** | gone, its holder alive, and the holder made, heated or combined something that week |
| **inherited** | moved from a person who died to a living person |
| **left with the body** | moved from a person who died to their body |
| **taken from a body** | moved from a body to a living person |
| **lost with the body** | gone when the body is gone |
| **lost at death** | gone in the week its holder died, not inherited and not with the body |
| **still held at the end** | — |
| **unknown** | any other disappearance |

**The ledger must balance in every world:** things that appeared = things that ended in a fate + things still in the
world at the end, exactly. "Unknown" fates must be under 1% of all ends, or the reading is marked unreliable.

## Questions (by LS1's bins up to 200 years; worlds alive at each bin's start; population beside every rate)

**Q1. How do forage tools end?** The share of forage tools (forage factor > 1) ending in each fate, by bin. Also
their life (weeks from first appearing to their end), and the uses they had left at their end.

**Q2. The carry limit.** Of things deleted at the carry limit:
- the share that were working forage tools;
- their uses left;
- the share that were better forage tools (a higher factor) than the worst thing kept;
- the share deleted while a child (under 16) in the holder's care, or any person, was within reach.

Also how much forage-tool life (in uses) the carry limit destroys, against wear.

**Q3. Things at death.** Of people who died holding a forage tool:
- the share whose tools were inherited, left with the body, then taken or lost with the body, or lost;
- **the forage-tool uses lost at death per 1,000 person-years**, by bin.

**Q4. Children and tools.**
- Child-weeks (ages 6–15) with no forage tool while their carer holds at least one, and while their carer holds two
  or more.
- The age at which a person first holds a forage tool, and how: made it, inherited it, or took it from a body.
- The share of adults (16+) holding a forage tool, by bin (to tie to LS1's s).

**Q5. Replacement, read by route.** After a person stops holding any forage tool: the share who hold one again within
52 weeks, by route (made, inherited, taken from a body), by bin.

## What would follow (stated now; not exclusive)

- **The carry limit destroys a large share of working forage tools** (Q2), or more tool life than wear: deletion is a
  leak of its own. Next: a candidate law for things that can lie in the world (persistence, decay, visibility, who may
  pick them up), as a separate study.
- **Many working tools are lost at death and children near tool-holding carers hold none** (Q3, Q4): material
  transmission is blocked. Next: the candidate law of handing over made things (the motive designed for durable
  things, not food's), with GPT's outcome: whether the pathway is used and what follows, by arms.
- **Tools mostly wear out, and are not remade** (Q1, Q5): the leak is the making choice (MK1), not the lifecycle.
- Whatever leads, the timing (the first bin) is reported.

## The assistant's prior (separate predictions)

1. Most forage tools end by wearing out (over half). Deletion at the carry limit is the second fate (10–30%).
2. A material share of deletions remove working forage tools (over a third), some better than the worst thing kept.
3. Most forage tools held at death are lost or left with the body, not inherited (under a third inherited), because
   the heir must be on the same tile.
4. Most child-weeks with a tool-holding carer have no forage tool (over 80%), and almost every first forage tool is
   self-made.
5. Replacement within a year falls by bin as in LS1, and almost all replacement is by making.

## Validity (hard stops)

- **Zero checks:**
  - the observer is read-only: state and random numbers identical with and without it, at 20 and at 60 years;
  - reload is exact;
  - the ledger balances in the zero runs.
- All 32 worlds present under one fingerprint (`code_v7`). The ledger balances in every world. Unknown fates under 1%
  (or marked).
- **An independent recompute** of Q1's fate shares, Q2's working-tool share of deletions, Q3's inherited share and
  Q4's child no-tool share, by GPT and Gemini (the creator's rule of 27 October), from the raw files, without the
  analysis script, before the findings are final.

## Sign-off (27 October 2026)

The creator: "approve the tool lifecycle audit, freeze it", on the audit drafted in
`docs/tool_transfer_review_2026-10-27.md` (debate rounds 2–3), written out here in full. Frozen as `TF1-frozen` before
any code or data. How the code reads choices the text leaves open goes in operational notes, appended before any data.

## Operational note 1 (27 October 2026, after freezing, before any data)

How the code (`run_tf1.py`) reads the text where it left a choice, found in a 15-year smoke world (seed 9957, not data):
1. **"Worn out" with more than one use lost in a week.** A thing can lose more than one use in a week (used in
   foraging and against the cold). Read literally, the frozen "last seen with 1 or fewer uses left" put such things
   under "unknown" (97 of 1,473 ends in the smoke world, 6.6%, all with 2 uses left and nothing made). The code reads
   "worn out" as: gone, its holder alive, and last seen with no more uses left than the most it has lost in any one
   week (at least 1). In the smoke world, unknown ends then fall to 1 in about 1,300.
2. **"Used up in making"** is a thing whose kind is a part of what its holder made, heated or combined that week (the
   recipe's parts, or a heating's part). In the smoke world, this is mostly cords and parts bound into larger composite
   things. It is a real fate, not a misreading.
3. **Origins:** "founding" = held at the start; "made" = first seen in its maker's hands in a week they made, played or
   heated that kind; otherwise "unseen".
4. **Seeds** 18301–18332 (new). **Carer** for children 12–15 is their last carer (carers end at 12), as in LS1.
5. **Replacement routes:** the route of the forage tool held again: made by the person, inherited, taken from a body,
   or unseen.

## Operational note 2 (27 October 2026, before any data)

The missing-abilities audit (`docs/missing_abilities_audit_2026-10-27.md`, item A4) found that a thing made when hands
are full can be deleted in the same week, and the weekly census never sees it: on a tie of worth, the newest thing is
the one deleted. In a 30-year smoke world, 15% of things made in play were gone by the end of their week, nearly all
new kinds with worth 0. TF1 therefore also counts, from each week's events, things made (in play, or deliberately)
that are not in their maker's hands at the week's end, and how many of them are kinds with worth 0. These are reported
beside Q2 and are not part of the ledger (they never entered the census). The zero checks are rerun with this code.
