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
