"""E3, second pass: how infants are fed, week by week. Read-only.

Wraps biology.body_phase to note, just before each week's feeding and eating, what every infant's carer has,
needs and did, and just after, whether the infant went hungry. The wrapper calls the real body_phase unchanged;
the year-100 world is checked against the saved experiment as before.

Usage: python experiments/E3_births/feeding_probe.py e1|e2 101 102 ...
"""
from __future__ import annotations

import json
import sys
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent.parent
CODE = sys.argv[1]
sys.path.insert(0, str(HERE / "code_e1") if CODE == "e1" else str(ROOT))

from acl import biology  # noqa: E402
from acl.config import WEEKS_PER_YEAR, Config  # noqa: E402
from acl.historian import Historian  # noqa: E402
from acl.measure import Lab  # noqa: E402
from acl.runner import load_snapshot  # noqa: E402
from acl.util import distance  # noqa: E402
from acl.world import World  # noqa: E402

SAVED = ROOT / "experiments" / ("E1" if CODE == "e1" else "E2") / "output"
OUT = HERE / "output"
ORIGINAL = biology.body_phase


def make_wrapper(c: Counter):
    def body_phase(world):
        cfg, tick = world.cfg, world.tick
        got = Counter()
        gifts = Counter()
        for e in world.events:
            if e["k"] == "forage" and e.get("a"):
                got[e["a"]] += e.get("got", 0.0)
            if e["k"] in ("forage", "hunt") and e.get("a"):
                pass
            if e["k"] == "give" and e.get("b"):
                gifts[e["b"]] += e.get("amount", 0.0)
        before = []
        for p in world.living():
            if p.age(tick) >= WEEKS_PER_YEAR or not p.caregiver:
                continue
            carer = world.people.get(p.caregiver)
            if carer is None or not carer.alive:
                continue
            deps = world.dependents(carer.id)
            dep_need = sum(d.need(cfg, tick) for d in deps)
            own = carer.need(cfg, tick)
            mate = world.people.get(carer.partner) if carer.partner else None
            before.append((p, carer, carer.edible(), own, dep_need, len(deps), carer.last_action, got.get(carer.id, 0.0),
                           gifts.get(carer.id, 0.0),
                           distance(carer.loc, mate.loc, cfg.width, cfg.height) if mate and mate.alive else None,
                           mate.edible() if mate and mate.alive else None))
        ORIGINAL(world)
        for (p, carer, food, own, dep_need, ndeps, act, foraged, gift, mate_d, mate_food) in before:
            hungry = p.alive and p.starving > 0 or (not p.alive and p.death_cause == "starvation")
            tag = "hungry" if hungry else "fed"
            c[f"{tag}:weeks"] += 1
            c[f"{tag}:carer_food"] += food
            c[f"{tag}:carer_need_total"] += own + dep_need
            c[f"{tag}:short"] += 1 if food < own + dep_need else 0
            c[f"{tag}:deps"] += ndeps
            c[f"{tag}:act:{act}"] += 1
            c[f"{tag}:foraged"] += foraged
            c[f"{tag}:did_forage"] += 1 if act == "forage" else 0
            c[f"{tag}:gift"] += gift
            c[f"{tag}:got_gift"] += 1 if gift > 0 else 0
            c[f"{tag}:carer_is_mother"] += 1 if carer.id == p.mother else 0
            if mate_d is not None:
                c[f"{tag}:has_mate"] += 1
                c[f"{tag}:mate_near"] += 1 if mate_d <= 2 else 0
                c[f"{tag}:mate_food"] += mate_food
    return body_phase


def run(seed, years=100):
    c = Counter()
    biology.body_phase = make_wrapper(c)
    try:
        w = World(Config(seed=seed))
        h = Historian()
        w.observers += [h, Lab(h)]
        t0 = time.time()
        for _ in range(years):
            for _ in range(WEEKS_PER_YEAR):
                w.step()
            if not w.living():
                break
    finally:
        biology.body_phase = ORIGINAL
    if w.year >= 100:
        sw, _ = load_snapshot(SAVED / f"seed_{seed}_year100.json.gz")
    else:
        sw, _ = load_snapshot(SAVED / f"seed_{seed}_end.json.gz")
    check = sw.tick == w.tick and sw.state_hash() == w.state_hash()
    out = {"code": CODE, "seed": seed, "years": w.year, "identical": check, "seconds": round(time.time() - t0),
           "counts": dict(c)}
    (OUT / f"feed_{CODE}_seed_{seed}.json").write_text(json.dumps(out), encoding="utf-8")
    return out


if __name__ == "__main__":
    for s in [int(a) for a in sys.argv[2:]]:
        if (OUT / f"feed_{CODE}_seed_{s}.json").exists():
            print(f"{CODE} seed {s}: already done", flush=True)
            continue
        r = run(s)
        print(f"{CODE} seed {s}: {r['years']} years, {r['seconds']}s, identical: {r['identical']}", flush=True)
