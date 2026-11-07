# NV15: Nature v15, children may make again (adopted 6 November 2026)

**Adopted by the assistant by `CLAUDE.md`'s safe path for a new law, under the creator's sleep-mode autonomy.**
- The creator's permission to edit world rules, 2 November 2026: "I give you permission to edit world rules. Take a
  look and check all rules. If you find something fix it or add any new rules. From now on keep working without me".
- Their last messages, 6 November: "check everything and learn first then keep working", then "keep working bro".

1. **A frozen study whose result supports the change:** CI1 (frozen `CI1-frozen`; final). LG was supported: the
   complete-set share went 0.0042 → 0.0225, +0.0183 [+0.0125, +0.0239], with no guard raised.
2. **An independent blind recompute:** GPT and Gemini, each with code, matched CI1 and CI1-C to 4 decimals.
3. **A confirmatory run on new seeds:** CI1-C (frozen `CI1C-frozen`; final) CONFIRMED all three frozen conditions on
   seeds 24101–24132:
   - no guard raised;
   - LG − v14 +0.0221 [+0.0166, +0.0283] (0.0041 → 0.0262);
   - LG − sham +0.0218 [+0.0169, +0.0278].
4. **The council on adoption, round 71** (`docs/debate_round71_adoption_v15_2026-11-06.md`): GPT 99%, Gemini 100%,
   DeepSeek about 94%; the assistant 92%.
5. **`code_v15`,** with zero checks (`zero.txt`): all pass (6 November 2026; zero.txt written at 21:29, by its file time): v15's code with child_make 0 = `code_v14` (4 runs, world and random stream); v15 = CI1-C's arm g (`code_ci1` with child_make 1, held_aim 0, CI1-C's set-up; 2 seeds); the live package's defaults = v15 (2 seeds); the law acts; reload is exact.
6. **Reference hashes** regenerated, and the tests passing: 70 pass (69 plus v15's replay test), run at 21:33. The live reference hashes were regenerated (= v15) and v15's set added; v14's is kept. Fingerprints: live `acl/` 2c95d323…; `code_v15` 3d46cd2c….
7. **A tag `nature-v15`,** a line in `docs/autonomous_decisions.md`, and a Telegram message.

## What changed (two files; `v14_to_v15.diff`)
- **`config.child_make` = 1.** Children aged 3 and over are offered the make option: they may make again a recipe they
  know, by the same rule as the grown (their own valuation, diligence, hunger and holdings).
  - **Before:** only people aged 12 and over were offered it. Children invented about 85% of new kinds in play (RF1)
    but could never choose to make them again.
  - Heat recipes are included when the child stands at a fire. Setting things down, holding food in the fire and
    filling stay for the grown (`mind.decide`: the grown block is split into the make block and the rest).
- **Not carried:** CI1's other arm, IN (a held aim that keeps its pieces). It had no effect and is set aside.
- **Unchanged:** the age floor of 3 is the code's existing `toddler` line, which already gates play. It is a chosen
  threshold, not an evidence-derived one: the Lew-Levy review reports children making simple tools by about 4–5. It is
  recorded as a known gap.

## What it does (CI1-C, 32 paired new worlds; LG against v14)
- **New inventions reaching a complete set of pieces:** about six times as often (0.0041 → 0.0262).
- **Kinds made again by their inventor within 5 years:** 2 → 32 of about 4,000. 31 of the 32 were by inventors who
  were children, spread over 20 of the 32 worlds.
- **Harm:** none. Starvation 0.994, child deaths 0.926, child starvation 0.945, living-weeks 0.973, extinctions 0
  against 2, gifts to kin's children 1.022.
- **Not changed: spread.** No new kind was made by anyone but its inventor within 5 years, in any arm (0 of about
  11,500). v15 raises making and remaking by the inventor. It does not yet show knowledge passing between people.
  That is the next wall for Bob.

## For studies
New studies use `code_v15`. v14 findings stay v14's. v14 stays in `experiments/NV14_nature_v14/code_v14`, so the change
can always be undone.

## A correction made on the way
The claim that heat recipes stay out of children's reach was in round 68, CI1's plan and CI1's findings. It was
wrong: the make option offers heat recipes at a fire. The correction is appended to CI1's findings and recorded in
round 71. No result changes.
