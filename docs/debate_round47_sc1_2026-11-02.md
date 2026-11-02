# Debate round 47: the SC1 draft (2 November 2026)

**What was asked:** review `docs/sc1_design_draft_2026-11-02.md`, attached as a file to fresh chats with the same
question (`research/local/round47_sc1.txt`).
- **Who:** GPT (chat `6ae85797`) and Gemini (chat `adf87c9139e469c3`).
- **Each answer is an opinion, not a sign-off.**

## GPT (opinion): 80%, "for a diagnostic baseline of observable capacities, not for establishing that Bob ... exists"
- **Weakest two:**
  - **5, planning:** `_material_wants` already favours needed materials. Match gathers on availability, inventory,
    person and circumstances. If the chain cannot be separated from the written pull, call it "organized production,
    not independent planning".
  - **10a, social cognition:** the share learned socially is social **transmission**, not cognition. Measure whether
    people pick better partners than opportunity-matched alternatives. Otherwise relabel it "social learning", or mark
    social cognition "not measurable".
- **Next most concerning:** 7, own goals, because surprise-driven attention is already favoured mechanically.
- **Its controls, measure by measure:**
  - 3: match age, situation and action;
  - 4: match the opportunities for an alternative means;
  - 6: match kind age, exposure and the chance to remake;
  - 9: match information age and distance;
  - 10b: require an **improvement** carried across holders, not mere survival or nesting.
- **12, identity:** "Fair as behavioral individuality; insufficient as identity". It suggests two nested models:
  - Model A: temperament, age, sex, situation **and year-t habit values**;
  - Model B: Model A plus the year-t action profile.

  Only gains from B over A, out of sample, count. Call the result "stable behavioral individuality".
- **Readings:**
  - report contrasts with 95% intervals as the result, with **no binary evidence / no-evidence rule**;
  - freeze one primary contrast, its sign and its control per capacity;
  - if labels are wanted: "positive contrast detected" or "inconclusive", never "absent".
- **Worlds:** at least 32; 64 is better for rare behaviours (invention, long chains, culture).

## Gemini (opinion): 88%, once 5, 7 and 12 are revised
- **Weakest two:**
  - **5, planning:** the same echo of `_material_wants`. Measure chains whose middle steps carry no pull of their own,
    or hold the pull constant.
  - **7, own goals:** it claims `thought.steer` gives own puzzles a direct bonus over told ones. Its fix: persistence
    against competing drives.
- **Its note on 10a:** the share learned socially is a ratio, not a controlled contrast.
- **12 re-measures habit persistence.** It suggests a cross-situation signature instead: does a person's own choice
  bias in situation A predict their bias in a situation B they have little experience of?
- **Readings:** contrasts are primary, and "evidence" needs both an interval above 0 **and** a minimum effect size (for
  example a relative contrast over 15%). With so many decisions, trivial echoes will clear 0.
- **Worlds:** keep 32.

## Checked against the code (the assistant, as council)
- **Gemini's mechanism for 7 is wrong, but its concern holds for another reason.**
  - **No bonus by source:** `thought.steer` adds no bonus for own puzzles over told ones. Both kinds pull with the same
    formula, size × (0.4 + 0.9 × curiosity) × (1 − 0.8 × hunger) (`thought.py` 148–149).
  - **The sizes differ by law:**
    - a told puzzle starts at 0.1 + 0.35 × curiosity × |claim|, so at most 0.45 (`information._wonder`);
    - an own surprise starts at the gap, at least 0.25 and up to 1 (`inquiry.surprised`).
  - **So the comparison must match puzzle size** (GPT's "match puzzle salience"); otherwise it re-measures this
    difference.
- **Both are right about 5.** `_material_wants` favours needed materials. A gather-then-make chain will partly echo it.
- **GPT is right about 10a.** The share learned socially measures the use of written channels. Partner choice is the
  closer test of social cognition. ACL people do learn whom to trust: `tested` raises the trust of people whose word
  held.
- **Both are right about 12.** The habit table must be among the predictors.
- **On readings, they differ:**
  - GPT: contrasts only, with "positive contrast detected" / "inconclusive" if labels are used;
  - Gemini: an effect-size gate on top of the interval.

  **The council's choice:** contrasts as the result. Labels only "positive contrast detected" (interval above 0 **and**
  a pre-set minimum effect) or "inconclusive", never "absent". The two are compatible.

## Outcome
Revise the draft before freezing:
- **5:** gathers matched on availability and inventory; chains labelled "organized production" unless they exceed the
  written pull.
- **7:** own against told puzzles, matched on puzzle size.
- **10a:** split. Social **learning** is described. Social **cognition** is partner choice against
  opportunity-matched alternatives, or "not measurable".
- **10b:** add improvement across holders: a kind whose made thing scores better on its use than the kind it came from.
- **12:** nested models with the habit table in Model A.
- **Readings:** as above.
- **Worlds:** 32, or 64 if the cloud budget allows.
