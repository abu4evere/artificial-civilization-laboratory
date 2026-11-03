# ACL council, round 53: after AF1, what to test next? (3 November 2026)

The same question goes to GPT, Gemini and DeepSeek. Your answer is an opinion, not sign-off.

## What we now know (all final, recomputed blind)
- **AF1 (just finished):** neither "make by what it does" (S) nor "containers contain" (K) lets late inventions be made
  again.
  - **Remade:** v11 1 of 3,414; S 2 of 3,437; K 0 of 3,150; S+K 0 of 3,194. No harm.
  - **Adults hold 0.9 made things on average** (the limit is 3) and **make something about once in 14 years** (0.07
    makes per adult-year).
  - About 80% of late kinds are still known by someone alive 5 years later. Knowledge is not lost; it is not used.
- **The earlier line:**
  - UP1: blocked at "cannot make";
  - WP1: wanting the parts does not help;
  - IW1: worth is learned correctly, but made things help modestly (0.163 per use);
  - CO2: making loses mainly on the built-in pull;
  - **TR1: tools add 1.0% of foraged food** (the best tool in anyone's hands would add 20%), and **hunting gives about
    0.001% of all food**.
- **An older evidence review** (`experiments/FX1_extracted_foods/evidence.md`, nature v2; the ID FX1 is that study's):
  - **in ACL:** 98.9% of food is wild plants simply picked up, and meat is 0.02%. A hunting week returns about 4% of a
    foraging week (8% success × 10.5 meat ≈ 0.9 food against about 20);
  - **among foragers** (Kaplan et al. 2000): about 60% of calories hunted. Among the Aché (Hill et al. 1987), hunting
    and gathering return about the same per hour (1,339 against 1,221 calories).
  - **Its candidates:** "embedded plant food" was then tested (FX2, FX3: tool use rose but worlds starved). **"Meat
    worth hunting" was never tested.**
- **New source** (Cordain et al. 2000, *Am J Clin Nutr* 71:682; abstract read): "Most (73%) of worldwide hunter-gatherer
  societies derived >50% of subsistence from animal foods". Hunter-gatherers ate "45-65% of energy" from animal food
  "whenever and wherever it was ecologically possible". (Its Ethnographic Atlas basis is debated, and warm-climate
  foragers rely more on plants.)
- **Where ACL's low hunting returns come from in the code** (the old review, still the same in v11):
  - a base success chance of 0.10, multiplied by a tool factor and capped at 0.92;
  - no prey on the tile means no chance, and the week is lost;
  - small game dominates;
  - meat beyond carrying room is lost.

## The reading to test
- In ACL, made things matter little because **the world asks little of them**: plants are simply picked up, and
  hunting, where weapons should matter most, returns almost nothing.
- So people rarely make, and new kinds are never worth making again.
- Calibrating hunting to evidence is **realism, not a reward**: it would make knowing matter by honest physics, as AG1
  calibrated ageing to the !Kung.

## Options
- **A. HR1, hunting returns anchored to forager evidence.** A calibration study like AG1:
  - **first,** a read-only funnel of where v11's hunts fail (no prey on the tile, the success roll, meat lost to
    carrying);
  - **then,** arms that change **one existing setting each** toward the evidence: base chance, prey density, or meat
    kept;
  - **primary:** calibration distance of the ratio of hunting to foraging returns (the Aché's about 1.1), or of the
    animal share of food;
  - **chosen on calibration and safety, never on remaking.** Remaking and tool use would be described only.
- **B. MT1:** made things as hammers and binders, by property (`docs/mt1_design_draft_2026-11-02.md`).
- **C. FT1:** free choice of targets (`docs/ft1_design_draft_2026-11-02.md`).
- **D. FF2:** the second round of fault fixes, after FF1 (`docs/ff2_design_draft_2026-11-02.md`). It covers materials
  past the limit, leaky water containers, and the scale of mark depth with wear anchored to evidence.
- **E.** The 12-recipe memory cap, anchored to evidence on individual know-how (27–51 plant uses per Tsimane adult in
  free lists; `docs/research/toolkit_sizes_2026-11-02.md`).

## Questions
1. Rank A–E for what moves ACL toward Bob, with an estimate (%) that your first choice succeeds (valid, answers its
   question, keeps to ACL's rules).
2. **For A:**
   - which single setting is the honest one to calibrate first;
   - which evidence target: the hunting/foraging return ratio, or the animal share of diet;
   - how do we keep it from becoming tuning toward an outcome?
3. Anything wrong in the reading above?

Please answer briefly (under 400 words).
