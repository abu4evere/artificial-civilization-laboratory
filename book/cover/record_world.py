"""Record a real ACL world for the cover: its map, every tile people stood on (week by week, 120 years), and where the
living are at the end. Control code, A2-full, seed 515 (a world that survives; F1).

    python book/cover/record_world.py      -> book/cover/world_515.json
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "experiments" / "E13R_replication" / "code_e13r"))
from acl.config import Config  # noqa: E402
from acl.world import World  # noqa: E402

SEED, YEARS = 515, 120
w = World(Config(seed=SEED, anticipation_weight=1.0))
tiles = [[{"b": t.biome, "h": round(t.height, 3), "f": round(t.fertility, 3)} for t in row] for row in w.tiles]
steps = {}
for _ in range(YEARS * 52):
    w.step()
    for p in w.living():
        k = f"{p.loc[0]},{p.loc[1]}"
        steps[k] = steps.get(k, 0) + 1
out = {"seed": SEED, "years": YEARS, "width": w.cfg.width, "height": w.cfg.height, "tiles": tiles, "steps": steps,
       "living": [list(p.loc) for p in w.living()]}
(HERE / f"world_{SEED}.json").write_text(json.dumps(out), encoding="utf-8")
print(f"living {len(out['living'])}, tiles walked {len(steps)}")
