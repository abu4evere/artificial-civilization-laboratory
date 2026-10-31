# TR1 — What do tools really add? (frozen plan)

**Read-only on nature v10. No change to nature.** It follows IW1 (`experiments/IW1_item_worth/findings.md`): people
value made things correctly, but the things help modestly (felt help 0.163 per use), so making loses to food. Before
any law of "a world where knowing matters" (the creator's third goal), **measure how much tools really add**, and how
much they could add.

## Why "felt" is not "real" (code, live v10; checked 31 October 2026)
- **Felt help** for tool use is `matter.factor(item, use) − 1`, a fixed formula of the item's properties:
  - forage: 1 + 0.25 × edge + 0.3 × contain, at most 1.55;
  - hunt: 1 + 1.5 × edge × reach + 0.3 × hard × reach, at most 2.8.
- **Foraging** (`actions._forage`): the yield is min(`forage_rate` × effort, carry room), then limited by the tile's
  crop and plants. `forage_rate` = (base + skill) × stage × tool factor. **The tool adds food only when neither the
  carry room nor the plants bind,** but the person feels factor − 1 either way.
- **Hunting** (`actions.resolve_hunts`): kill chance = min(0.92, base × n^1.5 × (0.5 + skill) × mean tool factor).
  FX1: an ACL hunting week yields about 4% of a foraging week (Aché: about 110%).

## Design (32 worlds, seeds 21001–21032; LP: 80 founders, 80×80; 200 years; `code_v10`; one arm)
**Read-only wrappers** call the original unchanged. Before it acts, each wrapper computes the counterfactuals from the
same state, with pure functions:
- **`actions.HANDLERS["forage"]`:** food got with the tool in hand; without any tool; with the best foraging tool
  **this person knows** (the best existing item of a kind in their memory); and with the best foraging tool **in
  anyone's hands** in the world that week. The "with the tool in hand" figure must equal the food actually got
  (mismatch counter).
- **`actions.resolve_hunts`:** the expected kill chance of each hunt with the hunters' tools, with no tools, and with
  the best hunting tool in anyone's hands. Expected food = chance × the world's mean meat per kill.

## Questions (adults, years 100–200; world bootstrap, 10,000 replicates)
- **Q1** (primary): the **realized share of adults' foraged food added by tools** = (food got − food without the
  tool) ÷ food got.
- **Q2: where the tool's help goes** (GPT, Gemini). Of tool-aided forage weeks:
  - the share where the tool added **nothing** (the carry room or plants bound);
  - the share **partly** capped;
  - the share **fully** realized.
  The **efficiency ratio** (Gemini) = realized food added ÷ uncapped food added (rate × tool − rate).
- **Q3: felt against real** (GPT). Felt help (factor − 1) against the **normalized realized gain**, (food with ÷ food
  without) − 1, per use.
- **Q4: headroom**, as a share of the same activity's food (Gemini: hunting is judged against hunting):
  - (a) foraging with the best tool **the person knows** (access and knowledge);
  - (b) foraging with the best tool **in anyone's hands** (the world's best);
  - (c) hunting: expected kills and expected food with the hunters' tools, with none, and with the world's best, kept
    apart from food produced (GPT).
- **Q5:** Q1 and Q4 by season.
- **Q6:** for scale, the share of adults' food from foraging and from hunting.

## Frozen reading (Q1, Q4b)
- **"Knowing barely matters":** the realized share is < 0.05 and foraging headroom (b) is < 0.10.
- **"Knowing matters but is unused":** headroom (b) is ≥ 0.10 and the realized share is < half of headroom (b).
- **Otherwise "knowing matters and is used".**
- **Near the line** (GPT): if an interval crosses the threshold that decides the reading, the reading is reported
  with "(near the line)".

## What would follow
- **"Barely matters":** the creator's question is the laws of how tools help (the factor formulas, carry room,
  hunting returns). Gemini's suggestion is a later frozen nature-change test (doubled carry; hunting returns anchored to
  the Aché). **The creator decides.**
- **"Matters but unused":** look at access and choice. Who holds the best tools; why others do not make them.
- **"Matters and is used":** tools are not the bottleneck. Look elsewhere (memory, death; LS2's leak).

## Validity (hard stops)
- **Zero checks:**
  - the wrappers are read-only (state and random numbers identical with and without them, at 20 and 120 years);
  - reload is exact;
  - the replayed forage yield equals the food actually got (mismatch 0).
- All worlds are present under one fingerprint (`code_v10`).
- **A blind recompute by GPT and Gemini** of Q1, headroom (b) and the reading.

## The assistant's prior
1. **"Barely matters":** the carry room often binds, so the realized share is small (< 0.05).
2. **Felt help clearly exceeds the realized gain.**
3. **Hunting tools double the kill chance,** but add little food overall.

## Review (debate round 34, `docs/debate_round34_tr1_2026-10-31.md`)
- **GPT: yes, 85%.** Adopted:
  - zero-gain against partly capped;
  - the normalized realized gain;
  - headroom split into "the person knows" and "anyone's hands";
  - paired expected kills kept apart from food;
  - "near the line".
- **Gemini: yes, 85%.** Adopted: separate foraging and hunting headroom, each against its own activity, and the
  efficiency ratio. Its "TR1b" (doubled carry, Aché hunting) would change nature in a copy, so it is a candidate for
  the creator, not part of TR1.

## Sign-off (31 October 2026)
The assistant, under the creator's sleep-mode autonomy. It is read-only (the 40% rule). GPT estimates 85%, Gemini 85%
and the assistant 75%. Frozen as `TR1-frozen` before any code or data.

## Operational note 1 (31 October 2026, after freezing, before any data)

How the code (`run_tr1.py`, `analyse_tr1.py`) reads the text where it left a choice, found in a 110-year smoke world
(seed 9993; not data):
1. **Zero checks run at 20 and 120 years,** not 20 and 60, so the late-window counters are checked too (stricter).
2. **"Food got"** is the edible food the forage adds (food and seeds together), as `_forage` adds it. The replay equals
   the food actually got in every forage of the smoke world (counter `forage_replay`, required 0).
3. **"The best tool the person knows"** is the best forage factor among items that exist that week (in anyone's
   hands) of a kind in the person's recipe memory, or the tool in hand if better. **"In anyone's hands"** is the best
   forage factor among all items held by the living that week.
4. **"Tool-aided week"** means the person holds an item whose forage factor is above 1.
   - "Added nothing": food with = food without.
   - "Partly capped": some gain, less than the uncapped gain (rate × effort × (factor − 1)).
   - "Fully realized": the whole uncapped gain.
5. **Hunting counts hunts in years 100–200 with at least one adult hunter,** and only where prey is present (as the
   law does). Expected kills sum the law's kill chance under each tool assumption. Meat per kill is the mean over all
   kills in the run.
6. **Q5's seasons** are the world's season index (0–3), as the code numbers them.
7. **"Near the line"** is decided on the threshold that sets the reading. For "knowing matters but is unused", it is
   headroom (b)'s lower bound below 0.10, or the realized share's upper bound at or above half of headroom (b).

## Amendment 1 (31 October 2026, ~07:40; after the first run, before any outcome was read)

- **The first run** (GitHub 41191446977, 32 of 32 worlds) failed its own validity check. There were 3 forage-replay
  mismatches: 1 in seed 21003 and 2 in seed 21016, out of about 10 million forages. The analysis stopped at validity,
  and no outcome was read. Its validity-only output is kept as `results_run1_invalid.md`.
- **The cause:** seed 21003 was re-run locally, stopping at the first mismatch.
  - Person p00059 died within the forage action (week 129; `alive` false after the action). Their food and seeds went
    to body or heir, so the change in their own food was −2.18, against a replayed yield of 14.71.
  - The replay was right; **the check compared it with a dead person's emptied stores.**
  - Seed 21016 is being re-run to confirm both of its mismatches have the same cause. The result is appended below.
- **The fix:** a forage in which the forager dies within the action is counted apart (`died_in_forage`) and not
  checked against the food actually got. Every other forage keeps the exact check.
  - The measured sums are unchanged: they always used the replayed yields.
  - No threshold, measure or seed changes.
- **The whole study is re-run** with the amended runner, on the same seeds, after fresh local zero checks.
