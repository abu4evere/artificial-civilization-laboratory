"""O4 feasibility pilot (read-only, descriptive). Replays the E7 code (control), seeds 301–304, 120 years. How often
are stories of deaths from starvation told, to how many people, and how long after the death are they still told?

  python experiments/E11_stories/run_o4_pilot.py all
"""
from __future__ import annotations

import json
import statistics
import subprocess
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
E7 = HERE.parent / "E7_passive"
sys.path.insert(0, str(E7 / "code_e7"))
from acl.config import Config  # noqa: E402
from acl.world import World  # noqa: E402

SEEDS = (301, 302, 303, 304)
WPY = 52
OUT = HERE / "output_o4_pilot"


class Probe:
    def __init__(self):
        self.pops = []
        self.death_eid = {}          # eid -> (cause, tick)
        self.tellings = Counter()    # (cause) -> tellings
        self.accepted = Counter()
        self.listeners = defaultdict(set)   # starvation eid -> listeners who accepted
        self.lags = []               # years between a starvation death and each telling of it
        self.all_tellings = 0

    def __call__(self, world, events):
        tick = world.tick - 1
        for e in events:
            if e["k"] == "death":
                self.death_eid[e["id"]] = (e.get("cause"), tick)
            elif e["k"] == "told":
                self.all_tellings += 1
                d = self.death_eid.get(e.get("story"))
                if d:
                    cause = "starvation" if d[0] == "starvation" else "other death"
                    self.tellings[cause] += 1
                    if e.get("heard") == "accepted":
                        self.accepted[cause] += 1
                        if cause == "starvation":
                            self.listeners[e["story"]].add(e.get("b"))
                    if cause == "starvation":
                        self.lags.append((tick - d[1]) / WPY)
        if tick % 520 == 519:
            self.pops.append(len(world.living()))


def run(seed):
    saved = json.loads((HERE.parent / "E9_anticipation" / "output" / f"arm0_seed_{seed}.json").read_text(encoding="utf-8"))
    w = World(Config(seed=seed))
    probe = Probe()
    w.observers.append(probe)
    for _ in range(120 * WPY):
        w.step()
    starv = [k for k, v in probe.death_eid.items() if v[0] == "starvation"]
    res = {"seed": seed, "replay_matches": probe.pops == saved["pops"], "starvation_deaths": len(starv),
           "all_tellings": probe.all_tellings, "tellings": dict(probe.tellings), "accepted": dict(probe.accepted),
           "starvation_stories_ever_told": sum(1 for k in starv if probe.listeners.get(k) or k in {e for e in probe.listeners}),
           "listeners_per_story": [len(probe.listeners.get(k, ())) for k in starv],
           "lag_years": probe.lags}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(f"seed {seed}: replay matches {res['replay_matches']}", flush=True)


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
