# MT1 draft: made things that strike and bind by their properties (2 November 2026)

**What this is:** a draft for council round 53, to be sent once AF1's result is known. Nothing is frozen and nothing
is run. It is the next step in `docs/rules_review_2026-11-02.md` (section C, item 4) and
`docs/affordance_audit_2026-11-02.md`.

## The restriction (v11, read from the code)
- **Striking:** both the struck thing and the hammer must be raw materials.
  - In `actions._play`, the hammer comes from `HARD` = stone, flint and bone.
  - `matter.strike` reads both from the raw table.
  - **The result:** a person holding a heavy made thing (hard ≥ 50) cannot use it as a hammer.
- **Binding:** the binder must be a raw material from `matter.FLEXIBLE` = fiber and hide (flex ≥ 50).
  - `matter.bind` reads the binder from the raw table.
  - **The result:** a made cord (fiber bound to fiber has flex 90) can never tie anything.
- **Why it matters:** nothing in the physics says only raw things are hard or flexible. The world already gives every
  made thing the same ten properties as a material. These two lists stop made things from entering the two joining
  verbs, so whole branches of possible things can never be made.

## The two rules (general laws by property; neither names an invention)
- **H, "anything hard strikes"** (setting `made_hammers`).
  - The hammer may be any held thing, raw or made, whose `hard` ≥ 50. That is the threshold the raw hammers already
    meet: bone 50, flint 70, stone 80.
  - The force comes from the hammer's own `hard`, as now.
  - A made hammer is not used up, as a raw one is not, but it wears one use, as a tool in any other use does.
  - The struck thing stays raw, because flaking depends on a material's brittleness, which made things do not have.
- **B, "anything flexible binds"** (setting `made_binders`).
  - The binder may be any held thing, raw or made, whose `flex` ≥ 50: the same threshold that defines `FLEXIBLE` now.
  - Its properties (contain, warm, tight, fuel) enter `bind` exactly as a raw binder's do.
  - It is used up, as a raw binder is.
- **Where they act:** in play (the things tried), in `make` (`can_make` and the craft), and in recipes, where a made
  hammer or binder is named by its kind.
- **What does not change:** teaching errors still swap among raw hammers and binders, because a mistaken lesson names
  something common.

## Proposed design
- **Arms:** v11 (or v12 if FX1 is adopted), H, B, H+B and the sham; 32 new paired seeds; LP worlds; 200 years; years
  100–200.
- **Primary (not true by definition):** tools' share of adults' foraged food in years 100–200. This is TR1's measure:
  the food added by the best tool in hand, as a share of the food foraged.
  - **Why:** more combinations will mechanically raise the number and depth of kinds. The question for Bob is whether
    the new possibilities make people's culture **better** (cumulative benefit), not just bigger.
- **Secondary, described:**
  - kinds per adult-year;
  - nesting depth of kinds alive at year 200;
  - AF1's lineage remaking R;
  - recipe availability;
  - how often made hammers and binders are used.
- **Rule:** GPT's, as in WP1 and AF1 (arm − v11 and arm − sham both above 0, both points at least a minimum). The
  minimum is to be set from TR1's spread before data.
- **Guards:** population and extinctions, as in AF1.

## Questions for round 53
1. Are H and B general laws, not scripted outcomes? Are the thresholds (`hard` ≥ 50, `flex` ≥ 50) right, taken from
   the existing raw lists?
2. Is tools' share of foraged food the right primary? Or should it be AF1's remaking R, or something else?
3. Should MT1 run on v11, or wait for v12 (FX1)? Should it build on AF1's S and K if either is positive?
