"""E8, Arms 0 and 1 (amendment_1.md, A6–A9). Seeds 301–304, 120 years, a read-only probe every 10 years.

Usage:
  python experiments/E8_crucible/run_arm1.py <arm> <seed>      # arm: arm0 (E7 code) or arm1 (E7 code + rule R2)
  python experiments/E8_crucible/run_arm1.py verify <arm> <seed>
  python experiments/E8_crucible/run_arm1.py all               # verify both, then 8 runs, 4 at a time
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
E7 = HERE.parent / "E7_passive"
CODE = {"arm0": E7 / "code_e7", "arm1": HERE / "code_arm1"}
SEEDS = (301, 302, 303, 304)
YEARS = 120
WPY = 52
LATER_BORN = 30 * WPY


def setup(arm):
    sys.path.insert(0, str(CODE[arm]))
    sys.path.insert(1, str(E7))
    import acl
    assert Path(acl.__file__).resolve().parent == (CODE[arm] / "acl").resolve()


class Probe:
    def __init__(self):
        self.decades = {}
        self.samples = []
        self.pops10 = []
        self.starved = 0
        self.deaths = Counter()

    def __call__(self, world, events):
        tick = world.tick - 1
        d = self.decades.setdefault(tick // 520, Counter())
        for e in events:
            if e["k"] == "make":
                d["deliberate"] += 1
            elif e["k"] == "play" and e.get("thing"):
                d["play_made"] += 1
            elif e["k"] == "death":
                self.deaths[e.get("cause")] += 1
        living = world.living()
        d["person_weeks"] += len(living)
        if tick % 520 == 519:
            self.pops10.append(len(living))
            self._sample(world, tick, living)

    def _sample(self, world, tick, living):
        later = [p for p in living if p.birth > LATER_BORN and p.age(world.tick) >= 16 * WPY]
        held = Counter(sig for p in living for sig in p.recipes)
        sk = [p.skills["crafting"] for p in later]
        self.samples.append({
            "year": tick // WPY + 1,
            "population": len(living),
            "later_born_adults": len(later),
            "later_skill_mean": round(sum(sk) / len(sk), 3) if sk else None,
            "later_skill_best": round(max(sk), 3) if sk else None,
            "recipes_unique": len(held),
            "composite_share": round(sum(1 for s in held if s.startswith("(")) / len(held), 3) if held else None,
            "held_by_3": sorted(s for s, n in held.items() if n >= 3),
            "food_per_person": round(sum(p.food + p.seeds for p in living) / len(living), 2) if living else None,
        })


def code_fp(arm):
    from run_e7 import code_hash
    return code_hash(CODE[arm] / "acl")


def run(arm, seed):
    setup(arm)
    from acl.config import Config
    from acl.world import World
    fp = code_fp(arm)
    w = World(Config(seed=seed))
    probe = Probe()
    w.observers.append(probe)
    t0 = time.time()
    for _ in range(YEARS * WPY):
        w.step()
        if not w.living():
            break
    saved = json.loads((E7 / "output" / "e7" / f"seed_{seed}.json").read_text(encoding="utf-8"))
    saved_pops = [s["population"] for s in saved["samples"]][: len(probe.pops10)]
    out = {"arm": arm, "seed": seed, "years": w.year, "code_hash": fp, "code_hash_after": code_fp(arm),
           "matches_saved_e7": probe.pops10 == saved_pops,     # expected True for arm0 only
           "samples": probe.samples, "decades": {str(k): dict(v) for k, v in sorted(probe.decades.items())},
           "deaths": dict(probe.deaths), "seconds": round(time.time() - t0)}
    (HERE / "output").mkdir(exist_ok=True)
    (HERE / "output" / f"{arm}_seed_{seed}.json").write_text(json.dumps(out), encoding="utf-8")
    print(f"{arm} seed {seed}: {w.year} years, alive {len(w.living())}, matches saved E7: {out['matches_saved_e7']}, "
          f"{out['seconds']}s", flush=True)


def verify(arm, seed, years=20):
    setup(arm)
    from acl.config import Config
    from acl.world import World
    hs = []
    for with_probe in (False, True):
        w = World(Config(seed=seed))
        if with_probe:
            w.observers.append(Probe())
        for _ in range(years * WPY):
            w.step()
        hs.append(w.state_hash())
    ok = hs[0] == hs[1]
    line = f"{arm} seed {seed}, {years} years: {hs[0][:16]} / {hs[1][:16]} -> {'READ-ONLY' if ok else 'CHANGES THE WORLD'}"
    print(line, flush=True)
    (HERE / "output").mkdir(exist_ok=True)
    with open(HERE / "output" / "verify.txt", "a", encoding="utf-8") as f:
        f.write(line + "\n")
    return ok


def run_all():
    me = [sys.executable, str(Path(__file__).resolve())]
    for arm in ("arm0", "arm1"):
        if subprocess.call(me + ["verify", arm, "304"]) != 0:
            print("ABORT: probe changes the world", flush=True)
            return
    jobs = [(a, s) for a in ("arm0", "arm1") for s in SEEDS if not (HERE / "output" / f"{a}_seed_{s}.json").exists()]
    with ThreadPoolExecutor(max_workers=4) as pool:
        codes = list(pool.map(lambda j: subprocess.call(me + [j[0], str(j[1])]), jobs))
    for (a, s), c in zip(jobs, codes):
        if c != 0:
            print(f"{a} seed {s}: CRASHED", flush=True)
    print("ALL DONE", flush=True)


if __name__ == "__main__":
    if sys.argv[1] == "all":
        run_all()
    elif sys.argv[1] == "verify":
        sys.exit(0 if verify(sys.argv[2], int(sys.argv[3])) else 1)
    else:
        run(sys.argv[1], int(sys.argv[2]))
