"""E9.2 children autopsy (E9_2_children_autopsy.md). Read-only replays of E9 arm0 and a2full, seeds 301–304.

  python experiments/E9_anticipation/run_e92.py all
"""
from __future__ import annotations

import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
E7 = HERE.parent / "E7_passive"
ARMS = {"arm0": (E7 / "code_e7", None), "a2full": (HERE / "code_a2", 1.0)}
SEEDS = (301, 302, 303, 304)
WPY, WPS = 52, 13
OUT = HERE / "output_e92"


def setup(arm):
    sys.path.insert(0, str(ARMS[arm][0]))
    import acl
    assert Path(acl.__file__).resolve().parent == (ARMS[arm][0] / "acl").resolve()


def make_world(arm, seed):
    from acl.config import Config
    from acl.world import World
    w = ARMS[arm][1]
    return World(Config(seed=seed) if w is None else Config(seed=seed, anticipation_weight=w))


class Probe:
    def __init__(self):
        self.pops = []
        self.cohort = {}
        self.rows = []

    def __call__(self, world, events):
        tick = world.tick - 1
        wk = tick % WPY
        for e in events:
            if e["k"] == "death" and e.get("cause") == "starvation" and e.get("a") in self.cohort:
                self.cohort[e["a"]]["starved"] = True
        living = world.living()
        if tick % 520 == 519:
            self.pops.append(len(living))
        if wk == 3 * WPS:
            self.cohort = {}
            for p in living:
                if p.age(world.tick) >= 12 * WPY:
                    continue
                cid = p.caregiver or p.mother
                carer = world.people.get(cid) if cid else None
                food = round(carer.food + carer.seeds, 1) if carer and carer.alive else None
                self.cohort[p.id] = {"stage": p.stage(world.tick), "carer_food": food, "starved": False}
        if wk == WPY - 1:
            self.rows.extend(self.cohort.values())
            self.cohort = {}


def run(arm, seed):
    setup(arm)
    saved = json.loads((HERE / "output" / f"{arm}_seed_{seed}.json").read_text(encoding="utf-8"))
    w = make_world(arm, seed)
    probe = Probe()
    w.observers.append(probe)
    for _ in range(120 * WPY):
        w.step()
    res = {"arm": arm, "seed": seed, "replay_matches_e9": probe.pops == saved["pops"], "rows": probe.rows}
    OUT.mkdir(exist_ok=True)
    (OUT / f"{arm}_seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"{arm} seed {seed}: replay matches E9 {res['replay_matches_e9']}, child-winters {len(probe.rows)}", flush=True)


def verify(arm, seed=304, years=20):
    setup(arm)
    hs = []
    for with_probe in (False, True):
        w = make_world(arm, seed)
        if with_probe:
            w.observers.append(Probe())
        for _ in range(years * WPY):
            w.step()
        hs.append(w.state_hash())
    ok = hs[0] == hs[1]
    print(f"verify {arm}:", "READ-ONLY" if ok else "CHANGES THE WORLD", flush=True)
    return ok


if __name__ == "__main__":
    if sys.argv[1] == "verify":
        sys.exit(0 if verify(sys.argv[2]) else 1)
    elif sys.argv[1] == "all":
        me = [sys.executable, str(Path(__file__).resolve())]
        for arm in ARMS:
            if subprocess.call(me + ["verify", arm]) != 0:
                sys.exit("ABORT")
        with ThreadPoolExecutor(4) as pool:
            list(pool.map(lambda j: subprocess.call(me + [j[0], str(j[1])]), [(a, s) for a in ARMS for s in SEEDS]))
    else:
        run(sys.argv[1], int(sys.argv[2]))
