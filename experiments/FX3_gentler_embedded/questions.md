# FX3 — Food that must be opened, at gentler settings: does the tool route change survival? (DRAFT, 21 October 2026; for the creator's sign-off)

**Why.** FX2 (`../FX2_embedded_food/findings.md`, `FX2-done`): with half of each tile's plant food embedded
(`embedded_share` 0.5) and bare hands opening it at a fifth of the normal rate (`embedded_bare` 0.2), people took up
hard tools when tools helped (a hard thing in hand in 40% of forage-weeks against 24%), but **every world died out** in
both E and E0, so the tool benefit could not show in survival. Both numbers were operational. The creator approved a
gentler follow-up (21 October 2026). **A study setting, not a change to nature**, using FX2's own code unchanged.

## Question

At settings where worlds can survive, does being able to open food with a hard thing (E) change survival against the
same world where it does not help (E0)? And do people still take up tools?

## Design (the assistant's recommendation; decisions marked)

**Code:** `code_fx2` exactly as frozen (`FX2-frozen`); only its settings differ. No new code.

**Two gentler levels (Decision 1), each with and without the tool route, plus the control:**

| arm | `embedded_share` | `embedded_bare` | hard things help | gentler than FX2 because |
|---|---|---|---|---|
| **C** | 0 | – | – | today's world (reference) |
| **S25** | 0.25 | 0.2 | yes | a quarter of plant food embedded, not half |
| **S25-0** | 0.25 | 0.2 | no | same, no tool route |
| **B50** | 0.5 | 0.5 | yes | half embedded, but bare hands open it at half the rate, not a fifth |
| **B50-0** | 0.5 | 0.5 | no | same, no tool route |

The numbers stay **operational**, chosen before any run by one rule: each level halves one of FX2's two harsh
settings (the share embedded, or what bare hands cannot get). No pilot of survival is run to pick them (that would tune
toward an answer). The embedded share of real foragers' diet, about 32% extracted food (Kaplan et al. 2000, via FX1),
sits between S25 and B50.

- **Seeds (Decision 2):** **256 new, 7301–7556** (used by no study), 20 founders, 40 × 40, 120 years; 1,280 worlds.
- **Where (Decision 3):** **on GitHub's machines** (`cloud-run`, 20 jobs at once; the zero checks run there first;
  results fetched and analysed here). The study's own zero checks: settings 0 = `code_v2`; each arm acts; observers
  read-only; save and reload exact (FX2's checks, reused).

## The frozen readings (proposed)

- **Primary 1 (survival, the question FX2 could not answer):** extinction, **S25 against S25-0** and **B50 against
  B50-0**, paired by seed: exact sign test; effect with a 95% bootstrap interval (10,000 resamples,
  `random.Random(2026)`); yardstick ±0.117; Holm over the two. Readings as FX2: "the tool route changes survival"
  (p < 0.05 after Holm), "no meaningful effect" (p ≥ 0.05 and the interval inside ±0.117), otherwise "unresolved".
- **Primary 2 (tool use):** share of adult forage-weeks with a hard thing (hardness ≥ 40) in hand, **S25 against
  S25-0** and **B50 against B50-0**, Wilcoxon signed-rank, bootstrap interval as above; Holm over the two.
- **Survival is always read**, whatever the extinction level (GPT's review: a rule that set aside a level whose tool-free
  arm dies out heavily could hide exactly a rescue by tools, e.g. 95% against 70%).
- **Limits on the mechanism measures only (stated in advance):** a tool-use comparison is labelled **"limited"**, and
  described rather than tested, if fewer than 64 seeds give adult forage-weeks in both arms of the pair. 64 is a
  practical minimum (a quarter of the seeds), not a calculated sample size; it applies the same way to both pairs and
  is fixed here. Survival is never labelled this way.
- **What the words mean:** "no meaningful effect" means p ≥ 0.05 after Holm **and** the 95% interval inside ±0.117
  (the yardstick every recent study uses); "changes survival" means p < 0.05 after Holm; anything else is
  "unresolved". The prior's "barely changes survival" means "no meaningful effect" in this sense. Every "changes
  survival" reading also carries a size label, **"beyond the yardstick"** (the estimate outside ±0.117) or **"within
  the yardstick"**, so a difference that is real but small is not read as a large one. The reading rules themselves
  stay the ones every recent study used, so FX3 can be compared with them.
- **Paired seeds:** the same 256 seeds in all five arms; every comparison is paired by seed.
- **Described** (population first): each arm against C (extinction, median population at years 60 and 119); births;
  partner blocking; embedded share of adults' food; how much embedded food was opened with a hard thing; forage-weeks a
  hard thing was used on embedded food (FX2's measures, the creator's note on "carried" versus "used"). Carrying a
  hard thing (primary 2) and using one on embedded food (described) are reported separately: the mechanism is use,
  not carrying.

## The assistant's prior (to be frozen at sign-off; held loosely)

S25 against S25-0: **no meaningful effect** on
survival (a quarter embedded is mild; the tool route matters little). B50 against B50-0: **the tool route changes
survival** (fewer worlds die with it), because half the food is embedded and a tool can double what bare hands get. Tool use
rises in both tool arms, **more in S25** (where bare hands get only a fifth, a tool helps more per use: up to five
times, against twice in B50). Each tool-free arm dies out more than C.

## Revision 1 (21 October 2026, before freezing; GPT's review, `gpt_review_fx3.md`)

The "no room" rule is removed: survival is always read. Limits apply only to the tool-use measures, defined above.
"No meaningful effect" and "changes survival" are defined in words; seeds are paired across all five arms; carrying and
using a hard thing are reported separately. The code fingerprint of `code_fx2` is recorded by the zero checks before any
world runs.

## Revision 2 (21 October 2026, before freezing; GPT's second review, `gpt_review_fx3.md`)

Size labels added to "changes survival" (beyond or within the ±0.117 yardstick), keeping the standard reading rules
for comparability with earlier studies; the 64-seed minimum is stated as practical, not calculated.

## Decisions for the creator

1. Levels: **S25 and B50, each with and without the tool route, plus C** (recommended), or only one level (768 worlds).
2. Seeds: **256 new, 7301–7556** (recommended).
3. Where: **on GitHub's machines** (recommended), or on this computer (about two days).
4. The prior above, frozen as written.
