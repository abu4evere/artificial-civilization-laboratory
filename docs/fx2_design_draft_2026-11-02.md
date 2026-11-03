# FX2 draft: the second round of fault fixes (2 November 2026)

**What this is:** a draft for a council round once FX1's result is known. It would run on v12 if FX1 is adopted.
Nothing is frozen or run. The faults are from `docs/rules_review_2026-11-02.md`; the evidence is in
`docs/research/rock_mark_durability_2026-11-02.md`.

## The faults
- **F4. Materials beyond the carry limit** (`actions.resolve_hunts`, `biology.die`).
  - **The fault:** hide and bone from a kill, and materials inherited at a death, are added past the 20-unit material
    limit.
  - **The fix:** what goes past a person's limit is left on their tile's pile (`tile.pile`), as materials set down
    are. It is kept, not deleted, by the same principle as v8's law for made things.
  - **With AF1's K, if adopted:** the limit is the container-raised one.
- **F5. A leaky container saves water walks** (`weather.drink`).
  - **The fault:** the walk-saving uses the best carry factor. The comment says "something that holds water".
  - **The fix:** only a thing that can hold water (`can_hold(item, "water") > 0`) saves walking, by the same formula
    with that thing's carry factor.
- **F6. Mark depth mixes scales** (`marks.tool_of`).
  - **The fault:** made things' `hard` and `edge` (0–100) are used as if on raw markers' 0–1 scale. Made-tool marks
    come out up to about 100 times deeper.
  - **The fix, in two parts:**
    - **(a) the scale:** a made thing's `hard` and `edge` are divided by 100 in `tool_of`, as `matter.factor` does;
    - **(b) the wear, anchored to evidence:** without this, fixing the scale alone would cut rock marks to about 17
      years, against both the docstring ("rock marks last generations") and the evidence.
      - **The assumption:** mark depth 1.0 = 1 mm.
      - **Rock:** linear retreat of 5.4 mm per thousand years (Portenga & Bierman 2011, outcrop median), about 0.0001
        mm a week.
      - **Wood:** 0.05 mm a year (Williams et al. 2001, planed wood), about 0.001 mm a week.
      - **Ground:** unchanged (× 0.8 a week), since no anchor has been found.
      - A mark is gone below 0.05 mm, as now.
    - **Expected lifetimes:**

      | mark | rock | wood |
      |---|---|---|
      | stone, 0.29 mm | about 45 years | |
      | stone, 0.54 mm | | about 10 years |

## Questions for the council
1. Is (b) a fault fix or a new law? It changes a rate to match evidence, which is calibration, like AG1's ageing. If it
   is calibration, it needs a calibration study (AG1-style) rather than a harm check.
2. Should F6(a) and F6(b) go together? (a) alone shortens marks; (a) and (b) together lengthen them.
3. **Primary, if run as a study:**
   - a harm check for F4 and F5;
   - for F6, a described effect on KL1's measure (know-how revived through marks) and on shared mark meanings
     (`marks.shared`).
