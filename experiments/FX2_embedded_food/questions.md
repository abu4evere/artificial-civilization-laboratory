# FX2 — Food that must be opened: do tools start to matter? (SIGNED OFF 18 October 2026; frozen as `FX2-frozen`, no study run before it)

**Why.** FX1 (`../FX1_extracted_foods/evidence.md`) measured that ACL's people get **98.9%** of their food by simply
picking wild plants, against about **8%** "collected" food among ten forager societies, where about **32%** is
*extracted* (dug up, cracked open, detoxified) and about 60% hunted (Kaplan, Gurven and Winking 2009, summarising Kaplan
et al. 2000). E8.2 found tools add only a few percent to food. A world that never asks for tools cannot show whether
tools, skill and teaching could matter. GPT, under the creator's delegation (18 Oct 2026), advised testing **food that
must be dug or cracked first, with hunting left unchanged**, drafted for sign-off, no runs before then.

**This is a study setting, not a change to nature.** Adopting it into nature later would be a separate Law 126 decision,
with this study and FX1 as its evidence.

## Question

When part of each tile's plant food is embedded (it yields little to bare hands and much to something hard), do ACL's
people come to forage with hard things in hand, and does the world's survival change?

## The one change: `embedded_share` (default 0 = `code_v2` exactly)

- Each land tile's plant food is split into two stands that grow by today's rule in proportion: **open** (share 1 − s)
  and **embedded** (share s). Total plant food on a tile, its cap and its regrowth are **unchanged**; only how it comes
  away differs.
- Foraging takes open food first, as today. What is still wanted then comes from the embedded stand at a rate
  `b + (1 − b) × hard / 100` of the forage rate, where `hard` is the hardness of the hardest thing in hand (0 bare-handed),
  read from properties ACL already has (`matter.PROPS`). No new item, recipe or action is added; nothing tells anyone
  that a hard thing helps. They can only find it by doing it, as every other use of an item is found (`_judge_use`).
- Nothing else changes: hunting, crops, carrying, sharing, storage.

**The two numbers (Decision 3), stated as operational, not anchored:**

- `s` = **0.5** (half of the plant food embedded). FX1's anchor is a diet share (extracted food is about 80% of forager
  plant calories), which is a result of choices, not what the land holds; no measure of the land was found. 0.5 is an
  operational middle, labelled as such.
- `b` = **0.2** (bare hands open embedded food at a fifth of the normal rate). No direct anchor was found; FX1's nearest
  figure is that 10-year-olds extract at 10–15% of adult rates, which is about skill, not tools.

Because the totals are unchanged but half the food is now slower to take by hand, **the world is harsher until tools are
used**. That is the point of the design, but it means survival can fall for a reason that has nothing to do with
learning. So a second arm keeps the harshness without the tool route.

## Design (the assistant's recommendation; decisions marked)

| arm | setting | role |
|---|---|---|
| **C** | `code_v2` | reference |
| **E** | `embedded_share` 0.5, `b` 0.2, hard things help | the question |
| **E0** | as E, but hard things do not help (rate always `b`) | harshness alone, no tool route |

- **Seeds:** 256 new (a range unused by any study, fixed at freezing), 20 founders, 40 × 40, 120 years; 768 worlds, about
  30 hours on four workers, after MB1b and RT1b.
- **Primary 1 (tool use):** share of adult forage-weeks with a thing of hardness ≥ 40 in hand, **E against E0**, per world,
  paired by seed: Wilcoxon signed-rank; effect with a 95% bootstrap interval (10,000 resamples, `random.Random(2026)`).
  The question is whether people learn to use the tool route when it exists, at equal harshness.
- **Primary 2 (survival):** extinction, **E against C** and **E against E0**, paired by seed: exact sign test; bootstrap
  interval as above; yardstick ±0.117; Holm over all three primary tests.
- **Described** (population first, rule 18): median population at years 60 and 119; diet shares (open, embedded, crop,
  meat; by `../FX1_extracted_foods/acl_diet.py`'s measure); the hardest thing in hand while foraging, by decade; how
  often a hard thing is made, kept, given or copied; children's foraging returns against adults'.

## Checks (hard stops; no outcome shown if any fails)

1. **Zero:** `embedded_share` 0 equals `code_v2` exactly (state hash without the settings; seeds 11 and 501 for 5 years,
   501 and 601 for 20 years); E and E0 differ from C (they act); observers read-only; a saved and reloaded E world
   continues exactly; one fingerprint.
2. **Manipulation check:** in E and E0, embedded food is at least 25% of all plant food eaten in years 0–10 (people do
   meet it); and in E, bare-handed embedded foraging returns about `b` of open foraging (measured, within ±0.05).

## What it can and cannot show

It can show whether ACL's minds pick up tools when the land rewards them and nothing else changes. It cannot show that
this is how human tool use began, and `s` and `b` are not anchored to any measure of real land. A null result would be
informative: it would point at learning (people do not find the tool route), not at the land.

## The assistant's prior (to be frozen at sign-off; held loosely)

E against E0: **more tool use** in E, but small (E8.2 and the copying studies found that what one person discovers
rarely spreads). E against C: **more extinction** (the world is harsher, at least early). E against E0: **less
extinction**, only if tool use spreads.

## Decisions for the creator

1. Arms: **C, E and E0** (recommended), or only C and E.
2. Order: **after MB1b and RT1b** (recommended).
3. Numbers: **s 0.5, b 0.2, labelled operational** (recommended), or two levels of s (0.5 and 0.8; 256 more worlds).
4. Primary: **tool use (E vs E0) and extinction** (recommended), or extinction only.

## GPT's review under the creator's delegation (18 October 2026) — choices recorded, **not a sign-off**

GPT chose every recommended option. Its reply, verbatim (FX2 part):

> Arms: C, E, E0. Keep the control with equal harshness but no benefit from hard things.
>
> Order: After MB1b and RT1b.
>
> Numbers: Use 0.5 embedded food and 0.2 bare-hand opening rate, explicitly labelled operational assumptions. Don't add
> the 0.8 arm yet.
>
> Primary outcomes: Tool use (E vs E0) and extinction (E vs C; E vs E0), with Holm correction.
>
> Keep the interpretations narrow. FX2 tests whether processing costs can create pressure for tool use under these
> rules. It does not establish that this is how real human tool use evolved.

On sign-off GPT replied: "Keep both plans as drafts until Abdurashid reads them himself." It allowed writing the code and
running zero checks, with no freezing, tagging or study runs until the creator approves. **The plan stays a draft.**

## Details fixed while writing the code (before any run; for the creator to check at sign-off)

Choices the plan above did not spell out, made by the assistant in `code_fx2` and listed so none is hidden:

- **What people see:** their choice of where to forage, and the "richer than around it" judgement, count all plant food,
  open and embedded, as today's code counts all plants. They are not told embedded food is slow; they find out by what
  they get.
- **Which thing opens it:** the hardest thing in hand (hardness 0–100 read as 0–1); bare hands 0. Opening rate =
  `b + (1 − b) × hardness`. A thing that helped is felt as worth `rate − b` (the existing item judgement); it wears by one
  use, like the forage item.
- **Animals:** see and graze all plant food, taking from both stands in proportion, so hunting is left as it is.
- **Fire, flood and winter:** harm both stands alike. Dead people's food goes back to the open stand, as today.
- **Seeds:** embedded food yields seed like any wild food.
- **Saving:** the embedded stand is saved only when `embedded_share` > 0, so a share of 0 saves exactly what `code_v2`
  does.

## Prepared before sign-off (18 October 2026; GPT's direction; nothing frozen)

- **Code:** `code_fx2` = `code_v2` + `embedded_share`, `embedded_bare`, `embedded_tool` (details above); runner
  `run_fx2.py` (its `run` refuses while this plan is a draft).
- **Zero checks: all PASS** (`zero_fx2.log`; `output/zero.txt`): share 0 = `code_v2` (seeds 11, 501, 601); E and E0
  act; E differs from E0; observers read-only; a saved and reloaded E world continues exactly. Fingerprint `a1780037…`.
- **Mechanism** (`mech_fx2.log`; throwaway seeds 9901–9904, years 0–10; only the mechanism was read, no survival,
  population, deaths or tool use): embedded food was **0.357** (E) and **0.316** (E0) of adults' foraged food (check ≥
  0.25); bare hands got **0.200** per unit wanted in both (check 0.20 ± 0.05).

## Sign-off (18 October 2026)

The creator: "**approve FX2 as is, freeze it**", with these notes (pasted by the creator, verbatim):

> Make sure the tool-use measure is interpreted carefully:
>
> * E vs E0: Does making hard things useful increase tool use?
> * E vs C: What happens to survival when food becomes harder to access but tools can help?
> * E vs E0: Does enabling the tool benefit change survival under the embedded-food condition?
>
> Also, tool use alone doesn't prove that agents discovered the food-opening mechanism. If the existing logs allow it,
> report whether hard things are actually used on embedded food, not merely held during foraging.
> Keep the 0.5 and 0.2 settings labelled as operational assumptions. Don't add another arm right now.

So: arms **C, E, E0**; `embedded_share` 0.5 and `embedded_bare` 0.2, **operational assumptions**; primary as written
(tool use E vs E0; extinction E vs C and E vs E0; Holm over the three), each read only as the question above beside it.
**Seeds: 6001–6256** (256 new, unused by any study; fixed now), 20 founders, 40 × 40, 120 years; after RT1b.

**Added, described (not primary; the logs allow it):** the code records each opening of embedded food with the hardness
of the thing used (`open_food` events). Reported per arm: the share of embedded food opened with a hard thing (hardness
> 0, and ≥ 0.4), and the share of adult forage-weeks in which a hard thing was actually used on embedded food, beside
the primary measure (held while foraging). Holding is not taken as proof of discovery.

The code and zero checks were prepared before this sign-off (recorded above; fingerprint `a1780037…`). The study runner
and analysis are written next, before any study data.
