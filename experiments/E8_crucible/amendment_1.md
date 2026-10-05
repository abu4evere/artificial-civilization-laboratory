# E8 — Amendment 1 (before any E8 code or run)

**Written:** 2026-10-05. `E8_crucible.md` and `predictions.md` are left exactly as frozen. Where this amendment
disagrees with them, this amendment holds. No E8 code existed and no E8 world had run when it was written.

**Why:** a review of the frozen design against the code found one impossible criterion, one confounded arm, one
self-contradiction, two inaccurate descriptions, and an over-optimistic compute estimate. It also sets the
order of execution and the success measures for Arm 1, the first arm to run.

## A1. An impossible criterion is removed

`predictions.md` asks for "LFA ≥ 80 in ≥ 2 seeds" in 120-year runs. A novelty counts as lasting only if it is
done again 50 or more years after it first appears, so in a 120-year run nothing first appearing after year 70
can ever qualify. The criterion could never be met.

**Fix:** no LFA criterion is applied to 120-year runs. Any arm that passes its 120-year test is run again for
300 years, where LFA is defined, with its own frozen novelty predictions written before that run.

## A2. Arm 2 is split, because it changed two things at once

Arm 2 added both (a) watching for every act of making, not only raft landings and shared hunts, and (b) faster
skill gain when practising a recipe shown by a more skilled person. If Arm 2 worked, its cause could not be
known.

**Fix:** Arm 2a = (a) only. Arm 2b = (b) only. Arm 2 = both, kept to measure their interaction.

The design called the narrow watching "a bug". It is a design decision in the current code (see the book's
Known Compromises). Widening it is a change to how people learn, not a correction.

## A3. Arm 4 contradicted itself; a pilot comes first

The design promises identical maps and founder genetics for every arm, and also a 4× larger map for Arm 4. Both
cannot hold. Separately, E5 showed populations settling at 30–90 people whatever happens early on, so 80
founders on today's land may simply fall back, and Arm 4 would not test a larger population at all.

**Fix:** before Arm 4 is designed further, a 30-year feasibility pilot (no predictions, reported as a pilot):
seeds 301–304, (i) today's map with 4 bands of 20, and (ii) a map scaled to keep land per person constant.
Recorded: population every 5 years. Arm 4 proceeds only with a setup whose population stays at least twice the
control's at year 30, and its predictions are re-frozen then. The claim of identical topography across arms is
withdrawn for Arm 4.

## A4. Two descriptions corrected

- "Tools last 20–50 weeks": a made thing has 15 + (30·hard + 25·warm + 20·contain)/100 uses (+10 if
  fire-hardened), roughly 15–45, and loses one per use. Durability is counted in uses, not weeks.
- "`mind.py` strictly forbids crafting an item if one is already held": the rule skips remaking a recipe only
  when the person holds one with more than 5 uses left **and** nothing else pulls them to it (an inquiry, a
  belief about a place and season, or the recipe being a part of something wanted).

## A5. Compute estimate corrected

Measured on this laptop: a 120-year run of a 20-founder world takes about 4 minutes on one thread. Worlds with
80 founders will be several times slower. With 8 threads, the full E8 is about 1–2 hours, not 42 minutes.

## A6. Order of execution

1. This amendment and the Arm 1 rule (A8) are frozen.
2. **Arm 0 and Arm 1 only**, seeds 301–304, 120 years. Plus the Arm 4 pilot (A3).
3. Arms 2–6 are run only if Arm 1's result says they are still needed, and are re-predicted before running.

## A7. What counts as success for Arm 1

More making raises skill by construction (skill grows only by making), so neither more making nor higher skill
is a success. Arm 1 is judged on what more practice does to everything else, Arm 1 against Arm 0:

- **Skill after the founders die:** best and mean crafting skill among people born after year 30, at years 60,
  90 and 120.
- **Recipes:** unique recipes held by the living, and the share that are composite, at years 60, 90 and 120.
- **Traditions:** techniques held by 3+ people in every 10-year sample from year 30 on.
- **Survival:** worlds alive at 120; population at 60, 90, 120.
- **The cost:** food per person and starvation deaths. More making must not hide a famine.
- **Making itself:** deliberate makes per person-decade, reported as a manipulation check only. If making does not
  rise, Arm 1 did not test its hypothesis, and its other results are not interpreted.

## A8. The rule that replaces the holding check (TO BE CHOSEN, then frozen here)

Today: a held recipe with more than 5 uses left is skipped unless something extra pulls the person to it.
Three candidates follow. Each changes only that check in `mind.py`, except where stated. The creator chooses
one before any code is written; the choice and the reason are recorded below.

**R1 — Early renewal.** A thing counts as held only while it keeps more than half of the uses it was made with.
- Makes people replace a tool before it is worn out, never make a second while the first is in good shape.
- Expected effect: making rises modestly (perhaps 1.5–2×), no duplicates, little extra time or material spent.
- Risk: the dose may be too small to answer the question. A null result would be ambiguous.

**R2 — Practise what has proved its worth.** The holding check is removed for any recipe the person values
above zero, but the pull to remake a thing already held is halved. The 3-thing carrying limit still drops the
least valued thing.
- People practise their most valued recipes even while holding one, at a real cost in weeks and materials.
- Expected effect: the largest rise in making, concentrated in proven tools (carriers, clubs, rafts); duplicates
  are discarded. The strongest test of "is practice what is missing?".
- Risk: time spent making is time not foraging; survival and food must be watched (A7).

**R3 — Make for kin.** A person may remake a thing they hold when a partner or child (6 years or older) on the
same tile has none, and then gives it to them. Requires a new act, giving a made thing, which does not exist
today (only food can be given; things pass only by inheritance at death).
- Closest to real provisioning; puts made things in children's hands early.
- Expected effect: making scales with family size; children hold tools sooner, which may lower their own play,
  and so their own practice.
- Risk: two changes at once (a new act and a new reason to make). Larger change than R1 or R2.

**Chosen: R2**, by the creator on 2026-10-05, because Arm 1 must answer one upstream question as clearly as
possible ("is practice what is missing?"): R1's effect may be too small to read, and R3 changes two things at
once.

**R2 exactly (the only change in Arm 1's code, in `mind.py`, the "make again" loop):**

```
held = _holding(p, sig)
if held and v == p.itemval.get(sig, 0.0):      # today this case is skipped
    if p.itemval.get(sig, 0.0) <= 0:            # practise only what has proved its worth
        continue
    v = 0.5 * v                                 # at half the pull
if v <= best_u or not can_make(p, recipe):
    continue
```

Every case today's rule allows is untouched, at full strength. Arm 1 only adds remaking a held, valued thing
at half its pull. The other two uses of `_holding` (parts and materials wanted for recipes) are unchanged.

## A9. Arm 0 and Arm 1: frozen predictions

Seeds 301–304, 120 years, Arm 0 = the E7 code, Arm 1 = the E7 code with R2. Measured every 10 years by a
read-only probe. "Later-born" = born after year 30, when nearly every founder is dead or old.

1. **Manipulation check.** Deliberate makes per person-decade, years 50–120, are at least 3× Arm 0's in all 4
   seeds. If this fails, Arm 1 did not test its hypothesis and predictions 2–6 are not interpreted.
2. **Skill outlives the founders.** Mean crafting skill of later-born adults (16+) at year 120 is at least 2×
   Arm 0's in at least 3 of 4 seeds.
3. **More is kept.** Unique recipes held by the living at year 120 are at least 1.3× Arm 0's in at least 3 of 4
   seeds.
4. **Composites are not crowded out.** The share of composite recipes among those held at year 120 is no lower
   than Arm 0's (within 2 percentage points) in at least 3 of 4 seeds.
5. **Traditions.** Techniques held by 3+ people in every 10-year sample from year 30 to 120 number at least as
   many as in Arm 0 in at least 3 of 4 seeds.
6. **Practice has a price, but not a famine.** All 4 Arm 1 worlds are alive at year 120; population at year 120
   is at least 80% of Arm 0's in at least 3 of 4 seeds; starvation deaths over 120 years are at most 1.3× Arm 0's
   pooled.

**What the result will decide:**
- 1 fails: making was not freed by this rule; autopsy why people do not make before anything else.
- 1 holds, 2–5 mostly fail: practice alone does not keep a culture; apprenticeship and population (Arms 2, 4)
  become the next tests.
- 1–5 mostly hold, 6 holds: practice scarcity was a real cause; the next step is a 300-year run of Arm 1 with
  novelty predictions (A1).
- 1–5 hold, 6 fails: practice works but the economy cannot pay for it; surplus becomes the question.

**Validity (kill criteria):** the probe changes nothing (state hash with and without it, 20 years, both codes);
Arm 0 reproduces the saved E7 runs' populations; code fingerprints unchanged during the runs; no crashes.
