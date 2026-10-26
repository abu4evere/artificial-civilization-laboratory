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

## Draft revision 1 (26 October 2026, after GPT's review; still a draft, not frozen)

After `gpt_review_mk1.md`. These replace the matching parts above when the creator reviews the plan:
- **The offer gate is logged** (feasible but not offered, because v ≤ 0.05 or the thing is already held; offered;
  chosen; done; a useful tool produced). The primary reading is conditional on being offered. How often making is
  offered is reported separately.
- **Q3 uses the full softmax:**
  - U_m is making's full score after the thought's pull (`thought.steer`), with its habit term. U_other =
    0.2 · log Σ exp(U_j / 0.2) over every other offered option, after the pull.
  - Exactly, log-odds(make | offered) = (U_m − U_other) / 0.2.
  - The early-to-late change in the mean log-odds, over matched states, is split into making's worth term,
    hunger and diligence, the habit term, the thought's pull, and U_other. The split uses a Shapley allocation for the
    interactions, written before data. The actual probability of choosing to make is reported beside it.
- **The whole choice set is logged:** every option's score, and which option scored highest against which was drawn.
- **Q2 is read as histories, not causes:** per person, the sequence of making, the tool's quality, its use, and the
  worth updates that follow. Associations are described, not ranked as causes.
- **Q4 is descriptive:**
  - the tool's incremental yield at each actual forage act (the food owed to the tool, as in A4), summed over the
    tool's life;
  - its life and use;
  - cumulative benefit curves at 13, 26, 52 and 104 weeks, with censoring (the tool lost, or the person dead)
    reported;
  - the immediate cost of the making week, estimated from comparable observed foraging.
  Their difference is "an observational benefit-cost proxy, not a causal net return".
- **Three hypotheses, all of which may hold:**
  - a low-skill trap;
  - opportunity cost dominates;
  - delayed-benefit failure: making pays over the longer term, but learned worth and choice don't reflect it.
- **Size:** 32 worlds × 200 years, for a descriptive audit. Early-to-late changes are reported within surviving worlds
  and across all worlds, with extinctions recorded.

## Sign-off (27 October 2026)

The creator: "yea approve mk1, freeze and run on github", on this plan with draft revision 1 (which replaces the
matching parts above). Frozen as `MK1-frozen` before any code or data. How the code reads choices the text leaves open
goes in operational notes, appended before any data.

## Operational note 1 (27 October 2026, after freezing, before any data)

How the code (`run_mk1.py`, `analyse_mk1.py`) reads the frozen text where it left a choice:
1. **Setting:**
   - LP (80 founders, 80×80), seeds 18201–18232 (new), 200 years, nature v7 (`code_v7`) unchanged.
   - The primary readings are for adults (16+). Teens (12–15) are logged apart.
   - Bins are LS1's up to 200 years. "Early" is years 0–10 and "late" is years 100–200, LS1's decomposition periods.
2. **The offer gate:**
   - **Feasible:** as LS1, the person can make at least one recipe now, with a fire for heating.
   - **Offered:** "make" is among the decision's final options.
   - **Why feasible but not offered**, from a read-only replay of the decision's own make loop:
     - "low": every feasible recipe's worth v ≤ 0.05;
     - "held": every feasible recipe above 0.05 is a thing already held at that worth;
     - "both";
     - "tired": too little energy.
   - **Two internal checks must be exact in every world** (mismatch counters 0): the replayed offer equals the
     decision's, and the replayed worth term equals the score the decision gave.
3. **Making's score parts:**
   - worth term = 2.0 × v × D × H, with D = 0.6 + 0.4 × diligence and H = 1 − 0.5 × hunger;
   - habit = 0.6 × the habit value in the week's situation;
   - thought = the steer bonus;
   - U_other = 0.2 · log Σ exp(U_j / 0.2) over every other option entry after the pull, which is exactly what the
     softmax draws from;
   - log-odds = (U_m − U_other) / 0.2, and P = the softmax's own probability.
4. **Matched states:** hunger band (< 0.25, 0.25–0.5, 0.5–0.75, ≥ 0.75; hunger as the decision computes it) × holding
   a forage tool (factor > 1) × food on the person's tile in weeks of their need (< 0.5, 0.5–2, ≥ 2).
   - Materials are matched by construction, since every offered week has them.
   - Skill is not matched: it is one of the explanations.
5. **Q3:**
   - Late states are weighted to the early distribution of adult offered weeks, over states present in both.
   - The change in mean log-odds is split exactly into worth term, habit, thought and −U_other. The worth term is split
     by a three-factor Shapley allocation on cell means (v, D, H), and the cell-level covariance is reported as its own
     part.
   - The share of the fall in "chosen given offered" that remains within matched states = matched Δ ln ÷ raw Δ ln.
   - Primary: worlds alive at year 100 (bootstrap over worlds, 10,000 replicates, seed 20261027). All worlds:
     described.
   - The part carrying the largest share is named.
6. **Q2:**
   - Crafting-skill bands < 0.1, 0.1–0.2, 0.2–0.35, 0.35–0.5, ≥ 0.5.
   - Rates are directly standardised to all adults' offered weeks over bin × hunger × tool × food, over the states each
     band has; the reference share covered is shown.
   - Makings of forage tools: the tool's forage factor and the maker's learned worth for that kind at the making and 13
     and 52 weeks later. "Relative" worth is compared within the same kind.
   - Described, not causal.
7. **Q4:**
   - **Which tools:** every forage tool (factor > 1) made deliberately. The item followed is the first item of that kind
     in the maker's hands not already followed.
   - **Benefit:** food owed to the tool (got × (1 − 1/f)) at the maker's forage acts, cumulative to 13, 26, 52 and 104
     weeks. A tool stops being followed when its maker dies or no longer holds it, and keeps what it earned.
   - **Cost:** one forage act's food, the mean per adult forage act in the maker's own world, bin and state (with
     skill).
   - **Proxy:** benefit − cost, an observational proxy.
8. **Q5:** the three hypotheses are read from the tables as listed in the analysis. No thresholds are set; all may
   hold.
9. **Zero checks:**
   - LP seed 501 for 20 years and seed 601 for 60 years, with and without the observer: identical state and random
     numbers;
   - the replay mismatches 0;
   - the observer must see offered weeks and forage tools;
   - reload is exact.
