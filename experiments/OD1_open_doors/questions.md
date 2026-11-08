# OD1: open the world's closed doors, once (frozen plan)

**A test of one package of general laws in a copy of nature v16, with a sham.** This is the creator's step 1 of the
Direction of 7 November 2026 (`CLAUDE.md`, "Direction"): open the closed doors once, then freeze the world until a
review on 7 December, then work almost only on Bob's brain.

- **The adoption bar, set by the creator** (7 November 2026, "yes go ahead"): the package goes live if this frozen test
  shows **no harm**, as for fault fixes, because the doors only open possibilities and push no outcome. No confirmatory
  run is needed for a no-harm reading.
- **Council round 80** (`docs/debate_round80_question_2026-11-07.md`, `docs/debate_round80_after_2026-11-07.md`):
  - GPT 75%, Gemini 80%, DeepSeek about 85%;
  - all three: no objection to the final design, after DeepSeek's cap point was taken (D5 below).
- **Sources:**
  - the affordance audit `docs/affordance_audit_2026-11-02.md`;
  - AF1 (`experiments/AF1_open_affordances/findings.md`): its S and K, on v11, were inconclusive and raised no guard.
- **The creator's principle:** "Don't build a world where intelligence is guaranteed to succeed. Build a mind capable of
  discovering how to succeed in the world it inherits." The doors give no tool, recipe or reward. They only stop the
  world from refusing what its own properties allow.

## The five doors (each a general law through the 10 properties; each 0 = v16 exactly)
The 10 properties are edge, reach, hard, contain, warm, float, tight, plastic, fuel and flex.

- **D1, similar parts** (`similar_parts`). This is AF1's S, unchanged.
  - When a person makes a thing they know, an input they do not hold may be replaced by something they hold whose 10
    properties are each within 10 of the original's.
  - The closest match is used first, in a fixed order with no chance involved. The remembered recipe never changes.
  - **The 10 is a chosen constant** (AF1's, never selected on outcomes), recorded as such (GPT, DeepSeek).
- **D2, containers carry** (`containers_carry`). This is AF1's K, unchanged.
  - The carry factor of the best container held (1 + contain/100, which already multiplies the food limit) also
    multiplies the made-thing limit (3) and the material limit (20).
  - Where things over the limit go, and the container counting toward its own limit, are as in AF1.
- **D3, made binders** (`made_binders`).
  - Any held made thing with flex ≥ 50 can bind, as raw fiber and hide do now. 50 is the existing threshold of
    `matter.FLEXIBLE`.
  - Its own properties enter `bind()` where a raw binder's do, and it is used up, like a raw binder.
- **D4, made hammers** (`made_hammers`).
  - Any held made thing with hard ≥ 50 can be the hammer in strike. 50 is bone's hardness, the softest raw hammer.
  - Its own hard sets the force through the existing strike formula. It is not used up, like a raw hammer.
  - The target stays a raw material.
- **D5, layers add, for warmth worn and carrying only** (`layers_add`). Tools of work and fighting still use the single
  best item.
  - Several items combine by the world's own law for joining coverings (`matter._layer`, as `bind` uses it): the bigger
    counts fully, the smaller half, in order from best down.
  - The result is **capped at 100 on the property scale, as `bind` caps it.** So carrying is at most doubled, also
    together with D2 (DeepSeek's point).

**Left out, with reasons:**
- **Heaps of made things:** a property-based shelter would need new coefficients.
- **Repair:** it needs a new wear constant.
- **Made shaping tools:** shaping is done by hand.
- **Already open in v16** (checked in the code):
  - a made thing held in a fire burns and feeds it (`actions._hold_in_fire`);
  - any made thing's edge counts in foraging, hunting, wood and fiber (`matter.factor`).

## Arms and seeds
- **c** v16;
- **o** doors (D1–D5);
- **p** doors without D1 (DeepSeek's split);
- **x** the sham, one extra draw from the world's generator in week one.

Seeds 25301–25332 (32 new paired seeds); LP; 200 years; years 100–200 counted. `code_od1` = `code_v16` + the five
switches.

## Frozen decision rule
- **The gate:** CI1's eight guards, exactly as in LW1, FF4 and VW1, each arm against v16. Paired world bootstrap, 10,000
  draws, NumPy seed 20261130. The sham is reported as a validity check (GPT).
- **What goes live:**
  - **o** goes live if it raises no guard;
  - if **o** raises a guard and **p** raises none, **p** goes live and D1 stays closed;
  - if both raise a guard, nothing goes live, and the world is frozen as v16.
- **The manipulation counts are reported first** (per door, per arm):
  - stand-ins used (D1);
  - person-weeks above the old item or material limit (D2);
  - made binders used (D3);
  - made hammers used (D4);
  - person-weeks where a second item adds warmth or carrying (D5).

  If they are near zero, the reading is **"no harm detected, doors barely exercised"**. The doors still go live under
  the creator's bar, labelled so. A pass means "no detected harm under the tested conditions", not "harmless" (GPT).

## Pre-registered descriptives (not gates)
- Killings and attacks by people holding a made thing with hard ≥ 50.
- The tool factor of things made with a stand-in, against things made from the original inputs.
- The spread of made things and materials carried (hoarding).
- Making per person; new kinds; MP1's stages B and C; remaking within 5 years.

## Validity (hard stops)
- **Zero checks:**
  - `code_od1` with all five at 0 = `code_v16` (20 and 60 years, world and random stream);
  - each door acts in a check world;
  - the observers are read-only;
  - reload is exact.
- **Unit checks** (an o world, 30 years), at sampled cases:
  - a stand-in is within 10 in all 10 properties;
  - a made binder has flex ≥ 50 and is used up;
  - a made hammer has hard ≥ 50 and is not used up;
  - layered values equal an independent computation and never pass 100;
  - limits equal 3 or 20 × the factor.
- **All 4 × 32 worlds** are present under one fingerprint.
- **A blind recompute** by GPT and Gemini of the guards and manipulation counts.

## The assistant's prior
- No guard raised: about 70%.
- The doors are used, but rarely (making is about once in 14 years per adult). "Doors barely exercised" is likely for
  D3 and D4.

## Sign-off (7 November 2026)
- The creator decided the direction, the package and its no-harm bar in this session.
- The design is the assistant's, after council round 80 (GPT, Gemini, DeepSeek: no objection).
- Frozen as `OD1-frozen` before any code or data.
