# Adopting AG1's arm b as nature v10: GPT's and Gemini's views (31 October 2026; opinions, not sign-off)

**The decision is the creator's** (at the PC: "Adopt b as v10 now"). Both models were consulted, as the adoption path
requires, with the same text: GPT in fresh chat `6ae58e26`, Gemini in chat `baf24cca07e573da`.

## GPT: adopt, 93%
- "I see no compelling reason to reject it. The improvement is large, the sham is stable, the population checks pass,
  and the change is biologically motivated rather than engineered to improve cognition."
- **The zero checks should show:**
  - exact equality with AG1's arm b, and v10 with the old base = v9;
  - save and reload;
  - the live defaults.
- **The first study on v10 should check:** age-specific mortality, age structure, population, and knowledge
  transmission.
- **On IW1:** "If IW1 runs on v10, refreeze its protocol and baseline."
- **Caution:** "Matching forager mortality better does not establish that the entire ageing model is realistic."

## Gemini: adopt, 98%
- No reason not to adopt.
- **The zero checks should show** bit-for-bit equality with arm b.
- **The first study should watch** whether a larger elder cohort acts as a "caloric sink" that raises group hunger,
  and so the hunger penalty on making.

## Council (checked against the code)
- **Every zero check both asked for was run, and all pass** (`experiments/NV10_nature_v10/zero.txt`).
- **Corrected:** Gemini asked to verify that the change "does not alter infant/juvenile survival logic". It does, a
  little:
  - the Gompertz term `mortality_base × e^(rate × age)` applies at every age (`biology.py`), so children's background
    risk falls by the same factor;
  - that is what AG1's arm b tested, and v10 equals it exactly.
- **On GPT's IW1 point:** IW1 was frozen on `code_v9` before the adoption, so it stays on v9 and its findings are v9's.
  No refreeze is needed.
