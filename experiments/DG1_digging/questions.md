# DG1 — Digging: what do people do when the ground can be opened? (DRAFT for the creator; reviewed by GPT, `gpt_review_dg1.md`; nothing built or run)

**Why (the creator, 23 October 2026):** "make diggin possible ... make these things possible for their nature". The
order agreed: bodies (BD1, running), then digging, then water. GPT's ideas (`../BD1_bodies_stay/gpt_ideas.md`):
digging where terrain and tools allow, at an energy cost; a lasting pit that can hold things, may collect water, and
can be filled or covered; pits never automatically graves, stores or homes.

A **Law 126 study**: one setting, `digging`, default 0 = nature v3 exactly.

## The candidate

**How digging fits ACL without a new action.** ACL's people choose among 19 actions, and their learned habits are
stored per action. A new action would change every person's habits table, even with digging switched off, so the
"off" world would no longer equal v3. Instead, digging is **gathering earth**: a new kind of material to gather, offered
only when `digging` is 1. Gathering earth on a tile deepens a pit there.

1. **Digging:** gathering "earth" on land (not rock, not water; not frozen ground in deep winter) takes v3's gathering
   effort and deepens the tile's pit by an amount set by the best digging tool held (a hard, edged or reaching thing
   digs faster; hands dig slowly). Earth itself is gathered like clay and can be set down again.
2. **A pit is only a hole:** it has a depth. It holds nothing by itself and means nothing. It slowly fills back in
   (rain, collapse) unless it is lined or deepened again.
3. **What a pit does physically:**
   - **food set down in a pit** (v3's "put", on a tile with a pit at least knee-deep) is **hidden** (others see it
     only if they saw it put there) and **keeps longer** (cool earth: slower rot);
   - **a covered pit** (earth set back over it) hides it fully and keeps it longest, but must be dug again to reach;
   - **rain collects** in a deep pit as drinkable water for a while (a seep), if the ground holds water;
   - **a body** in a pit (only possible if someone dies there, until carrying exists) rots out of sight: no smell,
     so no disgust (links BD1).
4. **Nothing else:** no wish to dig, no burial instinct, no "store food in pits" rule. Whether pits become stores,
   wells, graves or nothing is up to them.

## Questions for GPT and the creator before freezing

- Is "gathering earth" an honest way to add digging without a new action? (Its drawback: digging shares the learned
  value of gathering in general.)
- Which pit effects to include in the first study: all four, or only hiding and keeping food (bottleneck B, storage)?
- Rates: how much a pit hides and slows rot, how fast it fills in. Each must be an assumption anchored to evidence
  (storage pits among foragers; the keeping of food in cool ground), never tuned toward an answer.
- Should BD1's result come first, since pits and bodies interact?

## Design (to be fixed after the review)

As BD1: C (v3, or v4 if bodies are adopted) against D; 512 new paired seeds; zero checks; manipulation check (pits are
dug); safety (survival, population); described: pits dug and their uses (food hidden, food kept, water drunk, bodies
inside), stores lost to theft, starvation in winter (does storage help?).

## After GPT's review (to apply in Revision 1)

- First study: **only hiding food and slower rot** in pits; rainwater and bodies in pits later.
- Hidden food can be found by perceivable signs (for example, freshly turned earth), not only by having watched.
- Rates are documented assumptions, with a sensitivity check (two values).
- Freeze DG1 only after BD1 is read, against the resulting baseline.
