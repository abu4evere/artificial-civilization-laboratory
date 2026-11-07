"""PLAY1 side look (NOT a study, NOT data): in the play world as it stands, for every living person and every recipe they
know that someone else invented, what stands between them and making it? Read-only on state/world.json.

  python experiments/PLAY1_inside_acl/explore_making.py
"""
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "NV15_nature_v15" / "code_v15"))
from acl import mind  # noqa: E402
from acl.world import World  # noqa: E402

w = World.from_dict(json.loads((HERE / "state" / "world.json").read_text(encoding="utf-8")))
why = Counter()
people = Counter()
for p in w.living():
    part_of = mind._wanted_parts(p)
    for sig, recipe in p.recipes.items():
        k = w.knowledge.get(sig, {})
        own = k.get("first_by") == p.id
        key = "own" if own else "others'"
        people[key] += 1
        v = max(p.itemval.get(sig, 0.0), part_of.get(sig, 0.0))
        if mind.can_make(p, recipe):
            r = "can make now" + (" (valued)" if v > 0.05 else " (but valued <= 0.05)")
        elif recipe["verb"] in ("fill",):
            r = "fill (never a make)"
        else:
            made = [x for x in recipe.get("parts", ()) if x not in p.mats and x not in mind.MATERIALS] \
                if recipe["verb"] not in ("shape", "heat", "strike") else []
            missing_made = [x for x in made if not any(it["sig"] == x for it in p.items)]
            if missing_made:
                r = "a made part not in hand" + (" (valued)" if v > 0.05 else " (and valued <= 0.05)")
            else:
                r = "a raw material short" + (" (valued)" if v > 0.05 else " (and valued <= 0.05)")
        why[(key, r)] += 1
print(f"week {w.tick}; living {len(w.living())}; known recipes: {dict(people)}")
for (key, r), n in sorted(why.items()):
    print(f"  {key:8s} {r}: {n}")
