"""code_od1 = code_v16 + OD1's five doors (questions.md, frozen as `OD1-frozen`); each switch 0 = v16 exactly.
  D1 similar_parts     AF1's S, unchanged: a held thing within 10 in all 10 properties may stand in for an input
  D2 containers_carry  AF1's K, unchanged: the carry factor also multiplies the made-thing and material limits
  D3 made_binders      a held made thing with flex >= 50 can bind (used up), its own properties entering bind()
  D4 made_hammers      a held made thing with hard >= 50 can be the hammer (not used up), its own hard setting the force
  D5 layers_add        warmth worn and carrying combine by matter._layer's law (best fully, each next half), capped at 100

  python experiments/OD1_open_doors/patch_od1.py <acl folder>      # patches the copy in place (line endings kept)
"""
import sys
from pathlib import Path

HERE = Path(__file__).parent


def patch(p, reps):
    s = p.read_bytes().decode("utf-8")
    crlf = "\r\n" in s
    s = s.replace("\r\n", "\n")
    for old, new in reps:
        assert s.count(old) == 1, (p.name, old[:80])
        s = s.replace(old, new)
    p.write_bytes((s.replace("\n", "\r\n") if crlf else s).encode("utf-8"))


root = Path(sys.argv[1])

patch(root / "config.py", [(
    "    fix_affordable_target: int = 1 ",
    "    similar_parts: int = 0             # OD1 (D1, AF1's S): 1 = when making a known thing, an input not held may be replaced\n"
    "                                       # by a held thing whose 10 properties are each within 10 of the original's\n"
    "    containers_carry: int = 0          # OD1 (D2, AF1's K): 1 = the best container's carry factor also multiplies the\n"
    "                                       # made-thing and material limits, as it multiplies the food limit\n"
    "    made_binders: int = 0              # OD1 (D3): 1 = a held made thing with flex >= 50 can bind, as raw fiber and hide do\n"
    "    made_hammers: int = 0              # OD1 (D4): 1 = a held made thing with hard >= 50 can be the hammer in striking\n"
    "    layers_add: int = 0                # OD1 (D5): 1 = for warmth worn and for carrying, several things combine by the law\n"
    "                                       # for joining coverings (the best fully, each next half), capped at 100\n"
    "    fix_affordable_target: int = 1 ")])

patch(root / "matter.py", [
    ('''def strike(target: str, hammer: str, skill: float, rng) -> dict | None:
    """Hit a raw material with another. Brittle things flake to an edge if the hammer is hard enough."""
    t, hm = raw_props(target), raw_props(hammer)
''',
     '''def strike(target: str, hammer: str, skill: float, rng, hammer_props: dict | None = None) -> dict | None:
    """Hit a raw material with another. Brittle things flake to an edge if the hammer is hard enough.
    OD1 (D4): the hammer may be a made thing; its own hardness sets the force."""
    t = raw_props(target)
    hm = hammer_props if hammer_props is not None else raw_props(hammer)
'''),
    ('''def sparks(target: str, hammer: str) -> bool:
    """Flint struck against something hard throws sparks."""
    return "flint" in (target, hammer) and min(RAW[target][2], RAW[hammer][2]) >= 50
''',
     '''def sparks(target: str, hammer: str, hammer_props: dict | None = None) -> bool:
    """Flint struck against something hard throws sparks. OD1 (D4): a made hammer's hardness is its own."""
    hh = hammer_props["hard"] if hammer_props is not None else RAW[hammer][2]
    return "flint" in (target, hammer) and min(RAW[target][2], hh) >= 50
'''),
    ('''def bind(a: dict, b: dict, binder: str) -> dict:
    """Tie two things together with something flexible."""
    bd = raw_props(binder)
''',
     '''def bind(a: dict, b: dict, binder: str, binder_props: dict | None = None) -> dict:
    """Tie two things together with something flexible. OD1 (D3): the binder may be a made thing; its own properties
    enter where a raw binder's do."""
    bd = binder_props if binder_props is not None else raw_props(binder)
'''),
    ('''    over = min(amount, max(0.0, p.mat_total() + amount - world.cfg.material_limit))''',
     '''    over = min(amount, max(0.0, p.mat_total() + amount - material_cap(world, p)))          # OD1 (D2)'''),
    ('''def carry_capacity(world, p) -> float:
    _, f = best_item(p, "carry")
    return world.cfg.carry_limit * f


def worn_warmth(p) -> float:
    """Share of cold kept out by what p wears."""
    _, f = best_item(p, "cold")
    return clamp(0.7 * (f - 1.0))
''',
     '''def layered(p, use: str) -> float:
    """OD1 (D5): what several things do together for warmth worn or for carrying, by the law for joining coverings
    (`_layer`, as `bind` uses it): the best counts fully, each next one half, in order from the best down; capped at 100
    on the property scale (1.0 here), as `bind` caps it."""
    v = 0.0
    for e in sorted((factor(it, use) - 1.0 for it in p.items), reverse=True):
        if e <= 0:
            break
        v = min(1.0, max(v, e) + min(v, e) / 2)
    return 1.0 + v


def use_factor(world, p, use: str) -> float:
    """How much p's things help with this use: the single best thing (v16), or for warmth worn and carrying the layered
    whole (OD1, D5)."""
    if world is not None and world.cfg.layers_add and use in ("carry", "cold"):
        return layered(p, use)
    return best_item(p, use)[1]


def carry_capacity(world, p) -> float:
    return world.cfg.carry_limit * use_factor(world, p, "carry")


def item_cap(world, p) -> int:
    """How many made things p can carry. OD1 (D2, AF1's K): multiplied by the carry factor, as food is; the container
    counts toward its own limit."""
    if not world.cfg.containers_carry:
        return world.cfg.item_limit
    return int(world.cfg.item_limit * use_factor(world, p, "carry"))


def material_cap(world, p) -> float:
    """How much raw material p can carry. OD1 (D2, AF1's K): multiplied by the carry factor."""
    if not world.cfg.containers_carry:
        return world.cfg.material_limit
    return world.cfg.material_limit * use_factor(world, p, "carry")


def worn_warmth(p, world=None) -> float:
    """Share of cold kept out by what p wears."""
    return clamp(0.7 * (use_factor(world, p, "cold") - 1.0))
'''),
])

patch(root / "biology.py", [
    ('''from .matter import best_item, pile_room, pile_shape, pile_warmth, worn_warmth''',
     '''from .matter import best_item, factor, pile_room, pile_shape, pile_warmth, worn_warmth'''),
    ('''            worn = worn_warmth(p)
''', '''            worn = worn_warmth(p, world)
'''),
    ('''                if worn > 0:
                    idx, _ = best_item(p, "cold")
                    knowhow.judge_item(world, p, p.items[idx]["sig"], worn)
                    p.items[idx]["uses"] -= 1
                    if p.items[idx]["uses"] <= 0:
                        p.items.pop(idx)
''',
     '''                if worn > 0:
                    idx, _ = best_item(p, "cold")
                    knowhow.judge_item(world, p, p.items[idx]["sig"], worn)
                    layers = [idx]
                    if c.layers_add:                    # OD1 (D5): every layer that keeps out cold wears
                        layers += [i for i, it in enumerate(p.items) if i != idx and factor(it, "cold") > 1.0]
                    for i in sorted(layers, reverse=True):
                        p.items[i]["uses"] -= 1
                        if p.items[i]["uses"] <= 0:
                            p.items.pop(i)
'''),
    ('''        while len(heir.items) > world.cfg.item_limit:''',
     '''        while len(heir.items) > matter.item_cap(world, heir):          # OD1 (D2)'''),
    ('''                while len(q.items) > world.cfg.item_limit:''',
     '''                while len(q.items) > matter.item_cap(world, q):          # OD1 (D2)'''),
])

patch(root / "actions.py", [
    ('''    got = min(tile.material(kind), rate, max(0.0, c.material_limit - p.mat_total()))''',
     '''    got = min(tile.material(kind), rate, max(0.0, matter.material_cap(world, p) - p.mat_total()))   # OD1 (D2)'''),
    ('''    item = _craft(world, p, recipe)
    if item is not None:
        p.reward += 0.1
''',
     '''    from .mind import resolve_recipe
    item = _craft(world, p, resolve_recipe(world, p, recipe) or recipe)          # OD1 (D1): stand-in inputs
    if item is not None:
        p.reward += 0.1
'''),
    ('''        p.mats[recipe["target"]] -= 1.0
        item = matter.strike(recipe["target"], recipe["tool"], p.skills["crafting"], rng)
''',
     '''        p.mats[recipe["target"]] -= 1.0
        hp = None
        if recipe["tool"] not in MATERIALS:             # OD1 (D4): a made hammer, not used up
            hp = next(it for it in p.items if it["sig"] == recipe["tool"])
        item = matter.strike(recipe["target"], recipe["tool"], p.skills["crafting"], rng, hp)
'''),
    ('''        if matter.sparks(recipe["target"], recipe["tool"]):''',
     '''        if matter.sparks(recipe["target"], recipe["tool"], hp):'''),
    ('''        p.mats[recipe["binder"]] -= 1.0
        item = matter.bind(parts[0], parts[1], recipe["binder"])
''',
     '''        bp = None
        if recipe["binder"] in MATERIALS:
            p.mats[recipe["binder"]] -= 1.0
        else:                                           # OD1 (D3): a made binder, used up
            bp = p.items.pop(next(i for i, it in enumerate(p.items) if it["sig"] == recipe["binder"]))
        item = matter.bind(parts[0], parts[1], recipe["binder"], bp)
'''),
    ('''def _keep(p: Person, item: dict, limit: int, world=None) -> None:
    p.items.append(item)
''',
     '''def _keep(p: Person, item: dict, limit: int, world=None) -> None:
    p.items.append(item)
    if world is not None:
        limit = matter.item_cap(world, p)          # OD1 (D2); = the given limit in v16
'''),
    ('''    first, until full. Things on the ground neither rot nor wear (as tools on a body). Draws nothing at random."""
    if not world.ground:
        return
    from .config import CHILD_END
    tick = world.tick
    limit = world.cfg.item_limit
''',
     '''    first, until full. Things on the ground neither rot nor wear (as tools on a body). Draws nothing at random."""
    if world.cfg.containers_carry:                  # OD1 (D2): over the limit (a container lost), the least valued go down
        for q in sorted(world.living(), key=lambda q: q.id):
            while len(q.items) > matter.item_cap(world, q):
                worst = min(range(len(q.items)), key=lambda i: (q.itemval.get(q.items[i]["sig"], 0.0), -i))
                drop_on_ground(world, q, q.items.pop(worst))
    if not world.ground:
        return
    from .config import CHILD_END
    tick = world.tick
'''),
    ('''        while len(p.items) < limit:
            left = [g for g in lying if id(g) not in taken]''',
     '''        while len(p.items) < matter.item_cap(world, p):          # OD1 (D2); = item_limit in v16
            left = [g for g in lying if id(g) not in taken]'''),
    ('''    if not p.items or len(q.items) >= world.cfg.item_limit:''',
     '''    if not p.items or len(q.items) >= matter.item_cap(world, q):          # OD1 (D2)'''),
    ('''            for h in HARD:
                if p.mats[h] >= (2.0 if h == t else 1.0):
                    choices.append({"verb": "strike", "target": t, "tool": h})
''',
     '''            for h in HARD:
                if p.mats[h] >= (2.0 if h == t else 1.0):
                    choices.append({"verb": "strike", "target": t, "tool": h})
            if world.cfg.made_hammers:                  # OD1 (D4): a held made thing hard enough to strike with
                for h in sorted({it["sig"] for it in p.items if it["hard"] >= 50}):
                    choices.append({"verb": "strike", "target": t, "tool": h})
'''),
    ('''    binders = [b for b in matter.FLEXIBLE if p.mats[b] >= 1.0]
''',
     '''    binders = [b for b in matter.FLEXIBLE if p.mats[b] >= 1.0]
    if world.cfg.made_binders:                      # OD1 (D3): a held made thing flexible enough to tie with
        binders += sorted({it["sig"] for it in p.items if it["flex"] >= 50})
'''),
])

af1 = (HERE.parent / "AF1_open_affordances" / "code_af1" / "acl" / "mind.py").read_bytes().decode("utf-8").replace("\r\n", "\n")
similar = af1[af1.index("SIMILAR_D = 10"):af1.index("def _holding(p: Person")]
similar = similar.replace("AF1 (S)", "OD1 (D1, AF1's S)")
patch(root / "mind.py", [
    ('''from .matter import MATERIALS, SOFT_WHEN_WET, best_holder, best_item, holding''',
     '''from .matter import MATERIALS, PROPS, SOFT_WHEN_WET, best_holder, best_item, holding, item_cap, material_cap, raw_props'''),
    ('''        if p.mat_total() < c.material_limit:''',
     '''        if p.mat_total() < material_cap(world, p):          # OD1 (D2)'''),
    ('''or not can_make(p, recipe):
                continue
            cands.append(''',
     '''or resolve_recipe(world, p, recipe) is None:     # OD1 (D1)
                continue
            cands.append('''),
    ('''            if p.items and len(q.items) < c.item_limit:''',
     '''            if p.items and len(q.items) < item_cap(world, q):          # OD1 (D2)'''),
    ('''        parts = list(recipe.get("parts", ())) + ([recipe["part"]] if recipe["verb"] == "heat" else [])
        for part in parts:
            if part not in MATERIALS and not _holding(p, part, worn_ok=True):''',
     '''        parts = list(recipe.get("parts", ())) + ([recipe["part"]] if recipe["verb"] == "heat" else [])
        parts += [x for x in (recipe.get("binder"), recipe.get("tool")) if x and x not in MATERIALS]   # OD1 (D3, D4)
        for part in parts:
            if part not in MATERIALS and not _holding(p, part, worn_ok=True):'''),
    ('''    if recipe["verb"] == "strike":
        return [recipe["target"], recipe["tool"]]
''',
     '''    if recipe["verb"] == "strike":
        return [recipe["target"]] + ([recipe["tool"]] if recipe["tool"] in MATERIALS else [])     # OD1 (D4)
'''),
    ('''    out = [part for part in recipe["parts"] if part in MATERIALS]
    out.append(recipe["binder"])
    return out
''',
     '''    out = [part for part in recipe["parts"] if part in MATERIALS]
    if recipe["binder"] in MATERIALS:                    # OD1 (D3): a made binder is not a material
        out.append(recipe["binder"])
    return out
'''),
    ('''        if recipe["tool"] != recipe["target"]:
            need[recipe["tool"]] = 1
''',
     '''        if recipe["tool"] != recipe["target"]:
            need[recipe["tool"]] = 1
        if recipe["tool"] not in MATERIALS:             # OD1 (D4): a made hammer in hand; the target stays raw
            if recipe["target"] not in MATERIALS or not any(it["sig"] == recipe["tool"] for it in p.items):
                return False
            need = {recipe["target"]: 1}
'''),
    ('''        need[recipe["binder"]] = need.get(recipe["binder"], 0) + 1
    return all(''',
     '''        if recipe["binder"] in MATERIALS:
            need[recipe["binder"]] = need.get(recipe["binder"], 0) + 1
        elif sum(1 for it in p.items if it["sig"] == recipe["binder"]) < made.get(recipe["binder"], 0) + 1:
            return False                                # OD1 (D3): a made binder in hand, besides the parts
    return all('''),
    ('''def _holding(p: Person, sig: str, worn_ok: bool = False) -> bool:''',
     similar + '''def _holding(p: Person, sig: str, worn_ok: bool = False) -> bool:'''),
])

patch(root / "knowhow.py", [
    ('''    parts = list(recipe.get("parts", ())) + ([recipe["part"]] if recipe.get("verb") == "heat" else [])
    for part in parts:
        if part not in MATERIALS and part not in learner.recipes:''',
     '''    parts = list(recipe.get("parts", ())) + ([recipe["part"]] if recipe.get("verb") == "heat" else [])
    parts += [x for x in (recipe.get("binder"), recipe.get("tool")) if x and x not in MATERIALS]   # OD1 (D3, D4)
    for part in parts:
        if part not in MATERIALS and part not in learner.recipes:'''),
])

patch(root / "information.py", [
    ('''        elif out["target"] in HARD:
            out["target"], out["tool"] = out["tool"], out["target"]''',
     '''        elif out["target"] in HARD and out["tool"] in HARD:      # OD1 (D4): a made hammer is never a target
            out["target"], out["tool"] = out["tool"], out["target"]'''),
])
print("patched", root)
