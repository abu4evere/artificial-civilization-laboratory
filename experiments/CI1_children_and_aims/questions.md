# CI1: Children may make again, and a held aim that keeps the pieces (frozen plan)

**A test of two general laws in a copy of nature v14, with a sham.**
- `code_ci1` = `code_v14` + two settings, `child_make` (LG) and `held_aim` (IN). With both at 0 it is v14 exactly.
- Nothing goes live except by the safe path: a final supported study, blind recomputes, a confirmatory run on new
  seeds, council, zero checks and tests.

**Why:**
- **RF1 (final):**
  - 1,062 of 1,246 new kinds were invented by people not yet grown, in play, and only the grown are offered "make
    again";
  - among grown inventors who wanted their thing again, pursuit failed (0.797): every started kind gathered a missing
    input, but in 45 of 53 a gathered piece was later gone before the set was complete. The missing pieces were mostly
    made parts.
- **The pull toward missing pieces already exists** (`mind._material_wants`, `mind._wanted_parts`). What is missing
  is keeping the pieces (`docs/ci1_design_draft_2026-11-06.md`).
- **Council rounds 67 and 68** (`docs/debate_round67_after_rf1_2026-11-06.md`,
  `docs/debate_round68_after_v14_2026-11-06.md`): one study with separate arms. IN is retention only, with nested
  pieces protected and survival uses open. LG is the make option only. The primary is a per-kind complete-set share.
- **Evidence for LG:** Lew-Levy et al. 2017 (`docs/research/children_tool_making_2026-11-06.md`; read as a summary).
  Hunter-gatherer children make their own simple tools by about 4–5.
- **The general form of a held course of action:** Sutton, Precup & Singh 1999
  (`docs/research/options_held_aims_2026-11-05.md`).

## The two laws (general; nothing named)
**LG, `child_make` = 1: children may make again what they know.**
- The make option (`mind.decide`, now inside `if grown:`) is offered also to children aged 3 and over (not toddlers).
- It uses exactly the same rule: the value floor 0.05, `can_make`, and the pull `worth_weight × value × (0.6 + 0.4 ×
  diligence) × (1 − 0.5 × hunger)` with the child's own genes and hunger.
- Put, heat and fill stay for the grown.

**IN, `held_aim` = 1: a held aim keeps its pieces.**
- **The aim forms** at a person's decision when they hold none. It is the most valued recipe they know whose value is
  above 0.05, whose thing they do not hold fresh (`_holding`, more than 5 uses left), and whose inputs are not all in
  hand (`can_make` False).
  - Ties are drawn as v14 draws ties.
  - One aim at a time, saved with the person.
- **The pieces it keeps** (recomputed each week from what is held):
  - the aim recipe's own inputs, as `can_make` reads them (raw materials and binders, and made parts), up to the
    number it needs;
  - and, for each made part it needs that is missing and whose recipe the person knows, that part's inputs, up to the
    number needed (one level down).
- **While the aim is held:**
  - a kept piece is not set down (`put`);
  - a kept made part is not handed to another (`hand`);
  - a kept piece is not used in a make of another recipe whose value is not higher than the aim's. **A make of higher
    value interrupts the aim**, which ends, and that make uses what it needs.
  - **Open:** survival uses (lighting a fire, tipping embers), heating at a fire, wear, loss at death, and anything
    the person does not keep.
- **The aim ends** when:
  - all its inputs are in hand (the make option then appears, as now);
  - its value falls to 0.05 or below;
  - its recipe is forgotten;
  - its thing is held fresh again;
  - or a higher-valued make interrupts it.
- **No new pull, no new weight, no time limit.**

## Arms (32 new paired seeds 24001–24032; LP: 80 founders, 80 × 80; 200 years; years 100–200 counted)
| arm | `child_make` | `held_aim` |
|---|---|---|
| **v14** (c) | 0 | 0 |
| **LG** (g) | 1 | 0 |
| **IN** (i) | 0 | 1 |
| **LG+IN** (b) | 1 | 1 |
| **sham** (x) | 0, `sham_draw` 1 | 0 |

## Measures
A paired world bootstrap: 10,000 replicates, NumPy seed 20261122. Each arm is judged alone against v14. The
interaction is described only.

### 1. Primary, per arm: harm guards against v14
A guard is raised by any of:
- **starvation:** deaths per 1,000 living-years, a ratio above 1.25 with the lower bound above 1;
- **killing:** deaths per 1,000 living-years higher by more than 0.05, with the lower bound above 0;
- **adult health:** lower by more than 5 points, with the upper bound below 0;
- **population:** a living-weeks ratio below 0.90 with the upper bound below 1;
- **extinction:** 3 or more extra worlds;
- **child deaths:** deaths of children (under 12) per 1,000 child-years, a ratio above 1.25 with the lower bound above
  1, **and** an absolute rise of 3 or more per 1,000 child-years;
- **child starvation:** starvation deaths of children per 1,000 child-years, a ratio above 1.25 with the lower bound
  above 1;
- **gifts to kin's children:** gifts of food from a person to a child of their kin (their own children,
  grandchildren, siblings' children), per 1,000 adult-weeks, **a ratio below 0.80 with the upper bound below 1**.

### 2. Co-primary, per arm: complete sets
- **The share of world-new kinds** (first made in years 100–195) **whose inventor, while alive and knowing the recipe,
  holds the complete input set (`can_make`) at some week's end within 5 years.**
- Per kind, with all such kinds as the denominator.
- It passes if arm − v14 has its 95% interval wholly above 0.

### 3. Readings, per arm
- **"Supported"** if no guard is raised and the co-primary passes. A supported arm goes to a confirmatory run on new
  seeds before any adoption.
- **"No harm, no effect"** if no guard is raised and the co-primary does not pass.
- **"Harm"** if a guard is raised.
- If both LG and IN are supported, LG+IN is described; the council chooses on this frozen data what goes to
  confirmation first.

### 4. Described
- **Remaking:** the share of world-new kinds made again by their inventor within 5 years. "Make chosen once complete":
  among kinds that reached a complete set, the share made again.
- **Each of the above** for child inventors (under 12 at invention) and grown inventors apart.
- **IN at work:** aims formed, aim-weeks, and endings by cause (complete, value, forgotten, held again, interrupted);
  puts, hands and makes blocked; makes that interrupted.
- **LG at work:** makes by children per 1,000 child-weeks.
- **Context:** care given, food per adult, the share of adult-weeks at the 20-unit carry limit, child health, makes
  per adult-year, world-new kinds, and LG+IN against LG and against IN.

## Validity (hard stops)
- **Zero checks:**
  - `code_ci1` with both at 0 = `code_v14` (20 and 60 years, state and random numbers);
  - the observer is read-only;
  - each arm acts, and the sham acts;
  - reload is exact (arm b, saved at year 10, continues exactly to year 15: the aim saved);
  - **unit checks:**
    - in an IN world (30 years), no kept piece is ever set down, handed, or used in a lower-valued make while the aim
      is held;
    - every aim formed meets the forming rule;
    - in an LG world, every make by a child is of a recipe they knew with `can_make` True before it.
- **All 5 × 32 worlds** are present under one `code_ci1` fingerprint.
- **A smoke run** before the cloud.
- **A blind recompute** by GPT, Gemini and DeepSeek of the guards and the co-primary for each arm.

## Known limits
- IN keeps pieces but does not order the steps (making a part before the whole). If complete sets stay rare, that is the
  next question (GPT).
- Heat recipes stay out of children's reach (they need the grown block). Described, for a possible LG2.
- Remaking is rare (about 1 in 3,000 new kinds in FF3), so it is described, not decided.

## The assistant's prior
- **LG:** complete sets rise (children hold their materials often), no harm likely, **supported about 45%**.
- **IN:** complete sets rise among grown inventors, but the effect on all kinds is small (most inventors are children),
  **supported about 30%**. A hunger guard is possible if keeping blocks a use.
- **LG+IN:** the most complete sets.
- Remaking stays rare in every arm.

## Sign-off (6 November 2026)
The assistant, under the creator's 2 November permission (tests of new laws in a copy, the safe path) and sleep-mode
autonomy (the creator's last messages: "keep working"; on Telegram at 01:58, "you can use pc at full capability").
Council rounds 67 and 68: GPT 95%, Gemini 95%, DeepSeek about 75%; the assistant 75%. Frozen as `CI1-frozen` before
any code or data.

## Amendment 1 (6 November 2026, 10:47, before any code or data): three readings of the IN rule made exact
The frozen text left three cases open. They are read as follows, so the code can be checked against them.
- **"A make" includes making in play.** Play turns held pieces into things through the same crafting (`_craft`) as a
  make, and RF1 found gathered pieces lost to other uses. So, while an aim is held, play is not offered a trial that
  would use up a kept piece, unless that trial's recipe is worth more than the aim. A new trial has value 0, so in
  practice play leaves kept pieces alone.
- **"Heating at a fire" stays open,** as the frozen text says. Heat-verb crafts (holding a material or part in a fire)
  may use a kept piece.
- **"Used" means used up.** A strike uses up the struck material, not the hammer, so only the struck material is
  protected. A bind uses up both parts and the binder; a shape uses up its material.

Nothing else changes: no arm, measure, guard or reading.
