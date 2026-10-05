"""O3 feasibility pilot (read-only, descriptive). Replays the E7 code (control), seeds 301–304, 120 years. For every
death from starvation (any age): how many adults are within sight (perception), and how many of them, at the next
autumn, are alive and caring for children.

  python experiments/E10_loss/run_o3_pilot.py all
"""
from __future__ import annotations

import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
E7 = HERE.parent / "E7_passive"
sys.path.insert(0, str(E7 / "code_e7"))
from acl.config import Config  # noqa: E402
from acl.world import World  # noqa: E402

SEEDS = (301, 302, 303, 304)
WPY, WPS = 52, 13
OUT = HERE / "output_o3_pilot"


class Probe:
    def __init__(self):
        self.pops = []
        self.events = []        # per starvation death: season, age, witnesses, settled next autumn

    def __call__(self, world, events):
        tick = world.tick - 1
        s = (tick % WPY) // WPS
        c = world.cfg
        for e in events:
            if e["k"] == "death" and e.get("cause") == "starvation" and e.get("a") in world.people:
                p = world.people[e["a"]]
                wit = [q.id for q in world.people_near(p.loc, c.perception, exclude=p.id)
                       if q.alive and q.age(tick) >= 16 * WPY]
                self.events.append({"tick": tick, "season": s, "child": p.age(tick) < 12 * WPY,
                                    "witnesses": wit, "with_children_next_autumn": None})
        living = world.living()
        if tick % 520 == 519:
            self.pops.append(len(living))
        if tick % WPY == 2 * WPS:
            for ev in self.events:
                if ev["with_children_next_autumn"] is None and 0 < tick - ev["tick"] < WPY:
                    ev["with_children_next_autumn"] = sum(
                        1 for q in ev["witnesses"] if world.people[q].alive and world.dependents(q))


def run(seed):
    saved = json.loads((HERE.parent / "E9_anticipation" / "output" / f"arm0_seed_{seed}.json").read_text(encoding="utf-8"))
    w = World(Config(seed=seed))
    probe = Probe()
    w.observers.append(probe)
    for _ in range(120 * WPY):
        w.step()
    res = {"seed": seed, "replay_matches": probe.pops == saved["pops"], "events": probe.events}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"seed {seed}: replay matches {res['replay_matches']}, starvation deaths {len(probe.events)}", flush=True)


def verify(seed=304, years=20):
    hs = []
    for with_probe in (False, True):
        w = World(Config(seed=seed))
        if with_probe:
            w.observers.append(Probe())
        for _ in range(years * WPY):
            w.step()
        hs.append(w.state_hash())
    ok = hs[0] == hs[1]
    print("verify:", "READ-ONLY" if ok else "CHANGES THE WORLD", flush=True)
    return ok


if __name__ == "__main__":
    if sys.argv[1] == "verify":
        sys.exit(0 if verify() else 1)
    elif sys.argv[1] == "all":
        me = [sys.executable, str(Path(__file__).resolve())]
        if subprocess.call(me + ["verify"]) != 0:
            sys.exit("ABORT")
        with ThreadPoolExecutor(4) as pool:
            list(pool.map(lambda s: subprocess.call(me + [str(s)]), SEEDS))
    else:
        run(int(sys.argv[1]))
