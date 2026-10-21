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
- **Room check (stated in advance):** if a level's tool-free arm dies out in more than 90% of worlds, its survival
  reading is reported as **"no room"** rather than read (FX2's failure, named before the data).
- **Described** (population first): each arm against C (extinction, median population at years 60 and 119); births;
  partner blocking; embedded share of adults' food; how much embedded food was opened with a hard thing; forage-weeks a
  hard thing was used on embedded food (FX2's measures, the creator's note on "carried" versus "used").

## The assistant's prior (to be frozen at sign-off; held loosely)

Both levels leave room (tool-free arms die out in under 90% of worlds). S25 against S25-0: **no meaningful effect** on
survival (a quarter embedded is mild; the tool route matters little). B50 against B50-0: **the tool route changes
survival** (fewer worlds die with it), because half the food is embedded and a tool can double what bare hands get. Tool use
rises in both tool arms, **more in S25** (where bare hands get only a fifth, a tool helps more per use: up to five
times, against twice in B50). Each tool-free arm dies out more than C.

## Decisions for the creator

1. Levels: **S25 and B50, each with and without the tool route, plus C** (recommended), or only one level (768 worlds).
2. Seeds: **256 new, 7301–7556** (recommended).
3. Where: **on GitHub's machines** (recommended), or on this computer (about two days).
4. The prior above, frozen as written.
