"""SC1 exploratory check (not part of the frozen plan): are kinds invented after year 100 ever made again?
Replays world 22001 (live v11, no observer but this one, read-only) to year 130 and records every make event:
the kind's first-made year in the world register, and whether the maker invented it.

  python experiments/SC1_bob_scorecard/explore/check_remakes.py
"""
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "ES2_realized_lookahead"))
import run_es2 as base  # noqa: E402

base.setup("v11")
w = base.make_world(22001, base.LP)
by_first = Counter()
late_new = Counter()


def obs(world, events):
    for ev in events:
        if ev["k"] == "make" and world.tick - 1 >= 100 * 52:
            rec = world.knowledge.get(ev.get("thing"))
            fy = rec["first_tick"] // 52 if rec else -1
            by_first["first made before year 100" if fy < 100 else "first made in year 100+"] += 1
            if fy >= 100:
                late_new[ev.get("thing")] += 1


w.observers.append(obs)
for _ in range(130 * 52):
    w.step()
out = {"makes_years_100_130_by_kind_age": dict(by_first), "late_kinds_remade": len(late_new),
       "late_kinds_registered": sum(1 for r in w.knowledge.values() if r["first_tick"] >= 100 * 52)}
(HERE / "check_remakes.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
print(json.dumps(out))
