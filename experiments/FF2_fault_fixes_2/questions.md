# FF2: Fixing three more faults, in nature v12 (frozen plan)

**A fault-fix check in a copy, not a new law** (the second round, after FF1).
- **The copy:** `code_ff2` = `code_v12` + three settings, `fix_hunt_expect` (F8), `fix_mat_limit` (F4) and
  `fix_water_holder` (F5). With all three at 0 it is v12 exactly.
- **The authority:** the creator, 2 November 2026: "I give you permission to edit world rules. Take a look and check
  all rules. If you find something fix it or add any new rules. From now on keep working without me".
- **The sources:**
  - the rules review, `docs/rules_review_2026-11-02.md` (F4, F5; F8 appended 3 November);
  - the draft, `docs/ff2_design_draft_2026-11-02.md`;
  - HN1's findings (F8 measured: 36.75 expected against 8.79 given per success).
- **The council:** round 54, `docs/debate_round54_after_hn1_am1_2026-11-03.md`. All three rank this first; final votes
  GPT 97%, Gemini 99%, DeepSeek about 92%.
- **Not in FF2:**
  - **F7** (per-species catch rates, never read since the first commit; provenance unknown) is a calibration item for
    HR1, not a fault;
  - **F6** (mark scale and wear) is a separate calibration item.

## The three faults (the code does not do what its own rule says)
- **F8, the hunt decision's meat** (`mind.decide`, the hunt option; setting `fix_hunt_expect`).
  - **The fault:** the option weighs a success as `(hunt_prey_base 25 + hunt_prey_per_hunter 12 × min(n, 5)) ÷ n` food
    per hunter. These two settings date from the first commit and are read nowhere else. What a kill really gives is
    the meat of the animals taken (`fauna.take_prey`): a rabbit success takes 3 (9 food), fish 7 (10.5), a deer 22, a
    bison 55.
  - **The fix:** the option weighs a success as the meat **of the prey the person sees on that tile**, divided by n.
    - It is the mean, over the prey groups that `take_prey` would choose from on that tile (the same list, in the same
      way), of the species' meat × the number it takes from that group.
    - It reads only what the option already reads to require prey (`fauna.prey_here`): the animals on that tile now.
    - It is not exact foresight (GPT's caution): it does not know which group a success would take, nor whether the
      roll succeeds.
  - **Unchanged:** the success chance, the distance and hunger terms, fear, and everything about the hunt itself.
- **F4, materials past the carry limit** (`actions.resolve_hunts`, `biology.die`; setting `fix_mat_limit`).
  - **The fault:** hide and bone from a kill, and the materials an heir takes at a death, are added past the 20-unit
    material limit (`material_limit`), which gathering obeys.
  - **The fix:** a person takes what fits under the limit. The rest is left on the pile of the tile where it happened
    (`tile.pile`, which keeps materials set down). Nothing is deleted.
    - Hide and bone: each share goes to the same hunter, chosen by the same draws as now.
    - An heir takes each material in the dead person's own order until the limit is reached.
    - A pile left this way records no builder: nobody chose to build with it.
- **F5, a leaky container saves water walks** (`weather.drink`; setting `fix_water_holder`).
  - **The fault:** the comment says "something that holds water saves some of the walking". The code uses the best
    **carry** factor, so a basket that cannot hold water (`matter.can_hold` = 0) cuts the walk.
  - **The fix:** only a thing that can hold water (`can_hold(item, "water") > 0`) saves walking. The formula is the
    same, with the best carry factor among such things (1.0, no saving, if none).

## Arms (32 paired seeds 22701–22732; LP: 80 founders, 80 × 80; 200 years; years 100–200 counted)
| arm | `fix_hunt_expect` | `fix_mat_limit` | `fix_water_holder` | |
|---|---|---|---|---|
| **v12** (c) | 0 | 0 | 0 | = `code_v12` (shown by the zero checks) |
| **f** | 1 | 1 | 1 | the candidate nature v13 |
| **f8** | 1 | 0 | 0 | described only |
| **f4** | 0 | 1 | 0 | described only |
| **f5** | 0 | 0 | 1 | described only |
| **sham** (x) | 0 | 0 | 0 | v12 with `sham_draw` 1 |

## Decision (frozen): a check for harm only (FF1's rule)
- **Guards** (f against v12):
  - **Population:** living-weeks in years 100–200, f ÷ v12 below 0.90 with the upper bound of its 95% interval below 1.
  - **Extinctions:** 3 or more worlds beyond v12's.
- **Intervals:** a paired world bootstrap, 10,000 replicates, NumPy seed 20261109. The same drawn seeds are used for
  every arm.
- **Reading:**
  - **"No harm"** if neither guard is raised. f is then adopted as **nature v13**: a fault fix restores what the rule
    says; it is not a new law, so there is no confirmatory run (as FF1; round 54).
  - **"Harm: investigate"** if a guard is raised. The cause is found and appended before anything else. The fault is
    not simply kept.
- **Flag for investigation** (not a stop): a read-only explanation is written before adoption if, for f against v12,
  any described measure below has a ratio outside [0.8, 1.25] with its 95% interval wholly outside 1. Adoption then
  goes ahead unless the explanation finds harm.
- **The sham:** sham − v12 is shown beside every contrast, for scale.

## Described (not decisive), per arm and as f, f8, f4, f5 and sham against v12
- **F8 at work** (a log the code writes at each hunt option; read by nothing in the world):
  - hunt options offered per 1,000 adult-weeks;
  - the mean food per success the option expects, under v12's rule and under the fixed rule, on the same options.
- **Hunting** (from the world's own `hunt` events): hunter-weeks per 1,000 adult-weeks, the success share, and meat
  from hunts per adult-year.
- **F4 at work** (log): material units past the limit, by source (hunt, inheritance): kept by the person (v12's rule) or
  left on the pile (the fix).
- **F5 at work** (log): water-walk weeks (adults) in which the best carry thing cannot hold water but would cut the
  walk under v12's rule.
- **Making:** makes per adult-year; made things held per adult (yearly census).
- **Population:** living-weeks and adult-weeks.

## Validity (hard stops)
- **Zero checks:**
  - `code_ff2` with all three settings 0 = `code_v12` (state and random numbers, 20 and 60 years);
  - the observer and the log are read-only (the same state with and without them; c, f, f8, f4, f5);
  - the sham acts; each fix acts where its log shows it triggered (the state then differs from v12's); a fix whose log
    shows no trigger in these runs is reported as "not triggered", which is not a failure;
  - reload is exact (arm f, saved at year 10, continues exactly to year 15);
  - **F8 unit check:** in an f8 world (30 years), at every hunt option the log's fixed-rule share equals the mean meat
    × number taken over `take_prey`'s list on that tile, ÷ n, computed independently;
  - **F4 unit check:** in an f world (60 years), materials are conserved at every hunt and death (what leaves the dead
    person or the kill is in hands or on the pile), and no person who was at or below the limit before a hunt or an
    inheritance is above it after;
  - **F5 unit check:** in an f world (60 years), no water walk is cut unless the person holds a thing that can hold
    water.
- **All 6 × 32 worlds** are present under one `code_ff2` fingerprint.
- **A blind recompute** by GPT, Gemini and DeepSeek, from per-world counts, of:
  - the population ratio f ÷ v12 and its interval;
  - the extinction difference;
  - the reading;
  - hunter-weeks per 1,000 adult-weeks per arm.

## Adoption (if "no harm")
1. `code_v13` = `code_v12` with all three settings default 1.
2. **Zero checks:** v13 with all three at 0 = `code_v12`; v13 = FF2's arm f.
3. Reference hashes regenerated; the tests pass.
4. Tag `nature-v13`, a line in `docs/autonomous_decisions.md`, and a Telegram to the creator.

## The assistant's prior
1. **No guard raised.**
2. **F8:** the expected food per success falls from about 37 to about 10; hunting, already rare (HN1: one adult-week
   in about 7,650 on v11), becomes rarer still; the hunting ratio is flagged and explained (fewer, honest choices).
3. **F4:** it triggers rarely (tens of units per world over the century), mostly at inheritance.
4. **F5:** it triggers rarely (few people hold a carry thing that cannot hold water when they walk to water).

## Sign-off (3 November 2026)
The assistant, under the creator's permission to edit world rules (2 November). Council round 54: GPT 97%, Gemini 99%,
DeepSeek about 92%, the assistant 90%. Frozen as `FF2-frozen` before any code or data.
