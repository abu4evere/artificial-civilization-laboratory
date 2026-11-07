# PL1: where do the made parts of new kinds go? (frozen plan)

**A read-only audit of nature v15.** Council round 76 chose it unanimously (`docs/debate_round76_after_lw1_eg1_2026-11-07.md`;
GPT 97%, Gemini 95%, DeepSeek about 90%). **Nothing in nature changes, and PL1 decides no law.**

## Why
- **LW1:** learners got missing parts nearly 3 times as often, but no one but the inventor made a new kind (1 → 0).
  Knowing is not making.
- **RF1:** an inventor's pursuit of a kind fails; the gathered pieces are lost or used.
- **PLAY1 side look** (not data): 86 of 90 recipes people had invented themselves could not be made, because a made part
  was not in hand.
- **Evidence** (`docs/research/curation_and_parts_2026-11-07.md`): people keep tools and spare parts for later
  ("curation", a measure of planning depth).
- **In the code:** a person carries at most **3 made things** (`item_limit`). When a fourth comes, the least valued one
  is left on the ground (OP1). Anyone aged 12+ standing there later picks it up, the most valued first.

## Design
- **Code:** `code_v15` (fingerprint 3d46cd2c…), unchanged. One arm, no sham. LP (80 founders, 80 × 80).
- **Seeds 24901–24932** (32 new seeds, used by no study). 200 years. Kinds born in years 100–190 are followed for 5
  years each.

## Followed kinds
- **Which:** world-new kinds (`world.knowledge`, first made in years 100–190) whose recipe needs **at least one made
  part**, a part that is not a raw material. That is a part of a bind, or the part held in a fire when it is a made
  thing.
- **Depth:** the longest chain of made parts, read from the recipes in `world.knowledge`.

## Primary: how far each followed kind gets (the stage funnel)
For each followed kind K, the **furthest stage reached within 5 years after its invention week**, by anyone who knows
K's recipe at that week's end:

| stage | reached when |
|---|---|
| **A** | no knower ever holds any of K's made parts at a week's end |
| **B** | some knower holds one or more of them, but never all at once (counted with multiplicity) |
| **C** | one knower holds all of K's made parts at once, but cannot make K (a raw material or the binder is missing) |
| **D** | one knower can make K at a week's end (`can_make`), but K is never made again |
| **E** | K is made again, by anyone (a make or play event of K after its invention week) |

**Primary outcome:** the shares of A–E among the followed kinds, pooled over the 32 worlds. Intervals are a world
bootstrap (10,000 draws, NumPy seed 20261125).

**Reading (frozen):**
- Name **the stage where most kinds stop:** the largest share among A–D.
- **"Clear"** if its lower bound is above the upper bound of the next largest of A–D; **"shared"** otherwise.

## Secondary: the fate of every tracked part
**Which items are tracked:** every made thing created in a knower's hands, by a make, play or fire, whose kind is a
made part of a followed kind K. It is tracked from that week until K's window closes.

**Its first fate,** once it leaves the maker's hands, is one of:
- **used** in another make, play or fire: into K itself, or into another kind;
- **worn out** in use (`matter.wear`), or by the cold (in the body phase);
- **dropped at the carry limit** (the 3-thing limit). The pickup is then followed: picked up again by the one who
  dropped it, picked up by someone else, or still on the ground when the window closes;
- **handed** to another person;
- **at death:** passed to an heir, or lost;
- **still held** when K's window closes.

These are read by wrapping, never changing:
- `actions._craft`, `actions._hold_in_fire`, `matter.wear`, `actions._hand`, `actions.drop_on_ground`,
  `actions.ground_week`, `biology.body_phase`, `biology.die`;
- a weekly look at who holds each tracked item.

## Described
- **By depth** (1, 2, 3+): the A–E shares.
- **For the inventor alone:** the A–E shares.
- **The carry limit:** the share of knower-weeks at the 3-thing limit; and, among the drops of tracked parts, the share
  where the dropped part was the holder's least valued thing.
- **New kinds made by a non-inventor within 5 years** (beside LW1's 0 of 3,297).

## Zero checks (hard stops)
1. **Read-only:** world and random-stream hashes with and without the observer (20 and 60 years).
2. **Fate accounting** (a 30-year world, every week counted): every tracked item has exactly one first fate or "still
   held". The fate is recorded by a wrapped step, or, for an item gone during the body phase from a living holder, by
   the cold. **An item gone with no fate recorded stops the study.**
3. **Stage check:** every kind recorded at E has a make or play event of K after its invention week; every kind at C or
   D had a knower holding all its made parts at some week's end.
4. **Reload is exact.**
5. **All 32 worlds** are present under one fingerprint.

## A blind recompute
GPT, Gemini and DeepSeek recompute from a per-world count file built by a script written before data:
- the A–E counts;
- the fate counts;
- the reading.

## Prior (the assistant)
- **Most kinds stop at A or B:** their parts are not held again after the invention. The share at C is small (raw
  materials are easy to get), D is near 0, and E is under 5%.
- **The fate most often first is "dropped at the carry limit" or "used in another kind",** not "worn out".
- **Reading likely "B, shared" or "A, clear":** about 60%.

## Sign-off (7 November 2026)
The assistant, under the creator's standing permissions (7 November: "you can keep going do not rely on me").

Council round 76:
- GPT 97%;
- Gemini 95%;
- DeepSeek about 90%;
- the assistant 85%.

Frozen as `PL1-frozen` before any code or data.
