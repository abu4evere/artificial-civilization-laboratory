# NV10 — Nature v10: ageing anchored to the !Kung (adopted 31 October 2026)

**The creator's decision,** at the PC in a Claude Code session, answering a question with the version named: "Adopt b as
v10 now". AG1 was final, and its blind recompute by GPT and Gemini matched. The adoption path followed is the one in
`CLAUDE.md`.

## What changed
- **One number:** `mortality_base` (Gompertz: weekly death risk = base × e^(rate × age)) goes from 1.5 × 10⁻⁵ (v9) to
  **1.5 × 10⁻⁵ × 0.0072 / 0.0249** ≈ 4.3373 × 10⁻⁶. That is AG1's arm b, the !Kung step at age 40. ACL's ageing rate
  is unchanged. `v9_to_v10.diff`: config.py only.
- **The risk applies at every age,** so children's background risk falls by the same factor (tiny at young ages). AG1
  tested exactly this.
- **What AG1 found** (`experiments/AG1_ageing_anchor/findings.md`; 20 paired seeds, 1,000 years):
  - the distance of adult death ages from the forager reference fell from 0.995 to 0.125;
  - mean adult age at death rose from 45 to 54;
  - 44% of adult deaths now come at 60 or older;
  - no flags (population ratio 1.034; extinctions 1 against 2);
  - knowledge did not improve by longer lives alone.

## The adoption path
1. **A frozen study supporting the change:** AG1, final.
2. **Independent blind recompute:** GPT and Gemini matched every number (`recompute_ag1.md`).
3. **Both models consulted on adoption** (`docs/gpt_view_adopt_v10_2026-10-31.md`): GPT 93%, Gemini 98%.
4. **`code_v10`** = `code_v9` with that default. Zero checks pass (`zero.txt`):
   - v10's code with v9's base = `code_v9` (4 runs);
   - v10 = AG1's arm b (2 seeds);
   - the live package's defaults = v10;
   - the change acts;
   - reload is exact.
5. **Reference hashes:** live regenerated (= v10); v10's set added; v9's kept. The tests pass (see the WORKLOG).
6. **Tag:** `nature-v10`. v9 stays in `experiments/NV9_nature_v9/code_v9`, so the change can be undone.

## What it means for studies
- **New studies use `code_v10`.** v9 findings stay v9's.
- **IW1** was frozen on `code_v9` before this adoption, and runs on v9 as frozen.
- **The first study on v10 should watch** (GPT and Gemini):
  - age structure, age-specific mortality and population;
  - who survives to teach;
  - whether a larger elder cohort adds to hunger, and so to the hunger penalty on making (Gemini).
- **GPT's caution:** matching forager mortality better does not make the whole ageing model realistic.
