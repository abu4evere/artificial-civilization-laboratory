# IC1 — How does information pass between people today, and where could words begin? (frozen plan)

**Read-only on nature v8. No change to nature.** It is the language groundwork audit chosen in debate round 16
(`docs/debate_after_v8_2026-10-28.md`, where it was called "TC0"). It is renamed IC1 because TC1 is taken (talk copying).
Chosen in sleep mode (`docs/autonomous_decisions.md`, 28 October 2026).

**Why.** Today people pass on some things by **direct transfer**: a told water place arrives as exact coordinates
(`information.tell_place`, a 10% chance of a one-tile shift). The creator's rule (27 October): "we cannot give them map for
sure it means cheating." Both models proposed that the first language law should replace the direct transfer of water
places with meaningless signals, learned only when both people perceive the same water (`docs/gpt_view_language_2026-10-27.md`).
**Before any such law,** this audit measures:
1. what each channel carries;
2. how much of it is used and how much is true;
3. whether the moments a signal could be grounded (two people talking while both see the same water) happen often enough.

## Design (32 worlds, seeds 19701–19732; LP: 80 founders, 80×80; 200 years; `code_v8` = live nature; one arm)

**The observer only reads:**
- events (`learn`, `verified`, `refuted`, `vouched`, `told`, `read`, `talk`);
- four read-only wrappers, which call the original unchanged:
  - `information.hear_place`: each place offered in talk, with the state at that moment;
  - the talk action (`actions.HANDLERS["talk"]`): the start of each talk, with both people's positions;
  - `actions._imitate`: each habit copy, with its size;
  - `mind._nearest_spring`: each thirst decision that has a water target, and whether that target was seen or told.

## Questions

- **Q1. Water places told** (primary; every water place offered in talk).
  - Accepted out of offered.
  - **New:** the listener knew no water of their own (`springs` empty) when accepted.
  - **First option** (GPT): new, and the listener had no other told water either, so it is their only water target.
  - **Distance** from the listener and from the speaker to the told spot at the telling (within 4 tiles = in sight;
    5–12; more than 12).
  - **The listener's thirst** at the telling (Gemini).
  - **Redundant:** the listener could see fresh water within 4 tiles (perception) at that moment.
  - **True:** fresh water within 1 tile of the told spot.
  - **Checked later,** and held or refuted (the law's own `verified` / `refuted`).
  - **Used:** the share of thirst decisions with a water target whose target came from a told place rather than own sight.
  - **Used per telling** (GPT): the share of accepted water places that later become a thirst target of the
    listener, overall and for spots out of the listener's sight at the telling. This shows whether talk carries
    something sight cannot.
- **Q2. Shared attention** (all talks).
  - The share of talks in which **both** people can see the **same** fresh-water tile (within 4 tiles of each).
  - Such talks per adult-year.
  - The same for water tellings: the share of water places told while both see the told spot's water.
  - The same per **pair**: how many distinct pairs share such moments, and how often each pair does (a word needs
    repetition between the same people).
  - **Per pair** (GPT, Gemini): how many different water places it shares (the source is the shared fresh tile
    nearest the first speaker), and its longest run of consecutive weeks with such moments.
  - **Clutter** (Gemini): in such moments, how many fresh tiles both see and how many animal groups both see.
- **Q3. The channels** (per 1,000 person-years; mean living population beside it).
  - places (water, game);
  - beliefs (stashing);
  - recipes (shown/told, copied by watching, read from marks);
  - stories;
  - word about others (reputation);
  - habit copying (copies and mean size).
  - For each channel: received, and where the law tests it, the share **held** against **refuted**, with the number
    tested.
  - **As GPT cautioned,** a habit copy blends a whole table and is not comparable in size to one place told. Counts
    are not amounts of information.

## Frozen descriptive branches (for the creator's language decision; none changes nature)

- **B1, water telling does real work:** raised if ≥ 20% of accepted water places are the listener's **first option**
  and ≥ 50% of checked water places **hold**.
  - If raised: removing direct transfer would cost something real, so a language-law study must carry a thirst and
    survival flag.
  - If not raised: water telling matters little today, and replacing it is low-risk.
- **B2, grounding moments exist:** raised if talks where both see the same water number ≥ 1 per adult-year **and**
  ≥ 25% of such moments fall to pairs who share at least 5 of them.
  - If raised: water is a workable first referent for a signal law.
  - If not raised: the first law needs another referent or setting, which is the creator's design question.

## The assistant's prior
1. Most water tellings are redundant (the listener already sees water). B1 is not raised.
2. B2 is raised: people gather at water, and talks there are common.
3. Recipes and stories dwarf places in count. Habit copying happens in nearly every talk.

## Validity (hard stops)
- **Zero checks:**
  - the observer and wrappers are read-only (state and random numbers identical with and without them, at 20 and 60
    years);
  - reload is exact;
  - the wrappers' counts match the law's own events: accepted water places = `learn` events with a `w:` spot; habit
    copies seen by the wrapper = copies replayed.
- All 32 worlds are present under one fingerprint (`code_v8`).
- An independent recompute by GPT and Gemini (fresh chats, raw files) of the B1 and B2 numbers before the findings are
  final.

## Review (debate round 17, `docs/debate_after_lr1_launch_2026-10-28.md`)
- **GPT:** yes, 90%. Its additions are adopted: first option, distance, used per telling, the number checked, and
  repeated pairs with different sources.
- **Gemini:** yes, 95%. Its additions are adopted: thirst at the telling, runs of weeks, and clutter.
- **Corrected:** Gemini calls the later study "the Law 33 water-signaling study". No such law or study exists.

## Sign-off (28 October 2026)
The assistant, under the creator's sleep-mode autonomy (CLAUDE.md, Sleep mode). GPT estimates 90% and Gemini 95%; the
assistant's estimate is 80%. Logged in `docs/autonomous_decisions.md`.

**Note, in the open:** a first draft of the runner was written while this plan was under review. Nothing was run. It is
committed only after the freeze and was revised to this plan.
