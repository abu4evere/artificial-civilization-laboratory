# A review of every rule of nature v11 (2 November 2026)

**Why:** the creator, 2 November 2026: "I give you permission to edit world rules. Take a look and check all rules. If
you find something fix it or add any new rules. From now on keep working without me".

**What it is:** a read-only reading of the live code (`acl/`).
- **Files read:** `config.py`, `matter.py`, `actions.py`, `mind.py`, `knowhow.py`, the teaching part of
  `information.py`, the body, learning and death parts of `biology.py`, and `World.step`.
- **Not yet read line by line:** `weather.py`, `fauna.py`, `geo.py`, `marks.py`, `social.py`, `thought.py`.
- **It goes with** the audits of what made things can do (`docs/affordance_audit_2026-11-02.md`) and of how free people
  are to act (`docs/action_audit_2026-11-02.md`).
- **It changes nothing.** Each fix below goes through council and a check before it reaches live nature.

## A. Faults: the code does not do what its own rule or comment says

### F1. The make choice compares two different scales (`mind.decide`, the "make again" loop)
- **The rule** ("Make again something that has proved its worth"):
  - every known recipe gets a value v;
  - its utility is u = k × v, with k = 2 × (0.6 + 0.4 × diligence) × (1 − 0.5 × hunger);
  - the option offered is the recipe with the highest u.
- **The code:** recipes are visited in the order they were learned. A recipe is skipped when `v <= best_u`. That
  compares its **unscaled** value v with the best so far's **scaled** utility u.
- **The effect:**
  - k ranges from 0.6 to 2.0 and is usually above 1 (1.6 for a fed person of middle diligence);
  - a recipe learned later needs a value k times the earlier best's to be considered, not merely a higher one;
  - **older recipes are favoured over newer ones,** the opposite of what a cumulative mind needs.
- **Measured:** UP1 counted the skip in 4.0% of old-kind make decisions (`experiments/UP1_uptake_of_new_kinds`).
- **The fix:**
  - skip only below the floor that the first comparison already applies (v ≤ 0.05);
  - then pick the highest u, as the comment says.

### F2. An heir's overflow is deleted, not left on the ground (`biology.die`)
- **What happens:** when someone dies with their partner or grown child on the same tile, that heir takes their made
  things. Things beyond the 3-thing limit are then **deleted** with `pop(0)`: the heir's own first-held thing, whatever
  its worth.
- **What v8 says:** OP1's law, live since v8, is that "a made thing pushed out by the carry limit is left on the ground
  (not deleted)". Everywhere else (`actions._keep`) the **least valued** thing goes.
- **The fix:** the least valued go down onto the ground, as in `_keep`.

### F3. Tools taken from a body push out the first-held thing (`biology.bodies_week`)
- **What happens:** they are left on the ground (OP1), but the thing chosen is the first held, not the least valued.
- **The fix:** the least valued, as in `_keep`.

### F4 (minor, noted; not fixed now). The material limit is not applied to hunting spoils or inheritance
- **What happens:** hide and bone from a kill, and materials inherited at a death, are added without the 20-unit
  material limit.
- **Why it waits:** fixing it would *reduce* what people can hold, against the creator's direction. It should wait for a
  measured count of how often it happens, and be weighed with K (containers carry), which raises the limit.

## B. Restrictions: rules that close possibilities without a physical reason
**Already in the audits:**
- strike, shape and the binder take raw materials only;
- 3 made things are carried, and a container multiplies only food;
- only raw materials can be set down or built with;
- one tool is used at a time;
- one action a week;
- targets are picked by formula;
- teaching is automatic.

**Found in this review:**
- **R1. A new recipe is the first thing forgotten** (`knowhow.remember_recipe`).
  - A person holds at most 12 recipes, and a fresh recipe starts at value 0.
  - So a person whose 12 recipes are all valued forgets a new invention the moment they make it.
  - SC1's addendum: 21% of new kinds in one world were dropped this way.
  - **Two general fixes:**
    - a recency law: what was just learned is not the first forgotten (the serial-position effect in human memory);
    - a larger capacity, anchored to evidence on how much know-how foragers hold.
- **R1 has a history:** MO1 (on v7) let a learned recipe enter memory with its value.
  - Retention at 52 weeks rose by +0.243 [0.220, 0.273].
  - Making did not change, and the manipulation check failed (0.837 < 0.90).
  - So recency alone is unlikely to unlock remaking. It is a realism fix, lower in the order than F1 and AF1.
- **R2. Small working memories** for other things:
  - 8 valued places;
  - 5 puzzles;
  - 4 springs;
  - 3 animal sightings;
  - 3 shores;
  - 40 placements;
  - 60 memories;
  - 16 marks.

  None is anchored to evidence. For now they are noted, not judged.
- **R3. The make choice offers a single recipe** (the best). Combined with the habit value for "make" as a whole, a
  person cannot weigh making one thing against making another as two options.

## C. The order of work (the assistant's proposal, for the council)
1. **FX1, the fault fixes F1–F3** in a copy (`code_fx1`, each switchable).
   - Zero checks: off = v11.
   - A harm check on 32 paired worlds against v11 and the sham: the population and extinction guards, plus a
     described effect on remaking.
   - If no guard is raised, adopt as **nature v12**. A fault fix restores what the rule says; it is not a new law, so
     it needs no confirmatory run.
2. **AF1** (running): S, make by what it does; K, containers contain. If supported, a confirmatory run on the newest
   nature.
3. **MR1, the memory recency law (R1),** a test in a copy.
4. **Made things as hammers and binders, and building and storing with made things** (the audit's next rules).
5. **Free targets, teaching as a choice, general verbs, goals across weeks** (`docs/action_audit_2026-11-02.md`).

## Appended (2 November 2026, 23:10): the files not read at first
- **Read since:** `social.py`, `thought.py`, `inquiry.py` and `weather.py`. No fault in the first three.
- **F5 (minor; found in `weather.drink`). A leaky container saves water walks.**
  - **The comment says:** "something that holds water saves some of the walking".
  - **The code:** it uses the best **carry** factor (`best_item(p, "carry")`, which depends on `contain` only). So a
    basket that cannot hold water (`tight` below 50, which `matter.can_hold` requires for water) cuts the daily walk
    to water in sight.
  - **The fix:** only a thing that can hold water (`can_hold(item, "water") > 0`) saves walking, by the same formula.
  - **The trade-off:** the effect is small (energy only), and fixing it removes a help some people now have. It is
    physics honesty, not a new limit. **It goes to the next fault-fix round (FX2)** with F4, after FX1's result.
- **Still not read line by line:** `fauna.py`, `geo.py`, `marks.py`, and the rest of `information.py`.
- **`fauna.py` (read in part, 23:10).** A predator that kills 3 rabbits from a herd of fewer than 3 leaves a negative
  count for the rest of that week, until the herd is removed. That week's total, which is used for the land's
  carrying cap, is off by at most a few animals. This is noted as trivial and is not fixed.
