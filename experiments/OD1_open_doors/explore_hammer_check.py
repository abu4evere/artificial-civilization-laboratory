"""A diagnostic after OD1's zero check failed (not data): in the unit check's world, when a made hammer is gone after a
strike, where did it go? Prints each case: still held, set on the ground this week, or gone.

  python experiments/OD1_open_doors/explore_hammer_check.py
"""
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import run_od1 as R  # noqa: E402

w = R.make(701, "o")
from acl import actions  # noqa: E402
from acl.matter import MATERIALS  # noqa: E402

cases = Counter()
craft0 = actions._craft


def craft(world, p, recipe):
    tool = recipe.get("tool") if recipe["verb"] == "strike" else None
    obj = next((it for it in p.items if tool and tool not in MATERIALS and it["sig"] == tool), None)
    n_before = len(p.items)
    cap = __import__("acl.matter", fromlist=["item_cap"]).item_cap(world, p)
    g0 = len(world.ground)
    item = craft0(world, p, recipe)
    if obj is not None:
        held = any(it is obj for it in p.items)
        on_ground = any(g["item"] is obj for g in world.ground[g0:])
        if not held:
            cases["gone_on_ground" if on_ground else "gone_elsewhere"] += 1
            print(json.dumps({"tick": world.tick, "who": p.id, "tool": tool, "made": item and item["sig"],
                              "items_before": n_before, "cap_before": cap, "items_after": len(p.items),
                              "on_ground": on_ground, "tool_uses": obj["uses"]}))
        else:
            cases["kept"] += 1
    return item


actions._craft = craft
for _ in range(30 * R.WPY):
    w.step()
print(dict(cases))
