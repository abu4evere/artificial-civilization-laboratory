"""code_vw1 = code_v16 + VW1's law (`want_down`; 0 = v16): what a valued whole needs is wanted. Value flows down the
recipe tree through recipes the person knows (0.8 a step), into both the make rule and the gather rule.

  python experiments/VW1_value_of_wholes/patch_vw1.py <acl folder>      # patches config.py and mind.py (CRLF kept)
"""
import sys
from pathlib import Path


def patch(p, reps):
    s = p.read_bytes().decode("utf-8")
    crlf = "\r\n" in s
    s = s.replace("\r\n", "\n")
    for old, new in reps:
        assert s.count(old) == 1, (p, old[:70])
        s = s.replace(old, new)
    p.write_bytes((s.replace("\n", "\r\n") if crlf else s).encode("utf-8"))


root = Path(sys.argv[1])
patch(root / "config.py", [(
    "    fix_affordable_target: int = 1 ",
    "    want_down: int = 0                 # VW1: 1 = what a valued whole needs is wanted: value flows down the recipe tree\n"
    "                                       # through recipes the person knows (0.8 a step) into the make and gather rules\n"
    "    fix_affordable_target: int = 1 ")])
patch(root / "mind.py", [
    ('''def _wanted_parts(p: Person) -> dict:
    """Made things that go into something they value and do not have: worth making for that."""
    out: dict = {}
    for sig, recipe in p.recipes.items():
        v = p.itemval.get(sig, 0.0)
        if v <= 0 or _holding(p, sig):
            continue
        parts = list(recipe.get("parts", ())) + ([recipe["part"]] if recipe["verb"] == "heat" else [])
        for part in parts:
            if part not in MATERIALS and not _holding(p, part, worn_ok=True):
                out[part] = max(out.get(part, 0.0), 0.8 * v)
    return out
''',
     '''def _wanted_parts(p: Person, deep: int = 0) -> dict:
    """Made things that go into something they value and do not have: worth making for that.
    VW1 (deep): the want flows on down, through the recipes they know, to the parts of those parts (0.8 a step)."""
    out: dict = {}
    for sig, recipe in p.recipes.items():
        v = p.itemval.get(sig, 0.0)
        if v <= 0 or _holding(p, sig):
            continue
        parts = list(recipe.get("parts", ())) + ([recipe["part"]] if recipe["verb"] == "heat" else [])
        for part in parts:
            if part not in MATERIALS and not _holding(p, part, worn_ok=True):
                out[part] = max(out.get(part, 0.0), 0.8 * v)
    if deep:
        frontier = list(out.items())
        while frontier:
            part, v = frontier.pop()
            if v < out.get(part, 0.0):
                continue
            recipe = p.recipes.get(part)
            if recipe is None:
                continue
            subs = list(recipe.get("parts", ())) + ([recipe["part"]] if recipe["verb"] == "heat" else [])
            for sub in subs:
                if sub in MATERIALS or _holding(p, sub, worn_ok=True):
                    continue
                nv = 0.8 * v
                if nv >= 0.01 and nv > out.get(sub, 0.0):
                    out[sub] = nv
                    frontier.append((sub, nv))
    return out
'''),
    ('''def _material_wants(p: Person, season: int) -> dict:
    """How much each material is wanted for the things p knows how to make, or likes to leave places."""
    want = {k: 0.0 for k in GATHERABLE}
    for sig, recipe in p.recipes.items():
        v = p.itemval.get(sig, 0.0)
        if v <= 0 or _holding(p, sig):
            continue
        for kind in recipe_materials(recipe):
            if kind in want and p.mats.get(kind, 0.0) < 1.0:
                want[kind] = max(want[kind], v)
''',
     '''def _material_wants(p: Person, season: int, deep: int = 0) -> dict:
    """How much each material is wanted for the things p knows how to make, or likes to leave places."""
    want = {k: 0.0 for k in GATHERABLE}
    for sig, recipe in p.recipes.items():
        v = p.itemval.get(sig, 0.0)
        if v <= 0 or _holding(p, sig):
            continue
        for kind in recipe_materials(recipe):
            if kind in want and p.mats.get(kind, 0.0) < 1.0:
                want[kind] = max(want[kind], v)
    if deep:                    # VW1: what the wanted parts are made of is wanted too
        for sig, v in _wanted_parts(p, deep).items():
            recipe = p.recipes.get(sig)
            if recipe is None or _holding(p, sig):
                continue
            for kind in recipe_materials(recipe):
                if kind in want and p.mats.get(kind, 0.0) < 1.0:
                    want[kind] = max(want[kind], v)
'''),
    ('''            want = _material_wants(p, season)''', '''            want = _material_wants(p, season, c.want_down)'''),
    ('''        part_of = _wanted_parts(p)''', '''        part_of = _wanted_parts(p, c.want_down)'''),
])
print("patched", root)
