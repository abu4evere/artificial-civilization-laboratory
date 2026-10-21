# TU1 — How is tool use learned, and does it spread? (SIGNED OFF 21 October 2026; frozen as `TU1-frozen` before any code or data)

**Why.** FX2 and FX3 (`../FX3_gentler_embedded/findings.md`, `FX3-done`): when a hard thing helps open embedded food,
people carry and use hard things more, but survival does not change. The decision of 21 October 2026
(`../../docs/decision_2026-10-21_LM1_FX.md`): embedded food is **not** adopted into nature; instead, a read-only study
of how tool use is learned and spreads. **Read-only: nothing in ACL changes.** Tool use, tool possession and survival
are kept as separate outcomes (GPT's warning).

## Questions

1. When a person first uses a hard thing on embedded food, how did they come to it: on their own, after being told it
   works, or after someone gave or left them the thing?
2. Does tool use spread: does a person's use follow others' use near them (in time and place), within and across
   families?
3. Does it last: once a person uses a tool on embedded food, how long do they keep doing so?

## How a person comes to value a tool today (read from `code_fx2`, 21 October 2026)

A person's sense of an item's worth (`itemval`) changes by **using it** (`knowhow.judge_item`: when a hard thing opens
embedded food, its value rises with how much it helped), by **being told** (`information`: a teacher's opinion of an
item can be passed on in talk, and taken on by the learner), and, for hunting, by **watching** (`knowhow.watch`).
Items themselves can be **made**, **given**, **taken** or **inherited**.

## Design (the assistant's recommendation; decisions marked)

- **Worlds (Decision 1):** FX3's tool arms, **S25 and B50**, seeds 7301–7556, **replayed exactly** (each replay's final
  state hash must equal FX3's saved one), with a read-only observer; S25-0 and B50-0 are not needed (no tool route).
  512 worlds, on GitHub's machines.
- **Instrument:** a read-only observer (no logging copy needed if the week's events and each person's `itemval` and
  `heard` are enough; if not, a logging copy shown to change nothing, as PF1 and PF2).
- **Per person:** the week of first tool use on embedded food; what they knew of that item before (own use of it, a
  heard opinion, nothing); how they got the item (made, given, taken, inherited); whether anyone within sight used a
  tool on embedded food in the 13 weeks before; whether that person was kin.
- **Per world:** the share of adults who ever use a tool on embedded food, by decade; the median time from a band's
  first user to its second; how long users keep using.

## The frozen reading (proposed)

- **Q1:** the share of first uses by route (own discovery / after being told / after receiving the item / other), per
  arm. **The main route** is the largest; it counts only if the same in both arms. Described, no test.
- **Q2, Q3:** described (no test). It shows how tool use is learned in these worlds; it does not show that tools cause
  survival differences.

## The assistant's prior (to be frozen at sign-off; held loosely)

Most first uses are **own discovery**: a person happens to hold a hard thing while foraging embedded food and feels it
help. Being told is rare (opinions of items are passed on only in some talks). Use spreads mostly within families,
because people forage near kin. Use, once started, lasts while the person keeps the item.

## Decisions for the creator

1. Worlds: **FX3's S25 and B50, replayed exactly, 512 worlds on GitHub** (recommended), or one arm only (256).
2. The prior, frozen as written.
3. Order: **after LX1** (recommended; both can run on GitHub at once if you prefer).

## Sign-off (21 October 2026)

The creator: "approve all recommendations, freeze both". All recommended options and the prior stand as written.

## Operational note (21 October 2026, while building, before any data; rule 19)

Reading the code (`code_fx2`: `actions._keep`, `biology.py` inheritance) showed that items are never handed from one
person to another except by **inheritance** at death; founders start with none. So the route "after receiving the item"
means **inherited**; "own discovery" covers items a person made or that hardened in their fire. The observer tracks each
item kind's origin from the week it first appears in a person's hands. Nothing else changes.
