# PC1: the part chains of new kinds: why lessons fail on a missing part (frozen plan)

**A read-only study on nature v15,** council round 73's first choice (`docs/debate_round73_after_fp1_sp1_2026-11-07.md`;
GPT 98%, DeepSeek about 93%; Gemini would run it alongside HR1). SP1 found that, of new-kind lessons that pass the
learner's acceptance, **97.6% fail on a missing part**. PC1 maps those failures: how many parts are missing and how
deep, whether the teacher knows them, and what the one-level part lesson (NV3's parts-first) does. **PC1 decides no
law.** It shows whether a learner-driven, deeper part lesson (round 73's (b)) could help, and how far it would have to
reach.

## Design
- **Code:** `code_v15` (fingerprint 3d46cd2c…), unchanged. One arm, no sham. LP (80 founders, 80 × 80).
- **Seeds 24501–24532** (32 new seeds, used by no study). 200 years.
- **The kinds followed:** invented kinds, those whose first record is made or heated, born in **years 100–190** and
  followed to year 200, as in SP1.
- **A code fact behind the design:** a copying error in a lesson changes raw materials, forms, tools or binders, never
  a made part (`information._recipe_as_shown`). So the made parts of a failed lesson are real kinds.

## The observer (read-only)
It wraps, never changes, `knowhow.remember_recipe` (births and learning), `information.hear_how` and
`knowhow.can_follow`. Every check it makes is a pure function of state, with no random draws.

**At a kind's birth, its tree:** its made parts (parts not in `MATERIALS`, and the part of a heat recipe), followed
recursively through the world's first record of each part (`world.knowledge[part]["recipe"]`). It records:
- the depth (the longest chain of made parts);
- the number of distinct made parts;
- parts with no world record, and cycles.

**For each top-level lesson of a followed kind** (`hear_how`, meant = K, not a part lesson) that **fails on a missing
part** (it passes the acceptance draw, then `can_follow` is False), it records:
1. **The missing made parts:** the recipe's made parts that the learner does not know. It records their number and,
   for each:
   - whether the teacher knows it;
   - whether anyone alive knows it;
   - its own missing depth: how many further unknown made parts lie beneath it, by the world's record.
2. **The part lesson** that follows, if any (NV3: the first made part of the recipe, in its own order, that the
   teacher knows), and its outcome:
   - **wasted:** the learner already knew that part;
   - declined at the draw;
   - itself failed on a missing part;
   - taken.
   - Also whether the part shown was one the learner was missing.
3. **What followed for that learner within 5 years:**
   - whether they learned the missing parts (any route);
   - whether they learned K itself (any route);
   - whether they made K.

## Zero checks (hard stops)
1. **Read-only:** world and random-stream hashes with and without the observer (20 and 60 years).
2. **Outcome replica:** every observed part lesson's outcome agrees with the learner's state (a "taken" part lesson
   matches one `learn` event with that thing, same week and learner). There are 0 mismatches.
3. **Tree check:** for every followed kind, the tree's depth and part count are recomputed by a second, independent
   function, and agree.
4. **Reload is exact.**
5. **All 32 worlds** are present under one fingerprint.

## Measures (descriptive; world bootstrap 95%, 10,000 draws; populations beside each)
1. **Trees:** the distribution of depth and of made-part count over followed kinds.
2. **Failed lessons:**
   - the distribution of the number of missing made parts, and of the deepest missing depth;
   - **the share where the teacher knows every missing part**, some of them, or none.
3. **Part lessons, per failed lesson:**
   - shown, or not (the teacher knows no made part);
   - wasted (a part the learner knew);
   - declined;
   - nested failure;
   - taken;
   - the share of shown parts that were ones the learner was missing.
4. **Later, within 5 years, per (learner, kind):** learned a missing part; learned K; made K.

## Reading (frozen; it guides (b), and decides no law)
- **"A deeper, learner-driven part lesson could help"** if, in most failed lessons (above 0.5), the teacher knows every
  missing part, and the one-level part lesson is mostly wasted, declined or failed nested.
- **"It could not"** if, in most failed lessons, the teacher knows none of the missing parts: the knowledge is not
  within the teacher's reach.
- **"Mixed"** otherwise.
- Each share is given with its interval. The reading uses the point estimate, and names a share whose interval crosses
  0.5.

## A blind recompute
GPT, Gemini and DeepSeek, from a per-world count file built by a script written before data.

## Prior (the assistant)
- Most trees are 1–2 deep.
- In most failed lessons a single part is missing.
- The teacher knows it in most of them (about 70%), since teachers usually learned the parts on the way.
- The one-level part lesson is often wasted (about 40%), because it shows the first part, which the learner may
  already know.
- **Reading: "could help", about 60%.**

## Sign-off (7 November 2026)
The assistant, under the creator's 2 November permission and sleep-mode autonomy. The creator last wrote at 03:16:
"Alr bro peace im drifting off leaving u alone". Council round 73: GPT 98% and DeepSeek about 93% for this study first;
Gemini would run it alongside HR1. The assistant 85%. Frozen as `PC1-frozen` before any code or data.
