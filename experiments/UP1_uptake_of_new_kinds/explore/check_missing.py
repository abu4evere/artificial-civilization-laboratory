"""UP1 follow-up, exploratory (not part of any frozen plan): when a new nested kind "cannot be made", what is missing?
Replays world 22101 (live v11; read-only wrappers) to year 130. At every adult decision, for each nested kind invented in
play from year 100 that the person knows, is not holding (as the code skips) and values above 0.05, but cannot make:
  raw        only raw materials (or the binder) are missing
  unknown    a made part is missing and the person does not know that part's recipe
  stuck      a made part is missing; its recipe is known but cannot be made now either
  bridge     a made part is missing; its recipe is known and could be made now (the wanted-part bridge could act)
and, for "bridge", whether that part was the person's make option this week.

  python experiments/UP1_uptake_of_new_kinds/explore/check_missing.py
"""
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "ES2_realized_lookahead"))
import run_es2 as base  # noqa: E402

base.setup("v11")
from acl import knowhow, thought  # noqa: E402
from acl.matter import MATERIALS  # noqa: E402

w = base.make_world(22101, base.LP)
START, END = 100 * 52, 130 * 52
played = set()
out = Counter()
o_rem, o_steer = knowhow.remember_recipe, thought.steer


def remember_recipe(world, p, sig, recipe, how, source=None, props=None, meant=None):
    new = sig not in world.knowledge
    r = o_rem(world, p, sig, recipe, how, source, props, meant)
    if new and how == "made" and world.tick >= START:
        played.add(sig)
    return r


def made_parts(recipe):
    if recipe.get("verb") == "bind":
        return [x for x in recipe["parts"] if x not in MATERIALS]
    if recipe.get("verb") == "heat" and recipe["part"] not in MATERIALS:
        return [recipe["part"]]
    return []


def steer(p, options):
    res = o_steer(p, options)
    world = w
    if not (START <= world.tick < END) or w.people.get(p.id) is not p or p.age(world.tick) < 16 * 52:
        return res
    from acl.mind import _holding, _wanted_parts, can_make
    make_t = next((o[2] for o in res if o[1] == "make"), None)
    part_of = _wanted_parts(p)
    for sig, recipe in p.recipes.items():
        if sig not in played:
            continue
        parts = made_parts(recipe)
        if not parts:
            continue
        v = max(p.itemval.get(sig, 0.0), part_of.get(sig, 0.0))
        if (_holding(p, sig) and v == p.itemval.get(sig, 0.0)) or v <= 0.05:
            continue
        heat_blocked = recipe["verb"] == "heat" and world.tile(p.loc).fire <= 0
        if not heat_blocked and can_make(p, recipe):
            continue
        missing = [x for x in parts if sum(1 for it in p.items if it["sig"] == x) < parts.count(x)]
        if not missing:
            out["raw"] += 1
            continue
        cls = "stuck"
        for x in missing:
            if x not in p.recipes:
                cls = "unknown"
                break
            if can_make(p, p.recipes[x]):
                cls = "bridge"
                out["bridge_part_is_make_option" if make_t == x else "bridge_part_not_make_option"] += 1
                break
        out[cls] += 1
        out["items_full"] += len(p.items) >= world.cfg.item_limit
    return res


knowhow.remember_recipe, thought.steer = remember_recipe, steer
for _ in range(END):
    w.step()
res = {"cases": dict(out), "new_kinds_played": len(played)}
(HERE / "check_missing.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
print(json.dumps(res))
