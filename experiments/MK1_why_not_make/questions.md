# MK1 — Why do people who can make, and weigh making, not choose it? (DRAFT, not frozen)

**Status: a draft written in sleep mode on 26 October 2026, for the creator's review. Not frozen, not signed off, no
code, no data.** It follows LS1's frozen next step and GPT's advice (`experiments/LS1_where_knowledge_goes/
gpt_view_ls1.md`): first a **read-only choice audit**, before any diagnostic world or change to nature.

## Why

LS1 (final, recomputed): from years 0–10 to 100–200, adults could make things more often (feasible Δ ln +0.77) and
weighed making more often (+0.33), but chose it far less often given weighed (−3.03). The choice carries the decline.
Foraging wins 0.68 of the time. Tools then vanish from people's hands (s carries 0.97 of A4's fall), and skill at 16
falls by cohort (0.45 → 0.04).

## How the choice works now (from `code_v7`, read-only)

- Every option gets a score, and one is picked by softmax (`choice_temperature` 0.2). The score is the option's
  instinct utility plus `learned_weight` (0.6) × the habit value for that action in the situation (32 situations).
- **Make:** the best recipe the person can make now. Its utility is `worth_weight` (2.0) × v × (0.6 + 0.4 × diligence)
  × (1 − 0.5 × hunger). v is the larger of:
  - the item's learned worth (`itemval`);
  - its worth as a part;
  - a belief;
  - half the surprise pull.
  Making is offered only if v > 0.05, and not to remake something already held at that worth.
- **Item worth** is learned from use: a forage tool's felt worth is its factor − 1, at rate 0.15 (0.3 when proved
  wrong).
- **A struck tool's quality depends on crafting skill:** quality ∝ (55 + 45 × skill)%, so a skill-0 maker gets 55% of
  a master's quality.
- **Forage:** (0.25 + 1.6 × food hunger) × the share of need the best nearby tile gives, + 0.08 × diligence.

A possible loop, **a hypothesis only**:
1. Low skill makes worse tools.
2. Worse tools are felt as worth less, so the item's worth is lower.
3. Lower worth means a lower score for making, so foraging wins.
4. Less practice keeps skill low.

The other explanation is **opportunity cost**: foraging pays more than making for everyone, skilled or not.

## Questions (read-only, v7, no change to nature)

**Q1. The score gap.** In every person-week where making was weighed, log:
- the full score of make and of the winner, the gap, and each part of make's score (v and where it came from;
  diligence; hunger; the habit term);
- the person's crafting skill, age, food, tools held, and the worth of each item they know.

Describe the gap by bin, as LS1 did.

**Q2. Skill and worth.** Is a maker's crafting skill associated with:
- (a) the quality (factor) of what they make;
- (b) the item worth they then learn;
- (c) the make score;
- (d) choosing to make?

Read within matched states (the same bin, hunger band, holding a forage tool or not, and food on the tile).

**Q3. Early against late, matched** (GPT's warning). Compare people in years 0–10 with people in years 100–200 in
matched states (hunger band, tool held, materials, food on the tile). How much of the fall in "chosen given weighed"
remains within matched states? How much is explained by:
- the item worth;
- skill;
- the habit term;
- the winner's score?

The split uses an exact decomposition of the score gap, written before data.

**Q4. Does making pay?** For each make, follow the maker for 52 weeks. Record the food got with the tool against the
food the maker would have got in the weeks spent making, read from the same person's forage returns in matched weeks.
This shows whether making is, in this world, a poor investment or a good one that is not chosen.

**Q5. What the trap would predict** (stated now). If the loop holds:
- within matched states, choosing to make rises with skill;
- the learned worth of the same recipe is lower for low-skill makers;
- late people's lower worth is mostly explained by lower skill.

If opportunity cost dominates:
- skilled makers also reject making when food is near;
- Q4 shows making pays less than foraging over a year.

## What would follow (stated now; for the creator)

- **The trap is supported:** propose (not run) GPT's isolated 2×2 diagnostic: making skill as now vs set higher, ×
  foraging return as now vs lower. The diagnostic is never a nature rule. Separately, evidence-led candidates such as
  tools passing to children (`docs/evidence_review_children_tools_2026-10-26.md`) for a separate decision.
- **Opportunity cost dominates:** the question becomes why forager tools pay in real life and not here (their
  returns, wear, or the delay before they pay). Then an evidence review of tool returns.
- **Making pays but is not chosen:** the learner fails to see a delayed benefit. Fly-brain step 3 (how worth is
  learned, over which timescale) becomes relevant.

## Setting (draft)

The LP arm as in LS1 (80 founders, 80×80), seeds new, 200 years, enough for the early and the decline period; 32
worlds. Validity as in LS1:
- an observer with identical state and random numbers with and without it;
- exact reload;
- one fingerprint;
- an independent recompute before the findings are final.

## The assistant's prior (to be restated before freezing)

1. The gap is mostly the item worth term: late makers value their tools less.
2. Skill and learned worth are associated within matched states.
3. Making a forage tool pays over a year (Q4) even for low-skill makers, so the choice, not the world, is short-sighted.

## Open for the creator

- Is a read-only audit the right next step, before the tool-lifecycle and transmission questions?
- 200 years and 32 worlds, or the full 1,000?
