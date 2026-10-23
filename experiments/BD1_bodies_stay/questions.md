# BD1 — Bodies stay: what do people do when the dead remain among them? (Revision 1 after GPT's review; SIGNED OFF 23 October 2026 on the creator's instruction; frozen as `BD1-frozen` before any data)

**Why (the creator, 23 October 2026):** "make body not disappear cuz bro its so unwise to make dead bodies to
disappear ... make these things possible for their nature but first ask gpt". The creator chose the assistant's order
(bodies, then digging, then water) and said "do all these things". GPT's ideas: `gpt_ideas.md`.

In v3 a dead person vanishes. Only a "grave" mark stays on the tile for 20 years. If no partner or grown child is on
the same tile, their tools are **deleted** and their food is **turned into plants**. That is not physics. BD1 is a
**Law 126 study**: one setting, `bodies_stay`, that adds a body and its physics, and nothing cultural.

## The candidate (one setting, default 0 = nature v3 exactly), Revision 1 after GPT's review

When someone dies with `bodies_stay` = 1:
1. **A body stays** where they died. Its meat (an adult 18 food units, a child in proportion to age, at least a fifth;
   an assumption, a deer gives 22) and the food they carried (if no relative on the spot took it, v3's rule) lie there
   as food on the ground **owned by the dead** (v3's store). *This keeps v3's existing idea of whose food it is; it is
   a shortcut, not a law of nature (GPT).*
2. **Eating from a body is a choice, not automatic.** It happens only through v3's own decision to take food that is
   not one's own: when hunger is above 0.4, with v3's small scruple for the dead. No new action, no preference.
3. **Tools** stay with the body. A partner or grown child who later stands there takes them (v3's inheritance, later
   in time). Materials go on the ground as in v3.
4. **Rot:** the body's food rots at v3's rate for loose food (4% a week; slower under a shelter or by a fire). It
   counts as **rotten** after 13 weeks (when 40% would have rotted at that rate). When the food is gone, only bones
   stay (v3's trace "bones:person").
5. **Rotten meat** makes the eater ill with chance 0.3 per meal (if not already ill; v3's illness).
6. **Feelings (nature):**
   - **disgust at rot:** standing on or next to a rotten body makes that place feel worse, at most once a week per
     body, through v3's place memory (-0.3; finding one's food gone is -0.6);
   - **knowing by sight:** someone close to the dead who had not known of the death learns it from the body, exactly
     as v3's witnesses of a death do (memory, grief).
   Nothing else: no burial wish, no respect for the dead, no reaction to someone eating a body, no taboo. No
   scavengers in this version (GPT: a fixed scavenging rate would decide too much; a later study).

## Design

- **Code:** `code_bd1` = `code_v3` + `bodies_stay` (default 0) + read-only logging of what happens to each body
  (`v3_to_bd1.diff`).
- **Arms:** C (v3) and B. **Seeds: 512 new, 12001–12512**; 20 founders, 120 years; 1,024 worlds on GitHub.
- **Zero checks (hard stops):** setting 0 = `code_v3`; B acts; observers and logging change nothing; reload exact.
- **Manipulation check (hard stop):** in B, bodies exist, decay, and some are reached by scavengers or people.
- **Safety (primary for adoption):** survival (sign test, bootstrap, yardstick ±0.117) and time-averaged population
  (B / C − 1, lower bound above −0.05 safe; as GR2).
- **Described (the point of the study):**
  - what happens to bodies: weeks until bones; meat lost to decay, scavengers, people;
  - **eating the dead:** how often; by whom (kin of the dead or not); in hunger or not; in which years and
    generations (does it fade or grow over time?); sickness from rotten meat;
  - **avoidance:** time people spend next to rotten bodies; whether places with bodies are avoided later;
  - **grief** from the sight of bodies; belongings recovered by kin; the dead's stores taken by others;
  - deaths by cause.
  BD1 changes several things at once (body, food left, tools, rot, feelings), so it cannot say which one caused an
  outcome (GPT); a change in eating over generations is described, not read as culture (ACL cannot pass on a "do
  not" about an action).

## The adoption rule (fixed now, before any data)

`bodies_stay` is **proposed for nature (v4)** if the manipulation check passes and survival and population are not
worse (survival "no meaningful effect" or fewer worlds dying; population "safe"). Then **the creator decides**
(this is a new kind of nature, not a fix with one number to beat). If survival or population are worse, it is not
adopted as is, and the cause is looked for.

## The assistant's prior

- Bodies mostly rot to bones; people eat from few, almost only in hunger (eating needs hunger above 0.4).
- Eating does **not** fade across generations by itself: ACL has no way to pass on "do not" about an action. That
  absence would itself be a finding about what culture needs.
- Survival and population: no meaningful effect.

## Sign-off (23 October 2026)

The creator: "i like ur way do all these things also taboo stuff ... do all these things i told you" (before
sleeping). Taken as sign-off of BD1 after GPT's review (`gpt_review_bd1.md`). Adoption into nature stays the
creator's decision, by the rule above.

## Operational note (23 October 2026, while building, before any data)

- A throwaway check (seeds 9971–9973, 40 years, not data) showed eating from bodies is possible but rare (one meal
  per world), and many "foul" person-weeks (bodies lie where people live). Nothing was changed after it.
- The body's food uses v3's store list (`tile.stash`), so v3's rot, cover and fire rules apply to it unchanged.
