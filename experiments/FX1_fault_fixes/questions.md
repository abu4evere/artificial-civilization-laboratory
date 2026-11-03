# FX1: Fixing three faults in nature v11 (frozen plan)

**A fault-fix check in a copy, not a new law.**
- **The copy:** `code_fx1` = `code_v11` + two settings, `fix_make_choice` and `fix_overflow`. With both at 0 it is v11
  exactly.
- **The authority:** the creator, 2 November 2026: "I give you permission to edit world rules. Take a look and check
  all rules. If you find something fix it or add any new rules. From now on keep working without me".
- **The source:** the assistant's review of the v11 code, `docs/rules_review_2026-11-02.md`.
- **The council:** round 51, `docs/debate_round51_fx1_2026-11-02.md`. Final votes: GPT 97%, Gemini 99%, DeepSeek about
  95%.

## The three faults (the code does not do what its own rule says)
- **F1, the make choice** (`mind.decide`; setting `fix_make_choice`).
  - **The fault:** a recipe is skipped when its unscaled value v ≤ the best so far's *scaled* utility u (u = k × v,
    with k = 2 × (0.6 + 0.4 × diligence) × (1 − 0.5 × hunger)). So a recipe later in the learned order must exceed k
    times the earlier best, and older recipes are favoured.
  - **The fix:** a recipe is skipped when v ≤ 0.05, the same floor the first recipe meets now. Its u must still exceed
    `best_u`, which starts at 0.05. The highest u wins. Both v11 floors stay exactly.
- **F2, an heir at death** (`biology.die`; setting `fix_overflow`).
  - **The fault:** made things beyond the 3-thing limit are deleted, and the one chosen is the heir's first-held thing.
    v8's law (OP1) says a thing pushed out by the carry limit is left on the ground, and `_keep` pushes out the least
    valued.
  - **The fix:** the least valued by the holder's own item values goes, with ties exactly as in `_keep` (the most
    recently added goes first). It goes onto the ground, unchanged, through `drop_on_ground`.
- **F3, tools taken from a body** (`biology.bodies_week`; setting `fix_overflow`).
  - **The fault:** the overflow goes to the ground, but the one chosen is the first held.
  - **The fix:** the least valued, as in F2.
- **Left for later:** F4, materials beyond the 20-unit limit from hunting and inheritance (see the review).

## Arms (32 paired seeds 22401–22432; LP: 80 founders, 80 × 80; 200 years; years 100–200 counted)
| arm | `fix_make_choice` | `fix_overflow` | |
|---|---|---|---|
| **v11** | 0 | 0 | = `code_v11` (shown by the zero checks) |
| **f** | 1 | 1 | the candidate nature v12 |
| **f1** | 1 | 0 | described only |
| **f23** | 0 | 1 | described only |
| **sham** | 0 | 0 | v11 with `sham_draw` 1 |

## Decision (frozen): a check for harm only
- **Guards** (f against v11):
  - **Population:** living-weeks in years 100–200, f ÷ v11 below 0.90 with the upper bound of its 95% interval below 1.
  - **Extinctions:** 3 or more worlds beyond v11's.
- **Intervals:** a paired world bootstrap, 10,000 replicates, NumPy seed 20261107. The same drawn seeds are used for
  every arm.
- **Reading:**
  - **"No harm"** if neither guard is raised. f is then adopted as **nature v12**: a fault fix restores what the rule
    says; it is not a new law, so there is no confirmatory run (round 51, all three advisors).
  - **"Harm: investigate"** if a guard is raised. The cause is found and appended before anything else. The bug is not
    simply kept.
- **Flag for investigation** (not a stop): a read-only explanation is written before adoption if, for f against v11,
  any described measure below has a ratio outside [0.8, 1.25] with its 95% interval wholly outside 1. Adoption then
  goes ahead unless the explanation finds harm.
- **The sham:** sham − v11 is shown beside every contrast, for scale.

## Described (not decisive), per arm and as f, f1, f23 and sham against v11
- **F1 at work** (a log the code writes at each make choice; read by nothing in the world):
  - **share differing:** the share of adult decisions with a make option in which v11's rule and the fixed rule offer
    different recipes;
  - **newest share:** the share of offered recipes that are the person's most recently learned.
- **F2 and F3 at work:** made things deleted at an inheritance (v11), and made things left on the ground at an
  inheritance.
- **Making:**
  - makes per adult-year;
  - kinds invented per 100 adult-years;
  - **lineage remaking R** (AF1's primary, unchanged): the share of world-new kinds first made in play in years 100–195
    whose own recipe is chosen again by a `make` action within 260 weeks.
- **Holding:** made things held per adult, and made things lying on the ground at year 200.
- **Population:** living-weeks and adult-weeks.

## Validity (hard stops)
- **Zero checks:**
  - `code_fx1` with both settings 0 = `code_v11` (state and random numbers, 20 and 60 years);
  - f, f1, f23 and the sham each act; f, f1 and f23 differ from each other;
  - the observer and the log are read-only (the same state with and without them);
  - reload is exact (arm f, saved at year 10, continues exactly to year 15);
  - **F1 unit check:** in an f world (30 years), at every adult decision with a make option, the offered recipe is the
    argmax of u among eligible recipes (v > 0.05, u > 0.05, holding rule, can-make);
  - **F2/F3 unit check:** in an f world (60 years), no made thing is deleted at an inheritance (every thing is
    conserved into the heir's hands or onto the ground).
- **All 5 × 32 worlds** are present under one `code_fx1` fingerprint.
- **A blind recompute** by GPT, Gemini and DeepSeek, from per-world counts, of:
  - the population ratio f ÷ v11 and its interval;
  - the extinction difference;
  - the reading;
  - R per arm.

## Adoption (if "no harm")
1. `code_v12` = `code_v11` with both settings default 1.
2. **Zero checks:** v12 with both at 0 = `code_v11`; v12 = FX1's arm f.
3. Reference hashes regenerated; the tests pass.
4. Tag `nature-v12`, a line in `docs/autonomous_decisions.md`, and a Telegram to the creator.

## The assistant's prior
1. **No guard raised.**
2. **The offer differs in 1–5% of make decisions,** and f's newest share is higher than v11's.
3. **R stays near 0 in every arm:** "cannot make" still dominates (UP1).
4. **F2:** v11 deletes some tens of things per world over years 100–200.

## Sign-off (2 November 2026)
The assistant, under the creator's permission to edit world rules (2 November). Council round 51: GPT 97%, Gemini 99%,
DeepSeek about 95%, the assistant 85%. Frozen as `FX1-frozen` before any code or data.

## Amendment 1 (2 November 2026, 22:25, before any data)
The code's log also records, at each make choice, whether v11's rule and whether the fixed rule would each offer the
person's newest recipe. This shows F1's effect on the same decisions, and it adds two described columns. Nothing else
changes: no world state, no reading and no guard.

## Amendment 2 (3 November 2026, 01:30): the study's name is FF1
- **Why:** the ID **FX1 was already in use** by an earlier study, `experiments/FX1_extracted_foods` (an evidence
  review of food that must be opened, dug or hunted). FX2 and FX3 also exist.
- **From now on this study is FF1** ("fault fixes"). Its folder (`FX1_fault_fixes`), tag (`FX1-frozen`), code
  (`code_fx1`, `run_fx1.py`, `analyse_fx1.py`) and recompute prompt keep their names, so the frozen files and the
  running cloud job are unchanged.
- **The planned second round of fault fixes is FF2**, not FX2.
