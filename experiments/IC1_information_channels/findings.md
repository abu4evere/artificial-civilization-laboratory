# IC1 — How does information pass between people today? Findings (NOT FINAL: blind recompute pending)

Frozen as `IC1-frozen` (operational note 1); decided and signed off in sleep mode (`docs/autonomous_decisions.md`).
Read-only on nature v8 (`code_v8`). Run on GitHub Actions (run 40642737865, `skip_zero=local`). 32 worlds (seeds
19701–19732; LP, 80 founders, 80×80), 200 years. Every number comes from `analyse_ic1.py`, written before data; full
tables are in `results.md`.

**Validity:**
- zero checks pass;
- all 32 worlds are present under one fingerprint (`code_v8`);
- the wrappers' counts match the law's own events (mismatches 0).

**Population beside it:** no world died out; mean living population 127.4; 815,664 person-years (500,945 adult-years).

## The answer

**Telling someone where water is does no real work today. But the moments a water word could be learned are common.**

### Q1 — Water places told (primary)
- **Offered 1,195,317; accepted 240,709 (0.201).**
- **Never new, never a first option:** 0.000 [0.000, 0.000]. Every listener already knew water of their own.
- **Redundant:** 0.997 of accepted places were told while the listener could already see fresh water.
- **True:** 1.000 (fresh water within 1 tile of the told spot). **Held when checked:** 0.886 [0.855, 0.908] of 262,774.
- **Used: never.** Of 3,310,125 thirst decisions with a water target, 0.0000 had a told target. Of 159,153 accepted
  listener-places, 0.0000 later became that listener's thirst target, and 0.0000 of the 21,142 out of sight.
- The listener's mean thirst at the telling was 0.000. Distance to the told spot: in sight 210,183; 5–12 tiles 30,499;
  13 or more, 27.

**B1 (water telling does real work): not raised** (first option 0.000, needs ≥ 0.20; held 0.886, needs ≥ 0.50).

### Q2 — Shared attention at water
- **Almost every talk happens with both people seeing the same water:** 0.989 [0.987, 0.991] of 8,641,237 talks.
- **Such talks between two adults: 4.04 [3.78, 4.28] per adult-year.**
- **They repeat between the same people:** 0.870 [0.859, 0.881] of such moments fall to pairs with at least 5 of them
  (513,853 of 986,994 pairs). Median per pair: 5 moments, 4 water tiles shared, longest run 1 week.
- **Clutter:** in such moments both people see on average 10.8 fresh-water tiles and 4.7 animal groups.

**B2 (grounding moments exist): RAISED** (4.04 per adult-year, needs ≥ 1; 0.870 in repeated pairs, needs ≥ 0.25).

### Q3 — The channels (per 1,000 person-years)
| channel | received | held, of those tested |
|---|---|---|
| water places | 295.1 | 0.886 of 262,774 |
| game places | 1,577.9 | 0.896 of 727,046 |
| beliefs about stashing | 485.7 | 0.496 of 60,292 |
| recipes taught / read / copied (heated: 10.0, not a channel) | 125.0 / 35.6 / 0.1 | claims 0.618 of 5,163 |
| marks read | 89.0 | |
| stories told (0.183 accepted) | 15,634.1 | |
| word about others | 5,423.8 | |
| habit copies (in 10,594.1 talks) | 3,165.8 (mean size 0.092) | |

As GPT cautioned, counts are not amounts of information.

## Against the prior (the assistant's, frozen)
1. "Most water tellings are redundant; B1 not raised": **right** (0.997 redundant; first option 0.000).
2. "B2 raised": **right** (4.04 per adult-year; 0.870 in repeated pairs).
3. "Recipes and stories dwarf places in count; habit copying happens in nearly every talk": **half wrong.** Stories do
   (15,634), but recipes passed between people (about 161) are fewer than water places (295) and far fewer than game
   places (1,578). Habit copies come in about 0.30 of talks, not nearly all.

## What follows (from the frozen branches)
- **B1 not raised:** "water telling matters little today, and replacing it is low-risk." Removing the direct transfer
  of water places would take away almost nothing people use.
- **B2 raised:** "water is a workable first referent for a signal law."
- **Described, for the language design (not a frozen reading):** water is nearly always in view when people talk
  (0.989 of talks), and in such moments about 11 water tiles are in view. So a signal paired with "water here" would
  rarely be informative, and "which water" is ambiguous. A law whose signals must carry something sight does not would
  need a setting where the listener cannot already see it. This is the creator's design question.
- **Next, by the handoff:** the first language law is a nature change and goes first to GPT and Gemini (debate), then
  the creator.

## Independent recompute
Pending: GPT and Gemini, fresh chats, raw numbers only, the B1 and B2 numbers. Recorded only from their actual replies.

## Note (28 October 2026, before the recompute)
"Every listener already knew water of their own" in Q1 is slightly too strong: 11 of the 240,709 accepted water places
were new (and first options) for the listener. Shown as 0.000 at three decimals. Nothing else changes.
